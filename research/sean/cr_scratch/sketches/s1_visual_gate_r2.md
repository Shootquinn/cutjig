# S1 visual gate, revision r2 (M1, The Designer)

Reviewer: The Designer, fresh spawn on an image-capable model. These figures are not my work. Every PNG below was opened with Read and returned image content. Detail crops were made from the same PNGs for inspection only. `fixtures/figs/key.json` was not opened.

Inputs: s1_pose_{load,start,capture_end,park}_r2.png; fixtures/figs/ctrl_a.png, ctrl_b.png; sketches/s1_spec.yaml; gameplan l.175-201, 495-507; sketches/s1_summary_r2.md; step1.1_engineer_revision_r2.md; step1.1_loftsman_crossreview.md "Re-check r2".

Corrections to the brief: none. Numbers read from the figures are MEASURED by grid at about 0.53 px/mm, good to about 5 mm. Spec and summary values are DECLARED or DERIVED as tagged there. The new dimensions in section 6 are ASSUMED (Designer working values).

## 1. Reviewer-model controls (blind)

| Figure | V1 | V2 | V3 | V4 | V5 | What I see |
|---|---|---|---|---|---|---|
| ctrl_a | PASS | PASS | **FAIL** | PASS | PASS | The wide block labelled "cutter OD ASSUMED 177.8" is at the **top** of the drill, z 1090 to 1195. The tube runs down to an open plain end at z 245, inside the core. No top-end block. The drill is drawn tip-up. The floor is at z 0 at the bottom. The axis is vertical. The core (z 100 to 605) is upright on its seat. The screw is vertical, with its guide block at the top (1195 to 1225), the anchor low (325 to 355) and the nut at the ring (about 370 to 395). |
| ctrl_b | PASS | PASS | PASS | PASS | PASS | The cutter block is at the **bottom** of the drill, z 245 to 350. The top-end block is at the top, z 1045 to 1195. The core is upright on its seat at z 100. Screw, anchor, guide and nut are as in ctrl_a. |

Verdict: ctrl_a FAILS V3 (tip-up). ctrl_b PASSES V1 to V5.

## 2. S1 rubric V1 to V10

| Item | load | start | capture_end | park | What I see |
|---|---|---|---|---|---|
| V1 | PASS | PASS | PASS | PASS | The floor line z_S 0 is at the bottom, under the base frame (X sections) and the plate. The lift motors (grey, about 255 to 300) hang below the anchors. The NEMA 23s sit on standoffs on the ring top. |
| V2 | **FAIL** | **FAIL** | **FAIL** | **FAIL** | The drill axis is vertical and the gear half-sections mirror about it. The pinions cannot be told from the gear wedge at 100 percent, and no pinion or motor shaft line is drawn. A radial pinion axis cannot be read from the figure (finding F1). |
| V3 | PASS | PASS | PASS | PASS | "HEAD (cutter, tip)" is at the bottom of the tube, hatched at the cutting edge. The grey "TOP-END BLOCK (tail)" is at the top. The gear and motors are on the ring, 130 above the tip. |
| V4 | PASS | PASS | PASS | n/a | At load the core is upright, mid-insertion, bottom about 161 z_S (spec 101.17 z_A). At start and capture_end it is upright with its bottom on the seat at about 102.5 z_S. Never inverted. At park the core is absent. |
| V5 | PASS | PASS | PASS | PASS | The screws are vertical. Anchors are at 325 to 355 z_S, top guides at 1195 to 1225, and the nut (amber) is in the ring housing in every pose. |
| V6 | PASS | PASS | PASS | PASS | Every part is a rectangle or trapezoid in side view. No circles. |
| V7 | **FAIL** | **FAIL** | **FAIL** | **FAIL** | The anchor blocks, top-guide blocks and the descent-stop pad float in space: no bracket arm joins them to the screw frame members at x ±230 to 290 (F2, F3). The spec shape text asks for those arms. The gear and pinions do not read as a meshing pair: no tooth ticks are visible and the two outlines are not distinguishable (F1). The NEMA 23 is a grey body with no shaft (F1). The ring plate, nut housings and standoffs do read as a structure. |
| V8 | **FAIL** | **FAIL** | **FAIL** | **FAIL** | Overlaps are listed in F4. Name-only labels carry no dimension: "top guide", "anchor", "HEAD (cutter, tip)", "TOP-END BLOCK (tail)". |
| V9 | **FAIL** | | | | See section 4. The figures do not show how the anchors and guides reach the frame, so the axial-loop clause cannot be answered from them. The park rule is not on the figures. |
| V10 | PASS | n/a | **FAIL** | n/a | See section 5. Load tasks: reach and sight PASS. Watch during a cut: at capture_end the ring rim hides the cutter (F6). |

