## Result-JSON contract: parts_cache/collet_<tag>_result.json (C2, C10b, F5, C11 to C14)

- Top: part, d, volume_mm3, isValid, isClosed, solid_count, run_seconds.
- cuts: list of {name, before_mm3, after_mm3, tool_mm3, expected_mm3}. Names contain "slit", "relief" (C2 requires both), also "rim notch" and "label". expected_mm3 is the integral of local wall thickness t(z); tests compare slit and relief expected_mm3 to an independent integral within 5 percent, and removed volume within 3 percent of expected_mm3.
- features: list of {feature, pass, volume_mm3 > 0}. Feature names contain: slit, relief hole, foot key, foot ring, core seat, rim notch, label, chamfer, bore lip. Extra fields: chamfer {c_mm, edge_z}; bore lip {radius}.
- notch_count (int, equals family index), colour (string, collet.colour[index - 1]), label_text (format "92.5 | 91.0-93.5").
- clamped: {Kd1: {slit_width}, Kmax: {slit_width}}, widths 1.238 and 0.584 within 0.01.
- caddy: {socket_d, socket_depth, height, margin}; socket_d = 2 x 66.99 + 2 x caddy.socket_clear = 139.98, margin = 8.0.
- Probe side: collet_family.json carries symdiff_region_mm3, symdiff_zero_control_mm3, symdiff_known_bad_mm3.

## C4 (revised)

The Loftsman's region statement leaves the conflict in place (bore, chamfer, notch and label differ between sizes), so the check now runs in the region r >= r_out(z) - 1.2, z 0 to 32, minus the seven notch boxes and the label box. Predicate: `cad_helpers.collet_c4_region`; probe: `region_mask` in probe_collet.py. Zero control: a size against itself reads 0. Known-bad: one slit widened 0.5 mm reads above 1 mm3. Pure control `test_C4_control_region_...` covers bore, chamfer, notch, label (excluded) and slit edge (included).

## F2 (revised)

Probe `base_gap` is now ledge top z minus `collet.core_seat_height`. Control `test_F2_control_base_gap_...`: 0 passes, ledge 0.5 high fails, the old -4.0 reading fails.

## C2 (revised)

Reference term is `cad_helpers.collet_expected_volume(d)`: revolve profile with ledge, chamfer and cone by integration, plus key beyond the ring, minus slits, relief holes (net of slit overlap), notches, label, lip. Band stays 0.95 to 1.05. Chamfer term is 16 279 mm3 at d 85 and 17 145 at d 90, which accounts for the -6 to -8 percent deviation. Added: generator expected_mm3 for slit and relief cuts is checked against the independent integral. Control `test_C2_control_...`.

## Gaps (pushback, one line each)

- Chamfer rule per d: C11 reads c_mm and edge_z for 7 sizes; the 2.5 branch (d > 105.6) is outside the family, so it is covered by arithmetic in the rule test (106.585 gives 2.5). Worth it.
- Notch count, colour index, label text: C12, one test per d. Worth it (the params formula returned -1 at 85).
- Caddy record: C13, one test. Marginal, kept because the Detail 5 outputs name it.
- Clamped slit width: C14 per d, values 1.238 and 0.584. Worth it.
- Refusal path: C15 calls `build_collet` above the cap, expects "exceeds envelope cap" and no file. C10a tests only the predicate, so this adds the wiring. Worth it.
- Not added: per-notch azimuth test and label geometry test; C12 and F5 catch a missing feature and the volume cuts catch a wrong one. Ceremony.

## F3, F1, A3a, C9b against the definition

No mismatch. F3 accept range d - 1.5 to d + 1.0 matches bore d + 2 and Delta 3.5. F1 R gap 0.30 matches 0.2999; Kd1/Kmax common volume 0 against 0.01; contact floor 200 against 11 855 x f. A3a 10.0 degrees matches. C9b floor 1.366 against width 1.5; wall 1.259 (C6) clears 1.2. Params gap: `collet.notch_azimuth_offsets_deg` and `collet.label_azimuth_offset_deg` are in `PARAM_GAPS` with Loftsman values until the Manager adds them. Note: params `collet.rim_notch_count` text still needs the clamped half-up formula (correction 3).

## Counts

Collected 540 (was 513). test_params_bom.py: 213 passed. green_at_5: 84 in test_collet_family.py, 98 in total.

## Added and revised tests

- C4 test_C4_family_invariants, discriminator, green_at 5, revised: Loftsman region.
- C4 test_C4_control_region_..., invariant, 4, added: zero and known-bad control.
- F2 test_F2_core_in_collet, discriminator, 5, revised: base_gap measure.
- F2 test_F2_control_base_gap_..., invariant, 4, added.
- C2 test_C2_volume_whole_part_and_per_cut, discriminator, 5, revised: reference term and cut cross-check.
- C2 test_C2_control_reference_term_..., invariant, 4, added.
- Rule arithmetic test, invariant, 4, added: table, old formula known-bad.
- C11 (7), C12 (7), C13 (1), C14 (7), C15 (1), discriminator, 5, added.
