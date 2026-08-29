#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
VALIDATOR = HERE / "validate_material_leg_history.py"

PREWORK = """COMMON_PROTOCOL: engineering-pr-delivery-v2
COMMON_PROTOCOL_STATUS: CURRENT
PREWORK_QUALIFICATION_READY: TRUE
QUALIFICATION_PROFILE: GENERAL_ENGINEERING
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


def sh(root, *args):
    return subprocess.run(args, cwd=root, check=True, capture_output=True, text=True).stdout.strip()


def commit(root, message):
    sh(root, "git", "add", ".")
    sh(root, "git", "commit", "-qm", message)
    return sh(root, "git", "rev-parse", "HEAD")


def init(root):
    sh(root, "git", "init", "-q")
    sh(root, "git", "config", "user.email", "test@example.com")
    sh(root, "git", "config", "user.name", "Test")
    (root / "README.md").write_text("base\n")
    base = commit(root, "base")
    chain = root / "agents/chains/T"
    (chain / "endpoints").mkdir(parents=True)
    active = chain / "ACTIVE.md"
    active.write_text(f"CHAIN_STATE_VERSION: 3\nCHAIN_ID: T\nMATERIAL_HISTORY_ROOT_BASE: {base}\n")
    commit(root, "relay root")
    return base, chain


def add_prework(root, chain, ep):
    p = chain / "endpoints" / f"{ep}.md"
    p.write_text(PREWORK)
    return commit(root, f"prework {ep}")


def add_material(root, name, value):
    p = root / "src" / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(value)
    return commit(root, f"material {name}")


def add_receipt(root, chain, leg, previous, base, prework_ep, head):
    d = chain / "material-legs"; d.mkdir(exist_ok=True)
    (d / f"{leg}.md").write_text(f"""CHAIN_ID: T
MATERIAL_LEG_ID: {leg}
PREVIOUS_MATERIAL_LEG: {previous}
MATERIAL_LEG_BASE: {base}
MATERIAL_LEG_PREWORK_ENDPOINT_FILE: agents/chains/T/endpoints/{prework_ep}.md
MATERIAL_LEG_HEAD: {head}
MATERIAL_LEG_HISTORY_STATUS: RECORDED
MATERIAL_SCOPE: test
""")
    return commit(root, f"receipt {leg}")


def run(root):
    return subprocess.run([sys.executable, str(VALIDATOR), str(root)], capture_output=True, text=True)


def expect(name, result, rc):
    ok = result.returncode == rc
    print(("PASS" if ok else "FAIL"), "SELF-TEST:", name)
    if not ok:
        print(result.stdout, result.stderr)
    return ok


def build_two_leg(root, omit_second=False, gap_material=False):
    root_base, chain = init(root)
    add_prework(root, chain, "EP-0001")
    leg1_base = sh(root, "git", "rev-parse", "HEAD")
    h1 = add_material(root, "a.js", "1\n")
    add_receipt(root, chain, "LEG-001", "NONE", leg1_base, "EP-0001", h1)
    add_prework(root, chain, "EP-0002")
    if gap_material:
        add_material(root, "gap.js", "gap\n")
    leg2_base = sh(root, "git", "rev-parse", "HEAD")
    h2 = add_material(root, "b.js", "2\n")
    if not omit_second:
        add_receipt(root, chain, "LEG-002", "LEG-001", leg2_base, "EP-0002", h2)


def main():
    ok = True
    with tempfile.TemporaryDirectory() as td:
        root = Path(td); build_two_leg(root); ok &= expect("two fully receipted material legs", run(root), 0)
    with tempfile.TemporaryDirectory() as td:
        root = Path(td); build_two_leg(root, omit_second=True); ok &= expect("unreceipted trailing material rejected", run(root), 1)
    with tempfile.TemporaryDirectory() as td:
        root = Path(td); build_two_leg(root, gap_material=True); ok &= expect("material hidden in inter-leg relay gap rejected", run(root), 1)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
