# Step 1.3 (b) Designer re-sign, S3 section A-A through screw c

Read: `step1.3_designer_spec_signoff.md` (mine), `step1.3_engineer_spec_fixes.md`, `step1.3_loftsman_spec_resign.md` (FIX 7, NOTE 3), `docs/sketches/s3_spec.yaml` (whole), `proposed_params.yaml` (ring, jackscrew, liftmotor, liftsync, liftload), `checks_s3.py` l.84, gameplan l.272, l.695. Heights z_A.

Dry runs, all in the scratchpad; nothing under `docs/sketches/` edited.
- `dry_resign.py` evaluates each row's `section_u` pieces (or its place rectangle at theta 270) in (u, z_A) through `check_stack.eval_expr`, then applies `sketch_common.overlap_area` and `min_distance`. On the spec as committed it reproduces the Engineer's table: clamp|switch 10.75, housing|switch 12.23, clamp|guide 21.16, coupling|anchor 2.06, shaft|screw end 1.00, coupling|pilot 12.00, every C pair 0.00 with 0.00 mm² (MEASURED).
- `patch7.py` writes the FIX A spec and overlay (option (a), section 4) into `scratchpad/dry7/`. The same pair evaluation is then run on that copy.

## Corrections to the brief

1. **The clamp joint cannot be built (Loftsman FIX 7, confirmed). My first counter-value also fails.**
   - At OD 46 the clamp covers r 21.5 to 23 of the 3.5 housing wall (r 21.5 to 25).
   - My first draft of this re-sign proposed OD 50 x 2 with M2 bolts at r 23.25. The M2 tap drill (1.6) at r 23.25 leaves 0.95 of wall each side, under the Loftsman's 1 mm rule (DERIVED).
   - A round clamp wide enough for M3 reads 8.69 to the switch (Loftsman).
   - The clamp-and-bolts form is dropped. Ruling: the Loftsman's option (a), shoulder screws through the nut flange (FIX A).
2. **Floating needs axial play (Loftsman NOTE 3, accepted).**
   - With the flange flush under a rigid seat, the nut is gripped axially. Friction at the two flange faces then resists the radial float. Under a clamp load the 0.5 float is locked and stops working.
   - Design Notes 31 says "axially clamped". The intent is "axially located": 0.05 axial play, set by the shoulder-screw length over the flange.
   - The cost is a 0.05 dead band when the load reverses between the cut and lift cases, 6.0 deg of screw rotation at lead 3 (DERIVED). Homing approaches in one direction, so the dead band does not enter the home position. Gameplan l.695 line below.
3. **The 288 shoulder needs plain bar under it.**
   - Tr12x3 root is 8.5 (`jackscrew.root_diameter`), smaller than the journal 10, so a journal 10 cannot be turned from rolled Tr12x3 stock. A thread running to 288 would also make the shoulder a helix crest.
   - The 288 shoulder, and the 1135 step to the guide journal, exist only on a screw cut from d 12 bar, with plain collars and the thread over the nut travel only.
   - The layout at 288 is right: at 272 the bearings would have to pass over the d 12 body. The screw_c text must say how the screw is made (FIX B).
4. **Two neighbour sources still carry the 25-gap numbers.** anchor_c|coupling_c reads "1.5 clear of the block underside" and liftmotor_pilot_c|coupling_c reads "1.5 clear of the pilot top". At 36 they are 2.00 (2.06 at the shoulder-bore corner) and 12.00 (MEASURED). FIX C.
5. **The cover is drawn as part of the block.** The anchor_c shape says "one hatched body with its cover". The bearings go in from the top (shoulder bore 20 < bearing OD 26), so the cover is a separate part, and V7 asks the reader to see it. With one hatch the cover joint at 288 cannot be seen. The wording is mine from FIX 3; FIX C corrects it.

## 1 FIX 1 to 6, closure

