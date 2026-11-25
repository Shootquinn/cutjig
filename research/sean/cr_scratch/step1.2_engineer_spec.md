## Corrections to the brief

1. **The guide tie as specified hits the top-guide bracket arm.** Designer 1.2 (a) row 21 puts the tie at the rod top (z_A 1212). A 30-6060 tie under the rod top spans 1152 to 1212 z_A. The guide arm at theta 30 (and 150) spans 1135 to 1165 z_A. In plan the tie strip (rod centre to member centre, half-width 30) overlaps the arm by 492.21 mm² (MEASURED, check_stack plan pieces). In z the two overlap by 13. guide_tie_a|bracket_guide_b and guide_tie_b|bracket_guide_a interfere. The spec carries the tie as written (z 1152 to 1212) and declares no relief. One option needs no key change: tie on the guide-arm top, z 1165 to 1225 (top flush with the member top), with the rod top 1212 clamped inside the tie. That is a design value, so it goes to the Designer at P3a (open item 1). DERIVED.
2. Designer section 4 gives the rod at theta 0 as "14 in x from the stop-pin pocket wall". 14 is measured from the rod centre (244 - 230). The rod surface is **4.00** from the wall (MEASURED, plan). The two are z-separated: the pocket is on the underside (z_A 0 to 4) and the rod starts at 12.
3. S2-5a Z in the Designer's file lists "housings 16.41". The nut housings are ring-mounted, so his own S2-5a rule does not cover them, and they lie outside the sector anyway. Least gaps to the fixed parts the rule names (MEASURED, 256-gon circumscribing wedge): lift motors 11.71, bracket arms 17.87, anchor and guide blocks 20.41, pad and post 22.79. Half-angle 49 gives 0.82 (Designer 0.84). The difference is the arc polygon; both read F.
4. Member c outer face R + 30 = 304.00 equals the plate edge and the rail outer face: margin **0.00** by identity (DERIVED). S2-6 tests containment in the rail strip, which holds exactly (3600.00 of 3600.00 mm², MEASURED).
5. The Designer's g_min table puts the guide rods in the moving-vs-fixed G 10 list. ring|guide_member then reads 10.00 = guide.radius - rod_od / 2 - ring.od / 2, a zero-margin identity (in S1 the pair is undeclared F). Spec follows the table; reported under tight spots.
6. S1 K7 state labels move at radius 274: G 16 to 0 and swept:G 4 to 0, F 266 to 282, swept:F 43 to 47, undeclared depth-separated 858 to 802, undeclared plan-separated 41 to 49 (MEASURED, r4 record against the r5 preview). The members' depth band moved 13 toward the axis (109.02..190.98 to 96.02..177.98), so pairs that passed as G on a band gap below g_min now overlap in depth and pass on the XZ distance (label F). Every pair passes.
7. The brief's projection rule (radial-axis parts as rectangles or trapezoids) meets K5 as written: `classify` reads a 4-vertex Polygon that is not axis-aligned as "trapezoid". Every radial rectangle at an oblique azimuth would fail K5 until TP-13 lands at (c): members a and b, arms at 30/150, pad and post, mounts, motors and shafts at 210/330, ties. Not a spec defect; recorded for (c).
8. K8 `outboard` and `side` read x cos(theta). At theta 90 that reads 0, and the predicate fails for motor23_c. The S2 rows carry `outboard ... frame: radial` (radial distance of centroids) for (c) to implement. The S1 `below`/`above` predicates read centroid z, which is y in plan; S2 rows do not carry them.

## 1 Files changed

All under `docs/sketches/`. CRLF kept.

