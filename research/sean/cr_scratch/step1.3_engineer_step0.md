# Step 1.3 step 0 (P0), The Engineer: harness before S3

Date 2026-11-26. Working copy `docs/sketches/`. Pre-change copy of the whole tree taken before the first edit (scratchpad `p0/pre`, params.yaml beside it); every red-first run below used that copy with only the new fixture files and manifest added. Python 3.12 at the path in [CTX COMMON]. Section screw: c (theta 270, YZ plane), STOP S3-0 "A: screw c"; no step 0 item reads it.

## Corrections to the brief

1. **TP1.1-9 as specified turns accepted S1 r7 red. BLOCKING for ORCH-A on s1.** `s1_side_poses.py` l.230 draws the anchor thrust-bearing line as a zero-height Rectangle tagged `anchor_a` / `anchor_b` (`sc.draw_rect(ax, f"anchor_{s}", x0, x1, (z0 + z1) / 2, (z0 + z1) / 2, linewidth=2)`). This is the exact artist the Topologist named in the TP1.1-9 NOTE (`step1.1_topologist_*`: "The anchor thrust-bearing line is a zero-height Rectangle tagged to the anchor row"). With the lint, `s1 --rev 7` reads K5 fail, 8 issues (2 anchors x 4 poses), cause content: 17/18 (MEASURED). R5 a asked for "Z live S1"; that Z cannot be clean without a drawing change. Drawing and check untouched, per R6. S2 r5 has no zero-area patch: 17/17. Options in section 11.
2. The brief puts K2 at l.135, K5 l.138, K6 l.139, K7 l.140, K8 l.141 and the Echo member-tops row at l.716. Live gameplan (MEASURED): K2 l.136, K5 l.139, K6 l.140, K7 l.141, K8 l.142, K9 l.143, K table pointer l.146, Echo member-tops row l.719 (l.716 is the screw frame radius row). Section 12 uses the live numbers.
3. O2 counts 19 DERIVED leaves in the overlay. MEASURED: 18 leaves with `status: DERIVED`; the 19th grep hit is a source string containing "DERIVED" (ring.position_above_tip or drill.mass).
4. The stack-tie expression "z_max = top guide + profile.height (offset)" maps onto the K6 field convention as `offset: "-profile.height"`: `plane_agreement_issues` compares `term` with `feature.edge + offset`, so term top_guide 1165 = member z_max 1225 + (-60).
5. Serial controls wall time on the pre-change code: 775 s (MEASURED this session, 230/230), not 794 s.

## 1. Files changed

| Path | What |
|---|---|
| docs/sketches/check_sketch.py | R1 `--jobs`, `--only`, `--manifest`, `control_row`, spawn pool, `CONTROL_EQ_FIELDS`, per-row `seconds`, summary `jobs` and `wall_seconds`; R3 `rpt_check`, `RPT_EXEMPT`, RPT appended to every sN run, `reported_items` carried in the record, Reported items table in the summary, `--accept` refuses a record that declares reported_items without an RPT row; R4 `SKETCH_CHECK` regex routing `S<n>-`, `k_checks(s)` (checks_sN.py `K_CHECKS` overrides K_BY_SKETCH); keys_read scope kept (P.accessed restored around `reported`); docstring |
| docs/sketches/check_stack.py | R2 `global_vars` term `top_guide` = `jackscrew.top_guide_z` (when the key exists) |
| docs/sketches/sketch_common.py | R2 `expr_agreement_issues` in K2 (P.accessed restored); R5 a `zero_area_issue` in K5; R5 b `STAND_IN_OWNER` regex in `cover_issues`; R5 c `FRAME_VALUES` in `sense_lint`; R5 d K7 side swept reads fixed rows' entries naming the moving row, N on either list excepts the pair, one unrestricted entry per pair (moving row's first) |
| docs/sketches/proposed_params.yaml | `expr` on 17 of 18 DERIVED leaves (section 3); no value changed |
| docs/sketches/s1_spec.yaml | `stack_ties` member_top_a, member_top_b (+2 comment lines) |
| docs/sketches/s2_spec.yaml | `stack_ties` member_top_a, _b, _c (new field, +2 comment lines) |
| docs/sketches/fixtures/builders.py | k2_z2, k2_b4, k2_b5, k6_b10, k6_b11, k5_b19, k8_b42, k8_b43, k7_b34 |
| docs/sketches/fixtures/step0_fixtures.py | rpt_z, rpt_b1, rpt_b2, h1_b_rpt_fail, h1_b_rpt_absent, run_z, run_b |
| docs/sketches/fixtures/manifest.yaml | 16 entries (section 7) |

No drawing script, stub or record edited.

## 2. R1 runner

Design. `controls()` loads the manifest, applies `--only`, and calls `run_controls_rows(man, jobs)`. jobs 1: in process. jobs > 1: `multiprocessing.get_context("spawn").Pool(min(jobs, n))`, `imap_unordered(_control_task, enumerate(man), chunksize=1)`, rows placed back by index, so the file and the printout are in manifest order. Each worker keeps its own `_MODS` and builder caches (`_S2_LIVE`); a control sees only its worker's caches, as in the serial run it sees the process's. Control figures and key.json are generated once, in the main process, after the pool, and only for the full live manifest. Default jobs `min(os.cpu_count() - 2, 12)` = 12 on this machine (16 logical CPUs). Each row gains `seconds` (control wall time in its worker); the summary gains `jobs` and `wall_seconds`.

