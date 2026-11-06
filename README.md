# mothership

A sizing model for a lifetime mothership: a spinning habitat where a town of people lives a
normal life in space for years or generations, powered by fusion (stellarators), able to move.
It is built around adult ice and roller hockey: everyone's purpose is having fun and pursuing their
athletic ceiling together, with pro-level sports science, medicine and recovery for all, and the
ship travels between worlds, sending expeditions down to planets and moons.
Every number lives in `params/*.yaml` with a range, a confidence and a source; the report runs a
Monte Carlo over the ranges and ranks what drives the mass.

Built so far: the whole-ship model (phase 0) and two research passes (72 parameters, 7 still
placeholders). Its job is to show where the mass is and which numbers to pin down next
(`docs/RESEARCH.md`).

## Run

```sh
uv run mothership check     # parameters and the central run are sane
uv run mothership report    # central run, P10/P50/P90, sensitivity -> out/report.md
uv run pytest               # the physics against closed forms and textbook values
```

## The model

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
- **Hockey**: spun at 1 rpm (Jon's call). Rinks lie across the tube, their long side parallel to
  the spin axis, where skating feels no Coriolis force; skating along the ring changes a skater's
  weight by (1 +- v w / g)^2. Ice sheets and roller rinks are counted from rink time a person;
  training, recovery and sports-medicine space adds to the lived-in volume; injuries and surgeries
  come from game and practice hours.
- **Care by robots**: massage tables, robotic kitchen lines and humanoid robots (hands-on care and
  chores), sized by hours of work, with spares, their mass and power.
- **Expeditions**: reusable landers at the still hub, with propellant for round trips from low
  orbit to the surface (rocket equation).
- **Drive**: a power-limited (Stuhlinger) drive with its own plants, for three scenarios: `park`
  (no move), `tour` (30 km/s over 20 years), `brisk` (30 km/s over 2 years).

## Results after research pass 2 (2026-11-06, 7 placeholders left, 5,000 draws)

For 10,000 people (central / P50 / P10-P90):

- Ship without drive: 23.0 / 27.0 / 18.5-39.7 million t, about 2,300 t a person. The shield (10
  t/m^2 of regolith for 20 mSv/yr) is 21.9 million t of the 23.0: 95% of the ship.
- One ring like the Stanford torus: outer floor 894 m from the axis at 1 rpm and 1 g, 65 m tube;
  electric power 197 MW (food under lights 14.5 kW a person for athletes' 2,700 kcal, most of
  it), 2 plants with the spare.
- The hockey ship costs almost no mass: everything athletic fits in the ring. 14 ice sheets and
  4 roller rinks (4 h of ice and 1 h of roller a person a week), 48 m^3 a person of rinks,
  training, recovery and sports medicine; 1.6 injuries a person a year, about 630 surgeries a
  year ship-wide. A trained skater at 8.7 m/s weighs 1.19x skating with the spin, 0.82x against.
- Care by robots: 234 massage tables, 15 kitchen lines and 1,479 humanoids, 230 t and 0.7 MW;
  done by people the same care would take about 1,300 clinicians (13% of the ship).
- Expeditions: 4 reusable 6-crew landers, 42 t of propellant a round trip from low orbit (4
  km/s); surface stays of about two weeks (radiation, coming back to 1 g).
- Moving it: `tour` (30 km/s over 20 years) needs about 660 GW of jet power and 1.3 million t of
  drive and propellant; `brisk` (2 years) about 2.3 TW and 4.7 million t. Living needs 0.2 GW.
  Stopping is costly: spiralling into a low orbit and out again costs ~6 km/s at Mars, and one
  visit to Callisto inside Jupiter's well about half the tour's 30 km/s.
- What drives the mass now: the tube's size (with rpm fixed one ring always holds everyone), then
  shield mass per area. Pass 3 sizes the tube from ground area, as SP-413 did. Details:
  `docs/RESEARCH.md`.

## Related

Subsystems that need real computation are projects in `C:\dev\cortenforge-cfsem` (cfsem
electromagnetics, CortenForge simulation and geometry): the stellarator there sizes the power
plant's magnets; next could be an active radiation shield, spin dynamics, a magnetic nozzle, the
hospital's MRI magnet.
