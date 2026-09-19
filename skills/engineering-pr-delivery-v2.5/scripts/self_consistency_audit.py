#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import re
from typing import Iterable

import yaml


REQUIRED_BLUEPRINT_HEADINGS = [
    "## WHEN TO APPLY",
    "## REQUIRED INPUTS",
    "## PROCEDURE",
    "## BEST-PRACTICE CHECKLIST",
    "## ANTI-PATTERNS",
    "## REQUIRED ARTIFACTS",
    "## VERIFICATION",
    "## QUALITY FINDING CLASSIFICATION",
    "## TRUE HARD-STOP CONDITIONS",
    "## OWNER REPORT",
    "## SUCCESSOR HANDOVER",
]

OBJECT_SURFACES = {
    "EP": ["templates/EP.yaml", "schemas/execution-package.schema.yaml", "scripts/validate_ep_semantics.py", "operating-model/execution-package.md"],
    "CP": ["templates/CP.yaml", "schemas/checkpoint.schema.yaml", "scripts/validate_checkpoint_linkage.py", "operating-model/checkpoint.md"],
    "DISC": ["templates/DISCOVERY_RECEIPT.yaml", "schemas/discovery-receipt.schema.yaml", "scripts/validate_discovery_receipt.py", "scripts/validate_takeover_certification.py"],
    "QSET": ["templates/QUESTION_SET.yaml", "schemas/question-set.schema.yaml", "scripts/validate_question_set.py", "operating-model/phase-transition.md"],
    "QUAL": ["templates/QUALIFICATION_RECEIPT.yaml", "schemas/qualification-receipt.schema.yaml", "scripts/validate_qualification_receipt.py", "operating-model/phase-transition.md"],
    "TC": ["templates/TAKEOVER_CERTIFICATION.yaml", "schemas/takeover-certification.schema.yaml", "scripts/validate_takeover_certification.py", "operating-model/takeover-certification.md"],
    "QRV": ["templates/QUALITY_REVIEW.yaml", "schemas/quality-review.schema.yaml", "scripts/validate_quality_review.py", "operating-model/quality-procedures.md"],
    "ODR": ["templates/ODR.yaml", "schemas/owner-decision.schema.yaml", "scripts/validate_owner_decision.py", "operating-model/owner-change-intake.md"],
    "REPO_STATE": ["templates/REPO_STATE.yaml", "schemas/repo-state.schema.yaml", "scripts/validate_repo_state.py"],
    "REPO_PROFILE": ["templates/REPO_PROFILE.yaml", "schemas/repo-profile.schema.yaml", "scripts/validate_repo_profile.py"],
    "ROADMAP": ["templates/OVERALL_ROADMAP.yaml", "schemas/roadmap.schema.yaml", "scripts/validate_roadmap.py"],
    "PROGRESS": ["templates/PROGRESS.yaml", "schemas/progress.schema.yaml", "scripts/validate_progress.py", "operating-model/progress-accounting.md"],
    "ISSUE_GRAPH": ["templates/ISSUE_GRAPH.yaml", "schemas/issue-graph.schema.yaml", "scripts/validate_issue_graph.py", "operating-model/issue-projection.md"],
    "PARALLEL_PLAN": ["templates/PARALLEL_PLAN.yaml", "schemas/parallel-plan.schema.yaml", "scripts/validate_parallel_plan.py"],
    "PARALLEL_JOIN": ["templates/PARALLEL_JOIN.yaml", "schemas/parallel-join.schema.yaml", "scripts/validate_parallel_join.py"],
    "PARALLEL_REPLAN": ["templates/PARALLEL_REPLAN.yaml", "schemas/parallel-replan.schema.yaml", "scripts/validate_parallel_replan.py"],
    "REPORT_PROJECTION": ["schemas/report-projection.schema.yaml", "scripts/report_projection.py", "scripts/validate_report_projection.py"],
    "COMMUNICATION_PROJECTION": ["schemas/communication-projection.schema.yaml", "scripts/communication_projection.py", "scripts/validate_human_communication.py", "scripts/render_owner_status.py", "scripts/render_technical_status.py", "operating-model/human-communication.md"],
    "OWNER_CHANGE_PROJECTION": ["schemas/owner-change-projection.schema.yaml", "scripts/owner_change_projection.py", "scripts/validate_owner_change_intake.py", "scripts/render_owner_change.py", "operating-model/owner-change-intake.md"],
    "ZERO_CONTEXT_RECONSTRUCTION": ["schemas/zero-context-reconstruction.schema.yaml", "scripts/zero_context_reconstruction.py", "scripts/validate_zero_context_reconstruction.py", "operating-model/relay-certification-matrix.md"],
    "HANDOVER_PLAN": ["schemas/handover-plan.schema.yaml", "scripts/handover_planning.py", "scripts/validate_handover_plan.py", "scripts/plan_handover.py", "scripts/prepare_handover_projection.py", "operating-model/human-communication.md"],
    "ROADMAP_EVENTS": ["templates/ROADMAP_EVENTS.yaml", "schemas/roadmap-events.schema.yaml", "scripts/roadmap_events.py", "scripts/validate_roadmap_events.py", "scripts/append_roadmap_event.py", "operating-model/dynamic-roadmap.md"],
    "OWNER_PUBLICATION": ["templates/OWNER_PUBLICATION.yaml", "schemas/owner-publication.schema.yaml", "scripts/owner_publication.py", "scripts/validate_owner_publication.py", "scripts/publish_owner_progress.py", "operating-model/human-communication.md"],
    "DELIVERY_OBSERVATION": ["templates/DELIVERY_OBSERVATION.yaml", "schemas/delivery-observation.schema.yaml", "scripts/validate_delivery_observation.py", "scripts/delivery_projection.py", "blueprints/github-delivery.md"],
}

