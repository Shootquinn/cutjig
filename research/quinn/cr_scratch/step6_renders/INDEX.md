## Conventions

Renderer: freecadcmd 1.1.4 with `Gui.showMainWindow()`, orthographic camera, Flat Lines, background RGB 204/207/212, 1600 x 1200. Shapes read from `parts_cache` BREP exports; no FCStd or test modified. Part poses are as built (local frame) except the witness, base and frame renders. Views: iso camera at +X -Y +Z; top looks down with +Y up; front looks along +Y with +X right; bottom looks up with +Y up (X mirrored). Colours: one per part; frame members grey, purchased brackets black, printed brackets pink, T-nut proxies orange. Sections remove the half-space on the viewer side of the plane. Thin parts read under 5 percent coverage by geometry (ring or plate seen edge-on): base_front, footring_front, tray_front, tray_ramp_section, washer_front, washer_iso, washer_top.

Fix pass: witness renders place the nut origin at the edge z (nut z 0, the reading face, annulus r 73.54 to 83.14) and the holder origin at edge + 40 - 88, receiver at the origin (edge 50.00 at K-max, 57.09 at K d+1). Re-rendered after the fix pass: all witness_*, nut_*, rest_*, tray_*, plug_*, base_tray_* PNGs; added rest_bottom, rest_slot_closeup, tray_cross_section.

Receiver ruler and holder tick close-ups use the part colour; legibility rests on edge lines (0.4 mm graduations, 1.0 mm tick). Oblique views add recess-wall shading.

## Index

