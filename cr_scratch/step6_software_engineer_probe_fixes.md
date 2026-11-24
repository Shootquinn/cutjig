## Result

green_at_6: 41 of 41 pass (was 26 of 33). green_at_4/5/6 together: 408 pass, 0 fail. Full suite: 591 collected, 415 pass, 176 fail; every failure is green_at 7 or later (assembly, exports, thread_clamp: MISSING).

## Probe fixes (measurement positions, not weakened predicates)

| Test | Old position | New position | Known-bad control |
|---|---|---|---|
| HD5 | annulus scan z over the full holder height crossed the key at az 33/36/39 | scan window starts at holder bottom + holder.key_length + 1 (above the key top); all 120 azimuths still scanned | holder with a 4 mm jacking hole at r 66.8 az 100 run through the same probe: scan reads a non-1 count, `flange_errors` fires |
| HD6 | flange interval read at r 66.77 (inside tube wall, reads 0 to 104.75) | read at r1 + 1.0 = 69.54 (flange annulus, 88 to 96) | holder fused with a 3 mm shoulder disc at bottom + 30: extra downward face at z 30, `stop_face_errors` fires |
| RC6/HD7 | rim radius thread.major/2 - 1 (lead-in chamfer, rim reads 88.25) | thread.minor/2 - 1 (flat rim 88.5) | existing off-by-one-mm tick and scale-reference controls |
| NT4/NT5 | glyph window from wingnut.body_od/2 + 3 (inside dust skirt) and median column level | window from nut.skirt_r_out + 0.5 to wingnut.span/2 - 6 (tip fillet start); unrecessed face level (column extreme), same as nut.py `measure_glyph` | nut with both glyph windows filled by slabs: no glyph, `glyph_errors` fires; wrong-sense control kept |

## Fix-pass rulings applied

1. `LOFTSMAN_KEYS`: tray.ramp_x replaced by fall_x; added tray.cross_fall_deg, drain_spot_r, witness.index_face_nut_z, nut.release_* (3), plug.lug_* (4), rest.pose_core_d, roller_r_range, core_d_range, slot_clear, slot_depth.
2. `test_params_bom.py` P15 pin tray.floor_slope_deg 3 to 2.0.
3. New `tests/probes/probe_witness_sight.py` (17 s): horizontal rays at az 127, r 200 to axis, z 44 to 64 step 0.05, nut at rim_top - nut.skirt_below_flange + gap. Edge 50.00 (want 50.00) at K-max with lines k0, k1 = 2; edge 57.10 (want 57.09) at K d+1 with k0 to k8 = 9. Matches the Loftsman. Control: nut at edge - 5 reads edge 45.0 and fires. Tests: `test_witness_ray_cast_edge_and_visible_line_count` (2 params), `test_control_witness_nut_five_mm_low_fails_the_ray_cast`. The receiver slab boolean returns empty on the threaded solid, so rays run on the full shapes.
4. NT4/NT5 span tolerance 1.0 to 1.5 against nut.glyph_length 10 (measured 9.04). New `test_NT8_release_arrow_recess_area_equals_NT4_within_10_percent` (34.37 vs 35.41, ratio 0.97) plus a detector control.
5. New rest D2 test on `step6_parts` probe: `rest.shape_at` at 9 sizes (88.5, 90 to 105 step 2.5, 106): 1 solid, valid, common volume with the Ø d core cylinder at most OVERLAP_TOL, ring material starts at ring_z_lo + slot_depth beside the pin (slot cut). Control: overlap 895 mm3 and a plain ring both fail the predicate.

## Runs

`probe_step6_parts` 26.8 s, `probe_witness_sight` 17.3 s, `probe_step6_marks` 3,346.8 s (PID started after the stale run 1908 was killed); logs `cr_scratch\step6_se_probe_*.log`. The earlier marks run (old nut) was stopped. Files edited: `tests\test_step6_parts.py`, `tests\test_params_bom.py`, `tests\probes\probe_step6_parts.py`, `tests\probes\probe_step6_marks.py`, new `tests\probes\probe_witness_sight.py`. `cad_helpers.py` unchanged.
