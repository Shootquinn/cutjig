# Step 1.4 P2f, The Engineer: fix pass after the (b) spec sign-offs (Designer P3a FIX 1 to 6, Loftsman P3b FIX 1 to 5)

## Corrections to the brief

1. **Designer FIX 1 and Loftsman FIX 1 cannot close as one value.** The Loftsman assigns the +u slit-tick form to The Designer and The Topologist, and both forms depart from the true projection. The labels are closed. The slit label is anchored on the -u line, which passes its admission in either +u form (u -55.425, z 40.00 to 65.00, inside the hull to 70.625, touching the foot; MEASURED, D9). The +u form goes back with the dry run (section 5).
2. **The hatch-adjacency class is wider in S3 and S1 than the two pairs FIX 2 names.**
   - On the live S3 r7 drawing, the lint (gap 0.5) reads **16 pairs** (MEASURED, `probe1.py`). S3 rows with no `hatch` field default to steel, so receiver, collet, core_seat and holder all draw `\\\\`. The pairs:
     - receiver with collet, core_seat and holder;
     - collet with core_seat and holder;
     - drill_tube with bearing and gear_hub;
     - ring with nut_housing_c;
     - gear with gear_hub and pinion_c;
     - motor23_c with motor_mount_c;
     - anchor_bearing_c with anchor_locknut_c;
     - base_frame, bracket_anchor_c and bracket_guide_c each with frame_upper_c;
     - liftmotor_c with liftmotor_pilot_c.
   - The S1 r8 side view hatches receiver, base_plate and collar `//` from the script (MEASURED, `probe3.py`). Its rows carry no `section_class`, so the lint cannot reach S1.
   - Both are carried by name to P6 (section 5).
3. **The Designer FIX 3 scope read is clean today.** core_750 rests_on core_seat bears 3.00 per side in S3 r7 (capture_end) and in S1 r8 (start, capture_end) (MEASURED, `probe1.py`, `probe4.py`). At load, S1's core sits 58.67 above the seat, and the predicate's pose list excludes load. min_bearing 0.25 would fire on neither record.
4. **The staged P6 set gains one shared row.** washer joins s1, s3 and s4. X1 on the staged set (live s2 added, per Loftsman Correction 4) compares 71 rows and passes. The live set compares 70 rows (MEASURED).
5. **Loftsman FIX 2 is applied in the true-section form.** The window removes the whole +u pocket rim: window r 70.90 to 84.14 over the rim band z 145.59 to 146.39, against the rim r 71.90 to 83.14 (DERIVED, D2). Sean's ruling draws the base stack in true section, and the Loftsman's own O2 (iii) puts plane-dependent features outside section_true. The form goes in a per-spec field `plane_cuts`, so X1 equality of section_true holds. The Designer rules at P2r. Removing the field restores the drafted rim.
6. **Every value-setting edit was dry-run on a scratch copy before the live edit.** The live s4_spec.yaml is byte-equal to the dry-run copy (`filecmp` True). The staged set regenerated from the live s4 is byte-equal to the dry-run staged set (MEASURED).

## 1 FIX table

Dry runs: `D:\Unleashed Robotics\_scratch\cutjig\open14\p2f\dry_p2f.py` and `dry_p2f.json` (D1 to D9). The S4 edit script is `e4.py` (33 edits, each asserting one unique Old). The staging generator is `research/sean/cr_scratch/step1.4_p6_staged/stage.py` (= `p2f/stage2.py`; 25 s1 edits, 28 s3 edits, Old/New in `stage_edits.json`).

