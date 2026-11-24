"""Step 6 shared builders: solid primitives, boolean recording (llm_plm_cad 7.1), result-JSON contract.
Every boolean goes through Rec so the result JSON carries faces_before / faces_after per boolean, plain versus optimal bbox,
and the boolean count. Fuse first, boolean once: tools are fused with one multiFuse and applied with one cut.
Runs inside freecadcmd (FreeCAD imported lazily)."""
import json
import math
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else r"C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\build_parts"
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import cadlib as C  # noqa: E402

CACHE = C.CACHE
V = C.V
TOL = 0.015     # default feature-row tolerance, mm (not a part dimension)
SCAN = 17.0     # measurement-line margin beyond a feature, mm (not a part dimension)
ND = 5          # digits kept in recorded positions


# ----------------------------------------------------------------- primitives
def box(x0, x1, y0, y1, z0, z1):
    import Part
    return Part.makeBox(x1 - x0, y1 - y0, z1 - z0, V(x0, y0, z0))


def cyl_z(cx, cy, r, z0, z1):
    import Part
    return Part.makeCylinder(r, z1 - z0, V(cx, cy, z0), V(0, 0, 1))


def cyl_dir(base, direction, r, h):
    import Part
    return Part.makeCylinder(r, h, base, direction)


def extrude_poly(pts, plane, c0, c1):
    """Closed polygon extruded between c0 and c1 along the plane normal. plane 'xz': pts are (x, z), extruded along y.
    plane 'yz': pts are (y, z), along x. plane 'xy': pts are (x, y), along z."""
    import Part
    if plane == "xz":
        v = [V(a, c0, b) for a, b in pts]
        d = V(0, c1 - c0, 0)
    elif plane == "yz":
        v = [V(c0, a, b) for a, b in pts]
        d = V(c1 - c0, 0, 0)
    else:
        v = [V(a, b, c0) for a, b in pts]
        d = V(0, 0, c1 - c0)
    return Part.Face(Part.makePolygon(v + [v[0]])).extrude(d)


def stadium(origin, long_dir, normal, length, width, depth):
    """Obround slot tool: overall `length` along long_dir, `width` across, extruded `depth` along normal from origin (centre of the start face)."""
    import FreeCAD as App
    import Part
    r, hl = width / 2.0, (length - width) / 2.0
    if hl <= 1e-9:
        face = Part.Face(Part.Wire(Part.makeCircle(r, V(0, 0, 0), V(0, 0, 1))))
    else:
        e = [Part.makeLine(V(-hl, -r, 0), V(hl, -r, 0)), Part.Arc(V(hl, -r, 0), V(hl + r, 0, 0), V(hl, r, 0)).toShape(),
             Part.makeLine(V(hl, r, 0), V(-hl, r, 0)), Part.Arc(V(-hl, r, 0), V(-hl - r, 0, 0), V(-hl, -r, 0)).toShape()]
        face = Part.Face(Part.Wire(e))
    sol = face.extrude(V(0, 0, depth))
    xv, zv = long_dir.normalize(), normal.normalize()
    yv = zv.cross(xv)
    sol.Placement = App.Placement(origin, App.Rotation(xv, yv, zv, "ZXY"))
    return sol.copy()


def placed(shape, origin, xdir, zdir):
    """Copy of `shape` (built with local x, local z) re-posed so local x -> xdir, local z -> zdir, local origin -> origin."""
    import FreeCAD as App
    xv, zv = xdir.normalize(), zdir.normalize()
    yv = zv.cross(xv)
    s = shape.copy()
    s.Placement = App.Placement(origin, App.Rotation(xv, yv, zv, "ZXY")).multiply(s.Placement)
    return s.copy()


# ----------------------------------------------------------------- recorded booleans
class Rec:
    def __init__(self, part):
        self.part = part
        self.t0 = time.time()
        self.booleans = []

    def _log(self, name, kind, before, after, extra=None):
        d = {"name": name, "kind": kind, "faces_before": int(before), "faces_after": int(after)}
        if extra:
            d.update(extra)
        self.booleans.append(d)

    def fuse(self, name, shapes):
        shapes = list(shapes)
        before = sum(len(s.Faces) for s in shapes)
        res = shapes[0].multiFuse(shapes[1:]) if len(shapes) > 1 else shapes[0]
        raw = len(res.Faces)
        res = res.removeSplitter()
        self._log(name, "fuse", before, raw, {"faces_after_clean": len(res.Faces), "valid": bool(res.isValid())})
        return res

    def cut(self, name, base, tool):
        before = len(base.Faces)
        res = base.cut(tool)
        raw = len(res.Faces)
        res = res.removeSplitter()
        self._log(name, "cut", before, raw, {"faces_after_clean": len(res.Faces), "valid": bool(res.isValid()), "tool_faces": len(tool.Faces)})
        return res


    def common(self, name, a, b):
        before = len(a.Faces) + len(b.Faces)
        res = a.common(b)
        raw = len(res.Faces)
        res = res.removeSplitter()
        self._log(name, "common", before, raw, {"faces_after_clean": len(res.Faces), "valid": bool(res.isValid())})
        return res


