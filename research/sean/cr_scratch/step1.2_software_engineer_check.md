# Step 1.2 (c) Software Engineer check: H6 delta, step 0 code, P4 plan rules and S2-x fixtures

Verdict: **FIX (5 items).** Every control the Engineer lists is real and matches on my re-run. Deleting branches in copies of the harness found seven branches that no control notices. Four of them guard a decision someone made at 1.1 or 1.2, so they are FIX. Each FIX is new or re-scoped fixtures plus manifest rows; FIX 4 also changes about four lines of `--accept`. No spec change. No check changes except FIX 4.

**SW-17: SIGNED.** K5-B7 fires on its reason with 1 issue. With the plan comparison removed, K5-B7 and K5-B8 both go clean (M01).

## Corrections to the brief

1. The Engineer's 1c table gives the annulus premise as "containment of the drawn annulus in [a, b] (K8 plan_extent)" and points at K7-B27. K7-B27 mutates the spec (bearing OD 101) and draws it faithfully, so it tests K7 and never the containment. The annulus branch of `outline_outside` has no B. Returning 0 from it leaves all 79 K7, K8 and S2-x controls matched (M04). This is FIX 1.
2. Engineer step 0 open item 4 holds. When the wip/ controls mismatch, `--accept` passes and silently skips the harness copy-up, and no control exercises the copy-up at all. In H1-Z1 the wip/ folder has no controls results, so `harness_outputs` returns []. Removing the mismatch guard leaves all 7 H1 controls matched (N21). This is FIX 4.
3. The gameplan has already applied the Engineer's P4 lines (l.138 to l.146, l.263, Progress Log row 1.2). The lines in the last section are against the current text.

Tags: run results MEASURED 2026-11-25. Hand values DERIVED.

## 1 Re-runs against the Engineer's counts (task 4)

| Command | Mine (MEASURED) | Engineer | Same |
|---|---|---|---|
| `check_sketch.py --controls` | Z 55/55, B 121/121, smoke 2/2 (178/178), exit 0, 270 s; mutation runs shared the machine for part of it | 178/178, 264 s | yes. Every control id, match flag and observed string equals `wip/fixtures/controls_results.json` as the Engineer left it |
| `check_sketch.py s2 --rev 0` | exit 1, 5.4 s. Green: K1, K2, K3, K5, X1. Red content: K4 (15), K9 (69). Red absent: K6 (68), K7 (1278), K8 (112), S2-1 to S2-6 (1 each) | same | yes. The result, cause and n_issues for each check equal the Engineer's r0 record |
| Run 2 against STUB_EXPECT / STUB_CAUSE, computed in-process from my r0 record | 17/17 | 17/17 | yes. I did not re-run `--baseline s2`, because it would add one more dated `prior` record (NOTE 3) |
| SHA-256 of the 40 committed files under `docs/sketches/` outside wip/, before my first run and after the last | **0 differences** | 0 (37 files at step 0) | yes. No `__pycache__` written |

## 2 Method

Each mutation ran in a fresh copy of `docs/sketches/` in my scratchpad, with `params.yaml` one level above. The copy deleted or weakened one branch. Then the manifest controls of the affected checks ran through `check_sketch.run_control` and `compare`. "Caught" means at least one control mismatched. The unmutated copy matched every control in the subsets (47 of 47 in the first subset).

