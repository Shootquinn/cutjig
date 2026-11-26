# Step 1.3 (a) Designer params review, S3 section through screw c

Sources (read 2026-11-26): gameplan l.115-209, 262-297, 507-560 (Design Notes 1, 2, 11, 13, 16), 617-760 (Design Notes 22 to 30, Echo Site Registry, Open Questions); step1.3_manager_open.md sections 0 to 3; my 1.1 and 1.2 params reviews; `docs/sketches/proposed_params.yaml` (whole); `s1_spec.yaml` rows ring, nut_housing_a, screw_a/_b, nut_a/_b, anchor_a/_b, guide_a/_b, liftmotor_a/_b, frame_upper_a/_b, bracket_*, descent_stop*, neighbour groups; `s2_spec.yaml` rows base_plate, base_frame, frame_upper_a/_b/_c, screw_c set, descent_stop*; `s1_checks_r7.json` and `s2_checks_r5.json` keys_read, reported, sketch checks; params.yaml `loads`, `upper`, `core`, `profile`, `base`, `frame`, `stop`, `icd`; step1_quinn_batch1.md; llm_plm_cad.md 8.4 to 8.4.2; ASSEMBLY.md Coordinate frame; `s1_pose_park_r7.png` and `s2_plan_r5.png` read as images. Arithmetic by a scratch script outside the project (thread, buckling, stall, critical speed). Heights z_A unless marked z_S (z_S = z_A + 60). E 200 GPa, steel density 7850 kg/m³, thread flank half-angle 15 deg, g 9.81: working values, ASSUMED.

## Corrections to the brief

1. **W omits four moving masses.** The O3 W (20.15 kg) has ring 6, drill 8, gear 3, three NEMA 23 3.0, nuts 0.15. The ring also carries the drill-to-ring bearing, three pinions, the gear hub and two guide bushings in housings, none with a mass leaf. Proposed (ASSUMED): bearing 1.5, pinions 3 x 0.5, gear hub 0.7 (aluminium clamp ring OD 180, bore 152.4, 33.77 tall: 0.66 DERIVED), bushings with housings 2 x 0.2. W = 24.25 kg, 237.89 N; per screw static 79.30 N, capture lift 113.31 N (DERIVED).
2. **S2 r5 does not read `jackscrew.length` or `jackscrew.lead`.** keys_read (MEASURED): S1 r7 reads both; S2 r5 reads neither. A lead change moves S1 only; a length change reaches S2 only through `top_guide_z` and the member lengths.
3. **K = 2 for a floating nut is wrong on a top-guided screw.** K = 2 is fixed-free: it needs a free screw top. The top guide holds the screw top radially (DN23, Design Notes 1). With a floating nut the column is the whole screw between the anchor bearing line and the guide bearing line, L_t = 870 (280 to 1150, DERIVED), loaded in compression over its lower part (815.84 at park). Compressing the whole span is the worse case, so P_cr >= pi² E I / (K L_t)² with K 1.0 (pinned anchor) or 0.7 (fixed anchor). At the O3 inputs (d_r 6.2, E 200): 189.2 N (K 1), 386.0 N (K 0.7), against O3's 55.8 N at K 2 (DERIVED). Design Notes 11 ("floating nuts drop S3-2 to K = 2") and the S3-2 row (l.285) carry the same error.
4. **Root 6.2 is a Tr8x1.5 root.** The T8 lead-8 screw is 4-start at pitch 2; ISO 2904 form d3 = d - 2(0.5 P + a_c) = 8 - 2(1.25) = 5.5 (DERIVED; vendor screws measure 5.5 to 6.0). I drops from 72.53 to 44.92 mm⁴ (-38 percent).
5. **Segment length from the bearing line, not the block top.** The anchor bearing sits mid-block (280), so the rigid-nut segment at park is 1095.84 - 280 = 815.84 (O3: 800.84 to the block top 295). DERIVED.
6. **The overlay lift cannot drive the 1000 N cut.** Cut case: the screws push the ring down with 1000 - W = 762.11 N, 254.04 per screw (DERIVED). At lead 8 that needs 0.489 to 0.549 N m per motor (eta 0.661 to 0.589, mu 0.15 to 0.20) against `liftmotor.holding_torque` 0.45. The largest WOB at holding torque (stall + W) is 874.07 N at the overlay eta 0.6 (862.4 to 938.7 over the mu range). DERIVED. Detail 1.3's cut case is unreachable on the overlay values; this is a Q8 (powered feed) finding as well as a load case.
7. **The round r 21 anchor block cannot carry a NEMA 17.** The NEMA 17 face pattern is 31 mm square (M3): its corners lie at r 21.92 from the motor axis, outside the r 21 block (DERIVED). A functional FAIL under 8.4a (T2-b, LF1.1-9).
8. **At x = 0 the base plate does not reach the rails.** `base.column_notch` removes the plate for |y| > 239 at |x| <= 35; the rails start at |y| 244. In the section the plate piece spans u -239 to 239 and sits 5 inboard of each rail (DERIVED). The plate-to-frame contact lies off the plane (rails beyond the notch, end members, supports), so base_plate|base_frame is certified by S1 r7 only, not by S3.
9. **Retract-with-bind compression is capped by the stall.** The motors cannot push harder than F_stall, so compression per screw is min((W + F_bind)/3, F_stall/3) for any F_bind.
10. O3 reproduced with the Manager's inputs: P_cr 223.2 N (K 1), 55.8 N (K 2); per screw 65.89 / 99.90 / 212.06 N; ratios 3.39, 2.23, 1.05 and 0.85, 0.56, 0.26 (DERIVED). O7, O11, O12 confirmed as written.

## 1. Functional completeness (8.4a), S3 parts

