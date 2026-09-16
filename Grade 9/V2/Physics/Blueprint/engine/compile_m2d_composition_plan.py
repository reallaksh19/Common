#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def digest_without_field(value: dict[str, Any], field: str) -> str:
    clone = dict(value)
    clone.pop(field, None)
    return digest(clone)


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


readiness_compiler = _module("bp_m2d_readiness_for_composition", ROOT / "engine" / "compile_m2d_render_readiness.py")


def current_real_inputs():
    chapter = readiness_compiler.real_chapter_plan()
    primitives = readiness_compiler.combined_primitive_registry()
    rep_policy = load(ROOT / "policy" / "m2d-representation-requirements.v1.json")
    readiness = readiness_compiler.compile_readiness(chapter, primitives, rep_policy)
    return chapter, readiness


def _has_forbidden_token(value: Any, policy: dict[str, Any]) -> bool:
    text = canonical(value).upper()
    return any(str(token).upper() in text for token in policy["requirements"]["forbidden_provenance_tokens"])


def validate_release_binding(
    *,
    chapter_plan: dict[str, Any],
    stage_run: dict[str, Any],
    binding: dict[str, Any],
    policy: dict[str, Any],
) -> dict[str, Any]:
    req = policy["requirements"]
    if _has_forbidden_token(stage_run, policy) or _has_forbidden_token(binding, policy):
        raise AssertionError("M2D_MANUSCRIPT_PROCESS_FIXTURE_FORBIDDEN")
    if binding.get("provenance_class") != req["provenance_class"]:
        raise AssertionError("M2D_MANUSCRIPT_PROVENANCE_CLASS_INVALID")
    if binding.get("binding_digest") != digest_without_field(binding, "binding_digest"):
        raise AssertionError("M2D_MANUSCRIPT_BINDING_DIGEST_DRIFT")
    if stage_run.get("stage_run_digest") != digest_without_field(stage_run, "stage_run_digest"):
        raise AssertionError("M2D_MANUSCRIPT_STAGE_RUN_DIGEST_DRIFT")
    if stage_run.get("topic_id") != "PHY-M2D" or binding.get("topic_id") != "PHY-M2D":
        raise AssertionError("M2D_MANUSCRIPT_TOPIC_BINDING_DRIFT")
    if binding.get("stage_run_ref") != stage_run.get("run_id") or binding.get("stage_run_digest") != stage_run.get("stage_run_digest"):
        raise AssertionError("M2D_MANUSCRIPT_STAGE_RUN_BINDING_DRIFT")
    if binding.get("chapter_plan_digest") != chapter_plan.get("plan_digest"):
        raise AssertionError("M2D_MANUSCRIPT_CHAPTER_DIGEST_DRIFT")
    if stage_run.get("manuscript_gate") != req["manuscript_gate"] or stage_run.get("next_stage") != req["manuscript_next_stage"]:
        raise AssertionError("M2D_MANUSCRIPT_STAGE_NOT_RELEASED")
    if stage_run.get("unresolved_required_jump_count") != req["unresolved_required_jump_count"]:
        raise AssertionError("M2D_MANUSCRIPT_UNRESOLVED_JUMPS")
    stages = list(stage_run.get("stage_results") or [])
    if len(stages) != 12 or any(row.get("status") != "PASS" for row in stages):
        raise AssertionError("M2D_MANUSCRIPT_PRE_MANUSCRIPT_STAGES_INCOMPLETE")

    prefix = req["repository_ref_prefix"]
    stage_artifacts = sorted({ref for row in stages for ref in (row.get("artifact_refs") or []) if str(ref).startswith(prefix)})
    stage_evidence = sorted({ref for row in stages for ref in (row.get("evidence_refs") or []) if str(ref).startswith(prefix)})
    for row in stages:
        if not any(str(ref).startswith(prefix) for ref in (row.get("artifact_refs") or [])):
            raise AssertionError("M2D_MANUSCRIPT_STAGE_REPOSITORY_ARTIFACT_REQUIRED:" + row.get("stage", "UNKNOWN"))
        if not any(str(ref).startswith(prefix) for ref in (row.get("evidence_refs") or [])):
            raise AssertionError("M2D_MANUSCRIPT_STAGE_REPOSITORY_EVIDENCE_REQUIRED:" + row.get("stage", "UNKNOWN"))

    declared_artifacts = set(binding.get("repository_artifact_refs") or [])
    declared_evidence = set(binding.get("repository_evidence_refs") or [])
    if not set(stage_artifacts).issubset(declared_artifacts):
        raise AssertionError("M2D_MANUSCRIPT_ARTIFACT_CUSTODY_INCOMPLETE")
    if not set(stage_evidence).issubset(declared_evidence):
        raise AssertionError("M2D_MANUSCRIPT_EVIDENCE_CUSTODY_INCOMPLETE")

    return {
        "binding_id": binding["binding_id"],
        "stage_run_ref": stage_run["run_id"],
        "stage_run_digest": stage_run["stage_run_digest"],
        "provenance_class": binding["provenance_class"],
    }


