#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from coordlib import dump_yaml, load_yaml, validate as schema_validate

from p3_integration_contract import (
    AUTHORITY_BOUNDARIES,
    CHECK_IDS,
    object_digest,
    validate_source,
)
from p3_integration_lanes import compile_qualification


def result_semantic_errors(result: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if result["result_digest"] != object_digest(result, "result_digest"):
        errors.append("result_digest does not match canonical result content")
    ids = [row["id"] for row in result["lanes"]]
    if tuple(ids) != CHECK_IDS:
        errors.append("result lanes must equal P3I-01..P3I-20 in order")
    passed = sum(row["passed"] for row in result["lanes"])
    if result["accounting"]["passed"] != passed:
        errors.append("accounting.passed does not equal passed lanes")
    if result["accounting"]["failed"] != len(result["lanes"]) - passed:
        errors.append("accounting.failed does not equal failed lanes")
    expected_status = "QUALIFIED" if passed == len(result["lanes"]) else "FAILED"
    if result["qualification_status"] != expected_status:
        errors.append("qualification_status does not match lane results")
    if result["authority_boundaries"] != AUTHORITY_BOUNDARIES:
        errors.append("result authority boundaries do not match fixed contract")
    return errors


def validate_result_shape(
    result: Any,
    label: str = "p3-integration-qualification-result",
) -> list[str]:
    errors = schema_validate("p3-integration-qualification-result", result, label)
    if errors:
        return errors
    return [f"{label}: {row}" for row in result_semantic_errors(result)]


def validate_result(
    result: Any,
    source: Any | None = None,
    candidate_sha: str | None = None,
    pr_number: int | None = None,
    candidate_ref: str | None = None,
    repo_root: Path | None = None,
    label: str = "p3-integration-qualification-result",
) -> list[str]:
    errors = validate_result_shape(result, label)
    if errors:
        return errors
    if any(
        item is None
        for item in (
            source,
            candidate_sha,
            pr_number,
            candidate_ref,
            repo_root,
        )
    ):
        return [f"{label}: source-bound exact-head P3-I replay is required"]
    try:
        fresh = compile_qualification(
            source,
            candidate_sha,
            pr_number,
            candidate_ref,
            repo_root,
        )
    except Exception as exc:
        return [f"{label}: exact-head P3-I replay failed: {exc}"]
    if fresh != result:
        errors.append(f"{label}: stored result does not equal fresh exact-head P3-I replay")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Qualify the full Phase-3 solo-principal review/control chain on an "
            "exact candidate. Emits qualification evidence only."
        )
    )
    sub = parser.add_subparsers(dest="command", required=True)

    compile_parser = sub.add_parser("compile")
    compile_parser.add_argument("source")
    compile_parser.add_argument("candidate_sha")
    compile_parser.add_argument("pr_number", type=int)
    compile_parser.add_argument("candidate_ref")
    compile_parser.add_argument("--repo-root", default=".")
    compile_parser.add_argument("--output")

    validate_parser = sub.add_parser("validate")
    validate_parser.add_argument("source")
    validate_parser.add_argument("result")
    validate_parser.add_argument("candidate_sha")
    validate_parser.add_argument("pr_number", type=int)
    validate_parser.add_argument("candidate_ref")
    validate_parser.add_argument("--repo-root", default=".")

    args = parser.parse_args()
    source = load_yaml(Path(args.source))
    root = Path(args.repo_root).resolve()

    if args.command == "compile":
        result = compile_qualification(
            source,
            args.candidate_sha,
            args.pr_number,
            args.candidate_ref,
            root,
        )
        rendered = dump_yaml(result)
        if args.output:
            Path(args.output).write_text(rendered, encoding="utf-8")
        else:
            print(rendered, end="")
        return

    result = load_yaml(Path(args.result))
    errors = validate_result(
        result,
        source,
        args.candidate_sha,
        args.pr_number,
        args.candidate_ref,
        root,
        Path(args.result).name,
    )
    if errors:
        for error in errors:
            print(error)
        raise SystemExit(1)
    print(
        "OK: P3-I exact-head solo role replay QUALIFIED; "
        "principal_independence=NONE; no lifecycle/merge/production authority emitted"
    )


if __name__ == "__main__":
    main()
