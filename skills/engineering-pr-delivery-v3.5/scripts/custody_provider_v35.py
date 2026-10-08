"""Observe one candidate native custody source from an immutable GitHub snapshot.

This is provider *visibility*, not approval of the selected repository/ref,
executor authentication, an active grant, fact fencing or permission to merge.
The Owner/Local selection and execution authority remain separate inputs.
"""
from __future__ import annotations

import re
from typing import Any, Mapping

from custody_source_v35 import assess_scoped_native_source

_SHA = re.compile(r"^[0-9a-f]{40}$")
_REF = re.compile(r"^[A-Za-z0-9_][A-Za-z0-9_.\-/]*$")
_EP = re.compile(r"^(?:EP-[A-Za-z0-9][A-Za-z0-9._-]*|EP\.(?:[1-9][0-9]*|REPO|INTERNAL)\.[1-9][0-9]*)$")
_LEASE = re.compile(r"^(?:LEASE-[A-Za-z0-9][A-Za-z0-9._-]*|LEASE\.(?:[1-9][0-9]*|REPO|INTERNAL)\.[1-9][0-9]*)$")


def _not_proven(leaf_ref: str, reason: str) -> dict[str, Any]:
    return {
        "status": "SOURCE_NOT_PROVEN",
        "authority": "NO_CUSTODY_AUTHORITY",
        "leaf": leaf_ref,
        "reason": reason,
    }


def observe_scoped_native_candidate(
    provider: Any,
    graph: Mapping[str, Any],
    leaf_ref: str,
    selector: Mapping[str, Any] | None,
) -> dict[str, Any]:
    """Provider-read native STATE/EP/LEASE for ONE leaf at one GitHub SHA.

    selector is merely a lookup request; its origin/Owner approval is NOT
    authenticated by this observer. get_commit_sha and read_native_yaml_at_sha
    must be implemented by the trusted GitHub transport, never executor facts.
    """
    if not isinstance(graph, Mapping) or not isinstance(graph.get("programme"), Mapping):
        return _not_proven(leaf_ref, "GRAPH_UNAVAILABLE")
    repo = graph["programme"].get("repository")
    if (
        not isinstance(repo, str)
        or not isinstance(selector, Mapping)
        or selector.get("repository") != repo
        or getattr(provider, "repository", None) != repo
    ):
        return _not_proven(leaf_ref, "SOURCE_REPOSITORY_MISMATCH")
    ref = selector.get("ref")
    if (
        not isinstance(ref, str)
        or not _REF.fullmatch(ref)
        or ".." in ref
        or ref.endswith("/")
        or ref.startswith("/")
    ):
        return _not_proven(leaf_ref, "SOURCE_REF_INVALID")
    try:
        head = provider.get_commit_sha(ref)
    except (OSError, LookupError, ValueError, RuntimeError):
        return _not_proven(leaf_ref, "SOURCE_REF_UNAVAILABLE")
    if not isinstance(head, str) or not _SHA.fullmatch(head):
        return _not_proven(leaf_ref, "SOURCE_COMMIT_UNOBSERVED")

    # Every read is pinned to the same immutable commit. Do not fetch each
    # document at a moving branch ref or infer lease scope from a filename.
    try:
        state = provider.read_native_yaml_at_sha("relay/STATE.yaml", head)
        execution = state.get("execution") if isinstance(state, Mapping) else None
        if not isinstance(execution, Mapping):
            return _not_proven(leaf_ref, "SOURCE_STATE_INVALID")
        ep_id = execution.get("ep")
        lease_id = execution.get("lease")
        if (
            not isinstance(ep_id, str)
            or not _EP.fullmatch(ep_id)
            or not isinstance(lease_id, str)
            or not _LEASE.fullmatch(lease_id)
        ):
            return _not_proven(leaf_ref, "SOURCE_NATIVE_ID_INVALID")
        ep_path = f"relay/WORK/{ep_id}.yaml"
        lease_path = f"relay/LEASES/{lease_id}.yaml"
        ep = provider.read_native_yaml_at_sha(ep_path, head)
        lease = provider.read_native_yaml_at_sha(lease_path, head)
        end = provider.get_commit_sha(ref)
    except (OSError, LookupError, ValueError, RuntimeError, AttributeError, TypeError):
        return _not_proven(leaf_ref, "SOURCE_PROVIDER_UNAVAILABLE")
    if end != head:
        return _not_proven(leaf_ref, "SOURCE_REF_MOVED_DURING_READ")

    result = assess_scoped_native_source(
        graph, leaf_ref,
        {
            "provider": "GITHUB",
            "repository": repo,
            "revision_sha": head,
            "state_path": "relay/STATE.yaml",
            "ep_path": ep_path,
            "lease_path": lease_path,
        },
        state, ep, lease,
    )
    if result["status"] != "SCOPE_MATCHED_UNVERIFIED":
        return result
    # Provider readback proves a snapshot was observed. It does not prove the
    # selection was authorized or that an impersonating same-login agent is safe.
    return {
        **result,
        "provider_observation": {
            "repository": repo,
            "selected_ref": ref,
            "observed_sha": head,
            "ref_stable_during_read": True,
        },
        "selector_approval": "NOT_PROVEN",
        "custody_grant_authority": "NOT_PROVEN",
    }
