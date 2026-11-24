## 1. Thread sign, cone sense, nesting: predicates with the Loftsman's numbers substituted

Frame: right-handed, +Z up, floor of the receiver pocket region at z = 0, theta CCW from +X seen from +Z. Poses: R (holder hung clear, gap c_s), K (clamped), plus two I add: R0 (holder resting on unclamped collet, zero force) and L (nut backed off the full lift play p, plate top on collar underside). All values are the Loftsman's unless marked.

### 1.1 Thread (TP-8 convention)

| ID | Predicate | Substituted | Verdict |
|---|---|---|---|
| H1 | z(theta) = z0 + (P / 2 pi) theta, P > 0 for both parts, no hand field | P = 8.0 single start, dz/dt > 0 both parts | PASS, accepted |
| H2 | T1a probe: (z(90) - z(0)) mod P = +P/4 on boss ridge and nut ridge | 2.000 mm on both | PASS |
| H3 | Tightening: nut descends (dz < 0), so dtheta < 0, clockwise from +Z | declared | PASS |
| H4 | lead/pitch = 1 | 1 | PASS |
| H5 | Lead angle lambda = atan(P / (2 pi r_p)) | atan(8 / (pi x 151.18)) = 0.965 deg | PASS, matches |
| H6 | Load-bearing flanks: nut upward-facing flank (n.Z > 0) on receiver downward-facing flank (n.Z < 0); opposite flanks gap 2 g_a = 0.60 | sweep validity f + 2h + 2 g_a = 7.1 < 8 | PASS (margin 0.9) |
| H7 | Boss and nut start at theta = 0, thread length an integer number of turns | nut 48 = 6.0 turns; receiver run in 3.3 | nut PASS; receiver run is an integer number of turns of 8: 46.5 mm is not, round to 48 |

Mesh-chirality check at export (T1d) is unchanged. Tessellation: sagitta s = r (1 - cos(pi/n)) <= 0.020 at r = 76.84 needs n >= 138 per turn. The Loftsman's c_r/10 = 0.035 only needs n >= 104. Use 0.020 for the export so the flank-sign probe sees one pitch per 0.058 mm; the STL is small (6 turns), so the finer value is free.

### 1.2 Cone sense and sides (alpha = 10.000 deg, tan = 0.176327)

Surface rho_C(z) = 63.79 - (z - 2) tan(alpha) for the collet cone (D_L/2 = 63.79 at z = 2, 58.50 at z = 32). Holder cone surface rho_H(z) = rho_C(z) + c_s in R.

| ID | Predicate | Substituted | Verdict |
|---|---|---|---|
| C1 | d rho_C/dz < 0 and d rho_H/dz < 0 (narrower upward) | -0.17633 both, from one `alpha` | PASS |
| C2 | Collet material lies on the axis side of its cone: n_out(cone) . (e_rho) > 0 and n_out . Z > 0 (outward normal tilts up) | (cos 10, sin 10) in (rho, z) | PASS |
| C3 | Holder material lies on the far side of its cone: n_out(cone, pointing into the cavity) has rho component < 0 and Z component < 0 | (-cos 10, -sin 10)... holder cone normal into cavity points inward and down | PASS |
| C4 | Closure direction: holder moves -Z, so rho_H at fixed z falls by s tan(alpha) | 0.17633 mm per mm | PASS |
| C5 | Self-lock: tan(alpha) < mu_k_min | 0.176 < 0.25 | PASS |
| C6 | Release reachable only by capture (S16) | pair: plate top (n = +Z) against collar underside (n = -Z), n.n = -1, gap p in K | PASS in form; see D-3 and D-7 for numbers |
| C7 | z0 = c_s / tan(alpha) | 0.30 / 0.176327 = 1.701 | PASS |
| C8 | s_z,max = (Delta / 2) / tan(alpha) | 1.75 / 0.176327 = 9.925 | PASS |
| C9 | Total holder travel R to K-max = z0 + s_z | 11.626 | PASS; the Loftsman's "10.3 mm" rim gap at core d + 1.0 is wrong: 13.13 - (1.701 + 2.836) = 8.59 mm. He dropped z0 |

