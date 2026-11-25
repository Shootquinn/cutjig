# S1 visual gate, revision r3 (M1 re-gate, The Designer)

Reviewer: The Designer, on an image-capable model. These figures are not my work. Each of the four r3 PNGs was opened with Read and returned image content. Detail crops of the ring zone at load and capture_end and of the head at park were made for inspection only. `fixtures/figs/key.json` was not opened. The reviewer-model controls were judged at r2 (ctrl_a FAIL V3, ctrl_b PASS V1 to V5) and are not repeated: the check runs once per reviewer model.

Inputs: s1_pose_{load,start,capture_end,park}_r3.png; step1.1_engineer_revision_r3.md; s1_visual_gate_r2.md.

Corrections to the brief:
1. My r2 F1 (a) said the shaft was "N with the pinion hub (already declared)". Only pinion|motor23 was declared. The Engineer's new N pairs, pinion_a|motor_shaft_a and pinion_b|motor_shaft_b, are correct.

Numbers read from the figures are MEASURED by grid at about 0.53 px/mm. New dimensions are ASSUMED (Designer, r2 F1 to F3).

## 1. Rubric V1 to V10

| Item | load | start | capture_end | park | What I see |
|---|---|---|---|---|---|
| V1 | PASS | PASS | PASS | PASS | The floor is at the bottom. Lift motors hang below the anchor arms. The NEMA 23s sit on their standoffs on the ring top. |
| V2 | PASS | PASS | PASS | PASS | The drill axis is vertical and the gear half-sections mirror about it. Each NEMA 23 now shows a black shaft bar into the pinion, and a dash-dot pinion axis runs horizontally through motor and pinion. The pinion axis reads as radial. |
| V3 | PASS | PASS | PASS | PASS | HEAD at the bottom of the tube, hatched at the cutting edge. Grey TOP-END BLOCK 150 at the top. |
| V4 | PASS | PASS | PASS | n/a | At load the core is upright, mid-insertion. At start and capture_end it is upright with its bottom on the seat at about 102.5 z_S. At park it is absent. |
| V5 | PASS | PASS | PASS | PASS | Screws vertical. Anchors at 325 to 355, top guides at 1195 to 1225, amber nut in the ring housing. |
| V6 | PASS | PASS | PASS | PASS | Rectangles and trapezoids only. The new dash-dot axis is a line. |
| V7 | PASS | PASS | PASS | PASS | Anchor arms at 325 to 355 run from each block to the screw frame member and overlap its inner face (x about -249 to -142). Guide arms do the same at 1195 to 1225. At capture_end the descent-stop pad (hatched) sits on its post on the left anchor arm and the ring rim lands on it. The gear (////) and pinion (\\\\) are hatched in opposite directions, so the mesh reads as two parts. The motor reads as body and shaft. Tooth ticks are not visible at this scale; that read is assigned to S6. |
| V8 | PASS | PASS | PASS | PASS | All labels sit in one right-margin column with leaders, and no label text overlaps another label or the drawing. Every label carries its dimension. The two leader crossings the Engineer lists are minor: at park the keep-out and lift-stroke leaders converge near the head; at capture_end the core 750 leader crosses the gear. Both labels stay legible and each leader ends on its feature. |
| V9 | PASS | | | | See section 3. |
| V10 | PASS | n/a | **FAIL (F6, carried)** | n/a | The load tasks have not changed since r2: reach and sightline PASS, hands clear at load. At capture_end the ring plate (underside 374.84) is over the cutter (244.84 to 351.21), so a standing observer cannot see the end of the cut. |

## 2. Rubric additions (spec wording)

| Line | Verdict | What I see |
|---|---|---|
| ring assembly on the drill tube between the head and the top-end block in every pose | PASS | The ring is 130 above the tip in all four poses, below the top block. |
| motors on the same side of the gear in every pose, outboard of the pinions, below the gear back face | PASS | The hatched pinion now reads. Each motor body is outboard of its pinion, with the shaft between, and its top is below the gear back face in all four poses. |
| 0.75 m core drawn solid at load (mid-insertion), start and capture_end, absent at park; no 0.5 m core | PASS | Bold solid outline at the three poses. None at park. |
| drill head at the bottom and the top-end block at the top | PASS | All four poses. |

## 3. V9

From the figures alone:
- **Height:** the jig peaks at about 1970 z_S at load and park, under the 2000 soft target.
- **Ring:** rides on the tube 130 above the cutter tip.
- **Screws:** anchors at z_S 325 (265 z_A), top guides at z_S 1225 (1165 z_A).
- **Park and stroke:** park = max(max_k start_k, entry_plane + max L) + upper.load_clearance = 959.84 z_A, 1019.84 z_S. Lift stroke 775.
- **Axial loop:** ring nut, T8 screw, anchor and guide blocks, bracket arms, screw frame 30-6060 at r 300, base plate, base frame, floor. The arms are drawn, and the loop is written in the margin note.

Spec question: "Is the jig tall enough, where along the drill does the ring sit, where are the screw anchors and top guides, what are the park rule and the lift stroke, and which frame and base members carry the axial loop?"

All five clauses are answered. PASS.

## 4. The Engineer's two items for the Designer

| Item | Ruling | Reason |
|---|---|---|
| (1) An arm is dashed only when a wholly nearer part overlaps it in z and covers at least half its projected x length. Result: guide arms dashed at load and park, solid at start and capture_end; anchor arms solid in every pose. | **Confirmed** | The guide rods are 20 wide and cover 20 of the 107.08 arm length. They are drawn over the arms, and that overlap already shows they are in front. Dashing the anchor arms for them would make a load-bearing arm read as hidden. At load and park the NEMA 23 covers 61.3 of 107.1, and the dashed arm reads correctly as behind the motor (checked in the crop). |
| (2) Label "anchor z_S 325 (jackscrew.anchor_z 265 z_A)" and "top guide z_S 1225 (jackscrew.top_guide_z 1165 z_A)", via a `z_S: true` label field | **Confirmed** | K4 needs the key value. Both frames on one label let the reader tie the figure (z_S) to params (z_A). The labels are legible at 100 percent. |

## 5. Re-signature of the r3 spec edits (Designer values, ASSUMED)

| Row / edit | Drawn or spec value | Ruling |
|---|---|---|
| bracket_anchor_a/_b, bracket_guide_a/_b | radial r 181 to 270, half-width 30, z 265 to 295 and 1135 to 1165 z_A. C with block and member through K7 plan-contact. In fixed_g10. | **Signed.** Matches r2 F2. Existing G pairs hold: nut_housing\|arm 10.84 at capture_end and 24.16 at park, ring\|arm 19.84 and 33.16, gear\|guide arm 37.30. The plan-contact rule needs the Loftsman and Topologist; it is outside my signature. |
| descent_stop_post | r 200 to 215, half-width 30, 295.00 to 302.84 z_A (z_rule from anchor_z and ring_bottom_low). C with arm and pad. | **Signed.** Matches r2 F3. ring\|post 12.00. nut_housing\|post is plan-separated at 14.99. |
| motor_shaft_a/_b | r 121 to 142, half-width 4, at the pinion axis z. C with motor23, N with pinion. | **Signed.** Matches r2 F1 (a), with the corrected N pair (Corrections to the brief, 1). |
| pinion_axis_a/_b | dash-dot line r 95.22 to 218 at theta 210 / 330, at the pinion axis z | **Signed.** Matches r2 F1 (b). |
| Gear //// and pinion \\\\ hatch | visual only | **Signed.** |
| Labels (anchor_b, guide_b, frame_upper_b, drill_head z_edge, drill_top_block), park-figure stroke and park rule, axial-loop margin note | as drawn | **Signed.** |
| Spec `notes`: holder stand-in (S4 governs); C means "located on that face" | text | **Signed.** Matches the r2 section 7 rulings. |
| Dash rule (item 1), label text (item 2) | as section 4 | **Signed.** |

All bracket and post values stay ASSUMED until Step 2 rules the bracket design.

## 6. Findings

| # | Item | Pose | Feature | Status |
|---|---|---|---|---|
| F1 to F5 (r2) | V2, V7, V8, V9 | all | pinion, motor shaft, bracket arms, post, labels | **Closed in r3** |
| F6 (r2) | V10 | capture_end | ring, drill_head | **Open, for Sean at M2.** No drawing action. Assigned to Step 2 (sight window, camera, or end-of-cut by the descent stop with an indicator) and to S2 (plan sightline). |
| F7 (r2) | NOTE | all | drill_head, keepout | Carried: S2 and the Step 4 ICD row. No S1 action. |
| N1 (new) | NOTE | park, capture_end | leaders | The two leader crossings stay visual only. No action. |

## Verdict

**S1 r3: every drawing item PASSES** (V1 to V9, V10 at load, all four rubric additions). One item fails: V10 at capture_end, which is F6. Because the gate passes only when every item passes, **the overall verdict is FAIL on F6 alone.** It becomes PASS when Sean accepts the F6 assignment to Step 2 and S2 at M2. FAIL count: 1.

---
Footer (orchestrator): control scoring per key.json recorded at the r2 gate. Reviewer verdicts there: ctrl_a fails V3, ctrl_b passes V1 to V5.
