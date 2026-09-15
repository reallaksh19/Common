# Mathematics V2 — Engineering Gate → Blueprint Authority Boundary

This document is normative for the Mathematics Engineering Gate / MathBlueprint boundary.

Its purpose is to prevent Blueprint from becoming topic-specific, example-specific, or dependent on remembered mathematics. Engineering is upstream technical authority. Blueprint may consume that authority only through exact, digest-bound identities, generic policy evaluation and deterministic closure.

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
  base registry
        +
  digest-bound extension catalog
        +
  governed Engineering extension data
        |
        | schema + generic validator
        | external mathematical invariant data
        | generic Engineering depth policy
        v
VALIDATED ENGINEERING GATE GRAPH
        |
        | exact runtime request; <=3 direct scope refs per authorization bundle
        v
TRANSITIVE ENGINEERING CLOSURE
        |
        | every gate admissible at requested Engineering depth
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

## 2. Non-negotiable ownership rule

```text
Engineering owns:
- mathematical gate identities;
- topic/subtopic-specific mathematical content;
- prerequisites;
- gate-specific invariant data;
- provenance;
- technical readiness data.

Blueprint owns:
- exact request resolution;
- generic depth evaluation;
- deterministic prerequisite closure;
- custody/binding;
- downstream orchestration.
```

Blueprint must not contain mathematical topic branches, topic-specific extension filenames, remembered aliases, title/fuzzy/semantic resolution, or locally invented capability mappings.

A new mathematical subtopic is an Engineering-data change. It is not a reason to add a new topic-specific Blueprint implementation.

## 3. Canonical Engineering graph

The base artifact is:

`policies/mathematics-technical-engineering-gates.v1.json`

Canonical additions are discovered only through:

`policies/mathematics-engineering-extension-catalog.v1.json`

The loader is:

`engine/engineering_registry_composition.py`

The extension catalog binds to the exact base Git blob and to the exact Git blob of each ordered extension. Each extension binds to the stable base registry identity, exact base blob, expected pre-extension gate count and expected composed gate count. Duplicate gate identities fail closed.

The current repository composes to **45 gates**. That is current evidence, not a hard-coded Blueprint gate inventory.

## 4. Mathematical invariants remain Engineering data

Gate-specific mandatory mathematical requirements live in:

`policies/mathematics-engineering-gate-invariants.v1.json`

The production validator knows only generic invariant categories:

```text
required_concept_ids
required_equation_ids
required_representation_ids
required_misconception_ids
required_prerequisite_ids
```

Current mathematical gate IDs may appear in that Engineering policy data. They must not appear as `if gate == <topic>` branches in Blueprint/validator orchestration code.

Changing invariant data changes `validator_contract_digest`, so stale downstream custody is rejected automatically.

## 5. Engineering depth is executable and generic

Every Engineering request specifies:

```text
FOUNDATION | STANDARD | RESEARCH
```

The structural depth rules live in:

`policies/mathematics-engineering-depth-policy.v1.json`

The policy contains no topic identities. It evaluates generic Engineering structure such as reasoning depth, model conditions, representations, misconceptions, transformations, verification/falsification coverage and provenance.

Therefore:

```text
same mathematical capability, greater rigor
    → same gate + stronger engineering_depth

new mathematical capability
    → new Engineering gate data

existing capability added to a product/exam scope
    → scope/crosswalk membership change only
```

A gate may legitimately pass `STANDARD` and be blocked at `RESEARCH`. Blueprint does not invent a research version of the topic.

## 6. Exact AssessmentScope → Engineering custody bridge

AssessmentScope and Engineering intentionally use different canonical identity systems. That vocabulary boundary is crossed only through an explicit, versioned exact-ID bridge.

Historical base authority:

`policies/math-assessment-engineering-crosswalk.mixed-grade9.v1.json`

Current patch:

`policies/math-assessment-engineering-crosswalk.mixed-grade9.v2.patch.json`

A patch may reference an Engineering extension only when the reference exists in the canonical extension catalog and its exact Git blob matches. Crosswalk composition does not know or infer the mathematical meaning of that extension.

Current mixed Grade-9 evidence is:

```text
30 required capabilities
30 COVERED
0 ENGINEERING_GAP
```

These counts are fixture/scope evidence rather than production constants.

No title matching, substring matching, semantic matching, LLM matching, remembered aliases, conversation memory, or per-topic runtime fallback may create Engineering authority.

## 7. Permitted Engineering resolution

Blueprint Engineering requests may resolve only by:

1. exact Engineering Gate identity; or
2. exact `linked_buckets` membership in the current Engineering registry.

The AssessmentScope bridge is a separate explicit custody layer for translating canonical capability IDs to exact Engineering gate IDs. It is not a fuzzy resolver.

Unknown scope is:

`MATH_ENG_SCOPE_UNMAPPED`

Unknown capability-to-gate custody is a crosswalk failure. Neither state is permission to infer.

## 8. Closure and bounded authorization

For direct gate set `D`, Blueprint computes:

```text
CLOSURE(D) = D union every transitive prerequisite reachable from D
```

Each Engineering request/authorization bundle may contain at most three direct scope refs. This is a relay/transport bound only; the transitive prerequisite closure has no three-gate cap.

A larger product may require multiple bounded authorization bundles. Canonical Domain admission references each bundle explicitly, and every admitted subtopic binds to exact gates inside an authorized closure.

Unknown prerequisites, self-dependencies and cycles fail upstream Engineering validation.

