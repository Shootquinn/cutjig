## Corrections to the brief

| # | Brief or definition says | Built says | Tag |
|---|---|---|---|
| P1 | Nut relief adds no boolean, faces net 0 (Topologist) | First build through the PartDesign Boolean refine pass: 177 faces, BOP check SelfIntersect plus 10 InvalidCurveOnSurface, and every boolean on the nut (common with a box, common with the receiver) returned 0. Refine switched off for that one cut (cadlib.body_boolean refine=False): 195 faces, edges 477, vertices 293, euler 11, BOP clean, 352,473.766 mm3. Known-bad thread controls read 10,130.6 and 6,269.0 mm3 again | MEASURED |
| P2 | C6 overlaps: 18,249 x 4, 1,061 x 4, 16,523 | Also 8 T-nut against purchased-bracket pairs, 716.0 mm3 total (max 89.5), absent from the brief. All zero after the cut | MEASURED |
| P3 | Holder top 104.75 keeps meaning | Result JSON row now reads the collar underside (tube top) by axial interval; bbox zmax 110.75 | MEASURED |
| P4 | Receiver engaged at R 25.705 | Re-measured on the relief nut at nut azimuths 77.670, -159.571, -478.575: 25.705 / 31.401 / 38.490 | MEASURED |
| P5 | Cutter compound valid | Each solid BOP clean; the compound check reports SelfIntersect on the coincident faces between touching solids | MEASURED |
| P6 | PARAM_GAPS keys absent | Added to params.yaml (19 keys, 444 to 463 leaves); nut.pad_overlap_max added with the min | DECLARED |

## C6 result table

| Pair class | Before mm3 | After mm3 |
|---|---|---|
| Purchased inboard vs printed outer, 4 sites | 18,248.6 each | 0 |
| Printed bracket vs end member, 4 sites | 1,061.4 each | 0 |
| T-nut pairs at the C6 sites, 16 pairs | 16,523.9 total | 0 |
| T-nut vs purchased bracket, 8 pairs (new) | 716.0 total | 0 |
| T-nut vs host profile, all T-nuts | 128 touching, 0 common | 96 touching, 0 common |
| Bracket vs member, all brackets | 4 over tolerance | 12 brackets, 24 of 24 near pairs touching, 0 common |

Counts after: 6 members, 12 brackets (8 purchased, 4 printed), 96 T-nuts. Source: cr_scratch\step7_c6_verify.json and step7_c6_verify_before.json (freecadcmd, pairs filtered by 0.02 mm bbox, common volume, distToShape at or under 0.01).

## Rebuild list

| File | Reason | Volume mm3 before / after | Faces before / after | Euler before / after |
|---|---|---|---|---|
| frame.FCStd | C6 option (a): four printed outer brackets, 32 T-nuts dropped | members 2,930,129.191 unchanged; printed brackets 383,550.9 to 191,775.5; T-nuts 177,119.8 to 132,839.8 | members 2478 / 2478; objects 150 / 114; booleans 49 / 37 | 11 / 11 |
| holder.FCStd | Collar ring r 55.0 to 76.2, z 104.75 to 110.75, four 6.6 holes | 407,841.181 / 459,449.003 | 28 / 40 | 8 / 14, 1 shell |
| nut.FCStd | Relief bore r 75.34, z 42.0 to 48.5 | 358,837.755 / 352,473.766 | 195 / 195 | 10 / 11, 1 shell |
| core.FCStd (new) | Stand-in d 100, L 500, chamfer 3.0 top | 3,925,605.375 | 4 | 2 |
| cutter.FCStd (new) | Four solids: annulus, tube, funnel, ring | 951,102.125 | 16 (4 each) | 8 (2 each) |

