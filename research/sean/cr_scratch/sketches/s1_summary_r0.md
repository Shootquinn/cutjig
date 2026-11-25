# S1 checks, revision r0

2026-11-24T23:32:48. Spec s1_spec.yaml (draft, unsigned); script stubs\s1_stub.py. Frame z_S = z_A + jig.datum_a_above_floor.

| Check | Result | Measured | Threshold | Z | B | Reason |
|---|---|---|---|---|---|---|
| K1 | pass | 0 | 0 | clean 1/1 | fired 2/2 | no literal outside [-1, 0, 0.5, 1, 2], no soft-key comparison, no figure setting (s1_stub.py) |
| K2 | pass | 0 | 0 | clean 1/1 | fired 3/3 | 138 spec keys resolve; 81 overlay leaves sourced, legal status, no shadow |
| K3 | pass | 0 | 0 | clean 1/1 | fired 7/7 | 4 figure(s): one Axes, title, (mm) labels, equal aspect, grids, figsize, dpi 150 |
| K4 | fail | 45 | 0 | clean 1/1 | fired 3/3 | load/wingnut: no annotation label:wingnut; load/core_500: no annotation label:core_500; load/core_750: no annotation label:core_750; load/drill_head: no annotat |
| K5 | pass | 0 | 0 | clean 1/1 | fired 5/5 | 4 tagged artist(s) projected per kind, axis and spec projection (view normal Y) |
| K6 | fail | 0.0 | 0.05 | clean 2/2 | fired 5/5 | load/base_frame: z_rule [0.00, 60.00] z_S, nothing drawn; load/base_plate: z_rule [60.00, 72.00] z_S, nothing drawn; load/receiver: z_rule [72.00, 188.50] z_S,  |
| K7 | fail | 80 | 0 | clean 7/7 | fired 10/10 | load/base_frame/base_plate C: untestable, base_frame/base_plate not drawn; load/base_plate/receiver C: untestable, base_plate/receiver not drawn; load/ring/fram |
| K8 | fail | 177 | 0 | clean 2/2 | fired 11/11 | load/base_frame below base_plate: untestable, base_frame not drawn; load/collet taper : untestable, collet not drawn; load/wingnut below drill_head: untestable, |
| K9 | fail | 141 | 0 | clean 1/1 | fired 4/4 | load: spec row base_frame has no patch; load: spec row base_plate has no patch; load: spec row receiver has no patch; load: spec row collet has no patch; load:  |
| S1-1 | fail | None | None | not run at 1.0 (Z fixture from the signed spec, 1.1) | not run at 1.0 (B fixture from the signed spec, 1.1) | measured: none; drill_head not drawn in pose start |
| S1-2 | fail | None | None | not run at 1.0 (Z fixture from the signed spec, 1.1) | not run at 1.0 (B fixture from the signed spec, 1.1) | measured: none; drill_head not drawn in pose park |
| S1-3 | fail | None | None | not run at 1.0 (Z fixture from the signed spec, 1.1) | not run at 1.0 (B fixture from the signed spec, 1.1) | measured: none; drill_head not drawn in pose park |
| S1-4 | fail | None | None | not run at 1.0 (Z fixture from the signed spec, 1.1) | not run at 1.0 (B fixture from the signed spec, 1.1) | measured: none; anchor_a not drawn in pose load |
| S1-5a | fail | None | None | not run at 1.0 (Z fixture from the signed spec, 1.1) | not run at 1.0 (B fixture from the signed spec, 1.1) | measured: none; bore_ceiling not drawn in pose capture_end |
| S1-5b | fail | None | None | not run at 1.0 (Z fixture from the signed spec, 1.1) | not run at 1.0 (B fixture from the signed spec, 1.1) | measured: none; ring not drawn in pose capture_end |
| S1-6 | fail | None | None | not run at 1.0 (Z fixture from the signed spec, 1.1) | not run at 1.0 (B fixture from the signed spec, 1.1) | measured: none; screw_a not drawn in pose load |

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

Reported (no threshold):
- Lift stroke (draft park rule, load plane core_stop): 830.16 mm
- Collar top recomputed 159.84 z_A against params stop.collar_top_z 159.84
- Park tip z_A by load plane and core length: core_stop: length_capture 1015.00, length_install 1015.00, length_optional 1092.50; collar_top: length_capture 1015.00, length_install 1015.00, length_optional 1209.84
- Start tip minus 0.5 m core top on the core stop: 292.34 mm (end tip + drill_advance_500core = 719.77 z_A; core top 542.50 z_A)
- load: highest point 2025.00 z_S, margin to the 2000 mm soft target -25.00 mm (spec values, not drawn)
- start: highest point 1844.84 z_S, margin to the 2000 mm soft target 155.16 mm (spec values, not drawn)
- capture_end: highest point 1260.00 z_S, margin to the 2000 mm soft target 740.00 mm (spec values, not drawn)
- park: highest point 2025.00 z_S, margin to the 2000 mm soft target -25.00 mm (spec values, not drawn)

Files: params.yaml 9469288a75c2, proposed_params.yaml bd38a0ba1f01
