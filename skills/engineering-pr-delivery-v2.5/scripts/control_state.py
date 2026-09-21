from __future__ import annotations

from pathlib import Path
from typing import Any

from relaylib import load_yaml


OPEN_STATE = "OPEN"


def control_obligations(state: dict[str, Any]) -> list[dict[str, Any]]:
    return [x for x in (state.get("control_obligations") or []) if isinstance(x, dict)]


def open_obligations(state: dict[str, Any], kind: str | None = None) -> list[dict[str, Any]]:
    out = []
    for item in control_obligations(state):
        if item.get("state") != OPEN_STATE:
            continue
        if kind is not None and item.get("kind") != kind:
            continue
        out.append(item)
    return out


def obligation_map(state: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {str(x.get("id")): x for x in control_obligations(state) if x.get("id")}


def boundary_blockers(state: dict[str, Any], boundary: str) -> list[dict[str, Any]]:
    return [
        x for x in open_obligations(state, "DEFERRED_VALIDATION")
        if boundary in (x.get("must_resolve_before") or [])
    ]


def active_executor(state: dict[str, Any], route_key: str) -> dict[str, Any] | None:
    leases = ((state.get("execution_custody") or {}).get("leases") or [])
    matches = [
        x for x in leases
        if isinstance(x, dict)
        and x.get("state") == "ACTIVE"
        and str(x.get("route_key")) == str(route_key)
    ]
    return matches[0] if len(matches) == 1 else None


def _owner_decisions(root: Path) -> list[tuple[Path, dict[str, Any]]]:
    base = root / "agents/relay/roadmap/owner-decisions"
    if not base.exists():
        return []
    out = []
    for path in sorted(list(base.glob("*.yaml")) + list(base.glob("*.yml"))):
        try:
            out.append((path, load_yaml(path)))
        except Exception:
            continue
    return out


def _repository_identity(state: dict[str, Any]) -> set[str]:
    repo = state.get("repository") or {}
    return {
        str(x).strip()
        for x in (repo.get("remote"), repo.get("name"))
        if str(x or "").strip()
    }


def resolve_execution_override(
    root: Path,
    state: dict[str, Any],
    *,
    branch: str,
    route_key: str | None,
) -> tuple[dict[str, Any] | None, list[str]]:
    """Resolve exactly one APPLIED bounded Owner execution override.

    The override is valid only while all referenced PEND-* obligations exist,
    remain OPEN, and are DEFERRED_VALIDATION obligations. It never resolves or
    marks those obligations PASS.
    """
    matches = []
    obligations = obligation_map(state)
    repo_ids = _repository_identity(state)

    for path, odr in _owner_decisions(root):
        if odr.get("status") != "APPLIED":
            continue
        decision = odr.get("decision") or {}
        if decision.get("kind") != "AUTHORIZATION":
            continue
        override = odr.get("execution_override")
        if not isinstance(override, dict) or override.get("disposition") != "GRANTED":
            continue
        if ((odr.get("effects") or {}).get("grants_material_write_authority")) is not True:
            continue
        scope = override.get("scope") or {}
        if str(scope.get("branch") or "") != str(branch):
            continue
        scoped_repo = str(scope.get("repository") or "").strip()
        if repo_ids and scoped_repo not in repo_ids:
            continue
        scoped_route = scope.get("route_key")
        if scoped_route not in {None, ""} and str(scoped_route) != str(route_key):
            continue

        pending_ids = [str(x) for x in (override.get("pending_obligations") or [])]
        pending = [obligations.get(x) for x in pending_ids]
        if not pending_ids or any(x is None for x in pending):
            continue
        if any(x.get("kind") != "DEFERRED_VALIDATION" or x.get("state") != "OPEN" for x in pending):
            continue

        matches.append({
            "odr_id": odr.get("id"),
            "odr_path": str(path.relative_to(root)),
            "override": override,
            "pending": pending,
        })

    if len(matches) > 1:
        return None, ["multiple APPLIED execution overrides match the current branch/route"]
    return (matches[0], []) if matches else (None, [])


def override_allows(override_record: dict[str, Any] | None, control: str) -> bool:
    if not override_record:
        return False
    return control in ((override_record.get("override") or {}).get("defers") or [])


def override_allows_action(override_record: dict[str, Any] | None, action: str) -> bool:
    if not override_record:
        return False
    return action in ((override_record.get("override") or {}).get("allows") or [])
