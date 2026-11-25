# Step 1.1 (e) Loftsman geometry cross-review, S1 r1

## Corrections to the brief

1. The Engineer's open item 1 (holder flange against the receiver rim) has an arithmetic answer. `holder.length` 88 excludes the flange (test_P18: holder_bottom - drop + holder.length + flange 8 + nut plate 8 + collar.top_above_plate). The holder z_rule is short by `holder.flange_thickness`. This is FIX LF1.1-1.
2. `s1_checks_r1.json` carries K7 states without pair names. The depth-separated pair list in section 3 comes from a scratch re-run of `sc.k7` on the r1 figures, with `assess_pair` wrapped to log names (MEASURED, 1037 depth-separated tests, 246 distinct pairs; K7 result unchanged, pass).

Tags: HAND = pencil arithmetic from params and overlay values (DERIVED). JSON = `s1_checks_r1.json`, `s1_summary_r1.md` or `s1_mass_report_r1.json` (MEASURED). Inputs are DECLARED or ASSUMED as `keys_read` lists them. Frame: z_S = z_A + 60 (`jig.datum_a_above_floor`); receiver floor z_A = 0 + 40 = 40.

## 1. Hand value beside JSON value

### Stack terms

| Term | HAND | JSON / code |
|---|---|---|
| drop | 13.126 - 8.59 = 4.536 | |
| nut plate | 7.5 + 1.3 - 0.8 = 8.00 | |
| collar top | 40 + 13.626 - 4.536 + 88 + 8 + 8 + 6.75 = 159.84 z_A (219.84 z_S) | 159.84 recomputed = params 159.84 |
| core stop | overlay 42.5 = 40 + 2.5 (core_seat z_max) | 42.5 (LF-16 agrees) |
| stop_k, 0.5 / 0.75 m | max(184.84, 42.5 + 500 + 25 - 800 = -232.5) = 184.84; max(184.84, 17.5) = 184.84 | 184.84 / 184.84 |
| start_k | 184.84 + 650 = 834.84 | 834.84 |
| park | max(834.84, 159.84 + 750 = 909.84) + 50 = 959.84 z_A | 959.84 |

### K6 tip z per pose and park tip

| Pose | tip_z rule | HAND z_A | HAND z_S | JSON / stack z_S |
|---|---|---|---|---|
| load | park_tip | 959.84 | 1019.84 | 1019.84 |
| start | stop.start_z[0] | 834.84 | 894.84 | 894.84 |
| capture_end | stop.height_z = 159.84 + 25 | 184.84 | 244.84 | 244.84 |
| park | park_tip | 959.84 | 1019.84 | 1019.84 |

Spot z_rules (HAND, z_S), all equal to the drawn extents K6 passes:
- Top-end block top = tip + 800 + 150: load and park 1969.84, start 1844.84, capture_end 1194.84.
- Ring = tip + 130 to + 142: load 1149.84 to 1161.84, capture_end 374.84 to 386.84 (JSON 374.84 to 386.84).
- Gear = ring top + 52 + 28.23 to + 62: capture_end 467.07 to 500.84.
- Bearing clears the head by tip + 117 - (tip + 106.369) = 10.631. Gear top under the tube top by 800 - 256 = 544.00.

### Lift stroke

959.84 - 184.84 = 775.00 (JSON 775.00). Plus 1 m: stop_k = 42.5 + 1000 + 25 - 800 = 267.5, start 917.5, park max(917.5, 159.84 + 1000) + 50 = 1209.84, stroke 1209.84 - 184.84 = 1025.00 (JSON 1209.84, 1025.00).

### S1 checks

| Check | HAND | JSON |
|---|---|---|
| S1-1 | 894.84 - 244.84 = 650.00, in [534.93, 650] | 650.0 |
| S1-2 | 1019.84 - 894.84 = 125.00 (park and load) | 125.0 |
| S1-3 | 959.84 - 50 - (42.5 + 500) = 367.34; 959.84 - 50 - (42.5 + 750) = 117.34 | 367.34, 117.34 |
| S1-5a | (184.84 + 800) - (42.5 + 750) = 984.84 - 792.50 = 192.34 | 192.34 |
| S1-5b | bearing bottom 184.84 + 142 - 25 = 301.84 minus collar top 159.84 = 142.00 | 142.0 |
| S1-7 | 792.50 - 184.84 = 607.66; spare 607.66 - 534.93 = 72.73 | 607.66, 72.73 |

S1-4 band (anchor top 295 + 10 + 15 = 320 z_A = 380 z_S; guide bottom 1135 - 10 - 15 = 1110 z_A = 1170 z_S), nut z = tip + 136:

| Pose | Nut z_S (HAND) | Low margin | High margin |
|---|---|---|---|
| load | 1155.84 | 775.84 | 14.16 |
| start | 1030.84 | 650.84 | 139.16 |
| capture_end | 380.84 | **0.84** | 789.16 |
| park | 1155.84 | 775.84 | 14.16 |

JSON least margin 0.84.

