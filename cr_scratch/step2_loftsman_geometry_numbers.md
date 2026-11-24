## 0. Corrections to my own Step 0 numbers (read first)

Four of my Step 0 figures were wrong or incomplete. The new numbers below replace them.

| ID | Step 0 statement | Correct | Effect |
|---|---|---|---|
| L-1 | Holding divisor tan(20) + 0.30 = 0.664 | tan(alpha) + mu_k = 0.364 + 0.35 = 0.714 | Releasing-cone holding at 12 N m falls from 8.1/6.9 to 7.1/6.1 N m (d = 105/90) |
| L-2 | Free tilt = c/h_g = 1.9 degrees | Core touches opposite bore edges at the two ends, so tilt = (B_f - d_core)/L_bore = 2.0/36 = 3.18 degrees | Tip offset 27.8 mm at 0.5 m, 41.7 mm at 0.75 m (was 16.6) |
| L-3 | Radial chain omitted the seat clearance c_s | Holder cone sits c_s outside the collet cone, so 2 c_s enters the chain | +0.6 mm on D_T |
| L-4 | Contact patch = H = 30 mm | The holder cone travels z0 + s_z down; the clamped collet cone overlaps it over only H - z0 - s_z = 18.4 mm at full closure | Grip and contact height drop 39 percent at the shallow cone; holding is unaffected (see 4.2), contact area stays far above `seat.min_contact_area` |

Sensitivity that Step 0 missed: at alpha = 10 degrees one millimetre of radial print error is 1/tan(10) = 5.67 mm of axial stroke. The stop margin must be sized on that (section 5).

## 1. Taper

| Quantity | Formula | Value | Status | Test |
|---|---|---|---|---|
| Cone half-angle alpha | chosen below atan(mu_k_min) | 10 degrees | ASSUMED (`cone.alpha`) | A3 (equal half-angles within 0.02 degrees), F1 |
| Friction bound atan(mu_k) | mu_k range 0.25 / 0.35 / 0.50, all ASSUMED (printed plastic on printed plastic, unmeasured) | 14.04 / 19.29 / 26.57 degrees | ASSUMED | A3 release clause, Step 8 cone coupon |
| Self-lock test | tan(alpha) < mu_k | tan(10) = 0.176 < 0.25: locks over the whole assumed range | DERIVED | A3 |
| Free closure Delta | Delta = (d - a) shortfall: Delta = a + tau + c_i, a = window_below = 1.5 | 1.5 + 1.0 + 1.0 = 3.5 mm diametral (same for all d) | DERIVED | C9, C8 |
| Seat gap z0 | c_s / tan(alpha), c_s = `fit.seat_clearance` = 0.30 | 1.701 mm | DERIVED | F1 (R), F6 |
| Stroke s_z, max closure (core at d - 1.5) | (Delta/2) / tan(alpha) | 9.925 mm (identical for d = 90 and d = 105) | DERIVED | F1 (K), F6 |
| Stroke s_z, core at d + 1.0 | (c_i/2) / tan(alpha) | 2.836 mm | DERIVED | T5 |
| Stop margin m | section 5 stack, RSS 1.11 mm, rounded up | 1.5 mm | ASSUMED | F6 |
| Stop gap g_stop (flange underside to receiver rim, nominal pose) | z0 + s_z,max + m | 13.13 mm | DERIVED | F6, A3 (stroke inequality) |
| Contact height at full closure | H - z0 - s_z,max | 18.37 mm | DERIVED | F1 |

The stop gap is not 6 mm. `stop.hard_stop_gap` = 6 and the "about 6 mm" in F6 and Detail 9 item 6 are the 20 degree numbers. At 10 degrees the gap is 13.13 mm, 1.64 pitches. The pinch point at the flange-to-rim gap is twice as deep as the plan assumes.

Self-release: the shallow cone does not self-release. It locks over the entire assumed mu range, as designed. Release comes from the captured lift collar (section 2.7). Lift force to free a locked wedge: F_lift = F (mu_k - tan alpha)/(tan alpha + mu_k) = 0.33 F at mu_k = 0.35 (0.17 F at 0.25, 0.48 F at 0.50). At F = 260 N that is 86 N (45 to 125 N over the range), about 4 N m at the nut. ASSUMED inputs; Step 8 coupon and H5.

### Ruling against the releasing-cone fallback, by number

