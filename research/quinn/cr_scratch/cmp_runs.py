import sys
import xml.etree.ElementTree as ET
from collections import Counter


def load(path):
    out = {}
    for tc in ET.parse(path).getroot().iter("testcase"):
        key = tc.get("classname") + "::" + tc.get("name")
        st = "pass"
        msg = ""
        for ch in tc:
            if ch.tag in ("failure", "error"):
                st = "fail"
                msg = (ch.get("message") or "")[:160]
            elif ch.tag == "skipped":
                st = "skip"
        out[key] = (st, msg)
    return out


a = load(sys.argv[1])
b = load(sys.argv[2])
print("collected", len(a), len(b))
print("pass", sum(1 for v in a.values() if v[0] == "pass"), sum(1 for v in b.values() if v[0] == "pass"))
reg = [k for k, v in a.items() if v[0] == "pass" and b.get(k, ("missing",))[0] != "pass"]
print("regressions", len(reg))
for k in reg:
    print("  REG", k, b.get(k))
new = [k for k, v in b.items() if v[0] == "pass" and a.get(k, ("missing",))[0] != "pass"]
print("newly passing", len(new))
fails = Counter()
kinds = Counter()
for k, v in b.items():
    if v[0] == "fail":
        fails[k.split("::")[0].split(".")[-1]] += 1
        m = v[1]
        kinds["MISSING" if "MISSING" in m else "ABSENT FEATURE" if "ABSENT FEATURE" in m else "OTHER"] += 1
print("fails by file", dict(fails))
print("fail kinds", dict(kinds))
if len(sys.argv) > 3:
    for k, v in b.items():
        if v[0] == "fail" and ("step6" in k):
            print("  F6", k.split("::")[-1], "|", v[1])
