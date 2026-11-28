# Step 1.4 P7dr: Designer re-sign of the (h) r2 fix pass (spawn A, S4 spec signer)

Sources:
- `step1.4_designer_spec_signoff.md` (P3a);
- `step1.4_engineer_revision_r2.md`;
- gameplan Design Notes 35;
- live `docs/sketches/s4_spec.yaml`, `s1_spec.yaml`, `s3_spec.yaml`, `sketch_common.py`, `fixtures/step14r2_fixtures.py`, `fixtures/manifest.yaml`, `wip/fixtures/controls_results.json`, `wip/s4_checks_r2.json`;
- the Engineer's scratch `open14\p9r2\` (pre-change tree, `probe_final_s4.json`).

Spec diff: `D:\Unleashed Robotics\_scratch\cutjig\open14\p7dr\specdiff.txt` (pre-change tree against live, CR stripped). Dry run: `D:\Unleashed Robotics\_scratch\cutjig\open14\p7dr\ws\o2_dry.py`.

## Corrections to the brief

1. **The washer leader lands on two different faces.** The Engineer's report and the spec comment say "-u inner face". `probe_final_s4.json` puts the anchor at u -68.40 in the carrier figure (washer bore, -u side) and at u -71.60 in the liner figure (washer OD, -u side). Both are at z 205.74 z_S, which is mid-height (MEASURED). Both are thin faces and both leaders run at 15 deg, so the R1 clause holds in each figure. The spec comment is loose, not wrong.
2. **K8 clause o2 (outline absent) has no B in the manifest.** K8-B120 and B121 cover o1, B123 covers o3 and B122 covers o4.
   - Dry run on live S4, carrier figure, with every `wingnut:outline` Line2D removed: `carrier/wingnut: no outline wingnut:outline (o2)`. The live figure is clean (MEASURED, `o2_dry.py`).
   - The branch fires. It has no control of record.
3. **The R1 premise "every script saves at the figure dpi" has no check that refuses a dpi argument.**
   - `saves_tight` reads only `bbox_inches`.
   - K3 checks `fig.dpi == DPI` (150).
   - Today the premise holds:
     - no `savefig` call in the four scripts passes `dpi` (MEASURED, grep);
     - `rcParams['savefig.dpi']` is `'figure'` from the stock matplotlibrc (MEASURED).
   - A later `dpi=` argument would change the saved px per mm without any check firing. The Topologist signs the rule and its Z/B (Design Notes 35), so this goes to him as N1.

## 1. Findings I raised (P3a)

All six were CLOSED at P2r. Re-read here against the r2 live specs and records:

| Finding | Status | Evidence on r2 |
|---|---|---|
| FIX 1 tick and root labels | CLOSED | `receiver.root.label` template and `collet.slits.label` template are unchanged in s4_spec.yaml. K4-Z14 is clean with 36 labels (`controls_results.json`, MEASURED). The receiver row label moved off the thread ("receiver shoulder OD", M1 F1), so the thread is named only by the root-line label, as FIX 1 intended. |
| FIX 2 hatch adjacency | CLOSED | `hatch_variant: alt` is still on receiver_spigot, receiver and liner (s4_spec.yaml l.250, 295, 627). S4 r2 K8 passes 187 predicates (MEASURED). |
| FIX 3 min_bearing and O5 text | CLOSED | Seven `min_bearing` entries are in s4_spec.yaml. `s4_checks_r2.json` seat_bearing reads 3.00 / 0.50 / 2.50 and 8.15 MPa (MEASURED). The core_seat depth edit does not touch the read, because core_seat is section_true and the bearing read uses its pieces. |
| FIX 4 O3 wing form | CLOSED | `wingnut.wing` style, label and admission text are unchanged in S4. S3 keeps the same x_band form. |
| FIX 5 O4 follow-ons | CLOSED | The S1 washer row is drawn (FIX 5 (c)). Its label is now null (M1 S1 r9 F2), and the row stays in the part list with its X1 equality (X1 72 rows pass, Engineer section 1). |
| FIX 6 rubric | CLOSED | Text only; r2 does not touch it. |

