"""The ship, from its parameters. Works on floats (one run) or arrays (Monte Carlo draws).

Layout (phase 0): a torus spun for gravity, inside a radiation shield that does not spin; fusion
power plants and radiators off the spin; a power-limited drive with its own plants.
"""

from __future__ import annotations

from collections.abc import Mapping

import numpy as np

from . import physics as ph
from .constants import DAY, G0, HOUR, M_AIR, R_GAS, WEEK, YEAR

SCENARIOS = ("park", "tour", "brisk")


def ship(v: Mapping[str, float | np.ndarray]) -> dict[str, np.ndarray]:
    """Everything but the drive. Masses in tonnes, power in MW, lengths in m."""
    n = v["mission.population"]

    # Spin and size.
    g, rpm = v["habitat.gravity_g"], v["habitat.rpm"]
    w = ph.omega(rpm)
    R = ph.spin_radius(g, rpm)
    # R is the outer floor's distance from the spin axis (gravity_g there). People live where
    # gravity is within gravity_band of that (SP-413: 0.9-1 g), so a ring holds the tube's
    # volume within band x R of the floor; as many rings as the usable volume needs, stacked along
    # the spin axis, each in its own still shield.
    #
    # Hockey: rinks lie across the tube, their long side parallel to the spin axis, so rushes end
    # to end feel no Coriolis force; skating along the ring changes a skater's weight
    # (ring_weight_factor). The tube must hold a rink pad across it. Rinks are sized by ice time;
    # training, recovery and sports-medicine space by person; both add to the lived-in volume.
    pad_l, pad_w, pad_h = v["athletics.rink.length"], v["athletics.rink.width"], v["athletics.rink.height"]
    session = v["athletics.skaters_per_session"] * v["athletics.rink_open_hours"]
    ice_sheets = np.ceil(n * v["athletics.ice_hours"] / session)
    roller_rinks = np.ceil(n * v["athletics.roller_hours"] / session)
    sheet_volume = pad_l * pad_w * pad_h + v["athletics.rink.support_area"] * v["athletics.rink.support_height"]
    rink_volume = (ice_sheets + roller_rinks) * sheet_volume
    athletic_volume = rink_volume + n * v["athletics.facility_volume_per_person"]
    # Injuries (sports medicine's load): game and practice hours at their injury rates.
    games = v["athletics.game_share"]
    rate = games * v["athletics.injury_rate_game"] + (1.0 - games) * v["athletics.injury_rate_practice"]
    injuries = (v["athletics.ice_hours"] + v["athletics.roller_hours"]) * (YEAR / WEEK) * rate / 1e3
    lived_in = n * v["habitat.usable_volume_per_person"] + athletic_volume
    r = np.maximum(v["habitat.tube_ratio"] * R, ph.box_tube_radius(pad_l, pad_h))
    usable_ring = ph.band_volume(R, r, v["habitat.gravity_band"])
    rings = np.ceil(lived_in / usable_ring)
    Rf = R
    R = Rf - r  # the torus's major radius (tube centre)
    volume = rings * ph.torus_volume(R, r)

    # Pressure shell, air, interior.
    p = v["habitat.air_pressure"] * 1e3
    rho, sigma = v["habitat.shell.density"], v["habitat.shell.allowable_stress"] * 1e6
    t_shell = ph.torus_shell_thickness(p, R, r, sigma)
    area = rings * ph.torus_area(R, r)
    shell = area * t_shell * rho
    air = volume * p * M_AIR / (R_GAS * v["habitat.air_temperature"])
    interior = n * v["habitat.interior_mass_per_person"] * 1e3

    # Care by robots (Jon: massage, cooking etc. are AI/robotic): massage tables sized by the
    # hours of table massage a person gets, kitchen lines by meals, humanoid robots by the hours
    # of hands-on care (stretching, physio) and chores (cooking prep, cleaning, laundry) they do,
    # at a robot's pace; spares for the time robots are down.
    spare = 1.0 + v["care.spares"]
    stations = np.ceil(n * v["care.bodywork_hours"] / v["care.station_hours"] * spare)
    kitchens = np.ceil(n * v["care.meals_per_day"] / (v["care.kitchen_meals_per_hour"] * v["care.kitchen_hours"]) * spare)
    work = n * (v["care.hands_on_hours"] + v["care.chore_hours"]) * v["care.robot_pace"]
    humanoids = np.ceil(work / v["care.humanoid_duty_hours"] * spare)
    robots = (stations * v["care.station_mass"] + kitchens * v["care.kitchen_mass"] + humanoids * v["care.humanoid_mass"]) * 1e3
    robot_w = (
        n * v["care.bodywork_hours"] / (WEEK / HOUR) * v["care.station_kw"]
        + kitchens * v["care.kitchen_hours"] / (DAY / HOUR) * v["care.kitchen_kw"]
        + humanoids * v["care.humanoid_kw"]
    ) * 1e3  # average over a week

    # The spinning ring carries the shell, air, interior and robots (and itself) against the spin.
    k = ph.ring_spin_factor(rho, w, Rf, sigma)  # at the outer floor, the worst case
    ring = ph.ring_structure_mass(shell + air + interior + robots, k)

    # Still shield round the tube.
    gap = v["habitat.shield.gap"]
    shield_area = rings * ph.torus_area(R, r + gap)
    shield = shield_area * v["habitat.shield.areal_density"] * 1e3

    # Power: food under lights plus everything else; all of it ends as heat in the habitat.
    food_w = ph.food_power(v["life.food_energy"], v["life.led_to_par"], v["life.par_to_food"])
    ice_w = ice_sheets * v["athletics.ice_plant_kw"] * 1e3
    p_elec = n * (food_w + v["life.other_power_per_person"] * 1e3) + ice_w + robot_w
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
    m_ring = (shell + air + interior + robots + np.nan_to_num(ring)) / rings
    i_one, i_one_cross = ph.torus_shell_inertia(m_ring, R, r)
    pitch = 2.0 * (r + gap)
    stack = m_ring * pitch**2 * (rings**2 - 1.0) * rings / 12.0  # sum of m z_i^2, rings centred
    i_spin, i_cross = rings * i_one, rings * i_one_cross + stack

    # Expeditions: reusable landers in a hangar at the still hub, each carried with propellant
    # for `sorties_carried` round trips from low orbit to the surface and back.
    lander_end = (v["expeditions.lander_dry"] + v["expeditions.payload"]) * 1e3
    sortie = ph.rocket_propellant(lander_end, v["expeditions.sortie_dv"] * 1e3, v["expeditions.isp"])
    landers = v["expeditions.landers"]
    expeditions = landers * (v["expeditions.lander_dry"] * 1e3 + v["expeditions.sorties_carried"] * sortie)

    dry = shield + shell + ring + air + interior + robots + plant_mass + radiators + expeditions
    return {
        "radius_m": Rf,
        "tube_centre_m": R,
        "tube_radius_m": r,
        "tube_over_radius": r / Rf,
        "volume_per_person_m3": volume / n,
        "rings": rings,
        "ice_sheets": ice_sheets,
        "roller_rinks": roller_rinks,
        "athletic_m3_per_person": athletic_volume / n,
        "injuries_per_person_year": injuries,
        "surgeries_per_year": n * injuries * v["athletics.surgery_fraction"],
        "skate_weight_with_spin": ph.ring_weight_factor(w, g * G0, v["athletics.skate_speed"]),
        "skate_weight_against_spin": ph.ring_weight_factor(w, g * G0, -v["athletics.skate_speed"]),
        "bodywork_stations": stations,
        "kitchen_lines": kitchens,
        "humanoids": humanoids,
        "robots_t": robots / 1e3,
        "robot_mw": robot_w / 1e6,
        "ice_mw": ice_w / 1e6,
        "landers": landers * np.ones_like(np.asarray(n, dtype=float)),
        "sortie_propellant_t": sortie / 1e3,
        "expeditions_t": expeditions / 1e3,
        "spin_stable": i_spin / i_cross >= v["habitat.min_inertia_ratio"],
        "rim_speed_m_s": w * Rf,
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
