# Mathematics V2 — Engineering Gate → Blueprint Authority Boundary

This document is normative for the Mathematics Engineering Gate / MathBlueprint boundary.

It exists to prevent Blueprint from becoming topic-specific, example-specific, or dependent on an agent's remembered mathematics. Engineering Gate content is upstream technical authority; Blueprint consumes that authority through explicit, digest-bound identities and deterministic closure.

## 1. Authority direction

```text
ASSESSMENT / DECLARED-SCOPE AUTHORITY
        |
        | exact, versioned capability identity bridge only when vocabularies differ
        v
DIRECT ENGINEERING GATE IDS
        ^
        |
MATHEMATICS TECHNICAL ENGINEERING GATE REGISTRY
        |
        | Engineering schema + validator
        v
VALIDATED ENGINEERING GATE GRAPH
        |
        | exact runtime Engineering request
        v
TRANSITIVE ENGINEERING CLOSURE
        |
        | every gate READY and in authorized closure
        v
ENGINEERING AUTHORIZATION BINDING
        |
        | explicit Canonical Domain admission + digest-bound custody
        v
CANONICAL DOMAIN REGISTRY
        |
        | same Engineering custody stamped by every producer
        v
CORE1A / CORE1B / CORE2A / CORE2B
        |
        | cross-Core custody equality + current-admission revalidation
        v
CDAU -> SDU / LAU -> TTU -> PRODUCT -> PUBLICATION
```

Engineering Gate is therefore an upstream technical-authority boundary. MathBlueprint is not allowed to recreate a second mathematics gate system downstream.

## 2. Ownership

### Engineering Gate owns

- the canonical gate inventory;
- gate identifiers;
- curriculum/source references;
- prerequisite edges;
- linked bucket identifiers;
- technical concepts, equations, representations and conditions recorded by a gate;
- technical readiness;
- the Engineering schema;
- Engineering registry validation and falsification.

The current Engineering authority imported from PR #382 contains 44 Grade 9–11 gates. The architecture does not depend on the number 44: adding, removing or changing gates changes registry data, not Blueprint routing code.

### AssessmentScope authority owns

- canonical assessment capability identifiers;
- declared-topic identity;
- capability prerequisite identity;
- source-question-to-capability binding;
- assessment problem-family identity boundaries.

AssessmentScope does not become Engineering authority merely because an assessment capability has a similar title to an Engineering gate.

### MathBlueprint Workbench owns

- accepting a bounded runtime Engineering request;
- resolving that request to exact Engineering Gate IDs;
- computing transitive prerequisite closure;
- refusing a closure containing a non-ready/held gate;
- emitting authorization manifest/receipt/binding;
- preserving registry and validator-contract custody by digest;
- proving that downstream consumers use a currently valid closure.

MathBlueprint Workbench does **not** own topic mathematics, a parallel invariant list, or a compiled-in gate allowlist.

## 3. Legal identity paths

Engineering scope must arrive at the Workbench as exact Engineering Gate IDs or exact Engineering-owned bucket IDs.

### A. Exact Engineering Gate identity

```text
scope_kind = ENGINEERING_GATE
scope_refs = [exact gate id ...]
```

Each supplied ID must exist exactly in the current Engineering registry.

### B. Exact Engineering registry bucket linkage

```text
scope_kind = BUCKET
scope_refs = [exact linked bucket id ...]
```

A bucket resolves only through `subtopic_gate.linked_buckets` in the current Engineering registry.

### C. Exact cross-authority custody bridge

AssessmentScope and Engineering intentionally use different canonical vocabularies. Where a downstream run begins from AssessmentScope capability IDs, a versioned repository authority bridge may translate those **exact IDs** to direct Engineering Gate IDs before constructing the Workbench request.

Such a bridge is legal only when all of the following are true:

```text
exact AssessmentScope capability id
+ exact AssessmentScope authority id/digest
+ exact Engineering registry id/digest
+ explicit Engineering gate id(s)
+ explicit binding role
+ explicit uncovered/gap state when no gate exists
```

The current mixed-Grade-9 bridge is:

`policies/math-assessment-engineering-crosswalk.mixed-grade9.v1.json`

and is validated by:

`engine/validate_assessment_engineering_crosswalk.py`.

This bridge is **not** an Engineering resolver and is not allowed to match titles, prose or embeddings. It is custody data between two independently canonical identifier systems. Runtime code joins exact IDs only.