def solid_of(sh):
    return sh.Solids[0] if len(sh.Solids) == 1 else sh


def removed(tool, pre):
    """Volume a cut tool removes from `pre` (feature-row volume for subtractive features)."""
    return tool.common(pre).Volume


# ----------------------------------------------------------------- result contract
def row(fid, feature, volume, built=None, expected=None, tol=0.05, ok=None, note=""):
    if ok is None:
        ok = built is not None and expected is not None and abs(built - expected) <= tol
    return {"id": fid, "feature": feature, "volume_mm3": round(float(volume), 3), "built": None if built is None else (round(built, 4) if isinstance(built, float) else built),
            "params": None if expected is None else (round(expected, 4) if isinstance(expected, float) else expected), "tol": tol, "pass": bool(ok), "note": note}


def _bb(b):
    return {"xmin": round(b.XMin, 3), "xmax": round(b.XMax, 3), "ymin": round(b.YMin, 3), "ymax": round(b.YMax, 3), "zmin": round(b.ZMin, 3), "zmax": round(b.ZMax, 3)}


def euler(sh):
    return len(sh.Vertexes) - len(sh.Edges) + len(sh.Faces)


def result(part, shape, rows, rec, extra=None):
    if hasattr(shape, "CenterOfMass"):
        com = shape.CenterOfMass
    else:
        sol = shape.Solids
        tv = sum(x.Volume for x in sol)
        com = V(sum(x.CenterOfMass.x * x.Volume for x in sol) / tv, sum(x.CenterOfMass.y * x.Volume for x in sol) / tv,
                sum(x.CenterOfMass.z * x.Volume for x in sol) / tv)
    res = {
        "part": part, "volume_mm3": round(shape.Volume, 3), "isValid": bool(shape.isValid()), "isClosed": bool(shape.isClosed()),
        "solid_count": len(shape.Solids), "shell_count": len(shape.Shells), "euler_VEF": euler(shape),
        "faces": len(shape.Faces), "edges": len(shape.Edges), "vertices": len(shape.Vertexes),
        "bbox_plain": _bb(shape.BoundBox), "bbox_optimal": _bb(C.bbox(shape)), "bbox": _bb(C.bbox(shape)),
        "centre_of_mass": [round(com.x, 3), round(com.y, 3), round(com.z, 3)],
        "features": rows, "all_features_pass": all(r["pass"] for r in rows),
        "booleans": rec.booleans, "boolean_count": len(rec.booleans),
        "run_seconds": round(time.time() - rec.t0, 1), "build_seconds": round(time.time() - rec.t0, 1),
    }
    if extra:
        res.update(extra)
    return res


def save_single(part, shape, res):
    """One document, one Part::Feature named Body (the probe opens `Body`). JSON beside it."""
    import FreeCAD as App
    CACHE.mkdir(exist_ok=True)
    doc = App.newDocument(part)
    o = doc.addObject("Part::Feature", "Body")
    o.Shape = shape
    doc.recompute()
    doc.saveAs(str(CACHE / (part + ".FCStd")))
    with open(CACHE / (part + "_result.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, indent=1)


# ----------------------------------------------------------------- rebuild support
BEFORE_DIR = C.ROOT / "cr_scratch" / "step6_before"


BEFORE_DIR_7 = C.ROOT / "cr_scratch" / "step7_before"


def before_state(part, src=None):
    """Volume, face count and euler of the solid saved in cr_scratch/step6_before (copy made before the Step 6 rebuild); src names another
    snapshot directory (Step 7: BEFORE_DIR_7, copy made before the holder and nut rebuild)."""
    import FreeCAD as App
    src = src or BEFORE_DIR
    j = json.load(open(src / (part + "_result.json"), encoding="utf-8"))
    doc = App.openDocument(str(src / (part + ".FCStd")))
    o = doc.getObject("Body")
    sh = C.final_shape(o)
    out = {"before_volume": j["volume_mm3"], "before_faces": len(sh.Faces), "before_euler": euler(sh), "before_features": len(j["features"])}
    App.closeDocument(doc.Name)
    return out


def rebuild_record(before, shape, reason_ids, booleans):
    d = dict(before)
    d.update({"after_volume": round(shape.Volume, 3), "after_faces": len(shape.Faces), "after_euler": euler(shape), "reason_ids": list(reason_ids),
              "volume_ratio": round(shape.Volume / before["before_volume"], ND)})
    return d


def point_at(az_deg, d, t, z):
    """World point at axial height z, distance d from the axis along azimuth az, tangential offset t (t = z x r, counter-clockwise)."""
    a = math.radians(az_deg)
    return V(d * math.cos(a) - t * math.sin(a), d * math.sin(a) + t * math.cos(a), z)
