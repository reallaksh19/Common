#!/usr/bin/env python3
"""
Engineering Preflight / Engineering Map Generator.

A strictly non-authoritative derived view that inspects the current repository
state, resolves subtopic gate readiness, exposes prerequisite edges (internal
and external cross-domain), and displays consumer permission states.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

SCRIPT_DIR = Path(__file__).resolve().parent
AGENT_TASKS_DIR = SCRIPT_DIR.parent

sys.path.insert(0, str(SCRIPT_DIR))
from resolve_execution_authority import find_repository_root, load_json


def generate_engineering_preflight(
    packet: Dict[str, Any],
    repo_root: Optional[Path] = None
) -> str:
    """Derive human-readable Engineering Preflight from packet and authoritative registries."""
    root = repo_root or find_repository_root()
    task = packet["task"]
    repo = packet["resolved_repository"]
    subject = task["subject"]
    topic = task["topic"]
    subtopic = task["subtopic"]
    depth = task["engineering_depth"]
    learner_state = task["learner_state"]

    lines = []
    lines.append("================================================================================")
    lines.append("                         ENGINEERING PREFLIGHT / MAP                            ")
    lines.append("             (Strictly Non-Authoritative Derived Visibility View)                ")
    lines.append("================================================================================")
    lines.append("")
    lines.append(f"Task: {subject} -> {topic} -> {subtopic}")
    lines.append(f"Task Kind: {task['task_kind']} | Depth: {depth} | Learner State: {learner_state}")
    lines.append(f"Packet ID: {packet['packet_id']} (Digest: {packet['compiled_packet_digest'][:16]}...)")
    lines.append("")
    lines.append("--- Bound Repository Authority ---")
    lines.append(f"Repository HEAD: {repo['resolved_head']}")
    lines.append(f"Repository Base: {repo['resolved_base']}")
    for b in packet.get("authority_bindings", []):
        lines.append(f"  [{b['authority_class']}] {b['ref_path']} (SHA: {b['digest_sha256'][:12]}...)")
    lines.append("")

    # Look up in Technical Engineering Gate registry if Physics
    gate_data: Optional[Dict[str, Any]] = None
    if subject == "PHYSICS":
        gate_path = root / "Grade 9" / "V2" / "Physics" / "Blueprint" / "policy" / "physics-technical-engineering-gates.v1.json"
        if gate_path.exists():
            gates_json = load_json(gate_path)
            for g in gates_json.get("subtopic_gates", []):
                # Match by ID or normalized title
                sid = g.get("subtopic_id", "")
                title = g.get("learner_title", "")
                if (subtopic.lower() in title.lower() or
                    title.lower() in subtopic.lower() or
                    subtopic.lower() in sid.lower()):
                    gate_data = g
                    break

    lines.append("--- Current Scope State ---")
    if gate_data:
        lines.append(f"Identity Resolution: REGISTERED ({gate_data['subtopic_id']})")
        lines.append(f"Learner Title:       {gate_data['learner_title']}")
        lines.append(f"Authority Tier:      {gate_data['authority_tier']}")
        lines.append(f"Gate Readiness:      {gate_data['technical_readiness']}")
        lines.append(f"Curriculum Binding:  CBSE Gr {gate_data['cbse_ref']['grade']}, Ch {gate_data['cbse_ref']['chapter']} | JEE: {gate_data['jee_tier']}")

        concepts = [c['concept_id'] for c in gate_data.get('technical_core', [])]
        lines.append(f"Canonical Concepts:  {len(concepts)} registered: {', '.join(concepts[:4])}{'...' if len(concepts) > 4 else ''}")

        prereqs = gate_data.get("prerequisite_ids", [])
        internal_prereqs = [p for p in prereqs if p.startswith("PHY-")]
        external_prereqs = [p for p in prereqs if not p.startswith("PHY-")]

        lines.append(f"Internal Prereqs:    {', '.join(internal_prereqs) if internal_prereqs else 'None'}")
        lines.append(f"External Prereqs:    {', '.join(external_prereqs) if external_prereqs else 'None'}")
        if external_prereqs:
            lines.append("  ↳ [CrossDomain Dependency]: Requires provider-owned authority; consumer subject cannot self-certify.")

        eqs = [e['equation_id'] for e in gate_data.get('mandatory_equations', [])]
        reps = [r['representation_id'] for r in gate_data.get('representations', [])]
        misconceptions = [m['misconception_id'] for m in gate_data.get('misconceptions', [])]
        lines.append(f"Mandatory Equations: {len(eqs)} required")
        lines.append(f"Representations:     {len(reps)} required: {', '.join(reps)}")
        lines.append(f"Known Misconceptions:{len(misconceptions)} cataloged")
    else:
        lines.append(f"Identity Resolution: UNREGISTERED CANDIDATE ({subtopic})")
        lines.append("Gate Readiness:      HELD (No entry in Technical Engineering Gate Registry)")
        lines.append("Canonical Concepts:  PENDING_DISCOVERY")
        lines.append("Prerequisites:       UNKNOWN")
        lines.append("Representations:     PENDING_DESIGN")

    lines.append("")
    lines.append("--- Consumer State ---")
    if gate_data and gate_data.get("technical_readiness") == "ENGINEERING_GATE_READY":
        lines.append("PROBLEM_SEMANTICS:   AUTHORIZED (Ready for problem family and verification mining)")
        lines.append("CORE_AUTHORING:      AUTHORIZED (Ready for Core1 lesson and concept TTU authoring)")
        lines.append("CORE2_TRANSFER:      AUTHORIZED (Ready for transfer item and hint ladder composition)")
        lines.append("REPRESENTATION:      AUTHORIZED (Primitives specified)")
        lines.append("PUBLICATION:         BLOCKED_PENDING_AUTHORIZED_REVIEW (Requires real human subject/pedagogy review)")
    else:
        lines.append("PROBLEM_SEMANTICS:   HELD (Technical engineering gate incomplete or unvalidated)")
        lines.append("CORE_AUTHORING:      HELD (Technical engineering gate incomplete or unvalidated)")
        lines.append("CORE2_TRANSFER:      HELD (Technical engineering gate incomplete or unvalidated)")
        lines.append("REPRESENTATION:      HELD (Technical engineering gate incomplete or unvalidated)")
        lines.append("PUBLICATION:         NOT_IMPLIED")

    lines.append("")
    lines.append("--- Open Actions ---")
    if not gate_data:
        lines.append("1. Perform OPEN_DISCOVERY to establish curriculum scope and canonical definitions.")
        lines.append("2. Reconcile capability granularity against Canonical registries.")
        lines.append("3. Formulate Free-Body / coordinate representations and model validity limits.")
        lines.append("4. Resolve external-domain mathematics prerequisites with provider ownership.")
        lines.append("5. Build candidate gate entry and run validate_engineering_gates.py.")
    elif gate_data.get("technical_readiness") == "ENGINEERING_GATE_READY":
        lines.append("1. Maintain zero Blueprint edits; generate content in data-only layers.")
        lines.append("2. Verify that problem families do not violate model conditions.")
        lines.append("3. Execute falsification battery and compile execution report.")
    else:
        lines.append(f"1. Resolve gate incompletions for {gate_data['subtopic_id']}.")

    lines.append("================================================================================")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate Engineering Preflight")
    parser.add_argument("--packet", required=True, type=Path, help="Path to compiled packet JSON")
    parser.add_argument("--repo-root", type=Path, default=None, help="Repository root path")

    args = parser.parse_args()
    packet = load_json(args.packet)
    preflight = generate_engineering_preflight(packet, repo_root=args.repo_root)
    print(preflight)


if __name__ == "__main__":
    main()
