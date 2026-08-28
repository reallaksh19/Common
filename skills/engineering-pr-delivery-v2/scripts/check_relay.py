#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys


def run(script: str, *args: str) -> int:
    return subprocess.run([sys.executable, str(Path(__file__).with_name(script)), *args]).returncode


def main():
    if len(sys.argv) not in {2, 3, 4}:
        print("Usage: check_relay.py <repo-root|agents/chains|legacy-agentchain.md> [<candidate-answer.md> [<verifier-verdict.md>]]", file=sys.stderr)
        return 2
    relay = Path(sys.argv[1]).resolve()
    if relay.is_file():
        rc = run("validate_agentchain.py", str(relay))
        structure = "legacy relay index"
    else:
        rc = run("validate_chain_store.py", str(relay))
        rc |= run("validate_roadmap_bindings.py", str(relay))
        rc |= run("validate_handover_snapshot.py", str(relay))
        rc |= run("validate_qualification_questions.py", str(relay))
        structure = "canonical relay + roadmap + handover + expert-question gates"
    if len(sys.argv) >= 3:
        rc |= run("validate_candidate_answer.py", sys.argv[2])
    if len(sys.argv) == 4:
        rc |= run("validate_qualification.py", sys.argv[2], sys.argv[3])
    if rc == 0:
        print(f"PASS: {structure}")
        if len(sys.argv) == 4:
            print("NOTE: qualification PASS proves competence only; current-state reconciliation is still required before WRITE_ALLOWED.")
    return 1 if rc else 0


if __name__ == "__main__":
    raise SystemExit(main())
