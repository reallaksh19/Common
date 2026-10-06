#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from coordlib import load_yaml, validate as schema_validate


LAYERS = ("l0", "l1", "l2")


def obligation_rows(manifest: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
    rows: list[tuple[str, dict[str, Any]]] = []
    for layer in LAYERS:
        for obligation in manifest[layer]["obligations"]:
            rows.append((layer.upper(), obligation))
    return rows


def manifest_semantic_errors(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    basis = manifest["basis"]
    l1 = manifest["l1"]
    l2 = manifest["l2"]

    if l1["baseline_sha"] != basis["base_sha"]:
        errors.append("l1.baseline_sha must equal basis.base_sha")

    candidate_sha = basis["candidate_sha"]
    if candidate_sha is None:
        if l2["candidate_sha"] is not None:
            errors.append("l2.candidate_sha must be null before a candidate exists")
        if l2["obligations"]:
            errors.append("l2 obligations cannot exist before a candidate exists")
        if l2["impact_ref"] is not None:
            errors.append("l2.impact_ref must be null before a candidate exists")
    else:
        if l2["candidate_sha"] != candidate_sha:
            errors.append("l2.candidate_sha must equal basis.candidate_sha")
        if l2["obligations"] and not l2["impact_ref"]:
            errors.append("l2 obligations require an impact_ref")

    ids: list[str] = []
    requirement_ids: list[str] = []
    for layer, obligation in obligation_rows(manifest):
        oid = obligation["id"]
        ids.append(oid)

        if obligation["severity"] == "CRITICAL" and not obligation["evidence_required"]:
            errors.append(
                f"{layer}.{oid}: CRITICAL obligation requires evidence_required"
            )

        local_requirement_ids = [
            requirement["id"] for requirement in obligation["evidence_required"]
        ]
        if len(local_requirement_ids) != len(set(local_requirement_ids)):
            errors.append(
                f"{layer}.{oid}: duplicate evidence requirement id within obligation"
            )
        requirement_ids.extend(local_requirement_ids)

    duplicate_ids = sorted({oid for oid in ids if ids.count(oid) > 1})
    if duplicate_ids:
        errors.append(
            "obligation ids must be globally unique: " + ", ".join(duplicate_ids)
        )

    duplicate_requirement_ids = sorted({
        rid for rid in requirement_ids if requirement_ids.count(rid) > 1
    })
    if duplicate_requirement_ids:
        errors.append(
            "evidence requirement ids must be globally unique: "
            + ", ".join(duplicate_requirement_ids)
        )

    return errors


def ledger_semantic_errors(ledger: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    candidate_sha = ledger["candidate_sha"]
    ids = [record["obligation_id"] for record in ledger["records"]]
    duplicates = sorted({oid for oid in ids if ids.count(oid) > 1})
    if duplicates:
        errors.append(
            "ledger obligation ids must be unique: " + ", ".join(duplicates)
        )

    for record in ledger["records"]:
        oid = record["obligation_id"]
        state = record["state"]

        if record["evidence_candidate_sha"] != candidate_sha:
            errors.append(
                f"{oid}: evidence_candidate_sha must equal ledger candidate_sha"
            )

        if state in {"VERIFIED", "REFUTED"} and not record["evidence_items"]:
            errors.append(f"{oid}: {state} requires evidence_items")

        if state == "NOT_APPLICABLE" and not record["disposition_ref"]:
            errors.append(
                f"{oid}: NOT_APPLICABLE requires disposition_ref"
            )

    return errors


def cross_errors(
    manifest: dict[str, Any],
    ledger: dict[str, Any],
) -> list[str]:
    errors: list[str] = []

    candidate_sha = manifest["basis"]["candidate_sha"]
    if candidate_sha is None:
        errors.append("evidence ledger cannot certify a manifest without candidate_sha")
        return errors

    if ledger["candidate_sha"] != candidate_sha:
        errors.append("ledger candidate_sha must equal manifest candidate_sha")

    rows = obligation_rows(manifest)
    obligation_by_id = {obligation["id"]: obligation for _, obligation in rows}
    expected_ids = set(obligation_by_id)
    actual_ids = {record["obligation_id"] for record in ledger["records"]}

    missing = sorted(expected_ids - actual_ids)
    extra = sorted(actual_ids - expected_ids)
    if missing:
        errors.append("ledger is missing obligations: " + ", ".join(missing))
    if extra:
        errors.append("ledger contains unknown obligations: " + ", ".join(extra))

    for record in ledger["records"]:
        oid = record["obligation_id"]
        obligation = obligation_by_id.get(oid)
        if obligation is None:
            continue

        required = {
            requirement["id"]: requirement
            for requirement in obligation["evidence_required"]
        }
        covered: set[str] = set()

        for item in record["evidence_items"]:
            requirement_id = item["requirement_id"]
            if requirement_id is None:
                continue
            if requirement_id not in required:
                errors.append(
                    f"{oid}: evidence references undeclared requirement {requirement_id}"
                )
                continue
            expected_method = required[requirement_id]["method"]
            if item["method"] != expected_method:
                errors.append(
                    f"{oid}: requirement {requirement_id} expects method "
                    f"{expected_method}, got {item['method']}"
                )
            covered.add(requirement_id)

        if record["state"] == "VERIFIED":
            missing_requirements = sorted(set(required) - covered)
            if missing_requirements:
                errors.append(
                    f"{oid}: VERIFIED without required evidence coverage: "
                    + ", ".join(missing_requirements)
                )

    return errors


def validate_manifest(
    manifest: Any,
    label: str = "proof-obligation-manifest",
) -> list[str]:
    errors = schema_validate("proof-obligation-manifest", manifest, label)
    if errors:
        return errors
    return [f"{label}: {error}" for error in manifest_semantic_errors(manifest)]


def validate_ledger(
    ledger: Any,
    label: str = "evidence-ledger",
) -> list[str]:
    errors = schema_validate("evidence-ledger", ledger, label)
    if errors:
        return errors
    return [f"{label}: {error}" for error in ledger_semantic_errors(ledger)]


def validate_pair(
    manifest: Any,
    ledger: Any,
    manifest_label: str = "proof-obligation-manifest",
    ledger_label: str = "evidence-ledger",
) -> list[str]:
    errors = validate_manifest(manifest, manifest_label)
    errors.extend(validate_ledger(ledger, ledger_label))
    if errors:
        return errors
    return [
        f"{manifest_label} + {ledger_label}: {error}"
        for error in cross_errors(manifest, ledger)
    ]


def critical_findings(
    manifest: dict[str, Any],
    ledger: dict[str, Any],
) -> list[dict[str, Any]]:
    obligation_by_id = {
        obligation["id"]: obligation
        for _, obligation in obligation_rows(manifest)
    }
    findings: list[dict[str, Any]] = []
    for record in ledger["records"]:
        obligation = obligation_by_id.get(record["obligation_id"])
        if not obligation or obligation["severity"] != "CRITICAL":
            continue
        if record["state"] not in {"REFUTED", "UNKNOWN"}:
            continue
        evidence_refs = [
            ref
            for item in record["evidence_items"]
            for ref in item["refs"]
        ]
        findings.append({
            "id": record["obligation_id"],
            "state": record["state"],
            "evidence_refs": evidence_refs,
        })
    return findings


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Cross-validate proof obligations and exact-candidate evidence."
    )
    parser.add_argument("manifest")
    parser.add_argument("ledger")
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    ledger_path = Path(args.ledger)
    manifest = load_yaml(manifest_path)
    ledger = load_yaml(ledger_path)

    errors = validate_pair(
        manifest,
        ledger,
        manifest_path.name,
        ledger_path.name,
    )
    if errors:
        for error in errors:
            print(error)
        raise SystemExit(1)

    print(
        "OK: proof obligations: "
        f"{manifest_path} + {ledger_path}"
    )


if __name__ == "__main__":
    main()