`FOUNDATIONAL_SUPPORT` means the Engineering gate authorizes the mathematical support used inside that bounded corpus; it does not claim semantic equivalence between the support capability and the entire gate.

## 4. Explicitly forbidden resolution

Blueprint and the custody bridge must never establish Engineering authority through:

```text
topic title similarity
substring matching
fuzzy matching
LLM semantic matching
remembered aliases
unversioned hand-written mappings in runtime code
per-topic if/else branches
sample/golden-case identity used as general authority
previous conversation memory
agent prior knowledge
```

A repository-authored crosswalk is not permission to guess. Every row is an explicit reviewed identity assertion bound to both current authorities. If an exact mapping is absent, the state is a named Engineering gap, not an inferred nearest gate.

For direct Workbench resolution the unmapped state remains:

```text
MATH_ENG_SCOPE_UNMAPPED
```

For the AssessmentScope bridge the blocked state is:

```text
MATH_ENG_CROSSWALK_REQUIRED_CAPABILITY_GAP
```

## 5. Closure rule

For direct gates `D`, Blueprint computes the complete prerequisite closure from the current Engineering graph:

```text
CLOSURE(D) = D union all transitive prerequisite_ids reachable from D
```

A relay Engineering request may contain at most three direct scope refs. That is a relay/scope bound only. The transitive Engineering closure has no three-gate cap.

When a product needs more than three direct gates, admission is partitioned into multiple bounded authorizations. Each Canonical Domain subtopic records exactly which direct gate(s) and which authorization(s) admit it.

Unknown prerequisite IDs fail closed. Dependency cycles fail closed.

A transitive prerequisite is not automatically permission to use that prerequisite gate as the direct semantic admission target of another domain subtopic.

## 6. Readiness rule

Blueprint first requires the Engineering registry to pass the Engineering-owned validator.

After that validation, each gate in the closure is admissible only when its authoritative Engineering state permits it. Blueprint does not re-derive mathematics with a second topic-specific table.

```text
ENGINEERING validator PASS
AND gate.technical_readiness == ENGINEERING_GATE_READY
AND gate.maturity == ENGINEERING
AND source scope is not HELD
=> blueprint_admissible = true
```

Otherwise technical authorization is blocked.

A downstream owner decision cannot rewrite Engineering truth, source custody, provenance or technical readiness.

## 7. Runtime custody

Every Engineering authorization binds at least:

```text
registry_digest
validator_contract_digest
scope_refs
direct_gate_ids
transitive_gate_ids
closure status
```

The validator-contract digest covers the Engineering schema and Engineering validator implementation. Therefore a change in either the registry or validator contract makes an old downstream binding stale.

Bindings are runtime artifacts. The repository must not use a persisted topic-specific binding as architectural authority for other topics.

## 8. Canonical Domain admission

A Canonical Domain Registry may be structurally valid and still lack current Engineering authorization.

Admission therefore requires both:

```text
DOMAIN REGISTRY VALID
AND
CURRENT ENGINEERING AUTHORIZATION(S) VALID
```

Every admitted domain subtopic must map explicitly to direct Engineering Gate IDs and to the authorization that owns each direct gate. The admission validator must verify:

- every domain subtopic is mapped;
- every mapped gate is a direct gate in the referenced authorization, not merely a transitive prerequisite;
- every authorization is current and targets `CANONICAL_DOMAIN_REGISTRY`;
- all direct authorization gates are actually used by the admission;
- Engineering registry and validator-contract digests are current;
- no authorization exceeds the relay direct-scope bound.

The admission validator may verify an explicit mapping; it may not invent that mapping from a domain title or remembered concept.

## 9. Producer custody invariant

Canonical Domain binding alone is insufficient for a release-ready producer receipt.

Every real Core1A/Core1B/Core2A/Core2B producer must stamp normalized Engineering custody containing the current domain-admission and Engineering authority digests.

```text
REGISTRY BOUND
AND PRODUCER GOVERNANCE COMPLETE
AND ENGINEERING CUSTODY BOUND
=> READY_FOR_CROSS_CORE_AUDIT
```

Otherwise the producer remains:

```text
UNBOUND_PRE_RELEASE
```

The cross-Core assembler requires all four stages to carry the same Engineering custody. Missing, unbound or different custody blocks assembly.

## 10. Final release revalidation

The final release gate must not trust a producer's stored custody merely because it has a valid shape.

Release therefore requires the current Engineering admission artifact and re-runs Engineering-domain validation from current repository authority. It then compares the freshly rebuilt custody against every producer receipt.

