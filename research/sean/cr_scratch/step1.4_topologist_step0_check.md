# Step 1.4 step 0 check (P0T), The Topologist

## Corrections to the brief

1. The S3 record does not carry the not_drawn band values. K8 records counts only: `[section] 218 predicate(s) hold` (TP1.3-16). The hand margin below is set against the harness value, re-evaluated in scratch from the live spec through `check_stack.eval_expr`, and against the keys_read values in `wip/s3_checks_r7.json`.
2. The Engineer's section 5 and the `collinear_lines` docstring both say "renderer hidden copies included". The implemented set admits `is_area(a)` only, meaning a Patch with a filled face or a hatch. Renderer split pieces are drawn unfilled: 37 clipped outline Patches in S2 r9 main (21 dashed hidden, 16 solid), 22 in the S3 r7 section, 12 in the S3 inset (MEASURED). The set therefore excludes them, and with them every stand-in outline and every unfilled part outline (section 3).

## 1 R2-6 and R2-7

### R2-6: CLOSED

- **Bands.** Both entries now carry their bands as expressions over keys. Values evaluated in scratch (MEASURED):
  - pinions: [-144.0536, -65.0889] and [65.0889, 144.0536]
  - base frame: [-262, -202], [-142, -82], [82, 142], [202, 262]
- **Reach.** The evaluation records in `P.accessed` every key the bands read: pinion.r_toe, pitch_diameter, tooth_count, pitch_angle, outer_diameter, r_heel, hub_length, angle; frame.end_x, frame.support_x; profile.width. All of them are in keys_read of `wip/s3_checks_r7.json`, so a key edit reaches `--stale` through the key branch. A spec edit reaches it through deps.spec.
- **Lint.** `ND_KEY_REF` refuses a band bound that names no dotted key. K8-B90 fires 2 on the re-planted literals.

Hand margin, pinion a at theta 210, toe corner (keys_read values: r_toe 96.54, pitch_diameter 83.33, tooth_count 20, pitch_angle 18.435, outer_diameter 91.24, r_heel 125):

| Quantity | Hand | Harness |
|---|---|---|
| m = 83.33 / 20 | 4.1665 (DERIVED) | |
| sin 18.435 | 0.316228 (= 1/sqrt 10; 18.435 = atan 1/3) | |
| r_in = 96.54 - 4.1665 x 0.316228 | 95.22244 (DERIVED) | |
| hw_in = 45.62 x 95.22244 / 125 | 34.75238 (DERIVED) | |
| x_toe = 95.22244 cos 210 - 34.75238 sin 210 = -82.46505 + 17.37619 | -65.08886 (DERIVED) | -65.0889 (MEASURED) |
| x_outer = 140 cos 210 + 45.62 sin 210 = -121.24356 - 22.81 | -144.05356 (DERIVED) | -144.0536 (MEASURED) |
| margin past the section band, -60 - x_toe | 5.08886 (DERIVED) | 5.0889 (MEASURED) |

- **Toe corner is the band maximum.** The other toe corner is at -99.84 and the outer corners at -98.43 and -144.05 (DERIVED). x_toe is the largest of the four. The band is the true x extent of the trapezoid, and its half-width grows linearly from the cone apex at the gear axis.
- **Base frame.** Margin -60 - (-82) = 22.00 (DERIVED). Equal to the 1.3 value.

### R2-7: CLOSED

- K5-B48 fires 1, reason "arc on screw_c admitted in plan_xy only (view section_yz)".
- With the a1 lines deleted it reads clean (mismatch).
- It also fires on the pre-change code, because the branch existed without a B. Deletion is the red-first evidence. That is the right form here.

## 2 TP NOTE dispositions

