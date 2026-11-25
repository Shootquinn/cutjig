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

## Re-check r2

Inputs: step1.1_engineer_revision_r2.md, s1_spec.yaml (r2 edits), s1_side_poses.py, check_stack.py, sketch_common.py (stack_ties lint), fixtures/manifest.yaml (K6-B7), sketches/s1_checks_r2.json. HAND values are DERIVED; JSON values are MEASURED.

### Findings

| ID | HAND | r2 (JSON / code) | Status |
|---|---|---|---|
| LF1.1-1 | holder z_A 49.09 to 49.09 + 88 = 137.09 (tube), flange 137.09 to 145.09 (z_S 197.09 to 205.09); rim 40 + 88.5 = 128.50, gap 137.09 - 128.50 = 8.59 = 13.126 - 4.536; tie 145.09 + 8.00 + 6.75 = 159.84 = collar_top | holder z_max = holder_bottom + holder.length + holder.flange_thickness; flange drawn 197.09 to 205.09; stack_ties.holder_flange linted in K6 (pass); K6-B7 at the r1 rule: 137.09 + 8.00 + 6.75 = 151.84 vs 159.84, "8.00 apart", fires | **closed** |
| LF1.1-2 | 959.84 - 50 - (159.84 + 750) = 0.00 | reported entry_plane_margin_mm 0.0 (lengths from park_lengths, always_loaded included) | **closed** |
| LF1.1-3 | capture class start 184.84 + 650 = 834.84; 834.84 - 792.50 = 42.34 | start_tip_minus_core_top_mm reads class_starts_z_A for capture_core_length: 42.34. global_vars sets start_tip_max once, after park_tip, from the class starts (834.84); the params 965 entry is gone | **closed** |
| LF1.1-4 to -7 | | NOTEs, carried to the Designer list (items 8 and 9) | open as NOTE, no action required |

### Hand values on r2 (unchanged from r1)

All agree to 0.01:
- Tips z_S: load and park 1019.84, start 894.84, capture_end 244.84.
- Park 959.84 z_A, stroke 775.00. Plus 1 m: 1209.84 and 1025.00.
- S1-1 650.00, S1-2 125.00, S1-3 367.34 and 117.34, S1-4 least 0.84, S1-5a 192.34, S1-5b 142.00 (bearing|collar 301.84 - 159.84), S1-6 x +/-138.564 with depth 80.00, S1-7 607.66 (spare 72.73).
- L_min 885.00, at anchor 885.84 (1135.00 and 1135.84 with the 1 m core).
- Highest points 1969.84 / 1844.84 / 1285.00 / 1969.84.

Pairs the flange move touches:
- ring|holder at capture_end: 374.84 - 205.09 = 169.75 vertical. 2D, the ring bore r 100 against the flange OD r 72.04 gives sqrt(169.75^2 + 27.96^2) = 172.04 (Engineer 172.04).
- bearing|holder: 361.84 - 205.09 = 156.75, above S1-5b's 142.00.
- head|holder at capture_end: 244.84 - 205.09 = 39.75.

### Spec placement re-signature (r2 edits)

| Edit | HAND | Ruling |
|---|---|---|
| holder `bore_cone: collet` | collet z_A 40 to 40 + 25 + 3 + 8 / 2 = 72. Cone r(z) = 67.29 - (z - 40) tan 10. At the holder bottom 49.09: 67.29 - 9.09 x 0.17633 = 65.687. At 72.00: 67.29 - 32 x 0.17633 = 61.648 (z_S 109.09 and 132.00, as the Engineer states). The holder piece runs from the cone face to r 67.29 over 49.09 to 72.00, then from r 50 to 67.29 to 137.09 | placement correct; contact on the cone face |
| receiver\|collet C | collet foot r 67.29 at the register bore 67.29; foot on the floor at 40 | correct as drawn |
| receiver\|core_seat C | seat bottom 40 = floor top 40 | correct |
| receiver\|holder C | holder OD drawn at the register bore 67.29 | correct as drawn. The part has g_reg 0.25 (OD 67.04), so the real pair is G 0.25; Designer at M1 |
| collet\|core_seat C | seat r 47 to 50, collet bore r 50 | correct |
| collet\|holder C | shared cone face, 49.09 to 72.00 | correct; resolves the r1 overlap of 313.12 mm2 per side (K7-B15) |
| collar\|holder F | 153.09 - 145.09 = 8.00 (nut plate 7.5 + 1.3 - 0.8) | correct for the S1 holder, which ends at the flange top. In build_parts the tube runs through the plate to the collar, which makes it C. Designer at M1 |
| stack_ties.holder_flange | 145.09 + 8.00 + 6.75 = 159.84 | correct; it closes the term my 1.1 (b) sign-off passed |