```text
CURRENT ADMISSION REVALIDATES
AND RECEIPT CUSTODY == CURRENT CUSTODY FOR ALL FOUR STAGES
AND CROSS-CORE GOVERNANCE PASS
AND SOURCE / ANSWER CUSTODY PASS
=> RELEASE PASS
```

A caller may not bypass current Engineering validation by supplying a pre-baked custody object.

## 11. Known mixed-Grade-9 coverage state

The current mixed Grade 9 cold-start corpus contains 30 required capabilities. The exact crosswalk currently reports:

```text
29 COVERED
1 ENGINEERING_GAP
```

The explicit gap is:

```text
MATH-EUCLID-CLASSIFY-AXIOM-POSTULATE
  -> MATH_ENG_GAP_EUCLID_FOUNDATIONS
```

No current direct Engineering gate owns axiom-versus-postulate classification. Mapping it to `MATH-GEO-LINES-ANGLES` or triangle axioms would overstate current Engineering authority.

Therefore the full mixed corpus is deliberately reported as:

```text
FULL_MIXED_CORPUS_NOT_ENGINEERING_RELEASE_READY
```

This is a valid governance finding, not a reason to weaken the boundary.

The actual-producer release golden separately uses the exact Engineering-covered projection declared in `golden/bound_producer_release/EXPECTED.json`:

```text
source question: Q2
capabilities:
  MATH-ORDERED-PAIR-SEMANTICS
  MATH-COORDINATE-DISTANCE
engineering gate:
  MATH-GEO-COORDINATES
```

The projection proves the complete producer/release machinery while retaining the full-corpus gap audit as a separate artifact. Adding a future Euclid-foundations Engineering gate must change the full-scope audit visibly; it must not silently widen the golden.

## 12. Global-change invariant

A valid Engineering registry expansion must not require new Blueprint topic logic.

The required behaviour is:

```text
Engineering registry N gates
        ↓
Blueprint enumerates current registry
        ↓
N runtime gate proofs
```

This is enforced by the registry-wide Workbench proof and its tests. The proof obtains its gate set from `subtopic_gates` at runtime; it does not contain a compiled-in gate list.

The PR #382 expansion from 10 to 44 gates is the current falsifier for this invariant: the same Blueprint Workbench code runs unchanged against the larger registry.

A new cross-authority mapping may require a crosswalk data update because AssessmentScope and Engineering are separate authority systems; it must not require a new resolver branch.

## 13. CI release invariant

CI must prove from current repository state:

```text
Engineering registry validator PASS
Engineering mutation falsifiers PASS
registry-driven Blueprint resolver/closure tests PASS
runtime custody binding tests PASS
generic engineered-domain admission tests PASS
AssessmentScope -> Engineering crosswalk validation PASS
full mixed-scope gap audit is explicit and stable
actual Core1A producer Engineering-bound
actual Core1B producer Engineering-bound
actual Core2A producer Engineering-bound
actual Core2B producer Engineering-bound
all four producer custody values equal
current Engineering admission revalidated at release
cross-Core release PASS
frozen source custody PASS
canonical answer custody PASS
learner publication regeneration PASS
```

A topic-specific CI step such as "compile quadratic closure" or "validate Theory-of-Equations admission" is not the governing architectural proof.

## 14. Separation from pedagogy

Engineering authorization means the required technical mathematics is permitted to enter the downstream design system. It does not itself authorize publication and it does not collapse CDAU/SDU/LAU/TTU responsibilities.

```text
ENGINEERING AUTHORIZATION != PUBLICATION AUTHORIZATION
```

Core1A/Core1B depth remains SDU-controlled by intrinsic difficulty. Core2A/Core2B adaptation remains LAU-controlled by learner evidence or explicit owner waiver. TTUs remain responsible for technical teaching/reconstruction completeness.

## 15. Non-regression rule

A future change is architecturally invalid if it introduces any of the following into MathBlueprint:

```text
a Blueprint-owned second Engineering truth registry
a Blueprint-owned compiled gate inventory
a title/fuzzy/memory resolver
an unversioned mapping embedded in runtime code
a persisted example binding treated as universal authority
a special runtime branch for one mathematical topic
a release path that trusts stale producer custody without current Engineering revalidation
```

The invariant is:

> **Engineering defines the technical gate graph. AssessmentScope and Engineering may be joined only through explicit, versioned exact-identity custody data. Blueprint consumes resulting Engineering IDs by deterministic closure and preserves that authority through every producer and release boundary. Examples may test the system; they may never define the system.**