Partial-run rule. `--only` takes comma-separated tokens; an entry is kept when its id matches a token as an fnmatch glob or its check id equals a token. Output goes to `wip/fixtures/controls_results_partial.json` with a `partial` field, figures are not generated, and the run prints "PARTIAL, not a record". `control_tally()` and `harness_outputs()` (`--accept`) read only `fixtures/controls_results.json` and `fixtures/figs/*`, so the partial file is never read by either. `--manifest <path>` (another manifest) writes `controls_results.json` beside that manifest and nothing under wip/ or docs/.

Equality (R1 b), fields compared: id, expected, observed, reason, match (`CONTROL_EQ_FIELDS`); excluded: `seconds`, file timestamp, summary `jobs` / `wall_seconds`.

Live manifest, 246 rows, `--jobs 12` against `--jobs 1` (MEASURED):

| Field | Rows differing |
|---|---|
| id (and order) | 0 |
| expected | 0 |
| observed | 0 |
| match | 0 |
| reason | 1: H1-B5, the temporary-directory path inside the refusal text (`tmp3lrqe4cl` against `tmpc27upxwy`); the path differs between any two runs, serial or parallel |

Also equal: check, control, finding, gameplan_line, reported (smoke per-check results). Both runs 246/246 matched.

Wall time (MEASURED):

| Run | Controls | Jobs | Wall |
|---|---|---|---|
| pre-change code, serial (scratchpad copy) | 230 | 1 | 775 s |
| post-change, default jobs | 246 | 12 | 113.4 s (shell 116 s) |
| post-change, serial | 246 | 1 | 804.3 s |

Target 200 s at default jobs: met. Sum of per-control seconds in the parallel run 1179.1 s (workers contend for memory bandwidth; serial per-control times are lower). Slowest controls at jobs 12: S2-FULL 30.2 s, K8-B35 18.9, K8-Z8 18.5, K8-B34 17.8, K8-B39 17.7, K8-B40 17.1, S1-FULL 16.1, K8-B37 16.0, K8-B19 16.0, K8-B23 16.0, K8-B29 15.8, K8-B25 15.7, K8-B41 15.7, K8-B38 15.7, K8-B21 15.6. The critical path is S2-FULL (30 s) plus spawn and import (about 5 s per worker).

Runner B (R1 e): RUN-B writes a temporary two-row manifest (K1-Z, K2-Z with expected fires), runs `check_sketch.py --controls --manifest <tmp> --jobs 2` as its own process: exit 1, mismatched ['K2-Z'], one printed "match NO" line, jobs 2. RUN-Z: same manifest with correct expectations, exit 0, both rows yes in manifest order. Pre-change code: both read argparse exit 2 ("unrecognized arguments"), RUN-B no "match NO" line (mismatch).

## 3. R2 expr leaves, tie rows, controls

`expr` evaluated by `check_stack.eval_expr(expr, P, {})`; values MEASURED by the K2 lint path on the live overlay.

| Key | expr | Value | eval |
|---|---|---|---|
| jackscrew.top_guide_z | jackscrew.anchor_z + jackscrew.length | 1165 | 1165.00 |
| frame_upper.member_length | jackscrew.top_guide_z + profile.height - base.plate_thickness | 1213 | 1213.00 |
| frame_upper.member_length_rail | jackscrew.top_guide_z + profile.height | 1225 | 1225.00 |
| ring.nut_housing_count | jackscrew.count | 3 | 3.00 |
| ring.motor_mount_count | pinion.count | 3 | 3.00 |
| ring.clearance_bore | bearing.od | 200 | 200.00 |
| ring.motor_mount_height | pinion.axis_above_ring_top - pinion.motor_body / 2 | 23.5 | 23.50 |
| guide.bushing_housing_od | 2 * ring.guide_lug_half_width | 40 | 40.00 |
| guide.bushing_drop | guide.bushing_length - ring.thickness | 30 | 30.00 |
| gear.od | gear.pitch_diameter + 2 * gear.pitch_diameter / gear.tooth_count * cosd(gear.pitch_angle) | 252.64 | 252.64 |
| gear.toe_tip_above_pinion_axis | pinion.r_toe * pinion.tooth_count / gear.tooth_count - gear.pitch_diameter / gear.tooth_count * cosd(pinion.pitch_angle) | 28.23 | 28.23 |
| pinion.pitch_angle | 90 - gear.pitch_angle | 18.435 | 18.435 |
| pinion.pitch_diameter | gear.pitch_diameter / gear.tooth_count * pinion.tooth_count | 83.33 | 83.33 |
| pinion.outer_diameter | pinion.pitch_diameter + 2 * gear.pitch_diameter / gear.tooth_count * cosd(pinion.pitch_angle) | 91.24 | 91.24 |
| pinion.face_width | gear.face_width | 30 | 30.00 |
| pinion.r_toe | gear.pitch_diameter / 2 - pinion.face_width * sind(gear.pitch_angle) | 96.54 | 96.54 |
| pinion.r_heel | gear.pitch_diameter / 2 | 125 | 125.00 |

All 17 within 0.05 (K2 reason on live S1 and S2: "17 expr leaves agree within 0.05"). Left without expr: `gear.pitch_angle` (atan of the tooth ratio; `eval_expr` FUNCS has no atan, and adding one is a check_stack change outside R2). The gear and pinion exprs read the gear module as `gear.pitch_diameter / gear.tooth_count` (4.1667), as the sources state.

