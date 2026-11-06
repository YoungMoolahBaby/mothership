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

## Next (pass 3)

1. **Tube from ground area** (model): size the tube by projected area a person (SP-413 67 m^2, at
   least 40), the lived-in volume in the band and the rink fit, instead of `tube_ratio`.
2. **Tour from stops** (model): heliocentric legs plus spirals at each stop (or a high parking
   orbit and bigger landers); gravity assists in the Jupiter and Saturn systems.
3. `habitat.shield.areal_density` (+0.33): shield material (water from asteroids vs slag) and an
   active magnetic shield (a cortenforge-cfsem project).
4. Placeholders (7): `care.robot_pace`, `care.kitchen_mass`, `care.kitchen_kw`,
   `expeditions.sorties_carried`, `habitat.shell.allowable_stress`, `power.habitat_radiator_temp`,
   `habitat.min_inertia_ratio`.
5. `habitat.gravity_band` (SP-413 calls its 10% arbitrary) matters again once the tube is fitted.
6. Model: farms in low-g decks (plants may not need 1 g), a spinning-shield variant, O'Neill
   cylinders; the lifelong ceiling (VO2max falls ~10% a decade even in trained people, Tanaka &
   Seals 2008; lifelong exercisers at ~75 keep about 1.5x the VO2max of sedentary peers, Gries
   2018).
