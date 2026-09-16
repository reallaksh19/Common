#!/usr/bin/env python3
"""
Standalone Execution Prompt Compiler Engine.

Deterministically composes:
  task-request inputs
  + prompt template
  + repository-discovery invariant
  + anti-drift invariants
  + subject profile
  + completion report contract
  -> StandaloneExecutionPrompt (.md) stamped with SHA-256 digest.
"""

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    from jsonschema import Draft202012Validator
except ImportError:
    Draft202012Validator = None

ENGINE_DIR = Path(__file__).resolve().parent
AGENT_TASKS_DIR = ENGINE_DIR.parent
PHYSICS_DIR = AGENT_TASKS_DIR.parent
V2_DIR = PHYSICS_DIR.parent
GENERAL_DIR = V2_DIR / "General"

CONTRACTS_DIR = AGENT_TASKS_DIR / "contracts"
INVARIANTS_DIR = AGENT_TASKS_DIR / "invariants"
TEMPLATES_DIRS = [AGENT_TASKS_DIR / "templates", GENERAL_DIR / "templates"]
SUBJECT_PROFILES_DIRS = [AGENT_TASKS_DIR / "subject-profiles", GENERAL_DIR / "subject-profiles"]

LEAK_DETECTION_TARGETS = [
    "M2D-SBA-04",
    "Q14",
    "Relative Motion",
]


def load_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def validate_task_request(task: Dict[str, Any]) -> None:
    schema_path = CONTRACTS_DIR / "execution-task.schema.json"
    if not schema_path.exists():
        raise FileNotFoundError(f"Schema not found: {schema_path}")
    schema = load_json(schema_path)
    if Draft202012Validator is not None:
        validator = Draft202012Validator(schema)
        errors = list(validator.iter_errors(task))
        if errors:
            msg = "\n".join(f"- {e.json_path}: {e.message}" for e in errors)
            raise ValueError(f"Task request failed schema validation:\n{msg}")
    else:
        # Fallback basic type checks if jsonschema not available
        required = schema.get("required", [])
        for field in required:
            if field not in task:
                raise ValueError(f"Missing required field in task: {field}")


def locate_template(template_id: str) -> Path:
    for t_dir in TEMPLATES_DIRS:
        if not t_dir.exists():
            continue
        for p in t_dir.glob("*.md"):
            if p.name.startswith(template_id):
                return p
    raise FileNotFoundError(f"Template not found for ID: {template_id}")


def locate_subject_profile(subject: str) -> Dict[str, Any]:
    subj_lower = subject.lower()
    for s_dir in SUBJECT_PROFILES_DIRS:
        if not s_dir.exists():
            continue
        p = s_dir / f"{subj_lower}.json"
        if p.exists():
            return load_json(p)
    raise FileNotFoundError(f"Subject profile not found for: {subject}")


def format_inputs_block(task: Dict[str, Any]) -> str:
    lines = [
        "```yaml",
        f"PROMPT_ID: {task.get('prompt_id')}",
        f"PROMPT_TEMPLATE_ID: {task.get('prompt_template_id')}",
        f"PROMPT_TEMPLATE_VERSION: {task.get('prompt_template_version')}",
        f"TASK_INSTANCE_ID: {task.get('task_instance_id')}",
        "",
        f"REPOSITORY: {task.get('repository')}",
        f"TARGET_BRANCH: {task.get('target_branch')}",
        f"BASELINE_PR: {task.get('baseline_pr') if task.get('baseline_pr') is not None else 'null'}",
        "",
        f"SUBJECT: {task.get('subject')}",
        f"GRADE: {task.get('grade')}",
        f"CURRICULUM: {task.get('curriculum')}",
        f"CURRICULUM_VERSION: {task.get('curriculum_version')}",
        "",
        f"TOPIC: {task.get('topic')}",
        f"SUBTOPIC: {task.get('subtopic')}",
        "",
        f"ENGINEERING_DEPTH: {task.get('engineering_depth')}",
        f"LEARNER_STATE: {task.get('learner_state')}",
        "",
        f"WEB_RESEARCH_ALLOWED: {str(task.get('web_research_allowed')).lower()}",
        f"LOCAL_QUESTION_BANKS: {task.get('local_question_banks')}",
        "",
        f"WRITE_MODE: {task.get('write_mode')}",
    ]

    expected = task.get("expected_scope", [])
    if expected:
        lines.append("EXPECTED_SCOPE:")
        for item in expected:
            lines.append(f"  - {item}")
    else:
        lines.append("EXPECTED_SCOPE: []")

    exclusions = task.get("explicit_exclusions", [])
    if exclusions:
        lines.append("EXPLICIT_EXCLUSIONS:")
        for item in exclusions:
            lines.append(f"  - {item}")
    else:
        lines.append("EXPLICIT_EXCLUSIONS: []")

    lines.append("```")
    return "\n".join(lines)


