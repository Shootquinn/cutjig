# Step 1.3 P0f, The Engineer: step 0 fix pass

Date 2026-11-26. Inputs: `step1.3_loftsman_step0_check.md` (FIX 1), `step1.3_topologist_step0_check.md` (FIX 1, K5 ruling), `step1.3_software_engineer_step0_check.md` (FIX 1 to 4). Before the first edit the tree was copied to scratchpad `p0f/pre`; its 57 SHA-256 equal P0 `sha_after.txt`. That copy is "the P0 code" below. Branch-deletion runs (scratchpad `p0f/mut.py`) each use a fresh copy of the post-fix tree with one branch removed.

## Corrections to the brief

1. Four of the new B controls guard branches that the P0 code already has: RPT-B5 (value None), RPT-B6 (ABSENT row), and the RPT-Z2 and RPT-Z3 Zs. On the P0 code they match, because the defect they plant was already handled. Each one is shown red by deleting its branch from the post-fix code (M11, M5, M4). That is the Software Engineer's stated test ("red under the matching M mutation"). On the code before step 0 (`p0/pre`) they error, since that code has no `rpt_check`.
2. K5-B23 (collinear Polygon, SW FIX 4) fires on the P0 code with the P0 reason "zero-area Polygon (area 0.0000 mm2)". It mismatches there only on the new reason substring "least thickness". It is red under M10 (Polygon skipped by the thickness test): there K5 reads the projection mismatch instead.
3. The Software Engineer asked to show FIX 1 red "with the `not only` deleted". The routing is now `controls_dst`, so the matching deletion is `if live and not only` becoming `if live` (M1). RUN-B2 reads clean under M1.
4. The S1 r7 record's Z and B tally columns (`z_result`, `b_result`) are read from the last full controls run. Re-running s1 r7 and s2 r5 after the P0f controls run updates those columns (for example K2 "fired 3/3" to "fired 7/7"). Diff field list in section 7.

## 1. FIX items closed

| Raiser, item | Change | Controls |
|---|---|---|
| Loftsman P0L FIX 1 | `sketch_common.EXPR_REQUIRED`: when `jackscrew.top_guide_z`, `frame_upper.member_length` or `frame_upper.member_length_rail` is in the overlay, K2 fails if the leaf has no `expr` ("expr required (...)") or an expr other than the stated one after whitespace removal ("expr altered, has ..., required ..."). | Z K2-Z2 (unchanged, clean); B K2-B6 (no expr, length 950), K2-B7 (expr `jackscrew.anchor_z + 900`, length 950) |
| Topologist P0T FIX 1 (a), (b) | `zero_area_issue` tests every Patch on a row whose kind is not line, arrow or callout. `least_thickness` = least 2A/P over the artist's pieces in data coordinates (transform chain). Annulus: the radial width of the transformed rings. A piece with fewer than 3 vertices counts as 0. Fails at <= 0.05 mm. Reason: "zero-area <Type> (least thickness t mm <= 0.05) on a <kind> row (TP1.1-9)". K5-B19's substrings still match. | K5-B20 (S1 r7 anchor line 0.001 high, planted 8), K5-B21 (S2 screw_a Circle radius 0); Z K5-Z2, K5-Z3 |
| Topologist P0T FIX 1 (c) | Any non-Patch artist (Line2D, Collection) under an area row's own id fails: "<Type> on a <kind> row draws no area (TP1.1-9)". Sub-gids (`:ticks`, `:outline`) do not reach this test. | K5-B22 (prism row without projection, Line2D under nut_a) |
| Software Engineer P0S FIX 4 | Merged into the same K5 sequence: a degenerate Polygon goes through the thickness test. | K5-B23 (collinear 3-vertex Polygon under drill_tube) |
| Software Engineer P0S FIX 1 | `check_sketch.controls_dst(man_path, only)` is a pure function. It returns ("record", fixtures/controls_results.json) only for the full live manifest, ("partial", fixtures/controls_results_partial.json) for --only on the live manifest, and ("other", <manifest dir>/controls_results.json) for any other manifest. `controls()` uses it. An `--only` that selects nothing prints "no control selected" and exits 1 without writing. Also from NOTE 1: `--jobs` < 1 exits 2; rows not in manifest order exit 1. | Z RUN-Z2; B RUN-B2 (--only routes to partial), RUN-B3 (--only K2-b4: exit 1, partial file unchanged) |
| Software Engineer P0S FIX 2 | `--accept` refuses any record without an RPT row ("RPT absent"). The H1 template (`_template`) carries an RPT pass row, so H1-Z1 to Z3 stay clean. H1-B8 is re-planted as a record with no RPT row and no reported_items. Closes P0 open item 2. | H1-B8 (re-planted); H1-Z1 to Z3, H1-B1 to B7 unchanged |
| Software Engineer P0S FIX 3 | `rpt_check` reason ends "; cause <cause>", written from the cause field. | RPT-B3 (rev 0, needs_drawing item missing: "cause absent"), RPT-B4 (needs_drawing false: "cause content"), RPT-B5 (value None), RPT-Z2 (exempt path), RPT-Z3 / RPT-B6 (summary table rows; ABSENT) |

