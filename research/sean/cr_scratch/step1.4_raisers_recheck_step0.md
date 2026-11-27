# Step 1.4 P0r: raiser re-checks after P0f (Software Engineer, Designer, Topologist, Loftsman)

## Corrections to the brief

1. The S2 keepout firing does not survive the P6 S2 batch at its present anchor. The other two S2 anchors (base_plate label_theta 5, screw_b label_theta 28) re-stack the right label column. The keepout text moves from (366.84, -56.89) to (366.84, -47.68), and the leader angle changes from 171.54 to 173.38 deg (MEASURED, `p0r/keep_meas.py`). At the new angle it is 3.33 deg off the pinion_b toe edge, 0.81 data mm away, and runs 18.3 mm within D 1.77. It reads clean only because of the 2 deg angle test, a margin of 1.33 deg (MEASURED). The Designer still gives it an anchor (section 2.3).
2. K4-B9 re-count, P0f table: "2 to 3, r6 core_750 leader along the stroked pinion_b outline (TP1.4-1)". With the stroked-edge clause of `strokes_boundary` deleted, K4-B9 still fires 3 with the same third reason (MEASURED, mutant top_stroke). In S1 side view the pinion_b firing goes through a filled or hatched face, so its cause is the L1 paper D (1.0 to 4.67 data mm on S1), not TP1.4-1. The count is right. The attributed cause is wrong.

Method, all four sections: every mutant is a scratch copy of the live tree (`D:\Unleashed Robotics\_scratch\cutjig\open14\p0r\deltest.py`, results `deltest.json`), with one branch or datum deleted. Each mutation differs from the Engineer's P0f mutants. Only the FIX's controls run on it (`check_sketch.py --controls --manifest`). On the unmutated copy, all 37 controls used match (MEASURED, run "live"). "Caught" means at least one named control mismatches on the mutant.

## 1 The Software Engineer

Signed from the P0f red-first table (pre-change and mutant columns) plus one deletion test of my own per FIX.

| FIX | P0f evidence | My deletion (scratch) | Result (MEASURED) | Verdict |
|---|---|---|---|---|
| 1 --fast call site | RUN-B5 red with the call-site argument dropped | `controls_dst`: `not fast` removed from the record branch | RUN-B5: partial False, full True, mismatch; RUN-Z3 returns ('record', ...), mismatch | CLOSED |
| 2 fast tier | 77 ids, 29.1 s, 77/77; FAST-B2, B3 red by clause deletion | S3-FULL deleted from the live fast.yaml | FAST-Z fires "smoke S3-FULL not in the fast tier", mismatch | CLOSED |
| 3 stale_deps branches | DEPS-B7, B8 red by append deletion | spec kind removed from the spec/script loop | DEPS-B8 and DEPS-B3 read clean, mismatch | CLOSED |
| 4 s3 r7 exempt | DEPS-Z3, B5 re-planted, B9 | s3_checks_r7.json entry deleted from deps_exempt.json | DEPS-Z3 fires "deps not recorded", DEPS-B10 reason lacks the S3 line: both mismatch | CLOSED |
| 5 refusal bypass | M1C-B5 red with the step 0 string test | samefile ancestor loop emptied (spelling-free test kept) | M1C-B5 1 of 2 (UNC admin-share form written), mismatch. Second deletion, the spelling-free test removed and samefile kept: M1C-B5 still 2, M1C-B3 (key in a not-yet-made out folder) clean, mismatch. Each half has a B | CLOSED |
| 6 clip-region firing | K4-B38 red with the region path at 0 | `reg.contains` replaced by False | K4-B38 clean, mismatch; K4-Z11 clean | CLOSED |
| 7 own-row relief | K4-Z12 red with the filter deleted | "part edge" dropped from OWN_ROW_FAMILIES | K4-Z12 fires "part edge of frame_upper_c", mismatch | CLOSED |
| 8 DR4-2 sub-conditions | K8-B93, B94 red by test deletion | (a) arrowstyle compared on class only; (b) class test widened to admit Angle3 | (a) K8-B93 clean, mismatch. (b) K8-B94 still fires, match: **deletion test passes** | B93 CLOSED; B94 **OPEN, class repeat** |
| 9 rule (j) branches | K4-B40 to B42 red by return deletion; K4-B39 pre-change only | the step 0 line `if "mu" not in txt: return []` restored | K4-B39 1 of 2, mismatch | CLOSED |

