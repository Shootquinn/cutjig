## Corrections to the brief

1. **The spec draws one pose.** S3 r1 draws capture_end only. Start and park appear only as the nut-station ticks `nut_station_start` and `nut_station_park`. S3 K8 judges anchor below nut below guide at capture_end alone.
   - At the other poses, screw c is held by S3-1 (check_stack nut_z per pose) and by SYM, which carries the S1 r8 K8 of screws a and b at every pose.
   - Hand values for all four poses are in section 1.
2. **S3-3 certifies contact, not load direction.** The chain order is continuous and closed in chains a, b and c. The certifiers are a K7 C state, or a K7 C state plus a named face with a horizontal edge at the face z. Neither reads which side of the face each part lies on.
   - 24 of the 51 links pass on a drawn contact that cannot carry the cut-case load in its direction: 8 per chain, MEASURED on c and DERIVED on a and b.
   - The P6 dry run with S1 r8 and S2 r9 accepted ("51 links closed") passes all 24. Finding TP1.3-10.
3. **The unsectioned class has no occlusion rule.** The renderer dashes only beyond rows behind cut pieces. In r1, 8 row pairs have an unsectioned piece drawn whole over another row's area. Area overlaps are up to 10636.90 mm² (MEASURED), and K8 passes. My P5T NOTE 6 predicted the beyond half of this. The cut and unsectioned halves are live. Finding TP1.3-11.
4. **The theta arc was replaced, not just dropped.** In its place is an untagged Text "theta ccw from +X". No check reads it.

