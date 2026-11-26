# Step 1.3 (c) (P5) Software Engineer check: P4 rules, S3-x fixtures and stub, harness delta since P0S

Verdict: **FIX (5 items).** The runner, the fixtures and the stub record reproduce: 336/336 in my copy, every control equal to the Engineer's, and the s3 --rev 0 record equal on every check. Every new B fires on its reason with its planted count, and 36 of 37 are red on the pre-change code. S3-2-B1 is the exception; its margin branch is shown red by deletion, which is acceptable. Branch deletion is the problem. 23 mutations in copies of the tree: 6 caught, 12 uncaught on rules P4 states (S3-2 span, five S3-3 branches, six section-convention clauses), 4 uncaught on named TP-7 and K4 branches, 5 equivalent or placer-only. One more branch, by inspection: `orphan_predicates` raises NameError on its only issue path. No check logic needs to change except the one-line NameError fix. Everything else is fixtures and manifest rows.

## Corrections to the brief

1. `--controls` has no output-location option, and two other reviewers run on the same tree. I ran every control, the stub and every mutation in byte-identical copies of `docs/sketches/` in my scratchpad (`sw/live/docs/sketches`, `params.yaml` two levels up; wip/, __pycache__ and figs excluded). My SHA-256 list of the 56 committed files under `docs/sketches/` (wip/, __pycache__, figs excluded) is unchanged from my first read to my last (MEASURED). Nothing of mine wrote to `docs/sketches/`.
2. The other reviewers may have shared the CPU during my run of record, so 148.0 s is an upper bound.
3. P4 section 1 lists `orphan_predicates` as the premise check "a predicate is evaluated in at least one Axes". It has no control, and it cannot report: the f-string names `t`, which is undefined in that function. I planted one predicate with `axes: nowhere` on the live S3 spec and called it directly: `NameError: name 't' is not defined` (MEASURED). Inside K8, `safe()` turns that into an error, so K8 fails closed. The reason it shows is a traceback, though, and the premise message never appears. That is FIX 1.
4. The manifest `gameplan_line` fields of the new entries do not match the lines P4 cites. K rows are 1 low (K3 at 136 against l.137) and S3 rows are 3 low (283 to 285 against l.286 to 288). Older entries carry the same offset (K5-B3 at 138, K5 row l.139). NOTE 6.

Tags: runs MEASURED 2026-11-26 in scratchpad copies. Hand reasoning DERIVED.

## 1 Re-runs against the Engineer's numbers (task 3)

| Run (copy `sw/live`) | Mine (MEASURED) | Engineer (P4 section 3, 4) |
|---|---|---|
| `--controls`, default jobs 12 | Z 88/88, B 245/245, smoke 3/3, exit 0; **148.0 s** wall | 336/336, 148.4 s |
| Per-control, mine against `docs/sketches/wip/fixtures/controls_results.json` | Row order and ids equal (336). expected 0 differ, observed 0, match 0, reason 1 (H1-B5: the temporary-directory name, as at P0S) | — |
| Sum of per-control seconds | 1603.8 s; slowest S2-FULL 28.4, K4-B18 24.1, K8-B39 16.5, S1-FULL 16.1 | — |
| `s3 --rev 0` (stub) | 15 checks. result, cause, n_issues and reason equal on all 15 against `docs/sketches/wip/s3_checks_r0.json`. Green: K1, K2, K3, K5, X1. Red: K4 content 23, K6 absent 69, K7 absent 326, K8 content 112, K9 content 71, S3-1/S3-2/S3-3 absent 1, SYM content 10, RPT absent 1 | same |
| Pre-change record `wip/p4_prerun/controls_results_prechange.json` (read) | 51 rows: Z 5/13, B 1/37 (S3-2-B1), smoke 0/1 | same |

The P0 target is 200 s and it is met. The run went from 285 controls in 121.9 s to 336 in 148 s: 51 controls for about 26 s, with S2-FULL still the critical path.

## 2 Branch deletion (task 1, task 2)

Each mutation is one exact replacement in a fresh copy, run with `--controls --only <set> --jobs 4`. Caught means at least one control mismatched. All controls matched in the unmutated copy (section 1).