| # | Feature | Keys | Result | Missing leaf, proposed value (status) |
|---|---|---|---|---|
| 1 | Anchor block with thrust bearing | `jackscrew.anchor_z`, `.anchor_allowance` 30; plan r 21 from `.nut_flange_od` by declaration | **FAIL** | no bearing leaves; r 21 cannot take the NEMA 17 (Correction 7). `jackscrew.anchor_block_width` 42 square, faces radial and tangential; `jackscrew.anchor_bearing` "fixed end: two 7000-class angular-contact bearings 10 x 26 x 8 back-to-back, M10x1 locknut, journal 10"; stack 16 + 6 + shoulders 8 = 30 = anchor_allowance (ASSUMED) |
| 2 | Screw | `jackscrew.nominal` 8, `.root_diameter` 6.2, `.lead` 8, `.length` 900, `.efficiency` 0.6 | **FAIL** | root does not match the thread (Correction 4); no starts, pitch, E, density, friction. Section 4 option: Tr12x3, root 8.5 (ISO 2904), starts 1; `jackscrew.youngs_modulus` 200000 N/mm², `.density` 7850 kg/m³, `.thread_mu` [0.15, 0.20] (ASSUMED) |
| 3 | Brass nut and housing, rigid mounting | `jackscrew.nut_length` 30, `.nut_flange_od` 42, `ring.nut_housing_od` 50, `.nut_housing_height` 30 | PASS | none (flange bolted to the housing) |
| 4 | Floating nut mounting | `ring.nut_mounting` text only | **FAIL** | `ring.nut_float` 0.5 radial; axial: flange clamped between the housing shoulder and a retaining ring, no axial play; anti-rotation: one pin through the flange into the housing (ASSUMED) |
| 5 | Top guide block | `jackscrew.top_guide_z`, `.guide_allowance` 30; r 21 by declaration | **FAIL** | no bearing leaf. `jackscrew.guide_bearing` "one 6000-2RS 10 x 26 x 8 radial, journal 10 axially free (no shoulder), radial support only"; block D42 x 30 unchanged (`jackscrew.guide_block_od` 42, ASSUMED) |
| 6 | Anchor and guide bracket arms | `frame_upper.radius`, `profile.width`, `jackscrew.pitch_radius` | PASS | none (r_in expression changes with row 1, value 181 unchanged) |
| 7 | Frame member c and its foot | `frame_upper.member_length_rail` 1225, `.foot` | PASS | none |
| 8 | Base plate and base frame in section | params `base.*`, `frame.*`, `icd.footprint_*` | PASS | none |
| 9 | NEMA 17 body, length, shaft, mount | `liftmotor.body` 42, `.length` 48, `.position`, `.plan_rot` | **FAIL** | `liftmotor.shaft_od` 5, `.shaft_length` 24, `.pilot` [22, 2], `.bolt_pattern` 31 (M3); mount: four M3 hex standoffs 25 long (= `coupling_length`) from the block underside (ASSUMED; NEMA 17 frame figures, no source on file) |
| 10 | Coupling | `liftmotor.coupling_length` 25 (the gap) | **FAIL** | `liftmotor.coupling` "beam coupling OD 19 x 20, bores 5 and 8, 1.5 clear of the pilot top (242) and the block underside (265)"; screw end journal 8, 10 engaged (ASSUMED) |
| 11 | Power-off hold device | `hold.device` "open" | **FAIL** | per section 4: self-locking lead (with Tr12x3) or brake on each NEMA 17 (`liftmotor.length` 78 with brake) or park pin |
| 12 | Load-case inputs | `loads.axial_design`, overlay masses | **FAIL** | F_bind, SF, E, rapid traverse, thread friction, bearing/pinion/hub/bushing masses (section 8) |
| 13 | Sync parts | none | **FAIL** | `liftsync.method` "one controller, three drivers, home switch per screw at park"; `liftsync.home_switch` "micro switch body 13 tall x 20 radial x 6, under the top-guide arm at r 190 to 210, z 1122 to 1135, roller lever on the nut-housing top at park" (ASSUMED) |
| 14 | Descent-stop pad and post | `frame_upper.stop_pad_*` | PASS | not in the plane (theta 150, x -173 to -186, beyond the 60 band): omitted, listed in the note |
| 15 | Ring and nut housing c in section | `ring.*` | PASS | none |
| 16 | Drill-to-ring bearing in section | `bearing.*` | PASS | mass in row 12 |
| 17 | Pinion c, NEMA 23 c, mount, shaft (theta 90, in the plane) | `pinion.*`, `ring.motor_mount_height` | PASS | none |
| 18 | Kept base stack on the axis (receiver, collet, core seat, holder, collar, wing nut, core 750) | S1 rows | PASS | holder stays an S4 stand-in |

PASS 9, FAIL 9.

## 2. Section plane and convention (screw c, theta 270)

**Plane.** The YZ plane x = 0, through the drill axis and screw c at (0, -160). Section A-A.

**Look direction.** Seen from +X, looking toward -X. Figure +u = +Y (right), +z up, plotted in z_S. (u, z, toward viewer) = (+Y, +Z, +X), right-handed: Y x Z = X. u equals the plan y coordinate, so plan values read with no sign change. Screw c, member c and the -Y rail sit on the left (u -304 to -135); pinion c and NEMA 23 c (theta 90) and the operator side on the right (u +95 to +218). K8 handedness predicates: screw c centre u = -160 < 0; NEMA 23 c centre u > 0.

**Pose.** capture_end (tip 184.84): cut case at the end of the cut, loop closed, ring low beside the anchors (ring 314.84 to 326.84, nut c centre 320.84, housing 305.84 to 335.84). Nut-centre stations at start (970.84) and park (1095.84) as dash-dot phantoms (kind line), with the S3-2 segment (park) and L_t span (280 to 1150) dimensioned.

**Three classes.**
- Cut (hatched where sectioned): base frame -Y and +Y rails (cut across, 60 x 60 at u ±244 to ±304, z -60 to 0); base plate (u -239 to 239 less the spigot hole ±80.2, z 0 to 12); receiver, collet, core seat, holder, collar, wing nut (sweep reference as in S1), core 750; drill head, tube, top block; keep-out lines u ±86.2 (reference); ring with nut housing c; drill-to-ring bearing; gear, gear hub; pinion c, motor mount c, NEMA 23 c, motor shaft c; member c (cut lengthwise at its centre, u -304 to -244, z 0 to 1225); bracket arms c (u -244 to -181); anchor block c and its bearings; guide block c and its bearing; screw c; nut c; NEMA 17 c (cut through its axis); coupling c; home switch c.
- Unsectioned although cut (ASME Y14.3 convention for parts whose axis lies in the plane): screw c, NEMA 17 shaft, NEMA 23 shaft, coupling, standoffs, anti-rotation pin, balls (drawn as circles). Drawn as outline over the hatch of the part around them.
- Beyond the plane within one profile width (0 > x >= -60, `profile.width`): drawn in elevation, visible edges solid, edges behind a cut part dashed (renderer section convention, P4). In the band: the two rear NEMA 17 standoffs (x -15.5, u -175.5 and -144.5). A cut row draws its section only; its far half is not drawn again.
- Beyond past 60 and in front (x > 0): omitted, listed in the figure note. Beyond: screw a set (x -138.6: screw, nut, housing, anchor, guide, arms, lift motor, member a), pinion a and NEMA 23 a (theta 210), guide rod at 180 and its lug, bushing and tie b, descent-stop pad and post (theta 150), base-frame end member and plate support at x -232, -112. Front: screw b set (x +138.6), pinion b and NEMA 23 b (theta 330), guide rod at 0 and tie a, end member and support at x +232, +112.

