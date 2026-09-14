import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIXTURE_DIR = (
    HERE.parent
    / "golden"
    / "all_core_trial"
    / "equidistant-point-on-axis"
)
BLOCKED_FIXTURE = FIXTURE_DIR / "trial.json"
OWNER_RUN = FIXTURE_DIR / "owner-waived-run.json"
OWNER_SPEC = FIXTURE_DIR / "owner-waived-generation-spec.json"
VALIDATOR = HERE.parent / "engine" / "validate_self_teaching_generation_spec.py"

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


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_same_subtopic_runs_through_all_six_cores():
    doc = load(BLOCKED_FIXTURE)
    assert doc["subtopic"]["subtopic_id"] == "MATH-EQUIDISTANT-POINT-ON-AXIS"
    for key in ("core1", "core1a", "core1b", "core2", "core2a", "core2b"):
        assert key in doc


def test_core1_series_is_medium_and_learner_percent_independent():
    doc = load(BLOCKED_FIXTURE)
    assert doc["subtopic"]["difficulty_badge"] == "MEDIUM"
    assert doc["core1a"]["difficulty_badge"] == "MEDIUM"
    assert doc["core1b"]["difficulty_badge"] == "MEDIUM"
    assert doc["core1a"]["learner_knowledge_consulted"] is False
    assert doc["core1b"]["learner_knowledge_consulted"] is False
    assert doc["core1a"]["max_pages"] == 20
    assert doc["core1a"]["target_page_budget"] <= 20


def test_medium_requires_research_and_subsubtopic_depth():
    doc = load(BLOCKED_FIXTURE)
    c1a = doc["core1a"]
    assert c1a["pedagogy_web_search_required"] is True
    assert c1a["web_search_depth"] == "STANDARD"
    assert c1a["research_brief_ref"]
    assert len(c1a["pedagogy_web_research_refs"]) >= 1
    assert len(c1a["subsubtopics"]) >= 2
    assert len(c1a["representation_requirements"]) >= 2


def test_core1b_adds_no_new_math():
    doc = load(BLOCKED_FIXTURE)
    assert doc["core1b"]["new_math_refs"] == []
    approved = {c["capability_id"] for c in doc["core1"]["capabilities"]}
    assert set(doc["core1b"]["approved_capability_refs"]).issubset(approved)


def test_core2_uses_only_core1_approved_knowledge():
    doc = load(BLOCKED_FIXTURE)
    approved = {c["capability_id"] for c in doc["core1"]["capabilities"]}
    assert set(doc["core2"]["required_knowledge"]).issubset(approved)


def test_missing_calibration_still_fails_closed():
    doc = load(BLOCKED_FIXTURE)
    run = doc["production_run"]
    assert run["learner_knowledge_percent"] is None
    assert run["owner_waiver"] is None
    assert doc["core2a"]["production_status"] == "BLOCKED_MISSING_KNOWLEDGE_CALIBRATION"
    assert doc["core2a"]["compiled_legal_pool"] is None
    assert doc["core2b"]["production_status"] == "BLOCKED_UPSTREAM_CORE2A_NOT_READY"
    assert doc["core2b"]["compiled_product"] is None


def test_owner_waiver_generation_spec_passes_canonical_validator():
    proc = subprocess.run(
        [sys.executable, str(VALIDATOR), "--input", str(OWNER_SPEC)],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(proc.stdout)
    assert payload["status"] == "PASS"
    assert payload["core2_calibration"] == "OWNER_WAIVER"
    assert payload["core2a_support_profile"] == "REDUCED_SUPPORT"
    assert payload["core2a_max_demand_level"] == "M4_HIDDEN_STRUCTURE"
    assert payload["core2b_max_demand_level"] == "M4_HIDDEN_STRUCTURE"


def test_owner_waiver_completes_all_six_cores_without_faking_learner_evidence():
    doc = load(OWNER_RUN)
    assert doc["subtopic_id"] == "MATH-EQUIDISTANT-POINT-ON-AXIS"
    assert doc["calibration"]["learner_knowledge_percent"] is None
    assert doc["calibration"]["owner_waiver"] is not None
    assert doc["calibration"]["is_learner_evidence"] is False
    assert doc["calibration"]["is_mastery_claim"] is False
    assert doc["core1"]["status"] == "AUTHORITY_READY"
    assert doc["core1a"]["status"] == "ASSIMILATION_COMPILED"
    assert doc["core1b"]["status"] == "STATIC_CONSOLIDATION_COMPILED"
    assert doc["core2"]["status"] == "ASSESSMENT_INTELLIGENCE_READY"
    assert doc["core2a"]["status"] == "LEGAL_POOL_COMPILED"
    assert doc["core2b"]["status"] == "STATIC_TRANSFER_COMPILED"
    assert doc["run_audit"]["status"] == "PASS"


def test_owner_waived_core2a_and_core2b_respect_m4_ceiling_and_legality():
    doc = load(OWNER_RUN)
    c2a = doc["core2a"]
    c2b = doc["core2b"]
    ceiling_i = LEVELS.index(c2a["max_demand_level"])
    legal_ids = set()
    for item in c2a["legal_items"]:
        legal_ids.add(item["item_id"])
        assert LEVELS.index(item["demand_level"]) <= ceiling_i
    assert c2b["compile_ceiling"] == c2a["max_demand_level"]
    assert set(c2b["selected_item_ids"]).issubset(legal_ids)
    assert c2b["delivery_mode"] == "STATIC"
    assert c2b["runtime_adaptation"] is False
    assert c2b["learner_state_transition"] is False


def test_owner_waived_answers_are_mathematically_consistent():
    doc = load(OWNER_RUN)
    assert doc["core1a"]["worked_anchor"]["answer"] == "P=(9/4,0)"
    x = 9 / 4
    pa2 = (x + 1) ** 2 + 16
    pb2 = (x - 7) ** 2 + 4
    assert pa2 == pb2 == 425 / 16

    hidden = next(x for x in doc["core2a"]["legal_items"] if x["item_id"] == "EQ-H1")
    assert hidden["answer_check"] == "P=(1/4,0)."
    x = 1 / 4
    left = (x + 3) ** 2 + 16
    right = (x - 5) ** 2 + 4
    assert left == right == 425 / 16

    inverse = next(x for x in doc["core2a"]["legal_items"] if x["item_id"] == "EQ-I1")
    assert inverse["answer_check"] == "k=2±sqrt(21)."


def test_original_engineering_simulation_remains_nonpublishable():
    doc = load(BLOCKED_FIXTURE)
    sim = doc["engineering_simulation"]
    assert sim["test_only"] is True
    assert sim["not_learner_evidence"] is True
    assert sim["not_publishable"] is True
