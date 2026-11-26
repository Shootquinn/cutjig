# S3 r1 visual gate (M1, Step 1.3 (f))

Reviewer: The Designer, fresh image-capable spawn; did not produce the images. Every PNG below opened with Read as an image; crops and zooms were made to D:\Unleashed Robotics\_scratch\cutjig\p8\. key.json not opened.

## Corrections to the brief

1. P8 READ FIRST 4 cites gameplan lines 178-206 for the rubric; V10 is at l.207. Lines 537-547 are Design Notes 6 to 11; Design Notes 13 (correction log) is at l.551-559 (DECLARED, gameplan as read 2026-11-26).
2. "S2 r<m> (r6 or the latest)": the latest is S2 r9 (wip/s2_plan_r9.png); gated in wip/s2_visual_gate_r9.md. S1 r8 is drawn; gated in wip/s1_visual_gate_r8.md.
3. S3 PNG is 4234 x 1559 px (MEASURED). The section Axes spans about x 440 to 1020 px for u -350 to +350 mm, 0.82 px/mm (MEASURED from tick positions); about 55 percent of the image width is blank.

## 1. Reviewer-model controls

| Figure | Verdict | What I see |
|---|---|---|
| ctrl_a.png | FAIL (V3) | The wide head block (labelled cutter OD ASSUMED 177.8) sits at the top, z 1090 to 1195, with the tube hanging below to 245. The drill is drawn tip up: the cutting head is not at the bottom. V1, V2, V4, V5 read correctly (floor at z 0, axis vertical, core upright, screw vertical with blocks at both ends). |
| ctrl_b.png | PASS | Head block at the bottom, z 245 to 350, tube above to 1195 with the top-end band at 1045. Floor at the bottom, axis vertical, core upright from 100 to 600, screw vertical. V1 to V5 pass. |
| ctrl_c.png | PASS (handedness) | +X arrow to the right, +Y arrow up, theta arc counter-clockwise from +X toward +Y. Screw a at 30 deg upper right, b at 150 upper left, c at 270 below the axis: consistent with the axes. |
| ctrl_d.png | FAIL (handedness) | +Y arrow points down; theta arc runs clockwise on the page from +X toward the downward +Y. Screw c labelled 270 deg is drawn at +y 160 (above), a and b below. Mirrored plan. |

## 2. S3 rubric (applicable: V1, V5 to V10; V2 to V4 N/A)

| Item | Verdict | What I see |
|---|---|---|
| V1 | PASS | Floor line at z_S 0 at the bottom. The NEMA 17 c (grey, steel hatch) hangs below the anchor block at about z_S 240 to 290 on the standoff stack; the brass nut sits in the boss on the ring at about z_S 380. Readable only at 4x zoom (F1). |
| V5 | PASS | Screw c vertical at u -160 from the anchor block (z_S about 300 to 330) to the top guide at z_S 1210 on the arm off member c; nut on the ring between them; nut-station ticks at start (about 1020) and park (about 1155) above the drawn nut. |
| V6 | PASS | Section: every part a rectangle or polygon; no circles in the section Axes except ball marks inside the bearings. Circles only in the inset. |
| V7 | FAIL | At 100 percent the screw set does not read as its parts: the nut, counterbored boss and inboard shoulder screw, the two angular-contact bearings, ball marks, locknut, coupling, standoffs, pilot and shaft are 2 to 35 px each (nut about 27 x 25 px, anchor block about 35 px wide, balls about 2 px). At 5x zoom: nut (brass fill) in a boss, anchor block with a red bearing line, grey motor below, a white stack between. The axial play, the shoulder screw head on the flange, the two separate bearings and the pilot cannot be told apart even zoomed. The red S3-2 span line runs on the screw centreline and reads as part of the screw (F1, F7). Inset: three screws and the single-controller callout read; the callout text is duplicated (F3). Hold device: the self-locking lead option reads from the callout text only (no drawn device; correct for that option). |
| V8 | FAIL | Leaders strike through label text: the power-off-hold leader passes through "S3-2 span L_t, K 0.7 870" and ends inside its own text at "self-locking Tr12x3 lead"; another leader strikes through "cut 1000 N up" and stops short of "HEAD". Hold and sync callouts repeat their own text. The hold callout runs to the inset's y tick labels (touching "-300"). Inset: "+Y" overprinted by the section line; home switch c hidden under the A-A line; a fan of three dotted leaders starts at an empty point (-320, 300) (F2 to F5). Detail illegible at 100 percent (F1). |
| V9 | FAIL | My sentence from the figure alone, below. The figure answers anchoring, guiding, drive, sync, tension and hold; it does not show the axial loop closing (F6). |
| V10 | PASS | Wing nut sweep r 115 (dashed band at z_S about 200 to 215) and the coupling stack at u -150 to -170, z_S about 290 to 325: hands at r <= 115 clear of the coupling by about 35 radially; ring at load is high (park tick at about 1155 z_S). Coupling guard and hold-state visibility are Step 2 rows in the operator table. Judged at zoom; at 100 percent the coupling region does not read (F1). |

