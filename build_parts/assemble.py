"""Step 7 assembler. Run under freecadcmd; mode and size come from the environment (success = BUILD_DONE line plus a fresh artifact, A.15).
  CJ_MODE=ledger   results/assembly_poses.json (pure arithmetic from params plus the frame instance names)
  CJ_MODE=poses    parts_cache/assembly/pose_<P>_<tag>.FCStd for R, Kd1, Kmax of the size CJ_D (default: every size, serial); CJ_D=100 builds the nominal size
  CJ_MODE=output   output/jig_assembly.FCStd and .step (nominal size, Kd1, every deliverable visible and named)
Poses come from one base pose (R) by the screw motion S(phi); see assemble_lib.py. Nothing here is imported by another script."""
import json
import os
import sys
import time
import traceback

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import assemble_lib as A  # noqa: E402
C = A.C
G = A.G


def build_size(p, d):
    core_lib = A.load_core_lib()
    audits = {}
    for pose in A.POSES:
        t0 = time.time()
        shapes = A.local_shapes(p, d, pose, core_lib)
        pls = A.placements(p, d, pose)
        doc = A.new_pose_doc("pose_%s_%s" % (pose, A.tag(d)), shapes, pls)
        path = A.ASM / ("pose_%s_%s.FCStd" % (pose, A.tag(d)))
        A.save_doc(doc, path)
        audits[pose] = A.audit(doc, pls)
        import FreeCAD as App
        App.closeDocument(doc.Name)
        A.log("POSE %s %s saved %s %.1fs max_placement_diff=%.2e non_identity=%s" % (pose, A.tag(d), path.name, time.time() - t0,
                                                                                    audits[pose]["max_diff"], audits[pose]["non_identity"]))
    A.RESULTS.mkdir(exist_ok=True)
    (A.RESULTS / ("assembly_audit_%s.json" % A.tag(d))).write_text(json.dumps({"sentinel": "AUDIT_OK", "tag": A.tag(d), "poses": audits}, indent=1), encoding="utf-8")


def context_placements(p):
    """Placements of the non-ASSEMBLY.md deliverables in the output assembly. foot: rail covers local x 0 to profile.width (Topologist E5: Placement(position, Rz(180)))."""
    import FreeCAD as App
    V, Z = App.Vector, App.Vector(0, 0, 1)
    fx, fy = G(p, "icd.footprint_x"), G(p, "icd.footprint_y")
    w, h = G(p, "profile.width"), G(p, "profile.height")
    ground = -(h + G(p, "foot.size")[2])
    xe, ye = fx / 2.0 - w, fy / 2.0 - w / 2.0
    out = {"tray": App.Placement(), "plug": App.Placement(), "stop": App.Placement(),
           "foot_1": App.Placement(V(xe, ye, ground), App.Rotation()), "foot_2": App.Placement(V(xe, -ye, ground), App.Rotation()),
           "foot_3": App.Placement(V(-xe, ye, ground), App.Rotation(Z, 180.0)), "foot_4": App.Placement(V(-xe, -ye, ground), App.Rotation(Z, 180.0)),
           "rest": App.Placement(V(0, 0, G(p, "icd.floor_above_datum_a") + G(p, "rest.height_positions")[0]), App.Rotation())}
    cad = A.part_shape("caddy").BoundBox
    gau = A.part_shape("gauge").BoundBox
    out["caddy"] = App.Placement(V(0, -(fy / 2.0 + A.CONTEXT_OFFSET + cad.YLength / 2.0), ground), App.Rotation())
    out["gauge"] = App.Placement(V(fx / 2.0 + A.CONTEXT_OFFSET + gau.XLength / 2.0, 0, ground), App.Rotation())
    return out


def build_output(p):
    import FreeCAD as App
    d, pose = G(p, "core.diameter_nominal"), "Kd1"
    shapes = A.local_shapes(p, d, pose)
    pls = A.placements(p, d, pose)
    ctx = context_placements(p)
    src = {"tray": "tray", "plug": "plug", "stop": "stop", "caddy": "caddy", "gauge": "gauge", "rest": "rest", "foot_1": "foot", "foot_2": "foot",
           "foot_3": "foot", "foot_4": "foot"}
    for k, v in src.items():
        shapes[k] = A.part_shape(v)
        pls[k] = ctx[k]
    extra = {k: None for k in src}
    doc = A.new_pose_doc("jig_assembly", shapes, pls, extra)
    A.OUT.mkdir(exist_ok=True)
    fc = A.OUT / "jig_assembly.FCStd"
    A.save_doc(doc, fc)
    objs = [o for o in doc.Objects if hasattr(o, "Shape") and o.Shape.Solids]
    import Import
    step = A.OUT / "jig_assembly.step"
    if step.exists():
        step.unlink()
    Import.export(objs, str(step))
    rep = A.audit(doc, pls)
    A.RESULTS.mkdir(exist_ok=True)
    (A.RESULTS / "assembly_audit_jig.json").write_text(json.dumps({"sentinel": "AUDIT_OK", "pose": pose, "tag": A.tag(d), "audit": rep,
                                                                  "objects": [o.Label for o in objs]}, indent=1), encoding="utf-8")
    A.log("OUTPUT jig_assembly objects=%d step_bytes=%d max_placement_diff=%.2e" % (len(objs), step.stat().st_size, rep["max_diff"]))
    App.closeDocument(doc.Name)


def main():
    t0 = time.time()
    p = C.params()
    mode = os.environ.get("CJ_MODE", "poses")
    A.log("START assemble mode=%s pid=%d t=%s" % (mode, os.getpid(), time.strftime("%H:%M:%S")))
    try:
        if mode == "ledger":
            led = A.write_ledger(p)
            A.log("LEDGER sizes=%d" % len(led["sizes"]))
        elif mode == "poses":
            ds = [float(os.environ["CJ_D"])] if os.environ.get("CJ_D") else list(G(p, "core.diameters"))
            for d in ds:
                build_size(p, d)
        elif mode == "output":
            build_output(p)
        else:
            raise SystemExit("unknown CJ_MODE %s" % mode)
    except BaseException:
        traceback.print_exc()
        A.log("BUILD_FAILED assemble %s" % mode)
    A.log("run_seconds %.1f" % (time.time() - t0))
    A.log("BUILD_DONE assemble %s" % os.environ.get("CJ_MODE", "poses"))


if __name__ in ("__main__", "assemble"):
    main()
