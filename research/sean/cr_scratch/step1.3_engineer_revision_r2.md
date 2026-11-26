## Corrections to the brief

1. **S1 r9 and S2 r10 are not opened.** No finding changes their pixels. S1 r8 and S2 r9 rebuilt on the r2 harness are pixel-equal to `wip/s1_pose_{load,start,capture_end,park}_r8.png` and `wip/s2_plan_r9.png` (`numpy.array_equal` True on all five, MEASURED). Both were re-run on the r2 harness as the same revision: S1 r8 19/19, S2 r9 18/18 (MEASURED). K4 (i) passes on both as drawn.
   - The S3 leader fix (leader leaves the text edge facing the anchor) is an option of the placer, `edge_leaders`. S3 turns it on. S2 keeps the default.
2. **S3 r2 cannot be all green.** Three checks stay red. None is a drawing defect the Engineer may fix.
   - K4 (1): D1, the sync_callout label text, is a Designer value.
   - K8 (2): TP1.3-12 and TP1.3-14. Each new rule reads a Designer decision that is still open.
   - S3-3 (7): S1 r7 and S2 r5 are stale records. ORCH-B turns this green. Dry run with S1 r8 and S2 r9 marked accepted: S3-3 pass, 48 links (MEASURED).
3. **The chain count is now 48 links, from 51.** This follows TP1.3-10 (a): the base route runs core, core seat, collet, receiver. collet|holder and holder|receiver have left chains c, a and b.
   - The `kept_axial` RPT item still lists the holder at 1000 N. That value belongs to The Loftsman and The Designer (TP1.3-10 owner line) and is unchanged here.
4. **TP1.3-13 (a1) cannot be reached in S3.** The per-Axes row filter refuses an arc drawn in the section Axes first ("sub-artist of no spec row plan_axes"). K5-B42 is matched on that reason.
5. **Two new Bs are not red on the pre-change code with a different reason:**
   - K8-B80 (block piece with the alternate) fires on the pre-change code. That code has no alternate pattern, so clause (1) already fails it. B80 guards that the alternate stays on the pieces above the split.
   - S3-3-B14 (side face as a face link) fires on the pre-change code through the old face test, with "no horizontal edge" in place of the sense reason.
   - Every other new B reads clean on the pre-change code, or fires there with the wrong reason or count.

Tags: MEASURED (read from a run in this session), DERIVED (hand arithmetic), DECLARED (spec, params or ruling).

