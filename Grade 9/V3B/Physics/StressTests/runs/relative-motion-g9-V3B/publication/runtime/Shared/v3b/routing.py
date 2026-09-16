"""Evidence-based routes and dependency-preserving bounded assignments."""

from __future__ import annotations

from .contracts import digest, require, strings, text, unique


def route_subtopic(subtopic: dict, manifest: dict) -> dict:
    evidence = {x["source_id"]: x for x in manifest["items"]}
    refs = subtopic["source_refs"]
    rows = [evidence[x] for x in refs]
    basis = subtopic.get("routing_basis", {})
    text(basis.get("rationale"), "ROUTING_RATIONALE_REQUIRED")
    for key in ("scope_established", "semantic_source_usable", "questions_interpretable", "material_conflict"):
        require(type(basis.get(key)) is bool, "ROUTING_BASIS_REQUIRED", key)
    semantic = any(x["kind"] in {"SYLLABUS", "TEXTBOOK", "SUPPLIED_MODEL"} and
                   x["availability"] in {"PRESENT", "PARTIAL"} for x in rows)
    questions = any(x["kind"] == "QUESTIONS" and
                    x["availability"] in {"PRESENT", "PARTIAL"} for x in rows)
    require(not basis["semantic_source_usable"] or semantic, "ROUTING_SEMANTIC_EVIDENCE_MISMATCH")
    require(not basis["questions_interpretable"] or questions, "ROUTING_QUESTION_EVIDENCE_MISMATCH")
    if basis["material_conflict"] or any(x["availability"] == "CONFLICTED" for x in rows):
        route, code = "BLOCK", "MATERIAL_CONFLICT"
    elif basis["scope_established"] and basis["semantic_source_usable"]:
        route, code = "CORE1_FIRST", "ESTABLISHED_SEMANTIC_SCOPE"
    elif basis["questions_interpretable"]:
        route, code = "CORE2_FIRST", "PROVISIONAL_QUESTION_SCOPE"
    else:
        route, code = "BLOCK", "INSUFFICIENT_BOUNDED_EVIDENCE"
    result = {"subtopic_id": subtopic["subtopic_id"], "route": route, "reason_code": code,
              "basis": basis, "source_refs": refs, "scope_provisional": route == "CORE2_FIRST"}
    return {**result, "route_digest": digest(result)}


def make_bundles(manifest: dict, assignments: list[dict]) -> list[dict]:
    topics = unique(manifest["subtopics"], "subtopic_id", "SUBTOPIC_ID_DUPLICATE")
    unique(assignments, "bundle_id", "BUNDLE_ID_DUPLICATE")
    seen, bundles = set(), []
    for assignment in assignments:
        ids = strings(assignment.get("subtopic_ids"), "BUNDLE_SUBTOPICS_REQUIRED")
        require(1 <= len(ids) <= 3, "BUNDLE_SIZE_EXCEEDED")
        require(set(ids) <= set(topics), "BUNDLE_UNKNOWN_SUBTOPIC")
        require(not seen.intersection(ids), "SUBTOPIC_ASSIGNED_TWICE")
        seen.update(ids)
        routes = [route_subtopic(topics[x], manifest) for x in ids]
        require(len({x["route"] for x in routes}) == 1, "RESHARD_DIFFERENT_FIRST_ROLES")
        bundles.append({**assignment, "routes": routes, "first_role": routes[0]["route"].removesuffix("_FIRST")})
    required = {x for x, row in topics.items() if row["disposition"] == "REQUIRED"}
    require(required <= seen, "REQUIRED_SUBTOPIC_UNASSIGNED", ",".join(sorted(required - seen)))
    return bundles
