# Step 1.2 (e) Loftsman cross-review: S2 r1, S1 r5 (changed rows)

## Corrections to the brief

1. The K7 record cannot be read pair by pair. `wip/s2_checks_r1.json` K7 holds `states`, a list of 7334 strings, with no pose, pair or value. I rebuilt every test by re-running `sketch_common.k7` on the live spec, script and overlay with a logging wrapper on `_plan_judge` / `assess_pair` (scratchpad only; nothing in `docs/` written). The result is the same: S2 1280 tests clean, S1 609 tests clean (MEASURED). My 1.2 (c) NOTE 3 required pair ids before the second drawn revision of any sketch. That is FIX LF1.2-1.
2. Several "plan distance" values in the K7 text and the reported table are lower bounds, not distances. `outline_measure` returns the bounding-box gap when the boxes are more than need + 1 apart. Footprints that circumscribe their parts also read short. Examples: nut_housing_a|frame_upper_a reads 32.746, true 58.99. motor23_a|guide_tie_b reads 14.766, true 46.16. S2-5a reads 11.71 for the lift motors, true 15.69. The passes are sound because a lower bound that clears g_min clears the true distance too. The numbers are not distances. Hand values below give the true figure.
3. The Engineer's tight-spot list leaves out the tightest clearance between two moving parts in the plan, pinion toe to gear hub, 5.22 (FIX LF1.2-2).

Tags: run values MEASURED 2026-11-25 on `docs/sketches/` (r1 record 17:58:08; live re-run same inputs). Hand values DERIVED. Design values ASSUMED as in the overlay.

## 1 S2 hand values beside JSON

### S2-1 azimuths and phase

| Row | Placed centre (x, y) DERIVED | atan2 DERIVED | JSON |
|---|---|---|---|
| screw_b | 160 cos 30, 160 sin 30 = (138.564, 80.000) | 30.000 | 30.0 |
| screw_a | (-138.564, 80.000) | 150.000 | 150.0 |
| screw_c | (0, -160.000) | 270.000 | 270.0 |
| pinion_c | trapezoid and hub symmetric about the 90 ray, r_c 117.611 | 90.000 | 90.0 |
| pinion_a | symmetric about 210 | 210.000 | 210.0 |
| pinion_b | symmetric about 330 | 330.000 | 330.0 |
| phase | 90 - 30 = 210 - 150 = 330 - 270 = 60; spacing 120 for both sets | 60.000, worst 0.000 | 0.0 against 0.1 |

### S2-2 margin

160.00 - 42 / 2 - 86.20 = **52.80** DERIVED; JSON 52.8. The expression reads the nut flange (r 21). The ring nut housing (r 25) has the same centre and leaves 160 - 25 - 86.20 = 48.80 to the keep-out (NOTE LF1.2-6).

### S2-3 pitch point radius

r_heel = gear.pitch_diameter / 2 = 250 / 2 = **125.000** for each pinion (DERIVED). The heel edge is drawn at `pinion.r_heel`, and its midpoint lies on the azimuth ray, so r = 125.000. JSON: pinion_a, _b, _c 125.0, off 0.000. This check is an identity of the overlay (`pinion.r_heel` is defined as `gear.pitch_diameter / 2`) and can fail only if the drawing leaves the overlay (NOTE LF1.2-6).

### S2-4 centres

| Row | Drawn extent DERIVED | Centre |
|---|---|---|
| drill_tube | annulus r 76.20 about origin | (0, 0) |
| collet_axis | cross to L = tube_id / 2 = 73.025 both axes; arrowheads and theta arc inside it | (0, 0) |
| ring | annulus 100 to 210 | (0, 0) |
| gear | annulus 90 to 126.32, pitch circle r 125 | (0, 0) |
JSON 4 centres within 0.000. Agrees.

### S2-5a sector boundary distances (sector theta 90 +- 45, r 400; edges on the 45 and 135 rays)

Distance of a point to the 45 ray = |x - y| / sqrt 2. To the 135 ray = |x + y| / sqrt 2. For a round part at (160, theta) the formula is 160 sin 15 - r = 41.411 - r.