## 3. S3 rubric additions, section convention, inset

| Item | Verdict | What I see |
|---|---|---|
| V1 addition (NEMA 17 hangs on standoffs under the block; nut in the ring housing) | PASS | As V1, at zoom. |
| V5 addition (anchor bearing line below the nut in every pose, radial guide at top, nut on ring) | PASS | Bearing line at about z_S 330, nut bottom above it at capture_end (harness S3-1 least 25.84 mm, MEASURED); start and park ticks higher. |
| Section handedness (u = +Y right; screw c and member c left, pinion c and NEMA 23 c right) | PASS | Member c (extrusion hatch) at u -300 to -240, screw at u -160; pinion c (hatched trapezoid with radial dash-dot axis) and NEMA 23 c (grey) at u +50 to +215, z_S about 440 to 520. Title states x = 0, seen from +X, u = +Y. |
| Inset handedness (+X right, +Y up, theta ccw; screws 30, 150, 270; A-A on x = 0, arrows toward -X) | PASS | Axes arrows +X right, +Y up; text "theta ccw from +X"; screws upper right (30), upper left (150), bottom (270); A-A chain line on x = 0 with both arrows pointing left (-X). No theta arc drawn; the text carries it. |
| V6 addition | PASS | As V6. |
| V7 addition (two bearings between shoulder, cover and locknut; floating nut in a counterbored boss on shoulder screws with axial play; radial guide; motor as body, pilot, shaft on standoffs) | FAIL | Not readable at 100 percent; at zoom the two bearings, shoulder screw, play and pilot are not distinguishable (F1). |
| V10 addition | PASS | As V10. |
| Section convention: cut hatched, beyond in elevation, hidden dashed | FAIL | Cut parts read: rails and member c cross-hatched, plate and ring single hatch, gear and anchor hatched; screw, core, head unsectioned outlines. The beyond layer (rear standoffs) and any dashed hidden edges sit inside the 30 px anchor stack and cannot be identified; the legend text states them but the drawing does not show them at a readable size (F1). |
| Radial symmetry in the inset (Topologist 1.2 (c) NOTE 1) | PASS | Members, anchor/motor squares and home-switch marks at a and b are the c set rotated by +-120 deg: squares turned 30 deg, switch marks on the outboard side of each screw. Switch c lies on the section line (F5). |

## 4. V9

From the figure alone: each screw is held at the bottom in a fixed angular-contact bearing block on an arm off its frame member, guided radially at the top on a second arm, driven from below by a NEMA 17 through a coupling, synced by one controller with three drivers and a home switch per screw; the 1000 N cut acts up on the head so the screw below the nut is in tension at 254.04 N per screw; the self-locking Tr12x3 lead holds the ring with power off; the loop closure is not shown.

Spec question: "How is each screw anchored, guided, driven and synced, does the 1000 N axial load put it in tension, what holds the ring with power off, and does the axial load loop close?"

Match on five of six clauses. The loop clause fails: there is no loop trace or loop note (S1 carries "axial loop: ..."; S3 does not), and at x = 0 the base plate's -Y end only abuts member c's side face; the plate-to-frame load path is off the plane (Designer 1.3 (a) Correction 8) and the figure does not say so. The legend line "chain: nut stations at start and park" uses "chain" for a line style, which reads against the spec's load chains.

## 5. Findings

Overall S3 r1: **FAIL**. Failing items: V7, V8, V9, V7 addition, section convention (5). Findings: 7.

**F1 (V7, V8, section convention; rows nut_c, nut_housing_c, nut_screws_c, anchor_c, anchor_bearing_c, anchor_locknut_c, screw_end_c, coupling_c, standoffs_c, liftmotor_c, liftmotor_pilot_c, liftmotor_shaft_c, guide_c, guide_bearing_c, home_switch_c).** The section is drawn at 0.82 px/mm in a 4234 px image with over half the width blank; the screw-set parts S3 exists to show are 2 to 35 px. Fix: add two detail views, each its own Axes declared under `insets` (TP-7 per-Axes K3 to K9): Detail B, screw set c from the motor bottom to the ring top (about z_S 230 to 420, u -250 to -60), and Detail C, the top guide (about z_S 1180 to 1240), each at 4:1 or larger, with the section convention, the shoulder screw, the axial play callout and the two bearings legible; or enlarge the section Axes into the blank width. Layout only, no part coordinate moves; dry-run: `check_sketch.py s3 --rev 2` with the detail Axes added, K3 to K9 green per Axes. The detail inset is a spec change: The Designer and The Loftsman re-sign the `insets` entry.

