import FreeCAD as App, json, sys, os
ROOT = r"C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig"
PC = os.path.join(ROOT, "parts_cache")
out = {}

def topo(s):
    V = len(s.Vertexes); E = len(s.Edges); F = len(s.Faces)
    R = sum(max(0, len(f.Wires) - 1) for f in s.Faces)
    S = len(s.Shells)
    chi = V - E + F
    H = S - (chi - R) / 2.0 if S else None
    bp = s.BoundBox
    try:
        bo = s.optimalBoundingBox(True, False)
        bo_t = [round(x, 3) for x in (bo.XMin, bo.XMax, bo.YMin, bo.YMax, bo.ZMin, bo.ZMax)]
    except Exception as e:
        bo_t = str(e)
    return dict(V=V, E=E, F=F, euler_VEF=chi, rings=R, shells=S, solids=len(s.Solids), genus=H,
                valid=s.isValid(), closed=s.isClosed(), vol=round(s.Volume, 3),
                bbox_plain=[round(x, 3) for x in (bp.XMin, bp.XMax, bp.YMin, bp.YMax, bp.ZMin, bp.ZMax)],
                bbox_opt=bo_t)

for name in ("core", "cutter", "holder", "nut", "frame", "bracket_purchased", "bracket_printed", "tnut"):
    d = App.openDocument(os.path.join(PC, name + ".FCStd"))
    rec = {}
    for o in d.Objects:
        if hasattr(o, "Shape") and not o.Shape.isNull() and o.Shape.Solids and (name != "frame" or True):
            if name in ("frame",) and not o.Name.startswith(("member", "Member", "Frame")) and len(d.Objects) > 20:
                pass
            rec[o.Name] = dict(label=o.Label, visible=getattr(o, "Visibility", None), **topo(o.Shape))
    out[name] = rec
    App.closeDocument(d.Name)
    print("done", name, len(rec), flush=True)
json.dump(out, open(os.path.join(ROOT, "research", "quinn", "cr_scratch", "step7_topo_parts.json"), "w"), indent=1)
print("BUILD_DONE")
