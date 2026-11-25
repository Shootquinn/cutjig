## Corrections to the brief

1. **The radial-orientation test is an orientation test modulo 90 deg.** A rectangle has an edge pair across any direction its other pair runs along, so a NEMA 23 rectangle turned 90 deg about its centre passes K5 (probe p3, MEASURED). The long axis is held radial by K8 plan_extent: the turned motor leaves its footprint by 9.50 (MEASURED). Section 1a of the red-first file states the K5 test without this dependence. The rule stands with the dependence stated (gameplan l.139 below).
2. **Hub admission admits a hub. It does not require one.** A pinion drawn as the toothed trapezoid with no hub passes K5 and K8 (probe p9, MEASURED). This is the narrower-than-footprint class (K8 containment only) and stays with M1.
3. **The radial `outboard` branch runs in side views.** The code condition is `pr.get("frame") == "radial" or plan` (sketch_common.py l.1932). In a side view, `centroid` returns (x, z), so `hypot` there is a distance in the XZ plane and is no radius. Probe p19 (MEASURED): S1 live with `frame: radial` on motor23_a. The motor is drawn mirrored inboard of pinion_a (x -155.88 to -57.20) and raised 10. The radial branch reports no outboard issue. The side form reports "(x - x_pinion_a) cos(theta) -42.73". Today no spec drawn in a side view carries `frame: radial`: s1_spec.yaml has none, and S2 is plan only. X1 does not compare `sense`, so a row copied from S2 into a side-view spec would carry the branch over without any check firing. This is FIX TP1.2-1 below.

## 1 Controls re-run in memory

All ten controls ran through `check_sketch.run_control` and `compare` on the current `docs/sketches/` code (MEASURED, scratch script `tp13_probe.py`).

| Control | Result | Issues / planted | Reason (head) | Hand value |
|---|---|---|---|---|
| K5-Z3 | match, clean | 0 | 97 tagged artists | |
| K5-B8 | match | 1/1 | "load/motor23_a: cylinder axis X in plan_xy drawn as circle, needs rectangle" | |
| K5-B9 | match | 1/1 | "rectangle not radial: no edge pair across the radial direction at theta 210" | |
| K5-B10 | match | 1/1 | "radial-axis cylinder row in plan_xy needs a radial place footprint (TP-13; has 'round')" | |
| K5-B11 | match | 1/1 | "hub rectangle u [130.00, 145.00], half-width 22.81 not on the heel ... (u 125.00, half-width 45.62)" | 125 + 5 = 130; 140 + 5 = 145; 45.62 / 2 = 22.81 (DERIVED) |
| K8-Z6 | match, clean | 0 | 114 predicates | |
| K8-B18 | match | 1/1 | "load: axis inverted (x False, y True)" | |
| K8-B19 | match | 6/6 | screw_a azimuth 210.00 vs 150.00, screw_b 330.00, screw_c 90.00; 3 plan_extent | -150 = 210, -30 = 330, -270 = 90 (mod 360, DERIVED) |
| K8-B21 | match | 1/1 | "motor23_c outboard of pinion_c (radial): centroid radius 58.00 vs 115.61" | |
| K8-B22 | match | 1/1 | "height at inner end 91.24, at outer end 69.50" | 2 x 45.62 = 91.24; 2 x 45.62 x 95.22 / 125 = 69.50 (DERIVED) |

## 2 Probes (own defects, MEASURED)

