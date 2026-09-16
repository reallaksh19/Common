"""Particle/accounting checks with explicit species and model boundaries."""

from __future__ import annotations


VALIDATORS = {"PARTICLE_ATOM_COUNT", "CONSERVATION_LEDGER", "REACTION_EXTENT_COUNTS"}


def _count(value, *, positive=False):
    if type(value) is not int or value < (1 if positive else 0):
        raise ValueError("INTEGER_PARTICLE_COUNT_REQUIRED")
    return value


def _species(case):
    species = case.get("species", {})
    if not species or not case.get("species_authority_ref"):
        raise ValueError("GOVERNED_SPECIES_COMPOSITION_REQUIRED")
    for name, atoms in species.items():
        if not name or not atoms:
            raise ValueError("SPECIES_COMPOSITION_EMPTY")
        for element, count in atoms.items():
            if not element:
                raise ValueError("ELEMENT_ID_REQUIRED")
            _count(count, positive=True)
    return species


def _atoms(species, amounts):
    result = {}
    for name, raw in amounts.items():
        if name not in species:
            raise ValueError("UNKNOWN_SPECIES")
        amount = _count(raw)
        for element, count in species[name].items():
            result[element] = result.get(element, 0) + count * amount
    return {k: v for k, v in sorted(result.items()) if v}


def recompute(case: dict):
    kind = case.get("validator_id")
    if kind not in VALIDATORS:
        raise ValueError(f"VALIDATOR_UNSUPPORTED:{kind}")
    species = _species(case)
    if kind == "PARTICLE_ATOM_COUNT":
        return _atoms(species, case["amounts"])
    left, right = case["reactant_coefficients"], case["product_coefficients"]
    if not left or not right:
        raise ValueError("REACTION_SIDES_REQUIRED")
    for value in list(left.values()) + list(right.values()):
        _count(value, positive=True)
    before, after = _atoms(species, left), _atoms(species, right)
    if kind == "CONSERVATION_LEDGER":
        return {"reactant_atoms": before, "product_atoms": after, "balanced": before == after}
    if before != after or case.get("model") != "COMPLETE_REACTION_INTEGER_PARTICLE_ACCOUNTING":
        raise ValueError("STOICHIOMETRIC_ACCOUNTING_MODEL_INVALID")
    amounts = case["available_reactants"]
    if set(amounts) != set(left):
        raise ValueError("REACTANT_INVENTORY_MISMATCH")
    extent = min(_count(amounts[x]) // left[x] for x in left)
    return {"products": {x: extent * right[x] for x in right},
            "leftover_reactants": {x: amounts[x] - extent * left[x] for x in left}}
