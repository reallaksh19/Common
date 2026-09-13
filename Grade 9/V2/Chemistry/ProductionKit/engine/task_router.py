from __future__ import annotations

import argparse
from copy import deepcopy
from pathlib import Path
from typing import Any

from common import ProductionKitError, digest, kit_root, load_json, write_json


ALLOWED_PRODUCTS = {"CORE1", "CORE2", "CORE1A", "CORE2A"}
ALLOWED_PURPOSES = {"STARTER", "PRACTICE", "REVISION", "COMPETITION"}


def _load_registries() -> tuple[dict[str, Any], dict[str, Any]]:
    profiles = load_json(kit_root() / "registry" / "scaffold-profiles.json")
    routes = load_json(kit_root() / "registry" / "product-routes.json")
    return profiles, routes


def route_task(
    task: dict[str, Any],
    profiles_registry: dict[str, Any] | None = None,
    routes_registry: dict[str, Any] | None = None,
) -> dict[str, Any]:
    profiles_registry, routes_registry = (
        (profiles_registry, routes_registry)
        if profiles_registry is not None and routes_registry is not None
        else _load_registries()
    )

    product = task.get("product")
    if product not in ALLOWED_PRODUCTS:
        raise ProductionKitError("PRODUCTION_PRODUCT_UNSUPPORTED", repr(product))
    if not task.get("task_id") or not task.get("topic"):
        raise ProductionKitError("PRODUCTION_TASK_INCOMPLETE", "task_id and topic are required")
    refs = task.get("question_refs") or []
    if not refs or len(set(refs)) != len(refs):
        raise ProductionKitError("PRODUCTION_QUESTION_DENOMINATOR_INVALID", "question_refs must be non-empty and unique")

    routes = routes_registry["routes"]
    profile_map = profiles_registry["profiles"]
    route_spec = routes[product]
    purpose = task.get("purpose")

    if product == "CORE2A":
        if purpose not in ALLOWED_PURPOSES:
            raise ProductionKitError(
                "CORE2A_PURPOSE_UNRESOLVED",
                "Core (2A) requires STARTER, PRACTICE, REVISION, or COMPETITION",
            )
        profile_id = route_spec["profiles_by_purpose"][purpose]
    else:
        if purpose not in (None, ""):
            raise ProductionKitError(
                "PRODUCTION_PURPOSE_NOT_APPLICABLE",
                f"purpose is only routed for CORE2A, got {purpose} for {product}",
            )
        profile_id = route_spec["profile_id"]

    profile = deepcopy(profile_map[profile_id])
    constraints = task.get("constraints") or {}
    requested_max = constraints.get("max_pages_per_question")
    if requested_max is not None:
        if requested_max > profile["max_pages_per_question"]:
            raise ProductionKitError(
                "PRODUCTION_PAGE_BUDGET_RELAXATION_FORBIDDEN",
                f"requested {requested_max} > governed {profile['max_pages_per_question']}",
            )
        profile["max_pages_per_question"] = requested_max

    if product == "CORE2A":
        if constraints.get("source_on_sheet1") is False:
            raise ProductionKitError(
                "CORE2A_SHEET1_SOURCE_MISSING",
                "Core (2A) may not disable Sheet-1 source/provenance display",
            )
        profile["source_on_sheet1"] = True

    if product == "CORE2A" and purpose == "COMPETITION":
        benchmarks = task.get("benchmark_sources") or []
        minimum = int(profile.get("minimum_external_benchmarks", 2))
        if len(benchmarks) < minimum:
            raise ProductionKitError(
                "CORE2A_COMPETITION_CONSTRUCTION_RESEARCH_MISSING",
                f"need at least {minimum} external benchmark sources; got {len(benchmarks)}",
            )
        for source in benchmarks:
            if source.get("role") != "CONSTRUCTION_REFERENCE" or not str(source.get("url", "")).startswith(("http://", "https://")):
                raise ProductionKitError(
                    "CORE2A_COMPETITION_BENCHMARK_INVALID",
                    "competition benchmarks need a web URL and CONSTRUCTION_REFERENCE role",
                )

    route_plan = {
        "task_id": task["task_id"],
        "product": product,
        "purpose": purpose if product == "CORE2A" else None,
        "topic": task["topic"],
        "question_refs": list(refs),
        "profile_id": profile_id,
        "profile": profile,
        "stages": list(route_spec["stages"]),
        "requested_output": task.get("requested_output", "RENDER_READY_PACKET"),
        "benchmark_sources": deepcopy(task.get("benchmark_sources") or []),
    }
    route_plan["route_digest"] = digest(route_plan)
    return route_plan


def main() -> int:
    parser = argparse.ArgumentParser(description="Route a Chemistry Core1/Core2/Core1A/Core2A production task")
    parser.add_argument("--task", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    plan = route_task(load_json(args.task))
    write_json(Path(args.out), plan)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
