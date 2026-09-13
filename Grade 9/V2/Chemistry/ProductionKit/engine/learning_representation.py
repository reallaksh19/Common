from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from common import ProductionKitError, chemistry_root, digest, load_json, write_json


def _registry_paths() -> tuple[Path, Path]:
    root = chemistry_root() / "Representation" / "registry"
    return root / "chemistry-page-intent-profile.json", root / "chemistry-teaching-primitive-registry.json"


def _load_authority() -> tuple[dict[str, Any], dict[str, Any]]:
    profile_path, primitive_path = _registry_paths()
    return load_json(profile_path), load_json(primitive_path)


def _topic_allows(primitive: dict[str, Any], topic: str) -> bool:
    scopes = primitive.get("topic_scope_refs") or []
    if not scopes:
        return True
    normalized = topic.upper().replace(" ", "_").replace("-", "_")
    return any(scope.upper() in normalized for scope in scopes)


def build_representation_plan(
    task: dict[str, Any],
    route_plan: dict[str, Any],
    questions: list[dict[str, Any]],
    page_profile: dict[str, Any] | None = None,
    primitive_registry: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if page_profile is None or primitive_registry is None:
        page_profile, primitive_registry = _load_authority()

    primary = page_profile.get("primary_primitives_by_capability") or {}
    primitives = {p["primitive_id"]: p for p in primitive_registry.get("primitives") or []}
    required_ids = set(primitive_registry.get("required_primitive_ids") or [])
    missing_registry_ids = sorted(required_ids - set(primitives))
    if missing_registry_ids:
        raise ProductionKitError(
            "REPRESENTATION_REGISTRY_INCOMPLETE",
            ", ".join(missing_registry_ids),
        )

    plans: list[dict[str, Any]] = []
    for question in questions:
        qid = question["question_id"]
        requests: list[dict[str, Any]] = []
        seen: set[str] = set()
        for capability in question.get("capability_refs") or []:
            primitive_ids = primary.get(capability)
            if not primitive_ids:
                raise ProductionKitError(
                    "REPRESENTATION_CAPABILITY_UNMAPPED",
                    f"{qid}: {capability}",
                )
            for primitive_id in primitive_ids:
                primitive = primitives.get(primitive_id)
                if primitive is None:
                    raise ProductionKitError(
                        "REPRESENTATION_PRIMITIVE_UNKNOWN",
                        f"{qid}: {primitive_id}",
                    )
                if capability not in (primitive.get("capability_refs") or []):
                    raise ProductionKitError(
                        "REPRESENTATION_CAPABILITY_PRIMITIVE_MISMATCH",
                        f"{qid}: {capability} -> {primitive_id}",
                    )
                if not _topic_allows(primitive, task["topic"]):
                    raise ProductionKitError(
                        "REPRESENTATION_TOPIC_SCOPE_VIOLATION",
                        f"{qid}: {primitive_id} not allowed for {task['topic']}",
                    )
                if primitive_id in seen:
                    continue
                seen.add(primitive_id)
                requests.append(
                    {
                        "primitive_id": primitive_id,
                        "capability_ref": capability,
                        "instructional_job": primitive["instructional_job"],
                        "learner_action": primitive["learner_action"],
                        "renderer_constraints": list(primitive.get("renderer_constraints") or []),
                        "topic_scope_refs": list(primitive.get("topic_scope_refs") or []),
                    }
                )

        # Verification is an explicit learning representation when the registry supports it.
        if "VERIFICATION" in (route_plan["profile"].get("required_blocks") or []):
            check_id = "FORMULA_EQUATION_CHECK_STRIP"
            check = primitives.get(check_id)
            supported_caps = set(check.get("capability_refs") or []) if check else set()
            if check and any(cap in supported_caps for cap in question.get("capability_refs") or []) and check_id not in seen:
                requests.append(
                    {
                        "primitive_id": check_id,
                        "capability_ref": "VERIFICATION",
                        "instructional_job": check["instructional_job"],
                        "learner_action": check["learner_action"],
                        "renderer_constraints": list(check.get("renderer_constraints") or []),
                        "topic_scope_refs": list(check.get("topic_scope_refs") or []),
                    }
                )

        if not requests:
            raise ProductionKitError("REPRESENTATION_PLAN_EMPTY", qid)
        plans.append({"question_id": qid, "requests": requests})

    plan = {
        "task_id": task["task_id"],
        "product": task["product"],
        "topic": task["topic"],
        "page_intent_profile_id": page_profile.get("profile_id"),
        "primitive_registry_id": primitive_registry.get("registry_id"),
        "question_plans": plans,
        "status": "PASS",
    }
    plan["representation_plan_digest"] = digest(plan)
    return plan


def validate_representation_plan(plan: dict[str, Any], questions: list[dict[str, Any]]) -> None:
    expected = [q["question_id"] for q in questions]
    actual = [item["question_id"] for item in plan.get("question_plans") or []]
    if expected != actual:
        raise ProductionKitError(
            "REPRESENTATION_QUESTION_CUSTODY_MISMATCH",
            f"expected={expected}; actual={actual}",
        )
    for item in plan["question_plans"]:
        if not item.get("requests"):
            raise ProductionKitError("REPRESENTATION_PLAN_EMPTY", item["question_id"])
        for request in item["requests"]:
            if not request.get("instructional_job") or not request.get("learner_action"):
                raise ProductionKitError(
                    "REPRESENTATION_SEMANTICS_INCOMPLETE",
                    f"{item['question_id']}: {request.get('primitive_id')}",
                )


def main() -> int:
    parser = argparse.ArgumentParser(description="Build and validate Chemistry learning representations")
    parser.add_argument("--task", required=True)
    parser.add_argument("--route-plan", required=True)
    parser.add_argument("--questions", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    task = load_json(args.task)
    route = load_json(args.route_plan)
    questions = load_json(args.questions)
    plan = build_representation_plan(task, route, questions)
    validate_representation_plan(plan, questions)
    write_json(args.out, plan)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
