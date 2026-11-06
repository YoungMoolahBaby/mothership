# Plan

Goal: a model that says what a lifetime mothership for a town of people would take (mass, power,
plants, radiators, drive) with every number traceable, and that gets better as each subsystem is
computed properly instead of guessed.

## Phase 0: whole-ship model (done 2026-11-06)

- `params/*.yaml`: 33 parameters (19 placeholders) with ranges, units, confidence and sources.
- `mothership check | report`: central run, Monte Carlo P10/P50/P90, sensitivity, three scenarios.
- 12 tests: spin radius, torus volume and area by integration, torus shell stress limits, the
  ring's spin limit (steel's 1 g radius limit 3,897 m), thin-torus inertia by integration, ring
  stacks, radiators (Stefan-Boltzmann), food power, the Stuhlinger drive against its own physics.
- Result: the still shield is about 91% of the ship; volume per person, rpm and shield mass per
  area drive everything; moving the ship takes hundreds of GW against 0.3 GW to live.

## Research pass 1 (done 2026-11-06)

- 19 placeholders -> 3, from NASA SP-413, Globus & Strout, NASA BVAD, ARIES-CS, Siamidis, DFD
  and Discovery II (`docs/RESEARCH.md`, `docs/SOURCES.md`); key quotes checked by hand.
- Model change: the habitat is sized by lived-in volume within a gravity band (SP-413's method),
  not the whole tube; it reproduces the Stanford torus geometry (a test).
- Result: 23.0 million t central (was 10.9), shield 95%; power 185 MW; `tour` ~660 GW, `brisk`
  ~2.3 TW. Next: the gravity band, farm volume, shield material (pass 2).

## Research pass 2: the hockey ship (done 2026-11-06)

- Five topics in parallel (rinks and spin, athletes, sports medicine, care robots, expeditions);
  `params/athletics.yaml`, `care.yaml`, `expeditions.yaml` (38 parameters, 4 placeholders); key
  quotes checked by hand (`docs/RESEARCH.md`).
- Model: rinks across the tube (the tube must hold one), rinks counted from ice time, athletic
  space, skaters' weight along the ring, injuries and surgeries, robots by hours of care and
  chores, landers by the rocket equation; rpm fixed at 1.
- Result: still 23.0 million t; everything athletic fits in SP-413's ring. 14 ice sheets and 4
  roller rinks, 48 m^3 a person of athletic space, 1.6 injuries a person a year (~630
  surgeries), 234 massage tables, 15 kitchen lines and 1,479 humanoids (230 t, 0.7 MW) instead
  of ~1,300 human carers; power 197 MW. A trained skater weighs 1.19 / 0.82 along the ring.
- Next: size the tube from ground area (it now drives 91% of the spread), build the tour's
  delta-v from its stops (one Callisto visit is about half of it), the shield (pass 3).

## Research pass 3: ground, tour, shield, science (done 2026-11-06)

- Five topics in parallel; placeholders 7 -> 0 (122 parameters); `params/tour.yaml`,
  `worlds.yaml`, `science.yaml` (`docs/RESEARCH.md`).
- Model: the tube sized from ground area a person, as SP-413 did (reproduced within 2%); the
  tour's delta-v built from its stops (Edelbaum legs, Hohmann past Jupiter, thrust-dependent
  spirals, parking at 7 body radii with landers carrying the rest); shield options (water,
  active, spinning); science (labs, computing, a collider round the ring in the still shield, a
  light source, a zero-g lab).
- Result: 25.1 million t, 228 MW; the tour is 69 km/s (not 30) and needs 1.7 TW of jet power;
  the collider reaches 2.9 TeV a beam with 16 T magnets; water would shield for 36% less mass.
- Next: Jon's choices (how roomy, which shield, the dose target), refuelling on the tour, the
  magnet projects in cortenforge-cfsem (pass 4).

## Pass 4: Jon's three choices (done 2026-11-06)

- The shield is water for 10 mSv/yr (8.0 t/m^2, 18.5 Mt); 67 m^2 of ground a person all for
  living; aeroponic mist farms anywhere in the tube (45 m^2 of racks and 63 m^3 a person, no soil).
