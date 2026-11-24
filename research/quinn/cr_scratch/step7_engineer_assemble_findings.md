## Corrections to the brief

| # | Brief or state says | Built says | Tag |
|---|---|---|---|
| A1 | probe_poses ABSENT message for fit_plate_key_stop_pin is stale | Measure added to probe_poses.py: pocket width read from base minus base.key_width over 2 (0.250), pin gap 0.000; value 0.250 against chain 0.32 | MEASURED |
| A2 | cutter booleans run per solid | Compound common is fast (0.0 to 0.4 s) and correct; distToShape on compounds is the cost (frame\|tnut 680 s, frame\|bracket 238 s). Probe distance now runs per solid pair in bbox order (solid_dist), values equal | MEASURED |
| A3 | contact patch = common-face area (Revision 1) | Empty for faces held 0.005 apart (fit.model_contact_gap): base\|nut, base\|frame, holder\|collet, holder\|washer, collet\|core read 0. patch_area: common face, else parallel planes brought together, else sampled fraction within tol. Probe position defect, thresholds unchanged | MEASURED |
| A4 | receiver_underside_contact_mm2 good value 0 | First read 121,902: the plate underside face has its centre of mass inside r 80. Selection now requires the face bbox inside the spigot radius; reads 0 | MEASURED |
| A5 | tilt control turns the part 1.0 deg | Limit is 1.021, so the control could not fire. TILT_CONTROL_DEG 2.0 | MEASURED |
| A6 | import probe_poses is a library import | Guard also matches the module name; probe_ws ran the full pose sweep for 5.1 h with no wrong state. CJ_PROBE_IMPORT flag set before the import; tests\test_probe_import.py (3 invariants, with a no-flag control) | MEASURED |
| A7 | Kd1 phi -237.241 | Holder bottom from params (9.090, Loftsman table 9.0890) gives dz -5.271, phi -237.195; Kmax -12.361 / -556.245 unchanged. Screw invariant z0 - 8 az/360 = 60.645 holds in all poses | DERIVED |
| A8 | WS9 stop travel | DZ_WS9 -13.510 declared in assemble_ws.py (10.01 stop travel + 3.5) | DECLARED |
| A9 | probe_ws runs all states | CJ_WS=<list> limits states, CJ_WS=none runs ws0 only (parallel runs) | DECLARED |

Probe JSON from an earlier sweep was overwritten by a rerun with the same code; no copy exists to diff. The final pose JSONs come from the corrected probes.

## Pose generation record

L = 8 (thread.pitch). Base pose R for every size; nut(P) = S(phi) nut(R), washer likewise, holder by T(0,0,dz) to its seat, base, frame (T(0,0,-0.005)), bracket, tnut, cutter fixed.

| Pose | holder bottom (floor frame) | nut z0 | dz | phi deg | nut azimuth |
|---|---|---|---|---|---|
| R | 13.626 | 62.371 | 0 | 0 | 77.670 |
| Kd1 | 9.090 | 57.100 | -5.271 | -237.195 | -159.525 |
| Kmax | 2.000 | 50.010 | -12.361 | -556.245 | -478.575 |

Nominal size 100.0. Core d: d, d+1.0, d-1.5. Ledger results\assembly_poses.json (gates.ledger_errors empty); audit results\assembly_audit_<tag>.json (max placement diff 0.0). Output jig_assembly.FCStd and .step: 20 objects, 8.2 MB STEP.

## Pair-matrix summary

7 sizes x 3 poses x 51 rows = 1071 rows, 1071 pass, 0 FAIL (tool report, cell values equal probe JSON). Per pose classes: R C7 P1 G12 F25 pairs; K C9 P1 G10 F25. nut\|washer overlap 2.387 mm3 in every pose. Nominal measures: floor_z 40.0, engaged 25.705 / 31.400 / 38.490, core axis offset 0.000, tilt 0.000, lead-in clearance 5.5 (Kd1), frame 644 x 608, receiver underside contact 0.0, fit_spigot_hole 0.200, fit_plate_key_stop_pin 0.250.

## Clamp range

