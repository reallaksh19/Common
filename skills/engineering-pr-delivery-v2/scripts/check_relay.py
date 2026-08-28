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
            "Usage: check_relay.py <repo-root|agents/chains|legacy-agentchain.md> "
            "[<candidate-answer.md> [<verifier-verdict.md>]]",
            file=sys.stderr,
        )
        return 2

    relay_arg = Path(sys.argv[1]).resolve()
    if relay_arg.is_file():
        rc = run("validate_agentchain.py", str(relay_arg))
        structure = "legacy relay index"
    else:
        rc = run("validate_chain_store.py", str(relay_arg))
        rc |= run("validate_roadmap_bindings.py", str(relay_arg))
        structure = "canonical chain-local relay store + roadmap bindings"

    if len(sys.argv) >= 3:
        rc |= run("validate_candidate_answer.py", sys.argv[2])

    if len(sys.argv) == 4:
        rc |= run("validate_qualification.py", sys.argv[2], sys.argv[3])

    if rc == 0:
        if len(sys.argv) == 2:
            print(f"PASS: {structure} structural gates")
        elif len(sys.argv) == 3:
            print(
                f"PASS: {structure} + deferred candidate answer; "
                "independent verdict still required"
            )
        else:
            print(f"PASS: {structure} + independent qualification gates")
    return 1 if rc else 0


if __name__ == "__main__":
    raise SystemExit(main())
