#!/usr/bin/env python3
"""Pilot falsifiers for foundational shared SKP contracts.

The fixture is deliberately synthetic. No real topic or subject case may define shared semantics.
"""
import copy
import json
from pathlib import Path

from jsonschema import Draft202012Validator, ValidationError

HERE = Path(__file__).resolve()
ROOT = HERE.parents[1]
FIXTURE = ROOT / "fixtures" / "skp-pilot-kernel.synthetic.fixture.json"

SCHEMAS = {
    "identity": "skp-identity.schema.json",
    "scope": "skp-scope.schema.json",
    "curriculum": "skp-curriculum-binding.schema.json",
    "capability": "skp-capability.schema.json",
    "edge": "skp-prerequisite-edge.schema.json",
    "source_plan": "skp-source-plan.schema.json",
    "source_record": "skp-source-record.schema.json",
}


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


validators = {
    key: Draft202012Validator(load(ROOT / "contracts" / filename))
    for key, filename in SCHEMAS.items()
}


def check(kind, obj):
    validators[kind].validate(obj)


def expect_schema_failure(kind, obj):
    try:
        check(kind, obj)
    except ValidationError:
        return
    raise AssertionError(f"expected {kind} schema failure")


def semantic_validate(pkg):
    check("identity", pkg["identity"])
    check("scope", pkg["scope"])
    for x in pkg["curriculum_bindings"]:
        check("curriculum", x)
    for x in pkg["capabilities"]:
        check("capability", x)
    for x in pkg["prerequisite_edges"]:
        check("edge", x)
    check("source_plan", pkg["source_plan"])
    for x in pkg["source_ledger"]:
        check("source_record", x)

    skp_id = pkg["identity"]["skp_id"]
    if pkg["scope"]["skp_ref"] != skp_id:
        raise ValueError("SKP_SCOPE_IDENTITY_MISMATCH")

    source_ids = [x["source_id"] for x in pkg["source_ledger"]]
    if len(source_ids) != len(set(source_ids)):
        raise ValueError("SKP_DUPLICATE_SOURCE_ID")
    sources = {x["source_id"]: x for x in pkg["source_ledger"]}

    include_ids = {x["scope_item_id"] for x in pkg["scope"]["includes"]}
    exclude_ids = {x["scope_item_id"] for x in pkg["scope"]["excludes"]}
    scope_item_ids = include_ids | exclude_ids
    if len(scope_item_ids) != len(pkg["scope"]["includes"]) + len(pkg["scope"]["excludes"]):
        raise ValueError("SKP_DUPLICATE_SCOPE_ITEM_ID")

    for item in pkg["scope"]["includes"] + pkg["scope"]["excludes"]:
        if not set(item["evidence_refs"]) <= set(source_ids):
            raise ValueError("SKP_SCOPE_EVIDENCE_UNRESOLVED")

    for binding in pkg["curriculum_bindings"]:
        if binding["skp_ref"] != skp_id:
            raise ValueError("SKP_CURRICULUM_IDENTITY_MISMATCH")
        if not set(binding["scope_refs"]) <= scope_item_ids:
            raise ValueError("SKP_CURRICULUM_SCOPE_UNRESOLVED")
        if not set(binding["evidence_refs"]) <= set(source_ids):
            raise ValueError("SKP_CURRICULUM_EVIDENCE_UNRESOLVED")

    capability_ids = [x["capability_id"] for x in pkg["capabilities"]]
    if len(capability_ids) != len(set(capability_ids)):
        raise ValueError("SKP_DUPLICATE_CAPABILITY_ID")
    capabilities = {x["capability_id"]: x for x in pkg["capabilities"]}
    for capability in pkg["capabilities"]:
        if capability["skp_ref"] != skp_id:
            raise ValueError("SKP_CAPABILITY_IDENTITY_MISMATCH")
        if not set(capability["scope_refs"]) <= include_ids:
            raise ValueError("SKP_CAPABILITY_SCOPE_UNRESOLVED")
        if not set(capability["source_refs"]) <= set(source_ids):
            raise ValueError("SKP_CAPABILITY_SOURCE_UNRESOLVED")

    edge_ids = [x["edge_id"] for x in pkg["prerequisite_edges"]]
    if len(edge_ids) != len(set(edge_ids)):
        raise ValueError("SKP_DUPLICATE_EDGE_ID")
    for edge in pkg["prerequisite_edges"]:
        if edge["skp_ref"] != skp_id:
            raise ValueError("SKP_EDGE_IDENTITY_MISMATCH")
        if edge["prerequisite_ref"] not in capabilities or edge["target_ref"] not in capabilities:
            raise ValueError("SKP_EDGE_CAPABILITY_UNRESOLVED")
        if edge["prerequisite_ref"] == edge["target_ref"]:
            raise ValueError("SKP_SELF_PREREQUISITE")
        if not set(edge["evidence_refs"]) <= set(source_ids):
            raise ValueError("SKP_EDGE_EVIDENCE_UNRESOLVED")
        if not set(edge["progression_evidence_refs"]) <= set(source_ids):
            raise ValueError("SKP_PROGRESSION_EVIDENCE_UNRESOLVED")
        if edge["hardness"] == "HARD" and edge["missing_behavior"] == "NO_BLOCK":
            raise ValueError("SKP_HARD_PREREQUISITE_CANNOT_NO_BLOCK")

    # Directed cycle falsifier. A future policy may permit explicitly typed cycles, but silent cycles are invalid.
    graph = {cap: [] for cap in capabilities}
    for edge in pkg["prerequisite_edges"]:
        graph[edge["prerequisite_ref"]].append(edge["target_ref"])
    visiting, visited = set(), set()

    def dfs(node):
        if node in visiting:
            raise ValueError("SKP_PREREQUISITE_CYCLE")
        if node in visited:
            return
        visiting.add(node)
        for nxt in graph[node]:
            dfs(nxt)
        visiting.remove(node)
        visited.add(node)

    for cap in graph:
        dfs(cap)

    target_refs = {skp_id} | scope_item_ids | set(capability_ids) | set(edge_ids)
    if pkg["source_plan"]["skp_ref"] != skp_id:
        raise ValueError("SKP_SOURCE_PLAN_IDENTITY_MISMATCH")
    for obligation in pkg["source_plan"]["obligations"]:
        if not set(obligation["target_refs"]) <= target_refs | {x["binding_id"] for x in pkg["curriculum_bindings"]}:
            raise ValueError("SKP_SOURCE_PLAN_TARGET_UNRESOLVED")
        if obligation["required"]:
            satisfied = False
            for source in pkg["source_ledger"]:
                for assessment in source["intent_assessments"]:
                    if assessment["source_intent"] != obligation["source_intent"]:
                        continue
                    if assessment["authority_disposition"] != "PROMOTED_FOR_INTENT":
                        continue
                    if set(obligation["target_refs"]) <= set(assessment["target_refs"]):
                        satisfied = True
            if not satisfied:
                raise ValueError("SKP_REQUIRED_SOURCE_OBLIGATION_UNSATISFIED")

    return True


