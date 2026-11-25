# Step 1.0 revision: Wave 2 findings applied to the sketch harness

The three BLOCKs are fixed in code. Each has a new B control that fires on the defect, and every Z stays clean. Of the 22 FIX findings, 19 are fixed in code with a control. LF-6, LF-7 and TP-9 are fixed in the harness, and the design value each one needs goes to Sean or the Designer (section 6). Findings in more than one review are fixed once: LF-5 and TP-4 (depth bands); SW-4, SW-5 and TP-3 (K8 predicates); LF-15 with TP-1 (artist transforms).

Results, all MEASURED 2026-11-24:
- Run 1 (controls): Z clean 17/17, B fired 50/50, smoke 1/1. Each B fires with its planted reason substrings and its planted issue count.
- Run 2 (S1 stub, draft spec): 16/16 match. The red/green set is the same as Wave 1b; the reds now carry cause labels.
- Q3-0: 4/4 as expected.

## 1. Corrections to the brief

1. The Wave 1b notes say s1_spec.yaml has 35 feature rows. It has 37 (MEASURED).
2. Two instructions about baseline_red.json differ. The orchestrator says regenerate it only if the red set changed; spawn prompt 2.7 says overwrite it. I regenerated it for two reasons:
   - Run 1 went from 41 to 68 rows (new controls).
   - The run 2 expected labels changed under SW-7.
   The run 2 red/green membership did not change. The Wave 1b file is kept as `sketches/baseline_red_wave1b.json`.
3. The pose table (gameplan l.214) calls start "cutter at first contact". The params define it another way: `stop.start_z` source (params.yaml l.179) is "height_range + upper.travel_max 650", so start is defined by travel. The LF-7 contradiction is between that table wording and the params. See section 6, item 2.
4. Static plan pairs are now separated by their z bands, the same way side views use depth bands. The Wave 1b code tested every static plan pair as an overlap, which TP section 3 called conservative. Plan control Z5 (SW-6) needs the change. The reasoning carries over from depth bands: disjoint z bands mean the solids cannot meet.
5. The SW-8 smoke control runs K1 with no script, so K1 passes there with nothing to scan. The other 15 checks run on content.

## 2. Disposition

Finding counts by reviewer:
- SW: 1 BLOCK, 8 FIX, 8 NOTE.
- LF: 1 BLOCK, 6 FIX, 8 NOTE.
- TP: 1 BLOCK, 8 FIX, 5 NOTE.

Paths below are relative to `research/sean/cr_scratch/sketches/` (sc = sketch_common.py).

