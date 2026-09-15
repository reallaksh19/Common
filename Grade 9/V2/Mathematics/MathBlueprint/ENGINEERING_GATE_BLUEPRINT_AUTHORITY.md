# Mathematics V2 — Engineering Gate → Blueprint Authority Boundary

This document is normative for the Mathematics Engineering Gate / MathBlueprint boundary.

Its purpose is to prevent Blueprint from becoming topic-specific, example-specific, or dependent on remembered mathematics. Engineering is upstream technical authority. Blueprint may consume that authority only through exact, digest-bound identities and deterministic closure.

## 1. Canonical authority direction

```text
ASSESSMENT / DECLARED-SCOPE AUTHORITY
        |
        | exact versioned capability custody bridge when vocabularies differ
        v
DIRECT ENGINEERING GATE IDS
        ^
        |
CANONICAL MATHEMATICS ENGINEERING GRAPH
  generated v1 base registry
        +
  exact digest-bound Engineering extensions
        |
        | Engineering schema + validator
        v
VALIDATED ENGINEERING GATE GRAPH
        |
        | exact runtime request; <=3 direct scope refs per authorization bundle
        v
TRANSITIVE ENGINEERING CLOSURE
        |
        | every gate READY and inside authorized closure
        v
ENGINEERING AUTHORIZATION BINDING(S)
        |
        | explicit Canonical Domain subtopic -> exact gate binding
        v
CANONICAL DOMAIN ADMISSION
        |
        | normalized Engineering custody
        v
Core1A / Core1B / Core2A / Core2B
        |
        | custody equality + current-admission revalidation
        v
CDAU -> SDU / LAU -> TTU -> PRODUCT -> PUBLICATION
```

Execution order may vary. Authority order may not.

## 2. Canonical Engineering graph

The current canonical graph contains **45 Grade 9–11 Engineering gates**.

The large generated artifact remains:

`policies/mathematics-technical-engineering-gates.v1.json`

The Euclidean-foundations authority is added through the exact extension:

`policies/mathematics-technical-engineering-gates.v1.euclid-extension.json`

The canonical loader is:

`engine/engineering_registry_composition.py`

The extension must bind to the exact base registry Git blob, the expected base gate count, and the expected composed gate count. Duplicate gate identities fail closed. The composed object retains registry identity `REG-MATH-TECH-GATE-V1`; however, its canonical digest changes when an authorized extension changes, so old downstream custody becomes stale automatically.

This is composition of one Engineering authority graph, not a second Blueprint-owned registry.

## 3. Euclid Foundations gate

The 45th gate is:

`MATH-GEO-EUCLID-FOUNDATIONS`

It closes the previously explicit upstream gap for:

`MATH-EUCLID-CLASSIFY-AXIOM-POSTULATE`

The gate is a full Engineering object, not a compatibility alias. It contains, among other required structures:

- `CON-MATH-EUCLID-AXIOM-POSTULATE-DISTINCTION`;
- `CON-MATH-EUCLID-ASSUMPTION-VS-THEOREM`;
- `CON-MATH-EUCLID-SCOPE-OF-ASSUMPTION`;
- `EQ-MATH-EUCLID-CLASSIFICATION`;
- `REP-MATH-EUCLID-CLASSIFICATION-TABLE`;
- `REP-MATH-EUCLID-LOGICAL-STATUS-FLOW`;
- `MISC-MATH-EUCLID-AXIOM-POSTULATE-PROOF`;
- `PF-MATH-EUCLID-AXIOM-POSTULATE-CLASSIFICATION`;
- explicit validity conditions, reasoning sequence, verification obligations, transformations, difficulty profile, release checklist, and falsification cases.

The validator has topic-specific Engineering invariants for this gate. Removing its classification concept, formal relation, required representation, or misconception repair must fail validation.

## 4. Exact AssessmentScope → Engineering custody bridge

AssessmentScope and Engineering intentionally use different canonical identity systems. That vocabulary boundary is crossed only through an explicit, versioned exact-ID bridge.

Historical v1 authority remains immutable:

`policies/math-assessment-engineering-crosswalk.mixed-grade9.v1.json`

It records the prior 29-covered / 1-gap state.

The current v2 migration is:

`policies/math-assessment-engineering-crosswalk.mixed-grade9.v2.patch.json`

The patch binds to:

- the exact v1 crosswalk Git blob;
- the v1 crosswalk identity;
- the exact historical Engineering registry digest;
- the exact Euclid extension reference;
- the exact Euclid extension Git blob.

It overrides only `MATH-EUCLID-CLASSIFY-AXIOM-POSTULATE`, binding it directly to `MATH-GEO-EUCLID-FOUNDATIONS`.

The canonical current result is:

```text
30 required mixed Grade-9 capabilities
30 COVERED
0 ENGINEERING_GAP
```

No title matching, substring matching, semantic matching, LLM matching, remembered aliases, conversation memory, or per-topic runtime fallback may create Engineering authority.

