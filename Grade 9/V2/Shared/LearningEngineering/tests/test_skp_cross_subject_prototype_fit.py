#!/usr/bin/env python3
"""Non-Physics stress tests for prototype-only shared SKP semantic contracts."""
import json
from pathlib import Path
from jsonschema import Draft202012Validator

HERE = Path(__file__).resolve()
ROOT, REPO = HERE.parents[1], HERE.parents[5]

def load(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def validator(name): return Draft202012Validator(load(ROOT/"prototypes"/"contracts"/name))

family_v=validator("skp-problem-family.prototype.schema.json")
reason_v=validator("skp-reasoning-sequence.prototype.schema.json")
rep_v=validator("skp-representation.prototype.schema.json")
verify_v=validator("skp-verification-route.prototype.schema.json")

# Mathematics: definition-based classification has a representation and reasoning route,
# but no formal relation object. Shared family semantics must not invent one.
math_shard=load(REPO/"Grade 9/V2/Mathematics/ProblemSemantics/registry/math-problem-family-registry-1.json")
math_family=next(x for x in math_shard["families"] if x["family_id"]=="MATH-PF-EUCLID-CLASSIFICATION")
math_routes=load(REPO/"Grade 9/V2/Mathematics/ProblemSemantics/registry/math-verification-route-registry.json")
math_route=next(x for x in math_routes["routes"] if x["verification_route_id"]==math_family["verification_route_ref"])
assert math_family["family_digest"]=="41d2de6efe3c2533990d083103bd501661534cb5576115ea1315d3bf5125f17e"
assert "relation_refs" not in math_family

math_rep={
 "schema_version":"0.1.0","prototype_only":True,
 "representation_id":"REP-MATH-NATURAL-LANGUAGE-STATEMENT","skp_ref":"SKP-MATH-EUCLID-CLASSIFICATION-PROTOTYPE",
 "title":"Natural-language mathematical statement","representation_kind":"TEXTUAL",
 "purpose":"Preserve the mathematical assertion while statement wording varies.",
 "encodes_refs":["FAMILY-MATH-EUCLID-CLASSIFICATION"],"decision_state":"CANDIDATE_ONLY","decision_basis_refs":[],
 "translation_invariants":math_family["representation_requirements"]["translation_invariants"],"translation_edges":[],
 "source_refs":["SRC-MATH-PROBLEM-FAMILY"],"source_representation_ref":"NATURAL_LANGUAGE_STATEMENT"}
rep_v.validate(math_rep)

math_reason={
 "schema_version":"0.1.0","prototype_only":True,"sequence_id":"REASON-MATH-EUCLID-CLASSIFICATION",
 "skp_ref":"SKP-MATH-EUCLID-CLASSIFICATION-PROTOTYPE","capability_refs":["CAP-MATH-EUCLID-CLASSIFY-AXIOM-POSTULATE"],
 "steps":[{
   "step_id":f"STEP-MATH-EUCLID-{i:02d}","semantic_role":s["role"],"semantic_job":s["semantic_job"],"semantic_job_state":"PRESENT",
   "subject_transition":{"kind":"MATHEMATICAL_TRANSITION","statement":s["mathematical_transition"]},
   "relation_refs":[],"representation_refs":["REP-MATH-NATURAL-LANGUAGE-STATEMENT"],
   "fragility":"UNRESOLVED","fragility_rationale":"Math source route does not authorize learner-fragility classification.",
   "source_step_ref":s["template_step_id"]} for i,s in enumerate(math_family["reasoning_route_template"],1)],
 "learner_support_authority":False,"source_refs":["SRC-MATH-PROBLEM-FAMILY"],"source_route_ref":math_family["family_id"]}
reason_v.validate(math_reason)
assert [s["subject_transition"]["statement"] for s in math_reason["steps"]]==[s["mathematical_transition"] for s in math_family["reasoning_route_template"]]

mc=math_route["checks"][0]
math_verify={
 "schema_version":"0.1.0","prototype_only":True,"verification_route_id":"VERIFY-MATH-EUCLID-CLASSIFICATION",
 "skp_ref":"SKP-MATH-EUCLID-CLASSIFICATION-PROTOTYPE","target_refs":["FAMILY-MATH-EUCLID-CLASSIFICATION","REASON-MATH-EUCLID-CLASSIFICATION"],
 "checks":[{"check_id":"CHECK-MATH-EUCLID-C01","check_kind":"LOGICAL_VALIDITY","statement":mc["acceptance_condition"],
            "acceptance_condition":mc["acceptance_condition"],"subject_target":mc["mathematical_target"],"source_check_type":mc["check_type"],
            "relation_refs":[],"independent_of_primary_route":False,
            "independence_rationale":"The source defines a criterion check, not an independent alternate proof.",
            "evidence_refs":["SRC-MATH-VERIFICATION"],"source_check_ref":mc["check_id"]}],
 "source_refs":["SRC-MATH-VERIFICATION"],"source_route_ref":math_route["verification_route_id"]}
verify_v.validate(math_verify)

math_projection={
 "schema_version":"0.1.0","prototype_only":True,"problem_family_id":"FAMILY-MATH-EUCLID-CLASSIFICATION",
 "skp_ref":"SKP-MATH-EUCLID-CLASSIFICATION-PROTOTYPE","title":"Euclidean statement classification",
 "structural_signature":math_family["problem_signature"]["mathematical_structure"],
 "capability_refs":["CAP-MATH-EUCLID-CLASSIFY-AXIOM-POSTULATE"],"concept_refs":[],"relation_refs":[],
 "reasoning_sequence_refs":["REASON-MATH-EUCLID-CLASSIFICATION"],"representation_refs":["REP-MATH-NATURAL-LANGUAGE-STATEMENT"],
 "verification_route_refs":["VERIFY-MATH-EUCLID-CLASSIFICATION"],"allowed_variations":math_family["allowed_variations"],
 "transfer_boundaries":math_family["transfer_boundaries"],"surface_cues_not_authority":True,
 "source_refs":["SRC-MATH-PROBLEM-FAMILY"],"source_family_ref":math_family["family_id"]}
family_v.validate(math_projection)
assert math_projection["relation_refs"]==[]

# Chemistry: a rule-with-exception family has neither a formal relation nor a required
# representation, and its repository reasoning route supplies governed role tokens but
# no semantic-job prose. The shared prototype must preserve that unresolved state.
chem_registry=load(REPO/"Grade 9/V2/Chemistry/ReasoningSemantics/registry/chemistry-problem-family-registry.json")
chem_family=next(x for x in chem_registry["families"] if x["family_id"]=="PF-RULE_WITH_EXCEPTION")
assert chem_registry["registry_id"]=="CHEM-C-D-PROBLEM-FAMILIES-v1"
assert chem_family["representation_requirements"]==[]
assert "relation_refs" not in chem_family

chem_reason={
 "schema_version":"0.1.0","prototype_only":True,"sequence_id":"REASON-CHEM-RULE-WITH-EXCEPTION",
 "skp_ref":"SKP-CHEM-RULE-WITH-EXCEPTION-PROTOTYPE","capability_refs":["CAP-CHEM-CHECK-RULE-EXCEPTION"],
 "steps":[{"step_id":f"STEP-CHEM-RULE-{i:02d}","semantic_role":role,"semantic_job":None,"semantic_job_state":"UNRESOLVED",
           "subject_transition":None,"relation_refs":[],"representation_refs":[],"fragility":"UNRESOLVED",
           "fragility_rationale":"Chemistry source route supplies a role token but no authorized learner-fragility or semantic-job gloss.",
           "source_step_ref":f"ROLE:{role}"} for i,role in enumerate(chem_family["reasoning_route_template"],1)],
 "learner_support_authority":False,"source_refs":["SRC-CHEM-PROBLEM-FAMILY"],"source_route_ref":chem_family["family_id"]}
reason_v.validate(chem_reason)
assert all(s["semantic_job"] is None and s["semantic_job_state"]=="UNRESOLVED" for s in chem_reason["steps"])

chem_verify={
 "schema_version":"0.1.0","prototype_only":True,"verification_route_id":"VERIFY-CHEM-RULE-WITH-EXCEPTION",
 "skp_ref":"SKP-CHEM-RULE-WITH-EXCEPTION-PROTOTYPE","target_refs":["FAMILY-CHEM-RULE-WITH-EXCEPTION","REASON-CHEM-RULE-WITH-EXCEPTION"],
 "checks":[{"check_id":f"CHECK-CHEM-RULE-{i:02d}","check_kind":"OTHER","statement":token,
            "acceptance_condition":None,"subject_target":None,"source_check_type":token,"relation_refs":[],
            "independent_of_primary_route":False,"independence_rationale":"The source supplies a verification token, not an independent alternate derivation.",
            "evidence_refs":["SRC-CHEM-PROBLEM-FAMILY"],"source_check_ref":token} for i,token in enumerate(chem_family["verification_route"],1)],
 "source_refs":["SRC-CHEM-PROBLEM-FAMILY"],"source_route_ref":chem_family["family_id"]}
verify_v.validate(chem_verify)

chem_projection={
 "schema_version":"0.1.0","prototype_only":True,"problem_family_id":"FAMILY-CHEM-RULE-WITH-EXCEPTION",
 "skp_ref":"SKP-CHEM-RULE-WITH-EXCEPTION-PROTOTYPE","title":"Rule with explicit exception",
 "structural_signature":chem_family["chemical_signature"],"capability_refs":["CAP-CHEM-CHECK-RULE-EXCEPTION"],
 "concept_refs":[],"relation_refs":[],"reasoning_sequence_refs":["REASON-CHEM-RULE-WITH-EXCEPTION"],"representation_refs":[],
 "verification_route_refs":["VERIFY-CHEM-RULE-WITH-EXCEPTION"],"allowed_variations":chem_family["allowed_variations"],
 "transfer_boundaries":chem_family["transfer_boundaries"],"surface_cues_not_authority":True,
 "source_refs":["SRC-CHEM-PROBLEM-FAMILY"],"source_family_ref":chem_family["family_id"]}
family_v.validate(chem_projection)
assert chem_projection["relation_refs"]==[] and chem_projection["representation_refs"]==[]

print("Shared SKP cross-subject prototype fit: PASS (Math definition/classification + Chemistry rule/exception without invented relations or representations)")
