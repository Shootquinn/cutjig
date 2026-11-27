# Step 1.4 (a) Designer params review, S4 side section through the base

## Corrections to the brief

1. **The kept receiver floor already has an 80 mm hole.** `receiver.floor_hole_dia` 80 (params, ASSUMED, "debris hole below the smallest core ledge ID 81.0 at d 85"); `build_parts/receiver.py` revolves the cup from (r_hole 40, z_bot) and (r_hole 40, 0), so the floor is an annulus r 40 to r 80 from z_A 0 to 40 (MEASURED from the profile points). A push rod of d <= 78 (G 1.0 radial) passes the floor and the collet core-seat ledge (ledge ID = d - 4: 86 at d 90, 96 at d 100, DERIVED from `collet_family.dims`). S4-2 as written ("the core's upward path from the core stop does not pass through receiver solid", B "receiver as built, floor present") is not red by construction: for a rod <= 78 it reads clean on the kept receiver, and for the core's own path it reads clean trivially (the core moves up, away from the floor). Its B fires only for a pusher wider than 80.
2. **S4-b holder figures are radii.** OD 134.08 (r 67.04), inner cone r 62.04 to r 56.75 over chain.H 30, bore r 56.75 (D 113.50), flange r 72.04 (D 144.08) (`holder.py dims()`, DERIVED). Gameplan Design Notes 25 row S4-b reads "OD 67.04"; item 1 of the last section corrects it.
3. **The receiver outer wall is r 80 only up to z_A 76.50.** `receiver.py`: spigot r 80 from z_A 0 to z_sh = 76.50 (z_R 36.5), runout land r 72.29 from 76.50 to 80.50, thread major r 74.79 from 80.50 to the rim 128.50 (DERIVED). S1 and S3 draw the wall r 67.29 to 80 to the rim; the wing nut bore (thread crest r 72.64) overlaps that stand-in wall. S4 draws the stepped wall.
4. **S1/S3 collar row includes the lift play.** S1/S3 `collar` z_min = collar_top - collar.top_above_plate = 153.09; `holder.py` fuses the collar ring at z_top 104.75 to 110.75 holder frame = z_A 153.84 to 159.84 (collar.thickness 6.0); 153.09 to 153.84 is the 0.75 lift play (nut.lift_play) between the nut plate top and the collar underside (DERIVED). The collar is one body with the holder.
5. **The collet grips the core over 23.20 mm, not its 32 mm height.** d 100 collet: straight bore from the core-seat top z_A 42.50 to the chamfer start z_A 65.70 (z_e = 32 - c, c = 6.30), DERIVED from `collet_family.dims` (r_top 58.50, r_b 51.0, min_wall 1.2). Any core motion above the seat greater than this loses the grip.
6. **Minimum slice under F4.** `core.min_exposed` 143.12 = kerf_standoff 106.369 + g_stop 25 + margin 5 + collar.top_above_plate 6.75: the core top must stand 5 above the kerf sphere centre with the drill at its stop. At the stop the tip is 184.84, the sphere centre 291.21 and the dome pole (sphere bottom, `drill.dome_pole_offset` 34.93) 219.77 z_A; the sphere (r `iris.face_radius_core` 71.4375) meets a d 100 core's surface at 240.19 (DERIVED). If F4 binds every slice, the least slice is 76.44 on the axis and 56.02 at the core surface. A coaster-thick slice (critical path 3.1) is not available under F4 as written. Batch 3 row B3-4 asks Quinn.

## 1. Section plane and look direction

| Feature | Azimuth / position | In plane x = 0 (section_yz)? | In plane y = 0 (section_xz)? |
|---|---|---|---|
| Receiver wall, floor annulus, register bore, spigot, shoulder (annuli) | round | yes | yes |
| Receiver thread (helix) | round | as a root line (section 2) | same |
| Receiver key slot, holder key, collet foot key | theta 37 | no (37 off +X, 53 off +Y) | no |
| Receiver shoulder bolts 4 x M5 | 30, 150, 210, 330, r 90 | no (x +-77.94; heads behind cut receiver body) | no (y +-45) |
| Witness ruler, holder flange tick | 127 | no | no |
| Collet slits (12, phase 52 + 30k) | nearest 82 and 112 (u > 0), 262 and 292 (u < 0) | no; 112 and 262 lie behind the plane (x = r cos theta < 0), 82 and 292 in front (cut away) | no (nearest 172/352, 8 off) |
| Wing-nut wings | 0 and 180 | no: -X wing behind the plane at u +-7 | yes: both wings cut, span 230 shown |
| Tommy bosses | 45 + 90k | no | no |
| Holder inserts M6, r 62 | 45 + 90k | no | no |
| Base plate, hole break, frame rails | Y extents | rails cut (u +-274 to +-304) | end members cut |

