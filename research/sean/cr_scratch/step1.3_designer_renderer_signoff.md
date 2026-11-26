## Corrections to the brief

1. **The anchor exemption in rule (e) moved the Design Notes 30 defect onto the ring label.** P1R re-anchored "ring OD 420" from (210, 0) to (209.75, -10.33) because the r5 leader ends 19.9 mm inside guide_member. The new anchor is on a dashed (hidden) stretch of the rim, inside the true outline of guide_tie_a (tie drawn x about 200.7 to 266, y about -30 to 96 on r6; DERIVED from pixels, +-1.5 mm). Rule (e) exempts that outline because it contains the anchor. On r6 the leader's last quarter (about 39 mm of a 155 mm leader, DERIVED from pixels) runs wholly inside tie a and ends on a dashed arc next to the guide lug square. At 100 percent it reads as pointing at the tie or the lug. The ring has visible rim on both sides of the tie. Premise 3 in section 4 ("an outline that contains the anchor is exempt") holds for a part with no visible ink. For a partly visible row it lets the placer pick hidden ink. FIX D1.
2. **The descent-stop leader on r6 has the same reading.** The pad is wholly hidden (P1R section 2 list). The leader runs at y 112.1 from the left column to (-166.21, 112.12). Its last quarter (about 49 mm, x -215 to -166; DERIVED) lies inside bracket_guide_a, the white arm at theta 150, and crosses the dashed rim. It passes the rule only because the arm and the ring contain the anchor. For a wholly hidden part this is unavoidable. The label text has to say what the reader is looking through (FIX D2). Mid-length, the same leader also crosses 58 mm of frame_upper_a's hatch (x -279 to -221; DERIVED). Rule (d) does not police this, because it falls outside the end quarter (NOTE N2).
3. **drill_head fails because the gear and ring enclose the cutter rim; neither covers it.** The rim at r 88.9 sits under gear_hub (76.2 to 90), which contains the anchor and is exempt. The gear annulus (90 to 126.32) and the ring outline lie around the anchor, so any leader from either column must cross them. A rule written on enclosure (outer boundary with holes filled, winding number about the anchor non-zero) exempts them by topology. No value is involved. The tie b case still fails under that rule: tie b neither contains nor encloses the pad anchor (DN30: anchor 3.1 mm outside tie b).
4. **The ties are visible parts drawn in the hidden style.** guide_tie_a and _b are the topmost rows (z_max 1285). They draw dashed because of the r3 plan_style stand_in convention I signed. Before r6 their interiors carried the plate tint and read as see-through outlines. On r6 the renderer removes the plate tint and ring fill under them, so each tie reads as a white top face with a hidden-line edge, which contradicts itself. Under a renderer where dashed means hidden, a visible stand-in needs its own line. FIX D3.

Images read: `docs/sketches/wip/s2_plan_r6.png` (1505 x 2332) and `docs/sketches/s2_plan_r5.png` (1487 x 2362), full frame and seven crops at 2x to 4x. Pixel scale 1.38 px/mm, origin at px (745, 648) (DERIVED from the tick labels). Fill colours are sampled from the PNGs (MEASURED, RGB 0-255).

## 1 Hidden convention as drawn on S2 r6; N2

| Place | r6 reading | Verdict |
|---|---|---|
| Ring rim under the top-guide arms at 30, 150 and the arm at 270 | Rim dashed inside each white arm, solid on either side. | Reads hidden. **N2 (r3 gate NOTE 2) CLOSED.** |
| Ring rim under the NEMA 23 bodies (90, 210, 330) | Rim dashed through the 0.5-alpha motor fill (r5: solid rim showing through). | Reads hidden. Better than r5. |
| Ring rim under the ties | Dashed inside both tall tie outlines. | Reads hidden. |
| Motor shafts under the gear | Visible stub solid; inner end dashed under the gear edge. | Correct. |
| Pinion teeth under the gear, base-frame rails and pockets under the plate, anchor arms, lift motors, lugs, bushings, nut flanges | Dashed, no fill. | Correct. |
| Rail top in the +Y notch | Solid, clipped to the notch. | Visible part reads visible (TP1.2-13 case closed in the drawing). |
| Bearing under the gear; guide-block edges under the screw disks | Not seen. The copies sit under opaque fills (Correction 8). | Accepted (section 2). |
| Plate tint and ring fill under nearer parts | Removed. Unfilled nearer parts read as white top faces. | Reads right: white means the face of the nearest part. |
| guide_tie_a, guide_tie_b (stand-ins, topmost) | Dashed edge around a white face. | **Visible part reads hidden. FIX D3.** |
| Drill tube bore | White (the drill_head solid disk hides the plate; TP1.2-7). | Reads as an open bore, consistent with "base plate (open)". Accepted while TP1.2-7 stays with S3/S6. |

