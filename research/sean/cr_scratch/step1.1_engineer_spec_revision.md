# Step 1.1 (b) Engineer spec revision, S1

## Corrections to the brief

1. **The P2 brief predates Design Notes 22.** Sean adopted option R after the Designer's review. Option R values replace the Designer's current-rule values:

   | Item | Designer 1.1 (a) value | Option R value (DECLARED, Sean) |
   |---|---|---|
   | jackscrew.length | 950 | 900, DECLARED [DN23] kept |
   | jackscrew.top_guide_z | 1215 | 1165 |
   | frame_upper.member_length | 1275 | 1225 |
   | park tip | 1015 | 959.84 z_A |
   | lift stroke | 830.16 | 775.00 |
   | highest point | 2025 | 1969.84 z_S |

   ring.position_above_tip 130, anchor_z 265, allowances 30/30/30 and collet.core_stop_z 42.5 are as the Designer set them.
2. **The S1-2 known-bad is retired (Design Notes 22).** The P4 text "S1-2 B sets park tip_z: upper.park_z (959.84, the live defect)" is void: 959.84 is now the live park and passes S1-2 by 125.00 (MEASURED, scratch run). The replacement B draws park `tip_z: start_tip_max`, the top of the 650 mm travel. That is the stroke-equals-travel conflation (SE-3, G3). It fires with a margin of 0.00 (MEASURED). S1-2 now requires the tip to be above the start by more than 0.05.
3. **The SW-10 S1-3 B no longer fires.** The SW-10 B is park `tip_z: park_tip - upper.load_clearance - 1`. The park is now set on the collar-top entry plane, 117.34 above the core stop that S1-3 reads, so that B leaves S1-3 a margin of 66.34 (MEASURED). Replacement: park `tip_z: core_stop + core.length_install + upper.load_clearance - 1`, which gives -1.00 and fires (MEASURED).
4. **LF-6's single `load_plane` field is split, per Design Notes 22.** `load_plane` (core stop 42.5, read by S1-3, G1) and `entry_plane` (collar top 159.84, read by the park rule). LF-16 lints both fields.
5. **Q9 options 1 and 2 coincide.** Under G2 the 0.75 m install core is the capture core and is loaded under every option (spec `always_loaded`). "0.5 m only" and "0.5 and 0.75 m" therefore share park 959.84, stroke 775 and L 900. That is the basis of Sean's 900 / 900 / 1140.
6. **Box-test artefacts (LF-8) would have kept K7 red at (d).** Nine pairs failed the side-view box test with real 3D clearance (section 6). The harness gained a plan-footprint lower bound with two Z controls and one B control. This is a K7 rule change for The Loftsman to rule on (open item 1).
7. **The TP-2 rulings flipped the harness fixtures.**
   - `draw_gear_section` now draws the teeth facing down; the mini spec gear predicate is "narrows down".
   - K8-B10 now plants the draft teeth-up section.
   - The taper fixture reads the collet as narrowing up, and K8-B11 plants the inverted cone.
8. **Parts of the ring shape note became their own rows.** The Designer's ring note draws bosses, standoffs and lugs inside the ring row. K6 compares a row's drawn z extent with its one z_rule, so the bosses (121 to 151 above the tip) cannot share the plate row (130 to 142).
   - New rows: `nut_housing_a/_b`, `motor_mount_a/_b`, `guide_lug_a/_b`. The `ring` row is the plate in section.
   - The pinion-shaft bushing blocks have no dimension, so they have no row (open item 3).
9. **The S1-5b least clearance is taken against the drawn wing-nut top.** The wing-nut top is 153.09 z_A; the collar top (159.84) is not a spec row. Result: bearing bottom 301.84 to wing nut, 148.75 (MEASURED), against the Designer's hand value of 142.00 to the collar top.
10. **K2 shadows at leaf level, not namespace level.** `sketch_loader.Params.shadowed` is the intersection of the flattened key sets. `collet.core_stop_z` is a new leaf beside the params `collet.*` leaves, and K2 reads clean (MEASURED, S1-FULL).

Tags: check_stack values are DERIVED. Values read from the S1-FULL smoke drawing and the control runs are MEASURED. Overlay design values are ASSUMED unless marked.

## 1. Files changed

All paths are under research/sean/cr_scratch/sketches/.

