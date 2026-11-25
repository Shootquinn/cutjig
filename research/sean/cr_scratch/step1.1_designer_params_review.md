# Step 1.1 (a) Designer params review, S1

## Corrections to the brief

1. **TP-2, collet: the draft has it backwards.** The collet's outer cone narrows upward, not downward. `build_parts/collet_family.py` dims() sets r(z) = r0 - (z - z_cone) tan(cone.alpha), so the radius falls as z rises. params `collet.min_wall` applies "at the cone top". The holder clamps by moving down: holder bottom goes from 13.626 (R) to 2.00 (K-max) above the floor (ASSEMBLY.md Poses). The predicate becomes `taper narrows: up`.
2. **TP-2, gear: the draft has it backwards.** Design Notes 1 says the pinions carry the drill weight, so the gear rests on the pinions and its teeth face down. The draft draws teeth facing up, with the pinions level with the gear. In each half-section the flat back face is on top and the tooth face is underneath, rising outward along the pitch cone (apex on the drill axis at the pinion axis height, slope 1 in 3, DERIVED from gear.pitch_angle 71.565). Read per side, the section narrows downward. Predicate in section 6.
3. **B3, screw length expression.** The ring nut housing is coaxial with the nut and has the same height (`ring.nut_housing_height` 30 = `jackscrew.nut_length` 30). The housing term in the detail 1.3 formula therefore counts the same 30 mm twice. The S1-4 band is short by a different term: the 10 mm G clearance between the moving nut housing and the fixed anchor and guide blocks (g_min seed l.148), at each end. Expression the screw needs: L_min = lift stroke + anchor_allowance + guide_allowance + max(nut_length, nut_housing_height) + 2 x 10. That gives 940.16 for the stand-in, against 920.16 (S1-4 as coded) and 950.16 (detail 1.3), all DERIVED. Handed to The Loftsman for P3b.
4. **The 830.16 stroke depends on a value no pose uses.** It rests on max(`stop.start_z`) = 965 = `stop.height_range[1]` 315 + 650. params marks 315 "old 300 seed + 15, not re-derived". Under G2 the 0.75 m capture ends at `stop.height_z` 184.84 (bore ceiling 984.84 clears the core top 792.5 by 192.34, DERIVED), so neither 315 nor 965 belongs to any S1 pose. S1 is the step that re-derives `stop.height_range[1]` (detail 1.1 "Closes"). The re-derivation and its effect on L are in item 9.2 for Sean.
5. **G1 plane against the loading task.** The operator must lift the core bottom over the collar top (159.84 z_A) before it drops into the holder bore. The clearance at loading is therefore set at the collar-top plane. The core stop (42.5) is where the core finishes. While max(stop.start_z) stays at 965 this changes nothing for 0.5 and 0.75 m (park 1015 under either plane). It matters for the 1 m core and under item 4: at a park of 884.84 the entering 0.75 m core top (909.84) would sit 25 mm inside the drill tip. Item 9.3 for Sean.
6. **`ring.clearance_bore` 190 contradicts `ring.bearing_seat`**, which says the seat ID equals `bearing.od` 200. Corrected to 200.
7. **`ring.gear_seat` puts the gear on the ring top face.** The gear turns with the drill and the ring does not turn, so the gear cannot sit on the ring. Corrected: the gear mounts on the tube through a hub (`gear.hub`). The ring carries the pinion shaft supports, the "support ring with shaft bushings" of Design Notes 1.
8. **The N1 lower bound comes from the drill head, not S1-5b.** With the bearing hanging 13 mm below the ring plate, S1-5b (ring assembly >= collar top 159.84 + 10 at capture_end) needs `ring.position_above_tip` >= -2.0. Keeping the ring assembly on the tube 10 mm above the head top needs >= 129.37 (both DERIVED).

All numbers below are DERIVED from params and the overlay unless tagged otherwise. ASSUMED marks a working value I set. Nothing here was measured.

## 1. Functional completeness (8.4a), against gameplan l.121

