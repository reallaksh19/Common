#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys
import tempfile

HERE=Path(__file__).resolve().parent
VALIDATOR=HERE/"validate_post_basis_drift.py"

BASE="""QUALIFICATION_PROTOCOL_VERSION: 3
CHAIN_ID: X
ENDPOINT_ID: EP-1
QUESTION_SET_ID: QS-X-1
QUALIFICATION_BASIS_HEAD: 0123456789012345678901234567890123456789
CANDIDATE_ID: candidate
RECONCILIATION_REVIEWER_ID: reviewer
LIVE_HEAD: 1111111111111111111111111111111111111111
POST_BASIS_COMMITS: abc123;def456
POST_BASIS_DRIFT: {drift}
QUALIFICATION_COVERAGE: {coverage}
CURRENT_STATE_AUTHORITY: {current}
WRITE_AUTHORITY_DECISION: {decision}
RECONCILIATION_EVIDENCE: compared every post-basis commit and authority boundary
"""

def run(text):
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/"r.md"; p.write_text(text)
        return subprocess.run([sys.executable,str(VALIDATOR),str(p)],capture_output=True,text=True)

def main():
    cases=[
        ("metadata retained write", BASE.format(drift="METADATA_ONLY",coverage="RETAINED",current="CLEAR",decision="WRITE_ALLOWED"),0),
        ("material within independently confirmed", BASE.format(drift="MATERIAL_WITHIN_QUALIFIED_BOUNDARY",coverage="INDEPENDENTLY_CONFIRMED",current="CLEAR",decision="WRITE_ALLOWED"),0),
        ("material boundary requal read only", BASE.format(drift="MATERIAL_BOUNDARY_CHANGED",coverage="REQUALIFICATION_REQUIRED",current="BLOCKED",decision="READ_ONLY"),0),
        ("authority changed cannot write", BASE.format(drift="AUTHORITY_CHANGED",coverage="RETAINED",current="CLEAR",decision="WRITE_ALLOWED"),1),
        ("contaminated cannot write", BASE.format(drift="CONTAMINATED",coverage="REQUALIFICATION_REQUIRED",current="CLEAR",decision="WRITE_ALLOWED"),1),
        ("candidate cannot self-confirm", BASE.format(drift="MATERIAL_WITHIN_QUALIFIED_BOUNDARY",coverage="INDEPENDENTLY_CONFIRMED",current="CLEAR",decision="WRITE_ALLOWED").replace("RECONCILIATION_REVIEWER_ID: reviewer","RECONCILIATION_REVIEWER_ID: candidate"),1),
        ("blocked cannot write", BASE.format(drift="METADATA_ONLY",coverage="RETAINED",current="BLOCKED",decision="WRITE_ALLOWED"),1),
    ]
    failed=0
    for name,text,expected in cases:
        r=run(text); ok=r.returncode==expected
        print(("PASS" if ok else "FAIL")+": "+name)
        if not ok:
            print(r.stdout+r.stderr); failed+=1
    return 1 if failed else 0

if __name__=="__main__":
    raise SystemExit(main())
