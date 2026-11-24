"""Step 7 planted wrong states WS1 to WS11 (Loftsman L7, Topologist E6) at the nominal size. Each file parts_cache/assembly/ws<n>.FCStd holds the same ten
objects as a pose file; one part is moved by the transform below. Run under freecadcmd; success = BUILD_DONE plus fresh ws<n>.FCStd files.
Planted-state magnitudes are DECLARED transform constants (Loftsman L7), not part dimensions; pivots are read from the built shapes.
  WS1 collet Rx(180) about its mid-height          WS2 holder Rx(180) about the tube mid-height     WS3 nut Rx(180) about its mid-height
  WS4 nut mirrored y to -y (improper; baked with Shape.mirror, identity placement)                  WS5 nut Rx(2) about its mid-height
  WS6 collet of the smallest family size on the nominal core                                        WS7 collet raised
  WS8 (Kmax) holder lowered    WS9 (Kmax) nut and washer further down the screw motion              WS10 base Rx(180) about the plate mid-thickness
  WS11 collet Rz(-15) about the axis"""
import json
import os
import sys
import time
import traceback

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import assemble_lib as A  # noqa: E402
sys.path.insert(0, os.path.join(A.ROOT, "tests", "probes"))
import gates  # noqa: E402
C = A.C
G = A.G

TILT_DEG = 2.0            # WS5 planted tilt
RAISE_MM = 3.0            # WS7 collet unseated height
LOWER_MM = -1.5           # WS8 holder pushed below its Kmax seat
SPIN_DEG = -15.0          # WS11 collet turned about the axis
DZ_WS9 = -13.510          # WS9 nut and washer descent from Kmax: 10.01 stop travel + 3.5 past the physical stop (Loftsman L7)
MIRROR_COM_TOL = 0.5       # WS4 guard: mirrored nut centre of mass against the pose nut centre of mass (x, -y, z)
POSE_OF = {8: "Kmax", 9: "Kmax"}


def rot_about(axis, deg, pivot_z):
    import FreeCAD as App
    return App.Placement(App.Vector(0, 0, 0), App.Rotation(axis, deg), App.Vector(0, 0, pivot_z))


