# Step 1.1 (h) Engineer revision, S1 r4 (from the r3 re-checks)

Sources: the Loftsman and Topologist r3 re-checks, as relayed by the orchestrator (LF1.1-8 = TP1.1-12, TP1.1-11, the l.140 wording, the gear|guide-arm lower bound). Drawn and check values are MEASURED (run 2026-11-25). Hand values are DERIVED.

## Corrections to the brief

1. **"Member turned 45 deg" needs a spec field.**
   - A radial footprint has no orientation of its own, so the B control cannot be stated in the r3 spec.
   - New optional `place.rot` (deg): the radial footprint is turned about its own centre. Both check_stack.place_extents (side-view x and depth) and sketch_common.plan_footprint read it, through one function, check_stack.radial_corners.
   - rot 0 reproduces the r3 extents exactly. The live spec uses no rot.
2. **K7-B20 fires 8 times.** Both arms of member a meet its turned corner, in four poses. The expected overlap is 12.43^2 = 154.4 mm2 (hand: 300 - 30 sqrt 2 = 257.57, 270 - 257.57 = 12.43). MEASURED: 154.416 mm2.
3. **The square member makes ring|frame_upper pass in plan only.**
   - In the side view the member box now starts at x -218.83, 8.83 from the ring rim (x -210), against g_min 10.
   - The pair passes on the plan gap 59.94 (hand 270 - 210 = 60; the ring's 128-gon footprint reads 59.94).
   - In r3, with the round footprint, the side-view gap was 19.81. The member's true section is wider in projection than r3 drew it.
4. **The shaft widening is "15 at each end".** The brief's "shaft 15 wider" was read the same way as the arm's "20 wider at each end", so the centre is unchanged and only the extent check can see it.

## Correction table

| ID | Finding | Fix | Predicate / rule | Z / B |
|---|---|---|---|---|
| LF1.1-8 = TP1.1-12 | frame_upper placed as a circle r 30; the 30-6060 member is a 60 x 60 square (circumradius 42.43) | frame_upper_a/_b `place`: radial footprint r_in frame_upper.radius - profile.width / 2 (270), r_out + profile.width / 2 (330), half-width profile.width / 2 (30), one face toward the axis. Drawn x -300.79 to -218.83, 81.96 wide, at theta 150 (hand: 330 cos 150 - 15 = -300.79; 270 cos 150 + 15 = -218.83). Arm\|member plan-contact reads distance 0.000, plan overlap 0.000 (r3: 0.003, 128-gon artefact). | K7 C plan-contact on the true section; `place.rot` | Z: K7-Z10 (live). B: K7-B20, member a rot 45, "bracket_anchor_a\|frame_upper_a C", "bracket_guide_a\|frame_upper_a C", "overlap 154.416 mm2", planted 8 |
| TP1.1-11 | plan-contact judges spec footprints only; an arm drawn 20 wider at each end, or a shaft 15 wider, passes | K8 TP-3 now also checks `projected_extent`: the whole drawn x extent of every placed row lies inside the spec footprint's projected x (TOL_Z 0.05). In plan views it checks y as well (`projected_extent_y`). | K8 projected_extent | Z: K8-Z5 (live S1, every placed row inside its footprint). B: K8-B15, bracket_anchor_a +20 each end, "(by 20.00)", planted 4. B: K8-B16, motor_shaft_a +15 each end, "(by 15.00)", planted 4 |
| LF (r3 re-check) | gear\|guide-arm lower bound reported as 15.43; true plan lower bound 54.65 | Reported values corrected (table below) | reported only | none |

Red first, run against a copy of the r3 code and spec with no files written in the project:
- K7-B20 reads K7 clean. The rot field is ignored there and the round footprint is tangent.
- K8-B15 and K8-B16 read clean on both K8 and K7.

## Gameplan l.140 wording (for the orchestrator; gameplan not edited)

Replace the side-view plan clause of l.140 with:

> "Side views: every placed row's plan footprint contains its whole part, as a true section with no circumscribing circle for a non-round part (a 30-6060 member is a 60 x 60 square, one face toward the axis), and K8 projected_extent checks that the whole drawn part lies inside the footprint's projection. On that containment, an F pair passes when the footprints are more than 0.05 apart, and a G pair passes when max(plan gap, projected distance) >= g_min - 0.05 (plan-separated). A C pair whose side-view pieces overlap passes when both rows are placed and their footprints touch (distance <= 0.05) without overlap (area <= 0.01) (plan-contact). Controls: K7-Z8, Z9, Z11, B11, B16, B17, B19, B20; K8-Z5, B15, B16."

Also l.141 (K8): add "placed rows: drawn centre at r_c cos theta and whole drawn extent inside the spec footprint projection (projected_extent, TP1.1-11)".
Also l.144: append "1.1 (h) r4 added K8-Z5, K7-B20, K8-B15, K8-B16 (117 controls: Z 35, B 81, smoke 1); K8-B7 planted 2 -> 3".

## Reported values (corrected)

| Pair | Pose | Side view (MEASURED) | Plan lower bound | Hand |
|---|---|---|---|---|
| gear \| bracket_guide_a (G 10) | park | 37.295 | **54.646** | 181 - 126.32 = 54.68 (the circumscribed 128-gon of r 126.32 reads 54.65). **r3 notes wrote "x gap 15.43 (lower bound)": wrong.** The Loftsman's correction stands at 54.65. |
| ring \| frame_upper_a (G 10) | capture_end | 8.827 | 59.944, plan-separated | 270 - 210 = 60 |
| nut_housing_a \| frame_upper_a (G 10) | park | 55.263 | 84.993 | 270 - 185 = 85 |
| bracket_anchor_a \| frame_upper_a (C) | all | overlap 900.000 mm2 in projection | distance 0.000, overlap 0.000 (plan-contact) | r_out 270 = 300 - 30 |
| frame_upper_a drawn x | all | -300.79 to -218.83 | | above |
| frame_upper_a depth band | all | 109.02 to 190.98 | | 150 +/- 25.98 (30 cos 30) |

The r3 values unchanged by r4 are 10.84, 19.84, 12.00, 24.16, 33.16 and plan 14.993.

## Check results

**`check_sketch.py s1 --rev 4`: 17/17 pass on run 1 of the drawing.**

| Check | Result | Change from r3 |
|---|---|---|
| K1 to K6 | pass | 0 literals; 284 keys; 55 labels; 327 tagged artists; 215 z_rules |
| K7 | pass | 477 pair tests (r3: 457). The square member footprint adds measured G pairs. |
| K8 | pass | 330 predicates. Every placed row is inside its footprint projection. |
| K9 | pass | 54 rows |
| S1-1 to S1-7 | pass | unchanged: 650.00, 125.00, 367.34 / 117.34, 0.84, 192.34, 142.00, 8 projections, 607.66 |

**Controls: 117, all matched.** Z 35/35 clean, B 81/81 fired, smoke 1/1. The r4 additions are K8-Z5, K7-B20, K8-B15 and K8-B16.

**Existing control re-scoped:** K8-B7 (motor mirrored to the far side) now also reports `motor23_a projected_extent`.
- The mirrored motor lies 282.32 outside its footprint, a correct third detection.
- The manifest entry is now planted 3 (was 2), with the reason substring added.
- The first r4 controls run scored it as a mismatch (3 issues against 2 planted). The second run matched.

**Stale:** `--stale` reports 0 records and 0 differences.
**Baseline:** `--baseline` was re-run because run 1 grew. Run 1 is 35/35, 81/81 and 1/1. Run 2 (stub) matches 17/17.
**Reported:** s1_summary_r4.md, with the s1_mass_report section appended once. The mass table is unchanged.

## PNGs

- research/sean/cr_scratch/s1_pose_load_r4.png
- research/sean/cr_scratch/s1_pose_start_r4.png
- research/sean/cr_scratch/s1_pose_capture_end_r4.png
- research/sean/cr_scratch/s1_pose_park_r4.png

The only visible change from r3 is the screw frame members, drawn 81.96 wide (r3: 60).

## Files changed

- sketches/check_stack.py: radial_corners, place_extents rot, place record rot.
- sketches/sketch_common.py: plan_footprint through radial_corners; K8 projected_extent (x; y in plan).
- sketches/s1_spec.yaml: frame_upper_a/_b place; r4 comment; place field doc.
- sketches/fixtures/builders.py: k7_b20, k8_b15, k8_b16.
- sketches/fixtures/manifest.yaml

**Spec re-sign is due:** the Loftsman for the member placement; the Designer for the drawn member width.

Carried from r3 and still open: the Designer re-sign (dash rule, label text, new rows), the plan-contact sign-off, and the Design Notes 20 rows listed in step1.1_engineer_revision_r3.md.
