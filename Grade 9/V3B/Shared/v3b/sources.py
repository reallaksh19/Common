"""Freeze source bytes and preserve absence separately from derived claims."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path

from .contracts import digest, require, strings, text, unique, validate_dag, verify_file


AVAILABILITY = {"PRESENT", "ABSENT", "PARTIAL", "UNRESOLVED", "CONFLICTED"}


def freeze_sources(spec: dict, source_root: Path, request: dict) -> dict:
    items = deepcopy(spec.get("items", []))
    require(bool(items), "SOURCE_INVENTORY_REQUIRED")
    unique(items, "source_id", "SOURCE_ID_DUPLICATE")
    for item in items:
        _check_source(item, source_root, request["run_kind"])
    scopes = deepcopy(spec.get("subtopics", []))
    require(bool(scopes), "SUBTOPIC_SCOPE_REQUIRED")
    order = validate_dag(scopes, "subtopic_id", "prerequisite_ids")
    all_capabilities = [c for row in scopes for c in row.get("capability_ids", [])]
    require(len(all_capabilities) == len(set(all_capabilities)), "CAPABILITY_PRIMARY_HOME_DUPLICATE")
    available = {x["source_id"] for x in items if x["availability"] in {"PRESENT", "PARTIAL"}}
    for row in scopes:
        text(row.get("title"), "SUBTOPIC_TITLE_REQUIRED")
        strings(row.get("capability_ids"), "CAPABILITY_SCOPE_REQUIRED")
        refs = strings(row.get("source_refs"), "SUBTOPIC_SOURCE_REQUIRED")
        require(set(refs) <= available, "SUBTOPIC_SOURCE_UNAVAILABLE", row["subtopic_id"])
        require(row.get("disposition") in {"REQUIRED", "OWNER_DEFERRED", "EXTENSION"}, "SCOPE_DISPOSITION_REQUIRED")
        if row["disposition"] != "REQUIRED":
            text(row.get("disposition_reason"), "SCOPE_DISPOSITION_REASON_REQUIRED")
    body = {"items": items, "subtopics": scopes, "dependency_order": order,
            "subject": request["subject"], "run_kind": request["run_kind"]}
    return {**body, "manifest_digest": digest(body)}


def _check_source(item: dict, root: Path, run_kind: str) -> None:
    require(item.get("authority") in {"ORIGINAL_EVIDENCE", "AUTHORITATIVE_SOURCE"},
            "GROUND_TRUTH_AUTHORITY_FORBIDDEN", item["source_id"])
    require(item.get("availability") in AVAILABILITY, "SOURCE_AVAILABILITY_INVALID")
    require(item.get("kind") in {"SYLLABUS", "TEXTBOOK", "QUESTIONS", "FIGURE", "ANSWER_KEY", "SUPPLIED_MODEL"},
            "SOURCE_KIND_INVALID")
    if item["availability"] == "ABSENT":
        require(item.get("file") is None, "ABSENT_SOURCE_HAS_FILE")
        return
    require(isinstance(item.get("file"), dict), "SOURCE_FILE_REQUIRED")
    verify_file(root, item["file"])
    text(item.get("locator"), "SOURCE_LOCATOR_REQUIRED")
    if run_kind == "PRODUCTION":
        require(item.get("provenance") == "ORIGINAL_SOURCE", "FIXTURE_CANNOT_AUTHORIZE_PRODUCTION")
    if item["availability"] == "CONFLICTED":
        strings(item.get("conflict_refs"), "SOURCE_CONFLICT_RECORD_REQUIRED")


def verify_manifest(manifest: dict, source_root: Path) -> None:
    body = {k: v for k, v in manifest.items() if k != "manifest_digest"}
    require(manifest.get("manifest_digest") == digest(body), "SOURCE_MANIFEST_CHANGED")
    for item in manifest["items"]:
        if item["availability"] != "ABSENT":
            verify_file(source_root, item["file"])
            if item.get("normalized_questions"):
                verify_file(source_root, item["normalized_questions"]["file"])
