"""One-shot params pass for Step 6 (single writer). Inserts new leaves into params.yaml and rows into report_assumptions.md."""
import json
import re
import sys

sys.path.insert(0, ".")
from build_parts import common  # noqa: E402

LD = "research/quinn/cr_scratch/step6_loftsman_definition.md"


def L(sec):
    return f"{LD} section {sec}"


A, D, DR = "ASSUMED", "DERIVED", "DECLARED"
TOP = "research/quinn/cr_scratch/step6_topologist_crossreview.md section 5"
NEW = {
    "witness": [
        ("azimuth_deg", 127, "deg", f"receiver.key_offset_deg 37 + 90: reader faces the ruler 90 deg from the key slot ({L(1)})", A),
        ("channel_width", 12.0, "mm", f"ruler channel width, tangential ({L(1)})", A),
        ("channel_floor_depth", 0.30, "mm", f"channel floor plane lies thread.minor/2 - 0.30 = 71.99 from the axis: 0.05 to 0.30 under the root cylinder across the width, no tangency ({L(1)})", A),
        ("line_height", 0.4, "mm", f"graduation line height, axial ({L(1)})", A),
        ("line_depth", 0.5, "mm", f"graduation line depth below the channel floor ({L(1)})", A),
        ("band_depth", 0.3, "mm", f"wrong-collet band depth below the channel floor ({L(1)})", A),
        ("tick_width", 1.0, "mm", f"holder flange tick groove width, tangential ({L(1)})", A),
        ("tick_depth", 2.0, "mm", f"holder flange tick groove depth, radial from the flange OD ({L(1)})", A),
        ("tick_height", 3.0, "mm", f"holder flange tick groove height above the flange underside ({L(1)})", A),
        ("channel_z", [47.0, 63.0], "mm", f"ruler channel z range in the receiver frame: graduation 0 at 48.5 minus 1.5, top 1.374 above the wrong-collet band top 61.626 ({L(1)})", A),
        ("line_length", 4.0, "mm", f"graduation line length, tangential, centred on witness.azimuth_deg ({L(1)})", A),
        ("line_length_major", 5.2, "mm", f"graduation line length at every witness.major_every ({L(1)})", A),
        ("major_every", 5, "", f"major graduation and digit every 5th line ({L(1)})", A),
        ("band_t", [-5.6, -3.8], "mm", f"wrong-collet band strips, tangential range left of the line (t = z x r) ({L(1)})", A),
        ("digit_t", [2.6, 5.6], "mm", f"digit pockets, tangential range right of the line ({L(1)})", A),
        ("digit_height", 3.0, "mm", f"digit pocket height, axial ({L(1)})", A),
        ("digit_z_shift", 0.2, "mm", f"digit pocket centre above its line z so no pocket face meets the channel floor edge z 47.0 ({TOP})", A),
    ],
    "nut": [
        ("glyph_length", 6.0, "mm", f"tighten and loosen glyph length along its direction: shaft 2.5 + head 3.5 ({L(2)})", A),
        ("shaft_width", 1.6, "mm", f"glyph shaft width ({L(2)})", A),
        ("head_width", 5.0, "mm", f"glyph arrowhead width ({L(2)})", A),
        ("head_length", 3.5, "mm", f"glyph arrowhead length ({L(2)})", A),
        ("skirt_r_out", 95.14, "mm", f"dust skirt outer radius = wingnut.body_od/2 83.14 + 12 ({L(2)})", D),
        ("skirt_z_lo", 5.0, "mm", f"dust skirt bottom, nut frame ({L(2)})", A),
        ("skirt_z_hi", 14.0, "mm", f"dust skirt top, 2 below the wing underside z 16 ({L(2)})", A),
        ("skirt_rim", 2.0, "mm", f"dust skirt vertical rim height at the outer radius ({L(2)})", A),
        ("skirt_embed", 1.0, "mm", f"dust skirt embed into the nut body so the fuse shares volume ({L(2)})", A),
    ],
    "base": [
        ("slot_centres", [[-255, 289], [-90, 289], [75, 289], [240, 289], [-240, -289], [-75, -289], [90, -289], [255, -289]], "mm",
         f"slot centres (x, y), long axis X; pattern is not symmetric under a flip about X or Y ({L(3)})", A),
        ("key_pocket_xy", [160, 259], "mm", f"plate key pockets at (+-x, y), underside; y is the datum C slot line ({L(3)})", A),
        ("pin_pocket_xy", [249, 0], "mm", f"stop pin pocket centre; wall x 244.0 touches the pin (contact intended) ({L(3)})", A),
        ("drain_xy", [-172, 0], "mm", f"drain hole and tray drain centre ({L(3)})", A),
        ("column_notch", [70, 65], "mm", f"plate edge notch at each column: width, depth from the long edge ({L(3)})", A),
        ("column_notch_x", 35, "mm", f"column notch centre x (+-) ({L(3)})", A),
        ("key_pocket_size", 12, "mm", f"key pocket square, key 11.5 with 0.25 per side ({L(3)})", A),
        ("pocket_depth", 4, "mm", f"underside pocket depth ({L(3)})", A),
        ("pin_pocket_size", [10, 14], "mm", f"stop pin pocket x, y ({L(3)})", A),
        ("drain_hole_dia", 26, "mm", f"plate drain hole, 0.5 radial over tray.drain_dia 25 ({L(3)})", A),
    ],
    "tray": [
        ("wall", 3, "mm", f"tray wall ({L(3)})", A),
        ("floor_min", 3, "mm", f"tray floor thickness at the drain end ({L(3)})", A),
        ("ramp_x", [-172, 81], "mm", f"floor ramp x range: 253 x tan(tray.floor_slope_deg) = 13.26 rise; 3 deg over the full 560 would rise 29.3, over the 25 depth ({L('Corrections C3')})", A),
        ("hole_r", 81.2, "mm", f"tray hole for the receiver spigot, 1.0 over receiver.spigot_od/2 ({L(3)})", A),
        ("relief", [72, 19], "mm", f"column relief at each long edge: width, depth inward from the edge, y 241 to 260 ({L(3)}; {TOP})", A),
    ],
    "frame": [
        ("end_x", 232, "mm", f"end member centre x (+-) ({L(4)})", A),
        ("support_x", 112, "mm", f"plate support centre x (+-) ({L(4)})", A),
        ("notch", [20, 30, 2], "mm", f"datum C slot-line notch on one rail: across, along, depth ({L(4)})", A),
    ],
    "bracket": [
        ("holes_purchased", [13.9, 43.1], "mm", f"purchased bracket hole positions along the leg ({L(4)})", A),
        ("slots_printed", [19.4, 48.6], "mm", f"printed bracket slot centres along the leg ({L(4)})", A),
        ("slot_lengths_printed", [11.0, 10.0], "mm", f"printed bracket slot overall lengths at slots_printed; hardware.printed_bracket_slot_width is the width ({L(4)})", A),
        ("purchased_leg", 57, "mm", f"purchased bracket leg ({L(4)})", A),
        ("purchased_plate", 6, "mm", f"purchased bracket plate ({L(4)})", A),
        ("printed_leg", 68, "mm", f"printed bracket leg ({L(4)})", A),
        ("printed_plate", 7, "mm", f"printed bracket plate ({L(4)})", A),
        ("width", 57, "mm", f"bracket width across the profile face ({L(4)})", A),
        ("hole_dia", 6.6, "mm", f"purchased bracket clearance hole for M6 ({L(4)})", A),
        ("across", 15, "mm", f"hole and slot offset across the leg from the bracket centre line ({L(4)})", A),
    ],
    "caddy": [
        ("web", 8, "mm", f"wall between sockets ({L(5)})", A),
        ("border", 10, "mm", f"border outside the outer sockets ({L(5)})", A),
        ("floor", 6, "mm", f"floor under the sockets ({L(5)})", A),
        ("row_spacing", 133.4, "mm", f"row spacing, staggered rows of 4 and 3 at pitch 154.08 ({L(5)})", A),
        ("rows", [4, 3], "", f"sockets per row; sum equals collets.count ({L(5)})", A),
        ("label_width", 30, "mm", f"size label recess width; height collet.label_height, depth collet.label_depth ({L(5)})", A),
        ("label_gap", 1.0, "mm", f"size label recess edge off the socket wall ({TOP})", A),
    ],
    "gauge": [
        ("cavity", [110, 130], "mm", f"cavity diameter and depth from below ({L(5)})", A),
        ("handle", [160, 25, 25], "mm", f"handle bar on top: length, width, height ({L(5)})", A),
    ],
    "rest": [
        ("ring", [62, 100, 8], "mm", f"C-ring inner radius, outer radius, thickness ({L(5)})", A),
        ("roller_r", 70, "mm", f"roller centre radius from the core axis ({L(5)})", A),
        ("pin", 10, "mm", f"roller pin diameter; the pin bridges the 0.5 gap to the ring ({L(5)})", A),
        ("mouth_deg", 90, "deg", f"C-ring mouth, centred on -X ({L(5)})", A),
        ("block", [60, 30, 60], "mm", f"column block x, y, z; interface plane at the column face ({L(5)})", A),
        ("hinge_boss_dia", 40, "mm", f"hinge boss at y = rest.arm_length ({L(5)})", A),
        ("arm", [20, 24], "mm", f"arm width and height to the ring ({L(5)})", A),
        ("roller_height", 30, "mm", f"roller height, centred on the roller plane z = 0 ({L(5)})", A),
        ("ring_z_lo", 15.5, "mm", f"C-ring bottom: roller top 15 + rest.roller_pin_gap 0.5 ({L(5)})", A),
        ("roller_pin_gap", 0.5, "mm", f"axial gap between roller top and ring ({L(5)})", A),
        ("handle_dia", 20, "mm", f"close handle diameter; length rest.close_handle_length ({L(5)})", A),
        ("detent_depth", 4, "mm", f"detent notch depth in the boss at 90 deg swing ({L(5)})", A),
        ("detent_width", 8, "mm", "detent notch width, tangential on the boss (Step 6 Pass 1 assumption, Step 9 refines)", A),
        ("tower", [14, 16], "mm", f"release tower tangential width and radial depth ({L(5)})", A),
        ("tower_inboard_r", 84, "mm", f"release tower inboard face radius ({L(5)})", A),
    ],
    "stop": [
        ("pad_thickness", 12, "mm", f"stop pad thickness below stop.height_z ({L(5)})", A),
        ("pad_xy", [0, 214], "mm", f"stop pad centre; y = column face 244 - stop.pad_length/2 ({L(5)})", A),
        ("pad_hole_dia", 6.6, "mm", "stop pad M6 clearance holes, two at x = +-stop.pad_hole_x, so the pad carries a boolean record (data71) (Step 6 Pass 1 assumption)", A),
        ("pad_hole_x", 15, "mm", "stop pad hole offset from the pad centre, equal to profile.slot_offset (Step 6 Pass 1 assumption)", A),
    ],
}
NEWGROUPS = {
    "plug": [
        ("head_dia", 40, "mm", f"drain plug head ({L(3)})", A), ("head_h", 14, "mm", f"drain plug head height ({L(3)})", A),
        ("flange_dia", 35, "mm", f"drain plug flange ({L(3)})", A), ("flange_t", 2, "mm", f"drain plug flange thickness ({L(3)})", A),
        ("shank_dia", 24, "mm", f"drain plug shank, 0.5 radial clearance in tray.drain_dia 25 ({L(3)})", A),
        ("shank_h", 3, "mm", f"drain plug shank length = tray.floor_min ({L(3)})", A)],
    "foot": [
        ("size", [100, 60, 8], "mm", f"bolt-down foot plate x, y, z ({L(3)})", A),
        ("m6_xy", [30, 15], "mm", f"M6 holes at (x, +-y), slot pitch 30 ({L(3)})", A),
        ("m6_hole", 6.6, "mm", f"M6 clearance hole ({L(3)})", A),
        ("m8_x", 88, "mm", f"M8 floor fastener hole x, 28 from the rail end ({L(3)})", A),
        ("m8_hole", 9, "mm", f"M8 clearance hole ({L(3)})", A)],
    "tnut": [
        ("body", [16, 16, 6.0], "mm", f"T-nut proxy body: across, along, height; PZRT 3030 has no CAD on disk ({L(4)})", A),
        ("neck", [7.6, 12, 2.2575], "mm", f"T-nut proxy neck: across, along, height = profile.slot_neck_depth ({L(4)})", A),
        ("hole", 5.0, "mm", f"T-nut proxy tapped hole, M6 tap drill region ({L(4)})", A),
        ("chamfer", 3.5, "mm", f"T-nut proxy long bottom edges chamfered 3.5 x 45 deg ({TOP})", A)],
}


