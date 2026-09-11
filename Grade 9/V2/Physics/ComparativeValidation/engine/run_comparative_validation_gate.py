#!/usr/bin/env python3
import argparse, hashlib, json
from pathlib import Path

REQUIRED_HUMAN_GATES = (
    "SUBJECT_CORRECTNESS",
    "PEDAGOGY_USABILITY",
    "VISUAL_USABILITY",
)

def load(path):
    return json.loads(Path(path).read_text())

def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()

def sha_obj(obj):
    return hashlib.sha256(canonical(obj)).hexdigest()

def _blocked(candidate_sha, human_authority, unmet):
    seed = {
        "candidate_artifact_sha256": candidate_sha,
        "status": "BLOCKED_HUMAN_QUALITY_GATES",
        "human_gate_authority": human_authority,
        "unmet_gates": list(unmet),
        "reference_access_status": "NOT_ATTEMPTED",
        "comparative_validation_status": "NOT_RUN",
    }
    return {
        "schema_version": "1.0.0",
        "validation_id": "PHY-COMP-" + sha_obj(seed)[:14].upper(),
        "candidate_artifact_sha256": candidate_sha,
        "status": "BLOCKED_HUMAN_QUALITY_GATES",
        "human_gate_authority": human_authority,
        "unmet_gates": list(unmet),
        "reference_access_status": "NOT_ATTEMPTED",
        "reference_sha256": None,
        "comparative_validation_status": "NOT_RUN",
        "release_evidence_eligible": False,
    }

def _validate_candidate_binding(manifest, ai_review):
    candidate_sha = manifest["artifact_sha256"]
    if ai_review["revised_artifact_sha256"] != candidate_sha:
        raise ValueError("candidate/review artifact identity mismatch")
    if ai_review.get("review_class") != "AI_PRE_REVIEW":
        raise ValueError("expected evidence-bound AI_PRE_REVIEW package")
    q = manifest["quality_states"]
    if q.get("PUBLICATION_ENGINEERING") != "PASS":
        raise ValueError("publication engineering must pass before final validation")
    if q.get("BENCHMARK_COMPARATIVE_VALIDATION") != "NOT_RUN":
        raise ValueError("candidate manifest must enter PHY-V2-07 with comparison NOT_RUN")
    if ai_review.get("release_evidence_eligible") is not False:
        raise ValueError("AI pre-review cannot make release evidence eligible")
    return candidate_sha

def _human_gate_state(human_review, candidate_sha):
    if human_review is None:
        return "NO_AUTHORIZED_HUMAN_EVIDENCE", list(REQUIRED_HUMAN_GATES)
    if human_review.get("candidate_artifact_sha256") != candidate_sha:
        raise ValueError("human review candidate identity mismatch")
    if human_review.get("authority_class") != "AUTHORIZED_HUMAN_REVIEW":
        return "UNAUTHORIZED_HUMAN_GATE_EVIDENCE", list(REQUIRED_HUMAN_GATES)
    if not human_review.get("reviewer_authority_refs") or not human_review.get("evidence_refs"):
        raise ValueError("authorized human review requires reviewer authority and evidence refs")
    states = human_review.get("quality_states", {})
    unmet = [gate for gate in REQUIRED_HUMAN_GATES if states.get(gate) != "PASS"]
    return "AUTHORIZED_HUMAN_REVIEW", unmet

def run_gate(manifest, ai_review, reference_path, human_review=None):
    candidate_sha = _validate_candidate_binding(manifest, ai_review)
    human_authority, unmet = _human_gate_state(human_review, candidate_sha)
    if unmet:
        return _blocked(candidate_sha, human_authority, unmet)

    # This is intentionally the first reference read in the control flow.
    reference_bytes = Path(reference_path).read_bytes()
    reference_sha = hashlib.sha256(reference_bytes).hexdigest()
    seed = {
        "candidate_artifact_sha256": candidate_sha,
        "status": "READY_FOR_REFERENCE_COMPARISON",
        "human_gate_authority": human_authority,
        "reference_sha256": reference_sha,
    }
    return {
        "schema_version": "1.0.0",
        "validation_id": "PHY-COMP-" + sha_obj(seed)[:14].upper(),
        "candidate_artifact_sha256": candidate_sha,
        "status": "READY_FOR_REFERENCE_COMPARISON",
        "human_gate_authority": human_authority,
        "unmet_gates": [],
        "reference_access_status": "ACCESSED_AFTER_HUMAN_GATES",
        "reference_sha256": reference_sha,
        "comparative_validation_status": "NOT_RUN",
        "release_evidence_eligible": False,
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--manifest", required=True)
    p.add_argument("--review-package", required=True)
    p.add_argument("--reference", required=True)
    p.add_argument("--human-review")
    p.add_argument("--out", required=True)
    a = p.parse_args()
    result = run_gate(
        load(a.manifest),
        load(a.review_package),
        a.reference,
        load(a.human_review) if a.human_review else None,
    )
    Path(a.out).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "candidate_artifact_sha256": result["candidate_artifact_sha256"],
        "reference_access_status": result["reference_access_status"],
    }, sort_keys=True))

if __name__ == "__main__":
    main()
