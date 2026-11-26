## Corrections to the brief

1. **Image sizes are width x height 2634 x 1505 (r7) and 2332 x 1505 (r6).** The P1Rf report ("1505 x 2634") and my P1Rd sign-off ("1505 x 2332", "1487 x 2362") give height first. The figure is landscape. MEASURED (PIL).
2. **The DR-1 premise is already bounded in the code, more narrowly than the P1Rf text states it.** P1Rf Correction 1 says the convention line of a stand_in row "counts as visible ink". In `sketch_common.row_visibility` the stand-in artist enters the solid list with `artist_covers(cc, a, fid)`. `anchor_visibility_issue` then rejects an anchor on that line where it lies under a cover of the artist (a true outline of a row higher by more than 0.05, or an opaque fill drawn above). The rule as coded is: a stand-in's line is visible ink where no nearer outline or opaque fill covers it. No control exercises that bound (section 2).
3. **My K4-B16 forecast was wrong.** I forecast "unplaceable" on the P1R code. The measured P1R result is the gear outline line, and on P1Rf code (g) also fires (planted 2). Accepted as P1Rf Correction 2 states it.
4. **Two leader pairs on r7 fail at 100 percent and K4 passes them.** No K4 clause bounds the distance between two leaders that do not cross (section 3, FIX D4).

Images read: `docs/sketches/wip/s2_plan_r7.png` (2634 x 1505) beside `docs/sketches/wip/s2_plan_r6.png` (2332 x 1505), full frame and crops at 2x to 4x. Pixel scale 1.38 px/mm, origin at about px (1047, 648) on r7 (DERIVED: r6 origin (745, 648) plus the 302 px the left column grew; the 0 and 100 tick labels agree within 1 px). Code read: `docs/sketches/sketch_common.py` l.218-219, 523-595, 3359-3371; `s2_plan.py` l.96; `s2_spec.yaml` l.90-102, 734, 1369; `fixtures/manifest.yaml` l.374-376; `wip/s2_summary_r7.md` l.86-101.

## 1 D1, D2, D3 on r7 and in docs/sketches/

| Item | Evidence | Verdict |
|---|---|---|
| D1 (e1), (e2), enclosure | `outline_encloses` (annulus: r <= b; polys: inside a convex piece), `counted_outlines`, `row_visibility`, `anchor_visibility_issue` present. Ring leader on r7 anchors at (205.96, -40.97) on solid rim, about 11 mm below the bottom edge of the right tie (DERIVED from pixels, +-1 mm); the rim is solid there and dashed only inside the tie. Its leader runs down-right to "ring OD 420" and enters no counted outline. | **CLOSED** |
| D1 (g) | `cover_name_issue` reads the spec `name` of a counted row that contains or encloses the anchor. | **CLOSED** |
| K4-B14, B15, B16 | manifest l.374-376 with reason substrings and planted counts 3, 1, 2; red-first on P1R `sketch_common.py` reported in P1Rf section 3; `--controls` 282, all match (P1Rf section 4). | **CLOSED** |
| D2 drill_head | Spec l.1369 suffix "(dotted, under ring gear)". Drawn "cutter OD ASSUMED 177.8 (dotted, under ring gear)", right column, leader from (88.90, 0.00). | **CLOSED** (leader legibility: FIX D4) |
| D2 descent_stop | Spec l.734 suffix "(dashed, under top-guide bracket arm)". Drawn "descent stop (one pad) r 200 (dashed, under top-guide bracket arm)", left column, text px x 14 to 522, inside the image; leader horizontal at y 112 ends in the white arm at theta 150 beside the dashed pad edges. The text names what the leader ends in. The mid-length crossing of member a's hatch remains (NOTE N2, M1). | **CLOSED** |
| D3 phantom line | `PHANTOM = (0, (12, 3, 3, 3, 3, 3))`, `STAND_IN_COLOR = "#8c510a"`, used by `s2_plan.py` l.96 with no fill. On r7 both ties read as long dash and two short dashes in brown around a white top face; the hue separates them from hidden black and rim blue at 100 percent. The white face with a phantom edge reads as a provisional visible part. | **CLOSED** |
| D3 legend | "phantom, brown: Step 2 stand-in (rod top ties)" between the dotted and dashed-tick lines. | **CLOSED** |

