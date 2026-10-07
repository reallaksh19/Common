#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
from fractions import Fraction
from pathlib import Path
from typing import Any, Mapping

M1_SCHEMA = "relay-v3.2-agent-quality-result"
M1_AUTHORITY = "DERIVED_AGENT_QUALITY_OBSERVATION_ONLY"
INPUT_SCHEMA = "relay-v3.2-agent-quality-trajectory-input"
RESULT_SCHEMA = "relay-v3.2-agent-quality-trajectory-result"
AUTHORITY = "DERIVED_AGENT_QUALITY_TRAJECTORY_ONLY"

_RATIO_KEYS = (
    "mutation_tpr",
    "clean_tnr",
    "balanced_accuracy",
    "critical_mutation_recall",
    "impact_coverage",
)
_COMPONENTS = _RATIO_KEYS + ("critical_unknown_rate", "repair_rate")
_DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")


class TrajectoryError(ValueError):
    pass


def _digest(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return "sha256:" + hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _positive_int(value: Any) -> bool:
    return not isinstance(value, bool) and isinstance(value, int) and value > 0


def _nonnegative_int(value: Any) -> bool:
    return not isinstance(value, bool) and isinstance(value, int) and value >= 0


def _fraction_dict(value: Fraction | None) -> dict[str, int] | None:
    if value is None:
        return None
    return {"numerator": value.numerator, "denominator": value.denominator}


def _parse_ratio(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, Mapping) or set(map(str, value)) != {"state", "numerator", "denominator", "value"}:
        raise TrajectoryError(f"{label}: exact ratio shape required")
    state = value.get("state")
    numerator = value.get("numerator")
    denominator = value.get("denominator")
    rendered = value.get("value")
    if state == "UNKNOWN":
        if numerator != 0 or denominator != 0 or rendered is not None:
            raise TrajectoryError(f"{label}: UNKNOWN must be 0/0 with null value")
        return {"state": "UNKNOWN", "numerator": 0, "denominator": 0, "value": None}
    if state != "OBSERVED":
        raise TrajectoryError(f"{label}.state: OBSERVED or UNKNOWN required")
    if not _nonnegative_int(numerator) or not _positive_int(denominator) or numerator > denominator:
        raise TrajectoryError(f"{label}: observed ratio requires 0 <= numerator <= denominator")
    exact = Fraction(numerator, denominator)
    if isinstance(rendered, bool) or not isinstance(rendered, (int, float)):
        raise TrajectoryError(f"{label}.value: numeric value required for OBSERVED")
    if abs(float(exact) - float(rendered)) > 1e-12:
        raise TrajectoryError(f"{label}.value: inconsistent with numerator/denominator")
    return {
        "state": "OBSERVED",
        "numerator": exact.numerator,
        "denominator": exact.denominator,
        "value": float(exact),
    }


def _normalize_m1(result: Any, label: str) -> dict[str, Any]:
    if not isinstance(result, Mapping):
        raise TrajectoryError(f"{label}: M1 result mapping required")
    allowed = {
        "schema", "authority", "window_id", "input_digest", "evidence_digest",
        "observation_count", "unknown_observation_count", "metrics", "evidence_refs",
        "authority_effects",
    }
    extra = set(map(str, result)) - allowed
    if extra:
        raise TrajectoryError(f"{label}: unknown fields {sorted(extra)}")
    if result.get("schema") != M1_SCHEMA:
        raise TrajectoryError(f"{label}.schema: expected {M1_SCHEMA}")
    if result.get("authority") != M1_AUTHORITY:
        raise TrajectoryError(f"{label}.authority: exact M1 derived authority required")
    window_id = result.get("window_id")
    if not isinstance(window_id, str) or not window_id.strip():
        raise TrajectoryError(f"{label}.window_id: non-empty string required")
    for key in ("input_digest", "evidence_digest"):
        if not _DIGEST.fullmatch(str(result.get(key) or "")):
            raise TrajectoryError(f"{label}.{key}: sha256 digest required")
    count = result.get("observation_count")
    unknown = result.get("unknown_observation_count")
    if not _positive_int(count):
        raise TrajectoryError(f"{label}.observation_count: positive integer required")
    if not _nonnegative_int(unknown) or unknown > count:
        raise TrajectoryError(f"{label}.unknown_observation_count: must be within observation_count")

    metrics = result.get("metrics")
    expected_metrics = set(_RATIO_KEYS) | {"critical_unknown_count", "repair_count"}
    if not isinstance(metrics, Mapping) or set(map(str, metrics)) != expected_metrics:
        raise TrajectoryError(f"{label}.metrics: exact M1 metric set required")
    normalized_metrics = {key: _parse_ratio(metrics[key], f"{label}.metrics.{key}") for key in _RATIO_KEYS}
    for key in ("critical_unknown_count", "repair_count"):
        value = metrics.get(key)
        if not _nonnegative_int(value):
            raise TrajectoryError(f"{label}.metrics.{key}: non-negative integer required")
        if key == "critical_unknown_count" and value > count:
            raise TrajectoryError(f"{label}.metrics.{key}: cannot exceed observation_count")
        normalized_metrics[key] = value

    refs = result.get("evidence_refs")
    if not isinstance(refs, list) or not refs or not all(isinstance(x, str) and x.strip() for x in refs):
        raise TrajectoryError(f"{label}.evidence_refs: non-empty string list required")
    if len(refs) != len(set(refs)):
        raise TrajectoryError(f"{label}.evidence_refs: duplicates are not allowed")
    if result.get("authority_effects") != []:
        raise TrajectoryError(f"{label}.authority_effects: must be empty")

    return {
        "schema": M1_SCHEMA,
        "authority": M1_AUTHORITY,
        "window_id": window_id.strip(),
        "input_digest": result["input_digest"],
        "evidence_digest": result["evidence_digest"],
        "observation_count": count,
        "unknown_observation_count": unknown,
        "metrics": normalized_metrics,
        "evidence_refs": sorted(refs),
        "authority_effects": [],
    }


def normalize_input(source: Any) -> dict[str, Any]:
    if not isinstance(source, Mapping):
        raise TrajectoryError("trajectory input: mapping required")
    if set(map(str, source)) != {"schema", "trajectory_id", "windows"}:
        raise TrajectoryError("trajectory input: exact schema/trajectory_id/windows fields required")
    if source.get("schema") != INPUT_SCHEMA:
        raise TrajectoryError(f"schema: expected {INPUT_SCHEMA}")
    trajectory_id = source.get("trajectory_id")
    if not isinstance(trajectory_id, str) or not trajectory_id.strip():
        raise TrajectoryError("trajectory_id: non-empty string required")
    windows = source.get("windows")
    if not isinstance(windows, list) or len(windows) < 2:
        raise TrajectoryError("windows: at least two M1 results required")

    normalized = []
    for index, row in enumerate(windows):
        label = f"windows[{index}]"
        if not isinstance(row, Mapping) or set(map(str, row)) != {"sequence", "result"}:
            raise TrajectoryError(f"{label}: exact sequence/result mapping required")
        sequence = row.get("sequence")
        if not _positive_int(sequence):
            raise TrajectoryError(f"{label}.sequence: positive integer required")
        normalized.append({"sequence": sequence, "result": _normalize_m1(row.get("result"), f"{label}.result")})

    sequences = [row["sequence"] for row in normalized]
    window_ids = [row["result"]["window_id"] for row in normalized]
    if len(sequences) != len(set(sequences)):
        raise TrajectoryError("windows: duplicate sequence")
    if len(window_ids) != len(set(window_ids)):
        raise TrajectoryError("windows: duplicate M1 window_id")
    normalized.sort(key=lambda row: row["sequence"])
    return {"schema": INPUT_SCHEMA, "trajectory_id": trajectory_id.strip(), "windows": normalized}


def _series(normalized: Mapping[str, Any], component: str) -> list[Fraction | None]:
    values: list[Fraction | None] = []
    for row in normalized["windows"]:
        result = row["result"]
        if component in _RATIO_KEYS:
            metric = result["metrics"][component]
            values.append(
                None if metric["state"] == "UNKNOWN"
                else Fraction(metric["numerator"], metric["denominator"])
            )
        elif component == "critical_unknown_rate":
            values.append(Fraction(result["metrics"]["critical_unknown_count"], result["observation_count"]))
        elif component == "repair_rate":
            values.append(Fraction(result["metrics"]["repair_count"], result["observation_count"]))
        else:
            raise TrajectoryError(f"unknown component {component}")
    return values


def _direction(values: list[Fraction | None], *, higher_is_better: bool) -> dict[str, Any]:
    observed = [value for value in values if value is not None]
    first = values[0]
    last = values[-1]
    if len(observed) != len(values):
        return {"direction": "INSUFFICIENT_DATA", "first": _fraction_dict(first), "last": _fraction_dict(last)}
    if all(value == values[0] for value in values[1:]):
        direction = "STABLE"
    else:
        nondecreasing = all(after >= before for before, after in zip(values, values[1:]))
        nonincreasing = all(after <= before for before, after in zip(values, values[1:]))
        if nondecreasing:
            direction = "IMPROVING" if higher_is_better else "DEGRADING"
        elif nonincreasing:
            direction = "DEGRADING" if higher_is_better else "IMPROVING"
        else:
            direction = "MIXED"
    return {"direction": direction, "first": _fraction_dict(first), "last": _fraction_dict(last)}


def evaluate(source: Any) -> dict[str, Any]:
    normalized = normalize_input(source)
    components = {}
    for component in _COMPONENTS:
        components[component] = _direction(
            _series(normalized, component),
            higher_is_better=component not in {"critical_unknown_rate", "repair_rate"},
        )

    directions = {row["direction"] for row in components.values()}
    if "MIXED" in directions:
        trajectory, reason = "INSUFFICIENT_DATA", "MIXED_SIGNAL"
    elif "INSUFFICIENT_DATA" in directions:
        trajectory, reason = "INSUFFICIENT_DATA", "INCOMPLETE_SIGNAL"
    elif "IMPROVING" in directions and "DEGRADING" in directions:
        trajectory, reason = "INSUFFICIENT_DATA", "CONFLICTING_SIGNAL"
    elif "IMPROVING" in directions:
        trajectory, reason = "IMPROVING", "MONOTONIC_IMPROVEMENT"
    elif "DEGRADING" in directions:
        trajectory, reason = "DEGRADING", "MONOTONIC_DEGRADATION"
    else:
        trajectory, reason = "STABLE", "ALL_COMPONENTS_STABLE"

    windows = [
        {
            "sequence": row["sequence"],
            "window_id": row["result"]["window_id"],
            "input_digest": row["result"]["input_digest"],
            "evidence_digest": row["result"]["evidence_digest"],
            "result_digest": _digest(row["result"]),
        }
        for row in normalized["windows"]
    ]
    input_digest = _digest(normalized)
    trajectory_basis = {
        "trajectory_id": normalized["trajectory_id"],
        "input_digest": input_digest,
        "trajectory": trajectory,
        "reason": reason,
        "windows": windows,
        "components": components,
    }
    return {
        "schema": RESULT_SCHEMA,
        "authority": AUTHORITY,
        "trajectory_id": normalized["trajectory_id"],
        "input_digest": input_digest,
        "trajectory_digest": _digest(trajectory_basis),
        "trajectory": trajectory,
        "reason": reason,
        "windows": windows,
        "components": components,
        "authority_effects": [],
    }


def _load(path: Path) -> Any:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        return json.loads(text)
    try:
        import yaml
    except ImportError as exc:
        raise TrajectoryError("PyYAML is required for non-JSON input") from exc
    return yaml.safe_load(text)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Derive a threshold-free V3.2 agent-quality trajectory.")
    parser.add_argument("input", type=Path)
    args = parser.parse_args(argv)
    try:
        result = evaluate(_load(args.input))
    except (TrajectoryError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