**Hatch.** One pattern per material, legend in the note: aluminium (ring, blocks, plate, receiver, holder), 30-6060 extrusion (members, arms, rails: square outline with the centre-bore lines), steel (bearing races, drill tube), brass (nut), plastic (collet). Hidden lines inside a cut part are not drawn.

**Ring at screw c.** One body in section: ring plate pieces stop at the housing outline (u -185 and -135); the housing pieces carry the boss above and below the plate and the nut bore (nut body + 2 x 0.5 float). Pair ring|nut_housing_c is C between two section rows (K7 refuses N there).

**Inset (end view).** plan_xy seen from +Z, +X right, +Y up (as S2), x and y -340 to 340, square, upper right of the figure, at least 0.3 of the figure height. Shows: screws a, b, c (circles d `jackscrew.nominal`), nut housings (circle d 50), anchor blocks (42 squares, faces radial), lift motors (42 squares, dashed under the blocks), members a, b, c (60 squares), home switches (three), the controller callout with leaders to the three lift motors ("one controller, three drivers, home switch per screw"), keep-out circle r 86.2, ring OD circle r 210 as a dashed reference (kind line, covers nothing), cutting-plane line A-A on x = 0 with arrows pointing toward -X, +X/+Y arrows and the theta arc. No operator-sector edge: the recommended sync crosses nothing. The inset is its own Axes: TP-7 per-Axes checks apply (K5 circles admitted there only, K8 handedness: screws at 30, 150, 270 counter-clockwise).

## 3. Block and motor-mount values (T2-b, LF1.1-9 to -11) with S1/S2 consequences

| Item | Proposed (ASSUMED) | Key | S1 r7 / S2 r5 effect |
|---|---|---|---|
| Anchor block plan | 42 square, faces radial and tangential (= `liftmotor.plan_rot` 0), radial footprint r 139 to 181, half-width 21; outer face bolted to the arm end face at r 181 | new `jackscrew.anchor_block_width` 42 | No key S1/S2 read moves. Spec rows anchor_a/_b (S1), anchor_a/_b/_c (S2) change place from round r 21 to radial; bracket r_in becomes `pitch_radius + anchor_block_width / 2` = 181 (value unchanged). Drawn change: S1 side projected half-width 21 to 28.69 at theta 30, 150 (21 (|cos| + |sin|), DERIVED); S2 circle to square. Opens S1 r8 and joins S2 r6. Margins: S1-4 0.84 unchanged (z only); S2-5a least stays 11.71 (block square least to the sector edge 15.69, DERIVED, equals the drawn motor square); anchor|bracket becomes face contact (plan-contact on true sections); post|block plan gap 19 unchanged (LF1.1-11) |
| Anchor block height | 30 | `jackscrew.anchor_allowance` 30 unchanged | none |
| Anchor bearings | two 7000-class 10 x 26 x 8 back-to-back, M10x1 locknut, journal 10; bearing line 280 (block mid) | new `jackscrew.anchor_bearing`; new `jackscrew.anchor_bearing_z` expr `anchor_z + anchor_allowance / 2` 280 (DERIVED) | none |
| Guide block | D42 x 30 round, one 6000-2RS radial, journal axially free; bearing line 1150 | new `jackscrew.guide_block_od` 42 (spec expression change, value equal); `jackscrew.guide_bearing_z` expr `top_guide_z - guide_allowance / 2` 1150 | spec text only if adopted in S1/S2 guide rows; no drawn change |
| Motor mount | NEMA 17 face up, four M3 hex standoffs 25 on the 31 pattern from the block underside; motor 192 to 240 | `liftmotor.coupling_length` 25 unchanged (meaning stated: motor face to block underside); new `liftmotor.bolt_pattern` 31, `.pilot` [22, 2] | none. LF1.1-10 closes: the motor hangs under its block (r 139 to 181), not under the arm |
| Coupling | beam OD 19 x 20, z 243.5 to 263.5, bores 5 / 8 | new `liftmotor.coupling` | none |
| Screw ends | journal 10 through both bearing sets, 8 into the coupling (10 engaged); the 900 bar spans 255 to 1155 | none | none: screw z_rule (anchor_z to top_guide_z) stays the envelope |
| Lift motor | 42 x 48, shaft 5 x 24 | `liftmotor.body`, `.length` unchanged; new `.shaft_od`, `.shaft_length` | none (with the brake option, section 4, `.length` 48 to 78) |
| Home switch | micro switch under the top-guide arm, r 190 to 210, z 1122 to 1135 | new `liftsync.home_switch` | none (S2 does not draw switches; theta 30/150 switches lie outside the sector, max 31.4 deg) |

Moved S1/S2 keys from this section: none. Spec and drawn changes: anchor rows in S1 and S2 (opens S1 r8). Member tops 1225, L 900, top_guide_z 1165 and S1-4 0.84 unchanged.

## 4. Options and recommendations

**Screw (decides S3-2, the hold and the WOB together).**

| Screw | lambda / phi (mu 0.15 to 0.20) | eta | F_stall per screw (mu 0.15 / 0.20) | Max WOB at holding torque | Back-drive | S1/S2 keys moved |
|---|---|---|---|---|---|---|
| T8x8, 4-start (overlay) | 19.99 / 8.83 to 11.70 | 0.661 to 0.589 | 233.6 / 208.2 | 938.7 / 862.4 (874.07 at eta 0.6) | yes | none |
| T8x2, 1-start | 5.20 / same | 0.364 to 0.299 | 514.6 / 422.7 | 1781.7 / 1506.0 | no | lead (S1) |
| Tr10x2 | 4.05 / same | 0.310 to 0.251 | 438.3 / 354.8 | 1552.6 / 1302.4 | no | nominal (S1, S2), lead (S1) |
| **Tr12x3, 1-start** | 5.20 / same | 0.364 to 0.299 | 343.1 / 281.8 | 1267.1 / 1083.3 | no | nominal 8 to 12 (S1, S2), lead 8 to 3 (S1) |

