import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIXTURE = (
    HERE.parent
    / "golden"
    / "all_core_trial"
    / "equidistant-point-on-axis"
    / "trial.json"
)

LEVELS = [
    "M0_DIRECT",
    "M1_CONTROLLED_VARIATION",
    "M2_REPRESENTATION_TRANSFER",
    "M3_INVERSE_TARGET",
    "M4_HIDDEN_STRUCTURE",
    "M5_METHOD_DISCRIMINATION",
    "M6_FAMILY_DISCRIMINATION",
    "M7_MULTI_STEP_SYNTHESIS",
    "M8_MIXED_COMPETITIVE",
]


def load_fixture():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def test_same_subtopic_runs_through_all_six_cores():
    doc = load_fixture()
    assert doc["subtopic"]["subtopic_id"] == "MATH-EQUIDISTANT-POINT-ON-AXIS"
    for key in ("core1", "core1a", "core1b", "core2", "core2a", "core2b"):
        assert key in doc


def test_core1_series_is_medium_and_learner_percent_independent():
    doc = load_fixture()
    assert doc["subtopic"]["difficulty_badge"] == "MEDIUM"
    assert doc["core1a"]["difficulty_badge"] == "MEDIUM"
    assert doc["core1b"]["difficulty_badge"] == "MEDIUM"
    assert doc["core1a"]["learner_knowledge_consulted"] is False
    assert doc["core1b"]["learner_knowledge_consulted"] is False
    assert doc["core1a"]["max_pages"] == 20
    assert doc["core1a"]["target_page_budget"] <= 20


def test_medium_requires_research_and_subsubtopic_depth():
    doc = load_fixture()
    c1a = doc["core1a"]
    assert c1a["pedagogy_web_search_required"] is True
    assert c1a["web_search_depth"] == "STANDARD"
    assert c1a["research_brief_ref"]
    assert len(c1a["pedagogy_web_research_refs"]) >= 1
    assert len(c1a["subsubtopics"]) >= 2
    assert len(c1a["representation_requirements"]) >= 2


def test_core1b_adds_no_new_math():
    doc = load_fixture()
    assert doc["core1b"]["new_math_refs"] == []
    approved = {c["capability_id"] for c in doc["core1"]["capabilities"]}
    assert set(doc["core1b"]["approved_capability_refs"]).issubset(approved)


def test_core2_uses_only_core1_approved_knowledge():
    doc = load_fixture()
    approved = {c["capability_id"] for c in doc["core1"]["capabilities"]}
    assert set(doc["core2"]["required_knowledge"]).issubset(approved)


def test_real_core2a_core2b_fail_closed_without_calibration():
    doc = load_fixture()
    run = doc["production_run"]
    assert run["learner_knowledge_percent"] is None
    assert run["owner_waiver"] is None
    assert doc["core2a"]["production_status"] == "BLOCKED_MISSING_KNOWLEDGE_CALIBRATION"
    assert doc["core2a"]["compiled_legal_pool"] is None
    assert doc["core2b"]["production_status"] == "BLOCKED_UPSTREAM_CORE2A_NOT_READY"
    assert doc["core2b"]["compiled_product"] is None


def test_engineering_simulation_is_nonpublishable_and_respects_ceiling():
    doc = load_fixture()
    sim = doc["engineering_simulation"]
    assert sim["test_only"] is True
    assert sim["not_learner_evidence"] is True
    assert sim["not_publishable"] is True

    ceiling = sim["synthetic_calibration"]["resolved_core2a_max_demand_level"]
    c2b_ceiling = sim["synthetic_calibration"]["resolved_core2b_max_demand_level"]
    assert ceiling == c2b_ceiling

    ceiling_i = LEVELS.index(ceiling)
    legal_ids = set()
    for item in sim["core2a_compiled"]["legal_items"]:
        legal_ids.add(item["item_id"])
        assert LEVELS.index(item["demand_level"]) <= ceiling_i

    assert set(sim["core2b_compiled"]["selected_item_ids"]).issubset(legal_ids)
    assert sim["core2b_compiled"]["compile_ceiling"] == c2b_ceiling


def test_anchor_solution_is_mathematically_consistent():
    doc = load_fixture()
    anchor = doc["core1a"]["worked_anchor"]
    assert anchor["answer"] == "P=(9/4,0)"
    x = 9 / 4
    pa2 = (x + 1) ** 2 + 16
    pb2 = (x - 7) ** 2 + 4
    assert pa2 == pb2 == 425 / 16
