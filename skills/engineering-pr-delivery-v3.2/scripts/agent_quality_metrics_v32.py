#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any, Mapping

AUTHORITY = "DERIVED_AGENT_QUALITY_OBSERVATION_ONLY"
WINDOW_SCHEMA = "relay-v3.2-agent-quality-window"
RESULT_SCHEMA = "relay-v3.2-agent-quality-result"

_ALLOWED_BY_CLASS = {
    "MUTATION": {"DETECTED", "MISSED", "UNKNOWN"},
    "CLEAN_CONTROL": {"CLEAN_ACCEPTED", "FALSE_POSITIVE", "UNKNOWN"},
}


class MetricError(ValueError):
    pass


def _digest(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return "sha256:" + hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _ratio(numerator: int, denominator: int) -> dict[str, Any]:
    if denominator == 0:
        return {"state": "UNKNOWN", "numerator": 0, "denominator": 0, "value": None}
    value = Fraction(numerator, denominator)
    return {
        "state": "OBSERVED",
        "numerator": value.numerator,
        "denominator": value.denominator,
        "value": float(value),
    }


def _fraction_metric(value: Fraction | None) -> dict[str, Any]:
    if value is None:
        return {"state": "UNKNOWN", "numerator": 0, "denominator": 0, "value": None}
    return {
        "state": "OBSERVED",
        "numerator": value.numerator,
        "denominator": value.denominator,
        "value": float(value),
    }


def _validate_row(row: Any, index: int) -> dict[str, Any]:
    label = f"observations[{index}]"
    if not isinstance(row, Mapping):
        raise MetricError(f"{label}: mapping required")
    allowed = {
        "id", "class", "critical", "disposition", "impact_expected",
        "impact_covered", "repairs", "evidence_refs",
    }
    extra = set(map(str, row)) - allowed
    if extra:
        raise MetricError(f"{label}: unknown fields {sorted(extra)}")

    oid = row.get("id")
    kind = row.get("class")
    critical = row.get("critical")
    disposition = row.get("disposition")
    repairs = row.get("repairs")
    refs = row.get("evidence_refs")

    if not isinstance(oid, str) or not oid.strip():
        raise MetricError(f"{label}.id: non-empty string required")
    if kind not in _ALLOWED_BY_CLASS:
        raise MetricError(f"{label}.class: MUTATION or CLEAN_CONTROL required")
    if not isinstance(critical, bool):
        raise MetricError(f"{label}.critical: boolean required")
    if disposition not in _ALLOWED_BY_CLASS[kind]:
        raise MetricError(f"{label}.disposition: invalid for {kind}")
    if isinstance(repairs, bool) or not isinstance(repairs, int) or repairs < 0:
        raise MetricError(f"{label}.repairs: non-negative integer required")
    if not isinstance(refs, list) or not refs or not all(isinstance(x, str) and x.strip() for x in refs):
        raise MetricError(f"{label}.evidence_refs: non-empty string list required")
    if len(refs) != len(set(refs)):
        raise MetricError(f"{label}.evidence_refs: duplicates are not allowed")

    expected = row.get("impact_expected")
    covered = row.get("impact_covered")
    if kind == "CLEAN_CONTROL" and (expected is not None or covered is not None):
        raise MetricError(f"{label}: clean controls cannot carry impact coverage")
    if expected is not None and (isinstance(expected, bool) or not isinstance(expected, int) or expected < 1):
        raise MetricError(f"{label}.impact_expected: positive integer or null required")
    if covered is not None and (isinstance(covered, bool) or not isinstance(covered, int) or covered < 0):
        raise MetricError(f"{label}.impact_covered: non-negative integer or null required")
    if covered is not None and expected is None:
        raise MetricError(f"{label}.impact_covered: impact_expected required when covered is set")
    if expected is not None and covered is None:
        raise MetricError(f"{label}.impact_covered: required when impact_expected is set")
    if expected is not None and covered > expected:
        raise MetricError(f"{label}: impact_covered cannot exceed impact_expected")

    return {
        "id": oid.strip(),
        "class": kind,
        "critical": critical,
        "disposition": disposition,
        "impact_expected": expected,
        "impact_covered": covered,
        "repairs": repairs,
        "evidence_refs": sorted(refs),
    }


def normalize_window(window: Any) -> dict[str, Any]:
    if not isinstance(window, Mapping):
        raise MetricError("window: mapping required")
    extra = set(map(str, window)) - {"schema", "window_id", "observations"}
    if extra:
        raise MetricError(f"window: unknown fields {sorted(extra)}")
    if window.get("schema") != WINDOW_SCHEMA:
        raise MetricError(f"schema: expected {WINDOW_SCHEMA}")
    window_id = window.get("window_id")
    if not isinstance(window_id, str) or not window_id.strip():
        raise MetricError("window_id: non-empty string required")
    observations = window.get("observations")
    if not isinstance(observations, list) or not observations:
        raise MetricError("observations: non-empty array required")

    rows = [_validate_row(row, i) for i, row in enumerate(observations)]
    ids = [row["id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise MetricError("observations: duplicate id")
    rows.sort(key=lambda row: row["id"])
    return {"schema": WINDOW_SCHEMA, "window_id": window_id.strip(), "observations": rows}


def evaluate(window: Any) -> dict[str, Any]:
    normalized = normalize_window(window)
    rows = normalized["observations"]

    mutation = [r for r in rows if r["class"] == "MUTATION"]
    clean = [r for r in rows if r["class"] == "CLEAN_CONTROL"]
    mutation_observed = [r for r in mutation if r["disposition"] != "UNKNOWN"]
    clean_observed = [r for r in clean if r["disposition"] != "UNKNOWN"]
    critical_mutation = [r for r in mutation if r["critical"]]
    critical_observed = [r for r in critical_mutation if r["disposition"] != "UNKNOWN"]

    tpr = _ratio(sum(r["disposition"] == "DETECTED" for r in mutation_observed), len(mutation_observed))
    tnr = _ratio(sum(r["disposition"] == "CLEAN_ACCEPTED" for r in clean_observed), len(clean_observed))
    critical_recall = _ratio(
        sum(r["disposition"] == "DETECTED" for r in critical_observed),
        len(critical_observed),
    )

    balanced = None
    if tpr["state"] == "OBSERVED" and tnr["state"] == "OBSERVED":
        balanced = (
            Fraction(tpr["numerator"], tpr["denominator"])
            + Fraction(tnr["numerator"], tnr["denominator"])
        ) / 2

    impact_rows = [r for r in mutation if r["impact_expected"] is not None]
    impact = _ratio(
        sum(r["impact_covered"] for r in impact_rows),
        sum(r["impact_expected"] for r in impact_rows),
    )

    evidence_refs = sorted({ref for row in rows for ref in row["evidence_refs"]})
    return {
        "schema": RESULT_SCHEMA,
        "authority": AUTHORITY,
        "window_id": normalized["window_id"],
        "input_digest": _digest(normalized),
        "evidence_digest": _digest(evidence_refs),
        "observation_count": len(rows),
        "unknown_observation_count": sum(r["disposition"] == "UNKNOWN" for r in rows),
        "metrics": {
            "mutation_tpr": tpr,
            "clean_tnr": tnr,
            "balanced_accuracy": _fraction_metric(balanced),
            "critical_mutation_recall": critical_recall,
            "impact_coverage": impact,
            "critical_unknown_count": sum(
                r["critical"] and r["disposition"] == "UNKNOWN" for r in rows
            ),
            "repair_count": sum(r["repairs"] for r in rows),
        },
        "evidence_refs": evidence_refs,
        "authority_effects": [],
    }


def _load(path: Path) -> Any:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        return json.loads(text)
    try:
        import yaml
    except ImportError as exc:
        raise MetricError("PyYAML is required for non-JSON input") from exc
    return yaml.safe_load(text)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Derive V3.2 agent/reviewer quality metrics.")
    parser.add_argument("input", type=Path)
    args = parser.parse_args(argv)
    try:
        result = evaluate(_load(args.input))
    except (MetricError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
