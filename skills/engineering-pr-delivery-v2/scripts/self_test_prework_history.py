#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
VALIDATOR = HERE / "validate_prework_history.py"

PREWORK = """CHAIN_ID: T
ENDPOINT_ID: EP-0001
COMMON_PROTOCOL: engineering-pr-delivery-v2
COMMON_PROTOCOL_STATUS: CURRENT
PREWORK_QUALIFICATION_READY: TRUE
QUALIFICATION_PROFILE: FEA
QUALIFICATION_PROTOCOL_VERSION: 3
QUESTION_SET_STATUS: CURRENT
QUESTION_SET_ADMISSION_REQUIREMENT: REQUIRED_ON_TAKEOVER
#### Q1 — Production Trace
x
#### Q2 — Current Unresolved Problem / Failure Isolation
x
#### Q3 — Authority / Invariant
x
#### Q4 — Independent Validation
x
#### Q5 — Next Contribution / Minimal Patch
x
"""

ACTIVE = """CHAIN_STATE_VERSION: 3
CHAIN_ID: T
MATERIAL_LEG_PREWORK_ENDPOINT_FILE: agents/chains/T/endpoints/EP-0001.md
"""


def sh(root, *args):
    return subprocess.run([*args], cwd=root, check=True, capture_output=True, text=True).stdout.strip()


def init(root):
    sh(root, "git", "init", "-q")
    sh(root, "git", "config", "user.email", "test@example.com")
    sh(root, "git", "config", "user.name", "Test")
    (root / "README.md").write_text("base\n")
    sh(root, "git", "add", "."); sh(root, "git", "commit", "-qm", "base")
    return sh(root, "git", "rev-parse", "HEAD")


def add_prework(root, with_material=False):
    ep = root / "agents/chains/T/endpoints/EP-0001.md"; ep.parent.mkdir(parents=True, exist_ok=True); ep.write_text(PREWORK)
    active = root / "agents/chains/T/ACTIVE.md"; active.write_text(ACTIVE)
    if with_material:
        p = root / "src/model.js"; p.parent.mkdir(parents=True, exist_ok=True); p.write_text("export const x = 1;\n")
    sh(root, "git", "add", "."); sh(root, "git", "commit", "-qm", "prework")


def add_material(root):
    p = root / "src/model.js"; p.parent.mkdir(parents=True, exist_ok=True); p.write_text("export const x = 2;\n")
    sh(root, "git", "add", "."); sh(root, "git", "commit", "-qm", "material")


def run(root, base):
    active = root / "agents/chains/T/ACTIVE.md"
    return subprocess.run([sys.executable, str(VALIDATOR), str(root), base, "HEAD", str(active)], capture_output=True, text=True)


def expect(name, result, rc):
    ok = result.returncode == rc
    print(("PASS" if ok else "FAIL"), "SELF-TEST:", name)
    if not ok: print(result.stdout, result.stderr)
    return ok


def main():
    ok = True
    with tempfile.TemporaryDirectory() as td:
        root = Path(td); base = init(root); add_prework(root); add_material(root); ok &= expect("prework commit precedes material", run(root, base), 0)
    with tempfile.TemporaryDirectory() as td:
        root = Path(td); base = init(root); add_prework(root, with_material=True); ok &= expect("same-commit prework plus material rejected", run(root, base), 1)
    with tempfile.TemporaryDirectory() as td:
        root = Path(td); base = init(root); add_material(root); add_prework(root); ok &= expect("material before prework rejected", run(root, base), 1)
    with tempfile.TemporaryDirectory() as td:
        root = Path(td); init(root); add_prework(root); base = sh(root, "git", "rev-parse", "HEAD"); add_material(root); ok &= expect("prework existing at exact base accepted", run(root, base), 0)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
