#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys


def run(script: str, *args: str) -> int:
    cmd = [sys.executable, str(Path(__file__).with_name(script)), *args]
    return subprocess.run(cmd).returncode


def main():
    if len(sys.argv) not in {2, 3, 4}:
        print(
            "Usage: check_relay.py <agents/agentchain.md> [<candidate-answer.md> [<verifier-verdict.md>]]",
            file=sys.stderr,
        )
        return 2

    rc = run("validate_agentchain.py", sys.argv[1])

    if len(sys.argv) >= 3:
        rc |= run("validate_candidate_answer.py", sys.argv[2])

    if len(sys.argv) == 4:
        rc |= run("validate_qualification.py", sys.argv[2], sys.argv[3])

    if rc == 0:
        if len(sys.argv) == 2:
            print("PASS: relay package structural gates")
        elif len(sys.argv) == 3:
            print("PASS: relay structure + deferred candidate answer; independent verdict still required")
        else:
            print("PASS: relay package + independent qualification gates")
    return 1 if rc else 0


if __name__ == "__main__":
    raise SystemExit(main())
