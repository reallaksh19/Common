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
BASIS_SCHEMA = "relay-v3.2-responsibility-basis-v1"
BASIS_AUTHORITY = "DERIVED_RESPONSIBILITY_BASIS_ONLY"
START = "<!-- relay-v32:pr-read-view:start -->"
END = "<!-- relay-v32:pr-read-view:end -->"
ISSUE_START = "<!-- relay-v32:issue-read-view:start -->"
ISSUE_END = "<!-- relay-v32:issue-read-view:end -->"
_SHA = re.compile(r"^[0-9a-f]{40}$", re.IGNORECASE)
_PHASE = re.compile(r"^C[0-9]+(?:-[A-Z])?$")
_LIFECYCLES = frozenset({"DRAFT", "OPEN", "MERGED", "CLOSED"})
OWNER_UNKNOWN = "UNRESOLVED_CHAT_MESSAGE_LINK"
HUMAN_SUFFIX = " — "

# Exact quotations frozen independently in C0 oracle commit 80a9c03.
# Original conversation permalink remains UNKNOWN: this proves frozen-mirror
# integrity only, not authenticity of the original ChatGPT message.
FROZEN_OWNER_VERBATIM = {
    "OI-718-03": "full of stats...\ni dont see any integration on github issue decompostion, issue title scorboard, task evidence, handover prompt and agent metric which is the core...\ni also don't see smart title in issue and draft... I also donot see \"My intent\" or\"Wowner inent\" presenvation i parent issue along with source links and golden fixtures which is mandatory.",
    "OI-718-04": "update git hub issue... walk the talk,  i.e, show how your implemented cycle will show in issue/OR/task evidence etc.... ensure that stress check achieves the same ie, self run via module once coded and achive same..."
}


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
    _require({i.get("id") for i in intents if isinstance(i, Mapping)} ==
             set(FROZEN_OWNER_VERBATIM) and len(intents) == len(FROZEN_OWNER_VERBATIM),
             "OWNER_INTENT_SET_UNTRUSTED")
    linked = []
    for intent in intents:
        _require(isinstance(intent, Mapping) and bool(intent.get("verbatim")), "OWNER_QUOTATION_MISSING")
        _require(intent["verbatim"] == FROZEN_OWNER_VERBATIM[intent["id"]],
                 "PRECOMMITTED_OWNER_QUOTE_TAMPERED")
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
    # The selected OR must own this exact leaf's claims, not merely any valid
    # programme claim. Unknown provenance cannot silently borrow sibling truth.
    expected_selected_claims = set(owner.get("selected_claims") or [])
    if expected_selected_claims:
        _require(all(set(a["claim_ids"]) == expected_selected_claims for a in accepted),
                 "SELECTED_OR_CLAIM_OWNERSHIP_DRIFT")
    _require(any(any(x["id"] in o["OR_ids"] for o in linked) for x in accepted),
             "SELECTED_OR_NOT_CONNECTED_TO_OWNER")
    return {"owner_intents": linked, "selected_OR": accepted}


def _independent_qualification(observation: Any, head_sha: str | None,
                               responsibility: str, repository: str) -> dict[str, str]:
    if observation is None:
        return {"state": "UNPROVEN", "basis": "NOT_OBSERVED"}
    _require(isinstance(observation, Mapping), "INVALID_QUALIFIER")
    _require(observation.get("authority") == "DERIVED_OBSERVATION_ONLY", "QUALIFIER_AUTHORITY_INVALID")
    _require(observation.get("schema") == "relay-v3.2-qualification-observation-v1",
             "QUALIFIER_SCHEMA_MISMATCH")
    _require(observation.get("responsibility") == responsibility,
             "QUALIFIER_WRONG_RESPONSIBILITY")
    _require(observation.get("repository") == repository,
             "QUALIFIER_WRONG_REPOSITORY")
    qhead = observation.get("observed_candidate_sha")
    expected_candidate = observation.get("expected_candidate_sha")
    _require(isinstance(expected_candidate, str) and bool(_SHA.fullmatch(expected_candidate)),
             "QUALIFIER_EXPECTED_SHA_INVALID")
    _require(qhead is None or qhead == expected_candidate or observation.get("overall") == "UNPROVEN",
             "QUALIFIER_INCOHERENT_EXPECTED_OBSERVED_HEAD")
    _require(qhead is None or _SHA.fullmatch(str(qhead)) is not None, "QUALIFIER_INVALID_SHA")
    state = observation.get("overall")
    _require(state in {"PROVEN", "UNPROVEN", "UNKNOWN"}, "QUALIFIER_INVALID_VERDICT")
    if not head_sha or qhead != head_sha:
        return {"state": "UNPROVEN", "basis": "STALE_OR_UNBOUND_QUALIFICATION"}
    return {"state": str(state), "basis": "INDEPENDENT_OBSERVATION_ONLY"}


