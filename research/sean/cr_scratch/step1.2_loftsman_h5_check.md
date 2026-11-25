## Verdict

**H5 PASS.** 0 FIX, 4 NOTE. No drawn or checked value moves; S1 stays r4. The orchestrator may run the accept.

c range, for Sean (DERIVED, c >= 0):
- **0 <= c <= 42.34**: Design Notes 23 holds exactly as written. The 0.5 and 0.75 m values are unchanged (stop 184.84, start 834.84, park 959.84 z_A, stroke 775). The 1 m class gives park 1209.84, stroke 1025, L 1140.
- **42.34 < c <= 117.34**: the 1 m park 1209.84, stroke 1025 and L 1140 still hold. The 0.75 m class stop and start rise with c (stop 142.50 + c, start 792.50 + c). The drawn S1 r4 start pose no longer matches.
- **c > 117.34**: the 1 m start governs park: park 1092.50 + c, stroke 907.66 + c, L_min 1017.66 + c (to c = 292.34).

## Corrections to the brief

1. TASK 2 asks for the range of c over which park 1209.84 holds. The answer is c <= 117.34. Sean also needs the narrower bound of 42.34, because the rule the Engineer wrote applies the start-above-core term to every class, while Design Notes 23 names only the 1 m class. NOTE 1.
2. The H5 record diff has 11 fields: 1 timestamp, 3 changed 1 m terms and 7 added fields (`drawn_symbol_validity`, plus `stops_z_A` and `symbol_terms` in each of the three options). Every added field is a 1 m or symbol report field. spec_status is equal.

## 1 Hand values against check_stack

Inputs (DECLARED/ASSUMED as tagged in keys_read): stop.height_z 184.84, collet.core_stop_z 42.5, stop.g_stop 25, drill.bore_ceiling_above_tip 800, upper.travel_max 650, stop.collar_top_z 159.84, upper.load_clearance 50, allowances 30/30, max(nut 30, housing 30) 30, g_min_screw_block 10.

stop_k = max(184.84, 42.5 + L + 25 - 800, 42.5 + L + c - 650):

| L | term 2 (bore) | term 3 (start-above-core) | stop_k (hand) | start_k (hand) | start_minus_core_top (hand) | check_stack (MEASURED) |
|---|---|---|---|---|---|---|
| 500 | -232.50 | c - 107.50 | 184.84 for c <= 292.34 | 834.84 | 834.84 - 542.50 = 292.34 | 184.84 / 834.84 / 292.34; breakpoint 292.34 |
| 750 | 17.50 | 142.50 + c | 184.84 for c <= 42.34 | 834.84 | 834.84 - 792.50 = 42.34 | 184.84 / 834.84 / 42.34; breakpoint 42.34 |
| 1000 | 267.50 | 392.50 + c | 392.50 + c for all c >= 0 (392.50 > 267.50) | 1042.50 + c | c | "392.50 + c" / "1042.50 + c" / "c" |

1 m capture = core top minus stop = 1042.50 - (392.50 + c) = 650 - c (DERIVED). This matches Design Notes 23.

Park, stroke and L per Q9 option. park = max(max_k start_k, 159.84 + max L) + 50. Max L is 750 under both first options, since core.length_install is always loaded.

| Option | park (hand) | stroke = park - lowest stop | L_min = stroke + 30 + 30 + 30 + 2(10) | at anchor_z (= park - 74.00) | check_stack (MEASURED) |
|---|---|---|---|---|---|
| 0.5 m only | max(834.84, 909.84) + 50 = 959.84 | 775.00 | 885.00 | 885.84 | 959.84 / 775.00 / 885.00 / 885.84 |
| 0.5 and 0.75 m | 959.84 | 775.00 | 885.00 | 885.84 | 959.84 / 775.00 / 885.00 / 885.84 |
| plus 1 m | max(1042.50 + c, 1159.84) + 50 = 1209.84 for c <= 117.34; 1092.50 + c above | 1025.00 (c <= 117.34) | 1135.00 (buy 1140) | 1135.84 | 1209.84 / 1025.00 / 1135.00 / 1135.84; park breakpoint 117.34 |

The at_anchor offset is 885.84 - 959.84 = -74.00 (DERIVED): +130 position_above_tip, +6 half thickness, +15, +30, +10, -265. It is the same for each option.

Each hand value matches the JSON to 0.01. Each breakpoint in `symbol_terms` matches the hand value: 292.34, 42.34, 117.34, and the stroke and L_min plateau at 292.34, where the lowest stop leaves 184.84.

## 2 stop_k and for_step4

- **stop_k**: correct. Term 3 makes start_k = stop_k + travel >= core_stop + L + c for every class. That is the FIX 5 condition: the cutter starts at least c above the core top. For the 1 m class it governs on all of c >= 0 and gives Sean's numbers.
- **for_step4**: correct. It is the same stop_k inside max_k(... + travel), against the entry plane stop.collar_top_z + max_k L_k, plus load_clearance. This matches `park_rule.park` and check_stack.park_tip_z_A.
- Park 1209.84 holds while the entry-plane term governs: 1042.50 + c <= 1159.84, so **c <= 117.34** (DERIVED). Above that the 1 m start term takes over (park 1092.50 + c).

