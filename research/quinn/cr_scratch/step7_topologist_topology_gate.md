## Parts

Read by freecadcmd (research\quinn\cr_scratch\step7_topo_probe_parts.py, step7_topo_split.py, step7_topo_c6.py; each under 10 s). All parts valid, closed, volume positive.

| Part | euler_VEF | Shells | Faces per boolean | Bbox plain vs optimal | Verdict |
|---|---|---|---|---|---|
| core | 2 | 1 | 4 | equal | SIGNED |
| cutter | 8 (4 x 2) | 4 solids | 16 (4 x 4) | equal | SIGNED |
| holder | 14 | 1 | 28 to 40 | equal, zmax 110.75 | SIGNED |
| nut | 11 | 1 | 195 to 195 | z -3.6 against 0.0 (helicoid, as Step 6) | SIGNED, N1 |
| frame | 11 | 6 solids | 2478; 37 booleans; 114 objects | equal | SIGNED |

Every Euler and face prediction hit. Holder z 104.75: two down faces (4,122.0; 614.4), four ledge annuli (14.577), no coplanar pair. Frame: 2,930,129.191 mm3; 12 brackets (288 faces); 96 T-nuts; printed brackets 191,775.468.

N1: nut carries 13 coplanar-adjacent pairs; 10 are Step 6, 3 are new at z 48.5 from the refine=False relief cut. Solid valid, volume and euler hit, no reader uses these faces. Ruled, no re-view.

## Assembly checks

- Placement: 21 poses, 210 placements equal the ledger (below 1e-4), det +1, valid solids. COM of holder, nut, washer, core, cutter equals Placement times part-file COM.
- Screw motion: nut and washer equal S(phi) nut(R) in 14 poses; z0 - 8 az/360 = 60.645 throughout; phi -237.195 / -556.245 with dz -5.271 / -12.361, so clockwise lowers (T1c). base|nut distance 0.004, overlap 0, at all three azimuths: helix sense matches. R to K also moves core (-0.995, L2 lift); criterion 9 omits it.
- C6: common volume 0 across 16 purchased|member, 8 printed|member, 96 T-nut|member, 96 T-nut|purchased, 32 T-nut|printed, 4 member|member pairs. Class C, touching; equals the report.
- Report: 1071 rows, 0 FAIL. Base compound: receiver to plate common 0, distance 0.200.
- Planted states: WS1, 2, 3, 10 are Rx(180), det +1, z normal flips, reflected COM matches. WS5 2.000 deg, WS7 +3.000, WS8 -1.500, WS11 Rz -15.000, WS9 dz -13.510 with rotation 112.05 = -607.95 mod 360 (same helix). WS6 collet 113 faces.

D1 (WS4): nut COM (-0.014, 0.126, 27.947); the y-mirrored pose nut is (0.057, -0.113, 125.047). The bake lost the pose placement, so gates fire on 97.1 mm displacement (skirt gap -40.0), not handedness. Fix: bake pls["nut"] into geometry before mirror in assemble_ws.py; rebuild ws4; rerun probe_ws CJ_WS=4 detached (earlier runs 2,150 to 3,600 s; log step7_probe_ws_4.log; BUILD_DONE).

## Re-check list

Generated 2026-11-11 15:38 by research\quinn\cr_scratch\step7_recheck_gen.py (raw: step7_recheck_raw.json). Unchanged mtimes: all 62 other baseline files, including bracket_purchased, bracket_printed, tnut. Authorization file covers frame, holder, nut.

| File | mtime 2026-11-10 | Reading | Verdict |
|---|---|---|---|
| frame.FCStd, result | 12:33:43 | 11 / 2478 / C6 zero | SIGNED |
| holder.FCStd, result | 12:33:38 | 14 / 40 | SIGNED |
| nut.FCStd, result | 12:58:07 | 11 / 195 / N1 | SIGNED |
| core.FCStd, result | 12:33:37 | 2 / 4 | SIGNED |
| cutter.FCStd, result | 12:59:01 | 8 / 16 | SIGNED |
| assembly pose_* (21) | 21:01 to 21:02 | placements, S(phi) | SIGNED |
| assembly ws1 to 3, 5 to 11 | 21:01 to 21:02 | transforms | SIGNED |
| assembly ws4.FCStd | 21:02 | D1 | DEFECT |

DEFECT D1: ws4.FCStd. All other rows SIGNED.

## Addendum (fix pass, 2026-11-11)

### A. Receiver and nut boolean validity

Jobs: research\quinn\cr_scratch\step7_topo_boolctl*.py, logs alongside, BUILD_DONE.

Method (probe_poses.py): overlap is `a.common(b).Volume`, distance is `distToShape`; `engaged_mm` and fits are sections; `stop_travel` uses `common`. No validity check on any common. A zero reads as PASS in C, G, F.

Reproduced: receiver against a half-space tool at x = 0 or y = 0.3 returns the cut unchanged (955,593.23), invalid, common 0.0. Planes z = 60 and 100 work. The probes never cut by an axial plane.

Controls:
- Planar box, analytic 125: receiver, plate, nut 125.000. Sphere distance, analytic 4: 4.000 on both.
- Thread slab against slice integral: receiver 51,544.44 against 51,543.07; nut 88,522.25 against 88,521.52.
- Nut shifted against receiver thread: common 40.716, 103.091, 6,908.2 against fuse-implied 41.9, 104.1, 6,909.7.
- Shifted partners (base|holder, base|collet, nut|holder, nut|washer): common agrees with fuse and cut within 0.1.
- BOP check: receiver InvalidCurveOnSurface; plate, nut OK.

| Pair class | Method | Check | Verdict |
|---|---|---|---|
| base|nut, holder, collet, washer, core | common, distToShape | none | VALID |
| base|cutter, frame, bracket, tnut | distance 1.5 and up | none | VALID |
| nut|holder, collet, washer, core, cutter | common, distToShape | none | VALID |
| nut|frame, bracket, tnut | distance 90 and up | none | VALID |

Every C and G zero also has min_dist above 0. W1 (clerical): add `isValid()` and a shifted positive control to probe_poses.py.

### B (superseded below). ws4 at 16:41

Pending: step7_probe_ws4_fix2.log (PID 4384) has no BUILD_DONE at 16:41. Rebuilt ws4.FCStd nut CoM (0.057, -0.113, 125.047) equals the y-mirrored pose nut; 195 faces, valid. Row stays DEFECT until ws4.json is read.

### B. ws4 (closed, 2026-11-11 17:46)

ws4.json (16:48:45, run_seconds 1,916.9, start 16:16:51, input ws4.FCStd 16:16:46) is PID 4384's run. The log ends at Postprocessing with no BUILD_DONE; the JSON carries sentinel PROBE_OK. Clerical.

Fired A1 and T1 (expected A1, T1): base|nut overlap 4,081.4 mm3 (thread flanks interfere) and nut|washer pad overlap 6.304 outside [2.0, 2.45]. A3 does not fire and no skirt-gap reason appears, so the nut sits at its seat and the overlap comes from the reversed helix, not displacement. D1 closed.

Re-check list regenerated 17:46: same ten rows as before plus 21 pose files (mtimes 2026-11-10 21:01 to 21:02, unchanged by the control rerun) and 11 ws files. The rerun rewrote probe JSONs only.

| File | Verdict |
|---|---|
| frame, holder, nut, core, cutter (FCStd and result) | SIGNED |
| assembly pose_* (21) | SIGNED |
| assembly ws1 to ws11 (ws4 at 16:16) | SIGNED |

SIGNED. All rows SIGNED; latest FCStd mtime (ws4, 16:16) precedes this reading.
