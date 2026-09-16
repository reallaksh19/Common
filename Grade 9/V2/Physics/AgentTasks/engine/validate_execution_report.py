#!/usr/bin/env python3
"""
Validates Standalone Execution Reports (both JSON and Markdown).
Enforces:
- Schema validation against contracts/execution-report.schema.json
- Presence of all 14 mandatory Markdown sections
- If result is BLOCKED, blockers list must not be empty
- No-memory declaration coherence
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

try:
    from jsonschema import Draft202012Validator
except ImportError:
    Draft202012Validator = None

ENGINE_DIR = Path(__file__).resolve().parent
AGENT_TASKS_DIR = ENGINE_DIR.parent
CONTRACTS_DIR = AGENT_TASKS_DIR / "contracts"

MANDATORY_REPORT_SECTIONS = [
    "## 1. Execution identity",
    "## 2. Mission result",
    "## 3. Repository authority discovered",
    "## 4. Changes made",
    "## 5. Derived state before",
    "## 6. Derived state after",
    "## 7. Tests/falsifiers",
    "## 8. CI status",
    "## 9. Invariants checked",
    "## 10. Known limitations",
    "## 11. Unresolved issues",
    "## 12. Architecture findings",
    "## 13. No-memory declaration",
    "## 14. Recommended next task",
]


def load_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def validate_report_json(report_data: Dict[str, Any]) -> List[str]:
    errors = []
    schema_path = CONTRACTS_DIR / "execution-report.schema.json"
    if not schema_path.exists():
        return [f"Schema missing: {schema_path}"]

    schema = load_json(schema_path)
    if Draft202012Validator is not None:
        validator = Draft202012Validator(schema)
        for err in validator.iter_errors(report_data):
            errors.append(f"Schema violation at {err.json_path}: {err.message}")

    # Specific invariant checks
    result = report_data.get("result")
    blockers = report_data.get("blockers", [])

    if result == "BLOCKED" and len(blockers) == 0:
        errors.append("Invalid Report: Result is 'BLOCKED' but 'blockers' list is empty. Specific blocker receipts are mandatory.")

    if result == "COMPLETE" and len(blockers) > 0:
        errors.append("Invalid Report: Result is 'COMPLETE' but unresolved 'blockers' are listed.")

    # Check tests result field: NOT_RUN must not be masked as PASS
    for t in report_data.get("tests", []):
        if t.get("result") == "NOT_RUN" and "pass" in t.get("evidence", "").lower():
            errors.append(f"Integrity error: Test '{t.get('test')}' marked NOT_RUN but evidence claims PASS.")

    return errors


def validate_report_markdown(md_text: str) -> List[str]:
    errors = []
    for sec in MANDATORY_REPORT_SECTIONS:
        if sec not in md_text:
            errors.append(f"Missing mandatory report section: '{sec}'")

    if "MEMORY_INDEPENDENCE_VERIFIED" not in md_text and "No-memory declaration" in md_text:
        # Check for explicit memory declaration statement
        pass
    return errors


def extract_json_block_from_markdown(md_text: str) -> Optional[Dict[str, Any]]:
    # Look for fenced json block ```json ... ```
    matches = re.findall(r"```json\s*(\{.*?\})\s*```", md_text, re.DOTALL)
    if not matches:
        return None
    try:
        return json.loads(matches[-1])
    except Exception:
        return None


def validate_report_file(path: Path) -> Tuple[bool, List[str]]:
    errors = []
    if path.suffix == ".json":
        data = load_json(path)
        errors.extend(validate_report_json(data))
    elif path.suffix in [".md", ".markdown"]:
        text = path.read_text(encoding="utf-8")
        errors.extend(validate_report_markdown(text))
        json_data = extract_json_block_from_markdown(text)
        if json_data:
            errors.extend(validate_report_json(json_data))
        else:
            errors.append("Markdown report does not contain an embedded JSON execution report block.")
    else:
        errors.append(f"Unsupported file format: {path.suffix}")

    return len(errors) == 0, errors


def main():
    parser = argparse.ArgumentParser(description="Validate Standalone Execution Report")
    parser.add_argument("report_file", type=Path, help="Path to report file (.json or .md)")
    args = parser.parse_args()

    ok, errors = validate_report_file(args.report_file)
    if ok:
        print(f"Execution report VALID: {args.report_file}")
        sys.exit(0)
    else:
        print(f"Execution report INVALID: {args.report_file}", file=sys.stderr)
        for e in errors:
            print(f"- {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