**Hidden copies stay at their own draw order: SIGNED.** An opaque fill means "nothing under this shows". Dashed edges lifted above an opaque fill would contradict the fill and clutter the gear face. A part under an opaque fill is shown in the side views (S1, S3). K9 coverage is unaffected, because the copy exists in the draw order.

Hidden convention item 1 in P1R section 9 (dashed or own non-solid style, no fill, no hatch, clipped to the hidden region; plate tint and ring fill removed under nearer outlines): **SIGNED**, with FIX D3 for the stand-in exception.

## 2 Placer order and the new last-quarter rule

**Placer order and layout steps (P1R section 4): SIGNED.**
- The candidate order (label_side column, label_theta hit, column default, ink samples at most 2 mm apart sorted from the column edge, then by distance from the default) is deterministic.
- Each label takes its first passing candidate, then the layout is re-judged after stacking. Three rounds is enough for 14 labels.
- **NOTE N3:** the left-column clearance from the y tick labels is a placer preference with no check. If it is a requirement, it needs a K3 or K4 clause with Z and B under detail 1 common (h). As a preference it needs nothing more.

**UNPLACEABLE record and the K4 reason "label unplaceable": SIGNED.** It replaces the r5 silent fall-back, which is the failure that produced DN30.

**Rule (e): z premise SIGNED; anchor exemption FIX D1.** The z premise counts only outlines higher by more than 0.05; zones count every outline. A leader that crosses a lower part is ordinary. A leader whose end lies over a nearer part reads as pointing at that part. The exemption must depend on whether the labelled row has visible ink.

**FIX D1 (rule (e), replaces premise 3 of P1R section 4).**
- (e1) **Rows with visible ink.** A row the renderer leaves with any visible ink (solid, not inside a nearer true outline and not under an opaque fill drawn above) anchors on visible ink. The last quarter of its leader lies outside every nearer true outline that does not enclose the anchor. "Encloses" means the outline's outer boundary, holes filled, contains the anchor: an annulus or ring around the labelled part, which every leader must cross.
- (e2) **Wholly hidden rows.** A row the renderer records as wholly hidden anchors on its hidden ink. The last quarter of its leader lies outside every nearer true outline that neither contains nor encloses the anchor.
- (g) **Label text of a wholly hidden row.** The drawn label text of a wholly hidden row contains "under " followed by the `name` of a nearer row whose true outline contains or encloses the anchor. A leader that must end inside a cover then names the cover.
- **Premises:**
  - Visible or hidden is read from the renderer split, which K8 cover certifies (clauses 1 to 3). K4 reads the K8-certified classification and keeps no second one.
  - Enclosure is a winding-number test on the outer ring. For the annulus outline (a, b), it is r <= b.
- **Controls** (each B shown red on the P1R code before the change):
  - K4-Z3, live S2 after D2: clean.
  - K4-B14: ring label forced to the r6 anchor (209.75, -10.33). Fires (e1) "anchor on hidden ink of a row with visible ink" (P1R code: passes, because tie a is exempt).
  - K4-B15: the D2 drill_head suffix removed. Fires (g) (P1R code: no clause (g)).
  - K4-B16: gear outline planted as an open C annulus 90 to 126.32 spanning -170 to 170 deg, so it does not enclose the anchor at theta 0. Fires (e2) "end inside outline / gear" (P1R code: reports "unplaceable", without the planted reason).
  - K4-B12 (tie b, DN30) still fires with its reason: tie b neither contains nor encloses (-201.20, 81.52).

## 3 UNPLACEABLE label: remedy

**drill_head "cutter OD ASSUMED 177.8": FIX D2 (field value), together with FIX D1.**
- Set `label.suffix: "(dotted, under ring gear)"` on drill_head. The drawn text becomes "cutter OD ASSUMED 177.8 (dotted, under ring gear)". gear's spec name is "ring gear", and the gear encloses the anchor.
- Under D1 (e2), gear and ring are exempt by enclosure and gear_hub by containment. The first candidate, label_theta 0 at (88.90, 0.00), failed only on gear (36.0 mm) and ring (58.5 mm) (K4 record, MEASURED by P1R). It is expected to pass. Rule (b), crossings, is still to be judged after stacking.
- A numbered callout and a label in the tube bore were rejected. The bore holds the datum cross, the theta arc and the axis arrows, and the hub band at r 76.2 to 90 is 19 px wide with the keep-out and tube circles in it.

