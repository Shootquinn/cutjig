p = r"C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\build_parts\holder.py"
s = open(p, encoding="utf-8").read()


def rep(old, new):
    global s
    assert old in s, old[:70]
    s = s.replace(old, new, 1)


rep('import cadlib as C  # noqa: E402\n', 'import cadlib as C  # noqa: E402\nimport step6lib as S  # noqa: E402\n')
rep('Local frame: bottom at z = 0."""', 'Local frame: bottom at z = 0.\nStep 6 rebuild (HD7, AC5): witness tick groove on the flange rim at witness.azimuth_deg, in the same cut as the notch and inserts."""')
rep('''def build():
    t0 = time.time()
    p = C.params()''', '''def build():
    t0 = time.time()
    before = S.before_state("holder")
    p = C.params()''')
rep('''    C.body_boolean(doc, body, key, "Fuse", "Key")''', '''    f_tube = len(C.final_shape(body).Faces)
    C.body_boolean(doc, body, key, "Fuse", "Key")
    pre_key = C.final_shape(body)
    bools = [{"name": "Key", "kind": "fuse", "faces_before": f_tube, "faces_after": len(pre_key.Faces)}]''')
rep('''    C.body_boolean(doc, body, C.fuse_all(tools), "Cut", "NotchAndInserts")
    sh = C.final_shape(body)''', '''    ov = g("collet.tool_overshoot")
    az_w = g("witness.azimuth_deg")
    tick = C.box_at(az_w, q["r_fl"] - g("witness.tick_depth"), q["r_fl"] + ov, g("witness.tick_width") / 2, q["L"] - ov, q["L"] + g("witness.tick_height"))
    tick_mm3 = S.removed(tick, pre_key)
    tools.append(tick)
    tool = C.fuse_all(tools)
    C.body_boolean(doc, body, tool, "Cut", "NotchInsertsTick")
    sh = C.final_shape(body)
    bools.append({"name": "NotchInsertsTick", "kind": "cut", "faces_before": len(pre_key.Faces), "faces_after": len(sh.Faces), "tool_faces": len(tool.Faces)})''')
rep('''    feats = [
        C.chk("holder outer diameter (D) = 2 (register r - g_reg)"''', '''    tk_w = C.tangential_ivals(sh, az_w, q["r_fl"] - g("witness.tick_depth") / 2, q["L"] + g("witness.tick_height") / 2, 5.0)
    tk_r = C.radial_ivals(sh, az_w, q["L"] + g("witness.tick_height") / 2, 0, 90)
    tk_a = C.axial_ivals(sh, az_w, q["r_fl"] - g("witness.tick_depth") / 2, -1, q["z_top"] + 1)
    under_other = C.axial_ivals(sh, az_w + 120.0, q["r_fl"] - g("witness.tick_depth") / 2, -1, q["z_top"] + 1)
    feats = [
        C.chk("holder outer diameter (D) = 2 (register r - g_reg)"''')
rep('''    res = C.base_result("holder", sh, feats, extra={"derived": {k: round(v, 4) for k, v in q.items()}}, t0=t0)''', '''    hd7 = [
        ("HD7 tick groove width (T)", tk_w[1][0] - tk_w[0][1] if len(tk_w) == 2 else None, g("witness.tick_width"), 0.02),
        ("HD7 tick groove depth from the flange OD (R)", q["r_fl"] - tk_r[-1][1] if tk_r else None, g("witness.tick_depth"), 0.02),
        ("HD7 tick groove height above the flange underside (A)", tk_a[0][0] - q["L"] if tk_a else None, g("witness.tick_height"), 0.02),
        ("HD7 tick lower edge = flange underside (A)", under_other[0][0] if under_other else None, g("holder.length"), 0.02),
        ("HD7 tick azimuth = witness.azimuth_deg (deg), groove empty at the azimuth, flange solid at +-120",
         az_w if (not sh.isInside(C.polar(q["r_fl"] - g("witness.tick_depth") / 2, az_w, q["L"] + 1.0), 1e-6, True)
                  and sh.isInside(C.polar(q["r_fl"] - g("witness.tick_depth") / 2, az_w + 120.0, q["L"] + 1.0), 1e-6, True)) else None, az_w, 0.01),
    ]
    for name, built, exp, tol in hd7:
        r = C.chk(name, built, exp, tol)
        r.update({"id": "HD7", "volume_mm3": round(tick_mm3, 3)})
        feats.append(r)
    res = C.base_result("holder", sh, feats, extra={"derived": {k: round(v, 4) for k, v in q.items()}, "booleans": bools, "boolean_count": len(bools),
                        "bbox_plain": S._bb(sh.BoundBox), "bbox_optimal": S._bb(C.bbox(sh)), "run_seconds": round(time.time() - t0, 1),
                        "witness": {"azimuth_deg": az_w, "tick_lowest_z": q["L"], "tick_height": g("witness.tick_height")},
                        "rebuild": S.rebuild_record(before, sh, ("HD7", "AC5"), bools)}, t0=t0)''')
open(p, "w", encoding="utf-8").write(s)
print("patched")
