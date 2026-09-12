#!/usr/bin/env python3
"""Compile river, rain and circular-motion Core (1A) concepts.

This is the second source-locked Motion in a Plane build. It begins at §6.1 after the
first build's Relative Motion concept and continues through §7.3. The compiler merges
the seed source inventory with a small source-supplement ledger so formula-sheet and
derivation relations cannot disappear between source reading and learner publication.
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
SUPPLEMENT = REG / "physics-core1a-motion-in-a-plane-source-supplement-v1.json"
FIRST = REG / "physics-core1a-motion-in-a-plane-chapter-v1.json"
NEXT = REG / "physics-core1a-motion-in-a-plane-next-topics-v1.json"
CORE2 = REG / "physics-core1a-core2-linkage.json"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def canonical(obj):
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def sha256(obj):
    return hashlib.sha256(canonical(obj).encode("utf-8")).hexdigest()


def index(rows):
    return {row["id"]: row for row in rows}


def fail(message):
    raise ValueError(message)


def merged_equations(source, supplement):
    rows = list(source.get("equations") or []) + list(supplement.get("equations") or [])
    ids = [r["id"] for r in rows]
    if len(ids) != len(set(ids)):
        dupes = sorted({x for x in ids if ids.count(x) > 1})
        fail("duplicate equation ids across source ledgers: " + ", ".join(dupes))
    return index(rows)


def validate(source, supplement, first, nxt, linkage):
    groups = index(source["source_groups"])
    equations = merged_equations(source, supplement)
    illustrations = index(source.get("worked_illustrations") or [])
    valid_qids = {row["challenge_id"] for row in linkage.get("challenge_links") or []}
    known_concepts = {c["concept_id"] for c in first["concepts"]} | {c["concept_id"] for c in nxt["concepts"]}

    seen = set()
    for concept in nxt["concepts"]:
        cid = concept["concept_id"]
        if cid in seen:
            fail(f"duplicate concept_id: {cid}")
        seen.add(cid)

        if concept["difficulty"] not in {"D1", "D2", "D3", "D4"}:
            fail(f"{cid}: invalid difficulty")
        if concept.get("build_status") not in {"PLANNED", "BUILT", "VERIFIED"}:
            fail(f"{cid}: invalid build_status")
        if not concept.get("plain_language"):
            fail(f"{cid}: plain-language explanation missing")
        if not concept.get("illustration", {}).get("stages"):
            fail(f"{cid}: staged illustration missing")
        if not concept.get("easy_mistake"):
            fail(f"{cid}: easy-mistake support missing")

        min_stages = {"D1": 2, "D2": 3, "D3": 3, "D4": 3}[concept["difficulty"]]
        if len(concept["illustration"]["stages"]) < min_stages:
            fail(f"{cid}: {concept['difficulty']} needs at least {min_stages} stages")

        for dep in concept.get("prerequisite_concepts", []):
            if dep not in known_concepts:
                fail(f"{cid}: unknown prerequisite concept {dep}")
        for gid in concept.get("source_group_ids", []):
            if gid not in groups:
                fail(f"{cid}: unknown source group {gid}")
        for eid in concept.get("equation_ids", []):
            if eid not in equations:
                fail(f"{cid}: unknown source equation {eid}")
        for iid in concept.get("source_examples", []):
            if iid not in illustrations:
                fail(f"{cid}: unknown source illustration {iid}")
        for qid in concept.get("core2_challenges", []):
            if qid not in valid_qids:
                fail(f"{cid}: unknown Revised Core (2) challenge {qid}")

        if not concept.get("core2_challenges") and concept.get("question_link_status") != "NO_DIRECT_MATCH_IN_REVISED_CORE2_V2":
            fail(f"{cid}: concepts without a Core2 question must say why no forward link is shown")

    required_groups = {
        "SRC-G6.1", "SRC-G6.1.1", "SRC-G6.1.2", "SRC-G6.1.3", "SRC-G6.1.4",
        "SRC-G6-RAIN", "SRC-G7", "SRC-G7.1", "SRC-G7.2", "SRC-G7.3"
    }
    covered_groups = {gid for c in nxt["concepts"] for gid in c.get("source_group_ids", [])}
    missing_groups = sorted(required_groups - covered_groups)
    if missing_groups:
        fail("next-topic source groups missing: " + ", ".join(missing_groups))

    build_homes = {
        "RIVER_FOUNDATION", "RIVER_RESULTANT", "RIVER_CROSSING_TIME", "RIVER_DRIFT",
        "RIVER_SHORTEST_TIME", "RIVER_ZERO_DRIFT", "RAIN_APPARENT_MOTION",
        "CIRCULAR_ANGULAR_LINEAR", "CIRCULAR_UNIFORM", "CIRCULAR_NONUNIFORM"
    }
    required_equations = {
        eid for eid, row in equations.items()
        if row.get("core1a_home") in build_homes and row.get("must_be_taught") is True
    }
    covered_equations = {eid for c in nxt["concepts"] for eid in c.get("equation_ids", [])}
    missing_equations = sorted(required_equations - covered_equations)
    if missing_equations:
        fail("next-topic source equations missing: " + ", ".join(missing_equations))

    for eid in covered_equations:
        if not equations[eid].get("valid_when"):
            fail(f"{eid}: validity condition missing")

    required_illustrations = {
        "M2D-ILL-12", "M2D-ILL-13", "M2D-ILL-14-RAIN", "M2D-ILL-14-CIRC",
        "M2D-ILL-15", "M2D-ILL-16", "M2D-ILL-17", "M2D-ILL-18"
    }
    covered_illustrations = {iid for c in nxt["concepts"] for iid in c.get("source_examples", [])}
    missing_illustrations = sorted(required_illustrations - covered_illustrations)
    if missing_illustrations:
        fail("next-topic source illustrations missing: " + ", ".join(missing_illustrations))

    return {
        "covered_source_groups": sorted(covered_groups),
        "covered_equations": sorted(covered_equations),
        "covered_source_illustrations": sorted(covered_illustrations),
        "covered_core2_challenges": sorted({q for c in nxt["concepts"] for q in c.get("core2_challenges", [])}),
    }


def compile_plan(source, supplement, first, nxt, linkage):
    coverage = validate(source, supplement, first, nxt, linkage)
    equations = merged_equations(source, supplement)
    question_rows = {row["challenge_id"]: row for row in linkage.get("challenge_links") or []}

    concepts = []
    for order, concept in enumerate(nxt["concepts"], 1):
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
            "difficulty_label": {"D1":"Foundation","D2":"Think carefully","D3":"Challenge","D4":"Stretch"}[concept["difficulty"]],
            "prerequisite_concepts": concept.get("prerequisite_concepts", []),
            "source_group_ids": concept.get("source_group_ids", []),
            "plain_language": concept["plain_language"],
            "physics_words": concept.get("physics_words", []),
            "model_notes": concept.get("model_notes", []),
            "equations": eqs,
            "illustration": concept["illustration"],
            "easy_mistake_to_make": concept["easy_mistake"],
            "source_examples": concept.get("source_examples", []),
            "where_you_will_use_this": qlinks,
            "core2_link_status": concept.get("question_link_status"),
            "build_status": concept["build_status"],
        })

    plan = {
        "schema_version": "1.0.0",
        "product": "CORE_STUDY_GUIDE",
        "chapter_id": nxt["chapter_id"],
        "chapter_title": nxt["chapter_title"],
        "build_scope": nxt["build_scope"],
        "learner_ui": {
            "difficulty_labels": {"D1":"Foundation","D2":"Think carefully","D3":"Challenge","D4":"Stretch"},
            "question_section": "Where you will use this",
            "practice_action": "Try Core (2)",
            "refresh_label": "Need a quick refresher?",
            "mistake_label": "Easy mistake to make",
            "empty_core2_link_rule": "Hide the Core (2) box when the revised 59-question set has no matching item; never invent a question link."
        },
        "coverage": coverage,
        "concepts": concepts,
        "source_inventory_digest": sha256(source),
        "source_supplement_digest": sha256(supplement),
        "chapter_registry_digest": sha256(nxt),
        "core2_linkage_digest": sha256(linkage),
    }
    plan["plan_digest"] = sha256(plan)
    return plan


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=Path("motion-in-a-plane-core1a-next-topics-plan.json"))
    args = ap.parse_args()

    source = load(SOURCE)
    supplement = load(SUPPLEMENT)
    first = load(FIRST)
    nxt = load(NEXT)
    linkage = load(CORE2)
    plan = compile_plan(source, supplement, first, nxt, linkage)
    args.out.write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(
        "PASS Motion in a Plane next topics: "
        f"{len(plan['concepts'])} concepts, "
        f"{len(plan['coverage']['covered_source_groups'])} source groups, "
        f"{len(plan['coverage']['covered_equations'])} equations, "
        f"{len(plan['coverage']['covered_source_illustrations'])} source illustrations"
    )


if __name__ == "__main__":
    main()
