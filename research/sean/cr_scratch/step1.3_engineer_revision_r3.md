## Corrections to the brief

1. **The Designer's dimension offset, u -225, fails the Loftsman test.** u -110 is applied, as the ruling directs.
   - At u -225 the line has both end points inside the arm sections: (u -225, z_S 340) lies in bracket_anchor_c and (u -225, 1210) in bracket_guide_c (MEASURED, `p9r3\probes\dimtest.py` on the live drawing; capture_end, the only pose the section draws).
   - Every u between the block face (-181) and member c (-244) puts both ends in the arms. The bearing lines (280 and 1150 z_A) lie inside the arm z bands (Loftsman re-check section 5).
   - The offset is written as an overlay leaf, `jackscrew.span_dim_offset` 50 (ASSUMED). It enters the row as `r_in: jackscrew.pitch_radius - jackscrew.span_dim_offset`.
2. **Three Topologist Bs match on the r2 code, because their branches landed at r2:** S3-3-B16 and B17 (R2-1) and K8-B86 (R2-2). Their red-first runs on the pre-r2 code (`p9r3\pre_r1`, the `p9r2\pre` harness with the r3 fixtures): all three read clean there (MEASURED).
3. **W_kg + drill.top_block_mass leaves S1 and S2 pixels unchanged.** S1 r8 (4 poses) and S2 r9 rebuild pixel-equal to `wip/` (`numpy.array_equal` True, MEASURED). No S1 r9 or S2 r10 opens.
   - The S1 mass report now carries W 26.25 kg with the block inside it.
   - Mass, COM and tip forces are unchanged: 81.50 / 81.50 / 81.50 / 65.90 kg and 351 / 379 / 563 / 269 N (MEASURED).
4. **Two existing S3 controls carried the W 24.25 literal:** K4-Z6 and K4-B21 (load_tension_c value_from 254.04). Re-planted at 247.5 (W 26.25, LF1.3-2).
5. **The Designer's item 9 and the Loftsman's LF1.3-10 give different kept_axial texts.** The Loftsman text, which carries a dry run, is applied in `checks_s3.py`, in the spec reported_items and in load_cases cut `kept_parts`.

Tags: MEASURED (read from a run in this session), DERIVED (hand arithmetic), DECLARED (spec, params or ruling), ASSUMED (working value).

