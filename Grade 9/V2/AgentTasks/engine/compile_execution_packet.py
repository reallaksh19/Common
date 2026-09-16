#!/usr/bin/env python3
"""
Standalone Execution Packet Compiler.

Deterministically compiles human task intent + resolved repository authority
into a self-contained, reproducible StandaloneExecutionPacket (.json or .md entrypoint)
bearing an immutable SHA-256 custody digest.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError as SchemaValidationError

# Local imports
SCRIPT_DIR = Path(__file__).resolve().parent
AGENT_TASKS_DIR = SCRIPT_DIR.parent
CONTRACTS_DIR = AGENT_TASKS_DIR / "contracts"
REGISTRY_DIR = AGENT_TASKS_DIR / "registry"

sys.path.insert(0, str(SCRIPT_DIR))
from resolve_execution_authority import (  # noqa: E402
    find_repository_root,
    get_git_head_and_base,
    resolve_authorities,
    load_json,
)


class PacketCompilationError(Exception):
    """Structured compilation error."""
    pass


def validate_schema(data: dict, schema_path: Path) -> None:
    schema = load_json(schema_path)
    validator = Draft202012Validator(schema)
    errors = list(validator.iter_errors(data))
    if errors:
        msg = "\n".join(f"- {e.json_path}: {e.message}" for e in errors)
        raise PacketCompilationError(f"Schema validation failed against {schema_path.name}:\n{msg}")


def compute_canonical_digest(packet_dict: Dict[str, Any]) -> str:
    """Compute deterministic SHA-256 digest of packet excluding compiled_packet_digest."""
    data = {k: v for k, v in packet_dict.items() if k != "compiled_packet_digest"}
    canonical_json = json.dumps(data, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical_json.encode("utf-8")).hexdigest()


def compile_packet(
    task_input: Dict[str, Any],
    repo_root: Optional[Path] = None,
    override_head: Optional[str] = None,
    override_base: Optional[str] = None
) -> Dict[str, Any]:
    """Compile task into a validated StandaloneExecutionPacket."""
    root = repo_root or find_repository_root()

    # 1. Validate task input schema
    task_schema_path = CONTRACTS_DIR / "execution-task.schema.json"
    validate_schema(task_input, task_schema_path)

    # 2. Resolve target repository and git state
    target_ref = task_input.get("target_ref", "DISCOVER_CURRENT")
    git_head, git_base = get_git_head_and_base(root, target_ref="main")
    if override_head:
        git_head = override_head
    if override_base:
        git_base = override_base

    resolved_repo = {
        "repository": task_input.get("repository", "reallaksh19/Common"),
        "target_ref": target_ref,
        "resolved_head": git_head,
        "resolved_base": git_base
    }

    # 3. Resolve authorities
    subject = task_input["subject"]
    authority_bindings = resolve_authorities(subject, repo_root=root)

    # 4. Resolve task-kind contract from registry
    task_kind_registry = load_json(REGISTRY_DIR / "task-kind-registry.json")
    task_kinds = task_kind_registry.get("task_kinds", {})
    task_kind_name = task_input["task_kind"]
    if task_kind_name not in task_kinds:
        raise PacketCompilationError(f"Unknown task_kind '{task_kind_name}' in task-kind-registry.json")

    task_kind_def = task_kinds[task_kind_name]
    task_kind_contract = {
        "task_kind": task_kind_name,
        "required_authority_classes": task_kind_def["required_authority_classes"],
        "allowed_change_classes": task_kind_def["allowed_change_classes"],
        "required_outputs": task_kind_def["required_outputs"],
        "required_validators": task_kind_def["required_validators"],
        "consumer_targets": task_kind_def["consumer_targets"],
        "promotion_permitted": task_kind_def["promotion_permitted"]
    }

    # 5. Build research policy
    research_policy = {
        "web_research_allowed": task_input.get("web_research_allowed", False),
        "discovery_dispositions": [
            "REUSE_EXISTING",
            "EXTEND_EXISTING",
            "CREATE_CHILD",
            "CREATE_NEW",
            "CURRICULUM_ONLY",
            "PEDAGOGY_ONLY",
            "ASSESSMENT_ONLY",
            "RESEARCH_OVERLAY_ONLY",
            "OUT_OF_SCOPE",
            "CONFLICTING",
            "UNRESOLVED"
        ],
        "promotion_rule": "DISCOVERY_PERMISSION_DOES_NOT_IMPLY_PROMOTION_PERMISSION",
        "source_governance_ref": "Grade 9/V2/Physics/AssessmentIntake/contracts/assessment-source-provenance.schema.json"
    }

    # 6. Prohibited actions
    prohibited_actions = [
        "BLUEPRINT_CASE_BRANCH",
        "MANUAL_READINESS_ASSERTION",
        "SAME_ID_MUTATION",
        "UNOWNED_EXTERNAL_PREREQUISITE_CERTIFICATION",
        "SILENT_RESEARCH_BASE_MUTATION",
        "UNATTRIBUTED_SOURCE_PROMOTION"
    ]

    packet_id = f"PKT-{task_input['task_id']}"
    report_contract_ref = "Grade 9/V2/AgentTasks/contracts/execution-report.schema.json"

    # Assemble packet dictionary
    packet = {
        "schema_version": "1.0.0",
        "packet_id": packet_id,
        "task": task_input,
        "resolved_repository": resolved_repo,
        "authority_bindings": authority_bindings,
        "task_kind_contract": task_kind_contract,
        "research_policy": research_policy,
        "allowed_change_classes": task_kind_def["allowed_change_classes"],
        "prohibited_actions": prohibited_actions,
        "required_outputs": task_kind_def["required_outputs"],
        "required_validators": task_kind_def["required_validators"],
        "required_tests": [
            "python -m unittest Grade 9/V2/AgentTasks/tests/test_execution_kernel.py"
        ],
        "consumer_targets": task_input.get("target_consumers", task_kind_def["consumer_targets"]),
        "report_contract_ref": report_contract_ref,
        "compiled_packet_digest": ""  # Calculated below
    }

    # 7. Compute deterministic custody digest
    digest = compute_canonical_digest(packet)
    packet["compiled_packet_digest"] = digest

    # 8. Validate against execution-packet schema
    packet_schema_path = CONTRACTS_DIR / "execution-packet.schema.json"
    validate_schema(packet, packet_schema_path)

    return packet


def format_markdown_entrypoint(packet: Dict[str, Any]) -> str:
    """Wrap execution packet into a clean Markdown entrypoint for agents."""
    t = packet["task"]
    repo = packet["resolved_repository"]
    return f"""# STANDALONE EXECUTION PACKET: {packet['packet_id']}