| NOTE | Engineer disposition | Verdict |
|---|---|---|
| TP1.3-4 (2.5 mm render resolution) | Stays NOTE; no live part or gap narrower; to S4 (c) | Stands. The S4 holder section (collet slits, holder wall, receiver thread ticks) is the first drawing likely to put a wall or gap under 2.5 mm. S4 (c) measures the narrowest drawn wall and gap before the renderer runs on it. |
| TP1.3-5 (stacked translucent fills) | Stays NOTE (The Designer); to S4 (c) | Stands. |
| TP1.3-6 (UNPLACEABLE after the rounds) | Closed in the P1R code; the rounds-exhausted path has no B; B to S4 (c) | Stands. Under process rule (h) the open branch is named and carried. The B lands with the K4 delta at S4 (c). |
| TP1.3-7 (drawn_region reads private attributes) | Stays NOTE; K4-Z11 exercises it | Stands. Its weight has grown: rule (l) part edges now depend on `drawn_region` for every renderer piece (section 3). On a matplotlib upgrade, K4-Z11 and the FIX TP1.4-1 outline B are the re-check. |
| TP1.3-9 (annulus edge band above width 125) | Stays NOTE; to S4 (c) | Stands. |
| TP1.3-16 (K8 per-predicate record) | To S4 (c) inside the K8 delta | Stands. The record should carry the not_drawn band margins as well: section 1 had to re-derive them because the record holds none. |
| TP1.3-17 (S1 anchor mark.z names the key) | To the P6 S1 r9 batch | Stands. S1 spec l.858 and l.874 still read `jackscrew.anchor_z + jackscrew.anchor_allowance / 2` (MEASURED). |
| TP1.3-18 (S1 lift motor at the circumscribing width) | To the S1 r9 M1 | Stands. |
| TP1.3-20 (wingnut sweep envelope under the part gid) | To the P6 S1 r9 batch | **FIX TP1.4-2**, see below. |

**FIX TP1.4-2 (disposition).**

- TP1.3-20 was raised on S3 r1.
- Both scripts draw the sweep under the `wingnut` gid:
  - `s3_jackscrew_section.py` l.185 to 188;
  - `s1_side_poses.py` l.148 to 152.
- In both live drawings it is one unclipped dashed outline Patch tagged `wingnut` (MEASURED).
- Required routing: the sweep moves to a reference row in S1 r9 and in S3 r8. Both revisions open at P6.
- The dry run is in section 3: with the envelope counted as a part edge of `wingnut`, no leader fires on it in S1 r8 or S3 r7. Moving it to a reference row changes no rule (l) result today.

## 3 Rule (l) part edges

### Predicate

Notation:

- Leader ℓ of row f, clipped to the Axes box, with unit direction t_ℓ.
- For every visible tagged artist a of a row r ≠ f that draws a stroke:
  - γ_a is its drawn path: the ring boundary ∂P_a of a Patch, or the polyline of a Line2D or Collection.
  - C_a is its clip region (the Axes box when it has none).

The part-edge set of f:

  E_f = ∪_a ( γ_a ∩ cl C_a )

Per edge e = [p, p + L t_e] with unit normal n_e, a leader sample q is near when it lies in the slab and the angle sign check holds:

- slab: |n_e · (q - p)| ≤ 1.0 and 0 ≤ t_e · (q - p) ≤ L
- angle: |t_ℓ × t_e| ≤ sin 2°
- drawn: the foot point is in cl C_a, within 0.05 across the edge

The rule fails on any connected run of near samples longer than 5 mm.

What "draws a stroke" admits:

| Admitted | Reason |
|---|---|
| A Patch with a filled face (alpha > 0) | Its boundary is a colour edge. |
| A Patch with a hatch | Its boundary bounds the hatch. |
| A Patch with a stroked edge (linewidth > 0, edge alpha > 0, line style not none) | This is every renderer solid or dashed piece, every stand-in phantom outline and every unfilled part outline. |
| A Line2D or Collection of a non-reference row | Axis lines, floor, slot lines, thread root lines, the bearing line, the lever, the S1/S2 keep-out. |

| Outside E_f | Reason |
|---|---|
| Hatch strokes | Interior to P_a, not on ∂P_a. The K4 hatch rule already governs a leader end in hatch. |
| FancyArrowPatch | Marks, not part boundaries. |
| Text | Not a part boundary. |
| Reference-row lines | Already the reference-line family. |

