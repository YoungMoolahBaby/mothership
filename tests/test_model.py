"""The whole model: it runs, adds up, and its Monte Carlo is ordered."""

import numpy as np
import pytest

from mothership.cli import main
from mothership.model import SCENARIOS, run
from mothership.params import check_params, draw, load_params, values

PARTS = ("shield_t", "shell_t", "ring_t", "air_t", "interior_t", "robots_t", "plants_t", "radiators_t", "expeditions_t")


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
    # landers: dry mass plus the propellant carried
    sortie = float(s["sortie_propellant_t"])
    assert float(s["expeditions_t"]) == pytest.approx(
        v["expeditions.landers"] * (v["expeditions.lander_dry"] + v["expeditions.sorties_carried"] * sortie)
    )
