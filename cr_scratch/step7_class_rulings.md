## Contact-class rulings, Step 7

Source of record: ASSEMBLY.md Relations (45 part pairs) and Feature pairs (6). Measured values: results\probes\pose_{R,Kd1,Kmax}_100p0.json (nominal size; all seven sizes pass, cr_scratch\step7_interference_report.md, 1071 rows). Tags: MEASURED = read from probe JSON or the rebuilt FCStd; DERIVED = computed from params or a stated formula; DECLARED = chosen by design, no measurement behind it.

Classes: C contact, P press pads, G gap, F free. Pose R = release; pose K = Kd1 and Kmax.

Pair-class totals: R C 7, P 1, G 12, F 25; K C 9, P 1, G 10, F 25 (matches ASSEMBLY.md).

### 1. Part pairs (45)

| Pairs | Class R | Class K | Evidence (nominal 100 mm) | Tag |
|---|---|---|---|---|
| base\|collet | C | C | dist 0.000, patch 6,726 / 6,966 / 7,341 mm2 (R / Kd1 / Kmax), overlap 0 | MEASURED |
| base\|nut | C | C | dist 0.004, patch 4,766 / 5,704 / 6,963 mm2, overlap 0 (thread flanks seated by model gap fit.model_contact_gap 0.005) | MEASURED |
| base\|frame | C | C | dist 0.005, patch 121,902 mm2 | MEASURED |
| frame\|bracket, frame\|tnut, bracket\|tnut | C | C | dist 0.000, patches 57,218 / 12,288 / 4,550 mm2 (nominal), per-instance common 0 at 16 purchased, 8 printed, 96 T-nut hosts | MEASURED |
| holder\|nut | C | G | R dist 0.005, patch 3,658 mm2 (collar underside on nut plate top); K dist 0.51 | MEASURED |
| holder\|collet | G | C | R dist 0.295; K dist 0.005, patch 4,164 / 11,539 mm2 | MEASURED |
| holder\|washer | G | C | R dist 0.74; K dist 0.005, patch 1,380 mm2 | MEASURED |
| collet\|core | G | C | R dist 1.000; K dist 0.005, patch 7,455 / 7,393 mm2 | MEASURED |
| nut\|washer | P | P | dist 0.000, overlap 2.387 mm3 in every pose, window 2.0 to 2.45 | MEASURED |
| base\|holder | G | G | dist 0.125 in every pose | MEASURED |
| base\|washer, base\|core, holder\|core, collet\|nut, collet\|washer, nut\|core, washer\|core | G | G | g_min 0.5 to 1.0 in ASSEMBLY.md; every cell passes in 21 pose JSONs | DECLARED (g_min), MEASURED (pass) |
| nut\|cutter | G | G | g_min 25 = stop.g_stop; 31.740 (Kd1), 38.830 (Kmax) | DERIVED |
| 25 free pairs: base with bracket, tnut, cutter (3); holder, collet, nut, washer, core each with frame, bracket, tnut (15); holder, collet, washer, core each with cutter (4); frame, bracket, tnut each with cutter (3) | F | F | overlap 0 in all 1071 rows | DECLARED (class), MEASURED (overlap 0) |

### 2. Feature pairs (6)

| Pair | R | Kd1 | Kmax | Gap R / Kd1 / Kmax | Tag |
|---|---|---|---|---|---|
| holder bottom \| collet foot ring top | G | G | C | 11.626 / 7.089 / 0.005 | MEASURED |
| holder flange underside \| receiver rim | G | G | G | 13.126 / 8.590 / 1.500 | MEASURED |
| holder bottom \| receiver floor | G | G | G | 13.626 / 9.090 / 2.000 | MEASURED |
| nut plate top \| holder collar underside | C | G | G | 0 / 0.75 / 0.74 | MEASURED |
| nut skirt bottom \| receiver floor | G | G | G | at least one pitch (8) | DECLARED (limit), MEASURED (pass) |
| nut collar top \| cutter lowest point | F | G | G | 20.464 (R) / 25.001 / 32.090 against 25 | MEASURED |

### 3. Relation rows changed in Step 7

Source of reasons: step7_loftsman_definition.md L4. Topologist sign: step7_topologist_crossreview.md, line "L4 placements: SIGN WITH EDITS E5, E7" (E7 sets the nut\|washer volume floor 2.30); Topologist gate addendum A confirms the pair measurements valid. Systems Engineer review row 6: reasons present, no threshold weakened.

| Row | Change | Geometric reason | Tag |
|---|---|---|---|
| base\|holder | g_min 1.5 to 0.12 | key in slot (12.0 - 11.75) / 2 = 0.125 | DERIVED; read 0.125 MEASURED |
| holder\|collet R | g_min 0.30 to 0.29 | 0.30 x cos 10 deg = 0.2954 normal to the cone | DERIVED; read 0.295 MEASURED |
| holder\|nut K | g_min 0.75 to 0.50 | washer proud = washer.thickness 1.3 - nut.washer_pocket_depth 0.8 + 0.01 = 0.51 | DERIVED; read 0.51 MEASURED |
| nut\|washer | C to P, overlap 2.0 to 2.45 mm3 | three press pads hold the washer; designed 2.40, built 2.387 | MEASURED |
| feature nut collar top \| cutter | Class_R G to F | R unclamped gap 20.464 is below g_stop 25; the 25 applies to the clamped poses | MEASURED |

No predicate threshold weakened. nut\|washer P is a retention feature (class C touching with a bounded pad overlap), not an interference allowance.

### 4. Receiver and nut pair classes (Topologist Addendum A)

Finding: receiver and nut pair classes are VALID (MEASURED). The receiver fails BOP (InvalidCurveOnSurface) and returns an invalid result against a half-space tool at an axial plane (x = 0, y = 0.3); the probes never cut by an axial plane. Controls: planar box analytic 125 mm3 reads 125.000 on receiver, plate, nut; sphere distance analytic 4 reads 4.000; thread slab 51,544.44 against slice integral 51,543.07 (receiver), 88,522.25 against 88,521.52 (nut); shifted-partner commons agree with fuse and cut within 0.1 mm3. Every C and G zero also has min_dist above 0. Affected pairs (base\|nut, holder, collet, washer, core; nut\|holder, collet, washer, core, cutter, frame, bracket, tnut): VALID. Fix-pass guard: checked_common raises InvalidCommon in place of a 0.0 read (control: shifted boxes 600 mm3 read 599.9999999999999; shifted tubes 18,849.556).

### 5. PZRT T-nut proxy standing

The PZRT 3030 T-nut CAD is not on disk; tnut.FCStd is a proxy (DECLARED). The 96 T-nuts (8 per bracket, 12 brackets) are ASSUMED. Pair classes frame\|tnut C, bracket\|tnut C and the F pairs carry no information about the real roll-in spring profile. The proxy stands to Step 9 BOM; no download.

### 6. Receiver-to-plate pairing

The base object is one compound of receiver and plate. base\|collet and base\|nut cannot separate receiver from plate. Receiver underside contact 0.0 (r 80 foot against plate hole r 80.2, fit_spigot_hole 0.200) is geometry, not a modelled support. Carried to Steps 8 and 12 (see step7_manager_close.md carry-forward).