### Implemented set

`collinear_lines`, sketch_common.py l.2353 to 2366, admits a non-reference artist only when `is_area(a)` holds (fill alpha > 0 or a hatch).

Artists drawn with a stroke and excluded from E_f by the implemented set (live, first pose, MEASURED):

| Drawing (Axes) | Unfilled stroked Patches | Non-reference Line2D / Collection |
|---|---|---|
| S1 r8 (side) | 42 (bracket arms, guide ties (dashed), drill head and tube copies, base_frame, holder, collet, frame_upper_a/_b, guide members, lugs, bushings, nut housings, wingnut sweep) | 8 (anchor_a/_b:line, bore_ceiling, floor, keepout, pinion_axis_a/_b) |
| S2 r9 (plan) | 85, of which 37 are clipped renderer pieces (21 dashed hidden, 16 solid); guide ties dash-dot stand-ins | 13 Line2D + 1 Collection (collet_axis, pinion axes, slot lines, gear:ticks) |
| S3 r7 (section) | 40, of which 22 are clipped renderer pieces (bearing balls, standoffs, top block, wingnut sweep among the rest) | 7 (anchor_bearing_c:line, floor, hold_callout, home_switch_c:lever, pinion_axis_c, screw_c:root) |
| S3 r7 (inset plan) | 20, of which 12 are clipped renderer pieces | 3 (sync_callout) |

**FIX TP1.4-1.**

- **Defect.** The implemented part-edge set is a strict subset of E_f. Its own docstring claims renderer hidden copies, and it misses them. K4-Z9 ("0 part-edge firings in every Axes") is vacuous over the excluded artists. K4-B33, B35 and B36 plant filled quads, so no B reaches the outline or line branch.
- **Fix.** Replace `is_area(a)` in `collinear_lines` with the stroke predicate above, and split the result into two families:
  - "part edge" for Patches;
  - "part line" for Line2D and Collections of non-reference rows.

  The own-row filter covers both. Correct the docstring.
- **Controls.**
  - B (plan, outline): a planted unfilled dashed clipped Patch edge beside a leader.
  - B (side, part line): a pinion_axis-like Line2D of another row beside a leader.
  - Both read clean on the pre-change code.
  - The live S2 firing below is a ready red for the outline branch.

Dry run in scratch (`_scratch/cutjig/open14/p0t/scripts/dry_edges.py`; the implemented rule and the extended rule on the drawings of record, live specs, MEASURED):

| Drawing (Axes) | Implemented | Extended | New firing |
|---|---|---|---|
| S1 r8 (side, 4 poses) | 4 | 4 | none |
| S2 r9 (plan) | 3 | 4 | load/keepout: label leader runs 25.8 mm along part edge of pinion_b |
| S3 r7 (section) | 0 | 0 | none |
| S3 r7 (inset plan) | 1 | 1 | none |

Hand check of the S2 firing (MEASURED from the drawn artists):

| Item | Value |
|---|---|
| keepout leader, clipped | (354.20, -55.01) to (84.82, -14.96), angle 171.54 deg, 272.3 mm |
| pinion_b toe-side edge | (131.06, -22.99) to (99.84, -17.51), angle 170.05 deg |
| angle between them | 1.49 deg (≤ 2) |
| separation at the toe corner x 99.84 | 0.32 mm |
| separation at x 125 | 0.98 mm normal to the edge (DERIVED: leader y -20.93, edge y -21.93; vertical 0.99 x cos 9.95) |
| run along the dashed hidden copy (clip region inside the ring) | 25.8 mm |
| run along the solid copy outside the ring | 1.3 mm |

The scratch crop `crop_s2_keepout.png` shows the leader merged with the dashed pinion edge from x 100 to about 122. The firing goes to the P6 S2 r10 batch with the other three S2 leaders. With the FIX:

