"""The closed forms the model is built from. Each is checked in tests/test_physics.py.

All functions take floats or numpy arrays (broadcast), SI units.
"""

from __future__ import annotations

import numpy as np

from .constants import C_LIGHT, G0, KCAL, DAY, SIGMA


def omega(rpm):
    """Spin rate (rad/s) from revolutions per minute."""
    return 2.0 * np.pi * np.asarray(rpm, dtype=float) / 60.0


def spin_radius(gravity_g, rpm):
    """Radius (m) where a spin of `rpm` gives `gravity_g` g: r = g / w^2."""
    return np.asarray(gravity_g, dtype=float) * G0 / omega(rpm) ** 2


def torus_volume(R, r):
    """Volume of a torus, major radius R, tube radius r: 2 pi^2 R r^2."""
    return 2.0 * np.pi**2 * R * r**2


def torus_area(R, r):
    """Surface area of a torus: 4 pi^2 R r."""
    return 4.0 * np.pi**2 * R * r


def torus_tube_radius(volume, R):
    """Tube radius that gives a torus of major radius R the volume `volume`."""
    return np.sqrt(volume / (2.0 * np.pi**2 * R))


def torus_shell_thickness(pressure, R, r, allowable):
    """Wall thickness (m) for a pressurized thin torus: the hoop stress peaks on the inner
    equator, sigma = p r (2R - r) / (2 t (R - r)) (Roark), so t = p r (2R - r) / (2 sigma (R - r)).
    Tends to the cylinder's p r / sigma as r / R -> 0."""
    return pressure * r * (2.0 * R - r) / (2.0 * allowable * (R - r))


def ring_spin_factor(density, w, R, allowable):
    """k = rho w^2 R^2 / sigma: a free spinning ring's own hoop stress over the allowable.
    A ring of material can only spin itself if k < 1, so R_max = sqrt(sigma / rho) / w."""
    return density * w**2 * R**2 / allowable


def ring_structure_mass(carried, k):
    """Mass of a spinning hoop that holds `carried` (kg, spread round its rim) and itself
    against the spin: m = k (carried + m), so m = k carried / (1 - k); NaN where k >= 1."""
    k = np.asarray(k, dtype=float)
    with np.errstate(divide="ignore", invalid="ignore"):
        m = k * carried / (1.0 - k)
    return np.where(k < 1.0, m, np.nan)


def torus_shell_inertia(M, R, r):
    """Moments of inertia of a thin torus shell: about the spin axis M (R^2 + 3/2 r^2), about a
    diameter M (R^2/2 + 5/4 r^2). Spin is stable (with energy loss) only about the largest."""
    return M * (R**2 + 1.5 * r**2), M * (0.5 * R**2 + 1.25 * r**2)


def radiator_area(heat, temperature, emissivity):
    """Two-sided panel area (m^2) radiating `heat` (W) to deep space at `temperature`."""
    return heat / (2.0 * emissivity * SIGMA * temperature**4)


def food_power(kcal_per_day, led_to_par, par_to_food):
    """Electric power (W) to grow one person's food under lights."""
    return kcal_per_day * KCAL / DAY / (led_to_par * par_to_food)


def stuhlinger(dv, burn_time, alpha, tankage=0.0, n_grid=800):
    """Power-limited rocket at constant power and exhaust speed, burning for `burn_time`.

    With v_ch = sqrt(2 alpha t) (alpha = jet power per kg of drive), u = v_e / v_ch and
    x = dv / v_ch, the fractions of the start mass m0 are:
      propellant  1 - e^(-x/u)
      drive       (1 - e^(-x/u)) u^2          (P = m_prop v_e^2 / 2t, drive = P / alpha)
      tanks       (1 - e^(-x/u)) tankage
      payload     the rest, maximized over u.
    Returns (payload fraction, u at the best, v_ch), with payload fraction <= 0 meaning the
    mission can't be flown with this drive."""
    dv, burn_time, alpha, tankage = np.broadcast_arrays(
        *(np.asarray(a, dtype=float) for a in (dv, burn_time, alpha, tankage))
    )
    v_ch = np.sqrt(2.0 * alpha * burn_time)
    x = (dv / v_ch)[..., None]
    u = np.geomspace(0.02, 5.0, n_grid)
    e = np.exp(-x / u)
    f = e - (1.0 - e) * (u**2 + tankage[..., None])
    i = np.argmax(f, axis=-1)
    best = np.take_along_axis(f, i[..., None], axis=-1)[..., 0]
    return best, u[i], v_ch


def segment_area(r, depth):
    """Area of the part of a circle of radius r within `depth` of one edge (a circular segment;
    depth is clipped to 0..2r)."""
    b = np.clip(depth, 0.0, 2.0 * r)
    h = r - b
    return r**2 * np.arccos(h / r) - h * np.sqrt(np.maximum(2.0 * r * b - b**2, 0.0))


def segment_centroid(r, depth):
    """Distance from the circle's centre to that segment's centroid, towards the edge:
    4 r sin^3(t/2) / (3 (t - sin t)), t the segment's central angle."""
    b = np.clip(depth, 1e-12, 2.0 * r)
    t = 2.0 * np.arccos((r - b) / r)
    with np.errstate(divide="ignore", invalid="ignore"):
        d = 4.0 * r * np.sin(t / 2.0) ** 3 / (3.0 * (t - np.sin(t)))
    return np.where(t < 2.0 * np.pi - 1e-9, d, 0.0)