| Quantity | alpha = 10 (captured flange) | alpha = 20 (releasing cone) | Test |
|---|---|---|---|
| Thread major D_T | 153.68 mm | 164.94 mm (+11.3) | T2 |
| Nut body OD | 170.4 mm | 181.6 mm | A2 |
| Release margin | by capture, any mu_k | 20 > 19.29 degrees by 0.71 degrees; fails for mu_k > 0.364 | A3 |
| Angle needed for mu_k = 0.50 | n/a | 29.1 degrees, D_T about 176.5 mm | A3 |
| Axial force per N m of nut torque (plain bearing) | 21.7 N | 20.2 N | T7 |
| Holding per unit axial force, 1/(tan alpha + mu_k) | 1.900 | 1.400 (-26 percent) | T7 |
| T_hold at 12 N m nut, plain bearing, d = 105 / 90 | 10.4 / 8.9 N m | 7.1 / 6.1 N m | T7 |
| T_hold at 12 N m nut, PTFE thrust washer, d = 105 / 90 | 15.1 / 12.9 N m | 10.4 / 8.9 N m | T7 |
| Nut torque needed for 10 N m hold at d = 90, plain / PTFE | 13.5 / 9.3 N m | 19.6 / 13.5 N m | T7 |

Ruling: retire the releasing cone as a fallback. With a hand limit of 12 N m it cannot reach 10 N m at d = 90 even with a PTFE washer (8.9 N m), and it needs a 165 mm thread. Keep `cone.alpha_release` as a reference value only, not as a build branch. If the Step 8 coupon rejects the captured collar, the response is a mechanical change to the collar (section 2.7), not a steeper cone. A3's "release by cone angle above atan(mu_max) or captured flange" resolves to the captured-flange branch.

## 2. Seat, register and radial chain

### 2.1 Radial chain, governing equation

D_T = B_f(d_max) + 2 t_c + 2 H tan(alpha) + 2 (c_s + t_h + g_reg + t_b + h)

| Step (outside in from the core) | Formula | alpha = 10 | alpha = 20 | Status |
|---|---|---|---|---|
| B_f(105) | d + tau + c_i | 107.00 | 107.00 | DERIVED |
| D_S, collet small-end OD | B_f + 2 t_c, t_c = 5 | 117.00 | 117.00 | DERIVED |
| D_L, collet large-end OD (cone base) | D_S + 2 H tan(alpha), H = 30 | 127.58 | 138.84 | DERIVED |
| Holder OD | D_L + 2 c_s + 2 t_h, c_s = 0.30, t_h = 5 | 138.18 | 149.44 | DERIVED |
| Receiver bore (register diameter) | holder OD + 2 g_reg, g_reg = 0.25 | 138.68 | 149.94 | DERIVED |
| Thread minor (boss root) | bore + 2 t_b, t_b = 5 | 148.68 | 159.94 | DERIVED |
| Thread major D_T | minor + 2 h, h = 2.5 | 153.68 | 164.94 | DERIVED |

The 165 mm seed closes only for the 20 degree fallback (164.94, rounds up to 165). With the primary cone the major is 153.68 mm. Replace `thread.major` = 165 by 153.68 (DERIVED). The family and the largest collet share one major: the cone, holder and receiver are common (C4), so d = 90 and d = 105 give the same D_T. The only d-dependent radial quantity is collet wall: t_small(d) = (D_S - B_f)/2 = 12.5 mm at d = 90, 5.0 mm at d = 105; t_large(d) = (D_L - B_f)/2 = 17.79 mm at 90, 10.29 mm at 105. Test: P1 (major above the largest bore plus walls), T2.

`wingnut.body_od` = D_T + 2 (c_r + 8) = 170.4 mm (was 181, DERIVED). `wingnut.span` 230 mm stands (wing tip radius 115 mm).

### 2.2 Collet axial stack (new, closes the open "collet total length and ring height")

| Quantity | Formula | Value | Status | Test |
|---|---|---|---|---|
| Collet length L_c | h_w + h_s = 4 + 32 | 36.0 mm | DERIVED | C4, C7 |
| Cone height H | seed | 30.0 mm | ASSUMED | C4 |
| Foot ring height h_r | L_c - H | 6.0 mm, OD = D_L = 127.58 | DERIVED | C4 |
| Seat pocket in receiver floor, diameter | D_L + 2 c_s | 128.18 mm | DERIVED | F1 (R), A3 (foot on seat) |
| Seat pocket depth h_seat | seed, less than h_r | 4.0 mm (foot protrudes 2.0 mm above the floor) | ASSUMED | A3 |
| Cone base above floor | h_r - h_seat | 2.0 mm | DERIVED | F1 |
| Collet top above floor | L_c - h_seat | 32.0 mm | DERIVED | F4 chain |

