## Corrections to the brief

1. **A filled arrowhead was counted as an area.** K4 ruled the K4-Z6 label anchor "under the area of load_comp_c": the leader ends on the load_tension_c arrow, and `is_area` counted the load_comp_c FancyArrowPatch as an area that covers it (MEASURED). Load and look arrows are line or arrow kinds and draw no area, so `is_area` now returns False for a FancyArrowPatch. S1 and S2 draw none (their leader arrows belong to Annotations, not to `ax.patches`), and their records and PNGs are unchanged (section 4).
2. **F5's spec declaration lands now with the rule.** The brief says the F5 disposition lands now. The harness rule alone leaves the inset K7 red on the 13 nested pair-pose tests, so `s3_spec.yaml` gains `class_by_axes: {inset_plan: N}` on three neighbour entries: nut_housing_c|screw_c, screw_c|anchor_c and anchor_c|screw_c. Each keeps F in the section. That is the whole spec edit of this pass. F1, F2 and F3 stay for P6.
3. **The class_by_axes Z needs a clean section K7, and only the F1 declaration gives one.** K7-Z18 therefore applies the Loftsman's P6 remedy item 1 (base_plate|receiver G 0.10) inside the fixture only (`_plate_g`). The spec keeps C until Sean rules on a seat.
4. **The Loftsman's SYM-P B as written does not fire.** It removes `jackscrew.pitch_radius` from every keys list, but that key is also screw_b's label key, and `spec_keys` reads label keys (MEASURED: SYM-P clean). The B removes `jackscrew.top_guide_z` instead (no label reads it): 3 issues, on screw_c, screw_a and screw_b (MEASURED).
5. **SYM-Z2 is merged into SYM-Z.** With the key-union step gone from `_post_p6_specs`, SYM-Z is the post-P6 state with the key lists as signed, which is the state SYM-Z2 was to certify.
6. **K4-B22 is kept: K4 now refuses a label outside its home Axes.** `sub_spec` records the home Axes of a withheld label (`label_home`). K4 fails a `label:<id>` text drawn in any other Axes.
7. **Manifest `gameplan_line` (SW NOTE 6).** Every entry with an integer line on a K, X1 or S3 row now carries that row's line, set by check id: K1 135 to K9 143, X1 144, SYM and SYM-P 145 (the row P4 inserts), S3-1 286 to S3-3 288. Older entries were inconsistent: some 1 low, some correct.

Tags: MEASURED (run in this session), DERIVED (hand arithmetic), DECLARED (spec, review or ruling).

## 1 Fix table (raiser item -> change -> controls)

Merged duplicates, one control each: orphan (SW FIX 1 = TP FIX 1), S3-2 drawn span (SW FIX 2 = LF FIX 4), S3-3 untested fail paths (SW FIX 3 b to d = LF FIX 5), look direction (SW FIX 5 part = the drawing half of TP FIX 2). TP FIX 2's sign check is its own control.

