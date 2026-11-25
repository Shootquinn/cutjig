# Step 1.2 (c) Engineer fix pass (P5f): sign-off FIXes and Software Engineer check FIX 1 to 5

## Corrections to the brief

1. **Control IDs.** The Topologist (TP1.2-1) and the Software Engineer (FIX 1, gear) both named K8-B24, and the gameplan K8 row already carries the Topologist's K8-B24. The Topologist keeps K8-B24. The Software Engineer's K8-B24 to B27 shift up by one, to K8-B25 to B28. Mapping in section 2.
2. **LF-c1 live scope.** The Loftsman expected two new swept tests per sketch (ring|descent_stop, nut_housing_a|descent_stop). That holds for S2: 1278 to 1280 plan tests (MEASURED). S1 gains **94** side-view swept tests: the S1-5b base group (`s1_5b_base`, G 10 at capture_end against collet, holder, wing nut, receiver, collar, base plate and base frame) is pose-restricted on every ring-assembly row, so each such pair is now swept as F. K7 on live S1 goes from 515 to 609 tests, still clean (MEASURED). No verdict changes on either sketch.
3. **LF-c1 side branch has its own B.** The Loftsman asked for one control, K7-B30, which is plan. Removing the side-view change leaves K7-B30 matched (MEASURED, mutation `pre_K7side`). Detail 1 common (h) needs a B per branch, so K7-B31 is added: the K7-B4 side fixture with its G 10 declaration restricted to p4.
4. **FIX R1 exemption.** The rule "exempt only a revision accepted before the rule with no not_drawn entries" needs no exemption code. A spec with no not_drawn entry has nothing to name, so `figure_note_issues` returns no issue for it whatever its sketch id. Only S1 r4 qualifies, and it qualifies on its empty not_drawn. The sketch-id test is deleted.
5. **Gameplan state.** The gameplan already carries several 1.2 (c) lines from the raisers' files: K4 row check text from S2 on (Designer's pre-FIX-R1 wording), K5 B12 and B13, K7 LF-c1 wording and B30, K8 TP1.2-1 wording and B24, l.124 refusal text, l.146 "(187 controls ...)", l.259 S2-6-B2. Section 6 gives Old text copied from the current file.

Tags: run results MEASURED 2026-11-25 on `docs/sketches/`. Hand values DERIVED.

## 1 Per-finding disposition