| ID | Class | Disposition | Change (file, function) | Control |
|---|---|---|---|---|
| SW-1 | BLOCK | ACCEPTED | s1_spec core_500, core_750: `on:` renamed `seat:`. sc `sense_lint`: a non-string or missing target key becomes one spec error per predicate, never an exception. sketch_loader `load_spec` rejects non-string keys in feature rows; check_sketch and check_stack load specs through it. Scratch spec with `on:` gives "REJECTED: ... row core_500 sense: key True" | K8-B9 |
| LF-1 | BLOCK | ACCEPTED | sc `assess_pair` (one judgement for K7 static, K7 swept and S1-5b). With band gap d > 0: F passes; C fails when d > 0.05; G passes when max(d, XZ distance) >= g_min - 0.05. Gameplan K table row l.140 reworded, B5 and B6 added (section 5) | K7-B5, K7-B6 |
| TP-1 | BLOCK | ACCEPTED | sc `_to_data`, `artist_polys`: every artist is measured through its full transform (T - transData, or T + transData inverse when the chain does not end in transData); Collection offsets included. Closes LF-15 | K8-B8 |
| SW-2 | FIX | ACCEPTED | manifest: every B carries `reason` substrings and `planted` count. check_sketch `compare` requires both; every check returns `n_issues` | all 50 B |
| SW-3 | FIX | ACCEPTED | sc `k4` finds the annotation by gid `label:<id>` | K4-B3 |
| SW-4 | FIX | ACCEPTED (with SW-5, TP-3) | builders: one-line mutations | K8-B4, K8-B5, K8-B6 |
| SW-5 | FIX | ACCEPTED (with TP-3) | sc `k8` predicate `side` (sign of x minus the target x, stated in the spec) and `outboard` ((x - x_target) cos theta > 0). s1_spec motor23_a `side` -1, motor23_b +1, both `outboard` of their pinion | K8-B7 |
| SW-6 | FIX | ACCEPTED | sc `k7` plan swept case: band gap of the swept z range against the member z band, through `assess_pair` | K7-Z5, K7-B8 |
| SW-7 | FIX | ACCEPTED | every result carries `cause` (absent or content). K6, K7 and K8 set absent when every issue is an undrawn part. checks_s1 `Absent` sets absent, `Content` sets content (SW-11). check_sketch `STUB_CAUSE`: run 2 expects "red (absent, fail-closed; content evidence run 1)" for K6, K7, K8 and "red (absent, fail-closed; content at 1.1 c)" for S1-x; a match needs the cause | run 2 |
| SW-8 | FIX | ACCEPTED | builders `s1_full_draw` draws every S1 row from check_stack. Control S1-FULL (check ALL, expected `runs`: none error, none absent). Per-check results recorded in controls_results.json as reported values | S1-FULL |
| SW-9 | FIX | ACCEPTED | s1_spec: the l.148 pairs written as neighbours (7 ring-assembly rows x 6 base parts, `group: S1-5b`, `poses: [capture_end]`, g_min 10). checks_s1 `s1_5b` reads the pairs and g_min from the spec and uses `assess_pair`. The hard-coded tables and 10.0 are removed | S1-FULL (42 pairs) |
| LF-2 | FIX | ACCEPTED | sc `stack_anchor_issues` in K6: sign anchors to_shop_floor(0) = +60, from_shop_floor(0) = -60, receiver_to_datum_a(0) = +40; collar_top_z_A equal to params `stop.collar_top_z` within 0.01; manifest hand numbers (floor 0, datum A 60, receiver floor 100, collar top 219.84 z_S) | K6-Z2, K6-B4 |
| LF-3 | FIX | ACCEPTED | sc `k7` swept: pieces paired by index across the lowest and highest poses, one hull per pair; mismatched piece counts are an issue | K7-Z6 |
| LF-4 | FIX | ACCEPTED | convexity guard inside `assess_pair`, so it covers static, swept and S1-5b | K7-B9 |
| LF-5 | FIX | ACCEPTED (with TP-4) | see TP-4 | K7-B7 |
| LF-6 | FIX | ACCEPTED, value to ruling | s1_spec `load_plane` {term, feature, edge, offset}. check_stack `park_tip_z_A` and checks_s1 `s1_3` both read it. Draft term core_stop (gameplan l.227). Park tip per plane and core length is reported (section 6, item 1) | none (one-datum refactor; S1-3 Z/B at 1.1 c) |
| LF-7 | FIX | ACCEPTED, value to ruling | core stop stays in one function (check_stack `core_stop_z_A`). Reported: start tip minus core top 292.34 mm; end tip + advance 719.77 z_A against core top 542.5 z_A (section 6, item 2) | none (reported) |
| TP-2 | FIX | ACCEPTED | sc `taper_issue`, predicate `taper` {narrows: up, down, inward, outward}. Added to collet (down, ASSUMED), gear (up), pinion_a and pinion_b (inward) | K8-B10, K8-B11 |
| TP-3 | FIX | ACCEPTED (with SW-4, SW-5) | spec field `place` {r_in, r_out, theta, half_width, footprint}. sc `k8` asserts drawn x centre = r_c cos theta in side views (x and y in plan) for every placed row: drill rows at r 0, pinions, motors, screws, nuts, anchors, guides, lift motors, guide member, frame members, descent stop. S1-6 reads r and theta from the place | K8-B7 |
| TP-4 | FIX | ACCEPTED (with LF-5) | check_stack `place_extents`: radial footprint gives y in [min(r_in s, r_out s) - w abs(c), max + w abs(c)] and x the same with s and c swapped; round footprint gives r ± w. The depth band is derived from the place. A spec band given beside a place is hulled with the true band and linted in K7. Gear band ±(PD/2 + face/2) = ±140 | K7-B7 |
| TP-5 | FIX | ACCEPTED | sc `k7`: every undeclared pair of drawn, measurable parts is tested as F. New class N (nested, declared, not measured). s1_spec `undeclared_pairs: F`; N declarations in the S1 spec are 1.1 (b) content (section 6, item 6) | K7-Z7, K7-B10 |
| TP-6 | FIX | ACCEPTED | sc `k5`: drawn class compared with spec `projection` on every row; spec lint requires axis X, Y or Z on cylinder, screw, cone and gear rows. sc `k9`: a Text satisfies a row only when the row kind is callout | K5-B4, K5-B5, K9-B3 |
| TP-7 | FIX | ACCEPTED | sc `k3`: more than one Axes without a spec `insets` declaration fails | K3-B7 |
| TP-8 | FIX | ACCEPTED | sc `k9` and `duplicate_ids`: a repeated row id fails | K9-B4 |
| TP-9 | FIX | ACCEPTED (harness), spec values carried to 1.1 (b) | sc `k8` predicates accept `poses`. The core_750 load z_rule (mid-insertion) and the rubric line "ring above the core" are spec content for the Designer (section 6, item 4); comment added at s1_spec core_750 | K8-Z2 |
| SW-10 | NOTE | carried | the 1.1 S1-2 and S1-3 B fixtures mutate the spec `tip_z` | — |
| SW-11 | NOTE | ACCEPTED | checks_s1 `_tip` raises `Content` | run 2 |
| SW-12, LF-14 | NOTE | no change | S1-6 depth half kept; it now checks check_stack's place derivation | — |
| SW-13 | NOTE | no change | accepted at 1.0 by the reviewer | — |
| SW-14 | NOTE | no change | — | — |
| SW-15 | NOTE | no change | step3_check.py unchanged; revisit with Q3-1 | — |
| SW-16 | NOTE | ACCEPTED | checks_s1: unused `ax` lines removed | — |
| SW-17 | NOTE | carried to S2 | K5 plan B written when S2 opens | — |
| LF-8 | NOTE | carried to 1.1 (a) or S2 | `frame_upper.radius` 300 still bends to the box test; XY footprint test once S2 exists | — |
| LF-9 | NOTE | no change | G passes at g_min - 0.05; the tolerance is stated in `assess_pair`. Spec-format statement at 1.1 (b) | — |
| LF-10 | NOTE | no change | signed sense lives in K8 and S1-5a | — |
| LF-11 | NOTE | no change | helpers draw two-point lines only (keep-out is drawn as two lines) | — |
| LF-12 | NOTE | ACCEPTED | check_stack `from_shop_floor`; `shop_floor_in_z_A` and the inline height_target conversion removed | K6 anchors |
| LF-13 | NOTE | carried to 4a | test_P18 literal 8 | — |
| LF-15 | NOTE | ACCEPTED via TP-1 | — | K8-B8 |
| TP-10, TP-11 | NOTE | TP-11 ACCEPTED: G failures print "gap - g_min" signed; TP-10 no change | — | K7-B3 reason |
| TP-12 | NOTE | carried to 1.1 | an unlabelled control pair is the Designer's call at the M1 gate; key.json stays out of the reviewer packet | — |
| TP-13 | NOTE | carried to S2 | place theta exists; K5 radial-axis plan rule at S2 | — |
| TP-14 | NOTE | ACCEPTED | `setup_figure` docstring: side views seen from -Y looking along +Y | — |

