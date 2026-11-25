# Step 1.0 Wave 1a: question batch 1 and Q3-0

Batch 1 has 17 rows (Q2a to Q2e, Q9, DN23-a to DN23-e, N5 to N10). Q3-0 is red on the empty batch, green on Z, fires on B, green on the batch. Files under research/sean/cr_scratch/: step3_check.py, step3_fixtures/ (3 files), step1_quinn_batch1.md, step3_check_q30_results.json.

## Corrections to the brief

1. Q2 scope. Gameplan line 158 lists four Q2 items (length, mass, top-end hardware, cutter OD). Open Questions line 554 and the brief list five (adds bore ceiling). The batch carries five, Q2a to Q2e.
2. `drill.bore_ceiling_z` (gameplan line 121) names a z, but the ceiling rides with the drill and changes with pose. The pose-invariant quantity is the offset above the cutter tip. Q2e asks for the offset. Recommend the overlay leaf `drill.bore_ceiling_above_tip` (800 mm, ASSUMED) with z per pose computed in check_stack.py. The Wave 1b harness spawn should carry this ruling.
3. params `upper.park_lock` (line 38) says "above start_z 800"; `stop.start_z` is [834.84, 965] DERIVED (params `upper.travel_max` source, line 32). Stale text in a shared file. Feeds N7 and 4a; not a batch row.
4. Critical-path section 8 calls `stop.collar_top_z` 159.84 "collar top above floor". tests/test_params_bom.py 700-702 make it a datum-A value (Manager open F1). Row N10 carries the shop-floor offset.
5. Q9 stand-in omits the 1000 mm core from the drawing. `core.length_optional` 1000 is DECLARED as optional (gate B6). Quinn's answer to Q9 rules.
6. Q3-0 rule. The brief reads "a stand-in without the word ASSUMED or a status tag". Implemented per gameplan line 158 ("an ASSUMED stand-in"): the stand-in must contain the word ASSUMED. A stand-in tagged only DERIVED or DECLARED fails. N10 carries both (DERIVED arithmetic, ASSUMED no-feet premise).

## Q3-0 results

| Run | File | Expected | Observed | Reason | Match |
|---|---|---|---|---|---|
| Red-first | step3_fixtures/q30_empty.md | FAIL | FAIL, exit 1 | table has no rows | yes |
| Z | step3_fixtures/q30_z_complete.md | PASS | PASS, exit 0 | 3 rows clean | yes |
| B | step3_fixtures/q30_b_blank_standin.md | FAIL | FAIL, exit 1 | line 6 row B2: blank standin (one failure, the planted row only) | yes |
| Batch | step1_quinn_batch1.md | PASS | PASS, exit 0 | 17 rows clean | yes |

All MEASURED 2026-11-24; timestamps per run in step3_check_q30_results.json. Order run: empty, Z, B, then the batch written and run.

Script: `step3_check.py --batch <path> [--json <out>]`. Columns located by header (ID, Question, Feeds, header containing "ASSUMED" or starting "Value used"). Fails on: no matching table, no rows, blank ID, question, feeds or stand-in, stand-in without ASSUMED. `--table` (Q3-1) is a separate function `check_q31` and CLI branch, exit 2 until Step 3; Q3-0 code is untouched by it.

## Stand-ins: seed list for the overlay

| Row | Proposed overlay leaf | Value | Status | Source |
|---|---|---|---|---|
| Q2a | `drill.length` | 800 mm | ASSUMED | [CP §3.2, 18:20] |
| Q2b | `drill.mass` | 8 kg | ASSUMED | no source; tube alone 3.215 kg DERIVED (pi/4 x (152.4^2 - 146.05^2) x 800 mm^3 x 2700 kg/m3; tube_od, tube_id ASSUMED in params; aluminium ASSUMED from [CP §12, 09:05]) |
| Q2c | `drill.top_block_length`, `drill.top_block_od`, `drill.top_block_mass` | 150 mm, 152.4 mm, 2 kg | ASSUMED | no source; OD = params `drill.tube_od` 152.4 ASSUMED |
| Q2d | `drill.head_od` | 177.8 mm | ASSUMED | params `drill.cutter_od_7in` (VERIFIED for the 7 in generation), upper bound; label "cutter OD ASSUMED" |
| Q2d | `drill.head_length` | 106.369 mm | ASSUMED | params `drill.kerf_standoff` (ASSUMED) |
| Q2e | `drill.bore_ceiling_above_tip` (correction 2) | 800 mm | ASSUMED | DERIVED from `drill.length`, open bore |
| Q9 | spec input, no leaf | 500 and 750 mm drawn; 1000 mm not drawn | ASSUMED | params `core.length_capture`, `core.length_install` DECLARED; gameplan Open Questions Q9 |
| DN23-a | `liftmotor.count` | 3 | ASSUMED | [DN23] |
| DN23-b | `pinion.gearbox_ratio` | 1 (direct drive) | ASSUMED | [DN23] |
| DN23-c | `drill.rpm` | 60 rpm | ASSUMED | no source |
| DN23-c | `drill.torque_target` | 10 N m | ASSUMED | cap at params `loads.torque_design` DECLARED |
| DN23-d | `gear.pitch_diameter` | 250 mm | ASSUMED | no source |
| DN23-d | `gear.bore` | 180 mm | ASSUMED | above 2 x `icd.keepout_radius` 86.2 = 172.4 mm DERIVED |
| DN23-e | ruling, no leaf | iris off the same ring gear drivetrain; S6 callout | ASSUMED | [DN23] |
| N5 | ruling, no leaf | kept base parts accept 1000 N, no rating check; S3 reports per-part force | ASSUMED | params `loads.wob_max` 1000 N VERIFIED; gameplan Design Notes 16 |
| N6 | ruling, no leaf | core lowered out of the drill bottom by hand, upright, iris open, drill at park | ASSUMED | tied to DN23-e |
| N7 | ruling, no leaf | B5 metal stop kept, 1000 N axial; power-off hold a separate Step 2 device | ASSUMED | params `upper.metal_stop` DECLARED |
| N8 | ruling, no leaf | ASSEMBLY.md (or shared ICD under docs/) becomes ICD authority; no edit until Quinn rules | ASSUMED | gameplan detail 4a line 391 |
| N9 | ruling, no leaf | test_P10_every_key_in_concept_icd_table_exists REWRITE to read the N8 source | ASSUMED | gameplan detail 4a line 391 |
| N10 | `jig.datum_a_above_floor` | 60 mm | ASSUMED | DERIVED from params `profile.height` 60 VERIFIED, no feet |

Numbers with no source (8 kg, 150 mm, 2 kg, 60 rpm, 250 mm) are working values for drawing and arithmetic only. Each is a row Quinn or Sean answers.

## Open items

- Sean: approve or strike N10 at the batch gate; rule on correction 2 (bore ceiling as an offset) before Wave 1b.
- Owner column follows Manager ruling F4: DN23-a, DN23-d, N7 owned by Sean, worded as input requested from Quinn.
