#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = json.loads((ROOT / "policy" / "self-help-core-publication.v1.json").read_text())
PILOT = json.loads((ROOT / "topics" / "self-help-three-topic-falsification-pilot.v1.json").read_text())

roles = POLICY["learner_surface_roles"]

assert POLICY["universal_self_help_contract"]["every_open_ended_prompt_has_local_resolution"] is True
assert POLICY["universal_self_help_contract"]["repair_route_required_for_nontrivial_failure"] is True

assert roles["CORE1A"]["mode"] == "DECLARATIVE_DEEP_TEACHING"
assert roles["CORE1B"]["mode"] == "GENERATIVE_CONCEPT_COACH"
assert roles["CORE2A"]["mode"] == "DECLARATIVE_WORKED_TRANSFER_ATLAS"
assert roles["CORE2B"]["mode"] == "GENERATIVE_TRANSFER_COACH"

for layer in ("CORE1B", "CORE2B"):
    episode = roles[layer]["required_episode"]
    assert episode.index("H1_NOTICE") < episode.index("H2_REPRESENT") < episode.index("H3_START")
    assert "CHECK_AFTER_ATTEMPT" in episode
    assert "REPAIR_ROUTE" in episode

assert "FULL_WORKING" in roles["CORE2A"]["required_problem_spine"]
assert "COMMON_WRONG_ROUTE" in roles["CORE2A"]["required_problem_spine"]
assert "VARIATION_NOTE" in roles["CORE2A"]["required_problem_spine"]

assert POLICY["authority_boundary"]["core1b_may_author_new_semantics"] is False
assert POLICY["authority_boundary"]["core2b_may_legalize_transfer"] is False
assert POLICY["authority_boundary"]["generated_items_may_replace_frozen_core2_source"] is False

assert POLICY["evidence_boundary"]["core1a_publication_proves_mastery"] is False
assert POLICY["evidence_boundary"]["core2a_worked_solution_proves_transfer"] is False

topics = PILOT["topics"]
assert len(topics) == 3
assert {x["topic_id"] for x in topics} == {
    "PROJECTILE_VERTICAL_EVENT",
    "MOVING_LAUNCHER_RELATIVE_VELOCITY",
    "NEWTON_MODEL_SELECTION",
}
moving = next(x for x in topics if x["topic_id"] == "MOVING_LAUNCHER_RELATIVE_VELOCITY")
assert "EXACT_Q15_HELD" in moving["source_status"]
newton = next(x for x in topics if x["topic_id"] == "NEWTON_MODEL_SELECTION")
assert newton["source_status"] == "DESIGN_ONLY_REQUIRES_FUTURE_CORE1_CORE2_BINDING"

pc = PILOT["pass_criteria"]
assert pc["a_layers_declarative"] is True
assert pc["b_layers_generative_attempt_first"] is True
assert pc["core2_source_immutability_preserved"] is True
assert pc["runtime_authority_guards_unchanged"] is True

print("Physics self-help core grammar: PASS")