| Namespace | Feature (l.121) | Result | Missing or wrong leaf, proposed value |
|---|---|---|---|
| ring | three nut housings at pitch radius and angle | PASS | none (count 3 DERIVED, od 50, height 30 ASSUMED) |
| ring | nut mounting, rigid or floating | PASS | none |
| ring | three NEMA 23 mounts at pinion.angle, S2 phase | FAIL | No mount geometry: motor axis height and mount standoff are missing. `ring.motor_mount_height` 23.5 mm DERIVED (pinion.axis_above_ring_top 52 - pinion.motor_body / 2 28.5); flange face radius `pinion.motor_r_in` 142 mm ASSUMED |
| ring | central clearance bore over gear and keep-out | FAIL | `ring.clearance_bore` 190 is below bearing.od 200. New 200 mm DERIVED (= bearing.od; 13.8 over icd.keepout_radius) |
| ring | gear and support-ring seat | FAIL | The value seats the gear on the ring. New `ring.gear_seat` text: "none: the gear turns with the drill on gear.hub". New `ring.pinion_support`: "three pinion-shaft bushing blocks on the ring top at pinion.angle, shaft axis at pinion.axis_above_ring_top (Design Notes 1 support ring)" ASSUMED. New `gear.hub`: "clamp hub on the tube, bore drill.tube_od 152.4, OD gear.bore 180, height = gear section height" ASSUMED |
| ring | drill-to-ring bearing seat | FAIL | The seat contradicts the bore (row above) and has no axial position. New `ring.bearing_seat` text: "outer race in the clearance bore (ID bearing.od), bearing top flush with the ring top, hanging bearing.height - ring.thickness = 13 below the underside" ASSUMED. Reason: a seat bottom-flush puts the bearing top 3.8 mm under the pinion toe |
| ring | guide and anti-rotation interface (N2) | PASS | NOTE: guide.radius 230 lies outside ring.od / 2 210, so the bushings need lugs. `ring.guide_lug_r_out` 250 mm ASSUMED, at guide.angle |
| ring | material and form | PASS | none (Sean) |
| ring | position along the drill (N1) | PASS | value changed (section 3) |
| ring | mass | PASS | none |
| bearing | type, bore, OD, height, axial both ways, radial | PASS (6) | NOTE: one 25 mm bearing plane gives the drill no tilt stiffness. N4 and S6 decide between two planes and a slewing ring |
| guide | type, count, positions, length | PASS (4) | none; guide.length 1200 covers ring travel 314.84 to 1157 z_A |
| gear | PD, face width, tooth count, pitch angle, bore, mass | PASS (6) | added for plotting: `gear.od`, `gear.toe_tip_above_pinion_axis`, `gear.back_face_above_pinion_axis`, `gear.hub` (section 3) |
| pinion | count, angle, tooth count, pitch angle, motor class | PASS (5) | added for plotting: R5 keys (section 3) |
| jackscrew | count, angle, pitch radius, nominal, length, root diameter, lead, efficiency, anchor z, top guide z, anchor and guide allowances | PASS (12) | values changed (section 3) |
| jackscrew | lead-screw nut keys under jackscrew.nut_* | PASS | none |
| liftmotor | NEMA 17, holding torque | PASS (2) | position changed; `liftmotor.coupling_length` added |
| hold | power-off hold device | PASS | Step 2 |
| frame_upper | profile, members, radius, length | PASS | stop pad radii added (R6) |
| drill | length, mass, head_od, head_length, top_block_*, bore ceiling | PASS (6) | none |

Count: 49 PASS, 4 FAIL, all four in `ring.*` (motor mounts, clearance bore, gear seat, bearing seat). Every FAIL has a proposed leaf in section 3.

## 2. Shape notes (8.4b), one per s1_spec.yaml row

