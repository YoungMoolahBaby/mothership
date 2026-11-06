"""The closed forms the model is built from. Each is checked in tests/test_physics.py.

All functions take floats or numpy arrays (broadcast), SI units.
"""

from __future__ import annotations

import numpy as np

from .constants import G0, KCAL, DAY, SIGMA


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
