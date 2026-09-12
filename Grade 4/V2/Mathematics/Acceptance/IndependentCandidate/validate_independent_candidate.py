"""Build and independently evaluate the exact Grade-4 Math V2 candidate."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import jsonschema
import pypdfium2 as pdfium

from Grade4.V2.Mathematics.Acceptance.IndependentCandidate.build_real_candidate import build_real_candidate
from Grade4.V2.Mathematics.Acceptance.IndependentCandidate.producer_cases import CASES, EXPECTED_CASE_IDS


REPO = Path(__file__).resolve().parents[5]
ORACLE = REPO / "Primary" / "V2" / "Mathematics" / "BenchmarkAcceptance"
BUILD = REPO / "build" / "grade4_math_v2" / "independent_acceptance"


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def render_pdf(path: Path, out_dir: Path) -> int:
    out_dir.mkdir(parents=True, exist_ok=True)
    doc = pdfium.PdfDocument(str(path))
    if len(doc) < 20:
        raise AssertionError(f"REAL_CANDIDATE_PAGE_COUNT_TOO_SMALL: {path.name}: {len(doc)}")
    leaks = ("PMV2-", "CORE1-P", "CORE2-P", "fixture://", "BENCH-")
    for index in range(len(doc)):
        page = doc[index]
        image = page.render(scale=1.3).to_pil()
        if image.width < 500 or image.height < 700:
            raise AssertionError(f"REAL_CANDIDATE_PAGE_RENDER_INVALID: {path.name} p{index + 1}")
        image.save(out_dir / f"page_{index + 1:03d}.png")
        textpage = page.get_textpage()
        text = textpage.get_text_range()
        for token in leaks:
            if token in text:
                raise AssertionError(f"LEARNER_FACING_INTERNAL_IDENTIFIER_LEAK: {path.name} p{index + 1}: {token}")
    return len(doc)


def main() -> None:
    outputs = build_real_candidate(BUILD)
    candidate = load(outputs["candidate"])
    schema = load(ORACLE / "contracts" / "candidate_export.schema.json")
    jsonschema.Draft202012Validator(schema).validate(candidate)

    # Producer must not dynamically consume the frozen oracle expected values.
    producer_source = (Path(__file__).parent / "producer_cases.py").read_text(encoding="utf-8")
    builder_source = (Path(__file__).parent / "build_real_candidate.py").read_text(encoding="utf-8")
    forbidden_runtime_reads = (
        "benchmark_cases.json",
        "semantic_cases.json",
        "from Primary.V2.Mathematics.BenchmarkAcceptance",
        "import Primary.V2.Mathematics.BenchmarkAcceptance",
    )
    for token in forbidden_runtime_reads:
        if token in producer_source or token in builder_source:
            raise AssertionError(f"PRODUCER_READS_INDEPENDENT_ORACLE: {token}")

    if len(CASES) != 20 or len(EXPECTED_CASE_IDS) != len(set(EXPECTED_CASE_IDS)):
        raise AssertionError("PRODUCER_CASE_SET_INVALID")

    c1_map = load(outputs["core1_map"])
    c2_map = load(outputs["core2_map"])
    c1_by_case: dict[str, set[str]] = {}
    c2_cases: set[str] = set()
    for row in c1_map["placements"]:
        c1_by_case.setdefault(str(row["case_id"]), set()).add(str(row["role"]))
    for row in c2_map["placements"]:
        c2_cases.add(str(row["case_id"]))

    for case in CASES:
        cid = str(case["case_id"])
        declared = set(case["representations"])
        realized = c1_by_case.get(cid, set())
        missing = sorted(declared - realized)
        if missing:
            raise AssertionError(f"REQUIRED_REPRESENTATION_NOT_PHYSICALLY_REALIZED: {cid}: {missing}")
        if cid not in c2_cases:
            raise AssertionError(f"CORE2_CASE_PLACEMENT_MISSING: {cid}")

    if candidate["artifacts"]["core1_sha256"] != sha256(outputs["core1"]):
        raise AssertionError("CORE1_ARTIFACT_HASH_NOT_BOUND")
    if candidate["artifacts"]["core2_sha256"] != sha256(outputs["core2"]):
        raise AssertionError("CORE2_ARTIFACT_HASH_NOT_BOUND")
    if len(candidate["artifacts"]["physical_page_map_digest"]) != 64:
        raise AssertionError("PHYSICAL_PAGE_MAP_DIGEST_INVALID")

    core1_pages = render_pdf(outputs["core1"], BUILD / "core1_renders")
    core2_pages = render_pdf(outputs["core2"], BUILD / "core2_renders")

    report_path = BUILD / "independent_acceptance_report.json"
    proc = subprocess.run(
        [sys.executable, str(ORACLE / "validator" / "evaluate_candidate.py"), str(outputs["candidate"]), "--out", str(report_path)],
        text=True,
        capture_output=True,
        check=False,
    )
    sys.stdout.write(proc.stdout)
    sys.stderr.write(proc.stderr)
    if proc.returncode != 0:
        raise AssertionError(f"INDEPENDENT_ORACLE_REJECTED_REAL_CANDIDATE: exit={proc.returncode}")

    report = load(report_path)
    expected = {
        "semantic_status": "PASS",
        "artifact_status": "PASS",
        "human_review_status": "PENDING_HUMAN_REVIEW",
        "classification": "BENCHMARK_ENGINEERING_PASS_PENDING_HUMAN_REVIEW",
        "producer_pass_claims_trusted": False,
    }
    for key, value in expected.items():
        if report.get(key) != value:
            raise AssertionError(f"INDEPENDENT_ACCEPTANCE_STATE_INVALID: {key}={report.get(key)!r}, expected={value!r}")
    if report.get("failures") or report.get("artifact_blockers"):
        raise AssertionError(f"INDEPENDENT_ACCEPTANCE_UNEXPECTED_BLOCKERS: {report}")

    summary = {
        "status": "PASS",
        "case_count": len(candidate["cases"]),
        "core1_pages": core1_pages,
        "core2_pages": core2_pages,
        "core1_sha256": candidate["artifacts"]["core1_sha256"],
        "core2_sha256": candidate["artifacts"]["core2_sha256"],
        "physical_page_map_digest": candidate["artifacts"]["physical_page_map_digest"],
        "independent_classification": report["classification"],
        "human_review_status": report["human_review_status"],
    }
    (BUILD / "validation_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