def compile_composition_plan(
    chapter_plan: dict[str, Any],
    readiness: dict[str, Any],
    policy: dict[str, Any],
    *,
    stage_run: dict[str, Any] | None = None,
    release_binding: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if policy.get("topic_id") != "PHY-M2D":
        raise AssertionError("M2D_COMPOSITION_POLICY_TOPIC_DRIFT")
    rules = policy.get("authority_rules") or {}
    if rules.get("composition_plan_may_invoke_renderer_directly") is not False or rules.get("composition_plan_may_authorize_release") is not False:
        raise AssertionError("M2D_COMPOSITION_AUTHORITY_ESCALATION")
    if readiness.get("readiness_digest") != digest_without_field(readiness, "readiness_digest"):
        raise AssertionError("M2D_COMPOSITION_READINESS_DIGEST_DRIFT")
    if readiness.get("chapter_plan_digest") != chapter_plan.get("plan_digest"):
        raise AssertionError("M2D_COMPOSITION_CHAPTER_READINESS_DRIFT")
    if (stage_run is None) != (release_binding is None):
        raise AssertionError("M2D_MANUSCRIPT_RELEASE_PAIR_REQUIRED")

    readiness_by_concept = {row["concept_id"]: row for row in readiness.get("concepts") or []}
    chapter_ids = [row["concept_id"] for row in chapter_plan.get("concepts") or []]
    if set(chapter_ids) != set(readiness_by_concept) or len(chapter_ids) != len(set(chapter_ids)):
        raise AssertionError("M2D_COMPOSITION_CONCEPT_COVERAGE_DRIFT")

    sections = []
    for concept in chapter_plan["concepts"]:
        cid = concept["concept_id"]
        rep = readiness_by_concept[cid]
        refs = list(rep.get("authorized_existing_primitive_refs") or [])
        if rep.get("state") == "READY_FOR_REALIZATION" and not refs:
            raise AssertionError("M2D_COMPOSITION_READY_CONCEPT_WITHOUT_REPRESENTATION:" + cid)
        sections.append({
            "section_id": f"M2D-COMP-{int(concept['order']):02d}",
            "order": int(concept["order"]),
            "concept_id": cid,
            "learner_title": concept["title"],
            "semantic_ref": "C1A-M2D-CONCEPT:" + cid,
            "semantic_digest": digest(concept),
            "difficulty": concept["difficulty"],
            "source_group_refs": sorted(set(concept.get("source_group_ids") or [])),
            "equation_refs": sorted({row["equation_id"] for row in concept.get("equations") or []}),
            "core2_challenge_refs": sorted({row["challenge_id"] for row in concept.get("where_you_will_use_this") or []}),
            "illustration_archetype": (concept.get("illustration") or {}).get("archetype", ""),
            "authorized_representation_refs": sorted(set(refs)),
            "page_intent": "TEACH_REPRESENT_PRACTISE_TRANSFER",
        })

    manuscript_release = None
    manuscript_status = "ABSENT"
    if stage_run is not None:
        manuscript_release = validate_release_binding(
            chapter_plan=chapter_plan,
            stage_run=stage_run,
            binding=release_binding,
            policy=policy,
        )
        manuscript_status = "BOUND_REPOSITORY_PRODUCTION"

    rep_status = readiness["summary"]["status"]
    blocks: list[str] = []
    if rep_status != policy["requirements"]["representation_readiness_status"]:
        composition_status = "BLOCKED_REPRESENTATION_GAP"
        publication_gate = "BLOCKED"
        next_action = "CLOSE_REPRESENTATION_GAPS"
        blocks.append("REPRESENTATION_READINESS_NOT_CLOSED")
    elif manuscript_release is None:
        composition_status = "BLOCKED_UPSTREAM_MANUSCRIPT_RELEASE"
        publication_gate = "BLOCKED"
        next_action = "MIGRATE_REAL_CORE1A_STAGE_RELEASE"
        blocks.append("REAL_CORE1A_MANUSCRIPT_RELEASE_NOT_BOUND")
    else:
        composition_status = "READY_FOR_PUBLICATION_IR"
        publication_gate = "OPEN"
        next_action = "COMPILE_PUBLICATION_IR"

    out = {
        "schema_version":"1.0.0",
        "composition_plan_id":"M2D-COMPOSITION-PLAN-v1",
        "topic_id":"PHY-M2D",
        "chapter_plan_digest":chapter_plan["plan_digest"],
        "representation_readiness_digest":readiness["readiness_digest"],
        "manuscript_release":manuscript_release,
        "sections":sections,
        "summary":{
            "concept_count":len(chapter_plan["concepts"]),
            "mapped_concept_count":len(sections),
            "representation_status":rep_status,
            "manuscript_release_status":manuscript_status,
            "composition_status":composition_status,
            "publication_ir_gate":publication_gate,
            "renderer_invocation_allowed":False,
            "release_authorized":False,
            "block_reasons":blocks,
            "next_action":next_action,
        },
    }
    out["composition_plan_digest"] = digest(out)
    return out


def main():
    import argparse
    from jsonschema import Draft202012Validator

    ap = argparse.ArgumentParser(description="Compile the real Motion-in-a-Plane composition plan behind manuscript-release and representation gates.")
    ap.add_argument("--stage-run", type=Path)
    ap.add_argument("--release-binding", type=Path)
    ap.add_argument("--out", type=Path)
    args = ap.parse_args()

    if (args.stage_run is None) != (args.release_binding is None):
        raise SystemExit("--stage-run and --release-binding must be supplied together")
    chapter, readiness = current_real_inputs()
    policy = load(ROOT / "policy" / "m2d-composition-release.v1.json")
    stage_run = load(args.stage_run) if args.stage_run else None
    binding = load(args.release_binding) if args.release_binding else None
    if binding is not None:
        Draft202012Validator(load(ROOT / "contracts" / "m2d-manuscript-release-binding.schema.json")).validate(binding)
    out = compile_composition_plan(chapter, readiness, policy, stage_run=stage_run, release_binding=binding)
    Draft202012Validator(load(ROOT / "contracts" / "m2d-composition-plan.schema.json")).validate(out)
    text = json.dumps(out, indent=2, ensure_ascii=False) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
