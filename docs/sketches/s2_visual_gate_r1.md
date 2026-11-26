# S2 visual gate, revision r1 (M1, The Designer)

Reviewer: The Designer, image-capable model, fresh spawn. I did not draw these figures. Every PNG below was opened with Read and returned pixels. Detail crops (centre, leaders, F6 line, member c, descent-stop pad, pinion b) were cut from `wip/s2_plan_r1.png` for inspection only. No `key.json` was opened.

Inputs: `wip/fixtures/figs/ctrl_a.png` to `ctrl_d.png`; `wip/s2_plan_r1.png`; `s2_spec.yaml` (question, rubric_additions, operator_sector, sightline_f6, gear, pinion, descent_stop, guide_tie rows); gameplan l.176-203; `wip/s2_checks_r1.json`, `wip/s2_summary_r1.md`; `research/sean/cr_scratch/step1.2_engineer_draw_r1.md`.

## Corrections to the brief

1. The pitch circle the Engineer drew in place of tooth ticks (r 125) sits 1.32 mm inside the gear OD (r 126.32). At the plan scale, 1.39 px/mm (MEASURED from the x ticks), that is under 2 px. I could not separate it from the OD in the full figure or in a 2x crop. The fallback in open item 1 does not show in the figure.
2. The F6 label anchor and the sector label anchor are placed at (max x, mid y) of the drawn piece (`sketch_common.place_labels`, `_right_anchor`; DECLARED in its docstring). On a slanted line or a wedge, that point is off the part (finding F4).

Tags: positions read from pixels MEASURED (about +-3 mm); hand values DERIVED; spec values DECLARED.

## 1. Reviewer-model controls (judged blind)

| Figure | Items | Verdict | What I see |
|---|---|---|---|
| ctrl_a | V1 to V5 | **FAIL V3** (V1, V2, V4, V5 PASS) | The block labelled "cutter OD ASSUMED 177.8" sits at the top of the tube (about 1090 to 1195 z). The tube runs down to about 245 with no head at its lower end, so the drill is tip-up. Floor line at z 0 at the bottom; tube vertical; core upright 100 to 605 on its stop line; screw vertical with a guide block at the top (1195 to 1225), anchor at the bottom, nut on the ring plate. |
| ctrl_b | V1 to V5 | **PASS** | Cutter block (177.8) at the bottom of the tube (about 245 to 350); a top-end block split off at about 1045 to 1195. The rest matches ctrl_a: floor at the bottom, axis vertical, core upright on its stop, screw with guide at the top, anchor at the bottom, nut on the ring. |
| ctrl_c | handedness | **PASS** | +X arrow to the right, +Y arrow up, theta arc counter-clockwise from +X to +Y. Screw a at (140, 80) = 30 deg, b at (-140, 80) = 150 deg, c at (0, -160) = 270 deg, each matching its tag. |
| ctrl_d | handedness | **FAIL** | The +Y arrow points down the page while the tick labels rise upward. The theta arc runs clockwise from +X. Screw c, tagged 270 deg, is drawn at (0, +160) on the axis ticks; screws a and b, tagged 30 and 150 deg, sit at y = -80. The figure is mirrored about X. |

## 2. S2 rubric (applicable: V2, V6 to V10; V1, V3, V4, V5 N/A)

