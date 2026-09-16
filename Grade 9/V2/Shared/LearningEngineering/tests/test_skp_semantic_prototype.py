#!/usr/bin/env python3
"""Falsifiers for prototype-only shared SKP semantic contracts and one exact Physics projection."""
import copy, json
from pathlib import Path
from jsonschema import Draft202012Validator, ValidationError

HERE = Path(__file__).resolve()
ROOT, REPO = HERE.parents[1], HERE.parents[5]

def load(p): return json.loads(Path(p).read_text(encoding="utf-8"))

FILES = {
 "identity":"contracts/skp-identity.schema.json",
 "scope":"contracts/skp-scope.schema.json",
 "curriculum":"contracts/skp-curriculum-binding.schema.json",
 "capability":"contracts/skp-capability.schema.json",
 "source_plan":"contracts/skp-source-plan.schema.json",
 "source_record":"contracts/skp-source-record.schema.json",
 "concept":"prototypes/contracts/skp-concept.prototype.schema.json",
 "relation":"prototypes/contracts/skp-relation.prototype.schema.json",
 "reasoning":"prototypes/contracts/skp-reasoning-sequence.prototype.schema.json",
 "representation":"prototypes/contracts/skp-representation.prototype.schema.json",
 "verification":"prototypes/contracts/skp-verification-route.prototype.schema.json",
 "family":"prototypes/contracts/skp-problem-family.prototype.schema.json",
}
V={k:Draft202012Validator(load(ROOT/v)) for k,v in FILES.items()}
def check(k,x): V[k].validate(x)
def schema_fail(k,x):
    try: check(k,x)
    except ValidationError: return
    raise AssertionError(f"expected {k} schema failure")

def validate(bundle, cap_ids, src_ids):
    groups=(("concepts","concept","concept_id"),("relations","relation","relation_id"),
            ("representations","representation","representation_id"),
            ("reasoning_sequences","reasoning","sequence_id"),
            ("verification_routes","verification","verification_route_id"),
            ("problem_families","family","problem_family_id"))
    idx={}
    skp=bundle.get("skp_ref") or bundle["identity"]["skp_id"]
    for group,kind,key in groups:
        rows=bundle[group]
        for x in rows: check(kind,x)
        ids=[x[key] for x in rows]
        assert len(ids)==len(set(ids)), f"duplicate {kind} IDs"
        idx[kind]={x[key]:x for x in rows}
        for x in rows:
            assert x["skp_ref"]==skp
            assert set(x["source_refs"])<=src_ids
    for r in idx["relation"].values():
        assert set(r["concept_refs"])<=set(idx["concept"])
        assert set(r["capability_refs"])<=cap_ids
        for c in r["applicability_conditions"]: assert set(c["evidence_refs"])<=src_ids
    for r in idx["representation"].values():
        for e in r["translation_edges"]:
            assert e["target_representation_ref"] in idx["representation"]
            assert set(e["capability_refs"])<=cap_ids
            assert set(e["evidence_refs"])<=src_ids
    for r in idx["reasoning"].values():
        assert set(r["capability_refs"])<=cap_ids
        assert len({s["step_id"] for s in r["steps"]})==len(r["steps"])
        for s in r["steps"]:
            assert set(s["relation_refs"])<=set(idx["relation"])
            assert set(s["representation_refs"])<=set(idx["representation"])
    targets=set(idx["relation"])|set(idx["reasoning"])|set(idx["family"])|cap_ids|set(idx["concept"])
    for r in idx["verification"].values():
        assert set(r["target_refs"])<=targets
        for c in r["checks"]:
            assert set(c["relation_refs"])<=set(idx["relation"])
            assert set(c["evidence_refs"])<=src_ids
    for f in idx["family"].values():
        assert set(f["capability_refs"])<=cap_ids
        assert set(f["concept_refs"])<=set(idx["concept"])
        assert set(f["relation_refs"])<=set(idx["relation"])
        assert set(f["reasoning_sequence_refs"])<=set(idx["reasoning"])
        assert set(f["representation_refs"])<=set(idx["representation"])
        assert set(f["verification_route_refs"])<=set(idx["verification"])
    return idx

foundation=load(ROOT/"fixtures/skp-pilot-kernel.synthetic.fixture.json")
synthetic=load(ROOT/"prototypes/fixtures/skp-semantic-prototype.synthetic.fixture.json")
caps={x["capability_id"] for x in foundation["capabilities"]}
srcs={x["source_id"] for x in foundation["source_ledger"]}
validate(synthetic,caps,srcs)

