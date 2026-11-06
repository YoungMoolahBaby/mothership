# Sources

Sources behind parameters and checks. Exact quotes live in the `source` fields of
`params/*.yaml`. Checked by hand in pass 1: SP-413 chapters 3 and 5, Globus & Strout 2017.

## Habitat and human factors

- NASA SP-413, "Space Settlements: A Design Study" (1977): https://settlement.nss.org/75SummerStudy/
  (Chapt3, Chapt4, Chapt5, 4appendB): 10,000 people, 1 rpm, 0.9-1 g, 1,738 m^3 and 67 m^2 a
  person (Table 3-2), major / minor radius 830 / 65 m, 69 x 10^6 m^3 enclosed, 50.8 kPa (Table
  4-3), internal masses 530,000 t (Table 5-3), shield 9,900,000 t of 1.7 m slag with a ~1.5 m
  gap (Table 5-2), 3 kW a person consumed.
- Globus & Strout, "Orbital Space Settlement Radiation Shielding", NSS Space Settlement Journal
  (2017): https://nss.org/wp-content/uploads/Orbital-Space-Settlement-Radiation-Shielding-Globus.pdf
  (OLTARIS dose vs shield mass; 10-11 t/m^2 regolith, 6-7 water or polyethylene for 20 mSv/yr).
- Globus & Hall, "Space Settlement Population Rotation Tolerance" (2015):
  https://nss.org/wp-content/uploads/Space-Settlement-Population-Rotation-Tolerance-Globus.pdf
- Hall, AIAA 99-4524 (comfort boundaries, Graybiel's slow rotation room):
  https://spacearchitect.org/pubs/AIAA-99-4524.pdf
- Clement et al. 2015, artificial gravity review: https://pmc.ncbi.nlm.nih.gov/articles/PMC4470275/
- Ellman et al. 2013, partial weight bearing in mice: https://pmc.ncbi.nlm.nih.gov/articles/PMC4118556/
- Wessel et al. 2018, NASA exploration atmosphere (56.5 kPa / 34% O2):
  https://asma.kglmeridian.com/downloadpdf/view/journals/amhp/89/9/article-p792.pdf
- Hancco et al. 2020, La Rinconada: https://www.frontiersin.org/journals/physiology/articles/10.3389/fphys.2020.00773/full
- NASA career dose limit 600 mSv: https://www.nasa.gov/wp-content/uploads/2023/03/radiation-protection-technical-brief-ochmo.pdf
- Earth's atmospheric column: 101.3 kPa / 9.80665 m/s^2 = 10.3 t/m^2 (computed).
- Torus shell stress: meridional stress p r (2R - r) / (2 t (R - r)) at the inner equator
  (thin toroidal shell, Roark's Formulas for Stress and Strain).

## Food and power

- Kusuma, Pattison & Bugbee 2020, "From physics to fixtures to food", Horticulture Research:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC7105460/
- NASA BVAD Rev 2 (2022), Baseline Values and Assumptions Document:
  https://ntrs.nasa.gov/api/citations/20210024855/downloads/BVAD_2.15.22-final.pdf
  (light delivery, crop yields and light, diet area, ECLSS power).
- Bugbee & Salisbury 1988, wheat yield and efficiency: https://pmc.ncbi.nlm.nih.gov/articles/PMC1055676
- Salisbury, Bugbee & Bubenheim 1987, CELSS size and lighting: https://ntrs.nasa.gov/citations/19880029853
- EIA, US energy per person: https://www.eia.gov/tools/FAQs/faq.php?id=85&t=1

## Power plants and drive

- ITER mass and power: https://www.iter.org/node/18506
- ARIES-CS (compact stellarator): https://www.nifs.ac.jp/itc/itc18/dir_presentation/presentation_upload/I-29_Najmabadi.pdf,
  https://fti.neep.wisc.edu/fti.neep.wisc.edu/presentations/lae_iaea0607.pdf
- ARC: Sorbom et al. 2015, https://arxiv.org/abs/1409.3540
- Siamidis et al., NASA TM-2005-213337 (Brayton efficiency vs radiator temperature, radiator mass):
  https://ntrs.nasa.gov/api/citations/20050160234/downloads/20050160234.pdf
- Mason, space nuclear power conversion: https://ntrs.nasa.gov/api/citations/20150012286/downloads/20150012286.pdf
- NASA TM-104335, radiator coatings: https://ntrs.nasa.gov/api/citations/19910013054/downloads/19910013054.pdf
- Williams et al., Discovery II, NASA TM-2005-213559:
  https://ntrs.nasa.gov/api/citations/20050160960/downloads/20050160960.pdf
- Direct Fusion Drive: https://arxiv.org/pdf/2009.12621, https://arxiv.org/pdf/2002.12686
- NASA TM-104503, tankage fractions: https://ntrs.nasa.gov/api/citations/19920001996/downloads/19920001996.pdf
- Power-limited rocket: Stuhlinger, "Ion Propulsion for Space Flight" (1964).
