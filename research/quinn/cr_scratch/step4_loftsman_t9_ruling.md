## Corrections to the brief

1. 1.021 deg is the T9 pass line (alpha_crit 1.532 / 1.5, DERIVED), not a register contact angle. The register contact angle is the register stop, 0.596 deg (MEASURED); 0.924 deg (DERIVED, params) is register plus plate rock.
2. The probe's "first thread contact" pose is the nut seated less than one turn on the receiver start (nut z_min 84.9 mm, receiver z_max 92.1 mm, overlap box z 84.3 to 92.1 mm, y 0 to 75 mm; MEASURED). It is the thread-start pose. The nut rests on one flank set. It is not a nut in full mesh.
3. 0.117 deg (DERIVED) is g_a/(2 r_p) = 0.15 / 73.54 rad, which is rotation about the nut centre. The probe pivot is at the holder bottom (x -67.04, z 40.5 mm). Rotation about that pivot moves the thread zone 0.15 mm toward the resting flank at about 0.12 deg, near 0.117 by coincidence.
4. The fix-pass "wall pose" values (86.0 mm3 at 0.924 deg) carry a 0.19 to 2.87 mm3 baseline from the anti-rotation key (common solid at x 49.9 to 52.2, y 45.1 to 46.8 mm; MEASURED). The -g_reg shift along X pushes the key into its slot side.

## 1. Reconciliation

### 0.903 (Step 2) against 0.117 (measured)

- 0.903 deg (DERIVED, Step 2 section 3) = 0.588 hanging register + 0.315 plate rock. This is the misalignment envelope of the nut relative to the receiver at the instant of first thread contact. Step 2 compared it with alpha_crit = P/(2 D_T) = 1.532 deg (DERIVED). It is an angle bound for cross-thread registration. It makes no claim that the flanks stay apart.
- Onset of 0.10 to 0.15 deg (MEASURED) comes from the probe pivot. A rigid rotation a about the holder-bottom point (-67.04, 0, 40.5) equals a rotation about the nut axis plus a whole-nut axial drop of 67.04 sin a. The drop closes the per-flank axial gap g_a/2 = 0.15 mm (DECLARED fit seed) on the flank the nut rests on. Diagnostic runs on the same shapes (MEASURED):

| pose | common mm3 | min distance mm |
|---|---|---|
| axial drop 0.10 | 0 | 0.035 |
| axial drop 0.15 | 0 | 0.000 |
| axial drop 0.20 | 0.1155 | 0 |
| tilt about nut centre (z 78.5) 0.10 / 0.15 / 0.20 deg | 0 / 0 / 0 | 0.0970 / 0.0925 / 0.0880 |
| tilt about holder-bottom pivot 0.15 / 0.30 deg | 0.0534 / 1.628 | 0 |

Tilt about the nut's own centre is clear through 0.20 deg; the measured interference is the pivot's axial drop.
- Is a rigid tilt with overlap volume a physical model of thread start? No. A nut that meets a flank is stopped by it: the contact force makes the nut ride the flank, and the plate rocks inside p = 0.75 mm (ASSUMED). Overlap volume measures how far the imposed pose is from a feasible one. It does not show whether a ridge lands in the wrong groove.
- The old criterion is also inverted. Zero overlap at alpha_reg needs g_a >= about D tan(alpha_reg) = 2.4 mm (DERIVED, Engineer). That is an axial slop of 0.6 x P/2 (DERIVED), which lowers cross-thread resistance. A sloppy thread passes the old criterion and a sound thread fails it.

### 0.35 (measured) against 1.021 / 0.924

- The fix-pass holder sweep pivoted at x = -(R - g_reg) = -67.04 mm, the face of a centred holder 0.25 mm (DECLARED g_reg seed) off the wall. Rotating about that point closes one side gap only, g_reg / L ≈ 0.25 / 47 rad ≈ 0.30 deg (DERIVED). Measured: 7e-8 mm3 at 0.30 deg, 5.14 mm3 at 0.35 deg (MEASURED).
- In the correct pose the holder bottom sits on the -X wall and its +X generator meets the bore edge at the chamfer bottom. That pose uses the diametral clearance 2 g_reg. Edge contact gives d + L sin a = Db cos a with d 134.08, Db 134.58, L 47.75 mm (DERIVED), so a = 0.591 deg (DERIVED). The new probe measures 0.596 deg (MEASURED, bisection to 0.001 deg at 0.01 mm3).
- The holder probe contains no plate rock (nut relative to holder): atan(0.75 / 136.44) = 0.315 deg (DERIVED from ASSUMED p).
- params register.t9_tilt_deg 0.924 (DERIVED) uses the corner formula d cos a + L sin a = Db (0.609 deg). The holder runs above the rim, so edge contact governs. 0.924 is a valid upper bound, 0.013 deg (DERIVED) above the measured total of 0.911.

## 2. Ruling

The existing criterion (rigid tilt at alpha_reg, overlap < 0.01 mm3) is withdrawn because it models an infeasible pose and does not discriminate cross-threading. T9 adopts the default candidate.

