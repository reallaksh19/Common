#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
VALIDATOR = HERE / "validate_leg_adoption.py"
BASIS = "36068fde5b860ca1870311b166d28077b4c0bcf8"
INSTANCE = "chatgpt:6c19e9d4-4be3-4f4c-9b4a-7a1f52d1e930"

OVERLAY = f"""# Project overlay
COMMON_POLICY_SOURCE: reallaksh19/Common/skills/engineering-pr-delivery-v2/
COMMON_POLICY_REFERENCE: reallaksh19/Common/skills/engineering-pr-delivery-v2/references/repository-agent-policy.md
COMMON_PROTOCOL_MINIMUM_BASIS: {BASIS}
LOCAL_POLICY_SCOPE: PROJECT_ONLY
LEGACY_RELAY_WRITES: FORBIDDEN
## Project identity / criticality
engineering
"""


def q(n, title, payload):
    return f"""#### Q{n} — {title}
Domain challenge: reconstruct bounded engineering evidence
Exact repository data required: actual bounded repository case
Concrete payload: {payload}
Required derivation: derive exact expected intermediate and falsifier
Calculation/reconstruction: compute exact bounded quantity
Required technical work: trace authority and calculate expected result
Required numerical/technical evidence: exact values
Predicted intermediate values: exact values
First wrong boundary: first mismatching boundary
Falsifier: one exact mismatch
Independent oracle: independent reconstruction
Units/sign/tolerance: exact
Safe patch boundary: smallest legal change
No-patch condition: source/environment issue
Fail if: answer is descriptive only
"""


