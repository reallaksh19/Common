"""Work-order boundary, fresh actors and the single accepted stage sequence."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path

from .assimilation import validate_plan
from .contracts import ContractError, digest, file_digest, require, strings, text, verify_file
from .intelligence import compile_join, validate_claim_review, validate_specialist
from .practice import compile_eligibility, validate_candidates, validate_practice_review
from .publication import compile_publication, validate_publication
from .question_sources import validate_question_custody
from .receipts import compile_receipts, validate_content_review, validate_manuscript
from .sources import verify_manifest


STAGES = ("FIRST_CORE", "SECOND_CORE_BLIND", "CLAIM_REVIEW", "JOIN", "ASSIMILATION_PLAN",
          "MANUSCRIPT", "CONTENT_REVIEW", "TEACHING_RECEIPTS", "PRACTICE_CANDIDATES",
          "PRACTICE_ELIGIBILITY", "PRACTICE_REVIEW", "PUBLICATION_IR")
AUTOMATIC = {"JOIN", "TEACHING_RECEIPTS", "PRACTICE_ELIGIBILITY", "PUBLICATION_IR"}


def context_for(store, bundle_id: str) -> dict:
    metadata = store.metadata()
    bundle = next((x for x in metadata["bundles"] if x["bundle_id"] == bundle_id), None)
    require(bundle is not None, "BUNDLE_UNKNOWN")
    require(bundle["first_role"] != "BLOCK", "BUNDLE_BLOCKED_BY_EVIDENCE")
    verify_manifest(metadata["manifest"], Path(metadata["source_root"]))
    for ref in metadata.get("runtime_bindings", []):
        require(file_digest(Path(ref["path"])) == ref["sha256"], "RUNTIME_POLICY_CHANGED", ref["path"])
    for packet in store.packets(bundle_id).values():
        for section in packet["payload"].get("sections", []):
            if isinstance(section, dict) and section.get("kind") == "REPRESENTATION":
                verify_file(Path(metadata["artifact_root"]), section["asset"])
    topics = [x for x in metadata["manifest"]["subtopics"] if x["subtopic_id"] in bundle["subtopic_ids"]]
    external_topics = _external_topics(metadata["manifest"]["subtopics"], bundle["subtopic_ids"])
    external_packets = {}
    for other in metadata["bundles"]:
        if set(other["subtopic_ids"]) & external_topics:
            receipt = store.packets(other["bundle_id"]).get("TEACHING_RECEIPTS")
            if receipt:
                external_packets[other["bundle_id"]] = receipt
    external_digests = {k: v["digest"] for k, v in external_packets.items()}
    for accepted in store.packets(bundle_id).values():
        binding = accepted["payload"].get("_execution", {}).get("external_teaching_digests")
        if binding is not None:
            require(binding == external_digests, "STALE_PREREQUISITE_TEACHING")
    available = [x for x in metadata["manifest"]["subtopics"] if x["subtopic_id"] in set(bundle["subtopic_ids"]) | external_topics]
    return {**metadata, "bundle": bundle, "subtopic_ids": bundle["subtopic_ids"],
            "capability_ids": sorted({c for x in topics for c in x["capability_ids"]}),
            "available_capability_ids": sorted({c for x in available for c in x["capability_ids"]}),
            "external_teaching_packets": external_packets, "external_teaching_digests": external_digests,
            "artifact_root": Path(metadata["artifact_root"]), "source_root": Path(metadata["source_root"])}


def _external_topics(topics: list[dict], assigned: list[str]) -> set[str]:
    indexed = {x["subtopic_id"]: x for x in topics}
    pending, seen = list(assigned), set()
    while pending:
        current = pending.pop()
        if current not in seen:
            seen.add(current)
            pending.extend(indexed[current]["prerequisite_ids"])
    return seen - set(assigned)


def _role(stage: str, context: dict) -> str:
    first = context["bundle"]["first_role"]
    if stage == "FIRST_CORE":
        return first
    if stage == "SECOND_CORE_BLIND":
        return "CORE2" if first == "CORE1" else "CORE1"
    return {"CLAIM_REVIEW": "CLAIM_REVIEW", "ASSIMILATION_PLAN": "CORE1A",
            "MANUSCRIPT": "CORE1A", "CONTENT_REVIEW": "CONTENT_REVIEW",
            "PRACTICE_CANDIDATES": "CORE2A", "PRACTICE_REVIEW": "PRACTICE_REVIEW"}[stage]


def _actor(stage: str, role: str, context: dict, packets: dict) -> dict:
    previous = {x["actor"] for x in packets.values() if x["actor"] != "GOVERNOR"}
    eligible = []
    for row in context["actors"]:
        if role not in row["eligible_roles"] or context["request"]["subject"] not in row["subjects"]:
            continue
        if stage == "MANUSCRIPT":
            if row["instance_id"] != packets["ASSIMILATION_PLAN"]["actor"]:
                continue
        elif row["instance_id"] in previous:
            continue
        eligible.append(row)
    require(bool(eligible), "NO_ELIGIBLE_FRESH_ACTOR", role)
    return sorted(eligible, key=lambda x: (x["priority"], x["profile_id"], x["instance_id"]))[0]


def work_order(store, bundle_id: str) -> dict:
    context = context_for(store, bundle_id)
    state = store.bundle(bundle_id)
    require(state["cursor"] < len(STAGES), "BUNDLE_ALREADY_COMPLETE")
    stage = STAGES[state["cursor"]]
    packets = store.packets(bundle_id)
    _check_prerequisites(store, context, stage)
    role = "GOVERNOR" if stage in AUTOMATIC else _role(stage, context)
    actor = {"instance_id": "GOVERNOR", "profile_id": "DETERMINISTIC_CONTROL"} if stage in AUTOMATIC else _actor(stage, role, context, packets)
    visible = {} if stage in {"FIRST_CORE", "SECOND_CORE_BLIND"} else packets
    order = {"bundle_id": bundle_id, "stage": stage, "role": role,
             "actor_instance_id": actor["instance_id"], "profile_id": actor["profile_id"],
             "revision": state["revision"], "epoch": state["epoch"],
             "request_digest": context["request_digest"], "manifest_digest": context["manifest"]["manifest_digest"],
             "allowed_packet_digests": sorted(x["digest"] for x in visible.values()),
             "source_ids": [x["source_id"] for x in context["manifest"]["items"]],
             "external_teaching_digests": context["external_teaching_digests"] if STAGES.index(stage) >= STAGES.index("ASSIMILATION_PLAN") else None,
             "subtopic_ids": context["subtopic_ids"], "capability_ids": context["capability_ids"],
             "isolation_requirement": "FRESH_SOURCE_ONLY_CONTEXT" if not visible else "FRESH_ROLE_OR_APPROVED_SAME_ROLE_CONTINUATION",
             "enforcement_scope": "WORK_ORDER_AND_PAYLOAD_FILTERING_HOST_MUST_ISOLATE_CONTEXT"}
    return {**order, "work_order_digest": digest(order), "visible_packets": visible,
            "owner_request": context["request"], "source_manifest": context["manifest"]}


def _check_prerequisites(store, context: dict, stage: str) -> None:
    if STAGES.index(stage) < STAGES.index("ASSIMILATION_PLAN"):
        return
    other = {sid: x["bundle_id"] for x in context["bundles"] for sid in x["subtopic_ids"]}
    for topic in context["manifest"]["subtopics"]:
        if topic["subtopic_id"] not in context["subtopic_ids"]:
            continue
        for prerequisite in topic["prerequisite_ids"]:
            if prerequisite in context["subtopic_ids"]:
                continue
            host = other.get(prerequisite)
            require(host is not None and "TEACHING_RECEIPTS" in store.packets(host),
                    "CROSS_BUNDLE_PREREQUISITE_NOT_TAUGHT", prerequisite)


def accept_submission(store, submission: dict) -> dict:
    order = submission["work_order"]
    bundle_id, stage = order["bundle_id"], order["stage"]
    actor = order["actor_instance_id"]
    payload = deepcopy(submission["payload"])
    context_for(store, bundle_id)
    previous = store.packets(bundle_id).get(stage)
    if previous:
        require(previous["payload"].get("_execution", {}).get("work_order_digest") == order["work_order_digest"],
                "CANONICAL_ACCEPTANCE_ALREADY_EXISTS")
        payload["_execution"] = previous["payload"]["_execution"]
        return store.accept(bundle_id, stage, actor, payload, order["revision"], order["epoch"])
    current = work_order(store, bundle_id)
    require(current == order, "STALE_OR_FORGED_WORK_ORDER")
    require(stage not in AUTOMATIC, "GOVERNOR_STAGE_NOT_AUTHORABLE")
    require(submission.get("visible_packet_digests") == current["allowed_packet_digests"], "CONTEXT_EXPOSURE_MISMATCH")
    context, packets = context_for(store, bundle_id), store.packets(bundle_id)
    try:
        _validate_stage(stage, payload, current["role"], actor, context, packets)
    except ContractError as exc:
        store.reject(bundle_id, stage, actor, payload, exc.code)
        raise
    payload["_execution"] = {k: current[k] for k in ("work_order_digest", "actor_instance_id", "profile_id", "request_digest", "manifest_digest", "allowed_packet_digests", "external_teaching_digests")}
    return store.accept(bundle_id, stage, actor, payload, current["revision"], current["epoch"])


def _validate_stage(stage: str, payload: dict, role: str, actor: str, context: dict, packets: dict) -> None:
    if stage in {"FIRST_CORE", "SECOND_CORE_BLIND"}:
        validate_specialist(payload, role, context)
        if role == "CORE2":
            validate_question_custody(payload.get("questions", []), context)
    elif stage == "CLAIM_REVIEW":
        validate_claim_review(payload, packets, actor)
        available = {x["source_id"] for x in context["manifest"]["items"] if x["availability"] in {"PRESENT", "PARTIAL"}}
        require(all(set(x["source_refs"]) <= available for x in payload["reviews"]), "REVIEW_UNKNOWN_SOURCE")
    elif stage == "ASSIMILATION_PLAN":
        validate_plan(payload, packets["JOIN"]["payload"], context)
    elif stage == "MANUSCRIPT":
        validate_manuscript(payload, packets["ASSIMILATION_PLAN"]["payload"], context)
    elif stage == "CONTENT_REVIEW":
        validate_content_review(payload, packets["MANUSCRIPT"], actor)
    elif stage == "PRACTICE_CANDIDATES":
        validate_candidates(payload, packets, context)
    elif stage == "PRACTICE_REVIEW":
        validate_practice_review(payload, packets["PRACTICE_ELIGIBILITY"], actor)


def advance_automatic(store, bundle_id: str) -> dict:
    order = work_order(store, bundle_id)
    stage = order["stage"]
    require(stage in AUTOMATIC, "NEXT_STAGE_REQUIRES_AGENT", stage)
    context, packets = context_for(store, bundle_id), store.packets(bundle_id)
    if stage == "JOIN":
        payload = compile_join(packets, context)
    elif stage == "TEACHING_RECEIPTS":
        payload = compile_receipts(packets, context)
    elif stage == "PRACTICE_ELIGIBILITY":
        payload = compile_eligibility(packets["PRACTICE_CANDIDATES"]["payload"], packets, context)
    else:
        payload = compile_publication(packets, context)
        validate_publication(payload, packets)
    return store.accept(bundle_id, stage, "GOVERNOR", payload, order["revision"], order["epoch"])


def validate_actors(actors: list[dict], run_kind: str) -> None:
    ids = strings([x.get("instance_id") for x in actors], "ACTOR_IDS_INVALID")
    require("GOVERNOR" not in ids, "RESERVED_ACTOR_ID")
    for actor in actors:
        for key in ("profile_id", "qualification_basis"):
            text(actor.get(key), "ACTOR_QUALIFICATION_REQUIRED")
        strings(actor.get("eligible_roles"), "ACTOR_ROLES_REQUIRED")
        strings(actor.get("subjects"), "ACTOR_SUBJECTS_REQUIRED")
        require(type(actor.get("priority")) is int, "ACTOR_PRIORITY_REQUIRED")
        if run_kind == "PRODUCTION":
            require(actor.get("qualification_status") == "INDEPENDENTLY_REVIEWED", "ACTOR_QUALIFICATION_UNVERIFIED")
            require(actor.get("qualification_reviewer_id") != actor["instance_id"] and
                    bool(actor.get("qualification_reviewer_id")), "ACTOR_SELF_QUALIFICATION")
