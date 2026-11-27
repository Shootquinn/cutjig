# Step 1.4 P2r: raiser re-check of the (b) spec fix pass (The Designer, The Loftsman, The Topologist)

Sources: `step1.4_designer_spec_signoff.md` (P3a), `step1.4_loftsman_spec_signoff.md` (P3b), `step1.4_engineer_spec_fixes.md` (P2f).
Dry runs and deletion tests: `D:\Unleashed Robotics\_scratch\cutjig\open14\p2r\`. The scripts there are `tick_win.py`, `adj_dry.py`, `adj_fam.py`, `s1_adj.py`, `s1_rem.py` and `lof_del.py`, with JSON outputs beside each. `ws\deltest.sh` and `ws\del_*.txt` hold the deletion tests, run on a scratch copy of docs/sketches (`ws\docs\sketches`; sketch_common.py restored and byte-equal to the live file after each test). Nothing under docs/sketches was edited.

## Corrections to the brief

1. **"3 pairs on the S1 side view" counts rows.** S1 r8 hatches three rows `//` (receiver, base_plate, collar; Engineer P2f Correction 2). On the drawn figures the lint form, compared by string within 0.5, finds **1 pair**: base_plate|receiver `//` 0.00, in all four poses (MEASURED, `s1_adj.py`). Compared by line family, it finds a **second pair**: descent_stop|ring `////`/`//` 0.00 at capture_end (MEASURED, `fam_probe.py`).
2. **The adjacency lint compares hatch strings.** `hatch_adjacency_issues` tests `ha == hb`, so `////` beside `//` passes. That is the same line family at a different density, the class the Topologist raised at 1.3 (R2-4, ruled into `hatch_family`). Designer R2 below.
3. **Deleting the lint's K8 call site passes the full manifest.** With `out += adj` removed from `section_convention_issues`, all 488 of 488 controls still match (Z 110, B 375, smoke 3; 148.1 s at 12 jobs; MEASURED, `ws\del_T2_full.txt`). Every adjacency B calls the function directly (`step14_fixtures.py::_hadj`). Designer R1 below.
4. **The tip schedules written beside the corrected stub do not end at the stop.** The counts, stubs and removed lengths are right. The Loftsman's P3b 1e list ("681.13, 604.69, ..., 222.51") and the Engineer's carrier list ("268.40, then 191.96") each place the last cut above the stop. They would leave 214.94 and 24.39, against the stated 177.27 and 17.27. The schedules that produce the stated values step up from the stop. The Loftsman section has them.

## 1. The Designer

### 1.1 Per FIX

The deletion tests ran on the scratch copy, on the eight P2f controls (`--only`) unless stated (MEASURED).

| FIX | Status | Evidence |
|---|---|---|
| 1 tick and root labels | CLOSED (spec) | The templates print "12 slits, alternating, 25 long" and "thread 149.58 x 8 RH, 6 turns" from the keys, with map right to RH (MEASURED). No harness reader exists before P4, so no deletion test is possible. The renderer and its K4/K5 reads are carried to P4 by name. |
| 2 hatch adjacency | CLOSED for S4, with R1 open | T3, cut_hatch variant branch deleted: K8-Z19 fires, K8-B98 counts 2 against 1 planted, K8-B101 counts 1 against 2 planted (3 mismatches). T4, hatch_variant lint clause deleted: K8-B99 clean, K8-B100 counts 1 against 2 planted. The lint function was red on the pre-change code (P2f section 2). T2, call site deleted: 488/488 match (R1). |
| 3 min_bearing | CLOSED | T1, min_bearing branch deleted: K8-B96 clean (red). The S4 drawn Z and the carrier-at-r-49.90 B land at P4. |
| 4 wing form | CLOSED (spec) | Style, label (span 230, MEASURED), admission text and convention.beyond are in the spec. The rule lands at P4, and the Topologist signs it there. |
| 5 staged O4 follow-ons | CLOSED (staged) | Staged X1 passes, and section_true is equal on receiver, collet, core_seat, holder, wingnut, washer and collar (MEASURED, `lof_del.json`). Deletion (the staged S3 wingnut shape back to the pre-FIX body): wingnut equality goes false. |
| 6 rubric | CLOSED | Text. |

### 1.2 Ruling: theta 90 washer window (Loftsman FIX 2): the true-section form stands

- **Form: plane_cuts, with the +u pocket rim absent.**
  - Sean's ruling draws the base stack in true section. The S4-c classes (wingnut|holder G 0.50, washer contact at 146.39) hold on the true section.
  - The Loftsman's O2 (iii) puts plane-dependent features outside section_true, which keeps X1 equality.
  - A rim drawn with a drafting reason would show material the part does not have, on the one plane the figure exists to show.