Recommendation: **section_yz** (plane x = 0, viewer at +X, look toward -X, u = +Y), the S3 plane. It reuses the signed section convention, look sign, section_u K7, hatch_split and rule (l), and puts S3 and S4 in one plane so a reader compares the two base stacks directly. section_xz would show the wing span in the cut but needs a harness generalisation at (c) for one feature the operator task does not depend on (the sweep r 115 is shown by the S3 dashed extent lines). Cost of yz: wings are off the plane (the -X wing drawn beyond, dashed where behind the core).

## 2. Shape notes (8.4b), every part S4 draws

All z in z_A at pose K d+1 (the governing clamped pose of `stop.collar_top_z` 159.84; ASSEMBLY.md Poses). DERIVED from params through the named build_parts function unless tagged.

| Row | Shape note |
|---|---|
| collet (d 100 of the seven) | Clamped d 100 collet in true section, cut, both walls: foot ring r 66.99 z 40.00 to 42.00 (0.30 radial to the register bore), outer cone r 63.29 at z 42.00 narrowing upward to r 58.00 at the top z 72.00 (alpha 10, shifted 0.5 inward by the clamp), straight bore r 50.50 from 42.50 to 65.70, 45 deg chamfer to r 56.80 at the top face, top face r 56.80 to 58.00 (collet.min_wall 1.2). Core-seat ledge r 47.50 to 50.50, z 40.00 to 42.50, drawn as the core_seat row. Why d 100: it is the family member for the Q10 core (core.diameter_nominal 100, critical-path 4 "about 100 mm diameter") and the S1/S3 drawn core; the outer profile is the same for all seven (r_fo and r0 do not depend on d), so the stack heights hold for the family. Slit ticks: section 2a. |
| core_seat | Ledge r 47.50 to 50.50, z 40.00 to 42.50 (collet.core_seat_height 2.5, core_seat_width 3), one body with the collet; top face is the core stop 42.50. |
| holder | True section from holder.py, cut, aluminium-family hatch as S3: tube OD r 67.04 from the bottom z 49.09 to the flange underside 137.09; inner cone r 62.04 at 49.09 to r 56.75 at 79.09 (chain.H 30); bore r 56.75 from 79.09 to the tube top 153.84; flange r 72.04, z 137.09 to 145.09; tube r 56.75 to 67.04 continues through the nut plate hole (r 68.04, 1.00 radial) to 153.84; collar ring r 55.00 to 76.20, z 153.84 to 159.84, fused (collar row, one body). Key 3.0 x 11.75 x 40 at theta 37 and four M6 inserts off the plane: not drawn, figure note. |
| collar | Collar ring r 55.00 to 76.20, z 153.84 to 159.84 (collar.thickness 6.0); top is the g_stop reference. |
| wingnut | Wing nut cut through its body: thread bore drawn at the receiver major r 74.79 (drafting convention for mated threads; true crest r 72.64, fit.c_r 0.35), body to r 83.14 from the skirt bottom z 97.09 to the plate top 153.09; dust skirt r 83.14 to 95.14, z 102.09 to 111.09; plate r 68.04 to 83.14 over z 145.59 to 153.09 with the washer pocket r 68.40 to 71.90, 0.80 deep in its underside. Wings at theta 0 and 180 lie off the plane: the -X wing beyond, u +-7, z 113.09 to 153.09, dashed where the core outline lies in front; sweep r 115 as dashed extent lines (S3 form). Nut thread root line: section 2b. |
| washer | PTFE ring r 68.40 to 71.60, 1.30 thick, z 145.09 to 146.39, cut, in the nut-plate pocket, standing 0.50 proud onto the holder flange top. Notch at theta 37 off the plane. |
| receiver | True section, cut: floor annulus r 40.00 to 67.29, z 0 to 40.00 (floor hole r 40); wall r 67.29 to 80.00 from z 0 to 76.50, runout land r 67.29 to 72.29 at 76.50 to 80.50, thread zone r 67.29 to 74.79 at 80.50 to 128.50 with the 1.0 x 45 register chamfer at the rim; shoulder r 80.00 to 100.00, z 12.00 to 20.00 (Design Notes 32). Root line: section 2b. Key slot at 37 and bolts off the plane. |
| receiver_spigot (S4 only) | The receiver below the plate top as its own row: r 40.00 to 80.00, z 0 to 12.00, inside the plate hole r 80.20 (section 3). |
| base_plate | Plate cut, 12 thick, u -80.20 to the crop (S3 extends to +-239), spigot-hole gap +-80.20, break line at the crop edge; aluminium hatch. |
| base_frame | Rails cut u +-274 to +-304 (S3 row), only if the crop reaches them; floor line at the datum offset (jig.datum_a_above_floor 60, ASSUMED, N10). |
| core_100 | The Q10 core: upright cylinder drawn d 101.0 (core.diameter_nominal + collet.grip_window_hi, the K d+1 core), 100 tall (core length ASSUMED from critical-path 4), unsectioned outline, chamfer mark 3 x 45 at the top end (core.top_chamfer); bottom on the carrier top. |
| carrier (new) | Riser under a short core: nylon rod d 101.0 at K d+1 (same family size as the core), length 160 (ASSUMED), square ends, unsectioned outline with a centre-line hatch-free fill; bottom on the core seat 42.50, top 202.50; joint to the core bottom drawn as a 1.0 bond line (gypsum or hot-melt bed, ASSUMED). Gripped by the collet over 42.50 to 65.70. |
| liner (liner figure only) | Sacrificial sleeve around the core and carrier: tube OD 106.0 at K d+1 (gripped by the d 105 collet), ID 101.0, wall 2.50, from the core seat 42.50 to the core top 302.50, cut, plastic hatch; drawn in the second figure (section 10). |
| drill_head (reference, moving) | Head outline at the stop, tip 184.84, unsectioned, as S3 (shared row); shows the cutter 25.00 above the collar top. |
| stop / kerf / exposure lines | Three reference lines: cutter tip at the stop 184.84; kerf sphere centre at the stop 291.21; minimum core top 296.21 = nut-plate top 153.09 + core.min_exposed 143.12. |

