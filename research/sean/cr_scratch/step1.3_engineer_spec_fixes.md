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

## Gameplan lines to change

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
3. l.272, replacing the P2 item 1 new text.
```
Old: Shows: bottom anchor with thrust bearing, screw
New: Shows: bottom anchor (fixed: two angular-contact bearings back-to-back in a 42-square block, outer races between a bore shoulder and a cover, inner races between the screw shoulder and an M10x1 locknut; Design Notes 31, Designer 1.3 (b) FIX 3), screw
```
4. l.272, within the line (replacing P2 item 2 new text where it reads the NEMA 17 mount).
```
Old: NEMA 17 mount and coupling
New: NEMA 17 on four M3 standoffs 36 long under the anchor block with a beam coupling 19 x 20 centred on the motor shaft tip, screw end 1 above it (Designer 1.3 (b) FIX 2; 1.3 P2f dry run)
```
5. l.272, within the line.
```
Old: brass nut on the ring with its mounting
New: brass flange nut in a counterbored boss under a clamp ring on the ring, with its mounting
```
6. l.288, the S3-3 row, supersedes P2 item 7 and the Loftsman sign-off item 1.
```
Old: every consecutive pair class C in the drawn figures (S1 for core, base and frame members; S3 for anchor, screw, nut, ring; S6 for bearing and tube), K7 C |
New: every consecutive pair class C, as an axial face contact in the section, in the K7 entries of a certifier named per pair in the spec `chains` by sketch and pair id and resolved at run time to the latest accepted S1 and S2 records (a stale record certifies nothing; S3 is accepted after S1 r8 and S2 r9), this figure, or declared (cutter\|core as the load-application pair, row load_cut; bearing and tube for S6-5). Chain per screw: screw c runs base plate, base frame, member c (Design Notes 27); screws a, b run base plate, member a or b; the a, b screw-set pairs are certified from screw c under the symmetry premise lint (P4; Loftsman 1.3 (b) R1), K7 C |
```
7. l.292, within the line.
```
Old: + max(nut length, ring nut-housing height) + 2 g_min (Loftsman ruling, 1.1 (b);
New: + max(nut length, ring nut-housing height) + 2 g_min, with the drawn bar length beside it (screw-end bottom to guide-block top, 911.00 at 1.3 (b) P2f, coupling_length 36; Loftsman 1.3 (b) NOTE 3) (Loftsman ruling, 1.1 (b);
```
8. Insert after the line inserted by P2 item 9 (text begins "| Anchor block **42 square x 30**"), replacing that line's text.
```
Old: | Anchor block **42 square x 30**; bearing lines **280** and **1150** z_A, span L_t **870** |
New: | Anchor block **42 square x 30**; bearing lines **280** and **1150** z_A, span L_t **870**; lift motor face **229** z_A (`liftmotor.coupling_length` 36, shaft gap 1); drawn screw bar **911.00** |
```
