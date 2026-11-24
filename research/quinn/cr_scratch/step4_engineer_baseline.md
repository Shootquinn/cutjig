## Module by state (B4, run 2026-11-08, 510 tests, 29 s)

| Module | pass | MISSING | ABSENT FEATURE | fail other | error | skip | xfail |
|---|---|---|---|---|---|---|---|
| test_params_bom | 212 | 0 | 0 | 0 | 0 | 0 | 0 |
| test_collet_family | 8 | 61 | 0 | 0 | 0 | 0 | 0 |
| test_thread_clamp | 11 | 17 | 1 | 2 | 0 | 0 | 0 |
| test_assembly | 10 | 141 | 0 | 0 | 0 | 0 | 0 |
| test_exports | 9 | 38 | 0 | 0 | 0 | 0 | 0 |
| Total | 250 | 257 | 1 | 2 | 0 | 0 | 0 |

## By label and green_at

| Label, green_at | n | pass | MISSING | ABSENT | fail other |
|---|---|---|---|---|---|
| invariant, 4 | 252 | 250 | 0 | 0 | 2 |
| discriminator, 5 | 75 | 0 | 75 | 0 | 0 |
| discriminator, 7 | 126 | 0 | 126 | 0 | 0 |
| discriminator, 8 | 1 | 0 | 0 | 1 | 0 |
| discriminator, 10 | 38 | 0 | 38 | 0 | 0 |
| discriminator, 12 | 18 | 0 | 18 | 0 | 0 |

Every discriminator fails with MISSING: or ABSENT FEATURE: (T7 is the one ABSENT FEATURE). No discriminator passes. Zero errors, skips, xfails. Collection clean. Junit: results\step4_baseline.xml.

## Defects (fail other)

1. test_thread_clamp.py::test_T9_register_stops_the_tilt_before_any_thread_interferes (invariant, green_at_4): `assert 70.927 <= 0.01` (H.OVERLAP_TOL). Source: results\probes\tilt.json thread_common_mm3 at tilt 0.924 deg.
2. test_thread_clamp.py::test_T9_control_double_critical_tilt_interferes (invariant, green_at_4): same message, same value 70.927 <= 0.01. The control fails on the register-tilt value; tilt.json holds common_at_2x_mm3 = 18.95, so the control does not reach the 2x key as its name states.

Cause candidates (assertions untouched, for the Software Engineer):
- tilt.json nut_samples are non-monotonic: 0.3 -> 1.63, 0.5 -> 10.20, 0.7 -> 30.98, 0.924 -> 70.93, 1.2 -> 0.0006, 1.6 -> 0.19, 2.0 -> 1.16, 2.5 -> 42872 mm3. A common volume that drops to 0.0006 at 1.2 deg and reaches 42872 at 2.5 deg is a boolean failure signature. The probe log carries `TopoShapeExpansion.cpp(922): hasher mismatch` before four of the booleans. The probe measurement is suspect.
- If the booleans are valid, the register tilt 0.924 deg interferes by 70.9 mm3 and register.t9_tilt_deg is wrong (probe first thread interference at 0.3 deg, register first at 0.5 deg).
- Control wiring: the control reads the register-tilt key.

## Mismatches against the Software Engineer prediction (per test)

| Test | Predicted | Observed | Reason |
|---|---|---|---|
| T9 register stops the tilt | pass after thread_mesh and tilt probes | fail other | defect 1 |
| T9 control double critical tilt | pass after both probes | fail other | defect 2 |

Count: 2. All other 508 states match the marker (invariant pass, discriminator MISSING/ABSENT). Aggregate prediction (248 pass today, 262 fail, 259 MISSING) does not reconcile with 252 invariants and 258 discriminators; observed 250 pass, 260 fail (257 MISSING, 1 ABSENT, 2 other). T1b and T1c pass on the fresh thread_mesh.json.

## Probe runs (freecadcmd, own outputs)

| Probe | Mode | PID | Start | Run time | Log | Sentinel |
|---|---|---|---|---|---|---|
| probe_thread_mesh | detached | 8724 | 22:06:29 | 7 s | research\quinn\cr_scratch\step4_probe_thread_mesh.log | BUILD_DONE |
| probe_tilt | detached | 34764 | 22:06:29 | 8 s | research\quinn\cr_scratch\step4_probe_tilt.log | BUILD_DONE |
| probe_step3_parts | foreground | - | - | 3 s | - | JSON mtime 22:06:52 |
| probe_thread | foreground | - | - | 24 s | - | JSON mtime 22:07:17 |

Both heavy probes finished in under 10 s (author estimate: many booleans). Four JSONs in results\probes\ are from this session. No harness repair was needed; no file edited.

## Tests run

test_params_bom alone: 212 passed (197 + 15 new) in 17 s. Full suite: 510 collected, 250 passed, 260 failed.

## Controls

32 test functions carry "control" in the name. 30 pass at B4. The other two: test_X1_negative_controls_fire (discriminator, MISSING, expected) and the T9 control (defect 2). Zero-control and known-bad-control pairs for A1 parser, P22, P23, C8, C9a, C3, T1a, T8, F5, E1, E2, T1d, B1 pass.

Planted-defect spot checks (temporary copy under the scratchpad, plant\):
- params.yaml core.min_exposed 143.12 -> 140.00: test_F4_exposed_core_arithmetic_and_assumed_standoff fails.
- ASSEMBLY.md one pair row deleted (nut/washer): test_A1_parser_reads_45_pairs_and_the_class_counts fails (the deleted-row control also fails, as it reads the live file).
- "ISO 13854 finger pinch" appended to bom_purchased.md: test_P22_live_files_have_no_banned_language fails (the P22 planted-string control also fails, same reason).
The clean copy lacked cr_scratch, so test_P10 failed there; that is a copy artifact, not a B4 result.

## parts_cache FCStd LastWriteTime

Before and after: equal (diff empty). Lists in research\quinn\cr_scratch\step4_fcstd_mtimes_before.txt and step4_fcstd_mtimes_after.txt. Six .FCBak files in parts_cache predate this session (16:05 to 20:25).
