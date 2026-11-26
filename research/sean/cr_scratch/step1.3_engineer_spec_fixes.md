## Corrections to the brief

1. **Shoulder position.** The brief places the journal step's shoulder at 272. The Designer's FIX 3 layout, which is the one adopted, puts the screw shoulder (Tr12 body, d 12) on the upper inner race at 288. The M10x1 thread and journal 10 run from the block underside (265) to 288. The locknut sits under the lower inner race (266 to 272), and the block carries a shoulder bore 20 under the outer races (face at 272) and a cover bore 16 over them (face at 288).
   - A screw shoulder at 272 would need the screw to be 12 below 272 and 10 above it, through the bearings and up the Tr12 body. That cannot be built.
   - With the screw shoulder at 288, both axial directions close in the drawn parts:
     - Cut case (screw pulled up): locknut → inner races → outer races → cover at 288.
     - Lifting cases (screw pushed down): screw shoulder → inner races → outer races → block shoulder at 272.
   - The Loftsman's "d 12 shoulder under the lower inner race at 272" (FIX 1) is the same property with the parts mirrored. The Designer's layout keeps the locknut on the thread end and is the one drawn.
2. **The coupling closes at 36 under the Designer's z_rules; 36.5 is not needed.** The Loftsman's 36.5 assumes a screw-end engagement of 10 and a coupling top 1.5 under the block. Under the Designer's remedy B, the coupling is centred on the motor shaft tip and the screw end starts `shaft_gap` above it. At 36 this gives shaft tip 253, screw end 254 to 265 (engaged 9), coupling 243 to 263, which is 2.0 below the block (2.06 at the bore corner) and 12.0 above the pilot.
   - Shaft|screw end: 0.00 mm² overlap, 1.00 apart (MEASURED, dry run).
   - The smallest value that closes the stack is 35. At 35 the coupling is 1.12 from the bore corner, which passes G 1. At 34 it would be 0.5 from the shoulder bore. The ruling keeps the Designer's 36 because 36 closes, so 36 stands.
   - Bar length: 911.00 at 36, 911.50 at 36.5 (DERIVED).
3. **Bore expressions had an operator-precedence error (found by the dry run, fixed here).** `nut_housing_c.section_u` as first written read `UC - nut_body_od / 2 + nut_float`, which is the u of r 10.5, not r 11.5, on the -u side. The dry run read a 15.00 mm² nut|housing overlap. The two -u bore and counterbore expressions now carry parentheses `UC - (nut_body_od / 2 + nut_float)`, and the overlap reads 0.00.
4. **The nut clamp is sized against the home switch.** The ruling asks for a clamp over the flange. A clamp as wide as the housing (OD 50) puts its top at 1113.84 at park, 5 radially from the switch (r 185 to 190): 9.57 in plane, under G 10 (DERIVED). At OD 46 (r 23 against switch r 190) it reads 10.75 (MEASURED). The home-switch lever tip moves from the Designer's 1112.00 to 1115.00 so that it keeps the 1.16 free gap over the clamp top at park (DERIVED). Both are Designer values to sign.
5. **The anchor locknut is cut, not unsectioned.** As an outline over the screw it read 60.00 mm² against the screw journal. As cut pieces r 5 to 9 it reads C at 0.00 (MEASURED).

## Dry-run table

Script: `dry_p2f.py` in the session scratchpad, run on the live `docs/sketches/s3_spec.yaml`. It evaluates the `section_u` pieces (or the place / plan_poly rectangle) in (u, z_A) through `check_stack.eval_expr` and computes `sketch_common.overlap_area` and `min_distance`. coupling_length variants use an overlay copy. All values MEASURED; K7 tolerances as spec (C at 0.05 with 0.01 mm², G at g_min - 0.05).

Coupling stack per `liftmotor.coupling_length` (z_A):

| coupling_length | motor | shaft | coupling | screw end | shaft\|end (G 1) | coupling\|anchor (G 1) | coupling\|locknut (F) | bar length | closes |
|---|---|---|---|---|---|---|---|---|---|
| 25 (old) | 192-240 | 240-264 | 254-274 | 265-265 | 1.00 (zero length end) | 0.50 | **48.00 mm² overlap** | 900.00 | no |
| 35 | 182-230 | 230-254 | 244-264 | 255-265 | 0.00 mm², 1.00 | 1.12 | 2.00 | 910.00 | yes (smallest) |
| **36 (drawn)** | **181-229** | **229-253** | **243-263** | **254-265** | **0.00 mm², 1.00** | **2.06** | **3.00** | **911.00** | **yes** |
| 36.5 | 180.5-228.5 | 228.5-252.5 | 242.5-262.5 | 253.5-265 | 0.00 mm², 1.00 | 2.55 | 3.50 | 911.50 | yes |

