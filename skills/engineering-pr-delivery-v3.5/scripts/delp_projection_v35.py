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
import copy
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
import types
from datetime import datetime, timezone
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
OBSERVATION_SCHEMA = f"{SCHEMA_PREFIX}-responsibility-observation"
CONDITION_SCHEMA = f"{SCHEMA_PREFIX}-responsibility-condition"
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
HANDOVER_EVENTS = {"OFFERED", "ACCEPTED"}
HANDOVER_MODES = {"CONTINUITY", "INDEPENDENT_RECONSTRUCTION"}
HANDOVER_RESULTS = {"RECONCILED", "DRIFT_FOUND", "INSUFFICIENT_GROUNDING", "OWNER_DECISION_REQUIRED"}
HANDOVER_AUTHORITY_CLASSES = {
    "PRODUCTION",
    "CANDIDATE_GENERATION",
    "REVIEW_ONLY",
    "VALIDATION_BENCHMARK",
    "HISTORICAL",
}
ENTRY_EVENTS = {"PREPARED", "EXECUTION_END"}
ENTRY_MODES = {"TAKEOVER_RECONCILE"}

# Decomposition gate. A graph without `programme.decomposition_policy` behaves exactly as before
# (mode OFF). `decompose-check` always evaluates; the mode decides whether projection/admission act on it.
POLICY_MODES = ("OFF", "ADVISORY", "ENFORCED")
WORK_CLASSES = ("PRODUCT", "MECHANICAL", "GATE")
CLAIM_KINDS = ("SEMANTIC", "DELIVERY_GATE")
CLAIM_RELATIONS = ("OWN", "ENABLES", "GATE")
TOPOLOGY_PROPOSAL_KINDS = ("LEAF", "ADJACENT_CHILDREN")
TOPOLOGY_SEMANTIC_COHESION = ("COHESIVE", "MIXED", "UNKNOWN")
TOPOLOGY_DEPENDENCY_CLOSURE = ("CLOSED", "OPEN", "UNKNOWN")
TOPOLOGY_VERIFICATION_CLOSURE = ("CLOSED", "DEFERRED", "UNKNOWN")
TOPOLOGY_UNCERTAINTY = ("LOW", "MATERIAL", "BLOCKING")
TOPOLOGY_CHANGE_IMPACT = ("LOCAL", "BOUNDED_MULTI_STAGE", "CROSS_CUTTING", "UNKNOWN")
TOPOLOGY_EXECUTION_HORIZON = ("SHORT", "MULTI_STEP", "LONG_OR_AMBIGUOUS")
TOPOLOGY_MUTATION_DOMAINS = (
    "LOCAL_FILES",
    "GIT_HISTORY",
    "REMOTE_BRANCH",
    "GITHUB_ISSUE",
    "GITHUB_PR",
    "CI",
    "BROWSER",
    "EXTERNAL_SERVICE",
)
TOPOLOGY_RECOVERY_RADIUS = ("SMALL", "MULTI_SURFACE", "AMBIGUOUS_EXTERNAL")
TOPOLOGY_HANDOFF_COST = ("LOW", "MATERIAL", "HIGH")
TOPOLOGY_CROSS_CHILD_COHESION = ("LOW", "HIGH")
TOPOLOGY_STABLE_CUT_FIELDS = (
    "output_contract",
    "independent_oracle",
    "consumer_stable",
    "risk_reduction",
    "handoff_economy",
)
TRANSFORMATION_BOUNDARIES = (
    "WIRE_SCHEMA",
    "ENGINE_VALIDATION",
    "COMPATIBILITY_NORMALIZATION",
    "PROVIDER_ADAPTER",
    "AUTHORITY_POLICY",
    "DERIVED_RECONCILIATION",
    "ACTUATION_UI_PROJECTION",
    "CUSTODY_FENCING",
    "ASSURANCE_POLICY",
    "MIGRATION",
    "QUALIFICATION_DOCS",
    "PRODUCT_IMPLEMENTATION",
)
PLAN_UPDATE_KINDS = ("SCOPE_EXPANSION", "SCOPE_REDUCTION", "UNIT_REWEIGHT", "UNIT_DROPPED", "POLICY_CHANGE")
# Display scale for "unit points". Percentages never use it: every share is an exact Fraction of the programme.
DEFAULT_TOTAL_WEIGHT = 10000
# NOT_RELEASEABLE only replaces these leaf states; every other state is more urgent or already means "not being worked".
_PLAN_OVERLAID_STATES = frozenset({"NOT_STARTED", "ACTIVE"})
# Provider-observed pull request states that prove work exists for a leaf. With no accepted facts such a leaf is
# UNMATERIALIZED (unknown), never NOT_STARTED (zero): the ledger is missing, the work may well be finished.
_PR_ACTIVITY_STATES = frozenset({"OPEN", "MERGED", "CLOSED"})
# Defaults follow the programme's written budgets (PROGRAMME_DECOMPOSITION_PROGRESS.md) and sit at the
# Young/Daly optimum for the interruption rate observed on the Common executors (see the contract doc).
DEFAULT_POLICY: dict[str, Any] = {
    "mode": "OFF",
    "units": {"min": 3, "max": 8, "max_share_percent": 40},
    "leaf_budget": {"target_loc": 700, "hard_loc": 1500, "target_minutes": 15, "hard_minutes": 20},
    "min_leaf_target_loc": 50,
    "require": {
        "outcome": True,
        "verify": True,
        "write_surface": True,
        "size_budget": True,
        "transformation_boundaries": False,
    },
}
_BUDGET_KEYS = ("target_loc", "hard_loc", "target_minutes", "hard_minutes")

# Agent health: delivery-continuity telemetry, advisory only. It is observed or derived, never declared; it never moves a
# percentage, a state or a title and never blocks work. Repository telemetry may locate evidence and constrain delivery;
# it never measures value, quality or capability. Defaults are the programme's own written rules (checkpoint triggers at
# 250 / 400 and the hard ceiling at 500 / 700 reviewable lines; the third stream loss in one executor lifecycle plans a
# handover); elapsed time alone is deliberately not a rule.
HEALTH_MODES = ("OFF", "ADVISORY")
HEALTH_RANK = {"OK": 0, "UNOBSERVED": 1, "WATCH": 2, "AT_RISK": 3}  # UNOBSERVED is never healthy, and never worse than a known concern
HEALTH_VERDICT = {"OK": "HEALTHY", "UNOBSERVED": "UNOBSERVED", "WATCH": "WATCH", "AT_RISK": "AT_RISK"}
DEFAULT_HEALTH_POLICY: dict[str, Any] = {
    "mode": "OFF",
    "checkpoint": {"watch_added_loc": 250, "at_risk_added_loc": 500, "watch_changed_loc": 400, "at_risk_changed_loc": 700},
    "drift": {"watch_behind": 1, "at_risk_behind": 20},
    "interruptions": {"watch": 1, "at_risk": 3},
}

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
        "currentness",
        "graph_generation",
        "graph_digest",
        "observed_generation",
        "contract_current",
        "observation",
        "observations",
        "provider_observation",
        "provider_visibility",
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
        "execution",
        "next",
        "blocker",
        "owner_action",
        "entry",
        "handover",
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
_EP_ID = re.compile(r"^(?:EP-[A-Za-z0-9][A-Za-z0-9._-]*|EP\.(?:[1-9][0-9]*|REPO|INTERNAL)\.[1-9][0-9]*)$")
_LEASE_ID = re.compile(r"^(?:LEASE-[A-Za-z0-9][A-Za-z0-9._-]*|LEASE\.(?:[1-9][0-9]*|REPO|INTERNAL)\.[1-9][0-9]*)$")
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
    "HANDOFF": LIGHT_ATTENTION,
    "RECONSTRUCTING": LIGHT_ATTENTION,
    "WAITING_CI": LIGHT_WAITING,
    "WAITING_TOOL": LIGHT_WAITING,
    "WAITING_EXTERNAL": LIGHT_WAITING,
    "WAITING_PROVIDER_VISIBILITY": LIGHT_WAITING,
    "WAITING_DEPENDENCY": LIGHT_WAITING,
    "WAITING": LIGHT_WAITING,
    "RECOVERING": LIGHT_ATTENTION,
    "QUIET": LIGHT_ATTENTION,
    "EVIDENCE_GAP": LIGHT_ATTENTION,
    "EVIDENCE_STALE": LIGHT_ATTENTION,
    "NOT_RELEASEABLE": LIGHT_ATTENTION,  # leaf whose plan fails the decomposition gate (ENFORCED mode)
    "PLAN_GAP": LIGHT_ATTENTION,  # ancestor with at least one non-releasable leaf
    "UNMATERIALIZED": LIGHT_ATTENTION,  # the provider shows work but the facts ledger is empty: unknown, not zero
    "STALE": LIGHT_STALE,
    "COMPLETE": LIGHT_COMPLETE,
    "SUPERSEDED": LIGHT_IDLE,
    "NOT_STARTED": LIGHT_IDLE,
    "PAUSED": LIGHT_IDLE,
    "IDLE": LIGHT_IDLE,
}
HEALTH_LIGHT = {"HEALTHY": LIGHT_ACTIVE, "UNOBSERVED": LIGHT_IDLE, "WATCH": LIGHT_ATTENTION, "AT_RISK": LIGHT_STALE}

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


OBSERVATION_VISIBILITY = frozenset({"OBSERVED", "UNAVAILABLE"})


def validate_observation(observation: Any) -> list[str]:
    """Validate one RESPONSIBILITY_OBSERVATION_V1 wire record."""
    if not isinstance(observation, Mapping):
        return ["observation: must be a mapping"]

    errors: list[str] = []
    allowed_top = {"schema", "visibility", "material", "custody", "liveness", "check", "diff"}
    if observation.get("schema") != OBSERVATION_SCHEMA:
        errors.append(f"schema: must be {OBSERVATION_SCHEMA}")
    visibility = observation.get("visibility")
    if not isinstance(visibility, str) or visibility not in OBSERVATION_VISIBILITY:
        errors.append(f"visibility: one of {sorted(OBSERVATION_VISIBILITY)}")
    extra = sorted(set(map(str, observation)) - allowed_top)
    if extra:
        errors.append(f"observation: unknown fields {extra}")

    def mapping(name: str, allowed: set[str]) -> Mapping[str, Any] | None:
        if name not in observation:
            return None
        value = observation[name]
        if not isinstance(value, Mapping):
            errors.append(f"{name}: must be a mapping")
            return None
        unknown = sorted(set(map(str, value)) - allowed)
        if unknown:
            errors.append(f"{name}: unknown fields {unknown}")
        return value

    def nonnegative(value: Any) -> bool:
        return isinstance(value, int) and not isinstance(value, bool) and value >= 0

    material = mapping("material", {"candidate_sha", "base_sha", "pr_state", "ahead_by", "behind_by"})
    if material is not None:
        for key in ("candidate_sha", "base_sha"):
            value = material.get(key)
            if value is not None and not _SHA.fullmatch(str(value)):
                errors.append(f"material.{key}: must be 40-hex lowercase or null")
        if "pr_state" in material:
            state = material["pr_state"]
            if not isinstance(state, str) or state not in {"OPEN", "MERGED", "CLOSED", "UNKNOWN"}:
                errors.append("material.pr_state: OPEN, MERGED, CLOSED or UNKNOWN")
        for key in ("ahead_by", "behind_by"):
            if key in material and not nonnegative(material[key]):
                errors.append(f"material.{key}: must be a non-negative integer")

    custody = mapping("custody", {"interruptions"})
    if custody is not None and custody.get("interruptions") is not None:
        interruptions = custody["interruptions"]
        if not isinstance(interruptions, Mapping):
            errors.append("custody.interruptions: must be a mapping")
        else:
            unknown = sorted(set(map(str, interruptions)) - {"coverage_from", "losses"})
            if unknown:
                errors.append(f"custody.interruptions: unknown fields {unknown}")
            if "coverage_from" in interruptions and not isinstance(interruptions["coverage_from"], str):
                errors.append("custody.interruptions.coverage_from: must be a string")
            if "losses" in interruptions and (
                not isinstance(interruptions["losses"], list)
                or any(not isinstance(item, Mapping) for item in interruptions["losses"])
            ):
                errors.append("custody.interruptions.losses: must be an array of mappings")

    liveness = mapping("liveness", {"value"})
    if liveness is not None:
        value = liveness.get("value")
        if not isinstance(value, str) or value not in OBSERVED_LIVENESS:
            errors.append(f"liveness.value: one of {sorted(OBSERVED_LIVENESS)}")

    check = mapping("check", {"result", "candidate_sha", "name"})
    if check is not None:
        if "result" in check:
            result = check["result"]
            if not isinstance(result, str) or result not in {"SUCCESS", "FAILURE", "PENDING"}:
                errors.append("check.result: SUCCESS, FAILURE or PENDING")
        if "candidate_sha" in check and not _SHA.fullmatch(str(check["candidate_sha"])):
            errors.append("check.candidate_sha: must be 40-hex lowercase")
        if "name" in check and (not isinstance(check["name"], str) or not check["name"].strip()):
            errors.append("check.name: must be a non-empty string")

    diff = mapping("diff", {"additions", "deletions", "since_checkpoint"})
    if diff is not None:
        for key in ("additions", "deletions"):
            if key in diff and not nonnegative(diff[key]):
                errors.append(f"diff.{key}: must be a non-negative integer")
        if "since_checkpoint" in diff:
            since = diff["since_checkpoint"]
            if not isinstance(since, Mapping):
                errors.append("diff.since_checkpoint: must be a mapping")
            else:
                unknown = sorted(set(map(str, since)) - {"additions", "deletions"})
                if unknown:
                    errors.append(f"diff.since_checkpoint: unknown fields {unknown}")
                for key in ("additions", "deletions"):
                    if key in since and not nonnegative(since[key]):
                        errors.append(f"diff.since_checkpoint.{key}: must be a non-negative integer")
    return errors


def normalize_observation(observation: Any) -> dict[str, Any]:
    """Normalize typed or legacy-flat observer input to DELP's existing flat projection vocabulary."""
    if observation is None:
        return {}
    if not isinstance(observation, Mapping):
        raise DelpError("observation: must be a mapping")

    if "schema" not in observation:
        typed_only = {"visibility", "material", "custody", "diff"} & set(map(str, observation))
        if typed_only or isinstance(observation.get("liveness"), Mapping):
            raise DelpError(
                "typed-shaped observation is missing required schema: "
                + ", ".join(sorted(typed_only or {"liveness"}))
            )
        out = dict(observation)
        category_fields = {
            "MATERIAL": {"candidate_sha", "base_sha", "pr_state", "ahead_by", "behind_by"},
            "CUSTODY": {"interruptions"},
            "LIVENESS": {"liveness"},
            "CHECK": {"check"},
            "DIFF": {"additions", "deletions", "since_checkpoint"},
        }
        out["_observation"] = {
            "schema": "LEGACY_FLAT_OBSERVATION",
            "visibility": "OBSERVED",
            "categories": {
                category: ("OBSERVED" if any(key in observation for key in fields) else "UNOBSERVED")
                for category, fields in category_fields.items()
            },
        }
        return out

    errors = validate_observation(observation)
    if errors:
        raise DelpError("invalid RESPONSIBILITY_OBSERVATION_V1: " + "; ".join(errors))

    visibility = str(observation["visibility"])
    sections = {
        "MATERIAL": observation.get("material"),
        "CUSTODY": observation.get("custody"),
        "LIVENESS": observation.get("liveness"),
        "CHECK": observation.get("check"),
        "DIFF": observation.get("diff"),
    }
    categories = {
        category: (
            "UNAVAILABLE"
            if visibility == "UNAVAILABLE"
            else "OBSERVED"
            if isinstance(section, Mapping) and bool(section)
            else "UNOBSERVED"
        )
        for category, section in sections.items()
    }
    out: dict[str, Any] = {}
    if visibility == "OBSERVED":
        material = observation.get("material") or {}
        for key in ("candidate_sha", "base_sha", "pr_state", "ahead_by", "behind_by"):
            if key in material and material[key] is not None:
                out[key] = material[key]

        custody = observation.get("custody") or {}
        if "interruptions" in custody:
            out["interruptions"] = copy.deepcopy(custody["interruptions"])

        liveness = observation.get("liveness") or {}
        if "value" in liveness:
            out["liveness"] = liveness["value"]

        check = observation.get("check") or {}
        if check:
            out["check"] = copy.deepcopy(check)

        diff = observation.get("diff") or {}
        for key in ("additions", "deletions", "since_checkpoint"):
            if key in diff:
                out[key] = copy.deepcopy(diff[key])

    out["_observation"] = {
        "schema": OBSERVATION_SCHEMA,
        "visibility": visibility,
        "categories": categories,
    }
    return out


def normalize_observations(
    indexed: Mapping[str, Any],
    observations: Mapping[Any, Any] | None,
) -> dict[int, dict[str, Any]]:
    """Resolve observation locators to declared leaves without crossing repository boundaries."""
    if observations is None:
        return {}
    if not isinstance(observations, Mapping):
        raise DelpError("observations: must be a mapping keyed by declared leaf reference")

    leaves = [ref for ref, node in indexed["nodes"].items() if node["kind"] == "LEAF"]
    declared_repository = str(indexed["programme"].get("repository") or "").strip().lower()
    normalized: dict[int, dict[str, Any]] = {}
    for supplied_ref, observation in observations.items():
        try:
            supplied_repo, _ = parse_ref(supplied_ref)
            if supplied_repo and declared_repository and "/" in supplied_repo:
                supplied_repo = supplied_repo.lower()
                if supplied_repo != declared_repository:
                    raise DelpError(
                        f"repository qualifier {supplied_repo!r} does not match programme.repository {declared_repository!r}"
                    )
            leaf_ref = next((ref for ref in leaves if same_ref(ref, supplied_ref)), None)
        except DelpError as exc:
            raise DelpError(f"observation key {supplied_ref!r}: {exc}") from exc
        if leaf_ref is None:
            raise DelpError(f"observation key {supplied_ref!r}: not a declared LEAF in this graph")

        number = indexed["nodes"][leaf_ref]["number"]
        if number in normalized:
            raise DelpError(f"observation key {supplied_ref!r}: duplicate observation for {leaf_ref}")
        normalized[number] = normalize_observation(observation)
    return normalized


CONDITION_TYPES = frozenset(
    {
        "PlanReady",
        "SpecCurrent",
        "MaterialObserved",
        "EvidenceCurrent",
        "DependenciesReady",
        "CustodySafe",
        "AssuranceSatisfied",
        "ProviderVisible",
    }
)
CONDITION_ORDER = (
    "PlanReady",
    "SpecCurrent",
    "MaterialObserved",
    "EvidenceCurrent",
    "DependenciesReady",
    "CustodySafe",
    "AssuranceSatisfied",
    "ProviderVisible",
)
CONDITION_STATUSES = frozenset({"TRUE", "FALSE", "UNKNOWN", "NOT_APPLICABLE"})
_CONDITION_FIELDS = frozenset(
    {"type", "status", "reason", "message", "observed_generation", "candidate_sha", "source_refs"}
)


def validate_condition(condition: Any) -> list[str]:
    """Validate one canonical derived Responsibility condition record."""
    if not isinstance(condition, Mapping):
        return ["condition: must be a mapping"]

    errors: list[str] = []
    keys = set(map(str, condition))
    missing = sorted(_CONDITION_FIELDS - keys)
    extra = sorted(keys - _CONDITION_FIELDS)
    if missing:
        errors.append(f"condition: missing fields {missing}")
    if extra:
        errors.append(f"condition: unknown fields {extra}")

    kind = condition.get("type")
    if not isinstance(kind, str) or kind not in CONDITION_TYPES:
        errors.append(f"type: one of {sorted(CONDITION_TYPES)}")

    status = condition.get("status")
    if not isinstance(status, str) or status not in CONDITION_STATUSES:
        errors.append(f"status: one of {sorted(CONDITION_STATUSES)}")

    for key in ("reason", "message"):
        value = condition.get(key)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{key}: must be a non-blank string")

    generation = condition.get("observed_generation")
    generation_is_integer = (
        isinstance(generation, int) and not isinstance(generation, bool)
    ) or (
        isinstance(generation, float) and generation.is_integer()
    )
    if generation is not None and (not generation_is_integer or generation < 1):
        errors.append("observed_generation: positive integer or null")

    candidate = condition.get("candidate_sha")
    if candidate is not None and (
        not isinstance(candidate, str) or not _SHA.fullmatch(candidate)
    ):
        errors.append("candidate_sha: 40-hex lowercase or null")

    refs = condition.get("source_refs")
    if not isinstance(refs, list):
        errors.append("source_refs: must be an array")
    else:
        if any(not isinstance(ref, str) or not ref.strip() for ref in refs):
            errors.append("source_refs: every item must be a non-blank string")
        elif len(refs) != len(set(refs)):
            errors.append("source_refs: items must be unique")
    return errors


