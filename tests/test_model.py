"""The whole model: it runs, adds up, and its Monte Carlo is ordered."""

import numpy as np
import pytest

from mothership.cli import main
from mothership.model import SCENARIOS, TOUR, run, tour_dv
from mothership.params import check_params, draw, load_params, values

PARTS = ("shield_t", "shell_t", "ring_t", "air_t", "interior_t", "robots_t", "plants_t", "radiators_t", "expeditions_t", "collider_t")


def test_params_clean():
    assert check_params(load_params()) == []


def test_central_run_adds_up():
    r = run(values(load_params()))
    s = r["ship"]
    assert np.isfinite(s["dry_t"])
    assert sum(float(s[k]) for k in PARTS) == pytest.approx(float(s["dry_t"]), rel=1e-12)
    park = r["park"]
    assert float(park["start_t"]) == float(s["dry_t"])  # no burn, no drive
    for sc in SCENARIOS:
        v = r[sc]
        if bool(v["feasible"]):
            total = float(s["dry_t"]) + float(v["propellant_t"]) + float(v["drive_t"]) + float(v["tanks_t"])
            assert total == pytest.approx(float(v["start_t"]), rel=1e-9)


def test_monte_carlo_ordered_and_deterministic():
    params = load_params()
    a = run(draw(params, 2000, 3))["ship"]["dry_t"]
    b = run(draw(params, 2000, 3))["ship"]["dry_t"]
    assert np.array_equal(a, b)
    p10, p50, p90 = np.percentile(a, [10, 50, 90])
    assert p10 <= p50 <= p90


def test_cli_check_passes():
    assert main(["check"]) == 0


def test_hockey_ship_parts():
    v = values(load_params())
    s = run(v)["ship"]
    n = v["mission.population"]
    session = v["athletics.skaters_per_session"] * v["athletics.rink_open_hours"]
    assert float(s["ice_sheets"]) == np.ceil(n * v["athletics.ice_hours"] / session)
    # a rink hall fits across the tube
    from mothership import physics as ph
    assert float(s["tube_radius_m"]) >= ph.box_tube_radius(v["athletics.rink.length"], v["athletics.rink.height"])
    # skaters are heavier with the spin, lighter against it
    assert float(s["skate_weight_with_spin"]) > 1.0 > float(s["skate_weight_against_spin"])
    # landers: dry mass plus the propellant carried (the mean sortie x sorties at every stop)
    sortie = float(s["sortie_propellant_t"])
    assert float(s["expeditions_t"]) == pytest.approx(
        v["expeditions.landers"] * v["expeditions.lander_dry"] + len(TOUR) * v["expeditions.sorties_per_stop"] * sortie
    )
    # parked higher than low orbit, a lander's round trip costs more than from low orbit
    from mothership.model import sortie_dv
    assert float(sortie_dv(v, "callisto")) > v["expeditions.sortie_dv"]


def test_tour_dv_adds_up():
    v = values(load_params())
    t = tour_dv(v)
    assert float(t["total_km_s"]) == pytest.approx(sum(float(x) for k, x in t.items() if k != "total_km_s"))
    # coplanar, out and back through planets ever farther from the Sun: the legs climb out of the
    # Sun's well and fall back in, 2 (v_earth - v_outermost)
    flat = dict(v)
    for body in ("earth", "mars", "ceres", "jupiter", "saturn"):
        flat[f"worlds.{body}.inclination"] = 0.0
    flat["tour.edelbaum_eps_max"] = 1e9  # every leg an Edelbaum spiral
    from mothership import physics as ph
    vc = lambda b: ph.circular_speed(v["worlds.sun.gm"], v[f"worlds.{b}.orbit"])
    outer = TOUR[-1].split(".")[0]
    assert float(tour_dv(flat)["legs_km_s"]) == pytest.approx(2 * (vc("earth") - vc(outer)))


def test_science_parts():
    v = values(load_params())
    s = run(v)["ship"]
    from mothership import physics as ph
    ring = float(s["radius_m"]) + v["habitat.shield.gap"]
    assert float(s["collider_t"]) == pytest.approx(2 * np.pi * ring * v["science.collider.cold_mass"])
    rho = v["science.collider.fill"] * ring
    assert float(s["collider_tev"]) == pytest.approx(ph.collider_energy_tev(v["science.collider.field"], rho))
    n = v["mission.population"]
    mw = (n * v["science.share"] * v["science.kw_per_researcher"] + n * v["science.data_kw_per_person"] + v["science.zero_g_kw"]) / 1e3
    mw += v["science.collider.power_mw"] + v["science.light_source_mw"]
    assert float(s["science_mw"]) == pytest.approx(mw)


def test_food_system_accounts():
    from mothership.model import CROPS, GARDENS, OTHER_FOOD, food_system
    v = values(load_params())
    q = dict(v)
    for s in OTHER_FOOD:
        q[f"food.{s}.share"] = 0.0
    q["life.yield_gain"] = 1.0
    n = 1.0
    f = food_system(q, n)
    shares = sum(q[f"crops.{c}.share"] for c in CROPS)
    crop_area = sum(q["life.food_energy"] * q[f"crops.{c}.share"] / shares / q[f"crops.{c}.yield"] for c in CROPS)
    assert float(f["crop_area"]) == pytest.approx(crop_area)
    gardens = sum(q[f"food.garden.{g}_area"] for g in GARDENS)
    assert float(f["area"]) == pytest.approx(crop_area + gardens + q["food.pharma.grow_area"])
    protein = sum(
        q["life.food_energy"] * q[f"crops.{c}.share"] / shares / q[f"crops.{c}.kcal_per_g"] * q[f"crops.{c}.protein_per_g"]
        for c in CROPS
    )
    assert float(f["protein"]) == pytest.approx(protein)
    assert float(f["crop_share"]) == pytest.approx(1.0)
    # moving calories to single-cell protein cuts the food power
    r = dict(q)
    r["food.scp.share"] = 0.2
    assert float(food_system(r, n)["power"]) < float(f["power"])
