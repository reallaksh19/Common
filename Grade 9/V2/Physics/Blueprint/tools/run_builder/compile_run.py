#!/usr/bin/env python3
"""Physics Blueprint Run Builder - Deterministic Run Compiler and Prompt Synthesizer.

Consumes a structured run configuration, resolves dependencies, validates governance
invariants (SDU difficulty isolation, LAU practice calibration, authority hierarchy),
and compiles a cold-start run manifest and execution prompt.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[4]
BLUEPRINT_ROOT = Path(__file__).resolve().parents[2]
GATES_PATH = BLUEPRINT_ROOT / "policy" / "physics-technical-engineering-gates.v1.json"


def canonical(val: Any) -> str:
    return json.dumps(val, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(val: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical(val).encode("utf-8")).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_gate_registry() -> dict[str, Any]:
    if GATES_PATH.exists():
        return load_json(GATES_PATH)
    return {"subtopic_gates": []}


def validate_config(config: dict[str, Any]) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []

    # 1. Required core fields
    if not config.get("subtopic_request") or not str(config["subtopic_request"]).strip():
        errors.append({"field": "subtopic_request", "code": "FIELD_REQUIRED", "message": "Subtopic request free-text is required."})

    grade = config.get("current_grade")
    if grade not in (9, 10, 11, "9", "10", "11"):
        errors.append({"field": "current_grade", "code": "INVALID_GRADE", "message": "Current grade must be 9, 10, or 11."})

    purpose = config.get("learning_purpose")
    valid_purposes = {"CBSE_EXAM", "COMPETITIVE_EXAM", "OLYMPIAD_FOUNDATION", "CONCEPT_REMEDIATION", "ACCELERATED_STUDY"}
    if purpose not in valid_purposes:
        errors.append({"field": "learning_purpose", "code": "INVALID_PURPOSE", "message": f"Learning purpose must be one of {sorted(valid_purposes)}."})

    depth = config.get("requested_engineering_depth", "STANDARD")
    if depth not in ("STANDARD", "RESEARCH"):
        errors.append({"field": "requested_engineering_depth", "code": "INVALID_DEPTH", "message": "Requested engineering depth must be STANDARD or RESEARCH."})

    # 2. SDU Invariant: Learner knowledge percent must NOT condition SDU difficulty
    core1_diff = config.get("core1_difficulty_control", "DERIVE")
    if core1_diff == "ADAPT_TO_LEARNER":
        errors.append({
            "field": "core1_difficulty_control",
            "code": "SDU_LEARNER_ADAPTATION_FORBIDDEN",
            "message": "Core1A/Core1B SDU depth must be governed by intrinsic physical difficulty, never adapted to learner knowledge percent."
        })

    # 3. LAU Invariant: Learner knowledge percentage requires named calibration policy or explicit owner waiver
    k_percent = config.get("learner_knowledge_percent")
    if k_percent is not None:
        if not (0 <= float(k_percent) <= 100):
            errors.append({"field": "learner_knowledge_percent", "code": "INVALID_PERCENTAGE", "message": "Learner knowledge percent must be between 0 and 100."})
        calib_ref = config.get("knowledge_calibration_policy_ref")
        waiver_id = config.get("owner_waiver_id")
        if not calib_ref and not waiver_id:
            errors.append({
                "field": "learner_knowledge_percent",
                "code": "UNBOUND_LAU_CALIBRATION",
                "message": "Conditioning practice on learner knowledge percent requires an explicit calibration policy reference or an Owner Waiver."
            })

    # 4. Exact Gate Selection (optional in config, validated if present)
    exact_gate = config.get("exact_gate_id")
    if exact_gate:
        registry = load_gate_registry()
        valid_gate_ids = {g["subtopic_id"] for g in registry.get("subtopic_gates", [])}
        if exact_gate not in valid_gate_ids:
            errors.append({"field": "exact_gate_id", "code": "UNKNOWN_ENGINEERING_GATE", "message": f"Exact gate ID '{exact_gate}' not found in Physics Gate Registry."})

    return errors


def resolve_dependencies(config: dict[str, Any]) -> dict[str, Any]:
    exact_gate = config.get("exact_gate_id")
    deps: dict[str, Any] = {
        "gate_registry_available": GATES_PATH.exists(),
        "exact_gate_id": exact_gate,
        "prerequisites_declared": [],
        "prerequisites_status": "UNRESOLVED" if not exact_gate else "RESOLVED",
        "representation_types_required": [],
        "mandatory_verifications": [],
    }

    if exact_gate and GATES_PATH.exists():
        registry = load_gate_registry()
        gate = next((g for g in registry.get("subtopic_gates", []) if g["subtopic_id"] == exact_gate), None)
        if gate:
            deps["prerequisites_declared"] = gate.get("prerequisite_ids", [])
            deps["representation_types_required"] = [r["representation_type"] for r in gate.get("representations", [])]
            deps["mandatory_verifications"] = gate.get("mandatory_verifications", [])
            deps["cbse_ref"] = gate.get("cbse_ref")
            deps["jee_tier"] = gate.get("jee_tier")
            deps["provisional_difficulty"] = gate.get("difficulty_profile", {}).get("provisional_difficulty", "MEDIUM")

    return deps


def compile_manifest(config: dict[str, Any]) -> dict[str, Any]:
    errors = validate_config(config)
    deps = resolve_dependencies(config)

    manifest: dict[str, Any] = {
        "schema_version": "1.0.0",
        "manifest_class": "PHYSICS_RUN_MANIFEST",
        "generator": "PhysicsBlueprintRunBuilder/v1",
        "input_config_digest": digest(config),
        "request": {
            "subject": "PHYSICS",
            "subtopic_request": config.get("subtopic_request", ""),
            "current_grade": int(config.get("current_grade", 9)),
            "exact_gate_id": config.get("exact_gate_id"),
        },
        "target": {
            "learning_purpose": config.get("learning_purpose"),
            "target_program_or_exam": config.get("target_program_or_exam", "IIT_JEE"),
        },
        "engineering": {
            "requested_depth": config.get("requested_engineering_depth", "STANDARD"),
            "exact_gate_selected": config.get("exact_gate_id"),
            "exact_resolver_passed": bool(config.get("exact_gate_id")),
        },
        "core1_control": {
            "difficulty_control": config.get("core1_difficulty_control", "DERIVE"),
            "owner_difficulty_override": config.get("owner_difficulty_override") or None,
            "isolated_from_learner_percent": True,
        },
        "research": {
            "web_research_allowed": bool(config.get("web_research_allowed", True)),
            "pedagogy_research_mode": config.get("pedagogy_research_mode", "DEFAULT"),
        },
        "context": {
            "repository": config.get("repository", "reallaksh19/Common"),
            "branch_or_ref": config.get("branch_or_ref", "v2-physics-gates-gr9-11"),
            "run_mode": config.get("run_mode", "GENERATION"),
            "mutation_mode": config.get("mutation_mode", "READ_ONLY"),
            "local_question_bank_ref": config.get("local_question_bank_ref") or None,
            "owner_scope_notes": config.get("owner_scope_notes") or None,
        },
        "dependencies": deps,
        "validation": {
            "status": "VALID" if not errors else "INVALID",
            "error_count": len(errors),
            "errors": errors,
        },
    }
    manifest["manifest_digest"] = digest(manifest)
    return manifest


def compile_prompt(config: dict[str, Any]) -> str:
    manifest = compile_manifest(config)
    subtopic = config.get("subtopic_request", "")
    grade = config.get("current_grade", "N/A")
    target = config.get("target_program_or_exam", "Competitive Exam")
    purpose = config.get("learning_purpose", "COMPETITIVE_EXAM")
    k_mode = config.get("learner_knowledge_mode", "UNKNOWN")
    k_percent = config.get("learner_knowledge_percent")
    k_percent_str = f"{k_percent}%" if k_percent is not None else "N/A"
    depth = config.get("requested_engineering_depth", "STANDARD")
    web_res = "Allowed" if config.get("web_research_allowed", True) else "Prohibited"
    run_mode = config.get("run_mode", "GENERATION")

    prompt = f"""# AGENT RUN ASSIGNMENT: Physics V2 Learning Pipeline