Re-check NOTE R2-1: the five C contacts are idealised zero-clearance fits (register bore, cone face). They are right for S1 placement. They are not fit values, and nothing downstream reads them as clearances.

**SPEC PLACEMENT SIGNED (Loftsman, r2).** The holder section (bore 56.75, tube through the nut plate, collar 6.0 on a 0.75 lift play) stays with the Designer at M1.

### Verdict r2

RE-CHECK PASS. LF1.1-1, LF1.1-2 and LF1.1-3 are closed. BLOCK 0, FIX 0 open, NOTE 4 carried plus R2-1.

## Re-check r3

Inputs: step1.1_engineer_revision_r3.md, s1_spec.yaml (r3 rows), sketch_common.py (`assess_pair` plan-contact branch, `plan_contact_fn`), s1_checks_r3.json. Plan footprints were re-evaluated in scratch from check_stack placements. That evaluation is MEASURED and writes no file. HAND values are DERIVED.

### Plan-contact rule: ruling

The code (sketch_common.py l.516-523, l.577-586) behaves as follows:
- The relief runs only when the class is C, the side-view state is "overlap", and both rows carry `place`.
- It passes when the plan distance is <= 0.05 and the plan overlap is <= 0.01 mm2.
- G and F do not reach it; they keep the plan-separated relief. C pairs are not swept.

1. **Soundness.** It holds when each plan footprint contains its part's plan projection at every z. The footprint is z-independent, so the part lies inside footprint x [z_min, z_max]. Two such cylinders with interior-disjoint footprints cannot interpenetrate, whatever the part's shape. A side-view overlap proves that the z ranges overlap, so the touching footprints mean contact on a vertical face. The premise is containment. Wherever containment holds, the rule cannot hide a 3D interference.
2. **Tolerance.**
   - Circle against line (arm on block, r 21): overlap area A ~ (4/3) sqrt(2 r d) d. A = 0.01 at d = 0.011 mm.
   - Line against line with face length L: d = 0.01 / L. For the arm on a 60 face that is 0.00017 mm.
   - The largest interference the area bound can hide is 0.011, below TOL_C 0.05.
   - Live overlaps are 0.0014 (arm|block) and 0.003 (arm|member). These are circumscribed 128-gon artefacts: the polygon is r / cos(pi/128) = 1.0003 r and conservative.
3. **Class scope.** C only, which is correct. Extending it to G would pass a zero gap. F already passes touching in side views (LF-9) and is relieved at a plan gap > 0.05, so it needs no plan-contact.
4. **Where containment fails, the rule can hide interference.** That is the case for **frame_upper**, which is FIX LF1.1-8 below. The anchor and guide blocks are round r 21 by declaration only (sign-off NOTE 5). Their contact with the arm is a tangent line, not a face; NOTE LF1.1-9.

**PLAN-CONTACT RULE SIGNED (Loftsman)** for C pairs between placed rows whose footprints contain their parts. The gameplan l.140 text should carry that containment condition.

### Placement of the new rows (HAND against stack and JSON)

| Row | HAND | Stack / JSON |
|---|---|---|
| bracket_anchor_a, bracket_guide_a | r_in 160 + 21 = 181 (block circle tangent); r_out 300 - 30 = 270 (member face); hw 30. x: 181 cos 150 = -156.75, 270 cos 150 = -233.83, +/- 30 sin 150 = 15, giving [-248.83, -141.75]. y: 90.50 to 135.00 +/- 30 x 0.866 = 25.98, giving [64.52, 160.98]. z_A 265 to 295 and 1165 - 30 = 1135 to 1165 | x [-248.83, -141.75], y [64.52, 160.98], z_A 265 to 295 and 1135 to 1165 |
| descent_stop_post | r 200 to 215, hw 30. x: [215 x -0.866 - 15, 200 x -0.866 + 15] = [-201.20, -158.21]. z_A 265 + 30 = 295 to 314.84 - 12 = 302.84 (7.84). Plan: inside the arm (r 181 to 270, same hw), plan overlap 30 x 15 x 2 = 900 | x [-201.20, -158.21]; z_S 355.00 to 362.84; post\|arm plan overlap 900.0, side-view face contact at 295 (ordinary C) |
| motor_shaft_a | r 142 - 21 = 121 to 142, hw 4. x: [142 x -0.866 - 2, 121 x -0.866 + 2] = [-124.98, -102.79]. z = ring top + 52 +/- 4: park 1101.84 + 52 = 1153.84 +/- 4 z_A; load 1213.84 +/- 4 z_S | x [-124.98, -102.79]; park z_A 1149.84 to 1157.84; load z_S 1209.84 to 1217.84 |
| pinion_axis_a | 95.22 cos 210 = -82.46; 218 cos 210 = -188.79 | -82.47 to -188.79 |

