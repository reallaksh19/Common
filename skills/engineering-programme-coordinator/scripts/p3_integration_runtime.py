#!/usr/bin/env python3
from __future__ import annotations

import copy
from pathlib import Path
from typing import Any

from coordlib import dump_yaml
from evidence_gate import (
    AUTHORITY_BOUNDARIES as GATE_AUTHORITY_BOUNDARIES,
    compile_gate,
)
from exact_candidate_evidence import compile_source as compile_evidence_ledger
from execution_kernel import derive_next_action, validate_execution_state
from l0_task_obligations import compile_l0
from l1_baseline_obligations import compile_source as compile_l1
from l2_diff_impact import compile_source as compile_l2
from principal_independence import compile_truth
from project_outcome_falsification import compile_result as compile_project_falsification
from review_basis import active_common_protocol_digest, review_basis_errors
from self_review_expectation_freeze import compile_freeze
from verdict_policy import derive_projection

from p3_integration_builders import (
    _l0_source,
    _l1_source,
    _l2_source,
    _observations,
    _profile,
    _self_check_basis,
)
from p3_integration_contract import (
    ACTION_UNIVERSE,
    _load_project_protocol,
    canonical_digest,
)


def _write_yaml(repo_root: Path, relative: Path, value: Any) -> None:
    path = repo_root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dump_yaml(value), encoding="utf-8")


def _manifest_requirements(manifest: dict[str, Any]):
    for obligation in manifest["obligations"]:
        value = obligation["evidence_required"]
        requirements = value if isinstance(value, list) else [value]
        for requirement in requirements:
            yield obligation, requirement


def _evidence_source(
    source: dict[str, Any],
    manifests: dict[str, dict[str, Any]],
    manifest_paths: dict[str, str],
    candidate_sha: str,
    pr_number: int,
    candidate_ref: str,
) -> dict[str, Any]:
    evidence_items = []
    seen = set()
    for layer in ("l0", "l1", "l2"):
        for _obligation, requirement in _manifest_requirements(manifests[layer]):
            rid = requirement["id"]
            if rid in seen:
                raise ValueError(f"duplicate current requirement id: {rid}")
            seen.add(rid)
            evidence_items.append(
                {
                    "evidence_id": f"EVID-{rid}",
                    "requirement_id": rid,
                    "method": requirement["method"],
                    "candidate_sha": candidate_sha,
                    "refs": [f"qualification://P3-I/{rid}"],
                    "verifier_kind": "DETERMINISTIC_TOOL",
                    "verifier_identity": "engineering-programme-coordinator-integrated",
                }
            )
    return {
        "schema_version": "EXACT_CANDIDATE_EVIDENCE_SOURCE_V1",
        "authority": "CLOSED_DENOMINATOR_EVIDENCE_INPUT",
        "identity": copy.deepcopy(source["identity"]),
        "candidate": {
            "repository": "reallaksh19/Common",
            "pr_number": pr_number,
            "ref": candidate_ref,
            "sha": candidate_sha,
        },
        "manifests": {
            layer: {
                "path": manifest_paths[layer],
                "digest": manifests[layer]["manifest_digest"],
            }
            for layer in ("l0", "l1", "l2")
        },
        "evidence_items": evidence_items,
        "forbidden_outcomes": [
            "any current L0 L1 L2 obligation is omitted",
            "evidence for another candidate SHA is accepted",
            "missing evidence disappears from denominator accounting",
            "ledger emits verdict or gate authority",
        ],
        "non_goals": copy.deepcopy(source["non_goals"]),
    }


def _zero_counts() -> dict[str, int]:
    return {
        "VERIFIED": 0,
        "REFUTED": 0,
        "UNKNOWN": 0,
        "NOT_APPLICABLE": 0,
        "WAIVER": 0,
    }


def _expected_from_projection(projection: dict[str, Any]) -> dict[str, Any]:
    critical = projection["criticality"]
    return {
        "obligation_count": projection["accounting"]["obligation_count"],
        "state_counts": copy.deepcopy(projection["accounting"]["state_counts"]),
        "critical": {
            "obligation_count": critical["obligation_count"],
            **copy.deepcopy(critical["state_counts"]),
        },
        "unresolved_critical_refuted": len(critical["unresolved_refuted_ids"]),
        "unresolved_critical_unknown": len(critical["unresolved_unknown_ids"]),
        "waived_critical": len(critical["waiver_ids"]),
        "not_applicable_critical": len(critical["not_applicable_ids"]),
    }


