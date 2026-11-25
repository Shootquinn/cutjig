## Corrections to the brief

1. **The swept plan form never tests a pose-restricted pair.** `_k7_plan` drops a neighbour that carries `poses` from the swept loop (`nb["class"] in ("C", "N") or nb.get("poses"): continue`). The undeclared-F branch also skips every pair in `all_decl`, and that set includes pairs declared at one pose only. So a pair declared at capture_end is tested at no swept position, although the K7 rule says it "counts as declared only at those poses; elsewhere the pair takes the undeclared-F test". The side-view swept loop (l.1538 to 1540, signed at 1.1) has the same hole. Live S2 has two such moving/fixed pairs, ring|descent_stop C and nut_housing_a|descent_stop G 10, both at capture_end. Swept as F they read: ring/pad sweep band 374.84 to 1161.84 z_S against pad 362.84 to 374.84, z-touch; housing/pad plan 14.99 with no overlap, F. Both pass, so no live verdict changes. MEASURED (code read; outline_measure on s2_live).
2. Engineer Correction 3 holds by hand. The lift motor 42 square with faces radial and tangential sits 160 sin 15 - 21 (cos 15 + sin 15) = 41.411 - 21 x 1.2247 = 41.411 - 25.719 = **15.69** from the 135 deg edge. The circumscribing outline gives 41.411 - 29.698 = **11.71**. DERIVED.

## 1 Controls re-run

Run in-process through `check_sketch.run_control` and `compare` on the live manifest, 33.6 s, all MATCH (MEASURED):

| Control | Result | Reason (excerpt) |
|---|---|---|
| K7-Z12 | clean, F | 1 pair, F |
| K7-Z13 | clean, z-contact | pad on post |
| K7-Z14 | clean | ring/tube undeclared F, bearing in bore plan-contact |
| K7-Z15 | clean | 1278 tests, 4 poses |
| K7-B20 | fires 12 / planted 12 | tie_b/member_a bands 3.111 apart; arm overlaps 154.416 |
| K7-B21 | fires 4 / 4 | tie_a/member_b overlap 1655.177 |
| K7-B22 | fires 1 | F, 60.000 mm² overlap |
| K7-B23 | fires 1 | G, lower bound 9.000, g_min 10 |
| K7-B24 | fires 1 | C z-separated 100.000 |
| K7-B25 | fires 1 | interference 900.000 mm² |
| K7-B26 | fires 1 | circumscribing outline, z-contact refused |
| K7-B27 | fires 1 | interference 631.460 mm² |
| K7-B28 | fires 1 | outline differs 15.00 between poses |
| K7-B29 | fires 1 | swept ring/bar, plan distance 0, overlap 400 |
| K6-Z4 | clean | 69 centres within 0.05 |
| K6-B8 | fires 1 | member c t 6.75 off |
| K6-B9 | fires 1 | load_plane: no owner spec with an equal field |
| X1-Z | clean | 47 compared; 3 skipped (base_frame, base_plate plan_poly; keepout place) |
| X1-B1, X1-B2 | fire 1 each | frame_upper_b place.r_in; nut_a z_rule.z_max |

## 2 Hand checks

| Item | Hand (DERIVED) | Code (MEASURED, s2_live outlines) |
|---|---|---|
| gear section: gear.bore / 2 to gear.od / 2 | 180 / 2 = 90.00 to 252.64 / 2 = 126.32 | annulus (90.0, 126.32), true |
| gear_hub: drill.tube_od / 2 to gear.bore / 2 | 76.20 to 90.00 | (76.2, 90.0) |
| gear/hub | contact at r 90, overlap 0 | 0.000 / 0.000 |
| gear/drill_tube | 90 - 76.20 = 13.80 | 13.800 |
| ring/bearing (bore 100) | contact at r 100 | 0.000 / 0.000 |
| K7-B27: bearing OD 1 into the ring bore | pi (101² - 100²) = pi x 201 = 631.46 | 631.460 |
| pad/post: r 200 to 215 x 60 | 15 x 60 = 900.00, z touch | 900.000, z-contact |
| member c/base_plate pieces | 35 - 30 = 5.00 | 5.000 |
| ring/member c | 244 - 210 = 34.00 | 34.000 |
| ring/guide rod | 230 - 10 - 210 = 10.00 | 10.000 |
| K7-B20 extra 4: member a turned 45 deg, y min 137 - 42.43 sin 60 = 100.26 against tie b y max 97.15 | 3.11 | 3.111 |
| K6-B8 | 6.75 off in t at theta 270 | t 6.75 |

