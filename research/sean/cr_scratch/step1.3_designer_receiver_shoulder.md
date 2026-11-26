# Step 1.3 receiver shoulder values and spec edits (Design Notes 32), The Designer

Date 2026-11-26. Read: gameplan Design Notes 32, detail 1.3 (S3-3 row l.288), Design Notes 25 S4-a (l.651); `step1.3_loftsman_redfirst_signoff.md` (F1, section 6); `step1.3_engineer_redfirst_fixes.md` (P6 items); `build_parts/receiver.py`, `tray.py`; `params.yaml` receiver, base, tray, icd leaves; `ASSEMBLY.md` Load path; `docs/sketches/` s1, s2, s3 specs, `proposed_params.yaml`, `s1_side_poses.py`, `fixtures/s3_fixtures.py`, `checks_s3.py` (`_face_issue`, `_face_of`), `check_sketch.py` (`x1_lint`). Section screw c (theta 270, YZ plane).

Dry run on a copy of `docs/sketches/` at `D:\Unleashed Robotics\_scratch\cutjig\designer_receiver\sk\`, with `params.yaml` copied beside it and TMP, TEMP and MPLCONFIGDIR set to `...\designer_receiver\tmp\`. A second, unedited copy at `...\designer_receiver\sk0\` gives the before values. Probes are in `...\designer_receiver\probes\`:
- `edit_specs.py`, `edit_s2.py`: the edits of section 2, applied to the copy.
- `s1_shoulder.py`: distances from the shoulder piece in the four S1 poses.
- `s3_dry.py`: S3 checks in the post-P6 state with fresh records, plus B plants.
- `k7diff.py`: K7 differences between the two copies.

Nothing under `docs/sketches/` was edited. Nothing was written on C:.

Tags: MEASURED (read from a run here), DERIVED (hand arithmetic), DECLARED (spec, params or ruling). Values I set are ASSUMED.

## Corrections to the brief

1. **K7 holds one class per pair, so receiver|base_plate cannot be both "C on the shoulder face" and "G 0.10 radial" as two neighbour classes.**
   - The pair is declared C, and the seat face is named on the entry (`face`), so S3-3 tests the shoulder underside against the plate top.
   - The radial spigot fit (r 80 in r 80.2, 0.20 against 0.10) is stated in the source text of the C entry.
   - It becomes a drawn radial gap at S4-a, where the hole break is drawn. Section 6 gives the S4-a text.
2. **The shoulder meets a kept part that no sketch draws: the debris tray.**
   - The tray stands on the plate top with its spigot hole at `tray.hole_r` 81.2 (params, Quinn).
   - Its floor is solid from the plate top up to 5.83 (at x = -91) and 12.18 (at x = +91) above the plate (DERIVED from `tray.py` fall_height: 3 + |x + 172| tan 2°).
   - Any shoulder wide enough to seat, meaning wider than the 1.0 annulus between r 80.2 and 81.2, intrudes into the tray floor.
   - `tray.hole_r` must grow with the shoulder. This is a params.yaml leaf on a kept part, so it goes to Quinn with B2-10. No dry run sees it.
3. **The receiver has no upward retention in any lifting case. The shoulder as ruled closes only the cut case.**
   - The spigot is a slip fit, and no fastener holds the receiver to the plate.
   - In retract with bind (F_bind 300 N) and in stall up (up to 3 x 343.18 = 1029.5 N, DERIVED), a core bound in the kerf pulls collet and receiver upward off the plate.
   - S3-3 covers the cut case only, so it does not see this. It goes to Sean in section 5.
4. **`ASSEMBLY.md` Load path says the receiver underside force on the base plate is 0.**
   - Under the powered lift the shoulder face carries the cut load, 1000 N, and the stall-down crash load, 1267 N (Design Notes 16 and 31; B2-7).
   - That text belongs to Quinn's file and goes to him with B2-10.

## 1 Values

| Leaf (overlay `receiver:`) | Value | Status | Basis |
|---|---|---|---|
| `receiver.shoulder_od` | 180 | ASSUMED | Seat annulus r 80.2 to 90, 9.80 wide, 9.60 with the spigot at its 0.20 float (DERIVED). After a 0.5 hole-edge chamfer and a 0.5 root relief, 8.6 remain. The seat lies over the plate-support inner edge (x 82, `frame.support_x` 112 - 30). |
| `receiver.shoulder_thickness` | 8 | ASSUMED | Shoulder top at z_A 20. That is below the receiver floor (40) and below the keep-out band, whose z_min is `receiver_floor` 40. |
| `receiver.shoulder_z` | 12, expr `base.plate_thickness` | DERIVED | The seat face is the plate top. |

**Body above the shoulder: unchanged.** The receiver keeps r 80 from the shoulder top (20) to the thread shoulder (76.5), then the thread run as built.
- The spigot below the plate top (z_A 0 to 12, r 80) is unchanged.
- `build_parts/receiver.py` profile, receiver frame (floor 0, z = z_A - 40): after (r_sp, z_bot) insert (r_sp, -28), (r_sh, -28), (r_sh, -20), (r_sp, -20), then continue to (r_sp, z_sh). Here r_sh = 90. This is a kept-part change and needs Quinn's answer to B2-10.

**Loads at the seat face (DERIVED).** Every value is far under `materials.tensile_design` 45 MPa (params, ASSUMED). The size is set by the fit, not by stress.

| Quantity | At 1000 N (cut) | At 1267 N (stall-down crash, B2-7) |
|---|---|---|
| Bearing, area π (90² - 80.2²) = 5240.0 mm² | 0.19 MPa | 0.24 MPa |
| Root shear, 2π · 80 · 8 = 4021 mm² | 0.25 MPa | 0.32 MPa |
| Flange bending, line load at r 85.1, arm 5.1, Z = t²/6 | 0.89 MPa | 1.13 MPa |

**Tray (Quinn, B2-10).** `tray.hole_r` goes from 81.2 to 91.0: shoulder r 90 plus the same 1.0 radial clearance the tray has today (DERIVED).
- The nearest other tray feature is the drain spot face, r 20 at x -172. Its nearest point is at r 152, 61 outside the new hole (DERIVED).
- The plate drain hole (r 13 at x -172) has its nearest point at r 159, 69 outside the shoulder (DERIVED).

## 2 Spec edits

All edits are applied in the copy and dry-run in section 3.

**Overlay `proposed_params.yaml`, new group `receiver:`.** It merges with params.yaml at leaf level and shadows nothing (K2 MEASURED: 189 overlay leaves, no shadow, 21 expr leaves agree).
```yaml
receiver:
  shoulder_od: {value: 180, unit: mm, source: "receiver shoulder resting on the plate top around base.spigot_hole_dia 160.4: seat annulus r 80.2 to 90 (9.8 wide, 9.6 at the 0.2 spigot float), over the plate-support inner edge x 82; bearing 0.24 MPa at 1267 N (Design Notes 32; Designer 1.3 receiver shoulder)", status: ASSUMED}
  shoulder_thickness: {value: 8, unit: mm, source: "shoulder flange thickness: top z_A 20, below the receiver floor 40 and the keep-out band (z_min 40); bending 1.1 MPa at 1267 N (Design Notes 32; Designer 1.3 receiver shoulder)", status: ASSUMED}
  shoulder_z: {value: 12, expr: "base.plate_thickness", unit: mm, source: "seat face z_A: shoulder underside on the plate top (Design Notes 32)", status: DERIVED}