Tags:
- MEASURED: probes `p1_build.py` to `p7_occl.py` in `D:\Unleashed Robotics\_scratch\cutjig\p7b\probes\`, run 2026-11-26 on the scratch copy `D:\Unleashed Robotics\_scratch\cutjig\p7b\sk\` of `docs/sketches/` (r1 state). Run with Python 3.12 and matplotlib 3.11.2; TMP and TEMP under `_scratch\cutjig\tmp`; nothing under `docs/sketches/` edited.
- DERIVED: hand arithmetic.
- DECLARED: spec, overlay or ruling.
- PNG `docs/sketches/wip/s3_jackscrew_section_r1.png` read as an image.

**Verdicts:**
- **S3 r1: CROSS-REVIEW FAIL.** 6 FIX (TP1.3-10 to -15) and 5 NOTE (TP1.3-16 to -20).
- **S1 r8: CROSS-REVIEW PASS.** K5 mark admission re-checked and SIGNED.
- **S2 r9: CROSS-REVIEW PASS.**

## 1 Anchor below nut below guide; section and inset handedness

### 1a K8 predicate by hand through the transform chain

Hand chain (`p1_build.py`, HAND rows): `a.get_path().vertices` → `a.get_transform()` (patch transform plus transData) → display → `ax.transData.inverted()` → data. The section Axes is not inverted on x or y (MEASURED). The pieces match `sc.artist_polys` vertex for vertex.

**nut_c** (5 pieces, z_S, MEASURED by the hand chain):

| Pieces | z | u | Area each (DERIVED) | Centroid z |
|---|---|---|---|---|
| Body walls (2) | 365.84 to 387.84 | [-171, -166] and [-154, -149] | 110 | 376.84 |
| Flange (3) | 387.84 to 395.84 | [-181, -166], [-154, -147.5], [-140.5, -139] | 120, 52, 12 | 391.84 |

Area-weighted centroid z = (220 x 376.84 + 184 x 391.84) / 404 = **383.67** (DERIVED).

**anchor_c** (6 pieces):
- Areas 77 x 2 at centroid z 328.5, 128 x 2 at 340.0, 91 x 2 at 351.5.
- Centroid z = 201602 / 592 = **340.54** (DERIVED).

**guide_c:** two symmetric pieces 1195 to 1225, centroid **1210.00** (DERIVED).

| Predicate (capture_end) | Hand (DERIVED) | Harness (MEASURED, probe centroid) | JSON `wip/s3_checks_r1.json` |
|---|---|---|---|
| anchor_c below nut_c | 340.54 < 383.67 | 340.54, 383.67 | K8 [section] pass, "218 predicate(s) hold" |
| nut_c below guide_c | 383.67 < 1210.00 | 383.67, 1210.00 | same |
| anchor_bearing_c below nut_c | 340.00 < 383.67 | 340.00 | same |
| guide_bearing_c above nut_c | 1210.00 > 383.67 | 1210.00 | same |
| S3-1 tension segment | nut bottom 365.84 - bearing line 340.00 = 25.84 | line 340.00 at mark.z 280 + 60 | S3-1 measured 25.84 |

The K8 JSON carries counts only, so a hand value can be set only against "pass, 0 issues" (NOTE TP1.3-16).

### 1b Every pose (z_S)

Anchor bearing line 340.00. Guide block bottom 1195.00. Guide bearing 1206 to 1214.

| Pose | Nut bottom to top | Anchor line < nut bottom | Nut top < guide block bottom | Held by |
|---|---|---|---|---|
| load (= park tip) | 1140.84 to 1170.84 | 800.84 | 24.16 | S3-1; SYM from S1 r8 K8 a, b |
| start | 1015.84 to 1045.84 | 675.84 | 149.16 | S3-1; SYM from S1 r8 |
| capture_end (drawn) | 365.84 to 395.84 | 25.84 | 799.16 | S3 K8, S3-1 |
| park | 1140.84 to 1170.84 | 800.84 | 24.16 | S3-1; SYM from S1 r8 |

- Nut positions: check_stack nut_z (MEASURED via the S1 r8 nut_a centroids 1155.84, 1030.84, 380.84, 1155.84).
- Differences: DERIVED.
- 24.16 matches the spec G entry nut_housing_c|guide_c (DECLARED).

### 1c Section handedness

Section frame (DECLARED, section.axes): u = +Y, z = +Z. u x z = (0, 1, 0) x (0, 0, 1) = (1, 0, 0) = +X, toward the viewer.

Viewer facing -X with up +Z: right = f x z = (-1, 0, 0) x (0, 0, 1) = (0, 1, 0) = +Y. That is u to the right (DERIVED).

| Row | u = r sin theta (DERIVED) | Drawn u centre (MEASURED) | Side predicate sign |
|---|---|---|---|
| screw_c | 160 sin 270 = -160 | -160.00, extent [-166, -154] | left of the tube, -1 |
| frame_upper_c | 274 sin 270 = -274 | -274.00 | left, -1 |
| pinion_c | r sin 90 > 0 | 118.57, extent [95.22, 140.00] | right, +1 |
| motor23_c | r sin 90 > 0 | 180.00, extent [142.00, 218.00] | right, +1 |
| motor_shaft_c outboard of pinion_c | (131.50 - 118.57) x sin 90 = +12.93 > 0 | | outboard holds |

Look sign (P5f FIX 2): `section_line` arrows run (0, ±307.02) → (-60, ±307.02), toward -X (MEASURED). So (u x z) . toward = (1, 0, 0) . (-1, 0, 0) = -1 (DERIVED).

### 1d Inset handedness

Drawn screw centroids (MEASURED): a (-138.56, 80.00) at 150.00 deg, b (138.56, 80.00) at 30.00 deg, c (0.00, -160.00) at 270.00 deg. Every r is 160.00.

Consecutive in theta, (p_i x p_j) . z:

| Pair | Arithmetic (DERIVED) |
|---|---|
| b → a | 138.56 x 80 - 80 x (-138.56) = +22169.6 |
| a → c | (-138.56)(-160) - 80 x 0 = +22169.6 |
| c → b | 0 x 80 - (-160)(138.56) = +22169.6 |

Each equals 160² sin 120 = 22170.1 (DERIVED; within rounding of the centroid digits). All three are positive, so theta runs counter-clockwise seen from +Z. The inset is not inverted on x or y (MEASURED).

## 2 Section convention as drawn

Render state per row (MEASURED, `p1_build.py`). Cut rows carry hatch at zorder 1; unsectioned rows carry no hatch at zorder 3.

| Class | Rows and state | Verdict |
|---|---|---|
| cut | Hatch by material: aluminium `//` (plate, ring, nut_housing_c, anchor_c, guide_c); extrusion `xx` (base_frame, frame_upper_c, brackets); steel `\\` (bearing, receiver, collet, holder, tube, gear, pinion, motors, locknut, bearings, home switch); brass `..` (nut_c) | as the convention states |
| unsectioned | screw_c, screw_end_c, nut_screws_c, coupling_c, liftmotor_shaft_c, motor_shaft_c, core_750, drill_head, drill_top_block, wingnut. Every band straddles x = 0 | occlusion gap, FIX TP1.3-11 |
| beyond | standoffs_c, two pieces u [-178.25, -172.75] and [-147.25, -141.75], z 289 to 325, drawn solid. Visible: no cut piece in that u-z box (pilot u [-171, -149], coupling unsectioned) | correct |
| omitted | No row drawn in front of the plane or past 60. The 12 inset-only rows classify as omitted (P5T p5) | correct for rows |
| omitted, not_drawn parts | Not classified: the rear nut shoulder screw lies in the beyond band | FIX TP1.3-12 |

