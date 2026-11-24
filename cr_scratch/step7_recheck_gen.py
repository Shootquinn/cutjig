import os, datetime, json, sys
ROOT = r"C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig"
base = {}
for l in open(os.path.join(ROOT, "cr_scratch", "step7_fcstd_mtimes_before.txt")):
    p = l.rstrip("\n").split("\t")
    if len(p) >= 2:
        base[p[0]] = p[1]
out = []
pc = os.path.join(ROOT, "parts_cache")
for root, _, fs in os.walk(pc):
    for f in fs:
        if not (f.endswith(".FCStd") or f.endswith(".json") or f.endswith(".FCBak")):
            continue
        full = os.path.join(root, f)
        rel = os.path.relpath(full, pc).replace(chr(92), "/")
        m = datetime.datetime.fromtimestamp(os.path.getmtime(full)).strftime("%Y-%m-%dT%H:%M:%S")
        if rel not in base:
            out.append((rel, m, "NEW"))
        elif base[rel] != m:
            out.append((rel, m, "MODIFIED"))
json.dump(out, open(os.path.join(ROOT, "cr_scratch", "step7_recheck_raw.json"), "w"))
for o in sorted(out):
    print(*o)
print("missing", [k for k in base if not os.path.exists(os.path.join(pc, k))])
print("gen_time", datetime.datetime.now().isoformat(timespec="seconds"))
