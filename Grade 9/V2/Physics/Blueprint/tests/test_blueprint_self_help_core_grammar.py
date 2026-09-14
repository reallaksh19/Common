#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUB = json.loads((ROOT / "policy" / "self-help-core-publication.v2.json").read_text())
BUCKET = json.loads((ROOT / "policy" / "core1ab-bucket-depth.v1.json").read_text())
KNOW = json.loads((ROOT / "policy" / "core2ab-knowledge-routing.v1.json").read_text())
PILOT = json.loads((ROOT / "topics" / "self-help-three-topic-falsification-pilot.v2.json").read_text())

cp = PUB["control_planes"]
assert cp["CORE1_FAMILY"]["adaptation_driver"] == "BUCKET_DIFFICULTY_BADGE_ONLY"
assert cp["CORE1_FAMILY"]["student_knowledge_pct_drives_depth"] is False
assert cp["CORE1_FAMILY"]["always_subtopic_bucket_wise"] is True
assert cp["CORE2_FAMILY"]["student_knowledge_pct_required_unless_owner_override"] is True

assert BUCKET["student_knowledge_pct_used_for_depth"] is False
assert BUCKET["page_budget_rule"]["anti_padding"] is True
assert BUCKET["badges"]["EASY"]["soft_page_ceiling"] == 10
assert BUCKET["badges"]["MEDIUM"]["soft_page_ceiling"] == 20
assert BUCKET["badges"]["HARD"]["soft_page_ceiling"] == 30
assert BUCKET["badges"]["EASY"]["web_research_required_for_visual_and_pedagogy_design"] is False
assert BUCKET["badges"]["MEDIUM"]["web_research_required_for_visual_and_pedagogy_design"] is True
assert BUCKET["badges"]["HARD"]["web_research_required_for_visual_and_pedagogy_design"] is True

rir = KNOW["required_input_rule"]
assert rir["no_silent_default"] is True
assert set(rir["selection_basis_enum"]) == {"KNOWLEDGE_PERCENT", "OWNER_OVERRIDE"}
assert rir["KNOWLEDGE_PERCENT"]["range_inclusive"] == [0, 100]
assert set(rir["OWNER_OVERRIDE"]["required_fields"]) == {"owner_ref", "reason", "support_band"}

guards = KNOW["authority_guards"]
assert guards["knowledge_pct_may_expand_core2a_legal_pool"] is False
assert guards["owner_override_may_expand_core2a_legal_pool"] is False
assert guards["owner_override_waives_only_missing_knowledge_pct"] is True

roles = PUB["learner_surface_roles"]
assert roles["CORE1A"]["depth_driver"] == "BUCKET_DIFFICULTY_BADGE"
assert roles["CORE1B"]["depth_driver"] == "BUCKET_DIFFICULTY_BADGE"
assert roles["CORE2A"]["adaptation_driver"] == "STUDENT_KNOWLEDGE_PERCENT_OR_OWNER_OVERRIDE"
assert roles["CORE2B"]["adaptation_driver"] == "STUDENT_KNOWLEDGE_PERCENT_OR_OWNER_OVERRIDE"

for layer in ("CORE1B", "CORE2B"):
    episode = roles[layer]["required_episode"]
    assert episode.index("H1_NOTICE") < episode.index("H2_REPRESENT") < episode.index("H3_START")
    assert "CHECK_AFTER_ATTEMPT" in episode
    assert "REPAIR_ROUTE" in episode

topics = PILOT["topics"]
assert len(topics) == 3
for t in topics:
    assert t["core1ab_bucket_difficulty_badge"] in {"EASY", "MEDIUM", "HARD"}
    inp = t["core2_adaptation_input"]
    assert inp["selection_basis"] in {"KNOWLEDGE_PERCENT", "OWNER_OVERRIDE"}
    if inp["selection_basis"] == "KNOWLEDGE_PERCENT":
        assert 0 <= inp["student_knowledge_pct"] <= 100
    else:
        assert inp["student_knowledge_pct"] is None
        ov = inp["owner_override"]
        assert ov["owner_ref"] and ov["reason"]
        assert ov["support_band"] in rir["OWNER_OVERRIDE"]["support_band_enum"]

moving = next(x for x in topics if x["topic_id"] == "MOVING_LAUNCHER_RELATIVE_VELOCITY")
assert "EXACT_Q15_HELD" in moving["source_status"]
assert moving["core2_adaptation_input"]["selection_basis"] == "OWNER_OVERRIDE"

pc = PILOT["pass_criteria"]
assert pc["core1ab_depth_driven_only_by_bucket_difficulty"] is True
assert pc["core2ab_requires_knowledge_or_owner_override"] is True
assert pc["owner_override_does_not_expand_legality"] is True

print("Physics self-help core grammar v2: PASS")