- Claim: alpha_total = measured register stop + plate rock. Then 1.5 x D tan(alpha_total) <= P/2, with D the measured receiver crest diameter and P the measured lead. The factor 1.5 (DECLARED) is the same pass line as register.tilt_limit_deg = alpha_crit / 1.5.
- Half-pitch across the full diameter is the governing onset. The first point down defines registration; the opposite side then sits D tan a away, so it lands in the wrong groove once that distance reaches P/2. This gives 1.532 deg (DERIVED). The Step 2 "true onset" of 3.064 deg (DERIVED) measures the spread about the mean and is not used.
- Known-bad controls, all measured on the model:
  - The superseded L_h 54 register (insertion 14.75 mm, DERIVED) stops at 1.826 deg (MEASURED; edge analytic 1.805, DERIVED). Total 2.141 deg gives 5.592 mm against 2.667 mm, so it fires.
  - 2 x alpha_crit = 3.064 deg gives 8.006 mm, a full pitch, so it fires.
  - The register blocks that tilt: holder/receiver common at 3.064 deg is 1949 mm3 (MEASURED).
- Zero controls: the wall pose is clear at 0 deg (0.0000 mm3, MEASURED). The criterion holds at 0 deg.
- Instrument controls on the thread-start pose:
  - Flank-normal gap 0.1061 mm (MEASURED) = g_a/2 cos 45.
  - Axial drop of 0.10 mm gives 0 mm3; a drop of 0.20 mm gives 0.1155 mm3 (MEASURED). The overlap instrument detects the resting flank at g_a/2.
- Booleans: holder against receiver only, valid throughout 0 to 5 deg; every sample agrees with V_receiver - V_cut (MEASURED). No helicoid-on-helicoid boolean above 0.2 mm of drop is used.

Result on the current design (MEASURED + DERIVED):
- Register 0.5963 + rock 0.3149 = 0.9113 deg.
- D tan = 149.58 x tan(0.9113 deg) = 2.379 mm, against P/2 = 4.000 mm (MEASURED). Factor 1.681 >= 1.5. Pass.
- The pass line holds while g_reg <= 0.299 mm (DERIVED, edge formula at a total of 1.021 deg). The Step 8 coupon checks g_reg against this.

The current geometry and fit pass. No fit change is needed for T9. g_a stays a T3 and coupon matter.

## 3. Edits made

- tests/probes/probe_tilt.py rewritten:
  - Holder hangs at insertion register_depth + lift_play = 48.75 mm (DERIVED), shifted -g_reg onto the -X wall and tilted about the bottom wall point.
  - The holder is cut to the slab |y| <= 20 mm, which leaves out the key. The key can only lower the stop, so the slab stop is the upper bound. Receiver-box common returns 0 under OCC 1.1 (MEASURED), so the receiver cannot be sliced.
  - Bisection to 0.001 deg; every sample cross-checked.
  - Also runs the short-register stop, the common at 2 x alpha_crit, the zero-tilt flank gap and the axial-drop instrument control.
  - The nut rigid-tilt sweep is removed.
  - Run time 12.5 s (MEASURED).
  - The fix-pass tilt.json is kept at C:\Users\QUINNM~1\AppData\Local\Temp\claude\6f0343b2791941ad\200377dc-f257-44be-a8a6-5a439d6cd6be\scratchpad\tilt_fixpass.json. The numbers are also in research/quinn/cr_scratch/step4_probe_tilt_stud.log.
- tests/test_thread_clamp.py, T9 block replaced, three tests:
  - test_T9_probe_is_self_consistent (invariant, green_at_4): sample validity, zero controls, measured stop within +0.03 deg of the analytic edge stop, flank gap, axial-drop control.
  - test_T9_control_short_register_and_double_critical_tilt_fire (invariant, green_at_4): zero control, short register fires, 2 x alpha_crit fires, register common at 2 x alpha_crit > 0.01 mm3.
  - test_T9_register_tilt_keeps_cross_thread_misregistration_under_half_pitch (invariant, green_at_4): the claim, plus total <= register.tilt_limit_deg and total <= register.t9_tilt_deg + 0.005.
  - The claim is an invariant at 4 because its inputs are Step 3 artifacts that exist at B4 and it passes (conftest definition). If the Step 8 coupon changes g_reg and the probe is rerun, the test re-evaluates.
- tests/cad_helpers.py: the tilt.json key list in the docstring is updated.
- pytest -k T9: 3 passed (MEASURED). Suite effect: the T9 ABSENT FEATURE failure becomes a pass, giving 255 passed and 258 failed of 513 (DERIVED from the fix-pass count).
- Not edited: gameplan.md, CLAUDE.md, ASSEMBLY.md, part geometry, params.yaml.

## 4. Replacement T9 row (gameplan.md line 339)

| T9 | Register and tilt (cross-thread) | At first thread contact (holder hanging at insertion register_depth + p), the measured register stop (holder on one bore wall at its bottom, generator on the opposite bore edge, holder/receiver common > 0.01 mm3, bisection to 0.001 deg) plus plate rock atan(p / 136.44) gives alpha_total. The axial misregistration across the thread, D tan(alpha_total) with D and P measured from the receiver thread, satisfies 1.5 x D tan(alpha_total) <= P/2 (same line as alpha_crit / 1.5 = 1.021 deg). Known-bad controls must fire: the superseded L_h 54 register (measured stop) and 2 x alpha_crit both exceed the line; at 2 x alpha_crit the holder/receiver common is > 0.01 mm3 (the register blocks the onset). Instrument controls: wall pose clear at zero tilt; nut axial drop of g_a/2 - 0.05 clear and g_a/2 + 0.05 interfering. Rigid-tilt nut/receiver overlap is not a T9 measure (it forces the nut through the flank it rests on). Step 4 measured: register 0.596 + rock 0.315 = 0.911 deg, misregistration 2.379 mm against 4.000, factor 1.68; holds for g_reg <= 0.299 mm; holder length 88.0, p = 0.75 |