Topologist K5 mark admission (option A, M1 to M5, B-m1 to B-m5b): carried, lands with the S1 r8 drawing (section 9). `s1_side_poses.py` not edited.

## 2. K5 numbering (one sequence)

| Control | Covers | Raiser |
|---|---|---|
| K5-B19 | zero-height Rectangle on drill_tube (P0) | TP1.1-9 |
| K5-B20 | sliver Rectangle 42 x 0.001 (area 0.042 mm², passed the P0 absolute area test) on the S1 r7 anchors, 8 issues | Topologist FIX 1 (a) |
| K5-B21 | Circle radius 0 on screw_a (S2) | Topologist FIX 1 (a) |
| K5-B22 | Line2D under nut_a with projection deleted | Topologist FIX 1 (c) |
| K5-B23 | collinear Polygon under drill_tube | Software Engineer FIX 4 |

## 3. Thickness dry run on the live drawings

| Drawing | K5 | Note |
|---|---|---|
| S1 r7 (s1_side_poses.py) | fail 8, cause content: anchor_a and anchor_b bearing lines, least thickness 0.0000, at load, start, capture_end, park | the same 8 artists as P0; nothing else fires |
| S2 r5 (s2_plan.py) | pass, 105 artists | drill_tube annulus wall and screw circles included |
| fixture S1 (K5-Z2), fixture S2 (K5-Z3) | pass | |

## 4. Controls added

Counts: 246 + 15 = 261 (Z 67 + 3 = 70: RUN-Z2, RPT-Z2, RPT-Z3; B 177 + 12 = 189; smoke 2). H1-B8 re-planted in place, so it is not counted as new.

| ID | Planted | Reason substring | P0 code | Post-fix |
|---|---|---|---|---|
| K2-B6 | top_guide_z expr removed, length 950 | "overlay jackscrew.top_guide_z: expr required" | clean: "16 expr leaves agree"; mismatch | match yes |
| K2-B7 | top_guide_z expr `jackscrew.anchor_z + 900`, length 950 | "expr altered", "jackscrew.anchor_z + 900" | clean: "17 expr leaves agree"; mismatch | match yes |
| K5-B20 | anchor lines 0.001 high (S1 r7 script) | "anchor_a: zero-area Rectangle (least thickness 0.0010", "anchor_b: zero-area Rectangle", "on a prism row (TP1.1-9)"; planted 8 | clean: 343 artists; mismatch | match yes |
| K5-B21 | screw_a Circle radius 0 (S2) | "load/screw_a: zero-area Circle (least thickness 0.0000", "on a screw row (TP1.1-9)" | clean: 99 artists; mismatch | match yes |
| K5-B22 | Line2D under nut_a, projection deleted | "load/nut_a: Line2D on a prism row draws no area (TP1.1-9)" | clean: 296 artists; mismatch | match yes |
| K5-B23 | collinear Polygon under drill_tube | "load/drill_tube: zero-area Polygon (least thickness 0.0000", "on a cylinder row (TP1.1-9)" | fires with the P0 reason "(area 0.0000 mm2)"; mismatch on substring (Correction 2) | match yes |
| RUN-Z2 | full live manifest | (clean) | error: no controls_dst | match yes |
| RUN-B2 | --only "K1-Z,K2-*" on the live manifest | "not a record: --only routes to partial", "controls_results_partial.json" | error: no controls_dst | match yes |
| RUN-B3 | --only "K2-b4" (selects none) | "exit 1", "no control selected", "partial file unchanged" | clean: exit 0, partial file written; mismatch | match yes |
| RPT-B3 | rev 0, F_stall (needs drawing) missing | "reported item F_stall", "cause absent" | fires, reason without cause; mismatch | match yes |
| RPT-B4 | rev 0, L_min (needs_drawing false) missing | "reported item L_min", "cause content" | fires, reason without cause; mismatch | match yes |
| RPT-B5 | F_stall value None | "reported item F_stall", "no value" | match (branch exists; Correction 1) | match yes |
| RPT-Z2 | no reported_items, s1_checks_r7.json | (clean, "exempt") | match (Correction 1) | match yes |
| RPT-Z3 | write_summary with both values | (clean) | match (Correction 1) | match yes |
| RPT-B6 | write_summary with F_stall missing | "summary row F_stall reads ABSENT" | match (Correction 1) | match yes |
| H1-B8 (re-planted) | record without RPT row or reported_items | "refused", "RPT absent" | clean: accepted, flagged, copied; mismatch | match yes |

