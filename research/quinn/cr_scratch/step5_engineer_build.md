## Corrections to the brief

- Leaf count is 324 before and 328 after the four new keys, not 327 to 331. MEASURED (common.iter_leaves).
- The 76 green_at_5 target is 98 (Software Engineer revision). MEASURED (pytest -m green_at_5: 98 passed).
- `parts_cache` nut and receiver mtimes (22:42:29, 22:45:48) differ from `step4_fcstd_mtimes_after.txt` (20:27, 20:24). They were rebuilt in the Step 4 fix pass after that file was written. Unchanged by Step 5: equal to the pre-build listing in `step5_fcstd_mtimes_before.txt`. MEASURED.
- `report_assumptions.md` regeneration (bom_tools main) also refreshed three fit.* source strings that had drifted from params. DECLARED clerical.

## Pass table

| Run | Result |
|---|---|
| green_at_5 | 98 of 98 pass |
| green_at_4 | 259 of 259 pass |
| Full pytest | 540 collected, 364 passed, 176 failed, 0 errors, skips, xfails |
| Failure types | 176 of 176 are MISSING: or ABSENT FEATURE: (test_assembly 134, test_exports 31, test_thread_clamp 11: T4, T5, T7) |
| test_params_bom.py | 213 passed |

## Collets

| d | volume mm3 | valid | solids | euler_VEF | seconds | notches | c |
|---|---|---|---|---|---|---|---|
| 90.0 | 139 234 | True | 1 | 0 | 30.4 | 1 | 10.50 |
| 92.5 | 129 681 | True | 1 | 0 | 34.5 | 2 | 10.05 |
| 95.0 | 121 994 | True | 1 | 0 | 33.7 | 3 | 8.80 |
| 97.5 | 113 685 | True | 1 | 0 | 32.3 | 4 | 7.55 |
| 100.0 | 104 734 | True | 1 | 0 | 36.5 | 5 | 6.30 |
| 102.5 | 95 117 | True | 1 | 0 | 35.8 | 6 | 5.05 |
| 105.0 | 84 802 | True | 1 | 0 | 35.4 | 7 | 3.80 |
| 97.0 (doc) | 115 386 | True | 1 | 0 | 23.7 | 4 | 7.80 |
| 93.7 (doc) | 126 094 | True | 1 | 0 | 24.6 | 2 | 9.45 |

Each collet result carries `checks_all_pass: true` (C1, C2, C3, C5, C6, C7, C9b, clamped solids valid). Clamped slit widths 1.2382 (Kd1) and 0.5837 (Kmax). Probe at d 90: C6 wall 2.059 (the Loftsman's 1.259 applies to d 92.5 to 105), slit_plane_faces 0, bad_edges 0, R gap 0.29998, Kd1 and Kmax common volume 0.0, contact 11 855 mm2. Family probe: zero control 0.0, known-bad 1.877 mm3, largest pair symdiff in the region 0.0.

The doc steps for 97.0 and 93.7 ran as written; no correction to the doc. The 110.0 refusal logged `REFUSED ... exceeds envelope cap 106.585` with BUILD_DONE in 0.2 s and no file.

Jobs (detached, `research\quinn\cr_scratch\step5_build_<tag>.log`, sentinel BUILD_DONE): 090p0 PID 12756; 092p5 35836; 095p0 30356; 097p5 34192; 100p0 22904; 102p5 27680; 105p0 12844; 097p0 and 093p7 via the usage doc (`research\quinn\cr_scratch\collet_097p0.log`, `collet_093p7.log`); probe_collet PID 2100 (231.4 s, log `step5_probe_collet.log`).

## New params keys (source and status set)

| Key | Value | Status |
|---|---|---|
| collet.notch_azimuth_offsets_deg | [60, 90, 120, 180, 210, 240, 300] | ASSUMED |
| collet.label_azimuth_offset_deg | -30 | ASSUMED |
| collet.label_window_width | 24 | ASSUMED |
| collet.tool_overshoot | 1.0 | ASSUMED |

`PARAM_GAPS` in `tests\cad_helpers.py` emptied. `report_assumptions.md` regenerated (counts line 328). The clamped half-up notch-count formula is in the `source` of `collet.rim_notch_count`; its `value` text stays `round((d - core.diameters[0]) / collets.spacing) + 1` because `test_params_bom.py` lines 595 and 780 pin that text (P14, P20). Finding for the Manager: if the value text itself should change, those two assertions change with it (Software Engineer owns).

## Deviations from the definition

- Tool radial span is r_b - ledge width - collet.tool_overshoot to r_fo + collet.tool_overshoot per size (42.0 to 67.99 at d 90) instead of the literal 38 to 72; the tools sit in the void at both ends and the keys stay clear. DERIVED, removes a literal.
- Label tool box spans z 11 to 21 so its faces are not coplanar with the band faces (z 12, 20). The band fixes the recess height.
- Bore lip volume is a Pappus term at radius r_b + 0.05; feature volume only.
- Clamped solids reuse the free c and z_e (Topologist non-blocking note); the label band follows the shifted cone.
- No Step 3 part fault found. No Step 3 file touched. No .FCBak created.

## Cleanup pass

New keys (source and status set): `collet.chamfer_cap` 10.5 (DERIVED), `collet.chamfer_band_lo` 2.5 (DERIVED), `collet.chamfer_band_hi` 3.5 (DERIVED), `collet.chamfer_angle_deg` 45 (ASSUMED; drives the chamfer and the lip arc angles). Leaf count 332 (was 328). `report_assumptions.md` regenerated (counts line 332). `collet.rim_notch_count` value already carries the clamped text in params.yaml and test_params_bom.py (lines 595, 780). Line endings: params.yaml and test_params_bom.py are both LF (0 CRLF); cadlib.py normalized to CRLF (it held 18 LF lines after my insert); the other files keep their existing endings.

Code: `slit_hole_tools(kind, ctx)` replaces the two loops; `cadlib.footring_derived` replaces the importlib workaround, and `footring.derived` delegates to it (footring.py build unchanged, FCStd not rebuilt).

Faces per cut (faces_before to faces_after), d 90 to 97.5 and 93.7, 97.0: slits 13 to 103, relief 103 to 103, notches 103 to 107 / 111 / 115 / 119 (1 to 4 notches: +4 each), label +6. d 100.0 to 105.0: slits 13 to 92, relief 92 to 103, notches +20 / +24 / +28 (5 to 7), label +6. Final faces: 113, 117, 121, 125, 129, 133, 137 (97.0 125, 93.7 117). The relief cut adds no faces for d up to 97.5 and 11 for d 100 and above; both groups reach 103 after the holes.

Bbox, plain against optimal: identical for all nine (x 66.99, z 32.0; keys in `bbox_plain` and `bbox_optimal`).

Volumes before and after the rebuild: free, Kd1 and Kmax of all nine collets differ by 0.000 percent (`research\quinn\cr_scratch\step5_volumes_before_cleanup.json`).

Pytest: 540 collected, 364 passed, 176 failed (all MISSING: or ABSENT FEATURE:), green_at_5 98 of 98. Probe re-run PROBE_DONE collet_family 231.6 s. Step 3 FCStd mtimes unchanged; no .FCBak files.