- **Dry run** (DERIVED, `tick_win.json`):
  - the window r 70.90 to 84.14 covers the rim r 71.90 to 83.14 over its whole z band 145.59 to 146.39;
  - the washer to plate-underside contact at 146.39 is unchanged on both sides.
- **The window's far wall is not drawn.** It is seen through the slot at x -5.00, u 71.73 to 82.99, 0.80 tall. That is two 0.80 edges against the plate and pocket-floor lines, too short to read. It goes in the figure note instead.
- **Figure note.** The asymmetry needs one line, or the absent rim reads as a drafting error. Change "washer windows at 210 and 330" to "washer windows at 210 and 330 (the theta 90 window lies in the plane: +u pocket rim absent)". The Engineer applies this at P4 with the plane_cuts renderer. It is a text edit and moves no key.

### 1.3 Ruling: +u slit tick (Loftsman FIX 1), with The Topologist: form (a)

- **Form.** The +u line is drawn vertical at the collet top-face mid-radius, z 47.00 to 72.00.
  - The u value is read from the collet section_true top piece: (r_in + r_out) / 2 of the top face = (56.8002 + 58.0002) / 2 = **57.4002**. It is never a literal.
  - The -u line stays as signed: u -55.425, z 40.00 to 65.00.
- **Why (a).** The alternation is the information in these two ticks. The reader learns which end of each slit is open from the end of the tick that meets a face:
  - +u meets the top face;
  - -u meets the floor.

  Form (b) ends at 66.52 on the chamfer edge. It loses that signifier and reads as a hidden edge stopping in mid-wall.
- **Dry run** (MEASURED on the live s4 spec through check_stack.eval_expr, `tick_win.py`):

| Form | u | z | Inside the drawn hull | Touches the top face | Least margin to the wall edges |
|---|---|---|---|---|---|
| (a) top-face mid-radius | +57.40 | 47.00 to 72.00 | yes (hull 40.00 to 72.00 at u) | yes (r 56.80 to 58.00) | 0.60 |
| (b) projected to the chamfer | +51.32 | 47.00 to 66.52 | yes | no | 0.00 (ends on the chamfer edge) |
| as spec | +51.32 | 47.00 to 72.00 | no (5.48 above the hull) | no | -5.48 |
| -u as signed | -55.43 | 40.00 to 65.00 | yes | floor | 3.81 |

- **Spec edits** (P4, with the sub-artist renderer):
  - `collet.slits.u` becomes "+u: the top-face mid-radius (top piece r_in + r_out) / 2, the line revolved into the plane at its own side (Designer/Topologist P2r form (a)); -u: r_mid sin(theta), r_mid the wall mid-radius at the line's mid-height".
  - The admission text keeps "the u > 0 line touching the top face".
  - Delete `u_form_open`.
- **The label stays anchored on the -u line.**
- **Relief-hole tick at the closed end.** It is collet.relief_hole_dia wide, centred on u 57.40 at z 47.00. The wall there spans r 50.50 to 62.41, so it stays inside (DERIVED).

### 1.4 Ruling: same-hatch adjacency for S3 r8 and S1 r9 (landing at P6)

The lint is not narrowed. Separate bodies in contact that carry one hatch read as one solid. Adjacent parts take different hatches (ASME Y14.3). The 16 S3 pairs come from three causes, and each cause gets its own remedy, applied in this order.

1. **Material truth first.**
   - Every cut row in a spec that declares the gap carries an explicit `hatch`, and the default steel is refused there. Lint text: "<id>: cut row with no hatch in a spec that declares section.hatch_adjacency_gap".
   - S3 shared rows take the S4 values (X1 rows):
     - receiver: aluminium, hatch_variant alt;
     - collet and core_seat: plastic;
     - holder and collar: aluminium.
   - S3-only rows (drafting material classes, ASSUMED; gate B2 bars material keys from params):
     - drill_tube steel (its shape text says steel);
     - bearing steel;
     - gear steel and pinion_c steel;
     - gear_hub aluminium;
     - motor23_c steel and liftmotor_c steel;
     - home_switch_c plastic.
2. **One body where the shape text already says one part.** A `neighbours` entry with kind one_body is added on each pair:
   - collet|core_seat (S4 form; "the core-seat ledge is the collet bore bottom");
   - ring|nut_housing_c ("one body: the ring pieces stop at the housing outline");
   - ring|motor_mount_c ("hatched with the ring");
   - liftmotor_c|liftmotor_pilot_c ("cut with the motor").
