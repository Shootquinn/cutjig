## Corrections to the brief

1. **S1-5b least does not move: 142.00 (bearing to collar top), MEASURED.** The expected 125.00 to 133.80 (Loftsman section 3) is max(z gap, plan gap) for housing|collar. S1-5b certifies the side-view projected distance (XZ Euclidean, LF-1 rule), which is the larger lower bound: housing|collar sqrt(133.80² + 125.00²) = **183.105** (hand, DERIVED; check 183.105, MEASURED). The nearest housing pair is housing|wing-nut sweep, **162.429** (x gap 210 - 115 = 95.00, MEASURED). Bearing|collar 142.000 stays least. 91 pairs (was 77; +14 = 2 housings x 7 s1_5b_base parts).
2. **Tie|arm plan overlap is 146.37 mm², not 492.21** (Designer FIX 1 neighbour line). 492.21 is the overlap of the old strip (rod centre to member centre, Engineer Correction 1). The amended strip gives 146.367 (MEASURED, `overlap_area`). The pair stays C with z contact at 1165; its plan C rule is (c) open item 4e.
3. **The S1-5b gameplan row is l.235, not l.234** (l.234 is S1-5a). N1 is l.713 (Open Questions) and l.634 (NOTE table).
4. **The Designer's tie strip cannot be written as plain `from`/`to` expressions without a 600-character expression per coordinate** (no `**`, no helper names in `eval_expr`). `plan_poly` strips gained two optional fields in check_stack: `back` (start e behind `from` along u) and `stop_at` (end at the station of a point on the axis; `to` sets the direction). The near corner K is written in expressions; the station s_c = u · (K - rod centre) is computed. Corners reproduce the Designer's to 0.01 (below).
5. **S1 side view needed three harness admissions to carry a plan_poly row with no `place`** (S1 tie rows). Each states its premise and has its B (detail 1 common (h)):
   - check_stack: a plan_poly row with no `place` and no `depth` gets depth = its plan y extent (side-view band).
   - sketch_common `plan_footprint`: a plan_poly row's footprint is its one piece (several pieces: their hull). `plan_contact_fn` admits a one-piece plan_poly row as placed. Without this the live S1 K7 fails 8 (tie|member C, "no placed plan footprints"; reproduced on the pre-fix function).
   - Premise: K8 `projected_extent` on `plan_x` (and `plan_y` in plan) for plan_poly rows with no place. K8-B17 fires 4; on the pre-fix K8 it reads clean (reproduced). K7-B21 plants the Designer's Correction 1 strip (to the member centre): fires 4, plan overlap 1655.177 mm².
   The Software Engineer reviews these with the rest of the check_stack plan code at P5 (open item 4g).

## 1 Per-finding changes

All under `docs/sketches/`. CRLF kept.

| ID | Change | Evidence |
|---|---|---|
| Designer FIX 1 | `s2_spec.yaml` guide_tie_a/_b: z_rule `jackscrew.top_guide_z` to `+ profile.height` (1165 to 1225 z_A); strip `back: profile.width / 2`, `stop_at` = near corner K (tie a: (R - w/2) cos θ + (w/2) sin θ, (R - w/2) sin θ - (w/2) cos θ at jackscrew.angle[0]; tie b: signs on the w/2 t̂ term flipped at angle[1]); keys + `jackscrew.top_guide_z`, `.pitch_radius`, `.nut_flange_od`, - `base.plate_thickness`; neighbours rod N, arm C, member C (replacing rod C, member C); shape and notes per the Designer's text. Overlay `guide.top_support` value and source per the Designer | Tie a corners (198.45, -28.36), (258.36, -31.55), (265.04, 93.96), (205.13, 97.15); tie b the x mirror; z_S 1225 to 1285 (MEASURED, check_stack). Plan, tie a: member b 0.000 / 0.000 mm² (point contact at K), arm b 0.000 / 146.367, guide_b block 44.556, NEMA 23 b 46.161, pinion b 54.436, gear 73.343, keep-out 113.467 (MEASURED; Designer 44.56, 46.16, 54.44, 73.35, 113.47) |
| Designer FIX 2 | `s2_spec.yaml` `not_drawn` + "LM20UU bushing (OD 32 x 42)" with the Designer's reason; `part_list` + matching line | Part list on the Designer's grouping: 41 rows / 4 not_drawn / 0 missing (`not_drawn` holds 6 entries: wing nut, collet, holder split) |
| Designer FIX 3 | `plan_figure.figure_note` with the Designer's text (names wing nut, collet, holder, hold device, LM20UU bushing, pads at 30 and 270 = every `not_drawn` part); comment: s2_plan.py prints it, K4 or a label check at (c) with Z and B | Field present; the drawn-text check is a (c) item (open) |
| Designer FIX 4 | Overlay `ring.motor_mount_placement` value "at each pinion.angle; pinion azimuths = screw azimuths + 60 deg (pinion.angle), S2; Designer 1.2 (a), Sean STOP S2-A O1-B" | Text leaf; no S1 or S2 row reads it; not in s1 r4 keys_read, so `--stale` does not list it |
| Designer NOTE 1 | `keepout` S2-a group + guide_tie_a, guide_tie_b (G 0) | 113.467 each (MEASURED) |
| Designer NOTE 2 | S1 header comment rewritten: housings and ties are now S1 rows (option A) | text |
| Designer NOTE 3 | Rubric line 4 "(visual only, V7)" | text |
| Loftsman FIX 1 (option A, Design Notes 28) | `s1_spec.yaml`: rows guide_bushing_a/_b (place and z_rule string-equal to S2; neighbours s1_5b_base, fixed_g10, rod N) and guide_tie_a/_b (z_rule and plan_poly string-equal to S2; neighbours rod N, arm C, member C); guide_lug_a/_b shape text as S2 (housing row and rod row named, r 250, 40 wide) and lug\|housing C; `not_drawn` field with the LM20UU bushing. `s1_side_poses.py` draws the housings with the lugs and the ties over their plan x extent, dashed. `fixtures/builders.py` full-draw reads plan_x for plan_poly rows | S1 r5 preview 17/17, 58 rows (K9). Housing a x 210 to 250, z_S 1119.84 / 994.84 / 344.84 / 1119.84 bottom (load / start / capture_end / park). S1-5b least 142.00 (Correction 1). Tie\|member b: plan-contact; tie\|arm b: C (z touch); rod: N |
| Loftsman NOTE (X1 lint) | Not written: it is a (c) item per Sean | open for (c) |

