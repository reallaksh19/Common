#!/usr/bin/env python3
import hashlib, importlib.util, json, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("phy_gate", ROOT / "engine/run_comparative_validation_gate.py")
G = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(G)

SHA = "9e5ef00e6a7049e076b56d58a7ce71460e7a8f632a9e42b9ec27e256af4847f8"

def manifest():
    return {
        "artifact_sha256": SHA,
        "quality_states": {
            "PUBLICATION_ENGINEERING": "PASS",
            "SUBJECT_CORRECTNESS": "PENDING",
            "PEDAGOGY_USABILITY": "PENDING",
            "VISUAL_USABILITY": "PENDING",
            "BENCHMARK_COMPARATIVE_VALIDATION": "NOT_RUN",
        },
    }

def ai_review():
    return {
        "revised_artifact_sha256": SHA,
        "review_class": "AI_PRE_REVIEW",
        "release_evidence_eligible": False,
        "quality_states": {
            "PUBLICATION_ENGINEERING": "PASS",
            "SUBJECT_CORRECTNESS": "PENDING",
            "PEDAGOGY_USABILITY": "PENDING",
            "VISUAL_USABILITY": "PENDING",
            "BENCHMARK_COMPARATIVE_VALIDATION": "NOT_RUN",
        },
    }

def human(authority="AUTHORIZED_HUMAN_REVIEW", states=None, sha=SHA, refs=True):
    return {
        "schema_version": "1.0.0",
        "candidate_artifact_sha256": sha,
        "authority_class": authority,
        "quality_states": states or {
            "SUBJECT_CORRECTNESS": "PASS",
            "PEDAGOGY_USABILITY": "PASS",
            "VISUAL_USABILITY": "PASS",
        },
        "reviewer_authority_refs": ["TEST_ONLY:reviewer-authority"] if refs else [],
        "evidence_refs": ["TEST_ONLY:human-evidence"] if refs else [],
    }

def must_raise(exc, fn):
    try:
        fn()
    except exc:
        return
    raise AssertionError(f"expected {exc.__name__}")

def main():
    count = 0
    r = G.run_gate(manifest(), ai_review(), "/tmp/PR156-MUST-NOT-BE-READ.json")
    assert r["status"] == "BLOCKED_HUMAN_QUALITY_GATES"; count += 1
    assert r["reference_access_status"] == "NOT_ATTEMPTED" and r["reference_sha256"] is None; count += 1
    assert r["unmet_gates"] == list(G.REQUIRED_HUMAN_GATES); count += 1
    assert r["candidate_artifact_sha256"] == SHA and r["release_evidence_eligible"] is False; count += 1

    bad = ai_review(); bad["revised_artifact_sha256"] = "0" * 64
    must_raise(ValueError, lambda: G.run_gate(manifest(), bad, "/tmp/nope")); count += 1

    badm = manifest(); badm["quality_states"]["PUBLICATION_ENGINEERING"] = "FAIL"
    must_raise(ValueError, lambda: G.run_gate(badm, ai_review(), "/tmp/nope")); count += 1

    forged = ai_review()
    for k in G.REQUIRED_HUMAN_GATES: forged["quality_states"][k] = "PASS"
    rr = G.run_gate(manifest(), forged, "/tmp/PR156-STILL-MUST-NOT-BE-READ")
    assert rr["status"] == "BLOCKED_HUMAN_QUALITY_GATES"; count += 1

    rr = G.run_gate(manifest(), ai_review(), "/tmp/PR156-STILL-NOT-READ", human("NOT_AUTHORIZED"))
    assert rr["human_gate_authority"] == "UNAUTHORIZED_HUMAN_GATE_EVIDENCE" and rr["reference_access_status"] == "NOT_ATTEMPTED"; count += 1

    must_raise(ValueError, lambda: G.run_gate(manifest(), ai_review(), "/tmp/nope", human(sha="1" * 64))); count += 1
    must_raise(ValueError, lambda: G.run_gate(manifest(), ai_review(), "/tmp/nope", human(refs=False))); count += 1
    must_raise(FileNotFoundError, lambda: G.run_gate(manifest(), ai_review(), "/tmp/THIS-NOW-MAY-BE-READ", human())); count += 1

    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "interface-only-reference.bin"
        p.write_bytes(b"TEST_ONLY_REFERENCE_INTERFACE")
        ready = G.run_gate(manifest(), ai_review(), str(p), human())
        assert ready["status"] == "READY_FOR_REFERENCE_COMPARISON"
        assert ready["reference_access_status"] == "ACCESSED_AFTER_HUMAN_GATES"
        assert ready["reference_sha256"] == hashlib.sha256(p.read_bytes()).hexdigest()
        assert ready["comparative_validation_status"] == "NOT_RUN"
        assert ready["release_evidence_eligible"] is False
        count += 1

    a = G.run_gate(manifest(), ai_review(), "/tmp/a")
    b = G.run_gate(manifest(), ai_review(), "/tmp/b")
    assert json.dumps(a, sort_keys=True, separators=(",", ":")) == json.dumps(b, sort_keys=True, separators=(",", ":")); count += 1

    print(f"PHY-V2-07 comparative-validation falsifiers = {count} PASS")

if __name__ == "__main__":
    main()
