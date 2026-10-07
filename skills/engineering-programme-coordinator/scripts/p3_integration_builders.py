#!/usr/bin/env python3
from __future__ import annotations

import copy
from typing import Any

from review_basis import active_common_protocol_digest, active_common_protocol_ref


def _l0_source(source: dict[str, Any]) -> dict[str, Any]:
    claims = []
    for item in source["contract_obligations"]:
        claims.append(
            {
                "id": item["id"],
                "severity": item["severity"],
                "claim": {
                    "type": item["claim_type"],
                    "statement": item["statement"],
                    "subject_refs": copy.deepcopy(item["subject_refs"]),
                },
                "expected_observation": item["expected_observation"],
                "plausible_green_but_wrong": item["plausible_green_but_wrong"],
                "oracle_refs": [item["oracle_ref"]],
                "evidence_required": [
                    {
                        "id": f"REQ-{item['id']}",
                        "method": item["method"],
                        "independence": "PRECOMMITTED",
                        "oracle_ref": item["oracle_ref"],
                    }
                ],
            }
        )
    return {
        "schema_version": "L0_TASK_CONTRACT_SOURCE_V1",
        "authority": "CHILD_CONTRACT_PROJECTION",
        "identity": copy.deepcopy(source["identity"]),
        "one_primary_outcome": (
            "Qualify the exact-candidate Phase-3 solo review/control chain end-to-end."
        ),
        "contract_claims": claims,
        "forbidden_outcomes": copy.deepcopy(source["forbidden_outcomes"]),
        "dependency_requirements": [
            {
                "producer": "PRD-527-P3-SOLO-1",
                "required_state": "VERIFIED_AND_MERGED",
                "exact_result_ref": "aeb855919d9866972248d811c75962dcb8fed861",
            },
            {
                "producer": "PRD-527-P3-SOLO-2",
                "required_state": "VERIFIED_AND_MERGED",
                "exact_result_ref": "39cca232b9a4cbdc3643f763af682c4aa3830828",
            },
            {
                "producer": "PRD-527-P3-SOLO-3",
                "required_state": "VERIFIED_AND_MERGED",
                "exact_result_ref": "8041f6ab4959a9aac4fbd1450e7e4523b18d8ce1",
            },
            {
                "producer": "PRD-527-P3-SOLO-4",
                "required_state": "VERIFIED_AND_MERGED",
                "exact_result_ref": "3157ddbfb6a47ba397480d4771ef3c906e03a4c9",
            },
            {
                "producer": "PRD-527-P3-SOLO-5",
                "required_state": "VERIFIED_AND_MERGED",
                "exact_result_ref": "a05db7c57fdacc2f5fcb0e55e300d6d76f70e4cd",
            },
            {
                "producer": "PRD-527-P3-SOLO-6",
                "required_state": "VERIFIED_AND_MERGED",
                "exact_result_ref": "6beb162cddd02100bc61079e53ad84d8563bb300",
            },
        ],
        "non_goals": copy.deepcopy(source["non_goals"]),
    }


def _l1_source(source: dict[str, Any]) -> dict[str, Any]:
    selectors = []
    for item in source["baseline_selectors"]:
        selectors.append(
            {
                "id": item["id"],
                "severity": item["severity"],
                "preservation_kind": item["preservation_kind"],
                "path": item["path"],
                "pointer": item["pointer"],
                "evidence_requirement": {
                    "id": f"REQ-{item['id']}",
                    "method": item["evidence_method"],
                },
            }
        )
    return {
        "schema_version": "L1_BASELINE_SOURCE_V1",
        "authority": "BASELINE_SELECTION_CONTRACT",
        "identity": copy.deepcopy(source["identity"]),
        "base": copy.deepcopy(source["base"]),
        "selectors": selectors,
        "forbidden_outcomes": [
            "candidate state substitutes for exact baseline truth",
            "missing selected baseline object is silently ignored",
            "aggregate PASS or lifecycle authority is emitted",
        ],
        "non_goals": copy.deepcopy(source["non_goals"]),
    }