| ID | Mutation | Controls run | Result |
|---|---|---|---|
| M01 | K5: `got != want` comparison off in plan (SW-17) | K5, 14 | caught: K5-B7, K5-B8 |
| M02 | K7: one-figure lint off (4f) | K7, 44 | caught: K7-B28 |
| M03 | K8: plan_extent polys branch off (4g) | K8, 29 | caught: K8-B20, K8-B19 |
| M04 | `outline_outside` annulus branch returns 0 (4g, annulus) | K7, K8, S2-2, S2-5a, S2-5b, 79 | **not caught** (FIX 1) |
| M05 | K8 sector: d_out (drawn wider than the wedge) off | K8, S2-5a, 31 | **not caught** (FIX 2) |
| M06 | K8 sector: d_in off | 31 | caught: K8-B23 |
| M07 | `flatten_path`: Bezier control points read as vertices (pre-change behaviour) | K5 to K9, S2-x, 123 | caught: K8-Z6 and 6 K8 Bs (false reds: spigot hole 2.77 out, screw_a 0.14, nut_a 0.72) |
| M08 | `BEZIER_STEPS = 1` (segment end points only) | 123 | not caught. Not load-bearing (section 5) |
| M09 | K5 bore_cone: lower z bound off | K5, 14 | **not caught** (FIX 5) |
| M10 | K9 pose-set: Text branch off | K9, 8 | not caught (NOTE 1) |
| M11 | `place_extents` ignores `rot` (side view) | K6, K7, K8, 87 | caught: K7-B20 |
| M12 | `plan_footprint` ignores `rot` | K7, K8, 73 | caught: K7-B20 |
| M13 | plan-contact: distance test off | K7, S1-5b, 46 | caught: K7-B16, K7-B19 |
| M14 | plan-contact: area test off | 46 | caught: K7-B17, K7-B20, K7-B21 |
| M15 | K8 projected_extent: low-x end off | K8, 29 | **not caught** (FIX 5) |
| M16 | K8 projected_extent: high-x end off | 29 | caught: K8-B7 |
| M17 | plan C: true-section premise off (`true = True`) | K7, 44 | caught: K7-B26 |
| M18 | K5 hub admission: width test off | K5, 14 | **not caught** (FIX 5) |
| N19 | S2-6: notch-clearance branch off | S2-6, 2 | **not caught** (FIX 3) |
| N20 | S2-1: phase branch off | S2-1, 2 | caught: S2-1-B1 |
| N21 | `harness_outputs`: mismatch guard off | H1, 7 | **not caught** (FIX 4) |
| N22 | `--accept`: supersession off | H1, 7 | caught: H1-B4 |
| N23 | K9 pose-set: artist branch off | K9, 8 | caught: K9-B5 |

## 3 H6: the r2 to r4 delta (task 1)

All 18 controls match on their reason substrings and planted counts: K5-Z2, K5-B6, K6-B7, K7-B14, K7-B15, K8-Z4, K8-B14, K9-Z2, K9-B5, K7-Z11, K7-B16 to B19, K8-Z5, K7-B20, K8-B15, K8-B16, plus K8-B7 re-scoped to planted 3. Each B plants a defect that occurred or nearly occurred in S1: the flange 8 low, the falling tooth face, the core shown at park, N hiding interference, the r1 holder, an arm 1 off or 1 into its block, the post short, the member turned 45, parts drawn wider than their footprint.

| Rule | Branches | B per branch | Gap |
|---|---|---|---|
| plan-contact (side view) | distance; area; no placed footprint | B16 and B19; B17, B20 and B21; B15 (the unplaced section pair; deleting the None guard gives an error) | none |
| projected_extent (side) | high-x end; low-x end; plan y | B7 (M16); **none** (M15); dead code (NOTE 2) | low-x end (FIX 5). B15 and B16 widen both ends, so the high-x test alone produces the planted count |
| section-N lint | one | B14 | none |
| pose-set (K9) | artist; Text with the row's gid | B5 (N23); none (M10) | Text branch, NOTE 1 |
| bore_cone (K5) | above the mate; below the mate; mate not drawn | B6; **none** (M09); deleting it errors | lower bound (FIX 5) |
| stack_ties (K6) | one | B7 | none |
| `place.rot` | side `place_extents`; plan `plan_footprint` | B20 (M11 and M12 both caught) | none |

## 4 Step 0 code (task 2)

- The `--accept` refusals are real controls. H1-B1 (check not pass), H1-B2 (empty note) and H1-B5 (PNG pixels) each check the refusal and that docs/ is unchanged. Supersession: H1-B4 catches its removal (N22). Re-run: H1-Z2 shows the docs flag survives a re-run to wip/.
- Revision copy-up is exercised by H1-Z1 (record, summary, byte-equal PNG). **Harness copy-up is not exercised** (FIX 4).
- Output rule: a verification run left the committed tree byte-equal (section 1).
- `--baseline`: correct. The dated key of an S2 assembly carries the prior record's S1 spec status (cosmetic). The history duplicates git (NOTE 3).

## 5 P4: plan rules, S2-x fixtures, stub (task 3)

**SW-17 (mine).** In plan, an axis-Z cylinder must be drawn as a Circle; any other class fails, a Rectangle included. K5-B7 removes the drill tube and draws a 152.4 square: 1 issue, "load/drill_tube: cylinder axis Z in plan_xy drawn as rectangle, needs circle". The B is drawing-only and K5 is the only check it reaches. If the plan view normal were lost, the spec-projection branch would fire with different text and the reason substrings would catch it. SIGNED.

