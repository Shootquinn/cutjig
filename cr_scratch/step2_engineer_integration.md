## 1. Evidence

| Item | Result |
|---|---|
| Red run (new tests, before any data) | cr_scratch/step2_integration_red_run.txt: 10 failed, 55 passed |
| Green run | cr_scratch/step2_integration_green_run.txt: `python -m pytest tests/test_params_bom.py -q` = 65 passed in 3.05 s |
| FreeCAD runs | none this step; no geometry created; nothing over 30 s |
| Regenerated | report_assumptions.md, bom_stock_allocation.md, bom_purchased.md via `python build_parts/bom_tools.py` (counts: DECLARED 22, ASSUMED 94, VERIFIED 34, DERIVED 43, total 193) |

New tests (tests/test_params_bom.py, group P10). Each is able to fail on a wrong value.

| Test | Asserts |
|---|---|
| P10_icd_frozen_keys_exist_with_source_and_status | 41 frozen keys exist, each has a source, a legal status and the concept's value |
| P10_every_key_in_concept_icd_table_exists | parses the backticked keys out of the concept's ICD table (the "was" key excluded) and requires every one in params.yaml |
| P10_coaxiality_chain_sums_inside_budget | chain 0.953 is at most 1.0; a wrong entry (0.5) breaks the budget |
| P10_working_stroke_per_core_class | start_z minus stop height is at most 500 for 0.5 m and 0.75 m; park above the working range (P6c, P6d precursor) |
| P10_stop_ownership_upper_assembly | `stop.owner` upper assembly; `upper.metal_stop` present; `stop.hard_stop_gap` and `stop.nut_top_z` absent; no stop key under base, receiver, holder, collet, nut, washer, wingnut, collar (stroke-gap keys exempt); ASSEMBLY.md carries the hard-stop sentence |
| P10_assembly_load_loop_ten_members | the ten members appear in order inside the Load path section, "(ten members)", receiver underside force 0, "holder stroke gap", no PLACEHOLDER, poses R / K d+1 / K-max, and every part pair is listed exactly once (n(n-1)/2) |
| P10_height_soft_recorded_reported_untested | 2000 DECLARED, soft flag, "Soft target ... not tested" line in report_assumptions.md; heights 3000 and 1500 pass validate_params, check_icd and check_throat_rule |
| P10_P8_against_final_throat | final radius 54.2925; slack per side 1.2925 / 3.7925 / 8.7925 at 105 / 100 / 90 (each with tol 1.0), 0.50 at 106.585; radius 52.9 fires on d = 105 |
| P10_envelope_request_refused_above_cap | 107.0 refused with "change `iris.throat_open_radius`"; 106.585 accepted; radius 55.0 admits 107.0 |
| P10_bracket_rule_superseded | `hardware.bracket_leg_min` 57 DECLARED; SKU is not 30-4332; alt key gone |

Code added to build_parts/common.py: `throat_slack_per_side`, `check_envelope_request`; REQUIRED_KEYS now `stop.collar_top_z`; ICD_FIELDS extended to the frozen keys, so P6 now fails on any blank frozen key.

## 2. ASSEMBLY.md

Rewritten (header "Step 2 integration"). Written exactly as the concept states: the ten-member sentence, ring as holder stop, rim gap never loaded, hard-stop sentence (verbatim in the Load path section); poses R, K d+1, K-max; datum A/B/C text; ICD pointer paragraph. Relation table: washer added as a tenth part (45 pairs, all listed: R pose C 8, G 12, F 25; K pose C 10, G 10, F 25), and a Feature pairs table for the pairs that differ by pose (ring top, rim, floor, plate-collar, skirt, collar to cutter). Deliberate edits to existing rows:

| Row | Was | Now |
|---|---|---|
| base / holder | G 3.0, "never bottoms" | G 1.5 (rim gap minimum at K-max; floor gap 2.00); 3.0 contradicted the 2.00 floor gap |
| holder / nut | G, C, 0.5 (K clamp face bears on holder flange) | C, G, 0.75 (R plate top on collar underside; K gap = lift play); the clamp face now bears on the washer |
| nut / cutter | g_min 10 from nut top | 10 from collar top, wings included |