**FIX 8 (b), class repeat (the orchestrator rules).**
- **Defect.** K8-B94 plants `angle3`. Angle3 has no `rad`, so `rad is None` fires it whatever the class test does. The class test `type(cs_).__name__ != "Arc3"` has no B of its own. A connection style that carries rad 0 and is not straight passes once the class test is gone: `angle` with rad 0 (a corner), or `arc`.
- **Remedy dry run** (`p0r/b94r.py`, `b94r.json`, MEASURED): the span_lt terminator with connectionstyle `angle,angleA=90,angleB=0,rad=0`.
  - Live code: fires 1, "connection style Angle rad 0 is not straight".
  - Class test deleted: clean.
- **Fix.** Re-plant K8-B94 on that style, reason "connection style Angle rad 0 is not straight", or add it as K8-B95. Fixture change only. No rule or code change.

Signatures:
- Fast tier as ruled (77 ids, FAST-Z family scope): SIGNED.
- Deps branch with the three exemption entries carrying deps: SIGNED.
- M1C refusal by identity and spelling-free path: SIGNED.
- Rule (l) clip and own-row branches: SIGNED.
- Rule (j) branch set: SIGNED.
- DR4-2 controls: NOT SIGNED until the K8-B94 re-plant lands. The rule text stands.

NOTE 1 to 6 as taken or carried at P0f: no objection. No new findings from the fix pass.

Verdict: 8 CLOSED + FIX 8 (a) CLOSED; FIX 8 (b) OPEN, class repeat, with a dry-run-clean remedy.

## 2 The Designer (spawn B)

### 2.1 FIX L1 to L4 and J1

| FIX | P0f evidence | My deletion (scratch) | Result (MEASURED) | Verdict |
|---|---|---|---|---|
| L1 paper thresholds | K4-B43 clean on pre-change; K4-B44 premise; K4-Z10 | `collinear_scale` returns 1.0 / 5.0 data mm (the step 0 reading) | K4-B43 clean, mismatch; K4-Z10 clean | CLOSED |
| L2 drawn line | K4-B45 to B47 clean on pre-change | drawn-line branch of `collinear_lines` set to `elif False` | K4-B45, B46, B47 clean; K4-Z4 2 of 4 (guide_b ×2 lost): all mismatch | CLOSED |
| L3 own-line relief | K4-B53 to B56, one per term, red by term deletion | relief test in `collinear_issues` set to `False and ...` | K4-Z13 fires on height_target (z 2000, 4 poses), mismatch | CLOSED |
| L4 leader family | K4-B50 to B52 clean on pre-change | leader list in `collinear_issues` filtered to empty | K4-B50, B51, B52 clean, mismatch | CLOSED |
| J1 bare literal | K4-B39 fires 1 on '343.18 / 282.21' | J1 count test `n_ > 1` raised to `n_ > 2` | K4-B39 1 of 2, mismatch | CLOSED |

### 2.2 L1 ruling: 0.4152 / 2.0756 paper mm SIGNED

- **Premise.** My FIX L1 premise was that the paper constants reproduce the signed 1.3 r6 section values, 1.0 and 5.0 data mm. The 0.4 / 2.0 I wrote were that conversion rounded down, and they break the premise.
- **Hand check** at 150 dpi (5.905512 px per paper mm) and 2.45136 px per data mm on the S3 section (all DERIVED):

| Constant | Paper mm | Data mm on the S3 section |
|---|---|---|
| D at 0.4 | 0.4 x 5.905512 / 2.45136 | 0.96363 |
| Premise D | 2.45136 / 5.905512 = 0.41510 | 1.0 |
| Premise R | 2.07549 | 5.0 |
| D at 0.4152 | 0.4152 | 1.00025 |
| R at 2.0756 | 2.0756 | 5.00027 |

