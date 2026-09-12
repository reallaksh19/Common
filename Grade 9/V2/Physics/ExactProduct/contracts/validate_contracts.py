#!/usr/bin/env python3
"""P-L contract validation: exact candidate, AI pre-review, release, attestation shape."""
import json, sys, tempfile, warnings
from pathlib import Path

warnings.filterwarnings("ignore", category=DeprecationWarning)
from jsonschema import Draft202012Validator  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
PHYS = ROOT.parent
REPO = ROOT.parents[3]
C = ROOT / "contracts"
sys.path[:0] = [str(ROOT / "engine"), str(PHYS / "ColdStart" / "engine")]

from physics_cold_start_runner import run_cold_start  # noqa: E402
from evaluate_physics_exact_product import build_candidate, evaluate, BLOCKED  # noqa: E402
from audit_physics_exact_candidate import build_review  # noqa: E402


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def check(name, instance):
    Draft202012Validator(load(C / name)).validate(instance)


policy = load(ROOT / "registry" / "physics-exact-product-quality-policy.json")
primitive_registry = load(PHYS / "Representation" / "registry" / "physics-teaching-primitive-registry.json")
manifest = load(PHYS / "GENERATION_AUTHORITY_MANIFEST.json")

assert set(policy["required_quality_states"]) == {
    "PUBLICATION_ENGINEERING", "SUBJECT_CORRECTNESS", "PEDAGOGICAL_DESIGN", "ASSESSMENT_DESIGN",
    "VISUAL_USABILITY", "MATURE_DESIGN_QUALITY", "REFERENCE_COMPARABILITY",
}
assert policy["machine_settable_states"] == ["PUBLICATION_ENGINEERING"]
assert policy["ai_pre_review"]["may_set_mature_classification"] is False
assert policy["reference_comparator_allowed_stage"] == "AFTER_ALL_HUMAN_GATES_PASS"

with tempfile.TemporaryDirectory() as td:
    run_dir = Path(td) / "with-attempts"
    report, _ = run_cold_start(manifest, run_dir, True, REPO)
    candidate = build_candidate(
        run_dir, report, load(run_dir / "coverage_closure.json"),
        load(run_dir / "core1_page_map.json"), load(run_dir / "core2_page_map.json"),
        load(run_dir / "core2.json"), primitive_registry, policy,
    )
    check("physics-exact-product-candidate.schema.json", candidate)

    ai_review = build_review(run_dir, policy)
    check("physics-exact-product-review.schema.json", ai_review)

    release = evaluate(candidate, policy, None, ai_review)
    check("physics-exact-product-release.schema.json", release)

    assert candidate["machine_gate"] == "PASS", candidate["machine_findings"]
    assert release["exit_code"] == BLOCKED
    assert release["classification"] == policy["blocked_classification"]
    assert release["quality_states"]["PUBLICATION_ENGINEERING"] == "PASS"
    for state in policy["human_settable_states"]:
        assert release["quality_states"][state] == "PENDING", state
    assert release["quality_states"]["MATURE_DESIGN_QUALITY"] == "PENDING"
    assert release["quality_states"]["REFERENCE_COMPARABILITY"] == "NOT_RUN"
    assert release["learning_effectiveness"] == "STUDY_REQUIRED"

print(
    "PHY P-L contract validation: PASS "
    f"(machine gate {candidate['machine_gate']}, classification {release['classification']}, "
    f"exit {release['exit_code']}, blocking {len(release['blocking_states'])} states, "
    f"AI pre-review advisory with {len(ai_review['advisory_concerns'])} concerns)"
)
