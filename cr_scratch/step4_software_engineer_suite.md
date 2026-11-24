## Inventory

Function count: 99 new test functions (35 assembly, 20 collet, 17 thread, 12 exports, 15 params) plus 71 existing; 510 collected cases, zero collection errors. Above 70 because the Manager's ID splits (A1b-e, A2a-h, A3a-i, A6a-c) and one control per numeric gate add 40. Modules: tests/test_params_bom.py, test_collet_family.py, test_thread_clamp.py, test_assembly.py, test_exports.py; helper tests/cad_helpers.py; probes tests/probes/{probe_lib,probe_thread,probe_thread_mesh,probe_tilt,probe_step3_parts,probe_collet,probe_poses,probe_exports}.py; markers and a label gate in conftest.py (a test without exactly one label and one green_at_N aborts collection).

| ID | Function(s) | Module | Label, green_at | Predicted B4 | SRC row, status | Threshold basis |
|---|---|---|---|---|---|---|
| P1-P21 | existing 197 | params | invariant, 4 | pass | as written | unchanged |
| P22 | 4 (scan, allowlist, planted, clean) | params | invariant, 4 | pass | Printer not a design input, DECLARED | word list in test only; one allowlisted line (kerf_standoff, row 106.369) |
| P23 | 3 (mutation, no soft-key bound, control) | params | invariant, 4 | pass | Core length capture goal, DECLARED | jig.height_target 3000, core.length_optional 1500 accepted |
| P24 | 3 | params | invariant, 4 | pass | all tags | tag parse, legal status, Register prefix and status, key= status and P7 row |
| P4, P6, P7 audits | T-nut PZRT, P6c, P6d, P6 split, params gaps declared | params | invariant, 4 | pass | 30-6060 DECLARED | P6d asserts the 0.5 m core only |
| C1 C2 C3 C5 C6 C7 | per d, 7 cases each | collet | discriminator, 5 | MISSING | C3 core.tol ASSUMED; C6 Printer DECLARED | C3 bore diametral 0.02; C5 width tangential at mid-wall 0.05, plane 0.01; C6 radial wall; C2 band 0.95-1.05, cuts 3 percent |
| C4 C9b C10b F2 F3 F5 | one each (C10b x2 sizes) | collet | discriminator, 5 | MISSING | none | C4 0.01 mm3 and 0.02 mm; C9b wall cubed ratio recorded |
| C8 (+control), C9a (+control), C10a, C3 control, predicate controls, C10b doc control | 8 | collet | invariant, 4 | pass | core.tol ASSUMED, Core range CONTRACT, Iris DECLARED, web strain ASSUMED | accept range from bore_free - c_i and s = grip window width; Delta = s + c_i |
| T1a, T1a control, T2, T3, T8 (+control), T2/T3 control | 7 | thread | invariant, 4 | pass (thread.json run) | Printer DECLARED (T3) | radii centre-line; g_a total at pitch line, g_a/2 per flank; flank 45 +/- 0.5 |
| T1b, T1c, T9, T9 control | 4 | thread | invariant, 4 | MISSING until thread_mesh and tilt probes run, then pass | none | common volume 0.01 mm3 |
| F4, T4 control | 2 | thread | invariant, 4 | pass | 106.369 VERIFIED | 143.119 arithmetic, ASSUMED label asserted |
| T7 | 1 | thread | discriminator, 8 | ABSENT FEATURE | Holding torque DECLARED | no holding_torque in params or common.py (grep) |
| F1 | per d | thread | discriminator, 5 | MISSING | none | R radial gap fit.seat_clearance +/- 0.05; K common < 0.01, contact > seat.min_contact_area |
| T4, T5 | per pose, d | thread | discriminator, 7 | MISSING | core.tol ASSUMED (T5) | engaged >= 3 x 8 = 24; T5 K means Kmax |
| A1 parser, control, A1a controls, A2 ring control, F5 five parts, F5 control | 6 | assembly | invariant, 4 | pass | none | 45 pairs, R C8/G12/F25, K C10/G10/F25; flip mismatch > 0.001 |
| A1a | pose x d, 21 cases | assembly | discriminator, 7 | MISSING | none | C: dist 0.01, patch > 0; G: >= g_min, contact 0; F: overlap < 0.01 |
| A3a | per d | assembly | discriminator, 5 | MISSING | Friction mu_k ASSUMED | cone 0.02 deg; alpha vs atan(mu_max) or capture pair |
| A3b-A3i, A4, A6, A6a-c, F6, P6b | 16 functions | assembly | discriminator, 7 | MISSING | 30-6060 DECLARED (P6b) | A3e 13.626 / 9.09 / 2.0 +/- 0.05; F6 ring gap Kmax +/- 0.01 |
| A1b-e, A2a-h | 12 | assembly | discriminator, 12 | MISSING | A2b cutter OD ASSUMED | A2b radial-free: gap >= stop.g_stop; keep-out icd.keepout_radius |
| E1, E2, T1d, B1, X1, X1 controls, E3 collets and assembly | 7 (E1, E2, E3 parametrized) | exports | discriminator, 10 | MISSING | Printer DECLARED (E2) | STEP 0.5 percent, STL 1 percent, tessellation c_r/10 and 2 deg, rebuild 1e-6 |
| E1 controls, E2 controls, T1d control, B1 control, E3 five parts | 5 | exports | invariant, 4 | pass | none | unit cube, removed triangle, mirrored helical ridge |