| ID | Mutation (file) | Controls run | Result |
|---|---|---|---|
| M01 | S3-2 span test `abs(L_drawn - L_spec) > TOL_Z` off (checks_s3) | S3-2-*, S3-FULL | **not caught** |
| M02 | S3-3 named-face veto `elif fi:` off | S3-3-* | **not caught** |
| M03 | S3-3 symmetry premise `sym["result"] == "pass"` dropped | S3-3-*, SYM-* | **not caught** |
| M04 | S3-3 "every c link between the counterparts passes" forced true | S3-3-* | **not caught** |
| M05 | S3-3 record certifier: a pair in a non-C state certifies | S3-3-* | **not caught** |
| M06 | S3-3 veto (`if veto: ok = False`) off | S3-3-* | caught: S3-3-B1 |
| M07 | S3-3 `_pair_ok` pose filter dropped | S3-3-* | not caught |
| M08 | section convention (5): section_class spec-error branch off (sketch_common) | K8-Z14, K8-B5*, K8-B6*, S3-FULL | **not caught** |
| M09 | convention (4): "past one profile width" off | same | **not caught** |
| M10 | convention (3): "partly behind a cut part, split required" off | same | **not caught** |
| M11 | convention (3): beyond row hatched, off | same | **not caught** |
| M12 | convention (3): beyond row reaching in front of the plane, off | same | **not caught** |
| M13 | convention (1): "cut row the plane x = 0 does not cut", off | same | **not caught** |
| M14 | TP-7: an Axes with an id the spec does not declare (`set(found) - known`) off | K3-*, K9-* | **not caught** (K3-B10 plants an Axes with no id) |
| M15 | `_pred_in_axes`: z predicates no longer withheld from plan | K8 (8) | caught: K8-Z14, B53, B54, B55 |
| M16 | `sub_spec`: label no longer limited to the home Axes | K4-*, S3-FULL | **not caught** |
| M17 | `label_value`: value_from branch off | K4-*, S3-FULL | **not caught** (two S3 rows use value_from, l.1699, l.1714) |
| M18 | section azimuth branch off (falls to the plan form) | K8-*, S3-FULL | caught: K8-Z14 and 8 B |
| M19 | S3-1 cut-arrow `points` test off | S3-1-* | caught: S3-1-B2 |
| M20 | `reflect_record` rot sign kept | K6, K7, K8, S3 (156) | not caught; equivalent on S3 (no `rot:` in s3_spec.yaml) |
| M21 | convention (2): unsectioned zorder off | conv set | caught: K8-B59 |
| M22 | `look_direction_issues` returns [] | K8-*, S3-FULL | **not caught** |
| M23 | section_u "drawn piece is no spec piece" off | K8-* | caught: K8-B54, B55, B63 |
| M24 | P1R placer `tick_clash` returns None | K4-*, S2-FULL | not caught (placer rule) |
| M25 | P1R `render_plan`: a restyled piece stays in the opaque list | K8 plan set (47) | not caught |
| M26 | P1R `render_plan`: hidden copy not re-inserted after its original | same | not caught |
| M27 | P1R `render_plan`: second-call guard off | same | not caught (no script calls it twice) |

Reachability probes. These were run to separate "branch reached by the Z but its fail path has no B" from "branch never reached":
- M28 (`_face_issue` always returns an issue) turns S3-3-Z red on chain c anchor_c|anchor_bearing_c, anchor_bearing_c|anchor_locknut_c and the nut face. The three named faces are evaluated, and pass, on the Z.
- M29 (SYM forced fail inside S3-3) turns S3-3-Z red on every a, b symmetry link. The symmetry path is reached.

So M02 to M04 are untested fail paths of live code.

By inspection: `orphan_predicates` has one issue branch, and it raises NameError (Correction 3).

## 3 S3-x fixtures, stub, SW-10 class, S3-2 form (task 2)

- **Reasons and counts.** Every S3-x B and every other P4 B matched its reason substrings and planted count in my run (section 1).
- **Stub.** No S3 check is green on the stub. K1, K2, K3, K5 and X1 are green as labelled guards.
  - The K8 content label depends on one spec defect (F3, STUB_CAUSE entry). Once P6 drops `frame: radial` from motor_shaft_c, the stub's K8 reads absent (111 untestable) and the STUB_CAUSE entry is wrong. NOTE 1.