## 2 DR-1 premise: stand-in line as visible ink

**SIGNED, as coded** (Correction 2): a stand_in row's convention line is visible ink for (e1) where no cover of its artist (a nearer true outline, or an opaque fill drawn above) lies over it.

- Basis: the line is the only ink of a visible part. The ties are the topmost rows (z_max 1285 z_S, DECLARED), and on r7 they lie outside the operator sector, so no counted outline or opaque fill covers them. Under D3 the phantom line is the drafting convention for a visible provisional part. An (e1) that found no visible ink on the ties would declare a visible part hidden, which contradicts D3.
- Premise enforcement (detail 1 common (h)): the cover bound is the premise that keeps a stand-in under a nearer part from anchoring on hidden ink. It has no B. **FIX D5** adds K4-B17: guide_tie_a with a planted row higher than 1285 whose outline covers the tie's top edge, and the label anchor forced onto the covered stretch. It fires "(e1)", planted 1. Red-first: K4-B17 shown red by deleting the `artist_covers` term for stand-in artists in `row_visibility` (the converse-by-deletion method of TP1.2-15), and clean on the live code. Check code only; no pixel change.

## 3 Delta read of r7 against r6

**W6, FIX D4: two leaders fork off the tube OD leader.** The P1Rf drill_tube anchor moved to an ink sample at (76.15, 1.87). Its leader runs horizontal at y about 1.9 to the column (px row 646 from x 1170 to 1552, MEASURED).
- (a) The drill_head anchor (88.90, 0.00) lies 1.87 mm (2.6 px) below that leader (DERIVED from the declared anchors). The cutter leader slopes down at about 0.087 and stays within 5 px of the tube leader for its first 22 mm (DERIVED). At 100 percent the cutter leader reads as a branch of the tube OD leader, and its anchor on the dotted cutter rim cannot be seen.
- (b) The base plate leader starts at the plate x edge, px (about 1494, 649), 3 px (about 2.2 mm) below the point where the tube leader crosses that edge (px row 646; MEASURED, +-1 px). It then slopes to "base plate (open), x 644". At 100 percent it reads as a kink in the tube OD leader. On r6 the base plate leader was horizontal and stood apart; this is the restack after the longer cutter text and the drill_tube move.
- K4 passes both because rule (b) judges crossings only. Read as drawn, the tube OD leader appears to point at the plate edge and at the cutter rim. That is the DN30 class of misreading: a leader read as pointing at a part it does not label.
- **FIX D4 (K4 clause (h), leader separation).** Any two plan leaders keep at least 4.0 mm apart (DECLARED; 5.5 px at 1.38 px/mm, two line widths plus a visible gap at dpi 150). A leader's anchor end counts as part of it. The placer treats a separation failure as it treats a crossing: the next candidate, then re-judge after stacking.
  - Premise: leaders are straight segments in plan mm, and the distance is segment to segment.
  - Z: K4-Z3 on the live S2 after D4.
  - B, K4-B18: the r7 layout forced (drill_tube at (76.15, 1.87), base_plate and drill_head at their r7 anchors). It fires "(h)" for drill_tube|drill_head and drill_tube|base_plate, planted 2. Red on the P1Rf code (clean there: K4 19/19 on r7).
- **Dry-run DR-4** (scratchpad copy, before any revision opens, detail 1 common (h)):
  1. Apply D4 and D5.
  2. Run `s2_plan.py` and `check_sketch.py s2`. Report K3 and K4 with no UNPLACEABLE, every label's anchor, and the least leader-to-leader distance per label.
  3. Run `--controls`: K4-B17, B18 red-first and match; K4-B7 to B16 counts stated where (h) adds a line.
  4. If 4.0 mm leaves a label UNPLACEABLE, report the least separation that places all 14. Do not choose the value; it returns to me.
  - D4 moves pixels, so it opens S2 r8 and the fresh M1 runs on r8.

**Other changes against r6: no new defect.**

