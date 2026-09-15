#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable

from jsonschema import Draft202012Validator

from compile_mathematics_engineering_workbench import digest as engineering_digest, load as load_engineering
from validate_mathematics_engineering_gates import validate as validate_engineering_registry

ROOT = Path(__file__).resolve().parents[1]
MATH = ROOT.parent
SCHEMA = ROOT / "contracts" / "math-assessment-engineering-crosswalk.schema.json"
DEFAULT_CROSSWALK = ROOT / "policies" / "math-assessment-engineering-crosswalk.mixed-grade9.v1.json"
DEFAULT_ASSESSMENT_AUTHORITY = MATH / "AssessmentScope" / "authority" / "math-assessment-scope-authority.json"


class MathematicsAssessmentEngineeringCrosswalkError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(f"[{code}] {message}")
        self.code = code
        self.message = message


def load(path: str | Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _schema_validate(doc: dict) -> None:
    schema = load(SCHEMA)
    errors = sorted(Draft202012Validator(schema).iter_errors(doc), key=lambda e: list(e.path))
    if errors:
        e = errors[0]
        raise MathematicsAssessmentEngineeringCrosswalkError(
            "MATH_ENG_CROSSWALK_SCHEMA",
            f"{e.message}; path={list(e.path)}",
        )


def validate(
    crosswalk: dict,
    *,
    assessment_authority: dict | None = None,
    engineering_registry: dict | None = None,
) -> dict:
    """Validate an exact-ID custody bridge; never infer a mapping from prose or titles."""
    _schema_validate(crosswalk)
    assessment_authority = assessment_authority or load(DEFAULT_ASSESSMENT_AUTHORITY)
    engineering_registry = engineering_registry or load_engineering("policies/mathematics-technical-engineering-gates.v1.json")
    validate_engineering_registry(engineering_registry)

    if crosswalk["assessment_scope_authority_id"] != assessment_authority.get("authority_id"):
        raise MathematicsAssessmentEngineeringCrosswalkError(
            "MATH_ENG_CROSSWALK_ASSESSMENT_AUTHORITY_ID_DRIFT",
            str(assessment_authority.get("authority_id")),
        )
    if crosswalk["assessment_scope_authority_digest"] != assessment_authority.get("authority_digest"):
        raise MathematicsAssessmentEngineeringCrosswalkError(
            "MATH_ENG_CROSSWALK_ASSESSMENT_AUTHORITY_DIGEST_DRIFT",
            str(assessment_authority.get("authority_digest")),
        )
    if crosswalk["engineering_registry_id"] != engineering_registry.get("registry_id"):
        raise MathematicsAssessmentEngineeringCrosswalkError(
            "MATH_ENG_CROSSWALK_ENGINEERING_REGISTRY_ID_DRIFT",
            str(engineering_registry.get("registry_id")),
        )
    current_engineering_digest = engineering_digest(engineering_registry)
    if crosswalk["engineering_registry_digest"] != current_engineering_digest:
        raise MathematicsAssessmentEngineeringCrosswalkError(
            "MATH_ENG_CROSSWALK_ENGINEERING_REGISTRY_DIGEST_DRIFT",
            current_engineering_digest,
        )

    capability_index = {row["capability_id"]: row for row in assessment_authority.get("capabilities", [])}
    gate_index = {row["subtopic_id"]: row for row in engineering_registry.get("subtopic_gates", [])}
    rows = crosswalk["rows"]
    refs = [row["capability_ref"] for row in rows]
    if len(refs) != len(set(refs)):
        raise MathematicsAssessmentEngineeringCrosswalkError(
            "MATH_ENG_CROSSWALK_DUPLICATE_CAPABILITY",
            "duplicate capability_ref",
        )
    declared = set(crosswalk["coverage_scope_capability_refs"])
    row_refs = set(refs)
    if declared != row_refs:
        raise MathematicsAssessmentEngineeringCrosswalkError(
            "MATH_ENG_CROSSWALK_SCOPE_ROW_MISMATCH",
            f"missing={sorted(declared-row_refs)}, stale={sorted(row_refs-declared)}",
        )

    covered = []
    gaps = []
    gate_ids = set()
    for row in rows:
        cap = row["capability_ref"]
        if cap not in capability_index:
            raise MathematicsAssessmentEngineeringCrosswalkError(
                "MATH_ENG_CROSSWALK_UNKNOWN_ASSESSMENT_CAPABILITY",
                cap,
            )
        if row["status"] == "ENGINEERING_GAP":
            gaps.append({
                "capability_ref": cap,
                "gap_code": row["gap_code"],
                "gap_reason": row["gap_reason"],
            })
            continue
        for gate_id in row["engineering_gate_ids"]:
            gate = gate_index.get(gate_id)
            if gate is None:
                raise MathematicsAssessmentEngineeringCrosswalkError(
                    "MATH_ENG_CROSSWALK_UNKNOWN_ENGINEERING_GATE",
                    f"{cap}:{gate_id}",
                )
            if gate.get("technical_readiness") != "ENGINEERING_GATE_READY" or gate.get("maturity") != "ENGINEERING":
                raise MathematicsAssessmentEngineeringCrosswalkError(
                    "MATH_ENG_CROSSWALK_ENGINEERING_GATE_NOT_READY",
                    f"{cap}:{gate_id}",
                )
            gate_ids.add(gate_id)
        covered.append(cap)

    return {
        "status": "PASS",
        "crosswalk_id": crosswalk["crosswalk_id"],
        "coverage_scope": crosswalk["coverage_scope"],
        "capability_count": len(rows),
        "covered_capability_count": len(covered),
        "engineering_gap_count": len(gaps),
        "engineering_gaps": gaps,
        "engineering_gate_ids": sorted(gate_ids),
        "assessment_scope_authority_id": crosswalk["assessment_scope_authority_id"],
        "assessment_scope_authority_digest": crosswalk["assessment_scope_authority_digest"],
        "engineering_registry_id": crosswalk["engineering_registry_id"],
        "engineering_registry_digest": current_engineering_digest,
    }


def resolve_capability_gates(
    crosswalk: dict,
    required_capability_refs: Iterable[str],
    *,
    assessment_authority: dict | None = None,
    engineering_registry: dict | None = None,
    fail_on_gap: bool = True,
) -> dict:
    result = validate(
        crosswalk,
        assessment_authority=assessment_authority,
        engineering_registry=engineering_registry,
    )
    rows = {row["capability_ref"]: row for row in crosswalk["rows"]}
    required = sorted(set(str(x) for x in required_capability_refs if str(x).strip()))
    outside = [cap for cap in required if cap not in rows]
    if outside:
        raise MathematicsAssessmentEngineeringCrosswalkError(
            "MATH_ENG_CROSSWALK_REQUIRED_CAPABILITY_OUTSIDE_SCOPE",
            ",".join(outside),
        )
    gaps = [rows[cap] for cap in required if rows[cap]["status"] == "ENGINEERING_GAP"]
    if gaps and fail_on_gap:
        detail = ";".join(f"{row['capability_ref']}:{row['gap_code']}" for row in gaps)
        raise MathematicsAssessmentEngineeringCrosswalkError(
            "MATH_ENG_CROSSWALK_REQUIRED_CAPABILITY_GAP",
            detail,
        )
    by_capability = {
        cap: list(rows[cap]["engineering_gate_ids"])
        for cap in required
        if rows[cap]["status"] == "COVERED"
    }
    return {
        **result,
        "required_capability_refs": required,
        "required_engineering_gaps": [
            {"capability_ref": row["capability_ref"], "gap_code": row["gap_code"], "gap_reason": row["gap_reason"]}
            for row in gaps
        ],
        "capability_gate_map": by_capability,
        "required_engineering_gate_ids": sorted({gate for gates in by_capability.values() for gate in gates}),
        "required_status": "BLOCKED_ENGINEERING_GAP" if gaps else "COVERED",
    }


def resolve_bucket_gate_map(
    crosswalk: dict,
    bucket_plan: dict,
    *,
    assessment_authority: dict | None = None,
    engineering_registry: dict | None = None,
    fail_on_gap: bool = True,
) -> dict:
    required = sorted({cap for bucket in bucket_plan.get("buckets", []) for cap in bucket.get("member_capability_refs", [])})
    resolved = resolve_capability_gates(
        crosswalk,
        required,
        assessment_authority=assessment_authority,
        engineering_registry=engineering_registry,
        fail_on_gap=fail_on_gap,
    )
    cap_map = resolved["capability_gate_map"]
    gap_caps = {row["capability_ref"] for row in resolved["required_engineering_gaps"]}
    bucket_rows = []
    for bucket in bucket_plan.get("buckets", []):
        caps = list(bucket.get("member_capability_refs", []))
        bucket_rows.append({
            "bucket_id": bucket["bucket_id"],
            "capability_refs": caps,
            "engineering_gate_ids": sorted({gate for cap in caps for gate in cap_map.get(cap, [])}),
            "engineering_gap_capability_refs": sorted(set(caps) & gap_caps),
        })
    return {**resolved, "bucket_gate_map": bucket_rows}


def main() -> None:
    ap = argparse.ArgumentParser(description="Validate exact Mathematics AssessmentScope to Engineering Gate crosswalk")
    ap.add_argument("--crosswalk", default=str(DEFAULT_CROSSWALK))
    args = ap.parse_args()
    print(json.dumps(validate(load(args.crosswalk)), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
