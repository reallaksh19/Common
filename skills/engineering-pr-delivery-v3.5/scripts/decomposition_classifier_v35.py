from __future__ import annotations

from typing import Any, Mapping

SCHEMA_PREFIX = "relay-v3.5-delp"
DECOMPOSITION_ASSESSMENT_SCHEMA = f"{SCHEMA_PREFIX}-decomposition-assessment"
DECOMPOSITION_DECISION_SCHEMA = f"{SCHEMA_PREFIX}-decomposition-decision"

DECOMPOSITION_DECISIONS = ("PASS", "SPLIT", "MERGE", "DISCOVER_FIRST", "REPLAN")
EXECUTION_BOUNDARY_DECISIONS = (
    "INLINE_SAFE",
    "CHECKPOINT_REQUIRED",
    "ETX_SPLIT_REQUIRED",
    "OBSERVE_BEFORE_RETRY_REQUIRED",
    "DISCOVERY_REQUIRED",
)
ASSESSMENT_PROPOSAL_KINDS = ("LEAF", "ADJACENT_CHILDREN")
ASSESSMENT_SEMANTIC_COHESION = ("COHESIVE", "MIXED", "UNKNOWN")
ASSESSMENT_DEPENDENCY_CLOSURE = ("CLOSED", "OPEN", "UNKNOWN")
ASSESSMENT_VERIFICATION_CLOSURE = ("CLOSED", "DEFERRED", "UNKNOWN")
ASSESSMENT_UNCERTAINTY = ("LOW", "MATERIAL", "BLOCKING")
ASSESSMENT_CHANGE_IMPACT = ("LOCAL", "BOUNDED_MULTI_STAGE", "CROSS_CUTTING", "UNKNOWN")
ASSESSMENT_EXECUTION_HORIZON = ("SHORT", "MULTI_STEP", "LONG_OR_AMBIGUOUS")
ASSESSMENT_MUTATION_DOMAINS = (
    "LOCAL_FILES",
    "GIT_HISTORY",
    "REMOTE_BRANCH",
    "GITHUB_ISSUE",
    "GITHUB_PR",
    "CI",
    "BROWSER",
    "EXTERNAL_SERVICE",
)
ASSESSMENT_RECOVERY_RADIUS = ("SMALL", "MULTI_SURFACE", "AMBIGUOUS_EXTERNAL")
ASSESSMENT_HANDOFF_COST = ("LOW", "MATERIAL", "HIGH")
ASSESSMENT_CROSS_CHILD_COHESION = ("LOW", "HIGH")


class DecompositionError(ValueError):
    """A decomposition assessment is malformed or cannot be classified safely."""


def validate_decomposition_assessment(value: Any) -> list[str]:
    """Validate normalized plan/observer input to the pure classifier."""
    if not isinstance(value, Mapping):
        return ["assessment: must be a mapping"]

    required = {
        "schema",
        "subject",
        "proposal_kind",
        "semantic_cohesion",
        "dependency_closure",
        "verification_closure",
        "uncertainty",
        "change_impact",
        "execution_horizon",
        "mutation_domains",
        "recovery_radius",
        "handoff_cost",
        "cross_child_cohesion",
        "stable_cut",
        "basis_moved",
    }
    errors: list[str] = []
    keys = set(map(str, value))
    missing = sorted(required - keys)
    extra = sorted(keys - required)
    if missing:
        errors.append(f"assessment: missing fields {missing}")
    if extra:
        errors.append(f"assessment: unknown fields {extra}")

    if value.get("schema") != DECOMPOSITION_ASSESSMENT_SCHEMA:
        errors.append(f"schema: must be {DECOMPOSITION_ASSESSMENT_SCHEMA}")
    subject = value.get("subject")
    if not isinstance(subject, str) or not subject.strip():
        errors.append("subject: must be a non-blank string")

    enum_fields = {
        "proposal_kind": ASSESSMENT_PROPOSAL_KINDS,
        "semantic_cohesion": ASSESSMENT_SEMANTIC_COHESION,
        "dependency_closure": ASSESSMENT_DEPENDENCY_CLOSURE,
        "verification_closure": ASSESSMENT_VERIFICATION_CLOSURE,
        "uncertainty": ASSESSMENT_UNCERTAINTY,
        "change_impact": ASSESSMENT_CHANGE_IMPACT,
        "execution_horizon": ASSESSMENT_EXECUTION_HORIZON,
        "recovery_radius": ASSESSMENT_RECOVERY_RADIUS,
        "handoff_cost": ASSESSMENT_HANDOFF_COST,
        "cross_child_cohesion": ASSESSMENT_CROSS_CHILD_COHESION,
    }
    for field, allowed in enum_fields.items():
        item = value.get(field)
        if not isinstance(item, str) or item not in allowed:
            errors.append(f"{field}: one of {list(allowed)}")

    domains = value.get("mutation_domains")
    if not isinstance(domains, list):
        errors.append("mutation_domains: must be an array")
    elif any(not isinstance(domain, str) for domain in domains):
        errors.append("mutation_domains: every value must be a string")
    else:
        if len(domains) != len(set(domains)):
            errors.append("mutation_domains: values must be unique")
        unknown = sorted(set(domains) - set(ASSESSMENT_MUTATION_DOMAINS))
        if unknown:
            errors.append(f"mutation_domains: unknown values {unknown}")

    stable = value.get("stable_cut")
    stable_fields = {
        "output_contract",
        "independent_oracle",
        "consumer_stable",
        "risk_reduction",
        "handoff_economy",
    }
    if not isinstance(stable, Mapping):
        errors.append("stable_cut: must be a mapping")
    else:
        stable_keys = set(map(str, stable))
        missing_stable = sorted(stable_fields - stable_keys)
        extra_stable = sorted(stable_keys - stable_fields)
        if missing_stable:
            errors.append(f"stable_cut: missing fields {missing_stable}")
        if extra_stable:
            errors.append(f"stable_cut: unknown fields {extra_stable}")
        for field in stable_fields:
            if field in stable and not isinstance(stable.get(field), bool):
                errors.append(f"stable_cut.{field}: must be boolean")

    if not isinstance(value.get("basis_moved"), bool):
        errors.append("basis_moved: must be boolean")
    return errors


