# Step 1.1 (b) Designer spec sign-off, S1

## Corrections to the brief

1. **The brief predates Design Notes 22.** I check the spec against option R, which Sean adopted after my review. Park is 959.84 z_A, stroke 775.00 and L 900 DECLARED [DN23]. Sean's 900 / 900 / 1140 replaces my current-rule values of 950 and 1015.
2. **My operator-task rows (review section 8) are stale under option R.** They used park 1015 (tip 1075 z_S). Section 6 below has the corrected heights. These rows go to the gameplan edit (l.179-183), so the fix belongs to the orchestrator at G-edit and needs no spec change.
3. **My `ring.pinion_support` contradicts my own R5 geometry.** The pinion back face is at r 140 and the NEMA 23 flange face at r 142, which leaves 2 mm of radial room. A shaft-bushing block cannot fit there. The Engineer's "no dimensions, so no row" result is the symptom. Ruling in section 1, item E3.
4. Geometry rulings belong to The Loftsman, who signs in parallel: the K7 plan-footprint bound, the screw-length expression, and S1-5b against the wing-nut top (148.75) or the collar top (142.00). They are not repeated here.

Numbers are DERIVED from proposed_params.yaml, params and the revised spec unless tagged. Values I set here are ASSUMED.

## 1. Rulings on the Engineer's open items (his section 9, items 3 to 6)

| # | Item | Ruling |
|---|---|---|
| E1 | Guide-lug width, half_width = `ring.guide_lug_r_out - guide.radius` = 20 | **Value accepted, expression rejected.** I meant a lug 40 x 40 (DERIVED) centred on the rod at r 230: radial span 210 to 250 and tangential width 40. That encloses an LM20UU bushing OD 32 (ASSUMED, catalogue class, no source) with a 4 mm wall. The spec expression ties the tangential width to the radial overhang. A change to guide.radius 240 at S2 would give a 20 mm wide lug around a 20 mm rod. New leaf `ring.guide_lug_half_width` 20 mm, ASSUMED, source "Designer 1.1 (b): LM20UU OD 32 + 2 x 4 wall". FIX F3. |
| E2 | Motor-standoff footprint = motor footprint (r 142 to 218, half-width 28.5) | **Rejected at r_out.** The motor ends at r 218 and the ring rim is at r 210, so a standoff "on the ring top face" overhangs the rim by 8 mm (DERIVED). The standoff runs r 142 to `ring.od / 2` 210 (68 long, half-width 28.5, height 23.5), with the motor body overhanging the rim by 8. r_in 142 is unchanged, so the motor_mount\|pinion plan gap stays 2.00. FIX F2. |
| E3 | Pinion-shaft bushing blocks have no dimensions, so no row | **Ruled: there are no separate blocks at S1.** The pinion is carried on the NEMA 23 shaft (8 x 21, into the pinion hub), on the motor's own bearings. The motor mount is the pinion support. The radial room between pinion back and flange is 2 mm, so a block has no place. Mesh load per pinion: 10 N m / 0.125 m / 3 = 26.7 N tangential (DERIVED from drill.torque_target and gear.pitch_diameter). That is small against a NEMA 23 shaft, but no shaft rating is on file. New `ring.pinion_support` value: "none separate at S1: each pinion is carried on its NEMA 23 shaft and motor bearings; the motor mount (ring.motor_mount_*) is the support; an outboard bushing is an S6 option if the mesh or drill-weight load exceeds the motor shaft rating". The ring shape string drops "pinion-shaft bushing blocks". FIX F1. |
| E4 | base_plate\|frame_upper_a/b and base_plate\|guide_member/_b declared N, "plate notched" | **Rejected: these are not real nests.** The overlay has no notch leaf. Nothing places a base-frame member under (x +/-259.8, y 150) or under the rod feet at (+/-230, 0): the side rails run at y about +/-274 and the end members at the x ends. As declared, a 60 x 60 member stands on air inside a hole in the plate. The ruling puts the members and rods on the plate top. The member foot bolts to the plate, and the plate, carried by the base frame, is in the axial chain. Axial load per member at the 1000 N cut case is about 333 N (DERIVED), small for a 12 mm plate, so the plate is a sound foot. The rods stand in shaft supports on the plate top. FIX F4. |
| E5 | Second guide-rod row `guide_member_b` | **Accepted.** guide.count 2 at 0 and 180 deg. Both rods project at x = +/-230 with depth band y +/-10, and guide_lug_b needs its rod for the N declaration and K9. Shape string: FIX F6. |
| E6 | Descent pad to nut housing at exactly 10.00 (zero margin) | **Rejected at 195.** `frame_upper.stop_pad_r_in` 200 mm ASSUMED. The pad-to-housing plan gap becomes 200 - 185 = 15.00, a margin of 5.00 over G 10, which covers the 128-gon 0.01 error and any S3 growth of the 50 OD housing up to 60 OD. The contact strip becomes r 200 to 210 x 60 = 600 mm², 1.67 MPa at 1000 N (DERIVED). The Engineer's 196 leaves 1 mm against an ASSUMED housing OD. FIX F5. |

