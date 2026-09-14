from __future__ import annotations

from typing import Dict, List, Mapping, Optional, Sequence


class Core2BValidationError(ValueError):
    pass


LEVEL_ORDER = {
    "T0_DIRECT": 0,
    "T1_NEAR_TRANSFER": 1,
    "T2_REPRESENTATION_TRANSFER": 2,
    "T3_REVERSED_TARGET": 3,
    "T4_CONSTRAINT_TRANSFER": 4,
    "T5_DISCRIMINATION": 5,
    "T6_MULTI_STEP_BRIDGE": 6,
    "T7_SYNTHESIS": 7,
    "T8_COMPETITIVE_MIXED": 8,
}


def validate_session(session: Mapping, escalation_policy: Mapping, hint_policy: Mapping) -> None:
    if session.get("subject") != "PHYSICS":
        raise Core2BValidationError("session subject must be PHYSICS")
    state = session.get("learner_state")
    if state not in escalation_policy.get("state_permissions", {}):
        raise Core2BValidationError(f"unknown learner state: {state}")

    items = session.get("legal_items", [])
    if not items:
        raise Core2BValidationError("session requires at least one Core2A-legal item")
    seen = set()
    forbidden = tuple(hint_policy.get("learner_surface_forbidden_tokens", []))
    for item in items:
        item_id = item.get("item_id")
        if not item_id or item_id in seen:
            raise Core2BValidationError(f"invalid or duplicate item_id: {item_id!r}")
        seen.add(item_id)
        if item.get("core2a_legal") is not True:
            raise Core2BValidationError(f"Core2B cannot admit non-Core2A-legal item {item_id}")
        level = item.get("transfer_level")
        if level not in LEVEL_ORDER:
            raise Core2BValidationError(f"unknown transfer level for {item_id}: {level}")
        if not item.get("required_capability_refs"):
            raise Core2BValidationError(f"{item_id} requires capability refs")
        surface = "\n".join([item.get("prompt", ""), *item.get("hint_texts", [])]).upper()
        leaked = [token for token in forbidden if token.upper() in surface]
        if leaked:
            raise Core2BValidationError(f"internal runtime labels leaked for {item_id}: {leaked}")


def _representation_selectable(item: Mapping, representation_coverage: Sequence[str]) -> bool:
    required = item.get("required_representation")
    if not required:
        return True
    # A transfer item may use a taught convention; it need not already be mastered in reverse.
    return required in set(representation_coverage)


def selectable_items(session: Mapping, escalation_policy: Mapping) -> List[Mapping]:
    state = session["learner_state"]
    allowed = set(escalation_policy["state_permissions"][state])
    coverage = session.get("representation_coverage", [])
    return [
        item
        for item in session["legal_items"]
        if item["transfer_level"] in allowed and _representation_selectable(item, coverage)
    ]


def choose_next_item(session: Mapping, escalation_policy: Mapping) -> Mapping:
    candidates = selectable_items(session, escalation_policy)
    if not candidates:
        raise Core2BValidationError("no learner-selectable item remains inside the Core2A legal pool")

    purpose = session.get("purpose")
    retrieval_due = bool(session.get("retrieval_state", {}).get("due"))

    if retrieval_due:
        # Retrieval should first test independent access, not jump to the maximum structural level.
        candidates = sorted(candidates, key=lambda x: LEVEL_ORDER[x["transfer_level"]])
        for item in candidates:
            if item["transfer_level"] in {"T0_DIRECT", "T1_NEAR_TRANSFER", "T2_REPRESENTATION_TRANSFER"}:
                return item
        return candidates[0]

    if purpose == "FIRST_STUDY":
        return min(candidates, key=lambda x: LEVEL_ORDER[x["transfer_level"]])
    if purpose == "PRACTICE":
        near = [x for x in candidates if x["transfer_level"] == "T1_NEAR_TRANSFER"]
        if near:
            return near[0]
    # REVISION and COMPETITIVE_EXAM prefer the highest currently justified demand.
    return max(candidates, key=lambda x: LEVEL_ORDER[x["transfer_level"]])


def classify_attempt(attempt: Mapping, error_taxonomy: Mapping) -> List[str]:
    if attempt.get("outcome") == "CORRECT":
        return []
    declared = list(attempt.get("error_classes", []))
    allowed = set(error_taxonomy.get("error_classes", []))
    invalid = [x for x in declared if x not in allowed]
    if invalid:
        raise Core2BValidationError(f"unknown error classes: {invalid}")
    if declared:
        return declared

    evidence = attempt.get("response_evidence", {})
    if not evidence.get("model_selected"):
        return ["MODEL_SELECTION"]
    if not evidence.get("first_move"):
        return ["EQUATION_FORMATION"]
    if not evidence.get("final_answer"):
        return ["SYMBOLIC_MANIPULATION"]
    return ["CARELESS_EXECUTION"]


def build_core1b_repair_request(
    learner_profile_ref: str,
    capability_id: str,
    error_classes: Sequence[str],
    error_taxonomy: Mapping,
) -> Optional[dict]:
    routes = error_taxonomy.get("repair_routes", {})
    atom_refs: List[str] = []
    for error in error_classes:
        for ref in routes.get(error, []):
            if ref not in atom_refs:
                atom_refs.append(ref)
    if not atom_refs:
        return None
    return {
        "schema_version": "0.1.0",
        "request_id": f"C2B-TO-C1B-{capability_id}",
        "learner_profile_ref": learner_profile_ref,
        "capability_id": capability_id,
        "error_classes": list(error_classes),
        "repair_atom_refs": atom_refs,
        "instruction": "Repair the smallest listed prerequisite set, recheck independently, then return to Core2B.",
    }


def update_retrieval_state(current: Mapping, outcome: str, hint_level_used: str, representation: Optional[str] = None) -> dict:
    state = dict(current)
    state.setdefault("schema_version", "0.1.0")
    state["retrieval_count"] = int(state.get("retrieval_count", 0)) + 1
    streak = int(state.get("success_streak", 0))
    if outcome == "CORRECT":
        state["success_streak"] = streak + 1
        state["next_due_bucket"] = "LONG" if streak + 1 >= 3 else "MEDIUM"
    else:
        state["success_streak"] = 0
        state["next_due_bucket"] = "SHORT"

    if hint_level_used == "NO_HINT":
        state["hint_dependence"] = "NONE"
    elif hint_level_used in {"RETRIEVAL_CUE", "REPRESENTATION_CUE"}:
        state["hint_dependence"] = "LOW"
    elif hint_level_used in {"MODEL_CUE", "FIRST_MOVE_CUE"}:
        state["hint_dependence"] = "MEDIUM"
    else:
        state["hint_dependence"] = "HIGH"

    coverage = list(state.get("representation_coverage", []))
    if representation and representation not in coverage:
        coverage.append(representation)
    state["representation_coverage"] = coverage
    return state