## 5. Branch deletion on the post-fix code (MEASURED)

| Mutation | Controls run | Result |
|---|---|---|
| M1 `controls_dst`: `if live and not only` to `if live` | RUN-Z2, RUN-B2 | caught: RUN-B2 clean ("routes to record") |
| M3 cause "absent" never set | RPT-B3, RPT-B4 | caught: RPT-B3 reason "cause content" |
| M4 RPT exemption removed | RPT-Z2 | caught: RPT-Z2 fires |
| M5 Reported items table removed | RPT-Z3, RPT-B6 | caught: both mismatch |
| M10 Polygon skipped by the thickness test | K5-B23 | caught: reason is the projection mismatch |
| M11 None counted as a value | RPT-B5 | caught: clean |
| M12 empty --only allowed | RUN-B3 | caught: exit 0 |
| M13 `--accept` RPT-row condition removed | H1-B8 | caught: accepted |
| M14 mandatory-expr loop removed | K2-B6, K2-B7 | caught: both clean |
| M15 non-patch clause removed | K5-B22 | caught: fires with the thickness reason instead of the "draws no area" substring |

SW M6 (RPT not appended in `run_sketch`) is still not caught by any control, since no control calls `run_sketch`. With FIX 2, a record written that way is refused at `--accept` ("RPT absent").

## 6. Runs from docs/sketches/

| Command | Exit | Wall | Result (MEASURED) |
|---|---|---|---|
| check_sketch.py --controls (default jobs 12) | 0 | 110.1 s | 261/261 matched: Z 70/70, B 189/189, smoke 2/2 |
| s2_plan.py --rev 5 | 0 | 10 s | PNG to wip/ |
| check_sketch.py s2 --rev 5 | 0 | 31 s | 17/17 + RPT pass (exempt) |
| s1_side_poses.py --rev 7 | 0 | 10 s | 4 PNGs to wip/ |
| check_sketch.py s1 --rev 7 | 1 | 18 s | 17/18 + RPT pass: **K5 fail, 8 issues, cause content** (anchor_a and anchor_b bearing lines at 4 poses, least thickness 0.0000); every other check passes |
| check_sketch.py --stale | 0 | | 2 records, 0 differences; X1 pass |
| check_sketch.py --stale --include-unaccepted | 0 | | 11 records, 0 differences |

The s2 and s1 runs came after the controls run, so their Z and B tally columns read the 261-control run. The last full controls run leaves `wip/fixtures/controls_results.json` with every control matched, as `--accept` requires. Serial `--jobs 1` was not re-run: the 15 new controls are fixture-only. P0's 804.3 s at 246 controls stands as the serial figure.

PNG equality (MEASURED): wip/s2_plan_r5.png is SHA-256 and pixel-equal to docs/sketches/s2_plan_r5.png. The four s1 r7 PNGs are also byte-equal.

## 7. Record diff and SHA-256

Record diff, wip/ against docs/ (MEASURED):

| Record | Differing fields |
|---|---|
| s2_checks_r5.json | accepted, accepted_at and accepted_note (absent in wip), timestamp, files_sha256.proposed_params.yaml; checks: RPT row added (pass, exempt); K2.reason (+ "17 expr leaves agree within 0.05"); tally columns K2.z_result (clean 1/1 to 2/2), K2.b_result (3/3 to 7/7), K5.b_result (18/18 to 23/23), K6.b_result (10/10 to 12/12), K7.b_result (33/33 to 34/34), K8.b_result (41/41 to 43/43) |
| s1_checks_r7.json | the s2 list, plus K7.reason, states and tests 5556 to 5557 (swept capture_end..park bore_ceiling|core_750 F, clean), plus **K5 result, cause, measured, n_issues and reason (red, 8)** |
| keys_read | equal on both |

