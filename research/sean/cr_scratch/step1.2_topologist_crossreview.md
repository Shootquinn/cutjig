## Corrections to the brief

1. **The phase has no sign to check.** Task 1 asks that "the stated phase has the stated sign". At 120 deg spacing a phase of +60 is the same set as -60 (pinion_c 90 = screw_b 30 + 60 = screw_a 150 - 60). S2-1 computes (pinion - screw) mod 120 = 60 for all nine pairs, and that value is the same for the drawing and for its mirror image. Plan handedness rests on the per-row K8 azimuth predicates and on the axes not being inverted (K8-B18, K8-B19). NOTE TP1.2-4.
2. **"Consecutive screw centres" depends on the order you take.** In azimuth (param index) order b 30, a 150, c 270, the cross products are positive. In letter order a, b, c the screws run clockwise and the pinions run counter-clockwise. NOTE TP1.2-5.
3. **The S2-5b list is not every moving part in the sector.** drill_tube and drill_head both enter the sector at load and are not on `ring_parts`. FIX TP1.2-3.
4. **TP1.2-1 is taken.** It was used at 1.2 (c) for the radial outboard gate. Findings here start at TP1.2-2.

Tags: values from the live r1 build (`s2_plan.build`, `s1_side_poses.build`) and from `wip/s2_checks_r1.json` are MEASURED. Hand values are DERIVED. Design values are ASSUMED as in the overlay. Scratch scripts: `tp_dump.py` and `tp_s1.py` in the session scratchpad. Inputs read: `s2_plan.py`, `s2_spec.yaml`, `checks_s2.py`, `sketch_common.py` (K5, K6 plan, K7 plan, K8, K9, plan_outline, sector helpers), `fixtures/manifest.yaml`, `wip/s2_checks_r1.json`, `wip/s2_plan_r1.png`, `wip/s1_pose_capture_end_r5.png`, `s1_spec.yaml` (changed rows), `step1.2_engineer_draw_r1.md`.

## 1 Handedness (task 1)

Frame: the K8 axes test reads xlim (-354.2, 354.2) and ylim (-399.2, 435.2), both increasing, so neither axis is inverted (MEASURED). Aspect is equal (K3 pass). Seen from +Z, +X is to the right and +Y is up.

**Cross products (p_i x p_j) . z from drawn centroids** (MEASURED; hand value r^2 sin 120 DERIVED):

| Sequence | Products | Hand | Sense |
|---|---|---|---|
| screws in index order: b 30, a 150, c 270 | +22170.25, +22170.25, +22170.25 | 160^2 x 0.8660254 = 22170.25 | counter-clockwise |
| screws in letter order: a 150, b 30, c 270 | -22170.25 (x3) | | clockwise |
| pinions in letter order: a 210, b 330, c 90 | +11575.25 (x3) | 115.6112^2 x 0.8660254 = 11575.25 | counter-clockwise |
| pinions in index order: c 90, a 210, b 330 | +11575.25 (x3) | | counter-clockwise |

Pinion centroid radius: 115.6112 MEASURED. Hand calculation, area-weighted: trapezoid 2393.30 mm2 at u 110.782, plus hub 684.30 mm2 at u 132.50, gives 115.611.

**S2-1 azimuths and phase.** The drawn centroid azimuths are screws 30.000, 150.000, 270.000 and pinions 90.000, 210.000, 330.000. For each pinion and screw pair, (p - s) mod 120 = 60.000. Examples: 210 - 150 = 60; 210 - 30 = 180, which is 60 mod 120; 210 - 270 = -60, which is 300 and therefore 60 mod 120. JSON: phase 60 within 0.000, measured 0.0. Hand: 0.000.

**K8 azimuth predicate through the transform chain (screw_a).** The artist is a Circle. Its path is the unit circle. `get_transform() - transData` is the patch transform Affine2D [[4, 0, -138.5641], [0, 4, 80.0000]] (MEASURED). Its 64 sampled curve points lie at radius 4 about (-138.5641, 80.0000), and the centroid is (-138.5641, 80.0000). atan2(80, -138.5641) = 150.000 deg against jackscrew.angle[1] = 150, a residual of 0.000 within the 0.1 tolerance. Hand: 160 cos 150 = -138.5641 and 160 sin 150 = 80. JSON: K8 pass, 114 predicates, 0 issues.

**K8 taper predicate (pinion_c, radial frame at theta 90: u = y, t = -x).** The Polygon has an IdentityTransform. Its vertices are (34.7524, 95.2224), (45.62, 125), (-45.62, 125), (-34.7524, 95.2224). In (u, t) these become (95.2224, -34.7524), (125, -45.62), (125, 45.62), (95.2224, 34.7524). The width is 69.5048 at the inner end and 91.24 at the outer end, so the piece narrows inward by 21.74 (more than 0.05). Hand: toe half-width 45.62 x 95.2224 / 125 = 34.7524. JSON: K8 pass.

