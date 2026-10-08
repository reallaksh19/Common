#!/usr/bin/env python3
"""Source-bound R-PROJECTION read model for Common #718/#733 (V3.2 only).

Pure/read-only: Owner provenance + released plan + accepted DELP facts +
provider-observed material + separately qualified R-PROOF observation.
The read views never grant programme, task, review, custody or merge authority.
The three human-facing title bases are human-owned; only prefixes and managed
blocks are regenerated. No live GitHub writer is enabled by this module.
"""
from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Mapping
from pathlib import Path
from typing import Any

import delp_projection_v32 as delp

AUTHORITY = "DERIVED_R_PROJECTION_READ_VIEW_ONLY"
SCHEMA = "relay-v3.2-source-bound-responsibility-view-v1"
START = "<!-- relay-v32:pr-read-view:start -->"
END = "<!-- relay-v32:pr-read-view:end -->"
ISSUE_START = "<!-- relay-v32:issue-read-view:start -->"
ISSUE_END = "<!-- relay-v32:issue-read-view:end -->"
_SHA = re.compile(r"^[0-9a-f]{40}$", re.IGNORECASE)
_PHASE = re.compile(r"^C[0-9]+(?:-[A-Z])?$")
_LIFECYCLES = frozenset({"DRAFT", "OPEN", "MERGED", "CLOSED"})
OWNER_UNKNOWN = "UNRESOLVED_CHAT_MESSAGE_LINK"
HUMAN_SUFFIX = " — "


class ViewError(ValueError):
    pass


def digest(value: Any) -> str:
    text = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def _require(condition: bool, code: str) -> None:
    if not condition:
        raise ViewError(code)


def _number(value: str) -> int:
    return int(value.rsplit("#", 1)[-1])


def _suffix_title(prefix: str, human_base: str) -> str:
    # Human identity cannot be scraped from a generated title: callers must
    # supply the independently observed/human-owned base explicitly.
    _require(isinstance(human_base, str) and bool(human_base.strip()), "HUMAN_TITLE_BASE_REQUIRED")
    _require("\n" not in human_base and "\r" not in human_base, "INVALID_HUMAN_TITLE")
    available = 250 - len(prefix) - len(HUMAN_SUFFIX)
    _require(available >= 3, "PREFIX_TOO_LONG")
    base = human_base.strip()
    if len(base) > available:
        base = base[:available - 1].rstrip() + "…"
    return prefix + HUMAN_SUFFIX + base


def owner_trace(
    owner: Mapping[str, Any],
    *,
    required_claims: set[str],
    responsibility_id: str,
) -> dict[str, Any]:
    """Validate an independently supplied Owner intent+OR ledger; no oracle outputs."""
    _require(isinstance(owner, Mapping), "OWNER_LEDGER_MISSING")
    intents = owner.get("owner_intents")
    requirements = owner.get("requirements")
    _require(isinstance(intents, list) and bool(intents), "OWNER_INTENTS_MISSING")
    _require(isinstance(requirements, list) and bool(requirements), "OR_LEDGER_MISSING")
    index = {r.get("id"): r for r in requirements if isinstance(r, Mapping)}
    _require(len(index) == len(requirements), "DUPLICATE_OR_ID")
    linked = []
    for intent in intents:
        _require(isinstance(intent, Mapping) and bool(intent.get("verbatim")), "OWNER_QUOTATION_MISSING")
        source = intent.get("original_source_ref")
        if source is None:
            _require(intent.get("original_source_status") == OWNER_UNKNOWN, "ORIGINAL_SOURCE_UNACCOUNTED")
        else:
            _require(isinstance(source, str) and bool(source.strip()), "ORIGINAL_SOURCE_INVALID")
        archive = intent.get("durable_archive_ref")
        _require(isinstance(archive, str) and archive.startswith("https://github.com/"), "DURABLE_ORIGIN_ARCHIVE_MISSING")
        refs = intent.get("requirements")
        _require(isinstance(refs, list) and bool(refs), "OWNER_REQUIREMENT_LINK_MISSING")
        for key in refs:
            _require(key in index, "ORIGINAL_INTENT_TO_OR_MISSING")
        linked.append({
            "id": intent.get("id"), "verbatim": intent["verbatim"],
            "original_source_ref": source,
            "original_source_status": intent.get("original_source_status") if source is None else "LINKED",
            "durable_archive_ref": archive, "OR_ids": refs,
        })
    accepted = []
    for req in requirements:
        _require(isinstance(req, Mapping), "MALFORMED_OR")
        _require(bool(req.get("claims")) and bool(req.get("fixture_ids")), "OR_TRACE_OR_FIXTURE_MISSING")
        _require(set(req["claims"]).issubset(required_claims), "OR_TO_UNRELEASED_CLAIM")
        if req.get("responsibility") == responsibility_id:
            accepted.append({
                "id": req["id"], "claim_ids": list(req["claims"]),
                "fixture_ids": list(req["fixture_ids"]),
                "source_refs": list(req.get("source_refs") or []),
            })
    _require(bool(accepted), "SELECTED_RESPONSIBILITY_HAS_NO_OR")
    _require(any(any(x["id"] in o["OR_ids"] for o in linked) for x in accepted),
             "SELECTED_OR_NOT_CONNECTED_TO_OWNER")
    return {"owner_intents": linked, "selected_OR": accepted}


