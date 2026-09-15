# Mathematics V2 — Engineering Gate → Blueprint Authority Boundary

This document is normative for the Mathematics Engineering Gate / MathBlueprint boundary.

It exists to prevent a Blueprint implementation from becoming topic-specific, example-specific, or dependent on an agent's remembered mathematics. Engineering Gate content is upstream authority; Blueprint resolves and consumes that authority mechanically.

## 1. Authority direction

```text
MATHEMATICS TECHNICAL ENGINEERING GATE REGISTRY
        |
        | validated by Engineering's own schema + validator
        v
VALIDATED ENGINEERING GATE GRAPH
        |
        | exact runtime scope resolution only
        v
DIRECT ENGINEERING GATE IDS
        |
        | transitive prerequisite traversal
        v
ENGINEERING CLOSURE
        |
        | every gate must be authoritatively READY and in scope
        v
ENGINEERING AUTHORIZATION RECEIPT
        |
        | digest-bound runtime custody
        v
MATHBLUEPRINT / CANONICAL DOMAIN REGISTRY
        |
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

### MathBlueprint Workbench owns

- accepting a bounded runtime scope request;
- resolving that request to exact Engineering Gate IDs;
- computing transitive prerequisite closure;
- refusing a closure containing a non-ready/held gate;
- emitting the authorization receipt/passport/binding;
- preserving registry and validator-contract custody by digest;
- proving that downstream consumers use a currently valid closure.

MathBlueprint Workbench does **not** own topic mathematics, a parallel invariant list, or a hand-authored gate allowlist.

## 3. Resolution rules

Only two resolution mechanisms are canonical.

### A. Exact Engineering Gate identity

```text
scope_kind = ENGINEERING_GATE
scope_refs = [exact gate id ...]
```

Each supplied ID must exist exactly in the current Engineering registry.

### B. Exact registry bucket linkage

```text
scope_kind = BUCKET
scope_refs = [exact bucket id ...]
```

A bucket resolves only through `subtopic_gate.linked_buckets` in the current Engineering registry.

No other resolver is legal.

## 4. Explicitly forbidden resolution

Blueprint must never resolve Engineering authority through:

```text
topic title similarity
substring matching
fuzzy matching
LLM semantic matching
remembered aliases
hard-coded topic maps
hand-written per-topic if/else branches
sample/golden-case identity
previous conversation memory
agent prior knowledge
```

If an exact mapping is absent, the state is:

```text
MATH_ENG_SCOPE_UNMAPPED
```

It is not permission to guess.

## 5. Closure rule

For direct gates `D`, Blueprint computes the complete prerequisite closure from the current Engineering graph:

```text
CLOSURE(D) = D union all transitive prerequisite_ids reachable from D
```

The relay request may contain at most three scope refs. That is a relay/scope bound only. The transitive Engineering closure has no three-gate cap.

Unknown prerequisite IDs fail closed. Dependency cycles fail closed.

## 6. Readiness rule

Blueprint first requires the Engineering registry to pass the Engineering-owned validator.

After that validation, each gate in the closure is admissible only when its authoritative Engineering state permits it. Blueprint does not re-derive mathematics with a second topic-specific table.

```text
ENGINEERING validator PASS
AND gate.technical_readiness == ENGINEERING_GATE_READY
AND source scope is not HELD
=> blueprint_admissible = true
```

Otherwise technical authorization is blocked.

A downstream owner decision cannot rewrite Engineering truth, source custody, provenance or technical readiness.

## 7. Runtime custody

Every authorization receipt binds at least:

```text
registry_digest
validator_contract_digest
scope_refs
direct_gate_ids
transitive_gate_ids
closure status
```

The validator-contract digest covers the Engineering schema and Engineering validator implementation. Therefore a change in either the registry or the validator contract makes an old downstream binding stale.

Bindings are runtime artifacts. The repository must not use a persisted topic-specific binding as the architectural authority for other topics.

## 8. Canonical Domain admission

A Canonical Domain Registry may be structurally valid and still lack current Engineering authorization.

Admission therefore requires both:

```text
DOMAIN REGISTRY VALID
AND
CURRENT ENGINEERING BINDING VALID
```

Any runtime `subtopic_id -> engineering_gate_id` mapping must use exact IDs, cover the domain subtopics being admitted, and point only to gates inside the current authorized closure.

The admission validator may verify an explicit mapping; it may not invent that mapping from a domain title or remembered concept.

## 9. Global-change invariant

A valid Engineering registry expansion must not require new Blueprint topic logic.

The required behaviour is:

```text
Engineering registry N gates
        ↓
Blueprint enumerates current registry
        ↓
N runtime gate proofs
```

This is enforced by the registry-wide Workbench proof and its tests. The proof obtains its gate set from `subtopic_gates` at runtime; it does not contain a compiled-in list.

The PR #382 expansion from 10 to 44 gates is the current falsifier for this invariant: the same Blueprint Workbench code must run unchanged against the larger registry.

## 10. CI release invariant

The dedicated Mathematics Engineering Workbench CI must prove, from current repository state:

```text
Engineering registry validator PASS
Engineering mutation falsifiers PASS
registry-driven Blueprint resolver/closure tests PASS
runtime custody binding tests PASS
generic engineered-domain admission tests PASS
registry-wide authorization proof PASS
```

A topic-specific CI step such as "compile quadratic closure" or "validate Theory-of-Equations admission" is not an architectural proof and must not be used as the governing gate.

## 11. Separation from pedagogy

Engineering authorization means the required technical mathematics is permitted to enter the downstream design system. It does not itself authorize publication and it does not collapse CDAU/SDU/LAU/TTU responsibilities.

```text
ENGINEERING AUTHORIZATION != PUBLICATION AUTHORIZATION
```

Core1A/Core1B depth remains SDU-controlled by intrinsic difficulty. Core2A/Core2B adaptation remains LAU-controlled by learner evidence or explicit owner waiver. TTUs remain responsible for technical teaching/reconstruction completeness.

## 12. Non-regression rule

A future change is architecturally invalid if it introduces any of the following into MathBlueprint:

```text
a Blueprint-owned per-topic Engineering invariant registry
a Blueprint-owned hard-coded gate inventory
a title/fuzzy/memory resolver
a persisted example binding treated as universal authority
a special branch for one mathematical topic
a requirement to edit Blueprint merely because Engineering adds a valid gate
```

The invariant is:

> **Engineering defines the technical gate graph. Blueprint consumes that graph by exact identifiers and deterministic closure logic. Examples may test the system; they may never define the system.**
