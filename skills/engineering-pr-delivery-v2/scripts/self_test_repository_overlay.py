#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
VALIDATOR = HERE / "validate_repository_overlay.py"

GOOD = """# Project overlay
COMMON_POLICY_SOURCE: reallaksh19/Common/skills/engineering-pr-delivery-v2/
COMMON_POLICY_REFERENCE: reallaksh19/Common/skills/engineering-pr-delivery-v2/references/repository-agent-policy.md
COMMON_PROTOCOL_MINIMUM_BASIS: 36068fde5b860ca1870311b166d28077b4c0bcf8
LOCAL_POLICY_SCOPE: PROJECT_ONLY
LEGACY_RELAY_WRITES: FORBIDDEN
## Project identity / criticality
engineering
"""

BAD_OLD = GOOD + "\n## 5. Five-question takeover gate\nagents/agentchain/<CHAIN_ID>/<ENDPOINT_ID>.md\n"


def run(text):
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        (root / "AGENTS.md").write_text(text, encoding="utf-8")
        return subprocess.run([sys.executable, str(VALIDATOR), str(root)], capture_output=True, text=True)


def expect(name, result, rc):
    ok = result.returncode == rc
    print(("PASS" if ok else "FAIL"), "SELF-TEST:", name)
    if not ok:
        print(result.stdout, result.stderr)
    return ok


def main():
    ok = True
    ok &= expect("thin project overlay", run(GOOD), 0)
    ok &= expect("old generic policy duplication rejected", run(BAD_OLD), 1)
    ok &= expect("missing adoption markers rejected", run("# Project\n"), 1)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