## 3 c treatment

- c is a spec symbol (`symbols.c`). It has no overlay leaf and no value, so it invents no value.
- K2 runs on overlay leaves and spec keys, and c is neither. K2 passes in the wip/ record (17/17).
- Domain lower bound 0 (DECLARED by the Engineer): sound. A negative c is the FIX 5 defect, a start inside the uncut core.
- `numeric()` takes a drawn value only where the function is constant on its first segment, and records that segment's upper end in `drawn_symbol_validity`: start max 42.34, park 117.34, lowest stop 292.34. Otherwise it raises "depends on symbol c" (H5-B fires). This is a lofting-legal treatment: drawn values carry their validity interval.

## 4 Record diff (wip/ against docs/ s1_checks_r4.json, MEASURED by a recursive field walk)

| Field | docs | wip | Class |
|---|---|---|---|
| timestamp | 13:49:52 | 15:36:23 | timestamp |
| reported.park_tip_by_plane_z_A.core_stop.core.length_optional | 1092.5 | "1092.50 + c for c >= 0" | 1 m term |
| reported.q9_options.plus 1 m.starts_z_A.core.length_optional | 917.5 | "1042.50 + c for c >= 0" | 1 m term |
| reported.q9_options.plus 1 m.start_minus_core_top.core.length_optional | -125.0 | "c for c >= 0" | 1 m term |
| reported.drawn_symbol_validity | absent | added | symbol report |
| reported.q9_options.{0.5 m only, 0.5 and 0.75 m, plus 1 m}.stops_z_A (3) | absent | added | report; 1 m entry symbolic, the rest equal to the stops in force |
| reported.q9_options.{same three}.symbol_terms (3) | absent | added | symbol report |

Other fields: keys_read, checks (17 pass, reasons equal), files_sha256, spec_status and every 0.5 / 0.75 m number are equal. No FIX.

## 5 Collar gloss

s1_spec.yaml l.320 reads "from the wing-nut top (collar.top_above_plate above the wing-nut top) to stop.collar_top_z". This is the change NOTE R2 asked for. It agrees with the z_rule z_min "collar_top - collar.top_above_plate" (6.75 below the collar top).

## 6 NOTEs

- **NOTE 1 (for Sean, N11).** The term applies to all classes. Design Notes 23 sets c for the 1 m class only.
  - If Sean sets c <= 42.34, nothing else moves.
  - If c > 42.34, he has two options. (a) Keep one c for every class (geometrically consistent: no class starts inside its core). The 0.75 m stop and start then rise to 142.50 + c and 792.50 + c, and S1 must be redrawn (r5). (b) Make the term class-specific (c_k, 0 for the 0.5 and 0.75 m classes). Both are design choices.
- **NOTE 2.** The domain [0, null] has no upper end. The 1 m capture is 650 - c, so c >= 650 leaves no cut. If capture must cover a stated cut depth d, the upper bound is c <= 650 - d. Add the bound when Sean sets c.
- **NOTE 3.** `--stale` compares keys_read, and c is not a key. When Sean sets c, it should become an overlay leaf with a value and status (K2), so that `--stale` reads it and a value above 42.34 shows up as a moved key on the accepted r4 record. A spec-only edit of `symbols.c` would not flag stale.
- **NOTE 4.** The Design Notes 23 cost line (highest point 2219.84 z_S for the 1 m class) rides on park 1209.84, so it carries the same bound, c <= 117.34.

## Gameplan lines to change

**l.591** (Design Notes 23, FIX 5). Append to the end of the bullet.

Old:
```
S1 draws the 0.75 m core only; the 1 m class is reported.
```
New:
```
S1 draws the 0.75 m core only; the 1 m class is reported. Range (Loftsman H5 check, 1.2 step 0, DERIVED): the spec applies the start-above-core term to every class, so the 0.5 and 0.75 m values stand for 0 <= c <= 42.34 (above it the 0.75 m stop and start read 142.50 + c and 792.50 + c); park 1209.84, stroke 1025, L 1140 and the 2219.84 z_S highest point stand for c <= 117.34 (above it park 1092.50 + c); 1 m capture 650 - c bounds c below 650.
```

**l.286** (detail 1.3, Reported).

Old:
```
S1 r4: 885.00 / 885.00 / 1135.00, 885.84 / 885.84 / 1135.84 at the drawn anchor, buy 900 / 900 / 1140)
```
New:
```
S1 r4: 885.00 / 885.00 / 1135.00, 885.84 / 885.84 / 1135.84 at the drawn anchor, buy 900 / 900 / 1140; the 1 m values hold for c <= 117.34 (Design Notes 23))
```

**l.649** (Echo Site Registry, lift stroke).

Old:
```
**1025** with the 1 m class)
```
New:
```
**1025** with the 1 m class, for c <= 117.34)
```

**l.650** (Echo Site Registry, park rule): adopt the Engineer's new text from step1.2_engineer_step0.md section 9 unchanged. It carries both c ranges.