- K4-Z3 is planted 4.
- K4-B34 and B35 are planted 5.
- Every K4 B drawn on live S2 gains 1.

Re-counts are the Engineer's at P0f.

Other line kinds, dry run:

- **FancyArrowPatch paths** added as lines: 0 further firings in all four Axes (MEASURED, `dry_arrows.py`).
- **Curves** tested as whole polylines: each stroked ring or line as one polyline (`curve_dry.py`: foot distance ≤ 1.0 mm, angle to the foot segment ≤ 5 deg, a loosened bound that covers chord-to-arc error up to the 5.6 deg vertex angle of a 64-sample r 274 circle; run > 5 mm). The result is two firings in all four Axes. The first is the S2 keepout on pinion_b above. The second is S2 load/drill_head, 7.8 mm along one `gear:ticks` segment: a straight tick between 2 and 5 deg off the leader, which does not fire at the signed 2 deg. No curved outline fires (MEASURED). The Engineer's open item 7 (curves tested edge by edge) has no live case. It stays carried by name.

## 4 Verdicts

| Item | Verdict |
|---|---|
| R2-6 | CLOSED |
| R2-7 | CLOSED |
| TP1.3-4, -5, -6, -7, -9, -16, -17, -18 | Disposition stands |
| TP1.3-20 | FIX TP1.4-2 (route to S1 r9 and S3 r8) |
| Rule (l) part-edge set | FIX TP1.4-1 (stroke predicate; live S2 r9 +1 firing) |

FIX count: 2.

## Gameplan lines to change

1. detail 1.0, K table, K4 row (l.138). Supersedes research/sean/cr_scratch/step1.4_engineer_step0.md item 2.

Old:

```
| K4 | Labels carry their dimension (8.4.2): each spec row with `label` has one annotation containing its name and the number formatted from its key; a label number that differs from the key value fails; from S2 and S1 r5 on, the spec figure_note and the drawn Text note:figure_note name the head (text before " (" or " at ") of every not_drawn part; only a revision accepted before the rule with no not_drawn entry is exempt (1.2 (c), Designer 1.2 (b) FIX 3, Designer 1.2 (c) FIX R1); every label leader ends on its row's ink within 0.05 and no two leaders cross; a concentric row may set label_theta, the leader azimuth (1.2 (h), Designer M1 r1 F4, F5); labels draw above every area (z order 100); no area artist (filled or hatched) of another row is drawn above a leader where it runs or above the row's ink at the anchor; at most a quarter of the samples in the last quarter of a leader lie in other rows' hatch, and place_labels re-anchors on the row's ink until it holds (1.2 (h) r3, Designer M1 S2 r2 F1, S1 r6 F1); red-first for K4-B9 to B11 MEASURED by branch deletion (Designer sign-off r3); a row may set label_side: left, a left label column under the same rules (1.2 (h) r4, Designer M1 S2 r3 N1); 1.3 P1R: plan labels are placed by one placer (sketch_common.place_plan_labels; candidates in order: label_side column then the other, label_theta ray hit, column default anchor, ink samples at most 2 mm apart; first candidate passing every leader rule, re-judged after column stacking; left-column text clear of the y tick labels); (e) only true outlines of rows higher than the labelled row by more than 0.05 (zones: every outline) count; (e1) a row with visible ink (renderer split, certified by K8 cover; a stand-in's convention line is visible ink where no cover contains it) anchors on visible ink and its leader's last quarter lies outside every counted outline that does not enclose the anchor; (e2) a wholly hidden row anchors on its hidden ink and its last quarter lies outside every counted outline that does not enclose the anchor (Design Notes 30; Designer P1Rd FIX D1); an outline encloses for (e1) and (e2) only when the anchor and every point within 0.05 of it lie inside its outer boundary with holes filled (Topologist TP1.3-8); (f) a label with no passing candidate is recorded UNPLACEABLE with its candidate table in the K4 record and fails with reason "unplaceable", no silent fall-back; (g) the drawn label of a wholly hidden row contains "under " and the name of a counted row whose outline contains or encloses the anchor; (h) any two plan leaders that do not cross, anchor ends included, keep at least 4.0 mm apart (DECLARED, Designer P1Rf re-check FIX D4), judged and placed as a crossing is | Fixture with all labels from keys; K4-Z2 live S2; K4-Z3 live S2 drawn by s2_plan.py; K4-Z4 live S1 drawn by s1_side_poses.py; K4-Z5 S3 span_lt label prints its expr value 870 | B1 label without a number; B2 label "tube OD 150" against `drill.tube_od` 152.4; K4-B4 drawn note without the LM20UU bushing; K4-B5 a not_drawn part in neither note; K4-B6 S1 r5 spec with not_drawn and no figure_note (FIX R1); K4-B7 sightline leader at the r1 anchor, off the line; K4-B8 r1 concentric anchors, three crossings; K4-B9 S1 core 750 at the r6 anchor (end in hatch); K4-B10 an area drawn over a leader; K4-B11 an area of another row over an anchor (with (e1) on the hidden ink); K4-B12 the descent-stop leader at the r4/r5 anchor (inside tie b); K4-B13 a pad under an opaque lid (unplaceable); K4-B14 ring label at the r6 anchor on hidden rim inside tie a (e1); K4-B15 drill_head label without its "under ring gear" suffix (g); K4-B16 gear outline planted as an open C, not enclosing the cutter anchor (e2, g); K4-B17 ring label anchored 0.028 mm outside tie a, last quarter 41.3 mm inside it (TP1.3-8); K4-B18 tie a label anchored on its phantom line under a planted nearer disk (e1, Designer FIX D5); K4-B19 the S2 r7 tube OD, base plate and cutter leaders, 1.87 mm apart (h, Designer FIX D4); K4-B8 re-planted at 1.3 P1R and P1Rf; K4-B7, B8, B10 to B12, B14 counts re-read at P1R to P1Rf2; K4-B20 span_lt label prints its key value 1150 where the spec names expr (1.3 P4: a label prints label.expr, a label.value_from spec value, or for fmt s the key's string value); K4-Z6 and K4-B21 load_tension_c value_from 254.04 against a printed 300; K4-B22 a label drawn outside its home Axes, refused (1.3 P5f); (i) on a script-drawn figure no drawn leader crosses a text box and no two text boxes overlap (labels, notes, tick labels, titles; boxes shrunk 1 px): K4-B23 text planted on two leaders, K4-B24 text planted on a label (1.3 (h) r2, Designer M1 S3 r1 F2, F3); K4-B7, B8, B18 re-counted 4, 7, 3; (j) a label printing a load reads checks_s3.loads() from the keys (load_comp_c cases, load_tension_c), and every load_cases per_screw literal agrees with loads() within 0.005 N (K4-Z7, Z8, B25 static 79, B26 ring.mass + 4 kg); (k) a row declaring label_anchor_frac ends its leader at that anchor, frac in [0, 1] (K4-B27, B28); (l) section views: no leader runs within 2 deg and 1.0 mm of a reference line or gridline over more than 5 mm (K4-B29, B30); (m) a stack_z label prints check_stack nut_z at its pose within 0.05 (K4-B31) (M1 S3 r4 F1, r5 Rule 1, Rule 2, F1, F2; 1.3 (h) r5, r6; rules (j) to (m) signed by the r6 fresh M1 reviewer, s3_visual_gate_r6.md; (l) covers reference lines and gridlines only, part edges and the S1/S2 views carried, Manager 1.3 close) |
```

New:

```
| K4 | Labels carry their dimension (8.4.2): each spec row with `label` has one annotation containing its name and the number formatted from its key; a label number that differs from the key value fails; from S2 and S1 r5 on, the spec figure_note and the drawn Text note:figure_note name the head (text before " (" or " at ") of every not_drawn part; only a revision accepted before the rule with no not_drawn entry is exempt (1.2 (c), Designer 1.2 (b) FIX 3, Designer 1.2 (c) FIX R1); every label leader ends on its row's ink within 0.05 and no two leaders cross; a concentric row may set label_theta, the leader azimuth (1.2 (h), Designer M1 r1 F4, F5); labels draw above every area (z order 100); no area artist (filled or hatched) of another row is drawn above a leader where it runs or above the row's ink at the anchor; at most a quarter of the samples in the last quarter of a leader lie in other rows' hatch, and place_labels re-anchors on the row's ink until it holds (1.2 (h) r3, Designer M1 S2 r2 F1, S1 r6 F1); red-first for K4-B9 to B11 MEASURED by branch deletion (Designer sign-off r3); a row may set label_side: left, a left label column under the same rules (1.2 (h) r4, Designer M1 S2 r3 N1); 1.3 P1R: plan labels are placed by one placer (sketch_common.place_plan_labels; candidates in order: label_side column then the other, label_theta ray hit, column default anchor, ink samples at most 2 mm apart; first candidate passing every leader rule, re-judged after column stacking; left-column text clear of the y tick labels); (e) only true outlines of rows higher than the labelled row by more than 0.05 (zones: every outline) count; (e1) a row with visible ink (renderer split, certified by K8 cover; a stand-in's convention line is visible ink where no cover contains it) anchors on visible ink and its leader's last quarter lies outside every counted outline that does not enclose the anchor; (e2) a wholly hidden row anchors on its hidden ink and its last quarter lies outside every counted outline that does not enclose the anchor (Design Notes 30; Designer P1Rd FIX D1); an outline encloses for (e1) and (e2) only when the anchor and every point within 0.05 of it lie inside its outer boundary with holes filled (Topologist TP1.3-8); (f) a label with no passing candidate is recorded UNPLACEABLE with its candidate table in the K4 record and fails with reason "unplaceable", no silent fall-back; (g) the drawn label of a wholly hidden row contains "under " and the name of a counted row whose outline contains or encloses the anchor; (h) any two plan leaders that do not cross, anchor ends included, keep at least 4.0 mm apart (DECLARED, Designer P1Rf re-check FIX D4), judged and placed as a crossing is | Fixture with all labels from keys; K4-Z2 live S2; K4-Z3 live S2 drawn by s2_plan.py; K4-Z4 live S1 drawn by s1_side_poses.py; K4-Z5 S3 span_lt label prints its expr value 870 | B1 label without a number; B2 label "tube OD 150" against `drill.tube_od` 152.4; K4-B4 drawn note without the LM20UU bushing; K4-B5 a not_drawn part in neither note; K4-B6 S1 r5 spec with not_drawn and no figure_note (FIX R1); K4-B7 sightline leader at the r1 anchor, off the line; K4-B8 r1 concentric anchors, three crossings; K4-B9 S1 core 750 at the r6 anchor (end in hatch); K4-B10 an area drawn over a leader; K4-B11 an area of another row over an anchor (with (e1) on the hidden ink); K4-B12 the descent-stop leader at the r4/r5 anchor (inside tie b); K4-B13 a pad under an opaque lid (unplaceable); K4-B14 ring label at the r6 anchor on hidden rim inside tie a (e1); K4-B15 drill_head label without its "under ring gear" suffix (g); K4-B16 gear outline planted as an open C, not enclosing the cutter anchor (e2, g); K4-B17 ring label anchored 0.028 mm outside tie a, last quarter 41.3 mm inside it (TP1.3-8); K4-B18 tie a label anchored on its phantom line under a planted nearer disk (e1, Designer FIX D5); K4-B19 the S2 r7 tube OD, base plate and cutter leaders, 1.87 mm apart (h, Designer FIX D4); K4-B8 re-planted at 1.3 P1R and P1Rf; K4-B7, B8, B10 to B12, B14 counts re-read at P1R to P1Rf2; K4-B20 span_lt label prints its key value 1150 where the spec names expr (1.3 P4: a label prints label.expr, a label.value_from spec value, or for fmt s the key's string value); K4-Z6 and K4-B21 load_tension_c value_from 254.04 against a printed 300; K4-B22 a label drawn outside its home Axes, refused (1.3 P5f); (i) on a script-drawn figure no drawn leader crosses a text box and no two text boxes overlap (labels, notes, tick labels, titles; boxes shrunk 1 px): K4-B23 text planted on two leaders, K4-B24 text planted on a label (1.3 (h) r2, Designer M1 S3 r1 F2, F3); K4-B7, B8, B18 re-counted 4, 7, 3; (j) a label printing a load reads checks_s3.loads() from the keys (load_comp_c cases, load_tension_c), and every load_cases per_screw literal agrees with loads() within 0.005 N, every number of a stall literal '<v1> / <v2> (mu <m1> / <m2>)' held to F_stall at its mu (K4-Z7, Z8, B25 static 79, B26 ring.mass + 4 kg; 1.4 step 0 K4-B37); (k) a row declaring label_anchor_frac ends its leader at that anchor, frac in [0, 1] (K4-B27, B28); (l) in every view (side, plan, section) and every declared Axes of a script-drawn figure, no leader (clipped to the Axes box) runs within 2 deg and 1.0 mm of a line of the families reference line, gridline (major and minor) or part edge over more than 5 mm; the part-edge set of a leader of row f is the union, over every visible tagged artist a of a row other than f, of the drawn stroke of a (the ring boundary of a Patch with a filled face, a hatch or a stroked edge, renderer solid and dashed pieces and stand-in outlines included; the polyline of a Line2D or Collection of a non-reference row) intersected with the closure of a's clip region; hatch strokes, FancyArrowPatch marks and text are outside it (Topologist 1.4 P0T TP1.4-1) (K4-B29, B30; 1.4 step 0, C1.3-a: K4-Z9 to Z11, K4-B32 to B36, outline and part-line B at P0f; K4-Z3, Z4, Z8 re-scoped to B as the live red of S2 r9, S1 r8, S3 r7); (m) a stack_z label prints check_stack nut_z at its pose within 0.05 (K4-B31) (M1 S3 r4 F1, r5 Rule 1, Rule 2, F1, F2; 1.3 (h) r5, r6; rules (j) to (m) signed by the r6 fresh M1 reviewer, s3_visual_gate_r6.md; (l) at class scope from 1.4 step 0, The Designer signs at P0D) |
```