Hidden edges where the renderer says:
- r1 has no hidden edge. The only beyond row is visible.
- Every dashed artist in the section is a declared non-part line: the keep-out reference, the wingnut sweep extent, the nut-station dash-dot ticks.
- Under the rule of TP1.3-11, edges hidden behind unsectioned rows are missing today. Examples: the core inside the drill head, the shaft ends inside the coupling.

## 3 K9 coverage

- **Section:** 49 rows, every row drawn, every tagged artist a row or an admitted sub-artist (JSON K9 [section] pass; MEASURED tag list). The admitted sub-artists are:
  - `anchor_bearing_c:line` (1 Line2D u -173 to -147 at 340.00);
  - `anchor_bearing_c:balls` (4 circles);
  - `guide_bearing_c:balls` (2);
  - `home_switch_c:lever` (1 Line2D (-190, 1182) to (-182, 1172)).
- **Inset:** 23 rows, the spec `insets[0].rows` list exactly (JSON K9 [inset_plan] pass):
  - screws a, b, c;
  - nut housings a, b, c;
  - anchors a, b, c;
  - lift motors a, b, c;
  - members a, b, c;
  - home switches a, b, c;
  - keepout, ring_ref, section_line, plan_axes, sync_callout.
- **Sync method in the inset:** sync_callout, three dotted leaders from the controller mark (-322.00, 304.00) to the lift-motor centres, plus the three home switches (MEASURED extents). No belt; Design Notes 31 picks one controller.

## 4 S3-3 chain order per screw

**Sequence (MEASURED from the spec):**
- Chain c: 19 links, continuous (pair[i][1] = pair[i+1][0]) and closed (last row = first row).
- Chains a and b: 16 links each, continuous and closed.
- Order c: drill_head, core_750, core_seat, collet, holder, receiver, base_plate, base_frame, frame_upper_c, bracket_anchor_c, anchor_c, anchor_bearing_c, anchor_locknut_c, screw_c, nut_c, nut_housing_c, ring, bearing, drill_tube, drill_head.
- Chains a and b go plate, member, bracket, anchor, screw, and drop the bearing and locknut rows. SYM range p(anchor_c) to p(screw_c) - 1 covers the three c links.

**Sense premise (DERIVED).** In the cut case the loop carries one axial force: the cutter reaction pushes the drill up, the nut holds the ring down, and the screw below the nut is in tension. At every link x → y, written in chain order, the force of x on y is -Z: x holds y down. Checked link by link:
- head pushes core down;
- receiver pushes plate down;
- the base frame holds the member down against the bracket's pull;
- the cover holds the bearing down against the locknut;
- the nut holds the housing down;
- the ring holds the bearing down against the tube.

So a horizontal face carries the link in compression only when x lies above the face: x's bottom edge and y's top edge on the face z. A face with x below is loaded in tension and opens. A vertical shared edge carries no axial load.