Which side of the cone each part is on: collet at rho < rho_C(z), holder at rho > rho_H(z), in R and K. The core lies at rho < rho_bore < rho_C. No part has material on both sides of the cone surface. This is the specification for the one-line test: for every point p on the holder cone, signed distance to the collet solid >= 0 and the collet-to-holder distance is c_s (R) or 0+ (K).

### 1.3 Nesting order as radial inequalities (outward), both ends

Collet cone top radius 58.50, base 63.79 (d-independent). Core diameter range d + tol with tol = 1.0.

| Link | d = 105 | d = 90 | Inequality | Verdict |
|---|---|---|---|---|
| r_core,max = (d + 1)/2 | 53.00 | 45.50 | < r_bore,free | |
| r_bore,free = (d + 2)/2 | 53.50 | 46.00 | gap 0.50 | PASS both |
| collet wall at cone top = 58.50 - r_bore | 5.00 | 12.50 | >= 1.2 (3.5 / 11.0 after 1.5 chamfer) | PASS |
| collet cone to holder cone | 0.30 radial, any z in overlap | same | = c_s in R | see D-1: not true with the holder bottom at z = 13.63 |
| holder OD / 2 | 69.09 | 69.09 | > holder inner radius at its widest | |
| receiver bore / 2 = 69.34 | 0.25 over holder | same | = g_reg | PASS |
| receiver thread minor / 2 = 74.34, major / 2 = 76.84 | wall 5.0 | same | bore < minor < major | PASS |
| nut crest / 2 = 74.69, nut root / 2 = 77.19, nut OD / 2 = 85.20 | | | minor + c_r < ... < OD | PASS, nut wall 8.01 |
| flange and collar OD / 2 = 74.34 | | | < nut crest 74.69 | PASS nominal; fails worst case, see D-4 |
| nut plate hole / 2 = 70.10 | | | > holder OD / 2 = 69.09 | PASS, 1.01 |

The nut is outside the receiver: order by radius is core < bore < collet cone < holder cone < holder OD < receiver bore < receiver minor < nut crest < receiver major < nut root < nut OD. "Nut" is not one link in the chain; the crest and the root bracket the receiver major. Tube envelope: receiver major radius 76.84 against cutting annulus edge 76.20: outside by 0.64. The nut body (85.20) is outside the annulus. The collar (74.34) is inside it.

### 1.4 Nesting as axial inequalities (floor z = 0)

Stack from the Loftsman's own L_h = 54.0, rim 54.5, g_stop 13.13, t_f = 8, plate 8, p = 1.5, collar 6.

| Level | R | K, core d - 1.5 (max closure) | K, core d + 1.0 |
|---|---|---|---|
| pocket bottom / collet bottom | -4.00 | -4.00 | -4.00 |
| cone base / foot ring top | 2.00 | 2.00 | 2.00 |
| collet top | 32.00 | 32.00 | 32.00 |
| holder bottom | 13.63 | 2.00 | 9.09 |
| flange underside | 67.63 | 56.00 | 63.09 |
| rim (receiver top) | 54.50 | 54.50 | 54.50 |
| flange underside - rim | 13.13 | 1.50 | 8.59 |
| plate top (nut seated) | 83.63 | 72.00 | 79.09 |
| collar top (plate top + 7.5) | 91.13 | 79.50 | 86.59 |
| nut skirt bottom (seated) | 27.63 | 16.00 | 23.09 |
| engaged length (rim - skirt bottom) | 26.87 | 38.50 | 31.41 |

Check: the d + 1.0 column is R minus (z0 + s_z) = 4.537 on every row. The Loftsman's "up to 10.3 mm" rim gap there omits z0; it is 8.59.

Inequalities:
- A1: holder bottom - floor >= m_floor > 0. K-max: 2.00 - 0 = 2.00; after the 1.5 stroke margin 0.50. PASS.
- A2: flange underside - rim > 0 in every pose. K-max 1.50. PASS (it is the intended hard stop, pair class G).
- A3: engaged length >= 24 in every pose. Minimum is R, 26.87. PASS (margin 2.87).
- A4: skirt bottom - floor >= P. K-max 16.00 >= 8.0. PASS. A nut cannot bottom: the plate seats on the flange first. WS9 is unrepresentable.
- A5: the d-dependence is nil. s_z,max is 9.925 for d = 90 and d = 105; only radii differ.