Locations:
- Scratch: `D:\Unleashed Robotics\_scratch\cutjig\p9r2\`.
  - `pre\`: the pre-change harness.
  - `pre_rf\`: the pre-change code with the r2 fixtures, manifest and spec, used for red-first.
  - `records\`: S1 r8 and S2 r9 marked accepted, plus `s1_mass_report_r8.json`.
  - `dry*`: the Designer dry runs.
  - `probes\`.
- TMP and TEMP: `_scratch\cutjig\tmp`. Nothing was written to C:.

## 1 Findings

| ID | Source | Dry run | Fix | K8 predicate / rule | B fixture |
|---|---|---|---|---|---|
| F1 | M1 S3 r1 | see section 4 (A, B) | **to The Designer** (scale remedy, design value) | none | none |
| F2 | M1 S3 r1 | live S3 at r2: K4 (i) clean on the section (MEASURED) | (i1) no drawn leader crosses any text box; (i2) no two text boxes overlap. S3 placer `edge_leaders=True`: the drawn leader is the placer's leg | K4 (i), `sketch_common.text_overlap_issues` | K4-B23, K4-B24 (Z: K4-Z3 live S2, K4-Z4 live S1) |
| F3 | M1 S3 r1 | (a) the hold label clear of the inset tick labels: inset placement counts its own tick and y labels (`_inset_right_of_labels`), K4 (i2) clean. (b) duplicated text: see section 4 | (a) layout, applied. (b) **to The Designer** (label text, design value) | K4 (i2) | K4-B24 |
| F4 | M1 S3 r1 | K4, K5, K8 clean (MEASURED) | sync fan hub at (+footprint_x / 2, +footprint_y / 2), the label's anchor; the label leader ends on the hub | visual only | none |
| F5 | M1 S3 r1 | K3, K4 clean | home switches drawn above the A-A line (inset zorder). "+Y" set 2 pt right of x = 0 | visual only | none |
| F6 | M1 S3 r1 | K4 clean | axial-loop note (route per the rerouted chain c). Legend "chain:" renamed "dash-dot:", and the "dashed: hidden edges" line added | visual only (text; K4 reads printed values) | none |
| F7 | M1 S3 r1 | u -210 and u -110: K4, K5, K6, K7, K9, S3-2 clean. K8 fails 2 at both offsets: the extension lines drawn under gid span_lt widen its projected extent (MEASURED) | **returned to The Designer**: the offset passes, the extension lines need a declared sub-artist (`span_lt:ext`, admission rule to write) | none | none |
| TP1.3-10 | Topologist | p2 dry run reproduced: face links pass at 102.50, 100.00 (receiver floor), 72.00, 348.00, 332.00, 387.84; B13 and B14 fire | link `kind` (face, face_record, thread, one_body, fastened, declared) on every chain link. Face sense: x's bottom edge and y's top edge on the face z, u overlap > 0.05. Lint: kind present, face link has an S3 certifier (a/b symmetry links excepted). Base route rerouted (collet foot on the receiver floor). Member feet and bracket ends `fastened`. ring\|bearing and bearing\|drill_tube `declared` (S6-5). Spec edit: **Designer re-sign** | S3-3 face sense; `checks_s3.link_kind_issues` | S3-3-B12, B13, B14, B15 (Z: S3-3-Z) |
| TP1.3-11 | Topologist | r1: 14 artists, 8 row pairs drawn solid under unsectioned outlines (MEASURED) | `render_occlusion`: each overlapped artist is split (clip region outside, dashed hidden copy inside), as the plan renderer splits | K8 section convention clause (6a, 6b), `occlusion_issues` | K8-B77, K8-B78 (Z: K8-Z14) |
| TP1.3-12 | Topologist | live: the rear nut shoulder screw x [-18.86, -8.86] fires. Pinions on the true trapezoid (65.09) clean, on the footprint (59.66) fire (B85) | not_drawn `omit: off_plane` (rows / rows_s2 / x bands) or `omit: deferred` (owner), on every entry. Remedy for the screw: **to The Designer** (beyond row or convention) | K8 `not_drawn_band_issues` | K8-B83, B84, B85 |
| TP1.3-13 | Topologist (ruling) | drawn | `plan_axes:arc`, Line2D 0 to 90 deg at r `profile.width * 2 / 3` (40) plus a FancyArrowPatch head at 90. The untagged "theta ccw from +X" text is replaced by "theta" beside the arc | K5 `arc_issues` (a1 to a5) | K5-B40, B41, B42 (Z: K5-Z7) |
| TP1.3-14 | Topologist (ruling) | candidates in section 4 | `section.hatch_alt` per material (spec, Designer value), `hatch_split.at` selects the pieces wholly above. Renderer and clause (1) read `cut_hatch`; lint on the alternates. Live: no alternate declared, **to The Designer** | K8 clause (1) per piece, `hatch_alt_issues` | K8-B79, B80, B81, B82 (Z: K8-Z16, fixture alternate "--") |
| TP1.3-15 | Topologist (ruling) | drawn | `screw_c:root`, two dashed Line2D at u -160 ∓ 4.25, 360.00 to 1180.00 z_S. Spec `ticks` replaced by `root` | K5 `root_issues` (r1 to r5) | K5-B37, B38, B39 (Z: K5-Z6) |
| TP1.3-19 (NOTE) | Topologist | pixel-equal lever | lever u = `liftsync.switch_r_in * sind(jackscrew.angle[2])` (-190.00) and `liftsync.lever_r_tip * sind(...)` (-182.00) | existing lever rule | none |
| TP1.3-16, -17, -18, -20 (NOTE) | Topologist | none | not applied: -17 is an S1 spec edit with no pixel change; -16, -18, -20 are carried | none | none |
| LF1.3-1 | Loftsman | RPT pass, 10 items | L_min item appends the drawn bar 911.00 and the values with the shoulder-screw head 4.55: 889.55 / 890.39 / 1139.55 / 1140.39 (MEASURED from the drawn pieces) | RPT (reported, no threshold) | none (SW rule: reported values carry no controls) |
| LF1.3-2 | Loftsman (= D5) | section 5 | **to The Designer** (W_kg is a D5 value). Not applied | none | none |
| LF1.3-3 | Loftsman (= D9) | S2 r9 with S1 r8 accepted (scratch records): 18/18, tip force 351 / 379 / 563 / 269 N, basis `s1_mass_report_r8.json` (MEASURED) | `checks_s2.accepted_s1_mass_report`: reads the latest accepted S1 record's mass report in the records directory. Live S2 r9 still reads r7 until ORCH-B; re-run `s2 --rev 9` after `--accept s1` | RPT | none |
| LF1.3-4 to -9 (NOTE) | Loftsman | none | -4 = D1 to The Designer; -5 ruled no edit (D8); -6 values in section 5; -7, -8, -9 carried | none | none |
| M1 S1 r8 N1, S2 r9 N1 | M1 | none | NOTEs; no revision | none | none |

Re-plants (same revision, counts changed by the new rules, each re-read in the final run):
- **K4-B7:** planted 4. B7 gains 2 (i1).
- **K4-B8:** planted 7. B8 gains 1 (i1), 1 (i2) and 1 more.
- **K4-B18:** planted 3. B18 gains 1 (i1). Each plant moves a leader through another label.
- **K8-B54:** planted 134. The plant moves parts onto unsectioned outlines (clause 6).
- **K8-B55:** planted 12. Same cause as B54.
- **S3-3-B2, B7, B8:** re-planted on base_plate\|base_frame in both records, 1 issue each. The holder links have left the chain.
- **S3-3-B3:** S2 record stale too, 7 issues.
- **S3-3-B4:** reason "no bottom horizontal edge".
- **S3-3-B9:** a/b links set `face_record` in the plant.

Fixture scaffolding, `fixtures/s3_fixtures.py::_designer_pending`, to remove when The Designer rules:
- s3_ctx draws with the fixture alternate "--" and the nut shoulder screws deferred.
- Without it, every K8 control on the S3 fixture carries the 2 pending reds.
- `pending=False` draws the live state. K8-B82 and K8-B83 plant that state.

## 2 Check results

**S3 r2** (`docs/sketches/wip/s3_checks_r2.json`, MEASURED): **13 of 16 pass**.

| Check | Result | Value |
|---|---|---|
| K1, K2, K3 | pass | 412 spec keys |
| K4 | fail 1 | inset sync_callout label (D1). Section: 19 labels, K4 (i) clean |
| K5 | pass | section 128 artists (14 hidden copies, root lines), inset 36 (arc) |
| K6, K7, K9 | pass | K7 269 section tests |
| K8 | fail 2 | not_drawn rear nut shoulder screw in the band (TP1.3-12); anchor_c hatch_split with no alternate (TP1.3-14) |
| S3-1 | pass | 25.84 |
| S3-2 | pass | P_cr 1363.8 N, least 3.97 stall up |
| S3-3 | fail 7 | stale S1 r7 / S2 r5 only. Dry run with S1 r8 / S2 r9 accepted: pass, 48 links. Listed: 15 declared (incl. core_seat\|collet one body), 1 face_record, 9 fastened, 8 by symmetry |
| X1, SYM, SYM-P | pass | |
| RPT | pass | 10 items |

**Other runs (MEASURED):**
- S1 r8 re-run: 19/19. S2 r9 re-run: 18/18.
- `--baseline s3`: 16/16 matched.
- `--stale`: 2 records, 5 differences, the adopted keys, unchanged.
- **`--controls --jobs 12`: 392/392 match (Z 95/95, B 294/294, smoke 3/3), 187.7 s.**

| | Controls |
|---|---|
| Added | 24: K4-B23, B24; K5-Z6, Z7, B37 to B42; K8-Z16, B77 to B85; S3-3-B12 to B15 |

**Red-first (pre-change code, `pre_rf`, MEASURED):**
- K4-B23, B24, K8-B77, B78, B79, B81 to B85, S3-3-B12, B13, B15 read clean.
- K5-B37 to B42 fire with "sub-artist root has no admission rule" and "parent plan_axes not drawn": wrong reason and count.
- K8-B80 and S3-3-B14: see Corrections 5.

### Reported items (`wip/s3_summary_r2.md`, through RPT)

All are r1 values except L_min.

| Item | Value |
|---|---|
| L_min | 885.00 / 885.84; 1 m 1135.00 / 1135.84; drawn bar 911.00; with head 889.55 / 890.39 / 1139.55 / 1140.39 |
| n_crit | 1336 / 2086 rpm against 500 |
| pcr_margin | least 3.97 |
| f_stall | 343.18 / 282.21 per screw |
| wob_max | 1267.43 / 1084.54 N |
| lift_torque | 0.333 / 0.149 N m |
| kept_axial | 1000 N; 1267.43 / 1084.54 N |
| backdrive | lambda 5.20, self-locking |
| screw_share | as r1 |
| tension_segment | 815.84 / 690.84 / 40.84 / 815.84 |

## 3 PNG paths

- S3 r2: `docs/sketches/wip/s3_jackscrew_section_r2.png`.
- S1 r8 and S2 r9: unchanged (pixel-equal).
- Dry-run images:
  - `_scratch\cutjig\p9r2\dry_f1a.png`
  - `_scratch\cutjig\p9r2\dry_f1b.png`
  - `_scratch\cutjig\p9r2\dry_f7_210.png`
  - `_scratch\cutjig\p9r2\dry_f7_110.png`
  - `_scratch\cutjig\p9r2\dry_labels.png`

## 4 Design values for The Designer (dry run each; none chosen)

| Item | Candidates and dry runs (MEASURED unless tagged) |
|---|---|
| F1 scale | (A) `FIGSIZE["section_yz"]` (20, 30) in place of (14, 10): K3 to K9 per Axes unchanged (K4 D1 and K8 pending only); PNG 4511 x 3859; about 2.5 px/mm in the section (DERIVED, 3 x the r1 0.82). (B) detail views as declared section_yz Axes: detail_b (u -250 to -60, z_S 230 to 420, 14 rows) and detail_c (u -250 to -100, z_S 1160 to 1240, 4 rows): K3, K6, K7, K9 pass in both; detail_b 3.3 px/mm (4 x). Needs: `projection_by_axes` for nut_housing_c in detail_b (K5 6 issues without it); inset positions as spec values (the dry layout used figure literals, K1 3, and detail_c overlaps detail_b). K8 per detail Axes reads the same 2 pending items |
| D1 / F3 sync label | text "sync:" with key liftsync.method: K4 pass in both Axes, the value printed once |
| F3 hold label | text "power-off hold:" with key hold.device: K4 pass, the value printed once |
| F7 span offset | u -210 and u -110 (row place r_in 210 or 110): see the table above; extension lines need `span_lt:ext` admission |
| TP1.3-14 alternate for aluminium | "--", "\|\|", "++", "////", "\\" (single, the reverse of "//"): each passes the lint and clause (1) (K8 shows only the TP1.3-12 item). "\\\\" (steel) fails the lint (K8-B81) |
| TP1.3-12 rear nut shoulder screw | (a) a beyond row (dashed shank behind the housing, head solid above 395.84); (b) a convention line "fasteners beyond the plane not drawn" with the entry `omit: deferred`. Dry run (b): K8 clean of that item (fixture state, K8-Z14) |
| D5 / LF1.3-2 W_kg | section 5 |
| D7 bolt PCD | open, entry `omit: deferred` |
| TP1.3-11 classes (alternative to the dashed split) | wingnut and drill_head as cut rows, pinion_c and liftmotor_pilot_c as their true cut with the shaft bore, coupling cut: Designer choice; the split satisfies clause (6) today |

**Spec re-sign (Designer; Loftsman for placement):**
- chains kinds and the reroute;
- not_drawn omit fields;
- plan_axes arc;
- screw_c root;
- lever expressions.

The spec status line names them.

## 5 Values for the orchestrator (Design Notes 32, B2-7)

| Quantity | Value |
|---|---|
| Receiver uplift, stall-limited bind 3 F_stall - W | 791.65 N (mu 0.15), 608.75 N (mu 0.20) at W 24.25 kg; 772.03 / 589.13 N at W 26.25 kg (DERIVED, equal to Loftsman LF1.3-6). Design Notes 32 states 1029.5 N gross (3 F_stall) |
| W with the top-end block | 26.25 kg, 257.51 N |
| Kept-part force at F_stall + W | 1287.05 N (mu 0.15), 1104.16 N (mu 0.20), against the 1267.43 sent as N5 (B2-7) |
| Per screw at W 26.25 | static 85.84, capture 119.85, retract 185.84, cut 247.50, stall up 343.18 |
| Margins at W 26.25 | 15.89 / 11.38 / 7.34 / 3.97 (least unchanged) |
| Lift torque at W 26.25 | cut 0.325 / capture 0.157 N m |

All rows are DERIVED by `checks_s3.loads` with `drill.top_block_mass` added to W_kg. They equal the Loftsman values.

## 6 Rules awaiting signature

| Rule | Premise | Z / B | Raiser |
|---|---|---|---|
| K4 (i) leader and text overlap (script figures) | a label is read only when no other ink runs through its letters | K4-Z3, Z4 / K4-B23, B24 | The Designer (F2, F3) |
| S3-3 link kinds and face sense | a horizontal face carries the cut-case link only with x above it | S3-3-Z / B12 to B15 | The Topologist (TP1.3-10) |
| Section convention clause (6) occlusion | an unsectioned row drawn whole hides the section inside its outline | K8-Z14 / B77, B78 | The Topologist (TP1.3-11) |
| not_drawn omit and band lint | an omitted part lies off the band or is deferred to an owner | K8-Z14 / B83 to B85 | The Topologist (TP1.3-12) |
| `plan_axes:arc` admission | the arc states theta ccw as a sign check | K5-Z7 / B40 to B42 | The Topologist (TP1.3-13) |
| hatch_split alternate per piece and lint | an alternate differs from every material pattern | K8-Z16 / B79 to B82 | The Topologist (TP1.3-14) |
| `screw_c:root` admission | the thread is stated by its span and root only; the lead is in the label | K5-Z6 / B37 to B39 | The Topologist (TP1.3-15) |

## Gameplan lines to change

1. l.138 (K4 row): insert after its last text `K4-B22 a label drawn outside its home Axes, refused (1.3 P5f)`.
   - Old: `K4-B22 a label drawn outside its home Axes, refused (1.3 P5f) |`
   - New: `K4-B22 a label drawn outside its home Axes, refused (1.3 P5f); (i) on a script-drawn figure no drawn leader crosses a text box and no two text boxes overlap (labels, notes, tick labels, titles; boxes shrunk 1 px): K4-B23 text planted on two leaders, K4-B24 text planted on a label (1.3 (h) r2, Designer M1 S3 r1 F2, F3); K4-B7, B8, B18 re-counted 4, 7, 3 |`
2. l.139 (K5 row).
   - Old: `K5-B36 S3 bearing line ending in the journal gap (section form, Topologist P5T FIX 5) |`
   - New: `K5-B36 S3 bearing line ending in the journal gap (section form, Topologist P5T FIX 5); 1.3 (h) r2: sub-artist screw_c:root, two dashed vertical root lines at u_c -+ d_r / 2 over root.from to root.to inside the drawn screw (K5-Z6, B37 nominal radius, B38 5 past thread_end, B39 solid; TP1.3-15); plan_axes:arc, plan only, points on r, ccw (cross > 0), ends at theta0 and theta1, head tangent ccw (K5-Z7, B40 reversed, B41 r + 5, B42 in the section; TP1.3-13) |`
3. l.142 (K8 row).
   - Old: `mirror_about_radial in plan (K8-Z15, B76); a FancyArrowPatch draws no area |`
   - New: `mirror_about_radial in plan (K8-Z15, B76); a FancyArrowPatch draws no area; 1.3 (h) r2: clause (6) no solid area of another row inside a solid unsectioned piece, the renderer splits it with a dashed hidden copy (K8-B77, B78; TP1.3-11); hatch_split pieces above the split carry section.hatch_alt[material], alternates differ from every material pattern (K8-Z16, B79 to B82; TP1.3-14); every not_drawn entry omit off_plane (rows, rows_s2 on the true plan outline, or x bands, off the band 0 to -profile.width) or deferred with an owner (K8-B83 to B85; TP1.3-12); K8-B54, B55 re-counted 134, 12 |`
4. l.147 (K table pointer).
   - Old: `(368 controls: Z 92, B 273, smoke 3, all match; 157.6 s at --jobs 12).`
   - New: `(368 controls: Z 92, B 273, smoke 3, all match; 157.6 s at --jobs 12). Step 1.3 (h) r2 (research/sean/cr_scratch/step1.3_engineer_revision_r2.md) added K4-B23, B24, K5-Z6, Z7, B37 to B42, K8-Z16, B77 to B85, S3-3-B12 to B15, re-planted K4-B7, B8, B18, K8-B54, B55, S3-3-B2 to B4, B7 to B9, and the fixture stand-ins for the two Designer-pending items (392 controls: Z 95, B 294, smoke 3, all match; 187.7 s at --jobs 12).`
5. l.276 (detail 1.3 Script).
   - Old: `s3 --rev 0 red by cause 16/16 in wip/baseline_red.json; SYM-P a green guard, 1.3 P5f).`
   - New: `s3 --rev 0 red by cause 16/16 in wip/baseline_red.json; SYM-P a green guard, 1.3 P5f). S3 r2 (1.3 (h) P9, step1.3_engineer_revision_r2.md): 13/16; K4 red on the sync_callout label (D1, Designer), K8 red on the rear nut shoulder screw in the beyond band (TP1.3-12) and the missing cover hatch alternate (TP1.3-14), both Designer values; S3-3 red on stale records only (dry run with S1 r8 / S2 r9 accepted: 48 links); S1 r8 and S2 r9 pixel-equal on the r2 harness.`
6. l.289 (S3-3 row).
   - Old: `spec \`chain\` cutter, core, collet core stop, collet, holder, receiver, base plate`
   - New: `spec \`chain\` cutter, core, collet core stop, collet, receiver (collet foot on the receiver floor; the holder carries no cut-case axial load in the drawing, Topologist 1.3 (e) TP1.3-10; every link carries a kind: face with its sense, face_record, thread, one_body, fastened, declared), base plate`
