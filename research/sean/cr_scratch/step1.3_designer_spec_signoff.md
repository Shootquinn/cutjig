# Step 1.3 (b) Designer spec sign-off, S3 section A-A through screw c

Read: `step1.3_designer_params_review.md`, `step1.3_engineer_spec.md`, `docs/sketches/s3_spec.yaml` (whole), `proposed_params.yaml` (jackscrew, liftmotor, hold, liftsync, liftload), gameplan l.148-153, 164-206, 212-295, Design Notes 4 and 31, `s1_spec.yaml` and `s2_spec.yaml` liftmotor and reported_items rows, `s1_checks_r7.json` and `s1_mass_report_r7.json` reported fields, `checks_s2.reported`, `check_sketch.py` RPT. Heights z_A unless marked z_S (z_S = z_A + 60).

Dry runs: a scratchpad copy of `docs/sketches/` with `params.yaml` beside it (nothing under `docs/sketches/` edited). Copy edits: overlay `jackscrew.nut_body_od` 22, `jackscrew.nut_flange_thickness` 8, `liftmotor.shaft_gap` 1, `liftmotor.coupling_length` 25 to 36; s3 coupling_c and screw_end_c z_rule per FIX 2. Runs: `check_stack.py s3_spec.yaml`; K2 key resolution and `expr_agreement_issues` on s3; `check_sketch.py s1 --rev 7` and `s2 --rev 5` at coupling_length 36 and again at 25 (`--overlay`, `--wip-dir`), records diffed field by field; section-piece overlap and distance script for the screw-set rows (rectangles in (u, z), the K7 C/F/G tolerances).

## Corrections to the brief

1. **The nut does not fit its housing as written.** With any flange nut (nut_body_od < nut_flange_od), `nut_housing_c.section_u` bores the housing to `nut_body_od / 2 + nut_float` over its full height, and `nut_c` puts the flange (r 21) inside that wall over its top `nut_flange_thickness`. At 22 / 8: overlap 152.0 mm² in the section (DERIVED, dry-run script), so the declared C pair nut_c|nut_housing_c reads interference. The housing needs a flange counterbore (FIX 1).
2. **The screw is drawn 12 wide through 10-bore bearings.** `screw_c` is one rectangle, nominal 12, anchor_z to top_guide_z. Against the bearing pieces (inner faces at journal_d / 2 = 5): overlap 32.0 mm² at the anchor pair and 16.0 mm² at the guide bearing (DERIVED). The shape text names the journal 10; no row or field draws it (FIX 3).
3. **The anchor as specified is not a fixed end.** `anchor_c.section_u` bores the block to bearing OD 26 over all 30 mm; nothing holds the outer races axially, and nothing holds the inner races on the screw (the locknut is `not_drawn`). Sean's K 0.7 credit "rests on the fixed-anchor credit" (Design Notes 31); the section must show what makes the end fixed. In the cut case the screw pulls the inner races up; in every compression case it pushes them down; both directions need a drawn stop. My (a) shape note ("bore with two angular-contact bearings, locknut above") did not set it; the locknut goes below (FIX 3).
4. **Coupling stack (Engineer Correction 5) confirmed.** Motor face 240, shaft tip 264.00, coupling 243.5 to 263.5, screw end 253.5 to 265: shaft and screw end overlap 10.50 inside the coupling (DERIVED). My (a) section 3 placed the coupling in the 25 gap without checking the 24 shaft. FIX 2.
5. **Home switches a, b name a lever that is not drawn.** `home_switch_a/_b` shape text: "roller lever drawn down to the nut-housing top at park (sub-artist home_switch_a:lever)", with `sub_artists: []` and inset-only axes (FIX 4).
6. **`load_comp_c` label omits its key value and the retract case.** Label key `liftload.f_bind` (300); text "static, capture, stall". The S3-2 cases are four (static 79.30, capture 113.31, retract 179.30, stall up 343.18 N per screw, DERIVED) (FIX 5).
7. **Rubric line "member c and the -Y rail on the left ... (K8 side predicates)" has no predicate for member c or pinion c.** Only screw_c (sign -1) and motor23_c (sign +1) carry `side` (FIX 6).
8. **Coupling_length is read by both accepted records.** Moving it adds `liftmotor.coupling_length` to the --stale lists of s1_checks_r7.json and s2_checks_r5.json (MEASURED, dry-run keys_read diff: 25 to 36). S1 r8 and S2 r9 are already open on `jackscrew.nominal` / `.lead`, so no new revision opens.