- **Dry run at 0.4 / 2.0** (scratch, MEASURED, mutant des_l1_ruling_04):
  - K4-B28 and K4-B29 drop to 3 of 4. The r95 guide_c leader along span_lt:ext (31 mm at 1.00 data mm, the M1 S3 r5 F1 defect) goes unseen.
  - K4-Z3, Z4 and Z8 keep their counts (3, 4, 1). Only the D printed in the reasons and the run lengths change (screw_b 75.8 against 78.8).
  - K4-Z10 is clean at both values.
- **Ruling.** Live firings are the same at both values, and only 0.4152 / 2.0756 holds the known defect. SIGNED: COLLINEAR_PAPER_MM 0.4152, COLLINEAR_PAPER_RUN_MM 2.0756.
- **Thresholds per Axes** (D / R in data mm, MEASURED at P0f, my keepout run reads S2 1.771 / 8.855):

| Axes | D | R |
|---|---|---|
| S1 side | 4.67 | 23.35 |
| S2 plan | 1.77 | 8.86 |
| S3 section | 1.00 | 5.00 |
| S3 inset | 1.54 | 7.72 |

- **Limit.** A leader at exactly 1.0000 data mm is held by a margin of 0.00025 mm, so the constant is a boundary value. A future figure scale or dpi change re-derives the section reading through `collinear_scale`. It does not move the paper constant.
- **My P0D anchor margins at the signed constants** (DERIVED from P0D section 4 and P0f section 1): S1 drill_tube 11.66 > 4.67, S2 screw_b 3.9 > 1.77, S3 inset screw_b 3.9 > 1.54. P6 re-runs them in the drawn revisions.

### 2.3 Keepout anchor for the P6 S2 r10 batch: `label_theta: 355` (from 350)

Dry run in the scratch ws (`p0r/ws`, P0f code at 0.4152 / 2.0756). The S2 spec carries base_plate label_theta 5, screw_b label_theta 28 and the keepout candidate. Each variant ran `s2_plan.py --rev 98` and `check_sketch.py s2 --rev 98` (`keepout_scan.py`, `keepout_scan.json`). Keepout leader geometry is from `keep_meas.py`, `keep_meas.json`. All MEASURED.

| keepout label_theta | S2 checks | Leader (text to anchor) | Nearest pinion_b edge (angle, distance, run within D) | Reading |
|---|---|---|---|---|
| 350, live spec (no batch) | K4 fail (3) | (366.84, -56.89) to (84.82, -14.96), 171.54 deg | 1.49 deg, 0.32 mm, 26.8 mm | the TP1.4-1 firing |
| 350 with the batch | 18/18 | (366.84, -47.68) to (84.82, -14.96), 173.38 deg | 3.33 deg, 0.81 mm, 18.3 mm | clean by angle only; refused |
| 345 | 18/18 | to (83.17, -22.29), 174.88 deg | 4.83 deg, 3.57 mm, 0 | clean |
| **355** | **18/18** | to (85.83, -7.51), 171.86 deg | 1.81 deg, 7.92 mm, 0 | **clean; separation 4.5 D** |
| 340 | 18/18 | to (85.95, 5.11) | none within 5 deg | clean; anchor jumps past theta 0 in the stacking |
| 0 | 17/18 | n/a | n/a | K4 fail: drill_head 12.5 mm along gear:ticks (a new firing) |

- **Choice: 355.** It is the least move from the signed M1 r1 F5 anchor. It keeps the leader 7.92 data mm (about 11 px) clear of the dashed toe edge along its whole length, and it passes every S2 check with the other two batch anchors.
- **Crop** `p0r/crop_keepout_355.png`: the keep-out leader reads as its own line above the pinion_b toe, between the cutter and ring OD leaders, with no merge.
- **Live firing set.** With the three S2 anchors, the S2 rule (l) firing set is empty: K4-Z3 can return to Z at P6.

### 2.4 Signatures

| Item | Signature |
|---|---|
| Rule (l) at class scope, with FIX L1 (0.4152 / 2.0756), L2, L3, L4 | SIGNED |
| Rule (j) with J1 and the branch B (K4-B39 to B42) | SIGNED |
| DR4-2 | unchanged (signed at P0D) |

NOTEs N-l1 to N-l5 and N-j1 are carried as listed at P0f. No new findings from the fix pass.

## 3 The Topologist