7. l.293 (Reported).
   - Old: `and the value with the nut shoulder-screw head above the housing top (889.55 / 890.39 at 1.3 (b) P2f2; Designer re-sign note 1)`
   - New: `and the value with the nut shoulder-screw head above the housing top (889.55 / 890.39 at 1.3 (b) P2f2; Designer re-sign note 1; both printed in the RPT L_min item from the drawn pieces at S3 r2, Loftsman 1.3 (e) LF1.3-1)`
8. Design Notes 13: insert after the row beginning `| S2-r5 | 2026-11-25 |`.
   - New: `| S3-r1 | 2026-11-26 | No correction from Sean yet. r2 came from M1 F1 to F7 and the (e) cross-reviews (TP1.3-10 to -15, LF1.3-1 to -3) | r2: K4 (i) (K4-B23, B24), S3-3 link kinds (S3-3-B12 to B15), K8 clause 6 (K8-B77, B78), not_drawn bands (K8-B83 to B85), hatch alternate (K8-B79 to B82), arc and root admissions (K5-B37 to B42); F4, F5, F6 visual only; F1, F3 text, F7, D1, D5, TP1.3-12 and -14 values to The Designer (\`step1.3_engineer_revision_r2.md\`) |`
9. Progress Log: insert after the row beginning `| 1.3 | 2026-11-26 | Receiver shoulder (`.
   - New: `| 1.3 | 2026-11-26 | (h) P9 (step1.3_engineer_revision_r2.md): S3 r2 13/16 (K4 D1, K8 TP1.3-12 / -14 Designer values, S3-3 stale records; dry run with S1 r8 / S2 r9 accepted: S3-3 48 links); seven new rules with Z and B, each B red on the pre-change code; S1 r8 19/19 and S2 r9 18/18 re-run, pixel-equal; controls 392/392 in 187.7 s; Designer items F1 (options A and B dry-run), D1 and hold label text, F7 offset with sub-artist, cover hatch alternate, nut shoulder screw convention, W_kg; values for Design Notes 32 and B2-7: uplift 791.65 N, W 26.25 kg, 1287.05 N |`
10. l.705 (Design Notes 32).
    - Old: `for uplift in retract-with-bind and stall up (up to 1029.5 N)`
    - New: `for uplift in retract-with-bind and stall up (up to 1029.5 N gross; stall-limited through a gripped core 3 F_stall - W = 791.65 N at mu 0.15, 772.03 N with the top-end block, DERIVED, Loftsman 1.3 (e) LF1.3-6, Engineer 1.3 (h) r2)`
