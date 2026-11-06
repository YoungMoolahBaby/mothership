# mothership

A sizing model for a lifetime mothership: a spinning habitat where a town of people lives a
normal life in space for years or generations, powered by fusion (stellarators), able to move.
Every number lives in `params/*.yaml` with a range, a confidence and a source; the report runs a
Monte Carlo over the ranges and ranks what drives the mass.

Phase 0 is built: the whole-ship model with placeholder numbers. Its job now is to show where the
mass is and which numbers to pin down first (`docs/RESEARCH.md`).

## Run

```sh
uv run mothership check     # parameters and the central run are sane
uv run mothership report    # central run, P10/P50/P90, sensitivity -> out/report.md
uv run pytest               # the physics against closed forms and textbook values
```

## The model (phase 0)

- **Habitat**: a torus spun for gravity (outer floor radius = g / w^2). People live where gravity
  is within a band of the floor's (SP-413: 0.9-1 g), so a ring holds only the tube's volume in
  that band; as many rings as the lived-in volume needs, stacked along the spin axis. With the
  Stanford torus study's numbers it reproduces that design (830 m ring, 65 m tube, 69 million m^3).
- **Shield**: a still (non-spinning) shell round each ring, as in the Stanford torus design,
  sized by mass per area.
- **Structure**: the pressure shell (thin torus, peak stress on the inner equator) and the
  spinning hoop that holds everything against the spin (k = rho w^2 R^2 / sigma).
- **Spin stability**: the stack's spin-axis over cross-axis moment of inertia; a body spins
  stably (with energy loss) only about its largest axis.
- **Life and power**: food grown under LEDs, plus everything else per person; stellarator plants
  with a spare; radiators for the plants' waste heat and for the habitat (all electric power ends
  as heat inside).
- **Drive**: a power-limited (Stuhlinger) drive with its own plants, for three scenarios: `park`
  (no move), `tour` (30 km/s over 20 years), `brisk` (30 km/s over 2 years).

## Results after research pass 1 (2026-11-06, 3 placeholders left, 5,000 draws)

For 10,000 people (central / P50 / P10-P90):

- Ship without drive: 23.0 / 21.0 / 13.2-34.4 million t, about 2,300 t a person. The shield (10
  t/m^2 of regolith for 20 mSv/yr) is 21.9 million t of the 23.0: 95% of the ship.
- One ring like the Stanford torus: outer floor 894 m from the axis at 1 rpm and 1 g, 65 m tube;
  electric power 185 MW (food under lights 13.5 kW a person, most of it), 2 plants with the spare.
- Moving it: `tour` (30 km/s over 20 years) needs about 660 GW of jet power and 1.3 million t of
  drive and propellant; `brisk` (2 years) about 2.3 TW and 4.7 million t. Living needs 0.19 GW.
- What drives the mass now: the gravity band people live in (how much of a tube is usable), lived-in
  volume per person, shield mass per area, tube shape. Spin is stable in 91% of draws.
- Pass 0 (placeholders) had 10.9 million t: the sourced shield and SP-413's big, slow ring doubled
  it. Details: `docs/RESEARCH.md`.

## Related

Subsystems that need real computation are projects in `C:\dev\cortenforge-cfsem` (cfsem
electromagnetics, CortenForge simulation and geometry): the stellarator there sizes the power
plant's magnets; next could be an active radiation shield, spin dynamics, a magnetic nozzle.