K2 lint premise: |value - eval(expr)| <= 0.05 for every leaf carrying `expr`; the evaluation restores `P.accessed`, so `keys_read` in records is unchanged (MEASURED: keys_read equal on s1 r7 and s2 r5 re-runs).

Tie rows (K6 `stack_ties`, term `top_guide` from `check_stack.global_vars` = `jackscrew.top_guide_z`, z_A):

| Spec | id | feature | edge | offset | term z_A | feature + offset z_A |
|---|---|---|---|---|---|---|
| s1 | member_top_a | frame_upper_a | z_max | -profile.height | 1165.00 | 1225 - 60 = 1165.00 |
| s1 | member_top_b | frame_upper_b | z_max | -profile.height | 1165.00 | 1165.00 |
| s2 | member_top_a | frame_upper_a | z_max | -profile.height | 1165.00 | 1165.00 |
| s2 | member_top_b | frame_upper_b | z_max | -profile.height | 1165.00 | 1165.00 |
| s2 | member_top_c | frame_upper_c | z_max | -profile.height | 1165.00 | 1165.00 |

Source on each row: "Loftsman 1.2 (b) NOTE 2". Z: K6-Z3 (live S1 spec, lint only) and K6-Z4 (live S2) carry the ties, both clean. Together: a `jackscrew.length` change without the dependent leaves fires K2 on top_guide_z (K2-B4); a top_guide_z change without the members fires K2 on both member leaves; a member leaf change fires K2 and the K6 tie (K6-B10, K6-B11). The member tops cannot drift from the screw length with every check green.

Controls: K2-Z2, K2-B4, K2-B5, K6-B10, K6-B11 (section 7). K6-B10 planted 2 (members a and b, 13.00 apart each); K6-B11 planted 1 (member c, 15.00 apart). On those two fixtures K2 also fires on the member expr; K2 is a separate check, so the K6 planted count excludes it (stated in each manifest desc).

## 4. R3 RPT

- Spec field `reported_items`: list of {id, text, source, needs_drawing}.
- Values: `checks_sN.py reported(ctx)` returns, besides `rows`, a dict `items` {id: {value, basis, tag}}. `run_sketch` passes it to `rpt_check`.
- RPT fails per declared id whose value is absent or None; malformed entries and duplicate ids are spec errors. Cause on rev 0: "absent" when every missing item has needs_drawing true, else "content".
- A spec with no `reported_items` fails unless the record name is in `RPT_EXEMPT` = {s1_checks_r7.json, s2_checks_r5.json}: reason "not declared, exempt (accepted before RPT): <record>, <accept note>".
- The record carries `reported_items` when the spec declares it; `write_summary` emits "## Reported items" (ID, Item, Value, Basis, Tag; ABSENT for a missing value), or for an exempt record the line "Reported items: not declared, exempt ...".
- `--accept`: refuses through RPT as through any check not pass; refuses also a record that declares `reported_items` and has no RPT row ("RPT absent (record declares reported_items)").
- Controls: RPT-Z, RPT-B1, RPT-B2, H1-B7, H1-B8 (section 7).

## 5. R4 hard-code list

Changed: `run_control` routes `^S(\d+)-` to `checks_s<n>.py` (was `("S1-", "S2-")`). `run_sketch` reads `k_checks(s)`: `checks_sN.py K_CHECKS` if defined, else K_BY_SKETCH (s5), else K1 to K9; S3 gets K1 to K9 with no edit. `sketch_table` already prefers `checks_sN.py` STUB_EXPECT / STUB_CAUSE / SOURCES, so s3 needs no SKETCH_TABLES entry.

| Place | Names | S3 needs a change |
|---|---|---|
| check_sketch.py SKETCH_TABLES "s1" | S1 stub tables | No (checks_s3.py defines its own; STUB_EXPECT must list RPT as red, cause absent, if S3 declares needs_drawing items) |
| check_sketch.py RPT_EXEMPT | s1 r7, s2 r5 record names | No; by design. An S1 r8 / S2 r6 must declare reported_items |
| check_sketch.py baseline() l.790 `{"s1": prior["run2"]}` | pre-H3 record shape | No |
| check_sketch.py write_summary "Reported (no threshold)" block | park rule, Q9, collar top from `check_stack.reported` | Yes if `s3_spec.yaml` lacks the park-rule fields check_stack.reported reads (load_plane, entry_plane, q9 keys); S2 carries them as data for this reason. Decide at (b) |
| check_stack.py main default spec s1_spec.yaml | CLI default | No |
| fixtures/builders.py imports checks_s1, checks_s2; `_script_ctx` map {"s1": s1_side_poses, "s2": s2_plan}; S1_SPEC, S2_SPEC | fixture helpers | Yes at (c): add checks_s3 import and the s3 script to `_script_ctx` |
| fixtures/step0_fixtures.py `_template` (s1_checks_r4.json), PNG name | H1 template | No |
| sketch_common.py VIEW_NORMAL, SIDE_VIEWS (side_xz, section_xz, plan_xy) | view names, no sketch id | Yes at (c) (O4): a YZ section view for screw c |
| s1_mass_report.py | S1 only | No |

## 6. R5 lints

