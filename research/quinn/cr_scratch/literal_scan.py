"""Scan Step 6 scripts for numeric literals equal to a params value (the duplicating-literal defect)."""
import io
import sys
import tokenize

sys.path.insert(0, "C:/Users/Quinn Morley/OneDrive/PROJECTS/CC/CuttingJig")
from build_parts import common  # noqa: E402

p = common.load_params()
vals = {}


def add(v, key):
    if isinstance(v, bool):
        return
    if isinstance(v, (int, float)):
        vals.setdefault(round(float(v), 9), set()).add(key)
    elif isinstance(v, (list, tuple)):
        for x in v:
            add(x, key)
    elif isinstance(v, dict):
        for x in v.values():
            add(x, key)


for k, lf in common.iter_leaves(p):
    add(lf["value"], k)

TRIVIAL = {0.0, 1.0, 2.0, 3.0, 4.0, 0.5, 90.0, 180.0, 360.0, 120.0, 0.25, 10.0, 5.0}
files = sys.argv[1:]
hits = 0
for f in files:
    src = open(f, encoding="utf-8").read()
    for tok in tokenize.generate_tokens(io.StringIO(src).readline):
        if tok.type == tokenize.NUMBER:
            try:
                v = float(tok.string)
            except ValueError:
                continue
            if v in TRIVIAL:
                continue
            m = vals.get(round(v, 9))
            if m:
                hits += 1
                line = src.splitlines()[tok.start[0] - 1].strip()[:110]
                print("%s:%d  %s  = %s | %s" % (f.split("/")[-1].split("\\")[-1], tok.start[0], tok.string, sorted(m)[:3], line))
print("HITS", hits)