| Fixed part | Nearest point DERIVED | Hand | JSON (live re-run, plan outline) |
|---|---|---|---|
| liftmotor_a, _b (circumscribed circle r 29.698) | 41.411 - 29.698 | 11.71 | 11.713 (check value) |
| liftmotor_a, _b (true 42 square, faces radial) | corner (109.87, 87.69): 22.18 / 1.4142 | **15.69** | n/a (outline is the circle; 15.691 by direct polygon) |
| bracket_anchor_a, _b; bracket_guide_a, _b | corner r 181 + 30 t at 30: (141.75, 116.48): 25.27 / 1.4142 | 17.87 | 17.868 |
| anchor, guide blocks a, b (r 21) | 41.411 - 21 | 20.41 | 20.411 |
| descent_stop, descent_stop_post (pad r 200 to 215 at 150, w 30) | corner (-158.21, 125.98): 32.23 / 1.4142 | 22.79 | 22.786 |
| frame_upper_a, _b | corner (196.31, 147.98): 48.33 / 1.4142 | 34.18 | 34.174 |
| screws a, b (r 4) | 41.411 - 4 | 37.41 | 37.411 |
| guide_tie_a, _b | corner (205.13, 97.15): 107.98 / 1.4142 | 76.35 | 76.354 |
| guide_member, _b (r 10 at 0, 180) | 230 sin 45 - 10 | 152.63 | 152.635 |
| anchor_c, guide_c (r 21 at 270) | apex at the origin: 160 - 21 | 139.00 | 139.0 |
| liftmotor_c | 160 - 29.698 | 130.30 | 130.302 |
| screw_c | 160 - 4 | 156.00 | 156.0 |
| bracket arms c | r_in 181 | 181.00 | 181.0 |
| frame_upper_c | r_in 244 | 244.00 | 244.0 |

S2-5b (premise): 8 ring parts enter the sector (ring, bearing, gear, gear_hub, motor_mount_c, pinion_c, motor23_c, motor_shaft_c). The nut housings at 30 and 150 stay out: 41.411 - 25 = 16.41. Least margin: bearing bottom = ring_top - bearing.height = (959.84 + 130 + 12) - 25 = 1076.84 z_A, and 1076.84 - 940 = **136.84**. JSON 136.84.

### Plan K6 centres (5 rows)

| Row | Spec centre DERIVED | Drawn mid-extent (JSON place x, y) |
|---|---|---|
| frame_upper_b | 274 (cos 30, sin 30) = (237.29, 137.00) | x 196.31 to 278.27 mid 237.29; y 96.02 to 177.98 mid 137.00 |
| motor23_c | r_c (142 + 218) / 2 = 180 at 90: (0, 180) | x +-28.5; y 142 to 218 mid 180 |
| descent_stop | r_c 207.5 at 150: (-179.70, 103.75) | x -201.20 to -158.21 mid -179.70; y 74.02 to 133.48 mid 103.75 |
| guide_member | (230, 0) | x 220 to 240; y -10 to 10 |
| nut_c | (0, -160) | x +-21; y -181 to -139 |
JSON K6: 69 centres within 0.00. Agrees.

### Members against the plate edge

The member square (60, one face toward the axis) at theta 30 projects to x and y half-extents of 30 (cos 30 + sin 30) = 40.98.

| Quantity | Hand | JSON / reported |
|---|---|---|
| members a, b x extent | 237.29 +- 40.98 = 196.31 to 278.27 | 196.31 to 278.27 |
| to plate x edge 322 | 322 - 278.27 = **43.73** | 43.73 |
| members a, b y extent | 137.00 +- 40.98 = 96.02 to 177.98 | 96.02 to 177.98 |
| to plate y edge 304 | 304 - 177.98 = 126.02 | 126.02 |
| member c outer face | 274 + 30 = 304 = rail outer edge, **0.00** | 0.00 |
| member c in the notch (x +-35, inner edge y -239) | 35 - 30 = 5.00; -239 - (-244) = 5.00 | S2-6 pass, notch_clear 5 |
| ring rim to member inner face | 244 - 210 = 34.00 | 34.000 (K7 ring\|frame_upper G) |
| ring rim to rod | 230 - 10 - 210 = 10.00 | 10.000 (g_min 10, +0.000) |
| member b foot over the end member (x 202 to 262) | turned square, 3256.89 of 3600 mm2 (90.5 %) | not reported (NOTE LF1.2-7) |

### Guide tie geometry (Designer 1.2 (b) FIX 1)