| Item | Rule | Live result | Controls |
|---|---|---|---|
| a TP1.1-9 | K5: Rectangle with width or height 0, or Polygon with area <= 0.01 mm² in data coordinates, on a row whose kind is not line, arrow or callout (`NO_AREA_KINDS`), fails | S2 r5 clean; **S1 r7 fails 8** (anchor thrust-bearing line, Correction 1); fixture S1 / S2 drawings clean (K5-Z2, K5-Z3) | K5-B19 |
| b TP1.2-18 | `stand_in_owner` must match `\bStep\s+\d+(\.\d+)?\b` or `\b[Ss][1-6]\b` ("Step 2", "S3", "1.3 (S3)", s1 to s6); otherwise spec error and the row loses the stand_in exemption (as TP1.2-17) | S2 ties ("Step 2: rod top support ...") pass; K8-Z8 clean | K8-B42 |
| c Topologist 1.2 (c) NOTE 2 | `sense_lint`: a predicate carrying `frame` must have a value in `FRAME_VALUES` = ("radial",) | S2 six `frame: radial` pass; S1 none | K8-B43 |
| d Loftsman 1.2 (c) NOTE 1 | side swept: a moving row's candidates are its own neighbours, then each fixed row's entries naming it; N on either list excepts the pair; one unrestricted entry per pair, the moving row's first; pose-restricted pairs swept as F once | S1 r7 gains one swept test, `swept capture_end..park bore_ceiling|core_750 F`, clean (617 to 618 tests); S2 (plan branch) unchanged | K7-B34 |

## 7. Control table (new controls)

Pre-change = scratchpad copy of `docs/sketches/` before the first edit, with the new fixtures and manifest only; run per entry with the pre-change `run_control` and `compare` (MEASURED).

| ID | Planted | Reason substring | Pre-change code | Result |
|---|---|---|---|---|
| RUN-Z | two-row manifest, correct, --jobs 2 | (clean) | fires: exit 2, unrecognized arguments | match yes |
| RUN-B | K2-Z expecting fires, --jobs 2 | "exit 1", "mismatched ['K2-Z']", "match NO" | clean (0 issues): exit 2, no match NO line; mismatch | match yes |
| K2-Z2 | live overlay with expr, live S1 spec | (clean) | clean | match yes |
| K2-B4 | jackscrew.length 950, top_guide_z 1165 | "overlay jackscrew.top_guide_z: value 1165 vs expr", "= 1215.00, 50.00 apart" | clean; mismatch | match yes |
| K2-B5 | member_length_rail 1230 | "overlay frame_upper.member_length_rail: value 1230 vs expr", "= 1225.00, 5.00 apart" | clean; mismatch | match yes |
| K6-B10 | S1 member_length 1200 | "stack_tie member_top_a: term top_guide", "frame_upper_a.z_max", "stack_tie member_top_b", "13.00 apart" (planted 2) | clean; mismatch | match yes |
| K6-B11 | S2 member_length_rail 1210 | "stack_tie member_top_c: term top_guide", "frame_upper_c.z_max", "15.00 apart" | clean; mismatch | match yes |
| RPT-Z | fixture spec, two items supplied | (clean) | error: no rpt_check | match yes |
| RPT-B1 | F_stall without value | "reported item F_stall", "no value (needs drawing)" | error | match yes |
| RPT-B2 | s3_checks_r1.json, no reported_items | "spec declares no reported_items", "s3_checks_r1.json" | error | match yes |
| H1-B7 | record with reported_items, RPT fail | "refused", "checks not pass: RPT fail" | error (fixture calls rpt_check). The refusal itself exists on the pre-change code through the generic not-pass rule; H1-B7 guards it, H1-B8 is the new branch | match yes |
| H1-B8 | record with reported_items, no RPT row | "refused", "RPT absent (record declares reported_items)" | clean: accepted, flagged True, record copied; mismatch | match yes |
| K5-B19 | zero-height Rectangle on drill_tube at load (fixture S1) | "load/drill_tube: zero-area Rectangle", "on a cylinder row (TP1.1-9)" | clean (296 artists projected); mismatch | match yes |
| K8-B42 | S2 tie a stand_in_owner "tbd" | "guide_tie_a cover: spec error, stand_in_owner 'tbd' names no Step id", "guide_tie_a cover: Polygon partly visible drawn dashed" (planted 2) | clean (190 predicates hold); mismatch | match yes |
| K8-B43 | S2 motor23_a outboard frame "polar" | "motor23_a outboard: spec error, unknown frame 'polar'" | clean (185 predicates hold); mismatch | match yes |
| K7-B34 | side: G 10 at p4 written only on the fixed member | "swept p1..p4/ring|member F", "swept hull", "overlap 2000.000" | clean (1 pair test; F, undeclared:F); mismatch | match yes |

Counts: 230 + 16 = 246 (Z 64 + 3 = 67, B 164 + 13 = 177, smoke 2).

## 8. R6 runs and record diff

| Command | Exit | Wall | Result |
|---|---|---|---|
| s1_side_poses.py --rev 7 | 0 | 11 s | 4 PNGs to wip/ |
| check_sketch.py s1 --rev 7 | 1 | 18 s | **17/18 + RPT pass: K5 fail (8, content)**; K1 to K4, K6 to K9, S1-1 to S1-7, X1, RPT pass |
| s2_plan.py --rev 5 | 0 | 11 s | PNG to wip/ |
| check_sketch.py s2 --rev 5 | 0 | 31 s | 17/17 + RPT pass (exempt) |
| s1_mass_report.py --rev 7 | 0 | 5 s | wip/s1_mass_report_r7.json |