3. **An alternate on one member of each remaining same-material pair.**
   - hatch_variant alt on bearing (against drill_tube), pinion_c (against gear) and anchor_locknut_c (against anchor_bearing_c): steel alternate `++`.
   - hatch_variant alt on frame_upper_c (against base_frame, bracket_anchor_c and bracket_guide_c): extrusion alternate `**`.
   - S3 `section.hatch_alt` becomes {aluminium: "||", plastic: "--", steel: "++", extrusion: "**"}. hatch_alt_issues is clean (MEASURED).
   - `**` is on the 60-wide member only, where the stars read. `++` on the small steel parts reads against the single diagonal `\\`.
   - S3 figure-note legend: "Hatch: aluminium // (receiver ||), extrusion xx (frame member c **), steel \\ (bearing, pinion c, anchor locknut ++), brass .., plastic oo".
4. **The lint compares line families** (`hatch_family`, the 1.3 R2-4 rule), and density no longer separates two parts (R2).
5. **S1 r9.**
   - S1 declares the gap.
   - The lint runs on every Axes of a spec that declares it. Where a row carries no section_class (S1 side views), it takes every row drawn with a hatched area.
   - Premise: the drawn hatch is read from the artist, family-compared. S1 carries no material convention, so none is assumed.
   - Pattern changes:
     - receiver `||`, the same receiver pattern as S3 and S4;
     - descent_stop `\\\\` (metal pad), off the ring's `/` family.

**Dry run** (MEASURED, `adj_dry.json`, `adj_fam.json`, `s1_rem.json`; S3 drawn by s3_jackscrew_section.build on the live r7 spec and on the staged r8 spec, gap 0.5 declared in memory):

| Figure | As drawn, string | As drawn, family | Remedy, string | Remedy, family |
|---|---|---|---|---|
| S3 r7 (live spec) | 16 | 16 | 0 | 0 |
| S3 r8 (staged spec) | 16 | 16 | 0 | 0 |
| S1 r8 (4 poses) | 1 | 2 | 0 | 0 |

- On S1 after the remedy, no same-family pair lies within 20 mm.
- In the S3 dry run, steps 1 and 2 alone leave 1 pair (ring|motor_mount_c `//`), which step 2 closes. The remedy as listed reaches 0.
- **P6 Bs, each red on the pre-change form:**
  - S3 receiver variant removed: receiver|holder fires;
  - S3 hatch removed from gear: the material-truth clause fires;
  - S1 receiver back to `//`: base_plate|receiver fires;
  - S1 descent_stop back to `////`: descent_stop|ring fires under the family compare only.
- S1 r9 is drawn at P6 with the true-section holder, wing nut and washer. Any pair those rows add takes the same three steps, and the Engineer lists each one.

### 1.5 New findings from the fix pass

- **R1. No B covers the K8 call site of the adjacency lint** (Correction 3). The lint is claimed live on S4, and deleting its wiring passes 488/488.
  - Remedy: one B that reaches the lint through `k8` / `section_convention_issues` on a section Axes whose spec declares the gap. The earliest is P4, with the S4 drawn figure 1 and the receiver hatch_variant removed (receiver|holder fires). The P6 S3 receiver B also qualifies.
  - No P2 revision opens on it.
- **R2. The adjacency lint compares strings** (Correction 2). **Class repeat** (Topologist 1.3 R2-4, hatch lint by string), so it goes to the orchestrator.
  - Remedy as in 1.4 item 4, landing with the P6 scope.
  - S4 is unaffected: its patterns are pairwise in different families.

### 1.6 Signatures and verdict

- min_bearing rule (FIX 3): **SIGNED.** The premise is stated, Z18 and B96 hold, and the deletion goes red.
- hatch_variant and alternate table (FIX 2): **SIGNED.**
- Adjacency lint (FIX 2 premise lint): **NOT SIGNED** until R1 has a B through the call site. The form and the lint text are signed.
- Staged S1 r9 / S3 r8 text (O1, FIX 5): **SIGNED.**

**Verdict: FIX 1 to 6 CLOSED.** R1 is open and lands with a drawn B at P4. R2 is a class repeat, for the orchestrator. The three rulings are in sections 1.2 to 1.4.

## 2. The Loftsman

### 2.1 Per FIX