| Item | Verdict | What I see |
|---|---|---|
| V2 | PASS | Tube annulus, keep-out (red dashed), cutter rim (dotted), bearing, gear, gear hub and ring OD are concentric on the datum B cross. Each pinion axis is a chain line running radially through pinion, hub, shaft and NEMA 23 at 90, 210 and 330. |
| V6 | PASS | Z-axis parts are circles. Pinions, shafts, NEMA 23s, mounts, arms and members are trapezoids or rectangles on their azimuths. No side-view shapes in the plan. |
| V7 | **FAIL** (F1, F2) | The ring reads as a structure (section 3, line 4). Screws read as a black screw dot on an amber nut flange in a nut-housing ring. The 30-6060 members read as cross-hatched 60 squares turned to their azimuths, and member c reads as a square in the notch. Each motor sits outboard of its shaft and pinion. Two failures. F1: the gear has no teeth. It is a diagonally hatched annulus r 90 to 126.32, and from the figure alone it reads as a washer or a hatched bearing race. F2: each pinion trapezoid (r 95 to 125, entirely inside the gear annulus in plan) is drawn solid and cross-hatched over the gear hatch. The figure note says "dashed: under a nearer part". The gear (1242.07 to 1275.84 z_S) is above pinion_c (1168.22 to 1259.46 z_S), so the drawing shows the pinions sitting on top of the gear. Design Notes 22 has them below it. |
| V8 | **FAIL** (F3, F4, F5) | Labels sit in one right-hand column and no two label texts overlap. Three failures. F3: the F6 label prints "eye z_S z_S 1600". F4: the "F6 sightline" leader ends at about (201, 173), 100 mm right of the line (the line passes x 99 at y 173), on the open plate near member b. The "load and collet change" leader ends at about (283, 200), outside the wedge (the wedge edge at y 200 is x 200). F5: the tube OD 152.4, keep-out r 86.2, cutter OD 177.8 and gear PD 250 leaders all end on y = 0 at r 76.2, 86.2, 88.9 and 125. The first three anchors lie within 13 mm (18 px) of each other, and the tube leader crosses the keep-out and cutter leaders just before they reach their anchors. I cannot tell from the figure which leader ends on which circle. The 2.70 cutter overhang of the keep-out (S2-a) is 3.75 px and only shows in a crop. |
| V9 | PASS | See section 5. |
| V10 | PASS | See section 6. |

## 3. S2 rubric additions

| Line (spec wording, shortened) | Verdict | What I see |
|---|---|---|
| plan handedness: +X along slot line C (y +259), theta CCW seen from +Z; screws 30, 150, 270, pinions 90, 210, 330 | PASS | Heavy chain line at y +259 on the +Y rail, labelled "slot line C, +X". Datum B cross in the tube bore with +X right, +Y up and a counter-clockwise theta arc. Screws at (139, 80), (-139, 80), (0, -160); pinions at 90 (top), 210 (lower left), 330 (lower right); each tag matches its azimuth. |
| all three screw sets, pinions, NEMA 23s, lift motors and frame members drawn | PASS (NOTE N1) | Three screws with flanges and housings, three anchor/guide arms, three members, three pinions with shafts and NEMA 23s, both guide rods with lugs, both ties. The three NEMA 17 lift motors are thin dashed 42 squares under the nut housings. Only their corners show (about 5 mm beyond the d 50 housing), and at 100 percent they are barely visible. |
| on every pinion axis the motor is outboard and the pinion inboard, narrowing toward the axis | PASS | All three: trapezoid narrow end toward the axis, then the hub, the dark shaft bar, the open mount block and the grey NEMA 23 body outboard, with the chain-line axis through all of them. |
| the ring reads as a structure with housings, mounts and lugs, not a washer | PASS | A tinted disc r 210 with a heavy OD edge, three nut-housing rings round the screws, three NEMA 23 mount blocks from r 142 to the rim, and two guide lugs as squares reaching out to the rods at 0 and 180. The clearance bore is under the gear and bearing and does not show. That is correct in plan. |
| member c on the rail top in the column notch, notch outline visible round it | PASS | Cross-hatched square at y -245 to -304, x +-30, with a white 5 mm notch margin on both sides; the rail chain line and pockets continue either side. |

## 4. TP-n: parts drawn narrower than their footprint

