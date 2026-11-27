# Step 1.4 (b) Designer spec sign-off, S4 (P3a)

## Corrections to the brief

1. **The -X wing is hidden over its whole extent.** Seen from +X at |u| <= 7, every sight line from the wing (x -83.14 to -115) to the viewer crosses the wing nut's own far wall: the body over z_A 113.09 to 145.59, the pocket rim and the plate over 145.59 to 153.09 (6 of 6 samples occluded, MEASURED, dry run D3). The spec style "solid where visible, dashed behind core_100 and carrier" is wrong, and so is my own 1.4 (a) row ("dashed where the core outline lies in front"). No part of the wing is visible.
2. **K8 `rests_on` tests z only** (sketch_common.py l.4947 to 4950: bottom minus seat top within tol). A member with no radial overlap of its seat passes. A carrier narrowed to r 49.90 in the liner figure bears on 0.00 of the ledge, and the predicate still reads clean (DERIVED, D1). As written, S4-2 (a) does not certify the O5 bearing.
3. **The staged S1 r9 and S3 r8 wing nuts have a washer pocket and no washer.** The staged wingnut `section_true` (pocket_rim from the pocket floor 145.59) puts the nut 0.50 above the flange top 145.09, with an empty pocket from r 68.04 to 71.90. Neither staged spec has a washer row or a washer not_drawn entry (MEASURED, grep).

## 1. Part list (spec `docs/sketches/s4_spec.yaml`)

Every part a shape string names was traced to a row, a sub-artist or a not_drawn entry:

| Shape-string part | Carried by |
|---|---|
| shop floor, ground hatch | floor |
| base plate, spigot-hole gap, crop break lines | base_plate (section_u) |
| receiver spigot below the plate top | receiver_spigot |
| receiver floor, wall, land, thread zone, register chamfer, lead-in, shoulder | receiver (section_true) |
| receiver thread root lines | receiver:root |
| d 100 collet foot, cone, bore, chamfer, top face | collet |
| slit ticks with the relief-hole ticks | collet:slits |
| d 100 core-seat ledge | core_seat |
| d 105 collet, d 105 ledge | collet_105, core_seat_105 |
| holder cone, tube, bore, flange, neck | holder |
| collar ring | collar |
| wing nut body, pocket rim, plate, dust skirt | wingnut |
| -X wing, sweep extent lines | wingnut:wing, wingnut:sweep |
| PTFE washer | washer |
| carrier, bond line | carrier, carrier:line |
| 100 mm core, chamfer mark | core_100, core_100:line |
| liner | liner |
| drill head, cutter teeth ticks | drill_head (as S3) |
| stop, kerf-centre and min-core lines | line_stop, line_kerf, line_min_core |
| base-frame rails; shoulder bolts; key slot, holder key, foot key; M6 inserts; witness ruler and tick; tommy bosses; +X wing; other slits; washer notch, pads, tab, windows; 0.75 m core; options A, B, E; taller collet | not_drawn (12) |

**S4 counts (MEASURED):**
- rows: 19
- not_drawn: 12 (the figure_note names all 12 heads)
- part_list: 17
- missing: 0

**Staged S3 r8 (and S1 r9) counts:** washer missing 1 (Correction 3; FIX 5).

## 2. Shape notes, ticks, options, operator rows, rubric, reported items

- The shape notes match my 1.4 (a) section 2 to 0.01. Two exceptions are the Engineer's build_parts readings, accepted: foot-ring top 41.995 (Correction 6) and pocket inner r 68.04 (Correction 5).
- Slit ticks:
  - theta 112 (k 2, top-open, z 47.00 to 72.00) and theta 262 (k 7, bottom-open, z 40.00 to 65.00) as ruled (DERIVED; the handedness line checks: x < 0 for both, u > 0 at 112, u < 0 at 262).
  - The label is missing (FIX 1).
