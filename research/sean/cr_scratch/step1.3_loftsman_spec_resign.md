# Step 1.3 (b) spec re-sign after P2f (FIX 1 to 6), The Loftsman

Date 2026-11-26. Read: my sign-off `step1.3_loftsman_spec_signoff.md`, `step1.3_engineer_spec_fixes.md`, `docs/sketches/s3_spec.yaml` (header, chains, s3_checks.S3-3, every screw-set, coupling, base and frame row), `proposed_params.yaml` (`jackscrew`, `liftmotor`, `liftsync`, `ring` clamp leaves). Section screw: c (theta 270, YZ plane, u = y, plotted z_S = z_A + 60). Scripts are in the scratchpad at `C:\Users\UR\AppData\Local\Temp\claude\eba575d6463ef2d6\6efaddfb-5e83-4849-8803-49d5d7303110\scratchpad\p3b2\`. `allpairs.py` runs on a copy of `docs/sketches/` in `p3b2\sk\`. It takes every declared neighbour pair, `use:` groups expanded and pose restrictions applied, between rows drawable in (u, z_A) (section_u, place, or plan_poly), across all four poses, and passes each through `sketch_common.overlap_area` / `min_distance`. The log is `allpairs3.log` (665 lines). `check_sketch.py --stale --docs-dir` was run on the copy. Nothing under `docs/sketches/` was edited.

## Corrections to the brief

1. **The Engineer is right: my shoulder at 272 cannot be built, and I withdraw it.** If the shoulder sat at 272, the screw would have to be d 12 below 272, journal 10 from 272 to 288, and d 12 again above 288 (the Tr12 body). A bearing with a 10 bore cannot pass over d 12 from either end. With the Designer's layout (screw shoulder on the upper inner race at 288, locknut under the lower inner race), both axial directions close in drawn parts (section 2). My FIX 1 asked for the property (an axial face on the screw for each direction), and the property holds.
2. **36 closes the coupling stack. 36.5 is not needed.** My 36.5 came from closure condition (b), CL >= S + e_s + g + c_t, with e_s 10 and c_t 1.5. At 36 the stack has e_s 9 and c_t 2.0, so 24 + 9 + 1 + 2 = 36 (DERIVED). The condition holds with equality, and the drawn values satisfy it. The total engagement is 10 + 9 = 19 of the 20-long coupling under both the 36 and the 36.5 values (NOTE 2).
3. **"Both load paths close" holds in the drawing, but two things still need work.**
   - Each joint that bears load must be buildable. The clamp-to-housing joint is not: FIX 7.
   - S3-3 must certify the face that carries load in the cut case. As written, chain c passes on the screw shoulder, which unloads in the cut case: FIX 8.

## 1 FIX 1 to 6 against the spec, hand beside computed

Hand values are DERIVED from the overlay leaves. Computed values are MEASURED from `allpairs.py` at capture_end unless marked. Tolerances follow K7: C passes at overlap <= 0.01 mm² and distance <= 0.05; G passes at distance >= g_min - 0.05.

**FIX 1, journal steps (screw_c `section_u`). Closed.**

| Piece | Hand (r, z_A) | Spec expression gives |
|---|---|---|
| Journal and M10x1 | r 5, 265 to 280 + 8 = 288 | 265 to 288 |
| Tr12 body | r 6, 288 to 1165 - 30 = 1135 | 288 to 1135 |
| Guide journal | r 5, 1135 to 1165; the bearing at 1146 to 1154 lies inside this band | 1135 to 1165 |

| Pair | Declared | Hand | Computed |
|---|---|---|---|
| screw_c\|anchor_bearing_c | C | r 5 radial face, plus the shoulder face at 288 (r 5 to 6) | 0.00 mm², 0.00 (was 32.00 mm²) |
| screw_c\|guide_bearing_c | C | r 5 radial face, no shoulder in 1146 to 1154 | 0.00 mm², 0.00 (was 16.00 mm²) |
| screw_c\|anchor_c | F | body r 6 against cover bore r 8: 2.00 | 0.00 mm², 2.00 |
| screw_c\|guide_c | F | body end r 6 at 1135 against block bore r 13: 7.00 | 0.00 mm², 7.00 |

The body-to-journal step at 1135 sits 11 below the guide bearing (1146), so the guide stays radial only and has no axial face, as intended.

**FIX 2, axial seats in the block (anchor_c `section_u`). Closed.**

| Band | Hand | Spec |
|---|---|---|
| Shoulder bore D20 | r 10 to 21, 265 to 280 - 8 = 272 | 265 to 272 |
| Bearing bore D26 | r 13 to 21, 272 to 288 | 272 to 288 |
| Cover bore D16 | r 8 to 21, 288 to 295 | 288 to 295 |

Both load paths, each face with its drawn contact width per side (DERIVED from the pieces):
- **Cut case** (cut reaction lifts the ring, so the screw is pulled up): locknut top at 272 against the lower race (r 5 to 9, width 4.0), then the bearing pair, then the upper race against the cover at 288 (r 8 to 13, width 5.0).
- **Lifting cases** (screw pushed down): screw shoulder at 288 against the upper race (r 5 to 6, width 1.0), then the bearing pair, then the lower race on the block shoulder at 272 (r 10 to 13, width 3.0).

| Pair | Declared | Computed |
|---|---|---|
| anchor_c\|anchor_bearing_c | C | 0.00 mm², 0.00 |
| anchor_locknut_c\|anchor_bearing_c | C | 0.00 mm², 0.00 |
| anchor_locknut_c\|screw_c | C | 0.00 mm², 0.00 |
| anchor_locknut_c\|anchor_c | F | 0.00 mm², 1.00 (hand: r 9 against bore r 10) |
| anchor_locknut_c\|screw_end_c | F | 0.00 mm², 1.41 (hand: corner (1, 1) from locknut bottom 266 to the screw-end top 265) |

The locknut spans 280 - 8 - 6 = 266 to 272 (hand), the same as the spec. Mounting caveats on the drawn faces are in NOTE 1.

**FIX 3, nut counterbore and upward seat. Geometry closed; the clamp joint cannot be built (FIX 7).** At capture_end, nut_z = 305.84 + 15 = 320.84 z_A (DERIVED).

| Piece | Hand | Spec |
|---|---|---|
| Housing bore | D 22 + 2 x 0.5 = 23, r 11.5 to 25, from 305.84 to nut_z + 15 - 8 = 327.84 | as hand; the -u expression now carries the parentheses (Engineer Correction 3, read in the spec) |
| Counterbore | D 42 + 1 = 43, r 21.5 to 25, from 327.84 to 335.84 (depth 8 = nut_flange_thickness) | as hand |
| Nut body | r 6 to 11, from 305.84 to 327.84 | as hand |
| Nut flange | r 6 to 21, from 327.84 to 335.84 | as hand |
| Clamp | r 15 to 23, from 335.84 to 338.84 | as hand |

Faces:
- Cut-case seat: the counterbore shoulder at 327.84 under the flange, r 11.5 to 21, 9.5 wide per side.
- Lifting seat: the clamp underside at 335.84 on the flange top, r 15 to 21, 6.0 wide.
- Clamp on the housing top: r 21.5 to 23, **1.5 wide**.

| Pair | Declared | Computed |
|---|---|---|
| nut_c\|nut_housing_c | C | 0.00 mm², 0.00 (was 152.00 mm²) |
| nut_c\|nut_clamp_c | C | 0.00 mm², 0.00 |
| nut_clamp_c\|nut_housing_c | C | 0.00 mm², 0.00 |
| screw_c\|nut_c | C | 0.00 mm², 0.00 |
| screw_c\|nut_housing_c | F | 0.00 mm², 5.50 (hand 11.5 - 6) |
| screw_c\|nut_clamp_c | F | 0.00 mm², 9.00 (hand 15 - 6) |
| ring\|nut_housing_c | C | 0.00 mm², 0.00 |
| ring\|nut_c | F | 0.00 mm², 4.12 |
| nut_housing_c\|anchor_c | G 10 | 0.00 mm², 10.84 (hand 305.84 - 295) |
| park: nut_clamp_c\|home_switch_c | G 10 | 0.00 mm², 10.75 (hand sqrt(7² + 8.16²) = 10.75; clamp top 1113.84, switch bottom 1122, r 183 against 190) |
| park: nut_housing_c\|home_switch_c | G 10 | 12.23 (hand sqrt(5² + 11.16²)) |
| park: nut_clamp_c\|guide_c; nut_housing_c\|guide_c | G 10 | 21.16; 24.17 |

The home-switch lever tip at park is at 1110.84 + 3 + 1.16 = 1115.00 z_A, r 182 (hand), which equals the spec expression. Where the lever crosses the clamp rim (r 183) it is at 1115.88, so it is 1.16 clear of the clamp top at its tip (DERIVED).

**FIX 4, coupling stack at 36. Closed.** Hand values, z_A:

| Part | Hand | Computed |
|---|---|---|
| Motor face | 265 - 36 = 229 | - |
| Motor | 181 to 229 | 181 to 229 |
| Pilot | 229 to 231 | - |
| Shaft | 229 to 253 | - |
| Coupling | centred on the shaft tip, 243 to 263 | 243 to 263 |
| Screw end | 253 + 1 = 254 to 265 | 254 to 265 |
| Engagements | shaft 10, screw end 9 | - |

| Pair | Declared | Hand | Computed |
|---|---|---|---|
| liftmotor_shaft_c\|screw_end_c | G 1 | 1.00 | 0.00 mm², 1.00 |
| coupling_c\|anchor_c | G 1 | 2.00 vertical; 2.06 at the shoulder-bore corner, sqrt(0.5² + 2²) | 2.06 |
| coupling_c\|liftmotor_pilot_c | G 1 | 243 - 231 = 12.00 | 12.00 |
| coupling_c\|anchor_locknut_c | F | 266 - 263 = 3.00 | 3.00 |
| coupling_c\|standoffs_c | F | - | 3.25 (x bands also disjoint) |
| standoffs_c\|anchor_c; standoffs_c\|liftmotor_c | C | - | 0.00; 0.00 |

- The z_rules now read the leaves (shaft tip = anchor_z - coupling_length + shaft_length). A future change to CL or S moves the parts consistently, and the G 1 on shaft|end makes K7 enforce closure condition (b).
- Bar length: 1165 - 254 = 911.00 (DERIVED), which equals the Engineer's figure.
- No S3-1, S3-2, L_min, L_t or critical-speed value reads coupling_length (my sign-off, section 5).

**FIX 5, base_plate|base_frame. Closed.** Both rows declare F (contact off the plane, certified by S1/S2). Computed: 0.00 mm², 5.00 at every pose (hand: plate edge 239, rail 244). The chain c certifiers for this pair name only S1 and S2. base_frame|frame_upper_c is C at 0.00.

**FIX 6, certifiers. Closed as specified.**
- Every `chains` certifier names a sketch and a pair id ("S1 collet|core_seat C", "S2 frame_upper_c|base_frame z-contact", "S3 anchor_c|anchor_bearing_c").
- `s3_checks.S3-3.records` resolves each to the latest accepted, unsuperseded record and gives a stale record no certifying power.
- drill_head|core_750 is "declared: load application" on chains a, b and c.
- `--stale` on the copy (MEASURED): 2 records, 5 differences. s1 r7: lead, nominal, coupling_length. s2 r5: nominal, coupling_length. This matches the Engineer's run, so the S1 and S2 certifiers resolve to r8 and r9 only once P6 accepts them, as ruled.
- X1: pass, 70 rows compared, 3 skipped, 3 exempt (anchor_a/_b/_c) (MEASURED).
- One certifier string names two pairs ("S3 anchor_locknut_c|anchor_bearing_c and anchor_locknut_c|screw_c"). The P4 reader has to parse it, or FIX 8 removes the need.

## 2 All declared pairs, all poses

`allpairs.py` (MEASURED) judged 104 C pair-pose entries and 496 G pair-pose entries, plus the F entries, on rows drawable in (u, z_A).
- **No C pair is off 0.00.** No C entry has overlap above 0.01 mm² or distance above 0.05.
- **No G pair is under its g_min, and no F pair overlaps.**
- Least G margins: coupling_c\|anchor_c 2.06 (G 1), liftmotor_shaft_c\|screw_end_c 1.00 (G 1, on its bound by design), nut_clamp_c\|home_switch_c 10.75, nut_housing_c\|anchor_c and nut_housing_c\|bracket_anchor_c 10.84 (G 10, the S1-4 identity 0.84).
- The N pairs that overlap (shaft in the coupling, 50.00 mm²; screw end in the coupling, 72.00 mm²; shaft in the pilot, 10.00 mm²) are declared N, which is correct for unsectioned parts inside a bore.
- Motion is pure translation in z, and every fixed part lies above park or below capture_end on the path. The four static poses therefore bound the swept G values.

Not judged by this script: the axis rows defined by `section` (receiver, collet, holder, core_seat and the rest) and the rows without section axes. P2f did not touch them, and S1 r7 certifies the axis pairs. K7 on the drawn S3 judges them at (d).

## 3 Findings

**FIX 7 (nut clamp joint: no room for the bolts that carry the lifting load).**
- The clamp (OD 46, r 23) overlaps the housing top only over r 21.5 to 23, a 1.5 band (DERIVED). The housing wall outside the counterbore is r 21.5 to 25 (3.5).
- Even if the clamp were widened, an axial screw tapped into that wall with 1 mm of wall on each side needs a centre radius r_b with r_b - d_tap/2 >= 22.5 and r_b + d_tap/2 <= 24. Neither fits:
  - M3 (tap 2.5): 23.75 <= r_b <= 22.75.
  - M2 (tap 1.6): 23.30 <= r_b <= 23.20.
- A round clamp wide enough for M3 heads (to r about 27) and a housing to match puts the clamp 8.69 in plane from the home switch at park, under G 10 (DERIVED: du 3, dz 8.16).
- "Bolts not drawn" therefore hides a joint that cannot be built. It carries every lifting case, stall up 343 N per screw.
- Required: the Designer states a fastening that fits, with a dry run. Two that need no G relief:
  - (a) Shoulder screws through the nut flange's holes into the counterbore floor (floor band r 11.5 to 21.5, 10 wide), with float clearance. The screw heads become the upward seat, and nut_clamp_c becomes washers or is removed. In-plane holes would appear in the section pieces.
  - (b) Keep the clamp at r 23 on the section side, with bolt ears and housing bosses at the tangential azimuths (±X, out of the plane and away from the switch). No section piece changes, so the dry run in section 1 stands as measured. The shape text, the part list and the not_drawn entry change.

**FIX 8 (chain c cut case: the locknut path must be the certified path).**
- S3-3 runs the cut case. In the cut case the screw is pulled up, and the anchor load passes locknut (272) → bearings → cover (288).
- Chain c lists [anchor_bearing_c, screw_c] with first certifier "S3 anchor_bearing_c|screw_c". That pair touches at the journal (radial) and at the screw shoulder (288), and the shoulder unloads in the cut case. "At least one certifier" therefore passes the chain on a face that carries no cut load. FIX 2 was raised against exactly this: a contact certified as the axial loop when it does not carry the load.
- Required:
  - (a) Chain c replaces [anchor_bearing_c, screw_c] with [anchor_bearing_c, anchor_locknut_c] (certifier "S3 anchor_locknut_c|anchor_bearing_c") and [anchor_locknut_c, screw_c] (certifier "S3 anchor_locknut_c|screw_c", the thread).
  - (b) The S3 certifiers of anchor_c|anchor_bearing_c, anchor_locknut_c|anchor_bearing_c and nut_housing_c|nut_c name the cut-case face: `face: {z: ..., side: ...}`. The values are the cover underside at jackscrew.anchor_bearing_z + jackscrew.anchor_bearing_width (288), the locknut top at 272, and the counterbore shoulder at nut_z + nut_length / 2 - nut_flange_thickness. P4's "axial face contact" test then reads that named horizontal edge.
  - (c) The R1 symmetry lint adds anchor_locknut to the row set.
- Dry run: no geometry changes. The three pairs read C at 0.00 mm², 0.00, and the face widths per side are 4.0 (272), 5.0 (288) and 9.5 (shoulder) (MEASURED / DERIVED, section 1).

**NOTE 1 (bearing mounting, drawn faces against catalogue form; for the Designer at vendor pick, B2).** The drawn bearing is a solid race from r 5 to 13, so every drawn face reads C. Against a 10 x 26 x 8 angular-contact bearing, from catalogue form (not on file, ASSUMED):
- The screw shoulder d 12 is at or just below the usual inner-ring abutment minimum (da min about 12 to 13).
- The locknut OD 18 reaches past the inner-ring land (OD about 15) to within about 1 of the outer-ring bore. A KM0-type nut is M10x0.75, not M10x1, and a spacer is usual.
- The cover bore 16 clears the inner ring by about 0.5 radial.

None of these changes a pair here. All belong in Step 2 vendor dimensions.

**NOTE 2 (coupling engagement).** The shaft and the screw end engage 10 + 9 = 19 of the 20-long beam coupling with a 1 gap. That leaves no room for the beam's flexing section if the clamp hubs are shorter than 10 and 9. My 36.5 had the same total. The coupling vendor's hub lengths set e_m and e_s. If the hubs are shorter, condition (b) gives the new coupling_length, and the G 1 on shaft|end catches any shortfall in K7. Step 2, with the coupling guard.

**NOTE 3 (flush flange under the clamp).** The counterbore depth equals the flange thickness, so the clamp grips the flange with zero axial play. A radially floating nut needs a few hundredths of axial clearance, or friction cancels the 0.5 float. The drawn identity is fine for the sketch. The part needs counterbore depth = t_f + about 0.05, or a shim. FIX 7 (a) removes the issue.

**Verdict: FIX (2 items: FIX 7, FIX 8).** FIX 1 to 6 are closed, with hand values equal to the computed values everywhere. No C pair is off 0.00, and no G or F pair is under threshold. FIX 7 sends the clamp fastening back to the Designer. FIX 8 is a chains and face-field edit in s3_spec.yaml plus a P4 harness item. I re-check both with `allpairs.py` and sign without re-reviewing the other sections.

## Gameplan lines to change

1. l.288, the S3-3 row, within the new text of the Engineer's P2f item 6.
```
Old: every consecutive pair class C, as an axial face contact in the section,
New: every consecutive pair class C, as an axial face contact that carries the cut-case load in its direction (named face per S3 certifier: anchor locknut top 272, cover underside 288, nut counterbore shoulder; the chain lists the locknut; Loftsman 1.3 (b) re-sign FIX 8) in the section,
```
2. l.272, the new text of the Engineer's P2f item 5, held until FIX 7 settles. The orchestrator applies P2f item 5 only after the Designer states the nut fastening, with its text taken from that statement.
```
Old: brass flange nut in a counterbored boss under a clamp ring on the ring, with its mounting
New: brass flange nut in a counterbored boss with its upward seat as fastened by the Designer (Loftsman 1.3 (b) re-sign FIX 7), with its mounting
```
