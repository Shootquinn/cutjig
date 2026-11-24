# Loftsman Geometry Review of the Step 0 Gameplan

Scope: geometry only. Sources read: workorder.md, step0_software_engineer_revision.md, step0_engineer_source_extraction.md. Numbers marked PROPOSED are seeds for params.yaml, worked by hand so the Engineer can check the script against them. Numbers marked UNVERIFIED have no source and are settled by the Step 9 coupon or by Mines.

## 1. Ranked findings

| Rank | ID | Finding | Hits |
|---|---|---|---|
| Blocker | G1 | The default thread Tr 60 x 8 cannot exist in this jig. A 60 mm major diameter is smaller than the 90 to 105 mm core it must surround. The thread diameter is an output of the radial stack, not a free choice. Worked chain gives a major of about 165 mm. | T2, T6, E1, A2, nut OD, bed fit, Detail 2 |
| Blocker | G2 | A Tr thread (30 degree included, 15 degree flank from the radial plane) prints with a 15 degree down-facing flank on both boss and nut. That is an unsupported near-horizontal roof. Use a symmetric 45/45 form. | T1 to T3, Detail 2, Detail 6 |
| High | G3 | The cone angle is unspecified. It is a single choice that sets release versus lock, radial budget, clamp stroke and holding torque. Self-locking cones will not release. | F1, C4, T5 |
| High | G4 | Friction holding torque is the binding requirement and has no analytic check. Hand-tightened, a printed cone collet holds about 8 N m against the 20 N m placeholder. The plan cut the wing-nut moment-arm check as ceremony. Reinstate it as an analytic test. | Detail 6 cut list, new T7 |
| High | G5 | A2 models the cutter as a bare tube (152.4 / 146.05). The cutting face is an annulus that reaches past the tube wall, so the keep-out plane is the top of the highest fixture within that footprint, wing tips included. F4 measures from the holder top, which is wrong. | A2, F4, E5 |
| High | G6 | Rigid-body clamp pose contradicts A1 and F1. A free collet seated deeper in a cone interferes by volume. The clamped state needs its own solid (equations in 5.2). | A1, F1, T4, T5 |
| High | G7 | Coverage (E4) and slit design are one problem. The closure a collet needs fixes slit count through hinge strain. Law in 4.3. Recommendation: 2.5 mm family spacing (7 collets). | C5, C8, T5 |
| Medium | G8 | STL tessellation can eat the thread clearance. Default FreeCAD deflection (0.1 mm) is the same size as the radial clearance. E2's 1 percent volume check will not see it. | E2, X1, T3 |
| Medium | G9 | C3 probes at 0, 120, 240 degrees can fall inside a slit when the slit count is a multiple of 3. | C3 |
| Medium | G10 | The holder flange needs an axial hard stop above the collet. Without it, nut torque sets slit strain, not geometry. | T5, C5, E7 |
| Medium | G11 | Core tilt in the clamp (E6) has a closed formula. See 6. | E6 |
| Low | G12 | Missing analytic definitions: key or flat, debris tray and drain, engraving, lead-in chamfer, core stop. Listed in section 8. | F5 |

## 2. Thread definition (boss and wing nut)

### 2.1 Form
Single start, right-hand, lead L = P = 8 mm (PROPOSED; a coarse pitch is right for FDM). Handedness check: helix (rho cos t, rho sin t, z0 + P t / 2 pi) with t increasing is right-hand (counter-clockwise rising seen from +Z). The nut uses the same sense. T1 passes when the sign of dz/dt is positive for both parts.

Profile: symmetric trapezoid with 45 degree flanks measured from the radial plane (90 degree included angle). Reason: the loaded flank of the boss (its underside) and the unloaded flank of the nut tooth both face down when the axis is vertical, and both parts print axis vertical. Any flank below 45 degrees from horizontal needs support in a thread that must stay clean. A buttress with a steep unloaded flank fails the nut. Hoop load from the 45 degree wedge is F tan 45 / 2 pi, about 0.16 F, trivial at 1000 N.

Basic profile (boss), tooth depth h = 2.5 mm (PROPOSED):
- crest flat f = (P - 2h) / 2 = 1.5 mm, root flat f = 1.5 mm
- axial tooth width at radius rho: w_b(rho) = f + 2 (R_T - rho), R_T = D_T / 2, for R_T - h <= rho <= R_T
- Flank surface (ruled conical helicoid): S(t, rho) = (rho cos t, rho sin t, z0 + P t / 2 pi +/- w_b(rho) / 2)