Locations:
- Scratch: `D:\Unleashed Robotics\_scratch\cutjig\p9r3\`.
  - `pre\`: the r2 harness, the pre-change code.
  - `pre_rf\`: the r2 code with the r3 fixtures, spec and overlay.
  - `pre_r1\`: the pre-r2 code with the r3 fixtures.
  - `probes\`.
- S3-3 dry run uses `p9r2\records` (S1 r8 and S2 r9 marked accepted).
- TMP and TEMP: `_scratch\cutjig\tmp`. Nothing was written to C:.

## 1 Fixes per source item

| Source item | Fix | Control IDs |
|---|---|---|
| Designer 1 (F1 option A) | `sketch_common.FIGSIZE["section_yz"] = (20, 30)`. PNG 4157 x 3876 px | K3 (figsize per view) |
| Designer 2 (D1, F3) | sync_callout text `sync:`, hold_callout text `power-off hold:` | K4 live pass |
| Designer 3 (F7) and orchestrator offset ruling | span_lt at u -110 (Corrections 1). Two extension lines `span_lt:ext` run from the screw edge at u -154 to 2 past the dimension line (-108), at z_S 340 and 1210. Admission rule `sketch_common.ext_issues` (e1 to e4, `EXT_OVERSHOOT_MAX` 3) | K5-B44 (e1), B45 (e2), B46 (e3), B47 (e4); Z: S3 live and K5-Z6 / Z7 fixtures (ext drawn) |
| Designer 4 and orchestrator hatch ruling | `section.hatch_alt: {aluminium: "--"}`. hatch_split `above` text. Legend line 2 `aluminium // (anchor cover above the joint --)` | K8-Z16 (live state), B79 to B82 |
| Designer 5 | not_drawn split: front nut shoulder screw `off_plane` (x 8.86 to 18.86), rear `deferred` (owner Step 2). Figure note text | K8-B83 (re-planted on the rear entry), B86 |
| Designer 6 | no change (dashed split kept) | K8-B77, B78 |
| Designer 7 (D5, LF1.3-2) | `load_cases.W_kg + drill.top_block_mass`. load_cases literals and S3-2 `expected` updated. `s1_mass_report.py` puts the block in W. Re-runs: `--stale`, `s1 --rev 8`, `s1_mass_report.py --rev 8`, `s2 --rev 9` | K4-Z6, B21 re-planted at 247.5 |
| Designer 8 (D7) | overlay leaves `receiver.shoulder_bolt_pcd` 180, `shoulder_bolt_angle` [30, 150, 210, 330], `shoulder_bolt_head_d` 8.5 (ASSUMED). `receiver.shoulder_bolts` value text updated. not_drawn `off_plane` with x bands ±77.94 ∓ 4.25. Figure note `(off the plane, PCD 180)` | K2 (194 overlay leaves), K8 not_drawn band clean |
| Designer 9 / LF1.3-10 | kept_axial text (Corrections 5) | RPT |
| Designer 11 | legend line 3 `, thread root inside screw c` | K4 (i) live pass |
| Orchestrator, remove stand-ins | `_designer_pending` and the `pending` argument removed. `FIXTURE_ALT` kept as the live "--" for plants | K8-B82, B83 judged on the live state |
| Topologist R2-1 | S3-3-B16 (kind face, no face z), B17 (kind face, record certifiers only). B14 desc: regression guard, not red-first | S3-3-B16, B17 |
| Topologist R2-2 | K8-B86: the rear entry with its owner removed (the bolt entry is now off_plane) | K8-B86 |
| Topologist R2-3 | fixture `_draw_arc` draws the head (FancyArrowPatch theta1 - 10 to theta1) as the script does | K5-Z7 (with head), K5-B43; K5-B41 re-counted 2 (the head leaves the circle with the line) |
| Topologist R2-4 | `hatch_family`: the lint compares line families, `+` as {\|, -}, `x` as {/, \\} | K8-B87; K8-B81 reason re-read ("line family of material pattern(s) steel") |
| Topologist R2-5 | ring\|bearing and bearing\|drill_tube in chains c, a, b: certifiers `["declared (S6-5 draws the axial seat)"]`, K7 certifiers dropped | S3-3-Z |
| Loftsman LF1.3-10 | kept_axial text (Corrections 5) | RPT |
| Loftsman NOTE LF1.3-11, -12; Topologist NOTE R2-6, R2-7 | not applied (S2 spec source text; Step 2 bearing row; literal x bands; arc a1 spec plant) | none |

## 2 Dry runs

| Item | Result (MEASURED) |
|---|---|
| span_lt u -225 (r_in 225), Loftsman test | **FAIL**: end (−225, 340) inside bracket_anchor_c, end (−225, 1210) inside bracket_guide_c; on no part edge; crosses both arms |
| span_lt u -110 (r_in 110), Loftsman test, on the r3 drawing | **PASS**: both ends in free space; on no part edge (ring OD, home-switch faces, arm sections none); crosses gear and ring (moving parts, cut). K4, K5 (ext admitted), K6, K7, K8 (projected_x / extent read the line alone), K9, S3-2 pass |
| u -210 (for the record) | FAIL: ends in both arms; on the ring OD edge (374.84 to 386.84) and the home_switch_c face (1182.00 to 1195.00) |
| Hatch line-family lint | "--", "\|\|", "++" pass; "////", "\\\\", "\\", "/", "xxx", "/\\", "..." fire (equals the Topologist R2-4 dry run) |
| W 26.25 kg | per screw 85.84 / 119.85 / 185.84 / 247.50 / 343.18; margins 15.89 / 11.38 / 7.34 / 3.97; WOB 1287.05 / 1104.16 N; lift torque 0.325 / 0.157 N m; uplift 3 F_stall - W 772.03 N |
| S1 / S2 on the r3 harness | pixel-equal (Corrections 3); S1 r8 19/19, S2 r9 18/18; S2 tip force still reads the accepted S1 r7 report until ORCH-B |

