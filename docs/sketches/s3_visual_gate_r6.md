## S3 r6 M1 visual gate (P8r, The Designer, fresh image-capable reviewer)

Image gated: `docs/sketches/wip/s3_jackscrew_section_r6.png` (4157 x 3876 px), opened with the Read tool, then cropped and enlarged 4x to 5x in `D:\Unleashed Robotics\_scratch\cutjig\p8r6\` (crop.py, zoom.py). S1 r8 and S2 r9 not gated in this spawn.

## Corrections to the brief

1. The P8 section of `step1.3_manager_open.md` (the block this spawn was told to read, line 929 to the line before P9) closes with the orchestrator's scoring line, which states the expected control outcomes from `key.json`. That line was read before the controls were opened. The verdicts below are what the pixels show; the orchestrator should weigh the control result with that exposure in mind.
2. `docs/sketches/wip/s3_summary_r6.md` (READ FIRST item 5) was not opened: the read was refused by the session's permission classifier. `wip/s3_checks_r6.json` was read.
3. Scale used for pixel readings: 2.435 px/mm in u, 2.455 px/mm in z on the full PNG (DERIVED from the 100 mm and 200 mm gridlines). Pixel heights below are within about 1 mm.

## Reviewer-model controls

| Figure | Verdict | What the figure shows |
|---|---|---|
| ctrl_a | FAIL V3 | Side view: the wide 177.8 cutter block sits at the top of the tube (z about 1090 to 1195) and the bottom end of the tube (z about 245) is bare; the cutting head is at the tail, away from the core. V1, V2, V4, V5 read correctly. |
| ctrl_b | PASS V1 to V5 | Same scene with the cutter block at the bottom (z about 245 to 350) over the core and a separate top-end block at the top; floor at z 0, screw guides at top and anchors at bottom, core upright. |
| ctrl_c | PASS handedness | Plan: +X right, +Y up, theta arc runs counter-clockwise from +X to +Y; screw a at 30 deg upper right, b at 150 deg upper left, c at 270 deg below the axis. |
| ctrl_d | FAIL handedness | Plan: +Y arrow points down; the theta arc runs clockwise on screen; screws labelled 30 and 150 deg sit below the X axis and 270 above it. |

## S3 r6 rubric (gameplan rubric applicability: S3 V1, V5 to V10)

| Item | Verdict | What the figure shows |
|---|---|---|
| V1 | PASS | Floor line at z_S 0 at the bottom; member c stands on the rail end at the left; the NEMA 17 (grey) hangs below the anchor block on two rear standoffs; the brass nut sits in the ring housing at z_S about 381. |
| V2, V3, V4 | N/A | Not in the S3 applicability list. |
| V5 | PASS | Screw c vertical at u -160; fixed anchor block with two ball rows at the bottom (bearing line z_S about 343); radial top guide with one ball row at z_S 1210; nut on the ring between them; dash-dot nut stations at 1030.84 and 1155.84 sit between nut and guide. |
| V6 | PASS | Every part in the section is a rectangle or a four-vertex section; circles appear only as bearing balls (admitted sub-artists) and in the plan inset. |
| V7 | PASS | Jack screw: shank with dashed root lines, journal stepping down through the top guide, floating brass nut with flange in a counterbored boss and the inboard shoulder screw with its head on the flange top. Anchor: block of two angular-contact rows with balls, cover above, locknut below, bearing line between the rows. NEMA 17: grey body, pilot, bare shaft, beam coupling around the screw end (dashed inside the coupling). Hold: callout on screw c naming the self-locking Tr12x3 lead (lambda 5.20 deg) with brake and park pin as Step 2 options. Inset: three screws at 30, 150, 270 deg with housings, anchor blocks, lift motors, members, home switches and the sync callout (one controller, three drivers, home switch per screw, no belt). |
| V8 | FAIL | Labels legible at 100 percent, no text overlaps, every label carries its value. Two leaders merge with part edges: F1 (load_comp_c) and F2 (nut_c) below. |
| V9 | PASS | See the V9 section. |
| V10 | PASS | Load: ring at park shown by the park nut station; hold callout states the lead holds and the hold state is not visible (Step 2 item in the operator table). Collet change: wing nut and its r 115 sweep drawn under the head; coupling c at u -150.5 to -169.5 between the standoffs, 35.5 outboard of the sweep, motor shaft bare below it, all in view. |

## S3 rubric additions

| Addition | Verdict | What the figure shows |
|---|---|---|
| V1 addition | PASS | NEMA 17 under the anchor block on standoffs; nut in the ring housing. |
| V5 addition | PASS | Anchor bearing line below the nut, radial guide at the top, nut on the ring; the tension pair arrows (outward heads) span bearing line to nut bottom. |
| Section handedness | PASS | Screw c and member c left of the axis (u < 0); pinion c and NEMA 23 c right (u > 0); inset section line A-A on x = 0 with arrows toward -X, consistent with viewer at +X and u = +Y right (Y x Z = X). |
| Inset handedness | PASS | +X right, +Y up, theta arc counter-clockwise from +X; screws at 30, 150, 270 deg. |
| V6 addition | PASS | Rectangles in the section; circles only as balls and in the inset. |
| V7 addition | PASS | Screw with fixed anchor (two rows between cover and locknut), floating nut in a counterbored boss with a shoulder screw, radial guide; motor as body, pilot and shaft on standoffs. The 0.05 axial play is below drawing resolution (0.12 px) and is not labelled; the radial float 0.5 is labelled. |
| V10 addition | PASS | Couplings, standoffs and motor shaft of screw c visible; park station drawn for the load pose. |
| Section convention | PASS | Cut parts hatched by material (legend in the note); rear standoffs beyond in solid elevation; hidden edges dashed (core inside the unsectioned head, screw end inside the coupling, thread root inside screw c). |
| Inset radial symmetry (Topologist 1.2 (c) NOTE 1) | PASS | Housings, motor squares, members and switch bodies at a and b are rotated with their azimuths (switch long side along the radial, -30 deg on screen at theta 30); a and b mirror about the Y axis (screen x 893 and 453 about 673 in the inset crop). |

## V9

From the figure alone: each screw is held axially at its bottom in a fixed block of two back-to-back angular-contact bearings on the member arm, guided radially at its top, driven by a NEMA 17 hanging below through a beam coupling and synced by one controller with three drivers and a home switch per screw; the 1000 N cut puts the screw between the anchor and the nut in tension (247.5 N per screw), the self-locking Tr12x3 lead holds the ring with power off, and the axial loop closes head, core, collet, receiver, plate, frame, member c, anchor, screw, nut, ring, bearing, tube, head.

Spec question: "How is each screw anchored, guided, driven and synced, does the 1000 N axial load put it in tension, what holds the ring with power off, and does the axial load loop close?" The sentence answers each clause.

## Findings (S3 r6), to Sean at M2

Orchestrator ruling in force: r6 is the last drawn revision before M2. Each finding carries its fix and dry-run; none opens a revision.

**F1 (load_comp_c, V8), to Sean at M2.** The compression leader ends on the arrow shaft at (-185.00, 410.84) and runs right at z_S 410.84, which is the bottom of the NEMA 23 c body and the top of motor mount c: 77.5 mm along motor23_c and 69.5 mm along motor_mount_c within 1 mm and 2 deg (MEASURED, scratch scan with the K4 collinear geometry applied to every tagged part edge). At 100 percent the leader reads as the body's bottom edge over u +117 to +218. The r6 fix for r5 F1 moved the leader off the z 400 gridline onto this edge.
- Fix: `load_comp_c.label_anchor_frac` 0.5 to 0.3 (anchor (-185.00, 404.84) on the arrow shaft; 4.84 above the z 400 gridline, 5.16 below z 410, 6.00 below the motor body).
- Dry-run (scratch copy `p8r6\ws`, F1 and F2 applied together, MEASURED): S3 15/16 with S3-3 failing on the stale S1 r7 / S2 r5 records only, as on the live r6; K4 pass in both Axes; `--controls --only "K4-*"` 39/39 match (Z 8, B 31; K4-B30 still fires on its planted z 400 leader); part-edge scan over all 20 section labels: no leader within 1 mm and 2 deg of any part edge over more than 5 mm; PNG `p8r6\ws\docs\sketches\wip\s3_jackscrew_section_r98.png` inspected: the leader crosses the mount hatch clear of every edge. Frac 0.7 was dry-run first and rejected: anchor 416.84 runs the leader through the grey NEMA 23 fill.

**F2 (nut_c, V8), to Sean at M2.** The "floating nut, radial float 0.5" leader ends at the default anchor (-139.00, 387.84), 1.00 mm above the ring top at 386.84, and runs 110 mm along the ring top, 12 mm along the bearing top, 68 mm along motor mount c and 5 mm along nut_housing_c (MEASURED, same scan). At 100 percent it doubles the ring's top line across the figure (3 px apart on the full PNG).
- Fix: add `nut_c.label_anchor_frac: 0.85` (anchor (-139.00, 391.34) on the flange face, 4.50 above the ring top).
- Dry-run: as F1 (applied together); K4 anchor record clean for nut_c; PNG r98 shows the leader 10 px above the ring top line.

**N1 (rule scope), to Sean at M2.** The r6 collinearity rule tests reference-line rows and gridlines only; F1 and F2 are the same merge against part edges. Proposed extension of `collinear_issues` in section views: add every tagged artist edge of the section Axes except the label's own row to the line set. Dry-run description: on the live r6 spec it fires 2 (load_comp_c on motor23_c / motor_mount_c, nut_c on ring / bearing / motor_mount_c / nut_housing_c; MEASURED by the scratch scan `p8r6\premise.py`, which applies the rule's own `_run_near` to all edges); after F1 and F2 it is clean (MEASURED, `p8r6\dryrun.py`); it needs its own Z (live after the fix) and B (the r6 anchors). Global scope (S1, S2 side and plan views) stays carried under the orchestrator ruling.

**N2 (drawing content against spec shape text), to Sean at M2.** The spec shape strings name tooth ticks on the gear lower face and the pinion upper face, cutter teeth ticks on the head bottom edge, collet slit ticks and receiver thread ticks; `s3_jackscrew_section.py` draws none of them and none are visible. The parts read by shape, label and hatch, so V7 passes on the S3 V7 list. Fix: either draw the ticks (gear and pinion at least, as S1 does per Design Notes 29) or strike "ticks" from the five S3 shape strings; a draw change opens a revision, a text change re-runs --stale and S3 (detail 1 common (i)).

**N3 (inset leader).** The sync callout's dotted leaders to screws a and c cross the left corner of member a's hatched square in the inset. They cross; they do not run along it. No action proposed.

**N4 (stale comment).** `s3_spec.yaml` load_cases header comment says "W_kg below, 24.25 kg"; the W_kg line and loads() give 26.25 kg (MEASURED 26.25). Comment only.

Overall S3 r6: **FAIL** (V8: F1, F2). FAIL count 1 rubric item, 2 findings.

## Raiser signatures, r6 rules (`step1.3_engineer_revision_r3.md` section r6)

Deletion tests on a scratch copy of `docs/sketches` (`D:\Unleashed Robotics\_scratch\cutjig\p8r6\ws`, key.json excluded), each deleting one rule in `sketch_common.py` and running `check_sketch.py --controls --only "K4-Z8,K4-B26,K4-B27,K4-B28,K4-B29,K4-B30,K4-B31"`; restored after each. Unmodified copy: Z 1/1 clean, B 6/6 fire, 23.7 s (MEASURED).

| Rule | Deletion | Controls after deletion (MEASURED) | Premise check (MEASURED) | Signature |
|---|---|---|---|---|
| 1 Computed load labels; spec per_screw literals held to loads() within 0.005 N | `load_literal_issues` returns [] | K4-B26 clean (planted 4): red; Z8 clean; others unchanged | loads() from the keys: W 26.25 kg; static 85.8375, capture 119.8455, retract 185.8375, cut 247.4958, stall 343.1803 N. Literal minus loads(): +0.0025, +0.0045, +0.0025, +0.0042, -0.0003, -0.0003, all inside 0.005. Printed labels: "static 86, capture 120, retract (F_bind 300) 186, stall up 343 N" and "T per screw, cut 247.5" equal loads() at their formats | SIGNED. NOTE: `_first_number` holds only the first figure of the stall literals ("343.18 / 282.21"); the mu 0.20 figure 282.21 is unheld. Proposed (to Sean at M2): compare every number of a text literal against loads() at mu low and high; dry-run for the Engineer (not run here): live spec clean; 282.21 changed to 292.21 in both stall literals must fire 2 (stall_up, stall_down). |
| 2 label_anchor_frac anchor record and [0, 1] lint | `anchor_record_issues` returns [] | K4-B27 clean (planted 1): red; K4-B28 fires 2 of 3 (lint reason gone): red; Z8 clean | Placer record on the live figure: anchor_c (-139.00, 353.50), guide_c (-139.00, 1219.90), load_comp_c (-185.00, 410.84), each with source label_anchor_frac; spec fracs 0.95, 0.83, 0.5, all in [0, 1]; `anchor_record_issues` on the live context: 0 | SIGNED. |
| 3 Leader collinearity, section views | `collinear_issues` returns [] | K4-B29 clean (planted 2), K4-B30 clean (planted 1), K4-B28 fires 1 of 3: red; Z8 clean | Live: 0 issues against reference lines and major and minor gridlines; least leader-to-gridline distance 1.98 mm (load_cut, drill_head, drill_tube). The premise ("a leader is followed by eye only where it does not merge with another line") holds for the lines the rule names; part edges are outside its line set, and F1 and F2 are that case on the live r6 | SIGNED for its stated set (reference lines, gridlines, section views; global scope carried per the ruling). Extension to part edges is N1, to Sean at M2. |
| 4 Nut station labels against check_stack nut_z | K4 stack_z comparison set to never fire | K4-B31 clean (planted 1): red; Z8 clean | check_stack nut_z: start 970.84 z_A = 1030.84 z_S; park 1095.84 z_A = 1155.84 z_S; labels print 1030.84 and 1155.84; ticks drawn at z_S 1031.4 and 1156.4 by pixel reading (within the 1 mm reading error). Printed value comes from the row's own stack z_min; the check reads check_stack nut_z at pose_of: two sources | SIGNED. |

Scratch files: `p8r6\deltest.py` (deletions), `p8r6\premise.py` (premise reads and part-edge scan), `p8r6\dryrun.py`, `p8r6\dry2.py` (F1, F2 dry-runs), `p8r6\s3_spec_orig.yaml`, `p8r6\sketch_common_orig.py`. The scratch copy holds the original spec and harness after the tests (byte-compared).

## Gameplan lines to change

none
