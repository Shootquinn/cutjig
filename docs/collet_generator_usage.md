# Collet generator usage

`build_parts\collet_family.py` builds one collet of core diameter `d` (mm) and its two clamped-state solids from `params.yaml`. It runs under FreeCAD's headless interpreter, `freecadcmd`.

## The one command

Run from the project directory (PowerShell). `CJ_D` carries the diameter (a comma list builds several, one after another); leave it unset to build the params family (`core.diameters`, seven sizes).

```powershell
$env:CJ_D = "97.0"
& "$env:LOCALAPPDATA\Programs\FreeCAD 1.1\bin\freecadcmd.exe" build_parts\collet_family.py
```

A build takes about 30 to 60 s. Start long jobs detached so the shell stays free, with output to a log:

```powershell
$env:CJ_D = "97.0"
$p = Start-Process -FilePath "$env:LOCALAPPDATA\Programs\FreeCAD 1.1\bin\freecadcmd.exe" -ArgumentList "build_parts\collet_family.py" `
     -RedirectStandardOutput "research\quinn\cr_scratch\collet_097p0.log" -RedirectStandardError "research\quinn\cr_scratch\collet_097p0.err" -PassThru -WindowStyle Hidden
```

If FreeCAD is installed elsewhere, substitute the path to its `freecadcmd.exe`. `CJ_D` stays set for the rest of the PowerShell session; clear it with `Remove-Item Env:CJ_D` to build the family. Check a detached job with `Get-Content research\quinn\cr_scratch\collet_097p0.log -Tail 3` (the `cr_scratch` folder must exist).

Success is the line `RESULT collet_<tag> ... checks_all_pass=True` followed by the last line `BUILD_DONE collet_family`, plus a fresh `parts_cache\collet_<tag>.FCStd`. FreeCAD exits 0 even after an error, so read the log, not the exit code. A failed size prints a traceback and `BUILD_FAILED collet_<tag>`.

## What it reads

Only `params.yaml`, through `build_parts\common.py`. Keys: `core.tol`, `core.diameters`, `collets.*` (count, spacing, envelope_min, envelope_max), `collet.*` (c_i, slit_count, slit_width_seed, slit_length, slit_ligament, relief_hole_dia, min_wall, core_seat_height, core_seat_width, foot_ring_width, bore_lip_radius, rim_notch_width, rim_notch_depth, notch_azimuth_offsets_deg, label_azimuth_offset_deg, label_window_width, label_height, label_depth, tool_overshoot, colour, grip_window_lo, grip_window_hi), `cone.alpha`, `receiver.register_bore_radius`, `receiver.key_offset_deg`, `fit.seat_clearance`, `fit.model_contact_gap`, `holder.bottom_above_floor_Kmax`, `holder.key_width`, `holder.key_height`, `register.g_reg`, `caddy.socket_clear`, `caddy.socket_depth`, `iris.throat_open_radius`. To change a size or a rule, edit `params.yaml`, never the script.

## What it builds

Free collet: foot ring (z 0 to 1.995, radius 66.99), foot key, core-seat ledge (z 0 to 2.5), bore of radius (d + core.tol + collet.c_i) / 2, 10 degree outer cone, 45 degree bore lead-in chamfer of size min(wall - collet.min_wall, 10.5) (2.5 where that lies in (2.5, 3.5)) with a 1.0 mm lip, 12 alternating slits (1.5 mm), 12 relief holes (8.0 mm), rim notches (count = family index 1 to 7), a label window (flat recess, text in the result file). Boolean order: revolve, key fuse, slits (one compound), relief holes, notches, label.

Clamped solids: the same builder with the bore closed onto a core of d + 1.0 (Kd1) and d - 1.5 (Kmax), the cone moved inward by s + g/cos(alpha), and the slits narrowed to 1.238 and 0.584 mm.

## Checks run on the result

After the build the generator measures its own final shape and runs these predicates (from `tests\cad_helpers.py`), recording pass or fail per check under `checks` in the result file: C1 validity and one solid; C2 volume band against the analytic reference and per-cut removed volume against the expected thickness integral; C3 bore diameter; C5 slit count, width and relief holes; C6 minimum wall; C7 edge and slit-plane topology; C9b slit width floor; clamped solids valid and single. C4 (pairs of sizes) and the F-tests run from `tests\probes\probe_collet.py` and pytest.

## Output locations (parts_cache\)

- `collet_<tag>.FCStd`, the free collet.
- `collet_<tag>_clamped_Kd1.FCStd`, `collet_<tag>_clamped_Kmax.FCStd`.
- `collet_<tag>_result.json`: volume, validity, `cuts` (before, after, tool, expected per cut), `features` (name, pass, volume), `chamfer`, `notch_count`, `colour`, `label_text`, `clamped`, `caddy`, `checks`, `run_seconds`.

`<tag>` is the diameter as three digits, `p`, one decimal: 97.0 gives `097p0`, 93.7 gives `093p7`, 92.5 gives `092p5`.

## Worked example, d = 97.0

Command: the first block above. Expected log line: `RESULT collet_097p0 volume=... valid=True solids=1 checks_all_pass=True`, then `BUILD_DONE collet_family`. Expected values in `collet_097p0_result.json`: bore radius 49.5, chamfer `c_mm` 7.80 with `edge_z` 24.20, `notch_count` 4, `colour` green, `label_text` "97.0 | 95.5-98.0", `caddy.socket_d` 139.98 with `margin` 8.0, `clamped.Kd1.slit_width` 1.238, `clamped.Kmax.slit_width` 0.584, every entry of `checks` with `"pass": true`. Three FCStd files appear in `parts_cache`.

## Limits

- Diameter range: `collets.envelope_min` (85.0) to `collets.envelope_max` (106.585). The upper bound is the iris throat opening minus core.tol minus the throat slack; a larger collet needs a larger `iris.throat_open_radius`.
- The label is a flat recess; the text string is recorded in `label_text` and is not engraved (Pass 1 model).
- Slit, notch and label layout come from `params.yaml`; the notch count is capped by the length of `collet.notch_azimuth_offsets_deg` (7).
- Chamfer edge clearance to the relief holes (0.5 mm) is designed for 85.0 to 106.585; a changed `collet.relief_hole_dia`, `collet.slit_length` or `collet.min_wall` needs the chamfer rule re-checked.
- The caddy is recorded as a fit record only; the caddy solid is a later part.
- The witness scale belongs to the receiver and holder, not to a collet.

## A refusal

A request outside the range stops before FreeCAD builds anything and writes no file. With `$env:CJ_D = "110.0"` the log reads:

```
REFUSED 110.0: requested 110.0 exceeds envelope cap 106.585: change `iris.throat_open_radius`
BUILD_DONE collet_family
```

A request below 85.0 reads `requested ... is below collets.envelope_min 85.0`. Calling `build_collet(d)` from Python raises `ValueError` with the same text.
