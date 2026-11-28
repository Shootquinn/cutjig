"""DEPS controls for the frozen record tree (1.4 P10f, Manager close N1; research/sean/cr_scratch/step1.4_engineer_close_fixes.md).

Premise: every DEPS control reads its accepted records from fixtures/deps_tree/ (byte copies of the save-point-5 s1 r8,
s2 r9, s3 r7 records, the S1 r8 mass report and deps_exempt.json), never from the live record set at the top level of
docs/sketches/, and the frozen tree matches its own exemption SHA-256. step14_fixtures holds the guard (_frozen) and the
premise lint (deps_frozen_issues). On the pre-change step14_fixtures (neither present) each B reads clean, so it is red
there (mismatch), and DEPS-Z6 errors.
"""
import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SK = HERE.parent
for p in (str(SK), str(HERE)):
    if p not in sys.path:
        sys.path.insert(0, p)
import step14_fixtures as s14  # noqa: E402
from sketch_loader import load_yaml  # noqa: E402

_GUARD = getattr(s14, "_frozen", lambda f: f)
_LINT = getattr(s14, "deps_frozen_issues", None)


def _man():
    return load_yaml(HERE / "manifest.yaml")["controls"]


def _lint_res(issues, what):
    return s14._res("DEPS", bool(issues), s14.sc._summ(issues) if issues else what, len(issues))


@_GUARD
def deps_z6_frozen_premise():
    """DEPS Z6: live manifest and fixtures/deps_tree/: every DEPS fixture guarded, the frozen tree complete and equal to
    its exemption SHA-256: clean."""
    return _lint_res(_LINT(_man()), "every DEPS fixture guarded; frozen tree matches its exemption")


def _unguarded():
    """A DEPS fixture without the guard (planted for B14)."""
    return s14._res("DEPS", False, "unguarded", 0)


@_GUARD
def deps_b14_unguarded():
    """DEPS B14: the live manifest plus one DEPS entry whose fixture lacks the guard."""
    man = _man() + [{"id": "DEPS-BX", "check": "DEPS", "control": "B", "fixture": "deps_frozen_fixtures.py::_unguarded"}]
    return _lint_res(_LINT(man) if _LINT else [], "lint absent")


def _reads_live():
    p = SK / "s3_checks_r7.json"
    try:   # the open is the plant: the audit event fires before the file is found, so a later removal of r7 keeps B15 red
        json.loads(p.read_text(encoding="utf-8"))
    except OSError:
        pass
    return s14._res("DEPS", False, "read s3_checks_r7.json from docs/sketches/", 0)


@_GUARD
def deps_b15_live_read():
    """DEPS B15: a guarded DEPS fixture that opens the live docs/sketches/s3_checks_r7.json."""
    return _reads_live()


@_GUARD
def deps_b16_frozen_edited():
    """DEPS B16: a temporary copy of fixtures/deps_tree/ with one field added to s1_checks_r8.json: its SHA-256 differs from
    the certifier SHA-256 the frozen exemption records (twice: S2 r9 and S3 r7 entries)."""
    t = s14._tmp() / "frozen"
    shutil.copytree(s14.FROZEN if hasattr(s14, "FROZEN") else HERE / "deps_tree", t)
    p = t / "s1_checks_r8.json"
    if p.is_file():
        r = json.loads(p.read_text(encoding="utf-8"))
        r["edited"] = "one field"
        p.write_text(json.dumps(r), encoding="utf-8")
    return _lint_res(_LINT([], t) if _LINT else [], "lint absent")
