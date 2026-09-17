#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine" / "build_motion_in_a_plane_next_topics.py"
REG = ROOT / "registry"

spec = importlib.util.spec_from_file_location("m2d_next_builder", ENGINE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

source = json.loads((REG / "physics-core1a-motion-in-a-plane-source-inventory.json").read_text(encoding="utf-8"))
supplement = json.loads((REG / "physics-core1a-motion-in-a-plane-source-supplement-v1.json").read_text(encoding="utf-8"))
first = json.loads((REG / "physics-core1a-motion-in-a-plane-chapter-v1.json").read_text(encoding="utf-8"))
nxt = json.loads((REG / "physics-core1a-motion-in-a-plane-next-topics-v1.json").read_text(encoding="utf-8"))
linkage = json.loads((REG / "physics-core1a-core2-linkage.json").read_text(encoding="utf-8"))

plan = mod.compile_plan(source, supplement, first, nxt, linkage)

assert plan["product"] == "CORE_STUDY_GUIDE"
assert len(plan["concepts"]) >= 12
assert len(plan["coverage"]["covered_source_groups"]) >= 10
assert len(plan["coverage"]["covered_equations"]) >= 20
assert len(plan["coverage"]["covered_source_illustrations"]) == 8

# Child-facing nomenclature must remain free of internal workflow language.
banned = {"repair", "remediation", "custody", "falsifier", "source-grounded"}
for concept in plan["concepts"]:
    learner_surface = " ".join([
        concept["title"],
        *concept["plain_language"],
        *concept["physics_words"],
        *concept["model_notes"],
        concept["easy_mistake_to_make"],
        *[stage["title"] + " " + stage["learner_question"] for stage in concept["illustration"]["stages"]],
    ]).lower()
    for word in banned:
        assert word not in learner_surface, f"{concept['concept_id']}: banned learner word {word}"

# Difficulty must change the amount of visual scaffolding.
minimum_stages = {"D1": 2, "D2": 3, "D3": 3, "D4": 3}
for concept in plan["concepts"]:
    assert len(concept["illustration"]["stages"]) >= minimum_stages[concept["difficulty"]]

# Every taught equation must carry name, expression, validity and source locator.
for concept in plan["concepts"]:
    for eq in concept["equations"]:
        assert eq["learner_name"]
        assert eq["expression"]
        assert eq["when_you_can_use_it"]
        assert eq["source_locator"]

# Concept linkage must be resolvable, including the bridge from the first build.
all_ids = {c["concept_id"] for c in first["concepts"]} | {c["concept_id"] for c in nxt["concepts"]}
for concept in plan["concepts"]:
    for dep in concept["prerequisite_concepts"]:
        assert dep in all_ids

# Revised Core (2) v2 has no direct river/rain/circular challenge in its 59 retained source items.
# The learner PDF must therefore hide rather than fabricate a Core (2) button for these concepts.
for concept in plan["concepts"]:
    if not concept["where_you_will_use_this"]:
        assert concept["core2_link_status"] == "NO_DIRECT_MATCH_IN_REVISED_CORE2_V2"

# The hard river/circular concepts must have explicit contrast or derivation staging.
by_id = {c["concept_id"]: c for c in plan["concepts"]}
assert by_id["RIVER_SHORTEST_TIME"]["illustration"]["archetype"] == "COMPARE"
assert by_id["CIRCULAR_ANGULAR_LINEAR"]["illustration"]["archetype"] == "DERIVATION_BRIDGE"
assert by_id["CIRCULAR_UNIFORM"]["difficulty"] == "D3"
assert by_id["CIRCULAR_NONUNIFORM"]["difficulty"] == "D3"

print(
    "PASS next Motion in a Plane build: "
    f"{len(plan['concepts'])} concepts / "
    f"{len(plan['coverage']['covered_source_groups'])} source groups / "
    f"{len(plan['coverage']['covered_equations'])} equations / "
    f"{len(plan['coverage']['covered_source_illustrations'])} source illustrations"
)