**K8 outboard predicate (motor23_c of pinion_c, radial form).** Centroid radius 180.000 against 115.611, a margin of 64.39 (MEASURED; hand (142 + 218) / 2 = 180). JSON: pass.

**S2-3 heel point (pinion_a).** The heel edge runs from (-131.0632, -22.9919) to (-85.4432, -102.0081). Its midpoint (-108.2532, -62.5000) has radius sqrt(11718.75 + 3906.25) = 125.000 and azimuth 210.000. JSON: 125.0.

**Sightline azimuth (K8).** The centroid of the two Line2D pieces is (102.50, 177.54), at azimuth 60.000 against operator.watch_theta 60. The solid piece starts at (105.000, 181.865), and sqrt(105^2 + 181.865^2) = 210.000 = ring.od / 2.

**Datum B.** The +X arrowhead apex is at (L, 0) and the +Y apex at (0, L), with L = drill.tube_id / 2. The theta arc runs from angle 0 to angle 90. Its arrowhead apex is at (0, ra) with barbs on the +x side, so it points along -x. That is the counter-clockwise tangent at 90 deg, which is correct. No check reads this row (NOTE TP1.2-6).

**Which drawn markers break the YZ mirror.** The x mirror maps the screw set {30, 150, 270} and the pinion set {90, 210, 330} onto themselves. The same holds for the sector at 90 and for slot line C. Five markers break the mirror, and each is held by K8 azimuth or K8 plan_extent:
- the descent pad at 150 (one pad);
- the sightline at 60;
- the pin pocket at x +249;
- tie a running from the 0 rod to member b at 30;
- the letters a and b on the screws and pinions.

K8-B19 (screws at -theta) fires on azimuth and plan_extent.

Verdict on handedness: correct (+X along slot line C at y +259, theta counter-clockwise from +X seen from +Z).

## 2 Projection, TP-13 radial-axis rule (task 2)

Rule as implemented (`sketch_common.k5`):
1. A plan row of a round kind (cylinder, screw, cone, gear) with axis X or Y is radial. Its premise is a radial place footprint, enforced as a spec lint.
2. Every four-vertex piece has a pair of edges across the radial direction at its placed theta (within 0.1 deg).
3. A gear row's rectangle piece is admitted as its hub only when it starts on the heel of the row's trapezoid and is no wider than the heel.

The long axis is held radial by K8 plan_extent. The edge-pair test alone is an orientation test modulo 90 deg. A motor turned 90 deg puts 76 across a footprint 57 wide, and the shaft puts 21 across a footprint 8 wide, so both leave the footprint.

Controls: K5-Z3 (live S2) clean. K5-B8 (motor drawn as a circle), K5-B9 (rectangle 10 deg off radial), K5-B10 (premise: round footprint), K5-B11 (hub off the heel) and K5-B13 (hub wider than the heel) all fire (manifest; JSON K5 b_result fired 13/13).

On r1 every radial-axis piece is a rectangle or trapezoid with its tangential pair at its theta:
- pinion_a, _b, _c: trapezoid plus hub. Hub u runs 125.00 to 140.00 with half-width 22.81, against a heel half-width of 45.62.
- motor23 and motor_shaft rows: rectangles.

Axis-Z rows are circles or annuli: screws, nuts, blocks, housings, rods, bushings, tube, bearing, gear, hub, ring, cutter rim and keep-out.

**TP-13: SIGNED on S2 r1.**

## 3 Sector and sightline half-spaces (task 3)

Sector (MEASURED from the stack): apex at the origin, theta 90, half-angle 45, r 400. Inward normals:
- n45 = (-sin 45, cos 45)
- n135 = (sin 135, -cos 135)

A point p is inside the sector iff n45 . p >= 0, n135 . p >= 0 and |p| <= 400. A convex outline piece lies outside when the maximum of n . p over its vertices is below 0. That maximum is the support value, and the 128-gon outlines circumscribe their parts, so the test is conservative. In the table, "margin" is the negative of that support value: the distance clear of the edge line.

| Fixed part (S2-5a list, 27) | Separating half-space | Margin (MEASURED) |
|---|---|---|
| frame_upper_a / _b / _c | n135 / n45 / both | 34.17 / 34.17 / 151.32 |
| liftmotor_a / _b / _c | n135 / n45 / both | **11.71** / **11.71** / 83.44 |
| anchor_a, guide_a / anchor_b, guide_b / anchor_c, guide_c | n135 / n45 / both | 20.41 / 20.41 / 92.14 |
| bracket_anchor_a, bracket_guide_a / _b / _c | n135 / n45 / both | 17.87 / 17.87 / 106.77 |
| descent_stop, descent_stop_post (150) | n135 | 22.79 |
| guide_member (0) / guide_member_b (180) | n45 / n135 | 152.64 / 152.64 |
| guide_tie_a / guide_tie_b | n45 / n135 | 76.35 / 76.35 |
| screw_a / _b / _c | n135 / n45 / both | 37.41 / 37.41 / 109.14 |