All predictions hit: holder 40 / 14 / 1 / 459,449.0; nut 195 / 11 / 1 / 352,473.8; frame 11 / 2478 / 2,930,129.191 / 114 objects / 37 booleans / printed 191,775.468; core 4 / 2; cutter 16. Bboxes plain equal optimal on all five (holder zmax 110.75). Mtime check against the 72-file baseline: modified frame, holder, nut (and their result JSON); new core, cutter; bracket_purchased, bracket_printed, tnut untouched. Four .FCBak moved to cr_scratch\fcbak_archive.

## Builds

| Job | PID | Log (cr_scratch) | BUILD_DONE | run_seconds |
|---|---|---|---|---|
| core | 33232 | step7_build_core.log | 12:33 | 0.4 |
| cutter | 29064; rebuilt foreground | step7_build_cutter.log | 12:33 | 0.4 |
| holder | 34788 | step7_build_holder.log | 12:33 | 0.8 |
| frame | 19688 | step7_build_frame.log | 12:33 | 10.1 |
| nut, first (defective, superseded) | 30320 | step7_build_nut.log | 12:35 | 98.5 |
| nut, final | 36476 | step7_build_nut2.log | 12:58 | 95.0 |
| C6 verify after / before | 36744 / 27424 | step7_c6_verify_after.log, _before.log | 12:37 / 12:42 | 153.6 / 173.9 |
| probes step3_parts, step6_parts, thread, witness_sight, tilt, thread_mesh, step6_marks | 25652, 17924, 32284, 32196, 22748, 8516, 26900 | step7_probe_<name>.log | 12:58 to 13:03; step6_marks pending | 6.7 to 252; step6_marks about 3350 |

Params pass: 19 keys with source and status (pose x6, cutter x2, collar x2, nut x4, core, hardware.printed_brackets_per_joint, base.key_width, pin_dia, pin_x); bom_tools regenerates bom_purchased.md (T-nuts 150 to 115, bracket screws 141 to 106) and report_assumptions.md (DECLARED 32, ASSUMED 296, VERIFIED 38, DERIVED 97, total 463). ASSEMBLY.md rows edited as in Revision 1: base|holder 0.12, holder|collet 0.29, holder|nut 0.50, nut|washer P with legend, collar top|cutter "at least 0 / 25 / 25", pair counts R C7 P1 G12 F25, K C9 P1 G10 F25. T9 criterion 2.379 mm against P/2 4.000 (register 0.5963 plus rock 0.3149 deg). Literal scan of new lines: probe azimuths and tolerances only, no part dimension.

## Test counts

pytest tests, run 4 (before the step6_marks probe finishes): 662 collected, 418 pass, 244 fail. By file: test_assembly 136, test_exports 31, test_step7_assembly 60, test_thread_clamp 11, test_step6_parts 6 (stale step6_marks.json only). Every other failure carries MISSING or ABSENT FEATURE. Final count: see Design issues item 1.

## Design issues

1. step6_marks probe (about 56 min) runs as PID 26900 since 12:58:51; six step6_parts tests (NT4, NT5, RC6, HD7 x2, one control) pass or fail only after it ends. Closed by the Manager run.
2. Revised tests with reasons (Step 7 rulings, not weakened): test_assembly class counts and cad_helpers legal classes admit P; gates.ROW_RE admits P; HD5 and HD6 probe windows end at the flange top (the collar sat inside the old window); HD6 allowed faces add the collar underside at holder top minus collar.thickness. Software Engineer review.
3. Cutter: assembler booleans and distances run per solid (comp.Solids). Input to 2b.
4. probe_poses ABSENT message for fit_plate_key_stop_pin still reads "params gap"; the three base keys now exist. Input to 2b.
5. Printed-bracket joint capacity with one bracket: DECLARED, Step 12.
6. 80/20 files on disk: 30-6060 STEP, 14089 STEP (and qmod v0), printed STL, 3mf and XL 3mf. Missing: PZRT 3030 T-nut CAD (proxy). Stock consumption unchanged: 644 x2, 488 x2, 468 x2; 1540, 980, 952, 728 untouched.
