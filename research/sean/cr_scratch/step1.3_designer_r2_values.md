# Step 1.3 (h) r2: Designer values, K4 (i) signature, spec re-sign

Reviewer: The Designer (image-capable). Read: `step1.3_engineer_revision_r2.md` sections 1, 4, 6; `docs/sketches/wip/s3_visual_gate_r1.md`; `wip/s3_jackscrew_section_r2.png`; the five dry-run PNGs in `_scratch\cutjig\p9r2\`, with crops at 100 percent and zooms. Own dry runs: `D:\Unleashed Robotics\_scratch\cutjig\des_r2\` (`dry225\`, `h_rev4\`, `h_fwd4\`, `final\`), each a copy of the Engineer's `p9r2\dry_f7_210\` harness with `check_sketch.py s3 --rev 2` and `s3_jackscrew_section.py --rev 2`. TMP/TEMP at `_scratch\cutjig\tmp`. Nothing under `docs/sketches/` edited.

Tags: MEASURED (read from a run or image in this session), DERIVED (hand arithmetic), DECLARED (spec, params, ruling), ASSUMED (working value).

## Corrections to the brief

1. **The F7 offset u -210 puts the dimension line on the ring rim.** `ring.od` is 420 (DECLARED), so the rim is at r 210. At 4x zoom of `dry_f7_210.png`, the red line runs on the rim end of the ring web at z_S about 390 (MEASURED). My M1 range (u -235 to -185) was wrong. From -210 to -185 the line lies over the ring at the ring height. The clear band at every height is u -244 (member c inner face, 274 - 30) to -210 (ring rim) (DERIVED). The pick is u -225 (item 3).
2. **The u -110 option crosses the ring web (z_S 380 to 400) and the gear's left piece (z_S 460 to 500)** (MEASURED, `dry_f7_110.png` crop). It is not a clear position.
3. **My r1 re-sign FIX C, "reversed hatch (cover)", is withdrawn.** Reversing "//" gives the steel direction, and the steel bearing races sit right beside the cover. In the dry run, the single "\\" alternate draws one or two lines in each cover piece, which reads as an unhatched piece (MEASURED, `des_r2\h_rev4_zoom.png`). The spec text `hatch_split.above: reversed hatch (cover)` changes (item 4).
4. **Neither F1 option reaches the 4:1 in my M1 F1.** Option A gives about 2.45 px/mm (MEASURED from the tick positions in `des_r2\final\wip\s3_jackscrew_section_r2.png`, 4157 x 3876 px). Option B detail_b gives 3.3 px/mm (Engineer, MEASURED), only 1.3 x option A. Option B also needs a new `projection_by_axes` rule and inset positions as spec values, and in the Engineer's layout detail_c overlaps detail_b. At 100 percent, option A shows each of these: the two bearings with balls, the locknut, the coupling, the four standoff lines, the pilot, the shaft, the inboard shoulder screw head and the nut in its boss (MEASURED, `des_r2\a_screwset.png`). The 0.05 axial play is 0.12 px at any of these scales (DERIVED). The label "floating nut, radial float 0.5" carries it, and the spec shape string already says so.
5. **D5 reaches S1.** `s1_mass_report.py` l.55 tags the top-end block "moving, not in W_kg", and the S1 RPT `com_height` prints W kg (DECLARED, code as read). Once W_kg includes the block, the S1 mass report and the S1 RPT text change, and the S2 tip-force basis is re-read. Total mass does not change, so the tip forces should not change (DERIVED; to be confirmed by the re-run). `step1.3_engineer_revision_r2.md` section 5 lists the S3 values only.
6. **The `kept_axial` part list still names the holder** (`s3_spec.yaml` l.247 text and `checks_s3.py` l.490: "collet, holder, receiver, base plate"). After the TP1.3-10 reroute, both reported cases are compression from core to seat to collet foot to receiver floor, and the holder is not in that path. Value in item 9.
7. **The current not_drawn text "two nut shoulder screws (off the plane)" is half false.** The rear screw, at x -13.86, lies inside the 60 beyond band (TP1.3-12, MEASURED live). Only the front screw, at x +13.86, is off the band.

## 1. Picks

| # | Item | Pick | Dry run (own unless named) |
|---|---|---|---|
| 1 | F1 scale | **Option A.** Spec in item 2 | `des_r2\final`: K3 pass with `FIGSIZE["section_yz"] = (20, 30)`; K4 to K7, K9, S3-1, S3-2, X1, SYM, RPT pass; K8 has only the 2 span_lt:ext items (item 3) (MEASURED) |
| 2 | D1 / F3 label text | sync_callout `text: 'sync:'`, key `liftsync.method`. hold_callout `text: 'power-off hold:'`, key `hold.device` | `final`: K4 pass in both Axes; each value printed once (MEASURED) |
| 3 | F7 offset | **span_lt `place.r_in` 225 (u -225)**: 15 from the ring rim, 19 from member c's face (DERIVED). About 37 and 46 px at option A (DERIVED) | `dry225` and `final`: K4, K5, K6, K7, K9, S3-2 pass. K8 fails 2, both span_lt:ext (drawn x [-225, -160], centre -192.50) (MEASURED). **span_lt:ext admitted, raised by me** (item 3) |
| 4 | Cover-hatch alternate | `section.hatch_alt: {aluminium: "////"}`: the aluminium angle at double density | `h_fwd4` and `final`: K8 shows no hatch item; the cover reads hatched and set apart by the joint line and the density (MEASURED, `des_r2\h_fwd4_zoom.png`). The alternate "\\" was rejected (Correction 3) |
| 5 | Rear nut shoulder screw | **Convention line plus deferred.** The not_drawn entry is split into front `off_plane` and rear `deferred` (item 5) | `final`: K8 clean of TP1.3-12; K4 figure-note branch pass (MEASURED) |
| 6 | Wing nut, drill head (TP1.3-11 classes) | **Keep the dashed split.** No cut rows. Pinion_c, liftmotor_pilot_c and the coupling stay as they are | No change. The Engineer's live run has clause (6) clean (K8-Z14) |
| 7 | D5 W_kg | **Yes (LF1.3-2).** Append `+ drill.top_block_mass` to `load_cases.W_kg` | `final` RPT: W 26.25 kg, 257.51 N; wob_max and kept_axial 1287.05 / 1104.16 N (MEASURED). Equals the Loftsman and Engineer section 5 values |
| 8 | D7 shoulder-bolt PCD | **PCD 180, theta 30 / 150 / 210 / 330, head D8.5, M5 blind-tapped 10 deep in the 12 plate.** not_drawn becomes `off_plane` with x bands | `final`: K2 pass (3 new leaves), K8 not_drawn lint clean, K4 figure note pass (MEASURED) |

Each `final` value was run together in one harness: 14 of 16 checks pass. K8 fails 2, both span_lt:ext. S3-3 fails 7, from the stale records only, since the copy has no accepted S1 r8 / S2 r9 (MEASURED).

## 2. F1, option A, full spec

- `sketch_common.FIGSIZE["section_yz"] = (20, 30)` (in), dpi 150 unchanged. The inset stays at `FIGSIZE["plan_xy"]` (10, 10), and the placement stays `_inset_right_of_labels`.
- The section Axes fills the figure height. The layout code puts the main Axes left; the labels and figure note fall to its right and the inset at the upper right. The saved image is 4157 x 3876 px at r2 + these picks (MEASURED).
- Scale: section about 2.45 px/mm (MEASURED). The screw-set parts are 10 to 100 px (anchor block 42 mm is 103 px; the nut boss 50 x 30 is 122 x 74 px; balls about 10 px) (DERIVED from 2.45).
- No detail Axes, no `insets` entry, no `projection_by_axes` rule.
- Gameplan detail 1.3 "Shows" carries the scale. This supersedes my M1 gameplan change 2 (the detail-view text), which has not been applied.

## 3. F7: span_lt at u -225, and the `span_lt:ext` admission (raised by The Designer)

- **Row value:** `span_lt.place: {r_in: 225, theta: 'jackscrew.angle[2]', half_width: 0, footprint: round}`. The dimension line is drawn at u -225 from z_S 340 (anchor bearing line) to 1210 (guide bearing line) (DECLARED z_rule).
- **Sub-artist `span_lt:ext`.** Two extension lines, Line2D, solid, in the row colour. Each is horizontal at one end of the row's z_rule and runs from the screw edge (u_c - jackscrew.nominal / 2) to the dimension line plus an overshoot.
- **Premise:** an extension line carries the measured feature (the bearing line on the screw) out to the dimension line and states no part. Its admission holds only where:
  - (e1) it is horizontal, at the z of a z_rule end of its parent (0.05);
  - (e2) it starts on the parent's measured feature, the screw edge at u_c ∓ nominal / 2 (0.05);
  - (e3) it ends past the dimension line by an overshoot of 0 to 3 mm and goes no further;
  - (e4) its parent is a `reference: true` row of kind line.

  The admitted artist has no area. It is left out of the parent's `projected_x` and `projected_extent`, which then read the dimension line alone at -225.
- **Z:** live S3 r3 with the pick.
- **B, each red on the r2 code with its own reason:**
  - (B-a) one extension 5 mm off the z_rule end (e1);
  - (B-b) start 5 mm off the screw edge (e2);
  - (B-c) end run on to u -244, onto member c (e3);
  - (B-d) `:ext` on a non-reference row (e4).
- The Engineer writes the rule and the fixtures with red-first. I sign them before the r3 M1.

## 4. Cover-hatch alternate

- Spec: `section.hatch_alt: {aluminium: "////"}`.
- `anchor_c.hatch_split.above` text: from `reversed hatch (cover)` to `section.hatch_alt (denser //, cover)`.
- Legend line 2 in the S3 script reads `aluminium // (anchor cover above the joint ////), extrusion xx, steel \\, brass ..`. Dry run `final`: K4 pass, and the line fits the image (MEASURED, `des_r2\final_legend.png`).
- The fixture stand-in "--" in `_designer_pending` is dropped.

## 5. Nut shoulder screws: two not_drawn entries

- `{part: "front nut shoulder screw", omit: off_plane, x: [["ring.nut_screw_pcd / 2 * sind(60) - ring.nut_screw_head_d / 2", "ring.nut_screw_pcd / 2 * sind(60) + ring.nut_screw_head_d / 2"]], x_source: "PCD 32 at +60 deg from the outboard radial, head D10 (Topologist TP1.3-12)", reason: "x +13.86, in front of the plane (cut away); leaf ring.nut_screw"}`
- `{part: "rear nut shoulder screw", omit: deferred, owner: "Step 2 (nut housing model, ring.nut_screw)", reason: "x -13.86, beyond the plane inside the 60 band: by the stated convention the inboard screw (row nut_screws_c) stands for the set of three; head D10 behind the screw and nut outline at 2.5 px/mm adds no reading (Designer 1.3 (h) r2 item 5)"}`
- figure_note: replace `two nut shoulder screws (off the plane);` with `front nut shoulder screw (cut away); rear nut shoulder screw (the inboard screw stands for the set);`.
- Why not a beyond row: the head would sit at u -173 to -163, partly behind the screw outline (-166 to -154) and the nut. The drawing would be a dashed and solid overlay inside a 30 px region that already holds the inboard head. The inboard screw drawn whole states the mechanism; the note states the count.

## 6. Wing nut and drill head: the dashed split stays

- The wing nut is a nut. By drafting convention nuts are not sectioned, and the section convention line already lists the head among the unsectioned parts.
- The drill head interior (wall and core-ring geometry) is ASSUMED (cutter OD ASSUMED 177.8). A cut row would draw an interior nobody has defined. The dashed hidden core inside the head reads correctly as "core inside the bit" (MEASURED, `a_screwset.png`).
- Pinion_c, liftmotor_pilot_c and the coupling keep their r2 drawing.

## 7. D5 W_kg

- `load_cases.W_kg` gains `+ drill.top_block_mass`. Values come from `final` RPT and equal Engineer section 5: W 26.25 kg, 257.51 N; least margin 3.97 unchanged.
- Uplift effect: 3 F_stall - W falls to 772.03 N. The bolt sizing stays on the gross 1029.5 N, so a larger W makes no sizing case less safe (DERIVED).
- Carry-on (Correction 5): `s1_mass_report.py` moves the block into the W items (tag l.55), and the S1 `com_height` RPT reads W 26.25. The Engineer re-runs `--stale`, `s1`, `s2` and the S3 RPT in the same session (process rule (i)).

## 8. D7 receiver shoulder bolts

- **Overlay leaves (ASSUMED):**
  - `receiver.shoulder_bolt_pcd` 180;
  - `receiver.shoulder_bolt_angle` [30, 150, 210, 330];
  - `receiver.shoulder_bolt_head_d` 8.5 (ISO 4762 M5).
- **Geometry (DERIVED):**
  - seat annulus r 80.2 to 100; bolt circle r 90;
  - clearance hole D5.5 at r 87.25 to 92.75, with ligament 7.05 to the plate hole and 7.25 to the rim;
  - head r 85.75 to 94.25, 5.75 clear of the receiver wall at r 80 (hex key straight down) and inside the tray hole r 101;
  - tapped M5, blind, 10 deep in the 12 plate.
- **Loads (DERIVED):** uplift 1029.5 N gross is 257 N per bolt. Core torque 10 N m at r 90 is 111 N shear, shared by four.
- **Azimuths:**
  - symmetric about X and Y;
  - none on the S3 plane x = 0;
  - heads at x ±77.94 ∓ 4.25, outside the 0 to -60 band.

  At 45 / 135 / 225 / 315 the heads would reach x -59.39 and enter the band by 0.61 (DERIVED).
- **S3 not_drawn:** `{part: "receiver shoulder bolts 4 x M5", omit: off_plane, x: [["-receiver.shoulder_bolt_pcd / 2 * sind(60) - receiver.shoulder_bolt_head_d / 2", "-receiver.shoulder_bolt_pcd / 2 * sind(60) + receiver.shoulder_bolt_head_d / 2"], ["receiver.shoulder_bolt_pcd / 2 * sind(60) - receiver.shoulder_bolt_head_d / 2", "receiver.shoulder_bolt_pcd / 2 * sind(60) + receiver.shoulder_bolt_head_d / 2"]], x_source: "PCD 180 at theta 30, 150, 210, 330, head D8.5 (Designer 1.3 (h) r2 D7)", reason: "x +-77.94, off the 60 band; drawn at S4-a"}`. In the figure note, `(layout open)` becomes `(off the plane, PCD 180)`.
- **S1 and S2:** the not_drawn reasons "PCD and azimuths open" are text in accepted specs and in their drawn notes. They change at the next drawn S1 / S2 revision; no revision opens for them alone.
- **`receiver.shoulder_bolts` value text:** "PCD and azimuths open (The Designer)" becomes "PCD 180 at theta 30, 150, 210, 330 (receiver.shoulder_bolt_*)".

## 9. kept_axial part list (TP1.3-10 owner line, Designer half)

- `kept_axial` text in the spec and in `checks_s3.py` l.490: "(collet, holder, receiver, base plate, compression)" becomes "(collet foot, receiver floor and shoulder, base plate, compression; holder not in the path, TP1.3-10)".
- The value 1000 N is unchanged. The Loftsman signs the other half.

## 10. K4 rule (i): SIGNED

- **Premise:** a label is read only when no other ink runs through its letters.
- **Implementation:** `sketch_common.text_overlap_issues`, as read.
  - (i1) tests each label's rendered arrow path against every text box, its own included. This covers the r1 hold leader that ended inside its own text.
  - (i2) tests every pair of text boxes, tick labels and titles included. This covers the r1 hold callout against the inset's "-300" tick label.
  - Boxes are shrunk 1 px.
- **Controls:** K4-Z3 (live S2), Z4 (live S1), B23 and B24 match the premise.
- The "anchor side" clause of my F2 is met through `edge_leaders` and (i1) on its own text.
- **NOTE (carried, no FIX):**
  - (i1) reads only `label:` annotations with an arrow_patch.
  - The inset sync fan is dotted Line2D. These lines and any future leader drawn as Line2D are outside the rule.
  - Today the fan meets no text (MEASURED, r2 and `final`).

## 11. Spec re-sign (r2 edits that are mine): SIGNED, with items 3, 4, 5, 8 and 9 applied

- **Chain kinds and reroute (part-list matter).**
  - Every link names a part that has a row. The base route core, core seat, collet, receiver, base plate matches the drawn axial-loop note (MEASURED, image).
  - The holder leaves only the chain; its row and part-list line stay.
  - Member feet and arm ends are `fastened`: correct, since in the cut case member c is pulled up at its foot by the screw tension.
  - Chains a and b collapse the bearing stack into `anchor_a|screw_a` (no rows for a/b bearings or locknuts in S3). This is accepted under the symmetry exception.
  - The kept_axial text is fixed in item 9.
- **not_drawn omit fields.** Signed, with the two entries changed in items 5 and 8. Every other entry's band and owner checked against the image.
- **plan_axes arc.** r 40, 0 to 90 deg, head at +Y, "theta" beside it. It reads as theta ccw from +X (MEASURED, inset). Signed.
- **screw_c root.** Two dashed lines at u -160 ∓ 4.25 (Tr12x3 d3 8.5) over z_S 360 to 1180 (thread 300 to 1120 z_A + 60) (DERIVED). The legend gave "dashed" one meaning, hidden edges. So line 3 of the legend gains `, thread root inside screw c`. Dry run `final`: K4 pass, the line fits (MEASURED, `final_legend.png`). Signed with that text.
- **Lever expressions.** u -190.00 / -182.00 from `liftsync.switch_r_in` / `lever_r_tip` × sind(270), pixel-equal. Signed.

## 12. For the Engineer at r3

Apply these: items 1 to 5, 7, 8, 9, and the legend text in items 4 and 11.

Then, in order:
1. Remove `_designer_pending`, then re-run K8-B82 and B83 on the live state.
2. Write the span_lt:ext rule with red-first.
3. Run `s3 --rev 3`.
4. Run `--stale`, `s1` and `s2` for D5.
5. Run `--controls`.

r3 gets a fresh M1.

## Gameplan lines to change

1. l.273 (detail 1.3 Shows). This replaces my `s3_visual_gate_r1.md` change 2, which has not been applied.
   ```
   Old: or the single-controller callout), so K9 sees all three.
   New: or the single-controller callout), so K9 sees all three. Section Axes at figsize 20 x 30 in (section_yz, about 2.45 px/mm) so every screw-set part reads at 100 percent (1.3 (f) M1 S3 r1 F1, option A at 1.3 (h) r2); S3-2 span L_t as a dimension at u -225 with extension lines from the two bearing lines (F7); anchor cover hatched with section.hatch_alt aluminium "////"; an axial-loop figure note naming where the loop leaves the plane (F6).
   ```
2. l.289 (S3-3 row). Insert into the Engineer's r2 change 6 New text after `every link carries a kind: face with its sense, face_record, thread, one_body, fastened, declared`.
   ```
   Old: every link carries a kind: face with its sense, face_record, thread, one_body, fastened, declared)
   New: every link carries a kind: face with its sense, face_record, thread, one_body, fastened, declared; RPT kept_axial names collet foot, receiver floor and shoulder, base plate, the holder out of the path, Designer 1.3 (h) r2)
   ```
3. l.705 (Design Notes 32). Append after its last sentence `the S1 certifier for that link is struck.`
   ```
   Old: the S1 certifier for that link is struck.
   New: the S1 certifier for that link is struck. Shoulder bolts (Designer 1.3 (h) r2, D7): 4 x M5 on PCD 180 at theta 30, 150, 210, 330, ISO 4762 head D8.5, blind-tapped 10 deep in the 12 plate (ASSUMED); heads off the S3 band (x +-77.94); 257 N per bolt at 1029.5 N gross. W_kg includes drill.top_block_mass (D5, LF1.3-2): W 26.25 kg.
   ```
4. Progress Log: insert after the Engineer's r2 row (beginning `| 1.3 | 2026-11-26 | (h) P9 (step1.3_engineer_revision_r2.md)`).
   ```
   New: | 1.3 | 2026-11-26 | Designer r2 values (step1.3_designer_r2_values.md): F1 option A (section_yz 20 x 30 in, 2.45 px/mm); labels 'sync:' and 'power-off hold:'; span_lt at u -225 (u -210 sat on the ring rim r 210) with span_lt:ext admission raised (premise e1 to e4); hatch_alt aluminium "////" (reversed withdrawn); rear nut shoulder screw deferred by convention, front off_plane; wing nut and head keep the dashed split; W_kg + top_block_mass (S1 mass report follows); receiver bolts PCD 180 at 30/150/210/330; kept_axial without the holder. Combined dry run 14/16 (K8 span_lt:ext 2, S3-3 stale). K4 (i) SIGNED (NOTE: Line2D leaders outside i1). r2 spec edits SIGNED with the root-line legend text |
   ```