| My FIX | Spec / overlay now | Dry run | Result |
|---|---|---|---|
| 1 nut and housing | leaves `nut_body_od` 22, `nut_flange_thickness` 8 with my source text; housing `section_u` four pieces, -u expressions parenthesised (Engineer Correction 3); keys added; counterbore and shoulder seat in the shape text | nut_c\|nut_housing_c C 0.00, 0.00 mm² (was 152.0) | closed; the upward seat is replaced by FIX A |
| 2 coupling stack | `coupling_length` 36, `shaft_gap` 1; coupling_c and screw_end_c z_rules as I wrote them; screw_end_c convention note gone; liftmotor_c 181 to 229; standoffs 36; shaft\|screw end G 1 (Loftsman, stricter than my F) | coupling 243 to 263, screw end 254 to 265, shaft\|end 1.00, coupling\|anchor 2.06, coupling\|pilot 12.00 | closed except two stale sources (FIX C) |
| 3 fixed end | leaves `locknut_od` 18, `locknut_thickness` 6, `anchor_shoulder_bore` 20, `anchor_cover_bore` 16; anchor_c three bands per side; screw_c stepped `section_u`; anchor_locknut_c 266 to 272, cut (Engineer Correction 5 accepted: as an outline it read 60.00 mm² on the journal), in fixed_g10, chain axial; out of not_drawn and the figure note; chain c notes name the faces | block\|bearing, screw\|bearing, locknut\|bearing C 0.00; screw\|block F 2.00 | closed; screw text FIX B, cover text FIX C |
| 4 home switches | lever field on home_switch_c; home_switch_a/_b "no lever drawn in plan" | lever tip 1115.00 over the clamp | rule closed; target returns to the housing rim under FIX A (tip 1112.00) |
| 5 load_comp_c | label and shape "static 79, capture 113, retract (F_bind 300) 179, stall up 343 N", key `liftload.f_bind` | - | closed |
| 6 side, rubric | `side` -1 on frame_upper_c, +1 on pinion_c (axes section); V7, V10 visual-only; V10 text mine; handedness line names four predicates | - | closed |

## 2 New values for my signature

| Value | Ruling | Evidence |
|---|---|---|
| nut_clamp_c OD 46, bore 30, 3 thick | **Refused**, and the row is removed (Correction 1). It is replaced by three shoulder screws through the flange, row nut_screws_c (FIX A). | section 4 |
| Lever tip 1115.00 | **Refused.** It rested on the clamp top. With no clamp the lever targets the housing rim again: tip at the housing top at park + `lever_free_gap` 1.16 = **1112.00**, r 182, 3 inboard of the rim r 185. This is my FIX 4 value. | MEASURED from the lever field on the dry7 copy: (u -190, 1122) to (u -182, 1112.00) |
| coupling_length 36 | **Signed.** 35 is the least that closes (coupling\|anchor 1.12 at the bore corner). 36 gives 2.06 to the block, 9 of screw end engaged and 12 of exposed shaft below each coupling. The Loftsman's 36.5 rests on 10 engaged, which remedy B does not use. Bar 911.00 goes to Sean (Engineer's M2 item 1). Coupling hub lengths stay with Step 2 (Loftsman NOTE 2). | Engineer table, reproduced |
| Screw shoulder 288 on the upper inner race | **Signed with FIX B.** Both axial directions close in drawn parts. Cut case: locknut, inner races, outer races, cover 288. Lifting cases: shoulder 288, inner races, outer races, block shoulder 272. | screw\|bearing C 0.00, locknut\|bearing C 0.00, block\|bearing C 0.00 (MEASURED) |
| `liftload.core_mass_capture` 10.4 | **Signed.** DERIVED from Quinn's SVR, density ASSUMED. checks_s3 l.84 reads the key. Capture lift (24.25 + 10.4) x 9.81 / 3 = 113.31 per screw (DERIVED), unchanged. | spec l.119, l.146 |

## 3 Part list

