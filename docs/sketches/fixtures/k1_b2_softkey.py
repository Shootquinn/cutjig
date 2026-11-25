"""K1 B2 fixture: planted assertion against the soft key jig.height_target. Scanned by AST only, never run."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import sketch_common as sc
from matplotlib.patches import Rectangle


def build(P, spec, stack):
    figs = {}
    get = P.get
    for pose in spec["poses"]:
        pid = pose["id"]
        fig, ax = sc.setup_figure(spec["view"], title=pid)
        z = stack["poses"][pid]["features"]["drill_tube"]
        half = get("drill.tube_od") / 2
        top = z["z_max"]
        assert top < get("jig.height_target")
        sc.draw("drill_tube", Rectangle((-half, z["z_min"]), 2 * half, top - z["z_min"]), ax)
        figs[pid] = fig
    return figs