def condition_record(
    condition_type: str,
    status: str,
    reason: str,
    message: str,
    *,
    observed_generation: int | float | None = None,
    candidate_sha: str | None = None,
    source_refs: Iterable[str] = (),
) -> dict[str, Any]:
    """Build one validated condition record, mapping caller-shape errors to DelpError."""
    if isinstance(source_refs, (str, bytes, bytearray, Mapping, set, frozenset)):
        raise DelpError(
            "condition source_refs: must be an ordered iterable of refs, not text/bytes/mapping/set"
        )
    try:
        refs = list(source_refs)
    except TypeError as exc:
        raise DelpError("condition source_refs: must be an iterable of refs") from exc

    record = {
        "type": condition_type,
        "status": status,
        "reason": reason,
        "message": message,
        "observed_generation": observed_generation,
        "candidate_sha": candidate_sha,
        "source_refs": refs,
    }
    errors = validate_condition(record)
    if errors:
        raise DelpError("invalid responsibility condition: " + "; ".join(errors))
    return record


_ACTUAL_NEXT_MODULE: Any = None


def _actual_next_module() -> Any:
    """Load the standalone R-P2-NEXT engine against this exact DELP contract.

    Some retained tests load DELP with exec_module() without registering it in
    sys.modules. actual_next_v35 imports only CONDITION_ORDER, DelpError and
    validate_condition from delp_projection_v35; provide those exact objects
    through a temporary module shim so integration never loads a second,
    inconsistent DELP instance.
    """
    global _ACTUAL_NEXT_MODULE
    if _ACTUAL_NEXT_MODULE is not None:
        return _ACTUAL_NEXT_MODULE

    path = Path(__file__).resolve().with_name("actual_next_v35.py")
    spec = importlib.util.spec_from_file_location("actual_next_v35_for_projection", path)
    if spec is None or spec.loader is None:
        raise DelpError(f"actual-next module could not be loaded from {path}")

    module = importlib.util.module_from_spec(spec)
    existing = sys.modules.get("delp_projection_v35")
    shimmed = existing is None
    if shimmed:
        shim = types.ModuleType("delp_projection_v35")
        shim.CONDITION_ORDER = CONDITION_ORDER
        shim.DelpError = DelpError
        shim.validate_condition = validate_condition
        sys.modules["delp_projection_v35"] = shim
    try:
        spec.loader.exec_module(module)
    finally:
        if shimmed:
            sys.modules.pop("delp_projection_v35", None)

    _ACTUAL_NEXT_MODULE = module
    return module


def _derive_actual_next_v35(leaf: Mapping[str, Any]) -> dict[str, Any]:
    decision = _actual_next_module().derive_actual_next(leaf)
    if not isinstance(decision, Mapping):
        raise DelpError("actual-next integration returned a non-mapping decision")
    return dict(decision)


