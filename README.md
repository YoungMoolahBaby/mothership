# mothership

A sizing model for a lifetime mothership: a spinning habitat where a town of people lives a
normal life in space for years or generations, powered by fusion (stellarators), able to move.
It is built around adult ice and roller hockey and around science, like a club crossed with CERN:
everyone's purpose is having fun, pursuing their athletic ceiling together (with pro-level sports
science, medicine and recovery for all) and doing science, and the ship travels between worlds,
sending expeditions down to planets and moons.
Every number lives in `params/*.yaml` with a range, a confidence and a source; the report runs a
Monte Carlo over the ranges and ranks what drives the mass.

Built so far: the whole-ship model (phase 0), research passes 1-5 and Jon's first design choices
(250 parameters, none placeholders). Its job is to show where the mass is and which choices and numbers matter next
(`docs/RESEARCH.md`).

## Run

```sh
uv run mothership check     # parameters and the central run are sane
uv run mothership report    # central run, P10/P50/P90, sensitivity -> out/report.md
uv run pytest               # the physics against closed forms and textbook values
```

## The model

- **Habitat**: a torus spun for gravity (outer floor radius = g / w^2). People live on a ground
  plane across the tube's widest chord, within a band of the floor's gravity (SP-413: 0.9-1 g),
  and the tube is the smallest that holds everyone's ground (and the rinks'), the lived-in
  volume in that band and the farms; past a size limit, rings are stacked along the spin axis.
  With the Stanford torus study's numbers it reproduces that design (67 m^2 a person on a 65 m
  tube).
- **Shield**: a still (non-spinning) fail-safe hybrid round each ring: water thick enough for 50
  mSv/yr with the magnet off (OLTARIS dose tables) and a low-field magnet for 10 mSv/yr with it
  on (cortenforge-cfsem); the report also prices water alone, regolith, the full magnet hybrid
  and spinning the shield.
- **Structure**: the pressure shell (thin torus, peak stress on the inner equator) and the
  spinning hoop that holds everything against the spin (k = rho w^2 R^2 / sigma).
- **Spin stability**: the stack's spin-axis over cross-axis moment of inertia; a body spins
  stably (with energy loss) only about its largest axis.