**F2 (V8; K4 gap; rows hold_callout, load_cut, drill_head, span_lt).** Leaders cross label text (power-off-hold leader through the S3-2 span label, ending inside its own text; a leader through "cut 1000 N up"). K4 tests leader against leader only. Rule (h): K4 predicate "no leader segment intersects the text box of any label other than its own, and its end lies on its own label's anchor side"; B fixture: the r1 label set (fires on hold_callout and on the leader through load_cut); Z: S1 r8 and S2 r9 live.

**F3 (V8; rows hold_callout, sync_callout).** Duplicated callout text: hold reads "self-locking Tr12x3, lambda 5.2 < phi 8.8 self-locking Tr12x3 lead (drawn; lambda 5.19 deg < phi_n 8.83 to 11.70 deg) ..."; sync reads "one controller, three drivers, home switch per screw one controller, three drivers, home switch per screw at park; no belt" (K4 already fails on sync_callout). One string each, from the key. The hold callout's right end touches the inset's "-300" tick label: wrap it or move it; K3 "every text inside the saved image" passes, so add text-against-text overlap to the F2 predicate.

**F4 (V8; row sync_callout, inset).** Three dotted leaders fan from an empty point at (-320, 300) to screws a, b, c; the callout text sits outside right with its own leader to screw a. Fan from the callout's anchor point or drop the fan.

**F5 (V8; rows home_switch_c, section_line, plan_axes, inset).** Home switch c sits under the A-A chain line and cannot be seen; "+Y" is overprinted by the section line. Draw the switch above the section line in z order or offset the axes labels; the A-A line may break across the switch mark.

**F6 (V9; figure note).** Add an axial-loop note naming the cut-case loop and where it leaves the plane: "axial loop (cut): head - core 750 - core seat - collet - holder - receiver shoulder - base plate - base frame (off the plane, S1/S2) - member c - anchor arm - anchor block - bearing pair - locknut - screw c (tension) - nut c - boss - ring - bearing - drill tube - head". Rename the legend's "chain:" line-style entry to "chain-dot:" or "dash-dot:". Text only; K4 checks the values it prints.

**F7 (V7, V8; row span_lt).** The red S3-2 span L_t is drawn on the screw centreline over its full length; it reads as part of the screw and its arrowheads are lost in the anchor and guide clutter. Draw it as a dimension offset from the screw with extension lines from the two bearing lines. The offset u is a coordinate: the Engineer dry-runs it (`check_sketch.py s3 --rev 2`, K4, K5, K7 reference-row and K8 green; S3-2 reads the bearing-line rows, not span_lt, so S3-2 is unaffected) at a value in u -235 to -185 or u -125 to -95 (both clear of the screw, nut boss and member faces at the bearing lines; DERIVED from the drawn extents, to be confirmed by the dry-run) before applying.

## Footer: control scoring

Reviewer verdicts: ctrl_a FAIL V3, ctrl_b PASS, ctrl_c PASS handedness, ctrl_d FAIL handedness. Orchestrator scoring against key.json (2026-11-26): 4 of 4 correct. ctrl_a expected FAIL V3, scored FAIL V3; ctrl_b expected PASS, scored PASS; ctrl_c expected PASS handedness, scored PASS; ctrl_d expected FAIL handedness, scored FAIL. The reviewer model is credited for this gate.

## Gameplan lines to change

1. l.138 (K4 row). Old text: "judged and placed as a crossing is |" (the end of the Check cell). New text: "judged and placed as a crossing is; (i) no leader segment intersects the text box of a label other than its own, and no text box overlaps another text box (labels, callouts, tick labels of any Axes) (1.3 (f) M1 S3 r1 F2, F3) |".
2. l.273 (detail 1.3 Shows). Old text: "or the single-controller callout), so K9 sees all three." New text: "or the single-controller callout), so K9 sees all three. Detail views at 4:1 or larger of the screw-c anchor and motor stack and of the top guide, each its own Axes under the per-Axes rule (TP-7), so every screw-set part reads at 100 percent (1.3 (f) M1 S3 r1 F1); an axial-loop figure note naming where the loop leaves the plane (F6)."
3. Design Notes 13: insert after the row beginning "| S2-r5 | 2026-11-25 |" the row: "| S3-r1 | 2026-11-26 | No correction from Sean yet. M1 FAIL F1 to F7 (`docs/sketches/wip/s3_visual_gate_r1.md`) | r2 (P9) |".
