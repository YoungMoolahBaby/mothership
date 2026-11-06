"""The closed forms in physics.py against independent results."""

import numpy as np
import pytest

from mothership import physics as ph
from mothership.constants import G0, SIGMA, YEAR


def test_spin_radius():
    # r = g / w^2: 1 g at 1 rpm is 894.26 m (the Stanford torus spun at 1 rpm on a ring about
    # 1.8 km across), at 2 rpm a quarter of that.
    assert ph.spin_radius(1.0, 1.0) == pytest.approx(G0 / (2 * np.pi / 60) ** 2)
    assert ph.spin_radius(1.0, 1.0) == pytest.approx(894.26, abs=0.01)
    assert ph.spin_radius(1.0, 2.0) == pytest.approx(894.26 / 4, abs=0.01)


def test_torus_volume_and_area_by_integration():
    R, r = 300.0, 70.0
    th = np.linspace(0, 2 * np.pi, 4001)[:-1]
    # Pappus: volume = disc area x path of its centroid; area by integrating the surface element.
    rho = np.linspace(0, r, 4001)
    disc = np.trapezoid(2 * np.pi * rho, rho)
    assert ph.torus_volume(R, r) == pytest.approx(disc * 2 * np.pi * R, rel=1e-8)
    area = np.mean(r * (R + r * np.cos(th))) * (2 * np.pi) ** 2
    assert ph.torus_area(R, r) == pytest.approx(area, rel=1e-12)
    assert ph.torus_tube_radius(ph.torus_volume(R, r), R) == pytest.approx(r)


def test_torus_shell_thickness():
    p, s = 101.3e3, 300e6
    # A thin tube tends to the cylinder's p r / sigma; at R = 2r the inner-equator factor is 3/2.
    assert ph.torus_shell_thickness(p, 1e6, 10.0, s) == pytest.approx(p * 10 / s, rel=1e-5)
    assert ph.torus_shell_thickness(p, 20.0, 10.0, s) == pytest.approx(1.5 * p * 10 / s)


def test_ring_spin_limit():
    # A ring spun to 1 g at radius R carries its own hoop stress rho g R: k = 1 at R = sigma / (rho g).
    rho, s = 7850.0, 300e6
    for rpm in (1.0, 2.0, 3.0):
        R = ph.spin_radius(1.0, rpm)
        assert ph.ring_spin_factor(rho, ph.omega(rpm), R, s) == pytest.approx(rho * G0 * R / s)
    assert s / (rho * G0) == pytest.approx(3897, abs=1)  # steel's 1 g radius limit, m
    assert ph.ring_structure_mass(100.0, 0.5) == pytest.approx(100.0)
    assert np.isnan(ph.ring_structure_mass(100.0, 1.0))


def test_torus_shell_inertia_by_integration():
    R, r, M = 200.0, 60.0, 1.0
    th, ph_ = np.meshgrid(np.linspace(0, 2 * np.pi, 801)[:-1], np.linspace(0, 2 * np.pi, 801)[:-1])
    rho = R + r * np.cos(th)
    w = rho / rho.sum()  # area element ~ r (R + r cos th) d th d phi
    x, y, z = rho * np.cos(ph_), rho * np.sin(ph_), r * np.sin(th)
    i_spin = M * np.sum(w * (x**2 + y**2))
    i_cross = M * np.sum(w * (y**2 + z**2))
    a, b = ph.torus_shell_inertia(M, R, r)
    assert a == pytest.approx(i_spin, rel=1e-10)
    assert b == pytest.approx(i_cross, rel=1e-10)
    assert a / b > 1  # a ring spins stably about its axis


def test_radiator_and_food():
    # 1 m^2 two-sided black panel at 300 K radiates 2 sigma T^4.
    assert ph.radiator_area(2 * SIGMA * 300.0**4, 300.0, 1.0) == pytest.approx(1.0)
    # 2,500 kcal a day is 121.1 W of food; at 50% LED and 1% crop efficiency, 24.2 kW electric.
    assert ph.food_power(2500, 1.0, 1.0) == pytest.approx(121.06, abs=0.01)
    assert ph.food_power(2500, 0.5, 0.01) == pytest.approx(24212, rel=1e-3)


def test_stuhlinger():
    # No speed change: everything is payload.
    frac, _, _ = ph.stuhlinger(0.0, YEAR, 500.0)
    assert frac == pytest.approx(1.0)
    # Worked case: 1 kW/kg at 60% jet efficiency, 50 km/s in half a year -> ~40% payload,
    # exhaust ~0.8 v_ch (v_ch = 138 km/s).
    dv, t, alpha = 50e3, 0.5 * YEAR, 600.0
    frac, u, v_ch = ph.stuhlinger(dv, t, alpha)
    assert v_ch == pytest.approx(np.sqrt(2 * alpha * t))
    assert 0.39 < frac < 0.41 and 0.7 < u < 0.95
    # The fractions add up from the physics, not the formula: P = mdot v_e^2 / 2, drive = P / alpha.
    m0 = 1.0
    v_e = u * v_ch
    prop = m0 * (1 - np.exp(-dv / v_e))
    drive = 0.5 * (prop / t) * v_e**2 / alpha
    assert m0 - prop - drive == pytest.approx(frac, rel=1e-12)
    # Too weak a drive cannot fly it.
    assert ph.stuhlinger(dv, t, 20.0)[0] <= 0
    # A far stronger drive approaches the ideal rocket with free power.
    assert ph.stuhlinger(dv, t, 1e9)[0] > 0.99


def test_stack_sum():
    # n rings centred on the middle, pitch d: sum z_i^2 = d^2 n (n^2 - 1) / 12.
    for n in range(1, 7):
        z = (np.arange(n) - (n - 1) / 2) * 3.0
        assert np.sum(z**2) == pytest.approx(9.0 * n * (n**2 - 1) / 12)