Pairs at coupling_length 36 (capture_end unless marked):

| Pair | Declared | Overlap mm² | Distance |
|---|---|---|---|
| screw_c \| anchor_bearing_c | C | 0.00 | 0.00 (was 32.00 overlap) |
| screw_c \| guide_bearing_c | C | 0.00 | 0.00 (was 16.00) |
| screw_c \| anchor_c | F | 0.00 | 2.00 |
| screw_c \| guide_c | F | 0.00 | 7.00 |
| anchor_c \| anchor_bearing_c | C | 0.00 | 0.00 (axial faces 272, 288) |
| anchor_locknut_c \| screw_c | C | 0.00 | 0.00 |
| anchor_locknut_c \| anchor_bearing_c | C | 0.00 | 0.00 |
| anchor_locknut_c \| anchor_c | F | 0.00 | 1.00 |
| screw_c \| nut_c | C | 0.00 | 0.00 |
| nut_c \| nut_housing_c | C | 0.00 | 0.00 (counterbore shoulder; was 152.00 at 22 / 8 per the raisers) |
| nut_c \| nut_clamp_c | C | 0.00 | 0.00 |
| nut_clamp_c \| nut_housing_c | C | 0.00 | 0.00 |
| screw_c \| nut_housing_c; screw_c \| nut_clamp_c | F | 0.00 | 5.50; 9.00 |
| ring \| nut_housing_c | C | 0.00 | 0.00 |
| nut_housing_c \| anchor_c | G 10 | 0.00 | 10.84 |
| liftmotor_shaft_c \| screw_end_c | G 1 | 0.00 | 1.00 |
| coupling_c \| liftmotor_pilot_c | G 1 | 0.00 | 12.00 |
| screw_end_c \| anchor_locknut_c; coupling_c \| anchor_locknut_c | F | 0.00 | 1.41; 3.00 |
| screw_end_c \| screw_c; standoffs_c \| anchor_c; standoffs_c \| liftmotor_c | C | 0.00 | 0.00 |
| park: nut_housing_c \| home_switch_c | G 10 | 0.00 | 12.23 |
| park: nut_clamp_c \| home_switch_c | G 10 | 0.00 | 10.75 |
| park: ring \| home_switch_c | G 10 | 0.00 | 20.16 |
| park: nut_housing_c \| guide_c; nut_clamp_c \| guide_c | G 10 | 0.00 | 24.17; 21.16 |

Home-switch lever tip at park: 1115.00 z_A, 1.16 above the clamp top (1113.84) (DERIVED from the lever field expression).

## Fix table

