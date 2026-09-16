#!/usr/bin/env python3
"""
Chemistry LearningBlueprint Run Builder CLI Compiler
===================================================
Translates run configuration into deterministic prompt manifests and execution manifests.
Enforces SDU/LAU isolation, exact gate validation, and non-authoritative discovery boundaries.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

VALID_SUBJECTS = {"CHEMISTRY"}
VALID_GRADES = {9, 10, 11}
VALID_PURPOSES = {"FOUNDATION", "CBSE_BOARD_EXAM", "COMPETITIVE_EXAM", "REMEDIAL", "ACCELERATED"}
VALID_KNOWLEDGE_MODES = {"UNKNOWN", "KNOWN_PERCENT", "DIAGNOSTIC_ASSESSMENT", "HISTORICAL_EVIDENCE"}
VALID_DEPTHS = {"MINIMAL", "STANDARD", "DEEP", "RESEARCH"}
VALID_SDU_CONTROLS = {"FIXED_INTRINSIC_DEPTH", "CANONICAL_DEFAULT"}
VALID_LAU_CONTROLS = {"DIAGNOSTIC_ADAPTIVE", "STANDARD_PRACTICE", "CHALLENGE_EXTENDED"}


def canonical(val: Any) -> str:
    return json.dumps(val, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(val: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical(val).encode("utf-8")).hexdigest()


def validate_config(config: dict[str, Any]) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []

    subtopic = config.get("subtopic_request", "").strip()
    if not subtopic:
        errors.append({"field": "subtopic_request", "code": "FIELD_REQUIRED", "message": "Subtopic request cannot be empty."})

    subj = config.get("subject", "CHEMISTRY")
    if subj not in VALID_SUBJECTS:
        errors.append({"field": "subject", "code": "INVALID_SUBJECT", "message": f"Subject must be one of {VALID_SUBJECTS}."})

    grade = config.get("current_grade")
    if grade not in VALID_GRADES:
        errors.append({"field": "current_grade", "code": "INVALID_GRADE", "message": f"Grade must be in {VALID_GRADES}."})

    purpose = config.get("learning_purpose")
    if purpose not in VALID_PURPOSES:
        errors.append({"field": "learning_purpose", "code": "INVALID_PURPOSE", "message": f"Purpose must be in {VALID_PURPOSES}."})

    k_mode = config.get("learner_knowledge_mode", "UNKNOWN")
    if k_mode not in VALID_KNOWLEDGE_MODES:
        errors.append({"field": "learner_knowledge_mode", "code": "INVALID_KNOWLEDGE_MODE", "message": f"Mode must be in {VALID_KNOWLEDGE_MODES}."})

    k_percent = config.get("learner_knowledge_percent")
    if k_mode == "KNOWN_PERCENT":
        if k_percent is None or not (0 <= k_percent <= 100):
            errors.append({"field": "learner_knowledge_percent", "code": "INVALID_PERCENT", "message": "Percentage must be in [0, 100]."})
        policy_ref = config.get("knowledge_calibration_policy_ref", "").strip()
        waiver_id = config.get("owner_waiver_id", "").strip()
        if not policy_ref and not waiver_id:
            errors.append({
                "field": "learner_knowledge_percent",
                "code": "MISSING_CALIBRATION_AUTHORITY",
                "message": "Conditioning practice on learner knowledge percent requires an explicit calibration policy or owner waiver.",
            })

    depth = config.get("requested_engineering_depth", "STANDARD")
    if depth not in VALID_DEPTHS:
        errors.append({"field": "requested_engineering_depth", "code": "INVALID_DEPTH", "message": f"Depth must be in {VALID_DEPTHS}."})

    sdu_ctrl = config.get("core1_difficulty_control", "FIXED_INTRINSIC_DEPTH")
    if sdu_ctrl not in VALID_SDU_CONTROLS:
        errors.append({
            "field": "core1_difficulty_control",
            "code": "SDU_LEARNER_ADAPTATION_FORBIDDEN",
            "message": "Core1 conceptual depth must be intrinsic and cannot adapt to learner percentages.",
        })

    return errors


def compile_manifest(config: dict[str, Any]) -> dict[str, Any]:
    errors = validate_config(config)
    exact_gate = config.get("exact_gate_id")

    deps = {
        "candidate_discovery_status": "DISCOVERED" if config.get("subtopic_request") else "PENDING",
        "exact_gate_selection_status": "EXPLICIT_SELECTION_MADE" if exact_gate else "PENDING_EXPLICIT_SELECTION",
        "prerequisites_status": "SATISFIED" if exact_gate else "UNRESOLVED",
    }

    manifest = {
        "schema_version": "1.0.0",
        "subject": "CHEMISTRY",
        "manifest_type": "CHEMISTRY_RUN_MANIFEST",
        "request": {
            "subtopic_request": config.get("subtopic_request", ""),
            "target_program_or_exam": config.get("target_program_or_exam", "General Curriculum"),
            "current_grade": config.get("current_grade", 10),
            "learning_purpose": config.get("learning_purpose", "CBSE_BOARD_EXAM"),
            "learner_knowledge_mode": config.get("learner_knowledge_mode", "UNKNOWN"),
            "learner_knowledge_percent": config.get("learner_knowledge_percent"),
        },
        "engineering": {
            "requested_depth": config.get("requested_engineering_depth", "STANDARD"),
            "exact_gate_selected": exact_gate,
            "exact_resolver_passed": bool(exact_gate),
            "core1_difficulty_control": config.get("core1_difficulty_control", "FIXED_INTRINSIC_DEPTH"),
            "core2_adaptation_mode": config.get("core2_adaptation_mode", "STANDARD_PRACTICE"),
        },
        "context": {
            "repository": config.get("repository", "reallaksh19/Common"),
            "branch_or_ref": config.get("branch_or_ref", "v2-chemistry-phase1-observability-workbench"),
            "run_mode": config.get("run_mode", "GENERATION"),
            "mutation_mode": config.get("mutation_mode", "READ_ONLY"),
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
    run_mode = config.get("run_mode", "GENERATION")

    prompt = f"""# AGENT RUN ASSIGNMENT: Chemistry V2 Learning Pipeline