| Row id | shape |
|---|---|
| floor | "shop floor line across the full footprint, ground hatch below" |
| base_frame | "30-6060 base frame: side rails along X seen as a 60 mm band over footprint_x; end members as 60 x 60 sections at x = +/- frame.end_x" |
| base_plate | "base plate in section, base.plate_thickness on the frame top, break at the receiver spigot hole" |
| receiver | "receiver cup in section: walls to the rim, floor at icd.floor_above_datum_a with the debris-hole gap, spigot into the plate, thread ticks on the outer wall" |
| collet | "collet cone in section, two four-vertex sides mirrored about the axis: foot ring on the receiver floor, outer cone narrowing upward at cone.alpha 10 deg, slit ticks" |
| core_seat | "core-seat ledge, collet.core_seat_height 2.5 tall and core_seat_width 3 wide, inside the collet bore bottom; core bottom bears on its top" |
| holder | "holder tube in section with flange and collar ring on top; flange above the receiver rim by the stroke gap" |
| wingnut | "wing nut: body wingnut.body_od x nut.overall_height, two wings to span 230, sweep radius 115 as dashed extent lines" |
| core_500 | row deleted: no 0.5 m core is drawn (section 5); the S1-7 B fixture uses it |
| core_750 | "capture core (0.75 m install core): upright cylinder 100 OD, solid outline, chamfer mark at the top end; bottom on the core seat at start and capture_end, at mid-insertion at load; absent at park" |
| drill_head | "cutter and iris head: wider than the tube, drill.head_od x drill.head_length from the tip, cutter teeth ticks on the bottom edge, iris throat as a dashed opening; label 'cutter OD ASSUMED'" |
| drill_tube | "drill tube: rectangle 152.4 wide from the head top to the drill top, bore dashed at tube ID; label 'tube OD 152.4 (keep-out basis)'" |
| drill_top_block | "top-end block on the drill top: solid block top_block_od x top_block_length, no teeth, cable-exit mark on top; reads as the tail, unlike the head" |
| bore_ceiling | "dashed line across the bore at tip + drill.bore_ceiling_above_tip, label" |
| keepout | "two dashed vertical lines at +/- icd.keepout_radius 86.2, label" |
| ring | "ring structure: plate section ring.od x ring.thickness with the clearance bore gap at the centre; nut-housing bosses (50 OD, 30 tall, centred on the nut) at each projected screw; NEMA 23 mount standoffs (ring.motor_mount_height) on the top face; pinion-shaft bushing blocks; guide lugs. Split into convex pieces. Reads as the structure that carries screws, motors and drill" |
| bearing | "drill-to-ring bearing: nested rectangles per side, outer race in the ring bore (r 100), inner race on the tube (r 76.2), top flush with the ring top, hanging 13 below the plate" |
| gear | "bevel ring gear in section: two four-vertex sides mirrored about the drill axis; flat back face on top; tooth face underneath rising outward at the pitch cone (1 in 3) toward the heel at gear.od; tooth ticks on the lower face toward the pinions" |
| gear_hub (new row) | "gear hub: rectangles per side from the tube OD to gear.bore, same height as the gear, clamped on the tube; turns with the drill" |
| pinion_a, pinion_b | "bevel pinion as projected at its azimuth: four-vertex trapezoid with the narrow toe toward the axis (r 96.54), heel 91.24 OD at r 125, hub to r 140; tooth ticks on the upper face meshing under the gear; shaft line outward to the motor" |
| motor23_a, motor23_b | "NEMA 23: square body 57 x 76 on a radial axis, flange face at r 142, shaft 8 x 21 inward into the pinion, connector end outboard; standoff to the ring top" |
| screw_a | "T8 jack screw: rectangle 8 wide from the anchor to the top guide, lead ticks at jackscrew.lead; label 'T8 screw L'" |
| screw_b | "T8 jack screw: rectangle 8 wide from the anchor to the top guide, lead ticks at jackscrew.lead" |
| nut_a, nut_b | "brass flange nut, nut_length 30 centred on nut z, flange at the ring face, inside the housing boss" |
| anchor_a, anchor_b | "bottom anchor: thrust-bearing block anchor_allowance tall on a bracket arm from the screw frame member, bearing line marked; coupling and lift motor below" |
| guide_a, guide_b | "top guide: radial bearing block guide_allowance tall on a bracket arm from the screw frame member, open top (radial only, no thrust)" |
| liftmotor_a, liftmotor_b | "NEMA 17 lift motor: square body 42 x 48 below the anchor, shaft up through a coupling (liftmotor.coupling_length) to the screw bottom; S3 places it" |
| guide_member | "ring guide rod: round rod 20 OD from the base to guide.length at its projected azimuth, ring bushing lug as a short block at the ring height" |
| frame_upper_a, frame_upper_b | "screw frame member: vertical 30-6060, 60 wide, from the base frame to top_guide_z + 60, with the anchor and guide bracket arms drawn to the screw" |
| descent_stop | "metal descent-stop pad, 12 thick, radial r 195 to 215 under the ring rim on the anchor bracket arm, metal hatch; the ring rim lands on it at capture_end" |
| height_target | "dashed reference line at 2000 above the floor, labelled 'soft target', never a limit" |

## 3. Overlay value table