## 3. Rubric additions (spec wording)

| Line | Verdict | What I see |
|---|---|---|
| ring assembly on the drill tube between the head and the top-end block in every pose | PASS | The ring is at 130 above the tip in all four poses. The bearing is above the head and the gear is below the top block. |
| motors on the same side of the gear in every pose, outboard of the pinions, below the gear back face | PASS (motors); pinion position not legible | The NEMA 23 bodies are outboard of the gear on both sides, with tops below the gear back face. "Outboard of the pinions" rests on K8; the pinion cannot be read by eye (F1). |
| 0.75 m core drawn solid at load (mid-insertion), start and capture_end, absent at park; no 0.5 m core | PASS | Bold solid outline at load, start and capture_end. No core at park. No second core. |
| drill head at the bottom and the top-end block at the top | PASS | All four poses. |

## 4. V9

From the figures alone: the jig peaks at about 1970 z_S at load and park, about 30 under the 2000 soft target. The ring rides on the tube 130 above the cutter tip. Screw anchors are at about 325 to 355 z_S and top guides at about 1195 to 1225, both unlabelled and read from the grid. The park tip is 1019.84 z_S, and the lift stroke is 775 by subtracting the park and capture_end titles. Two screw frame members (to about 1285), the base plate and the base frame are drawn, but nothing ties the anchors or guides to the members.

Spec question: "Is the jig tall enough, where along the drill does the ring sit, where are the screw anchors and top guides, what are the park rule and the lift stroke, and which frame and base members carry the axial loop?"

Comparison:
- Height and ring position are answered.
- Anchor and guide heights are answered only by reading the grid.
- The park rule is not stated on any figure, and the stroke has to be derived.
- The axial loop is not answered: the path from anchor and guide into the frame member is undrawn.

FAIL.

## 5. V10, per S1 operator task

| Task | Reach | Sightline | Verdict |
|---|---|---|---|
| Lift the 0.75 m core into the collet under the parked ring (load) | Core path between the screws, under the ring at 1149.84 to 1161.84 with the NEMA 23 above it to about 1242. The drawn mid-insertion core top is about 911, 109 under the tip. The entry instant (top 969.84, 50 under the tip) is not drawn, as the spec's mid-insertion z_rule intends. | Down the holder bore past the ring bore. The side view cannot show the S2-5 sector (S2 owns it). | PASS. Lift is idle and the drill is stopped at load, so the hands are clear of moving parts. The ring and motor at chest-to-shoulder height are a strike hazard (table row, Step 2). |
| Change a collet, wing nut under the ring (load) | Wing nut at about 170 to 205 z_S, sweep r 115. The nearest parts above it are the lift motors (about 255), the anchors (325) and the pad (363 to 375). Kneeling reach. | Wing nut visible from knee height. | PASS |
| Watch during a cut (start to capture_end) | Outside the frame. | At start the cutter (894.84 to 1001.21) is in view under the ring. At capture_end the ring plate (underside 374.84, rim r 210) is directly over the cutter (244.84 to 351.21) in the figure. A standing observer cannot see the end of the cut. | **FAIL** at capture_end (F6) |

## 6. Findings (overall FAIL)

