#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker

from coordlib import validate as schema_validate


SKILLS = Path(__file__).resolve().parents[2]
REPO_ROOT = SKILLS.parent
COMMON_PROFILE_SCHEMA = (
    SKILLS
    / "common-reviewer-protocol-v1.0"
    / "schemas"
    / "common-review-profile.schema.yaml"
)


def _schema_errors(schema: dict[str, Any], value: Any, label: str) -> list[str]:
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors: list[str] = []
    for error in sorted(validator.iter_errors(value), key=lambda item: list(item.path)):
        where = ".".join(str(part) for part in error.path)
        errors.append(f"{label}{'.' + where if where else ''}: {error.message}")
    return errors


def _resolve_repo_ref(
    ref: str,
    *,
    repository_root: Path = REPO_ROOT,
) -> tuple[Path | None, str | None]:
    prefix = "repo://"
    if not ref.startswith(prefix):
        return None, "unsupported ref scheme; expected repo://<relative-path>"
    relative = ref[len(prefix):]
    if not relative:
        return None, "repo ref is empty"

    root = repository_root.resolve()
    candidate = (root / relative).resolve()
    try:
        candidate.relative_to(root)
    except ValueError:
        return None, "repo ref escapes repository root"
    return candidate, None


def _file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def self_check_basis_attestation_errors(
    context: dict[str, Any],
    *,
    repository_root: Path = REPO_ROOT,
) -> list[str]:
    """Attest locally provable SELF_CHECK_CONTEXT_V1 basis claims.

    The manifest is mandatory and source-bound through a repo:// reference whose
    raw-file SHA-256 must equal manifest_digest. Repository context may include
    provider refs, but at least one repo:// context ref must resolve so a
    same-principal self-check cannot be grounded only in self-asserted labels.

    Provider-owned task identity and historical base availability are intentionally
    not guessed here; this validator attests only evidence the current checkout can
    prove.
    """
    errors: list[str] = []
    manifest_ref = context["manifest_ref"]
    manifest_path, manifest_error = _resolve_repo_ref(
        manifest_ref,
        repository_root=repository_root,
    )
    if manifest_error:
        errors.append(f"manifest_ref: {manifest_error}")
    elif manifest_path is None or not manifest_path.is_file():
        errors.append(f"manifest_ref does not resolve to a repository file: {manifest_ref}")
    else:
        actual = _file_digest(manifest_path)
        expected = context["manifest_digest"]
        if actual != expected:
            errors.append(
                "manifest_digest does not match source-bound manifest_ref "
                f"(expected {expected}, observed {actual})"
            )

    policy = context["reconstruction_policy"]
    source_bound_contexts = 0
    for ref in policy["repository_context_refs"]:
        if not ref.startswith("repo://"):
            continue
        source_bound_contexts += 1
        path, ref_error = _resolve_repo_ref(ref, repository_root=repository_root)
        if ref_error:
            errors.append(f"repository_context_ref {ref!r}: {ref_error}")
        elif path is None or not path.exists():
            errors.append(f"repository_context_ref does not resolve: {ref}")

    if source_bound_contexts == 0:
        errors.append(
            "reconstruction_policy.repository_context_refs must include at least "
            "one source-bound repo:// reference"
        )

    return errors


def validate_common_profile(value: Any, label: str = "common-review-profile") -> list[str]:
    with COMMON_PROFILE_SCHEMA.open("r", encoding="utf-8") as fh:
        schema = yaml.safe_load(fh)
    errors = _schema_errors(schema, value, label)
    if errors:
        return errors
    return [f"{label}: {error}" for error in common_profile_semantic_errors(value)]


