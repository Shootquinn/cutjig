# Step 1.3 (h) r2 re-check (P7r), The Loftsman

Date 2026-11-26. Under review: S3 r2 (`docs/sketches/wip/s3_checks_r2.json`, `s3_jackscrew_section_r2.png`, `s3_summary_r2.md`), the r2 spec edits that need a placement signature, and the closure of LF1.3-1 and LF1.3-3. Section screw: c (theta 270, YZ plane).

Read: `step1.3_loftsman_crossreview.md`, `step1.3_engineer_revision_r2.md`; `docs/sketches/s3_spec.yaml` (chains, load_cases, reported_items, not_drawn, home_switch_a/_b/_c, span_lt, section_line, plan_axes), `checks_s3.py` (`_face_issue`, `link_kind_issues`, `s3_3`, `reported`), `checks_s2.py` (`accepted_s1_mass_report`), `s3_jackscrew_section.py` (lever), `sketch_common.py` (`tagged`, `pieces`), `proposed_params.yaml`, `params.yaml`. Also the Engineer's F7 dry runs (`_scratch\cutjig\p9r2\dry_f7_110`, `dry_f7_210`).

Runs:
- Copy of `docs/sketches/` at `D:\Unleashed Robotics\_scratch\cutjig\lof_r2\sk\`, with `params.yaml` beside it. The dry-run copy is `lof_r2\sk_dry\`. TMP and TEMP point to `_scratch\cutjig\tmp`.
- Records folder `lof_r2\records\`:
  - S1 r7, S2 r5 and `s1_mass_report_r7.json`, copied from `docs/sketches/`.
  - `wip/s1_checks_r8.json` and `wip/s2_checks_r9.json` with `accepted: true`. Apart from that field, both are equal to the wip files (MEASURED).
  - `wip/s1_mass_report_r8.json`.
- Scripts: `lof_r2\scripts\probe.py` (face links, lever, crossings at the dimension offsets, inset centres) and `spans.py`.
- Nothing under `docs/sketches/` was edited.

Tags: MEASURED (read from a run here), DERIVED (hand arithmetic), DECLARED (spec, overlay or ruling), ASSUMED (working value).

## Corrections to the brief

1. **The S3-3 listing has 30 entries, and 12 of them are declared.** The Engineer's report gives 15 declared plus 1 face_record, 9 fastened and 8 by symmetry, which makes 33. With S1 r8 accepted, core_seat|collet passes on its record certifier "S1 collet|core_seat C". It is therefore not listed as declared in chains c, a and b. 12 + 1 + 9 + 8 = 30 (MEASURED). The 48-link count holds.
2. **`kept_axial` still names the holder after the reroute.** The Engineer flagged this item to me. It is FIX LF1.3-10 below.
3. **The context's accepted-state line is still out of date.** `--stale` on the copy's own records (S1 r7, S2 r5) reports 5 differences: jackscrew.lead, jackscrew.nominal and liftmotor.coupling_length (MEASURED). This is unchanged from my (e) Correction 1.

## 1 S3-3 re-run with S1 r8 and S2 r9 accepted

- `--stale --docs-dir records`: 2 records, 0 differences. X1 passes on 70 rows (MEASURED).
- `s3 --rev 2 --docs-dir records`: **14 of 16 pass** (MEASURED).
  - K4 fails on D1, a Designer value.
  - K8 fails on TP1.3-12 and TP1.3-14, both Designer values.
  - **S3-3 passes: 48 links closed in the cut case.**
  - S3-1: 25.84. S3-2: P_cr 1363.8 N, least margin 3.97. RPT: 10 items.
- The script run on the copy renders the same pixels as `docs/sketches/wip/s3_jackscrew_section_r2.png`: 1603 x 4307 x 4, `numpy.array_equal` True (MEASURED).
- Chain count:
  - c has 18 links, a and b have 15 each, for 48 in total (DERIVED).
  - At r1, each chain had core_seat|collet, collet|holder and holder|receiver. At r2 it has core_seat|collet and collet|receiver. That is one link fewer per chain: 51 - 3 = 48.

## 2 Chain reroute: the new seat faces and the load sense of every face link

The cut-case loop (DECLARED arrow +Z on the cutter; DERIVED):
- The core pushes the cutter up. The drill tube, bearing, ring and nut housing carry that push to the nut flange.
- The nut pulls the screw up, so the screw is in tension. The screw pulls the locknut up, and the locknut lifts the lower inner race. The races push the cover up, and the cover passes the load through the block, arm and member c into the base frame.
- On the base side, the core presses down on the seat, the collet foot on the receiver floor, the receiver shoulder on the plate, and the plate on the frame.

A face link carries the cut-case load when the upper piece is pressed down onto the lower piece. This is the sense `_face_issue` tests: x lies above the face and y below it.

**Hand values at capture_end.** z_S = z_A + 60 (DECLARED). Spans in u, centre u = 0 for base rows and -160 for screw c rows.

| Link (x above, y below) | Face z_A / z_S | Hand (DERIVED) | Drawn x bottom edge / y top edge (MEASURED) | Overlap per side, hand = drawn |
|---|---|---|---|---|
| core_750 \| core_seat (new route) | 40 + 2.5 = 42.50 / 102.50 | core r 50 (d 100); ledge r 50 - 3 = 47 to 50 | -50.00 to 50.00 / -50.00 to -47.00, 47.00 to 50.00 | 3.00 |
| collet \| receiver (**new seat face**) | icd.floor_above_datum_a 40 / 100.00 | collet foot r 50 to register_bore_radius 67.29; floor r 80 / 2 = 40 to 67.29 | -67.29 to -50.00 (both sides) / -67.29 to -40.00 (both sides) | 67.29 - 50 = **17.29** |
| receiver \| base_plate | receiver.shoulder_z 12 / 72.00 | shoulder r to 100; plate hole 160.4 / 2 = 80.2 | -100.00 to -40.00 (three spans) / -239.00 to -80.20 | 19.80 |
| anchor_c \| anchor_bearing_c | 280 + 8 = 288 / 348.00 | cover bore r 8 to 21 from the screw axis; race r 5 to 13 | -181.00 to -168.00, -152.00 to -139.00 / -173.00 to -165.00, -155.00 to -147.00 | 5.00 |
| anchor_bearing_c \| anchor_locknut_c | 280 - 8 = 272 / 332.00 | locknut r 5 to 9 | -173.00 to -165.00 / -169.00 to -165.00 | 4.00 |
| nut_c \| nut_housing_c | 320.84 + 15 - 8 = 327.84 / 387.84 | flange r 6 to 21, interrupted by the shoulder-screw hole at r 16 ± 3.5; shoulder r 11.5 to 25, interrupted by the M5 hole at r 16 ± 2.5 | flange -181.00 to -166.00, -154.00 to -147.50, -140.50 to -139.00 / housing -185.00 to -171.50, -148.50 to -146.50, -141.50 to -135.00 | outboard 9.50; inboard 1.00 and 1.50 |

The sense of each face link in the cut case (DERIVED). Every link is written upper piece first, as `_face_issue` reads it.

| Link | Force on x from y | Sense | `_face_issue`, sense on (MEASURED) |
|---|---|---|---|
| core_750 \| core_seat | +Z (the seat holds the core up against the cutter) | compression | None |
| collet \| receiver | +Z | compression | None |
| receiver \| base_plate | +Z | compression | None |
| anchor_c \| anchor_bearing_c | +Z (the upper outer race lifts the cover) | compression | None |
| anchor_bearing_c \| anchor_locknut_c | +Z (the locknut, pulled up by the screw, lifts the lower inner race) | compression | None |
| nut_c \| nut_housing_c | +Z (the housing shoulder lifts the flange) | compression | None |

The other link kinds, checked against the same loop (DERIVED):
- **Fastened.** These faces would open in tension or are side faces:
  - base_frame|frame_upper_c: the member foot on the rail is pulled up by 254.04 N.
  - base_plate|frame_upper_a/_b: the member feet on the plate are pulled up by 254.04 N each.
  - Bracket to member: side face, shear.
  - Block to arm end: vertical face at r 181, shear.
- **base_plate|base_frame (face_record).** In compression: 1000 - 2 x 254.04 = 491.93 N down. The frame then takes 254.04 N up from member c, which leaves W = 237.89 N to the floor. The sum closes at W 24.25 kg; LF1.3-2 is still open.
- **Thread links.** screw|nut: the nut is above the anchor in every pose, so the screw is in tension (S3-1 least 25.84). locknut|screw: M10x1, in tension.
- **The holder is outside the route.**
  - collet|holder: the only horizontal contact is at z_S 132.00. The holder bottom edge (-67.29 to -50.00) lies on the collet top edge (-61.65 to -50.00) with an overlap of 11.65 (MEASURED). The holder is the upper piece. Under the cut load the collet is pushed down and away, so this face unloads.
  - holder|receiver: no horizontal contact is drawn (MEASURED).
  - The reroute matches the drawing. The holder carries 0 N of the cut reaction (DERIVED).

**Placement: SIGNED.** The chain reroute, the link kinds and the face expressions are signed.

## 3 Lever expressions r sin(theta)

`home_switch_c.lever` (DECLARED), u = r sin(jackscrew.angle[2]), theta 270:

| Point | Hand u (DERIVED) | Hand z_A / z_S (DERIVED) | Drawn (MEASURED) |
|---|---|---|---|
| from (switch body, inboard bottom corner) | 190 sin 270 = -190.00 | 1165 - 30 - 13 = 1122.00 / 1182.00 | (-190.00, 1182.00) |
| to (roller tip, free state) | 182 sin 270 = -182.00 | park tip 959.84 + 130 + 12 / 2 + 30 / 2 + lever_free_gap 1.16 = 1112.00 / 1172.00 | (-182.00, 1172.00) |

- The tip lies 3.00 inboard of the housing rim (r 185) and 1.16 above the housing top at park (1110.84 z_A, DERIVED; MEASURED by the same expression in `check_stack`).
- r sin(theta) is the section u (plan y) at any theta. At theta 270, the depth r cos(theta) is 0.00, so the lever lies in the plane.

**SIGNED.**

## 4 Inset move and home-switch positions

- The inset Axes now sits at figure bounds (1.2135, 0.50, 0.30, 0.42) and is saved through `bbox_inches="tight"`. Its limits are x and y ±340, equal aspect (MEASURED).
- The move changes only figure coordinates. Every plan coordinate below equals its hand value and its r1 value (MEASURED and DERIVED):

| Row | Hand (DERIVED) | Drawn centre and extent (MEASURED) |
|---|---|---|
| home_switch_a (r 190 to 210, hw 3, theta 150) | centre 200 (cos 150, sin 150) = (-173.205, 100.000); x -164.545 to -181.865 ∓ 1.5 = -183.365 to -163.045; y 95 to 105 ∓ 2.598 = 92.402 to 107.598 | (-173.205, 100.000); x -183.365 to -163.045; y 92.402 to 107.598 |
| home_switch_b (theta 30) | (173.205, 100.000), mirror of a | (173.205, 100.000); x 163.045 to 183.365 |
| home_switch_c (theta 270) | (0, -200.000); x ±3; y -210 to -190 | (0.000, -200.000); x -3.000 to 3.000; y -210.000 to -190.000 |
| screw_a / _b / _c | 160 (cos theta, sin theta): (-138.564, 80), (138.564, 80), (0, -160) | equal |
| anchor_a (42 square) | ±21 (cos 30 + sin 30) = ±28.687 about (-138.564, 80) | x -167.251 to -109.878, y 51.313 to 108.687 |
| frame_upper_a | (-237.291, 137.000) ± 40.981 | x -278.272 to -196.310, centre (-237.291, 137.000) |
| liftmotor_c, anchor_c | x ±21, y -181 to -139 | equal |

- The home switches draw at zorder 9. The A-A line draws at zorder 1 and 2, and screws at 7, so switch c reads above the cutting-plane line on x = 0 (F5, MEASURED).

**SIGNED.**

## 5 Dimension offset options (span_lt, u -210 / u -110)

The live r2 row draws span_lt at r_in = pitch_radius, u = -160.00, on the screw axis over z_S 340.00 to 1210.00. The line runs inside screw_c, and load_tension_c lies on it (MEASURED). The table below lists what each offset meets at capture_end, the only pose the section draws. The probe checks a vertical line at u over z_S 340 to 1210 and horizontal extension lines at z_S 340 and 1210 (MEASURED; hand u = r_in sin 270, DERIVED).

| | u -210 (r_in 210) | u -110 (r_in 110) |
|---|---|---|
| Line lies on an outline | ring OD edge, z_S 374.84 to 386.84 (12.00); home_switch_c outer face r 210, z_S 1182.00 to 1195.00 (13.00) | none |
| Line runs inside a solid piece | bracket_anchor_c, 340.00 to 355.00; bracket_guide_c, 1195.00 to 1210.00 | ring plate piece u -135 to -100, 374.84 to 386.84 (12.00); gear teeth u -126.32 to -90, 476.37 to 500.84 (24.47). Both are moving parts, cut |
| End points | both inside the arm sections (anchor arm z_S 325 to 355, guide arm 1195 to 1225; both arms r 181 to 244) | both in free space |
| Extension line from the axis (-160) | 50.00 long; crosses screw 5, block 8 (anchor end) or block 8 and guide bearing 8 (guide end), arm 29 | 50.00 long; crosses screw 5, block 8 (with guide bearing 8 at the top end); free from -139 to -110 (29.00) |
| Extension line from the bearing-line end | -173 to -210, 37.00; crosses block 8 and arm 29 | -147 to -110, 37.00; crosses block 8 only |

- Every inboard u between the housing (-135) and the drill tube crosses the ring plate at capture_end.
- Every outboard u between the block face (-181) and member c (-244) puts both end points inside the arms, because the bearing lines (280 and 1150 z_A) lie within the arm z bands.
- **u -110: placement SIGNED.**
- **u -210: NOT SIGNED.** It lies on two outlines (ring OD, switch face), and both terminators sit inside arm sections.
- The Engineer's dry spec writes `r_in: 110` as a literal. The signed form needs an expression: for example a Designer leaf `section.dim_offset_lt` 50 (DECLARED) with `r_in: jackscrew.pitch_radius - section.dim_offset_lt`.
- The K8 projected_extent failure needs the `span_lt:ext` admission, with extent [u_c, u_dim], or [u_c + 13, u_dim] if the extension starts at the bearing-line end. That admission is the Designer's and the Topologist's (F7, returned).

## 6 LF1.3-1, -2, -3

- **LF1.3-1: CLOSED.** The RPT L_min item in `s3_checks_r2.json` reads "drawn bar 911.00 (screw_end_c bottom to guide_c top); with the shoulder-screw head 4.55 above the housing top: ... L_min 889.55, at anchor_z 890.39; ... L_min 1139.55, at anchor_z 1140.39" (MEASURED). These equal the hand values of my (e) remedy: 1165 - 254 = 911.00 and 400.39 - 395.84 = 4.55.
- **LF1.3-2: with The Designer, not re-checked.** W_kg is unchanged at 24.25 kg, and every RPT value equals r1 (MEASURED).
- **LF1.3-3: CLOSED.**
  - `s2 --rev 9 --docs-dir records` gives 18/18. `tip_force_footprint` reads 351 / 379 / 563 / 269 N with basis "s1_mass_report_r8.json tip_force_at_com_N (latest accepted S1 report)" (MEASURED).
  - The live wip S2 r9 still reads r7 until ORCH-B runs `--accept s1`, then re-runs `s2 --rev 9`.
  - See NOTE LF1.3-11 for the spec source text.

## 7 Findings

**FIX LF1.3-10 (`kept_axial` names the holder, contrary to the reroute).**
- Problem:
  - `checks_s3.reported` (l.490) prints "(collet, holder, receiver, base plate, compression)".
  - `s3_spec.yaml` reported_items kept_axial text and load_cases cut `kept_parts` say the same.
  - Section 2 shows that the holder carries 0 N of the cut reaction in the drawing.
  - Stall down into a jam follows the same base route, core to seat to collet to floor, so the holder carries none of F_stall + W either (DERIVED).
- Remedy, text only:
  - `checks_s3.py` l.490: `" (collet, holder, receiver, base plate, compression)"` becomes `" (collet with its core seat, receiver, base plate, compression; the holder is outside the cut-case route, Topologist TP1.3-10 (a))"`.
  - `s3_spec.yaml` kept_axial text: `axial force in collet, holder, receiver, base plate at 1000 N and at F_stall + W (N5)` becomes `axial force in collet (core seat), receiver, base plate at 1000 N and at F_stall + W (N5); the holder is outside the cut-case route (Topologist TP1.3-10 (a))`.
  - load_cases cut: `kept_parts: "1000 compression (collet, holder, receiver, base plate);` becomes `kept_parts: "1000 compression (collet with its core seat, receiver, base plate; holder outside the route, TP1.3-10 (a));`.
- Dry run (`lof_r2\sk_dry`, records with S1 r8 and S2 r9 accepted, MEASURED):
  - 14/16, with every check's result, issue count and reason equal to the undried run.
  - RPT passes on 10 items. kept_axial reads "1000 N at the cut; mu 0.15: 1267.43 N at F_stall + W; mu 0.2: 1084.54 N at F_stall + W (collet with its core seat, receiver, base plate, compression; the holder is outside the cut-case route, Topologist TP1.3-10 (a))".
  - The PNG is pixel-equal to the r2 of record.
- Effect: no pixel changes and no revision opens. The value sent to Quinn as N5 (B2-7) keeps its numbers, but its part list loses the holder.

**NOTE LF1.3-11 (S2 spec source text still names r7).**
- `s2_spec.yaml` l.94 reported_items tip_force_footprint `source` reads "s1_mass_report_r7.json ...".
- The drawn basis and the summary read r8 from the records (MEASURED). The summary prints the basis, not the source.
- Correct the source text at the next S2 spec edit.

**NOTE LF1.3-12 (anchor faces measured against a bearing drawn solid).**
- The section draws each bearing as one block per side, from r 5 to 13 about the screw axis. The race split is not drawn.
- The cover (r 8 to 21) and the locknut (r 5 to 9) overlap radially over r 8 to 9.
- "Cover on the outer race only" and "locknut on the inner race only" hold together only if the inner ring outer edge is at r 8 or less and the outer ring inner edge is at r 9 or more.
- Catalogue 7000-series 10 x 26 x 8 shoulders (ASSUMED, unchecked: d1 about 14.2, D1 about 21.6) satisfy this. The true contacts would then be about 2.2 (cover) and 2.1 (locknut), against the drawn 5.00 and 4.00 (DERIVED from the ASSUMED shoulders).
- To the Step 2 bearing row: cover bore and locknut OD against the catalogue d1 and D1.

Counts: BLOCK 0, FIX 1 (LF1.3-10), NOTE 2 (LF1.3-11, -12). LF1.3-1 and LF1.3-3 are closed; LF1.3-2 is with The Designer.

**RE-SIGN PASS (S3 r2 placement), with FIX LF1.3-10 (text only, dry run clean, no revision).**
- The chain reroute and seat faces, with every face link in compression in the cut case: section 2.
- The lever expressions: section 3.
- The inset move and home-switch positions: section 4.
- Offset u -110 is signed; u -210 is not: section 5.
- S3-3 closes 48 links with S1 r8 and S2 r9 accepted.

## Gameplan lines to change

1. l.293 (Reported), applies with LF1.3-10:
```
Old: axial force in each kept part (collet, holder, receiver, base plate) at 1000 N and at F_stall, for Quinn's N5 ruling;
New: axial force in each kept part (collet with its core seat, receiver, base plate; the holder is outside the cut-case route at S3 r2, Topologist 1.3 (e) TP1.3-10 (a), Loftsman 1.3 (h) re-check LF1.3-10) at 1000 N and at F_stall, for Quinn's N5 ruling;
```
2. l.580 (Design Notes 16), append after the line's last text `with the base frame supporting the plate (Loftsman R1).`:
```
Old: with the base frame supporting the plate (Loftsman R1).
New: with the base frame supporting the plate (Loftsman R1). Updated at 1.3 (h) r2: the drawn base route is core, core seat, collet foot on the receiver floor, receiver shoulder on the plate top; the holder carries no cut-case axial load in the drawing (Topologist TP1.3-10 (a); Loftsman re-check LF1.3-10), so the N5 part list is collet, receiver, base plate.
```