## 2. Task checks

| # | Check | Result |
|---|---|---|
| 1 | Every row `shape` matches my note; every ring.* feature has a row or key | FAIL on four strings, which F1, F4, F5 and F6 correct: ring (bushing blocks), frame_upper_a/b ("from the base frame"), guide_member/_b ("ring bushing lug as a short block", now its own row), descent_stop ("r 195 to 215"). The other 33 rows match my section 2 text or the Engineer's split-out text drawn from my ring note. Coverage of ring.* at l.121: nut housings in rows nut_housing_a/b; nut mounting by key; motor mounts in rows motor_mount_a/b; clearance bore as the ring `section` r 100 to 210; gear seat by key (none); bearing seat in the bearing row (top flush, hanging 13); guide interface in rows guide_lug_a/b; material, position and mass by key. PASS once F1 is applied. |
| 2 | Pose table and cores per pose | PASS. load park_tip 959.84, core 101.17 to 851.17. start stop.start_z[0] 834.84, "top of the 650 mm travel", core 42.5 to 792.5. capture_end 184.84. park with no core. `capture_core: core_750`; core_500 deleted; `rests_on` poses [start, capture_end]. |
| 3 | Rubric additions true in every pose | PASS. ring_on_tube: bearing bottom - head top = (tip + 117) - (tip + 106.369) = 10.63; tube top - gear top = (tip + 800) - (tip + 256) = 544.00; both constant in every pose. Motors: top tip + 222.5 against gear back face tip + 256, -33.50; motor r_in 142 > pinion r_out 140 (outboard 2.00); motor23_a at 210 deg cos < 0, motor23_b at 330 deg cos > 0. Core: row poses [load, start, capture_end]. Head below gear and top block: tip + 106.37 against tip + 222.23 and tip + 800. |
| 4 | R6 nests and dispositions | PASS except E4. Real nests: the base stack (collet in register bore, ledge in collet, holder in bore, wing nut on receiver thread, core through all), screw in nut, anchor and guide; boss through the ring plate; nut and screw in the ring; core in the drill bore at capture_end only; gear\|pinion mesh; pinion\|motor23 (shaft in hub); lug\|rod (rod in bushing). The C and F dispositions are acceptable. gear_hub\|pinion plan gap 6.52 (hub r 90 against toe 96.54) is acceptable as F between two turning parts. ring\|descent_stop C at capture_end: ring underside 314.84 = pad top 314.84, contact at r 200 to 210 after F5. Lift motors at 192 to 240 z_A, 61.84 below the lowest ring-assembly point 301.84, are acceptable. |
| 5 | g_min per pair | PASS. fixed_g10 (frame members, lift motors, anchor and guide blocks; G 10, swept), s1_5b_base (six base parts, G 10, capture_end), core_750\|bore_ceiling G 25 at capture_end (192.34), nut_housing_a\|descent_stop G 10 (15.00 after F5), ring\|descent_stop C, gear\|pinion N. NOTE N1 covers the keep-out seed. |
| 6 | Operator-task rows against the check_stack heights | FAIL in my own rows 1 and 2 (stale park). Corrected rows in section 6. This changes the G-edit input and the spec is unaffected. |
| 7 | S1-7 row | PASS. checks_s1.s1_7 reads z_max of the `capture_core` patch at start minus the capture_end tip, against upper.drill_advance_500core: 792.50 - 184.84 = 607.66 >= 534.93, spare 72.73. The planned B (0.5 m core as capture core) gives 357.66, short 177.27. Both as I wrote them. |

## 3. FIX list (for P2f)

