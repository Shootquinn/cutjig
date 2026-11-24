## Step 1 gate: Fact-Checker verdict table

Files read: gate decisions, extraction file, step1 foundation report, params.yaml (Grep), gameplan Register 377-411 and Design Notes 8, 12 (558-612), INSITU2 157-166, 186-188, 406-414, INSITU3 267-268, 424-430, four Mines PDFs (text extracted with pdftotext to scratchpad `mines_fc/`; originals untouched). `C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\gpr\double_dong_params.py`: **path not found** (recorded, not searched for).

### 1. PATCHED lines in step0_engineer_source_extraction.md

| Line | Claim | Source checked | Verdict |
|---|---|---|---|
| 9 (C3) | 1 to 60 rpm is motor and brake range, not cutter spin | summary_yokeless_motor.md, ip_and_competitive_position.md: not in the named file set | NOT CHECKED (outside named files). Prior F-2 stands; not re-read this run |
| 11 (C5) | 20 and 50 N m retired; no source states a torque; closure torque vs angle 0 to 90 deg, 10 deg steps is a Phase I measurement; 10 N m DECLARED | INSITU2 408-411: "Closure torque... 0 to 90 degrees at 10-degree increments... Output is the full torque curve in N-m versus angle" | MATCHES. No torque number in 406-414. Retention N=9 at 411-413 also matches |
| 15 (C9) | 100 mm = Phase I EDU cores "pre-cast to 100 mm diameter to match the iris aperture"; Figure 2 caption "Core diameter is above 100 mm" | INSITU2 406-407 and 186-188 | MATCHES both quotes. Caption describes "Full scale 6" core drill", so the conflict is real |
| 15 (C9) | "Mines budget justifications, LOIs and budgets (the zip contents) state no core diameter, length, mass or delivery state" | Four PDFs read; XLSX budgets never opened (foundation line 41) | PARTLY. True for the 4 PDFs. "and budgets" is unsupported: the XLSX were not read |
| 16 (C10) | Rigged model is 7 in generation, bore 177.8 mm; lines 354, 91-96 | double_dong_params.py | PATH NOT FOUND. Also internal inconsistency: C10 cites 91-96, row 37 cites IRIS_LEAVES 93-98 |
| 38 | Leaf thickness 3.175 mm, plate thickness, lines 402-404 | double_dong_params.py | PATH NOT FOUND (not re-verified) |
| 42 | Face radii 71.4375 / 74.6125, lines 366-368 | same | PATH NOT FOUND |
| 43 | 54.2925 mm is a radius; open diameter 108.585 mm DECLARED | gate B1 text; arithmetic 2 x 54.2925 = 108.585 | Gate claim matches B1. Tag cell reads MEASURED, not DECLARED (see fix 4). Line 92 not re-read: PATH NOT FOUND |
| 44 | Open diameter parameter; "INSITU2 states the aperture matches a 100 mm core" | INSITU2 407 | MATCHES (pre-cast to 100 mm "to match the iris aperture"). Tag cell "MEASURED / DECLARED" |
| 47 | 106.369 mm head tip to sphere centre; dome pole 34.9315 mm; lines 372-380 | double_dong_params.py | PATH NOT FOUND. Arithmetic 106.369 - 71.4375 = 34.9315 checks |
| 66 | 152.4 mm is tubing OD not cutter OD; 177.80 mm cutter; 106.369 carried by ASSUMED | borebot_operating_envelope.md: not in named set | NOT CHECKED for 177.8; ASSUMED labelling is correct |
| 87 | Spin patch | as line 9 | NOT CHECKED |
| 99 | Diameter: 100 mm Phase I EDU, 186-188 conflict | INSITU2 406-407, 186-188 | MATCHES |
| 105 | Four PDFs read with pdftotext; no core dimension, length or mass; LOI subcontract $74,250 for 9/1/26-1/30/27 | Mines PDFs | MATCHES. LOI 260647 text: "Mines will be issued a subcontract by Unleashed Robotics at the proposed federal level of $74,250 for the period 9/1/26-1/30/27". "XLSX not opened" is stated honestly. First sentence "They carry budget and commitment language only" is fine for PDFs |
| 110, 111, 114 | Open aperture resolved by B1; 10 N m by B4; STEP moot | gate decisions | MATCH gate text |

Unpatched lines checked against named ranges, for completeness:

