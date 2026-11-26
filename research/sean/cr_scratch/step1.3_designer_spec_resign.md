# Step 1.3 (b) Designer re-sign, S3 section A-A through screw c

Read: `step1.3_designer_spec_signoff.md` (mine), `step1.3_engineer_spec_fixes.md`, `docs/sketches/s3_spec.yaml` (whole), `proposed_params.yaml` (ring, jackscrew, liftmotor, liftsync, liftload), `checks_s3.py` l.84, gameplan l.272. Heights z_A.

Dry run: scratchpad copy of `docs/sketches/` with `params.yaml` beside it; nothing under `docs/sketches/` edited. Script `dry_resign.py` (scratchpad) evaluates each row's `section_u` pieces (or its place rectangle at theta 270) in (u, z_A) through `check_stack.eval_expr` and applies `sketch_common.overlap_area` and `min_distance`; overlay values overridden in memory. On the spec as committed it reproduces the Engineer's table (clamp|switch 10.75, housing|switch 12.23, clamp|guide 21.16, coupling|anchor 2.06, shaft|screw end 1.00, coupling|pilot 12.00, every C pair 0.00 with 0.00 mm²; MEASURED).

## Corrections to the brief

1. **OD 46 leaves the clamp no bolt land.** The housing wall at the top is r 21.5 to 25 (counterbore D43 in a D50 boss, 3.5 wall; DERIVED). A clamp OD 46 covers r 21.5 to 23 of it, 1.5 wide. A bolt circle in that wall (r 23.25, wall centre) lies outside the clamp. The clamp is the seat for every lifting case (static 79.30 to stall up 343.18 N per screw, through the bolts in tension), so its bolts are load path, not decoration. OD 46 is a dimensionally clean, unbuildable placeholder. Refused; FIX A gives OD 50 x 2 with a dry run.
2. **The 288 shoulder needs plain bar under it.** Tr12x3 root is 8.5 (`jackscrew.root_diameter`), smaller than the journal 10. A journal 10 cannot be turned from rolled Tr12x3 stock, and a thread running to 288 makes the shoulder a helix crest. The 288 shoulder (and the 1135 step to the guide journal) exists only on a screw cut from d 12 bar with plain collars and the thread over the nut travel. The layout at 288 is right (272 cannot be built: bearings would have to pass over the d 12 body); the screw_c text must say how it is made (FIX B).
3. **Two neighbour sources still carry the 25-gap numbers.** anchor_c|coupling_c reads "1.5 clear of the block underside"; liftmotor_pilot_c|coupling_c reads "1.5 clear of the pilot top". At 36 they are 2.00 (2.06 at the shoulder-bore corner) and 12.00 (MEASURED). FIX C.
4. **The cover is drawn as part of the block.** anchor_c shape: "one hatched body with its cover". The bearings go in from the top (shoulder bore 20 < bearing OD 26), so the cover is a separate part, and V7 asks the reader to see a cover. With one hatch the cover joint at 288 is invisible. My FIX 3 wording; corrected in FIX C.

## 1 FIX 1 to 6, closure

| My FIX | Spec / overlay now | Dry run | Result |
|---|---|---|---|
| 1 nut and housing | leaves `nut_body_od` 22, `nut_flange_thickness` 8 with my source text; housing `section_u` four pieces, -u expressions parenthesised (Engineer Correction 3); keys added; shape text names the counterbore, the shoulder seat and the clamp | nut_c\|nut_housing_c C 0.00, 0.00 mm² (was 152.0) | closed |
| 2 coupling stack | `coupling_length` 36, `shaft_gap` 1; coupling_c and screw_end_c z_rules as I wrote them; screw_end_c convention note gone; liftmotor_c shape 181 to 229; standoffs 36; shaft\|screw end declared G 1 (Loftsman, stricter than my F) | coupling 243 to 263, screw end 254 to 265, shaft\|end 1.00, coupling\|anchor 2.06, coupling\|pilot 12.00 | closed except two stale sources (FIX C) |
| 3 fixed end | leaves `locknut_od` 18, `locknut_thickness` 6, `anchor_shoulder_bore` 20, `anchor_cover_bore` 16; anchor_c three bands per side; screw_c stepped `section_u`; anchor_locknut_c 266 to 272, cut (Engineer Correction 5 accepted: as an outline it read 60.00 mm² on the journal), in fixed_g10, chain axial; removed from not_drawn and the figure note; chain c notes name the faces | block\|bearing, screw\|bearing, locknut\|bearing C 0.00; screw\|block F 2.00 | closed; screw text FIX B, cover text FIX C |
| 4 home switches | lever field on home_switch_c (body corner (u -190, 1122) to (u -182, clamp top at park + 1.16)); home_switch_a/_b "no lever drawn in plan" | lever tip 1115.00 at OD 46 x 3 | rule closed; value moves with FIX A |
| 5 load_comp_c | label and shape "static 79, capture 113, retract (F_bind 300) 179, stall up 343 N", key `liftload.f_bind` | - | closed |
| 6 side, rubric | `side` -1 on frame_upper_c, +1 on pinion_c (axes section); V7, V10 visual-only; V10 text mine; handedness line names four predicates | - | closed |

