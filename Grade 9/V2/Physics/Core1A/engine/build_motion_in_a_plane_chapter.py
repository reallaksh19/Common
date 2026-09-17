#!/usr/bin/env python3
"""Compile the source-locked Motion in a Plane Core (1A) chapter registry.

This compiler is intentionally stricter than the generic Core1A compiler.  It is used
for a source-specific chapter build where every source subtopic/equation must have an
explicit learner home before the PDF renderer is allowed to claim chapter coverage.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parents[1]
REG = ROOT / "registry"
SOURCE = REG / "physics-core1a-motion-in-a-plane-source-inventory.json"
CHAPTER = REG / "physics-core1a-motion-in-a-plane-chapter-v1.json"
CORE2 = REG / "physics-core1a-core2-linkage.json"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def canonical(obj):
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def sha256(obj):
    return hashlib.sha256(canonical(obj).encode("utf-8")).hexdigest()


def challenge_ids(linkage):
    rows = linkage.get("challenge_links") or []
    return {row["challenge_id"] for row in rows}


def index(rows):
    return {row["id"]: row for row in rows}


def fail(message):
    raise ValueError(message)


def validate(source, chapter, linkage):
    groups = index(source["source_groups"])
    equations = index(source["equations"])
    valid_questions = challenge_ids(linkage)

    seen = set()
    for concept in chapter["concepts"]:
        cid = concept["concept_id"]
        if cid in seen:
            fail(f"duplicate concept_id: {cid}")
        seen.add(cid)

        if concept["difficulty"] not in {"D1", "D2", "D3", "D4"}:
            fail(f"{cid}: invalid difficulty")
        if concept["build_status"] not in {"PLANNED", "BUILT", "VERIFIED"}:
            fail(f"{cid}: invalid build_status")
        if not concept.get("learner_title"):
            fail(f"{cid}: learner title missing")
        if not concept.get("plain_language"):
            fail(f"{cid}: plain-language explanation missing")
        if not concept.get("illustration", {}).get("stages"):
            fail(f"{cid}: staged illustration missing")
        if not concept.get("easy_mistake"):
            fail(f"{cid}: easy-mistake support missing")

        min_stages = {"D1": 2, "D2": 3, "D3": 3, "D4": 3}[concept["difficulty"]]
        if len(concept["illustration"]["stages"]) < min_stages:
            fail(f"{cid}: {concept['difficulty']} needs at least {min_stages} stages")

        for gid in concept.get("source_group_ids", []):
            if gid not in groups:
                fail(f"{cid}: unknown source group {gid}")
        for eid in concept.get("equation_ids", []):
            if eid not in equations:
                fail(f"{cid}: unknown equation {eid}")
        for qid in concept.get("core2_challenges", []):
            if qid not in valid_questions:
                fail(f"{cid}: unknown Core (2) challenge {qid}")

    # Every source group in the declared build scope through §6 must have a home.
    required_groups = {
        "SRC-G1", "SRC-G2", "SRC-G3", "SRC-G3.1", "SRC-G3.1.1", "SRC-G3.1.2",
        "SRC-G3.1.3", "SRC-G3.1.4", "SRC-G3.1.5", "SRC-G3-TRAJ", "SRC-G6"
    }
    covered_groups = {gid for c in chapter["concepts"] for gid in c.get("source_group_ids", [])}
    missing_groups = sorted(required_groups - covered_groups)
    if missing_groups:
        fail("source groups missing from first build: " + ", ".join(missing_groups))

    # Every equation belonging to a source group in this build must be taught somewhere.
    build_homes = {
        "PROJECTILE_COMPONENT_CLOCK", "PROJECTILE_SAME_HEIGHT", "PROJECTILE_APEX",
        "PROJECTILE_TRAJECTORY", "RELATIVE_MOTION_FOUNDATION"
    }
    required_equations = {eid for eid, row in equations.items() if row.get("core1a_home") in build_homes}
    covered_equations = {eid for c in chapter["concepts"] for eid in c.get("equation_ids", [])}
    missing_equations = sorted(required_equations - covered_equations)
    if missing_equations:
        fail("source equations missing from first build: " + ", ".join(missing_equations))

    # No equation is accepted merely because it is named: it must carry a source validity condition.
    for eid in covered_equations:
        if not equations[eid].get("valid_when"):
            fail(f"{eid}: validity condition missing")

    return {
        "covered_source_groups": sorted(covered_groups),
        "covered_equations": sorted(covered_equations),
        "covered_core2_challenges": sorted({q for c in chapter["concepts"] for q in c.get("core2_challenges", [])}),
    }


def compile_plan(source, chapter, linkage):
    coverage = validate(source, chapter, linkage)
    equations = index(source["equations"])
    question_rows = {row["challenge_id"]: row for row in linkage.get("challenge_links") or []}

    concepts = []
    for order, concept in enumerate(chapter["concepts"], 1):
        eqs = []
        for eid in concept.get("equation_ids", []):
            src = equations[eid]
            eqs.append({
                "equation_id": eid,
                "learner_name": src["learner_name"],
                "expression": src["canonical_expression"],
                "when_you_can_use_it": src["valid_when"],
                "source_locator": src["source_locator"],
            })

        qlinks = []
        for qid in concept.get("core2_challenges", []):
            row = question_rows[qid]
            qlinks.append({
                "challenge_id": qid,
                "challenge_title": row["challenge_title"],
                "prompt_page": row.get("core2_prompt_page"),
                "learner_label": f"Try Core (2): {qid}",
            })

        concepts.append({
            "order": order,
            "concept_id": concept["concept_id"],
            "title": concept["learner_title"],
            "difficulty": concept["difficulty"],
            "difficulty_label": {
                "D1": "Foundation", "D2": "Think carefully", "D3": "Challenge", "D4": "Stretch"
            }[concept["difficulty"]],
            "source_group_ids": concept.get("source_group_ids", []),
            "plain_language": concept["plain_language"],
            "physics_words": concept.get("physics_words", []),
            "model_notes": concept.get("model_notes", []),
            "equations": eqs,
            "illustration": concept["illustration"],
            "easy_mistake_to_make": concept["easy_mistake"],
            "where_you_will_use_this": qlinks,
            "source_examples": concept.get("source_examples", []),
            "build_status": concept["build_status"],
        })

    plan = {
        "schema_version": "1.0.0",
        "product": "CORE_STUDY_GUIDE",
        "chapter_id": chapter["chapter_id"],
        "chapter_title": chapter["chapter_title"],
        "build_scope": chapter["build_scope"],
        "learner_ui": {
            "difficulty_labels": {"D1":"Foundation","D2":"Think carefully","D3":"Challenge","D4":"Stretch"},
            "question_section": "Where you will use this",
            "practice_action": "Try Core (2)",
            "refresh_label": "Need a quick refresher?",
            "mistake_label": "Easy mistake to make"
        },
        "coverage": coverage,
        "concepts": concepts,
        "source_inventory_digest": sha256(source),
        "chapter_registry_digest": sha256(chapter),
        "core2_linkage_digest": sha256(linkage),
    }
    plan["plan_digest"] = sha256(plan)
    return plan


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=Path("motion-in-a-plane-core1a-chapter-plan.json"))
    args = ap.parse_args()

    source = load(SOURCE)
    chapter = load(CHAPTER)
    linkage = load(CORE2)
    plan = compile_plan(source, chapter, linkage)
    args.out.write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(
        "PASS Motion in a Plane first build: "
        f"{len(plan['concepts'])} concepts, "
        f"{len(plan['coverage']['covered_source_groups'])} source groups, "
        f"{len(plan['coverage']['covered_equations'])} equations"
    )


if __name__ == "__main__":
    main()