| Line | Claim | Source | Verdict |
|---|---|---|---|
| 8 (C2) | No external actuator; planetary sun gear braked; Hall; release by reversing braking torque | INSITU2 157-166 | MATCHES (Hall "approximately 400 to approximately 45 counts"; "no dedicated actuator is required") |
| 10 (C4) | WOB 100 to 1000 N; upper bound is Borebot anchoring force | INSITU3 424-430 | MATCHES. Source also says 100 to 1000 N matches Honeybee 64 mm precedent. Lines 269-270 and envelope.md line 58 not read |
| 12 (C6) | Pass threshold >= 5 mm/min at WOB >= 100 N | INSITU3 267-268 | MATCHES |
| 13 (C7) | Density not stated; cites INSITU2 408, 834 | INSITU2 408 | Line 408 is the closure-torque sentence and says nothing on density. Absence claim not contradicted by 406-414. Line 834 and csm_sow.md not in named set: NOT CHECKED |
| 14 (C8) | Depth-series 200 cm, INSITU2 425-427; CORE_LENGTH_MM = 500 | 425-427 outside named ranges; params.py path not found | NOT CHECKED / PATH NOT FOUND |
| 74-80 | Actuator, Hall, release, back cap, stroke, torque | INSITU2 157-166, 406-414 | 74-76 MATCH. 77-78 cite 399-402, outside named range: NOT CHECKED. 79-80 MATCH for 408-411/411-414 (no linear stroke; torque curve and N=9 are Phase I outputs) |

### 2. Retired values and status tags

- Retired 20 and 50 N m: extraction line 11 names them only as the brief's retired placeholders (Brief-says column and PATCHED text). params.yaml line 37 names them only as retired. No sourced-fact use. PASS.
- params.yaml: 116 `value:` leaves, 116 `source:`, status counts DECLARED 25, ASSUMED 70, VERIFIED 11, DERIVED 10 = 116, matches foundation line 26. No other tag appears. Every leaf carries both. PASS.
- Externally sourced number lacking source: and status: none found.
- Gate facts in params.yaml: throat_open_diameter 108.585, throat_open_radius 54.2925, torque_design 10, collets.count 7, collets.spacing 2.5, core.length_capture/install/optional 500/750/1000 all DECLARED, sources cite gate B1/B4/B3/B6, none cites Mines or SBIR text as origin. PASS. throat_open_diameter source also cites double_dong_params.py line 92 for the radius value, which I could not re-read this run.
- Extraction file: seven collets, core lengths and printer are not carried there (acceptable). 10 N m carried as DECLARED. 108.585 carried with a MEASURED tag cell (fix 4).
- VERIFIED tags resting on files I could not read this run: iris.leaf_count, leaf_thickness, face_radius_core, face_radius_rock, closure_deg (double_dong_params.py, PATH NOT FOUND); drill.cutter_od_7in (borebot_operating_envelope.md, not in set). VERIFIED tags I confirmed: core.diameter_nominal (INSITU2 406-407, with conflict noted in the source string), loads.wob_min, loads.wob_max (INSITU3 424-430). The 80/20 catalog VERIFIED rows are outside my file set.

### 3. Claims citing Mines documents

| Location | Claim | Mines PDFs say | Verdict |
|---|---|---|---|
| extraction C9 (line 15) | zip contents state no core diameter, length, mass, delivery state | 260647_Just, 260648_Just, 260647_LOI_signed_flat, 260648_LOI_signed: nothing on core diameter, tolerance, length, mass or delivery state. Just.pdf mentions only "materials and supplies... low density concrete icy regolith cores" ($3,570: aggregate, low-density additives, cement, forms, testing materials). LOIs carry commitment and subcontract language only | MATCHES for the PDFs; strike "and budgets" or say XLSX unopened |
| extraction line 105 | as above plus subcontract line | as above | MATCHES |
| extraction line 98, 103 (Dreyer, properties) | csm_sow.md | not in named set; Mines PDFs do not mention Dreyer formulation or properties except LOI naming "Dr. Chris Dreyer as a Science Investigator" | NOT CHECKED against csm_sow.md |
| extraction C7 | "Mines cores are low-density concrete... density not stated" | Just.pdf "low density concrete icy regolith cores"; density not stated | MATCHES |
| params.yaml core.tol, core.density | "Mines manufacturing variation", "Mines density not stated" | PDFs state no density or tolerance | OK: tagged ASSUMED, source says not stated |
| gameplan Register row 398 and Design Notes 12 line 605, Note 8 line 564 | "Mines PDFs were not read (pdftoppm absent)" / "stay unread" | PDFs now read | STALE, contradicts the record (fix 2) |