| Raiser item | Closed by | Evidence |
|---|---|---|
| Designer FIX 1 = Loftsman FIX 3 (counterbore, upward seat) | Overlay `jackscrew.nut_body_od` 22 and `nut_flange_thickness` 8 (Designer). Housing `section_u`: bore D23 from the housing bottom to the counterbore shoulder at `nut_z + nut_length / 2 - nut_flange_thickness`, counterbore D43 x 8 above it. New row **nut_clamp_c**: ring OD 46, bore 30, 3 thick on the housing top, bolted (bolts not_drawn); overlay `ring.nut_clamp_od` 46, `nut_clamp_id` 30, `nut_clamp_thickness` 3, ASSUMED, **Designer to sign**. Declarations: nut_c\|nut_housing_c C (cut-case seat), nut_c\|nut_clamp_c C (lifting cases), nut_clamp_c\|nut_housing_c C, plus G 10 against home_switch_c and guide_c | dry run above; K2 396 keys resolve |
| Designer FIX 2 = Loftsman FIX 4 (coupling) | Remedy B: `liftmotor.coupling_length` 25 → 36; new `liftmotor.shaft_gap` 1. coupling_c z_rule = shaft tip ± coupling_height / 2 (shaft tip = `anchor_z - coupling_length + shaft_length`). screw_end_c from shaft tip + shaft_gap to anchor_z. liftmotor_shaft_c\|screw_end_c declared G g_min 1 (Loftsman FIX 4 (b)). Source texts of coupling, coupling_height, screw_end_d and the liftmotor / standoff shapes updated (standoffs 36) | coupling table above |
| Designer FIX 3 = Loftsman FIX 1, 2 (fixed end, journals) | Overlay `jackscrew.locknut_od` 18, `locknut_thickness` 6, `anchor_shoulder_bore` 20, `anchor_cover_bore` 16. anchor_c `section_u` in three bands per side: shoulder bore 265 to 272, bearing bore 26 272 to 288, cover bore 288 to 295. screw_c `section_u` steps: journal 10 265 to 288, body 12 288 to 1135, journal 10 1135 to 1165 (place and z_rule unchanged for X1). New row **anchor_locknut_c** (cut, 266 to 272, in fixed_g10, keepout G 0). Removed from not_drawn and from the figure note. Chain notes name the axial faces | dry run above |
| Designer FIX 4 (home switches) | home_switch_c: lever field (from the body bottom inboard corner to r `liftsync.lever_r_tip` 182 at the clamp top at park + `liftsync.lever_free_gap` 1.16), with the shape stating the free state and the trip about 2 above park. home_switch_a/_b shape: "20 x 6 radial rectangle (inset; no lever drawn in plan)". G 10 home_switch_c\|nut_clamp_c added | lever tip 1115.00 |
| Designer FIX 5 (load_comp_c) | Label "compression per screw: static 79, capture 113, retract (F_bind 300) 179, stall up 343 N", key liftload.f_bind; shape the same | spec |
| Designer FIX 6 (handedness, rubric) | `side` sign -1 on frame_upper_c and +1 on pinion_c (axes section). V7 and V10 rubric lines marked visual-only with the Designer's V10 text. Section-handedness rubric line names the four predicates | spec |
| Designer section 7 item 9 (core mass) | Overlay `liftload.core_mass_capture` 10.4 (DERIVED, Quinn SVR). s3_checks.S3-2.core_mass reads the key and checks_s3.loads reads it (literal removed) | capture lift 113.31 unchanged |
| Loftsman FIX 5 (base_plate\|base_frame) | Declared F in S3 on both rows: contact off the plane, certified by S1/S2 | dry run (Loftsman): 5.00 apart, F |
| Loftsman FIX 6 (certifiers) | `chains` certifiers name sketch and pair ("S1 collet\|core_seat C"). s3_checks.S3-3.records: resolved at run time to the latest accepted, unsuperseded record of that sketch, --stale clean, S3 accepted after S1 r8 and S2 r9. drill_head\|core_750 on chains a, b, c: "declared: load application (row load_cut, S3-1 reads it +Z)". The S3-3 rule text names the axial-face requirement and the P4 symmetry lint | spec |
| Loftsman R2 (x1_exempt) | Unchanged in the spec. Field scope and --accept refusal listed for P4 | - |
| Loftsman NOTE 2 (lever) | Covered by Designer FIX 4: the lever is a line outside K7 and drawn in its free state; the body pairs stay G | - |
| Loftsman NOTE 3 (bar length) | 911.00 at 36; to Sean at M2 | below |

Spec now 65 rows (nut_clamp_c and anchor_locknut_c added); not_drawn 10 entries (locknut and retaining ring removed, clamp bolts added); the part list gains "anchor locknut" and "nut clamp ring".

## Check results

All MEASURED after the edits.

| Run | Result |
|---|---|
| `--controls` (default 12 jobs) | Z clean 75/75, B fired 208/208, smoke 2/2: 285/285 match; wall 126.0 s |
| `--stale` | 2 records, 5 differences, exit 1. s1_checks_r7.json: jackscrew.lead 8 → 3, jackscrew.nominal 8 → 12, liftmotor.coupling_length 25 → 36. s2_checks_r5.json: jackscrew.nominal 8 → 12, liftmotor.coupling_length 25 → 36 |
| `--stale --include-unaccepted` | 15 records, 32 differences: the 5 above, the same keys on the older wip records, and coupling_length on the P2 previews wip s1 r8 and s2 r9 |

coupling_length joins the S1 r8 and S2 r9 key lists. No new revision opens. Per detail 1 common (i), S1 and S2 re-run in the same session: the Designer's dry run at 36 (`s1 --rev 7`, `s2 --rev 5` with `--overlay`) has every check result equal to the run at 25. S1-4 0.84, S1-5b 142.00, S2-2 52.80, S2-5a 11.71 and S2-5b 19.84 are unchanged (Designer sign-off section 7, MEASURED there). The P2 previews s1 r8 / s2 r9 in wip/ are stale on coupling_length. P6 re-runs them as drawn revisions.

