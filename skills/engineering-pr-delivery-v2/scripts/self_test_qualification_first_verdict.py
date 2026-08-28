#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
VALIDATOR = HERE / "validate_qualification.py"


def artifacts(root, decision, protocol="3"):
    p = f"QUALIFICATION_PROTOCOL_VERSION: {protocol}\n" if protocol else ""
    answer = p + """CHAIN_ID: T
ENDPOINT_ID: EP-1
QUESTION_SET_ID: QS-T-1
QUALIFICATION_BASIS_HEAD: abc
CANDIDATE_ID: candidate
# Q1
answer
# Q2
answer
# Q3
answer
# Q4
answer
# Q5
answer
"""
    verdict = p + f"""CHAIN_ID: T
ENDPOINT_ID: EP-1
QUESTION_SET_ID: QS-T-1
QUALIFICATION_BASIS_HEAD: abc
CANDIDATE_ID: candidate
VERIFIER_ID: verifier
VERDICT_BASIS_HEAD: abc
AUTOMATIC_FAILURE_REASON: NONE
Q1 20 / 20
Q2 19 / 20
Q3 19 / 20
Q4 18 / 20
Q5 18 / 20
TOTAL 94 / 100
MINIMUM_QUESTION 18 / 20
VERDICT: {decision}
"""
    a = root / "a.md"; v = root / "v.md"
    a.write_text(answer); v.write_text(verdict)
    return a, v


def run(a, v):
    return subprocess.run([sys.executable, str(VALIDATOR), str(a), str(v)], capture_output=True, text=True)


def expect(name, r, rc):
    ok = r.returncode == rc
    print(("PASS" if ok else "FAIL"), "SELF-TEST:", name)
    if not ok: print(r.stdout, r.stderr)
    return ok


def main():
    ok = True
    with tempfile.TemporaryDirectory() as td:
        a,v = artifacts(Path(td), "PASS_QUALIFIED_READ_ONLY"); ok &= expect("v3 qualified-read-only pass", run(a,v), 0)
    with tempfile.TemporaryDirectory() as td:
        a,v = artifacts(Path(td), "PASS_WRITE_ALLOWED"); ok &= expect("v3 cannot grant write", run(a,v), 1)
    with tempfile.TemporaryDirectory() as td:
        a,v = artifacts(Path(td), "PASS_WRITE_ALLOWED", protocol=""); ok &= expect("legacy pass remains compatible", run(a,v), 0)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