| Raiser | FIX | Dry run (MEASURED unless tagged) | Change | Control | Status |
|---|---|---|---|---|---|
| Designer | 1 (tick and root labels) | D5 strings: "12 slits, alternating, 25 long" and "thread 149.58 x 8 RH, 6 turns" | `collet.slits.label {template, keys, on: "-u"}`; `receiver.root.label {template, keys, map: thread.hand right RH}`; thread.hand added to the receiver keys. Template form declared in the header for the P4 renderer | none: the sub-artist label renderer and its K4/K5 reads land at P4 | closed (spec); +u position returned (Loftsman 1) |
| Designer | 2 (hatch adjacency) | D3 in both figures: 0 same-pattern pairs within 0.5 after the change. Without the variants: 3 pairs in figure 1, 5 in figure 2 (equals Designer D2). hatch_alt_issues clean. Patterns: receiver and spigot `\|\|`, liner `--` | spec: `section.hatch_alt {aluminium: "\|\|", plastic: "--"}`, `section.hatch_adjacency_gap: 0.5`; `hatch_variant: alt` on receiver_spigot, receiver and liner; figure_note legend as worded. Code: `cut_hatch` returns the alternate on a hatch_variant row; `hatch_alt_issues` lints hatch_variant (unknown value; material with no alternate); new `hatch_adjacency_issues` (K8, section convention). It runs on a section Axes whose spec declares the gap, skips one_body pairs, and uses the drawn hatch and min_distance | K8-Z19, K8-B97 to B101 | closed for S4. S3 r8 and S1 r9 carried by name (Correction 2) |
| Designer | 3 (O5 bearing) | D4 bearings: carrier on core_seat 3.00; carrier on core_seat_105 0.50; liner 2.50; core_100 on carrier 50.50; collet foot on the floor piece 16.49 (d 105: 13.99). All are >= 0.25, and dz is 0.000 on each | Code: K8 `rests_on` gains `min_bearing`. New `face_spans` and `bearing_width`: the member's bottom-face spans are overlapped with the seat's top-face spans, per side of the member centroid, and the least side is taken. Spec: `min_bearing: 0.25` on the 6 rests_on predicates (collet, collet_105, carrier x2, core_100, liner). carrier\|core_seat_105 source text as worded. reported_items `seat_bearing`, with a checks_s4 reader on the drawn faces (None until drawn) | K8-Z18, K8-B96 | closed. The S4 drawn Z and the Designer's B (carrier at r 49.90 in figure 2) land at P4 |
| Designer | 4 (O3 wing form) | Designer D3 holds with the relief split: the occluders run contiguous from 113.09 to 153.09 (body to 139.09, relief to 145.59, pocket rim to 146.39, plate to 153.09), each with r_out 83.14 = -x_band[1] (DERIVED). The theta 210 window sits at \|u\| >= 30.45 (0.5 r - 5 at r 70.90), off every sight line \|u\| <= 7 (DERIVED) | wing.style hidden; wing.label "-X wing (behind), span" from wingnut.span (D5: "span 230"); wing.admission text with (i) to (iii) and the four Bs; convention.beyond appended; "(open item)" removed from the +X wing reason and from wing.source | none: K8-B74 still refuses a wing past the band. The admission and its Z/B land with the sub-artist renderer at P4 (Topologist signs) | closed (spec); rule at P4 |
| Designer | 5 (O4 follow-ons, staged) | X1 staged (live s2): pass, 71 rows. section_true is equal on receiver, collet, core_seat, holder, wingnut, washer and collar. Holder tie diff 0.0000 on s1 and s4. check_stack exits 0 on staged s1, s3 and s4 | (a) wingnut section_true_note in s4 and in staged s1 and s3. (b) staged S3 wingnut shape to the drawn pieces; plane_cuts, sub_artists [wing, sweep] with wing and sweep as s4; +X wing not_drawn entry and figure_note; part_list names the washer and the sub-artists; wing and window keys added. (c) washer row equal to S4 in staged S3 r8 (cut, plastic) and S1 r9 (notes field), washer z_A 145.09 to 146.39 in all three. holder\|washer C and wingnut\|washer C declared in both | X1 and stack ties on the staged set (no new control: staged files are not run until P6) | closed (staged) |
| Designer | 6 (rubric) | n/a (text) | third V3 line replaced by the V4 (S4) line; V7 (S4, figure 2) added | n/a | closed |
| Loftsman | 1 (+u slit tick) | D9 hull at u 51.322 tops at 66.522. As-spec projected line 47.00 to 72.00: outside the hull. Form (a) u +57.40 (top-face mid-radius, top face r 56.80 to 58.00), 47.00 to 72.00: inside, touches the top face, length 25.00. Form (b) u +51.322 ended at 66.522: inside, length 19.522, does not touch the top face. Max projectable \|u\| at theta 112: 53.777 | `slits.u_form_open` records the open choice; `u` unchanged | n/a | **returned** to The Designer and The Topologist |
| Loftsman | 2 (theta 90 window) | D2: theta k0 = 90; the window covers the rim in r (70.90 <= 71.90, 84.14 >= 83.14) and equals its z band. Windows k1, k2 at 210 and 330, 60 deg off theta 270. Washer to plate-underside contact at 146.39 unchanged on both sides | `plane_cuts: [{piece: pocket_rim, side: "+u", reason}]` on wingnut in s4 and staged s3 (S1 xz: no window in the plane). Header declares the field outside X1. Window keys added. not_drawn entry and figure_note now name only the 210 and 330 windows | none: the renderer reads plane_cuts at P4 | applied; form to The Designer at P2r |
| Loftsman | 3 (relief bore) | D1: body r 74.79 to 83.14 over 97.09 to 139.09; relief r 75.34 to 83.14 over 139.09 to 145.59. Least flange-to-body gap stays 2.75; 3.30 in the relief zone. Every other row's section_true and z extent are unchanged in both figures (31 row-poses) | body split into body + relief in s4 and staged s1, s3; keys nut.relief_r, nut.relief_z | X1 staged pass | closed |
| Loftsman | 4 (skirt profile) | D1: (83.14, 102.09), (95.14, 102.09), (95.14, 104.09), (83.14, 111.09), convex CCW, area 66.000 | skirt as `{poly}` in s4 and staged s1, s3; key nut.skirt_rim | X1 staged pass | closed |
| Loftsman | 5 (slice count, stub) | D6 and the RPT smoke (empty figure set): tip span 496.29 (681.13 to 184.84), **7 slices**, 572.73 removed. Stub on the stop 177.27 (axis) / 197.69 (surface). On the carrier: top 379.77, exposure 226.68, 2 slices, 160.00 removed. Least core on the stop 253.71, on the carrier 93.71 | checks_s4.slice_numbers: slices_075 = floor(span / least slice) + 1; adds first/last tip, removed, stub_075 axis and surface, the stub on the carrier (top, exposure, slices, removed) and min_on_carrier. RPT advance text; spec reported_items advance text; not_drawn entry and figure_note 253.71 to 177.27 | none: RPT carries no threshold | closed |
| Loftsman | NOTE N6 | n/a | receiver.key_offset_deg added to the collet_105 keys | n/a | closed |