The axis is u = unit((237.29, 137.00) - (230, 0)) = (0.05314, 0.99859). The near corner K of member b is (226.31, 96.02), at station (K - rod) . u = -0.196 + 95.885 = 95.69 and length 30 + 95.69 = 125.69. K lies 8.79 to the clockwise side of the tie centreline, on the end edge. Both member edges leaving K have positive u-components, 0.545 and 0.838. The member touches the tie at K only: plan distance 0.000, overlap 0.000 (JSON plan-contact). The tie rests on bracket_guide_b over a triangle with vertices (205.13, 97.15), K, and (204.40, 83.37), area **146.37** mm2 by hand. JSON z-contact overlap 146.367. Corners (198.45, -28.36), (258.36, -31.55), (265.04, 93.96), (205.13, 97.15) match the spec comment.

### Pinion toe to gear hub

pinion r_in = r_toe - (pitch_diameter / tooth_count) sin(pitch_angle) = 96.54 - 4.1665 x 0.31623 = **95.22**. Hub OD r = gear.bore / 2 = 90.00, so the plan gap is **5.22**. z: pinion 1168.22 to 1259.46 z_S and hub 1242.07 to 1275.84 z_S overlap over 17.39 (band). JSON `outline_measure` 5.222, undeclared F, passes on no overlap. FIX LF1.2-2.

## 2 Plan K7 (LF-8): rule against my plan form, premise checks

| Element of my plan form | As implemented (`sketch_common._k7_plan`, `_plan_judge`, `plan_outline`, `outline_measure`) | Premise check, Z / B |
|---|---|---|
| True XY outlines: annulus for section rows, footprint polygon, plan_poly pieces | `plan_outline` as signed at (c) | K7-Z14, B27 (annulus); K7-B21 (plan_poly) |
| Containment: every drawn point inside its outline | K8 plan_extent / projected_extent, x and y | K8-Z6; K8-B17, B20, B25, B26, B28 |
| Centre held | K6 plan centre | K6 Z4; K6 B (10/10 fired) |
| z bands from the spec per stack pose (the plan carries no z) | `zb` reads check_stack z_min, z_max per pose | K7-B24 (C z-separated), K7-B25 (interference by z) |
| C passes only on true sections | `true` flag; circumscribing outlines refused | K7-B26 |
| One figure for four poses | outline pose-invariance lint | K7-B28 |
| Swept: moving outline against fixed rows over the sweep band; pose-restricted pairs as F | LF-c1 | K7-Z15; K7-B29, B30 |
| G and F on lower bounds (box gap, circumscribed footprint) | sound: every lower bound clears or fails conservatively | K7-B11, B23 |

The rule as implemented matches the form I signed at (c). Every premise has a Z and a B in the manifest, and 191/191 matched at P6 (MEASURED by the Engineer, `wip/fixtures/controls_results.json`). **LF-8 plan K7: SIGNED** on r1. FIX LF1.2-1 changes only what the record holds, not the rule.

## 3 Pairs passed as z-separated

Counts (live re-run, MEASURED): declared F/G pairs settled by z bands: 386 pair-class entries over the four poses. Undeclared pairs z-separated: 61 pairs with plan overlap, plus the rest with no plan overlap. Swept z-separated: listed below where the plan outlines overlap. The z separation matters only where the plan outlines overlap or sit within g_min. Every such pair is listed here, with its hand value.

