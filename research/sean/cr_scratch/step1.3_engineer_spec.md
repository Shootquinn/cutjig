## Corrections to the brief

1. **Tr12x3 moves no chain leaf.** The P0L note says the Tr12x3 change "must move anchor_z, length, top_guide_z and both member leaves in one overlay edit". Loftsman P0L NOTE 1 reads "any change to anchor_z, length or block height must carry top_guide_z and both member leaves". The rulings leave anchor_z 265, length 900 and the block 30 tall (anchor_allowance 30), so none of the five keys moves. K2 on the edited overlay: 166 leaves, 20 expr leaves agree within 0.05 (MEASURED). S1-4 0.84, L 900, top_guide_z 1165 and member tops 1225 are unchanged (DERIVED).
2. **The next S2 revision is r9, not r6.** The Designer wrote "S2 r6". S2 is at r8 in wip/, so the key-driven S2 revision is r9 (MEASURED, wip/ listing).
3. **The anchor-row spec edit in S1 and S2 cannot land before P6.** Dry run: anchor_a/_b (S1) and anchor_a/_b/_c (S2) moved to the 42-square radial place, and bracket_anchor r_in moved to `pitch_radius + anchor_block_width / 2`. Result: controls Z 73/75, B 193/208 (MEASURED). K5-Z3 and K7-Z15 (live S2) fire. K5-B7 to B11, B13 to B18, B21 and B24 show 3 extra issues each from the S2 anchor circles. K7-B33 fires 24 against 12 planted, and K7-B19 (live S1) gives a different reason. The edit is reverted. S1 and S2 take the square at P6 together with their script redraw. The S3 anchor_a/_b/_c rows carry `x1_exempt` with that reason. bracket_anchor_c keeps the S2 expression (`nut_flange_od / 2`, 181, same value).
4. **The screw bar "255 to 1155" (Designer section 3) conflicts with the shared screw z_rule.** The screw z_rule is anchor_z to top_guide_z (265 to 1165) in S1, S2 and S3 (X1). The spec keeps the shared envelope. The end below the anchor is a separate row, screw_end_c (d 8, 253.5 to 265 z_A).
5. **The coupling stack does not close.** The NEMA 17 shaft runs 24 from the motor face at 240 and ends at 264.00 z_A. That is 0.50 above the coupling top (263.5) and 1.00 below the block underside (DERIVED). In a 20-long coupling the motor shaft (240 to 264) and the screw end (253.5 to 265) overlap by 10.50. K7 will read liftmotor_shaft_c|screw_end_c as interference. Open item 5.
6. **Four nut and anchor values are missing from both sources.** `jackscrew.nut_body_od` and `jackscrew.nut_flange_thickness` are missing. The Designer's shape text needs them for the floating-nut section (body step, float gap, flange). The spec names both keys with no overlay leaf, so K2 on s3 reads red until they are supplied (MEASURED: "spec key jackscrew.nut_body_od resolves in neither params.yaml nor the overlay", and the same for nut_flange_thickness). The anti-rotation pin, the M10x1 locknut and the nut retaining ring have no leaf. They are `not_drawn` with that reason.
7. **Rounding against the Designer's values.** The stall margin at K 0.7 is 3.97 (Designer 3.98). WOB is 1267.43 / 1084.54 N (Designer 1267.1 / 1083.3). Capture-lift torque at mu 0.15 is 0.149 N m; the Designer quoted 0.181, which is the mu 0.20 end (DERIVED). The differences come from eta rounding. No conclusion changes.
8. **S1 r7 certifies two fewer chain pairs than the Designer's section 11 shows.** core_750|core_seat is undeclared F in s1_checks_r7.json (states undeclared:C, undeclared:F). drill_head|drill_tube is undeclared F in both s1_checks_r7.json and s2_checks_r5.json (MEASURED from the K7 records). S3 declares core_750|core_seat C at capture_end, so this figure certifies it. drill_head|drill_tube is declared and left to S6-5.
9. **check_stack read the screw-block g_min from letters a and b only.** S3 declares nut_housing_c|anchor_c and |guide_c, so `reported()` raised a KeyError on `g_min_screw_block`. The loop now reads a, b and c. S1 and S2 have no c pair, so their reported values do not move.

## 1 Files changed

