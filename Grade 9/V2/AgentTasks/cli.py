#!/usr/bin/env python3
"""
Unified CLI for the Standalone Delegation Layer / Task Composer.

Subcommands:
  resolve          Inspect current repository authority bindings and digests
  compile          Compile human task intent into a StandaloneExecutionPacket
  preflight        Generate non-authoritative Engineering Preflight visibility map
  validate-report  Validate execution report against schema and fail-closed rules
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

CLI_DIR = Path(__file__).resolve().parent
ENGINE_DIR = CLI_DIR / "engine"
sys.path.insert(0, str(ENGINE_DIR))

from resolve_execution_authority import (  # noqa: E402
    find_repository_root,
    get_git_head_and_base,
    resolve_authorities,
    load_json,
)
from compile_execution_packet import (  # noqa: E402
    compile_packet,
    format_markdown_entrypoint,
)
from validate_execution_report import validate_report  # noqa: E402
from engineering_preflight import generate_engineering_preflight  # noqa: E402


def cmd_resolve(args: argparse.Namespace) -> None:
    root = args.repo_root or find_repository_root()
    head, base = get_git_head_and_base(root)
    print(f"Repository Root: {root}")
    print(f"Current HEAD:    {head}")
    print(f"Target Base:     {base}\n")

    bindings = resolve_authorities(args.subject, repo_root=root)
    print(f"Authority Bindings for {args.subject} ({len(bindings)} resolved):")
    for b in bindings:
        print(f"  [{b['authority_class']:24}] {b['ref_path']}")
        print(f"    SHA-256: {b['digest_sha256']}")
        print(f"    Maturity: {b['maturity']} | Version: {b['version']}")


def cmd_compile(args: argparse.Namespace) -> None:
    task = load_json(args.task)
    packet = compile_packet(
        task,
        repo_root=args.repo_root,
        override_head=args.override_head,
        override_base=args.override_base,
    )

    args.out.parent.mkdir(parents=True, exist_ok=True)
    if args.out.suffix.lower() == ".md":
        content = format_markdown_entrypoint(packet)
        args.out.write_text(content, encoding="utf-8")
    else:
        args.out.write_text(json.dumps(packet, indent=2), encoding="utf-8")

    print(f"Compiled StandaloneExecutionPacket: {args.out}")
    print(f"Packet Digest: {packet['compiled_packet_digest']}")


def cmd_preflight(args: argparse.Namespace) -> None:
    packet = load_json(args.packet)
    preflight = generate_engineering_preflight(packet, repo_root=args.repo_root)
    print(preflight)


def cmd_validate_report(args: argparse.Namespace) -> None:
    report = load_json(args.report)
    packet = load_json(args.packet) if args.packet else None
    errors = validate_report(report, packet=packet)
    if errors:
        print(f"Validation FAILED ({len(errors)} errors):")
        for e in errors:
            print(f"- {e}")
        sys.exit(1)
    else:
        print("Validation PASS: Report satisfies all schema and fail-closed rules.")


def main():
    parser = argparse.ArgumentParser(
        description="Standalone Delegation Layer / Task Composer CLI"
    )
    parser.add_argument("--repo-root", type=Path, default=None, help="Repository root override")
    subparsers = parser.add_subparsers(dest="subcommand", required=True)

    # resolve
    p_res = subparsers.add_parser("resolve", help="Resolve current repository authority")
    p_res.add_argument("--subject", choices=["PHYSICS", "MATHEMATICS", "CHEMISTRY"], default="PHYSICS")
    p_res.set_defaults(func=cmd_resolve)

    # compile
    p_comp = subparsers.add_parser("compile", help="Compile task to execution packet")
    p_comp.add_argument("--task", required=True, type=Path, help="Input task JSON path")
    p_comp.add_argument("--out", required=True, type=Path, help="Output packet path (.json or .md)")
    p_comp.add_argument("--override-head", type=str, default=None, help="Override git HEAD")
    p_comp.add_argument("--override-base", type=str, default=None, help="Override git base")
    p_comp.set_defaults(func=cmd_compile)

    # preflight
    p_pref = subparsers.add_parser("preflight", help="Generate Engineering Preflight / Map")
    p_pref.add_argument("--packet", required=True, type=Path, help="Compiled packet JSON path")
    p_pref.set_defaults(func=cmd_preflight)

    # validate-report
    p_val = subparsers.add_parser("validate-report", help="Validate execution report")
    p_val.add_argument("--report", required=True, type=Path, help="Report JSON path")
    p_val.add_argument("--packet", type=Path, default=None, help="Optional compiled packet path for reconciliation")
    p_val.set_defaults(func=cmd_validate_report)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