| Pair (pose) | z gap JSON | Hand | Real? |
|---|---|---|---|
| ring \| anchor_*, bracket_anchor_* (swept to capture_end) | 19.84 | ring underside 374.84 z_S - arm/block top 355 = 19.84 | real |
| ring \| guide_*, bracket_guide_* (load, park) | 33.16 | block bottom 1195 - ring top 1161.84 | real |
| ring \| descent_stop_post (swept) | 12.00 | pad 12 between ring and post (ring lands on the pad, C at capture_end) | real |
| ring \| liftmotor_* (swept) | 74.84 | 374.84 - 300 | real |
| ring, guide_lug_* \| guide_tie_* (load, park) | 63.16 | tie bottom 1225 - ring top 1161.84 | real |
| guide_bushing_* \| guide_tie_* | 75.16 | 1225 - 1149.84 | real |
| nut_housing_* \| anchor_*, bracket_anchor_* (capture_end, swept) | 10.84 | housing bottom 365.84 - 355 (g_min 10, +0.84; S1 identity) | real |
| nut_housing_* \| guide_*, bracket_guide_* (load, park) | 24.16 | 1195 - 1170.84 | real |
| nut_* \| guide_*, anchor_*, liftmotor_* (undeclared) | 24.16, 10.84, 65.84 | as above; nut equals housing band | real |
| screw_* \| liftmotor_* (undeclared) | 25.00 | coupling: screw bottom 325 - motor top 300 | real |
| anchor_* \| liftmotor_*, bracket_anchor_* \| liftmotor_* | 25.00 | 325 - 300 | real |
| bracket_anchor_a \| descent_stop | 7.84 | post height 362.84 - 355 between them | real |
| ring \| pinion_* (undeclared) | 6.38 | axis 52 - OD / 2 45.62 above the ring top | real |
| bearing \| pinion_* | 6.38 | bearing top flush with the ring top | real |
| ring \| motor23_* | 23.50 | motor_mount_height | real |
| ring, bearing \| gear, gear_hub | 80.23 | 52 + 28.23 | real |
| gear \| motor_shaft_* | 24.23 | gear bottom 1242.07 - shaft top 1217.84 | real |
| bearing \| drill_head | 10.63 | N1: ring underside 130 above the tip - bearing hang 13 - head length 106.37 = 10.63 | real |
| gear_hub \| drill_head | 115.86 | 1242.07 - 1126.21 | real |
| base_frame \| guide_member_b, drill_head, guide_tie_* | 12.00 and more | plate between | real |
| descent_stop \| ring (load, start, park; C declared at capture_end) | 775, 650 | ring above the pad except at capture_end | real |
| gear \| liftmotor_* | 942.07 | plan 3.98 is the circumscribed bound (160 - 29.70 - 126.32); drawn square face at r 139: 139 - 126.32 = 12.68 | real |
| keepout \| guide_*, bracket_guide_* (capture_end) | 0.16 | keep-out top = top-block top 1194.84 vs 1195 | real; plan 52.79 and 94.80 settle it anyway |

None of these passes is false. Each z band comes from check_stack, and each gap reproduces by hand.

## 4 Reported values (arithmetic only)

| Reported | Hand | Agrees |
|---|---|---|
| extents x +-322, y +-304 | plate and frame | yes |
| parts above the plate: x +-278.27, y -304 to 218 | members a, b; motor23_c r_out 218; member c face 304 | yes |
| sector y to 400, 96 past 304; x +-282.84 | 400 sin 45 = 282.84 | yes |
| cutter overhang 2.70 | 177.8 / 2 - 86.20 | yes |
| lever 304 | min(644, 608) / 2 | yes (tip forces from the mass report, equal to r4; not recomputed) |
| F6 to axis 492.46 | 244.84 + 130 x 400 / 210 = 244.84 + 247.62 | yes |
| F6 to cutter rim 578.80 | 244.84 + 130 x 311.10 / 121.10 = 244.84 + 333.96 | yes |
| strike list z_S | bearing 1161.84 - 25 = 1136.84; ring 1149.84; mount 1161.84; pinion 1161.84 + 52 - 45.62 = 1168.22; motor 1161.84 + 52 - 28.5 = 1185.34; shaft 1213.84 - 4 = 1209.84; gear 1213.84 + 28.23 = 1242.07 | yes |
| drill tip over hand band 19.84 | 959.84 - 940 | yes |
| lift motors to sector edge 11.71 "MEASURED" | circumscribed-circle bound; drawn square 15.69 | value right, label wrong (NOTE LF1.2-4) |
| highest point capture_end 1600.00 z_S | eye end of sightline_f6, a reference line; highest part 1285.00 (member and tie tops) | wrong part (NOTE LF1.2-5) |
| highest point load, park 1969.84 | keep-out z_max = top-block top 959.84 + 60 + 800 + 150 | yes |

## 5 S1 r5, changed rows only (frame_upper.radius 300 to 274; arms; ties; housings)