def _plan_spec_conditions(
    indexed: Mapping[str, Any],
    ref: str,
    leaf: Mapping[str, Any],
    accepted_records: Iterable[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    """Derive PlanReady and SpecCurrent from existing plan/spec authority only."""
    node = indexed["nodes"][ref]
    generation = node.get("spec_generation")
    lifecycle = str(leaf.get("lifecycle") or "")
    mode = indexed["policy"]["mode"]
    plan = leaf.get("plan")

    if lifecycle in _TERMINAL:
        plan_status = "NOT_APPLICABLE"
        plan_reason = "PLAN_NOT_APPLICABLE_TERMINAL"
        plan_message = f"{lifecycle} Responsibility has no further execution plan to release."
    elif mode == "OFF":
        plan_status = "TRUE"
        plan_reason = "PLAN_GATE_OFF"
        plan_message = "Decomposition enforcement is OFF; plan readiness does not block execution."
    elif mode == "ADVISORY":
        plan_status = "TRUE"
        blockers = list((plan or {}).get("blockers") or [])
        if blockers:
            plan_reason = "PLAN_ADVISORY_WOULD_BLOCK"
            codes = ", ".join(sorted({str(row["code"]) for row in blockers}))
            plan_message = f"Advisory decomposition findings would block if enforced: {codes}."
        else:
            plan_reason = "PLAN_RELEASEABLE"
            plan_message = "The current advisory plan has no blocking decomposition findings."
    elif plan is None:
        plan_status = "UNKNOWN"
        plan_reason = "PLAN_RELEASEABILITY_UNOBSERVED"
        plan_message = "Enforced plan readiness was not projected."
    elif plan["releasable"]:
        plan_status = "TRUE"
        plan_reason = "PLAN_RELEASEABLE"
        plan_message = "The current enforced plan is releaseable."
    else:
        plan_status = "FALSE"
        plan_reason = "PLAN_NOT_RELEASEABLE"
        codes = ", ".join(sorted({str(row["code"]) for row in plan["blockers"]}))
        plan_message = f"The current enforced plan is not releaseable: {codes or 'blocking finding'}."

    records = list(accepted_records)
    if not indexed["stable_identity_mode"] or generation is None or not node.get("contract_digest"):
        spec_status = "UNKNOWN"
        spec_reason = "SPEC_BINDING_UNAVAILABLE"
        spec_message = "Stable Responsibility contract binding is unavailable."
        spec_sources = [f"{ref}:contract"]
    elif records:
        spec_status = "TRUE"
        spec_reason = "SPEC_BINDING_CURRENT"
        spec_message = (
            "Accepted facts are bound to the current Responsibility id, spec generation and contract digest."
        )
        spec_sources = []
        for record in records:
            source = str(record.get("_source") or "").strip()
            if source and source not in spec_sources:
                spec_sources.append(source)
        if not spec_sources:
            spec_sources = [f"{ref}:accepted-facts"]
    else:
        spec_status = "UNKNOWN"
        spec_reason = "SPEC_BINDING_UNOBSERVED"
        spec_message = "No accepted fact basis establishes current Responsibility contract binding."
        spec_sources = [f"{ref}:accepted-facts"]

    return [
        condition_record(
            "PlanReady",
            plan_status,
            plan_reason,
            plan_message,
            observed_generation=generation,
            candidate_sha=None,
            source_refs=[f"{ref}:plan"],
        ),
        condition_record(
            "SpecCurrent",
            spec_status,
            spec_reason,
            spec_message,
            observed_generation=generation,
            candidate_sha=None,
            source_refs=spec_sources,
        ),
    ]



def _provider_evidence_conditions(
    indexed: Mapping[str, Any],
    ref: str,
    leaf: Mapping[str, Any],
    observation: Mapping[str, Any] | None,
    accepted_records: Iterable[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    """Derive provider/material/evidence conditions from normalized existing truth."""
    node = indexed["nodes"][ref]
    generation = node.get("spec_generation")
    observation = dict(observation or {})
    meta = observation.get("_observation") if isinstance(observation.get("_observation"), Mapping) else {}
    visibility = str(meta.get("visibility") or "")
    categories = meta.get("categories") if isinstance(meta.get("categories"), Mapping) else {}
    material_visibility = str(categories.get("MATERIAL") or "")

    if visibility == "OBSERVED":
        provider_status = "TRUE"
        provider_reason = "PROVIDER_VISIBLE"
        provider_message = "Provider observation was successfully obtained."
    else:
        provider_status = "UNKNOWN"
        provider_reason = "PROVIDER_UNAVAILABLE" if visibility == "UNAVAILABLE" else "PROVIDER_UNOBSERVED"
        provider_message = (
            "Provider observation is unavailable."
            if visibility == "UNAVAILABLE"
            else "Provider visibility was not observed."
        )

    candidate = observation.get("candidate_sha")
    candidate_sha = str(candidate) if isinstance(candidate, str) and _SHA.fullmatch(candidate) else None
    material_signal = candidate_sha is not None or _provider_signal(observation) is not None
    if material_visibility == "OBSERVED":
        if material_signal:
            material_status = "TRUE"
            material_reason = "MATERIAL_OBSERVED"
            material_message = "Provider observation contains current material or candidate signal."
        else:
            material_status = "FALSE"
            material_reason = "MATERIAL_NOT_PRESENT"
            material_message = "Provider material was observed but no current material/candidate signal exists."
    else:
        material_status = "UNKNOWN"
        material_reason = (
            "MATERIAL_UNAVAILABLE" if material_visibility == "UNAVAILABLE" else "MATERIAL_UNOBSERVED"
        )
        material_message = (
            "Provider material visibility is unavailable."
            if material_visibility == "UNAVAILABLE"
            else "Provider material visibility was not observed."
        )

    records = list(accepted_records)
    evidence_health = str((leaf.get("evidence") or {}).get("health") or "")
    if not records:
        evidence_status = "UNKNOWN"
        evidence_reason = "EVIDENCE_BASIS_UNOBSERVED"
        evidence_message = "No accepted fact basis exists from which to establish evidence currentness."
    elif evidence_health == "CURRENT":
        evidence_status = "TRUE"
        evidence_reason = "EVIDENCE_CURRENT"
        evidence_message = "Accepted evidence is current for the observed candidate."
    elif evidence_health in {"GAP", "STALE_CANDIDATE"}:
        evidence_status = "FALSE"
        evidence_reason = (
            "EVIDENCE_STALE_CANDIDATE"
            if evidence_health == "STALE_CANDIDATE"
            else "EVIDENCE_GAP"
        )
        evidence_message = (
            "Accepted evidence is stale against the observed candidate."
            if evidence_health == "STALE_CANDIDATE"
            else "Accepted facts contain incomplete or invalid current evidence."
        )
    else:
        evidence_status = "UNKNOWN"
        evidence_reason = "EVIDENCE_UNVERIFIABLE"
        evidence_message = "Evidence currentness cannot be established from the available provider truth."

    evidence_source = str((leaf.get("evidence") or {}).get("latest_source") or "").strip()
    return [
        condition_record(
            "ProviderVisible",
            provider_status,
            provider_reason,
            provider_message,
            observed_generation=generation,
            candidate_sha=candidate_sha,
            source_refs=[f"{ref}:provider"],
        ),
        condition_record(
            "MaterialObserved",
            material_status,
            material_reason,
            material_message,
            observed_generation=generation,
            candidate_sha=candidate_sha,
            source_refs=[f"{ref}:provider-material"],
        ),
        condition_record(
            "EvidenceCurrent",
            evidence_status,
            evidence_reason,
            evidence_message,
            observed_generation=generation,
            candidate_sha=leaf.get("frontier", {}).get("evidence_candidate"),
            source_refs=[evidence_source or f"{ref}:evidence"],
        ),
    ]



def _dependency_condition(
    indexed: Mapping[str, Any],
    ref: str,
    leaf: Mapping[str, Any],
) -> dict[str, Any]:
    """Derive DependenciesReady from the already-derived declared dependency projection only."""
    node = indexed["nodes"][ref]
    generation = node.get("spec_generation")
    dependencies = leaf.get("dependencies")
    if not isinstance(dependencies, Mapping):
        return condition_record(
            "DependenciesReady",
            "UNKNOWN",
            "DEPENDENCY_STATE_UNOBSERVED",
            "Dependency readiness was not projected.",
            observed_generation=generation,
            candidate_sha=None,
            source_refs=[f"{ref}:dependencies"],
        )

    declared = [str(value) for value in dependencies.get("declared") or []]
    if not declared:
        return condition_record(
            "DependenciesReady",
            "NOT_APPLICABLE",
            "NO_DECLARED_DEPENDENCIES",
            "The Responsibility declares no execution dependencies.",
            observed_generation=generation,
            candidate_sha=None,
            source_refs=[f"{ref}:dependencies"],
        )

    blocking = list(dependencies.get("blocking") or [])
    if bool(dependencies.get("ready")) and not blocking:
        return condition_record(
            "DependenciesReady",
            "TRUE",
            "DEPENDENCIES_COMPLETE",
            "Every declared predecessor Responsibility is complete.",
            observed_generation=generation,
            candidate_sha=None,
            source_refs=declared,
        )

    unresolved = [
        row
        for row in blocking
        if not isinstance(row, Mapping)
        or not str(row.get("lifecycle") or "").strip()
    ]
    if unresolved:
        return condition_record(
            "DependenciesReady",
            "UNKNOWN",
            "DEPENDENCY_STATE_UNKNOWN",
            "At least one declared predecessor has unresolved lifecycle truth.",
            observed_generation=generation,
            candidate_sha=None,
            source_refs=declared,
        )

    shown = ", ".join(
        f"{row['ref']}:{row['lifecycle']}"
        for row in blocking
        if isinstance(row, Mapping)
    )
    return condition_record(
        "DependenciesReady",
        "FALSE",
        "DEPENDENCIES_INCOMPLETE",
        f"Declared predecessor Responsibilities are not complete: {shown}.",
        observed_generation=generation,
        candidate_sha=None,
        source_refs=declared,
    )



def _custody_assurance_placeholders(
    indexed: Mapping[str, Any],
    ref: str,
) -> list[dict[str, Any]]:
    """Represent not-yet-implemented P3/P4 axes without fabricating safe/satisfied truth."""
    generation = indexed["nodes"][ref].get("spec_generation")
    return [
        condition_record(
            "CustodySafe",
            "NOT_APPLICABLE",
            "CUSTODY_POLICY_NOT_IMPLEMENTED",
            "P3 custody epoch/fencing authority is not implemented in the current kernel.",
            observed_generation=generation,
            candidate_sha=None,
            source_refs=["programme:P3-custody"],
        ),
        condition_record(
            "AssuranceSatisfied",
            "NOT_APPLICABLE",
            "ASSURANCE_POLICY_NOT_IMPLEMENTED",
            "P4 assurance actor/policy authority is not implemented in the current kernel.",
            observed_generation=generation,
            candidate_sha=None,
            source_refs=["programme:P4-assurance"],
        ),
    ]


def _finalize_condition_set(
    conditions: Iterable[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    """Validate and canonically order one complete eight-condition read model."""
    rows = [dict(row) for row in conditions]
    by_type: dict[str, dict[str, Any]] = {}
    for row in rows:
        errors = validate_condition(row)
        if errors:
            raise DelpError("invalid derived responsibility condition: " + "; ".join(errors))
        kind = str(row["type"])
        if kind in by_type:
            raise DelpError(f"duplicate derived responsibility condition {kind}")
        by_type[kind] = row
    missing = [kind for kind in CONDITION_ORDER if kind not in by_type]
    extra = sorted(set(by_type) - set(CONDITION_ORDER))
    if missing or extra:
        raise DelpError(
            f"incomplete derived responsibility condition set: missing={missing}, extra={extra}"
        )
    return [by_type[kind] for kind in CONDITION_ORDER]

def graph_digest_basis(graph: Mapping[str, Any]) -> dict[str, Any]:
    """Canonical graph input used for identity/currentness.

    Legacy graphs that omit programme.graph_generation are normalized to generation 1,
    so adding the explicit default does not manufacture semantic drift. In stable-identity
    mode a leaf contract_digest is derived data, so an optional matching assertion is not
    allowed to manufacture graph drift merely by being present or absent.
    """
    value = copy.deepcopy(dict(graph))
    programme = dict(value.get("programme") or {})
    stable_identity_mode = "graph_generation" in programme
    programme["graph_generation"] = programme.get("graph_generation", 1)
    value["programme"] = programme
    if stable_identity_mode:
        for node in value.get("nodes") or []:
            if isinstance(node, dict) and node.get("kind") == "LEAF":
                node.pop("contract_digest", None)
    return value


def responsibility_contract_basis(
    node: Mapping[str, Any],
    nodes: Mapping[str, Mapping[str, Any]],
    claims_by_id: Mapping[str, Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    """Semantic/execution contract whose digest binds evidence, excluding provider/topology metadata."""
    dependencies = sorted(
        str(nodes[ref].get("responsibility_id") or ref)
        for ref in node.get("depends_on") or []
    )
    claims_by_id = claims_by_id or {}
    claim_relationships = []
    for relation in node.get("claim_relationships") or []:
        claim = claims_by_id.get(relation["claim_id"])
        if claim is None:
            raise GraphError(
                f"{node.get('ref', '<leaf>')}.claim_relationships: missing normalized claim {relation['claim_id']!r}"
            )
        claim_relationships.append(
            {
                "claim_id": claim["id"],
                "claim": claim["claim"],
                "kind": claim["kind"],
                "shared": claim["shared"],
                "relation": relation["relation"],
            }
        )
    claim_relationships.sort(key=lambda row: (row["claim_id"], row["relation"]))
    return {
        "responsibility_id": node.get("responsibility_id"),
        "claim_relationships": claim_relationships,
        "outcome": node.get("outcome"),
        "units": sorted(
            (
                {
                    "id": unit["id"],
                    "verify": unit.get("verify"),
                    "outcome": unit.get("outcome"),
                }
                for unit in node.get("units") or []
            ),
            key=lambda row: row["id"],
        ),
        "delivery_gates": sorted(
            ({"id": gate["id"]} for gate in node.get("delivery_gates") or []),
            key=lambda row: row["id"],
        ),
        "verification": sorted(node.get("verification") or []),
        "write_surface": sorted(node.get("write_surface") or []),
        "depends_on": dependencies,
        "size_budget": node.get("size_budget"),
        "work_class": node.get("work_class"),
    }


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
        if responsibility.get("id") is not None and (
            not isinstance(responsibility["id"], str) or not responsibility["id"].strip()
        ):
            errors.append("responsibility.id: must be a non-empty string")
        spec_generation = responsibility.get("spec_generation")
        if spec_generation is not None and (
            isinstance(spec_generation, bool) or not isinstance(spec_generation, int) or spec_generation < 1
        ):
            errors.append("responsibility.spec_generation: must be a positive integer")
        contract_digest = responsibility.get("contract_digest")
        if contract_digest is not None and not _DIGEST.fullmatch(str(contract_digest)):
            errors.append("responsibility.contract_digest: must be sha256:<64 hex>")
        extra = set(map(str, responsibility)) - {"issue", "id", "spec_generation", "contract_digest"}
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

    execution = facts.get("execution")
    if execution is not None:
        if not isinstance(execution, Mapping):
            errors.append("execution: must be a mapping")
        else:
            allowed_execution = {"ep", "lease", "executor", "custody_epoch"}
            missing_execution = sorted(allowed_execution - set(map(str, execution)))
            extra_execution = sorted(set(map(str, execution)) - allowed_execution)
            if missing_execution:
                errors.append(f"execution: missing fields {missing_execution}")
            if extra_execution:
                errors.append(f"execution: unknown fields {extra_execution}")
            if not _EP_ID.fullmatch(str(execution.get("ep") or "")):
                errors.append("execution.ep: required canonical EP identifier")
            if not _LEASE_ID.fullmatch(str(execution.get("lease") or "")):
                errors.append("execution.lease: required canonical LEASE identifier")
            executor = execution.get("executor")
            if not isinstance(executor, str) or not executor.strip():
                errors.append("execution.executor: non-empty string required")
            custody_epoch = execution.get("custody_epoch")
            if isinstance(custody_epoch, bool) or not isinstance(custody_epoch, int) or custody_epoch < 1:
                errors.append("execution.custody_epoch: positive integer required")

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

    entry_fact = facts.get("entry")
    if entry_fact is not None:
        if not isinstance(entry_fact, Mapping):
            errors.append("entry: must be a mapping")
        else:
            allowed = {
                "event", "mode", "session_digest", "plan_digest", "child_ref", "child_contract_digest",
                "sequence", "phase_plan_ref", "reconciliation_ref", "previous_leaf_ref",
                "previous_evidence_ref", "evidence_refs",
            }
            extra = set(map(str, entry_fact)) - allowed
            if extra:
                errors.append(f"entry: unknown fields {sorted(extra)}")
            event = entry_fact.get("event")
            if event not in ENTRY_EVENTS:
                errors.append(f"entry.event: one of {sorted(ENTRY_EVENTS)}")
            if entry_fact.get("mode") not in ENTRY_MODES:
                errors.append(f"entry.mode: one of {sorted(ENTRY_MODES)}")
            for key in ("session_digest", "plan_digest"):
                if not _DIGEST.fullmatch(str(entry_fact.get(key) or "")):
                    errors.append(f"entry.{key}: required sha256:<64 hex>")
            contract = entry_fact.get("child_contract_digest")
            if contract is not None and not _DIGEST.fullmatch(str(contract)):
                errors.append("entry.child_contract_digest: sha256:<64 hex> when present")
            for key in ("child_ref", "previous_leaf_ref"):
                value = entry_fact.get(key)
                if value is not None:
                    try:
                        parse_ref(value)
                    except DelpError as exc:
                        errors.append(f"entry.{key}: {exc}")
            if entry_fact.get("child_ref") is None:
                errors.append("entry.child_ref: required")
            sequence = entry_fact.get("sequence")
            if isinstance(sequence, bool) or not isinstance(sequence, int) or sequence < 1:
                errors.append("entry.sequence: positive integer required")
                sequence = None
            _check_refs(entry_fact.get("evidence_refs"), "entry.evidence_refs", errors)
            if not entry_fact.get("evidence_refs"):
                errors.append("entry.evidence_refs: at least one durable evidence ref required")
            if event == "PREPARED":
                for key in ("phase_plan_ref", "reconciliation_ref"):
                    value = entry_fact.get(key)
                    if not isinstance(value, str) or not value.strip():
                        errors.append(f"entry.{key}: non-empty string required for PREPARED")
            for key in ("phase_plan_ref", "reconciliation_ref", "previous_evidence_ref"):
                value = entry_fact.get(key)
                if value is not None and (not isinstance(value, str) or not value.strip()):
                    errors.append(f"entry.{key}: non-empty string when present")
            previous_leaf = entry_fact.get("previous_leaf_ref")
            previous_evidence = entry_fact.get("previous_evidence_ref")
            if sequence is not None and sequence > 1 and (not previous_leaf or not previous_evidence):
                errors.append("entry: sequence >1 requires previous_leaf_ref and previous_evidence_ref")
            if sequence == 1 and (previous_leaf is not None or previous_evidence is not None):
                errors.append("entry: sequence 1 cannot carry previous entry linkage")

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

    handover = facts.get("handover")
    if handover is not None:
        if not isinstance(handover, Mapping):
            errors.append("handover: must be a mapping")
        else:
            extra = set(map(str, handover)) - {
                "event", "mode", "predecessor_ref", "frontier_digest", "decision_at_risk", "result",
                "challenge_digest", "question_ids", "answer_evidence", "root_classification",
            }
            if extra:
                errors.append(f"handover: unknown fields {sorted(extra)}")
            event = handover.get("event")
            mode = handover.get("mode")
            if event not in HANDOVER_EVENTS:
                errors.append(f"handover.event: one of {sorted(HANDOVER_EVENTS)}")
            if mode not in HANDOVER_MODES:
                errors.append(f"handover.mode: one of {sorted(HANDOVER_MODES)}")
            digest = handover.get("frontier_digest")
            if not _DIGEST.fullmatch(str(digest or "")):
                errors.append("handover.frontier_digest: required sha256:<64 hex>")
            decision = handover.get("decision_at_risk")
            if not isinstance(decision, str) or not decision.strip() or len(decision) > 200 or "\n" in decision:
                errors.append("handover.decision_at_risk: single non-empty line, at most 200 characters")
            predecessor = handover.get("predecessor_ref")
            if predecessor is not None and (not isinstance(predecessor, str) or not predecessor.strip()):
                errors.append("handover.predecessor_ref: non-empty string when present")
            hresult = handover.get("result")
            if hresult is not None and hresult not in HANDOVER_RESULTS:
                errors.append(f"handover.result: one of {sorted(HANDOVER_RESULTS)}")

            challenge_digest = handover.get("challenge_digest")
            if challenge_digest is not None and not _DIGEST.fullmatch(str(challenge_digest)):
                errors.append("handover.challenge_digest: sha256:<64 hex> when present")
            question_ids = handover.get("question_ids")
            if question_ids is not None:
                if (
                    not isinstance(question_ids, list)
                    or not question_ids
                    or not all(isinstance(q, str) and re.fullmatch(r"Q[1-9][0-9]*", q) for q in question_ids)
                    or len(question_ids) != len(set(question_ids))
                ):
                    errors.append("handover.question_ids: non-empty unique Q<n> list when present")

            answer_evidence = handover.get("answer_evidence")
            answer_ids: list[str] = []
            if answer_evidence is not None:
                if not isinstance(answer_evidence, list) or not answer_evidence:
                    errors.append("handover.answer_evidence: non-empty array when present")
                else:
                    for index, answer in enumerate(answer_evidence):
                        label = f"handover.answer_evidence[{index}]"
                        if not isinstance(answer, Mapping):
                            errors.append(f"{label}: must be a mapping")
                            continue
                        extra_answer = set(map(str, answer)) - {
                            "question_id", "evidence_refs", "live_refs", "evidence_summary", "authority_classifications"
                        }
                        if extra_answer:
                            errors.append(f"{label}: unknown fields {sorted(extra_answer)}")
                        qid = answer.get("question_id")
                        if not isinstance(qid, str) or not re.fullmatch(r"Q[1-9][0-9]*", qid):
                            errors.append(f"{label}.question_id: required Q<n>")
                        else:
                            answer_ids.append(qid)
                        _check_refs(answer.get("evidence_refs"), f"{label}.evidence_refs", errors)
                        if not answer.get("evidence_refs"):
                            errors.append(f"{label}.evidence_refs: at least one durable evidence ref required")
                        live_refs = answer.get("live_refs")
                        if not isinstance(live_refs, list) or not live_refs:
                            errors.append(f"{label}.live_refs: at least one live repository/provider ref required")
                        else:
                            for live_index, live in enumerate(live_refs):
                                live_label = f"{label}.live_refs[{live_index}]"
                                if not isinstance(live, Mapping) or set(map(str, live)) - {"kind", "ref"}:
                                    errors.append(f"{live_label}: mapping with only kind/ref")
                                    continue
                                kind, ref = live.get("kind"), live.get("ref")
                                if kind not in {"REPOSITORY", "PROVIDER"}:
                                    errors.append(f"{live_label}.kind: REPOSITORY or PROVIDER")
                                if not isinstance(ref, str) or not ref.strip():
                                    errors.append(f"{live_label}.ref: non-empty string required")
                                elif kind == "REPOSITORY" and not re.match(r"^(?:path|function|commit|blob|tree):\S+", ref):
                                    errors.append(f"{live_label}.ref: repository live ref must start path:/function:/commit:/blob:/tree:")
                                elif kind == "PROVIDER" and not re.match(r"^(?:provider|pr|branch|commit):\S+", ref):
                                    errors.append(f"{live_label}.ref: provider live ref must start provider:/pr:/branch:/commit:")
                        summary = answer.get("evidence_summary")
                        if not isinstance(summary, str) or len(summary.strip()) < 20 or len(summary) > 1000:
                            errors.append(f"{label}.evidence_summary: 20..1000 characters required")
                        classes = answer.get("authority_classifications")
                        if classes is not None and (
                            not isinstance(classes, list)
                            or not classes
                            or len(classes) != len(set(classes))
                            or any(value not in HANDOVER_AUTHORITY_CLASSES for value in classes)
                        ):
                            errors.append(f"{label}.authority_classifications: unique values from {sorted(HANDOVER_AUTHORITY_CLASSES)}")
                    if len(answer_ids) != len(set(answer_ids)):
                        errors.append("handover.answer_evidence: duplicate question_id")

            root = handover.get("root_classification")
            if root is not None:
                if not isinstance(root, Mapping):
                    errors.append("handover.root_classification: must be a mapping")
                else:
                    allowed_root = {
                        "classification", "owning_layer", "upstream_boundary",
                        "downstream_boundary", "proof_required", "evidence_refs",
                    }
                    extra_root = set(map(str, root)) - allowed_root
                    if extra_root:
                        errors.append(f"handover.root_classification: unknown fields {sorted(extra_root)}")
                    for key in ("classification", "owning_layer", "upstream_boundary", "downstream_boundary", "proof_required"):
                        value = root.get(key)
                        if not isinstance(value, str) or not value.strip() or len(value) > 500:
                            errors.append(f"handover.root_classification.{key}: non-empty string up to 500 characters")
                    _check_refs(root.get("evidence_refs"), "handover.root_classification.evidence_refs", errors)
                    if not root.get("evidence_refs"):
                        errors.append("handover.root_classification.evidence_refs: at least one durable evidence ref required")

            if event == "OFFERED":
                if hresult is not None:
                    errors.append("handover.result: OFFERED cannot carry a successor result")
                if answer_evidence is not None or root is not None:
                    errors.append("handover: OFFERED cannot carry successor answer evidence/root classification")
                if challenge_digest is not None and not question_ids:
                    errors.append("handover.question_ids: required when OFFERED carries challenge_digest")
                if question_ids is not None and challenge_digest is None:
                    errors.append("handover.challenge_digest: required when OFFERED carries question_ids")
            if event == "ACCEPTED":
                if not predecessor:
                    errors.append("handover.predecessor_ref: required for ACCEPTED")
                if question_ids is not None:
                    errors.append("handover.question_ids: ACCEPTED must use the predecessor OFFERED question set")
                if (answer_evidence is not None or root is not None) and challenge_digest is None:
                    errors.append("handover.challenge_digest: required when ACCEPTED carries challenge evidence")
                if hresult == "RECONCILED" and challenge_digest is not None:
                    if not answer_evidence:
                        errors.append("handover.answer_evidence: required for challenged RECONCILED acceptance")
                    if root is None:
                        errors.append("handover.root_classification: required for challenged RECONCILED acceptance")

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


def _transformation_boundaries(value: Any, ref: str) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
        raise GraphError(f"{ref}.transformation_boundaries: must be a list of exact boundary tokens")
    if any(item != item.strip() for item in value):
        raise GraphError(f"{ref}.transformation_boundaries: tokens must not contain surrounding whitespace")
    values = list(value)
    duplicates = sorted({item for item in values if values.count(item) > 1})
    if duplicates:
        raise GraphError(f"{ref}.transformation_boundaries: duplicate values {duplicates}")
    unknown = sorted(set(values) - set(TRANSFORMATION_BOUNDARIES))
    if unknown:
        raise GraphError(
            f"{ref}.transformation_boundaries: unknown values {unknown} "
            f"(allowed: {list(TRANSFORMATION_BOUNDARIES)})"
        )
    return sorted(values)


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



def _acceptance_claims(value: Any) -> list[dict[str, Any]]:
    """Normalize parent acceptance claims without making an admission decision."""
    if value is None:
        return []
    if not isinstance(value, list):
        raise GraphError("programme.acceptance_claims: must be an array")
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, raw in enumerate(value):
        where = f"programme.acceptance_claims[{index}]"
        if not isinstance(raw, Mapping):
            raise GraphError(f"{where}: must be a mapping")
        extra = sorted(set(map(str, raw)) - {"id", "claim", "kind", "shared"})
        if extra:
            raise GraphError(f"{where}: unknown fields {extra}")
        claim_id = str(raw.get("id") or "")
        if not _UNIT_ID.fullmatch(claim_id) or claim_id in seen:
            raise GraphError(f"{where}.id: invalid or duplicate claim id {claim_id!r}")
        claim = raw.get("claim")
        if not isinstance(claim, str) or not claim.strip():
            raise GraphError(f"{where}.claim: must be a non-blank string")
        kind = raw.get("kind")
        if kind not in CLAIM_KINDS:
            raise GraphError(f"{where}.kind: one of {list(CLAIM_KINDS)}")
        shared = raw.get("shared", False)
        if not isinstance(shared, bool):
            raise GraphError(f"{where}.shared: must be boolean")
        seen.add(claim_id)
        rows.append({"id": claim_id, "claim": claim.strip(), "kind": kind, "shared": shared})
    return sorted(rows, key=lambda row: row["id"])


def _claim_relationships(
    value: Any, leaf_ref: str, claims_by_id: Mapping[str, Mapping[str, Any]]
) -> list[dict[str, str]]:
    """Normalize one leaf's claim relationships and reject undeclared/conflicting targets."""
    if value is None:
        return []
    if not isinstance(value, list):
        raise GraphError(f"{leaf_ref}.claim_relationships: must be an array")
    rows: list[dict[str, str]] = []
    seen: set[str] = set()
    for index, raw in enumerate(value):
        where = f"{leaf_ref}.claim_relationships[{index}]"
        if not isinstance(raw, Mapping):
            raise GraphError(f"{where}: must be a mapping")
        extra = sorted(set(map(str, raw)) - {"claim_id", "relation"})
        if extra:
            raise GraphError(f"{where}: unknown fields {extra}")
        claim_id = str(raw.get("claim_id") or "")
        if not _UNIT_ID.fullmatch(claim_id):
            raise GraphError(f"{where}.claim_id: invalid claim id {claim_id!r}")
        if claim_id not in claims_by_id:
            raise GraphError(f"{where}.claim_id: undeclared parent claim {claim_id!r}")
        if claim_id in seen:
            raise GraphError(f"{leaf_ref}.claim_relationships: duplicate relationship target {claim_id!r}")
        relation = raw.get("relation")
        if relation not in CLAIM_RELATIONS:
            raise GraphError(f"{where}.relation: one of {list(CLAIM_RELATIONS)}")
        seen.add(claim_id)
        rows.append({"claim_id": claim_id, "relation": str(relation)})
    return sorted(rows, key=lambda row: (row["claim_id"], row["relation"]))



def _topology_assessments(
    value: Any,
    nodes: Mapping[str, Mapping[str, Any]],
    order: Iterable[str],
) -> list[dict[str, Any]]:
    """Normalize plan-authority topology assessments using stable Responsibility ids."""
    if value is None:
        return []
    if not isinstance(value, list):
        raise GraphError("programme.topology_assessments: must be an array")

    id_to_ref = {
        str(nodes[ref].get("responsibility_id")): ref
        for ref in order
        if nodes[ref]["kind"] == "LEAF" and nodes[ref].get("responsibility_id")
    }
    rows: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    seen_subjects: set[tuple[str, tuple[str, ...]]] = set()

    enum_fields = {
        "proposal_kind": TOPOLOGY_PROPOSAL_KINDS,
        "semantic_cohesion": TOPOLOGY_SEMANTIC_COHESION,
        "dependency_closure": TOPOLOGY_DEPENDENCY_CLOSURE,
        "verification_closure": TOPOLOGY_VERIFICATION_CLOSURE,
        "uncertainty": TOPOLOGY_UNCERTAINTY,
        "change_impact": TOPOLOGY_CHANGE_IMPACT,
        "execution_horizon": TOPOLOGY_EXECUTION_HORIZON,
        "recovery_radius": TOPOLOGY_RECOVERY_RADIUS,
        "handoff_cost": TOPOLOGY_HANDOFF_COST,
        "cross_child_cohesion": TOPOLOGY_CROSS_CHILD_COHESION,
    }
    allowed = {
        "id",
        "proposal_kind",
        "responsibility_ids",
        "semantic_cohesion",
        "dependency_closure",
        "verification_closure",
        "uncertainty",
        "change_impact",
        "execution_horizon",
        "mutation_domains",
        "recovery_radius",
        "handoff_cost",
        "cross_child_cohesion",
        "stable_cut",
        "source_refs",
    }

    for index, raw in enumerate(value):
        where = f"programme.topology_assessments[{index}]"
        if not isinstance(raw, Mapping):
            raise GraphError(f"{where}: must be a mapping")
        extra = sorted(set(map(str, raw)) - allowed)
        if extra:
            raise GraphError(f"{where}: unknown fields {extra}")

        assessment_id = str(raw.get("id") or "")
        if not _UNIT_ID.fullmatch(assessment_id) or assessment_id in seen_ids:
            raise GraphError(f"{where}.id: invalid or duplicate assessment id {assessment_id!r}")
        seen_ids.add(assessment_id)

        normalized: dict[str, Any] = {"id": assessment_id}
        for field, choices in enum_fields.items():
            item = raw.get(field)
            if item not in choices:
                raise GraphError(f"{where}.{field}: one of {list(choices)}")
            normalized[field] = item

        ids = raw.get("responsibility_ids")
        if (
            not isinstance(ids, list)
            or not ids
            or any(not isinstance(item, str) or not item.strip() for item in ids)
        ):
            raise GraphError(f"{where}.responsibility_ids: non-empty array of stable Responsibility ids")
        subject_ids = sorted(item.strip() for item in ids)
        if len(subject_ids) != len(set(subject_ids)):
            raise GraphError(f"{where}.responsibility_ids: values must be unique")
        missing = [item for item in subject_ids if item not in id_to_ref]
        if missing:
            raise GraphError(f"{where}.responsibility_ids: undeclared stable ids {missing}")

        proposal_kind = normalized["proposal_kind"]
        if proposal_kind == "LEAF" and len(subject_ids) != 1:
            raise GraphError(f"{where}.responsibility_ids: LEAF requires exactly one subject")
        if proposal_kind == "ADJACENT_CHILDREN":
            if len(subject_ids) < 2:
                raise GraphError(f"{where}.responsibility_ids: ADJACENT_CHILDREN requires at least two subjects")
            parents = {nodes[id_to_ref[item]].get("parent_ref") for item in subject_ids}
            if len(parents) != 1:
                raise GraphError(f"{where}.responsibility_ids: ADJACENT_CHILDREN subjects must be siblings")

        signature = (proposal_kind, tuple(subject_ids))
        if signature in seen_subjects:
            raise GraphError(f"{where}: duplicate assessment subject set {list(subject_ids)}")
        seen_subjects.add(signature)
        normalized["responsibility_ids"] = subject_ids

        domains = raw.get("mutation_domains")
        if not isinstance(domains, list) or any(not isinstance(item, str) for item in domains):
            raise GraphError(f"{where}.mutation_domains: must be an array")
        if len(domains) != len(set(domains)):
            raise GraphError(f"{where}.mutation_domains: values must be unique")
        unknown_domains = sorted(set(domains) - set(TOPOLOGY_MUTATION_DOMAINS))
        if unknown_domains:
            raise GraphError(f"{where}.mutation_domains: unknown values {unknown_domains}")
        normalized["mutation_domains"] = sorted(domains)

        stable_cut = raw.get("stable_cut")
        if not isinstance(stable_cut, Mapping):
            raise GraphError(f"{where}.stable_cut: must be a mapping")
        stable_keys = set(map(str, stable_cut))
        required_stable = set(TOPOLOGY_STABLE_CUT_FIELDS)
        if stable_keys != required_stable:
            raise GraphError(
                f"{where}.stable_cut: expected exactly {sorted(required_stable)}, got {sorted(stable_keys)}"
            )
        for field in TOPOLOGY_STABLE_CUT_FIELDS:
            if not isinstance(stable_cut.get(field), bool):
                raise GraphError(f"{where}.stable_cut.{field}: must be boolean")
        normalized["stable_cut"] = {
            field: bool(stable_cut[field]) for field in TOPOLOGY_STABLE_CUT_FIELDS
        }

        refs = raw.get("source_refs")
        if (
            not isinstance(refs, list)
            or not refs
            or any(not isinstance(item, str) or not item.strip() for item in refs)
        ):
            raise GraphError(f"{where}.source_refs: non-empty array of refs required")
        source_refs = sorted(item.strip() for item in refs)
        if len(source_refs) != len(set(source_refs)):
            raise GraphError(f"{where}.source_refs: values must be unique")
        normalized["source_refs"] = source_refs
        rows.append(normalized)

    return sorted(rows, key=lambda row: row["id"])


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


def resolve_health_policy(overrides: Any) -> dict[str, Any]:
    """Merge `programme.health_policy` over the defaults and validate it. Raises GraphError."""
    policy = copy.deepcopy(DEFAULT_HEALTH_POLICY)
    if overrides is None:
        return policy
    if not isinstance(overrides, Mapping):
        raise GraphError("programme.health_policy: must be a mapping")
    unknown = sorted(set(map(str, overrides)) - set(DEFAULT_HEALTH_POLICY))
    if unknown:
        raise GraphError(f"programme.health_policy: unknown keys {unknown}")
    for key, value in overrides.items():
        if key == "mode":
            if value not in HEALTH_MODES:
                raise GraphError(f"programme.health_policy.mode: one of {list(HEALTH_MODES)}")
            policy["mode"] = value
            continue
        if not isinstance(value, Mapping):
            raise GraphError(f"programme.health_policy.{key}: must be a mapping")
        extra = sorted(set(map(str, value)) - set(policy[key]))
        if extra:
            raise GraphError(f"programme.health_policy.{key}: unknown keys {extra}")
        policy[key].update(value)
    for section in ("checkpoint", "drift", "interruptions"):
        for name, number in policy[section].items():
            _positive_int(number, f"programme.health_policy.{section}.{name}")
    c, d, i = policy["checkpoint"], policy["drift"], policy["interruptions"]
    if c["watch_added_loc"] > c["at_risk_added_loc"] or c["watch_changed_loc"] > c["at_risk_changed_loc"]:
        raise GraphError("programme.health_policy.checkpoint: a watch level must not exceed its at-risk level")
    if d["watch_behind"] > d["at_risk_behind"] or i["watch"] > i["at_risk"]:
        raise GraphError("programme.health_policy: a watch level must not exceed its at-risk level")
    return policy


def validate_graph(graph: Any) -> dict[str, Any]:
    """Validate the plan and return an indexed view. Raises GraphError."""
    if not isinstance(graph, Mapping):
        raise GraphError("graph must be a mapping")
    if graph.get("schema") not in (None, GRAPH_SCHEMA):
        raise GraphError(f"schema: must be {GRAPH_SCHEMA}")
    programme = graph.get("programme") or {}
    declared_graph_generation = "graph_generation" in programme
    graph_generation = programme.get("graph_generation", 1)
    if isinstance(graph_generation, bool) or not isinstance(graph_generation, int) or graph_generation < 1:
        raise GraphError("programme.graph_generation: must be a positive integer")
    root_ref = programme.get("root")
    if not root_ref:
        raise GraphError("programme.root: required")
    try:
        parse_ref(root_ref)
    except DelpError as exc:
        raise GraphError(f"programme.root: {exc}") from exc
    policy = resolve_policy(programme.get("decomposition_policy"))
    health_policy = resolve_health_policy(programme.get("health_policy"))
    acceptance_claims = _acceptance_claims(programme.get("acceptance_claims"))
    claims_by_id = {row["id"]: row for row in acceptance_claims}
    total_weight = _positive_int(programme.get("total_weight", DEFAULT_TOTAL_WEIGHT), "programme.total_weight")
    base_ref = programme.get("base_ref")
    if base_ref is not None and (not isinstance(base_ref, str) or not base_ref.strip()):
        raise GraphError("programme.base_ref: must be a non-empty branch name")

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
                successor_policy = unit.get("successor_policy")
                clean_successor_policy = None
                if successor_policy is not None:
                    if not isinstance(successor_policy, Mapping):
                        raise GraphError(f"{ref}.units.{uid}.successor_policy: must be a mapping")
                    extra_policy = sorted(
                        set(map(str, successor_policy)) - {"mode", "decision_at_risk", "protected_invariants"}
                    )
                    if extra_policy:
                        raise GraphError(
                            f"{ref}.units.{uid}.successor_policy: unknown keys {extra_policy}"
                        )
                    policy_mode = successor_policy.get("mode")
                    if policy_mode not in HANDOVER_MODES:
                        raise GraphError(
                            f"{ref}.units.{uid}.successor_policy.mode: one of {sorted(HANDOVER_MODES)}"
                        )
                    decision = successor_policy.get("decision_at_risk")
                    if decision is not None and (
                        not isinstance(decision, str) or not decision.strip() or len(decision) > 200 or "\n" in decision
                    ):
                        raise GraphError(
                            f"{ref}.units.{uid}.successor_policy.decision_at_risk: single non-empty line, at most 200 characters"
                        )
                    if policy_mode == "INDEPENDENT_RECONSTRUCTION" and not decision:
                        raise GraphError(
                            f"{ref}.units.{uid}.successor_policy.decision_at_risk: required for INDEPENDENT_RECONSTRUCTION"
                        )
                    invariants = successor_policy.get("protected_invariants") or []
                    if not isinstance(invariants, list) or not all(
                        isinstance(item, str) and item.strip() and len(item) <= 200 and "\n" not in item
                        for item in invariants
                    ):
                        raise GraphError(
                            f"{ref}.units.{uid}.successor_policy.protected_invariants: list of non-empty single lines <= 200 chars"
                        )
                    if len(set(invariants)) != len(invariants):
                        raise GraphError(
                            f"{ref}.units.{uid}.successor_policy.protected_invariants: duplicates are not allowed"
                        )
                    clean_successor_policy = {
                        "mode": policy_mode,
                        "decision_at_risk": decision.strip() if isinstance(decision, str) else None,
                        "protected_invariants": list(invariants),
                    }
                clean_units.append(
                    {
                        "id": uid,
                        "weight": _positive_int(unit.get("weight"), f"{ref}.units.{uid}.weight"),
                        "verify": texts["verify"],
                        "outcome": texts["outcome"],
                        "successor_policy": clean_successor_policy,
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
            integration_basis = raw.get("integration_basis")
            if integration_basis is not None and (
                not isinstance(integration_basis, str) or not integration_basis.strip()
            ):
                raise GraphError(f"{ref}.integration_basis: must be a non-blank string")
            claim_relationships = _claim_relationships(raw.get("claim_relationships"), ref, claims_by_id)
            node.update(
                {
                    "units": clean_units,
                    "delivery_gates": gates,
                    "coder_weight": coder_weight if gates else 1,
                    "responsibility_id": raw.get("responsibility_id"),
                    "spec_generation": raw.get("spec_generation"),
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
                    "claim_relationships": claim_relationships,
                    "transformation_boundaries": _transformation_boundaries(
                        raw.get("transformation_boundaries"), ref
                    ),
                    "integration_basis": (
                        integration_basis.strip() if isinstance(integration_basis, str) else None
                    ),
                }
            )
            if node["spec_generation"] is not None:
                node["spec_generation"] = _positive_int(node["spec_generation"], f"{ref}.spec_generation")
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

    # Stable identity is distinct from the provider locator. Legacy graphs may omit it;
    # once graph_generation is explicitly declared, every leaf must carry a unique Responsibility id.
    seen_responsibility_ids: dict[str, str] = {}
    for ref, node in nodes.items():
        if node["kind"] != "LEAF":
            continue
        rid = node.get("responsibility_id")
        if declared_graph_generation and not rid:
            raise GraphError(f"{ref}.responsibility_id: required when programme.graph_generation is declared")
        if declared_graph_generation and node.get("spec_generation") is None:
            raise GraphError(f"{ref}.spec_generation: required when programme.graph_generation is declared")
        if rid is not None:
            rid = str(rid).strip()
            if not rid:
                raise GraphError(f"{ref}.responsibility_id: must be a non-empty string")
            other = seen_responsibility_ids.get(rid)
            if other is not None:
                raise GraphError(f"{ref}.responsibility_id: duplicate stable id {rid!r} already used by {other}")
            seen_responsibility_ids[rid] = ref
            node["responsibility_id"] = rid

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

    topology_assessments = _topology_assessments(
        programme.get("topology_assessments"),
        nodes,
        order,
    )

    # Stable-identity graphs derive each leaf contract digest mechanically. Locator/topology/provider
    # metadata and weights are intentionally excluded so transfers/reparenting/reweighting do not stale evidence.
    if declared_graph_generation:
        for ref in leaf_by_number.values():
            node = nodes[ref]
            derived_digest = canonical_digest(responsibility_contract_basis(node, nodes, claims_by_id))
            asserted_digest = node.get("contract_digest")
            if asserted_digest is not None and asserted_digest != derived_digest:
                raise GraphError(
                    f"{ref}.contract_digest: asserted {asserted_digest} does not match derived {derived_digest}; "
                    "omit the field and let the engine derive it"
                )
            node["contract_digest"] = derived_digest

    normalized_programme = dict(programme)
    normalized_programme["graph_generation"] = graph_generation
    if "topology_assessments" in programme:
        normalized_programme["topology_assessments"] = topology_assessments
    return {
        "programme": normalized_programme,
        "stable_identity_mode": declared_graph_generation,
        "policy": policy,
        "health_policy": health_policy,
        "acceptance_claims": acceptance_claims,
        "claims_by_id": claims_by_id,
        "topology_assessments": topology_assessments,
        "topology_assessments_by_id": {row["id"]: row for row in topology_assessments},
        "total_weight": total_weight,
        "plan_updates": _plan_updates(graph.get("plan_updates")),
        "nodes": nodes,
        "order": order,
        "root": roots[0],
        "by_number": by_number,
        "digest": canonical_digest(graph_digest_basis(graph)),
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



def claim_topology_report(graph: Any) -> dict[str, Any]:
    """Pure claim/Responsibility relationship facts; never an admission or progress verdict."""
    indexed = validate_graph(graph)
    claims = indexed["acceptance_claims"]
    nodes = indexed["nodes"]

    by_claim: dict[str, dict[str, Any]] = {}
    for claim in claims:
        by_claim[claim["id"]] = {
            "id": claim["id"],
            "claim": claim["claim"],
            "kind": claim["kind"],
            "shared": claim["shared"],
            "owners": [],
            "enablers": [],
            "gates": [],
        }

    responsibility_rows: list[dict[str, Any]] = []
    for ref in indexed["order"]:
        node = nodes[ref]
        if node["kind"] != "LEAF":
            continue
        relations = list(node.get("claim_relationships") or [])
        responsibility_rows.append(
            {
                "ref": ref,
                "responsibility_id": node.get("responsibility_id"),
                "relations": relations,
                "orphan": not relations,
            }
        )
        for rel in relations:
            bucket = {
                "OWN": "owners",
                "ENABLES": "enablers",
                "GATE": "gates",
            }[rel["relation"]]
            by_claim[rel["claim_id"]][bucket].append(ref)

    claim_rows: list[dict[str, Any]] = []
    for claim in claims:
        row = by_claim[claim["id"]]
        row["owners"].sort(key=ref_number)
        row["enablers"].sort(key=ref_number)
        row["gates"].sort(key=ref_number)
        if claim["kind"] == "SEMANTIC":
            coverage = "OWNED" if row["owners"] else "UNCOVERED"
        else:
            coverage = "COVERED" if row["owners"] or row["gates"] else "UNCOVERED"
        row["coverage"] = coverage
        row["duplicate_owners"] = (
            list(row["owners"]) if len(row["owners"]) > 1 and not claim["shared"] else []
        )
        claim_rows.append(row)

    claim_rows.sort(key=lambda row: row["id"])
    responsibility_rows.sort(key=lambda row: ref_number(row["ref"]))
    return {
        "authority": "DERIVED_CLAIM_TOPOLOGY_ONLY",
        "claims": claim_rows,
        "responsibilities": responsibility_rows,
        "summary": {
            "claims": len(claim_rows),
            "uncovered_claims": sum(1 for row in claim_rows if row["coverage"] == "UNCOVERED"),
            "orphan_responsibilities": sum(1 for row in responsibility_rows if row["orphan"]),
            "duplicate_nonshared_ownership": sum(1 for row in claim_rows if row["duplicate_owners"]),
        },
    }


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


def decomposition_report(
    graph: Any,
    mode: str | None = None,
    closed: Iterable[str] = (),
    topology_observations: Mapping[str, Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    """Evaluate one integrated mechanical + semantic topology release report.

    R2 remains the semantic decision authority. This function only merges its
    already-derived blockers into the existing decomposition report shape.
    """
    if mode is not None and mode not in POLICY_MODES:
        raise GraphError(f"mode: one of {list(POLICY_MODES)}")
    if topology_observations is None:
        topology_observations = {}
    if not isinstance(topology_observations, Mapping):
        raise DelpError("topology_observations: must be a mapping keyed by declared leaf reference")

    indexed = validate_graph(graph)
    closed_numbers = {ref_number(c) for c in closed}
    closed_refs = {
        r
        for r in indexed["nodes"]
        if indexed["nodes"][r]["number"] in closed_numbers
    }
    report = _decomposition(indexed, closed_refs, mode)

    claim_first_active = bool(
        indexed.get("acceptance_claims") or indexed.get("topology_assessments")
    )
    if not claim_first_active:
        return report

    try:
        topology_release = _topology_assembler_module().topology_release_findings(
            graph,
            observations=topology_observations,
            closed=closed_refs,
        )
    except Exception as exc:
        raise DelpError(f"topology release derivation failed: {exc}") from exc

    for ref, row in report["leaves"].items():
        topology_row = topology_release["leaves"].get(ref) or {
            "blockers": [],
            "admissions": [],
        }
        topology_blockers = [
            {"code": blocker["code"], "detail": blocker["detail"]}
            for blocker in topology_row["blockers"]
        ]
        row["blockers"] = sorted(
            [*row["blockers"], *topology_blockers],
            key=lambda item: (item["code"], item["detail"]),
        )
        row["releasable"] = not row["blockers"]
        if topology_row["admissions"] or topology_row["blockers"]:
            row["topology"] = {
                "authority": topology_release["authority"],
                "admissions": copy.deepcopy(topology_row["admissions"]),
                "blockers": copy.deepcopy(topology_row["blockers"]),
            }

    report["summary"]["releasable"] = sum(
        1 for row in report["leaves"].values() if row["releasable"]
    )
    report["summary"]["not_releasable"] = sum(
        1 for row in report["leaves"].values() if not row["releasable"]
    )
    return report


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
# agent health: observed or derived, never declared. Advisory; never moves a number, a state or a title.
#
# Seven components, each OK / WATCH / AT_RISK / UNOBSERVED. UNOBSERVED means nothing was observed and is never read
# as healthy; the verdict is the worst component, never an average. The words are about delivery continuity (how far
# a successor would have to reconstruct), not about the quality of anyone's work: telemetry locates evidence and
# constrains delivery, it does not measure value.
# --------------------------------------------------------------------------


def _count(value: Any) -> int | None:
    return value if isinstance(value, int) and not isinstance(value, bool) and value >= 0 else None


def _health_components(
    leaf: Mapping[str, Any],
    node: Mapping[str, Any],
    observation: Mapping[str, Any],
    policy: Mapping[str, Any],
    limits: Mapping[str, int],
) -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}

    def put(name: str, status: str, detail: str) -> None:
        out[name] = {"status": status, "detail": detail}

    materialization = leaf.get("materialization")
    if materialization:
        put("materialization", "AT_RISK", f"no accepted facts; the provider shows {materialization['provider_signal']}")
        put("evidence", "UNOBSERVED", "no facts to qualify")
    else:
        put("materialization", "OK", "the ledger holds accepted facts")
        verdict, gaps = leaf["evidence"]["health"], leaf["evidence"]["gaps"]
        put(
            "evidence",
            {"CURRENT": "OK", "GAP": "WATCH", "STALE_CANDIDATE": "AT_RISK", "UNVERIFIABLE": "UNOBSERVED"}[verdict],
            verdict + (": " + ", ".join(f"{g['unit']}:{g['reason']}" for g in gaps) if gaps else ""),
        )

    additions = _count(observation.get("additions"))
    deletions = _count(observation.get("deletions")) or 0
    since = observation.get("since_checkpoint")
    distance: tuple[int, int] | None
    if isinstance(since, Mapping) and _count(since.get("additions")) is not None:
        distance = (since["additions"], since["additions"] + (_count(since.get("deletions")) or 0))
    elif materialization and additions is not None:
        distance = (additions, additions + deletions)  # nothing was ever checkpointed: the whole branch is the distance
    else:
        distance = None
    c = policy["checkpoint"]
    if distance is None:
        put("checkpoint_distance", "UNOBSERVED", "the lines authored since the last checkpoint were not observed")
    else:
        added, changed = distance
        if added >= c["at_risk_added_loc"] or changed >= c["at_risk_changed_loc"]:
            status = "AT_RISK"
        elif added >= c["watch_added_loc"] or changed >= c["watch_changed_loc"]:
            status = "WATCH"
        else:
            status = "OK"
        put(
            "checkpoint_distance",
            status,
            f"{added} lines authored ({changed} changed) since the last checkpoint; trigger {c['watch_added_loc']}, hard ceiling {c['at_risk_added_loc']}",
        )

    budget = node.get("size_budget") or {}
    declared = "target_loc" in budget and "hard_loc" in budget
    target, hard = (budget["target_loc"], budget["hard_loc"]) if declared else (limits["target_loc"], limits["hard_loc"])
    if additions is None:
        put("size", "UNOBSERVED", "the changed lines of the candidate were not observed")
    else:
        total = additions + deletions
        status = "AT_RISK" if total > hard else "WATCH" if total > target else "OK"
        put("size", status, f"{total} changed lines against target {target} / hard {hard} ({'declared budget' if declared else 'policy default'})")

    behind = _count(observation.get("behind_by"))
    d = policy["drift"]
    if behind is None:
        put("base_drift", "UNOBSERVED", "the divergence from the base was not observed")
    else:
        status = "AT_RISK" if behind >= d["at_risk_behind"] else "WATCH" if behind >= d["watch_behind"] else "OK"
        put("base_drift", status, f"{behind} commit(s) behind the base")

    interruptions = observation.get("interruptions")
    i = policy["interruptions"]
    recorded = interruptions.get("losses") if isinstance(interruptions, Mapping) else None
    watched_from = interruptions.get("coverage_from") if isinstance(interruptions, Mapping) else None
    if not isinstance(recorded, list) or (not recorded and not watched_from):
        # A recorded loss is a loss whether or not anyone declared when watching began; zero can only be claimed by an observer.
        put("interruptions", "UNOBSERVED", "no observer was watching for stream losses, so zero cannot be claimed")
    else:
        losses = len(recorded)
        status = "AT_RISK" if losses >= i["at_risk"] else "WATCH" if losses >= i["watch"] else "OK"
        put(
            "interruptions",
            status,
            f"{losses} stream loss(es) in this executor lifecycle" + ("; the written rule plans a handover at the third" if losses >= i["at_risk"] else ""),
        )

    liveness = leaf.get("liveness")
    put(
        "liveness",
        {"ACTIVE": "OK", "QUIET": "WATCH", "STALE": "AT_RISK"}.get(liveness or "", "UNOBSERVED"),
        f"observed {liveness}" if liveness else "no observer reported liveness",
    )
    return out


def _health_block(components: Mapping[str, Mapping[str, str]]) -> dict[str, Any]:
    worst = max((c["status"] for c in components.values()), key=HEALTH_RANK.__getitem__)
    verdict = HEALTH_VERDICT[worst]
    ordered = sorted(components.items(), key=lambda kv: (-HEALTH_RANK[kv[1]["status"]], kv[0]))
    return {
        "mode": "ADVISORY",
        "verdict": verdict,
        "light": HEALTH_LIGHT[verdict],
        "components": {name: dict(c) for name, c in ordered},
        "reasons": [f"{name} ({c['detail']})" for name, c in ordered if c["status"] != "OK"],
        "advisory": True,
    }


def _health_rollup(rows: list[tuple[str, Mapping[str, Any]]]) -> dict[str, Any] | None:
    if not rows:
        return None
    rank = {"HEALTHY": 0, "UNOBSERVED": 1, "WATCH": 2, "AT_RISK": 3}
    verdict = max((h["verdict"] for _, h in rows), key=rank.__getitem__)
    counts = {v: sum(1 for _, h in rows if h["verdict"] == v) for v in rank}
    return {
        "mode": "ADVISORY",
        "verdict": verdict,
        "light": HEALTH_LIGHT[verdict],
        "leaves": len(rows),
        "counts": {k: v for k, v in counts.items() if v},
        "at_risk": [ref for ref, h in rows if h["verdict"] == "AT_RISK"],
        "advisory": True,
    }


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

    contracts_changed = 0
    generation_bumps = 0
    old_by_id = {
        str(node["responsibility_id"]): node
        for node in old["nodes"].values()
        if node["kind"] == "LEAF" and node.get("responsibility_id") and node.get("spec_generation") is not None
    }
    new_by_id = {
        str(node["responsibility_id"]): node
        for node in new["nodes"].values()
        if node["kind"] == "LEAF" and node.get("responsibility_id") and node.get("spec_generation") is not None
    }
    for rid in sorted(set(old_by_id) & set(new_by_id)):
        before, after = old_by_id[rid], new_by_id[rid]
        old_gen, new_gen = before["spec_generation"], after["spec_generation"]
        changed = before.get("contract_digest") != after.get("contract_digest")
        if new_gen < old_gen:
            add("SPEC_GENERATION_REGRESSED", f"{rid} spec_generation {old_gen} -> {new_gen}")
        if changed:
            contracts_changed += 1
            if new_gen <= old_gen:
                add(
                    "SPEC_GENERATION_NOT_BUMPED",
                    f"{rid} semantic contract changed but spec_generation stayed {old_gen} -> {new_gen}",
                )
        elif new_gen != old_gen:
            add(
                "SPEC_GENERATION_BUMP_WITHOUT_CONTRACT_CHANGE",
                f"{rid} spec_generation {old_gen} -> {new_gen} but the derived contract digest is unchanged",
                "ADVISORY",
            )
        if new_gen > old_gen:
            generation_bumps += 1

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


def _observed_material(observation: Mapping[str, Any]) -> dict[str, Any]:
    """The provider-observed facts about a leaf's material that are safe to publish, validated and typed."""
    out: dict[str, Any] = {}
    base = observation.get("base_sha")
    if isinstance(base, str) and _SHA.fullmatch(base):
        out["base_sha"] = base
    pr_state = str(observation.get("pr_state") or "").upper()
    if pr_state in _PR_ACTIVITY_STATES:
        out["pr_state"] = pr_state
    for key in ("ahead_by", "behind_by"):
        value = observation.get(key)
        if isinstance(value, int) and not isinstance(value, bool) and value >= 0:
            out[key] = value
    return out


def _provider_signal(observation: Mapping[str, Any]) -> str | None:
    """What the provider shows about a leaf's work, independent of anything an agent published."""
    pr_state = str(observation.get("pr_state") or "").upper()
    if pr_state in _PR_ACTIVITY_STATES:
        return f"PR_{pr_state}"
    ahead = observation.get("ahead_by")
    if isinstance(ahead, int) and not isinstance(ahead, bool) and ahead > 0:
        return f"BRANCH_AHEAD_{ahead}"
    return None


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
    handover_offer: Mapping[str, Any] | None = None
    handover_accept: Mapping[str, Any] | None = None
    entry_prepared: Mapping[str, Any] | None = None
    entry_end: Mapping[str, Any] | None = None
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
        if rec.get("handover") is not None:
            h = dict(rec["handover"])
            h["_source"] = rec.get("_source")
            h["_candidate_sha"] = (rec.get("material") or {}).get("candidate_sha")
            if h.get("event") == "OFFERED":
                handover_offer = h
                handover_accept = None
            else:
                handover_accept = h
        if rec.get("entry") is not None:
            e = dict(rec["entry"])
            e["_source"] = rec.get("_source")
            e["_candidate_sha"] = (rec.get("material") or {}).get("candidate_sha")
            if e.get("event") == "PREPARED":
                entry_prepared = e
            else:
                entry_end = e
        record_candidate = (rec.get("material") or {}).get("candidate_sha")
        record_pr = (rec.get("material") or {}).get("pr")
        record_contract_digest = (rec.get("responsibility") or {}).get("contract_digest")
        for unit in rec.get("units") or []:
            if unit["id"] not in declared:
                warnings.append(f"UNKNOWN_UNIT:{unit['id']}")
                continue
            claims[unit["id"]] = {
                "state": unit["state"],
                "result": unit.get("result") or "NOT_RUN",
                "evidence_refs": [str(r) for r in unit.get("evidence_refs") or []],
                "candidate_sha": unit.get("candidate_sha") or record_candidate,
                "contract_digest": unit.get("contract_digest") or record_contract_digest,
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
    active_plan_unit = next((item for item in node["units"] if item["id"] == active_unit), None)
    successor_policy = (active_plan_unit or {}).get("successor_policy")

    handover_projection = None
    if handover_offer is not None:
        accepted = handover_accept is not None
        offered_challenge_digest = handover_offer.get("challenge_digest")
        expected_question_ids = list(handover_offer.get("question_ids") or [])
        accepted_answers = list((handover_accept or {}).get("answer_evidence") or [])
        answered_question_ids = [row.get("question_id") for row in accepted_answers if isinstance(row, Mapping)]
        accepted_challenge_digest = (handover_accept or {}).get("challenge_digest")
        challenge_identity_matched = (
            offered_challenge_digest is None
            or accepted_challenge_digest == offered_challenge_digest
        )
        coverage_matched = (
            offered_challenge_digest is None
            or answered_question_ids == expected_question_ids
        )
        answers_grounded = bool(
            offered_challenge_digest is None
            or (
                accepted_answers
                and all(row.get("evidence_refs") and row.get("live_refs") for row in accepted_answers if isinstance(row, Mapping))
            )
        )
        by_id = {
            row.get("question_id"): row
            for row in accepted_answers
            if isinstance(row, Mapping) and row.get("question_id")
        }
        q1_grounded = (
            "Q1" not in expected_question_ids
            or any(live.get("kind") == "REPOSITORY" for live in (by_id.get("Q1") or {}).get("live_refs") or [] if isinstance(live, Mapping))
        )
        q2_authority = (
            "Q2" not in expected_question_ids
            or bool((by_id.get("Q2") or {}).get("authority_classifications"))
        )
        root_classification = (handover_accept or {}).get("root_classification")
        q3_rooted = (
            "Q3" not in expected_question_ids
            or bool(root_classification and root_classification.get("evidence_refs"))
        )
        challenge_evidence_complete = bool(
            offered_challenge_digest is None
            or (
                challenge_identity_matched
                and coverage_matched
                and answers_grounded
                and q1_grounded
                and q2_authority
                and q3_rooted
            )
        )
        matched = bool(
            accepted
            and handover_accept.get("mode") == handover_offer.get("mode")
            and handover_accept.get("decision_at_risk") == handover_offer.get("decision_at_risk")
            and handover_accept.get("frontier_digest") == handover_offer.get("frontier_digest")
            and handover_accept.get("predecessor_ref") == handover_offer.get("_source")
            and handover_accept.get("_candidate_sha") == handover_offer.get("_candidate_sha")
            and challenge_identity_matched
        )
        if accepted and not matched:
            warnings.append("HANDOVER_ACCEPTANCE_MISMATCH")
        if accepted and offered_challenge_digest is not None and not challenge_evidence_complete:
            warnings.append("HANDOVER_CHALLENGE_EVIDENCE_INCOMPLETE")
        if successor_policy and handover_offer.get("mode") != successor_policy.get("mode"):
            warnings.append("HANDOVER_MODE_DIFFERS_FROM_ACTIVE_UNIT_POLICY")
        if (
            successor_policy
            and successor_policy.get("decision_at_risk")
            and handover_offer.get("decision_at_risk") != successor_policy.get("decision_at_risk")
        ):
            warnings.append("HANDOVER_DECISION_DIFFERS_FROM_ACTIVE_UNIT_POLICY")
        if not accepted:
            handover_status = "HANDOFF"
        elif matched and handover_accept.get("result") == "RECONCILED" and challenge_evidence_complete:
            handover_status = "RECONCILED"
        else:
            handover_status = "RECONSTRUCTING"
        handover_projection = {
            "status": handover_status,
            "mode": handover_offer.get("mode"),
            "decision_at_risk": handover_offer.get("decision_at_risk"),
            "frontier_digest": handover_offer.get("frontier_digest"),
            "challenge_digest": offered_challenge_digest,
            "expected_question_ids": expected_question_ids,
            "answered_question_ids": answered_question_ids,
            "challenge_evidence_complete": challenge_evidence_complete,
            "root_classification": (
                root_classification.get("classification")
                if isinstance(root_classification, Mapping)
                else None
            ),
            "predecessor_ref": handover_accept.get("predecessor_ref") if accepted else None,
            "result": handover_accept.get("result") if accepted else None,
            "matched": matched,
        }

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

    # No accepted facts but the provider shows work: the numbers are a lower bound, not the truth.
    provider_signal = _provider_signal(observation)
    unmaterialized = not records and provider_signal is not None
    if unmaterialized:
        active_unit = None  # no fact says which unit is next
        warnings.append(f"UNMATERIALIZED:{provider_signal}")

    if superseded_by:
        lifecycle = "SUPERSEDED"
    elif claims_complete and not incomplete and health == "CURRENT" and D == 1 and DE == 1:
        lifecycle = "COMPLETE"
    elif unmaterialized:
        lifecycle = "UNMATERIALIZED"
    elif not records and liveness is None:
        lifecycle = "NOT_STARTED"
    elif activity == "PAUSED" and handover_projection is None:
        lifecycle = "PAUSED"
    elif activity == "RECOVERING":
        lifecycle = "RECOVERING"
    else:
        lifecycle = "ACTIVE"

    if lifecycle in {"COMPLETE", "SUPERSEDED", "NOT_STARTED", "PAUSED"}:
        state = lifecycle
    elif liveness == "STALE":
        state = "STALE"
    elif lifecycle == "UNMATERIALIZED":
        state = "UNMATERIALIZED"
    elif health == "STALE_CANDIDATE":
        state = "EVIDENCE_STALE"
    elif health in {"GAP", "UNVERIFIABLE"}:
        state = "EVIDENCE_GAP"
    elif handover_projection and handover_projection["status"] == "HANDOFF":
        state = "HANDOFF"
    elif handover_projection and handover_projection["status"] == "RECONSTRUCTING":
        state = "RECONSTRUCTING"
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
    result = {
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
        "successor_policy": successor_policy,
        "warnings": warnings,
    }
    if handover_projection is not None:
        result["handover"] = handover_projection
    if entry_prepared is not None or entry_end is not None:
        result["entry"] = {
            "prepared": dict(entry_prepared) if entry_prepared is not None else None,
            "execution_end": dict(entry_end) if entry_end is not None else None,
        }
    if unmaterialized:
        result["materialization"] = {"status": "UNMATERIALIZED", "provider_signal": provider_signal}
    return result


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


def bind_facts_to_graph(graph: Any, facts: Mapping[str, Any]) -> dict[str, Any]:
    """Stamp current Responsibility contract identity into one facts record before publication.

    This is a pure publication helper. It never repairs a conflicting pre-existing binding.
    """
    errors = validate_facts(facts)
    if errors:
        raise DelpError("cannot bind invalid facts: " + "; ".join(errors))
    indexed = validate_graph(graph)
    claimed_issue = facts["responsibility"]["issue"]
    leaf_ref = next(
        (
            ref
            for ref, node in indexed["nodes"].items()
            if node["kind"] == "LEAF" and same_ref(ref, claimed_issue)
        ),
        None,
    )
    if leaf_ref is None:
        raise DelpError(f"responsibility.issue: {facts['responsibility']['issue']} is not a declared LEAF")
    node = indexed["nodes"][leaf_ref]
    bound = copy.deepcopy(dict(facts))
    responsibility = dict(bound["responsibility"])

    expected: dict[str, Any] = {}
    if node.get("responsibility_id") is not None:
        expected["id"] = node["responsibility_id"]
    if indexed["stable_identity_mode"]:
        expected["spec_generation"] = node["spec_generation"]
        expected["contract_digest"] = node["contract_digest"]

    for field, value in expected.items():
        current = responsibility.get(field)
        if current is not None and current != value:
            raise DelpError(
                f"responsibility.{field}: existing {current!r} conflicts with current planned {value!r}"
            )
        responsibility[field] = value
    bound["responsibility"] = responsibility
    return bound


def execution_binding_from_state_lease(
    state: Mapping[str, Any], lease: Mapping[str, Any]
) -> dict[str, Any]:
    """Derive the current facts execution provenance from existing STATE + active LEASE truth.

    This helper creates no new custody authority. It only verifies that the two existing
    custody surfaces agree and returns their canonical identity tuple.
    """
    if not isinstance(state, Mapping) or not isinstance(lease, Mapping):
        raise DelpError("execution binding requires STATE and LEASE mappings")

    execution = state.get("execution")
    if not isinstance(execution, Mapping) or execution.get("lifecycle") != "ACTIVE":
        raise DelpError("execution binding requires ACTIVE STATE.execution")

    ep = execution.get("ep")
    lease_id = execution.get("lease")
    custody_epoch = execution.get("custody_epoch")
    if not _EP_ID.fullmatch(str(ep or "")):
        raise DelpError("STATE.execution.ep: active canonical EP identifier required")
    if not _LEASE_ID.fullmatch(str(lease_id or "")):
        raise DelpError("STATE.execution.lease: active canonical LEASE identifier required")
    if isinstance(custody_epoch, bool) or not isinstance(custody_epoch, int) or custody_epoch < 1:
        raise DelpError("STATE.execution.custody_epoch: positive integer required for active binding")

    if lease.get("state") != "ACTIVE":
        raise DelpError("execution binding requires ACTIVE LEASE")
    if lease.get("id") != lease_id:
        raise DelpError("LEASE.id does not match STATE.execution.lease")

    basis = lease.get("basis")
    if not isinstance(basis, Mapping) or basis.get("ep_id") != ep:
        raise DelpError("LEASE.basis.ep_id does not match STATE.execution.ep")

    custody = lease.get("custody")
    lease_epoch = custody.get("epoch") if isinstance(custody, Mapping) else None
    if isinstance(lease_epoch, bool) or not isinstance(lease_epoch, int) or lease_epoch < 1:
        raise DelpError("LEASE.custody.epoch: positive integer required")
    if lease_epoch != custody_epoch:
        raise DelpError("LEASE.custody.epoch does not match STATE.execution.custody_epoch")

    executor = lease.get("executor")
    executor_id = executor.get("id") if isinstance(executor, Mapping) else None
    if not isinstance(executor_id, str) or not executor_id.strip():
        raise DelpError("LEASE.executor.id: non-empty string required")

    return {
        "ep": str(ep),
        "lease": str(lease_id),
        "executor": executor_id,
        "custody_epoch": custody_epoch,
    }


def bind_facts_to_execution(
    facts: Mapping[str, Any], state: Mapping[str, Any], lease: Mapping[str, Any]
) -> dict[str, Any]:
    """Stamp current execution provenance into facts without repairing conflicts."""
    errors = validate_facts(facts)
    if errors:
        raise DelpError("cannot bind invalid facts: " + "; ".join(errors))

    expected = execution_binding_from_state_lease(state, lease)
    bound = copy.deepcopy(dict(facts))
    current = bound.get("execution")
    if current is not None and dict(current) != expected:
        raise DelpError(
            f"execution: existing {dict(current)!r} conflicts with current custody binding {expected!r}"
        )
    bound["execution"] = expected
    return bound


def execution_provenance(records: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    """Summarize accepted fact execution bindings without deciding custody currentness."""
    bound = 0
    unbound = 0
    buckets: dict[tuple[str, str, str, int], set[str]] = {}

    for record in records:
        execution = record.get("execution") if isinstance(record, Mapping) else None
        if not isinstance(execution, Mapping):
            unbound += 1
            continue

        bound += 1
        key = (
            str(execution["ep"]),
            str(execution["lease"]),
            str(execution["executor"]),
            int(execution["custody_epoch"]),
        )
        source = str(record.get("_source") or "").strip()
        buckets.setdefault(key, set())
        if source:
            buckets[key].add(source)

    bindings = []
    for ep, lease_id, executor, custody_epoch in sorted(
        buckets,
        key=lambda row: (row[3], row[0], row[1], row[2]),
    ):
        bindings.append(
            {
                "ep": ep,
                "lease": lease_id,
                "executor": executor,
                "custody_epoch": custody_epoch,
                "source_refs": sorted(buckets[(ep, lease_id, executor, custody_epoch)]),
            }
        )

    return {
        "bound_fact_count": bound,
        "unbound_fact_count": unbound,
        "bindings": bindings,
    }


def partition_ledger(
    indexed: Mapping[str, Any], ledger: Iterable[Mapping[str, Any]]
) -> tuple[dict[str, list[dict[str, Any]]], list[dict[str, Any]]]:
    """Validate every facts record. Invalid/forbidden/unknown records are rejected, never trusted."""
    accepted: dict[str, list[tuple[int, int, dict[str, Any]]]] = {}
    rejected: list[dict[str, Any]] = []
    leaves = [ref for ref, n in indexed["nodes"].items() if n["kind"] == "LEAF"]
    for position, entry in enumerate(ledger):
        facts = entry.get("facts") if isinstance(entry, Mapping) else None
        source = str((entry or {}).get("source") or f"ledger[{position}]")
        errors = validate_facts(facts)
        if not errors and (entry or {}).get("untrusted_author"):
            errors = [f"author {(entry or {})['untrusted_author']} is not a trusted fact author for this programme"]
        if not errors:
            claimed_issue = facts["responsibility"]["issue"]
            leaf_ref = next((ref for ref in leaves if same_ref(ref, claimed_issue)), None)
            if leaf_ref is None:
                errors = [f"responsibility.issue: {facts['responsibility']['issue']} is not a declared LEAF"]
            else:
                node = indexed["nodes"][leaf_ref]
                declared_id = node.get("responsibility_id")
                claimed = facts["responsibility"]
                claimed_id = claimed.get("id")
                if indexed["stable_identity_mode"]:
                    expected = {
                        "id": declared_id,
                        "spec_generation": node.get("spec_generation"),
                        "contract_digest": node.get("contract_digest"),
                    }
                    for field, value in expected.items():
                        if claimed.get(field) is None:
                            errors.append(f"responsibility.{field}: required for stable-identity facts")
                        elif claimed.get(field) != value:
                            errors.append(
                                f"responsibility.{field}: {claimed.get(field)} does not match planned {value}"
                            )
                elif declared_id and claimed_id and declared_id != claimed_id:
                    errors = [f"responsibility.id: {claimed_id} does not match planned {declared_id}"]
        if errors:
            rejected.append({"source": source, "reasons": errors})
            continue
        order = entry.get("order")
        record = dict(facts)
        record["_source"] = source
        if isinstance((entry or {}).get("provider"), Mapping):
            record["_provider"] = copy.deepcopy(entry["provider"])
        accepted.setdefault(leaf_ref, []).append(
            (int(order) if isinstance(order, int) and not isinstance(order, bool) else position, position, record)
        )
    return (
        {ref: [item[2] for item in sorted(rows, key=lambda r: (r[0], r[1]))] for ref, rows in accepted.items()},
        rejected,
    )



_TOPOLOGY_ASSEMBLER_MODULE: Any | None = None


def _topology_assembler_module():
    """Load the already-qualified R2 assembler lazily to avoid a module-import cycle."""
    global _TOPOLOGY_ASSEMBLER_MODULE
    if _TOPOLOGY_ASSEMBLER_MODULE is None:
        path = Path(__file__).resolve().with_name("decomposition_assembler_v35.py")
        spec = importlib.util.spec_from_file_location("decomposition_assembler_v35_for_projection", path)
        module = importlib.util.module_from_spec(spec)
        if spec.loader is None:  # pragma: no cover
            raise DelpError(f"cannot load topology assembler {path}")
        spec.loader.exec_module(module)
        _TOPOLOGY_ASSEMBLER_MODULE = module
    return _TOPOLOGY_ASSEMBLER_MODULE


_TOPOLOGY_OBSERVER_MODULE: Any | None = None


def _topology_observer_module():
    """Load the qualified read-only repository observer lazily."""
    global _TOPOLOGY_OBSERVER_MODULE
    if _TOPOLOGY_OBSERVER_MODULE is None:
        path = Path(__file__).resolve().with_name("decomposition_observer_v35.py")
        spec = importlib.util.spec_from_file_location("decomposition_observer_v35_for_projection", path)
        module = importlib.util.module_from_spec(spec)
        if spec.loader is None:  # pragma: no cover
            raise DelpError(f"cannot load topology observer {path}")
        spec.loader.exec_module(module)
        _TOPOLOGY_OBSERVER_MODULE = module
    return _TOPOLOGY_OBSERVER_MODULE


def _local_repository_slug(repo_root: Path | str) -> str:
    root = Path(repo_root).resolve()
    proc = subprocess.run(
        ["git", "-C", str(root), "config", "--get", "remote.origin.url"],
        text=True,
        capture_output=True,
        check=False,
    )
    if proc.returncode or not proc.stdout.strip():
        raise DelpError(f"{root}: cannot resolve remote.origin.url for topology observation")
    remote = proc.stdout.strip().replace("\\", "/")
    match = re.search(r"github\.com[/:]([^/]+)/([^/]+?)(?:\.git)?$", remote, re.IGNORECASE)
    if not match:
        raise DelpError(f"{root}: origin is not a supported GitHub repository URL: {remote!r}")
    return f"{match.group(1)}/{match.group(2)}"


def observe_topology_repository(
    graph: Any,
    repo_root: Path | str,
    expected_repository: str | None = None,
) -> dict[str, dict[str, Any]]:
    """Derive R2 repository observations from a checked-out Git tree; read-only."""
    indexed = validate_graph(graph)
    if not (indexed.get("acceptance_claims") or indexed.get("topology_assessments")):
        return {}
    observer = _topology_observer_module()
    root = Path(repo_root).resolve()
    if expected_repository is not None:
        local_repository = _local_repository_slug(root)
        if local_repository.lower() != str(expected_repository).strip().lower():
            raise DelpError(
                f"{root}: local topology repository {local_repository!r} does not match "
                f"expected GitHub repository {expected_repository!r}"
            )
    rows: dict[str, dict[str, Any]] = {}
    for ref in indexed["order"]:
        if indexed["nodes"][ref]["kind"] != "LEAF":
            continue
        try:
            rows[ref] = observer.observe_repository_basis(
                graph,
                leaf_ref=ref,
                repo_root=root,
            )
        except Exception as exc:
            raise DelpError(f"{ref}: topology repository observation failed: {exc}") from exc
    return rows


def project(
    graph: Any,
    ledger: Iterable[Mapping[str, Any]] = (),
    observations: Mapping[str, Mapping[str, Any]] | None = None,
    topology_observations: Mapping[str, Mapping[str, Any]] | None = None,
    custody_state: Mapping[str, Any] | None = None,
    custody_lease: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Recompute every node from plan, facts, provider truth, topology and optional active custody."""
    ledger = list(ledger)
    if topology_observations is None:
        topology_observations = {}
    if not isinstance(topology_observations, Mapping):
        raise DelpError("topology_observations: must be a mapping keyed by declared leaf reference")
    indexed = validate_graph(graph)
    nodes = indexed["nodes"]
    observations = normalize_observations(indexed, observations)
    accepted_all, rejected = partition_ledger(indexed, ledger)
    if (custody_state is None) != (custody_lease is None):
        raise DelpError("custody_state and custody_lease must be supplied together")
    accepted = accepted_all
    fenced_facts: list[dict[str, Any]] = []
    custody_summaries: dict[str, dict[str, Any]] = {}
    custody_fence = None
    if custody_state is not None and custody_lease is not None:
        accepted, fenced_facts, custody_summaries, custody_fence = apply_custody_fact_fence(
            accepted_all,
            custody_state,
            custody_lease,
        )
    results: dict[str, dict[str, Any]] = {}
    mode = indexed["policy"]["mode"]

    for ref in indexed["order"]:
        if nodes[ref]["kind"] == "LEAF":
            records = accepted.get(ref, [])
            results[ref] = compute_leaf(nodes[ref], records, observations.get(nodes[ref]["number"]))
            results[ref]["execution_provenance"] = execution_provenance(accepted_all.get(ref, []))
            if custody_fence is not None:
                results[ref]["custody_fence"] = custody_summaries.get(
                    ref,
                    {
                        "active_execution": {
                            key: custody_fence[key]
                            for key in ("ep", "lease", "executor", "custody_epoch")
                        },
                        "granted_at": custody_fence["granted_at"],
                        "effective_fact_count": 0,
                        "fenced_fact_count": 0,
                        "fenced_sources": [],
                    },
                )
    if mode != "OFF":
        # Closed (COMPLETE/SUPERSEDED) leaves are history, not work to release: the gate skips them.
        closed = {ref for ref, leaf in results.items() if leaf["lifecycle"] in _TERMINAL}
        release = decomposition_report(
            graph,
            mode,
            closed,
            topology_observations=topology_observations,
        )
        for ref, row in release["leaves"].items():
            leaf = results[ref]
            leaf["plan"] = {
                "mode": mode,
                "releasable": row["releasable"],
                "blockers": copy.deepcopy(row["blockers"]),
                "advisories": copy.deepcopy(row["advisories"]),
            }
            if row.get("topology") is not None:
                leaf["plan"]["topology"] = copy.deepcopy(row["topology"])
            if row["blockers"]:
                leaf["warnings"].append(
                    "DECOMPOSITION_BLOCKERS:" + ",".join(sorted({b["code"] for b in row["blockers"]}))
                )
            if row["advisories"]:
                leaf["warnings"].append(
                    "DECOMPOSITION_ADVISORIES:" + ",".join(sorted({a["code"] for a in row["advisories"]}))
                )
            if mode == "ENFORCED" and not row["releasable"] and leaf["state"] in _PLAN_OVERLAID_STATES:
                leaf["state"] = "NOT_RELEASEABLE"

    for ref in indexed["order"]:
        if nodes[ref]["kind"] != "LEAF":
            continue
        results[ref]["conditions"] = [
            *_plan_spec_conditions(
                indexed,
                ref,
                results[ref],
                accepted.get(ref, []),
            ),
            *_provider_evidence_conditions(
                indexed,
                ref,
                results[ref],
                observations.get(nodes[ref]["number"]),
                accepted.get(ref, []),
            ),
        ]

    # Serial decomposition is an execution constraint, not documentation. Dependency readiness is derived only
    # from predecessor projections; agents never author it and it never changes P/E/D.
    for ref in indexed["order"]:
        if nodes[ref]["kind"] != "LEAF":
            continue
        declared_dependencies = list(nodes[ref]["depends_on"])
        blocking_dependencies = [
            {
                "ref": dep,
                "state": results[dep]["state"],
                "lifecycle": results[dep]["lifecycle"],
            }
            for dep in declared_dependencies
            if results[dep]["lifecycle"] != "COMPLETE"
        ]
        results[ref]["dependencies"] = {
            "declared": declared_dependencies,
            "ready": not blocking_dependencies,
            "blocking": blocking_dependencies,
        }
        if blocking_dependencies and results[ref]["state"] in {"ACTIVE", "NOT_STARTED"}:
            results[ref]["state"] = "WAITING_DEPENDENCY"

    for ref in indexed["order"]:
        if nodes[ref]["kind"] != "LEAF":
            continue
        results[ref]["conditions"].append(
            _dependency_condition(indexed, ref, results[ref])
        )
        results[ref]["conditions"].extend(
            _custody_assurance_placeholders(indexed, ref)
        )
        results[ref]["conditions"] = _finalize_condition_set(
            results[ref]["conditions"]
        )
        results[ref]["actual_next"] = _derive_actual_next_v35(results[ref])

    health_mode = indexed["health_policy"]["mode"]
    if health_mode != "OFF":
        # Advisory telemetry for leaves that have started and are not finished: it adds a block, never a state or a number.
        for ref, leaf in results.items():
            if leaf["lifecycle"] in {"NOT_STARTED", "COMPLETE", "SUPERSEDED"}:
                continue
            seen = observations.get(nodes[ref]["number"]) or {}
            leaf["health"] = _health_block(
                _health_components(leaf, nodes[ref], seen, indexed["health_policy"], indexed["policy"]["leaf_budget"])
            )

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
        unmaterialized = [leaf for leaf in _leaves_under(indexed, ref) if results[leaf]["lifecycle"] == "UNMATERIALIZED"]
        if D == 1 and all(r["lifecycle"] in _TERMINAL for r in leaf_rows) and node["reserve_weight"] == 0:
            state = "COMPLETE"
        elif any(r["state"] == "STALE" for r in critical):
            state = "STALE"
        elif unmaterialized:
            state = "UNMATERIALIZED"  # the roll-up below is a lower bound: it cannot see the work the ledger lacks
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
        if unmaterialized:
            warnings.append(f"UNMATERIALIZED_LEAVES:{len(unmaterialized)}")
        result = {
            "lifecycle": {"COMPLETE": "COMPLETE", "IDLE": "IDLE", "PLAN_GAP": "IDLE", "UNMATERIALIZED": "UNMATERIALIZED"}.get(
                state, "ACTIVE"
            ),
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
        if unmaterialized:
            result["materialization"] = {"status": "UNMATERIALIZED", "leaves": unmaterialized}
        if health_mode != "OFF":
            rollup = _health_rollup([(leaf, results[leaf]["health"]) for leaf in _leaves_under(indexed, ref) if "health" in results[leaf]])
            if rollup:
                result["health"] = rollup
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
                    "spec_generation": node.get("spec_generation"),
                    "contract_digest": node.get("contract_digest"),
                },
                "currentness": {
                    "mode": "STABLE" if indexed["stable_identity_mode"] else "LEGACY",
                    "graph_generation": indexed["programme"]["graph_generation"],
                    "graph_digest": indexed["digest"],
                    "spec_generation": node.get("spec_generation"),
                    "contract_digest": node.get("contract_digest"),
                    "fact_binding_required": bool(indexed["stable_identity_mode"] and node["kind"] == "LEAF"),
                },
                "weight": node["weight"],
            }
        )
        if node["kind"] == "LEAF":
            public["material"] = {
                "primary_pr": node.get("primary_pr"),
                "candidate_sha": data["frontier"]["material_candidate"],
                **_observed_material(observations.get(node["number"]) or {}),
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
        "graph_digest": indexed["digest"],
        "root": indexed["root"],
        "nodes": out_nodes,
        "rejected_facts": rejected,
        "fenced_facts": fenced_facts,
        "input_digest": canonical_digest(
            {
                "graph": indexed["digest"],
                "ledger": [
                    {
                        "source": str((e or {}).get("source") or ""),
                        "order": (e or {}).get("order"),
                        "facts": (e or {}).get("facts"),
                        **(
                            {"provider": (e or {}).get("provider")}
                            if custody_fence is not None
                            else {}
                        ),
                    }
                    for e in ledger
                ],
                "custody_fence": custody_fence,
                "observations": {str(k): v for k, v in sorted(observations.items())},
                "topology_observations": {
                    str(k): v
                    for k, v in sorted(topology_observations.items(), key=lambda item: str(item[0]))
                },
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
    actual_next = data.get("actual_next")
    if not isinstance(actual_next, Mapping) or not actual_next.get("action"):
        raise DelpError(f"{ref}: leaf title requires canonical actual_next")
    tokens.append(f"NEXT:{actual_next['action']}")
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


def _takeover_entry_requirement(owner_intent: Any) -> dict[str, Any] | None:
    if owner_intent is None:
        return None
    if not isinstance(owner_intent, Mapping):
        raise DelpError("owner_intent: must be a mapping")
    payload = owner_intent.get("owner_intent") if isinstance(owner_intent.get("owner_intent"), Mapping) else owner_intent
    intent = owner_intent.get("intent")
    deliverables = payload.get("requested_deliverables") or []
    kinds = {row.get("type") for row in deliverables if isinstance(row, Mapping) and isinstance(row.get("type"), str)}
    takeover = intent == "TAKEOVER_RECONCILE" or {
        "ENTRY_RECONCILIATION", "PHASE_PLAN_REFRESH", "BOUNDED_CHILD_BLOCK"
    }.issubset(kinds)
    if not takeover:
        return None
    source_ref = payload.get("source_ref")
    if not isinstance(source_ref, str) or not source_ref.strip():
        return {"error": "OWNER_INTENT_SOURCE_REQUIRED", "detail": "takeover/lateral admission requires durable owner_intent.source_ref"}
    basis = {
        "source_ref": source_ref,
        "verbatim_request": payload.get("verbatim_request"),
        "target": payload.get("target"),
        "requested_deliverables": deliverables,
        "boundary_constraints": payload.get("boundary_constraints") or [],
    }
    return {"session_digest": canonical_digest(basis), "source_ref": source_ref}


def entry_session_digest(owner_intent: Any) -> str:
    requirement = _takeover_entry_requirement(owner_intent)
    if requirement is None:
        raise DelpError("owner_intent is not a takeover/lateral entry")
    if requirement.get("error"):
        raise DelpError(str(requirement["detail"]))
    return str(requirement["session_digest"])


def _entry_admission(projection: Mapping[str, Any], leaf_ref: str, owner_intent: Any) -> dict[str, Any] | None:
    requirement = _takeover_entry_requirement(owner_intent)
    if requirement is None:
        return None
    if requirement.get("error"):
        return {"code": requirement["error"], "detail": requirement["detail"]}
    leaf = projection["nodes"][leaf_ref]
    plan = leaf.get("plan")
    if not plan or plan.get("mode") != "ENFORCED" or not plan.get("releasable"):
        return {"code": "ENTRY_PLAN_NOT_RELEASEABLE", "detail": "takeover/lateral coding requires the current bounded child to pass the ENFORCED decomposition gate"}
    prepared = (leaf.get("entry") or {}).get("prepared")
    if not prepared:
        return {"code": "ENTRY_PREPARED_EVIDENCE_MISSING", "detail": "publish current PREPARED entry evidence after reconciliation, phase-plan refresh and bounded-child materialization"}
    if prepared.get("session_digest") != requirement["session_digest"]:
        return {"code": "ENTRY_OWNER_SESSION_MISMATCH", "detail": "PREPARED evidence is not bound to the active Owner entry request"}
    live_plan_digest = projection.get("plan_digest") or projection.get("graph_digest")
    if prepared.get("plan_digest") != live_plan_digest:
        return {"code": "ENTRY_PLAN_STALE", "detail": "PREPARED evidence covers a different execution graph; refresh the phase plan and evidence"}
    try:
        child_matches = same_ref(prepared.get("child_ref"), leaf_ref)
    except DelpError:
        child_matches = False
    if not child_matches:
        return {"code": "ENTRY_CHILD_MISMATCH", "detail": "PREPARED evidence names a different bounded child"}
    planned_contract = (leaf.get("identity") or {}).get("contract_digest")
    if planned_contract and prepared.get("child_contract_digest") != planned_contract:
        return {"code": "ENTRY_CHILD_CONTRACT_MISMATCH", "detail": "PREPARED evidence does not match the bounded child's current contract digest"}
    if not prepared.get("phase_plan_ref") or not prepared.get("reconciliation_ref") or not prepared.get("evidence_refs"):
        return {"code": "ENTRY_GROUNDING_MISSING", "detail": "phase-plan, reconciliation and durable evidence references are required"}
    sequence = int(prepared.get("sequence") or 0)
    if sequence == 1:
        for ref, other in projection["nodes"].items():
            if ref == leaf_ref or other.get("kind") != "LEAF":
                continue
            other_prepared = (other.get("entry") or {}).get("prepared")
            if other_prepared and other_prepared.get("session_digest") == requirement["session_digest"]:
                return {"code": "ENTRY_SEQUENCE_RESTART", "detail": f"the Owner entry session already prepared {ref}; next child must use sequence >1 and link its execution-end evidence"}
    elif sequence > 1:
        previous_ref = prepared.get("previous_leaf_ref")
        previous_source = prepared.get("previous_evidence_ref")
        if not previous_ref or not previous_source or previous_ref not in projection["nodes"]:
            return {"code": "ENTRY_PREVIOUS_END_MISSING", "detail": "sequence >1 requires the exact previous leaf and execution-end evidence"}
        previous = projection["nodes"][previous_ref]
        previous_end = (previous.get("entry") or {}).get("execution_end")
        if not previous_end:
            return {"code": "ENTRY_PREVIOUS_END_MISSING", "detail": f"{previous_ref} has no accepted EXECUTION_END entry evidence"}
        if (
            previous_end.get("session_digest") != requirement["session_digest"]
            or previous_end.get("sequence") != sequence - 1
            or previous_end.get("_source") != previous_source
        ):
            return {"code": "ENTRY_PREVIOUS_END_MISMATCH", "detail": "previous execution-end evidence does not match this Owner entry sequence"}
        if previous.get("evidence", {}).get("health") != "CURRENT":
            return {"code": "ENTRY_PREVIOUS_END_STALE", "detail": f"{previous_ref} execution-end evidence is not current"}
        if previous_end.get("_candidate_sha") != previous.get("material", {}).get("candidate_sha"):
            return {"code": "ENTRY_PREVIOUS_END_STALE", "detail": f"{previous_ref} material moved after its execution-end evidence"}
    else:
        return {"code": "ENTRY_SEQUENCE_INVALID", "detail": "PREPARED entry evidence requires sequence >=1"}
    return None


def _admit_next_text(leaf: Mapping[str, Any], decision: Mapping[str, Any]) -> str:
    """Render the canonical actual-next decision for continuation UX.

    This helper formats an already-selected action. It must never choose or
    reprioritize a Responsibility action.
    """
    action = str(decision.get("action") or "")
    detail = str(decision.get("detail") or "").strip()
    reason = str(decision.get("reason") or "").strip()

    if action == "NONE":
        return detail or f"{leaf['lifecycle']} — no further actual-next action"
    if action == "MATERIALIZE_FACTS":
        materialization = leaf.get("materialization") or {}
        signal = materialization.get("provider_signal") or "provider work"
        return (
            f"MATERIALIZE_FACTS before any new work — the provider shows {signal} but the ledger has "
            "no accepted CHECKPOINT_FACTS_V1 for this leaf; publish facts for exactly what current evidence supports "
            "(completion is never inferred)"
        )
    if action == "FIX_PLAN":
        plan = leaf.get("plan") or {}
        blockers = list(plan.get("blockers") or [])
        if blockers:
            shown = "; ".join(f"{b['code']} ({b['detail']})" for b in blockers[:3])
            more = f"; +{len(blockers) - 3} more" if len(blockers) > 3 else ""
            health = str((leaf.get("evidence") or {}).get("health") or "")
            also = f"; evidence is also {health}" if health and health != "CURRENT" else ""
            return (
                f"FIX_PLAN before coding — {shown}{more}{also} — "
                "request a plan update (split or reweight) from the Coordinator; do not start or continue units"
            )
    if action == "RECOVER_EVIDENCE":
        gaps = list((leaf.get("evidence") or {}).get("gaps") or [])
        health = str((leaf.get("evidence") or {}).get("health") or "UNKNOWN")
        gap_detail = ", ".join(f"{g['unit']}:{g['reason']}" for g in gaps) or health
        return f"RECOVER_EVIDENCE before new coding — {gap_detail}"
    if action == "RECONCILE_HANDOFF":
        policy = leaf.get("successor_policy") or {}
        return (
            "RECONCILE_HANDOFF before this high-risk unit — "
            + str(policy.get("decision_at_risk") or detail or "successor grounding required")
        )
    if action == "WAIT_DEPENDENCY":
        dependencies = leaf.get("dependencies") or {}
        blocked = ", ".join(
            f"{row['ref']}:{row['lifecycle']}" for row in dependencies.get("blocking") or []
        )
        return (
            f"WAIT_DEPENDENCY before coding — {blocked}; only COMPLETE predecessors satisfy depends_on, "
            "then reproject from durable facts"
        )
    if action == "CONTINUE_UNIT":
        return detail or str(leaf.get("active_unit") or "CONTINUE_UNIT")
    if action == "PUBLISH_RESULT":
        return detail or "Publish the scoped Responsibility result."
    return f"{action} — {detail or reason}"


def admit(
    projection: Mapping[str, Any],
    leaf_ref: str,
    command: str = "continue",
    owner_intent: Any = None,
) -> dict[str, Any]:
    """Compact reconstruction proof for continuation/takeover commands. Pure; changes nothing.

    Responsibility action authority comes only from leaf.actual_next. TAKEOVER
    entry admission is an execution-policy overlay and can block only a
    would-be CONTINUE_UNIT/PUBLISH_RESULT; it never outranks a canonical
    recovery, wait, plan, dependency, handoff, assurance or owner action.
    """
    nodes = projection["nodes"]
    if leaf_ref not in nodes or nodes[leaf_ref]["kind"] != "LEAF":
        raise DelpError(f"{leaf_ref} is not a LEAF in the projection")
    leaf = nodes[leaf_ref]
    lineage_refs = leaf["identity"]["lineage"]
    ancestors = [nodes[r] for r in lineage_refs[:-1]]
    health = leaf["evidence"]["health"]
    plan = leaf.get("plan")
    materialization = leaf.get("materialization")

    decision = leaf.get("actual_next")
    if not isinstance(decision, Mapping):
        raise DelpError("admission requires canonical leaf.actual_next")
    if decision.get("authority") != "DERIVED_ACTUAL_NEXT_ONLY":
        raise DelpError("admission requires DERIVED_ACTUAL_NEXT_ONLY actual_next authority")
    base_action = str(decision.get("action") or "")
    if not base_action:
        raise DelpError("admission requires a non-empty canonical actual_next action")

    entry_block = _entry_admission(projection, leaf_ref, owner_intent)
    entry_required = _takeover_entry_requirement(owner_intent) is not None
    if entry_block and base_action in {"CONTINUE_UNIT", "PUBLISH_RESULT"}:
        action = "RECONCILE_ENTRY"
        next_text = f"RECONCILE_ENTRY before coding — {entry_block['code']}: {entry_block['detail']}"
    else:
        action = base_action
        next_text = _admit_next_text(leaf, decision)

    report = {
        "command": command,
        "is_continuation": classify_continuation(command),
        "leaf": leaf_ref,
        "lineage": lineage_refs,
        "state": leaf["state"],
        "evidence_health": "NONE" if materialization else health,
        "action": action,
        "actual_next": dict(decision),
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
        "authority_effects": [],
    }
    if entry_required:
        report["entry_admission"] = {
            "required": True,
            "ready": entry_block is None,
            "blocker": entry_block,
            "session_digest": (_takeover_entry_requirement(owner_intent) or {}).get("session_digest"),
        }
    if leaf.get("successor_policy") is not None:
        report["successor_policy"] = leaf["successor_policy"]
    if leaf.get("handover") is not None:
        report["handover"] = leaf["handover"]
        report["handover_reconciliation_required"] = action == "RECONCILE_HANDOFF"
    if leaf.get("dependencies") is not None:
        report["dependencies"] = leaf["dependencies"]
        report["dependency_wait_required"] = action == "WAIT_DEPENDENCY"
    if plan:
        report["plan"] = plan
        report["plan_fix_required"] = action == "FIX_PLAN"
    if materialization:
        report["materialization"] = materialization
        # Pending requirement semantics are retained even when a higher
        # canonical actual-next action (for example FIX_PLAN) runs first.
        report["materialize_required"] = True
    if leaf.get("health"):
        report["health"] = leaf["health"]
    return report


def render_checkpoint(report: Mapping[str, Any]) -> str:
    short = lambda sha: (sha or "UNKNOWN")[:7]  # noqa: E731
    path = " → ".join(f"#{ref_number(r)}" for r in report["lineage"])
    pr = report["material"].get("primary_pr")
    if pr:
        path += f" → PR#{ref_number(pr)}"
    if report["evidence_health"] == "NONE":
        evidence = (
            f"NONE — no accepted facts; provider shows {report['materialization']['provider_signal']} "
            f"(live @ {short(report['material'].get('candidate_sha'))})"
        )
    elif report["evidence_health"] == "CURRENT":
        evidence = f"CURRENT @ {short(report['material'].get('candidate_sha'))}"
    else:
        evidence = (
            f"{report['evidence_health']} (evidence @ {short(report['evidence_candidate'])}, "
            f"live @ {short(report['material'].get('candidate_sha'))})"
        )
    lines = [
        "CONTINUE CHECKPOINT",
        "",
        f"PATH: {path}",
        f"CHILD: R:P{report['child']['P']}/E{report['child']['E']} · {report['child']['unit'] or 'NO_ACTIVE_UNIT'} · {report['state']}",
        f"EVIDENCE: {evidence}",
    ]
    material = report["material"]
    seen = [
        f"base {short(material['base_sha'])}" if material.get("base_sha") else None,
        f"candidate {short(material.get('candidate_sha'))}",
        f"PR {material['pr_state']}" if material.get("pr_state") else None,
        f"ahead {material['ahead_by']}" if material.get("ahead_by") is not None else None,
        f"behind {material['behind_by']}" if material.get("behind_by") is not None else None,
    ]
    if any(material.get(k) is not None for k in ("base_sha", "pr_state", "ahead_by", "behind_by")):
        lines.append("FRONTIER: " + " · ".join(s for s in seen if s))
    plan = report.get("plan")
    if plan:
        codes = ", ".join(b["code"] for b in plan["blockers"])
        if plan["blockers"]:
            lines.append(f"PLAN: {'NOT_RELEASEABLE' if plan['mode'] == 'ENFORCED' else 'WOULD_BLOCK (advisory)'} — {codes}")
        elif plan["advisories"]:
            lines.append(f"PLAN: RELEASABLE — ADVISORY: {', '.join(a['code'] for a in plan['advisories'])}")
        else:
            lines.append("PLAN: RELEASABLE")
    dependencies = report.get("dependencies")
    if dependencies and dependencies["declared"]:
        if dependencies["ready"]:
            lines.append("DEPENDENCIES: READY — " + ", ".join(dependencies["declared"]))
        else:
            shown = ", ".join(
                f"{row['ref']}:{row['lifecycle']}" for row in dependencies["blocking"]
            )
            lines.append("DEPENDENCIES: BLOCKED — " + shown)
    handover = report.get("handover")
    if handover:
        lines.append(
            "HANDOVER: "
            + handover["status"]
            + " · "
            + handover["mode"]
            + " · decision "
            + str(handover.get("decision_at_risk") or "UNKNOWN")
        )
    health = report.get("health")
    if health:
        shown = health["reasons"][:3]
        more = f"; +{len(health['reasons']) - 3} more" if len(health["reasons"]) > 3 else ""
        lines.append(f"HEALTH: {health['light']} {health['verdict']} (advisory)" + (f" — {'; '.join(shown)}{more}" if shown else ""))
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
# frontier: what a handover may honestly carry, and how a successor checks it is still true
# --------------------------------------------------------------------------

FRONTIER_DRIFT_SCHEMA = f"{SCHEMA_PREFIX}-frontier-drift"
# Provider-observed or ledger inputs a frontier depends on. A change in any of them means the handed-over values are
# stale. Divergence counts (ahead/behind) follow from the base and the candidate, so they are shown, not judged.
_FRONTIER_INPUTS = (
    ("BASE", ("observed", "base_sha")),
    ("CANDIDATE_HEAD", ("observed", "candidate_sha")),
    ("PR_STATE", ("observed", "pr_state")),
    ("LIVENESS", ("observed", "liveness")),
    ("FACTS", ("inputs", "facts", "digest")),
    ("DEPENDENCY_FACTS", ("inputs", "dependencies", "digest")),
    ("PLAN", ("inputs", "graph")),
    ("TOPOLOGY_OBSERVATIONS", ("inputs", "topology_observations")),
)
_FRONTIER_CONSEQUENCES = (
    ("STATE", ("derived", "state")),
    ("EVIDENCE_HEALTH", ("derived", "evidence", "health")),
    ("PROGRESS_P", ("derived", "progress", "P")),
    ("PROGRESS_E", ("derived", "progress", "E")),
    ("ACTIVE_UNIT", ("derived", "active_unit")),
    ("DEPENDENCIES", ("derived", "dependencies")),
    ("ACTUAL_NEXT", ("derived", "actual_next")),
    ("PLAN_RESULT", ("derived", "plan")),
)


def _dig(value: Any, path: tuple[str, ...]) -> Any:
    for key in path:
        value = value.get(key) if isinstance(value, Mapping) else None
    return value


def frontier(
    graph: Any,
    ledger: Iterable[Mapping[str, Any]],
    observations: Mapping[str, Mapping[str, Any]] | None,
    leaf_ref: str,
    topology_observations: Mapping[str, Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    """One leaf's frontier at this moment: provider-observed material, derived state, and the digests of its inputs.

    This is what a handover may honestly carry. It holds no authored number: everything in it is observed or derived,
    and it is only ever the predecessor's view at one instant, never current truth. Pure.
    """
    ledger = list(ledger)
    indexed = validate_graph(graph)
    ref = indexed["by_number"].get(ref_number(leaf_ref))
    if ref is None or indexed["nodes"][ref]["kind"] != "LEAF":
        raise DelpError(f"{leaf_ref} is not a LEAF in the graph")
    projection = project(
        graph,
        ledger,
        observations,
        topology_observations=topology_observations,
    )
    leaf = projection["nodes"][ref]
    accepted, _ = partition_ledger(indexed, ledger)
    mine = [{k: v for k, v in record.items() if k != "_source"} for record in accepted.get(ref, [])]
    dependency_facts = {
        dep: [{k: v for k, v in record.items() if k != "_source"} for record in accepted.get(dep, [])]
        for dep in indexed["nodes"][ref]["depends_on"]
    }
    material = leaf["material"]
    observed = {k: material[k] for k in ("base_sha", "candidate_sha", "pr_state", "ahead_by", "behind_by") if material.get(k) is not None}
    if leaf.get("liveness"):
        observed["liveness"] = leaf["liveness"]
    ratios = leaf["progress"]["ratio"]
    derived: dict[str, Any] = {
        "state": leaf["state"],
        "lifecycle": leaf["lifecycle"],
        "active_unit": leaf["active_unit"],
        "progress": dict(ratios),
        "evidence": {
            "health": leaf["evidence"]["health"],
            "candidate": leaf["frontier"]["evidence_candidate"],
            "gaps": [f"{g['unit']}:{g['reason']}" for g in leaf["evidence"]["gaps"]],
        },
        "conditions": copy.deepcopy(leaf["conditions"]),
        "actual_next": copy.deepcopy(leaf["actual_next"]),
        "blocker": leaf["blocker"],
        "owner_action": leaf["owner_action"],
        "dependencies": copy.deepcopy(leaf.get("dependencies") or {"declared": [], "ready": True, "blocking": []}),
    }
    if "plan" in leaf:
        derived["plan"] = {"mode": leaf["plan"]["mode"], "releasable": leaf["plan"]["releasable"], "blockers": [b["code"] for b in leaf["plan"]["blockers"]]}
    if "materialization" in leaf:
        derived["materialization"] = dict(leaf["materialization"])
    body = {
        "leaf": ref,
        "observed": observed,
        "derived": derived,
        "inputs": {
            "graph": indexed["digest"],
            "facts": {"accepted": len(mine), "digest": canonical_digest(mine)},
            "dependencies": {
                "accepted": {dep: len(records) for dep, records in dependency_facts.items()},
                "digest": canonical_digest(dependency_facts),
            },
        },
    }
    if topology_observations is not None:
        body["inputs"]["topology_observations"] = canonical_digest(
            {
                str(key): value
                for key, value in sorted(
                    topology_observations.items(),
                    key=lambda item: str(item[0]),
                )
            }
        )
    ancestors = [projection["nodes"][r] for r in leaf["identity"]["lineage"][:-1]]
    return {
        "schema": f"{SCHEMA_PREFIX}-frontier",
        "authority": AUTHORITY,
        "protocol_line": PROTOCOL_LINE,
        "lineage": leaf["identity"]["lineage"],
        "ancestors": [
            {"ref": a["ref"], "state": a["state"], "D": a["progress"]["ratio"]["D"], "E": a["progress"]["ratio"]["E"]} for a in ancestors
        ],
        **body,
        "frontier_digest": canonical_digest(body),
    }


def frontier_drift(snapshot: Mapping[str, Any], live: Mapping[str, Any]) -> dict[str, Any]:
    """Compare a handed-over frontier with the one recomputed now. Pure.

    `moved` names the inputs that changed since the snapshot (provider truth, ledger, plan): any of them means the
    handed-over values are stale and must be recomputed, never trusted. `changed` lists the derived consequences, which are
    informational. An input the snapshot never observed counts as moved once it is observed: unobserved is not unchanged.
    """
    if snapshot.get("leaf") != live.get("leaf"):
        raise DelpError(f"the snapshot is for {snapshot.get('leaf')} but the live frontier is for {live.get('leaf')}")

    def differences(fields: tuple[tuple[str, tuple[str, ...]], ...]) -> list[dict[str, Any]]:
        rows = []
        for name, path in fields:
            was, now = _dig(snapshot, path), _dig(live, path)
            if was != now:
                rows.append({"what": name, "was": was, "now": now})
        return rows

    moved = differences(_FRONTIER_INPUTS)
    for row in moved:
        if row["what"] == "FACTS":  # show the count, not two digests
            row["was"], row["now"] = _dig(snapshot, ("inputs", "facts", "accepted")), _dig(live, ("inputs", "facts", "accepted"))
            row["detail"] = "accepted facts records (content differs)" if row["was"] == row["now"] else "accepted facts records"
        elif row["what"] == "DEPENDENCY_FACTS":
            row["was"], row["now"] = (
                _dig(snapshot, ("inputs", "dependencies", "accepted")),
                _dig(live, ("inputs", "dependencies", "accepted")),
            )
            row["detail"] = "accepted dependency facts changed"
        elif row["what"] == "PLAN":
            row["was"], row["now"] = str(row["was"])[:19], str(row["now"])[:19]
    return {
        "schema": FRONTIER_DRIFT_SCHEMA,
        "authority": AUTHORITY,
        "leaf": live["leaf"],
        "status": "MOVED" if moved else "CURRENT",
        "action": "RECONCILE" if moved else "NONE",
        "moved": moved,
        "changed": differences(_FRONTIER_CONSEQUENCES),
        "snapshot_digest": snapshot.get("frontier_digest"),
        "live_digest": live.get("frontier_digest"),
    }


def render_health(projection: Mapping[str, Any], only: str | None = None) -> str:
    nodes = projection["nodes"]
    lines = ["AGENT HEALTH (advisory; observed or derived, never declared; telemetry constrains delivery and does not measure value)"]
    root = nodes[projection["root"]].get("health")
    if root and only is None:
        counts = ", ".join(f"{k} {v}" for k, v in root["counts"].items())
        lines.append(f"PROGRAMME: {root['light']} {root['verdict']} — {root['leaves']} started leaves ({counts})")
    for ref, node in nodes.items():
        if node["kind"] == "LEAF" and node.get("health") and (only is None or ref == only):
            h = node["health"]
            lines.append(f"{h['light']} {h['verdict']:<10} {ref}  {'; '.join(h['reasons']) or 'every component observed and OK'}")
    if len(lines) == 1:
        lines.append("(no started leaf to assess, or the health policy is OFF)")
    return "\n".join(lines)


def render_frontier(snapshot: Mapping[str, Any]) -> str:
    o, d = snapshot["observed"], snapshot["derived"]
    short = lambda sha: (sha or "UNOBSERVED")[:7]  # noqa: E731
    lines = [
        f"FRONTIER (derived, observed at one instant; not current truth) — {snapshot['leaf']}",
        f"PATH: {' → '.join('#' + str(ref_number(r)) for r in snapshot['lineage'])}",
        f"MATERIAL: base {short(o.get('base_sha'))} · candidate {short(o.get('candidate_sha'))}"
        + (f" · PR {o['pr_state']}" if o.get("pr_state") else "")
        + (f" · ahead {o['ahead_by']}" if o.get("ahead_by") is not None else "")
        + (f" · behind {o['behind_by']}" if o.get("behind_by") is not None else ""),
        f"STATE: {d['state']} · P {d['progress']['P']} · E {d['progress']['E']} · unit {d['active_unit'] or 'NONE'}",
        f"EVIDENCE: {d['evidence']['health']}" + (f" ({', '.join(d['evidence']['gaps'])})" if d["evidence"]["gaps"] else ""),
        f"FRONTIER_DIGEST: {snapshot['frontier_digest']}",
    ]
    return "\n".join(lines)


def render_frontier_drift(report: Mapping[str, Any]) -> str:
    short = lambda v: str(v)[:7] if isinstance(v, str) and _SHA.fullmatch(v) else str(v)  # noqa: E731
    lines = [f"FRONTIER DRIFT — {report['status']} ({report['leaf']})"]
    lines += [f"  MOVED   {r['what']}: {short(r['was'])} -> {short(r['now'])}" + (f" ({r['detail']})" if r.get("detail") else "") for r in report["moved"]]
    lines += [f"  changed {r['what']}: {short(r['was'])} -> {short(r['now'])}" for r in report["changed"]]
    lines.append(
        "ACTION: NONE — every input is as the predecessor observed it"
        if report["status"] == "CURRENT"
        else "ACTION: RECONCILE — the handed-over frontier is stale; recompute from live truth before acting (a handover is the predecessor's view at one instant, never current truth)"
    )
    return "\n".join(lines)


# --------------------------------------------------------------------------
# provider surface: compare-and-swap by version + digest (no last-writer-wins)
# --------------------------------------------------------------------------


def status_document(node_projection: Mapping[str, Any], *, version: int, digest: str, programme: Mapping[str, Any]) -> dict[str, Any]:
    """LIVE_STATUS_V1 document written to the provider for one node."""
    # LIVE_STATUS is a disposable read model. LEAF conditions + actual_next are
    # already canonical derived kernel state and are published here without
    # becoming a new authority.
    body = {
        k: v
        for k, v in node_projection.items()
        if k != "title_prefix"
    }
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
        topology_observation_provider: Callable[[], Mapping[str, Mapping[str, Any]]] | None = None,
    ) -> None:
        self.graph = graph
        self.ledger_provider = ledger_provider
        self.observation_provider = observation_provider
        self.topology_observation_provider = topology_observation_provider or (lambda: {})
        self._projection: dict[str, Any] | None = None

    def invalidate(self) -> None:
        self._projection = None

    def projection(self) -> dict[str, Any]:
        if self._projection is None:
            self._projection = project(
                self.graph,
                self.ledger_provider(),
                self.observation_provider(),
                topology_observations=self.topology_observation_provider(),
            )
        return self._projection


def sync_projection(
    store: Any,
    graph: Any,
    ledger_provider: Callable[[], Iterable[Mapping[str, Any]]],
    observation_provider: Callable[[], Mapping[str, Mapping[str, Any]]],
    base_titles: Mapping[str, str],
    topology_observation_provider: Callable[[], Mapping[str, Mapping[str, Any]]] | None = None,
) -> dict[str, Any]:
    """Project every node and write each with compare-and-swap. Leaves first, root last."""
    indexed = validate_graph(graph)
    cache = _InputCache(
        graph,
        ledger_provider,
        observation_provider,
        topology_observation_provider,
    )
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


def _provider_comment_timestamp(value: Any, label: str) -> tuple[str, datetime]:
    """Validate and normalize one provider-authored issue-comment timestamp."""
    if not isinstance(value, str) or not value.strip():
        raise DelpError(f"{label}: provider timestamp required")
    raw = value.strip()
    try:
        parsed = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError as exc:
        raise DelpError(f"{label}: valid ISO-8601 provider timestamp required") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise DelpError(f"{label}: timezone-aware provider timestamp required")
    utc = parsed.astimezone(timezone.utc)
    return utc.isoformat().replace("+00:00", "Z"), utc


def _github_comment_provider_envelope(comment: Mapping[str, Any]) -> dict[str, Any]:
    """Return provider-authored publication/edit time for one GitHub issue comment."""
    created_text, created = _provider_comment_timestamp(
        comment.get("created_at"),
        "GitHub comment.created_at",
    )
    updated_text, updated = _provider_comment_timestamp(
        comment.get("updated_at"),
        "GitHub comment.updated_at",
    )
    if updated < created:
        raise DelpError("GitHub comment.updated_at: cannot precede created_at")
    return {
        "kind": "GITHUB_ISSUE_COMMENT",
        "created_at": created_text,
        "updated_at": updated_text,
    }


def custody_fence_from_state_lease(
    state: Mapping[str, Any], lease: Mapping[str, Any]
) -> dict[str, Any]:
    """Derive the active custody fence without creating a second custody authority."""
    binding = execution_binding_from_state_lease(state, lease)
    custody = lease.get("custody")
    granted_raw = custody.get("granted_at") if isinstance(custody, Mapping) else None
    granted_at, _ = _provider_comment_timestamp(
        granted_raw,
        "LEASE.custody.granted_at",
    )
    return {
        **binding,
        "granted_at": granted_at,
    }


def classify_fact_custody(
    entry: Mapping[str, Any],
    state: Mapping[str, Any],
    lease: Mapping[str, Any],
) -> dict[str, Any]:
    """Classify one fact against active custody without filtering or changing the fact."""
    if not isinstance(entry, Mapping) or not isinstance(entry.get("facts"), Mapping):
        raise DelpError("custody classification requires one ledger entry with facts")
    errors = validate_facts(entry["facts"])
    if errors:
        raise DelpError("cannot classify invalid facts: " + "; ".join(errors))

    fact_execution = entry["facts"].get("execution")
    fence = custody_fence_from_state_lease(state, lease)
    base = {
        "active_execution": {
            key: fence[key]
            for key in ("ep", "lease", "executor", "custody_epoch")
        },
        "fence_granted_at": fence["granted_at"],
        "fact_execution": copy.deepcopy(fact_execution),
        "provider_updated_at": None,
    }

    provider = entry.get("provider")
    if not isinstance(provider, Mapping) or provider.get("kind") != "GITHUB_ISSUE_COMMENT":
        if not isinstance(fact_execution, Mapping):
            return {
                **base,
                "relation": "UNBOUND",
                "reason": "FACT_EXECUTION_UNBOUND_PROVIDER_TIME_UNAVAILABLE",
            }
        return {
            **base,
            "relation": "UNKNOWN",
            "reason": "PROVIDER_TIME_UNAVAILABLE",
        }

    updated_text, updated = _provider_comment_timestamp(
        provider.get("updated_at"),
        "ledger provider.updated_at",
    )
    _, granted = _provider_comment_timestamp(
        fence["granted_at"],
        "LEASE.custody.granted_at",
    )
    base["provider_updated_at"] = updated_text

    if not isinstance(fact_execution, Mapping):
        if updated < granted:
            return {
                **base,
                "relation": "UNBOUND",
                "reason": "UNBOUND_PUBLISHED_BEFORE_CURRENT_GRANT",
            }
        if updated > granted:
            return {
                **base,
                "relation": "UNKNOWN",
                "reason": "UNBOUND_POST_FENCE_CANNOT_PROVE_CURRENT_CUSTODY",
            }
        return {
            **base,
            "relation": "UNKNOWN",
            "reason": "UNBOUND_FENCE_TIMESTAMP_TIE",
        }

    fact_epoch = int(fact_execution["custody_epoch"])
    active_epoch = int(fence["custody_epoch"])
    exact_binding = all(
        fact_execution.get(key) == fence[key]
        for key in ("ep", "lease", "executor", "custody_epoch")
    )

    if fact_epoch == active_epoch:
        if not exact_binding:
            return {
                **base,
                "relation": "UNKNOWN",
                "reason": "CURRENT_EPOCH_IDENTITY_MISMATCH",
            }
        if updated < granted:
            return {
                **base,
                "relation": "UNKNOWN",
                "reason": "CURRENT_EPOCH_PREDATES_GRANT",
            }
        return {
            **base,
            "relation": "CURRENT_EPOCH",
            "reason": "ACTIVE_EXECUTION_BINDING_MATCH",
        }

    if fact_epoch > active_epoch:
        return {
            **base,
            "relation": "UNKNOWN",
            "reason": "FUTURE_CUSTODY_EPOCH",
        }

    if updated < granted:
        return {
            **base,
            "relation": "HISTORICAL_PRE_FENCE",
            "reason": "OLDER_EPOCH_PUBLISHED_BEFORE_CURRENT_GRANT",
        }
    if updated > granted:
        return {
            **base,
            "relation": "STALE_POST_FENCE",
            "reason": "OLDER_EPOCH_PUBLISHED_AFTER_CURRENT_GRANT",
        }
    return {
        **base,
        "relation": "UNKNOWN",
        "reason": "FENCE_TIMESTAMP_TIE",
    }


def apply_custody_fact_fence(
    accepted: Mapping[str, list[dict[str, Any]]],
    state: Mapping[str, Any],
    lease: Mapping[str, Any],
) -> tuple[
    dict[str, list[dict[str, Any]]],
    list[dict[str, Any]],
    dict[str, dict[str, Any]],
    dict[str, Any],
]:
    """Return effective semantic facts while retaining fenced facts as audit evidence."""
    fence = custody_fence_from_state_lease(state, lease)
    active_execution = {
        key: fence[key]
        for key in ("ep", "lease", "executor", "custody_epoch")
    }
    effective: dict[str, list[dict[str, Any]]] = {}
    fenced: list[dict[str, Any]] = []
    summaries: dict[str, dict[str, Any]] = {}

    for ref, records in accepted.items():
        kept: list[dict[str, Any]] = []
        leaf_fenced: list[str] = []
        for record in records:
            facts = {
                key: copy.deepcopy(value)
                for key, value in record.items()
                if not str(key).startswith("_")
            }
            entry: dict[str, Any] = {"facts": facts}
            if isinstance(record.get("_provider"), Mapping):
                entry["provider"] = copy.deepcopy(record["_provider"])
            relation = classify_fact_custody(entry, state, lease)
            unsafe = relation["relation"] in {"STALE_POST_FENCE", "UNKNOWN"}
            if unsafe:
                source = str(record.get("_source") or "")
                leaf_fenced.append(source)
                fenced.append(
                    {
                        "leaf": ref,
                        "source": source,
                        "relation": relation["relation"],
                        "reason": relation["reason"],
                        "fact_execution": copy.deepcopy(relation["fact_execution"]),
                        "provider_updated_at": relation["provider_updated_at"],
                        "fence_granted_at": relation["fence_granted_at"],
                    }
                )
            else:
                kept.append(record)
        effective[ref] = kept
        summaries[ref] = {
            "active_execution": copy.deepcopy(active_execution),
            "granted_at": fence["granted_at"],
            "effective_fact_count": len(kept),
            "fenced_fact_count": len(leaf_fenced),
            "fenced_sources": sorted(source for source in leaf_fenced if source),
        }

    return effective, fenced, summaries, fence


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
            blocks = extract_facts_blocks(str(comment.get("body") or ""))
            provider = _github_comment_provider_envelope(comment) if blocks else None
            for facts in blocks:
                row = {
                    "source": f"{ref}#issuecomment-{comment.get('id')}",
                    "order": int(comment.get("id") or 0),
                    "provider": provider,
                    "facts": facts,
                }
                if not trusted:
                    row["untrusted_author"] = login or "UNKNOWN"
                ledger.append(row)
    return ledger


def require_repository_match(graph: Any, repository: str, *, live: bool) -> None:
    """A plan may only be applied to the repository it declares.

    Issue numbers in a plan are not globally unique, and the shipped examples deliberately reuse numbers that exist
    in real repositories. A live `sync-github` therefore needs `programme.repository` and refuses on any mismatch; a
    dry run (read-only) may omit it but is still refused when it declares a different repository.
    """
    declared = (graph.get("programme") or {}).get("repository") if isinstance(graph, Mapping) else None
    if declared is None or not str(declared).strip():
        if live:
            raise DelpError(
                "programme.repository is required for a live sync-github and must equal --repository, "
                "so that a plan can never write to another repository"
            )
        return
    if str(declared).strip().lower() != str(repository).strip().lower():
        raise DelpError(
            f"programme.repository {str(declared).strip()!r} does not match --repository {repository!r}: "
            "refusing to read or write (the shipped examples declare example/delp-demo for this reason)"
        )


def plan_github(transport: Any, graph: Any, repo_root: Path | str = Path.cwd()) -> dict[str, Any]:
    """Read-only dry run of `sync-github`: what would change, what drifted, what was rejected. Writes nothing."""
    indexed = validate_graph(graph)
    titles = {ref: str(transport.get_issue(ref_number(ref)).get("title") or "") for ref in indexed["nodes"]}
    projection = project(
        graph,
        ledger_from_github(transport, graph),
        observe_github(transport, graph),
        topology_observations=observe_topology_repository(
            graph,
            repo_root,
            expected_repository=getattr(transport, "repository", None),
        ),
    )
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

    A leaf's candidate is its primary PR head, or the head of `candidate_ref` when it has no PR. A branch-only leaf
    also gets `ahead_by` / `behind_by` against `programme.base_ref` (default `main`): commits beyond the base are the
    provider's proof that work exists, which is what separates an unreported leaf from one that has not started.
    """
    indexed = validate_graph(graph)
    base_ref = str(indexed["programme"].get("base_ref") or "main")
    base_sha = str(transport.get_commit_sha(base_ref) or "") or None  # one read per pass: the head every leaf is measured against
    observed: dict[str, dict[str, Any]] = {}
    for ref, node in indexed["nodes"].items():
        if node["kind"] != "LEAF":
            continue
        pr = node.get("primary_pr")
        if pr:
            pull = transport.get_pull(ref_number(pr))
            observed[ref] = {
                "schema": OBSERVATION_SCHEMA,
                "visibility": "OBSERVED",
                "material": {
                    "candidate_sha": str((pull.get("head") or {}).get("sha") or "") or None,
                    "pr_state": "MERGED" if pull.get("merged") else str(pull.get("state") or "UNKNOWN").upper(),
                    "base_sha": base_sha,
                },
            }
        elif node.get("candidate_ref"):
            comparison = transport.compare(base_ref, node["candidate_ref"])
            observed[ref] = {
                "schema": OBSERVATION_SCHEMA,
                "visibility": "OBSERVED",
                "material": {
                    "candidate_sha": str(transport.get_commit_sha(node["candidate_ref"]) or "") or None,
                    "ahead_by": int(comparison.get("ahead_by") or 0),
                    "behind_by": int(comparison.get("behind_by") or 0),
                    "base_sha": base_sha,
                },
            }
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

    def compare(self, base: str, head: str) -> dict[str, Any]:
        return self._gh(f"repos/{self.repository}/compare/{base}...{head}")

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

    bf = sub.add_parser(
        "bind-facts",
        help="Stamp current Responsibility id/spec_generation/contract_digest from the graph before publication.",
    )
    bf.add_argument("--graph", type=Path, required=True)
    bf.add_argument("--facts", type=Path, required=True, help="Exactly one facts record or one CHECKPOINT_FACTS_V1 block.")
    bf.add_argument("--output", type=Path)

    dc = sub.add_parser(
        "decompose-check",
        help="Judge the plan against the decomposition policy; exit 1 on blockers when the effective mode is ENFORCED.",
    )
    dc.add_argument("--graph", type=Path, required=True)
    dc.add_argument("--mode", choices=POLICY_MODES, help="Override programme.decomposition_policy.mode for this run.")
    dc.add_argument("--facts", type=Path, nargs="*", default=[], help="Skip leaves these facts show COMPLETE or SUPERSEDED.")
    dc.add_argument("--observations", type=Path)
    dc.add_argument("--topology-observations", type=Path)
    dc.add_argument("--json", action="store_true")

    gd = sub.add_parser("graph-diff", help="Check that a re-plan conserves progress and records its scope changes; exit 1 on blockers.")
    gd.add_argument("--old", type=Path, required=True, help="The plan being replaced (e.g. the PR base version).")
    gd.add_argument("--new", type=Path, required=True)
    gd.add_argument("--json", action="store_true")

    fr = sub.add_parser(
        "frontier",
        help="One leaf's derived frontier at this instant (observed material, derived state, input digests): what a handover may carry.",
    )
    fv = sub.add_parser(
        "frontier-verify",
        help="Compare a handed-over frontier with the live one; exit 2 when any input moved (the handover is stale).",
    )
    for sp in (fr, fv):
        sp.add_argument("--graph", type=Path, required=True)
        sp.add_argument("--facts", type=Path, nargs="*", default=[])
        sp.add_argument("--observations", type=Path)
        sp.add_argument("--topology-observations", type=Path)
        sp.add_argument("--repository", help="Observe live from GitHub (read-only) instead of --facts / --observations.")
        sp.add_argument("--repo-root", type=Path, default=Path.cwd(), help="Checked-out Git repository used for read-only topology observation.")
        sp.add_argument("--leaf", required=True)
    fr.add_argument("--output", type=Path)
    fr.add_argument("--text", action="store_true", help="Human-readable form instead of JSON.")
    fv.add_argument("--snapshot", type=Path, required=True, help="The frontier JSON the predecessor handed over.")
    fv.add_argument("--json", action="store_true")

    hl = sub.add_parser(
        "health",
        help="Advisory delivery-continuity health of started leaves: observed or derived, never declared. Always exits 0.",
    )
    hl.add_argument("--graph", type=Path, required=True)
    hl.add_argument("--facts", type=Path, nargs="*", default=[])
    hl.add_argument("--observations", type=Path)
    hl.add_argument("--topology-observations", type=Path)
    hl.add_argument("--mode", choices=HEALTH_MODES, default="ADVISORY", help="Override programme.health_policy.mode for this run.")
    hl.add_argument("--leaf", help="Show a single leaf.")
    hl.add_argument("--json", action="store_true")

    pr = sub.add_parser("project")
    pr.add_argument("--graph", type=Path, required=True)
    pr.add_argument("--facts", type=Path, nargs="*", default=[])
    pr.add_argument("--observations", type=Path)
    pr.add_argument("--topology-observations", type=Path)
    pr.add_argument("--base-titles", type=Path)
    pr.add_argument("--output", type=Path)

    ad = sub.add_parser("admit", help="Reconstruct-before-continue checkpoint for continue/proceed/next/resume.")
    ad.add_argument("--graph", type=Path, required=True)
    ad.add_argument("--facts", type=Path, nargs="*", default=[])
    ad.add_argument("--observations", type=Path)
    ad.add_argument("--topology-observations", type=Path)
    ad.add_argument("--leaf", required=True)
    ad.add_argument("--command", default="continue")
    ad.add_argument("--owner-intent", type=Path, help="Parsed Owner command/envelope; TAKEOVER_RECONCILE enables entry admission.")
    ad.add_argument("--json", action="store_true")

    vt = sub.add_parser("verify-titles", help="Report hand-edited, stale, missing or legacy titles; exit 2 on drift.")
    vt.add_argument("--graph", type=Path, required=True)
    vt.add_argument("--facts", type=Path, nargs="*", default=[])
    vt.add_argument("--observations", type=Path)
    vt.add_argument("--topology-observations", type=Path)
    vt.add_argument("--actual-titles", type=Path, required=True)

    gh = sub.add_parser(
        "sync-github",
        help="Observe live PR heads + CHECKPOINT_FACTS_V1 comments, then write titles and LIVE_STATUS with compare-and-swap (uses gh).",
    )
    gh.add_argument("--graph", type=Path, required=True)
    gh.add_argument("--repository", required=True)
    gh.add_argument("--dry-run", action="store_true", help="Read-only: report drift, rejected facts and expected titles; write nothing.")
    gh.add_argument("--repo-root", type=Path, default=Path.cwd(), help="Checked-out Git repository used for read-only topology observation.")

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
        if args.cmd == "bind-facts":
            rows = _load_ledger([args.facts])
            if len(rows) != 1:
                raise DelpError(f"bind-facts requires exactly one facts record; found {len(rows)}")
            bound = bind_facts_to_graph(_load_structured(args.graph), rows[0]["facts"])
            _emit(bound, args.output)
            return 0
        if args.cmd == "graph-diff":
            diff = graph_diff(_load_structured(args.old), _load_structured(args.new))
            if args.json:
                _emit(diff, None)
            else:
                print(render_graph_diff(diff))
            return 0 if diff["conserved"] else 1

        graph = _load_structured(args.graph)
        if args.cmd == "decompose-check":
            topology_observations = (
                _load_structured(args.topology_observations)
                if args.topology_observations
                else {}
            )
            closed: list[str] = []
            if args.facts:
                seen = project(
                    graph,
                    _load_ledger(args.facts),
                    _load_structured(args.observations) if args.observations else {},
                    topology_observations=topology_observations,
                )
                closed = [r for r, n in seen["nodes"].items() if n["kind"] == "LEAF" and n["lifecycle"] in _TERMINAL]
            report = decomposition_report(
                graph,
                args.mode,
                closed,
                topology_observations=topology_observations,
            )
            if args.json:
                _emit(report, None)
            else:
                print(render_decomposition(report))
            return 1 if report["mode"] == "ENFORCED" and report["summary"]["not_releasable"] else 0
        if args.cmd == "health":
            planned = copy.deepcopy(graph)
            planned.setdefault("programme", {}).setdefault("health_policy", {})["mode"] = args.mode
            projected = project(
                planned,
                _load_ledger(args.facts),
                _load_structured(args.observations) if args.observations else {},
                topology_observations=(
                    _load_structured(args.topology_observations)
                    if args.topology_observations
                    else {}
                ),
            )
            if args.json:
                _emit(
                    {
                        "programme": projected["nodes"][projected["root"]].get("health"),
                        "leaves": {r: n["health"] for r, n in projected["nodes"].items() if n["kind"] == "LEAF" and n.get("health")},
                    },
                    None,
                )
            else:
                print(render_health(projected, args.leaf))
            return 0
        if args.cmd in {"frontier", "frontier-verify"}:
            if args.repository:
                require_repository_match(graph, args.repository, live=False)
                transport = GhTransport(args.repository)
                ledger, observations = ledger_from_github(transport, graph), observe_github(transport, graph)
                topology_observations = (
                    _load_structured(args.topology_observations)
                    if args.topology_observations
                    else observe_topology_repository(
                        graph,
                        args.repo_root,
                        expected_repository=args.repository,
                    )
                )
            else:
                ledger = _load_ledger(args.facts)
                observations = _load_structured(args.observations) if args.observations else {}
                topology_observations = (
                    _load_structured(args.topology_observations)
                    if args.topology_observations
                    else {}
                )
            live = frontier(
                graph,
                ledger,
                observations,
                args.leaf,
                topology_observations=topology_observations,
            )
            if args.cmd == "frontier":
                if args.text:
                    print(render_frontier(live))
                else:
                    _emit(live, args.output)
                return 0
            drift = frontier_drift(_load_structured(args.snapshot), live)
            if args.json:
                _emit(drift, None)
            else:
                print(render_frontier_drift(drift))
            return 2 if drift["status"] == "MOVED" else 0
        if args.cmd == "sync-github":
            require_repository_match(graph, args.repository, live=not args.dry_run)
        if args.cmd == "sync-github" and args.dry_run:
            _emit(plan_github(GhTransport(args.repository), graph, args.repo_root), None)
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
                topology_observation_provider=lambda: observe_topology_repository(
                    graph,
                    args.repo_root,
                    expected_repository=args.repository,
                ),
            )
            _emit(report, None)
            return 0
        ledger = _load_ledger(args.facts)
        observations = _load_structured(args.observations) if getattr(args, "observations", None) else {}
        topology_observations = (
            _load_structured(args.topology_observations)
            if getattr(args, "topology_observations", None)
            else {}
        )
        projection = project(
            graph,
            ledger,
            observations,
            topology_observations=topology_observations,
        )
        if args.cmd == "project":
            if args.base_titles:
                projection["expected_titles"] = expected_titles(projection, _load_structured(args.base_titles))
            _emit(projection, args.output)
            return 0
        if args.cmd == "admit":
            owner_intent = _load_structured(args.owner_intent) if args.owner_intent else None
            report = admit(projection, args.leaf, args.command, owner_intent)
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