| Key | Old | New | Unit | Source | Status |
|---|---|---|---|---|---|
| ring.position_above_tip | 200 | 130 | mm | Designer 1.1 (a), G3: bearing bottom (ring underside - 13) 10.63 above the head top (tip + 106.369); N1 lower bound 129.37 DERIVED; S1-5b bound -2.0, not binding | ASSUMED |
| ring.clearance_bore | 190 | 200 | mm | = bearing.od (bearing seat); 13.8 over icd.keepout_radius | DERIVED |
| ring.gear_seat | "gear and support-ring seat on the ring top face" | "none: the gear turns with the drill on gear.hub; the ring carries ring.pinion_support" | | Designer 1.1 (a); Design Notes 1 | ASSUMED |
| ring.pinion_support | none | "three pinion-shaft bushing blocks on the ring top at pinion.angle, shaft axis at pinion.axis_above_ring_top" | | Design Notes 1 (support ring with shaft bushings) | ASSUMED |
| ring.bearing_seat | "...in the clearance bore, ID = bearing.od" | "outer race in the clearance bore (ID bearing.od), bearing top flush with the ring top, hanging bearing.height - ring.thickness below" | | Designer 1.1 (a); pinion toe clearance | ASSUMED |
| ring.motor_mount_height | none | 23.5 | mm | pinion.axis_above_ring_top 52 - pinion.motor_body / 2 28.5 | DERIVED |
| ring.guide_lug_r_out | none | 250 | mm | guide.radius 230 + bushing 20; no source | ASSUMED |
| jackscrew.anchor_z | 0 | 265 | mm | Designer 1.1 (a), G3: anchor block 265 to 295 on the frame-member bracket, 253 above the plate top (12); nut-housing bottom at capture_end 305.84, gap 10.84 >= g_min 10 | ASSUMED |
| jackscrew.length | 900 (DECLARED) | 950 | mm | Designer 1.1 (a), G3; DN23 estimate 800-900 exceeded. L_min 940.16 = stroke 830.16 + 30 + 30 + max(30, 30) + 2 x 10, rounded up to 10 mm | ASSUMED |
| jackscrew.top_guide_z | 900 | 1215 | mm | anchor_z + length | DERIVED |
| jackscrew.anchor_allowance, guide_allowance, nut_length | 30, 30, 30 | unchanged | mm | | ASSUMED |
| collet.core_stop_z | none | 42.5 | mm | G4: receiver floor icd.floor_above_datum_a 40 (ASSEMBLY.md Coordinate frame; icd.datum_a) + collet.core_seat_height 2.5 (ledge top; build_parts/collet_family.py dims(), inner radius steps below z = seat); collet foot ring on the receiver floor seat (ASSEMBLY.md Relations base\|collet C; Load path "core stop, collet foot, floor seat"); Designer 1.1 (a); 4a promotion list | ASSUMED |
| pinion.pitch_diameter | none | 83.33 | mm | gear.pitch_diameter / gear.tooth_count x pinion.tooth_count (module 4.1667) | DERIVED |
| pinion.outer_diameter | none | 91.24 | mm | pitch_diameter + 2 m cos(pinion.pitch_angle) | DERIVED |
| pinion.face_width | none | 30 | mm | = gear.face_width | DERIVED |
| pinion.r_toe | none | 96.54 | mm | gear.pitch_diameter / 2 - face_width sin(gear.pitch_angle) | DERIVED |
| pinion.r_heel | none | 125 | mm | gear.pitch_diameter / 2 | DERIVED |
| pinion.hub_length | none | 15 | mm | no source; pinion back face at r 140 | ASSUMED |
| pinion.axis_above_ring_top | none | 52 | mm | heel tip radius 45.62 + 6.38 clear of the ring top | ASSUMED |
| pinion.motor_r_in | none | 142 | mm | flange face 2 mm outboard of the pinion back (r 140); motor outer end 218 | ASSUMED |
| pinion.motor_shaft_od | none | 8 | mm | NEMA 23 common shaft; no source | ASSUMED |
| pinion.motor_shaft_length | none | 21 | mm | NEMA 23 common shaft; no source | ASSUMED |
| gear.od | none | 252.64 | mm | pitch_diameter + 2 m cos(gear.pitch_angle) | DERIVED |
| gear.toe_tip_above_pinion_axis | none | 28.23 | mm | toe pitch point z 32.18 (r 96.54 / 3) minus addendum normal 3.95 | DERIVED |
| gear.back_face_above_pinion_axis | none | 62 | mm | heel pitch point 41.67 + rim 20.33; no source | ASSUMED |
| gear.hub | none | "clamp hub on the tube, bore drill.tube_od, OD gear.bore, height = gear section height 33.77" | | Designer 1.1 (a) | ASSUMED |
| liftmotor.position | "above the top guide, direct coupling" | "below the bottom anchor, coupling up to the screw bottom (placeholder; S3 places it)" | | Designer 1.1 (a), R6: the ring sweep (gear top 1271 z_A at park) then passes no lift motor | ASSUMED |
| liftmotor.coupling_length | none | 25 | mm | no source | ASSUMED |
| frame_upper.member_length | 960 | 1275 | mm | jackscrew.top_guide_z + profile.height | DERIVED |
| frame_upper.stop_pad_r_in | none | 195 | mm | descent-stop pad inner edge, 10 clear of the nut housing (housing centre r 160, radius 25) | ASSUMED |
| frame_upper.stop_pad_r_out | none | 215 | mm | ring.od / 2 210 + 5 | ASSUMED |