- **Food** (the backbone: "food/herbs/spices/medicine are sacred to humans"): a 13-crop diet
  under LEDs in aeroponic mist racks anywhere in the tube, each crop at its measured yield and
  light; herbs, spices, medicinal plants and a tea and coffee grove; a plant-made-medicine
  facility; microbial protein from cabin CO2, fungi and insects on crop waste, fermented dairy,
  algae (vegan, Jon's choice); high-pressure mist with redundant loops and a deep-flow buffer; a
  nutrient loop recycling ~95%.
- **Power**: food plus everything else per person; stellarator plants with a spare; radiators for
  the plants' waste heat and for the habitat (all electric power ends as heat inside).
- **Hockey**: spun at 1 rpm (Jon's call). Rinks lie across the tube, their long side parallel to
  the spin axis, where skating feels no Coriolis force; skating along the ring changes a skater's
  weight by (1 +- v w / g)^2. Ice sheets and roller rinks are counted from rink time a person;
  training, recovery and sports-medicine space adds to the lived-in volume; injuries and surgeries
  come from game and practice hours.
- **Care by robots**: massage tables, robotic kitchen lines and humanoid robots (hands-on care and
  chores), sized by hours of work, with spares, their mass and power.
- **Science** (like CERN): labs for the people doing science, a data centre, a proton collider
  round the ring inside the still shield, a light source, a zero-g lab at the hub.
- **Expeditions**: reusable landers at the still hub, with propellant for round trips from the
  ship's parking orbit to the surface at each stop (rocket equation).
- **The tour**: Earth -> Mars -> Ceres -> Callisto -> Titan -> Earth, its delta-v built from low-
  thrust legs (Edelbaum, Hohmann past Jupiter) and spirals into and out of a parking orbit at
  each stop (JPL data).
- **Building it**: each material's source (asteroids, the Moon, Earth), the energy to mine,
  refine and deliver it, launches from Earth, and the years at the build site's power.
- **Drive**: a power-limited (Stuhlinger) drive with its own plants, for three scenarios: `park`
  (no move), `tour` (the tour over 20 years of thrust), `brisk` (the same in 2 years).

## Results after pass 5, the farms (2026-11-06, no placeholders, 5,000 draws)

For 10,000 people (central / P50 / P10-P90):

- Ship without drive: 12.5 / 13.2 / 12.3-14.1 million t, about 1,250 t a person. The shield is a
  fail-safe hybrid, 11.5 million t: 4.72 t/m^2 of water (within ICRP's 50 mSv single-year ceiling
  with the magnet off) and a low-field MgB2 magnet (50 T m, 0.55 million t, 40 MW of cryocoolers) that
  brings it to 9-10 mSv/yr; water alone would be 18.5 million t (computed in cortenforge-cfsem
  `projects/active-shield`).
- One ring: outer floor 894 m from the axis at 1 rpm and 1 g, a 70 m tube (SP-413's 65 m plus the
  rinks' ground); 67 m^2 of ground a person, all for living. Electric power 229 MW: food 10.7 kW a
  person, the shield magnet's cryocoolers 40 MW, science 29 MW; 2 plants with the spare.
- Food (vegan): 78% of the athletes' 2,700 kcal from 13 crops on 55 m^2 of racks a person (59 with
  herbs, spices, medicine and the grove), the rest from microbial protein, fungi on crop waste,
  precision-fermented dairy and algae; protein 2.5 g/kg a day. High-pressure mist (0.3 MW for the
  ship) grew plants best in the trials; ultrasonic fog grew them worst and would cost 17.8 MW.
- How roomy it is drives everything: 40 m^2 of ground a person gives 12 million t, 67 gives 19,
  100 gives 28, Kalpana One's ~170 needs two rings and 46.
- Hockey: 14 ice sheets and 4 roller rinks (4 h of ice and 1 h of roller a person a week), 48 m^3 a
  person of rinks, training, recovery and sports medicine; 1.6 injuries a person a year, about 630
  surgeries a year ship-wide. A trained skater at 8.7 m/s weighs 1.19x skating with the spin,
  0.82x against.
- Care by robots: 234 massage tables, 15 kitchen lines and 1,972 humanoids (working at half a
  person's pace), 260 t and 2.7 MW; done by people it would take about 1,300 clinicians.
- Science: 3,000 people doing it, 16 m^3 a person of labs; a collider round the ring with 16 T
  magnets reaches 2.9 TeV a beam (the Tevatron ~1, the LHC 6.8) for 15 MW and 7,600 t.
- The tour is 69 km/s, not the 30 assumed before: Callisto inside Jupiter's well costs 14.6 and
  Titan 10.2, coming home from Saturn 15.7. It needs about 0.87 TW of jet power and 1.8 million t
  of drive and propellant over 20 years of thrust; `brisk` (2 years) 3.3 TW and 7.3 million t.
  Living needs 0.23 GW.
- Expeditions: 4 reusable 6-crew landers, about 90 t of propellant a round trip from the ship's
  parking orbit at 7 body radii; surface stays of about two weeks (radiation, coming back to 1 g).
- Building it: the shield water from one Bennu-class asteroid (70%) and lunar polar ice (30%),
  metals from the Moon, carbon and nitrogen from the asteroid ore, MgB2 wire for the magnet;
  ~40,000 t and ~540 launches from Earth (~$54 billion); ~3.4e17 J, ~21 years of bulk build at 0.5
  GW after ~13 years of preparation: ~34 years from go-ahead to move-in. Carbon fibre (the magnet's
  structure) is half the build energy.
- Details and sources: `docs/RESEARCH.md`, `docs/SOURCES.md`.

## Related

Subsystems that need real computation are projects in `C:\dev\cortenforge-cfsem` (cfsem
electromagnetics, CortenForge simulation and geometry): the stellarator there sizes the power
plant's magnets; next could be an active radiation shield, the collider's dipoles, spin
dynamics, a magnetic nozzle, the hospital's MRI magnet.