def review_context_semantic_errors(context: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    reviewer = context["reviewer"]
    policy = context["context_policy"]
    if policy["candidate_sha"] != context["candidate_sha"]:
        errors.append("context_policy.candidate_sha must equal review candidate_sha")
    kind = reviewer["kind"]
    independence = reviewer["principal_independence"]
    if kind == "SAME_PRINCIPAL_FRESH_CONTEXT" and independence != "DEGRADED":
        errors.append("same-principal fresh-context review must record DEGRADED independence")
    if kind in {"DISTINCT_PRINCIPAL", "HUMAN_REVIEWER"} and independence != "DISTINCT":
        errors.append(f"{kind} must record DISTINCT principal independence")
    return errors


def self_check_context_semantic_errors(context: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    principal = context["principal"]
    policy = context["reconstruction_policy"]
    if policy["candidate_sha"] != context["candidate_sha"]:
        errors.append("reconstruction_policy.candidate_sha must equal self-check candidate_sha")
    if principal["principal_independence"] != "NONE":
        errors.append("solo self-check must record principal_independence NONE")
    if principal["blindness_claim"] != "NONE":
        errors.append("solo self-check cannot claim blinded or independent review")
    if not principal["fresh_reconstruction"]:
        errors.append("solo self-check requires fresh reconstruction")
    if policy["author_reasoning_used_as_evidence"]:
        errors.append("author reasoning cannot be used as self-check acceptance evidence")
    if policy["coder_confidence_used_as_evidence"]:
        errors.append("coder confidence cannot be used as self-check acceptance evidence")
    if policy["prior_self_check_used_as_evidence"]:
        errors.append("prior self-check cannot be used as current self-check acceptance evidence")
    return errors


def validate_assessment_context(value: Any, label: str = "assessment-context") -> list[str]:
    if not isinstance(value, dict):
        return [f"{label}: assessment context must be an object"]
    version = value.get("schema_version")
    if version == "SELF_CHECK_CONTEXT_V1":
        errors = schema_validate("self-check-context", value, label)
        if not errors:
            errors.extend(
                f"{label}: {error}"
                for error in self_check_context_semantic_errors(value)
            )
        return errors
    if version == "REVIEW_CONTEXT_V1":
        errors = schema_validate("review-context", value, label)
        if not errors:
            errors.extend(
                f"{label}: {error}"
                for error in review_context_semantic_errors(value)
            )
        return errors
    return [f"{label}: unsupported schema_version: {version!r}"]


def common_profile_semantic_errors(value: dict[str, Any]) -> list[str]:
    review = value["review_profile"]
    errors: list[str] = []
    role = review["role"]
    independence = review["principal_independence"]
    author = review["author_principal"]
    reviewer = review["review_principal"]

    if role == "SELF_REVIEW":
        if independence != "NONE":
            errors.append("SELF_REVIEW must record principal_independence NONE")
        if author != reviewer:
            errors.append("SELF_REVIEW author_principal and review_principal must match")
    else:
        if independence == "NONE":
            errors.append(f"{role} cannot record principal_independence NONE")
        if independence == "DEGRADED" and author != reviewer:
            errors.append("DEGRADED review must use the same principal identity")
        if independence == "DISTINCT_PRINCIPAL" and author == reviewer:
            errors.append("DISTINCT_PRINCIPAL review requires distinct principal identities")

    for criterion_id, criterion in review["common_criteria"].items():
        applicability = criterion["applicability"]
        result = criterion["result"]
        if applicability == "REQUIRED" and result in {"NOT_APPLICABLE", "WAIVED"}:
            errors.append(f"{criterion_id}: REQUIRED criterion cannot be {result}")
        if result == "PASS" and not criterion.get("evidence_refs"):
            errors.append(f"{criterion_id}: PASS requires at least one evidence_ref")

    if review.get("result") == "COMPLETE":
        if review.get("unresolved_required_findings", 0) != 0:
            errors.append("COMPLETE review cannot have unresolved required findings")
        if not review.get("final_candidate"):
            errors.append("COMPLETE review requires final_candidate")
        for criterion_id, criterion in review["common_criteria"].items():
            if criterion["applicability"] == "REQUIRED" and criterion["result"] != "PASS":
                errors.append(
                    f"{criterion_id}: COMPLETE review requires PASS for REQUIRED criterion"
                )

    return errors


def review_basis_errors(
    profile: Any,
    assessment_context: Any,
) -> list[str]:
    errors = validate_common_profile(profile)
    errors.extend(validate_assessment_context(assessment_context))
    if errors:
        return errors

    if assessment_context["schema_version"] == "SELF_CHECK_CONTEXT_V1":
        errors.extend(self_check_basis_attestation_errors(assessment_context))
        if errors:
            return errors

    review = profile["review_profile"]
    role = review["role"]
    version = assessment_context["schema_version"]

    if role == "SELF_REVIEW":
        if version != "SELF_CHECK_CONTEXT_V1":
            errors.append("SELF_REVIEW requires SELF_CHECK_CONTEXT_V1")
        else:
            principal = assessment_context["principal"]
            if principal["identity"] != review["review_principal"]:
                errors.append("self-check principal identity must match review_principal")
    else:
        if version != "REVIEW_CONTEXT_V1":
            errors.append(f"{role} requires REVIEW_CONTEXT_V1")
        else:
            reviewer = assessment_context["reviewer"]
            if reviewer["identity"] != review["review_principal"]:
                errors.append("review-context reviewer identity must match review_principal")
            expected = (
                "DEGRADED"
                if review["principal_independence"] == "DEGRADED"
                else "DISTINCT"
            )
            if reviewer["principal_independence"] != expected:
                errors.append(
                    "review-context independence must match Common Review Profile"
                )

    final_candidate = review.get("final_candidate")
    if final_candidate and assessment_context["candidate_sha"] != final_candidate:
        errors.append("assessment context candidate must equal profile final_candidate")

    return errors


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Validate a Common Review Profile and selected assessment context. "
            "This validates review basis only and never emits engineering PASS "
            "or lifecycle advancement."
        )
    )
    parser.add_argument("profile")
    parser.add_argument("assessment_context")
    args = parser.parse_args()

    with Path(args.profile).open("r", encoding="utf-8") as fh:
        profile = yaml.safe_load(fh)
    with Path(args.assessment_context).open("r", encoding="utf-8") as fh:
        context = yaml.safe_load(fh)

    errors = review_basis_errors(profile, context)
    if errors:
        for error in errors:
            print(error)
        raise SystemExit(1)
    print("OK: review basis/context is coherent; no acceptance decision emitted")


if __name__ == "__main__":
    main()