2. Design Notes 25, row C1.3-a (l.705). Supersedes research/sean/cr_scratch/step1.4_engineer_step0.md item 4.

Old:

```
| C1.3-a (carried at the 1.3 close) | K4 rule (l) leader collinearity: (1) global scope, S1 and S2 side and plan views (dry-run fires on S1 r8 height_target leader along the z 2000 gridline; landing it opens S1 r9); (2) part-edge extension in section views (s3_visual_gate_r6.md N1: add every tagged artist edge except the label's own row; live r6 fires 2, r7 clean, MEASURED by the reviewer) | 1.4 (S4) step 0, before the S4 draw; S1 r9 only if Sean takes (1) | The Engineer; The Designer signs; Sean on (1) |
```

New:

```
| C1.3-a (carried at the 1.3 close) | K4 rule (l) leader collinearity: (1) global scope, S1 and S2 side and plan views (dry-run fires on S1 r8 height_target leader along the z 2000 gridline; landing it opens S1 r9); (2) part-edge extension in section views (s3_visual_gate_r6.md N1: add every tagged artist edge except the label's own row; live r6 fires 2, r7 clean, MEASURED by the reviewer) ; 1.4 step 0 (`research/sean/cr_scratch/step1.4_engineer_step0.md`): implemented at class scope (reference lines, gridlines, part edges; side, plan, section; every declared Axes; K4-Z9 to Z11, K4-B32 to B36); dry run on the drawings of record fires S1 r8 4 (height_target on the z 2000 gridline, each pose), S2 r9 3 (plan gridlines y 0, y 260, y 80), S3 r7 1 (inset gridline y 80), reference lines 0, part edges 0 under the implemented area-only set; with the part-edge set of Topologist 1.4 P0T TP1.4-1 (every drawn stroke of another row) S2 r9 fires 1 more (keepout leader 25.8 mm along the dashed hidden toe edge of pinion_b), S1 r8 and S3 r7 0 more (MEASURED, step1.4_topologist_step0_check.md); firings go to the P6 batch (S1 r9, S2 r10, S3 r8) | 1.4 (S4) step 0, before the S4 draw; S1 r9, S2 r10, S3 r8 at P6 | The Engineer; The Designer signs (P0D); Sean on (1) |
```