- Receiver root lines: the signed form. The label text exists only in source prose (FIX 1).
- Options drawn as ruled (Design Notes 34):
  - D with C drawn (figure 1);
  - cast-on liner (figure 2);
  - kept 32 mm collet;
  - A, B and E, and the taller collet, in not_drawn with owners.
- Hatch: three same-pattern adjacencies of separate bodies in figure 1, and five in figure 2 (FIX 2). The figure-note legend lists steel and nylon, and neither is hatched on any row.
- Operator rows: my 1.4 (a) section 11 rows are cited by rubric V10. The gameplan operator-task table still carries the pre-ruling S4 row ("Advance the core for a slice; take the slice off | start | ... collet top"), which contradicts advance D. Replaced under Gameplan lines item 1.
- Rubric additions: V4 as written fails S4 on a strict reading, because the core bottom is on the carrier and not on the stop. The liner figure has no rubric line (FIX 6).
- reported_items cover DC13:
  - 100 mm core against the collar top and core.min_exposed: q10_core_top, q10_exposed;
  - minimum core length: q10_min_on_stop;
  - advance per slice: advance;
  - collet options with the collar-top move: q5_delta;
  - sacrificial option: liner_wall;
  - cut-case seat: cut_case_seat.

  O5 adds one more (FIX 3).
- S4-2 and S4-3 forms match the Design Notes 34 ruling and my 1.4 (a) section 12. The collet-flipped B fires on `taper narrows up` (piece cone). `below holder` (foot) passes a flipped collet (centroid 70 against about 101) and certifies nothing alone. It is harmless.

## 3. Rulings on the Engineer's open items

**O3 (-X wing past the beyond band): drawn, hidden, with a declared band.**
- Sean ruled "wing nut wings drawn beyond" (Design Notes 34), so not_drawn is out.
- Drawn form:
  - wingnut:wing as a dashed hidden outline over its whole extent, unfilled: u -7.00 to 7.00, z_A 113.09 to 153.09 (DERIVED, D3);
  - label "-X wing (behind), span 230" from `wingnut.span`, with the leader landing outside the carrier outline. A bare dashed rectangle inside the carrier outline reads as a feature of the carrier.
- Admission (rule (h); the Topologist signs at (c)): a sub-artist with a spec `x_band` past -profile.width is admitted only when all three hold, each with its own Z and B:
  - (i) it is drawn dashed and unfilled;
  - (ii) its drawn u and z extents equal the spec values within 0.05;
  - (iii) every vertex is occluded by a section_true piece of its own row, as a half-space test along +X: the piece's z band contains the vertex z, and r_out > |u| with r_out <= -x_band[1].
- Bs: wing drawn solid; wing u at 9; x_band deleted; plate and body pieces deleted (occluder absent).
- Scope: S3 r8 draws the same wingnut row in the same plane and takes the same sub-artist (FIX 5).

**O4 (wing-nut true section): in.**
- Sean adopted wingnut|receiver C on the drawn major cylinder, wingnut|holder G 0.50 and collar|wingnut G 0.75 (S4-c, Design Notes 34). Those classes, and staged edit 6 for S1/S3, hold only on the true section.
- Under the rule-scope rule, two different wing nuts in one plane (S3 and S4) is the same X1 hole the holder had.
- No key, z_rule, place or margin moves (the staged X1 run passes 70 rows, Engineer section 6).
- The S3 r8 consequences are FIX 5.

**O5 (carrier on 0.50 of the d 105 ledge): value, with a bearing read.**
- Dry run D1 (MEASURED through check_stack.eval_expr on the live spec):

| Pose / member | Ledge r | Member bottom r | Bearing width | Area mm2 | All of 1287.05 N on it |
|---|---|---|---|---|---|
| carrier / carrier | 47.50 to 50.50 | 0 to 50.50 | 3.00 | 923.6 | 1.39 MPa |
| liner / carrier | 50.00 to 53.00 | 0 to 50.50 | 0.50 | 157.9 | 8.15 MPa |
| liner / liner | 50.00 to 53.00 | 50.50 to 53.00 | 2.50 | 812.9 | 1.58 MPa |

