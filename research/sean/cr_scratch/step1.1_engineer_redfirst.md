# Step 1.1 (c) Engineer red-first, S1

## Corrections to the brief

1. **The P4 text for the S1-2 B is void.** The text says to set park `tip_z: upper.park_z` (959.84, the live defect). Under option R (Design Notes 22) 959.84 is the live park and passes S1-2 by 125.00. The gameplan l.229 replacement is used: park `tip_z: start_tip_max`, the top of the 650 mm travel. It fires at margin 0.00 (MEASURED). This is SW-10 as revised at 1.1 (b), correction 2.
2. **The P4 text for the S1-3 B is void.** The SW-10 form `park_tip - upper.load_clearance - 1` leaves a 66.34 margin under the collar-top park. The replacement is park `tip_z: core_stop + core.length_install + upper.load_clearance - 1`, which gives -1.00 (MEASURED). This is the 1.1 (b) correction 3, recorded in gameplan l.230.
3. **S1-4 and S1-5b already had Z and B controls from the (b) fix pass.** Those are S1-4-Z, S1-4-B1, S1-5b-Z and S1-5b-B1. S1-4 gains B2, the gameplan l.231 B (ring nut 100 above the top guide at park).
4. **The gameplan l.233 S1-5b B ("ring.position at the drill's lower third") cannot fire on the signed values.** The ring already sits 130 above the tip. The lower third is 266.67, which raises the ring and widens the 142.00 clearance. S1-5b-B1 (collar drawn 133 high, bearing 9 above the collar top) is the S1-5b B, and l.233 needs that text.
5. **The S1-1 Z sits on its upper bound.** The drawn reach is 650.00 against `upper.travel_max` 650, so the margin is 0.00 (DERIVED, stop.start_z[0] - stop.height_z). This is by construction, and S1-1 takes TOL.

Tags: control and stub results are MEASURED (run 2026-11-25). Fixture values are DERIVED from the signed spec and overlay.

## 1. Fixture table

All builders are in `research/sean/cr_scratch/sketches/fixtures/builders.py`, and all entries are in `fixtures/manifest.yaml`. Z is always `s1_live`: the signed spec, every row drawn from check_stack.

| ID | Z | B builder | Planted defect | Reason substring | Planted | Result |
|---|---|---|---|---|---|---|
| S1-1 | s1_live: 650.00 in [534.93, 650] | s1_1_b1 | `upper.travel_max` 500 (params value replaced) | "650.00 mm against [534.93, 500]" | 1 | Z clean, B fires 1 |
| S1-1 | | s1_1_b2 | spec start `tip_z: stop.height_z + upper.drill_advance_500core - 1` | "533.93 mm against [534.93, 650]" | 1 | B fires 1 |
| S1-2 | s1_live: +125.00 | s1_2_b1 | spec park `tip_z: start_tip_max` (SW-10, replacement) | "park: drawn tip 894.84 not above the highest class start 894.84" | 1 | Z clean, B fires 1 |
| S1-3 | s1_live: 367.34 / 117.34 | s1_3_b1 | spec park `tip_z: core_stop + core.length_install + upper.load_clearance - 1` (SW-10, revised) | "core.length_install: park tip - load_clearance - (core_stop + length) = -1.00" | 1 | Z clean, B fires 1 |
| S1-4 | S1-4-Z (b): 0.84 | s1_4_b1 (b) | top guides drawn 20 low | "load/screw a", "park/screw b", "high margin -5.84" | 4 | Z clean, B fires 4 |
| S1-4 | | s1_4_b2 | nut_a and nut_housing_a drawn with the nut 100 above guide_a top at park | "park/screw a", "high margin -155.00" | 1 | B fires 1 |
| S1-5a | s1_live: 192.34, need 25 | s1_5a_b1 | `drill.bore_ceiling_above_tip` 533.93 (advance - 1) | "capture-core (core_750) top at end of capture -73.73" | 1 | Z clean, B fires 1 |
| S1-5b | S1-5b-Z (b): 77 pairs, 142.00 | s1_5b_b1 (b) | collar drawn 133 high at capture_end | "bearing\|collar", "gap - g_min -1.000" | 1 | Z clean, B fires 1 |
| S1-6 | s1_live: 8 projections, 0 issues | s1_6_b1 | screw_b (theta 30) drawn at x = r = 160 in every pose (r cos 30 = 138.56) | "screw_b: drawn x 160.00, r cos(theta) 138.56 (theta 30)" | 4 | Z clean, B fires 4 |
| S1-7 | s1_live: 607.66, spare 72.73 | s1_7_b1 | core_750 row z_max `capture_core_bottom + core.length_capture` (0.5 m core as the capture core) | "357.66 mm, need 534.93 (short 177.27)" | 1 | Z clean, B fires 1 |

Hand values (DERIVED), all in z_A:
- **S1-2 B:** start_tip_max = stop_k 184.84 + 650 = 834.84, which is 894.84 z_S. The park is drawn at 894.84, so the margin is 0.00.
- **S1-3 B:** 42.50 + 750 + 50 - 1 = 841.50. The S1-3 margin is 841.50 - 50 - 792.50 = -1.00.
- **S1-5a B:** 184.84 + 533.93 - 792.50 = -73.73.
- **S1-7 B:** 42.50 + 500 - 184.84 = 357.66, which is 177.27 short of 534.93.
- **S1-4 B2:** guide_a top 1225 z_S at park. The nut is at 1325, against the high limit 1170, so the margin is -155.00.