| Place | r7 reading | Verdict |
|---|---|---|
| Right column text | Six rows at 26 px pitch, no glyph overlap. The base plate and cutter leaders end on the top edge of their own text box, 15 to 60 px right of the text start and 6 px below the row above (MEASURED). r6 had one such end (tube OD). | NOTE N4: readable, because each end touches its own text. If D4 restacks the column, prefer ends on the left edge. Not blocking. |
| Left column | Long descent-stop text clears the y tick labels; its leader passes 16 px above the "100" tick label. | Accepted (N3 unchanged). |
| Ring leader | Crosses no leader and no tie. | Accepted. |
| Rod top tie leader | Horizontal at about y 100 to the tie's top-right corner on the phantom line. No crossing. | Accepted. |
| Cutter and keep-out leaders mid-length | Pass through the right tie interior and over the dashed guide lug and bushing. Mid-length only, outside the last quarter (rule (e)). | Accepted (M1 item with N2). |
| Fill and colour | Unchanged from r6 except the tie edges. N1 (ring face colour) stays open. | No change. |

## 4 reported_items as landed (DR-3)

`s2_spec.yaml` l.90-102 carries the 12 ids in the signed order. `wip/s2_summary_r7.md` l.86-101 carries the table, and every value equals my r6 column within 0.01 (0.01 m for f6_eye_limits), MEASURED against P1Rd section 5. The f6 basis (ring z_min 374.84 at capture_end) is the one I used. Highest point at capture_end is guide_tie_b 1285.00 z_S (stand-in counted as a part, reference rows excluded): consistent with LF1.2-5. The s2_5b list now carries 10 rows with drill_head 19.84 least, which matches.

**reported_items values SIGNED.** NOTE N5: the summary prints "2.7" and "10.0" where the spec text implies two decimals ("2.70", "10.00"). The values are equal; this is format only, so it is not blocking.

## Verdict

**FIX 2** (D4, D5).
- D1, D2 and D3 are CLOSED on r7 and in `docs/sketches/`.
- The DR-1 premise is SIGNED as coded, with its cover bound. D5 adds the B control the premise lacks; it changes check code only.
- reported_items are SIGNED.
- D4 needs DR-4 and opens S2 r8, with the fresh M1 on r8 (P8, KC11).
- NOTEs N1 to N5 do not block.
- I re-check D4 and D5 on the DR-4 result and the r8 pixels.

## Gameplan lines to change

**l.138 (K4 row), rule cell.** Apply after the P1Rf new text for the same cell. Old is the end of the P1Rf new text:
```
contains or encloses the anchor (1.3 P1Rf) |
```
New:
```
contains or encloses the anchor (1.3 P1Rf); a stand-in's convention line is visible ink for (e1) only where no cover of its artist lies over it (Designer P1Rf re-check, FIX D5); (h) any two plan leaders, anchor ends included, keep at least 4.0 mm apart, judged and placed as a crossing is (Designer P1Rf re-check FIX D4; S2 r7 tube OD leader 1.87 mm from the cutter anchor) |
```

**l.138 (K4 row), B cell.** Apply after the P1Rf new text for the same cell. Old is the end of the P1Rf new text:
```
K4-B8 re-planted at 1.3 P1Rf (texts below the anchors in reverse radial order) |
```
New:
```
K4-B8 re-planted at 1.3 P1Rf (texts below the anchors in reverse radial order); K4-B17 tie a label anchored on its phantom line under a planted nearer outline (e1, FIX D5); K4-B18 the r7 layout forced, tube OD leader within 4 mm of the drill_head and base_plate leaders (h, FIX D4) |
```

**l.667 (Design Notes 25, TP1.2-18/19 and N2 renderer row).** Apply after the P1Rf change. Old is the end of the P1Rf new text:
```
stand-ins as a brown phantom line (D3) landed in S2 r7; awaiting the P1Rf re-checks |
```
New:
```
stand-ins as a brown phantom line (D3) landed in S2 r7; Designer re-check: D1 to D3 closed, stand-in visible-ink premise signed with its cover bound, reported_items signed, FIX D4 (leader separation 4.0 mm, K4 (h)) and D5 (K4-B17) through DR-4 to S2 r8 |
```
