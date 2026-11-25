# Step 1.0 Wave 1b: sketch harness and red-first baseline

Run 1 (controls): Z clean 12/12, B fired 29/29, each B on its planted reason. Run 2 (S1 stub, draft spec): 16/16 match; K1, K2, K3, K5 green as guards; K4, K6, K7, K8, K9 and S1-1 to S1-6 red; no red from a missing file. K6, K7, K8 and S1-1 to S1-6 are red on the stub because the patches they measure are absent (a K9 reason); The Software Engineer rules on them (section 5). All counts MEASURED 2026-11-24.

## 1. Corrections to the brief

1. `drill.bore_ceiling_z` (gameplan l.121, l.147, l.229) is replaced by `drill.bore_ceiling_above_tip` 800 mm ASSUMED per Design Notes 19. check_stack.py computes `bore_ceiling = tip + drill.bore_ceiling_above_tip` per pose.
2. K6 frame text (gameplan l.139) is replaced by Design Notes 17. check_stack.py evaluates every z_rule in z_A and converts once in `to_shop_floor()` (z_S = z_A + `jig.datum_a_above_floor`). B2 plants 60 mm low (z_A), B2b 100 mm low (z_R).
3. Loader placement. Gameplan l.122 puts the loader in sketch_common.py; l.123 says check_stack.py imports the loader and no drawing helper. Both hold only if the loader is its own module: `sketch_loader.py` (stdlib and PyYAML), re-exported by sketch_common.py. The K6 import guard allows stdlib plus `sketch_loader`; anything else fires (B3).
4. `draw(feature_id, patch)` (l.122) has no axes argument. Implemented as `draw(feature_id, artist, ax=None)`; `ax` defaults to `plt.gca()`. Figures are built on `matplotlib.figure.Figure` (no pyplot state), so the harness passes `ax`.
5. Collet core-stop z has no params key. check_stack.py derives `core_stop = icd.floor_above_datum_a + collet.core_seat_height` = 42.5 z_A, ASSUMED (collet foot on the receiver floor). The Designer confirms it at 1.1 (a).
6. test_P18 (tests/test_params_bom.py 700) writes the nut plate as the literal 8. check_stack.py writes it from params: `nut.plate_thickness` 7.5 + `washer.thickness` 1.3 - `nut.washer_pocket_depth` 0.8 = 8.0 DERIVED. Collar top recomputes to 159.84 z_A, equal to `stop.collar_top_z` 159.84 (MEASURED, check_stack.py).
7. S1 controls marked "Live params" (S1-1 Z, S1-2 B, S1-3 Z) still need a drawn figure under ruling F3. None of the S1-x Z or B fixtures runs at 1.0; the JSON records them "not run at 1.0".
8. Gameplan Design Notes are numbered 17, 19, 18 in file order (lines 518-522). Cosmetic; orchestrator's file.

## 2. Files

All under `research/sean/cr_scratch/sketches/`. Line counts MEASURED.

| File | Lines | Content |
|---|---|---|
| proposed_params.yaml | 97 | overlay, 81 leaves, 13 namespaces; no params.yaml shadow (K2 live: clean) |
| sketch_loader.py | 71 | `Params` (params.yaml then overlay, leaf merge, params wins, shadows listed), path walk-up, SHA-256 |
| sketch_common.py | 632 | `setup_figure`, `draw`, drawing helpers, geometry (clip, min distance, hull), K1 to K9, `Ctx` |
| check_stack.py | 174 | frames, collar-top formula, draft park rule, per-pose stack names, z_rule evaluator, reported values |
| check_sketch.py | 237 | `sN [--rev k]`, `--stale [--include-unaccepted]`, `--controls`, `--baseline`, `--params`, `--overlay` |
| checks_s1.py | 130 | S1-1 to S1-6 (5a, 5b) on drawn patches by gid |
| s1_spec.yaml | 574 | DRAFT, `status: draft, unsigned`; header, four poses, 35 feature rows with every l.130 field |
| stubs/s1_stub.py | 16 | params, `setup_figure`, floor line at z_S = 0 per pose |
| fixtures/manifest.yaml | 47 | 41 controls: id, check, Z or B, expected, fixture, planted defect, gameplan line |
| fixtures/builders.py | 359 | one builder per control; mini side and plan specs; M1 control figures |
| fixtures/k1_*.py (3), k6_b3_check_stack.py | 16, 16, 19, 7 | AST-scanned fixtures |
| fixtures/k2_*.yaml (5) | 5 to 7 | K2 spec and four overlays |
| fixtures/figs/ctrl_a.png, ctrl_b.png, key.json | | K8 B1 (tip-up) and K8 Z at the end-of-capture pose, same title "side_xz: control figure"; mapping in key.json |
| fixtures/controls_results.json | 422 | run 1 |
| s1_checks_r0.json, s1_summary_r0.md | 655, 28 | run 2 |
| baseline_red.json | 476 | runs 1 and 2, 57 rows: ID, run, expected, observed, reason, match |