| Finding | Raiser | Change | Control(s) | Pre-fix or branch-deleted (MEASURED) | Fixed code (MEASURED) |
|---|---|---|---|---|---|
| FIX R1 figure-note exemption by sketch id | Designer | `sketch_common.figure_note_issues`: sketch-id exemption deleted; `s1_spec.yaml` top-level `figure_note: "Not drawn: LM20UU bushing (inside the housing and lug)"`; `s1_side_poses.py` draws it as Text gid `note:figure_note` on each of the four pose figures; `place_labels` notes take an optional gid; `builders._s1_draw_pose` draws the note | K4-B6 (S1 r5 spec, figure_note removed) | clean (`pre_K4`: S1 exempt) | fires 1, "spec error: not_drawn (1) without figure_note" |
| FIX LF-c1 swept form, plan | Loftsman | `_k7_plan`: `all_decl` holds declarations without poses only; the swept relation reads declarations without poses; a pair declared with poses only is swept as F; N excepted | K7-B30 (K7-B29 bar, G 10 at p4 only) | clean (`pre_K7plan`) | fires 1, "swept p1..p4/ring\|bar F: swept outline plan distance 0.000 mm, overlap 400.000 mm2" |
| FIX LF-c1 swept form, side | Loftsman | `k7` swept loop: a neighbour with poses becomes F, g_min 0, once per b, unless the pair is also declared without poses; N excepted | K7-B31 (K7-B4 member, G 10 at p4 only) | clean (`pre_K7side`) | fires 1, "swept p1..p4/ring\|member F: swept hull distance 0.000 mm, overlap 2000.000 mm2" |
| FIX TP1.2-1 radial outboard in a side view | Topologist | `k8`: radial outboard form only when the view is plan_xy; outside plan_xy a predicate with `frame: radial` is reported once as "spec error: frame radial needs plan_xy" and skipped (the side form stays the only side-view outboard test) | K8-B24 (live S1, `frame: radial` on motor23_a outboard) | clean (`pre_K8`; 346 predicates hold) | fires 1, "motor23_a outboard of pinion_a: spec error, frame radial needs plan_xy (view side_xz)" |
| SW FIX 1 annulus containment | Software Engineer | none (fixtures only) | K8-B25 gear OD / 2 + 5; K8-B26 bearing bore 5 under | both clean (`annulus_off`) | each fires 1, "load/gear plan_extent ... (by 5.00)", "load/bearing plan_extent ... (by 5.00)" |
| SW FIX 2 sector wider than its wedge | Software Engineer | none | K8-B27 (half-angle 50) | clean (`sector_dout_off`); K8-B23 still fires | fires 1, "34.86 outside, spec boundary 0.00 outside the drawing" (400 sin 5 = 34.86, DERIVED) |
| SW FIX 3 S2-6 notch clearance | Software Engineer | none | S2-6-B2 (member c +2 in x) | clean (`notch_off`) | fires 1, "frame_upper_c: 3.00 from the plate edge in the notch, want 5" |
| SW FIX 4 `--accept` on a red harness | Software Engineer | `check_sketch.accept`: after the PNG check and before the flag, a wip/ controls results file with any row not matched refuses with "refused: wip/ controls results: N mismatched", writes nothing; no wip/ controls file keeps today's behaviour | H1-Z3 (matched file and baseline copied up byte-equal); H1-B6 (one row match no) | H1-B6 clean, record flagged and copied (`pre_accept`); H1-Z3 matched | H1-Z3 clean; H1-B6 fires 1, "refused: wip/ controls results: 1 mismatched", record not flagged, docs/ holds only the pre-existing PNG |
| SW FIX 5 projected_extent low-x end | Software Engineer | none | K8-B28 (motor_shaft_a 15 longer at low x) | 4 issues against planted 8, reason lacks "projected_extent" (`lowx_off`) | fires 8: projected_x (centre -121.38 vs -113.88) and projected_extent (by 15.00) at four poses |
| SW FIX 5 bore_cone lower bound | Software Engineer | none | K5-B12 (piece z 90 to 95 under the collet 100 to 132) | clean (`borecone_low_off`); K5-B6 still fires | fires 1, "capture_end/holder: bore_cone trapezoid z [90.00, 95.00] outside mate collet z [100.00, 132.00]" |
| SW FIX 5 TP-13 hub width | Software Engineer | none | K5-B13 (hub on the heel, half-width w + 5) | clean (`hubwidth_off`); K5-B11 still fires | fires 1, "hub rectangle u [125.00, 140.00], half-width 50.62 not on the heel ... (u 125.00, half-width 45.62)" |

Every new B fires on the raiser's reason text and count as the raiser probed it: Designer "without figure_note"; Loftsman "swept ... ring|bar F", plan overlap 400 > 0.01; Topologist "frame radial needs plan_xy", 1; Software Engineer the exact strings and counts in his section 7 (8 for the low-x B).

Mutation method: a fresh copy of `docs/sketches/` (no wip/) in the scratchpad with `params.yaml` one level above, one exact-string replacement per run, the named manifest entries run through `check_sketch.run_control` and `compare`. The pre-fix mutations restore the old line; the branch mutations delete the branch as the Software Engineer did (M04, M05, N19, M15, M09, M18, N21).

## 2 Control ID mapping

| Final ID | Raised as | Raiser, finding |
|---|---|---|
| K4-B6 | "one B control" (no ID) | Designer FIX R1 |
| K5-B12 | K5-B12 | Software Engineer FIX 5 |
| K5-B13 | K5-B13 | Software Engineer FIX 5 |
| K7-B30 | K7-B30 | Loftsman LF-c1 (plan) |
| K7-B31 | none (added, section Corrections 3) | Loftsman LF-c1 (side) |
| K8-B24 | K8-B24 | Topologist TP1.2-1 |
| K8-B25 | K8-B24 | Software Engineer FIX 1 (gear) |
| K8-B26 | K8-B25 | Software Engineer FIX 1 (bearing) |
| K8-B27 | K8-B26 | Software Engineer FIX 2 (sector 50) |
| K8-B28 | K8-B27 | Software Engineer FIX 5 (low-x end) |
| S2-6-B2 | S2-6-B2 | Software Engineer FIX 3 |
| H1-Z3 | H1-Z3 | Software Engineer FIX 4 |
| H1-B6 | H1-B6 | Software Engineer FIX 4 |