Defect reproduced against the Wave 1b check code. Wave 1b sketch_common was run on the new fixtures from a scratchpad snapshot; probe `scratchpad/old_vs_new.py`, MEASURED:
- K8-B9, `on:` spec: Wave 1b TypeError; revised fail, "core_500 rests_on: spec error, non-string key True".
- K7-B5: Wave 1b pass, "depth-separated"; revised fail, "C pair depth-separated by 490.000 mm".
- K7-B6: Wave 1b pass; revised fail, "band gap 1.000 mm ... lower bound 1.000, g_min 10".
- K8-B8 figure through K6: Wave 1b pass, "14 z_rule(s) match"; revised fail, drill_head drawn z [1088.47, 1194.84] against stack [244.84, 351.21]. Hand value: lo + hi - z with lo 244.84, hi 1194.84 gives head [1088.47, 1194.84]. Agrees.
- K4-B3: Wave 1b pass; revised fail on both cores.
- K7-Z6: Wave 1b false fire, overlap 20800 mm²; revised pass, distance 80.
- K7-B10, K5-B4, K9-B3, K3-B7: Wave 1b pass; revised fail.

Hand values beside code values:
- motor23_a band [-125.18, -37.82]; TP-4 hand [-125.2, -37.8].
- pinion_a band [-106.08, -18.92] = centre -62.5 ± 43.58; LF-5 hand half-width 43.58.
- screw_a band [76.0, 84.0]; LF hand [76, 84].
- gear band ±140.0; TP hand 140.
- Collar top 159.84 z_A, 219.84 z_S; K6-Z2 clean against hand 219.84.

## 3. Run 1: controls (`check_sketch.py --controls`)

Wave 1b controls are unchanged in fixture and outcome; the first table lists them by check. Every B now matches on its reason substrings and planted count.

| Check | Wave 1b controls | Observed |
|---|---|---|
| K1 | Z, B1, B2 | as expected |
| K2 | Z, B1 to B3 | as expected |
| K3 | Z, B1 to B6 | as expected |
| K4 | Z, B1, B2 | as expected |
| K5 | Z (now adds the mini side figure), B1 to B3 | as expected |
| K6 | Z, B1 (3 issues), B2, B2b, B3 | as expected |
| K7 | Z1 to Z4, B1 (3 issues), B2 to B4 | as expected |
| K8 | Z (now adds the taper figure), B1 (2 issues), B2, B3 | as expected |
| K9 | Z, B1, B2 | as expected |

