# S1 checks, revision r0

2026-11-25T11:58:51. Spec s1_spec.yaml (signed (Designer, Loftsman; pose table confirmed by Sean 2026-11-25)); script stubs\s1_stub.py. Frame z_S = z_A + jig.datum_a_above_floor.

| Check | Result | Measured | Threshold | Z | B | Reason |
|---|---|---|---|---|---|---|
| K1 | pass | 0 | 0 | clean 1/1 | fired 2/2 | no literal outside [-1, 0, 0.5, 1, 2], no soft-key comparison, no figure setting (s1_stub.py) |
| K2 | pass | 0 | 0 | clean 1/1 | fired 3/3 | 210 spec keys resolve; 103 overlay leaves sourced, legal status, no shadow |
| K3 | pass | 0 | 0 | clean 1/1 | fired 7/7 | 4 figure(s): one Axes, title, (mm) labels, equal aspect, grids, figsize, dpi 150 |
| K4 | fail | 43 | 0 | clean 1/1 | fired 3/3 | load/wingnut: no annotation label:wingnut; load/core_750: no annotation label:core_750; load/drill_head: no annotation label:drill_head; load/drill_tube: no ann |
| K5 | pass | 0 | 0 | clean 1/1 | fired 5/5 | 4 tagged artist(s) projected per kind, axis and spec projection (view normal Y) |
| K6 | fail | 0.0 | 0.05 | clean 3/3 | fired 7/7 | load/base_frame: z_rule [0.00, 60.00] z_S, nothing drawn; load/base_plate: z_rule [60.00, 72.00] z_S, nothing drawn; load/receiver: z_rule [72.00, 188.50] z_S,  |
| K7 | fail | 285 | 0 | clean 10/10 | fired 13/13 | load/base_frame/base_plate C: untestable, base_frame/base_plate not drawn; load/base_plate/receiver C: untestable, base_plate/receiver not drawn; load/drill_tub |
| K8 | fail | 226 | 0 | clean 3/3 | fired 13/13 | load/base_frame below base_plate: untestable, base_frame not drawn; load/collet taper : untestable, collet not drawn; load/wingnut below drill_head: untestable, |
| K9 | fail | 175 | 0 | clean 1/1 | fired 4/4 | load: spec row base_frame has no patch; load: spec row base_plate has no patch; load: spec row receiver has no patch; load: spec row collet has no patch; load:  |
| S1-1 | fail | None | None | clean 1/1 | fired 2/2 | measured: none; drill_head not drawn in pose start |
| S1-2 | fail | None | None | clean 1/1 | fired 1/1 | measured: none; drill_head not drawn in pose park |
| S1-3 | fail | None | None | clean 1/1 | fired 1/1 | measured: none; drill_head not drawn in pose park |
| S1-4 | fail | None | None | clean 1/1 | fired 2/2 | measured: none; anchor_a not drawn in pose load |
| S1-5a | fail | None | None | clean 1/1 | fired 1/1 | measured: none; bore_ceiling not drawn in pose capture_end |
| S1-5b | fail | None | None | clean 1/1 | fired 1/1 | measured: none; ring not drawn in pose capture_end |
| S1-6 | fail | None | None | clean 1/1 | fired 1/1 | measured: none; screw_a not drawn in pose load |
| S1-7 | fail | None | None | clean 1/1 | fired 1/1 | measured: none; core_750 not drawn in pose start |

| Check | Cause of red |
|---|---|
| K4 | content |
| K6 | absent |
| K7 | absent |
| K8 | absent |
| K9 | content |
| S1-1 | absent |
| S1-2 | absent |
| S1-3 | absent |
| S1-4 | absent |
| S1-5a | absent |
| S1-5b | absent |
| S1-6 | absent |
| S1-7 | absent |

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

Files: params.yaml 9469288a75c2, proposed_params.yaml 0b160d002b83
