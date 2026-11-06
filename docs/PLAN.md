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

## Decisions

- **2026-11-06, own repo** (Jon): the sizing model lives here; subsystems that need cfsem or
  CortenForge are projects in cortenforge-cfsem and feed numbers back.
- **2026-11-06, layout for phase 0**: a torus (or a stack of tori) spun for gravity inside a still
  shield, Stanford-torus style. Why: the still shield puts no load on the spinning structure, and a
  ring spins stably about its axis. Variants to add: a spinning shield, an O'Neill cylinder pair,
  an asteroid as the shield.
- **2026-11-06, stellarators for power**: steady state, no plasma current to lose; the drive has
  its own plants (they may not be stellarators: open-ended designs suit exhaust).

## Next

1. **Research pass 1**: source the placeholders in sensitivity order (`docs/RESEARCH.md`).
2. **Subsystems from cortenforge-cfsem**, each replacing a guess with a computed number:
   active radiation shield (cfsem fields + particle orbits) against the 10 Mt passive shield;
   reactor magnets (the stellarator project: stored energy, forces, structure mass); spin dynamics
   in sim-core (people and water moving, docking at the hub); a magnetic nozzle for the drive.
3. **Structures**: hand formulas now; pmsim as a check on rings, spokes and hub when the layout
   firms up (CortenForge has no linear-elastic solver yet; logged in its Suggestions).
4. **Variants**: spinning shield, O'Neill cylinders, asteroid shield, lower pressure, partial g.