## 0. Run Context and Inputs
- **Subject**: PHYSICS
- **Subtopic Request**: "{subtopic}" (NON-AUTHORITATIVE FREE-TEXT)
- **Target Program / Exam**: {target}
- **Current Grade**: {grade}
- **Learning Purpose**: {purpose}
- **Learner Knowledge Mode**: {k_mode} (Percent: {k_percent_str})
- **Requested Engineering Depth**: {depth}
- **Web Pedagogy Research**: {web_res}
- **Run Mode**: {run_mode}
- **Run Manifest Digest**: `{manifest['manifest_digest']}`

## 1. Cold-Start Requirement
Operate as a strict cold-start implementation agent.
Assume no conversational memory of previous gate IDs, topic mappings, or test results.
Rediscover all schemas, policies, and gate registries directly from current repository files.

## 2. Authority Hierarchy
Preserve exact authority boundaries:
1. Ground Truth / Source Evidence (Immutable)
2. Engineering Authority (Canonical Gate Registry: 43 subtopics across Grades 9–11)
3. Non-Authoritative Candidate Discovery (Broad, tolerant search)
4. Explicit Exact-ID Selection & Exact Authoritative Resolver
5. CDAU / SDU (Intrinsic study depth) & LAU (Learner-adapted practice)
6. Publication & Rendering