```

**S1 (`s1_spec.yaml` receiver row; base_plate neighbour).**
- `shape`: "receiver cup in section: walls to the rim, floor at icd.floor_above_datum_a with the debris-hole gap, shoulder D180 x 8 on the plate top (seat face), spigot into the plate below it (not drawn: S1 draws the plate without its hole), thread ticks on the outer wall".
- `keys`: add `receiver.shoulder_od`, `receiver.shoulder_thickness`, `receiver.shoulder_z`.
- `section`: add the piece `["receiver.spigot_od / 2", "receiver.shoulder_od / 2", "receiver.shoulder_z", "receiver.shoulder_z + receiver.shoulder_thickness"]`.
- `depth`: `["-receiver.shoulder_od / 2", "receiver.shoulder_od / 2"]`.
- `z_rule` unchanged: z_min `base.plate_thickness`, so X1 is unchanged.
- base_plate neighbour receiver stays C. New source: "receiver shoulder underside on the plate top (Design Notes 32); S1 draws the plate without its spigot hole, so this C is not an S3-3 certifier (struck from s3_spec chains)".
- `s1_side_poses.py` (P6, the S1 r8 script): after the receiver wall `_sides` call, draw `_sides(ax, "receiver", r_out, shoulder_od / 2, zs, zs + shoulder_thickness, hatch="//")`, where zs = `receiver.shoulder_z` in z_S.

**S2 (`s2_spec.yaml`).** New row `receiver_shoulder`, inserted before `base_slots`; the id is new, so X1 skips it.
- kind cylinder, axis Z, projection circle.
- keys: the three shoulder leaves.
- z_rule: `receiver.shoulder_z` to `receiver.shoulder_z + receiver.shoulder_thickness`.
- place: round, r_in 0, half_width `receiver.shoulder_od / 2`.
- neighbour base_plate C, with source "shoulder underside on the plate top (Design Notes 32); the S3 section certifies the seat face (S3-3)".
- chain [axial], moves false.
- note: "the receiver body above the shoulder is not drawn in S2 (S1, S3 draw it); the row stands for the seat footprint on the plate".
- `part_list`: add `{part: "receiver shoulder", row: receiver_shoulder}`.

The spigot hole row (`base_spigot_hole`) stays as it is. The renderer places it under the shoulder (K8 MEASURED clean).

**S3 (`s3_spec.yaml`).**
- receiver row: the same `shape` intent as S1 ("... shoulder D180 x 8 resting on the plate top either side of the spigot hole (seat face at receiver.shoulder_z, the cut-case seat), spigot below the plate top not drawn (S4-a) ..."). It gets the same `keys`, `section` piece and `depth` as S1. z_rule is unchanged.
- base_plate neighbour receiver:
```yaml
  - id: receiver
    class: C
    source: 'receiver shoulder underside on the plate top, annulus r 80.2 to 90 either side of the spigot hole: the cut-case seat (Design Notes 32; Designer 1.3 receiver shoulder); spigot r 80 in the hole r 80.2 is the G 0.10 radial fit, drawn at S4-a'
    face: {z: receiver.shoulder_z, side: shoulder underside on the plate top (cut case)}