| # | Item | Pose | Feature id | Finding | Ruling and dimensions |
|---|---|---|---|---|---|
| F1 | V2, V7 | all | pinion_a, pinion_b, motor23_a, motor23_b, gear | Pinion outline indistinct from the gear, no tooth ticks visible at 100 percent, no motor or pinion shaft | **Fix in r3:**<br>(a) Draw the NEMA 23 shaft as a radial rectangle, r 121 to 142 (pinion.motor_r_in - pinion.motor_shaft_length to pinion.motor_r_in), height pinion.motor_shaft_od 8, centred on the pinion axis z. Declare it C with the motor and N with the pinion hub (already declared).<br>(b) Draw the pinion axis as a dash-dot centreline from r 95.22 to r 218, horizontal in side view. This is the visual signifier that the axis is radial.<br>(c) Hatch the pinion and the gear in opposite directions so the mesh reads.<br>Tooth ticks at module 4.17 are below 3 px at S1 scale. The tooth-level read goes to **S6**, which fixes the gear and pinion geometry. |
| F2 | V7, V9 | all | anchor_a, anchor_b, guide_a, guide_b, frame_upper_a, frame_upper_b | Anchor and top-guide blocks float. The spec shape text ("on a bracket arm from the screw frame member") is not drawn. | **Fix in r3.** New rows bracket_anchor_a/_b and bracket_guide_a/_b:<br>- kind prism, radial footprint, theta jackscrew.angle[1]/[0].<br>- r_in = jackscrew.pitch_radius + jackscrew.nut_flange_od / 2 = 181. r_out = frame_upper.radius - profile.width / 2 = 270.<br>- half_width profile.width / 2 = 30.<br>- Anchor arm z = anchor block z (jackscrew.anchor_z to + anchor_allowance, 265 to 295 z_A). Guide arm z = guide block z (1135 to 1165 z_A). Arm top is flush with the block top.<br>- C with the block and with frame_upper. chain [axial].<br>- Existing G pairs carry over: nut_housing|arm equals nut_housing|block, 10.84 at capture_end and 24.16 at park, because the arm z equals the block z.<br>- The ring rim over the anchor arm at capture_end is 314.84 - 295 = 19.84 (G 10).<br>- Where a nearer part covers an arm in projection (the guide arm behind the NEMA 23 at load and park), draw the arm dashed.<br>All values ASSUMED. Step 2 rules the bracket design. |
| F3 | V7 | all (lands at capture_end) | descent_stop | Pad drawn floating at r 200 to 215 with no support | **Fix in r3.** New row descent_stop_post:<br>- prism, radial footprint, theta jackscrew.angle[1].<br>- r 200 to 215 (frame_upper.stop_pad_r_in to stop_pad_r_out), half_width stop.pad_width / 2 = 30.<br>- z from anchor arm top (jackscrew.anchor_z + anchor_allowance = 295 z_A) to the pad bottom (ring_bottom_low - stop.pad_thickness = 302.84 z_A), height 7.84, as a z_rule so it tracks anchor_z.<br>- C with bracket_anchor_a and with descent_stop.<br>- Plan gap to the nut housing stays 15.0 (r 200 against r 185). |
| F4 | V8 | all | labels | Overlaps:<br>- load and park: "top guide" over the gear and motor outlines and the "gear PD 250" leader; "HEAD (cutter, tip)" crossed by screw_b; "T8 screw L 900" across the core and screw_a; "anchor" across both screws; "TOP-END BLOCK (tail)" on the block edge.<br>- start: "keep-out r 86.2" touching "cutter OD ASSUMED 177.8".<br>- capture_end: "core 750" on top of "gear PD 250" (both illegible); "top block 150" and "bore ceiling above tip 800" across screw_a; "cutter OD ASSUMED" over the right "anchor"; "HEAD (cutter, tip)" over liftmotor_b; "anchor" over the cutter outline. | **Fix in r3:**<br>- Put every label in the free right margin (x > 330 mm) with a leader, stacked at least one text height apart, and keep the left side clear.<br>- Dimension the name-only labels: "anchor z_S 325" (jackscrew.anchor_z), "top guide z_S 1225" (jackscrew.top_guide_z), "HEAD (cutter, tip) z_S <tip>", "TOP-END BLOCK 150".<br>- Add on the park figure "lift stroke 775 (park 1019.84 - capture_end 244.84 z_S)" and the park rule in one line (spec park_rule.park).<br>- Label the frame members "screw frame 30-6060 r 300".<br>This also closes the V9 gaps on anchor and guide heights, park rule and stroke. |
| F5 | V9 | all | frame_upper, bracket rows | Axial loop not readable | Closed by F2 and F4 in r3. |
| F6 | V10 | capture_end | ring, drill_head | The ring plate over the cutter hides the end of the cut from a standing observer | Not an S1 drawing fix. It is a property of the ring rim r 210 over the cutter. **Assigned to Step 2**, with the gear guard and interlock row already open: choose a sight window in the ring plate between the screw and pinion azimuths, a camera, or end-of-cut by the descent stop with a stop indicator. **S2** shows the sector sightline in plan. For S1 r3 this item passes once Sean accepts the Step 2 assignment at M2. |
| F7 | NOTE | all | drill_head, keepout | The cutter outline (r 88.90) is drawn outside the dashed keep-out line (r 86.2, tube basis). The keep-out does not bound the drill head. | No r3 action, since the ring bore r 100 and pinion toe r 95.22 clear 88.90. Owner: S2 plan clearance, and the Step 4 ICD row for icd.keepout_radius (LF1.1-5). |

