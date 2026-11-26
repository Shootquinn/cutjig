# S2 checks, revision r5

2026-11-25T21:19:39. Spec s2_spec.yaml (signed (Designer, Loftsman 1.2 (b), with re-check sections; step1.2_designer_spec_signoff.md, step1.2_loftsman_spec_signoff.md); 1.2 (c) gear section field added for the plan annulus (signed at (c) by the Loftsman, Designer, Topologist and Software Engineer after P5f); 1.2 (h) r2 edits (gear ticks and shape text, label_theta, reference rows, F6 label text, pinion|gear_hub G 3, S2-5b over moves: true) re-checked by the Loftsman and the Topologist; r3 edits (tick toe pinion.r_toe 96.54 per Design Notes 29, plan_style: stand_in on the ties) signed by the Designer (sign-off r3); r4 edits (outline_matches on base_plate, stand_in_owner on the ties, label_side left on descent_stop) signed by the Designer (sign-off r4); r5 edit (label_theta 150 on descent_stop, Designer sign-off r4 FIX D4-1; step1.2_engineer_revision_r5.md)); script s2_plan.py. Frame z_S = z_A + jig.datum_a_above_floor.

| Check | Result | Measured | Threshold | Z | B | Reason |
|---|---|---|---|---|---|---|
| K1 | pass | 0 | 0 | clean 1/1 | fired 2/2 | no literal outside [-1, 0, 0.5, 1, 2], no soft-key comparison, no figure setting (s2_plan.py) |
| K2 | pass | 0 | 0 | clean 1/1 | fired 3/3 | 420 spec keys resolve; 121 overlay leaves sourced, legal status, no shadow |
| K3 | pass | 0 | 0 | clean 3/3 | fired 9/9 | 1 figure(s): one Axes, title, (mm) labels, equal aspect, grids, figsize, dpi 150; every text inside the saved image |
| K4 | pass | 0 | 0 | clean 4/4 | fired 11/11 | 14 label(s) carry their key value, each leader ends on its part, no two leaders cross; figure note names every not_drawn part |
| K5 | pass | 0 | 0 | clean 3/3 | fired 18/18 | 105 tagged artist(s) projected per kind, axis and spec projection (view normal Z) |
| K6 | pass | 0.0 | 0.05 | clean 4/4 | fired 10/10 | 69 plan centre(s) on the spec within 0.05 mm (z not drawn in plan); check_stack imports and anchors clean |
| K7 | pass | 0 | 0 | clean 17/17 | fired 33/33 | 1292 plan pair test(s) clean over 4 pose(s); states ['G', 'N', 'plan-contact', 'swept:F', 'swept:G', 'swept:z-separated', 'swept:z-touch', 'undeclared:F', 'unde |
| K8 | pass | 0 | 0 | clean 8/8 | fired 41/41 | 190 predicate(s) hold, axes not inverted |
| K9 | pass | 0 | 0 | clean 3/3 | fired 7/7 | every spec row drawn, every tagged artist in the spec (70 rows) |
| S2-1 | pass | 0.0 | 0.1 | clean 1/1 | fired 1/1 | screws [30.0, 150.0, 270.0], pinions [90.0, 210.0, 330.0], phase 60 within 0.000 |
| S2-2 | pass | 52.8 | 10 | clean 1/1 | fired 1/1 | least margin 52.80 mm over g_min 10 |
| S2-3 | pass | 0.0 | 0.05 | clean 1/1 | fired 1/1 | pitch points {'pinion_a': 125.0, 'pinion_b': 125.0, 'pinion_c': 125.0} at the gear pitch radius 125.00 within 0.000 |
| S2-4 | pass | 0.0 | 0.05 | clean 1/1 | fired 1/1 | 4 centres within 0.000 mm |
| S2-5a | pass | 11.713 | F | clean 1/1 | fired 1/1 | 27 fixed parts clear of the sector, least 11.71 mm |
| S2-5b | pass | 19.84 | 10 | clean 1/1 | fired 3/3 | 10 moving parts in the sector, least 19.84 mm above the hand band (drill_head) |
| S2-6 | pass | 0 | 0 | clean 1/1 | fired 2/2 | 3 members seated |
| X1 | pass | 0 | 0 | clean 1/1 | fired 2/2 | 47 shared row(s) compared on place, z_rule, plan_poly; skipped 3: base_frame plan_poly (only in s2), base_plate plan_poly (only in s2), keepout place (only in s |

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

## Reported values, drawn (s2_plan.py r5; no threshold, never asserted)

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

Files: params.yaml 9469288a75c2, proposed_params.yaml d647105fe3d3
