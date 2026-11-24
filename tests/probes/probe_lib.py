"""Shared probe plumbing. Runs under freecadcmd only. Probes open FCStd read-only (never doc.save, which creates .FCBak files),
measure final shapes, and write results/probes/<name>.json with the PROBE_OK sentinel. pytest never launches FreeCAD."""
import json
import os
import sys
import time
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "build_parts"))
import cadlib as C  # noqa: E402  (measurement helpers: line_ivals, radial_ivals, axial_ivals, tangential_ivals)
import common  # noqa: E402

CACHE = common.PARTS_CACHE
OUT = os.path.join(ROOT, "results", "probes")
T0 = time.time()


def params():
    return common.load_params()


def G(p, key):
    return common.get(p, key)


def open_shape(path, obj="Body"):
    """Open an FCStd read-only and return (shape, doc). Falls back to the first visible solid object."""
    import FreeCAD as App
    doc = App.openDocument(str(path))
    o = doc.getObject(obj)
    if o is None:
        cands = [x for x in doc.Objects if hasattr(x, "Shape") and x.Shape.Solids]
        o = cands[-1]
    return C.final_shape(o), doc


def part(name):
    return open_shape(os.path.join(CACHE, name + ".FCStd"))[0]


def moved(sh, x=0.0, y=0.0, z=0.0):
    s = sh.copy()
    s.translate(C.V(x, y, z))
    return s


def finish(name, data, inputs=()):
    os.makedirs(OUT, exist_ok=True)
    data = dict(data)
    data.update({"sentinel": "PROBE_OK", "probe": name, "run_started_epoch": T0, "run_seconds": round(time.time() - T0, 1),
                 "inputs": [str(i) for i in inputs]})
    with open(os.path.join(OUT, name + ".json"), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1)
    print("PROBE_DONE %s %.1fs" % (name, time.time() - T0), flush=True)


def guarded(main, name):
    try:
        main()
    except BaseException:
        traceback.print_exc()
        print("PROBE_FAILED %s" % name, flush=True)