Shared-row field compare after the edits (MEASURED, whitespace-normalised): 47 row ids in both specs (43 + 2 housings + 2 ties); `place`, `plan_poly` and `z_rule` string-equal in every one except where the field exists in S2 only: keepout `place`, base_plate and base_frame `plan_poly` (S1 uses `depth`).

## 2 Re-run results

| Command | Result | Time |
|---|---|---|
| `check_stack.py s2_spec.yaml` / `s1_spec.yaml` | exit 0 / exit 0 | < 2 s each |
| `check_sketch.py s1 --rev 5` (preview to wip/, not of record, no PNG) | **17/17 pass**; K9 58 rows; K7 515 pair tests clean; K8 346; S1-5b 91 pairs, least 142.00 | 12.9 s |
| `check_sketch.py --stale` | red, exit 1: 1 record, 1 difference, `frame_upper.radius recorded 300, live 274` | 3 s |
| `check_sketch.py --stale --include-unaccepted` | red, exit 1: 2 records (s1 r4, wip s1 r5), the same single difference | 3 s |
| `check_sketch.py --controls` (run 1) | Z 38/38, B 88/89, smoke 1/1, exit 1: K7-B20 fired 12 against planted 8. The rotated member a also opens the new tie b corner contact (guide_tie_b\|frame_upper_a C, bands 3.111 apart), 4 poses. Correct detection; manifest planted 8 to 12, reason substring added | 192 s |
| `check_sketch.py --controls` (run 2) | **Z 38/38, B 89/89, smoke 1/1 (128/128; P2 count 126 + K8-B17, K7-B21)**, exit 0; to wip/fixtures/ | 189 s |

`--stale` keys changed by this pass: none in the s1 r4 record. Overlay leaves edited: `guide.top_support`, `ring.motor_mount_placement` (text values). Neither is in the r4 keys_read; the r5 preview reads `guide.top_support` and the five `guide.bushing_*` leaves for the first time (keys only in r5, MEASURED).

S1 r5 preview against the accepted r4 record (MEASURED):
- keys_read: changed `frame_upper.radius` only; added `guide.bushing_type`, `.bushing_od`, `.bushing_length`, `.bushing_housing_od`, `.bushing_drop`, `guide.top_support`.
- check reasons that differ: K2 (322 keys, 121 leaves), K5 343 artists, K6 231 z_rules, K7 515 tests, K8 346, K9 58 rows, S1-5b 91 pairs. S1-1 650.00, S1-2 125.00, S1-3 367.34 / 117.34, S1-4 0.84, S1-5a 192.34, S1-5b 142.00, S1-6, S1-7 607.66 unchanged. `reported` equal.
- K7 labels r4 to r5: C 93 to 109, F 266 to 296, G 16 to 0, N 125 to 141, plan-contact 40 to 48, swept:F 43 to 47, swept:G 4 to 0, undeclared:C 18 to 26, undeclared:plan-separated 41 to 49.

Spec header `s2_spec.yaml` status: "fixes applied, awaiting re-check". S1 status line unchanged (r5 re-sign follows the P3b re-check).