def _verdict_source(
    source: dict[str, Any],
    evidence_source: dict[str, Any],
    ledger: dict[str, Any],
    evidence_source_path: str,
    ledger_path: str,
    *,
    mode: str,
    repo_root: Path,
) -> tuple[dict[str, Any], dict[str, Any]]:
    candidate = copy.deepcopy(evidence_source["candidate"])
    evaluations = []
    critical_requirement = None
    for record in ledger["records"]:
        if record["severity"] == "CRITICAL" and record["requirements"]:
            critical_requirement = record["requirements"][0]["requirement_id"]
            break
    if critical_requirement is None:
        raise ValueError("P3-I current denominator lacks a CRITICAL requirement")

    for record in ledger["records"]:
        for requirement in record["requirements"]:
            rid = requirement["requirement_id"]
            for item in requirement["evidence_items"]:
                if mode == "unknown" and rid == critical_requirement:
                    continue
                outcome = (
                    "CONTRADICTS"
                    if mode == "refuted" and rid == critical_requirement
                    else "SATISFIES"
                )
                evaluations.append(
                    {
                        "evidence_id": item["evidence_id"],
                        "requirement_id": rid,
                        "candidate_sha": candidate["sha"],
                        "outcome": outcome,
                        "basis_ref": item["refs"][0],
                    }
                )

    verdict_source = {
        "schema_version": "VERDICT_POLICY_SOURCE_V1",
        "authority": "EVIDENCE_VERDICT_POLICY_INPUT",
        "identity": copy.deepcopy(source["identity"]),
        "ledger_basis": {
            "evidence_source": {
                "path": evidence_source_path,
                "digest": canonical_digest(evidence_source),
            },
            "evidence_ledger": {
                "path": ledger_path,
                "digest": ledger["ledger_digest"],
            },
            "candidate": candidate,
        },
        "evidence_evaluations": evaluations,
        "dispositions": [],
        "criticality_policy": {
            "critical_severity": "CRITICAL",
            "unresolved_states": ["REFUTED", "UNKNOWN"],
            "not_applicable_counts_as_verified": False,
            "waiver_counts_as_verified": False,
            "waiver_requires_owner_authority": True,
        },
        "expected_projection": {
            "obligation_count": 0,
            "state_counts": _zero_counts(),
            "critical": {"obligation_count": 0, **_zero_counts()},
            "unresolved_critical_refuted": 0,
            "unresolved_critical_unknown": 0,
            "waived_critical": 0,
            "not_applicable_critical": 0,
        },
        "forbidden_outcomes": [
            "UNKNOWN counts as VERIFIED",
            "NOT_APPLICABLE or WAIVER masquerades as VERIFIED",
            "verdict emits aggregate PASS or gate disposition",
        ],
        "non_goals": copy.deepcopy(source["non_goals"]),
    }
    provisional = derive_projection(
        verdict_source,
        repo_root,
        enforce_expected=False,
    )
    verdict_source["expected_projection"] = _expected_from_projection(provisional)
    projection = derive_projection(verdict_source, repo_root)
    return verdict_source, projection


def _gate_binding(ref: str, digest: str, candidate_sha: str) -> dict[str, str]:
    return {"ref": ref, "digest": digest, "candidate_sha": candidate_sha}


def _gate_source(
    candidate_sha: str,
    candidate_ref: str,
    verdict_projection: dict[str, Any],
    context: dict[str, Any],
    governing_basis: dict[str, Any],
    profile: dict[str, Any],
    freeze: dict[str, Any],
    falsification: dict[str, Any],
    truth: dict[str, Any],
    local_resolution: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "schema_version": "DETERMINISTIC_EVIDENCE_GATE_SOURCE_V1",
        "authority": "DETERMINISTIC_EVIDENCE_GATE_INPUT",
        "identity": {
            "programme_or_parent_id": "COMMON-PROD-CONTROL-V1",
            "parent_ref": "https://github.com/reallaksh19/Common/issues/527",
            "task_id": "PRD-527-P3-SOLO-6",
            "child_ref": "SELF:PRD-527-P3-SOLO-6",
            "contract_version": "P3-SOLO-6-v1",
        },
        "candidate": {
            "repository": "reallaksh19/Common",
            "ref": candidate_ref,
            "sha": candidate_sha,
        },
        "inputs": {
            "verdict_projection": _gate_binding(
                "runtime://p3-i/verdict",
                verdict_projection["projection_digest"],
                candidate_sha,
            ),
            "self_check_context": _gate_binding(
                "runtime://p3-i/self-check",
                canonical_digest(
                    {
                        "context": context,
                        "governing_basis": governing_basis,
                    }
                ),
                candidate_sha,
            ),
            "common_review_floor": _gate_binding(
                "runtime://p3-i/common-review-floor",
                canonical_digest(profile),
                candidate_sha,
            ),
            "expectation_challenge": _gate_binding(
                "runtime://p3-i/expectation-challenge",
                freeze["freeze_digest"],
                candidate_sha,
            ),
            "project_falsification": _gate_binding(
                "runtime://p3-i/project-falsification",
                falsification["result_digest"],
                candidate_sha,
            ),
            "principal_truth": _gate_binding(
                "runtime://p3-i/principal-truth",
                truth["truth_digest"],
                candidate_sha,
            ),
        },
        "local_resolution": copy.deepcopy(local_resolution),
        "decision_policy": {
            "stale_or_invalid": "REPLAY",
            "proven_repairable_defect": "REPAIR",
            "unknown_local_work_remaining": "REPLAY",
            "unknown_local_resolution_exhausted": "ESCALATE",
            "closed_current_denominator": "ADVANCE_ELIGIBLE",
        },
        "authority_boundaries": copy.deepcopy(GATE_AUTHORITY_BOUNDARIES),
    }