| File | Change |
|---|---|
| docs/sketches/proposed_params.yaml | Overlay edit (table below) |
| docs/sketches/s3_spec.yaml | New: 63 rows, 1624 lines; header with view section_yz, inset, section convention, pose table, load cases, s3_checks, chains, reported_items, part list, not_drawn, figure_note |
| docs/sketches/checks_s3.py | New skeleton: S3-1, S3-2 (threshold form), S3-3 (fail-closed until P4), load and Euler arithmetic, `reported(ctx)` for RPT, STUB_EXPECT, STUB_CAUSE, SOURCES, K_CHECKS |
| docs/sketches/check_stack.py | l.604: screw-block g_min letters `("a", "b", "c")` (Correction 9) |
| docs/sketches/s1_spec.yaml | `mark: {sub: line, z: "jackscrew.anchor_z + jackscrew.anchor_allowance / 2", source: ...}` on anchor_a and anchor_b (Topologist P0T section 4; clause and controls at P4, drawn at P6). No other S1 change |

Overlay, changed leaves (source "Sean STOP S3-A, Design Notes 31" or "Designer 1.3 (a)" in each):

| Key | Old | New | Status |
|---|---|---|---|
| jackscrew.nominal | 8 (DECLARED [DN23]) | 12 | ASSUMED |
| jackscrew.lead | 8 | 3 | ASSUMED |
| jackscrew.root_diameter | 6.2 | 8.5 | ASSUMED |
| jackscrew.efficiency | 0.6 | 0.33 (0.364 to 0.299 over mu) | DERIVED |
| ring.nut_mounting | rigid K 1.0 / floating K 2.0 | floating, 0.5 radial, axially clamped, pinned; K 0.7 on L_t | ASSUMED |
| hold.device | open | self-locking Tr12x3 lead (drawn); brake, park pin as options | ASSUMED |
| jackscrew.anchor_allowance, guide_allowance, nut_flange_od, liftmotor.coupling_length | values unchanged | source text (basis stated) | ASSUMED |

New leaves: jackscrew.starts 1, mean_diameter 10.5 (expr), thread_half_angle 15, thread_mu [0.15, 0.2], youngs_modulus 200000, density 7850, end_factor_floating 0.7, end_factor_rigid 0.5, buckling_sf 3, anchor_block_width 42, anchor_bearing (text), anchor_bearing_count 2, anchor_bearing_od 26, anchor_bearing_width 8, anchor_bearing_z 280 (expr), journal_d 10, guide_block_od 42, guide_bearing (text), guide_bearing_od 26, guide_bearing_width 8, guide_bearing_z 1150 (expr); ring.nut_float 0.5; liftmotor.shaft_od 5, shaft_length 24, pilot [22, 2], bolt_pattern 31, standoff (text), standoff_af 5.5, coupling (text), coupling_od 19, coupling_height 20, screw_end_d 8, mass 0.35; liftsync.method, home_switch (text), switch_r_in 190, switch_r_out 210, switch_height 13, switch_width 6; liftload.f_bind 300, rapid_speed 25; bearing.mass 1.5, pinion.mass 0.5, gear.hub_mass 0.7, guide.bushing_mass 0.2. All are ASSUMED except the three expr leaves (DERIVED). The Designer's single `end_factor` map is split into two numeric leaves, because a dict value cannot be evaluated by check_stack. liftmotor.standoff_af 5.5 (M3 hex across flats) is a working value for the elevation width of standoffs_c. The Designer gave no number for it: open item 6.

## 2 Part list

Every part a `shape` string names has a row, a sub-artist or a `not_drawn` entry (spec `part_list`, 28 entries).

| Part | Row |
|---|---|
| base frame rails cut across (slot notches, centre bore lines) | base_frame |
| base plate with spigot-hole gap | base_plate |
| receiver, collet, core seat, holder (S4 stand-in), wing nut, collar, capture core | receiver, collet, core_seat, holder, wingnut, collar, core_750 |
| drill head (cutter ticks), tube walls, top-end block | drill_head, drill_tube, drill_top_block |
| keep-out lines / inset circle | keepout |
| ring plate pieces; nut-housing boss c; floating nut c | ring, nut_housing_c, nut_c |
| drill-to-ring bearing, gear, gear hub | bearing, gear, gear_hub |
| pinion c, NEMA 23 c, its shaft, mount, pinion axis | pinion_c, motor23_c, motor_shaft_c, motor_mount_c, pinion_axis_c |
| screw c (thread ticks), screw end | screw_c, screw_end_c |
| anchor block, angular-contact pair, balls, bearing line | anchor_c, anchor_bearing_c (sub-artists balls, line) |
| top-guide block, radial bearing, balls | guide_c, guide_bearing_c (sub-artist balls) |
| bracket arms c; member c | bracket_anchor_c, bracket_guide_c, frame_upper_c |
| NEMA 17 c, pilot, shaft; beam coupling; rear standoffs | liftmotor_c, liftmotor_pilot_c, liftmotor_shaft_c, coupling_c, standoffs_c |
| home switch c and lever | home_switch_c (sub-artist lever) |
| hold callout; nut stations; L_t dimension; load arrows | hold_callout, nut_station_start, nut_station_park, span_lt, load_cut, load_tension_c, load_comp_c |
| inset: screws, housings, blocks, lift motors, members, switches a, b, c | screw_a/_b/_c, nut_housing_a/_b/_c, anchor_a/_b/_c, liftmotor_a/_b/_c, frame_upper_a/_b/_c, home_switch_a/_b/_c |
| inset: controller callout, ring OD reference, A-A line, axes and theta arc | sync_callout, ring_ref, section_line, plan_axes |
| not drawn | screw a set (beyond), screw b set (in front), pinions a and b, NEMA 23 a and b, guide rods with lugs, housings and ties, descent-stop pad and post, base-frame end members and supports, front M3 standoffs, anchor locknut, nut retaining ring, anti-rotation pin |