| Quantity | r4 | r5 hand | r5 JSON / record |
|---|---|---|---|
| frame_upper_a x | -300.79 to -218.83 | -237.29 +- 40.98 = -278.27 to -196.31 | -278.27 to -196.31 |
| bracket arms a x (r 181 to 244 at 150, w 30) | -248.83 to -141.75 | r 181: -156.75 +- 15 = -171.75, -141.75; r 244: -211.31 +- 15 = -226.31, -196.31 | -226.31 to -141.75 |
| arm r_out = member inner face | 270 | 274 - 30 = 244 | 244 |
| ring \| frame_upper G (plan) | 60.00 | 244 - 210 = **34.00** | 33.944 (ring 128-gon bound) |
| nut_housing_a \| frame_upper_a (XZ) | 55.27 | -196.31 - (-163.56) = 32.75 | 32.746 |
| nut_housing_a \| frame_upper_a (plan, true) | n/a | 244 - 160 - 25 = 59.00 | not recorded (box bound 32.746 in S2) |
| swept ring \| bracket_anchor_* (z) | 19.84 | 374.84 - 355 | 19.84 |
| swept nut_housing \| bracket_anchor_* (z) | 10.84 | 365.84 - 355 | 10.84 (+0.84) |
| nut_housing \| bracket_guide_* (z, park) | 24.16 | 1195 - 1170.84 | 24.16 |
| descent_stop pad r 200 to 215 on arm r 181 to 244 | inside | 181 < 200, 215 < 244; widths 30 = 30 | post\|arm C, post\|pad C |
| guide_tie \| frame_upper (plan-contact at K) | not drawn | 0.00 at (226.31, 96.02) | 0.000 / 0.000 |
| guide_tie \| bracket_guide (z-contact 1225 z_S) | not drawn | 1165 + 60 = 1225 | C, 0.000 |
| guide_bushing z at load | not drawn | ring_bottom 1149.84 - 30 = 1119.84 to 1149.84 | 1119.84 to 1149.84 |
| bushing \| lug C | not drawn | z touch at 1149.84; plan pi 20^2 = 1256.64 (128-gon 1256.89) | C |
| bushing \| liftmotor depth band | not drawn | 80 - 29.70 - 20 = 30.30 | 30.302 |
| bushing \| anchor, guide depth band | not drawn | 80 - 21 - 20 = 39.00 | 39.000 |
| bushing, lug \| frame_upper depth band | not drawn | 96.02 - 20 = 76.02 | 76.019 |
| lug \| arms depth band | n/a | 64.52 - 20 = 44.52 | 44.519 |

Unchanged checks reproduce r4: S1-1 650.00, S1-2 125.00, S1-3 367.34 / 117.34, S1-4 0.84, S1-5a 192.34, S1-5b 142.00, S1-7 607.66 (MEASURED, record diff r4 against r5). Keys: frame_upper.radius 300 to 274 changed. New keys: guide.bushing_drop, bushing_housing_od, bushing_length, bushing_od, bushing_type, top_support. None dropped.

## 6 Findings

**FIX LF1.2-1 (record; carried 1.2 (c) NOTE 3, deadline S2 r2).** The K7 record holds states only. P9 adds per-test entries to `sN_checks_r<k>.json` K7: pose, pair, class, state, z gap, plan or XZ distance, overlap, and the basis of the distance (exact, box bound, circumscribed outline, depth disk). With that, r1 to r2 names the pairs that moved, and a bound can never be read as a distance. Z: live S2 record carries 1280 entries with ids. B: drop the ids from one entry and a record lint fires. Apply the same change to the S1 r5 record before S1 r6.

**FIX LF1.2-2 (spec declaration; Designer rules, Engineer applies).** pinion_a, _b, _c | gear_hub is undeclared F. Plan gap 95.22 - 90.00 = **5.22** with z overlap 17.39 (band). The two parts turn on different bodies: the hub with the drill, the pinion on its radial shaft. No class states the intended clearance, and the Engineer's tight-spot list does not show it. The Designer declares the pair, G with a ruled g_min. At g_min 10 the pair fails on r1, and the toe, `pinion.r_toe`, `gear.bore` or the hub OD must move. At g_min 5 or less it passes. The Engineer adds "pinion toe to gear hub 5.22" to the reported tight spots in `s2_summary_r<k>.md` and the spec `reported` list.

**NOTE LF1.2-3 (zero-measure C contacts).** The plan C rule passes these contacts, which have no length or area:
- guide_lug_* | ring: the chord at r 210 touches the rim circle at (210, 0) only. The corners sit at sqrt(210^2 + 20^2) = 210.95, so they are 0.95 clear.
- guide_bushing_* | ring: housing tangent at r 210, z-contact overlap 0.000. The spec source text "top on the ring underside" is false in plan: the housing top lies on the lug underside (bushing|lug overlap 1256.89).
- bracket_anchor/guide_* | anchor/guide_*: the arm end chord at r 181 is tangent to the r 21 block.
- guide_tie_* | frame_upper_*: corner K.

