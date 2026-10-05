#!/usr/bin/env python3
"""Scaffold a thin repository adapter for Engineering Relay V3.1 RLL-1."""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys

TOKEN_RE = re.compile(r"\{\{([A-Z0-9_]+)\}\}")

TEMPLATES = {
    ".agents/rules/rll-1.md": ".agents/rules/rll-1.md.tmpl",
    "scripts/rll1-antigravity-worker.ps1": "scripts/rll1-antigravity-worker.ps1.tmpl",
    "scripts/install-rll1-antigravity-sidecar.ps1": "scripts/install-rll1-antigravity-sidecar.ps1.tmpl",
    "docs/RLL1_LOCAL_AUTOMATION.md": "docs/RLL1_LOCAL_AUTOMATION.md.tmpl",
}


def sidecar_id(repository: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", repository.lower()).strip("-") + "-rll1"


def render(source: str, values: dict[str, str]) -> str:
    missing = sorted({m.group(1) for m in TOKEN_RE.finditer(source)} - values.keys())
    if missing:
        raise ValueError(f"missing template values: {', '.join(missing)}")
    result = source
    for key, value in values.items():
        result = result.replace("{{" + key + "}}", value)
    unresolved = sorted({m.group(1) for m in TOKEN_RE.finditer(result)})
    if unresolved:
        raise ValueError(f"unresolved template values: {', '.join(unresolved)}")
    return result


def scaffold(
    repo_root: Path,
    *,
    repository: str,
    required_common_basis: str,
    authorized_login: str,
    worker_id: str,
    force: bool,
) -> list[str]:
    template_root = Path(__file__).resolve().parents[1] / "templates" / "rll-adapter"
    values = {
        "REPOSITORY": repository,
        "REQUIRED_COMMON_BASIS": required_common_basis,
        "AUTHORIZED_LOGIN": authorized_login,
        "WORKER_ID": worker_id,
        "SIDECAR_ID": sidecar_id(repository),
    }

    written: list[str] = []
    for destination, template_rel in TEMPLATES.items():
        source_path = template_root / template_rel
        if not source_path.is_file():
            raise FileNotFoundError(f"missing RLL adapter template: {source_path}")
        rendered = render(source_path.read_text(encoding="utf-8"), values)
        target = repo_root / destination
        if target.exists():
            existing = target.read_text(encoding="utf-8")
            if existing == rendered:
                continue
            if not force:
                raise FileExistsError(
                    f"{target} already exists with different content; use --force only after review"
                )
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(rendered, encoding="utf-8", newline="\n")
        written.append(destination)
    return written


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Scaffold a thin RLL-1 repository adapter.")
    p.add_argument("--repo-root", required=True)
    p.add_argument("--repository", required=True, help="GitHub owner/repo")
    p.add_argument("--required-common-basis", required=True)
    p.add_argument("--authorized-login", required=True)
    p.add_argument("--worker-id", default="antigravity-local")
    p.add_argument("--force", action="store_true")
    return p


def main() -> int:
    args = parser().parse_args()
    repo_root = Path(args.repo_root).resolve()
    if not repo_root.exists():
        print(f"repo root does not exist: {repo_root}", file=sys.stderr)
        return 2
    try:
        written = scaffold(
            repo_root,
            repository=args.repository,
            required_common_basis=args.required_common_basis,
            authorized_login=args.authorized_login,
            worker_id=args.worker_id,
            force=args.force,
        )
    except (ValueError, FileExistsError, FileNotFoundError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    for path in written:
        print(path)
    if not written:
        print("RLL adapter already matches the requested template.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
