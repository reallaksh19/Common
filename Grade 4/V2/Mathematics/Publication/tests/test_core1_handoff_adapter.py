import copy

import pytest

from Primary.V2.Mathematics.Publication.engine.authoring_handoff_adapter import (
    AuthoringHandoffAdapter,
    AuthoringHandoffPublicationError,
)
from Primary.V2.Mathematics.Publication.tests.test_authoring_handoff_adapter import _handoff


def _core1_handoff():
    handoff = copy.deepcopy(_handoff())
    handoff["authoring_result"] = {
        "skill_model": {
            "concepts": [
                {
                    "concept_id": "CONCEPT-RATE",
                    "title": "Same-rate scaling"
                }
            ]
        },
        "core1_plan": {
            "modules": [
                {
                    "module_id": "C1-RATE",
                    "concept_ref": "CONCEPT-RATE",
                    "concept_mode": "CONNECT",
                    "objective": "Connect the money scale factor to the object-count scale factor.",
                    "learner_action": "Show the same scale factor on both quantities.",
                    "source_refs": ["Q-RATE-01"]
                }
            ]
        }
    }
    return handoff


def test_core1_handoff_exposes_validated_representation_plan_without_old_sections():
    result = AuthoringHandoffAdapter.build_core1_items(_core1_handoff())
    assert result["planned_module_count"] == 1
    assert result["probe_module_count"] == 0
    item = result["items"][0]
    assert item["module_id"] == "C1-RATE"
    assert item["concept_title"] == "Same-rate scaling"
    assert item["objective"].startswith("Connect the money")
    assert item["learning_representation_plan"]["task_ref"] == "C1-RATE"
    assert "sections" not in item
    assert "primitive_call" not in item


def test_core1_handoff_fails_if_support_rows_do_not_match_modules():
    handoff = _core1_handoff()
    handoff["module_support"][0]["module_id"] = "C1-OTHER"
    with pytest.raises(AuthoringHandoffPublicationError) as exc:
        AuthoringHandoffAdapter.build_core1_items(handoff)
    assert exc.value.code == "CORE1_HANDOFF_COVERAGE_INCOMPLETE"


def test_core1_probe_is_explicitly_exempt_from_guided_plan():
    handoff = _core1_handoff()
    handoff["authoring_result"]["core1_plan"]["modules"][0]["concept_mode"] = "PROBE"
    row = handoff["module_support"][0]
    row["support_status"] = "INDEPENDENT_PROBE_ONLY"
    row["learning_representation_plan"] = None
    row["fresh_retry_prompt"] = None
    result = AuthoringHandoffAdapter.build_core1_items(handoff)
    assert result["planned_module_count"] == 0
    assert result["independent_probe_module_ids"] == ["C1-RATE"]