Summary of what the Mines PDFs say about core dimensions, tolerance, length, mass, delivery state: nothing. All four carry no figure for any of them. Core dimensions rest on SBIR text (INSITU2 406-407, with the 186-188 conflict) and on the human's declarations.

### 4. Signature

**WITHHELD**

Reason: the checkable lines match, but (a) the Register still states the Mines PDFs are unread, now false; (b) one Mines-related claim overreaches to unopened XLSX; (c) the gate named `gpr\double_dong_params.py` and it did not resolve, so seven PATCHED lines and five VERIFIED params tags (leaf_count, leaf_thickness, face_radius_core, face_radius_rock, closure_deg) have no re-read this run, so I cannot sign them. The Step 0 Fact-Checker findings F-1, F-2, F-3, F-6 remain accepted from the earlier run.

### 5. Fix list (Engineer's files; I have not edited them)

1. step0_engineer_source_extraction.md line 15 (C9): change "Mines budget justifications, LOIs and budgets (the zip contents)" to "Mines budget justifications and LOIs (the four PDFs; the XLSX budgets were not opened)".
2. gameplan.md line 398 (Register row), line 564 (Note 8 last bullet), line 605 (Note 12 ASSUMED bullet): replace "Mines PDFs unread / pdftoppm absent" with "Mines PDFs read at Step 1 (pdftotext): no core dimension, tolerance, length, mass or delivery state; the report still asserts SBIR text only for core diameter". Foundation line 79 already admits these rows are out of date.
3. step0_engineer_source_extraction.md line 16 (C10): cites "lines 354, 91-96" while row 37 cites IRIS_LEAVES at 93-98. Reconcile to one range from the file.
4. step0_engineer_source_extraction.md lines 43-44: Tag cell for the 54.2925 radius / 108.585 diameter reads MEASURED or MEASURED / DECLARED. Set the tag for the radius reading and the diameter to DECLARED (the number 54.2925 sits in the source; its meaning as a radius is the human's declaration).
5. step0_engineer_source_extraction.md line 13 (C7): cite INSITU2 line 408 does not support the density statement; drop 408 or give the line that does.
6. Path to double_dong_params.py: the gate path `CC\gpr\double_dong_params.py` does not resolve. Supply the correct path (the extraction file implies `gpr\build_parts_double_dong\`) so the seven PATCHED lines and five VERIFIED params tags (iris.leaf_count, leaf_thickness, face_radius_core, face_radius_rock, closure_deg) can be re-read at lines 90-98, 354-380, 402-404. Until then, params.yaml should keep those five VERIFIED tags only with the note "Step 0 Fact-Checker read; not re-read at Step 1", or downgrade them to ASSUMED.
7. Lines marked NOT CHECKED (C3, C4 envelope line 58, C7 csm_sow, C8 425-427, rows 77-78 at 399-402, row 66 cutter OD): outside the named file set; add them to the Step 4 gate list or confirm from the Step 0 record.

## Re-check after corrections

Primary: `gpr\build_parts_double_dong\double_dong_params.py` 90-98, 352-381, 400-405; INSITU2_text.md 186-188, 218, 406-408, 829; INSITU3_text.md 424-430; both XLSX opened read-only (openpyxl); params.yaml in full; gameplan.md 390-400 and grep of "Mines"; green run file.

### 1. Previously unreadable lines and VERIFIED tags

| Item | Claim | Source | Verdict |
|---|---|---|---|
| ext line 16 (C10) | 7 in bore 177.8; lines 354-356, 92-98 | 354 `CORE_BORE_OD_MM = 177.8 # 7 inches exactly`; 92 `IRIS_CLOSED_DEG`; 93-98 `IRIS_LEAVES` | MATCHES. Range reconciled |
| ext line 38 | 3.175 mm plate, 402-404 | 402 `CORE_KERF_WIDTH_MM = 3.175 # = 74.6125 - 71.4375, i.e. 0.125 INCH exactly -- the plate thickness` | MATCHES |
| ext line 42 | Face radii 71.4375 / 74.6125, 366-368 | 368 "measured shell faces: 71.4375 core side, 74.6125 rock side" | MATCHES |
| ext line 43 | -62 deg, 54.2925 to 0.0000, line 92 | 92 `-62.0 # aperture 54.2925 -> 0.0000 mm` | MATCHES. Radius reading is the human's (gate B1), tagged DECLARED. Split tag acceptable |
| ext line 44 | 54.2925 at line 92 | same | MATCHES |
| ext line 47 | 106.369 head tip to sphere centre, 372-380; pole 34.9315 | 372 `CORE_IRIS_STANDOFF_MM = 106.369`; 373-378 "head tip z -789.1834 ... sphere centre z -682.8144 ... pinched off INSIDE the head"; 379-380 `500 + 106.369 - 71.4375` | MATCHES; 106.369 - 71.4375 = 34.9315 |
| ext line 66 | 177.80 cutter; 106.369 carried by ASSUMED | 354 supports 177.8 as the 7 in bore the drill cuts; `borebot_operating_envelope.md` not in set | Bore MATCHES. "Cutter OD" wording rests on a file outside the set; ASSUMED label on the carry-over is correct |

VERIFIED params tags:

| Leaf | Value | Source line | Verdict |
|---|---|---|---|
| iris.leaf_count | 4 | 93-98, four census entries 1041-1044 | CONFIRMED |
| iris.leaf_thickness | 3.175 | 402-404 | CONFIRMED |
| iris.face_radius_core | 71.4375 | 360 `CORE_KERF_SPHERE_R_MM = 71.4375`; 368 | CONFIRMED |
| iris.face_radius_rock | 74.6125 | 368 | CONFIRMED |
| iris.closure_deg | -62 | 92 | CONFIRMED |

Gate fact: throat_open_radius 54.2925 DECLARED, throat_open_diameter 108.585 DERIVED from it. Accepted, not a withhold reason.

### 2. Corrected cites

- C7 (ext line 13): cites csm_sow.md 24 and INSITU2 218, 829; line 408 dropped. INSITU2 218 "low-density concrete formulation", 829 "low-density concrete simulant in two forms". No density value in either. MATCHES. csm_sow.md 24 not in set (carried from earlier run).
- C10 (ext line 16): MATCHES (above).
- C9 (ext line 15): 186-188 caption "Core diameter is above 100 mm" and 406-407 "pre-cast to 100 mm diameter to match the iris aperture" confirmed. XLSX claim: 260647_Budg.xlsx and 260648_Budg.xlsx each 3 sheets, 491 text cells; whole-word search for core, diameter, length, tolerance, mm, inch, mass, kg, cm returned zero hits in both. MATCHES the stated search terms and counts. ("delivery state" was not a search term; it is covered by the PDF read and zero hits on the terms above.)
- gameplan.md 398, 564, 605: each now says PDFs read (pdftotext) and XLSX opened (openpyxl), no core dimension, tolerance, length, mass or delivery state; report asserts SBIR text only. MATCHES the record.

Advisory, not a withhold reason (outside the three edited statements, and not in my fix list): stale statements remain in gameplan.md. Line 60 ("Mines documents were not read in full (PDF render unavailable)") and line 706 ("Mines PDFs unread (pdftoppm missing)") now contradict lines 398, 564, 605. Line 103 is the dated Step 0 environment-check instruction and is historical. Recommend updating 60 and 706 to the Step 1 wording.

### 3. Edited params leaves

| Leaf | Value | Check | Verdict |
|---|---|---|---|
| collets.envelope_max | 106.585 DERIVED | 108.585 - 1.0 (core.tol) - 1.0 (min_throat_slack) = 106.585; both inputs tagged ASSUMED, throat DERIVED/DECLARED chain | CORRECT; source string states formula |
| icd.keepout_radius | 86.2 DERIVED | 152.4/2 + 10 = 86.2 = drill.r_face | CORRECT |
| stop.height_z | 160 DERIVED | nut_top_z 150 + g_stop 10 = 160; labelled PLACEHOLDER, no test asserts it, Step 12 fixes it | CORRECT and honest; DERIVED from ASSUMED inputs |
| (follow-ons) stop.start_z 660, icd.stop_height 160, core.min_exposed 121.369 | | 160+500; equals height_z; 106.369+10+5 | CORRECT arithmetic |

Tag census recomputed from params.yaml: ASSUMED 69, DECLARED 23, DERIVED 15, VERIFIED 11, total 118. Matches the green run (28 passed; P2 counts identical). No other tag. Gate facts still DECLARED.

### 4. Signature

**SIGNED**

All seven previously unreadable PATCHED lines and the five VERIFIED tags match the source at the cited lines. C7, C9, C10, the three gameplan statements and the three edited leaves check out. Open items carried, none blocking: stale gameplan.md lines 60 and 706 (advisory above); lines marked NOT CHECKED in section 1 of the earlier run that rest on files outside my set (C3 motor summary, C4 envelope line 58, C8 INSITU2 425-427, rows 77-78 at 399-402, csm_sow.md 24, borebot_operating_envelope.md for cutter_od_7in) stay on the Step 4 gate list.
