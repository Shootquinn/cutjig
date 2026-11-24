## Signature: WITHHELD

Checked against cr_scratch/step2_loftsman_crossreview_reply.md, cr_scratch/step2_loftsman_geometry_numbers.md and params.yaml, arithmetic rerun in `python -I`. Two lines carry wrong geometry. Everything else in decisions 2, 3, 4, 5, 7 and the ICD matches.

## Withheld lines

| # | Line (step2_system_concept.md) | Number written | Correct number | Basis |
|---|---|---|---|---|
| W-1 | Decision 7, line 17: "Accepts nominal plus or minus 1.25 mm; coverage 88.75 to 106.25 against the widened core range 89 to 106" | window symmetric about d; coverage 88.75 to 106.25 | window is d - 1.5 to d + 1.0, centre d - 0.25; coverage 88.5 to 106.0, windows abut with no gap | Same line gives the window d - 1.5 to d + 1.0. For d = 90 that is 88.5 to 91.0; for d = 105 it is 103.5 to 106.0. The line contradicts itself. Reply table 3.1 lists the same windows. Widened range 89 to 106 sits inside 88.5 to 106.0, so the conclusion survives. |
| W-2 | Tolerance table, line 49: "Slack at envelope max 106.585 : 0.29" (decision 5 does not repeat it) | 0.29 per side | 0.50 per side (1.00 diametral) | Worst core on the 106.585 collet is 106.585 + 1.0 = 107.585. (108.585 - 107.585) / 2 = 0.50. The 0.29 came from my step 2 numbers file, section 3.2. It subtracts 1.0 mm diametral from 1.2925 mm per side, which mixes units. I withdraw it. Rule `collets.min_throat_slack` 1.0 is met exactly, diametral. |

Required edits: W-1 reads "Accepts d - 1.5 to d + 1.0 (window 2.5, centre d - 0.25); coverage 88.5 to 106.0 against the widened core range 89 to 106". W-2 reads "0.50 per side (1.00 diametral)".

## Numbers that match (no change)

| Item | Concept value | Check |
|---|---|---|
| Release, cone 10 deg | tan 10 = 0.176 < 0.25 | 0.17633 |
| Retired 20 deg cone | 10.72 and 9.19 N m, +11.26 mm major | reply sec. 5 and 4 |
| Lift play, flange annulus | p 0.75; 5.00 against 7.4 | reply D-5 |
| Collar back-off | 281.5 N against 46 / 88 / 128; ratio 2.20 | 281.5 / 128 = 2.199 |
| Lateral moment | 100 N at 106.4 mm = 10.6 N m | 10.64 |
| Grip couple | 354 N over 30 mm | 10.6 / 0.03 = 353.3 to 354 |
| Core mass at d = 105, 2400 kg/m3 | 10.4 / 15.6 / 20.8 kg; 102 / 153 / 204 N | 10.39 at 0.5 m |
| H3 side load | 21.2 N | 10.6 / 0.5 |
| H2 pull | 204 N at 0.5 m, 306 N at 0.75 m | 2 x weight |
| Holding | PTFE 15.47 / 13.26; plain 10.65 / 9.13; miss 8.7 percent; margin 33 percent | reply sec. 5 |
| Hand force | 52 N per hand on 230 mm | 12 / 0.230 = 52.2 |
| Washer | ID 136.8, OD 143.2, t 1.3; pocket r 68.3 to 71.7 | reply sec. 4 table |
| Spread at d = 90 | plain 3.8 to 23.1; PTFE 5.8 to 31.0 | reply sec. 5 |
| Throat slack per side | 1.29 at 105 + 1.0; 3.79 at 100; 8.79 at 90 | 1.2925 / 3.7925 / 8.7925 |
| Core axis offset | 0.805 linear, 0.41 RSS | 0.805; 0.412 |
| Clamped tilt | 0.57 deg; 5.0 mm at 0.5 m, 7.5 mm at 0.75 m | atan(0.30/30) = 0.573 deg |
| Register tilt | 0.597 / 0.588 deg, rock 0.315, total 0.903 against 1.021 | reply sec. 3 |
| alpha_crit | 1.532 deg; line 1.021 | 8 / (2 x 149.58) |
| Lead-in check at d = 105 | 0.50 against 1.29, margin 0.79 | 1.29 - 0.50 = 0.79 |
| Linear sum without lead-in | 1.805 against 1.29 | 0.805 + 1.0 |
| Lead-in capture radius, ICD U12 | 10 mm | Worst core top offset 7.5 + 0.805 + 1.0 = 9.31 mm < 10 mm, margin 0.69. Passes; the margin is thin. |
| Lead-in centring | plus or minus 0.25 mm | matches the 0.25 + 0.25 residual |
| Collet family | 7 collets, 2.5 mm; free bore d + 2; window d - 1.5 to d + 1.0; 12 slits at 1.5; clamped slit 0.584 | reply sec. 2 and numbers file 3.1 |
| Envelope | 85.0 to 106.585 | 108.585 - 1.0 - 1.0 |
| Gaps (decision 1, ICD context) | 13.126 / 1.5 / 8.59; holder bottom 2.00 and 0.50 | reply D-9 and sec. 2 |
| ICD keep-out, stop gap | 86.2; g_stop 10 | params.yaml |
| ICD heights | start_z 660 = 160 + 500; 800 = 300 + 500 | exact |
| ICD exposed core | 128.12 = 121.369 + 6.75; collar top 6.75 = 0.75 + 6.0 | 128.119 |
| ICD drill advance | 534.93 = 500 + 34.93; captured length 465.07 | params.yaml dome_pole_offset 34.9315 |
| ICD mounting, footprint | slot offset 15, pitch 30; 644 x 608 | params.yaml profile and icd |

