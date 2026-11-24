import json, os, glob
T = r"C:\Users\Quinn Morley\AppData\Local\Temp\rend7\results.json"
rows = {r["name"]: r for r in json.load(open(T))}
for r in json.load(open(T + ".test")): rows[r["name"]] = r
D = r"C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\cr_scratch\step7_renders"
files = sorted(os.path.basename(f)[:-4] for f in glob.glob(D + r"\*.png"))
missing = [f for f in files if f not in rows]; extra = [k for k in rows if k not in files]
print("files", len(files), "rows", len(rows), "missing", missing, "extra", extra)
L = [r"Source: parts_cache\assembly\pose_<P>_<tag>.FCStd (read only) and output\jig_assembly.FCStd (tray, plug, stop, feet, caddy, gauge, rest). Renderer: cr_scratch\step7_render.py, freecadcmd 1.1.4, orthographic, Flat Lines, 1600 x 1200, background 204/207/212. Pose frame z = floor frame + 40. Views: front looks along +Y (+X right); side looks along -X from +X; top looks down, +Y up; bottom looks up, +Y up; iso camera at +X -Y +Z. Cutter keep-out transparent in whole-assembly and context views. Collet colour from params collet.colour by size index (90 red, 100 blue, 105 white). Sections: the receiver and nut are cut from the tessellation with a cap face where the OCC boolean fails (logged FALLBACK). Underside views: dark backdrop (60/60/65), part colours unchanged. Fix pass 2026-11-11: receiver sections, collet colours, core top sections, stop pad phantom column, context cutter transparency. Sections remove the half-space on the viewer side.",
     "", "| File | Pose | Size | View | Rubric items |", "|---|---|---|---|---|"]
for f in files:
    r = rows[f]
    L.append("| %s\%s.png | %s | %s | %s | %s |" % (D, f, r["pose"], r["size"], r["view"], r["ids"]))
open(D + r"\INDEX.md", "w").write("\n".join(L) + "\n")
cs = sorted((rows[f]["cov"], f) for f in files)
print("min cov", cs[:5], "max", cs[-2:], "blank", [f for c, f in cs if c < 0.5])
