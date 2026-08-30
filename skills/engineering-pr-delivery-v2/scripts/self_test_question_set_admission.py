#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
VALIDATOR = HERE / "validate_question_set_admission.py"

LEGACY_ENDPOINT = """CHAIN_ID: X
ENDPOINT_ID: EP-1
QUALIFICATION_BASIS_HEAD: 0123456789012345678901234567890123456789
QUESTION_SET_ID: QS-X-1
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
"""

V2_ENDPOINT = """CHAIN_ID: X
ENDPOINT_ID: EP-1
QUALIFICATION_BASIS_HEAD: 0123456789012345678901234567890123456789
QUESTION_SET_ID: QS-X-1
QUALIFICATION_PROFILE_VERSION: 2
OWNER_QUALIFICATION_BASELINE_STATUS: SATISFIED
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
"""

BASE = """QUALIFICATION_PROTOCOL_VERSION: 3
CHAIN_ID: X
ENDPOINT_ID: EP-1
QUESTION_SET_ID: QS-X-1
QUALIFICATION_BASIS_HEAD: 0123456789012345678901234567890123456789
QUESTION_SET_ADMISSION_STATUS: {status}
ADMISSION_AUTHORITY_ID: verifier-a
BASIS_RETRIEVABLE: TRUE
TECHNICAL_DEPTH_STATUS: PASS
ROADMAP_AUTHORITY_STATUS: VALID
SOURCE_ORACLE_AUTHORITY_STATUS: VALID
{owner}
LEGACY_SET: {legacy}
ADMISSION_EVIDENCE: exact basis and governing authority checked
"""

ANSWER = """CANDIDATE_ID: candidate-b
"""


def receipt(status="VALID", owner="", legacy="TRUE"):
    return BASE.format(status=status, owner=owner, legacy=legacy)


def run(ep, admission, answer=None):
    with tempfile.TemporaryDirectory() as td:
        p = Path(td)
        epf = p / "ep.md"; epf.write_text(ep)
        rf = p / "admission.md"; rf.write_text(admission)
        cmd = [sys.executable, str(VALIDATOR), str(epf), str(rf)]
        if answer is not None:
            af = p / "answer.md"; af.write_text(answer); cmd.append(str(af))
        return subprocess.run(cmd, capture_output=True, text=True)


def main():
    cases = [
        ("legacy valid", LEGACY_ENDPOINT, receipt(), ANSWER, 0),
        ("authority contaminated", LEGACY_ENDPOINT, receipt(status="AUTHORITY_CONTAMINATED"), ANSWER, 1),
        ("candidate self admission", LEGACY_ENDPOINT, receipt().replace("verifier-a", "candidate-b"), ANSWER, 1),
        ("roadmap authority blocked", LEGACY_ENDPOINT, receipt().replace("ROADMAP_AUTHORITY_STATUS: VALID", "ROADMAP_AUTHORITY_STATUS: UNPROVEN"), ANSWER, 1),
        ("shallow status", LEGACY_ENDPOINT, receipt().replace("TECHNICAL_DEPTH_STATUS: PASS", "TECHNICAL_DEPTH_STATUS: FAIL"), ANSWER, 1),
        ("profile-v2 valid baseline", V2_ENDPOINT, receipt(owner="OWNER_BASELINE_STATUS: SATISFIED", legacy="FALSE"), ANSWER, 0),
        ("profile-v2 missing baseline receipt", V2_ENDPOINT, receipt(owner="", legacy="FALSE"), ANSWER, 1),
        ("profile-v2 baseline mismatch", V2_ENDPOINT, receipt(owner="OWNER_BASELINE_STATUS: NOT_APPLICABLE", legacy="FALSE"), ANSWER, 1),
        ("profile-v2 cannot claim legacy", V2_ENDPOINT, receipt(owner="OWNER_BASELINE_STATUS: SATISFIED", legacy="TRUE"), ANSWER, 1),
    ]
    failed = 0
    for name, ep, adm, answer, expected in cases:
        r = run(ep, adm, answer)
        ok = r.returncode == expected
        print(("PASS" if ok else "FAIL") + ": " + name)
        if not ok:
            print(r.stdout + r.stderr); failed += 1
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