- **SW-10 class (cannot fail through the drawing).**
  - **S3-2 margin branch.** It reads keys only. S3-2-B1 is a params plant (root 6.2, span 850), valid for the margin and the ruling. Only the span test reads the drawing, and M01 shows it has no B. Stays (Design Notes 31), with FIX 2.
  - **SYM.** A spec lint, the premise of S3-3's a, b links, in the same class as X1. Stays.
  - **S3-3 record certifiers (S1, S2).** They read records, not the figure. Only S3 certifiers, their faces and the veto read the drawing. Stays.
  - **S3-1.** Reads the drawn bearing line and cut arrow; the nut heights come from check_stack. Drawing-sensitive.
- **S3-2 form against Design Notes 31.**
  - The spec cases are static, capture_lift, retract_bind and stall_up, with SF from `jackscrew.buckling_sf` (3), K `end_factor_floating` (0.7) and L_t from the expression (870). That matches "SF 3 in every case, stall included" and the K 0.7 credit on L_t.
  - The cut case is tension (S3-1), so its exclusion is correct. The rigid segment is reported only.
  - It cannot pass silently:
    - a missing bearing row is absent;
    - an empty `cases` list raises at `min()`, an error that fails closed;
    - an unknown case name raises KeyError, also an error.
  - The one silent route is the drawn span, because P_cr is computed from L_spec. With the span test deleted, any drawn bearing rows pass (M01). FIX 2.
- **Veto rule (new, Correction 3 of P4).**
  - The rule is sound and small. A section that draws the pair open contradicts the record, so the record cannot certify that link. M06 shows B1 guards it.
  - Under the rule the signed spec vetoes receiver|base_plate (F1). The S3-3 fixtures drop that one certifier. S3-3-Z therefore runs on an edited spec: post-P6 symmetry state, receiver certifier dropped, P4 findings applied. NOTE 2.

## 4 Simplicity gate (task 4)

- **Per-Axes (TP-7).** `AxesFig` presents one Axes as a one-Axes figure. `sub_spec` and `per_axes` wrap K3 to K9 without touching their bodies. S1 and S2 take the old path (`needs_split` false); their records and PNGs are equal (P4 section 3). This is the least code that gives each Axes its own view. PASS.
- **Section view.** The section is evaluated as the side view of the plan reflected across x = y, so K6 and K7 reuse the side-view code. That is cheaper than a second frame. PASS. The reflected `rot` is unexercised (M20, no rot in S3); a rotated placed row in a later section needs a control first. NOTE 4.
- **Renderer section convention.** `render_section` is about 25 lines and its check about 65. PASS, with one gap. `render_section` dashes a beyond piece only when every sample is behind a cut part, and its own check then fails a partly hidden piece ("split required"). The plan renderer splits by clip path (`region_split`); the section renderer leaves the split to the script. No fixture has a partly hidden beyond piece (M10). NOTE 3.
- **S3-3.** About 130 lines. The symmetry-range expression (first index of the c counterpart of x to last index of y) is opaque but conservative: it also requires screw_c|nut_c for anchor|screw and ring|bearing for nut_housing|ring. Acceptable.
- **Ceremony.** `checks_s3.K_CHECKS` equals the default K1 to K9 list: a dead override (my P0S NOTE 3). Drop it. NOTE 5.

## 5 Findings

**FIX 1 (orphan_predicates).** Replace the undefined `t` in the f-string with `_pred_target(pr)`.
- Add K8-B64: an S3 fixture whose spec gives one predicate `axes: nowhere`.
  - Reason "spec error, predicate evaluated in no declared Axes".
  - Red on the current code (K8 error, NameError reason).

**FIX 2 (S3-2 drawn span).** Add S3-2-B2: guide_bearing_c drawn 5 mm up in the figure only, keys unchanged.
- Reason "drawn span 875.00 against 870.00 (spec)", planted 1.
- Red under M01.

**FIX 3 (S3-3 branches the rule text names).** Each fixture goes through `_s3_3_ctx`, and each must be red under the matching mutation:
- (a) S3-3-B4, named face, M02: nut_c drawn with its flange 1 mm above the counterbore shoulder while the side faces still touch (K7 C). If that layout cannot hold C, plant the face through the spec neighbour face z + 1 instead.
  - Reason "S3 face: no horizontal edge", planted 1.
- (b) S3-3-B5, symmetry premise, M03: specs with x1_exempt left on S3 anchor_b.
  - Reason "symmetry premise (SYM) fails", planted 8 (chains a and b, four links each).
