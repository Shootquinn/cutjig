# S2 checks, revision r11

2026-11-27T21:54:00. Spec s2_spec.yaml (signed (Designer, Loftsman 1.2 (b), with re-check sections; step1.2_designer_spec_signoff.md, step1.2_loftsman_spec_signoff.md); 1.2 (c) gear section field added for the plan annulus (signed at (c) by the Loftsman, Designer, Topologist and Software Engineer after P5f); 1.2 (h) r2 edits (gear ticks and shape text, label_theta, reference rows, F6 label text, pinion|gear_hub G 3, S2-5b over moves: true) re-checked by the Loftsman and the Topologist; r3 edits (tick toe pinion.r_toe 96.54 per Design Notes 29, plan_style: stand_in on the ties) signed by the Designer (sign-off r3); r4 edits (outline_matches on base_plate, stand_in_owner on the ties, label_side left on descent_stop) signed by the Designer (sign-off r4); r5 edit (label_theta 150 on descent_stop, Designer sign-off r4 FIX D4-1; step1.2_engineer_revision_r5.md); 1.3 P1Rf: reported_items (Designer P1Rd section 5) and label suffixes on drill_head and descent_stop (Designer P1Rd FIX D2)); script s2_plan.py. Frame z_S = z_A + jig.datum_a_above_floor.