## 2. Register and cross-thread defence: the 40 mm figure is not what the stack supplies

### 2.1 What the register has to be measured at

The tilt that matters is the tilt of the nut axis against the receiver axis at the moment the first nut ridge touches the receiver lead-in. At that instant the nut skirt bottom is at the rim plane. The holder does not control the nut at any other moment.

Unit assembled (nut captured on the holder). Let skirt-below-flange S = L_n - t_f = 48 - 8 = 40.0.

| Case | Flange underside at first thread contact | Holder inserted L_ins1 | Source |
|---|---|---|---|
| Nut seated on flange (gravity, flat on flat) | rim + S = rim + 40.0 | L_h - 40.0 = 14.0 | L_h = 54.0 |
| Nut hanging on collar (lifted by p) | rim + S - p = rim + 38.5 | L_h - 38.5 = 15.5 | p = 1.5 |

The Loftsman's L_reg = 40.0 is the length needed, and L_h = L_reg + g_stop = 53.13 is not the length supplied at first contact. It is the insertion at pose R. At first contact the holder is inserted 14.0 to 15.5 mm.

### 2.2 Tilt budget by number

| Quantity | Value | Basis |
|---|---|---|
| alpha_crit | P / (2 D_T) = 8 / (2 x 153.68) = 0.02603 rad = 1.49 deg | the Loftsman's definition; peak-to-peak axial offset across the diameter of half a pitch |
| allowed total tilt | alpha_crit / 2 = 0.746 deg | safety factor 2 |
| theta_h = 2 g_reg / L_ins1 (holder in bore) | 14.0: 2.046 deg; 15.5: 1.848 deg; 40.0: 0.716 deg | g_reg = 0.25 |
| theta_n (nut on holder), seated | 0 (flat on flat; machining flatness 0.1 over 148 mm: 0.04 deg) | |
| theta_n, hanging on collar | atan(p / (r_flange + r_hole)) = atan(1.5 / 144.44) = 0.595 deg | plate rocks between flange top and collar underside |
| total, as built (hanging) | 1.848 + 0.595 = 2.44 deg | exceeds alpha_crit 1.49 by 1.6 times, and the allowed 0.746 by 3.3 times |

My Step 0 alpha_crit was atan(P / (4 D)). The Loftsman's allowed value 0.746 deg equals my critical value 0.746 deg. The two files agree on the limit; only the label differs. Use 0.746 deg as the limit and call it the allowed register tilt.

Verdict: as built, a cross-threaded start is reachable (tilt 1.85 to 2.44 deg against a thread-forgiving 1.49 deg). The T9 known-bad control (2 x alpha_crit = 2.98 deg) fires correctly, but the band between 1.49 and 2.98 deg is reachable and unprotected.

### 2.3 Replacement: stacked register by number

Two stacked contributors, holder bore and nut-on-holder.

| Item | Replace | With |
|---|---|---|
| Holder body length L_h | 54.0 | 80.0 (L_reg 40.0 + S 40.0; seated insertion 40.0) |
| Receiver rim above floor | 54.5 | 80.5 (2 + 80 - 1.5) |
| Lift play p (`nut.lift_play`) | 1.5 | 0.75 |
| Collar top above plate top | 7.5 | 6.75 |
| theta_h seated | 2.046 deg | 0.716 deg (limit 0.746, passes by 0.03 deg) |
| theta_h hanging | 1.848 deg | L_ins1 = 80 - 39.25 = 40.75, 0.703 deg |
| theta_n hanging | 0.595 deg | atan(0.75 / 144.44) = 0.297 deg |
| total hanging | 2.44 deg | 1.00 deg (safety factor 1.49 on 1.49 deg; seated 2.08) |

The deciding quantity is p: theta_n is 0.595 deg at p = 1.5 and the hanging total becomes 0.703 + 0.595 = 1.30 deg, safety factor 1.15. For safety factor >= 1.5 in the hanging case, theta_n <= 0.30 deg, so p <= 0.75 mm. Back-off lost motion becomes p / P = 0.094 turn (was 0.19).

