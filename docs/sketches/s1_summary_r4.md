# S1 checks, revision r4

2026-11-25T13:49:52. Spec s1_spec.yaml (signed (Designer, Loftsman; pose table confirmed by Sean 2026-11-25)); script s1_side_poses.py. Frame z_S = z_A + jig.datum_a_above_floor.

| Check | Result | Measured | Threshold | Z | B | Reason |
|---|---|---|---|---|---|---|
| K1 | pass | 0 | 0 | clean 1/1 | fired 2/2 | no literal outside [-1, 0, 0.5, 1, 2], no soft-key comparison, no figure setting (s1_side_poses.py) |
| K2 | pass | 0 | 0 | clean 1/1 | fired 3/3 | 284 spec keys resolve; 103 overlay leaves sourced, legal status, no shadow |
| K3 | pass | 0 | 0 | clean 1/1 | fired 7/7 | 4 figure(s): one Axes, title, (mm) labels, equal aspect, grids, figsize, dpi 150 |
| K4 | pass | 0 | 0 | clean 1/1 | fired 3/3 | 55 label(s) carry their key value |
| K5 | pass | 0 | 0 | clean 2/2 | fired 6/6 | 327 tagged artist(s) projected per kind, axis and spec projection (view normal Y) |
| K6 | pass | 0.0 | 0.05 | clean 3/3 | fired 8/8 | 215 z_rule(s) match drawn extents within 0.05 mm; check_stack imports and anchors clean |
| K7 | pass | 0 | 0 | clean 11/11 | fired 20/20 | 477 pair test(s) clean; states ['C', 'F', 'G', 'N', 'depth-separated', 'plan-contact', 'plan-separated', 'swept:F', 'swept:G', 'swept:depth-separated', 'swept:p |
| K8 | pass | 0 | 0 | clean 5/5 | fired 16/16 | 330 predicate(s) hold, axes not inverted |
| K9 | pass | 0 | 0 | clean 2/2 | fired 5/5 | every spec row drawn, every tagged artist in the spec (54 rows) |
| S1-1 | pass | 650.0 | [534.93, 650] | clean 1/1 | fired 2/2 | drawn start tip minus end-of-capture tip 650.00 mm against [534.93, 650] |
| S1-2 | pass | 125.0 | > 0 | clean 1/1 | fired 2/2 | park tip above the highest class start by 125.00 mm |
| S1-3 | pass | {'core.length_capture': 367.34, 'core.length_install': 117.34} | >= 0 | clean 1/1 | fired 1/1 | margins over core_stop {'core.length_capture': 367.34, 'core.length_install': 117.34} |
| S1-4 | pass | 0.84 | >= 0 | clean 1/1 | fired 2/2 | nut inside travel at every pose, least margin 0.84 mm |
| S1-5a | pass | 192.34 | 25 | clean 1/1 | fired 1/1 | bore ceiling minus capture-core (core_750) top at end of capture 192.34 mm, need 25 |
| S1-5b | pass | 142.0 | 10 | clean 1/1 | fired 1/1 | 77 pairs, least certified clearance 142.00 mm |
| S1-6 | pass | 0 | 0 | clean 1/1 | fired 1/1 | 8 screw projections at r cos(theta), depth r sin(theta) |
| S1-7 | pass | 607.66 | 534.93 | clean 1/1 | fired 1/1 | capture-core (core_750) top at start minus end-of-capture tip 607.66 mm, need 534.93 (spare 72.73) |

| Check | Cause of red |
|---|---|

Reported (no threshold):
- Park tip 959.84 z_A (entry plane collar_top); highest class start 834.84 z_A; lift stroke 775.00 mm; S1-3 load plane core_stop
- Q9 0.5 m only: park 959.84 z_A, stroke 775.00 mm, L L_min 885.00, at anchor_z 885.84
- Q9 0.5 and 0.75 m: park 959.84 z_A, stroke 775.00 mm, L L_min 885.00, at anchor_z 885.84
- Q9 plus 1 m: park 1209.84 z_A, stroke 1025.00 mm, L L_min 1135.00, at anchor_z 1135.84
- Collar top recomputed 159.84 z_A against params stop.collar_top_z 159.84
- Park tip z_A by plane and core length: core_stop: length_capture 884.84, length_install 884.84, length_optional 1092.50; collar_top: length_capture 959.84, length_install 959.84, length_optional 1209.84
- Start tip minus capture-core top (core.length_install) on the core stop: 42.34 mm (end tip + drill_advance_500core = 719.77 z_A; core top 792.50 z_A)
- load: highest point 1969.84 z_S, margin to the 2000 mm soft target 30.16 mm (spec values, not drawn)
- start: highest point 1844.84 z_S, margin to the 2000 mm soft target 155.16 mm (spec values, not drawn)
- capture_end: highest point 1285.00 z_S, margin to the 2000 mm soft target 715.00 mm (spec values, not drawn)
- park: highest point 1969.84 z_S, margin to the 2000 mm soft target 30.16 mm (spec values, not drawn)

Files: params.yaml 9469288a75c2, proposed_params.yaml bc68ca444fb8

## Reported values, drawn (s1_mass_report.py; no threshold, never asserted)

| Pose | Highest drawn point z_S (part) | Margin to 2000 soft target | Ring z_S | Mass kg | COM z_S | Tip force at COM N | Tip force at frame top N |
|---|---|---|---|---|---|---|---|
| load | 1969.84 (drill_top_block) | 30.16 | 1149.84 to 1161.84 | 76.07 | 664.8 | 341 | 177 |
| start | 1844.84 (drill_top_block) | 155.16 | 1024.84 to 1036.84 | 76.07 | 616.4 | 368 | 177 |
| capture_end | 1285.00 (frame_upper_a) | 715.00 | 374.84 to 386.84 | 76.07 | 427.1 | 531 | 177 |
| park | 1969.84 (drill_top_block) | 30.16 | 1149.84 to 1161.84 | 60.47 | 698.0 | 258 | 140 |

- Ring (N1): ring.position_above_tip 130 mm, bottom of ring plate above the tip; ring thickness 12.
- Anchors: jackscrew.anchor_z 265 z_A, drawn 325.00 to 355.00 z_S; top guides: jackscrew.top_guide_z 1165 z_A, drawn 1195.00 to 1225.00 z_S; screw length jackscrew.length 900.
- Park rule for Step 4: upper.park_z = max(max_k (max(stop.height_z, collet.core_stop_z + L_k + stop.g_stop - drill.bore_ceiling_above_tip) + upper.travel_max), stop.collar_top_z + max_k L_k) + upper.load_clearance
- Tip force: horizontal force that tips the unbolted jig about the nearest base edge, lever 304 mm (min footprint / 2, COM on the drill axis by three-fold symmetry), g 9.81. Masses: overlay ASSUMED; structure DERIVED; working values {'rho_al_kg_m3': 2700, 'rho_steel_kg_m3': 7850, 'nema17_kg': 0.35} ASSUMED. Receiver, collet, holder, wing nut, anchor and guide blocks omitted.
- Old reference icd.tipover_statement: unbolted tip force 158 N at COM (0.69 m), 68 N at column top; bolt-down required with cutter above z = 400 mm