13 new controls: Z 1, B 12.

## 3 Runs

| Run | Result (MEASURED) |
|---|---|
| `check_sketch.py --controls` (background) | exit 0, **191/191 matched**: Z 56/56, B 133/133, smoke 2/2, 295 s (178 before; +13). `wip/fixtures/controls_results.json`. The machine also ran mutation copies for part of the time |
| `check_sketch.py s1 --rev 5` (S1 r5 preview) | exit 0, 18/18 pass (K1 to K9, S1-1 to S1-7, X1), 14 s. K4 "55 label(s) carry their key value; figure note names every not_drawn part". K7 609 tests clean. Record `wip/s1_checks_r5.json` |
| `s1_side_poses.py --rev 5` | four PNGs in `wip/`; "Not drawn: LM20UU bushing (inside the housing and lug)" in the margin column under the axial-loop note (load pose inspected) |
| `check_sketch.py s2 --rev 0` (S2 stub) | exit 1, 5.5 s. Green: K1, K2, K3, K5, X1. Red content: K4 (15), K9 (69). Red absent: K6 (68), K7 (**1280**, was 1278: the two LF-c1 swept pairs), K8 (112), S2-1 to S2-6 (1 each). Result and cause per check equal the r0 record before the fix |
| Run 2 for s2, in-process against STUB_EXPECT / STUB_CAUSE | 17/17 |
| `check_sketch.py s1 --rev 0` to a scratch wip dir | result and cause per check equal the committed `s1_checks_r0.json` (17 checks); counts differ because that record predates the r5 spec. `--baseline` not re-run (Software Engineer NOTE 3) |

## 4 Files changed

- `docs/sketches/sketch_common.py`: `figure_note_issues` (FIX R1); `place_labels` notes with optional gid (FIX R1); `k7` side swept loop and `_k7_plan` swept relation and `all_decl` (LF-c1); `k8` radial outboard gate and spec-error lint (TP1.2-1).
- `docs/sketches/check_sketch.py`: `accept` wip/ controls refusal (SW FIX 4).
- `docs/sketches/s1_spec.yaml`: top-level `figure_note` (FIX R1).
- `docs/sketches/s1_side_poses.py`: figure note Text on each pose figure (FIX R1).
- `docs/sketches/fixtures/builders.py`: `_s1_draw_pose` figure note; `k4_b6`, `k5_b12`, `k5_b13`, `k7_b30`, `k7_b31`, `k8_b24` to `k8_b28`, `s2_6_b2`, `_annulus_row`.
- `docs/sketches/fixtures/step0_fixtures.py`: `h1_z_harness_copy`, `h1_b_controls_mismatch`, `_harness_wip`.
- `docs/sketches/fixtures/manifest.yaml`: 13 rows.

Not changed: s2_spec.yaml, checks_s1.py, checks_s2.py, check_stack.py, sketch_loader.py, the committed records under `docs/sketches/`. Software Engineer NOTEs 1 to 6 are not FIXes and stay open (NOTE 2 dead code, NOTE 3 baseline history, NOTE 5 Collections).

## 5 Open

- Re-signature: Designer (exemption line, S1 spec field, K4-B6), Loftsman (swept form, K7-B30, K7-B31), Topologist (K8 gate, K8-B24); Software Engineer re-check (P5 TASK 0).
- Loftsman 1.2 (c) lines for the 1.3 entry gate (NOTE 2) and detail 1 common (h) (NOTE 3) are in his file and outside this pass.

## Gameplan lines to change

**l.124** (accept and baseline sentence, end fragment).

Old:
```
(Z and B controls: H1-Z1, H1-Z2, H1-B1 to H1-B5).
```
New:
```
(Z and B controls: H1-Z1 to H1-Z3, H1-B1 to H1-B6).
```

**l.138** (K4 row, check cell end; Designer FIX R1 wording, re-based on the current text).

Old:
```
from S2 on, the spec figure_note and the drawn Text note:figure_note name the head (text before " (" or " at ") of every not_drawn part (1.2 (c), Designer 1.2 (b) FIX 3) |
```
New:
```
from S2 and S1 r5 on, the spec figure_note and the drawn Text note:figure_note name the head (text before " (" or " at ") of every not_drawn part; only a revision accepted before the rule with no not_drawn entry is exempt (1.2 (c), Designer 1.2 (b) FIX 3, Designer 1.2 (c) FIX R1) |
```