On the spec as committed: 65 rows, 10 not_drawn entries, 0 named parts missing (MEASURED, spec text). Every part a `shape` string names has a row or a not_drawn entry.
- That is my sign-off list plus the anchor locknut (anchor_locknut_c), the nut clamp ring (nut_clamp_c) and the clamp bolts (not_drawn).
- The retaining ring is gone from the nut and housing text and from not_drawn.
- The `part_list` field (30 entries) covers 64 of the 65 rows. It omits the shop floor line (row floor): FIX D.

After FIX A: still 65 rows (nut_screws_c replaces nut_clamp_c) and 9 not_drawn entries.
- Out: clamp bolts. Out: anti-rotation pin (the shoulder screws locate the nut in rotation).
- In: "two nut shoulder screws off the plane".

## 4 FIX items

**A. Nut upward seat: three shoulder screws through the flange (Loftsman FIX 7 option (a)). Removes nut_clamp_c, adds nut_screws_c.**

Option (b), bolt ears at ±X, keeps the clamp. It also keeps NOTE 3's zero axial play, needs a shim, and adds two housing bosses. Option (a) does more with fewer parts: one feature carries the upward seat, sets the 0.05 axial play, stops rotation within the float (the pin goes), and keeps every fastener head off the switch side.

Values (all ASSUMED; vendor B2-1 for the flange holes):
- 3 x ISO 7379-type shoulder screws, shoulder d 6, thread M5 x 8 into the counterbore floor, head D10 x 4.5, on PCD 32.
- Positions: one on the inboard radial (toward the drill axis, in the section plane at u -144), two at ±60 deg from the outboard radial (off the plane, x ±13.86).
- Nut flange holes D7 = shoulder 6 + 2 x `ring.nut_float`, so the shoulder float equals the body and counterbore float, 0.5.
- Shoulder length = `nut_flange_thickness` + `ring.nut_axial_play` 0.05 (ground shoulder, or a stock 8 shoulder on a 0.05 shim under it).
- Flange ligament outside the hole: 21 - 19.5 = 1.5 (DERIVED).
- Tapped hole walls: r 13.9 to 18.1 about the screw axis, 2.4 to the body bore r 11.5 and 6.9 to the boss OD (DERIVED), inside the Loftsman's 1 mm rule.
- Load: stall up 343.18 N over 3 screws, 114 N each, 8.1 MPa on the M5 stress area 14.2 mm² (DERIVED).

Overlay:
- Remove `ring.nut_clamp_od`, `ring.nut_clamp_id`, `ring.nut_clamp_thickness`.
- Add (ASSUMED, source "Designer 1.3 (b) re-sign FIX A; Loftsman 1.3 (b) re-sign FIX 7 (a), NOTE 3"): `ring.nut_screw` (text "3 x ISO 7379-type shoulder screw d 6, M5, head D10 x 4.5, PCD 32, one on the inboard radial, two at ±60 deg from the outboard radial"), `ring.nut_screw_pcd` 32, `ring.nut_screw_shoulder_d` 6, `ring.nut_screw_thread_d` 5, `ring.nut_screw_head_d` 10, `ring.nut_screw_head_height` 4.5, `ring.nut_screw_thread_length` 8, `ring.nut_axial_play` 0.05.
- `liftsync.lever_free_gap` source: "lever tip above the nut-housing top at park in the free state (Designer 1.3 (b) FIX 4; re-sign FIX A)".

Rows (UC = `jackscrew.pitch_radius * sind(jackscrew.angle[2])`, US = `UC + ring.nut_screw_pcd / 2`, FLB = `nut_z + jackscrew.nut_length / 2 - jackscrew.nut_flange_thickness`, FT = `nut_z + jackscrew.nut_length / 2`):
- **nut_c** `section_u`: replace the +u flange piece by [UC + nominal / 2, US - (shoulder_d / 2 + nut_float), FLB, FT] and [US + (shoulder_d / 2 + nut_float), UC + nut_flange_od / 2, FLB, FT].
  - Shape: "... flange step to nut_flange_od / 2 at the top with three D7 holes on PCD 32 (one cut by the plane, inboard), seated on the counterbore shoulder; shoulder screws (row nut_screws_c) through the holes, 0.5 radial and 0.05 axial play; rotation located by the screws".
  - Delete the anti-rotation-pin phrase.
  - Neighbour nut_clamp_c becomes `{id: nut_screws_c, class: F, source: "shoulder in the flange hole 0.5 radial, head 0.05 above the flange top (axial play, NOTE 3); the lifting cases close the 0.05 against the head"}`.