| FIX | Status | Evidence (deletion test) |
|---|---|---|
| 1 +u slit tick | CLOSED by the 1.3 ruling, form (a) | u 57.4002, inside the hull, touches the top face, margin 0.60 (MEASURED). The hull and line arithmetic matches my P3b values: top face 56.80 to 58.00, mid 57.40. The Engineer writes the spec text at P4, and the harness dry run is due with the sub-artist renderer. |
| 2 theta 90 window | CLOSED, form ruled (1.2) | The window covers the rim: 70.90 <= 71.90 and 84.14 >= 83.14, z band equal (DERIVED). No harness reader exists before P4. |
| 3 relief bore | CLOSED | Pieces as my P3b dry run: body 74.79 to 83.14 over 97.09 to 139.09; relief 75.34 to 83.14 over 139.09 to 145.59. Deletion (relief removed in staged S3 only): wingnut section_true equality goes false. Harness X1 still passes, because section_true compare is O2 (i) and lands at P4 (carried by name). |
| 4 skirt profile | CLOSED | Poly (83.14, 102.09), (95.14, 102.09), (95.14, 104.09), (83.14, 111.09), area 66.000. Deletion (staged S3 skirt back to the rectangle): wingnut equality goes false. Harness X1 passes, as for FIX 3. |
| 5 slice count, stub | CLOSED | `checks_s4.slice_numbers` prints 7. Deleting the +1 prints 6 against the hand 7. RPT carries no threshold, so the hand value stands as the check at each re-check. |
| N6 key_offset_deg | CLOSED | Key present in the collet_105 list. |

### 2.2 Corrected stub: arithmetic confirmed

From the keys (MEASURED, `slice_numbers`; hand DERIVED):
- tip 184.84;
- pole offset 34.9315, pole 219.7715;
- least core top 153.09 + 143.12 = 296.21;
- least slice 296.21 - 219.77 = **76.44** (axis);
- core top 42.50 + 750 = 792.50.

| Item | Hand | Code |
|---|---|---|
| Tip span (admissible tips) | 792.50 - 296.21 = 496.29, 681.13 to 184.84 | 496.29 |
| Cuts on the stop | 1 + floor(496.29 / 76.44) = 1 + 6 = 7. Eight need 7 x 76.44 = 535.07 > 496.29 | 7 |
| Schedule ending at the stop | tips 184.84, 261.28, 337.72, 414.16, 490.59, 567.03, 643.47; first slice 792.50 - (643.47 + 34.93) = 114.10, then six at 76.44 | |
| Removed on the stop | 792.50 - 219.77 = 572.73 | 572.73 |
| Stub on the stop | 219.77 - 42.50 = **177.27** axis; 240.19 - 42.50 = 197.69 surface | 177.27 / 197.69 |
| Least core on the carrier | 296.21 - (42.50 + 160) = **93.71** | 93.71 |
| Stub against it | 177.27 - 93.71 = 83.56 to spare | |
| Stub on the carrier | top 202.50 + 177.27 = 379.77; exposure 379.77 - 153.09 = 226.68 | 379.77 / 226.68 |
| Cuts on the carrier | 1 + floor((379.77 - 296.21) / 76.44) = 2; tips 261.28 then 184.84 (first slice 83.56) | 2 |
| Removed on the carrier | 379.77 - 219.77 = 160.00 (= carrier length, an identity: stub top minus pole = carrier top minus core stop) | 160.00 |
| Left | 219.77 - 202.50 = 17.27 axis / 37.69 surface | 17.27 / 37.69 |
| End to end | 9 cuts; 572.73 + 160.00 = 732.73 removed; 750 - 732.73 = 17.27 left | 9 / 732.73 / 17.27 |

The arithmetic holds. The tip lists in my P3b 1e and in the Engineer's section 5 do not end at the stop (Correction 4). They describe text only and appear in no gameplan line. The Reported line in P2f item 1 states the span, counts, stubs and removed lengths, all correct. The 7 cuts on the stop with a 177.27 stub need the schedule above, whose first slice is 114.10.

### 2.3 Signature

**SIGNED** on the S4 spec and the staged S1 r9 / S3 r8 text. The renderer-dependent items carried to P4 are FIX 1, FIX 2 and the X1 section_true compare O2 (i) and (ii). NOTES N2 to N5 stand as written (P4 and the Designer part list).

## 3. The Topologist

### 3.1 Slit tick form: section sense

- **Sense of the two slits** (DERIVED):
  - theta 112: cos -0.3746, sin +0.9272;
  - theta 262: cos -0.1392, sin -0.9903.

  Both lie at x < 0, behind the cut face seen from +X, so both are hidden in truth. Their marks are dashed, which agrees.
