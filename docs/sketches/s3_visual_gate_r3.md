# S3 r3 visual gate (M1 re-gate P8r, Step 1.3 (f))

Reviewer: The Designer, fresh image-capable spawn; did not produce the images. Every PNG below opened with Read as an image; 1:1 crops and 2x to 5x zooms made to D:\Unleashed Robotics\_scratch\cutjig\p8r3\. key.json not opened. The r1 gate file was read only after scoring, for section 6.

## Corrections to the brief

1. S3 r3 PNG: 4157 x 3876 px (MEASURED); SHA-256 030453fd120382679badd6286527216f86859633d139a00da55fe6e2fed33d5f (MEASURED). Section Axes about 2.48 px/mm (MEASURED from tick positions: u -300 and +300 at about 243 and 1715 px).
2. S1 r8 and S2 r9 are not re-gated here (fresh M1 PASS at r1, pixel-equal since, per the orchestrator).
3. wip/s3_checks_r3.json: 15 of 16 checks pass; S3-3 fails, 7 issues, cause content: chains a, b, c links base_plate|base_frame, base_plate|frame_upper_a/b, frame_upper_a/b|bracket_anchor_a/b, bracket_anchor_a/b|anchor_a/b "not certified" because the certifying records s1_checks_r7.json and s2_checks_r5.json are stale (jackscrew.lead recorded 8, live 3; jackscrew.nominal recorded 8, live 12) (MEASURED from the JSON). Not a visual item; it blocks acceptance until S1 r8 / S2 r9 are accepted or the certifier reads them. To the orchestrator.

## 1. Reviewer-model controls

| Figure | Verdict | What I see |
|---|---|---|
| ctrl_a.png | FAIL (V3) | The wide block labelled "cutter OD ASSUMED 177.8" is at the top, z 1090 to 1195, tube below to 245: drill drawn tip up, cutting head not at the bottom. V1, V2, V4, V5 read correctly (floor z 0, axis vertical, core upright 100 to 600, screw vertical with blocks at both ends). |
| ctrl_b.png | PASS | Cutter block at the bottom, z 245 to 350, tube above to 1195 with the top-end band at 1045; floor at the bottom, axis vertical, core upright, screw vertical. V1 to V5 pass. |
| ctrl_c.png | PASS (handedness) | +X arrow right, +Y arrow up, theta arc counter-clockwise from +X to +Y; screw a (30) upper right, b (150) upper left, c (270) below the axis. |
| ctrl_d.png | FAIL (handedness) | +Y arrow points down; theta arc runs clockwise on the page; screw c labelled 270 sits at y +160, a and b below. Mirrored plan. |

## 2. S3 rubric (applicable V1, V5 to V10; V2 to V4 N/A)

| Item | Verdict | What I see |
|---|---|---|
| V1 | PASS | Floor line at z_S 0 at the bottom. NEMA 17 c (grey, steel hatch) hangs under the anchor block at about z_S 240 to 290 on the rear standoffs; brass nut sits in the ring boss at about z_S 375 to 395. |
| V5 | PASS | Screw c vertical at u -160 from the anchor block (z_S about 325 to 355) to the top guide at z_S 1210 on the arm off member c; nut on the ring between them; dash-dot nut stations at about 1030 (labelled start) and 1155 (park), both below the guide. |
| V6 | PASS | Section: every part a rectangle or polygon; circles only as ball marks in the anchor and guide bearings. Circles otherwise only in the inset (screws, housings, keep-out, ring reference). |
| V7 | PASS | Read at 100 percent (1:1 crop): Tr12x3 screw with dashed root lines over the thread; floating brass nut, flange seated in the counterbored boss, inboard shoulder screw with its head above the flange; anchor block with two separate ball rows (back-to-back pair), cover above the joint in the "--" hatch, locknut under the inner races; journal into a beam coupling (screw end dashed inside), shaft down to the NEMA 17 pilot and body, two rear standoffs either side. Top guide: block with a radial ball row each side of the journal, no axial seat, on the extrusion arm; home switch with lever under the arm. Hold device: the self-locking lead option as a callout naming lambda 5.19 < phi_n 8.83 to 11.70 and the deferred alternatives (correct for that option: no drawn device). Pinion c, gear section and NEMA 23 c with shaft on the right read as S2. Inset: three screws, housings, 42 blocks, motors, members, switches and the sync callout. |
| V8 | FAIL | Labels legible at 100 percent and none overlapping; no leader crosses text. Two defects: the span label reads "S3-2 span L_t, K 0.7 870", pairing 870 with K (F1); the power-off-hold callout mark is a 30 mm line sticking out of the left (outboard) side of screw c at z_S about 790 into empty space, while its leader crosses the screw body from the right to land at that mark's root (F2). |
| V9 | PASS | Sentence in section 4; matches every clause of the spec question. |
| V10 | PASS | Load row: ring held on the self-locking lead (callout) with the park station marked at about 1155 z_S; collet change: wing nut sweep r 115 (dashed, z_S about 215 to 270) clear of the coupling at u -150 to -170, z_S about 303 to 323, about 35 radially, coupling exposed between the standoffs with bare shaft below, as the operator table states; guard and hold-state visibility are Step 2 rows. |

