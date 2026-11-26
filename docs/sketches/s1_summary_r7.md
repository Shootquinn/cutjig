# S1 checks, revision r7

2026-11-25T21:06:27. Spec s1_spec.yaml (signed (Designer, Loftsman; pose table confirmed by Sean 2026-11-25)); script s1_side_poses.py. Frame z_S = z_A + jig.datum_a_above_floor.

| Check | Result | Measured | Threshold | Z | B | Reason |
|---|---|---|---|---|---|---|
| K1 | pass | 0 | 0 | clean 1/1 | fired 2/2 | no literal outside [-1, 0, 0.5, 1, 2], no soft-key comparison, no figure setting (s1_side_poses.py) |
| K2 | pass | 0 | 0 | clean 1/1 | fired 3/3 | 322 spec keys resolve; 121 overlay leaves sourced, legal status, no shadow |
| K3 | pass | 0 | 0 | clean 3/3 | fired 9/9 | 4 figure(s): one Axes, title, (mm) labels, equal aspect, grids, figsize, dpi 150; every text inside the saved image |
| K4 | pass | 0 | 0 | clean 4/4 | fired 11/11 | 55 label(s) carry their key value, each leader ends on its part, no two leaders cross; figure note names every not_drawn part |
| K5 | pass | 0 | 0 | clean 3/3 | fired 18/18 | 343 tagged artist(s) projected per kind, axis and spec projection (view normal Y) |
| K6 | pass | 0.0 | 0.05 | clean 4/4 | fired 10/10 | 231 z_rule(s) match drawn extents within 0.05 mm; check_stack imports and anchors clean |
| K7 | pass | 0 | 0 | clean 17/17 | fired 33/33 | 617 pair test(s) clean; states ['C', 'F', 'N', 'depth-separated', 'plan-contact', 'plan-separated', 'swept:C', 'swept:F', 'swept:depth-separated', 'swept:plan-s |
| K8 | pass | 0 | 0 | clean 8/8 | fired 41/41 | 346 predicate(s) hold, axes not inverted |
| K9 | pass | 0 | 0 | clean 3/3 | fired 7/7 | every spec row drawn, every tagged artist in the spec (58 rows) |
| S1-1 | pass | 650.0 | [534.93, 650] | clean 1/1 | fired 2/2 | drawn start tip minus end-of-capture tip 650.00 mm against [534.93, 650] |
| S1-2 | pass | 125.0 | > 0 | clean 1/1 | fired 2/2 | park tip above the highest class start by 125.00 mm |
| S1-3 | pass | {'core.length_capture': 367.34, 'core.length_install': 117.34} | >= 0 | clean 1/1 | fired 1/1 | margins over core_stop {'core.length_capture': 367.34, 'core.length_install': 117.34} |
| S1-4 | pass | 0.84 | >= 0 | clean 1/1 | fired 2/2 | nut inside travel at every pose, least margin 0.84 mm |
| S1-5a | pass | 192.34 | 25 | clean 1/1 | fired 1/1 | bore ceiling minus capture-core (core_750) top at end of capture 192.34 mm, need 25 |
| S1-5b | pass | 142.0 | 10 | clean 1/1 | fired 1/1 | 91 pairs, least certified clearance 142.00 mm |
| S1-6 | pass | 0 | 0 | clean 1/1 | fired 1/1 | 8 screw projections at r cos(theta), depth r sin(theta) |
| S1-7 | pass | 607.66 | 534.93 | clean 1/1 | fired 1/1 | capture-core (core_750) top at start minus end-of-capture tip 607.66 mm, need 534.93 (spare 72.73) |
| X1 | pass | 0 | 0 | clean 1/1 | fired 2/2 | 47 shared row(s) compared on place, z_rule, plan_poly; skipped 3: base_frame plan_poly (only in s2), base_plate plan_poly (only in s2), keepout place (only in s |

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

Files: params.yaml 9469288a75c2, proposed_params.yaml d647105fe3d3