bad=copy.deepcopy(synthetic["reasoning_sequences"][0]); bad["steps"][0]["hint_text"]="do the subtraction"; schema_fail("reasoning",bad)
bad=copy.deepcopy(synthetic["reasoning_sequences"][0]); bad["steps"][0]["fragility"]="HIGH"; bad["steps"][0]["fragility_rationale"]=""; schema_fail("reasoning",bad)
bad=copy.deepcopy(synthetic["representations"][0]); bad["decision_basis_refs"]=[]; schema_fail("representation",bad)
bad=copy.deepcopy(synthetic["problem_families"][0]); bad["surface_cues_not_authority"]=False; schema_fail("family",bad)

schema_text="\n".join((ROOT/p).read_text(encoding="utf-8") for k,p in FILES.items() if k in {"concept","relation","reasoning","representation","verification","family"}).upper()
for forbidden in ("PHYSICS","RELATIVE_G","SBA04","SBA23","Q14","Q27"): assert forbidden not in schema_text

pilot=load(ROOT/"pilots/physics-relative-g-cancellation.standard.prototype.json")
assert pilot["prototype_only"] is True and pilot["runtime_authority"] is False and pilot["promotion_state"]=="HELD"
check("identity",pilot["identity"]); check("scope",pilot["scope"])
for x in pilot["curriculum_bindings"]: check("curriculum",x)
for x in pilot["capabilities"]: check("capability",x)
check("source_plan",pilot["source_plan"])
for x in pilot["source_ledger"]: check("source_record",x)
pcaps={x["capability_id"] for x in pilot["capabilities"]}
psrcs={x["source_id"] for x in pilot["source_ledger"]}
idx=validate(pilot,pcaps,psrcs)

sb=pilot["source_bindings"]["assessment_scope"]; sa=load(REPO/sb["path"])
assert sa["authority_id"]==sb["authority_id"] and sa["authority_digest"]==sb["authority_digest"]
cap=next(x for x in sa["capabilities"] if x["capability_id"]==sb["capability_ref"])
con=next(x for x in sa["concepts"] if x["concept_id"]==sb["concept_ref"])
assert pilot["capabilities"][0]["title"]==cap["title"] and sb["concept_ref"] in cap["concept_refs"]
assert pilot["concepts"][0]["title"]==con["title"] and pilot["concepts"][0]["source_object_ref"]==con["concept_id"]

fb=pilot["source_bindings"]["problem_family"]; fr=load(REPO/fb["path"])
fam=next(x for x in fr["families"] if x["family_id"]==fb["family_ref"])
assert fam["family_digest"]==fb["family_digest"] and cap["capability_id"] in fam["canonical_capability_refs"]
pf=pilot["problem_families"][0]
assert pf["source_family_ref"]==fam["family_id"]
assert pf["structural_signature"]==fam["physical_signature"]
assert pf["allowed_variations"]==fam["allowed_variations"] and pf["transfer_boundaries"]==fam["transfer_boundaries"]

rel=pilot["relations"][0]
assert rel["source_relation_ref"] in fam["law_refs"] and rel["formal_expression"] in fam["invariants"][0]
assert {x["statement"] for x in rel["applicability_conditions"]}==set(fam["model_validity_conditions"])
rep=pilot["representations"][0]
assert rep["source_representation_ref"] in fam["representation_requirements"]["required_refs"]
assert rep["decision_state"]=="CANDIDATE_ONLY" and rep["translation_edges"]==[]

steps=pilot["reasoning_sequences"][0]["steps"]
assert len(steps)==len(fam["reasoning_route_template"])
for p,s in zip(steps,fam["reasoning_route_template"]):
    assert (p["source_step_ref"],p["semantic_role"],p["semantic_job"])==(s["template_step_id"],s["role"],s["semantic_job"])
    assert p["fragility"]=="UNRESOLVED"

vb=pilot["source_bindings"]["verification_route"]; vr=load(REPO/vb["path"])
route=next(x for x in vr["routes"] if x["verification_route_id"]==vb["route_ref"])
assert route["route_digest"]==vb["route_digest"] and route["family_ref"]==fam["family_id"]
checks={x["check_id"]:x for x in route["checks"]}
for p in pilot["verification_routes"][0]["checks"]: assert p["statement"]==checks[p["source_check_ref"]]["physical_check"]

assert not [a for s in pilot["source_ledger"] for a in s["intent_assessments"]
            if a["source_intent"]=="CURRICULUM_AUTHORITY" and a["authority_disposition"]=="PROMOTED_FOR_INTENT"]
assert pilot["curriculum_bindings"][0]["classification"]=="UNRESOLVED"
assert pilot["curriculum_bindings"][0]["binding_state"]=="UNRESOLVED"
assert set(pilot["hold_reasons"])=={
 "CURRICULUM_AUTHORITY_UNRESOLVED","REPRESENTATION_DECISION_UNRESOLVED",
 "REPRESENTATION_TRANSLATION_UNRESOLVED","REASONING_FRAGILITY_UNRESOLVED"}

print("Shared SKP semantic prototype: PASS (6 prototype contracts + synthetic falsifiers + exact Physics relative-g projection; runtime authority false and promotion HELD)")