### 2.3 Holder and receiver register

| Quantity | Formula | Value | Status | Test |
|---|---|---|---|---|
| Register clearance g_reg (radial, holder in receiver bore) | seed | 0.25 mm | ASSUMED (`fit.register_clearance`, new) | T9 |
| Critical tilt alpha_crit | P / (2 D_T), half a pitch of thread-start offset across the diameter | 8/(2 x 153.68) = 0.02603 rad = 1.49 degrees | DERIVED | T9 |
| Allowed register tilt | alpha_crit / 2 (safety factor 2) | 0.01301 rad = 0.746 degrees | DERIVED | T9 |
| Register length L_reg | 2 g_reg / (alpha_crit / 2) | 38.4 mm, set 40.0 mm | DERIVED | T9 |
| Tilt at L_reg = 40 | 2 g_reg / L_reg | 0.0125 rad = 0.716 degrees (passes by 0.03 degrees) | DERIVED | T9 |
| Holder body length below flange L_h | L_reg + g_stop = 40 + 13.13 | 54.0 mm (holder inserted 40.9 mm at the nominal pose) | DERIVED | A3, F6 |
| Receiver rim above floor | h_r - h_seat + L_h - m = 2 + 54 - 1.5 | 54.5 mm | DERIVED | F6, S6 |
| Flange: OD | = thread minor (passes nut tooth crests with c_r) | 148.68 mm | DERIVED | A1 (nut-flange G pair) |
| Flange thickness t_f | seed | 8.0 mm | ASSUMED | A3 |

Register verdict: the 54 mm figure is replaced by 40 mm. It comes from the stacked register (holder body in the receiver bore, flange face flat against the nut bearing face). It rests on g_reg = 0.25 mm; with the Step 0 value of 0.5 mm the length would be 77 mm. At 0.35 mm (the thread c_r) it is 54 mm, which is where the Topologist's number came from. The 0.25 mm fit is the sensitive assumption: if the coupon needs 0.35, L_reg becomes 54 mm and L_h becomes 68 mm.

### 2.4 Key, slot and slit phase

| Quantity | Value | Status | Test |
|---|---|---|---|
| Holder key: width x radial height x length | 8.0 x 3.0 x 40.0 mm, at angle phi_key = 0 (+X) | ASSUMED | A3, A6 (WS2), F5 |
| Receiver key slot: width x depth | 8.6 x 3.3 mm (0.3 mm per side and 0.3 deep); remaining wall at the thread root 5.0 - 3.3 = 1.7 mm, above `collet.min_wall` | ASSUMED | A1, C6 style check |
| Collet foot key: width x height x length | 6.0 x 3.0 x 6.0 mm, at phi_key; pocket slot 6.6 x 3.3 | ASSUMED | A6 (WS1, WS7), F5 |
| Slit phase | phi_k = phi_key + 180/N + 360 k/N: the key sits mid-web, never over a slit | DERIVED | C5, A6 (WS11) |

### 2.5 Receiver thread ends

| Quantity | Value | Status | Test |
|---|---|---|---|
| Lead-in chamfer (receiver top and nut mouth) | 45 degrees x 2.5 mm (= h) | ASSUMED | T4, T8 |
| Run-out land (cylinder at the minor diameter, receiver top and thread bottom) | 4.0 mm | ASSUMED | T1a, C7 style topology |
| Helix start | t0 = 0 on +X for boss and nut, thread length an integer number of turns | DECLARED (rule) | T1a, T1b |

### 2.6 Thread form, clearance and nut length

