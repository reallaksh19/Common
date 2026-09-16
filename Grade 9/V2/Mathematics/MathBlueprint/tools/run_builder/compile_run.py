#!/usr/bin/env python3
"""MathBlueprint Run Builder - Configuration Compiler.

Translates human run configuration into:
1. A complete agent assignment prompt.
2. A machine-readable run manifest.
3. Live validation diagnostics explaining missing/invalid inputs and educational rationale.
4. Dependency visibility showing unresolved downstream decisions.

Strictly preserves topic independence: zero hard-coded topic branches or invented percentage rules.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

VALID_PURPOSES = {"FIRST_STUDY", "CONSOLIDATION", "REVISION", "COMPETITIVE_EXAM"}
VALID_DEPTHS = {"FOUNDATION", "STANDARD", "RESEARCH"}
VALID_RUN_MODES = {"STRESS_TEST", "GENERATION", "LIBRARY_AUDIT", "RESEARCH_AUDIT"}
VALID_MUTATION_MODES = {"READ_ONLY", "TEST_MUTATIONS_ALLOWED"}
VALID_DIFFICULTIES = {"EASY", "MEDIUM", "HARD"}


def digest(data: Any) -> str:
    serialized = json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return "sha256:" + hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def validate_run_configuration(config: dict[str, Any]) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []

    # Subject validation
    subject = config.get("subject")
    if not subject:
        errors.append({
            "code": "MISSING_REQUIRED_INPUT",
            "field": "subject",
            "message": "Subject is required. The Mathematics Blueprint only authorizes MATHEMATICS runs.",
        })
    elif subject != "MATHEMATICS":
        errors.append({
            "code": "INVALID_COMBINATION",
            "field": "subject",
            "message": f"Unsupported subject '{subject}'. This blueprint instance is strictly bounded to MATHEMATICS.",
        })

    # Subtopic validation
    subtopic = config.get("subtopic_request", "").strip()
    if not subtopic:
        errors.append({
            "code": "MISSING_REQUIRED_INPUT",
            "field": "subtopic_request",
            "message": "Subtopic request is required. A run must have a focus area for candidate discovery and authoring.",
        })

    # Grade validation
    grade = config.get("current_grade")
    if grade is None:
        errors.append({
            "code": "MISSING_REQUIRED_INPUT",
            "field": "current_grade",
            "message": "Current grade is required to determine learner baseline expectations and curriculum level.",
        })
    elif not isinstance(grade, int) or grade < 1 or grade > 12:
        errors.append({
            "code": "INVALID_COMBINATION",
            "field": "current_grade",
            "message": f"Invalid grade {grade}. Must be an integer between 1 and 12.",
        })

    # Purpose validation
    purpose = config.get("learning_purpose")
    if not purpose:
        errors.append({
            "code": "MISSING_REQUIRED_INPUT",
            "field": "learning_purpose",
            "message": "Learning purpose is required (e.g. FIRST_STUDY, COMPETITIVE_EXAM).",
        })
    elif purpose not in VALID_PURPOSES:
        errors.append({
            "code": "UNKNOWN_POLICY",
            "field": "learning_purpose",
            "message": f"Unknown learning purpose '{purpose}'. Must be one of: {sorted(VALID_PURPOSES)}.",
        })

    # Learner knowledge validation
    k_mode = config.get("learner_knowledge_mode", "UNKNOWN")
    if k_mode == "KNOWN_PERCENT":
        k_percent = config.get("learner_knowledge_percent")
        if k_percent is None:
            errors.append({
                "code": "MISSING_REQUIRED_INPUT",
                "field": "learner_knowledge_percent",
                "message": "Learner knowledge percent is required when knowledge mode is KNOWN_PERCENT.",
            })
        elif not (isinstance(k_percent, (int, float)) and 0 <= k_percent <= 100):
            errors.append({
                "code": "INVALID_COMBINATION",
                "field": "learner_knowledge_percent",
                "message": f"Learner knowledge percentage {k_percent} is out of bounds (must be 0..100).",
            })

        k_source = config.get("knowledge_source_ref", "").strip()
        if not k_source:
            errors.append({
                "code": "MISSING_REQUIRED_INPUT",
                "field": "knowledge_source_ref",
                "message": "Knowledge source reference is required when percentage is supplied. Unattributed percentages are non-authoritative.",
            })

        k_policy = config.get("knowledge_calibration_policy_ref", "").strip()
        if not k_policy:
            errors.append({
                "code": "MISSING_REQUIRED_INPUT",
                "field": "knowledge_calibration_policy_ref",
                "message": "Learner knowledge percentage is present, but no calibration-policy reference has been supplied. The percentage does not independently determine learner support.",
            })
    elif k_mode == "UNKNOWN":
        if config.get("learner_knowledge_percent") is not None:
            errors.append({
                "code": "INVALID_COMBINATION",
                "field": "learner_knowledge_percent",
                "message": "Learner knowledge percentage cannot be populated when knowledge mode is declared UNKNOWN.",
            })
    else:
        errors.append({
            "code": "UNKNOWN_POLICY",
            "field": "learner_knowledge_mode",
            "message": f"Unknown learner knowledge mode '{k_mode}'. Must be KNOWN_PERCENT or UNKNOWN.",
        })

    # Engineering depth validation
    depth = config.get("requested_engineering_depth")
    if not depth:
        errors.append({
            "code": "MISSING_REQUIRED_INPUT",
            "field": "requested_engineering_depth",
            "message": "Engineering depth is required (FOUNDATION, STANDARD, or RESEARCH).",
        })
    elif depth not in VALID_DEPTHS:
        errors.append({
            "code": "UNKNOWN_POLICY",
            "field": "requested_engineering_depth",
            "message": f"Unknown engineering depth '{depth}'. Must be one of: {sorted(VALID_DEPTHS)}.",
        })

    # Core1 difficulty control validation
    diff_ctrl = config.get("core1_difficulty_control", "DERIVE")
    if diff_ctrl == "OWNER_OVERRIDE":
        override = config.get("owner_difficulty_override")
        if not override:
            errors.append({
                "code": "OWNER_DECISION_REQUIRED",
                "field": "owner_difficulty_override",
                "message": "Owner difficulty override is selected, but no difficulty badge (EASY, MEDIUM, HARD) was supplied.",
            })
        elif override not in VALID_DIFFICULTIES:
            errors.append({
                "code": "UNKNOWN_POLICY",
                "field": "owner_difficulty_override",
                "message": f"Unknown difficulty badge '{override}'. Must be one of: {sorted(VALID_DIFFICULTIES)}.",
            })

    # Run mode validation
    run_mode = config.get("run_mode", "GENERATION")
    if run_mode not in VALID_RUN_MODES:
        errors.append({
            "code": "UNKNOWN_POLICY",
            "field": "run_mode",
            "message": f"Unknown run mode '{run_mode}'. Must be one of: {sorted(VALID_RUN_MODES)}.",
        })

    # Mutation mode validation
    mut_mode = config.get("mutation_mode", "READ_ONLY")
    if mut_mode not in VALID_MUTATION_MODES:
        errors.append({
            "code": "UNKNOWN_POLICY",
            "field": "mutation_mode",
            "message": f"Unknown mutation mode '{mut_mode}'. Must be one of: {sorted(VALID_MUTATION_MODES)}.",
        })

    return errors


def compute_dependencies(config: dict[str, Any], errors: list[dict[str, str]]) -> dict[str, Any]:
    subtopic = config.get("subtopic_request", "")
    k_mode = config.get("learner_knowledge_mode", "UNKNOWN")
    k_percent = config.get("learner_knowledge_percent")
    k_policy = config.get("knowledge_calibration_policy_ref", "")

    return {
        "subtopic_resolution": {
            "status": "UNRESOLVED",
            "current_state": "NON_AUTHORITATIVE_FREE_TEXT",
            "input_text": subtopic,
            "next_required_step": "EXPLICIT_EXACT_ENGINEERING_GATE_SELECTION",
        },
        "engineering_authorization": {
            "status": "BLOCKED" if not subtopic else "READY_FOR_DISCOVERY",
            "exact_gate_id": None,
            "authority_state": "NOT_EVALUATED",
        },
        "learner_adaptation_status": {
            "mode": k_mode,
            "percentage": k_percent,
            "calibration_policy": k_policy or "MISSING",
            "support_conditioned": bool(k_mode == "KNOWN_PERCENT" and k_percent is not None and k_policy),
        },
        "study_differentiation_status": {
            "rule": "SDU_GOVERNED_BY_INTRINSIC_DIFFICULTY_ONLY",
            "learner_percentage_isolated": True,
            "control_basis": config.get("core1_difficulty_control", "DERIVE"),
        },
        "overall_run_status": "VALID_CONFIGURATION" if not errors else "CONFIGURATION_INCOMPLETE",
    }


def compile_manifest(config: dict[str, Any]) -> dict[str, Any]:
    errors = validate_run_configuration(config)
    deps = compute_dependencies(config, errors)

    manifest = {
        "schema_version": "1.0.0",
        "subject": config.get("subject", "MATHEMATICS"),
        "subtopic_request": config.get("subtopic_request", ""),
        "subtopic_authority_state": "NON_AUTHORITATIVE_FREE_TEXT",
        "learner": {
            "current_grade": config.get("current_grade"),
            "knowledge_mode": config.get("learner_knowledge_mode", "UNKNOWN"),
            "knowledge_percent": config.get("learner_knowledge_percent"),
            "knowledge_source_ref": config.get("knowledge_source_ref") or None,
            "calibration_policy_ref": config.get("knowledge_calibration_policy_ref") or None,
        },
        "target": {
            "learning_purpose": config.get("learning_purpose"),
            "target_program_or_exam": config.get("target_program_or_exam", "IIT_JEE"),
        },
        "engineering": {
            "requested_depth": config.get("requested_engineering_depth"),
            "exact_gate_selected": None,
            "exact_resolver_passed": False,
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
            "branch_or_ref": config.get("branch_or_ref", "v2-math-core1a-textbook-quality"),
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

    prompt = f"""# AGENT RUN ASSIGNMENT: Mathematics V2 Learning Pipeline

