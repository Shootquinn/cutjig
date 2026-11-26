# Step 1.2 (h) Engineer: S2 r4 (S1 stays r7)

## Corrections to the brief

1. **Gameplan line numbers.** The Designer's sign-off r3 names the K5 row as l.148 and the K8 row as l.186. In the gameplan as it stands they are l.139 (K5) and l.142 (K8). The lines below quote those rows.
2. **S1 stays at r7.** The shared changes in `sketch_common.py` touch S1 in three places: cover sampling (plan only), the `label_side` column (no S1 row carries it) and the left-edge re-anchor (left labels only). S1 r7 was redrawn with the r4 code, and all four PNGs are pixel-equal to the r7 PNGs from r3 (MEASURED, numpy array equality). The S1 r7 record was re-run so it cites the r4 control tally (TP1.2-14 practice). No S1 revision opens.
3. **N2 (ring rim through the guide arms) is not a drawing-order error.**
   - The arms (z order 9) are drawn above the ring (5).
   - The arms are unfilled, so the ring rim under them shows.
   - K8 cover reads the ring annulus as partly visible, and a partly visible solid piece is legal.
   - Drawing its covered arc dashed needs either opaque cover fills or a dashed overlay copy above them. Either way, every hidden dashed piece under the arms (anchor arms, descent pad and post) would also need to move above those fills.

   That is a general hidden-line renderer for solid pieces under unfilled covers. It is listed for S3 with the Topologist, and nothing is changed here.
4. **Runtime.** TP1.2-16 sets the cover grid step to the short side / 12, capped at 2.5 mm. This raises the controls run from 446 s (r3) to 734 s (MEASURED). The fine grid is what resolves the 5 x 60 strips.
5. **Red-first, MEASURED.** Each new B was run on the r3 modules kept in the scratchpad before the change (`pre_r4/`), with params read from the project.
   - With the r4 specs, every new B is NO MATCH. K8-B37 and K8-B38 fire only "unknown predicate 'outline_matches'". K5-B17 and K5-B18 read clean (r3 skips sub-gids in K5). K9-B7 fires 2 against 1 planted, because r3 also flags `base_plate:outline`.
   - With the r3 specs, K8-B39, B40 and B41 read clean, "188 predicate(s) hold". The r3 converse ignored opacity, the r3 grid missed the strips, and r3 had no owner lint.

Tags: run results MEASURED 2026-11-25 on `docs/sketches/`, Python 3.12, matplotlib 3.11.2. Hand values DERIVED. Design values DECLARED, or ASSUMED as in the overlay.

## 1 Disposition per finding

| Finding | Source | Fix | Check | B (Z) |
|---|---|---|---|---|
| Plate notch outline | Designer sign-off r3 ruling (M1 S2 r2 N2) | Base plate row gets `outline_matches`. `s2_plan.py` draws one unfilled Polygon, gid `base_plate:outline`, at bracket weight (1, dark grey), z order 3 above the plate tint. Its ring comes from `sc.union_boundary` over the plan_poly pieces: 12 vertices, 644 x 608 with both 70 x 65 notches (MEASURED). The fixture drawing builds its own ring (`_notch_ring`, independent code). | K5 outline admission (plate row with plan_poly, unfilled Polygon, one, predicate present); K8 `outline_matches` (same vertex count, same orientation, one cyclic shift within 0.05); K9 sub-gid on an existing row | K8-B37 plain rectangle (B1). K8-B38 notch offset 5 (B2). K5-B17 two outlines (B3). K5-B18 no predicate (B4). K9-B7 `base_plate2:outline`. Z: K5-Z3, K8-Z6, K9-Z3 (live S2 fixture), K8-Z8 (live script) |
| TP1.2-15 rail-top copy masked by the sector | Topologist re-check r3 | The sector fill is drawn translucent (alpha 0.5, option (a)). The converse now also requires that the solid piece showing a visible sample lies under no opaque fill of another row drawn above it. | K8 cover converse (opacity, `is_opaque`) | K8-B39 sector opaque, as r3. Z: K8-Z8 |
| TP1.2-16 grid misses thin strips | Topologist | Grid step = short side / 12, capped at 2.5. Samples per piece are capped at 20000. The -Y rail is now partial: the two 5 x 60 strips beside member c are visible, so the rail gets a solid copy under the plate. | K8 cover | K8-B40 -Y rail copy removed (on r3 the rail read hidden). Z: K8-Z8 |
| TP1.2-17 unrestricted stand_in | Topologist | `plan_style: stand_in` is honoured only with a non-empty `stand_in_owner`. Without one, the cover check reports a spec error and voids the exemption. Ties: "Step 2: rod top support (guide.top_support ASSUMED; Designer 1.2 (b) FIX 1)". | K8 cover lint | K8-B41 tie a without an owner (lint plus converse, planted 2). Z: K8-Z8 |
| M1 S2 r3 N1 descent-stop leader | Designer M1 S2 r3 | New row field `label_side: left` puts the label in a left column. Its leader ends on the pad's left edge, clear of member a's hatch (re-anchor from the left edge), at (-201.20, 81.52), 166 mm from the column (MEASURED; r3 about 520). | K4 rules (unchanged) apply to both columns | Z: K4-Z3 |
| M1 S2 r3 N2 ring rim through the arms | Designer M1 S2 r3 | Not a drawing-order error (Correction 3). Listed for S3. | none | none |
| Fixture K8-B34 | own | The r4 split adds a -Y rail copy too. K8-B34 now removes the +Y copy only, so the planted count stays 1. | | |