| Path | Part | View | Checklist IDs | Coverage % |
|---|---|---|---|---|
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\base_bottom.png | base | underside, key and pin pockets | BS4 | 62.9 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\base_front.png | base | front | BS1-BS4 | 2.2 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\base_iso.png | base | iso | BS1-BS4 | 32.2 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\base_slots_closeup.png | base | slotted mounting holes at +Y edge, key pocket and column notch region, top | BS3 BS4 | 67.7 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\base_slots_closeup_iso.png | base | mounting slots and column notch, oblique | BS3 BS4 | 38.4 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\base_top.png | base | top | BS1-BS4 | 62.9 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\base_tray_drain_section.png | base+tray+plug | section at y=0, drain and plug close-up | BS6 BS2 | 55.1 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\base_tray_drain_top.png | base+tray+plug | drain and plug close-up, top | BS2 BS6 | 11.8 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\base_tray_front.png | base+tray+plug | front | BS1 BS5 | 5.8 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\base_tray_iso.png | base+tray+plug | iso, base with tray and drain plug | BS1 BS5 BS6 | 32.5 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\base_tray_relief_closeup.png | base+tray+plug | column relief at +Y edge, top oblique | BS5 BS4 | 59.7 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\base_tray_section.png | base+tray+plug | section at y=0 viewed from -Y: ramp rise, cavity, drain bore, plug | BS5 BS6 BS2 | 5.8 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\base_tray_top.png | base+tray+plug | top, tray ramp, drain, reliefs, slots | BS2-BS6 | 63.1 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\bracket_printed_front.png | bracket_printed | front | FR2 | 71.9 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\bracket_printed_iso.png | bracket_printed | iso | FR2 | 25.1 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\bracket_printed_top.png | bracket_printed | top | FR2 | 12.6 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\bracket_purchased_front.png | bracket_purchased | front | FR2 | 61.7 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\bracket_purchased_iso.png | bracket_purchased | iso | FR2 | 23.8 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\bracket_purchased_top.png | bracket_purchased | top | FR2 | 12.9 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\caddy_front.png | caddy | front | AC1 | 8.5 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\caddy_iso.png | caddy | iso | AC1 | 35.5 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\caddy_top.png | caddy | top | AC1 | 54.6 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\collet_090p0_iso.png | collet_090p0 | iso | CO1-CO8 | 27.3 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\collet_090p0_section.png | collet_090p0 | section through slit plane az 52 deg, viewed from the cut side | CO3 CO4 CO2 | 17.1 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\collet_090p0_top.png | collet_090p0 | top | CO3 CO5 CO7 | 29.4 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\collet_097p5_iso.png | collet_097p5 | iso | CO1-CO8 | 26.2 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\collet_097p5_section.png | collet_097p5 | section through slit plane az 52 deg, viewed from the cut side | CO3 CO4 CO2 | 17.1 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\collet_097p5_top.png | collet_097p5 | top | CO3 CO5 CO7 | 25.7 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\collet_105p0_iso.png | collet_105p0 | iso | CO1-CO8 | 25.3 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\collet_105p0_section.png | collet_105p0 | section through slit plane az 52 deg, viewed from the cut side | CO3 CO4 CO2 | 17.0 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\collet_105p0_top.png | collet_105p0 | top | CO3 CO5 CO7 | 21.7 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\foot_front.png | foot | front | BS7 | 9.3 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\foot_iso.png | foot | iso | BS7 | 37.6 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\foot_top.png | foot | top | BS7 | 67.2 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\footring_front.png | footring | front | CO foot ring seat | 2.0 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\footring_iso.png | footring | iso | CO foot ring seat | 16.7 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\footring_top.png | footring | top | CO foot ring seat | 30.0 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\frame_bottom.png | frame | from below | FR1 FR2 FR3 | 35.3 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\frame_brackets_closeup.png | frame | brackets and T-nuts, corner +X +Y, iso close-up | FR2 FR3 | 85.3 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\frame_brackets_closeup_under.png | frame | brackets and T-nuts, corner +X +Y, from below | FR2 FR3 | 61.4 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\frame_front.png | frame | front (members grey, purchased brackets black, printed brackets pink, T-nut proxies orange) | FR1 FR2 FR3 | 10.8 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\frame_iso.png | frame | iso (members grey, purchased brackets black, printed brackets pink, T-nut proxies orange) | FR1 FR2 FR3 | 30.9 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\frame_notch_iso.png | frame | FR4 datum C notch, rail_1, oblique close-up | FR4 | 50.6 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\frame_notch_top.png | frame | FR4 datum C notch, rail_1, top close-up | FR4 | 58.4 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\frame_tnuts_closeup.png | frame | brackets and T-nut proxies only (members hidden), corner +X +Y, iso | FR2 FR3 | 29.3 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\frame_top.png | frame | top (members grey, purchased brackets black, printed brackets pink, T-nut proxies orange) | FR1 FR2 FR3 | 35.3 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\gauge_front.png | gauge | front | AC2 | 50.8 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\gauge_iso.png | gauge | iso | AC2 | 23.9 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\gauge_top.png | gauge | top | AC2 | 53.1 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\holder_bottom.png | holder | from below | HD5 HD6 HD7 | 19.3 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\holder_front.png | holder | front | HD1-HD7 AC5 | 77.9 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\holder_iso.png | holder | iso | HD1-HD7 AC5 | 31.2 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\holder_tick_below.png | holder | HD7 tick from below, flange underside, radial up | HD7 HD5 HD6 | 47.9 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\holder_tick_closeup.png | holder | HD7 tick at az 127 deg on the flange rim, radial view | HD7 AC5 | 88.0 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\holder_tick_oblique.png | holder | HD7 tick, oblique from below and outside | HD7 | 90.6 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\holder_top.png | holder | top | HD1-HD7 AC5 | 19.3 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\nut_bottom.png | nut | from below | NT2 NT5 NT7 | 26.4 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\nut_front.png | nut | front | NT1-NT8 | 25.2 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\nut_glyph_nt4_oblique.png | nut | NT4 glyph, oblique 35 deg for recess walls | NT4 | 35.1 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\nut_glyph_nt4_top.png | nut | NT4 tighten glyph close-up, normal to face, +Y up | NT4 | 87.6 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\nut_glyph_nt5_oblique.png | nut | NT5 glyph, oblique 35 deg for recess walls | NT5 | 86.2 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\nut_glyph_nt5_under.png | nut | NT5 loosen glyph close-up from below, +Y up | NT5 | 87.6 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\nut_iso.png | nut | iso | NT1-NT8 | 26.0 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\nut_skirt_below.png | nut | dust skirt from below and outside, -Y side | NT7 | 47.4 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\nut_skirt_section.png | nut | section at x=0, skirt profile on the -Y side, viewed from +X | NT7 | 30.2 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\nut_top.png | nut | top: NT4 glyph (10 mm) and NT8 release arrow (area matched) on wing 0 and the top face | NT4 NT8 NT1-NT3 NT6 | 26.4 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\nut_wing0_top.png | nut | wing 0 top face, NT4 glyph, normal to face | NT4 | 43.1 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\nut_wing0_under.png | nut | wing 0 underside, NT5 glyph, normal to face (viewed from below, +Y up) | NT5 | 31.1 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\plug_front.png | plug | front | BS6 | 74.6 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\plug_iso.png | plug | iso | BS6 | 25.3 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\plug_top.png | plug | top | BS6 | 50.5 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\receiver_bottom.png | receiver | from below | RC3 RC4 | 38.0 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\receiver_front.png | receiver | front | RC1-RC6 AC4 | 77.5 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\receiver_iso.png | receiver | iso | RC1-RC6 AC4 | 31.6 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\receiver_rim_scale_closeup.png | receiver | RC6 ruler at az 127 deg, radial view, z 44 to 68 | RC6 AC4 | 51.2 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\receiver_rim_scale_context.png | receiver | RC6 ruler in context, whole upper receiver, radial view at az 127 | RC6 RC5 RC1 | 63.4 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\receiver_rim_scale_oblique.png | receiver | RC6 ruler, oblique 30 deg about the axis | RC6 AC4 | 29.8 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\receiver_top.png | receiver | top | RC1-RC6 AC4 | 38.0 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\rest_bottom.png | rest | from below, ring and rollers (slots hidden behind the rollers) | AC3 | 12.6 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\rest_front.png | rest | front | AC3 | 9.0 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\rest_iso.png | rest | iso | AC3 | 7.8 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\rest_iso_back.png | rest | iso from the opposite corner | AC3 | 7.8 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\rest_slot_closeup.png | rest | section at z 17 viewed from above: radial pin slot at azimuth 0, roller pin at the pose radius 70.005 | AC3 | 68.9 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\rest_top.png | rest | top | AC3 | 12.6 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\stop_front.png | stop | front | ST1 | 23.0 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\stop_iso.png | stop | iso | ST1 | 46.3 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\stop_top.png | stop | top | ST1 | 63.2 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\tnut_front.png | tnut | front | FR3 | 55.1 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\tnut_iso.png | tnut | iso | FR3 | 36.2 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\tnut_top.png | tnut | top | FR3 | 59.5 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\tray_cross_section.png | tray | section at the drain x = -172 viewed from -X: cross fall to the drain, y -257 to 257 | BS5 | 5.6 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\tray_front.png | tray | front | BS5 | 4.9 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\tray_iso.png | tray | iso | BS5 | 33.6 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\tray_ramp_section.png | tray | section at y=0 viewed from -Y: floor falls to the drain both ways, x -277 to 277 | BS5 | 4.9 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\tray_top.png | tray | top | BS5 | 63.7 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\washer_front.png | washer | front | WS1-WS3 | 1.1 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\washer_iso.png | washer | iso | WS1-WS3 | 3.2 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\washer_top.png | washer | top | WS1-WS3 | 4.5 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\witness_Kd1_closeup.png | witness | line of sight close-up, nut z 0 reading face against ruler graduations, eye level | RC6 HD7 NT7 NT9 | 99.5 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\witness_Kd1_section.png | witness | section through the axis at az 127, ruler and nut profile, viewed from the cut side | RC6 HD7 NT7 NT9 | 56.2 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\witness_Kd1_view.png | witness | receiver, holder, nut at Kd1: edge z 57.09 = nut z 0, horizontal line of sight at az 127 | RC6 HD7 NT7 NT9 | 51.1 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\witness_Kmax_closeup.png | witness | line of sight close-up, nut z 0 reading face against ruler graduations, eye level | RC6 HD7 NT7 NT9 | 99.5 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\witness_Kmax_section.png | witness | section through the axis at az 127, ruler and nut profile, viewed from the cut side | RC6 HD7 NT7 NT9 | 56.9 |
| C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders\witness_Kmax_view.png | witness | receiver, holder, nut at Kmax: edge z 50.00 = nut z 0, horizontal line of sight at az 127 | RC6 HD7 NT7 NT9 | 48.9 |

PNG count: 104