### 2a. Collet slit ticks (drawn form)

No slit lies in the plane. The nearest slit behind the plane on each side is drawn as hidden-line ticks, and the two are of opposite type, so the figure shows the alternating pattern: u > 0, theta 112, top-open slit, z 47.00 to 72.00 (relief hole centre 47.00); u < 0, theta 262, bottom-open slit, z 40.00 to 65.00 (hole centre 65.00). Form: one dashed vertical line per side at the wall mid-radius (projected u = r_mid sin theta), from the open face to the hole centre, with a short horizontal tick 8.0 long (collet.relief_hole_dia) at the closed end; label "12 slits, alternating, 25 long". Admission: a declared sub-artist `collet:slits` (LineCollection, dashed), count 2 lines plus 2 ticks, each line vertical, inside the collet's drawn hull, length collet.slit_length 25 within 0.05, the u > 0 line touching the top face and the u < 0 line touching the foot. The Topologist signs the admission at (c).

### 2b. Receiver thread ticks (drawn form)

The signed screw_c:root form (K5-B37 to B39): two dashed vertical root lines at r thread.minor / 2 = 72.29, one each side, over the thread run z 80.50 to 128.50 (thread.run_turns 6 x pitch 8), inside the drawn receiver wall (major r 74.79), sub-artist `receiver:root`; label "thread 149.58 x 8 RH, 6 turns". The nut's engaged zone (z 97.09 to 128.50) reads from the overlap of the nut and receiver outlines.

## 3. S4-a: row split under X1

- Shared rows stay X1-equal: `receiver` keeps its z_rule (z_min base.plate_thickness) and place; `base_plate` keeps z_rule and plan_poly. Neither changes.
- New S4-only row `receiver_spigot`: section [receiver.floor_hole_dia / 2, receiver.spigot_od / 2, 0, base.plate_thickness], neighbours: receiver C (kind one_body), base_plate G g_min 0.10 (radial 0.20 drawn, base.spigot_hole_dia / 2 - receiver.spigot_od / 2; icd.coaxiality_chain[1] 0.20; g_min 0.10 = half the chain entry, the same floor as fit.c_r_min, ASSUMED).
- The plate-hole break is a field of the S4 base_plate row: `section_u` pieces ending at +-base.spigot_hole_dia / 2 (the S3 row already has this form; X1 does not compare section_u). No new row.
- receiver|base_plate stays C on the shoulder face z 12.00 (Design Notes 32).

## 4. S4-b: holder section, class changes, scope

Values: section 2 (holder row). Class changes in S4:

| Pair | S1/S3 today | S4 |
|---|---|---|
| receiver\|holder | C (stand-in OD = register bore) | G 0.25 (register.g_reg; drawn 0.25 radial) |
| holder\|collet | C | C on the cone, z 49.09 to 72.00 (contact height 22.91 at K d+1, seat.contact_height_Kmax note) |
| collar\|holder | F (S1 drew the holder to the flange top) | C, kind one_body |
| wingnut\|holder | N | G 0.50 (axial: washer proud; radial 1.00 at the plate hole) |
| collar\|wingnut | N | G 0.75 (nut.lift_play) |
| holder\|core / carrier | N | G 1.0 (radial 6.25 at the bore, ASSEMBLY.md holder\|core G 1.0) |

