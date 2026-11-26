# Step 1.3 step 0 check (P0L), The Loftsman

Date 2026-11-26. Inputs: `research/sean/cr_scratch/step1.3_engineer_step0.md` sections 3, 6, 7, 8; `docs/sketches/proposed_params.yaml` (expr fields), `check_stack.py` (`global_vars`, `eval_expr`), `sketch_common.py` (`k2`, `expr_agreement_issues`, `plane_agreement_issues`, `_k7` side swept branch l.2106-2173, plan swept branch l.2314-2374), `s1_spec.yaml`, `s2_spec.yaml` (stack_ties, frame_upper, jackscrew, guide, anchor, guide_tie rows), `fixtures/manifest.yaml`, `fixtures/builders.py` (k2_b4, k2_b5, k6_b10, k6_b11, k7_b34); `step1.3_manager_open.md` O2; my `step1.2_loftsman_redfirst_signoff.md` NOTE 1, NOTE 2. Section screw: c (theta 270, YZ plane); no step 0 item reads it. Dry runs: scratchpad scripts `p0l_dryrun.py` and `p0l_b34.py` (C:\Users\UR\AppData\Local\Temp\claude\eba575d6463ef2d6\6efaddfb-5e83-4849-8803-49d5d7303110\scratchpad\), temporary overlay copies only; the live overlay and specs untouched.

## Corrections to the brief

1. **My 1.2 (c) NOTE 1 count was wrong by one pair.** I wrote that every S1 pose-restricted declaration sits on the moving row. `s1_spec.yaml` l.371 puts `{id: bore_ceiling, class: G, g_min: 25, poses: [capture_end]}` (S1-5a) on fixed row `core_750`; `bore_ceiling` (moving) lists no neighbours. That pair escaped the side sweep through r4 to r7. Its verdict, swept now, is clean (section 4), so no accepted verdict was wrong.
2. The records carry no spec SHA-256. `files_sha256` holds only `params.yaml` and `proposed_params.yaml` (`check_sketch.py` l.450, `Params.hashes`). The brief's allowed list names "spec and overlay SHA-256". The `stack_ties` edits to `s1_spec.yaml` and `s2_spec.yaml` show in no record field. NOTE 2.
3. The brief's hand value "member tops 12 + 1213, 0 + 1225, 1165 + 60" reads member z_max = top guide + profile.height. The K6 field convention gives the same equality as term = feature edge + offset, offset `-profile.height` (Engineer Correction 4). Same plane, sign as coded.

## 1. Hand values beside the harness

Leaf values read from the live overlay and params (MEASURED, `p0l_dryrun.py`): anchor_z 265, length 900, top_guide_z 1165, profile.height 60, base.plate_thickness 12, member_length 1213, member_length_rail 1225; gear pitch_diameter 250, tooth_count 60, pitch_angle 71.565, face_width 30; pinion tooth_count 20; m = 250 / 60 = 4.16667.

| Quantity | Hand (DERIVED) | Harness (MEASURED) | Agree |
|---|---|---|---|
| top_guide_z = anchor_z + length | 265 + 900 = 1165 | 1165.00 | yes |
| member a, b top z_A | 12 + 1213 = 1225 | S1 and S2 frame_upper_a/_b z_max 1225.00 | yes |
| member c top z_A | 0 + 1225 = 1225 | S2 frame_upper_c z_max 1225.00 | yes |
| top guide + profile.height | 1165 + 60 = 1225 | guide_tie_a z_max 1225.00 (S1, S2) | yes |
| tie term vs feature + offset | 1165 vs 1225 - 60 = 1165 | 1165.00 vs 1165.00, five rows | yes |
| guide block | 1165 - 30 .. 1165 | guide_a 1135.00 .. 1165.00 | yes |
| anchor block | 265 .. 265 + 30 | anchor_a 265.00 .. 295.00 | yes |
| member_length expr | 1165 + 60 - 12 = 1213 | 1213.00 | yes |
| member_length_rail expr | 1165 + 60 = 1225 | 1225.00 | yes |
| ring.motor_mount_height | 52 - 57 / 2 = 23.5 | 23.50 | yes |
| guide.bushing_housing_od | 2 x 20 = 40 | 40.00 | yes |
| guide.bushing_drop | 42 - 12 = 30 | 30.00 | yes |
| ring.clearance_bore, counts | 200; 3; 3 | 200.00; 3.00; 3.00 | yes |
| gear.od | 250 + 2 m cos 71.565 = 250 + 8.3333 x 0.31623 = 252.635 | 252.64 (value), 0.005 apart | yes |
| pinion.pitch_angle | 90 - 71.565 = 18.435 | 18.435 | yes |
| pinion.pitch_diameter | 4.16667 x 20 = 83.333 | 83.33 | yes |
| pinion.outer_diameter | 83.333 + 8.3333 x 0.94868 = 91.239 | 91.24 | yes |
| pinion.r_toe | 125 - 30 x 0.94868 = 96.540 | 96.54 | yes |
| pinion.r_heel | 250 / 2 = 125 | 125.00 | yes |
| gear.toe_tip_above_pinion_axis | 96.54 x 20 / 60 - 4.16667 x 0.94868 = 32.180 - 3.953 = 28.227 | 28.23, 0.003 apart | yes |
| gear.pitch_angle (no expr) | atan(60 / 20) = 71.5651 | value 71.565 | yes, by hand only (NOTE 3) |

