# S4 checks, revision r2

2026-11-27T21:55:30. Spec s4_spec.yaml (signed at 1.4 (b) (Designer P3a, Loftsman P3b, re-check P2r); (c) edits P4, P5f (signed P5r); P6: x1_edits_at_p6 applied to s1, s3, s4 and the field deleted, legend brass pattern (Designer P5D N2). Written 2026-11-27 (P2).); script s4_base_section.py. Frame z_S = z_A + jig.datum_a_above_floor.

| Check | Result | Measured | Threshold | Z | B | Reason |
|---|---|---|---|---|---|---|
| K1 | pass | 0 | 0 | clean 1/1 | fired 3/3 | no literal outside [-1, 0, 0.5, 1, 2], no soft-key comparison, no figure setting (s4_base_section.py) |
| K2 | pass | 0 | 0 | clean 2/2 | fired 7/7 | 173 spec keys resolve; 203 overlay leaves sourced, legal status, no shadow; 24 expr leaves agree within 0.05 |
| K3 | pass | 0 | 0 | clean 4/4 | fired 11/11 | [section] 2 figure(s): one Axes, title, (mm) labels, equal aspect, grids, figsize, dpi 150; every text inside the saved image |
| K4 | pass | 0 | 0 | clean 14/14 | fired 64/64 | [section] 36 label(s) carry their key value, each leader ends on its part, no two leaders cross; figure note names every not_drawn part |
| K5 | pass | 0 | 0 | clean 9/9 | fired 76/76 | [section] 168 tagged artist(s) projected per kind, axis and spec projection (view normal X) |
| K6 | pass | 0.0 | 0.05 | clean 6/6 | fired 12/12 | [section] 35 z_rule(s) match drawn extents within 0.05 mm; check_stack imports and anchors clean |
| K7 | pass | 0 | 0 | clean 19/19 | fired 38/38 | [section] 55 pair test(s) clean; states ['C', 'F', 'N', 'swept:F', 'undeclared:F'] |
| K8 | pass | 0 | 0 | clean 23/23 | fired 128/128 | [section] 187 predicate(s) hold, axes not inverted |
| K9 | pass | 0 | 0 | clean 6/6 | fired 9/9 | [section] every spec row drawn, every tagged artist in the spec (20 rows) |
| S4-1 | pass | 159.84 | 0.01 | clean 1/1 | fired 3/3 | collar top 159.84 z_A = stop.collar_top_z 159.84; drawn top equal in every figure |
| S4-2 | pass | 6.29 | 0 | clean 1/1 | fired 5/5 | least exposure margin 6.29 mm over core.min_exposed 143.12; rests_on and grip hold in every figure |
| S4-3 | pass | None | None | clean 1/1 | fired 8/8 | kept-part sense predicates hold (carrier, collar, collet, collet_105, core_100, holder, liner, receiver, washer, wingnut) |
| X1 | pass | 0 | 0 | clean 2/2 | fired 6/6 | 72 shared row(s) compared on place, z_rule, plan_poly; skipped 3: base_frame plan_poly (only in s2, s3), base_plate plan_poly (only in s2, s3, s4), keepout plac |
| RPT | pass | 0 | 0 | clean 3/3 | fired 6/6 | 11 reported item(s) declared, every one has a value |

| Check | Cause of red |
|---|---|

Reported (no threshold):
- Park tip 1015.00 z_A (entry plane collar_top); highest class start 965.00 z_A; lift stroke 830.16 mm; S1-3 load plane core_stop
- Collar top recomputed 159.84 z_A against params stop.collar_top_z 159.84
- Park tip z_A by plane and core length: core_stop: length_capture 1015.00, length_install 1015.00, length_optional 1092.50; collar_top: length_capture 1015.00, length_install 1015.00, length_optional 1209.84
- Start tip minus capture-core top (core.length_capture) on the core stop: 422.50 mm (end tip + drill_advance_500core = 719.77 z_A; core top 542.50 z_A)
- carrier: highest point 390.00 z_S, margin to the 2000 mm soft target 1610.00 mm (spec values, not drawn)
- liner: highest point 390.00 z_S, margin to the 2000 mm soft target 1610.00 mm (spec values, not drawn)

## Reported values, drawn (s4_base_section.py r2; no threshold, never asserted)