**descent_stop: same remedy, FIX D2.** Set `label.suffix: "(dashed, under top-guide bracket arm)"`. bracket_guide_a's name is "top-guide bracket arm", and it contains the anchor. The drawn text becomes "descent stop (one pad) r 200 (dashed, under top-guide bracket arm)". The leader into the arm is then a stated reading.

**Dry-run DR-1** (the Engineer runs it in a scratchpad copy of `docs/sketches/` before any revision opens; detail 1 common (h)):
1. Apply D1 (e1, e2, g), the two D2 suffixes and the controls K4-B14 to B16.
2. Run `s2_plan.py --rev 6` and `check_sketch.py s2 --rev 6` in the copy. Report:
   - K3 (both longer texts inside the saved image; the left column grows leftward) and K4 (no UNPLACEABLE).
   - For every label: column, anchor, visible or hidden ink, and each nearer outline the last quarter enters, with the exemption basis (contains or encloses).
   - Expected: drill_head right column at (88.90, 0.00); descent_stop inside bracket_guide_a and ring only, no tie b; ring on visible rim outside tie a and guide_member.
3. Run `--controls`:
   - K4-Z3 clean;
   - K4-B7, B8, B10, B11 and B12 planted counts each down by one (the drill_head red is gone);
   - K4-B12 still fires on tie b;
   - B14 to B16 fire and match;
   - the red-first of B14 to B16 run on the P1R `sketch_common.py`.
4. A failure of any expectation returns D1 and D2 to me. It opens no revision.

**Gate for S2 r7.** If DR-1 passes, the real run draws S2 r7, since pixels change (P1Rf rule). The S2 r7 accept still needs RPT green (section 5) and the fresh M1 (P8, KC11).

## 4 S2 r6 against r5: what reads worse

| # | Item | Class |
|---|---|---|
| W1 | Ring label leader now ends on hidden rim inside tie a (Correction 1). | FIX D1 |
| W2 | Ties read as white faces with hidden edges (Correction 4). | FIX D3 |
| W3 | Ring fill now (227, 237, 246) over white, lighter than the plate tint (221, 228, 236). In r5 it was (210, 223, 237), darker than the plate. The rim line carries the boundary and the difference is small in both revisions, but the nearer part now reads paler than the floor it stands over and closer to the white open bore. | NOTE N1: darken the ring face colour at the same alpha 0.5, so that its composite over white is about (210, 223, 237). The opacity lint is unaffected. Pixel check on the ring rows only, at the next drawn revision. Not blocking. |
| W4 | The descent-stop leader crosses 58 mm of member a's hatch mid-length (r5: crossed tie b's dashed outline). | NOTE N2: left to M1 (P8). Rule (d) polices only the end quarter, and DR-1 may move the anchor. |
| W5 | NEMA 23 bodies read beige-grey (sector over motor over white) in place of grey. | No issue: the colour follows the plate tint removal. |

Nothing else reads worse. The changed pixels in P1R section 5 are accounted for by tint removal, hidden arcs and three moved leaders.

**FIX D3 (stand-in line).**
- Draw plan_style stand_in edges as a phantom line: long dash and two short dashes, matplotlib dash pattern (0, (12, 3, 3, 3, 3, 3)) in points. Use dark brown #8c510a at the present line width, with no fill.
- Change the legend line to "phantom, brown: Step 2 stand-in (rod top ties)".
- Rationale: a phantom line is the drafting line for an adjacent or provisional part. It is distinct from hidden (short dash) and from the chain line used for slot lines and pinion axes, and the hue separates it from the hidden black and the rim blue.
- Scope: plan figures now. S1 r7 stays pixel-equal at this step, and S1 takes the same style when S1 r8 opens (P0T K5 ruling). If the style lives in one shared helper, the Engineer gates it by figure until then.

**Dry-run DR-2** (scratchpad copy):
- Apply D3 and redraw S2.
- Report K5 (stand_in class admission with the new dash), K8:
  - the stand_in rows stay out of the renderer;
  - cover clause 3 no longer applies to a solid-classed edge, or state how the phantom style is classed;
  - K8-B42 and every control that plants or reads stand_in pass.
- Report the K4 figure note, the legend text, and the S1 r7 pixel equality.
- A failure returns D3 to me.

## 5 Reported items for s2_spec.yaml (ruling on the S2 r6 RPT red)

Step 1.2 gate D3 applies from S3 on. S2 r6 is a 1.3 revision, so `s2_spec.yaml` gets `reported_items`. The list comes from detail 1.2 "Reported" (gameplan l.264), the spec's own `reported:` block (s2_spec.yaml l.90-98), and the three values J13 found outside `s2_summary_r5.md` (step1.2_manager_close.md J13, D3).