**4f, one-figure premise (review of the code; Loftsman and Topologist sign at (e)).** The lint compares each row's plan outline across the stack poses it applies to, at TOL_Z, and runs only when there are fewer figures than poses. It is correct, and K7-B28 notices its removal (M02). Two edges, both NOTE 4:
- A row whose outline is None at one pose skips the rest of its poses (`break`).
- A `sector` row has no plan outline, so it is not linted. K8 sector equality runs at the figure pose only. Harmless while the sector reads only params.

**4g, plan_extent premise (review of the code).** Every drawn point is tested against the row's plan outline at TOL_Z. For polys this is containment in the union of convex pieces (`_inside` or edge distance); B20 and B19 cover it. For annuli it is max(a - r, r - b, 0). **No control reaches that branch** (M04). The rows that rely on it are ring, bearing, gear (the 1.2 (c) section edit exists to make gear|gear_hub C a true-section contact), gear hub, drill tube, cutter rim and keep-out. A gear drawn 5 over its OD, or a bearing drawn with its bore 5 small, passes every control today. FIX 1. Containment only, as before: a part drawn narrower than its outline passes K8. S2-5a now reads outlines, which closes that hole for the sector.

**Curve flattening (review of the code).** `flatten_path` walks `iter_segments(curves=True)` and samples each quadratic or cubic Bezier at 8 points on the curve, de Casteljau. The transform is applied to the path before sampling, which is exact for the affine transData chain. The closing vertex is dropped. Reverting to control points makes K8-Z6 fire (M07), so a regression is caught as a false red.
- The step count is not protected (M08). It is not load-bearing: containment and centres read points that lie on the curve for any step count. Chord sag only affects K7 tests that fall back to drawn pieces, and no curved S2 row does (collet_axis and operator_sector are the only fallbacks, MEASURED).
- The Collection branch of `artist_polys` still reads raw path vertices (NOTE 5).

**Premises with their own Z and B (detail 1 common (h)).**

