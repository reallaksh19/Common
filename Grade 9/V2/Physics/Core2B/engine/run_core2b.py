from __future__ import annotations

import argparse
import json
from pathlib import Path

from core2b_common import (
    build_core1b_repair_request,
    choose_next_item,
    classify_attempt,
    update_retrieval_state,
    validate_session,
)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--session", required=True)
    parser.add_argument("--escalation-policy", required=True)
    parser.add_argument("--hint-policy", required=True)
    parser.add_argument("--error-taxonomy", required=True)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()

    session = load_json(Path(args.session))
    escalation = load_json(Path(args.escalation_policy))
    hint_policy = load_json(Path(args.hint_policy))
    taxonomy = load_json(Path(args.error_taxonomy))

    validate_session(session, escalation, hint_policy)
    selected = choose_next_item(session, escalation)

    # Golden runner emits a representative correct independent attempt.
    attempt = {
        "schema_version": "0.1.0",
        "attempt_id": "PHY-C2B-GOLDEN-ATTEMPT-01",
        "item_id": selected["item_id"],
        "outcome": "CORRECT",
        "hint_level_used": "NO_HINT",
        "error_classes": [],
        "response_evidence": {
            "model_selected": "VERTICAL_CONSTANT_ACCELERATION",
            "representation_used": selected.get("required_representation"),
            "first_move": "Identify known quantities and target before substitution.",
            "final_answer": "validated by upstream Core2A item contract",
            "physical_check": "result is consistent with downward constant acceleration",
        },
    }
    errors = classify_attempt(attempt, taxonomy)
    repair = build_core1b_repair_request(
        session["learner_profile_ref"],
        selected["required_capability_refs"][0],
        errors,
        taxonomy,
    )

    retrieval = update_retrieval_state(
        {
            "schema_version": "0.1.0",
            "capability_id": selected["required_capability_refs"][0],
            "retrieval_count": session["retrieval_state"]["retrieval_count"],
            "success_streak": 1 if session["retrieval_state"].get("last_result") == "PASS" else 0,
            "hint_dependence": "NONE",
            "representation_coverage": list(session.get("representation_coverage", [])),
            "next_due_bucket": "MEDIUM",
        },
        outcome=attempt["outcome"],
        hint_level_used=attempt["hint_level_used"],
        representation=attempt["response_evidence"]["representation_used"],
    )

    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "selected-item.json").write_text(json.dumps(selected, indent=2) + "\n", encoding="utf-8")
    (out / "attempt.json").write_text(json.dumps(attempt, indent=2) + "\n", encoding="utf-8")
    (out / "retrieval-state.json").write_text(json.dumps(retrieval, indent=2) + "\n", encoding="utf-8")
    if repair is not None:
        (out / "core1b-repair-request.json").write_text(json.dumps(repair, indent=2) + "\n", encoding="utf-8")
    print(f"PASS Core2B golden -> {selected['item_id']}")


if __name__ == "__main__":
    main()
