# Research queue

Ordered by the sensitivity table in `out/report.md`. When an item is done: update the
parameter's value/range/conf/source, tick it here (old -> **new**), rerun the report.

## Research pass 1 (2026-11-06)

Four topics researched in parallel (habitat studies, human factors, food and power, power plants
and drive); the highest-impact quotes rechecked by hand against SP-413 chapters 3 and 5 and the
Globus & Strout PDF. 19 placeholders -> 3. Exact quotes are in the `source` fields of
`params/*.yaml`; references in `docs/SOURCES.md`.

**Model change.** The Stanford torus study (SP-413) sizes a habitat by where people can live, not
by the tube: floors must sit within a gravity band (0.9-1 g), and most of its tube is air above
the band (1,738 m^3 a person used of 6,900 enclosed). `volume_per_person` and `max_tube_ratio`
gave way to `usable_volume_per_person`, `gravity_band` and `tube_ratio`: a ring holds the tube's
volume within band x R of the outer floor (`physics.band_volume`). With SP-413's numbers the model
reproduces its geometry: outer floor 894 m, ring radius 829 m (SP-413: 830), tube 65 m, 6,973
m^3 enclosed a person (SP-413: 69 x 10^6 m^3 for 10,000), one ring (`test_stanford_torus_geometry`).

1. [x] `habitat.volume_per_person` 5,000 -> replaced by `usable_volume_per_person` **1,738**
   (1,040-3,500): SP-413 Table 3-2 (community 823 + agriculture 915).
2. [x] `habitat.rpm` 2 (1-3) -> **1** (1-2): SP-413's 1 rpm limit; Globus & Hall 2015 "up to 2
   rpm should be no problem for residents". Adaptation to 3-10 rpm is shown only in short studies
   of young adults.
3. [x] `habitat.shield.areal_density` 7 (4.5-10) -> **10** (6.5-11): regolith for 20 mSv/yr
   (Globus & Strout 2017; the limit is set for adults and, at 6.6 mGy/yr, for pregnant women);
   water or polyethylene 6-7. SP-413's 4.5 is "quite low".
4. [x] `habitat.max_tube_ratio` 0.4 -> replaced by `tube_ratio` **0.073** (0.05-0.2): SP-413
   65 m on an 895 m floor radius. New `gravity_band` **0.1** (0.05-0.2, low): SP-413's band,
   which it calls arbitrary.
5. [x] `habitat.shield.gap` 5 (2-20) -> **1.5** (1-5): SP-413 "approximately 1-1/2 m".
6. [x] `habitat.gravity_g` 1.0 (0.8-1.0) -> **1.0** (0.9-1.0, low): no human data on long-term
   partial g; mouse bone loss scales with unloading even at 70% (Ellman et al. 2013).
7. [x] `habitat.interior_mass_per_person` 50 (20-150) -> **53** (30-80): SP-413 Table 5-3.
8. [x] `habitat.air_pressure` 101.3 (60-101.3) -> **70** (50.8-101.3): sea-level inspired O2 at
   30% O2 or less, under NASA's 31.4% no-faster-burning limit at 56.5 kPa; SP-413 used 50.8.
9. [x] `life.led_to_par` 0.5 -> **0.45** (0.3-0.65): fixtures 2.5-2.8 umol/J (~0.55 W/W) x
   delivery 0.8 (NASA BVAD). `life.par_to_food` 0.01 -> **0.02** (0.01-0.04): BVAD crop tables,
   wheat 1.3% to sweet potato 6%. Food power now 13.5 kW a person (cross-check 7-18 kW).
10. [x] `life.other_power_per_person` 5 (2-15) -> **5** (3-10): SP-413 3 kW consumed and 5 kW
    supplied a person (sunlit farms), ISS ECLSS ~0.8 kW a crew member.
11. [x] `power.specific_mass` 20 (5-60) -> **20** (10-60, low): ARIES-CS core ~11 t/MWe.
    `power.thermal_efficiency` 0.4 -> **0.25** (0.2-0.3) and `power.plant_radiator_temp` 700 ->
    **500 K** (400-600): space Brayton optimum (Siamidis). `power.radiator_areal_density` 8 ->
    **10** kg/m^2 planform (2-18). `power.emissivity` 0.9 (0.8-0.92). `power.unit_mwe` 500
    (200-1000; ARC 200-250, ARIES-CS 1000).
12. [x] `propulsion.jet_specific_power` 500 (100-2000) -> **1,000** (300-7,500, low): DFD 0.3-1.5
    kW/kg, Discovery II ~7.5. `propulsion.tankage` 0.05 -> **0.10** (0.03-0.15).

**Result** (`uv run mothership report`, 5,000 draws): the ship without drive went from 10.9 to
23.0 million t central (P10-P90 13.2-34.4), 2,300 t a person. The shield is 21.9 of the 23.0
(95%): the sourced 10 t/m^2 and SP-413's big slow ring (more hull to enclose the band) both grew
it. Power fell from 292 to 185 MW (food 13.5 kW a person). Moving the heavier ship: `tour` 664 GW
of jet power, `brisk` 2.3 TW, against 0.19 GW to live. Spin stable in 91% of draws.

## Next (pass 2), from the new sensitivity table (start mass, `park`)

1. `habitat.gravity_band` (-0.47, low): the band sets how much of a tube is usable. How much
   gravity difference between floors is fine for life (stairs, sports, children)? SP-413 calls
   its 10% arbitrary.
2. `habitat.usable_volume_per_person` (+0.41): farm volume with stacked LED racks (vertical
   farms) against SP-413's sunlit single-level fields; this links to `life.*`.
3. `habitat.shield.areal_density` (+0.26) and `habitat.tube_ratio` (+0.26): shield material
   (water from asteroids vs slag) and an active magnetic shield (a cortenforge-cfsem project);
   tube shape (SP-413 kept it thin for structure).
4. Remaining placeholders: `habitat.shell.allowable_stress`, `power.habitat_radiator_temp`,
   `habitat.min_inertia_ratio`.
5. Model: farms in low-g decks (plants may not need 1 g), a spinning-shield variant, O'Neill
   cylinders.