Annulus against a piece (`_annulus_vs_polys`). The distance is exact: a convex piece's radii form one interval, so an intersection with [a, b] puts a point of the piece in the annulus. The area is the piece against the 128-gon about b, less the piece against the 128-gon about a. The inner 128-gon reaches a / cos(pi / 128) = 1.000301 a, so overlap inside a + 0.0301 a can be under-read (0.03 at r 100). That lies within TOL_C, so the method is sound.

## 3 Rulings

| Rule | Ruling | Basis |
|---|---|---|
| LF-8 plan outlines (`plan_outline`): annulus, footprint polygon, plan_poly pieces, depth-band disk, drawn fallback | **SIGNED** | Outlines contain their parts. Held round the drawing by K6 plan centre and K8 plan_extent. The true flag is false for circumscribing outlines (lift motor round with a rectangle projection; pinion radial with a trapezoid projection; depth disk). |
| z-band rules: F z-separated and z-touch, G max(z gap, plan distance), C z-separated fails | **SIGNED** | F forbids common volume only (class definition "overlap 0"). Touching bands within TOL_C leave no common volume. This is the plan analogue of the LF-1 rule. NOTE 1. |
| Plan C rule (z-contact, plan-contact, interference) and its true-section premise | **SIGNED** | The three states partition the C cases. Both passes need `true` on both outlines, which K7-B26 holds. plan_poly pieces count as true: the uncut plate holes can only over-read overlap, so a wrong result would be a false fail and never a false pass. |
| Annulus form (4d) | **SIGNED** | Annulus pairs are exact. Annulus against a piece is as in section 2. K7-Z14 and B27. |
| One-figure premise (4f) | Raised by the Engineer, signed at (e). From the geometry side: **sound**. K7-B28 fires on a pose-reading r_in. | n/a |
| Swept plan form | **NOT SIGNED**, FIX LF-c1 | Correction 1 |
| K6 plan centre | **SIGNED** | The radial-frame mid-extent equals r_c for rectangles, axis-symmetric trapezoids with their hub (pinion 95.22 to 140, mid 117.61 = r_c), circles and footprints turned about their centre. plan_poly, sector and axis rows use the xy mid-extent. |
| LF-16 owner rule (relaxed) | **SIGNED** | The premise (another spec has the row and an equal field) is checked by `_plane_owner`, B9. The numeric agreement runs where the row is drawn: the s1 run lints both planes (S1 r5 preview 18/18). |
| X1 | **SIGNED** | Fields `place`, `z_rule`, `plan_poly`. A field in one spec only is skipped and listed. An exemption needs a reason. Z, B1 and B2 match. |
| S2 gear `section` edit (with the Designer) | **SIGNED (Loftsman)** | 90.00 to 126.32 by hand. No key or class change. `section` is outside X1 (gear has no plain section in S1), which is correct. The Designer signs the shape side. |

**FIX LF-c1 (swept form, plan and side).** A neighbour declared with `poses` is tested in the swept case as undeclared F (g_min 0). N pairs are still excepted. A pair declared at every pose keeps its class, as now. In the plan branch, `all_decl` excludes pose-restricted declarations. In the side branch, the pose-restricted pair joins the swept loop as F.
- New B, K7-B30: a fixed bar mid-stroke, inside the ring annulus in plan and inside the sweep in z, declared `{class: G, g_min: 10, poses: [capture_end]}` against the ring and clear at all four poses. It must fire "swept ... ring|bar F" with plan overlap > 0.01. On the current code it reads clean.
- Expected live change: S2 and S1 each gain the swept tests ring|descent_stop (z-touch) and nut_housing_a|descent_stop (F, 14.99). Both pass, and no verdict moves.

