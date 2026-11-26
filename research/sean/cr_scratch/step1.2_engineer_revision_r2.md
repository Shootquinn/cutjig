# Step 1.2 (h) Engineer: S2 r2 and S1 r6

## Corrections to the brief

1. **Tick toe radius.** The F1 rule names the toe as `pinion.r_toe` and gives r 95.2. `pinion.r_toe` is 96.54 (DECLARED, overlay, toe pitch point). r 95.22 is the pinion toe tip, the pinion place `r_in` expression `pinion.r_toe - pinion.pitch_diameter / pinion.tooth_count * sind(pinion.pitch_angle)` = 96.54 - 4.1665 x 0.31623 = 95.22 (DERIVED). The ticks and the K8 `ticks_radial` predicate use that expression, so the drawn ticks run 95.22 to 125.00, as the rule's stated radii and the amended shape text say. The Designer confirms the key at re-sign, or names `pinion.r_toe` and the ticks start at 96.54.
2. **`reference: true` on the keep-out moves the S2 highest point.** The keep-out z_max is `top_block_top`, and S2 has no top-end block row. With the keep-out excluded, the S2 highest point at load and park reads 1819.84 z_S (drill tube top), not 1969.84 (MEASURED, check_stack). The jig top stays 1969.84 z_S from S1 (top-end block). At capture_end it reads 1285.00 z_S (tie and member tops), as the Loftsman (LF1.2-5) gives. Open item 1.
3. **TP1.2-9 cover premise "B2" is a Z.** "A circumscribing lift-motor circle offered as cover and not counted" is the correct behaviour, so its control reads clean (K8-Z7). It fails on code that counts circumscribing outlines. K8-B33 is its contrast B: the same motor drawn as its circle, a true outline, covers the pad and fires.
4. **S1 r6 PNG size.** The S1 fix for M1 S1 r5 F1 saves with `bbox_inches="tight"`, as S2 does. The r6 PNGs are cropped to their content (park 1422 x 1390 px, r5 2100 x 1500, MEASURED). Scale, the drawn geometry and every label anchor are unchanged (S1 label anchors moved: 0 of 55 per pose set, MEASURED).
5. **F2 was ruled "visual only".** The brief requires every new rule to ship with Z and B (h), so the dashed-if-hidden rule ships as the K8 `cover` check (the Topologist's optional TP1.2-9 predicate). The Topologist signs it as raiser, the Designer signs the drawing rule.
6. **Two existing B fixtures re-styled.** K8-B19 (screws drawn at -theta land under pinions and motors) and K8-B26 (bearing annulus under the gear and hub) drew their planted pieces solid. With the new K8 cover check they fired 9 and 2 issues against 6 and 1 planted. Each planted piece is now drawn dashed. The planted defect is unchanged, and the counts match again.

Tags: run results MEASURED 2026-11-25 on `docs/sketches/`, Python 3.12, matplotlib 3.11.2. Hand values DERIVED. Design values DECLARED, or ASSUMED as in the overlay.

## 1 Disposition per finding

| Finding | Source | Fix | K8 predicate / check | B fixture (Z) |
|---|---|---|---|---|
| F1 gear teeth | Designer M1 S2 r1, ruling 1 | The pitch circle is removed. Dashed radial ticks run on the underside face from 95.22 to 125.00, `gear.tooth_count` 60 of them, as one LineCollection, gid `gear:ticks`. The gear has a light plain fill, no hatch. Shape text amended per the ruling, and the part list updated. K5 admits a `<row>:ticks` LineCollection only for a gear row with axis Z in plan, one per figure, and only when the row carries `ticks_radial`. K9 accepts the sub-gid only for an existing row. | K8 `ticks_radial` (spec sense on `gear`: r_in, r_out, count). K5 tick admission. K9 sub-gid. | K8-B29 one tick tangential, K8-B30 one tick 5 past the heel, K8-B31 59 ticks (Designer's B1 to B3). K5-B14 ticks as a Line2D, K5-B15 ticks without the predicate (premise), K5-B16 two collections, K9-B6 `gear2:ticks`. Z: K8-Z6, K5-Z3, K9-Z3 (live S2 with ticks) |
| F2 dashed-if-hidden | Designer M1 F2 and addendum; Topologist TP1.2-2 | `sketch_common.hidden_rows`: a row whose plan outline lies wholly under true outlines of rows with a z_max higher by more than 0.05 is drawn dashed, with no fill and no hatch. Live set at load: nuts a/b/c, descent-stop pad, motor mounts a/b/c, guide lugs a/b, guide rods (both), and the rows already dashed (base frame, anchors and arms, lift motors, bushings, bearing, cutter rim, post). The pinion toothed piece is drawn hidden (it lies inside the gear annulus, with its heel corners at r 133.07). Its hub stays solid. The fixture drawing applies the same set. | K8 `cover` (plan): any drawn area artist wholly under true outlines of higher rows must be non-solid. Premise: only true outlines count as cover. | K8-B32 nut_a solid under guide_a (as r1). K8-Z7 premise (circumscribing circle not counted). K8-B33 premise contrast (circle outline covers). Z: K8-Z6 |
| TP1.2-2 tie legend | Topologist; Designer addendum | The legend is split: "dashed, no fill: under a nearer part (...)" and "dashed: Step 2 stand-in (rod top ties)". The ties stay dashed. | visual only (the Designer signs the legend) | none |
| F3 F6 label | Designer M1 F3, ruling 2 | `sightline_f6.label.text` loses its trailing " z_S". The drawn label reads "...; eye z_S 1600 (operator.eye_height 1540 z_A)" (MEASURED, PNG). | visual only (K4 carries the number) | none |
| F4 leader ends on ink | Designer M1 F4 | `sketch_common.label_anchor` keeps (max x, mid y) when it lies on the row's ink. Otherwise it takes the drawn vertex of greatest x (nearest mid y). Sightline: observer (200.00, 346.41). Sector: wedge corner (282.84, 282.84). | K4 leader rule (a): every label xy within 0.05 of its row's ink | K4-B7 sightline at the r1 anchor (200.00, 173.21), 86.60 off the line (it also crosses the sector leader, planted 2). Z: K4-Z3 live S2 script, K4-Z2 |
| F5 concentric leaders | Designer M1 F5 | New spec row field `label_theta`: tube 340, keep-out 350, cutter 0, gear 10. The anchor is the farthest ink point on that ray. | K4 leader rule (b): no two leaders cross | K4-B8 live S2 without `label_theta` (r1 anchors), 3 crossings. Z: K4-Z3 |
| S1 r5 F1 park note clipped | Designer M1 S1 r5 | `s1_side_poses.py` saves `bbox_inches="tight"`. | K3 text rule: every Text inside the saved image (the canvas, or the tight bbox when every `savefig` in the script passes `bbox_inches="tight"`; premise read from the script AST) | K3-B8 r5 park on the canvas (9 px out). K3-B9 premise: one `savefig` without tight in the script list. Z: K3-Z2 S1 load on the canvas, K3-Z3 S1 with the tight premise |
| Ruling 3 reference rows | Designer M1 ruling 3; Loftsman LF1.2-5 | `reference: true` added to `sightline_f6`, `collet_axis` and `keepout` (`operator_sector` already had it). check_stack's highest point already excluded reference rows. The new `checks_s2.reported` excludes them from the outline extents. The keep-out's declared S2-a pairs are still judged (K7 tests declared pairs whatever the flag). | none (report) | none |
| Ruling 4 spec status | Designer M1 ruling 4 | Status text applied, plus an r2 clause naming the edits awaiting re-sign. | none | none |
| N1 lift motors faint | Designer M1 NOTE | Lift-motor dash weight 0.5 to 1. | visual only | none |
| N2 pad outline | Designer M1 NOTE | Withdrawn by the Designer (the pad is hidden, so dashed). | none | none |
| TP1.2-3 S2-5b premise set | Topologist | `s2_checks.S2-5b.parts: moves`. The check takes every `moves: true` row that is not reference and not a line kind. A hand list is refused as a content failure. Live: 10 moving parts in the sector, least drill_head 19.84. | S2-5b | S2-5b-B2 drill tip at 945 z_A (on the r1 code: clean, "8 ring parts in the sector, least 136.84", MEASURED before the change). S2-5b-B3 r1 hand list refused. S2-5b-B1 unchanged. Z: S2-5b-Z |
| LF1.2-1 K7 record | Loftsman | Every K7 result carries `test_fields` [pose, pair, class, state, z_gap, distance, overlap, basis] and `tests`, one entry per state, in plan and side views. Basis values: z band, depth band, box bound, circumscribed outline, depth disk, exact, XZ projection (exact), plan footprint (spec placement), declared N; swept entries tagged. `check_sketch.run_sketch` lints the record and fails K7 on a defect. S2 r2: 7334 entries. S1 r6: 5556 entries. | `k7_record_issues` | K7-B32 pair id dropped from entry 0. Z: K7-Z16 (S2), K7-Z17 (S1) |
| LF1.2-2 pinion\|gear_hub | Loftsman; Designer addendum ruling | Declared on `gear_hub`: pinion_a/_b/_c class G, g_min 3 ASSUMED, with the Designer's source text. No geometry change. Record: `gear_hub\|pinion_a G G z_gap -17.39 distance 5.222 basis circumscribed outline` at all four poses. "pinion toe to gear hub 5.22" added to the spec `reported` list and the summary. | K7 G (existing rule) | K7-B33 g_min 6: short at 4 poses x 3 pinions (12). Z: K7-Z15 |

Rules awaiting signature, before the revision goes to M1:

| Rule | Premise check | Raiser, signs |
|---|---|---|
| K5 tick admission and K8 `ticks_radial` | K8 `ticks_radial` (B29 to B31); admission requires the predicate (K5-B15) | The Designer (F1) |
| K8 `cover` (dashed if hidden) | only true outlines count as cover (K8-Z7, K8-B33) | The Topologist (TP1.2-9); the Designer signs the drawing rule and the split legend |
| K4 leader rules (on ink; no crossing) and spec field `label_theta` | the anchor is computed on the drawn ink (K4-B7, K4-B8) | The Designer (F4, F5) |
| K3 text inside the saved image | `bbox_inches="tight"` read from the script (K3-Z3, K3-B9) | The Designer (S1 r5 F1) |
| K7 record lint | entry count equals state count; ids present (K7-B32) | The Loftsman (LF1.2-1) |
| S2-5b over `moves: true` | a hand list is refused (S2-5b-B3) | The Topologist (TP1.2-3); the Designer as S2-5b raiser |

Spec changes for Designer re-sign (placement-free; the Loftsman checks the G 3 declaration): gear shape text and `ticks_radial`; `label_theta` on four rows; `reference: true` on three rows; F6 label text; status text; `reported` list (tight spots with basis, highest point over parts); S2-5b `parts: moves`; gear_hub neighbours G 3; part-list gear entry. No S1 key and no params or overlay value changed.

## 2 Files changed

| File | Change |
|---|---|
| `docs/sketches/sketch_common.py` | `ink_pieces`, `ink_distance`, `label_anchor` (replaces `_right_anchor`); `leader_issues` in K4; `saves_tight`, `text_clip_issues` in K3; `TICKS_SUFFIX`, `ticks_admission_issue` (K5), `ticks_radial_issue` (K8), K9 sub-gid; `hidden_rows`, `cover_issues`, `is_solid` (K8 plan); `K7_TEST_FIELDS`, `_side_measure`, `_plan_basis`, `k7_record_issues`, per-test logging in `k7` and `_k7_plan` |
| `docs/sketches/check_sketch.py` | K7 record lint in `run_sketch`; per-sketch `reported(ctx)` written to the record (`reported_drawn`) and to the summary |
| `docs/sketches/checks_s2.py` | `moving_parts`, S2-5b over `parts: moves`; `reported(ctx)` (extents without reference rows, highest point over parts, tight spots with basis, S2-5b strike list) |
| `docs/sketches/s2_spec.yaml` | section 1 |
| `docs/sketches/s2_plan.py` | hidden-row styling from `hidden_rows`; pinion toothed piece hidden; gear plain fill plus `gear:ticks`; pitch circle removed; legend split; lift-motor dash weight |
| `docs/sketches/s1_side_poses.py` | `savefig(..., bbox_inches="tight")` |
| `docs/sketches/fixtures/builders.py` | hidden rows dashed and gear ticks in the S2 fixture drawing; `_ticks`; 23 new builders; K8-B19 and K8-B26 planted pieces dashed |
| `docs/sketches/fixtures/manifest.yaml` | 23 entries (section 3); S2-5b-Z description |

## 3 Check results

New controls (23): K3-Z2, K3-Z3, K3-B8, K3-B9, K4-Z3, K4-B7, K4-B8, K5-B14 to B16, K9-B6, K8-Z7, K8-B29 to B33, K7-Z16, K7-Z17, K7-B32, K7-B33, S2-5b-B2, S2-5b-B3.

Red-first: on the r1 code none of the new branches existed, so each new B read clean there. S2-5b-B2 was run on the r1 `checks_s2.py` before the change and read pass, "8 ring parts in the sector, least 136.84" (MEASURED).

**Controls** (`check_sketch.py --controls`, final run 2026-11-25): exit 0, **214/214 matched** (Z 62/62, B 150/150, smoke 2/2), **1640 s** (r1: 191 in 284 s). Results are in `docs/sketches/wip/fixtures/controls_results.json`. The first full run after the change matched 212/214. K8-B19 and K8-B26 fired extra cover issues (Correction 6). Their fixtures were re-styled, and the final run is clean.

**S2 r2** (`check_sketch.py s2 --rev 2`): **17/17 pass**, green on the first run. K4 14 labels, leaders on ink, no crossing. K5 99 artists. K7 1292 plan tests, 7334 record entries. K8 183 predicates (ticks_radial, cover over 68 artists). K9 70 rows. S2-5b 10 moving parts, least 19.84 (drill_head). S2-1 to S2-6 values equal to r1.

**S1 r6** (`check_sketch.py s1 --rev 6`): **18/18 pass**. K3 every text inside the saved image. K4 55 labels. K7 609 tests, 5556 record entries. S1-1 650.00, S1-2 125.00, S1-3 367.34 / 117.34, S1-4 0.84, S1-5a 192.34, S1-5b 142.00, S1-7 spare 72.73, all equal to r5. Mass report r6 is byte-equal to r5.

**Stale** (`--stale`): exit 1, one difference, `sketches/s1_checks_r4.json: frame_upper.radius recorded 300, live 274` (the adopted key only). With `--include-unaccepted`: 6 records checked, the same single difference.

PNG paths:
- `docs/sketches/wip/s2_plan_r2.png`
- `docs/sketches/wip/s1_pose_load_r6.png`, `wip/s1_pose_start_r6.png`, `wip/s1_pose_capture_end_r6.png`, `wip/s1_pose_park_r6.png`

Records:
- `docs/sketches/wip/s2_checks_r2.json`, `wip/s2_summary_r2.md` (reported values appended by `checks_s2.reported`)
- `docs/sketches/wip/s1_checks_r6.json`, `wip/s1_summary_r6.md`, `wip/s1_mass_report_r6.json` (byte-equal to r5)

## 4 Reported values, S2 r2

| Quantity | Value | Tag |
|---|---|---|
| Outline extents, every drawn part (reference rows excluded) | x -322.00 to 322.00, y -304.00 to 304.00 | MEASURED |
| Outline extents, parts above the plate | x -278.27 to 278.27, y -304.00 to 218.00 | MEASURED |
| Highest point over parts | load and park 1819.84 z_S (drill tube top; Correction 2); start 1694.84; capture_end 1285.00 (tie b) | MEASURED |
| Pinion toe to gear hub | 5.22 = 95.22 - 90.00 (G 3 ASSUMED; record basis circumscribed outline, equal to the drawn toe edge) | MEASURED, DERIVED |
| Lift motors to the sector edge | 11.71 bound (circumscribed) / 15.69 drawn square | MEASURED |
| Ring rim to guide rod / to member | 10.00 / 34.00 (record basis exact) | DERIVED, MEASURED |
| S2-5b strike list at load (margin over 940 z_A) | drill_head 19.84, drill_tube 126.21, bearing 136.84, ring 149.84, motor_mount_c 161.84, pinion_c 168.22, motor23_c 185.34, motor_shaft_c 209.84, gear and gear_hub 242.07 | MEASURED |
| Cutter overhang of the keep-out, F6 eye limits, member edges, tip force | unchanged from r1 (2.70; 492.46 / 578.80 z_S; 43.73, 0.00; S1 mass report r6 = r5) | DERIVED, MEASURED |

## 5 Open items

1. **S2 highest point (Designer, Loftsman).** S2 draws no top-end block, so the S2 highest point after ruling 3 is the tube top (Correction 2). Either S2 takes a top-end block row (it sits on the axis above the tube and would be the topmost plan part over the bore), or the S2 summary cites the S1 height. No change made.
2. **K7 record size.** `s2_checks_r2.json` is 1.38 MB (r1 0.19 MB): 7334 entries of 8 fields. The fields are as LF1.2-1 asks.
3. **Run time.** K3 text extents (a renderer per figure), K8 cover and the per-test K7 measures raise `check_sketch.py s2` from 14 s (r1) to about 58 s, and `--controls` from 284 s to 1640 s (MEASURED). The Software Engineer may want the K7 record measures cached or the K3 renderer shared across checks.

## Gameplan lines to change

**l.137** (K table, K3 row; three changes on the line).

Old:
```
figsize at least (14, 10) side or (10, 10) plan; dpi 150 | Conforming fixture figure |
```
New:
```
figsize at least (14, 10) side or (10, 10) plan; dpi 150; every Text inside the saved image (the canvas, or the tight bounding box when every savefig of the script passes bbox_inches="tight", read from the script; 1.2 (h), Designer M1 S1 r5 F1) | Conforming fixture figure; K3-Z2 live S1 load on the canvas; K3-Z3 live S1 with the tight premise |
```
Old:
```
default figsize (6.4, 4.8), dpi 100 |
```
New:
```
default figsize (6.4, 4.8), dpi 100; K3-B8 S1 r5 park note below the canvas; K3-B9 one savefig without bbox_inches="tight" |
```

**l.138** (K table, K4 row).

Old:
```
(1.2 (c), Designer 1.2 (b) FIX 3, Designer 1.2 (c) FIX R1) | Fixture with all labels from keys; K4-Z2 live S2 |
```
New:
```
(1.2 (c), Designer 1.2 (b) FIX 3, Designer 1.2 (c) FIX R1); every label leader ends on its row's ink within 0.05 and no two leaders cross; a concentric row may set label_theta, the leader azimuth (1.2 (h), Designer M1 r1 F4, F5) | Fixture with all labels from keys; K4-Z2 live S2; K4-Z3 live S2 drawn by s2_plan.py |
```
Old:
```
K4-B6 S1 r5 spec with not_drawn and no figure_note (FIX R1) |
```
New:
```
K4-B6 S1 r5 spec with not_drawn and no figure_note (FIX R1); K4-B7 sightline leader at the r1 anchor, off the line; K4-B8 r1 concentric anchors, three crossings |
```

**l.139** (K table, K5 row).

Old:
```
(TP-13; admission, not presence: a missing hub is an M1 item) |
```
New:
```
(TP-13; admission, not presence: a missing hub is an M1 item); 1.2 (h): a gear row with axis Z in plan admits one LineCollection <row>:ticks (dashed tooth ticks on the underside face) only when the row carries K8 ticks_radial (Designer M1 r1 F1) |
```
Old:
```
K5-B13 pinion hub wider than the heel |
```
New:
```
K5-B13 pinion hub wider than the heel; K5-B14 ticks as a Line2D; K5-B15 ticks without the ticks_radial predicate; K5-B16 two tick collections |
```

**l.141** (K table, K7 row, Z and B columns).

Old:
```
Z14 plan annuli (ring, bearing, tube); Z15 live S2 |
```
New:
```
Z14 plan annuli (ring, bearing, tube); Z15 live S2; Z16, Z17 record lint on live S2 and S1 |
```
Old:
```
swept as F (LF-c1) |
```
New:
```
swept as F (LF-c1); B32 record entry without its pair id (LF1.2-1); B33 pinion|gear_hub at g_min 6 against the 5.22 toe gap (LF1.2-2) |
```

**l.142** (K table, K8 row).

Old:
```
taper in the radial frame on the toothed trapezoid |
```
New:
```
taper in the radial frame on the toothed trapezoid. 1.2 (h): ticks_radial, the <row>:ticks segments lie on radii (line within 0.05 of the axis) between r_in and r_out, count as the spec (Designer M1 r1 F1); cover, in plan a drawn area artist wholly inside true outlines of rows with a z_max higher by more than 0.05 is drawn non-solid (dashed or dotted, no fill, no hatch); premise: only true outlines cover (Designer M1 r1 F2 rule, Topologist TP1.2-2, TP1.2-9) |
```
Old:
```
B28 motor shaft 15 longer at its low-x end only |
```
New:
```
B28 motor shaft 15 longer at its low-x end only; B29 one tick tangential; B30 one tick 5 past the heel; B31 59 ticks; B32 nut_a solid under guide_a; Z7 cover premise (circumscribing circle not counted) and B33 its contrast (circle outline covers) |
```

**l.143** (K table, K9 row).

Old:
```
outside its `poses` (TP1.1-2) |
```
New:
```
outside its `poses` (TP1.1-2); a <row>:ticks sub-artist of an existing row is not a stray (K5 rules its admission; 1.2 (h)) |
```
Old:
```
K9-B5 core_750 drawn seated at park |
```
New:
```
K9-B5 core_750 drawn seated at park; K9-B6 ticks under a row the spec does not have |
```

**l.146** (K table summary paragraph, end).

Old:
```
(191 controls: Z 56, B 133, smoke 2; 295 s).
```
New:
```
(191 controls: Z 56, B 133, smoke 2; 295 s). Step 1.2 (h) r2 (`research/sean/cr_scratch/step1.2_engineer_revision_r2.md`) added K3-Z2, K3-Z3, K3-B8, K3-B9, K4-Z3, K4-B7, K4-B8, K5-B14 to B16, K9-B6, K8-Z7, K8-B29 to B33, K7-Z16, K7-Z17, K7-B32, K7-B33, S2-5b-B2, S2-5b-B3 (214 controls: Z 62, B 150, smoke 2; 1640 s).
```

**l.258** (S2-5b row, B column).

Old:
```
drill_head tip at 945 z_A at load (TP1.2-3) | hand band ASSUMED |
```
New:
```
drill_head tip at 945 z_A at load (TP1.2-3); spec S2-5b with a hand list in place of parts: moves (S2-5b-B3) | hand band ASSUMED |
```

**l.493** (Progress Log, add a row after it).

Old:
```
| 1.2 | 2026-11-25 | (e) P7a Loftsman (`step1.2_loftsman_crossreview.md`):
```
New (insert this row after the l.493 row; the l.493 row itself is unchanged):
```
| 1.2 | 2026-11-25 | (h) P9 (`step1.2_engineer_revision_r2.md`): S2 r2 and S1 r6 for Designer M1 S2 r1 F1 to F5 and rulings 1 to 4, S1 r5 F1, TP1.2-2, TP1.2-3, LF1.2-1, LF1.2-2. Gear ticks (K5 admission, K8 ticks_radial); dashed-if-hidden (K8 cover); leaders on ink and uncrossed (K4, label_theta); text inside the saved image (K3; S1 saves tight); reference rows out of highest point and extents; S2-5b over moves: true (least drill_head 19.84); K7 record per test with basis; pinion\|gear_hub G 3 (5.22). S2 r2 17/17, S1 r6 18/18 (values equal to r5), controls 214/214 (1640 s), --stale red on s1 r4 frame_upper.radius only. Rules awaiting signature: Designer (ticks, leaders, K3), Topologist (cover, S2-5b set), Loftsman (record lint). Next: P7r, P8r. |
```
