#!/usr/bin/env python3
from pathlib import Path
import argparse
import re
import subprocess
import sys


def run(script: str, *args: str) -> int:
    return subprocess.run([sys.executable, str(Path(__file__).with_name(script)), *args]).returncode


def protocol_version(path: str | None):
    if not path:
        return None
    text = Path(path).read_text(encoding="utf-8")
    m = re.search(r"(?mi)^\s*QUALIFICATION_PROTOCOL_VERSION\s*:\s*([^\n#]+)", text)
    return m.group(1).strip() if m else None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("relay")
    parser.add_argument("legacy_answer", nargs="?")
    parser.add_argument("legacy_verdict", nargs="?")
    parser.add_argument("--endpoint")
    parser.add_argument("--admission")
    parser.add_argument("--answer")
    parser.add_argument("--verdict")
    parser.add_argument("--reconciliation")
    args = parser.parse_args()

    answer = args.answer or args.legacy_answer
    verdict = args.verdict or args.legacy_verdict
    relay = Path(args.relay).resolve()

    if relay.is_file():
        rc = run("validate_agentchain.py", str(relay))
        structure = "legacy relay index"
    else:
        rc = run("validate_chain_store.py", str(relay))
        rc |= run("validate_roadmap_bindings.py", str(relay))
        rc |= run("validate_handover_snapshot.py", str(relay))
        rc |= run("validate_qualification_questions.py", str(relay))
        structure = "canonical relay + roadmap + handover + expert-question gates"

    v3 = protocol_version(answer) == "3" or protocol_version(verdict) == "3"

    if args.admission:
        if not args.endpoint:
            print("FAIL: --admission requires --endpoint", file=sys.stderr)
            rc |= 1
        else:
            admission_args = [args.endpoint, args.admission]
            if answer:
                admission_args.append(answer)
            rc |= run("validate_question_set_admission.py", *admission_args)
    elif v3 and (answer or verdict):
        print("FAIL: version-3 takeover qualification requires --endpoint and --admission first", file=sys.stderr)
        rc |= 1

    if answer:
        rc |= run("validate_candidate_answer.py", answer)
    if verdict:
        if not answer:
            print("FAIL: verdict requires candidate answer", file=sys.stderr)
            rc |= 1
        else:
            rc |= run("validate_qualification.py", answer, verdict)

    if args.reconciliation:
        if not verdict:
            print("FAIL: reconciliation requires completed qualification verdict", file=sys.stderr)
            rc |= 1
        else:
            rc |= run("validate_post_basis_drift.py", args.reconciliation)

    if rc == 0:
        print(f"PASS: {structure}")
        if v3 and verdict and not args.reconciliation:
            print("NOTE: qualified READ_ONLY; post-basis reconciliation is still required before WRITE_ALLOWED.")
        if args.reconciliation:
            print("NOTE: reconciliation validator checks drift/coverage logic; custody epoch and all other authority gates must still clear before mutation.")
    return 1 if rc else 0


if __name__ == "__main__":
    raise SystemExit(main())
