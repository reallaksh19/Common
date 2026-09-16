#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine" / "build_motion_in_a_plane_chapter.py"
REG = ROOT / "registry"

spec = importlib.util.spec_from_file_location("m2d_builder", ENGINE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

source = json.loads((REG / "physics-core1a-motion-in-a-plane-source-inventory.json").read_text(encoding="utf-8"))
chapter = json.loads((REG / "physics-core1a-motion-in-a-plane-chapter-v1.json").read_text(encoding="utf-8"))
linkage = json.loads((REG / "physics-core1a-core2-linkage.json").read_text(encoding="utf-8"))

plan = mod.compile_plan(source, chapter, linkage)

assert plan["product"] == "CORE_STUDY_GUIDE"
assert plan["build_scope"].endswith("before §6.1 Motion of Boat in a Stream.")
assert len(plan["concepts"]) >= 10
assert len(plan["coverage"]["covered_source_groups"]) >= 11
assert len(plan["coverage"]["covered_equations"]) >= 16

# Learner-facing vocabulary must stay child-friendly.
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

# Difficulty is an actual support rule, not decoration.
minimum_stages = {"D1": 2, "D2": 3, "D3": 3, "D4": 3}
for concept in plan["concepts"]:
    assert len(concept["illustration"]["stages"]) >= minimum_stages[concept["difficulty"]]

# Equation coverage means name + expression + validity, not just a formula string.
for concept in plan["concepts"]:
    for eq in concept["equations"]:
        assert eq["learner_name"]
        assert eq["expression"]
        assert eq["when_you_can_use_it"]
        assert eq["source_locator"]

# Every Core2 link in the plan resolves to the ready Core2 registry.
valid_qids = {row["challenge_id"] for row in linkage["challenge_links"]}
for concept in plan["concepts"]:
    for link in concept["where_you_will_use_this"]:
        assert link["challenge_id"] in valid_qids
        assert link["learner_label"].startswith("Try Core (2):")

print(
    "PASS first Motion in a Plane build: "
    f"{len(plan['concepts'])} concepts / "
    f"{len(plan['coverage']['covered_source_groups'])} source groups / "
    f"{len(plan['coverage']['covered_equations'])} equations"
)
