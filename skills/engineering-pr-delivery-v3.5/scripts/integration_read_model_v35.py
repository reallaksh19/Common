"""R2-A: read-only responsibility bridge over the existing V3.5 DELP kernel.

This is NOT a replacement DELP projector, Owner authenticator, GitHub publisher,
reviewer adjudicator, Local authority, or production custody grant.
In particular a passed workflow does not authorize programme IC credit.
"""
from __future__ import annotations

import hashlib
import json
from collections.abc import Iterable, Mapping
from typing import Any

import delp_projection_v35 as DELP


class ReadModelError(ValueError):
    """An unresolvable identity/source boundary must never yield a green read view."""


def _sha(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def _leaf_ref(indexed: Mapping[str, Any], requested: str) -> str:
    # Never join solely on issue number in another repository.
    for ref, node in indexed["nodes"].items():
        if ref == requested and node["kind"] == "LEAF":
            return ref
    raise ReadModelError(f"{requested}: not a declared responsibility LEAF")


def _owner_state(origin: Mapping[str, Any] | None) -> dict[str, Any]:
    """Owner text may be preserved; its original-source authority is not inferred."""
    if origin is None:
        return {"verbatim": None, "first_durable_mirror": None,
                "original_source_status": "UNKNOWN", "authentication": "NOT_PROVEN"}
    if not isinstance(origin, Mapping):
        raise ReadModelError("owner source must be a structured record")
    verbatim = origin.get("verbatim")
    mirror = origin.get("first_durable_mirror")
    if not isinstance(verbatim, str) or not verbatim.strip():
        raise ReadModelError("Owner verbatim missing; cannot silently synthesize it")
    if not isinstance(mirror, str) or not mirror.startswith("https://github.com/"):
        raise ReadModelError("Owner durable mirror locator missing")
    if origin.get("original_source_status") not in ("UNRESOLVED_CHAT_LINK", "UNKNOWN"):
        raise ReadModelError("original Owner authenticity cannot be asserted by fixture")
    return {"verbatim": verbatim, "first_durable_mirror": mirror,
            "original_source_status": origin["original_source_status"],
            "authentication": "MIRROR_UNVERIFIED_ORIGINAL"}


def from_observations(
    graph: Mapping[str, Any],
    responsibility_ref: str,
    ledger: Iterable[Mapping[str, Any]],
    observations: Mapping[str, Mapping[str, Any]],
    *,
    human_titles: Mapping[str, str] | None = None,
    owner_origin: Mapping[str, Any] | None = None,
    topology_observations: Mapping[str, Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    """Compute from actual graph, facts and observations using DELP.project(), not R1 fixture fields.

    Inputs here may be deterministic test observations. Use from_provider() for
    the real read-only GitHub path; neither path independently proves Owner authorship.
    """
    indexed = DELP.validate_graph(graph)
    ref = _leaf_ref(indexed, responsibility_ref)
    repo = indexed["programme"].get("repository")
    if not repo or not isinstance(repo, str):
        raise ReadModelError("approved programme repository identity is required")
    rows = list(ledger)
    derived = DELP.project(
        graph, rows, observations, topology_observations=topology_observations or {}
    )
    leaf = derived["nodes"][ref]
    root_ref = derived["root"]
    parent = derived["nodes"][root_ref]
    owner = _owner_state(owner_origin)
    # Identity, facts, provider observations and Owner receipt (whether authenticated
    # or not) affect this view digest. The digest is integrity, NEVER authority.
    basis = {
        "repository": repo,
        "programme_root": root_ref,
        "responsibility_ref": ref,
        "graph_digest": derived["graph_digest"],
        "input_digest": derived["input_digest"],
        "spec_generation": leaf["identity"]["spec_generation"],
        "contract_digest": leaf["identity"]["contract_digest"],
        "owner": owner,
    }
    digest = _sha(basis)
    candidate = leaf.get("material") or {}
    candidate_sha = candidate.get("candidate_sha")
    _, human_parent = DELP.split_title((human_titles or {}).get(root_ref, ""))
    _, human_leaf = DELP.split_title((human_titles or {}).get(ref, ""))
    titles = {
        "parent_issue": DELP.render_title(parent["title_prefix"], human_parent),
        "child_issue": DELP.render_title(leaf["title_prefix"], human_leaf),
        # Candidate status is separate from semantic acceptance and CI verification.
        "draft_pr": (
            f"[{root_ref}→{ref} PR:{candidate.get('primary_pr') or 'UNKNOWN'} "
            f"HEAD:{(candidate_sha or 'UNKNOWN')[:12]} "
            "CHECKS:UNKNOWN NO_MERGE_AUTHORITY] Candidate evidence"
        ),
    }
    accepted, rejected = DELP.partition_ledger(indexed, rows)
    evidence_sources = [row.get("_source") for row in accepted.get(ref, ())]
    live_next = leaf.get("actual_next") or {}
    actual_next = live_next.get("action") if isinstance(live_next, Mapping) else None
    if not actual_next:
        raise ReadModelError("DELP projection did not resolve an actual-next action")
    prefix = f"BASIS_SHA256: {digest}\\nSOURCE: DELP_PROJECTED_READ_ONLY\\n"
    identity = (
        f"REPO: {repo}\\nROOT: {root_ref}\\nLEAF: {ref}\\n"
        f"GRAPH_DIGEST: {derived['graph_digest']}\\n"
        f"CONTRACT_DIGEST: {leaf['identity']['contract_digest'] or 'UNKNOWN'}\\n"
        f"SPEC_GENERATION: {leaf['identity']['spec_generation'] or 'UNKNOWN'}\\n"
        f"CANDIDATE_SHA: {candidate_sha or 'UNKNOWN'}\\n"
        f"OWNER_AUTH: {owner['authentication']}\\n"
        f"NEXT: {actual_next}\\n"
    )
    # Pure views only: actual GitHub status/title writers belong to the separately
    # governed R3/R4 publication phase, not this read-only R2 adapter.
    bodies = {
        "parent_issue": prefix + identity + f"STATUS: {parent['state']}\\nPROGRESS: {parent['progress']}\\n",
        "child_issue": prefix + identity + f"STATUS: {leaf['state']}\\nPROGRESS: {leaf['progress']}\\nEVIDENCE_SOURCES: {evidence_sources}\\n",
        "draft_pr": prefix + identity + "CHECKS: UNKNOWN_UNOBSERVED\\nMERGE_AUTHORITY: NONE_DERIVED\\n",
        "owner_report": prefix + identity + "IC_ACCEPTANCE: UNKNOWN_NOT_DERIVED\\n",
        "task_evidence_start": prefix + identity + "TEMPLATE_ONLY: NO_PUBLICATION_ASSERTED\\n",
        "task_evidence_end": prefix + identity + "TEMPLATE_ONLY: NO_PUBLICATION_ASSERTED\\n",
        "handover_prompt": prefix + identity + f"OWNER_VERBATIM: {owner['verbatim'] or 'UNKNOWN'}\\nEVIDENCE_SOURCES: {evidence_sources}\\n",
        "agent_metrics": prefix + identity + "AGENT_HEALTH: UNVERIFIED_ADVISORY\\nPROGRESS_EFFECT: NONE\\n",
        "reviewer_checklist": prefix + identity + "REVIEW: NOT_OBSERVED\\nINDEPENDENCE: NOT_PROVEN\\n",
    }
    return {
        "schema": "v3.5-r2-read-only-v1",
        "mode": "DELP_SOURCE_PROJECTED_READ_ONLY",
        "basis_sha256": digest,
        "source_identity": basis,
        "titles": titles,
        "surfaces": bodies,
        "state": leaf["state"],
        "progress": leaf["progress"],
        "actual_next": live_next,
        "candidate_sha": candidate_sha,
        "accepted_evidence_sources": evidence_sources,
        "rejected_facts": rejected,
        "owner": owner,
        "ci_qualification": "UNKNOWN_UNOBSERVED",
        "integration_acceptance": "UNKNOWN_NOT_DERIVED",
        "custody_grant": "NOT_PROVEN_NO_AUTHORITY",
    }


def from_provider(
    graph: Mapping[str, Any],
    responsibility_ref: str,
    transport: Any,
    *,
    human_titles: Mapping[str, str] | None = None,
    owner_origin: Mapping[str, Any] | None = None,
    topology_observations: Mapping[str, Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    """READ-ONLY GitHub observation: calls real DELP ledger/observation/project paths.

    The caller supplies an approved graph and caller-owned Owner receipt. This
    API never patches issues/PRs and does not independently approve either source.
    """
    repository = getattr(transport, "repository", None)
    if not repository:
        raise ReadModelError("authenticated provider repository identity required")
    DELP.require_repository_match(graph, repository, live=True)
    ledger = DELP.ledger_from_github(transport, graph)
    observed = DELP.observe_github(transport, graph)
    return from_observations(
        graph, responsibility_ref, ledger, observed, human_titles=human_titles,
        owner_origin=owner_origin, topology_observations=topology_observations,
    )
