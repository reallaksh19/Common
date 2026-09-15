#!/usr/bin/env python3
import json
import sys
from pathlib import Path

AUTHORITY_CLASSES = {"CANONICAL", "EVIDENCE", "INFERENCE", "DECISION", "REALIZATION", "VALIDATION"}
ACTIONS = {"COPY", "ADAPT", "REWRITE", "REJECT", "TEST_FIXTURE_ONLY", "REFERENCE_ONLY"}
OWNERS = {
    "ARCHITECTURE_GOVERNANCE",
    "CORE1_CANONICAL_AUTHORITY",
    "CORE1_EVIDENCE_CUSTODY",
    "LEARNER_INTELLIGENCE",
    "CORE2A_STUDY_SYNTHESIS",
    "CORE2B_LEARNING_DESIGN",
    "CORE2C_PUBLICATION_REALIZATION",
    "TEST_CONFORMANCE",
    "RELEASE_VALIDATION",
}
REQUIRED = {
    "id", "source_pr_or_issue", "source_path_or_artifact", "source_commit_or_identity",
    "source_authority_class", "behavior_or_invariant", "v2_action", "v2_owner",
    "v2_destination", "semantic_differences", "old_validation", "new_validation_required",
    "runtime_dependency_allowed", "benchmark_derived", "status",
}


def validate_document(doc):
    errors = []
    if doc.get("schema_version") != "0.1.0":
        errors.append("schema_version must be 0.1.0")
    if doc.get("programme_issue") != 175:
        errors.append("programme_issue must be 175")
    if doc.get("implementation_issue") != 178:
        errors.append("implementation_issue must be 178")
    entries = doc.get("entries")
    if not isinstance(entries, list) or not entries:
        return errors + ["entries must be a non-empty list"]

    seen = set()
    for i, entry in enumerate(entries):
        prefix = f"entries[{i}]"
        if not isinstance(entry, dict):
            errors.append(f"{prefix} must be an object")
            continue
        missing = sorted(REQUIRED - set(entry))
        if missing:
            errors.append(f"{prefix} missing required fields: {', '.join(missing)}")
            continue
        eid = entry["id"]
        if eid in seen:
            errors.append(f"{prefix} duplicate id {eid}")
        seen.add(eid)

        if entry["source_authority_class"] not in AUTHORITY_CLASSES:
            errors.append(f"{prefix} invalid source_authority_class")
        if entry["v2_action"] not in ACTIONS:
            errors.append(f"{prefix} invalid v2_action")
        if entry["v2_owner"] not in OWNERS:
            errors.append(f"{prefix} invalid v2_owner")
        if entry["runtime_dependency_allowed"] is not False:
            errors.append(f"{prefix} old-branch runtime dependency is forbidden")
        if not isinstance(entry["semantic_differences"], list) or not entry["semantic_differences"]:
            errors.append(f"{prefix} semantic_differences must be non-empty")
        if not isinstance(entry["new_validation_required"], list) or not entry["new_validation_required"]:
            errors.append(f"{prefix} new_validation_required must be non-empty")

        action = entry["v2_action"]
        status = entry["status"]
        if action == "COPY" and not entry.get("copy_equivalence_evidence"):
            errors.append(f"{prefix} COPY requires copy_equivalence_evidence")
        if action == "TEST_FIXTURE_ONLY" and status != "TEST_ONLY":
            errors.append(f"{prefix} TEST_FIXTURE_ONLY requires TEST_ONLY status")
        if action == "REFERENCE_ONLY" and status != "REFERENCE_ONLY":
            errors.append(f"{prefix} REFERENCE_ONLY requires REFERENCE_ONLY status")

        source = entry["source_pr_or_issue"].lower()
        artifact = entry["source_path_or_artifact"].lower()
        destination = entry["v2_destination"].lower()

        if entry["benchmark_derived"] and action not in {"REFERENCE_ONLY", "TEST_FIXTURE_ONLY", "REJECT"}:
            errors.append(f"{prefix} benchmark-derived material cannot enter the V2-00A producer")
        if ("pr #156" in source or "pr #157" in source) and (
            entry["source_authority_class"] != "VALIDATION"
            or entry["v2_owner"] != "RELEASE_VALIDATION"
            or action != "REFERENCE_ONLY"
        ):
            errors.append(f"{prefix} PR #156/#157 must remain final-validation REFERENCE_ONLY")
        if "synthetic" in artifact and "#168" in source and action != "TEST_FIXTURE_ONLY":
            errors.append(f"{prefix} PR #168 synthetic fixtures must be TEST_FIXTURE_ONLY")
        if entry["source_authority_class"] in {"EVIDENCE", "INFERENCE"} and entry["v2_owner"] == "CORE1_CANONICAL_AUTHORITY":
            errors.append(f"{prefix} learner/evidence semantics cannot mutate Core1 canonical truth")
        if entry["source_authority_class"] == "REALIZATION" and entry["v2_owner"] == "CORE2A_STUDY_SYNTHESIS":
            errors.append(f"{prefix} publication realization cannot own Study Synthesis")
        if any(token in destination for token in ("refs/pull/", "heads/architecture/learner-intelligence", "heads/architecture/core2", "heads/architecture/competitive-exams")):
            errors.append(f"{prefix} v2_destination appears to depend on an old branch ref")
    return errors


def main(path):
    doc = json.loads(Path(path).read_text(encoding="utf-8"))
    errors = validate_document(doc)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print(f"PASS: {len(doc['entries'])} adoption entries validated")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: validate_adoption_ledger.py <ledger.json>")
        raise SystemExit(2)
    raise SystemExit(main(sys.argv[1]))