def expect_semantic_failure(code, pkg):
    try:
        semantic_validate(pkg)
    except ValueError as exc:
        assert str(exc) == code, (code, str(exc))
        return
    raise AssertionError(f"expected semantic failure {code}")


base = load(FIXTURE)
assert semantic_validate(base)

# Shared identity does not whitelist a Physics ontology. Current subject names and future adapters use the same contract.
for subject in ("PHYSICS", "MATHEMATICS", "CHEMISTRY"):
    x = copy.deepcopy(base["identity"])
    x["subject"] = subject
    check("identity", x)

# External-domain edges require provider-owned authority rather than remembered cross-domain knowledge.
external = copy.deepcopy(base["prerequisite_edges"][0])
external["edge_id"] = "EDGE-EXTERNAL-PROVIDER"
external["edge_type"] = "EXTERNAL_DOMAIN_PREREQUISITE"
external["provider_owner"] = None
expect_schema_failure("edge", external)
external["provider_owner"] = {"subject": "MATHEMATICS", "authority_ref": "provider://math/test"}
check("edge", external)

# Empirical progression claims require progression evidence; a structural edge cannot promote itself.
empirical = copy.deepcopy(base["prerequisite_edges"][0])
empirical["progression_status"] = "EMPIRICALLY_SUPPORTED_PROGRESSION"
empirical["progression_evidence_refs"] = []
expect_schema_failure("edge", empirical)

# A promoted source must explain why it is selected for that purpose.
bad_source = copy.deepcopy(base["source_ledger"][0])
bad_source["intent_assessments"][0]["selection_reason"] = "short"
expect_schema_failure("source_record", bad_source)

# Duplicate stable identity is not repaired by list order.
dup_cap = copy.deepcopy(base)
dup_cap["capabilities"].append(copy.deepcopy(dup_cap["capabilities"][0]))
expect_semantic_failure("SKP_DUPLICATE_CAPABILITY_ID", dup_cap)

# Missing references remain explicit rather than being guessed from names.
bad_ref = copy.deepcopy(base)
bad_ref["prerequisite_edges"][0]["target_ref"] = "CAP-REMEMBERED-TARGET"
expect_semantic_failure("SKP_EDGE_CAPABILITY_UNRESOLVED", bad_ref)

# A HARD prerequisite cannot simultaneously claim that absence has no effect.
bad_hardness = copy.deepcopy(base)
bad_hardness["prerequisite_edges"][0]["missing_behavior"] = "NO_BLOCK"
expect_semantic_failure("SKP_HARD_PREREQUISITE_CANNOT_NO_BLOCK", bad_hardness)

# Silent cycles are rejected.
cycle = copy.deepcopy(base)
reverse = copy.deepcopy(cycle["prerequisite_edges"][0])
reverse["edge_id"] = "EDGE-APPLY-BEFORE-INTERPRET"
reverse["prerequisite_ref"] = "CAP-APPLY-RELATION"
reverse["target_ref"] = "CAP-INTERPRET-RELATION"
cycle["prerequisite_edges"].append(reverse)
expect_semantic_failure("SKP_PREREQUISITE_CYCLE", cycle)

# Removing the exact promoted curriculum source leaves the required source obligation open; no fallback is invented.
missing_authority = copy.deepcopy(base)
missing_authority["source_ledger"] = [s for s in missing_authority["source_ledger"] if s["source_id"] != "SRC-CURRICULUM"]
expect_semantic_failure("SKP_SCOPE_EVIDENCE_UNRESOLVED", missing_authority)

print("Shared SKP pilot kernel: PASS (7 foundational contracts + 8 falsifiers; synthetic topic-neutral fixture)")