Spec z_rules these values need, for the Engineer at (b). All are in z_A; tip is the pose tip_z.
- ring_bottom = tip + ring.position_above_tip; ring_top = ring_bottom + ring.thickness; nut_z = ring_bottom + ring.thickness / 2 (as coded).
- bearing: ring_top - bearing.height to ring_top.
- pinion_axis = ring_top + pinion.axis_above_ring_top. pinion: pinion_axis +/- pinion.outer_diameter / 2, place r_in pinion.r_toe, r_out pinion.r_heel + pinion.hub_length, half_width pinion.outer_diameter / 2, radial.
- motor23: pinion_axis +/- pinion.motor_body / 2, place r_in pinion.motor_r_in, r_out pinion.motor_r_in + pinion.motor_length, radial.
- gear and gear_hub: pinion_axis + gear.toe_tip_above_pinion_axis to pinion_axis + gear.back_face_above_pinion_axis. Gear depth +/- gear.od / 2.
- liftmotor: anchor_z - coupling_length - liftmotor.length to anchor_z - coupling_length.
- descent_stop: (stop.height_z + ring.position_above_tip) - stop.pad_thickness to stop.height_z + ring.position_above_tip, place r_in frame_upper.stop_pad_r_in, r_out frame_upper.stop_pad_r_out, theta jackscrew.angle[1], half_width stop.pad_width / 2, radial.

Ring-assembly stack, the same in every pose, relative to the tip (DERIVED):

| Feature | Low | High |
|---|---|---|
| bearing | 117 | 142 |
| ring plate | 130 | 142 |
| nut and housing | 121 | 151 |
| pinion | 148.38 | 239.62 |
| NEMA 23 | 165.5 | 222.5 |
| gear and hub | 222.23 | 256 |

## 4. S1-4 band by hand, per pose

Values: anchor_z 265, L 950, top guide 1215, allowances 30/30, nut 30. Band as coded: 265 + 30 + 15 = 310 <= nut_z <= 1215 - 30 - 15 = 1170 z_A (z_S 370 to 1230). nut_z = tip + 136. Tips from the current params rule: park 1015, start 834.84, capture_end 184.84.

| Pose | Tip z_A | Ring bottom z_A | Nut z_A (z_S) | Anchor block z_A | Guide block z_A | Margin low | Margin high | S1-4 |
|---|---|---|---|---|---|---|---|---|
| load | 1015.00 | 1145.00 | 1151.00 (1211.00) | 265-295 | 1185-1215 | 841.00 | 19.00 | pass |
| start | 834.84 | 964.84 | 970.84 (1030.84) | 265-295 | 1185-1215 | 660.84 | 199.16 | pass |
| capture_end | 184.84 | 314.84 | 320.84 (380.84) | 265-295 | 1185-1215 | 10.84 | 849.16 | pass |
| park | 1015.00 | 1145.00 | 1151.00 (1211.00) | 265-295 | 1185-1215 | 841.00 | 19.00 | pass |

Margin low and high are also the K7 G gaps from the nut housing to the anchor top (capture_end, 10.84) and to the guide bottom (park, 19.00). Both are >= g_min 10.

Stroke and L per Q9 option. L_min is the corrected expression (item 3 of the corrections), with the anchor at 265.