Order written: overlay, manifest, fixtures and builders, then loader, check_stack, sketch_common checks, check_sketch, stub, spec, checks_s1.

## 3. Run 1: controls (`check_sketch.py --controls`)

All MEASURED. Observed reason from controls_results.json.

| Check | Control | Expected | Observed | Reason (abridged) |
|---|---|---|---|---|
| K1 | Z | clean | clean | no literal outside {0, 1, -1, 2, 0.5} |
| K1 | B1 | fires | fires | k1_b1_literal.py:16 literal 152.4 |
| K1 | B2 | fires | fires | k1_b2_softkey.py:19 comparison with soft key jig.height_target |
| K2 | Z | clean | clean | 5 spec keys resolve; 3 overlay leaves clean |
| K2 | B1 | fires | fires | overlay key drill.tube_od shadows params.yaml |
| K2 | B2 | fires | fires | fx.ring_thickness: empty source |
| K2 | B3 | fires | fires | fx.ring_od: DECLARED without [CP §n, mm:ss] or [DN23] |
| K3 | Z | clean | clean | title, (mm) labels, equal aspect, grids, figsize, dpi 150 |
| K3 | B1 to B6 | fires | fires (6/6) | title lacks view; x label 'x'; aspect 'auto'; minor grid off; figsize (6.4, 4.8); dpi 100 |
| K4 | Z | clean | clean | 3 labels carry their key value |
| K4 | B1 | fires | fires | label 'tube OD' carries no number (want 152.4) |
| K4 | B2 | fires | fires | label 'tube OD 150' differs from drill.tube_od = 152.4 |
| K5 | Z | clean | clean | rectangle in XZ (normal Y), circle in XY (normal Z) |
| K5 | B1 | fires | fires | drill_tube cylinder axis Z in side_xz drawn as circle |
| K5 | B2 | fires | fires | pinion_a gear axis X in side_xz drawn as rectangle, needs trapezoid |
| K5 | B3 | fires | fires | untagged Rectangle |
| K6 | Z | clean | clean | 14 z_rules match within 0.05 mm; imports clean |
| K6 | B1 | fires | fires | drill_head, drill_tube, drill_top_block off 6.75 |
| K6 | B2 | fires | fires | core_500 drawn [42.50, 542.50] vs stack [102.50, 602.50] z_S, off 60.00 |
| K6 | B2b | fires | fires | core_500 drawn [2.50, 502.50] vs stack [102.50, 602.50] z_S, off 100.00 |
| K6 | B3 | fires | fires | import guard: k6_b3_check_stack.py:6 imports stubs |
| K7 | Z1 | F | clean, state F | distance 100 |
| K7 | Z2 | depth-separated | clean, depth-separated | bands [0, 10] and [20, 30] |
| K7 | Z3 | C | clean, state C | distance 0, overlap 0 |
| K7 | Z4 | clean | clean | 4 pose tests F, swept F; member 80 mm above the swept hull |
| K7 | B1 | fires | fires, 3 of 3 pairs | C, G, F pairs each overlap 100.000 mm² |
| K7 | B2 | fires | fires | C pair distance 1.000 mm |
| K7 | B3 | fires | fires | G pair distance 9.000 mm, g_min 10 |
| K7 | B4 | fires | fires | swept hull overlap 2000.000 mm² with the mid-stroke member |
| K8 | Z | clean | clean | 8 side predicates and 4 plan predicates hold, axes not inverted |
| K8 | B1 | fires | fires | drill_head below gear: centroid z 1141.7 vs 471.0; below top block: 1141.7 vs 319.8 |
| K8 | B2 | fires | fires | anchor_a below nut_a: centroid z 510.8 vs 450.8 |
| K8 | B3 | fires | fires | plan: axis inverted (y True) |
| K9 | Z | clean | clean | 14 rows drawn, no extra gid |
| K9 | B1 | fires | fires | spec row guide_member has no patch |
| K9 | B2 | fires | fires | tagged artist spare_bracket has no spec row |

