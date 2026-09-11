#!/usr/bin/env python3
from __future__ import annotations
import copy, importlib.util, json
from pathlib import Path
HERE=Path(__file__).resolve().parent
SPEC=importlib.util.spec_from_file_location("resolve_canonical",HERE/"resolve_canonical.py"); mod=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(mod)
def load(rel): return json.loads((HERE/rel).read_text())
def expect_error(registry,needle):
    try: mod.validate_registry(registry)
    except mod.CanonicalError as exc: assert needle in str(exc),(needle,str(exc))
    else: raise AssertionError(f"expected CanonicalError containing {needle!r}")
def main():
    registry=load("fixtures/valid/registry.json"); request=load("fixtures/valid/request.json")
    first=mod.resolve_canonical(registry,request); second=mod.resolve_canonical(copy.deepcopy(registry),copy.deepcopy(request))
    assert first["status"]=="SUCCESS" and mod.render_bytes(first)==mod.render_bytes(second)
    assert [x["canonical_id"] for x in first["primary_assets"]]==["SYN-CHEM-A","SYN-PHYS-B"]
    dep_ids=[x["canonical_id"] for x in first["dependency_assets"]]; assert dep_ids==["SYN-MATH-PROP","SYN-MATH-RATIO"] and dep_ids.count("SYN-MATH-PROP")==1
    assert first["canonical_registry_version"]=="SYN-REG-1" and all(len(x["semantic_digest"])==64 for x in first["primary_assets"]+first["dependency_assets"])
    assert any(r["canonical_id"]=="SYN-PHYS-B" and r["action"]=="REVALIDATE" for r in first["resolution_records"])
    missing=load("fixtures/invalid/registry_missing_dependency.json"); gap1=mod.resolve_canonical(missing,request); gap2=mod.resolve_canonical(copy.deepcopy(missing),copy.deepcopy(request)); assert gap1==gap2 and gap1["status"]=="CANONICAL_GAP" and gap1["gap_candidates"][0]["resolution_failure"]=="MISSING_ASSET" and gap1["gap_candidates"][0]["status"]=="OPEN"
    unpromoted=load("fixtures/invalid/registry_unpromoted_dependency.json"); gap=mod.resolve_canonical(unpromoted,request); assert gap["status"]=="CANONICAL_GAP" and any(g["resolution_failure"]=="NOT_PROMOTED" for g in gap["gap_candidates"])
    expect_error(load("fixtures/invalid/registry_cycle.json"),"dependency cycle")
    expect_error(load("fixtures/invalid/registry_digest_mismatch.json"),"semantic digest mismatch")
    expect_error(load("fixtures/invalid/registry_learner_contamination.json"),"forbidden producer field")
    expect_error(load("fixtures/invalid/registry_benchmark_contamination.json"),"forbidden producer field")
    bad=copy.deepcopy(request); bad["learner_state"]={"x":1}
    try: mod.resolve_canonical(registry,bad)
    except mod.CanonicalError: pass
    else: raise AssertionError("learner-contaminated request unexpectedly accepted")
    projection=dict(first); digest=projection.pop("knowledge_set_digest"); assert digest==mod.sha256_obj(projection)
    for gate in ["CORE1_CONTRACT_LOGIC","DEPENDENCY_CLOSURE","SHARED_DEPENDENCY_DEDUPLICATION","CANONICAL_GAP_CANDIDATE","UNPROMOTED_ASSET_BLOCK","DEPENDENCY_CYCLE_REJECTION","DIGEST_DRIFT_REJECTION","LEARNER_CONTAMINATION_REJECTION","BENCHMARK_CONTAMINATION_REJECTION","DETERMINISTIC_KNOWLEDGE_SET"]: print(f"{gate} = PASS")
if __name__=="__main__": main()