Sensitivity (T9 input): L_h = L_reg + S where L_reg = 2 g_reg / (alpha_crit / 2). At g_reg = 0.35 it is 53.8, which is the coincidence that produced the old 54. The Loftsman's text, "at 0.35 mm L_reg becomes 54 and L_h 68", should read L_h = 54 + 40 = 94, not 68, because S is added, not g_stop. Only L_h = 80 supports the 40 mm figure and only at g_reg = 0.25.

Does the register see the key slot as a break? Yes. Key slot width 8.6 on a circumference of pi x 138.68 = 435.7 mm is 2.0 percent of the arc. The register arcs on either side remain; tilt is limited by arcs at the bore edge, not by the key. Key radial height: key tip at 69.09 + 3.0 = 72.09, slot floor at 69.34 + 3.3 = 72.64, radial gap 0.55 (not 0.3; the Loftsman's "0.3 deep" is 0.3 relative to the 3.0 key, but the 0.25 register clearance adds). The key never contacts the slot floor before the register arcs touch. PASS.

### 2.4 T9 inputs (final-shape measurements, Rule M)

| Input | Value | Measured from |
|---|---|---|
| g_reg | 0.25 | bore diameter minus holder OD, fitted cylinders |
| L_ins1 (seated, hanging) | 40.0, 40.75 | holder bottom to rim at the pose where nut skirt bottom z = rim z |
| P, D_T, alpha_crit | 8.0, 153.68 (or per D-1), 1.49 deg | fitted helix and major cylinder |
| register tilt limit | atan(2 g_reg / L_ins1) | tilt the holder to contact the bore at both ends |
| pass | register-limited tilt + theta_n <= alpha_crit / 1.5; thread ridges do not interfere (common volume < 0.01 mm3) at that tilt | |
| known-bad | tilt 2 x alpha_crit = 2.98 deg about a transverse axis at the bore edge: register arcs interfere (> 0.01 mm3) before any thread ridge does | must fire |
| S1 treatment | nominal pose: norm(axis x Z) <= 1e-4. Pose T (register-limited tilt): fitted tilt = 0.716 deg +/- 0.01 and < alpha_crit / 2. Two poses, two predicates; the nominal test is not relaxed | answers the Loftsman's S1 to S5 question |

## 3. Collet topology and the clamped-state solid

### 3.1 Alternating slits: counts

N = 12, 6 from the top (depth 32, ending in z = 0, leaving the foot web z -4 to 0) and 6 from the bottom (ending at z = 28, leaving the top web z 28 to 32). Slit phase phi_k = phi_key + 15 deg + 30 deg k.

| Quantity | Value |
|---|---|
| Components (shells) | 1 (zigzag band; adjacent fingers joined alternately at top and bottom webs) |
| Genus | 1 (band closes on itself; a solid torus) |
| chi = 2 - 2g | 0 |
| Euler check | V - E + F - R = 2 (S - g) = 0, with R = number of inner wires; every face simply connected apart from the foot ring, where R must be counted |
| Relief holes Ø6, radial axis, centre at depth 29 | each hole opens into its slit (slit 1.5 < 6): a keyhole notch. No genus change. A hole not tangent-connected to its slit would add +1 genus and +1 shell loop: the test must fire on it |
| Slit planes | contain Z: plane-to-axis distance < 0.01 |
| Top ring faces | 6 arcs; bottom 6 arcs; bore 6 faces; cone 6 strips, each notched by one bottom slit |
| Clamped slit width (mouth) | 1.5 - pi (3.5)/12 = 0.584 nominal; 0.434 worst (+/-0.15 non-uniformity): positive in all cases |

Key between slits: arc from the key centre to the nearest slit centre at the foot ring radius 63.79 is 63.79 x 0.2618 = 16.70 mm; key half-width 3.0 plus slit half-width 0.75 = 3.75; clear by 12.95 mm. At the bore (r = 53.5 for d = 105): 14.0 against 3.75, clear by 10.2. PASS for all seven collets (phase is a generator function, not a parameter). Adjacent relief hole centres 28.0 apart at the bore; hole diameter 6, web between holes 22 mm. PASS.

Slit-width floors, one note: the 0.5 mm `min_slit_clamped` is a design floor on the nominal (0.584 passes). The topological floor is "greater than the OCC fuse tolerance and the 0.01 contact band": 0.434 worst-case passes it. Keep them as two separate tests (C9a nominal >= 0.5, C9b worst >= 0.1). I accept w_s = 1.5.

### 3.2 Clamped-state solid and OCC strategy

Do not fuse any pair. Each part is its own solid. The clamped state is generated analytically, not by deforming the free solid:

1. Clamped collet = revolve of the clamped profile (bore radius = r_core, cone radius = rho_C(z) - (r_bf - r_core) - delta), slits regenerated at w_s - pi (B_f - d_core)/N, foot web and ring below z = 0 unchanged.
2. Holder cone built from the same `alpha` variable as the collet cone, not from a second parameter. Then the half-angle mismatch is 0 to floating error. If I allowed the S5 tolerance (0.02 deg) the radial deviation over 30 mm would be 30 x tan(0.02 deg) = 0.0105 mm, which is larger than any safe offset and would give crossing surfaces, hence slivers.
3. Offset delta = 0.005 mm radial inward on the collet cone only. It is 50 times the OCC default tolerance (1e-7), below the 0.01 mm contact band, and above the 1e-3 the Loftsman proposed (which is only 10 times the typical sewing tolerance of 1e-4 on revolved helices; I want the margin).
4. Pair test: BRepExtrema min distance = delta (class C requires min_dist <= 0.01) and common volume = 0 exactly. Never boolean-cut one against the other; `common()` of two disjoint solids is cheap and returns empty.
5. Contact patch area computed from the strip of the cone where distance <= 0.01, not from the intersection.

Which faces coincide, in the stack that the Loftsman's own axial numbers give: collet cone strips (6) against the holder cone over z = 2 to 32, a 30 mm strip (see D-2: not 18.37). The coincident circles are at z = 2 (holder bottom inner edge against collet cone base) and z = 32 (holder cone-to-cylinder transition against collet top). With the 0.005 offset the circles are 5 micrometres apart; no boolean touches them.

The Loftsman's reading (holder cone extending 11.63 below the collet cone base): that is not a sliver. The holder cone at z = 2 - x has radius 62.04 + x tan(alpha); the unclamped foot web (z < 0) has radius 63.79. They overlap for x from 2 to 9.925 over radial depth falling from 1.40 to 0: about 2 pi x 63 x 0.70 x 7.9 = 2.2e3 mm3 of real interference, and the holder bottom would be at -9.63, 9.63 mm below the floor. That reading cannot be built.

## 4. Contact classes (C, G, F), poses R and K, the Loftsman's numbers

Parts: Co core, Cl collet, H holder (with collar ring Cr bolted on top), N nut, W washer (see D-6), Rc receiver (floor, pocket, bore, rim, thread).
Classes: C contact required/allowed, G gap forbidden contact, F free. Value = gap in mm, nominal.

| Pair | R | K (max closure) | Class | Note |
|---|---|---|---|---|
| Co - Cl bore | 0.50 radial | 0 over patch | G / C | patch area test; tilt-free pose requires slit width > 0.1 |
| Co - Cl ledge | core sits on ledge, overlap 1.25 (both d) | same | C | ledge ID = d - 4; core d - 1.5 overlaps 1.25 |
| Co - H | 56.75 - 53.0 = 3.75 radial at cone top | 3.75 | G | PASS |
| Co - N plate hole | 17.1 radial | same | G | |
| Co - Cr | collar ID unspecified | | G required | the Loftsman must give collar ID >= 2 x 57; add to params |
| Co - Rc floor/pocket | core bottom on ledge, 4.0 mm ledge height above | | G (core never reaches pocket for d_core >= d - 4) | WS6 control |
| Cl - H cone | 0.30 radial (see D-1) | 0.005 | G / C | PASS in K; R fails by 2.05 under the as-built chain |
| Cl - H bottom | holder bottom 13.63, collet ledge top 2.0 | 2.00 | G | PASS, no ledge at fingers (contracted) |
| Cl - Rc foot pocket | 0.30 radial, ring bottom on pocket floor | same | C axial, G radial | |
| Cl - Rc key | key 6.0 x 3.0 in slot 6.6 x 3.3, 0.3 per side | | G | PASS |
| Cl - N | far | | F | |
| H - Rc register | 0.25 radial | 0.25 | G (contact only at tilt) | limit state defines the class; add pose T |
| H - Rc rim (flange underside) | 13.13 | 1.50 | G | the hard stop; 1.5 > RSS 1.11 PASS |
| H - Rc floor | holder bottom 13.63 | 2.00 | G | answers Loftsman's S6: add the floor pair, minimum 0.50 after overshoot |
| H key - Rc slot | 0.30 tangential, 0.55 radial | | G | PASS |
| H flange - N plate (via W) | 0 (seated), gap p = 0.75 (L) | 0 | C | see D-6 |
| N plate top - Cr underside | p = 1.5 (as built) | p | G in K, C in L | the S16 release pair; antiparallel n.n = -1 PASS |
| H body - N plate hole | 1.01 radial | | G | worst offset 0.55 |
| H flange / collar OD - N crest | 0.35 | 0.35 | G | worst-case 0.55 > 0.35: FAIL, see D-4 |
| N thread - Rc thread | bearing flank C; crest/root 0.35 G; other flank 0.60 G | | C only on flank pair | PASS |
| N skirt bottom - Rc floor | 27.63 | 16.00 | G | 16.00 >= P |
| N - E (cutter) | z_cut,min - collar top >= g_stop | | G | reference is the collar top (pose R, 91.13); take the maximum over poses |
| Cr - H top face | face on face, 4 x M6 | | C | separate solid; fused is wrong, separate is manifold |

F where G is required, or the reverse:
- Holder flange against nut plate through the pocket: without a washer the bearing pair is a 0.04 mm ring (see D-6). Required C, delivered a knife edge. Not an F/G swap but a contact-area failure.
- H - Rc register: classed G, but physically it is a limit contact (C at tilt). Class it G with the tilt pose T as the case where contact is expected. No change in the number.
- Cl - H cone in R: the Loftsman's chain gives G at 2.35 mm, not 0.30 (D-1).

## 5. Wrong states WS1 to WS11 (my W1 to W11)

| ID | State | Unrepresentable by the Loftsman's numbers? | Becomes a feature at Step 3 |
|---|---|---|---|
| WS1 | Collet upside down | Only if the holder's bottom inner radius is below D_L/2: 62.04 < 63.79 blocks the holder by 1.75 mm. With the as-built chain (64.09 > 63.79) the holder passes by 0.30 mm and the flip is not prevented. Depends on D-1 | Holder lead-in rule: holder bottom inner radius < collet wide end radius |
| WS2 | Holder upside down | YES. Flange OD 148.68 against receiver bore 138.68: 10.0 mm of interference | none |
| WS3 | Nut upside down | NO. Flipped nut (skirt up) sits on the holder with the plate on the flange, the skirt wraps the collar zone: collar OD 148.68 < nut crest 149.38 passes inside. No engagement, so S13 catches it only after the fact | Collar OD 152.4 (> crest bore 149.38 by 3.0): collar cannot enter a flipped skirt, so the collar cannot be installed on a flipped nut. Collar r 76.2 equals the cutting annulus edge, harmless |
| WS4 | Wrong-hand thread | YES at build: no hand field, one helix function | T1a, T1b, T1d backstops |
| WS5 | Cross-threading | NO (tilt 1.85 to 2.44 deg reachable, section 2) | L_h = 80, p = 0.75: tilt 0.72 deg seated, 1.00 deg hanging |
| WS6 | Wrong collet for core | Partly. 105 core into a 90 collet: 13.0 mm bore shortfall, no entry (YES). 90 core in 105 collet: core r 45.0 against ledge ID r 50.5: core falls through the ledge (S9 violated). One-step mismatch (core d - 2.5): sits on the ledge, grip window starts 1.0 mm higher, holder reaches the rim stop with the core not gripped: caught by the stroke test, not prevented | F3 sweep widened from 4x4 to 7x7 |
| WS7 | Collet not seated (propped on key) | NO. Foot key lug (radius 66.79) rests on the floor 4.0 mm above its seat: S3 gap 4.0 vs 0.05, caught | Chamfer the pocket slot lead-in; test remains |
| WS8 | Holder bottoms before clamp | Order is correct: rim stop 1.50 reached before the floor (2.00) and before the ledge at z = 0 (2.00 below holder bottom) | none |
| WS9 | Nut bottoms on base | YES. Plate seats on flange before skirt gets within 16.0 of floor; 2 pitches | none |
| WS10 | Base on frame upside down | not in the Loftsman's numbers | outside scope |
| WS11 | Slit over key | YES. Slit phase is key + 15 deg + 30 deg k, 12.95 mm clear. The 15 deg rotation control is the intended planted state | none |

Reachable wrong states after Step 2: WS3, WS5, WS7, and WS1 conditional on D-1. WS6 and WS7 stay test-caught.

## 6. Disagreements

Each is two numbers and the quantity that decides it.

| ID | The Loftsman | The Topologist | Deciding quantity |
|---|---|---|---|
| D-1 | Holder inner radius at its bottom = D_L/2 + c_s = 64.09. D_T = 153.68, nut OD 170.4 | Holder bottom sits at z = 13.63 (his L_h 54, rim 54.5, g_stop 13.13). rho_C(13.63) + c_s = 61.739 + 0.30 = 62.04. Holder OD at t_h = 5: 134.08. D_T = 149.58, nut OD 166.3, alpha_crit 1.53 deg | Radial gap between holder and collet cone at R, measured from the final shapes at z = 13.63: 64.09 - 61.74 = 2.35 (not c_s = 0.30). With 64.09 first touch needs the holder bottom at z = 0.30 and full closure at -7.9, below the floor (1.70 to 9.925 more travel). The axial numbers are needed by F6, A3 and T9; the chain must follow them |
| D-2 | Contact height at K-max 18.37 (L-4) | 30.0. The holder cone spans 2 to 32 at K-max, the collet cone 2 to 32. At core d + 1.0: 32 - 9.09 = 22.9. At first touch (R0): 32 - 11.93 = 20.1 | Overlap of axial intervals [max(2, z_holder_bottom), 32] using the table in 1.4. L-4 subtracts the travel from H as if the holder cone started at the collet cone base in R, which contradicts L_h |
| D-3 | Register 40.0 mm, L_h 54.0, p = 1.5 | Insertion at first thread contact is 14.0 (seated) / 15.5 (hanging). Needed 40.0. L_h = 80.0, p = 0.75 | L_ins1 = L_h - (L_n - t_f) + p_hang. Tilt: 2.44 deg total as built against alpha_crit 1.49 |
| D-4 | Flange and collar OD = thread minor 148.68, clearance to nut crest 0.35 | Offset stack = thread lateral play 0.30 + register 0.25 = 0.55 > 0.35. Flange OD <= nut crest diameter - 2 x (0.55 + 0.05) = 149.38 - 1.20 = 148.18 | Flange-to-nut-crest distance at the worst combined offset: 0.35 - 0.55 = -0.20 (contact). The collar in WS3 (OD 152.4) is a separate feature and is not affected: the collar sits above the plate, outside the thread bore |
| D-5 | Two M6 jacking holes through the flange at r = 71.84 | Hole cylinder Ø5.0 (tap drill) spans 69.34 to 74.34 and is tangent to the flange OD, with 0.25 to the holder body at the inside edge; wall needed 1.2 each side. Required radial width 5.0 + 2.4 = 7.4 (M6 clear: 8.4); available 74.34 - 69.09 = 5.25 | Containment: hole minus flange annulus, wall >= 1.2 fails by 2.15 to 3.15 mm. Jacking holes cannot sit in the flange. The Loftsman must supply another jacking path (jack from the collar or through lugs inside the nut crest bore) |
| D-6 | Washer pocket annulus 70.1 to 74.3 is a recess, plain bearing T_hold 10.4/8.9 N m | The flange top annulus under the plate is r 70.1 to 74.34. The pocket takes 70.1 to 74.3, leaving a ring 0.04 mm wide (area 18.7 mm2) when no washer is fitted. Washer is a separate part, always present (printed plain ring or PTFE); thickness >= pocket depth + 0.3 = 1.3; OD 148.2 < flange 148.68 | Bearing contact area without washer: 18.7 mm2 against annulus 606.5 mm2 assumed by the T7 plain case. Also his mean bearing radius 71.7 is 72.2 by (2/3)(r_o3 - r_i3)/(r_o2 - r_i2); negligible effect on k (0.3 percent) |
| D-7 | S15 form: L_n >= s + 24 + 8 = 41.9 | L_n - t_f >= 24 + z0 + s_z,max + m = 37.13 (L_n >= 45.13, which is the form he used to set 48). The "+8" in S15 is a pitch of receiver run, not nut length. Receiver run from the rim >= E_K + P = 38.5 + 8 = 46.5, rounded to 48 for turns, plus land 4.0 | S15 as written understates nut length by 3.2. The 48 mm figure itself stands |
| D-8 | Wing ellipse centred rho 70, semi-axis 45 radial: spans rho 25 to 115 | Plate hole is r 70.1 and the holder body r 69.09 passes through it; the ellipse region rho < 70.1 (45 mm of its span) lies inside the hole and the holder | Wing planform must be trimmed to rho >= 85.2 (nut body OD / 2) or to the plate: common(wing, holder) volume must be 0. Visible wing then 85.2 to 115 = 29.8 mm, arm 100 mm unchanged |
| D-9 | K rim gap at core d + 1.0: 10.3 | 8.59 | 13.13 - z0 (1.701) - 2.836 = 8.593 |

## 7. Resolved list: accepted as written

- Thread hand (H1 to H4), lead angle, flank-pair rule, single start, helix start rule, integer turns for the nut (H5, H6, H7 nut part).
- Cone half-angle 10 deg on both cones from one variable; self-lock test 0.176 < 0.25 (C1 to C5); retirement of the releasing-cone fallback; S16 resolves to the captured-collar branch (C6) with the pair named: plate top face (n = +Z) against collar underside (n = -Z).
- z0 = 1.701; s_z,max = 9.925; s_z at d + 1.0 = 2.836; both d-independent; stop gap formula 13.13 as z0 + s_z + m.
- Radial chain as a formula (the structure is right; the wide-end term is D-1).
- Collet length 36, cone height 30, foot ring 6, pocket 128.18 over D_L 127.58 (0.30), pocket depth 4, foot protrusion 2.0.
- Collet law: free bore d + 2, window [d - 1.5, d + 1.0], closure 3.5, N = 12, strain 0.00954 against 0.010, windows abut 88.5 to 106.0; replacement of the C8 widening test by a continuous sweep.
- Slit phase function, key mid-web, 12.95 mm clear (S17 to S21).
- Alternating slits: 1 component, genus 1, chi 0 (S22, S23); relief holes as keyholes.
- Nut thread 48 mm, engaged 26.87 (R) and 38.5 (K) (S13); exposure measured from the collar top (S14), taken in pose R.
- Plate hole 140.2 against holder OD 138.18, 1.01 per side, clears every pose (worst offset 0.55). Collar as a separate bolted ring: manifold as a separate solid, class C on a planar face.
- S12: receiver run 46.5 minimum (E_K + P), 4.0 land; nut cannot bottom (A4, WS9).
- WS2, WS4, WS9, WS11 unrepresentable.
- Planted controls: WS5 tilt 2.98 deg (register must fire first) and WS11 15 deg rotation are the intended states.
- Throat check P8 (slack 1.29 per side, 0.29 at envelope_max).
- Tessellation: n >= 138 per turn for the export (0.020 deflection).

Replies owed by the Loftsman: D-1, D-3, D-4, D-5, D-6, D-8. D-2, D-7 and D-9 follow from his own numbers and need only a confirmation.