Hand values beside code values (DERIVED by hand, MEASURED by code):
- K6 B1 shift 6.75 = `collar.top_above_plate`; code off 6.75. B2 60 = `jig.datum_a_above_floor`; code 60.00. B2b 100 = 60 + `icd.floor_above_datum_a` 40; code 100.00.
- K7 B1 overlap 1 x 100 = 100 mm² per pair; code 100.000. B4 member 200 x 10 inside the hull z 100 to 620 = 2000 mm²; code 2000.000. Z4 hull top p4 tip 500 + 100 + 20 = 620, member 700, gap 80 ≥ 10.
- Geometry spot checks (scratch run): two 10 x 10 squares offset 5: overlap 25.0 for CCW/CCW, CW/CCW, CCW/CW; contained 2 x 2 square: overlap 4.0, distance 0; shared edge: overlap 0, distance 0; corner gap (3, 3): 4.2426 = sqrt(18).

## 4. Run 2: S1 stub (`check_sketch.py s1 --rev 0`)

Spec `s1_spec.yaml` (draft, unsigned), script `stubs/s1_stub.py`, four poses.

| Check | Expected | Observed | Reason (abridged) | Match |
|---|---|---|---|---|
| K1 | green, guard | green | no literal, soft key or figure setting in s1_stub.py | yes |
| K2 | green, guard | green | 138 spec keys resolve; 81 overlay leaves clean | yes |
| K3 | green, guard | green | 4 figures conform | yes |
| K4 | red | red | 45 labels missing (first: load/wingnut 'wing nut sweep r') | yes |
| K5 | green, guard | green | 4 tagged lines (floor), nothing to project | yes |
| K6 | red | red | z_rules with nothing drawn (first: load/base_frame [0.00, 60.00] z_S); floor matches | yes |
| K7 | red | red | 53 pair tests untestable, parts not drawn | yes |
| K8 | red | red | 61 predicates untestable, parts not drawn | yes |
| K9 | red | red | 141 spec rows with no patch across four poses | yes |
| S1-1 | red | red | drill_head not drawn in pose start | yes |
| S1-2 | red | red | drill_head not drawn in pose park | yes |
| S1-3 | red | red | drill_head not drawn in pose park | yes |
| S1-4 | red | red | anchor_a not drawn in pose load | yes |
| S1-5a | red | red | bore_ceiling not drawn in pose capture_end | yes |
| S1-5b | red | red | ring not drawn in pose capture_end | yes |
| S1-6 | red | red | screw_a not drawn in pose load | yes |

No red from a missing file: every red reason names a spec row with no drawn patch.

## 5. For The Software Engineer to rule