def line(k, v, u, s, st):
    return f'  {k}: {{value: {json.dumps(v)}, unit: "{u}", source: "{s}", status: {st}}}'


txt = open("params.yaml", encoding="utf-8").read().split("\n")
out = []
for ln in txt:
    out.append(ln)
    m = re.match(r"^([a-z_]+):\s*$", ln)
    if m and m.group(1) in NEW:
        out += [line(*k) for k in NEW[m.group(1)]]
text = "\n".join(out)
if not text.endswith("\n"):
    text += "\n"
for g, ks in NEWGROUPS.items():
    text += "\n" + g + ":\n" + "\n".join(line(*k) for k in ks) + "\n"
open("params.yaml", "w", encoding="utf-8").write(text)

p = common.load_params()
rows = []
for g, ks in list(NEW.items()) + list(NEWGROUPS.items()):
    for k, v, u, s, st in ks:
        if st in (A, DR):
            rows.append(f"| `{g}.{k}` | {st} | {s} |")
rep = open("report_assumptions.md", encoding="utf-8").read()
c = common.status_counts(p)
rep = re.sub(r"Counts: .*", f"Counts: DECLARED {c['DECLARED']}, ASSUMED {c['ASSUMED']}, VERIFIED {c['VERIFIED']}, DERIVED {c['DERIVED']}, total {c['total']}", rep, count=1)
rl = rep.split("\n")
last = max(i for i, l in enumerate(rl) if l.startswith("| `"))
rl[last + 1:last + 1] = rows
rep = "\n".join(rl)
open("report_assumptions.md", "w", encoding="utf-8").write(rep)
print("leaves", c)