New controls:

| Control | Expected | Observed | Issues / planted |
|---|---|---|---|
| K3-B7 | fires | fires | 1/1 |
| K4-B3 | fires | fires | 2/2 |
| K5-B4 | fires | fires | 1/1 |
| K5-B5 | fires | fires | 1/1 |
| K6-Z2 | clean | clean | — |
| K6-B4 | fires | fires | 1/1 |
| K7-Z5 | clean | clean | — |
| K7-Z6 | clean | clean | — |
| K7-Z7 | clean | clean | — |
| K7-B5 | fires | fires | 1/1 |
| K7-B6 | fires | fires | 1/1 |
| K7-B7 | fires | fires | 2/2 |
| K7-B8 | fires | fires | 1/1 |
| K7-B9 | fires | fires | 3/3 |
| K7-B10 | fires | fires | 1/1 |
| K8-Z2 | clean | clean | — |
| K8-B4 | fires | fires | 1/1 |
| K8-B5 | fires | fires | 1/1 |
| K8-B6 | fires | fires | 1/1 |
| K8-B7 | fires | fires | 2/2 |
| K8-B8 | fires | fires | 2/2 |
| K8-B9 | fires | fires | 1/1 |
| K8-B10 | fires | fires | 1/1 |
| K8-B11 | fires | fires | 1/1 |
| K9-B3 | fires | fires | 1/1 |
| K9-B4 | fires | fires | 1/1 |
| S1-FULL | runs | runs | — |

Totals: Z 17/17, B 50/50, smoke 1/1, exit 0.

S1-FULL reported results. These are reported values with no threshold; the draft spec is unsigned.

| Check | Result | Cause | Note |
|---|---|---|---|
| K1 | pass | — | no script |
| K2 | pass | — | 138 keys, 81 leaves |
| K3 | pass | — | — |
| K4 | pass | — | 45 labels |
| K5 | pass | — | 153 artists |
| K6 | pass | — | 145 z_rules, anchors clean |
| K7 | fail | content | 190 issues (187 undeclared, 58 unique pairs); 3 declared (see below) |
| K8 | fail | content | 6 issues: nut above guide at load, start and park |
| K9 | pass | — | 37 rows |
| S1-1 | pass | — | 650.00 against [534.93, 650] |
| S1-2 | pass | — | 50.00 |
| S1-3 | pass | — | margins 422.5, 172.5 over core_stop |
| S1-4 | fail | content | nut z 1281.0 against [105.0, 915.0] |
| S1-5a | pass | — | 442.34 against 25 |
| S1-5b | pass | — | 42 pairs, least 231.75 |
| S1-6 | pass | — | 8 projections |

The 3 declared K7 failures:
- ring|descent_stop C, open 19.81 mm.
- Swept ring|liftmotor_a and ring|liftmotor_b G, overlap 2016 mm² each.

## 4. Run 2: S1 stub (`check_sketch.py s1 --rev 0`)

| Check | Expected | Observed | Match |
|---|---|---|---|
| K1, K2, K3, K5 | green (guard) | green | yes |
| K4 | red (content) | red (content), "no annotation label:wingnut" ... | yes |
| K6 | red (absent, fail-closed; content evidence run 1) | red (absent) | yes |
| K7 | same | red (absent) | yes |
| K8 | same | red (absent) | yes |
| K9 | red (content) | red (content) | yes |
| S1-1 to S1-6 (7 rows) | red (absent, fail-closed; content at 1.1 c) | red (absent) | yes |

16/16. No red comes from a missing file.

Q3-0, re-run (step3_check_q30_results.json):

| Input | Exit | Result |
|---|---|---|
| empty | 1 | FAIL, "table has no rows" |
| Z | 0 | PASS |
| B | 1 | FAIL, "line 6 row 'B2': blank standin" |
| batch 1 | 0 | PASS |

Other checks:
- `--stale` on live files: 0 records, exit 0.
- `--stale --include-unaccepted` with a scratch overlay at `ring.thickness` 13: "STALE s1_checks_r0.json: ring.thickness recorded 12, live 13", exit 1.
- `check_stack.py`: exit 0.

Run times (MEASURED):
- `--controls` 42.1 s (68 controls, two PNGs; was 23.4 s for 41).
- `s1 --rev 0` 3.5 s.
- `--baseline` 2.1 s.

