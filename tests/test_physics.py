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


def test_segment_area_and_centroid_by_integration():
    r = 50.0
    for depth in (5.0, 30.0, 50.0, 80.0, 100.0):
        # Strips across the circle from the edge (x = r) inwards to x = r - depth.
        x = np.linspace(r - depth, r, 200001)
        w = 2 * np.sqrt(np.maximum(r**2 - x**2, 0.0))
        area = np.trapezoid(w, x)
        assert ph.segment_area(r, depth) == pytest.approx(area, rel=1e-6)
        if depth < 2 * r:
            assert ph.segment_centroid(r, depth) == pytest.approx(np.trapezoid(w * x, x) / area, rel=1e-6)
    assert ph.segment_area(r, 2 * r) == pytest.approx(np.pi * r**2)


def test_stanford_torus_geometry():
    # SP-413: 1 rpm, outer floor at 1 g -> 895 m; tube radius 65 m -> major radius 830 m and
    # '69 X 10^6 m^3 which is enclosed by the torus'; it lives in 1,738 m^3 a person x 10,000.
    R_floor = ph.spin_radius(1.0, 1.0)
    r = 65.0
    assert R_floor - r == pytest.approx(830, abs=1.0)  # SP-413 rounds to 830; exact 829.3
    assert ph.torus_volume(R_floor - r, r) == pytest.approx(69e6, rel=0.01)
    usable = ph.band_volume(R_floor, r, 0.1)
    assert usable > 10_000 * 1738  # one ring is enough
    assert usable < ph.torus_volume(R_floor - r, r)


def test_ring_weight_factor_from_rotating_frame_forces():
    # In the rotating frame the floor's push N balances centrifugal -w x (w x r), Coriolis
    # -2 w x v and the path's own curvature (v^2 / R towards the axis for motion along the ring).
    rpm, g = 1.0, G0
    w = ph.omega(rpm)
    R = ph.spin_radius(1.0, rpm)
    W, pos = np.array([0, 0, w]), np.array([R, 0, 0])
    for v in (-45.0, -8.0, 0.0, 6.0, 11.0, 45.0):
        vel = np.array([0, v, 0])  # along the ring
        a_path = np.array([-v**2 / R, 0, 0])
        N = a_path + np.cross(W, np.cross(W, pos)) + 2 * np.cross(W, vel)
        assert -N[0] / g == pytest.approx(ph.ring_weight_factor(w, g, v), rel=1e-12)
        vel = np.array([0, 0, v])  # parallel to the spin axis: no Coriolis, straight path
        N = np.cross(W, np.cross(W, pos)) + 2 * np.cross(W, vel)
        assert -N[0] / g == pytest.approx(1.0, rel=1e-12)
    assert ph.ring_weight_factor(w, g, 8.0) == pytest.approx(1.18, abs=0.005)
    assert ph.ring_weight_factor(w, g, -8.0) == pytest.approx(0.84, abs=0.005)


def test_box_tube_radius_and_rocket():
    r = ph.box_tube_radius(66.0, 9.0)
    assert np.hypot(33.0, 4.5) == pytest.approx(r)  # the corners touch the circle
    assert ph.box_tube_radius(130.0, 0.0) == pytest.approx(65.0)
    m_f, dv, isp = 10.0, 4000.0, 360.0
    prop = ph.rocket_propellant(m_f, dv, isp)
    assert isp * G0 * np.log((m_f + prop) / m_f) == pytest.approx(dv, rel=1e-12)
    assert ph.rocket_propellant(m_f, 0.0, isp) == 0.0


def test_ground_area_reproduces_sp413():
    # SP-413: 67 m^2 of projected area a person for 10,000 on a 65 m tube whose outer floor is
    # 894 m out; the widest ground (across the tube's centre, inside the 0.9-1 g band) is
    # 2 r x 2 pi (R - r).
    R = ph.spin_radius(1.0, 1.0)
    g = ph.ground_area(R, 65.0, 0.1)
    assert g == pytest.approx(2 * 65.0 * 2 * np.pi * (R - 65.0))
    assert g == pytest.approx(10_000 * 67, rel=0.02)
    # a band too shallow to reach the centre: the ground sits at the band's top, narrower
    d = 0.05 * R
    assert ph.ground_area(R, 65.0, 0.05) == pytest.approx(2 * np.sqrt(d * (130 - d)) * 2 * np.pi * (R - d))
    # the solver finds the smallest tube that holds both
    r = ph.tube_radius_for(R, 0.1, 1.7e7, 10_000 * 67, 30.0, 200.0)
    assert ph.ground_area(R, r, 0.1) == pytest.approx(10_000 * 67, rel=1e-6)
    assert ph.band_volume(R, r, 0.1) >= 1.7e7
    assert ph.tube_radius_for(R, 0.1, 1.0, 1.0, 30.0, 200.0) == pytest.approx(30.0)  # r_min binds


def test_edelbaum():
    assert ph.edelbaum_dv(29.78, 24.07, 0.0) == pytest.approx(5.71)
    v, di = 7.5, 1e-3
    assert ph.edelbaum_dv(v, v, di) == pytest.approx(0.5 * np.pi * v * di, rel=1e-6)
    assert ph.circular_speed(398600.4418, 6378.137) == pytest.approx(7.905, abs=1e-3)


def test_collider_energy_lhc():
    # LHC design: 8.33 T dipoles bending on 2,804 m give 7 TeV protons.
    assert ph.collider_energy_tev(8.33, 2804.0) == pytest.approx(7.0, abs=0.01)


def test_orbit_helpers():
    # LEO (300 km) to GEO, coplanar Hohmann: the textbook ~3.89 km/s
    assert ph.hohmann_dv(398600.4418, 6678.0, 42164.0) == pytest.approx(3.89, abs=0.01)
    # same node: the planes differ by the difference of inclinations
    d = ph.relative_inclination(np.radians(1.85), 0.5, np.radians(10.6), 0.5)
    assert np.degrees(d) == pytest.approx(10.6 - 1.85)
    # Mars to Ceres with their nodes (49.56, 80.2 deg): ~9.05 deg
    d = ph.relative_inclination(*np.radians([1.85, 49.56, 10.6, 80.2]))
    assert np.degrees(d) == pytest.approx(9.05, abs=0.02)
    # the spiral factor against MIT 16.522's table: 0.9245 at eps 1e-4, 0.8657 at 1e-3
    g = 398600.0 / 7000.0**2 * 1e3  # m/s^2 at 7,000 km
    assert ph.spiral_factor(1e-4 * g, 398600.0, 7000.0, 0.754) == pytest.approx(0.9245, abs=5e-4)
    assert ph.spiral_factor(1e-3 * g, 398600.0, 7000.0, 0.754) == pytest.approx(0.8657, abs=5e-4)