## 3. S3 rubric additions, section convention, inset

| Item | Verdict | What I see |
|---|---|---|
| V1 addition (NEMA 17 under the block on standoffs; nut in the ring housing) | PASS | As V1. |
| V5 addition (bearing line below the nut in every pose; radial guide at top; nut on ring) | PASS | Red anchor bearing line at about z_S 340, nut bottom above it at capture_end; start and park stations higher; guide at 1210. |
| Section handedness (u = +Y right; screw c, member c left; pinion c, NEMA 23 c right) | PASS | Member c (extrusion hatch) u -304 to -244, screw at u -160; pinion trapezoid with radial dash-dot axis and grey NEMA 23 c at u +95 to +215, z_S about 410 to 470. Title states x = 0, seen from +X, u = +Y. |
| Inset handedness (+X right, +Y up, theta ccw; screws 30, 150, 270; A-A on x = 0 toward -X) | PASS | Axes arrows +X right, +Y up, theta arc counter-clockwise; screws at (139, 80), (-139, 80), (0, -160); A-A dash-dot on x = 0 with both arrows pointing to -X. |
| V6 addition | PASS | As V6. |
| V7 addition (two bearings between shoulder, cover and locknut; floating nut in counterbored boss on shoulder screws with axial play; radial guide; motor body, pilot, shaft on standoffs) | PASS | All parts identifiable at 100 percent. The axial play (sub-mm) is below drawing resolution; the label states radial float 0.5 and the shoulder-screw head reads above the flange. |
| V10 addition (fixed parts; nut_station_park at load) | PASS | As V10. |
| Section convention (cut hatched, beyond in elevation, hidden dashed) | PASS | Cut: rails and member c cross-hatched, plate, ring, boss, gear, receiver, collet, anchor block single-hatched by material, nut brass dots. Unsectioned outlines: screw, shafts, coupling, core, head. Beyond: rear standoffs solid. Hidden: core edges inside the head dashed, wing nut and collar dashed, screw end inside the coupling dashed. |
| Radial symmetry in the inset (Topologist 1.2 (c) NOTE 1) | PASS | Members, 42 squares and switch marks at a and b are the c set rotated by +-120 deg: squares turned with faces radial, switch marks on the outboard radial of each screw. |

## 4. V9

From the figure alone: each screw is fixed at the bottom by two back-to-back angular-contact bearings in a 42 block with cover and locknut on an arm off its frame member, guided radially only at the top on a second arm, driven from below by its own NEMA 17 through a beam coupling, and synced by one controller with three drivers and a home switch per screw (no belt); the 1000 N cut acts up on the head and puts the screw between anchor and nut in tension (247.5 N per screw); the self-locking Tr12x3 lead holds the ring with power off; the axial loop closes head - core - core seat - collet - receiver - base plate - base frame (off the plane) - member c - anchor arm - block - bearings - locknut - screw (tension) - nut - boss - ring - bearing - tube - head.

Spec question: "How is each screw anchored, guided, driven and synced, does the 1000 N axial load put it in tension, what holds the ring with power off, and does the axial load loop close?" Six of six clauses answered.

## 5. Findings

Overall S3 r3: **FAIL**. Failing items: V8 (1). Findings: 2. Both are text and mark placement; no part coordinate moves.

**F1 (V8; row span_lt).** Label "S3-2 span L_t, K 0.7 870": the printed value follows K, so the reader takes 870 as part of the K term; the row's own shape text says 'L_t 870, K 0.7'. Fix: label text so the value lands after L_t, e.g. text "S3-2 span, K 0.7; L_t" with the same expr, printing "S3-2 span, K 0.7; L_t 870". Dry-run: `check_sketch.py s3 --rev 4`, K4 (printed value against expr) and K9 green.

