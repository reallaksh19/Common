#!/usr/bin/env python3
"""P-K contract validation: authority manifest, run reports, comparison, two-product package."""
import json, sys, tempfile, warnings
from pathlib import Path

warnings.filterwarnings("ignore", category=DeprecationWarning)
from jsonschema import Draft202012Validator  # noqa: E402
from referencing import Registry, Resource  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
PHYS = ROOT.parent
REPO = ROOT.parents[3]
C = ROOT / "contracts"
sys.path.insert(0, str(ROOT / "engine"))

from physics_cold_start_runner import run_cold_start, compare_runs, verify_manifest  # noqa: E402
from physics_cold_start_validator import validate_report, validate_comparison  # noqa: E402


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


NAMES = [
    "physics-two-product-package.schema.json",
    "physics-cold-start-run-report.schema.json",
    "physics-cold-start-comparison.schema.json",
    "physics-generation-authority-manifest.schema.json",
]
STORE = {n: load(C / n) for n in NAMES}
REGISTRY = Registry().with_resources(
    [(n, Resource.from_contents(s)) for n, s in STORE.items()]
)


def validator(name):
    return Draft202012Validator(STORE[name], registry=REGISTRY)


manifest = load(PHYS / "GENERATION_AUTHORITY_MANIFEST.json")
validator("physics-generation-authority-manifest.schema.json").validate(manifest)
verify_manifest(manifest)

# every artifact the manifest names must actually exist in the repository
missing = [rel for rel in list(manifest["authorities"].values()) + list(manifest["engines"].values())
           if not (REPO / rel).exists()]
assert not missing, missing
entrypoint = REPO / manifest["entrypoint_doc"]
assert entrypoint.exists(), manifest["entrypoint_doc"]

with tempfile.TemporaryDirectory() as td:
    out = Path(td)
    no_attempt, artifacts_na = run_cold_start(manifest, out / "no-attempt", False, REPO)
    with_attempts, artifacts_a = run_cold_start(manifest, out / "with-attempts", True, REPO)
    comparison = compare_runs(no_attempt, with_attempts)

    report_v = validator("physics-cold-start-run-report.schema.json")
    package_v = validator("physics-two-product-package.schema.json")
    for report in (no_attempt, with_attempts):
        report_v.validate(report)
        package_v.validate(report["two_product_package"])
    validator("physics-cold-start-comparison.schema.json").validate(comparison)

    validate_report(no_attempt, manifest, artifacts_na)
    validate_report(with_attempts, manifest, artifacts_a)
    validate_comparison(comparison, no_attempt, with_attempts)

    assert all(comparison["invariants"].values())
    assert no_attempt["summary"]["closure_state"] == "CLOSED"
    assert with_attempts["summary"]["closure_state"] == "CLOSED"

print(
    "PHY P-K contract validation: PASS "
    f"({len(manifest['authorities'])} declared authorities, {len(manifest['engines'])} engines, "
    f"two runs over the same assessment with identical scope digest "
    f"{no_attempt['assessment_truth']['study_scope_digest'][:16]}, "
    f"{no_attempt['summary']['total_vector_ops']} vector operations per run)"
)