def build_responsibility_basis(
    graph: Mapping[str, Any],
    owner: Mapping[str, Any],
    *,
    selected_leaf: str,
    phase: str = "C4",
    ledger: list[Mapping[str, Any]] | None = None,
    observations: Mapping[str, Mapping[str, Any]] | None = None,
    draft_pr: Mapping[str, Any] | None = None,
    qualification: Mapping[str, Any] | None = None,
    frozen_basis: Mapping[str, Any] | None = None,
    human_titles: Mapping[str, str] | None = None,
    title_contract: str = "C4-S6",
) -> dict[str, Any]:
    """Single canonical source-bound responsibility basis derived from real graph and DELP."""
    _require(bool(_PHASE.fullmatch(phase)), "UNRELEASED_PHASE")
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
    proof = owner_trace(
        {**owner, "selected_claims": sorted(raw_node.get("owns_claims") or [])},
        required_claims=claim_ids, responsibility_id=identity,
    )
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
        repository_short = graph["programme"]["repository"].rsplit("/", 1)[-1]
        bound = raw_node.get("primary_pr") == f"{repository_short}#{number}"
        observed_candidate = (observations or {}).get(selected_leaf, {}).get("candidate_sha")
        _require(observed_candidate is None or observed_candidate == sha,
                 "SOURCE_CANDIDATE_HEAD_MISMATCH")
        pr_details = {"number": number, "head_sha": sha,
                      "lifecycle": lifecycle, "binding": "BOUND" if bound else "UNBOUND_ADVISORY"}
    candidate = pr_details["head_sha"] if pr_details else None
    q = _independent_qualification(qualification, candidate, selected_leaf,
                                   graph["programme"]["repository"])
    _require(not pr_details or not pr_details["binding"] == "UNBOUND_ADVISORY" or q["state"] != "PROVEN",
             "UNBOUND_PR_CANNOT_ACQUIRE_QUALIFICATION")
    _require(q["state"] != "PROVEN", "PROVEN_REQUIRES_REAL_ASSESSOR_EXECUTION")

    reserve = next(n.get("reserve_weight", 0) for n in graph["nodes"] if n["ref"] == root_ref)
    root = nodes[root_ref]
    child = nodes[selected_leaf]
    historical_unreported = [
        n["ref"] for n in graph["nodes"]
        if n["kind"] == "LEAF" and n.get("primary_pr") and
        (observations or {}).get(n["ref"], {}).get("pr_state") == "MERGED" and
        nodes[n["ref"]]["progress"]["P"] == 0 and nodes[n["ref"]]["progress"]["E"] == 0 and
        nodes[n["ref"]]["state"] in {"UNMATERIALIZED", "EVIDENCE_GAP"}
    ]
    actual_next = (
        "MATERIALIZE_FACTS_OR_CONTRACT" if child["state"] == "UNMATERIALIZED" else
        "RELEASE_AND_BIND_PRODUCT_PR" if not raw_node.get("primary_pr") else
        "RECONCILE_CURRENT_FACTS_AND_QUALIFICATION"
    )

    owner_intents_list = proof["owner_intents"]
    owner_statuses = sorted(set(i["original_source_status"] for i in owner_intents_list))
    single_owner_status = owner_statuses[0] if len(owner_statuses) == 1 else "MIXED"

    digests = {
        "graph": delp.canonical_digest(graph) if hasattr(delp, "canonical_digest") else digest(graph),
        "plan": projection["plan_digest"],
        "input": projection["input_digest"],
        "provider": digest({"observations": observations or {}, "selected_leaf": (observations or {}).get(selected_leaf)}),
    }
    moved_axes = []
    if frozen_basis is not None:
        _require(isinstance(frozen_basis, Mapping), "FROZEN_BASIS_INVALID")
        _require(set(frozen_basis) == set(digests), "FROZEN_SOURCE_BASIS_INCOMPLETE")
        _require(all(isinstance(frozen_basis[k], str)
                     and frozen_basis[k].startswith("sha256:")
                     and len(frozen_basis[k]) == 71 for k in digests),
                 "FROZEN_SOURCE_BASIS_INVALID")
        for k in ("graph", "plan", "input", "provider"):
            if frozen_basis[k] != digests[k]:
                moved_axes.append(k)
    # A pure formatter cannot authenticate GitHub, current default-branch
    # graph custody, or provider double-read. Only the separately governed
    # native C6 handover can return CURRENT_READ_ONLY after those checks.
    currentness = "RECONCILE_REQUIRED" if moved_axes else "UNVERIFIED_LOCAL_INPUT"

    basis = {
        "schema": BASIS_SCHEMA,
        "authority": BASIS_AUTHORITY,
        "provenance": {
            "owner_trace": proof,
            "OR_ids": sorted({r["id"] for r in proof["selected_OR"]}),
            "golden_fixture_ids": sorted({f for r in proof["selected_OR"] for f in r["fixture_ids"]}),
        },
        "programme": {
            "repository": graph["programme"]["repository"],
            "root": root_ref,
            "base_ref": graph["programme"].get("base_ref", "main"),
            "owner_intent_digest": digest({
                "owner_intents": owner["owner_intents"], "requirements": owner["requirements"],
                "released_proposal_digest": owner["released_proposal_digest"],
            }),
            "owner_source_status": single_owner_status,
        },
        "plan": {
            "graph_digest": digests["graph"],
            "plan_digest": projection["plan_digest"],
            "released_proposal_digest": release.get("released_proposal_digest"),
            "reserve_weight": reserve,
        },
        "responsibility": {
            "id": identity,
            "leaf": selected_leaf,
            "work_class": raw_node.get("work_class", "PRODUCT"),
            "claim_ids": sorted(raw_node.get("owns_claims") or []),
            "semantic_units": raw_node.get("units") or [],
            "depends_on": raw_node.get("depends_on") or [],
            "weight": raw_node.get("weight"),
        },
        "material": {
            "primary_pr": raw_node.get("primary_pr"),
            "observed_pr": pr_details,
            "candidate_sha": candidate,
            "base_sha": (observations or {}).get(selected_leaf, {}).get("base_sha"),
            "lifecycle": pr_details["lifecycle"] if pr_details else "UNMATERIALIZED",
            "binding": pr_details["binding"] if pr_details else "UNBOUND",
        },
        "evidence": {
            "delp_input_digest": projection["input_digest"],
            "fact_count": len(ledger or []),
            "rejected_fact_count": len(projection.get("rejected_facts") or []),
            "historical_unreported": historical_unreported,
        },
        "qualification": {
            "state": q["state"],
            "basis": q["basis"],
            "expected_candidate_sha": (qualification or {}).get("expected_candidate_sha"),
            "observed_candidate_sha": (qualification or {}).get("observed_candidate_sha"),
        },
        "projection": {
            "leaf_state": child["state"],
            "leaf_progress": {"P": child["progress"]["P"], "E": child["progress"]["E"]},
            "root_progress": {"D": root["progress"]["D"], "E": root["progress"]["E"]},
            "actual_next": actual_next,
        },
        "provider": {
            "observed_leaf": (observations or {}).get(selected_leaf, {}),
        },
        "handover": {
            "currentness": currentness,
            "moved_axes": moved_axes,
            "frozen_basis": dict(frozen_basis) if frozen_basis is not None else None,
            "verification": "CALLER_INPUT_NOT_AUTHENTICATED_BY_PURE_VIEW",
        },
        "authority_effects": [],
    }
    basis["basis_digest"] = digest(basis)
    return basis


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
    title_contract: str = "C0",
) -> dict[str, Any]:
    """Generate all currently released R-PROJECTION read views at one basis.

    A material candidate not yet bound in released graph is shown as advisory
    and does NOT qualify/complete the leaf. The input observer must be trusted
    by the caller; this pure function cannot authenticate GitHub provider data.
    """
    _require(bool(_PHASE.fullmatch(phase)), "UNRELEASED_PHASE")
    _require(title_contract in {"C0", "C4-S6"}, "UNRELEASED_TITLE_CONTRACT")
    _require(isinstance(human_titles, Mapping), "HUMAN_TITLES_MISSING")
    # One source projection and one canonical basis drive every read view.
    # Do not recompute DELP or independently reconstruct evidence/material.
    canonical_basis = build_responsibility_basis(
        graph, owner, selected_leaf=selected_leaf, phase=phase,
        ledger=ledger, observations=observations, draft_pr=draft_pr,
        qualification=qualification, human_titles=human_titles,
        title_contract=title_contract,
    )
    root_ref = canonical_basis["programme"]["root"]
    identity = canonical_basis["responsibility"]["id"]
    pr_details = canonical_basis["material"]["observed_pr"]
    q = {
        "state": canonical_basis["qualification"]["state"],
        "basis": canonical_basis["qualification"]["basis"],
    }
    proof = canonical_basis["provenance"]["owner_trace"]
    reserve = canonical_basis["plan"]["reserve_weight"]
    raw_node = {"primary_pr": canonical_basis["material"]["primary_pr"]}
    root = {"progress": canonical_basis["projection"]["root_progress"]}
    child = {
        "progress": canonical_basis["projection"]["leaf_progress"],
        "state": canonical_basis["projection"]["leaf_state"],
    }
    number = _number(selected_leaf)
    parent_number = _number(root_ref)
    historical_unreported = canonical_basis["evidence"]["historical_unreported"]
    facts_label = "FACTS UNREPORTED" if historical_unreported else "FACTS RECONCILED"
    # DELP's actual root roll-up has D/E, NOT P. Leaf execution has P/E.
    # Frozen C0 oracle/title output must remain byte-identical. In C4-S6
    # only these source-derived numbers enter the smart issue title; no
    # input-supplied title/percentage has authority.
    parent_progress = ""
    child_progress = ""
    if title_contract == "C4-S6":
        rp, cp = root["progress"], child["progress"]
        _require(all(type(rp.get(k)) is int and 0 <= rp[k] <= 100 for k in ("D", "E")),
                 "INVALID_DELP_ROOT_PROGRESS")
        _require(all(type(cp.get(k)) is int and 0 <= cp[k] <= 100 for k in ("P", "E")),
                 "INVALID_DELP_LEAF_PROGRESS")
        parent_progress = f" · D{rp['D']}/E{rp['E']}"
        child_progress = f" · P{cp['P']}/E{cp['E']}"
    parent_prefix = (
        f"🟡 [{parent_number}] NEXT #{number}/{phase}{parent_progress} · RESERVE{reserve} · {facts_label}"
    )
    leaf_prefix = (
        f"🟡 [{parent_number}›{number}] {identity} · {phase}{child_progress} · NO PRODUCT PR · CODE HELD"
        if not raw_node.get("primary_pr")
        else f"🟡 [{parent_number}›{number}] {identity} · {phase}{child_progress} · PR#{_number(raw_node['primary_pr'])} · {child['state']}"
    )
    parent_title = _suffix_title(parent_prefix, human_titles[root_ref])
    child_title = _suffix_title(leaf_prefix, human_titles[selected_leaf])
    pr_title = None
    if pr_details:
        pr_prefix = (f"🟡 [{parent_number}›{number}] {pr_details['lifecycle']} · VIEW-PR · "
                     f"HEAD:{pr_details['head_sha'][:7]} · Q:{q['state']}")
        pr_title = _suffix_title(pr_prefix, human_titles["PR"])
    or_ids = canonical_basis["provenance"]["OR_ids"]
    fixture_ids = canonical_basis["provenance"]["golden_fixture_ids"]
    actual_next = canonical_basis["projection"]["actual_next"]
    basis = {
        "graph": canonical_basis["plan"]["plan_digest"],
        "delp_input": canonical_basis["evidence"]["delp_input_digest"],
        "owner_intent_requirements": canonical_basis["programme"]["owner_intent_digest"],
        "selected_leaf": selected_leaf, "phase": phase,
        "title_contract": title_contract,
        "draft_pr": pr_details, "qualifier": dict(qualification or {}),
        "human_titles": {k: human_titles[k] for k in (root_ref, selected_leaf) if k in human_titles},
        "human_pr_title": human_titles.get("PR") if pr_details else None,
    }
    snapshot = {
        "schema": SCHEMA, "authority": AUTHORITY, "input_digest": digest(basis),
        "delp_input_digest": canonical_basis["evidence"]["delp_input_digest"],
        "plan_digest": canonical_basis["plan"]["plan_digest"],
        "root": root_ref, "leaf": selected_leaf, "responsibility": identity,
        "claim_ids": canonical_basis["responsibility"]["claim_ids"],
        "owner_trace": proof, "OR_ids": or_ids, "golden_fixture_ids": fixture_ids,
        "root_reserve": reserve, "historical_unreported": historical_unreported,
        "title_contract": title_contract,
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
    snapshot["responsibility_basis"] = canonical_basis
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


def inspect_managed_block(existing: str, expected: str, *, pr: bool = False) -> str:
    """Check the ENTIRE expected managed block, not just marker presence."""
    _require(isinstance(existing, str) and isinstance(expected, str),
             "MANAGED_CONTENT_MUST_BE_TEXT")
    start, end = (START, END) if pr else (ISSUE_START, ISSUE_END)
    _require(expected.startswith(start) and expected.endswith(end),
             "INVALID_EXPECTED_MANAGED_BLOCK")
    left, right = existing.count(start), existing.count(end)
    if not left and not right:
        return "MISSING"
    if left != 1 or right != 1:
        return "CORRUPT_MARKERS"
    i, j = existing.index(start), existing.index(end)
    if i >= j:
        return "CORRUPT_MARKERS"
    actual = existing[i:j + len(end)]
    return "MATCH" if actual == expected else "DRIFT"


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
    "AUTHORITY", "SCHEMA", "BASIS_SCHEMA", "BASIS_AUTHORITY", "ViewError",
    "build_views", "build_responsibility_basis", "digest", "owner_trace",
    "inspect_managed_block", "reconcile_managed_block", "render_issue_block", "render_pr_block",
]
