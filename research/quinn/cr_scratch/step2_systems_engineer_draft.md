## Decision 1. Closed force loop (final wording for ASSEMBLY.md)

**Sentence.** The clamp force closes inside the receiver assembly and nowhere else: from the nut thread flank it passes through the nut body to the nut clamp shoulder, into the holder bearing flange (through the thrust washer when fitted), down the holder cone onto the collet cone, through the collet to the collet foot, into the receiver floor seat, up the receiver wall in tension to the receiver thread flank, and back across the thread contact to the nut thread flank. That is ten members, with the nut thread flank starting and closing the chain. The base plate, the frame and the upper assembly carry none of it. The holder flange never touches the receiver rim and the holder never bottoms on the receiver or the base, so the stroke is taken only by the collet. The nut clamp shoulder never touches the receiver rim or the base, so the nut and receiver alone never form a closed loop that moves nothing.

**Numbers and assumptions.**
- Holder flange to receiver rim gap in K: `stop.hard_stop_gap` 6 mm (ASSUMED; F6 seed). It must stay above 0 in R and K.
- Nut clamp shoulder to receiver rim: gap above 0 in K, with at least 1 pitch (8 mm, ASSUMED) of nut travel left (S12).
- Clamp axial force in the loop: about 250 N (Decision 4). Core weight adds to the floor seat, not to the loop: up to 204 N (Decision 3b).
- Floor seat bearing stress: (250 + 204) N / 200 mm2 (`seat.min_contact_area`, ASSUMED) = 2.3 MPa, against `friction.tensile_in_layer` 45 MPa (ASSUMED). Ratio 0.05, a screening check, not a proof.
- The core axis is located by cone and pilot, never by the trapezoidal thread (Design Notes 3).

**Checked by:** A3 (placement predicates: holder never bottoms, nut clamp face bears on flange face, 1 pitch travel left, engagement), F6 (flange to rim gap), T4 and T5 (engagement and travel at d = 90 and 105), F1 (cone contact in K), A1 (G-class pairs nut-base, base-holder), A6 WS8 and WS9 (holder bottomed, nut bottomed on base must fire).

**Defect found while writing it.** Detail 2 item 1 (gameplan.md:109) lists "nut thread flank" at both ends. Read as ten distinct members it is a nine-member chain. The sentence above states the closure, not a tenth member.

## Decision 2. Release mechanism (stub for integration)

Inputs fixed elsewhere: captured-flange nut with shallow cone primary, releasing cone fallback, two M6 jacking holes either way (Design Notes 3). Integration fills: chosen alpha (`cone.alpha` 10 deg or `cone.alpha_release` 20 deg), pose R/K travel s_z, jacking hole pattern. Checks: A3 (release by cone angle above atan(mu_max) or captured flange), T1c, Step 11 H5.

## Decision 3. Load cases

Frame of reference: z up, origin on datum A. Core diameter family 90 to 105 mm, mass m = rho x pi x d^2 x L / 4, rho = 2400 kg/m3 (ASSUMED, `core.density`), g = 9.81.

**(a) Iris closure torque and lateral load.**
- Torque on the core: T = 10 N m (DECLARED, `loads.torque_design`). No safety factor stacked. The core is expected to fail before the collet slips.
- Equivalent tangential force at the core surface, for scale: F = T / r = 10 / 0.050 = 200 N at d = 100 (222 N at 90, 190 N at 105).
- Lateral load: F_lat = 100 N (ASSUMED; equals `loads.wob_min`; the four-leaf iris is symmetric, so lateral is the unbalanced residual; no source). Applied at a lever arm of 106.4 mm or more above the holder (`drill.kerf_standoff` 106.369). Moment at the holder: M = 0.100 kN x 0.1064 m = 10.6 N m. At a 150 mm arm it is 15 N m.
- Grip couple: over a 30 mm grip (Design Notes 9), the lateral moment becomes a pair of radial edge forces of 10.6 / 0.030 = 354 N (500 N at the 150 mm arm). The total radial clamp normal is about 500 N (Decision 4). The unguided moment therefore uses most of the clamp, so the lateral guide (steady rest or cradle, Decision 9) is not optional, and grip length is a parameter with floor 30 mm (ASSUMED).
- Tilt before and after clamping (Design Notes 9): 1.9 deg unclamped, 0.6 deg clamped. Weight moment from tilt at 105 mm, 0.5 m: 102 N x 0.25 m x sin 1.9 deg = 0.85 N m unclamped; 0.27 N m clamped. At 0.75 m: 1.9 and 0.60 N m. All under 20 % of the lateral moment, so the lateral case governs.

