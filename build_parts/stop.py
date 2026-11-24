"""Stop (ST1): interface item, owner `upper assembly` (stop.owner). Pad stop.pad_width x stop.pad_length x stop.pad_thickness on the column face,
top face at stop.height_z (datum A, Loftsman C9). Zero nut volume: the stop is not a nut property. Two M6 clearance holes give the F5 boolean record."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import step6lib as S  # noqa: E402
import cadlib as C  # noqa: E402


def nut_overlap(sh):
    import FreeCAD as App
    doc = App.openDocument(str(C.CACHE / "nut.FCStd"))
    v = sh.common(C.final_shape(doc.getObject("Body"))).Volume
    App.closeDocument(doc.Name)
    return v


def build():
    p = C.params()
    g = lambda k: C.G(p, k)
    rec = S.Rec("stop")
    cx, cy = g("stop.pad_xy")
    w, ln, th, zt = g("stop.pad_width"), g("stop.pad_length"), g("stop.pad_thickness"), g("stop.height_z")
    ov = g("collet.tool_overshoot")
    pad = S.box(cx - w / 2, cx + w / 2, cy - ln / 2, cy + ln / 2, zt - th, zt)
    holes = [S.cyl_z(cx + s * g("stop.pad_hole_x"), cy, g("stop.pad_hole_dia") / 2, zt - th - ov, zt + ov) for s in (-1, 1)]
    tool = rec.fuse("holes_tool_fuse", holes)
    sh = S.solid_of(rec.cut("holes_cut", pad, tool))
    col_face = g("column.spacing") / 2 - g("profile.width") / 2
    rows = [
        S.row("ST1", "stop pad top face z = stop.height_z (A)", pad.Volume, sh.BoundBox.ZMax, zt, S.TOL),
        S.row("ST1", "stop pad underside z = stop.height_z - stop.pad_thickness (A)", pad.Volume, sh.BoundBox.ZMin, zt - th, S.TOL),
        S.row("ST1", "stop pad width x (T)", pad.Volume, sh.BoundBox.XLength, w, S.TOL),
        S.row("ST1", "stop pad length y (L)", pad.Volume, sh.BoundBox.YLength, ln, S.TOL),
        S.row("ST1", "stop pad meets the column face plane y (L)", pad.Volume, sh.BoundBox.YMax, col_face, S.TOL),
    ]
    nv = nut_overlap(sh)
    res = S.result("stop", sh, rows, rec, extra={
        "owner": g("stop.owner"), "nut_volume_mm3": round(nv, S.ND),
        "interface": {"height_z_datum_A": zt, "face": "top", "normal": "+z", "pad_mm": [w, ln, th], "centre_xy": [cx, cy],
                      "rated_load_N": g("stop.rated_load"), "collar_top_z": g("stop.collar_top_z"), "g_stop": g("stop.g_stop"),
                      "gap_to_collar_top": zt - th - g("stop.collar_top_z"), "owner": g("stop.owner"), "column_face_y": col_face}})
    S.save_single("stop", sh, res)
    return res


if __name__ in ("__main__", "stop"):
    C.run_main("stop", build)