**F2 (V8; row hold_callout, s3_jackscrew_section.py l.134-138).** The callout mark runs from the outboard screw edge (u -166) to u -196 at z_S about 790, pointing at nothing; the placer's leader comes from the label column on the right, crosses the screw outline and both root lines, and ends at the mark's root on the far edge. Fix: start the mark on the inboard edge (u0 = us + nominal / 2, running toward +u, ending at about u -124, clear of the span line at u -110), so the leader ends on the near outline without crossing the screw; or end the leader on the right outline and drop the mark if K9 coverage is carried by the label. The mark end is a coordinate: dry-run `check_sketch.py s3 --rev 4`, K4 leader rules, K7 reference row against span_lt and the extension lines, K9 hold_callout drawn.

NOTES (no verdict effect):
- N1 (inset): the 42 anchor square (solid) and the 42 NEMA 17 square (dashed) coincide, so each reads as one square with mixed edges; acceptable as drawn since both are 42.
- N2 (nut_station_park): the park tick is unlabelled (spec label null); identified only through the legend's "dash-dot: nut stations at start and park". "nut at start" prints no value (start depends on c).
- N3 (legend): grey fill on the NEMA 17 and NEMA 23 bodies is not named in the hatch legend; the legend lists "plastic" with no pattern.
- N4: S3-3 red in the r3 record on stale S1 r7 / S2 r5 certifiers (Corrections 3).

## 6. r1 findings F1 to F7 on r3

| r1 finding | Status on r3 | Evidence |
|---|---|---|
| F1 (scale; screw set illegible) | Closed | Section Axes enlarged to about 2.48 px/mm (r1 0.82): anchor block about 104 px, balls about 10 px, nut, shoulder screw head, cover, locknut, coupling, standoffs, pilot readable at 1:1. |
| F2 (leaders through label text) | Closed | No leader crosses any text in the section or inset. The hold leader now crosses the screw body instead (r3 F2). |
| F3 (duplicated callout text; hold text touching inset tick) | Closed | Hold and sync callouts print once; hold callout sits at z_S about 750, far from the inset. |
| F4 (sync fan from an empty point) | Closed | Fan apex is the callout's anchor at the inset edge, joined to the label's leader. |
| F5 (switch c under A-A; +Y overprinted) | Closed | Switch c outline visible over the A-A line; "+Y" set right of the line. |
| F6 (axial loop not shown; "chain" legend wording) | Closed | Figure note carries the axial-loop line naming where it leaves the plane; legend reads "dash-dot:". |
| F7 (span on the screw centreline) | Closed | Span is a red dimension line at u -110 with extension lines from the anchor and guide bearing lines. Its label text is r3 F1. |

## Footer: control scoring

Reviewer verdicts: ctrl_a FAIL V3, ctrl_b PASS, ctrl_c PASS handedness, ctrl_d FAIL handedness. Orchestrator scoring against key.json (2026-11-26): 4 of 4 correct (ctrl_a FAIL V3, ctrl_b PASS, ctrl_c PASS handedness, ctrl_d FAIL handedness, each as keyed). The reviewer model is credited for this gate.

## Gameplan lines to change

none (the orchestrator writes the Progress Log row for this return and the Design Notes 13 S3-r3 row at STOP M2).

## Designer delta read r4

Reader: The Designer (image-capable), raiser of D-r3-1 and D-r3-2. Delta read only, not the fresh M1 of record on r4. Scratch: D:\Unleashed Robotics\_scratch\cutjig\des_r4\ (crops r3_*/r4_* at 2x and 6x; probes\deltest.py, probes\base.log, probes\term_premise.log).

### Corrections to the brief

1. wip/s3_jackscrew_section_r4.png: 4157 x 3876 px, SHA-256 7c778b0067cf5ac04b330620a221cf8ff7c68116a85e9df8e0a472a055404adb (MEASURED). 53 363 px differ from r3 (MEASURED), in five places: the span ends (rows 300 to 560, px 600 to 800), the span-label and top-guide leaders (rows 380 to 400), the hold leader and mark (rows 1400 to 1500), the anchor cover (rows 2400 to 2560, px 500 to 800), the legend line (rows 3500 to 3600). No part outline moved.
2. The top-guide label leader lay exactly on the span extension line at z_S 1210 in r3 (hidden under the red); in r4 it lies 1 to 2 px above it (rows 384 to 385 against 386 to 387, MEASURED). See NOTE DR4-1.

### 1. M1 r3 findings on r4

| Finding | Status | Evidence (MEASURED, r4 pixels) |
|---|---|---|
| F1 span label | Closed | Label prints "S3-2 span, K 0.7; L_t 870": the value follows L_t; K 0.7 stands apart behind the semicolon. Legible at 1:1, no overlap with "top guide (radial only) z_S 1210 ..." above it. |
| F2 hold mark | Closed | Mark runs from the inboard screw edge (px 602, u -154) to px 675 (u -124), 14 mm clear of the span line at px 709.5 (u -110). The leader from the label column ends at the mark's free end (gap about 3 px) and crosses neither the screw outline nor its root lines. The mark reads as a leader shoulder touching the screw. |

