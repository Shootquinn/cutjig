# S3 r4 M1 visual gate (P8r, The Designer, fresh image-capable reviewer)

Image: docs/sketches/wip/s3_jackscrew_section_r4.png, 4157 x 3876 px (MEASURED), opened with Read and inspected in crops at 1x to 4x (crops in D:\Unleashed Robotics\_scratch\cutjig\p8r4\). Inputs: s3_spec.yaml, gameplan l.178-207, wip/s3_checks_r4.json, wip/s3_summary_r4.md. S1 r8 and S2 r9 not gated here (fresh M1 PASS at r1, pixel-equal since, per the orchestrator).

## Corrections to the brief

1. The P8 READ FIRST items 6 and 7 (S2 r<m>, S1 r8) do not apply to this spawn; S3 only.
2. Spec row load_tension_c shape text reads "T 254 N per screw (cut)" (DECLARED); load_cases cut per_screw is 247.50 (DECLARED) and the figure prints 247.5. The spec shape text is stale, the drawing is right.
3. Spec row floor shape reads "ground hatch below"; the figure draws the floor line with no ground hatch (N4).

## 1. Reviewer-model controls

| Figure | Judged on | Verdict | What I see |
|---|---|---|---|
| ctrl_a | V1 to V5 | FAIL (V3) | Large OD 177.8 cutter block at the top of the drill (z about 1090 to 1195), plain tube running down to about 245 with no head at the bottom: cutting head at the tail, drill tip-up. V1, V2, V4, V5 read correctly (floor at 0, axis vertical, core upright on the bottom, screw with blocks at both ends). |
| ctrl_b | V1 to V5 | PASS | Cutter block OD 177.8 at the bottom (about 245 to 350), separate top-end block at the top (about 1045 to 1195), core upright from 100, screw vertical with end blocks, floor at the bottom. |
| ctrl_c | plan handedness | PASS | +X arrow right, +Y arrow up, theta arc from +X counter-clockwise to +Y; screw a at 30 deg upper right, b at 150 deg upper left, c at 270 deg bottom. |
| ctrl_d | plan handedness | FAIL | +Y arrow points down (mirror about X); theta arc sweeps clockwise on the page; screw c labelled 270 deg sits at +y 160 and a, b below the X axis. |

## 2. S3 r4 rubric (applicable: V1, V5 to V10)

| Item | Verdict | What I see |
|---|---|---|
| V1 | PASS | Floor line at z_S 0 at the bottom; rails stand on it, member c on the -Y rail. NEMA 17 c (grey, hatched) hangs under the anchor block on the two rear standoffs with pilot, shaft and coupling between; nut c (brass, dotted) sits in the ring boss, flange in the counterbore. |
| V5 | PASS | Screw c vertical at u -160; fixed anchor block at the bottom (bearing line about z_S 340), radial top guide at the top (z_S 1210), nut on the ring between them (about z_S 380). Bearing line below the nut bottom in the drawn pose; start and park nut ticks lie higher still. |
| V6 | PASS | Section: every part a rectangle or a true-section polygon (gear, pinion, collet cone); the only circles are the bearing balls (admitted sub-artists). Inset: circles for screws, housings, keep-out and ring OD only. |
| V7 | PASS | Screw: thread root lines dashed over the Tr12x3 span, plain collar above and below, journal into the guide block. Fixed anchor: two ball rows in a 42 block, cover above the joint in "||" hatch, locknut hatched under the lower inner race, block on the extrusion arm. Floating nut: brass body in a counterbored boss with clearance, inboard shoulder screw with its head over the flange. Top guide: single radial ball row in the block, journal free axially, home switch with lever under the guide arm. NEMA 17: body, pilot, shaft into a beam coupling, the screw end entering the coupling from above (hidden ends dashed). Hold device: callout names the self-locking lead as the drawn option and lists brake and park pin as Step 2 options. Gear and pinion c: bevel pair, gear teeth face down onto the pinion, NEMA 23 c with shaft on the dash-dot pinion axis, mount on the ring. Inset: three screws, housings, blocks, motors, members and switches, plus the sync callout with leaders to all three screws. |
| V8 | FAIL | Labels legible at 100 percent, none overlap, every leader ends on its part. One label value is wrong: F1. |
| V9 | PASS | See section 4. |
| V10 | PASS | Load row: the park nut tick (z_S about 1156) places the ring overhead at load; the hold callout states the self-locking lead, the hold state not visible, as the operator row records (Step 2). Collet-change row: coupling c at u -169.5 to -150.5 and z_S about 303 to 323 between the rear standoffs with bare motor shaft below, outside the wing-nut sweep r 115; the lift is idle at load. Hands at r <= 115 are clear of every moving part drawn. |

## 3. S3 rubric additions and section convention

