## Corrections to the brief

Datum A frame (plate z 0 to 12, receiver floor z 40); floor-frame part values add 40. Tags: M MEASURED (FreeCAD on the built FCStd, 7 sizes x 3 poses), D DERIVED, X DECLARED.

| # | Brief says | Built geometry says | Tag |
|---|---|---|---|
| K1 | R nut at holder + 48.0 (witness R edge 61.626, engaged 26.87) | R class C (plate top meets collar underside) gives holder + 48.745: edge 62.371, engaged 25.705 (floor 24) | M |
| K2 | holder\|nut R is C | No collar solid exists (holder.FCStd ends 104.75); built min_dist 0.60. The pose fuses a collar ring (r 55.0 to 76.2, holder z 104.75 to 110.75) into object holder: contact 9,978 mm2, collar top 159.839 / 164.376 / 152.750 | M |
| K3 | five relation rows hold | They contradict the solids; rulings in L4 | M |
| K4 | probe lacks the measures | It has them. Defects: slit_width_clamped_min samples odd slits at absolute z 5.0, reads 0.0 for a collet at z 40 (use ZMin + 5.0); "nut plate top\|holder collar underside" reads 6.005 / 6.74 with the collar (use zhi(holder) - collar.thickness) | M |
| K5 | S12 travel left at least one pitch | Probe proxy reads 9.51. Physical stop: nut thread end meets the receiver rim at z0 46.0, travel 4.01. Step 8 coupon decides | M |
| K6 | cutter is two solids | Four (ruling 2) | D |
| K7 | 16 brackets, 128 T-nuts | Cannot hold; L5 | D |

## L1 Pose generation

| Item | R | Kd1 | Kmax | Basis | Tag |
|---|---|---|---|---|---|
| core d (diametral) | d | d + 1.0 | d - 1.5 | collet.grip_window_hi / lo | D |
| collet file, z | collet_tag, 0 | _clamped_Kd1, 0 | _clamped_Kmax, 0 | foot ring on floor | D |
| holder bottom z | 13.626 | 9.0890 | 2.0000 | R seat.holder_bottom_R; K = 13.626 - (0.30 + s) / tan 10 deg, s 0.5 / 1.75 | D |
| flange to rim | 13.126 | 8.589 | 1.500 | holder z + 88 - 88.5 | M |
| ring top gap | 11.631 | 7.094 | 0.005 | F6 value + fit.model_contact_gap | M |
| nut z0 | 62.371 | 57.099 | 50.010 | R holder + 48.745 (104.75 - 56 - 0.005); K holder + 48.010 (96 - 48 + 2 x 0.005) | D |
| washer z | 110.366 | 105.094 | 98.005 | nut z0 + 47.995 | D |
| dz vs R | 0 | -5.272 | -12.361 | nut z0(P) - nut z0(R) | D |
| phi (deg) | 0 | -237.241 | -556.245 | 360 dz / L, L = 8 | D |
| nut azimuth | 77.670 | -159.571 | -478.575 | base azimuth + phi | D |
| core bottom z | 3.500 | 2.505 | 2.505 | collet z + collet.core_seat_height 2.5 + 0.005 (R lifted 1.0) | D |
| engaged_mm | 25.705 | 31.401 | 38.490 | probe zones | M |
| nut travel left | 22.295 | 16.599 | 9.510 | nut z0 - 40.5 | M |

R is the base pose of every size. Ledger fixed parts: base, frame, bracket, tnut, cutter. nut(P) = S(phi) nut(R), S = Rz(phi) T(0,0,L phi / 2 pi), right hand: clockwise (phi < 0) lowers the nut. The washer takes the nut's phi. The holder never rotates; the cone sets its z (R: collar hangs it from the nut; K: the nut pushes it through the washer until the cone seats). Collet azimuth 0. nut(R) = Rz(77.670) T(0,0,62.371): nut ridge at azimuth 0 is z0 + 4.0 - 8 phi / 360 = 0.645 mod 8, clamp flank 0.005 axial from the receiver flank (tooth 3.7 in groove 4.0 centred 0.5 mod 8; ridge phases 4.0 nut, 4.5 receiver). M: base\|nut min_dist 0.0035, overlap 0 in 21 poses. Seat keys: Kd1 = seat.holder_bottom_R - (holder.stroke_gap_R - witness.zone_high) = 9.090 (built 9.0890); Kmax = holder.bottom_above_floor_Kmax. Witness edge = nut z0 (57.099 / 50.010; R 62.371 supersedes 61.626). Object base = Compound(receiver T(0,0,40), plate I), ledger matrix I.

