#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PHYS = ROOT.parent
CORE1A = PHYS / "Core1A"
REP = PHYS / "Representation"


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def real_chapter_plan():
    builder = _module("bp_m2d_chapter_builder", CORE1A / "engine" / "build_motion_in_a_plane_chapter.py")
    reg = CORE1A / "registry"
    return builder.compile_plan(
        load(reg / "physics-core1a-motion-in-a-plane-source-inventory.json"),
        load(reg / "physics-core1a-motion-in-a-plane-chapter-v1.json"),
        load(reg / "physics-core1a-core2-linkage.json"),
    )


def combined_primitive_registry():
    base = load(REP / "registry" / "physics-teaching-primitive-registry.json")
    ext = load(REP / "registry" / "physics-2d-teaching-primitive-registry-v1.json")
    base_ids = {row["primitive_id"] for row in base.get("primitives") or []}
    ext_ids = {row["primitive_id"] for row in ext.get("primitives") or []}
    overlap = sorted(base_ids & ext_ids)
    if overlap:
        raise AssertionError("M2D_RENDER_PRIMITIVE_REGISTRY_COLLISION:" + ",".join(overlap))
    return {
        "registry_sources": [base["registry_id"], ext["registry_id"]],
        "primitives": list(base.get("primitives") or []) + list(ext.get("primitives") or []),
    }


def compile_readiness(chapter_plan: dict[str, Any], primitive_registry: dict[str, Any], policy: dict[str, Any]):
    if policy.get("topic_id") != "PHY-M2D":
        raise AssertionError("M2D_RENDER_POLICY_TOPIC_DRIFT")
    rules = policy.get("rules") or {}
    required_rules = [
        "exact_concept_coverage_required",
        "name_similarity_authorization_forbidden",
        "schematic_fallback_does_not_satisfy_missing_cognitive_job",
        "ready_requires_at_least_one_authorized_existing_primitive",
    ]
    if any(rules.get(k) is not True for k in required_rules):
        raise AssertionError("M2D_RENDER_POLICY_GUARD_DISABLED")

    chapter_concepts = {row["concept_id"]: row for row in chapter_plan.get("concepts") or []}
    requirements = {row["concept_id"]: row for row in policy.get("requirements") or []}
    if len(requirements) != len(policy.get("requirements") or []):
        raise AssertionError("M2D_RENDER_DUPLICATE_POLICY_CONCEPT")
    if set(chapter_concepts) != set(requirements):
        missing = sorted(set(chapter_concepts) - set(requirements))
        extra = sorted(set(requirements) - set(chapter_concepts))
        raise AssertionError("M2D_RENDER_POLICY_CONCEPT_COVERAGE_DRIFT:missing=%s;extra=%s" % (",".join(missing), ",".join(extra)))

    primitives = {row["primitive_id"]: row for row in primitive_registry.get("primitives") or []}
    if len(primitives) != len(primitive_registry.get("primitives") or []):
        raise AssertionError("M2D_RENDER_DUPLICATE_PRIMITIVE_ID")

    concepts = []
    blocked = []
    for concept in chapter_plan["concepts"]:
        cid = concept["concept_id"]
        req = requirements[cid]
        actual_archetype = (concept.get("illustration") or {}).get("archetype")
        if req.get("illustration_archetype") != actual_archetype:
            raise AssertionError("M2D_RENDER_ARCHETYPE_DRIFT:" + cid)

        authorized = list(req.get("authorized_existing_primitive_refs") or [])
        missing_caps = list(req.get("missing_primitive_capabilities") or [])
        for primitive_id in authorized:
            if primitive_id not in primitives:
                raise AssertionError("M2D_RENDER_UNKNOWN_AUTHORIZED_PRIMITIVE:" + primitive_id)
            primitive = primitives[primitive_id]
            if primitive.get("decorative") is not False or primitive.get("realized_as_vector_graphics") is not True:
                raise AssertionError("M2D_RENDER_PRIMITIVE_NOT_INSTRUCTIONAL_VECTOR:" + primitive_id)
        if not missing_caps and not authorized:
            raise AssertionError("M2D_RENDER_REQUIREMENT_UNSATISFIED_WITHOUT_PRIMITIVE:" + cid)

        state = "BLOCKED_NEEDS_PRIMITIVE" if missing_caps else "READY_FOR_REALIZATION"
        if state == "BLOCKED_NEEDS_PRIMITIVE":
            blocked.append(cid)
        concepts.append({
            "concept_id": cid,
            "illustration_archetype": actual_archetype,
            "required_cognitive_jobs": list(req["required_cognitive_jobs"]),
            "authorized_existing_primitive_refs": authorized,
            "missing_primitive_capabilities": missing_caps,
            "state": state,
            "rationale": req["rationale"],
        })

    ready_count = len(concepts) - len(blocked)
    status = "BLOCKED_REPRESENTATION_GAP" if blocked else "READY_FOR_RENDER_ADAPTER"
    out = {
        "schema_version": "1.0.0",
        "readiness_id": "M2D-RENDER-READINESS-v1",
        "topic_id": "PHY-M2D",
        "chapter_plan_digest": chapter_plan["plan_digest"],
        "primitive_registry_digest": digest(primitive_registry),
        "requirements_policy_digest": digest(policy),
        "concepts": concepts,
        "summary": {
            "concept_count": len(concepts),
            "ready_count": ready_count,
            "blocked_count": len(blocked),
            "blocked_concept_ids": sorted(blocked),
            "status": status,
            "release_authorized": False,
        },
    }
    out["readiness_digest"] = digest(out)
    return out


def main():
    import argparse
    from jsonschema import Draft202012Validator

    ap = argparse.ArgumentParser(description="Compile real Motion-in-a-Plane representation readiness against the subject-wide Physics primitive registries.")
    ap.add_argument("--out", type=Path)
    args = ap.parse_args()

    chapter_plan = real_chapter_plan()
    primitive_registry = combined_primitive_registry()
    policy = load(ROOT / "policy" / "m2d-representation-requirements.v1.json")
    report = compile_readiness(chapter_plan, primitive_registry, policy)
    Draft202012Validator(load(ROOT / "contracts" / "m2d-render-readiness.schema.json")).validate(report)
    text = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