## 3 Open

1. figure_note drawn-text check (Designer FIX 3): K4 or a label check with Z and B at (c).
2. X1 shared-row lint (Loftsman section 2): (c). Its field list now includes `plan_poly`.
3. Plan C rule for tie|arm (z contact, plan overlap 146.37) and housing|lug: (c) open item 4e.
4. S1 `fixed_g10` does not list the ties (S2's does). Moving parts against the ties in S1 are undeclared F: every one passes depth- or plan-separated at r5 (NEMA 23 b to tie a 46.16 plan). The swept G 10 case for the ties is carried by S2.

## 4 Disposition

| Finding | Raiser | Disposition | Where |
|---|---|---|---|
| FIX 1 guide tie on the arm, 125.69 x 60 to corner K, N / C / C, overlay text | Designer | Closed | s2_spec.yaml guide_tie_a/_b; proposed_params.yaml guide.top_support; check_stack strip `back`, `stop_at` |
| FIX 2 LM20UU bushing not_drawn | Designer | Closed | s2_spec.yaml not_drawn, part_list; s1_spec.yaml not_drawn |
| FIX 3 figure_note | Designer | Closed (field); drawn-text check open for (c) | s2_spec.yaml plan_figure |
| FIX 4 motor_mount_placement text | Designer | Closed | proposed_params.yaml |
| NOTE 1 ties in S2-a | Designer | Closed | s2_spec.yaml keepout |
| NOTE 2 ties in the S1 r5 header list | Designer | Closed (now rows; header rewritten) | s1_spec.yaml header |
| NOTE 3 rubric line 4 visual only | Designer | Closed | s2_spec.yaml rubric_additions |
| FIX 1 S1 r5 housings and ties, option A; lug shape text | Loftsman | Closed; S1-5b measured 142.00 (Correction 1) | s1_spec.yaml, s1_side_poses.py, builders.py |
| X1 shared-row lint | Loftsman | Open for (c) (Sean) | none |
| Premise checks for the plan_poly admissions | Engineer (h) | Closed: K8-B17, K7-B21; K7-B20 planted 8 to 12 | sketch_common.py, manifest.yaml, builders.py |

## Gameplan lines to change

**l.235** (S1-5b row), Z cell.

Old:
```
| Live S1 (least 142.00, bearing to collar top) |
```
New:
```
| Live S1 (least 142.00, bearing to collar top; 91 pairs with the r5 LM20UU housings, housing least 162.43 to the wing-nut sweep, 183.11 to the collar, MEASURED 1.2 (b) fix pass) |
```

**l.713** (N1, Open Questions), fragment.

Old:
```
not by S1-5b (least 142.00)
```
New:
```
not by S1-5b (least 142.00, unchanged at S1 r5 with the guide housings, MEASURED 1.2 (b) fix pass)
```

**l.140** (K table, K7 row) and **l.141** (K8 row): append to each control list. K7: `; B21 live S1 tie a strip to the member centre (plan_poly plan-contact)`. K8: `; B17 live S1 tie a drawn 10 wider than its plan_poly extent`. Exact old text for the append point is the end of each row's B cell; the orchestrator places it.

**l.131** (spec format, the 1.2 (b) fields sentence the Engineer proposed at P2), fragment.

Old:
```
or a strip from point to point with a half-width;
```
New:
```
or a strip from point to point with a half-width, optional `back` (start behind `from`) and `stop_at` (end at a point's station on the strip axis); a one-piece plan_poly row with no `place` is a plan footprint for K7 plan-contact and plan-separated, its depth band is its plan y extent, and K8 projected_extent holds the drawn part inside its plan_poly extent (K8-B17, K7-B21);
```

**Echo Site Registry**: insert the Designer's row (his Gameplan lines item 1) with the area corrected: `| Guide rod top tie **30-6060, z_A 1165 to 1225** on the top-guide arm, rod top 1212 in the tie, end at the member's near corner (125.69 x 60) | overlay \`guide.top_support\`, \`jackscrew.top_guide_z\`, \`profile.*\`, \`frame_upper.radius\` | ASSUMED (Designer 1.2 (b) sign-off FIX 1; Step 2 decides) |`

**Progress Log, row 1.2** (append): `P2f fix pass: Designer FIX 1 to 4 and NOTEs 1 to 3 applied; Loftsman FIX 1 option A (S1 r5 rows guide_bushing_a/_b, guide_tie_a/_b, lug shape text); S1 r5 preview 17/17, S1-5b least 142.00 unchanged (housing least 162.43); controls Z 38/38, B 89/89, smoke 1/1 (K8-B17, K7-B21 new; K7-B20 planted 8 to 12); --stale red on frame_upper.radius only; s2 status "fixes applied, awaiting re-check".`