## 1 Part list

Every part a `shape` string names, with its row or `not_drawn` entry. As received: 63 rows, 11 not_drawn entries, 2 named parts with neither (MEASURED, spec text).

| Part (named in shape text) | Row / not_drawn |
|---|---|
| shop floor line | floor |
| -Y and +Y rails (slot notches, centre-bore lines) | base_frame |
| base plate, spigot-hole gap | base_plate |
| receiver (debris-hole gap, spigot, thread ticks) | receiver |
| collet (slit ticks) | collet |
| core-seat ledge | core_seat |
| holder tube and flange | holder |
| wing nut, wings, sweep lines | wingnut |
| collar ring | collar |
| capture core | core_750 |
| cutter and iris head (cutter ticks) | drill_head |
| drill tube walls | drill_tube |
| top-end block (cable-exit mark) | drill_top_block |
| keep-out lines / circle | keepout |
| ring plate pieces | ring |
| nut-housing boss c | nut_housing_c |
| nut retaining ring | not_drawn |
| floating nut c, body and flange | nut_c |
| anti-rotation pin | not_drawn |
| drill-to-ring bearing | bearing |
| ring gear (tooth ticks), gear hub | gear, gear_hub |
| pinion c, NEMA 23 c, its shaft, its mount, pinion axis | pinion_c, motor23_c, motor_shaft_c, motor_mount_c, pinion_axis_c |
| screw c, thread ticks | screw_c |
| **screw journals 10 in the anchor and guide bearings** | **missing (FIX 3)** |
| screw end into the coupling | screw_end_c |
| anchor block c | anchor_c |
| angular-contact pair, balls, bearing line | anchor_bearing_c (sub-artists balls, line) |
| anchor locknut | not_drawn as received; row anchor_locknut_c after FIX 3 |
| top-guide block, radial bearing, balls | guide_c, guide_bearing_c (sub-artist balls) |
| anchor and guide bracket arms c | bracket_anchor_c, bracket_guide_c |
| member c | frame_upper_c |
| NEMA 17 c, pilot, shaft | liftmotor_c, liftmotor_pilot_c, liftmotor_shaft_c |
| beam coupling (slots) | coupling_c |
| rear M3 standoffs; front M3 standoffs | standoffs_c; not_drawn |
| home switch c and lever | home_switch_c (sub-artist lever; geometry FIX 4) |
| **home switch a, b levers** | **missing (FIX 4: shape text corrected, inset draws no lever)** |
| hold callout | hold_callout |
| nut stations start, park; L_t dimension | nut_station_start, nut_station_park, span_lt |
| load arrows cut, tension, compression | load_cut, load_tension_c, load_comp_c |
| inset: screws, housings, blocks, lift motors, members, switches a, b, c | screw_a/_b/_c, nut_housing_a/_b/_c, anchor_a/_b/_c, liftmotor_a/_b/_c, frame_upper_a/_b/_c, home_switch_a/_b/_c |
| inset: controller callout and leaders, ring OD reference, A-A line, axes and theta arc | sync_callout, ring_ref, section_line, plan_axes |
| screw a set, screw b set, pinions a b, NEMA 23 a b, guide rods with lugs, housings and ties, descent-stop pad and post, base-frame end members and supports | not_drawn (figure note) |

After FIX 3 and 4: 64 rows, 10 not_drawn, 0 missing. The figure note drops "anchor locknut".

## 2 Shapes, section convention, inset

Row shapes match my (a) section 7 notes except items in Corrections 1 to 5. Section convention (cut / unsectioned / beyond / omitted, hatch per material, far half of a cut row not redrawn) matches my section 2. Section plane, look direction, handedness, pose capture_end and the nut stations match. Inset content matches section 2 (screws, housings, 42-square blocks, dashed lift motors, members, three switches, controller callout with leaders, keep-out, ring reference, A-A with arrows toward -X, axes and theta arc). The inset is its own Axes for TP-7.

Representative shape after the FIXes (8.4b): the section reads as a fixed end (outer races between a bore shoulder and a cover, inner races between the screw shoulder and a locknut), a radial-only guide, a floating flange nut in a counterbored boss, and a motor coupled to the screw with both shafts engaged.