| Raiser item | Change (file) | Controls |
|---|---|---|
| SW FIX 1 = TP FIX 1 (orphan_predicates NameError) | the message names `_pred_target(pr)` (sketch_common) | K8-B64 |
| SW FIX 2 = LF FIX 4 (S3-2 drawn span has no B) | fixture only | S3-2-B2 (guide bearing drawn 10 up: "drawn span 880.00 against 870.00") |
| SW FIX 3 (a) (named face, M02) | fixture only | S3-3-B4 (nut face named 1 above the shoulder: 3, i.e. c, plus the a and b nut links by symmetry) |
| SW FIX 3 (b) = LF FIX 5 (SYM failing inside S3-3, M03) | fixture only | S3-3-B5 (exempt anchor_b: 8) |
| SW FIX 3 (c) = LF FIX 5 (c link between counterparts open, M04) | exact range p(x_c) to p(y_c) - 1 (LF NOTE 1, checks_s3 `_c_range`) | S3-3-B6 (nut_housing_c 1 down: 3, the LF's 7 under the old range) |
| SW FIX 3 (d) = LF FIX 5 (record certifier in a non-C state, M05) | fixture only | S3-3-B7 (S1 collet\|holder F: 3) |
| SW NOTE 7 (pose filter, M07) | fixture only | S3-3-B8 (S1 collet\|holder at load only: 3) |
| SW FIX 4 (six convention clauses) | fixtures only | K8-B67 (5, class missing), B68 (4, past one profile width), B69 (3, partly behind), B70 (3, beyond hatched), B71 (3, beyond reaching x > 0), B72 (1, cut row missing x = 0) |
| SW FIX 5 (M14 undeclared id) | fixture only | K3-B11 |
| SW FIX 5 (M22 look direction) = TP look drawing | fixture only | K8-B65 (arrows toward +X: 2) |
| SW FIX 5 (M17 value_from) | fixture only | K4-Z6, K4-B21 |
| SW FIX 5 (M16 label off home) | K4 refuses a label drawn outside its home Axes (`label_home` in sub_spec; K4) | K4-B22 |
| SW NOTE 5 | `checks_s3.K_CHECKS` dropped | (runner default) |
| SW NOTE 6 | manifest gameplan_line by check row (Correction 7) | — |
| LF FIX 1 (veto per pair) | S3 verdict per pair across all chains (`s3v`); a failing verdict opens the pair in every chain (checks_s3) | S3-3-B9 (signed chains: 3, was 1) |
| LF FIX 2 (face width) | named faces overlap in u by more than TOL_Z (`_face_issue`) | S3-3-B11 (cover meeting the bearing at its corners: 3) |
| LF FIX 3 (veto premise) | `true_cut_issues`: every row of an S3-certified pair has section_u or section, an axis-Z round row with depth symmetric about x = 0, or a place centred on and symmetric about x = 0 (checks_s3, inside S3-3) | Z: S3-3-Z (15 rows); B: S3-3-B10 (bracket_anchor_c at theta 150: lint 1 plus its 2 opened links) |
| LF FIX 6 (SYM fields, F4 ruling) | SYM_FIELDS = (z_rule, place); `_post_p6_specs` loses its key union; SYM-P `sym_keys_premise` (check_sketch; appended to S3 runs only, so S1 and S2 records are unchanged) | SYM-Z (Z2 merged), SYM-P-Z, SYM-P-B1 |
| TP FIX 2 (section look sign) | `section_look_issues`: for section_yz, (u x z) . toward = -1 needs toward -X; any other toward is a spec error in the main Axes (sketch_common) | K8-B66 (spec +X, arrows +X) |
| TP FIX 3 (a) (unsectioned straddle) | an unsectioned row's depth band straddles x = 0 (convention 2) | K8-B73 |
| TP FIX 3 (b) (omitted-row converse) | `omitted_row_issues`: an area row absent from the section Axes lies wholly in front or wholly past one profile width (plan x band from the parent stack) | Z: K8-Z14 (12 inset-only rows omitted); B: K8-B74 |
| TP FIX 4 (points apart) | opposite senses on one line, plus heads apart (sketch_common `points_issues`) | K8-B75 |
| TP FIX 5 (mark section form B) | fixture only | K5-B36 |
| TP FIX 6 (mirror_about_radial) | K8 plan predicate `mirror_radial_issue` (PRED_TARGET, PLAN_PREDS); declared at P6 on the 12 radial inset rows | K8-Z15 (fixture declares it), K8-B76 |
| TP FIX 7 (F5, class per Axes) | `sub_spec` reads `class_by_axes[aid]`; premise lint `class_by_axes_issues` (K7, main Axes): an N override needs the pair at its base class C, F or G in another declared Axes; spec edit (Correction 2) | K7-Z18, K7-B35 |

## 2 Red-first table

Pre-change code: the P4 tree copied before the first P5f edit, at `docs/sketches/wip/p5f_pre/` (git-ignored), with the 32 new manifest rows (`new_manifest.yaml`) and the new fixtures. Its result file is `controls_results_prechange.json`. On that code: Z 0/4 clean, B 11/28 fired (MEASURED).

The 11 B controls that fire there plant defects in branches that P4 already had. Each of those is shown red by deleting the branch in a fresh copy of the current tree (`deletions.json` in the same folder). K5-B36 also fires on the P4 code, because the section form was a P4 rule; it is red on the save point 3 code (`wip/p4_prerun/`: 14 other issues, reason absent).

| Control | On the P4 code (MEASURED) | Branch deletion on the P5f code (MEASURED) |
|---|---|---|
| K3-B11 | fires (pre-existing branch) | M14 undeclared-id branch off: clean |
| K4-Z6 | fires (the arrow counted as an area, Correction 1) | — |
| K4-B21 | fires 2 (reason count mismatch) | M17 value_from off: fires 1, reason absent |
| K4-B22 | clean | — (new rule) |
| K5-B36 | fires (P4 section form) | save point 3 code: 14 other issues, reason absent |
| K7-Z18, K7-B35 | Z fires (13 inset overlaps), B 17 issues | — (new rule) |
| K8-B64 | error (NameError) | — (fix) |
| K8-B65 | fires 2 (pre-existing) | M22 look_direction off: clean |
| K8-B66 | clean | — (new rule) |
| K8-B67 to B72 | each fires 1 (pre-existing clauses) | M08, M11, M12, M13: clean; M09, M10: fires 1 on another clause, reason absent |
| K8-B73, B74, B75 | clean | — (new rules) |
| K8-Z15, K8-B76 | Z fires (unknown predicate), B 12 | — (new predicate) |
| S3-2-B2 | fires 1 (pre-existing) | M01 span test off: clean |
| S3-3-B4 | fires 9 (the old SYM key compare also opens a, b links) | M02 face verdict off: clean (and S3-3-B11 clean) |
| S3-3-B5 | fires 8 (pre-existing) | M03 SYM premise dropped: clean |
| S3-3-B6 | fires 9 (old range and SYM keys) | M04 range forced true: fires 1 (c link only), reason absent |
| S3-3-B7 | fires 11 | M05 non-C states certify: clean |
| S3-3-B8 | fires 11 | M07 pose filter dropped: clean |
| S3-3-B9 | fires 9 (veto per link: 1 of the 3 planted) | — (new rule) |
| S3-3-B10 | fires 10, lint reason absent | — (new rule) |
| S3-3-B11 | fires 8, face-width reason absent | — (new rule) |
| SYM-P-Z, SYM-P-B1 | error (no sym_keys_premise) | — (new rule) |

Every new B is red on the pre-change code or under the deletion of its branch.

## 3 Check results

| Run | Result (MEASURED) |
|---|---|
| `--controls`, default 12 jobs | **368/368 match**: Z 92/92, B 273/273, smoke 3/3, **157.6 s** wall (P4: 336 in 148.4 s; target 200 s). 32 added: Z 4, B 28 |
| `s3 --rev 0` (stub) | 16 checks. Green guards: K1, K2, K3, K5, X1, SYM-P. Red, content: K4 23, K8 112 (F3 spec error; the rest untestable), K9 71, SYM 3 (the S3 anchor exemptions only, under the F4 ruling). Red, absent: K6 69, K7 313 (13 fewer than P4: the inset pairs now N), S3-1, S3-2, S3-3, RPT |
| `--baseline s3` | run 2 matched **16/16** (SYM-P added to the stub guards, `checks_s3.STUB_EXPECT`) |
| `s1 --rev 7` | 18/19, no field differs from the P4 run (K5 red 8: the zero-area anchor line, until S1 r8) |
| `s2 --rev 8` | 18/18, no field differs from the P4 run |
| PNGs | `s1_side_poses.py --rev 7` (4) and `s2_plan.py --rev 8` (1) drawn on the P5f code pixel-equal to the same scripts on the P4 code at the live overlay; wip/ r7 and r8 PNGs restored |
| `--stale` | 2 records, the same 5 differences; X1 pass (70 rows, exemptions on place) |
| S3-3 on the fixtures | S3-3-Z clean, 51 links; true-cut lint passes on the 15 rows of S3-certified pairs |

Disk note: C: had 143 MB free when the first P5f controls run failed with Errno 28 on two fixtures. The P4 S3-3 fixtures had leaked one 1.6 MB temporary records directory per call (92 directories). They are removed, and `s3_fixtures` now reuses one directory per process (`_new_tmp`) with exit cleanup. A worker killed by the pool can still leave one directory. The rest of the full disk is outside this work.

## 4 Items for P6

| # | Item | Source |
|---|---|---|
| 1 | F1 receiver seat: apply the Loftsman's interim remedy only when P6 runs and Sean has ruled. The remedy is base_plate\|receiver G 0.10 and S3-only certifiers on chains a, b and c. Until a seat is ruled, S3-3 stays red on receiver\|base_plate in all three chains (veto per pair, S3-3-B9) | Loftsman P5L section 6; orchestrator |
| 2 | F2: nut_c and guide_c `projection: rectangle` | Topologist P5T section 7 |
| 3 | F3: drop `frame: radial` from motor_shaft_c outboard. Then remove the K8 STUB_CAUSE entry and re-run `s3 --rev 0` and `--baseline s3` (stub K8 reads absent) | Topologist P5T; SW NOTE 1 |
| 4 | Declare `{pred: mirror_about_radial, axes: inset_plan}` on anchor_a/_b/_c, liftmotor_a/_b/_c, frame_upper_a/_b/_c, home_switch_a/_b/_c (K8-Z15 shows the declaration clean) | Topologist FIX 6 |
| 5 | Remove the fixture scaffolding in the same revision that accepts S1 r8 and S2 r9 and lands the S3 spec edits: `p4_spec_findings`, `_receiver_cert`, `_post_p6_specs`, `_plate_g`, the pre-P4 figure fallback. Point S3-3-Z, SYM-Z, K5-Z4, K8-Z14 and K7-Z18 at the live specs | SW NOTE 2 |
| 6 | Section split: if S3 r1 has a beyond piece partly behind a cut part, the script draws two pieces (render_section dashes whole pieces only) | SW NOTE 3 |
| 7 | Record currency compares keys only. The spec SHA-256 in records and an S3-3 comparison, for sketches after S3 | Loftsman NOTE 2 |
| 8 | The lever u expressions as `r * sind(jackscrew.angle[2])`; axis X/Y rows in a section at theta 0, 90, 180, 270 only (lint) | Topologist NOTES 2, 3 |

## 5 Code changes

- `docs/sketches/sketch_common.py`:
  - `orphan_predicates` message fixed.
  - `sub_spec` gains `class_by_axes` and `label_home`.
  - New: `class_by_axes_issues` (K7, main Axes); `section_look_issues`, `omitted_row_issues` and `mirror_radial_issue` (K8).
  - Section convention clause for unsectioned straddle; `points_issues` apart senses.
  - K4 refuses an off-home label; `is_area` excludes FancyArrowPatch.
  - PRED_TARGET and PLAN_PREDS gain `mirror_about_radial`.
- `docs/sketches/checks_s3.py`:
  - S3 verdict per pair (`s3v`); face overlap above TOL_Z; `true_cut_issues`; exact symmetry range `_c_range`.
  - K_CHECKS dropped; STUB_EXPECT (SYM-P guard) and STUB_CAUSE (SYM text) updated.
- `docs/sketches/check_sketch.py`: SYM_FIELDS (z_rule, place); `sym_keys_premise` (SYM-P), appended to runs of a spec with `chains`.
- `docs/sketches/s3_spec.yaml`: `class_by_axes: {inset_plan: N}` on three neighbour entries (Correction 2).
- `docs/sketches/fixtures/s3_fixtures.py`:
  - 32 builders added (one per new control) plus helpers; `_post_p6_specs` without key union.
  - Temporary-directory reuse and cleanup.
- `docs/sketches/fixtures/manifest.yaml`: 32 entries; `gameplan_line` by check row.
- Run outputs: `wip/fixtures/controls_results.json`, `wip/s3_checks_r0.json`, `wip/baseline_red.json`, `wip/s1_checks_r7.json`, `wip/s2_checks_r8.json`, `wip/p5f_pre/` (pre-change copy, `controls_results_prechange.json`, `deletions.json`).

## 6 Gameplan lines to change

Apply after the P4 items (`step1.3_engineer_redfirst.md` section 7) and the Topologist P5T items. The Loftsman P5L items 1 to 3 are replaced by items 7 to 9 below. His item 4 (l.650, F1) is held until Sean rules on a seat. Old and new are exact fragments of the named line.

1. l.146 (K table pointer, after P4 item 17)
```
Old: 336 controls: Z 88, B 245, smoke 3, all match; 148.4 s at --jobs 12).
New: 336 controls: Z 88, B 245, smoke 3, all match; 148.4 s at --jobs 12). Step 1.3 P5f (research/sean/cr_scratch/step1.3_engineer_redfirst_fixes.md; Software Engineer FIX 1 to 5, Loftsman FIX 1 to 6, Topologist FIX 1 to 7) added K3-B11, K4-Z6, K4-B21, K4-B22, K5-B36, K7-Z18, K7-B35, K8-Z15, K8-B64 to B76, S3-2-B2, S3-3-B4 to B11, SYM-P-Z, SYM-P-B1 (368 controls: Z 92, B 273, smoke 3, all match; 157.6 s at --jobs 12).
```
2. l.137 (K3, after P4 item 2)
```
Old: K3-B10 a third Axes with no declared id in the S3 figure (TP-7, 1.3 P4) |
New: K3-B10 a third Axes with no declared id in the S3 figure (TP-7, 1.3 P4); K3-B11 a third Axes carrying an undeclared id (1.3 P5f) |
```
3. l.138 (K4, after P4 item 5)
```
Old: or for fmt s the key's string value) |
New: or for fmt s the key's string value); K4-Z6 and K4-B21 load_tension_c value_from 254.04 against a printed 300; K4-B22 a label drawn outside its home Axes, refused (1.3 P5f) |
```
4. l.139 (K5, after P4 item 7)
```
Old: B35 lever end 5 low |
New: B35 lever end 5 low; K5-B36 S3 bearing line ending in the journal gap (section form, Topologist P5T FIX 5) |
```
5. l.141 (K7, after P4 item 9)
```
Old: a per-Axes result carries tests_axes beside tests |
New: a per-Axes result carries tests_axes beside tests; 1.3 P5f: a neighbour's class_by_axes sets its class in that Axes; an N override needs the pair at its base class C, F or G in another declared Axes of the figure (premise lint, Topologist P5T FIX 7, F5), K7-Z18, K7-B35 |
```
6. l.142 (K8, after P4 item 11)
```
Old: predicates points, look_direction, axes_not_inverted |
New: predicates points, look_direction, axes_not_inverted; 1.3 P5f: orphan predicate (K8-B64); look arrows toward +X (B65); section look sign, (u x z) . toward = -1 so section_yz looks toward -X, any other toward a spec error (B66); convention clauses B67 to B72; unsectioned row straddles x = 0 (B73); an area row absent from the section Axes lies wholly in front or past one profile width (B74); points apart needs opposite senses on one line (B75); mirror_about_radial in plan (K8-Z15, B76); a FancyArrowPatch draws no area |
```
7. SYM row inserted by P4 item 16 (after l.144)
```
Old: rows of a and b equal the c row (or each other) in z_rule, place and keys with the angle index swapped
New: rows of a and b equal the c row (or each other) in z_rule and place with the angle index swapped (keys not compared: keys_read holds spec_keys and every key check_stack reads, so equal place and z_rule give equal geometric keys; premise check SYM-P; Loftsman 1.3 (c) P5L F4 ruling, 1.3 P5f)
```
```
Old: | SYM-Z the three specs in the post-P6 state (18 pairs) |
New: | SYM-Z the three specs in the post-P6 state, key lists as signed (18 pairs); SYM-P-Z keys_read covers every key read by place and z_rule of every SYM row (S1, S2, S3) |
```
```
Old: B3 s2 nut_housing_b z_max + 1 |
New: B3 s2 nut_housing_b z_max + 1; SYM-P-B1 S3 keys_read from spec_keys alone with jackscrew.top_guide_z removed from every keys list |
```
8. l.287 (S3-2, after P4 item 19)
```
Old: retract 2.26 and stall 1.18 against SF 3) |
New: retract 2.26 and stall 1.18 against SF 3); S3-2-B2 guide bearing drawn 10 above its row, drawn span 880.00 against 870.00 (1.3 P5f; Software Engineer FIX 2, Loftsman FIX 4) |
```
9. l.288 (S3-3, rule column, original text)
```
Old: symmetry premise lint (anchor, anchor locknut, screw, nut, nut-housing rows; P4; Loftsman 1.3 (b) R1), K7 C |
New: symmetry premise lint (anchor, anchor locknut, screw, nut, nut-housing rows equal in z_rule and place with the angle index swapped, keys not compared; the c links between the counterparts, p(x_c) to p(y_c) - 1 along chain c, must pass; P4; Loftsman 1.3 (b) R1, 1.3 (c) P5L F4, NOTE 1); a pair an S3 certifier names is judged by the section K7 in every chain it occurs in and a failing section test opens it there whatever a record certifies (premise: S3-certified rows drawn as their true cut, section_u, section, an axis-Z round row symmetric about x = 0, or a footprint centred on and symmetric about x = 0, linted); a named face needs an overlap in u above 0.05 (Loftsman 1.3 (c) P5L FIX 1 to 3; 1.3 P5f), K7 C |
```
l.288 (S3-3, B column, after P4 item 20)
```
Old: a, b links by symmetry from c under SYM) |
New: a, b links by symmetry from c under SYM); 1.3 P5f B per branch: named face off its z (S3-3-B4), SYM failing (B5), a c link between the counterparts open (B6), a record pair in a non-C state (B7) or at another pose only (B8), the section F on receiver\|base_plate opening it in chains c, a, b (B9), a row of an S3-certified pair off the plane (B10), a face meeting only at a corner (B11) |
```
10. l.275 (detail 1.3 Script line, after P4 item 21)
```
Old: s3 --rev 0 red by cause 15/15 in wip/baseline_red.json).
New: s3 --rev 0 red by cause 16/16 in wip/baseline_red.json; SYM-P a green guard, 1.3 P5f).
```
11. l.295 (TP-7 carried, after Topologist P5T item 1)
```
Old: mirror_about_radial in plan, neighbour class_by_axes) to P5f.
New: mirror_about_radial in plan, neighbour class_by_axes) to P5f. Closed at P5f (step1.3_engineer_redfirst_fixes.md): every FIX of the Software Engineer (1 to 5), the Loftsman (1 to 6) and the Topologist (1 to 7) with its Z and B, each B red on the P4 code or by branch deletion; 368 controls, 157.6 s; raisers sign from that file.
```
12. l.607 (Design Notes 20 TP-7 row, after Topologist P5T item 2)
```
Old: section rules FIX 1 to 7 to P5f (step1.3_topologist_redfirst_signoff.md)
New: section rules FIX 1 to 7 to P5f (step1.3_topologist_redfirst_signoff.md), closed at P5f (step1.3_engineer_redfirst_fixes.md), Topologist re-check pending
```
13. l.650 (S4-a row): none in this pass (the Loftsman's P5L item 4 waits for Sean's ruling on a receiver seat, applied at P6).