- **nut_housing_c** `section_u`:
  - Replace the +u lower-band piece by [UC + nut_body_od / 2 + nut_float, US - thread_d / 2, lo, FLB] and [US + thread_d / 2, UC + housing_od / 2, lo, FLB].
  - Add [US - thread_d / 2, US + thread_d / 2, lo, FLB - thread_length] (material under the tapped hole).
  - Shape: replace the clamp sentence by "three M5 tapped holes in the counterbore floor on PCD 32 for the nut shoulder screws (row nut_screws_c)".
  - Neighbour nut_clamp_c becomes `{id: nut_screws_c, class: C, source: "M5 in the floor, shoulder on the counterbore floor"}`.
- **nut_screws_c** (new; replaces nut_clamp_c in the row order):
  - name "nut shoulder screws"; kind screw; axis Z; projection rectangle; section_class unsectioned (ASME Y14.3, fastener on its axis in the plane); hatch none.
  - Keys: the eight ring.nut_screw* and nut_axial_play leaves, jackscrew.nut_length, jackscrew.nut_flange_thickness, jackscrew.pitch_radius, jackscrew.angle.
  - z_rule: z_min FLB - thread_length, z_max FT + nut_axial_play + head_height.
  - place: round, r_in pitch_radius, theta angle[2], half_width pcd / 2 + head_d / 2.
  - `section_u` (three steps of the inboard screw): thread [US ± thread_d / 2, FLB - thread_length, FLB]; shoulder [US ± shoulder_d / 2, FLB, FT + nut_axial_play]; head [US ± head_d / 2, FT + nut_axial_play, FT + nut_axial_play + head_height].
  - Neighbours: nut_housing_c C; nut_c F; screw_c F; ring F; `use: fixed_g10`; `use: s1_5b_base`; home_switch_c G 10; guide_c G 10.
  - sense below guide_c; chain [axial]; moves true; axes [section].
  - Shape: "shoulder screw d 6 x 8.05, M5 into the counterbore floor, head D10 x 4.5 over the nut flange, 0.05 axial play; the one on the inboard radial drawn (unsectioned), two at ±60 deg from the outboard radial off the plane (not_drawn); the nut's upward seat in every lifting case (Designer 1.3 (b) re-sign FIX A)".
- **home_switch_c**: lever `to` z = `park_tip + ring.position_above_tip + ring.thickness / 2 + ring.nut_housing_height / 2 + liftsync.lever_free_gap`. Drop `ring.nut_clamp_thickness` from the keys. Shape "1115.00 z_A" becomes "1112.00 z_A, over the housing rim". The neighbour nut_clamp_c becomes nut_screws_c G 10.
- **screw_c**: the neighbour nut_clamp_c becomes nut_screws_c F.
- **chains c**, pair [nut_c, nut_housing_c]: note "cut case: flange on the counterbore shoulder; lifting cases through nut_screws_c (head on the flange top)".
- **not_drawn**:
  - Remove "anti-rotation pin" and "clamp bolts".
  - Add `{part: "two nut shoulder screws", reason: "at ±60 deg from the outboard radial, x ±13.86, off the plane; leaf ring.nut_screw; the inboard screw is row nut_screws_c"}`.
  - Figure note to match.
- **part_list**: "nut clamp ring" becomes `{part: "nut shoulder screw (inboard)", row: nut_screws_c}`. The not_drawn line reads "front standoffs, two nut shoulder screws, off-plane sets".
- **rubric V7**: "a floating nut in a counterbored, clamped boss" becomes "a floating nut in a counterbored boss held by shoulder screws with axial play".

