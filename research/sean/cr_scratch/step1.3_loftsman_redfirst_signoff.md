# Step 1.3 (c) section coordinates and cross-record S3-3 (P5L), The Loftsman

Date 2026-11-26. Read: `step1.3_engineer_redfirst.md` (all sections); `docs/sketches/checks_s3.py`, `check_sketch.py` (sym_lint, x1_lint, stale_records, stale_diffs, run_sketch), `sketch_common.py` (reflect_record, reflect_stack, axes_contexts, sub_spec, per_axes, spec_keys), `fixtures/s3_fixtures.py`, `s3_spec.yaml` (chains, s3_checks, screw-set, base and frame rows), `s1_spec.yaml` and `s2_spec.yaml` (base_plate, receiver, base_frame, screw-set rows), `sketch_loader.py` (Params.get, hashes); `build_parts/receiver.py`, `base.py`, `tray.py`, `assemble_lib.py` (base_shape); `params.yaml` receiver and base leaves; my files `step1.3_loftsman_spec_signoff.md` and `step1.3_loftsman_spec_resign.md`. Section screw: c (theta 270, YZ plane).

Every probe ran on a copy of `docs/sketches/` at `C:\Users\UR\AppData\Local\Temp\claude\eba575d6463ef2d6\6efaddfb-5e83-4849-8803-49d5d7303110\scratchpad\p5l\sk\`. The scripts are in `C:\Users\UR\AppData\Local\Temp\claude\eba575d6463ef2d6\6efaddfb-5e83-4849-8803-49d5d7303110\scratchpad\p5l\probes\`:
- `k67_probe.py`: K6 and K7 in the section.
- `s32_probe.py`: S3-2.
- `s33_probe.py`, `s33b_probe.py`, `s33c_probe.py`: S3-3 resolution, veto, face test and branches.
- `sym_probe.py`, `cov_probe.py`: SYM and F4.
- `f1_dry.py`: the F1 remedy dry run.

Nothing under `docs/sketches/` was edited. Tags: MEASURED (read from a run here), DERIVED (hand arithmetic), DECLARED (spec, params or ruling).

## Corrections to the brief

1. **The veto is implemented per link. The same physical pair therefore passes in chains a and b while chain c vetoes it.**
   - On the signed chains (S3 receiver certifier kept, post-P6 specs, fresh records), S3-3 reads n = 1: chain c receiver|base_plate, S3 K7 state F (MEASURED).
   - Chains a and b list only "S1 base_plate|receiver C" for that link, so they pass on the record.
   - There is one receiver and one plate, so the cut loop of every screw passes through that one contact. FIX 1.
2. **F1 is a design gap, and the drawing shows it correctly.** The kept receiver has no axial seat on the base plate in any representation (section 6).
   - S1 r7 certifies the pair C because S1 draws the plate as a slab with no hole (`depth` ±footprint_y/2; the hole appears only in the shape text) and the receiver standing on its top (z_min `base.plate_thickness`).
   - The S3 section K7 is also red on the pair: 1 issue, distance 0.200, state F, on `s3_fixed` (MEASURED). P6 cannot reach a green K7 without a declaration change.
3. **"Equal in keys" was my wording at (b) R1. It certifies nothing, and I withdraw it** (section 5).
   - Per-row `keys` lists have no per-row meaning in the harness. `spec_keys` takes their union over the whole spec.
   - A record's `keys_read` also holds every key `Params.get` returned (sketch_loader l.163).
   - S1 r7 carries 11 keys that appear in no row list, among them `frame.end_x`, `stop.start_z` and `wingnut.body_od` (MEASURED).
4. **K6 in the section asserts z extents only.** It reads "48 z_rule(s) match drawn extents within 0.05 mm" (MEASURED). The u centre is held by K8 (TP-3, or the section_u piece test). So the "centre in u, z" of task 1 is split across K8 and K6. Both are given in section 1, with the u values checked against the reflected stack and the drawn pieces.

## 1 K6 and K7 in the section plane

**The map as implemented.** `reflect_record` reflects the plan record across x = y:
- x' = plan y = u.
- y' = plan x = depth (positive toward the viewer at +X).
- theta' = 90 - theta and rot' = -rot.

A radial footprint centred at (r cos θ, r sin θ) maps to (r sin θ, r cos θ) = (r cos θ', r sin θ'), and a direction θ + rot maps to θ' - rot. That is the reflection, exact (DERIVED). The depth band is the place x extent, the plan_poly x extent, or the spec depth hulled with place x. This closes NOTE 5 of my (b) sign-off: check_stack's `depth` (place y) is no longer used as depth in the section.

Fixture `s3_fixed`, capture_end. Hand values are DERIVED from the overlay. Harness values are MEASURED: the reflected stack record, the drawn pieces in the section Axes, and K6.

| Row | Hand u | Reflected x' (theta') | Drawn u | Hand z_S | Drawn z_S (K6) | Hand depth | Harness depth |
|---|---|---|---|---|---|---|---|
| screw_c (round, r 160, θ 270, hw 6) | -166.00 to -154.00 | -166.00 to -154.00 (-180) | -166.00 to -154.00 | 325.00 to 1225.00 (265 + 60, 1165 + 60) | same, pass | ±6.00 | ±6.00 |
| anchor_c (radial square 42, θ 270) | -181.00 to -139.00 | same (-180) | same | 325.00 to 355.00 | same, pass | ±21.00 | ±21.00 |
| pinion_c (radial, θ = pinion.angle[0] = 90) | r_in = 96.54 - (83.33/20) sin 18.435° = 95.22 to r_heel 125 + hub 15 = 140.00 | 95.22 to 140.00 (0) | 95.22 to 140.00 | not hand-computed | 393.22 to 484.46, pass | ±91.24/2 = ±45.62 | ±45.62 |
| standoffs_c (plan_poly, beyond) | -160 ∓ 15.50 ± 2.75: -178.25 to -172.75 and -147.25 to -141.75 | plan_y -178.25 to -141.75 | -178.25 to -141.75 | 229 to 265 z_A (face = 265 - coupling_length 36): 289.00 to 325.00 | same, pass | -31/2 ± 5.5/2 = -18.25 to -12.75 | -18.25 to -12.75 |
| coupling_c (round, hw 9.5) | -169.50 to -150.50 | same (-180) | same | 303.00 to 323.00 | same, pass | ±9.50 | ±9.50 |

Signs:
- screw_c at θ 270 lands at u < 0, and pinion_c at θ 90 at u > 0, as my (b) map states.
- The standoffs lie at x < 0, that is, behind the plane as seen from +X. That agrees with their `section_class: beyond`.

K6 section Axes: PASS, 48 z_rules within 0.05 (MEASURED). K7 entries along the plane normal (MEASURED) against hand (DERIVED):

| Pair | State, basis | Value | Hand |
|---|---|---|---|
| coupling_c\|standoffs_c (F) | depth-separated, depth band | gap 3.25 | 12.75 - 9.50 = 3.25 |
| anchor_c\|standoffs_c (C) | C, XZ exact | 0.00, overlap 0.00 | standoff top 325 = block bottom 325 z_S; the bands overlap ([-18.25, -12.75] inside ±21) |
| screw_c\|anchor_c (F) | F, XZ exact | 2.00 | cover bore r 8 - body r 6 = 2.00 |

The depth-band rule (LF-1 form) reads x in the section. Signed.

## 2 S3-2 as implemented

Formula (checks_s3 `s3_2`, `euler`, `loads`):
- P_cr = π² E I / (K L)², with I = π d_r⁴ / 64.
- L = the spec expression `jackscrew.guide_bearing_z - jackscrew.anchor_bearing_z`.
- K = `jackscrew.end_factor_floating`; SF = `jackscrew.buckling_sf`.
- Margin = P_cr / per-screw force for each case in `s3_checks.S3-2.cases` (static, capture_lift, retract_bind, stall_up).
- The cut case is in tension and is correctly absent from the list.
- The drawn span (centres of the drawn anchor_bearing_c and guide_bearing_c pieces) must equal L within 0.05.

| Quantity | Hand (DERIVED) | Harness (MEASURED) |
|---|---|---|
| I (d_r 8.5) | 256.24 mm⁴ | 256.24 |
| L_t | 1150 - 280 = 870.00; drawn centres (272 + 288)/2 and (1146 + 1154)/2 | 870.00, drawn 870.00 |
| P_cr (E 200000 N/mm², K 0.7) | 9.8696 x 200000 x 256.24 / 609² = 1363.8 N | 1363.8 |
| W | 24.25 x 9.81 = 237.89 N | 237.89 |
| static | 237.89 / 3 = 79.30; margin 17.20 | 79.30 |
| capture_lift | (237.89 + 10.4 x 9.81) / 3 = 113.31; margin 12.04 | 113.31 |
| retract_bind | min((237.89 + 300) / 3, 343.18) = 179.30; margin 7.61 | 179.30 |
| stall_up | F_stall at mu 0.15 = 343.18; margin **3.97** | 343.18, least 3.97 |
| S3-2-B1 (d_r 6.2, span 850) | I 72.53, P_cr 404.4; retract 2.26, stall 1.18 < 3 | fires 2, as the Engineer reports |

Silent passes:
- An empty `cases` list raises at `min()`, and a case missing from `per_screw` raises KeyError. Neither is caught by `_run`, so the run errors. Neither passes.
- A non-positive force gives a negative margin (fails) or ZeroDivisionError.
- The margin branch carries S3-2-B1. The Engineer's deletion test applies, because the B fires on the pre-change code.

**The span branch has no B.** Moving the drawn guide_bearing_c up 10 makes S3-2 read "drawn span 880.00 against 870.00 (spec)" (MEASURED). No S3-2 control plants it, so deleting the branch would pass all three S3-2 controls. K6 catches the same plant independently (off 10.00, MEASURED). The span read is still the premise of S3-2 (the drawn mounting is the computed column), so it needs its own B. FIX 4.

## 3 S3-3 as implemented

**Resolution.**
- `_records` calls `check_sketch.stale_records(docs, wip)`, which gives, per sketch, the highest-rev record in `ctx.records_dir` that is `accepted` and has no `superseded_by`. Each record is keyed by its `sketch` field (S1, S2).
- `stale_diffs` compares the record's `keys_read` with live params and overlay, and any difference strips the record of certifying power.
- `run_sketch` sets `records_dir` from `--docs-dir` (default docs/sketches/).
- On the live tree the records are S1 r7 (3 differences: lead, nominal, coupling_length) and S2 r5 (2 differences). So S3-3 can certify nothing from records until S1 r8 and S2 r9 are accepted, as ruled at (b).
- Certifiers read the K7 entries at the section figure pose (capture_end). Both records carry capture_end entries (MEASURED: poses load, start, capture_end, park and swept).
- Every certifier's pair id equals its link's pair (0 differ, MEASURED). The check reads the link pair. The state word in the certifier string goes unread, and any of C, z-contact or plan-contact passes.

**Controls (MEASURED, my runs).**

| Control | Fires | Reason |
|---|---|---|
| S3-3-Z | clean, 51 links | declared links and the a, b symmetry links listed |
| S3-3-B1 (member c 1 mm up) | 1 | chain c base_frame\|frame_upper_c, S3 section K7 F. S2 certifies the pair; the veto opens it |
| S3-3-B2 (receiver\|holder absent from S1) | 3 | chains c, a, b: pair absent |
| S3-3-B3 (S1 keys_read lead 8) | 14 | every link that S1 alone certifies: stale |

The stale premise is enforced inside the check, and the B controls reproduce a missing pair and a stale record. Branches with no S3-3 B (MEASURED with planted cases):

| Branch | Plant | Fires |
|---|---|---|
| record state not C | S1 collet\|holder state F | 3 (chains c, a, b) |
| SYM fails inside S3-3 | x1_exempt on S3 anchor_b in the post-P6 specs | 8 (the a and b screw-set links) |
| a c link between counterparts open | nut_housing_c drawn 1 down | 7 (c nut_c\|nut_housing_c; a and b links by symmetry) |

FIX 5 adds these as B controls.

**Named faces.** `_face_of` reads the neighbour entry's `face {z}`. The three faces of my re-sign FIX 8 are present and read:
- anchor_c → anchor_bearing_c at 288;
- anchor_bearing_c → anchor_locknut_c at 272;
- nut_housing_c → nut_c at the counterbore shoulder.

`_face_issue` accepts an overlap in u of more than -0.05, so a face of zero width passes. Plant: the anchor cover's bore widened to the bearing OD (cover pieces -181 to -173 and -147 to -139 at 348 z_S), so the cover meets the bearing top only at u = -173 and -147. Result: S3-3 clean, 51 links (MEASURED). K7 still reads C, through the radial bore face. A corner is not an axial seat. FIX 2.

**Symmetry range (NOTE 1).** For an a or b link, the c links that must pass run from the first c link containing x_c to the last c link containing y_c.
- anchor_a|screw_a therefore requires c links 9 to 13. The counterpart path is links 10 to 12 (anchor_c, anchor_bearing_c, anchor_locknut_c, screw_c).
- The range is sound, because it demands more. It misreports, though. In the nut_housing_c plant, screw_a|nut_a reads open while screw_c|nut_c passes.
- Exact range: with row positions p(r) along chain c (p(r_i) = i for link i = [r_i, r_i+1]), the counterpart links are p(x_c) to p(y_c) - 1.

## 4 The veto rule (Correction 3 of P4): signed, amended to the pair

**Rule.** A pair that a chain link certifies with "S3 x|y" is judged by this run's section K7 in every chain where the pair occurs. If that test reads a state outside C, or a named face fails, the pair is open in every such chain, whatever a record certifies.

**Premise.** The section is a true cut through x = 0, and both rows of an S3-certified pair are drawn there as their true cut. A side-view or plan record projects and simplifies: the S1 slab without its hole, footprints that circumscribe. Where the true cut and a record disagree, the true cut governs.

The rows of the 13 S3-certified pairs (MEASURED from the spec) are drawn as follows:
- section_u: base_plate, base_frame, frame_upper_c, anchor_c, anchor_bearing_c, anchor_locknut_c, screw_c, nut_c, nut_housing_c, ring.
- section: core_seat, receiver, bearing.
- An axis-Z solid cylinder: core_750.
- A radial prism whose radial direction lies in the plane: bracket_anchor_c, at θ 270.

A footprint centred on x = 0 and symmetric about it is its own cut. A footprint off the plane is not.

**Premise check (FIX 3).** S3-3 lint: every row of a pair named by an S3 certifier carries `section_u` or `section`, or a place footprint centred on x = 0 (|r_c cos θ| <= 0.05) and symmetric about it (round, or radial at θ 90 or 270). Otherwise it is a spec error.
- Z: the live spec, with 15 rows passing.
- B: one S3-certified row with its section_u removed and its theta moved off the plane.

**Why per pair (FIX 1).** The S1 C on receiver|base_plate comes from the hole S1 leaves undrawn. That holds for every chain the pair is on. Measured on the signed chains: n = 1, and n = 3 is required. B: the signed chains (S3 receiver certifier kept, fresh records). It fires 3 after the fix and 1 today.

## 5 SYM as implemented, and F4

**As implemented** (`check_sketch.sym_lint`):
- Families: anchor, anchor_locknut, screw, nut, nut_housing.
- In each spec, each a and b row is compared with the c row (or a with b where there is no c row) on z_rule, place and keys, with `jackscrew.angle[n]` normalised.
- Each theta must name its own index (a 1, b 0, c 2).
- No x1_exempt on those rows.

Live: 10 issues (MEASURED). 3 are the S3 anchor exemptions. 7 are key lists:
- S1 screw_a lists `jackscrew.length` (its label key) and screw_b does not.
- The S3 anchor_c, screw_c and nut_housing_c lists carry the section_u keys (bearing, journal, nut and screw leaves) that the inset a and b rows lack.

**Ruling on F4: SYM compares z_rule and place. Keys are withdrawn from the comparison. P6 makes no key-list edit for SYM.**

Premises:
- The symmetry premise is geometric: the a and b rows are the c row rotated, so their footprint (place) and their heights (z_rule) must be equal after the index swap. Those two fields are what check_stack evaluates, and so they are what K6, K7 and K8 read.
- Every key that place and z_rule read is in the record's staleness scope whatever the row lists say. `keys_read` = `spec_keys(spec)` ∪ `P.accessed`, and `Params.get` records every key evaluated (sketch_loader l.163).
- Evidence: S1 r7 carries 11 keys that come from `P.accessed` alone (MEASURED).
- So if place and z_rule are equal after the swap, the geometric keys are equal too.
- Keys outside that subset are read by fields only a c row has (section_u) or by a label on a home row (screw_a `jackscrew.length`, S1). They describe no a or b geometry.

Measured under the ruled fields (SYM_FIELDS = z_rule, place, run on the copy):

| Case | Result |
|---|---|
| live specs | 3 issues (the S3 anchor exemptions), clearing at P6 |
| post-P6 state (S3 anchor place on the S1 and S2 anchor rows, exemptions removed), key lists as signed | pass, 18 row pairs |
| same state, keys still compared | 7 issues (the lists above) |
| SYM-B1, B2, B3 | each fires 1, unchanged |

No B control depended on keys.

The coverage alternative (each row lists every key its place and z_rule read) would fail S1 anchor_a and anchor_b (angle, nut_flange_od and pitch_radius missing) and S1 nut_a and nut_b (MEASURED, `cov_probe.py`). The comparison would buy nothing that `P.accessed` does not already give.

**Premise check:**
- SYM-Z2: the post-P6 specs with the signed key lists pass (18 pairs, MEASURED above).
- SYM-P (Z): on S1, S2 and S3 runs, `keys_read` contains every key referenced by place and z_rule of every SYM row.
- SYM-P (B): `keys_read` built from `spec_keys` alone (P.accessed dropped), with one geometric key removed from every row list. The lint fires.

`_post_p6_specs` drops its key-union step, so SYM-Z certifies the state P6 will actually produce. FIX 6.

Composition: SYM compares rows within one spec, and X1 compares the same row id across specs. Once no x1_exempt remains, every a and b row in every spec equals S3's c row in place and z_rule. That is the full R1 premise.

## 6 F1: receiver spigot 0.20 clear of the plate hole, no seat

**Confirmed.**
- On `s3_fixed`, K7 reads base_plate|receiver C: distance 0.200, overlap 0.000, state F (MEASURED). By hand: receiver spigot r 80.00 against hole r 80.20, at 72 z_S.
- On the signed chains, S3-3 vetoes the link in chain c (MEASURED).

The kept geometry:
- `build_parts/receiver.py`: the spigot r = `receiver.spigot_od / 2` = 80 is the receiver's largest radius, from z_bot = datum A (z_A 0) to the shoulder, where the profile steps in to the thread minor r 72.29. No face of the receiver projects past r 80.
- `base.py` cuts the hole at r 80.2.
- `assemble_lib.base_shape`: "receiver and plate stay two solids (0.2 radial gap, A3b spigot fit)".
- No row of S1, S2 or S3 lies under the receiver bottom inside r 80.2. The base frame rails are at |u| 244 to 304. In S2 the end members are at x ±232 and the plate supports at x ±112. The tray (`tray.py`) sits on the plate top with a hole of r 81.2.

The cut-case load path from receiver to plate therefore has no axial face. ASSEMBLY.md states the receiver underside force on the plate is 0, which held for the old loop. Under the powered lift (Design Notes 16) it is false.

**P6 spec remedy (dry run, `f1_dry.py`, post-P6 specs, fresh records, MEASURED):**
1. S3 `base_plate` neighbour `receiver`: class C becomes G, g_min 0.10, source "A3b spigot fit 0.20 radial (assemble_lib base_shape); gameplan S4-a; Loftsman 1.3 (c) P5L F1". Dry run: K7 section clean, 269 tests; the pair reads distance 0.200 against 0.10.
2. `chains` a, b and c, link [receiver, base_plate]: the certifiers become `["S3 base_plate|receiver"]`. "S1 base_plate|receiver C" is struck, because S1 draws the plate without the hole and the receiver on its top, so its C is that simplification. Dry run: S3-3 red 3 (chains a, b and c, S3 section state F), and every other link closes.
3. P6 draws no seat and drops no certifier. No part carries a seat, and dropping the certifier would close a loop that is open. S3-3 stays red on receiver|base_plate. P6 lists it as an open item. **S3 cannot be accepted until Sean rules on a seat.**
4. The decision goes to Sean through the Designer, and to Quinn with B2-7 (N5: the kept parts carry the cut reaction). The candidates are design changes, not values P6 sets:
   - (A) A receiver shoulder above the plate top (the kept receiver changes). It meets the tray floor, which stands on the plate top with hole r 81.2, unless the tray hole changes with it.
   - (B) A support under the receiver bottom at datum A: a base-frame cross member, or a disc under the hole. It must keep the debris hole r 40 open.
   - (C) A stepped plate hole bearing on a reduced receiver foot (the kept receiver changes).
   - Each needs a face of positive width in the section and a dry run.
5. The S1 declaration (C, slab) stays until S4-a draws the hole break, as planned at l.650.

## 7 Findings

**FIX 1 (veto per pair).** A pair named by any "S3 x|y" certifier is judged by the section in every chain where it occurs, and a failing test opens it in each one. B: the signed chains fire 3 (today 1, MEASURED). The F1 remedy above lists the S3 certifier on all three links anyway. The rule covers the next pair that is listed on one chain only (ring|bearing is S3-certified on c only).

**FIX 2 (face width).** `_face_issue` requires the two horizontal edges at the face z to overlap in u by more than TOL_Z (0.05). Today it accepts > -0.05.
- B: the anchor cover meeting the bearing at its corner only. It fires on chain c anchor_c|anchor_bearing_c, and on the a and b links whose counterpart range spans it. Today it is clean (MEASURED).
- The drawn widths are 4.0 at 272, 5.0 at 288 and 9.5 at the shoulder (re-sign, DERIVED), so the Z stays clean.

**FIX 3 (veto premise).** The true-cut lint of section 4, with its Z (15 rows) and B.

**FIX 4 (S3-2 span branch).** S3-2-B2: guide_bearing_c drawn 10 above its row. It fires 1, "drawn span 880.00 against 870.00 (spec)" (MEASURED).

**FIX 5 (S3-3 branch Bs).** Three B controls, with the counts MEASURED:
- an S1 record state not C: 3;
- SYM failing inside S3-3: 8;
- a c link between counterparts open: 7, which becomes 3 once NOTE 1's exact range lands.

**FIX 6 (SYM fields).** SYM_FIELDS = (z_rule, place) per section 5.
- The SYM-Z2 and SYM-P Z and B are added.
- `_post_p6_specs` loses its key union.
- The `sym_lint` docstring and the gameplan SYM row drop "keys".

**NOTE 1.** Exact symmetry range, p(x_c) to p(y_c) - 1 (section 3). The current range is sound and misreports.

**NOTE 2 (record currency is keys only).** `stale_diffs` compares `keys_read`. A record carries `files_sha256` of params and overlay only (`Params.hashes`). A spec-text edit that changes no key value, for example the S1 anchor place to the 42 square, leaves the old record certifying. The order ruled at (b) (S1 r8 and S2 r9 accepted before S3) covers P6. For later sketches, the record should carry the spec SHA-256, and S3-3 should compare it.

**NOTE 3 (F5, inset K7).** In the inset, screw_c in nut_housing_c and in anchor_c is a plan nesting. S2 declares those pairs N (s2_spec l.629, l.840). In the inset they should be N, as in S2, and F stays in the section, where the bores are drawn (2.00 and 5.50 MEASURED). `sub_spec` carries no per-Axes neighbour class today. The Engineer adds `axes` on neighbour entries, or the inset pair takes plan bores.

**NOTE 4.** The face test does not order the faces (which piece is above). K6 holds each row's z band, so an inverted pair fails there first.

**Verdict: FIX (6 items: FIX 1 to 6).**
- Signed as implemented: K6 and K7 in the section plane (section 1); S3-2 formula, inputs and per-case arithmetic (section 2); S3-3 record resolution and stale premise (section 3); SYM within-spec form with the exemption and theta-index branches (section 5).
- The veto rule is signed, amended to the pair (FIX 1), with a face width (FIX 2) and its premise check (FIX 3).
- F4 is ruled: z_rule and place, no key-list edits at P6 (FIX 6).
- F1 is confirmed as a design gap. The P6 remedy is a G 0.10 declaration plus S3-only certifiers on all three chains, with S3-3 red until Sean rules on a seat.
- I re-check FIX 1 to 6 with the probes above and sign without re-reviewing the other sections.

## Gameplan lines to change

1. l.288 (S3-3 row, rule column).
```
Old: symmetry premise lint (anchor, anchor locknut, screw, nut, nut-housing rows; P4; Loftsman 1.3 (b) R1), K7 C |
New: symmetry premise lint (anchor, anchor locknut, screw, nut, nut-housing rows equal in z_rule and place with the angle index swapped, keys not compared; P4; Loftsman 1.3 (b) R1, 1.3 (c) P5L F4); a pair an S3 certifier names is judged by the section K7 in every chain it occurs in and a failing section test opens it there whatever a record certifies (premise: S3-certified rows drawn as their true cut, section_u, section, or a footprint centred on and symmetric about x = 0, linted); a named face needs an overlap in u above 0.05 (Loftsman 1.3 (c) P5L FIX 1 to 3), K7 C |
```
2. l.287 (S3-2 row, B column). Apply after P4 item 19, whose new text ends with the old fragment below.
```
Old: retract 2.26 and stall 1.18 against SF 3) |
New: retract 2.26 and stall 1.18 against SF 3); S3-2-B2 guide bearing drawn 10 above its row, drawn span 880.00 against 870.00 (Loftsman 1.3 (c) P5L FIX 4) |
```
3. The SYM row inserted by P4 item 16 (after l.144).
```
Old: rows of a and b equal the c row (or each other) in z_rule, place and keys with the angle index swapped
New: rows of a and b equal the c row (or each other) in z_rule and place with the angle index swapped (keys not compared: keys_read holds spec_keys and every key check_stack reads, so equal place and z_rule give equal geometric keys; Loftsman 1.3 (c) P5L F4)
```
```
Old: SYM-Z the three specs in the post-P6 state (18 pairs)
New: SYM-Z the three specs in the post-P6 state (18 pairs); SYM-Z2 the same with the key lists as signed; SYM-P keys_read covers every key read by place and z_rule of every SYM row, B with P.accessed dropped
```
4. l.650 (S4-a row).
```
Old: receiver\|base_plate becomes G 0.10 | 1.4 (S4) |
New: receiver\|base_plate becomes G 0.10 (S3 declares G 0.10 from 1.3 (d); the kept receiver has no axial seat on the plate (spigot r 80 is its largest radius, hole r 80.2, nothing under it), so the S3-3 cut loop is open at receiver\|base_plate in chains a, b, c until Sean rules on a seat; S1 base_plate\|receiver C struck from the chains; Loftsman 1.3 (c) P5L F1) | 1.4 (S4) |
```
