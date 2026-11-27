"""S4 stub for the red-first run (gameplan detail 1 common (c), detail 1.4): loads params, calls setup_figure with the
spec view (section_yz), draws the shop floor line only (row floor, across its depth band at z_S 0). One figure per spec
section_figures pose (carrier: figure 1; liner: figure 2)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import sketch_common as sc  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402


def build(P, spec, stack):
    figs = {}
    for fd in spec.get("section_figures") or [spec.get("section_figure") or {"pose": spec["poses"][0]["id"]}]:
        pid = fd["pose"]
        fig, ax = sc.setup_figure(spec["view"], title=f"S4 stub, section B-B at pose {pid}", insets=spec.get("insets"))
        f = stack["poses"][pid]["features"]["floor"]
        u0, u1 = f["depth"]
        sc.draw("floor", Line2D([u0, u1], [f["z_min"], f["z_max"]]), ax)
        sc.finish_axes(ax)
        figs[pid] = fig
    return figs