## 2 New values for my signature

| Value | Ruling | Evidence |
|---|---|---|
| nut_clamp_c OD 46, bore 30, 3 thick | **Refused** (Correction 1). New: OD 50, bore 30, 2 thick, steel, 4 x M2 low-head on bolt circle D46.5 at 45 deg to the outboard radial (ASSUMED). | Dry run at OD 50 x 2 (MEASURED): park clamp\|home_switch_c 10.44 (G 10 passes at 9.95); clamp\|guide_c 22.16; housing\|switch 12.23 and housing\|guide 24.17 unchanged; capture_end nut\|clamp C 0.00, clamp\|housing C 0.00, screw\|clamp F 9.00. Limits (MEASURED): OD 50 x 3 reads 9.57, OD 50 x 2.5 reads 10.00, so 2 is the largest round thickness with margin. Bolt heads (D3.8 ASSUMED) at 45 deg reach 18.34 from the screw axis radially, 11.66 inside the switch face (r_in 30 from the screw axis): no head under the switch (DERIVED). Plate bending, crude strip at 343.18 N, arm 5.25 from the flange mean radius 18 to the bolt circle: 24 MPa, 72 at SF 3, steel (DERIVED). M2 bolt tension 86 N each, 41 MPa on 2.07 mm² (DERIVED). |
| Lever tip 1115.00 | Rule signed (tip = clamp top at park + `lever_free_gap` 1.16, r 182). Value under FIX A: **1114.00** (MEASURED from the lever field). Tip r 182 sits 3 inboard of the clamp rim r 185 at OD 50; at OD 46 it sat 1 inboard of r 183, a roller lever on the edge of its target. | dry run |
| coupling_length 36 | **Signed.** 35 is the least that closes (coupling\|anchor 1.12 at the bore corner); 36 gives 2.06, the screw end 9 engaged, 12 of exposed shaft below each coupling. The Loftsman's 36.5 rests on 10 engagement, which remedy B does not use. Bar 911.00 to Sean (M2 item 1, Engineer). | Engineer table, reproduced |
| Screw shoulder 288 on the upper inner race | **Signed with FIX B.** Both axial directions close in drawn parts: cut case locknut, inner races, outer races, cover 288; lifting cases shoulder 288, inner races, outer races, block shoulder 272. | screw\|bearing C 0.00, locknut\|bearing C 0.00, block\|bearing C 0.00 (MEASURED) |
| `liftload.core_mass_capture` 10.4 | **Signed.** DERIVED, Quinn SVR, density ASSUMED; checks_s3 l.84 reads the key; capture lift (24.25 + 10.4) x 9.81 / 3 = 113.31 per screw (DERIVED), unchanged. | spec l.119, l.146 |

## 3 Part list

65 rows, 10 not_drawn entries, 0 named parts missing (MEASURED, spec text). Every part a `shape` string names has a row or a not_drawn entry: my sign-off list plus anchor locknut (anchor_locknut_c), nut clamp ring (nut_clamp_c), clamp bolts (not_drawn); retaining ring gone from the nut and housing text and from not_drawn. The `part_list` field (30 entries) covers 64 of the 65 rows; it omits the shop floor line (row floor), FIX D.

## 4 FIX items

**A. nut_clamp_c, home_switch_c, overlay `ring.nut_clamp_*`, not_drawn.**
- Overlay: `ring.nut_clamp_od` 46 to 50, source "nut clamp ring over the flange, OD = ring.nut_housing_od so the four bolts land in the 3.5 housing wall (bolt circle D46.5); Designer 1.3 (b) re-sign FIX A"; `ring.nut_clamp_thickness` 3 to 2, source "largest round thickness keeping clamp|home_switch_c G 10 at park with OD 50 (10.44; 3 reads 9.57); Designer 1.3 (b) re-sign FIX A"; `ring.nut_clamp_id` 30, source "...; Designer signed". New leaf `ring.nut_clamp_bolts` {value: "4 x M2 low-head on D46.5, at 45 deg to the outboard radial", status: ASSUMED, source: "Designer 1.3 (b) re-sign FIX A: no bolt head under the home switch"}.
- nut_clamp_c shape: "nut clamp ring OD 50, bore 30, 2 thick on the housing top over the nut flange, 4 x M2 into the housing wall at 45 deg to the radial (not drawn, off the plane); seat of the nut for every lifting case; hatched steel (Designer 1.3 (b) re-sign FIX A)". Add `ring.nut_clamp_bolts` to its keys.
- nut_clamp_c|home_switch_c source (both rows): "g_min seed l.148; clamp top at park 1112.84 to switch bottom 1122, 5 radially (r 185 to 190): 10.44 in plane (Designer re-sign dry run)". nut_clamp_c|guide_c source: "21.16" to "22.16" (top 1112.84).
- nut_housing_c|nut_clamp_c source: "clamp ring bolted on the housing top over the full wall r 21.5 to 25".
- home_switch_c shape: "1115.00 z_A" to "1114.00 z_A".
- not_drawn clamp bolts reason: "4 x M2 at 45 deg to the radial, off the plane; leaf ring.nut_clamp_bolts; named in the nut_clamp_c shape".
- Dry run: section 2 row 1 (MEASURED).

