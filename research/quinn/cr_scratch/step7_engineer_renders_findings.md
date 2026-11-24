## Render set

122 PNGs, 1600 x 1200, in research\quinn\cr_scratch\step7_renders; INDEX.md has 122 rows (file, pose, size, view, rubric items). Whole assembly, four views each: R 100, Kmax 100, Kmax 90, Kmax 105 (16). Axis sections R, Kd1, Kmax. Close-ups cover rubric items 1 to 14; item 15 is the Designer's.

Numeric check: no blank PNG; coverage minimum 3.2 percent (washer iso), whole-assembly views 15.5 to 17.4 percent (core and cutter 500 mm tall).

## Harness check

witness_Kmax_100p0_closeup, rendered from the pose FCStd, reproduces step6_renders\witness_Kmax_closeup.png: pose agrees with the Step 6 fix-pass pose.

## Pose numbers (MEASURED from the pose FCStd, floor_z 40.0)

| Pose | nut zmin | reading face z | holder zmin | wing azimuth |
|---|---|---|---|---|
| R | 98.771 | 102.371 | 53.626 | 77.5 |
| Kd1 | 93.500 | 97.100 | 49.090 | not rendered |
| Kmax | 86.410 | 90.010 | 42.000 | 241.5 (second wing; first 61.5) |

Kmax values are equal at 90, 100, 105. Reading face: planar face between r 73.54 and 83.14. Holder tick z = holder zmin + 90. NT4 arrow: wing 0 in R, wing 1 at Kmax; clockwise from above.

## Harness changes

Source is the pose FCStd (opened, shapes copied, not saved). Added section scenes, cutter transparency, wing scan, reading-face measurement. Ruler close-up target moved from edge + 2 to edge - 6.

## Issues

1. Pose files hold no tray, plug, stop or feet. Those come from output\jig_assembly.FCStd (fixed, pose independent). Caddy, gauge and rest appear only in context_* (Kd1).
2. First full run missed the Kmax nut wings (5 degree scan too coarse); rerun at 1 degree added 8 PNGs.

## Jobs

| Job | PID | Log | Result |
|---|---|---|---|
| smoke | 32668 | step7_render.log | done |
| full | 2940 | step7_render_main.log | done 114 OK, 0 FAIL |
| Kmax nut rerun | 23484 | step7_render.log | done 8 OK |

FCStd mtimes unchanged; no .FCBak.

## Fix pass

All 122 PNGs re-rendered (PID 23920, step7_render.log, 122 OK, 0 FAIL, 16:05 to 16:14). PID 22652 (step7_render_run3_partial.log) stopped at 61 OK on the new cut check. INDEX.md regenerated.

R1 cause: the receiver fails every OCC boolean (BOPAlgo_InvalidCurveOnSurface); `cut` returned the uncut volume and the harness kept it. The nut also failed (section_R/Kd1/Kmax, witness, washer and cutter sections had a wrong nut half; fixed by the same change). `halfcut` now raises on unchanged volume, invalid result or material past the plane. `cut_items` catches that, clips the tessellation at the plane, caps it from the clipped mesh outline, logs FALLBACK.

| PNG set | Receiver cross-section check |
|---|---|
| 8 section PNGs incl. receiver_section | flat cap region 6.2 to 21.7 percent of frame, all PASS (threshold 0.3) |

R2: colours from params collet.colour by core.diameters index (90 red, 100 blue, 105 white); no literals. Caution: the white collet underside reads at background grey (0.4 percent coverage, outlines only).

R3: core top sections framed on the +X edge (chamfer visible); core colour now steel grey. stop_closeup adds a translucent plate as phantom upper-assembly column face.

R4: context_* cutter at 75 percent transparency.

ws4.FCStd mtime 15:50 is another job's; the harness never opens it.

Underside fix: all 4 collet_*_underside PNGs re-rendered on a dark backdrop (60/60/65), params colours unchanged. Coverage against the corner-pixel background: R 100 24.4, Kmax 90 31.4, Kmax 100 26.5, Kmax 105 (white) 23.9 percent, was 0.4 (job PID not recorded, foreground run, step7_render.log).
INDEX.md rows carry "dark background 60/60/65"; no FCStd modified.
