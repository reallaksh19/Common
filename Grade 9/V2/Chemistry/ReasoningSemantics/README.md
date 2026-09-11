# Chemistry V2 — C-D reasoning semantics

This directory implements **C-D / #266**. It sits after C-C scope reconciliation and before learner diagnosis, PCK promotion, hint writing, solution writing, or page composition.

```text
C-C source obligations + question/capability bindings
        ↓
ChemistryProblemFamilyDefinition
        ↓
ChemistryReasoningRoute
        ↓
ConditionValidityBinding + VerificationRoute
        ↓
ChemistryDemandVector
        ↓
versioned guide-demand badge
```

## Hard separations

`ChemistryReasoningRoute` is not a hint ladder and is not a worked-solution summary. It records the semantic chemistry path independent of learner support. H1/H2/H3 belongs to C-I. Full solution prose also belongs downstream.

A source-owned difficulty code is preserved separately. The learner-facing demand badge is derived only from the multidimensional demand vector under a versioned editor policy.

## Chemistry invariants

- conditions/exceptions are route dependencies when decisive;
- macro / particulate / symbolic translation remains explicit;
- conservation checks name what is conserved;
- experimental observation and chemical claim are separate roles;
- structure/site dependencies cannot be flattened;
- reagent familiarity cannot replace equation/source evidence;
- verification is mandatory for every family;
- out-of-scope and unresolved records may be modelled, but do not become learner-authorized content.

## Pilot coverage

The registry contains 12 families spanning formula/charge parsing, representation translation, conservation, process classification, rule/exception logic, condition validity, evidence-to-claim, practical method selection, species-role assignment, structure/site reasoning, oxidation-state tracking, and chemical verification.

CI validates the contracts, runs all 12 required C-D falsifiers, generates semantics twice, checks byte-identical JSON, and validates every generated route/condition/verification/demand object.
