# Topologist Review, Step 0: Core Cutter Test Jig

Reviewed: workorder.md, step0_software_engineer_revision.md (draft gameplan), step0_engineer_source_extraction.md, llm_plm_cad.md 4.3, 7.4, 7.5.
Method: every relationship below is a sign, a half-space membership, a containment, or a minimum distance. No relationship is left as "looks right."

---

## 1. Findings, ranked

| Rank | ID | Severity | Finding | Where it bites |
|---|---|---|---|---|
| 1 | TP-1 | Critical | The default boss thread, Tr 60 x 8 (major diameter 60 mm), is smaller than the cores it must hold (90 to 105 mm). No topology that satisfies the stated relationships allows it. | Params, T2, T6, A2, E5, every part script |
| 2 | TP-2 | Critical | The stack is stated three incompatible ways (workorder, draft, this review's brief). If the holder lands on the boss top or base, the nut load bypasses the collet and the collet cannot close. Load path and stroke are not specified. | E2, F1, T5, Step 2 |
| 3 | TP-3 | High | A1 says "touching is not overlapping." That erases the difference between allowed and forbidden contact. A nut resting on the collet, or a holder resting on the base, passes A1 with zero volume. | A1, Step 5 |
| 4 | TP-4 | High | A2 and F4 use the wrong envelope footprint and the wrong reference plane. The cutting face is an annulus from the core out to 76.2 mm, not just the tube wall. The nut, not the holder, is the highest fixture. The "pass-over" branch does not exist for anything that wraps the core. | A2, F4, E5, Detail 5 |
| 5 | TP-5 | High | A 105 mm core must fit the iris open aperture. The aperture for the 6 in drill is unmeasured. In the 7 in model it is either 54.29 mm or 108.59 mm (unit unstated), leaving at most 1.8 mm radial slack at 105 mm. | Family range, coaxiality budget |
| 6 | TP-6 | High | Collet topology contradiction: C1 requires a single solid, C5 requires slits through the full wall height. Two or more full-height slits make two or more solids. Also: a self-locking taper cannot reach the "release pose" by backing off the nut. | C1, C5, T5, F1 |
| 7 | TP-7 | Medium | A3 sign checks can be satisfied from the parameters instead of the geometry. The z-order check uses nut mid-height, which is meaningless for a cup nut. The bracket-normal test is a proxy. The flip control is blind to symmetric parts. | A3 |
| 8 | TP-8 | Medium | T1 (helix sign probe) is under-specified. Cross-threading is not tested. Chirality is not checked on the exported STL, where a mirror can occur. | T1, T2, T3, X1 |
| 9 | TP-9 | Medium | Fixed collet exterior means wall thickness varies about 7 to 1 across the family. T5's stated reason (stack height monotonic in d) is wrong: with identical exteriors it is constant. The real reason to test the extremes is stiffness. | C4, C6, T5 |
| 10 | TP-10 | Medium | Draft claims a stack reversal "changes data, not tests." False for containment direction and signs. The relations must be data-driven for that to be true. | Detail 1, F1/T5/A3 |
| 11 | TP-11 | Low | ASSEMBLY.md 4.3 (coordinate system) is not specified anywhere. Labels, key marks and slit phase have no orientation spec. | Step 1, Step 7 |

---

## 2. Frame and measurement rules (for ASSEMBLY.md 4.3)

- Right-handed. +Z up. Origin: top face of the base plate, on the boss axis. +X toward the front. Angle theta measured counter-clockwise from +X as seen from +Z (looking down).
- Poses: R (release: nut backed off, collet free) and K (clamp: nut hand-tight).
- top(P) = max z of P. bot(P) = min z of P. rho = distance from the Z axis.
- n_out(F, p) = the outward unit normal of face F at point p. Defined operationally, not by trusting `normalAt`: p + eps*n is outside the solid and p - eps*n is inside (`Shape.isInside`). A sign test that does not pass this self-check is void.
- Rule M: every predicate is computed from the final shape (faces, fitted axes, helix probes), never from the placement or the parameter used to build it. A test that reads the parameter proves the script agrees with itself.
- Rule P: each part defines at least one signed asymmetric feature (a face with a known outward normal, or a profile with a known slope sign). A part with none cannot be checked for flipping, so it must be flip-invariant by design or it must gain one.
- Relations are data. The pair table in section 6 lives in ASSEMBLY.md as a table; tests iterate over it. That is what makes a stack reversal a data change.

---

## 3. The stack as predicates

### 3.1 Required radial and axial nesting (TP-1, TP-2)

Reading: the workorder says the boss seats the collet. The brief says the collet sits on the boss seat and is inside the holder, with the nut above the holder on the boss thread. Both are satisfied by one topology only. The boss is a tube, not a post (a post would sit under or inside the core). Nesting from the axis outward:

core < collet bore < collet wall < holder cavity < holder wall < boss bore < boss wall and thread < nut

Load path (closed loop, must be written in ASSEMBLY.md):
nut thread flank -> nut clamp shoulder -> holder bearing flange (down) -> holder cone -> collet cone (down and inward) -> collet foot -> boss seat -> boss -> boss thread flank -> nut thread flank. The nut reaction is carried by the thread, the collet reaction by the seat. No other path may carry axial load.

Radial chain, minimum values for the 105 mm end (Loftsman supplies final numbers):

| Link | Value | Basis |
|---|---|---|
| core radius max | 52.5 mm | 105 / 2 |
| collet free bore radius | 53.0 mm | (105 + insert_clearance 1.0) / 2 |
| collet top outer radius | >= 54.2 mm | bore + min wall 1.2 (C6) |
| holder wall | >= 4 mm (placeholder, UNVERIFIED) | print rule of thumb |
| holder body outer radius | >= 58 mm | sum |
| boss bore radius | >= 59 mm | sliding clearance |
| boss thread minor radius | >= 64 mm | boss wall 5 mm (placeholder) |
| boss thread major radius | ~ 68 mm | + thread depth 4.5 (Tr x 8) |
| nut outer radius | ~ 76 mm | + nut wall 8 mm |

Result: thread major diameter is about 135 mm, nut OD at least about 150 mm. Not 60 mm. Consequence: the nut is wider than the 146.05 mm tube ID. E5 resolves itself: `nut_is_stop = true` by geometry, not by choice.

### 3.2 Predicates

| ID | Relationship | Predicate (pass) | Pose |
|---|---|---|---|
| S1 | Coaxial | For every axisymmetric part: fitted axis a satisfies norm(a x Z) <= 1e-4 and radial offset of axis at z=0 <= 0.05 mm. Tilt included. A3's x,y offset alone misses tilt. | R, K |
| S2 | Boss rises from base | bot(boss) = 0 +/- 0.05. (tip - root) . Z > 0. Plate top face n_out = +Z. | both |
| S3 | Collet sits on boss seat | Collet foot face n_out = -Z. Seat face n_out = +Z. n_C . n_seat = -1. bot(C) - z_seat in [0, 0.05]. Contact area >= A_seat_min. | both |
| S4 | Collet inside holder | vol(C minus Cavity(H)) <= 0.01 mm3, where Cavity(H) is the solid of revolution of the holder's inner profile. Also top(C) <= top(H). | both |
| S5 | Matched taper, correct sense | d(rho_out^C)/dz < 0 and d(rho_in^H)/dz < 0 over the cone (narrower at the top). Half-angles equal within 0.02 deg. Reason: the holder moves down on a fixed collet; closure requires the cone radius to fall as z rises. | both |
| S6 | Holder never bottoms | bot(H) - z_seat >= stroke s + margin in R; > margin in K. Holder body radial gap to boss bore >= c_slide (0.2 mm). This is a forbidden contact (see 6). | both |
| S7 | Release/clamp gap on the cone | R: radial gap g = rho_in^H - rho_out^C in [0, seat_clearance] everywhere. K: g = 0 over a contact patch of area >= A_cone_min. | R, K |
| S8 | Core inside collet bore | For z in [bot(C), top(C)]: R: rho_core <= rho_bore - insert_clearance/2. K: rho_core = rho_bore within 0.05 mm over a contact patch (area >= A_grip_min), slit width > min_slit_clamped. | R, K |
| S9 | Core above base, on its stop | Core bottom n_out = -Z. Stop face n_out = +Z. bot(K) - z_stop = 0 +/- 0.05. bot(K) - top(base plate) >= h_min > 0 (core never rests on the tray or plate). | both |
| S10 | Nut above holder, clamp face bears on holder | Nut clamp face F_N: planar annulus, n_out = -Z. Holder bearing face F_H: n_out = +Z. n_N . n_H = -1. K: z(F_N) - z(F_H) in [0, 0.05], overlap area >= A_clamp_min. R: z(F_N) - z(F_H) = screw travel s > 0. Sign(z(F_N) - z(F_H)) >= 0 in both poses. Use faces, not centroids. | R, K |
| S11 | Nut does not bear on collet or core | min_dist(N, C) >= 1.0 mm and min_dist(N, Core) >= 1.0 mm, both poses. Zero contact area. | both |
| S12 | Nut has travel left | z(nut lowest face) - z(boss shoulder or base) >= 1 pitch in K. | K |
| S13 | Thread engagement | engaged axial length >= min_engage in K, and >= min_engage in R at the point just before disengagement is possible. | R, K |
| S14 | Core exposed above the highest fixture | top(Core) - top(N) >= S_iris + g_stop + m, S_iris = 106.369 mm (7 in model, UNVERIFIED for 6 in). Reference is the nut top, not the holder top (TP-4). | K |
| S15 | Stroke inequality | s = d_rho / tan(alpha), d_rho = (insert_clearance + core.tol)/2 for one collet's bore. Available thread length >= s + min_engage + 1 pitch. Example: alpha = 8 deg, d_rho = 1.0 gives s = 7.1 mm; the E4 reading (+/- 2.5 mm range) gives d_rho = 3.0 and s = 21 mm. | design |
| S16 | Release by elastic recovery | alpha > atan(mu_max), mu UNVERIFIED (PETG on PETG, order 0.3 to 0.5, so alpha above about 22 to 27 deg), OR the holder flange is captured so that unscrewing lifts it. Without one of these the release pose is not reachable by turning the nut (TP-6). | design |

---

## 4. Thread handedness (TP-8)

### 4.1 Convention
Right-handed means the helix satisfies z(theta) = z0 + (L / 2 pi) * theta with lead L > 0, theta counter-clockwise from +Z view. Boss (external) and nut (internal) must carry the same sign, because handedness is a property of the helix, not of which side the material lies on.

Tightening: nut descends toward the holder (dz < 0). With L > 0 that means dtheta < 0: clockwise seen from above. Tightening is clockwise by construction when sign(L) = +1 for both parts.

### 4.2 Tests, replacing the "helix sign probe"
- **T1a (probe, numeric):** sample the ridge centerline of the boss at theta = 0 and 90 degrees at fixed rho. (z90 - z0) mod L = +L/4 for right-hand, 3L/4 for left-hand. Do the same on the nut ridge. Both must read L/4. Use 90 degrees, not 180: at 180 both hands read L/2 and the test is blind.
- **T1b (mesh invariant, the real test):** apply the screw motion S(phi) = Rz(phi) * T(0, 0, L*phi/(2 pi)) to the nut at pose K. For phi in {15, 90, 180, 360} degrees, vol(common(boss, nut after S(phi))) <= 0.01 mm3. Then apply the opposite-hand motion Rz(phi) * T(0, 0, -L*phi/(2 pi)) at phi = 90: the common volume must be large (ridge lands on ridge, order L/2 axial shift). A rotation with no translation must also fire. A matched pair passes the first and fails the second and third; a left-hand nut against a right-hand boss does the reverse. This handles both-wrong (LH/LH passes mesh but fails T1a) by keeping T1a.
- **T1c (direction):** from K, apply Rz(-phi) * T(0,0,-L*phi/(2 pi)): the nut descends. Pass: dz < 0 for a clockwise turn. This is the "tightening is clockwise" statement as a sign.
- **T1d (export):** repeat T1a on the exported STL and STEP in X1. A mirrored export flips the sign and, if the winding was repaired afterward, the signed volume is still positive. E2's signed-volume test does not catch it.

Unrepresentable by construction: the nut builder has no handedness parameter. The boss and the nut both call one function in common.py that returns the helix, and `hand = +1` is a constant there, not a field in params.yaml. No `mirror` on any threaded part. T1a and T1b are the backstop, not the mechanism.

### 4.3 Cross-threading
Cross-threading is axis tilt at first engagement. Make it geometrically unreachable:
- Single start (lead = pitch). Test: lead/pitch = 1.
- Cylindrical pilot (register) on the boss and a matching bore in the nut, engaged for at least one full register length before the first ridge touches. Tilt allowed by the register: alpha_reg = atan(c_diam / L_reg). Tilt the thread cannot forgive: alpha_crit = atan(L / (4 D)), about 1.9 deg for L = 8, D = 60, smaller as D grows. Requirement: alpha_reg <= alpha_crit / 2, so L_reg >= 2 * c_diam / tan(alpha_crit / 2)... for c_diam = 0.4 mm and D = 135 mm: alpha_crit = 0.85 deg, L_reg >= about 54 mm. That is long; at this diameter the lead-in must be a deeper pilot. Loftsman confirms the number.
- Test: with nut tilted by alpha_reg about a transverse axis through the pilot contact, the thread ridges must not interfere (vol < 0.01), and tilted by 2 * alpha_crit the pilot must interfere before any thread does (pilot-first ordering). The second is the known-bad: it must fire.

---

## 5. Envelope: drill tubing (TP-4, TP-5)

Tubing OD 152.40 mm (rho 76.20), ID 146.05 mm (rho 73.025).

| ID | Predicate |
|---|---|
| E-1 | Core inside bore: 73.025 - rho_core,max >= margin. Radial gap 28.025 (90), 20.525 (105). Containment: vol(Core minus BoreSolid(146.05 - 2*margin)) = 0. |
| E-2 | Coaxial: core axis vs tube axis offset <= delta_axis over the full stroke. |
| E-3 | Cutter footprint is the full annulus from the core kerf radius out to 76.20, not the tube wall. Any fixture with rho in that range lies under the cutting face. A holder or collet around the core always does. |
| E-4 | Stop plane: at full descent z_cut,min >= top(highest fixture with rho <= 76.20) + g_stop. That fixture is the nut (above the holder), so the stop is top(N). |
| E-5 | Fixtures outside rho = 76.20 + margin (frame columns, brackets) are free of the stroke sweep. Nothing between the core and 76.20 is. |
| E-6 | If rho_nut,max > 73.025, the nut cannot enter the tube; it is a hard stop and `nut_is_stop = true`. Section 3.1 shows rho_nut,max is about 76 or more, so it is always true. Test it as a derived value; the Engineer does not choose it. |
| E-7 | The iris severs the core at z_cut,min + S_iris. Require top(Core) > z_cut,min + S_iris + m (same as S14). If the core is short the iris closes on air. |
| E-8 | Aperture: rho_core,max <= rho_aperture,open - m_ap for every accepted d, with aperture from the 6 in iris (UNVERIFIED). The 7 in value 54.2925 is a radius if the open diameter is 108.585; that leaves 1.79 mm radial slack at 105 mm and the jig's total coaxiality error must be inside it. If the aperture is a diameter of 54.3, no core in range enters. Resolve before the 90 to 105 range is baked in. |
| E-9 | Swept check: tube-and-cutting-annulus solid, swept along Z over the stroke, intersected with every fixture except Core. Core is checked by containment, not intersection. A1's A2 branch 1 (tube wall only) becomes a subset test. |

---

## 6. Contact classes and the forbidden-overlap matrix (TP-3)

Three classes replace one:

- **C (contact):** allowed or required. min_dist = 0 +/- 0.01, and the contact patch area meets a floor. Overlap volume still < 0.01 mm3.
- **G (gap):** contact forbidden. min_dist >= g_min (stated per pair), overlap = 0, contact area = 0.
- **F (free):** remote, overlap = 0 only.

Every pair must have a class. An unlisted pair is a failure, not a default pass. Overlap < 0.01 mm3 applies to all of them.

Parts: B base with boss, H holder, C collet, K core, N nut, F frame, R brackets and T-nuts, E cutter envelope (E-9 sweep).

| | B | H | C | K | N | F | R | E |
|---|---|---|---|---|---|---|---|---|
| **B** | | G (S6) | C seat (S3) | C stop (S9), G lateral | C thread bearing flank only; G crest/root/other flank | C plate on frame | C or F | F |
| **H** | | | C cone (K) / G or unloaded (R) | G | C clamp face (K) / G (R); G radial | F | F | G, below stop |
| **C** | | | | C bore on core (K) / G (R) | G (S11) | F | F | G, below stop |
| **K** | | | | | G (S11) | F | F | contained (E-1) |
| **N** | | | | | | F | F | C or G by design: stop contact with tube end is forbidden; G with g_stop |
| **F** | | | | | | | C T-nut in slot, bracket faces on profile faces | F |
| **R** | | | | | | | | F |

Notes on specific cells:
- B-N: contact exists only on the bearing flanks. Under the clamp load the nut is pushed up, so the contacting flanks are the nut's upward-facing flank (n . Z > 0) against the boss's downward-facing flank (n . Z < 0). The opposite flank pair has clearance 2c total. Crest and root radial gap >= c_min (UNVERIFIED until the Step 9 print). Any other thread contact is a failure.
- B-H: forbidden. A hard stop here bypasses the collet and defeats the clamp range (TP-2).
- H-N radial: nut bore to holder body gap >= c_slide.
- N-E: with the nut as the stop, z_cut,min - top(N) >= g_stop > 0. The cutter must not touch the printed nut.
- B-F, F-R: for brackets, mate faces antiparallel: n_bracket . n_profile = -1 and the bracket body lies in the half-space n_profile . (x - p0) > 0. Replace A3's "outward normal points away from the frame centroid": that is false for any interior bracket. T-nut: centroid inside the profile slot cavity, common volume with profile 0, bolt axis . n_slot_face = -1.

Run the matrix at poses R and K, for each of the four collets.
Controls: a planted nut resting on the collet top (G violated by contact, overlap 0) must fire; a planted holder resting on the boss top must fire; two parts 100 mm apart read F; a 1 mm overlap fires every class.

---

## 7. Family interface invariants (all collets share the boss-facing interface)

Let X_d = solid of revolution of the collet's outer profile with the bore filled. Let I = {foot face z and annulus radii, key or flat, taper half-angle, large and small outer radii, height, seat height}.

- **S17:** for every pair d, d' in {90, 95, 100, 105}: vol(X_d common X_d') = vol(X_d) = vol(X_d') within 0.01 mm3. One test supersedes C4's five scalar comparisons and catches shape differences the scalars miss.
- **S18:** the only d-dependent geometry is the bore. C_d = X minus Bore(d), Bore(d) a coaxial cylinder of radius (d + insert_clearance)/2. Test: symmetric difference of any two collets lies inside the larger bore cylinder's annulus.
- **S19:** Bore(d) inside X with wall >= w_min at the narrowest point, which is at the top of the cone: rho_out(top) - (d_max + ins)/2 >= 1.2 mm.
- **S20:** bore axis = outer axis = part axis (S1) for each d. The collet centers the core on the boss axis for every d; no d shifts the core off axis.
- **S21 (stiffness, TP-9):** with X fixed, wall(105) is about 1.2 mm and wall(90) about 8.7 mm. Bending stiffness scales roughly with wall cubed: the 90 mm collet is on the order of 300 times stiffer. Hand-tight closure on the 90 collet may not occur. Loftsman: flexure relief (finger thinning, slit count) is needed on the thick end, or the exterior must scale. T5's justification must be rewritten: the extremes bound the family by wall thickness and by min slit travel, not by monotone stack height. Stack height at cone contact is identical for all d because X is identical.

---

## 8. Collet topology (TP-6)

C1 (single solid) and C5 (a ray across the slit meets void along the full wall height) conflict. A full-height slit through the whole wall height splits a ring into one C-shape (one slit) or n solids (n >= 2).

Choose one and state it:

| Type | Slits | Components | Euler genus | chi = 2 - 2g | Closure |
|---|---|---|---|---|---|
| C-ring | 1, full height | 1 | 0 | 2 | poor roundness |
| Finger collet | n >= 3 from the top, depth < H, base ring intact, stress-relief radius at each slit end | 1 | 1 | 0 | good; typical |
| Alternating | n slits from top, n from bottom | 1 | 1 | 0 | good, stiffer |

Recommended: finger collet. Replace C5's ray rule: the ray meets void for the slit depth only and meets solid below. Add:
- **S22:** component count = 1; chi equals the expected value above; slit planes contain the Z axis (distance of plane from axis < 0.01 mm), slit direction perpendicular to Z.
- **S23:** closure arithmetic: bore circumference change for d_rho radial closure is 2 pi d_rho; per slit width change = 2 pi d_rho / n. For d_rho = 3.0 (E4 reading) and n = 4: 4.7 mm per slit. The un-clamped slit width must exceed it. Slit width test (C5, 0.05 mm) must be against this derived value, not just params.
- For other parts, add genus checks: genus equals the declared through-hole count (base: drain holes and bolt holes; nut and holder: 1). A forgotten or filled feature changes genus and fires. This supports F5.

---

## 9. Wrong states, made unrepresentable (or caught)

| ID | Wrong state | Why it is wrong | Mechanism that prevents it | Residual check |
|---|---|---|---|---|
| W1 | Collet upside down | S5 sign violated (cone widens upward); foot face n_out = +Z | Foot has a key or flat that the seat has and the top lacks. Wide end must enter the boss bore first; flipped, the foot (largest radius) cannot pass the holder's narrow top aperture. | S3 fails (gap > 0.05), S4 fails (outside cavity), S13 fails (nut cannot engage). Known-bad control: flip 180 deg about X, all three must fire. |
| W2 | Holder upside down | Flange at the bottom; cone narrows downward (S5 violated) | Flange OD > boss bore > body OD. Body-first is the only entry. | S10 fails (clamp face z-order), S6 fails (bottoms on boss), S4 fails. |
| W3 | Nut upside down | Clamp shoulder faces up | Thread only at one end; blind from the other. Boss enters only from the thread end. | T1a/T1b on a flipped nut, S10 (n_N . n_H = +1 instead of -1). |
| W4 | Wrong-hand thread (either part) | Cannot mesh, or meshes with the wrong sense | Section 4.2 (no hand parameter, one helix function). | T1a, T1b, T1c. |
| W5 | Cross-threading | Nut axis tilted at first engagement | Section 4.3 pilot. | Tilt test with pilot-first ordering. |
| W6 | Wrong collet for the core | 105 core in 90 collet (no entry); 90 core in 105 collet (no grip, slit bottoms) | Engraved d on the foot and top rim (label normal n . Z > 0 on a non-mating face; engraving must not cut a seat or cone face). | F3 4x4 sweep: diagonal passes, off-diagonal rejected. The draft tests only one mismatch. |
| W7 | Collet not seated (propped on the holder) | Holder cannot descend; stack shortened | Cone matching plus S6 stroke margin. | S3, S6. |
| W8 | Holder bottoms before clamp | Hard stop bypasses collet | S6: bot(H) - z_seat >= s + margin. | G class for B-H. |
| W9 | Nut bottoms on base | Overtravel, no clamp feel | S12: >= 1 pitch of travel left. | S12 in K. |
| W10 | Base on frame upside down or plate hits profile slot side | Boss points down | S2, plate underside n_out = -Z on frame top face n_out = +Z. | A3 bracket and plate mates. |
| W11 | Collet slit phase vs key | Slit over the key stub | Slit angle is a fixed function of key angle in the generator. | Per-collet slit angle = key angle + constant. |

Note: W1 and W2 must be unrepresentable by features, not by tests. If the only defense is that S5 fails afterward, a human can still assemble it wrong. The chain above gives a physical reason each flipped part will not go on.

---

## 10. Placement verification each CAD step needs

All steps: 7.5 applies. Placements are identity where parts are built at absolute coordinates, otherwise equal to the ASSEMBLY.md expected placement within 0.01 mm and 0.01 deg. Gate on faces and fitted axes (Rule M).

| Step | Placement and spatial check required |
|---|---|
| 1 Foundation | ASSEMBLY.md 4.3 written: frame, poses R and K, expected placements, signed feature per part (Rule P), relation table (section 6) as data. Tests for S1 to S23 exist and are red. Declare the load path (3.1). |
| 2 Geometry cross-review | Resolve TP-1 and TP-2 by number. Output must include: the thread size (3.1 chain), taper alpha with S15 and S16 numbers, stroke s, register length (4.3), collet type (section 8), pilot, thread hand constant. Both personas sign the predicate table. |
| 3 Generator | Per collet, built at the origin in the part frame: S5 sign, foot normal, S17 vs a reference collet, S19, S20, S22 genus and slit plane, key angle vs slit angle, label face normal. Negative control: one collet generated with the taper reversed must fire S5. |
| 4 Exploratory | Every part at its assembly placement. S1, S2, S3, S4, S6 at K. First interference matrix with classes. Feature presence by genus (F5 extended). Flipped-part controls run per part, and each part's flipped copy must be distinguishable under Rule P. |
| 5 Assembly | Full S1 to S16 at R and K for d = 90 and 105, section 6 matrix for all four collets, T1a to T1d on the FCStd, tilt test for 4.3, E-1 to E-9, F3 4x4 sweep. Poses R and K must be generated from one pose by the screw motion S(phi), not placed independently: the nut position is on the helix, so z and theta are coupled. A4 product tree. A5 four-view PNG with a rubric item per signed feature. |
| 6 Printability | Coupon frames: print orientation is a separate transform from the assembly placement; chirality survives it (T1a on the coupon STL). Thread coupon exercises the pilot and tilt test. Slit flex bar against S23. |
| 7 Production | Re-run everything on production geometry. Chamfers and lead-ins must not change S3, S5, S10 contact faces or the thread sign. Engraved labels checked for position (non-mating face) and outward normal. The poka-yoke features in section 9 exist and change genus or volume as expected. |
| 8 Final | X1 on exported STEP and STL only: chirality (T1a, T1b), S5 sign, containment S4, S8, the section 6 matrix, E-1 to E-9, genus and component count per part, signed volume per solid positive. Euler check V - E + F = 2(S - g) per solid, with C7's faces-per-edge = 2 as the manifold test. Negative controls from the section 9 table. |

---

## 11. Where The Loftsman cross-review is required

Rule A.4: two geometry personas before build. I supply the signs. The Loftsman supplies the numbers and the profile continuity. Disagreements go by number.

| ID | Item | Question for the Loftsman |
|---|---|---|
| L1 | Boss thread size | Resolve TP-1: thread major near 135 mm, pitch (8 to 12), depth, flank angle, and what happens to the nut wall and wing span against the 256 mm bed. |
| L2 | Taper half-angle alpha | S15 stroke and S16 release: choose alpha against mu_max (UNVERIFIED) or specify the captured flange. Collet and holder cone are one definition. |
| L3 | bore_free(d) and clamped bore | One formula. Slit width, slit count, relief for the thick collets (S21, S23). |
| L4 | Thread clearance and pilot | c per flank, c_diam, register length L_reg for 4.3. |
| L5 | Collet wall and finger geometry | w_min at the cone top, finger thinning, stress-relief radius at slit ends. Also whether the exterior stays fixed or scales (S17 versus TP-9). |
| L6 | Wing nut profile | Wings tangent-continuous to the cup body, thread and shoulder planes unaffected, OD against the bed. Cannot be checked by a sign test. |
| L7 | Lead-ins and chamfers (Step 7) | Confirm no change to the thread sign, the pilot, or any contact face. |
| L8 | Iris aperture and jig coaxiality | E-8: if the aperture is 108.59 mm, what centering tolerance does the jig meet. Ties to the descent guide in Step 10. |

Required reviews by step: Step 2 (L1 to L5, mandatory, before any solid), Step 4 (L1, L5, L6), Step 6 (L4), Step 7 (L6, L7), Step 8 (topology gate with the Topologist).

---

## 12. Edits I recommend to the gameplan

1. Add TP-1 and TP-2 to the Flags to the Engineer. They outrank E1 to E8. E5 is closed by TP-1 (the nut is a stop).
2. Replace Tr 60 x 8 default in params, the Echo Site Registry and Detail 2 with "thread major near 135 mm, Step 2 to fix."
3. A1: replace the "intended-contact pairs read < 0.01 mm3" sentence with the C/G/F class table in section 6. Require every pair classed.
4. A2 and F4: use E-3, E-4, E-6, S14. Reference the nut top. Remove "pass-over" for anything that wraps the core.
5. A3: replace with S1 to S13, using faces and fitted axes. Drop "nut mid-height." Drop "bracket outward normal points away from the frame centroid."
6. T1: replace with T1a to T1d. Add T7 (tilt and pilot). Hand is a constant, not a parameter.
7. C1 and C5: choose the finger collet. Add S22 and S23.
8. C4: replace with S17 and S18.
9. T5: rewrite the reason (section 7, S21). Generate R and K from one pose by the screw motion.
10. F3: 4x4 matrix, not one mismatch.
11. Add W1 to W11 as known-bad controls in Step 5.
12. Detail 1: the pair table and the signed feature list go in ASSEMBLY.md at Step 1, as data.
13. Add E-8 to Open Questions. Ask the human or Engineer for the 6 in iris open aperture; a 105 mm core may not be accepted by any 100 mm-class aperture.

---

## 13. Items I could not verify

- The 7 in iris aperture unit (radius or diameter): extraction states this is unresolved.
- Whether the holder body is meant to sit inside the boss bore or the nut is a cup that overhangs a holder flange. Section 3.1 chooses the first because it satisfies every stated relationship. If the Engineer proposes another topology, supply equivalent S-predicates; the sign tests are reusable, the numbers are not.
- mu_max, printer, wall minima: all UNVERIFIED and flagged as such above.
- I did not open the SBIR folder, the Mines zip or the gpr model.
