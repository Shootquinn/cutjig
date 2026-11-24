## Findings that change the register

| # | Claim | Result | What the source says |
|---|---|---|---|
| F-1 | "Iris pinches the core 106.369 mm behind the cutting face" (extraction section 3 and 7; test F4; Echo registry; Design Notes) | CONTRADICTED as worded | double_dong_params.py lines 372-378: 106.369 is the distance from the head tip (z -789.1834) to the kerf SPHERE CENTRE (z -682.8144). Not the pinch plane. Lines 379-380: the dome pole sits CORE_IRIS_STANDOFF - kerf sphere R = 106.369 - 71.4375 = 34.9315 mm behind the face. Lines 376-378: the core is "pinched off INSIDE the head", stub 31.76 mm on axis, 50.99 mm at core rim. My arithmetic (not in the source): at a 50 mm core radius the sphere meets the core about 55 mm behind the face. The number is real; its label is wrong. 7 in model only. |
| F-2 | Spin 1 to 60 rpm as the cutter spin | VERIFIED as text, NOT VERIFIED as drill spin | summary_yokeless_motor.md line 158: "Operating range is 1-60 RPM" (Track 2 brake thermal-crossover analysis); line 200: M5 brake/aft-complexity motor "0-60 RPM". ip_and_competitive_position.md line 59: Hall trials at 2/20/60 RPM. No read line says the cutter spins at 1 to 60 rpm. The range belongs to the Borebot motor/brake subsystem. |
| F-3 | "Cutter OD 152.4 mm" (extraction section 3, design consequence) | UNVERIFIED | No source gives a cutter OD of 152.4 mm. 152.4 mm is the tubing OD (workorder.md, derived). The only sourced cutter diameter is 7.00 in = 177.80 mm (borebot_operating_envelope.md line 29), the 7 in generation. Workorder.md states the cutting face is out of scope. Test A2 may use a 152.4/146.05 tube as a stated assumption, not as the cutter. |
| F-4 | Core diameter tolerance +/-1 mm | UNVERIFIED (confirmed) | No tolerance in INSITU2 lines 157-190, 397-434, 514-519, 830-837, csm_sow.md lines 22-27 and 54-62, csm_package.md lines 54-58. Searched only the cited ranges. |
| F-5 | Torque 20 N m (jig) and 50 N m (iris) | UNVERIFIED (confirmed) | INSITU2 lines 408-411: closure torque is a measurement to be taken ("Output is the full torque curve in N-m versus angle"). No value stated. |
| F-6 | Core nominal 100 mm | VERIFIED with a conflict | INSITU2 lines 406-407: "CSM low-density concrete simulant cores pre-cast to 100 mm diameter to match the iris aperture." Same document, lines 186-188, Figure 2 caption on the full-scale 6 in drill: "Core diameter is above 100 mm." The 100 mm applies to Phase I EDU test cores. csm_sow.md line 56 says only "matching the iris aperture", no number. The 90 to 105 range comes from workorder.md alone. |
| F-7 | Iris open aperture | UNVERIFIED | params line 92: "aperture 54.2925 -> 0.0000 mm", unit (radius or diameter) not stated. Not the 6 in design. |

## Priority items

