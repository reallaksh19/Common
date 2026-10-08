"""Pure scope assessment for a prospective native V3.5 custody source.

This module NEVER authenticates a provider, acquires a lease, authorizes an
executor, fences facts, or reports CustodySafe. It only rejects scope-mismatched
native STATE/EP/LEASE records before a separate provider adapter can consider
them for one declared Responsibility leaf.

Authority: DERIVED_SCOPE_ASSESSMENT_ONLY; no I/O, time or mutation.
"""
from __future__ import annotations

import re
from datetime import datetime
from typing import Any, Mapping

_SHA = re.compile(r"^[0-9a-f]{40}$")
_REPO = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
_STATUS = "SCOPE_MATCHED_UNVERIFIED"
_UNKNOWN = "SOURCE_NOT_PROVEN"


def _issue_number(ref: Any) -> int | None:
    if not isinstance(ref, str) or "#" not in ref:
        return None
    tail = ref.rsplit("#", 1)[1]
    return int(tail) if tail.isdecimal() and int(tail) > 0 else None


def _not_proven(leaf: str, reason: str) -> dict[str, Any]:
    return {
        "status": _UNKNOWN,
        "authority": "NO_CUSTODY_AUTHORITY",
        "leaf": leaf,
        "reason": reason,
    }


def _native_parent_matches(parent: Any, repository: str, number: int) -> bool:
    return (
        isinstance(parent, Mapping)
        and parent.get("provider") == "GITHUB"
        and str(parent.get("repository") or "").lower() == repository.lower()
        and type(parent.get("number")) is int
        and parent["number"] == number
    )


def _valid_grant_time(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    try:
        when = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return when.tzinfo is not None and when.utcoffset() is not None


def assess_scoped_native_source(
    graph: Mapping[str, Any],
    leaf_ref: str,
    source: Mapping[str, Any] | None,
    state: Mapping[str, Any] | None,
    ep: Mapping[str, Any] | None,
    lease: Mapping[str, Any] | None,
) -> dict[str, Any]:
    """Assess ONE graph leaf; never apply a custody tuple across sibling leaves.

    source is a *claimed* immutable provider locator. Its structure is checked,
    but actual provider retrieval, signature/authentication, currentness and
    revocation MUST be independently established by the B2.3-C adapter.
    Even a match is therefore SCOPE_MATCHED_UNVERIFIED, never a live grant.
    """
    if not isinstance(graph, Mapping):
        return _not_proven(str(leaf_ref), "GRAPH_UNAVAILABLE")
    programme = graph.get("programme")
    nodes = graph.get("nodes")
    if not isinstance(programme, Mapping) or not isinstance(nodes, list):
        return _not_proven(str(leaf_ref), "GRAPH_UNAVAILABLE")
    repository = programme.get("repository")
    root_ref = programme.get("root")
    if not isinstance(repository, str) or not _REPO.fullmatch(repository):
        return _not_proven(str(leaf_ref), "PROGRAMME_REPOSITORY_UNDECLARED")
    root_number = _issue_number(root_ref)
    if root_number is None:
        return _not_proven(str(leaf_ref), "PROGRAMME_ROOT_UNDECLARED")
    leaves = [
        n for n in nodes
        if isinstance(n, Mapping) and n.get("ref") == leaf_ref
        and n.get("kind") == "LEAF"
    ]
    if len(leaves) != 1:
        return _not_proven(str(leaf_ref), "LEAF_NOT_UNIQUELY_DECLARED")
    leaf = leaves[0]
    number = _issue_number(leaf_ref)
    responsibility_id = leaf.get("responsibility_id")
    if number is None or not isinstance(responsibility_id, str) or not responsibility_id:
        return _not_proven(str(leaf_ref), "LEAF_IDENTITY_UNDECLARED")
    if not all(isinstance(v, Mapping) for v in (source, state, ep, lease)):
        return _not_proven(leaf_ref, "NATIVE_SOURCE_MISSING")

    if (
        source.get("provider") != "GITHUB"
        or str(source.get("repository") or "").lower() != repository.lower()
        or not isinstance(source.get("revision_sha"), str)
        or not _SHA.fullmatch(source["revision_sha"])
        or source.get("state_path") != "relay/STATE.yaml"
    ):
        return _not_proven(leaf_ref, "SOURCE_LOCATOR_MISMATCH")

    execution = state.get("execution")
    if not isinstance(execution, Mapping) or execution.get("lifecycle") != "ACTIVE":
        return _not_proven(leaf_ref, "STATE_NOT_ACTIVE")
    ep_id = execution.get("ep")
    lease_id = execution.get("lease")
    if (
        not isinstance(ep_id, str) or not ep_id
        or not isinstance(lease_id, str) or not lease_id
        or source.get("ep_path") != f"relay/WORK/{ep_id}.yaml"
        or source.get("lease_path") != f"relay/LEASES/{lease_id}.yaml"
    ):
        return _not_proven(leaf_ref, "NATIVE_PATH_MISMATCH")
    if ep.get("id") != ep_id:
        return _not_proven(leaf_ref, "EP_ID_MISMATCH")
    if not _native_parent_matches(ep.get("parent_issue"), repository, number):
        return _not_proven(leaf_ref, "EP_LEAF_SCOPE_MISMATCH")
    if not _native_parent_matches(ep.get("programme_parent"), repository, root_number):
        return _not_proven(leaf_ref, "EP_PROGRAMME_SCOPE_MISMATCH")

    plan_basis = ep.get("implementation_plan_basis")
    if isinstance(plan_basis, Mapping):
        declared = plan_basis.get("responsibility_basis_ref")
        if declared is not None and declared not in (leaf_ref, responsibility_id):
            return _not_proven(leaf_ref, "EP_RESPONSIBILITY_BASIS_MISMATCH")

    basis = lease.get("basis")
    custody = lease.get("custody")
    executor = lease.get("executor")
    epoch = execution.get("custody_epoch")
    if (
        lease.get("state") != "ACTIVE"
        or lease.get("id") != lease_id
        or not isinstance(basis, Mapping) or basis.get("ep_id") != ep_id
        or not isinstance(custody, Mapping)
        or type(epoch) is not int or epoch < 1
        or type(custody.get("epoch")) is not int or custody["epoch"] != epoch
        or execution.get("route") != f"SERIAL:{ep_id}"
        or lease.get("route") != execution.get("route")
        or not isinstance(executor, Mapping)
        or not isinstance(executor.get("id"), str) or not executor["id"].strip()
        or not _valid_grant_time(custody.get("granted_at"))
    ):
        return _not_proven(leaf_ref, "ACTIVE_BINDING_INVALID")
    lease_scope = lease.get("scope")
    if lease_scope is not None and (
        not isinstance(lease_scope, Mapping)
        or lease_scope.get("ep_or_task") not in (ep_id, responsibility_id, leaf_ref)
    ):
        return _not_proven(leaf_ref, "LEASE_SCOPE_MISMATCH")

    # Never label this result VERIFIED, AUTHORIZED, CURRENT or CustodySafe.
    # The supplied source locator and native documents have not been read
    # and authenticated by the independent provider/currentness adapter.
    return {
        "status": _STATUS,
        "authority": "DERIVED_SCOPE_ASSESSMENT_ONLY",
        "leaf": leaf_ref,
        "responsibility_id": responsibility_id,
        "source_revision_sha": source["revision_sha"],
        "ep": ep_id,
        "lease": lease_id,
        "custody_epoch": epoch,
        "asserted_granted_at": custody["granted_at"],
        "provider_authentication": "NOT_PROVEN",
        "source_currentness": "NOT_PROVEN",
    }
