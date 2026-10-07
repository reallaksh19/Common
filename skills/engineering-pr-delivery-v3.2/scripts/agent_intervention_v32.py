#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
from fractions import Fraction
from pathlib import Path
from typing import Any, Mapping

INPUT_SCHEMA = "relay-v3.2-agent-intervention-input"
RESULT_SCHEMA = "relay-v3.2-agent-intervention-result"
M2_SCHEMA = "relay-v3.2-agent-quality-trajectory-result"
M2_AUTHORITY = "DERIVED_AGENT_QUALITY_TRAJECTORY_ONLY"
AUTHORITY = "DERIVED_AGENT_INTERVENTION_ADVISORY_ONLY"
POLICY_VERSION = "V3.2-M3-1"

_COMPONENTS = (
    "mutation_tpr",
    "clean_tnr",
    "balanced_accuracy",
    "critical_mutation_recall",
    "impact_coverage",
    "critical_unknown_rate",
    "repair_rate",
)
_DIRECTIONS = {"STABLE", "IMPROVING", "DEGRADING", "MIXED", "INSUFFICIENT_DATA"}
_DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")


class InterventionError(ValueError):
    pass


def _digest(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return "sha256:" + hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _positive_int(value: Any) -> bool:
    return not isinstance(value, bool) and isinstance(value, int) and value > 0


def _fraction(value: Any, label: str) -> Fraction | None:
    if value is None:
        return None
    if not isinstance(value, Mapping) or set(map(str, value)) != {"numerator", "denominator"}:
        raise InterventionError(f"{label}: exact numerator/denominator mapping or null required")
    numerator, denominator = value.get("numerator"), value.get("denominator")
    if isinstance(numerator, bool) or not isinstance(numerator, int) or numerator < 0:
        raise InterventionError(f"{label}.numerator: non-negative integer required")
    if not _positive_int(denominator):
        raise InterventionError(f"{label}.denominator: positive integer required")
    return Fraction(numerator, denominator)


def _fraction_dict(value: Fraction | None) -> dict[str, int] | None:
    if value is None:
        return None
    return {"numerator": value.numerator, "denominator": value.denominator}


def _normalize_component(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, Mapping) or set(map(str, value)) != {"direction", "first", "last"}:
        raise InterventionError(f"{label}: exact direction/first/last mapping required")
    direction = value.get("direction")
    if direction not in _DIRECTIONS:
        raise InterventionError(f"{label}.direction: invalid")
    first = _fraction(value.get("first"), f"{label}.first")
    last = _fraction(value.get("last"), f"{label}.last")
    if direction == "INSUFFICIENT_DATA":
        if first is not None and last is not None:
            raise InterventionError(f"{label}: INSUFFICIENT_DATA requires an unavailable boundary")
    elif first is None or last is None:
        raise InterventionError(f"{label}: observed direction requires first and last")
    return {"direction": direction, "first": _fraction_dict(first), "last": _fraction_dict(last)}


def _expected_trajectory(components: Mapping[str, Any]) -> tuple[str, str]:
    directions = {components[key]["direction"] for key in _COMPONENTS}
    if "MIXED" in directions:
        return "INSUFFICIENT_DATA", "MIXED_SIGNAL"
    if "INSUFFICIENT_DATA" in directions:
        return "INSUFFICIENT_DATA", "INCOMPLETE_SIGNAL"
    if "IMPROVING" in directions and "DEGRADING" in directions:
        return "INSUFFICIENT_DATA", "CONFLICTING_SIGNAL"
    if "IMPROVING" in directions:
        return "IMPROVING", "MONOTONIC_IMPROVEMENT"
    if "DEGRADING" in directions:
        return "DEGRADING", "MONOTONIC_DEGRADATION"
    return "STABLE", "ALL_COMPONENTS_STABLE"


def _normalize_m2(value: Any) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise InterventionError("trajectory: M2 result mapping required")
    allowed = {
        "schema", "authority", "trajectory_id", "comparison_basis", "input_digest",
        "trajectory_digest", "trajectory", "reason", "windows", "components", "authority_effects",
    }
    extra = set(map(str, value)) - allowed
    missing = allowed - set(map(str, value))
    if extra or missing:
        raise InterventionError(f"trajectory: exact M2 result fields required; missing={sorted(missing)} extra={sorted(extra)}")
    if value.get("schema") != M2_SCHEMA:
        raise InterventionError(f"trajectory.schema: expected {M2_SCHEMA}")
    if value.get("authority") != M2_AUTHORITY:
        raise InterventionError("trajectory.authority: exact M2 derived authority required")
    if value.get("authority_effects") != []:
        raise InterventionError("trajectory.authority_effects: must be empty")

    trajectory_id = value.get("trajectory_id")
    if not isinstance(trajectory_id, str) or not trajectory_id.strip():
        raise InterventionError("trajectory.trajectory_id: non-empty string required")
    for key in ("input_digest", "trajectory_digest"):
        if not _DIGEST.fullmatch(str(value.get(key) or "")):
            raise InterventionError(f"trajectory.{key}: sha256 digest required")

    basis = value.get("comparison_basis")
    if not isinstance(basis, Mapping) or set(map(str, basis)) != {"ref", "digest"}:
        raise InterventionError("trajectory.comparison_basis: exact ref/digest mapping required")
    basis_ref, basis_digest = basis.get("ref"), basis.get("digest")
    if not isinstance(basis_ref, str) or not basis_ref.strip() or not _DIGEST.fullmatch(str(basis_digest or "")):
        raise InterventionError("trajectory.comparison_basis: durable ref and sha256 digest required")

    windows = value.get("windows")
    if not isinstance(windows, list) or len(windows) < 2:
        raise InterventionError("trajectory.windows: at least two source windows required")
    normalized_windows = []
    sequences = []
    for index, row in enumerate(windows):
        label = f"trajectory.windows[{index}]"
        required = {"sequence", "window_id", "input_digest", "evidence_digest", "result_digest"}
        if not isinstance(row, Mapping) or set(map(str, row)) != required:
            raise InterventionError(f"{label}: exact source-window shape required")
        sequence = row.get("sequence")
        if not _positive_int(sequence):
            raise InterventionError(f"{label}.sequence: positive integer required")
        sequences.append(sequence)
        window_id = row.get("window_id")
        if not isinstance(window_id, str) or not window_id.strip():
            raise InterventionError(f"{label}.window_id: non-empty string required")
        for key in ("input_digest", "evidence_digest", "result_digest"):
            if not _DIGEST.fullmatch(str(row.get(key) or "")):
                raise InterventionError(f"{label}.{key}: sha256 digest required")
        normalized_windows.append({
            "sequence": sequence,
            "window_id": window_id.strip(),
            "input_digest": row["input_digest"],
            "evidence_digest": row["evidence_digest"],
            "result_digest": row["result_digest"],
        })
    if sequences != sorted(sequences) or len(sequences) != len(set(sequences)):
        raise InterventionError("trajectory.windows: sequences must be unique and ascending")

    components = value.get("components")
    if not isinstance(components, Mapping) or set(map(str, components)) != set(_COMPONENTS):
        raise InterventionError("trajectory.components: exact M2 component set required")
    normalized_components = {
        key: _normalize_component(components[key], f"trajectory.components.{key}") for key in _COMPONENTS
    }

    expected_trajectory, expected_reason = _expected_trajectory(normalized_components)
    if (value.get("trajectory"), value.get("reason")) != (expected_trajectory, expected_reason):
        raise InterventionError("trajectory: trajectory/reason inconsistent with component directions")

    normalized = {
        "schema": M2_SCHEMA,
        "authority": M2_AUTHORITY,
        "trajectory_id": trajectory_id.strip(),
        "comparison_basis": {"ref": basis_ref.strip(), "digest": basis_digest},
        "input_digest": value["input_digest"],
        "trajectory_digest": value["trajectory_digest"],
        "trajectory": expected_trajectory,
        "reason": expected_reason,
        "windows": normalized_windows,
        "components": normalized_components,
        "authority_effects": [],
    }
    digest_basis = {
        "trajectory_id": normalized["trajectory_id"],
        "comparison_basis": normalized["comparison_basis"],
        "input_digest": normalized["input_digest"],
        "trajectory": normalized["trajectory"],
        "reason": normalized["reason"],
        "windows": normalized["windows"],
        "components": normalized["components"],
    }
    if normalized["trajectory_digest"] != _digest(digest_basis):
        raise InterventionError("trajectory.trajectory_digest: does not match exact M2 result basis")
    return normalized


def normalize_input(source: Any) -> dict[str, Any]:
    if not isinstance(source, Mapping) or set(map(str, source)) != {"schema", "trajectory"}:
        raise InterventionError("input: exact schema/trajectory mapping required")
    if source.get("schema") != INPUT_SCHEMA:
        raise InterventionError(f"schema: expected {INPUT_SCHEMA}")
    return {"schema": INPUT_SCHEMA, "trajectory": _normalize_m2(source.get("trajectory"))}


def _last(component: Mapping[str, Any]) -> Fraction | None:
    value = component.get("last")
    if value is None:
        return None
    return Fraction(value["numerator"], value["denominator"])


def evaluate(source: Any) -> dict[str, Any]:
    normalized = normalize_input(source)
    trajectory = normalized["trajectory"]
    state, reason = trajectory["trajectory"], trajectory["reason"]
    critical_unknown = trajectory["components"]["critical_unknown_rate"]
    repair_rate = trajectory["components"]["repair_rate"]

    source_basis = [f"trajectory={state}", f"reason={reason}"]
    if state == "INSUFFICIENT_DATA" and reason == "INCOMPLETE_SIGNAL":
        recommendation, why = "REPLAY_REQUIRED", "EVIDENCE_INCOMPLETE"
    elif state == "INSUFFICIENT_DATA" and reason == "MIXED_SIGNAL":
        recommendation, why = "FRESH_SELF_REVIEW", "DIRECTION_REVERSAL"
    elif state == "INSUFFICIENT_DATA" and reason == "CONFLICTING_SIGNAL":
        recommendation, why = "CHECKPOINT", "COMPONENTS_CONFLICT"
    elif state == "DEGRADING" and (_last(critical_unknown) or Fraction(0, 1)) > 0:
        recommendation, why = "FRESH_RECONSTRUCTION", "DEGRADING_WITH_CRITICAL_UNCERTAINTY"
        source_basis.append(
            f"critical_unknown_rate.last={critical_unknown['last']['numerator']}/{critical_unknown['last']['denominator']}"
        )
    elif (
        state == "DEGRADING"
        and repair_rate["direction"] == "DEGRADING"
        and (_last(repair_rate) or Fraction(0, 1)) > 0
    ):
        recommendation, why = "SPLIT_REMAINDER", "DEGRADING_WITH_RISING_REPAIR_RATE"
        source_basis.extend([
            "repair_rate.direction=DEGRADING",
            f"repair_rate.last={repair_rate['last']['numerator']}/{repair_rate['last']['denominator']}",
        ])
    elif state == "DEGRADING":
        recommendation, why = "CHECKPOINT", "DEGRADING_CHECKPOINT"
    else:
        recommendation, why = "NONE", "STABLE_OR_IMPROVING"

    basis = {
        "policy_version": POLICY_VERSION,
        "source_trajectory_id": trajectory["trajectory_id"],
        "source_trajectory_digest": trajectory["trajectory_digest"],
        "comparison_basis": trajectory["comparison_basis"],
        "recommendation": recommendation,
        "reason": why,
        "source_basis": source_basis,
        "advisory_only": True,
        "authority_effects": [],
    }
    return {
        "schema": RESULT_SCHEMA,
        "authority": AUTHORITY,
        **basis,
        "recommendation_digest": _digest(basis),
    }


def _load(path: Path) -> Any:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        return json.loads(text)
    try:
        import yaml
    except ImportError as exc:
        raise InterventionError("PyYAML is required for non-JSON input") from exc
    return yaml.safe_load(text)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Derive a V3.2 advisory execution intervention from M2 trajectory evidence.")
    parser.add_argument("input", type=Path)
    args = parser.parse_args(argv)
    try:
        result = evaluate(_load(args.input))
    except (InterventionError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
