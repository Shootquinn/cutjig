## Usage doc cold read

| Step | Followable | Reader would not know | Edit made |
|---|---|---|---|
| Set CJ_D, run freecadcmd | Yes | FreeCAD path if installed elsewhere; CJ_D persists in session | Added path substitution and Remove-Item Env:CJ_D line |
| Detached run | Yes | How to watch the log; cr_scratch must exist | Added Get-Content -Tail 3 line |
| Read success | Yes | Exit code is 0 on failure; doc says so | None |
| Compare result JSON | Yes | Tag format; doc gives it | None |
| Refusal at 110.0 | Yes | Message text given verbatim | None |

Worked example values (bore 49.5, chamfer 7.80, edge_z 24.20, notch_count 4, green, label "97.0 | 95.5-98.0") match collet_097p0_result.json and the Loftsman table. No number changed.

## Completeness (collet_090p0 JSON; all seven sizes show the same feature list, all pass)

| Feature | Status | Basis |
|---|---|---|
| Slit | PRESENT | 12 alternating, width 1.5 |
| Relief hole | PRESENT | 12 |
| Foot key | PRESENT | width 11.75 |
| Foot ring | PRESENT | radius 66.99 |
| Core seat | PRESENT | ledge top 2.5 |
| Rim notch | PRESENT | count equals family index |
| Label | SIMPLIFIED | flat recess 0.81 deep; text string in JSON, not engraved |
| Chamfer | PRESENT | 45 degree, c 10.5 at d 90 |
| Bore lip | PRESENT | R 1.0 |
| Colour | PRESENT | recorded per size |
| Caddy fit record | PRESENT | socket 139.98, depth 40, margin 8.0 |
| Distinctness | PRESENT | notches 1,2,3,4,5,6,7 for 90.0 to 105.0; colours red, orange, yellow, green, blue, violet, white; seven distinct label strings |

Witness scale is on the receiver and holder, not a collet feature; not a Pass 1 criterion.

Free-text findings (non-blocking): the label text is not physically present on the part, so identification by label depends on the Step 6 production pass.

## Verdict

PASS for Pass 1 completeness. No ABSENT feature.

visual gate NOT RUN