def _stable_cut_is_beneficial(assessment: Mapping[str, Any]) -> bool:
    stable = assessment["stable_cut"]
    return all(
        bool(stable.get(field))
        for field in (
            "output_contract",
            "independent_oracle",
            "consumer_stable",
            "risk_reduction",
            "handoff_economy",
        )
    )


def _execution_boundary(assessment: Mapping[str, Any], decision: str) -> str:
    if decision == "DISCOVER_FIRST":
        return "DISCOVERY_REQUIRED"
    domains = assessment["mutation_domains"]
    if assessment["recovery_radius"] == "AMBIGUOUS_EXTERNAL":
        return "OBSERVE_BEFORE_RETRY_REQUIRED"
    if (
        assessment["execution_horizon"] == "LONG_OR_AMBIGUOUS"
        or len(domains) >= 3
        or (assessment["recovery_radius"] == "MULTI_SURFACE" and len(domains) >= 2)
    ):
        return "ETX_SPLIT_REQUIRED"
    if (
        assessment["execution_horizon"] == "MULTI_STEP"
        or len(domains) >= 2
        or assessment["recovery_radius"] == "MULTI_SURFACE"
    ):
        return "CHECKPOINT_REQUIRED"
    return "INLINE_SAFE"


def classify_decomposition_assessment(value: Any) -> dict[str, Any]:
    """Return deterministic semantic and execution-boundary decisions.

    Precedence: REPLAN -> DISCOVER_FIRST -> MERGE -> SPLIT -> PASS.
    """
    errors = validate_decomposition_assessment(value)
    if errors:
        raise DecompositionError("invalid DECOMPOSITION_ASSESSMENT_V1: " + "; ".join(errors))

    assessment = dict(value)
    stable_cut = _stable_cut_is_beneficial(assessment)
    reasons: list[str] = []

    if assessment["basis_moved"]:
        decision = "REPLAN"
        reasons.append("BASIS_MOVED")
    elif (
        assessment["uncertainty"] == "BLOCKING"
        or assessment["semantic_cohesion"] == "UNKNOWN"
        or assessment["dependency_closure"] == "UNKNOWN"
        or assessment["verification_closure"] == "UNKNOWN"
        or assessment["change_impact"] == "UNKNOWN"
    ):
        decision = "DISCOVER_FIRST"
        reasons.append("IMPLEMENTATION_BASIS_UNKNOWN")
    elif assessment["dependency_closure"] == "OPEN" and not stable_cut:
        decision = "DISCOVER_FIRST"
        reasons.append("DEPENDENCY_NOT_CLOSED")
    elif (
        assessment["proposal_kind"] == "ADJACENT_CHILDREN"
        and assessment["semantic_cohesion"] == "COHESIVE"
        and assessment["dependency_closure"] == "CLOSED"
        and assessment["verification_closure"] == "CLOSED"
        and assessment["cross_child_cohesion"] == "HIGH"
        and assessment["handoff_cost"] in {"MATERIAL", "HIGH"}
        and not stable_cut
    ):
        decision = "MERGE"
        reasons.extend(["HIGH_CROSS_CHILD_COHESION", "NO_BENEFICIAL_STABLE_CUT"])
    elif (
        assessment["semantic_cohesion"] == "MIXED"
        or stable_cut
        or assessment["verification_closure"] == "DEFERRED"
    ):
        decision = "SPLIT"
        if assessment["semantic_cohesion"] == "MIXED":
            reasons.append("MIXED_SEMANTIC_OUTCOME")
        if stable_cut:
            reasons.append("BENEFICIAL_STABLE_CUT")
        if assessment["verification_closure"] == "DEFERRED":
            reasons.append("LEAF_VERIFICATION_DEFERRED")
    else:
        decision = "PASS"
        reasons.append("COHESIVE_CLOSED_VERIFIABLE_LEAF")

    return {
        "schema": DECOMPOSITION_DECISION_SCHEMA,
        "assessment_schema": DECOMPOSITION_ASSESSMENT_SCHEMA,
        "subject": assessment["subject"],
        "decision": decision,
        "reasons": reasons,
        "stable_cut": stable_cut,
        "execution_boundary": _execution_boundary(assessment, decision),
    }