- Result: 19.4 million t (was 25.1), 245 MW, the tour 1.35 TW. Finding: the two trials of
  ultrasonic (1.7 MHz) foggers grew plants poorly; air-assisted ~11 um mist did best (Jon's call).
- Next: the active shield in cortenforge-cfsem, refuelling on the tour (pass 5).

## Pass 5: the farms (done 2026-11-06)

- Four topics in parallel; `params/crops.yaml`, `params/food.yaml`; `model.food_system`.
- A 13-crop diet (53 m^2 of crop racks a person), herbs, spices, medicinal plants, a tea and
  coffee grove, a plant-made-medicine facility, microbial protein, fungi on crop waste, fermented
  dairy, algae, insects, a little egg and fish, and a 95%-closed nutrient loop.
- Result: 211 MW (food 12.9 kW a person), protein 2.7 g/kg/day. Finding: ultrasonic misters
  grew plants worst in the trials and cost 17 MW; high-pressure mist did best for 0.3 MW.
- Jon then chose high-pressure mist and a vegan diet: **189 MW** (food 10.7 kW a person), crops 78%
  of kcal on 55 m^2 of racks a person, protein 2.5 g/kg/day; 19.4 million t.
- Next: the active shield in cortenforge-cfsem (pass 6).

## Decisions

- **2026-11-06, own repo** (Jon): the sizing model lives here; subsystems that need cfsem or
  CortenForge are projects in cortenforge-cfsem and feed numbers back.
- **2026-11-06, layout for phase 0**: a torus (or a stack of tori) spun for gravity inside a still
  shield, Stanford-torus style. Why: the still shield puts no load on the spinning structure, and a
  ring spins stably about its axis. Variants to add: a spinning shield, an O'Neill cylinder pair,
  an asteroid as the shield.
- **2026-11-06, stellarators for power**: steady state, no plasma current to lose; the drive has
  its own plants (they may not be stellarators: open-ended designs suit exhaust).
- **2026-11-06, the ship's purpose: hockey** (Jon): the ship is built around adult ice and roller
  hockey. Everyone's purpose is having fun and pursuing, and keeping, their athletic ceiling
  together, with sports science, sports medicine, massage and recovery for all: "basically like if
  every person on the ship got lebron james treatment". What it sets:
  - 1 g is a requirement, not a choice: the body's ceiling needs full loading.
  - New loads to size: rinks (ice and roller), training and recovery space, athletes' diets (food
    power), hours of hands-on care a person, a sports-medicine hospital.
  - The spin: skating along the ring changes a skater's weight by (1 +- v w / g)^2 (at 1 rpm and
    8 m/s, 1.18 spinward, 0.84 antispinward); skating parallel to the spin axis has no Coriolis
    force, so rinks lie across the tube. Earth-feel hockey (+-10% at 8-11 m/s) needs 0.57-0.42 rpm
    (floor radius 2.7-5.2 km) and a much heavier ship. Jon's call: **1 rpm is fine** (rinks across
    the tube; side-to-side skating swings weight about +-15-25% and becomes the ship's home-ice
    character).
  - The feel (Jon): "like if the main ship in no mans sky was like equinox x schwans super rink":
    a home base that travels, with a premium club and a rink complex at its heart.
  - Care is automated (Jon): "the masages, cooking, etc would all be ai/automated/robotic". So
    the "LeBron" care hours are robot hours: the model sizes robots (count, mass, power, upkeep),
    and people's time stays theirs for play.
- **2026-11-06, science with sports** (Jon): "it should be like cern too. like basically science
  with sports. as youd imagine life aboard a mothership like this would look like". The ship is a
  research campus as well as a club: labs, big instruments, the expeditions' planetary science,
  sports science and medicine itself. To size: lab space and power, big facilities (a collider
  could run round the ring inside the still shield, which doesn't spin and shields its beam
  losses; a light source; telescopes; a zero-g lab at the hub; a data centre).
- **2026-11-06, Jon's three choices** (pass 4, on my recommendation):
  - The shield is **water, for 10 mSv/yr** (half the adult 20, for people who live aboard for
    life, children included): ~8.0 t/m^2, still lighter than regolith at 20 mSv/yr (10.3), and
    the tour passes water (Ceres, Callisto, Titan).
  - **67 m^2 of ground a person, all for living**: the farms come off the ground.
  - The farms are **aeroponic ultrasonic mist farms, "wherever it can"**: racks anywhere in the
    tube, in or out of the living band, no soil.
- **2026-11-06, the farms are the backbone** (Jon): "we can do research on state of the art
  aeroponic practices first, as thats the backbone of this, as food/herbs/spices/medicine are
  sacred to humans". The farms must give a complete, varied, delicious diet, herbs and spices,
  and medicine, not only calories: pass 5 researches aeroponic practice, a full crop mix, herbs,
  spices and medicinal plants, and the rest of the food system (fungi, fermentation, the
  nutrient loop) before the active shield.
- **2026-11-06, vegan, and the aeroponic system** (Jon): "ideally vegan/vegetarian too. and ok to
  your recommendation for the aeroponic system". No insects, eggs or fish; dairy from precision
  fermentation (no animals); B12 from bacterial fermentation. The farms run on high-pressure mist
  (~0.5-0.7 MPa, 10-30 um), ultrasonic or dry fog only on propagation benches and a test bench;
  many small independent loops with spare pumps and accumulators for ~1 h, lights dimmed on a mist
  fault, UV and filtration on every return, ~20% of racks deep-flow hydroponics as a buffer.
- **2026-11-06, missions to other planets** (Jon): the ship travels and sends expeditions down to
  planets and moons while it stays in orbit. To size: landers and their propellant (a lander per
  body type: airless moons, Mars-like, thick atmospheres), a hangar at the still hub (docking is
  easiest off the spin), crews away and coming back to 1 g, and the orbit insertion each stop
  adds to the drive's delta-v.

## Next

1. **Pass 6** (`docs/RESEARCH.md`): the active shield as a cortenforge-cfsem project, then
   refuelling and moon flybys on the tour.
2. **Subsystems from cortenforge-cfsem**, each replacing a guess with a computed number:
   active radiation shield (cfsem fields + particle orbits) against the 10 Mt passive shield;
   reactor magnets (the stellarator project: stored energy, forces, structure mass); spin dynamics
   in sim-core (people and water moving, docking at the hub); a magnetic nozzle for the drive.
3. **Structures**: hand formulas now; pmsim as a check on rings, spokes and hub when the layout
   firms up (CortenForge has no linear-elastic solver yet; logged in its Suggestions).
4. **Variants**: spinning shield, O'Neill cylinders, asteroid shield, lower pressure, partial g.