Nut (internal), with radial crest clearance c_r and axial flank gap g_a per side (PROPOSED c_r = 0.35, g_a = 0.25, UNVERIFIED until the Step 9 coupon):
- nut tooth tip radius (inner): R_nc = R_T - h + c_r; nut groove radius (outer): R_nr = R_T + c_r
- nut tooth axial width at rho: w_n(rho) = P - w_b(rho) - 2 g_a

Total axial play is 2 g_a = 0.5 mm. Engagement shear area at 3 turns is far above any 1000 N load, so strength is not what bounds the thread; clearance and ovality are.

### 2.2 Closure of the helix
- Cut each thread length as an integer number of turns N_t, so start and end angles coincide: H_thread = N_t P. The Engineer's 24 mm minimum engagement is N_t = 3.
- Single start means any start angle engages. Fix t0 = 0 on +X for boss and nut so both scripts share one helix function. The holder key is referenced to the base, not to the thread start.
- Run-out: a 45 degree lead-in chamfer on the boss top and nut mouth, depth h. Terminate the boss helix on a cylindrical land, not in mid-flank.
- Sweep validity: a swept profile is valid only if profile width at the widest radius (c + 2h = 6.5 mm) is less than P = 8 mm. It is; the margin is 1.5 mm, so the sweep cannot self-overlap. Keep it that way if P or h change: require c + 2h + 2 g_a < P.
- Export: tessellation chord deviation e = R (1 - cos(dtheta / 2)). With R = 82 mm and e <= 0.02 mm, dtheta <= 0.044 rad, about 140 segments per turn. Set STL linear deflection <= c_r / 10 = 0.035 mm and angular deflection <= 2 degrees. See G8.

### 2.3 Thread size is derived (G1)
The radial chain, outside in, at d = 105, with alpha the cone half-angle and H the cone height (PROPOSED seeds in brackets):

D_S = B_f(105) + 2 t_c (t_c = 5 mm min collet wall at the small end; B_f(105) = 107 mm) = 117 mm
D_L = D_S + 2 H tan(alpha) (alpha = 20 degrees, H = 30 mm) = 138.8 mm
holder OD = D_L + 2 t_h (t_h = 5 mm) = 148.8 mm
boss ring ID = holder OD + 2 x 0.5 = 149.8 mm
boss root OD (thread minor) = ID + 2 t_b (t_b = 5 mm) = 159.8 mm
D_T (major) = minor + 2h = 164.8 mm, call it 165 mm

State this as the governing equation: D_T = B_f(105) + 2 t_c + 2 H tan(alpha) + 2 (t_h + t_b + 0.5 + h). The Engineer replaces the label "Tr 60 x 8" with this output and carries the number through T2, T6, A2 and the nut OD. Nut body OD is about D_T + 2 (c_r + 8) = 181 mm. Wing span in 7.2 reaches about 230 mm, inside 256 - 5 = 251 mm, so T6 passes on a 256 bed with 21 mm to spare. If the printer is smaller, the nut splits or the cone steepens less.

## 3. Cone (conic) seat: E2 and the stack

E2 answer, recommended: the workorder is literally met. The boss seats the collet; the holder presses it.
- The boss is a tubular riser with the external thread and an internal flat annular land at its floor. The collet's large-end ring stands on that land. This is "the boss seats the collet".
- The holder is a sleeve with a female cone (small end up), a top flange and a key. It slides over the collet inside the boss bore, keyed to the boss.
- The wing nut screws on the boss and bears on the holder flange. Tightening drives the holder down; the female cone closes the collet.
- A closed force loop exists only if the holder flange sits above the boss rim with a gap. Nut-boss-holder alone is a closed loop that moves nothing. The gap is the stroke (3.2).

Collet outer cone: large end down, small end up (self-supporting in print, and the holder cone is the same, narrower toward its top, self-supporting too).

