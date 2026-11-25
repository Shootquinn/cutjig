"""K1 Z fixture: a sketch script that reads every value from the loader. Scanned by AST only, never run."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import sketch_common as sc
from matplotlib.patches import Rectangle


def build(P, spec, stack):
    figs = {}
    for pose in spec["poses"]:
        pid = pose["id"]
        fig, ax = sc.setup_figure(spec["view"], title=pid)
        z = stack["poses"][pid]["features"]["drill_tube"]
        half = P.get("drill.tube_od") / 2
        sc.draw("drill_tube", Rectangle((-half, z["z_min"]), 2 * half, z["z_max"] - z["z_min"]), ax)
        figs[pid] = fig
    return figs