| Quantity | Formula | Value | Status | Test |
|---|---|---|---|---|
| Hand, starts | right-hand, single start (dz/dt > 0 for both parts) | DECLARED rule | T1a, T1c |
| Flank angle | 45 / 45 symmetric trapezoid, 90 degree included | 45 degrees | ASSUMED (`thread.flank_deg`) | T2, T8 |
| Pitch / lead P | PROPOSED 8 mm, confirmed here | 8.0 mm | ASSUMED | T2 |
| Tooth depth h, crest flat f | f = (P - 2h)/2 | 2.5 mm, 1.5 mm | ASSUMED | T2 |
| Sweep validity | f + 2h + 2 g_a < P | 6.5 + 0.6 = 7.1 < 8 (margin 0.9 mm) | DERIVED | T2, T3 |
| Radial crest clearance c_r | seed | 0.35 mm | ASSUMED (`fit.c_r`) | T3, E2 |
| Axial flank gap per side g_a | seed (Step 0 draft said 0.25, params.yaml says 0.30; params wins) | 0.30 mm | ASSUMED (`fit.g_a`) | T3 |
| Pitch diameter, radius r_p | D_T - h, half of it | 151.18 mm, 75.59 mm | DERIVED | T7 |
| Lead angle lambda | atan(P / (pi x 2 r_p)) | 0.965 degrees | DERIVED | T7 |
| Nut thread length L_n | ceil_to_pitch(min_engage + g_stop + t_f) = ceil(24 + 13.13 + 8 = 45.13) | 48.0 mm (6 turns); engaged 26.9 mm in R, 38.5 mm in K | DERIVED | T4, T5, A3 (stroke inequality) |
| Tessellation deflection | c_r / 10, angular 2 degrees | 0.035 mm | DERIVED | E2 |

Step 0's 40 mm nut omitted the flange thickness. At 40 mm the engaged length in R would be 18.9 mm, below the 24 mm minimum (T4 fires).

Load per flank at 10 N m of nut torque (plain bearing): axial force F = 10 / (0.02817 + 0.25 x 0.0717) = 217.5 N. Flank normal 1.414 F = 307.6 N total; per engaged turn (3 turns minimum) 72.5 N axial; pressure on the projected flank area (3 turns x pi x 151.2 x 2.15 mm = 3063 mm2) is 0.071 MPa; tooth-root shear (3 turns x pi x 148.7 x 6.5 mm) is 0.024 MPa; hoop component F tan 45 / (2 pi) = 34.6 N. Strength does not bound this thread; clearance, ovality and tessellation do. With a PTFE washer F = 314.9 N at 10 N m, still two orders below any layer-limit. DERIVED, T7.

### 2.7 Captured lift collar (primary release mechanism; not previously defined)

The nut pushes the holder down through its top plate. To lift on back-off, the holder carries a lift collar above the plate. Layout from the flange up: flange F1 (t_f = 8), nut top plate (t_p = 8 mm, thrust-washer recess in its underside), play p = 1.5 mm, lift collar F2 (t_k = 6 mm, OD 148.68 mm, a separate ring fixed to the holder top with four M6 screws; a one-piece collar cannot be assembled past the plate). Plate hole ID 140.2 mm (1.0 mm per side over the holder OD). Back-off lost motion p / P = 0.19 turn before the collar lifts.

| Quantity | Value | Status | Test |
|---|---|---|---|
| Play p | 1.5 mm | ASSUMED (`nut.lift_play`, new) | A3, H5 |
| Collar thickness t_k | 6.0 mm | ASSUMED (`holder.collar_t`, new) | A1 |
| Highest fixture above the nut top plate | p + t_k = 7.5 mm (wing tops are at or below the plate top plane) | DERIVED | F4, A2 (z_stop is collar top, not nut top) |
| Jacking holes | 2 x M6 through F1 at r = 71.84 mm (rim centreline), at phi_key +/- 90 degrees; they push on the receiver rim | ASSUMED | A3, H5 |
| Washer pocket (nut plate underside) | annulus 70.1 to 74.3 mm radius, depth 1.0 mm; mean bearing radius 71.7 mm | ASSUMED | A1 |

Flag for the Topologist and Engineer: F4 and A2 must measure from the collar top (nut top plate + 7.5 mm), which raises `core.min_exposed` by 7.5 mm to about 128.9 mm. This is a consequence of the capture, not a hidden margin.

### 2.8 Wing planform and tommy-bar socket (closes Designer items)

Two wings 180 degrees apart. Elliptical planform, centre rho_0 = 70 mm, semi-axes a = 45 mm radial, b = 18 mm vertical (36 mm high, top at the plate top plane); thickness 12 mm at root tapering to 8 mm at tip; root fillet 6 mm; tip radius 115 mm; hand arm 100 mm. Root bending (150 N abuse, 50 mm lever, 30 mm x 10 mm section): 15 MPa against `friction.tensile_in_layer` 45 MPa, factor 3. Tommy-bar socket: two radial holes, diameter 10 mm, 20 mm deep, at wing angle + 90 degrees, at mid-plate height. All ASSUMED; tests F5, A1.

