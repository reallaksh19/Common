#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
VALIDATOR = HERE / "validate_leg_adoption.py"
BASIS = "36068fde5b860ca1870311b166d28077b4c0bcf8"

OVERLAY = f"""# Project overlay
COMMON_POLICY_SOURCE: reallaksh19/Common/skills/engineering-pr-delivery-v2/
COMMON_POLICY_REFERENCE: reallaksh19/Common/skills/engineering-pr-delivery-v2/references/repository-agent-policy.md
COMMON_PROTOCOL_MINIMUM_BASIS: {BASIS}
LOCAL_POLICY_SCOPE: PROJECT_ONLY
LEGACY_RELAY_WRITES: FORBIDDEN
## Project identity / criticality
engineering
"""


def make(root: Path, *, status="CURRENT", prework="TRUE", legacy=False):
    (root / "AGENTS.md").write_text(OVERLAY, encoding="utf-8")
    if legacy:
        chain = root / "agents/agentchain/T"
        chain.mkdir(parents=True)
        ep_rel = "agents/agentchain/T/EP-0001.md"
        active = root / "agents/agentchain/T/ACTIVE.md"
    else:
        chain = root / "agents/chains/T/endpoints"
        chain.mkdir(parents=True)
        ep_rel = "agents/chains/T/endpoints/EP-0001.md"
        active = root / "agents/chains/T/ACTIVE.md"
    ep = root / ep_rel
    ep.write_text(f"""# EP-0001
COMMON_PROTOCOL: engineering-pr-delivery-v2
COMMON_PROTOCOL_BASIS: {BASIS}
COMMON_PROTOCOL_STATUS: {status}
PREWORK_QUALIFICATION_READY: {prework}
HANDOVER_READY: TRUE
QUESTION_SET_STATUS: CURRENT
QUALIFICATION_PROTOCOL_VERSION: 3
QUESTION_SET_ADMISSION_REQUIREMENT: REQUIRED_ON_TAKEOVER
### Handover snapshot
Repo: R
Task: T
Q1: trace
Q2: calculate
Q3: falsify
Q4: oracle
Q5: safe patch
### Takeover qualification pack
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
""", encoding="utf-8")
    active.write_text(f"""CHAIN_STATE_VERSION: 3
CHAIN_ID: T
ACTIVE_ENDPOINT_FILE: {ep_rel}
COMMON_PROTOCOL: engineering-pr-delivery-v2
COMMON_PROTOCOL_BASIS: {BASIS}
COMMON_PROTOCOL_STATUS: {status}
HANDOVER_READY: TRUE
""", encoding="utf-8")
    return active


def run(root, active):
    return subprocess.run([sys.executable, str(VALIDATOR), str(root), str(active)], capture_output=True, text=True)


def expect(name, result, rc):
    ok = result.returncode == rc
    print(("PASS" if ok else "FAIL"), "SELF-TEST:", name)
    if not ok:
        print(result.stdout, result.stderr)
    return ok


def main():
    ok = True
    with tempfile.TemporaryDirectory() as td:
        root = Path(td); active = make(root); ok &= expect("current v3 pre-work leg", run(root, active), 0)
    with tempfile.TemporaryDirectory() as td:
        root = Path(td); active = make(root, status="STALE_PROTOCOL"); ok &= expect("stale protocol blocks leg", run(root, active), 1)
    with tempfile.TemporaryDirectory() as td:
        root = Path(td); active = make(root, prework="FALSE"); ok &= expect("code-first/question-later marker rejected", run(root, active), 1)
    with tempfile.TemporaryDirectory() as td:
        root = Path(td); active = make(root, legacy=True); ok &= expect("legacy relay path rejected for new leg", run(root, active), 1)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