All 17 expr leaves sit within 0.005 of their expressions, inside the 0.05 tolerance.

## 2. Dry run, temporary overlay (MEASURED)

K2 = `expr_agreement_issues`; K6 = `plane_agreement_issues` on the S1 and S2 specs, figures empty (spec stack only).

| Stage | Values | K2 | K6 S1 | K6 S2 | Drawn state | Inconsistent and green? |
|---|---|---|---|---|---|---|
| S0 live | as accepted | 0 | 0 | 0 | screw 265..1165, members 1225 | no |
| S1 | length 950 only | 1: top_guide_z 1165 vs expr 1215.00, 50.00 apart | 0 | 0 | screw drawn 900 (anchor_z..top_guide_z) under label "T8 screw L" reading 950; members 1225 | no (K2) |
| S2 | + top_guide_z 1215 | 2: member_length 1213 vs 1263.00; member_length_rail 1225 vs 1275.00; 50.00 apart each | 2: member_top_a, _b, term 1215.00 vs 1165.00, 50.00 apart | 3: member_top_a, _b, _c, 50.00 apart | screw 265..1215, guide 1185..1215, guide ties to 1275, members still 1225 | no (K2, K6) |
| S3 | + member_length 1263, rail 1275 | 0 | 0 | 0 | screw 265..1215, members 1275, ties 1215..1275 | no (consistent) |
| X1 | top_guide_z 1215 only | 3: top_guide_z vs 1165.00; both member leaves | 2 | 3 | screw drawn 950, label 900 | no |
| X4 | anchor_z 280 only | 1: top_guide_z 1165 vs 1180.00, 15.00 apart | 0 | 0 | screw drawn 885, label 900 | no |
| **X2** | length 950, **expr deleted from top_guide_z** | 0 (16 leaves) | 0 | 0 | screw drawn 900, label 950 | **yes: every check green** |
| X3 | S2 values, expr deleted from both member leaves | 0 (15 leaves) | 2 | 3 | members 1225 against top guide 1215 | no (K6 ties) |

With the expr fields in place the chain anchor_z + length -> top_guide_z -> member tops is closed: no stage with a member top or guide height inconsistent with the screw passes. The two links are independent. K2 alone governs length -> top_guide_z, and K2 and the K6 ties both govern top_guide_z -> member tops (X3 shows the ties hold the second link without the member exprs).

The first link has one route past it: X2. Delete `expr` from `jackscrew.top_guide_z` and a screw length change leaves the drawn screw, guide blocks, ties and members at the old height while the label reads the new length, with K2 and K6 green. The Engineer names this route (open item 3). R2 a calls the three exprs mandatory; the overlay file enforces that and no check does. Detail 1 common (h) requires a relaxed or new rule's premise to be enforced by a check with its own Z and B. FIX 1.

## 3. Tie form

