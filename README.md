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

- **Habitat**: a torus spun for gravity (radius = g / w^2), as many rings as the volume needs,
  each tube no wider than a set fraction of the radius, rings stacked along the spin axis.
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

## First results (2026-11-06, placeholders, 5,000 draws)

For 10,000 people (central / P50 / P10-P90):

- Ship without drive: 10.9 / 12.5 / 8.0-21.1 million t, about 1,100 t a person. The shield is
  9.9 million t of the 10.9: 91% of the ship.
- Spin radius 224 m at 2 rpm and 1 g, 2 rings; electric power 292 MW (food under lights is 24 kW a
  person, most of it), 2 plants with the spare.
- Moving it: `tour` needs about 220 GW of jet power and 0.9 million t of drive and propellant;
  `brisk` about 770 GW and 3.3 million t. Living needs 0.3 GW.
- What drives the mass: volume per person, rpm (a faster spin means a smaller radius, more rings
  and more shield), shield mass per area. Spin stability fails in 44% of draws: fast spins need
  long ring stacks, and a long stack tumbles.

## Related

Subsystems that need real computation are projects in `C:\dev\cortenforge-cfsem` (cfsem
electromagnetics, CortenForge simulation and geometry): the stellarator there sizes the power
plant's magnets; next could be an active radiation shield, spin dynamics, a magnetic nozzle.
