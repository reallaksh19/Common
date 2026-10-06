#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

from coordlib import load_yaml, validate as schema_validate


CLASSIFICATIONS = (
    "TRUE_CLEAR",
    "TRUE_BLOCK",
    "FALSE_CLEAR",
    "FALSE_BLOCK",
    "PROTECTIVE_ESCALATION",
    "CONSERVATIVE_ESCALATION",
    "PENDING_ADJUDICATION",
)

RELATIVE_OUTCOMES = (
    "SAME",
    "CAUGHT_INCUMBENT_MISS",
    "AVOIDED_INCUMBENT_FALSE_BLOCK",
    "DIVERGENT",
    "PENDING",
)


def derive_classification(observation: dict[str, Any]) -> str:
    gate = observation["gate_result"]["decision"]
    adjudication = observation["adjudication"]["state"]

    if adjudication == "UNKNOWN":
        return "PENDING_ADJUDICATION"

    if gate == "ADVANCE_ELIGIBLE":
        return "TRUE_CLEAR" if adjudication == "CORRECT" else "FALSE_CLEAR"

    if gate == "REPAIR":
        return "TRUE_BLOCK" if adjudication == "DEFECT" else "FALSE_BLOCK"

    if adjudication == "DEFECT":
        return "PROTECTIVE_ESCALATION"
    return "CONSERVATIVE_ESCALATION"


def derive_relative_outcome(observation: dict[str, Any]) -> str:
    gate = observation["gate_result"]["decision"]
    incumbent = observation["incumbent"]["decision"]
    adjudication = observation["adjudication"]["state"]

    if adjudication == "UNKNOWN" or incumbent == "UNKNOWN":
        return "PENDING"

    gate_advances = gate == "ADVANCE_ELIGIBLE"
    incumbent_advances = incumbent == "ADVANCE"

    if incumbent_advances and not gate_advances and adjudication == "DEFECT":
        return "CAUGHT_INCUMBENT_MISS"

    if not incumbent_advances and gate_advances and adjudication == "CORRECT":
        return "AVOIDED_INCUMBENT_FALSE_BLOCK"

    if gate_advances == incumbent_advances:
        return "SAME"

    return "DIVERGENT"


def semantic_errors(observation: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    adjudication = observation["adjudication"]

    if adjudication["state"] == "DEFECT":
        if adjudication["severity"] is None:
            errors.append("DEFECT adjudication requires severity")
        if not adjudication["evidence_refs"]:
            errors.append("DEFECT adjudication requires evidence_refs")
    else:
        if adjudication["severity"] is not None:
            errors.append(
                f"{adjudication['state']} adjudication requires severity=null"
            )

    expected_classification = derive_classification(observation)
    if observation["classification"] != expected_classification:
        errors.append(
            "classification "
            f"{observation['classification']} does not match derived "
            f"{expected_classification}"
        )

    expected_relative = derive_relative_outcome(observation)
    if observation["relative_outcome"] != expected_relative:
        errors.append(
            "relative_outcome "
            f"{observation['relative_outcome']} does not match derived "
            f"{expected_relative}"
        )

    return errors


def validate_observation(
    observation: Any,
    label: str = "shadow-observation",
) -> list[str]:
    errors = schema_validate("shadow-observation", observation, label)
    if errors:
        return errors
    return [f"{label}: {error}" for error in semantic_errors(observation)]


def summarize(observations: list[dict[str, Any]]) -> dict[str, Any]:
    errors: list[str] = []
    for index, observation in enumerate(observations):
        errors.extend(validate_observation(observation, f"observation[{index}]"))
    if errors:
        raise ValueError("; ".join(errors))

    counts = Counter(observation["classification"] for observation in observations)
    relative = Counter(observation["relative_outcome"] for observation in observations)

    return {
        "schema_version": "SHADOW_SUMMARY_V1",
        "authority": "NON_BLOCKING_SHADOW_SUMMARY",
        "production_effect": "NONE",
        "sample_count": len(observations),
        "adjudicated_count": sum(
            observation["adjudication"]["state"] != "UNKNOWN"
            for observation in observations
        ),
        "counts": {
            key: counts.get(key, 0)
            for key in CLASSIFICATIONS
        },
        "relative_counts": {
            key: relative.get(key, 0)
            for key in RELATIVE_OUTCOMES
        },
        "candidate_refs": [
            observation["candidate_sha"]
            for observation in observations
        ],
    }


def validate_summary(
    summary: Any,
    label: str = "shadow-summary",
) -> list[str]:
    errors = schema_validate("shadow-summary", summary, label)
    if errors:
        return errors

    if summary["adjudicated_count"] > summary["sample_count"]:
        return [
            f"{label}: adjudicated_count cannot exceed sample_count"
        ]

    if sum(summary["counts"].values()) != summary["sample_count"]:
        return [
            f"{label}: classification counts must equal sample_count"
        ]

    if sum(summary["relative_counts"].values()) != summary["sample_count"]:
        return [
            f"{label}: relative counts must equal sample_count"
        ]

    if len(summary["candidate_refs"]) != summary["sample_count"]:
        return [
            f"{label}: candidate_refs length must equal sample_count"
        ]

    return []


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate and summarize non-blocking production shadow observations."
    )
    parser.add_argument("observations", nargs="+")
    args = parser.parse_args()

    observations = [
        load_yaml(Path(path))
        for path in args.observations
    ]
    summary = summarize(observations)
    errors = validate_summary(summary)
    if errors:
        for error in errors:
            print(error)
        raise SystemExit(1)

    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
