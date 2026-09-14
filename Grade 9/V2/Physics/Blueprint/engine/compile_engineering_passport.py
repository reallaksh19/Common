#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))
from compile_engineering_closure import canonical_digest, load  # noqa: E402


class EngineeringPassportError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


def fail(code: str, message: str):
    raise EngineeringPassportError(code, message)


def validate_schema(obj: dict, schema_rel: str, code: str):
    try:
        jsonschema.validate(obj, load(schema_rel))
    except jsonschema.ValidationError as exc:
        fail(code, exc.message)


def validate_receipt_semantics(receipt: dict):
    states = receipt["gate_states"]
    counts = receipt["counts"]
    actual_ready = sum(1 for state in states if state["status"] == "ENGINEERING_GATE_READY")
    actual_blocked = sum(1 for state in states if state["status"] != "ENGINEERING_GATE_READY")
    if counts["direct_gate_count"] != len(receipt["direct_gate_ids"]):
        fail("E_PASS_RECEIPT_INCONSISTENT", "direct_gate_count does not match direct_gate_ids")
    if counts["transitive_gate_count"] != len(receipt["transitive_gate_ids"]):
        fail("E_PASS_RECEIPT_INCONSISTENT", "transitive_gate_count does not match transitive_gate_ids")
    if counts["ready_gate_count"] != actual_ready or counts["blocked_gate_count"] != actual_blocked:
        fail("E_PASS_RECEIPT_INCONSISTENT", "gate-state counts do not match gate_states")
    should_block = bool(receipt["blockers"]) or actual_blocked > 0
    if (receipt["closure_status"] == "BLOCKED") != should_block:
        fail("E_PASS_RECEIPT_INCONSISTENT", "closure_status does not match blockers/gate states")


def compile_passport(request: dict, receipt: dict) -> dict:
    validate_schema(request, "contracts/engineering-request.schema.json", "E_PASS_REQUEST_SCHEMA")
    validate_schema(receipt, "contracts/engineering-closure-receipt.schema.json", "E_PASS_RECEIPT_SCHEMA")
    validate_receipt_semantics(receipt)
    if request["request_id"] != receipt["request_id"]:
        fail("E_PASS_REQUEST_RECEIPT_MISMATCH", "receipt request_id does not match request")

    ready = receipt["closure_status"] == "READY"
    if ready and receipt["source_item_status"] == "SOURCE_HELD":
        next_action = "Proceed to CCU for technical consumption while preserving the independent source/legal hold."
    elif ready:
        next_action = "Proceed to CCU; custody, pedagogy, publication and learner-evidence gates remain independently governed."
    else:
        next_action = receipt["blockers"][0]["message"] if receipt["blockers"] else "Resolve blocked technical gates and recompile closure."

    counts = receipt["counts"]
    passport = {
        "schema_version": "1.0.0",
        "passport_id": receipt["receipt_id"].replace("ENG-CLOSURE-", "ENG-PASS-", 1),
        "request_id": request["request_id"],
        "manifest_id": receipt["manifest_id"],
        "closure_receipt_id": receipt["receipt_id"],
        "closure_receipt_digest": canonical_digest(receipt),
        "requested_topic": request["requested_topic"],
        "requested_scope": request["requested_scope"],
        "engineering_depth": request["engineering_depth"],
        "technical_state": "ENGINEERING_READY" if ready else "BLOCKED_PENDING_ENGINEERING",
        "direct_gate_count": counts["direct_gate_count"],
        "transitive_gate_count": counts["transitive_gate_count"],
        "ready_gate_count": counts["ready_gate_count"],
        "blocked_gate_count": counts["blocked_gate_count"],
        "gate_states": receipt["gate_states"],
        "source_item_status": receipt["source_item_status"],
        "ccu_technical_authorization": "ALLOWED" if ready else "BLOCKED",
        "next_action": next_action,
    }
    validate_schema(passport, "contracts/engineering-passport.schema.json", "E_PASS_SCHEMA")
    return passport


def render_markdown(passport: dict) -> str:
    mark = {"ENGINEERING_GATE_READY": "✓", "ENGINEERING_GATE_INCOMPLETE": "△", "SOURCE_SCOPE_HELD": "✕", "MISSING": "✕"}
    lines = [
        "# Physics Engineering Passport",
        "",
        f"- **Request:** {passport['requested_topic']} — {passport['requested_scope']}",
        f"- **Engineering depth:** {passport['engineering_depth']}",
        f"- **Technical state:** {passport['technical_state']}",
        f"- **Closure:** {passport['ready_gate_count']}/{passport['transitive_gate_count']} gates READY",
        f"- **Source state:** {passport['source_item_status']}",
        f"- **CCU technical authorization:** {passport['ccu_technical_authorization']}",
        "",
        "## Gate closure",
        "",
    ]
    for state in passport["gate_states"]:
        direct = " (direct)" if state["direct"] else ""
        lines.append(f"- {mark[state['status']]} `{state['gate_id']}` — {state['status']}{direct}")
    lines.extend(["", "## Next action", "", passport["next_action"], ""])
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Compile a human-visible Physics Engineering Passport")
    parser.add_argument("request")
    parser.add_argument("closure_receipt")
    parser.add_argument("--out")
    parser.add_argument("--markdown-out")
    args = parser.parse_args()

    passport = compile_passport(load(args.request), load(args.closure_receipt))
    rendered = json.dumps(passport, indent=2) + "\n"
    if args.out:
        Path(args.out).write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    if args.markdown_out:
        Path(args.markdown_out).write_text(render_markdown(passport), encoding="utf-8")


if __name__ == "__main__":
    main()
