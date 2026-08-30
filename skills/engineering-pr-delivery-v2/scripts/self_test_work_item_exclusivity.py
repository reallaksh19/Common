#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
VALIDATOR = HERE / "validate_work_item_exclusivity.py"
UUID1 = "6c19e9d4-4be3-4f4c-9b4a-7a1f52d1e930"
UUID2 = "3487ad68-7933-4b62-a35b-c9a803948477"


def active(root, name, key=None, mode=None, instance=None, partition=None, authority=None, state="ACTIVE"):
    d = root / "agents" / "chains" / name
    d.mkdir(parents=True, exist_ok=True)
    lines = ["CHAIN_STATE_VERSION: 3", f"CHAIN_ID: {name}", f"STATE: {state}"]
    for k, v in [
        ("WORK_ITEM_KEY", key), ("WORK_ITEM_MODE", mode), ("AGENT_INSTANCE_ID", instance),
        ("WORK_ITEM_PARTITION", partition), ("WORK_ITEM_PARTITION_AUTHORITY", authority),
    ]:
        if v is not None:
            lines.append(f"{k}: {v}")
    (d / "ACTIVE.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(root):
    return subprocess.run([sys.executable, str(VALIDATOR), str(root)], capture_output=True, text=True)


def expect(name, result, rc):
    ok = result.returncode == rc
    print(("PASS" if ok else "FAIL"), "SELF-TEST:", name)
    if not ok:
        print(result.stdout, result.stderr)
    return ok


def main():
    ok = True
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        active(r, "A", "github:o/r#1535", "EXCLUSIVE", f"chatgpt:{UUID1}")
        active(r, "B", "github:o/r#1536", "EXCLUSIVE", f"chatgpt:{UUID2}")
        ok &= expect("different exclusive work items", run(r), 0)
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        active(r, "A", "github:o/r#1535", "EXCLUSIVE", f"chatgpt:{UUID1}")
        active(r, "B", "github:o/r#1535", "EXCLUSIVE", f"chatgpt:{UUID2}")
        ok &= expect("same issue dual writer rejected", run(r), 1)
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        active(r, "A", "github:o/r#1535", "EXCLUSIVE", "OPENAI-GPT-5.6-SOL")
        ok &= expect("model name is not agent instance", run(r), 1)
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        active(r, "A", "github:o/r#1535", "PARTITIONED", f"chatgpt:{UUID1}", "backend", "OWNER:issue-comment-1")
        active(r, "B", "github:o/r#1535", "PARTITIONED", f"chatgpt:{UUID2}", "ui", "OWNER:issue-comment-1")
        ok &= expect("owner-approved distinct partitions", run(r), 0)
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        active(r, "A", "github:o/r#1535", "PARTITIONED", f"chatgpt:{UUID1}", "backend", "OWNER:issue-comment-1")
        active(r, "B", "github:o/r#1535", "PARTITIONED", f"chatgpt:{UUID2}", "backend", "OWNER:issue-comment-1")
        ok &= expect("duplicate partition rejected", run(r), 1)
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        active(r, "OLD")
        ok &= expect("historical active without adoption fields grandfathered", run(r), 0)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