| Probe | Defect | Expected | K5 | K8 | Verdict |
|---|---|---|---|---|---|
| p1 | motor23_a rectangle turned 0.5 deg | fire (tolerance 0.1) | fires "not radial" | | holds |
| p2 | turned 0.05 deg | pass (inside tolerance) | pass | pass | holds |
| p3 | turned 90 deg about its centre | K5 pass, K8 fire | pass | fires plan_extent by 9.50 | holds through the K8 premise (Correction 1) |
| p4 | motor as a parallelogram, tangential pair kept, skew 5 | fire | fires "trapezoid not radial" | | holds (four right angles required) |
| p5 | pinion hub extended 15 into the teeth | fire | fires "u [110.00, 140.00] not on the heel" | | holds |
| p6 | hub 3 wider than the heel each side | fire | fires "half-width 48.62" | fires plan_extent by 3.00 | holds |
| p7 | toothed piece asymmetric about the radial axis (heel symmetric, toe offset; t mid-extent 0) | | pass | fires azimuth 212.00 | caught by the centroid azimuth (NOTE 1) |
| p8 | hub drawn at the toe | fire | fires "u [80.22, 95.22]" | fires plan_extent by 15.00 | holds |
| p9 | teeth only, no hub | | pass | pass | narrower-than-footprint class (Correction 2) |
| p10 | whole pinion turned 180 deg about its centre | fire | fires hub "u 140.00" | fires taper 91.24 / 69.50 | holds |
| p11 | whole plan mirrored in y by the artist transform, axes not inverted | fire | | 83 issues (azimuth, plan_extent) | holds through TP-1 transform chain |
| p12 | whole plan rotated 120 deg (cyclic relabel of a, b, c) | fire | | 99 issues | holds |
| p13 | whole plan transposed (x, y swapped: a mirror about y = x) | fire | | 99 issues | holds |
| p14 | both axes inverted | fire | | "axis inverted (x True, y True)" | holds |
| p15 | motor23_c drawn at theta + 180, radius kept | fire | pass | fires plan_extent by 360.00, azimuth 270.00 | holds (radial outboard is radius-only; azimuth and extent carry the angle) |
| p16 | extra toothed piece widening inward beside a correct one | fire | | fires taper piece 1, 45.62 / 22.81 | holds (every piece tested) |
| p17 | S1 live, every `outboard` tagged `frame: radial`, side view | | | pass | radial branch active in a side view |
| p19 | p17 plus motor23_a mirrored inboard of pinion_a and raised 10 | fire | | no outboard issue (side form: -42.73) | **defect, FIX TP1.2-1** |

The rules as sign checks:
- **Classify:** a four-vertex piece is a rectangle iff e_i . e_(i+1) = 0 at all four vertices (relative 1e-7). A closed quadrilateral with four zero dot products cannot alternate its turn signs and close with positive edge lengths, so the test is exactly "rectangle".
- **Radial orientation:** in (u, t) at theta, at least two edges with |du| / L <= sin 0.1 deg.
- **Taper inward:** in (u, t), the t-extent at max u exceeds the t-extent at min u by more than TOL_Z.
- **Outboard radial:** |c(me)| - |c(other)| > 0, with c the plan centroid.
- **Handedness:** atan2(c_y, c_x) mod 360 within 0.1 deg of the key value, with the axes not inverted. Under any transform with det < 0, the azimuth order a, b, c reverses, so azimuth fires on at least two of the three screws.

## 3 Signatures

| Rule | Controls | Signature |
|---|---|---|
| Right-angle classify (four right angles = rectangle at any orientation; Annulus = circle) | K5-Z3 | **SIGNED** |
| Radial-axis orientation (tangential edge pair at theta, 0.1 deg) | K5-Z3, K5-B9 | **SIGNED**. The long-axis direction is held by K8 plan_extent (Correction 1, p3) |
| Radial-footprint premise (radial-axis round-kind row in plan needs `footprint: radial`, spec lint) | K5-B10 | **SIGNED** |
| Pinion hub admission only at the heel (starts on the heel edge within TOL_Z, half-width no greater than the heel) | K5-B11 | **SIGNED**. A missing hub is left to M1 (Correction 2) |
| K8 taper in the radial frame (toothed trapezoid pieces; the hub excluded by `_is_rect`) | K8-Z6, K8-B22 | **SIGNED** |
| K8 outboard, radial form | K8-Z6, K8-B21 | **SIGNED for plan_xy**. FIX TP1.2-1 lands in this revision, before M1 |
| Plan handedness B (axes not inverted; azimuth predicates) | K8-Z6, K8-B18, K8-B19 | **SIGNED** |

**FIX TP1.2-1 (Engineer, this revision).**
- Defect: the radial outboard branch in sketch_common.py l.1932 runs in side views.
- Change: take the radial form only when `ctx.view == "plan_xy"`. In a side view, a predicate carrying `frame: radial` is reported as "spec error: outboard frame radial needs plan_xy". The side form then remains the only side-view outboard test.
- Controls: new B K8-B24 on S1 live with `frame: radial` on motor23_a's outboard predicate, reason "frame radial needs plan_xy", planted 1. K8-Z4/Z5 and K8-Z6 stay clean.
- The rule premise is the plan centroid, (x, y) in the drill-axis frame. The view gate is the premise check.

**NOTE 1 (M1, S3).** Symmetry about the radial axis is not a K5 or K8 predicate in plan. The asymmetry in p7 was caught only because the centroid moved 2.00 deg. A smaller toe offset passes. The S2-3 pitch point reads the heel midpoint, so S2-3 is unaffected. The sign check, if wanted, is the plan analogue of `mirror_about_axis`: each vertex (u, t) has a partner (u, -t) in the radial frame.

## Gameplan lines to change

Apply after the Engineer's l.139 and l.142 changes in step1.2_engineer_redfirst.md section 8. Each Old below is a fragment of the Engineer's New text.

