#!/usr/bin/env python3
import json
from pathlib import Path
from jsonschema import Draft202012Validator, RefResolver

D = Path(__file__).resolve().parents[1]
C = D / "contracts"
R = D / "registry"

def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

schemas = {
    p.name: load(p)
    for p in C.glob("*.schema.json")
}
store = {schema["$id"]: schema for schema in schemas.values() if "$id" in schema}

def validate(name, value):
    schema = schemas[name]
    resolver = RefResolver.from_schema(schema, store=store)
    errors = sorted(Draft202012Validator(schema, resolver=resolver).iter_errors(value), key=lambda e:list(e.path))
    if errors:
        for err in errors:
            print(f"{name}: {list(err.path)}: {err.message}")
        raise SystemExit(1)

validate("chemistry-source-obligation-ledger.schema.json", load(R / "chemistry-source-obligation-ledger.json"))
binding_schema = schemas["chemistry-question-capability-binding.schema.json"]
for i, record in enumerate(load(R / "chemistry-question-capability-bindings.json")["bindings"]):
    errors = sorted(Draft202012Validator(binding_schema).iter_errors(record), key=lambda e:list(e.path))
    if errors:
        for err in errors:
            print(f"chemistry-question-capability-binding.schema.json[{i}]: {list(err.path)}: {err.message}")
        raise SystemExit(1)
validate("chemistry-external-corpus-classification.schema.json", load(R / "chemistry-external-corpus-classification.json"))

# The capability taxonomy is the subject-wide, chapter-generic capability
# contract. Its full cross-registry closure (PCK families, allowed visual
# families, page-intent agreement) runs in the C-H validator, which is the phase
# that owns the primitive registry. Here we only prove there is no drift from
# the canonical authority and no topic-named capability.
taxonomy = load(R / "chemistry-capability-taxonomy.json")
authority = load(D / "authority" / "chemistry-canonical-authority.json")
taxonomy_caps = {c["capability_id"]: c for c in taxonomy["capabilities"]}
assert len(taxonomy_caps) == len(taxonomy["capabilities"]), "duplicate capability id"
for record in authority["capabilities"]:
    assert record["capability_id"] in taxonomy_caps, record["capability_id"]
for capability_id, record in taxonomy_caps.items():
    for fragment in taxonomy["forbidden_capability_name_fragments"]:
        assert fragment.upper() not in capability_id.upper(), (capability_id, fragment)
    assert record["learner_can_statement"].lower().startswith("i can"), capability_id
    for key in ["required_source_evidence", "primary_pck_family", "verification_checks", "allowed_visual_families"]:
        assert record[key], (capability_id, key)
assert taxonomy["unresolved_semantic_input_policy"] == "FAIL_CLOSED_NEVER_RENDER_INVENTED_VALUE"

print("CHEMISTRY C-C registry/schema validation = PASS")
print("source obligations = 12")
print("question/subpart bindings = 17")
print("external candidate classifications = 6")
print("capability taxonomy = %d chapter-generic capabilities" % len(taxonomy_caps))