## L2 Core stand-in

| Item | Value | Basis | Tag |
|---|---|---|---|
| diameter | by pose, L1 | window law | D |
| length | 500 (750, 1000 recorded) | core.length_capture | D |
| bottom z | K collet z + 2.5 + 0.005; R plus pose.core_lift_R 1.0 | ledge top 2.5; collet\|core R gap 1.0 against 0.5 | M |
| top chamfer | 3.0 x 45 deg, top end only; bottom square | core.top_chamfer | X |
| azimuth reference | none; Rule P is the single-end chamfer | | D |
| axis | x = y = 0; offset 0.000, tilt 0.000 | | M |

core.py: make_core(d, length); writes parts_cache\core.FCStd (d 100) and core_result.json. Keys: core.length_capture, core.top_chamfer, core.diameters, collet.core_seat_height, fit.model_contact_gap, pose.core_lift_R.

## L3 Cutter keep-out

| Solid | Radii | z (datum A) | Basis | Tag |
|---|---|---|---|---|
| annulus | 71.4375 to 86.2 | 184.840 to 188.015 | iris.face_radius_core to drill.r_face; z_low = stop.collar_top_z + stop.g_stop; cutter.face_thickness | D |
| tube | 73.025 to 76.2 | 188.015 to 684.840 | drill.tube_id / od; top = stop.start_z[0] | D |
| funnel | cone 66.0 mouth to 56.0 throat, outer 73.025 | 188.015 to 198.015 | icd.core_lead_in_bore + icd.core_lead_in_capture; 45 deg | D |
| lead-in ring | 56.0 to 73.025 | 198.015 to 218.015 | icd.core_lead_in_bore; cutter.lead_in_height | X |

One compound named cutter; solids touch on faces. M: lead_in_bore_radius 56.0; nut\|cutter 26.469 / 31.741 / 38.830 (g_min 25); core\|cutter 3.0 minimum. cutter.py writes parts_cache\cutter.FCStd and cutter_result.json.

## L4 Frame placement and classes

| Item | Value | Basis | Tag |
|---|---|---|---|
| frame, bracket, tnut | T(0,0,-0.005), all poses | base\|frame C at gap 0.005 | D |
| receiver foot | z 0, r 40 to 80; nearest member edge x 82 | A6a contact 0.0 | D |
| frame\|bracket, frame\|tnut, bracket\|tnut | C unchanged | frame_result host overlap 0.0 | M |
| base\|bracket, base\|tnut | F unchanged | bracket z -58.5 to -1.5 | D |
| tray | identity, z 12 to 37 | output assembly only | D |
| foot x4 | +x end T(262, +-274, -68); -x end Rz(180) T(-262, -+274, -68) | rail covers local x 0 to 60 | D |
| stop, plug, caddy, gauge, rest | stop identity; plug (-172, 0); others at their interface planes, 100 mm off the frame | context views | X |

ASSEMBLY.md changes (step7_class_rulings.md, Topologist sign). With them R, Kd1, Kmax fire no gate (M).

| Row | Change | Reason | Tag |
|---|---|---|---|
| base\|holder | g_min 1.5 to 0.12 | key in slot (12.0 - 11.75) / 2 = 0.125 | M |
| holder\|collet R | g_min 0.30 to 0.29 | 0.30 x cos 10 deg = 0.2954 normal | M |
| holder\|nut K | g_min 0.75 to 0.50 | flange top to pad bottom = washer proud 0.5 (0.51) | M |
| nut\|washer | C to P: overlap at most 2.45, min_dist 0 +- 0.01 | press pads, 2.40 designed, 2.387 built | M |
| feature "nut collar top\|cutter" | Class_R G to F (gap above 0) | R unclamped: 20.464; K 25.001 / 32.090 keep "at least 25" | M |