Contacts and clearances:

| Pair | HAND | MEASURED |
|---|---|---|
| shaft\|motor23 | shaft r_out 142 = motor r_in 142, shared edge | plan distance 0.000, overlap 0.000 |
| shaft in the pinion hub | r 121 to 140 inside the hub (pinion r_out 140); N | N |
| nut_housing_a\|bracket_anchor_a | 305.84 - 295 = 10.84 | 10.840 |
| ring\|bracket_anchor_a | 314.84 - 295 = 19.84 | 19.840 |
| ring\|descent_stop_post | 314.84 - 302.84 = 12.00 | 12.000 |
| nut_housing_a\|post | plan 200 - 185 = 15.00 | 14.993 |
| nut_housing_a\|bracket_guide_a, park | 1135 - 1110.84 = 24.16 | 24.160 |
| ring\|bracket_guide_a, park | 1135 - 1101.84 = 33.16 | 33.160 |
| gear\|bracket_guide_a, park | plan 181 - 126.32 = 54.68 (gear bottom 1182.07 - arm top 1165 = 17.07 vertical) | plan 54.646, side 37.295 |
| motor23_a\|bracket_guide_a, park | band 64.52 + 46.32 = 110.84 | band 110.838, plan 116.09 |
| pinion_a\|bracket_guide_a, park | | plan 96.13 |

The gear line corrects the Engineer's table: the true lower bound is max(plan 54.65, side 37.30) = 54.65. The "x gap 15.43" in that table is a projected separation, not a clearance.

### Findings r3

**FIX LF1.1-8. frame_upper footprint and drawing are a circle r 30; the part is a 30-6060, a 60 square with circumradius 42.43.**
- The Designer's F2 places the arm "on the member face at r 270", so the square is face-on to the axis: r 270 to 330, half-width 30.
- At theta 150 / 30 that square projects 60 (cos 30 + sin 30) = 81.96 wide: x [-300.79, -218.83] for _a. The drawing shows 60 ([-289.81, -229.81]).
- Its depth band is [109.02, 190.98], against the drawn [120, 180].
- The round footprint breaks the containment premise of the plan-contact rule and of plan-separated, by up to 12.43.

Scratch evaluation of the square footprint against every placed row in all four poses (MEASURED):
- Only the four arms come within 20 mm: distance 0.000, overlap 0.000.
- Nothing is hidden today. Every side and depth value moves by 12 mm or less, and every relieved pair involving frame_upper keeps more than 84 mm.

Fix (Engineer):
- frame_upper_a/_b place: r_in "frame_upper.radius - profile.width / 2", r_out "frame_upper.radius + profile.width / 2", half_width "profile.width / 2", footprint radial.
- The script draws the projected width from place.x.
- The x centre stays at r cos theta = -259.81, so the TP-3 centre check is unchanged.
- arm|member then shares an edge in plan: plan-contact distance 0, overlap 0.

**NOTE LF1.1-9.** arm|block "C" is a tangent line in plan: the declared round block r 21 touches the arm's flat end at r 181. That is right for S1 placement. The block shape is Step 2's (ASSUMED).

**NOTE LF1.1-10.** bracket_anchor_a and liftmotor_a overlap in plan by 251.86 mm2: the motor's circumscribed r 29.70 reaches r 189.70 under the arm's inner end. They are separated by 265 - 240 = 25 vertically (the coupling), and the undeclared F pair passes. The motor mount to the arm or block is Step 2's.

**NOTE LF1.1-11 (post|block).** In the side view, block x [-159.56, -117.56] and post x [-201.20, -158.21] overlap by 1.35 in x and touch at z 295. As undeclared F this reads touching (LF-9). In plan they are 200 - 181 = 19 apart.

### Spec placement re-signature (r3)

**SPEC PLACEMENT SIGNED (Loftsman, r3)** for these rows:
- bracket_anchor_a/_b and bracket_guide_a/_b
- descent_stop_post
- motor_shaft_a/_b
- pinion_axis_a/_b

The signature is subject to FIX LF1.1-8 on frame_upper_a/_b, which is open to the Engineer. LF1.1-8 changes no S1 check value, but containment is the premise of the signed plan-contact rule.