- K2 on s3_spec.yaml: pass, 396 spec keys resolve, 179 overlay leaves, 20 expr leaves agree (the two missing nut keys are now supplied).
- X1: pass, 70 shared rows compared, 3 skipped, 3 exempt (anchor_a/_b/_c).
- checks_s3 on the floor-only figure (no stub before (c), as at P2): S3-1, S3-2, S3-3 fail, cause absent. reported: 9 of 10 items (tension_segment needs drawing). S3-2 margins unchanged: P_cr 1363.8 N; 17.20 / 12.04 / 7.61 / 3.97.

## Items for P4 (harness, each with Z and B)

1. **Symmetry premise lint (Loftsman R1).** Anchor, screw, nut and nut-housing rows for k = a, b have z_rule, place and keys equal to the c row after `angle[2]` → `angle[k]`, in every spec, with no x1_exempt on the set. B controls: nut_housing_a z offset 1; anchor_a round while anchor_c is square; screw_b with `angle[1]`.
2. **x1_exempt narrowed to fields (`fields: [place]`)**, so z_rule and plan_poly stay compared; `--accept` refuses while any exemption remains (Loftsman R2).
3. Section view section_yz: depth along X from place / plan x; `side` reads u. Per-Axes K3 to K9 (TP-7). K5 admissions:
   - the stepped `section_u` outline on the unsectioned screw_c;
   - balls, line (the bearing-line mark in section form, Topologist) and lever sub-artists.

   Renderer section convention.
4. S3-3 cross-record reader resolving "S1 / S2 <pair>" to the latest accepted record with --stale clean.
5. K5 mark admission for the S1 anchor line (Topologist P0T section 4).

## Items for P6 (S1 r8, S2 r9 drawing and spec edits)

1. S1 and S2 anchor rows to the 42-square place. S2 anchor kind and projection change to prism / rectangle. bracket_anchor r_in becomes `anchor_block_width / 2`. Remove the S3 x1_exempt. Re-plant K5-Z3, K7-Z15, K5-B7 to B11, B13 to B18, B21, B24, K7-B33 and K7-B19, each B re-shown red.
2. S1 screw text "T8" → "Tr12x3". The S2 screw_c shape "d 8" → "d 12". The S1 lead ticks read 3.
3. S1 `reported_items` (8 ids, Designer sign-off section 8) with `checks_s1.reported(ctx)["items"]`. The mass report carries W 24.25 kg, Tr12x3 screws 2.40 kg, NEMA 17 at 0.35 each at the new motor height.
4. **liftmotor.coupling_length 36 moves the S1 and S2 lift motors down 11.00** (S1 motor 181 to 229 z_A). Designer dry run: no S1 or S2 margin moves.
5. The guide-row block radius is renamed to `guide_block_od / 2` in all three specs.
6. The S1 anchor mark line is drawn (spec field present).

## Items for Sean at M2

1. **Drawn screw bar 911.00 mm** (screw end at 254 to the guide-block top at 1165) against DN23's 800 to 900. L 900 is the screw from the block underside, and L_min 885.00 / 885.84 is unchanged. The bar adds the 11 mm end in the coupling (Loftsman NOTE 3; detail 1.3 sends out-of-range values to Sean).
2. **coupling_length 36**: NEMA 17 on 36-long M3 standoffs; motors 11 lower in S1/S2. 12 mm of bare 5 mm shaft below each coupling (z_S 291 to 303) turns beside the collet-change zone. Coupling guard to Step 2.
3. **Nut clamp ring OD 46 / bore 30 / 3**, the upward seat of the floating nut. Designer value to sign, then Sean's pick of the nut mounting.
4. Brass Tr12 nut mass 0.14 against the overlay 0.05 (Loftsman NOTE 4): W rises 2.6 N, every margin falls less than 1 percent. Designer / vendor (B2-1).
5. Carried picks: nut mounting, hold device, sync, anchoring (Design Notes 31).

## P2f2

Last (b) pass, run under the loop cap: the raisers sign from this table and there is no further re-sign round. Sources: `step1.3_designer_spec_resign.md` (FIX A to D, notes; rewritten FIX A) and `step1.3_loftsman_spec_resign.md` (FIX 7, FIX 8, notes). Orchestrator rulings: the revised nut-seat ruling (Designer option (a), shoulder screws) replaces the earlier OD 50 x 2 clamp with M3 ears.

