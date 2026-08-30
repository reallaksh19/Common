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


def detailed_q(n, title, payload):
    return f"""#### Q{n} — {title}
Repository anchors: src/mesh.js; src/element.js
Production object/case: element 17 node 6
Domain challenge: reconstruct mesh element node Jacobian equilibrium evidence
Exact repository data required: actual bounded mesh/element case
Concrete payload: {payload}
Required derivation: derive exact Jacobian/equilibrium intermediate and falsifier
Calculation/reconstruction: compute exact bounded quantity
Required technical work: trace authority and calculate expected result
Required numerical/technical evidence: exact values
Predicted intermediate values: exact values
First authority/ownership boundaries: mesh to element
First wrong boundary: first mismatching boundary
Authority/source trace: source to mesh to solver
Protected invariant: numerical authority
Falsifier: one exact mismatch
Invalid shortcut: prose-only answer
Independent oracle: independent reconstruction
Units/sign/tolerance: exact
Safe patch boundary: smallest legal change
Expected before/after evidence: exact
Protected unchanged domains: solver
Validation required: focused regression
Negative test: adjacent near-miss
Rollback/falsifier boundary: revert on neighbor regression
No-patch condition: source/environment issue
Fail if: answer is descriptive only
"""


def make(root, *, status="CURRENT", profile="FEA", history_root=BASIS, work_key="task:test", instance=INSTANCE, source="OWNER_DIRECT"):
    (root / "AGENTS.md").write_text(OVERLAY, encoding="utf-8")
    d = root / "agents/chains/T/endpoints"; d.mkdir(parents=True)
    ep_rel = "agents/chains/T/endpoints/EP-0001.md"
    questions = "\n".join([
        "Q1: Trace mesh element 17 and node 6 through solver boundaries using F=1000 N and exact repository identifiers.",
        "Q2: Using N1=(0,0), N2=(40,0), N3=(0,30), calculate the Jacobian and det J at the specified integration point.",
        "Q3: Prove mesh/element numerical authority for element=17, node=6, load=1000 N and state the falsifying boundary.",
        "Q4: For a=10 mm, R=100 mm and sigma=50 MPa, derive an independent Kirsch oracle and compare expected traction.",
        "Q5: With before=0, after=1 and tolerance=0, define the smallest safe patch, rollback, negative test and NO-PATCH case.",
    ])
    pack = "\n".join([
        detailed_q(1, "Production Trace", "x=0, y=0, F=1000 N"),
        detailed_q(2, "Current Unresolved Problem / Failure Isolation", "N1=(0,0), N2=(40,0), N3=(0,30) mm"),
        detailed_q(3, "Authority / Invariant", "element=17, node=6, load=1000 N"),
        detailed_q(4, "Independent Validation", "a=10 mm, R=100 mm, sigma=50 MPa"),
        detailed_q(5, "Next Contribution / Minimal Patch", "before=0, after=1, tolerance=0"),
    ])
    ep = f"""# EP-0001
COMMON_PROTOCOL: engineering-pr-delivery-v2
COMMON_PROTOCOL_BASIS: {BASIS}
COMMON_PROTOCOL_STATUS: {status}
PREWORK_QUALIFICATION_READY: TRUE
QUALIFICATION_PROFILE: {profile}
QUALIFICATION_PROFILE_VERSION: 2
WORK_ITEM_SOURCE: {source}
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
QUALIFICATION_PROTOCOL_VERSION: 3
QUESTION_SET_ID: QS-T-1
QUESTION_SET_ADMISSION_REQUIREMENT: REQUIRED_ON_TAKEOVER
{pack}
"""
    (root / ep_rel).write_text(ep, encoding="utf-8")
    active = root / "agents/chains/T/ACTIVE.md"
    active.write_text(f"""CHAIN_STATE_VERSION: 3
CHAIN_ID: T
ACTIVE_ENDPOINT_FILE: {ep_rel}
MATERIAL_HISTORY_ROOT_BASE: {history_root}
MATERIAL_LEG_PREWORK_ENDPOINT_FILE: {ep_rel}
COMMON_PROTOCOL: engineering-pr-delivery-v2
COMMON_PROTOCOL_BASIS: {BASIS}
COMMON_PROTOCOL_STATUS: {status}
WORK_ITEM_SOURCE: {source}
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
    cases = [
        ("current non-issue material leg", {}, 0),
        ("stale protocol blocks leg", {"status": "STALE_PROTOCOL"}, 1),
        ("unknown qualification profile rejected", {"profile": "UNKNOWN"}, 1),
        ("invalid material history root rejected", {"history_root": "NOT_A_SHA"}, 1),
        ("missing work-item key rejected", {"work_key": ""}, 1),
        ("invalid work-item source rejected", {"source": "CHAT"}, 1),
        ("model label cannot be agent instance", {"instance": "OPENAI-GPT-5.6-SOL"}, 1),
    ]
    for name, kwargs, rc in cases:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); active = make(root, **kwargs); ok &= expect(name, run(root, active), rc)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