**(b) Core weight with retention.** Basis stated per diameter. Gameplan.md:111 mixes bases (see contradiction C2).

| L | d = 90 | d = 100 | d = 105 | Weight at d = 105 |
|---|---|---|---|---|
| 0.5 m | 7.6 kg | 9.4 kg | 10.4 kg | 102 N |
| 0.75 m | 11.5 kg | 14.1 kg | 15.6 kg | 153 N |
| 1.0 m | 15.3 kg | 18.9 kg | 20.8 kg | 204 N |

- DERIVED from ASSUMED density. Design value for structure is the d = 105 column: 102 N at 0.5 m, 153 N at 0.75 m, 204 N at 1 m.
- Path: core base on the collet core stop, collet foot, receiver floor seat. Axial compression only. When the iris severs and retains the upper piece, the retained weight leaves the jig; the stub weight stays.
- Hold-test hook: H2 pull-out at 2 x weight is 185 N (9.4 kg) and 277 N (14.1 kg) as written (gameplan.md:198); at d = 105 the figures are 204 N and 306 N.

**(c) Cutter descent load.** Axial design load 1000 N (ASSUMED; `loads.axial_design`; bounded by the Phase I WOB range 100 to 1000 N, VERIFIED). The cutter never touches a 90 to 105 mm core: the 146.05 mm bore leaves (146.05 - 105)/2 = 20.5 mm radial gap per side at worst. The path is cutter, carriage, metal hard stop on the upper assembly, columns, frame. It must not pass through the nut, holder, collet, receiver or base plate. Required gap at the stop: g_stop 10 mm (ASSUMED) between nut top (wing tops included) and cutter lowest point.

**Checked by:** (a) T7 (analytic hold torque, prediction only), A3 (core coaxial incl. tilt), Step 11 H1 and H3. (b) F2 (core lands on stop), F4, H2. (c) A2, F4, A1 (column-to-base-plate pair is class G or F, never C), H8.

**Hold-test mismatch.** H3 applies 10 N at the core top (gameplan.md:199). At a 0.5 m arm that is 5 N m, half the 10.6 N m case above. To load the holder to 10.6 N m, apply 21 N at the core top or 100 N at 106 mm. Raise H3 to 21 N at the core top.

## Decision 4. Holding capacity and the design response

**Required:** 10 N m torque on the core, no extra factor.

**Derivation (independent route; the Loftsman estimate is a slot below).**
1. Friction needed at the core: T = mu_c x N x r, with mu_c = 0.40 (`friction.mu_c`, ASSUMED). Total radial normal force N = T / (mu_c x r): 556 N at d = 90, 500 N at 100, 476 N at 105.
2. Cone: half-angle alpha = 10 deg (`cone.alpha`, ASSUMED), mu_k = 0.35 (ASSUMED). Axial force F on the cone gives cone normal N_c = F / (sin a + mu_k cos a) = F / 0.518 = 1.93 F. Radial inward on the collet N_r = N_c (cos a + mu_k sin a) = 1.93 F x 1.046 = 2.02 F.
3. Axial force required: F = N_r / 2.02 = 275 N at d = 90, 248 N at 100, 236 N at 105.
4. Nut torque: from the Loftsman ratio F/T = 21 per m (`gameplan.md:570`): T_nut = 275 / 21 = 13.1 N m at 90 and 236 / 21 = 11.2 N m at 105. At a 230 mm wing span (couple, `wingnut.span`, ASSUMED) the hand force is 57 N per hand at 90 and 49 N at 105.

**Loftsman holding estimate (slot, fill at integration):** [Loftsman: T_hold at d = 90 and 105 for F_hand and wing arm] . Current published figure: 6.9 and 8.1 N m at 12 N m nut torque (gameplan.md:570). It is 20 to 45 % below the 10 N m. The two routes disagree on the cone friction handling and on mu_c use. This is recorded, not hidden. Rule (Design Notes 10): a miss by more than a factor 2 is a change order. The prediction does not prove the hold; H1 is the authority.

