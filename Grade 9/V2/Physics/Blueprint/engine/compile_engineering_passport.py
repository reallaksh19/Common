#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))
from compile_engineering_closure import V3_REGISTRY_REF, canonical_digest, load  # noqa: E402
from build_physics_engineering_gate_registry_v3 import build_registry as build_registry_v3  # noqa: E402
from validate_engineering_gates_v3 import PhysicsEngineeringGateV3Error, validate as validate_registry_v3  # noqa: E402


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


def _base_passport(request: dict, receipt: dict) -> dict:
    ready = receipt["closure_status"] == "READY"
    if ready:
        next_action = "Submit the exact engineering closure and manifest to the global Engineering Gate before any downstream consumer proceeds."
    else:
        next_action = receipt["blockers"][0]["message"] if receipt["blockers"] else "Resolve blocked technical gates and recompile closure."
    counts = receipt["counts"]
    return {
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
        "consumer_authorization": "NOT_EVALUATED",
        "next_action": next_action,
    }


def _compile_v3_passport(base: dict, receipt: dict) -> dict:
    registry = build_registry_v3()
    try:
        validate_registry_v3(registry)
    except PhysicsEngineeringGateV3Error as exc:
        fail("E_PASS_REGISTRY_INVALID", f"{exc.code}: {exc.message}")
    current_digest = canonical_digest(registry)
    if current_digest != receipt["registry_digest"]:
        fail("E_PASS_REGISTRY_DIGEST_DRIFT", f"receipt={receipt['registry_digest']} current={current_digest}")

    gate_map = {g["subtopic_id"]: g for g in registry["gates"]}
    closure = [gate_map[gid] for gid in receipt["transitive_gate_ids"] if gid in gate_map]
    if len(closure) != len(receipt["transitive_gate_ids"]):
        fail("E_PASS_REGISTRY_CLOSURE_DRIFT", "receipt references gates missing from current v3 registry")

    keys = {
        "concepts": "concepts",
        "relations": "relations",
        "model_conditions": "model_conditions",
        "representations": "representations",
        "reasoning_steps": "reasoning_sequence",
        "transformations": "required_transformations",
        "misconceptions": "misconceptions",
        "verifications": "verifications",
        "problem_families": "problem_families",
    }
    coverage = {}
    for out_key, gate_key in keys.items():
        count = sum(len(g[gate_key]) for g in closure)
        coverage[out_key] = {"status": "PASS" if count > 0 else "BLOCKED", "count": count}

    hotspots = []
    for gate in closure:
        for step in gate["reasoning_sequence"]:
            if step["inferential_jump"] == "HIGH_FRAGILITY":
                hotspots.append({
                    "gate_id": gate["subtopic_id"], "hotspot_type": "INFERENTIAL_JUMP",
                    "ref": step["step_id"], "level": 3, "description": step["expert_action"],
                })
    direct_profiles = []
    for gid in receipt["direct_gate_ids"]:
        gate = gate_map[gid]
        profile = gate["difficulty_engineering"]
        direct_profiles.append({
            "gate_id": gid,
            "provisional_badge": profile["provisional_badge"],
            "maturity": profile["maturity"],
            "dimensions": profile["dimensions"],
        })
        for dim, value in profile["dimensions"].items():
            if value == 3:
                hotspots.append({
                    "gate_id": gid, "hotspot_type": "DIFFICULTY_DIMENSION", "ref": dim,
                    "level": 3, "description": f"Direct-gate engineering dimension {dim} is at maximum provisional engineering intensity.",
                })

    passport = {
        "schema_version": "2.0.0",
        **base,
        "registry_ref": receipt["registry_ref"],
        "registry_digest": receipt["registry_digest"],
        "technical_coverage": coverage,
        "fragility_hotspots": hotspots,
        "direct_gate_profiles": direct_profiles,
        "publication_authorization": "NOT_IMPLIED",
    }
    validate_schema(passport, "contracts/engineering-passport-v2.schema.json", "E_PASS_SCHEMA")
    return passport


def compile_passport(request: dict, receipt: dict) -> dict:
    validate_schema(request, "contracts/engineering-request.schema.json", "E_PASS_REQUEST_SCHEMA")
    validate_schema(receipt, "contracts/engineering-closure-receipt.schema.json", "E_PASS_RECEIPT_SCHEMA")
    validate_receipt_semantics(receipt)
    if request["request_id"] != receipt["request_id"]:
        fail("E_PASS_REQUEST_RECEIPT_MISMATCH", "receipt request_id does not match request")

    base = _base_passport(request, receipt)
    if receipt["registry_ref"] == V3_REGISTRY_REF:
        return _compile_v3_passport(base, receipt)

    passport = {"schema_version": "1.0.0", **base}
    validate_schema(passport, "contracts/engineering-passport.schema.json", "E_PASS_SCHEMA")
    return passport


def render_markdown(passport: dict) -> str:
    mark = {"ENGINEERING_GATE_READY": "✓", "ENGINEERING_GATE_INCOMPLETE": "△", "SOURCE_SCOPE_HELD": "✕", "MISSING": "✕"}
    lines = [
        "# Physics Engineering Passport — diagnostic only",
        "",
        f"- **Request:** {passport['requested_topic']} — {passport['requested_scope']}",
        f"- **Engineering depth:** {passport['engineering_depth']}",
        f"- **Technical state:** {passport['technical_state']}",
        f"- **Closure:** {passport['ready_gate_count']}/{passport['transitive_gate_count']} gates READY",
        f"- **Source state:** {passport['source_item_status']}",
        f"- **Consumer authorization:** {passport['consumer_authorization']} — owned by global Engineering Gate",
    ]
    if passport.get("schema_version") == "2.0.0":
        lines.extend([
            f"- **Publication authorization:** {passport['publication_authorization']}",
            f"- **Registry digest:** `{passport['registry_digest']}`",
            "",
            "## Technical coverage",
            "",
        ])
        for name, row in passport["technical_coverage"].items():
            lines.append(f"- **{name}:** {row['status']} ({row['count']})")
        lines.extend(["", "## Direct-gate engineering profile", ""])
        for row in passport["direct_gate_profiles"]:
            lines.append(f"- `{row['gate_id']}` — {row['provisional_badge']} ({row['maturity']} maturity)")
        lines.extend(["", "## Fragility hotspots", ""])
        if passport["fragility_hotspots"]:
            for row in passport["fragility_hotspots"]:
                lines.append(f"- `{row['gate_id']}` · {row['hotspot_type']} · `{row['ref']}` — {row['description']}")
        else:
            lines.append("- None at level 3.")

    lines.extend(["", "## Gate closure", ""])
    for state in passport["gate_states"]:
        direct = " (direct)" if state["direct"] else ""
        lines.append(f"- {mark[state['status']]} `{state['gate_id']}` — {state['status']}{direct}")
    lines.extend(["", "## Next action", "", passport["next_action"], ""])
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Compile a diagnostic subject Engineering Passport; consumer authority is evaluated globally")
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