S1-6, both drawn screws, every pose (r 160):

| Screw | theta | x = r cos theta (HAND) | Drawn centroid x | Depth centre r sin theta (HAND) | Stack band |
|---|---|---|---|---|---|
| screw_a | 150 | -138.564 | -138.564 | 80.000 | [76.00, 84.00] |
| screw_b | 30 | +138.564 | +138.564 | 80.000 | [76.00, 84.00] |

The third screw (270) is at x 0, depth -160, undrawn by spec. "8 screw projections" = 2 screws x 4 poses.

## 2. Reported values (arithmetic only)

| Value | HAND | JSON |
|---|---|---|
| Highest point, load / park | 959.84 + 950 + 60 = 1969.84, margin 30.16 | 1969.84, 30.16 |
| Highest point, start | 834.84 + 950 + 60 = 1844.84, margin 155.16 | 1844.84, 155.16 |
| Highest point, capture_end | frame member 12 + 1213 + 60 = 1285.00 (top block 1194.84 below it), margin 715.00 | 1285.00, 715.00 |
| L_min, stand-in options | 775 + 30 + 30 + max(30, 30) + 2 x 10 = 885.00 | 885.00 |
| L at anchor_z | 959.84 + 130 + 6 + 15 + 30 + 10 - 265 = 885.84 | 885.84 |
| L_min / at anchor, plus 1 m | 1025 + 110 = 1135.00; 1209.84 + 191 - 265 = 1135.84 | 1135.00, 1135.84 |
| Screw spare | 900 - 885.84 = 14.16 (= S1-4 high margin at park); 1 m short 1135 - 900 = 235 | 235 short |
| Start minus 0.75 m core top | 834.84 - 792.50 = 42.34 | 42.34 |
| Mass, load | 8 + 2 + 6 + 3 + 3 + 0.15 + 15.6 + 8.234 + 12.686 + 9.363 + 5.919 + 1.065 + 1.05 = 76.067 | 76.07 |
| COM, load | sum m z = 50 569.3 kg mm / 76.067 = 664.80 z_S | 664.8 |
| Tip force at COM, load | 76.067 x 9.81 x 304 / 664.80 = 341.2 N | 341 |
| Tip force at frame top | 76.067 x 9.81 x 304 / 1285 = 176.5 N (park 60.467: 140.3 N) | 177, 140 |

Item checks (HAND): base plate 644 x 608 x 12 mm3 x 2700 = 12.686 kg; guide rod pi 0.01^2 x 1.2 x 7850 = 2.959 kg each; T8 at nominal 8 mm, pi 0.004^2 x 0.9 x 7850 = 0.355 kg each; gear centroid at load 1161.84 + 52 + (28.23 + 62) / 2 = 1258.955; core at load (161.17 + 911.17) / 2 = 536.17.

The Engineer's correction 4 holds. F h = W g a with the pivot at the floor edge, so F at the frame top is W g a / h_top, which does not depend on the COM height. Lever a = min(644, 608) / 2 = 304, with the COM on the axis (three-fold screw, pinion and motor sets; the two guide rods at 0 and 180 are symmetric).

## 3. K7 depth-separated pairs

There are 1037 depth-separated pair tests over 246 distinct pairs. In 222 of those pairs the XZ projection alone also clears the class requirement. The remaining 24 depend on the depth band. Every one of them is two parts at different azimuths. In each, the plan gap is at least the band gap, so the band gap is a true lower bound on the 3D clearance. All are **real clearances**, and none is an LF-8 artefact. The LF-8 box-test artefacts are the pairs that fail the side-view box and are relieved as plan-separated, as tabulated in the spec sign-off section 6.

| Pair (a and b mirror) | Class | Poses | Band gap (MEASURED) | Plan gap (MEASURED) | HAND |
|---|---|---|---|---|---|
| guide_lug_a\|frame_upper_b | G 10 | all | 100.00 | 100.36 | lug y [-20, 20], member 150 +/- 30: 120 - 20 = 100 |
| motor_mount_a\|guide_a | G 10 | load, park, capture_end (XZ 9.66) | 105.32 | 105.32 | |
| pinion_a\|guide_a | G 10 | load, park, capture_end | 67.10 | 73.18 | pinion y up to -47.61 + 39.51 = -8.10; guide 80 - 21 = 59: 67.10 |
| motor23_a\|guide_a | G 10 | load, park, capture_end | 105.32 | 105.32 | motor y up to -46.32; 59 + 46.32 = 105.32 |
| nut_housing_a\|motor_mount_a | F | all | 101.32 | 101.32 | |
| nut_housing_a\|pinion_a | F | all | 63.10 | 69.18 | 55 - (-8.10) = 63.10 |
| motor_mount_a\|screw_a, \|nut_a | F | all | 122.32, 105.32 | 122.33, 105.32 | |
| pinion_a\|screw_a, \|nut_a | F | all | 84.10, 67.10 | 90.18, 73.18 | |
| motor23_a\|screw_a | F | all | 122.32 | 122.33 | |
| guide_member\|frame_upper_b | F | all | 110.00 | 112.93 | rod y [-10, 10]: 120 - 10 = 110 |