## 5. Diff against the Wave 1b baseline

- Run 1 grew from 41 rows (12 Z, 29 B) to 68 rows (17 Z, 50 B, 1 smoke).
  - Wave 1b rows: same observed outcome. Reason strings changed where a reason format changed: K7 G now prints "gap - g_min"; K4 names the gid.
  - Matching is stricter: reason substrings and issue count.
- Run 2 has the same 16 checks and the same red and green members.
  - Expected labels for K6, K7, K8 and S1-1 to S1-6 changed from "red (content)" to the absent labels.
  - Observed rows now carry their cause.
- Gameplan l.140, K7 row only:
  - "In side views a pair is tested only when its depth bands overlap; other pairs are listed "depth-separated"" was replaced. It now reads: disjoint depth bands settle F only; a C pair fails when the band gap exceeds 0.05 mm; a G pair passes when max(band gap, XZ distance) reaches g_min; pairs passed on the bands alone are listed "depth-separated".
  - B column: B5 and B6 appended.
  - The other new K7 controls (Z5 to Z7, B7 to B10) are in the manifest only; adding them to the gameplan is the orchestrator's call.

Files (line counts MEASURED):
- Changed:
  - sketch_loader.py 88
  - sketch_common.py 922
  - check_stack.py 224
  - check_sketch.py 281
  - checks_s1.py 140
  - s1_spec.yaml 590
  - fixtures/builders.py 607
  - fixtures/manifest.yaml 79
- Rewritten:
  - baseline_red.json 753
  - s1_checks_r0.json 708
  - s1_summary_r0.md 44
  - fixtures/controls_results.json 868
  - figs ctrl_a.png, ctrl_b.png: motor23_a now drawn at its placed x
- Kept: baseline_red_wave1b.json.
- Not changed: step3_check.py.

## 6. Values for Sean's or Quinn's ruling at the gate (harness uses the stated draft; nothing invented)

1. **Load plane for the park rule (LF-6).** Two candidates:
   - Draft: core_stop 42.5 z_A (gameplan S1-3 text).
   - params U13 (`upper.park_z`): collar_top 159.84 z_A.

   The two differ by 117.34 mm. Park tip z_A, DERIVED by check_stack:

   | Core length | core_stop plane | collar_top plane |
   |---|---|---|
   | 500 | 1015 | 1015 |
   | 750 | 1015 | 1015 |
   | 1000 | 1092.5 | 1209.84 |

   Sean or the Designer names the plane. The spec field `load_plane` takes it, and both the park rule and S1-3 follow.
2. **Start pose against the core stop (LF-7).** With the 0.5 m core on the 42.5 z_A stop:
   - Start tip 834.84 z_A sits 292.34 mm above the core top (542.5).
   - End tip + `upper.drill_advance_500core` = 719.77 z_A, which is 177.27 above that core top.

   `stop.start_z` is travel-derived (params l.179, Quinn's source). One of three things is wrong: the pose wording "first contact", `collet.core_seat_height` 2.5 above the receiver floor (ASSUMED), or the advance basis. Sean rules; Quinn is consulted on `stop.start_z` and the advance.
3. **Taper directions (TP-2).**
   - Collet narrows down: ASSUMED; ASSEMBLY.md does not state it.
   - Gear section narrows up: per `draw_gear_section`.

   The Designer confirms both at 1.1 (a).
4. **TP-9 spec content.**
   - The core_750 load z_rule (mid-insertion per the pose table) is not given.
   - The rubric line "ring above the core in every pose" is false at capture_end on the draft seeds: ring bottom 384.84 against core top 542.5 z_A, DERIVED.

   The Designer rewords the line or names the predicate.
5. **Draft radial geometry.**
   - The pinion z_rule is 30 mm tall (face width), while its diameter is 83.33 (module 4.1667 x 20, DERIVED).
   - The motor radial span is pitch radius 125 to 201, as in Wave 1b, which overlaps the pinion span 110 to 140.

   Designer, 1.1 (a).
6. **Smoke clashes for 1.1 (b).** All are on the unsigned draft:
   - 58 undeclared overlapping pairs, most of them nests to declare N (screw in nut, nut in ring, drill in ring and bearing, base stack). The pinion-tube and gear-screw pairs are box-test artefacts per LF-8.
   - Anchors inside the base plate: `jackscrew.anchor_z` 0 is the plate underside.
   - ring|descent_stop C open 19.81 mm: the stop sits at r 300, outside the ring footprint.
   - Ring sweeps through both lift motors.
   - Nut above guide at load, start and park; S1-4 fails. This is open item 1 of the Wave 1b notes: the draft overlay does not fit the lift.