The tie's real seat is the 146.37 mm2 triangle on the arm. Each is a correct geometric fact at sketch level, and Step 2 and S3 dimension the joints (LF1.1-9 to -11). The Designer may want to correct the source text on ring|guide_bushing_*. FIX LF1.2-1's record can carry the contact area or length so M1 sees which joints are points.

**NOTE LF1.2-4 (labels).** Reported "lift motors to sector edge 11.71 MEASURED" is the circumscribed bound. The drawn square sits 15.69 from the edge. Tag the value "bound (circumscribed outline)", or report both.

**NOTE LF1.2-5 (highest point).** The capture_end highest point 1600.00 z_S is the eye end of sightline_f6. The highest drawn part is 1285.00 z_S (member and tie tops). This agrees with the Engineer's open item 3. Excluding kind line from the highest-point report also covers any future reference line.

**NOTE LF1.2-6 (construction identities).** S2-3 holds by the definition of `pinion.r_heel` (= gear.pitch_diameter / 2), so it can fail only through the drawing. That puts it in the SW-10 class; it stays. S2-2 reads the nut flange r 21. The ring nut housing r 25 on the same centre leaves 48.80 to the keep-out, which also clears 10.

**NOTE LF1.2-7 (member feet).** Members a, b, turned with one face to the axis, bear 3256.89 of 3600 mm2 (90.5 %) over the end member x 202 to 262. The rest bears on the 12 plate alone. Report only, for Step 2 (R1 bolt-down row).

## Verdicts

S2 r1: **CROSS-REVIEW PASS** (every S2 check and the K6 and K7 samples reproduce by hand against the signed spec; FIX LF1.2-1 and LF1.2-2 go into P9).
S1 r5 (changed rows): **CROSS-REVIEW PASS**.
LF-8 plan K7: **SIGNED** on its premise (containment, true sections for C, z bands from the spec, one-figure lint, swept form; each with Z and B).
Counts: BLOCK 0, FIX 2, NOTE 5.

## Gameplan lines to change

**l.141** (K table, K7 row, end of the plan clause).

Old:
```
whose z band meets the sweep band |
```
New:
```
whose z band meets the sweep band; the checks record lists every K7 test by pose and pair with class, state, z gap, distance, overlap and the distance basis (exact, box bound, circumscribed outline, depth disk) (Loftsman 1.2 (e) LF1.2-1) |
```

**l.261** (detail 1.2, Reported).

Old:
```
Reported: outline extents against the current 644 x 608 footprint (open, not asserted); footprint against the S1 unbolted tip force (bolt-down or footprint goes to the Step 2 row, R1).
```
New:
```
Reported: outline extents against the current 644 x 608 footprint (open, not asserted); footprint against the S1 unbolted tip force (bolt-down or footprint goes to the Step 2 row, R1); tight spots with their basis (ring rim to rod 10.00, ring rim to member 34.00, lift motors to the sector edge 11.71 circumscribed / 15.69 drawn square, pinion toe to gear hub 5.22; Loftsman 1.2 (e) LF1.2-2, -4); highest point over parts only (reference lines excluded, LF1.2-5).
```

**l.262** (detail 1.2, Cross-review).

Old:
```
Cross-review: The Loftsman (azimuths, radii), The Topologist (handedness: +X along slot line C, theta counter-clockwise from +X seen from +Z per ASSEMBLY.md; K8 B3).
```
New:
```
Cross-review: The Loftsman (azimuths, radii; 1.2 (e) S2 r1 and S1 r5 PASS, LF-8 plan K7 signed, `step1.2_loftsman_crossreview.md`), The Topologist (handedness: +X along slot line C, theta counter-clockwise from +X seen from +Z per ASSEMBLY.md; K8 B3).
```

**l.491** (Progress Log, add a row after it).