| ID | Row or key | Required change |
|---|---|---|
| F1 | proposed_params `ring.pinion_support`; s1_spec row `ring` shape | pinion_support value as section 1 E3, source "Designer 1.1 (b): pinion on the NEMA 23 shaft; 2 mm between pinion back r 140 and flange r 142", ASSUMED. Ring shape: delete "pinion-shaft bushing blocks;". |
| F2 | rows `motor_mount_a`, `motor_mount_b` place; shape | `r_out: "ring.od / 2"` (210). Add `ring.od` to keys. Shape: "NEMA 23 mount standoff, ring.motor_mount_height tall, r pinion.motor_r_in to the ring rim, under motor23_x; the motor overhangs the rim by 8 (part of the ring structure)". |
| F3 | proposed_params new `ring.guide_lug_half_width`; rows `guide_lug_a`, `guide_lug_b` place and keys | New leaf {value 20, unit mm, source "Designer 1.1 (b): LM20UU OD 32 + 2 x 4 wall; no source", status ASSUMED}. `half_width: ring.guide_lug_half_width`. |
| F4 | rows `frame_upper_a/b`, `guide_member`, `guide_member_b`, `base_plate`; proposed_params `frame_upper.member_length` | Delete the four N entries from base_plate. frame_upper_a/b: z_rule {z_min: base.plate_thickness, z_max: "base.plate_thickness + frame_upper.member_length"}, neighbour `{id: base_plate, class: C, g_min: 0, source: "member foot bolted on the plate top; axial loop through the plate to the base frame (Designer 1.1 (b))"}` in place of base_frame C. member_length 1213 DERIVED (top_guide_z 1165 + profile.height 60 - base.plate_thickness 12); the top stays at 1225 z_A (1285 z_S). Shape: "screw frame member: vertical 30-6060, 60 wide, from the plate top to top_guide_z + 60, with the anchor and guide bracket arms drawn to the screw". guide_member/_b: z_rule {z_min: base.plate_thickness, z_max: "base.plate_thickness + guide.length"} (12 to 1212), neighbour `{id: base_plate, class: C, g_min: 0, source: "rod in a shaft support on the plate top (Designer 1.1 (b))"}`. |
| F5 | proposed_params `frame_upper.stop_pad_r_in`; row `descent_stop` shape; row `nut_housing_a` and `ring` neighbour sources | stop_pad_r_in 200, source "Designer 1.1 (b): 15 clear of the nut housing (r 185), 5 over G 10", ASSUMED. Shape "radial r 200 to 215". nut_housing_a\|descent_stop source "plan gap 15.0 (pad r 200, housing r 185)". ring\|descent_stop source "contact strip r 200 to 210 x 60". |
| F6 | rows `guide_member`, `guide_member_b` shape | "ring guide rod: round rod 20 OD in a shaft support on the plate top, guide.length tall at its projected azimuth; the bushing lug is row guide_lug_x". |

Expected effects after P2f, DERIVED and for the Engineer to confirm by run:
- K7: frame_upper\|base_plate and rod\|base_plate read C at z 12. frame_upper\|base_frame becomes undeclared F with a 12 mm XZ gap.
- Highest point: unchanged, 1969.84 z_S.
- S1-x: no value changes. nut_housing_a\|descent_stop goes from 10.00 to 15.00.

## 4. NOTES (no action at (b))

- N1. **The keep-out seed pair (l.147) is not expressed in the spec.** The keepout row has no neighbours, and no harness code reads icd.keepout_radius. No S1 part violates it on these values. Least radial clearance over 86.2: gear bore r 90, 3.80, but the hub (exempt) fills it; ring bore r 100, 13.80; pinion toe r 96.54, 10.34. The fixed parts above the drill path sit at r >= 139 (anchor and guide blocks at r 160 - 21). S2 (plan view) is the natural place for the check.
- N2. **The θ 270 screw frame member, not drawn in S1, overhangs the plate edge.** Member outer edge r 330 against footprint_y / 2 = 304, overhang 26 (DERIVED). S2 must set `frame_upper.radius` <= 274 or widen the plate. 274 still clears the guide lugs: about 117 at the 30 deg separation.
- N3. **Guide bushing length against ring thickness.** An LM20UU is 42 long (ASSUMED, catalogue class) against ring.thickness 12, so the drawn lug is the mount and the bushing is longer than it. The likely form is a flanged bushing below the lug (down to about 284.84 z_A at capture_end, with no neighbour at 0 or 180 deg). A 12 mm plain bushing (L/D 0.6) will cock. S2/S6, N2.
- N4. **Design Notes 1 against the bearing.** Design Notes 1 says the pinions carry the drill weight. The overlay bearing is a thrust pair rated 2000 N both ways, so the bearing carries the axial loop and the pinions see mesh load only. Teeth-down (TP-2) still holds from the R5 geometry: the pinions sit below the gear. If the weight were meant to go through the mesh, about 26 N per pinion (8 kg / 3) adds radial load on each NEMA 23 shaft. Decided at S6.
- N5. **Load-pose margin under tilt.** At entry the core top is 50.00 below the tip under option R (collar-top plane). A tilted 750 x 100 core raises its top by at most sqrt(750² + 100²) - 750 = 6.64, at 7.6 deg (DERIVED). The margin cannot be consumed by tilt.
- N6. **Every operator sector between two screws holds a NEMA 23.** The pinions are phased 60 deg from the screws. The sector at 90 deg is the only one without a guide rod, and the motor at 90 deg sits at 1185.34 to 1242.34 z_S, r 142 to 218, at load. A leaning operator meets it at chest and shoulder height. For S2-5 and the Step 2 guard row.

