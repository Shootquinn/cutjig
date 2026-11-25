# Step 1.1 (h) Engineer revision, S1 r2 (from the (e) cross-review findings)

## Corrections to the brief

1. **LF1.1-1 does not resolve TP1.1-3.** The holder|collet interference sits at the holder bottom, 109.09 to 132.00 z_S, inside the collet height. The 8 mm flange fix moves only the holder top edge. TP1.1-3 needed its own drawing fix: the holder bore follows the collet outer cone over the collet height.
2. **build_parts/holder.py already models the holder with a 10 deg inner cone.** In that file:
   - r_od = receiver.register_bore_radius - register.g_reg = 67.04.
   - The cone starts at r_od - chain.t_h = 62.04 at the holder bottom and runs chain.H 30 up to r 56.75.
   - The bore above the cone stays at 56.75.
   - The flange runs from holder.length to holder.length + holder.flange_thickness. This confirms LF1.1-1.
   - The tube continues above the flange to the collar underside (0.75 lift play above the plate top), and the collar ring is collar.thickness 6.0 thick.

   S1 r2 draws a stand-in: the bore follows the drawn collet cone (r 67.29 at the receiver floor), and the bore above is at the core OD. The Designer rules the real section at M1 (list below). No spec row was added for it.
3. **Collar|holder cannot be C as S1 draws it.** The S1 holder ends at the flange top (145.09 z_A), and the collar row starts at the plate top (153.09). The 8.00 between them is the wing-nut plate, so the pair is declared F. In the part, the holder tube runs through the plate to the collar. That is a Designer shape item.
4. **Every former N pair between section rows is a measured contact,** except collar|holder: receiver|collet, receiver|core_seat, receiver|holder, collet|core_seat and collet|holder all read distance 0.000 and overlap 0.000 in all four poses (MEASURED). They are declared C.
5. **The smoke drawer (`fixtures/builders.py::_s1_draw_pose`) drew section rows as full-width rectangles.** It now draws them from the spec `section` field. That field now takes a list of pieces with z (receiver cup, holder plus flange), plus `bore_cone`. Without this change the live-spec Z controls fail the new C pairs.

Tags: drawn and check values MEASURED (run 2026-11-25). Stack values DERIVED. Inputs as `keys_read` lists them.

## Correction table

| ID | Finding (source words) | Fix | Predicate / rule | B fixture |
|---|---|---|---|---|
| LF1.1-1 | "Holder flange drawn 8 mm low; holder z_rule short by holder.flange_thickness" | Spec holder z_max = holder_bottom + holder.length + holder.flange_thickness. Script draws the flange from holder_bottom + holder.length. New spec field `stack_ties.holder_flange`: holder z_max + (nut.plate_thickness + washer.thickness - nut.washer_pocket_depth) + collar.top_above_plate = collar_top, linted in K6 beside LF-16 | K6 stack_tie (Z: K6-Z3, live spec) | K6-B7: r1 rule, "137.09 + 8.00 + 6.75 = 151.84 vs 159.84, 8.00 apart" |
| TP1.1-1 | "The gear taper predicate accepts a tooth face falling outward" | K8 predicate `face_rises: {toward: outward}` on the gear row. Per piece, a = the lowest vertex and b = the adjacent vertex with the larger radial change; requires (z_b - z_a)(abs x_b - abs x_a) > 0 | K8 face_rises (Z: K8-Z4) | K8-B14: heel low, face falling ("dz +15.00 over d abs x -35.00"); taper narrows down passes it |
| TP1.1-2 | "'Absent at park' is claimed for K9 and is not checked" | K9 adds the pose-set half-space: no tagged artist or Text of a row at a pose outside `row.poses`. Spec rubric line names it | K9 pose-set rule (Z: K9-Z2, live) | K9-B5: core_750 seated at park |
| TP1.1-3 (spec) | "collet\|holder becomes C. Add `section` ... lint refuses class N between two `section` rows" | `section` added to receiver (two pieces, cup), collet, core_seat, holder (two pieces, tube plus flange) and collar. K7 lint refuses N between two section rows. The N pairs are reclassified: five C, collar\|holder F. Spec header states the convention (TP1.1-8) | K7 section-N lint | K7-B14: collet\|holder N restored |
| TP1.1-3 (drawing) | "Holder and collet interpenetrate ... 313.12 mm2 per side" | Holder row `bore_cone: collet`. Over the collet height the holder piece runs from the cone face r = 67.29 - (z - 100) tan 10 to the register bore: r 65.687 at 109.09, 61.648 at 132.00 z_S (DERIVED). K5 admits that four-vertex piece only inside the mate's z extent | K7 C collet\|holder; K5 bore_cone admission (Z: K5-Z2) | K7-B15: r1 holder drawing, "overlap 626.239" x 4 poses. K5-B6: bore_cone piece 5 to 10 above the collet top |
| TP1.1-7 (NOTE) | third screw set and third motor undrawn, no figure says so | Untagged note on every figure, built from jackscrew.angle[-1] and pinion.angle[0] | visual only | none |
| LF1.1-2 (NOTE) | governing park clearance tested by no check | check_stack.reported `entry_plane_margin_mm` (no threshold): 0.00 | reported only | none |
| LF1.1-3 (NOTE) | reported reads params stop.start_z | `start_tip_minus_core_top_mm` reads the capture class start from the park rule (42.34, unchanged). The dead `start_tip_max` = 965 entry is removed from global_vars | reported only | none |