Every band comes from a `place` record (FIX 4a/4b footprints in force), so each band contains its part.

## 4. Findings

### BLOCK

None.

### FIX

**LF1.1-1 Holder flange drawn 8 mm low; holder z_rule short by holder.flange_thickness.** The params stack (test_P18, `check_stack.collar_top_z_A`) stacks holder.length 88, then flange 8, then nut plate 8, then 6.75 to the collar top. The flange underside is therefore at the holder.length top:
- HAND z_A: holder bottom 49.09, flange underside 137.09, flange top 145.09, nut plate 145.09 to 153.09, collar 153.09 to 159.84.
- Flange underside to rim: 137.09 - 128.50 = 8.59 = stroke_gap_R 13.126 - drop 4.536 = witness.zone_high (pose K d+1). In pose R it is 13.126, the params definition.

The spec ends the holder at holder_bottom + holder.length = 137.09, and the script draws the flange from 129.09 to 137.09. That gives the 0.59 gap the Engineer measured and leaves an undrawn 8 mm under the wing-nut plate. No S1 check changes: the nearest affected pair is ring|holder, which goes from 177.75 to 169.75 against g_min 10. The drawing misstates the R-to-K stroke gap, and the Designer's gate reads it.

Fix, Engineer, with the Designer ruling the shape field:
- Spec holder z_max = "holder_bottom + holder.length + holder.flange_thickness".
- Script flange from holder_bottom + holder.length up to that z_max; holder tube from holder_bottom to holder_bottom + holder.length.
- The spec carries no other holder edge.
- Recommended: an LF-16-style lint that holder z_max + (nut.plate_thickness + washer.thickness - nut.washer_pocket_depth) + collar.top_above_plate = collar_top within 0.05, with a B control at the r1 rule (fires by 8.00). This is the term my 1.1 (b) sign-off passed.

### NOTE

**LF1.1-2 The governing park clearance is tested by no check.** Park 959.84 is set by the entry-plane term: 959.84 - 50 - (159.84 + 750) = 0.00. S1-3 measures from the load plane (G1) and reports 117.34. The load pose draws the core at mid-insertion, bottom 101.17, with 108.67 to the tip, not at the critical instant (core bottom on the collar top, top 909.84 z_A, gap 50.00). The identity holds by construction. Proposal: S1-3 also reports the entry-plane margin, with no threshold.

**LF1.1-3 check_stack.reported reads params stop.start_z where the class start belongs.**
- `start_tip_minus_core_top_mm` uses `P.get("stop.start_z")[0]`, which is the class start 834.84 by coincidence. The params pair [834.84, 965] still carries 965 = 315 + 650 from the retired height_range[1].
- `global_vars` passes start_tip_max = 965 into the park-rule names before overwriting it with 834.84; no current expression reads it.

Both go stale when Step 4 rewrites stop.*. Read `class_starts_z_A` for the capture class.

**LF1.1-4 Zero and near-zero margins are design identities, not drawing slack.**
- drill_head|collar G 25 passes at 25.000 (stop.height_z = collar top + g_stop).
- S1-1 upper bound 0.00 (start = stop + travel).
- Entry-plane clearance 0.00 (LF1.1-2).
- S1-4 low margin 0.84, set by anchor_z 265 against ring.position_above_tip 130.
- Screw spare 14.16.

Any change to the ring offset, the anchor or the guide heights moves S1-4 and L together.

**LF1.1-5 The cutter head is outside the keep-out radius.** Head r 177.8 / 2 = 88.90 against icd.keepout_radius 86.2 (tube basis), 2.70 outside, over head_length 106.369 above the tip. At capture_end the head clears the collar by 25.00 and the wing-nut body (r 83.14, top 153.09 z_A) by 31.75. No check is affected. A consumer that takes 86.2 as the drill envelope radius below head_top is 2.70 short.

**LF1.1-6 Mass-report modelling choices.**
- The 0.75 m core is counted in full at load, where the operator holds it mid-insertion: +15.6 kg at COM 536.17.
- The base plate is solid; the spigot hole r 80.2 x 12 is 0.655 kg.
- The receiver, collet, holder, wing nut and blocks are omitted.
- The third screw frame member, screw and motors are counted but not drawn.

Arithmetic agrees to 0.1 N.

**LF1.1-7 Side view omits the third leg by spec.** The 270 screw, nut, anchor, guide and lift motor project at x 0, depth -160. The 90 pinion and NEMA 23 project at x 0, depth +95 to +218. K7 does not test them; the spec states two. S2 (plan) carries them.

### Gameplan lines

None from this review beyond the Engineer's open items 4 and 5 (l.144, l.229).

## Verdict

CROSS-REVIEW PASS. Every hand value matches its JSON value to 0.01 mm (0.1 N for forces). LF1.1-1 is open to the Engineer, with the shape ruling to the Designer, before M1 acceptance.
