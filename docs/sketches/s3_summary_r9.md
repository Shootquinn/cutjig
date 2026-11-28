# S3 checks, revision r9

2026-11-27T21:54:40. Spec s3_spec.yaml (accepted at S3 r7 (Sean M2 2026-11-26, 'Apply fixes as r7, accept'; Design Notes 13; --accept s3 --rev 7 at 1.3 ORCH-B); signed by The Designer (part list) and The Loftsman at 1.3 (b) P2f2. History: 1.3 (b), The Engineer, 2026-11-26; P2f fix pass (Designer FIX 1 to 6, Loftsman FIX 1 to 6, orchestrator rulings); P2f2 (Designer re-sign FIX A to D, Loftsman FIX 8; nut shoulder screws per the revised orchestrator ruling), research/sean/cr_scratch/step1.3_engineer_spec_fixes.md; 1.3 P6 edits (a), (e), (f), step1.3_engineer_draw_r1.md; 1.3 (h) r2 edits for Designer re-sign (chain link kinds and the base-route reroute TP1.3-10, not_drawn omit fields TP1.3-12, plan_axes arc TP1.3-13, screw_c root lines TP1.3-15, lever u expressions TP1.3-19), step1.3_engineer_revision_r2.md; 1.3 (h) r6 edits (labels print computed loads; nut station labels with z_S from the stack; load_comp_c leader on the arrow shaft); 1.3 (h) r5 edits (load_comp_c cases label M1 S3 r4 F1, hold label lead angle from stall.lead_angle N5, label anchors DR4-1); 1.3 (h) r4 edits (span_lt label text M1 S3 r3 F1, hatch_alt '||'); 1.3 (h) r3 edits (Designer r2 values picks 2, 3 (offset per orchestrator ruling u -110), 4 ('--' per orchestrator ruling), 5, 7, 8, 9; Loftsman LF1.3-10; Topologist R2-5), step1.3_engineer_revision_r3.md); script s3_jackscrew_section.py. Frame z_S = z_A + jig.datum_a_above_floor.