Rules for signature before M1:

| Rule | Premise check | Raiser |
|---|---|---|
| K5 outline admission and K8 `outline_matches` | `outline_matches` (K8-B37, B38); admission requires it (K5-B18) | The Designer |
| K8 cover converse, opacity clause | `is_opaque` from the drawn artist's fill and alpha (K8-B39) | The Topologist (TP1.2-15) |
| K8 cover grid from the short side | K8-B40 | The Topologist (TP1.2-16) |
| `stand_in_owner` lint | K8-B41 | The Topologist (TP1.2-17) |
| Spec field `label_side: left` | K4 (a') to (d) on the left column (K4-Z3) | The Designer (N1) |

Spec changes for Designer re-sign (`s2_spec.yaml`): `outline_matches` on base_plate; `stand_in_owner` on guide_tie_a/_b; `label_side: left` on descent_stop; status text. S1 spec unchanged.

## 2 Files changed

| File | Change |
|---|---|
| `docs/sketches/sketch_common.py` | `OUTLINE_SUFFIX`, `SUB_SUFFIXES`, `outline_admission_issue`, `union_boundary`, `outline_matches_issue`; K5 and K9 sub-gid generalised; `is_opaque`; cover converse with opacity and owner lint; `_piece_samples` grid from the short side (`COVER_STEP_MAX` 2.5, `COVER_SAMPLES_MAX`); `_stack_z`, left label column, left-edge re-anchor |
| `docs/sketches/s2_plan.py` | sector alpha 0.5; `_plate_outline` |
| `docs/sketches/s2_spec.yaml` | section 1 |
| `docs/sketches/fixtures/builders.py` | `_notch_ring`, outline in the S2 fixture drawing; 8 new builders; K8-B34 removes the +Y copy only |
| `docs/sketches/fixtures/manifest.yaml` | 8 entries |

## 3 Check results

New controls (8): K8-B37 to B41, K5-B17, K5-B18, K9-B7.

**Controls** (final run): exit 0, **230/230 matched** (Z 64/64, B 164/164, smoke 2/2), 734 s. The first r4 run matched 229/230. K8-B34 fired 2 against 1 planted, because the r4 split also gives the -Y rail a copy and the fixture removed both copies. The fixture now removes the +Y copy only.

**S2 r4** (`check_sketch.py s2 --rev 4`, after the controls run): **17/17 pass**. K4 14 labels. K5 105 artists. K7 1292 plan tests. K8 190 predicates, including outline_matches and cover. S2-5b 10 moving parts, least 19.84 (drill_head). S2-1 to S2-6 values equal to r3.

**S1 r7** (re-run on the r4 code, record rewritten with the r4 tally): **18/18 pass**. The four PNGs are pixel-equal to the r3-code r7 PNGs.

**Stale**: one difference, `sketches/s1_checks_r4.json: frame_upper.radius recorded 300, live 274`. With `--include-unaccepted`: 10 records checked, the same single difference.

PNG: `docs/sketches/wip/s2_plan_r4.png`. Records: `wip/s2_checks_r4.json` and `wip/s2_summary_r4.md`; `wip/s1_checks_r7.json` re-run.

## 4 Open items

1. N2 (Correction 3): a hidden-line renderer for solid pieces under unfilled covers. S3, with the Topologist.
2. Runtime (Correction 4): the cover grid could sample only near cover edges that cross a piece (the Topologist's alternative). That is an S3 item if runtime matters.

## Gameplan lines to change

**l.138** (K4 row, end of the rule text; Designer sign-off r3).

Old:
```
Designer M1 S2 r2 F1, S1 r6 F1) |
```
New:
```
Designer M1 S2 r2 F1, S1 r6 F1); red-first for K4-B9 to B11 MEASURED by branch deletion (Designer sign-off r3); a row may set label_side: left, a left label column under the same rules (1.2 (h) r4, Designer M1 S2 r3 N1) |
```

**l.139** (K5 row, rule text).

Old:
```
only when the row carries K8 ticks_radial (Designer M1 r1 F1) |
```
New:
```
only when the row carries K8 ticks_radial (Designer M1 r1 F1); a base_plate row admits one unfilled Polygon base_plate:outline only when the row carries K8 outline_matches (Designer sign-off r3, M1 S2 r2 N2) |
```

**l.139** (K5 row, B column).

Old:
```
K5-B16 two tick collections |
```
New:
```
K5-B16 two tick collections; K5-B17 two plate outlines; K5-B18 plate outline without outline_matches |
```

**l.142** (K8 row, rule text).

Old:
```
rows with plan_style: stand_in exempt (Topologist TP1.2-13) |
```
New:
```
rows with plan_style: stand_in exempt (Topologist TP1.2-13); r4: the solid piece that shows a visible sample lies under no opaque fill of another row drawn above it (TP1.2-15); grid step the short side / 12, at most 2.5 (TP1.2-16); stand_in counts only with a stand_in_owner, else a spec error (TP1.2-17); outline_matches, the base_plate:outline ring equals the boundary of the union of the plan_poly pieces within 0.05 (Designer sign-off r3) |
```

**l.142** (K8 row, B column).

Old:
```
B36 bar with an open middle (probe p4) |
```
New:
```
B36 bar with an open middle (probe p4); B37 outline as a plain rectangle; B38 outline notch 5 deeper; B39 opaque sector over the rail-top copy; B40 -Y rail strips beside member c drawn dashed only; B41 stand_in without an owner |
```

**l.143** (K9 row, rule text).

Old:
```
a <row>:ticks sub-artist of an existing row is not a stray (K5 rules its admission; 1.2 (h)) |
```
New:
```
a <row>:ticks or <row>:outline sub-artist of an existing row is not a stray (K5 rules its admission; 1.2 (h)) |
```

**l.143** (K9 row, B column).

Old:
```
K9-B6 ticks under a row the spec does not have |
```
New:
```
K9-B6 ticks under a row the spec does not have; K9-B7 outline under a row the spec does not have |
```

**l.146** (K table summary, end).

Old:
```
K4-Z4, K4-B9 to B11 (222 controls: Z 64, B 156, smoke 2; 446 s).
```
New:
```
K4-Z4, K4-B9 to B11 (222 controls: Z 64, B 156, smoke 2; 446 s). Step 1.2 (h) r4 (`research/sean/cr_scratch/step1.2_engineer_revision_r4.md`) added K8-B37 to B41, K5-B17, K5-B18, K9-B7 (230 controls: Z 64, B 164, smoke 2; 734 s).
```

**Progress Log** (insert after the latest 1.2 row; anchor the r3 P9 row if applied, else l.494).

New row:
```
| 1.2 | 2026-11-25 | (h) P9 r4 (`step1.2_engineer_revision_r4.md`): S2 r4 (S1 stays r7, PNGs pixel-equal under the r4 code): plate notch outline (K5 admission, K8 outline_matches, K9 sub-gid; Designer sign-off r3), TP1.2-15 (sector translucent; converse requires no opaque fill over the showing piece), TP1.2-16 (grid step short side / 12, at most 2.5; -Y rail strips beside member c now split solid), TP1.2-17 (stand_in_owner lint), M1 S2 r3 N1 (descent-stop label in a left column, leader 166), N2 listed (not a drawing-order error; S3). Red-first of all 8 new B MEASURED on the kept r3 modules. S2 r4 17/17, S1 r7 18/18 (record re-run), controls 230/230 in 734 s, --stale red on s1 r4 frame_upper.radius only. |
```