**Design response (all serve the 10 N m and none is a positive lock):**
- Core liner, TPU or silicone, in the collet bore. Raising mu_c from 0.40 to 0.70 (ASSUMED) cuts N from 500 N to 286 N at d = 100 and F from 248 N to 142 N. This is the largest lever.
- Thrust washer pocket on the holder flange (`friction.bearing` 0.25, ASSUMED), so the nut torque is spent on the thread, not on face friction.
- Tommy-bar socket in the nut: a 0.4 m bar needs 28 N for 11.2 N m, which is below the 49 N per hand.
- Longer wings: span is a parameter (230 mm seed); the span grows only if H1 demands it.

**Checked by:** T7 (prediction exists, every input labelled, margin reported; a miss is a design response item, not a geometry failure), T5 (clamp range at the extremes), C9 (stiffness ratio at 90 and 105), Step 11 H1 (authority) and H4 (creep).

## Decision 5. Tolerance budget (stub for integration)

Fixed already: rule core diameter + `core.tol` < `iris.throat_open_diameter`; slack per side at d = 105 is (108.585 - 106) / 2 = 1.29 mm; at 100 mm it is 3.79 mm with tol (4.29 mm without). Datum scheme: B is the receiver axis located by cone and pilot. Integration fills the stack-up lines (thread radial clearance and tilt, collet bore print error, slit non-uniformity, core out-of-round, `icd.coaxiality_budget` 1.0 mm ASSUMED). Checks: P8, C3, T3, T9, A3, H3.

## Decision 6. Interface control table (stub for integration; rows fixed below)

See "ICD rows fixed from params.yaml" and "Base to upper assembly rows" at the end of this file. Checks: P6, A1, A2, F4.

## Decision 7. Collet family and custom envelope

1. **Family:** 7 collets, 90.0 to 105.0 mm at 2.5 mm (DECLARED, `core.diameters`, the single source). Accept range per collet: nominal plus or minus 1.25 mm (derived from Delta = s + c_i, not asserted; Step 3 confirms). Coverage: the family covers 88.75 to 106.25 mm. The widened core range is 89 to 106 mm (90 - 1 to 105 + 1), so it is covered with 0.25 mm to spare at each end. The margin is thin; a wider tolerance than plus or minus 1.25 mm of coverage must be served by a custom collet, not by a wider family.
2. **Generator envelope:** lower bound 85.0 mm (`collets.envelope_min`, ASSUMED). Upper bound is min(110 mm, throat - tol - slack) = min(110, 108.585 - 1.0 - 1.0) = **106.585 mm** at the current throat (`collets.envelope_max`, DERIVED). The 85 to 110 mm range in Detail 5 (gameplan.md:139) is the geometric build range. It is not the admissible range. A request above 106.585 mm is rejected with the stated reason "needs a larger throat; change `iris.throat_open_radius`". Each 1 mm of throat radius raises the cap by 2 mm.
3. **Custom collet:** a generator argument, not a params edit. One command, C1 to C7 and C9 run on the result, outputs under the naming rule (`collet_097p0`). Off-grid examples 97.0 and 93.7 mm (C10).
4. **Function claim kept separate:** clamp force per N m and wall stiffness are checked at the extremes (C9, T5, H1 at 90 and 105), not by the geometry tests.

**Checked by:** P1 (diameter outside the envelope rejected), P8 (throat rule), C4 (family invariants), C8 (coverage, known-bad: remove a middle collet), C9 (extremes), C10 (off-grid collet from the usage doc alone).

## Decision 8. Hard stop ownership

**Owner:** the upper assembly (DECLARED, B5; `stop.owner`). The wing nut only tightens the collet and carries no descent load. It is never a stop and `nut_is_stop` stays deleted.

**What the base ICD exposes to the owner:**
- Datum A: frame top plane (z = 0). Datum B: receiver axis, +Z. Datum C: a frame slot line fixing rotation about Z.
- Mounting pattern: T-slot lines on the frame top face, 30 mm pitch, M6 spring-ball roll-in T-nuts, minus the lines the base plate occupies. The columns land on frame slot lines, never on the printed base plate.
- Load rating of the frame interface: 1000 N axial compression (`icd.stop_rating`, `stop.rated_load`, ASSUMED, equal to `loads.axial_design`). No safety factor is stacked on it.
- Stop gap g_stop: 10 mm minimum between nut top (wing tops included) and the cutter lowest point at the stop (`stop.g_stop`, ASSUMED).
- Stop height H_stop: `stop.height_z` 160 mm is a PLACEHOLDER (nut_top_z 150 + g_stop 10). It is a function of core length, not a single number (see C4 below). The owner sets it; the base only guarantees nut_top_z, the keep-out and g_stop.
- Keep-out: cylinder of radius 86.2 mm about datum B (`icd.keepout_radius`, DERIVED: tube OD/2 + 10 mm margin) from the nut top to stroke end.
- Exposed core: core top at least 121.369 mm above the nut top (`core.min_exposed`, DERIVED: 106.369 + 10 + 5).