All DERIVED, T 0.45 N m, W 237.89 N. Recommend **Tr12x3 single start** (DN23's named fallback): the only row that passes S3-2 at SF 3 in every case (section 5), reaches 1000 N WOB across the friction range, and holds with power off. Cost: S1 r8 (screw width 8 to 12, label "Tr12x3", lead ticks 3) and S2 r6 (screw circle d 12); no margin moves (S1-4, L, member tops, S2-5a: screw at theta 30 is 35.4 from the 45 deg edge, DERIVED); rapid 25 mm/s needs 500 rpm (critical speed section 5); lift torque for the 1000 N cut 0.333 to 0.406 N m against 0.45 (margin 1.11 to 1.35 at low speed). Nut flange OD 42 and length 30 kept ASSUMED until vendor data.

**Nut mounting.** Rigid: flange bolted; segment nut to anchor, K 0.5 (nut held in rotation by the ring) to 1.0; three rigid nuts on three top-guided screws plus two guide rods overconstrain the ring (Design Notes 11). Floating: radial float 0.5, axially clamped, pin anti-rotation; the rods guide the ring; S3-2 over the anchor-to-guide span L_t 870, K 0.7 with the fixed anchor (Correction 3). **Recommend floating.** `ring.nut_mounting` is read by neither accepted record.

**Hold device.** (a) Self-locking lead: no added part; Tr12x3 lambda 5.20 < phi 8.83 (back-drive efficiency negative); can creep under vibration; state not visible. (b) Brake on each NEMA 17: works with the back-driving T8x8; back-drive torque to hold per screw 0.055 N m (79.30 N x 8 x 0.542 / 2 pi, DERIVED), small brake; `liftmotor.length` 48 to about 78 (S1, S2 key; motor 162 to 240). (c) Park pin with visible state: holds at park only; mid-stroke power loss drops the ring onto the one descent pad at theta 150. **Recommend (a) with Tr12x3**, drawn as a callout on screw c; (b) if Sean keeps T8x8. A visible hold state at load is a Step 2 row (section 10).

**Sync.** Belt enclosing the axis: the 30-to-150 strand runs at y = 80 + rho inside the operator sector (S2-5a red), 80 + rho from the axis against the cutter, at knee height (O7 confirmed). Belt not enclosing the axis: serpentine with idlers around screw c, strands near member c and the anchor arms; the pulleys need a free screw zone, and the only free zone below the nut-housing sweep is the coupling gap, so anchor_z or coupling_length moves (S1-4, L, top_guide_z, member tops). Single controller with three drivers and a home switch per screw at park: no parts in the sector, step loss re-levelled at each park homing. **Recommend single controller with home switches**: the inset shows the callout and three switches, K9 sees them.

**Anchoring.** Anchor: fixed end, two angular-contact bearings back-to-back (catalogue "fixed" support; credits K 0.7); thrust washers plus one radial bearing read as pinned (K 1.0); a set-screw pillow-block insert is rejected (axial hold by set screws on a thread). Top guide: one radial bearing, journal free axially (DN23 "guided only at the top"); no top guide is rejected (K 2). **Recommend fixed anchor, radial top guide.**

## 5. S3-2 inputs, preview and options

Inputs (ASSUMED unless stated): E 200 GPa; SF 3 (Sean); d_r 8.5 (Tr12x3) / 5.5 (T8x8) / 6.2 (overlay); K per mounting (section 4); rigid segment a = 1095.84 - 280 = 815.84; floating span L_t = 1150 - 280 = 870 (DERIVED); compression per screw: static 79.30, capture lift 113.31, retract with bind 179.30 (F_bind 300), stall up 343.1 (Tr12x3) / 233.6 (T8x8, mu 0.15).

| Screw, mounting, K, L | P_cr (N) | static | capture | retract | stall |
|---|---|---|---|---|---|
| T8x8 d_r 5.5, floating, K 0.7, 870 | 239.1 | 3.01 | 2.11 | 1.33 | 1.02 |
| T8x8 d_r 5.5, rigid, K 0.5, 815.84 | 532.8 | 6.72 | 4.70 | 2.97 | 2.28 |
| T8x8 d_r 6.2, rigid, K 0.5, 815.84 | 860.4 | 10.85 | 7.59 | 4.80 | 3.68 |
| Tr12x3, floating, K 1.0, 870 | 668.2 | 8.43 | 5.90 | 3.73 | 1.95 |
| **Tr12x3, floating, K 0.7, 870** | **1363.8** | **17.20** | **12.04** | **7.61** | **3.98** |
| Tr12x3, rigid, K 0.5, 815.84 | 3039.7 | 38.33 | 26.83 | 16.95 | 8.86 |

DERIVED. Two-screw share (Tr12x3 floating K 0.7): static 11.47, capture 8.02, retract 5.07.

Options for Sean:
- (i) **Change the screw now to Tr12x3** (recommended). S3-2 passes SF 3 in every case at K 0.7 (least 3.98, stall up); at K 1.0 the stall reads 1.95, so the K 0.7 credit rests on the back-to-back anchor pair. Opens S1 r8; S2 r6 is open at P1R.
- (ii) Keep T8x8, keep the threshold and its controls; `--accept` admits a content red only with a Design Notes reference to the Step 2 screw-size row (harness change at (c)). S3-2 reads red at capture (2.11) and stall (1.02) floating; the WOB shortfall (874 N) and the back-drive stay open.
- (iii) Make S3-2 a reported value (P_cr margin per case and K, no threshold): a relaxed rule; under detail 1 common (h) it needs a premise check with Z and B (for example: the summary RPT row carries every case and K). Loses the guard.
- (iv) Pre-tensioned screw, thrust at both ends, preload above the largest compression share: removes buckling; contradicts DN23 "guided only at the top" (Quinn's decision). Not recommended now.

Critical speed (span L_t 870, d_r, E 200, 7850): Tr12x3 1336 rpm pinned-pinned, 2086 fixed-pinned, against 500 rpm at rapid 25 mm/s (2.67 at pinned); T8x8 864 / 1350 rpm against 187.5 rpm (4.61). DERIVED.

## 6. Load-case table (per screw = load / 3; two-screw = load / 2; Tr12x3, eta 0.364 to 0.299)

| Case | Total on the screws | Per screw | Two-screw | Segment below the nut | Kept parts (collet, holder, receiver, base plate) |
|---|---|---|---|---|---|
| Static W 24.25 kg (ring 6, drill 8, gear 3, NEMA 23 3 x 1.0, nuts 0.15, bearing 1.5, pinions 1.5, hub 0.7, bushings 0.4) | 237.89 down | 79.30 | 118.95 | compression | 0 |
| Capture lift W + 0.5 m core 10.4 kg | 339.92 | 113.31 | 169.96 | compression | 0 |
| Retract with bind, F_bind 300 (Sean) | 537.89 | 179.30 (cap 343.1) | 268.95 | compression | 0 |
| Cut 1000 N up on the cutter (`loads.axial_design`) | 762.11 (1000 - W) | 254.04 | 381.05 | tension (stress 4.48 MPa per screw on 56.75 mm²) | 1000 compression; plate also takes 508.07 up at members a, b; member c's 254.04 goes to the -Y rail |
| Stall down into a jam through the cutter | 1029.2 / 845.4 (F_stall) | 343.1 / 281.8 | (each motor its own) | tension | F_stall + W = 1267.1 / 1083.3 (T8x8: 874.07 at eta 0.6) |
| Stall up at the top of travel | F_stall | 343.1 / 281.8 | | compression (S3-2) | 0 |

All DERIVED from ASSUMED inputs. Rapid traverse 25 mm/s (ASSUMED) for critical speed; thread mu 0.15 to 0.20 (ASSUMED) for back-drive. Lift torque per screw: capture lift 0.181 N m (eta 0.299) at rapid; cut 0.333 to 0.406 N m. A stall-down jam on the descent pad loads the pad, not the kept parts. N5 consequence: with Tr12x3 the kept parts can see 1267 N in a crash, above the 1000 N Quinn is asked to accept.

## 7. Shape notes (8.4b)

| Row | Shape |
|---|---|
| screw_c | "Tr12x3 lead screw, unsectioned: rectangle 12 wide, thread ticks at the lead 3, journal 10 in both bearing sets, 8 into the coupling; label 'Tr12x3 screw L 900, lead 3'" |
| nut_c | "brass flange nut hatched either side of the screw: body and flange step, flange up at the ring face, 0.5 radial float gap to the housing bore, anti-rotation pin through the flange (pin unsectioned)" |
| nut_housing_c | "ring boss D50 x 30 at the screw, hatched with the ring, bore over the nut body plus float, retaining ring under the flange" |
| ring | "ring plate 12 in section either side of the clearance bore, nut-housing boss at u -160, NEMA 23 c mount on the top face at u +142 to +218" |
| anchor_c | "anchor block 42 square x 30 hatched, bore with two angular-contact bearings back-to-back (rows anchor_bearing_c), locknut above, outer face on the arm end at r 181" |
| anchor_bearing_c | "two angular-contact bearings 10 x 26 x 8: races hatched, balls as circles, contact lines converging outward (back-to-back)" |
| guide_c | "top-guide block D42 x 30 hatched, one radial bearing (row guide_bearing_c), journal through with no shoulder: radial only" |
| guide_bearing_c | "deep-groove radial bearing 10 x 26 x 8: races hatched, ball circles" |
| bracket_anchor_c, bracket_guide_c | "30-6060 stub cut lengthwise, extrusion hatch, r 181 to 244 at the block heights" |
| frame_upper_c | "30-6060 member cut lengthwise at its centre, 60 wide, on the -Y rail top z_A 0 to 1225, extrusion hatch" |
| base_frame | "-Y and +Y rails cut across: 60 x 60 extrusion sections with slot notches, under the plate edges, 5 outboard of the notch edges" |
| base_plate | "plate cut, 12 thick, u -239 to 239 (notches at x = 0), spigot hole gap ±80.2" |
| liftmotor_c | "NEMA 17 cut through its axis: body 42 x 48, pilot 22 x 2 on the top face, shaft 5 x 24 unsectioned up into the coupling" |
| coupling_c | "beam coupling OD 19 x 20, unsectioned, slots drawn, clamping the motor shaft and the screw end" |
| standoffs_c | "two rear M3 x 25 hex standoffs in elevation (beyond, x -15.5) from the motor face to the block underside" |
| home_switch_c | "micro switch under the top-guide arm, roller lever drawn down to the nut-housing top at park" |
| hold_callout | "callout on screw c: 'power-off hold: self-locking Tr12x3, lambda 5.2 < phi 8.8'" |
| load arrows | "cut: 1000 N up at the cutter; T arrows on the screw below the nut, 254 per screw; compression: down arrows on housing c labelled static 79, capture 113, stall 343" |
| nut stations | "dash-dot nut-centre ticks at start 970.84 and park 1095.84 z_A; S3-2 span 280 to 1150 dimensioned" |
| drill, bearing, gear, hub, pinion c, NEMA 23 c, kept base stack, core 750 | S1/S2 shapes, true half-sections on both sides of the axis |
| inset rows | screws, housings, blocks, motors, members, switches, controller callout, keep-out, ring reference, A-A line (section 2) |

## 8. Overlay value table

| Key | Old | New | Unit | Source | Status | Read by S1 r7 / S2 r5 |
|---|---|---|---|---|---|---|
| jackscrew.nominal | 8 | 12 | mm | Tr12x3, DN23 fallback; Sean STOP S3-A | ASSUMED (was DECLARED [DN23]) | yes / yes |
| jackscrew.lead | 8 | 3 | mm | Tr12x3 single start | ASSUMED | yes / no |
| jackscrew.root_diameter | 6.2 | 8.5 | mm | ISO 2904 Tr12x3 d3; vendor (Sean) | ASSUMED | no / no |
| jackscrew.efficiency | 0.6 | 0.33 (0.299 to 0.364) | | lambda 5.20, mu 0.15 to 0.20 | DERIVED from ASSUMED mu | no / no |
| jackscrew.starts | | 1 | | Tr12x3 | ASSUMED | no / no |
| jackscrew.thread_mu | | [0.15, 0.20] | | brass on steel, lubricated; no source | ASSUMED | no / no |
| jackscrew.youngs_modulus | | 200000 | N/mm² | steel 193 to 210 | ASSUMED | no / no |
| jackscrew.density | | 7850 | kg/m³ | steel | ASSUMED | no / no |
| jackscrew.anchor_block_width | | 42 | mm | section 3 | ASSUMED | no (spec rows change) |
| jackscrew.anchor_bearing | | "two 7000-class 10x26x8 back-to-back, locknut M10x1" | | section 3 | ASSUMED | no / no |
| jackscrew.anchor_bearing_z | | 280, expr `jackscrew.anchor_z + jackscrew.anchor_allowance / 2` | mm | section 3 | DERIVED | no / no |
| jackscrew.guide_block_od | | 42 | mm | equals the r 21 declaration | ASSUMED | no / no |
| jackscrew.guide_bearing | | "6000-2RS 10x26x8, journal axially free" | | section 3 | ASSUMED | no / no |
| jackscrew.guide_bearing_z | | 1150, expr `jackscrew.top_guide_z - jackscrew.guide_allowance / 2` | mm | section 3 | DERIVED | no / no |
| jackscrew.end_factor | | {rigid: 0.5 on nut-to-anchor, floating: 0.7 on anchor-to-guide} | | section 5 | ASSUMED | no / no |
| jackscrew.buckling_sf | | 3 | | detail 1.3; Sean | ASSUMED | no / no |
| ring.nut_mounting | "rigid (K 1.0) ..." | "floating: 0.5 radial, axially clamped, pin anti-rotation (K 0.7 over the anchor-to-guide span)" | | section 4 | ASSUMED | no / no |
| ring.nut_float | | 0.5 | mm | section 1 row 4 | ASSUMED | no / no |
| liftmotor.shaft_od, .shaft_length | | 5, 24 | mm | NEMA 17 frame | ASSUMED | no / no |
| liftmotor.pilot | | [22, 2] | mm | NEMA 17 frame | ASSUMED | no / no |
| liftmotor.bolt_pattern | | 31 (M3) | mm | NEMA 17 frame | ASSUMED | no / no |
| liftmotor.coupling | | "beam OD 19 x 20, bores 5 / 8" | | section 3 | ASSUMED | no / no |
| liftmotor.coupling_length | 25 | 25 (meaning: motor face to block underside, = standoff length) | mm | unchanged | ASSUMED | yes / yes (value unchanged) |
| liftmotor.mass | | 0.35 | kg | each, fixed | ASSUMED | no / no |
| hold.device | "open: ..." | "self-locking Tr12x3 lead (drawn); options brake, park pin; Step 2 decides" | | section 4 | ASSUMED | no / no |
| liftsync.method | | "one controller, three drivers, home switch per screw at park" | | section 4 | ASSUMED | no / no |
| liftsync.home_switch | | "micro switch r 190 to 210, z 1122 to 1135, under the top-guide arm" | | section 1 row 13 | ASSUMED | no / no |
| liftload.f_bind | | 300 | N | retract bind; Sean owns | ASSUMED | no / no |
| liftload.rapid_speed | | 25 | mm/s | stroke 775 in 31 s | ASSUMED | no / no |
| bearing.mass | | 1.5 | kg | no source | ASSUMED | no / no |
| pinion.mass | | 0.5 | kg | each; no source | ASSUMED | no / no |
| gear.hub_mass | | 0.7 | kg | 0.66 DERIVED (aluminium clamp ring) | ASSUMED | no / no |
| guide.bushing_mass | | 0.2 | kg | each with housing; no source | ASSUMED | no / no |

Fallback if Sean keeps T8x8: root_diameter 6.2 to 5.5, efficiency 0.6 kept, hold.device brake, `liftmotor.length` 48 to 78 (S1, S2 key; brake) or a NEMA 17 of 0.65 N m holding torque (`liftmotor.length` about 60) for the WOB.

## 9. g_min for the S3 K7 pairs

| Pair | Class | g_min | Source | Value |
|---|---|---|---|---|
| nut_housing_c \| anchor_c (capture_end) | G | 10 | seed l.150 | 10.84 DERIVED |
| nut_housing_c \| guide_c (park) | G | 10 | seed l.150 | 24.16 |
| nut_housing_c \| home_switch_c (park) | G | 10 | seed l.150 | 11.16 |
| ring \| home_switch_c (park) | G | 10 | seed l.150 | 20.16 |
| ring \| bracket_anchor_c, anchor_c (capture_end) | G | 10 | seed l.150 | 19.84 |
| ring \| frame_upper_c | G | 10 | seed l.150 | 34.00 (plan, ring rim 210 to face 244) |
| moving parts \| keep-out | G | 0 | seed l.149 | as S2 |
| coupling_c \| liftmotor_c pilot, \| anchor_c underside | G | 1 | rotating in place; new, ASSUMED | 1.5 |
| nut_c \| nut_housing_c | C | 0 | axial clamp faces | float 0.5 radial inside |
| screw_c \| nut_c; screw_c \| anchor_bearing_c; anchor_bearing_c \| anchor_c; screw_c \| guide_bearing_c; guide_bearing_c \| guide_c | C | 0 | journal and thread contacts | |
| screw_c \| anchor_c, guide_c | F | | bore clears the journal | |
| ring \| nut_housing_c | C | 0 | one body (section 2) | |
| anchor_c \| bracket_anchor_c; guide_c \| bracket_guide_c; brackets \| frame_upper_c; frame_upper_c \| base_frame; home_switch_c \| bracket_guide_c; standoffs \| anchor_c, liftmotor_c; coupling \| screw_c, motor shaft | C | 0 | bolted or clamped | |

No belt is drawn, so no belt pairs.

## 10. Operator-task rows (S3; z_S)

| Task | Pose | Sketch | Reach height and stance | Sightline | Hazard | Check or rubric |
|---|---|---|---|---|---|---|
| Load a core under the parked ring held by the power-off hold | load | S3 | as the S1/S2 load row | ring and housings visible from the sector; the hold state is not visible (self-locking lead) | ring assembly 24.25 kg plus drill overhead at 1136.84 to 1275.84 on the lead alone; homing moves the ring up to the switches while the operator may be under it: interlock and a visible hold state (park pin flag or enable lamp) to Step 2 | V10 |
| Change a collet beside the lift motors and couplings | load | S3 | kneel in the sector, hands at r <= 115, knee height | couplings at screws a, b in view at the sector edges | couplings (r 150.5 to 169.5, z_S 303.5 to 323.5) 35.5 radially from the hand zone, exposed between the standoffs; the lift is idle at load; coupling guard sleeve to Step 2 | V10 |

S3 rubric applicability gains V10: S3 V1, V5 to V10.

## 11. S3-3 chains (cut case)

| Pair | Screw a (150) | Screw b (30) | Screw c (270) |
|---|---|---|---|
| cutter \| core ... receiver \| base_plate | S1 r7 K7 C | S1 r7 | S1 r7; S3 draws them on the axis too |
| base_plate \| base_frame | S1 r7 | S1 r7 | S1 r7 (not at x = 0, Correction 8) |
| base_plate \| frame_upper_k | S1 r7 (side), S2 r5 (plan) | S1 r7, S2 r5 | n/a |
| base_frame \| frame_upper_c | n/a | n/a | S3 (section), S2 r5 (plan z-contact) |
| frame_upper_k \| bracket_anchor_k | S1 r7, S2 r5 | S1 r7, S2 r5 | S3, S2 r5 |
| bracket_anchor_k \| anchor_k | S1 r7, S2 r5 | S1 r7, S2 r5 | S3, S2 r5 |
| anchor_k \| anchor_bearing_k \| screw_k | S3 by symmetry (premise below) | S3 by symmetry | S3 |
| screw_k \| nut_k \| nut_housing_k \| ring | S3 by symmetry | S3 by symmetry | S3 |
| ring \| bearing | S1 r7 (declared C), S3 | same | S3 |
| bearing \| drill_tube \| drill_head (cutter) | declared at S3, drawn at S6 (S6-5) | same | same |

Chain order screw c: cutter, core, core seat, collet, holder, receiver, base plate, base frame, frame_upper_c, bracket_anchor_c, anchor_c, anchor_bearing_c, screw_c (tension), nut_c, nut_housing_c, ring, bearing, drill tube, cutter. Screws a, b: base plate to frame_upper_k directly. S1 declares anchor|screw as N, so S1 cannot certify the screw-set pairs for a and b; S3 certifies them on screw c. Premise for "by symmetry": the anchor, bearing, screw, nut and housing rows of a, b, c are equal in z_rule and place up to theta (a lint with Z and B, detail 1 common (h); Topologist 1.2 (c) NOTE 1 holds that radial symmetry is no predicate until such a check exists).

## 12. Reported items (`reported_items`)

| id | text | needs_drawing |
|---|---|---|
| L_min | screw length L_min per Q9 option and at the drawn anchor, against DN23 800 to 900 (885.00 / 885.84 / 1135.00 unchanged) | false |
| n_crit | critical speed over L_t with the end factor stated, against rapid traverse | false |
| pcr_margin | P_cr / F per compression case (static, capture lift, retract with bind, stall up), per mounting and K, per screw and two-screw | false |
| f_stall | F_stall total and per screw, both directions, mu range | false |
| wob_max | largest WOB at holding torque (F_stall + W) against `loads.axial_design` 1000 | false |
| lift_torque | motor torque per screw for the cut and for capture lift, against `liftmotor.holding_torque` | false |
| kept_axial | axial force in collet, holder, receiver, base plate at 1000 N and at F_stall + W (N5) | false |
| backdrive | lead angle against friction angle, back-drive efficiency | false |
| screw_share | per-screw (load / 3) and two-screw (load / 2) force per case | false |
| tension_segment | screw length in tension below the nut per S1 pose in the cut case | true |

## 13. Items for Sean (STOP S3-A)

1. **Screw Tr12x3 single start** (section 4): `jackscrew.nominal` 8 to 12 (S1 r7, S2 r5 read it), `jackscrew.lead` 8 to 3 (S1 r7). Rows that move: S1 screw_a/_b width and label, S2 screw_a/_b/_c circles; margins unchanged. Opens S1 r8. Rule now (moves keys before (b)).
2. **S3-2 disposition**: (i) recommended; (ii), (iii), (iv) in section 5. Rule now.
3. **WOB finding**: T8x8 with the overlay NEMA 17 delivers at most 874 N (862 to 939) against the 1000 N cut; resolved by item 1 (1083 to 1267). Rule now with item 1.
4. **Anchor block 42 square** with the motor on standoffs (section 3): no key moves; S1/S2 anchor rows change (drawn change, S1 r8). Rule now.
5. Belt routing: not drawn (single controller recommended). Sync pick can wait for M2.
6. Lead change for the hold: part of item 1; hold pick can wait for M2.
7. Inputs Sean owns: SF 3 (and whether the stall fault case takes SF 3 or 2), F_bind 300 N. Rule now or accept as ASSUMED.
8. Inputs set without a source (accept ASSUMED or give a value): E 200 GPa, thread mu 0.15 to 0.20, rapid 25 mm/s, masses (bearing 1.5, pinions 0.5 each, hub 0.7, bushings 0.2 each), K credit 0.7 for the back-to-back anchor, bearing classes, coupling, switch.
9. N5 update: kept parts see up to 1267 N in a stall-down crash with Tr12x3. Goes to Quinn in batch 2.
10. Batch 2 draft (section 14): send or hold.
Can wait for M2: nut mounting (floating drawn), hold device (self-locking drawn), sync (controller drawn), anchoring type (fixed anchor, radial guide drawn).

## 14. Batch 2 draft

| ID | Question | Feeds | Owner | Value used until answered (ASSUMED) | Answer | Date |
|---|---|---|---|---|---|---|
| B2-1 | Which lead screw do you buy: thread (Tr12x3 or T8x8), root diameter, material, nut flange OD and length, machined ends? | S3-2, S1/S2 screw rows, Step 2 screw row | Sean | Tr12x3, root 8.5, steel E 200 GPa, flange 42, nut 30, ends 10 / 8 | | |
| B2-2 | Which NEMA 17 do you have (DN23-a): holding torque, body length, shaft, brake? | F_stall, WOB, lift motor rows | Sean | 0.45 N m, 48 long, shaft 5 x 24, no brake | | |
| B2-3 | What force can the cutter bind with on retract? | S3 retract case | Sean | F_bind 300 N | | |
| B2-4 | Safety factor on screw buckling, operating cases and the stall fault case | S3-2 | Sean | 3 for all cases | | |
| B2-5 | Rapid traverse speed for the lift | critical speed, cycle time | Sean | 25 mm/s | | |
| B2-6 | Masses of the drill-to-ring bearing, pinions, gear hub, guide bushings with housings | W, S3 load cases, S6 | Sean | 1.5, 0.5 each, 0.7, 0.2 each kg | | |
| B2-7 | N5 update: in a stall-down crash through the cutter the kept parts see up to 1267 N (Tr12x3), above 1000 N. Accept, or name a rating check or a current limit? | S3-3, Step 2, 4a | Quinn | accept at 1267 N with no rating check | | |
| B2-8 | Is a self-locking lead acceptable as the power-off hold while the operator loads under the ring, or must the hold state be visible (park pin)? | hold row, N7, Step 2 | Quinn and Sean | self-locking lead, no visible state | | |
| B2-9 | DN23 names T8 with TR10 or TR12 if a compression case is needed. Every lift puts the screw below the nut in compression. Do you agree to Tr12x3? | jackscrew.*, DN23 | Quinn | Tr12x3 | | |

N12 (NEMA 23 shaft rating) stays in the next batch as planned.

## 15. Echo sites S3 creates

| Value | Authority | Derived locations |
|---|---|---|
| Screw Tr12x3, nominal 12, lead 3 (on adoption) | overlay `jackscrew.nominal`, `.lead` | S1 screw rows and label, S2 screw circles, S3 screw row and callout, gameplan Design Notes 1 text, detail 1.3 l.270, Echo row "T8 screws" |
| Moving mass W 24.25 kg (237.89 N) | overlay masses | S3 load table and summary, S6, Step 2 tip-force row, S1 mass report (does not yet carry the four new masses) |
| F_stall 1029.2 / 845.4 N total; max WOB 1267.1 / 1083.3 N | overlay `liftmotor.holding_torque`, `jackscrew.lead`, `.thread_mu` | S3 summary, N5 (batch 2), Step 2 lift row |
| Bearing lines 280 and 1150, span L_t 870 | overlay `jackscrew.anchor_bearing_z`, `.guide_bearing_z` (expr) | S3-2, critical speed, S3 figure dimension |
| Anchor block 42 square | overlay `jackscrew.anchor_block_width` | S1 anchor_a/_b, S2 anchor_a/_b/_c, S3 anchor_c, bracket r_in expressions |
| Section A-A: plane x = 0, seen from +X, u = +Y | S3 spec view | S3 figure title, inset cutting-plane line, K8 section handedness |
| Home switch r 190 to 210, z 1122 to 1135 | overlay `liftsync.home_switch` | S3 section and inset; Step 2 sync row |

## 16. Gameplan lines to change

1. l.276. Old: "- Static: W down, W = ring + drill + gear + three NEMA 23 + nuts (overlay masses, ASSUMED until Q2 and DN23-d are answered)." New: "- Static: W down, W = ring + drill + gear + three NEMA 23 + nuts + drill-to-ring bearing + three pinions + gear hub + two guide bushings with housings (overlay masses, ASSUMED until Q2, DN23-d and batch 2 B2-6 are answered; 24.25 kg at the 1.3 (a) values, Designer 1.3 (a) Correction 1)."
2. l.278. Old: "- Retract with bind: W + F_bind (ASSUMED; Sean owns the value at Step 2)." New: "- Retract with bind: W + F_bind (ASSUMED; Sean owns the value at Step 2); compression per screw is capped at F_stall / 3, since the motors cannot push harder."
3. l.280. Old: "In the capture-lift and retract cases the screw segment below the nut is in compression; S3-2 covers them (The Software Engineer's estimate: margin 1.5 at K = 1 in capture lift, fail at K = 2)." New: "Every lifting case (static, capture lift, retract, stall up at the top of travel) puts the screw below the nut in compression; S3-2 covers them. With the overlay T8x8 the cut case cannot be driven: the largest WOB at holding torque is F_stall + W = 874 N (Designer 1.3 (a) Correction 6)."
4. l.285, within the S3-2 row. Old: "K from the nut mounting in the spec (1.0 rigid nut, nut and anchor both held laterally; 2.0 floating nut)" New: "K and length from the nut mounting in the spec (rigid nut: nut centre to the anchor bearing line, K 0.5 fixed-fixed, 1.0 conservative; floating nut with the top guide: anchor bearing line to guide bearing line L_t, K 0.7 with a fixed anchor, 1.0 pinned; K 2 applies only to a screw with no top guide; Designer 1.3 (a) Correction 3)"
5. l.536, within Design Notes 11. Old: "three rigid nuts on three top-guided screws overconstrain the ring, floating nuts drop S3-2 to K = 2." New: "three rigid nuts on three top-guided screws overconstrain the ring; floating nuts move S3-2 to the anchor-to-guide span with K 0.7 (fixed anchor) or 1.0, not K = 2, because the top guide holds the screw top (Designer 1.3 (a) Correction 3)."
6. l.188, within the line. Old: "S3 V1, V5 to V9" New: "S3 V1, V5 to V10"
7. Insert after l.186 (line text: "| Stand and watch during a cut | start to capture_end | S1, S2 | outside the frame at r 400, theta 60 (operator.watch_*), eye 1.6 m, standing | At start the cutter (894.84 to 1001.21) is in view under the ring. At capture_end the ring rim (r 210, underside 374.84) hides the cutter (244.84 to 351.21) from any eye above about 0.49 m at r 400 (0.58 m for the cutter rim r 88.9; S2 sightline_f6); a standing observer cannot see the end of the cut | The gear (r <= 126.32) and three pinions turn at drill.rpm 60, and the NEMA 23s (r <= 218) ride with them. The gear passes 1150.84 to 467.07 through the open operator sector, so a guard or interlock is needed (Step 2 row) | K7 swept case, V10 |"): the two rows of section 10 of this file, verbatim.
8. Insert after l.705 (line text: "| Axial design load **1000 N** | `loads.axial_design`; `loads.wob_max` | ASSUMED (design choice); wob_max VERIFIED |"): "| Moving mass **W 24.25 kg** (237.89 N; per screw 79.30) | overlay ring, drill, gear, pinion, bearing, jackscrew nut, guide bushing masses | ASSUMED (Designer 1.3 (a)); S3 load table |" and "| Largest WOB at holding torque **F_stall + W**: 874 N at T8x8 (overlay), 1083 to 1267 N at Tr12x3 | overlay liftmotor.holding_torque, jackscrew.lead, jackscrew.thread_mu | DERIVED (Designer 1.3 (a)); S3 reported wob_max |"
9. On Sean's adoption of Tr12x3 at STOP S3-A only: l.270 old "screw (rectangle, 8 mm nominal, lead labelled from `jackscrew.lead`)" new "screw (rectangle, `jackscrew.nominal` wide, lead labelled from `jackscrew.lead`; Tr12x3 from STOP S3-A)"; l.698 old "| T8 screws **800 to 900 mm** |" new "| Lead screws **800 to 900 mm** (Tr12x3 from STOP S3-A; DN23 named T8 with TR10/TR12 as the compression fallback) |" (rest of the row unchanged).
