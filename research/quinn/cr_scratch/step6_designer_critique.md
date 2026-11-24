## Gate status

visual gate RUN. 101 of 101 PNGs read. Unreadable: none.

## 1. Checklist verdicts

| ID | Verdict | PNG |
|---|---|---|
| RC1, RC2 | PRESENT | receiver_front, receiver_rim_scale_context |
| RC3, RC4 | PRESENT | receiver_top (floor annulus, register bore) |
| RC5 | PRESENT | receiver_top (slot at upper right of bore) |
| RC6 / AC4 | PRESENT; reading FAILS in context (section 3) | receiver_rim_scale_closeup, _oblique, witness_Kd1_closeup |
| HD1-HD4 | PRESENT | holder_iso, holder_top (4 insert bores) |
| HD5, HD6 | PRESENT by absence | holder_bottom, holder_tick_below |
| HD7 / AC5 | PRESENT | holder_tick_closeup, holder_tick_oblique, holder_front |
| WS1, WS2 | PRESENT | washer_top, washer_iso |
| WS3 | SIMPLIFIED: pads on nut face, washer not shown seated | nut_bottom |
| CO1-CO8 | PRESENT, 3 sizes | collet_*_iso, _section, _top |
| NT1-NT3 | PRESENT | nut_iso, nut_front, nut_skirt_section |
| NT4, NT5 | PRESENT, readable | nut_glyph_*, nut_wing0_*, nut_top, nut_bottom |
| NT6 | PRESENT | nut_front |
| NT7 | PRESENT | nut_skirt_section, nut_skirt_below, nut_front |
| NT8 | PRESENT | nut_top |
| NT9 | FAIL at K-max | witness_Kmax_view, witness_Kmax_closeup |
| BS1-BS4 | PRESENT | base_top, base_bottom (2 key pockets, pin pocket), base_iso |
| BS5 | PRESENT | base_tray_section, tray_ramp_section |
| BS6 | SIMPLIFIED: plain bore, puck plug | base_tray_drain_section |
| BS7 | PRESENT | foot_iso, foot_top |
| FR1, FR4 | PRESENT | frame_top, frame_notch_iso |
| FR2 | PRESENT; overlap at 4 sites visible (Step 7) | frame_top, frame_iso |
| FR3 | PRESENT, 8 per bracket | frame_tnuts_closeup |
| AC1 | PRESENT | caddy_iso, caddy_top |
| AC2 | PRESENT | gauge_iso, gauge_top |
| AC3 | PRESENT; roller radius fix pending | rest_iso, rest_top, rest_front |
| ST1 | PRESENT | stop_iso |

## 2. Nut glyphs

Both on wing 0 (+X). NT4, top face: arrow points toward -Y. At +X, motion toward -Y is clockwise seen from above. NT5, underside: in the from-below view (+Y up) the arrow points toward +Y; at +X, motion toward +Y is counter-clockwise seen from above. Recess walls read in the oblique views. At full-nut scale (nut_top, nut_bottom) each glyph is about 50 px and readable.

## 3. Witness

Line of sight: horizontal, at azimuth 127, onto the receiver ruler below the nut. The index the reader sees is the lowest nut face.

- K-max (witness_Kmax_view, _closeup): the nut body (nut z 0 to 5) covers the whole ruler. The reader sees the nut body and thread, and no graduation. 1.5 cannot be read.
- K d+1 (witness_Kd1_view, _closeup): four graduations and the lower band strip show below the nut body bottom. The visible edge sits 5 mm below the declared edge: a reader counts about 3.6, against the intended 8.59.
- Cause: the declared index is nut z 5 (skirt bottom), but the nut body runs 5 mm lower at r 83.14, which sits outside the ruler at r 72. The probe readings (1.525, 8.615) use the declared face, which the eye never sees.
- Bands: in receiver_rim_scale_closeup the lower band (48.5 to 50) and upper band (57.09 to 61.63) show as strips left of the graduations, set apart by shape. At witness_*_view scale the ruler is about 100 px, and zone and bands cannot be told apart by edge lines alone.

## 4. Collets 90, 97.5, 105

Slits, relief holes, foot key, core stop, lead-in chamfer and label recess are visible at all three sizes. Rim notch count reads 1, 4, 7 (collet_*_top). Wall and bore change with size in the sections. The label recess is blank (text in JSON). Render colours (blue, green, gold) are render assignments and do not follow the size colour record.

## 5. Design Critique