### Corrections to the brief

1. **The ear form was applied first, measured, then reverted.** The first P2f2 ruling (clamp OD 50 x 2, 2 x M3 through ears at ±X) was applied and dry-run before the revised ruling arrived.
   - Clamp results: clamp|home_switch_c 10.44 at park, clamp|guide_c 22.16, lever tip 1114.00, all C pairs 0.00, controls 285/285 at 128.3 s.
   - S2 r8 plan geometry (ears 9 wide, from 20 to 33 off the screw axis tangentially, at all three screws; dimensions ASSUMED for the dry run):
     - The ears stay inside the ring OD (outer corner r 167.78) and 8.37 outside the operator sector edge in plan.
     - They overlap the guide and anchor block footprints in plan, z-separated by 22.16 (park) and 32.84 (capture_end).
     - They would have entered the S2 plan as drawn detail outside the d 50 housing circle. No S2 check value moved.
   - The revised ruling removed the clamp. The overlay clamp leaves and `nut_clamp_bolts` are out, nut_clamp_c is out, and nothing of the ear form remains (MEASURED: 0 occurrences of `nut_clamp` in the overlay and the spec).
2. **nut_c|home_switch_c is undeclared F in the spec, not G 10 as the Designer's table labels it.** The distance equals the Designer's: 14.34 at park (MEASURED). fixed_g10 does not expand on the switch row, and nut_c carries no group. The pair passes under either class.

### Dry run (Designer re-sign section 4, six steps)

All MEASURED, live `docs/sketches/` after the edit.

1. **K2 on s3:** pass. 409 spec keys resolve; 186 overlay leaves; 20 expr leaves agree (`expr_agreement_issues` 0 issues). The three clamp leaves are gone and the eight `ring.nut_screw*` / `ring.nut_axial_play` leaves are in.
2. **check_stack on s3_spec.yaml:** nut_screws_c spans 319.84 to 340.39 z_A at capture_end (969.84 to 990.39 at start, 1094.84 to 1115.39 at load and park). This equals the Designer's 319.84 to 340.39.
3. **Section-piece script:** every declared pair of nut_c, nut_housing_c, nut_screws_c, home_switch_c and ring, all four poses. 250 pair-pose tests, 0 failures (C off 0.00, G under g_min, F overlapping). The pair table (below) equals the Designer's table entry for entry.
4. **Lever tip from the lever field:** 1112.00 z_A (r 182, 3 inboard of the housing rim).
5. **`--stale`:** 2 records, 5 differences, unchanged from P2f (clamp and screw leaves are read by no accepted record).
6. **X1:** pass, 70 compared, 3 skipped, 3 exempt, unchanged.

| Pair (pose) | Declared | Overlap mm² | Distance | Designer table |
|---|---|---|---|---|
| nut_screws_c \| nut_housing_c (capture_end) | C | 0.00 | 0.00 | 0.00 |
| nut_screws_c \| nut_c (capture_end) | F | 0.00 | 0.05 (head play) | 0.05 |
| nut_c \| nut_housing_c (capture_end) | C | 0.00 | 0.00 | 0.00 |
| screw_c \| nut_c; screw_c \| nut_housing_c; screw_c \| nut_screws_c | C; F; F | 0.00 | 0.00; 5.50; 5.00 | same |
| nut_screws_c \| ring (capture_end) | F | 0.00 | 6.08 | 6.08 |
| nut_screws_c \| home_switch_c (park) | G 10 | 0.00 | 41.53 | 41.53 |
| nut_screws_c \| guide_c (park) | G 10 | 0.00 | 19.61 | 19.61 |
| nut_screws_c \| guide_bearing_c; \| bracket_guide_c (park) | G 10 | 0.00 | 30.61; 37.53 | - |
| nut_housing_c \| home_switch_c; \| guide_c (park) | G 10 | 0.00 | 12.23; 24.17 | same |
| nut_c \| home_switch_c (park) | F (undeclared; Correction 2) | 0.00 | 14.34 | 14.34 |
| nut_housing_c \| anchor_c; nut_screws_c \| anchor_c (capture_end) | G 10 | 0.00 | 10.84; 24.84 | same |

