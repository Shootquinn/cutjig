"""Step 6 fix-pass params edit (single writer): changed values and sources, new keys, report_assumptions rows."""
import re
LF = "cr_scratch/step6_loftsman_fixpass.md"
OR = "Orchestrator ruling, Step 6 fix pass"
A, D = "ASSUMED", "DERIVED"
P = open("params.yaml", encoding="utf-8").read().split("\n")
R = open("report_assumptions.md", encoding="utf-8").read().split("\n")

def fmt(v):
    if isinstance(v, list):
        return "[" + ", ".join(str(x) for x in v) + "]"
    return str(v)

def leaf(key, val, unit, src, st):
    return '  %s: {value: %s, unit: "%s", source: "%s", status: %s}' % (key, fmt(val), unit, src, st)

def section_range(lines, sec):
    i = lines.index(sec + ":")
    j = i + 1
    while j < len(lines) and (lines[j].startswith("  ") or lines[j].strip() == ""):
        j += 1
    while lines[j - 1].strip() == "":
        j -= 1
    return i, j

def set_leaf(sec, key, val, unit, src, st):
    i, j = section_range(P, sec)
    for k in range(i, j):
        if P[k].startswith("  %s:" % key):
            P[k] = leaf(key, val, unit, src, st)
            return
    raise KeyError(sec + "." + key)

def add_leaf(sec, key, val, unit, src, st):
    i, j = section_range(P, sec)
    P.insert(j, leaf(key, val, unit, src, st))

def del_leaf(sec, key):
    i, j = section_range(P, sec)
    for k in range(i, j):
        if P[k].startswith("  %s:" % key):
            del P[k]
            return
    raise KeyError(key)

rows = {}
def rrow(label, st, src):
    rows[label] = "| `%s` | %s | %s |" % (label, st, src)

def change(sec, key, val, unit, src, st):
    set_leaf(sec, key, val, unit, src, st); rrow("%s.%s" % (sec, key), st, src)

def new(sec, key, val, unit, src, st):
    add_leaf(sec, key, val, unit, src, st); rrow("%s.%s" % (sec, key), st, src)

# ---- D3 nut NT4 glyph and NT8 parity
change("nut", "glyph_length", 10.0, "mm", f"tighten and loosen glyph length along its direction: shaft 4.2 + head 5.8 = wing 14 minus 2 x 2.0 walls = NT8 head length ({LF} D3)", A)
change("nut", "shaft_width", 2.7, "mm", f"glyph shaft width ({LF} D3)", A)
change("nut", "head_width", 8.3, "mm", f"glyph arrowhead width; radial window 95.64 (skirt 95.14 + 0.5) to 109.0 (tip fillet start) ({LF} D3)", A)
change("nut", "head_length", 5.8, "mm", f"glyph arrowhead length ({LF} D3)", A)
change("nut", "skirt_z_lo", 5.0, "mm", "dust skirt bottom, nut frame (cr_scratch/step6_loftsman_definition.md section 2); dust skirt, not the reading face (the reading face is nut z 0, witness.index_face_nut_z)", A)
new("nut", "release_shaft_width", 0.7, "mm", f"NT8 release arrow shaft width; NT8 recess area matched to the NT4 glyph recess area within 10 percent ({OR} item 3)", A)
new("nut", "release_head_width", 3.0, "mm", f"NT8 release arrowhead base width, radial ({OR} item 3)", A)
new("nut", "release_head_length", 4.0, "mm", f"NT8 release arrowhead length, tangential; shaft length follows from nut.release_dead_turn_deg ({OR} item 3)", A)
new("witness", "index_face_nut_z", 0.0, "mm", f"reading face: nut z 0, the skirt underside annulus r 73.54 to 83.14 (revolve starts at z 0) ({LF} D1)", D)
# ---- D2 rest
change("rest", "ring", [58, 100, 8], "mm", f"C-ring inner radius, outer radius, thickness; inner 58 keeps the roller pin span 59.255 to 78.005 clear of the bore ({LF} D2)", A)
change("rest", "roller_r", 70.005, "mm", f"roller centre radius at the pose core: pose_core_d/2 + rest.roller_dia/2 + fit.model_contact_gap ({LF} D2)", D)
new("rest", "pose_core_d", 100, "mm", f"core diameter of the modelled rest pose ({LF} D2)", A)
new("rest", "roller_r_range", [64.255, 73.005], "mm", f"roller centre radius travel for core d 88.5 to 106: 8.75 mm ({LF} D2)", D)
new("rest", "core_d_range", [88.5, 106.0], "mm", "core diameter range the rest grips: collet grip-window coverage 88.5 to 106.0 (collet.grip_window)", D)
new("rest", "slot_clear", 0.5, "mm", f"pin slot clearance per side in the ring (width) ({OR} item 2)", A)
new("rest", "slot_depth", 3.0, "mm", f"pin slot depth up from the ring bottom; the pin top fuses into the slot ceiling ({OR} item 2)", A)
# ---- D5 tray
change("tray", "floor_slope_deg", 2.0, "deg", f"floor fall to the drain along x, both directions from the drain (3.0 gives floor 26.53 at the wall, over 25) ({LF} D5)", A)
new("tray", "cross_fall_deg", 2.0, "deg", f"floor fall to the drain along y, both directions from the drain ({LF} D5)", A)
new("tray", "drain_spot_r", 20.0, "mm", f"spot face radius at the drain: flat at z floor_min under the plug flange, plug.flange_dia/2 17.5 + 2.5 ({LF} D5)", D)
del_leaf("tray", "ramp_x")
R = [l for l in R if not l.startswith("| `tray.ramp_x`")]
new("tray", "fall_x", [-277, 277], "mm", f"floor fall x extent, inner wall to inner wall: tray.length/2 - tray.wall, replaces tray.ramp_x ({LF} D5)", A)
# ---- D6 plug
new("plug", "lug_length", 34, "mm", f"plug grip lug length along X ({LF} D6)", A)
new("plug", "lug_width", 8, "mm", f"plug grip lug width ({LF} D6)", A)
new("plug", "lug_height", 10, "mm", f"plug grip lug height above the head top ({LF} D6)", A)
new("plug", "lug_embed", 1.0, "mm", f"plug grip lug embed into the head ({LF} D6)", A)

# report rows: replace existing, append new
for label, line in rows.items():
    hit = [k for k, l in enumerate(R) if l.startswith("| `%s` |" % label)]
    if hit:
        R[hit[0]] = line
last = max(k for k, l in enumerate(R) if l.startswith("| `") )
for label, line in rows.items():
    if not any(l.startswith("| `%s` |" % label) for l in R):
        last += 1
        R.insert(last, line)
open("params.yaml", "w", encoding="utf-8", newline="\n").write("\n".join(P))
open("report_assumptions.md", "w", encoding="utf-8", newline="\n").write("\n".join(R))
print("ok")
