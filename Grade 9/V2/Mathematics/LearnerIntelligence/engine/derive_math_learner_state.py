#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, sys
from pathlib import Path

INDEPENDENT = {"INDEPENDENT_SUCCESS", "INDEPENDENT_FAILURE"}
FAILURE = {"INDEPENDENT_FAILURE", "GUIDED_FAILURE"}
AMBIGUOUS = {"AMBIGUOUS"}
FORBIDDEN_VIEW_KEYS = {
    "RETEACH","REPAIR_BEFORE","REPAIR_IN_UNIT","PROBE_FIRST","COMPRESS",
    "USE_AS_ENTRY_POINT","INCLUDE_CONTRAST","HINT_RUNG","practice_count",
    "teaching_sequence","page_layout"
}

def canonical_bytes(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

def digest(obj):
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()

def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def validate_interface(interface, evidence):
    if interface.get("privacy_class") != "PUBLIC_SYNTHETIC":
        raise ValueError("canonical interface fixture must be PUBLIC_SYNTHETIC")
    allowed_caps = set(interface["capability_refs"])
    allowed_probes = set(interface["probe_refs"])
    allowed_checkpoints = set(interface["checkpoint_refs"])
    for r in evidence["records"]:
        if r["capability_ref"] not in allowed_caps:
            raise ValueError(f"unknown capability ref: {r['capability_ref']}")
        if r["checkpoint_ref"] not in allowed_checkpoints:
            raise ValueError(f"unknown checkpoint ref: {r['checkpoint_ref']}")
        for c in r["candidate_capability_refs"]:
            if c not in allowed_caps:
                raise ValueError(f"unknown candidate capability ref: {c}")
        if r.get("probe_ref") and r["probe_ref"] not in allowed_probes:
            raise ValueError(f"unknown probe ref: {r['probe_ref']}")

def derive(interface, evidence):
    if evidence.get("privacy_class") != "PUBLIC_SYNTHETIC":
        raise ValueError("only PUBLIC_SYNTHETIC fixtures are accepted by this subject acceptance engine")
    if not str(evidence.get("learner_ref","")).startswith("SYNTHETIC-"):
        raise ValueError("real learner references are forbidden")
    validate_interface(interface, evidence)

    observations=[]
    for r in sorted(evidence["records"], key=lambda x: x["evidence_id"]):
        observations.append({
            "observation_id": "OBS-" + r["evidence_id"],
            "evidence_ref": r["evidence_id"],
            "checkpoint_ref": r["checkpoint_ref"],
            "capability_ref": r["capability_ref"],
            "evidence_class": r["evidence_class"],
            "independent": r["evidence_class"] in INDEPENDENT,
        })

    by_cap={c: [] for c in interface["capability_refs"]}
    for r in evidence["records"]:
        by_cap[r["capability_ref"]].append(r)

    states=[]
    for cap in sorted(interface["capability_refs"]):
        rows=by_cap[cap]
        indep_success=any(r["evidence_class"]=="INDEPENDENT_SUCCESS" for r in rows)
        ordinary_failure=any(r["evidence_class"]=="INDEPENDENT_FAILURE" for r in rows)
        guided_or_prompted_success=any(r["evidence_class"] in {"GUIDED_SUCCESS","VERIFICATION_PROMPTED_SUCCESS"} for r in rows)
        ambiguous=any(r["evidence_class"]=="AMBIGUOUS" for r in rows)

        if indep_success and not ordinary_failure and not ambiguous:
            state="READY"
        elif rows and (ordinary_failure or guided_or_prompted_success):
            state="DEVELOPING"
        elif ambiguous:
            state="UNKNOWN"
        else:
            state="UNKNOWN"

        states.append({"capability_ref":cap,"state":state,"evidence_refs":sorted(r["evidence_id"] for r in rows)})

    diagnostics=[]
    for r in sorted(evidence["records"], key=lambda x:x["evidence_id"]):
        if r["evidence_class"] in FAILURE | AMBIGUOUS or r["evidence_class"]=="VERIFICATION_NOT_INITIATED":
            candidates=r["candidate_capability_refs"] or [r["capability_ref"]]
            probe_required = r["evidence_class"]=="AMBIGUOUS" or len(candidates) > 1
            if r["evidence_class"]=="INDEPENDENT_FAILURE" and r.get("probe_ref"):
                probe_required=True
            diagnostics.append({
                "diagnostic_case_id":"DC-"+r["evidence_id"],
                "evidence_refs":[r["evidence_id"]],
                "candidate_capability_refs":sorted(candidates),
                "hypothesis_status":"UNRESOLVED" if r["evidence_class"]=="AMBIGUOUS" else "SUSPECTED",
                "probe_required":probe_required,
                "probe_ref":r.get("probe_ref") if probe_required else None,
            })

    verify_rows=[r for r in evidence["records"] if r["capability_ref"]=="MATH-SOLUTION-VERIFICATION"]
    verification_behavior={
        "can_verify_when_prompted": any(r["evidence_class"]=="VERIFICATION_PROMPTED_SUCCESS" for r in verify_rows),
        "self_initiated_verification": any(r["checkpoint_ref"]=="VERIFY_INITIATION" and r["evidence_class"]=="INDEPENDENT_SUCCESS" for r in verify_rows),
        "evidence_refs":sorted(r["evidence_id"] for r in verify_rows),
    }

    semantic_core={
        "state_id":"MATH-V2-02-STATE-SYNTHETIC",
        "privacy_class":"PUBLIC_SYNTHETIC",
        "as_of":evidence["as_of"],
        "capability_states":states,
        "verification_behavior":verification_behavior,
    }
    semantic_core["semantic_digest"]=digest(semantic_core)
    view={
        "view_id":"MATH-V2-02-RESEARCH-VIEW-SYNTHETIC",
        "privacy_class":"PUBLIC_SYNTHETIC",
        "state_digest":semantic_core["semantic_digest"],
        "capability_states":states,
        "diagnostic_cases":diagnostics,
        "verification_behavior":verification_behavior,
    }
    if FORBIDDEN_VIEW_KEYS.intersection(view.keys()):
        raise AssertionError("descriptive view contains downstream decision keys")
    return {"observations":observations,"diagnostic_cases":diagnostics,"state":semantic_core,"research_learner_view":view}

def main():
    if len(sys.argv) != 4:
        raise SystemExit("usage: derive_math_learner_state.py canonical_interface.json learner_evidence.json output.json")
    out=derive(load(sys.argv[1]),load(sys.argv[2]))
    Path(sys.argv[3]).write_bytes(canonical_bytes(out)+b"\n")

if __name__ == "__main__":
    main()