projected_extent tests containment only. By eye, every narrower case below reads as the part:
- Lift motors (round footprint r 29.7, drawn 42 square): read as square motor bodies, though faint (N1).
- Members a, b, c (60 squares inside their footprints): read as 30-6060 sections.
- Pinions (trapezoid narrower at the toe than the half_width outer_diameter / 2): the taper is the bevel form and reads correctly.
- Sightline, pinion axes (half_width 0): lines, as intended.
- Descent-stop pad (r 200 to 215 x 60 on arm a): drawn full width with two grey hatch strokes, under the ring rim edge. It reads as a strip on the arm (N2).

No part's drawn width misreads the part.

## 5. V9

From the figure alone: everything above the plate lies inside the 644 x 608 base outline (members a, b inside the x edge, member c on the -Y rail edge). The drill, bearing, gear, hub and ring are concentric on the datum B cross. The +Y side between members a and b (theta 45 to 135, out to r 400 off the plate edge) is open for loading the core and changing collets, with only the ring-mounted pinion c and its NEMA 23 overhead.

Spec question: "Does it fit, stay coaxial, and leave the operator a side to load the core and change collets?" My sentence answers all three parts, and it agrees with S2-2, S2-4, S2-5a and S2-6. The overhead height of pinion c and its motor (S2-5b, 136.84 above the hand band) cannot be read in a plan. It comes from the summary.

## 6. V10, operator tasks assigned to S2

| Task | Reach | Sightline | Verdict |
|---|---|---|---|
| Load core | Operator stands in the wedge beyond the plate edge y 304, the plate corner and members a, b outside the wedge (lift motors 11.71 clear, MEASURED in the summary). About 300 from the plate edge to the axis. | Down to the tube bore at the axis from the +Y side, past pinion c / NEMA 23 at theta 90 overhead. | PASS |
| Collet change | Same sector; the wing nut sweep is a side-view item (not_drawn, S1). Arms and anchors at 30 and 150 lie at the wedge edges, outside it. | From the sector at knee height (S1). | PASS |
| Stand and watch | Observer dot at r 400, theta 60, on the sector arc, off the plate. | Line to the axis. | PASS |
| F6 sightline | n/a | Drawn to its row: solid from the observer to the ring rim r 210, dashed inside it to the axis. The drawing places the observer and puts the ring rim on the line of sight. Whether the rim hides the cut depends on eye height, which a plan cannot show; the label states the result, and the eye limits (492.46 and 578.80 z_S against eye 1600 z_S, DERIVED in the summary) carry it. Step 2 owns the fix (Design Notes 24). The plan sightline is adequate as the azimuth locator. | PASS (label text: F3) |

## 7. Findings