| Q9 option | Park tip, current rule (max stop.start_z, core-stop plane) | Stroke | L_min | L to buy | Option R park (re-derived height_range, collar-top entry; item 9.2) | Stroke R | L_min R | L R |
|---|---|---|---|---|---|---|---|---|
| 0.5 m only | 884.84 | 700.00 | 810.84 | 820 | 959.84 | 775.00 | 885.84 | 900 |
| 0.5 and 0.75 m (stand-in) | 1015.00 | 830.16 | 941.00 | **950 (set)** | 959.84 | 775.00 | 885.84 | **900** |
| plus 1 m | 1092.50 | 907.66 | 1018.50 | 1020 | 1209.84 | 1025.00 | 1135.84 | 1140 |

The detail 1.3 formula gives 820.00 / 950.16 / 1027.66 on the current rule. The S1-4 band as coded gives 790.00 / 920.16 / 997.66. Under option R with L 900, the band is 310 to 1120 and the load and park nut is at 1095.84, so the high margin is 24.16. Option R needs one condition for the 1 m core: stop for 1 m = max(184.84, 42.5 + 1000 + 25 - 800) = 267.5, so start = 917.5 (DERIVED).

## 5. Pose table and S1-7

| Pose | Tip z expression (z_A; z_S = z_A + 60) | Cores drawn | Purpose |
|---|---|---|---|
| load | park tip (S1-2 rule; 1015.00 on the current rule) | 0.75 m install core, solid, mid-insertion: bottom at collet.core_stop_z + 0.5 (stop.collar_top_z - collet.core_stop_z) = 101.17, top 851.17 | operator lowers the core into the holder under the held ring (operator-task table) |
| start | stop.start_z[0] (834.84) | 0.75 m install core (capture core), solid, bottom on the core stop 42.5, top 792.5 | top of the 650 mm travel |
| capture_end | stop.height_z (184.84) | 0.75 m install core, solid, on the core stop, 607.66 of it above the tip | lowest ring position; S1-5a, S1-5b, S1-7 |
| park | park tip (as load) | none; captured-core removal is N6 (Quinn) | lift idle, top of the lift stroke, held by the Step 2 hold device |

The 0.5 m core appears in no figure and is not dashed. Under G2 it has no pose. It remains in `q9_length_keys` for the park and stroke report, and it is the capture core of the S1-7 B fixture. Row core_500 is deleted. Row core_750 is renamed "capture core (0.75 m install core)" with poses [load, start, capture_end]. Its `rests_on core_seat` predicate takes poses [start, capture_end]. S1-5a's neighbour (bore_ceiling, G 25, capture_end) moves to core_750: 984.84 - 792.5 = 192.34 >= 25.

| ID | Check | Z | B | Source |
|---|---|---|---|---|
| S1-7 | Capture reach from the drawn core top (G2): z_max of the core_750 patch in the start figure, minus capture_end tip z, is at least upper.drill_advance_500core | Signed spec: 792.50 - 184.84 = 607.66 >= 534.93, spare 72.73 | Fixture with the 0.5 m core as the capture core on the core stop: 542.50 - 184.84 = 357.66, short 177.27 | G2 (Design Notes 21); advance DERIVED; collet.core_stop_z ASSUMED |

## 6. TP-9 and TP-2 rulings

**TP-9, core_750 load z_rule.** z_min = collet.core_stop_z + 0.5 x (stop.collar_top_z - collet.core_stop_z) = 101.17 z_A; z_max = z_min + core.length_install = 851.17 z_A. Plane: the insertion stroke from the collar top, where the core enters the holder bore, down to the core stop, where it lands. Fraction: one half. Reason: at the half point the core reads as passing through the holder. Seated, it would read as loaded. At the collar top it would read as floating above the holder. The clearance worst case is the entry instant, core bottom at the collar top: core top 909.84, which sits 105.16 below the tip at 1015 (DERIVED). That case is reported, not drawn.

**TP-9, rubric line.** Replace "the ring is on the drill above the core in every pose" with: "the ring assembly is on the drill tube between the head and the top-end block in every pose". Per-pose predicate `ring_on_tube` (sign checks on drawn patches):
- z_min(bearing) - z_max(drill_head) > 0. Hand value 10.63 in every pose.
- z_max(drill_tube) - z_max(gear) > 0. Hand value 544.00 in every pose.

The ring assembly is rigid on the drill, so both values are constant. The predicate still fires on a figure that draws the ring off the tube in any one pose.

