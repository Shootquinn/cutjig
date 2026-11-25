# Step 1.0 Wave 2: Software Engineer review of the sketch harness, fixture run, S1 stub run and Q3-0

Verdict: NOT SIGNED. Held by SW-1 (BLOCK) and SW-2 to SW-9 (FIX). Q3-0 (step3_check.py) passes review. 1 BLOCK, 8 FIX, 8 NOTE.

## 1. Re-runs (MEASURED 2026-11-24)

| Command | Exit | Result | Seconds |
|---|---|---|---|
| `check_sketch.py --controls` | 0 | Z clean 12/12, B fired 29/29 | 24.2 |
| `check_sketch.py s1 --rev 0` | 1 | 16 checks: K1, K2, K3, K5 pass; K4, K6, K7, K8, K9, S1-1 to S1-6 fail | 3.3 |

Against baseline_red.json: run 1, 41 of 41 rows with the same observed result and the same reason string; run 2, 16 of 16 the same. The re-runs overwrote fixtures/controls_results.json, s1_checks_r0.json, s1_summary_r0.md, figs/ctrl_a.png, ctrl_b.png and key.json with identical content and new timestamps. baseline_red.json was not rewritten.

Hand checks beside code values: capture-end tip z_S = `stop.height_z` 184.84 + 60 = 244.84, head top 244.84 + 106.369 = 351.21; code (K6-B1 reason) 244.84 and 351.21. Draft park tip = max(965, 42.5 + 750) + 50 = 1015 z_A; lift stroke 1015 - 184.84 = 830.16; code 830.16.

## 2. Ruling on reds caused by an absent patch (Engineer notes section 5)

K6, K7, K8 and S1-1 to S1-6 are red on the stub because the patches they measure are not drawn.

- **K6, K7, K8: ACCEPTED.** The stub can show one property of these checks, fail-closed on absent input. A K7 that skipped undrawn pairs would read green on the stub and on any sketch that leaves a part out. That would be a vacuous gate (Principle 10), and the stub run shows these checks are not one. Each check gives its own reason (K6 names z_rules, K7 pairs, K8 predicates), and none depends on K9: delete K9 and all three stay red. Content firing comes from run 1: K6 four B, K7 four B, K8 three B. I read the reason strings, and each fires on its planted defect (section 3). Gameplan l.153 "each for its own reason" is met on these terms.
- **S1-1 to S1-6: ACCEPTED as fail-closed evidence only.** No content red is shown for them at 1.0. They have no B fixture until the signed spec (Manager open, out of scope at 1.0). At 1.1 (c) the S1-x Z and B fixtures run, and each B must fire on its content reason before (d) begins. Until then the S1-x rows in baseline_red.json mean "fails closed" and nothing more.
- **Conditions.** An absence red hides a check that cannot run on its real input. SW-1 is that case: K8 throws a TypeError on any drawn S1 figure, and the stub red hides it. SW-7 (label the cause) and SW-8 (full-draw smoke control) are the conditions on this ruling.

## 3. Per-check test design (K1 to K9, S1-1 to S1-6)