Dry run on the `dry7` copy (MEASURED, `patch7.py` then the pair evaluation):

| Pair (pose) | Declared | Overlap mm² | Distance |
|---|---|---|---|
| nut_screws_c \| nut_housing_c (capture_end) | C | 0.00 | 0.00 |
| nut_screws_c \| nut_c (capture_end) | F | 0.00 | 0.05 (head play) |
| nut_c \| nut_housing_c (capture_end) | C | 0.00 | 0.00 |
| screw_c \| nut_c; screw_c \| nut_housing_c; screw_c \| nut_screws_c | C; F; F | 0.00 | 0.00; 5.50; 5.00 |
| nut_screws_c \| ring (capture_end) | F | 0.00 | 6.08 |
| nut_screws_c \| home_switch_c (park) | G 10 | 0.00 | 41.53 |
| nut_screws_c \| guide_c (park) | G 10 | 0.00 | 19.61 (head top 1115.39) |
| nut_housing_c \| home_switch_c; \| guide_c (park) | G 10 | 0.00 | 12.23; 24.17 (unchanged) |
| nut_c \| home_switch_c (park) | G 10 (fixed_g10 on the switch side) | 0.00 | 14.34 |
| nut_housing_c \| anchor_c; nut_screws_c \| anchor_c (capture_end) | G 10 | 0.00 | 10.84; 24.84 |

- Off-plane heads (DERIVED, plan): radial reach 16 cos 60 + 5 = 13 from the screw axis (drill r 173), tangential 13.86 - 5 = 8.86 from the plane. The switch (r 190 to 210, tangential ±3) and the lever (in the plane, r 182 to 190) are clear by 17 radial and 8.86 tangential.
- Dry run the Engineer runs after applying FIX A:
  1. K2 key resolution and `expr_agreement_issues` on s3 (the three clamp leaves gone, eight new leaves).
  2. `check_stack.py s3_spec.yaml`: nut_screws_c 319.84 to 340.39 at capture_end.
  3. The P2f section-piece script over every declared pair of nut_c, nut_housing_c, nut_screws_c, home_switch_c and ring in all four poses, against the table above.
  4. The lever tip read from the field: 1112.00.
  5. `--stale`: the clamp leaves are read by no accepted record, so the result is expected unchanged.
  6. X1 unchanged (nut rows are not shared).

**B. screw_c (shape, keys), overlay.**
- New leaves `jackscrew.thread_start_z` 300 and `jackscrew.thread_end_z` 1120 (ASSUMED). Source: "Tr12x3 thread over the nut travel only: nut bottom 305.84 at capture_end, nut top 1112.84 at the homing trip 2 above park; plain d 12 collars below and above, the screw cut from d 12 bar (root 8.5 < journal 10); Designer 1.3 (b) re-sign FIX B; vendor B2-1".
- screw_c shape: "Tr12x3 lead screw cut from d 12 bar, unsectioned outline in three steps (section_u): M10x1 thread and journal 10 from the block underside through the locknut and both anchor bearings (265 to 288); plain d 12 collar from the shoulder on the upper inner race (288) to the thread start (300); Tr12x3 thread 300 to 1120, thread ticks at the lead 3 over that span only; plain d 12 collar 1120 to the guide-block bottom (1135); journal 10 through the guide bearing to the block top (1165, no axial contact); ...(rest unchanged)". Both leaves go into its keys.
- Dry run (DERIVED, arithmetic; no K rule reads tick extents): the thread covers the nut by 5.84 at capture_end and by 7.16 at the homing trip. The collar 288 to 300 passes the cover bore 16 at F 2.00 (MEASURED, screw|anchor).