Files changed: `sketches/s1_spec.yaml`, `sketches/s1_side_poses.py`, `sketches/sketch_common.py` (K5, K6, K7, K8, K9), `sketches/check_stack.py` (reported, global_vars), `sketches/fixtures/builders.py`, `sketches/fixtures/manifest.yaml`. The spec now needs re-signing by the Designer, and by the Loftsman for the holder z_rule and `stack_ties`. The status line is unchanged, with an r2 edit comment under it.

## Check results (MEASURED)

`check_sketch.py s1 --rev 2`: K1 to K9 and S1-1 to S1-7, 17/17 pass on run 1 of the drawing. Two re-runs followed: one after the note placement moved and one after the check_stack reported edit. Both were also green.

| Check | Result | Reason |
|---|---|---|
| K1 | pass | 0 literals, s1_side_poses.py |
| K2 | pass | 219 spec keys resolve (r1 210) |
| K5 | pass | 291 tagged artists (r1 283; holder 6 pieces) |
| K6 | pass | 179 z_rules within 0.05; LF-16 planes and stack_tie holder_flange agree |
| K7 | pass | 309 pair tests clean (r1 285) |
| K8 | pass | 234 predicates (r1 230; face_rises x 4 poses) |
| K9 | pass | 45 rows, none drawn outside its poses |
| S1-1 to S1-7 | pass | unchanged: 650.00, 125.00, 367.34 / 117.34, 0.84, 192.34, 142.00, 8 projections, 607.66 (spare 72.73) |

Holder values in r2 (MEASURED, every pose):
- Flange: 197.09 to 205.09 z_S. Flange underside to rim 188.50: 8.59 = witness.zone_high (HAND: 137.09 - 128.50).
- collet|holder: distance 0.000, overlap 0.000. collar|holder: 8.00.
- ring|holder at capture_end: 169.75 vertical (374.84 - 205.09), 172.04 as the 2D minimum distance (r1 177.75 vertical).
- holder|wingnut: N, silhouette over section, 3471.68 mm2.

**Controls:** `--controls` gives 108 controls: Z 33/33 clean, B 74/74 fired, smoke 1/1, exit 0. The r2 additions are K5-Z2, K5-B6, K6-B7, K7-B14, K7-B15, K8-Z4, K8-B14, K9-Z2 and K9-B5.
**Stale:** `--stale` gives 0 records and 0 differences.
**Baseline:** the stub red set is unchanged. On the r2 spec it was checked in-process without writing: K1, K2, K3 and K5 are green (guard), K4 and K9 are red (content), and K6 to K8 and S1-1 to S1-7 are red (absent), identical to s1_checks_r0.json. `--baseline` was re-run because run 1 grew: run 1 is 33/33, 74/74 and 1/1, and run 2 is unchanged. The prior record is kept under `prior`.
**Reported:** unchanged from r1 (s1_summary_r2.md with the s1_mass_report section). The new entry_plane_margin_mm is 0.00.