| Path | Change |
|---|---|
| proposed_params.yaml | Values from Designer section 3 with option R applied:<br>- ring.*: position_above_tip 130, clearance_bore 200 DERIVED, gear_seat, pinion_support, bearing_seat, motor_mount_height 23.5 DERIVED, guide_lug_r_out 250<br>- gear.*: od 252.64, toe_tip_above_pinion_axis 28.23, back_face_above_pinion_axis 62, hub<br>- pinion.*: R5 keys (11 leaves)<br>- jackscrew.*: anchor_z 265, length 900 DECLARED (source adds option R), top_guide_z 1165 DERIVED<br>- liftmotor.*: position below the anchor, coupling_length 25<br>- frame_upper.*: member_length 1225 DERIVED, stop_pad_r_in 195, stop_pad_r_out 215<br>- new leaf collet.core_stop_z 42.5 ASSUMED (G4)<br>Each changed leaf cites "Designer 1.1 (a)" and its basis. |
| s1_spec.yaml | Full revision (section 2 of the brief, items a to h). Header status: revised, awaiting Designer and Loftsman signatures. |
| check_stack.py | - `core_stop_z_A` reads collet.core_stop_z.<br>- `entry_plane` field.<br>- Option R park rule (`park_rule.stop_k`, `start_k`; `class_starts_z_A`, `class_stops_z_A`, `park_lengths` with `always_loaded`).<br>- Per-pose `vars`.<br>- `place` record carries r_in, r_out, half_width, footprint.<br>- `reported()` adds park and highest start, `q9_options` (park, stroke, L per `screw_length` expression) and the capture-core key. |
| sketch_common.py | - K6: LF-16 `plane_agreement_issues` (load_plane and entry_plane).<br>- K7: plan-footprint lower bound (`plan_footprint`, `plan_gap_fn`, `assess_pair(plan_gap=)`, state `plan-separated`).<br>- K8: predicates `clears_above` and `top_within` (TP-9 ring_on_tube).<br>- `draw_gear_section` draws teeth down (TP-2). |
| sketch_loader.py | `expand_neighbour_groups`: spec `neighbour_groups` with `{use: <group>}`; explicit row entries win. |
| checks_s1.py | - S1-2: start per class from the spec park rule; above by more than 0.05.<br>- S1-3: lengths include `always_loaded`; docstring names load_plane and entry_plane.<br>- S1-5a: reads spec `capture_core`; docstring "capture-core top".<br>- New S1-7 (capture reach from the drawn core top). |
| check_sketch.py | - S1-7 added to the stub red list, stub causes and sources.<br>- Summary prints park, entry plane and Q9 options. |
| fixtures/builders.py | - Mini gear "narrows down"; taper fixture collet "narrows up"; K8-B10 plants teeth-up.<br>- S1-FULL draws `section` rows per side, the cone per its taper predicate, the gear to gear.od, and the pinion trapezoid narrowing inward.<br>- New builders k6_z3, k6_b5 (LF-16), k7_z8, k7_z9, k7_b11 (plan bound), k8_z3, k8_b12, k8_b13 (ring_on_tube). |
| fixtures/manifest.yaml | - Eight new controls: K6-Z3, K6-B5, K7-Z8, K7-Z9, K7-B11, K8-Z3, K8-B12, K8-B13.<br>- K8-B10 and K8-B11 reasons follow the TP-2 ruling.<br>- S1-FULL description covers S1-7. |

Spec revision by brief item:
- a. `shape` on every row is the Designer's text. The rows split out of the ring (correction 8) carry shape strings written from his ring note.
- b. G1: `load_plane {term: core_stop, feature: core_seat, edge: z_max, offset: 0}`.
  - The `core_stop` term reads collet.core_stop_z.
  - The core_seat z_max is now the geometric expression `receiver_floor + collet.core_seat_height`, so LF-16 compares the leaf with the geometry. Before this change it was a tautology.
  - Design Notes 22: `entry_plane {term: collar_top, feature: wingnut, edge: z_max, offset: collar.top_above_plate}`.
- c. G2 pose table as the Designer's section 5:
  - Start purpose reads "top of the 650 mm travel".
  - Row core_500 is deleted.
  - core_750 is the capture core at load, start and capture_end (spec `capture_core: core_750`).
  - S1-5a refers to the capture-core top in the spec and in the checks_s1.py docstring.
- d. TP-9:
  - Load pose var `capture_core_bottom: collet.core_stop_z + 0.5 * (stop.collar_top_z - collet.core_stop_z)` gives 101.17, top 851.17 z_A (DERIVED).
  - `rests_on` applies to start and capture_end.
  - Rubric line as worded.
  - Predicate ring_on_tube: bearing `clears_above` drill_head, gear `top_within` drill_tube.
  - Motor rows: `top_within` gear (the "below the gear back face" addition).