figure_note: "Not drawn: screw a set (beyond); screw b set (in front); pinions a and b; NEMA 23 a and b; guide rods, lugs, housings and ties; descent-stop pad and post (beyond); base-frame end members and plate supports; front M3 standoffs; anchor locknut; nut retaining ring; anti-rotation pin. Hatch: aluminium, extrusion, steel, brass, plastic (legend)."

## 3 Row table

View section_yz: section A-A, plane x = 0, viewer at +X looking toward -X, u = +Y right, z up, plotted z_S. Inset plan_xy: +X right, +Y up, x and y -340 to 340, upper right, at least 0.3 of the figure height. Axes: S = section, I = inset. The extents are check_stack place or plan_poly x and u (= y) at capture_end. z is z_S: one band for fixed rows, and load / start / capture_end / park for moving rows. The drawn pose is capture_end (MEASURED, check_stack on s3_spec.yaml).

| Row | Axes | Section class | Extents (mm) | z band z_S |
|---|---|---|---|---|
| floor | S | reference | - | 0.00-0.00 |
| base_frame | S | cut (section_u u +-244 to +-304) | x -322..322, u -304..304 | 0.00-60.00 |
| base_plate | S | cut (u -239..-80.2, 80.2..239) | x -322..322, u -304..304 | 60.00-72.00 |
| receiver | S | cut | axis | 72.00-188.50 |
| collet | S | cut | axis | 100.00-132.00 |
| core_seat | S | cut | axis | 100.00-102.50 |
| holder | S | cut | axis | 109.09-205.09 |
| wingnut | S | unsectioned | axis | 157.09-213.09 |
| collar | S | cut | axis | 213.09-219.84 |
| core_750 | S | unsectioned | axis | 102.50-852.50 (capture_end only) |
| drill_head | S | unsectioned | u -88.90..88.90 | 1019.84-1126.21 / 894.84-1001.21 / 244.84-351.21 / 1019.84-1126.21 |
| drill_tube | S | cut (walls tube_id / 2 to 76.2) | u -76.20..76.20 | 1126.21-1819.84 / 1001.21-1694.84 / 351.21-1044.84 / 1126.21-1819.84 |
| drill_top_block | S | unsectioned | u -76.20..76.20 | 1819.84-1969.84 / 1694.84-1844.84 / 1044.84-1194.84 / 1819.84-1969.84 |
| keepout | S, I | reference | u -86.20..86.20 | 100.00-1969.84 / 100.00-1844.84 / 100.00-1194.84 / 100.00-1969.84 |
| ring | S | cut (u -210..-185, -135..-100, 100..210) | - | 1149.84-1161.84 / 1024.84-1036.84 / 374.84-386.84 / 1149.84-1161.84 |
| nut_housing_c | S, I | cut | x -25..25, u -185..-135 | 1140.84-1170.84 / 1015.84-1045.84 / 365.84-395.84 / 1140.84-1170.84 |
| nut_c | S | cut | x -21..21, u -181..-139 | 1140.84-1170.84 / 1015.84-1045.84 / 365.84-395.84 / 1140.84-1170.84 |
| bearing | S | cut | axis | 1136.84-1161.84 / 1011.84-1036.84 / 361.84-386.84 / 1136.84-1161.84 |
| gear, gear_hub | S | cut | axis | 1242.07-1275.84 / 1117.07-1150.84 / 467.07-500.84 / 1242.07-1275.84 |
| pinion_c | S | cut | x -45.62..45.62, u 95.22..140.00 | 1168.22-1259.46 / 1043.22-1134.46 / 393.22-484.46 / 1168.22-1259.46 |
| motor23_c | S | cut | x -28.5..28.5, u 142..218 | 1185.34-1242.34 / 1060.34-1117.34 / 410.34-467.34 / 1185.34-1242.34 |
| motor_shaft_c | S | unsectioned | u 121..142 | 1209.84-1217.84 / ... / 434.84-442.84 / ... |
| motor_mount_c | S | cut | u 142..210 | 1161.84-1185.34 / 1036.84-1060.34 / 386.84-410.34 / 1161.84-1185.34 |
| pinion_axis_c | S | reference | u 95.22..218 | 1213.84 / 1088.84 / 438.84 / 1213.84 |
| screw_c | S, I | unsectioned | x -6..6, u -166..-154 | 325.00-1225.00 |
| screw_end_c | S | unsectioned | u -164..-156 | 313.50-325.00 |
| anchor_c | S, I | cut (42 square, bore 26) | x -21..21, u -181..-139 | 325.00-355.00 |
| anchor_bearing_c | S | cut (two 10 x 26 x 8) | u -173..-147 | 332.00-348.00 (line 340.00) |
| guide_c | S | cut (bore 26) | u -181..-139 | 1195.00-1225.00 |
| guide_bearing_c | S | cut | u -173..-147 | 1206.00-1214.00 (line 1210.00) |
| bracket_anchor_c | S | cut | u -244..-181 | 325.00-355.00 |
| bracket_guide_c | S | cut | u -244..-181 | 1195.00-1225.00 |
| frame_upper_c | S, I | cut | x -30..30, u -304..-244 | 60.00-1285.00 |
| liftmotor_c | S, I | cut | u -189.70..-130.30 (footprint r 29.70) | 252.00-300.00 |
| liftmotor_pilot_c | S | cut | u -171..-149 | 300.00-302.00 |
| liftmotor_shaft_c | S | unsectioned | u -162.5..-157.5 | 300.00-324.00 |
| coupling_c | S | unsectioned | u -169.5..-150.5 | 303.50-323.50 |
| standoffs_c | S | beyond | x -18.25..-12.75, u -178.25..-141.75 | 300.00-325.00 |
| home_switch_c | S, I | cut | x -3..3, u -210..-190 | 1182.00-1195.00 |
| screw_a / screw_b | I | - | x -144.56..-132.56 / 132.56..144.56, y 74..86 | 325.00-1225.00 |
| nut_housing_a / _b | I | - | x -163.56..-113.56 / 113.56..163.56, y 55..105 | moving, as nut_housing_c |
| anchor_a / _b | I | - | x -167.25..-109.88 / 109.88..167.25, y 51.31..108.69 | 325.00-355.00 |
| liftmotor_a / _b | I | - | x -168.26..-108.87 / 108.87..168.26, y 50.30..109.70 | 252.00-300.00 |
| frame_upper_a / _b | I | - | x -278.27..-196.31 / 196.31..278.27, y 96.02..177.98 | 72.00-1285.00 |
| home_switch_a / _b | I | - | x -183.37..-163.04 / 163.04..183.37, y 92.40..107.60 | 1182.00-1195.00 |
| ring_ref | I | reference | r 210 | moving, as ring |
| section_line | I | reference | x 0, y -304..304 | - |
| plan_axes, sync_callout | I | reference / callout | - | - |
| hold_callout | S | callout | leader to screw_c | - |
| nut_station_start / _park | S | reference | u -185..-135 | 1030.84 / 1155.84 |
| span_lt | S | reference | u -160 | 340.00-1210.00 |
| load_cut | S | arrow +Z | axis | moving with the head |
| load_tension_c | S | arrow (apart) | screw c | 340.00 to nut bottom (365.84 at capture_end) |
| load_comp_c | S | arrow -Z | housing c top | 395.84-425.84 at capture_end |