Least G margins over the five rows, all poses: nut_housing_c|anchor_c and |bracket_anchor_c 10.84, nut_housing_c|home_switch_c 12.23, nut_housing_c|anchor_bearing_c 17.84, nut_screws_c|guide_c 19.61, ring|bracket_anchor_c 19.84, ring|home_switch_c 20.16 (MEASURED).

### Pairs that moved since P2f

| Pair | P2f | P2f2 |
|---|---|---|
| nut_clamp_c \| nut_c, \| nut_housing_c (C 0.00) | present | removed with the row |
| nut_clamp_c \| home_switch_c (park) | G 10, 10.75 | removed |
| nut_clamp_c \| guide_c (park) | G 10, 21.16 | removed |
| nut_screws_c \| nut_housing_c | - | C 0.00 |
| nut_screws_c \| nut_c | - | F 0.05 |
| nut_screws_c \| home_switch_c / \| guide_c (park) | - | G 10, 41.53 / 19.61 |
| nut_screws_c \| ring; \| anchor_c; \| screw_c | - | F 6.08; G 24.84; F 5.00 |
| Lever tip | 1115.00 | 1112.00 |
| anchor_c \| anchor_bearing_c, anchor_bearing_c \| anchor_locknut_c, nut_housing_c \| nut_c | C 0.00 | C 0.00, now with the cut-case `face` field (Loftsman FIX 8) |

All other pairs from the P2f table are unchanged (MEASURED, same script).

### Items closed

| Item | Closed by |
|---|---|
| Designer FIX A (revised ruling) | nut_clamp_c deleted and **nut_screws_c** added; still 65 rows. Three ISO 7379-type shoulder screws: shoulder d 6, M5 x 8, head D10 x 4.5, PCD 32. One on the inboard radial in the plane (u -144), unsectioned; two at ±60 deg from the outboard radial, off the plane, not_drawn. Flange holes D7 (0.5 float); shoulder length 8.05 (0.05 axial play). nut_c +u flange split at the hole; nut_housing_c +u lower band split at the tapped hole, with material under it. Anti-rotation pin deleted (the screws locate rotation). Nut shape: "floating = radial float only, axially located with 0.05 play". Overlay: `ring.nut_screw`, `nut_screw_pcd` 32, `nut_screw_shoulder_d` 6, `nut_screw_thread_d` 5, `nut_screw_head_d` 10, `nut_screw_head_height` 4.5, `nut_screw_thread_length` 8, `nut_axial_play` 0.05 (ASSUMED). Lever `to` z reads the housing top at park + `lever_free_gap`: 1112.00. not_drawn 9 entries |
| Designer FIX B | Overlay `jackscrew.thread_start_z` 300 and `thread_end_z` 1120. screw_c shape: "cut from d 12 bar", plain collars 288 to 300 and 1120 to 1135. New field `ticks: {from: thread_start_z, to: thread_end_z, pitch: lead}`, so the ticks run over 300 to 1120 only. Keys added |
| Designer FIX C | anchor_c\|coupling_c source "2.0 below (2.06 at the bore corner) at coupling_length 36". liftmotor_pilot_c\|coupling_c source "12.0 above the pilot top at 36". anchor_c shape: block 265 to 288 and a separate bolted cover 288 to 295, hatched at the opposite angle, joint line at 288. Field `hatch_split` on anchor_c. The cover pieces stay in anchor_c.section_u so the row extent keeps the shared z_rule (X1, K6) |
| Designer FIX D | part_list gains "shop floor line (ground hatch)", row floor |
| Loftsman FIX 8 | Chain c: [anchor_bearing_c, screw_c] replaced by [anchor_bearing_c, anchor_locknut_c] (certifier "S3 anchor_locknut_c\|anchor_bearing_c") and [anchor_locknut_c, screw_c] (certifier "S3 anchor_locknut_c\|screw_c", the thread). Cut-case `face` fields: cover underside 288 on anchor_c\|anchor_bearing_c, locknut top 272 on anchor_bearing_c\|anchor_locknut_c, counterbore shoulder on nut_housing_c\|nut_c. The S3-3 rule reads "axial face contact that carries the cut-case load in its direction". anchor_locknut joins the P4 symmetry-lint row set |
| Loftsman FIX 7 | Superseded by Designer FIX A (option (a)) per the revised ruling |
| Designer note 1 (L_min) | L_min reported both ways (DERIVED, check_stack `screw_length` + head 4.55 above the housing top = nut_axial_play + head_height): **without the head 885.00 / 885.84 at anchor_z (1 m: 1135.00 / 1135.84); with it 889.55 / 890.39 (1 m: 1139.55 / 1140.39)**. Drawn L 900 still covers both 0.5 / 0.75 m values. The expression is the Loftsman's to amend; no geometry change |