- 1287.05 N is the kept-part force F_stall + W (Design Notes 32, DECLARED).
- In the liner figure the carrier and the liner share the ledge. The cast-on liner carries the core's side load into its own 2.50 annulus. The worst case, the whole kept-part force on the carrier's 0.50 annulus, is 8.15 MPa on PA6. That is well under the compressive strength of a nylon rod (ASSUMED, no params leaf). The 0.50 stands. No geometry change.
- The figure needs the claim certified (Correction 2). FIX 3 adds the bearing read and states the share in the source text.

## 4. FIX items

**FIX 1. Tick and root-line labels.**
- `collet.slits` and `receiver.root` get label fields that print from keys:
  - "12 slits, alternating, 25 long" (`collet.slit_count`, `collet.slit_length`);
  - "thread 149.58 x 8 RH, 6 turns" (`thread.major`, `thread.pitch`, `thread.hand`, `thread.run_turns`).
- Dry run D4: both strings computed from params (MEASURED).
- Without labels the dashed lines read as hidden edges of the collet and receiver (V7). The printed value comes from the computing function (1.3 position).

**FIX 2. Hatch adjacency.**
- Separate bodies with the same pattern in contact or within 0.5 (MEASURED, D2):
  - base_plate|receiver 0.00 (//);
  - base_plate|receiver_spigot 0.20 (//);
  - receiver|holder 0.25 (//);
  - liner figure only: collet_105|liner 0.00 (oo) and core_seat_105|liner 0.00 (oo).
- At 0.25 the holder and the receiver wall read as one solid, and the stack is what S4 exists to show.
- Set:
  - `section.hatch_alt: {aluminium: "||", plastic: "--"}`;
  - a new row field `hatch_variant: alt` on receiver, receiver_spigot and liner. cut_hatch returns `hatch_alt[material]` for those rows, and the hatch_alt_issues clause covers hatch_variant as it covers hatch_split.

  "--" is in a thin vertical strip with no joint line beside it. That is not the S3 cover case where I objected to it.
- Premise lint (rule (h)): two cut rows that are not one_body and have equal drawn patterns within 0.5 mm are an issue.
  - Z: S4 as fixed, 0 pairs in both figures (MEASURED, D2 after).
  - B1: receiver variant removed (receiver|holder fires).
  - B2: liner variant removed (collet_105|liner fires).
  - Lint B: plastic alternate 'o' is refused (MEASURED).
- Scope: every view that hatches the receiver beside the true-section holder. That means S3 r8 (receiver|holder 0.25, receiver|base_plate 0.00). It is carried to P6 by name.
- figure_note legend: "aluminium // (receiver ||), brass, plastic oo (liner --); carrier and core unsectioned". Remove steel and nylon.

**FIX 3. O5 bearing read and text.**
- K8 `rests_on` gains `min_bearing`: the radial overlap of the member's bottom-face span with the seat's top-face span, both round rows (section_true, or depth for unsectioned rows), must be >= min_bearing.
- Set `min_bearing: 0.25` (half the least drawn bearing 0.50, ASSUMED) on every S4 rests_on: carrier (both poses), core_100, liner and the collet foot on the receiver floor.
  - Z: live values 3.00 / 0.50 / 2.50 (D1).
  - B: carrier drawn at r 49.90 in the liner figure gives bearing 0.00, and the predicate fires. Today the z-only predicate passes it.
- Scope: rests_on rows in S1 and S3 (core on the core seat). P4 runs the read on the S1 r8 and S3 r7 records and lists firings; carried by name.
- carrier|core_seat_105 source: "bearing annulus r 50.00 to 50.50 (0.50, 157.9 mm2); the liner bears on r 50.50 to 53.00 (812.9 mm2); worst case 1287.05 N on the carrier annulus 8.15 MPa (Designer P3a O5)". Drop "(open item)".
- reported_items add: `{id: seat_bearing, text: "core-seat bearing widths: carrier 3.00 (figure 1); carrier 0.50 and liner 2.50 on the d 105 ledge (figure 2); 8.15 MPa if all of F_stall + W bears on the carrier annulus", needs_drawing: true}`.

**FIX 4. O3 wing form.**
- `wingnut.wing.style` becomes "hidden: dashed outline over the whole extent, unfilled (occluded by the row's own body and plate, Designer P3a D3)".
- Add `wing.label: {text: "-X wing (behind), span", key: wingnut.span, fmt: .0f}`.
- `section.convention.beyond`: append "a sub-artist with a declared x_band past the band is admitted only as a hidden outline occluded by its own row (P3a O3; Topologist signs at (c))".
- Remove "(open item at (c))" from the +X wing not_drawn reason. Remove "open item" from wing.source.
- Admission checks and Bs: section 3, O3.

**FIX 5. O4 consequences in the staged S1 r9 / S3 r8 set.**
- (a) wingnut `section_true_note` in all three specs becomes "true section in S4, S1 and S3 (Designer P3a O4: follows from the S4-c fits Sean adopted; X1 class)".
- (b) The staged S3 r8 wingnut shape string ("body wingnut.body_od x nut.overall_height, two wings to span 230 ...") is rewritten to the pieces drawn: body, pocket rim, plate, skirt, the -X wing hidden (sub-artist wing, FIX 4) and the sweep lines. The +X wing goes to S3 not_drawn.
- (c) The washer, as a shared row equal to S4 (X1), is added to S3 r8, and to S1 r9 wherever S1 draws the wing nut's true section. Otherwise S1 gets a not_drawn entry naming it with its reason. Without it the figure shows the nut standing 0.50 off the flange over an empty pocket.

**FIX 6. Rubric.**
- Replace the third V3 addition with "V4 (S4): the carrier stands on the core stop, gripped by the collet; the 100 mm core stands on the carrier, chamfer mark at the top; the core top above the minimum-exposure line (Design Notes 34: the core bottom is on the carrier, not on the stop)".
- Add "V7 (S4, figure 2): the liner reads as one sleeve around carrier and core, gripped by the d 105 collet; the carrier and the liner bottoms both on the ledge".

**Verdict: FIX 6.** No BLOCK. O1: the staged text is signed subject to FIX 5. I re-sign at P2r on the fix-pass file and the dry-run outputs.

Dry runs: `D:\Unleashed Robotics\_scratch\cutjig\open14\p3a\ws\dry_p3a.py`, `dry_p3a.json`. These are read-only on the live spec; the hatch lint runs on an in-memory copy.

## Gameplan lines to change

1. Detail 1 common, operator-task table, row at line 186.
Old:
```
| Advance the core for a slice; take the slice off | start | S4 | collet top | slice plane | cutter at rest only | S4-2, V10 |
```
New:
```
| Set a short core: carrier and core (3.3 kg, 260 tall) into the collet | load (ring parked, tip 1019.84 z_S) | S4, S1, S2 | kneel or stand in the S2 sector (theta 90 +- 45); wing nut backed off (pose R); lower the stack over the collar top 219.84 z_S, hands at 280 to 520 z_S; re-tighten the wings (sweep r 115) | down the holder bore from the sector | fingers cannot enter the 4.5 radial gap at the collar ID; hold the stack upright until clamped (the carrier joint is the weak point) | S4-2, V4, V10 |
| Advance for a slice (advance D, Design Notes 34) | slice_stop sequence | S4, S1 | none: the lift steps the drill down one slice | as the S1 watch row | gear and pinions turning (S1 watch row) | V10, reported advance |
| Take the slice off | park | S4 | slice captured in the drill above the iris, released at park over the base | open | slice falls when the iris opens (N6) | N6, owner Quinn |
| Change a collet (liner option) | load | S4, S1 | as the S1 collet row; the liner comes out upward with the core | wing nut from the sector | as the S1 row | V10 |
```
