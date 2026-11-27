# Step 1.4 P5T, The Topologist: 1.4 (c) sense, admissions and the not_drawn rulings

Scratch: `D:\Unleashed Robotics\_scratch\cutjig\open14\p5t\` (`probe.py` / `probe_out.txt` fixture coordinates and hand predicate values; `probe2b.py` / `probe2b_out.txt` plants on the current code; `dry.py`, `dry2.py` / `dry_out.txt`, `dry2_out.txt` dry runs of every form proposed below). All runs on the live P4 tree, read only, fixture `s4_fixtures.s4_live` (P6 state, both figures).

## Corrections to the brief

1. **The washer window at theta 330 lies in front of the plane, not behind it.** At theta 330, x = r cos 330 = +0.866 r: the window spans x +58.90 to +75.37 (DERIVED). The spec reason "windows at 210 and 330 lie at x -61.4 to -72.7, past the band" is wrong in sign for 330.
2. **The theta 210 window meets the beyond band.** With its 5.0 half-width (nut.washer_window_width 10), the band is x -75.37 to -58.90 against -profile.width -60: 1.10 inside (DERIVED). The P4 band -61.4 to -72.7 leaves out the tangential half-width, so off_plane does not hold there either.
3. **The witness ruler lies on the receiver, not the holder.** It is a channel in the receiver thread zone with its floor at r 71.99 (thread.minor / 2 - witness.channel_floor_depth). Its parent row is receiver. The "holder flange tick" is the holder's.
4. **The tommy bosses straddle the band.** At theta 135 the boss spans x -77.53 to -49.24 (DERIVED), so "near x -0.71 r, at the band edge" understates it. Neither off_plane form holds.
5. **The -u slit tick at d 105 cannot be drawn 8.00 long inside the collet.** At the closed end, z_A 65.00, the d 105 wall runs r 53.000 to 59.234, 6.234 wide (DERIVED).

## 1 S4-3 predicates, by hand on the fixture (figure 1 unless stated)

All coordinates are drawn values in z_A (MEASURED, `probe_out.txt`; z_S = z_A + 60.00).

| Row: predicate | Sign check | Invariant | Hand value | Verdict |
|---|---|---|---|---|
| collet: taper narrows up, piece cone | the outer edge has \|u\|(top) < \|u\|(bottom) - tol | flips under z -> -z; holds under the u mirror | outer 63.291 at 41.995 to 59.111 at 65.700; d 105: 63.291 to 58.670 at 68.200 | PASS |
| collet: below holder, piece foot | centroid z(foot) < centroid z(holder) | z order | 41.00 < 106.23 | PASS |
| collet: rests_on receiver, seat_piece floor | \|z_min(collet) - z_max(floor)\| <= 0.05; bearing >= 0.25 | z contact plus radial overlap | 0.000; bearing 16.49 per side (d 105: 13.99) | PASS |
| collet: vertical_edge, piece cone | inner edge du <= 0.05 | translation in u or z | u 50.500 from 41.995 to 65.700 (d 105: 53.000 to 68.200) | PASS |
| holder: taper narrows up, edge inner | inner edge \|u\|(top) < \|u\|(bottom) - tol | as taper | 62.040 at 49.09 to 56.750 at 79.09 | PASS |
| holder cone against the collet cone | | mating sense | collet outer 62.04 at 49.09 and 58.00 at 72.00, equal to the holder inner edge at both heights: contact over 49.09 to 72.00 | consistent |
| wingnut: clears_above holder, piece pocket_rim, of_piece flange | z_min(rim) - z_max(flange) > 0 | z order | +0.50 | PASS |
| collar: clears_above holder flange | z_min - z_max > 0 | z order | +8.75 | PASS |
| washer: between flange and plate | (z_mid - z_max(flange)) (z_min(plate) - z_mid) > 0 | **the order is not encoded; see section 7 and F4** | a +0.65, b +0.65 | PASS on live; form FIX |
| receiver: below collet, piece floor | centroid z order | z order | 26.00 < 53.28 | PASS |
| carrier: rests_on core_seat (min_bearing 0.25) | contact plus bearing | | 0.000; 3.00 per side. Figure 2 on core_seat_105: 0.000; 0.50 | PASS |
| core_100: rests_on carrier; above carrier | contact; centroid order | | 0.000, bearing 50.50; 252.50 > 122.50 | PASS |
| liner: rests_on core_seat_105 | | | 0.000; 2.50 per side | PASS |

S4-3-B1 to B7 are red on the pre-change code (P4 table, `pre_run.txt`). With the section_true premise holding, drawn equals spec, so these predicates guard the spec polygons. That is their job on S4.

## 2 Section look sign and handedness on the S4 plane

- section_yz has u = +Y and z = +Z. u x z = Y x Z = +X, toward the viewer. Look toward -X: (u x z) . toward = -1, the K8-B66 form. The S4 spec text agrees: look "from +X toward -X", toward_viewer +X, "u equals plan y".
- Slit sides:
  - theta 112: (x, u) = r(-0.375, +0.927). Behind, at u > 0.
  - theta 262: r(-0.139, -0.990). Behind, at u < 0.
  - The (i) sign check sin(theta) u > 0 is the correct sense.
- Wings:
  - The -X wing x_band [-115.00, -83.14] is negative: behind.
  - The +X wing band [+83.14, +115.00] is in front, so off_plane holds.
- Plane cut: the theta 90 window is at u = +r, side +u, matching plane_cuts side "+u".
- Receiver bolts: x +-77.94 = 90 sin 60 (PCD 180 at 30, 150, 210, 330), past the band.

**PASS.**

## 3 Tick admission, collet:slits (form (a)): FIX F1

The premise and branches (n), (i), (iii) and (iv) are sound. They are re-computed on the drawn lines:
- +u line at u 57.400, z 47.00 to 72.00. The open top meets the top face span 56.80 to 58.00.
- -u line at u -55.425 (d 105: -56.662), z 40.00 to 65.00. The open bottom lies on the foot face, -66.99 to -50.50 (d 105: -53.00).

Four defects:

- **(a) The tick is not contained.** No branch reads the tick's ends (MEASURED):
  - figure 1: the -u tick runs -59.425 to -51.425 at z 65.00, 0.187 outside the cone outer edge (-59.234), into the holder;
  - figure 2: the -u tick runs -60.662 to -52.662, 1.406 outside the cone and 0.338 inside the bore (into the liner).
  - A tick that leaves its part breaks the premise "the line states nothing else". Correction 5 shows that no centred 8.00 tick fits at d 105.
- **(b) (ii) reads the convex hull.** The hull of the side pieces adds the foot-step triangle, (66.99, 41.995) to (58.00, 72.00), which is not collet. A -u line and tick at u -59.80 pass today (MEASURED: K5 0 issues, `probe2b_out.txt`), yet the line leaves the union above 41.995 (DERIVED, sampled at 0.5).
- **(c) The premise of (iv), "behind the plane", is unchecked.** A spec line at theta 82 (k 1, x > 0, cut away with the front half) passes as a dashed hidden slit today (MEASURED: K5 0 issues).
- **(d) The tick is drawn solid.** The relief hole lies behind the plane with its slit, so by the convention it is a hidden edge.

## 4 Wing by declared x_band (Designer P3a O3): FIX F2

Half-space view. Take a wing point at (x_w, u, z) with x_w <= x_band[1] = -83.14 and |u| <= 7. The sight line runs along -X at offset u. Behind the plane, a revolved piece [r_in, r_out] of the row crosses it over x in [-sqrt(r_out^2 - u^2), -sqrt(max(r_in, |u|)^2 - u^2)], which is non-empty when r_out > |u|. That interval lies wholly in front of x_w when r_out <= -x_band[1].

So the wing rule's test (r_out > |u|, r_out <= -x_band[1], z band holding z) is a sufficient half-space condition for occlusion. It is the special case of the general test in F5: chord a < r_f and b > |u|.

Two defects:
- **(a) Vertices only.** The test reads the four corners. An edge that crosses an unoccluded z band passes. B plant: delete the relief piece. The corners stay occluded (body at 113.09, plate at 153.09), but the edges cross 139.09 to 145.59 with nothing in front (DERIVED, `dry2_out.txt`). This reads clean on the current code (MEASURED: K5 0 issues).
- **(b) Occluders come from the +u section pieces, plane_cuts applied.** The +u pocket rim is the theta 90 plane cut. The material in front of the wing lies at azimuth 180 +- asin(|u| / r_in), at most 5.91 deg (DERIVED). That is 84 deg from the window, whose half-angle is 3.98 deg.
  - Read with plane_cuts applied, exact interval coverage finds a false gap at 145.59 to 146.39 (DERIVED).
  - Today's vertex test, and a 2.5 sample step, both step over that 0.80 gap.
  - The occluder is the revolve half-profile. plane_cuts describe the plane only.

The wing's (w0), (i) and (ii) are SIGNED.

## 5 Sweep sub-artist: FIX F3

- (s2) and (s3) are sound. The lines sit at u -+115.00, symmetric, so no sense question arises.
- (s1) has no B (the P4 report says so), and every branch needs one.
- Shape NOTE for the Designer: the lines run over the row's z extent, 97.09 to 153.09. The wings sweep r 115 over wing.z only, 113.09 to 153.09; below that the nut reaches r 95.14 (the skirt). Over 97.09 to 113.09 the lines state an envelope that does not exist. My view is that (s3) should read wing.z when the row carries a wing. This is the Designer's call (S3 drew the sweep over the full nut height, where the stand-in wings ran from the nut bottom).

## 6 section_true premise and K5 admission (O7): SIGNED

- section_true_issues demands both directions:
  - every spec piece on each side (plane_cuts applied) is drawn as a named artist equal to its polygon;
  - every drawn area artist of the row is named and equals its piece.
- The mirror is keyed on the field. Side -1 polygons are reversed, so the orientation stays counter-clockwise.
- st_admitted admits only a named artist that equals its piece. Its premise is the K8 call on every section_true row in a side or section view, and that call runs whenever the row is drawn (K8-B103 to B105).
- The root u_c = 0 branch rests on the same premise (section 8).
- NOTE N1: poly_match compares vertex sets, not cyclic order. A bow-tie plant on the collet +u cone, with the same vertices reordered (a, c, b, d), reads clean in K8 section_true. It was caught only by K5 zero-area in that instance (MEASURED, `probe2b_out.txt`). Cyclic-order equality (up to rotation and reversal) closes it.

## 7 New predicate forms (O6)

- piece, of_piece, seat_piece: they read named pieces. A missing piece reports untestable / absent, which fails K8 by cause. **SIGNED.** NOTE N3: a piece name absent from the target row's section_true should be a spec error, not "absent".
- vertical_edge: inner_edge picks the non-horizontal edge of least mean |u|. On the collet cone piece that is the bore edge (the outer cone has mean |u| 61.2). It holds on both sides through |u|. **SIGNED.**
- taper, edge inner: |u| at the top is less than |u| at the bottom minus tol. **SIGNED.**
- **between: FIX F4.** The product (z_mid - z_max(below)) (z_min(above) - z_mid) > 0 also holds when both factors are negative, so the predicate states betweenness without order.
  - Plant (figure 1): washer 1.5 low, wing nut 2.5 low. a = -0.85, b = -0.35, product +0.2975, and between passes. K8 reports only wingnut clears_above (MEASURED, `probe2b_out.txt`).
  - The sign check with its order is min(a, b) > 0.

## 8 Root `r` form, u_c = 0 on section_true rows: SIGNED

- d = 2 r. The lines are at -+72.290 (thread.minor / 2) over 80.50 to 128.50.
- Both ends are inside the drawn pieces:
  - at 128.50, the rim top edge runs 68.29 to 73.54;
  - at 80.50, the line meets the land and thread corner.
- The root continues the runout land's outer edge (r 72.29, 76.50 to 80.50): the land sits at the root diameter, as built.
- NOTE N2: when a row carries both `d` and `r`, d wins silently; this should be a spec error.

## 9 not_drawn rulings (the five P5T-deferred entries and the window entry): FIX F5

**Ruling.** Every feature the P4 text puts in the beyond band (inserts at x -43.84, witness ruler and flange tick at theta 127, the slits behind the plane) is a hidden feature of a cut row. So are the theta 210 window and the tommy bosses. Each is occluded, along its sight line, by a revolve piece of a drawn cut row (often its own) or by an unsectioned row drawn whole.

The section convention omits hidden features of a drawn row behind the plane (ASME Y14.3 omits hidden lines in sections unless needed). Declared sub-artists are the stated exceptions (collet:slits, wingnut:wing). The omission needs its premise checked, so a new form is needed: `omit: hidden`.

Neither existing form holds:
- off_plane fails, because these features meet the band (Corrections 2 and 4);
- deferred leaves the converse unjudged.

**Form.** A not_drawn entry carries:
- `omit: hidden`;
- `rows` (parent row ids);
- `theta` (expressions, deg);
- `r: [lo, hi]`, `z: [lo, hi]` (z_A expressions over keys, R2-6);
- `t` (tangential half-width);
- `source`.

Samples: r and z at <= 2.5 including the ends, t at -t, 0, +t (theta shifted by atan(t / r)). Each sample is taken at every figure pose where a listed row is drawn. With x = r_f cos theta and u = r_f sin theta:
- **(h1)** |x| <= 0.05: the plane cuts the feature. It must be drawn, or listed as a plane_cuts entry.
- **(h2)** x > 0.05: the feature is cut away with the front half. This holds only when the parent is section_class cut; an unsectioned parent is drawn whole, so its front features are visible.
- **(h3)** x < -0.05: some occluder drawn at that pose must cover the sample:
  - a cut row's section_true revolve piece (plane_cuts ignored, premise as F2) whose chord [a, b] at z has a < r_f - 0.05 and b > |u| + 0.05;
  - or an unsectioned row drawn whole whose half-width exceeds |u| + 0.05.
- Premise: occluders are revolve profiles, and feature voids in an occluder are neglected, which is the drafting convention. The section.convention `omitted` text gains the clause.

**Entries.** Dry run of every entry in both figures (`dry2_out.txt`, DERIVED): 0 samples in the plane, 0 front samples on an uncut parent, 0 behind samples unoccluded.

| # | Entry | Ruled form | Dry run |
|---|---|---|---|
| 1 | receiver key slot, holder key, collet foot key (theta 37) | `omit: off_plane`, x: `[["(receiver.register_bore_radius - fit.seat_clearance) * cosd(receiver.key_offset_deg) - receiver.key_slot_width / 2 * sind(receiver.key_offset_deg)", "wingnut.body_od / 2 * cosd(receiver.key_offset_deg) + receiver.key_slot_width / 2 * sind(receiver.key_offset_deg)"]]` | [+49.89, +70.01], in front |
| 2a | holder M6 inserts | `omit: hidden`; rows [holder]; theta [45, 135, 225, 315] (holder.py 45 + 90k; literals as the slit 15); r: insert_circle_radius -+ insert_dia / 2; z: [collar_top - collar.thickness - holder.insert_depth, collar_top - collar.thickness]; t 0 | 216 samples per figure; front at 45, 315; 135 and 225 behind the holder neck and flange |
| 2b | collar holes | `omit: hidden`; rows [collar]; theta as 2a; r: insert_circle_radius -+ collar.hole_dia / 2; z: [collar_top - collar.thickness, collar_top]; t 0 | 192 per figure; collar ring and neck |
| 3a | witness ruler | `omit: hidden`; rows [receiver]; theta [witness.azimuth_deg]; r: [thread.minor / 2 - witness.channel_floor_depth, thread.major / 2]; z: [receiver_floor + witness.channel_z[0], receiver_floor + witness.channel_z[1]]; t witness.channel_width / 2. The channel_z frame origin is ASSUMED at the receiver floor; The Engineer confirms it against build_parts/receiver.py | 72 per figure; receiver thread piece |
| 3b | holder flange tick | `omit: hidden`; rows [holder]; theta [witness.azimuth_deg]; r: [holder.flange_od / 2 - witness.tick_depth, holder.flange_od / 2]; z: [holder_bottom + holder.length, holder_bottom + holder.length + witness.tick_height]; t witness.tick_width / 2 | 18 per figure; flange (behind its own cut face) |
| 4 | wing-nut tommy bosses | `omit: hidden`; rows [wingnut]; theta [45, 135, 225, 315]; r: [wingnut.body_od / 2, nut.tommy_hole_bottom_r + nut.tommy_hole_depth]; z: collar_top - collar.top_above_plate - nut.tommy_hole_depth -+ nut.tommy_boss_od / 2 (axis 133.09); t nut.tommy_boss_od / 2 | 924 per figure; holder flange and tube, receiver thread, wingnut body |
| 5a | collet slits not drawn, bottom-open | `omit: hidden`; rows [collet, collet_105]; theta "receiver.key_offset_deg + 15 + k * 360 / collet.slit_count", k 1, 3, 5, 9, 11 (82, 142, 202, 322, 22); r: [(core.diameter_nominal + collet.grip_window_hi) / 2, receiver.register_bore_radius - fit.seat_clearance]; z: [receiver_floor, receiver_floor + collet.slit_length]; t collet.slit_width_seed / 2 | 1320 per figure; front 82, 322, 22; behind: collet cone, carrier, receiver floor, core seat |
| 5b | collet slits not drawn, top-open | as 5a, k 0, 4, 6, 8, 10 (52, 172, 232, 292, 352); z: [receiver_floor + collet.slit_ligament + collet.relief_hole_dia / 2, receiver_floor + collet.slit_length + collet.slit_ligament + collet.relief_hole_dia / 2] | 1320 per figure |
| 6a | washer notch, anti-rotation tab (theta 37) | `omit: off_plane`, the entry 1 band | in front |
| 6b | washer windows | `omit: hidden`; rows [wingnut]; theta ["180 / wingnut.wing_count + 360 / nut.washer_window_count", "180 / wingnut.wing_count + 2 * 360 / nut.washer_window_count"] (210, 330); r: [nut.washer_pocket_od / 2 - 1, wingnut.body_od / 2 + 1] (nut.py box_at); z: pocket floor to pocket floor + nut.washer_pocket_depth; t nut.washer_window_width / 2. The theta 90 window stays with plane_cuts | 84 per figure; 330 in front; 210 behind the holder neck |
| 6c | nut press pads | `omit: deferred`, owner Step 2 (not placed in params) | listed |

Reason texts change with the forms: Correction 1 for 330, Correction 3 for the ruler's parent.

Shape, with the Designer: omitting these is a drafting decision for the reader. The witness ruler is the operator's readout, and it lies on the back side in this plane. If The Designer wants it shown, it belongs to another view (S6 or a detail), not as a dashed outline through the holder cut face. The Designer confirms that no omitted feature is needed for a V10 operator row.

## 10 FIX list (dry runs above; each B is clean on the current code unless stated)

| FIX | Change | Dry run (DERIVED / MEASURED) | Z | B |
|---|---|---|---|---|
| **F1** collet:slits | (a) **(t) containment:** both tick ends inside the union of the row's side pieces within 0.05. The tick form changes (Designer rules the shape). Recommended: the tick spans the wall at the closed z, inner to outer edge (`tick: wall` replaces tick_length), and (t) reads the tick ends on the union chord at zc. A fixed length min(tick_length, chord) centred on the chord is the alternative. (b) **(ii)** reads the union of the side pieces, sampled at <= 0.5 along the line. (c) **(i0)** spec lint cos(theta) < 0 for every slit line (behind the plane; the premise of (iv)). (d) the tick is dashed, as (iv) | Chords at the closed z: fig 1 +u 50.500 to 62.408, -u 50.500 to 59.234; fig 2 +u 53.000 to 62.408, -u 53.000 to 59.234. Each line u lies on its chord (57.400, -55.425, 57.400, -56.662). Live -u line inside the union; u -59.80 leaves it | K5-Z8 with the new ticks, both figures | (a) fig 2 -u tick 1.00 past the outer edge; (b) -u line and tick at u -59.80 (0 issues today, MEASURED); (c) +u line theta k 1 (82 deg) (0 issues today, MEASURED); (d) tick solid |
| **F2** wingnut:wing (iii) | (a) Exact z-interval coverage of every drawn edge by the union of occluder z bands with max\|u\| < r_out <= -x_band[1]; gaps > 0.05 fail. (b) Occluders from the section_true revolve half-profile, plane_cuts ignored. (c) Premise lint: every plane_cuts entry carries theta, 90 for side +u or 270 for side -u (sign(sin theta) = side), and (iii) asserts asin(max\|u\| / r_in) < 45 deg for every occluder it reads | Live, plane_cuts ignored: no gap. Live, plane_cuts applied: false gap 145.59 to 146.39. Relief deleted: gap 139.09 to 145.59. Sight half-angle at most 5.91 deg | K5-Z8 | (a) relief piece deleted from section_true (0 issues today, MEASURED); (c) wingnut plane_cut with theta 270 on side +u |
| **F3** wingnut:sweep | B for (s1) | n/a (existing branch) | | one sweep line deleted, "(s1)"; red by branch deletion |
| **F4** between | min(a, b) > 0 in place of the product | live a = b = +0.65 passes; plant a -0.85, b -0.35 fires (product form passes) | K8-Z20 | washer 1.5 low and wing nut 2.5 low, figure 1, reason "between holder and wingnut" (absent today, MEASURED) |
| **F5** not_drawn | `omit: hidden` with (h1), (h2), (h3) in not_drawn_band_issues at every figure pose. The section 9 entry forms in s4_spec.yaml; the convention clause; ND_OMIT gains hidden | Section 9 table: every entry clean in both figures | K8-Z20 (the entries) | (h1) insert at theta 90 (54 of 54 samples in the plane); (h2) a theta 0 feature on the unsectioned carrier (30 of 30); (h3) an insert on the holder bore at theta 110, r 56.75 to 57.75, z 130 to 136, in the carrier and holder gap (12 of 24 unoccluded) |

Rule scope (process rule): F1 covers every row with sub_artists slits, in side and section views, through same_as. F2 and F5 read every drawn cut row and unsectioned row at each figure pose. F5 applies to every spec with not_drawn. S3 carries no hidden entries today, and its plane_cuts list is empty.

## 11 NOTES

- N1. poly_match is order-free (section 6). Cyclic-order equality; to P6.
- N2. root with both d and r: spec error.
- N3. Unknown piece / of_piece / seat_piece / below_piece / above_piece names: spec error.
- N4. Sweep z extent against wing.z (Designer, section 5).
- N5. Slit line u is not asserted: +u is revolved (top-face mid-radius 57.40) and -u is projected (r_mid sin theta). These are two conventions in one figure, signed at P2r form (a). The Designer may unify them; the admission holds either way.
- N6. base-frame rails `omit: deferred, owner S3` stands. The exact statement is a crop form (u band outside crop.u), checked; to S6.
- N7. section_true_issues accepts two equal artists for one piece (doubled ink); to P6.

## Signatures

| Rule / item | Verdict |
|---|---|
| S4-3 predicates (hand) | PASS (between form under F4) |
| Section look sign and handedness | PASS |
| Tick admission collet:slits (n), (i), (ii), (iii), (iv), (t) | FIX F1 |
| Wing by x_band (w0), (i), (ii) | SIGNED; (iii) FIX F2 |
| Sweep sub-artist | FIX F3 (shape NOTE N4 to the Designer) |
| section_true premise and K5 admission | SIGNED |
| piece / of_piece / seat_piece, vertical_edge, taper edge inner | SIGNED |
| between | FIX F4 |
| root `r`, u_c = 0 | SIGNED |
| not_drawn: five deferred entries and the window entry | FIX F5 (ruled forms in section 9) |

## Gameplan lines to change

none