No part needs the arc boundary. Least: liftmotor_b. Hand: 160 sin 15 - 21 sqrt 2 = 41.411 - 29.698 = **11.713**. JSON S2-5a: least 11.713. The drawn 42 square clears by 41.411 - 21 (cos 15 + sin 15) = 15.69, as in gameplan l.257.

Moving parts whose plan outline enters the sector at load (MEASURED, overlap area greater than 0.01):

| Row | On S2-5b list | Lowest z_A | Margin over 940 |
|---|---|---|---|
| bearing | yes | 1076.84 | 136.84 |
| ring | yes | 1089.84 | 149.84 |
| motor_mount_c | yes | 1101.84 | 161.84 |
| pinion_c | yes | 1108.22 | 168.22 |
| motor23_c | yes | 1125.34 | 185.34 |
| motor_shaft_c | yes | 1149.84 | 209.84 |
| gear, gear_hub | yes | 1182.07 | 242.07 |
| **drill_tube** | **no** | 1066.21 | 126.21 |
| **drill_head** | **no** | 959.84 | **19.84** |

The keep-out also enters, but it is kind line and is excluded correctly. JSON S2-5b: 8 ring parts, least 136.84. With the two drill rows, the least is 19.84 (drill_head). It passes g_min 10, but no check computes it. FIX TP1.2-3.

**Sightline F6.** The direction u60 = (cos 60, sin 60) satisfies n45 . u60 = sin 15 = 0.2588 and n135 . u60 = sin 75 = 0.9659, so it lies inside the sector. The observer point at r 400 lies on the arc. Solid r 210 to 400, dashed 0 to 210: the dashed part is under the ring rim, as the shape requires.

Sign of n60 . p for parts beside the solid segment, with n60 = (-sin 60, cos 60):

| Side | Part | Distance from the segment (MEASURED) |
|---|---|---|
| clockwise (n60 . p < 0) | bracket_guide_b | 75.00 |
| clockwise | liftmotor_b | 77.55 |
| clockwise | nut_housing_b | 82.24 |
| clockwise | frame_upper_b | 96.02 |
| clockwise | guide_tie_a | 131.16 |
| clockwise | guide_lug_a | 192.94 |
| counter-clockwise | motor23_c | 76.50 |
| counter-clockwise | motor_mount_c | 76.50 |
| counter-clockwise | frame_upper_a | 303.21 |

Hand checks:
- motor23_c corner (28.5, 142): 144.83 sin 18.65 = 46.32 is its n60 . p. The 76.50 in the table is the distance to the segment, which starts at r 210.
- bracket_guide_b inner corner: 183.47 sin(-20.59) = -64.52.

The solid segment crosses nothing but the plate.

## 4 K9 coverage (task 4)

K9 r1: 70 rows, every row drawn, no tagged artist outside the spec, and no row with a pose set (JSON pass). K5 r1: 99 tagged artists and no untagged patch, line or collection (JSON pass). Part tags and margin notes are Text without a row gid, and K9 admits them.

S2-f presence (MEASURED, artists per row in the dump):
- screws a, b, c
- nuts and nut housings a, b, c
- anchors and guides a, b, c
- both arms on a, b, c
- lift motors a, b, c
- frame members a, b, c
- pinions a, b, c, each with trapezoid and hub
- NEMA 23 a, b, c
- shafts and axes a, b, c

All are present.

## 5 TP-n: parts drawn narrower than their footprints (task 5)

From the live build (MEASURED): the largest distance from an outline vertex to the drawing, and the drawn area against the outline area.

| Row | Outline | Narrower by | Area drawn / outline (mm2) |
|---|---|---|---|
| liftmotor_a, _b, _c | circle r 29.70 (circumscribing, `true` False) | 8.70 (hand 21 sqrt 2 - 21 = 8.698) | 1764.0 / 2771.4 |
| pinion_a, _b, _c | radial rectangle r 95.22 to 140, half-width 45.62 (`true` False) | 15.00 at the hub corners (heel corner 125, 45.62 against footprint corner 140, 45.62) | 3077.6 / 4085.5 |

Every other area row equals its outline within 0.031. The residue is the 8-segment Bezier circle against the 128-gon. TP-n list length: **6**. M1 reads the lift motor squares and the pinion trapezoids with hubs as the shapes they are.

Line rows are outside TP-n: the spigot hole, keep-out, cutter rim circle, slot lines, pinion axes and sightline. The drill tube draws its true annulus inside a solid disk outline (NOTE TP1.2-7).

## 6 S1 r5 changed rows (task 6)

Triggered by frame_upper.radius 300 to 274 (Design Notes 27) and by the rows guide_bushing_a, _b and guide_tie_a, _b (Design Notes 28). The table gives drawn x against the footprint projection at every pose, MEASURED from the live build. Drawn equals footprint at load, start, capture_end and park.

