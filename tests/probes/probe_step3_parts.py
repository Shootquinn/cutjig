"""F5 and E3 inputs for the five Step 3 parts: validity, solid and shell counts, Euler record, volume, flipped-copy mismatch (Rule P),
reopened-document visible object count, and genus. The B-rep V-E+F is not a disc-cell Euler count for these annular and periodic faces
(cadlib.base_result records genus null), so genus is computed by a cell count over the B-rep (cell_genus): chi = V - E' + sum of open-face characteristics, genus = (2 - chi) / 2
for one closed orientable shell. It equals the number of through-holes.
Output results/probes/step3_parts.json.
Run (3 s): freecadcmd tests/probes/probe_step3_parts.py"""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import probe_lib as L  # noqa: E402
C = L.C

PARTS = ("receiver", "holder", "nut", "washer", "footring")


def flip_mismatch(sh):
    """Rotate 180 degrees about the X axis through the mid-height; 1 - common/volume is the fraction of the part that moves."""
    bb = sh.BoundBox
    f = sh.copy()
    f.rotate(C.V(0, 0, (bb.ZMin + bb.ZMax) / 2.0), C.V(1, 0, 0), 180.0)
    return 1.0 - sh.common(f).Volume / sh.Volume


def _face_chi_open(f, tol=0.05):
    """Compactly supported Euler characteristic of the open face: chi of its own merged triangulation minus chi of its boundary graph."""
    pts, tris = f.tessellate(tol)
    idx, vid = {}, []
    for q in pts:
        vid.append(idx.setdefault((round(q.x * 1e4), round(q.y * 1e4), round(q.z * 1e4)), len(idx)))
    ed, nf = {}, 0
    for a, b, c in tris:
        t = (vid[a], vid[b], vid[c])
        if len(set(t)) < 3:
            continue
        nf += 1
        for u, v in ((t[0], t[1]), (t[1], t[2]), (t[2], t[0])):
            k = (min(u, v), max(u, v))
            ed[k] = ed.get(k, 0) + 1
    bv = set()
    be = 0
    for (u, v), n in ed.items():
        if n == 1:
            bv.update((u, v))
            be += 1
    return (len(idx) - len(ed) + nf) - (len(bv) - be)


def cell_genus(sh):
    """Genus of the single closed shell from a cell count: chi = V - E' + sum chi_open(face), E' = B-rep edges minus seam edges
    (an edge used twice by one face). Per-face triangulations are never matched across faces, so tessellation cracks between faces
    do not enter. Validated on a ring (1), ring + 4 holes (5), ring + radial tunnel (2). genus = (2 - chi) / 2."""
    seams = 0
    for f in sh.Faces:
        for w in f.Wires:
            oe = w.OrderedEdges
            seams += sum(1 for i, e in enumerate(oe) if any(e.isSame(o) for o in oe[i + 1:]))
    chi = len(sh.Vertexes) - (len(sh.Edges) - seams) + sum(_face_chi_open(f) for f in sh.Faces)
    return {"cell_chi": chi, "cell_genus": (2 - chi) / 2.0, "seam_edges": seams}


def main():
    out, inputs = {}, []
    for name in PARTS:
        t = time.time()
        path = os.path.join(L.CACHE, name + ".FCStd")
        sh, doc = L.open_shape(path)
        visible = [o.Name for o in doc.Objects if hasattr(o, "Shape") and getattr(o, "Visibility", True) and o.TypeId == "PartDesign::Body"]
        out[name] = {"valid": bool(sh.isValid()), "closed": bool(sh.isClosed()), "solids": len(sh.Solids), "shells": len(sh.Shells),
                     "volume": sh.Volume, "euler_VEF": len(sh.Vertexes) - len(sh.Edges) + len(sh.Faces),
                     "flip_mismatch_fraction": flip_mismatch(sh), **cell_genus(sh), "bodies": visible, "object_count": len(doc.Objects)}
        inputs.append(path)
        print("PART %s %.1fs" % (name, time.time() - t), flush=True)
    L.finish("step3_parts", out, inputs)


if __name__ in ("__main__", "probe_step3_parts"):
    L.guarded(main, "step3_parts")
