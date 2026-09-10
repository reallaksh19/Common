#!/usr/bin/env python3
"""Final integration falsifiers for the two-core stack.

A: repository-owned QuestionContent/Occurrence/Evidence -> FULL_TOPIC_PAIR -> reopened PDF QA.
B: one frozen Permutations ResearchPackage -> B40 and B90 Core (2) publications.

This script performs no subject or web research.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def run(*args: object) -> None:
    cmd = [str(x) for x in args]
    print("+", " ".join(cmd))
    subprocess.run(cmd, check=True)


def full_pair(root: Path, out_root: Path) -> None:
    grade9 = root / "Grade 9"
    base_input = grade9 / "Architecture/replays/laws_of_motion/research_input.json"
    source_questions = grade9 / "architecture/core2/tests/fixtures/full_topic_pair_questions.md"
    transfer_template = grade9 / "architecture/core2/tests/fixtures/full_topic_pair_transfer.template.json"
    physics_skill = grade9 / "skills/grade9-physics/SKILL.md"

    data = copy.deepcopy(load(base_input))
    data["artifact_prefix"] = "Laws_of_Motion_FullPair"
    data["research_bundle_id"] = "RB-G9-PHY-LAWS-MOTION-FULLPAIR-2026"
    data["release_note"] = (
        "Repository-owned FULL_TOPIC_PAIR integration falsifier. The two questions are "
        "internal original fixtures and are not claimed as exam occurrences."
    )

    registry_hash = sha256_file(physics_skill)
    for reg in data["scope_graph"]["canonical_registry_versions"]:
        reg["registry_sha256"] = registry_hash
        reg["registry_locator"] = "Grade 9/skills/grade9-physics/SKILL.md"

    locator_by_source = {
        "SRC-NCERT-G9-SYLLABUS-FORCE": "Grade 9 Force and Laws of Motion scope / learning outcomes",
        "SRC-SOF-ISO-G9-SYLLABUS-2026": "Class 9 syllabus / exam pattern",
        "SRC-REPO-G9-PHYSICS-SKILL": "Physics subject authority reasoning contract",
    }
    for claim in data["research_claims"]:
        if claim.get("source_refs"):
            src = claim["source_refs"][0]
            claim["evidence_refs"] = [{
                "source_id": src,
                "locator": {"section": locator_by_source.get(src, f"Evidence for {claim['claim_id']}")},
            }]

    source_id = "SRC-REPO-CORE2-FULLPAIR-QUESTIONS"
    source_hash = sha256_file(source_questions)
    data["source_ledger"]["sources"].append({
        "source_id": source_id,
        "provider": "Common repository",
        "source_type": "REPOSITORY_OWNED_QUESTION_FIXTURE",
        "repo_path": "Grade 9/architecture/core2/tests/fixtures/full_topic_pair_questions.md",
        "retrieved_at": "2026-09-10T11:00:00Z",
        "content_sha256": source_hash,
        "authority_level": "VERIFIED_SECONDARY",
        "verification_status": "VERIFIED",
        "scope_role": "Repository-owned questions used only to falsify the full-pair publication pipeline.",
        "rights": {
            "status": "REPRODUCTION_ALLOWED",
            "basis": "Repository-owned integration fixture.",
            "allowed_uses": ["CITE_SOURCE", "REUSE_INTERNAL_CONTRACT"],
            "prohibited_uses": [],
        },
    })

    q1_stem = "A 2 kg block on a frictionless horizontal surface has a 6 N horizontal force to the right. What is its acceleration?"
    q2_stem = "Two horizontal forces, 10 N right and 4 N left, act on a 2 kg object. Determine the acceleration and direction."
    answer = "3 m/s^2 to the right"

    data["question_content_ledger"] = {
        "question_content_ledger_id": "QCL-G9-PHY-FULLPAIR-001",
        "schema_version": "1.0.0",
        "records": [
            {
                "question_content_id": "QC-G9-PHY-FULLPAIR-001",
                "content_origin": "SOURCE_DERIVED",
                "primary_concept_id": "PHY-G9-NEWTON-LAW-2",
                "supporting_concept_ids": ["PHY-G9-SYSTEM-REPRESENTATION"],
                "stem": q1_stem,
                "answer": answer,
                "dependency_class": "NONE",
                "occurrence_ids": ["QO-G9-PHY-FULLPAIR-001"],
                "research_refs": ["R-PHY-LM-003", "R-PHY-LM-005"],
            },
            {
                "question_content_id": "QC-G9-PHY-FULLPAIR-002",
                "content_origin": "SOURCE_DERIVED",
                "primary_concept_id": "PHY-G9-NEWTON-LAW-2",
                "supporting_concept_ids": ["PHY-G9-FORCE-VECTOR", "PHY-G9-SYSTEM-REPRESENTATION"],
                "stem": q2_stem,
                "answer": answer,
                "dependency_class": "NONE",
                "occurrence_ids": ["QO-G9-PHY-FULLPAIR-002"],
                "research_refs": ["R-PHY-LM-001", "R-PHY-LM-003", "R-PHY-LM-005"],
            },
        ],
    }
    data["question_occurrence_ledger"] = {
        "question_occurrence_ledger_id": "QOL-G9-PHY-FULLPAIR-001",
        "schema_version": "1.0.0",
        "records": [
            {
                "occurrence_id": "QO-G9-PHY-FULLPAIR-001",
                "question_content_id": "QC-G9-PHY-FULLPAIR-001",
                "source_id": source_id,
                "source_locator": {"section": "Q1", "source_question_id": "Q1"},
                "source_fingerprint_sha256": source_hash,
                "storage_mode": "FULL_TEXT",
                "raw_stem": q1_stem,
                "raw_answer": answer,
                "values_units": ["2 kg", "6 N", "m/s^2"],
                "transcription_state": "VERIFIED",
                "answer_state": "VERIFIED",
                "rights_status_at_freeze": "REPRODUCTION_ALLOWED",
            },
            {
                "occurrence_id": "QO-G9-PHY-FULLPAIR-002",
                "question_content_id": "QC-G9-PHY-FULLPAIR-002",
                "source_id": source_id,
                "source_locator": {"section": "Q2", "source_question_id": "Q2"},
                "source_fingerprint_sha256": source_hash,
                "storage_mode": "FULL_TEXT",
                "raw_stem": q2_stem,
                "raw_answer": answer,
                "values_units": ["10 N", "4 N", "2 kg", "m/s^2"],
                "transcription_state": "VERIFIED",
                "answer_state": "VERIFIED",
                "rights_status_at_freeze": "REPRODUCTION_ALLOWED",
            },
        ],
    }
    data["question_evidence_ledger"] = {
        "question_evidence_ledger_id": "QEL-G9-PHY-FULLPAIR-001",
        "schema_version": "1.0.0",
        "corpus_authority_id": "CORPUS-REPO-CORE2-FULLPAIR",
        "candidate_denominator": 2,
        "frozen_at": "2026-09-10T11:00:00Z",
        "rows": [
            {
                "occurrence_id": "QO-G9-PHY-FULLPAIR-001",
                "question_content_id": "QC-G9-PHY-FULLPAIR-001",
                "disposition": "REQUIRED",
                "primary_owner": "PHY-G9-NEWTON-LAW-2",
                "source_state": "VERIFIED",
                "transcription_state": "VERIFIED",
                "answer_state": "VERIFIED",
                "publication_targets": ["TRANSFER_BOOK"],
            },
            {
                "occurrence_id": "QO-G9-PHY-FULLPAIR-002",
                "question_content_id": "QC-G9-PHY-FULLPAIR-002",
                "disposition": "REQUIRED",
                "primary_owner": "PHY-G9-NEWTON-LAW-2",
                "source_state": "VERIFIED",
                "transcription_state": "VERIFIED",
                "answer_state": "VERIFIED",
                "publication_targets": ["TRANSFER_BOOK"],
            },
        ],
        "summary": {"required": 2, "defer": 0, "exclude": 0, "review": 0, "duplicate": 0},
    }

    work = out_root / "full-topic-pair"
    core1 = work / "core1"
    core2 = work / "core2"
    input_path = work / "research_input.json"
    learner_path = work / "learner_profile.json"
    request_path = work / "publication_target.request.json"
    target_path = work / "publication_target.json"
    write(input_path, data)

    learner = load(grade9 / "Architecture/replays/laws_of_motion/learner_profile.json")
    learner["learner_profile_id"] = "LP-G9-PHY-FULLPAIR-B50-001"
    for row in learner["baselines"]:
        row["value"] = 50
        row["basis"] = "EVIDENCE_ESTIMATED"
        row["confidence"] = "LOW"
        row["evidence_refs"] = []
    learner["notes"] = "Synthetic repository-owned FULL_TOPIC_PAIR integration falsifier."
    write(learner_path, learner)

    request = {
        "publication_target_id": "PT-G9-PHY-FULLPAIR-B50-001",
        "purpose": {
            "type": "COMPETITIVE_EXAM",
            "exam_profile_id": "SOF_ISO_L1",
            "curriculum_profile_id": "NCERT-G9-SECONDARY-PHASE1-2026"
        },
        "requested_products": {"study_guide": True, "transfer_book": True},
        "publication_profile": {
            "delivery_contract": "FULL_TOPIC_PAIR",
            "subject_profile": "PHYSICS_PR156",
            "orientation": "AUTO",
            "answer_separation": True,
            "grayscale_safe": True
        }
    }
    write(request_path, request)

    py = sys.executable
    build = grade9 / "Architecture/core1/build_research_package.py"
    bind = grade9 / "architecture/core2/bind_publication_target.py"
    handoff = grade9 / "Architecture/contracts/v1/validate_handoff.py"
    publisher = grade9 / "skills/grade9-core2-publisher/scripts/run_core2.py"
    validate_pub = grade9 / "skills/grade9-core2-publisher/scripts/validate_core2_package.py"

    run(py, build, "--input", input_path, "--out", core1)
    prefix = "Laws_of_Motion_FullPair"
    bundle = core1 / f"{prefix}_Research_Bundle.json"
    manifest = core1 / f"{prefix}_Research_Bundle_Manifest.json"
    source_ledger = core1 / f"{prefix}_Source_Ledger.json"
    qcontent = core1 / f"{prefix}_Question_Content_Ledger.json"
    qocc = core1 / f"{prefix}_Question_Occurrence_Ledger.json"
    qel = core1 / f"{prefix}_Question_Evidence_Ledger.json"
    exam = sorted(core1.glob(f"{prefix}_Exam_Demand_*.json"))[0]

    run(py, bind, "--manifest", manifest, "--learner", learner_path, "--request", request_path, "--out", target_path)
    run(py, handoff, "--bundle", bundle, "--manifest", manifest, "--learner", learner_path, "--target", target_path,
        "--source-ledger", source_ledger, "--exam-demand", exam, "--question-content-ledger", qcontent,
        "--question-occurrence-ledger", qocc, "--question-ledger", qel, "--verify-artifact-bytes")
    run(py, publisher, "--bundle", bundle, "--manifest", manifest, "--learner", learner_path, "--target", target_path,
        "--transfer-model", transfer_template, "--out", core2, "--prefix", prefix)
    run(py, validate_pub, "--dir", core2, "--prefix", prefix)

    qcontent_obj = load(qcontent)
    qocc_obj = load(qocc)
    qel_obj = load(qel)
    tb = load(core2 / f"{prefix}_Core2_Transfer_Book.json")
    study = load(core2 / f"{prefix}_Core2_Study_Guide.json")
    audit = load(core2 / f"{prefix}_Core2_Publication_Audit.json")
    pub_manifest = load(core2 / f"{prefix}_Core2_Publication_Manifest.json")

    required_rows = [r for r in qel_obj["rows"] if r["disposition"] == "REQUIRED" and "TRANSFER_BOOK" in r.get("publication_targets", [])]
    required_occ = {r["occurrence_id"] for r in required_rows}
    required_content = {r["question_content_id"] for r in required_rows}
    assert required_occ == {q["occurrence_id"] for q in tb["questions"]}
    assert required_content == {q["question_content_id"] for q in tb["questions"]}
    assert required_occ == {r["occurrence_id"] for r in qocc_obj["records"]}
    assert required_content == {r["question_content_id"] for r in qcontent_obj["records"]}

    sid = study["product_identity"]
    tid = tb["product_identity"]
    assert sid["pair_id"] == tid["pair_id"]
    assert sid["companion_product_id"] == tb["publication_id"]
    assert tid["companion_product_id"] == study["publication_id"]
    assert len([a for a in pub_manifest["artifacts"] if a["role"].endswith("_PDF")]) == 2
    assert all(audit["gates"].values()), audit["gates"]
    assert all(ev["sha256"] for ev in audit["pdf_evidence"])

    print("FULL_TOPIC_PAIR_CORE1_CUSTODY = PASS")
    print("FULL_TOPIC_PAIR_HANDOFF = PASS")
    print("FULL_TOPIC_PAIR_RECIPROCAL_IDENTITY = PASS")
    print("FULL_TOPIC_PAIR_TRANSFER_CLOSURE = PASS")
    print("FULL_TOPIC_PAIR_REOPENED_PDF_QA = PASS")


def b40_b90(root: Path, out_root: Path) -> None:
    grade9 = root / "Grade 9"
    perm = grade9 / "Mathematics/Permutations/Core1"
    bundle = perm / "Permutations_Core1_Research_Bundle.json"
    manifest = perm / "Permutations_Core1_Research_Bundle_Manifest.json"
    source_ledger = perm / "Permutations_Core1_Source_Ledger.json"
    base_learner = load(grade9 / "architecture/replays/permutations/learner_profile.json")
    base_request = load(grade9 / "architecture/replays/permutations/publication_target.request.json")

    py = sys.executable
    bind = grade9 / "architecture/core2/bind_publication_target.py"
    handoff = grade9 / "Architecture/contracts/v1/validate_handoff.py"
    publisher = grade9 / "skills/grade9-core2-publisher/scripts/run_core2.py"
    validate_pub = grade9 / "skills/grade9-core2-publisher/scripts/validate_core2_package.py"
    package_digest = load(manifest)["package_digest"]
    outputs = {}

    for value in (40, 90):
        label = f"B{value}"
        work = out_root / f"permutations-{label.lower()}"
        learner_path = work / "learner_profile.json"
        request_path = work / "publication_target.request.json"
        target_path = work / "publication_target.json"
        pub_dir = work / "core2"

        learner = copy.deepcopy(base_learner)
        learner["learner_profile_id"] = f"LP-G11-MATH-PERMUTATIONS-{label}-FALSIFIER"
        for row in learner["baselines"]:
            row["value"] = value
            row["basis"] = "EVIDENCE_ESTIMATED"
            row["confidence"] = "LOW"
            row["evidence_refs"] = []
        learner["notes"] = f"Synthetic {label} Core (2) same-ResearchPackage falsifier."
        write(learner_path, learner)

        request = copy.deepcopy(base_request)
        request["publication_target_id"] = f"PT-G11-MATH-PERMUTATIONS-{label}-FALSIFIER"
        request["requested_products"] = {"study_guide": True, "transfer_book": False}
        request.setdefault("publication_profile", {})["delivery_contract"] = "STUDY_GUIDE_ONLY"
        write(request_path, request)

        run(py, bind, "--manifest", manifest, "--learner", learner_path, "--request", request_path, "--out", target_path)
        assert load(target_path)["research_package_digest"] == package_digest
        run(py, handoff, "--bundle", bundle, "--manifest", manifest, "--learner", learner_path, "--target", target_path, "--source-ledger", source_ledger)
        run(py, publisher, "--bundle", bundle, "--manifest", manifest, "--learner", learner_path, "--target", target_path,
            "--out", pub_dir, "--prefix", f"Permutations_{label}")
        run(py, validate_pub, "--dir", pub_dir, "--prefix", f"Permutations_{label}")

        plan = load(pub_dir / f"Permutations_{label}_Core2_Publication_Plan.json")
        study = load(pub_dir / f"Permutations_{label}_Core2_Study_Guide.json")
        audit = load(pub_dir / f"Permutations_{label}_Core2_Publication_Audit.json")
        assert all(audit["gates"].values()), audit["gates"]
        outputs[value] = (plan, study)

    plan40, study40 = outputs[40]
    plan90, study90 = outputs[90]
    assert plan40["research_package_digest"] == plan90["research_package_digest"] == package_digest
    refs40 = [(s["concept_id"], tuple(s["research_refs"])) for s in plan40["sections"]]
    refs90 = [(s["concept_id"], tuple(s["research_refs"])) for s in plan90["sections"]]
    assert refs40 == refs90
    assert {s["instructional_profile"] for s in plan40["sections"]} == {"BRIDGE"}
    assert {s["instructional_profile"] for s in plan90["sections"]} == {"REFERENCE"}
    assert study40 != study90

    def count_items(model: dict, item_type: str) -> int:
        return sum(1 for sec in model["main_sections"] for item in sec["items"] if item["type"] == item_type)

    assert count_items(study40, "WORKED_REASONING") > count_items(study90, "WORKED_REASONING")
    practice40 = " ".join(x["content"] for x in study40["appendix_A"]["items"])
    practice90 = " ".join(x["content"] for x in study90["appendix_A"]["items"])
    assert "What do you notice first" in practice40
    assert "shortest correct trigger" in practice90

    print("B40_B90_SAME_RESEARCH_PACKAGE_DIGEST = PASS")
    print("B40_B90_PLAN_RESEARCH_REFS_IDENTICAL = PASS")
    print("B40_B90_INSTRUCTIONAL_PROFILE_DIFFERENT = PASS")
    print("B40_B90_STUDY_MODEL_DIFFERENT = PASS")
    print("B40_B90_WORKED_SUPPORT_DIFFERENT = PASS")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=Path("/tmp/core2-final-falsifiers"))
    args = ap.parse_args()
    root = Path(__file__).resolve().parents[4]
    args.out.mkdir(parents=True, exist_ok=True)
    full_pair(root, args.out)
    b40_b90(root, args.out)
    print("CORE2_FINAL_FALSIFIERS = PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