- e. R5: pinion and NEMA 23 rows on his z_rules and places.
- f. R6: section 6.
- g. LF-9: header field `k7_tolerance` and comment. A G pair passes at distance >= g_min - 0.05 (`sketch_common.judge`, `_assess_pair`; TOL_C 0.05).
- h. Status as required.

## 2. check_stack table per pose (DERIVED)

Option R, Q9 stand-in. z_S = z_A + 60.

| Pose | Tip z_A (z_S) | Ring bottom z_A (z_S) | Nut z_A (z_S) | Anchor block z_A (z_S) | Guide block z_A (z_S) | Highest z_S | Margin to 2000 (reported) |
|---|---|---|---|---|---|---|---|
| load | 959.84 (1019.84) | 1089.84 (1149.84) | 1095.84 (1155.84) | 265 to 295 (325 to 355) | 1135 to 1165 (1195 to 1225) | 1969.84 (top block) | +30.16 |
| start | 834.84 (894.84) | 964.84 (1024.84) | 970.84 (1030.84) | 265 to 295 | 1135 to 1165 | 1844.84 | +155.16 |
| capture_end | 184.84 (244.84) | 314.84 (374.84) | 320.84 (380.84) | 265 to 295 | 1135 to 1165 | 1285.00 (frame member top) | +715.00 |
| park | 959.84 (1019.84) | 1089.84 (1149.84) | 1095.84 (1155.84) | 265 to 295 | 1135 to 1165 | 1969.84 (top block) | +30.16 |

Global terms (DERIVED):
- Planes: core_stop 42.5 (load_plane); collar_top 159.84 (entry_plane, test_P18 recompute equals params).
- Start and stop per class: highest class start 834.84; lowest stop 184.84.
- Park and stroke: park 959.84 (equals params upper.park_z); lift stroke 775.00.
- Load-pose core: 101.17 to 851.17. Its top sits 108.67 below the tip at 959.84.

Ring assembly at capture_end (z_A, DERIVED):

| Part | z_A |
|---|---|
| bearing | 301.84 to 326.84 |
| nut housing | 305.84 to 335.84 |
| pinion | 333.22 to 424.46 |
| NEMA 23 | 350.34 to 407.34 |
| gear | 407.07 to 440.84 |
| descent pad | 302.84 to 314.84, top = ring underside |
| lift motor | 192 to 240 |

S1-x on the S1-FULL smoke drawing (MEASURED; all pass):

| Check | Value |
|---|---|
| S1-1 | 650.00 within [534.93, 650] |
| S1-2 | +125.00 |
| S1-3 margins | 367.34 / 117.34 |
| S1-4 least margin | 10.84 |
| S1-5a | 192.34 |
| S1-5b | 66 pairs, least 148.75 |
| S1-6 | 8 projections, 0 issues |
| S1-7 | 607.66 against 534.93, spare 72.73 |

S1-7 planned B (scratch, MEASURED): the 0.5 m core as capture core gives 357.66, short 177.27, and fires. Z and B go into the manifest at (c).

## 3. S1-4 hand vs MEASURED

Band as coded:
- Low limit: 265 + 30 + 15 = 310.
- High limit: 1165 - 30 - 15 = 1120 z_A.

The Designer's section 4 table used L 950 and the current rule. His option R note gives band 310 to 1120, park nut 1095.84 and high margin 24.16. The hand column below is that note re-applied to each pose.

| Pose | Nut z_A, hand | Margin low, hand / MEASURED | Margin high, hand / MEASURED | S1-4 |
|---|---|---|---|---|
| load | 959.84 + 136 = 1095.84 | 785.84 / 785.84 | 24.16 / 24.16 | pass |
| start | 970.84 | 660.84 / 660.84 | 149.16 / 149.16 | pass |
| capture_end | 320.84 | 10.84 / 10.84 | 799.16 / 799.16 | pass |
| park | 1095.84 | 785.84 / 785.84 | 24.16 / 24.16 | pass |

K7 G gaps from the nut housing (MEASURED, swept and static):
- To the anchor block at capture_end: 10.84 (305.84 - 295).
- To the guide block at park: 24.16 (1135 - 1110.84).

## 4. Stroke and L per Q9 option (DERIVED; reported, never asserted)

Every option includes the always-loaded 0.75 m install core.

