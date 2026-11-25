"""Step 3 scripted checks (research/sean/gameplan.md detail 1.0 l.158, detail 3 l.375-381).

Q3-0 (batch mode, Step 1.0): every row of a question batch has an ID, a question,
a feed and a stand-in carrying the word ASSUMED.
Q3-1 (table mode, Step 3): reserved; added as its own function and CLI branch
without touching Q3-0.

Usage:
    step3_check.py --batch <path> [--json <out>]
    step3_check.py --table <path> [--json <out>]   (Q3-1, not yet implemented)

Exit 0 on pass, 1 on fail, 2 on usage error or unimplemented mode.
"""
import argparse
import datetime
import json
import re
import sys
from pathlib import Path

# Q3-0 column roles: role -> predicate on the lower-cased header text.
Q30_COLUMNS = {
    "id": lambda h: h == "id",
    "question": lambda h: h == "question",
    "feeds": lambda h: h.startswith("feeds"),
    "standin": lambda h: "assumed" in h or h.startswith("value used"),
}
Q30_STANDIN_WORD = re.compile(r"\bASSUMED\b")


def _split_row(line):
    """Split one markdown table line into stripped cells."""
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return [c.strip() for c in s.split("|")]


def _is_separator(cells):
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", c) for c in cells)


def parse_tables(text):
    """Return a list of tables; each is (header_cells, [(line_no, cells), ...])."""
    tables = []
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        if lines[i].strip().startswith("|") and i + 1 < len(lines) \
                and _is_separator(_split_row(lines[i + 1])):
            header = _split_row(lines[i])
            rows = []
            j = i + 2
            while j < len(lines) and lines[j].strip().startswith("|"):
                rows.append((j + 1, _split_row(lines[j])))
                j += 1
            tables.append((header, rows))
            i = j
        else:
            i += 1
    return tables


def check_q30(path):
    """Q3-0 on a batch file. Returns a result dict."""
    p = Path(path)
    result = {"check": "Q3-0", "file": str(p),
              "timestamp": datetime.datetime.now().isoformat(timespec="seconds"),
              "rows": [], "failures": []}
    if not p.is_file():
        result["failures"].append(f"file not found: {p}")
        result["result"] = "FAIL"
        return result
    tables = parse_tables(p.read_text(encoding="utf-8"))
    table = None
    colmap = {}
    for header, rows in tables:
        low = [h.lower() for h in header]
        cand = {}
        for role, pred in Q30_COLUMNS.items():
            idx = [k for k, h in enumerate(low) if pred(h)]
            if idx:
                cand[role] = idx[0]
        if len(cand) == len(Q30_COLUMNS):
            table, colmap = (header, rows), cand
            break
    if table is None:
        result["failures"].append(
            "no table with columns ID, Question, Feeds, Value used until answered (ASSUMED)")
        result["result"] = "FAIL"
        return result
    header, rows = table
    if not rows:
        result["failures"].append("table has no rows")
    for line_no, cells in rows:
        cells = cells + [""] * (len(header) - len(cells))
        rid = cells[colmap["id"]]
        row = {"line": line_no, "id": rid, "failures": []}
        for role in ("id", "question", "feeds", "standin"):
            if not cells[colmap[role]]:
                row["failures"].append(f"blank {role}")
        standin = cells[colmap["standin"]]
        if standin and not Q30_STANDIN_WORD.search(standin):
            row["failures"].append("stand-in lacks status word ASSUMED")
        for f in row["failures"]:
            result["failures"].append(f"line {line_no} row '{rid}': {f}")
        result["rows"].append(row)
    result["row_count"] = len(rows)
    result["result"] = "FAIL" if result["failures"] else "PASS"
    return result


def check_q31(path):
    """Q3-1 (detail 3): Open Questions table closeout. Added at Step 3."""
    raise NotImplementedError("Q3-1 is added at Step 3 (gameplan detail 3)")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--batch", help="question batch file (Q3-0)")
    mode.add_argument("--table", help="Open Questions table file (Q3-1)")
    ap.add_argument("--json", help="write the result JSON here")
    a = ap.parse_args(argv)
    if a.table:
        try:
            res = check_q31(a.table)
        except NotImplementedError as e:
            print(str(e), file=sys.stderr)
            return 2
    else:
        res = check_q30(a.batch)
    out = json.dumps(res, indent=2)
    if a.json:
        Path(a.json).write_text(out + "\n", encoding="utf-8")
    print(f"{res['check']} {res['result']} {res['file']}")
    for f in res["failures"]:
        print(f"  {f}")
    return 0 if res["result"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