## 0. Run Context and Inputs
- **Subject**: MATHEMATICS
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
2. Engineering Authority (Canonical Gate Registry)
3. Non-Authoritative Candidate Discovery (Broad, tolerant search)
4. Explicit Exact-ID Selection & Exact Authoritative Resolver
5. CDAU / SDU (Intrinsic study depth) & LAU (Learner-adapted practice)
6. Publication & Rendering

## 3. Invariants & Anti-Drift Guard
- **SDU Depth Invariant**: Core1A/Core1B depth is governed by intrinsic mathematical difficulty (EASY, MEDIUM, HARD). SDU MUST NOT inspect or adapt to learner knowledge percentage.
- **LAU Practice Adaptation**: Core2A/Core2B question demand is conditioned on learner knowledge percentage only when bound to an explicit calibration policy and source reference, or under explicit Owner Waiver.
- **Discovery vs. Authorization**: Natural language matching, high semantic similarity, or Rank 1 candidate ranking NEVER grants Engineering authorization. Downstream work requires explicit selection of the exact gate identity.
- **No Topic Branches**: Generic orchestration code must not contain topic-specific branches or hardcoded mathematical formulas.

## 4. Required Execution Steps
1. Execute discovery for candidate gates matching "{subtopic}".
2. Explicitly select the exact Engineering Gate ID.
3. Validate gate against `mathematics-technical-engineering-gates.v1.json` at depth `{depth}`.
4. If research is enabled, ensure claim-level coverage, evidence stance classification, and contradiction resolution.
5. Compile Core1A/Core1B and Core2A/Core2B generation specifications.
6. Verify release gate dispositions in Product Governance.