**What the base does not carry:** descent load, stop impact, drill torque reaction. If any of these appears on a printed part, A1 or A2 fails.

**Checked by:** A2 (two-solid keep-out: tube swept the full stroke and the face annulus at its lowest point; asserts g_stop; control: a ring in the face annulus fires), F4 (exposed core measured from the nut top), A1 (nut-cutter and column-base-plate pairs), P6 (ICD has stop height and rating, no empty field), Step 11 H8 (envelope template).

## Decision 9. Base stability and core handling (stub for integration)

Fixed already: footprint 644 x 608 mm, four feet or bolt-down slots, tip-over number at Step 12, jig height 2 m soft and unasserted, travel at most 500 mm. Integration fills: steady rest or cradle (carries the lateral load in Decision 3a), lift strap point, mass target, derived centre-of-mass using `profile.mass_per_m_catalog` 2.573 kg/m (not the solid model volume). Checks: P6, A1, Step 11 H7.

## ICD rows fixed from params.yaml (Design Notes 5)

| Item | Value | Key | Status |
|---|---|---|---|
| Datum A | Frame top plane, base plate underside, z = 0 | `icd.datum_a` | ASSUMED |
| Datum B | Receiver axis, +Z, the one alignment axis | `icd.datum_b` | ASSUMED |
| Datum C | A frame slot line fixing rotation about Z | `icd.datum_c` | ASSUMED |
| Mounting pattern | T-slot lines, 30 mm pitch, M6 roll-in T-nuts; slot offset 15 mm | `icd.mounting_pattern`, `profile.slot_pitch` | ASSUMED / DECLARED |
| Coaxiality budget | 1.0 mm, drill centreline to receiver axis (Step 2 tolerance table sets it) | `icd.coaxiality_budget` | ASSUMED |
| Keep-out radius | 86.2 mm | `icd.keepout_radius` | DERIVED |
| Stop height | 160 mm, placeholder | `icd.stop_height` | DERIVED |
| Stop rating | 1000 N | `icd.stop_rating` | ASSUMED |
| Footprint | 644 x 608 mm | `icd.footprint_x`, `icd.footprint_y` | DERIVED |
| Tip-over | Statement only; the final number at Step 12 | `icd.tipover_statement` | ASSUMED |
| Cable exit and debris | From the drill back cap through the upper assembly; tray in the base; dust skirt on the nut | `icd.cable_exit` | ASSUMED |
| Core diameters | 90 to 105 mm at 2.5 mm | `core.diameters` | DECLARED |
| Throat | open radius 54.2925 mm (diameter 108.585 mm) | `iris.throat_open_radius` | DECLARED |
| Design torque | 10 N m | `loads.torque_design` | DECLARED |
| Design axial | 1000 N | `loads.axial_design` | ASSUMED |
| Jig height | 2000 mm, soft, recorded, not tested | `jig.height_target`, `jig.height_is_soft` | DECLARED |
| Profile | 30-6060, 60 x 60 mm | `profile.*` | DECLARED |

## Base to upper assembly rows

| Row | Base provides | Upper assembly provides or accepts | Key / test |
|---|---|---|---|
| U1 Datums | A, B, C as above | Column axes referenced to B within the coaxiality budget 1.0 mm | `icd.coaxiality_budget`; A3 |
| U2 Column foot | Frame slot lines, M6 T-nuts, 30 mm pitch | Column feet on frame slot lines, never on the base plate | `icd.mounting_pattern`; A1 (column-base plate pair G or F) |
| U3 Stop | Frame interface rated 1000 N axial compression | Owns the metal hard stop, its height and its load path to the frame | `stop.owner`, `icd.stop_rating`; A2 |
| U4 Stop gap | Nut top z (placeholder 150 mm), wing tops included | Cutter lowest point at the stop at least g_stop = 10 mm above nut top | `stop.g_stop`; A2, H8 |
| U5 Stop height | Not owned | H_stop is a function of core length: 160 mm placeholder at the 0.5 m core; adjustable range 0 to +500 mm so a 0.75 m or 1 m core still gets the same travel (see C4) | `stop.height_z`; A2 at each length class |
| U6 Travel | None | Travel at most 500 mm (DECLARED); start_z = height_z + travel | `upper.travel_max`, `stop.start_z`; P6 |
| U7 Keep-out | Everything below the nut top inside r = 86.2 mm | Nothing of the tube or face annulus below the stop height | `icd.keepout_radius`; A2 |
| U8 Exposed core | Core top at least 121.369 mm above the nut top | Sever plane inside the core at full descent | `core.min_exposed`; F4 |
| U9 Frame load from columns | Frame rails take axial compression | Column-foot moment: 100 N m (ASSUMED: 1000 N at a 0.1 m column offset); Step 12 replaces it | New ICD field; checked at Step 12 |
| U10 Cable and debris | Tray in the base, dust skirt on the nut | Cable from the back cap exits through the upper assembly clear of r = 86.2 mm | `icd.cable_exit` |
| U11 Torque reaction | Not carried by the base | Drill torque (value not stated in any source read) reacts through the carriage to the columns | Extraction line 91 |