PNGs: s1_pose_load/start/capture_end/park_r7.png and s2_plan_r5.png SHA-256 equal and pixel-equal to `docs/sketches/` (MEASURED).

Record diff (wip/ against docs/, `_json_field_diffs` plus per-check fields):

| Record | Differing fields | Allowed |
|---|---|---|
| s1_checks_r7.json | accepted (False in wip), accepted_at and accepted_note (absent in wip), timestamp, files_sha256.proposed_params.yaml; checks: list length (RPT row added: pass, exempt); K2.reason (+ "; 17 expr leaves agree within 0.05"); K7.reason 617 to 618 tests, K7.states and K7.tests 5556 to 5557 (added swept capture_end..park bore_ceiling|core_750 F); **K5.result pass to fail, K5.measured 0 to 8, K5.n_issues 0 to 8, K5.cause None to content, K5.reason** | all but K5 result/cause: K5 turns red (Correction 1) |
| s2_checks_r5.json | accepted, accepted_at, accepted_note, timestamp, files_sha256.proposed_params.yaml; checks length (RPT row, exempt); K2.reason | yes |
| s1_mass_report_r7.json | none | yes |
| keys_read | equal on both records | yes |

Summaries (line-positional diff is long because the RPT row shifts every line): s1_summary_r7.md content changes are the timestamp, K2 reason, K5 row and its cause-of-red row, K7 count, RPT row, the "Reported items: not declared, exempt" line and the overlay hash; s2_summary_r5.md the same less K5 and K7.

Stale and final runs: `--stale`: 2 records (s1_checks_r7.json, s2_checks_r5.json), 0 differences, X1 pass, exit 0. `--stale --include-unaccepted`: 11 records, 0 differences, exit 0. Final `--controls` (default jobs 12): 246 matched (Z 67/67, B 177/177, smoke 2/2), 113.4 s; `--controls --jobs 1`: 246 matched, 804.3 s. The last run (jobs 1) leaves `wip/fixtures/controls_results.json` fully matched for `--accept`.

## 9. SHA-256 of committed files

Committed files under `docs/sketches/` (wip/ and __pycache__ excluded), 57 files, SHA-256 first 16 hex digits; full hashes in scratchpad p0/sha_before.txt and p0/sha_after.txt. Changed: 9, every one in section 1. Unexpected differences: 0. `fixtures/controls_results.json` and `fixtures/figs/*` unchanged (runs write wip/ only).

