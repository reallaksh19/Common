#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))
from validate_gravity_research_v1 import GravityResearchValidationError, load, validate  # noqa: E402

REQUEST = load("fixtures/engineering-workbench/grav-field-request.v1.json")
DISCOVERY = load("fixtures/engineering-workbench/grav-field-discovery.v1.json")
MANIFEST = load("fixtures/engineering-workbench/grav-field-manifest.v1.json")
DOSSIER = load("fixtures/engineering-workbench/grav-field-research-dossier.v1.json")
LEDGER = load("fixtures/engineering-workbench/grav-field-claim-ledger.v1.json")
EXTENSION = load("policy/physics-technical-engineering-gates.gravity.v1.json")


def must_fail(request, discovery, manifest, dossier, ledger, code):
    try:
        validate(request, discovery, manifest, dossier, ledger)
    except GravityResearchValidationError as exc:
        assert exc.code == code, (code, exc.code, str(exc))
        return
    raise AssertionError(f"expected {code}")


def gate(extension, gate_id):
    return next(item for item in extension["gates"] if item["subtopic_id"] == gate_id)


def manifest_with_extension(extension, name):
    rel = f"/tmp/{name}.json"
    Path(rel).write_text(json.dumps(extension, indent=2), encoding="utf-8")
    manifest = copy.deepcopy(MANIFEST)
    manifest["gate_extension_refs"] = [rel]
    return manifest


# Positive: a RESEARCH request reaches ENGINEERING_READY only through discovery, claim provenance and exact closure.
result = validate(REQUEST, DISCOVERY, MANIFEST, DOSSIER, LEDGER)
assert result["status"] == "PASS"
assert result["gravity_gates"] == ["PHY-GRAV-FIELD", "PHY-GRAV-FORCE"]
assert result["claim_count"] == 9
assert result["closure_gate_count"] == 10
assert result["closure_digest"].startswith("sha256:")

# Falsifier 1: inverse-square field semantics cannot disappear from the new field gate.
bad_extension = copy.deepcopy(EXTENSION)
gate(bad_extension, "PHY-GRAV-FIELD")["required_invariants"].remove("INV-GRAV-FIELD-INVERSE-SQUARE")
must_fail(REQUEST, DISCOVERY, manifest_with_extension(bad_extension, "grav-no-inverse-square"), DOSSIER, LEDGER, "E_GRAV_GATE_INVARIANT")

# Falsifier 2: superposition relation cannot disappear while its technical representation still depends on it.
bad_extension = copy.deepcopy(EXTENSION)
g = gate(bad_extension, "PHY-GRAV-FIELD")
g["relations"] = [r for r in g["relations"] if r["relation_id"] != "EQ-GRAV-FIELD-SUPERPOSITION"]
must_fail(REQUEST, DISCOVERY, manifest_with_extension(bad_extension, "grav-no-superposition"), DOSSIER, LEDGER, "E_GRAV_GATE_INVARIANT")

# Falsifier 3: field may not be silently EXTENDed into NLM; the reviewed decision is CREATE_CHILD.
bad_discovery = copy.deepcopy(DISCOVERY)
field_op = next(op for op in bad_discovery["operations"] if op["gate_id"] == "PHY-GRAV-FIELD")
field_op["operation"] = "EXTEND"
must_fail(REQUEST, bad_discovery, MANIFEST, DOSSIER, LEDGER, "E_GRAV_DISCOVERY")

# Falsifier 4: field ownership must remain downstream of gravitational force.
bad_discovery = copy.deepcopy(DISCOVERY)
field_op = next(op for op in bad_discovery["operations"] if op["gate_id"] == "PHY-GRAV-FIELD")
field_op["parent_gate_id"] = "PHY-NLM-SECOND-LAW"
must_fail(REQUEST, bad_discovery, MANIFEST, DOSSIER, LEDGER, "E_GRAV_DISCOVERY")

# Falsifier 5: every claim source must be admitted by the research dossier.
bad_ledger = copy.deepcopy(LEDGER)
bad_ledger["claims"][0]["source_refs"] = ["https://example.invalid/not-authorized"]
must_fail(REQUEST, DISCOVERY, MANIFEST, DOSSIER, bad_ledger, "E_GRAV_PROVENANCE")

# Falsifier 6: a READY claim ledger may not contain provisional research claims.
bad_ledger = copy.deepcopy(LEDGER)
bad_ledger["claims"][0]["claim_status"] = "PROVISIONAL"
must_fail(REQUEST, DISCOVERY, MANIFEST, DOSSIER, bad_ledger, "E_GRAV_PROVENANCE")

# Falsifier 7: removing misconception evidence from the dossier invalidates the claim ledger provenance.
bad_dossier = copy.deepcopy(DOSSIER)
bad_dossier["authoritative_source_set"] = [
    source for source in bad_dossier["authoritative_source_set"]
    if "springer.com/chapter/10.1007/978-3-030-30188-0_4" not in source["source_ref"]
]
must_fail(REQUEST, DISCOVERY, MANIFEST, bad_dossier, LEDGER, "E_GRAV_PROVENANCE")

# Falsifier 8: RESEARCH closure may not bypass the dossier reference even when a dossier object exists in memory.
bad_manifest = copy.deepcopy(MANIFEST)
del bad_manifest["research_dossier_ref"]
must_fail(REQUEST, DISCOVERY, bad_manifest, DOSSIER, LEDGER, "E_GRAV_CLOSURE")

# Falsifier 9: the direct manifest target remains the field capability; adding force as a second direct gate defeats closure ownership.
bad_manifest = copy.deepcopy(MANIFEST)
bad_manifest["required_gate_ids"] = ["PHY-GRAV-FORCE", "PHY-GRAV-FIELD"]
must_fail(REQUEST, DISCOVERY, bad_manifest, DOSSIER, LEDGER, "E_GRAV_DISCOVERY")

print("Physics Gravity research v1: PASS (discovery + research provenance + gate + closure falsifiers)")