## 3. Collet family

### 3.1 Law (in terms of existing keys)

| Quantity | Law | Value | Status | Test |
|---|---|---|---|---|
| Free bore | `core.diameters[i]` + `core.tol` + `collet.c_i` | d + 2.0 | DERIVED | C3 |
| Grip window | [d - window_below, d + `core.tol`], window_below = 1.5 | width 2.5 = `collets.spacing` | DERIVED | C8 |
| Closure | Delta = window_below + `core.tol` + `collet.c_i` | 3.5 mm | DERIVED | C9 |
| Slit count N | even N >= pi Delta h_w / (2 eps_allow h_s l_h) | 11.5, N = 12 (`collet.slit_count`) | DERIVED | C5 |
| Free slit width | w_s = pi Delta / N + `collet.min_slit_clamped`, rounded up to 0.5 | 0.916 + 0.5 = 1.416, set 1.5 mm (`collet.slit_width_seed`) | DERIVED | C5 |
| Web strain | eps = h_w (pi Delta / N) / (2 h_s l_h), h_w = 4, h_s = 32, l_h = 6 | 0.00954 against `collet.web_strain_allow` 0.010: ratio 0.954 | ASSUMED allowable | C9 |
| Slit width clamped at d - 1.5 / at d + 1.0 | w_s - pi (B_f - core)/N | 0.584 / 1.238 mm | DERIVED | C9, F1 (K) |
| Wall at the cone top | (D_S - B_f)/2 less the 1.5 mm x 45 degree bore lead-in | 5.0 mm at 105, 12.5 at 90; 3.5 mm and 11.0 mm after chamfer; all above `collet.min_wall` 1.2 | DERIVED | C6 |
| Seat clearance | `fit.seat_clearance`, same for every d | 0.30 mm radial | ASSUMED | F1 (R) |

Coverage and grip-window spacing, all seven:

| d | B_f | Window | t_small | t_large |
|---|---|---|---|---|
| 90.0 | 92.0 | 88.5 to 91.0 | 12.50 | 17.79 |
| 92.5 | 94.5 | 91.0 to 93.5 | 11.25 | 16.54 |
| 95.0 | 97.0 | 93.5 to 96.0 | 10.00 | 15.29 |
| 97.5 | 99.5 | 96.0 to 98.5 | 8.75 | 14.04 |
| 100.0 | 102.0 | 98.5 to 101.0 | 7.50 | 12.79 |
| 102.5 | 104.5 | 101.0 to 103.5 | 6.25 | 11.54 |
| 105.0 | 107.0 | 103.5 to 106.0 | 5.00 | 10.29 |

The windows abut with no gap from 88.5 to 106.0 mm. The label shows the window, not the nominal, because the window is asymmetric about d (centre at d - 0.25). The stop margin gives an extra 0.53 mm diametral of mechanical overshoot below each window (slit still open 0.44 mm there), so a core on a boundary seats in either neighbour.

Problem in C8 as written: "widen each core diameter by tol, then require one collet's range to contain it" cannot pass. A 2.0 mm wide core band does not fit in a 2.5 mm window except over a 0.5 mm slice of nominals. The tolerance is already in the window ends (the window top is d + tol). Replace the test: sweep a continuous measured diameter x from `core.diameters[0]` - 1.5 to `core.diameters[-1]` + 1.0 in 0.1 mm steps, no widening, require some window to contain x. Known-bad control (remove a mid collet) stands.

### 3.2 Upper-end throat check (P8, my input)
Largest accepted core d_max + tol = 106.0 mm; throat 108.585; slack 1.29 mm per side; `collets.envelope_max` 106.585 leaves 0.29 mm per side in the worst case (DERIVED, P8).

## 4. Holding estimate (T7 inputs)

### 4.1 Model

- Clamp force: F = T_nut / k, with k = r_p (tan lambda + mu') / (1 - mu' tan lambda) + mu_b r_bm, mu' = mu_t / cos 45 = 0.354, r_bm = 0.0717 m.
- Radial force on the core, exact for a cone: Sum N_r = F / (tan alpha + mu_k). Thin-ring transfer to the bore preserves the sum.
- T_hold = mu_c F r_core / (tan alpha + mu_k), r_core = d/2. Grip height cancels; it sets pressure, not torque.