## L5 C6 resolution

| Item | Value | Basis | Tag |
|---|---|---|---|
| rail inner face need | 4 x 57 + 4 x 68 + 2 x 60 + 2 x 60 = 740 against 644 | gap x 142 to 202 is 60: one 57 bracket | D |
| (b) | rejected | other faces are horizontal; an L needs two perpendicular contacts on its concave side | D |
| (c) | rejected | 980 stock, footprint 644 (P6b) and P3 change | D |
| (d) | rejected | 18,249 mm3 is interpenetration | D |
| (a) chosen | delete bracket_printed_1 to 4 (x 142 to 210) | 12 brackets (8 purchased, 4 printed at x +-82), 96 T-nuts, 8 per bracket as built | D |
| after | no pair above 0.01 mm3 (96 touching pairs); before 18,248.6 x 4, 1,061.4 x 4, 16,523.2 | frame.FCStd copy without those 4 brackets and tnut_65 to 96 | M |
| stock | 644, 488, 468 unchanged; P3 holds | | D |
| tests | FR2 12, FR3 96, printed 4; test_step6_parts line 218 formula; step7 lines 129, 145, 146 (6 / 12 / 96) | | D |

Printed names renumber: bracket_printed_1 to 4 are old 5 to 8 (corners (+-82, +-244)); tnut_1 to 96. Joint capacity with one inboard printed bracket per support end is DECLARED; Step 12 reviews.

## L6 Measures

| Measure | Equation on built features | Value | Bound | Tag |
|---|---|---|---|---|
| core_axis_offset | core section centroid at collet mid-height | 0.000 | icd.core_axis_offset_max 0.805 | M |
| clamped_tilt_deg | atan(centroid shift / dz) | 0.000 | register.clamped_tilt_max_deg 0.573 | M |
| lead_in_clearance | min Z cylinder radius of cutter 56.0 - core radius | 3.5 to 11.0 | icd.core_lead_in_clearance_min 2.055 | M |
| funnel_capture_radius | max Z cone rim 66.0 - core radius | 13.5 to 21.0 | icd.core_lead_in_capture_min 9.31 | M |
| receiver_underside_contact_mm2 | base down faces r < 80 within 0.01 of frame | 0.0 (face 15,080) | zero | D |
| frame_footprint_x / y | frame bbox | 644.0 / 608.0 | icd.footprint_x / y | M |
| slit_width_clamped_min | collet result clamped.slit_width | 1.2382 / 0.5837 | collet.min_slit_clamped 0.5 | M |
| nut_travel_left_mm | min(zone bottoms, skirt above floor) | L1 | thread.pitch 8 | M |
| nut_tilt_deg, holder_tilt_deg | largest cylinder axis | 0.000 | register.tilt_limit_deg 1.021 | M |
| fit_spigot_hole | r 80.2 plate-hole face - r 80.0 receiver face | 0.200 | chain[1] 0.20 | D |
| fit_plate_key_stop_pin | max((pocket 12.0 - base.key_width) / 2, pin gap) | 0.250 | chain[0] 0.32 | D |

Base keeps receiver and plate as two solids (0.2 radial gap), so both Z-axis cylinder faces exist. Sum 0.45 against icd.coaxiality_budget 1.0. Column foot and carriage guide: green_at_12.

## L7 Wrong states (nominal 100 mm, Kd1 unless stated)