## 4 Open NOTES from my 1.2 (b) sign-off

- **NOTE 2 (member-top stack tie) need not land before (d).** Today both leaves give 1225 (12 + 1213; 0 + 1225), and no (d) value reads a difference. It must land before S3 opens (detail 1.3): S3's L expression can move `jackscrew.length` and so `top_guide_z`. Neither leaf follows that change, and no drawn check sees member c's top (S1 does not draw member c; plan does not draw z).
- **NOTE 3 (K7 pair ids in the record) need not land before (d).** The r4 record has no ids, so the r4-to-r5 diff cannot use them whenever they land. It must land before the second drawn revision of any sketch (S2 r2 or S1 r6), so that the revision diff names the pairs that moved.

## 5 NOTES (new)

1. F z-touch admits up to 0.05 interpenetration in z over any plan area, and an undeclared part standing on another reads "undeclared:z-touch" with no C declaration demanded. The side view already admitted "undeclared:C" in the same way. Acceptable at sketch level. M1 should read undeclared z-touch pairs as contacts the spec did not name: 158 static and 2 swept on live S2.
2. The drill tube and keep-out are solid annuli (0 to 76.20, 0 to 86.20). The hollow tube (tube_id) is not modelled, so the outline is a containment bound. That is correct for F and G, and no C pair is claimed on the tube bore.

## Verdict

LF-8 plan K7: **SIGNED**, except the swept plan form, which is **NOT SIGNED** (FIX LF-c1, one control K7-B30, no live verdict change). K6 plan centre and the LF-16 owner rule: **SIGNED**. X1: **SIGNED**. Gear `section` edit: **SIGNED (Loftsman)**. NOTEs 2 and 3: not blocking (d). NOTE 2 must land before S3 opens; NOTE 3 must land before any second drawn revision.

## Gameplan lines to change

**l.141** (K table, K7 row, swept clause), two fragments.

Old:
```
in side views, per convex piece, the hull of that piece at the lowest and highest pose,
```
New:
```
in side views, per convex piece, the hull of that piece at the lowest and highest pose (a pair declared with `poses` is swept as undeclared F, N excepted; Loftsman 1.2 (c) LF-c1),
```

Old:
```
swept: each moving outline against every fixed row (declared F or G without poses, undeclared F) whose z band meets the sweep band
```
New:
```
swept: each moving outline against every fixed row (declared F or G without poses; undeclared, or declared with poses, as F; N excepted; LF-c1, K7-B30) whose z band meets the sweep band
```

**K7 row, B cell** (l.141), append after the last B control:

Old:
```
B29 swept plan: fixed bar inside the ring annulus within the sweep |
```
New:
```
B29 swept plan: fixed bar inside the ring annulus within the sweep; B30 swept plan: fixed bar mid-stroke declared G with poses [capture_end] against the ring, swept as F (LF-c1) |
```

**Open items, 1.3 entry gate** (detail 1.3, l.284 region): add, as a new bullet:
```
- Before S3 opens: stack tie frame_upper_a z_max = frame_upper_c z_max = jackscrew.top_guide_z + profile.height (Loftsman 1.2 (b) NOTE 2); S3 can move jackscrew.length.
```

**Detail 1 common (h)** (l.173), end fragment:

Old:
```
the raiser signs the rule before the revision goes to M1
```
New:
```
the raiser signs the rule before the revision goes to M1; before any sketch's second drawn revision, the K7 record carries the pair id beside each state (Loftsman 1.2 (b) NOTE 3)
```

---

## Re-sign after P5f