Not mine, not checked: floor stress 2.3 MPa, mass and tip-over figures in decision 9.

## Release condition

Signature is given when W-1 and W-2 are corrected in step2_system_concept.md. Neither changes a design decision; both are figures that disagree with the window law or with arithmetic.

## Re-check (after Systems Engineer revision)

Verdict: WITHHELD, one line. W-1 and W-2 are closed; all else below matches.

| Item | Concept value | Result |
|---|---|---|
| W-1 grip window | d-1.5 to d+1.0, coverage 88.5 to 106.0 | CLOSED |
| W-2 slack at 106.585 | 0.50 per side, 1.00 diametral | CLOSED (107.585 core, (108.585-107.585)/2) |
| Datum B chain | 0.30 + 0.25 + 0.25 + 0.20 = 1.00; bore r 67.29 | matches (134.58 / 2) |
| Floor offset | 40 mm above datum A; core top about 790 at 0.75 m | matches (750 + 40) |
| Funnel bore | 56.0 against 55.06 required | matches (53 + 1.0 + 0.805 + 0.25 = 55.055); margin 0.94 |
| Capture radius | 10 mm | still passes (9.31 worst) |
| Steady rest detents | 310 and 560 mm above seat | matches: finger tip = core top + 60 - 250 = core top - 190 = 310 / 560 above seat for 500 / 750 mm cores |
| Park height | 950 mm | clears core top 790 + 50 = 840 by 110; the stated sum "collar top 150 + core 750 + 50" is not the geometry (the core stands on the floor, not on the collar), though the number is safe |
| Strap pull | 77 N for 153 N | 76.5 N, ideal 2:1 |
| Strap anchor 300 mm | 728 member | not contradicted; half-span 364 leaves 64 mm to the member end, so column centre spacing must be at least 334 + clearance. State column spacing. |
| Stop height note | seed 160 becomes about 170 | matches: highest clamped collar top 119.84 + 40 + 10 = 169.84 |

### Withheld line

Decision 9, "The collet has a 10 mm funnel chamfer matching the lead-in capture": 10 mm is wrong. Collet wall at the cone top is 5.0 mm at d = 105 (bore r 53.5, outer r 58.5), against `collet.min_wall` 1.2. Maximum radial chamfer is 5.0 - 1.2 = 3.8 mm at d = 105 (11.3 at d = 90); a 10 mm chamfer cuts through the wall. Correct to: funnel chamfer sized per collet to wall minus 1.2 (3.8 mm at d = 105, 1.5 mm x 45 deg stands as the minimum), with the 10 mm capture carried by the upper-assembly funnel (U12), not the collet.

Signature is given when that line is corrected.

## Re-check 2 (second revision)

Verdict: SIGNED. Every geometry number in decisions 2, 3, 4, 5, 7, 9 and the ICD rows now matches, and the earlier withheld line is closed. Arithmetic in `python -I`.

| Item | Concept value | Check |
|---|---|---|
| Collet bore chamfer | wall minus 1.2: 3.8 mm at d = 105, 11.3 at d = 90, 1.5 x 45 deg floor | 5.0 - 1.2 = 3.8; 12.5 - 1.2 = 11.3. CLOSED. 10 mm capture sits on the upper-assembly funnel only. |
| Column spacing | 548 mm rail centrelines, 488 mm clear | 488 + 60 = 548; 548 - 60 = 488; footprint 488 + 120 = 608 |
| Coaxiality chain | 0.32 + 0.20 + 0.20 + 0.15 = 0.87 against 1.0, margin 0.13 | 0.87 exact. The funnel check still uses the full 1.0 budget, so it stays conservative. |
| Rope crossing (reason for withdrawing the anchor) | 21 to 59 mm from axis at z 950, inside 88.9 mm cutter radius | 300 (950 - t) / (1600 - t): 59.3 at core top t = 790, 21.4 at t = 900 |
| Choke strap | 250 mm side handle at 0.55 L, rated 80 kg | handle radius 250 is above the 95 lug and the 125 rest clearance; 0.55 L is 275 / 412 mm above the seat |
| Rest release | lug radius 95, arm clears to 125 (30 mm outside lug), tower 250 | 125 - 95 = 30. Tower top = arm 310 + 40 + 250 = 600 and 560 + 40 + 250 = 850, equal to core top + 60 (540 + 60, 790 + 60). Detents 310 / 560 stand. |
| Park | 950 mm, 160 above the seated 790 core | 950 - 790 = 160 |
| Footprint, mass figures | unchanged | not re-opened |