| Spec | id | term | feature | edge | offset | term z_A | edge + offset z_A |
|---|---|---|---|---|---|---|---|
| s1 | member_top_a | top_guide | frame_upper_a | z_max | -profile.height | 1165.00 | 1165.00 |
| s1 | member_top_b | top_guide | frame_upper_b | z_max | -profile.height | 1165.00 | 1165.00 |
| s2 | member_top_a | top_guide | frame_upper_a | z_max | -profile.height | 1165.00 | 1165.00 |
| s2 | member_top_b | top_guide | frame_upper_b | z_max | -profile.height | 1165.00 | 1165.00 |
| s2 | member_top_c | top_guide | frame_upper_c | z_max | -profile.height | 1165.00 | 1165.00 |

- Term: `check_stack.global_vars` sets `top_guide` = `jackscrew.top_guide_z` (z_A) when the key exists. The features' z_rule reads `base.plate_thickness + frame_upper.member_length` (a, b) and `frame_upper.member_length_rail` (c). The tie compares two different keys, so it carries information. It does not restate one key.
- Stub: `plane_agreement_issues` reads `ctx.stack` (spec z_rule per pose) and no figure. My dry run passes `figs={}` and the ties evaluate and fire (S2 stage). It holds on the stub.
- Offset sign: the K6-B10 fixture (member_length 1200: 12 + 1200 - 60 = 1152, 13.00 apart) and K6-B11 (rail 1210: 1210 - 60 = 1150, 15.00 apart) agree with the hand values. A sign error in the offset would read 1285 and 120 apart on the live spec; live reads 0.00.
- `top_guide` is added only when `jackscrew.top_guide_z` exists. A spec whose tie names it with the key absent reads "term 'top_guide' is not a stack name", a K6 failure. It cannot pass silently.

**SIGNED (Loftsman):** tie rows, term and offset.

## 4. NOTE 1, side swept branch

Code (l.2114-2141): the moving row's neighbours, then every fixed row's entries naming it (as `dict(nb, id=b)`). `unrestricted` and `rel_n` collect over both lists; `seen_un` lets the moving row's unrestricted entry govern a pair declared on both rows; a pose-restricted entry becomes F, g_min 0, once per pair, unless an unrestricted declaration exists on either row; C without poses skipped; N on either list excepts the pair. The plan branch (l.2324-2341) builds `rel` by `setdefault`, moving row first, and `rel_n` over both lists. Case by case the two branches give the same class for every combination of {none, unrestricted F/G/C/N, pose-restricted} on the two rows. One difference stays: the side branch does not sweep a pair declared on neither row, and the plan branch sweeps it as F. That scope dates from 1.1 (LF-3) and NOTE 1 did not raise it. The static per-pose undeclared F test covers the end poses.

Deletion test (MEASURED, `p0l_b34.py`): K7-B34 fixture on the current `sketch_common.py`: fail, "swept p1..p4/ring|member F: swept hull distance 0.000 mm, overlap 2000.000 mm2". The same fixture with the one line that reads the fixed rows (l.2120) replaced by `pass`: pass, "1 pair test(s) clean; states ['F', 'undeclared:F']". The B reproduces the escape and the new line closes it.

S1 r7 swept tests (MEASURED from `docs/sketches/s1_checks_r7.json` and `wip/s1_checks_r7.json`): pair tests 617 -> 618; K7 test rows 5556 -> 5557; swept:F 139 -> 140; swept:depth-separated 156, swept:plan-separated 6, swept:C 1 unchanged. New pair: `swept capture_end..park bore_ceiling|core_750 F`, state swept:F, z_gap -123.025, distance 192.34, overlap 0.0, basis XZ projection (exact). The swept distance equals the static capture_end distance (192.34): the bore ceiling rises from capture_end to park, so the hull's nearest edge to the core is its capture_end line. Hand check holds. Verdict pass. S2 uses the plan branch: unchanged.

**SIGNED (Loftsman):** NOTE 1 closed.

## 5. S1 r7 and S2 r5 record diffs (MEASURED, wip/ against docs/sketches/)

