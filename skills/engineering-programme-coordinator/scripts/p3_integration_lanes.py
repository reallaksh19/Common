#!/usr/bin/env python3
from __future__ import annotations

import copy
import tempfile
from pathlib import Path
from typing import Any

from coordlib import load_yaml, validate as schema_validate
from evidence_gate import validate_result as validate_gate_result
from phase2_self_review_qualification import compile_source as compile_phase2_qualification
from principal_independence import compile_truth
from review_basis import review_basis_errors
from self_review_expectation_freeze import object_digest as freeze_object_digest

from p3_integration_contract import (
    AUTHORITY_BOUNDARIES,
    CHECK_IDS,
    _safe_path,
    _validate_runtime_basis,
    canonical_digest,
    object_digest,
    validate_source,
)
from p3_integration_runtime import (
    _compile_gate_for,
    _current_artifacts,
    _execution_state,
)


def _legacy_degraded_truth(
    clean: dict[str, Any],
    candidate_sha: str,
) -> dict[str, Any]:
    profile = copy.deepcopy(clean["profile"])
    review = profile["review_profile"]
    review["role"] = "REVIEWER"
    review["author_principal"] = "agent://p3-i-same"
    review["review_principal"] = "agent://p3-i-same"
    review["principal_independence"] = "DEGRADED"
    context = {
        "schema_version": "REVIEW_CONTEXT_V1",
        "authority": "FRESH_REVIEW_CONTEXT",
        "candidate_sha": candidate_sha,
        "manifest_ref": clean["context"]["manifest_ref"],
        "manifest_digest": clean["context"]["manifest_digest"],
        "reviewer": {
            "kind": "SAME_PRINCIPAL_FRESH_CONTEXT",
            "identity": "agent://p3-i-same",
            "principal_independence": "DEGRADED",
            "fresh_context": True,
        },
        "context_policy": {
            "original_task_ref": "https://github.com/reallaksh19/Common/issues/588",
            "base_sha": clean["governing_basis"]["base_sha"],
            "candidate_sha": candidate_sha,
            "repository_context_refs": ["repo://p3-i"],
            "candidate_visible_in_phase_a": False,
            "generated_tests_visible_in_phase_a": False,
            "coder_reasoning_included": False,
            "coder_confidence_included": False,
            "prior_self_review_included": False,
            "implementation_rationale_included": False,
            "candidate_visible_in_phase_b": True,
        },
        "tool_access": ["repository", "tests"],
    }
    return compile_truth(profile, context)


def _lane(
    source: dict[str, Any],
    check_id: str,
    passed: bool,
    observed: str,
    *refs: str,
) -> dict[str, Any]:
    expected = next(
        row["expected"]
        for row in source["expected_checks"]
        if row["id"] == check_id
    )
    return {
        "id": check_id,
        "passed": passed,
        "expected": expected,
        "observed": observed,
        "evidence_refs": list(refs) or [f"runtime://P3-I/{check_id}"],
    }