| Path | What |
|---|---|
| `proposed_params.yaml` | `frame_upper.radius` 300 to 274 (source Sean STOP S2-A, Design Notes 27); new `frame_upper.member_length_rail` 1225 (DERIVED), `.foot`, `.orientation`, `.stop_pad_count` 1 (ASSUMED, Sean's one-pad ruling); `pinion.angle` and `guide.angle` source text (values unchanged); new `guide.bushing_type`, `.bushing_od` 32, `.bushing_length` 42, `.bushing_housing_od` 40 (DERIVED), `.bushing_drop` 30 (DERIVED), `.top_support`; `liftmotor.position` text (H4), new `liftmotor.plan_rot` 0; new namespace `operator` (sector_theta 90, sector_half_angle 45, sector_radius 400, hand_band [440, 940], watch_r 400, watch_theta 60, eye_height 1540), all ASSUMED. 103 to 121 overlay leaves; K2 clean, no shadow (`operator` is not a params.yaml namespace) |
| `s2_spec.yaml` | new, 70 rows, status "draft for signature" (sections 2, 3, 6) |
| `checks_s2.py` | new skeleton S2-1 to S2-6 from the spec block `s2_checks`; reads drawn patches by gid in the plan figure, fails closed (absent) on an undrawn part; S2-3 fails closed (content): no drawn pitch point yet |
| `check_stack.py` | `strip_corners`, `plan_poly_pieces`, `sector_record`; `evaluate_spec` evaluates the new optional row fields `plan_poly` (convex pieces from [x, y] expressions, or a strip) and `sector` into `plan_pieces`, `plan_x`, `plan_y`, `sector`. No S1 row carries either field; S1 results unchanged (section 5) |
| `s1_spec.yaml` | r5 text only: header comment block (r5 trigger, S2-only parts); member comments "r 244 to 304"; four bracket-arm shape strings and four arm source strings "r 270" to "r 244"; arm comments "= 244". No key, expression, class or row change. The shape-string edits are outside "comments and source strings"; the Loftsman rules them at P3b (open item 7) |

Not changed: params.yaml, the gameplan, `s1_side_poses.py`, `sketch_common.py`, `check_sketch.py`, fixtures.

## 2 Part list (detail 1 common (b))

Every part a `shape` string in `s2_spec.yaml` names, with its row or `not_drawn` entry. The same list is in the spec (`part_list`, `not_drawn`).

| Part named in a shape string | Row |
|---|---|
| base plate | base_plate |
| receiver spigot hole | base_spigot_hole |
| column notches (2), plate notch outline round member c | base_plate (boundary between its five plan_poly pieces) |
| slotted fastener holes | base_slots |
| key pockets, pin pocket | base_key_pockets, base_pin_pocket |
| base frame rails, end members, plate supports; end member under members a, b; rail top under member c | base_frame |
| slot line C; other rail slot lines | slot_line_c; slot_lines |
| screw frame members a, b, c | frame_upper_a, frame_upper_b, frame_upper_c |
| T8 screws; nut flanges; nut-housing bosses | screw_a/_b/_c; nut_a/_b/_c; nut_housing_a/_b/_c |
| anchor and top-guide bracket arms | bracket_anchor_a/_b/_c, bracket_guide_a/_b/_c |
| anchor and top-guide blocks (block circle r 21) | anchor_a/_b/_c, guide_a/_b/_c |
| descent-stop pad (one); post; anchor arm under the pad | descent_stop; descent_stop_post; bracket_anchor_a |
| NEMA 17 lift motors | liftmotor_a/_b/_c |
| ring plate with clearance bore | ring |
| NEMA 23 mount blocks | motor_mount_a/_b/_c |
| guide lugs; LM20UU bushing housings | guide_lug_a/_b; guide_bushing_a/_b |
| bearing; gear with tooth ticks; gear clamp hub | bearing; gear; gear_hub |
| bevel pinions with hubs; pinion axes | pinion_a/_b/_c; pinion_axis_a/_b/_c |
| NEMA 23 motors; NEMA 23 shafts | motor23_a/_b/_c; motor_shaft_a/_b/_c |
| guide rods; rod top ties | guide_member, guide_member_b; guide_tie_a/_b |
| drill tube; keep-out circle; cutter rim circle | drill_tube; keepout; drill_head |
| datum B cross, +X/+Y arrows, theta arrow | collet_axis (drawing signifiers in one row) |
| operator loading sector; F6 sightline and observer point | operator_sector; sightline_f6 |
| wing nut, collet, holder | not_drawn: below the drill path, drawn in S1 (Designer section 8) |
| power-off hold device | not_drawn: Step 2 decides (N7, T2-c) |
| descent-stop pads at jackscrew.angle[0], [2] | not_drawn: declined by Sean (Design Notes 27) |

The drain hole and receiver are not named in any S2 shape string, so they have no entry.

Letter map (S1 ids kept for every shared row): screw set a = theta 150, b = 30, c = 270. Pinion set a = 210, b = 330, c = 90. guide_member = 0, guide_member_b = 180. Tie a runs from rod 0 to member b (30); tie b from rod 180 to member a (150).

## 3 Plan table per part

MEASURED from `check_stack.evaluate_spec` on `s2_spec.yaml` with the edited overlay. z_S per pose: load / start / capture_end / park. Plan extents are footprint extents in mm.

| Row | r_c | theta | x, y | plan x | plan y | z_S load | start | capture_end | park |
|---|---|---|---|---|---|---|---|---|---|
| base_plate (5 pieces) | | | | -322..322 | -304..304 | 60..72 | same | same | same |
| base_frame (6 pieces) | | | | -322..322 | -304..304 | 0..60 | same | same | same |
| base_spigot_hole | 0 | | 0, 0 | -80.20..80.20 | -80.20..80.20 | 60..72 | | | |
| base_slots / key / pin pockets | | | | -265..265 / -166..166 / 244..254 | -292.5..292.5 / 253..265 / -7..7 | 60..72 / 60..64 / 60..64 | | | |
| frame_upper_a | 274 | 150 | -237.29, 137.00 | -278.27..-196.31 | 96.02..177.98 | 72..1285 | same | same | same |
| frame_upper_b | 274 | 30 | 237.29, 137.00 | 196.31..278.27 | 96.02..177.98 | 72..1285 | same | same | same |
| frame_upper_c | 274 | 270 | 0, -274 | -30..30 | -304..-244 | 60..1285 | same | same | same |
| screw_a/_b/_c | 160 | 150/30/270 | (-138.56, 80)/(138.56, 80)/(0, -160) | ±4 about x | ±4 about y | 325..1225 | same | same | same |
| nut_x, nut_housing_x | 160 | as screw | as screw | r 21 / r 25 | | 1140.84..1170.84 | 1015.84..1045.84 | 365.84..395.84 | 1140.84..1170.84 |
| anchor_x / guide_x | 160 | as screw | as screw | r 21 | | 325..355 / 1195..1225 | same | same | same |
| bracket_anchor_x / _guide_x | 212.50 | as screw | b: (184.03, 106.25); c: (0, -212.50) | b: 141.75..226.31; c: -30..30 | b: 64.52..147.98; c: -244..-181 | 325..355 / 1195..1225 | same | same | same |
| liftmotor_x | 160 | as screw | as screw | r 29.70 | | 252..300 | same | same | same |
| descent_stop / post | 207.50 | 150 | -179.70, 103.75 | -201.20..-158.21 | 74.02..133.48 | 362.84..374.84 / 355..362.84 | same | same | same |
| ring | 0 | | 0, 0 | ±210 | ±210 | 1149.84..1161.84 | 1024.84..1036.84 | 374.84..386.84 | 1149.84..1161.84 |
| bearing | 0 | | 0, 0 | ±100 | ±100 | 1136.84..1161.84 | 1011.84..1036.84 | 361.84..386.84 | 1136.84..1161.84 |
| gear, gear_hub | 0 | | 0, 0 | ±126.32, ±90 | | 1242.07..1275.84 | 1117.07..1150.84 | 467.07..500.84 | 1242.07..1275.84 |
| motor_mount_a/_b/_c | 176 | 210/330/90 | c: (0, 176) | c: -28.5..28.5 | c: 142..210 | 1161.84..1185.34 | 1036.84..1060.34 | 386.84..410.34 | 1161.84..1185.34 |
| guide_lug_a/_b | 230 | 0/180 | (±230, 0) | 210..250 | -20..20 | 1149.84..1161.84 | 1024.84..1036.84 | 374.84..386.84 | 1149.84..1161.84 |
| guide_bushing_a/_b | 230 | 0/180 | (±230, 0) | 210..250 | -20..20 | 1119.84..1149.84 | 994.84..1024.84 | 344.84..374.84 | 1119.84..1149.84 |
| pinion_a/_b/_c | 117.61 | 210/330/90 | c: (0, 117.61) | c: -45.62..45.62 | c: 95.22..140 | 1168.22..1259.46 | 1043.22..1134.46 | 393.22..484.46 | 1168.22..1259.46 |
| motor23_a/_b/_c | 180 | 210/330/90 | c: (0, 180) | c: -28.5..28.5 | c: 142..218 | 1185.34..1242.34 | 1060.34..1117.34 | 410.34..467.34 | 1185.34..1242.34 |
| motor_shaft_x | 131.50 | as pinion | c: (0, 131.5) | c: ±4 | c: 121..142 | 1209.84..1217.84 | 1084.84..1092.84 | 434.84..442.84 | 1209.84..1217.84 |
| guide_member / _b | 230 | 0/180 | (±230, 0) | 220..240 | -10..10 | 72..1272 | same | same | same |
| guide_tie_a / _b | | | strip | 200.04..267.25 / mirror | -1.59..138.59 | 1212..1272 | same | same | same |
| drill_tube | 0 | | 0, 0 | ±76.20 | | 1126.21..1819.84 | 1001.21..1694.84 | 351.21..1044.84 | 1126.21..1819.84 |
| keepout | 0 | | 0, 0 | ±86.20 | | 100..1969.84 | 100..1844.84 | 100..1194.84 | 100..1969.84 |
| drill_head | 0 | | 0, 0 | ±88.90 | | 1019.84..1126.21 | 894.84..1001.21 | 244.84..351.21 | 1019.84..1126.21 |
| operator_sector | r 400 | 90 ± 45 | | -282.84..282.84 | 0..400 | all z | | | |
| sightline_f6 | line r 0..400 | 60 | | 0..200 | 0..346.41 | 244.84..1600 | same | same | same |

Outline extents, every footprint at every pose (MEASURED): x -322.00..322.00, y -304.00..304.00, the 644 x 608 plate exactly. Reported, not asserted. No part reaches past the plate. Member c's outer face and the base-plate pieces set the y extent.

Spec-level S2 values (MEASURED with `checks_s2.py` on a scratch figure drawn from the spec footprints; not a run of record, no PNG): S2-1 screws 30/150/270, pinions 90/210/330, phase 60 within 0.000; S2-2 52.80; S2-4 fails absent (collet_axis not drawn by the scratch figure); S2-5a 27 fixed parts clear, least 11.71; S2-5b 8 ring parts in the sector, least 136.84; S2-6 three members seated. On the floor-only stub every S2 check fails closed.

S2-5b strike list at load, ring parts entering the sector (DERIVED from the stack): bearing 1076.84 z_A (margin 136.84), ring 1089.84 (149.84), motor_mount_c 1101.84 (161.84), pinion_c 1108.22 (168.22), motor23_c 1125.34 (185.34), motor_shaft_c 1149.84 (209.84), gear and gear_hub 1182.07 (242.07). These match the Designer's section 5.

S2-a keep-out pairs (plan lower bound, 128-gon): lift motors 44.10, blocks 52.78, screws 69.78, arms 94.78, pad and post 113.78, rods 133.80, members 157.78. Cutter overhang 2.70 (reported).

## 4 S2-2 and plate edge, hand against computed

| Quantity | Hand (DERIVED) | Computed (MEASURED) |
|---|---|---|
| S2-2: pitch radius - nut flange radius - keep-out | 160 - 21 - 86.2 = **52.80** | 52.779 (128-gon footprints, lower bound); 52.80 on the scratch figure's drawn extents |
| Screw rod to keep-out | 160 - 4 - 86.2 = 69.80 | 69.78 |
| Member c outer face against the plate edge (theta 270) | 274 + 30 = 304 against 304: 0.00 | y extent -304.00..-244.00 |
| Members a, b x extent against 322 | (274 ± 30) cos 30 ± 30 sin 30 = 196.31..278.27 | 196.31..278.27 |
| Member c in the notch | sides 35 - 30 = 5; inner edge 304 - 65 = 239 against 244: 5 | 5.000 to the plate pieces; on the rail strip 3600.00 of 3600.00 mm² |
| Members a, b on the plate | inside 644 x 608 less notches | 3600.00 of 3600.00 mm² on the plate pieces |
| Ring rim to member | 274 - 30 - 210 = 34.00 | 34.000 (c), 33.944 (b, 128-gon) |
| Ring rim to guide rod | 230 - 10 - 210 = 10.00 | 10.000 |
| Bracket arm length | 244 - 181 = 63 (was 89) | r_out 244.00 |

## 5 --controls, --stale, S1 r5 preview

| Command | Result | Time |
|---|---|---|
| `check_stack.py docs/sketches/s2_spec.yaml` | exit 0; 70 rows evaluated at 4 poses | <2 s |
| `check_sketch.py --stale` (before the overlay edit) | 1 record (s1 r4), 0 differences, exit 0 | 3 s |
| `check_sketch.py --stale` (after) | **red, as expected**: 1 record, 1 difference: `frame_upper.radius recorded 300, live 274`; exit 1 | 3 s |
| `check_sketch.py --stale --include-unaccepted` | 2 records (docs s1 r4, wip s1 r5); 1 difference, the same key; exit 1 | 3 s |
| `check_sketch.py --controls` | Z 38/38, B 87/87, smoke 1/1 (126/126, equal to the P0 count; the live-S1 controls ran at radius 274); exit 0; to wip/fixtures/ | 158 s |
| `check_sketch.py s1 --rev 5` (preview, unchanged `s1_side_poses.py`, to wip/, not of record) | **17/17 pass** | 11.7 s |

s1 r4 key list for the stale red: exactly `frame_upper.radius` (300 to 274). The red is the guard working. It opens S1 r5 (open section 1.2); the record is kept.

S1 r5 preview against the accepted r4 record (MEASURED, `wip/s1_checks_r5.json` against `docs/sketches/s1_checks_r4.json`):
- keys_read: 1 difference, `frame_upper.radius`. files_sha256: proposed_params.yaml. reported: 0 differences (park 959.84, stroke 775, L, highest points unchanged). spec_status unchanged.
- check reasons: K2 overlay leaves 103 to 121; K7 state labels (Correction 6). Every other check reason is equal: S1-1 650.00, S1-2 125.00, S1-3 367.34 / 117.34, S1-4 0.84, S1-5a 192.34, S1-5b 142.00, S1-6, S1-7 607.66.
- S1 values that moved (load pose; the same at every pose):

| Row | r_in, r_out | r_c | x extent | depth band |
|---|---|---|---|---|
| frame_upper_a | 270, 330 to 244, 304 | 300 to 274 | -300.79..-218.83 to -278.27..-196.31 | 109.02..190.98 to 96.02..177.98 |
| frame_upper_b | as a | 300 to 274 | 218.83..300.79 to 196.31..278.27 | as a |
| bracket_anchor_a, bracket_guide_a | 181, 270 to 181, 244 | 225.50 to 212.50 | -248.83..-141.75 to -226.31..-141.75 | 64.52..160.98 to 64.52..147.98 |
| bracket_anchor_b, bracket_guide_b | as a | as a | 141.75..248.83 to 141.75..226.31 | as a |

The member x centres move from ±259.81 to ±237.29 (Design Notes 27). Label "screw frame 30-6060 r" prints 274 (K4 pass). The pad and post are unchanged: r 200 to 215 on a 244 arm. The four r5 PNGs are not drawn here; P6 draws them.

## 6 Shared rows S1/S2

43 row ids are in both specs (MEASURED, field compare). `place` is identical in every one except keepout:

| Rows | place expressions (both specs) | Other field differences in S2 |
|---|---|---|
| frame_upper_a, _b | radial r `frame_upper.radius ∓ profile.width / 2`, theta `jackscrew.angle[1]` / `[0]`, half-width `profile.width / 2` | none |
| screw_a, _b | round r `jackscrew.pitch_radius`, theta `jackscrew.angle[1]` / `[0]`, hw `jackscrew.nominal / 2` | projection circle |
| nut_a, _b; anchor_a, _b; guide_a, _b | round r pitch_radius, hw `jackscrew.nut_flange_od / 2` | kind prism to cylinder (axis Z), projection circle |
| nut_housing_a, _b | round r pitch_radius, hw `ring.nut_housing_od / 2` | projection circle |
| bracket_anchor_a, _b; bracket_guide_a, _b | radial r `jackscrew.pitch_radius + jackscrew.nut_flange_od / 2` to `frame_upper.radius - profile.width / 2`, hw `profile.width / 2` | none |
| liftmotor_a, _b | round r pitch_radius, hw `liftmotor.body / 2 * sqrt(2)` (r 29.70) | kind cylinder to prism (42 square drawn inside the circle) |
| descent_stop, descent_stop_post | radial r `frame_upper.stop_pad_r_in` to `_r_out`, theta `jackscrew.angle[1]`, hw `stop.pad_width / 2` | none |
| motor_mount_a, _b | radial r `pinion.motor_r_in` to `ring.od / 2`, theta `pinion.angle[1]` / `[2]`, hw `pinion.motor_body / 2` | none |
| guide_lug_a, _b | radial r `ring.od / 2` to `ring.guide_lug_r_out`, theta `guide.angle[0]` / `[1]`, hw `ring.guide_lug_half_width` | none |
| pinion_a, _b | radial r `pinion.r_toe - pinion.pitch_diameter / pinion.tooth_count * sind(pinion.pitch_angle)` to `pinion.r_heel + pinion.hub_length`, hw `pinion.outer_diameter / 2` | none |
| motor23_a, _b | radial r `pinion.motor_r_in` to `+ pinion.motor_length`, hw `pinion.motor_body / 2` | none |
| motor_shaft_a, _b | radial r `pinion.motor_r_in - pinion.motor_shaft_length` to `pinion.motor_r_in`, hw `pinion.motor_shaft_od / 2` | none |
| pinion_axis_a, _b | radial r toe tip to `pinion.motor_r_in + pinion.motor_length`, hw 0 | none |
| guide_member, guide_member_b | round r `guide.radius`, theta `guide.angle[0]` / `[1]`, hw `guide.rod_od / 2` | projection circle |
| drill_tube, drill_head | round r 0, hw `drill.tube_od / 2`, `drill.head_od / 2` | projection circle |
| ring, bearing, gear, gear_hub | no place; `section` and `depth` identical | projection circle (gear: trapezoid to circle) |
| base_plate, base_frame | no place | S1 `depth` band; S2 `plan_poly` pieces |
| keepout | S1: none (side-view lines). S2: round r 0, hw `icd.keepout_radius` | S2 adds place for the S2-a pairs; projection circle |

Every `z_rule` of a shared row is identical. S2 drops the side-view predicates (below, above, side, top_within, clears_above, mirror) and the S1-5b group, and adds azimuth predicates.

## 7 Open items for signature

1. **Guide tie z (Designer, blocks P3a).** Correction 1. The tie at the rod top interferes with the top-guide arm. Option: tie z 1165 to 1225 on the arm top, top flush with the member, rod top inside the tie, no key change (tie|arm becomes a z contact, tie|motor at park plan 72.90 ≥ 10). Designer picks; the spec row `guide_tie_a/_b` z_rule changes.
2. **Rubric additions** (spec `rubric_additions`): five lines written from detail 1.2 and the Designer's notes; the Designer confirms or edits.
3. **Shape strings rewritten by the Engineer** (Designer confirms): descent_stop (one pad; the Designer's text said "on each anchor arm"), bracket rows (split into anchor and guide rows that share a footprint, S1 ids kept), base_plate (row references added), lift motor (circumscribing footprint note).
4. **Plan-view harness items for (c)** (no spec change; P4 writes rules, Z and B):
   - a. TP-13: radial rectangles at oblique azimuths classify as "trapezoid" (Correction 7).
   - b. K8 `outboard` with `frame: radial` (Correction 8); `taper` in plan for pinions (narrows inward along the radial axis).
   - c. K8 projected_x/y uses the drawn extent midpoint. A pinion trapezoid at 210 or 330 has an extent midpoint off r_c cos/sin theta, so (c) needs the footprint centre form for trapezoids.
   - d. Plan annuli: ring, bearing, gear, gear_hub and drill_tube footprints are disks (depth-band disk or round place). In plan the nested annuli overlap where their z bands overlap, for example drill_tube|ring undeclared F. (c) needs a plan form from `section` (radial intervals), or the spec declares the nests.
   - e. Plan C pairs that touch in z and overlap in plan (base_frame|base_plate, member feet, rods on the plate, post|pad, tie|member, housing|lug) fail `_assess_pair` C on overlap area. This is the K6 plan form and the LF-8 plan K7 C rule.
   - f. K9 and `figs` keyed by pose: S2 draws one figure; the spec names it `plan_figure: {pose: load}`, and `checks_s2.py` reads that pose. The swept case needs the z bands of every pose but only one figure; (c) defines it.
   - g. `plan_poly` and `sector` are new spec fields evaluated in check_stack. Their premise is containment of the drawn pieces in the evaluated pieces (K8 projected_extent analogue), with Z and B at (c) under detail 1 common (h). The Software Engineer reviews the check_stack addition at P5.
   - h. S2-3: no drawn pitch point; (c) defines the drawn quantity, its Z and its B.
   - i. STUB_EXPECT, STUB_CAUSE, SOURCES for s2 in `checks_s2.py`.
5. **S2-5b ships with S2-5a in the same revision** (detail 1 common (h)); the Designer raises and signs it at P3a.
6. **Tight spots, reported:** ring rim to rod 10.00 (identity under G 10), member c outer face 0.00 to the plate edge (identity), member c 5.00 to the notch on three sides, lift motors 11.71 to the sector edge.
7. **S1 spec edits beyond comments (Loftsman rules at P3b):** four bracket-arm `shape` strings now read "member face (r 244)" (were r 270). Source strings and comments changed as well. Keys, expressions and rows are untouched. If the Loftsman rules shape text frozen at r4, revert those four strings and the r5 M1 reads them against a 244 drawing.
8. **Text values not updated:** `ring.motor_mount_placement` still reads "phase to the screws per S2". The phase is now stated (60 deg) in `pinion.angle` source. No S1 or S2 row reads the key.
9. The orchestrator's `--accept s1 --rev 5` comes after P6, P7, P8 and M2 (open section 1.2). Until then `--stale` stays red on s1 r4 with the one key above.

## 8 Gameplan lines to change

**l.131** (spec format, fields added)

Old:
```
- Fields added at 1.1 (S1): `place` (plan footprint, round or radial: r_in, r_out, half_width, optional `rot` in deg; the footprint contains the whole part, K8 projected_extent); `section` (true-section pieces; K7 refuses class N between two section rows) and `bore_cone` (a bore that follows its mate's cone, K5); `poses` on rows (K9 pose set) and on neighbours (pose-restricted declarations, K7); `load_plane`, `entry_plane` and `stack_ties` (z agreement lints in K6, LF-16, LF1.1-1); `screw_length` (one L expression, detail 1.3); `notes` (stand-ins and the meaning of C); label fields `z_S` and `z_edge`. Expression functions include `sqrt` and `sind`.
```
New:
```
- Fields added at 1.1 (S1): `place` (plan footprint, round or radial: r_in, r_out, half_width, optional `rot` in deg; the footprint contains the whole part, K8 projected_extent); `section` (true-section pieces; K7 refuses class N between two section rows) and `bore_cone` (a bore that follows its mate's cone, K5); `poses` on rows (K9 pose set) and on neighbours (pose-restricted declarations, K7); `load_plane`, `entry_plane` and `stack_ties` (z agreement lints in K6, LF-16, LF1.1-1); `screw_length` (one L expression, detail 1.3); `notes` (stand-ins and the meaning of C); label fields `z_S` and `z_edge`. Expression functions include `sqrt` and `sind`. Fields added at 1.2 (b) (S2): `plan_poly` (convex plan pieces as [x, y] expression points, or a strip from point to point with a half-width; base plate less the column notches, base frame, plate holes, slot lines, guide ties), `sector` (apex on the axis: theta, half_angle, r; operator sector), `plan_figure` (the one plan figure and its pose), `s2_checks` (per-check parameters read by checks_s2.py), `part_list` and `not_drawn` (detail 1 common (b)); check_stack evaluates `plan_poly` and `sector`; their containment premise gets its check at 1.2 (c).
```

**l.247** (detail 1.2 Params keys)

Old:
```
Params keys: `drill.tube_od`, `drill.tube_id`, `icd.keepout_radius`, `icd.footprint_x`, `icd.footprint_y`, `icd.datum_*`, `icd.mounting_pattern`, `frame.*`, `profile.*`, `base.*`; overlay `pinion.*`, `jackscrew.*`, `ring.*`, `guide.*`, `frame_upper.*`.
```
New:
```
Params keys: `drill.tube_od`, `drill.tube_id`, `icd.keepout_radius`, `icd.footprint_x`, `icd.footprint_y`, `icd.datum_*`, `icd.mounting_pattern`, `frame.*`, `profile.*`, `base.*`; overlay `pinion.*`, `jackscrew.*`, `ring.*`, `guide.*` (with `guide.bushing_*`, `guide.top_support`), `frame_upper.*` (with `member_length_rail`, `foot`, `orientation`, `stop_pad_count`), `liftmotor.*` (with `plan_rot`), `operator.*` (sector, hand band, watch position, eye height), `drill.head_*`; the stack keys of the S1 park rule (S2 z bands use the S1 pose stack).
```

**l.248** (detail 1.2 Script)

Old:
```
Script: `docs/sketches/s2_plan.py`. PNG: `s2_plan_r1.png` (location per the Design Notes 25 output rule).
```
New:
```
Spec: `docs/sketches/s2_spec.yaml` (70 rows; S1 ids kept for the 43 shared rows, same place expressions; letter map screw set a 150, b 30, c 270, pinion set a 210, b 330, c 90). Checks: `docs/sketches/checks_s2.py` (S2-1 to S2-6). Script: `docs/sketches/s2_plan.py`. PNG: `s2_plan_r1.png` (location per the Design Notes 25 output rule).
```

**l.181** (operator-task table, change a collet)

Old:
```
Kneel or crouch in the sector, hands at r <= 115, reach about 215 from r 330
```
New:
```
Kneel or crouch in the sector (theta 90 +- 45), hands at r <= 115, reach about 190 from r 304
```

**Echo Site Registry**, after the "Screw frame radius **274 mm**" row, insert:
```
| Screw-to-pinion phase **60 deg** (screws 30, 150, 270; pinions 90, 210, 330) | overlay `jackscrew.angle`, `pinion.angle` | ASSUMED (Designer 1.2 (a); Sean STOP S2-A, O1-B) |
| Bracket arms **r 181 to 244** (63 long) at frame_upper.radius 274; one descent-stop pad r 200 to 215 at jackscrew.angle[1] | overlay `frame_upper.radius`, `frame_upper.stop_pad_*`, `jackscrew.*` | ASSUMED (S1 r5, S2) |
| Guide bushing **LM20UU 32 x 42** in an OD 40 housing hanging 30 below the ring | overlay `guide.bushing_*`, `ring.guide_lug_half_width` | ASSUMED (Designer 1.2 (a)) |
```

**Progress Log, row 1.2** (append): `P2 done: overlay at frame_upper.radius 274 (stale red on s1 r4: frame_upper.radius only, recorded), s2_spec.yaml 70 rows draft for signature, checks_s2.py skeleton, S1 r5 preview 17/17; guide tie z open for the Designer.`

The detail 1.2 Shows line (l.245) and the S2-5a, S2-5b, S2-6 rows (l.256 to 258) already match the spec: no change.
