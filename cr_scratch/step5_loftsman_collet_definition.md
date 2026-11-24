## Corrections to the brief

1. Green count: `collet_family` collects 61 green_at_5 tests, not 62 (8 per-d groups x 7 = 56, plus C4, C9b, F3, 2 x C10b). Total 61 + 7 + 7 = 75, not 76. MEASURED (collect-only).
2. `parts_cache` holds 6 `.FCBak` files at B5 (footring, frame_profiles, holder, nut, receiver, washer). Criterion 8 fails before any build. MEASURED.
3. `collet.rim_notch_count` formula returns -1 at d 85 and 8 at 106.585. Rule: idx = clamp(floor((d - 90)/2.5 + 0.5) + 1, 1, `collets.count`); colour index = idx. 97.0 gives 4, 93.7 gives 2. DERIVED.
4. The 0.5 chamfer-edge clearance holds. The bore lip R 1.0 starts 0.414 below the edge, so lip-to-hole-edge clearance is 0.086 at c 10.5 (d <= 91.6) and at c 2.5 (d > 105.6); the hole crosses the lip edge at about 12 degrees. DERIVED.

## Identical for every d (basis in brackets)

- Height 32.0 [A] = `slit_length` 25 + `slit_ligament` 3 + hole radius 4.
- Ring: r_fo 66.99 [R], z 0 to 1.995. Key: az 37, r 65.99 to 70.04, width 11.75 [T], z 0 to 1.995, fused.
- Outer cone [R]: r(z) = 63.79 - (z - 2.0) tan 10; 63.791 at z 1.995, 58.500 at z 32; D(z5) 126.52, D(z20) 121.23 [D].
- Slits: az 52 + 30k; even k top-open (tool z 7 to 33), odd k bottom-open (tool z -1 to 25); width 1.5 [T, mid-wall]; tool r 38 to 72. Overlap z 7 to 25 = 18.
- Relief holes: r 4.0, axis radial at the slit az, centre z 7 (top-open) or 25 (bottom-open); edges z 3, 11, 21, 29 (ledge top 2.5 clears 3 by 0.5).
- Notches: width 6 [T], floor z 29.0, tool z 29 to 33. Azimuths 97, 127, 157, 217, 247, 277, 337 (key +60, 90, 120, 180, 210, 240, 300); size idx cuts the first idx. Each lies 15 degrees from the nearest slit and hole (about 8 degrees clear).
- Label window (Pass 1, flat recess, text string in JSON): az 7, z 12 to 20 (clears hole edges 11, 21 by 1.0), chord 24 [T], depth 0.8 normal. Tool = conical band from r_out(z) - 0.8/cos10 to r_out(z) + `collet.tool_overshoot`, intersect box, sides offset +-12. Hole and notch tools span r 38 to 72 (hole axis radial, length 34); notch tool z 29 to 33. [Topologist cross-review edits, applied by the orchestrator at Step 5]
- Probe azimuths 67, 187, 307 carry no notch, label or slit.

## Varies with d

r_b [R] = (d + `core.tol` + `collet.c_i`)/2. Ledge ID [D] = 2(r_b - 3), top z 2.5. Wall [R] at z 32 = 58.500 - r_b. c = min(wall - 1.2, 10.5), c = 2.5 where wall - 1.2 lies in (2.5, 3.5); edge z = 32 - c; chamfer is 45 degrees, c axial equals c radial. Lip R 1.0 tangent length 0.414. Label string: f"{d:.1f} | {d-1.5:.1f}-{d+1.0:.1f}", e.g. 92.5 | 91.0-93.5.

| d | r_b | c | edge z | top face [R] | lip-to-hole | notches | colour |
|---|---|---|---|---|---|---|---|
| 85.0 | 43.500 | 10.5 | 21.50 | 4.50 | 0.086 | 1 | red |
| 90.0 | 46.000 | 10.5 | 21.50 | 2.00 | 0.086 | 1 | red |
| 92.5 | 47.250 | 10.05 | 21.95 | 1.20 | 0.536 | 2 | orange |
| 93.7 | 47.850 | 9.45 | 22.55 | 1.20 | 1.136 | 2 | orange |
| 95.0 | 48.500 | 8.80 | 23.20 | 1.20 | 1.786 | 3 | yellow |
| 97.0 | 49.500 | 7.80 | 24.20 | 1.20 | 2.786 | 4 | green |
| 97.5 | 49.750 | 7.55 | 24.45 | 1.20 | 3.036 | 4 | green |
| 100.0 | 51.000 | 6.30 | 25.70 | 1.20 | 3.714 | 5 | blue |
| 102.5 | 52.250 | 5.05 | 26.95 | 1.20 | 2.464 | 6 | violet |
| 105.0 | 53.500 | 3.80 | 28.20 | 1.20 | 1.214 | 7 | white |
| 106.585 | 54.292 | 2.50 | 29.50 | 1.71 | 0.086 | 7 | white |

