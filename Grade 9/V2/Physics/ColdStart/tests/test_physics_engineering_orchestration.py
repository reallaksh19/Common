#!/usr/bin/env python3
"""P-K orchestration falsifiers for mandatory P-C.5 Engineering custody."""
import copy, json, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHYS = ROOT.parent
REPO = ROOT.parents[3]
sys.path.insert(0, str(ROOT / "engine"))

from physics_cold_start_runner import run_cold_start, compare_runs, digest  # noqa: E402
from physics_cold_start_validator import validate_report, validate_comparison  # noqa: E402


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


manifest = load(PHYS / "GENERATION_AUTHORITY_MANIFEST.json")
assert "P-C.5 EngineeringReadiness" in manifest["phase_order"]
assert "engineering_scope_bindings" in manifest["authorities"]
assert "assessment_scope" in manifest["engines"]
assert "engineering_readiness" in manifest["engines"]
assert "MANUAL_ENGINEERING_READINESS" in manifest["runtime_input_contract"]["forbidden"]
assert "ENGINEERING_READINESS" in manifest["required_authority_trace_decisions"]

with tempfile.TemporaryDirectory() as td:
    out = Path(td)
    no_attempt, a0 = run_cold_start(manifest, out / "no-attempt", False, REPO)
    with_attempts, a1 = run_cold_start(manifest, out / "with-attempts", True, REPO)
    comparison = compare_runs(no_attempt, with_attempts)

    assert validate_report(no_attempt, manifest, a0)
    assert validate_report(with_attempts, manifest, a1)
    assert validate_comparison(comparison, no_attempt, with_attempts)

    for report, artifacts in ((no_attempt, a0), (with_attempts, a1)):
        truth = report["assessment_truth"]
        readiness = artifacts["engineering_readiness"]
        scope = artifacts["assessment_scope_model"]
        semantics = artifacts["problem_semantics"]
        assert truth["engineering_consumer_status"] == "ALLOWED"
        assert report["stage_digests"]["P_C_assessment_scope"] == scope["scope_model_digest"]
        assert report["stage_digests"]["P_C5_engineering_readiness"] == truth["engineering_readiness_digest"]
        assert readiness["readiness_digest"] == "sha256:" + truth["engineering_readiness_digest"]
        assert readiness["scope_model_digest"] == scope["scope_model_digest"]
        assert semantics["scope_model_ref"] == scope["scope_model_id"]
        assert readiness["required_consumer"] == "PROBLEM_SEMANTICS"

    assert comparison["invariants"]["assessment_scope_digest_identical"]
    assert comparison["invariants"]["engineering_readiness_digest_identical"]
    assert comparison["invariants"]["engineering_consumer_status_identical"]
    assert comparison["invariants"]["engineering_gate_requirement_state_identical"]

    drifted = copy.deepcopy(a1)
    drifted["assessment_scope_model"]["scope_model_id"] += "-DRIFT"
    try:
        validate_report(with_attempts, manifest, drifted)
    except ValueError as exc:
        assert str(exc).startswith("P_D_CONSUMED_DIFFERENT_SCOPE_AFTER_ENGINEERING_GATE"), exc
    else:
        raise AssertionError("P-D scope drift after Engineering authorization was accepted")

    manual = copy.deepcopy(with_attempts)
    manual["runtime_dependency_audit"]["manual_precomputed_inputs_used"] = ["EngineeringReadiness"]
    manual["report_digest"] = digest(manual, "report_digest")
    try:
        validate_report(manual, manifest)
    except ValueError as exc:
        assert str(exc).startswith("MANUAL_ENGINEERING_READINESS_REQUIRED"), exc
    else:
        raise AssertionError("manually supplied Engineering Readiness was accepted")

print("Physics P-C.5 cold-start orchestration: PASS (exact P-C -> Engineering Gate -> exact P-D custody; two-run invariant)")