## PNGs

- research/sean/cr_scratch/s1_pose_load_r2.png
- research/sean/cr_scratch/s1_pose_start_r2.png
- research/sean/cr_scratch/s1_pose_capture_end_r2.png
- research/sean/cr_scratch/s1_pose_park_r2.png

Also written: `sketches/s1_checks_r2.json`, `sketches/s1_summary_r2.md` and `sketches/s1_mass_report_r2.json`.

## For the Designer at M1 (no spec rows added; each needs Designer dimensions or a ruling)

1. **Holder and collet section.**
   - S1 r2 draws the holder OD at the register bore, with the bore on the drawn collet cone and the core OD above.
   - build_parts/holder.py has OD 67.04 (g_reg 0.25), inner cone 62.04 to 56.75 over chain.H 30 and bore 56.75 above. The tube runs through the nut plate to the collar, and the collar is 6.0 thick on a 0.75 lift play. S1 draws the collar from the plate top, 6.75 tall.
   - The S1 collet foot is drawn at r 67.29, against build_parts/collet_family.py, where the cone line passes r0 at holder.bottom_above_floor_Kmax.
   - Rule on whether S1 adopts the part section. Doing so makes collar|holder C and moves the contact radius.
2. **Screw-frame bracket arms, the descent-stop pad support, and the NEMA 23 and pinion shafts are undrawn.** The pad reads as floating at r 200 to 215. Options: new rows (bracket_a/_b, kind prism, radial place) with Designer dimensions, or accept them as absent at S1.
3. **Base plate spigot-hole break.** It is undrawn. The 80.2 hole against the 80 spigot opens the receiver|base_plate C pair by 0.20. Draw it only if wanted, with the pair reclassified.
4. **TP1.1-6:** the drawn gear face slope is 0.465 against the 1 in 3 pitch cone (0.333). The rise is the draw_gear_section default. The sense is now enforced by face_rises; the magnitude is the Designer's.
5. **TP1.1-4:** an optional predicate that the collet bore edge is vertical.
6. **TP1.1-9:** the zero-height anchor thrust line passes K5. Optionally close it.
7. **TP1.1-10:** the pinion toe is drawn at the envelope (K7-conservative).
8. **LF1.1-5:** the cutter head r 88.90 is 2.70 outside icd.keepout_radius 86.2.
9. **LF1.1-6:** mass-report modelling choices. LF1.1-4: zero margins are identities.
10. **Spec re-sign of the r2 edits** (header comment in s1_spec.yaml).

## Gameplan lines that need a change (for the orchestrator; gameplan not edited)

From the Topologist cross-review section 7, with the control IDs filled in:
- l.141 (K8 seed set): add "gear tooth face rises outward (cone apex below the gear), K8 face_rises" with K8-Z4 / K8-B14 (TP1.1-1).
- l.142 (K9): add "no artist of a row at a pose outside its `poses`" with K9-Z2 / K9-B5 (TP1.1-2).
- l.237 (rubric additions): "absent at park" is enforced by the K9 pose-set rule (K9-B5); the solid line is visual only.
- l.140 (K7 classes): "N is refused between two rows drawn in true section (spec `section`)" with K7-B14. The r1 holder interference is K7-B15 (TP1.1-3).

Engineer additions:
- l.138 (K5): a `bore_cone` row's four-vertex piece is admitted only inside its mate's z extent (K5-Z2 / K5-B6).
- l.139 (K6): `stack_ties` linted like the LF-16 planes; holder flange tie (K6-B7, LF1.1-1).
- l.144 (control count): append "1.1 (h) r2 added K5-Z2, K5-B6, K6-B7, K7-B14, K7-B15, K8-Z4, K8-B14, K9-Z2, K9-B5 (108 controls: Z 33, B 74, smoke 1)".
- Carried from r1 open items 4 and 5: l.144 S1-2-B2 insertion and l.229 append. Both are still pending if not yet applied.