Probe wall at z 31.95 is 1.259 (d 92.5 to 105). Lip sits at the chamfer-to-bore junction; a round on the top-face edge gives wall 1.107 at that sample and fails C6. Fallback if withheld: cap 10.0 and a 2.0 branch (clearance 0.586).

Caddy record: socket D = 2 x 66.99 + 2 x `caddy.socket_clear` = 139.98; depth 40 against height 32 (margin 8.0).

## Construction and boolean order

1. One revolve sketch: ledge, bore, lip arc (threePoints (r_b, z_e - 0.414), (r_b + 0.076, z_e - 0.032), (r_b + 0.293, z_e + 0.293)), chamfer, top face, cone, ring. Chamfer and lip need no boolean; their volumes come from Pappus on the profile.
2. Fuse the key. 3. Cut slit tools as one compound. 4. Cut the 12 holes. 5. Cut notches. 6. Cut label. Expected_mm3 per cut: integral of local thickness t(z) over the removed region.
7. No tool face lies in a plane through the axis, so `slit_plane_faces` is 0 by construction (slit walls at +-0.75, notch +-3, label +-12). One lateral face per hole gives `relief_holes` 12.

## Clamped solids (same builder, three calls)

Pose Kd1: core d + `grip_window_hi`, closure Delta = tol + c_i - hi = 1.0 [D]. Kmax: core d + `grip_window_lo`, Delta 3.5. s = Delta/2 = 0.5, 1.75 [R].
- Cone line moves inward s + g/cos10 (g = `fit.model_contact_gap` 0.005; 0.00508 radial). Bore, lip, chamfer, ledge move inward s - g, so bore = core radius + 0.005. Ring r_fo and key unchanged.
- Slit width w = 1.5 - pi x Delta/12: 1.238 (Kd1), 0.584 (Kmax). Holes, notches, label unchanged.
- Holder bottom z: Kd1 9.089, Kmax 2.0. Cone gap = -1.75 + s + (z_hb - 2.0) tan10 = 0.000 in both, so the surfaces coincide except the 0.005 model gap; common volume 0 with gap 0.005 far above OCC tolerance.
- F1 area: A = pi (D(z5) + D(z20))/2 x `chain.H` / cos10 x f = 11 855 mm2 at f = 1 (|gap| < 0.01 holds at 0.00508); floor 200.

## Test-versus-geometry conflicts

- C4 symdiff: sizes differ only in (a) r < r_b(d), z 0 to 32 (bore, ledge); (b) chamfer and lip, always inside r < r_out(z) - 1.2 with r_out(z) = 63.79 - (z - 2) tan10; (c) notch boxes, z >= 29, chord +-3 at the seven azimuths; (d) label box (identical at Pass 1). Test region: r >= r_out(z) - 1.2, 0 <= z <= 32, minus the notch and label boxes. Known-bad: one size with a different slit width.
- F2: `base_gap` = distToShape - 5.0, but the nearest approach is the 1.0 radial bore clearance, so base_gap is -4.0 for all d against a 0.05 limit. Fix: gap = z_ledge - `collet.core_seat_height`.
- C2 volume band: analytic omits chamfer, ledge, key, notches. Deviation -6.5% (85), -7.9% (90), -7.9% (92.5), -6.2% (95): outside +-5%. Add the profile terms.
- C7: notches change V, E, F but not V - E + F (genus 1); no conflict.

## Witness scale

`witness.*` belongs to the receiver rim (scale) and holder flange (tick), per gameplan line 153. The collet carries none; routed to Step 6.

## New params keys (4; leaves 327 to 331)

| Key | Value | Unit | Basis | Status |
|---|---|---|---|---|
| `collet.notch_azimuth_offsets_deg` | [60, 90, 120, 180, 210, 240, 300] | deg | from `receiver.key_offset_deg`; first idx used | ASSUMED |
| `collet.label_azimuth_offset_deg` | -30 | deg | sector centre, off probe azimuths | ASSUMED |
| `collet.label_window_width` | 24 | mm | chord [T]; 3 mm margin to slit edges | ASSUMED |
| `collet.tool_overshoot` | 1.0 | mm | tool extent beyond a face; no part dimension | ASSUMED |

Text edit, no new leaf: `collet.rim_notch_count` becomes the clamped, half-up formula (correction 3).

## Self-check (python)

Min probe wall 1.259; edge clearance 0.5; R gap 0.2999; Kd1 gap 0.0000; label residual wall >= 6.9; ledge ID at d 85 is 81.0 against floor hole 80.0.
