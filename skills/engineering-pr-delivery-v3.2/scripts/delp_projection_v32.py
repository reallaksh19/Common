#!/usr/bin/env python3
"""Durable Execution Lineage and Projection (DELP) for Engineering Relay V3.2.

Agents publish engineering FACTS about their own leaf responsibility: which
declared units they report complete, the verification result, the durable
evidence refs, the candidate those refs cover, and the next unit.

Everything an Owner reads as progress or status is recomputed here from those
facts plus observed material truth: the leaf P/E, the delivery D/E of every
ancestor, the lineage path, the frontier count and the issue title. Nothing in
this module trusts a percentage, a title, a frontier count, an activity epoch,
a weight or a parent/programme number supplied by an agent; a facts record that
contains one is rejected and reported, and cannot move any number.

The module is deterministic and has no wall-clock, network or random inputs. A
projection is a pure function of: execution graph (the Coordinator's plan),
accepted facts ledger, and observations (live PR head / liveness).

Authority: DERIVED_PROJECTION_ONLY. A projection is never engineering
permission, acceptance evidence or programme authority.

Standard-library only, except that the CLI/parser load YAML when PyYAML exists.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import subprocess
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping

PROTOCOL_LINE = "V3.2"
SCHEMA_PREFIX = "relay-v3.2-delp"
AUTHORITY = "DERIVED_PROJECTION_ONLY"
FACTS_SCHEMA = f"{SCHEMA_PREFIX}-checkpoint-facts"
GRAPH_SCHEMA = f"{SCHEMA_PREFIX}-execution-graph"
PROJECTION_SCHEMA = f"{SCHEMA_PREFIX}-projection"
STATUS_SCHEMA = f"{SCHEMA_PREFIX}-live-status"
DECOMPOSITION_SCHEMA = f"{SCHEMA_PREFIX}-decomposition-report"
DIFF_SCHEMA = f"{SCHEMA_PREFIX}-graph-diff"
FACTS_KEY = "CHECKPOINT_FACTS_V1"

STATUS_START = "<!-- relay-delp:live-status:start -->"
STATUS_END = "<!-- relay-delp:live-status:end -->"
_STATUS_MARKER = re.compile(
    r"<!-- relay-delp:version=(?P<version>\d+) digest=(?P<digest>sha256:[0-9a-f]{64}) -->"
)

# Who may publish facts that the projector will believe. Anyone can comment on a public issue, so a facts
# block from an unrecognised author is rejected, never counted. `programme.fact_authors` (explicit logins)
# overrides the default of repository OWNER / MEMBER / COLLABORATOR.
TRUSTED_ASSOCIATIONS = frozenset({"OWNER", "MEMBER", "COLLABORATOR"})

TITLE_LIMIT = 250  # GitHub rejects titles over 256; keep a margin for UTF-16 emoji.

NODE_KINDS = {"ROOT", "INTERMEDIATE", "LEAF"}
UNIT_STATES = {"COMPLETE", "IN_PROGRESS", "NOT_STARTED"}
UNIT_RESULTS = {"VERIFIED", "PARTIAL", "FAILED", "NOT_RUN", "PENDING"}
GATE_RESULTS = {"PASSED", "FAILED", "NOT_RUN"}
ACTIVITY_FACTS = {
    "ACTIVE",
    "WAITING_CI",
    "WAITING_TOOL",
    "WAITING_EXTERNAL",
    "WAITING_PROVIDER_VISIBILITY",
    "RECOVERING",
    "PAUSED",
}
# A dead executor cannot declare itself QUIET/STALE; only an observer can.
OBSERVED_LIVENESS = {"ACTIVE", "QUIET", "STALE"}
RESULT_SCOPES = {"STEP", "PRODUCT", "RESPONSIBILITY"}
COMPLETE_VALUES = {"YES", "NO", "UNKNOWN"}

# Decomposition gate. A graph without `programme.decomposition_policy` behaves exactly as before
# (mode OFF). `decompose-check` always evaluates; the mode decides whether projection/admission act on it.
POLICY_MODES = ("OFF", "ADVISORY", "ENFORCED")
WORK_CLASSES = ("PRODUCT", "MECHANICAL", "GATE")
PLAN_UPDATE_KINDS = ("SCOPE_EXPANSION", "SCOPE_REDUCTION", "UNIT_REWEIGHT", "UNIT_DROPPED", "POLICY_CHANGE")
# Display scale for "unit points". Percentages never use it: every share is an exact Fraction of the programme.
DEFAULT_TOTAL_WEIGHT = 10000
# NOT_RELEASEABLE only replaces these leaf states; every other state is more urgent or already means "not being worked".
_PLAN_OVERLAID_STATES = frozenset({"NOT_STARTED", "ACTIVE"})
# Defaults follow the programme's written budgets (PROGRAMME_DECOMPOSITION_PROGRESS.md) and sit at the
# Young/Daly optimum for the interruption rate observed on the Common executors (see the contract doc).
DEFAULT_POLICY: dict[str, Any] = {
    "mode": "OFF",
    "units": {"min": 3, "max": 8, "max_share_percent": 40},
    "leaf_budget": {"target_loc": 700, "hard_loc": 1500, "target_minutes": 15, "hard_minutes": 20},
    "min_leaf_target_loc": 50,
    "require": {"outcome": True, "verify": True, "write_surface": True, "size_budget": True},
}
_BUDGET_KEYS = ("target_loc", "hard_loc", "target_minutes", "hard_minutes")

# Keys an agent must never author. They are projections, plan authority or
# derived bookkeeping. Matching is case-insensitive on exact key names and is
# applied recursively to every mapping in a facts record.
FORBIDDEN_FACT_KEYS = frozenset(
    {
        "progress",
        "percent",
        "percentage",
        "p",
        "e",
        "d",
        "pe",
        "ped",
        "title",
        "issue_title",
        "new_title",
        "parent_progress",
        "programme_progress",
        "program_progress",
        "phase_progress",
        "root_progress",
        "frontier",
        "frontier_count",
        "activity_epoch",
        "epoch",
        "evidence_health",
        "projection",
        "live_status",
        "state_light",
        "light",
        "denominator",
        "weight",
        "weights",
        "total_weight",
        "reserve",
        "reserve_weight",
        "evidenced",
        "r_p",
        "r_e",
    }
)
_ALLOWED_FACT_TOP = frozenset(
    {
        "schema",
        "responsibility",
        "material",
        "units",
        "gates",
        "activity",
        "next",
        "blocker",
        "owner_action",
        "result",
    }
)
# Projection notation an agent must not paste into a facts record.
_NOTATION = re.compile(
    r"R:P\d+\s*/\s*E\d+|[ΦΠ]:D\d+\s*/\s*E\d+|\{P\d+%\s*·\s*E\d+%",
)

_SHA = re.compile(r"^[0-9a-f]{40}$")
_DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")
_REF = re.compile(
    r"^(?:(?P<repo>[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)?)#)?(?P<number>[1-9][0-9]*)$"
)
_UNIT_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
# `<leaf ref>:<unit id>` or `<leaf ref>:gate:<gate id>` — how a plan update names the work it changes.
_ITEM_KEY = re.compile(r"^(?P<ref>[^:\s]+):(?P<item>(?:gate:)?[A-Za-z0-9][A-Za-z0-9._-]{0,63})$")
_SURFACE_GLOB = re.compile(r"[*?\[\]\\]")

LIGHT_ACTIVE = "🟢"
LIGHT_ATTENTION = "🟡"
LIGHT_WAITING = "🔵"
LIGHT_STALE = "🔴"
LIGHT_COMPLETE = "✅"
LIGHT_IDLE = "⚪"
_LIGHTS = LIGHT_ACTIVE + LIGHT_ATTENTION + LIGHT_WAITING + LIGHT_STALE + LIGHT_COMPLETE + LIGHT_IDLE

STATE_LIGHT = {
    "ACTIVE": LIGHT_ACTIVE,
    "WAITING_CI": LIGHT_WAITING,
    "WAITING_TOOL": LIGHT_WAITING,
    "WAITING_EXTERNAL": LIGHT_WAITING,
    "WAITING_PROVIDER_VISIBILITY": LIGHT_WAITING,
    "WAITING": LIGHT_WAITING,
    "RECOVERING": LIGHT_ATTENTION,
    "QUIET": LIGHT_ATTENTION,
    "EVIDENCE_GAP": LIGHT_ATTENTION,
    "EVIDENCE_STALE": LIGHT_ATTENTION,
    "NOT_RELEASEABLE": LIGHT_ATTENTION,  # leaf whose plan fails the decomposition gate (ENFORCED mode)
    "PLAN_GAP": LIGHT_ATTENTION,  # ancestor with at least one non-releasable leaf
    "STALE": LIGHT_STALE,
    "COMPLETE": LIGHT_COMPLETE,
    "SUPERSEDED": LIGHT_IDLE,
    "NOT_STARTED": LIGHT_IDLE,
    "PAUSED": LIGHT_IDLE,
    "IDLE": LIGHT_IDLE,
}

CONTINUATION_COMMANDS = re.compile(
    r"^\s*(?:continue|proceed|next|resume|reconcile|take\s+over|keep\s+going|carry\s+on)"
    r"(?:\s+(?:please|now|next))?\s*[?!.,]*\s*$",
    re.IGNORECASE,
)

_FRONTIER_LIFECYCLE = {"ACTIVE", "RECOVERING"}
_TERMINAL = {"COMPLETE", "SUPERSEDED"}


class DelpError(ValueError):
    """Base class for DELP contract violations."""


class GraphError(DelpError):
    """The execution graph (plan) is structurally invalid."""


class ForbiddenProjectionField(DelpError):
    """A facts record tried to author a projection, weight or title."""


class ProjectionConflict(DelpError):
    """A projection write lost a compare-and-swap race."""


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def canonical_digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def percent(value: Fraction) -> int:
    """Display percent: half-up, never 100 unless exactly full, never 0 unless exactly empty."""
    if value <= 0:
        return 0
    if value >= 1:
        return 100
    rounded = int((value * 100 + Fraction(1, 2)) // 1)
    return min(99, max(1, rounded))


def ratio_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def parse_ref(value: Any) -> tuple[str | None, int]:
    match = _REF.fullmatch(str(value or "").strip())
    if not match:
        raise DelpError(f"invalid issue/PR reference: {value!r}")
    return match.group("repo"), int(match.group("number"))


def ref_number(value: Any) -> int:
    return parse_ref(value)[1]


def same_ref(left: Any, right: Any) -> bool:
    lrepo, lnum = parse_ref(left)
    rrepo, rnum = parse_ref(right)
    if lnum != rnum:
        return False
    if lrepo and rrepo:
        return lrepo.lower().split("/")[-1] == rrepo.lower().split("/")[-1] and (
            "/" not in lrepo or "/" not in rrepo or lrepo.lower() == rrepo.lower()
        )
    return True


def _one_line(value: Any, limit: int = 200) -> str:
    text = re.sub(r"\s+", " ", str(value or "")).strip()
    return text if len(text) <= limit else text[: limit - 1] + "…"


# --------------------------------------------------------------------------
# facts: the only thing an agent publishes
# --------------------------------------------------------------------------


def _walk_keys(value: Any, path: str = "") -> Iterable[tuple[str, str]]:
    if isinstance(value, Mapping):
        for key, item in value.items():
            where = f"{path}.{key}" if path else str(key)
            yield where, str(key)
            yield from _walk_keys(item, where)
    elif isinstance(value, (list, tuple)):
        for index, item in enumerate(value):
            yield from _walk_keys(item, f"{path}[{index}]")


def _walk_strings(value: Any, path: str = "") -> Iterable[tuple[str, str]]:
    if isinstance(value, str):
        yield path, value
    elif isinstance(value, Mapping):
        for key, item in value.items():
            yield from _walk_strings(item, f"{path}.{key}" if path else str(key))
    elif isinstance(value, (list, tuple)):
        for index, item in enumerate(value):
            yield from _walk_strings(item, f"{path}[{index}]")


def forbidden_fields(facts: Any) -> list[str]:
    """Paths of every agent-authored projection/plan field in a facts record."""
    found = [
        f"{where}: agents publish facts only; '{key}' is derived or plan authority"
        for where, key in _walk_keys(facts)
        if key.lower() in FORBIDDEN_FACT_KEYS
    ]
    found += [
        f"{where}: contains projection notation; titles and P/E/D are derived"
        for where, text in _walk_strings(facts)
        if _NOTATION.search(text)
    ]
    return found


def _check_refs(values: Any, label: str, errors: list[str]) -> None:
    if values is None:
        return
    if not isinstance(values, list) or not all(isinstance(v, str) and v.strip() for v in values):
        errors.append(f"{label}: must be a list of non-empty strings")


def validate_facts(facts: Any) -> list[str]:
    """Return contract violations for one facts record (empty list = acceptable)."""
    if not isinstance(facts, Mapping):
        return ["facts record must be a mapping"]
    errors = forbidden_fields(facts)
    unknown = sorted(set(map(str, facts)) - _ALLOWED_FACT_TOP)
    errors += [
        f"{key}: unknown field (facts carry only {', '.join(sorted(_ALLOWED_FACT_TOP - {'schema'}))})"
        for key in unknown
        if key.lower() not in FORBIDDEN_FACT_KEYS
    ]
    if facts.get("schema") not in (None, FACTS_SCHEMA):
        errors.append(f"schema: must be {FACTS_SCHEMA}")

    responsibility = facts.get("responsibility")
    if not isinstance(responsibility, Mapping) or not responsibility.get("issue"):
        errors.append("responsibility.issue: required")
    else:
        try:
            parse_ref(responsibility["issue"])
        except DelpError as exc:
            errors.append(f"responsibility.issue: {exc}")
        extra = set(map(str, responsibility)) - {"issue", "id"}
        if extra:
            errors.append(f"responsibility: unknown fields {sorted(extra)}")

    material = facts.get("material")
    if not isinstance(material, Mapping) or not _SHA.fullmatch(str(material.get("candidate_sha") or "")):
        errors.append("material.candidate_sha: required 40-hex lowercase candidate commit")
    else:
        if material.get("pr") is not None:
            try:
                parse_ref(material["pr"])
            except DelpError as exc:
                errors.append(f"material.pr: {exc}")
        extra = set(map(str, material)) - {"pr", "candidate_sha", "base_sha"}
        if extra:
            errors.append(f"material: unknown fields {sorted(extra)}")
        if material.get("base_sha") is not None and not _SHA.fullmatch(str(material["base_sha"])):
            errors.append("material.base_sha: must be 40-hex lowercase")

    seen: set[str] = set()
    for index, unit in enumerate(facts.get("units") or []):
        label = f"units[{index}]"
        if not isinstance(unit, Mapping) or not _UNIT_ID.fullmatch(str(unit.get("id") or "")):
            errors.append(f"{label}.id: required unit id")
            continue
        uid = str(unit["id"])
        if uid in seen:
            errors.append(f"{label}.id: duplicate unit {uid} in one record")
        seen.add(uid)
        if unit.get("state") not in UNIT_STATES:
            errors.append(f"{label}.state: one of {sorted(UNIT_STATES)}")
        if unit.get("result") is not None and unit["result"] not in UNIT_RESULTS:
            errors.append(f"{label}.result: one of {sorted(UNIT_RESULTS)}")
        _check_refs(unit.get("evidence_refs"), f"{label}.evidence_refs", errors)
        if unit.get("candidate_sha") is not None and not _SHA.fullmatch(str(unit["candidate_sha"])):
            errors.append(f"{label}.candidate_sha: must be 40-hex lowercase")
        if unit.get("contract_digest") is not None and not _DIGEST.fullmatch(str(unit["contract_digest"])):
            errors.append(f"{label}.contract_digest: must be sha256:<64 hex>")
        extra = set(map(str, unit)) - {"id", "state", "result", "evidence_refs", "candidate_sha", "contract_digest"}
        extra = {key for key in extra if key.lower() not in FORBIDDEN_FACT_KEYS}
        if extra:
            errors.append(f"{label}: unknown fields {sorted(extra)}")

    gate_seen: set[str] = set()
    for index, gate in enumerate(facts.get("gates") or []):
        label = f"gates[{index}]"
        if not isinstance(gate, Mapping) or not _UNIT_ID.fullmatch(str(gate.get("id") or "")):
            errors.append(f"{label}.id: required gate id")
            continue
        gid = str(gate["id"])
        if gid in gate_seen:
            errors.append(f"{label}.id: duplicate gate {gid} in one record")
        gate_seen.add(gid)
        if gate.get("result") not in GATE_RESULTS:
            errors.append(f"{label}.result: one of {sorted(GATE_RESULTS)}")
        _check_refs(gate.get("evidence_refs"), f"{label}.evidence_refs", errors)
        if gate.get("candidate_sha") is not None and not _SHA.fullmatch(str(gate["candidate_sha"])):
            errors.append(f"{label}.candidate_sha: must be 40-hex lowercase")
        extra = set(map(str, gate)) - {"id", "result", "evidence_refs", "candidate_sha"}
        extra = {key for key in extra if key.lower() not in FORBIDDEN_FACT_KEYS}
        if extra:
            errors.append(f"{label}: unknown fields {sorted(extra)}")

    if facts.get("activity") is not None and facts["activity"] not in ACTIVITY_FACTS:
        errors.append(f"activity: one of {sorted(ACTIVITY_FACTS)} (QUIET/STALE are observed, never declared)")

    nxt = facts.get("next")
    if nxt is not None:
        if not isinstance(nxt, Mapping) or set(map(str, nxt)) - {"unit", "action"}:
            errors.append("next: mapping with only 'unit' and 'action'")
        else:
            if nxt.get("unit") is not None and not _UNIT_ID.fullmatch(str(nxt["unit"])):
                errors.append("next.unit: invalid unit id")
            if nxt.get("action") is not None and (
                not isinstance(nxt["action"], str) or len(nxt["action"]) > 200 or "\n" in nxt["action"]
            ):
                errors.append("next.action: single line, at most 200 characters")
    for key in ("blocker", "owner_action"):
        value = facts.get(key)
        if value is not None and (not isinstance(value, str) or len(value) > 200 or "\n" in value):
            errors.append(f"{key}: single line, at most 200 characters")

    result = facts.get("result")
    if result is not None:
        if not isinstance(result, Mapping) or result.get("scope") not in RESULT_SCOPES:
            errors.append(f"result.scope: one of {sorted(RESULT_SCOPES)}")
        else:
            complete = result.get("responsibility_complete", "UNKNOWN")
            if complete not in COMPLETE_VALUES:
                errors.append(f"result.responsibility_complete: one of {sorted(COMPLETE_VALUES)}")
            if complete == "YES" and result["scope"] != "RESPONSIBILITY":
                errors.append("result: complete YES requires RESPONSIBILITY scope")
            if result.get("superseded_by") is not None:
                try:
                    parse_ref(result["superseded_by"])
                except DelpError as exc:
                    errors.append(f"result.superseded_by: {exc}")
            extra = set(map(str, result)) - {"scope", "responsibility_complete", "superseded_by"}
            if extra:
                errors.append(f"result: unknown fields {sorted(extra)}")
    return errors


def require_facts(facts: Any) -> dict[str, Any]:
    errors = validate_facts(facts)
    if errors:
        if any("agents publish facts only" in e or "projection notation" in e for e in errors):
            raise ForbiddenProjectionField("; ".join(errors))
        raise DelpError("; ".join(errors))
    return dict(facts)


_FENCE = re.compile(
    r"```[ \t]*(?:ya?ml)?[ \t]*\r?\n(?P<body>[ \t]*" + FACTS_KEY + r":.*?)\r?\n```",
    re.DOTALL,
)


def extract_facts_blocks(text: str) -> list[dict[str, Any]]:
    """Parse every CHECKPOINT_FACTS_V1 fenced block found in a comment body."""
    try:
        import yaml  # type: ignore
    except ImportError as exc:  # pragma: no cover - environment dependent
        raise DelpError("PyYAML is required to parse CHECKPOINT_FACTS_V1 blocks") from exc
    blocks: list[dict[str, Any]] = []
    for match in _FENCE.finditer(str(text or "")):
        document = yaml.safe_load(match.group("body"))
        body = (document or {}).get(FACTS_KEY)
        if not isinstance(body, Mapping):
            raise DelpError(f"{FACTS_KEY} block must be a mapping")
        facts = dict(body)
        facts.setdefault("schema", FACTS_SCHEMA)
        blocks.append(facts)
    return blocks


# --------------------------------------------------------------------------
# graph: the Coordinator's plan (denominators and lineage live here only)
# --------------------------------------------------------------------------


def _positive_int(value: Any, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise GraphError(f"{label}: must be a positive integer")
    return value


def _str_list(value: Any, label: str) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list) or not all(isinstance(v, str) and v.strip() for v in value):
        raise GraphError(f"{label}: must be a list of non-empty strings")
    return [v.strip() for v in value]


def _ref_list(value: Any, label: str) -> list[str]:
    refs = _str_list(value, label)
    for item in refs:
        try:
            parse_ref(item)
        except DelpError as exc:
            raise GraphError(f"{label}: {exc}") from exc
    return refs


def _size_budget(value: Any, ref: str) -> dict[str, int] | None:
    if value is None:
        return None
    if not isinstance(value, Mapping):
        raise GraphError(f"{ref}.size_budget: must be a mapping")
    unknown = sorted(set(map(str, value)) - set(_BUDGET_KEYS))
    if unknown:
        raise GraphError(f"{ref}.size_budget: unknown keys {unknown} (allowed: {list(_BUDGET_KEYS)})")
    return {str(k): _positive_int(v, f"{ref}.size_budget.{k}") for k, v in value.items()}


def _write_surface(value: Any, ref: str) -> list[str]:
    """Repo-relative file paths or directory prefixes (trailing '/'); globs are rejected so overlap stays decidable."""
    entries = _str_list(value, f"{ref}.write_surface")
    clean = []
    for entry in entries:
        text = entry[2:] if entry.startswith("./") else entry
        segments = [s for s in text.split("/") if s != ""]
        if not segments or text.startswith("/") or "//" in text or ".." in segments or "." in segments or _SURFACE_GLOB.search(text):
            raise GraphError(
                f"{ref}.write_surface: {entry!r} must be a repo-relative file path or a directory prefix ending in '/' "
                "(no globs, no '..', no absolute paths)"
            )
        clean.append(text)
    return sorted(set(clean))


def _surface_overlap(left: list[str], right: list[str]) -> list[str]:
    """Entries on which two write surfaces collide (the more specific side is reported)."""
    hits = set()
    for a in left:
        for b in right:
            if a == b or (a.endswith("/") and b.startswith(a)) or (b.endswith("/") and a.startswith(b)):
                hits.add(a if len(a) >= len(b) else b)
    return sorted(hits)


def _item_key(value: Any, label: str) -> tuple[int, str]:
    match = _ITEM_KEY.fullmatch(str(value or "").strip())
    if not match:
        raise GraphError(f"{label}: {value!r} must be '<leaf ref>:<unit id>' or '<leaf ref>:gate:<gate id>'")
    try:
        return ref_number(match.group("ref")), match.group("item")
    except DelpError as exc:
        raise GraphError(f"{label}: {exc}") from exc


def _plan_updates(value: Any) -> list[dict[str, Any]]:
    """Plan updates are the append-only record of deliberate scope/weight/policy changes."""
    if value is None:
        return []
    if not isinstance(value, list):
        raise GraphError("plan_updates: must be a list")
    seen: set[str] = set()
    rows: list[dict[str, Any]] = []
    for index, raw in enumerate(value):
        where = f"plan_updates[{index}]"
        if not isinstance(raw, Mapping):
            raise GraphError(f"{where}: must be a mapping")
        pid = str(raw.get("id") or "").strip()
        if not pid or pid in seen:
            raise GraphError(f"{where}.id: required and unique")
        seen.add(pid)
        kind = raw.get("kind")
        if kind not in PLAN_UPDATE_KINDS:
            raise GraphError(f"{where}.kind: one of {list(PLAN_UPDATE_KINDS)}")
        reason = str(raw.get("reason") or "").strip()
        if not reason:
            raise GraphError(f"{where}.reason: required")
        owner_authorized = raw.get("owner_authorized", False)
        if not isinstance(owner_authorized, bool):
            raise GraphError(f"{where}.owner_authorized: must be a boolean")
        unit_keys = [_item_key(v, f"{where}.units") for v in _str_list(raw.get("units"), f"{where}.units")]
        try:
            node_numbers = [ref_number(v) for v in _str_list(raw.get("nodes"), f"{where}.nodes")]
        except DelpError as exc:
            raise GraphError(f"{where}.nodes: {exc}") from exc
        if kind != "POLICY_CHANGE" and not unit_keys and not node_numbers:
            raise GraphError(f"{where}: name the units and/or nodes the update covers")
        rows.append(
            {
                "id": pid,
                "kind": kind,
                "reason": reason,
                "owner_authorized": owner_authorized,
                "owner_basis": str(raw.get("owner_basis") or "").strip(),
                "unit_keys": unit_keys,
                "node_numbers": node_numbers,
                "raw": canonical_json(raw),
            }
        )
    return rows


def resolve_policy(overrides: Any) -> dict[str, Any]:
    """Merge `programme.decomposition_policy` over the defaults and validate it. Raises GraphError."""
    policy = copy.deepcopy(DEFAULT_POLICY)
    if overrides is None:
        return policy
    if not isinstance(overrides, Mapping):
        raise GraphError("programme.decomposition_policy: must be a mapping")
    unknown = sorted(set(map(str, overrides)) - set(DEFAULT_POLICY))
    if unknown:
        raise GraphError(f"programme.decomposition_policy: unknown keys {unknown}")
    for key, value in overrides.items():
        if key == "mode":
            if value not in POLICY_MODES:
                raise GraphError(f"programme.decomposition_policy.mode: one of {list(POLICY_MODES)}")
            policy["mode"] = value
        elif key in ("units", "leaf_budget", "require"):
            if not isinstance(value, Mapping):
                raise GraphError(f"programme.decomposition_policy.{key}: must be a mapping")
            extra = sorted(set(map(str, value)) - set(policy[key]))
            if extra:
                raise GraphError(f"programme.decomposition_policy.{key}: unknown keys {extra}")
            policy[key].update(value)
        else:
            policy[key] = value
    units, budget = policy["units"], policy["leaf_budget"]
    for label, mapping in (("units", units), ("leaf_budget", budget)):
        for k, v in mapping.items():
            _positive_int(v, f"programme.decomposition_policy.{label}.{k}")
    if units["min"] > units["max"]:
        raise GraphError("programme.decomposition_policy.units: min must not exceed max")
    if units["max_share_percent"] > 100:
        raise GraphError("programme.decomposition_policy.units.max_share_percent: at most 100")
    if budget["target_loc"] > budget["hard_loc"] or budget["target_minutes"] > budget["hard_minutes"]:
        raise GraphError("programme.decomposition_policy.leaf_budget: target must not exceed hard")
    nano = policy["min_leaf_target_loc"]
    if isinstance(nano, bool) or not isinstance(nano, int) or nano < 0:
        raise GraphError("programme.decomposition_policy.min_leaf_target_loc: must be a non-negative integer")
    if not all(isinstance(v, bool) for v in policy["require"].values()):
        raise GraphError("programme.decomposition_policy.require: values must be booleans")
    return policy


def validate_graph(graph: Any) -> dict[str, Any]:
    """Validate the plan and return an indexed view. Raises GraphError."""
    if not isinstance(graph, Mapping):
        raise GraphError("graph must be a mapping")
    if graph.get("schema") not in (None, GRAPH_SCHEMA):
        raise GraphError(f"schema: must be {GRAPH_SCHEMA}")
    programme = graph.get("programme") or {}
    root_ref = programme.get("root")
    if not root_ref:
        raise GraphError("programme.root: required")
    try:
        parse_ref(root_ref)
    except DelpError as exc:
        raise GraphError(f"programme.root: {exc}") from exc
    policy = resolve_policy(programme.get("decomposition_policy"))
    total_weight = _positive_int(programme.get("total_weight", DEFAULT_TOTAL_WEIGHT), "programme.total_weight")

    nodes: dict[str, dict[str, Any]] = {}
    by_number: dict[int, str] = {}
    order: list[str] = []
    for raw in graph.get("nodes") or []:
        if not isinstance(raw, Mapping):
            raise GraphError("nodes[]: must be mappings")
        ref = str(raw.get("ref") or "")
        try:
            number = ref_number(ref)
        except DelpError as exc:
            raise GraphError(f"nodes[].ref: {exc}") from exc
        if number in by_number:
            raise GraphError(f"duplicate node {ref}")
        kind = raw.get("kind")
        if kind not in NODE_KINDS:
            raise GraphError(f"{ref}.kind: one of {sorted(NODE_KINDS)}")
        node = {
            "ref": ref,
            "number": number,
            "kind": kind,
            "parent": raw.get("parent"),
            "weight": None,
            "reserve_weight": 0,
            "children": [],
        }
        if kind != "ROOT":
            if not raw.get("parent"):
                raise GraphError(f"{ref}.parent: required")
            node["weight"] = _positive_int(raw.get("weight"), f"{ref}.weight")
        elif raw.get("parent"):
            raise GraphError(f"{ref}: ROOT cannot have a parent")
        reserve = raw.get("reserve_weight", 0)
        if kind == "LEAF" and reserve:
            raise GraphError(f"{ref}: reserve_weight is only valid on ROOT/INTERMEDIATE nodes")
        if isinstance(reserve, bool) or not isinstance(reserve, int) or reserve < 0:
            raise GraphError(f"{ref}.reserve_weight: must be a non-negative integer")
        node["reserve_weight"] = reserve
        if kind == "LEAF":
            units = raw.get("units")
            if not isinstance(units, list) or not units:
                raise GraphError(f"{ref}.units: at least one declared unit with a weight is required")
            seen_units: set[str] = set()
            clean_units = []
            for unit in units:
                if not isinstance(unit, Mapping):
                    raise GraphError(f"{ref}.units: every unit must be a mapping")
                uid = str(unit.get("id") or "")
                if not _UNIT_ID.fullmatch(uid) or uid in seen_units:
                    raise GraphError(f"{ref}.units: invalid or duplicate unit id {uid!r}")
                seen_units.add(uid)
                moved_from = unit.get("moved_from")
                if moved_from is not None:
                    try:
                        parse_ref(moved_from)
                    except DelpError as exc:
                        raise GraphError(f"{ref}.units.{uid}.moved_from: {exc}") from exc
                texts = {}
                for text_key in ("verify", "outcome"):
                    if unit.get(text_key) is not None and not isinstance(unit[text_key], str):
                        raise GraphError(f"{ref}.units.{uid}.{text_key}: must be a string")
                    texts[text_key] = str(unit.get(text_key) or "").strip() or None
                clean_units.append(
                    {
                        "id": uid,
                        "weight": _positive_int(unit.get("weight"), f"{ref}.units.{uid}.weight"),
                        "verify": texts["verify"],
                        "outcome": texts["outcome"],
                        "moved_from": moved_from,
                    }
                )
            gates = []
            seen_gates: set[str] = set()
            for gate in raw.get("delivery_gates") or []:
                gid = str((gate or {}).get("id") or "")
                if not _UNIT_ID.fullmatch(gid) or gid in seen_gates:
                    raise GraphError(f"{ref}.delivery_gates: invalid or duplicate gate id {gid!r}")
                seen_gates.add(gid)
                gates.append({"id": gid, "weight": _positive_int(gate.get("weight"), f"{ref}.delivery_gates.{gid}.weight")})
            coder_weight = raw.get("coder_weight")
            if gates:
                coder_weight = _positive_int(coder_weight if coder_weight is not None else 60, f"{ref}.coder_weight")
            outcome = raw.get("outcome")
            if outcome is not None and not isinstance(outcome, str):
                raise GraphError(f"{ref}.outcome: must be a string")
            work_class = raw.get("work_class", "PRODUCT")
            if work_class not in WORK_CLASSES:
                raise GraphError(f"{ref}.work_class: one of {list(WORK_CLASSES)}")
            basis = raw.get("parallel_ok_basis")
            if basis is not None and not isinstance(basis, str):
                raise GraphError(f"{ref}.parallel_ok_basis: must be a string")
            node.update(
                {
                    "units": clean_units,
                    "delivery_gates": gates,
                    "coder_weight": coder_weight if gates else 1,
                    "responsibility_id": raw.get("responsibility_id"),
                    "primary_pr": raw.get("primary_pr"),
                    # Branch/tag whose head is the candidate when the leaf has no PR yet.
                    "candidate_ref": (str(raw["candidate_ref"]) if raw.get("candidate_ref") else None),
                    "critical": bool(raw.get("critical", False)),
                    "verification": sorted(set(raw.get("verification") or ["VERIFIED"])),
                    "contract_digest": raw.get("contract_digest"),
                    # decomposition contract (judged by decomposition_report; the progress maths never reads it)
                    "work_class": work_class,
                    "outcome": (outcome or "").strip() or None,
                    "size_budget": _size_budget(raw.get("size_budget"), ref),
                    "write_surface": _write_surface(raw.get("write_surface"), ref),
                    "depends_on": _ref_list(raw.get("depends_on"), f"{ref}.depends_on"),
                    "parallel_ok": _ref_list(raw.get("parallel_ok"), f"{ref}.parallel_ok"),
                    "parallel_ok_basis": (basis or "").strip() or None,
                }
            )
            if node["primary_pr"] is not None:
                try:
                    parse_ref(node["primary_pr"])
                except DelpError as exc:
                    raise GraphError(f"{ref}.primary_pr: {exc}") from exc
            bad = [r for r in node["verification"] if r not in UNIT_RESULTS]
            if bad:
                raise GraphError(f"{ref}.verification: unknown results {bad}")
            if node["contract_digest"] is not None and not _DIGEST.fullmatch(str(node["contract_digest"])):
                raise GraphError(f"{ref}.contract_digest: must be sha256:<64 hex>")
        nodes[ref] = node
        by_number[number] = ref
        order.append(ref)

    roots = [ref for ref, n in nodes.items() if n["kind"] == "ROOT"]
    if len(roots) != 1:
        raise GraphError("exactly one ROOT node is required")
    if not same_ref(roots[0], root_ref):
        raise GraphError("programme.root must name the ROOT node")

    for ref, node in nodes.items():
        if node["kind"] == "ROOT":
            continue
        parent_number = ref_number(node["parent"])
        parent_ref = by_number.get(parent_number)
        if parent_ref is None:
            raise GraphError(f"{ref}.parent: {node['parent']} is not a declared node")
        if nodes[parent_ref]["kind"] == "LEAF":
            raise GraphError(f"{ref}.parent: a LEAF cannot have children")
        node["parent_ref"] = parent_ref
        nodes[parent_ref]["children"].append(ref)

    # cycle / reachability: every node must reach the root by following parents
    for ref in nodes:
        seen: set[str] = set()
        cursor = ref
        while nodes[cursor]["kind"] != "ROOT":
            if cursor in seen:
                raise GraphError(f"cycle through {ref}")
            seen.add(cursor)
            cursor = nodes[cursor]["parent_ref"]
    for ref, node in nodes.items():
        if node["kind"] != "LEAF" and not node["children"]:
            raise GraphError(f"{ref}: a ROOT/INTERMEDIATE node needs at least one child")

    # leaf-to-leaf references (ordering and declared parallelism) must name declared leaves
    leaf_by_number = {n["number"]: ref for ref, n in nodes.items() if n["kind"] == "LEAF"}
    for ref, node in nodes.items():
        if node["kind"] != "LEAF":
            continue
        for field in ("depends_on", "parallel_ok"):
            resolved = set()
            for value in node[field]:
                target = leaf_by_number.get(ref_number(value))
                if target is None:
                    raise GraphError(f"{ref}.{field}: {value} is not a declared LEAF")
                if target == ref:
                    raise GraphError(f"{ref}.{field}: a leaf cannot reference itself")
                resolved.add(target)
            node[field] = sorted(resolved, key=lambda r: nodes[r]["number"])
    walk_state: dict[str, int] = {}  # 1 = on the current path, 2 = fully explored

    def walk(ref: str) -> None:
        walk_state[ref] = 1
        for dep in nodes[ref]["depends_on"]:
            if walk_state.get(dep) == 1:
                raise GraphError(f"depends_on cycle through {ref} and {dep}")
            if dep not in walk_state:
                walk(dep)
        walk_state[ref] = 2

    for ref in leaf_by_number.values():
        if ref not in walk_state:
            walk(ref)

    return {
        "programme": dict(programme),
        "policy": policy,
        "total_weight": total_weight,
        "plan_updates": _plan_updates(graph.get("plan_updates")),
        "nodes": nodes,
        "order": order,
        "root": roots[0],
        "by_number": by_number,
        "digest": canonical_digest(graph),
    }


def lineage(indexed: Mapping[str, Any], ref: str) -> list[str]:
    nodes = indexed["nodes"]
    chain = [ref]
    while nodes[chain[-1]]["kind"] != "ROOT":
        chain.append(nodes[chain[-1]]["parent_ref"])
    return list(reversed(chain))


# --------------------------------------------------------------------------
# decomposition gate: is the plan small, verifiable and collision-free enough to hand to an agent?
#
# The gate judges the PLAN (the execution graph). It never reads agent facts and never moves a percentage;
# its only effects are a `plan` block, a NOT_RELEASEABLE / PLAN_GAP state (ENFORCED mode only) and the
# FIX_PLAN continuation action.
# --------------------------------------------------------------------------


def _finding(code: str, detail: str, severity: str = "BLOCKER") -> dict[str, str]:
    return {"code": code, "severity": severity, "detail": detail}


def _id_list(ids: Iterable[str], limit: int = 6) -> str:
    ids = list(ids)
    return ", ".join(ids[:limit]) + (f" (+{len(ids) - limit} more)" if len(ids) > limit else "")


def _parts_at_target(budget: Mapping[str, int], limits: Mapping[str, int]) -> int:
    parts = 1
    for dim in ("loc", "minutes"):
        declared = budget.get(f"target_{dim}") or budget.get(f"hard_{dim}")
        if declared:
            parts = max(parts, -(-declared // limits[f"target_{dim}"]))
    return parts


def _leaf_findings(node: Mapping[str, Any], policy: Mapping[str, Any]) -> list[dict[str, str]]:
    """Every per-leaf rule. MECHANICAL and GATE leaves are exempt from the unit-count floor and the share cap only."""
    unit_rules, limits, require = policy["units"], policy["leaf_budget"], policy["require"]
    product = node["work_class"] == "PRODUCT"
    rows = node["units"]
    found: list[dict[str, str]] = []
    if len(rows) > unit_rules["max"]:
        found.append(_finding("UNITS_ABOVE_MAX", f"{len(rows)} units (max {unit_rules['max']}): split the leaf"))
    if product and len(rows) < unit_rules["min"]:
        found.append(
            _finding(
                "UNITS_BELOW_MIN",
                f"{len(rows)} units (min {unit_rules['min']}): declare verifiable slices (rote or review-only work is classed MECHANICAL or GATE by the Coordinator)",
            )
        )
    if product:
        total = sum(u["weight"] for u in rows)
        for u in rows:
            if u["weight"] * 100 > unit_rules["max_share_percent"] * total:
                found.append(
                    _finding(
                        "UNIT_SHARE_OVER",
                        f"{u['id']} carries {percent(Fraction(u['weight'], total))}% of the leaf "
                        f"(max {unit_rules['max_share_percent']}%): split or reweight it",
                    )
                )
    if require["verify"]:
        unverifiable = [u["id"] for u in rows if not u["verify"]]
        if unverifiable:
            found.append(_finding("UNIT_VERIFY_MISSING", f"no verify step for {_id_list(unverifiable)}"))
    if require["outcome"] and not node["outcome"]:
        found.append(_finding("OUTCOME_MISSING", "state the observable outcome of the leaf in one sentence"))
    if require["write_surface"] and not node["write_surface"]:
        found.append(_finding("WRITE_SURFACE_MISSING", "declare the files or directories the leaf will write"))
    budget = node["size_budget"] or {}
    absent = [k for k in _BUDGET_KEYS if k not in budget]
    if require["size_budget"] and absent:
        found.append(_finding("SIZE_BUDGET_MISSING", f"declare the size_budget keys {_id_list(absent)}"))
    for dim in ("loc", "minutes"):
        target, hard = budget.get(f"target_{dim}"), budget.get(f"hard_{dim}")
        if target is not None and hard is not None and target > hard:
            found.append(_finding("SIZE_BUDGET_INCONSISTENT", f"target_{dim} {target} exceeds hard_{dim} {hard}"))
    over_hard = [
        f"hard_{dim} {budget[f'hard_{dim}']} > {limits[f'hard_{dim}']}"
        for dim in ("loc", "minutes")
        if budget.get(f"hard_{dim}", 0) > limits[f"hard_{dim}"]
    ]
    over_target = [
        f"target_{dim} {budget[f'target_{dim}']} > {limits[f'target_{dim}']}"
        for dim in ("loc", "minutes")
        if budget.get(f"target_{dim}", 0) > limits[f"target_{dim}"]
    ]
    if over_hard:
        parts = _parts_at_target(budget, limits)
        hint = f"split into at least {parts} leaves" if parts > 1 else "lower the cap or split the leaf"
        found.append(_finding("SIZE_OVER_HARD", f"{', '.join(over_hard)}: {hint}"))
    elif over_target:
        found.append(_finding("SIZE_OVER_TARGET", ", ".join(over_target), "ADVISORY"))
    nano = policy["min_leaf_target_loc"]
    if product and nano and budget.get("target_loc", nano) < nano:
        found.append(
            _finding(
                "LEAF_TOO_SMALL",
                f"target_loc {budget['target_loc']} < {nano}: fold it into a sibling leaf (an issue and a PR cost more than the work)",
                "ADVISORY",
            )
        )
    if node["parallel_ok"] and not node["parallel_ok_basis"]:
        found.append(_finding("PARALLEL_BASIS_MISSING", "parallel_ok needs a parallel_ok_basis saying why the write surfaces do not conflict"))
    return found


def _decomposition(
    indexed: Mapping[str, Any], closed: Iterable[str] = (), mode: str | None = None
) -> dict[str, Any]:
    nodes, policy = indexed["nodes"], indexed["policy"]
    closed = set(closed)
    leaves = [ref for ref in indexed["order"] if nodes[ref]["kind"] == "LEAF"]
    active = [ref for ref in leaves if ref not in closed]
    found = {ref: _leaf_findings(nodes[ref], policy) for ref in active}

    reach: dict[str, set[str]] = {}

    def reachable(ref: str) -> set[str]:
        if ref not in reach:  # validate_graph guarantees the depends_on graph is acyclic
            reach[ref] = set()
            for dep in nodes[ref]["depends_on"]:
                reach[ref] |= {dep} | reachable(dep)
        return reach[ref]

    for index, a in enumerate(active):
        for b in active[index + 1 :]:
            hits = _surface_overlap(nodes[a]["write_surface"], nodes[b]["write_surface"])
            ordered = b in reachable(a) or a in reachable(b)
            declared_parallel = b in nodes[a]["parallel_ok"] or a in nodes[b]["parallel_ok"]
            if not hits or ordered or declared_parallel:
                continue
            for me, other in ((a, b), (b, a)):
                found[me].append(
                    _finding(
                        "WRITE_SURFACE_COLLISION",
                        f"overlaps #{nodes[other]['number']} on {_id_list(hits, 3)} with no depends_on order and no parallel_ok",
                    )
                )

    rows: dict[str, Any] = {}
    classes: dict[str, int] = {}
    for ref in active:
        ordered_findings = sorted(found[ref], key=lambda f: (f["severity"] != "BLOCKER", f["code"], f["detail"]))
        blockers = [{"code": f["code"], "detail": f["detail"]} for f in ordered_findings if f["severity"] == "BLOCKER"]
        advisories = [{"code": f["code"], "detail": f["detail"]} for f in ordered_findings if f["severity"] != "BLOCKER"]
        rows[ref] = {
            "work_class": nodes[ref]["work_class"],
            "releasable": not blockers,
            "blockers": blockers,
            "advisories": advisories,
        }
        classes[nodes[ref]["work_class"]] = classes.get(nodes[ref]["work_class"], 0) + 1
    return {
        "schema": DECOMPOSITION_SCHEMA,
        "authority": AUTHORITY,
        "mode": mode or policy["mode"],
        "policy": policy,
        "leaves": rows,
        "summary": {
            "evaluated": len(active),
            "skipped_closed": len(leaves) - len(active),
            "releasable": sum(1 for r in rows.values() if r["releasable"]),
            "not_releasable": sum(1 for r in rows.values() if not r["releasable"]),
            "advisories": sum(len(r["advisories"]) for r in rows.values()),
            "by_class": dict(sorted(classes.items())),
        },
    }


def decomposition_report(graph: Any, mode: str | None = None, closed: Iterable[str] = ()) -> dict[str, Any]:
    """Evaluate the decomposition policy over every LEAF not in `closed` (e.g. already COMPLETE). Pure."""
    if mode is not None and mode not in POLICY_MODES:
        raise GraphError(f"mode: one of {list(POLICY_MODES)}")
    indexed = validate_graph(graph)
    closed_numbers = {ref_number(c) for c in closed}
    return _decomposition(indexed, {r for r in indexed["nodes"] if indexed["nodes"][r]["number"] in closed_numbers}, mode)


def render_decomposition(report: Mapping[str, Any]) -> str:
    mode = report["mode"]
    lines = [f"DECOMPOSITION GATE — {mode}" + (" (informational: nothing is enforced)" if mode == "OFF" else "")]
    for ref, row in report["leaves"].items():
        lines.append(f"{ref} [{row['work_class']}] {'RELEASABLE' if row['releasable'] else 'NOT_RELEASEABLE'}")
        lines += [f"  BLOCKER  {f['code']}: {f['detail']}" for f in row["blockers"]]
        lines += [f"  ADVISORY {f['code']}: {f['detail']}" for f in row["advisories"]]
    s = report["summary"]
    classes = ", ".join(f"{k} {v}" for k, v in s["by_class"].items())
    lines.append(
        f"SUMMARY: {s['evaluated']} leaves · {s['releasable']} releasable · {s['not_releasable']} not releasable"
        f" · {s['advisories']} advisories · {s['skipped_closed']} closed (skipped) · classes: {classes or 'none'}"
    )
    return "\n".join(lines)


# --------------------------------------------------------------------------
# conservation: re-planning must not create or destroy progress
# --------------------------------------------------------------------------


def _item_shares(indexed: Mapping[str, Any]) -> dict[tuple[int, str], Fraction]:
    """Exact share of the whole programme carried by every unit and delivery gate.

    share = Π(sibling weight / (Σ sibling weights + reserve)) down the lineage, then the unit's slice of the
    leaf's coder share (or the gate's slice of the delivery weight). The shares plus every reserve sum to 1, so
    adding, dropping, reweighting or moving work changes somebody's share unless the plan conserves it.
    """
    nodes = indexed["nodes"]
    shares: dict[tuple[int, str], Fraction] = {}

    def descend(ref: str, share: Fraction) -> None:
        node = nodes[ref]
        if node["kind"] == "LEAF":
            unit_total = sum(u["weight"] for u in node["units"])
            delivery_total = node["coder_weight"] + sum(g["weight"] for g in node["delivery_gates"])
            coder = share * Fraction(node["coder_weight"], delivery_total)
            for u in node["units"]:
                shares[(node["number"], u["id"])] = coder * Fraction(u["weight"], unit_total)
            for g in node["delivery_gates"]:
                shares[(node["number"], f"gate:{g['id']}")] = share * Fraction(g["weight"], delivery_total)
            return
        den = sum(nodes[c]["weight"] for c in node["children"]) + node["reserve_weight"]
        for child in node["children"]:
            descend(child, share * Fraction(nodes[child]["weight"], den))

    descend(indexed["root"], Fraction(1))
    return shares


def _lineage_numbers(indexed: Mapping[str, Any], number: int) -> set[int]:
    ref = indexed["by_number"].get(number)
    return {indexed["nodes"][r]["number"] for r in lineage(indexed, ref)} if ref else {number}


def _item_text(indexed: Mapping[str, Any], key: tuple[int, str]) -> str:
    return f"{indexed['by_number'].get(key[0], f'#{key[0]}')}:{key[1]}"


def _points_text(share: Fraction, scale: int) -> str:
    points = share * scale
    return str(points.numerator) if points.denominator == 1 else f"{float(points):.2f}"


def _policy_weakened(old: Mapping[str, Any], new: Mapping[str, Any]) -> list[str]:
    """Ways in which `new` is a looser gate than `old`. Tightening is never reported."""
    rank = {m: i for i, m in enumerate(POLICY_MODES)}
    out = []
    if rank[new["mode"]] < rank[old["mode"]]:
        out.append(f"mode {old['mode']} -> {new['mode']}")
    for section, key, looser_is_higher in (
        ("units", "max", True),
        ("units", "min", False),
        ("units", "max_share_percent", True),
        ("leaf_budget", "target_loc", True),
        ("leaf_budget", "hard_loc", True),
        ("leaf_budget", "target_minutes", True),
        ("leaf_budget", "hard_minutes", True),
    ):
        before, after = old[section][key], new[section][key]
        if (after > before) if looser_is_higher else (after < before):
            out.append(f"{section}.{key} {before} -> {after}")
    if new["min_leaf_target_loc"] < old["min_leaf_target_loc"]:
        out.append(f"min_leaf_target_loc {old['min_leaf_target_loc']} -> {new['min_leaf_target_loc']}")
    out += [f"require.{k} dropped" for k, v in old["require"].items() if v and not new["require"][k]]
    return out


def graph_diff(old_graph: Any, new_graph: Any) -> dict[str, Any]:
    """Judge a re-plan (split, merge, reweight, drop) against the plan it replaces. Pure.

    A unit or gate keeps its exact programme share across a re-plan unless a NEW `plan_updates` entry covers the
    change, so splitting a leaf can neither manufacture progress nor delete it. Plan updates are append-only
    history; each new one must carry `owner_authorized: true` and an `owner_basis`. Weakening the decomposition
    policy needs a POLICY_CHANGE update. `owner_authorized` is a record for review, not proof of identity.
    """
    old, new = validate_graph(old_graph), validate_graph(new_graph)
    old_shares, new_shares = _item_shares(old), _item_shares(new)
    scale = new["total_weight"]
    findings: list[dict[str, str]] = []

    def add(code: str, detail: str, severity: str = "BLOCKER") -> None:
        findings.append(_finding(code, detail, severity))

    previous = {u["id"]: u for u in old["plan_updates"]}
    current = {u["id"]: u for u in new["plan_updates"]}
    for pid, u in previous.items():
        if pid not in current or current[pid]["raw"] != u["raw"]:
            add("PLAN_HISTORY_CHANGED", f"plan update {pid} was removed or edited; plan_updates is append-only")
    fresh = [u for u in new["plan_updates"] if u["id"] not in previous]
    for u in fresh:
        if not (u["owner_authorized"] and u["owner_basis"]):
            add("PLAN_UPDATE_UNAUTHORISED", f"{u['id']} ({u['kind']}) needs owner_authorized: true and an owner_basis")
    used: set[str] = set()

    def covered(kinds: set[str], key: tuple[int, str], scope_numbers: set[int]) -> bool:
        for u in fresh:
            if u["kind"] not in kinds:
                continue
            scope = set(u["node_numbers"])
            if u["kind"] == "UNIT_DROPPED":  # dropping a unit re-normalises the rest of its leaf
                scope |= {n for n, _ in u["unit_keys"]}
            if key in u["unit_keys"] or scope & scope_numbers:
                used.add(u["id"])
                return True
        return False

    origin: dict[tuple[int, str], tuple[int, str] | None] = {}
    claims: dict[tuple[int, str], list[tuple[int, str]]] = {}
    for key in sorted(new_shares):
        number, item = key
        source: tuple[int, str] | None = key if key in old_shares else None
        if source is None and not item.startswith("gate:"):
            leaf = new["nodes"][new["by_number"][number]]
            moved_from = next((u["moved_from"] for u in leaf["units"] if u["id"] == item and u["moved_from"]), None)
            if moved_from is not None:
                candidate = (ref_number(moved_from), item)
                if candidate in old_shares:
                    source = candidate
                else:
                    add("MOVE_ORIGIN_UNKNOWN", f"{_item_text(new, key)} claims moved_from {moved_from} but that leaf had no {item}")
        origin[key] = source
        if source is not None:
            claims.setdefault(source, []).append(key)
    for source, keys in sorted(claims.items()):
        if len(keys) > 1:
            add("MOVE_DUPLICATE", f"{_item_text(old, source)} is claimed by {_id_list(_item_text(new, k) for k in keys)}")

    dropped = []
    for source in sorted(old_shares):
        if source in claims:
            continue
        dropped.append(_item_text(old, source))
        if not covered({"UNIT_DROPPED", "SCOPE_REDUCTION"}, source, _lineage_numbers(old, source[0])):
            add("UNIT_LOST", f"{_item_text(old, source)} no longer exists and no UNIT_DROPPED or SCOPE_REDUCTION update covers it")

    drift: list[dict[str, str]] = []
    for key, source in origin.items():
        if source is None or new_shares[key] == old_shares[source]:
            continue
        diluted = new_shares[key] < old_shares[source]
        kinds = {"SCOPE_EXPANSION", "UNIT_REWEIGHT"} if diluted else {"SCOPE_REDUCTION", "UNIT_REWEIGHT", "UNIT_DROPPED"}
        row = {
            "item": _item_text(new, key),
            "points_before": _points_text(old_shares[source], scale),
            "points_after": _points_text(new_shares[key], scale),
        }
        drift.append(row)
        if not covered(kinds, key, _lineage_numbers(new, key[0]) | _lineage_numbers(old, source[0])):
            add(
                "POINTS_DRIFT",
                f"{row['item']} {row['points_before']} -> {row['points_after']} points; "
                f"no {' / '.join(sorted(kinds))} update covers it",
            )

    weakened = _policy_weakened(old["policy"], new["policy"])
    policy_updates = [u for u in fresh if u["kind"] == "POLICY_CHANGE"]
    if old["policy"] != new["policy"]:
        used.update(u["id"] for u in policy_updates)
    if weakened and not policy_updates:
        add("POLICY_WEAKENED", f"{'; '.join(weakened)} without a POLICY_CHANGE update")
    for u in fresh:
        if u["id"] not in used:
            add("PLAN_UPDATE_UNUSED", f"{u['id']} ({u['kind']}) covers nothing in this change", "ADVISORY")

    ordered = sorted(findings, key=lambda f: (f["severity"] != "BLOCKER", f["code"], f["detail"]))
    return {
        "schema": DIFF_SCHEMA,
        "authority": AUTHORITY,
        "conserved": not any(f["severity"] == "BLOCKER" for f in ordered),
        "findings": ordered,
        "drift": drift,
        "summary": {
            "items_before": len(old_shares),
            "items_after": len(new_shares),
            "moved": sum(1 for k, s in origin.items() if s is not None and s != k),
            "added": sum(1 for s in origin.values() if s is None),
            "dropped": len(dropped),
            "new_plan_updates": len(fresh),
        },
    }


def render_graph_diff(report: Mapping[str, Any]) -> str:
    s = report["summary"]
    lines = [
        f"PLAN CONSERVATION — {'CONSERVED' if report['conserved'] else 'NOT_CONSERVED'}",
        f"items {s['items_before']} -> {s['items_after']} · moved {s['moved']} · added {s['added']} · dropped {s['dropped']}"
        f" · new plan updates {s['new_plan_updates']}",
    ]
    lines += [f"  {f['severity']:<8} {f['code']}: {f['detail']}" for f in report["findings"]]
    return "\n".join(lines)


# --------------------------------------------------------------------------
# leaf computation: P from claimed units, E only from CURRENT evidence
# --------------------------------------------------------------------------


def _fraction(num: int, den: int) -> Fraction:
    return Fraction(num, den) if den else Fraction(0)


def compute_leaf(
    node: Mapping[str, Any],
    records: list[Mapping[str, Any]],
    observation: Mapping[str, Any] | None,
) -> dict[str, Any]:
    """Pure leaf projection. `records` are accepted facts for this leaf, oldest first."""
    observation = dict(observation or {})
    observed_candidate = observation.get("candidate_sha")
    if observed_candidate is not None and not _SHA.fullmatch(str(observed_candidate)):
        observed_candidate = None
    declared = {u["id"]: u["weight"] for u in node["units"]}
    gate_weights = {g["id"]: g["weight"] for g in node["delivery_gates"]}
    warnings: list[str] = []

    claims: dict[str, dict[str, Any]] = {}
    gate_claims: dict[str, dict[str, Any]] = {}
    latest: Mapping[str, Any] | None = None
    result_fact: Mapping[str, Any] | None = None
    # Most recent STATED value per field: a reviewer's gates-only record must not reset the Coder's
    # blocker / next unit / owner action / activity back to defaults.
    last_next: Mapping[str, Any] = {}
    last_activity = None
    last_blocker = None
    last_owner_action = None
    for rec in records:
        latest = rec
        if rec.get("next") is not None:
            last_next = rec["next"]
        if rec.get("activity") is not None:
            last_activity = rec["activity"]
        if rec.get("blocker") is not None:
            last_blocker = rec["blocker"]
        if rec.get("owner_action") is not None:
            last_owner_action = rec["owner_action"]
        record_candidate = (rec.get("material") or {}).get("candidate_sha")
        record_pr = (rec.get("material") or {}).get("pr")
        for unit in rec.get("units") or []:
            if unit["id"] not in declared:
                warnings.append(f"UNKNOWN_UNIT:{unit['id']}")
                continue
            claims[unit["id"]] = {
                "state": unit["state"],
                "result": unit.get("result") or "NOT_RUN",
                "evidence_refs": [str(r) for r in unit.get("evidence_refs") or []],
                "candidate_sha": unit.get("candidate_sha") or record_candidate,
                "contract_digest": unit.get("contract_digest"),
                "pr": record_pr,
                "source": rec.get("_source"),
            }
        for gate in rec.get("gates") or []:
            if gate["id"] not in gate_weights:
                warnings.append(f"UNKNOWN_GATE:{gate['id']}")
                continue
            gate_claims[gate["id"]] = {
                "result": gate["result"],
                "evidence_refs": [str(r) for r in gate.get("evidence_refs") or []],
                "candidate_sha": gate.get("candidate_sha") or record_candidate,
                "pr": record_pr,
            }
        if rec.get("result") is not None:
            result_fact = rec["result"]

    def unit_gap(uid: str, claim: Mapping[str, Any]) -> str | None:
        if claim["result"] not in node["verification"]:
            return f"RESULT_NOT_ACCEPTED({claim['result']})"
        if not claim["evidence_refs"]:
            return "NO_EVIDENCE_REFS"
        if node.get("primary_pr") and claim.get("pr") and not same_ref(node["primary_pr"], claim["pr"]):
            return "PR_MISMATCH"
        if observed_candidate is None:
            return "CANDIDATE_UNOBSERVED"
        if claim["candidate_sha"] != observed_candidate:
            return "CANDIDATE_MISMATCH"
        digest = node.get("contract_digest")
        if digest and claim.get("contract_digest") != digest:
            return "CONTRACT_DIGEST_MISMATCH"
        return None

    total = sum(declared.values())
    complete_weight = 0
    evidenced_weight = 0
    unit_rows = []
    gaps: list[dict[str, str]] = []
    for uid, weight in declared.items():
        claim = claims.get(uid)
        complete = bool(claim and claim["state"] == "COMPLETE")
        gap = unit_gap(uid, claim) if complete and claim else None
        current = complete and gap is None
        if complete:
            complete_weight += weight
        if current:
            evidenced_weight += weight
        if gap:
            gaps.append({"unit": uid, "reason": gap})
        unit_rows.append(
            {
                "id": uid,
                "weight": weight,
                "claimed_state": claim["state"] if claim else "NOT_STARTED",
                "complete": complete,
                "evidence_current": current,
                "gap": gap,
                "evidence_refs": claim["evidence_refs"] if claim else [],
                "evidence_candidate_sha": claim["candidate_sha"] if claim else None,
            }
        )
    P = _fraction(complete_weight, total)
    E = _fraction(evidenced_weight, total)

    gate_rows = []
    gate_total = sum(gate_weights.values())
    gate_passed = 0
    gate_evidenced = 0
    for gid, weight in gate_weights.items():
        claim = gate_claims.get(gid)
        passed = bool(claim and claim["result"] == "PASSED")
        current = bool(
            passed
            and claim["evidence_refs"]
            and observed_candidate is not None
            and claim["candidate_sha"] == observed_candidate
        )
        if passed:
            gate_passed += weight
        if current:
            gate_evidenced += weight
        gate_rows.append({"id": gid, "weight": weight, "passed": passed, "evidence_current": current})
    coder_weight = node["coder_weight"]
    delivery_total = coder_weight + gate_total
    D = (coder_weight * P + gate_passed) / delivery_total
    DE = (coder_weight * E + gate_evidenced) / delivery_total

    reasons = {g["reason"].split("(")[0] for g in gaps}
    if not gaps:
        health = "CURRENT"
    elif "CANDIDATE_UNOBSERVED" in reasons:
        health = "UNVERIFIABLE"
    elif "CANDIDATE_MISMATCH" in reasons or "PR_MISMATCH" in reasons:
        health = "STALE_CANDIDATE"
    else:
        health = "GAP"

    incomplete = [row["id"] for row in unit_rows if not row["complete"]]
    next_unit = last_next.get("unit")
    active_unit = next_unit if next_unit in incomplete else (incomplete[0] if incomplete else None)

    superseded_by = (result_fact or {}).get("superseded_by")
    claims_complete = bool(
        result_fact
        and result_fact.get("scope") == "RESPONSIBILITY"
        and result_fact.get("responsibility_complete") == "YES"
    )
    if claims_complete and incomplete:
        warnings.append("RESULT_CLAIMS_COMPLETE_BUT_UNITS_OPEN")
    if claims_complete and not incomplete and health != "CURRENT":
        warnings.append("COMPLETE_CLAIM_WITHOUT_CURRENT_EVIDENCE")
    if claims_complete and not incomplete and delivery_total > coder_weight and gate_passed < gate_total:
        warnings.append("COMPLETE_CLAIM_WITH_OPEN_DELIVERY_GATES")
    if claims_complete and not incomplete and gate_passed == gate_total and gate_evidenced < gate_total:
        warnings.append("COMPLETE_CLAIM_WITH_UNEVIDENCED_DELIVERY_GATES")

    activity = last_activity
    liveness = observation.get("liveness")
    if liveness not in OBSERVED_LIVENESS:
        liveness = None

    if superseded_by:
        lifecycle = "SUPERSEDED"
    elif claims_complete and not incomplete and health == "CURRENT" and D == 1 and DE == 1:
        lifecycle = "COMPLETE"
    elif not records and liveness is None:
        lifecycle = "NOT_STARTED"
    elif activity == "PAUSED":
        lifecycle = "PAUSED"
    elif activity == "RECOVERING":
        lifecycle = "RECOVERING"
    else:
        lifecycle = "ACTIVE"

    if lifecycle in {"COMPLETE", "SUPERSEDED", "NOT_STARTED", "PAUSED"}:
        state = lifecycle
    elif liveness == "STALE":
        state = "STALE"
    elif health == "STALE_CANDIDATE":
        state = "EVIDENCE_STALE"
    elif health in {"GAP", "UNVERIFIABLE"}:
        state = "EVIDENCE_GAP"
    elif liveness == "QUIET":
        state = "QUIET"
    elif lifecycle == "RECOVERING":
        state = "RECOVERING"
    elif activity and activity.startswith("WAITING"):
        state = activity
    else:
        state = "ACTIVE"

    material_candidate = observed_candidate
    evidence_candidate = ((latest or {}).get("material") or {}).get("candidate_sha")
    if material_candidate is None:
        relation = "MATERIAL_UNKNOWN"
    elif evidence_candidate is None:
        relation = "EVIDENCE_UNKNOWN"
    elif evidence_candidate == material_candidate:
        relation = "ALIGNED"
    else:
        relation = "CANDIDATE_MOVED"

    owner_action = last_owner_action
    if latest and owner_action is None:
        warnings.append("OWNER_ACTION_UNSTATED")
    return {
        "lifecycle": lifecycle,
        "state": state,
        "active_unit": active_unit,
        "progress": {
            "P": percent(P),
            "E": percent(E),
            "D": percent(D),
            "DE": percent(DE),
            "ratio": {"P": ratio_text(P), "E": ratio_text(E), "D": ratio_text(D), "DE": ratio_text(DE)},
        },
        "_fractions": {"D": D, "DE": DE},
        "units": unit_rows,
        "gates": gate_rows,
        "evidence": {
            "health": health,
            "gaps": gaps,
            "latest_source": (records[-1].get("_source") if records else None),
        },
        "frontier": {
            "material_candidate": material_candidate,
            "evidence_candidate": evidence_candidate,
            "relation": relation,
        },
        "activity_epoch": len(records),
        "liveness": liveness,
        "next": {
            "unit": active_unit,
            "action": _one_line(last_next.get("action")) or None,
        },
        "blocker": _one_line(last_blocker or "NONE"),
        "owner_action": _one_line(owner_action or "NONE"),
        "warnings": warnings,
    }


# --------------------------------------------------------------------------
# title grammar
# --------------------------------------------------------------------------

_PREFIX = re.compile(
    "^(?P<light>[" + _LIGHTS + r"])\s+\[(?P<path>[^\[\]]*)\]\s+(?P<scope>R|Φ|Π):(?P<dm>[PD])(?P<primary>\d{1,3})/E(?P<evidence>\d{1,3})"
    r"(?P<tail>(?:\s+·\s+[^—·]+?)*)(?:\s+—\s+(?P<base>.*))?$",
    re.DOTALL,
)
_LEGACY_PREFIX = re.compile("^[" + _LIGHTS + r"]\s+\{P\d+%[^{}]*\}\s+(?P<base>.*)$", re.DOTALL)
_LEGACY_SUFFIX = re.compile(r"\s+\{P\d+% · E\d+% · [^{}]+\}\s*$")


def split_title(title: str) -> tuple[dict[str, str] | None, str]:
    """Return (generated-part info or None, human base title)."""
    text = str(title or "")
    match = _PREFIX.match(text)
    if match:
        info = {k: (v or "") for k, v in match.groupdict().items() if k != "base"}
        return info, (match.group("base") or "").strip()
    legacy = _LEGACY_PREFIX.match(text)
    if legacy:
        return {"legacy": "PREFIX"}, legacy.group("base").strip()
    stripped = _LEGACY_SUFFIX.sub("", text).strip()
    if stripped != text.strip():
        return {"legacy": "SUFFIX"}, stripped
    return None, text.strip()


def _path_text(indexed: Mapping[str, Any], ref: str) -> str:
    return " › ".join(f"#{indexed['nodes'][r]['number']}" for r in lineage(indexed, ref))


def render_title(prefix: str, base: str) -> str:
    base = (base or "").strip()
    if not base:
        return prefix
    text = f"{prefix} — {base}"
    if len(text) <= TITLE_LIMIT:
        return text
    room = TITLE_LIMIT - len(prefix) - len(" — ") - 1
    return f"{prefix} — {base[: max(room, 1)].rstrip()}…" if room > 0 else prefix[:TITLE_LIMIT]


def title_drift(actual_title: str, expected_prefix: str, expected_base: str | None = None) -> dict[str, Any]:
    """Classify a provider title against the derived projection."""
    info, base = split_title(actual_title)
    expected = render_title(expected_prefix, expected_base if expected_base is not None else base)
    if actual_title.strip() == expected.strip():
        return {"status": "OK", "expected": expected}
    if info is None:
        # Projection notation outside the generated grammar is still an agent-authored projection.
        status = "STALE_OR_HAND_EDITED" if _NOTATION.search(str(actual_title)) else "MISSING_PROJECTION"
    elif "legacy" in info:
        status = "LEGACY_FORMAT"
    else:
        status = "STALE_OR_HAND_EDITED"
    return {"status": status, "expected": expected, "actual": actual_title, "base": base}


# --------------------------------------------------------------------------
# projection
# --------------------------------------------------------------------------


def _frontier_summary(indexed: Mapping[str, Any], leaves: list[str]) -> str:
    parts = []
    for ref in leaves[:2]:
        n = indexed["nodes"][ref]
        pr = n.get("primary_pr")
        parts.append(f"#{n['number']}/PR#{ref_number(pr)}" if pr else f"#{n['number']}")
    if len(leaves) > 2:
        parts.append(f"+{len(leaves) - 2}")
    return ", ".join(parts)


def partition_ledger(
    indexed: Mapping[str, Any], ledger: Iterable[Mapping[str, Any]]
) -> tuple[dict[str, list[dict[str, Any]]], list[dict[str, Any]]]:
    """Validate every facts record. Invalid/forbidden/unknown records are rejected, never trusted."""
    accepted: dict[str, list[tuple[int, int, dict[str, Any]]]] = {}
    rejected: list[dict[str, Any]] = []
    leaves = {n["number"]: ref for ref, n in indexed["nodes"].items() if n["kind"] == "LEAF"}
    for position, entry in enumerate(ledger):
        facts = entry.get("facts") if isinstance(entry, Mapping) else None
        source = str((entry or {}).get("source") or f"ledger[{position}]")
        errors = validate_facts(facts)
        if not errors and (entry or {}).get("untrusted_author"):
            errors = [f"author {(entry or {})['untrusted_author']} is not a trusted fact author for this programme"]
        if not errors:
            number = ref_number(facts["responsibility"]["issue"])
            leaf_ref = leaves.get(number)
            if leaf_ref is None:
                errors = [f"responsibility.issue: {facts['responsibility']['issue']} is not a declared LEAF"]
            else:
                declared_id = indexed["nodes"][leaf_ref].get("responsibility_id")
                claimed_id = facts["responsibility"].get("id")
                if declared_id and claimed_id and declared_id != claimed_id:
                    errors = [f"responsibility.id: {claimed_id} does not match planned {declared_id}"]
        if errors:
            rejected.append({"source": source, "reasons": errors})
            continue
        order = entry.get("order")
        record = dict(facts)
        record["_source"] = source
        accepted.setdefault(leaf_ref, []).append(
            (int(order) if isinstance(order, int) and not isinstance(order, bool) else position, position, record)
        )
    return (
        {ref: [item[2] for item in sorted(rows, key=lambda r: (r[0], r[1]))] for ref, rows in accepted.items()},
        rejected,
    )


def project(
    graph: Any,
    ledger: Iterable[Mapping[str, Any]] = (),
    observations: Mapping[str, Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    """Recompute every node from the plan, accepted facts and observations."""
    ledger = list(ledger)
    indexed = validate_graph(graph)
    nodes = indexed["nodes"]
    observations = {ref_number(k): dict(v or {}) for k, v in (observations or {}).items()}
    accepted, rejected = partition_ledger(indexed, ledger)
    results: dict[str, dict[str, Any]] = {}
    mode = indexed["policy"]["mode"]

    for ref in indexed["order"]:
        if nodes[ref]["kind"] == "LEAF":
            results[ref] = compute_leaf(nodes[ref], accepted.get(ref, []), observations.get(nodes[ref]["number"]))
    if mode != "OFF":
        # Closed (COMPLETE/SUPERSEDED) leaves are history, not work to release: the gate skips them.
        closed = {ref for ref, leaf in results.items() if leaf["lifecycle"] in _TERMINAL}
        for ref, row in _decomposition(indexed, closed)["leaves"].items():
            leaf = results[ref]
            leaf["plan"] = {
                "mode": mode,
                "releasable": row["releasable"],
                "blockers": row["blockers"],
                "advisories": row["advisories"],
            }
            if row["blockers"]:
                leaf["warnings"].append("DECOMPOSITION_BLOCKERS:" + ",".join(sorted({b["code"] for b in row["blockers"]})))
            if row["advisories"]:
                leaf["warnings"].append("DECOMPOSITION_ADVISORIES:" + ",".join(sorted({a["code"] for a in row["advisories"]})))
            if mode == "ENFORCED" and not row["releasable"] and leaf["state"] in _PLAN_OVERLAID_STATES:
                leaf["state"] = "NOT_RELEASEABLE"

    def visit(ref: str) -> dict[str, Any]:
        node = nodes[ref]
        if node["kind"] == "LEAF":
            return results[ref]
        child_rows = [(c, visit(c)) for c in node["children"]]
        den = sum(nodes[c]["weight"] for c, _ in child_rows) + node["reserve_weight"]
        D = sum(Fraction(nodes[c]["weight"]) * _node_fraction(r, "D") for c, r in child_rows) / den
        E = sum(Fraction(nodes[c]["weight"]) * _node_fraction(r, "DE") for c, r in child_rows) / den
        frontier = sorted(
            (leaf for leaf in _leaves_under(indexed, ref) if results[leaf]["lifecycle"] in _FRONTIER_LIFECYCLE),
            key=lambda r: nodes[r]["number"],
        )
        leaf_rows = [results[leaf] for leaf in _leaves_under(indexed, ref)]
        critical = [r for leaf, r in zip(_leaves_under(indexed, ref), leaf_rows) if nodes[leaf]["critical"]]
        states = {r["state"] for r in leaf_rows}
        unreleasable = [
            leaf for leaf in _leaves_under(indexed, ref) if (results[leaf].get("plan") or {}).get("releasable") is False
        ]
        if D == 1 and all(r["lifecycle"] in _TERMINAL for r in leaf_rows) and node["reserve_weight"] == 0:
            state = "COMPLETE"
        elif any(r["state"] == "STALE" for r in critical):
            state = "STALE"
        elif "EVIDENCE_STALE" in states or "EVIDENCE_GAP" in states:
            state = "EVIDENCE_GAP"
        elif any(r["state"] in {"QUIET", "RECOVERING"} for r in critical) or "STALE" in states:
            state = "QUIET"
        elif any(r["state"].startswith("WAITING") for r in critical):
            state = "WAITING"
        elif frontier:
            state = "ACTIVE"
        elif mode == "ENFORCED" and unreleasable:
            state = "PLAN_GAP"  # nothing is moving and the plan, not the executors, is why
        else:
            state = "IDLE"
        warnings: list[str] = []
        if node["reserve_weight"]:
            warnings.append(f"UNDECOMPOSED_RESERVE:{node['reserve_weight']}")
        if unreleasable:
            warnings.append(f"DECOMPOSITION_BLOCKED_LEAVES:{len(unreleasable)}")
        result = {
            "lifecycle": {"COMPLETE": "COMPLETE", "IDLE": "IDLE", "PLAN_GAP": "IDLE"}.get(state, "ACTIVE"),
            "state": state,
            "progress": {
                "D": percent(D),
                "E": percent(E),
                "ratio": {"D": ratio_text(D), "E": ratio_text(E)},
            },
            "_fractions": {"D": D, "DE": E},
            "frontier": {"count": len(frontier), "leaves": frontier},
            "children": node["children"],
            "warnings": warnings,
        }
        if mode != "OFF":
            result["plan"] = {"mode": mode, "not_releasable": len(unreleasable), "leaves": unreleasable}
        results[ref] = result
        return result

    visit(indexed["root"])

    out_nodes: dict[str, Any] = {}
    for ref in indexed["order"]:
        node = nodes[ref]
        data = results[ref]
        chain = lineage(indexed, ref)
        public = {k: v for k, v in data.items() if not k.startswith("_")}
        public.update(
            {
                "ref": ref,
                "kind": node["kind"],
                "identity": {
                    "programme": indexed["programme"].get("id"),
                    "root": indexed["root"],
                    "lineage": chain,
                    "responsibility_id": node.get("responsibility_id"),
                },
                "weight": node["weight"],
            }
        )
        if node["kind"] == "LEAF":
            public["material"] = {
                "primary_pr": node.get("primary_pr"),
                "candidate_sha": data["frontier"]["material_candidate"],
            }
            prefix = _leaf_prefix(indexed, ref, data)
        elif node["kind"] == "INTERMEDIATE":
            prefix = _group_prefix(indexed, ref, data, "Φ", with_frontier=True)
        else:
            prefix = _group_prefix(indexed, ref, data, "Π", with_frontier=False)
        public["title_prefix"] = prefix
        public["light"] = STATE_LIGHT[data["state"]]
        out_nodes[ref] = public

    return {
        "schema": PROJECTION_SCHEMA,
        "authority": AUTHORITY,
        "protocol_line": PROTOCOL_LINE,
        "programme": indexed["programme"],
        "root": indexed["root"],
        "nodes": out_nodes,
        "rejected_facts": rejected,
        "input_digest": canonical_digest(
            {
                "graph": indexed["digest"],
                "ledger": [
                    {"source": str((e or {}).get("source") or ""), "order": (e or {}).get("order"), "facts": (e or {}).get("facts")}
                    for e in ledger
                ],
                "observations": {str(k): v for k, v in sorted(observations.items())},
            }
        ),
    }


def _node_fraction(result: Mapping[str, Any], key: str) -> Fraction:
    return result["_fractions"][key]


def _leaves_under(indexed: Mapping[str, Any], ref: str) -> list[str]:
    node = indexed["nodes"][ref]
    if node["kind"] == "LEAF":
        return [ref]
    out: list[str] = []
    for child in node["children"]:
        out.extend(_leaves_under(indexed, child))
    return out


def _leaf_prefix(indexed: Mapping[str, Any], ref: str, data: Mapping[str, Any]) -> str:
    node = indexed["nodes"][ref]
    pr = node.get("primary_pr")
    path = _path_text(indexed, ref) + (f" → PR#{ref_number(pr)}" if pr else "")
    p = data["progress"]
    tokens = [f"R:P{p['P']}/E{p['E']}"]
    if data["active_unit"]:
        tokens.append(data["active_unit"])
    elif data["state"] != "COMPLETE":
        tokens.append("NO_ACTIVE_UNIT")
    tokens.append(data["state"])
    return f"{STATE_LIGHT[data['state']]} [{path}] " + " · ".join(tokens)


def _group_prefix(
    indexed: Mapping[str, Any], ref: str, data: Mapping[str, Any], scope: str, *, with_frontier: bool
) -> str:
    path = _path_text(indexed, ref)
    leaves = data["frontier"]["leaves"]
    if with_frontier and leaves:
        path += " → " + _frontier_summary(indexed, leaves)
    p = data["progress"]
    light = STATE_LIGHT[data["state"]]
    return f"{light} [{path}] {scope}:D{p['D']}/E{p['E']} · F{data['frontier']['count']} · {data['state']}"


def expected_titles(projection: Mapping[str, Any], base_titles: Mapping[str, str]) -> dict[str, str]:
    """Derive the exact issue title for every node from the current human base titles."""
    out = {}
    for ref, node in projection["nodes"].items():
        _, base = split_title(base_titles.get(ref, ""))
        out[ref] = render_title(node["title_prefix"], base)
    return out


# --------------------------------------------------------------------------
# continuation admission: reconstruct, never continue from conversation memory
# --------------------------------------------------------------------------


def classify_continuation(text: str) -> bool:
    return bool(CONTINUATION_COMMANDS.match(str(text or "")))


def admit(projection: Mapping[str, Any], leaf_ref: str, command: str = "continue") -> dict[str, Any]:
    """Compact reconstruction proof for a continuation command. Pure; changes nothing."""
    nodes = projection["nodes"]
    if leaf_ref not in nodes or nodes[leaf_ref]["kind"] != "LEAF":
        raise DelpError(f"{leaf_ref} is not a LEAF in the projection")
    leaf = nodes[leaf_ref]
    lineage_refs = leaf["identity"]["lineage"]
    ancestors = [nodes[r] for r in lineage_refs[:-1]]
    health = leaf["evidence"]["health"]
    gaps = leaf["evidence"]["gaps"]
    plan = leaf.get("plan")
    if leaf["lifecycle"] in _TERMINAL:
        action = "NONE"
        next_text = f"{leaf['lifecycle']} — no further unit; select the next responsibility from the plan"
    elif plan and plan["mode"] == "ENFORCED" and not plan["releasable"]:
        action = "FIX_PLAN"
        shown = "; ".join(f"{b['code']} ({b['detail']})" for b in plan["blockers"][:3])
        more = f"; +{len(plan['blockers']) - 3} more" if len(plan["blockers"]) > 3 else ""
        also = f"; evidence is also {health}" if health != "CURRENT" else ""
        next_text = (
            f"FIX_PLAN before coding — {shown}{more}{also} — "
            "request a plan update (split or reweight) from the Coordinator; do not start or continue units"
        )
    elif health != "CURRENT":
        action = "RECOVER_EVIDENCE"
        detail = ", ".join(f"{g['unit']}:{g['reason']}" for g in gaps) or health
        next_text = f"RECOVER_EVIDENCE before new coding — {detail}"
    elif leaf["active_unit"]:
        action = "CONTINUE_UNIT"
        tail = f" — {leaf['next']['action']}" if leaf["next"]["action"] else ""
        next_text = f"{leaf['active_unit']}{tail}"
    else:
        action = "AWAIT_RESULT"
        next_text = "all declared units complete — publish the scoped result"
    report = {
        "command": command,
        "is_continuation": classify_continuation(command),
        "leaf": leaf_ref,
        "lineage": lineage_refs,
        "state": leaf["state"],
        "evidence_health": health,
        "action": action,
        "recovery_required": action == "RECOVER_EVIDENCE",
        "next": next_text,
        "blocker": leaf["blocker"],
        "owner_action": leaf["owner_action"],
        "ancestors": [
            {"ref": a["ref"], "scope": "Φ" if a["kind"] == "INTERMEDIATE" else "Π", "D": a["progress"]["D"], "E": a["progress"]["E"]}
            for a in ancestors
        ],
        "child": {"P": leaf["progress"]["P"], "E": leaf["progress"]["E"], "unit": leaf["active_unit"]},
        "material": leaf["material"],
        "evidence_candidate": leaf["frontier"]["evidence_candidate"],
        "authority_effects": [],  # a continuation never changes parent, denominator, scope or merge authority
    }
    if plan:  # present only when the decomposition gate is not OFF
        report["plan"] = plan
        report["plan_fix_required"] = action == "FIX_PLAN"
    return report


def render_checkpoint(report: Mapping[str, Any]) -> str:
    short = lambda sha: (sha or "UNKNOWN")[:7]  # noqa: E731
    path = " → ".join(f"#{ref_number(r)}" for r in report["lineage"])
    pr = report["material"].get("primary_pr")
    if pr:
        path += f" → PR#{ref_number(pr)}"
    evidence = (
        f"CURRENT @ {short(report['material'].get('candidate_sha'))}"
        if report["evidence_health"] == "CURRENT"
        else f"{report['evidence_health']} (evidence @ {short(report['evidence_candidate'])}, "
        f"live @ {short(report['material'].get('candidate_sha'))})"
    )
    lines = [
        "CONTINUE CHECKPOINT",
        "",
        f"PATH: {path}",
        f"CHILD: R:P{report['child']['P']}/E{report['child']['E']} · {report['child']['unit'] or 'NO_ACTIVE_UNIT'} · {report['state']}",
        f"EVIDENCE: {evidence}",
    ]
    plan = report.get("plan")
    if plan:
        codes = ", ".join(b["code"] for b in plan["blockers"])
        if plan["blockers"]:
            lines.append(f"PLAN: {'NOT_RELEASEABLE' if plan['mode'] == 'ENFORCED' else 'WOULD_BLOCK (advisory)'} — {codes}")
        elif plan["advisories"]:
            lines.append(f"PLAN: RELEASABLE — ADVISORY: {', '.join(a['code'] for a in plan['advisories'])}")
        else:
            lines.append("PLAN: RELEASABLE")
    for ancestor in reversed(report["ancestors"]):
        label = "ROOT" if ancestor["scope"] == "Π" else "PARENT"
        lines.append(f"{label}: #{ref_number(ancestor['ref'])} {ancestor['scope']}:D{ancestor['D']}/E{ancestor['E']}")
    lines += [
        f"BLOCKER: {report['blocker']}",
        f"OWNER_ACTION: {report['owner_action']}",
        f"NEXT: {report['next']}",
    ]
    return "\n".join(lines)


# --------------------------------------------------------------------------
# provider surface: compare-and-swap by version + digest (no last-writer-wins)
# --------------------------------------------------------------------------


def status_document(node_projection: Mapping[str, Any], *, version: int, digest: str, programme: Mapping[str, Any]) -> dict[str, Any]:
    """LIVE_STATUS_V1 document written to the provider for one node."""
    body = {k: v for k, v in node_projection.items() if k not in {"title_prefix"}}
    return {
        "schema": STATUS_SCHEMA,
        "authority": AUTHORITY,
        "programme": programme.get("id"),
        "node": body,
        "projection": {"version": version, "input_digest": digest},
    }


def render_status_comment(document: Mapping[str, Any]) -> str:
    version = document["projection"]["version"]
    digest = document["projection"]["input_digest"]
    return "\n".join(
        [
            STATUS_START,
            f"<!-- relay-delp:version={version} digest={digest} -->",
            "LIVE_STATUS_V1 — derived projection; never authority; agents do not edit this comment.",
            "",
            "```json",
            json.dumps(document, indent=2, sort_keys=True, ensure_ascii=False),
            "```",
            STATUS_END,
        ]
    )


def read_status_marker(body: str) -> dict[str, Any] | None:
    if STATUS_START not in str(body or ""):
        return None
    match = _STATUS_MARKER.search(body)
    if not match:
        return None
    return {"version": int(match.group("version")), "input_digest": match.group("digest")}


class InMemoryStore:
    """Reference provider with real compare-and-swap semantics (used by tests and dry runs)."""

    def __init__(self, titles: Mapping[str, str] | None = None) -> None:
        self.titles = dict(titles or {})
        self.status: dict[str, dict[str, Any]] = {}
        self.writes: list[tuple[str, int | None, int]] = []

    def read(self, ref: str) -> dict[str, Any] | None:
        row = self.status.get(ref)
        if row is None:
            return {"version": None, "input_digest": None, "title": self.titles.get(ref, "")}
        return {"version": row["version"], "input_digest": row["digest"], "title": self.titles.get(ref, "")}

    def write(self, ref: str, expected_version: int | None, document: Mapping[str, Any], title: str) -> int:
        row = self.status.get(ref)
        observed = row["version"] if row else None
        if observed != expected_version:
            raise ProjectionConflict(f"{ref}: expected version {expected_version}, observed {observed}")
        version = (observed or 0) + 1
        final = json.loads(canonical_json(document))
        final["projection"]["version"] = version
        self.status[ref] = {"version": version, "digest": final["projection"]["input_digest"], "document": final}
        self.titles[ref] = title
        self.writes.append((ref, expected_version, version))
        return version


def apply_projection(
    store: Any,
    ref: str,
    compute: Callable[[], tuple[dict[str, Any], str]],
    *,
    max_attempts: int = 4,
    on_conflict: Callable[[], None] | None = None,
) -> dict[str, Any]:
    """Write one node projection with compare-and-swap.

    `compute()` returns `(status_document_without_final_version, title)`. After a lost race
    `on_conflict()` drops cached inputs so the next attempt recomputes from fresh truth and
    converges instead of overwriting.
    """
    last: Exception | None = None
    for attempt in range(1, max_attempts + 1):
        current = store.read(ref) or {"version": None, "input_digest": None, "title": ""}
        expected = current["version"]
        document, title = compute()
        digest = document["projection"]["input_digest"]
        if current["input_digest"] == digest and current.get("title") == title:
            return {"status": "UNCHANGED", "version": expected, "attempts": attempt}
        try:
            version = store.write(ref, expected, document, title)
        except ProjectionConflict as exc:
            last = exc
            if on_conflict:
                on_conflict()
            continue
        return {
            "status": "WRITTEN",
            "version": version,
            "attempts": attempt,
            "title_corrected": current.get("title") not in ("", title),
        }
    raise ProjectionConflict(f"{ref}: lost compare-and-swap {max_attempts} times: {last}")


class _InputCache:
    """Compute the projection once per pass; recompute from fresh inputs after a conflict."""

    def __init__(
        self,
        graph: Any,
        ledger_provider: Callable[[], Iterable[Mapping[str, Any]]],
        observation_provider: Callable[[], Mapping[str, Mapping[str, Any]]],
    ) -> None:
        self.graph = graph
        self.ledger_provider = ledger_provider
        self.observation_provider = observation_provider
        self._projection: dict[str, Any] | None = None

    def invalidate(self) -> None:
        self._projection = None

    def projection(self) -> dict[str, Any]:
        if self._projection is None:
            self._projection = project(self.graph, self.ledger_provider(), self.observation_provider())
        return self._projection


def sync_projection(
    store: Any,
    graph: Any,
    ledger_provider: Callable[[], Iterable[Mapping[str, Any]]],
    observation_provider: Callable[[], Mapping[str, Mapping[str, Any]]],
    base_titles: Mapping[str, str],
) -> dict[str, Any]:
    """Project every node and write each with compare-and-swap. Leaves first, root last."""
    indexed = validate_graph(graph)
    cache = _InputCache(graph, ledger_provider, observation_provider)
    report: dict[str, Any] = {}
    ordered = sorted(indexed["nodes"], key=lambda r: (-len(lineage(indexed, r)), indexed["nodes"][r]["number"]))
    for ref in ordered:

        def compute(ref: str = ref) -> tuple[dict[str, Any], str]:
            projection = cache.projection()
            node = projection["nodes"][ref]
            _, base = split_title(base_titles.get(ref, ""))
            return (
                status_document(node, version=0, digest=projection["input_digest"], programme=projection["programme"]),
                render_title(node["title_prefix"], base),
            )

        report[ref] = apply_projection(store, ref, compute, on_conflict=cache.invalidate)
    return report


def ledger_from_github(transport: Any, graph: Any) -> list[dict[str, Any]]:
    """Collect CHECKPOINT_FACTS_V1 blocks from each declared leaf issue's comments, oldest first.

    Blocks from untrusted authors are kept but tagged, so the projector rejects them visibly
    (`rejected_facts`) instead of silently dropping or, worse, believing them.
    """
    indexed = validate_graph(graph)
    allowlist = {str(a) for a in (indexed["programme"].get("fact_authors") or [])}
    ledger: list[dict[str, Any]] = []
    for ref, node in indexed["nodes"].items():
        if node["kind"] != "LEAF":
            continue
        for comment in transport.list_comments(node["number"]):
            login = str((comment.get("user") or {}).get("login") or "")
            trusted = (
                login in allowlist
                if allowlist
                else str(comment.get("author_association") or "") in TRUSTED_ASSOCIATIONS
            )
            for facts in extract_facts_blocks(str(comment.get("body") or "")):
                row = {
                    "source": f"{ref}#issuecomment-{comment.get('id')}",
                    "order": int(comment.get("id") or 0),
                    "facts": facts,
                }
                if not trusted:
                    row["untrusted_author"] = login or "UNKNOWN"
                ledger.append(row)
    return ledger


def plan_github(transport: Any, graph: Any) -> dict[str, Any]:
    """Read-only dry run of `sync-github`: what would change, what drifted, what was rejected. Writes nothing."""
    indexed = validate_graph(graph)
    titles = {ref: str(transport.get_issue(ref_number(ref)).get("title") or "") for ref in indexed["nodes"]}
    projection = project(graph, ledger_from_github(transport, graph), observe_github(transport, graph))
    drift = {}
    for ref, node in projection["nodes"].items():
        result = title_drift(titles[ref], node["title_prefix"])
        if result["status"] != "OK":
            drift[ref] = result
    return {
        "would_write_titles": len(drift),
        "drift": drift,
        "rejected_facts": projection["rejected_facts"],
        "expected_titles": expected_titles(projection, titles),
        "input_digest": projection["input_digest"],
    }


def observe_github(transport: Any, graph: Any) -> dict[str, dict[str, Any]]:
    """Observe the live candidate for every leaf from provider truth, never from agent facts.

    A leaf's candidate is its primary PR head, or the head of `candidate_ref` when it has no PR.
    """
    indexed = validate_graph(graph)
    observed: dict[str, dict[str, Any]] = {}
    for ref, node in indexed["nodes"].items():
        if node["kind"] != "LEAF":
            continue
        pr = node.get("primary_pr")
        if pr:
            pull = transport.get_pull(ref_number(pr))
            observed[ref] = {
                "candidate_sha": str((pull.get("head") or {}).get("sha") or "") or None,
                "pr_state": "MERGED" if pull.get("merged") else str(pull.get("state") or "UNKNOWN").upper(),
            }
        elif node.get("candidate_ref"):
            observed[ref] = {"candidate_sha": str(transport.get_commit_sha(node["candidate_ref"]) or "") or None}
    return observed


class GhTransport:
    """`gh api` transport. Kept thin so tests can substitute a fake."""

    def __init__(self, repository: str) -> None:
        self.repository = repository

    def _gh(self, *args: str) -> Any:
        proc = subprocess.run(
            ["gh", "api", *args], text=True, capture_output=True, encoding="utf-8", errors="replace"
        )
        if proc.returncode:
            raise DelpError(proc.stderr.strip() or "gh api failed")
        return json.loads(proc.stdout) if proc.stdout.strip() else {}

    def get_commit_sha(self, ref: str) -> str:
        return str(self._gh(f"repos/{self.repository}/commits/{ref}").get("sha") or "")

    def get_issue(self, number: int) -> dict[str, Any]:
        return self._gh(f"repos/{self.repository}/issues/{number}")

    def get_pull(self, number: int) -> dict[str, Any]:
        return self._gh(f"repos/{self.repository}/pulls/{number}")

    def list_comments(self, number: int) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        page = 1
        while True:
            chunk = self._gh("--method", "GET", f"repos/{self.repository}/issues/{number}/comments", "-f", "per_page=100", "-f", f"page={page}")
            if not isinstance(chunk, list):
                raise DelpError("GitHub comments response must be a list")
            rows.extend(chunk)
            if len(chunk) < 100:
                return rows
            page += 1

    def post_comment(self, number: int, body: str) -> dict[str, Any]:
        return self._gh("--method", "POST", f"repos/{self.repository}/issues/{number}/comments", "-f", f"body={body}")

    def patch_comment(self, comment_id: int, body: str) -> dict[str, Any]:
        return self._gh("--method", "PATCH", f"repos/{self.repository}/issues/comments/{comment_id}", "-f", f"body={body}")

    def patch_title(self, number: int, title: str) -> dict[str, Any]:
        return self._gh("--method", "PATCH", f"repos/{self.repository}/issues/{number}", "-f", f"title={title}")


class GitHubStore:
    """Managed LIVE_STATUS comment + issue title per node, written with detect-and-retry CAS.

    GitHub has no conditional update for comments or titles. DELP therefore re-reads the
    version marker immediately before writing, writes version N+1, and reads back; a lost
    race is detected (version/digest mismatch) and retried from freshly recomputed inputs.
    """

    def __init__(self, transport: Any) -> None:
        self.transport = transport

    def _managed(self, number: int) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
        matches = [c for c in self.transport.list_comments(number) if STATUS_START in str(c.get("body") or "")]
        if len(matches) > 1:
            raise DelpError(f"#{number}: multiple managed LIVE_STATUS comments")
        if not matches:
            return None, None
        return matches[0], read_status_marker(str(matches[0].get("body") or ""))

    def read(self, ref: str) -> dict[str, Any] | None:
        number = ref_number(ref)
        comment, marker = self._managed(number)
        title = str(self.transport.get_issue(number).get("title") or "")
        return {
            "version": marker["version"] if marker else None,
            "input_digest": marker["input_digest"] if marker else None,
            "title": title,
            "comment_id": comment.get("id") if comment else None,
        }

    def write(self, ref: str, expected_version: int | None, document: Mapping[str, Any], title: str) -> int:
        number = ref_number(ref)
        comment, marker = self._managed(number)
        observed = marker["version"] if marker else None
        if observed != expected_version:
            raise ProjectionConflict(f"{ref}: expected version {expected_version}, observed {observed}")
        version = (observed or 0) + 1
        final = json.loads(canonical_json(document))
        final["projection"]["version"] = version
        body = render_status_comment(final)
        if comment:
            self.transport.patch_comment(int(comment["id"]), body)
        else:
            self.transport.post_comment(number, body)
        if str(self.transport.get_issue(number).get("title") or "") != title:
            self.transport.patch_title(number, title)
        _, back = self._managed(number)
        if not back or back["version"] != version or back["input_digest"] != final["projection"]["input_digest"]:
            raise ProjectionConflict(f"{ref}: readback lost the race (wrote {version}, saw {back})")
        return version


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def _load_structured(path: Path) -> Any:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() in {".yaml", ".yml"}:
        try:
            import yaml  # type: ignore
        except ImportError as exc:  # pragma: no cover
            raise DelpError("PyYAML is required to read YAML inputs") from exc
        return yaml.safe_load(text)
    return json.loads(text)


def _load_ledger(paths: list[Path]) -> list[dict[str, Any]]:
    ledger: list[dict[str, Any]] = []
    for path in paths:
        if path.suffix.lower() in {".md", ".txt"}:
            for facts in extract_facts_blocks(path.read_text(encoding="utf-8")):
                ledger.append({"source": str(path), "order": len(ledger), "facts": facts})
            continue
        document = _load_structured(path)
        rows = document if isinstance(document, list) else [document]
        for row in rows:
            facts = row.get("facts") if isinstance(row, Mapping) and "facts" in row else row
            if isinstance(facts, Mapping) and FACTS_KEY in facts:
                facts = {**facts[FACTS_KEY], "schema": FACTS_SCHEMA}
            ledger.append({"source": f"{path}", "order": len(ledger), "facts": facts})
    return ledger


def _emit(value: Any, output: Path | None) -> None:
    text = json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=f"DELP {PROTOCOL_LINE}: facts in, projections out.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    vg = sub.add_parser("validate-graph")
    vg.add_argument("--graph", type=Path, required=True)

    vf = sub.add_parser("validate-facts", help="Reject agent-authored progress/titles; exit 1 on any violation.")
    vf.add_argument("facts", type=Path, nargs="+")

    dc = sub.add_parser(
        "decompose-check",
        help="Judge the plan against the decomposition policy; exit 1 on blockers when the effective mode is ENFORCED.",
    )
    dc.add_argument("--graph", type=Path, required=True)
    dc.add_argument("--mode", choices=POLICY_MODES, help="Override programme.decomposition_policy.mode for this run.")
    dc.add_argument("--facts", type=Path, nargs="*", default=[], help="Skip leaves these facts show COMPLETE or SUPERSEDED.")
    dc.add_argument("--observations", type=Path)
    dc.add_argument("--json", action="store_true")

    gd = sub.add_parser("graph-diff", help="Check that a re-plan conserves progress and records its scope changes; exit 1 on blockers.")
    gd.add_argument("--old", type=Path, required=True, help="The plan being replaced (e.g. the PR base version).")
    gd.add_argument("--new", type=Path, required=True)
    gd.add_argument("--json", action="store_true")

    pr = sub.add_parser("project")
    pr.add_argument("--graph", type=Path, required=True)
    pr.add_argument("--facts", type=Path, nargs="*", default=[])
    pr.add_argument("--observations", type=Path)
    pr.add_argument("--base-titles", type=Path)
    pr.add_argument("--output", type=Path)

    ad = sub.add_parser("admit", help="Reconstruct-before-continue checkpoint for continue/proceed/next/resume.")
    ad.add_argument("--graph", type=Path, required=True)
    ad.add_argument("--facts", type=Path, nargs="*", default=[])
    ad.add_argument("--observations", type=Path)
    ad.add_argument("--leaf", required=True)
    ad.add_argument("--command", default="continue")
    ad.add_argument("--json", action="store_true")

    vt = sub.add_parser("verify-titles", help="Report hand-edited, stale, missing or legacy titles; exit 2 on drift.")
    vt.add_argument("--graph", type=Path, required=True)
    vt.add_argument("--facts", type=Path, nargs="*", default=[])
    vt.add_argument("--observations", type=Path)
    vt.add_argument("--actual-titles", type=Path, required=True)

    gh = sub.add_parser(
        "sync-github",
        help="Observe live PR heads + CHECKPOINT_FACTS_V1 comments, then write titles and LIVE_STATUS with compare-and-swap (uses gh).",
    )
    gh.add_argument("--graph", type=Path, required=True)
    gh.add_argument("--repository", required=True)
    gh.add_argument("--dry-run", action="store_true", help="Read-only: report drift, rejected facts and expected titles; write nothing.")

    args = parser.parse_args(argv)
    for stream in (sys.stdout, sys.stderr):  # titles carry emoji and arrows; never depend on the console codepage
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8")
            except (ValueError, OSError):  # pragma: no cover - exotic stream
                pass
    try:
        if args.cmd == "validate-graph":
            indexed = validate_graph(_load_structured(args.graph))
            print(f"OK {len(indexed['nodes'])} nodes root={indexed['root']} digest={indexed['digest']}")
            return 0
        if args.cmd == "validate-facts":
            failed = 0
            for path in args.facts:
                rows = _load_ledger([path])
                if not rows:
                    failed += 1
                    print(f"REJECTED {path}", file=sys.stderr)
                    print(f"  - no {FACTS_KEY} block found (a malformed fence or key is not a valid publication)", file=sys.stderr)
                for row in rows:
                    errors = validate_facts(row["facts"])
                    if errors:
                        failed += 1
                        print(f"REJECTED {row['source']}", file=sys.stderr)
                        for error in errors:
                            print(f"  - {error}", file=sys.stderr)
            return 1 if failed else 0
        if args.cmd == "graph-diff":
            diff = graph_diff(_load_structured(args.old), _load_structured(args.new))
            if args.json:
                _emit(diff, None)
            else:
                print(render_graph_diff(diff))
            return 0 if diff["conserved"] else 1

        graph = _load_structured(args.graph)
        if args.cmd == "decompose-check":
            closed: list[str] = []
            if args.facts:
                seen = project(graph, _load_ledger(args.facts), _load_structured(args.observations) if args.observations else {})
                closed = [r for r, n in seen["nodes"].items() if n["kind"] == "LEAF" and n["lifecycle"] in _TERMINAL]
            report = decomposition_report(graph, args.mode, closed)
            if args.json:
                _emit(report, None)
            else:
                print(render_decomposition(report))
            return 1 if report["mode"] == "ENFORCED" and report["summary"]["not_releasable"] else 0
        if args.cmd == "sync-github" and args.dry_run:
            _emit(plan_github(GhTransport(args.repository), graph), None)
            return 0
        if args.cmd == "sync-github":
            transport = GhTransport(args.repository)
            store = GitHubStore(transport)
            indexed = validate_graph(graph)
            base_titles = {
                ref: str(transport.get_issue(ref_number(ref)).get("title") or "") for ref in indexed["nodes"]
            }
            report = sync_projection(
                store,
                graph,
                lambda: ledger_from_github(transport, graph),
                lambda: observe_github(transport, graph),
                base_titles,
            )
            _emit(report, None)
            return 0
        ledger = _load_ledger(args.facts)
        observations = _load_structured(args.observations) if getattr(args, "observations", None) else {}
        projection = project(graph, ledger, observations)
        if args.cmd == "project":
            if args.base_titles:
                projection["expected_titles"] = expected_titles(projection, _load_structured(args.base_titles))
            _emit(projection, args.output)
            return 0
        if args.cmd == "admit":
            report = admit(projection, args.leaf, args.command)
            if args.json:
                _emit(report, None)
            else:
                print(render_checkpoint(report))
            return 0
        if args.cmd == "verify-titles":
            actual = _load_structured(args.actual_titles)
            drift = {}
            for ref, node in projection["nodes"].items():
                result = title_drift(str(actual.get(ref, "")), node["title_prefix"])
                if result["status"] != "OK":
                    drift[ref] = result
            _emit({"drift": drift, "checked": len(projection["nodes"])}, None)
            return 2 if drift else 0
    except DelpError as exc:
        print(f"DELP error: {exc}", file=sys.stderr)
        return 1
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