def build_ws(p, n, d, core_lib):
    import FreeCAD as App
    V = App.Vector
    pose = POSE_OF.get(n, "Kd1")
    shapes = A.local_shapes(p, d, pose, core_lib)
    pls = A.placements(p, d, pose)
    nm = A.pose_numbers(p, d, pose)
    X, Z = V(1, 0, 0), V(0, 0, 1)
    nut_h = C.bbox(shapes["nut"]).ZMax
    if n == 1:
        pls["collet"] = rot_about(X, 180.0, nm["zf"] + C.bbox(shapes["collet"]).ZMax / 2.0).multiply(pls["collet"])
    elif n == 2:
        top = C.bbox(shapes["holder"]).ZMax - G(p, "collar.thickness")        # unfused tube top, E6
        pls["holder"] = rot_about(X, 180.0, nm["holder_z"] + top / 2.0).multiply(pls["holder"])
    elif n == 3:
        pls["nut"] = rot_about(X, 180.0, nm["nut_z"] + nut_h / 2.0).multiply(pls["nut"])
    elif n == 4:
        # Topologist D1: the pose placement is baked into the geometry first (transformShape), then mirrored y -> -y; the object keeps the location the mirrored shape carries (the pose placement).
        bad = shapes["nut"].copy().mirror(V(0, 0, 0), V(0, 1, 0)).CenterOfMass     # known-bad: the unplaced (displaced) mirror of the earlier build
        posed = shapes["nut"].copy()
        posed.transformShape(pls["nut"].toMatrix())
        com_pose = posed.CenterOfMass
        m = posed.mirror(V(0, 0, 0), V(0, 1, 0))
        if m.Volume < 0:
            m.reverse()
        if not (m.Volume > 0 and m.isValid()):
            raise RuntimeError("mirrored nut volume %s valid %s" % (m.Volume, m.isValid()))
        com_m = m.CenterOfMass
        good_d = (com_m - V(com_pose.x, -com_pose.y, com_pose.z)).Length
        bad_d = (bad - V(com_pose.x, -com_pose.y, com_pose.z)).Length
        guard = {"good_mm": good_d, "bad_mm": bad_d, "tol_mm": MIRROR_COM_TOL, "com_pose": [com_pose.x, com_pose.y, com_pose.z], "com_mirrored": [com_m.x, com_m.y, com_m.z]}
        A.RESULTS.mkdir(exist_ok=True)
        (A.RESULTS / "assembly_ws4_guard.json").write_text(json.dumps(guard, indent=1), encoding="utf-8")
        if good_d > MIRROR_COM_TOL:
            raise RuntimeError("mirrored nut CoM is %.3f mm from the pose CoM mirrored in y" % good_d)
        shapes["nut"] = m
        pls["nut"] = m.Placement       # the mirrored shape carries the pose location; resetting the object placement to identity would drop it (D1 root cause)
    elif n == 5:
        pls["nut"] = rot_about(X, TILT_DEG, nm["nut_z"] + nut_h / 2.0).multiply(pls["nut"])
    elif n == 6:
        small = min(G(p, "core.diameters"))
        shapes["collet"] = A.part_shape(A.collet_name(small, pose))
    elif n == 7:
        pls["collet"] = App.Placement(V(0, 0, RAISE_MM), App.Rotation()).multiply(pls["collet"])
    elif n == 8:
        pls["holder"] = App.Placement(V(0, 0, LOWER_MM), App.Rotation()).multiply(pls["holder"])
    elif n == 9:
        led = A.pose_numbers(p, d, "Kmax")
        dz = DZ_WS9
        s = App.Placement(V(0, 0, dz), App.Rotation(Z, 360.0 * dz / led["lead"]))
        pls["nut"] = s.multiply(pls["nut"])
        pls["washer"] = s.multiply(pls["washer"])
    elif n == 10:
        pls["base"] = rot_about(X, 180.0, G(p, "base.plate_thickness") / 2.0).multiply(pls["base"])
    elif n == 11:
        pls["collet"] = rot_about(Z, SPIN_DEG, 0.0).multiply(pls["collet"])
    doc = A.new_pose_doc("ws%d" % n, shapes, pls)
    path = A.ASM / ("ws%d.FCStd" % n)
    A.save_doc(doc, path)
    rep = A.audit(doc, pls)
    App.closeDocument(doc.Name)
    return {"pose": pose, "tag": A.tag(d), "audit_max_diff": rep["max_diff"]}


def main():
    t0 = time.time()
    A.log("START assemble_ws pid=%d t=%s" % (os.getpid(), time.strftime("%H:%M:%S")))
    try:
        p = C.params()
        d = G(p, "core.diameter_nominal")
        core_lib = A.load_core_lib()
        meta = {}
        only = os.environ.get("CJ_WS")
        for n in [k for k in sorted(gates.WS_EXPECT) if not only or str(k) in only.split(",")]:
            t1 = time.time()
            meta[str(n)] = build_ws(p, n, d, core_lib)
            A.log("WS%d saved %.1fs %s" % (n, time.time() - t1, meta[str(n)]))
        led = json.loads(A.LEDGER.read_text(encoding="utf-8"))
        led["ws"].update({k: {"pose": v["pose"], "tag": v["tag"]} for k, v in meta.items()})
        A.LEDGER.write_text(json.dumps(led, indent=1), encoding="utf-8")
    except BaseException:
        traceback.print_exc()
        A.log("BUILD_FAILED assemble_ws")
    A.log("run_seconds %.1f" % (time.time() - t0))
    A.log("BUILD_DONE assemble_ws")


if __name__ in ("__main__", "assemble_ws"):
    main()
