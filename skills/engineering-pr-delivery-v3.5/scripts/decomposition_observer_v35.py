from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Mapping

SCHEMA = "relay-v3.5-delp-decomposition-repository-observation"
PATH_IMPACTS = ("LOCAL", "BOUNDED_MULTI_STAGE", "CROSS_CUTTING", "UNKNOWN")
CHANGE_IMPACTS = ("CROSS_CUTTING", "UNKNOWN")
SAMPLE_LIMIT_DEFAULT = 20
SAMPLE_LIMIT_MAX = 100


class ObservationError(ValueError):
    """Repository decomposition basis could not be observed safely."""


def _digest(values: list[str]) -> str:
    payload = json.dumps(sorted(values), ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def _git(root: Path, *args: str) -> bytes:
    run = subprocess.run(
        ["git", "-C", str(root), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if run.returncode:
        detail = run.stderr.decode("utf-8", errors="replace").strip()
        raise ObservationError(f"git {' '.join(args)} failed: {detail or 'unknown error'}")
    return run.stdout


def _zpaths(data: bytes) -> list[str]:
    return sorted(
        item.decode("utf-8", errors="strict")
        for item in data.split(b"\0")
        if item
    )


def _tracked_files(root: Path) -> list[str]:
    return _zpaths(_git(root, "ls-files", "-z"))


def _normalise_surface(value: Any) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ObservationError("write_surface entries must be non-blank strings")
    text = value[2:] if value.startswith("./") else value
    segments = [part for part in text.split("/") if part]
    if (
        text.startswith("/")
        or "//" in text
        or not segments
        or "." in segments
        or ".." in segments
        or any(token in text for token in ("*", "?", "[", "]", "\\"))
    ):
        raise ObservationError(
            f"invalid write_surface {value!r}: expected repo-relative file or directory prefix, no glob"
        )
    return text


def _surface_contains(path: str, surface: str) -> bool:
    return path.startswith(surface) if surface.endswith("/") else path == surface


def _surface_overlap(left: list[str], right: list[str]) -> list[str]:
    hits: set[str] = set()
    for a in left:
        for b in right:
            if a == b or (a.endswith("/") and b.startswith(a)) or (b.endswith("/") and a.startswith(b)):
                hits.add(a if len(a) >= len(b) else b)
    return sorted(hits)


def _leaf(graph: Mapping[str, Any], ref: str) -> Mapping[str, Any]:
    nodes = graph.get("nodes")
    if not isinstance(nodes, list):
        raise ObservationError("graph.nodes must be a list")
    matches = [node for node in nodes if isinstance(node, Mapping) and str(node.get("ref") or "") == ref]
    if len(matches) != 1:
        raise ObservationError(f"leaf {ref!r}: expected exactly one exact graph node, found {len(matches)}")
    node = matches[0]
    if node.get("kind") != "LEAF":
        raise ObservationError(f"{ref}: repository observation requires a LEAF")
    return node


def _surface_list(node: Mapping[str, Any]) -> list[str]:
    raw = node.get("write_surface") or []
    if not isinstance(raw, list):
        raise ObservationError("write_surface must be a list")
    return sorted({_normalise_surface(item) for item in raw})


def _string_list(value: Any, label: str) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list) or any(not isinstance(item, str) or not item.strip() for item in value):
        raise ObservationError(f"{label} must be a list of non-blank strings")
    return sorted(set(value))


def _resolve_ref(root: Path, ref: str) -> str:
    return _git(root, "rev-parse", "--verify", f"{ref}^{{commit}}").decode("ascii").strip()


def observe_repository_basis(
    graph: Mapping[str, Any],
    *,
    leaf_ref: str,
    repo_root: Path,
    base_ref: str | None = None,
    candidate_ref: str | None = None,
    sample_limit: int = SAMPLE_LIMIT_DEFAULT,
) -> dict[str, Any]:
    """Observe path-level repository truth for one proposed/existing leaf.

    The result deliberately does not claim semantic cohesion, dependency closure,
    verification closure, stable-cut validity, or handoff cost.
    """
    if isinstance(sample_limit, bool) or not isinstance(sample_limit, int) or not (1 <= sample_limit <= SAMPLE_LIMIT_MAX):
        raise ObservationError(f"sample_limit must be 1..{SAMPLE_LIMIT_MAX}")
    root = Path(repo_root).resolve()
    if not (root / ".git").exists():
        raise ObservationError(f"repo_root is not a Git working tree: {root}")

    node = _leaf(graph, leaf_ref)
    surfaces = _surface_list(node)
    tracked = _tracked_files(root)

    entries: list[dict[str, Any]] = []
    matched_flags: list[bool] = []
    for surface in surfaces:
        matched = [path for path in tracked if _surface_contains(path, surface)]
        matched_flags.append(bool(matched))
        entries.append(
            {
                "surface": surface,
                "matched_count": len(matched),
                "matched_digest": _digest(matched),
                "sample": matched[:sample_limit],
            }
        )

    if not surfaces:
        surface_status = "EMPTY"
    elif all(matched_flags):
        surface_status = "COMPLETE"
    elif any(matched_flags):
        surface_status = "PARTIAL"
    else:
        surface_status = "UNRESOLVED"

    overlaps: list[dict[str, Any]] = []
    nodes = graph.get("nodes") or []
    for sibling in nodes:
        if not isinstance(sibling, Mapping) or sibling is node or sibling.get("kind") != "LEAF":
            continue
        sibling_ref = str(sibling.get("ref") or "")
        sibling_surface = _surface_list(sibling)
        hit = _surface_overlap(surfaces, sibling_surface)
        if hit:
            overlaps.append({"ref": sibling_ref, "overlaps": hit})
    overlaps.sort(key=lambda row: row["ref"])

    boundaries = _string_list(node.get("transformation_boundaries"), "transformation_boundaries")
    dependencies = _string_list(node.get("depends_on"), "depends_on")

    if (base_ref is None) != (candidate_ref is None):
        raise ObservationError("base_ref and candidate_ref must be supplied together")

    if base_ref is None:
        diff = {
            "visibility": "NOT_REQUESTED",
            "base_ref": None,
            "candidate_ref": None,
            "base_sha": None,
            "candidate_sha": None,
            "changed_count": None,
            "changed_digest": None,
            "sample": [],
            "outside_surface_count": None,
            "outside_surface_digest": None,
            "outside_sample": [],
        }
        outside: list[str] = []
    else:
        base_sha = _resolve_ref(root, str(base_ref))
        candidate_sha = _resolve_ref(root, str(candidate_ref))
        changed = _zpaths(_git(root, "diff", "--name-only", "-z", f"{base_sha}...{candidate_sha}"))
        outside = [
            path
            for path in changed
            if not any(_surface_contains(path, surface) for surface in surfaces)
        ]
        diff = {
            "visibility": "OBSERVED",
            "base_ref": str(base_ref),
            "candidate_ref": str(candidate_ref),
            "base_sha": base_sha,
            "candidate_sha": candidate_sha,
            "changed_count": len(changed),
            "changed_digest": _digest(changed),
            "sample": changed[:sample_limit],
            "outside_surface_count": len(outside),
            "outside_surface_digest": _digest(outside),
            "outside_sample": outside[:sample_limit],
        }

    cross_cutting = bool(overlaps) or bool(outside)
    if cross_cutting:
        path_impact = "CROSS_CUTTING"
    elif surface_status != "COMPLETE":
        path_impact = "UNKNOWN"
    elif len(boundaries) > 1:
        path_impact = "BOUNDED_MULTI_STAGE"
    elif surfaces:
        path_impact = "LOCAL"
    else:
        path_impact = "UNKNOWN"

    # Path locality cannot prove semantic dependency locality without a language/
    # build-system dependency observer. Only proven cross-cutting evidence is
    # promoted to the semantic change-impact vocabulary.
    change_impact = "CROSS_CUTTING" if cross_cutting else "UNKNOWN"

    return {
        "schema": SCHEMA,
        "subject": leaf_ref,
        "repository": {
            "tracked_count": len(tracked),
            "tracked_digest": _digest(tracked),
            "sample": tracked[:sample_limit],
        },
        "write_surface": {
            "declared": surfaces,
            "status": surface_status,
            "entries": entries,
        },
        "sibling_overlaps": overlaps,
        "transformation_boundaries": boundaries,
        "declared_dependencies": dependencies,
        "candidate_diff": diff,
        "path_impact": path_impact,
        "change_impact": change_impact,
        "static_dependency_visibility": "UNAVAILABLE",
    }


def _load(path: Path) -> Any:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() in {".yaml", ".yml"}:
        try:
            import yaml  # type: ignore
        except ImportError as exc:  # pragma: no cover
            raise ObservationError("PyYAML is required for YAML graph inputs") from exc
        return yaml.safe_load(text)
    return json.loads(text)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Observe V3.5 decomposition repository basis without mutating it.")
    parser.add_argument("--graph", type=Path, required=True)
    parser.add_argument("--leaf", required=True)
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--base-ref")
    parser.add_argument("--candidate-ref")
    parser.add_argument("--sample-limit", type=int, default=SAMPLE_LIMIT_DEFAULT)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)

    graph = _load(args.graph)
    if not isinstance(graph, Mapping):
        raise ObservationError("graph input must be a mapping")
    result = observe_repository_basis(
        graph,
        leaf_ref=args.leaf,
        repo_root=args.repo_root,
        base_ref=args.base_ref,
        candidate_ref=args.candidate_ref,
        sample_limit=args.sample_limit,
    )
    text = json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