## 3 Red-first

| Control | Pre-change code | Observed there | Red |
|---|---|---|---|
| K5-B43 head cw | r2 (`pre_rf`) | fires 2 against planted 1 | yes (count) |
| K5-B44 to B46 ext e1 to e3 | r2 | fires 1, "sub-artist ext has no admission rule" | yes (reason) |
| K5-B47 ext e4 | r2 | fires 2, unadmitted reason | yes (reason, count) |
| K8-B87 '////' | r2 | clean | yes |
| K8-B86 deferred no owner | pre-r2 (`pre_r1`) | clean | yes |
| S3-3-B16 face no z | pre-r2 | clean | yes |
| S3-3-B17 face no S3 | pre-r2 | clean | yes |
| K4-Z6, B21, K5-B41, K8-B81, B83 | re-plants / re-reads | not new rules | n/a |

## 4 Check results (MEASURED)

**S3 r3** (`docs/sketches/wip/s3_checks_r3.json`): **15 of 16 pass**.
- K4 is clean; K8 is clean.
- S3-3 fails 7 issues, from the stale S1 r7 / S2 r5 records only.
- Dry run with S1 r8 and S2 r9 accepted (`--docs-dir p9r2\records`): **16/16**, S3-3 48 links.
- K5: section 130 artists, inset 36. K7: 269 section tests. K8: 218 section predicates, 75 inset.
- S3-1: 25.84. S3-2: least 3.97. RPT: 10 items (wob_max 1287.05 / 1104.16 N; kept_axial without the holder).

| Run | Result |
|---|---|
| S1 r8 re-run | 19/19 |
| S2 r9 re-run | 18/18 |
| `--baseline s3` | 16/16 matched |
| `--stale` | 2 records, 5 differences (adopted keys, unchanged) |
| `--controls --jobs 12` | **401/401 match (Z 95, B 303, smoke 3), 191.8 s** |

Controls added in r3: K5-B43 to B47, K8-B86, B87, S3-3-B16, B17 (9).

## 5 PNG

`docs/sketches/wip/s3_jackscrew_section_r3.png` (4157 x 3876 px).

## 6 Rules awaiting signature

| Rule | Raiser | Z / B |
|---|---|---|
| `span_lt:ext` admission (e1 to e4) | The Designer | S3 live, K5-Z6 / Z7 fixtures / K5-B44 to B47 |
| S3-3 link kinds and face sense (with B16, B17) | The Topologist (R2-1) | S3-3-Z / B12 to B17 |
| not_drawn bands, deferred owner branch (B86) | The Topologist (R2-2) | K8-Z14 / B83 to B86 |
| `plan_axes:arc` head (B43, Z7 with head) | The Topologist (R2-3) | K5-Z7 / B40 to B43 |
| hatch alternate by line family (B87) | The Topologist (R2-4) | K8-Z16 / B79 to B82, B87 |

## r4

