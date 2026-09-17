#!/usr/bin/env python3
"""Falsifiers for the non-runtime Shared LearningEngineering architecture roadmap."""
import json
import runpy
from pathlib import Path

from jsonschema import Draft202012Validator

HERE = Path(__file__).resolve()
ROOT = HERE.parents[1]
REPO = HERE.parents[5]


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


schema = load(ROOT / "contracts" / "skp-schema-roadmap.schema.json")
roadmap = load(ROOT / "registry" / "skp-schema-roadmap.v1.json")
errors = sorted(Draft202012Validator(schema).iter_errors(roadmap), key=lambda e: list(e.path))
assert not errors, f"roadmap schema: {errors[0].message} at {list(errors[0].path)}"

assert roadmap["authority_state"] == "NON_RUNTIME_DESIGN_AUTHORITY"
assert roadmap["bulk_population_allowed"] is False
assert roadmap["bulk_population_state"] == "BLOCKED_UNTIL_DIVERSITY_PILOTS_AND_SCHEMA_ACTIVATION"

module_ids = [m["module_id"] for m in roadmap["modules"]]
assert len(module_ids) == len(set(module_ids)), "duplicate module IDs"
module_set = set(module_ids)
expected_pilot_modules = {
    "SKP-IDENTITY",
    "SKP-SCOPE",
    "SKP-CURRICULUM-BINDING",
    "SKP-CAPABILITY",
    "SKP-PREREQUISITE-EDGE",
    "SKP-SOURCE-PLAN",
    "SKP-SOURCE-RECORD",
}
pilot_modules = {m["module_id"] for m in roadmap["modules"] if m["status"] == "PILOT"}
assert pilot_modules == expected_pilot_modules, pilot_modules
for module in roadmap["modules"]:
    assert module["runtime_authority"] is False, module["module_id"]
    assert module["status"] in {"PLANNED", "PILOT"}, module["module_id"]
    assert set(module["depends_on"]) <= module_set, (module["module_id"], module["depends_on"])
    target = ROOT / module["target_contract"]
    if module["status"] == "PILOT":
        assert target.exists(), f"PILOT roadmap contract missing: {target}"
    else:
        assert not target.exists(), f"PLANNED roadmap contract materialized without status change: {target}"

# Shared kernel must remain case-neutral. Topic fixtures are legal in pilot data, not module semantics.
shared_text = json.dumps(roadmap["modules"], sort_keys=True).upper()
for forbidden in ("M2D", "SBA04", "SBA23", "Q14", "Q27", "RELATIVE MOTION"):
    assert forbidden not in shared_text, forbidden

subjects = {x["subject"] for x in roadmap["subject_adapters"]}
assert subjects == {"PHYSICS", "MATHEMATICS", "CHEMISTRY"}
pilot_ids = {p["pilot_id"] for p in roadmap["pilots"]}
assert len(pilot_ids) == len(roadmap["pilots"])
assert len(roadmap["pilots"]) >= 4
for adapter in roadmap["subject_adapters"]:
    assert adapter["runtime_authority"] is False
    assert adapter["status"] == "PLANNED"
    assert set(adapter["pilot_refs"]) <= pilot_ids
    assert (REPO / adapter["current_authority_manifest_ref"]).exists(), adapter["current_authority_manifest_ref"]
for pilot in roadmap["pilots"]:
    assert pilot["status"] == "PLANNED"
    assert pilot["bulk_population_gate"] is True

invariants = {x["invariant_id"] for x in roadmap["global_invariants"]}
required_invariants = {
    "LE-ENGINEERING-ABOVE-BLUEPRINT",
    "LE-ORDINARY-SUBTOPIC-DATA",
    "LE-NO-MEMORY-AUTHORITY",
    "LE-LEARNER-DOMAIN-SEPARATION",
    "LE-DEPTH-LEARNER-SEPARATION",
    "LE-SOURCE-NOT-AUTHORITY",
    "LE-PROVENANCE-NOT-TRUTH",
    "LE-PUBLICATION-INDEPENDENT",
    "LE-SCHEMA-NOT-SEMANTICS",
    "LE-PROGRESSION-EVIDENCE",
}
assert required_invariants <= invariants

architecture = (ROOT / "V2_LEARNING_ENGINEERING_ARCHITECTURE.md").read_text(encoding="utf-8")
ontology = (ROOT / "SUBTOPIC_KNOWLEDGE_MODEL.md").read_text(encoding="utf-8")
sources = (ROOT / "SOURCE_GOVERNANCE.md").read_text(encoding="utf-8")
roadmap_doc = (ROOT / "SKP_SCHEMA_ROADMAP.md").read_text(encoding="utf-8")

for phrase in (
    "An ordinary new subtopic must not require a Blueprint code change",
    "Engineering Gate > Blueprint",
    "Schema validity is necessary, not sufficient",
    "ENGINEERING_DEPTH != LEARNER_STATE",
    "Known limitations and risks",
    "Physics adapter",
    "Mathematics adapter",
    "Chemistry adapter",
):
    assert phrase in architecture, phrase
for phrase in (
    "HYPOTHESIZED_PROGRESSION",
    "EMPIRICALLY_SUPPORTED_PROGRESSION",
    "MISCONCEPTION",
    "CONTEXTUAL_RESOURCE",
    "NOT_APPLICABLE",
    "UNRESOLVED",
):
    assert phrase in ontology, phrase
for phrase in (
    "SOURCE != AUTHORITY",
    "CURRICULUM_AUTHORITY",
    "MISCONCEPTION_EVIDENCE",
    "Provenance is not truth",
):
    assert phrase in sources, phrase
for phrase in (
    "Bulk library population: **BLOCKED**",
    "Physics Relative Motion",
    "Physics Thermodynamics",
    "Mathematics geometry or trigonometry",
    "Chemistry atomic/bonding/reaction",
):
    assert phrase in roadmap_doc, phrase

# The roadmap itself is not a hidden production promotion mechanism.
assert "ACTIVE" in json.dumps(schema), "lifecycle supports future ACTIVE state"
assert not any(m["status"] == "ACTIVE" for m in roadmap["modules"])
assert not any(a["status"] == "ACTIVE" for a in roadmap["subject_adapters"])

# Foundational PILOT contracts are exercised through a synthetic topic-neutral fixture and negative falsifiers.
runpy.run_path(str(ROOT / "tests" / "test_skp_pilot_kernel.py"), run_name="__main__")

# The next semantic tranche remains prototype-only but must be executable, case-neutral in schema,
# and able to project exact existing Physics authority without fabricating unresolved curriculum/pedagogy.
runpy.run_path(str(ROOT / "tests" / "test_skp_semantic_prototype.py"), run_name="__main__")

# Non-Physics repository authority must challenge shared shapes before promotion. These tests
# specifically reject placeholder relations/representations where Math/Chemistry do not own them.
runpy.run_path(str(ROOT / "tests" / "test_skp_cross_subject_prototype_fit.py"), run_name="__main__")

print(
    "Shared LearningEngineering architecture: PASS "
    f"({len(pilot_modules)} pilot modules / {len(module_ids) - len(pilot_modules)} planned modules, "
    f"{len(roadmap['subject_adapters'])} planned subject adapters, "
    f"{len(roadmap['pilots'])} diversity pilots; bulk population remains BLOCKED)"
)
