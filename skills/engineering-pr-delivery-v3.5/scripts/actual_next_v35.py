#!/usr/bin/env python3
"""Pure deterministic actual-next derivation for Engineering Relay V3.5.

R-P2-NEXT consumes the canonical eight-condition read model plus the current
derived LEAF state and returns one decision. It does not render or publish
LIVE_STATUS, mutate titles/frontier/admission/provider state, or author
progress.

Authority: DERIVED_ACTUAL_NEXT_ONLY.
"""

from __future__ import annotations

from typing import Any, Mapping, Sequence

from delp_projection_v35 import CONDITION_ORDER, DelpError, validate_condition

AUTHORITY = "DERIVED_ACTUAL_NEXT_ONLY"

ACTIONS = (
    "NONE",
    "FIX_PLAN",
    "RECONCILE_SPEC",
    "RECOVER_CUSTODY",
    "MATERIALIZE_FACTS",
    "WAIT_PROVIDER",
    "RECOVER_EVIDENCE",
    "RECONCILE_HANDOFF",
    "WAIT_DEPENDENCY",
    "REMEDIATE_FINDING",
    "REVIEW_CANDIDATE",
    "WAIT_OWNER",
    "CONTINUE_UNIT",
    "PUBLISH_RESULT",
)

_TERMINAL_LIFECYCLES = frozenset({"COMPLETE", "SUPERSEDED"})


def _condition_index(raw: Any) -> dict[str, Mapping[str, Any]]:
    if not isinstance(raw, Sequence) or isinstance(raw, (str, bytes, bytearray)):
        raise DelpError("actual-next conditions: canonical condition array required")

    by_type: dict[str, Mapping[str, Any]] = {}
    for index, row in enumerate(raw):
        errors = validate_condition(row)
        if errors:
            raise DelpError(
                f"actual-next conditions[{index}]: " + "; ".join(errors)
            )
        kind = str(row["type"])
        if kind in by_type:
            raise DelpError(f"actual-next conditions: duplicate {kind}")
        by_type[kind] = row

    missing = [kind for kind in CONDITION_ORDER if kind not in by_type]
    extra = sorted(set(by_type) - set(CONDITION_ORDER))
    if missing or extra or len(by_type) != len(CONDITION_ORDER):
        raise DelpError(
            f"actual-next conditions: exact canonical set required; missing={missing}, extra={extra}"
        )
    return by_type


def _condition_basis(row: Mapping[str, Any]) -> list[str]:
    basis = [
        f"condition:{row['type']}:{row['status']}:{row['reason']}",
    ]
    basis.extend(f"ref:{ref}" for ref in sorted(row.get("source_refs") or []))
    return basis


def _decision(
    action: str,
    reason: str,
    source_basis: Sequence[str],
    detail: str | None = None,
) -> dict[str, Any]:
    if action not in ACTIONS:
        raise DelpError(f"actual-next action: unsupported {action}")
    return {
        "authority": AUTHORITY,
        "action": action,
        "reason": reason,
        "source_basis": list(dict.fromkeys(source_basis)),
        "detail": detail,
    }


def _accepted_facts_exist(leaf: Mapping[str, Any]) -> bool:
    epoch = leaf.get("activity_epoch", 0)
    if isinstance(epoch, bool):
        return False
    try:
        return int(epoch or 0) > 0
    except (TypeError, ValueError):
        return False


def _declared_dependencies(leaf: Mapping[str, Any]) -> list[str]:
    dependencies = leaf.get("dependencies") or {}
    declared = dependencies.get("declared") if isinstance(dependencies, Mapping) else None
    if declared is None:
        return []
    if not isinstance(declared, list) or not all(isinstance(ref, str) and ref for ref in declared):
        raise DelpError("actual-next leaf.dependencies.declared: string array required")
    return list(declared)


def _all_units_complete(leaf: Mapping[str, Any]) -> bool:
    units = leaf.get("units")
    return bool(
        isinstance(units, list)
        and units
        and all(isinstance(row, Mapping) and row.get("complete") is True for row in units)
    )


def _delivery_review_outstanding(leaf: Mapping[str, Any]) -> bool:
    gates = leaf.get("gates")
    if not isinstance(gates, list) or not gates:
        return False
    return any(
        not isinstance(row, Mapping)
        or row.get("passed") is not True
        or row.get("evidence_current") is not True
        for row in gates
    )


def _owner_action_pending(leaf: Mapping[str, Any]) -> bool:
    value = leaf.get("owner_action")
    if value is None:
        return False
    text = str(value).strip()
    return bool(text and text.upper() != "NONE")


def _handoff_reconciliation_required(leaf: Mapping[str, Any]) -> bool:
    policy = leaf.get("successor_policy")
    handover = leaf.get("handover")
    return bool(
        isinstance(policy, Mapping)
        and policy.get("mode") == "INDEPENDENT_RECONSTRUCTION"
        and isinstance(handover, Mapping)
        and handover.get("status") != "RECONCILED"
    )