- **Form (a) is a revolution.** It turns the 112 slit by 22 deg about Z into the +u half-plane. The rotation runs from 112 to 90 inside (0, 180), so it never crosses the line x = 0, y < 0, and the side sense is kept.
- **Admission predicate** for each slit mark. This is the K5 mark admission (option A) extended to sub-artist ticks. Each clause gets a Z and a B at P4:
  - (i) sin(theta_slit) x u_drawn > 0. Live values: +0.9272 x 57.40 > 0; -0.9903 x -55.43 > 0.
  - (ii) The line lies inside the collet's drawn hull within 0.05.
  - (iii) The line meets the face at its open end within 0.05: top-open at the top face, z_top 72.00, r 56.80 to 58.00; bottom-open at the floor 40.00.
  - (iv) It is drawn dashed.
- **Bs:**
  - +u line moved to u -57.40 (fires (i));
  - +u as spec at 51.32, 47 to 72 (fires (ii));
  - +u ended at 66.52 (fires (iii));
  - drawn solid (fires (iv)).
- The magnitude rule differs per line: +u is revolved, and -u is the projection r_mid sin(theta), 0.55 short of revolved. The predicate tests sign and containment, so both pass. The admission text states each rule.

**SIGNED, form (a).** The Bs are due at P4.

### 3.2 NOTE

The Designer's R2 (adjacency compared by string) is the class of my 1.3 R2-4. I agree with the family compare in section 1.4 item 4. The orchestrator rules the class repeat.

## Gameplan lines to change

1. Detail 1 common, operator-task table, row at line 186. Supersedes `research/sean/cr_scratch/step1.4_designer_spec_signoff.md` item 1. The text is that item's text, with the 0.75 m stub height added to the first row (Engineer P2f section 5: 160 + 177.27 = 337.27, DERIVED).
Old:
```
| Advance the core for a slice; take the slice off | start | S4 | collet top | slice plane | cutter at rest only | S4-2, V10 |
```
New:
```
| Set a short core: carrier and core (100 mm core 3.3 kg, 260 tall; a 0.75 m stub on the carrier 337.27 tall) into the collet | load (ring parked, tip 1019.84 z_S) | S4, S1, S2 | kneel or stand in the S2 sector (theta 90 +- 45); wing nut backed off (pose R); lower the stack over the collar top 219.84 z_S, hands at 280 to 520 z_S; re-tighten the wings (sweep r 115) | down the holder bore from the sector | fingers cannot enter the 4.5 radial gap at the collar ID; hold the stack upright until clamped (the carrier joint is the weak point) | S4-2, V4, V10 |
| Advance for a slice (advance D, Design Notes 34) | slice_stop sequence | S4, S1 | none: the lift steps the drill down one slice | as the S1 watch row | gear and pinions turning (S1 watch row) | V10, reported advance |
| Take the slice off | park | S4 | slice captured in the drill above the iris, released at park over the base | open | slice falls when the iris opens (N6) | N6, owner Quinn |
| Change a collet (liner option) | load | S4, S1 | as the S1 collet row; the liner comes out upward with the core | wing nut from the sector | as the S1 row | V10 |
```
2. Detail 1.4, insertion after line 321.
Insert after:
```
Cross-review (STOP S4-0, Design Notes 33): The Loftsman (base-stack arithmetic, holder section, spigot radial fit, advance path; (b), (c), (e)), The Topologist (kept-part orientation predicates, section sense, tick admission; (c), (e)); S1 r9 changed rows by both at (e); The Designer reviews the kept parts as drawn.
```
New:
```
Hatch adjacency at P6 (Designer P2r ruling, `research/sean/cr_scratch/step1.4_raisers_recheck_spec.md` section 1.4): S3 r8 and S1 r9 declare `hatch_adjacency_gap` 0.5; the lint compares line families (hatch_family) and in a view without section_class takes every row drawn with a hatched area; remedy order (1) explicit `hatch` on every cut row (default steel refused; S3 shared rows as S4), (2) one_body where the shape text names one part (collet|core_seat, ring|nut_housing_c, ring|motor_mount_c, liftmotor_c|liftmotor_pilot_c), (3) hatch_variant alt on one member of each remaining same-material pair (S3: bearing, pinion_c, anchor_locknut_c steel `++`; frame_upper_c extrusion `**`; S1: receiver `||`, descent_stop `\\\\`); dry run S3 16 to 0, S1 2 to 0 (MEASURED); P6 Bs: S3 receiver variant removed, S3 gear hatch removed, S1 receiver `//`, S1 descent_stop `////`. Designer R1: a B through the K8 call site (S4 figure 1 at P4).
```