| Plan rule | Premise check | Z | B | Gap |
|---|---|---|---|---|
| SW-17 | none | K5-Z3 | K5-B7 | none |
| TP-13 radial axis | radial footprint lint | K5-Z3 | K5-B9; K5-B10 | none |
| TP-13 hub admission | on the heel; no wider than the heel | K5-Z3 | K5-B11 (heel); **none for width** (M18) | FIX 5 (Topologist's rule; named here, he signs) |
| K7 plan F, G, C on outlines | K8 plan_extent, K6 plan centre | K7-Z12 to Z15 | B22 to B27, B29 | the annulus half of the premise (FIX 1) |
| plan C true section | `true` flag | Z13, Z14 | B26 (M17) | none |
| one figure (4f) | lint | Z15 | B28 | none |
| sector equal to wedge | drawn inside the wedge; wedge inside the drawing | K8-Z6 | B23 covers the drawing narrower only | drawn wider (FIX 2) |
| S2-6 seats | containment; notch clearance | S2-6-Z | B1 covers containment only | notch (FIX 3) |

**S2-x Bs.** All seven fire on their reasons with planted counts 5, 3, 3, 1, 18, 1, 1. S2-1-B1's planted 5 needs both the spacing and the phase branches (N20). S2-FULL runs, with no check erroring and none absent. The stub reds match STUB_EXPECT by cause, and no sketch check is green on the stub.

**SW-10 class (cannot fail through the drawing).**

| Check | Why | Stay/drop |
|---|---|---|
| S2-5a | Its fixed-part geometry is the spec outline. The only drawn input is the sector, which K8 holds equal to the wedge. A fixed part drawn wrong fails K8 or K6, never S2-5a. | Stays. It guards the sector-against-frame layout decision, and its B mutates the spec (half-angle 65) |
| S2-5b | Heights come from check_stack, and membership is spec outline against the drawn sector | Stays. It is the premise of the S2-5a relief, and its B mutates the spec (motor bottom 930) |
| S2-1, S2-2, S2-3, S2-4, S2-6 | read drawn centres, extents, heel points and pieces | n/a |

## 6 Simplicity gate (task 5)

- `place.rot` exists only to state K7-B20, and no live row uses it. It costs one argument through one function (`radial_corners`), and both of its paths are covered (M11, M12). Keep.
- `x1_lint` runs with every sN run and every `--stale`: about 0.1 s for a premise four rules depend on. Keep.
- The `--accept` JSON field diff and positional line diff are print-only, about 15 lines. Keep. The positional summary diff is cosmetic (Engineer step 0 open item 3).
- NOTE 2 (dead code) and NOTE 3 (baseline history) are the two items that cost more than they protect.

## 7 Findings

**FIX 1 (4g annulus containment has no B).** Add two drawing-only Bs to builders.py, each drawn with `_s2_replace(_s2_ctx(), fid, ...)` as an Annulus about the axis. Probe on the current code (MEASURED): each fires 1 issue.
- `K8-B24`: gear drawn with outer radius OD/2 + 5. Reason `["load/gear plan_extent", "(by 5.00)"]`, planted 1.
- `K8-B25`: bearing drawn with bore radius bore/2 - 5. Reason `["load/bearing plan_extent", "(by 5.00)"]`, planted 1.

**FIX 2 (sector drawn wider than its wedge has no B).** Add `K8-B26`: `k8_b23` with half_angle 50. Probe (MEASURED): 1 issue, "load/operator_sector sector: drawn wedge differs from the spec wedge (theta 90, half-angle 45, r 400): 34.86 outside, spec boundary 0.00 outside the drawing". Reason `["operator_sector sector", "34.86 outside"]`, planted 1. Hand: 400 sin 5 = 34.86 (DERIVED).

**FIX 3 (S2-6 notch-clearance branch has no B).** Live member c sits 5.00 from the plate edge against notch_clear 5 (MEASURED), so the Z is on its bound. Add `S2-6-B2`: `_shift(_s2_ctx(), "frame_upper_c", 2, 0)`. Probe (MEASURED): 1 issue, "frame_upper_c: 3.00 from the plate edge in the notch, want 5". Reason `["frame_upper_c: 3.00 from the plate edge in the notch, want 5"]`, planted 1. NOTE: the Z on its bound is a design identity (member c is centred in the notch), the same as S1-1.

**FIX 4 (`--accept` harness copy-up: silent skip, no control).**
- `accept()`: when wip/ holds a controls results file with any row not matched, refuse before the flag is set, with "refused: wip/ controls results: N mismatched", and write nothing. A wip/ folder with no controls results keeps today's behaviour.
- `H1-Z3`: H1-Z1 plus a matched wip/ `fixtures/controls_results.json` and `baseline_red.json`. After the accept, both are byte-equal in docs/.
- `H1-B6`: the same with one row `match: "no"`. Accept refused, docs/ unchanged, reason `["refused", "controls results", "1 mismatched"]`, planted 1.
- Two people commit from this tree. A revision accepted on a red harness is the exact failure the controls exist to stop.

**FIX 5 (one-sided and half-premise branches with no B). Three fixtures. Probes on the current code each fire as stated (MEASURED).**
- `K8-B27` (r4 rule, low-x end): motor_shaft_a drawn 15 longer at its low-x end only (`set_x(x - 15)`, `set_width(w + 15)`). Fires 8: projected_x and projected_extent at each of four poses. Reason `["load/motor_shaft_a projected_extent", "(by 15.00)", "projected_x"]`, planted 8.
- `K5-B12` (r2 rule, bore_cone lower bound): holder bore_cone piece drawn 10 to 5 below the collet bottom at capture_end. 1 issue, "capture_end/holder: bore_cone trapezoid z [90.00, 95.00] outside mate collet z [100.00, 132.00]", planted 1.
- `K5-B13` (TP-13 hub width; the Topologist signs): pinion_a hub drawn on the heel with half-width w + 5. 1 issue, "load/pinion_a: hub rectangle u [125.00, 140.00], half-width 50.62 not on the heel of the toothed piece (u 125.00, half-width 45.62)". Reason `["load/pinion_a: hub rectangle", "half-width 50.62"]`, planted 1.

Expected after P5f: 187 controls (Z 56, B 129, smoke 2), all matched. Run 2 is unchanged (17/17 s1, 17/17 s2). The new Z is H1-Z3; the new Bs are K8-B24 to B27, S2-6-B2, H1-B6, K5-B12 and K5-B13.

**NOTE 1.** The K9 pose-set Text branch (M10) has no B. A bare row-id Text appears only through a script bug, since labels carry `label:`. Optional B: a Text with gid core_750 at park.
**NOTE 2.** K8 has dead code. The `if plan:` blocks for projected_y and projected_extent_y, both in the placed branch and in the plan_poly branch, sit inside `side` conditions, and SIDE_VIEWS excludes plan_xy. Delete them; plan containment is plan_extent.
**NOTE 3.** `baseline_red.json` now carries 9 dated prior records (wip/ copy 399 KB, all from 2026-11-24 and 25), and each `--baseline` adds one more. Git already keeps every committed version. Keep the prior record only when a sketch's run 2 result set changes, or drop `prior`.
**NOTE 4.** In the 4f lint, a None outline at one pose skips the row's later poses, and `sector` rows are outside the lint. Both are harmless on the signed S2 spec.
**NOTE 5.** `artist_polys` does not flatten Collections. A PatchCollection of circles at P6 would read control points and fire K8 as a false red (210.086 for r 210). Draw plan circles as patches, or route Collection paths through `flatten_path`.
**NOTE 6.** Engineer step 0 Correction 2 (c <= 42.34) and Correction 3 (`depends on symbol c`) are outside the harness review and stay with the Loftsman and Sean.

FIX (5 items: FIX 1 to FIX 5). SW-17 SIGNED. The code of 4f, 4g and curve flattening is reviewed: sound, with the 4g annulus gap at FIX 1.

## Gameplan lines to change

**l.124** (accept sentence), fragment. Apply after FIX 4 lands.

Old:
```
refuses on an absent record, a check not pass, an empty note or a PNG differing in pixels from an accepted one,
```
New:
```
refuses on an absent record, a check not pass, an empty note, a PNG differing in pixels from an accepted one or a wip/ controls results file with any control not matched (1.2 (c) SW FIX 4, H1-Z3, H1-B6),
```

**l.139** (K5 row, B cell end). Apply after FIX 5 lands.

Old:
```
K5-B11 pinion hub 5 off the heel |
```
New:
```
K5-B11 pinion hub 5 off the heel; K5-B12 bore_cone piece below the collet bottom; K5-B13 pinion hub wider than the heel |
```

**l.142** (K8 row, B cell end). Apply after FIX 1, FIX 2 and FIX 5 land.

Old:
```
B22 pinion teeth widening inward; B23 sector drawn at half-angle 40 |
```
New:
```
B22 pinion teeth widening inward; B23 sector drawn at half-angle 40; B24 gear drawn 5 over its section OD; B25 bearing drawn with its bore 5 under its section; B26 sector drawn at half-angle 50; B27 motor shaft 15 longer at its low-x end |
```

**l.146** (control pointer), end fragment. Apply after P5f; the Engineer fills in the measured time.

Old:
```
(178 controls: Z 55, B 121, smoke 2; 264 s).
```
New:
```
(178 controls: Z 55, B 121, smoke 2; 264 s). Step 1.2 (c) Software Engineer check (FIX 1 to 5) added H1-Z3, H1-B6, K5-B12, K5-B13, K8-B24 to B27 and S2-6-B2 (187 controls: Z 56, B 129, smoke 2).
```

**l.259** (S2-6 row, B cell). Apply after FIX 3 lands.

Old:
```
| Member c at radius 300 (26 off the plate edge) |
```
New:
```
| Member c at radius 300 (26 off the plate edge); member c drawn 2 toward the notch edge (3.00 against notch_clear 5, S2-6-B2) |
```

**l.575** (Design Notes 20, SW-17 row).

Old:
```
| SW-17, TP-13 | K5 plan-view B control; radial-axis plan rule | 1.2 (S2) | The Engineer |
```
New:
```
| SW-17, TP-13 | K5 plan-view B control; radial-axis plan rule | 1.2 (S2); SW-17 written at 1.2 (c) as K5-B7, signed by the Software Engineer 1.2 (c) | The Engineer |
```

**l.616** (H6 row).

Old:
```
| H6 | Harness delta since the Software Engineer's 1.1 (c) check: 18 controls (r2 to r4) and the plan-contact, projected_extent, section-N, pose-set, bore_cone, stack_ties and `place.rot` rules, reviewed so far by the Loftsman and The Topologist only | 1.2 (c), before the S2 stub run | The Software Engineer |
```
New:
```
| H6 | Harness delta since the Software Engineer's 1.1 (c) check: 18 controls (r2 to r4) and the plan-contact, projected_extent, section-N, pose-set, bore_cone, stack_ties and `place.rot` rules, reviewed so far by the Loftsman and The Topologist only | 1.2 (c), checked by the Software Engineer: 18 controls real; branch gaps projected_extent low-x end and bore_cone lower bound (FIX 5), pose-set Text branch (NOTE 1) | The Software Engineer |
```