| WS | Transform (datum A) | Fires (M) |
|---|---|---|
| 1 | collet Rx(+180) about (0,0,56.0) | A1 base\|collet 66.5 mm3; F1 18,682 mm3 |
| 2 | holder Rx(+180) about (0,0,101.464) | A1 base\|holder contact 25,297 mm2; A3 holder bottom 3.089 vs 9.090 |
| 3 | nut Rx(+180) about (0,0,125.099) | A1 nut\|washer min_dist 1.04; A3 engaged 16.797 below 24; T1 silent |
| 4 | nut mirror y to -y (improper) | T1 base\|nut 4,079.7 mm3 |
| 5 | nut Rx(+2.0) about (0,0,125.099) | T9 tilt 2.000 above 1.021; T1 878.8 mm3 |
| 6 | collet_090p0_clamped_Kd1 at z 0 | F3 collet\|core 29,236 mm3 |
| 7 | collet T(0,0,+3.0) | A1 base\|collet min_dist 0.125; F1 4,571 mm3 |
| 8 Kmax | holder T(0,0,-1.5) | A1 base\|holder contact 6,615 mm2; A3 holder bottom 0.500 vs 2.000 |
| 9 Kmax | nut and washer S(phi), dz -13.510, phi -607.95 | A1 / T1 base\|nut 57,157 mm3 |
| 10 | base Rx(+180) about (0,0,6.0) | A1 base\|collet min_dist 28.0; A3 holder bottom 37.089 |
| 11 | collet Rz(-15) about the axis | A1 base\|collet 66.5 mm3 |

Each state fires an expected gate and nothing outside the six.

## L8 Clamp range (T5)

| Quantity | d 90 R | d 105 R | d 90 Kmax | d 105 Kmax | Basis |
|---|---|---|---|---|---|
| free bore (diametral) | 92.0 | 107.0 | | | d + core.tol + collet.c_i |
| core | 90 | 105 | 88.5 | 103.5 | L1 |
| clamped bore radius | | | 44.255 | 51.755 | core / 2 + 0.005 |
| slit width | | | 0.5837 | 0.5837 | above 0.5 |
| engaged | 25.705 | 25.705 | 38.490 | 38.490 | independent of d |
| nut travel left | 22.295 | 22.295 | 9.510 | 9.510 | at least 8 |
| flange gap to rim | 13.126 | 13.126 | 1.500 | 1.500 | above 0 |

## Params keys to add

| Key | Value | Source | Status |
|---|---|---|---|
| pose.core_lift_R | 1.0 mm | R core above ledge | DECLARED |
| pose.nut_over_holder_K / _R | 48.010 / 48.745 mm | L1 formulas | DERIVED |
| pose.nut_phi_R_deg | 77.670 | ridge 0.645 mod 8 | DERIVED |
| pose.washer_z_in_nut | 47.995 mm | nut.length - fit.model_contact_gap | DERIVED |
| pose.frame_dz | -0.005 mm | -fit.model_contact_gap | DERIVED |
| collar.thickness | 6.0 mm | collar.top_above_plate - nut.lift_play | DERIVED |
| core.top_chamfer | 3.0 mm | L2 | DECLARED |
| cutter.face_thickness / lead_in_height | 3.175 / 20.0 mm | drill.tube_wall / L3 | DERIVED / DECLARED |
| base.key_width, pin_dia, pin_x | 11.5, 6.0, 247 mm | Step 6 BS4 | DECLARED |
| hardware.printed_brackets_per_joint | 1 | L5 | ASSUMED |
| nut.pad_overlap_max | 2.45 mm3 | 2.40 designed + 0.05 | ASSUMED |

## Files

Rebuilt: parts_cache\frame.FCStd and frame_result.json (frame.py drops the support-outer-face bracket loop). bracket_purchased, bracket_printed, tnut: not rebuilt, mtimes kept. Created: core.py to core.FCStd; cutter.py to cutter.FCStd; assemble.py to parts_cache\assembly\pose_*.FCStd and results\assembly_poses.json; assemble_ws.py to ws*.FCStd. The collar ring is built in assemble.py and fused into the pose holder; holder.FCStd is untouched. Edits: ASSEMBLY.md rows, params.yaml, the tests named in L5.

## Revision 1

### Corrections to the brief

| # | Brief or earlier line says | Now | Tag |
|---|---|---|---|
| V1 | K2: pose fuses the collar | Withdrawn. Collar goes into holder.py; assemble.py adds no geometry | D |
| V2 | Candidates: longer receiver thread, shorter nut skirt | Neither restores travel. Travel at Kmax = flange gap 1.5 + 8 - nut.length 48 + U (full-groove top 42.5) = 4.0. A shorter skirt moves z0 and U together; a longer receiver lowers travel; a shorter receiver gains at most 1.7 before R engaged falls under 24 | D |
| V3 | K5 physical stop 4.01 | Cause: the nut groove runs out helically; no full turn above nut z 42.5. Fix: nut thread relief | M |