Class repeats: none.

## 2. Signatures

**(1) 12 px threshold, Design Notes 35 R1: SIGNED.**
- `COLLINEAR_PX_MIN = 12.0` and D = max(COLLINEAR_PAPER_MM x f, 12 / kx) per Axes (`collinear_scale`, sketch_common.py l.2662 to 2678).
- At DPI 150, 12 px is 2.03 paper mm, about six 1-pt line widths (DERIVED).
- The M1 S4 r1 F2 offenders read 7 to 8 px. K4-B61 plants 8 px and fires at D 1.49 data mm (MEASURED).
- Per-Axes D (MEASURED, Engineer section 2):
  - S1 22.86;
  - S2 8.67;
  - S3 4.90 (section) and 7.56 (inset);
  - S4 1.47 to 1.49 data mm.
- Final firings and unplaceable labels are 0 in every Axes, and no label went null.
- Condition carried as N1: the dpi premise check (Correction 3).

**Correction 6 of the fix pass (frac anchor on a thin face): ruling.**
- A `label_anchor_frac` or `label_theta` anchor in a signed spec stays where the spec puts it, provided its angled leader passes rule (l).
- R1's mid-height clause governs default and ink anchors.
- S1 guide_b frac 0.75 at -15 deg stands. The angle takes the leader off the 30 mm face edges, which is the premise of the clause.

**(2) Spec edits: SIGNED, each as below.**

s4_spec.yaml:
- **receiver label "receiver shoulder OD" (receiver.shoulder_od, .0f): SIGNED.**
  - The leader ends at u 100.00, the shoulder (placer record).
  - The text prints 200 and names the cut-case seat feature.
- **base_plate label "base plate, hole": SIGNED.**
  - The leader ends on the plate end (u 130).
  - The text names the part first and the number second, as M1 F1 set.
- **wingnut label null; sweep label template on `wingnut:sweep`: SIGNED.**
  - The template prints "wing nut sweep r 115" from `wingnut.sweep_clear_radius`.
  - This is the S1 / S3 landing (Design Notes 35 R3).
  - N3 covers the unnamed nut body.
- **washer `label_anchor_frac` removed: SIGNED.**
  - At D 1.47 the 0.80 slot between the relief top 145.59 and the plate underside 146.39 admits no leader to the +u face, and frac 0.69 and 0.5 were both refused (Engineer Correction 3, MEASURED).
  - The landing at mid-height of a -u face (z_S 205.74) at 15 deg meets R1's thin-face clause.
  - Correction 1 and N2 apply.
- **drill_tube_stub row: SIGNED.**
  - Unsectioned outline r 76.20 from head_top to z_A 330. The tube is an unsectioned body under `convention.unsectioned`, which is amended to "drill tube to the crop".
  - Neighbours: drill_head C, core_100 N, liner N (liner pose only).
  - Part-list row added.
  - A separate id is needed because X1 holds `drill_tube` z_rule equal in s1 and s3. The notes field states that reason.
  - The z_max literal 330 duplicates `crop.z_A[1]` (N4).
- **Shape, crop and note text: SIGNED.**
  - floor: ground hatch dropped.
  - base_plate: "ends square at the crop".
  - crop source: break lines not drawn, tube to the crop top.
  - figure 2 note: "OD 105 nominal (drawn 106 x 2.50 at K d+1)". This is one stated value with its drawn value; F5 (a) closed.
  - figure note: "the carrier and core stay on the stop" (F5 (b) closed), plus "Plate ends square at the crop; drill tube drawn to the crop top".
  - Every part a shape string names has a row or a not_drawn entry. The part list now holds 18 entries with drill_tube_stub. Missing: 0 (DERIVED from the diff).
- **core_seat depth ±(core.diameter_nominal + collet.grip_window_hi) / 2 = ±50.50: SIGNED.**
  - This equals the drawn ledge r 50.50 and the core_seat_105 form.
  - K7-B38 fires at ±50.00 (MEASURED).