| Row | Drawn x = footprint x | Centre x / hand | z |
|---|---|---|---|
| frame_upper_a | -278.27 to -196.31 | -237.29 / 274 cos 150 = -237.29; half-extent 30 (cos 30 + sin 30) = 40.98 | 72 to 1285 |
| frame_upper_b | 196.31 to 278.27 | 237.29 | 72 to 1285 |
| bracket_anchor_a, bracket_guide_a | -226.31 to -141.75 | -184.03 / 212.5 cos 150; corners u 244, t +30: -211.31 - 15 = -226.31; u 181, t -30: -156.75 + 15 = -141.75 | 325 to 355; 1195 to 1225 |
| bracket_anchor_b, bracket_guide_b | 141.75 to 226.31 | 184.03 | as a |
| guide_bushing_a / _b | 210 to 250 / -250 to -210 | 230 / -230 | ring_bottom - 30 to ring_bottom per pose |
| guide_tie_a / _b | 198.45 to 265.04 / -265.04 to -198.45 (plan_x) | spec corners (198.45, -28.36) to (265.04, 93.96) | 1225 to 1285 |

Sense predicates on the changed rows, hand values at load:
- bracket_anchor_a outboard of anchor_a: (x - x_anchor) cos 150 = (-184.03 + 138.56)(-0.8660) = **39.375**. Hand: (212.5 - 160) cos^2 150 = 52.5 x 0.75 = 39.375. At r4: (225.5 - 160) x 0.75 = 49.125.
- bracket_guide_a outboard of guide_a: 39.375. The b side is the same.
- bracket_anchor below nut_a: centroid z 340.00 against 1155.84.
- bracket_guide above nut_a: 1210.00 against 1155.84.
- At capture_end the nut sits at 365.84 to 395.84 with centroid 380.84, against the anchor arm at 340.00, so the arm is below by 40.84.

frame_upper rows carry no sense in S1. JSON S1 r5: K8 346 predicates pass, K9 58 rows, K5 343 artists. The four new rows have no drawn extent outside their footprints.

**S1 r5: CROSS-REVIEW PASS.**

## 7 Findings

**FIX TP1.2-2 (Engineer, r2; Designer signs the legend). Hidden-line sense in plan: rows wholly under a nearer part are drawn as visible.**

Seen from +Z, a point of row A is hidden when some row B has a true plan section over that point and z_max(B) > z_max(A). The figure's own legend states "dashed: under a nearer part". MEASURED at load from the drawn pieces, sampled at 98 % toward each piece centroid, against true outlines of rows with a higher top. These rows are covered at every sample and drawn solid:

| Row | Top z_S | Covered by (top z_S) |
|---|---|---|
| nut_a, nut_b, nut_c (brass fill) | 1170.84 | guide_a, _b, _c (1225.00), both of r 21 |
| descent_stop (hatched) | 374.84 | bracket_guide_a (1225.00): pad r 200 to 215 x 60 inside arm r 181 to 244 x 60; also the ring rim (1161.84) over r 200 to 210 |
| motor_mount_a, _b, _c | 1185.34 | motor23_a, _b, _c (1242.34): mount r 142 to 210 inside motor r 142 to 218, same half-width 28.5 |
| guide_lug_a, guide_lug_b | 1161.84 | guide_tie_a, _b (1285.00) |
| guide_member, guide_member_b | 1272.00 | guide_tie_a, _b (1285.00); rod top in the tie bore |

The ties are the topmost parts at their positions (1225 to 1285). They are drawn dashed, which the spec asks for as the Step 2 stand-in. The legend files them under "under a nearer part", and that statement is false for the ties.

These rows are drawn correctly hidden (all at coverage 1.00 and dashed or dotted): base_frame, anchors, anchor arms, lift motors, post, bushings, bearing, cutter rim.

Close at r2:
1. The seven non-stand-in rows (nuts x3, descent_stop, motor mounts x3) are drawn hidden.
2. One of these two:
   - the legend separates "dashed: Step 2 stand-in (rod top ties), drawn see-through" from "dashed: under a nearer part"; or
   - the ties are drawn as the visible top, with the lugs and rod tops hidden.

   Designer's pick, with the N2 guide read at M2 in mind.
3. I re-run the coverage computation on r2.

No new check is required to close this FIX. NOTE TP1.2-9 proposes one.

**FIX TP1.2-3 (Engineer; Designer as the S2-5b raiser; Topologist signs). The S2-5b premise set is a hand list and misses two moving rows in the sector.**

S2-5a relieves the sector of every moving part on the premise that each moving part in the sector at load lies above the hand band. S2-5b tests only `ring_parts`. drill_tube (126.21) and drill_head (19.84, the tip) enter the sector and are not tested. Both pass today. A moving row added later (S3 motor mount, S6 bearing parts) would escape the same way. Process fix (h) requires the premise to be enforced.