def _execution_state(
    source: dict[str, Any],
    candidate_sha: str,
    candidate_ref: str,
    pr_number: int,
    verdict_projection: dict[str, Any],
    gate_result: dict[str, Any],
    *,
    deny_advance: bool = False,
) -> dict[str, Any]:
    disposition = gate_result["disposition"]
    allowed_by_disposition = {
        "REPLAY": {"RUN_VERIFICATION"},
        "REPAIR": {"REPAIR_CANDIDATE"},
        "ESCALATE": {"ESCALATE"},
        "ADVANCE_ELIGIBLE": {"REQUEST_STAGE_ADVANCE"},
    }
    allowed = set(allowed_by_disposition[disposition])
    if deny_advance:
        allowed.discard("REQUEST_STAGE_ADVANCE")
    forbidden = ACTION_UNIVERSE - allowed

    unresolved = []
    for oid in verdict_projection["criticality"]["unresolved_refuted_ids"]:
        unresolved.append(
            {
                "id": oid,
                "state": "REFUTED",
                "evidence_refs": [f"runtime://p3-i/verdict/{oid}"],
            }
        )
    for oid in verdict_projection["criticality"]["unresolved_unknown_ids"]:
        unresolved.append(
            {
                "id": oid,
                "state": "UNKNOWN",
                "evidence_refs": [],
            }
        )

    result = {
        "schema_version": "EXECUTION_STATE_V1",
        "authority": "EXECUTION_STATE_PROJECTION",
        "identity": {
            "parent": "PARENT-527",
            "responsibility": "PRD-527-P3-I",
            "attempt": 1,
        },
        "repository": {
            "target_ref": source["base"]["ref"],
            "target_sha": source["base"]["sha"],
            "branch": candidate_ref,
            "pr": pr_number,
            "candidate_sha": candidate_sha,
        },
        "protocol": {
            "local_ref": (
                f"reallaksh19/Common@{candidate_sha}:skills/Local_PR_Deliverty_v1.1"
            ),
            "local_digest": canonical_digest({"local": candidate_sha}),
            "v35_ref": (
                f"reallaksh19/Common@{candidate_sha}:skills/engineering-pr-delivery-v3.5"
            ),
            "v35_digest": canonical_digest({"v35": candidate_sha}),
            "common_reviewer_ref": (
                f"reallaksh19/Common@{candidate_sha}:skills/common-reviewer-protocol-v1.0"
            ),
            "common_reviewer_digest": active_common_protocol_digest(),
        },
        "capability": {
            "resolution_state": "VERIFIED",
            "resolver_ref": (
                f"reallaksh19/Common@{candidate_sha}:"
                "skills/engineering-programme-coordinator/scripts/authority_resolver.py"
            ),
            "resolver_digest": canonical_digest({"resolver": candidate_sha}),
            "active_role": "CODER",
            "capability_basis": ["authority://p3-i-hosted-qualification"],
            "allowed_actions": sorted(allowed),
            "forbidden_actions": sorted(forbidden),
        },
        "lifecycle": {
            "stage": "CODING",
            "last_completed_checkpoint": "P3-I-QUALIFICATION",
        },
        "dependencies": {
            "satisfied": [
                f"P3-SOLO-{index}" for index in range(1, 7)
            ],
            "blocked": [],
        },
        "verification": {
            "expectation_manifest_ref": "repo://p3-i-self-check-manifest",
            "evidence_ledger_ref": "runtime://p3-i/current-ledger",
            "evidence_state": "CURRENT",
            "evidence_candidate_sha": candidate_sha,
            "unresolved_critical": unresolved,
            "gate": {
                "disposition": disposition,
                "candidate_sha": candidate_sha,
                "result_ref": "runtime://p3-i/gate-result",
                "result_digest": gate_result["result_digest"],
            },
        },
        "contradictions": [],
        "next_action": {
            "type": "RECONCILE",
            "reason_code": "PLACEHOLDER",
            "basis_refs": ["runtime://p3-i"],
        },
    }
    result["next_action"] = derive_next_action(result)
    errors = validate_execution_state(result)
    if errors:
        raise ValueError("; ".join(errors))
    return result