SHA-256 of committed files under docs/sketches/ (57; wip/ and __pycache__ excluded). Before P0f equals P0 `sha_after.txt`. Changed by P0f: 5 files, all on purpose; unexpected differences 0. proposed_params.yaml, s1_spec.yaml, s2_spec.yaml and check_stack.py are unchanged since P0. Full hashes are in scratchpad p0f/sha_before.txt and p0f/sha_after.txt.

| File | Before (P0 after) | After |
|---|---|---|
| check_sketch.py | f13990a4c604aa68 | 72d126d68bde081f |
| fixtures/builders.py | cbed0420db785f33 | 47eb9356aec759be |
| fixtures/manifest.yaml | de0a1f5f428dfc3b | 591de03b2e9a23eb |
| fixtures/step0_fixtures.py | 6a4e230b4429ce87 | b11457a84fe01921 |
| sketch_common.py | a5a2d91e5b82234a | 79f7f8de9577994e |

## 8. ORCH-A accept command (s2 r5 only)

From `docs/sketches/`, after the P0f re-checks pass, with `wip/fixtures/controls_results.json` from the full run in section 6:

```
C:\Users\UR\AppData\Local\Programs\Python\Python312\python.exe check_sketch.py --accept s2 --rev 5 --note "Design Notes 13 S2-r5; records refreshed at 1.3 step 0"
C:\Users\UR\AppData\Local\Programs\Python\Python312\python.exe check_sketch.py --stale
```

Expected: exit 0. "replace s2_checks_r5.json: 5 differing field(s): accepted_at; accepted_note; checks; files_sha256.proposed_params.yaml; timestamp". "replace s2_summary_r5.md". "kept s2_plan_r5.png (byte-equal, kept)". The wip/ controls results and control figures are copied up (the committed `fixtures/controls_results.json` and `fixtures/figs/*` change here, by design). wip/baseline_red.json is kept or copied. Last line "accepted s2 r5". Then `--stale`: 2 records, 0 differences. S1 r7 stays the accepted record (docs copy unchanged) until S1 r8; `--accept s1 --rev 7` would be refused ("K5 fail").

## 9. Carried items

1. Topologist K5 mark admission rule (option A: `mark: {sub: line, z, source}`, M1 to M5; B-m1, B-m2, B-m3a, B-m3b, B-m4, B-m5a, B-m5b; fixture and live S1 r8 Z) lands with the S1 r8 drawing. The best pixel variant is 1 px off r7, so it cannot ride on r7.
2. SW NOTE 2 (tag vocabulary on reported items, `reported()` exception text into RPT), NOTE 3 (`K_CHECKS` control at S3 (c); per-Axes view in `run_sketch`), NOTE 5 (`--controls` has no output-location option, so runs of record are serialised through the orchestrator).
3. Topologist NOTE 1 (line-kind rows named at the S3 sign-off), NOTE 3 (`frame` admitted only on outboard when S3 adds sense rows).
4. `gear.pitch_angle` without expr (no atan in `eval_expr`).

## P0f addendum

Orchestrator ruling after the P0T and P0S re-checks (`step1.3_topologist_step0_recheck.md` FIX 1r; `step1.3_software_engineer_step0_recheck.md` FIX R1, NOTE 1, NOTE 3). Loop cap applies: the raisers sign from this dry-run table. Before the first edit the tree was copied to scratchpad `p0f2/pre`; its 57 SHA-256 equal the P0f "After" column.

