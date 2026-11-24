## Contract

Pose FCStd `parts_cache\assembly\pose_<P>_<tag>.FCStd`: ten objects, Name = Label = part name. `frame` = compound of 6 member solids, `bracket` = 16, `tnut` = 128. `base` = receiver fused with plate (thread zone read from it). `core` = cylinder stand-in. `cutter` = compound of tube, face annulus, lead-in ring (coaxial cylinder face, r = icd.core_lead_in_bore) and funnel (Z-axis cone with circular rim).

`results\assembly_poses.json`: `lead_mm`; `base_pose{part: 4x4}`; `sizes{tag{R|Kd1|Kmax{phi_deg, dz_mm, placements{part: 4x4 row-major}}}}`; `instances{member[], bracket[], tnut[]}` (names in compound solid order: member_<id>_<n>, bracket_<purchased|printed>_<n>, tnut_<n>); `ws{"<n>"{pose, tag}}`. phi and dz are negative for a clockwise turn from R.

`ws<n>.FCStd`: the same ten names. `ws<n>.json`: pose, tag, fired[], reasons, expected[], absent. `ws0.json`: poses R, Kd1, Kmax at nominal, fired[] empty. Pose JSON: pairs `a|b` (45), feature_pairs `fa|fb` (6), measures, controls `{key{good,bad}}`, absent. `frame_instances.json`: pairs `a|b{overlap_mm3, min_dist}`, counts, per_bracket_tnuts. Optional ASSEMBLY.md section `### Instance pair rulings` (kind pair, max mm3).

Report: header names `assemble_report.py`; `## Size <tag>`; rows `| a / b | pose | mm3 | dist_mm | class | pass or FAIL |`, 51 per pose, feature rows mm3 `-`.

## Test review

| Tests | Reads | Correct pass | Control |
|---|---|---|---|
| A1a x21, F6 x3, A4 x3 | pairs, feature_pairs, tree | yes | check_class controls (Step 4) |
| A3e, A3h, A3i, T4 | holder_bottom, skirt, engaged_mm | yes | G2 gate controls |
| A3c, A3f, A3d, A3g, A6a, P6b, T5 | new measures | yes | G1 good/bad (new) |
| A3b | four fits | no: 2 of 4 fits (column foot, carriage guide) belong to Step 12; fused base hides the spigot | none |
| A6 x9, A6b, A6c | ws<n>.json fired | any gate passed | G2 expected gate, G3 zero |

## New tests

| ID | Reads | Control |
|---|---|---|
| G1 x10 | pose controls per measure | good passes, bad fires |
| G1 bore | lead_in_bore_radius = icd.core_lead_in_bore | cutter without lead-in reads 71.44 |
| G2 x11 | ws<n>.json fired meets WS_EXPECT | planted gate variants (6) |
| G3 | ws0.json empty, three poses | synthetic correct pose |
| G4 x6 kinds, bracket-tnut | frame_instances.json | planted overlap, ruled row |
| G5 | assembly_poses.json | pure-z nut, displaced frame, wrong sign |
| G6 x7 | report vs pose JSON | edited cell, dropped row, flipped verdict |
| G7 x21 | collet volume and slit width equal generator solid | |
| G7 sizes | marks of A1a, A3d, A3e, A3h, A3i, T4 | |

Invariants (6) carry green_at_4: `label()` and conftest allow an invariant at 4 only. 59 discriminators carry green_at_7.

## Counts

Refreshed baseline, new file excluded: 591 collected, 415 pass, 176 fail. With new file: 656 collected, 421 pass, 235 fail. Every failure carries MISSING: or ABSENT FEATURE: (470 matching lines). green_at_7: 185, all red.

## Findings

1. A3b: Manager rules. Recommend relabelling to green_at_12 and measuring only key/pin and spigot at 7; the probe lists the four fits as absent.
2. `probe_step6_parts.py` imported `rest.py`, which rebuilt and saved `rest.FCStd` on import. Probe now loads it under another name. `rest.FCStd` restored from the FCBak with mtime 05:44:49; FCBak archived; the 72-file mtime list matches.
3. Smoke test: probes ran on an identity-placed fixture of existing parts (R pose, one planted file); every measure, control, instance table and gate wrote JSON. Frame/tnut contact area now bbox-filtered per solid.

## Probe refresh

`probe_step6_parts.py` ran detached (log `step7_probe_step6_parts.log`); `step6_parts.json` newer than `rest.FCStd`; test_step6_parts 51 pass.