| Quantity | Value | Basis |
|---|---|---|
| q10_min_on_stop | 253.71 (nut-plate datum); 260.46 (collar-top datum) | nut-plate top + core.min_exposed - core stop |
| advance | option D: the lift lowers the drill one slice per cut; least slice 76.44 (axis), 56.02 (r 50); 0.75 m core: tip span 496.29 (681.13 to 184.84), 7 slices, 572.73 removed; stub on the stop 177.27 (axis) to 197.69 (surface), below the least core on the stop 253.71; on the carrier: top 379.77, exposure 226.68, 2 slices, 160.00 removed (least core on the carrier 93.71); 100 mm core on the carrier: 1 slice, stub 17.27 (axis) to 37.69 (surface) | F4: core top >= kerf centre + stop.margin at the stop |
| carrier_torque | bottom face 50.9 kPa; liner side 6.37 kPa | 2T / (pi r^3); T / (2 pi r^2 L) |
| q5_delta | Delta 0: collar top 159.84, stop 184.84, min core on the stop 253.71; Delta 25: collar top 184.84, stop 209.84, min core on the stop 278.71; Delta 50: collar top 209.84, stop 234.84, min core on the stop 303.71; kept 32 mm (Design Notes 34) | Designer 1.4 (a) section 7 |
| liner_wall | D = d + 5, free wall 2.00; d 105 core: no liner (110 > collets.envelope_max 106.585) | liner.od_offset, liner.wall |
| kept_axial | as S3 r7 kept_axial (1000 N at the cut; F_stall + W 1287.05 / 1104.16 N) | checks_s3.loads on s3_spec.yaml (F_stall total + W per mu; spec read recorded in deps) |
| q10_core_top | on the carrier 302.50 (collar top 159.84); on the stop 142.50 (17.34 below the collar top) | drawn core_100 (MEASURED); core on the stop DERIVED |
| q10_exposed | 149.41 on the carrier against 143.12; on the stop -10.59 | drawn core_100 and wingnut tops |
| grip_length | collet: 23.20 (42.50 to 65.70); collet_105: 25.70 (42.50 to 68.20) (chamfer drawn straight; the true straight bore ends 0.41 lower at the 1 bore-lip fillet, tangent length r tan 22.5, Loftsman P3b N2) | drawn core-seat top to the top of the cone piece's inner (bore) edge (MEASURED) |
| cut_case_seat | collet foot 40.00 on the receiver floor top 40.00 (gap 0.00); receiver shoulder underside 12.00 on the plate top 12.00 (gap 0.00); spigot radial gap 0.20 in the plate hole | drawn collet foot, receiver floor and shoulder pieces, base_plate and receiver_spigot (MEASURED, figure 1) |
| seat_bearing | carrier: carrier on core_seat 3.00; liner: carrier on core_seat_105 0.50; liner: liner on core_seat_105 2.50; all of F_stall + W on the carrier annulus r 50.00 to 50.50: 8.15 MPa | drawn bottom and seat faces (MEASURED); stress DERIVED |

## Reported items (spec reported_items; RPT)

