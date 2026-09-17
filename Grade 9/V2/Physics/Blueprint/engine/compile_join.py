#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PASS_STATES = {"CONFIRMED", "REFINED"}
UNRESOLVED_STATES = {"MISSING", "UNSUPPORTED", "CONTRADICTED", "OUT_OF_SCOPE", "UNKNOWN"}
COVERAGE_STATES = {"DEMANDS_PRESENT", "VERIFIED_NO_TARGET_DEMAND", "COVERAGE_UNKNOWN"}


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def _claim_refs(rows: list[dict[str, Any]], label: str) -> list[str]:
    refs = [str(row.get("claim_ref", "")).strip() for row in rows]
    if any(not ref for ref in refs):
        raise AssertionError(f"{label}_CLAIM_REF_REQUIRED")
    if len(refs) != len(set(refs)):
        raise AssertionError(f"{label}_CLAIM_REF_DUPLICATE")
    return refs


def _validated_zero_demand_coverage(coverage: dict[str, Any]) -> dict[str, Any]:
    state = coverage.get("state")
    if state not in COVERAGE_STATES:
        raise AssertionError("JOIN_ASSESSMENT_COVERAGE_STATE_INVALID")
    count = int(coverage.get("matched_target_item_count", -1))
    evidence_refs = [str(x).strip() for x in (coverage.get("evidence_refs") or []) if str(x).strip()]
    issues = [str(x).strip() for x in (coverage.get("unresolved_issues") or []) if str(x).strip()]
    if not evidence_refs:
        raise AssertionError("JOIN_ASSESSMENT_COVERAGE_EVIDENCE_REQUIRED")
    if not str(coverage.get("scope_digest", "")).startswith("sha256:"):
        raise AssertionError("JOIN_ASSESSMENT_SCOPE_DIGEST_REQUIRED")
    if not str(coverage.get("corpus_digest", "")).startswith("sha256:"):
        raise AssertionError("JOIN_ASSESSMENT_CORPUS_DIGEST_REQUIRED")
    if state == "DEMANDS_PRESENT":
        raise AssertionError("JOIN_DEMANDS_PRESENT_WITH_ZERO_DEMAND_CLAIMS")
    if state == "VERIFIED_NO_TARGET_DEMAND" and count != 0:
        raise AssertionError("JOIN_VERIFIED_ZERO_DEMAND_COUNT_MISMATCH")
    if state == "COVERAGE_UNKNOWN" and not issues:
        raise AssertionError("JOIN_COVERAGE_UNKNOWN_REQUIRES_ISSUE")
    return {
        "state": state,
        "matched_target_item_count": count,
        "scope_digest": coverage["scope_digest"],
        "corpus_digest": coverage["corpus_digest"],
        "evidence_refs": sorted(set(evidence_refs)),
        "unresolved_issues": sorted(set(issues)),
    }


