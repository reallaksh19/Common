#!/usr/bin/env python3
import copy
import json
import sys
from pathlib import Path

D = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(D / "engine"))

from build_chemistry_representations import primitive_supports_capability, validate_registry  # noqa: E402


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


registry = load(D / "registry" / "chemistry-teaching-primitive-registry.json")
profile = load(D / "registry" / "chemistry-page-intent-profile.json")
extension = load(D / "registry" / "chemistry-electron-transfer-primitive-extension.v1.json")

assert extension["subject"] == "CHEMISTRY"
assert extension["extends_primitive_registry"] == registry["registry_id"]
assert extension["extends_page_intent_profile"] == profile["profile_id"]
assert extension["renderer_selection_forbidden"] is True
assert set(extension["conditional_primitives"]) == {"ELECTRON_TRANSFER_EVIDENCE"}
primitive = extension["primitives"][0]
assert primitive["primitive_id"] == "ELECTRON_TRANSFER_LEDGER"
assert primitive["topic_scope_refs"] == []
assert primitive["decorative"] is False
required_constraints = {
    "STATE_VALUES_EXPLICIT",
    "ELECTRON_COUNT_EXPLICIT",
    "LOSS_GAIN_DIRECTION_FROM_STATE_CHANGE",
    "ELECTRON_EXCHANGE_BALANCED",
    "SPECIES_IDENTITY_STABLE",
}
assert required_constraints <= set(primitive["renderer_constraints"])
for capability in primitive["capability_refs"]:
    assert primitive_supports_capability(primitive, capability)

combined = copy.deepcopy(registry)
existing = {row["primitive_id"] for row in combined["primitives"]}
assert primitive["primitive_id"] not in existing
combined["primitives"].extend(copy.deepcopy(extension["primitives"]))
by_id = validate_registry(combined)
assert by_id["ELECTRON_TRANSFER_LEDGER"]["translation_obligation"] == "SYMBOLIC_TO_LEDGER"
assert extension["conditional_primitives"]["ELECTRON_TRANSFER_EVIDENCE"] in by_id

# Falsifier: the authority file itself must keep the balance invariant explicit.
bad = copy.deepcopy(extension)
bad["primitives"][0]["renderer_constraints"].remove("ELECTRON_EXCHANGE_BALANCED")
assert not required_constraints <= set(bad["primitives"][0]["renderer_constraints"])

print("CHEMISTRY C-H electron-transfer authority extension = PASS")
print("Topic scope is empty; renderer selection remains forbidden.")