Sources: `docs/sketches/wip/s3_visual_gate_r3.md` (fresh M1 S3 r3 FAIL V8: F1, F2), `research/sean/cr_scratch/step1.3_raisers_sign_r3.md` (five rules signed; Designer objection D-r3-2 to "--"; NOTE D-r3-1), orchestrator rulings for r4. Scratch: `D:\Unleashed Robotics\_scratch\cutjig\p9r4\` (`pre\` the r3 harness, `pre_rf\` the r3 code with the r4 fixtures, spec and script). TMP and TEMP at `_scratch\cutjig\tmp`; nothing on C:.

### Corrections to the brief (r4)

1. **Both terminator forms touch K8 projected_extent on a reference line row of footprint half-width 0.** Ticks and arrowheads both widen the drawn x of span_lt: arrowheads drawn under gid span_lt read x [-111.14, -108.86] on the r3 code (K8-Z17 there, MEASURED). Arrowheads are picked. The K8 projected tests of a reference line row in a side or section view now read the row through `geom_pieces`, the P4 rule that an arrowhead on a line row marks it and is not its extent. The premise is checked: every arrow of the row has tail and head on the row's line ink (`sketch_common.terminator_issues`). This is a new relief, so it is listed for signature (Designer, raiser of D-r3-1).
2. **The extension-line overrun stays at 2 (e3 0 to 3).** With the `_` marker gone, the visible red past the dimension line is the extension line's 2 mm alone (D-r3-1: was 6.1 from the marker).

### Fixes

| Item | Fix | Controls |
|---|---|---|
| M1 S3 r3 F1 | span_lt label text `S3-2 span, K 0.7; L_t` (expr unchanged): prints "S3-2 span, K 0.7; L_t 870" | K4 live pass; K4-B20 reason re-read ("S3-2 span, K 0.7; L_t 1150") |
| M1 S3 r3 F2 | hold_callout mark from the inboard screw edge u -154 toward +u to u -124 (us + nominal / 2 + profile.width / 2); the leader lands at the mark root from the label column without crossing the screw | K4 (leader rules, (i)), K7 (269 section tests clean), K9 live pass |
| Orchestrator hatch ruling (Designer D-r3-2) | `section.hatch_alt: {aluminium: "||"}`, hatch_split `above` text, legend `(anchor cover above the joint ||)`, `FIXTURE_ALT` "\|\|" | K8-Z16 clean; K8-B79, B80 reasons re-worded to '\|\|' |
| D-r3-1 | `marker="_"` removed from span_lt; two arrowhead terminators (FancyArrowPatch, LABEL_FONTSIZE long, heads on the extension lines at z_S 340 and 1210); K8 projected tests read the line without its arrows, premise `terminator_issues` | K8-Z17 (live S3), K8-B88 (line 5 off: guard), K8-B89 (arrow 10 off the line) |

### Red-first (r3 code, `p9r4\pre_rf`, MEASURED)

| Control | Observed on the r3 code | Red |
|---|---|---|
| K8-Z17 live S3 with terminators | fires: span_lt projected_extent x [-111.14, -108.86] (by 1.14) | yes |
| K8-B89 arrow off the line | fires 2 with the projected_x / extent reason, not the terminator reason | yes (reason) |
| K8-B88 line 5 off | fires 2, same reason: a guard that the relief does not hide the line position (not red-first) | n/a |

### Check results (MEASURED)

- **S3 r4** (`docs/sketches/wip/s3_checks_r4.json`): **15 of 16 pass**. S3-3 fails only on the stale S1 r7 / S2 r5 records. Dry run with S1 r8 and S2 r9 accepted: **16/16**.
- `--baseline s3`: 16/16 matched.
- `--stale`: 2 records, 5 differences (the adopted keys, unchanged).
- **`--controls --jobs 12`: 404/404 match (Z 96, B 305, smoke 3), 196.5 s.** Added: K8-Z17, B88, B89.

PNG: `docs/sketches/wip/s3_jackscrew_section_r4.png` (4157 x 3876 px).

Rule awaiting signature: K8 reference-line terminator relief with its premise (`terminator_issues`; Z K8-Z17, B K8-B88, B89), raiser The Designer (D-r3-1).

## r5

Sources: `docs/sketches/wip/s3_visual_gate_r4.md` (fresh M1 S3 r4 FAIL F1, NOTEs N1 to N10) and the Designer's r4 delta-read notes DR4-1, DR4-2 in `wip/s3_visual_gate_r3.md`. Scratch: `D:\Unleashed Robotics\_scratch\cutjig\p9r5\` (`pre\` the r4 harness, `pre_rf\` the r4 code with the r5 fixtures, spec and overlay). TMP and TEMP at `_scratch\cutjig\tmp`; nothing on C:.

### Corrections to the brief (r5)

1. **N3 cannot be drawn solid under the plan renderer rule.** The block's shared outline with the NEMA 17 lies inside the nut-housing circle (r 25 > the block half-width 21) seen from +Z. render_plan therefore splits anchor_c: it is solid outside the housing (the four corners) and dashed inside, as a hidden part under a higher row (MEASURED, inset artists: anchor_c Polygon solid with clip, hidden copy dashed; liftmotor_c dashed). The anchor square is now drawn above the NEMA 17 (inset zorder 4 against 3), so the block corners lie over the motor's dashes. Inside the housing both outlines stay dashed by rule. Drawing them solid would need a cover exception, not a draw-order change.
2. **The phi_n range leaves the hold label.** hold.device carried the literals "lambda 5.19 deg < phi_n 8.83 to 11.70 deg". The label now prints the lead angle from the one spec expression `s3_checks.S3-2.stall.lead_angle`, `atand(jackscrew.lead / (pi * jackscrew.mean_diameter))`, which `checks_s3.loads` also uses. The phi_n range is printed by RPT backdrive. Both now read 5.20 (MEASURED: label "lambda 5.20 deg", RPT "lambda 5.20 deg"). `check_stack.eval_expr` gains `atand` and the constant `pi`.

### Fixes

| Item | Fix | Controls |
|---|---|---|
| M1 S3 r4 F1 (rule (h)) | load_comp_c label built at run time from load_cases per_screw: spec label `cases` [[static, static], [capture_lift, capture], [retract_bind, 'retract (F_bind {liftload.f_bind})'], [stall_up, stall up]], fmt .0f, suffix N. It prints "compression per screw: static 86, capture 120, retract (F_bind 300) 186, stall up 343 N". The text entries use the first number (governing mu). K4 cases branch: every case prints `name value` as load_cases per_screw gives it. Shape texts of load_comp_c (86 / 120 / 186 / 343) and load_tension_c ('T per screw, cut 247.5') corrected | K4-Z7, K4-B25 ("static 79" fires); load_tension_c stays on K4-Z6 / B21 (value_from 247.5) |
| N5 | hold label `expr_ref: s3_checks.S3-2.stall.lead_angle`, fmt .2f: "power-off hold: self-locking Tr12x3 lead, lambda 5.20 deg < phi_n (self-locking, RPT backdrive); options brake on each NEMA 17, park pin with visible state; Step 2 decides". hold.device value text without the numbers. `checks_s3.loads` takes lambda from the same expression | K4 live (value from expr_ref) |
| DR4-1 | placer anchor candidate `label_anchor_frac` on the column-side face. guide_c 0.83: anchor (-139, 1219.9), 9.9 above the extension line at 1210. anchor_c 0.95: anchor (-139, 353.5) on the cover, 13.5 above the extension line at 340. Dry runs (MEASURED): anchor_c 0.88 passed alone but failed the stacked-layout leader separation (placer fell back to an ink anchor at 338); 0.2 and 0.12 placed at 331 and 328.6 (below the line); 0.95 chosen (above the joint, per DR4-1). K4 leader rules and K9 pass | K4, K9 live |
| N3 | inset anchor square zorder 4 over the NEMA 17 at 3 (Corrections 1) | K8 inset cover pass |
| N1, N2, N4, N6 to N9; DR4-2 | notes, not applied | none |

### Red-first (r4 code, `p9r5\pre_rf`, MEASURED)

| Control | Observed on the r4 code | Red |
|---|---|---|
| K4-B25 "static 79" | clean: K4 skipped the label (value_from names a block, no single value) | yes |
| K4-Z7 | clean | Z |

### Check results (MEASURED)

- **S3 r5** (`docs/sketches/wip/s3_checks_r5.json`): **15 of 16 pass**. S3-3 fails only on the stale S1 r7 / S2 r5 records. Dry run with S1 r8 and S2 r9 accepted: **16/16**.
- RPT backdrive: "lambda 5.20 deg; mu 0.15: phi_n 8.83 deg ... mu 0.2: phi_n 11.70 deg".
- `--baseline s3`: 16/16 matched.
- `--stale`: 2 records, 5 differences (the adopted keys, unchanged).
- **`--controls --jobs 12`: 406/406 match (Z 97, B 306, smoke 3), 197.1 s.** Added: K4-Z7, K4-B25.

PNG: `docs/sketches/wip/s3_jackscrew_section_r5.png`.

Rule awaiting signature: K4 cases label value check. Premise: a label that prints several load-case values reads each from the load_cases entry at run time, so a change of W reaches the label. Every case prints `name value` in the label's fmt. Z K4-Z7, B K4-B25. Raiser The Designer (M1 S3 r4 F1).

## Gameplan lines to change

Merged from `step1.3_engineer_revision_r2.md` (E2), `step1.3_designer_r2_values.md` (D), `step1.3_loftsman_recheck_r2.md` (L) and `step1.3_topologist_recheck_r2.md` (T), plus r3. Apply the E2 items first. Each later Old reads text an earlier New writes; where an item supersedes an earlier one, the earlier item is marked.

1. E2 items 1 to 10 as written in `step1.3_engineer_revision_r2.md`. E2 item 9 (Progress Log row) and item 6 apply unchanged. Items 2, 3 and 6 are extended by items 2, 3 and 6 below.
2. l.139 (K5 row), after E2 item 2 (T item 1, extended):
```
Old: (K5-Z7, B40 reversed, B41 r + 5, B42 in the section; TP1.3-13) |
New: (K5-Z7 with the head drawn, B40 reversed, B41 r + 5, B42 in the section, B43 head clockwise on a ccw line; TP1.3-13, Topologist 1.3 P7r R2-3); span_lt:ext extension lines of a reference line row, horizontal at a z_rule end, from the screw edge facing the dimension line to 0 to 3 past it (K5-B44 to B47, e1 to e4; Designer 1.3 (h) r2 item 3) |
```
3. l.142 (K8 row), after E2 item 3 (T items 2 and 3):
```
Old: alternates differ from every material pattern (K8-Z16, B79 to B82; TP1.3-14)
New: alternates differ in line family (characters, + as | and -, x as / and \) from every material pattern and every other alternate (K8-Z16, B79 to B82, B87 alternate '////'; TP1.3-14, Topologist 1.3 P7r R2-4)
```
```
Old: or deferred with an owner (K8-B83 to B85; TP1.3-12)
New: or deferred with an owner (K8-B83 to B85, B86 deferred with no owner; TP1.3-12, Topologist 1.3 P7r R2-2)
```
4. l.147 (K table pointer), after E2 item 4:
```
Old: (392 controls: Z 95, B 294, smoke 3, all match; 187.7 s at --jobs 12).
New: (392 controls: Z 95, B 294, smoke 3, all match; 187.7 s at --jobs 12). Step 1.3 (h) r3 (research/sean/cr_scratch/step1.3_engineer_revision_r3.md) added K5-B43 to B47, K8-B86, B87, S3-3-B16, B17, removed the fixture stand-ins, re-planted K4-Z6 and B21 at 247.5 (W 26.25 kg) and K8-B83 on the rear nut shoulder screw entry, re-read K5-B41 (2) and K8-B81 (line family) (401 controls: Z 95, B 303, smoke 3, all match; 191.8 s at --jobs 12).
```
5. l.273 (detail 1.3 Shows; D item 1 with the offset per the r3 ruling):
```
Old: or the single-controller callout), so K9 sees all three.
New: or the single-controller callout), so K9 sees all three. Section Axes at figsize 20 x 30 in (section_yz, about 2.45 px/mm) so every screw-set part reads at 100 percent (1.3 (f) M1 S3 r1 F1, option A at 1.3 (h) r2); S3-2 span L_t as a dimension at u -110 (jackscrew.span_dim_offset 50; u -225 put both ends in the arm sections, orchestrator ruling 1.3 (h) r3) with extension lines from the screw edge (F7); anchor cover hatched with section.hatch_alt aluminium "--" ("////" refused by the line-family lint); an axial-loop figure note naming where the loop leaves the plane (F6).
```
6. l.289 (S3-3 row), after E2 item 6 (D item 2 and T item 4 merged):
```
Old: every link carries a kind: face with its sense, face_record, thread, one_body, fastened, declared)
New: every link carries a kind: face with its sense, face_record, thread, one_body, fastened, declared; S3-3-B12, B13 sense, B15 kind, B16 face kind with no face z, B17 face link with no S3 certifier, B14 a regression guard of the face-edge branch (Topologist 1.3 P7r R2-1); ring|bearing and bearing|drill_tube declared (S6-5 draws the axial seat), K7 certifiers dropped (R2-5); RPT kept_axial names collet with its core seat, receiver, base plate, the holder out of the path (Designer 1.3 (h) r2, Loftsman LF1.3-10))
```
7. l.293 (Reported), after E2 item 7 (L item 1):
```
Old: axial force in each kept part (collet, holder, receiver, base plate) at 1000 N and at F_stall, for Quinn's N5 ruling;
New: axial force in each kept part (collet with its core seat, receiver, base plate; the holder is outside the cut-case route at S3 r2, Topologist 1.3 (e) TP1.3-10 (a), Loftsman 1.3 (h) re-check LF1.3-10) at 1000 N and at F_stall, for Quinn's N5 ruling;
```
8. l.279 (load case Static; the Loftsman (e) item 1, applies with D item 7):
```
Old: two guide bushings with housings (overlay masses, ASSUMED until Q2, DN23-d and batch 2 B2-6 are answered; 24.25 kg at the 1.3 (a) values, Designer 1.3 (a) Correction 1).
New: two guide bushings with housings + the drill top-end block (drill.top_block_mass, moving; Loftsman 1.3 (e) LF1.3-2, Designer 1.3 (h) r2 pick 7) (overlay masses, ASSUMED until Q2, DN23-d and batch 2 B2-6 are answered; 24.25 kg at the 1.3 (a) values, Designer 1.3 (a) Correction 1; 26.25 kg with the block from S3 r3: WOB max 1287.05 N, S3-2 least margin 3.97 unchanged).
```
9. l.580 (Design Notes 16; L item 2):
```
Old: with the base frame supporting the plate (Loftsman R1).
New: with the base frame supporting the plate (Loftsman R1). Updated at 1.3 (h) r2: the drawn base route is core, core seat, collet foot on the receiver floor, receiver shoulder on the plate top; the holder carries no cut-case axial load in the drawing (Topologist TP1.3-10 (a); Loftsman re-check LF1.3-10), so the N5 part list is collet, receiver, base plate.
```
10. l.705 (Design Notes 32). This supersedes E2 item 10 and merges D item 3:
```
Old: for uplift in retract-with-bind and stall up (up to 1029.5 N)
New: for uplift in retract-with-bind and stall up (up to 1029.5 N gross; stall-limited through a gripped core 3 F_stall - W = 772.03 N at mu 0.15 with W 26.25 kg (791.65 N at 24.25), DERIVED, Loftsman 1.3 (e) LF1.3-6)
```
```
Old: the S1 certifier for that link is struck.
New: the S1 certifier for that link is struck. Shoulder bolts (Designer 1.3 (h) r2, D7): 4 x M5 on PCD 180 at theta 30, 150, 210, 330, ISO 4762 head D8.5, blind-tapped 10 deep in the 12 plate (ASSUMED); heads off the S3 band (x +-77.94); 257 N per bolt at 1029.5 N gross. W_kg includes drill.top_block_mass (D5, LF1.3-2): W 26.25 kg; kept-part force at F_stall + W 1287.05 N (B2-7 figure, was 1267.43).
```
11. Progress Log: insert after the E2 item 9 row, in this order: the D item 4 row and the T item 5 row (both verbatim from their files), then:
```
New: | 1.3 | 2026-11-26 | (h) P9 r3 (step1.3_engineer_revision_r3.md): S3 r3 15/16 (S3-3 stale records only; dry run with S1 r8 / S2 r9 accepted 16/16, 48 links); Designer picks 1 to 9 and 11 applied, offset u -110 (u -225 failed the Loftsman test: both ends in the arm sections), hatch_alt "--", fixture stand-ins removed; Topologist R2-1 to R2-5, Loftsman LF1.3-10 applied; span_lt:ext admission with K5-B44 to B47; W 26.25 kg: S1 r8 and S2 r9 pixel-equal, re-run 19/19 and 18/18, tip forces unchanged; controls 401/401 in 191.8 s; wip/s3_jackscrew_section_r3.png for the fresh M1 |
```
12. Design Notes 13: E2 item 8 row stands; insert after it:
```
New: | S3-r2 | 2026-11-26 | No correction from Sean yet. r3 came from the Designer r2 values, the Topologist and Loftsman r2 re-checks and the orchestrator rulings (offset, hatch alternate) | r3: K5-B43 to B47, K8-B86, B87, S3-3-B16, B17 (`step1.3_engineer_revision_r3.md`) |
```
13. r4, l.142 (K8 row), after item 3:
```
Old: or deferred with an owner (K8-B83 to B85, B86 deferred with no owner; TP1.3-12, Topologist 1.3 P7r R2-2)
New: or deferred with an owner (K8-B83 to B85, B86 deferred with no owner; TP1.3-12, Topologist 1.3 P7r R2-2); a reference line row's projected tests read its line without its arrowhead terminators, premise every arrow on the line ink (K8-Z17, B88, B89; Designer NOTE D-r3-1, 1.3 (h) r4)
```
14. r4, l.273 (detail 1.3 Shows), after item 5:
```
Old: anchor cover hatched with section.hatch_alt aluminium "--" ("////" refused by the line-family lint);
New: anchor cover hatched with section.hatch_alt aluminium "||" ("////" refused by the line-family lint; "--" read as a doubled joint line, Designer D-r3-2, orchestrator ruling 1.3 (h) r4); the L_t dimension terminated by arrowheads (D-r3-1);
```
15. r4, l.147 (K table pointer), after item 4:
```
Old: (401 controls: Z 95, B 303, smoke 3, all match; 191.8 s at --jobs 12).
New: (401 controls: Z 95, B 303, smoke 3, all match; 191.8 s at --jobs 12). Step 1.3 (h) r4 added K8-Z17, B88, B89 and re-worded K4-B20, K8-B79, B80 (404 controls: Z 96, B 305, smoke 3, all match; 196.5 s at --jobs 12).
```
16. r4, Progress Log, insert after the item 11 r3 row:
```
New: | 1.3 | 2026-11-26 | (h) P9 r4 (step1.3_engineer_revision_r3.md section r4): M1 S3 r3 F1 (span label 'S3-2 span, K 0.7; L_t 870') and F2 (hold mark from the inboard screw edge to u -124) fixed; hatch_alt '||'; span_lt arrowhead terminators with the K8 reference-line relief and its premise (K8-Z17, B88, B89); S3 r4 15/16 (S3-3 stale records only; 16/16 with S1 r8 / S2 r9 accepted); controls 404/404 in 196.5 s; wip/s3_jackscrew_section_r4.png for the Designer delta read |
```
17. r5, l.138 (K4 row), after E2 item 1:
```
Old: K4-B7, B8, B18 re-counted 4, 7, 3 |
New: K4-B7, B8, B18 re-counted 4, 7, 3; (j) a cases label (load_comp_c) prints every load case as `name value` from load_cases per_screw at run time (K4-Z7, B25 static 79; M1 S3 r4 F1, 1.3 (h) r5) |
```
18. r5, l.147 (K table pointer), after item 15:
```
Old: (404 controls: Z 96, B 305, smoke 3, all match; 196.5 s at --jobs 12).
New: (404 controls: Z 96, B 305, smoke 3, all match; 196.5 s at --jobs 12). Step 1.3 (h) r5 added K4-Z7, B25 (406 controls: Z 97, B 306, smoke 3, all match; 197.1 s at --jobs 12).
```
19. r5, Progress Log, insert after the item 16 r4 row:
```
New: | 1.3 | 2026-11-26 | (h) P9 r5 (step1.3_engineer_revision_r3.md section r5): M1 S3 r4 F1 fixed (load_comp_c label from load_cases per_screw: static 86, capture 120, retract 186, stall up 343 N; K4 cases rule, K4-Z7, B25 red on r4); N5 hold label lambda 5.20 from s3_checks.S3-2.stall.lead_angle, the expression RPT uses; DR4-1 leaders on the block faces at z_S 1219.9 and 353.5; N3 block over motor in the inset (inside the housing both stay hidden by rule); S3 r5 15/16 (S3-3 stale records only; 16/16 with S1 r8 / S2 r9 accepted); controls 406/406 in 197.1 s; wip/s3_jackscrew_section_r5.png |
```