**Where the values come from.** RPT reads values from `checks_s2.reported(ctx)["items"]` ({id: {value, basis, tag}}). Today `reported()` returns `rows` only. The Engineer adds the `items` dict, reuses the existing rows where they exist, and adds the rows marked "new".

| id | text | source | needs_drawing | r6 value (for the dry-run comparison) |
|---|---|---|---|---|
| outline_extents_all | Outline extents, every drawn part, reference rows excluded, against the 644 x 608 footprint (open, not asserted) | checks_s2.reported row "Outline extents, every drawn part" (drawn pieces; MEASURED) | true | x -322.00 to 322.00, y -304.00 to 304.00 |
| outline_extents_above_plate | Outline extents, parts above the plate | checks_s2.reported row "Outline extents, parts above the plate" (MEASURED) | true | x -278.27 to 278.27, y -304.00 to 218.00 |
| members_to_plate_edge | Members against the plate edge: members a, b x extent against 322; member c against the notch edges and the plate y edge 304 | new: min distance of the frame_upper_a/b drawn pieces to the base_plate x edges; member c drawn pieces against the notch edges (S2-6 notch_clear basis) and against y -304 (MEASURED, drawn pieces) | true | a, b 43.73 inside the x edge; c on the rail, 0.00 to the plate y edge (J13) |
| tip_force_footprint | Footprint against the S1 unbolted tip force (bolt-down or footprint goes to the Step 2 row, R1) | new: `s1_mass_report_r7.json` `<pose>.tip_force_at_com_N` for load, start, capture_end, park, lever `icd.footprint_y` / 2 = 304 (read from the accepted S1 report; DERIVED) | false | 341 / 368 / 531 / 258 N over lever 304 (J13) |
| cutter_overhang | Cutter overhang of the keep-out: drill.head_od / 2 - icd.keepout_radius (S2-a; Step 4 ICD row icd.keepout_radius) | new: keys `drill.head_od` (ASSUMED, Q2) and `icd.keepout_radius` (DERIVED) | false | 2.70 |
| f6_eye_limits | F6 eye limits at r 400: eye height below which the ring rim hides the cut at capture_end, to the axis and to the cutter rim | new: Designer 1.2 (a) section 6 (`step1.2_designer_params_review.md` l.107, 211). Line from the target (r 0 or `drill.head_od` / 2, at the cut z at capture_end) through the ring rim (`ring.od` / 2, ring bottom at capture_end from check_stack), extended to r = `operator.watch_r` 400 (DERIVED) | false | 0.49 m (axis), 0.58 m (cutter rim) z_S |
| s2_5b_strike_list | S2-5b overhead strike list in the sector at load, z_S bands, with margin over the hand-band top | checks_s2.reported row "S2-5b strike list" (MEASURED, check_stack) | true | drill_head 19.84 least |
| tight_rim_to_rod | Tight spot: ring rim to guide rod | new: K7 plan record, pair ring and guide_member, G distance (MEASURED, drawn K7; identity with g_min 10) | true | 10.00 |
| tight_rim_to_member | Tight spot: ring rim to member inner face | new: K7 plan record, pair ring and frame_upper_a (least over a, b, c), G distance (MEASURED) | true | 34.00 |
| tight_liftmotor_sector | Tight spot: lift motors to the sector edge, bound (circumscribed) and drawn square | checks_s2.reported row "Tight spot: lift motors to the sector edge" (MEASURED) | true | 11.71 / 15.69 |
| tight_pinion_toe_hub | Tight spot: pinion toe to gear hub | checks_s2.reported row "Tight spot: pinion toe to gear hub" (MEASURED; DERIVED 95.22 - 90.00) | true | 5.22 |
| highest_point_parts | Highest point over parts at each pose, reference rows excluded (LF1.2-5) | checks_s2.reported rows "Highest point over parts, <pose>" (MEASURED, check_stack) | true | load 1819.84, start 1694.84, capture_end 1285.00, park 1819.84 z_S |

Basis rule for items 1, 2 and 12: rows with `reference: true` (keepout, collet_axis, operator_sector, sightline_f6) are excluded (Designer M1 r1 ruling 3; LF1.2-5).

**Dry-run DR-3** (Engineer):
1. Add `reported_items` with the 12 entries above, and the `items` dict in `checks_s2.reported`.
2. Record the edit in the spec `status` line ("1.3 P1Rd: reported_items, Designer").
3. Run `check_sketch.py s2 --rev 6` (or r7): RPT pass, "12 reported item(s) declared, every one has a value". The summary carries the Reported items table, and each value matches the r6 column above within 0.01 (f6_eye_limits within 0.01 m).
4. Run `--stale`: clean. `reported_items` is a spec field and no overlay key moves.
5. Run `--controls`: RPT controls unchanged.
6. If a value differs from the r6 column, report it. Do not adjust it.

