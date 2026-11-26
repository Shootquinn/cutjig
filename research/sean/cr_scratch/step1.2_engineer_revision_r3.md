# Step 1.2 (h) Engineer: S2 r3 and S1 r7

## Corrections to the brief

1. **The literal K4 rule from the M1 file does not catch S1 r6 F1.** At capture_end the core 750 anchor (50.00, 477.50) lies on the core edge, and no filled or hatched area contains it. Every area on the leader's path (gear, pinion_b, NEMA 23, hub, tube) is drawn at z order 1, under the leader at 3 (MEASURED, live build). What loses the leader is its last quarter running through the pinion_b and gear hatch. Two rules are added and both are tested:
   - the l.138 wording proposed in the M1 file, for areas drawn over a leader or an anchor;
   - a hatch rule: no more than a quarter of the samples in the last quarter of a leader may lie in another row's hatch.

   A thread strip such as screw_b passes the hatch rule. Applied with no share limit, the rule moved 13 S1 anchors and created leader crossings (MEASURED, trial). The 25 % limit moves only core 750 at capture_end, to (50.00, 540.00).
2. **"Partly visible part drawn solid" applied literally would undo F2 for the pinions.** The pinion toothed piece is partly visible (heel corners at r 133.07 outside the gear OD 126.32). The fix takes the brief's second option: split the piece. A dashed piece that is partly visible gets a solid copy just under the lowest covering fill. The fill then hides the covered part and the dashed piece above it shows that part, so the visible area reads solid and the hidden area dashed. Live cases: the base-frame +Y rail top in the column notch, and the three pinion toothed pieces.
3. **The Step 2 ties are partly visible and dashed by convention.** The converse rule would fire on them. A new row field, `plan_style: stand_in`, exempts them, and K8-B35 holds the exemption to the spec field.
4. **Red-first for the r3 B controls is DERIVED.** The r2 module was not kept, so the controls could not be re-run on it. None of the new branches existed at r2, and probe p4 (K8-B36) read hidden under r2's vertex-only samples (Topologist re-check r2, MEASURED there).
5. **Runtime cause.** The jump to 1640 s did not come from K7. It came from r2's `hidden_rows`, called in every S2 fixture drawing, and from K8 cover. Both used `outline_outside` (an edge-distance computation) where an inside test suffices, with no bounding-box prefilter. MEASURED on the live S2 fixture:
   - drawing: 28.4 s to 2.6 s;
   - K8: 12.9 s to 2.1 s.

   K7 per-test logging costs little: S2 K7 3.4 s, S1 K7 7.0 s.

Tags: run results MEASURED 2026-11-25 on `docs/sketches/`, Python 3.12, matplotlib 3.11.2. Hand values DERIVED. Design values DECLARED, or ASSUMED as in the overlay.

## 1 Disposition per finding