## 5. Items for Sean at STOP S-1 (added to my review section 9)

- frame_upper.stop_pad_r_in 200 (was 195), ring.guide_lug_half_width 20, motor standoff to the ring rim. All ASSUMED.
- Screw frame members and guide rods stand on the base-plate top (F4). The alternative, members through a plate notch onto base-frame cross members, is an S2 footprint choice and needs a cross member under each foot.
- No separate pinion bushing: the pinions ride on the NEMA 23 shafts (F1, N4).

## 6. Operator-task rows, corrected for option R (replace review section 8 at G-edit; z_S = z_A + 60)

| Task | Pose | Reach height and stance | Sightline | Hazard | Check or rubric |
|---|---|---|---|---|---|
| Lift a 0.75 m core (15.6 kg) into the collet under the parked ring | load | Core bottom passes over the collar top at 219.84. The core top at entry is 969.84, 50.00 below the tip at 1019.84 (tilt costs at most 6.64). Operator stands in the S2-5 sector between two screws, torso outside the frame members (r >= 330), arms reaching about 330 to the axis with the core upright; hands 0.5 to 1.0 m | down into the holder bore from the sector, between the base (213) and the bearing bottom at 1136.84 | 15.6 kg held about 330 mm out, about 50 N m at the shoulder (Step 2 loading aid). Ring assembly at 1136.84 to 1275.84, with the NEMA 23 in the sector at 1185.34 to 1242.34: chest and shoulder strike when leaning in. Ring overhead on the power-off hold (Step 2) | S1-3, S2-5, V10 |
| Change a collet (wing nut, 230 span) beneath the ring, between screws | load | Wing nut body 157 to 213, sweep radius 115. Kneel or crouch in the sector, hands at r <= 115, reach about 215 from r 330 | wing nut from the sector at knee height | Either side of the sector: lift motors and couplings at the screw azimuths (252 to 325, r 160), anchor arms (325 to 355, r 160 to 270), descent-stop pad (363 to 375, theta 150, r 200 to 215). Drill head overhead at 1019.84 | S1-5b, S2-5, V10 |
| Stand and watch during a cut | start to capture_end | outside the frame (r >= 400), standing | At start the cutter (894.84 to 1001.21) is in view under the ring. At capture_end the ring rim (r 210, underside 374.84) hides the cutter (244.84 to 351.21) from any eye above about 0.49 m at r 400; a standing observer cannot see the end of the cut | The gear (r <= 126.32) and three pinions turn at drill.rpm 60, and the NEMA 23s (r <= 218) ride with them. The gear passes 1150.84 to 467.07 through the open operator sector, so a guard or interlock is needed (Step 2 row) | K7 swept case, V10 |

## 7. Gameplan lines to change (in addition to review section 10 and Engineer section 8)

- l.121 ring.* seed: "pinion support: the NEMA 23 shaft and motor mount (no separate bushing at S1)".
- l.179-183 operator-task table: S1 rows from section 6 of this file, in place of review section 8.
- Design Notes 1, "support ring with shaft bushings": add "(1.1 (b): the ring carries the motors; the pinions ride on the motor shafts; the drill axial load goes through the drill-to-ring bearing)".

## Verdict

FIX: 6 items, F1 to F6 in section 3. SPEC NOT SIGNED (Designer). A re-check after P2f covers F1 to F6 only. Every other part of the spec carries my signature as revised: shapes, pose table, rubric additions and ring_on_tube, R6 nests except E4, g_min, and S1-7.