**Packet Digest (SHA-256):** `{packet['compiled_packet_digest']}`
**Target Repository:** `{repo['repository']}`
**Resolved HEAD:** `{repo['resolved_head']}`
**Resolved Base:** `{repo['resolved_base']}`

---

## 1. Task Mission
- **Task Kind:** `{t['task_kind']}`
- **Subject:** `{t['subject']}`
- **Topic:** `{t['topic']}`
- **Subtopic:** `{t['subtopic']}`
- **Engineering Depth:** `{t['engineering_depth']}`
- **Learner State:** `{t['learner_state']}`
- **Web Research Allowed:** `{t['web_research_allowed']}`
- **Write Mode:** `{t['write_mode']}`
- **Target Consumers:** {', '.join(f'`{c}`' for c in packet['consumer_targets'])}

---

## 2. Bound Repository Authorities
Each authority below was bound at compile-time and stamped with its exact SHA-256 digest:
{chr(10).join(f"- **{b['authority_class']}**: `{b['ref_path']}` (`{b['digest_sha256'][:16]}...`)" for b in packet['authority_bindings'])}

---

## 3. Cold-Start Agent Discovery Protocol
Before editing any file, you must:
1. Verify packet digest matches `{packet['compiled_packet_digest']}`.
2. Confirm repository identity is `{repo['repository']}`.
3. Confirm repository HEAD is `{repo['resolved_head']}` or reconcile drift.
4. Read all bound authority artifacts listed in section 2.
5. Generate the non-authoritative **Engineering Preflight** to inspect current scope state.
6. Verify whether external prerequisites exist and who owns them.

---

## 4. Invariants & Prohibited Actions
- **Maximum flexibility in discovery and content; minimum flexibility in authority and promotion.**
- **No Blueprint case branch**: A new subtopic must not introduce `if topic == ...` in Blueprint or global orchestration.
- **Derived readiness**: Technical readiness comes strictly from running validators; manual assertion in data is forbidden.
- **Learner state invariance**: Changing learner state conditions pedagogy; it strictly never changes physical/mathematical domain truth.
- **Research depth non-mutation**: At RESEARCH depth, base claims cannot be silently mutated without explicit supersession.
- **Prohibited actions**: {', '.join(f'`{a}`' for a in packet['prohibited_actions'])}.

---

## 5. Required Deliverables & Report
- **Required Outputs:** {', '.join(f'`{o}`' for o in packet['required_outputs'])}
- **Required Validators:** {', '.join(f'`{v}`' for v in packet['required_validators']) if packet['required_validators'] else 'None'}
- Return your findings in a JSON report conforming to `{packet['report_contract_ref']}`.

---

## 6. Machine Packet Payload
```json
{json.dumps(packet, indent=2)}
```
"""


def main():
    parser = argparse.ArgumentParser(description="Compile execution packet")
    parser.add_argument("--task-file", required=True, type=Path, help="Path to input task JSON")
    parser.add_argument("--output", required=True, type=Path, help="Output packet path (.json or .md)")
    parser.add_argument("--repo-root", type=Path, default=None, help="Repository root path")
    parser.add_argument("--override-head", type=str, default=None, help="Override git HEAD")
    parser.add_argument("--override-base", type=str, default=None, help="Override git base")

    args = parser.parse_args()
    task = load_json(args.task_file)
    packet = compile_packet(
        task,
        repo_root=args.repo_root,
        override_head=args.override_head,
        override_base=args.override_base
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    if args.output.suffix.lower() == ".md":
        content = format_markdown_entrypoint(packet)
        args.output.write_text(content, encoding="utf-8")
    else:
        args.output.write_text(json.dumps(packet, indent=2), encoding="utf-8")

    print(f"Compiled packet successfully: {args.output} (Digest: {packet['compiled_packet_digest'][:16]}...)")


if __name__ == "__main__":
    main()