**TP-9, the other rubric additions.** "The 0.75 m core is dashed in the load and park poses only" becomes "the 0.75 m core is drawn solid at load (mid-insertion), start and capture_end and is absent at park; no 0.5 m core is drawn". "The motors sit on the same side of the gear in every pose" stays, with "outboard of the pinions, below the gear back face" added. Sign check: motor z_max - gear z_max < 0 (222.5 - 256 = -33.5 above tip). Motor top 222.5 sits 0.27 above the gear's lowest tooth tip 222.23, but radially apart (motor r >= 142, gear r <= 126.32), so no "below the gear" predicate is written.

**TP-2.**
- Collet: corrected to `taper narrows: up` (corrections, item 1).
- Gear: corrected. Teeth face down onto pinions mounted below the gear (Design Notes 1). Sign checks on each half-section: (a) the tooth-face edge lies below the back-face edge; (b) the tooth-face edge rises with r (dz/dr > 0; pitch-cone slope 1/3, drawn chord 0.26). Read as width against z, each half narrows downward. The draft's "narrows up" fails.
- Pinion: `narrows: inward` confirmed. The toe faces the axis and the apex lies on the drill axis at pinion-axis height.

## 7. g_min per K7 seed pair (gameplan l.146-151)

| Seed pair | Ruling | g_min | Note |
|---|---|---|---|
| Parts against the drill swept envelope at keep-out 86.2 | confirm, extend exemptions | G 0 | Exempt: core, collet (slice mode), gear hub, and now the bearing, which rides on the tube with bore = tube OD. Ring bore r 100 and gear bore r 90 clear 86.2 |
| Moving parts against fixed frame members and lift motors | confirm | G 10 | Includes nut housing against anchor block (10.84 at capture_end) and guide block (19.00 at park). Gear (r 126.32) against guide blocks (inner r 139): 3D gap 12.68, side-view box hit (LF-8) |
| Capture-core top against the bore ceiling at capture_end | change subject from the 0.5 m to the 0.75 m capture core; value confirmed | G 25 | 192.34 on these values; stop.g_stop reuse ASSUMED |
| Ring assembly at its lowest pose against the fixed base parts | confirm | G 10 | Lowest ring-assembly point is the bearing bottom 301.84, against collar top 159.84: 142.00 |
| Operator sector against screws, motors, frame (plan) | confirm | F | S2 |
| ring \| descent_stop (new) | declare | C at capture_end | Ring underside 314.84 on pad top 314.84; contact strip r 195 to 210 x 60 = 900 mm², 1.1 MPa at 1000 N |
| nut housing \| descent_stop (new) | declare | G 10 | 3D gap 10.0 (pad edge r 195 against housing r 185); side-view box hit (LF-8) |
| gear \| pinion (new) | declare | N (mesh) | Overlap in z by design at the tooth mesh |

## 8. Operator-task rows (S1), z_S = z_A + 60

| Task | Pose | Reach height and stance | Sightline | Hazard | Check or rubric |
|---|---|---|---|---|---|
| Lift a 0.75 m core (15.6 kg) into the collet under the parked ring | load | Core bottom must pass over the collar top at 219.84; core top at entry 969.84, 105.16 below the tip at 1075 (50.00 under option R). Operator stands in the S2-5 sector between two screws, torso outside the frame members (r >= 330), arms reaching about 330 to the axis with the core upright; hands 0.5 to 1.0 m | down into the holder bore from the sector, clear between the base (213) and the bearing bottom at 1192 | 15.6 kg held about 330 mm out, about 50 N m at the shoulder: a loading aid is a Step 2 row. Head at 1.5 to 1.75 m is level with the ring assembly (1192 to 1331) when leaning in, so a head strike on motors or gear is possible. Ring overhead on the power-off hold (Step 2) | S1-3, S2-5, V10 |
| Change a collet (wing nut, 230 span) beneath the ring, between screws | load | Wing nut body 157 to 213, sweep radius 115. Kneel or crouch in the sector, hands at r <= 115, reach about 215 from r 330 | wing nut from the sector at knee height | Either side of the sector: lift motors and couplings at screw azimuths (252 to 325, r 160), anchor arms (325 to 355, r 160 to 270), descent-stop pad (363 to 375, theta 150). Drill head overhead at 1075 | S1-5b, S2-5, V10 |
| Stand and watch during a cut | start to capture_end | outside the frame (r >= 400), standing | At start the cutter (894.84 to 1001.2) is in view under the ring. At capture_end the ring rim (r 210, underside 374.84) hides the cutter (244.84 to 351.2) from any eye above about 0.49 m at r 400 (DERIVED); a standing observer cannot see the end of the cut | Gear (r <= 126.3) and three pinions turn at drill.rpm 60, and the NEMA 23s (r <= 218) ride with them. The gear passes 1150.84 to 467.07 through the open operator sector: a guard or interlock is needed during the cut (Step 2 row) | K7 swept case, V10 |