def compile_join(spec: dict[str, Any], assessment_coverage: dict[str, Any] | None = None) -> dict[str, Any]:
    validation_refs = list(spec.get("validation_session_refs") or [])
    if not validation_refs:
        raise AssertionError("JOIN_VALIDATION_SESSION_REQUIRED")
    if len(validation_refs) != len(set(validation_refs)):
        raise AssertionError("JOIN_VALIDATION_SESSION_DUPLICATE")

    knowledge_refs = set(_claim_refs(list(spec.get("knowledge_claims") or []), "KNOWLEDGE"))
    demand_order = _claim_refs(list(spec.get("demand_claims") or []), "DEMAND")
    demand_refs = set(demand_order)

    # V10: zero demands are legal only when a scoped assessment-coverage receipt proves
    # either VERIFIED_NO_TARGET_DEMAND or COVERAGE_UNKNOWN. This distinguishes verified
    # absence from missing knowledge while keeping ordinary demand-bearing JOINs byte-stable.
    if not demand_refs:
        coverage = _validated_zero_demand_coverage(assessment_coverage or spec.get("assessment_coverage") or {})
        if list(spec.get("reconciliations") or []):
            raise AssertionError("JOIN_ZERO_DEMAND_RECONCILIATION_FORBIDDEN")
        if coverage["state"] == "VERIFIED_NO_TARGET_DEMAND":
            join_status, assimilation_ready = "JOIN_READY_NO_CORE2_DEMAND", True
            conflicts: list[dict[str, Any]] = []
        else:
            join_status, assimilation_ready = "JOIN_BLOCKED", False
            conflicts = [{
                "demand_claim_ref": "ASSESSMENT_COVERAGE",
                "status": "UNKNOWN",
                "reason": coverage["unresolved_issues"][0],
            }]
        packet = {
            "schema_version": "1.0.0",
            "join_id": spec["join_id"],
            "topic_id": spec["topic_id"],
            "core1_packet_ref": spec["core1_packet_ref"],
            "core2_packet_ref": spec["core2_packet_ref"],
            "validation_session_refs": sorted(validation_refs),
            "demand_claim_count": 0,
            "items": [],
            "critical_conflicts": conflicts,
            "join_status": join_status,
            "assimilation_ready": assimilation_ready,
            "assessment_coverage": coverage,
        }
        packet["join_digest"] = digest(packet)
        return packet

    if assessment_coverage is not None and assessment_coverage.get("state") != "DEMANDS_PRESENT":
        raise AssertionError("JOIN_ASSESSMENT_COVERAGE_DEMAND_MISMATCH")

    reconciliations = list(spec.get("reconciliations") or [])
    by_demand: dict[str, dict[str, Any]] = {}
    for row in reconciliations:
        demand_ref = str(row.get("demand_claim_ref", "")).strip()
        if demand_ref not in demand_refs:
            raise AssertionError("JOIN_UNKNOWN_DEMAND_REF:" + demand_ref)
        if demand_ref in by_demand:
            raise AssertionError("JOIN_DUPLICATE_DEMAND_RECONCILIATION:" + demand_ref)
        by_demand[demand_ref] = row

    missing = [ref for ref in demand_order if ref not in by_demand]
    if missing:
        raise AssertionError("JOIN_DEMAND_COVERAGE_GAP:" + ",".join(missing))

    items: list[dict[str, Any]] = []
    conflicts: list[dict[str, Any]] = []
    hold_count = 0
    block_count = 0

    for ordinal, demand_ref in enumerate(sorted(demand_order), start=1):
        row = by_demand[demand_ref]
        status = row.get("status")
        if status not in PASS_STATES | UNRESOLVED_STATES:
            raise AssertionError("JOIN_STATUS_INVALID:" + demand_ref)
        criticality = row.get("criticality")
        if criticality not in {"REQUIRED", "NON_BLOCKING"}:
            raise AssertionError("JOIN_CRITICALITY_INVALID:" + demand_ref)

        krefs = list(row.get("knowledge_claim_refs") or [])
        if len(krefs) != len(set(krefs)):
            raise AssertionError("JOIN_KNOWLEDGE_REF_DUPLICATE:" + demand_ref)
        unknown_k = sorted(set(krefs) - knowledge_refs)
        if unknown_k:
            raise AssertionError("JOIN_UNKNOWN_KNOWLEDGE_REF:" + ",".join(unknown_k))

        capability = str(row.get("required_capability", "")).strip()
        if not capability:
            raise AssertionError("JOIN_REQUIRED_CAPABILITY_MISSING:" + demand_ref)
        obligations = [str(x).strip() for x in (row.get("assimilation_obligations") or []) if str(x).strip()]
        issues = [str(x).strip() for x in (row.get("unresolved_issues") or []) if str(x).strip()]
        evidence = [str(x).strip() for x in (row.get("evidence_refs") or []) if str(x).strip()]
        if not evidence:
            raise AssertionError("JOIN_EVIDENCE_REQUIRED:" + demand_ref)

        if status in PASS_STATES:
            if not krefs:
                raise AssertionError("JOIN_SEMANTIC_GROUNDING_REQUIRED:" + demand_ref)
            if not obligations:
                raise AssertionError("JOIN_ASSIMILATION_OBLIGATION_REQUIRED:" + demand_ref)
            disposition = "READY_FOR_ASSIMILATION"
        else:
            if not issues:
                raise AssertionError("JOIN_UNRESOLVED_ISSUE_REQUIRED:" + demand_ref)
            if criticality == "REQUIRED":
                disposition = "BLOCK"
                block_count += 1
                conflicts.append({"demand_claim_ref": demand_ref, "status": status, "reason": issues[0]})
            else:
                disposition = "HOLD"
                hold_count += 1

        items.append({
            "join_item_id": f"JITEM-PHY-{ordinal:04d}",
            "demand_claim_ref": demand_ref,
            "knowledge_claim_refs": sorted(krefs),
            "status": status,
            "criticality": criticality,
            "required_capability": capability,
            "assimilation_obligations": obligations,
            "unresolved_issues": issues,
            "evidence_refs": sorted(evidence),
            "disposition": disposition,
        })

    if block_count:
        join_status, assimilation_ready = "JOIN_BLOCKED", False
    elif hold_count:
        join_status, assimilation_ready = "JOIN_READY_WITH_HOLDS", True
    else:
        join_status, assimilation_ready = "JOIN_READY", True

    packet = {
        "schema_version": "1.0.0",
        "join_id": spec["join_id"],
        "topic_id": spec["topic_id"],
        "core1_packet_ref": spec["core1_packet_ref"],
        "core2_packet_ref": spec["core2_packet_ref"],
        "validation_session_refs": sorted(validation_refs),
        "demand_claim_count": len(demand_order),
        "items": items,
        "critical_conflicts": sorted(conflicts, key=lambda x: x["demand_claim_ref"]),
        "join_status": join_status,
        "assimilation_ready": assimilation_ready,
    }
    packet["join_digest"] = digest(packet)
    return packet


def main() -> None:
    import argparse
    from jsonschema import Draft202012Validator

    ap = argparse.ArgumentParser(description="Compile the Physics Core1 x Core2 Join gate.")
    ap.add_argument("spec", type=Path)
    ap.add_argument("--assessment-coverage", type=Path)
    ap.add_argument("--out", type=Path)
    args = ap.parse_args()

    spec = json.loads(args.spec.read_text(encoding="utf-8"))
    coverage = json.loads(args.assessment_coverage.read_text(encoding="utf-8")) if args.assessment_coverage else None
    packet = compile_join(spec, assessment_coverage=coverage)
    schema = json.loads((ROOT / "contracts" / "join-packet.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator(schema).validate(packet)
    text = json.dumps(packet, indent=2, ensure_ascii=False) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