SW-10: the S1-2 and S1-3 B fixtures mutate the spec pose `tip_z` and draw the mutated spec faithfully, so the drawn tip agrees with check_stack. S1-1-B2 and S1-7-B1 also mutate the spec, and S1-1-B1 and S1-5a-B1 replace a params or overlay value. S1-4-B2 and S1-6-B1 are drawing-only defects. S1-2 and S1-3 still cannot fail through the drawing. `_tip` raises a content red on any drawn tip that disagrees with check_stack, so a wrong drawing reds them for that reason, never for the park rule. They stay under the SW-10 rule.

## 2. --controls

`check_sketch.py --controls`: 98 controls. Z clean 30/30, B fired 67/67 (each on its reason substrings and planted count), smoke S1-FULL 1/1. Exit 0. Run time 91.3 s (68.5 s at 84 controls). The new controls are S1-1-Z, S1-1-B1, S1-1-B2, S1-2-Z, S1-2-B1, S1-3-Z, S1-3-B1, S1-4-B2, S1-5a-Z, S1-5a-B1, S1-6-Z, S1-6-B1, S1-7-Z and S1-7-B1 (14). The LF-16 controls K6-Z3, K6-B5 and K6-B6 match.

`check_sketch.py --stale`: 0 records, 0 differences.

## 3. Stub run, rev 0, signed spec

`check_sketch.py s1 --rev 0` on stubs/s1_stub.py (floor line only): exit 1. The results are in `s1_checks_r0.json` and `s1_summary_r0.md`, with spec status "signed (Designer, Loftsman; pose table confirmed by Sean 2026-11-25)".

| Check | Expected (baseline run 2) | Observed | Reason | Match |
|---|---|---|---|---|
| K1 | green (guard) | green | no literal, no soft key (s1_stub.py) | yes |
| K2 | green (guard) | green | 210 spec keys, 103 overlay leaves | yes |
| K3 | green (guard) | green | 4 figures conform | yes |
| K4 | red (content) | red (content) | no annotation per labelled row | yes |
| K5 | green (guard) | green | 4 tagged artists projected | yes |
| K6 | red (absent; content evidence run 1) | red (absent) | z_rule rows, nothing drawn | yes |
| K7 | red (absent; content evidence run 1) | red (absent) | pairs untestable, not drawn | yes |
| K8 | red (absent; content evidence run 1) | red (absent) | predicates untestable | yes |
| K9 | red (content) | red (content) | spec rows with no patch | yes |
| S1-1 | red (absent; content evidence run 1) | red (absent) | drill_head not drawn in pose start | yes |
| S1-2 | same | red (absent) | drill_head not drawn in pose park | yes |
| S1-3 | same | red (absent) | drill_head not drawn in pose park | yes |
| S1-4 | same | red (absent) | anchor_a not drawn in pose load | yes |
| S1-5a | same | red (absent) | bore_ceiling not drawn in pose capture_end | yes |
| S1-5b | same | red (absent) | ring not drawn in pose capture_end | yes |
| S1-6 | same | red (absent) | screw_a not drawn in pose load | yes |
| S1-7 | same | red (absent) | core_750 not drawn in pose start | yes |

Counts: 4 green (the K1, K2, K3 and K5 guards) and 13 red. Each red is labelled by cause: K4 and K9 content; K6, K7, K8 and S1-1 to S1-7 absent (fail-closed). Every absent red now has content evidence in run 1, because each S1-x B fires on content. No sketch check is green on the stub, so no check was rewritten.

`baseline_red.json` was rebuilt with `--baseline`. Run 1 is 30/30 Z, 67/67 B and 1/1 smoke; run 2 matches 17/17 on the signed spec. The 1.0 record is kept under `prior["2026-11-24T23:26:11 (spec draft, unsigned)"]`.

## 4. Changes to code

- **fixtures/builders.py**
  - `_s1_ctx` gains three arguments:
    - `spec_mut`: edits the spec before check_stack runs.
    - `values`: replaces a params or overlay value.
    - `xshift`: drawing-only x shift.
  - New builders: `_pose_tip`, `s1_1_b1`, `s1_1_b2`, `s1_2_b1`, `s1_3_b1`, `s1_4_b2`, `s1_5a_b1`, `s1_6_b1`, `s1_7_b1`.
- **fixtures/manifest.yaml:** 14 entries (section 2).
- **check_sketch.py**
  - The STUB_CAUSE label for S1-1 to S1-7 now reads "content evidence run 1, S1-x B fixtures 1.1 (c)" (was "content at 1.1 c").
  - `baseline()` keeps the prior baseline under a dated `prior` key.
- **No change to checks_s1.py, the spec or the overlay.**

## 5. Gameplan lines to change (orchestrator)

| Line | Change |
|---|---|
| l.144 control pointer | Add S1-1-Z, S1-1-B1, S1-1-B2, S1-2-Z, S1-2-B1, S1-3-Z, S1-3-B1, S1-4-B2, S1-5a-Z, S1-5a-B1, S1-6-Z, S1-6-B1, S1-7-Z, S1-7-B1. |
| l.233 S1-5b B | "Collar drawn 133 high at capture_end (bearing 9 above the collar top)". The lower-third ring B raises the ring on the signed values (ring 130 above tip vs 266.67) and cannot fire. |
| Design Notes 20 H6, SW-10 | H6 done at 1.1 (c). SW-10 applied with the 1.1 (b) replacement values. |