def band_volume(R_floor, r, band):
    """Volume of a torus tube (tube radius r, outer floor at R_floor from the spin axis) where the
    spin gravity is within `band` (a fraction) of the floor's: radii R_floor (1 - band) to
    R_floor. Pappus: the segment's area times the path of its centroid."""
    depth = band * R_floor
    centre = R_floor - r
    return 2.0 * np.pi * (centre + segment_centroid(r, depth)) * segment_area(r, depth)


def ring_weight_factor(w, gravity, v):
    """Apparent weight over floor weight for something moving at v (m/s) along the floor of a
    spinning ring, v > 0 with the spin, v < 0 against it; `gravity` (m/s^2) is the floor's spin
    gravity. Its speed past the axis is w R + v on the radius R = gravity / w^2, so the floor
    pushes (w R + v)^2 / R = gravity (1 + v w / gravity)^2. Motion parallel to the spin axis
    feels no change (the Coriolis force is w x v = 0), so rinks lie across the tube."""
    return (1.0 + np.asarray(v, dtype=float) * w / gravity) ** 2


def box_tube_radius(width, height):
    """Smallest tube radius whose circular cross-section holds a box `width` across and `height`
    tall (the box centred, its corners on the circle): sqrt(width^2 + height^2) / 2."""
    return 0.5 * np.hypot(width, height)


def rocket_propellant(final_mass, dv, isp):
    """Propellant for a burn of delta-v `dv` (m/s) at specific impulse `isp` (s) that ends with
    `final_mass` (Tsiolkovsky): final_mass (e^(dv / (isp g0)) - 1), same unit as final_mass."""
    return final_mass * np.expm1(np.asarray(dv, dtype=float) / (np.asarray(isp, dtype=float) * G0))


def ground_area(R_floor, r, band):
    """Area of the widest ground a tube holds within the gravity band: a floor across the tube at
    depth d above the outer floor (the tube's centre, d = r, where the chord is widest, unless the
    band stops lower: d = band x R_floor), its width the chord there, times its circumference."""
    d = np.minimum(r, band * R_floor)
    chord = 2.0 * np.sqrt(np.maximum(d * (2.0 * r - d), 0.0))
    return chord * 2.0 * np.pi * (R_floor - d)


def tube_radius_for(R_floor, band, volume, ground, r_min, r_max, iterations=80):
    """Smallest tube radius (between r_min and r_max) whose gravity band holds `volume` and whose
    widest ground holds `ground`; both grow with r, so bisect. Returns r_max where even that
    falls short (the caller then adds rings)."""
    R_floor, band, volume, ground, r_min, r_max = np.broadcast_arrays(
        *(np.asarray(a, dtype=float) for a in (R_floor, band, volume, ground, r_min, r_max))
    )
    lo, hi = np.minimum(r_min, r_max), r_max.copy()
    ok = lambda r: (band_volume(R_floor, r, band) >= volume) & (ground_area(R_floor, r, band) >= ground)
    done = ok(lo)
    for _ in range(iterations):
        mid = 0.5 * (lo + hi)
        good = ok(mid)
        hi = np.where(good, mid, hi)
        lo = np.where(good, lo, mid)
    return np.where(done, np.minimum(r_min, r_max), hi)


def circular_speed(gm, r):
    """Circular orbit speed sqrt(GM / r) (units of gm and r: km^3/s^2 and km give km/s)."""
    return np.sqrt(gm / r)


def edelbaum_dv(v1, v2, di):
    """Low-thrust transfer between circular orbits of speeds v1 and v2 with a plane change of di
    (radians), thrust steered optimally (Edelbaum 1961): sqrt(v1^2 + v2^2 - 2 v1 v2 cos(pi/2 di)).
    Coplanar it is |v1 - v2|; a pure plane change costs (pi/2) v di for small di."""
    return np.sqrt(v1**2 + v2**2 - 2.0 * v1 * v2 * np.cos(0.5 * np.pi * di))


def collider_energy_tev(field, bend_radius):
    """Beam energy (TeV) of a proton ring with dipoles of `field` (T) bending on `bend_radius`
    (m): p = e B rho, so pc in eV = c B rho; at these energies E = pc."""
    return C_LIGHT * np.asarray(field, dtype=float) * bend_radius / 1e12


def relative_inclination(i1, node1, i2, node2):
    """Angle (radians) between two orbit planes given their inclinations and ascending nodes
    (radians) to a common reference plane: cos d = cos i1 cos i2 + sin i1 sin i2 cos(node1 - node2)."""
    c = np.cos(i1) * np.cos(i2) + np.sin(i1) * np.sin(i2) * np.cos(node1 - node2)
    return np.arccos(np.clip(c, -1.0, 1.0))


def hohmann_dv(gm, r1, r2):
    """Two-burn Hohmann transfer between coplanar circular orbits (units of gm and r: km^3/s^2
    and km give km/s)."""
    a = 0.5 * (r1 + r2)
    v1, v2 = np.sqrt(gm / r1), np.sqrt(gm / r2)
    return np.abs(np.sqrt(gm * (2.0 / r1 - 1.0 / a)) - v1) + np.abs(v2 - np.sqrt(gm * (2.0 / r2 - 1.0 / a)))


def spiral_factor(acceleration, gm, r, coefficient):
    """Delta-v of a low-thrust spiral between circular speed at r and escape, over that circular
    speed: 1 - c eps^(1/4), eps = thrust acceleration / local gravity (MIT 16.522 lecture 6,
    c = 0.754). `acceleration` in m/s^2, gm in km^3/s^2, r in km."""
    eps = acceleration / (gm / r**2 * 1e3)
    return np.clip(1.0 - coefficient * eps**0.25, 0.0, 1.0)
