"""One run at the central values, Monte Carlo P10 / P50 / P90, and what drives the mass."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from .model import SCENARIOS, TOUR, run, tour_dv
from .params import Param, draw, values

SHIP_ROWS = [
    ("radius_m", "spin radius (outer floor)", "m", "{:,.0f}"),
    ("tube_centre_m", "ring radius (tube centre)", "m", "{:,.0f}"),
    ("rings", "rings", "", "{:,.0f}"),
    ("tube_radius_m", "tube radius", "m", "{:,.0f}"),
    ("rim_speed_m_s", "rim speed", "m/s", "{:,.0f}"),
    ("shield_t_per_m2", "shield water (dose with the magnet off at the fail-safe limit)", "t/m^2", "{:.2f}"),
    ("volume_per_person_m3", "enclosed volume per person", "m^3", "{:,.0f}"),
    ("shell_thickness_mm", "pressure shell", "mm steel", "{:,.0f}"),
    ("ice_sheets", "ice sheets", "", "{:,.0f}"),
    ("roller_rinks", "roller rinks", "", "{:,.0f}"),
    ("athletic_m3_per_person", "rinks, training, recovery, sports medicine per person", "m^3", "{:,.0f}"),
    ("injuries_per_person_year", "hockey injuries a person a year", "", "{:.1f}"),
    ("surgeries_per_year", "of which surgeries, ship-wide a year", "", "{:,.0f}"),
    ("skate_weight_with_spin", "skater at top speed along the ring, with the spin", "x weight", "{:.2f}"),
    ("skate_weight_against_spin", "same, against the spin", "x weight", "{:.2f}"),
    ("bodywork_stations", "robotic massage tables", "", "{:,.0f}"),
    ("kitchen_lines", "robotic kitchen lines", "", "{:,.0f}"),
    ("humanoids", "humanoid robots (hands-on care, chores)", "", "{:,.0f}"),
    ("crop_share", "food from LED crops (rest: microbes, fungi, fermented dairy, algae; vegan)", "of kcal", "{:.2f}"),
    ("crop_m2_per_person", "crop racks per person", "m^2", "{:,.0f}"),
    ("grow_m2_per_person", "all racks per person (crops, herbs, spices, medicine, grove)", "m^2", "{:,.0f}"),
    ("crop_kcal_per_mol", "crops: food per mol of light", "kcal/mol", "{:.2f}"),
    ("protein_g_per_kg", "protein per kg of body mass (athletes need ~1.6)", "g/kg/d", "{:.2f}"),
    ("farm_m3_per_person", "farm volume per person (anywhere in the tube)", "m^3", "{:,.0f}"),
    ("researchers", "people doing science (FTE)", "", "{:,.0f}"),
    ("science_m3_per_person", "labs per person (beyond SP-413)", "m^3", "{:,.0f}"),
    ("collider_tev", "collider round the ring, energy a beam", "TeV", "{:.1f}"),
    ("landers", "landers", "", "{:,.0f}"),
    ("sortie_propellant_t", "propellant a sortie", "t", "{:,.0f}"),
    ("power_mw", "electric power", "MW", "{:,.0f}"),
    ("food_kw_per_person", "of which food (lights, mist, fans, microbes, loop), per person", "kW", "{:,.1f}"),
    ("mist_mw", "of which high-pressure misters", "MW", "{:,.1f}"),
    ("ultrasonic_mist_mw", "(ultrasonic fog instead)", "MW", "{:,.1f}"),
    ("other_food_mw", "of which microbes, fungi, dairy, algae", "MW", "{:,.1f}"),
    ("ice_mw", "of which ice plants", "MW", "{:,.1f}"),
    ("cryo_mw", "of which the shield magnet's cryocoolers", "MW", "{:,.0f}"),
    ("robot_mw", "of which robots", "MW", "{:,.1f}"),
    ("science_mw", "of which science (labs, computing, collider, light source)", "MW", "{:,.1f}"),
    ("plants", "fusion plants (with spares)", "", "{:,.0f}"),
    ("radiator_km2", "radiator panels", "km^2", "{:,.2f}"),
    ("shield_t", "shield (water + magnet, fail-safe)", "t", "{:,.0f}"),
    ("magnet_t", "of which the magnet", "t", "{:,.0f}"),
    ("shell_t", "pressure shell", "t", "{:,.0f}"),
    ("ring_t", "spin ring structure", "t", "{:,.0f}"),
    ("air_t", "air", "t", "{:,.0f}"),
    ("interior_t", "interior", "t", "{:,.0f}"),
    ("robots_t", "robots", "t", "{:,.0f}"),
    ("plants_t", "fusion plants", "t", "{:,.0f}"),
    ("radiators_t", "radiators", "t", "{:,.0f}"),
    ("expeditions_t", "landers and their propellant", "t", "{:,.0f}"),
    ("collider_t", "collider magnets", "t", "{:,.0f}"),
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
        f"Population {params['mission.population'].value:,.0f}, built around adult ice and roller "
        "hockey with robotic care for all, sending expeditions to planets and moons. Layout: a "
        "torus spun for gravity inside a shield that does not spin, rinks across the tube; "
        "stellarator power plants and radiators off the spin; landers at the still hub; a "
        "power-limited drive with its own plants.",
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
    parts = tour_dv(values(params))
    lines += [
        "",
        f"## The tour: {' -> '.join(['earth', *TOUR, 'earth'])}",
        "",
        "Low-thrust legs between the planets (Edelbaum) and spirals into a low parking orbit at "
        "each stop and out again (for a moon, down its planet's well first). Central values:",
        "",
        "| part | delta-v (km/s) |",
        "|---|---|",
    ]
    for key, val in parts.items():
        if key != "total_km_s":
            lines.append(f"| {key.removesuffix('_km_s')} | {float(val):.1f} |")
    tot = _pct(np.asarray(tour_dv(d)["total_km_s"], dtype=float))
    lines.append(f"| **total** | **{float(parts['total_km_s']):.1f}** (P10-P90 {tot[0]:.1f}-{tot[2]:.1f}) |")
    lines += [
        "",
        "## Shield options",
        "",
        "The design's shield is the fail-safe hybrid (water for the dose with the magnet off, a magnet for the target); these would replace it (or, spinning, add to it):",
        "",
        "| | central | P10 | P50 | P90 | unit |",
        "|---|---|---|---|---|---|",
    ]
    for key, label in (
        ("shield_t", "fail-safe hybrid (the design)"),
        ("shield_water_only_t", "water alone for the dose target"),
        ("shield_regolith_t", "lunar regolith alone, same dose"),
        ("shield_active_t", "full magnet + thin water (not fail-safe)"),
        ("spinning_shield_extra_t", "extra ring structure to spin the shield"),
    ):
        c = float(base["ship"][key])
        p10, p50, p90 = _pct(np.asarray(mc["ship"][key], dtype=float))
        lines.append(f"| {label} | {_fmt('{:,.0f}', c)} | {_fmt('{:,.0f}', p10)} | {_fmt('{:,.0f}', p50)} | {_fmt('{:,.0f}', p90)} | t |")
    for sc in SCENARIOS:
        dv = float(base[sc]["dv_km_s"])
        yr = params[f"mission.scenario.{sc}.years"].value
        lines += [
            "",
            f"## Scenario `{sc}`: delta-v {dv:.1f} km/s over {yr:g} years",
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