### Verdict r3

RE-CHECK PASS. BLOCK 0, FIX 1 open (LF1.1-8), NOTE 3 new (LF1.1-9 to -11). Carried: LF1.1-4 to -7 and R2-1.

Gameplan l.140 plan-contact text: add "both footprints contain their parts".

## Re-check r4

Inputs: step1.1_engineer_revision_r4.md, s1_spec.yaml frame_upper_a/_b `place`, fixtures/manifest.yaml K7-B20. HAND values are DERIVED; quoted values are MEASURED by the Engineer.

### LF1.1-8: closed

| Item | HAND | r4 |
|---|---|---|
| Footprint | r 300 -/+ 30 = 270 to 330, hw 30, radial, one face toward the axis | place r_in radius - width / 2, r_out radius + width / 2, hw width / 2, radial |
| Drawn x, theta 150 | 330 cos 150 - 15 = -285.79 - 15 = -300.79; 270 cos 150 + 15 = -233.83 + 15 = -218.83; width 60 (cos 30 + sin 30) = 81.96 | -300.79 to -218.83 |
| Depth band | 135 - 30 cos 30 = 109.02 to 165 + 25.98 = 190.98 | 109.02 to 190.98 |
| arm\|member | arm r_out 270 = member inner face 270, shared 60 edge | plan-contact 0.000 / 0.000 |
| K7-B20 (rot 45) | The corner is 30 sqrt 2 = 42.426 from the centre, at r 300 - 42.426 = 257.574, 12.426 into the arm face. The wedge between two 45 deg faces of depth h has area h^2 = 12.426^2 = 154.41 mm2. Its base 2h = 24.85 lies inside the arm width 60. Count: 2 arms x 4 poses = 8 | fires 8 x 154.416 mm2 |
| ring\|frame_upper_a, capture_end | Plan: the ring disk r 210 against the inner face at r 270 gives 60.00 (59.94 with the circumscribed 128-gon r 210.06). Side: ring rim x -210 against member x -218.83 gives 8.83 < 10. The true clearance is at least max(60, 8.83) = 60 | plan-separated 59.944, side 8.827 |
| guide_lug_a\|frame_upper_b (spot check) | Member inner corner (248.83, 109.02) against lug y <= 20: 89.02 >= 10 | K7 pass |

The side-view drop from 19.81 (r3) to 8.83 is the true projected width of the square. The real clearance is the plan 60.

### Proposed gameplan wording

- **l.141** (projected_extent) is correct as written.
- **l.144** (117 controls: Z 35, B 81, smoke 1; K8-B7 planted 3) is correct as written.
- **l.140** has two amendments.
  1. The clause "as a true section with no circumscribing circle for a non-round part" conflicts with signed footprints:
     - The lift motor is a circumscribing circle r 21 sqrt 2 = 29.70 around a 42 square (FIX 4b, 1.1 (b)).
     - Every round part is a circumscribed 128-gon.
     - Containment is the condition for F and G relief, and a circumscribing footprint satisfies it conservatively.
     - Only plan-contact needs more. A touch on a circumscribing boundary does not prove the part touches, so a C pair passes plan-contact only when both footprints are the part's true plan section. The 128-gon of a round part counts as true within the 0.01 mm2 area bound.

     Replace that clause with: "every row's plan footprint contains its whole part (a circumscribing footprint is admitted for the F and G relief); plan-contact for a C pair requires both footprints to be the parts' true plan sections (a 128-gon for a round part)".
  2. Tag the orientation as a design value: "(a 30-6060 member is a 60 x 60 square, one face toward the axis, ASSUMED, Designer M1 r2 F2)".

  The rest of the l.140 text and its control list are correct.

Live C plan-contact pairs against amendment 1:
- arm|member: square against rectangle, true.
- shaft|motor23: rectangles, true.
- arm|block: the block is round r 21 by declaration (NOTE LF1.1-9), so its footprint is its declared section.

None is a circumscribing footprint, so amendment 1 changes no result.

### Member placement re-signature

**SPEC PLACEMENT SIGNED (Loftsman, r4)** for frame_upper_a/_b: radial r 270 to 330, hw 30, face toward the axis. With this, the r3 placement signature holds without condition. The Designer re-signs the drawn width of 81.96.

### Verdict r4

RE-CHECK PASS. LF1.1-8 is closed. BLOCK 0, FIX 0 open. Wording note: the two l.140 amendments above. Carried NOTEs: LF1.1-4 to -7, LF1.1-9 to -11, R2-1.