## 3. params.yaml

Added with source (the Step 2 file) and status: all concept lines (thread.major 149.58, wingnut.body_od 166.28, holder.flange_od 144.08, holder.length 88.0, receiver.rim_above_floor 88.5, nut.lift_play 0.75, stroke gaps, collar, washer, core.min_exposed 128.12, core.mass_kg_d105, loads, upper.*, icd.*, column, hoist, strap, rest); Loftsman values (cone.alpha 10 with alpha_release marked RETIRED, thread minor, hand right, nut.length 48, seat holder_bottom_R 13.626 and contact_height_Kmax 30.0, register g_reg 0.25 and tilt limit 1.021, collet grip window -1.5 / +1.0, clamped slit 0.584, 12 slits at 1.5); park 950 and park_stroke 780 kept separate from travel_max 500; stop.g_stop reworded to the collar top; collar_top_z 150 replaces nut_top_z; height_range [160, 300]; start_z now the list [660, 800]; detents [310, 560]; bracket_leg_min 57 DECLARED; bracket_sku 8020-14089 ASSUMED, 30-4332 and 30-4302 recorded as superseded; purchased and printed bracket joints 4 and 4. Deleted: stop.hard_stop_gap, stop.nut_top_z, hardware.bracket_sku_alt. Jack-hole keys never existed in params, nothing to delete.

## 4. Problems found

1. Key name conflict. The concept names `washer.material`. The Step 1 gate B2 filter (`_PRINTER_KEY`) rejects any key named `material`. I did not weaken the gate. Key is `washer.type` (PTFE, ASSUMED) with the rename in its source. Manager: confirm, or rule that the filter takes a path-qualified exemption.
2. Bracket SKU 8020-14089 is named in the concept but its page was not read; ASSUMED, verify at purchase. The 68 mm printed bracket was taken from the concept, not re-read from the human's file; ASSUMED.
3. Bracket purchase count falls from 16 to 8 (four outer corners, two each); the four plate-support ends take printed brackets. T-nuts and screws still count all 16 brackets (44 T-nuts, unchanged). Printed bracket T-nut use is an assumption.
4. Washer is a new tenth part: its signed feature (a radial tab notch) is my seed; the Topologist should confirm or replace it. Its pair gaps (0.5, 1.0) are seeds.
5. stop.height_z stays 160 (collar top 150 + 10) as the concept's seed. The concept's own open flag says A2b will compute about 170 at floor 40. Step 3 fixes it; nothing tests the 160.
6. The concept's recurring phrase "poses R, K d+1, K-max" implied a third pose that Step 1 never had. Defined in ASSEMBLY.md as above; K-max core is d - 1.5.
7. Concept ICD row "Mass" and statements of 10 N m, 12 N m: `loads.nut_torque` 12 is ASSUMED, separate from the DECLARED 10 N m design torque.
8. Not done, outside this directive: W-1 coverage and slit law in the generator, `stop.nut_top_z_min/_max` (absorbed at Step 3 or 5), `loads.nut_torque_abuse`.

## 5. Gameplan versus directives (the Manager applies at close; gameplan.md not edited)

Line numbers are gameplan.md as read today.

