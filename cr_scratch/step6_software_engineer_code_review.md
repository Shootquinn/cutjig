## 1. Result-changing defects

None in build_parts. Geometry, signs and measurement lines read correct (rest ring mouth centred on -X via `sector_solid` centring; base notch, tray ramp, bracket hole rows).

Row weaknesses that cannot fail:
- `tray.py:61` cavity depth row: built equals expected (`ztop - z1`), pass forced by `ok=`.
- `plug.py:29` shank-gap row: derived from the same radial read it compares against.
- `base.py:45` `sl_pos` computed, never used.
- `frame.py:80` `cxp` computed, never used.

## 2. Params-duplicating literals

Numeric-literal grep over base, tray, plug, foot, tnut, bracket, frame, caddy, gauge, rest, stop, step6lib, hardware_geom (excluding 0, 1, 2, 0.5, 360, 90, 180), compared to all params leaf values. Every hit is a coincidental value (scan span, fraction, rounding digit, unit conversion), none a part dimension:

| File:line | Literal | Role |
|---|---|---|
| base 43, tray 47 | 120.0 | radial scan length |
| tray 41-43 | 4.0, 5.0 | Wy/4, Lx/5 scan positions |
| frame 130 | 1000.0 | mm to m |
| rest 62 | 3600 | mouth sampling steps |
| step6lib 18, 19 | 0.015, 17.0 | `TOL`, `SCAN` |

String literals that duplicate params values (defect class, fixed by deriving the text from `g()`):
- `tray.py:60` "253" (= `tray.ramp_x` span 81 - (-172)).
- `foot.py` note "28 from the rail end" (= `foot.m8_x - profile.width`).
- `frame.py:186` FR4 note "0.35 mm2", "y 249", "245.3 to 249.5".

Params-internal duplicate: `base.column_notch_x` equals half of `base.column_notch[0]` (70 = 2 x 35); `tray.relief` repeats the same notch.

`frame.py:156` T-nut sample names `tnut_1,2,33,34,65,66,97,98` hard-code 8 per bracket; derive from `hardware.tnuts_per_bracket`.

## 3. Duplication, term greps

- The per-feature `C.line_ivals` width/depth measurement idiom repeats in base, tray, foot, caddy, rest. A `S.span(sh, p0, p1)` helper returning gap or extent removes about 40 lines. Not blocking.
- Dead helpers in step6lib: `fdiv`, `extent_along`, `ivals`, `inside`, `present` (zero callers).
- Unused imports: `math` in caddy and gauge.
- Hazard-term grep (pinch, finger, crush, hand entry, 13854, knuckle, safety) over all 16 scripts: no hits.
- Printer-term grep (bed, nozzle, material, orientation, layer): one hit, `receiver.py:95` comment "same material removal"; no key read.

## 4. Criterion 11 and FCBak

- `SubtractiveHelix` in nut.py, tray.py, base.py: no hits. Tray drain is a plain bore with the thread named in the row (BS6).
- `.FCBak` in `parts_cache` and `results`: none.

## 5. Test counts (read-only; full suite not run while probe fixes are in progress)

- Collected 584 (540 + 44 in `test_step6_parts.py`; Engineer's 582 plus 2 added by the probe-fix pass). Criterion 6 "540 + added": met.
- `green_at_6` collected: 35. `test_step6_parts.py`: 38 pass, 6 fail. HD5 and HD6 now pass.
- Failing, all stale-probe reads (probe copies patched per findings D2, D3 pass):

| Test | Reason |
|---|---|
| NT4_NT5_glyph_sense_span_and_faces | `ABSENT FEATURE` sense -1 count 3, sense +1 count 4: glyph window starts inside the skirt (D3) |
| NT4_NT5_result_json_glyph_record_matches_probe | same probe |
| control_nt4_nt5_fire_on_filled_window | same window |
| RC6_scale_graduation_count_and_pitch | rim radius on lead-in chamfer (D2) |
| HD7 tick K-max | D2 |
| HD7 tick K d+1 | D2 |

Close criterion 6 holds when the probe-fix pass lands and `probe_step6_marks` reruns (3,212 s).