Fix: S2-5b tests every row with `moves: true` that is not `reference` and not of a NO_AREA kind and whose plan outline enters the drawn sector. Keep `ring_parts` only as an optional cross-check, or drop it. Controls:
- Z: live S2 (10 rows; least drill_head 19.84).
- B1: the existing NEMA 23 c at 930 z_A fires.
- B2 (new): drill_head drawn with its tip at the hand band top + 5 at load fires "drill_head: ... 5.00 above the hand band top 940". On the r1 code B2 reads clean, which is the red-first evidence.

The reported value "drill tip above the hand band at load 19.84" then becomes the S2-5b least.

**NOTE TP1.2-4. The phase sign is unobservable.** At phase = spacing / 2, +60 and -60 are one set (section 1). S2-1 is invariant under the x mirror, and on its sets also under the y mirror. Handedness is carried by K8 azimuth (one predicate per placed row) and by the axes test. K8-B18 and K8-B19 hold it. No action.

**NOTE TP1.2-5. Letter chirality.** Screw letters a, b, c run clockwise (-22170.25). Pinion letters a, b, c run counter-clockwise (+11575.25). Both come from the S1 letter map (screw a = jackscrew.angle[1], pinion c = pinion.angle[0]). No check reads letter order. The plan tags carry letter and azimuth together, so a reader is not misled. Record for M2 and for Step 2 wiring names; no change proposed.

**NOTE TP1.2-6. Datum B is unchecked.** collet_axis (kind arrow, sense []) carries the +X and +Y arrowheads and the theta arrowhead. On r1 all three point the right way (section 1). A reversed theta arrowhead passes every K check, so M1 reads it. If wanted, a K8 predicate on arrow rows checks (head - tail) x (tangent) for the arc.

**NOTE TP1.2-7. Hollow rows carry a solid "true" outline.** plan_outline returns ("annulus", (0, OD/2), true) for drill_tube and drill_head (round, centred, projection circle). The tube is an annulus with bore r 73.025, and the cutter is a hole saw. A C pair seated inside the bore would pass contact on an outline that is no true section. No pair does so today: tube|bearing and tube|gear_hub touch at r 76.20, which is exact on the annulus as well. To S3 or S6, where collet and core may enter the plan.

**NOTE TP1.2-8. Dead K8 branches.** In `k8`, `if plan:` sits inside `if pl and side:` (projected_y, projected_extent_y), and again inside the plan_poly side branch. Neither block ever runs. Plan containment is plan_extent. No manifest control expects those reasons. Delete them, or leave them for the Software Engineer.

**NOTE TP1.2-9. Pinion over gear, and an optional cover predicate.**
- The pinion toothed pieces (r 95.22 to 125) lie inside the gear annulus (r 90 to 126.32, top 1275.84 against the pinion top 1259.46). The heel corners stick out at r 133.07, so the pinion is partly visible and solid is legal. Both pieces are drawn with hatch at equal zorder, and the pinion is painted after the gear, so the plan reads as pinions over the gear. Design Notes 22 has the gear above. This goes to M1 (V3, V7).
- Optional K8 plan predicate `cover`: a drawn piece wholly inside true outlines of rows with z_max greater by more than 0.05 is drawn non-solid. Premise: only `true` outlines count as cover. Controls:
  - Z: live S2 after FIX TP1.2-2.
  - B1: nut_a drawn solid under guide_a.
  - B2: the premise, a circumscribing lift-motor circle offered as cover and not counted.
- Raised here; signed only if adopted under (h).

**NOTE TP1.2-10. TP-n on S2 r1: 6 rows** (section 5): liftmotor_a, _b, _c and pinion_a, _b, _c. To M1.

**NOTE TP1.2-11. TP1.1-9 holds in plan.** A zero-radius Circle or a zero-width rectangle passes K5, K6 plan, K8 plan_extent and K9. None are on r1 (section 5: every area row equals its outline). Carried to S3 as listed.

## 8 Verdicts

- TP-13 radial-axis rule: **SIGNED** on S2 r1.
- Handedness: correct, and held by K8 azimuth and the axes test.
- **S2 r1: CROSS-REVIEW FAIL** (FIX TP1.2-2, TP1.2-3).
- **S1 r5: CROSS-REVIEW PASS.**

Counts: BLOCK 0, FIX 2, NOTE 8. TP-n list length: 6.

## Gameplan lines to change

**l.638** (Open Questions, TP-n row):