| # | Item | Type | Tag |
|---|---|---|---|
| D1 | Witness index hidden at K-max and offset 5 mm at K d+1. Engineer checks the render pose against the built nut and holder. If the pose is right, the index is the nut z 0 face: the Loftsman moves ruler zero to that face (graduation 0 at z 43.5 for the same g) or trims the nut body below the skirt. Re-render witness_Kmax/Kd1 view and closeup, and re-read the probe on the visible face | functional | BLOCK |
| D2 | Steady-rest rollers fit only d 100 (ruled; fix pass) | functional | BLOCK |
| D3 | The top face carries the large NT8 release arrow (counter-clockwise) next to the small NT4 tighten arrow (clockwise). The dominant top signifier says loosen. Scale NT4 up to the 21.86 band, or move NT8 off the top | functional | CARRY |
| D4 | Ruler, bands and digit pockets share the part colour, and the digits are blank. Fill colour or deepen the band strips; engrave 0, 5, 10 | aesthetic | CARRY |
| D5 | Tray floor is level from x 81 to the +X wall. Debris on that shelf does not run to the drain. Extend the fall to the wall | functional | CARRY |
| D6 | Plug is a plain puck with nothing to grip. Add a bar or knurl so it reads as removable | pride | CARRY |
| D7 | Caddy sockets are 40 deep in a 46 block with no lift relief and no key slot. Add a side relief per socket and a key notch that sets orientation | functional | CARRY |
| D8 | Gauge form reads correctly: plug, key, handle bar | none | none |
| D9 | Rest reads as a C-clamp on an arm. The tower post dominates the ring at 250 tall. The hold-open detent notch is visible only in rest_top. Mark the open and closed positions on the boss | spatial | CARRY |
| D10 | Stop pad is a bare block, acceptable as an interface item | none | none |
| D11 | base_slots_closeup frames slots and the tray edge, not the key pocket and notch named in the index; base_bottom covers BS4 | clerical | none |

## 6. Fix-pass re-read list

witness_Kmax_view, witness_Kmax_closeup, witness_Kmax_section, witness_Kd1_view, witness_Kd1_closeup, witness_Kd1_section, rest_iso, rest_iso_back, rest_top, rest_front, plus any receiver or nut render changed by D1.

## Re-gate

Read: witness_* (6), rest_iso, rest_top, rest_bottom, rest_slot_closeup, nut_top, nut_glyph_nt4_top, nut_glyph_nt4_oblique, nut_glyph_nt5_under, nut_wing0_top, tray_top, tray_iso, tray_front, tray_ramp_section, tray_cross_section, plug_iso, plug_front, plug_top, base_tray_iso, base_tray_drain_section.

| ID | Verdict | Evidence |
|---|---|---|
| D1 | PASS | witness_Kmax_closeup: nut z 0 edge forms a straight index line across the ruler window; below it one long line (k 0) and one short line (k 1), lower band strip at left and right. Reads 1.5. witness_Kd1_closeup: nine lines below the index, long at k 0 and k 5, short between; upper band strips flank the zone. Reads about 8.6. Sections show the nut flange clear of the ruler face in both poses. At witness_*_view scale the window is about 70 px; legibility at that scale rests on D4 fill (carried). |
| D2 | PASS | rest_bottom: three rollers ride on the ring bore at the pose radius. rest_slot_closeup: radial slot about 1.9 pin diameters long, pin centred, travel visible. Adjustment present. |
| D3 | PASS | nut_top: NT4 is a solid 10 mm block arrow on wing 0; NT8 is now a hairline arc with a small head. NT4 is the heavier mark; the top face no longer reads as loosen first. NT4 and NT5 point opposite senses (nut_glyph_nt4_top, nut_glyph_nt5_under). |
| D5 | PASS | tray_top and tray_iso: four hip lines meet at the drain spot face; no level shelf. tray_ramp_section and tray_cross_section: floor falls to the drain from both walls on both axes. |
| D6 | PASS | plug_iso, base_tray_iso: bar lug across the head reads as a grip; plug reads as removable from the tray iso. base_tray_drain_section: lug clear of the tray floor. |

New, non-blocking, Step 9:

| # | Item | Type | Tag |
|---|---|---|---|
| D12 | Rest roller pin has no visible lock or radius mark; the slot sits under the roller (rest_bottom). Mark the pose radius per core size on the ring face or a pin-side index | functional | CARRY |
| D13 | NT8 shaft 0.7 is under two 0.4 nozzle widths and narrower than the 0.8 mark line; the arc may print as a broken groove | functional | CARRY |

Gate: PASS. D1 and D2 cleared. Carried: D4, D7, D9, D12, D13.