### Check results

| Run | Result |
|---|---|
| `--controls` (default 12 jobs) | Z clean 75/75, B fired 208/208, smoke 2/2: 285/285 match; wall 125.8 s |
| `--stale` | 2 records, 5 differences (s1 r7: lead, nominal, coupling_length; s2 r5: nominal, coupling_length), unchanged from P2f; X1 pass (70 compared, 3 skipped, 3 exempt) |
| `--stale --include-unaccepted` | 15 records, 32 differences, unchanged from P2f |
| K2 on s3_spec.yaml | pass, 409 spec keys, 186 overlay leaves, 20 expr leaves agree |
| s3 empty-figure run (checks_s3 on no figure; no stub before (c)) | S3-1, S3-2, S3-3 fail, cause absent; reported 9 of 10 (tension_segment needs drawing); S3-2 P_cr 1363.8 N, margins 17.20 / 12.04 / 7.61 / 3.97 unchanged |
| Spec | 65 rows, 9 not_drawn, 0 neighbour ids outside the spec |

### Items for P4 (added)

1. The symmetry premise lint row set gains anchor_locknut (Loftsman FIX 8 (c)). The full set is anchor, anchor_locknut, screw, nut and nut_housing for k = a, b against c.
2. The S3-3 reader reads the `face` field of each S3 certifier (the named horizontal edge carries the contact).
3. K5 admission of the screw_c `ticks` span and of the anchor_c `hatch_split` (cover hatch and joint line), with Z and B.
4. Open: "contact lines" on anchor_bearing_c are admitted under `anchor_bearing_c:balls`, or `contact` is added to its sub_artists (Designer note 3, Topologist).

### Items for P6 (added)

1. The S2 r9 plan draws nothing new for the nut. The shoulder-screw heads (D10 at PCD 32, r up to 21 from the screw axis) lie inside the d 50 housing circle (DERIVED: 16 + 5 = 21 < 25).

### Items for Sean at M2 (P2f2)

1. **Drawn screw bar 911.00** against DN23 800 to 900 (unchanged from P2f).
2. **L_min with the shoulder-screw head:** 889.55 / 890.39 (0.5 and 0.75 m), 1139.55 / 1140.39 (1 m), against 885.00 / 885.84 without it. The drawn 900 covers both.
3. **Floating nut re-ruled as "axially located with 0.05 play".** Design Notes 31 says "axially clamped". This leaves a 0.05 dead band on load reversal (6.0 deg of screw rotation at lead 3). Homing approaches in one direction (Designer Correction 2). Gameplan l.695 line below.
4. **Nut upward seat by three shoulder screws:** d 6, M5, head D10 x 4.5, PCD 32. The anti-rotation pin is removed.
5. **Seat assignment:** the screw heads carry the ring weight in every lifting case; the counterbore shoulder carries the cut case only (Designer note 4). This bears on the nut-mounting pick.
6. Carried from P2f: coupling_length 36 with 12 mm of bare shaft below each coupling; Tr12 nut mass 0.14 against 0.05; picks for nut mounting, hold, sync and anchoring.

## Gameplan lines to change

Final list. It merges P2f, the Designer re-sign and the Loftsman re-sign. P2f items 5 and 6 and Loftsman re-sign item 2 are superseded by items 5 and 6 below.