## 4 Load cases; S3-2 and S3-3 hand against computed

Inputs (ASSUMED, Design Notes 31): E 200000 N/mm², d_r 8.5, d2 10.5, lead 3, one start, flank 15 deg, mu 0.15 to 0.20, T 0.45 N m, SF 3, F_bind 300 N, rapid 25 mm/s, density 7850. W = 6 + 8 + 3 + 3 x 1.0 + 3 x 0.05 + 1.5 + 3 x 0.5 + 0.7 + 2 x 0.2 = 24.25 kg, 237.89 N. "Hand" means a stand-alone scratch script with no harness import. "Computed" means checks_s3.reported on s3_spec.yaml with check_stack. Both are DERIVED; they agree at the printed precision.

| Quantity | Hand | Computed |
|---|---|---|
| L_min per Q9 option (0.5; 0.5 and 0.75; plus 1 m) | 885.00 / 885.00 / 1135.00; 885.84 / 885.84 / 1135.84 at anchor_z | same (check_stack q9_options) |
| L_t, bearing line to bearing line | 1150 - 280 = 870.00 | 870.00 |
| Nut-to-anchor segment at park | 1095.84 - 280 = 815.84 | 815.84 |
| I | pi 8.5⁴ / 64 = 256.24 mm⁴ | 256.24 |
| P_cr floating K 0.7, L_t | 1363.8 N | 1363.8 |
| P_cr floating K 1.0, L_t | 668.2 N | 668.2 |
| P_cr rigid K 0.5, 815.84 | 3039.7 N | 3039.7 |
| P_cr rigid K 1.0, 815.84 | 759.9 N | 759.9 |
| lambda; phi_n (mu 0.15 / 0.20) | 5.20 deg; 8.83 / 11.70 deg | same |
| eta (mu 0.15 / 0.20) | 0.3641 / 0.2994 | same |
| F_stall per screw / total | 343.18 / 1029.54 N; 282.21 / 846.64 N | same |
| Back-drive efficiency | -0.698 / -1.253 (self-locking) | same |
| WOB max (F_stall + W) | 1267.43 / 1084.54 N | same |
| Lift torque per screw, cut / capture lift | 0.333 / 0.149 (mu 0.15); 0.405 / 0.181 N m (mu 0.20) against 0.45 | same |
| Critical speed over L_t | 1336 rpm pinned-pinned (2.67 x), 2086 rpm fixed-pinned (4.17 x) against 500 rpm | same |
| Tension segment per S1 pose (nut centre - 280) | load 815.84, start 690.84, capture_end 40.84, park 815.84 | needs drawing (RPT absent until (d)) |

