"""The ship, from its parameters. Works on floats (one run) or arrays (Monte Carlo draws).

Layout (phase 0): a torus spun for gravity, inside a radiation shield that does not spin; fusion
power plants and radiators off the spin; a power-limited drive with its own plants.
"""

from __future__ import annotations

from collections.abc import Mapping

import numpy as np

from . import physics as ph
from .constants import M_AIR, R_GAS, YEAR

SCENARIOS = ("park", "tour", "brisk")


def ship(v: Mapping[str, float | np.ndarray]) -> dict[str, np.ndarray]:
    """Everything but the drive. Masses in tonnes, power in MW, lengths in m."""
    n = v["mission.population"]

    # Spin and size.
    g, rpm = v["habitat.gravity_g"], v["habitat.rpm"]
    w = ph.omega(rpm)
    R = ph.spin_radius(g, rpm)
    volume = n * v["habitat.volume_per_person"]
    # As many rings as the volume needs, each tube no wider than max_tube_ratio x R; the rings
    # stack along the spin axis, each in its own still shield.
    ring_max = ph.torus_volume(R, v["habitat.max_tube_ratio"] * R)
    rings = np.ceil(volume / ring_max)
    r = ph.torus_tube_radius(volume / rings, R)

    # Pressure shell, air, interior.
    p = v["habitat.air_pressure"] * 1e3
    rho, sigma = v["habitat.shell.density"], v["habitat.shell.allowable_stress"] * 1e6
    t_shell = ph.torus_shell_thickness(p, R, r, sigma)
    area = rings * ph.torus_area(R, r)
    shell = area * t_shell * rho
    air = volume * p * M_AIR / (R_GAS * v["habitat.air_temperature"])
    interior = n * v["habitat.interior_mass_per_person"] * 1e3

    # The spinning ring carries the shell, air and interior (and itself) against the spin.
    k = ph.ring_spin_factor(rho, w, R, sigma)
    ring = ph.ring_structure_mass(shell + air + interior, k)

    # Still shield round the tube.
    gap = v["habitat.shield.gap"]
    shield_area = rings * ph.torus_area(R, r + gap)
    shield = shield_area * v["habitat.shield.areal_density"] * 1e3

    # Power: food under lights plus everything else; all of it ends as heat in the habitat.
    food_w = ph.food_power(v["life.food_energy"], v["life.led_to_par"], v["life.par_to_food"])
    p_elec = n * (food_w + v["life.other_power_per_person"] * 1e3)
    unit = v["power.unit_mwe"] * 1e6
    plants = np.ceil(p_elec / unit) + v["power.spares"]
    plant_mass = plants * v["power.unit_mwe"] * v["power.specific_mass"] * 1e3
    eta = v["power.thermal_efficiency"]
    waste = p_elec * (1.0 - eta) / eta
    eps = v["power.emissivity"]
    rad_area = ph.radiator_area(waste, v["power.plant_radiator_temp"], eps) + ph.radiator_area(
        p_elec, v["power.habitat_radiator_temp"], eps
    )
    radiators = rad_area * v["power.radiator_areal_density"]

    # Spin stability of the spinning stack (each ring as a thin shell of its share of the
    # spinning mass, rings 2 (r + gap) apart along the axis).
    m_ring = (shell + air + interior + np.nan_to_num(ring)) / rings
    i_one, i_one_cross = ph.torus_shell_inertia(m_ring, R, r)
    pitch = 2.0 * (r + gap)
    stack = m_ring * pitch**2 * (rings**2 - 1.0) * rings / 12.0  # sum of m z_i^2, rings centred
    i_spin, i_cross = rings * i_one, rings * i_one_cross + stack
    dry = shield + shell + ring + air + interior + plant_mass + radiators
    return {
        "radius_m": R,
        "tube_radius_m": r,
        "tube_over_radius": r / R,
        "rings": rings,
        "spin_stable": i_spin / i_cross >= v["habitat.min_inertia_ratio"],
        "rim_speed_m_s": w * R,
        "shell_thickness_mm": t_shell * 1e3,
        "ring_spin_factor": k,
        "spin_inertia_ratio": i_spin / i_cross,
        "shield_t": shield / 1e3,
        "shell_t": shell / 1e3,
        "ring_t": ring / 1e3,
        "air_t": air / 1e3,
        "interior_t": interior / 1e3,
        "plants_t": plant_mass / 1e3,
        "radiators_t": radiators / 1e3,
        "dry_t": dry / 1e3,
        "food_kw_per_person": food_w / 1e3,
        "power_mw": p_elec / 1e6,
        "plants": plants,
        "radiator_km2": rad_area / 1e6,
        "habitat_t_per_person": dry / 1e3 / n,
    }


def voyage(v: Mapping[str, float | np.ndarray], dry_t, scenario: str) -> dict[str, np.ndarray]:
    """The drive for one scenario, carrying the whole ship (`dry_t`, tonnes) as its payload."""
    dv = v[f"mission.scenario.{scenario}.dv"] * 1e3
    t = v[f"mission.scenario.{scenario}.years"] * YEAR
    alpha = v["propulsion.jet_specific_power"]
    frac, u, v_ch = ph.stuhlinger(dv, t, alpha, v["propulsion.tankage"])
    ok = frac > 0
    with np.errstate(divide="ignore", invalid="ignore"):
        m0 = np.where(ok, dry_t / frac, np.nan)
        e = np.exp(-np.where(dv > 0, dv / (u * v_ch), 0.0))
    prop = m0 * (1.0 - e)
    drive = prop * u**2
    tanks = prop * v["propulsion.tankage"]
    jet_mw = np.where(dv > 0, drive * 1e3 * alpha / 1e6, 0.0)
    return {
        "feasible": ok,
        "start_t": m0,
        "propellant_t": np.where(dv > 0, prop, 0.0),
        "drive_t": np.where(dv > 0, drive, 0.0),
        "tanks_t": np.where(dv > 0, tanks, 0.0),
        "jet_power_mw": jet_mw,
        "exhaust_km_s": np.where(dv > 0, u * v_ch / 1e3, np.nan),
        "payload_fraction": frac,
    }


def run(v: Mapping[str, float | np.ndarray]) -> dict[str, dict[str, np.ndarray]]:
    s = ship(v)
    return {"ship": s, **{sc: voyage(v, s["dry_t"], sc) for sc in SCENARIOS}}