Not acted on (P4 or the owner named): Loftsman N2 (grip 23.20 straight chamfer against 22.79 to the lip fillet; reported wording), N3 (S4-2 B1 cause absent), N4 (S4-2 (b) datum read restricted to the plate piece), N5 (off-plane collet rim notches, label window and Rule P notch: Designer part list).

Rule (h) premises of the two new rules:
- min_bearing:
  - premise: member and seat faces are the horizontal edges at each part's own extreme z, and the rests_on z test in the same branch holds them within tol;
  - per-side split at the member centroid: a round row drawn about its axis.
  - Scope: every rests_on that declares the field, in side, plan and section views. Today S4 only, and S1 and S3 read 3.00 (Correction 3).
- Adjacency lint:
  - premise: drawn hatch = material pattern (section convention 1, K8-B57), and section pieces convex for min_distance (K5 convexity guard, LF-4).
  - Scope: section views whose spec declares `hatch_adjacency_gap`. Today S4. S3 r8 and S1 r9 are carried by name (Correction 2).

## 2 Controls added

All 8 controls are in `fixtures/step14_fixtures.py` (P2f section) and `fixtures/manifest.yaml`, check K8.

Pre-change runs used a copy of docs/sketches taken before the first edit (`p2f\prerun`) with the new fixtures and manifest, via `--manifest ... --only` (MEASURED).
- On the pre-change code there is no min_bearing branch and no adjacency lint, and cut_hatch ignores hatch_variant.
- The synthetic fixtures model the absent lint as "no issue" (`hasattr`).