| FIX | P0f evidence | My deletion (scratch) | Result (MEASURED) | Verdict |
|---|---|---|---|---|
| TP1.4-1 part-edge set | K4-B48, B49 clean on pre-change; live S2 +1 (keepout, 26.8 mm at D 1.77) | stroked-edge clause of `strokes_boundary` set to `False and ...` (filled and hatched kept) | K4-B48, B49 clean; K4-Z3 2 of 3 (keepout lost); K4-B30 2 of 3 (nut_screws_c outline lost): all mismatch | CLOSED |

Implemented predicate against my P0T statement:
- `strokes_boundary` admits a visible Patch with a filled face, a hatch, or a stroked edge (linewidth > 0, edge alpha > 0, line style not none), and excludes FancyArrowPatch.
- Patch rings go to "part edge". Line2D and Collection of non-reference rows go to "drawn line", the Designer's L2 name for my "part line" family. Each counts inside the closure of its clip region (`_run_near_vis`, 0.05 across).
- Own-row exclusion covers both families (K4-Z12).

This is E_f as written. SIGNED.

Hand re-check of the live S2 firing at the signed D:
- Leader 171.54 deg against the edge 170.05 deg: 1.49 deg ≤ 2.
- Separation 0.32 at the toe corner. Run 26.8 mm in my measurement, against 25.8 mm at P0T, which was measured at D 1.0. The P0f D 1.77 lengthens the run.

NOTE (no FIX): the K4-B9 re-count cause in the P0f table is L1, not TP1.4-1 (Correction 2).

TP1.4-2 (wingnut sweep to a reference row) was not a P0f item. It stays carried to P6 (S1 r9, S3 r8). The NOTE dispositions TP1.3-4 to -7, -9, -16 to -18 stand.

Verdict: TP1.4-1 CLOSED and SIGNED; 0 open.

## 4 The Loftsman

| FIX | P0f evidence | My deletion (scratch) | Result (MEASURED) | Verdict |
|---|---|---|---|---|
| 1 exemption window | DEPS-B10 red with name-only entries; DEPS-B13 premise B | certifiers list emptied in the s3_checks_r7.json entry of deps_exempt.json (entry and its other deps kept) | DEPS-B10 1 of 2 (S3 r7 line lost), mismatch; DEPS-Z3 clean | CLOSED |
| 2 SYM specs (spec_read) | DEPS-B11 red with the stale_deps spec_read loop deleted | record side: `specs_read = []` in run_sketch | DEPS-Z2 fires "deps spec_read [] against [s1_spec.yaml a585abc3..., s2_spec.yaml ef399381...]", mismatch | CLOSED |
| 3 S2 mass report | DEPS-Z4 red with the certifier setting deleted; DEPS-B12 | `ctx.certifier_files["s1"]` assignment removed in checks_s2 (certifier kept) | DEPS-Z4 fires: certifier s1 r8 recorded with files () against (s1_mass_report_r8.json), mismatch | CLOSED |