def derive_actual_next(leaf: Any) -> dict[str, Any]:
    """Return one deterministic actual-next decision for a canonical LEAF projection.

    The function consumes already-derived conditions. It does not recompute
    condition truth and never treats executor-authored leaf.next as authority;
    that field is used only to decorate CONTINUE_UNIT detail.
    """
    if not isinstance(leaf, Mapping):
        raise DelpError("actual-next leaf: mapping required")

    conditions = _condition_index(leaf.get("conditions"))
    lifecycle = str(leaf.get("lifecycle") or "")

    if lifecycle in _TERMINAL_LIFECYCLES:
        return _decision(
            "NONE",
            "TERMINAL_LIFECYCLE",
            [f"leaf.lifecycle:{lifecycle}"],
            f"{lifecycle} Responsibility has no further actual-next action.",
        )

    plan = conditions["PlanReady"]
    if plan["status"] == "FALSE":
        return _decision("FIX_PLAN", "PLAN_NOT_READY", _condition_basis(plan), plan["message"])

    spec = conditions["SpecCurrent"]
    if spec["status"] == "FALSE":
        return _decision(
            "RECONCILE_SPEC",
            "SPEC_NOT_CURRENT",
            _condition_basis(spec),
            spec["message"],
        )
    if (
        spec["status"] == "UNKNOWN"
        and _accepted_facts_exist(leaf)
        and spec.get("reason") != "SPEC_BINDING_UNAVAILABLE"
    ):
        return _decision(
            "RECONCILE_SPEC",
            "SPEC_CURRENTNESS_UNKNOWN_WITH_ACCEPTED_FACTS",
            _condition_basis(spec) + ["leaf:accepted_facts_present"],
            spec["message"],
        )

    custody = conditions["CustodySafe"]
    if custody["status"] == "FALSE":
        return _decision(
            "RECOVER_CUSTODY",
            "CUSTODY_UNSAFE",
            _condition_basis(custody),
            custody["message"],
        )

    materialization = leaf.get("materialization")
    if isinstance(materialization, Mapping) and materialization.get("status") == "UNMATERIALIZED":
        signal = str(materialization.get("provider_signal") or "provider work observed")
        return _decision(
            "MATERIALIZE_FACTS",
            "PROVIDER_WORK_WITHOUT_ACCEPTED_FACTS",
            ["leaf.materialization:UNMATERIALIZED", f"leaf.provider_signal:{signal}"],
            "Publish CHECKPOINT_FACTS_V1 for exactly what current evidence supports.",
        )

    provider = conditions["ProviderVisible"]
    material = conditions["MaterialObserved"]
    evidence = conditions["EvidenceCurrent"]
    if (
        provider["status"] == "UNKNOWN"
        and _accepted_facts_exist(leaf)
        and (material["status"] == "UNKNOWN" or evidence["status"] == "UNKNOWN")
    ):
        return _decision(
            "WAIT_PROVIDER",
            "PROVIDER_VISIBILITY_REQUIRED",
            _condition_basis(provider)
            + _condition_basis(material)
            + _condition_basis(evidence)
            + ["leaf:accepted_facts_present"],
            provider["message"],
        )

    if evidence["status"] == "FALSE":
        return _decision(
            "RECOVER_EVIDENCE",
            "EVIDENCE_NOT_CURRENT",
            _condition_basis(evidence),
            evidence["message"],
        )

    if _handoff_reconciliation_required(leaf):
        policy = leaf["successor_policy"]
        handover = leaf["handover"]
        return _decision(
            "RECONCILE_HANDOFF",
            "INDEPENDENT_RECONSTRUCTION_REQUIRED",
            [
                "leaf.successor_policy:INDEPENDENT_RECONSTRUCTION",
                f"leaf.handover:{handover.get('status')}",
            ],
            str(
                policy.get("decision_at_risk")
                or "Independent-reconstruction handoff must be reconciled before continuation."
            ),
        )

    dependencies = conditions["DependenciesReady"]
    declared = _declared_dependencies(leaf)
    if declared:
        if dependencies["status"] in {"FALSE", "UNKNOWN"}:
            return _decision(
                "WAIT_DEPENDENCY",
                "DEPENDENCIES_NOT_READY",
                _condition_basis(dependencies)
                + [f"leaf.dependency:{ref}" for ref in sorted(declared)],
                dependencies["message"],
            )
        if dependencies["status"] == "NOT_APPLICABLE":
            raise DelpError(
                "actual-next dependency contradiction: declared dependencies with NOT_APPLICABLE DependenciesReady"
            )

    assurance = conditions["AssuranceSatisfied"]
    if assurance["status"] == "FALSE":
        return _decision(
            "REMEDIATE_FINDING",
            "ASSURANCE_NOT_SATISFIED",
            _condition_basis(assurance),
            assurance["message"],
        )

    units_complete = _all_units_complete(leaf)
    if units_complete and _delivery_review_outstanding(leaf):
        return _decision(
            "REVIEW_CANDIDATE",
            "DELIVERY_REVIEW_OUTSTANDING",
            ["leaf.units:COMPLETE", "leaf.delivery_gates:OPEN"],
            "Implementation units are complete but a declared delivery gate remains open.",
        )

    if _owner_action_pending(leaf):
        return _decision(
            "WAIT_OWNER",
            "OWNER_ACTION_REQUIRED",
            ["leaf.owner_action"],
            str(leaf.get("owner_action")),
        )

    active_unit = leaf.get("active_unit")
    if isinstance(active_unit, str) and active_unit:
        proposed = leaf.get("next")
        decoration = None
        if isinstance(proposed, Mapping):
            raw = proposed.get("action")
            if isinstance(raw, str) and raw.strip():
                decoration = raw.strip()
        return _decision(
            "CONTINUE_UNIT",
            "ACTIVE_UNIT_AVAILABLE",
            [f"leaf.active_unit:{active_unit}"],
            f"{active_unit}" + (f" — {decoration}" if decoration else ""),
        )

    if units_complete:
        return _decision(
            "PUBLISH_RESULT",
            "IMPLEMENTATION_UNITS_COMPLETE",
            ["leaf.units:COMPLETE", "leaf.delivery_gates:CLEAR"],
            "Publish the Responsibility result; no higher-priority action remains.",
        )

    raise DelpError(
        "actual-next leaf state is incomplete but exposes no active unit or higher-priority recovery/wait action"
    )