| File | Before | After | Edited on purpose |
|---|---|---|---|
| baseline_red.json | ded24e26ee9104f7 | ded24e26ee9104f7 | unchanged |
| check_sketch.py | 7e68a99acfc49899 | f13990a4c604aa68 | yes |
| check_stack.py | b5d30b468d296127 | ba68ceb8594f42fb | yes |
| checks_s1.py | d0981dd756c8b75b | d0981dd756c8b75b | unchanged |
| checks_s2.py | e18708622e1fb095 | e18708622e1fb095 | unchanged |
| fixtures/builders.py | c1c9338e70ed0a85 | cbed0420db785f33 | yes |
| fixtures/controls_results.json | 64c0339a058ce217 | 64c0339a058ce217 | unchanged |
| fixtures/figs/ctrl_a.png | 38bb75517ddc5ef4 | 38bb75517ddc5ef4 | unchanged |
| fixtures/figs/ctrl_b.png | aa784a1561f0bc9b | aa784a1561f0bc9b | unchanged |
| fixtures/figs/ctrl_c.png | f0b94f1f50fdb198 | f0b94f1f50fdb198 | unchanged |
| fixtures/figs/ctrl_d.png | a9f68b7b35479d93 | a9f68b7b35479d93 | unchanged |
| fixtures/figs/key.json | b41eabba9ad3f0bd | b41eabba9ad3f0bd | unchanged |
| fixtures/k1_b1_literal.py | 9b46618d41374b4a | 9b46618d41374b4a | unchanged |
| fixtures/k1_b2_softkey.py | a35213270980553b | a35213270980553b | unchanged |
| fixtures/k1_z_clean.py | e631b8597b30c017 | e631b8597b30c017 | unchanged |
| fixtures/k2_b1_overlay.yaml | b9040a085498ebf3 | b9040a085498ebf3 | unchanged |
| fixtures/k2_b2_overlay.yaml | dd6ec09f1cf99774 | dd6ec09f1cf99774 | unchanged |
| fixtures/k2_b3_overlay.yaml | a714a288b1ff9e96 | a714a288b1ff9e96 | unchanged |
| fixtures/k2_spec.yaml | e4d09a77493417d3 | e4d09a77493417d3 | unchanged |
| fixtures/k2_z_overlay.yaml | 1405246f55046918 | 1405246f55046918 | unchanged |
| fixtures/k6_b3_check_stack.py | 5b1fa0d58e8d09d6 | 5b1fa0d58e8d09d6 | unchanged |
| fixtures/manifest.yaml | 0153d7df9eba3db0 | de0a1f5f428dfc3b | yes |
| fixtures/step0_fixtures.py | ef337e870b16b03d | 6a4e230b4429ce87 | yes |
| gitignore | 2a3c1254ccaa3898 | 2a3c1254ccaa3898 | unchanged |
| proposed_params.yaml | d647105fe3d3a89d | 3bb83d7f7819b174 | yes |
| s1_checks_r0.json | 7454be78c0816cd2 | 7454be78c0816cd2 | unchanged |
| s1_checks_r4.json | 2443eb47ac57199f | 2443eb47ac57199f | unchanged |
| s1_checks_r7.json | 79c0569082d323c4 | 79c0569082d323c4 | unchanged |
| s1_mass_report.py | 5f60de14994f2364 | 5f60de14994f2364 | unchanged |
| s1_mass_report_r4.json | 34cface837bbc753 | 34cface837bbc753 | unchanged |
| s1_mass_report_r7.json | 34cface837bbc753 | 34cface837bbc753 | unchanged |
| s1_pose_capture_end_r4.png | b490bc840ba3acfd | b490bc840ba3acfd | unchanged |
| s1_pose_capture_end_r7.png | 06737eaa7b096b36 | 06737eaa7b096b36 | unchanged |
| s1_pose_load_r4.png | 9cb0949db4be94f3 | 9cb0949db4be94f3 | unchanged |
| s1_pose_load_r7.png | f078e511aa5d276f | f078e511aa5d276f | unchanged |
| s1_pose_park_r4.png | b3d2cffce16af13c | b3d2cffce16af13c | unchanged |
| s1_pose_park_r7.png | 1710cca8225e679b | 1710cca8225e679b | unchanged |
| s1_pose_start_r4.png | 37642cf4b1a091d1 | 37642cf4b1a091d1 | unchanged |
| s1_pose_start_r7.png | 715b397137e22bcd | 715b397137e22bcd | unchanged |
| s1_side_poses.py | 1a5914db43dbee08 | 1a5914db43dbee08 | unchanged |
| s1_spec.yaml | b85f86443c0d7ecf | 8e1b271187753373 | yes |
| s1_summary_r4.md | 015ca326b2235517 | 015ca326b2235517 | unchanged |
| s1_summary_r7.md | b21f3315e95f0c91 | b21f3315e95f0c91 | unchanged |
| s1_visual_gate_r3.md | 0366c2cab3b9e6b4 | 0366c2cab3b9e6b4 | unchanged |
| s1_visual_gate_r7.md | 32878e2356808f6c | 32878e2356808f6c | unchanged |
| s2_checks_r0.json | 104cb910cf7e06c8 | 104cb910cf7e06c8 | unchanged |
| s2_checks_r5.json | bce3a5ae03272566 | bce3a5ae03272566 | unchanged |
| s2_plan.py | b37e498ddf4576a7 | b37e498ddf4576a7 | unchanged |
| s2_plan_r5.png | 07830026d256cb9a | 07830026d256cb9a | unchanged |
| s2_spec.yaml | 8f6a13e2c03d683d | 7b3ab8e1f93447e6 | yes |
| s2_summary_r5.md | 6ffb3089352e1af0 | 6ffb3089352e1af0 | unchanged |
| s2_visual_gate_r1.md | d141d01fa821e6f8 | d141d01fa821e6f8 | unchanged |
| s2_visual_gate_r3.md | e09551cd0945a4f9 | e09551cd0945a4f9 | unchanged |
| sketch_common.py | fef5089179e33a97 | a5a2d91e5b82234a | yes |
| sketch_loader.py | a6fec2eb3f191513 | a6fec2eb3f191513 | unchanged |
| stubs/s1_stub.py | cc35b89f124cb77b | cc35b89f124cb77b | unchanged |
| stubs/s2_stub.py | 3b0a8685eee47c1e | 3b0a8685eee47c1e | unchanged |

## 10. Accept commands and expected output

Run from `docs/sketches/` after the reviews pass, with `wip/fixtures/controls_results.json` from a full run with every control matched.

```
python check_sketch.py --accept s2 --rev 5 --note "Design Notes 13 S2-r5; re-accepted 1.3 step 0 (RPT exempt, member-top ties, K2 expr lint)"
python check_sketch.py --accept s1 --rev 7 --note "Design Notes 13 S1-r7; re-accepted 1.3 step 0 (RPT exempt, member-top ties, K2 expr lint)"
python check_sketch.py --stale
```

Expected, s2: exit 0; "replace s2_checks_r5.json: N differing field(s): accepted_at; accepted_note; checks; files_sha256.proposed_params.yaml; timestamp" (accepted_note differs only if the note text differs from "Design Notes 13 S2-r5"); "replace s2_summary_r5.md: ... differing line(s)"; "kept s2_plan_r5.png (byte-equal, kept)"; controls results and control figures copied up from wip/ (wip/baseline_red.json too, kept if byte-equal); "accepted s2 r5". No earlier s2 record to supersede.

Expected, s1 on the current code and drawing: **exit 1, "refused: s1_checks_r7.json has checks not pass: K5 fail"**. Once Correction 1 is resolved (section 11) the same command gives exit 0 with replace s1_checks_r7.json (same field list as s2 plus K7 tests/states/reason), replace s1_summary_r7.md, replace s1_mass_report_r7.json (0 differing fields, byte copy), four PNGs kept byte-equal, "accepted s1 r7".

`--stale` after either: 2 records, 0 differences; X1 pass.

## 11. Open items