| Item | Status | Location and note |
|---|---|---|
| Iris leaf count 4 | VERIFIED | double_dong_params.py lines 93-98 (census 1041 to 1044). 7 in model. |
| Pivot positions (+/-66.7945, 0, -711.6599) and (0, +/-66.7945, -711.6599) | VERIFIED | lines 94-97. |
| Pivot axis direction (0.9181, 0, -0.3965) | VERIFIED | lines 94-97. Tilt 23.3573 deg appears only in the comment, line 367: R = 66.7945 / cos(23.3573 deg) = 72.7569. My check: atan(0.3965/0.9181) = 23.36 deg. Consistent. |
| Spherical motion, axes meet bore axis at z = -682.814389 | VERIFIED | lines 361-366, attributed to the Loftsman (derived, not measured). |
| Face radii 71.4375 (core side), 74.6125 (rock side) | VERIFIED | line 368 comment, "measured shell faces"; also line 360 `CORE_KERF_SPHERE_R_MM = 71.4375`. |
| Leaf thickness 3.175 mm | VERIFIED | lines 402-404 (`CORE_KERF_WIDTH_MM`), "0.125 INCH exactly -- the plate thickness". Extraction cites "line 410-411"; actual location is 402-404. Source calls it the plate thickness; extraction calls it DERIVED. |
| Closure -62 deg per leaf | VERIFIED | line 92. |
| Standoff 106.369 mm (= 106.4 rounded) | VERIFIED as a number, MISLABELED, see F-1 | line 372 (`CORE_IRIS_STANDOFF_MM`). Head tip ZMin -789.1833947 verified in gpr cr_scratch/step40_iris_sizes.json line 5; the census id 1000 for that entry was not read. Sphere centre -682.814389 (line 362). Difference 106.369. |
| Leaf bbox (r 52.93, z -723.987 to -654.214) | PARTLY VERIFIED | ZMin -723.987 appears at lines 17, 29, 41, 53 of step40_iris_sizes.json. The -654.214 maximum and the r 52.93 were not read. |
| Adjacent-leaf overlap 34.58 / 339.08 mm3 | VERIFIED | params lines 102-104. |
| Model is 7 in, not 6 in | VERIFIED | params lines 354-356: `CORE_BORE_OD_MM = 177.8`, `CORE_OD_MM = 100.0`, annulus wall 38.9 mm. |
| Core length 500 mm | VERIFIED as Quinn's DECLARED value | params lines 357-359. Not a Mines value. Register row is correct. |
| WOB 100 to 1000 N | VERIFIED | INSITU3_text.md lines 424-430: "set at 100-1000 N", benchmarked to the Honeybee Planetary Deep Drill (Zacny 2016, 64 mm); upper bound "set by the anchoring force limit of the Borebot's wall-anchored locomotion system." borebot_operating_envelope.md line 58 gives 100 - 1000 N; line 59 paraphrases the upper-bound sentence in quotation marks that are not verbatim. It is a Phase I drilling-mechanics test range, not a stated jig load rating. Using 1000 N as the jig design load is a design choice and should be labelled so. |
| Penetration >= 5 mm/min at WOB >= 100 N | VERIFIED | INSITU3_text.md lines 267-268. |
| Core diameter 100 mm | VERIFIED with conflict, see F-6 | INSITU2 lines 406-407. |
| Tubing 6.00 in OD / 5.75 in ID / 1/8 in wall | VERIFIED (contract) | workorder.md, sole primary source. |
| 6.00 in = 152.40 mm; 5.75 in = 146.05 mm; wall (152.40 - 146.05)/2 = 3.175 mm = 0.125 in | VERIFIED (recomputed) | Arithmetic is exact. |
| Radial gaps 28.025 / 25.525 / 23.025 / 20.525 mm at 90 / 95 / 100 / 105 mm cores | VERIFIED (recomputed) | (146.05 - d)/2. Ratio 146.05/105 = 1.391 confirmed. 7 in model annulus 38.9 mm confirmed. |
| Spin 1 to 60 rpm, Hall trials 2/20/60 | VERIFIED as text, see F-2 | summary_yokeless_motor.md lines 158, 200; ip_and_competitive_position.md line 59. |

## Remaining extraction rows