| Check | Z real clean case | B plausible, fires for the planted reason | Stub |
|---|---|---|---|
| K1 | yes, a sketch-shaped script reading the loader | B1 `k1_b1_literal.py:16 literal 152.4`; B2 `:19 comparison with soft key` | guard, nothing to violate |
| K2 | yes | B1 shadow `drill.tube_od`; B2 empty source; B3 DECLARED without citation | guard; live overlay clean |
| K3 | yes, from setup_figure | six mutations, six named reasons | guard |
| K4 | yes | B1 no number, B2 150 against 152.4. Hole: SW-3 | red on content (labels absent) |
| K5 | yes, side and plan | B1 circle in XZ, B2 pinion rectangle, B3 untagged | guard (floor line only) |
| K6 | yes (drawn from check_stack, clean by construction; check_stack itself is the cross-review's) | B1 off 6.75 on the three drill rows only; B2 off 60.00; B2b off 100.00; B3 import of `stubs` | red, absent (ruling 2) |
| K7 | Z1 F, Z2 depth-separated (0 pair tests, correct), Z3 C, Z4 swept F | B1 three classes at 100 mm² each; B2 1.000 mm on C; B3 9.000 against 10; B4 swept 2000 mm². Plan swept path uncontrolled: SW-6 | red, absent |
| K8 | yes, side and plan | B1 head above gear and top block; B2 anchor above nut; B3 y inverted. rests_on, mirror, azimuth without B: SW-4; side predicate missing: SW-5; S1 spec crash: SW-1 | red, absent; hides SW-1 |
| K9 | yes | B1 guide_member absent; B2 spare_bracket untagged | red on content |
| S1-1 to S1-6 | not run at 1.0 | not run at 1.0 | red, absent (ruling 2) |

No check is green on the stub for a reason other than nothing to violate. No red comes from a missing file. run_sketch loads the stub and spec outside `safe()`, so a missing file raises a traceback and writes no JSON. It never produces a labelled red.

## 4. Q3-0 (step3_check.py), re-run

| Input | Exit | Result |
|---|---|---|
| step3_fixtures/q30_empty.md | 1 | FAIL, "table has no rows" (red-first) |
| step3_fixtures/q30_z_complete.md | 0 | PASS |
| step3_fixtures/q30_b_blank_standin.md | 1 | FAIL, "line 6 row 'B2': blank standin" |
| step1_quinn_batch1.md | 0 | PASS, 17 rows |

The B fires on its planted reason. Q3-1 has its own function and CLI branch (exit 2 until Step 3), so adding it does not touch Q3-0. Signed for Q3-0, apart from note SW-15.

## 5. Overlay against batch 1

All 15 numeric stand-ins are equal in the overlay, all ASSUMED: `drill.length` 800, `drill.mass` 8, `drill.top_block_length` 150, `drill.top_block_od` 152.4, `drill.top_block_mass` 2, `drill.head_od` 177.8 (= params `drill.cutter_od_7in`), `drill.head_length` 106.369 (= params `drill.kerf_standoff`), `drill.bore_ceiling_above_tip` 800, `liftmotor.count` 3, `pinion.gearbox_ratio` 1, `drill.rpm` 60, `drill.torque_target` 10, `gear.pitch_diameter` 250, `gear.bore` 180, `jig.datum_a_above_floor` 60 (= params `profile.height`). K2 on the live overlay: pass, 138 spec keys, 81 leaves. Shadowed leaves: none.

## 6. Structure

- Spec as the single feature table: K-checks read the spec rows. checks_s1.py hard-codes S1-5b's pairs and its 10 mm threshold (SW-9).
- check_stack.py imports: argparse, ast, json, math, sys, pathlib, sketch_loader. The K6 import guard reports none.
- setup_figure is the only place figsize, dpi, aspect and grid are set. The other hits are the K3 B mutations in fixtures/builders.py 207-219. K1 enforces the rule on sketch scripts.
- `--stale`: a scratch overlay copy with `ring.thickness` 13 (live 12) gives `--stale --include-unaccepted --overlay <copy>` exit 1 and "STALE s1_checks_r0.json: ring.thickness recorded 12, live 13". Against live files: exit 0, 0 differences. With no record accepted, the default `--stale` checks 0 records, exit 0.
- Relocation: the harness was copied to a scratch `docs/sketches/` with params.yaml two levels up. `check_sketch.py s1 --rev 0` there gives the same 16 results and hashes both files. No absolute path, no import from research/sean.

## 7. Ceremony gate

- S1-2 and S1-3 cannot fail through the drawing. `_tip` forces the drawn tip onto the check_stack tip, and `park_tip_z_A` (check_stack.py 71-75) builds both conditions into the draft rule. They fail only when the spec's pose `tip_z` changes. That is still the decision they guard (the park rule), so they stay. Their 1.1 B fixtures must mutate the spec (SW-10).
- S1-6's depth half tests the spec expression and no drawn coordinate, which is all a side view can carry. It fires on a wrong angle index in the spec, so it stays (SW-12).
- Nothing else qualifies. The `z_result` and `b_result` fields copy the run-1 tally, which l.124 requires. The six K3 mutations each cost one line.

## 8. Findings

**SW-1 BLOCK. K8 cannot run on any drawn S1 figure.** s1_spec.yaml lines 172 and 188 write `sense: [{pred: rests_on, on: core_seat, tol: 0.05}]`. PyYAML reads the YAML 1.1 boolean `on` as the key `True` (MEASURED: keys `['pred', True, 'tol']`). In sketch_common.py 704, `pr.get("on")` returns None, so `other` is None, and line 716 `extent_z(other)` raises `TypeError: 'NoneType' object is not iterable` (MEASURED: every spec row drawn from check_stack values, `k8(ctx)` raised). The stub red hides it because `me` is empty first. The builders' mini spec is a Python dict with a string key, so K8-Z exercises rests_on and passes. Fix: rename the field (`seat:`) or quote `"on"`. In k8, a predicate whose target key is missing is a spec error that names the row and the key, and is never an exception. The spec loader rejects non-string keys in sense rows.

**SW-2 FIX. The controls compare exit state only.** check_sketch.py 85-97 `compare()` counts any `fail` as "fires". A B that fires for a different reason (an untestable pair, a second unplanted issue) reads as a match. Today every B reason is the planted one (section 3, read by hand). That holds only until the next edit to the check. Fix: each manifest B entry gets `reason:` (a substring of the expected reason: the feature id and the measured term, e.g. `"core_500"` and `"off 60.00"`). compare() requires it, and a B whose failing count exceeds its planted count is a mismatch.

**SW-3 FIX. K4 matches labels by text substring, not by feature.** sketch_common.py 490-498. In s1_spec.yaml, core_500 and core_750 share label text `core`. A figure with "core 750" on core_500 and "core 500" on core_750 passes K4 (MEASURED probe: `pass, 2 label(s) carry their key value`). A label on the wrong part is a plausible defect. Fix: K4 locates the annotation by gid `label:<id>` (place_labels already sets it, line 147) and checks the text and number on that annotation. Add B3: swapped core labels.

**SW-4 FIX. Three K8 predicate kinds have no known-bad control.** rests_on, mirror_about_axis and azimuth run on the K8 Z fixtures and on no B (manifest.yaml 49-52). Principle 9: a detector never shown to fire carries no information. Each B is a one-line mutation in builders.py:
- B4 core_500 lifted 1 mm off core_seat. MEASURED on the mini spec: K8 fires, "bottom minus seat top 1.000 mm".
- B5 one gear trapezoid shifted 1 mm in x.
- B6 screw_b drawn at `jackscrew.angle[2]`.

**SW-5 FIX. The K8 library lacks the seed predicate "motors on the side of the gear the spec states"** (gameplan l.141; S1 rubric addition "the motors sit on the same side of the gear in every pose"). k8 knows below, above, rests_on, mirror_about_axis and azimuth. s1_spec.yaml motor23_a and motor23_b carry only `above ring`. Fix: add a `side` predicate: sign of (centroid x minus the axis feature's centroid x), stated in the spec. Add a B with one motor mirrored to the other side, and put the predicate on both motor rows.

**SW-6 FIX. K7's plan-view swept path has no control.** sketch_common.py 664-669: in plan, a fixed member whose z band misses the sweep is skipped. The skip can mask a hit, and no Z or B runs through it (Z4 and B4 are side_xz). K7 is signed at 1.0 for all six sketches, and S2 is a plan sketch. Fix: plan Z5, a member inside the ring outline with its z band above the sweep, reads clean (skip taken). Plan B5, the same member with its z band inside the sweep, fires.

**SW-7 FIX. baseline_red.json labels absence reds as content reds.** check_sketch.py 228-230 writes `expected: "red (content)"` for K6, K7, K8 and S1-1 to S1-6, but their reasons are "nothing drawn", "untestable" and "not drawn". Fix:
- Each result dict gets `cause: absent | content`. K6, K7, K8 and checks_s1 `Absent` set `absent` when the only issues are undrawn rows.
- Run 2 expected becomes "red (absent, fail-closed; content evidence run 1)" for K6, K7, K8 and "red (absent, fail-closed; content at 1.1 c)" for S1-x.
- 1.1 (d) can then tell when a check first meets real content.

**SW-8 FIX. No control runs the checks on the S1 spec with every row drawn.** The Engineer's scratch `s1_sanity.py` does this and showed S1-4 failing on content. It was never turned into a harness control, and that is how SW-1 got through. Fix: move it to `fixtures/builders.py::s1_full_draw`. `--controls` runs K1 to K9 and S1-1 to S1-6 on it. Expected per check: result pass or fail, never `error`, never `cause: absent`. The observed results are recorded as reported values, with no thresholds; the draft overlay does not fit the lift (open item 1), so S1-4 is expected to fail.

**SW-9 FIX. S1-5b keeps its own pair table.** checks_s1.py 117-118 hard-code RING_ASSY (7 ids) and BASE (6 ids), and line 122 hard-codes `need = 10.0`. The spec carries the l.148 ring-assembly pairs on `ring` only, against wingnut, holder and receiver. Collet, base_plate and base_frame are missing, and bearing, gear, pinions and motors have no neighbours. K7 and S1-5b therefore test different pair sets with g_min in two places (Design Notes 14: one table). Fix: write the l.148 pairs into the spec as neighbours with `poses: [capture_end]`, `g_min: 10`, source l.148. S1-5b reads them from the spec (or filters the K7 results for them) and takes g_min from the rows.

**SW-10 NOTE.** S1-2 and S1-3 are true by construction under the draft park rule (section 7). At 1.1 their B fixtures mutate the spec pose `tip_z`: S1-2 B sets park `tip_z: upper.park_z` (959.84, the live defect, Design Notes 14). S1-3 B sets `park_tip - upper.load_clearance - 1`.

**SW-11 NOTE.** checks_s1.py 43-44 reports a drawn tip that disagrees with check_stack as `Absent` ("measured: none"). It is a content disagreement, and K6 also reports it. Label it `cause: content` under SW-7.

**SW-12 NOTE.** The S1-6 depth half (checks_s1.py 151-156) compares the spec's depth expression with r sin(theta). It tests the spec, which is the only depth information a side view has. Keep it.

**SW-13 NOTE.** The K1 soft-key test (sketch_common.py 390-393) finds the key string inside a Compare node. `h = get("jig.height_target"); assert top < h` passes. Accepted at 1.0. If a sketch script ever does this, the check gains a name-binding pass.

**SW-14 NOTE.** K2 accepts source "no source" (sketch_common.py 431). That is consistent with ASSUMED as a working value. DECLARED leaves still need [CP] or [DN23], and B3 shows that rule fires.

**SW-15 NOTE.** Q3-0 (step3_check.py 101-106) passes a stand-in that reads only "ASSUMED" with no value, and passes duplicate IDs. Batch 1 has neither: 17 unique IDs, each stand-in with a value. Revisit when Q3-1 is written.

**SW-16 NOTE.** checks_s1.py 123 and 137: `ax` is assigned and deleted unused. Delete both lines.

**SW-17 NOTE.** The K5 plan path has a Z (circle in XY) and no B. B1's comparison code covers it. Add a plan B (cylinder axis Z drawn as a rectangle in plan) when S2 opens.

NOT SIGNED (harness, fixture run, S1 stub run): SW-1, SW-2, SW-3, SW-4, SW-5, SW-6, SW-7, SW-8, SW-9. step3_check.py Q3-0: SIGNED.