### 3.1 Taper angle (G3)
Closure by friction cone. Let mu_k be printed PETG on PETG (UNVERIFIED; seed 0.35 static).
- Self-locking: tan(alpha) <= mu_k. With alpha = 10 degrees, tan = 0.176 < 0.35: the collet will stay jammed after the nut backs off, because spring-back axial force is F_r tan(alpha) and friction resists with F_r mu_k. The holder, lifted by hand, takes the wedged collet and core with it. Releasing fails.
- Releasing: tan(alpha) > mu_k, i.e., alpha > atan(mu_k) = 19.3 degrees. Seed alpha = 20 degrees. Measure mu_k on the Step 9 cone coupon by tilt-plane test and set alpha = atan(mu_k) + 2.5 degrees.
- Cost of releasing: radial budget grows (D_T 165 against 158 at 10 degrees) and holding torque per axial force falls 28 percent (see 5.1). Alternative if the budget or torque is unacceptable: alpha = 10 degrees with a captive-flange nut that lifts the holder on back-off. That adds two bearing faces in print. I recommend the releasing cone first.

### 3.2 Stroke and stop
Radial closure at the cone surface equals axial holder travel times tan(alpha). The relation:

s_z = (B_f - B_c) / (2 tan(alpha)), where B_c is the clamped bore.

For a family closure Delta = B_f - (d - tau), s_z = Delta / (2 tan alpha). Seed (Delta = 3.5, alpha = 20 degrees): s_z = 4.8 mm. Add the free seat gap z0 = c_s / tan(alpha), with c_s = 0.30 mm radial seat clearance: z0 = 0.8 mm. Hard stop gap (holder flange to boss rim): g_stop = z0 + s_z + 0.7 mm margin = 6.3 mm. That is under one pitch (8 mm); about 0.8 turn from first touch to the stop. Plan for it: torque rises sharply, which is good for a hand nut, and thread backlash (2 g_a = 0.5 mm) is a visible fraction of it.

The stop is common to the family only because Delta is common (4.3). The hard stop bounds slit strain independent of nut torque (G10).

Nut thread length: L_n >= min_engage (24) + g_stop (6.3) + P (8) = 38.3 mm, so 5 turns, 40 mm.

## 4. Collet: one law, diameter d as the parameter

Domain: 90 <= d <= 105 mm. Outside the domain the generator raises an error (P1 rejects 89 and 106 already).

### 4.1 Fixed versus scaled

| Quantity | Law | Scales with d? |
|---|---|---|
| Free bore B_f | d + tau + c_i (tau core tolerance, c_i insertion clearance, diametral) | Yes, linear |
| Clamped bore B_c | equals the actual core diameter | Per use |
| Closure Delta | B_f - (d - tau) = 2 tau + c_i | No |
| Cone half-angle alpha, D_S, D_L, H, seat land height | fixed by the radial chain at d = 105 | No (holder and boss common) |
| Wall at the small end t(d) | (D_S - B_f) / 2 | Yes: 12.5 mm at 90, 5 mm at 105 |
| Slit count N, slit width w_s, slot depth h_s | 4.3 | No (law below) |
| Core stop, key, flange | fixed | No |
| Engraved label | d | Yes (text only) |

The bore is the only dimension on the closing side that scales. The outer cone is invariant, so holder, boss, nut, stop gap and stack height do not depend on d. T5's remark that stack height is monotonic in d is true in a stronger form: it is independent of d. Testing d = 90 and 105 then bounds the bore range and the wall, not the stack.

### 4.2 E3: one formula for bore and clamped bore
bore_free(d) = d + tau + c_i. Seed tau = 1.0 (UNVERIFIED), c_i = 1.0, so B_f = d + 2. The Engineer's T5 text ("at least d + insert_clearance") with tau = 1 makes zero clearance at the loose core. Use d + tau + c_i.
bore_clamped for core diameter d_c: d_c. Closure that case needs: Delta_c = B_f - d_c <= Delta.
C3 asserts bore_free only. A separate test asserts the clamped-state solid (5.2).

### 4.3 Coverage, slit count and width (E4, G7)
Cover real cores in [d_i - a, d_i + b]; family spacing s requires s <= a + b. Closure Delta = a + b + c_i = s + c_i.

Closure by slits (alternating slits, as in ER collets): slits start from the top for odd indices and from the bottom for even; the web at each slit end is a hinge. Total slit closure across the ring = pi Delta (circumference reduction for a radial closure of Delta / 2). With N slits, per-slit closure: dw = pi Delta / N.