## 3 Options, load cases, reported_items

| Item | Rulings / recommendation | Spec | Result |
|---|---|---|---|
| Screw | Tr12x3 single start (Design Notes 31) | nominal 12, lead 3, root 8.5, label "Tr12x3 screw L 900, lead 3" | PASS |
| Nut mounting | floating, 0.5 radial, axially clamped, pinned | nut_c, nut_housing_c, ring.nut_mounting | PASS after FIX 1 |
| Hold | self-locking lead, callout | hold_callout, hold.device | PASS |
| Sync | single controller, home switch per screw, no belt | sync_callout, home_switch_a/_b/_c, liftsync.* | PASS after FIX 4 |
| Anchoring | fixed anchor (back-to-back pair), radial top guide | anchor_c, anchor_bearing_c, guide_c, guide_bearing_c | FIX 3 |
| Load cases | my section 6; F_bind 300, SF 3 (Design Notes 31) | load_cases, per-screw 79.30 / 113.31 / 179.30 / 254.04 / 343.18 | PASS (Engineer rounding, Correction 7, accepted) |
| reported_items | my section 12, against detail 1.3 Reported (L_min, critical speed, P_cr margin, F_stall, kept-part axial force, back-drive) | 10 ids, tension_segment needs_drawing | PASS, complete |

## 4 Neighbour classes and g_min

Spec classes match my section 9 for every listed pair. Values on the spec with the FIXes applied (DERIVED, dry-run script; z_A):

| Pair | Class, g_min | Value |
|---|---|---|
| nut_housing_c \| anchor_c (capture_end) | G 10 | 10.84 |
| nut_housing_c \| guide_c, \| home_switch_c (park) | G 10 | 24.16, 11.16 |
| ring \| home_switch_c (park) | G 10 | 20.16 |
| coupling_c \| anchor_c | G 1 | 2.00 (2.06 at the bore corner) |
| coupling_c \| liftmotor_pilot_c | G 1 | 12.00 |
| liftmotor_shaft_c \| screw_end_c | F | 1.00 gap (was 10.50 overlap) |
| nut_c \| nut_housing_c | C | 0.00, no overlap (counterbore shoulder; was 152.0 mm² overlap) |
| screw_c \| nut_c; screw_c \| anchor_bearing_c; screw_c \| guide_bearing_c | C | 0.00 each, no overlap (was 32.0 and 16.0 mm²) |
| anchor_c \| anchor_bearing_c | C | 0.00 (bore face, shoulder at 272, cover at 288) |
| screw_c \| anchor_c; screw_c \| guide_c | F | 2.00; 7.00 |
| anchor_locknut_c (new) \| screw_c, \| anchor_bearing_c | C | 0.00 |
| anchor_locknut_c \| anchor_c | F | 1.00 |
| screw_end_c \| anchor_locknut_c; coupling_c \| anchor_locknut_c | F | 1.41; 3.00 |
| nut_c \| anchor_c (capture_end) | undeclared F | 10.84 |

anchor_locknut_c joins `fixed_g10` (moving parts against it: housing bottom 305.84 to locknut top 272 at capture_end, 33.84).

## 5 Operator-task rows

Both S3 rows (gameplan l.187, 188) agree with the spec except the coupling height after FIX 2: coupling z_S 303 to 323 (was 303.5 to 323.5), and 12 of bare 5 mm motor shaft below each coupling (z_S 291 to 303), turning when the lift runs. Gameplan line 1 below.

## 6 Rubric additions

| Addition | True on the spec values | Predicate |
|---|---|---|
| V1 NEMA 17 under the block, nut in the housing | yes: motor 181 to 229 under block 265 (FIX 2); nut in housing | K8 liftmotor_c below anchor_c; nut_c above anchor_c |
| V5 anchor, nut, guide order | yes: bearing line 280 < nut bottom 365.84 at capture_end < guide 1135 | K8 below / above; S3-1 |
| Section handedness | yes for screw c (u -160), NEMA 23 c (u 142 to 218), member c (u -304 to -244), pinion c (u 95.22 to 140) | screw_c, motor23_c only: FIX 6 adds frame_upper_c (sign -1), pinion_c (sign +1) |
| Inset handedness | yes | K8 per Axes (P4) |
| V6 | yes | K5 per Axes (P4) |
| V7 | yes after FIX 3 | visual-only: FIX 6 marks it |
| V10 | yes; the drawn pose is capture_end, so the reviewer judges the hold row from nut_station_park (load tip = park tip 959.84) and the coupling row from fixed parts | visual-only: FIX 6 marks it |

