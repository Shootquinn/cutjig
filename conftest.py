"""pytest root config. Puts the project root on sys.path; params fixture loads params.yaml.
Registers the Step 4 markers and enforces the label rule: every test carries exactly one of discriminator|invariant and
exactly one green_at_N; an invariant carries green_at_4."""
import copy
import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

LABELS = ("discriminator", "invariant")
GREEN = (4, 5, 6, 7, 8, 10, 12)


def pytest_configure(config):
    config.addinivalue_line("markers", "discriminator: fails at baseline B4 because the artifact or feature is absent; becomes the build target")
    config.addinivalue_line("markers", "invariant: passes at B4 and stays green (includes zero and known-bad controls)")
    for n in GREEN:
        config.addinivalue_line("markers", f"green_at_{n}: the step that builds the measured artifact is step {n}")


def pytest_collection_modifyitems(config, items):
    bad = []
    for it in items:
        names = [m.name for m in it.iter_markers()]
        labels = {n for n in names if n in LABELS}
        greens = {n for n in names if n.startswith("green_at_")}
        if len(labels) != 1 or len(greens) != 1:
            bad.append(f"{it.nodeid}: labels {sorted(labels)} greens {sorted(greens)}")
        elif "invariant" in labels and "green_at_4" not in greens:
            bad.append(f"{it.nodeid}: invariant without green_at_4")
    if bad:
        raise pytest.UsageError("label rule violated:\n" + "\n".join(bad[:20]))


@pytest.fixture(scope="session")
def root():
    return ROOT


@pytest.fixture
def params():
    from build_parts import common
    return common.load_params()


@pytest.fixture
def mutated(params):
    """Return a function that deep-copies params and sets one leaf value.
    Raises KeyError on a missing key, so a known-bad test cannot pass on an empty file."""
    from build_parts import common

    def _mut(key, value):
        p = copy.deepcopy(params)
        common.set_value(p, key, value)
        return p
    return _mut