## 0. Run Context and Inputs
- **Subject**: CHEMISTRY
- **Subtopic Request**: "{subtopic}" (NON-AUTHORITATIVE FREE-TEXT)
- **Target Program / Exam**: {target}
- **Current Grade**: {grade}
- **Learning Purpose**: {purpose}
- **Learner Knowledge Mode**: {k_mode} (Percent: {k_percent_str})
- **Requested Engineering Depth**: {depth}
- **Run Mode**: {run_mode}
- **Run Manifest Digest**: `{manifest['manifest_digest']}`

## 1. Authority Hierarchy
Preserve exact authority boundaries:
1. Ground Truth / Source Evidence (Immutable)
2. Engineering Authority (Canonical Gate Registry: 52 subtopics across Grades 9–11)
3. Non-Authoritative Candidate Discovery (Broad, tolerant search)
4. Explicit Exact-ID Selection & Exact Authoritative Resolver
5. CDAU / SDU (Intrinsic study depth) & LAU (Learner-adapted practice)
6. Publication & Rendering

## 2. Invariants & Anti-Drift Guard
- **SDU Depth Invariant**: Core1A/Core1B depth is governed strictly by intrinsic chemical difficulty. SDU MUST NOT inspect or adapt to learner knowledge percentage.
- **LAU Practice Adaptation**: Core2A/Core2B question demand is conditioned on learner knowledge percentage only when bound to an explicit calibration policy and source reference, or under explicit Owner Waiver.
- **Discovery vs. Authorization**: Natural language matching, high semantic similarity, or Rank 1 candidate ranking NEVER grants Engineering authorization.
- **Chemical Model Consistency**: State symbols (s, l, g, aq), mass conservation, electroneutrality, and thermodynamic reference states must be strictly preserved.
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
    parser = argparse.ArgumentParser(description="Chemistry Blueprint Run Builder CLI Compiler")
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


if __name__ == "__main__":
    main()
