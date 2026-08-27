#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent

VALID_SOURCE = """# EP
CHAIN_ID: C1
ENDPOINT_ID: EP-1
PREVIOUS_ENDPOINT: NONE
STATE: QUALIFICATION_REQUIRED
QUALIFICATION_BASIS_HEAD: abc
QUESTION_SET_STATUS: CURRENT
### Inputs
- `input.json`
### Benchmarks
- `bench.json`
### Common / governing documents
- `AGENTS.md`
### Authoritative sources
- live repository
### Production paths
- `src/a.py`
### Validation / test paths
- `tests/a.py`
### Expected next-leg files / domains
- `src/a.py`
"""


def run(script, *args):
    return subprocess.run([sys.executable, str(HERE / script), *map(str, args)], capture_output=True, text=True)


def expect(name, result, code):
    ok = result.returncode == code
    print(("PASS" if ok else "FAIL"), name, "rc=", result.returncode)
    if not ok:
        print(result.stdout, result.stderr)
    return ok


def main():
    checks = []
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        agents = root / "agents"; agents.mkdir()
        chain_dir = agents / "agentchain"; chain_dir.mkdir()

        ep1 = root / "ep1.md"; ep1.write_text(VALID_SOURCE, encoding="utf-8")
        bad_source = root / "bad-source.md"; bad_source.write_text(VALID_SOURCE.replace("### Benchmarks\n- `bench.json`\n", ""), encoding="utf-8")
        checks.append(expect("source-valid", run("validate_source_index.py", ep1), 0))
        checks.append(expect("source-missing-benchmark", run("validate_source_index.py", bad_source), 1))

        checks.append(expect("freshness-current", run("validate_endpoint_freshness.py", ep1, "abc"), 0))
        checks.append(expect("freshness-stale", run("validate_endpoint_freshness.py", ep1, "def"), 1))
        checks.append(expect("freshness-metadata-only", run("validate_endpoint_freshness.py", ep1, "def", "--metadata-only"), 0))

        prev = root / "prev.md"; prev.write_text("CHAIN_ID: C1\nENDPOINT_ID: EP-1\nSTATE: QUALIFICATION_REQUIRED\n", encoding="utf-8")
        cur = root / "cur.md"; cur.write_text("CHAIN_ID: C1\nENDPOINT_ID: EP-2\nPREVIOUS_ENDPOINT: EP-1\nSTATE: READY_FOR_NEXT_LEG\n", encoding="utf-8")
        checks.append(expect("transition-valid", run("validate_relay_transition.py", prev, cur), 0))
        done = root / "done.md"; done.write_text("CHAIN_ID: C1\nENDPOINT_ID: EP-3\nSTATE: COMPLETE\n", encoding="utf-8")
        revive = root / "revive.md"; revive.write_text("CHAIN_ID: C1\nENDPOINT_ID: EP-4\nPREVIOUS_ENDPOINT: EP-3\nSTATE: ACTIVE\n", encoding="utf-8")
        checks.append(expect("transition-complete-to-active", run("validate_relay_transition.py", done, revive), 1))

        c1 = chain_dir / "C1"; c1.mkdir(); c2 = chain_dir / "C2"; c2.mkdir()
        (c1 / "EP-1.md").write_text(VALID_SOURCE.replace("CHAIN_ID: C1", "CHAIN_ID: C1"), encoding="utf-8")
        (c2 / "EP-1.md").write_text(VALID_SOURCE.replace("CHAIN_ID: C1", "CHAIN_ID: C2").replace("src/a.py", "src/b.py").replace("tests/a.py", "tests/b.py"), encoding="utf-8")
        index = agents / "agentchain.md"
        index.write_text("""# Engineering Agent Chain
## ACTIVE CHAINS
| Chain | Mission | Latest endpoint | Endpoint file | PR | State | Authority domain | Next action |
|---|---|---|---|---|---|---|---|
| C1 | one | EP-1 | agents/agentchain/C1/EP-1.md | #1 | ACTIVE | Domain A | x |
| C2 | two | EP-1 | agents/agentchain/C2/EP-1.md | #2 | ACTIVE | Domain B | y |
## ENDPOINT LOG
""", encoding="utf-8")
        checks.append(expect("overlap-safe", run("detect_chain_overlap.py", index), 0))
        index.write_text(index.read_text().replace("Domain B", "Domain A"), encoding="utf-8")
        checks.append(expect("overlap-authority", run("detect_chain_overlap.py", index), 1))

    if all(checks):
        print(f"PASS: all {len(checks)} policy-control cases")
        return 0
    print("FAIL: policy-control suite")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