Old:
```
| TP-n (narrower than footprint) | K8 projected_extent is containment only: a part drawn narrower than its footprint passes (probe: member drawn 60 wide as in r3). Safe for interference; only the M1 read sees it | every M1 from 1.2 on | The Designer (M1); The Topologist at each (e) |
```
New:
```
| TP-n (narrower than footprint) | K8 projected_extent is containment only: a part drawn narrower than its footprint passes (probe: member drawn 60 wide as in r3). Safe for interference; only the M1 read sees it. S2 r1 (Topologist 1.2 (e)): 6 rows, liftmotor_a, _b, _c (42 square in its r 29.70 circle, 8.70) and pinion_a, _b, _c (trapezoid and hub in the radial rectangle, 15.00); drill_tube and drill_head outlines are solid disks flagged true over hollow parts (TP1.2-7, S3/S6) | every M1 from 1.2 on | The Designer (M1); The Topologist at each (e) |
```

**l.258** (S2-5b row; apply when FIX TP1.2-3 lands, not before):

Old:
```
| S2-5b | Premise of the S2-5a relief for ring-mounted parts: at load every ring-mounted part whose plan outline enters the drawn sector lies, by its lowest z, at least 10 above the top of operator.hand_band (940 z_A); no ring part in the sector is a content failure; least: bearing bottom 1076.84, margin 136.84 (1.2 (c)) | Live layout | NEMA 23 at theta 90 drawn at load with its bottom at 930 z_A | hand band ASSUMED |
```
New:
```
| S2-5b | Premise of the S2-5a relief for moving parts: at load every moving row (spec moves: true, not reference, not a line kind) whose plan outline enters the drawn sector lies, by its lowest z, at least 10 above the top of operator.hand_band (940 z_A); no moving part in the sector is a content failure; least: drill_head tip 959.84, margin 19.84 (1.2 (c); set from the spec, TP1.2-3 at 1.2 (e)) | Live layout | NEMA 23 at theta 90 drawn at load with its bottom at 930 z_A; drill_head tip at 945 z_A at load (TP1.2-3) | hand band ASSUMED |
```

**l.491** (Progress Log, add a row after it):

Old:
```
| 1.2 | 2026-11-25 | (d) P6 (`step1.2_engineer_draw_r1.md`): `s2_plan.py` written; `wip/s2_plan_r1.png` first written 17:57:05; S2 r1 17/17 on run 1; S1 r5 18/18 (four poses, mass report equal to r4); members a, b 43.73 from the plate x edge, member c on the rail edge 0.00; cutter overhang 2.70; controls 191/191 (284 s); --stale red on s1 r4 frame_upper.radius only. Open: gear ticks, F6 label "z_S z_S", sightline in the highest-point report, s2 status text. Next: STOP-T5, (e) and M1 in parallel. |
```
New:
```
| 1.2 | 2026-11-25 | (d) P6 (`step1.2_engineer_draw_r1.md`): `s2_plan.py` written; `wip/s2_plan_r1.png` first written 17:57:05; S2 r1 17/17 on run 1; S1 r5 18/18 (four poses, mass report equal to r4); members a, b 43.73 from the plate x edge, member c on the rail edge 0.00; cutter overhang 2.70; controls 191/191 (284 s); --stale red on s1 r4 frame_upper.radius only. Open: gear ticks, F6 label "z_S z_S", sightline in the highest-point report, s2 status text. Next: STOP-T5, (e) and M1 in parallel. |
| 1.2 | 2026-11-25 | (e) Topologist (`step1.2_topologist_crossreview.md`): S2 r1 CROSS-REVIEW FAIL, FIX TP1.2-2 (nuts, descent pad, motor mounts drawn solid under nearer parts; tie legend) and TP1.2-3 (S2-5b misses drill_tube, drill_head; set from moves: true); handedness correct (screw cross products +22170.25 in azimuth order); TP-13 SIGNED; TP-n 6 rows; S1 r5 CROSS-REVIEW PASS (arms outboard 39.375). NOTEs TP1.2-4 to -11. |
```

## Re-check r2

### Corrections to the brief

1. **The r2 records carry the pre-fix control tally.** `wip/s2_checks_r2.json` (19:08:25) and `wip/s1_checks_r6.json` (19:09:13) were written before the final controls run (19:37:04, 214/214). Both read K8 b_result "fired 31/33", which is the 212/214 run (MEASURED). The checks themselves are unchanged. Re-run `check_sketch.py s2 --rev 2` and `s1 --rev 6` so that the record of the revision cites the final tally (NOTE TP1.2-14).

Inputs: `step1.2_engineer_revision_r2.md`, `sketch_common.py` (`hidden_rows`, `cover_issues`, `_cover_samples`, `is_solid`), `checks_s2.py` (`moving_parts`, `s2_5b`), `fixtures/builders.py` (`k8_b19`, `k8_b26`), `fixtures/manifest.yaml`, `wip/fixtures/controls_results.json`, `wip/s2_plan_r2.png`, `wip/s2_checks_r2.json` and `wip/s1_checks_r6.json`. Probes were run in memory on the live r2 build (scratchpad `tp_r2.py`). Results are MEASURED; hand values are DERIVED.

### 1 TP1.2-2: K8 `cover` and the r2 drawing