Each FIX now has a red on both sides of the branch: the record side (my deletions 2, 3) and the stale side (the Engineer's).

Scratch `--stale` on the unchanged copy (`p0r/ws`, MEASURED):
- key branch: 3 records, 0 differences;
- deps branch: 3 exempt with the deps of their re-records, 0 differences;
- X1 pass, 70 shared rows.

Premise at the S1 r9 accept: S3 r7 and S2 r9 both read "certifier superseded" (DEPS-B10, planted 2, match). The accept order in P0f section 5 item 3 follows: S2 r10 and S3 r8 are each re-run after S1 r9 is accepted and before their own accept.

NOTEs N1, N3, N4 carried. N2 (`--accept` does not test deps) is with the orchestrator, as P0f lists it.

Signature: the deps branch against the S3-3 certifier semantics, SIGNED. Verdict: FIX 1 to 3 CLOSED; 0 open.

## Gameplan lines to change

1. detail 1.0, K table, K4 row (l.138). Supersedes research/sean/cr_scratch/step1.4_engineer_step0_fixes.md item 2.

Old:

```
| K4 | Labels carry their dimension (8.4.2): each spec row with `label` has one annotation containing its name and the number formatted from its key; a label number that differs from the key value fails; from S2 and S1 r5 on, the spec figure_note and the drawn Text note:figure_note name the head (text before " (" or " at ") of every not_drawn part; only a revision accepted before the rule with no not_drawn entry is exempt (1.2 (c), Designer 1.2 (b) FIX 3, Designer 1.2 (c) FIX R1); every label leader ends on its row's ink within 0.05 and no two leaders cross; a concentric row may set label_theta, the leader azimuth (1.2 (h), Designer M1 r1 F4, F5); labels draw above every area (z order 100); no area artist (filled or hatched) of another row is drawn above a leader where it runs or above the row's ink at the anchor; at most a quarter of the samples in the last quarter of a leader lie in other rows' hatch, and place_labels re-anchors on the row's ink until it holds (1.2 (h) r3, Designer M1 S2 r2 F1, S1 r6 F1); red-first for K4-B9 to B11 MEASURED by branch deletion (Designer sign-off r3); a row may set label_side: left, a left label column under the same rules (1.2 (h) r4, Designer M1 S2 r3 N1); 1.3 P1R: plan labels are placed by one placer (sketch_common.place_plan_labels; candidates in order: label_side column then the other, label_theta ray hit, column default anchor, ink samples at most 2 mm apart; first candidate passing every leader rule, re-judged after column stacking; left-column text clear of the y tick labels); (e) only true outlines of rows higher than the labelled row by more than 0.05 (zones: every outline) count; (e1) a row with visible ink (renderer split, certified by K8 cover; a stand-in's convention line is visible ink where no cover contains it) anchors on visible ink and its leader's last quarter lies outside every counted outline that does not enclose the anchor; (e2) a wholly hidden row anchors on its hidden ink and its last quarter lies outside every counted outline that does not enclose the anchor (Design Notes 30; Designer P1Rd FIX D1); an outline encloses for (e1) and (e2) only when the anchor and every point within 0.05 of it lie inside its outer boundary with holes filled (Topologist TP1.3-8); (f) a label with no passing candidate is recorded UNPLACEABLE with its candidate table in the K4 record and fails with reason "unplaceable", no silent fall-back; (g) the drawn label of a wholly hidden row contains "under " and the name of a counted row whose outline contains or encloses the anchor; (h) any two plan leaders that do not cross, anchor ends included, keep at least 4.0 mm apart (DECLARED, Designer P1Rf re-check FIX D4), judged and placed as a crossing is | Fixture with all labels from keys; K4-Z2 live S2; K4-Z3 live S2 drawn by s2_plan.py; K4-Z4 live S1 drawn by s1_side_poses.py; K4-Z5 S3 span_lt label prints its expr value 870 | B1 label without a number; B2 label "tube OD 150" against `drill.tube_od` 152.4; K4-B4 drawn note without the LM20UU bushing; K4-B5 a not_drawn part in neither note; K4-B6 S1 r5 spec with not_drawn and no figure_note (FIX R1); K4-B7 sightline leader at the r1 anchor, off the line; K4-B8 r1 concentric anchors, three crossings; K4-B9 S1 core 750 at the r6 anchor (end in hatch); K4-B10 an area drawn over a leader; K4-B11 an area of another row over an anchor (with (e1) on the hidden ink); K4-B12 the descent-stop leader at the r4/r5 anchor (inside tie b); K4-B13 a pad under an opaque lid (unplaceable); K4-B14 ring label at the r6 anchor on hidden rim inside tie a (e1); K4-B15 drill_head label without its "under ring gear" suffix (g); K4-B16 gear outline planted as an open C, not enclosing the cutter anchor (e2, g); K4-B17 ring label anchored 0.028 mm outside tie a, last quarter 41.3 mm inside it (TP1.3-8); K4-B18 tie a label anchored on its phantom line under a planted nearer disk (e1, Designer FIX D5); K4-B19 the S2 r7 tube OD, base plate and cutter leaders, 1.87 mm apart (h, Designer FIX D4); K4-B8 re-planted at 1.3 P1R and P1Rf; K4-B7, B8, B10 to B12, B14 counts re-read at P1R to P1Rf2; K4-B20 span_lt label prints its key value 1150 where the spec names expr (1.3 P4: a label prints label.expr, a label.value_from spec value, or for fmt s the key's string value); K4-Z6 and K4-B21 load_tension_c value_from 254.04 against a printed 300; K4-B22 a label drawn outside its home Axes, refused (1.3 P5f); (i) on a script-drawn figure no drawn leader crosses a text box and no two text boxes overlap (labels, notes, tick labels, titles; boxes shrunk 1 px): K4-B23 text planted on two leaders, K4-B24 text planted on a label (1.3 (h) r2, Designer M1 S3 r1 F2, F3); K4-B7, B8, B18 re-counted 4, 7, 3; (j) a label printing a load reads checks_s3.loads() from the keys (load_comp_c cases, load_tension_c), and every load_cases per_screw literal agrees with loads() within 0.005 N (K4-Z7, Z8, B25 static 79, B26 ring.mass + 4 kg); (k) a row declaring label_anchor_frac ends its leader at that anchor, frac in [0, 1] (K4-B27, B28); (l) section views: no leader runs within 2 deg and 1.0 mm of a reference line or gridline over more than 5 mm (K4-B29, B30); (m) a stack_z label prints check_stack nut_z at its pose within 0.05 (K4-B31) (M1 S3 r4 F1, r5 Rule 1, Rule 2, F1, F2; 1.3 (h) r5, r6; rules (j) to (m) signed by the r6 fresh M1 reviewer, s3_visual_gate_r6.md; (l) covers reference lines and gridlines only, part edges and the S1/S2 views carried, Manager 1.3 close) |
```

New:

```
| K4 | Labels carry their dimension (8.4.2): each spec row with `label` has one annotation containing its name and the number formatted from its key; a label number that differs from the key value fails; from S2 and S1 r5 on, the spec figure_note and the drawn Text note:figure_note name the head (text before " (" or " at ") of every not_drawn part; only a revision accepted before the rule with no not_drawn entry is exempt (1.2 (c), Designer 1.2 (b) FIX 3, Designer 1.2 (c) FIX R1); every label leader ends on its row's ink within 0.05 and no two leaders cross; a concentric row may set label_theta, the leader azimuth (1.2 (h), Designer M1 r1 F4, F5); labels draw above every area (z order 100); no area artist (filled or hatched) of another row is drawn above a leader where it runs or above the row's ink at the anchor; at most a quarter of the samples in the last quarter of a leader lie in other rows' hatch, and place_labels re-anchors on the row's ink until it holds (1.2 (h) r3, Designer M1 S2 r2 F1, S1 r6 F1); red-first for K4-B9 to B11 MEASURED by branch deletion (Designer sign-off r3); a row may set label_side: left, a left label column under the same rules (1.2 (h) r4, Designer M1 S2 r3 N1); 1.3 P1R: plan labels are placed by one placer (sketch_common.place_plan_labels; candidates in order: label_side column then the other, label_theta ray hit, column default anchor, ink samples at most 2 mm apart; first candidate passing every leader rule, re-judged after column stacking; left-column text clear of the y tick labels); (e) only true outlines of rows higher than the labelled row by more than 0.05 (zones: every outline) count; (e1) a row with visible ink (renderer split, certified by K8 cover; a stand-in's convention line is visible ink where no cover contains it) anchors on visible ink and its leader's last quarter lies outside every counted outline that does not enclose the anchor; (e2) a wholly hidden row anchors on its hidden ink and its last quarter lies outside every counted outline that does not enclose the anchor (Design Notes 30; Designer P1Rd FIX D1); an outline encloses for (e1) and (e2) only when the anchor and every point within 0.05 of it lie inside its outer boundary with holes filled (Topologist TP1.3-8); (f) a label with no passing candidate is recorded UNPLACEABLE with its candidate table in the K4 record and fails with reason "unplaceable", no silent fall-back; (g) the drawn label of a wholly hidden row contains "under " and the name of a counted row whose outline contains or encloses the anchor; (h) any two plan leaders that do not cross, anchor ends included, keep at least 4.0 mm apart (DECLARED, Designer P1Rf re-check FIX D4), judged and placed as a crossing is | Fixture with all labels from keys; K4-Z2 live S2; K4-Z3 live S2 drawn by s2_plan.py; K4-Z4 live S1 drawn by s1_side_poses.py; K4-Z5 S3 span_lt label prints its expr value 870 | B1 label without a number; B2 label "tube OD 150" against `drill.tube_od` 152.4; K4-B4 drawn note without the LM20UU bushing; K4-B5 a not_drawn part in neither note; K4-B6 S1 r5 spec with not_drawn and no figure_note (FIX R1); K4-B7 sightline leader at the r1 anchor, off the line; K4-B8 r1 concentric anchors, three crossings; K4-B9 S1 core 750 at the r6 anchor (end in hatch); K4-B10 an area drawn over a leader; K4-B11 an area of another row over an anchor (with (e1) on the hidden ink); K4-B12 the descent-stop leader at the r4/r5 anchor (inside tie b); K4-B13 a pad under an opaque lid (unplaceable); K4-B14 ring label at the r6 anchor on hidden rim inside tie a (e1); K4-B15 drill_head label without its "under ring gear" suffix (g); K4-B16 gear outline planted as an open C, not enclosing the cutter anchor (e2, g); K4-B17 ring label anchored 0.028 mm outside tie a, last quarter 41.3 mm inside it (TP1.3-8); K4-B18 tie a label anchored on its phantom line under a planted nearer disk (e1, Designer FIX D5); K4-B19 the S2 r7 tube OD, base plate and cutter leaders, 1.87 mm apart (h, Designer FIX D4); K4-B8 re-planted at 1.3 P1R and P1Rf; K4-B7, B8, B10 to B12, B14 counts re-read at P1R to P1Rf2; K4-B20 span_lt label prints its key value 1150 where the spec names expr (1.3 P4: a label prints label.expr, a label.value_from spec value, or for fmt s the key's string value); K4-Z6 and K4-B21 load_tension_c value_from 254.04 against a printed 300; K4-B22 a label drawn outside its home Axes, refused (1.3 P5f); (i) on a script-drawn figure no drawn leader crosses a text box and no two text boxes overlap (labels, notes, tick labels, titles; boxes shrunk 1 px): K4-B23 text planted on two leaders, K4-B24 text planted on a label (1.3 (h) r2, Designer M1 S3 r1 F2, F3); K4-B7, B8, B18 re-counted 4, 7, 3; (j) a label printing a load reads checks_s3.loads() from the keys (load_comp_c cases, load_tension_c), and every load_cases per_screw literal agrees with loads() within 0.005 N, every number of a stall literal '<v1> / <v2> (mu <m1> / <m2>)' held to F_stall at its mu, and a text per_screw literal with two or more numbers and no mu list fails (K4-Z7, Z8, B25 static 79, B26 ring.mass + 4 kg; 1.4 step 0 K4-B37; Designer P0D FIX J1 and the other stall-literal branches at P0f: K4-B39 to B42); (k) a row declaring label_anchor_frac ends its leader at that anchor, frac in [0, 1] (K4-B27, B28); (l) in every view (side, plan, section) and every declared Axes of a script-drawn figure, no leader (clipped to the Axes box) runs within 2 deg of, and within 0.4152 mm on paper of, a line of the families reference line (every Line2D segment of a reference-line row, the labelled row's own included), gridline (major and minor), part edge (every ring edge of every visible Patch of another row whose boundary is drawn: a filled face, a hatch or a stroked edge, renderer solid and dashed pieces and stand-in outlines included, counted only inside its clip region), drawn line (every segment of every visible Line2D or Collection of another row that is not a reference-line row, counted only inside its clip region) or leader (every other label leader in the Axes) over more than 2.0756 mm on paper (paper mm at the figure dpi, converted per Axes to data mm; equal to the 1.3 r6 S3 section values 1.0 and 5 data mm; premise equal aspect, an Axes without it is reported); relief: a line row's leader that leaves an end of its own open ink away from the ink is exempt against a line that the ink itself runs along under the same test (premise: the line marks the row's own position; Designer P0D FIX L3); hatch strokes, FancyArrowPatch marks, text and the labelled row's own edges and lines are outside the rule (Designer P0D NOTEs N-l2, N-l3; Topologist P0T TP1.4-1) (K4-B29, B30; 1.4 step 0, C1.3-a: K4-Z9 to Z11, K4-B32 to B36; P0f: K4-Z12, Z13, K4-B38, K4-B43 to B56; K4-Z3, Z4, Z8 re-scoped to B as the live red of S2 r9, S1 r8, S3 r7 until P6); (m) a stack_z label prints check_stack nut_z at its pose within 0.05 (K4-B31) (M1 S3 r4 F1, r5 Rule 1, Rule 2, F1, F2; 1.3 (h) r5, r6; rules (j) to (m) signed by the r6 fresh M1 reviewer, s3_visual_gate_r6.md; (l) at class scope from 1.4 step 0, signed with FIX L1 to L4 and rule (j) with FIX J1 at P0D, research/sean/cr_scratch/step1.4_designer_step0_signoff.md; the paper constants 0.4152 and 2.0756 mm applied at P0f (the premise value: 1.0 and 5.0 data mm on the S3 section at 2.45136 px per data mm) and signed by The Designer at P0r, research/sean/cr_scratch/step1.4_raisers_recheck_step0.md; DR4-2 signed with no numeric bound) |
```

2. Design Notes 25, row C1.3-a (l.706). Supersedes research/sean/cr_scratch/step1.4_engineer_step0_fixes.md item 5.

Old:

```
| C1.3-a (carried at the 1.3 close) | K4 rule (l) leader collinearity: (1) global scope, S1 and S2 side and plan views (dry-run fires on S1 r8 height_target leader along the z 2000 gridline; landing it opens S1 r9); (2) part-edge extension in section views (s3_visual_gate_r6.md N1: add every tagged artist edge except the label's own row; live r6 fires 2, r7 clean, MEASURED by the reviewer) | 1.4 (S4) step 0, before the S4 draw; S1 r9 only if Sean takes (1) | The Engineer; The Designer signs; Sean on (1) |
```

New:

```
| C1.3-a (carried at the 1.3 close) | K4 rule (l) leader collinearity: (1) global scope, S1 and S2 side and plan views (dry-run fires on S1 r8 height_target leader along the z 2000 gridline; landing it opens S1 r9); (2) part-edge extension in section views (s3_visual_gate_r6.md N1: add every tagged artist edge except the label's own row; live r6 fires 2, r7 clean, MEASURED by the reviewer) ; 1.4 step 0 (`research/sean/cr_scratch/step1.4_engineer_step0.md`): implemented at class scope (reference lines, gridlines, part edges; side, plan, section; every declared Axes; K4-Z9 to Z11, K4-B32 to B36); dry run on the drawings of record fires S1 r8 4 (height_target on the z 2000 gridline, each pose), S2 r9 3 (plan gridlines y 0, y 260, y 80), S3 r7 1 (inset gridline y 80), reference lines 0, part edges 0 under the implemented area-only set; with the part-edge set of Topologist 1.4 P0T TP1.4-1 (every drawn stroke of another row) S2 r9 fires 1 more (keepout leader 25.8 mm along the dashed hidden toe edge of pinion_b), S1 r8 and S3 r7 0 more (MEASURED, step1.4_topologist_step0_check.md); P0f (`step1.4_engineer_step0_fixes.md`): Designer P0D FIX L1 to L4 and Topologist TP1.4-1 in the rule; live firings S1 r8 4 (drill_tube on gridline z 1350 at start and z 700 at capture_end; guide_b along drawn line pinion_axis_b at load and park), S2 r9 3 (base_plate on gridline y 0, screw_b on gridline y 80, keepout along the dashed pinion_b toe edge), S3 r7 1 (inset screw_b on gridline y 80); height_target and slot_line_c relieved by FIX L3; recorded as expected reds on the r8, r9, r7 re-records; the anchor fixes (label_theta 5 and 28, label_anchor_frac 0.45 and 0.75 with the side-placer change, the L3 relief; keepout label_theta 355 in S2 r10, Designer P0r, dry run S2 18/18) and TP1.4-2 (wingnut sweep to a reference row) land at P6 in S1 r9, S2 r10, S3 r8 | 1.4 (S4) step 0, before the S4 draw; S1 r9, S2 r10, S3 r8 at P6 | The Engineer; The Designer signs (P0D); Sean on (1) |
```