## 5. Known Input Uncertainty & Downstream Blockers
- **Subtopic Status**: Unresolved free-text request until exact Engineering Gate is confirmed.
- **Learner Calibration**: {"Calibration policy is bound." if config.get("knowledge_calibration_policy_ref") else "No calibration policy supplied; learner percentage cannot independently condition support."}
"""
    return prompt.strip()


def validate_all_fixtures(fixtures_dir: Path | None = None) -> list[dict[str, Any]]:
    fixtures_dir = fixtures_dir or (Path(__file__).parent / "fixtures")
    results = []
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
            })
        except Exception as e:
            results.append({
                "fixture": path.name,
                "status": "ERROR",
                "error_count": 1,
                "message": str(e),
            })
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="MathBlueprint Run Builder CLI Compiler")
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
            print(f"  [{r['status']}] {r['fixture']} (digest: {r.get('digest', 'N/A')[:20]}...)")
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
        Path(args.out_manifest).write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"Manifest written to {args.out_manifest}")

    if args.out_prompt:
        Path(args.out_prompt).write_text(prompt + "\n", encoding="utf-8")
        print(f"Prompt written to {args.out_prompt}")

    print(f"Compilation Status: {manifest['validation']['status']}")
    print(f"Manifest Digest: {manifest['manifest_digest']}")
    if manifest['validation']['errors']:
        print("Validation Diagnostics:")
        for err in manifest['validation']['errors']:
            print(f"  [{err['code']}] {err['field']}: {err['message']}")


if __name__ == "__main__":
    main()