1. l.188, within the line.
```
Old: couplings (r 150.5 to 169.5, z_S 303.5 to 323.5) 35.5 radially from the hand zone, exposed between the standoffs; the lift is idle at load;
New: couplings (r 150.5 to 169.5, z_S 303 to 323) 35.5 radially from the hand zone, exposed between the 36-long standoffs, with 12 of bare 5 mm motor shaft below each (z_S 291 to 303); the lift is idle at load;
```
2. l.242, append at the end of the line (after "is the old-design reference).").
```
Old: (end of line)
New:  From S1 r8 these are the spec field reported_items in s1_spec.yaml (8 ids, Designer 1.3 (b) sign-off section 8), read by RPT from checks_s1.reported items; the mass report carries W 24.25 kg (s3_spec load_cases.W_kg) and Tr12x3 screws.
```
3. l.272, within the line (supersedes P2 item 1).
```
Old: Shows: bottom anchor with thrust bearing, screw
New: Shows: bottom anchor (fixed: two angular-contact bearings back-to-back in a 42-square block with a bolted cover, outer races between the block shoulder and the cover, inner races between the screw shoulder and an M10x1 locknut; Design Notes 31, Designer 1.3 (b) FIX 3, re-sign FIX C), screw
```
4. l.272, within the line (Designer re-sign item 1).
```
Old: screw (rectangle, `jackscrew.nominal` wide, lead labelled from `jackscrew.lead`; Tr12x3 from STOP S3-A)
New: screw (stepped outline cut from d 12 bar: journal 10 in the anchor and guide bearings, plain d 12 collars at the 288 shoulder and under the guide, Tr12x3 thread over the nut travel 300 to 1120 z_A, lead labelled from `jackscrew.lead`; Tr12x3 from STOP S3-A; Designer 1.3 (b) re-sign FIX B)
```
5. l.272, within the line (Designer re-sign item 2; supersedes P2f item 5 and Loftsman re-sign item 2).
```
Old: brass nut on the ring with its mounting
New: brass flange nut in a counterbored boss on the ring, held up by three shoulder screws through the flange (d 6, M5, PCD 32, 0.5 radial and 0.05 axial play; Designer 1.3 (b) re-sign FIX A, Loftsman 1.3 (b) re-sign FIX 7 (a)), with its mounting
```
6. l.272, within the line.
```
Old: NEMA 17 mount and coupling
New: NEMA 17 on four M3 standoffs 36 long under the anchor block with a beam coupling 19 x 20 centred on the motor shaft tip, screw end 1 above it (Designer 1.3 (b) FIX 2; 1.3 P2f dry run)
```
7. l.288, the S3-3 row (merges P2f item 6 and Loftsman re-sign item 1; supersedes P2 item 7).
```
Old: every consecutive pair class C in the drawn figures (S1 for core, base and frame members; S3 for anchor, screw, nut, ring; S6 for bearing and tube), K7 C |
New: every consecutive pair class C, as an axial face contact that carries the cut-case load in its direction (named face per S3 certifier: anchor locknut top 272, cover underside 288, nut counterbore shoulder; the chain lists the locknut; Loftsman 1.3 (b) re-sign FIX 8) in the section, in the K7 entries of a certifier named per pair in the spec `chains` by sketch and pair id and resolved at run time to the latest accepted S1 and S2 records (a stale record certifies nothing; S3 is accepted after S1 r8 and S2 r9), this figure, or declared (cutter\|core as the load-application pair, row load_cut; bearing and tube for S6-5). Chain per screw: screw c runs base plate, base frame, member c (Design Notes 27); screws a, b run base plate, member a or b; the a, b screw-set pairs are certified from screw c under the symmetry premise lint (anchor, anchor locknut, screw, nut, nut-housing rows; P4; Loftsman 1.3 (b) R1), K7 C |
```
8. l.292, within the line.
```
Old: + max(nut length, ring nut-housing height) + 2 g_min (Loftsman ruling, 1.1 (b);
New: + max(nut length, ring nut-housing height) + 2 g_min, with the drawn bar length beside it (screw-end bottom to guide-block top, 911.00 at 1.3 (b) P2f, coupling_length 36; Loftsman 1.3 (b) NOTE 3) and the value with the nut shoulder-screw head above the housing top (889.55 / 890.39 at 1.3 (b) P2f2; Designer re-sign note 1) (Loftsman ruling, 1.1 (b);
```
9. l.695, within the line (Designer re-sign item 3).
```
Old: floating nut (0.5 radial float, axially clamped, pinned against rotation)
New: floating nut (0.5 radial float, axially located with 0.05 play by three shoulder screws that also stop rotation; Designer 1.3 (b) re-sign FIX A, Loftsman NOTE 3)
```
10. The echo row inserted by P2 item 9 (text begins "| Anchor block **42 square x 30**").
```
Old: | Anchor block **42 square x 30**; bearing lines **280** and **1150** z_A, span L_t **870** |
New: | Anchor block **42 square x 30**; bearing lines **280** and **1150** z_A, span L_t **870**; lift motor face **229** z_A (`liftmotor.coupling_length` 36, shaft gap 1); drawn screw bar **911.00** |
```