| ID | Planted | Reason substring | Post-change | Pre-change |
|---|---|---|---|---|
| K8-Z18 | S3 core_750 rests_on with min_bearing 0.25 | (clean) | clean, match | clean |
| K8-B96 | S3 core drawn at r 46.50 inside the ledge r 47 to 50, bottom on the seat | "core_750 rests_on core_seat: bearing width 0.000 mm on the seat top face", "needs >= 0.25 (min_bearing)" | fires 1, match | **clean (red)** |
| K8-Z19 | synthetic stack: receiver hatch_variant alt 0.25 from holder; collar\|holder one_body | (clean) | clean, match | clean |
| K8-B97 | receiver variant removed | "receiver\|holder: separate cut bodies with the same hatch '//' 0.25 mm apart" | fires 1, match | **clean (red)** |
| K8-B98 | collar\|holder one_body removed | "holder\|collar: separate cut bodies with the same hatch '//' 0.00 mm apart" | fires 1, match | **clean (red)** |
| K8-B99 | hatch_variant on a brass row | "receiver: hatch_variant declared with no section.hatch_alt for brass" | fires 1, match | **clean (red)** |
| K8-B100 | hatch_variant 'alt2' | "spec error: receiver: hatch_variant 'alt2' (known: alt)", "receiver\|holder: ... '//'" (planted 2) | fires 2, match | **clean (red)** |
| K8-B101 | hatch_variant alt, receiver drawn `//` | "p/receiver: hatch '//' against material aluminium '\|\|'", "receiver\|holder: ... 0.25 mm apart" (planted 2) | fires 2, match | **clean (red)** |

fast.yaml is unchanged: K8 already holds a Z and a B in the fast tier.

## 3 Runs

- `check_sketch.py --controls` (full, live manifest): **488/488 match (Z 110, B 375, smoke 3), 156.2 s at 12 jobs** (159 s with start-up) (MEASURED). That is 480 + 8.
- `--stale`: 3 records, 0 differences; deps 3 exempt, 0 differences; X1 pass, 70 shared rows (MEASURED).
- `check_sketch.py s1 --rev 8`, `s2 --rev 9`, `s3 --rev 7` on the post-change code, and on the pre-change copy:
  - every check line is identical between the two (MEASURED, `run_post_*.txt` and `run_pre_*.txt`);
  - K4 fails on all three under the rule (l) global scope from step 0, the same on both trees. These are the anchors carried to P6 (P2 Correction 3).
  - All other checks pass: S1 18 of 19, S2 17 of 18, S3 15 of 16 lines.
- `check_stack.py` exits 0 on live s4 and on staged s1, s3 and s4.
- S4 checks on an empty figure set: S4-1, S4-2 and S4-3 fail, cause absent. RPT values are as in the Loftsman FIX 5 row. needs_drawing items, seat_bearing included, read None.
- Staged X1 (`step1.4_p6_staged/x1dry.py`, live s2 added): pass, 71 rows; section_true equal on 7 rows; ties 0.0000.

## 4 SHA-256

Before: `p2f\sha_before.json`. After: `p2f\sha_after.json` (88 files before, 90 after; 78 unchanged). Prefixes below.