| d | pose | engaged | slit min | stop travel | flange gap |
|---|---|---|---|---|---|
| 90 / 105 | R | 25.705 | 1.500 | 22.375 | 13.126 |
| 90 / 105 | Kd1 | 31.400 | 1.238 | 17.102 | 8.590 |
| 90 / 105 | Kmax | 38.490 | 0.584 | 10.016 | 1.500 |

T4 and T5 pass at 90 and 105.

## Wrong states

| WS | Fired | WS | Fired |
|---|---|---|---|
| 1 | A1 F1 F3 | 7 | A1 F1 F3 |
| 2 | A1 A3 F1 | 8 | A1 A3 F1 |
| 3 | A1 T1 | 9 | A1 T1 |
| 4 | A1 A3 T1 | 10 | A1 A3 T1 |
| 5 | A1 T1 T9 | 11 | A1 |
| 6 | A1 F3 | ws0 (R, Kd1, Kmax) | none |

All inside the six gates. Planted states fire a superset of the Loftsman list in WS1, 2, 4, 7, 8, 10; WS9 fires A1 T1 (expected set A3 or A1 met); WS11 fires A1 only.

## Builds

| Job | PID | Log (cr_scratch) | BUILD_DONE / PROBE_DONE | run_seconds |
|---|---|---|---|---|
| ledger | 34880 | step7_asm_ledger.log | yes | 0.7 |
| poses x7 | 29980, 31084, 20012, 27920, 23924, 30648, 4684 | step7_asm_poses_<tag>.log | yes | 5 to 8 each |
| output | 16740 | step7_asm_output.log | yes | 5 |
| ws build | 34284 | step7_asm_ws.log | yes | 16.3 |
| probe_poses x7 (final) | 25604, 25144, 26076, 3304, 3908, 8552, 4136 | step7_probe_poses_<tag>_b.log | yes | 7,700 to 8,075 |
| probe_ws, 9 processes | 30180, 14248, 31932, 35776, 31812, 32764, 36728, 20092, 32896 | step7_probe_ws_<n>.log | yes (ws1, ws10 from step7_probe_ws3.log) | 2,150 to 3,600 |
| probe_ws ws0 | 8396 | step7_probe_ws_none.log | yes | 5,157 |

Probe time cost: 7,700 s per size under 16-process contention.

## Test counts and green_at_7 status

green_at_7: 188 collected, 188 pass. Full suite: 665 collected, 615 pass, 50 fail (test_assembly 19, test_exports 30, test_thread_clamp 1); test_step6_parts 51 of 51 pass; test_step7_assembly all pass. Remaining failures are test_exports (green_at_10), test_assembly green_at_12 (A1b to A1e, A2a to A2h), T7 (green_at_8).

## Design issues with disposition

1. Probe edits (probe_poses.py, probe_ws.py), measurement positions only, thresholds untouched: A1 to A6, A9. Software Engineer review.
2. Distance cost: bbox-ordered per-solid evaluation; a rerun of all poses takes about 2 h at 16 processes.
3. Holder Kd1 at 9.090 against Loftsman 9.0890: A3e tolerance 0.05, holder\|collet overlap 0.000, class C holds.
4. Context placements (caddy, gauge, rest, feet) in jig_assembly are DECLARED (100 mm off the frame; rest roller plane at floor + rest.height_positions[0]); Designer reads placement only.
5. PZRT T-nut CAD absent: proxy stands. No relation row changed; step7_class_rulings.md not written by the Engineer.
6. Rebuilds: none after 2a. .FCBak: two moved to research\quinn\cr_scratch\fcbak_archive.

## Fix pass

### Corrections to the brief

| # | Brief says | Built says | Tag |
|---|---|---|---|
| F1 | D1 fix: bake the nut placement into the geometry before the mirror | First rebuild (PID 33504, step7_asm_ws4_fix.log) baked correctly and passed the CoM guard, but `o.Placement = identity` on the Part::Feature dropped the location the mirrored shape carries; probe (step7_probe_ws4_fix.log, 1,452 s) still read nut skirt -40.0 and 232,814 mm3. Second rebuild (PID 17180, step7_asm_ws4_fix2.log) keeps the carried placement as the object placement; nut CoM (0.057, -0.113, 125.047) | MEASURED |
| F2 | ws4 placement identity (Topologist E6) | ws4 nut object placement equals the pose placement; geometry is the mirrored nut | DECLARED |
| F3 | probe_ws log ends BUILD_DONE | Probe logs end PROBE_DONE (probe_lib.finish); step7_probe_ws4_fix2.log has no BUILD_DONE line, PROBE_DONE ws4 1916.9s is the sentinel | MEASURED |
| F4 | frame_footprint_x control by removing the solid of lowest XMin | Both rails span x, so one removal left 644.0 and the control could not fire. Control now removes both full-length rails | MEASURED |