## 7 Engineer blockers and open items

**Blocker 1, nut keys (FIX 1).** `jackscrew.nut_body_od` 22, `jackscrew.nut_flange_thickness` 8 (ASSUMED; Tr12x3 brass flange nut, body D22, flange D42 x 8, length 30, typical catalogue form; vendor open, batch 2 B2-1). With the floating mount: lower bore D23 (22 + 2 x 0.5), wall 13.5; flange counterbore D43 (42 + 2 x 0.5), 8 deep, wall 3.5; flange seated on the counterbore shoulder, retaining ring over it (not drawn). Dry run: K2 key resolution on s3 in the copy: 369 spec keys resolve, 0 missing; 20 expr leaves agree (MEASURED).

**Blocker 2, coupling stack (FIX 2).** Remedy: motor position. `liftmotor.coupling_length` 25 to 36 (motor face to block underside, = standoff length; ASSUMED); new `liftmotor.shaft_gap` 1 (motor shaft tip to screw end, inside the coupling; ASSUMED). The coupling is placed from the shaft tip, half its length on each shaft:
- motor 181 to 229, pilot top 231, shaft 229 to 253;
- coupling 19 x 20 at 243 to 263 (motor shaft engaged 10.00, 2.00 below the block, 12.00 above the pilot);
- screw end d 8 at 254 to 265 (engaged 9.00), 1.00 above the shaft tip.
All DERIVED; the coupling length 20 and the shaft 24 unchanged. Dry run (MEASURED, scratchpad copy): check_stack on s3 gives coupling 303.0 to 323.0, screw end 314.0 to 325.0, shaft 289.0 to 313.0, motor 241.0 to 289.0 z_S. `check_sketch.py s1 --rev 7` at 36: every check result equal to the run at 25 (K5 red at both, the known anchor zero-area Rectangle; RPT exempt); S1-4 0.84, S1-5b 142.00, K7 618 tests clean; least K7 distance moved: wingnut|liftmotor_a/_b XZ 38.91 to 27.91 (undeclared F, 0 overlap; plan-separated, motor r_in 130.30 > sweep 115). `s2 --rev 5` at 36: 19/19 at both; S2-2 52.80, S2-5a 11.71, S2-5b 19.84 unchanged; only base_plate|liftmotor_k z-separation 180.00 to 169.00 moved. No S1 or S2 margin moves; the drawn S1 motors drop 11.00 (lands with S1 r8 at P6).
Alternatives considered: a 13.5 motor shaft (cut shaft on the motor Sean has, B2-2) or a longer coupling in the 25 gap (the 24 shaft still reaches 264); both rejected.

**Blocker 3, S1/S2 anchor place at P6.** Confirmed. The S3 anchor_a/_b/_c rows keep `x1_exempt` until P6; P6 lands the 42-square place in s1_spec.yaml and s2_spec.yaml with the redraw and removes the exemption in the same edit, so X1 then compares those rows. bracket_anchor r_in keeps `nut_flange_od / 2` (value 21 = anchor_block_width / 2) until the same edit.

**Blocker 4, S1 r8 reported_items.** Section 8.

**Open items (Engineer section 8).**
- 2 (pin, locknut, retaining ring): the locknut is drawn (FIX 3); pin and retaining ring stay not_drawn, named in the nut and housing shape text.
- 4 (bearing-line mark, section form): no objection; the Topologist sets it at P4.
- 6 (`liftmotor.standoff_af` 5.5): confirmed, M3 hex across flats 5.5 (ISO 4032 M3 nut size; ASSUMED). The standoff length is now 36.
- 8 (symmetry premise lint): required at P4. Without it S3-3 lists eight a/b pairs uncertified.
- 9 (core mass 10.4 in the spec): NOTE. Move it to an overlay leaf `liftload.core_mass_capture` 10.4, DERIVED, source Quinn's Source Verification Register (density ASSUMED), so the spec carries no unsourced literal; at P4 or P6.
- 10 (S1 "T8" label text): S1 r8 at P6.
- 11 (home-switch lever): FIX 4.

## 8 S1 r8 reported_items (blocker 4)

