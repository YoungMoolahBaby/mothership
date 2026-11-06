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

## Research pass 2 (2026-11-06): the hockey ship

The ship is built around adult ice and roller hockey, with LeBron-level care for everyone done by
robots, and expeditions to planets and moons (`docs/PLAN.md`, decisions of 2026-11-06; Jon kept
1 rpm). Five topics researched in parallel (rinks and spin; athletes' diet, training and recovery;
sports medicine and facilities; care robots; expeditions); key quotes rechecked by hand (IIHF
arena guides, Hall AIAA 99-4524, ISSN 2018, Caputo & Mattson 2005, North Dumfries, BLS ATUS).
New: `params/athletics.yaml`, `params/care.yaml`, `params/expeditions.yaml` (38 parameters, 4
placeholders); references in `docs/SOURCES.md`.

**Model.** Rinks lie across the tube (their long side parallel to the spin axis, where motion
feels no Coriolis force), so the tube must hold a rink hall across it (`physics.box_tube_radius`).
Rinks (ice and roller) are counted from rink hours a person, skaters a session and open hours;
with training, recovery and sports-medicine space they add to the lived-in volume. Skaters along
the ring weigh `physics.ring_weight_factor` = (1 +- v w / g)^2. Injuries and surgeries come from
game and practice hours. Robots: massage tables by table hours, kitchen lines by meals, humanoids
by hours of hands-on care and chores at a robot's pace, with spares; their mass is carried by the
spinning ring, their power adds to the load. Landers carry propellant for some round trips
(`physics.rocket_propellant`). `habitat.rpm` is fixed at 1 (Jon's decision).

1. [x] A, spin: `athletics.skate_speed` **8.7 m/s** (7-11.15): varsity game peaks 8.66 / 7.98
   m/s men / women (Gamble et al. 2022); NHL EDGE record 24.94 mph. At 1 rpm a trained skater
   along the ring weighs **1.19 with the spin, 0.82 against**; the NHL record 1.25 / 0.78. Hall
   reports comfort criteria of 15% and 25% weight change set for walking and carrying; no study
   covers fast skating or sport at ~1 rpm. Limbs adapt "with 10-20 additional movements" even at
   10 rpm (Lackner & DiZio 1998); "A home team could take advantage of their adaptation" (Globus
   & Hall 2015). Pucks shot along the ring: 2.19 / 0.27 at 45 m/s. Rink floors should follow the
   ring's curve across their width (30 m drops 0.13 m).
2. [x] B, rinks: hall 64 x 34 m (IIHF: 2,000-2,200 m^2 halls for 58 x 28 to 60 x 30 m ice),
   clear height **7 m** (IIHF: 5 practice, 7 competition), ~800 m^2 of rooms a sheet; rink time
   **4 h ice + 1 h roller** a person a week (judgement within 5 (3-8) h; lifelong exercisers ~7
   h a week of exercise), 24 skaters a session, 121 open hours a week. Result: **14 ice sheets
   and 4 roller rinks** (P10-P90 11-20 and 2-7); Earth provision norms give 15-25 pads for
   10,000 players. Ice plant **68 kW** a sheet year-round (IIHF: 460-1,000 MWh/yr an arena,
   refrigeration ~43%): 1.0 MW in all. A rink across the tube needs a tube radius of at least 32 m.
3. [x] C, diet: `life.food_energy` 2,500 -> **2,700** kcal (2,200-3,300): adults at ~40 kcal/kg
   (ISSN: 25-35 for general fitness, 40-70 for 2-3 h a day of hard training), 20% children. Food
   power 13.5 -> **14.5 kW** a person.
4. [x] D, training, recovery and medicine: **15 m^3** a person beyond SP-413 (gym, recovery,
   sports clinic, a bigger hospital); SP-413 Table 3-2 has no gyms, rinks or sports clinic. With
   the rinks, **48 m^3** a person of athletic space, 3% of the 1,738 lived in. Injuries
   **1.6 a person a year** (rec games 12.2 per 1,000 game exposures, practice ~2 per 1,000 h),
   about **630 surgeries a year** ship-wide: an orthopaedic hospital (50 beds, 2 MRI, 2 CT, 4-6
   surgeons or surgical robots; an MRI magnet is a cortenforge-cfsem project).
5. [x] E, care by robots: done by people, pro-level care (2.5-4 h of hands-on care a person a
   week; NHL/NBA teams run 0.4-0.8 care staff a player) would take about **1,300 clinicians, 13%
   of the ship**. By robots: **234 massage tables** (1.5 h a person a week; Aescape-style, 45 min
   sessions), **15 kitchen lines** (400 meals an hour, Sweetgreen-class), **1,479 humanoids**
   (2 h of hands-on care + 10 h of chores a person a week at 1.5x a person's time, 20 h a day
   each): **230 t and 0.7 MW**. No robot stretches people yet, and kitchen robots assemble but
   don't cook: the humanoids carry that.
6. [x] F, expeditions: 4 reusable 6-crew landers of **18 t** (Apollo LM 2.2-2.6 t a crew member),
   **4.0 km/s** a round trip from low orbit (Apollo 3.97; Mars 4.8, Titan ~4.2, Callisto 4.0,
   Mercury 7.2), Isp **360 s**: **42 t of propellant a sortie**, 1,800 t in all with 10 sorties
   carried. Limits on stays: the 20 mSv/yr budget is ~15 days on the Moon or Callisto (1.37
   mSv/day, Chang'e-4) and ~31 on Mars (0.64, MSL RAD); Europa's surface ~5 Sv/day, no crewed
   stays. Coming back: balance recovers to 95% ~15 days after 6 months at 0 g; in mice lunar
   gravity "failed to prevent the slow-to-fast myofiber transition": for athletes, stays of about
   two weeks.

**Result** (`uv run mothership report`, 5,000 draws): the hockey ship weighs what the plain ship
did: **23.0 million t central** (P50 27.0, P10-P90 18.5-39.7; P50 was 21.0 when rpm drew up to
2). Rinks, robots and landers add 0.002 million t; everything athletic fits in the ring SP-413
already sized (its 0.9-1 g band holds 51.6 million m^3 against 17.9 million needed). Power 185 ->
**197 MW**: athletes' food (+10 MW), ice (1.0), robots (0.7). The tour still needs ~660 GW of jet
power.

**Finding: the tube now drives the ship.** With rpm fixed, one ring always holds everyone, and the
spread in mass is the tube's size: `habitat.tube_ratio` +0.91, shield +0.33, gravity_g +0.15
(the gravity band and lived-in volume dropped out, since the band always has room). SP-413 chose
its 65 m tube for ground: 67 m^2 of projected area a person (at least 40), a ~120 m wide ground
plane round the ring. The tube should be sized by that, not by a ratio (pass 3, item 1).

**Finding: stopping is the expensive part of a tour.** A low-thrust ship spirals in and out of
each orbit at ~0.93 of the circular speed each way (MIT 16.522): a visit to low orbit costs Moon
3.0, Mars 6.3, Mercury 5.4, Titan 2.8 km/s; reaching Callisto's orbit inside Jupiter's well costs
6.6-8.2 km/s each way, so one Callisto visit is about half of `tour`'s 30 km/s. Parking high (10
body radii) cuts a visit about 3x but asks ~1.5x more of the landers. The tour's delta-v should be
built from its stops (pass 3).

## Research pass 3 (2026-11-06): ground, the tour, the shield, science

Five topics in parallel (habitat geometry and the gravity band; the tour; the shield; the
remaining placeholders; science aboard, after Jon's "like cern too ... science with sports").
Placeholders 7 -> **0** (122 parameters). New: `params/tour.yaml`, `params/worlds.yaml` (JPL
data), `params/science.yaml`; references in `docs/SOURCES.md`. Key quotes rechecked by hand
against the fetched pages and PDFs the researchers saved (SP-413 ch. 4-5 and app. 4A-4B, MIT
16.522, Globus & Strout, ESRF, CERN).

1. [x] **Tube from ground area** (model). SP-413: "In a torus the projected area is a strip
   through the diameter of the tube of the torus", Ap = 4 pi r R, on "the central plain running
   the full circumference of the torus along the middle of the tube"; "the radius needed to
   enclose the 670,000 m^2 of projected area can be quite small". `physics.ground_area` (the
   widest chord in the band, at the tube's centre unless the band stops lower) reproduces it
   within 2% (`test_ground_area_reproduces_sp413`). `habitat.tube_ratio` -> **`ground_area_per_
   person` 67** (40-155: SP-413's minimum 40; its whole floor 155, Kalpana One 170) and
   `max_tube_ratio` 0.2 (more rings past it). The rinks' 54,000 m^2 of ground make the tube
   **70 m** (SP-413: 65).
2. [x] **Tour from stops** (model, `model.tour_dv`): Earth (home orbit at 60 Earth radii) ->
   Mars -> Ceres (water) -> Callisto (outside Jupiter's worst belts) -> Titan (methane) -> Earth.
   Legs: Edelbaum spirals with the true plane change (nodes included) while the drive's
   acceleration is under 0.3 of the Sun's pull, Hohmann transfers beyond (Jupiter outward:
   months of thrust against years of coast). Spirals cost 1 - 0.754 eps^(1/4) of circular speed
   (MIT 16.522). The ship parks at **7 body radii** (Deimos's orbit at Mars, ~1/3 of the Hill
   radius at Callisto and Titan); landers carry the rest (Hohmann to low orbit and back). Result:
   **69.1 km/s** (P10-P90 68.8-72.4): home 1.4, legs 40.5 (15.7 of it the Hohmann home from
   Saturn), Mars 2.3, Ceres 0.2, Callisto 14.6, Titan 10.2; pass 2's flat 30 km/s was 2.3x low.
   Checks: Dawn's ion drive gave "almost 11.5 km/s" (Rayman & Garner 2018); JIMO's Callisto-
   Ganymede-Europa tour needed "nearly 25 km/s". Moon flybys could cut the Jupiter and Saturn
   spirals by ~30% and more (Ross et al. 2003: "using only 22 m/s" between Callisto, Ganymede and
   Europa with years of flight), not modelled.
3. [x] **Shield**: regolith 10 -> **10.3 t/m^2** (9.5-11.1, log-interpolated to 20 mSv/yr in
   Globus & Strout's Table 2). Options now in the report: **water 6.6 t/m^2 (15.3 Mt against
   23.9)**, the same dose for 36% less; an **active magnetic shield over 0.5 t/m^2 of passive
   (~3.7 Mt, low confidence: only SP-413 studied one at settlement scale and rejected it)**;
   **spinning the shield** with the habitat costs ~6.6 Mt more ring (SP-413's reason for a still
   one; Kalpana One spins it to avoid "catastrophic failure modes"). Water for a shield is ~360x
   the settlement's own water; at ~2 MJ/kg to extract (EMMI), 15 Mt is ~0.9 GW-yr.
4. [x] **Placeholders**: `habitat.shell.allowable_stress` **320 MPa** (A514 steel, ASME VIII-2 /
   NASA-STD-5001B; SP-413 used aluminium at 234); `power.habitat_radiator_temp` **280 K** (SP-413
   "Assuming a radiator temperature of 280 K"); `care.robot_pace` **2** (Dyna-1 "60% of human
   throughput", laundry folding ~3.4x slower); `care.kitchen_kw` -> **`kitchen_kwh_per_meal`
   1.6** (LBNL, fast food median 1.88 less heating); `habitat.min_inertia_ratio` **1.2** ("at
   least 1.2 times greater than any other axis", Globus et al. 2007); `expeditions.sorties_
   carried` -> `sorties_per_stop` 3 (judgement); `habitat.gravity_band` **0.1** (0.06-0.15:
   Queijo 1988's +-3% decks, Jensen 2024's 0.95-1.1 g).
5. [x] **Science** (Jon: "like cern too"): **3,000** people doing science (0.3 of the ship, judgement;
   CERN 2,500 staff and 12,200 users), **16 m^3** a person of labs, **28.7 MW**: labs 3.6, data
   centre 4.0 (CERN's 4 -> 12 MW), a **collider round the ring inside the still shield** 15 MW
   (the LHC's 87 MW scaled by length), a light source 6 (ESRF), a zero-g lab 0.06. With 16 T
   dipoles the collider reaches **2.9 TeV a beam** (5.8 TeV collisions; Tevatron ~1, LHC 6.8),
   7,600 t of magnets. Space gives its vacuum ("at least 100 times better than the vacuum in the
   beam pipes of the LHC" on the Moon, Beacham & Zimmermann 2022); the shield absorbs its outward
   losses, its inward side needs metres of local shielding at collimators and dumps.

**Result** (`uv run mothership report`, 5,000 draws): **25.1 million t central** (P50 31.5,
P10-P90 22.6-45.7), shield 23.9 of it; **228 MW** (science 29, robots 2.7, ice 1.0). The tour
needs **1.7 TW of jet power** and 3.6 million t of drive and propellant (start 28.7 Mt); `brisk`
6.7 TW and 14.8 Mt. Spin stable in all draws.

**Finding: how roomy the ship is drives everything.** `habitat.ground_area_per_person` is +0.99:
SP-413's minimum 40 m^2 a person gives 16 Mt, its 67 gives 25, 100 gives 36, and Kalpana One's
~170 needs two rings and ~60 Mt. That is a choice for Jon, not a fact to research.

**Finding: water is the cheaper shield and the tour passes water.** The same 20 mSv/yr for 36%
less mass, and Ceres, Callisto and Titan are on the route; regolith is only cheaper where the ship
is built (lunar material at L5).

## Pass 4 (2026-11-06): Jon's three choices, mist farms

Jon took the three recommendations (`docs/PLAN.md`): a water shield for 10 mSv/yr, 67 m^2 of
ground a person all for living, and farms as aeroponic ultrasonic mist racks "wherever it can".
One researcher on the farms; the shield rows rechecked by hand in Globus & Strout's Table 2.

1. [x] **Shield: water, 10 mSv/yr.** `habitat.shield.areal_density` -> the dose target and the
   OLTARIS table's deepest rows, extended by their e-fold (`physics.shield_areal_density`):
   water 7 t/m^2 gives 16.1 mSv/yr and the dose falls by e every 2.01 t/m^2 (6 -> 7), so 10
   mSv/yr takes **8.0 t/m^2** (a 1 t/m^2 extrapolation past the table); regolith 11.8. A
   `code_factor` (0.77-1.3) carries the transport codes' ~30% spread. Shield **18.5 million t**
   (regolith for the same dose 27.4).
2. [x] **Ground for living.** `ground_area_per_person` stays 67 but is all living ground now (SP-413
   had 46.6 community + 20.4 farms); `usable_volume_per_person` 1,738 -> `community_volume_per_
   person` **823** (SP-413's community subtotal) in the band. The tube stays 70 m (ground binds).
3. [x] **Mist farms anywhere in the tube** (model: farms need only the tube's total volume, not the
   band or the ground). Grow area from `life.food_per_grow_area` **60 kcal/m^2/d** (28-93: Johnson
   et al. 2021 '40-50 m2' a person, Salisbury & Bugbee '30 m2' for 2,800 kcal, BVAD's all-crop
   diet 65 m^2 for 1,850): **45 m^2 a person**; racks ~1 m a tier with access, **1.4 m^3/m^2**:
   **63 m^3 a person** against SP-413's 915; **80 kg/m^2** of racks, water and crop (BVAD 101.5,
   HPS era): 3.6 t a person against SP-413's 22 t of soil, so `interior_mass_per_person` 53 ->
   **31**. Power: misters **20 W/m^2** (derived, low confidence), fans and pumps 6% of the lights
   (Kozai 2013): food **16.3 kW** a person (was 14.5).

**Finding: ultrasonic foggers grew plants poorly where tested.** Aeroponics works ("remarkably
improved root growth") but gives no more food than hydroponics ("the greater root growth did not
lead to greater shoot growth compared with hydroponics", Li et al. 2018). Of four misters, "the
plants did not grow well" under the 4.89 um ultrasonic fogger and best under an 11.24 um
air-assisted nozzle (Tunio et al. 2022); "the high-frequency (1.7 MHz) ultrasonic atomizer is not
suitable for aeroponics cultivation" (Lakhiar et al. 2018, nutrient EC and pH drift). Jon's call:
ultrasonic as chosen, or ~10-20 um air-assisted / high-pressure mist. Plants also look fine at
lower gravity ("0.38 g may be enough", Kiss 2014), so farms could go in spokes or an inner ring.

**Result** (5,000 draws): **19.4 million t central** (P50 24.5, P10-P90 17.4-35.8), down from 25.1:
the water shield at half the dose (-5.4 Mt) and no soil (-0.2 Mt). **245 MW** (food 16.3 kW a
person). The tour needs **1.35 TW** of jet power (was 1.7). How roomy the ship is still drives the
spread (`ground_area_per_person` +0.99).

## Pass 5 (2026-11-06): the farms, the backbone

Jon: "we can do research on state of the art aeroponic practices first, as thats the backbone of
this, as food/herbs/spices/medicine are sacred to humans". Four topics in parallel: aeroponic
engineering; a complete diet; herbs, spices and medicinal plants; the rest of the food system and
the nutrient loop. New: `params/crops.yaml` (13 crops), `params/food.yaml` (other food, gardens,
plant-made medicine, nutrient loop); `life.yaml` reworked (LED efficacy and delivery, yield gain,
rack geometry, mist power); `model.food_system`.

1. [x] **Mist: high-pressure, not ultrasonic (finding; Jon chose ultrasonic).** Two comparative
   trials put an ~11 um high-pressure nozzle first and the 1.7 MHz ultrasonic fogger last, below
   soil (Tunio et al. 2023: shoot fresh weight 73.74 against 2.73 g a plant). Fog at ~3-5 um sits
   on the floor where "Aerosol droplets < 2 um are thought unlikely to deposit on the root
   surface" (Eldridge et al. 2020); ultrasonic atomising drifts the solution ("the EC value
   decreased and pH increased", Lakhiar et al. 2018), heats the root zone (~90 Wh a litre), and
   its transducers are rated for demineralised water. Only company data favour it (LettUs Grow).
   Continuous fine "dry fog" (8.85 um, two-fluid nozzle) matched hydroponics (Hikosaka et al.
   2014). Power: ultrasonic **17 MW** for the ship's racks, high-pressure **0.3 MW**.
2. [x] **Practice for a ship where a farm failure is a famine:** roots survive ~1 h without mist
   and die within ~12 h (CIP: "if an irrigation pump breaks down on a Friday night and it is not
   repaired in the following 12 hours ... the plants ... will die"); power cuts are "the greatest
   risk factor". So: many small independent loops with spare pumps and accumulators for ~1 h,
   lights dimmed on a mist fault, UV (Fusarium "completely eliminated ... at a UV-dose of 70 mJ
   cm-2", Runia 1994) and filtration on every return, EC ~1.6 dS/m, pH ~5.8, roots below 20 C,
   and a share of deep-flow hydroponic racks as a water-buffered hedge (~56 L/m^2 against ~15).
3. [x] **A complete diet from 13 crops** (BVAD Rev2 / NASA Biomass Production Chamber yields and
   light, USDA composition): wheat 21% of crop kcal, potato 13, pulses 12, soybean 9, oils 7,
   fruit 7, rice 6, peanut 6, vegetables 6, sweet potato 5, nuts 4, maize 2, sugar 2. **53 m^2 of
   crop racks a person** (BVAD's all-crop diet took 65 m^2 for 1,850 kcal); 1.09 kcal of food a
   mol of light. No staple has been grown aeroponically to harvest with a reported yield, and
   EDEN ISS warns aeroponics may "lower the harvest index". Fresh food matters: 85% of Antarctic
   crews said food grown at the station "would have improved their overall well-being"; "The
   most common gripe was the boring food" (Mars-500).
4. [x] **Herbs, spices, medicine, beverages**: herbs 0.12 m^2 a person (basil "optimal when DLI is
   14 mol"), spices 1.0 (saffron forces in stacked racks on ~3.6 mol a day; ginger and chili
   grow indoors; cinnamon, pepper and vanilla have no indoor yields), medicinal plants 0.2
   ("Aeroponics appeared to be the most productive system in CE for medicinal crops where the herb
   ... or roots were harvested", Hayden 2006; UV-B gave no reliable artemisinin gain), a tea,
   coffee and cacao grove 3 m^2 (tea plausible; coffee has no controlled-environment data at all).
   **Plant-made medicine**: ~60 m^2 of Nicotiana benthamiana makes ~1 kg of purified antibody or
   vaccine protein a year ("yielding up to 3-5 g/kg of FW", "usually within 4 to 7 days"; Health
   Canada approved the plant-made vaccine Covifenz in 2022), ~30 kW; small-molecule drugs still
   need a chemistry line.
5. [x] **The rest of the food system** (shares of all kcal): hydrogen-oxidising bacteria on cabin
   CO2 10% (~0.0066 kWh/kcal, ~22x less than LED crops, ~60x less per kg of protein), fungi on
   crop waste 6% (the crops leave ~0.7 kg dry a person a day), precision-fermented dairy 4%,
   algae 2% (DHA; not B12), mealworms on waste 2%, eggs and fish 1% (fed from crops each kcal
   costs ~6-15x a crop kcal: 1% is ~9 MW). B12 and vitamin D from fermentation and UV-B; iodine
   from seaweed. Crops make **75% of the kcal**; protein **2.7 g/kg/day** (need ~1.6).
6. [x] **The nutrient loop**: ~95 kg of nutrient salts a person a year (BVAD), urine nitrified at
   "95-100% efficiency" (MELiSSA), phosphate as struvite ("more than 90%"), Lunar Palace 365's
   "material closure degree of 98.2%"; at 95% closure the make-up is ~48 t a year ship-wide, a
   lifetime's stock ~0.01% of the ship. Water recovery 98% (ISS with its brine processor).

**Result** (5,000 draws): **19.4 million t** (farms change power, not mass); **211 MW** (was
245): food **12.9 kW** a person (lights and fans ~9.8, ultrasonic misters 1.7, microbes, fungi, algae and
animals 1.4, the loop 0.03). With high-pressure mist instead: ~194 MW.

**Jon's calls** (same day): "ideally vegan/vegetarian too. and ok to your recommendation for the
aeroponic system". `life.mist_w_per_grow_area` 30 (ultrasonic) -> **0.5 W/m^2** (high-pressure;
ultrasonic kept as an option, 17.8 MW); insects and eggs/fish 0; `life.deep_flow_share` **0.2**
of racks as a water buffer (+41 kg/m^2 of water). Result: **189 MW** (food **10.7 kW** a person:
lights and fans ~10.1, microbes, fungi, dairy and algae 0.5), crops **78%** of kcal on **55 m^2**
of racks a person (59 with the gardens), protein **2.5 g/kg/day**; 19.4 million t.

## Next (pass 6)

1. **cortenforge-cfsem: the active shield** (coils, field, forces, stored energy -> structure
   mass), the only option that could cut the 18.5 Mt water shield several times; then the
   collider's dipoles round the ring and the hospital's MRI magnet.
2. **Refuelling and staging** (model): split the tour at refuel stops (Ceres, Callisto, Titan;
   water gives 0.112 kg of H2 a kg), moon flybys in the Jupiter and Saturn systems.
3. Model: farms in low-g spokes or an inner ring (plants look fine at lower g: "0.38 g may be
   enough", Kiss 2014), O'Neill cylinders; heat pumps on the habitat radiators; the lifelong
   ceiling (VO2max falls ~10% a decade even in trained people, Tanaka & Seals 2008; lifelong
   exercisers at ~75 keep about 1.5x the VO2max of sedentary peers, Gries 2018).
