#!/usr/bin/env python3
"""Independent preflight for the Redox Core1A Workbench v2 stress receipt."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[5]
BP = ROOT / "Grade 9" / "V2" / "Chemistry" / "LearningBlueprint"

EXPECTED_BLOCKER = "CHEM_PRODUCT_SCOPE_STRESS_AUDIT_NOT_AUTHORITY"
CURRENT = {
    "authority": "golden/v7/core1a-study-note-redox-authority.json",
    "ccbom": "golden/v7/ccbom-redox.json",
    "ttu": "golden/v5/core1a-hard-study-product.json",
    "sdu": "golden/v6/sdu-hard-redox.json",
    "concept_ttu": "golden/v6/concept-ttu-core1a-redox.json",
    "self_help": "golden/v6/self-help-core1a-redox.json",
    "study_policy": "policies/v7-core1a-study-note-sufficiency-policy.json",
    "stress_audit": "stress_tests/redox/source-audit.v2.json",
}
FORBIDDEN_V1_REFS = (
    "fixtures/engineering-workbench/redox-request.v1.json",
    "fixtures/engineering-workbench/redox-manifest.v1.json",
    "fixtures/engineering-workbench/redox-product-source-scope.v1.json",
    "policies/chemistry-redox-source-audit.v1.json",
    "v2-chemistry-engineering-workbench-v1",
)


def load(rel: str) -> dict[str, Any]:
    return json.loads((BP / rel).read_text(encoding="utf-8"))


def sha(obj: Any) -> str:
    raw = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("receipt")
    args = parser.parse_args()
    receipt_path = Path(args.receipt)
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))

    authority = load(CURRENT["authority"])
    ccbom = load(CURRENT["ccbom"])
    ttu = load(CURRENT["ttu"])
    sdu = load(CURRENT["sdu"])
    concept_ttu = load(CURRENT["concept_ttu"])
    self_help = load(CURRENT["self_help"])
    study_policy = load(CURRENT["study_policy"])
    stress_audit = load(CURRENT["stress_audit"])

    assert receipt["status"] == "EXPECTED_BLOCK_CONFIRMED"
    assert receipt["product_mode"] == "CORE1A"
    assert receipt["product_emitted"] is False
    assert receipt["pdf_emitted"] is False
    assert receipt["workbench_version"] == "V2"
    assert receipt["stress_authority_status"] == "NON_AUTHORITATIVE_FIXTURE"
    assert receipt["expected_blocker"] == EXPECTED_BLOCKER
    assert receipt["observed_blocker"] == EXPECTED_BLOCKER
    assert receipt["source_audit"]["audit_role"] == "STRESS_TEST_SOURCE_AUDIT"
    assert receipt["source_audit"]["authority_effect"] == "NONE_STRESS_TEST_ONLY"
    assert receipt["source_audit"]["digest"] == sha(stress_audit)
    assert receipt["historical_v1_authority_used"] is False
    assert receipt["release_condition"] == "NO_LEARNER_PRODUCT_RENDER_UNTIL_EXPLICIT_PRODUCTION_SOURCE_AUDIT_EXISTS"

    current = receipt["current_blueprint"]
    assert current["authority_id"] == authority["authority_id"]
    assert current["authority_digest"] == sha(authority)
    assert current["subtopic_id"] == authority["subtopic_id"]
    assert current["difficulty_badge"] == authority["difficulty_badge"] == "HARD"
    assert current["learning_atom_count"] == len(authority["learning_atoms"])
    assert current["content_object_count"] == len(authority["content_objects"])
    assert current["ccbom_id"] == ccbom["ccbom_id"]
    assert current["ccbom_digest"] == sha(ccbom)
    assert current["sdu_digest"] == sha(sdu)
    assert current["concept_ttu_id"] == concept_ttu["ttu_id"]
    assert current["concept_ttu_digest"] == sha(concept_ttu)
    assert current["self_help_closure_id"] == self_help["closure_id"]
    assert current["self_help_digest"] == sha(self_help)
    assert current["study_policy_id"] == study_policy["policy_id"]
    assert current["study_policy_digest"] == sha(study_policy)

    required = set(authority["reconstructable_ttu_refs"])
    serialized = {row["ttu_id"] for row in ttu.get("reconstructable_ttus", [])}
    assert set(current["required_reconstructable_ttu_ids"]) == required
    assert required <= serialized
    assert set(current["serialized_reconstructable_ttu_ids"]) == serialized

    # This stress proof must stop before rendering. Any PDF beside the receipt is a failure.
    pdfs = sorted(str(path) for path in receipt_path.parent.rglob("*.pdf"))
    assert not pdfs, f"learner PDF emitted despite missing production source authority: {pdfs}"

    # The rebuilt harness itself must not retain old Workbench v1 authority paths.
    harness_text = "\n".join(
        (HERE / name).read_text(encoding="utf-8")
        for name in ("build_core1a.py", "preflight_core1a.py")
    )
    for ref in FORBIDDEN_V1_REFS:
        assert ref not in harness_text, f"old Workbench v1 authority reference retained: {ref}"

    print(json.dumps({
        "status": "PASS",
        "proof": receipt["proof_id"],
        "observed_blocker": receipt["observed_blocker"],
        "audit_role": receipt["source_audit"]["audit_role"],
        "authority_effect": receipt["source_audit"]["authority_effect"],
        "product_emitted": receipt["product_emitted"],
        "pdf_count": len(pdfs),
        "current_content_objects": current["content_object_count"],
        "current_reconstructable_ttus": len(required),
    }, indent=2))


if __name__ == "__main__":
    main()