Per-screw forces and S3-2 margins (floating, K 0.7, L_t 870, P_cr 1363.8 N; SF 3):

| Case | Total (N) | Per screw | Two-screw | Segment below nut | P_cr / F per screw | Two-screw |
|---|---|---|---|---|---|---|
| Static | 237.89 down | 79.30 | 118.95 | compression | 17.20 | 11.47 |
| Capture lift (+ 10.4 kg) | 339.92 | 113.31 | 169.96 | compression | 12.04 | 8.02 |
| Retract with bind (+ 300) | 537.89 | 179.30 (cap 343.18) | 268.95 | compression | 7.61 | 5.07 |
| Cut 1000 N | 762.11 | 254.04 | 381.05 | tension, 4.48 MPa on 56.75 mm² | - | - |
| Stall down | 1029.54 / 846.64 | 343.18 / 282.21 | - | tension | - | - |
| Stall up | 1029.54 / 846.64 | 343.18 / 282.21 | - | compression | **3.97** (least) | - |

S3-2 passes SF 3 in every case at K 0.7: least margin 3.97 at stall up (DERIVED). At K 1.0 the stall reads 1.95, so the pass rests on the fixed-anchor credit (Design Notes 31). Kept parts (collet, holder, receiver, base plate): 1000 N at the cut, 1267.43 / 1084.54 N at F_stall + W (N5, B2-7).

S3-3 hand: chain screw c has 18 pairs. 15 are certified (by S1 r7, S2 r5 or this figure), 2 are declared (bearing|tube, tube|head; drawn at S6) and 1 is uncertified (cutter|core) (section 5).

## 5 S3-3 chains and certifying records

Pair ids are as written in the K7 records, MEASURED from docs/sketches/s1_checks_r7.json and s2_checks_r5.json (all four poses). "S3" means this figure's K7 at (d).

Screw c: drill_head, core_750, core_seat, collet, holder, receiver, base_plate, base_frame, frame_upper_c, bracket_anchor_c, anchor_c, anchor_bearing_c, screw_c, nut_c, nut_housing_c, ring, bearing, drill_tube, drill_head.

