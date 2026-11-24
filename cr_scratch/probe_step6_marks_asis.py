"""Step 6 marks: nut glyph sense and witness scale/tick. Rule M: everything is read from the built solids.
Writes results/probes/step6_marks.json:
  glyphs   [{wing, face, count, span, direction_sign}]  wing 0 is +X, wing 1 is -X; face in +y -y +z -z; a glyph is a recess of at least
           nut.arrow_depth / 2 below the median wing-face surface of its x column; direction_sign from glyph_math.analyze (+1 counter-clockwise from +Z)
  witness  {az, rim_top_z, marks_z[], holder_under_local_z, tick_local_z, tick_count}
           marks_z: z centres where the receiver column at witness.azimuth_deg differs from the columns at +-120 deg, from rim_top_z - nut.skirt_below_flange - 0.5 upward
           tick_local_z: lowest z of the holder flange-rim column difference at witness.azimuth_deg (holder-local frame)
Run: freecadcmd tests/probes/probe_step6_marks.py"""
import os
import sys

sys.path.insert(0, 'C:/Users/Quinn Morley/OneDrive/PROJECTS/CC/CuttingJig/tests/probes')
import probe_lib as L  # noqa: E402
import glyph_math  # noqa: E402
C = L.C
STEP = 0.5
SPAN_Y = 22.0   # y line span: wing half root width 20 + 2; shorter than the tommy bosses at 45 + 90k (no fake glyphs)


def surface(sh, axis, sign, a, b):
    """Surface coordinate along `axis` (1 = y, 2 = z) of the solid at in-face position (x = a, other = b); None when no solid."""
    if axis == 1:
        p0, p1 = C.V(a, -SPAN_Y, b), C.V(a, SPAN_Y, b)
    else:
        p0, p1 = C.V(a, b, -10.0), C.V(a, b, 90.0)
    iv = C.line_ivals(sh, p0, p1)
    if not iv:
        return None
    base = p0.y if axis == 1 else p0.z
    return base + (iv[-1][1] if sign > 0 else iv[0][0])


def glyphs(sh, p):
    depth = L.G(p, "nut.arrow_depth")
    r_in = L.G(p, "wingnut.body_od") / 2 + 3
    r_out = L.G(p, "wingnut.span") / 2 - 3
    xs = [r_in + i * STEP for i in range(int((r_out - r_in) / STEP) + 1)]
    root = L.G(p, "wingnut.wing_root_width")
    z_hi = L.G(p, "nut.overall_height")
    found = []
    import Part
    crops = [Part.makeBox(r_out - r_in + 2, 2 * SPAN_Y, z_hi + 20, C.V(r_in - 1, -SPAN_Y, -10)),
             Part.makeBox(r_out - r_in + 2, 2 * SPAN_Y, z_hi + 20, C.V(-(r_out + 1), -SPAN_Y, -10))]
    sh = sh.common(Part.makeCompound(crops))
    for wing, sx in ((0, 1.0), (1, -1.0)):
        for face, axis, sign, (lo, hi) in (("+y", 1, 1.0, (0.0, z_hi)), ("-y", 1, -1.0, (0.0, z_hi)),
                                           ("+z", 2, 1.0, (-root / 2, root / 2)), ("-z", 2, -1.0, (-root / 2, root / 2))):
            bs = [lo + 3 + j * STEP for j in range(int((hi - lo - 6) / STEP) + 1)]
            void = []
            for x in (sx * v for v in xs):
                col = [(b, surface(sh, axis, sign, x, b)) for b in bs]
                col = [(b, v) for b, v in col if v is not None]
                if not col:
                    continue
                vals = sorted(v for _, v in col)
                med = vals[len(vals) // 2]
                for b, v in col:
                    if sign * (med - v) >= depth / 2.0:
                        void.append((x, v, b) if axis == 1 else (x, b, v))
            if len(void) >= 4:
                r = glyph_math.analyze(void)
                found.append({"wing": wing, "face": face, "count": r["count"], "span": r["span"], "direction_sign": r["direction_sign"]})
    return found


def occupied(iv, z):
    return any(a <= z <= b for a, b in iv)


def diff_marks(sh, az, r_list, z0, z1, dz=0.05, edge=False):
    zs = [z0 + i * dz for i in range(int((z1 - z0) / dz) + 1)]
    hit = set()
    for r in r_list:
        base = C.axial_ivals(sh, az, r, z0, z1)
        r1 = C.axial_ivals(sh, az + 120.0, r, z0, z1)
        r2 = C.axial_ivals(sh, az - 120.0, r, z0, z1)
        for i, z in enumerate(zs):
            o = occupied(base, z)
            if o != occupied(r1, z) and o != occupied(r2, z):
                hit.add(i)
    marks, cur = [], []
    for i in sorted(hit):
        if cur and i - cur[-1] > 6:
            marks.append(cur[0] if edge else sum(cur) / len(cur))
            cur = []
        cur.append(i)
    if cur:
        marks.append(cur[0] if edge else sum(cur) / len(cur))
    return [z0 + m * dz for m in marks]


def witness(p):
    az = L.G(p, "witness.azimuth_deg")
    rsh, _ = L.open_shape(os.path.join(L.CACHE, "receiver.FCStd"))
    hsh, _ = L.open_shape(os.path.join(L.CACHE, "holder.FCStd"))
    ref = (az + 120.0) % 360.0
    r_rim = L.G(p, "thread.major") / 2 - 1.0
    rim_top = C.axial_ivals(rsh, ref, r_rim, 0.0, 200.0)[-1][1]
    skirt = L.G(p, "nut.skirt_below_flange")
    z_ref = rim_top - skirt                                    # reading plane: nut skirt bottom face at gap 0 (Loftsman C1)
    floor_r = L.G(p, "thread.minor") / 2 - L.G(p, "witness.channel_floor_depth")
    radii = [floor_r - f * L.G(p, "witness.line_depth") for f in (0.2, 0.5, 0.8)]   # inside the graduation cut, below the channel floor
    marks = diff_marks(rsh, az, radii, z_ref - 0.5, z_ref - 0.5 + 0.5 + L.G(p, "holder.stroke_gap_R") + 2.0)
    hz = C.axial_ivals(hsh, ref, L.G(p, "holder.flange_od") / 2 - 4.0, hsh.BoundBox.ZMin - 1, hsh.BoundBox.ZMax + 1)
    fr = [L.G(p, "holder.flange_od") / 2 - 0.5 - 0.25 * k for k in range(8)]
    tk = diff_marks(hsh, az, fr, hsh.BoundBox.ZMin, hsh.BoundBox.ZMax, edge=True)   # lowest z of the mark
    return {"az": az, "rim_top_z": rim_top, "marks_z": marks, "holder_under_local_z": hz[-1][0] if hz else None,
            "tick_local_z": tk[0] if tk else None, "tick_count": len(tk)}


def main():
    p, out, inputs = L.params(), {}, []
    nut_path = os.path.join(L.CACHE, "nut.FCStd")
    if os.path.exists(nut_path):
        out["glyphs"] = glyphs(L.open_shape(nut_path)[0], p)
        inputs.append(nut_path)
    try:
        out["witness"] = witness(p)
        inputs += [os.path.join(L.CACHE, "receiver.FCStd"), os.path.join(L.CACHE, "holder.FCStd")]
    except KeyError as e:
        out["witness"] = {"error": "params key %s" % e}
    L.finish("step6_marks_asis", out, inputs)


if __name__ in ("__main__", "probe_step6_marks_asis"):
    L.guarded(main, "step6_marks_asis")
