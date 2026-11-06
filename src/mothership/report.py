"""One run at the central values, Monte Carlo P10 / P50 / P90, and what drives the mass."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from .model import SCENARIOS, run
from .params import Param, draw, values

SHIP_ROWS = [
    ("radius_m", "spin radius", "m", "{:,.0f}"),
    ("rings", "rings", "", "{:,.0f}"),
    ("tube_radius_m", "tube radius", "m", "{:,.0f}"),
    ("rim_speed_m_s", "rim speed", "m/s", "{:,.0f}"),
    ("shell_thickness_mm", "pressure shell", "mm steel", "{:,.0f}"),
    ("power_mw", "electric power", "MW", "{:,.0f}"),
    ("food_kw_per_person", "of which food, per person", "kW", "{:,.1f}"),
    ("plants", "fusion plants (with spares)", "", "{:,.0f}"),
    ("radiator_km2", "radiator panels", "km^2", "{:,.2f}"),
    ("shield_t", "shield", "t", "{:,.0f}"),
    ("shell_t", "pressure shell", "t", "{:,.0f}"),
    ("ring_t", "spin ring structure", "t", "{:,.0f}"),
    ("air_t", "air", "t", "{:,.0f}"),
    ("interior_t", "interior", "t", "{:,.0f}"),
    ("plants_t", "fusion plants", "t", "{:,.0f}"),
    ("radiators_t", "radiators", "t", "{:,.0f}"),
    ("dry_t", "ship without drive", "t", "{:,.0f}"),
    ("habitat_t_per_person", "per person", "t", "{:,.0f}"),
]
VOYAGE_ROWS = [
    ("start_t", "start mass", "t", "{:,.0f}"),
    ("propellant_t", "propellant", "t", "{:,.0f}"),
    ("drive_t", "drive (its plants, radiators, thrusters)", "t", "{:,.0f}"),
    ("jet_power_mw", "jet power", "MW", "{:,.0f}"),
    ("exhaust_km_s", "exhaust speed", "km/s", "{:,.0f}"),
    ("payload_fraction", "ship / start mass", "", "{:.3f}"),
]


def _fmt(fmt: str, x: float) -> str:
    return "-" if not np.isfinite(x) else fmt.format(x)


def _pct(a: np.ndarray) -> tuple[float, float, float]:
    a = a[np.isfinite(a)]
    if a.size == 0:
        return (np.nan, np.nan, np.nan)
    return tuple(float(x) for x in np.percentile(a, [10, 50, 90]))


def _ranks(a: np.ndarray) -> np.ndarray:
    r = np.empty(a.size)
    r[np.argsort(a, kind="stable")] = np.arange(a.size)
    return r


def sensitivity(params: dict[str, Param], draws: dict[str, np.ndarray], out: np.ndarray, top: int = 10):
    """Spearman rank correlation of `out` with every parameter that varies."""
    ok = np.isfinite(out)
    ro = _ranks(out[ok])
    rows = []
    for k, p in params.items():
        if p.varies:
            rows.append((k, float(np.corrcoef(_ranks(draws[k][ok]), ro)[0, 1]), p.conf))
    rows.sort(key=lambda x: -abs(x[1]))
    return rows[:top]


def build(params: dict[str, Param], n: int = 5000, seed: int = 1) -> str:
    base = run(values(params))
    d = draw(params, n, seed)
    mc = run(d)
    lines = [
        "# Mothership sizing report",
        "",
        f"From `params/*.yaml` ({len(params)} parameters, "
        f"{sum(p.conf == 'placeholder' for p in params.values())} still placeholders). "
        f"Monte Carlo: {n} draws, seed {seed}, triangular(low, value, high). Masses in tonnes.",
        "",
        f"Population {params['mission.population'].value:,.0f}. Layout: a torus spun for gravity "
        "inside a shield that does not spin; stellarator power plants and radiators off the spin; "
        "a power-limited drive with its own plants.",
        "",
        "## The ship",
        "",
        "| | central | P10 | P50 | P90 | unit |",
        "|---|---|---|---|---|---|",
    ]
    for key, label, unit, fmt in SHIP_ROWS:
        c = float(base["ship"][key])
        p10, p50, p90 = _pct(np.asarray(mc["ship"][key], dtype=float))
        lines.append(f"| {label} | {_fmt(fmt, c)} | {_fmt(fmt, p10)} | {_fmt(fmt, p50)} | {_fmt(fmt, p90)} | {unit} |")
    s = base["ship"]
    lines += [
        "",
        f"Checks at the central values: tube / spin radius {float(s['tube_over_radius']):.2f}; "
        f"ring spin factor rho w^2 R^2 / sigma {float(s['ring_spin_factor']):.3f} (must stay under 1); "
        f"spin-axis / cross-axis inertia {float(s['spin_inertia_ratio']):.2f} (above 1: spin is stable).",
        f"Across the draws: spin stable with margin in {float(np.mean(mc['ship']['spin_stable'])):.0%}; "
        f"rings needed P10 / P50 / P90 {' / '.join(f'{x:.0f}' for x in _pct(np.asarray(mc['ship']['rings'], dtype=float)))}.",
    ]
    for sc in SCENARIOS:
        dv = params[f"mission.scenario.{sc}.dv"].value
        yr = params[f"mission.scenario.{sc}.years"].value
        lines += [
            "",
            f"## Scenario `{sc}`: delta-v {dv:g} km/s over {yr:g} years",
            "",
            "| | central | P10 | P50 | P90 | unit |",
            "|---|---|---|---|---|---|",
        ]
        for key, label, unit, fmt in VOYAGE_ROWS:
            c = float(base[sc][key])
            p10, p50, p90 = _pct(np.asarray(mc[sc][key], dtype=float))
            lines.append(f"| {label} | {_fmt(fmt, c)} | {_fmt(fmt, p10)} | {_fmt(fmt, p50)} | {_fmt(fmt, p90)} | {unit} |")
        feas = float(np.mean(mc[sc]["feasible"]))
        lines.append("")
        lines.append(f"Feasible in {feas:.0%} of draws (the drive can carry the ship at all).")
        if feas > 0.05:
            lines += ["", f"What drives the start mass (Spearman rank correlation, feasible draws):", ""]
            for k, rho, conf in sensitivity(params, d, np.asarray(mc[sc]["start_t"], dtype=float)):
                lines.append(f"- `{k}` {rho:+.2f} ({conf})")
    return "\n".join(lines) + "\n"


def write(params: dict[str, Param], path: Path, n: int = 5000, seed: int = 1) -> str:
    text = build(params, n, seed)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return text