| Pair | Certifier |
|---|---|
| drill_head \| core_750 | **none**. S1 r7 has core_750\|drill_head as N / undeclared F; no record holds it as C |
| core_750 \| core_seat | S3 (declared C at capture_end here). S1 r7 has core_seat\|core_750 as undeclared F |
| core_seat \| collet | S1 r7 collet\|core_seat C |
| collet \| holder | S1 r7 collet\|holder C |
| holder \| receiver | S1 r7 receiver\|holder C |
| receiver \| base_plate | S1 r7 base_plate\|receiver C; S3 |
| base_plate \| base_frame | S1 r7 base_frame\|base_plate C; S2 r5 base_plate\|base_frame z-contact (not at x = 0) |
| base_frame \| frame_upper_c | S2 r5 frame_upper_c\|base_frame z-contact; S3 |
| frame_upper_c \| bracket_anchor_c | S2 r5 bracket_anchor_c\|frame_upper_c plan-contact; S3 |
| bracket_anchor_c \| anchor_c | S2 r5 bracket_anchor_c\|anchor_c plan-contact (round r 21 block; r9 re-certifies the square); S3 |
| anchor_c \| anchor_bearing_c; anchor_bearing_c \| screw_c; screw_c \| nut_c; nut_c \| nut_housing_c; nut_housing_c \| ring | S3 only (S1/S2 declare the screw-set pairs N) |
| ring \| bearing | S1 r7 ring\|bearing C; S2 r5 plan-contact; S3 |
| bearing \| drill_tube | S1 r7 drill_tube\|bearing C; S2 r5 plan-contact; declared (S6-5) |
| drill_tube \| drill_head | declared (S3 declares C; S6-5 draws it). Undeclared F in S1 r7 and S2 r5 |

Screws a, b: base_plate\|frame_upper_k (S1 r7 C, S2 r5 z-contact), frame_upper_k\|bracket_anchor_k and bracket_anchor_k\|anchor_k (S1 r7 and S2 r5 plan-contact) are certified.

**Uncertified pairs:**
1. drill_head\|core_750 on all three chains (cut contact; no record declares it C).
2. anchor_k\|screw_k, screw_k\|nut_k, nut_k\|nut_housing_k and nut_housing_k\|ring for k = a, b (8 pairs). S1 and S2 declare them N. S3 certifies screw c only. "By symmetry" needs a premise lint (rows a, b, c equal in z_rule and place up to theta), which does not exist yet (Topologist 1.2 (c) NOTE 1).
3. drill_tube\|drill_head and bearing\|drill_tube are declared only, as detail 1.3 states (S6-5).

## 6 Shared rows

X1 on the three specs: pass, 70 shared rows compared on place, z_rule, plan_poly. Skipped 3: base_frame and base_plate plan_poly (in s2, s3 only), keepout place (in s2, s3 only). Exempt: anchor_a, anchor_b, anchor_c (MEASURED, check_sketch.x1_lint).

S3 rows shared with S1 and S2 (19): base_frame, base_plate, drill_head, drill_tube, keepout, ring, bearing, gear, gear_hub, screw_a, nut_housing_a, anchor_a (exempt), liftmotor_a, frame_upper_a, screw_b, nut_housing_b, anchor_b (exempt), liftmotor_b, frame_upper_b.
Shared with S1 only (9): floor, receiver, collet, core_seat, holder, wingnut, collar, core_750, drill_top_block.
Shared with S2 only (14): nut_housing_c, nut_c, pinion_c, motor23_c, motor_shaft_c, motor_mount_c, pinion_axis_c, screw_c, anchor_c (exempt), guide_c, bracket_anchor_c, bracket_guide_c, frame_upper_c, liftmotor_c.
New (21): screw_end_c, anchor_bearing_c, guide_bearing_c, liftmotor_pilot_c, liftmotor_shaft_c, coupling_c, standoffs_c, home_switch_a/_b/_c, ring_ref, section_line, plan_axes, sync_callout, hold_callout, nut_station_start, nut_station_park, span_lt, load_cut, load_tension_c, load_comp_c.

## 7 Run results, stale key lists, previews

All values MEASURED, with the overlay edit and s3_spec.yaml in place.

| Run | Result |
|---|---|
| `--controls` (default 12 jobs) | Z clean 75/75, B fired 208/208, smoke 2/2: 285/285 match; wall 124.4 s |
| `--controls`, anchor-row dry run (reverted, Correction 3) | Z 73/75, B 193/208; wall 121.2 s |
| `--stale` | 2 records, 3 differences, exit 1. s1_checks_r7.json: jackscrew.lead 8 -> 3, jackscrew.nominal 8 -> 12. s2_checks_r5.json: jackscrew.nominal 8 -> 12. X1 pass (70 compared, 3 skipped, 3 exempt) |
| `--stale --include-unaccepted` | 15 records, 17 differences: the 3 above plus wip s1 r5, r6, r7 (lead, nominal) and wip s2 r0 to r4, r6, r7, r8 (nominal). The previews s1 r8 and s2 r9 are clean |
| `check_sketch.py s1 --rev 8` (preview, unchanged s1_side_poses.py, wip/, not of record) | 18 pass, 2 fail. K5 fail: the anchor zero-area Rectangle, known since step 0; cleared at P4/P6 by the mark rule. RPT fail: "spec declares no reported_items (s1_checks_r8.json is not a record accepted before RPT)" |
| `check_sketch.py s2 --rev 9` (preview, unchanged s2_plan.py) | 19/19 pass, RPT 12 items |