RELEASE_DOCS = {
    "operating-model/architecture-index.md": ["operator-quick-start.md", "synthetic-relay-example.md", "self_consistency_audit.py"],
    "operating-model/operator-quick-start.md": ["validate_relay_conformance.py", "material_write_ready.py", "plan_handover.py", "prior conversation"],
    "operating-model/synthetic-relay-example.md": ["DSTEP-01", "DISC-0002", "QUAL-0002", "TC-0002", "MATERIAL_WRITE_READY"],
}

AGGREGATE_REQUIRED_MODULES = [
    "validate_repo_state", "validate_repo_profile", "validate_roadmap", "validate_roadmap_events", "validate_execution_frontier",
    "validate_progress", "validate_report_projection", "validate_human_communication", "validate_owner_publication", "validate_delivery_observation", "validate_owner_change_intake",
    "validate_zero_context_reconstruction", "validate_serial_execution", "validate_parallel_plan", "validate_parallel_join",
    "validate_parallel_replan", "validate_roadmap_continuity", "validate_state_planes", "validate_projection_convergence",
    "validate_github_projection", "validate_github_generation_history", "validate_checkpoint_linkage", "validate_owner_decision",
    "validate_issue_graph", "validate_issue_projection_tree", "validate_issue_closure", "validate_supersession",
    "validate_roadmap_transaction", "validate_question_set", "validate_qualification_receipt", "validate_takeover_certification",
    "validate_blueprints", "validate_quality_router", "validate_quality_review", "validate_baton_readiness",
]

README_REQUIRED_ENTRYPOINTS = [
    "validate_relay_conformance.py", "cold_start_check.py", "validate_zero_context_reconstruction.py",
    "zero_context_reconstruction.py", "validate_baton_readiness.py", "validate_takeover_certification.py",
    "material_write_ready.py", "validate_quality_review.py", "validate_human_communication.py",
    "validate_owner_change_intake.py", "render_roadmap.py", "self_consistency_audit.py",
    "plan_handover.py", "validate_handover_plan.py", "prepare_handover_projection.py", "append_roadmap_event.py", "publish_owner_progress.py",
]

SKILL_REQUIRED_ENTRYPOINTS = [
    "validate_relay_conformance.py", "cold_start_check.py", "validate_zero_context_reconstruction.py",
    "material_write_ready.py", "publish_owner_progress.py", "plan_handover.py", "self_consistency_audit.py",
]

STALE_MARKERS = {
    "operating-model/object-authority-matrix.md": [
        "Current matrix after CP-R002", "Not implemented", "`repository_ready` kernel field", "future `DISC/QUAL/TC` objects",
    ],
    "operating-model/relay-conformance.md": ["WP-03 still has to implement", "Later WPs still own"],
    "operating-model/catchup-completion-roadmap.md": ["PR #396 remains draft"],
    "SKILL.md": ["WP-07 will translate"],
}

AUTHORITY_SENTINELS = {
    "SKILL.md": [
        "Conversation is acceleration, never custody.",
        "GitHub Issues and generated Markdown are projections, not roadmap authority.",
        "`PROGRESS.yaml` is authority.",
        "Never persist this as a timeless boolean.",
    ],
    "operating-model/object-authority-matrix.md": [
        "BATON_READY", "TAKEOVER_CERTIFIED", "MATERIAL_WRITE_READY", "QRV-*", "OWNER_STATUS.md", "ZERO_CONTEXT_RECONSTRUCTION",
    ],
}

REPO_URL_RE = re.compile(r"https?://(?:www\.)?github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+")


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _yaml_files(paths: Iterable[Path]) -> list[Path]:
    out: list[Path] = []
    for base in paths:
        if base.exists():
            out.extend(sorted(base.glob("*.yaml")))
            out.extend(sorted(base.glob("*.yml")))
    return out