**Live r2.** K8 cover tests 68 artists with 0 issues. `hidden_rows` at load returns 26 rows:
- anchor_a, _b, _c
- base_frame
- bearing
- bracket_anchor_a, _b, _c
- descent_stop and post
- drill_head
- guide_bushing_a, _b
- guide_lug_a, _b
- guide_member, guide_member_b
- liftmotor_a, _b, _c
- motor_mount_a, _b, _c
- nut_a, _b, _c

The seven rows named in FIX TP1.2-2 are drawn dashed with no fill (nuts x3, pad, mounts x3). The tie legend is split into "under a nearer part" and "Step 2 stand-in". FIX TP1.2-2 is closed.

**Premise: only true outlines count.** `cover_issues` and `hidden_rows` both admit covers only where `plan_outline` returns true. K8-Z7 (a circumscribing circle is no cover) reads clean. K8-B33 (the same motor drawn as its circle covers the pad) fires. Both match (controls_results 19:37:04).

**Own probes (MEASURED):**

| Probe | Planted | Result |
|---|---|---|
| p1 | descent_stop solid, no fill, no hatch | fires: "wholly under bracket_guide_a drawn solid (linestyle '-')" |
| p2 | descent_stop dashed with hatch '//' | fires (`is_solid` counts a hatch) |
| p3 | bearing Annulus solid | fires: "wholly under gear, gear_hub" (annulus samples at 2, 50 and 98 % of its width) |
| p4 | synthetic: bar C (0 to 100 x 0 to 10, top 10) whose ends lie under A (-5 to 20) and B (80 to 105, top 100), middle 60 open | `hidden_rows` = {C}; cover fires on C drawn solid. **Over-cover** (NOTE TP1.2-13) |
| p5 | drill_tube and drill_head marked reference (no cover from the hollow disks) | `hidden_rows` loses drill_head. Its outline samples at r 44.45 and r 1.78 are covered only by the drill_tube disk (TP1.2-7) |

**Fixture restyles, K8-B19 and K8-B26: legitimate.**
- K8-B19 plants each screw at -theta. That puts screw_a at (r 160, 210), under motor23_a (r 142 to 218, half-width 28.5, top 1242.34 against the screw top 1225.00). The same holds for screw_b under motor23_b and screw_c under motor23_c. At those positions each screw is truly hidden, so dashed is the correct style. The planted defects (azimuth x3, plan_extent x3, planted 6) are unchanged, and the match is yes.
- K8-B26 redraws the bearing annulus with its bore 5 under its section. The bearing is hidden under the gear and hub in the live drawing (dashed at r1 and r2). The restyle returns the non-planted property to the live style, and the planted plan_extent (by 5.00) still fires alone.

Both restyles isolate the B on its own defect.

**Over-cover is the direction the rule tolerates.** All three over-cover routes can only add rows to the hidden set:
- p4: vertex samples against a union of covers;
- vertex samples against an annulus cover (a chord piece can span the bore);
- a hollow part with a solid true disk (TP1.2-7).

The cover check then demands dashed, and a solid hidden part still fires, so no solid-hidden defect passes. The converse case, a visible part drawn dashed, is not checked. `hidden_rows` now generates the drawing styles, so an over-cover reaches the PNG.

One live instance: **base_frame**. The +Y rail (y 244 to 304) has its vertices in the plate edge strips, but the plate column notch (x -35 to 35, y 239 to 304) is open. A 70 x 60 piece of the rail top is visible from +Z and is drawn dashed (DERIVED: rail y 244 to 304 against notch y 239 to 304, x +-35; no row covers it; the sector is reference).

The pinion toothed piece is drawn dashed by choice. Its heel corners at r 133.07 lie outside the gear OD of 126.32, and `hidden_rows` reads it as visible. The legend states "pinion teeth under the gear". This is a Designer convention.

Neither instance passes a solid-hidden defect. NOTE TP1.2-13.

**K8 cover: SIGNED.**

### 2 TP1.2-3: S2-5b over `moves: true`

`moving_parts` takes every `moves: true` row that is not reference and not a NO_AREA kind. `s2_5b` refuses any `parts` other than "moves". Live: 10 moving parts in the sector, least 19.84 (drill_head). Hand: 959.84 - 940 = 19.84. The strike list matches section 3 of this file row for row.

Controls (match yes):
- S2-5b-B2: drill tip at 945 z_A. Red-first: it read clean on the r1 hand list.
- S2-5b-B3: the r1 hand list is refused.
- S2-5b-B1 and S2-5b-Z: unchanged.

**Own probes (MEASURED):**

| Probe | Planted | Result |
|---|---|---|
| p6 | stack drill_head z_min 15 lower | fail: "drill_head: lowest z 944.84 z_A, 4.84 above the hand band top 940, need 10" |
| p7 | `parts: [drill_head]` | refused: "spec parts must be 'moves'" |
| p8 | `parts` key deleted | refused (same reason) |
| p5' | drill_head `moves: false` | pass, 9 parts, least drill_tube 126.21 |

