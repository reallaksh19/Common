#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

ENGINE_VERSION = "1.0.0"


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _registry_index(registry: dict[str, Any]) -> dict[str, dict[str, Any]]:
    rows = registry.get("capabilities", [])
    index = {row["capability_id"]: row for row in rows}
    if len(index) != len(rows):
        raise ValueError("Capability registry contains duplicate capability_id values")
    return index


def _state_for(stats: dict[str, Any], policy: dict[str, Any]) -> tuple[str, str]:
    success = stats["independent_success"]
    failure = stats["independent_failure"]
    transfer = stats["transfer_success"]
    delayed = stats["delayed_success"]

    if failure >= policy["repair_independent_failure_min"]:
        confidence = "HIGH" if failure > policy["repair_independent_failure_min"] else "MEDIUM"
        return "REPAIR_REQUIRED", confidence

    if (
        success >= policy["robust_independent_success_min"]
        and failure == 0
        and ((transfer + delayed) > 0 or not policy["robust_requires_transfer_or_delayed"])
    ):
        return "ROBUST", "HIGH"

    if success >= policy["ready_independent_success_min"] and failure == 0:
        return "READY", "MEDIUM"

    if success > 0:
        return policy["single_success_state"], "LOW"

    if failure == 1:
        return policy["single_failure_state"], "LOW"

    return "UNKNOWN", "LOW"


def derive(
    fixture: dict[str, Any],
    registry: dict[str, Any],
    policy: dict[str, Any],
) -> dict[str, Any]:
    if policy.get("psychological_cause_inference_allowed") is not False:
        raise ValueError("Phase 5 reference policy must prohibit psychological-cause inference")

    reg = _registry_index(registry)
    stats: dict[str, dict[str, Any]] = defaultdict(
        lambda: {
            "independent_success": 0,
            "independent_failure": 0,
            "ambiguous_evidence": 0,
            "guided_success": 0,
            "transfer_success": 0,
            "delayed_success": 0,
            "subjects_seen": set(),
            "case_refs": [],
        }
    )

    case_results: list[dict[str, Any]] = []

    for case in fixture.get("cases", []):
        case_id = case["case_id"]
        subject = case["subject"]
        preserved = sorted(set(case.get("must_preserve", [])))
        failures = sorted(set(case.get("candidate_failure_capabilities", [])))
        ambiguous = any(obs.get("result") == "AMBIGUOUS" for obs in case.get("observations", []))

        for capability_id in preserved + failures:
            if capability_id not in reg:
                raise ValueError(f"Unknown capability reference: {capability_id}")
            definition = reg[capability_id]
            if definition.get("scope") == "SUBJECT" and definition.get("subject") != subject:
                raise ValueError(
                    f"Subject-scoped capability {capability_id} cannot be used by {subject}"
                )

        for capability_id in preserved:
            row = stats[capability_id]
            row["independent_success"] += 1
            row["subjects_seen"].add(subject)
            row["case_refs"].append(case_id)

        for capability_id in failures:
            row = stats[capability_id]
            row["subjects_seen"].add(subject)
            row["case_refs"].append(case_id)
            if ambiguous:
                row["ambiguous_evidence"] += 1
            else:
                row["independent_failure"] += 1

        if case.get("required_action"):
            action = case["required_action"]
        elif ambiguous:
            action = policy["ambiguity_action"]
        elif failures:
            action = "OPEN_DIAGNOSTIC_CASE"
        else:
            action = "NO_ACTION"

        if ambiguous and action != policy["ambiguity_action"]:
            raise ValueError(f"Ambiguous case {case_id} must require diagnostic probing")

        case_results.append(
            {
                "case_id": case_id,
                "subject": subject,
                "preserved_capabilities": preserved,
                "candidate_failure_capabilities": failures,
                "action": action,
                "forbidden_conclusions": sorted(set(case.get("must_not_conclude", []))),
            }
        )

    capability_states: list[dict[str, Any]] = []
    cross_subject_candidates: list[dict[str, Any]] = []

    for capability_id in sorted(stats):
        row = stats[capability_id]
        state, confidence = _state_for(row, policy)
        subjects = sorted(row["subjects_seen"])
        definition = reg[capability_id]

        capability_states.append(
            {
                "capability_ref": capability_id,
                "scope": definition["scope"],
                "subjects_seen": subjects,
                "state": state,
                "confidence": confidence,
                "evidence_summary": {
                    "independent_success": row["independent_success"],
                    "independent_failure": row["independent_failure"],
                    "ambiguous_evidence": row["ambiguous_evidence"],
                    "guided_success": row["guided_success"],
                    "transfer_success": row["transfer_success"],
                    "delayed_success": row["delayed_success"],
                },
                "case_refs": sorted(set(row["case_refs"])),
            }
        )

        if (
            definition["scope"] == "SHARED"
            and row["independent_failure"] >= policy["cross_subject_candidate_min_failures"]
            and len(subjects) >= policy["cross_subject_candidate_min_subjects"]
        ):
            cross_subject_candidates.append(
                {
                    "capability_ref": capability_id,
                    "subjects_seen": subjects,
                    "failure_count": row["independent_failure"],
                    "classification": "CROSS_SUBJECT_RECURRING_FAILURE_CANDIDATE",
                    "causal_status": "CANDIDATE_NOT_CAUSE",
                }
            )

    result: dict[str, Any] = {
        "engine_version": ENGINE_VERSION,
        "fixture_id": fixture["fixture_id"],
        "policy_id": policy["policy_id"],
        "policy_version": policy["version"],
        "registry_version": registry["registry_version"],
        "evidence_digest": digest(fixture),
        "policy_digest": digest(policy),
        "registry_digest": digest(registry),
        "case_results": sorted(case_results, key=lambda x: x["case_id"]),
        "capability_states": capability_states,
        "cross_subject_candidates": cross_subject_candidates,
        "global_falsifiers": sorted(set(fixture.get("global_falsifiers", []))),
        "psychological_cause_inference": "PROHIBITED",
    }
    result["output_digest"] = digest(result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", required=True, type=Path)
    parser.add_argument("--registry", required=True, type=Path)
    parser.add_argument("--policy", required=True, type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()

    result = derive(load_json(args.fixture), load_json(args.registry), load_json(args.policy))
    text = json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
