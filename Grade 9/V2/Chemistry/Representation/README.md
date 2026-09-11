# Chemistry V2 C-H — Teaching Primitives and Representation Closure

C-H makes Chemistry representations first-class semantic objects rather than renderer-selected decoration.

The phase consumes the C-G Core1 plan and C-F LearnerStudyModel and emits source-bound `ChemistryRepresentationSpec` records. Every representation carries a capability binding, instructional job, attention target, learner action, translation obligation, chemical entities, condition/exception context, accessibility text, renderer constraints and an explicit notation contract reference.

## Authority boundary

Visual selection originates from the learner treatment, Core1 lesson semantics, problem-family/capability authority and the C-H page-intent profile. The renderer is not allowed to invent chemical entities, conditions, apparatus observations, structure sites, particle composition or notation meaning.

## Primitive registry

The registry covers the required C-H primitive family, including macro/particle/symbolic bridges, formula anatomy, charge/subscript and coefficient/subscript contrasts, conservation ledgers, reaction maps, species-role maps, condition gates, structure-site annotation, oxidation-state lanes, SELF/OTHER agent framing, split/converge topology, evidence→claim chains, apparatus flows, observation/inference tables, minimal contrasts and chemical check strips.

## Safety rules

- decorative visuals never satisfy an instructional representation requirement;
- particle views preserve source composition and avoid literal particle-size or undeclared bonding claims;
- structure-site identity is stable;
- required conditions/exceptions remain visible;
- apparatus representations cannot invent observations;
- minimal contrasts contain two cases differing on one decisive feature;
- formula/charge notation is source-bound and ambiguous flat ASCII is forbidden.

## Validation

`contracts/validate_contracts.py` validates the schema, primitive registry, page-intent profile and notation contract.

`tests/test_chemistry_representations.py` exercises all 11 issue #270 falsifiers and proves deterministic semantic replay.

This phase does not claim final PDF quality, visual-usability approval, Core2 hint/solution quality or mature-product release.