## 5. Permitted Engineering resolution

Blueprint Engineering requests may resolve only by:

1. exact Engineering Gate identity; or
2. exact `linked_buckets` membership in the current Engineering registry.

The AssessmentScope bridge is a separate explicit custody layer for translating canonical capability IDs to exact Engineering gate IDs. It is not a fuzzy resolver.

Unknown scope is:

`MATH_ENG_SCOPE_UNMAPPED`

Unknown capability-to-gate custody is a crosswalk failure. Neither state is permission to infer.

## 6. Closure and bounded authorization

For direct gate set `D`, Blueprint computes:

```text
CLOSURE(D) = D union every transitive prerequisite reachable from D
```

Each Engineering request/authorization bundle may contain at most three direct scope refs. This is a relay bound only; the transitive closure has no three-gate cap.

A larger product may therefore require multiple bounded authorization bundles. Canonical Domain admission must reference each bundle explicitly, and every admitted subtopic must bind to exact gates inside one of the authorized closures.

Unknown prerequisites and dependency cycles fail closed.

## 7. Readiness and custody

Engineering authorization requires current Engineering validation plus admissible gate state:

```text
ENGINEERING validator PASS
AND gate.technical_readiness == ENGINEERING_GATE_READY
AND source scope is not HELD
=> Blueprint technical admission may proceed
```

Every Engineering binding carries at least:

```text
registry_digest
validator_contract_digest
scope_refs
direct_gate_ids
transitive_gate_ids
closure_receipt_digest
downstream_consumer
```

The validator-contract digest includes the Engineering schema, Engineering validator, canonical registry composer, and canonical extension sources. Therefore changing any of those inputs invalidates old custody.

## 8. Producer invariant

Registry binding alone is insufficient for a producer to claim release readiness.

```text
REGISTRY BOUND
+ PRODUCER GOVERNANCE COMPLETE
+ ENGINEERING CUSTODY BOUND
=> READY_FOR_CROSS_CORE_AUDIT
```

Core1A, Core1B, Core2A and Core2B must all carry normalized Engineering custody. Cross-Core assembly rejects custody disagreement. Final release reconstructs current Engineering admission from current repository authority and compares it with producer receipts; a stale or pre-baked custody object cannot authorize release.

Engineering authorization does not replace SDU, LAU, TTU, source custody, answer custody, similarity governance, or publication governance.

```text
ENGINEERING AUTHORIZATION != PUBLICATION AUTHORIZATION
```

## 9. Full mixed-corpus release proof

`golden/bound_producer_release/EXPECTED.json` now defines `MATH-BOUND-PRODUCER-RELEASE-v3`.

The deterministic projection contract is identity-preserving and equals the complete current mixed Grade-9 cold-start scope:

```text
source questions: Q1 ... Q14
required capabilities: 30 / 30
Engineering gaps: 0
```

The run must:

- synthesize the complete mixed Core1 / StudyModel / Core2 scope;
- resolve every required capability through the exact v2 bridge;
- build one or more bounded Engineering authorization bundles;
- admit the same-run Canonical Domain Registry;
- execute the actual Core1A, Core1B, Core2A and Core2B CLIs;
- stamp matching Engineering custody into every stage receipt;
- cover all six cross-Core stage pairs;
- revalidate current Engineering admission at final release;
- preserve frozen source-question hashes;
- preserve canonical answer-contract custody;
- regenerate the governed learner publication.

Any future capability that is not Engineering-covered must fail before authoring. The golden may not silently narrow itself back to a covered subset.

## 10. Falsification requirements

The authority boundary is valid only while CI proves all of the following:

```text
45-gate canonical Engineering graph validates
Engineering mutation falsifiers pass
Euclid-specific invariant falsifiers pass
registry-wide exact gate proof covers every current gate
runtime custody binding falsifiers pass
Canonical Domain admission falsifiers pass
stale extension base-blob custody fails
wrong extension base gate count fails
duplicate extension gate identity fails
stale v2 crosswalk base custody fails
stale v2 crosswalk extension custody fails
30/30 mixed capability bridge validates
full 14-question four-producer Engineering-bound release passes
all producer Engineering custody values agree
frozen source custody passes
canonical answer custody passes
learner publication regeneration passes
```

## 11. Non-regression rule

A future change is architecturally invalid if it introduces any of the following:

```text
Blueprint-owned parallel mathematics truth
a hard-coded runtime gate inventory
a title/fuzzy/semantic/memory resolver
an undeclared capability-to-gate inference
a persisted example binding treated as universal authority
a topic-specific release bypass
an owner override that rewrites Engineering truth or provenance
```

The invariant is:

> **Engineering defines the technical gate graph. Explicit custody bridges connect other canonical vocabularies to that graph. Blueprint consumes the resulting exact identities and deterministic closures; examples test the system but never define it.**