## Contradictions found against the gate decisions and params

| # | Where | Finding | Resolution adopted |
|---|---|---|---|
| C1 | gameplan.md:139 vs params.yaml:58 | Detail 5 says the generator envelope is 85 to 110 mm. params.yaml `collets.envelope_max` is 106.585 DERIVED and its own note says "the generator default of 110 exceeded the throat" | Decision 7: 110 is the build range, 106.585 is the admissible range at the current throat. Detail 5 text to read "85 to min(110, throat - tol - slack)" |
| C2 | gameplan.md:111, 658, 192 | 9.4 kg at 0.5 m and 14 kg at 0.75 m are d = 100 values; the 19 to 21 kg at 1 m spans d = 100 to 105. Mixed basis. At d = 105 the figures are 10.4, 15.6 and 20.8 kg. The "up to about 9.4 kg" stand-in at gameplan.md:192 is not an upper bound | Decision 3b: structural design on d = 105; 9.4 kg stays the nominal 100 mm figure |
| C3 | params.yaml:28 and :105 vs extraction line 51 | Extraction line 51 says the drill advances 534.9315 mm for a 500 mm core (first core). `upper.travel_max` is 500 mm DECLARED, so 500 mm of travel captures about 465 mm | Adopt: the 500 mm figure is a ceiling on the travel; the captured length is travel less 34.93 mm unless the sever plane is placed by H_stop. Recorded here; no change to the DECLARED travel |
| C4 | params.yaml:105 vs core.length_install 750 | `stop.start_z` = 660 mm with the note "the 1 m optional core does not set it". A 0.75 m core on a seat near z = 40 mm has its top at about 790 mm, above the 660 mm start height. The cutter cannot start inside the core | Adopt: H_stop (and so start_z) is an upper-assembly adjustable range equal to the core length minus 500 mm, 0 to +500 mm (U5). params.yaml should hold `stop.height_z` as the 0.5 m case and a `stop.height_range` key. A2 runs per core length class |
| C5 | gameplan.md:345, 147, 127, 180; params.yaml:102 | "Hard stop" names two things: the holder flange to receiver rim stroke gap (F6, `stop.hard_stop_gap` 6 mm, the Holder "hard-stop face") and the metal descent stop that the gate gave to the upper assembly. A reader will assign the descent stop to the base from the F6 name, and the key sits in the `stop:` block whose owner is the upper assembly | Rename F6 to "holder stroke gap" and the key to `holder.stroke_gap`; reserve "hard stop" for the metal descent stop. Same change at gameplan.md:147 and 180 |
| C6 | gameplan.md:199 (H3) | Side load 10 N at the core top gives 5 N m at the holder; the load case is 10.6 N m at 106 mm | Raise H3 to 21 N at the core top |
| C7 | gameplan.md:570, 193 vs gate B4 | Both analytic estimates (6.9 to 8.1 N m, about 10 N m) sit at or below the DECLARED 10 N m; the gate says friction will reach it | Not an error. The plan already reports a miss as a change order (H1b). Stated so the report does not claim margin |
| C8 | gameplan.md:109 | The "ten-member chain" repeats the nut thread flank at both ends | Decision 1 wording |
| C9 | gameplan.md:536 vs params.yaml `icd.keepout_radius` | Design Notes 5 keep-out is "76.2 mm plus margin"; params holds 86.2 mm as the same cylinder as the face annulus. Consistent only if margin = 10 mm | Params value stands (86.2 mm, DERIVED); Design Notes 5 text to state it |