These stale lists open a revision drawn at (d): **S1 r8** (jackscrew.lead, jackscrew.nominal) and **S2 r9** (jackscrew.nominal). None is suppressed.

What moved in the previews (record diff of wip/s1_checks_r7.json against r8, and wip/s2_checks_r8.json against r9):
- keys_read: S1 jackscrew.lead 8 -> 3 and jackscrew.nominal 8 -> 12; S2 jackscrew.nominal 8 -> 12. No key added.
- Checks: S1 RPT pass (exempt by record name r7) -> fail (r8 has no exemption). Every other check result and measured value is equal in both sketches, including S1-4 0.84, S1-5b 142.00, S2-2 52.80, S2-5a 11.71, K6, K7 and K8 counts.
- check_stack reported values and drawn reported rows: none moved.
- Drawn: the S1 screw rectangles widen from 8 to 12 and the S2 screw circles from d 8 to d 12, both read from jackscrew.nominal. The check runs write no PNGs, so pixels were not compared here (P6). S1 lead ticks read jackscrew.lead.
- Not yet moved (spec edits at P6): anchor squares in S1 and S2, the S1 screw label text "T8", the S1 mark line, and S1 reported_items.

DERIVED-chain lint: K2 on S1, S2 and the overlay passes (166 leaves, 20 expr leaves agree within 0.05). top_guide_z, member_length and member_length_rail are untouched, because their inputs did not move. The three new expr leaves (mean_diameter, anchor_bearing_z, guide_bearing_z) agree.

S3: there is no stub run before (c). checks_s3.run on an empty figure gives S3-1, S3-2 and S3-3 fail, cause absent. checks_s3.reported gives 9 of 10 items; tension_segment is absent (needs drawing). K2 on s3_spec.yaml fails on the two missing nut keys (open item 1).

## 8 Open items for signature

1. **K2 red on s3 until two values are supplied** (Designer / Sean): `jackscrew.nut_body_od` and `jackscrew.nut_flange_thickness` (Correction 6). Blocking for (c): the stub run reads K2 as a guard.
2. **Anti-rotation pin, M10x1 locknut, nut retaining ring**: not_drawn for want of leaves. Designer rules at P3a whether they are drawn (values needed) or stay in the note.
3. **Anchor rows in S1 and S2** take the 42-square place at P6 with their redraw, and the S3 x1_exempt is removed then (Correction 3). The guide rows keep `nut_flange_od / 2` for the block radius, value equal to `guide_block_od / 2`. The rename lands in all three specs at P6.
4. **Bearing-line mark in the section.** anchor_bearing_c carries `mark: {sub: line, z: jackscrew.anchor_bearing_z}`. P0T admits the S1 side-view form only, so the section form (endpoints on the bearing bore faces, u -173 to -147) needs its own rule at P4 (Topologist).
5. **Coupling stack** (Correction 5): shaft 240 to 264 against screw end 253.5 to 265 in a 20 coupling. The Designer picks a shaft engagement, a screw-end length or a longer coupling_length. coupling_length moves anchor_z or the motor (S1-4, L, chain leaves).
6. **liftmotor.standoff_af 5.5**: a working value with no Designer source, used only for the elevation width of standoffs_c.
7. **New spec fields** (section_yz, axes, projection_by_axes, section_class, section_u, hatch, sub_artists, leaders_to, value_from, look_direction, axes_not_inverted, points) are declared here and implemented at P4 (TP-7 per-Axes view, section-view depth along X, renderer section convention, K5 admissions for balls, line and lever). check_stack today hulls the depth band with the place y extent, which is wrong for section_yz (O4).
8. **S3-3 symmetry premise lint** (rows a, b, c equal up to theta) with Z and B: written at P4, or the eight a/b screw-set pairs stay uncertified (section 5).
9. **0.5 m core mass 10.4 kg** has no params or overlay leaf. s3_checks.S3-2.core_mass_kg carries it from Quinn's Source Verification Register (DERIVED).
10. **Name and label text in S1/S2**: S1 screw rows still read "T8 jack screw" / "T8 screw L". With nominal 12 the S1 K4 label number is unchanged (L 900), but the text is wrong. The edit belongs to S1 r8 (P6).
11. **Home-switch lever**: drawn at capture_end it hangs free (the housing is 726.16 below it). The Designer confirms whether the lever is drawn at its park contact as a phantom.
12. **K8 handedness in the section** relies on the `side` predicate reading u, not x, in section_yz (P4).
13. **S1 r8 needs `reported_items`** in s1_spec.yaml. The RPT exemption is by record name (s1_checks_r7.json) and r8 fails RPT. Designer list due before P6.

