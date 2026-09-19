"""Lossless, composition-only publication plans with truthful release state."""

from __future__ import annotations

from .contracts import digest, require


def compile_publication(packets: dict, context: dict) -> dict:
    reviewed = packets["PRACTICE_REVIEW"]["payload"]["items"]
    require(all(x["decision"] == "ACCEPT" for x in reviewed), "QUESTION_REWORK_REQUIRED")
    manuscript = packets["MANUSCRIPT"]["payload"]
    practice = packets["PRACTICE_ELIGIBILITY"]["payload"]
    teaching_units = [{"unit_id": x["section_id"], "source_role": "CORE1A",
                       "content_digest": digest(x), "content": x} for x in manuscript["sections"]]
    question_units = [_question_unit(x, context["request"]["practice"]) for x in practice["items"]]
    ids = [x["unit_id"] for x in teaching_units + question_units]
    require(len(ids) == len(set(ids)), "PUBLICATION_UNIT_ID_COLLISION")
    return {"subject": context["request"]["subject"], "topic": context["request"]["topic"],
            "request_digest": context["request_digest"], "manifest_digest": context["manifest"]["manifest_digest"],
            "authority": {"semantic_authority": "UPSTREAM_ONLY", "renderer_authority": "COMPOSITION_ONLY",
                          "may_introduce_claims": False, "may_substitute_representations": False},
            "teaching_units": teaching_units, "question_units": question_units,
            "source_custody": practice["source_custody"],
            "machine_state": "SEMANTIC_IR_READY_RENDER_PENDING", "render_validation": "NOT_RUN",
            "human_gates": {x: "PENDING" for x in ("subject", "pedagogy", "assessment", "visual_usability")},
            "release_authorized": False, "run_kind": context["request"]["run_kind"]}


def _question_unit(question: dict, policy: dict) -> dict:
    require(policy["max_pages_per_question"] == 2, "ATTEMPT_ANSWER_SEPARATION_NEEDS_TWO_PAGES")
    hints = question.get("hints", [])
    visible = policy["hint_visibility"] == "VISIBLE_TECHNICAL"
    require(not (question["support_mode"] == "INDEPENDENT" and hints), "INDEPENDENCE_LABEL_DRIFT")
    attempt = {"page_role": "ATTEMPT", "provenance": question["provenance"],
               "stem": question["stem"], "options": question.get("options", []),
               "subparts": question.get("subparts", []), "figures": question.get("figures", []),
               "conditions": question.get("conditions", []),
               "workspace_mm": question.get("workspace_mm", 45),
               "hints": hints if visible else []}
    answer = {"page_role": "CHECK_AND_REPAIR", "answer": question["answer"],
              "optional_hints": hints if not visible else []}
    return {"unit_id": question["question_id"], "source_role": "CORE2A",
            "content_digest": digest(question), "content": question,
            "pages": [attempt, answer], "physical_page_count_verified": False}


def validate_publication(ir: dict, packets: dict) -> None:
    expected = {x["section_id"]: x for x in packets["MANUSCRIPT"]["payload"]["sections"]}
    expected.update({x["question_id"]: x for x in packets["PRACTICE_ELIGIBILITY"]["payload"]["items"]})
    units = ir["teaching_units"] + ir["question_units"]
    require(len(units) == len(expected) and {x["unit_id"] for x in units} == set(expected),
            "PUBLICATION_LOSSLESS_COVERAGE")
    for unit in units:
        require(unit["content"] == expected[unit["unit_id"]] and
                unit["content_digest"] == digest(expected[unit["unit_id"]]), "PUBLICATION_SEMANTIC_MUTATION")
    require(ir["release_authorized"] is False, "MACHINE_CANNOT_AUTHORIZE_RELEASE")