```
- `chains` a, b and c, link [receiver, base_plate]:
```yaml
    - {pair: [receiver, base_plate], certifiers: ["S3 base_plate|receiver"], note: "shoulder underside on the plate top (Design Notes 32); S1 base_plate|receiver C struck: S1 draws the plate without its hole (Loftsman 1.3 (c) P5L F1)"}
```

**S3-3 certifier text (the spec and gameplan l.288).**
- receiver|base_plate is certified by "S3 base_plate|receiver" alone, on the named face `receiver.shoulder_z` (shoulder underside on the plate top, 12 z_A).
- "S1 base_plate|receiver C" is struck from chains a, b and c.

**Fixtures (P6, with the Engineer's item 5 scaffolding removal).** The live-spec changes require these:
- `_receiver_cert` and `_plate_g` go.
- S3-3-B3 `planted` goes from 14 to 11, because the three receiver links are no longer certified by S1.
- S3-3-B9 is redefined; its old plant no longer exists. The new plant: seat face 1 above the plate top (`receiver.shoulder_z` 13), with chains a and b listing only "S1 base_plate|receiver C". The section F opens the pair in chains c, a and b.

## 3 Dry run

**S3, post-P6 state, fresh records, live P4 findings applied (`s3_dry.py z`, MEASURED).**

| Check | After | Before (sk0, same probe) |
|---|---|---|
| K2 | pass (412 keys) | pass (409) |
| K4 | fail 22, fixture draws no labels | fail 22, the same |
| K5 | pass, 104 artists | pass, 102 |
| K6 | pass, 48 z_rules within 0.05 | pass |
| K7 section | **pass, 269 tests; base_plate\|receiver C, distance 0.000, overlap 0.000** | fail 1: base_plate\|receiver distance 0.200, state F |
| K7 inset | pass, 44 tests | pass |
| K8 | pass, 212 + 63 predicates | pass, 210 + 63 |
| K9 | pass | pass |
| S3-1 | pass, 25.84 | pass |
| S3-2 | pass, 3.97 | pass |
| **S3-3** | **pass, 51 links closed** (face at 12 z_A: shoulder 80 to 90 and plate 80.2 to 239 overlap 9.80 in u) | fail 3: chains c, a, b, receiver\|base_plate, state F |

The drawn shoulder pieces at capture_end are u -90 to -80 and u 80 to 90, z_A 12 to 20 (MEASURED).

**B plants on S3 (MEASURED).**

| Plant | K7 section | S3-3 |
|---|---|---|
| Shoulder OD 160.4 (= the hole: a corner) | C 0.000 | fails 3: "faces ... overlap by no more than 0.05 in u (a corner is no axial seat)" |
| Seat face 1 above the plate top (`shoulder_z` 13) | fails 1: 0.200, state F | fails 3, state F |
| New S3-3-B9 (seat 1 up, chains a and b S1-only) | fails 1 | fails 3 (chains c, a, b) |
| Signed receiver row (no shoulder) | fails 1: 0.200 F | fails 3 |

**Shoulder piece against every neighbour (piece-to-piece XZ distance, MEASURED).**
- In S1 the distances are equal in all four poses (load, start, capture_end, park) unless the table says otherwise.
- The S3 column is the section at capture_end.

| Neighbour | S1 | S3 section | Note |
|---|---|---|---|
| base_plate | 0.00 (C) | 0.00 (C, face) | |
| base_frame | 12.00 (the plate between) | 154.47 (rail at \|u\| 244) | |
| collet | 23.70 | 23.70 | Receiver floor and wall between (nested) |
| core_seat | 36.06 | 36.06 | |
| holder | 31.75 | 31.75 | |
| wing nut (box, sweep r 115) | 77.09 | 77.09 | Wing-nut bottom 97.09 above the shoulder top 20: knuckle room under the wings |
| collar | 133.14 | 133.14 | |
| core_750 | 86.54 load; 37.50 start, capture_end | 37.50 | |
| drill_head (cutter r 88.9) | 939.84 load and park; 814.84 start; **164.84 capture_end** | 164.84 | Cutter tip 184.84 z_A at its lowest |
| frame_upper_a, _b | XZ 106.31; depth bands 6.02 apart (state depth-separated, unchanged) | frame_upper_c 154.00 | |
| guide rods | 130.00 (was 140.00 to the receiver row) | not drawn | |
| liftmotor_a / _c | 162.10 | 165.97 | |
| anchor_a | 246.55 | | |
| descent_stop_post | 283.33 | | |
| keep-out line (r 86.2, from z_A 40) | 20.00 | 20.00 | Shoulder r 90 lies outside r 86.2 in plan and 20 below the keep-out band |

**S1 full run (`check_sketch.py s1 --rev 90`, MEASURED).**
- Every check reads as on sk0 (K5 red 8, the anchor line until r8; RPT not a record).
- K7 618 tests, all clean. The only receiver differences are guide_member and guide_member_b, 140.00 to 130.00, in all four poses (8 tests).
- base_plate|receiver stays C 0.000 in all four poses. S1-5b least 142.00 is unchanged.

**S2 full run (`check_sketch.py s2 --rev 90`, MEASURED).** 18 of 18 pass.
- **S2-5a: 27 fixed parts, least 11.71 (unchanged).** S2-5b: 19.84 (unchanged).
- K7 went from 1292 to 1296 tests. receiver_shoulder|base_plate reads z-contact, distance 0.
- Every other receiver_shoulder pair reads undeclared:z-separated.
- K4, K5, K8 and K9 are clean with the new row.

**S2 plan footprint (DERIVED).**
- The shoulder disc r 90 lies inside the operator sector wedge (r 400). So do the receiver, holder and wing nut, which are the work the sector serves. It is not on the S2-5a fixed list and sits at z_A 12 to 20, 420 below the hand band (440).
- In plan it covers the spigot hole circle r 80.2, the keep-out r 86.2 and the tube r 76.2, at z below all three bands.

**`--stale` on the copy (MEASURED).** 2 records, the same 5 differences as the live tree. The new keys appear in no accepted record. X1 pass, 70 rows.

**Controls on the copy (`--controls --jobs 12`, 173.5 s, MEASURED).** Z 90/92, B 261/273, smoke 3/3. All 14 mismatches are S3-3 and K7-Z18/B35, and every one traces to the scaffolding listed in section 2.
- With `_receiver_cert` and `_plate_g` made no-ops (`--only "S3-3-*,K7-Z18,K7-B35"`), 12 of 14 match.
- S3-3-B3 fires 11 against a planted 14. The difference is the three receiver links no longer certified by S1.
- S3-3-B9 reads clean. Its signed plant opened the pair through an F that the shoulder removes. The redefined B9 fires 3 (above).

**Wider shoulder, option (ii) of section 5 (S3 only, `s3_dry.py od200`, MEASURED).** All checks as in the Z run.
- S3-3 passes, 51 links.
- Shoulder to frame_upper_c is 144.00, and to base_frame 144.50.

## 4 Representative-shape notes

- The S3 section shows the shoulder and the plate hole gap. The spigot below the plate top (z_A 0 to 12) stays undrawn until S4-a, because z_rule z_min = plate top is shared with S1 (X1).
- The shape strings and the part list say this.
- At M1, the empty hole under the receiver reads as "spigot not drawn (S4-a)". The figure note carries it.
- S1 draws the shoulder as two hatched 10 x 8 pieces standing on the slab. This is consistent with S3, and the S1 C is labelled a slab simplification in its source.

## 5 For Sean

1. **Values:** shoulder OD 180, thickness 8, seat face at the plate top (12 z_A), body above unchanged (ASSUMED). The tray hole goes from 81.2 to 91.0 with it. Quinn's answer to B2-10 also covers the tray and the ASSEMBLY.md load-path line.
2. **Uplift (Correction 3).** Retract with bind, and stall up up to 1029.5 N, lift the receiver off the plate. Nothing holds it down today. Options:
   - (i) As ruled: OD 180 and no fasteners. Uplift is left to Step 2, the bind and stall rows.
   - (ii) OD 200 with 4 x M5 through the shoulder into the plate. This holds the uplift and gives an anti-rotation path for the core torque beside the foot flat. The tray hole becomes r 101. The S3 dry run is clean (section 3).

   Recommendation (i) now, because Sean's ruling is the cut-case seat, with (ii) carried as a Step 2 row.

## Gameplan lines to change

1. l.703 (Design Notes 32).
```
Old: (dimensions ASSUMED, set by the Designer with a dry-run before P6).
New: (dimensions ASSUMED, set by the Designer with a dry-run before P6: receiver.shoulder_od 180, receiver.shoulder_thickness 8, seat face receiver.shoulder_z = base.plate_thickness 12 z_A, body above unchanged; tray.hole_r 81.2 to 91.0 with it (Quinn, B2-10); S3-3 Z 51 links closed on the dry run; research/sean/cr_scratch/step1.3_designer_receiver_shoulder.md). Uplift in retract-bind and stall up (receiver unfastened) goes to the Step 2 bind and stall rows (option: OD 200 with 4 x M5 into the plate).
```
2. l.288 (S3-3 row, rule column, live text).
```
Old: (named face per S3 certifier: anchor locknut top 272, cover underside 288, nut counterbore shoulder;
New: (named face per S3 certifier: receiver shoulder underside on the plate top 12, certified by S3 alone in chains a, b, c, the S1 slab C struck (Design Notes 32); anchor locknut top 272, cover underside 288, nut counterbore shoulder;
```
3. l.288 (S3-3 row, B column, after P5f item 9).
```
Old: the section F on receiver\|base_plate opening it in chains c, a, b (B9)
New: the receiver shoulder seat 1 above the plate top opening receiver\|base_plate in chains c, a, b with chains a and b certified by S1 only (B9, redefined at P6 for Design Notes 32)
```
4. l.651 (S4-a row).
```
Old: | S4-a | Base-plate spigot-hole break (80.2 hole on the 80 spigot); receiver\|base_plate becomes G 0.10 | 1.4 (S4) |
New: | S4-a | Base-plate spigot-hole break (80.2 hole on the 80 spigot, spigot drawn z_A 0 to 12 under the receiver shoulder); receiver\|base_plate stays C on the shoulder face (Design Notes 32); the spigot fit, 0.20 radial against 0.10, is drawn and checked as a radial gap | 1.4 (S4) |
```
