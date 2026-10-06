#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from coordlib import load_yaml, validate as schema_validate
from proof_obligations import validate_pair


def canonical_manifest_digest(manifest: dict[str, Any]) -> str:
    payload = json.dumps(
        manifest,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def review_context_semantic_errors(context: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    reviewer = context["reviewer"]
    policy = context["context_policy"]

    if policy["candidate_sha"] != context["candidate_sha"]:
        errors.append(
            "context_policy.candidate_sha must equal review candidate_sha"
        )

    kind = reviewer["kind"]
    independence = reviewer["principal_independence"]
    if kind == "SAME_PRINCIPAL_FRESH_CONTEXT" and independence != "DEGRADED":
        errors.append(
            "same-principal fresh-context review must record DEGRADED independence"
        )
    if kind in {"DISTINCT_PRINCIPAL", "HUMAN_REVIEWER"} and independence != "DISTINCT":
        errors.append(
            f"{kind} must record DISTINCT principal independence"
        )

    return errors


def self_check_context_semantic_errors(context: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    principal = context["principal"]
    policy = context["reconstruction_policy"]

    if policy["candidate_sha"] != context["candidate_sha"]:
        errors.append(
            "reconstruction_policy.candidate_sha must equal self-check candidate_sha"
        )
    if principal["principal_independence"] != "NONE":
        errors.append(
            "solo self-check must record principal_independence NONE"
        )
    if principal["blindness_claim"] != "NONE":
        errors.append(
            "solo self-check cannot claim blinded or independent review"
        )
    if not principal["fresh_reconstruction"]:
        errors.append(
            "solo self-check requires a fresh reconstruction pass"
        )

    return errors


def validate_review_context(
    context: Any,
    label: str = "review-context",
) -> list[str]:
    errors = schema_validate("review-context", context, label)
    if errors:
        return errors
    return [
        f"{label}: {error}"
        for error in review_context_semantic_errors(context)
    ]


def validate_self_check_context(
    context: Any,
    label: str = "self-check-context",
) -> list[str]:
    errors = schema_validate("self-check-context", context, label)
    if errors:
        return errors
    return [
        f"{label}: {error}"
        for error in self_check_context_semantic_errors(context)
    ]


def validate_assessment_context(
    context: Any,
    label: str = "assessment-context",
) -> list[str]:
    if not isinstance(context, dict):
        return [f"{label}: assessment context must be an object"]

    version = context.get("schema_version")
    if version == "REVIEW_CONTEXT_V1":
        return validate_review_context(context, label)
    if version == "SELF_CHECK_CONTEXT_V1":
        return validate_self_check_context(context, label)

    return [
        f"{label}: unsupported assessment context schema_version: {version!r}"
    ]


def _policy(context: dict[str, Any]) -> dict[str, Any]:
    if context.get("schema_version") == "SELF_CHECK_CONTEXT_V1":
        return context.get("reconstruction_policy") or {}
    return context.get("context_policy") or {}


def _result_basis(
    manifest: Any,
    ledger: Any,
    assessment_context: Any,
) -> tuple[str, str]:
    candidate = None
    digest = None

    if isinstance(ledger, dict):
        candidate = ledger.get("candidate_sha")
        digest = ledger.get("manifest_digest")

    if not candidate and isinstance(assessment_context, dict):
        candidate = assessment_context.get("candidate_sha")
    if not digest and isinstance(assessment_context, dict):
        digest = assessment_context.get("manifest_digest")

    if not candidate and isinstance(manifest, dict):
        candidate = (manifest.get("basis") or {}).get("candidate_sha")

    if not isinstance(candidate, str) or len(candidate) != 40:
        candidate = "0" * 40
    if not isinstance(digest, str) or len(digest) != 64:
        digest = "0" * 64

    return candidate, digest


def _invalid_basis_reason(assessment_context: Any) -> str:
    if (
        isinstance(assessment_context, dict)
        and assessment_context.get("schema_version") == "SELF_CHECK_CONTEXT_V1"
    ):
        return "INVALID_SELF_CHECK_BASIS"
    return "INVALID_REVIEW_BASIS"


def gate_decision(
    manifest: Any,
    ledger: Any,
    assessment_context: Any,
) -> dict[str, Any]:
    errors = validate_pair(manifest, ledger)
    errors.extend(validate_assessment_context(assessment_context))

    if not errors:
        actual_digest = canonical_manifest_digest(manifest)
        if ledger["manifest_digest"] != actual_digest:
            errors.append(
                "evidence-ledger: manifest_digest does not match canonical manifest"
            )
        if assessment_context["manifest_digest"] != actual_digest:
            errors.append(
                "assessment-context: manifest_digest does not match canonical manifest"
            )
        if assessment_context["manifest_ref"] != ledger["manifest_ref"]:
            errors.append(
                "assessment-context.manifest_ref must equal evidence-ledger.manifest_ref"
            )
        if assessment_context["candidate_sha"] != ledger["candidate_sha"]:
            errors.append(
                "assessment-context candidate_sha must equal evidence-ledger candidate_sha"
            )
        if assessment_context["candidate_sha"] != manifest["basis"]["candidate_sha"]:
            errors.append(
                "assessment-context candidate_sha must equal manifest candidate_sha"
            )

        policy = _policy(assessment_context)
        if policy.get("base_sha") != manifest["basis"]["base_sha"]:
            errors.append(
                "assessment-context base_sha must equal manifest base_sha"
            )

    candidate, digest = _result_basis(manifest, ledger, assessment_context)

    if errors:
        return {
            "schema_version": "EVIDENCE_GATE_RESULT_V1",
            "authority": "DETERMINISTIC_EVIDENCE_GATE",
            "decision": "REPLAY_EVIDENCE",
            "candidate_sha": candidate,
            "manifest_digest": digest,
            "reason_codes": [_invalid_basis_reason(assessment_context)],
            "blocking_obligations": [],
            "validation_errors": errors,
        }

    refuted = sorted(
        record["obligation_id"]
        for record in ledger["records"]
        if record["state"] == "REFUTED"
    )
    if refuted:
        return {
            "schema_version": "EVIDENCE_GATE_RESULT_V1",
            "authority": "DETERMINISTIC_EVIDENCE_GATE",
            "decision": "REPAIR",
            "candidate_sha": ledger["candidate_sha"],
            "manifest_digest": ledger["manifest_digest"],
            "reason_codes": ["REFUTED_OBLIGATION"],
            "blocking_obligations": refuted,
            "validation_errors": [],
        }

    unknown = sorted(
        record["obligation_id"]
        for record in ledger["records"]
        if record["state"] == "UNKNOWN"
    )
    if unknown:
        return {
            "schema_version": "EVIDENCE_GATE_RESULT_V1",
            "authority": "DETERMINISTIC_EVIDENCE_GATE",
            "decision": "ESCALATE",
            "candidate_sha": ledger["candidate_sha"],
            "manifest_digest": ledger["manifest_digest"],
            "reason_codes": ["UNKNOWN_OBLIGATION"],
            "blocking_obligations": unknown,
            "validation_errors": [],
        }

    return {
        "schema_version": "EVIDENCE_GATE_RESULT_V1",
        "authority": "DETERMINISTIC_EVIDENCE_GATE",
        "decision": "ADVANCE_ELIGIBLE",
        "candidate_sha": ledger["candidate_sha"],
        "manifest_digest": ledger["manifest_digest"],
        "reason_codes": ["CLOSED_DENOMINATOR"],
        "blocking_obligations": [],
        "validation_errors": [],
    }


def validate_gate_result(
    result: Any,
    label: str = "evidence-gate-result",
) -> list[str]:
    return schema_validate("evidence-gate-result", result, label)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Evaluate exact-candidate proof evidence under either a truthful solo "
            "self-check context or an optional fresh review context."
        )
    )
    parser.add_argument("manifest")
    parser.add_argument("ledger")
    parser.add_argument("assessment_context")
    args = parser.parse_args()

    manifest = load_yaml(Path(args.manifest))
    ledger = load_yaml(Path(args.ledger))
    assessment_context = load_yaml(Path(args.assessment_context))

    result = gate_decision(manifest, ledger, assessment_context)
    errors = validate_gate_result(result)
    if errors:
        for error in errors:
            print(error)
        raise SystemExit(1)

    print(json.dumps(result, indent=2, sort_keys=True))
    if result["decision"] != "ADVANCE_ELIGIBLE":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