def make(root: Path, *, status="CURRENT", prework="TRUE", legacy=False, profile="FEA", history_root=BASIS, work_key="github:o/r#1", instance=INSTANCE):
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
    questions = "\n".join([
        "Q1: Trace actual node/load route using x=0, y=0, F=1000 N and compute first boundary.",
        "Q2: For N1=(0,0), N2=(40,0), N3=(0,30), calculate the Jacobian and det J.",
        "Q3: Prove authority using element=17, node=6, load=1000 N and state one falsifier.",
        "Q4: For a=10 mm, R=100 mm, sigma=50 MPa, derive the independent boundary oracle.",
        "Q5: With before=0, after=1, tolerance=0, define minimal patch, rollback and NO-PATCH.",
    ])
    detailed = "\n".join([
        q(1, "Production Trace", "x=0, y=0, F=1000 N"),
        q(2, "Current Unresolved Problem / Failure Isolation", "N1=(0,0), N2=(40,0), N3=(0,30) mm"),
        q(3, "Authority / Invariant", "element=17, node=6, load=1000 N"),
        q(4, "Independent Validation", "a=10 mm, R=100 mm, sigma=50 MPa"),
        q(5, "Next Contribution / Minimal Patch", "before=0, after=1, tolerance=0"),
    ])
    ep.write_text(f"""# EP-0001
COMMON_PROTOCOL: engineering-pr-delivery-v2
COMMON_PROTOCOL_BASIS: {BASIS}
COMMON_PROTOCOL_STATUS: {status}
PREWORK_QUALIFICATION_READY: {prework}
QUALIFICATION_PROFILE: {profile}
QUALIFICATION_PROFILE_VERSION: 2
WORK_ITEM_KEY: {work_key}
WORK_ITEM_MODE: EXCLUSIVE
AGENT_INSTANCE_ID: {instance}
OWNER_QUALIFICATION_BASELINE_DISCOVERY: COMPLETE
OWNER_QUALIFICATION_BASELINE_SOURCE: NONE
OWNER_QUALIFICATION_BASELINE_MANIFEST: NONE
OWNER_QUALIFICATION_BASELINE_STATUS: NOT_APPLICABLE
HANDOVER_PROTOCOL_VERSION: 2
HANDOVER_CONTENT_READY: TRUE
HANDOVER_VALIDATION_STATUS: PASS
HANDOVER_VALIDATION_EVIDENCE: test:handover
HANDOVER_READY: TRUE
REPORTING_CONTRACT: ACTIVE_HANDOVER_FIRST
HANDOVER_RESPONSE_REQUIRED: ALWAYS
RESPONSE_DELTA_MODE: DELTA_ONLY
QUESTION_SET_STATUS: CURRENT
QUALIFICATION_PROTOCOL_VERSION: 3
QUESTION_SET_ADMISSION_REQUIREMENT: REQUIRED_ON_TAKEOVER
### Active handover snapshot
Repo: R
Task: T
Chain: T
Endpoint: EP-0001
PR: 1
PR status: DRAFT
Branch / PR head / main: b / h / m
Merge authority: OWNER_ONLY
Engineering / custody / qualification / write state: READY / HELD / NOT_REQUIRED / WRITE_ALLOWED
AUTO: NOT_APPLICABLE
Protocol basis / status: x / CURRENT
Roadmap: NONE
Inputs: I
Benchmarks: B
Governing docs / authoritative sources: S
Current blocker: NONE
Leg diagnosis: READY
Exact next action: test
### Active qualification questions
{questions}
### Takeover qualification pack
QUALIFICATION_PROFILE: {profile}
QUALIFICATION_PROFILE_VERSION: 2
QUESTION_SET_ID: QS-T-1
{detailed}
""", encoding="utf-8")
    active.write_text(f"""CHAIN_STATE_VERSION: 3
CHAIN_ID: T
ACTIVE_ENDPOINT_FILE: {ep_rel}
MATERIAL_HISTORY_ROOT_BASE: {history_root}
MATERIAL_LEG_PREWORK_ENDPOINT_FILE: {ep_rel}
COMMON_PROTOCOL: engineering-pr-delivery-v2
COMMON_PROTOCOL_BASIS: {BASIS}
COMMON_PROTOCOL_STATUS: {status}
WORK_ITEM_KEY: {work_key}
WORK_ITEM_MODE: EXCLUSIVE
AGENT_INSTANCE_ID: {instance}
OWNER_QUALIFICATION_BASELINE_DISCOVERY: COMPLETE
HANDOVER_PROTOCOL_VERSION: 2
HANDOVER_CONTENT_READY: TRUE
HANDOVER_VALIDATION_STATUS: PASS
HANDOVER_VALIDATION_EVIDENCE: test:handover
HANDOVER_READY: TRUE
REPORTING_CONTRACT: ACTIVE_HANDOVER_FIRST
HANDOVER_RESPONSE_REQUIRED: ALWAYS
RESPONSE_DELTA_MODE: DELTA_ONLY
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
        root = Path(td); active = make(root); ok &= expect("current P0 pre-work leg", run(root, active), 0)
    with tempfile.TemporaryDirectory() as td:
        root = Path(td); active = make(root, status="STALE_PROTOCOL"); ok &= expect("stale protocol blocks leg", run(root, active), 1)
    with tempfile.TemporaryDirectory() as td:
        root = Path(td); active = make(root, prework="FALSE"); ok &= expect("code-first/question-later marker rejected", run(root, active), 1)
    with tempfile.TemporaryDirectory() as td:
        root = Path(td); active = make(root, legacy=True); ok &= expect("legacy relay path rejected for new leg", run(root, active), 1)
    with tempfile.TemporaryDirectory() as td:
        root = Path(td); active = make(root, profile="UNKNOWN"); ok &= expect("unknown qualification profile rejected", run(root, active), 1)
    with tempfile.TemporaryDirectory() as td:
        root = Path(td); active = make(root, history_root="NOT_A_SHA"); ok &= expect("invalid material history root rejected", run(root, active), 1)
    with tempfile.TemporaryDirectory() as td:
        root = Path(td); active = make(root, work_key=""); ok &= expect("missing work-item key rejected", run(root, active), 1)
    with tempfile.TemporaryDirectory() as td:
        root = Path(td); active = make(root, instance="OPENAI-GPT-5.6-SOL"); ok &= expect("model label cannot be agent instance", run(root, active), 1)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