def _independent_qualification(observation: Any, head_sha: str | None) -> dict[str, str]:
    if observation is None:
        return {"state": "UNPROVEN", "basis": "NOT_OBSERVED"}
    _require(isinstance(observation, Mapping), "INVALID_QUALIFIER")
    _require(observation.get("authority") == "DERIVED_OBSERVATION_ONLY", "QUALIFIER_AUTHORITY_INVALID")
    qhead = observation.get("observed_candidate_sha")
    _require(qhead is None or _SHA.fullmatch(str(qhead)) is not None, "QUALIFIER_INVALID_SHA")
    state = observation.get("overall")
    _require(state in {"PROVEN", "UNPROVEN", "UNKNOWN"}, "QUALIFIER_INVALID_VERDICT")
    if not head_sha or qhead != head_sha:
        return {"state": "UNPROVEN", "basis": "STALE_OR_UNBOUND_QUALIFICATION"}
    return {"state": str(state), "basis": "INDEPENDENT_OBSERVATION_ONLY"}


def build_views(
    graph: Mapping[str, Any],
    owner: Mapping[str, Any],
    *,
    ledger: list[Mapping[str, Any]] | None = None,
    observations: Mapping[str, Mapping[str, Any]] | None = None,
    selected_leaf: str,
    phase: str,
    human_titles: Mapping[str, str],
    draft_pr: Mapping[str, Any] | None = None,
    qualification: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Generate all currently released R-PROJECTION read views at one basis.

    A material candidate not yet bound in released graph is shown as advisory
    and does NOT qualify/complete the leaf. The input observer must be trusted
    by the caller; this pure function cannot authenticate GitHub provider data.
    """
    _require(bool(_PHASE.fullmatch(phase)), "UNRELEASED_PHASE")
    _require(isinstance(human_titles, Mapping), "HUMAN_TITLES_MISSING")
    projection = delp.project(graph, ledger or [], observations or {})
    nodes = projection["nodes"]
    root_ref = projection["root"]
    _require(selected_leaf in nodes and nodes[selected_leaf]["kind"] == "LEAF", "SELECTED_CHILD_NOT_LEAF")
    raw_node = next((n for n in graph["nodes"] if n["ref"] == selected_leaf), None)
    _require(raw_node is not None and bool(raw_node.get("responsibility_id")), "RESPONSIBILITY_ID_MISSING")
    identity = raw_node["responsibility_id"]
    claim_ids = set(row["id"] for row in graph["programme"]["acceptance_claims"])
    _require(set(raw_node.get("owns_claims") or []).issubset(claim_ids), "UNKNOWN_SELECTED_CLAIM")
    release = graph["programme"].get("decomposition_proposal") or {}
    _require(owner.get("released_proposal_digest") == release.get("released_proposal_digest"),
             "OWNER_TO_RELEASE_DIGEST_MISMATCH")
    proof = owner_trace(owner, required_claims=claim_ids, responsibility_id=identity)
    proposed = {r["id"]: r for r in release.get("responsibilities") or []}
    _require(identity in proposed and set(proposed[identity]["owns_claims"]) == set(raw_node.get("owns_claims") or []),
             "SELECTED_CLAIM_CONTRACT_DRIFT")
    _require(any(b.get("responsibility_id") == identity and b.get("ref") == selected_leaf
                 for b in release.get("bindings") or []), "RESPONSIBILITY_NOT_PROVIDER_BOUND")
    pr_details = None
    if draft_pr is not None:
        _require(isinstance(draft_pr, Mapping), "INVALID_PR_OBSERVATION")
        sha = draft_pr.get("head_sha")
        _require(isinstance(sha, str) and bool(_SHA.fullmatch(sha)), "PR_EXACT_HEAD_REQUIRED")
        number = draft_pr.get("number")
        _require(type(number) is int and number > 0, "PR_NUMBER_REQUIRED")
        lifecycle = draft_pr.get("lifecycle")
        _require(lifecycle in _LIFECYCLES, "PR_LIFECYCLE_INVALID")
        # Not every draft is in the released execution graph yet. This is a
        # distinct provider-delivery view, NEVER an accepted fact.
        bound = raw_node.get("primary_pr") == f"Common#{number}"
        pr_details = {"number": number, "head_sha": sha,
                      "lifecycle": lifecycle, "binding": "BOUND" if bound else "UNBOUND_ADVISORY"}
    candidate = pr_details["head_sha"] if pr_details else None
    q = _independent_qualification(qualification, candidate)
    _require(not pr_details or not pr_details["binding"] == "UNBOUND_ADVISORY" or q["state"] != "PROVEN",
             "UNBOUND_PR_CANNOT_ACQUIRE_QUALIFICATION")
    reserve = next(n.get("reserve_weight", 0) for n in graph["nodes"] if n["ref"] == root_ref)
    root = nodes[root_ref]
    child = nodes[selected_leaf]
    number = _number(selected_leaf)
    parent_number = _number(root_ref)
    historical_unreported = [
        n["ref"] for n in graph["nodes"]
        if n["kind"] == "LEAF" and n.get("primary_pr") and
        nodes[n["ref"]]["progress"]["P"] == 0 and nodes[n["ref"]]["progress"]["E"] == 0 and
        nodes[n["ref"]]["state"] in {"UNMATERIALIZED", "EVIDENCE_GAP"}
    ]
    facts_label = "FACTS UNREPORTED" if historical_unreported else "FACTS RECONCILED"
    parent_prefix = f"🟡 [{parent_number}] NEXT #{number}/{phase} · RESERVE{reserve} · {facts_label}"
    leaf_prefix = (
        f"🟡 [{parent_number}›{number}] {identity} · {phase} · NO PRODUCT PR · CODE HELD"
        if not raw_node.get("primary_pr")
        else f"🟡 [{parent_number}›{number}] {identity} · {phase} · PR#{_number(raw_node['primary_pr'])} · {child['state']}"
    )
    parent_title = _suffix_title(parent_prefix, human_titles[root_ref])
    child_title = _suffix_title(leaf_prefix, human_titles[selected_leaf])
    pr_title = None
    if pr_details:
        pr_prefix = (f"🟡 [{parent_number}›{number}] {pr_details['lifecycle']} · VIEW-PR · "
                     f"HEAD:{pr_details['head_sha'][:7]} · Q:{q['state']}")
        pr_title = _suffix_title(pr_prefix, human_titles["PR"])
    or_ids = sorted({r["id"] for r in proof["selected_OR"]})
    fixture_ids = sorted({s for r in proof["selected_OR"] for s in r["fixture_ids"]})
    actual_next = (
        "MATERIALIZE_FACTS_OR_CONTRACT" if child["state"] == "UNMATERIALIZED" else
        "RELEASE_AND_BIND_PRODUCT_PR" if not raw_node.get("primary_pr") else
        "RECONCILE_CURRENT_FACTS_AND_QUALIFICATION"
    )
    basis = {
        "graph": projection["plan_digest"], "delp_input": projection["input_digest"],
        "owner_intent_requirements": digest({
            "owner_intents": owner["owner_intents"], "requirements": owner["requirements"],
            "released_proposal_digest": owner["released_proposal_digest"],
        }),
        "selected_leaf": selected_leaf, "phase": phase,
        "draft_pr": pr_details, "qualifier": dict(qualification or {}),
        "human_titles": {k: human_titles[k] for k in (root_ref, selected_leaf) if k in human_titles},
        "human_pr_title": human_titles.get("PR") if pr_details else None,
    }
    snapshot = {
        "schema": SCHEMA, "authority": AUTHORITY, "input_digest": digest(basis),
        "delp_input_digest": projection["input_digest"], "plan_digest": projection["plan_digest"],
        "root": root_ref, "leaf": selected_leaf, "responsibility": identity,
        "claim_ids": sorted(raw_node.get("owns_claims") or []),
        "owner_trace": proof, "OR_ids": or_ids, "golden_fixture_ids": fixture_ids,
        "root_reserve": reserve, "historical_unreported": historical_unreported,
        "parent_semantic": root["progress"], "leaf_semantic": child["progress"],
        "leaf_state": child["state"], "qualification": q,
        "pr": pr_details, "actual_next": actual_next,
        "issue_titles": {root_ref: parent_title, selected_leaf: child_title},
        "draft_pr_title": pr_title,
        "unreleased_consumers": {"handover": "NOT_IMPLEMENTED", "agent_matrix": "NOT_IMPLEMENTED"},
        "authority_effects": [],
    }
    snapshot["issue_read_views"] = {
        ref: render_issue_block(snapshot, ref) for ref in (root_ref, selected_leaf)
    }
    snapshot["pr_managed_block"] = render_pr_block(snapshot) if pr_details else None
    return snapshot


def render_issue_block(snapshot: Mapping[str, Any], ref: str) -> str:
    _require(ref in snapshot["issue_titles"], "UNKNOWN_ISSUE_VIEW")
    part = "PARENT" if ref == snapshot["root"] else "CHILD"
    return "\n".join([
        ISSUE_START, f"**{part} RESPONSIBILITY READ VIEW / V3.2**",
        f"- Authority: `{AUTHORITY}` (not Owner acceptance)",
        f"- Owner origin: `{','.join(i['id'] for i in snapshot['owner_trace']['owner_intents'])}`",
        f"- Original source status: `{','.join(sorted(set(i['original_source_status'] for i in snapshot['owner_trace']['owner_intents'])))}`",
        f"- OR: `{','.join(snapshot['OR_ids'])}`; claims: `{','.join(snapshot['claim_ids'])}`",
        f"- Golden fixtures: `{','.join(snapshot['golden_fixture_ids'])}`",
        f"- Source input: `{snapshot['input_digest']}`",
        f"- Historical facts unreported: `{','.join(snapshot['historical_unreported']) or 'NONE'}`",
        f"- Independent PR qualification: `{snapshot['qualification']['state']}` ({snapshot['qualification']['basis']})",
        f"- Next: `{snapshot['actual_next']}`",
        ISSUE_END,
    ])


def render_pr_block(snapshot: Mapping[str, Any]) -> str:
    pr = snapshot.get("pr")
    _require(pr is not None, "PRODUCT_PR_NOT_OBSERVED")
    return "\n".join([
        START, "**R-PROJECTION DRAFT PR READ VIEW (derived/advisory; no merge permission)**",
        f"- Responsibility: `{snapshot['responsibility']}` / `{snapshot['leaf']}`",
        f"- Owner intents: `{','.join(i['id'] for i in snapshot['owner_trace']['owner_intents'])}`",
        f"- OR/claim: `{','.join(snapshot['OR_ids'])}` / `{','.join(snapshot['claim_ids'])}`",
        f"- Required fixtures: `{','.join(snapshot['golden_fixture_ids'])}`",
        f"- Candidate: `{pr['head_sha']}`; lifecycle: `{pr['lifecycle']}`; binding: `{pr['binding']}`",
        f"- Candidate qualification: `{snapshot['qualification']['state']}` ({snapshot['qualification']['basis']})",
        f"- Input basis: `{snapshot['input_digest']}`",
        f"- Actual next: `{snapshot['actual_next']}`",
        END,
    ])


def reconcile_managed_block(existing: str, replacement: str, *, observed_digest: str,
                            pr: bool = True) -> str:
    """Pure, guarded edit proposal. Never performs a remote write.

    A GitHub provider caller must re-read the COMPLETE body and re-verify
    digest before submission; this guard alone cannot make REST updates atomic.
    """
    _require(digest(existing) == observed_digest, "PROVIDER_BODY_MOVED_RECONCILE")
    start, end = (START, END) if pr else (ISSUE_START, ISSUE_END)
    _require(replacement.startswith(start) and replacement.endswith(end), "INVALID_MANAGED_BLOCK")
    _require(existing.count(start) <= 1 and existing.count(end) <= 1, "DUPLICATE_MANAGED_MARKER")
    if start not in existing and end not in existing:
        return existing.rstrip() + "\n\n" + replacement + "\n"
    _require(start in existing and end in existing and existing.index(start) < existing.index(end),
             "BROKEN_MANAGED_MARKERS")
    begin = existing.index(start)
    finish = existing.index(end, begin) + len(end)
    return existing[:begin] + replacement + existing[finish:]


__all__ = [
    "AUTHORITY", "SCHEMA", "ViewError", "build_views", "digest", "owner_trace",
    "reconcile_managed_block", "render_issue_block", "render_pr_block",
]