| Addition | Verdict | What I see |
|---|---|---|
| V1 (NEMA 17 hangs on standoffs; nut in the ring housing) | PASS | As V1. |
| V5 (anchor below nut below guide; bearing line below the nut in every pose) | PASS | Anchor line about z_S 340, nut start tick about z_S 1031, park tick about z_S 1156, guide z_S 1210 (MEASURED from pixels, +-3); summary tension_segment least 40.84 at capture_end, S3-1 least 25.84 to the nut bottom (MEASURED, checks JSON). |
| Section handedness (viewer +X, u = +Y right; screw c and member c left, pinion c and NEMA 23 c right) | PASS | Screw c, member c, anchor and guide arms at u < 0; pinion c, NEMA 23 c and its mount at u > 0. Title states x = 0, seen from +X, u = +Y. |
| Inset handedness (+X right, +Y up, theta CCW; screws 30, 150, 270; A-A on x = 0, arrows toward -X) | PASS | +X arrow right, +Y arrow up on the section line, theta arc CCW from +X; screws at upper right, upper left, bottom; A-A dash-dot on x = 0 with both end arrows pointing to -X, letter A at both ends. |
| V6 (rectangles in the section, circles only in the inset, balls admitted) | PASS | As V6. |
| V7 (fixed anchor with two bearings between shoulder, cover and locknut; floating nut held by shoulder screws with play; radial guide; motor as body, pilot and shaft on standoffs) | PASS | As V7. |
| V10 (fixed parts and nut_station_park at load) | PASS | As V10. |
| Section convention: cut hatched | PASS | Cut parts hatched by material (aluminium //, cover ||, extrusion xx, steel \\, brass dotted); legend in the figure note. |
| Section convention: beyond in elevation | PASS | Rear M3 standoffs drawn in elevation as plain outlines, solid where visible. |
| Section convention: hidden dashed | PASS | Screw end and motor shaft inside the coupling dashed; core inside the head dashed; thread root dashed inside screw c. See N2 for one inverse case. |
| Radial symmetry in the inset (Topologist 1.2 (c) NOTE 1) | PASS | Members a and b, anchor blocks, motor squares and home switches are each turned square to their own radial at 30 and 150 deg and mirror about x = 0; set c lies on the -Y radial. |

## 4. V9

From the figure: each screw stands in a fixed anchor of two back-to-back angular-contact bearings in a 42 block on an arm from its frame member, runs up through a floating nut in the ring boss to a radial-only top guide, is driven from below by a hung NEMA 17 through a beam coupling and synced by one controller with three drivers and a home switch per screw; the 1000 N cut load puts the screw between anchor and nut in tension (247.5 N per screw), the self-locking Tr12x3 lead holds the ring with power off, and the load loop closes head, core, core seat, collet, receiver shoulder, base plate, base frame, member c, arm, anchor block, bearing pair, locknut, screw c, nut c, boss, ring, bearing, drill tube, head.

Spec question: "How is each screw anchored, guided, driven and synced, does the 1000 N axial load put it in tension, what holds the ring with power off, and does the axial load loop close?" Every clause is answered by the figure; match.

## 5. Findings

F1 (FAIL, V8, row load_comp_c). The compression label reads "compression per screw: static 79, capture 113, retract (F_bind 300) 179, stall up 343 N" (MEASURED, label text). The spec load_cases and wip/s3_summary_r4.md screw_share give static 85.84, capture_lift 119.85, retract_bind 185.84, stall_up 343.18 (DECLARED / DERIVED). 79, 113 and 179 are the per-screw values for W 24.25 kg (24.25 x 9.81 / 3 = 79.30, DERIVED); the r3 change put the top-end block into W (26.25 kg) and the label was not regenerated. The tension label 247.5 uses the new W, so the figure states two inconsistent W values. Fix: label text from load_cases per_screw at run time (static 86, capture 120, retract 186, stall up 343 N, rounded as drawn). Dry-run required (detail 1 common (h)): the Engineer runs check_sketch.py s3 on the revised label and shows K4 reading load_comp_c against load_cases per_screw; a B fixture carrying "static 79" must fire K4 on load_comp_c (today K4 passes 19 labels with this one wrong, so the label carries no value_from coverage). Correct the stale spec shape text of load_comp_c and load_tension_c ("T 254") in the same edit.

## 6. Notes (no verdict effect)

N1. Park nut tick (z_S about 1156) has no label; the start tick is labelled "nut at start". The figure note explains both ticks; a "nut at park" label would let V10 read without the note.
N2. Drill head: its top, bottom and cutter-band lines are dashed between the core walls. The head's front rim lies in front of the core, so those segments are visible and should be solid; the core edges inside the head are correctly dashed. To the renderer co-owners (Designer, Topologist).
N3. Inset: anchor block (solid) and NEMA 17 (dashed) are coincident 42 squares; at screw c the dashed square draws over the block and the block reads as hidden. Draw the block outline last.
N4. Floor row: spec shape names a ground hatch below the floor line; none drawn. The floor reads without it; fix the spec text or the drawing.
N5. Hold callout prints lambda 5.19 deg; the summary backdrive item gives 5.20 (DERIVED, atan(3 / (pi 10.5)) = 5.197). Round the callout as the summary does.
N6. Head bottom edge: no cutter tooth ticks visible at 4x; spec row drill_head names them. The label "HEAD (cutter, tip)" carries the reading.
N7. The L_t dimension line at u -110 (orchestrator ruling) crosses the ring and gear sections in red; it reads as a dimension, no change asked.
N8. Hatch legend lists no plastic pattern; the last note line names plastic. Drop plastic or add its pattern.
N9. The three dotted sync leaders cross member a in the inset; they converge on the callout and read correctly.
N10. S3-3 fails in r4 (content) on stale S1 r7 and S2 r5 records; per the spec it clears only after S1 r8 and S2 r9 are accepted. Outside M1.

## 7. Verdict

S3 r4: FAIL, 1 finding (F1, V8, load_comp_c). Every other applicable item and rubric addition PASS.

Controls: ctrl_a FAIL V3, ctrl_b PASS, ctrl_c PASS handedness, ctrl_d FAIL handedness. Orchestrator scoring against key.json (2026-11-26): 4 of 4 correct, each as keyed; the reviewer model is credited for this gate.

## Gameplan lines to change

none