**l.138** (K4 row, full control-list cell).

Old:
```
B1 label without a number; B2 label "tube OD 150" against `drill.tube_od` 152.4; K4-B4 drawn note without the LM20UU bushing; K4-B5 a not_drawn part in neither note |
```
New:
```
B1 label without a number; B2 label "tube OD 150" against `drill.tube_od` 152.4; K4-B4 drawn note without the LM20UU bushing; K4-B5 a not_drawn part in neither note; K4-B6 S1 r5 spec with not_drawn and no figure_note (FIX R1) |
```

**l.139** (K5 row, full control-list cell). The current cell is final (K5-B12, K5-B13 already applied); no change. Current text for reference:
```
B1 drill tube as Circle in XZ; B2 bevel pinion as rectangle in side view; B3 untagged patch; K5-B6 bore_cone piece above the collet top; K5-B7 drill tube as a rectangle in plan (SW-17); K5-B8 NEMA 23 as a circle in plan; K5-B9 NEMA 23 rectangle 10 deg off radial; K5-B10 radial-axis row with a round footprint; K5-B11 pinion hub 5 off the heel; K5-B12 bore_cone piece below the collet bottom; K5-B13 pinion hub wider than the heel |
```

**l.141** (K7 row, side-view swept clause).

Old:
```
(a pair declared with `poses` is swept as undeclared F, N excepted; Loftsman 1.2 (c) LF-c1)
```
New:
```
(a pair declared with `poses` only is swept as undeclared F, N excepted; Loftsman 1.2 (c) LF-c1, K7-B31)
```

**l.141** (K7 row, full control-list cell).

Old:
```
B1 1 mm overlap fires every class; B2 1 mm gap on a C pair fires; B3 a G pair at g_min - 1 fires; B4 a horizontal fixed member at mid-stroke inside the ring outline, clear of all four poses, fires in the swept case; B5 a C pair touching in XZ with depth bands 490 mm apart fires; B6 a G pair (g_min 10) with depth bands 1 mm apart, overlapping in XZ, fires; B11 to B13 (1.1 (b)); B14 collet\|holder N between section rows; B15 the r1 holder interference; B16, B17 plan-contact footprints 1 mm apart and 1 mm into; B18, B19 live descent-stop post and anchor arm 1 mm off; B20 a member turned 45 deg (corner 12.43 into the arm); B21 live S1 tie a strip to the member centre (plan_poly plan-contact); B22 plan 1 mm overlap on F; B23 plan G at g_min - 1; B24 plan C z-separated by 100; B25 pad 1 mm into its post (interference); B26 z-contact on a circumscribing footprint; B27 bearing OD 1 into the ring bore; B28 plan outline moving with the pose in one figure; B29 swept plan: fixed bar inside the ring annulus within the sweep; B30 swept plan: fixed bar mid-stroke declared G with poses [capture_end] against the ring, swept as F (LF-c1) |
```
New:
```
B1 1 mm overlap fires every class; B2 1 mm gap on a C pair fires; B3 a G pair at g_min - 1 fires; B4 a horizontal fixed member at mid-stroke inside the ring outline, clear of all four poses, fires in the swept case; B5 a C pair touching in XZ with depth bands 490 mm apart fires; B6 a G pair (g_min 10) with depth bands 1 mm apart, overlapping in XZ, fires; B11 to B13 (1.1 (b)); B14 collet\|holder N between section rows; B15 the r1 holder interference; B16, B17 plan-contact footprints 1 mm apart and 1 mm into; B18, B19 live descent-stop post and anchor arm 1 mm off; B20 a member turned 45 deg (corner 12.43 into the arm); B21 live S1 tie a strip to the member centre (plan_poly plan-contact); B22 plan 1 mm overlap on F; B23 plan G at g_min - 1; B24 plan C z-separated by 100; B25 pad 1 mm into its post (interference); B26 z-contact on a circumscribing footprint; B27 bearing OD 1 into the ring bore; B28 plan outline moving with the pose in one figure; B29 swept plan: fixed bar inside the ring annulus within the sweep; B30 swept plan: fixed bar mid-stroke declared G against the ring at the last pose only, swept as F (LF-c1); B31 swept side view: the B4 member declared G against the ring at the last pose only, swept as F (LF-c1) |
```