Changes:
1. K5-B24 (Topologist FIX 1r, which is the same gap as Software Engineer FIX R1). Builder `k5_b24`: the S2 script drawing (`_script_ctx("s2")`) with the drill_tube Annulus wall set to 0.001 at load, outer radius kept. Planted 1. Reason substrings "load/drill_tube: zero-area Annulus (least thickness 0.0010" and "on a cylinder row (TP1.1-9)". This follows the Topologist's spec (wall 0.001, script drawing). The Software Engineer's variant (fixture drawing, wall 0.01) tests the same branch and is not added.
2. RUN-B4 (Software Engineer NOTE 1, taken as a fix). Fixture `run_b4` runs `controls()` in process, on a temporary one-row manifest (K1-Z) set as `cs.MANIFEST`, with `cs.output_path` pointed at a temporary directory. Both are restored in a `finally` block. It fires ("partial run") when an `--only` run writes the partial file and does not write the full-results path.
3. `zero_area_issue` docstring now states the thickness rule (least 2A/P in data coordinates, Annulus radial width, <= TOL_Z 0.05 mm) and the non-Patch clause (Topologist NOTE 1, Software Engineer NOTE 3).

Dry-run table (MEASURED; scratchpad `p0f2/red.py`; each case is a copy of the named code with the new fixtures and manifest added, run through that copy's `run_control` and `compare`):

| Case | K5-B24 | RUN-B4 |
|---|---|---|
| P0 code (`p0f/pre`) | clean, 0 issues, "105 tagged artist(s) projected"; **mismatch (red)** | fires, matched (the call site was correct at P0; RUN-B4 guards it) |
| P0f code before this addendum (`p0f2/pre`) | fires 1, matched (the branch exists; K5-B24 guards it) | fires, matched |
| fixed code with the Annulus branch disabled (`if False:`) | clean, 0 issues, "105 tagged artist(s) projected"; **mismatch (red)**. This reproduces the Topologist's `ann` row | fires, matched |
| fixed code with the call `controls_dst(man_path, None)` | fires, matched | clean: "partial file written False; full-results path written True"; **mismatch (red)** |
| fixed code (live tree) | fires 1, "load/drill_tube: zero-area Annulus (least thickness 0.0010 mm <= 0.05) on a cylinder row (TP1.1-9)"; matched | fires, "partial run: exit 0; partial file written True; full-results path written False"; matched |

Runs from `docs/sketches/` (MEASURED):

| Command | Exit | Result |
|---|---|---|
| check_sketch.py --controls (default jobs 12) | 0 | 263/263 matched: Z 70/70, B 191/191, smoke 2/2; 111.1 s |
| s2_plan.py --rev 5, check_sketch.py s2 --rev 5 | 0 | 17/17 + RPT pass (exempt); wip/s2_plan_r5.png SHA-256 and pixel-equal to docs/sketches/s2_plan_r5.png |
| check_sketch.py --stale | 0 | 2 records, 0 differences; X1 pass |

Counts: 261 + 2 = 263 (Z 70, B 189 + 2 = 191, smoke 2).

SHA-256 of committed files (57): before this addendum they equal the P0f "After" column. Changed: sketch_common.py (docstring only) 79f7f8de9577994e to 2e47d3615b4e879a; fixtures/builders.py 47eb9356aec759be to 3f15ad86870f851e; fixtures/step0_fixtures.py b11457a84fe01921 to 886e3d8b75d357ae; fixtures/manifest.yaml 591de03b2e9a23eb to ec8f6d28096ae715. Unexpected differences: 0. check_sketch.py is unchanged by the addendum.

The ORCH-A command in section 8 stands as written: `wip/fixtures/controls_results.json` is from the 263-control run, with every control matched.

## Gameplan lines to change

Old texts are the current gameplan (P0 lines applied). Each Old fragment is unique in its line.

**l.124** (detail 1.0, check_sketch.py bullet; the Software Engineer's hold released, FIX 2 landed).
Old: `` `--only <id globs or check ids>` writes `wip/fixtures/controls_results_partial.json`, "PARTIAL, not a record", never read by control_tally or `--accept`; runs of record use the full set.``
New: `` `--only <id globs or check ids>` writes `wip/fixtures/controls_results_partial.json`, "PARTIAL, not a record", never read by control_tally or `--accept` (destination from the pure function `controls_dst`, RUN-Z2, RUN-B2; its call site in `controls()`, RUN-B4); an `--only` that selects nothing exits 1 (RUN-B3); runs of record use the full set; per-control equality between job counts excludes the temporary-directory path in the H1-B5 reason (Software Engineer P0S).``
Old: `` `--accept` refuses through RPT and refuses a record declaring reported_items without an RPT row (RPT-Z, RPT-B1, RPT-B2, H1-B7, H1-B8; 1.3 open O10).``
New: `` `--accept` refuses through RPT and refuses any record without an RPT row; the RPT reason states its cause (RPT-Z, RPT-Z2, RPT-Z3, RPT-B1 to RPT-B6, H1-B7, H1-B8; 1.3 open O10; Software Engineer P0S FIX 2, FIX 3).``

**l.136** (K table, K2 row), Loftsman P0L FIX 1.
Old: `mandatory on jackscrew.top_guide_z, frame_upper.member_length, frame_upper.member_length_rail (1.3 step 0, O2) |`
New: `mandatory on jackscrew.top_guide_z, frame_upper.member_length, frame_upper.member_length_rail: a missing or altered expr on those three fails (1.3 step 0, O2; Loftsman P0L FIX 1) |`
Old: `B4 jackscrew.length 950 with top_guide_z 1165; B5 member_length_rail 1230 |`
New: `B4 jackscrew.length 950 with top_guide_z 1165; B5 member_length_rail 1230; B6 top_guide_z without expr, length 950; B7 top_guide_z expr altered (Loftsman P0L FIX 1) |`

**l.139** (K table, K5 row), Topologist P0T FIX 1 and Software Engineer P0S FIX 4. The mark admission clause is not included; it lands with S1 r8.
Old: `1.3 step 0: a Rectangle of zero width or height, or a Polygon of area <= 0.01 mm², on a row whose kind is not line, arrow or callout fails (TP1.1-9) |`
New: `1.3 step 0: on a row whose kind is not line, arrow or callout, a patch whose least drawn thickness 2A/P (Annulus: radial width) is <= 0.05 mm fails, and a Line2D or Collection under the row's own id fails (TP1.1-9; Topologist P0T FIX 1) |`
Old: `K5-B19 zero-height Rectangle on the drill tube (TP1.1-9) |`
New: `K5-B19 zero-height Rectangle on the drill tube (TP1.1-9); K5-B20 S1 anchor line 0.001 high; K5-B21 S2 screw circle radius 0; K5-B22 prism row without projection drawn as a Line2D; K5-B23 collinear Polygon on the drill tube (Software Engineer P0S FIX 4); K5-B24 S2 drill tube Annulus wall 0.001 (Topologist P0T re-check FIX 1r; Software Engineer P0S re-check FIX R1) |`

**l.146** (K table control pointer).
Old: `(246 controls: Z 67, B 177, smoke 2; 113 s at --jobs 12, 804.3 s at --jobs 1).`
New: `(246 controls: Z 67, B 177, smoke 2; 113 s at --jobs 12, 804.3 s at --jobs 1). Step 1.3 P0f (`research/sean/cr_scratch/step1.3_engineer_step0_fixes.md`) and its addendum added K2-B6, K2-B7, K5-B20 to B24, RUN-Z2, RUN-B2, RUN-B3, RUN-B4, RPT-Z2, RPT-Z3, RPT-B3 to B6 and re-planted H1-B8 (263 controls: Z 70, B 191, smoke 2; 111 s at --jobs 12).`

**l.665** (Design Notes 25, TP1.2-18/19 row).
Old: `stand_in_owner accepts any non-empty string;`
New: `stand_in_owner must name a Step or sketch id (1.3 step 0, K8-B42, signed P0T; overlay-key form deferred to S3 stand-ins);`

**l.666** (Design Notes 25, TP1.1-9 row).
Old: `| TP1.1-9 | A zero-height Rectangle passes K5 as "rectangle"; optional K5 lint for zero-area patches on non-line rows | 1.3 (S3), with TP-7 | The Topologist proposes; The Engineer |`
New: `| TP1.1-9 | A zero-height Rectangle passes K5 as "rectangle"; K5 zero-area lint landed at 1.3 step 0, thickness form per Topologist P0T FIX 1 at P0f (step1.3_engineer_step0_fixes.md); S1 r7 anchor bearing line (s1_side_poses.py l.230) fails 8 and is redrawn in S1 r8 as anchor_<s>:line under the K5 mark admission rule | 1.3 step 0 (P0f); S1 r8 | The Topologist proposes; The Engineer |`

**l.732** (Echo Site Registry, member tops row).
Old: `Loftsman sign at P0L |`
New: `signed by the Loftsman at P0L (research/sean/cr_scratch/step1.3_loftsman_step0_check.md), mandatory-expr rule FIX 1 at P0f (K2-B6, K2-B7) |`