| Finding | Source | Fix | Check | B (Z) |
|---|---|---|---|---|
| FIX R2-1 tick toe | Loftsman re-check r2; Design Notes 29 | `ticks_radial` r_in = `pinion.r_toe` (96.54). Source text rewritten. Gear shape text "toe r 96.54 to heel r 125 along the gear pitch cone". Ticks drawn 96.54 to 125.00. | K8 `ticks_radial` (unchanged) | K8-B30 reason now "[96.54, 130.00] outside [96.54, 125.00]". Z: K8-Z6 |
| NOTE R2-1 S1 class | Loftsman | `s1_spec.yaml` gear_hub declares pinion_a and pinion_b G, g_min 3, ASSUMED, with the S2 source text. S1 has no pinion_c row. | K7 (S1) | (existing K7 G controls). Z: K7-Z11 and S1 live |
| NOTE R2-2 record wording | Loftsman | Side view: a plan-footprint basis reads "plan footprint (circumscribed 128-gon)" when either footprint is round or a depth disk, "(hull of plan_poly pieces)" for several pieces, else "(spec placement, exact)". z band and depth band entries carry `distance: null` and `overlap: null`. | K7 record lint (unchanged) | Z: K7-Z16, K7-Z17 |
| TP1.2-13 over-cover | Topologist re-check r2 | Cover samples now include a 12 x 12 interior grid per piece (an annulus: 5 rings across the width). Each drawn artist is classified hidden, partial or visible (`plan_cover_states`), and the drawings restyle per artist (`style_hidden`). K8 cover gains the converse: a non-solid artist with an uncovered sample outside every solid piece of its row fires. The S2 split is in Correction 2; the ties are exempt (Correction 3). | K8 cover (hidden drawn solid; partly visible drawn dashed) | K8-B34 base-frame rail top dashed only (as r2). K8-B35 ties without stand_in. K8-B36 probe p4, a bar with an open middle. Z: K8-Z8 live S2 script, K8-Z6, K8-Z7 |
| TP1.2-14 stale tally | Topologist | The S2 r3 and S1 r7 records are written after the final controls run, so they cite its tally. | none | none |
| M1 S2 r2 F1 leaders under the gear fill | Designer M1 S2 r2 | All label annotations at z order 100 (`LEADER_ZORDER`), above every area. K4 (a'): the anchor lies under no area of another row drawn above that row's ink. K4 (c): no area drawn above a leader where it runs. | K4 | K4-B10 filled area over the tube OD leader. K4-B11 filled area of another row over the tube OD anchor. Z: K4-Z3, K4-Z4 |
| M1 S1 r6 F1 core 750 leader | Designer M1 S1 r6 | K4 (d), the hatch rule in Correction 1. `place_labels` re-anchors a label whose leader end fails (d) before stacking. It searches the row's ink with points on the first anchor's edge first, then the nearest. Core 750 at capture_end: (50.00, 477.50) to (50.00, 540.00), between the gear top and the core top as the M1 file asks. | K4 | K4-B9 core 750 at the r6 anchor: "label leader ends across the hatch of gear". Z: K4-Z4 |
| M1 S1 N1 tube OD leader on the keep-out line | Designer M1 S1 r6 | Fixed by the z order: the anchor was on the tube wall (76.20, MEASURED). The leader end was hidden under fills drawn above it at r6, and it now draws on top. | K4 (c) | as F1 |
| M1 S2 N1 pinion c tag on slot line C | Designer M1 S2 r2 | Each pinion tag sits beside its NEMA 23, at mid-length and a half-width plus one profile width off the axis. The script takes the side farther from the guide rods and the F6 sightline. Tags: a (-112, -167), b (112, -167), c (-88, 180). | visual only | none |
| M1 S2 N2 notch outline | Designer M1 S2 r2 | Listed, not done. A plate outline needs a K5 admission for a non-rectangle base_plate sub-artist (a new rule with Z and B). Outlining the five plate pieces instead would draw false seams. The visible rail-top piece in the notch now draws solid (TP1.2-13), which marks the notch floor. | none | none |
| M1 S2 N3 nut under the guide block | Designer M1 S2 r2 | Legend: "nut flanges under the guide blocks". | visual only | none |
| Runtime | coordinator | Correction 5: `outline_contains` (inside test) in place of distance; bbox prefilter per cover; the cover table shared per figure. No result changes: controls match the same Z and B with the same planted counts. One reason string changed because the cover list now names both rows (K8-B32: "guide_a, screw_a"). | none | none |

Rules for signature before M1:

| Rule | Premise check | Raiser |
|---|---|---|
| K8 cover converse with split and the `plan_style: stand_in` field | interior-grid samples (K8-B36); stand-in held to the spec field (K8-B35) | The Topologist (TP1.2-13); the Designer for the split drawing convention |
| K4 (a') anchor under no area, (c) no area over a leader, (d) leader end clear of hatch (25 % / 25 %) | z order read from the drawn artists (K4-B10, B11); hatch share (K4-B9; screw thread strip passes, K4-Z4) | The Designer (M1 S2 r2 F1, S1 r6 F1) |

Spec changes for Designer re-sign:
- `s2_spec.yaml`: `ticks_radial` r_in, gear shape text, `plan_style: stand_in` on guide_tie_a/_b, status text.
- `s1_spec.yaml`: gear_hub pinion_a/_b G 3.

No params or overlay value changed.

## 2 Files changed

| File | Change |
|---|---|
| `docs/sketches/sketch_common.py` | cover: `_piece_samples`, `outline_contains`, `cover_table`, `_covers_of`, `_covered_by`, `artist_cover`, `plan_cover_states`, `style_hidden`, converse in `cover_issues`; labels: `LEADER_ZORDER`, `_rank`, `is_area`, `covering_areas`, `hatch_areas`, `leader_hatch`, `_reanchor`, anchor search in `label_anchor`, hatch re-anchor in `place_labels`, K4 (a'), (c), (d); record: `_fp_basis`, null distance on band entries |
| `docs/sketches/s2_plan.py` | `_hidden_lines` (style_hidden plus solid copies of partly visible dashed pieces); pinion tags; legend |
| `docs/sketches/s2_spec.yaml`, `s1_spec.yaml` | section 1 |
| `docs/sketches/fixtures/builders.py` | S2 fixture drawing via `style_hidden`; 8 new builders; K4-B9 at the r6 anchor |
| `docs/sketches/fixtures/manifest.yaml` | 8 entries; K8-B30 and K8-B32 reason strings |

## 3 Check results

New controls (8): K8-Z8, K8-B34, K8-B35, K8-B36, K4-Z4, K4-B9, K4-B10, K4-B11.

**Controls** (`check_sketch.py --controls`, final run): exit 0, **222/222 matched** (Z 64/64, B 156/156, smoke 2/2), 446 s. The first r3 run matched 221/222: K8-B32 fired as planted, but its reason now lists both covers, "guide_a, screw_a". The manifest string was updated.

**S2 r3** (`check_sketch.py s2 --rev 3`, written after the controls run): **17/17 pass**. K4 14 labels. K7 1292 plan tests, 7334 record entries. K8 188 predicates. S2-5b least 19.84 (drill_head). Every other S2 value is equal to r2. The record cites K8 B fired 36/36, Z clean 8/8 (TP1.2-14).

**S1 r7** (`check_sketch.py s1 --rev 7`): **18/18 pass**. K4 55 labels. K7 617 tests (r6 609; the 8 added tests are gear_hub|pinion_a/_b G at four poses, plan-separated 5.198 against 3, basis "plan footprint (circumscribed 128-gon)"), 5556 record entries. S1-1 to S1-7 are equal to r6. The mass report r7 is byte-equal to r6.

**Stale**: `--stale` exit 1, one difference, `sketches/s1_checks_r4.json: frame_upper.radius recorded 300, live 274`. With `--include-unaccepted`: 8 records checked, the same single difference.

Runtime:

| Item | r2 | r3 |
|---|---|---|
| `--controls` | 1640 s | 446 s |
| S2 fixture drawing (`s2_live`) | 28.4 s | 2.6 s |
| K8 on live S2 | 12.9 s | 2.1 s |
| `check_sketch.py s2` | about 58 s | 23 s |
| `check_sketch.py s1` | not timed | 18 s |

PNG paths:
- `docs/sketches/wip/s2_plan_r3.png`
- `docs/sketches/wip/s1_pose_load_r7.png`, `wip/s1_pose_start_r7.png`, `wip/s1_pose_capture_end_r7.png`, `wip/s1_pose_park_r7.png`

Records:
- `wip/s2_checks_r3.json`, `wip/s2_summary_r3.md`
- `wip/s1_checks_r7.json`, `wip/s1_summary_r7.md`, `wip/s1_mass_report_r7.json`

## 4 Open items

1. M1 S2 N2 (notch outline): this needs a K5 sub-artist admission. That is the Designer's call; it is not done.
2. TP1.2-7 (hollow disks counted as true cover for drill_tube and drill_head) is unchanged and stays with S3/S6. Its only effect is on the cutter rim, which is truly under the gear hub.

## Gameplan lines to change

**l.138** (K table, K4 row, rule column).

Old:
```
no two leaders cross; a concentric row may set label_theta, the leader azimuth (1.2 (h), Designer M1 r1 F4, F5)
```
New:
```
no two leaders cross; a concentric row may set label_theta, the leader azimuth (1.2 (h), Designer M1 r1 F4, F5); labels draw above every area (z order 100); no area artist (filled or hatched) of another row is drawn above a leader where it runs or above the row's ink at the anchor; at most a quarter of the samples in the last quarter of a leader lie in other rows' hatch, and place_labels re-anchors on the row's ink until it holds (1.2 (h) r3, Designer M1 S2 r2 F1, S1 r6 F1)
```

**l.138** (K table, K4 row, B column).

Old:
```
K4-B8 r1 concentric anchors, three crossings |
```
New:
```
K4-B8 r1 concentric anchors, three crossings; K4-B9 S1 core 750 at the r6 anchor (end in hatch); K4-B10 an area drawn over a leader; K4-B11 an area of another row over an anchor |
```

**l.138** (K table, K4 row, Z column).

Old:
```
K4-Z3 live S2 drawn by s2_plan.py |
```
New:
```
K4-Z3 live S2 drawn by s2_plan.py; K4-Z4 live S1 drawn by s1_side_poses.py |
```

**l.142** (K table, K8 row, rule column).

Old:
```
premise: only true outlines cover (Designer M1 r1 F2 rule, Topologist TP1.2-2, TP1.2-9) |
```
New:
```
premise: only true outlines cover (Designer M1 r1 F2 rule, Topologist TP1.2-2, TP1.2-9); r3: samples are an interior grid plus pulled-in vertices, and the converse holds: a partly visible artist drawn non-solid fires unless a solid piece of its row shows the visible area (the drawing splits it: a solid copy under the covering fill), rows with plan_style: stand_in exempt (Topologist TP1.2-13) |
```

**l.142** (K table, K8 row, B column).

Old:
```
Z7 cover premise (circumscribing circle not counted) and B33 its contrast (circle outline covers) |
```
New:
```
Z7 cover premise (circumscribing circle not counted) and B33 its contrast (circle outline covers); Z8 live S2 script (split pieces); B34 base-frame rail top dashed only; B35 ties without stand_in; B36 bar with an open middle (probe p4) |
```

**l.146** (K table summary paragraph, end).

Old:
```
S2-5b-B2, S2-5b-B3 (214 controls: Z 62, B 150, smoke 2; 1640 s).
```
New:
```
S2-5b-B2, S2-5b-B3 (214 controls: Z 62, B 150, smoke 2; 1640 s). Step 1.2 (h) r3 (`research/sean/cr_scratch/step1.2_engineer_revision_r3.md`) added K8-Z8, K8-B34 to B36, K4-Z4, K4-B9 to B11 (222 controls: Z 64, B 156, smoke 2; 446 s).
```

**l.494** (Progress Log, add a row after it; the l.494 row itself is unchanged).

Old:
```
| 1.2 | 2026-11-25 | r2 reviews:
```
New (row to insert after l.494):
```
| 1.2 | 2026-11-25 | (h) P9 r3 (`step1.2_engineer_revision_r3.md`): S2 r3 and S1 r7 for FIX R2-1 (ticks 96.54 to 125, Design Notes 29), NOTE R2-1 (S1 gear_hub\|pinion G 3), NOTE R2-2 (basis wording, null band distances), TP1.2-13 (grid cover samples; converse with split pieces; plan_style: stand_in), TP1.2-14 (records after controls), M1 S2 r2 F1 and S1 r6 F1 (leaders on top; anchor and leader under no other area; leader end clear of hatch; core 750 re-anchored to z_S 540), N1, N3; N2 listed. S2 r3 17/17, S1 r7 18/18, controls 222/222 in 446 s (r2 1640 s), --stale red on s1 r4 frame_upper.radius only. Rules awaiting signature: Topologist (cover converse), Designer (K4 a', c, d; split convention). Next: P7r, P8r. |
```