## 9. Items for Sean at STOP S-1

1. **Values set (ASSUMED).** ring.position_above_tip 130. jackscrew.anchor_z 265 (anchors on the frame-member bracket, 253 above the plate). jackscrew.length 950: above the DN23 800-900 estimate, status DECLARED to ASSUMED. top_guide_z 1215. Allowances 30/30/30 unchanged. collet.core_stop_z 42.5. Lift motors placed below the anchors.
2. **Option R, height_range[1] re-derivation (decision).** Under G2 the 0.75 m capture ends at stop.height_z 184.84, so stop.height_range[1] re-derives to 184.84 and stop.start_z[1] to 834.84. The 965 term leaves the park rule. Effects:
   - Park becomes max(834.84, entry plane + 750) + 50 = 959.84, which equals params upper.park_z (U13).
   - Stroke becomes 775.00 and L_min 885.84, so the DN23 900 mm screw fits.
   - Highest point (top block at park) becomes 1969.84 z_S: margin +30.16 to the 2000 soft target, which also closes G7/H2.
   - S1-2's known-bad control (live 959.84 below 965) no longer exists. Its B changes to "park below max start".
   - params stays unchanged until Step 4. The spec park rule would read the start of each supported class instead of max(stop.start_z). Quinn owns height_range (A2b).
3. **G1 plane for loading clearance.** The core passes over the collar top while it enters the holder, so entry clearance is measured from the collar top (159.84). The core stop (42.5) is where the core lands. G1 stands for S1-3 as coded. Option R needs the collar-top plane for the park, otherwise the entering core top is 25 mm inside the drill tip.
4. **L per Q9 option.** Current rule: 820 / 950 / 1020. Option R: 900 / 900 / 1140. Values for 0.5 m only / 0.5 and 0.75 m / plus 1 m.
5. **Pose table.** The 0.75 m core is the capture core, solid at load, start and capture_end. No 0.5 m core is drawn.
6. **Rubric reword (TP-9).** "The ring assembly is on the drill tube between the head and the top-end block in every pose", predicate ring_on_tube.
7. **TP-2 corrections.** The collet narrows up. The gear teeth face down onto pinions below the gear. Both flip the draft.
8. **Notes for later steps.** A single 25 mm bearing plane has no tilt stiffness (N4, S6). The turning gear passes through the open operator sector during a cut (guard row, Step 2). The end of the cut cannot be seen by a standing observer (V10). Loading a 15.6 kg core at arm's length (Step 2 loading aid).

## 10. Gameplan lines to change

- l.121 `ring.*` seed list: replace "gear and support-ring seat" with "pinion-shaft supports (support ring); the gear mounts on the tube through `gear.hub`".
- l.146-151 g_min seeds: bearing added to the keep-out exemptions; "0.5 m core top" becomes "capture-core top"; new pairs ring|descent_stop C, nut housing|descent_stop G 10, gear|pinion N.
- l.179-183 operator-task table: S1 rows as section 8.
- l.210 "Shows": core list becomes "core (0.75 m install core as the capture core, solid at load, start and capture_end; no 0.5 m core drawn)"; lift motors "below the anchors (placeholder)".
- l.212-219 pose table: as section 5.
- l.222 "re-derives `stop.height_range[1]`": add the option R expression stop_k = max(stop.height_z, collet.core_stop_z + L_k + stop.g_stop - drill.bore_ceiling_above_tip), if Sean accepts.
- l.231 S1-4: add "with the nut housing against anchor and guide blocks at G 10".
- l.232 S1-5a: "0.5 m core top" becomes "capture-core top".
- New row S1-7 after S1-6 (section 5).
- l.237 rubric additions: lines 1 and 3 as section 6.
- l.284 detail 1.3 L formula: becomes "lift stroke + anchor allowance + guide allowance + max(nut length, ring nut-housing height) + 2 x g_min (nut housing to anchor and guide)"; The Loftsman rules at P3b.
- Detail 1.0 K8 seed (l.141): collet taper "narrows up"; gear "tooth face below the back face, rising outward".