### 4.2 Friction values (all ASSUMED, none measured)

| Symbol | Seed | Range used for the spread | Source |
|---|---|---|---|
| mu_k (cone) | 0.35 | 0.25 to 0.50 | `friction.mu_k` |
| mu_c (core, concrete on printed plastic) | 0.40 | 0.30 to 0.50 | `friction.mu_c` |
| mu_t (thread) | 0.25 | 0.15 to 0.35 | `friction.mu_t` |
| mu_b (bearing, plain / PTFE washer) | 0.25 / 0.05 | 0.15 to 0.35 / 0.05 | `friction.bearing` |
| Hand torque T_nut | 12 N m (two hands, 60 N each at 100 mm) | 8 to 15 N m | PROPOSED |

### 4.3 Results (alpha = 10, T_nut = 12 N m, seeds)

| | k (m/N) | F | T_hold d = 105 | T_hold d = 90 | vs 10 N m (105 / 90) |
|---|---|---|---|---|---|
| Plain bearing | 0.04609 | 260.3 N | 10.4 N m | 8.9 N m | +4 percent / -11 percent |
| PTFE thrust washer | 0.03175 | 377.9 N | 15.1 N m | 12.9 N m | +51 percent / +29 percent |

At T_nut = 10 N m: plain 8.7 / 7.4 N m; PTFE 12.6 / 10.8 N m. Nut torque needed for exactly 10 N m: plain 11.6 N m (d = 105) and 13.5 N m (d = 90); PTFE 8.0 and 9.3 N m. Axial force required: 250.6 N (105), 292.4 N (90).

Margin, plainly: with a plain bearing the design misses 10 N m at d = 90 by 11 percent and clears it at d = 105 by 4 percent. With the PTFE washer (already in the Detail 2 item 4 response list) it clears both, by 29 and 51 percent. The spread from the unmeasured coefficients is a factor of about six (plain, d = 90: 3.7 to 22.5 N m; PTFE: 5.6 to 30.2 N m). This is a prediction, not proof: the sign of the margin is settled by H1, not by this table. There is no positive core lock and no escalation path; the levers in hand are the PTFE washer, wing length, the tommy-bar socket and a core liner. Status: DERIVED from ASSUMED inputs. Test: T7 (existence, labels, margin report), H1 (authority).

The worst d is 90, not 105: holding scales with core radius at fixed F. T7 must run both extremes (Detail 8 says so).

## 5. Tolerance-budget inputs (Detail 2 item 5; the stack numbers I own)

Datum rule: the core axis is located by the cone and the register, never by the thread.

| Item | Value | Status | Test |
|---|---|---|---|
| Thread lateral play | min(c_r, g_a / tan 45) = 0.30 mm per side | ASSUMED | T3 |
| Thread tilt (nut on receiver), 2 x 0.30 / engaged length | 1.24 degrees in R (26.9 mm engaged), 0.89 degrees in K (38.5 mm); acts on the flange bearing face only, not on the core axis | DERIVED | T4, T9 |
| Register tilt | 0.716 degrees, limit 0.746 degrees | DERIVED | T9 |
| Core axis offset at the holder plane | worst case g_reg + e_b/2 + e_cone = 0.25 + 0.10 + 0.10 = 0.45 mm; RSS 0.29 mm; budget `icd.coaxiality_budget` 1.0 mm | ASSUMED | A3 (coaxial), H3 |
| Collet bore print error e_b | +/- 0.20 mm diametral (generic process figure, not a printer input); unclamped bore never below d + 1.8, so a core of d + tol still clears by 0.8 mm | ASSUMED | C3, T5 |
| Cone surface radial error, each cone | +/- 0.10 mm (collet and holder) | ASSUMED | F1 |
| Cone half-angle error | +/- 0.5 degrees, gives +/- 0.51 mm stroke | ASSUMED | A3 |
| Stroke error from bore (0.10 radial), cones (0.14 RSS) and angle | 0.57, 0.80, 0.51 mm; RSS 1.11 mm, so m = 1.5 mm | DERIVED | F6 |
| Slit width non-uniformity | +/- 0.15 mm per slit; clamped residual 0.584 - 0.15 = 0.43 mm at worst, above zero but below the 0.5 design floor (nominal passes C9) | ASSUMED | C5, C9 |
| Slit angular position | +/- 0.5 degrees (about 0.5 mm at the bore) | ASSUMED | C5 |
| Free core tilt (unclamped) | 2.0/36 gives 3.18 degrees; 27.8 mm at 0.5 m, 41.7 mm at 0.75 m | DERIVED | H3 note; steady rest decision |
| Clamped core tilt | 2 x 0.15 radial misfit over 18.4 mm contact height: 0.93 degrees; 8.2 mm at 0.5 m, 12.2 mm at 0.75 m | ASSUMED | H3 |
| Throat slack at d_max + tol | 1.29 mm per side | DERIVED | P8 |

