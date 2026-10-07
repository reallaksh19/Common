#!/usr/bin/env python3
"""Durable Execution Lineage and Projection (DELP) for Engineering Relay V3.5.

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
import hashlib
import json
import re
import subprocess
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping

PROTOCOL_LINE = "V3.5"
SCHEMA_PREFIX = "relay-v3.5-delp"
AUTHORITY = "DERIVED_PROJECTION_ONLY"
FACTS_SCHEMA = f"{SCHEMA_PREFIX}-checkpoint-facts"
GRAPH_SCHEMA = f"{SCHEMA_PREFIX}-execution-graph"
PROJECTION_SCHEMA = f"{SCHEMA_PREFIX}-projection"
STATUS_SCHEMA = f"{SCHEMA_PREFIX}-live-status"
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
                uid = str((unit or {}).get("id") or "")
                if not _UNIT_ID.fullmatch(uid) or uid in seen_units:
                    raise GraphError(f"{ref}.units: invalid or duplicate unit id {uid!r}")
                seen_units.add(uid)
                clean_units.append({"id": uid, "weight": _positive_int(unit.get("weight"), f"{ref}.units.{uid}.weight")})
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

    return {
        "programme": dict(programme),
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

    def visit(ref: str) -> dict[str, Any]:
        node = nodes[ref]
        if node["kind"] == "LEAF":
            leaf = compute_leaf(node, accepted.get(ref, []), observations.get(node["number"]))
            results[ref] = leaf
            return leaf
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
        else:
            state = "IDLE"
        warnings: list[str] = []
        if node["reserve_weight"]:
            warnings.append(f"UNDECOMPOSED_RESERVE:{node['reserve_weight']}")
        result = {
            "lifecycle": state if state in {"COMPLETE", "IDLE"} else "ACTIVE",
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
    if leaf["lifecycle"] in _TERMINAL:
        action = "NONE"
        next_text = f"{leaf['lifecycle']} — no further unit; select the next responsibility from the plan"
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
    return {
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

        graph = _load_structured(args.graph)
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