| Record | Top-level fields | Check fields | Allowed |
|---|---|---|---|
| s1_checks_r7.json | accepted; accepted_at, accepted_note (accepted copy only); files_sha256.proposed_params.yaml; timestamp | K2.reason; K7.reason, states, tests (section 4); new RPT pass (exempt); **K5 cause, measured, n_issues, reason, result** | all but K5: K5 pass -> fail, 8 issues, the TP1.1-9 zero-area anchor line (Engineer Correction 1; Topologist rules at P0T) |
| s2_checks_r5.json | same set | K2.reason; new RPT pass (exempt) | yes |
| s1_mass_report_r7.json | none | none | yes |

K6 reason and result unchanged on both (ties clean). keys_read equal (Engineer, section 8). No field from R2 or R5 d changed beyond the allowed list. The S1 K5 red is outside my items; it blocks the S1 re-accept until P0T rules.

## 6. Findings

**FIX 1 (chain premise unenforced).** K2 must fail when any of `jackscrew.top_guide_z`, `frame_upper.member_length`, `frame_upper.member_length_rail` carries no `expr`, or carries an expr other than the stated one: `jackscrew.anchor_z + jackscrew.length`; `jackscrew.top_guide_z + profile.height - base.plate_thickness`; `jackscrew.top_guide_z + profile.height` (compare after whitespace normalisation). Dry-run result (pre-fix code, section 2 X2): with length 950 and expr removed from top_guide_z, K2 0 issues and K6 0 on S1 and S2, so the B is red-first by construction. Controls: Z = K2-Z2 (live, unchanged); B "top_guide_z without expr, length 950" (reason substring "jackscrew.top_guide_z: expr required"); B "top_guide_z expr `jackscrew.anchor_z + 900`, length 950" (fires on the altered expr; the agreement lint alone reads 0 apart). No drawn value moves; S1 r7, S2 r5 results unchanged except K2 reason text.

**NOTE 1 (S3 and S1 r8 consequence).** Sean's STOP S3-A ruling (Design Notes 31: Tr12x3, fixed anchor in a 42-square block) opens S1 r8. Any change to `jackscrew.anchor_z`, `length` or block height must carry `top_guide_z` and both member leaves in the same overlay edit (stage S3 values). K2 and K6 will refuse a partial edit, and `--stale` will list all five keys on s1 r7 and s2 r5.

**NOTE 2 (records carry no spec or script hash).** `files_sha256` holds the params and overlay only. A spec edit (here `stack_ties` on both accepted specs) shows only through re-run results. For P1R or (c): add the spec and drawing-script SHA-256 to `files_sha256` and to `--stale`.

**NOTE 3.** `gear.pitch_angle` (atan 3 = 71.5651) has no expr; `eval_expr` has no `atand`. A one-function addition closes the 18th leaf. Not blocking.

**NOTE 4.** The side sweep still skips pairs declared on neither row (plan sweeps them as F). That is pre-existing LF-3 scope and outside NOTE 1. Name it for the S3 section view at (c), where the nut housing sweeps past the guide and anchor brackets.

**Verdict: FIX (1 item: FIX 1).** Signed pending FIX 1: tie rows, the K2 agreement lint, NOTE 1. On FIX 1 landing with its two B red-first, this reads STEP 0 PASS (Loftsman), with no re-review of the other items.

## Gameplan lines to change

**l.136** (K table, K2 row), after FIX 1 lands.
Old: `mandatory on jackscrew.top_guide_z, frame_upper.member_length, frame_upper.member_length_rail (1.3 step 0, O2) |`
New: `mandatory on jackscrew.top_guide_z, frame_upper.member_length, frame_upper.member_length_rail: a missing or altered expr on those three fails (1.3 step 0, O2; Loftsman P0L FIX 1) |`
Old: `B4 jackscrew.length 950 with top_guide_z 1165; B5 member_length_rail 1230 |`
New: `B4 jackscrew.length 950 with top_guide_z 1165; B5 member_length_rail 1230; B6 top_guide_z without expr, length 950; B7 top_guide_z expr altered (Loftsman P0L FIX 1) |` (the control ids are the Engineer's to assign at P0f)

**l.732** (Echo Site Registry, member tops row).
Old: `Loftsman sign at P0L |`
New: `signed by the Loftsman at P0L (research/sean/cr_scratch/step1.3_loftsman_step0_check.md), mandatory-expr rule FIX 1 at P0f |`

The K7 row (l.141) wording proposed by the Engineer (section 12) stands as written.