From gameplan detail 1.1 Reported (l.242). For `s1_spec.yaml` at P6, with `checks_s1.reported(ctx)` returning `items` ({id: {value, basis, tag}}) as checks_s2 does; RPT reads it.

```yaml
reported_items:   # 1.3 (b) Designer sign-off section 8; gameplan detail 1.1 Reported; RPT reads checks_s1.reported(ctx) items
  - {id: highest_point, text: "Highest point at each pose and its margin to the 2000 mm soft target (jig.height_target), parts only, reference rows excluded (LF1.2-5)", source: "drawn extents over parts per pose (checks_s1.reported); spec value check_stack.reported poses highest_z_S, margin_to_soft_target", needs_drawing: true}
  - {id: ring_position, text: "Ring position along the drill (N1): ring underside above the cutter tip, and ring underside and top per pose", source: "ring.position_above_tip, ring.thickness; check_stack pose vars ring_bottom, ring_top", needs_drawing: false}
  - {id: anchor_guide_heights, text: "Anchor and top-guide heights the ring position sets: anchor block, top-guide block, bearing lines and span L_t, with the S1-4 least margin", source: "jackscrew.anchor_z, anchor_allowance, top_guide_z, guide_allowance, anchor_bearing_z, guide_bearing_z; S1-4 measured", needs_drawing: false}
  - {id: park_rule, text: "Re-derived park rule as an expression for Step 4, with the park tip by plane and core length and the symbol c validity ranges (N11)", source: "spec park_rule; check_stack.reported park_tip_z_A, park_tip_by_plane_z_A, drawn_symbol_validity", needs_drawing: false}
  - {id: lift_stroke_q9, text: "Lift stroke per Q9 option (0.5 m only; 0.5 and 0.75 m; plus 1 m), with the c terms", source: "check_stack.reported q9_options lift_stroke, symbol_terms", needs_drawing: false}
  - {id: screw_length_q9, text: "Screw length L_min and L at the drawn anchor per Q9 option (detail 1.3 expression), against the drawn jackscrew.length 900 and DN23 800 to 900", source: "check_stack.reported q9_options L (spec screw_length); jackscrew.length", needs_drawing: false}
  - {id: com_height, text: "Centre-of-mass height per pose (overlay masses, ASSUMED)", source: "s1_mass_report.py logic, same revision: com_z_S per pose; items per the note below", needs_drawing: false}
  - {id: tip_force, text: "Unbolted tip force at the frame top and at the CoM height per pose (icd.tipover_statement is the old-design reference)", source: "s1_mass_report.py logic: tip_force_frame_top_N, tip_force_at_com_N", needs_drawing: false}
```

Mass-report items at S1 r8 (com_height and tip_force depend on them): the moving mass matches `s3_spec.yaml load_cases.W_kg` (24.25 kg): add drill-to-ring bearing 1.5, pinions 3 x 0.5, gear hub 0.7, guide bushings with housings 2 x 0.2 (overlay `bearing.mass`, `pinion.mass`, `gear.hub_mass`, `guide.bushing_mass`); screws "Tr12x3 screws x3" at nominal 12: 3 x pi / 4 x 12² x 900 x 7.85e-6 = 2.40 kg (DERIVED; r7 carries "T8 screws x3" 1.065); NEMA 17 x3 from `liftmotor.mass` 0.35 each (same 1.05) at the new motor height (centre 205 z_A after FIX 2).

## 9 FIX items