| ID | Item | Value | Basis | Tag |
|---|---|---|---|---|
| q10_core_top | 100 mm core top on the stop against the collar top (142.50 vs 159.84, 17.34 below) and on the carrier (302.50) | on the carrier 302.50 (collar top 159.84); on the stop 142.50 (17.34 below the collar top) | drawn core_100 (MEASURED); core on the stop DERIVED | MEASURED |
| q10_exposed | exposed length of the drawn 100 mm core above the nut-plate top against core.min_exposed 143.12 (on the stop -10.59; on the carrier 149.41) | 149.41 on the carrier against 143.12; on the stop -10.59 | drawn core_100 and wingnut tops | MEASURED |
| q10_min_on_stop | minimum core length on the stop 253.71 (nut-plate datum; 260.46 at the collar-top datum) | 253.71 (nut-plate datum); 260.46 (collar-top datum) | nut-plate top + core.min_exposed - core stop | DERIVED |
| grip_length | collet straight-bore grip, d 100: 23.20 (d 105: 25.70) | collet: 23.20 (42.50 to 65.70); collet_105: 25.70 (42.50 to 68.20) (chamfer drawn straight; the true straight bore ends 0.41 lower at the 1 bore-lip fillet, tangent length r tan 22.5, Loftsman P3b N2) | drawn core-seat top to the top of the cone piece's inner (bore) edge (MEASURED) | MEASURED |
| advance | advance per slice and slices per core for the drawn option D: the lift lowers the drill one slice per cut; least slice under F4 76.44 on the axis, 56.02 at r 50; 0.75 m core: tip span 496.29 (681.13 to 184.84), 7 slices at the F4 least slice 76.44, 572.73 removed; stub on the stop 177.27 (axis) to 197.69 (surface), onto the carrier for further slices (top 379.77, exposure 226.68, 2 slices, 160.00 removed, stub 17.27 to 37.69 left on the carrier); 253.71 is the least core that takes a cut on the stop, 93.71 on the carrier; 100 mm core on the carrier: 1 slice, stub 17.27 (axis) to 37.69 (surface) (Loftsman P3b FIX 5) | option D: the lift lowers the drill one slice per cut; least slice 76.44 (axis), 56.02 (r 50); 0.75 m core: tip span 496.29 (681.13 to 184.84), 7 slices, 572.73 removed; stub on the stop 177.27 (axis) to 197.69 (surface), below the least core on the stop 253.71; on the carrier: top 379.77, exposure 226.68, 2 slices, 160.00 removed (least core on the carrier 93.71); 100 mm core on the carrier: 1 slice, stub 17.27 (axis) to 37.69 (surface) | F4: core top >= kerf centre + stop.margin at the stop | DERIVED |
| carrier_torque | carrier-joint shear at 10 N m: 50.9 kPa on the bottom face; liner side shear 6.37 kPa over 100 | bottom face 50.9 kPa; liner side 6.37 kPa | 2T / (pi r^3); T / (2 pi r^2 L) | DERIVED |
| q5_delta | collet length options: collar top, stop, minimum core on the stop and S1 park highest point per Delta 0 / 25 / 50 (159.84 / 184.84 / 209.84; 253.71 / 278.71 / 303.71; 1969.84 / 1994.84 / 2019.84 z_S); kept 32 mm (Design Notes 34) | Delta 0: collar top 159.84, stop 184.84, min core on the stop 253.71; Delta 25: collar top 184.84, stop 209.84, min core on the stop 278.71; Delta 50: collar top 209.84, stop 234.84, min core on the stop 303.71; kept 32 mm (Design Notes 34) | Designer 1.4 (a) section 7 | DERIVED |
| liner_wall | liner per core size: D = d + 5, free wall 2.0 (drawn 2.50 at K d+1); d 105 core has no liner (110 above collets.envelope_max 106.585) | D = d + 5, free wall 2.00; d 105 core: no liner (110 > collets.envelope_max 106.585) | liner.od_offset, liner.wall | DERIVED |
| cut_case_seat | cut-case seat as drawn: collet foot on the receiver floor top (40.00), receiver shoulder underside on the plate top (12.00); spigot radial gap 0.20 in the plate hole | collet foot 40.00 on the receiver floor top 40.00 (gap 0.00); receiver shoulder underside 12.00 on the plate top 12.00 (gap 0.00); spigot radial gap 0.20 in the plate hole | drawn collet foot, receiver floor and shoulder pieces, base_plate and receiver_spigot (MEASURED, figure 1) | MEASURED |
| kept_axial | axial force in collet, receiver, base plate at 1000 N and at F_stall + W 1287.05 N (unchanged from S3 r7) | as S3 r7 kept_axial (1000 N at the cut; F_stall + W 1287.05 / 1104.16 N) | checks_s3.loads on s3_spec.yaml (F_stall total + W per mu; spec read recorded in deps) | DERIVED |
| seat_bearing | core-seat bearing widths: carrier 3.00 (figure 1); carrier 0.50 and liner 2.50 on the d 105 ledge (figure 2); 8.15 MPa if all of F_stall + W bears on the carrier annulus | carrier: carrier on core_seat 3.00; liner: carrier on core_seat_105 0.50; liner: liner on core_seat_105 2.50; all of F_stall + W on the carrier annulus r 50.00 to 50.50: 8.15 MPa | drawn bottom and seat faces (MEASURED); stress DERIVED | MEASURED |

Files: params.yaml 9469288a75c2, proposed_params.yaml b2488c014c25