### Holder collar (holder.py, holder.FCStd)

| Item | Value | Basis | Tag |
|---|---|---|---|
| ring | r 55.0 to 76.2 | collar.id / 2 (params 110.0, not 114.0) to collar.od / 2 | D |
| z | z_top 104.75 to 110.75 | z_top = existing dims()["z_top"]; collar.thickness = collar.top_above_plate 6.75 - nut.lift_play 0.75 = 6.0 | D |
| join | ring fused with the key tool before the one Fuse boolean ("Key" becomes "KeyCollar"); the tube-top annulus r 56.75 to 67.04 is the shared face | fuse first, boolean once | D |
| insert holes | each insert tool gains a collar.hole_dia 6.6 cylinder from z_top to z_top + 6 + overshoot, same Cut | the 1 mm insert overshoot would otherwise leave 1 mm blind pockets in the collar | D |

holder_result.json adds collar radii, z span and hole count; "holder top height 104.75" keeps meaning (tube top). Pose probe: collar underside = lowest down-facing planar face of holder with r above 68.04 above the flange; collar_top_z = zhi(holder) (159.839 / 164.376 / 152.750). Trial fuse M: holder\|nut R contact 9,978 mm2.

### Nut thread relief (nut.py, nut.FCStd)

| Item | Value | Basis | Tag |
|---|---|---|---|
| relief | plain bore r 75.34, nut z 42.0 to 48.5 (plate underside) | nut.relief_r = thread.major / 2 + fit.c_r + 0.2; nut.relief_z 42.0 = full-groove top 42.5 - 0.5 | D |
| volume removed | 6,364 mm3 of 358,838; one solid, valid | trial cut | M |
| stop | rim meets plate underside at z0 40.0 (overlap 0.000 at 40.0, 110 mm3 at 39.8) | | M |
| travel left, Kmax | 50.010 - 40.0 = 10.01 (was 4.01) | requirement 8.0 | M |

Tool joins the existing fused cut list (no new boolean).

Consequences, all M unless stated:
- Engaged 25.705 / 31.401 / 38.490 unchanged (nut zone top stays above the rim at every pose).
- Witness ruler: receiver, nut z0 and reading plane unchanged; edge readings 50.00 and 57.09 stand.
- T9: 1.5 x D x tan(0.596 + 0.315 deg) = 2.379 against P/2 = 4.000 unchanged (no input moves, D). Engineer re-runs probe_tilt.py and probe_thread_mesh.py.
- Receiver BOP: receiver not rebuilt, record unchanged.
- Numbers that move: nut volume, faces, Euler; holder volume (+51,600 mm3), bbox zmax 104.75 to 110.75, Euler; BOM mass rows; step3_parts and step6_parts probe JSON refresh.
- The probe measure nut_travel_left_mm is replaced by nut_stop_travel_mm: lower the nut along S(phi) in 0.25 mm steps to the first base|nut common volume of 0.01 mm3 or more; expected 10.01; bad control = unrelieved nut, 4.01.

### Contract rows (Systems Engineer)

| Row | Final text |
|---|---|
| holder\|nut K | g_min 0.50 = washer.thickness 1.3 - nut.washer_pocket_depth 0.8 + 0.01 stack gaps (built 0.51) |
| nut\|washer | class P, overlap 2.0 to 2.45 mm3 (nut.pad_overlap_min / max; built 2.387), legend entry in ASSEMBLY.md |
| nut collar top\|cutter | G, minima 0 at R, 25 at Kd1 and Kmax (25.001 / 32.090); parser takes per-pose minima |

### Params and rebuilds

New keys: collar.thickness 6.0, collar.hole_dia 6.6 (DECLARED), nut.relief_z 42.0, nut.relief_r 75.34 (DERIVED), nut.pad_overlap_min 2.0 (ASSUMED). Changed values: none. Rebuild: holder.FCStd (authorized) and nut.FCStd (needs a Manager entry in step7_rebuild_authorizations.md); both re-signed by the Topologist. Receiver, washer, collets untouched.