Core out-of-round and core diameter tolerance belong to the Systems Engineer's table.

## 6. New parameter keys

Needed, with seed values. These close 16 of the Designer's 24 MISSING items.

| Key | Value | Status | Closes |
|---|---|---|---|
| `cone.alpha` | 10 stays; `cone.alpha_release` demoted to reference | ASSUMED | n/a |
| `collet.window_below` | 1.5 mm | ASSUMED | grip-window spacing |
| `collet.web_height` | 4.0 mm (h_w) | ASSUMED | relief geometry |
| `collet.slot_depth` | 32.0 mm (h_s) | ASSUMED | relief geometry |
| `collet.relief_diameter` | 6.0 mm (l_h), radial axis | ASSUMED | **slit relief holes** |
| `collet.length` | 36.0 mm | DERIVED | collet length |
| `collet.foot_height` | 6.0 mm | DERIVED | ring height |
| `collet.foot_key_width` / `foot_key_height` / `foot_key_length` | 6.0 / 3.0 / 6.0 mm | ASSUMED | **foot key** |
| `collet.bore_chamfer` | 1.5 mm x 45 degrees | ASSUMED | **lead-in chamfer** |
| `collet.core_stop_width` / `core_stop_height` | 3.0 / 4.0 mm ledge at the foot | ASSUMED | **core stop** |
| `chain.c_s` | = `fit.seat_clearance` (0.30) | ASSUMED | chain |
| `fit.register_clearance` | 0.25 mm | ASSUMED | **register** |
| `register.length` | 40.0 mm | DERIVED | **register** |
| `seat.pocket_depth` | 4.0 mm | ASSUMED | receiver floor seat |
| `holder.body_length` | 54.0 mm | DERIVED | holder |
| `holder.flange_od` / `flange_t` | 148.68 / 8.0 mm | DERIVED / ASSUMED | **flange** |
| `holder.key_width` / `key_height` / `key_length` | 8.0 / 3.0 / 40.0 mm | ASSUMED | **holder key** |
| `receiver.key_slot_width` / `key_slot_depth` | 8.6 / 3.3 mm | ASSUMED | **key slot** |
| `receiver.rim_above_floor` | 54.5 mm | DERIVED | receiver |
| `receiver.thread_leadin` / `thread_land` | 2.5 mm x 45 degrees / 4.0 mm | ASSUMED | **thread lead-in and land** |
| `holder.jack_hole_thread` / `jack_hole_radius` | M6 / 71.84 mm (x 2) | ASSUMED | **jacking holes** |
| `holder.collar_t` / `collar_od` / `nut.lift_play` | 6.0 / 148.68 / 1.5 mm | ASSUMED | captured collar, **hard-stop face** gap |
| `nut.plate_t` / `plate_hole_id` | 8.0 / 140.2 mm | ASSUMED | **bearing face** |
| `nut.washer_pocket_r_in` / `r_out` / `depth` | 70.1 / 74.3 / 1.0 mm | ASSUMED | **bearing recess** |
| `nut.thread_length` | 48.0 mm | DERIVED | nut |
| `nut.wing_count` / `wing_a` / `wing_b` / `wing_rho0` / `wing_t_root` / `wing_t_tip` / `wing_fillet` | 2 / 45 / 18 / 70 / 12 / 8 / 6 mm | ASSUMED | **wing planform** |
| `nut.tommy_diameter` / `tommy_depth` | 10 / 20 mm | ASSUMED | **tommy-bar socket** |

Changed existing keys: `thread.major` 165 to 153.68 (DERIVED); `wingnut.body_od` 181 to 170.4; `stop.hard_stop_gap` 6 to 13.13; `stop.margin` is F4's margin and is separate from the stroke margin m = 1.5 (new key `stop.stroke_margin`); `core.min_exposed` 121.369 to about 128.9 once F4 measures from the collar top; `fit.g_a` 0.30 stands.