1. **nut_c, nut_housing_c (overlay, rows).** Add overlay leaves `jackscrew.nut_body_od` 22 and `jackscrew.nut_flange_thickness` 8 (ASSUMED, source "Tr12x3 brass flange nut, body D22, flange D42 x 8, length 30; Designer 1.3 (b) sign-off FIX 1; vendor open, batch 2 B2-1"). Replace `nut_housing_c.section_u` by four pieces (u offsets from `jackscrew.pitch_radius * sind(jackscrew.angle[2])`): lower band, nut_z - housing_height / 2 to nut_z + nut_length / 2 - nut_flange_thickness, from housing_od / 2 to nut_body_od / 2 + nut_float, both sides; counterbore band, nut_z + nut_length / 2 - nut_flange_thickness to nut_z + housing_height / 2, from housing_od / 2 to nut_flange_od / 2 + nut_float, both sides. Add `jackscrew.nut_flange_thickness`, `jackscrew.nut_flange_od` to its keys. nut_housing_c shape: "ring boss D50 x 30, bore D23 over the nut body (0.5 float), counterbore D43 x 8 at the top for the flange, flange seated on the counterbore shoulder, retaining ring over the flange (not drawn)". Dry run: section 7 blocker 1 and section 4 (overlap 152.0 mm² to C at 0.00; K2 369 keys, 0 missing).
2. **liftmotor_c, liftmotor_pilot_c, liftmotor_shaft_c, coupling_c, screw_end_c, standoffs_c (overlay, rows).** `liftmotor.coupling_length` 25 to 36; source text "motor face to anchor-block underside = M3 standoff length; shaft 24 with half the 20 coupling on each shaft and shaft_gap 1 (Designer 1.3 (b) sign-off FIX 2)". New leaf `liftmotor.shaft_gap` 1 (ASSUMED). `liftmotor.coupling` and `coupling_height` source texts: "z 243 to 263 z_A in the 36 gap, 2.0 below the block, 12.0 above the pilot". `liftmotor.screw_end_d` source: "9 engaged". coupling_c z_rule: z_min `jackscrew.anchor_z - liftmotor.coupling_length + liftmotor.shaft_length - liftmotor.coupling_height / 2`, z_max the same `+ liftmotor.coupling_height / 2`; shape "z 243 to 263". screw_end_c z_rule: z_min `jackscrew.anchor_z - liftmotor.coupling_length + liftmotor.shaft_length + liftmotor.shaft_gap`, z_max `jackscrew.anchor_z`; delete its convention note. liftmotor_c shape "body 42 x 48 (z 181 to 229)". liftmotor_shaft_c|screw_end_c F source: "1.0 gap at the shaft tip". Keys lists gain `liftmotor.shaft_length`, `liftmotor.shaft_gap` where read. Run --stale and S1, S2 the same session (detail 1 common (i)): coupling_length joins the open S1 r8 / S2 r9 lists. Dry run: section 7 blocker 2.
3. **anchor_c, screw_c, new row anchor_locknut_c (overlay, rows): draw the fixed end.** New overlay leaves (ASSUMED, source "fixed-end layout, Designer 1.3 (b) sign-off FIX 3"): `jackscrew.locknut_od` 18, `jackscrew.locknut_thickness` 6 (M10x1 locknut), `jackscrew.anchor_shoulder_bore` 20, `jackscrew.anchor_cover_bore` 16. Layout (z_A): locknut zone 265 to 272, bearings 272 to 288, cover zone 288 to 295; anchor_bearing_z 280 and anchor_allowance 30 unchanged.
   - anchor_c section_u, three bands per side: anchor_z to anchor_bearing_z - anchor_bearing_width, from anchor_block_width / 2 to anchor_shoulder_bore / 2 (outer-race shoulder at 272); anchor_bearing_z ± anchor_bearing_width, to anchor_bearing_od / 2; anchor_bearing_z + anchor_bearing_width to anchor_z + anchor_allowance, to anchor_cover_bore / 2 (cover over the outer races at 288). Shape: "anchor block 42 square x 30, one hatched body with its cover: bore 26 for the back-to-back pair, shoulder bore 20 under the outer races, cover bore 16 over them; locknut (row anchor_locknut_c) under the inner races; outer face on the arm end at r 181".
   - screw_c drawn outline (new outline field, the Engineer names it; place and z_rule unchanged for X1): journal_d wide from anchor_z to anchor_bearing_z + anchor_bearing_width (M10x1 thread under the locknut, journal in the bearings), nominal wide from there to top_guide_z - guide_allowance (shoulder on the upper inner race at 288), journal_d wide to top_guide_z (guide journal, 11 below the guide bearing, no axial contact). K6 reads the z_rule envelope; K5 admits the stepped outline on the unsectioned row (rule and Z/B at P4, raiser the Topologist).
   - anchor_locknut_c: kind cylinder, unsectioned outline over the bore, z anchor_bearing_z - anchor_bearing_width - locknut_thickness to anchor_bearing_z - anchor_bearing_width (266 to 272), place round half_width locknut_od / 2 at screw c; neighbours screw_c C (thread), anchor_bearing_c C (clamps the inner races), anchor_c F, in fixed_g10; chain [axial]; hatch steel. Remove "anchor locknut" from not_drawn and the figure note.
   - S3-3 chain c is unchanged (anchor_c, anchor_bearing_c, screw_c); add a note on anchor_bearing_c|screw_c and anchor_c|anchor_bearing_c that the axial contact is the shoulder / cover / locknut faces.
   Dry run (DERIVED, section 4 table): block|bearing 0.00, screw|bearing 0.00, locknut|screw 0.00, locknut|bearing 0.00, screw|block 2.00, locknut|block 1.00, no overlap anywhere.
