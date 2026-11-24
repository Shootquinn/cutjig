import os, time, pathlib
R = pathlib.Path(r"C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig")
base = {}
for ln in open(R / "research" / "quinn" / "cr_scratch" / "step7_fcstd_mtimes_before.txt", encoding="utf-8"):
    p = ln.split()
    if len(p) >= 2:
        base[p[0]] = p[1]
now = {f.name: time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(f.stat().st_mtime)) for f in (R / "parts_cache").iterdir() if f.is_file()}
mod = sorted(n for n in base if n in now and now[n] != base[n])
new = sorted(n for n in now if n not in base)
gone = sorted(n for n in base if n not in now)
print("baseline files", len(base), "now", len(now))
print("modified", mod)
print("new", new)
print("missing", gone)
print("fcbak in parts_cache/results:", [str(p) for d in ("parts_cache", "results") for p in (R / d).rglob("*.FCBak")])
