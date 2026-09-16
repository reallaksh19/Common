#!/usr/bin/env python3
"""
Execution Authority Resolver.

Discovers current repository state, git HEAD/base commits, binds applicable
canonical manifests and engineering gate policies, and calculates deterministic
SHA-256 digests for all authoritative dependencies.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


def find_repository_root(start_path: Optional[Path] = None) -> Path:
    """Traverse up to find the repository root containing .git."""
    curr = (start_path or Path(__file__)).resolve()
    for parent in [curr] + list(curr.parents):
        if (parent / ".git").exists():
            return parent
    # Fallback to parents[3] if running from Grade 9/V2/AgentTasks/engine
    return Path(__file__).resolve().parents[3]


def get_git_head_and_base(repo_root: Path, target_ref: str = "main") -> Tuple[str, str]:
    """Retrieve exact current HEAD and merge base with target ref."""
    try:
        head = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_root,
            text=True,
            stderr=subprocess.DEVNULL
        ).strip()
    except Exception:
        head = "UNKNOWN"

    try:
        # Determine base against target ref or origin/main
        candidate_refs = [target_ref, f"origin/{target_ref}", "origin/main", "main"]
        base = "UNKNOWN"
        for ref in candidate_refs:
            try:
                base = subprocess.check_output(
                    ["git", "merge-base", "HEAD", ref],
                    cwd=repo_root,
                    text=True,
                    stderr=subprocess.DEVNULL
                ).strip()
                if base:
                    break
            except Exception:
                continue
    except Exception:
        base = "UNKNOWN"

    return head, base


def compute_file_sha256(path: Path) -> str:
    """Compute SHA-256 hex digest of file bytes."""
    if not path.is_file():
        raise FileNotFoundError(f"Authoritative file not found: {path}")
    hasher = hashlib.sha256()
    hasher.update(path.read_bytes())
    return hasher.hexdigest()


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_authorities(
    subject: str,
    repo_root: Optional[Path] = None
) -> List[Dict[str, Any]]:
    """Resolve authoritative files for the given subject and compute their digests."""
    root = repo_root or find_repository_root()
    routing_path = root / "Grade 9" / "V2" / "AgentTasks" / "registry" / "subject-routing-registry.json"
    routing = load_json(routing_path)

    routes = routing.get("routes", {})
    if subject not in routes:
        raise ValueError(f"Unknown subject '{subject}' in routing registry.")

    subj_routes = routes[subject]
    bindings: List[Dict[str, Any]] = []

    # Map routing keys to authority classes
    key_to_class = {
        "manifest_ref": ("SUBJECT_MANIFEST", "ACTIVE"),
        "entrypoint_ref": ("SUBJECT_ENTRYPOINT", "ACTIVE"),
        "engineering_gate_spec": ("ENGINEERING_GATE_SPEC", "ACTIVE"),
        "gate_policy_ref": ("ENGINEERING_GATE_POLICY", "ACTIVE"),
        "gate_validator_ref": ("ENGINEERING_GATE_VALIDATOR", "ACTIVE"),
        "canonical_capabilities_ref": ("CANONICAL_CAPABILITIES", "ACTIVE"),
        "source_provenance_schema_ref": ("SOURCE_PROVENANCE_SCHEMA", "ACTIVE"),
        "blueprint_architecture_ref": ("BLUEPRINT_ARCHITECTURE", "ACTIVE"),
    }

    for key, (auth_class, maturity) in key_to_class.items():
        if key in subj_routes:
            rel_path = subj_routes[key]
            full_path = root / rel_path
            if full_path.exists():
                digest = compute_file_sha256(full_path)
                bindings.append({
                    "authority_class": auth_class,
                    "ref_path": rel_path.replace("\\", "/"),
                    "digest_sha256": digest,
                    "maturity": maturity,
                    "version": "1.0.0"
                })

    return bindings


def check_packet_freshness(
    packet: Dict[str, Any],
    repo_root: Optional[Path] = None
) -> List[str]:
    """Check whether a compiled packet's authority bindings match the current working tree.
    Returns list of mismatch descriptions; empty if completely fresh."""
    root = repo_root or find_repository_root()
    mismatches: List[str] = []

    bindings = packet.get("authority_bindings", [])
    for b in bindings:
        rel_path = b.get("ref_path")
        expected_digest = b.get("digest_sha256")
        full_path = root / rel_path
        if not full_path.exists():
            mismatches.append(f"Missing authority file: {rel_path}")
            continue

        actual_digest = compute_file_sha256(full_path)
        if actual_digest != expected_digest:
            mismatches.append(
                f"Stale authority for {rel_path}: expected {expected_digest[:12]}..., got {actual_digest[:12]}..."
            )

    return mismatches