**l.139** (K5 row), the Engineer's new fragment.

Old:
```
each four-vertex piece has an edge pair across the radial direction at its theta (0.1 deg), and a gear row's rectangle is admitted as its hub only on the heel edge of its trapezoid and no wider (TP-13) |
```
New:
```
each four-vertex piece has an edge pair across the radial direction at its theta (0.1 deg; an orientation test modulo 90 deg, the long axis held radial by K8 plan_extent), and a gear row's rectangle is admitted as its hub only on the heel edge of its trapezoid and no wider (TP-13; admission, not presence: a missing hub is an M1 item) |
```

**l.142** (K8 row), the Engineer's new fragment.

Old:
```
outboard in radial form (centroid radius), taper in the radial frame on the toothed trapezoid |
```
New:
```
outboard in radial form (centroid radius; plan_xy only, `frame: radial` in a side view is a spec error, TP1.2-1), taper in the radial frame on the toothed trapezoid |
```

**l.142** (K8 row), the Engineer's new B fragment.

Old:
```
B23 sector drawn at half-angle 40 |
```
New:
```
B23 sector drawn at half-angle 40; B24 live S1 outboard with frame: radial in a side view (TP1.2-1) |
```

## Re-sign after P5f

Source: step1.2_engineer_redfirst_fixes.md. The code read is sketch_common.py `k8`, l.1842 to l.1849 (the TP1.2-1 gate). Run in memory on the current `docs/sketches/` code with the scratch script `tp13_resign.py`. Results MEASURED; hand values DERIVED.

**Gate.** Outside plan_xy, an `outboard` predicate with `frame: radial` is reported once as a spec error and goes into `bad`, so the per-pose loop skips it. In plan_xy the radial form is unchanged.

| Control | Result | Issues / planted | Reason (head) | Hand value |
|---|---|---|---|---|
| K8-B24 | match | 1/1 | "motor23_a outboard of pinion_a: spec error, frame radial needs plan_xy (view side_xz)" | |
| K8-B28 | match | 8/8 | projected_x centre -121.38 vs -113.88; projected_extent x [-139.98, -102.79] outside [-124.98, -102.79] (by 15.00), at four poses | 131.50 cos 210 = -113.88; -113.88 - 15 / 2 = -121.38 |
| K5-B12 | match | 1/1 | "capture_end/holder: bore_cone trapezoid z [90.00, 95.00] outside mate collet z [100.00, 132.00]" | |
| K5-B13 | match | 1/1 | "load/pinion_a: hub rectangle u [125.00, 140.00], half-width 50.62 not on the heel ... half-width 45.62" | 45.62 + 5 = 50.62 |

Unchanged controls re-run, all matching: K5-Z2, K5-Z3, K5-B6, K5-B11, K8-Z4, K8-Z5 (346 predicates), K8-Z6 (114), K8-B21.

| Probe | Defect | Result |
|---|---|---|
| p19 | S1 side view, `frame: radial` on motor23_a outboard, motor drawn inboard of pinion_a and raised 10 | K8 fails with "spec error, frame radial needs plan_xy". It was silent before P5f. With `frame` removed, the side form reports -42.73 (p18b) |
| p20 | the same defect with `frame: polar` (a value no rule defines) | side form fires, -42.73 at each pose |
| p21 | `frame: polar`, no defect | K8 pass (NOTE 2) |
| p22 | S2 live plan after the gate | K8 pass |

| Rule | Controls | Signature |
|---|---|---|
| FIX TP1.2-1: radial outboard form only in plan_xy; `frame: radial` in a side view is a spec error | K8-B24; K8-Z4, Z5, Z6 clean | **SIGNED**. K8 outboard radial is now SIGNED without restriction |
| TP-13 hub width (hub half-width no greater than the heel half-width) | K5-B13; K5-B11 unchanged | **SIGNED** |
| TP1.1-3 bore_cone lower bound (piece inside the mate's z extent on the low side) | K5-B12; K5-B6 high side unchanged | **SIGNED** |
| TP1.1-11 projected_extent low-x end | K8-B28 | **SIGNED** |

**NOTE 2 (not blocking).** `sense_lint` does not check the value of `frame`. In a side view an unknown value falls through to the side form, which is correct there. In plan the radial form applies whatever the value. No predicate reads a wrong sense because of this. The value lint belongs in the S3 lint pass.

### Gameplan lines to change (re-sign)

none. The K5 B12 and B13 text and the K8 TP1.2-1 wording and B24 are already in the gameplan (fixes file, Corrections 5). The l.139 and l.142 Old/New above still apply, but only where their Old text is still present.