| Q9 option | Start per class z_A | Park z_A | Lowest stop | Stroke | L, S1-4 band as coded | L, detail 1.3 formula | L, Designer expression | L at anchor_z 265 | L to buy (Sean, Design Notes 22) |
|---|---|---|---|---|---|---|---|---|---|
| 0.5 m only | 834.84 / 834.84 (0.75 m loaded) | 959.84 | 184.84 | 775.00 | 865.00 | 895.00 | 885.00 | 885.84 | 900 |
| 0.5 and 0.75 m (stand-in) | 834.84 / 834.84 | 959.84 | 184.84 | 775.00 | 865.00 | 895.00 | 885.00 | 885.84 | 900 (drawn) |
| plus 1 m | 834.84 / 834.84 / 917.5 | 1209.84 | 184.84 | 1025.00 | 1115.00 | 1145.00 | 1135.00 | 1135.84 | 1140 |

The four L expressions (spec `screw_length`):

| Expression | Formula |
|---|---|
| S1-4 band as coded | stroke + 30 + 30 + 30 |
| detail 1.3 formula | S1-4 band + ring.nut_housing_height 30 |
| Designer expression | stroke + 30 + 30 + max(30, 30) + 2 x 10 |
| L at anchor_z 265 | park + 130 + 6 + 15 + 30 + 10 - 265 (the Designer's 885.84 / 1135.84 form, lower end carrying 10.84) |

The 1 m option needs stop_1000 = max(184.84, 42.5 + 1000 + 25 - 800) = 267.5, so start_1000 = 917.5. The drawn L 900 is too short for that option. Park by plane (reported): core_stop 884.84 / 884.84 / 1092.5; collar_top 959.84 / 959.84 / 1209.84.

## 5. --controls and --stale results

| Command | Result | Run time (MEASURED, Measure-Command) |
|---|---|---|
| `check_sketch.py --controls` | 76 controls: Z clean 21/21, B fired 54/54 (each on its reason substrings and planted count), smoke 1/1 | 51.4 s |
| `check_sketch.py --stale` | 0 records checked, 0 differences (no accepted revision) | 2.6 s |

At 1.0 the run was 41.3 s for 68 controls. Eight controls are new:

| Control | Fixture | Observed reason or state |
|---|---|---|
| K6-Z3 (LF-16) | live spec | clean |
| K6-B5 (LF-16) | collar-top plane named as core_stop | "LF-16 load_plane: term core_stop 42.50 z_A vs wingnut.z_max + offset 159.84 z_A, 117.34 apart" |
| K7-Z8 (LF-8, plan bound) | G 10 pair, plan gap 11 | plan-separated |
| K7-Z9 (LF-8, plan bound) | F pair, plan gap 11 | clean |
| K7-B11 (LF-8, plan bound) | G 10 pair at plan gap 9 | "plan footprints 8.979 mm apart ... gap - g_min -1.021" |
| K8-Z3 (TP-9 ring_on_tube) | correct sense | clean |
| K8-B12 (TP-9 ring_on_tube) | bearing slid onto the head | "bearing clears_above drill_head ... -5.00" |
| K8-B13 (TP-9 ring_on_tube) | gear 5 mm above the tube top | "gear top_within drill_tube ... -5.00" |

K8-B10 and K8-B11 fire on the ruled senses: "gear taper narrows down", "collet taper narrows up".

S1-FULL reports every K-check and S1-1 to S1-7 as pass on the revised spec. On that drawing the K7 states are:

| State | Count |
|---|---|
| F | 179 |
| C | 57 |
| N | 147 |
| depth-separated | 272 |
| plan-separated (declared) | 1 |
| undeclared F | 1488 |
| undeclared depth-separated | 685 |
| undeclared plan-separated | 24 |
| undeclared C | 18 |
| swept F | 26 |
| swept depth-separated | 68 |
| swept plan-separated | 2 |

The stub run (`s1 --rev 0`) was not executed: it rewrites s1_checks_r0.json, which belongs to (c).

## 6. R6 pair dispositions

The 1.0 smoke had 58 undeclared overlaps. On the revised spec and S1-FULL drawing, K7 has 0 failing tests (MEASURED).

**Class N declarations (real nests):**

| Group | Pairs |
|---|---|
| Base stack | receiver with collet, core_seat, holder, wingnut, core_750; collet with core_seat, holder, core_750; holder with wingnut, core_750; wingnut with core_750 |
| Screw in nut and blocks | screw_a/b with nut_a/b, anchor_a/b, guide_a/b |
| Nut and housing in ring | ring with nut_housing_a/b, nut_a/b, screw_a/b; nut_housing_a/b with nut_a/b and screw_a/b |
| Drill and core | core_750 with drill_head and drill_tube at capture_end only (607.66 of the core inside the bore) |
| Gear train | gear with pinion_a/b (mesh, Designer section 7); pinion_a/b with motor23_a/b (shaft 21 into the hub; plan gap of the bodies 2.00) |
| Guide rods | guide_lug_a with guide_member; guide_lug_b with guide_member_b (bushing on the rod) |

The drill was not nested in the ring and bearing. In section the bearing inner race touches the tube, so the pairs are declared C: drill_tube|bearing C and drill_tube|gear_hub C.

**Class C declarations:**
- base_frame|base_plate
- base_plate|receiver
- frame_upper_a/b|base_frame
- ring|bearing (outer race in the bore)
- ring|motor_mount_a/b
- ring|guide_lug_a/b
- motor_mount|motor23
- gear|gear_hub
- ring|descent_stop at capture_end. The pad is now at r 195 to 215, theta 150. The ring underside lands on it at 314.84, contact MEASURED. At 1.0 the stop sat at r 300 and the C pair was open by 19.81.

**G pairs:**
- core_750|bore_ceiling G 25 at capture_end: 192.34 (MEASURED).
- S1-5b group: 6 base parts against every ring-assembly row at capture_end, 66 pairs, least 148.75.
- fixed_g10 group (frame members, lift motors, anchor and guide blocks) against every moving ring-assembly row, static and swept.
- nut_housing_a|descent_stop G 10.

Lift-motor clearance (R6): the lift motors sit below the anchors at 192 to 240 z_A. The ring sweep from 301.84 up passes no lift motor. Anchors: the block at 265 to 295 sits 253 above the plate top. The 1.0 anchors-inside-the-plate defect is closed.

**Box-test artefacts (LF-8), passed by the new plan-footprint lower bound (MEASURED plan gaps):**

| Pair | Pose | Plan gap | Class |
|---|---|---|---|
| drill_tube\|pinion_a, \_b | all | 20.32 | F |
| gear_hub\|pinion_a, \_b | all | 6.52 | F |
| motor_mount_a\|pinion_a, b\|b | all | 2.00 | F |
| nut_a\|descent_stop | capture_end | 13.99 | F |
| nut_housing_a\|descent_stop | capture_end | 9.99 (true 10.00; the circumscribed 128-gon reads 0.01 low) | G 10, passes at the 9.95 tolerance; zero design margin |
| gear swept\|guide_a, \_b | capture_end to park | about 12.68 | G 10 |

**Declared N on an Engineer disposition, for the Designer to confirm (real 3D question):**
- base_plate|frame_upper_a/b: the 644 x 608 plate covers the screw frame members at r 300 (x -259.8, y 150).
- base_plate|guide_member/_b: the guide rod feet also sit inside the plate outline.

Both are declared N, "plate notched at the member (S2 footprint, LF-8)". Whether a base-frame member lies under (x -259.8, y 150) is not checked: frame_upper|base_frame C passes on the full-width box.

## 7. SW-18

K1 scans the spec `script:` path at rev >= 1:
- `check_sketch.py` `run_sketch`, l.179, picks the script: `HERE / "stubs" / f"{s}_stub.py" if rev == 0 else HERE / spec["script"]`.
- l.182 passes `script_paths=[script]` to the context.
- `sketch_common.k1` walks `ctx.script_paths`.

The spec reads `script: s1_side_poses.py`, so at (d) K1 scans that file. No code change was needed.

## 8. Gameplan lines to change (orchestrator, after STOP S-1)

| Gameplan line | Change |
|---|---|
| l.130 spec format | Add the fields `entry_plane`, `park_rule`, `always_loaded`, `q9_options`, `capture_core`, `capture_core_length`, `screw_length`, `k7_tolerance`, `neighbour_groups` (`{use: <group>}`), row `section`, pose `vars`. Add the predicates `clears_above` and `top_within`. |
| l.140 K7 row | Add "in side views the plan footprints from spec placement give a further lower bound: F passes at plan gap > 0.05, G when max(plan gap, XZ distance) >= g_min - 0.05 (state plan-separated)", with controls K7-Z8, K7-Z9, K7-B11. Only if The Loftsman accepts it. |
| l.141 K8 seed | Collet taper narrows up; gear tooth face below the back face, section narrows down; ring_on_tube (bearing clears_above drill_head, gear top_within drill_tube). |
| l.144 control pointer | Add K6-Z3, K6-B5, K7-Z8, K7-Z9, K7-B11, K8-Z3, K8-B12, K8-B13. |
| l.147-150 g_min seeds | As Designer section 10: bearing added to the keep-out exemptions; "0.5 m core top" becomes "capture-core top"; new pairs ring\|descent_stop C, nut housing\|descent_stop G 10, gear\|pinion N. |
| l.155 stub red list | Add S1-7. |
| l.210 Shows | Core list as Designer section 10; lift motors "below the anchors (placeholder)". |
| l.212-219 pose table | As the signed spec `poses` (manager open section 4 items 1 to 3). |
| l.221 lift stroke | "park tip minus the lowest stop tip over the supported classes, stop_k per option R". |
| l.222 Closes | Re-derives: add the option R expression (spec `park_rule.for_step4`). |
| l.229 S1-2 | Z: "signed spec (option R park rule)". B: "park drawn at the top of the 650 mm travel (stroke taken as travel)". Remove "Live params.yaml (959.84 below 965)". |
| l.230 S1-3 | B: "park tip at core stop + 0.75 m + upper.load_clearance - 1" (the SW-10 B leaves 66.34 under the collar-top park). |
| l.231 S1-4 | Add "with the nut housing against anchor and guide blocks at G 10". |
| l.232 S1-5a | "0.5 m core top" becomes "capture-core top". |
| New row after S1-6 | S1-7 (manager open section 4 item 5; values confirmed: 607.66 / 534.93 / spare 72.73; B 357.66, short 177.27). |
| l.236 Reported | Screw length "per spec screw_length expressions" until The Loftsman rules B3. |
| l.237 rubric additions | As spec `rubric_additions`. |
| l.284 detail 1.3 L formula | Per The Loftsman's ruling. |
| Design Notes 14, bullet 5 | "S1-2: park 959.84 below start 965" is no longer the live defect; S4-2 stands. |
| Design Notes 20, SW-10 row | The B values change (corrections 2 and 3). |

## 9. Open items for signature

1. **The Loftsman: K7 plan-footprint lower bound (LF-8 brought forward from S2 for placed and axis-Z round rows).**
   - Rule: 3D distance >= distance between the plan footprints. Footprints are circumscribed 128-gons for round parts, exact rectangles for radial parts, and the depth disk for section and axis-Z round rows without placement. Rows without a plan basis (plates, prisms without place) get no relief, and C pairs are never relieved.
   - Accept it, or revert it by dropping the `plan_gap` argument. If reverted, the nine pairs in section 6 fail K7 at (d) and (d) cannot go green.
2. **The Loftsman: screw-length expression (B3).** Four expressions are reported in section 4. The Designer argues the housing term is double-counted and that 2 x g_min 10 is missing.
3. **The Designer: rows split out of the ring (correction 8).**
   - guide_lug half_width = ring.guide_lug_r_out - guide.radius = 20 (my reading of his "bushing 20").
   - motor_mount footprint = the NEMA 23 footprint (r 142 to 218, half-width 28.5). It was not dimensioned in his review.
   - The pinion-shaft bushing blocks (ring.pinion_support) have no dimensions, so no row. Give them, or accept them as visual only.
4. **The Designer: base plate against the frame members and guide rods (section 6).** Declared N "plate notched" on my disposition. This is a real 3D question for S2, which also decides whether the r 300 members stand on a base-frame member.
5. **The Designer: second guide rod row `guide_member_b` added at guide.angle[1].** guide_lug_b needs a rod.
6. **The Designer: descent pad to nut housing is exactly 10.00 in plan (G 10, zero margin).** stop_pad_r_in 196 gives 1 mm of margin.
7. **The Loftsman: core_750|drill_head and |drill_tube N are restricted to capture_end.** K7's declared set is pose-blind, so the pair goes untested at load and start: gaps 108.67 and 42.34 (DERIVED). This is a harness limitation; no change.
8. **The Loftsman: S1-5b reference.** S1-5b is judged against the drawn wing-nut top 153.09 z_A, 148.75 to the bearing. The collar top 159.84 has no spec row; the Designer's hand value is 142.00.
9. **Carried ASSUMED:** Q2 (drill length 800, bore ceiling 800), Q9 stand-in (0.5 and 0.75 m), N10 floor offset 60. Batch 1 is unanswered.