### 2. Cover hatch '||' and the arrowhead terminators

- Cover '||': PASS. Each cover piece above the joint shows two vertical lines, perpendicular to the joint and to the piece's edges; it reads as a hatched piece of its own, set apart from the '//' block below and from the bearing rows. The r3 '--' doubled-edge reading is gone. Legend reads "aluminium // (anchor cover above the joint ||)".
- Terminators: PASS. Two filled red arrowheads, tips on the extension lines at z_S 1210 (row 386) and 340 (row 2519), pointing outward to the extension lines from inside the span. The `_` marker is gone: red past the dimension line is now the extension line alone, px 601 to 724 against the line at 709.5, about 6 px (2 mm) overshoot, e3 bound met. D-r3-1 closed. The span-label leader lands on the flank of the upper arrowhead (px 717, row 397): it names the dimension at its terminator; acceptable.

### 3. Relief: K8 reference-line terminator relief, premise `terminator_issues`

**SIGNED.**

- Rule (DECLARED, sketch_common.py l.4366 to 4370, l.1140 to 1166): in a side or section view, a `kind: line`, `reference: true` row reads its projected tests (projected_x, projected_extent, section_u, sense predicates) through `geom_pieces`, which drops the row's FancyArrowPatch artists. Premise: every FancyArrowPatch of the row has tail and head within TOL_Z 0.05 of the row's Line2D ink (`terminator_issues`); a row with arrows and no line ink fires (distance inf). The relief removes FancyArrowPatch only, and the premise covers exactly FancyArrowPatch, so nothing is relieved unchecked.
- Base run on a copy of docs/sketches (des_r4\sk, 13-control subset K8-Z14, Z16, Z17, B79, B80, B88, B89, K5-Z6, Z7, B44 to B47): 13 of 13 match (MEASURED, probes\base.log). K8-Z17 clean on the live S3; K8-B88 fires 2 "projected_x: drawn x centre -105.00" (the relief does not hide a moved line); K8-B89 fires 2 with the terminator reason (tail and head of the planted arrow 10 off the line).
- Deletion test (des_r4\del_term_premise, one edit: the `issues += terminator_issues(ax, fid, pose)` call at l.4370 replaced by `pass`): K8-B89 clean, **mismatch**; the other 12 controls match (MEASURED, probes\term_premise.log). The premise branch is held by B89 alone.
- Red-first: Engineer r4 table (DECLARED). On the r3 code K8-B89 fires 2 on the projected_x / extent reason, not the terminator reason; the manifest matches B89 on "span_lt terminator: arrow tail" and "off the line (D-r3-1)", so on r3 it is a reason mismatch, which counts as red. K8-Z17 fires on r3 (extent x [-111.14, -108.86], by 1.14): red. B88 is a guard, not red-first; acceptable.

NOTES on the relief (no condition of the signature):
- DR4-2. The premise bounds where an arrow sits, not its size: an arrow lying on the line with a head of any width (mutation_scale) or a curved connectionstyle bulging off the line passes. The live heads are LABEL_FONTSIZE long, half-width 1.14 mm (MEASURED via K8-Z17 on r3). A head-width bound (for example half-width <= 2.0) and straight-only connection would close it; for the owner of the next K8 delta.

### 4. New legibility

- DR4-1 (NOTE). Both bearing-line label leaders run parallel to the span extension lines and land on the block edge at px 643 (u -137): the top-guide leader 1 to 2 px above the upper extension line over px 643 to 724 (33 mm), the anchor-bearing leader about 5 px (2 mm) below the lower one (unchanged from r3, passed by M1 r3). Each reads as a doubled extension line; the labels stay clearly attached. Drafting practice keeps a leader off the line of an adjacent extension line. At the next drawn revision, anchor these two leaders on the block faces at a z off the bearing line (for example mid-height of the guide block and of the anchor block above the joint), with a dry run of K4 leader rules and K9. No verdict effect on r4.
- No other new item: no label overlaps, no leader crosses text, the hold leader crosses the drill tube and core outlines as in r3.

### Verdict

Delta read S3 r4: **PASS** (F1, F2 closed; '||' and arrowheads PASS). Relief (K8 reference-line terminator relief, premise `terminator_issues`, K8-Z17, B88, B89): **SIGNED**. NOTES DR4-1, DR4-2 carried. The revision Sean accepts still needs a fresh M1 PASS file on the r4 pixels (KC11).

### Gameplan lines to change

none (the orchestrator writes the Progress Log row for this return).
