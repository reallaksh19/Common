#!/usr/bin/env python3
"""Generate structured JavaScript catalog data from SUBTOPIC_INTELLIGENCE_INTAKE_SPECIFICATION.md.

Runs deterministically without external dependencies.
Outputs tools/sil_explorer/sil_catalog_data.js for offline UI consumption across all 43 Physics subtopics.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[2]
SPEC_PATH = ROOT / "SUBTOPIC_INTELLIGENCE_INTAKE_SPECIFICATION.md"
ENGINE_PATH = ROOT / "engine"
GATES_PATH = ROOT / "policy" / "physics-technical-engineering-gates.v1.json"
OUTPUT_JS = ROOT / "tools" / "sil_explorer" / "sil_catalog_data.js"

sys.path.insert(0, str(ENGINE_PATH))
from validate_subtopic_intelligence_library import extract_packets  # noqa: E402


def _load_gates_metadata() -> Dict[str, Dict[str, Any]]:
    if not GATES_PATH.exists():
        return {}
    data = json.loads(GATES_PATH.read_text(encoding="utf-8"))
    return {g["subtopic_id"]: g for g in data.get("subtopic_gates", [])}


GATES_META = _load_gates_metadata()


def parse_packet_details(packet: Dict[str, Any]) -> Dict[str, Any]:
    gate_id = packet["gate_id"]
    title = packet["title"]
    body = packet["body"]
    sec_num = packet["section_number"]

    meta = GATES_META.get(gate_id, {})
    domain = meta.get("chapter", "Physics Mechanics")
    grade_val = meta.get("cbse_ref", {}).get("grade", 11)
    grade_level = f"Grade {grade_val}"
    tier = meta.get("jee_tier", "JEE_MAIN")
    exam_families = ["CBSE", "JEE Main"]
    if tier in ("JEE_ADVANCED", "OLYMPIAD"):
        exam_families.extend(["JEE Advanced", "NSEP Olympiad"])

    # Extract Preconditions
    preconditions = []
    precon_block = re.search(r"\*\*Non-Negotiable Preconditions\*\*:\s*\n(.*?)(?=\n###|\n---|\Z)", body, re.DOTALL)
    if precon_block:
        for line in precon_block.group(1).strip().splitlines():
            line = line.strip()
            if re.match(r"^\d+\.\s+\*\*", line):
                preconditions.append(re.sub(r"^\d+\.\s+", "", line))

    # Extract Atoms
    atoms = []
    atom_matches = re.finditer(
        r"[`]?([A-Z0-9_-]+)[`]?\s*\([`'\"']?(CONCEPT|RELATION|INVARIANT|PROCEDURE|STRATEGY)[`'\"']?\):\s*(.*?)(?=\n-\s*[`]?[A-Z0-9_-]+[`]?\s*\(|\n####|\n###|\Z)",
        body,
        re.DOTALL,
    )
    for am in atom_matches:
        atoms.append({
            "atom_id": am.group(1).strip("`"),
            "atom_type": am.group(2),
            "description": am.group(3).strip(),
        })

    # Extract Misconceptions
    misconceptions = []
    misc_matches = re.finditer(
        r"\*\*Misconception:\s*(.*?)\*\*:\s*\n\s*-\s*\*Flawed Action\*:\s*(.*?)\n\s*-\s*\*(?:Correct )?Diagnostic Cue\*:\s*(.*?)(?=\n\s*\d+\.|\n###|\n---|\Z)",
        body,
        re.DOTALL,
    )
    for mm in misc_matches:
        misconceptions.append({
            "name": mm.group(1).strip(),
            "flawed_action": mm.group(2).strip(),
            "diagnostic_cue": mm.group(3).strip(),
        })

    # Extract TTUs
    ttus = []
    ttu_matches = re.finditer(
        r"####\s+(TTU-[A-Z0-9-]+):\s+(.*?)\s*\((.*?)\)\s*\n(.*?)(?=####|\n### Layer 4|\n---\s*\n###|\Z)",
        body,
        re.DOTALL,
    )
    for tm in ttu_matches:
        ttu_id = tm.group(1).strip()
        ttu_title = tm.group(2).strip()
        ttu_role = tm.group(3).strip()
        ttu_content = tm.group(4)

        kind_m = re.search(r"\*Kind\*:\s*`?(.*?)`?\s*\|", ttu_content)
        viewport_m = re.search(r"(?:Viewport|\*Viewport\*):\s*`?(.*?)`?(?:,\s*clip_to_viewport|\||\n)", ttu_content)
        scaffold_m = re.search(r"(?:\[INCOMPLETE.*?\]|\*Incomplete Scaffold\*:\s*)(.*?)(?=\[COMPLETION|\*Completion Key\*|\Z)", ttu_content, re.DOTALL)
        key_m = re.search(r"(?:\[COMPLETION.*?\]|\*Completion Key\*:\s*)(.*?)(?=```|\n####|\n###|\Z)", ttu_content, re.DOTALL)

        ttus.append({
            "ttu_id": ttu_id,
            "title": ttu_title,
            "role": ttu_role,
            "kind": kind_m.group(1).strip() if kind_m else "RECONSTRUCTABLE_SCAFFOLD",
            "viewport": viewport_m.group(1).strip() if viewport_m else "x ∈ [-5, 5], y ∈ [-5, 5]",
            "scaffold": scaffold_m.group(1).strip() if scaffold_m else "Incomplete physical scaffold",
            "completion_key": key_m.group(1).strip() if key_m else "Verification key",
        })

    # Extract Problem Families
    families = []
    fam_matches = re.finditer(
        r"(?:-\s+\*\*|)(FAMILY-[A-Z0-9-]+)\s*\((.*?)\)(?:\*\*:\s*|:\s*\n\s*)(.*?)(?=\n\s*(?:-\s+\*\*|)FAMILY|\n```|\n---|\n##|\Z)",
        body,
        re.DOTALL,
    )
    for fm in fam_matches:
        families.append({
            "family_id": fm.group(1).strip(),
            "tier": fm.group(2).strip(),
            "description": fm.group(3).strip(),
        })

    return {
        "gate_id": gate_id,
        "title": title,
        "section_number": sec_num,
        "domain": domain,
        "grade_level": grade_level,
        "exam_families": exam_families,
        "preconditions": preconditions,
        "atoms": atoms,
        "misconceptions": misconceptions,
        "ttus": ttus,
        "families": families,
    }


def main() -> None:
    spec_text = SPEC_PATH.read_text(encoding="utf-8")
    raw_packets = extract_packets(spec_text)

    catalog = [parse_packet_details(p) for p in raw_packets]

    OUTPUT_JS.parent.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(catalog, indent=2, ensure_ascii=False)
    js_content = f"// Subtopic Intelligence Library - Catalog Data\n// Auto-generated by generate_sil_catalog.py. Deterministic & Offline Capable.\n\nwindow.SIL_CATALOG = {serialized};\n"
    OUTPUT_JS.write_text(js_content, encoding="utf-8")
    print(f"Generated Physics SIL catalog data at {OUTPUT_JS} ({len(catalog)} packets)")


if __name__ == "__main__":
    main()