| Check | Result | Measured | Threshold | Z | B | Reason |
|---|---|---|---|---|---|---|
| K1 | pass | 0 | 0 | clean 1/1 | fired 3/3 | no literal outside [-1, 0, 0.5, 1, 2], no soft-key comparison, no figure setting (s2_plan.py) |
| K2 | pass | 0 | 0 | clean 2/2 | fired 7/7 | 426 spec keys resolve; 203 overlay leaves sourced, legal status, no shadow; 24 expr leaves agree within 0.05 |
| K3 | pass | 0 | 0 | clean 4/4 | fired 11/11 | 1 figure(s): one Axes, title, (mm) labels, equal aspect, grids, figsize, dpi 150; every text inside the saved image |
| K4 | pass | 0 | 0 | clean 14/14 | fired 64/64 | 14 label(s) carry their key value, each leader ends on its part, no two leaders cross; figure note names every not_drawn part |
| K5 | pass | 0 | 0 | clean 9/9 | fired 76/76 | 122 tagged artist(s) projected per kind, axis and spec projection (view normal Z) |
| K6 | pass | 0.0 | 0.05 | clean 6/6 | fired 12/12 | 70 plan centre(s) on the spec within 0.05 mm (z not drawn in plan); check_stack imports and anchors clean |
| K7 | pass | 0 | 0 | clean 19/19 | fired 38/38 | 1296 plan pair test(s) clean over 4 pose(s); states ['G', 'N', 'plan-contact', 'swept:F', 'swept:G', 'swept:z-separated', 'swept:z-touch', 'undeclared:F', 'unde |
| K8 | pass | 0 | 0 | clean 23/23 | fired 128/128 | 208 predicate(s) hold, axes not inverted |
| K9 | pass | 0 | 0 | clean 6/6 | fired 9/9 | every spec row drawn, every tagged artist in the spec (71 rows) |
| S2-1 | pass | 0.0 | 0.1 | clean 1/1 | fired 1/1 | screws [30.0, 150.0, 270.0], pinions [90.0, 210.0, 330.0], phase 60 within 0.000 |
| S2-2 | pass | 52.8 | 10 | clean 1/1 | fired 1/1 | least margin 52.80 mm over g_min 10 |
| S2-3 | pass | 0.0 | 0.05 | clean 1/1 | fired 1/1 | pitch points {'pinion_a': 125.0, 'pinion_b': 125.0, 'pinion_c': 125.0} at the gear pitch radius 125.00 within 0.000 |
| S2-4 | pass | 0.0 | 0.05 | clean 1/1 | fired 1/1 | 4 centres within 0.000 mm |
| S2-5a | pass | 11.713 | F | clean 1/1 | fired 1/1 | 27 fixed parts clear of the sector, least 11.71 mm |
| S2-5b | pass | 19.84 | 10 | clean 1/1 | fired 3/3 | 10 moving parts in the sector, least 19.84 mm above the hand band (drill_head) |
| S2-6 | pass | 0 | 0 | clean 1/1 | fired 2/2 | 3 members seated |
| X1 | pass | 0 | 0 | clean 2/2 | fired 6/6 | 72 shared row(s) compared on place, z_rule, plan_poly; skipped 3: base_frame plan_poly (only in s2, s3), base_plate plan_poly (only in s2, s3, s4), keepout plac |
| RPT | pass | 0 | 0 | clean 3/3 | fired 6/6 | 12 reported item(s) declared, every one has a value |

| Check | Cause of red |
|---|---|

Reported (no threshold):
- Park tip 959.84 z_A (entry plane collar_top); highest class start 834.84 z_A; lift stroke 775.00 mm; S1-3 load plane core_stop
- Q9 0.5 m only: park 959.84 z_A, stroke 775.00 mm, L 
  - 0.5 m only, park: 959.84 for 0 <= c <= 117.34; 842.50 + c for c >= 117.34
  - 0.5 m only, lowest stop: 184.84 for 0 <= c <= 292.34; c - 107.50 for c >= 292.34
  - 0.5 m only, lift stroke: 775.00 for 0 <= c <= 117.34; 657.66 + c for 117.34 <= c <= 292.34; 950.00 for c >= 292.34
  - 0.5 m only, stop core.length_capture: 184.84 for 0 <= c <= 292.34; c - 107.50 for c >= 292.34
  - 0.5 m only, stop core.length_install: 184.84 for 0 <= c <= 42.34; 142.50 + c for c >= 42.34
  - 0.5 m only, start core.length_capture: 834.84 for 0 <= c <= 292.34; 542.50 + c for c >= 292.34
  - 0.5 m only, start core.length_install: 834.84 for 0 <= c <= 42.34; 792.50 + c for c >= 42.34
  - 0.5 m only, start_minus_core_top core.length_capture: 292.34 for 0 <= c <= 292.34; c for c >= 292.34
  - 0.5 m only, start_minus_core_top core.length_install: 42.34 for 0 <= c <= 42.34; c for c >= 42.34
- Q9 0.5 and 0.75 m: park 959.84 z_A, stroke 775.00 mm, L 
  - 0.5 and 0.75 m, park: 959.84 for 0 <= c <= 117.34; 842.50 + c for c >= 117.34
  - 0.5 and 0.75 m, lowest stop: 184.84 for 0 <= c <= 292.34; c - 107.50 for c >= 292.34
  - 0.5 and 0.75 m, lift stroke: 775.00 for 0 <= c <= 117.34; 657.66 + c for 117.34 <= c <= 292.34; 950.00 for c >= 292.34
  - 0.5 and 0.75 m, stop core.length_capture: 184.84 for 0 <= c <= 292.34; c - 107.50 for c >= 292.34
  - 0.5 and 0.75 m, stop core.length_install: 184.84 for 0 <= c <= 42.34; 142.50 + c for c >= 42.34
  - 0.5 and 0.75 m, start core.length_capture: 834.84 for 0 <= c <= 292.34; 542.50 + c for c >= 292.34
  - 0.5 and 0.75 m, start core.length_install: 834.84 for 0 <= c <= 42.34; 792.50 + c for c >= 42.34
  - 0.5 and 0.75 m, start_minus_core_top core.length_capture: 292.34 for 0 <= c <= 292.34; c for c >= 292.34
  - 0.5 and 0.75 m, start_minus_core_top core.length_install: 42.34 for 0 <= c <= 42.34; c for c >= 42.34
- Q9 plus 1 m: park 1209.84 z_A, stroke 1025.00 mm, L 
  - plus 1 m, park: 1209.84 for 0 <= c <= 117.34; 1092.50 + c for c >= 117.34
  - plus 1 m, lowest stop: 184.84 for 0 <= c <= 292.34; c - 107.50 for c >= 292.34
  - plus 1 m, lift stroke: 1025.00 for 0 <= c <= 117.34; 907.66 + c for 117.34 <= c <= 292.34; 1200.00 for c >= 292.34
  - plus 1 m, stop core.length_capture: 184.84 for 0 <= c <= 292.34; c - 107.50 for c >= 292.34
  - plus 1 m, stop core.length_install: 184.84 for 0 <= c <= 42.34; 142.50 + c for c >= 42.34
  - plus 1 m, stop core.length_optional: 392.50 + c for c >= 0
  - plus 1 m, start core.length_capture: 834.84 for 0 <= c <= 292.34; 542.50 + c for c >= 292.34
  - plus 1 m, start core.length_install: 834.84 for 0 <= c <= 42.34; 792.50 + c for c >= 42.34
  - plus 1 m, start core.length_optional: 1042.50 + c for c >= 0
  - plus 1 m, start_minus_core_top core.length_capture: 292.34 for 0 <= c <= 292.34; c for c >= 292.34
  - plus 1 m, start_minus_core_top core.length_install: 42.34 for 0 <= c <= 42.34; c for c >= 42.34
  - plus 1 m, start_minus_core_top core.length_optional: c for c >= 0
- Collar top recomputed 159.84 z_A against params stop.collar_top_z 159.84
- Park tip z_A by plane and core length: core_stop: length_capture 884.84, length_install 884.84, length_optional 1092.50 + c for c >= 0; collar_top: length_capture 959.84, length_install 959.84, length_optional 1209.84
- Start tip minus capture-core top (core.length_install) on the core stop: 42.34 mm (end tip + drill_advance_500core = 719.77 z_A; core top 792.50 z_A)
- load: highest point 1819.84 z_S, margin to the 2000 mm soft target 180.16 mm (spec values, not drawn)
- start: highest point 1694.84 z_S, margin to the 2000 mm soft target 305.16 mm (spec values, not drawn)
- capture_end: highest point 1285.00 z_S, margin to the 2000 mm soft target 715.00 mm (spec values, not drawn)
- park: highest point 1819.84 z_S, margin to the 2000 mm soft target 180.16 mm (spec values, not drawn)

## Reported values, drawn (s2_plan.py r11; no threshold, never asserted)

| Quantity | Value | Basis |
|---|---|---|
| Outline extents, every drawn part (reference rows excluded: keepout, collet_axis, operator_sector, sightline_f6) | x -322.00 to 322.00, y -304.00 to 304.00 | MEASURED (drawn pieces) |
| Outline extents, parts above the plate | x -278.27 to 278.27, y -304.00 to 218.00 | MEASURED (drawn pieces) |
| Highest point over parts, load | 1819.84 z_S (drill_tube) | MEASURED (check_stack) |
| Highest point over parts, start | 1694.84 z_S (drill_tube) | MEASURED (check_stack) |
| Highest point over parts, capture_end | 1285.00 z_S (guide_tie_b) | MEASURED (check_stack) |
| Highest point over parts, park | 1819.84 z_S (drill_tube) | MEASURED (check_stack) |
| Tight spot: pinion toe to gear hub (plan, G g_min 3 ASSUMED) | 5.22 | MEASURED; basis circumscribed outline (pinion radial footprint) against the hub annulus; the toe edge midpoint is on the drawn trapezoid, so the bound equals the drawn gap (DERIVED 95.22 - 90.00) |
| Tight spot: lift motors to the sector edge | 11.71 (bound) / 15.69 (drawn square) | MEASURED: circumscribed outline (S2-5a) / drawn pieces |
| S2-5b strike list at load (z_S band; margin over the hand-band top 940 z_A) | drill_head 1019.84 to 1126.21 (19.84); drill_tube 1126.21 to 1819.84 (126.21); bearing 1136.84 to 1161.84 (136.84); ring 1149.84 to 1161.84 (149.84); motor_mount_c 1161.84 to 1185.34 (161.84); pinion_c 1168.22 to 1259.46 (168.22); motor23_c 1185.34 to 1242.34 (185.34); motor_shaft_c 1209.84 to 1217.84 (209.84); gear 1242.07 to 1275.84 (242.07); gear_hub 1242.07 to 1275.84 (242.07) | MEASURED (check_stack) |

## Reported items (spec reported_items; RPT)

| ID | Item | Value | Basis | Tag |
|---|---|---|---|---|
| outline_extents_all | Outline extents, every drawn part, reference rows excluded, against the 644 x 608 footprint (open, not asserted) | x -322.00 to 322.00, y -304.00 to 304.00 | MEASURED (drawn pieces) | MEASURED |
| outline_extents_above_plate | Outline extents, parts above the plate | x -278.27 to 278.27, y -304.00 to 218.00 | MEASURED (drawn pieces) | MEASURED |
| members_to_plate_edge | Members against the plate edge: members a, b x extent against 322; member c against the plate y edge 304 | a, b 43.73 inside the x edge 322; c 0.00 to the plate y edge -304 | drawn pieces of frame_upper_a/b/c against the plate edges (icd.footprint_x, icd.footprint_y) | MEASURED |
| tip_force_footprint | Footprint against the S1 unbolted tip force (bolt-down or footprint goes to the Step 2 row, R1) | 351 / 379 / 563 / 269 N (load, start, capture_end, park) over lever 304 | s1_mass_report_r10.json tip_force_at_com_N (latest accepted S1 report); lever icd.footprint_y / 2 | DERIVED |
| cutter_overhang | Cutter overhang of the keep-out: drill.head_od / 2 - icd.keepout_radius (S2-a; Step 4 ICD row icd.keepout_radius) | 2.70 | drill.head_od / 2 - icd.keepout_radius (drill.head_od ASSUMED, Q2) | DERIVED |
| f6_eye_limits | F6 eye limits at r 400: eye height below which the ring rim hides the cut at capture_end, to the axis and to the cutter rim | 0.49 m (axis), 0.58 m (cutter rim) z_S | line from the cut at capture_end (drill_head z_min; r 0 or drill.head_od / 2) through the ring rim (ring.od / 2, ring z_min at capture_end) to r = operator.watch_r (check_stack, z_S) | DERIVED |
| s2_5b_strike_list | S2-5b overhead strike list in the sector at load, z_S bands, with margin over the hand-band top | drill_head 1019.84 to 1126.21 (19.84); drill_tube 1126.21 to 1819.84 (126.21); bearing 1136.84 to 1161.84 (136.84); ring 1149.84 to 1161.84 (149.84); motor_mount_c 1161.84 to 1185.34 (161.84); pinion_c 1168.22 to 1259.46 (168.22); motor23_c 1185.34 to 1242.34 (185.34); motor_shaft_c 1209.84 to 1217.84 (209.84); gear 1242.07 to 1275.84 (242.07); gear_hub 1242.07 to 1275.84 (242.07) | MEASURED (check_stack) | MEASURED |
| tight_rim_to_rod | Tight spot: ring rim to guide rod | 10.00 | plan outlines ring and guide_member, the K7 plan measure (G, g_min 10 identity) | MEASURED |
| tight_rim_to_member | Tight spot: ring rim to member inner face | 34.00 | plan outlines ring and frame_upper_a/b/c, the K7 plan measure | MEASURED |
| tight_liftmotor_sector | Tight spot: lift motors to the sector edge, bound (circumscribed) and drawn square | 11.71 (bound) / 15.69 (drawn square) | circumscribed outline (S2-5a) / drawn pieces | MEASURED |
| tight_pinion_toe_hub | Tight spot: pinion toe to gear hub | 5.22 | circumscribed outline (pinion radial footprint) against the hub annulus | MEASURED |
| highest_point_parts | Highest point over parts at each pose, reference rows excluded (LF1.2-5) | load 1819.84 z_S (drill_tube); start 1694.84 z_S (drill_tube); capture_end 1285.00 z_S (guide_tie_b); park 1819.84 z_S (drill_tube) | check_stack, reference rows excluded (LF1.2-5) | MEASURED |

Files: params.yaml 9469288a75c2, proposed_params.yaml b2488c014c25
