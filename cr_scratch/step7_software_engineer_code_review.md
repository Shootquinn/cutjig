## Defects (result-changing)

None. gates.thresholds reads every limit from params.yaml; the six probe changes alter measurement positions and controls only. No pass/fail threshold moved.

| # | Probe change | Ruling | Reason |
|---|---|---|---|
| 1 | TILT_CONTROL_DEG 1.0 to 2.0 | Accepted | 1.0 sat under the 1.021 limit; the control could not fire. |
| 2 | patch_area gap-aware (probe_poses.py:102) | Accepted | Faces held 0.005 apart have an empty common face; the 0 read was a position defect. Used only where min_dist is at most 0.01. |
| 3 | receiver_underside bbox selection (:354) | Accepted | Centre of mass counted the plate underside. Block control present; good reads 0. |
| 4 | tilt measure (:168) | Accepted | atan2 of centroid shift over axial span; the 2.0 deg control reads about 2.0. |
| 5 | CJ_PROBE_IMPORT guard, test_probe_import.py | Accepted | Prevented a 5 h sweep; three invariants plus a no-flag control. |
| 6 | solid_dist per solid pair (:134) | Accepted | Bbox gap is a lower bound; early exit returns the same minimum as distToShape. |

Checks:
- Rule M: probes read shapes from pose FCStd by Label; no placement is recomputed from params.
- SubtractiveHelix into a bore: none in new scripts.
- Build/probe sharing: probes import cadlib and common only. assemble_report.py imports tests\probes\gates and judges probe JSON cells; build geometry does not enter the gates.
- Ledger test G5 reads results\assembly_poses.json written by assemble.py, checks it against gates.screw (independent matrix code) with lead from params; zero control and three known-bad ledgers present.
- Known-bad controls present for core_axis_offset, clamped_tilt_deg, lead_in_clearance, funnel_capture_radius, receiver_underside, frame_footprint_y, slit_width, nut_stop_travel, tilt.

## Clerical

- C1: A3c and A3f read a core the assembler placed untilted on the axis; they fire only on planted states.
- C2: probe_poses.py:307 control uses 66.0 and 42.5 (nut.relief_z + 0.5); read params.
- C3: no good/bad control for fit_spigot_hole, fit_plate_key_stop_pin, frame_footprint_x.
- C4: assemble_report.py:92 and assemble_ws.py:94 `range(1, 12)`; use len(gates.WS_EXPECT).
- C5: ledger and placements share pose_numbers; G5 and the shape-based A3 measures break the circle.

## Literal scan

python cr_scratch\literal_scan.py over assemble*.py, assemble_lib.py, core.py, cutter.py, bracket.py, tnut.py, frame.py, probe_poses.py, probe_ws.py: 51 raw hits. Coincidences: 0.01 tolerances, 20.0 azimuth offsets, 1000.0 unit conversion, 24 grid, WS indices. Real: assemble_lib.py:34 CONTEXT_OFFSET 100.0 (DECLARED context offset), probe_poses.py:307 (C2). No part-dimension duplicate.

## Final counts

python -m pytest tests -q (cr_scratch\step7_se_final_run.log): 665 collected, 615 pass, 50 fail. python -m pytest tests -m green_at_7: 188 collected, 188 pass.

| Remaining failure | Count | Step |
|---|---|---|
| test_exports E1 13, E2 12, T1d 2, B1, X1 2 | 30 | green_at_10 |
| test_assembly A1b to A1e, A2a, A2b x7, A2c to A2h, A3b (column foot, carriage guide) | 19 | green_at_12 |
| test_thread_clamp T7 | 1 | green_at_8 |

All 50 carry MISSING: or ABSENT FEATURE:.