Hinge strain (screening model, needs the coupon): epsilon_web = h_w dw / (2 h_s l_h)
- h_w web height (axial), seed 4 mm
- h_s slot depth, seed 32 mm
- l_h effective hinge length, taken as the diameter of the keyhole relief at the slot end, seed 6 mm
- epsilon allowable for PETG, in-layer, UNVERIFIED; seed 0.01 (E7)

Solve for slits: N >= pi Delta h_w / (2 epsilon h_s l_h), rounded up to an even number.
- s = 5 mm (4 collets): Delta = 6, N >= 19.6, so N = 20. Tight, 22 mm segments, 20 relief holes.
- s = 2.5 mm (7 collets: 90, 92.5, 95, 97.5, 100, 102.5, 105): Delta = 3.5, N >= 11.5, so N = 12.
- s = 2.0 mm: Delta = 3, N = 10.

Recommendation: s = 2.5 mm and N = 12. The generator already takes any d, so the extra collets cost a params line plus print time. The workorder says "a separate collet per diameter"; seven diameters is a reading the human must accept. If the human insists on four, N = 20 and the web strain is the Step 9 coupon's first question.

Slit width at the bore: w_s = pi Delta / N + w_min, with w_min = 0.5 mm (the clamped residual, matching T5's min_slit_clamped): s = 2.5 gives 0.916 + 0.5 = 1.42, set 1.5 mm. Independent of d, so one number for the family. Set an angular position of slit k at phi_k = 2 pi k / N + phi_0.

Orientation: web bending stress lies in the layer plane for alternating slits (horizontal webs). Axial finger cantilevers would bend across layers, the weak direction, and are the reason to prefer alternating slits over fingers.

### 4.4 Analytic volume (for C2)
Frustum shell: V_outer = (pi H_c / 12) (D_L^2 + D_L D_S + D_S^2) for the cone zone of height H_c, plus the solid ring below it. Subtract the bore cylinder pi B_f^2 L / 4 and N slits at N w_s h_s t_avg, with t_avg the mean wall over the slot depth, then add relief holes. Give the Engineer this as the C2 expectation. Each cut is tested separately (3 percent), which discriminates the slits, because the full-part 5 percent band does not: at d = 105 the slits are about 5 percent of volume.

### 4.5 C3 probes (G9)
Probe azimuths must avoid slit centers: use phi_p = phi_0 + 180 / N + 120 k (degrees). Reject any probe that returns a slit hit. With N = 12 and slits at 0, 30, 60, ... the Engineer's 0, 120, 240 hit slits at all three angles.

## 5. Clamp physics

### 5.1 Holding torque (G4)
Axial force F from the nut. Cone mean radius r_m, height H, kinetic friction mu_k, core friction mu_c (UNVERIFIED; seed 0.4 concrete on PETG).
- Cone pressure p_cone = F / (2 pi r_m H (tan alpha + mu_k))
- Core pressure (thin-wall hinge ring) p_core = p_cone r_m / r_b = F / (2 pi r_b H (tan alpha + mu_k)), r_b = B_f / 2
- Holding torque T_hold = mu_c F r_b h_g / (H (tan alpha + mu_k)), h_g the grip height (take h_g = H)

Nut torque for F, pitch radius r_p = (D_T - h) / 2 = 81 mm, thread friction mu_t = 0.25 (UNVERIFIED):
- lead angle lambda = atan(P / (pi 2 r_p)) = 0.90 degrees
- mu' = mu_t / cos(45 degrees) = 0.354
- T_nut = F [ r_p (tan lambda + mu') / (1 - mu' tan lambda) + mu_b r_b,bearing ] = F (0.0301 + 0.0175) m = 0.0476 F m (bearing mu_b = 0.25, mean bearing radius 70 mm)

Hand: two hands on wings, F_h = 60 N each at lever arm a = 100 mm gives T_nut = 12 N m, so F = 252 N, so T_hold(d = 105) = 0.4 x 0.0535 x 252 / 0.664 = 8.1 N m; at d = 90, T_hold = 6.9 N m. Required 20 N m placeholder (UNVERIFIED, extraction C5) with safety factor 2 needs F = 1330 N, which is 63 N m at the nut. Hand-tightened PETG cannot do that. The numbers are PROPOSED seeds; the shape of the result will not change: a 165 mm thread gives F / T = 21 per meter, poor mechanical advantage.

Levers the Engineer has: a PTFE or ball thrust washer (mu_b 0.05 lowers the bearing term to 0.0035, F = 357 N at 12 N m); longer wings; a tommy-bar socket in the nut; lubrication; a shallower cone (self-locking, 3.1). Or the true torque reaction is smaller than 20 N m, which only Phase I can say. Reinstate the moment-arm check as T7: T_hold(d, F_hand) >= SF x T_load, with T_load UNVERIFIED and labelled as an assumption in the report.

### 5.2 Clamp-pose solid (G6)
For a rigid cone seat, shrinking the collet radially by Delta_R is geometrically identical to sliding it axially by s_z = Delta_R / tan(alpha). Build two collet states from one generator call:
- free: bore B_f, slit width w_s, outer cone D_S and D_L.
- clamped onto core d_c: bore d_c, slit width w_s - pi (B_f - d_c) / N, outer cone radii reduced by Delta_R = (B_f - d_c) / 2.

Place the clamped solid at holder-relative axial offset s_z; its cone coincides with the holder cone. Then F1's clamp-pose claim holds: common volume < 0.01 mm3 and positive contact area. Without this, a rigid collet pushed into a rigid cone overlaps by volume 2 pi r_m H s_z tan(alpha) cos(alpha) approximately, which A1 would flag.

Coincident conical faces break OCC Booleans. Offset the clamped solid by 1e-3 mm radially for the common-volume test, or compute contact as face-to-face distance. Topologist to confirm (section 9).

## 6. Core tilt and coaxiality (E6)
Free bore B_f = d + 2 leaves 1 mm radial clearance per side before clamping; clamped, residual is the tolerance mismatch. Tilt of the core axis from the holder axis before full clamp: theta_tilt = c_r,loose / h_g. With 1 mm and h_g = 30 mm: 1.9 degrees; tip displacement at a core 500 mm tall: 500 tan(1.9 degrees) = 16.6 mm. Clamped, the 12 line contacts at the leg midpoints centre the core to within the print tolerance of the cone, about 0.3 mm over 30 mm, so 0.6 degrees, 5 mm at the tip. This is a lateral-guide question for Step 10; I do not add a test. Report both numbers as the tilt bound.

## 7. Wing nut

### 7.1 Body
Internal thread per 2.1, nut length 40 mm (3.2), bearing face on the holder flange with a recess for a PTFE or ball washer. Lead-in chamfer 45 degrees. Nut ID = 2 R_nr = D_T + 2 c_r = 165.7 mm; body OD about 181 mm.

### 7.2 Wings
Two wings, 180 degrees apart. Elliptical planform (a conic, so every point follows from the ellipse equation): (rho - rho_0)^2 / a^2 + (z - z_0)^2 / b^2 <= 1. Seed a = 45 mm radial, b = 18 mm (so wing height 36 mm), tangential thickness t_w tapering 12 mm at the root to 8 mm at the tip, root fillet 6 mm. Wing tip radius about 115 mm, effective hand arm a_h = 100 mm.

Check: the wing is a vertical fin printed axis vertical, so bending stress runs in the layer plane. Root stress under a tangential hand force F_h with arm l (root to hand): sigma = 6 F_h l / (h_w t_w^2). With F_h = 150 N (abuse), l = 50 mm, h_w = 30 mm, t_w = 10 mm: 15 MPa. In-layer PETG tensile strength is of order 45 MPa (UNVERIFIED), safety factor about 3. Moment arm for torque: T = 2 F_h a_h.

### 7.3 Cutter relation (G5)
With D_T about 165 mm, the nut cannot pass inside the 146.05 mm bore. Branch 2 of A2 is forced: the nut top (including wing tops) is the hard stop. Define the stop plane z_stop = max z of any fixture with rho_out > 73.025 - m_r. F4 becomes: core top above z_stop by at least 106.369 + margin (UNVERIFIED for the 6 in iris). Wing height matters: wings at 36 mm raise z_stop above the holder top by the wing height unless the wings stay below the flange plane. Place wing tops at or below the nut top plane, or add the wing height to F4.

## 8. Cutter clearance envelope (100 mm core in 146.05 mm bore)

Radial gap per side: g(d) = (146.05 - d) / 2: 28.025 at 90, 23.025 at 100, 20.525 at 105, confirmed. Above z_stop, only the core and the collet's small-end zone may sit inside the tube: allowed fixture radius rho <= 73.025 - m_r. The collet small end D_S / 2 = 58.5 mm leaves 14.5 mm per side, so it clears (m_r = 3).

Missing in the plan: the cutting face is an annulus that extends radially from the core to beyond the tube wall (the 7 in model has a head of r = 107 mm; the 6 in head is unmeasured, extraction section 7 item 4). A2's tube solid (152.4 / 146.05) therefore under-represents the keep-out: the face below the tube end sweeps everything between the core and the face OD. Treat the keep-out as two solids: the tube (rho 73.025 to 76.2, full stroke) and a face annulus (rho from d / 2 + kerf to R_face, thickness t_face, at the lowest point). R_face is UNVERIFIED. Until measured, take R_face = 76.2 + 10 mm as a flagged assumption. Add negative control: a ring in the face annulus path fires.

## 9. Required Topologist cross-review (A.4 geometry rule)

Per Detail 2 and the slots listed under Design Notes, the following need two geometry-competent sign-offs before build:
1. Thread sweep validity: profile width versus pitch, helix sense of boss versus nut, start and end faces, no self-intersection, manifold solid after sweep and Boolean.
2. Seat half-spaces: coincident conical faces in the clamp pose (5.2); offset strategy for OCC.
3. Slit topology: slot ends on the cone surface, keyhole relief holes, face and edge counts for C7, alternating pattern phase.
4. STEP versus STL of the helicoid and cone: tessellation tolerance (G8) and the X1 independent re-measure.
5. The two-state collet (free and clamped) as one generator: parameter continuity of the cone.
6. Mirror and flip control for T1 and A3 (a mirrored nut must fire; a flipped collet must fire).
7. Keep-out solids for A2 (tube plus face annulus): sweep Boolean validity.
8. Step 4 (exploratory), Step 7 (production) and Step 8 (final topology gate), as the gameplan lists.

## 10. Steps lacking an analytic definition

| Step or item | What is missing |
|---|---|
| Detail 2 thread | Only a label "Tr 60 x 8". No profile, flank angle, depth, clearance equations, closure rule. Supplied in 2. |
| Taper | No angle, no radial budget. Supplied in 3. |
| bore_free(d) | Flagged by E3, not solved. Supplied in 4.2. |
| Clamp range | E4 open. Supplied in 4.3. |
| Slit | Count and width unstated; no strain relation. Supplied in 4.3. |
| Collet height, ring height, seat land | Unstated. Only H and the radial chain are given here; the ring height h_r and total collet length are open. |
| Anti-rotation key or flat | Listed in F5, no geometry. Needs width, height, keyway clearance. |
| Debris tray and drain | Listed in F5, no geometry at all. |
| Core stop | Listed, no height or form. |
| Engraved label | Text position and depth open. |
| Wing nut planform | Only "very large". Supplied in 7.2. |
| Cutter face | Not defined in any source for the 6 in drill. A2 depends on it. |

## 11. Tests to add or amend (for the Software Engineer)

- T2 reads D_T from the derived chain, not a constant. Add flank angle (45 degrees +/- 0.5), tooth depth and crest flat.
- T3: also assert axial flank gap 2 g_a and radial crest clearance c_r.
- New T7: holding torque check from 5.1, with mu values labelled UNVERIFIED.
- New T8: print overhang rule: no down-facing thread flank below 45 degrees from horizontal (a sectional probe, not a slicer script). Known-bad control: a Tr 15 degree profile must fire.
- C3 probe azimuths (4.5); C5 slit width equals the law in 4.3.
- E2: tessellation deflection stored in the STL result JSON and asserted <= c_r / 10.
- F1 clamp-pose uses the clamped solid (5.2).
- A2 and F4 use the face annulus and z_stop (7.3, 8).

## 12. Open items for the Engineer to decide with a number

1. Cone half-angle: releasing 20 degrees versus self-locking 10 degrees with a captive nut (3.1). Settled by measured mu_k.
2. Family spacing: 2.5 mm (7 collets, N = 12) versus 5 mm (4 collets, N = 20) (4.3).
3. Hand torque and thrust bearing: PTFE or ball washer, wing arm length (5.1).
4. Collet total length and ring height (section 10).
5. Core tolerance tau and insertion clearance c_i (both seeded, tau UNVERIFIED).