Old:
```
| 1.2 | 2026-11-25 | (d) P6 (`step1.2_engineer_draw_r1.md`): `s2_plan.py` written; `wip/s2_plan_r1.png` first written 17:57:05; S2 r1 17/17 on run 1; S1 r5 18/18 (four poses, mass report equal to r4); members a, b 43.73 from the plate x edge, member c on the rail edge 0.00; cutter overhang 2.70; controls 191/191 (284 s); --stale red on s1 r4 frame_upper.radius only. Open: gear ticks, F6 label "z_S z_S", sightline in the highest-point report, s2 status text. Next: STOP-T5, (e) and M1 in parallel. |
```
New:
```
| 1.2 | 2026-11-25 | (d) P6 (`step1.2_engineer_draw_r1.md`): `s2_plan.py` written; `wip/s2_plan_r1.png` first written 17:57:05; S2 r1 17/17 on run 1; S1 r5 18/18 (four poses, mass report equal to r4); members a, b 43.73 from the plate x edge, member c on the rail edge 0.00; cutter overhang 2.70; controls 191/191 (284 s); --stale red on s1 r4 frame_upper.radius only. Open: gear ticks, F6 label "z_S z_S", sightline in the highest-point report, s2 status text. Next: STOP-T5, (e) and M1 in parallel. |
| 1.2 | 2026-11-25 | (e) P7a Loftsman (`step1.2_loftsman_crossreview.md`): S2 r1 CROSS-REVIEW PASS, S1 r5 changed rows PASS, LF-8 plan K7 SIGNED; BLOCK 0, FIX 2 (LF1.2-1 K7 record pair ids and distance basis before S2 r2; LF1.2-2 pinion\|gear_hub undeclared, toe gap 5.22, Designer rules the class), NOTE 5 (zero-measure C contacts, bound labels, highest point 1285.00 at capture_end, S2-3 identity, member feet 90.5 % on the end member). |
```

## Re-check r2 (S2 r2, S1 r6; `step1.2_engineer_revision_r2.md`)

Corrections to the brief: none. Records read: `wip/s2_checks_r2.json`, `wip/s1_checks_r6.json` (MEASURED 2026-11-25). Hand values DERIVED as in sections 1 and 5.

### LF1.2-1 K7 record: CLOSED

| Item | S2 r2 | S1 r6 |
|---|---|---|
| `test_fields` | [pose, pair, class, state, z_gap, distance, overlap, basis] | same |
| entries / states | 7334 / 7334 | 5556 / 5556 |
| malformed entries (wrong length, empty pose, pair, class or state) | 0 | 0 |
| state per entry equal to `states` | yes | yes |
| bases | z band 4059, box bound 1848, exact 778, circumscribed outline 477, declared N 172 | XZ projection (exact) 3428, depth band 1578, depth band (swept hull) 156, declared N 141, XZ (swept hull) 140, plan footprint (spec placement) 107, plan footprint (swept hull) 6 |

Spot checks, record value against hand value:

| Entry | Record | Hand | Basis right? |
|---|---|---|---|
| S2 load nut_housing_a\|frame_upper_a G | 32.746 | true 58.99 (244 - 160 - 25) | yes: box bound |
| S2 load motor23_a\|guide_tie_b G | 14.766 | true 46.16 | yes: box bound |
| S2 load ring\|frame_upper_a G | 34.000 | 244 - 210 = 34.00 | yes: exact |
| S2 load guide_tie_a\|bracket_guide_b C | overlap 146.367 | 146.37 triangle | yes: exact |
| S2 load ring\|guide_lug_a C | 0.000 / 0.000 | point (210, 0) | yes: exact |
| S2 load gear_hub\|pinion_a G | z -17.39, 5.222 | 95.22 - 90.00 = 5.22; band overlap 1259.46 - 1242.07 = 17.39 | yes: circumscribed outline (the toe chord midpoint lies on the drawn edge, so bound = drawn gap) |
| S2 load ring\|liftmotor_a G | z-separated 849.84 | 1149.84 - 300 | yes: z band |
| S1 load nut_housing_a\|frame_upper_a G | 32.746 | -196.31 + 163.56 = 32.75 | yes: XZ exact |
| S1 load ring\|frame_upper_a G | 33.944 | 34.00 true | basis reads "plan footprint (spec placement)": correct source, but the value is a 128-gon bound (NOTE R2-2) |

Record lint `k7_record_issues`: it checks the field list, the count, the 8-field shape, non-empty pose, pair, class, state and basis, the pair form a|b, and state equality. It runs in `check_sketch.run_sketch` and fails K7. Z: K7-Z16 (S2), K7-Z17 (S1). B: K7-B32 (pair dropped from entry 0, reason "entry 0 lacks ['pair']"). The lint holds what LF1.2-1 asked. **Record lint: SIGNED (Loftsman).**

### LF1.2-2 pinion|gear_hub: CLOSED

