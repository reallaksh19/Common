#!/usr/bin/env python3
from __future__ import annotations

import copy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))
from build_physics_engineering_gate_registry_v3 import build_registry  # noqa: E402
from validate_gravity_research_v1 import GravityResearchValidationError, load, validate  # noqa: E402

REQUEST = load("fixtures/engineering-workbench/grav-field-request.v1.json")
DISCOVERY = load("fixtures/engineering-workbench/grav-field-discovery.v1.json")
MANIFEST = load("fixtures/engineering-workbench/grav-field-manifest.v3.json")
DOSSIER = load("fixtures/engineering-workbench/grav-field-research-dossier.v1.json")
LEDGER = load("fixtures/engineering-workbench/grav-field-claim-ledger.v1.json")
REGISTRY = build_registry()


def must_fail(request, discovery, manifest, dossier, ledger, code, *, registry=None):
    try:
        validate(request, discovery, manifest, dossier, ledger, registry=registry)
    except GravityResearchValidationError as exc:
        assert exc.code == code, (code, exc.code, str(exc))
        return
    raise AssertionError(f"expected {code}")


def gate(registry, gate_id):
    return next(item for item in registry["gates"] if item["subtopic_id"] == gate_id)


# Positive: RESEARCH reaches ENGINEERING_READY only through reviewed discovery, claim provenance and canonical v3 closure.
result = validate(REQUEST, DISCOVERY, MANIFEST, DOSSIER, LEDGER, registry=REGISTRY)
assert result["status"] == "PASS"
assert result["registry_id"] == "PHYSICS-TECHNICAL-ENGINEERING-GATES-V3"
assert result["gravity_gates"] == ["PHY-GRAV-FIELD", "PHY-GRAV-FORCE"]
assert result["claim_count"] == 9
assert result["closure_gate_count"] == 10
assert result["closure_digest"].startswith("sha256:")

# 1. inverse-square field semantics cannot disappear.
bad = copy.deepcopy(REGISTRY)
gate(bad, "PHY-GRAV-FIELD")["required_invariants"].remove("INV-GRAV-FIELD-INVERSE-SQUARE")
must_fail(REQUEST, DISCOVERY, MANIFEST, DOSSIER, LEDGER, "E_GRAV_GATE_INVARIANT", registry=bad)

# 2. superposition relation cannot disappear.
bad = copy.deepcopy(REGISTRY)
g = gate(bad, "PHY-GRAV-FIELD")
g["relations"] = [r for r in g["relations"] if r["relation_id"] != "EQ-GRAV-FIELD-SUPERPOSITION"]
must_fail(REQUEST, DISCOVERY, MANIFEST, DOSSIER, LEDGER, "E_GRAV_GATE_INVARIANT", registry=bad)

# 3. field may not be silently EXTENDed into NLM; reviewed decision is CREATE_CHILD.
bad_discovery = copy.deepcopy(DISCOVERY)
next(op for op in bad_discovery["operations"] if op["gate_id"] == "PHY-GRAV-FIELD")["operation"] = "EXTEND"
must_fail(REQUEST, bad_discovery, MANIFEST, DOSSIER, LEDGER, "E_GRAV_DISCOVERY")

# 4. field ownership remains downstream of gravitational force.
bad_discovery = copy.deepcopy(DISCOVERY)
next(op for op in bad_discovery["operations"] if op["gate_id"] == "PHY-GRAV-FIELD")["parent_gate_id"] = "PHY-NLM-SECOND-LAW"
must_fail(REQUEST, bad_discovery, MANIFEST, DOSSIER, LEDGER, "E_GRAV_DISCOVERY")

# 5. every claim source must be admitted by the research dossier.
bad_ledger = copy.deepcopy(LEDGER)
bad_ledger["claims"][0]["source_refs"] = ["https://example.invalid/not-authorized"]
must_fail(REQUEST, DISCOVERY, MANIFEST, DOSSIER, bad_ledger, "E_GRAV_PROVENANCE")

# 6. a READY claim ledger may not contain provisional research claims.
bad_ledger = copy.deepcopy(LEDGER)
bad_ledger["claims"][0]["claim_status"] = "PROVISIONAL"
must_fail(REQUEST, DISCOVERY, MANIFEST, DOSSIER, bad_ledger, "E_GRAV_PROVENANCE")

# 7. removing misconception evidence from dossier invalidates claim provenance.
bad_dossier = copy.deepcopy(DOSSIER)
bad_dossier["authoritative_source_set"] = [source for source in bad_dossier["authoritative_source_set"] if "springer.com/chapter/10.1007/978-3-030-30188-0_4" not in source["source_ref"]]
must_fail(REQUEST, DISCOVERY, MANIFEST, bad_dossier, LEDGER, "E_GRAV_PROVENANCE")

# 8. RESEARCH closure may not bypass the dossier reference.
bad_manifest = copy.deepcopy(MANIFEST)
del bad_manifest["research_dossier_ref"]
must_fail(REQUEST, DISCOVERY, bad_manifest, DOSSIER, LEDGER, "E_GRAV_CLOSURE")

# 9. direct target remains field only; force must be derived as prerequisite.
bad_manifest = copy.deepcopy(MANIFEST)
bad_manifest["required_gate_ids"] = ["PHY-GRAV-FORCE", "PHY-GRAV-FIELD"]
must_fail(REQUEST, DISCOVERY, bad_manifest, DOSSIER, LEDGER, "E_GRAV_DISCOVERY")

# 10. canonical v3 Gravity may not fall back to the legacy extension mechanism.
bad_manifest = copy.deepcopy(MANIFEST)
bad_manifest["gate_extension_refs"] = ["policy/physics-technical-engineering-gates.gravity.v1.json"]
must_fail(REQUEST, DISCOVERY, bad_manifest, DOSSIER, LEDGER, "E_GRAV_DISCOVERY")

# 11. field force-per-mass authority must remain claim-ledger backed.
bad = copy.deepcopy(REGISTRY)
gate(bad, "PHY-GRAV-FIELD")["authority_basis"][0]["source_ref"] = "STANDARD_PHYSICS:UNBOUND"
must_fail(REQUEST, DISCOVERY, MANIFEST, DOSSIER, LEDGER, "E_GRAV_PROVENANCE", registry=bad)

# 12. exact 10-gate closure cannot be padded by adding an unrelated direct gate.
bad_manifest = copy.deepcopy(MANIFEST)
bad_manifest["required_gate_ids"] = ["PHY-GRAV-FIELD", "PHY-NLM-FRICTION"]
must_fail(REQUEST, DISCOVERY, bad_manifest, DOSSIER, LEDGER, "E_GRAV_DISCOVERY")

print("Physics Gravity research v3: PASS (reviewed discovery + research provenance + canonical registry + exact closure falsifiers)")