def _current_artifacts(
    source: dict[str, Any],
    candidate_sha: str,
    pr_number: int,
    candidate_ref: str,
    repo_root: Path,
    scratch_relative: Path,
    *,
    verdict_mode: str = "clean",
    project_fail: bool = False,
) -> dict[str, Any]:
    protocol = _load_project_protocol(source, repo_root)
    method_ids = source["local_project_protocol"]["method_ids"]

    l0 = compile_l0(_l0_source(source))
    l1 = compile_l1(_l1_source(source), repo_root)
    l2 = compile_l2(
        _l2_source(source, candidate_sha, pr_number, candidate_ref),
        repo_root,
    )

    manifest_paths = {
        "l0": str(scratch_relative / "l0.yaml"),
        "l1": str(scratch_relative / "l1.yaml"),
        "l2": str(scratch_relative / "l2.yaml"),
    }
    for layer, value in (("l0", l0), ("l1", l1), ("l2", l2)):
        _write_yaml(repo_root, Path(manifest_paths[layer]), value)

    evidence_source = _evidence_source(
        source,
        {"l0": l0, "l1": l1, "l2": l2},
        manifest_paths,
        candidate_sha,
        pr_number,
        candidate_ref,
    )
    evidence_source_path = str(scratch_relative / "evidence-source.yaml")
    _write_yaml(repo_root, Path(evidence_source_path), evidence_source)
    ledger = compile_evidence_ledger(evidence_source, repo_root)
    ledger_path = str(scratch_relative / "evidence-ledger.yaml")
    _write_yaml(repo_root, Path(ledger_path), ledger)

    verdict_source, verdict_projection = _verdict_source(
        source,
        evidence_source,
        ledger,
        evidence_source_path,
        ledger_path,
        mode=verdict_mode,
        repo_root=repo_root,
    )
    _write_yaml(repo_root, scratch_relative / "verdict-source.yaml", verdict_source)

    profile = _profile(candidate_sha, protocol, method_ids)
    context, governing_basis = _self_check_basis(source, candidate_sha)
    basis_errors = review_basis_errors(
        profile,
        context,
        governing_basis,
        repo_root,
    )
    if basis_errors:
        raise ValueError("; ".join(basis_errors))

    freeze = compile_freeze(
        "PRD-527-P3-I",
        l0,
        l1,
        l2,
        profile,
    )
    observations = _observations(
        candidate_sha,
        method_ids,
        fail_first=project_fail,
    )
    falsification = compile_project_falsification(
        "PRD-527-P3-I",
        freeze,
        l0,
        l1,
        l2,
        profile,
        protocol,
        observations,
    )
    truth = compile_truth(profile, context)

    return {
        "protocol": protocol,
        "method_ids": method_ids,
        "l0": l0,
        "l1": l1,
        "l2": l2,
        "evidence_source": evidence_source,
        "ledger": ledger,
        "verdict_source": verdict_source,
        "verdict_projection": verdict_projection,
        "profile": profile,
        "context": context,
        "governing_basis": governing_basis,
        "freeze": freeze,
        "observations": observations,
        "falsification": falsification,
        "truth": truth,
    }


def _compile_gate_for(
    source: dict[str, Any],
    artifacts: dict[str, Any],
    candidate_sha: str,
    candidate_ref: str,
    repo_root: Path,
    *,
    local_resolution: list[dict[str, Any]] | None = None,
    context: dict[str, Any] | None = None,
    governing_basis: dict[str, Any] | None = None,
    profile: dict[str, Any] | None = None,
    freeze: dict[str, Any] | None = None,
    falsification: dict[str, Any] | None = None,
    truth: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    ctx = context if context is not None else artifacts["context"]
    basis = governing_basis if governing_basis is not None else artifacts["governing_basis"]
    prof = profile if profile is not None else artifacts["profile"]
    frz = freeze if freeze is not None else artifacts["freeze"]
    fals = falsification if falsification is not None else artifacts["falsification"]
    principal = truth if truth is not None else artifacts["truth"]
    gate_source = _gate_source(
        candidate_sha,
        candidate_ref,
        artifacts["verdict_projection"],
        ctx,
        basis,
        prof,
        frz,
        fals,
        principal,
        local_resolution or [],
    )
    result = compile_gate(
        gate_source,
        artifacts["verdict_projection"],
        artifacts["verdict_source"],
        ctx,
        basis,
        prof,
        frz,
        artifacts["l0"],
        artifacts["l1"],
        artifacts["l2"],
        artifacts["protocol"],
        artifacts["observations"],
        fals,
        principal,
        repo_root,
    )
    return gate_source, result