Closed in bold: receiver lead-in and land, register, key slot, holder flange, bearing recess, holder key, jacking holes, hard-stop face, relief holes, foot key, core stop, lead-in chamfer, wing nut bearing face, wings and planform, tommy-bar socket, plus the family window (16 with the grip-window spacing). Not mine and still open: rim notches, label text, colour, tighten arrows, dust skirt, base plate, tray, drain, slotted holes, feet, caddy, alignment gauge, cradle, witness scale (the witness mark is derivable: flange-to-rim gap runs 13.13 mm free to 1.5 mm at full closure).

## 7. Questions for the Topologist

Predicates are cited by the IDs visible in the plan (A3 text covers S1 to S16; S6, S12, S16, S22, S23 are named elsewhere). The Topologist's own table, with S17 to S21, was outside my inputs; I map those by content.

| ID | Question |
|---|---|
| S1 to S5 (coaxial, boss rises, foot on seat, collet inside holder, cone narrows with z) | Do these numbers satisfy them: half-angle 10.000 degrees on both cones within 0.02 degrees; foot pocket 128.18 mm against D_L 127.58 mm. Note the register permits 0.716 degrees of real tilt, so the A3 coaxial test (norm(a x Z) <= 1e-4) holds only for the nominal pose; say how it treats the tilted pose. |
| S6 | Holder never bottoms: the nominal pose has 13.13 mm gap, K has 1.5 mm at core d - 1.5 and up to 10.3 mm at core d + 1.0. Is a floor-contact check against the holder bottom needed (holder bottom 2.0 mm above floor at K)? |
| S7 to S11 (gap R, contact K, core in bore, core on stop and off tray, nut bears on flange) | Is the nut-flange antiparallel normal rule satisfied by a thrust-washer recess (pocket annulus 70.1 to 74.3 mm), or does the washer become a separate part with its own pair class? |
| S12 | One pitch of nut travel left: the receiver thread run must be at least engaged length at K (38.5 mm) plus 8 mm below the nut skirt; confirm that requirement and that the nut cannot bottom on the base (WS9). |
| S13, S14 | Engagement per T4 (26.9 mm R, 38.5 mm K) and exposure per F4 (collar top, not nut top): agree? |
| S15 | Stroke inequality: s_z = Delta/(2 tan alpha) = 9.925 mm; thread length 48 >= s + 24 + 8 = 41.9. Confirm sign and form. |
| S16 | Release: cone-angle branch is retired; confirm that S16 resolves to the captured-collar branch and name the contact pair (plate top face against collar underside, p = 1.5 mm). |
| S17 to S21 (by content: key and slot phase, slit-over-key, relief topology, foot-key to pocket-slot, flange OD against the receiver bore) | Slit phase phi_key + 180/N + 360 k/N (key mid-web); the key 8.0 wide against webs about 30 mm wide at the bore: confirm no slit overlap in any of 7 collets. |
| S22, S23 | Alternating slits, N = 12 (6 from each end), relief holes Ø6 on a radial axis at depth 29 mm to 32 mm: genus, face and edge counts, one component. Holes of adjacent slits are about 28 mm apart at the bore. |
| Register length | Confirm 40.0 mm (T9 control: tilt 2 x alpha_crit must fire the register before the thread). Does the register see the holder key slot as a break in the cylinder? |
| Clamped-state coincident cone faces (F1 K) | Clamped solid: bore = core, outer cone reduced by (B_f - d_c)/2, placed at holder-relative offset s_z, contact height 18.37 mm only (L-4), so the holder cone extends 11.63 mm below the collet cone base and the collet cone extends 11.63 mm above the holder cone top. Which faces coincide, and does the 1e-3 mm radial offset leave a sliver where the holder cone passes below the cone base onto the D_L cylinder? |
| Capture assembly path | Lift collar as a separate bolted ring: confirm it is manifold as a separate solid and that the nut plate hole (140.2 mm) clears the holder OD (138.18 mm) in every pose. |
| A6, WS5, WS11 | Cross-thread control tilts by 2 x alpha_crit = 2.98 degrees; slit-over-key control rotates the collet by 15 degrees. Are these the intended planted states? |
| E2, T1d, X1 | Tessellation c_r / 10 = 0.035 mm on a 153.7 mm helicoid: chord error 0.02 mm needs about 140 segments per turn; does the STL checker see it? |