**Reported items list SIGNED (Designer).**

## Verdict

**FIX 3** (D1, D2, D3).
- Signed now: the hidden convention as drawn (except D3), hidden copies at their own draw order, the placer order and layout, the UNPLACEABLE record, the rule (e) z premise, and the reported items list.
- N2 closed.
- NOTEs N1 to N3 do not block.
- D1 and D2 close through DR-1, D3 through DR-2, and the RPT red through DR-3. Each is re-checked by me (P1Rf, `step1.3_designer_renderer_recheck.md`).

## Gameplan lines to change

**l.138 (K4 row), rule cell.** This supersedes the P1R new text for the same cell.

Old:
```
a row may set label_side: left, a left label column under the same rules (1.2 (h) r4, Designer M1 S2 r3 N1) |
```
New:
```
a row may set label_side: left, a left label column under the same rules (1.2 (h) r4, Designer M1 S2 r3 N1); 1.3 P1R: plan labels are placed by one placer (sketch_common.place_plan_labels; candidates in order: label_side column then the other, label_theta ray hit, column default anchor, ink samples at most 2 mm apart; first candidate passing every leader rule, re-judged after column stacking); (e) only true outlines of rows higher than the labelled row by more than 0.05 (zones: every outline) count; (e1) a row with visible ink (renderer split, certified by K8 cover) anchors on visible ink and its leader's last quarter lies outside every counted outline that does not enclose the anchor (outer boundary, holes filled); (e2) a wholly hidden row anchors on its hidden ink and its last quarter lies outside every counted outline that neither contains nor encloses the anchor (Design Notes 30; Designer P1Rd FIX D1); (f) a label with no passing candidate is recorded UNPLACEABLE with its candidate table in the K4 record and fails with reason "unplaceable", no silent fall-back; (g) the drawn label of a wholly hidden row contains "under " and the name of a counted row whose outline contains or encloses the anchor |
```

**l.138 (K4 row), B cell.** This is appended after the P1R new text for the same cell.

Old:
```
K4-B11 an area of another row over an anchor |
```
New:
```
K4-B11 an area of another row over an anchor; K4-B12 the descent-stop leader at the r4/r5 anchor (inside tie b); K4-B13 a pad under an opaque lid (unplaceable); K4-B14 ring label at the r6 anchor on hidden rim inside tie a (e1); K4-B15 drill_head label without its "under ring gear" suffix (g); K4-B16 gear outline planted as an open C, not enclosing the cutter anchor (e2); K4-B8 re-planted at 1.3 P1R |
```

**l.264 (detail 1.2, Reported).**

Old:
```
highest point over parts only (reference lines excluded, LF1.2-5).
```
New:
```
highest point over parts only (reference lines excluded, LF1.2-5). From S2 r6 (1.3) these are the spec field reported_items in s2_spec.yaml (12 ids, with members to plate edge, tip force, cutter overhang and F6 eye limits; Designer P1Rd section 5), read by RPT.
```

**l.667 (Design Notes 25, TP1.2-18/19 and N2 renderer row).** This is appended after the P1R new text.

Old:
```
awaiting P1Rt and P1Rd signatures | 1.3 (S3) | The Topologist proposes; The Engineer; The Designer co-owns the renderer |
```
New:
```
awaiting P1Rt signature; P1Rd: N2 closed on S2 r6 (ring rim dashed under the arms, ties and motors), hidden convention and hidden-copy draw order signed, FIX D1 (rule (e) by visible ink and enclosure, clause (g)), D2 (drill_head and descent_stop label suffixes naming their cover), D3 (stand-in edges as a brown phantom line, S1 at r8) with dry-runs DR-1, DR-2 | 1.3 (S3) | The Topologist proposes; The Engineer; The Designer co-owns the renderer |
```

**l.690 (Design Notes 30), end of entry.**

Old:
```
The 60.1 mm of leader inside tie b goes to Sean at M2 as a visual item and to the S3 hidden-line renderer item (N2).
```
New:
```
The 60.1 mm of leader inside tie b goes to Sean at M2 as a visual item and to the S3 hidden-line renderer item (N2). 1.3 P1R: placer rule (e) keeps the leader out of tie b (K4-B12); P1Rd FIX D1 and D2: the pad is wholly hidden, so its leader ends inside the containing top-guide bracket arm and its label says so ("under top-guide bracket arm").
```