### WS4 result

ws4.json: fired A1, T1 (expected A1, T1). Reasons: base\|nut 4,081.4 mm3 (Loftsman 4,079.7), nut\|washer overlap 6.304 outside [2.0, 2.45]. No A3 skirt reason. Mirror guard (results\assembly_ws4_guard.json): good 1.2e-13 mm, displaced old build 97.100 mm, tolerance 0.5.

### Changes

| Item | Change | Tag |
|---|---|---|
| Mirror guard | assemble_ws.py raises if the mirrored CoM is over 0.5 mm from the pose CoM (x, -y, z); tests D1 in test_step7_fix_controls.py | MEASURED |
| Literals | probe_poses.py nut-fill control reads nut.relief_z, nut.relief_r, receiver.register_bore_radius, nut.length, washer.thickness, nut.washer_pocket_depth | DERIVED |
| WS registry | assemble_report.py and assemble_ws.py iterate gates.WS_EXPECT | DERIVED |
| Controls | fit_spigot_hole (plate hole 0.6 too large), fit_plate_key_stop_pin (key pocket 1.0 too wide), frame_footprint_x; 4 tests | MEASURED |
| Common-validity guard | checked_common in probe_poses.py: invalid common raises InvalidCommon (never 0.0); used for pair overlaps, stop travel, patch area, instance pairs. probe_ws uses analyse | DECLARED |
| Guard control | probe_common_guard.py: shifted boxes 600 mm3 (read 599.9999999999999), shifted tubes 18,849.556 (read the same), stub invalid result raises; 2 tests | MEASURED |
| D15 | ASSEMBLY.md base row: -y row is the +y row shifted 15 mm in x (whole-row offset); the pattern maps onto itself under a 180 deg turn about Z, caught by the stop-pin pocket at +x and the plate-key pockets on the +y slot line | MEASURED |

### Builds

| Job | PID | Log (cr_scratch) | Sentinel | run_seconds |
|---|---|---|---|---|
| ws4 build 1 / 2 | 33504 / 17180 | step7_asm_ws4_fix.log / _fix2.log | BUILD_DONE | 2.7 / 7.0 |
| ws4 probe 1 / 2 | 34652 / 4384 | step7_probe_ws4_fix.log / _fix2.log | PROBE_DONE | 1,452 / 1,917 |
| pose probes x7 (controls) | 23496, 17084, 19748, 20536, 16848, 15228, 27844 | step7_probe_poses_<tag>_c.log | PROBE_DONE | about 2,250 per pose |
| guard control | 13568 | step7_probe_guard_control.log | BUILD_DONE | 0.0 |
| R 100p0 re-probe (F4 control) | 23596 | step7_probe_poses_100p0_R_d.log | PROBE_DONE | 1,129.4 (frame_instances 1,426.8) |

F4 result (MEASURED): pose_R_100p0.json frame_footprint_x 644.0; control good 644.0, bad 524.0 (both rails removed); fires against icd.footprint_x 644 (tol 0.05).

### Final test counts

pytest tests: 672 collected, 622 pass, 50 fail (output research\quinn\cr_scratch\step7_pytest_fixpass.txt).

| File | Fail | Marker |
|---|---|---|
| test_exports.py | 30 | green_at_10 |
| test_assembly.py | 19 | green_at_12 (A1b to A1e, A2a to A2h, A2b x7, A3b column foot and carriage guide) |
| test_thread_clamp.py | 1 | green_at_8 (T7) |

green_at_7: 194 selected, 194 pass. test_step7_fix_controls.py and test_probe_import.py pass.