3. Design Notes 25, row TP1.3-10 to TP1.3-20 (l.704)

Old:

```
| TP1.3-10 to TP1.3-20 (S3 r1 cross-review, step1.3_topologist_crossreview.md) | S3-3 certifies contact without load sense: 24 of 51 links pass on a contact that cannot carry the cut-case force in its direction (base route core_seat, collet, holder, receiver; member feet in tension; bracket side faces; ring and bearing radial fits); link kind face / thread / one_body / declared with a face-sense predicate (TP1.3-10); unsectioned occlusion premise for convention clause (2), 8 row pairs live in r1 (TP1.3-11); not_drawn parts classified against the section band, rear nut shoulder screw in the beyond band (TP1.3-12); sub-artist rulings: plan_axes:arc admission with the ccw sign check (TP1.3-13), anchor cover alternate hatch per piece under hatch_split, no sub-artist (TP1.3-14), screw thread root-line or tick admission (TP1.3-15); NOTEs K8 per-predicate record, S1 mark.z names the key, S1 lift motor at the circumscribing width, lever u expression, wingnut sweep under the part gid (TP1.3-16 to -20). TP1.3-10 to -15 and -19 CLOSED as rules at r2/r3 (P7r, raisers signed r3); TP1.3-16 to -18, -20 carried as NOTEs | 1.3 (h) P9; NOTEs to S4 | The Topologist proposes and signs; The Designer (spec chains, classes, patterns, thread form); The Engineer; The Loftsman (kept_axial holder value) |
```

New:

```
| TP1.3-10 to TP1.3-20 (S3 r1 cross-review, step1.3_topologist_crossreview.md) | S3-3 certifies contact without load sense: 24 of 51 links pass on a contact that cannot carry the cut-case force in its direction (base route core_seat, collet, holder, receiver; member feet in tension; bracket side faces; ring and bearing radial fits); link kind face / thread / one_body / declared with a face-sense predicate (TP1.3-10); unsectioned occlusion premise for convention clause (2), 8 row pairs live in r1 (TP1.3-11); not_drawn parts classified against the section band, rear nut shoulder screw in the beyond band (TP1.3-12); sub-artist rulings: plan_axes:arc admission with the ccw sign check (TP1.3-13), anchor cover alternate hatch per piece under hatch_split, no sub-artist (TP1.3-14), screw thread root-line or tick admission (TP1.3-15); NOTEs K8 per-predicate record, S1 mark.z names the key, S1 lift motor at the circumscribing width, lever u expression, wingnut sweep under the part gid (TP1.3-16 to -20). TP1.3-10 to -15 and -19 CLOSED as rules at r2/r3 (P7r, raisers signed r3); TP1.3-16 to -18, -20 carried as NOTEs; 1.4 step 0 (step1.4_topologist_step0_check.md): -16 to S4 (c) with the not_drawn band margins in the K8 record, -17 to S1 r9, -18 to the S1 r9 M1, -20 (sweep envelope under the wingnut gid, drawn in S1 and S3) to S1 r9 and S3 r8 | 1.3 (h) P9; NOTEs to S4 | The Topologist proposes and signs; The Designer (spec chains, classes, patterns, thread form); The Engineer; The Loftsman (kept_axial holder value) |
```