| # | File and line | Stale text | Corrected text |
|---|---|---|---|
| 1 | gameplan.md 74 (Steps table, Step 2) | "force loop, release, three load cases, tolerance budget, interface control table, family spacing, stop ownership" | "force loop (ten members, foot ring is the holder stop), release (10 deg captured-flange nut, collar back-off lift), load cases, tolerance budget and datum scheme, frozen ICD, family and 106.585 mm cap, stop ownership (upper assembly) and holder stroke gap, stability and handling. Nine decisions." Status: Done at close |
| 2 | 110 (Detail 2 item 2) | "captured-flange nut with a modest cone, or releasing cone ...; jacking provision regardless" | "Captured-flange nut, cone half-angle 10 deg. The releasing cone (20 deg) is retired. Jacking holes are deleted; the jacking provision is the collar back-off lift (281.5 N at 12 N m against a release need of 46, 88, 128 N)." |
| 3 | 111 (item 3) | "9.4 kg at 0.5 m, about 14 kg at the 0.75 m ..., about 19 to 21 kg at an optional 1 m"; "no further safety factor" is correct and stays | "10.4 kg at 0.5 m, 15.6 kg at 0.75 m, 20.8 kg at 1 m (d = 105, 2400 kg/m3)"; add "lateral 100 N at 106.4 mm or more above the holder = 10.6 N m; cutter descent 1000 N via cutter, carriage, metal stop, columns, frame" |
| 4 | 112 (item 4) | "thrust washer pocket" among optional responses | "PTFE washer always fitted (ID 136.8, OD 143.2, 1.3 mm); predicted 15.47 N m at d = 105 and 13.26 at d = 90 at 12 N m nut torque; plain printed washer 10.65 and 9.13 (misses 10 N m at d = 90 by 8.7 percent, no margin claimed)" |
| 5 | 113 (item 5) | "slack is about 1.3 mm per side"; datum text "core axis located by the cone and pilot" | keep the 1.3 (it is 1.29 at 105 plus tolerance); add "datum B is the receiver register bore axis, located through two plate keys and a plate stop pin; chain 0.32 + 0.20 + 0.283 + 0.15 = 0.953 against 1.0; slack 3.79 at 100 mm and 8.79 at 90 mm" |
| 6 | 116 (item 8) | "Hard stop ownership: not the printed nut." | "Hard stop: the metal descent stop, owned by the upper assembly, 1000 N. The holder stroke gap (flange to rim, 1.5 mm minimum in K) is a separate, never-loaded base-side gap." |
| 7 | 125 (Step 3 Work, Loftsman) | "seed 165 mm at 20 degree cone, reviewers' range 135 to 165 mm"; "confirm or replace the 54 mm figure" | "major 149.58 mm (closed form, 10 deg cone); register closed at holder length 88.0, lift play 0.75, g_reg 0.25". The 54 mm figure is withdrawn (fails T9 at 2.477 deg) |
| 8 | 139 (Detail 5 family) | "default 85 to 110 mm, ASSUMED" | "85 to min(110, throat - tol - slack) = 85.0 to 106.585 mm; a request above is refused with 'change `iris.throat_open_radius`'" |
| 9 | 147 (Detail 3 holder list) | "bearing recess for thrust washer, key, jacking holes, hard-stop face" | "cone, flange, key, collar; no jacking holes; no hard-stop face (the foot ring top is the holder stop, the rim gap is never loaded)" |
| 10 | 153 (Detail 3 stop) | stop shown at the descent assembly | no change in meaning; add "owner upper assembly, `upper.metal_stop`" |
| 11 | 180 (Step 12 item 5) | "jam release (jacking holes)" | "jam release (collar back-off lift); manual raise with 300 N shear link; park latch" |
| 12 | 199 (H3) | "Side load at core top (10 N PROPOSED)" | "21.2 N at the top of a 0.5 m core (100 N at 106 mm), loading the holder to 10.6 N m" |
| 13 | 201 (H5) | "with and without jacking holes"; "Release without tools beyond the jacking provision" | "Collet frees by nut back-off lift, tool-free, cold user; minimum lift ratio 2.20" |
| 14 | 204 (H8) | "Gap nut top to template stop plane" | "Stop gap trial: collar top (wings included) to cutter lowest point at the stop, at least 10 mm; funnel seating force through the collet not above the H3 lateral load" |
| 15 | 193 (Step 8 prediction text) | "Loftsman estimate 6.9 to 8.1 N m torque-to-slip at 12 N m nut torque" | "Loftsman 10.65 / 9.13 N m plain and 15.47 / 13.26 N m PTFE (d = 105 / 90); spread at d = 90: plain 3.8 to 23.1, PTFE 5.8 to 31.0" |
| 16 | 220 (Step 12 agenda) | no steady-rest detents, park, strap | add: "bolt-down operating condition (115 N per bolt), steady rest at every core length (detents 310 and 560), choke strap with 250 mm side handle, park 950 with latch, hoist and cross member (joints 8 to 10)" |
| 17 | 298 (P4) | "every bracket is a SKU or full-size 30-series class" | add "leg at least 57 mm; 30-4332 (30 mm legs) superseded". Test spec: add the P10 tests as P6 (frozen keys), P6c/P6d precursor, P8 slack numbers |
| 18 | 300 (P6) | "datums A, B, C, ... no empty field" | add "every key in the concept ICD table exists (test P10), ICD fields include floor_above_datum_a, coaxiality_chain, U12 to U16 keys; P6a is a document check outside Rule M" |
| 19 | 302 (P8) | "seed 108.585 mm" | no stale value; add "slack per side 1.29 / 3.79 / 8.79 mm at 105 / 100 / 90; request above 106.585 refused" |
| 20 | 343 (F4) | "Core top above the nut top ... by at least `core.min_exposed` = standoff + g_stop + margin" | "above the plate top by at least 128.12 = 106.369 + 10 + 5 + collar top 6.75" |
| 21 | 345 (F6) | "Hard-stop gap | Holder flange to receiver rim gap in K equals z0 + s_z + margin (about 6 mm seed); holder never bottoms" | "Holder stroke gap: flange to rim 13.126 (R), 8.59 (K d+1), 1.5 (K-max); key `holder.stroke_gap_*`; holder bottom to ring top 11.626 / 7.089 / 0.00; class C at K-max only" |
| 22 | 351 (A1) | "Required G pairs include base-holder, nut-collet, nut-core, nut-cutter"; matrix of 8 parts | add washer as a part (10 parts, 45 pairs); add the Feature pairs table (ring top, rim, floor, plate-collar, skirt). Pair count line "36" is stale: 45 (R: C 8, G 12, F 25) |
| 23 | 352 (A2) | "gap g_stop between nut top (wing tops included) and the cutter lowest point" | "between collar top (wings included) and the cutter lowest point, at the highest clamped nut position; keep-out radius 86.2" |
| 24 | 353 (A3) | "nut clamp face bears on holder flange face (... travel > 0 in R)"; "holder never bottoms" | "nut clamp shoulder bears on the washer, which bears on the flange; holder bottom above the receiver floor in every pose (A3e); skirt at least 1 pitch above floor (A3h); engaged length at least 24 mm (A3i); the holder stops on the ring top at K-max" |
| 25 | 334 (T9) | "Register geometry from Step 3" | "register g_reg 0.25, tilt line 1.021 deg, total 0.903 deg at first thread contact; L_h = 88.0, p = 0.75" |
| 26 | 484-493 (Design Notes 2) | "F4 measures from the nut top"; "A2 asserts the gap g_stop between nut top" | "from the collar top" (same two statements); "stop in the ICD (height, rated load, owner)" is now frozen |
| 27 | 505, 514-517 (Design Notes 3 table and ruling) | "about 165 mm major, nut body about 181 mm"; "two M6 jacking holes on the holder flange are required either way" | "149.58 mm major, 166.28 nut OD; no jacking holes (flange annulus 5.00 mm against 7.4 required); releasing cone retired" |
| 28 | 521 (Design Notes 3 register) | "needs about 54 mm or more" | "register closed at L_h 88.0 (the Topologist's 80 passes by 0.003 deg only at g_reg 0.2513 or tighter)" |
| 29 | 529-538 (Design Notes 5 ICD table) | Datum A, B, C rows; "Keep-out ... from nut top to stroke end"; "Stop ... owner (Step 12)"; "Core handling | Steady rest or cradle and lift strap point on the frame" | Datum B receiver register bore axis; C slot line with two plate keys and a stop pin; A with floor 40 mm; keep-out 86.2 from collar top; stop owner upper assembly, gap 10 from collar top; core handling: steady rest at every length with detents, choke strap with 250 mm side handle, no overhead anchor |
| 30 | 554 (Design Notes bracket line) | "ordered catalog brackets must be full size ... BOM names the SKU or full-size class" | add "leg at least 57 mm and width 57 mm; 30-4332 (30 mm legs) superseded; eight joints: four outer corners 57 mm class two per joint, four plate-support ends the 68 mm printed bracket" |
| 31 | 557 (Design Notes tip-over) | "final tip-over number at Step 12" | tip-over numbers fixed at Step 2: 23.8 deg static tilt, 158 N at the centre of mass, 68 N at the column top; bolt-down with cutter above z = 400 mm; Step 12 replaces |
| 32 | 570 (Design Notes holding) | "about 8.1 N m at d = 105 and 6.9 at d = 90 ... (about 250 N axial ... at a 165 mm thread)" | "10.65 / 9.13 plain, 15.47 / 13.26 PTFE; about 267 N plain, 388 N PTFE axial at 149.58 mm" |
| 33 | 622 (Progress-log param keys) | "`stop.height_z` 160 is a placeholder DERIVED value that Step 12 fixes" | "fixed per core class by A2b at Step 3; keys: `stop.collar_top_z` (was `nut_top_z`), `stop.height_range`, `stop.start_z` list; `stop.hard_stop_gap` deleted, use `holder.stroke_gap_*`" |
| 34 | 647 (Echo Site Registry, thread) | "major diameter = Step 3 output (reviewers' range 135 to 165 mm; no single number until Step 3)" | "major **149.58 mm** DERIVED (`thread.major`), minor 144.58; right-hand, single start, 45/45, pitch 8" |
| 35 | 648 (Echo, cone) | "seeds about 10 degrees with captured nut, or 20 degrees releasing" | "half-angle **10 degrees** (`cone.alpha`); 20 degrees retired" |
| 36 | 649 (Echo, slits) | "params.yaml `collet.slits`"; "20 at 5 mm"; "min clamped slit 0.5 mm (PROPOSED)" | "`collet.slit_count` 12, `collet.slit_width_seed` 1.5; clamped slit 0.584; grip window d - 1.5 to d + 1.0" (key `collet.slits` does not exist) |
| 37 | 650 (Echo, engagement) | "params.yaml `thread.min_engage`" | key is `thread.min_engage_pitches` (existing mismatch); engaged length at least 24 mm in every pose (A3i) |
| 38 | 651 (Echo, nut OD) | "seeds about 181 mm body, about 230 mm span" | "nut OD **166.28 mm** DERIVED; span 230 mm ASSUMED (parameter)" |
| 39 | 652 (Echo, hard stop) | "Hard stop: metal, owner and height in the ICD (Step 12); the printed nut is not a stop" | "Hard stop: metal descent stop, owner upper assembly (`upper.metal_stop`), 1000 N; stop gap `stop.g_stop` 10 from collar top; holder stroke gap is a separate, never-loaded gap" |
| 40 | 655-656 (Echo, loads and holding) | "Holding torque estimate about 7 to 10 N m at hand-tight" | "10.65 / 9.13 N m plain, 15.47 / 13.26 N m PTFE at 12 N m nut torque (d = 105 / 90); PREDICTED, ASSUMED inputs" |
| 41 | 658 (Echo, core length row); also 393 (register row, same text) | "mass about 9.4 kg at 0.5 m (DERIVED); upper assembly travel at most 0.5 m; jig height 2 m soft" | "10.4 kg at 0.5 m; 15.6 and 20.8 at 0.75 and 1 m; travel at most 0.5 m is the working stroke, park 950 mm is separate; 2 m soft, recorded and reported, not tested; captured length 465.07 mm for a 500 mm core" |
| 42 | 647 and 622 region (Echo, missing rows) | none | add Echo rows: lateral 100 N and 10.6 N m; H3 21.2 N; washer ID/OD/thickness; floor 40 mm above datum A; coaxiality chain 0.953; collar OD/ID/top 152.4 / 114.0 / 6.75; steady-rest detents 310 / 560; strap 80 kg and 250 mm handle; park 950 and 300 N fuse; bracket leg minimum 57 mm |
| 43 | 101 (Step 1 Work text) and 598 (B5) | "(full-size 30-series, no 'mini')" in a Step 1 record | no change to the record; note that `bracket_sku` 30-4332 is superseded for new work. Do not add the word "mini" to ASSEMBLY.md, params.yaml or the BOM files (P4 greps for it) |
| 44 | Progress Log (line 465 onward) | Step 1 test count of 55 | Step 2 integration: 65 tests pass (55 plus 10 P10) |
| 45 | 661 (Echo, report test count "about 90 (91)") | 91 | the P-group grew by 10 tests; recount at Step 13 |

Left for the Manager: "Step 2 status Not started" in the Steps table (line 74) is the only status cell to change.