**l.142** (K8 row, full control-list cell; Software Engineer's B24 to B27 renumbered B25 to B28).

Old:
```
B1 drill flipped tip-up; B2 a screw with its anchor above the nut; B3 plan view with the y axis inverted; K8-B14 tooth face falling outward; K8-B15 anchor arm 20 wider at each end; K8-B16 motor shaft 15 wider at each end; B17 live S1 tie a drawn 10 wider than its plan_poly extent; B18 live S2 y inverted; B19 screws at -theta (azimuth clockwise); B20 NEMA 23 a 10 wider; B21 NEMA 23 c inboard of its pinion; B22 pinion teeth widening inward; B23 sector drawn at half-angle 40; B24 live S1 outboard with frame: radial in a side view (TP1.2-1) |
```
New:
```
B1 drill flipped tip-up; B2 a screw with its anchor above the nut; B3 plan view with the y axis inverted; K8-B14 tooth face falling outward; K8-B15 anchor arm 20 wider at each end; K8-B16 motor shaft 15 wider at each end; B17 live S1 tie a drawn 10 wider than its plan_poly extent; B18 live S2 y inverted; B19 screws at -theta (azimuth clockwise); B20 NEMA 23 a 10 wider; B21 NEMA 23 c inboard of its pinion; B22 pinion teeth widening inward; B23 sector drawn at half-angle 40; B24 live S1 outboard with frame: radial in a side view (TP1.2-1); B25 gear drawn 5 over its section OD; B26 bearing drawn with its bore 5 under its section; B27 sector drawn at half-angle 50; B28 motor shaft 15 longer at its low-x end only |
```

**l.146** (control pointer, end fragment).

Old:
```
Step 1.2 (c) Software Engineer check (FIX 1 to 5) added H1-Z3, H1-B6, K5-B12, K5-B13, K8-B24 to B27 and S2-6-B2 (187 controls: Z 56, B 129, smoke 2).
```
New:
```
Step 1.2 (c) fix pass P5f (Designer FIX R1, Loftsman LF-c1, Topologist TP1.2-1, Software Engineer FIX 1 to 5; `research/sean/cr_scratch/step1.2_engineer_redfirst_fixes.md`) added K4-B6, K5-B12, K5-B13, K7-B30, K7-B31, K8-B24 to B28, S2-6-B2, H1-Z3 and H1-B6 (191 controls: Z 56, B 133, smoke 2; 295 s).
```

**l.488** (Progress Log, add a row after it).

Old:
```
| 1.2 | 2026-11-25 | (c) raiser signatures: Designer 4 of 5 SIGNED (figure-note check FIX R1); Loftsman SIGNED except swept plan form (FIX LF-c1); Topologist TP-13 SIGNED, FIX TP1.2-1 (radial outboard in side views); Software Engineer SW-17 SIGNED, check FIX 5 (annulus and sector containment B, S2-6 notch B, --accept copy-up refusal, TP-13 hub-width B); 178/178 re-run. Next: P5f Engineer fix pass. |
```
New:
```
| 1.2 | 2026-11-25 | (c) raiser signatures: Designer 4 of 5 SIGNED (figure-note check FIX R1); Loftsman SIGNED except swept plan form (FIX LF-c1); Topologist TP-13 SIGNED, FIX TP1.2-1 (radial outboard in side views); Software Engineer SW-17 SIGNED, check FIX 5 (annulus and sector containment B, S2-6 notch B, --accept copy-up refusal, TP-13 hub-width B); 178/178 re-run. Next: P5f Engineer fix pass. |
| 1.2 | 2026-11-25 | P5f fix pass (`step1.2_engineer_redfirst_fixes.md`): Designer FIX R1 (S1 sketch-id exemption removed; S1 r5 figure_note drawn on four poses), Loftsman LF-c1 (pose-restricted pairs swept as F, plan and side; S1 +94 swept tests, S2 +2, all clean), Topologist TP1.2-1 (radial outboard plan_xy only), Software Engineer FIX 1 to 5; 13 controls, Software Engineer K8-B24 to B27 renumbered K8-B25 to B28; 191/191 matched; S1 r5 preview 18/18; S2 stub 17/17. Next: raiser re-signs, P5 re-check. |
```

**l.259** (S2-6 row): none; S2-6-B2 is already in the row.

