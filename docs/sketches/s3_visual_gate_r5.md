# S3 r5 M1 visual gate (P8r, fresh reviewer)

## Corrections to the brief

1. The P8 prompt also gates S2 r<m> and S1 r8. Per the orchestrator, this spawn gates S3 r5 only; no S2 or S1 file is written.
2. `docs/sketches/wip/s3_checks_r5.json` records S3-3 **fail** (15 of 16 checks pass; S3-3 is red on the stale S1 r7 / S2 r5 records, cause content). M1 does not score check results. S3 is not acceptable while S3-3 is red, whatever this gate says.

Image read: `docs/sketches/wip/s3_jackscrew_section_r5.png`, 4157 x 3876 px (MEASURED), Read as an image at the full figure and in crops at native and 3x resolution (scratch `D:\Unleashed Robotics\_scratch\cutjig\p8r5\`). Leader endpoints were traced from the pixels (gray leader ink, `trace.py` in scratch) and converted at 2.447 px/mm in u and 2.453 px/mm in z (DERIVED from the axis ticks).

## 1 Reviewer-model controls (unlabelled; key.json not opened)

| Figure | Verdict | What I see |
|---|---|---|
| ctrl_a.png | FAIL V3 | The 177.8 cutter block sits at the top of the drill tube (z 1090 to 1195). The tube's lower end at 245 has no head. The tail is on the nose. V1, V2, V4 and V5 read correctly. |
| ctrl_b.png | PASS V1 to V5 | Cutter at the bottom (245 to 350) and top-end block at 1045 to 1195. Core upright from 100 to 605. Screw vertical with its nut on the ring and blocks at the bottom and top. Floor at 0. |
| ctrl_c.png | PASS handedness | +X right, +Y up, theta arc counter-clockwise from +X to +Y. Screw a at 30 deg upper right, b at 150 deg upper left, c at 270 deg at (0, -160). |
| ctrl_d.png | FAIL handedness | The +Y arrow points down the page while the y tick labels increase upward. The theta arc runs clockwise from +X. Screw c, labelled theta 270, is drawn at y +160 and screws a and b sit below the X axis. The figure is mirrored about X. |

## 2 S3 r5 rubric (section A-A through screw c, theta 270, YZ plane; pose capture_end)

| Item | Verdict | What I see |
|---|---|---|
| V1 | PASS | The floor line is at z 0 at the bottom. The NEMA 17 (grey, hatched) hangs under the anchor block on two standoffs with a coupling between them. Nut c sits in the ring housing at z_S about 375 to 403. Ring, drill and core read with top on top. |
| V2 to V4 | N/A | S3 applicability is V1, V5 to V10. |
| V5 | PASS | Screw c is vertical at u -160. The fixed anchor block, with two ball pairs, a cover above and a locknut below, is on the anchor arm at z_S 325 to 355. The radial top guide (one ball pair in a block) is on the top-guide arm at 1195 to 1225. The nut is in the ring boss at 375 to 403, between them. The anchor bearing line lies below the nut. |
| V6 | PASS | The section shows rectangles only, except the ball circles admitted as sub-artists. Circles (screws, housings, keep-out r 86.2, ring rim r 210) appear only in the plan inset. |
| V7 | PASS | Jack screw: unsectioned outline with dashed thread root, a flanged brass nut in a counterbored hatched boss with the rear shoulder screw and its head above the housing top, the anchor with two balls per side between cover and locknut, and the top guide with a radial ball pair. Thrust bearing: reads as a bearing pair in a block. NEMA 17: body, pilot plate and shaft into the coupling, with the coupling showing a dashed shaft inside. Hold device: drawn as what it is, the self-locking lead, with its label on the screw (lambda 5.20 deg < phi_n; brake and park pin options to Step 2). Inset: three screws at 30, 150 and 270 deg, each with its housing circle, anchor square and home switch, plus the sync callout with leaders to all three screws ("one controller, three drivers, home switch per screw at park; no belt"). Gear and pinion c read as a bevel pair: the pinion's axis is radial (horizontal dash-dot), its small end inboard, and it sits under the gear's down-facing tooth face with the NEMA 23 c outboard. |
| V8 | **FAIL** | F1 and F2 below. Text is legible at 100 percent, no two text boxes overlap, and the long hold label clears the inset (inset axis bottom about z_S 640 against the label at 765). The sync callout ends 16 px inside the image edge (MEASURED, last dark column 4141 of 4157). |
| V9 | PASS | See section 4. |
| V10 | PASS | The spec carries the two S3 operator rows. Collet change: the wing-nut sweep r 115 (157 to 213) is labelled. Coupling c is at u -160 (r 150 to 170, z_S about 300 to 323), above and outboard of the hand zone, between the standoffs, and visibly exposed. That exposure is the Step 2 guard row. Load under the parked ring: the park nut-station tick at z_S 1155.8 (DERIVED from the pixels; check_stack park nut 1095.84 z_A + 60) places the ring head-high over the collet. The figure shows no hold state, as the table records (Step 2). |

### S3 rubric additions

| Addition | Verdict | What I see |
|---|---|---|
| V1 NEMA 17 under the anchor on standoffs; nut in the ring housing | PASS | As V1. |
| V5 anchor bottom, guide top, nut between; anchor line below the nut | PASS | Anchor bearing line at about z_S 340, nut bottom at about 375 at capture_end. |
| Section handedness (viewer +X, u = +Y right; screw c and member c left, pinion c and NEMA 23 c right) | PASS | Screw c at u -160 and member c at u -245 to -305 are on the left. Pinion c (u 95 to 140) and NEMA 23 c (u 140 to 218) are on the right. Title and note state the viewer at +X. With look direction -X and up +Z, right = (-X) x Z = +Y, which matches. |
| Inset handedness | PASS | +X right, +Y up, theta arc counter-clockwise. Screws at 30, 150, 270. The A-A line is on x = 0 with both arrows pointing -X (viewer at +X). |
| V6 rectangles in the section, circles only in the inset and balls | PASS | As V6. |
| V7 fixed anchor, floating nut with shoulder screws and play, radial guide; motor body, pilot, shaft on standoffs | PASS | As V7. Only the rear shoulder screw is drawn; the front one is cut away per the note. |
| V10 fixed parts and nut_station_park for the ring at load | PASS | As V10. |
| Section convention (cut hatched, beyond in elevation, hidden dashed) | PASS | Cut parts are hatched by material per the legend: member c and the arms crosshatched (extrusion), ring, tube walls, collet, receiver and plate in steel or aluminium patterns, the nut brass-dotted, the anchor cover in '||'. Unsectioned parts are outlines over the hatch: screw, coupling, core, head. Hidden edges are dashed: the core inside the unsectioned head, the thread root, the wing-nut edges behind the collet, the coupling shaft. The member at u 245 to 305, z 0 to 60, is the base-frame rail in section. |
| Radial symmetry of radial parts in the inset (Topologist 1.2 (c) NOTE 1) | PASS | Members a and b are rotated by their theta and member c is axis-aligned at 270. Anchor squares a and b are rotated by theta and c is axis-aligned. Home switches at r about 200 have their long axis radial at all three screws. The three screw sets are congruent under 120 deg rotation. |

### Findings

**F1 (V8; row load_comp_c, label "compression per screw: ...").** The leader runs horizontally at z_S 400.0. That puts it one display pixel below the z 400 major gridline (MEASURED: gridline at image row 2373, value 176; leader at row 2375, value 136) from the label column to its end at u -184.5. Along its 650 mm run it crosses the head, tube, core, keep-out lines, the S3-2 span line, the screw and the shoulder-screw head before it ends at the static-load arrow. At 100 percent it reads as a thickened gridline, and its end cannot be found by eye. The other 18 section leaders and 3 inset leaders are slanted or lie off the gridlines and can be followed. Fix: the leader must not run collinear with a gridline. Either end it on the load arrow shaft at a height that is not a multiple of 50 mm (minor grid pitch; for example the arrow-shaft midpoint, about z_S 412), or give the placer a gridline-clearance term. Dry-run the Engineer must run (detail 1 common (h)): re-render r6. Report each section leader's minimum vertical distance to the nearest grid line over its horizontal run (MEASURED from the leader artist path against the major and minor tick sets). The load_comp_c value must be >= 1.0 mm. K4 leader separation and K4 cases must stay green. Add a K4 B with a leader planted on z 400 that fires, red on the r5 code.

**F2 (V8; rows nut_station_start, nut_station_park).** "Every labelled feature dimensioned": the label "nut at start" carries no value. The park tick at z_S 1155.8 has no label at all; only the legend line "dash-dot: nut stations at start and park" identifies it. The two ticks set the S3-2 rigid segment and the ring height at load (V10), so a reader cannot tell from the figure where they stand. Fix: label both ticks with their nut-centre heights: "nut at start z_S 1030.84" and "nut at park (= load) z_S 1155.84". The values are DERIVED: check_stack nut centre 970.84 and 1095.84 z_A (tension_segment start 690.84 and park 815.84 above the anchor line 280.00) plus datum 60. Dry-run the Engineer must run: draw r6 with value_from on both station rows. K4 must read the printed value against check_stack nut_z per pose within 0.05. Add a K4 B where the start label prints 1020.84, red on the r5 code. Confirm with the placer that the new park label does not stack onto the "top guide" and "S3-2 span" labels (z_S 1210, 1206).

### NOTEs (no verdict impact)

- N1 (gear_c, label "gear PD 250"): the leader ends at (u 94.9, z_S 474.2), at the toe of the gear tooth face where the pinion's top corner touches it. The end reads ambiguously as gear or pinion. An anchor on the gear rim top (u 110, z_S 500) is unambiguous.
- N2 (frame_upper_c, "member c ... length 1225"): the leader crosses keep-out, tube, core and screw c to reach the member at u -242. It follows, but it is the longest crossing in the figure. A left-column label for the member removes it.
- N3: the ball circles in the anchor and top guide each carry one stroke of the surrounding race hatch through them. The screw interior is masked, so the balls are treated inconsistently. It still reads as balls.
- N4: the inset's blue dashed circle r 210 (ring rim) and the home-switch rectangles are unlabelled. The sync callout names the switches but its leaders go to the screws.
- N5: S3-3 is red on the stale records (Corrections 2).

## 3 Overall

**S3 r5: FAIL, 2 findings (F1, F2), both V8.** V1, V5, V6, V7, V9, V10 and every rubric addition pass.

## 4 V9

From the figure alone: each screw is fixed at the bottom in a block of two back-to-back angular-contact bearings on an arm from its 30-6060 member, guided radially at the top, and driven from below by a NEMA 17 through a coupling. One controller drives the three screws with three drivers and a home switch per screw. The 1000 N cut load puts the screw below the nut in tension. The self-locking Tr12x3 lead (lambda 5.20 deg < phi_n) holds the ring with power off. The axial loop closes head, core, core seat, collet, receiver, base plate, base frame (off the plane), member c, anchor arm, anchor block, bearing pair, locknut, screw c, nut c, boss, ring, bearing, drill tube, head.

Spec question: "How is each screw anchored, guided, driven and synced, does the 1000 N axial load put it in tension, what holds the ring with power off, and does the axial load loop close?" Every clause is answered by the figure. Match.

## 5 Raiser signatures, r5 rules (`research/sean/cr_scratch/step1.3_engineer_revision_r3.md` section r5)

Written after the scoring above. Scratch copy: `D:\Unleashed Robotics\_scratch\cutjig\p8r5\root\` (params.yaml plus `docs/sketches/` without wip/). An unmodified scratch render (`wip/s3_jackscrew_section_r96.png`) is pixel-equal to the gated r5 PNG (MEASURED, array equality), so the scratch copy reproduces r5. The baseline `--controls --only K4-Z7,K4-B25,K4-Z6,K4-B21` matches 4/4 (MEASURED).

### Rule 1: K4 cases label value check (K4-Z7, K4-B25). **REFUSED.**

Stated premise: "a label that prints several load-case values reads each from the load_cases entry at run time, so a change of W reaches the label."

- Deletion test: in the scratch copy I deleted the `if lab.get("cases")` branch of `sketch_common.k4`. `--only K4-Z7,K4-B25` then gives Z clean 1/1 and B fired 0/1: K4-B25 goes clean, match NO (MEASURED). The branch is live and B25 guards it.
- Premise test: `sketch_common.label_cases` reads `load_cases.<case>.per_screw` from s3_spec.yaml. Those are hand-entered literals (85.84, 119.85, 185.84, "343.18 / 282.21"). `checks_s3.loads` computes per_screw from the keys, and no check compares the two (grep of checks_s3, sketch_common, check_sketch, check_stack: no reader of the spec per_screw literals besides `label_cases`). I ran the K4-Z7 fixture in scratch with `ring.mass` 6.00 and then 10.00. At 10.00, `checks_s3.loads` gives static 98.92, capture 132.93, retract 198.92 N (MEASURED). The label still prints "static 86, capture 120, retract (F_bind 300) 186, stall up 343 N" and K4 passes at both masses (MEASURED, `p8r5\premise2.py`). A change of W does not reach the label. That is the r4 F1 defect class (a label stale against W), and the rule passes it.
- Fix to sign: `label_cases` takes its values from `checks_s3.loads(P, spec)["per_screw"]`, with stall_up as F_stall at the governing mu. Alternatively, K4 compares each spec per_screw literal against `loads()` within 0.005 N. Either way, add a B that sets `ring.mass` +4 kg with the spec literals unchanged and fires; it must be red on the r5 code (it is clean on r5, as measured above). K4-Z7 and K4-B25 stay.

### Rule 2: placer input `label_anchor_frac` (guide_c 0.83, anchor_c 0.95). **REFUSED.**

The rule puts the leader on the column-side face at a height fraction, so that the guide and anchor leaders leave the S3-2 span extension lines (z_S 1210, 340; DR4-1). In code, the candidate is admitted only when it lies on the row's ink (`ink_distance <= TOL_Z`). Otherwise the placer falls through to the default and ink anchors with no record.

- Deletion test: in the scratch copy I disabled the `label_anchor_frac` branch of `sketch_common.anchor_candidates`, then re-rendered (`r95`) and re-ran `check_sketch.py s3`. The top-guide leader ends at (u -137.3, z_S 1210.7), running along the red extension line at 1210. The fixed-anchor leader ends at (u -137.3, z_S 338.4), 1.6 mm below and parallel to the extension line at 340 (MEASURED by pixel trace; crops `p8r5\del_guide.png`, `del_anchor.png`). That is the DR4-1 defect back. Every S3 check gives the same result and the same reason text as the r5 record (15/16, S3-3 stale only; MEASURED, JSON compared check by check). No manifest control names label_anchor_frac. The premise is enforced by nothing: a later layout change that drops the candidate (as the 0.88 dry run did, falling back to 338) reverts the fix silently.
- Fix to sign: (a) K4 records the anchor source per leader. A row declaring `label_anchor_frac` whose leader does not end at that anchor (within TOL_Z) is an issue, with a B at frac 0.88 on anchor_c (the measured fallback) that fires. (b) A K4 leader-collinearity rule: a leader segment parallel to, and within 1.0 mm of, a reference-line row (span_lt and its :ext lines) over more than 5 mm is an issue. Add a B with the frac branch removed (the r95 layout) that fires, and a Z on r5. Rule (b) with grid lines added to the line set also catches F1. (c) A lint that frac lies in [0, 1]. All new Bs red on the r5 code.

## 6 Control footer

Reviewer verdicts recorded for the orchestrator's key.json scoring: ctrl_a FAIL (V3), ctrl_b PASS, ctrl_c PASS (handedness), ctrl_d FAIL (handedness). key.json not opened.

## Gameplan lines to change

none. Item 17 of `step1.3_engineer_revision_r3.md` (the l.138 K4 cases text) records Rule 1, which is refused above. Hold it until Rule 1 is re-signed.
