# S1 checks, revision r10

2026-11-27T20:37:03. Spec s1_spec.yaml (signed (Designer, Loftsman; pose table confirmed by Sean 2026-11-25); r8 edits at 1.3 P6 under the orchestrator-named exceptions (a) to (f)); script s1_side_poses.py. Frame z_S = z_A + jig.datum_a_above_floor.

| Check | Result | Measured | Threshold | Z | B | Reason |
|---|---|---|---|---|---|---|
| K1 | pass | 0 | 0 | clean 1/1 | fired 3/3 | no literal outside [-1, 0, 0.5, 1, 2], no soft-key comparison, no figure setting (s1_side_poses.py) |
| K2 | pass | 0 | 0 | clean 2/2 | fired 7/7 | 384 spec keys resolve; 203 overlay leaves sourced, legal status, no shadow; 24 expr leaves agree within 0.05 |
| K3 | pass | 0 | 0 | clean 4/4 | fired 11/11 | 4 figure(s): one Axes, title, (mm) labels, equal aspect, grids, figsize, dpi 150; every text inside the saved image |
| K4 | pass | 0 | 0 | clean 14/14 | fired 64/64 | 55 label(s) carry their key value, each leader ends on its part, no two leaders cross; figure note names every not_drawn part |
| K5 | pass | 0 | 0 | clean 9/9 | fired 76/76 | 495 tagged artist(s) projected per kind, axis and spec projection (view normal Y) |
| K6 | pass | 0.0 | 0.05 | clean 6/6 | fired 12/12 | 239 z_rule(s) match drawn extents within 0.05 mm; check_stack imports and anchors clean |
| K7 | pass | 0 | 0 | clean 19/19 | fired 38/38 | 638 pair test(s) clean; states ['C', 'F', 'N', 'depth-separated', 'plan-contact', 'plan-separated', 'swept:C', 'swept:F', 'swept:depth-separated', 'swept:plan-s |
| K8 | pass | 0 | 0 | clean 23/23 | fired 126/128 | 386 predicate(s) hold, axes not inverted |
| K9 | pass | 0 | 0 | clean 6/6 | fired 9/9 | every spec row drawn, every tagged artist in the spec (60 rows) |
| S1-1 | pass | 650.0 | [534.93, 650] | clean 1/1 | fired 2/2 | drawn start tip minus end-of-capture tip 650.00 mm against [534.93, 650] |
| S1-2 | pass | 125.0 | > 0 | clean 1/1 | fired 2/2 | park tip above the highest class start by 125.00 mm |
| S1-3 | pass | {'core.length_capture': 367.34, 'core.length_install': 117.34} | >= 0 | clean 1/1 | fired 1/1 | margins over core_stop {'core.length_capture': 367.34, 'core.length_install': 117.34} |
| S1-4 | pass | 0.84 | >= 0 | clean 1/1 | fired 2/2 | nut inside travel at every pose, least margin 0.84 mm |
| S1-5a | pass | 192.34 | 25 | clean 1/1 | fired 1/1 | bore ceiling minus capture-core (core_750) top at end of capture 192.34 mm, need 25 |
| S1-5b | pass | 142.0 | 10 | clean 1/1 | fired 1/1 | 91 pairs, least certified clearance 142.00 mm |
| S1-6 | pass | 0 | 0 | clean 1/1 | fired 1/1 | 8 screw projections at r cos(theta), depth r sin(theta) |
| S1-7 | pass | 607.66 | 534.93 | clean 1/1 | fired 1/1 | capture-core (core_750) top at start minus end-of-capture tip 607.66 mm, need 534.93 (spare 72.73) |
| X1 | pass | 0 | 0 | clean 2/2 | fired 6/6 | 72 shared row(s) compared on place, z_rule, plan_poly; skipped 3: base_frame plan_poly (only in s2, s3), base_plate plan_poly (only in s2, s3, s4), keepout plac |
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

## Reported values, drawn (s1_mass_report.py; no threshold, never asserted)

| Pose | Highest drawn point z_S (part) | Margin to 2000 soft target | Ring z_S | Mass kg | W kg (moving, W_kg items) | COM z_S | Tip force at COM N | Tip force at frame top N |
|---|---|---|---|---|---|---|---|---|
| load | 1969.84 (drill_top_block) | 30.16 | 1149.84 to 1161.84 | 81.50 | 26.25 | 692.9 | 351 | 189 |
| start | 1844.84 (drill_top_block) | 155.16 | 1024.84 to 1036.84 | 81.50 | 26.25 | 641.4 | 379 | 189 |
| capture_end | 1285.00 (frame_upper_a) | 715.00 | 374.84 to 386.84 | 81.50 | 26.25 | 432.0 | 563 | 189 |
| park | 1969.84 (drill_top_block) | 30.16 | 1149.84 to 1161.84 | 65.90 | 26.25 | 730.0 | 269 | 153 |

- Ring (N1): ring.position_above_tip 130 mm, bottom of ring plate above the tip; ring thickness 12.
- Anchors: jackscrew.anchor_z 265 z_A, drawn 325.00 to 355.00 z_S; top guides: jackscrew.top_guide_z 1165 z_A, drawn 1195.00 to 1225.00 z_S; screw length jackscrew.length 900.
- Park rule for Step 4: upper.park_z = max(max_k (max(stop.height_z, collet.core_stop_z + L_k + stop.g_stop - drill.bore_ceiling_above_tip, collet.core_stop_z + L_k + c - upper.travel_max) + upper.travel_max), stop.collar_top_z + max_k L_k) + upper.load_clearance; c = start clearance above the core top (Sean, N11)
- Moving mass W (s3_spec.yaml load_cases.W_kg items): 26.25 kg, the top-end block 2 kg included (1.3 (h) r3, LF1.3-2).
- Tip force: horizontal force that tips the unbolted jig about the nearest base edge, lever 304 mm (min footprint / 2, COM on the drill axis by three-fold symmetry), g 9.81. Masses: overlay ASSUMED; structure DERIVED; working densities {'rho_al_kg_m3': 2700, 'rho_steel_kg_m3': 7850} ASSUMED. Receiver, collet, holder, wing nut, anchor and guide blocks omitted.
- Old reference icd.tipover_statement: unbolted tip force 158 N at COM (0.69 m), 68 N at column top; bolt-down required with cutter above z = 400 mm