Scope options:
- (i) S1 r9 and S3 r8 both draw the true base-stack sections (holder, collar, collet, receiver wall), and X1 gains the `section` field for every shared row. One holder per plane and per figure; closes the X1 hole for its class.
- (ii) S1 r9 only; S3 keeps the stand-in. X1 cannot gain `section` until S3 changes, so the hole stays open for S3 and S4 (two different holders in the same section plane).
- (iii) Neither; S4 draws the true sections under the shared ids and X1 stays blind to it.

Recommendation: (i). The rule-scope rule (detail 1 common) asks for the class, and S3 and S4 share a plane. S1-5b, S1-4, the drill_head|collar 25.000 identity and every S2 margin are unchanged by the section change (the collar top and wing-nut top do not move); S3-3's base links (core_seat, collet, receiver shoulder) keep their faces. Cost: S3 r8 with a fresh M1.

## 5. S4-c fits and S4-d

| C pair (base stack) | Fit (source) | S4 class |
|---|---|---|
| collet foot\|receiver floor | axial face; radial 0.30 to the register bore (fit.seat_clearance) | C, fit in the source text |
| core_seat\|receiver | one body with the collet foot | C, one_body |
| core or carrier\|core_seat | axial face, core weight | C |
| collet\|carrier (grip) | clamped, K d+1; R pose zero interference | C over 42.50 to 65.70 |
| holder\|collet | cone face; R pose 0.2954 normal (ASSEMBLY.md) | C |
| holder\|washer | flange top bears on the washer at K | C |
| washer\|wingnut | press pads, 2.40 mm3 designed (class P, ASSEMBLY.md) | C, class P in the source text |
| wingnut\|receiver | thread flank; crest clearance fit.c_r 0.35, axial flank gap fit.g_a 0.30 | C on the drawn major cylinder, fits in the source text |
| collar\|holder | one body | C, one_body |
| receiver\|base_plate | shoulder face z 12 | C |
| receiver_spigot\|base_plate | radial 0.20 | G 0.10 |
| receiver\|holder | radial 0.25 | G 0.25 |

S4-d: adopt. Predicate `vertical_edge` on the collet bore piece: both bore edges between the core-seat top and the chamfer start keep u constant within 0.05. Reason: the bore is the grip face; a bore drawn parallel to the cone tells the reader the core is wedged by a taper, the wrong mental model, and it costs one predicate. B: bore drawn parallel to the outer cone.

## 6. Advance options (Q4)

Constraint common to every core-moving option (DERIVED): the collet grips 23.20 of core; the least slice under F4 is 56.02 to 76.44. So no option that moves the core through the kept collet can deliver one slice with the core still gripped, unless the gripped member moves with the core.

