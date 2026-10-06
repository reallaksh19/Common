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


def _result_basis(
    manifest: Any,
    ledger: Any,
    review_context: Any,
) -> tuple[str, str]:
    candidate = None
    digest = None

    if isinstance(ledger, dict):
        candidate = ledger.get("candidate_sha")
        digest = ledger.get("manifest_digest")

    if not candidate and isinstance(review_context, dict):
        candidate = review_context.get("candidate_sha")
    if not digest and isinstance(review_context, dict):
        digest = review_context.get("manifest_digest")

    if not candidate and isinstance(manifest, dict):
        candidate = (manifest.get("basis") or {}).get("candidate_sha")

    if not isinstance(candidate, str) or len(candidate) != 40:
        candidate = "0" * 40
    if not isinstance(digest, str) or len(digest) != 64:
        digest = "0" * 64

    return candidate, digest


def gate_decision(
    manifest: Any,
    ledger: Any,
    review_context: Any,
) -> dict[str, Any]:
    errors = validate_pair(manifest, ledger)
    errors.extend(validate_review_context(review_context))

    if not errors:
        actual_digest = canonical_manifest_digest(manifest)
        if ledger["manifest_digest"] != actual_digest:
            errors.append(
                "evidence-ledger: manifest_digest does not match canonical manifest"
            )
        if review_context["manifest_digest"] != actual_digest:
            errors.append(
                "review-context: manifest_digest does not match canonical manifest"
            )
        if review_context["manifest_ref"] != ledger["manifest_ref"]:
            errors.append(
                "review-context.manifest_ref must equal evidence-ledger.manifest_ref"
            )
        if review_context["candidate_sha"] != ledger["candidate_sha"]:
            errors.append(
                "review-context candidate_sha must equal evidence-ledger candidate_sha"
            )
        if review_context["candidate_sha"] != manifest["basis"]["candidate_sha"]:
            errors.append(
                "review-context candidate_sha must equal manifest candidate_sha"
            )
        if review_context["context_policy"]["base_sha"] != manifest["basis"]["base_sha"]:
            errors.append(
                "review-context base_sha must equal manifest base_sha"
            )

    candidate, digest = _result_basis(manifest, ledger, review_context)

    if errors:
        return {
            "schema_version": "EVIDENCE_GATE_RESULT_V1",
            "authority": "DETERMINISTIC_EVIDENCE_GATE",
            "decision": "REPLAY_EVIDENCE",
            "candidate_sha": candidate,
            "manifest_digest": digest,
            "reason_codes": ["INVALID_REVIEW_BASIS"],
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
        description="Evaluate exact-candidate proof evidence under a fresh review context."
    )
    parser.add_argument("manifest")
    parser.add_argument("ledger")
    parser.add_argument("review_context")
    args = parser.parse_args()

    manifest = load_yaml(Path(args.manifest))
    ledger = load_yaml(Path(args.ledger))
    review_context = load_yaml(Path(args.review_context))

    result = gate_decision(manifest, ledger, review_context)
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