def audit(repo_root: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    skill = repo_root / "skills" / "engineering-pr-delivery-v2.5"
    workflow = repo_root / ".github" / "workflows" / "engineering-pr-delivery-v2.5.yml"

    if not skill.is_dir():
        return [f"missing skill root: {skill}"], warnings

    for rel in ["SKILL.md", "blueprints", "operating-model", "schemas", "scripts", "templates", "tests"]:
        if not (skill / rel).exists():
            errors.append(f"missing required surface: {rel}")

    for rel, sentinels in RELEASE_DOCS.items():
        path = skill / rel
        if not path.is_file():
            errors.append(f"missing release navigation document: {rel}")
            continue
        text = _text(path)
        for sentinel in sentinels:
            if sentinel not in text:
                errors.append(f"release navigation document {rel} missing sentinel: {sentinel}")

    for path in _yaml_files([skill / "schemas", skill / "templates"]):
        try:
            data = yaml.safe_load(_text(path))
        except Exception as exc:
            errors.append(f"YAML parse failed {path.relative_to(skill)}: {exc}")
            continue
        if not isinstance(data, dict):
            errors.append(f"YAML top-level must be mapping: {path.relative_to(skill)}")

    for object_name, rels in OBJECT_SURFACES.items():
        for rel in rels:
            if not (skill / rel).exists():
                errors.append(f"{object_name}: missing surface {rel}")

    blueprints = sorted((skill / "blueprints").glob("*.md"))
    if not blueprints:
        errors.append("no quality blueprints found")
    for path in blueprints:
        text = _text(path)
        for heading in REQUIRED_BLUEPRINT_HEADINGS:
            if heading not in text:
                errors.append(f"{path.name}: missing procedural heading {heading}")

    aggregate = _text(skill / "scripts" / "validate_relay_conformance.py")
    readme = _text(skill / "scripts" / "README.md")
    skill_doc = _text(skill / "SKILL.md")

    for module in AGGREGATE_REQUIRED_MODULES:
        if module not in aggregate:
            errors.append(f"aggregate conformance does not reference {module}")

    for path in sorted((skill / "scripts").glob("validate_*.py")):
        module = path.stem
        if module not in aggregate and path.name not in readme:
            errors.append(f"orphan validator: {path.name} is neither aggregate-reachable nor documented")

    for path in sorted((skill / "scripts").glob("render_*.py")):
        if path.name not in readme:
            errors.append(f"undocumented renderer: {path.name}")

    for name in README_REQUIRED_ENTRYPOINTS:
        if name not in readme:
            errors.append(f"scripts/README.md missing operator entrypoint {name}")
    for name in SKILL_REQUIRED_ENTRYPOINTS:
        if name not in skill_doc:
            errors.append(f"SKILL.md missing core entrypoint {name}")

    for rel, markers in STALE_MARKERS.items():
        text = _text(skill / rel)
        for marker in markers:
            if marker in text:
                errors.append(f"stale normative claim in {rel}: {marker}")

    matrix = _text(skill / "operating-model" / "object-authority-matrix.md")
    if "Current matrix after CP-R010" not in matrix:
        errors.append("object-authority-matrix.md is not reconciled through CP-R010")

    for rel, sentinels in AUTHORITY_SENTINELS.items():
        text = _text(skill / rel)
        for sentinel in sentinels:
            if sentinel not in text:
                errors.append(f"authority sentinel missing from {rel}: {sentinel}")

    for path in sorted((skill / "scripts").glob("*.py")):
        if REPO_URL_RE.search(_text(path)):
            errors.append(f"hard-coded GitHub repository URL in protocol code: {path.relative_to(skill)}")

    if not workflow.exists():
        errors.append("missing scoped V2.5 CI workflow")
    else:
        wf = _text(workflow)
        audit_cmd = "python skills/engineering-pr-delivery-v2.5/scripts/self_consistency_audit.py ."
        root_cmd = "unittest discover -s skills/engineering-pr-delivery-v2.5/tests -p 'test*.py' -v"
        stress_cmd = "unittest discover -s skills/engineering-pr-delivery-v2.5/tests/stress -p 'test*.py' -v"
        if audit_cmd not in wf:
            errors.append("CI workflow does not execute the self-consistency audit")
        if root_cmd not in wf:
            errors.append("CI workflow does not explicitly execute root unit discovery")
        if stress_cmd not in wf:
            errors.append("CI workflow does not explicitly execute dedicated stress discovery")

    documented = readme + "\n" + skill_doc
    library_modules = {
        "relaylib.py", "qualitylib.py", "takeoverlib.py", "progress_projection.py", "report_projection.py",
        "communication_projection.py", "owner_change_projection.py", "zero_context_reconstruction.py",
    }
    for path in sorted((skill / "scripts").glob("*.py")):
        if path.name.startswith("validate_") or path.name.startswith("render_") or path.name in library_modules:
            continue
        if path.name not in documented:
            warnings.append(f"script not named in operator docs: {path.name}")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit Engineering Relay V2.5 cross-surface consistency")
    parser.add_argument("repo_root", nargs="?", default=".")
    args = parser.parse_args()
    errors, warnings = audit(Path(args.repo_root).resolve())
    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        print(f"FAIL: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    print(f"PASS: self-consistency audit; {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