## 9 Gameplan lines to change

1. l.272, within the line. Old: "Shows: bottom anchor with thrust bearing, screw" New: "Shows: bottom anchor (fixed: two angular-contact bearings back-to-back in a 42-square block, Design Notes 31), screw"
2. l.272, within the line. Old: "top guide (radial support only), NEMA 17 mount and coupling, power-off hold device (option drawn: non-back-driving lead, brake, or park pin with visible state; Step 2 decides)" New: "top guide (radial support only), NEMA 17 on four standoffs under the anchor block with a beam coupling, power-off hold device (option drawn: self-locking Tr12x3 lead per Design Notes 31; brake or park pin with visible state remain options; Step 2 decides)"
3. l.275. Old: "Script: `docs/sketches/s3_jackscrew_section.py`. PNG: `s3_jackscrew_section_r1.png` (location per the Design Notes 25 output rule)." New: "Script: `docs/sketches/s3_jackscrew_section.py`. PNG: `s3_jackscrew_section_r1.png` (location per the Design Notes 25 output rule). Spec `docs/sketches/s3_spec.yaml` (1.3 (b), `research/sean/cr_scratch/step1.3_engineer_spec.md`): view section_yz (section A-A, plane x = 0, viewer at +X, u = +Y), inset plan_xy, pose capture_end, 63 rows, load_cases, s3_checks, chains, reported_items (10)."
4. l.287, the S3-2 row. Old: "| S3-2 | Buckling of the nut-to-anchor segment at its longest (nut at park), worst compression case per screw:" New: "| S3-2 | Buckling, worst compression case per screw (form per Design Notes 31: threshold kept; drawn mounting floating, column the anchor-to-guide bearing span L_t 870 read from the drawn bearing rows, K 0.7; rigid nut-to-anchor segment at park reported only):"
5. l.287, within the S3-2 row. Old: "d_r (T8 root diameter, ASSUMED until vendor data, Sean)" New: "d_r (Tr12x3 root 8.5, ASSUMED until vendor data, batch 2 B2-1)"
6. l.287, within the S3-2 row. Old: "SF (ASSUMED 3, Sean confirms) | 100 mm segment under W |" New: "SF 3 in every case, stall included (Sean, Design Notes 31); spec values P_cr 1363.8 N, least margin 3.97 at stall up (DERIVED, 1.3 (b)) | 100 mm segment under W |"
7. l.288, the S3-3 row. Old: "every consecutive pair class C in the drawn figures (S1 for core, base and frame members; S3 for anchor, screw, nut, ring; S6 for bearing and tube), K7 C |" New: "every consecutive pair class C in the K7 entries of a certifying record named per pair in the spec `chains` (latest accepted S1 and S2 records with --stale clean, read by S3-3; this figure; or declared for the S6 segment). Chain per screw: screw c runs base plate, base frame, member c (Design Notes 27); screws a, b run base plate, member a or b. Uncertified at 1.3 (b): cutter\\|core (all chains) and the a, b screw-set pairs until the symmetry premise lint lands (P4) (`step1.3_engineer_spec.md` section 5), K7 C |"
8. l.293. Old: "Sync: the spec states the method drawn." New: "Sync: the spec states the method drawn (1.3 (b): single controller, three drivers, home switch per screw at park, `liftsync.*`; no belt; Design Notes 31)."
9. Insert after l.718 (line text begins "| Ring **130 mm** above the tip; anchors 265 z_A (325 z_S), top guides 1165 z_A (1225 z_S)"): "| Anchor block **42 square x 30**; bearing lines **280** and **1150** z_A, span L_t **870** | overlay `jackscrew.anchor_block_width`, `jackscrew.anchor_bearing_z`, `jackscrew.guide_bearing_z` (expr) | ASSUMED / DERIVED (Design Notes 31); S3 rows anchor_c, anchor_bearing_c, guide_bearing_c, span_lt; S1, S2 anchor rows at P6 |"
10. Insert after the line inserted by item 9: "| Section A-A: plane x = 0, viewer at +X, u = +Y, pose capture_end | `s3_spec.yaml` section block | DECLARED (Designer 1.3 (a), Design Notes 4); S3 figure title, inset cutting-plane line, K8 section handedness |"
11. l.722, within the line. Old: "1083 to 1267 N at Tr12x3" New: "1084.54 to 1267.43 N at Tr12x3 (1.3 (b) hand and checks_s3 computed)"
12. l.712 (Echo row "Three screws and three pinions at **120 deg**"): none.