| File | Before | After |
|---|---|---|
| docs/sketches/s4_spec.yaml | FFFFC8CC3C35 | A4EA84D66393 |
| docs/sketches/sketch_common.py | 46DEB3ABD479 | 1F273892D3AB |
| docs/sketches/checks_s4.py | 4F0F17410D94 | 84E7D6484C22 |
| docs/sketches/fixtures/step14_fixtures.py | 047F81240F97 | C2D0C16C2601 |
| docs/sketches/fixtures/manifest.yaml | 293B802B8AD8 | E23D8558F7C1 |
| step1.4_p6_staged/s1_spec.yaml | 6BEA4572F713 | 3A5E8B462CA8 |
| step1.4_p6_staged/s3_spec.yaml | 961AF86E1D15 | EF2EAB6E2852 |
| step1.4_p6_staged/s4_spec.yaml | 4CD1F364E0B2 | B579CE29EA3A |
| step1.4_p6_staged/stage.py | 92DB8C459452 | 4918FE83C102 |
| step1.4_p6_staged/x1dry.py | 2D5C262177C0 | 43B7B308EF1A |
| step1.4_p6_staged/stage_edits.json | absent | 15AF99A85AFC |
| step1.4_p6_staged/x1dry.json | absent | F7D02B2300E8 |

No unexpected difference.
- s1_spec.yaml, s2_spec.yaml, s3_spec.yaml, proposed_params.yaml and every accepted record, PNG and committed controls_results.json are unchanged.
- No key read by S1 r8, S2 r9 or S3 r7 moved: params and overlay are untouched.

## 5 Items returned or sent to Sean

Returned:
1. **Loftsman FIX 1 (+u slit tick form), to The Designer and The Topologist.** Form (a) is schematic at u +57.40, 47.00 to 72.00, touching the top face. Form (b) is the projected u +51.32 ended on the chamfer edge at 66.52 (19.52 long), with the admission text changed to "ending on the hull boundary". Both lie inside the drawn hull, and the as-spec line does not (D9). The Engineer writes the chosen form at P2r or P4. The slit label is anchored on the -u line and stands in either form.
2. **Loftsman FIX 2 form, to The Designer at P2r.** The true-section form (plane_cuts, +u rim absent) is applied. The alternative is the rim drawn with a drafting reason.
3. **S3 r8 and S1 r9 hatch adjacency, to The Designer before P6 (FIX 2 scope).**
   - 16 same-pattern pairs on the S3 r7 drawing (Correction 2). Most come from rows with no `hatch` field that default to steel.
   - S1's script hatches receiver, base_plate and collar `//` in the side view. At P6 the specs that draw these rows declare the gap and the patterns, or the scope stays listed.
4. **Orchestrator.** Design Notes 34 quotes "the last 253.71 mm stub". The corrected stub on the stop is 177.27 (axis) and 197.69 (surface). 253.71 is the least core that takes a cut on the stop. The ruling itself (a carrier for the stub) is unchanged.

Advance D with carrier C and the corrected stub (orchestrator note):
- **The carrier takes the stub.** The least core that takes a cut on the carrier is 253.71 - 160 = **93.71** (DERIVED). The stub of 177.27 clears it by 83.56.
- **On the carrier:**
  - stub top 202.50 + 177.27 = 379.77 (axis), exposure 379.77 - 153.09 = 226.68 against 143.12;
  - first cut tip 379.77 - 111.37 = 268.40, then 191.96, within the tip window down to 184.84: 2 slices, 160.00 removed (axis);
  - left on the carrier 17.27 (axis) to 37.69 (surface), the same waste as the drawn 100 mm core.