`s2_spec.yaml` l.996-998 declares pinion_a, _b, _c on gear_hub as G, g_min 3, ASSUMED, with the Designer's source (toe runout; Step 2 hub clamp heads below r 90). The record shows 5.222 against 3: +2.22 at four poses x three pinions. K7-B33 (g_min 6) fires 12 short as planted. The spec `reported` list (l.91) and `wip/s2_summary_r2.md` l.81 report "pinion toe to gear hub 5.22" with its basis. **G 3 declaration: SIGNED (Loftsman)** on the geometry: 5.22 by hand. g_min 3 is the Designer's value.

### Ruling: tick toe radius

The ticks stand for the gear's teeth, so both ends should lie on the gear. With the heel end at the pitch radius 125.00 (`gear.pitch_diameter / 2`), the toe end on the same pitch cone is the toe pitch point, `pinion.r_toe` = 125 - 30 sin 71.565 = 125 - 28.46 = **96.54** (DERIVED; the key value). 95.22 = r_toe - m sin(pinion pitch angle) is the pinion's toe-tip radius, a point on the pinion, not on the gear. A tick from 95.22 to 125 mixes a pinion tip with a gear pitch point, and no gear generator has that pair of ends. The geometrically right tick is **96.54 to 125.00**: `ticks_radial r_in: pinion.r_toe`, as the Designer's rule names the key. The "r 95.2" in the rule text and the gear shape text is the wrong number. The 1.32 mm difference is not visible at plot scale, and no check verdict moves.

FIX R2-1 (spec only; no other geometry): `s2_spec.yaml` l.978 `ticks_radial` r_in becomes `pinion.r_toe`, and its source text "toe pitch point r 96.54". l.958 shape text "toe r 95.2" becomes "toe r 96.54". `s2_plan.py` reads the same predicate value. Re-run `s2 --rev 3` (or fold into the Designer re-sign revision). K8-B29 to B31 stand as written.

### NOTES

- R2-1 (S1/S2 class agreement). S1 r6 records `gear_hub|pinion_a` as undeclared F, 5.198 (plan footprint). S2 declares the same physical pair G 3. Declare it G 3 in `s1_spec.yaml` before `--accept s1 --rev 6`. It passes: 5.198 > 3. X1 compares place, z_rule and plan_poly only, so it does not see neighbour classes.
- R2-2 (basis wording). A round placed footprint in S1 (ring 128-gon) is tagged "plan footprint (spec placement)" with no word that it is a circumscribed bound: 33.944 against a true 34.00. Tag it "plan footprint (circumscribed 128-gon)" when `footprint: round` or a depth disk is used. In z-separated entries the `distance` field repeats the z gap (S2 ring|liftmotor 849.84 / 849.84). Write `null` there, or the plan distance; the basis already says z band. Neither is blocking.

### Verdict r2

LF1.2-1: **PASS** (closed). LF1.2-2: **PASS** (closed). Record lint and G 3 declaration: **SIGNED**. Tick toe radius: **96.54** (`pinion.r_toe`); FIX R2-1, spec-only. Counts r2: BLOCK 0, FIX 1, NOTE 2.

### Gameplan lines to change (re-check r2)

**Progress Log** (add a row after the (h) P9 row; the orchestrator places it after the P9 row once that row is applied).

Old:
```
| 1.2 | 2026-11-25 | (h) P9 (`step1.2_engineer_revision_r2.md`):
```
New:
```
| 1.2 | 2026-11-25 | P7r Loftsman re-check r2 (`step1.2_loftsman_crossreview.md`, Re-check r2): LF1.2-1 closed (S2 7334, S1 5556 entries, record lint SIGNED), LF1.2-2 closed (pinion\|gear_hub G 3 SIGNED, 5.22); tick toe ruled 96.54 = pinion.r_toe (pitch cone, toe to heel 125), FIX R2-1 spec-only; NOTE: declare S1 gear_hub\|pinion G 3 before --accept s1 r6. |
| 1.2 | 2026-11-25 | (h) P9 (`step1.2_engineer_revision_r2.md`):
```
(The new row goes after the P9 row; the anchor is the P9 row's first cells. If the orchestrator applies rows in order, append it after that row.)

**l.141** (K7 row, the clause added at (e)).

Old:
```
(exact, box bound, circumscribed outline, depth disk) (Loftsman 1.2 (e) LF1.2-1) |
```
New:
```
(exact, box bound, circumscribed outline, depth disk) (Loftsman 1.2 (e) LF1.2-1; record lint k7_record_issues, K7-Z16, Z17, B32, signed at re-check r2) |
```