Probe p5' shows that the premise set is only as good as the `moves` flag. That flag is also the K7 swept-case key (one field, two uses). A wrong `moves` already breaks the swept test, so this adds no new failure route.

**S2-5b set: SIGNED.**

### 3 S1 r6

Values equal to r5 (engineer record). The JSON reports 18/18: K8 346 predicates, K9 58 rows, K5 343. No row moved: label anchors moved 0 of 55, and only the save crop changed. Section 6 of this file stands.

### Findings (re-check)

**NOTE TP1.2-13. Cover samples can over-cover.**
- Vertex samples against a union of covers, or against an annulus cover, can declare a partly visible piece hidden (probe p4).
- Since `hidden_rows` drives the r2 styles, the base_frame rail top in the +Y notch (70 x 60) is drawn dashed while visible.
- The rule never passes a solid hidden part.

Fix at S3, or when the converse is wanted: sample the piece interior on a grid, or test containment exactly per cover (convex piece in one convex cover, or the piece's radius range inside one annulus), and treat a union as covering only when the pieces tile. Raise a K8 converse ("visible drawn dashed") only if the Designer wants dashed to mean hidden strictly.

**NOTE TP1.2-14. Records cite the stale tally.** Re-run the two record commands after the final `--controls` (Corrections 1).

**NOTE TP1.2-7, updated.** The hollow-disk outline now feeds `hidden_rows` (probe p5: drill_head is hidden only through the tube disk). There is no drawing effect, because the cutter rim circle at r 88.9 is truly under the gear_hub (r 76.2 to 90, top 1275.84). Still to S3 or S6.

### Verdicts (re-check)

- FIX TP1.2-2: CLOSED. K8 `cover`: **SIGNED**.
- FIX TP1.2-3: CLOSED. S2-5b over `moves: true`: **SIGNED**.
- **S2 r2: CROSS-REVIEW PASS.**
- **S1 r6: CROSS-REVIEW PASS.**

Counts (re-check): BLOCK 0, FIX 0, NOTE 2 new (TP1.2-13, TP1.2-14), TP1.2-7 updated.

### Gameplan lines to change

**l.638** (Open Questions). Add a row after the TP-n row. Old is the TP-n row as it stands after this file's 1.2 (e) change is applied:

Old:
```
| TP-n (narrower than footprint) | K8 projected_extent is containment only: a part drawn narrower than its footprint passes (probe: member drawn 60 wide as in r3). Safe for interference; only the M1 read sees it. S2 r1 (Topologist 1.2 (e)): 6 rows, liftmotor_a, _b, _c (42 square in its r 29.70 circle, 8.70) and pinion_a, _b, _c (trapezoid and hub in the radial rectangle, 15.00); drill_tube and drill_head outlines are solid disks flagged true over hollow parts (TP1.2-7, S3/S6) | every M1 from 1.2 on | The Designer (M1); The Topologist at each (e) |
```
New:
```
| TP-n (narrower than footprint) | K8 projected_extent is containment only: a part drawn narrower than its footprint passes (probe: member drawn 60 wide as in r3). Safe for interference; only the M1 read sees it. S2 r1 (Topologist 1.2 (e)): 6 rows, liftmotor_a, _b, _c (42 square in its r 29.70 circle, 8.70) and pinion_a, _b, _c (trapezoid and hub in the radial rectangle, 15.00); drill_tube and drill_head outlines are solid disks flagged true over hollow parts (TP1.2-7, S3/S6) | every M1 from 1.2 on | The Designer (M1); The Topologist at each (e) |
| TP1.2-13 (cover over-cover) | K8 cover and hidden_rows sample piece vertices: a union of covers, an annulus cover or a hollow true disk (TP1.2-7) can mark a partly visible piece hidden; never passes a solid hidden part; live: base_frame rail top in the +Y notch (70 x 60) drawn dashed while visible; visible-drawn-dashed is unchecked | 1.3 (S3) | The Topologist proposes; The Engineer |
```

**Progress Log.** Add a row after the (h) P9 row (`| 1.2 | 2026-11-25 | (h) P9 (`step1.2_engineer_revision_r2.md`): ...`). Old is that row unchanged; New is that row followed by:
```
| 1.2 | 2026-11-25 | (e) re-check r2 Topologist (`step1.2_topologist_crossreview.md`, Re-check r2): TP1.2-2 and TP1.2-3 closed; K8 cover SIGNED (probes p1 to p5; K8-B19, K8-B26 restyles legitimate), S2-5b over moves: true SIGNED (p5' to p8, least drill_head 19.84); S2 r2 and S1 r6 CROSS-REVIEW PASS; NOTEs TP1.2-13 (cover over-cover, base_frame in the +Y notch), TP1.2-14 (records cite the 212/214 tally; re-run s2 r2, s1 r6). |
```