## 7. Rulings on the r2 open items

| Item | Ruling | Reason |
|---|---|---|
| Undrawn bracket arms | **Fix in r3**, F2 dimensions | The spec shape already requires them. Without them V7 and V9 fail. |
| Descent-stop pad support | **Fix in r3**, F3 dimensions | The pad must visibly sit on the anchor arm. |
| Motor and pinion shafts | **Fix in r3**, F1 (a) and (b) | The spec shape already requires them. The shaft is the signifier for the radial axis in V2. |
| Base plate spigot-hole break (80.2 hole against 80 spigot) | **Assign to S4** | It is 0.10 per side, about 0.05 px at S1 scale. No S1 check reads it. S4 draws the base stack at detail scale and reclassifies receiver\|base_plate as G 0.10. |
| build_parts/holder.py section differs from the S1 stand-in | **Assign to S4**; S1 r3 adds a spec note: "holder section is a stand-in; S4 governs (build_parts/holder.py)" | The differences are 0.25 to 6.75 radial, below S1 resolution. No S1 check value moves: head\|holder 39.75 and ring\|holder 172.04 depend on the flange, which is unchanged, and the K6 stack tie is unchanged. S4 adopts OD 67.04, cone 62.04 to 56.75 over 30, bore 56.75, and the tube through the nut plate. |
| receiver\|holder 0.25 fit gap drawn as contact | **Assign to S4** with the section | The pair becomes G 0.25 when S4 adopts the part section. |
| Tube through the nut plate (collar\|holder would be C) | **Assign to S4** | It changes only that pair's class. S1 keeps F 8.00 for its stand-in, as the Loftsman confirmed. |
| C contacts as idealised fits (Loftsman R2-1) | **Accept at S1** | At S1, C means "located on that face". Fit values belong to S4 (base stack) and to Step 4 tolerancing. Add one line to the spec header saying so, so that no later reader takes a C as a clearance. |

Verdict: **S1 r2 FAIL.** FAIL items: V2, V7 and V8 in all poses, V9, and V10 at capture_end. Findings F1 to F6, plus NOTE F7. The r3 drawing fixes are F1 to F5. F6 is assigned to Step 2 and S2 for Sean's acceptance at M2.

---
Footer (orchestrator): control scoring per key.json is recorded here and in the Progress Log after this file is returned. Reviewer verdicts: ctrl_a fails V3, ctrl_b passes V1 to V5.