4. **home_switch_c, home_switch_a, home_switch_b (rows).** home_switch_c:lever is drawn in its free state as a line (no area, outside K7): from the switch bottom inboard corner (r 190, 1122) to (r 182, 1112) z_A, tip 1.16 above the housing top at park and 3 inboard of the housing rim (r 185). The ring trips the switch about 2 above park when homing and backs off to park; K7 judges the switch body only (pairs as declared, 11.16 and 20.16 at park). home_switch_c shape: "micro switch under the top-guide arm, body 13 x 20 x 6 at r 190 to 210, top on the arm underside; roller lever in its free state reaching to 1112 z_A over the housing rim (trips about 2 above park when homing)". home_switch_a/_b shape: "home switch 20 x 6 radial rectangle at r 190 to 210 (inset)". Dry run: arithmetic only (no K rule judges a line sub-artist's z today).
5. **load_comp_c (label).** Text "compression per screw: static 79, capture 113, retract (F_bind 300) 179, stall up 343 N", key `liftload.f_bind`; shape the same four values.
6. **frame_upper_c, pinion_c, rubric_additions.** Add `{pred: side, of: drill_tube, sign: -1, axes: section}` to frame_upper_c and `{pred: side, of: drill_tube, sign: 1, axes: section}` to pinion_c (Designer 1.3 (a) section 2 handedness). Append "(visual-only)" to the V7 and V10 rubric lines; V10 line text: "V10: the operator rows of gameplan detail 1 common for S3, judged on fixed parts (couplings, standoffs, motor shafts) and on nut_station_park for the ring at load (load tip = park tip) (visual-only)".

Verdict: **FIX** (6 items: 1 nut_c / nut_housing_c, 2 coupling stack, 3 fixed anchor and screw journals, 4 home switches, 5 load_comp_c label, 6 side predicates and rubric). Blocker 3 confirmed. S1 r8 reported_items given (section 8).

## Gameplan lines to change

1. l.188, within the line. Old: "couplings (r 150.5 to 169.5, z_S 303.5 to 323.5) 35.5 radially from the hand zone, exposed between the standoffs; the lift is idle at load;" New: "couplings (r 150.5 to 169.5, z_S 303 to 323) 35.5 radially from the hand zone, exposed between the standoffs, with 12 of bare 5 mm motor shaft below each (z_S 291 to 303); the lift is idle at load;"
2. l.242, append at the end of the line (after "is the old-design reference)."): " From S1 r8 these are the spec field reported_items in s1_spec.yaml (8 ids: highest_point, ring_position, anchor_guide_heights, park_rule, lift_stroke_q9, screw_length_q9, com_height, tip_force; Designer 1.3 (b) sign-off section 8), read by RPT from checks_s1.reported items; the mass report carries W 24.25 kg (s3_spec load_cases.W_kg) and Tr12x3 screws."
3. Engineer spec item 1 (l.272), replace its new text by: "Shows: bottom anchor (fixed: two angular-contact bearings back-to-back in a 42-square block, outer races between a bore shoulder and a cover, inner races between the screw shoulder and an M10x1 locknut; Design Notes 31, Designer 1.3 (b) FIX 3), screw"
4. Engineer spec item 2 (l.272), in its new text, old: "NEMA 17 on four standoffs under the anchor block with a beam coupling" new: "NEMA 17 on four M3 standoffs 36 long under the anchor block with a beam coupling 19 x 20, half on each shaft (Designer 1.3 (b) FIX 2)"
5. Engineer spec item 9 (insert after l.718), in its new text, old: "| Anchor block **42 square x 30**; bearing lines **280** and **1150** z_A, span L_t **870** |" new: "| Anchor block **42 square x 30**; bearing lines **280** and **1150** z_A, span L_t **870**; lift motor face **229** z_A (`liftmotor.coupling_length` 36) |"