**B. screw_c (shape, keys), overlay.** New leaves `jackscrew.thread_start_z` 300 and `jackscrew.thread_end_z` 1120 (ASSUMED, source "Tr12x3 thread over the nut travel only: nut bottom 305.84 at capture_end, nut top 1112.84 at the homing trip 2 above park; plain d 12 collars below and above, the screw cut from d 12 bar (root 8.5 < journal 10); Designer 1.3 (b) re-sign FIX B; vendor B2-1"). screw_c shape: "Tr12x3 lead screw cut from d 12 bar, unsectioned outline in three steps (section_u): M10x1 thread and journal 10 from the block underside through the locknut and both anchor bearings (265 to 288); plain d 12 collar from the shoulder on the upper inner race (288) to the thread start (300); Tr12x3 thread 300 to 1120, thread ticks at the lead 3 over that span only; plain d 12 collar 1120 to the guide-block bottom (1135); journal 10 through the guide bearing to the block top (1165, no axial contact); ...(rest unchanged)". Keys gain both leaves. Dry run (DERIVED, arithmetic; no K rule reads tick extents): thread covers the nut at capture_end by 5.84 and at the homing trip by 7.16; collar 288 to 300 passes the cover bore 16 at F 2.00 (MEASURED, screw|anchor).

**C. Text only (anchor_c, liftmotor_pilot_c).**
- anchor_c neighbour coupling_c source: "2.0 below the block underside (2.06 at the shoulder-bore corner) at liftmotor.coupling_length 36 (Designer 1.3 (b) FIX 2; g_min 1 Designer 1.3 (a) section 9, ASSUMED)".
- liftmotor_pilot_c neighbour coupling_c source: "12.0 above the pilot top at liftmotor.coupling_length 36 (Designer 1.3 (b) FIX 2)".
- anchor_c shape, replace "one hatched body with its cover" by "block 265 to 288 and bolted cover 288 to 295 (bearings enter from the top), the cover hatched at the opposite angle with its joint line drawn at 288". The `section_u` cover pieces (288 to 295) stay as they are; the renderer draws them with the reversed hatch.

**D. part_list.** Add `{part: "shop floor line (ground hatch)", row: floor}`.

## 5 Notes

1. **L_min omits the clamp.** The moving stack top is now housing top + clamp (2 above `nut_z + nut_housing_height / 2`); `screw_length.L_min` and `at anchor_z` still read `max(nut_length, nut_housing_height)`. Drawn margin at park clamp|guide 22.16 against G 10 holds (MEASURED). To the Loftsman for the reported expression; no geometry change.
2. **Shoulder land.** The d 12 collar bears on the upper inner race over r 5 to 6. Check the vendor's abutment diameter for the 7000-class bearing at B2-1; if d 12 is under it, a spacer ring on the journal between the race and the collar (inside the cover bore 16) is the remedy.
3. **Contact lines.** anchor_bearing_c shape names "contact lines converging outward"; no sub-artist is listed for them. Admit them under `anchor_bearing_c:balls` in the P4 K5 admission (Topologist), or add `contact` to `sub_artists` there.
4. **Seat assignment.** The clamp carries the ring weight in every lifting case; the counterbore shoulder carries only the cut case (254.04 per screw). A nut flipped flange-down on a bottom shoulder would put the all-day load on solid metal. Recorded for Sean's nut-mounting pick at M2; no change asked here.

Verdict: **FIX** (4 items: A nut_clamp_c values refused, OD 50 x 2 with bolts; B screw_c thread span and bar stock; C two stale neighbour sources and the cover text; D part_list floor). Signed: FIX 1 to 6 closures, coupling_length 36, shoulder 288 (with B), lever rule (tip 1114.00 under A), core mass leaf 10.4. Part list 65 rows / 10 not_drawn / 0 missing.

## Gameplan lines to change

1. l.272, within the line.
```
Old: screw (rectangle, `jackscrew.nominal` wide, lead labelled from `jackscrew.lead`; Tr12x3 from STOP S3-A)
New: screw (stepped outline cut from d 12 bar: journal 10 in the anchor and guide bearings, plain d 12 collars at the 288 shoulder and under the guide, Tr12x3 thread over the nut travel 300 to 1120 z_A, lead labelled from `jackscrew.lead`; Tr12x3 from STOP S3-A; Designer 1.3 (b) re-sign FIX B)
```
2. l.272, supersedes Engineer fix-pass gameplan item 5.
```
Old: brass nut on the ring with its mounting
New: brass flange nut in a counterbored boss under a clamp ring (OD 50 x 2, 4 x M2 at 45 deg to the radial; Designer 1.3 (b) re-sign FIX A) on the ring, with its mounting
```