def format_repository_authority(task: Dict[str, Any]) -> str:
    lines = [
        f"- Target Repository: `{task.get('repository')}`",
        f"- Target Branch: `{task.get('target_branch')}`",
        f"- Baseline PR: `{task.get('baseline_pr')}`" if task.get("baseline_pr") else "- Baseline PR: None (Independent run)",
        "- Governing Manifests: `AGENTS.md`, `README.md`, `contracts/`",
        "- All actions must be validated against repository HEAD.",
    ]
    return "\n".join(lines)


def format_subject_architecture(profile: Dict[str, Any]) -> str:
    lines = [
        f"### Subject Disciplinary Rules ({profile.get('subject')} v{profile.get('version')})",
        f"_{profile.get('description', '')}_",
        "",
        "**Epistemological Rules:**",
    ]
    for rule in profile.get("epistemological_rules", []):
        lines.append(f"- {rule}")

    lines.append("")
    lines.append("**Allowed Representations:**")
    for rep in profile.get("allowed_representations", []):
        lines.append(f"- `{rep}`")

    return "\n".join(lines)


def format_subject_falsifiers(profile: Dict[str, Any]) -> str:
    lines = [
        f"### Subject Mandatory Falsifiers ({profile.get('subject')})",
    ]
    for fal in profile.get("mandatory_falsifiers", []):
        lines.append(f"- `{fal}`")
    return "\n".join(lines)


def run_prompt_linter(
    prompt_text: str,
    task: Dict[str, Any],
    allow_case_leakage: bool = False
) -> List[str]:
    errors = []

    # 1. Verify all 17 required sections (0 through 16)
    expected_sections = [
        "## 0. Editable Inputs",
        "## 1. Mission",
        "## 2. Repository / Branch Authority",
        "## 3. Cold-Start Discovery",
        "## 4. Existing Architecture to Respect",
        "## 5. Task Scope",
        "## 6. Required Deliverables",
        "## 7. Allowed Changes",
        "## 8. Prohibited Changes",
        "## 9. Anti-Drift Invariants",
        "## 10. Research / Source Policy",
        "## 11. Implementation Procedure",
        "## 12. Mandatory Falsifiers",
        "## 13. Tests / CI",
        "## 14. Acceptance Criteria",
        "## 15. Stop / Block Conditions",
        "## 16. Exact Completion Report",
    ]
    for sec in expected_sections:
        if sec not in prompt_text:
            errors.append(f"Missing mandatory section header: '{sec}'")

    # 2. Check for unresolved template placeholders {{...}}
    unresolved = re.findall(r"\{\{([A-Z0-9_]+)\}\}", prompt_text)
    if unresolved:
        errors.append(f"Unresolved template placeholders detected: {set(unresolved)}")

    # 3. Check for BLOCKED outcome permission in Section 15
    if "BLOCKED" not in prompt_text:
        errors.append("Section 15 does not declare BLOCKED as a valid execution outcome.")

    # 4. Anti-coupling / leakage lint: generic body must not leak case literals unless passed in task inputs
    if not allow_case_leakage:
        # Separate section 0 from the rest of the prompt
        sec0_idx = prompt_text.find("## 0. Editable Inputs")
        sec1_idx = prompt_text.find("## 1. Mission")
        body_text = prompt_text[sec1_idx:] if sec1_idx != -1 else prompt_text

        for target in LEAK_DETECTION_TARGETS:
            # If target was explicitly passed in inputs (e.g. topic or subtopic), it is permitted
            input_values = [
                str(v) for v in [task.get("topic"), task.get("subtopic")] if v
            ] + task.get("expected_scope", [])
            is_input = any(target.lower() in iv.lower() for iv in input_values)
            if not is_input and target.lower() in body_text.lower():
                errors.append(
                    f"Coupling/Leakage error: Generic prompt body contains literal '{target}' "
                    "which was not declared in task inputs!"
                )

    return errors


