# Physics V2 Blueprint — evidence-adaptive orchestration

`Grade 9/V2/Physics/Blueprint/` is the **canonical orchestration root for Physics Blueprint work**. Role-specific sibling directories (`CoreAuthoring/`, `Core2Transfer/`, `Core1A/`, `Core2A/`) are subordinate execution kits; `policy/role-bindings.v1.json` freezes that mapping.

## Executable topology

```text
ORIGINAL GROUND TRUTH
        ↓
      CORE0
        ↓
CORE1 ↔ independent second pass ↔ CORE2
        ↓
       JOIN
        ↓
learner state × purpose
        ↓
CORE1A 1A0…1A11
        ↓
1A12 manuscript + T receipts
        ↓
      CORE2A
        ↓
PUBLICATION IR
lossless semantic audit
        ↓
renderer (composition only)
```

## Blueprint guarantees now implemented

- evidence-adaptive routing, never topic-name routing;
- independent second-role re-grounding;
- Core1 × Core2 Join with exact demand coverage and critical-conflict blocking;
- learner `20/50/80` prior resolved to capability state, with real learner evidence distinguished from teaching receipts;
- orthogonal purpose contracts;
- strict Core1A cognition-before-manuscript stage machine;
- Motion-in-a-Plane real topic pilot deriving `CORE2_FIRST` from `SA=2, SS=3, QE=4, QR=4, UA=1, CI=1`;
- taught-state-gated Core2A;
- Publication IR with a fail-closed lossless semantic boundary.

## Publication boundary

The renderer is **not** a reasoning role. Publication IR can consume only upstream artifacts whose release state is already `RELEASED`. Every required upstream semantic ref must be placed exactly once. The compiler rejects missing or duplicated required refs, unknown semantic refs, changed content digests, source-role drift and unauthorized representation substitution.

The resulting IR fixes:

```text
semantic_authority = UPSTREAM_ONLY
renderer_authority = COMPOSITION_ONLY
renderer_may_introduce_semantic_claims = false
renderer_may_substitute_representation = false
```

Optional semantic refs may be intentionally omitted; required semantics may not disappear through layout decisions.

## Current next boundary

The reasoning Blueprint and the semantic publication boundary are now machine-specified. The next tranche is **figure/page realization + actual-render QA**, consuming Publication IR without adding Physics reasoning. Human subject, pedagogy, assessment and visual review remain separate release gates.