def _l2_source(
    source: dict[str, Any],
    candidate_sha: str,
    pr_number: int,
    candidate_ref: str,
) -> dict[str, Any]:
    rules = []
    for item in source["impact_rules"]:
        rules.append(
            {
                "id": item["id"],
                "path_glob": item["path_glob"],
                "severity": item["severity"],
                "impact_statement": item["impact_statement"],
                "expected_observation": item["expected_observation"],
                "plausible_green_but_wrong": item["plausible_green_but_wrong"],
                "evidence_requirement": {
                    "id_prefix": f"REQ-{item['id'].replace('L2-RULE-', '')}",
                    "method": item["evidence_method"],
                },
            }
        )
    unknown = source["unknown_impact_policy"]
    return {
        "schema_version": "L2_IMPACT_SOURCE_V1",
        "authority": "CANDIDATE_DIFF_SELECTION_CONTRACT",
        "identity": copy.deepcopy(source["identity"]),
        "candidate": {
            "repository": "reallaksh19/Common",
            "pr_number": pr_number,
            "base_ref": source["base"]["ref"],
            "base_sha": source["base"]["sha"],
            "head_ref": candidate_ref,
            "head_sha": candidate_sha,
            "diff_mode": "NO_RENAMES_PATH_SET",
        },
        "rules": rules,
        "unknown_policy": {
            "severity": unknown["severity"],
            "expected_observation": unknown["expected_observation"],
            "plausible_green_but_wrong": unknown["plausible_green_but_wrong"],
            "evidence_requirement": {
                "id_prefix": "REQ-P3I-UNKNOWN",
                "method": unknown["evidence_method"],
            },
        },
        "forbidden_outcomes": [
            "changed candidate path is silently omitted",
            "unmatched changed path is treated as known",
            "multiple rule matches are silently resolved by order",
            "aggregate PASS or lifecycle authority is emitted",
        ],
        "non_goals": copy.deepcopy(source["non_goals"]),
    }


def _profile(
    candidate_sha: str,
    protocol: dict[str, Any],
    method_ids: list[str],
    *,
    result: str = "COMPLETE",
) -> dict[str, Any]:
    return {
        "review_profile": {
            "common_protocol": {
                "ref": active_common_protocol_ref(),
                "version": "1.0",
                "digest": active_common_protocol_digest(),
            },
            "project_protocol": {
                "ref": protocol["source_ref"],
                "digest": protocol["digest"],
            },
            "role": "SELF_REVIEW",
            "author_principal": "agent://p3-i-solo",
            "review_principal": "agent://p3-i-solo",
            "principal_independence": "NONE",
            "context_reset": "FRESH_REVIEW_ATTEMPT",
            "common_criteria": {
                f"CR-{index:02d}": {
                    "applicability": "REQUIRED",
                    "result": "PASS",
                    "evidence_refs": [f"qualification://P3-I/CR-{index:02d}"],
                }
                for index in range(1, 11)
            },
            "project_method_ids": list(method_ids),
            "specialist_required": [],
            "findings": [],
            "unresolved_required_findings": 0,
            "result": result,
            "final_candidate": candidate_sha,
        }
    }


def _self_check_basis(
    source: dict[str, Any],
    candidate_sha: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    manifest = source["self_check_manifest"]
    manifest_ref = f"repo://{manifest['path']}"
    repo_refs = [
        f"repo://{row['path']}"
        for row in source["runtime_basis"]
    ]
    basis = {
        "original_task_ref": source["identity"]["child_ref"],
        "base_sha": source["base"]["sha"],
        "candidate_sha": candidate_sha,
        "manifest_ref": manifest_ref,
        "manifest_path": manifest["path"],
        "manifest_digest": manifest["digest"],
        "repository_context_refs": repo_refs,
    }
    context = {
        "schema_version": "SELF_CHECK_CONTEXT_V1",
        "authority": "SOLO_SELF_CHECK_CONTEXT",
        "candidate_sha": candidate_sha,
        "manifest_ref": manifest_ref,
        "manifest_digest": manifest["digest"],
        "principal": {
            "kind": "SOLO_PRINCIPAL",
            "identity": "agent://p3-i-solo",
            "principal_independence": "NONE",
            "fresh_reconstruction": True,
            "blindness_claim": "NONE",
        },
        "reconstruction_policy": {
            "original_task_ref": source["identity"]["child_ref"],
            "base_sha": source["base"]["sha"],
            "candidate_sha": candidate_sha,
            "repository_context_refs": repo_refs,
            "expectation_manifest_frozen": True,
            "author_reasoning_used_as_evidence": False,
            "coder_confidence_used_as_evidence": False,
            "prior_self_check_used_as_evidence": False,
            "outcome_falsification_required": True,
        },
        "tool_access": ["repository", "tests"],
    }
    return context, basis


def _observations(
    candidate_sha: str,
    method_ids: list[str],
    *,
    fail_first: bool = False,
) -> list[dict[str, Any]]:
    rows = []
    for index, method_id in enumerate(sorted(method_ids)):
        result = "FAIL" if fail_first and index == 0 else "PASS"
        rows.append(
            {
                "method_id": method_id,
                "candidate_sha": candidate_sha,
                "result": result,
                "evidence_origin": "SAME_PRINCIPAL_EXECUTION",
                "evidence_refs": [f"qualification://P3-I/project/{method_id}"],
                "procedure": (
                    f"Replay pinned project method {method_id} against exact P3-I candidate."
                ),
                "limitation": None,
            }
        )
    return rows
