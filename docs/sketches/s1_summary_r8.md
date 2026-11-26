# S1 checks, revision r8

2026-11-26T15:10:05. Spec s1_spec.yaml (signed (Designer, Loftsman; pose table confirmed by Sean 2026-11-25); r8 edits at 1.3 P6 under the orchestrator-named exceptions (a) to (f)); script s1_side_poses.py. Frame z_S = z_A + jig.datum_a_above_floor.

| Check | Result | Measured | Threshold | Z | B | Reason |
|---|---|---|---|---|---|---|
| K1 | pass | 0 | 0 | clean 1/1 | fired 2/2 | no literal outside [-1, 0, 0.5, 1, 2], no soft-key comparison, no figure setting (s1_side_poses.py) |
| K2 | pass | 0 | 0 | clean 2/2 | fired 7/7 | 331 spec keys resolve; 194 overlay leaves sourced, legal status, no shadow; 21 expr leaves agree within 0.05 |
| K3 | pass | 0 | 0 | clean 4/4 | fired 11/11 | 4 figure(s): one Axes, title, (mm) labels, equal aspect, grids, figsize, dpi 150; every text inside the saved image |
| K4 | pass | 0 | 0 | clean 8/8 | fired 31/31 | 55 label(s) carry their key value, each leader ends on its part, no two leaders cross; figure note names every not_drawn part |
| K5 | pass | 0 | 0 | clean 7/7 | fired 47/47 | 351 tagged artist(s) projected per kind, axis and spec projection (view normal Y) |
| K6 | pass | 0.0 | 0.05 | clean 5/5 | fired 12/12 | 231 z_rule(s) match drawn extents within 0.05 mm; check_stack imports and anchors clean |
| K7 | pass | 0 | 0 | clean 18/18 | fired 35/35 | 618 pair test(s) clean; states ['C', 'F', 'N', 'depth-separated', 'plan-contact', 'plan-separated', 'swept:C', 'swept:F', 'swept:depth-separated', 'swept:plan-s |
| K8 | pass | 0 | 0 | clean 17/17 | fired 89/89 | 346 predicate(s) hold, axes not inverted |
| K9 | pass | 0 | 0 | clean 5/5 | fired 9/9 | every spec row drawn, every tagged artist in the spec (58 rows) |
| S1-1 | pass | 650.0 | [534.93, 650] | clean 1/1 | fired 2/2 | drawn start tip minus end-of-capture tip 650.00 mm against [534.93, 650] |
| S1-2 | pass | 125.0 | > 0 | clean 1/1 | fired 2/2 | park tip above the highest class start by 125.00 mm |
| S1-3 | pass | {'core.length_capture': 367.34, 'core.length_install': 117.34} | >= 0 | clean 1/1 | fired 1/1 | margins over core_stop {'core.length_capture': 367.34, 'core.length_install': 117.34} |
| S1-4 | pass | 0.84 | >= 0 | clean 1/1 | fired 2/2 | nut inside travel at every pose, least margin 0.84 mm |
| S1-5a | pass | 192.34 | 25 | clean 1/1 | fired 1/1 | bore ceiling minus capture-core (core_750) top at end of capture 192.34 mm, need 25 |
| S1-5b | pass | 142.0 | 10 | clean 1/1 | fired 1/1 | 91 pairs, least certified clearance 142.00 mm |
| S1-6 | pass | 0 | 0 | clean 1/1 | fired 1/1 | 8 screw projections at r cos(theta), depth r sin(theta) |
| S1-7 | pass | 607.66 | 534.93 | clean 1/1 | fired 1/1 | capture-core (core_750) top at start minus end-of-capture tip 607.66 mm, need 534.93 (spare 72.73) |
| X1 | pass | 0 | 0 | clean 1/1 | fired 3/3 | 70 shared row(s) compared on place, z_rule, plan_poly; skipped 3: base_frame plan_poly (only in s2, s3), base_plate plan_poly (only in s2, s3), keepout place (o |
| RPT | pass | 0 | 0 | clean 3/3 | fired 6/6 | 8 reported item(s) declared, every one has a value |

| Check | Cause of red |
|---|---|

Reported (no threshold):
- Park tip 959.84 z_A (entry plane collar_top); highest class start 834.84 z_A; lift stroke 775.00 mm; S1-3 load plane core_stop
- Q9 0.5 m only: park 959.84 z_A, stroke 775.00 mm, L L_min 885.00, at anchor_z 885.84
  - 0.5 m only, park: 959.84 for 0 <= c <= 117.34; 842.50 + c for c >= 117.34
  - 0.5 m only, lowest stop: 184.84 for 0 <= c <= 292.34; c - 107.50 for c >= 292.34
  - 0.5 m only, lift stroke: 775.00 for 0 <= c <= 117.34; 657.66 + c for 117.34 <= c <= 292.34; 950.00 for c >= 292.34
  - 0.5 m only, L L_min: 885.00 for 0 <= c <= 117.34; 767.66 + c for 117.34 <= c <= 292.34; 1060.00 for c >= 292.34
  - 0.5 m only, L at anchor_z: 885.84 for 0 <= c <= 117.34; 768.50 + c for c >= 117.34
  - 0.5 m only, stop core.length_capture: 184.84 for 0 <= c <= 292.34; c - 107.50 for c >= 292.34
  - 0.5 m only, stop core.length_install: 184.84 for 0 <= c <= 42.34; 142.50 + c for c >= 42.34
  - 0.5 m only, start core.length_capture: 834.84 for 0 <= c <= 292.34; 542.50 + c for c >= 292.34
  - 0.5 m only, start core.length_install: 834.84 for 0 <= c <= 42.34; 792.50 + c for c >= 42.34
  - 0.5 m only, start_minus_core_top core.length_capture: 292.34 for 0 <= c <= 292.34; c for c >= 292.34
  - 0.5 m only, start_minus_core_top core.length_install: 42.34 for 0 <= c <= 42.34; c for c >= 42.34
- Q9 0.5 and 0.75 m: park 959.84 z_A, stroke 775.00 mm, L L_min 885.00, at anchor_z 885.84
  - 0.5 and 0.75 m, park: 959.84 for 0 <= c <= 117.34; 842.50 + c for c >= 117.34
  - 0.5 and 0.75 m, lowest stop: 184.84 for 0 <= c <= 292.34; c - 107.50 for c >= 292.34
  - 0.5 and 0.75 m, lift stroke: 775.00 for 0 <= c <= 117.34; 657.66 + c for 117.34 <= c <= 292.34; 950.00 for c >= 292.34
  - 0.5 and 0.75 m, L L_min: 885.00 for 0 <= c <= 117.34; 767.66 + c for 117.34 <= c <= 292.34; 1060.00 for c >= 292.34
  - 0.5 and 0.75 m, L at anchor_z: 885.84 for 0 <= c <= 117.34; 768.50 + c for c >= 117.34
  - 0.5 and 0.75 m, stop core.length_capture: 184.84 for 0 <= c <= 292.34; c - 107.50 for c >= 292.34
  - 0.5 and 0.75 m, stop core.length_install: 184.84 for 0 <= c <= 42.34; 142.50 + c for c >= 42.34
  - 0.5 and 0.75 m, start core.length_capture: 834.84 for 0 <= c <= 292.34; 542.50 + c for c >= 292.34
  - 0.5 and 0.75 m, start core.length_install: 834.84 for 0 <= c <= 42.34; 792.50 + c for c >= 42.34
  - 0.5 and 0.75 m, start_minus_core_top core.length_capture: 292.34 for 0 <= c <= 292.34; c for c >= 292.34
  - 0.5 and 0.75 m, start_minus_core_top core.length_install: 42.34 for 0 <= c <= 42.34; c for c >= 42.34
- Q9 plus 1 m: park 1209.84 z_A, stroke 1025.00 mm, L L_min 1135.00, at anchor_z 1135.84
  - plus 1 m, park: 1209.84 for 0 <= c <= 117.34; 1092.50 + c for c >= 117.34
  - plus 1 m, lowest stop: 184.84 for 0 <= c <= 292.34; c - 107.50 for c >= 292.34
  - plus 1 m, lift stroke: 1025.00 for 0 <= c <= 117.34; 907.66 + c for 117.34 <= c <= 292.34; 1200.00 for c >= 292.34
  - plus 1 m, L L_min: 1135.00 for 0 <= c <= 117.34; 1017.66 + c for 117.34 <= c <= 292.34; 1310.00 for c >= 292.34
  - plus 1 m, L at anchor_z: 1135.84 for 0 <= c <= 117.34; 1018.50 + c for c >= 117.34
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
- load: highest point 1969.84 z_S, margin to the 2000 mm soft target 30.16 mm (spec values, not drawn)
- start: highest point 1844.84 z_S, margin to the 2000 mm soft target 155.16 mm (spec values, not drawn)
- capture_end: highest point 1285.00 z_S, margin to the 2000 mm soft target 715.00 mm (spec values, not drawn)
- park: highest point 1969.84 z_S, margin to the 2000 mm soft target 30.16 mm (spec values, not drawn)

## Reported values, drawn (s1_side_poses.py r8; no threshold, never asserted)

| Quantity | Value | Basis |
|---|---|---|
| highest_point | load 1969.84 z_S (drill_top_block), margin 30.16; start 1844.84 z_S (drill_top_block), margin 155.16; capture_end 1285.00 z_S (frame_upper_a), margin 715.00; park 1969.84 z_S (drill_top_block), margin 30.16 | drawn extents over parts per pose, reference rows out; soft target jig.height_target 2000 |
| ring_position | ring underside 130 above the tip, thickness 12; load 1089.84 to 1101.84 z_A; start 964.84 to 976.84 z_A; capture_end 314.84 to 326.84 z_A; park 1089.84 to 1101.84 z_A | ring.position_above_tip, ring.thickness; check_stack pose vars ring_bottom, ring_top |
| anchor_guide_heights | anchor block 265 to 295 z_A, top-guide block 1135 to 1165 z_A, bearing lines 280 and 1150 z_A, L_t 870.00; S1-4 least margin 0.84 | jackscrew.anchor_z, anchor_allowance, top_guide_z, guide_allowance, anchor_bearing_z, guide_bearing_z; S1-4 on the drawing |
| park_rule | upper.park_z = max(max_k (max(stop.height_z, collet.core_stop_z + L_k + stop.g_stop - drill.bore_ceiling_above_tip, collet.core_stop_z + L_k + c - upper.travel_max) + upper.travel_max), stop.collar_top_z + max_k L_k) + upper.load_clearance; c = start clearance above the core top (Sean, N11); park 959.84 z_A; by plane and core length {'core_stop': {'core.length_capture': 884.84, 'core.length_install': 884.84, 'core.length_optional': '1092.50 + c for c >= 0'}, 'collar_top': {'core.length_capture': 959.84, 'core.length_install': 959.84, 'core.length_optional': 1209.84}}; c validity {'lowest stop': 292.34000000000003, 'park': 117.34000000000003, 'start max': 42.34} | spec park_rule; check_stack.reported |
| lift_stroke_q9 | 0.5 m only: 775.0 (775.00 for 0 <= c <= 117.34; 657.66 + c for 117.34 <= c <= 292.34; 950.00 for c >= 292.34); 0.5 and 0.75 m: 775.0 (775.00 for 0 <= c <= 117.34; 657.66 + c for 117.34 <= c <= 292.34; 950.00 for c >= 292.34); plus 1 m: 1025.0 (1025.00 for 0 <= c <= 117.34; 907.66 + c for 117.34 <= c <= 292.34; 1200.00 for c >= 292.34) | check_stack.reported q9_options lift_stroke, symbol_terms |
| screw_length_q9 | 0.5 m only: L_min 885.0, at anchor_z 885.8400000000001; 0.5 and 0.75 m: L_min 885.0, at anchor_z 885.8400000000001; plus 1 m: L_min 1135.0, at anchor_z 1135.84; drawn jackscrew.length 900; DN23 800 to 900 | check_stack.reported q9_options L (spec screw_length) |
| com_height | load 692.9 z_S (mass 81.50 kg, W 26.25 kg); start 641.4 z_S (mass 81.50 kg, W 26.25 kg); capture_end 432.0 z_S (mass 81.50 kg, W 26.25 kg); park 730.0 z_S (mass 65.90 kg, W 26.25 kg) | s1_mass_report.pose_data: overlay masses ASSUMED, structure DERIVED |
| tip_force | load 189 N at the frame top 1285.00 z_S, 351 N at the CoM; start 189 N at the frame top 1285.00 z_S, 379 N at the CoM; capture_end 189 N at the frame top 1285.00 z_S, 563 N at the CoM; park 153 N at the frame top 1285.00 z_S, 269 N at the CoM | s1_mass_report.pose_data: lever 304 (min footprint / 2), g 9.81; icd.tipover_statement is the old reference |

## Reported items (spec reported_items; RPT)

| ID | Item | Value | Basis | Tag |
|---|---|---|---|---|
| highest_point | Highest point at each pose and its margin to the 2000 mm soft target (jig.height_target), parts only, reference rows excluded (LF1.2-5) | load 1969.84 z_S (drill_top_block), margin 30.16; start 1844.84 z_S (drill_top_block), margin 155.16; capture_end 1285.00 z_S (frame_upper_a), margin 715.00; park 1969.84 z_S (drill_top_block), margin 30.16 | drawn extents over parts per pose, reference rows out; soft target jig.height_target 2000 | MEASURED |
| ring_position | Ring position along the drill (N1): ring underside above the cutter tip, and ring underside and top per pose | ring underside 130 above the tip, thickness 12; load 1089.84 to 1101.84 z_A; start 964.84 to 976.84 z_A; capture_end 314.84 to 326.84 z_A; park 1089.84 to 1101.84 z_A | ring.position_above_tip, ring.thickness; check_stack pose vars ring_bottom, ring_top | DERIVED |
| anchor_guide_heights | Anchor and top-guide heights the ring position sets: anchor block, top-guide block, bearing lines and span L_t, with the S1-4 least margin | anchor block 265 to 295 z_A, top-guide block 1135 to 1165 z_A, bearing lines 280 and 1150 z_A, L_t 870.00; S1-4 least margin 0.84 | jackscrew.anchor_z, anchor_allowance, top_guide_z, guide_allowance, anchor_bearing_z, guide_bearing_z; S1-4 on the drawing | DERIVED / MEASURED |
| park_rule | Re-derived park rule as an expression for Step 4, with the park tip by plane and core length and the symbol c validity ranges (N11) | upper.park_z = max(max_k (max(stop.height_z, collet.core_stop_z + L_k + stop.g_stop - drill.bore_ceiling_above_tip, collet.core_stop_z + L_k + c - upper.travel_max) + upper.travel_max), stop.collar_top_z + max_k L_k) + upper.load_clearance; c = start clearance above the core top (Sean, N11); park 959.84 z_A; by plane and core length {'core_stop': {'core.length_capture': 884.84, 'core.length_install': 884.84, 'core.length_optional': '1092.50 + c for c >= 0'}, 'collar_top': {'core.length_capture': 959.84, 'core.length_install': 959.84, 'core.length_optional': 1209.84}}; c validity {'lowest stop': 292.34000000000003, 'park': 117.34000000000003, 'start max': 42.34} | spec park_rule; check_stack.reported | DERIVED |
| lift_stroke_q9 | Lift stroke per Q9 option (0.5 m only; 0.5 and 0.75 m; plus 1 m), with the c terms | 0.5 m only: 775.0 (775.00 for 0 <= c <= 117.34; 657.66 + c for 117.34 <= c <= 292.34; 950.00 for c >= 292.34); 0.5 and 0.75 m: 775.0 (775.00 for 0 <= c <= 117.34; 657.66 + c for 117.34 <= c <= 292.34; 950.00 for c >= 292.34); plus 1 m: 1025.0 (1025.00 for 0 <= c <= 117.34; 907.66 + c for 117.34 <= c <= 292.34; 1200.00 for c >= 292.34) | check_stack.reported q9_options lift_stroke, symbol_terms | DERIVED |
| screw_length_q9 | Screw length L_min and L at the drawn anchor per Q9 option (detail 1.3 expression), against the drawn jackscrew.length 900 and DN23 800 to 900 | 0.5 m only: L_min 885.0, at anchor_z 885.8400000000001; 0.5 and 0.75 m: L_min 885.0, at anchor_z 885.8400000000001; plus 1 m: L_min 1135.0, at anchor_z 1135.84; drawn jackscrew.length 900; DN23 800 to 900 | check_stack.reported q9_options L (spec screw_length) | DERIVED |
| com_height | Centre-of-mass height per pose (overlay masses, ASSUMED) | load 692.9 z_S (mass 81.50 kg, W 26.25 kg); start 641.4 z_S (mass 81.50 kg, W 26.25 kg); capture_end 432.0 z_S (mass 81.50 kg, W 26.25 kg); park 730.0 z_S (mass 65.90 kg, W 26.25 kg) | s1_mass_report.pose_data: overlay masses ASSUMED, structure DERIVED | DERIVED |
| tip_force | Unbolted tip force at the frame top and at the CoM height per pose (icd.tipover_statement is the old-design reference) | load 189 N at the frame top 1285.00 z_S, 351 N at the CoM; start 189 N at the frame top 1285.00 z_S, 379 N at the CoM; capture_end 189 N at the frame top 1285.00 z_S, 563 N at the CoM; park 153 N at the frame top 1285.00 z_S, 269 N at the CoM | s1_mass_report.pose_data: lever 304 (min footprint / 2), g 9.81; icd.tipover_statement is the old reference | DERIVED |

Files: params.yaml 9469288a75c2, proposed_params.yaml d1413c0e6e82