Predictions at B4 after the Engineer runs probe_thread, probe_step3_parts, probe_thread_mesh and probe_tilt: 248 pass today (4 invariants wait on the two heavy probes), 262 fail, of which 259 MISSING, 1 ABSENT FEATURE (T7), and the C10b doc check now raises MISSING (fixed after this count).

## X1 script and artifact contract

X1 path: independent/x1_remeasure.py (Step 10). Output results/x1_remeasure.json keys volumes{name}, interference{"a|b"}, chirality{nut_stl, boss_stl, nut_step} as [theta0, theta90] phases mod pitch, controls{away_hits, wrong_expected_fires, mirrored_nut_fires}. Test X1 fails if the script text names build_parts, cad_helpers or common.load_params.
Poses: R, Kd1, Kmax; files parts_cache/assembly/pose_<P>_<tag>.FCStd, tag 092p5 style; collets parts_cache/collet_<tag>.FCStd, _result.json (cuts, features with volume_mm3, tessellation, run_seconds), clamped solids collet_<tag>_clamped_Kd1.FCStd and _Kmax.FCStd; docs/collet_generator_usage.md; planted states parts_cache/assembly/ws<n>.FCStd with results/probes/ws<n>.json {fired[]}; output/step, output/stl, results/rebuild_record.json. Full key lists are in the tests/cad_helpers.py docstring and test_assembly.MEASURES.
Probe run order for the Engineer: probe_thread (24 s), probe_step3_parts (3 s), then detached probe_thread_mesh and probe_tilt (many thread booleans). The thread probe took 76 s in its first version and 24 s now; I ran it once beyond the 30 s rule by mistake.

## Params gaps (proposed keys; tests read them through need_key and fail ABSENT FEATURE until set)

icd.core_axis_offset_max 0.805 (A3c); icd.core_lead_in_clearance_min 2.055 (A3d); icd.core_lead_in_capture_min 9.31 (A3g); register.clamped_tilt_max_deg 0.573 (A3f); collet.delta 3.5 DERIVED (single source for Delta; helper derives it now); fit.min_contact_patch (A1a, floor 0 until set); fit.c_r_min and fit.g_a_min (T3, floor 0 until set). Count: 8. Also: a hold-torque record common.holding_torque(params, d) returning {value_nm, inputs{key: label}} (T7).

## Spec conflicts (params and measurement govern)

1. gameplan 349 F5 "genus equals declared through-hole count": genus is null in all five result JSONs (cadlib.py 243-244). Test asserts shell count 1, Euler record equal on reopen, features pass, flipped-copy mismatch.
2. gameplan 349 "On the empty baseline every one fails": five parts pass at B4 (Manager amends).
3. gameplan 317 C5 width law w_s = pi x Delta / N + w_min gives 1.416; params slit_width_seed 1.5. Test: width within 0.05 of 1.5 and not below the law.
4. gameplan 350 F6 ring gap 0.00 at K-max: built 0.005 (fit.model_contact_gap); tolerance 0.01.
5. gameplan 333 T3 "g_a per side": params g_a 0.30 is the total at the pitch line (nut tooth P/2 - g_a); per flank 0.15.
6. gameplan 321 C8 "accept range contains it": the widened core is tested at both ends x +/- core.tol (union coverage), since one window of 2.5 cannot contain a 2.0 interval at every x.
7. gameplan 339 T9 "alpha_crit": no params key; the probe measures the first thread-interference tilt and T9 compares it with register.t9_tilt_deg (0.924).
8. gameplan 315 C3 control: slits sit at 52 + 30k, so 0/120/240 miss them; the control uses a phase-0 stand-in.
9. common.py 191-196 check_envelope_request has no lower bound; envelope_min 85 is guarded only by validate_params.
10. gameplan 335 T5 "four poses": R and K-max at d_min and d_max.
11. P6d: spec "core top 650 and 900 plus 50" is read as collar_top_z + core length + load_clearance.

## Manual tests

A5 four-view PNG set, evidence: image-reviewer rubric table with one row per signed feature. H1 to H10: evidence is a measurement sheet (torque wrench, force gauge, scale, hand trial) with date, value, operator. No stub functions.

## Ceremony pushback

1. P7 list audit: P7 already covers every leaf; replaced by the declared-gaps audit.
2. Per-cut volume checks (C2) read generator-recorded volumes; they cannot be re-derived from the final shape.
3. A1a patch floor and T3 minima have no params values; floors of 0 until the Manager sets keys.
4. 99 functions is above the 70 guide; the splits are the Manager's.
5. T4 control, B1 control and E1 control test arithmetic of one-line helpers; kept only because rule 7 requires a control per gate.
6. A6b and A6c duplicate WS8 and WS9 coverage by ID only.

No ID moved between modules.