| # | Feature | Item | Finding | Fix |
|---|---|---|---|---|
| F1 | gear | V7 | No teeth. The hatched annulus reads as a washer, and the pitch circle r 125 is not visible (1.32 mm inside the OD). | The teeth face down (Design Notes 22), so from +Z they are hidden on the gear's underside, across the face from the toe (pinion.r_toe, 95.2) to the heel (pitch radius 125). The honest plan is dashed radial ticks across that face, which also signals that the teeth face down. Ticks on the OD would be 1.32 mm long (the addendum), about 2 px, and would not read. Rule (raised and signed by The Designer, detail 1 common (h)): K5 admits, under gid `gear`, one LineCollection sub-artist `gear:ticks` of radial dashed segments from pinion.r_toe to gear.pitch_diameter / 2, gear.tooth_count of them, evenly spaced. Premise check (K8 `ticks_radial`, through the artist transform): every segment's direction is parallel to its radius vector (|cross| <= 0.05 mm per mm), both ends lie within [pinion.r_toe - 0.05, gear.pitch_diameter / 2 + 0.05], and the count equals gear.tooth_count. Z: correct ticks. B1: one tick turned tangential. B2: one tick ending beyond the pitch radius. B3: count gear.tooth_count - 1. Replace the gear's diagonal hatch with a light plain fill so the ticks read. Shape text, old: "annulus r 90 to 126.32 with tooth ticks on the OD". New: "annulus r 90 to 126.32 with dashed tooth ticks on the underside face, toe r 95.2 to heel r 125 (teeth face down)". |
| F2 | pinion_a, _b, _c (with gear) | V7 | Pinions drawn solid and hatched over the gear, against the figure's own hidden-line legend. The drawing reads as pinions above the gear. | Draw the part of each pinion inside r gear.od / 2 as a dashed outline with no hatch. Hub, shaft, mount and motor stay solid outboard. Visual only; no new check. |
| F3 | sightline_f6 | V8 | Label prints "eye z_S z_S 1600". | Spec label text: drop the trailing "z_S" (section 8, item 2). |
| F4 | sightline_f6, operator_sector | V8 | Leaders end off the part: about 100 mm right of the sightline and outside the wedge. | In `place_labels`, anchor on a vertex of the drawn piece: the drawn vertex with the largest x, or the point of the piece nearest the label column. That gives the observer point (200, 346) for the sightline and the wedge corner (283, 283) for the sector. The Engineer picks the rule. The leader has to end on ink. |
| F5 | drill_tube, keepout, drill_head (cutter rim), gear | V8 | Four concentric leaders end on y = 0 within 13 mm, crossing. | Give each concentric circle its own leader azimuth from the spec (a row field such as `label_theta`, read by the script, so K1 holds), spread in order of radius over the clear band theta 340 to 20 (e.g. tube 340, keep-out 350, cutter 0, gear 10). The leaders must not cross. |

NOTEs (no gate effect):
- N1 (liftmotor_a/b/c): lift motors barely visible under the housings. Raise the dashed line weight to match the bracket dashes.
- N2 (descent_stop): the pad's two grey hatch strokes are faint. Give it a solid outline at bracket weight. It sits on the arm top, so it is nearer than the arm.
- N3 (guide_tie_a/b): the figure note lists "ties" under "dashed: under a nearer part". At load the ties (1225 to 1285 z_S) are the topmost parts at their plan position. The dashes signify the Step 2 stand-in from the shape text, not a hidden part. Split the note: "dashed: Step 2 stand-in (ties)".
- N4 (S2-a): the 2.70 cutter overhang of the keep-out cannot be read at plan scale. When TP-7 inset iteration lands (S3), add a 5:1 detail of the tube, keep-out and cutter rim, checked as its own view.

**Overall S2 r1: FAIL, 5 findings (F1 to F5).** Controls: ctrl_a FAIL V3, ctrl_b PASS, ctrl_c PASS, ctrl_d FAIL.

## 8. Rulings on the Engineer's open items (`step1.2_engineer_draw_r1.md` section 6)

1. **Gear tooth ticks.** Draw the ticks as dashed radial ticks on the underside face, toe r 95.2 to heel r 125. They are admitted by the F1 rule, with its premise check and Z/B, which I raise and sign. The shape text is amended to match (F1). A pitch circle 1.32 mm inside the OD does not read.
2. **F6 label.** Spec defect, fix in the spec. `sightline_f6.label.text` old: `"F6 sightline: ring rim r 210 hides the cut at capture_end; eye z_S"`. New: `"F6 sightline: ring rim r 210 hides the cut at capture_end; eye"`. The z_S suffix then prints "eye z_S 1600 (operator.eye_height 1540 z_A)" once.
3. **Highest-point report.** The sightline is a reference line, not a part. Add `reference: true` to rows sightline_f6, operator_sector, collet_axis (datum B) and keepout, and exclude reference rows from the highest-point and outline-extent reports. The capture_end highest point then reports the true top part, not 1600.00. The Loftsman confirms the corrected value. The outline-extent report already excludes these three by hand; the field makes it one rule.
4. **Spec status string.** Orchestrator edit. Old: `"...; 1.2 (c) gear section field added for the plan annulus (awaiting the Loftsman and Designer at (c)/(e))"`. New: `"...; 1.2 (c) gear section field added for the plan annulus (signed at (c) by the Loftsman, Designer, Topologist and Software Engineer after P5f)"`.
5. **Label leaders.** FAIL, see F4 and F5. The descent-stop leader that crosses the drawing ends on its pad and is legible; it stands.
6. **Plate as tinted pieces without edges.** Legible. The tint edge, the dashed base frame and the white notch margin give the outline. No change.