- (c) S3-3-B6, open c link between the counterparts, M04: nut_housing_c|nut_c open in the section. A face plant that leaves the c link vetoed also works.
  - Reason "symmetry: a c link between the counterparts is open".
- (d) S3-3-B7, record certifier in a non-C state, M05: the S1 record with collet|holder at capture_end set to F.
  - Reason "states ['F']", planted 3 (chains c, a, b).

**FIX 4 (section convention clauses without a B).** One fixture per clause on `s3_fixed`, each red under its mutation:
- (5) a row with `section_class` removed (M08);
- (4) a row drawn wholly past one profile width behind the plane (M09);
- (3) a beyond piece partly behind the anchor block, drawn solid and unsplit (M10);
- (3) a beyond row hatched (M11);
- (3) a beyond row whose depth band reaches x > 0 (M12);
- (1) a cut row moved so its depth band misses x = 0 (M13).

Six B, each planted 1 with the clause's reason text.

**FIX 5 (TP-7 and K4 rule branches P4 names).** Each B must be red under its mutation:
- K3-B11: a third Axes carrying an id the spec does not declare. Reason "is not declared in the spec (insets)" (M14).
- K8-B65: look arrows reversed toward +X. Reason from `look_direction_issues` (M22).
- K4-B21: the load_cut label printing a number other than its value_from value (M17).
- K4-B22: an inset row's label drawn in the inset, where it is not the row's home Axes (M16). This one applies only if K4 is meant to refuse it. If labels are only withheld and never refused, state that in the rule text and drop the B.

**NOTE 1 (stub cause).** K8's content red on the stub rests on F3. At P6, re-run `s3 --rev 0` and `--baseline s3` after the spec edits, and remove the K8 STUB_CAUSE entry. The content evidence is then the K8 B fixtures in run 1.

**NOTE 2 (fixture scaffolding with a removal trigger).** These exist only until P6:
- `p4_spec_findings` (F2, F3);
- `_receiver_cert` (F1);
- `_post_p6_specs` (SYM state);
- the pre-P4 figure fallback in `_figure`.

When S1 r8 and S2 r9 are accepted and the S3 spec edits land, point S3-3-Z, SYM-Z and the K5/K8 Z at the live specs and delete the scaffolding in the same revision. Otherwise the Z stays green on specs that no longer exist.

**NOTE 3 (section split).** If the S3 drawing has a beyond piece partly behind a cut part, either give `render_section` the plan renderer's clip split, or have the script draw the two pieces. Decide before P6 draws.

**NOTE 4 (equivalent or unexercised).**
- Reflected `rot` (M20): no rot on S3.
- `render_plan` copy order, second-call guard and opaque-list drop (M25 to M27): no observable difference on S2 r8; P1R signed by the Topologist and the Designer.
- Placer `tick_clash` (M24): a placer rule without a K check. A tick-label overlap is legibility, so it goes to M1.

No action unless a later sketch exercises these.

**NOTE 5.** Drop `checks_s3.K_CHECKS` (equal to the default).

**NOTE 6.** Re-number the manifest `gameplan_line` fields in one pass at P5f (K rows +1, S3 rows +3), or drop the field. The gameplan K table pointer carries the ids.

**NOTE 7 (S3-3 pose filter, M07).** No B shows a record pair that is C only at a pose other than the figure pose. Cheap to add with FIX 3 (S1 record collet|holder moved to pose load only); optional.

## Gameplan lines to change

1. l.146 (K table pointer, P4 line 17): hold the P4 text until P5f. At P5f, add the FIX controls to the list: K3-B11, K4-B21, K4-B22 (or dropped), K8-B64, K8-B65, the six convention B ids P5f assigns, S3-2-B2, S3-3-B4 to B7. Replace "336 controls: Z 88, B 245, smoke 3, all match; 148.4 s at --jobs 12" with the P5f counts and time.
2. l.287 (S3-2), after the P4 line 19 text `against SF 3)`, insert: `; S3-2-B2 bearing row drawn 5 above its key (drawn span against the expression, 1.3 P5 FIX 2)`.
3. l.288 (S3-3), after the P4 line 20 text `a, b links by symmetry from c under SYM)`, insert: `; B controls per branch (1.3 P5 FIX 3): named face off its z (S3-3-B4), SYM failing (B5), a c link between the counterparts open (B6), a record pair in a non-C state (B7)`.
4. All other lines: none. The FIX closures carry their K-row text at P5f.