- K6, K7, K8 and S1-1 to S1-6 are red on the stub only because the patches they measure are absent, which is a K9 reason. A floor-only stub cannot give them content to violate. Each has a B fixture that fires on content (run 1); S1-x have none until 1.1.
- Scratch evidence that S1-x compute on drawn patches (not a harness file; `scratchpad/s1_sanity.py` drew every spec row as a rectangle from check_stack values): S1-1 pass (650.00 against [534.93, 650]), S1-2 pass (park tip 50.00 above 965 z_A), S1-3 pass (margins 422.5 and 172.5), S1-4 fail (nut at load 1281.0 z_S outside [105.0, 915.0]), S1-5a pass (442.34 against 25), S1-5b pass (40 pairs, least 231.75), S1-6 pass (8 projections). MEASURED.
- `--stale`: no record is accepted, so the default run checks 0 records (exit 0). With `--include-unaccepted` and a scratch overlay copy setting `drill.length` 810: "STALE s1_checks_r0.json: drill.length recorded 800, live 810", exit 1. Against live files: 0 differences, exit 0. MEASURED.

## 6. Overlay seeds against batch 1

Each batch 1 stand-in is an overlay leaf with the same value: `drill.length` 800, `drill.mass` 8 kg, `drill.top_block_length` 150, `drill.top_block_od` 152.4, `drill.top_block_mass` 2 kg, `drill.head_od` 177.8, `drill.head_length` 106.369, `drill.bore_ceiling_above_tip` 800, `liftmotor.count` 3, `pinion.gearbox_ratio` 1, `drill.rpm` 60, `drill.torque_target` 10 N m, `gear.pitch_diameter` 250, `gear.bore` 180, `jig.datum_a_above_floor` 60; all ASSUMED. Q9, DN23-e, N5 to N9 are rulings with no leaf; Q9 enters the spec as `q9_length_keys` (500, 750). The other leaves (ring, bearing, guide, gear, pinion, jackscrew, liftmotor, hold, frame_upper) are seeds with no batch row; numbers with "no source" are ASSUMED working values. DECLARED leaves cite [DN23]: `pinion.count` 3, `pinion.motor_class` NEMA 23, `jackscrew.count` 3, `jackscrew.nominal` 8, `jackscrew.length` 900 (upper end of 800 to 900, reported, never asserted).

## 7. Run times (MEASURED, PowerShell Measure-Command)

| Command | Seconds |
|---|---|
| `check_sketch.py --controls` (41 controls, two PNGs) | 23.4 |
| `check_sketch.py s1 --rev 0` | 3.3 |
| `check_sketch.py --baseline` | 2.2 |
| `check_sketch.py --stale` | 2.7 |
| `check_stack.py` | 1.1 |

## 8. Open items for 1.1

1. The draft overlay does not fit the lift. Draft park rule (check_stack `park_tip_z_A`): park tip = max(max(`stop.start_z`) 965, core stop 42.5 + 750) + `upper.load_clearance` 50 = 1015 z_A. Lift stroke = 1015 - 184.84 = 830.16 mm DERIVED, above travel 650. With `ring.position_above_tip` 200, `jackscrew.anchor_z` 0 and `jackscrew.length` 900, the nut runs 390.84 to 1221 z_A against a usable screw band of 45 to 855 z_A (S1-4 fails in the scratch run). The fix is N1 (ring position), anchor height, screw length or the park rule. Sean and The Designer pick at 1.1 (a).
2. Highest point at load and park: 2025 z_S (top block top), margin to the 2000 mm soft target -25 mm. Reported, never asserted.
3. Core stop z 42.5 z_A (correction 5) needs the Designer's confirmation, or a params key.
4. Lift motor position (above the top guide) and guide rods at 0 and 180 deg are placeholders; S2 and S3 place them.
5. Side-view K7 is a box test on depth bands. Frame members at radius 250 would hit the 420 mm ring in XZ although they clear it by 10 mm radially; `frame_upper.radius` is set to 300 for that reason. The Loftsman reviews the box approximation against the S2 plan.
6. S1-x Z and B fixtures ("fixture from the spec", live params, live params.yaml park 959.84 for S1-2 B) are written at 1.1 after the spec is signed.
7. ctrl_a and ctrl_b carry the feature labels ("cutter OD ASSUMED 177.8" sits at the head wherever the head is drawn); no title or text names the good or bad figure. The mapping is in key.json; the reviewer receives the PNGs only.