- **The 0.75 m core end to end:** 7 + 2 = 9 slices, 732.73 removed on the axis (DERIVED; MEASURED through checks_s4.slice_numbers).
- **Checks:** none moves. S4-2 asserts the drawn 100 mm configuration (exposure 149.41, margin 6.29, grip bands 42.50 to 65.70 and 42.50 to 68.20), and the stub case is reported arithmetic.
- **Reported items that move:**
  - the RPT `advance` value and the spec reported_items text;
  - the not_drawn entry and the figure_note (253.71 to 177.27);
  - the gameplan Reported line (item 1 below).
- **Values:** no design value changes, so nothing goes to The Designer as a value.
- **For the Designer's operator row (P3a gameplan item 1).** A 0.75 m stub on the carrier is a 337.27 stack (carrier 160 + stub 177.27), against the 260 the row states for the 100 mm core. This is row text and needs no new value.

Sent to Sean: none.

## 6 Gameplan lines to change

1. Detail 1.4, Reported line (line 318). Supersedes `research/sean/cr_scratch/step1.4_loftsman_spec_signoff.md` item 1 and `research/sean/cr_scratch/step1.4_engineer_spec.md` item 5.
Old:
```
Reported: exposed length of a 100 mm tall core against `core.min_exposed` 143.12 (Q10); collet length options (Q5); sacrificial collet or liner (Q6).
```
New:
```
Reported (spec reported_items, RPT): 100 mm core top against the collar top (142.50 on the stop, 17.34 below; 302.50 on the carrier) and its exposure against `core.min_exposed` 143.12 (-10.59 / 149.41); minimum core on the stop 253.71 (nut-plate datum; 260.46 collar-top datum), the least core that takes a cut on the stop (93.71 on the 160 carrier); collet grip 23.20 (d 100, straight chamfer drawn; 22.79 to the lip fillet); advance D: least slice 76.44 axis / 56.02 surface; 0.75 m core tip span 496.29 (681.13 to 184.84), 7 slices, 572.73 removed, stub on the stop 177.27 axis / 197.69 surface, moved onto the carrier: top 379.77, exposure 226.68, 2 slices, 160.00 removed, 17.27 / 37.69 left; 100 mm core on the carrier 1 slice, stub 17.27 / 37.69; core-seat bearing widths 3.00 (figure 1), 0.50 carrier and 2.50 liner (figure 2), 8.15 MPa with all of F_stall + W on the carrier annulus; carrier-joint shear 50.9 kPa (liner 6.37); collet length options Delta 0 / 25 / 50 (Q5, kept 32 mm); liner D = d + 5, wall 2.0 (Q6); cut-case seat as drawn; kept-part axial forces (as S3 r7).
```
2. Detail 1.4, check table row S4-3 (line 316). Supersedes `research/sean/cr_scratch/step1.4_engineer_spec.md` item 4.
Old:
```
| S4-3 | Orientation of the kept parts (K8 predicates in the S4 spec): collet taper sense per `cone.alpha`, narrow end as in ASSEMBLY.md; wing nut above holder; washer between nut and holder; receiver floor at the bottom | Fixture in correct sense | Collet flipped end for end | ASSEMBLY.md; critical-path 7.1 (backcap failure) |
```
New:
```
| S4-3 | Orientation of the kept parts (K8 predicates in the S4 spec): collet taper sense per `cone.alpha` on the cone piece, foot ring on the receiver floor, narrow end up as in ASSEMBLY.md; holder cone narrowing up; collet bore vertical (S4-d, Design Notes 34); wing nut above the holder flange; washer between the flange and the nut plate; receiver floor at the bottom; core and carrier upright; every rests_on (collet foot, carrier, core, liner) with radial bearing `min_bearing` 0.25 on the seat face (Designer P3a FIX 3: carrier 3.00, carrier 0.50 and liner 2.50 on the d 105 ledge) | Fixture in correct sense | Collet flipped end for end; washer above the nut plate; wing nut below the flange; collet bore drawn parallel to the cone (S4-d); carrier drawn at r 49.90 in the liner figure (bearing 0) | ASSEMBLY.md; critical-path 7.1 (backcap failure) |
```