| Check | Result | Measured | Threshold | Z | B | Reason |
|---|---|---|---|---|---|---|
| K1 | pass | 0 | 0 | clean 1/1 | fired 3/3 | no literal outside [-1, 0, 0.5, 1, 2], no soft-key comparison, no figure setting (s3_jackscrew_section.py) |
| K2 | pass | 0 | 0 | clean 2/2 | fired 7/7 | 471 spec keys resolve; 203 overlay leaves sourced, legal status, no shadow; 24 expr leaves agree within 0.05 |
| K3 | pass | 0 | 0 | clean 4/4 | fired 11/11 | [section] 1 figure(s): one Axes, title, (mm) labels, equal aspect, grids, figsize, dpi 150; every text inside the saved image / [inset_plan] 1 figure(s): one Ax |
| K4 | pass | 0 | 0 | clean 14/14 | fired 64/64 | [section] 21 label(s) carry their key value, each leader ends on its part, no two leaders cross; figure note names every not_drawn part / [inset_plan] 3 label(s |
| K5 | pass | 0 | 0 | clean 9/9 | fired 76/76 | [section] 156 tagged artist(s) projected per kind, axis and spec projection (view normal X) / [inset_plan] 36 tagged artist(s) projected per kind, axis and spec |
| K6 | pass | 0.0 | 0.05 | clean 6/6 | fired 12/12 | [section] 50 z_rule(s) match drawn extents within 0.05 mm; check_stack imports and anchors clean / [inset_plan] 22 plan centre(s) on the spec within 0.05 mm (z  |
| K7 | pass | 0 | 0 | clean 19/19 | fired 38/38 | [section] 274 pair test(s) clean; states ['C', 'F', 'G', 'N', 'depth-separated', 'undeclared:C', 'undeclared:F', 'undeclared:depth-separated'] / [inset_plan] 44 |
| K8 | pass | 0 | 0 | clean 23/23 | fired 128/128 | [section] 248 predicate(s) hold, axes not inverted / [inset_plan] 75 predicate(s) hold, axes not inverted |
| K9 | pass | 0 | 0 | clean 6/6 | fired 9/9 | [section] every spec row drawn, every tagged artist in the spec (51 rows) / [inset_plan] every spec row drawn, every tagged artist in the spec (23 rows) |
| S3-1 | pass | 25.84 | 0 | clean 1/1 | fired 2/2 | tension segment least 25.84 mm (nut bottom above the anchor line in every pose; cut arrow +Z) |
| S3-2 | pass | 3.974 | 3 | clean 2/2 | fired 2/2 | P_cr 1363.8 N (K 0.7, L_t 870.00); least margin 3.97 (stall_up) against SF 3 |
| S3-3 | pass | 0 | 0 | clean 1/1 | fired 17/17 | 48 chain link(s) closed in the cut case; listed: c drill_head/core_750 declared; c base_plate/base_frame face_record; c base_frame/frame_upper_c fastened; c fra |
| X1 | pass | 0 | 0 | clean 2/2 | fired 6/6 | 72 shared row(s) compared on place, z_rule, plan_poly; skipped 3: base_frame plan_poly (only in s2, s3), base_plate plan_poly (only in s2, s3, s4), keepout plac |
| SYM | pass | 0 | 0 | clean 1/1 | fired 3/3 | 18 row pair(s) compared on z_rule, place in 4 spec(s) |
| RPT | pass | 0 | 0 | clean 3/3 | fired 6/6 | 10 reported item(s) declared, every one has a value |
| SYM-P | pass | 0 | 0 | clean 1/1 | fired 1/1 | keys_read covers every key read by place and z_rule of the SYM rows |

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

## Reported values, drawn (s3_jackscrew_section.py r9; no threshold, never asserted)

| Quantity | Value | Basis |
|---|---|---|
| L_min | 0.5 m only: L_min 885.00, at anchor_z 885.84; 0.5 and 0.75 m: L_min 885.00, at anchor_z 885.84; plus 1 m: L_min 1135.00, at anchor_z 1135.84 (DN23 800 to 900); drawn bar 911.00 (screw_end_c bottom to guide_c top); with the shoulder-screw head 4.55 above the housing top: 0.5 m only: L_min 889.55, at anchor_z 890.39; 0.5 and 0.75 m: L_min 889.55, at anchor_z 890.39; plus 1 m: L_min 1139.55, at anchor_z 1140.39 | check_stack.reported q9_options, spec screw_length (S1 expressions); drawn pieces screw_end_c, guide_c, nut_screws_c, nut_housing_c (section Axes, MEASURED) |
| n_crit | pinned-pinned 1336 rpm (2.67 x), fixed-pinned 2086 rpm (4.17 x) against 500 rpm at 25 mm/s | L_t 870.00, d_r 8.5, E, density; fixed-pinned is the drawn end condition (K 0.7) |
| pcr_margin | floating (K 0.7, L 870.00, P_cr 1363.8 N): per screw static 15.89, capture_lift 11.38, retract_bind 7.34, stall_up 3.97; two-screw static 10.59, capture_lift 7.59, retract_bind 4.89 | floating K 1.0 (K 1.0, L 870.00, P_cr 668.2 N): per screw static 7.79, capture_lift 5.58, retract_bind 3.60, stall_up 1.95; two-screw static 5.19, capture_lift 3.72, retract_bind 2.40 | rigid (K 0.5, L 815.84, P_cr 3039.7 N): per screw static 35.41, capture_lift 25.36, retract_bind 16.36, stall_up 8.86; two-screw static 23.61, capture_lift 16.91, retract_bind 10.90 | rigid K 1.0 (K 1.0, L 815.84, P_cr 759.9 N): per screw static 8.85, capture_lift 6.34, retract_bind 4.09, stall_up 2.21; two-screw static 5.90, capture_lift 4.23, retract_bind 2.73 | Euler, I = pi d_r^4 / 64; per-screw forces from load_cases |
| f_stall | mu 0.15: 343.18 per screw, 1029.54 total, both directions; mu 0.2: 282.21 per screw, 846.64 total, both directions | 2 pi T eta / lead, eta over jackscrew.thread_mu |
| wob_max | mu 0.15: 1287.05 N; mu 0.2: 1104.16 N against 1000 N | F_stall total + W (26.25 kg, 257.51 N) |
| lift_torque | mu 0.15: cut 0.325, capture lift 0.157 N m; mu 0.2: cut 0.395, capture lift 0.191 N m against 0.45 N m | T = F lead / (2 pi eta), per screw |
| kept_axial | 1000 N at the cut; mu 0.15: 1287.05 N at F_stall + W; mu 0.2: 1104.16 N at F_stall + W (collet with its core seat, receiver, base plate, compression; the holder is outside the cut-case route, Topologist TP1.3-10 (a)) | loads.axial_design; F_stall + W (N5) |
| backdrive | lambda 5.20 deg; mu 0.15: phi_n 8.83 deg, back-drive efficiency -0.698 (self-locking); mu 0.2: phi_n 11.70 deg, back-drive efficiency -1.253 (self-locking) | lambda = atan(lead / (pi d2)), phi_n = atan(mu / cos 15) |
| screw_share | static 85.84 / 128.76; capture_lift 119.85 / 179.77; retract_bind 185.84 / 278.76; cut 247.50 / 371.24; stall_up 343.18 | per screw (load / 3) / two-screw (load / 2), N |
| tension_segment | load 815.84; start 690.84; capture_end 40.84; park 815.84 | nut centre per pose (check_stack) - drawn anchor bearing line anchor_bearing_c:line |

## Reported items (spec reported_items; RPT)

| ID | Item | Value | Basis | Tag |
|---|---|---|---|---|
| L_min | screw length L_min per Q9 option and at the drawn anchor, against DN23 800 to 900 (885.00 / 885.84 / 1135.00 unchanged) | 0.5 m only: L_min 885.00, at anchor_z 885.84; 0.5 and 0.75 m: L_min 885.00, at anchor_z 885.84; plus 1 m: L_min 1135.00, at anchor_z 1135.84 (DN23 800 to 900); drawn bar 911.00 (screw_end_c bottom to guide_c top); with the shoulder-screw head 4.55 above the housing top: 0.5 m only: L_min 889.55, at anchor_z 890.39; 0.5 and 0.75 m: L_min 889.55, at anchor_z 890.39; plus 1 m: L_min 1139.55, at anchor_z 1140.39 | check_stack.reported q9_options, spec screw_length (S1 expressions); drawn pieces screw_end_c, guide_c, nut_screws_c, nut_housing_c (section Axes, MEASURED) | DERIVED |
| n_crit | critical speed over L_t with the end factor stated, against the rapid traverse | pinned-pinned 1336 rpm (2.67 x), fixed-pinned 2086 rpm (4.17 x) against 500 rpm at 25 mm/s | L_t 870.00, d_r 8.5, E, density; fixed-pinned is the drawn end condition (K 0.7) | DERIVED |
| pcr_margin | P_cr / F per compression case (static, capture lift, retract with bind, stall up), per mounting and K, per screw and two-screw | floating (K 0.7, L 870.00, P_cr 1363.8 N): per screw static 15.89, capture_lift 11.38, retract_bind 7.34, stall_up 3.97; two-screw static 10.59, capture_lift 7.59, retract_bind 4.89 / floating K 1.0 (K 1.0, L 870.00, P_cr 668.2 N): per screw static 7.79, capture_lift 5.58, retract_bind 3.60, stall_up 1.95; two-screw static 5.19, capture_lift 3.72, retract_bind 2.40 / rigid (K 0.5, L 815.84, P_cr 3039.7 N): per screw static 35.41, capture_lift 25.36, retract_bind 16.36, stall_up 8.86; two-screw static 23.61, capture_lift 16.91, retract_bind 10.90 / rigid K 1.0 (K 1.0, L 815.84, P_cr 759.9 N): per screw static 8.85, capture_lift 6.34, retract_bind 4.09, stall_up 2.21; two-screw static 5.90, capture_lift 4.23, retract_bind 2.73 | Euler, I = pi d_r^4 / 64; per-screw forces from load_cases | DERIVED |
| f_stall | F_stall total and per screw, both directions, mu range | mu 0.15: 343.18 per screw, 1029.54 total, both directions; mu 0.2: 282.21 per screw, 846.64 total, both directions | 2 pi T eta / lead, eta over jackscrew.thread_mu | DERIVED |
| wob_max | largest WOB at holding torque (F_stall + W) against loads.axial_design 1000 | mu 0.15: 1287.05 N; mu 0.2: 1104.16 N against 1000 N | F_stall total + W (26.25 kg, 257.51 N) | DERIVED |
| lift_torque | motor torque per screw for the cut and for capture lift, against liftmotor.holding_torque | mu 0.15: cut 0.325, capture lift 0.157 N m; mu 0.2: cut 0.395, capture lift 0.191 N m against 0.45 N m | T = F lead / (2 pi eta), per screw | DERIVED |
| kept_axial | axial force in collet (core seat), receiver, base plate at 1000 N and at F_stall + W (N5); the holder is outside the cut-case route (Topologist TP1.3-10 (a)) | 1000 N at the cut; mu 0.15: 1287.05 N at F_stall + W; mu 0.2: 1104.16 N at F_stall + W (collet with its core seat, receiver, base plate, compression; the holder is outside the cut-case route, Topologist TP1.3-10 (a)) | loads.axial_design; F_stall + W (N5) | DERIVED |
| backdrive | lead angle against friction angle, back-drive efficiency | lambda 5.20 deg; mu 0.15: phi_n 8.83 deg, back-drive efficiency -0.698 (self-locking); mu 0.2: phi_n 11.70 deg, back-drive efficiency -1.253 (self-locking) | lambda = atan(lead / (pi d2)), phi_n = atan(mu / cos 15) | DERIVED |
| screw_share | per-screw (load / 3) and two-screw (load / 2) force per case | static 85.84 / 128.76; capture_lift 119.85 / 179.77; retract_bind 185.84 / 278.76; cut 247.50 / 371.24; stall_up 343.18 | per screw (load / 3) / two-screw (load / 2), N | DERIVED |
| tension_segment | screw length in tension below the nut per S1 pose in the cut case | load 815.84; start 690.84; capture_end 40.84; park 815.84 | nut centre per pose (check_stack) - drawn anchor bearing line anchor_bearing_c:line | MEASURED |

Files: params.yaml 9469288a75c2, proposed_params.yaml b2488c014c25