## 3. Invariants & Anti-Drift Guard
- **SDU Depth Invariant**: Core1A/Core1B depth is governed strictly by intrinsic physical difficulty (EASY, MEDIUM, HARD). SDU MUST NOT inspect or adapt to learner knowledge percentage.
- **LAU Practice Adaptation**: Core2A/Core2B question demand is conditioned on learner knowledge percentage only when bound to an explicit calibration policy and source reference, or under explicit Owner Waiver.
- **Discovery vs. Authorization**: Natural language matching, high semantic similarity, or Rank 1 candidate ranking NEVER grants Engineering authorization. Downstream work requires explicit selection of the exact gate identity.
- **Physical Model Consistency**: Energy accounting must distinguish general energy conservation ($\\Delta K + \\Delta U = W_{{\\text{{nc}}}}$) from unconditional mechanical energy conservation ($K + U = \\text{{const}}$). Mechanical energy conservation is strictly conditional upon $W_{{\\text{{nc}}}} = 0$.
- **No Topic Branches**: Generic orchestration code must not contain topic-specific branches or hardcoded physics formulas.

## 4. Required Execution Steps
1. Execute discovery for candidate gates matching "{subtopic}".
2. Explicitly select the exact Engineering Gate ID from `physics-technical-engineering-gates.v1.json`.
3. Validate gate against schema at depth `{depth}`.
4. Ensure explicit system boundary isolation, sign convention, coordinate frame, and model conditions are stated before equation application.
5. Compile Core1A/Core1B semantic reconstruction and Core2A/Core2B transfer specifications.
6. Verify release gate dispositions in Product Governance.

## 5. Known Input Uncertainty & Downstream Blockers
- **Subtopic Status**: Unresolved free-text request until exact Engineering Gate is confirmed.
- **Learner Calibration**: {"Calibration policy is bound." if config.get("knowledge_calibration_policy_ref") else "No calibration policy supplied; learner percentage cannot independently condition support."}
"""
    return prompt.strip()


def validate_all_fixtures(fixtures_dir: Path | None = None) -> list[dict[str, Any]]:
    fixtures_dir = fixtures_dir or (Path(__file__).parent / "fixtures")
    results = []
    if not fixtures_dir.exists():
        return results
    for path in sorted(fixtures_dir.glob("*.json")):
        try:
            config = json.loads(path.read_text(encoding="utf-8"))
            manifest = compile_manifest(config)
            status = manifest["validation"]["status"]
            error_count = manifest["validation"]["error_count"]
            results.append({
                "fixture": path.name,
                "status": status,
                "error_count": error_count,
                "digest": manifest.get("manifest_digest"),
                "errors": manifest["validation"]["errors"],
            })
        except Exception as e:
            results.append({
                "fixture": path.name,
                "status": "ERROR",
                "error_count": 1,
                "message": str(e),
                "errors": [{"field": "file", "code": "JSON_PARSE_OR_RUNTIME_ERROR", "message": str(e)}],
            })
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Physics Blueprint Run Builder CLI Compiler")
    parser.add_argument("--config", help="Path to input configuration JSON")
    parser.add_argument("--out-manifest", help="Path to write compiled run manifest JSON")
    parser.add_argument("--out-prompt", help="Path to write compiled agent prompt markdown")
    parser.add_argument("--validate-fixtures", action="store_true", help="Validate all fixtures in fixtures/")
    args = parser.parse_args()

    if args.validate_fixtures:
        results = validate_all_fixtures()
        all_valid = all(r["status"] == "VALID" for r in results)
        print(f"Validated {len(results)} fixtures in tools/run_builder/fixtures/:")
        for r in results:
            print(f"  [{r['status']}] {r['fixture']} (digest: {str(r.get('digest', 'N/A'))[:20]}...)")
        if not all_valid:
            raise SystemExit("Fixture validation FAILED: some fixtures are invalid.")
        print("All fixtures are VALID.")
        return

    if not args.config:
        parser.error("--config is required when not running --validate-fixtures")

    config = json.loads(Path(args.config).read_text(encoding="utf-8"))
    manifest = compile_manifest(config)
    prompt = compile_prompt(config)

    if args.out_manifest:
        out_p = Path(args.out_manifest)
        out_p.parent.mkdir(parents=True, exist_ok=True)
        out_p.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"Manifest written to {args.out_manifest}")

    if args.out_prompt:
        out_pr = Path(args.out_prompt)
        out_pr.parent.mkdir(parents=True, exist_ok=True)
        out_pr.write_text(prompt + "\n", encoding="utf-8")
        print(f"Prompt written to {args.out_prompt}")

    print(f"Compilation Status: {manifest['validation']['status']}")
    print(f"Manifest Digest: {manifest['manifest_digest']}")
    if manifest['validation']['errors']:
        print("Validation Diagnostics:")
        for err in manifest['validation']['errors']:
            print(f"  [{err['code']}] {err['field']}: {err['message']}")


if __name__ == "__main__":
    main()