def compile_prompt(task: Dict[str, Any], allow_case_leakage: bool = False) -> Tuple[str, str]:
    """
    Compiles a standalone execution prompt from task inputs.
    Returns: (compiled_prompt_text, sha256_digest)
    """
    validate_task_request(task)

    template_id = task["prompt_template_id"]
    template_path = locate_template(template_id)
    template_text = template_path.read_text(encoding="utf-8")

    # Load invariants
    discovery_text = (INVARIANTS_DIR / "repository-discovery.md").read_text(encoding="utf-8")
    anti_drift_text = (INVARIANTS_DIR / "anti-drift.md").read_text(encoding="utf-8")
    report_text = (INVARIANTS_DIR / "completion-report.md").read_text(encoding="utf-8")

    # Load subject profile
    subject = task["subject"]
    profile = locate_subject_profile(subject)

    # Prepare injected components
    inputs_block = format_inputs_block(task)
    repo_auth_block = format_repository_authority(task)
    subject_arch_block = format_subject_architecture(profile)
    subject_falsifiers_block = format_subject_falsifiers(profile)

    # Assemble prompt
    compiled = template_text
    compiled = compiled.replace("{{EDITABLE_INPUTS_BLOCK}}", inputs_block)
    compiled = compiled.replace("{{REPOSITORY_BRANCH_AUTHORITY}}", repo_auth_block)
    compiled = compiled.replace("{{COLD_START_DISCOVERY}}", discovery_text)
    compiled = compiled.replace("{{SUBJECT_ARCHITECTURE_GUIDELINES}}", subject_arch_block)
    compiled = compiled.replace("{{ANTI_DRIFT_INVARIANTS}}", anti_drift_text)
    compiled = compiled.replace("{{SUBJECT_MANDATORY_FALSIFIERS}}", subject_falsifiers_block)
    compiled = compiled.replace("{{COMPLETION_REPORT_CONTRACT}}", report_text)

    # Run linter
    lint_errors = run_prompt_linter(compiled, task, allow_case_leakage=allow_case_leakage)
    if lint_errors:
        err_msg = "\n".join(f"- {e}" for e in lint_errors)
        raise ValueError(f"Compiled prompt failed lint checks:\n{err_msg}")

    # Compute digest of preliminary text
    pre_digest = hashlib.sha256(compiled.encode("utf-8")).hexdigest()

    # Append provenance and metadata header/footer
    provenance_header = (
        f"<!-- COMPILED STANDALONE EXECUTION PROMPT -->\n"
        f"<!-- PROMPT_ID: {task.get('prompt_id')} -->\n"
        f"<!-- PROMPT_TEMPLATE_ID: {task.get('prompt_template_id')} -->\n"
        f"<!-- PROMPT_TEMPLATE_VERSION: {task.get('prompt_template_version')} -->\n"
        f"<!-- SUBJECT_PROFILE_VERSION: {profile.get('version')} -->\n"
        f"<!-- SCHEMA_REGISTRY_VERSION: 1.0.0 -->\n"
        f"<!-- COMPILED_PROMPT_DIGEST: {pre_digest} -->\n\n"
    )
    final_prompt = provenance_header + compiled

    # Final deterministic digest calculation
    final_digest = hashlib.sha256(final_prompt.encode("utf-8")).hexdigest()
    return final_prompt, final_digest


def main():
    parser = argparse.ArgumentParser(description="Compile a StandaloneExecutionPrompt (.md)")
    parser.add_argument("--task-file", type=Path, help="Path to execution task JSON file")
    parser.add_argument("--output", type=Path, help="Output .md file path (default: stdout)")
    parser.add_argument("--allow-case-leakage", action="store_true", help="Bypass anti-coupling linter")
    args = parser.parse_args()

    if not args.task_file:
        parser.print_help()
        sys.exit(1)

    task_data = load_json(args.task_file)
    try:
        compiled, digest = compile_prompt(task_data, allow_case_leakage=args.allow_case_leakage)
    except Exception as e:
        print(f"COMPILATION ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(compiled, encoding="utf-8")
        print(f"Prompt compiled successfully to: {args.output}")
        print(f"SHA-256 Digest: {digest}")
    else:
        print(compiled)


if __name__ == "__main__":
    main()