s1_spec.yaml:
- **wingnut shape text and wing block: SIGNED.**
  - The text carries "wing outline simplified (build_parts/nut.py tapered wing_poly)" verbatim from R2.
  - The block declares u body_od / 2 to span / 2 (83.14 to 115) and z = collar-top expressions minus `wingnut.wing_height` 40 (113.09 to 153.09 z_A), the band R2 names. `count: wingnut.wing_count` is 2.
  - The keys `wingnut.wing_height` and `wingnut.wing_count` already exist in params.yaml (l.158, 159, ASSUMED), and params.yaml is unchanged (MEASURED, diff).
  - The solid, unhatched wing beside the hatched body is the ASME Y14.3 rib convention for a thin web cut lengthwise. The style text can say so (N5).
- **washer label null: SIGNED.** The washer is 1.3 thick, 0.7 px at the S1 scale, and S4 labels it.
- **not_drawn wings entry and figure-note text removed: SIGNED.**
  - Both are removed together, so K4's figure-note head rule stays consistent.
  - No other S1 part entry names the wings (grep).
- **core_seat depth: SIGNED** (same expression as S4; X1 shared row).

s3_spec.yaml:
- **core_seat depth: SIGNED** (same expression; X1 shared row; K7-B37 fires).

**(3) Cut-body outline checks K8-Z23, B120 to B123 (M1 F3 form): SIGNED for o1, o3 and o4.**
- `draw_cut_outlines` sets every section_true piece of a one_body group to linewidth 0 and draws the union boundary as `<first row>:outline`. `one_body_groups` includes single-row groups, so a single multi-piece body (holder cone, tube, flange) loses its internal seams as well.
- The F3 class is "a line across one cut body", in the side and section views (S1, S3, S4). Clause by clause:

| Clause | What it catches | B and observed result (MEASURED, `controls_results.json`) |
|---|---|---|
| o1 | the r1 seams | K8-B120 S4 holder+collar and K8-B121 S1 holder fire 1/1 |
| o3 | seams drawn as outline | K8-B123 fires (206 samples) |
| o4 | partial outline | K8-B122 S3 collet fires (184 samples) |
| o2 | no outline at all | the branch fires in the dry run but has no control (Correction 2, N6) |

- K8-Z23 is clean on live S4 (187 predicates).
- The premise (drawn pieces equal spec pieces) is held by K8 section_true_issues.

## 3. New findings introduced by the fix pass

No FIX. NOTES:

- **N1 (Topologist, R1 premise).** `saves_tight` or K3 should refuse a `savefig` call with a `dpi` argument, and `rcParams['savefig.dpi']` other than `'figure'`. Z: the four live scripts. B: a script copy with `dpi=75`. Today no check fires on either (Correction 3).
- **N2 (M1, S4 r2).** The washer and core_seat leaders cross the whole stack from the right column, the washer leader to the -u side:
  - washer: about 214 mm at 15 deg;
  - core_seat: about 193 mm at -25 deg.

  Both are DERIVED from the placer record. Both pass K4. `label_side: left` would shorten both to the -u side. The side placer honours it (place_labels l.620, 677); the section placer has no dry run, so this is not issued as a FIX.
- **N3 (M1, S4 r2).** No S4 label names the wing nut body. "wing nut" appears only in the sweep label, and "-X wing (behind)" names the wing. M1 r1 V7 read the body, skirt and plate unaided.
- **N4 (Engineer, next spec edit).** drill_tube_stub `z_max: 330` should read from `crop.z_A[1]` if eval_expr resolves it. As written, a crop change leaves the stub at 330, and K6 and K7 would not flag it.
- **N5 (Engineer, text).** Append "ASME Y14.3 rib convention: a thin web cut lengthwise is not hatched" to the S1 `wing.style`.
- **N6 (Engineer, manifest).** Add K8-B124: the outline sub-artist of one group removed whole (o2). The dry run reason is in Correction 2.

## Gameplan lines to change

none
