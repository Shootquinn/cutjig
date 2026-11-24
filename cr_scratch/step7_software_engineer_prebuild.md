## Mismatches and revisions

| Item | Test | Definition | Resolution | Reason |
|---|---|---|---|---|
| A3b fits | one green_at_7 test, four fits | key/pin 0.250 and spigot 0.200 at 7; foot and guide at 12 | split: test_A3b_..._key_pin_and_spigot green_at_7; test_A3b_..._column_foot_and_carriage_guide green_at_12 | ruling 1; base keeps receiver and plate as two solids |
| fit_spigot_hole | probe listed absent | r 80.2 plate-hole face minus r 80.0 receiver face | probe reads the two coaxial Z cylinders of base | ruling 1 |
| fit_plate_key_stop_pin | probe listed absent | max((12.0 - base.key_width) / 2, pin gap) | stays ABSENT FEATURE naming base.key_width, pin_dia, pin_x | params keys not yet added |
| slit_width_clamped_min | odd slits sampled at absolute z 5.0 | ZMin + 5.0 | probe uses collet ZMin + 5.0 | K4; a collet at z 40 read 0.0 |
| nut plate top / holder collar underside | holder top minus nut top | zhi(holder) - collar.thickness | probe subtracts G(collar.thickness); absent without the key | K4; fused collar made the gap read the collar top |
| FR2 / FR3 | 8 + 8 brackets, joints = 16 / per_joint | 12 brackets, 96 T-nuts | printed count = printed joints x hardware.printed_brackets_per_joint (4); total 12; T-nuts 96; joints = purchased + printed joints = 8 | ruling 3 (option a provisional) |
| G4 counts | 6 / 16 / 128; 16 brackets; 128 T-nuts | 6 / 12 / 96 | derived from params through _counts(), asserts 12 and 96 | ruling 3 |
| Params keys | no entry | hardware.printed_brackets_per_joint, collar.thickness | added to PARAM_GAPS (Step 7) so P7 accepts them until params carries them | P7 audit |

## Contract and coverage check

| Definition row | Test | Match |
|---|---|---|
| L1 ledger, phi, dz, screw motion | G5 ledger, A3e, A3h, A3i, T4 | yes |
| L2 core, L3 cutter | A3c, A3d, A3f, A3g, G1 bore | yes |
| L4 frame T(0,0,-0.005) | G5 fixed parts, A6a, A1a | yes |
| L5 C6 | FR2/FR3, G4 x2 | yes, ruling 3 |
| L6 measures | G1 x10, A3c to A3g, A6a, P6b, T5 | yes; fit_plate_key_stop_pin open |
| L7 WS1 to WS11 | G2 x11, A6 x9, A6a to A6c, G3 | yes |
| L8 clamp range | T5 x4, G7 slit width | yes |

Pending ASSEMBLY.md rows (Systems Engineer review; no threshold edited):

| Row | Tests that read it |
|---|---|
| base\|holder g_min 0.12 | A1a x21 (R, Kd1, Kmax), G6 x7, G3, G2 WS2/WS8/WS10 (A1) |
| holder\|collet R 0.29 | A1a x21, G6, G3, G2 WS2 and WS1 (F1) |
| holder\|nut K 0.50 | A1a x21, G6, G3 |
| nut\|washer class P, 2.45 mm3 | A1a x21, G6, G3, WS3 (A1 min_dist) |
| collar top\|cutter R class F | F6 x3, A4 x3, A2b via feature gaps, G6 |

All read the table through gates.parse_assembly, so the row edits land without test changes; class P needs a gates.py class branch (Engineer, at the edit).

## Counts

| | Before | After |
|---|---|---|
| collected | 656 | 657 |
| pass | 421 | 420 |
| fail | 235 | 237 |
| green_at_7 | 185 red | 185 red |
| green_at_12 | 18 | 19 |

The two added failures: FR2/FR3 (MISSING: params key hardware.printed_brackets_per_joint) and the new A3b green_at_12 test. All 237 failures carry MISSING: or ABSENT FEATURE: (474 matching lines).

## Revision 1 test edits

| Item | Edit | File |
|---|---|---|
| 1 contact area | probe contact_area sums the common-face intersection area (fallback: smaller face on boolean error). New test: holder\|nut R contact at most 3,698 mm2 (annulus); 9,978 is the bad control | probe_poses.py, test_assembly.py |
| 2 stop travel | nut_travel_left_mm replaced by nut_stop_travel_mm (screw-motion descent, 0.25 mm steps, bisect to 0.01, first common volume 0.01 mm3). T5 and G1 read it at 8.0 (thread.pitch). New test: Kmax 10.01; relief-filled control about 4.0 fails | probe_poses.py, test_thread_clamp.py, test_step7_assembly.py |
| 3 rows | gates.py owns the parser (the Engineer prompt lists no gates.py or test work): class P (min_dist 0 +-0.01, overlap in nut.pad_overlap_min..max; absent keys give MISSING:), per-pose minima ("at least 0 / 25 / 25" parses to a list; min_for_pose).  New test_A1_contract_rows_revision_1 (row 3 g_min within 0.011 of washer.thickness - nut.washer_pocket_depth; row 4 P; row 5 minima) is red until ASSEMBLY.md carries the rows. Invariant control covers both | gates.py, test_assembly.py, test_step7_assembly.py |

## Tests whose numbers move with the holder and nut rebuild

| Test | Quantity | Action |
|---|---|---|
| test_step6_parts HD6 (line 254) and control (line 429) | holder down_planar_z gains the collar underside at z_top | add bbox zmax - collar.thickness to allowed; edit after measured values |
| test_step6_parts line 168 (holder, nut) and test_assembly line 422 | probe Euler/volume against result JSON | self-consistent; pass once step3_parts and step6_parts JSON refresh (holder Euler 8 to 14, nut 10 to 11; volumes 459,449 and 352,474) |
| BOM mass rows | holder +51,600 mm3, nut -6,364 mm3 | no test pins a holder or nut mass; Engineer's BOM refresh |
| G7, T4, A3h, A3i | nut zone unchanged (engaged 25.705 / 31.401 / 38.490) | none |

Counts after edits: 662 collected; green_at_7 188. Every failure is MISSING: or ABSENT FEATURE:; step6_parts.json is older than the rebuilt parts_cache, and a probe refresh restores those.