| Option | Kept-part change (Quinn) | S3-3 cut-case chain | Operator steps per slice | Advance per slice | S4-2 tests | With the sacrificial option |
|---|---|---|---|---|---|---|
| (A) Push rod from below through the floor hole | None to the receiver (hole d 80 exists). A jack bracket under the base plate (plate holes, Quinn's base.py). Under-plate void 60 tall inside the closed frame (N10): no hand access without feet | core, rod (thread), jack bracket, base plate: collet and receiver leave the chain in slice mode | reach under the frame, turn the jack, back off and re-tighten the wing nut | <= 23.20 with grip; beyond that the core stands free on the rod (R10 fails) | rod\|receiver floor hole G 1.0 (rod d <= 78); B rod d 82 | needs the liner to keep grip; the core then slides in a loose liner and carries no torque |
| (B) Spacer pucks on the core seat | none | adds one face link (core, puck, core seat) | lift the core out, drop a puck, reinsert, re-clamp | <= 13.20 (23.20 less a 10 grip, ASSUMED): less than one slice | puck rests_on core_seat; grip overlap | none |
| (C) Carrier (riser) under the core | none (consumable, like the stand-in core) | core, bond, carrier, core seat, collet, receiver: one face link added | none per slice; set once per core | n/a (the lift advances) | exposure and grip (below) | liner around core and carrier (section 8) |
| (D) Relative advance by the lift: the core stays on the stop, the drill lowers one slice per cut | none | unchanged | none (the lift steps down) | any, within 650 travel | slice positions reachable: core top >= kerf centre + 5 at a tip >= 184.84 | compatible |
| (E) Liner push-pop (Quinn's image: tube gripped, core pushed up inside) | as A | as A | as A | any | as A | the liner is the tube; the core inside is loose in the liner and takes no drill torque unless bonded, and a bonded core cannot be pushed |

Recommendation: **(D) with (C) drawn.** Slices come from the lift: a 0.75 m core on the stop is sliced from its top 792.50 down to 296.21 by lowering the drill (496.29 of sliceable core, 6 slices at the F4 minimum 76.44; DERIVED). Only the last 253.71 (and any short core) needs a riser, and the carrier supplies it with the grip kept. No kept part changes; the S3-3 chain is unchanged at capture. R11 ("core can be advanced upward through the collet") is met as relative advance; Sean rules whether that wording holds (STOP item 2).

S4-2 form for (D)+(C), "short-core exposure and grip": (a) core_100 rests_on carrier, carrier rests_on core_seat (0.05); (b) drawn core_100 top minus the nut-plate top >= core.min_exposed; (c) the carrier's drawn extent covers the collet straight bore 42.50 to 65.70. Z: live spec, exposure 149.41 against 143.12 (margin 6.29, DERIVED). B1: carrier deleted (core on the seat, exposure -10.59). B2: carrier 150 (139.41). B3: carrier bottom drawn at 66.00 (no grip overlap). Detail 1.4 lists the 100 mm exposure as a reported value; (b) asserts it on the drawn configuration only (the claim the figure makes), and core.min_exposed is DERIVED from DECLARED g_stop, not a soft key. Sean rules (item 2).

Torque through the carrier joint (DERIVED, 10 N m, loads.torque_design): bottom-face shear 2T / (pi r^3) = 50.9 kPa on r 50. A weak cement core (near-zero tensile strength, critical-path 4) may shear at that face; the cast-on liner spreads the same torque over the side, T / (2 pi r^2 L) = 6.37 kPa on 100 of length. That is the case for the liner on weak cores.

## 7. Collet length (Q5)

A taller collet (cone and holder longer by Delta) raises the collar top by Delta (DERIVED):

| Delta | collar top | stop.height_z | min core on the stop (Q10) | highest point z_S (S1 park) |
|---|---|---|---|---|
| 0 (kept) | 159.84 | 184.84 | 253.71 | 1969.84 |
| 25 | 184.84 | 209.84 | 278.71 | 1994.84 |
| 50 | 209.84 | 234.84 | 303.71 | 2019.84 (over the soft target) |

Rows that move with Delta: S1 every pose tip and the core_750 z rules (load, start, capture_end, park +Delta), S1-4 (anchor margin 0.84 + Delta at capture_end; guide margin at park -Delta unless anchor_z and top_guide_z rise Delta, which moves member tops 1225, member_length 1213, member_length_rail 1225 and L), S1-5a, S1-5b positions; S2 z bands and S2-5b (drill-head tip at load 959.84 + Delta against the hand band 940); S3 capture_end pose, nut stations and the S3-2 span positions. The identities drill_head|collar 25.000 and S1-1 hold. The grip length grows Delta, and the minimum core length grows Delta, so a taller collet makes Q10 worse.

Recommendation: keep the kept 32 mm collet (no value, no key moves). Quinn's "taller collet" (support along the core) is given by the liner (section 8), drawn as the second figure; that alternate outline changes no key S1, S2 or S3 reads.

## 8. Sacrificial collet or liner (Q6)

- (a) Sacrificial collet variant: the collet sits z 40 to 72, under the holder and collar; the cutter stops at 184.84 and the dome is 219.77 to 240.19. A collet the drill can cut must rise above about 220 through the collar ID 110 and the iris throat 108.585, so its upper part is a thin tube: that tube is the liner.
- (b) **Liner (recommended):** a thin tube, OD equal to a family size, ID = core d + core.tol, around the core from the core seat to the core top, gripped by the collet of its OD and cut with each slice (the slice comes off with a ring of liner, R12). Best made as the casting sleeve of the cement core left on (bond over the whole side; torque 6.37 kPa, section 6). Wall = (D - d - 1) / 2 >= collet.min_wall 1.2, so D = d + 5: core 100 in a 105 liner (wall 2.0 free, 2.50 drawn at K d+1 as OD 106 / ID 101); core 95 in 100; core 105 has no liner (needs 110, above collets.envelope_max 106.585). Drawn form: two cut strips, plastic hatch, 42.50 to the core top, in the liner figure.

## 9. Q10: datum, minimum length, slices

- Datum: the nut-plate top. Source: params `core.min_exposed` text ("plus collar.top_above_plate 6.75") and the ICD row Exposed core, research/quinn/cr_scratch/step2_system_concept.md line 72, "above the plate top (collar top is 6.75 above plate)" (DECLARED by the source). The arithmetic is consistent: plate top 153.09 + 143.12 = 296.21 = collar top 159.84 + 136.369 = kerf centre at the stop 291.21 + stop.margin 5 (DERIVED).
- Minimum core length on the stop: 296.21 - 42.50 = **253.71** (DERIVED; 260.46 if the datum were the collar top).
- A 100 mm core on the stop tops out at 142.50, 17.34 below the collar top, exposure -10.59: the kept family does not cover it directly.
- Option that exposes it: (C) carrier 160 under it (core top 302.50, exposure 149.41). (A), (B) and (E) cannot, with grip (section 6).
- Slices at the drawn advance: one slice from a 100 mm core under F4 (the slice is at least 76.44 on the axis; the core is 100), cut at the stop with the core top at 302.50, leaving a stub 17.27 (axis, to the dome pole 219.77) to 37.69 (core surface, to 240.19) bonded to the carrier; a second cut runs into the carrier (sacrificial, R12). If Quinn rules F4 does not bind each slice (B3-4), the count follows his least slice.

## 10. Poses and cores drawn

One pose, `slice_stop`: drill tip at stop.height_z 184.84, base stack at K d+1. Two figures by configuration: (1) `carrier`: d 100 collet, carrier 160, 100 mm core; (2) `liner`: d 105 collet, liner OD 106 x 2.50, carrier d 101 inside, the same 100 mm core. Cores drawn: the 100 mm core only. The 0.75 m core and its 253.71 stub are reported (S1 draws the 0.75 m core). Option (A) rod not drawn unless Sean picks it. Crop: z_A -60 (floor) to about 330, u +-130 with plate break lines.

## 11. Operator-task rows (S4; z_S = z_A + 60)

| Task | Pose | Sketch | Reach height and stance | Sightline | Hazard | Check or rubric |
|---|---|---|---|---|---|---|
| Set a short core: carrier and core (3.3 kg, 260 tall) into the collet | load (ring parked, tip 1019.84 z_S) | S4, S1, S2 | kneel or stand in the S2 sector (theta 90 +- 45); wing nut backed off (pose R); lower the stack over the collar top 219.84 z_S, hands at 280 to 520 z_S, grip the core top; re-tighten the wings (sweep r 115) | down the holder bore from the sector | fingers cannot enter the 4.5 radial gap at the collar ID; the stack must be held upright until clamped (the carrier joint is the weak point) | S4-2, V4, V10 |
| Advance for a slice | slice_stop sequence | S4, S1 | none: the lift steps down one slice (D) | as the S1 watch row | gear and pinions turning (S1 watch row) | V10, reported slice count |
| Take the slice off | park | S4 | slice captured in the drill above the iris; opened at park over the base | open | slice falls when the iris opens; tie to N6 (captured-core removal) | N6, owner Quinn |
| Change a collet (liner option) | load | S4, S1 | as the S1 collet row; the liner comes out with the core, upward | wing nut from the sector | as the S1 row | V10 |

## 12. K8 predicates (S4-3), rubric, g_min, reported items

Predicates (sign checks on drawn coordinates):
- collet taper: (r(z_top) - r(z_bot)) / (z_top - z_bot) < 0 on the outer cone piece (existing `taper narrows: up`).
- collet narrow end up, foot at the bottom: foot ring z_max < cone top z (`below`, foot under cone); foot z_min on the receiver floor top within 0.05.
- holder bore cone narrows up: same sign on the holder inner cone piece; the holder cone and collet cone share a sign (mating sense).
- collet bore vertical (S4-d): |u(z1) - u(z2)| <= 0.05 on both bore edges.
- wing nut above holder flange: z_min(nut plate piece) - z_max(flange) = +0.50 > 0.
- washer between nut and holder: (z_mid(washer) - z_max(flange)) x (z_min(nut plate top) - z_mid(washer)) > 0.
- receiver floor at the bottom: z_max(floor annulus) = 40.00 < z_rim 128.50, and z_min(collet) = z_max(floor) within 0.05.
- core upright on the stop: core_100 rests_on carrier, carrier rests_on core_seat (0.05); chamfer mark z > core mid z.
- collar above the flange: z_min(collar) - z_max(flange) > 0.

Rubric additions (S4): the collet foot is at the bottom and its cone narrows upward; the wing nut sits above the washer above the holder flange; the 100 mm core and its carrier stand upright, chamfer at the top, the core top above the minimum-exposure line; the two slit ticks show one top-open and one bottom-open slit.

g_min for new pairs (ASSUMED unless sourced): receiver_spigot|base_plate G 0.10; receiver|holder G 0.25 (register.g_reg); wingnut|holder G 0.50; collar|wingnut G 0.75; carrier|holder, core_100|holder, carrier|wingnut, core_100|collar G 1.0 (ASSEMBLY.md core pairs; drawn radial 6.25 to the holder bore, 17.54 to the nut-plate hole, 4.50 to the collar ID); carrier|collet C; carrier|core_seat C; core_100|carrier C (bond); liner|collet C; liner|core_100 C (cast-on); liner|holder G 0.5 (drawn 3.75 at r 53 to 56.75); drill_head|collar G 25 (shared, stop.g_stop); option A only: rod|receiver G 1.0.

reported_items:

| id | text | source | needs_drawing |
|---|---|---|---|
| q10_exposed | exposed length of the drawn 100 mm core above the nut-plate top, against core.min_exposed 143.12 (on the stop -10.59; on the carrier 149.41) | core.min_exposed, collet.core_stop_z, carrier.length | true |
| q10_min_on_stop | minimum core length on the stop, 253.71 (nut-plate datum; 260.46 collar-top datum) | core.min_exposed, stop.collar_top_z, collar.top_above_plate | false |
| grip_length | collet straight-bore grip, d 100: 23.20 | collet_family dims | true |
| slice_min | least slice under F4: 76.44 axis, 56.02 at r 50 | drill.kerf_standoff, drill.dome_pole_offset, iris.face_radius_core | false |
| slices_075 | 0.75 m core: sliceable 496.29, 6 slices at the F4 least slice, stub 253.71 | core.length_install, core.min_exposed | false |
| carrier_torque | carrier-joint shear at 10 N m: 50.9 kPa; liner side shear 6.37 kPa | loads.torque_design | false |
| q5_delta | collar top, stop, min core length per collet Delta (section 7 table) | stop.collar_top_z | false |
| liner_wall | liner wall per core size (D = d + 5, wall 2.0) | collet.min_wall, collets.envelope_max | false |
| kept_axial | axial force in collet, receiver, base plate at 1000 N and F_stall + W 1287.05 N (unchanged from S3 r7) | S3 load_cases | false |

## 13. Values that move keys read by S1 r8, S2 r9, S3 r7

Under the recommendations: **0**. New overlay keys only (carrier.length 160, carrier.material nylon, carrier.bond, liner.wall 2.0, liner.od_rule "core d + 5"; all ASSUMED), none in any keys_read. The S4-b scope (i) edits z_rule and section fields (collar z_min to collar_top - collar.thickness; holder, collet, receiver sections) in s1_spec.yaml and s3_spec.yaml and adds keys to their keys_read (register.g_reg, chain.t_h, chain.H, collar.thickness, nut.lift_play, thread.minor, thread.major) at unchanged values; that opens S1 r9 and S3 r8 under step (i) with no margin moving. A taller collet (rejected) moves stop.collar_top_z and with it the S1, S2, S3 rows in section 7.

## 14. Batch 3 draft (to Quinn)

| ID | Question | Feeds | Owner | Value used until answered (ASSUMED) | Answer | Date |
|---|---|---|---|---|---|---|
| B3-1 | Receiver floor: the debris hole (d 80) already passes a push rod up to d 78. If Sean picks a push from below, may a jack bracket be bolted under the base plate, and may the debris hole carry the rod? No receiver change is proposed | S4-2 option A, base plate | Quinn | not used: slices come from lowering the drill; a carrier under short cores | | |
| B3-2 | Collet length: a taller collet raises the collar top and the cutter stop by the same amount and makes a 100 mm core harder to reach (min core on the stop 253.71 + Delta). We propose keeping the 32 mm collets and giving long support with a liner. Agree? | Q5, stop.collar_top_z, S1 to S3 | Quinn and Sean | kept 32 mm collet | | |
| B3-3 | Sacrificial option: a liner tube (OD a family size, wall 2, cast on as the core's mould sleeve) gripped by the collet and cut with each slice, in place of a sacrificial collet variant. Can the core supplier cast into a sleeve, and can the iris leaves cut a 2 mm printed or card wall? | Q6, R12, S4 liner figure | Quinn | liner, PETG or card, wall 2.0 | | |
| B3-4 | core.min_exposed (F4) puts the core top 5 above the kerf sphere centre. Does that hold for every slice? If so the least slice is 76.44 on the axis (56.02 at the core surface) and a coaster slice is not possible. What is the least slice the iris can cut? | Q10, slice count, S4 reported items | Quinn | F4 binds every slice | | |

## 15. Section-view reviewer control figure

Yes. S4 is the first M1 whose rubric includes collet and nut sense (V3 per the applicability line) in a section view; the side and plan controls do not exercise a flipped collet in a cut. Add one section-view control pair: the S4 base section correct, and the same with the collet flipped end for end (foot ring at the top, cone widening upward), scored on V3 under the blinded key.

## 16. Decisions for Sean (STOP S4-A)

1. **Plane.** Options: section_yz (signed machinery, S3 plane), section_xz (wings in the cut; harness work at (c)). Recommend section_yz.
2. **Advance option and S4-2 form.** Options: (A) push rod, (B) pucks, (C) carrier, (D) lift advance, (E) liner push-pop. Recommend (D) with (C) drawn; R11 read as relative advance; S4-2 rewritten as short-core exposure and grip (section 6), asserting exposure on the drawn configuration. Alternative: keep exposure reported only, S4-2 grip and rests_on only.
3. **Collet length.** Options: keep 32 mm; Delta 25; Delta 50 (section 7). Recommend keep 32 mm, with the liner as the long-support outline.
4. **Sacrificial option.** Options: sacrificial collet variant; liner. Recommend the cast-on liner, D = d + 5, drawn in the second figure.
5. **Holder scope and X1 section.** Options (i) S1 r9 + S3 r8 with X1 comparing `section`; (ii) S1 r9 only; (iii) neither. Recommend (i).
6. **Values moving S1/S2/S3 keys.** None under the recommendations; the S4-b z_rule and section edits open S1 r9 and S3 r8 with no margin change.
7. **Left to the orchestrator:** rule (l) firings on S1 r8, S2 r9, S3 r7 from the step 0 dry run, and their coupling to S1 r9.
8. **Batch 3.** Send B3-1 to B3-4 now (B3-1 informational unless (A) is picked). Recommend send.
9. **S4-c and S4-d.** S4-c: keep the C pairs as C with fits in the source text; receiver|holder G 0.25, receiver_spigot|base_plate G 0.10, wingnut|holder G 0.50, collar|wingnut G 0.75, wingnut|receiver C on the drawn major cylinder. S4-d: adopt the bore-vertical predicate. Recommend both as listed.

## Gameplan lines to change

1. Design Notes 25, row S4-b (line 683).
Old:
```
| S4-b | Holder section from `build_parts/holder.py`: OD 67.04, cone 62.04 to 56.75 over chain.H 30, bore 56.75, tube through the nut plate to the collar. Then receiver\|holder becomes G 0.25 and collar\|holder becomes C. Retire the S1 spec holder-stand-in note when S4 is accepted; S1 re-runs under step (i) | 1.4 (S4) | The Engineer; The Designer |
```
New:
```
| S4-b | Holder section from `build_parts/holder.py` (radii): OD r 67.04 (D 134.08), cone r 62.04 to 56.75 over chain.H 30, bore r 56.75, flange r 72.04, tube through the nut plate to the collar underside 153.84 z_A, collar ring fused (collar.thickness 6.0, 153.84 to 159.84; the S1/S3 collar row z_min 153.09 includes the 0.75 lift play). Then receiver\|holder becomes G 0.25 and collar\|holder becomes C (one body). Retire the S1 spec holder-stand-in note when S4 is accepted; S1 re-runs under step (i) | 1.4 (S4) | The Engineer; The Designer |
```
2. Detail 1.4, line 320.
Old:
```
Sequenced at the 1.4 open (`research/sean/cr_scratch/step1.4_manager_open.md` section 1.1): step 0 (P0) carries G4 (per-control times, fast tier, pruning ruled by The Software Engineer), G5 with its class (record deps: certifier records, spec, script; a --stale deps branch; S3 r7 re-recorded at ORCH-A), G2 control blinding (`--m1-controls`, fresh tokens per round, key outside the tree), K4 rule (l) over its class (reference lines, gridlines, part edges; side, plan, section) with a dry run on S1 r8, S2 r9 and S3 r7, C1.3-b and C1.3-c; (a) carries S4-a (S4-only spigot row and plate-hole break under X1), S4-b (holder.py section; S1 r9, and S3 r8 if ruled), S4-c, S4-d, the collet-slit and receiver-thread ticks, the section plane, and the advance, collet-length and sacrificial options for STOP S4-A. Q10 at the open (DERIVED): a 100 mm core on the core stop tops out 17.34 below the collar top; exposure needs at least 253.71 of core on the stop (nut-plate datum). S4-2 as written is red on the kept receiver; its form goes to Sean at STOP S4-A.
```
New:
```
Sequenced at the 1.4 open (`research/sean/cr_scratch/step1.4_manager_open.md` section 1.1): step 0 (P0) carries G4 (per-control times, fast tier, pruning ruled by The Software Engineer), G5 with its class (record deps: certifier records, spec, script; a --stale deps branch; S3 r7 re-recorded at ORCH-A), G2 control blinding (`--m1-controls`, fresh tokens per round, key outside the tree), K4 rule (l) over its class (reference lines, gridlines, part edges; side, plan, section) with a dry run on S1 r8, S2 r9 and S3 r7, C1.3-b and C1.3-c; (a) carries S4-a (S4-only spigot row and plate-hole break under X1), S4-b (holder.py section; S1 r9, and S3 r8 if ruled), S4-c, S4-d, the collet-slit and receiver-thread ticks, the section plane, and the advance, collet-length and sacrificial options for STOP S4-A. Q10 at the open (DERIVED): a 100 mm core on the core stop tops out 17.34 below the collar top; exposure needs at least 253.71 of core on the stop (nut-plate datum, confirmed at 1.4 (a) from the ICD row Exposed core). S4-2 as written is not red on the kept receiver: its floor carries the 80 mm debris hole (receiver.floor_hole_dia), which passes a push rod up to d 78 (Designer 1.4 (a) Correction 1); its form goes to Sean at STOP S4-A.
```