Inputs: research/sean/cr_scratch/step1.2_engineer_redfirst_fixes.md; docs/sketches/sketch_common.py (side swept loop l.1537 to 1556; `_k7_plan` `all_decl` l.1658 and swept relation l.1728 to 1749); fixtures/manifest.yaml.

### Corrections to the brief

1. **My live-scope estimate for LF-c1 was low for S1.** I predicted two new swept tests per sketch. S1 gains **94**, MEASURED by my own count over s1_spec.yaml of moving-to-fixed pairs declared with poses only and not also declared without poses. The breakdown: collar 14, and 13 each for base_plate, receiver, base_frame, wingnut, collet and holder; these are the pose-restricted S1-5b base group at capture_end, one pair per ring-assembly row. descent_stop adds 2 more. 515 + 94 = 609, as the Engineer reports. S2 gains 2, as predicted: swept:z-touch 2 to 3 (ring|descent_stop) and swept:F 154 to 155 (nut_housing_a|descent_stop, plan 14.99).

### Code check

- **Plan.** `all_decl` now holds only declarations without poses. The swept relation reads only declarations without poses, and an N declaration of either kind is collected into `rel_n` and excepted. A pair declared with poses only falls to the undeclared branch as F, g_min 0. A pair that also has a declaration without poses keeps that class (C and N skipped, F and G at their g_min). This is the LF-c1 rule as written.
- **Side.** A neighbour with poses becomes F, g_min 0, once per fixed row (`seen_pr`), unless the moving row also declares the pair without poses. N is excepted. A C declaration without poses is still skipped. The side loop reads only the moving row's own neighbour list. That scope comes from 1.1 and is unchanged. A pose-restricted declaration written only on the fixed row is not swept in the side view. Every S1 declaration of this kind sits on the moving row (count above), so nothing is lost today. NOTE 1.
- **States.** S1's new `swept:C` (1) is ring|descent_stop swept as F. The ring hull meets the pad top at distance 0 with overlap 0, which reads state C and passes F. That is consistent with the side-view F rule.

### Controls re-run (in-process, all MATCH, MEASURED)

| Control | Result |
|---|---|
| K7-B30 (plan) | fires 1: "swept p1..p4/ring\|bar F: swept outline plan distance 0.000 mm, overlap 400.000 mm2" |
| K7-B31 (side) | fires 1: "swept p1..p4/ring\|member F: swept hull distance 0.000 mm, overlap 2000.000 mm2" |
| K7-B4, K7-B29 (unrestricted G versions) | fire 1 each, unchanged |
| K7-Z10 (live S1) | clean, 609 tests (swept:F 139, swept:depth-separated 156, swept:plan-separated 6, swept:C 1) |
| K7-Z15 (live S2) | clean, 1280 tests (swept:F 155, swept:G 243, swept:z-separated 425, swept:z-touch 3) |
| K8-Z5 | clean, 346 predicates |

Hand: the B30 bar of 20 x 20 lies inside the ring annulus, so the overlap is the bar's full 400 mm² of plan area. B31's 2000 mm² is the K7-B4 member's overlap with the ring hull, unchanged from K7-B4. A separate B per branch is required under detail 1 common (h), and the Engineer's mutation `pre_K7side` showed B30 alone leaves the side branch unguarded.

### NOTE

1. Side swept scope: only the moving row's neighbour list is read. A future spec that writes a pose-restricted declaration only on the fixed row would escape the side sweep, where the plan branch reads both lists. This dates from 1.1, with no live case. When the side branch is next touched, read the fixed row's list as the plan branch does. Not blocking.

### Verdict

**SIGNED.** FIX LF-c1 is closed, plan (K7-B30) and side (K7-B31). With this, the swept plan form is SIGNED. Every rule in this file is now signed.

### Gameplan lines to change

none. The gameplan K7 row (l.141) already carries B30 (plan) and B31 (side) in the Engineer's wording, and that wording is correct. My earlier B30 line in this file is superseded and is not to be applied.