**F6 sightline (Sean's Step 2 assignment, Design Notes 24).** The S2 drawing matches its row and is adequate for S2. A plan cannot prove the occlusion. The Step 2 row needs an elevation section in the theta 60 plane (eye at r 400, ring rim r 210 at 374.84 z_S, cutter 244.84 to 351.21 z_S) to show that the cut is hidden and to judge any fix: a lower viewing port, a mirror or camera, or a cut-out in the ring rim.

## Gameplan lines to change

none

Orchestrator scoring of the controls against `key.json` (to be filled by the orchestrator): ctrl_a ____, ctrl_b ____, ctrl_c ____, ctrl_d ____; match: ____.

## Addendum (coordinator query before r2): LF1.2-2 and TP1.2-2

**LF1.2-2, pinion_a/_b/_c | gear_hub: declare class G, g_min 3 (ASSUMED).** The toe gap 5.22 = pinion r_in 95.22 - gear.bore / 2 90.00 (DERIVED, Loftsman) follows from the mesh geometry: pinion toe r 96.54 set by face width, and the hub OD equal to the gear bore. It is a gear-set identity, not a frame clearance. The g_min 10 seed is for moving parts against fixed members and does not apply. Both parts belong to one driven train with no relative radial motion. The real risks are toe runout and any clamp-screw head on the hub OD, and g_min 3 covers runout at sketch level. Source text: "Designer M1 r1 ruling: toe to hub is set by pinion.r_toe and gear.bore; g_min 3 ASSUMED for toe runout; hub clamp screw heads (Step 2) must stay below r 90 or be re-checked". No geometry change. The Engineer adds "pinion toe to gear hub 5.22" to the tight spots and the `reported` list, as LF1.2-2 asks.

**TP1.2-2: confirmed.** The F2 dashed-if-hidden fix applies to every row the Topologist lists: nut_a/_b/_c under guide_a/_b/_c, descent_stop under bracket_guide_a and the ring rim, motor_mount_a/_b/_c under motor23_a/_b/_c, guide_lug_a/_b and guide_member/_b under the ties, and the pinions under the gear (F2). Rule: in plan, a row point covered by a true section of a row with a higher z_max is drawn dashed, with no fill or hatch. My N2 is withdrawn: the descent-stop pad stays dashed because it is hidden, and its visibility goes to the S1 side view. The ties stay dashed as the Step 2 stand-in, and the legend splits as in N3: "dashed: under a nearer part" and "dashed: Step 2 stand-in (ties)". I sign the legend once r2 draws it.

## Sign-off r2 (rules raised by The Designer; `research/sean/cr_scratch/step1.2_engineer_revision_r2.md`)

Corrections to my F1 text: "pinion.r_toe 95.2" named the wrong key. `pinion.r_toe` is 96.54, the toe pitch point (DECLARED). The tick toe is the toe tip, given by the pinion place `r_in` expression `pinion.r_toe - pinion.pitch_diameter / pinion.tooth_count * sind(pinion.pitch_angle)` = 95.22 (DERIVED). That is the radius I meant, and it puts the ticks at the drawn pinion toe. The Engineer's expression stands, and the shape text "toe r 95.2" reads as 95.22. Figures are not re-scored here; a fresh M1 (P8r) does that.

| Rule or edit | Premise check and controls | Verdict |
|---|---|---|
| K8 `ticks_radial` + K5 tick admission + K9 sub-gid `<row>:ticks` | Admission only with the predicate (K5-B15). Radial, within r_in 95.22 to r_out 125.00, count `gear.tooth_count` (K8-B29 tangential, B30 past the heel, B31 59 ticks). One collection (K5-B16), Line2D refused (K5-B14), sub-gid of an existing row only (K9-B6). Z on live S2. | **SIGNED** |
| K4 leader rules: (a) every leader ends within 0.05 of its row's ink, (b) no two leaders cross; spec field `label_theta` (tube 340, keep-out 350, cutter 0, gear 10) | Anchor computed on drawn ink. K4-B7 (r1 sightline anchor 86.60 off), K4-B8 (r1 concentric anchors, 3 crossings); Z: K4-Z3 live S2, S1 r6 55 labels clean. Azimuths come from the spec, so K1 holds. | **SIGNED** |
| K3 every Text inside the saved image (canvas, or tight bbox when every `savefig` passes `bbox_inches="tight"`, read from the AST) | K3-B8 (r5 park note 9 px out), K3-B9 (one savefig without tight); Z: K3-Z2, K3-Z3. | **SIGNED** |
| Split legend: "dashed, no fill: under a nearer part (...)" / "dashed: Step 2 stand-in (rod top ties)" | Visual only. The text matches addendum N3 and TP1.2-2. | **SIGNED** (P8r reads it on the figure) |
| Dashed-if-hidden drawing rule (K8 `cover`) | The drawing rule is mine, and the premise (true outlines only, K8-Z7, B33) is the Topologist's to sign. | **SIGNED** (drawing rule) |
| Spec: `reference: true` on sightline_f6, collet_axis, keepout (operator_sector already) | Ruling 3 applied. Declared S2-a pairs on the keep-out are still judged by K7. | **SIGNED** |
| Spec: status text | Ruling 4 applied, plus an r2 clause. | **SIGNED** |
| Spec: F6 label text without the trailing "z_S" | Draws "eye z_S 1600 (operator.eye_height 1540 z_A)" once. | **SIGNED** |
| Spec: gear shape text, part-list gear entry, `reported` tight spots incl. "pinion toe to gear hub 5.22", gear_hub neighbours pinion_* G 3 | Match my rulings (F1, addendum LF1.2-2). The Loftsman checks the G 3 declaration. | **SIGNED** |

**S2 highest point 1819.84 z_S at load and park: accepted.** S2 is a plan sketch, and its highest point is reported over its own drawn parts. The jig height of record is S1's 1969.84 z_S (top-end block). Do not add a top-end block row to S2: in plan it would sit over the bore and hide the datum B cross. The S2 summary line reads "highest drawn part 1819.84 z_S (tube top); jig height of record 1969.84 z_S from S1 (top-end block)". This closes the Engineer's open item 1.

## Gameplan lines to change

The Designer adds no gameplan lines here. The K3, K4, K5, K8 and K9 row changes and the Progress Log row are in `step1.2_engineer_revision_r2.md` "Gameplan lines to change". Endorsed as worded for the rules signed above.

## Sign-off r3 (`research/sean/cr_scratch/step1.2_engineer_revision_r3.md`)

Figures are not re-scored here; a fresh M1 does that.

**Red-first for the K4 B controls, MEASURED 2026-11-25.** The Engineer could not run these red-first (his Correction 4 tags them DERIVED). I ran them in memory: the live `sketch_common.leader_issues` was redefined with one branch removed at a time, and K4-Z4, B9, B10 and B11 were run through `check_sketch.run_control` and `compare`. No repo file was touched. Script: `<scratchpad>/des_k4/mutk4.py`.

| Branch removed | K4-Z4 | K4-B9 (d) | K4-B10 (c) | K4-B11 (a') |
|---|---|---|---|---|
| none (live) | clean, match | fires, match | fires, match | fires, match |
| (a') anchor under another row's area | clean | fires | fires | **clean, NO MATCH** |
| (c) area over the leader | clean | fires | **clean, NO MATCH** | fires |
| (d) leader end across hatch | clean | **clean, NO MATCH** | fires | fires |

Each B fails to match exactly when its own branch is deleted, and no B depends on a branch other than its own. Red-first is now MEASURED.

| Item | Verdict | Note |
|---|---|---|
| Labels drawn above every area (`LEADER_ZORDER` 100) | **SIGNED** | Premise read from the drawn z order (K4 (c), B10). |
| K4 (a'): no other row's area over the anchor | **SIGNED** | B11; red-first above. |
| K4 (c): no area drawn over the leader | **SIGNED** | B10; red-first above. |
| K4 (d): at most 25 % of the last quarter of a leader inside other rows' hatch | **SIGNED** | B9; Z4 (live S1, thread strips pass). The 25 % / 25 % shares are DECLARED, chosen on the Engineer's trial (no limit moved 13 S1 anchors and crossed leaders; 25 % moves only core 750). Tighten later only with a new B. |
| Re-anchor in `place_labels` (search the row's ink, first-anchor edge first) | **SIGNED** | Core 750 at capture_end, (50.00, 540.00), lands between the gear top and the core top, as asked. |
| Split convention: a partly visible piece gets a solid copy just under the lowest covering fill plus its dashed outline on top | **SIGNED** | The visible part reads solid, the hidden part dashed, and F2 holds for the pinions (heel corners at r 133.07 show). The cover converse premise is the Topologist's (K8-B34, B36). |
| `plan_style: stand_in` on guide_tie_a/_b | **SIGNED** | Held to the spec field (K8-B35). The legend "dashed: Step 2 stand-in (rod top ties)" stands. |
| S2 spec: `ticks_radial` r_in = `pinion.r_toe` 96.54, gear shape text "toe r 96.54 to heel r 125 along the gear pitch cone" (Design Notes 29), status text | **SIGNED** | Supersedes my r2 ruling of 95.22. The gear's tooth face starts at the toe pitch point, and Design Notes 29 governs. |
| S1 spec: gear_hub declares pinion_a/_b G, g_min 3 ASSUMED, S2 source text | **SIGNED** | Matches the LF1.2-2 ruling. S1 plan-separated distance 5.198 against 3 (MEASURED by the Engineer). |

**Ruling on M1 S2 r2 N2 (notch outline): draw it now.** The rubric addition "member c ... with the notch outline visible round it" is a spec line, and a solid rail-top piece is a floor, not an outline. Rule (raised and signed by The Designer, detail 1 common (h)):
- K5 admits under gid `base_plate` one sub-artist `base_plate:outline`: an unfilled closed Polygon at bracket line weight, drawn above the plate tint.
- Premise check (K8 `outline_matches`, through the artist transform): its vertex ring equals the boundary of the union of the `base_plate` plan_poly pieces (outer 644 x 608 rectangle with the column notch) within 0.05, with the same vertex count and orientation.
- Z: live S2.
- B1: plain 644 x 608 rectangle (notch missing).
- B2: notch outline offset 5.
- B3: two outline artists.
- B4: outline without the predicate on the row (admission requires the premise, as K5-B15).
- K9 accepts the sub-gid only on an existing row (as for `gear:ticks`).
- Outlining the five plate pieces stays refused (false seams).

## Gameplan lines to change

The Designer adds no lines of his own. The K4 row (l.138) gets the (a'), (c) and (d) wording and the controls K4-Z4 and K4-B9 to B11, as in the Engineer's r3 file. Endorsed, with this addition at the end of the l.138 rule text: "; red-first for K4-B9 to B11 MEASURED by branch deletion (Designer sign-off r3)". When N2 is applied: the K5 row (l.148) gets, after "...only when the row carries K8 ticks_radial (Designer M1 r1 F1)", the text "; a base_plate row admits one unfilled Polygon base_plate:outline only when the row carries K8 outline_matches (Designer sign-off r3, M1 S2 r2 N2)". The K8 row (l.186) gets "; outline_matches, the base_plate:outline ring equals the boundary of the union of the plan_poly pieces within 0.05". The exact old text for both is the Engineer's to quote, from the lines as they stand after r3.

## Sign-off r4 (`research/sean/cr_scratch/step1.2_engineer_revision_r4.md`)

Delta read of `wip/s2_plan_r4.png` (opened with Read; crops of the descent-stop pad, member c and the +Y notch). This is not a re-score.

| Item | Verdict | Note |
|---|---|---|
| K5 `base_plate:outline` admission (one unfilled Polygon, plate row with plan_poly, predicate present) | **SIGNED** | K5-B17 (two outlines), K5-B18 (no predicate). |
| K8 `outline_matches` (same vertex count, same orientation, one cyclic shift within 0.05) | **SIGNED** | K8-B37 (plain rectangle), K8-B38 (notch offset 5). The fixture ring is built independently (`_notch_ring`). |
| K9 sub-gid generalised (`<row>:ticks`, `<row>:outline` on existing rows only) | **SIGNED** | K9-B7. |
| Red-first on the kept r3 modules | **Accepted as MEASURED** (Engineer, Correction 5) | Every new B is NO MATCH on r3, for the stated reasons. |
| Spec field `label_side: left` | **SIGNED** | K4 (a') to (d) apply to the left column (K4-Z3). |
| S2 spec edits: `outline_matches` on base_plate, `stand_in_owner` on guide_tie_a/_b, `label_side: left` on descent_stop, status text | **SIGNED** | |

**Visual delta at 100 percent:**
- **Notch outline: reads.** A dark-grey 1-weight line round the 644 x 608 plate with both 70 x 65 notches (+Y and -Y). At -Y, member c sits in the notch with the 5 mm gaps between the outline and the hatched square.
- **Translucent sector: reads.** The plate tint, the +Y rail and pocket outlines, slot line C and the +Y notch outline all show through the wedge.
- **Rail strips beside member c: read.** The two 5 mm strips between member c and the notch outline show the rail top, light and edge-bounded, distinct from the plate tint. They are thin at this scale and legible.
- **Descent-stop label: does not read correctly (FIX D4-1).** The label now sits in a left column, and the leader runs at y 81.5 from x about -355 to its anchor (-201.20, 81.52), the pad's outer-left corner. Its last 64 mm run inside the dashed outline of rod-top tie b's footprint (x -265 to -198, y -30 to 97), and the anchor lies 1.2 mm from that dashed edge. At 100 percent the leader reads as pointing at the tie corner. Fix with the existing field, no new rule: `label_theta: 150` on descent_stop. The anchor becomes the farthest ink point on the theta 150 ray, the pad's outer-edge midpoint (-186.20, 107.50) (DERIVED, 215 (cos 150, sin 150)). A leader at y 107.5 clears the tie top (97). It crosses member a's hatch at x -254.6 to -228.0 (DERIVED), which is outside the last quarter of a leader about 170 long, so K4 (d) holds. K4 confirms on the run.

**Fresh-M1 N2 (ring rim shows through the unfilled guide arms): carry to S3 accepted.** The guide arms (1195 to 1225 z_S) are above the ring rim (1161.84) and drawn unfilled, so the rim arc shows through them. The arm outline stays complete and nothing is mistaken for another part. The correct fix is a general hidden-line renderer for solid pieces under unfilled covers (Engineer Correction 3), and it belongs with S3, where the arms are the subject. The Topologist co-owns it there. S2 acceptance does not wait on it.

## Gameplan lines to change

The K5 (l.139), K8 (l.142) and K9 row changes are in `step1.2_engineer_revision_r4.md` "Gameplan lines to change". Endorsed as worded, and they supersede the line numbers 148 and 186 in my sign-off r3. The Designer adds none.