**C. Text only (anchor_c, liftmotor_pilot_c).**
- anchor_c neighbour coupling_c source: "2.0 below the block underside (2.06 at the shoulder-bore corner) at liftmotor.coupling_length 36 (Designer 1.3 (b) FIX 2; g_min 1 Designer 1.3 (a) section 9, ASSUMED)".
- liftmotor_pilot_c neighbour coupling_c source: "12.0 above the pilot top at liftmotor.coupling_length 36 (Designer 1.3 (b) FIX 2)".
- anchor_c shape: "one hatched body with its cover" becomes "block 265 to 288 and bolted cover 288 to 295 (bearings enter from the top), the cover hatched at the opposite angle with its joint line drawn at 288". The `section_u` cover pieces (288 to 295) stand; the renderer draws them with the reversed hatch.

**D. part_list.** Add `{part: "shop floor line (ground hatch)", row: floor}`.

## 5 Notes

1. **L_min leaves out the head.** The moving stack top is now the shoulder-screw head, 4.55 above the housing top, while `screw_length.L_min` and `at anchor_z` read `max(nut_length, nut_housing_height)`. The drawn margin nut_screws_c|guide_c 19.61 at park against G 10 holds (MEASURED). To the Loftsman for the reported expression; no geometry change.
2. **Shoulder land.** The d 12 collar bears on the upper inner race over r 5 to 6. Check the vendor's abutment diameter for the 7000-class bearing at B2-1. If d 12 is under it, the remedy is a spacer ring on the journal between the race and the collar, inside the cover bore 16.
3. **Contact lines.** The anchor_bearing_c shape names "contact lines converging outward", and no sub-artist is listed for them. Either admit them under `anchor_bearing_c:balls` in the P4 K5 admission (Topologist), or add `contact` to `sub_artists` there.
4. **Seat assignment.** The upward seat (now the shoulder-screw heads) carries the ring weight in every lifting case. The counterbore shoulder carries only the cut case (254.04 per screw). A nut flipped flange-down onto a bottom shoulder would put the all-day load on solid metal. Recorded for Sean's nut-mounting pick at M2; no change asked here.

Verdict: **FIX** (4 items):
- A: nut upward seat by three shoulder screws (Loftsman FIX 7 (a)); nut_clamp_c removed, nut_screws_c added; lever tip 1112.00; 0.05 axial play (NOTE 3).
- B: screw_c thread span and bar stock.
- C: two stale neighbour sources and the cover text.
- D: part_list floor.

Signed: FIX 1 to 6 closures, coupling_length 36, shoulder 288 (with B), core mass leaf 10.4. Refused: nut_clamp_c 46 / 30 / 3 and lever tip 1115.00. Part list as committed: 65 rows / 10 not_drawn / 0 missing; after A: 65 / 9 / 0.

## Gameplan lines to change

1. l.272, within the line.
```
Old: screw (rectangle, `jackscrew.nominal` wide, lead labelled from `jackscrew.lead`; Tr12x3 from STOP S3-A)
New: screw (stepped outline cut from d 12 bar: journal 10 in the anchor and guide bearings, plain d 12 collars at the 288 shoulder and under the guide, Tr12x3 thread over the nut travel 300 to 1120 z_A, lead labelled from `jackscrew.lead`; Tr12x3 from STOP S3-A; Designer 1.3 (b) re-sign FIX B)
```
2. l.272, supersedes Engineer fix-pass item 5 and Loftsman re-sign gameplan item 2.
```
Old: brass nut on the ring with its mounting
New: brass flange nut in a counterbored boss on the ring, held up by three shoulder screws through the flange (d 6, M5, PCD 32, 0.5 radial and 0.05 axial play; Designer 1.3 (b) re-sign FIX A, Loftsman 1.3 (b) re-sign FIX 7 (a)), with its mounting
```
3. l.695, within the line.
```
Old: floating nut (0.5 radial float, axially clamped, pinned against rotation)
New: floating nut (0.5 radial float, axially located with 0.05 play by three shoulder screws that also stop rotation; Designer 1.3 (b) re-sign FIX A, Loftsman NOTE 3)
```