def compile_qualification(
    source: dict[str, Any],
    candidate_sha: str,
    pr_number: int,
    candidate_ref: str,
    repo_root: Path,
) -> dict[str, Any]:
    errors = validate_source(source)
    if errors:
        raise ValueError("; ".join(errors))
    if not isinstance(pr_number, int) or pr_number < 1:
        raise ValueError("P3-I qualification requires positive PR number")

    _validate_runtime_basis(source, candidate_sha, repo_root)

    with tempfile.TemporaryDirectory(
        dir=repo_root,
        prefix=".p3i-runtime-",
    ) as tmp:
        scratch_relative = Path(tmp).resolve().relative_to(repo_root.resolve())

        clean = _current_artifacts(
            source,
            candidate_sha,
            pr_number,
            candidate_ref,
            repo_root,
            scratch_relative / "clean",
        )
        clean_gate_source, clean_gate = _compile_gate_for(
            source,
            clean,
            candidate_sha,
            candidate_ref,
            repo_root,
        )
        clean_kernel = _execution_state(
            source,
            candidate_sha,
            candidate_ref,
            pr_number,
            clean["verdict_projection"],
            clean_gate,
        )

        candidate_values = {
            clean["context"]["candidate_sha"],
            clean["profile"]["review_profile"]["final_candidate"],
            clean["freeze"]["identity"]["candidate_sha"],
            clean["falsification"]["identity"]["candidate_sha"],
            clean["truth"]["candidate_sha"],
            clean["verdict_projection"]["candidate"]["sha"],
            clean_gate["candidate_sha"],
            clean_kernel["repository"]["candidate_sha"],
        }

        stale_context = copy.deepcopy(clean["context"])
        stale_basis = copy.deepcopy(clean["governing_basis"])
        stale_context["manifest_digest"] = "f" * 64
        stale_basis["manifest_digest"] = "f" * 64
        stale_context["reconstruction_policy"]["repository_context_refs"] = copy.deepcopy(
            stale_basis["repository_context_refs"]
        )
        _stale_source, stale_gate = _compile_gate_for(
            source,
            clean,
            candidate_sha,
            candidate_ref,
            repo_root,
            context=stale_context,
            governing_basis=stale_basis,
        )

        weak_profile = copy.deepcopy(clean["profile"])
        weak_profile["review_profile"]["common_criteria"]["CR-01"] = {
            "applicability": "NOT_APPLICABLE",
            "applicability_basis": "caller://weaken-common-floor",
            "result": "NOT_APPLICABLE",
        }
        weak_errors = review_basis_errors(
            weak_profile,
            clean["context"],
            clean["governing_basis"],
            repo_root,
        )

        stale_freeze = copy.deepcopy(clean["freeze"])
        stale_freeze["expectations"][0]["expected_observation"] += " tampered"
        stale_freeze["freeze_digest"] = freeze_object_digest(
            stale_freeze,
            "freeze_digest",
        )
        _stale_freeze_source, stale_freeze_gate = _compile_gate_for(
            source,
            clean,
            candidate_sha,
            candidate_ref,
            repo_root,
            freeze=stale_freeze,
        )

        project_bad = _current_artifacts(
            source,
            candidate_sha,
            pr_number,
            candidate_ref,
            repo_root,
            scratch_relative / "project-bad",
            project_fail=True,
        )
        _project_bad_source, project_bad_gate = _compile_gate_for(
            source,
            project_bad,
            candidate_sha,
            candidate_ref,
            repo_root,
        )

        legacy_truth = _legacy_degraded_truth(clean, candidate_sha)

        refuted = _current_artifacts(
            source,
            candidate_sha,
            pr_number,
            candidate_ref,
            repo_root,
            scratch_relative / "refuted",
            verdict_mode="refuted",
        )
        _refuted_source, refuted_gate = _compile_gate_for(
            source,
            refuted,
            candidate_sha,
            candidate_ref,
            repo_root,
        )
        refuted_kernel = _execution_state(
            source,
            candidate_sha,
            candidate_ref,
            pr_number,
            refuted["verdict_projection"],
            refuted_gate,
        )

        unknown = _current_artifacts(
            source,
            candidate_sha,
            pr_number,
            candidate_ref,
            repo_root,
            scratch_relative / "unknown",
            verdict_mode="unknown",
        )
        _unknown_source, unknown_gate = _compile_gate_for(
            source,
            unknown,
            candidate_sha,
            candidate_ref,
            repo_root,
        )
        unknown_kernel = _execution_state(
            source,
            candidate_sha,
            candidate_ref,
            pr_number,
            unknown["verdict_projection"],
            unknown_gate,
        )
        unknown_refs = [
            f"obligation://{oid}"
            for oid in unknown["verdict_projection"]["criticality"]["unresolved_unknown_ids"]
        ]
        if not unknown_refs:
            raise ValueError("P3-I unknown lane produced no unresolved critical obligation")

        exhausted_records = [
            {
                "subject_ref": ref,
                "candidate_sha": candidate_sha,
                "state": "LOCAL_RESOLUTION_EXHAUSTED",
                "evidence_refs": [f"provider://p3-i/exhaustion/{index + 1}"],
                "boundary_ref": "owner://p3-i/decision-required",
            }
            for index, ref in enumerate(unknown_refs)
        ]
        _escalate_source, escalate_gate = _compile_gate_for(
            source,
            unknown,
            candidate_sha,
            candidate_ref,
            repo_root,
            local_resolution=exhausted_records,
        )
        escalate_kernel = _execution_state(
            source,
            candidate_sha,
            candidate_ref,
            pr_number,
            unknown["verdict_projection"],
            escalate_gate,
        )

        duplicate_records = copy.deepcopy(exhausted_records)
        duplicate_records.insert(
            0,
            {
                "subject_ref": unknown_refs[0],
                "candidate_sha": candidate_sha,
                "state": "LOCAL_WORK_REMAINING",
                "evidence_refs": [],
                "boundary_ref": None,
            },
        )
        _dup_source, duplicate_gate = _compile_gate_for(
            source,
            unknown,
            candidate_sha,
            candidate_ref,
            repo_root,
            local_resolution=duplicate_records,
        )

        fake_records = copy.deepcopy(exhausted_records)
        fake_records[0]["boundary_ref"] = "caller-says-exhausted"
        _fake_source, fake_gate = _compile_gate_for(
            source,
            unknown,
            candidate_sha,
            candidate_ref,
            repo_root,
            local_resolution=fake_records,
        )

        denied_kernel = _execution_state(
            source,
            candidate_sha,
            candidate_ref,
            pr_number,
            clean["verdict_projection"],
            clean_gate,
            deny_advance=True,
        )

        unbound_gate_errors = validate_gate_result(clean_gate)

        forbidden_true = []
        for label, artifact in (
            ("freeze", clean["freeze"]),
            ("falsification", clean["falsification"]),
            ("truth", clean["truth"]),
            ("gate", clean_gate),
        ):
            boundaries = artifact.get("authority_boundaries", {})
            for key in (
                "emits_engineering_pass",
                "emits_project_acceptance_pass",
                "emits_independent_review_verdict",
                "performs_lifecycle_advance",
                "grants_merge_authority",
                "grants_production_cutover",
            ):
                if boundaries.get(key) is True:
                    forbidden_true.append(f"{label}.{key}")

        p2i_source_path = _safe_path(
            repo_root,
            source["retained_p2i"]["source_path"],
        )
        p2i_source = load_yaml(p2i_source_path)
        p2i_result = compile_phase2_qualification(p2i_source, repo_root)

        lanes = [
            _lane(
                source,
                "P3I-01",
                candidate_values == {candidate_sha},
                f"candidate identities={sorted(candidate_values)}",
                "runtime://p3-i/candidate-identity",
            ),
            _lane(
                source,
                "P3I-02",
                stale_gate["disposition"] == "REPLAY",
                f"gate={stale_gate['disposition']}",
                "runtime://p3-i/stale-self-check",
            ),
            _lane(
                source,
                "P3I-03",
                bool(weak_errors),
                "REJECTED" if weak_errors else "ACCEPTED",
                "runtime://p3-i/common-floor",
            ),
            _lane(
                source,
                "P3I-04",
                stale_freeze_gate["disposition"] == "REPLAY",
                f"gate={stale_freeze_gate['disposition']}",
                "runtime://p3-i/stale-freeze",
            ),
            _lane(
                source,
                "P3I-05",
                (
                    project_bad["falsification"]["falsification_status"] == "FALSIFIED"
                    and project_bad_gate["disposition"] == "REPAIR"
                ),
                (
                    "project="
                    f"{project_bad['falsification']['falsification_status']};"
                    f"gate={project_bad_gate['disposition']}"
                ),
                "runtime://p3-i/project-falsification",
            ),
            _lane(
                source,
                "P3I-06",
                (
                    clean["falsification"]["falsification_status"] == "NOT_FALSIFIED"
                    and clean["falsification"]["falsification_status"] != "PASS"
                ),
                f"project={clean['falsification']['falsification_status']}",
                "runtime://p3-i/project-non-pass",
            ),
            _lane(
                source,
                "P3I-07",
                (
                    clean["truth"]["principals"]["relationship"] == "SAME_PRINCIPAL"
                    and clean["truth"]["principals"]["principal_independence"] == "NONE"
                ),
                (
                    f"relationship={clean['truth']['principals']['relationship']};"
                    "independence="
                    f"{clean['truth']['principals']['principal_independence']}"
                ),
                "runtime://p3-i/principal-truth",
            ),
            _lane(
                source,
                "P3I-08",
                (
                    legacy_truth["compatibility"]["legacy_degraded_input_consumed"] is True
                    and legacy_truth["principals"]["principal_independence"] == "NONE"
                ),
                (
                    "legacy_consumed="
                    f"{legacy_truth['compatibility']['legacy_degraded_input_consumed']};"
                    "canonical="
                    f"{legacy_truth['principals']['principal_independence']}"
                ),
                "runtime://p3-i/legacy-degraded",
            ),
            _lane(
                source,
                "P3I-09",
                (
                    refuted_gate["disposition"] == "REPAIR"
                    and refuted_kernel["next_action"]["type"] == "REPAIR_CANDIDATE"
                ),
                (
                    f"gate={refuted_gate['disposition']};"
                    f"kernel={refuted_kernel['next_action']['type']}"
                ),
                "runtime://p3-i/refuted",
            ),
            _lane(
                source,
                "P3I-10",
                (
                    unknown_gate["disposition"] == "REPLAY"
                    and unknown_kernel["next_action"]["type"] == "VERIFY_CANDIDATE"
                ),
                (
                    f"gate={unknown_gate['disposition']};"
                    f"kernel={unknown_kernel['next_action']['type']}"
                ),
                "runtime://p3-i/unknown-local-work",
            ),
            _lane(
                source,
                "P3I-11",
                (
                    escalate_gate["disposition"] == "ESCALATE"
                    and escalate_kernel["next_action"]["type"] == "ESCALATE"
                ),
                (
                    f"gate={escalate_gate['disposition']};"
                    f"kernel={escalate_kernel['next_action']['type']}"
                ),
                "runtime://p3-i/proven-exhaustion",
            ),
            _lane(
                source,
                "P3I-12",
                duplicate_gate["disposition"] == "REPLAY",
                f"gate={duplicate_gate['disposition']}",
                "runtime://p3-i/duplicate-exhaustion",
            ),
            _lane(
                source,
                "P3I-13",
                fake_gate["disposition"] == "REPLAY",
                f"gate={fake_gate['disposition']}",
                "runtime://p3-i/fake-boundary",
            ),
            _lane(
                source,
                "P3I-14",
                clean_gate["disposition"] == "ADVANCE_ELIGIBLE",
                f"gate={clean_gate['disposition']}",
                "runtime://p3-i/clean-gate",
            ),
            _lane(
                source,
                "P3I-15",
                clean_kernel["next_action"]["type"] == "REQUEST_STAGE_ADVANCE",
                f"kernel={clean_kernel['next_action']['type']}",
                "runtime://p3-i/clean-kernel",
            ),
            _lane(
                source,
                "P3I-16",
                (
                    denied_kernel["next_action"]["type"] == "RECONCILE"
                    and denied_kernel["next_action"]["reason_code"] == "CAPABILITY_MISSING"
                ),
                (
                    f"kernel={denied_kernel['next_action']['type']};"
                    f"reason={denied_kernel['next_action']['reason_code']}"
                ),
                "runtime://p3-i/capability-denial",
            ),
            _lane(
                source,
                "P3I-17",
                any(
                    "source-bound fresh gate replay is required" in row
                    for row in unbound_gate_errors
                ),
                "REJECTED_UNBOUND" if unbound_gate_errors else "ACCEPTED_UNBOUND",
                "runtime://p3-i/gate-self-certification",
            ),
            _lane(
                source,
                "P3I-18",
                not forbidden_true,
                "no forbidden authority true" if not forbidden_true else ",".join(forbidden_true),
                "runtime://p3-i/authority-boundaries",
            ),
            _lane(
                source,
                "P3I-19",
                p2i_result["qualification_status"] == "QUALIFIED",
                f"P2-I={p2i_result['qualification_status']}",
                source["retained_p2i"]["source_path"],
            ),
            _lane(
                source,
                "P3I-20",
                (
                    clean_gate["disposition"] == "ADVANCE_ELIGIBLE"
                    and clean_kernel["next_action"]["type"] == "REQUEST_STAGE_ADVANCE"
                ),
                (
                    f"false_block={not (clean_gate['disposition'] == 'ADVANCE_ELIGIBLE' and clean_kernel['next_action']['type'] == 'REQUEST_STAGE_ADVANCE')}"
                ),
                "runtime://p3-i/clean-control",
            ),
        ]

        passed = sum(row["passed"] for row in lanes)
        result = {
            "schema_version": "P3_INTEGRATION_QUALIFICATION_RESULT_V1",
            "authority": "PHASE3_SOLO_INTEGRATION_QUALIFICATION_EVIDENCE",
            "identity": {
                "task_id": "PRD-527-P3-I",
                "base_sha": source["base"]["sha"],
                "candidate_sha": candidate_sha,
                "pr_number": pr_number,
            },
            "source_digest": canonical_digest(source),
            "runtime_basis_digest": canonical_digest(source["runtime_basis"]),
            "lanes": lanes,
            "accounting": {
                "checks": len(lanes),
                "passed": passed,
                "failed": len(lanes) - passed,
                "clean_false_blocks": (
                    0
                    if (
                        clean_gate["disposition"] == "ADVANCE_ELIGIBLE"
                        and clean_kernel["next_action"]["type"] == "REQUEST_STAGE_ADVANCE"
                    )
                    else 1
                ),
            },
            "clean_control": {
                "project_falsification_status": clean["falsification"]["falsification_status"],
                "gate_disposition": clean_gate["disposition"],
                "kernel_action": clean_kernel["next_action"]["type"],
                "lifecycle_transition_performed": False,
            },
            "retained_p2i_status": p2i_result["qualification_status"],
            "principal_independence": clean["truth"]["principals"]["principal_independence"],
            "qualification_status": "QUALIFIED" if passed == len(lanes) else "FAILED",
            "authority_boundaries": copy.deepcopy(AUTHORITY_BOUNDARIES),
        }
        result["result_digest"] = object_digest(result, "result_digest")
        shape_errors = schema_validate(
            "p3-integration-qualification-result",
            result,
            "compiled-p3-integration-qualification",
        )
        if shape_errors:
            raise ValueError("; ".join(shape_errors))
        return result