## 9. Readiness and custody

Engineering authorization requires current generic Engineering validation and current depth admission:

```text
schema PASS
+ global identity/cross-reference/prerequisite graph PASS
+ external mathematical invariant data PASS
+ declared READY state internally consistent
+ source scope not held
+ requested engineering_depth PASS
= Blueprint technical admission may proceed
```

A READY label cannot rescue missing required Engineering structure.

Every Engineering binding carries exact custody including:

```text
request_digest
manifest_digest
registry_digest
validator_contract_digest
scope_refs
direct_gate_ids
transitive_gate_ids
closure_receipt_digest
downstream_consumer
```

The validator-contract digest includes the Engineering schema, generic validator source, registry composer, extension catalog, all canonical extension sources, invariant profile and depth policy. Changes to those inputs invalidate old custody automatically.

## 10. Engineering visibility / Passport

Engineering must be visible without creating a second source of truth.

`compile_passport()` therefore derives a non-authoritative Engineering surface from the exact bound registry + closure receipt. The surface exposes, per gate:

- direct versus prerequisite-closure role;
- learner-facing title/chapter;
- requested Engineering depth;
- READY/BLOCKED state and generic failure codes;
- prerequisite IDs;
- provenance summary;
- structural counts for concepts, equations, representations, model conditions, reasoning steps, transformations, misconceptions, verifications, problem families and falsifiers;
- intrinsic difficulty profile; and
- release-checklist status.

Before rendering that view, Passport verifies that the supplied registry digest equals the registry digest in the closure receipt. A stale or different registry cannot be used merely to make Engineering look complete.

The Passport is a view of Engineering authority, never a replacement for it.

## 11. Producer invariant

Registry binding alone is insufficient for a producer to claim release readiness.

```text
REGISTRY BOUND
+ PRODUCER GOVERNANCE COMPLETE
+ ENGINEERING CUSTODY BOUND
=> READY_FOR_CROSS_CORE_AUDIT
```

Core1A, Core1B, Core2A and Core2B must carry normalized Engineering custody. Cross-Core assembly rejects custody disagreement. Final release reconstructs current Engineering admission from current repository authority and compares it with producer receipts; a stale or pre-baked custody object cannot authorize release.

Engineering authorization does not replace SDU, LAU, TTU, source custody, answer custody, similarity governance or publication governance.

```text
ENGINEERING AUTHORIZATION != PUBLICATION AUTHORIZATION
```

## 12. Research permission versus promotion obligation

Pedagogy web search is not mathematical authority and must not be artificially disabled merely because a bucket is intrinsically EASY.

```text
EASY    → research OPTIONAL
MEDIUM  → targeted research REQUIRED
HARD    → deep research REQUIRED
```

When optional research is used, its research brief and evidence references must still be fully bound. Partial custody fails. Production research still requires production-grade verified evidence, while TEST_ONLY evidence cannot authorize a production release.

This keeps discovery permissive while keeping promotion strict.

## 13. Full mixed-corpus release proof

`golden/bound_producer_release/EXPECTED.json` defines the current deterministic full mixed Grade-9 proof.

Current scope evidence is:

```text
source questions: Q1 ... Q14
required capabilities: 30 / 30
Engineering gaps: 0
```

The run must:

- synthesize the complete mixed Core1 / StudyModel / Core2 scope;
- resolve every required capability through the exact bridge;
- build one or more bounded Engineering authorization bundles;
- admit the same-run Canonical Domain Registry;
- execute the actual Core1A, Core1B, Core2A and Core2B CLIs;
- stamp matching Engineering custody into every stage receipt;
- cover all six cross-Core stage pairs;
- revalidate current Engineering admission at final release;
- preserve frozen source-question hashes;
- preserve canonical answer-contract custody;
- preserve the bound pedagogy research manifest ID, digest and release class; and
- regenerate the governed learner publication.

Any future capability that is not Engineering-covered must fail before authoring. The golden may not silently narrow itself back to a covered subset.

## 14. Falsification requirements

The authority boundary is valid only while CI proves the current generic properties, including:

```text
canonical Engineering graph validates
data-derived Engineering invariant mutation falsifiers pass
catalog/base/blob/count custody falsifiers pass
synthetic new gate composes and validates without production topic-code changes
registry-wide exact gate proof covers every current gate
generic STANDARD-vs-RESEARCH depth falsifier passes
runtime custody binding falsifiers pass
Canonical Domain admission falsifiers pass
exact AssessmentScope bridge validates
full four-producer Engineering-bound release passes
all producer Engineering custody values agree
frozen source custody passes
canonical answer custody passes
pedagogy research release class is explicitly bound
learner publication regeneration passes
```

The current mutation count and current gate count are CI evidence, not constants that production logic should assume.

## 15. Non-regression rule

A future change is architecturally invalid if it introduces any of the following:

```text
Blueprint-owned parallel mathematics truth
a hard-coded runtime gate inventory
a topic-specific validator branch
a topic-specific extension path in production Python
a title/fuzzy/semantic/memory resolver
an undeclared capability-to-gate inference
a persisted example binding treated as universal authority
a topic-specific release bypass
an owner override that rewrites Engineering truth or provenance
```

The invariant is:

> **Engineering defines mathematical identities and topic-specific technical truth as governed data. Explicit custody bridges connect other canonical vocabularies to that graph. Blueprint consumes exact identities, generic depth policy and deterministic closure; examples test the system but never define it.**