| Row | Status | Location |
|---|---|---|
| C2 / section 4: no jig actuator; drill drivetrain via braked planetary sun gear | VERIFIED | INSITU2_text.md lines 157-161. |
| Hall amplitude about 400 to about 45 counts | VERIFIED | lines 161-163. |
| Release by reversing braking torque | VERIFIED | lines 164-165. |
| Load cell in back cap near gearbox; gearbox swappable; metal blades; predecessor plastic | VERIFIED | lines 398-405. |
| Closure torque vs angle 0 to 90 deg in 10 deg steps; retention force N=9 | VERIFIED | lines 408-414. |
| Marker depths 25, 50, 100, 150, 200 cm | VERIFIED | lines 425-428. These are "columns"; lines 516-517 and 830-832 call them "cores". Length is not stated. |
| Core count at least 12 plain plus at least 12 layered | VERIFIED | INSITU2 lines 514-518 and 830-833; csm_sow.md lines 56 and 58. |
| csm_package estimate 40+ / 15 / 30 | VERIFIED | csm_package.md line 56. The 15 is "depth-series captures", not cores. Sources disagree, as C11 says. |
| Dreyer low-density concrete; replicates strength and fracture behaviour of ice-cemented regolith | VERIFIED | csm_sow.md line 24 (drilling SOW), line 56 (iris cores). |
| Properties delivered: strength, fracture toughness, density, grain size | VERIFIED | csm_sow.md lines 27, 61. |
| Borebot OD 6.375 in; cutter 7.00 in; design bore 7.25 in; train bore 7.5 in | VERIFIED | borebot_operating_envelope.md lines 24-30, 38. |
| Ascent test 600 s at 1x, 1.5x, 2x | NOT CHECKED | INSITU2 lines 444-461 not read (budget). Treat as UNVERIFIED by this review. |
| Docx holds no geometry (C1) | PARTLY VERIFIED | iris.txt keyword search, first 20 matches (lines 37, 124 long and not displayed): torque, retention and cycling as test activities only; no numeric geometry in the lines seen. |
| Mines zip holds no core dimensions (section 6) | NOT VERIFIED | The six files are PDF and XLSX; PDF render failed (pdftoppm not installed). Claim rests on the Engineer's text read only. |
| gameplan.md line 141 model-of-record; FCStd not on this machine | NOT CHECKED | outside the cited-range budget. |

## Tests that must be marked UNVERIFIED under A.10 item 2

1. Core tolerance +/-1 mm: C8, T5, F3, and any F-group test reading `params.core.tol`. Assert as a labelled assumption.
2. F4 (exposed core above holder >= 106.369 mm + margin): the number is the sphere-centre standoff, not the pinch plane (F-1), and it is the 7 in model. UNVERIFIED as a pinch offset and for the 6 in drill.
3. Any test that states a spin speed as the cutter spin (S2, scoping agenda): the 1 to 60 rpm range is the motor/brake range (F-2). UNVERIFIED as drill spin until a source says so.
4. Any test or A2 text that calls 152.4 mm the cutter OD (F-3). Keep-out tube 152.4/146.05 may stand as a workorder-derived assumption only.
5. Loads tests using 20 N m or 50 N m (F-5). Axial 1000 N: label as design choice bounded by the SBIR test range.
6. Core length 500 mm, core mass 9.4 kg, density 2400 kg/m3: UNVERIFIED as Mines requirements (register already correct).
7. Core count, any "Mines specifies/requires/delivers" sentence, Mines zip contents: UNVERIFIED (sources disagree; zip unreadable here).
8. Iris open aperture and anything about the 6 in iris (F-7); also which 2026 STEP is the 6 in drill.
9. Ascent test profile (lines 444-461), printer bed/material/nozzle, 30-6060 catalog and stock: not verified by this review.
10. Core nominal 100 mm tests (P2, C8, S2): may stay TRACED, but must say "Phase I EDU test cores, INSITU2 lines 406-407" and carry the Figure 2 caption conflict (F-6).

## Register edits required

- Row "Spin 1 to 60 rpm": change from TRACED to VERIFIED-as-text, UNVERIFIED-as-cutter-spin.
- Row "Iris standoff 106.369 mm": relabel "kerf sphere centre standoff from head tip"; add pole at 34.9315 mm (params lines 379-380).
- Add row: cutter OD 152.4 mm, UNVERIFIED.
- Extraction line cites to correct: leaf thickness is params lines 402-404, standoff line 372, face radii lines 366-368.
