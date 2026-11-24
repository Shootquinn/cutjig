"""Importing a probe module from another probe must have no side effects (Step 7: probe_ws imported probe_poses, whose guard also matches the module name,
and ran the full pose sweep for 5 h). The flag CJ_PROBE_IMPORT suppresses the module-name branch of the guard."""
import os
import pathlib
import subprocess
import sys

import cad_helpers as H

ROOT = H.ROOT


def _import(flag):
    env = dict(os.environ)
    env.pop("CJ_PROBE_IMPORT", None)
    if flag:
        env["CJ_PROBE_IMPORT"] = "1"
    code = "import sys; sys.path.insert(0, r'%s'); sys.path.insert(0, r'%s'); import probe_poses" % (ROOT / "tests" / "probes", ROOT)
    r = subprocess.run([sys.executable, "-c", code], env=env, capture_output=True, text=True, cwd=str(ROOT))
    return r.stdout + r.stderr


@H.label("invariant", 4)
def test_importing_probe_poses_with_the_flag_runs_nothing():
    out = _import(True)
    assert "PROBE_" not in out and "Traceback" not in out, out


@H.label("invariant", 4)
def test_control_importing_without_the_flag_does_run_main():
    assert "PROBE_FAILED" in _import(False)      # known-bad: the unguarded import enters main (no FreeCAD here, so it reports PROBE_FAILED)


@H.label("invariant", 4)
def test_probe_ws_sets_the_flag_before_importing_probe_poses():
    src = (ROOT / "tests" / "probes" / "probe_ws.py").read_text(encoding="utf-8")
    assert src.index("CJ_PROBE_IMPORT") < src.index("import probe_poses")