**Drawn contacts of chain c in the section** (`p2_faces.py`, MEASURED; "x above" = x's piece above the shared horizontal edge):

| # | Link | Certifier | Drawn contact | Cut-case sense |
|---|---|---|---|---|
| 1 | drill_head → core_750 | declared (load application) | — | declared |
| 2 | core_750 → core_seat | S3 | face 102.50, x above, u ±[47, 50] | compression |
| 3 | core_seat → collet | S1 | vertical only (u ±50, z 100 to 102.5) | **no axial face** |
| 4 | collet → holder | S1 | cone, collet face normal (-32.00, +5.64) per unit; the holder face points down and in | **opens** (an upward-narrowing cone pushes the collet down; it cannot hold it up) |
| 5 | holder → receiver | S1 | vertical only (u ±67.29, z 109.09 to 188.5; holder flange top 197.09 to 205.09 clear of the rim 188.5) | **no axial face** |
| 6 | receiver → base_plate | S3 (face 12 z_A) | face 72.00, x above, u ±[80.2, 100] | compression |
| 7 | base_plate → base_frame | S1, S2 | off the plane; plate on the rails (DERIVED) | compression |
| 8 | base_frame → frame_upper_c | S2, S3 | face 60.00, **x below** (member foot on the rail top) | **tension: face opens** |
| 9 | frame_upper_c → bracket_anchor_c | S2, S3 | vertical only, u -244 | **side face: fasteners** |
| 10 | bracket_anchor_c → anchor_c | S2, S3 | vertical only, u -181 | **side face: fasteners** |
| 11 | anchor_c → anchor_bearing_c | S3 (face 288 z_A) | face 348.00 x above (cover); also face 332.00 x below (block shoulder, lifting cases) | compression at 288 |
| 12 | anchor_bearing_c → anchor_locknut_c | S3 (face 272 z_A) | face 332.00, x above | compression |
| 13 | anchor_locknut_c → screw_c | S3 | vertical (M10x1 thread) | thread, needs its own kind |
| 14 | screw_c → nut_c | S3 | vertical (Tr12x3 thread) | thread |
| 15 | nut_c → nut_housing_c | S3 (face) | face 387.84, x above | compression |
| 16 | nut_housing_c → ring | S3 | vertical (one body, spec) | one body |
| 17 | ring → bearing | S1, S2, S3 | vertical only, u ±100 (bearing top flush with the ring top) | **no axial seat drawn** |
| 18 | bearing → drill_tube | S1, S2, declared | vertical only, u ±76.2 | **no axial seat drawn** |
| 19 | drill_tube → drill_head | declared | face 351.21, x above | compression |

**Chains a and b (DERIVED):**
- Same base route, links 3 to 5.
- Member foot on the plate top: S1 frame_upper_a z_min = `base.plate_thickness`; S1 source "member foot bolted on the plate top". The face is in tension. The spec's own kept-parts entry confirms it: "plate also takes 508.07 up at members a, b".
- Bracket side faces at r 244 and r 181.
- ring|bearing and bearing|drill_tube.

That is 8 per chain and **24 of 51 links** whose certified contact does not carry the cut-case axial load in its direction. FIX TP1.3-10.

The drawn compression path at the base is core_750 → core_seat (face 102.50) → receiver floor at 100.00 z_S. The collet foot also seats on the receiver floor at 100.00 (MEASURED: core_seat|receiver and collet|receiver, x above, u ±[47, 50] and ±[50, 67.29]). The holder carries no cut-case axial load in the drawing. The `kept_axial` report lists 1000 N in the holder (DECLARED, spec load_cases cut). That item goes to The Loftsman and The Designer under TP1.3-10.

## 5 TP-n: parts drawn narrower than their footprints

Drawn extent against the place footprint (`p6_tpn.py`, MEASURED). Every other placed row is drawn equal to its footprint extent.

| # | Row | Axes | Drawn | Footprint | Inset each side | True part? |
|---|---|---|---|---|---|---|
| 1 | liftmotor_c | section | u [-181.00, -139.00] | u [-189.70, -130.30] (round r 29.70) | 8.70 | yes: the 42 square cut at x = 0 |
| 2 | liftmotor_c | inset | x [-21, 21], y [-181, -139] | r 29.70 circle | 8.70 | yes |
| 3 | liftmotor_a | inset | square at 150 deg, x [-167.25, -109.88] | circle x [-168.26, -108.87] | 1.01 | yes |
| 4 | liftmotor_b | inset | square at 30 deg | circle | 1.01 | yes |
| 5 | nut_screws_c | section | u [-149.00, -139.00] | u [-181.00, -139.00] (the nut-flange footprint) | 32.00 / 0.00 | yes: inboard screw at u = -160 + 16 = -144, r 144 < 160, inboard sign holds (DERIVED) |

**TP-n list length: 5.** Each row is the true part. None hides a wrong shape. The anchor rows (42 square, radial place) are drawn equal to their footprints in both Axes. mirror_about_radial holds: the anchor in the inset at (u, t) = (139 to 181, ±21) in its radial frame (MEASURED, P5T FIX 6 form).

## 6 S1 r8 and S2 r9 changed rows

### 6a K5 mark admission at S1 r8 (`anchor_<s>:line`), re-check due under the P0T ruling

Hand values on every pose (`p4_s1s2.py`, MEASURED; mark.z by check_stack). The values are identical at load, start, capture_end and park:

| Check | anchor_a | anchor_b |
|---|---|---|
| M1 declared | `s1_spec.yaml` l.858: mark {sub: line, z: "jackscrew.anchor_z + jackscrew.anchor_allowance / 2"} | l.874, same |
| M2 parent area drawn | block rectangle x [-167.25, -109.88], z 325 to 355, least thickness about 19 mm | x [109.88, 167.25] |
| M3 | one Line2D, 2 vertices, per pose | same |
| M4 signed cross, least over the 4 edges of the CCW block and both endpoints | 0.000 (endpoints on the edges) | 0.000 |
| M5 direction | dz 0.00 | 0.00 |
| M5 place | z 340.00 = mark.z 265 + 30 / 2 + 60 = 340.00 (DERIVED) | 340.00 |
| M5 endpoints on vertical edges | (-167.25, 340), (-109.88, 340) | (109.88, 340), (167.25, 340) |
| `mark_issues` | [] | [] |

- Width: 57.37 = 2 x (21 cos 30 + 21 sin 30) = 2 x 28.69, the projection of the 42 square at theta 150 and 30 (DERIVED).
- Butt cap: no stroke runs past the block edge.
- The S3 section form matches: `anchor_bearing_c:line` is at u -173.00 to -147.00 (bearing OD 26 about u -160) at 340.00 z_S. Both marks name the same plane, 280 z_A.
- Controls K5-B26 to B32 and K5-B36 match in the P6 run (368/368, DECLARED by P6).

**Mark admission re-checked: SIGNED.** The P0T option A stands. Option B (delete the line) is not needed.

### 6b Sense and projected_extent on the changed rows (MEASURED)

**S1 r8, all four poses:**
- anchor_a and anchor_b: drawn x equals the footprint x [-167.25, -109.88] and [109.88, 167.25]; centres ±138.56 = 160 cos 150 and 160 cos 30.
- Screws Tr12x3: x [-144.56, -132.56] and [132.56, 144.56], 12 wide, equal to the footprint.
- Nut and guide D42: equal to the footprint.
- Anchor below nut below guide: 340.00 < 380.84 / 1030.84 / 1155.84 < 1210.00.
- Receiver shoulder pieces u ±[80, 100], z 72 to 80, on the plate top 72.00.

**S2 r9:**
- anchor_a, _b, _c: azimuth 150.00, 30.00, 270.00, r 160.00.
- Pieces symmetric about the radial: (u, t) = (139 to 181, ±21).
- Drawn dashed: wholly under the ring annulus 100 to 210. Corner radii 140.58 and 182.21 lie inside it (DERIVED).
- Screws: circles d 12 at r 160.
- receiver_shoulder: circle r 100, dashed. It is wholly under the bearing annulus (76.2, 100) plus the drill-tube disk r 76.2 (DERIVED).
- K8 holds: S1 346 and S2 208 predicates (JSON).

**S1/S2 revision verdicts: S1 r8 CROSS-REVIEW PASS; S2 r9 CROSS-REVIEW PASS.** NOTEs TP1.3-17 and -18.

## 7 Sub-artist rulings (Engineer open items D2, D3, D4)

| Item | Ruling | Rule (h): premise, check, Z, B |
|---|---|---|
| D4 plan-inset theta arc | **Admission needed, and wanted.** The arc is the one artist that states the theta sense on the figure. Today the sense rests on an untagged Text, and the axes_not_inverted mark branch passes one diagonal (my P5T NOTE 5). | Declared sub-artist `plan_axes:arc` in `sub_artists`, plan_xy only. One Line2D or FancyArrowPatch. Every point on the circle about the origin at the declared radius within 0.05. Consecutive points with cross(p_i, p_i+1) > 0: counter-clockwise seen from +Z, the ASSEMBLY.md convention as a sign check. Start at the declared theta0, end at theta1 > theta0, head at theta1 with tangent . (-sin theta1, cos theta1) > 0. K8 plan_extent reads the parent pieces without the arc. Z: arc 0 to 90 deg at r 40. B1: points reversed (clockwise). B2: radius +5. B3: the arc in the section Axes. FIX TP1.3-13. |
| D3 anchor cover reversed hatch and joint line | **No sub-artist.** The joint line already exists: the cover pieces at 348.00 to 355.00 z_S are separate artists from the block pieces (MEASURED). The alternate hatch is a clause (1) extension. | Spec `hatch_split.at` selects the pieces wholly above `at`. Clause (1) accepts HATCH_ALT[material] on exactly those pieces and HATCH[material] on the rest. Spec lint: every HATCH_ALT value differs from every HATCH value and every other alternate. Aluminium reversed `\\` equals steel today, so The Designer sets the alternate. The renderer applies the same split. Z: r2 anchor_c. B1: a cover piece with the plain hatch. B2: a block piece with the alternate. B3: alternate equal to a material pattern. FIX TP1.3-14. |
| D2 screw c thread ticks | **Admission needed if drawn.** 274 ticks at 3 mm render at 2.58 px pitch (lead 3 x 0.86 px per mm, P6 D6, DERIVED), a grey band. My pick, if The Designer keeps a thread mark: the simplified form, two dashed root lines. | Declared sub-artist `screw_c:root` in a side or section view. Two vertical Line2D at u_c ± d_r / 2 (d_r `jackscrew.root_diameter` 8.5). z from `jackscrew.thread_start_z` to `thread_end_z` (z_S 360 to 1180) within 0.05. Each inside the drawn screw piece over that range. The lead stays in the label. If ticks are kept, the K5 form is: one LineCollection; each segment's ends on the two vertical edges of the screw piece at its z; dz <= 0.05; stations from + k x lead; count floor((to - from) / lead) + 1. Z and B as for the root lines (B: one line at d / 2, one past thread_end + 5, ticks at 3.1 spacing). FIX TP1.3-15 (owner The Designer for the form). |

These three rules are mine to sign when they land at P9.

## Findings

| ID | Kind | Owner | Finding |
|---|---|---|---|
| TP1.3-10 | FIX | The Designer (spec chains), The Engineer (S3-3), The Loftsman (kept_axial) | S3-3 certifies contact without load sense. 24 of 51 links pass on a contact that cannot carry the cut-case force in its direction: 8 per chain, section 4. (a) Base route: core_seat → collet (side), collet → holder (cone opens), holder → receiver (radial fit). Drawn path: core_seat or collet foot on the receiver floor, face `receiver_floor` (100.00 z_S, x above). The holder carries no cut-case load in the drawing; the `kept_axial` row lists it at 1000 N. (b) Member foot faces in tension: base_frame → frame_upper_c at 60.00 (x below), base_plate → frame_upper_a and _b. (c) Bracket side faces at u -244 and -181 (each chain). (d) ring → bearing and bearing → drill_tube: radial fits only, no axial seat drawn. Remedy: link `kind` in the spec chains: face, thread, one_body, declared (fastened: Step 2 bolt row; S6-5). Face links name `face {z}`. The predicate: x's drawn bottom edge and y's top edge on the face z, u overlap > 0.05 (x above y: compression under the -Z force on y). (b) and (c) declared fastened. (d) declared S6-5 only, the K7 certifiers removed. (a) rerouted. Dry run (`p2_faces.py`, MEASURED): the face links pass at 102.50, 72.00, 348.00, 332.00, 387.84 and 351.21; a face kind on link 8 fires (x below at 60.00); a face kind on links 9 and 10 fires (no horizontal edge). B: S3-3-B12 anchor_c\|anchor_bearing_c face named at the block shoulder 272 z_A (332.00 z_S, x below; the current face test passes it); S3-3-B13 base_frame\|frame_upper_c as face; S3-3-B14 frame_upper_c\|bracket_anchor_c as face. Z: the r2 spec with the kinds. |
| TP1.3-11 | FIX | The Engineer (K8 clause), The Designer (classes) | Convention clause (2) has no occlusion premise. An unsectioned row has its axis in the plane: a solid of revolution whose front surface at u lies at x = +sqrt(R² - (u - u_c)²) > 0. Any area at x <= 0 inside its outline lies behind it. In r1, 8 row pairs overlap with solid pieces (`p7_occl.py`, mm², MEASURED): wingnut over receiver 2 x 399.22, holder 2 x 691.60 + 2 x 176.32, and core_750 5600.00; drill_head over core_750 10636.90 + 1270.00; coupling_c over screw_end_c 72.00 and liftmotor_shaft_c 50.00; motor_shaft_c over pinion_c 152.00; liftmotor_shaft_c over liftmotor_pilot_c 10.00. K8 passes r1. Rule: a solid unsectioned piece overlaps no other area piece of the section Axes by more than 0.01 mm², unless that piece is split and drawn dashed inside the outline (renderer). Remedy by row: wingnut and drill_head cut (The Designer 1.3 (a) section 2 lists both as cut; the drill head is a hollow core bit), or the inner rows dashed. pinion_c and liftmotor_pilot_c drawn as their true cut with the shaft bore. Coupling cut, or the shaft ends dashed. Z: r2. B: r1 live (8 pairs). |
| TP1.3-12 | FIX | The Designer (spec), The Engineer (lint) | not_drawn parts are not classified against the band. The rear nut shoulder screw sits at (-13.86, -168) (PCD 32, -60 deg from the outboard radial, DERIVED). Its x band with the D10 head is [-18.86, -8.86]: inside the beyond band 0 > x >= -60. The convention draws it (shank dashed behind the housing, head solid above the flange top 395.84); the figure note says "off the plane". Remedy: draw it as a beyond row, or state in `section.convention` that fasteners beyond the plane are not drawn. Lint: each not_drawn entry names a row id of S1/S2/S3 or an x band, and omitted_row_issues reads it. Same lint, NOTE case: pinion_a's footprint x1 -59.66 enters the band by 0.34 (MEASURED, S1/S2 stack). The true trapezoid's toe corner is at x = -95.22 cos 30 + 34.75 sin 30 = -65.09, past -60 (DERIVED), so pinion_a is correctly omitted. The lint reads the true outline where a row has one. |
| TP1.3-13 | FIX | The Engineer, The Designer | Theta arc: admission `plan_axes:arc` with the ccw sign check (section 7). |
| TP1.3-14 | FIX | The Designer (alternate pattern), The Engineer | Anchor cover hatch: clause (1) per-piece alternate under `hatch_split`; no sub-artist (section 7). |
| TP1.3-15 | FIX | The Designer (form), The Engineer | Screw thread mark: admission `screw_c:root` (or `:ticks`), or remove `ticks` from the spec (section 7). |
| TP1.3-16 | NOTE | The Engineer | The K8 record carries counts only. Hand values compare against "0 issues". A K8 test list (pose, row, predicate, measured, sign), as K7 carries, makes cross-review hand checks comparable. |
| TP1.3-17 | NOTE | The Engineer | The S1 anchor mark.z restates the arithmetic of `jackscrew.anchor_bearing_z`; S3 names the key. The two agree today only through the K2 expr lint on that leaf. A new expr on the leaf moves the S3 line and leaves S1 at 280. One plane, one name: set the S1 mark.z to `jackscrew.anchor_bearing_z`. |
| TP1.3-18 | NOTE | The Designer (M1) | S1 r8 draws anchor_a/_b at the true projection of the 42 square (57.37 wide). It draws liftmotor_a/_b, the same 42 square at the same theta, at the circumscribing circle (59.39, x [-168.26, -108.87]): 1.01 wider than the part each side (MEASURED). Containment passes. |
| TP1.3-19 | NOTE | The Engineer | P5T NOTE 3 still open. `home_switch_c.lever` u expressions encode u = -r (sin 270 = -1). `r * sind(jackscrew.angle[2])` gives -190.00 and -182.00 and holds at any theta. |
| TP1.3-20 | NOTE | The Engineer | The wingnut sweep envelope (u ±115, dashed) is drawn under the wingnut gid. K5, K6 and K7 read it as part geometry. It belongs to a reference row. |

**Counts:**
- S3 r1: 6 FIX, 5 NOTE, 0 BLOCK.
- TP-n list length: 5.
- Hand checks: K8 below/above 4 predicates and S3-1 agree with the harness.
- S1 r8 mark admission: M1 to M5 hold on 8 marks (2 rows x 4 poses).

## Gameplan lines to change

1. **l.300** (detail 1.3, Carried to S1 r8). Apply after P6 item 4 (`step1.3_engineer_draw_r1.md` section 8).
   - Old (the P6 New text ending): `S3 r1 anchor_bearing_c:line.`
   - New: `S3 r1 anchor_bearing_c:line. Re-checked at P7b (step1.3_topologist_crossreview.md section 6a): M1 to M5 hold on anchor_a and anchor_b at all four poses (endpoints on the block's vertical edges, least signed cross 0.000, z 340.00 = mark.z); mark admission SIGNED, option B not needed.`
2. **l.674** (Design Notes 25, TP1.1-9 row). Apply after P6 item 5.
   - Old: `(done at 1.3 P6, wip/s1_checks_r8.json K5 pass) |`
   - New: `(done at 1.3 P6, wip/s1_checks_r8.json K5 pass; re-checked and signed at 1.3 P7b, step1.3_topologist_crossreview.md) |`
3. **l.670** (Design Notes 25, TP-n row).
   - Old: `(TP1.2-7, S3/S6) |`
   - New: `(TP1.2-7, S3/S6); S3 r1 (Topologist 1.3 (e)): 5 rows, liftmotor_c in the section and the inset (42 square in r 29.70, 8.70), liftmotor_a, _b in the inset (1.01), nut_screws_c in the section (inside the nut-flange footprint, 32.00), each the true part |`
4. **Insertion after l.673**, the line beginning `| TP1.3-4 to TP1.3-9 (renderer notes) |`:
   - New: `| TP1.3-10 to TP1.3-20 (S3 r1 cross-review, step1.3_topologist_crossreview.md) | S3-3 certifies contact without load sense: 24 of 51 links pass on a contact that cannot carry the cut-case force in its direction (base route core_seat, collet, holder, receiver; member feet in tension; bracket side faces; ring and bearing radial fits); link kind face / thread / one_body / declared with a face-sense predicate (TP1.3-10); unsectioned occlusion premise for convention clause (2), 8 row pairs live in r1 (TP1.3-11); not_drawn parts classified against the section band, rear nut shoulder screw in the beyond band (TP1.3-12); sub-artist rulings: plan_axes:arc admission with the ccw sign check (TP1.3-13), anchor cover alternate hatch per piece under hatch_split, no sub-artist (TP1.3-14), screw thread root-line or tick admission (TP1.3-15); NOTEs K8 per-predicate record, S1 mark.z names the key, S1 lift motor at the circumscribing width, lever u expression, wingnut sweep under the part gid (TP1.3-16 to -20) | 1.3 (h) P9 | The Topologist proposes and signs; The Designer (spec chains, classes, patterns, thread form); The Engineer; The Loftsman (kept_axial holder value) |`