1. **BLOCKING (orchestrator to Sean): S1 r7 K5 red under TP1.1-9.** Artist: `s1_side_poses.py` l.230, zero-height Rectangle tagged anchor_a / anchor_b, 4 poses. Options: (A) S1 r8: draw the bearing line as a sub-artist `anchor_<s>:line` (Line2D) with a K5 admission rule and K9 sub-gid rule in the pattern of `:ticks` / `:outline`, plus Z and B; pixel equality not yet dry-run; a PNG that differs opens r8 under (i) with M1 on its pixels. (B) S1 r8: remove the line (pixels change; the thrust bearing is then unmarked until S3 draws it). (C) Scope the lint to exclude this device (an exemption the Topologist rejected in the NOTE's own words: "The same device can carry any line past K5's projection rule"). Recommendation A; it needs the Topologist's sign at P0T. ORCH-A can re-accept S2 r5 alone in the meantime.
2. `--accept` does not refuse a record that carries no RPT row and declares no reported_items (pre-rule records such as the H1 template s1 r4). Every record written by the current `run_sketch` carries an RPT row, so the gap applies only to records written by older code.
3. The three chain leaves are "mandatory expr" by this file, not by a lint: deleting `expr` from top_guide_z silences the agreement check. A K2 rule "these keys must carry expr" with its own B is a one-line addition if P0L wants it.
4. `gear.pitch_angle` has no expr (no atan in `eval_expr`).
5. S3 items carried: checks_s3.py STUB_EXPECT must list RPT; write_summary park-rule block needs the S1/S2 park-rule fields in s3_spec.yaml or a guard; builders.py `_script_ctx` map and imports; YZ section view (O4).

## 12. Gameplan lines to change

Line numbers are the live gameplan (Correction 2). Each change replaces the Old fragment (exact, unique in its line) with the New fragment.

**l.124** (detail 1.0, check_sketch.py bullet).
Old: `` `check_sketch.py --baseline sN` assembles run 2 for sN (Z and B controls: H1-Z1 to H1-Z3, H1-B1 to H1-B6).``
New: `` `check_sketch.py --baseline sN` assembles run 2 for sN (Z and B controls: H1-Z1 to H1-Z3, H1-B1 to H1-B8). `check_sketch.py --controls --jobs N` runs the manifest in N spawn worker processes (default min(cpu_count - 2, 12)), rows in manifest order, per-control id, expected, observed, reason and match equal to `--jobs 1` (1.3 step 0, RUN-Z, RUN-B; 246 controls 113 s at 12 jobs against 775 s serial on 230); `--only <id globs or check ids>` writes `wip/fixtures/controls_results_partial.json`, "PARTIAL, not a record", never read by control_tally or `--accept`; runs of record use the full set. Every sN run ends with check RPT: each id in the spec's `reported_items` ({id, text, source, needs_drawing}) has a value from `checks_sN.py reported(ctx)["items"]`, cause absent on rev 0 for needs_drawing items; the summary carries a Reported items table; s1 r7 and s2 r5 read "not declared, exempt (accepted before RPT)" by record name; `--accept` refuses through RPT and refuses a record declaring reported_items without an RPT row (RPT-Z, RPT-B1, RPT-B2, H1-B7, H1-B8; 1.3 open O10). `run_control` routes any `S<n>-` check to `checks_s<n>.py`; `checks_sN.py K_CHECKS` overrides the K list (1.3 open O13).``

**l.136** (K table, K2 row).
Old: `a DECLARED overlay leaf cites [CP §n, mm:ss] or [DN23] | Fixture overlay with sourced leaves | B1 overlay key `drill.tube_od`; B2 overlay leaf with empty source; B3 DECLARED leaf with no citation |`
New: `a DECLARED overlay leaf cites [CP §n, mm:ss] or [DN23]; an overlay leaf with an `expr` field (arithmetic in other keys, check_stack.eval_expr) fails when |value - eval(expr)| > 0.05, premise of every DERIVED literal; expr on 17 of 18 DERIVED leaves, mandatory on jackscrew.top_guide_z, frame_upper.member_length, frame_upper.member_length_rail (1.3 step 0, O2) | Fixture overlay with sourced leaves; K2-Z2 live overlay | B1 overlay key `drill.tube_od`; B2 overlay leaf with empty source; B3 DECLARED leaf with no citation; B4 jackscrew.length 950 with top_guide_z 1165; B5 member_length_rail 1230 |`

**l.139** (K table, K5 row).
Old: `a base_plate row admits one unfilled Polygon base_plate:outline only when the row carries K8 outline_matches (Designer sign-off r3, M1 S2 r2 N2) |`
New: `a base_plate row admits one unfilled Polygon base_plate:outline only when the row carries K8 outline_matches (Designer sign-off r3, M1 S2 r2 N2); 1.3 step 0: a Rectangle of zero width or height, or a Polygon of area <= 0.01 mm², on a row whose kind is not line, arrow or callout fails (TP1.1-9) |`
Old: `K5-B17 two plate outlines; K5-B18 plate outline without outline_matches |`
New: `K5-B17 two plate outlines; K5-B18 plate outline without outline_matches; K5-B19 zero-height Rectangle on the drill tube (TP1.1-9) |`

**l.140** (K table, K6 row).
Old: `the spec's `load_plane`, `entry_plane` (LF-16) and `stack_ties` (holder flange to collar top, LF1.1-1) must name the same z within 0.05 mm;`
New: `the spec's `load_plane`, `entry_plane` (LF-16) and `stack_ties` (holder flange to collar top, LF1.1-1; member tops: frame_upper_a, _b (S1, S2) and _c (S2) z_max - profile.height = term top_guide = jackscrew.top_guide_z, Loftsman 1.2 (b) NOTE 2, 1.3 step 0) must name the same z within 0.05 mm;`
Old: `K6-B9 S2 load_plane unequal to the S1 field that owns core_seat |`
New: `K6-B9 S2 load_plane unequal to the S1 field that owns core_seat; K6-B10 S1 member_length 1200 (ties a, b 13.00 apart); K6-B11 S2 member_length_rail 1210 (tie c 15.00 apart) |`

**l.141** (K table, K7 row).
Old: `in side views, per convex piece, the hull of that piece at the lowest and highest pose (a pair declared with `poses` only is swept as undeclared F, N excepted; Loftsman 1.2 (c) LF-c1, K7-B31),`
New: `in side views, per convex piece, the hull of that piece at the lowest and highest pose (a pair declared with `poses` only is swept as undeclared F, N excepted; Loftsman 1.2 (c) LF-c1, K7-B31; the moving row's neighbours and every fixed row's entries naming it are read, as in plan, Loftsman 1.2 (c) NOTE 1, K7-B34),`
Old: `B33 pinion|gear_hub at g_min 6 against the 5.22 toe gap (LF1.2-2) |`
New: `B33 pinion|gear_hub at g_min 6 against the 5.22 toe gap (LF1.2-2); B34 swept side view: the B4 member declared G against the ring at the last pose only, written on the member's row only, swept as F (Loftsman 1.2 (c) NOTE 1) |`

**l.142** (K table, K8 row).
Old: `stand_in counts only with a stand_in_owner, else a spec error (TP1.2-17);`
New: `stand_in counts only with a stand_in_owner that names a Step id (Step 2) or a sketch id (S3, s1 to s6), else a spec error (TP1.2-17, TP1.2-18); a sense predicate's `frame` value must be known (radial), else a spec error (Topologist 1.2 (c) NOTE 2);`
Old: `B40 -Y rail strips beside member c drawn dashed only; B41 stand_in without an owner |`
New: `B40 -Y rail strips beside member c drawn dashed only; B41 stand_in without an owner; B42 stand_in_owner "tbd"; B43 frame "polar" |`

**l.146** (K table control pointer).
Old: `Step 1.2 (h) r4 (`research/sean/cr_scratch/step1.2_engineer_revision_r4.md`) added K8-B37 to B41, K5-B17, K5-B18, K9-B7 (230 controls: Z 64, B 164, smoke 2; 734 s).`
New: `Step 1.2 (h) r4 (`research/sean/cr_scratch/step1.2_engineer_revision_r4.md`) added K8-B37 to B41, K5-B17, K5-B18, K9-B7 (230 controls: Z 64, B 164, smoke 2; 734 s). Step 1.3 step 0 (`research/sean/cr_scratch/step1.3_engineer_step0.md`) added RUN-Z, RUN-B, K2-Z2, K2-B4, K2-B5, K6-B10, K6-B11, RPT-Z, RPT-B1, RPT-B2, H1-B7, H1-B8, K5-B19, K8-B42, K8-B43, K7-B34 (246 controls: Z 67, B 177, smoke 2; 113 s at --jobs 12, 804.3 s at --jobs 1).`

**l.719** (Echo Site Registry, member tops row).
Old: `DERIVED; the tie is not yet a lint (both leaves read 1225 today); it lands before S3 (b) (Loftsman 1.2 (b) NOTE 2, detail 1.3 carried item 1) |`
New: `DERIVED; tied at 1.3 step 0: K2 expr agreement on top_guide_z, member_length, member_length_rail and K6 stack_ties member_top_a/_b (S1, S2), member_top_c (S2) to term top_guide (Loftsman 1.2 (b) NOTE 2; K2-B4, K2-B5, K6-B10, K6-B11); Loftsman sign at P0L |`

**Insertion after l.295** (detail 1.3). Line it follows, exact: `Sequenced at the 1.3 open (`research/sean/cr_scratch/step1.3_manager_open.md` section 1.1): step 0 (P0) carries item (1) with a K2 agreement lint for DERIVED overlay leaves (top_guide_z, member_length, member_length_rail are literals), item (5) as `--controls --jobs N` (target 200 s) and `--only`, item (6) as check RPT on spec field `reported_items`, and from item (3) TP1.1-9, TP1.2-18, Topologist NOTE 2 and Loftsman NOTE 1; P1R carries item (4) in plan with TP1.2-13 and TP1.2-19 and opens S2 r6; (c) carries TP-7 as a view per Axes, the section view for the screw Sean names, the renderer's section convention and S3-3 reading the accepted K7 records. S3-2 is red on the seeds (P_cr / F 2.23 capture lift, 1.05 stall at K = 1, SF 3, DERIVED at the open); its form goes to Sean at STOP S3-A before (b).`
New line: `Done at step 0 (P0, `research/sean/cr_scratch/step1.3_engineer_step0.md`; reviews P0L, P0T, P0S pending): item (1) member-top stack_ties plus K2 expr lint; item (5) `--jobs` (246 controls 113 s at 12 jobs) and `--only`; item (6) RPT and `reported_items`; from item (3) TP1.1-9 (K5 zero-area), TP1.2-18 (stand_in_owner id), Topologist NOTE 2 (frame value), Loftsman NOTE 1 (side sweep reads the fixed row). TP1.1-9 turns accepted S1 r7 K5 red (anchor thrust-bearing line drawn as a zero-height Rectangle, 8 issues); S1 r7 is not re-acceptable until that is resolved; S2 r5 17/17.`
