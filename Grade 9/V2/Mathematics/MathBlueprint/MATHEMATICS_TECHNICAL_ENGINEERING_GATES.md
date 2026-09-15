# Mathematics Technical Engineering Gate Registry (Grades 9–11)

**Canonical Registry ID:** `REG-MATH-TECH-GATE-V1`  
**Current Canonical Gate Count:** **45**  
**Maturity:** `ENGINEERING`  
**Boundary:** upstream technical/epistemic authority before Blueprint product design  
**Psychometric status:** no unvalidated psychometric claims are promoted into Engineering truth

This document describes the current technical contract. The executable registry, schema and validator remain authoritative.

## 1. Canonical source composition

The canonical Engineering graph is assembled deterministically from:

```text
policies/mathematics-technical-engineering-gates.v1.json
        44-gate generated base
                +
policies/mathematics-technical-engineering-gates.v1.euclid-extension.json
        exact digest-bound Euclid Foundations extension
                ↓
engine/engineering_registry_composition.py
                ↓
REG-MATH-TECH-GATE-V1
        45-gate canonical graph
```

The extension is accepted only when it binds to the exact base Git blob, expected base gate count and expected composed gate count. Duplicate gate IDs fail closed. The composed registry keeps the stable registry identity but receives a new canonical digest, which invalidates stale downstream Engineering custody.

## 2. Gate structure

Each Engineering gate is schema-closed and must carry the complete technical object required by `contracts/mathematics-technical-engineering-gate.schema.json`:

1. canonical `subtopic_id` and learner title;
2. chapter / curriculum provenance;
3. authority tier and `ENGINEERING` maturity;
4. technical readiness;
5. provenance and claim status;
6. canonical concept identities;
7. prerequisite gate identities;
8. linked curriculum buckets;
9. linked problem-family identities;
10. technical-core invariant statements;
11. mandatory equations / formal relations with symbol meaning and validity;
12. required representations;
13. model conditions and boundary cases;
14. expert reasoning sequence;
15. required representation transformations across Core roles;
16. misconception traps with counterexamples and repairs;
17. mandatory independent verifications;
18. problem-family recognition and first move;
19. ten-dimension intrinsic difficulty profile;
20. all-true release checklist for `ENGINEERING_GATE_READY`;
21. badges;
22. explicit falsification cases.

A fluent explanation without these structures is not an Engineering-ready gate.

## 3. Current 45th gate: Euclidean Foundations

The current expansion adds:

`MATH-GEO-EUCLID-FOUNDATIONS`

**Learner title:** Euclidean Foundations: Axioms, Postulates & Theorem Status  
**CBSE scope:** Grade 9, Introduction to Euclid's Geometry  
**JEE tier:** `NOT_IN_JEE`

The gate closes the exact AssessmentScope capability:

`MATH-EUCLID-CLASSIFY-AXIOM-POSTULATE`

It does not alias that capability to lines/angles or triangle proof. It owns the missing foundational classification object directly.

Mandatory Euclid structures include:

```text
CON-MATH-EUCLID-AXIOM-POSTULATE-DISTINCTION
CON-MATH-EUCLID-ASSUMPTION-VS-THEOREM
CON-MATH-EUCLID-SCOPE-OF-ASSUMPTION
EQ-MATH-EUCLID-CLASSIFICATION
REP-MATH-EUCLID-CLASSIFICATION-TABLE
REP-MATH-EUCLID-LOGICAL-STATUS-FLOW
MISC-MATH-EUCLID-AXIOM-POSTULATE-PROOF
PF-MATH-EUCLID-AXIOM-POSTULATE-CLASSIFICATION
```

The validity boundary is explicit: the Grade-9 curriculum convention first separates foundational assumptions from definitions/theorems, then distinguishes an axiom/common notion from a postulate by general-mathematics versus geometry-specific scope. The gate also records that broader mathematical traditions may use the terminology less sharply, so the classification frame must remain declared.

## 4. Representation vocabulary

The Engineering schema includes formal mathematical and pedagogical representations such as coordinate plots, proof layouts, sign/discriminant charts, probability trees, Argand plots and conic constructions.

For Euclid Foundations the schema now also admits:

`DEFINITION_CLASSIFICATION_TABLE`

This is used for both the explicit axiom/postulate/theorem comparison table and the independent logical-status decision flow. A one-step memorization list is not an adequate representation.

## 5. Graph and closure invariants

The validator requires:

- globally unique gate, concept, equation, representation and misconception IDs;
- every prerequisite gate to exist;
- no self-dependency;
- linked problem-family IDs to resolve inside the gate;
- every READY gate to have a complete release checklist;
- structural difficulty dimensions to remain in their permitted ranges;
- selected domain gates to preserve mandatory concepts/equations/representations/misconceptions.

Blueprint then computes transitive prerequisite closure over the validated graph. Blueprint does not maintain a duplicate topic graph.

## 6. Stable validation failures

The production validator emits stable codes including:

```text
MATH_GATE_SCHEMA_VIOLATION
MATH_GATE_DUPLICATE_ID
MATH_GATE_INVALID_SUBTOPIC_ID
MATH_GATE_MATURITY_OVERREACH
MATH_GATE_UNRESOLVED_PREREQUISITE
MATH_GATE_CROSS_REFERENCE_INTEGRITY_FAIL
MATH_GATE_MISSING_REQUIRED_CONCEPT
MATH_GATE_MISSING_MANDATORY_EQUATION
MATH_GATE_MISSING_MANDATORY_REPRESENTATION
MATH_GATE_MISSING_MISCONCEPTION_TRAP
MATH_GATE_INVALID_DIFFICULTY_PROFILE
MATH_GATE_RELEASE_CHECKLIST_INCOMPLETE
```

The composition layer additionally fails stale or conflicting extension custody before Engineering validation can proceed.

## 7. Mutation falsification battery

`engine/validate_mathematics_engineering_gates.py` executes **16 mutation falsifiers**. Existing falsifiers cover radicals, quadratics, coordinate geometry, polynomials, triangle congruence, probability, prerequisite closure, proof representation, problem-family cross-reference, global ID uniqueness and release-checklist readiness.

Four additional Euclid-specific mutations must fail:

1. remove `CON-MATH-EUCLID-AXIOM-POSTULATE-DISTINCTION`;
2. remove `EQ-MATH-EUCLID-CLASSIFICATION`;
3. remove `REP-MATH-EUCLID-CLASSIFICATION-TABLE` while retaining another schema-valid representation;
4. remove `MISC-MATH-EUCLID-AXIOM-POSTULATE-PROOF`.

This ensures Euclid Foundations is an engineered gate, not merely a 45th identifier.

## 8. Composition/custody falsifiers

`tests/test_engineering_registry_composition.py` separately verifies that:

- the canonical composition has 45 unique gates;
- an extension bound to a stale base Git blob fails;
- an extension declaring the wrong base gate count fails;
- an extension that duplicates an existing gate ID fails;
- a v2 AssessmentScope crosswalk patch bound to a stale Euclid-extension blob fails;
- a v2 crosswalk patch bound to a stale base-crosswalk blob fails.

These tests protect the authority chain around the registry rather than only the mathematical contents inside a gate.

## 9. AssessmentScope coverage

AssessmentScope and Engineering are separate canonical vocabularies. Their bridge is exact and versioned.

Historical v1:

`policies/math-assessment-engineering-crosswalk.mixed-grade9.v1.json`

Current v2 patch:

`policies/math-assessment-engineering-crosswalk.mixed-grade9.v2.patch.json`

Current mixed Grade-9 coverage is:

```text
required capabilities: 30
Engineering-covered:   30
Engineering gaps:       0
```

The old v1 29/30 state remains preserved as historical custody. V2 changes only the Euclid-classification row and binds it to `MATH-GEO-EUCLID-FOUNDATIONS`.

## 10. Release proof

The registry is not considered operationally sufficient merely because all 45 gates validate. CI must also prove that downstream Blueprint consumers use current authority.

The full mixed-corpus golden now covers:

```text
Q1 ... Q14
30 required capabilities
45-gate current Engineering graph
one or more bounded Engineering authorization bundles
actual Core1A
actual Core1B
actual Core2A
actual Core2B
strict cross-Core release
frozen source custody
canonical answer custody
governed learner publication regeneration
```

A future Engineering expansion should change registry/extension data and custody, not add topic-name branches to Blueprint.

## 11. Canonical files

```text
contracts/mathematics-technical-engineering-gate.schema.json
policies/mathematics-technical-engineering-gates.v1.json
policies/mathematics-technical-engineering-gates.v1.euclid-extension.json
engine/engineering_registry_composition.py
engine/validate_mathematics_engineering_gates.py
engine/compile_mathematics_engineering_workbench.py
policies/math-assessment-engineering-crosswalk.mixed-grade9.v1.json
policies/math-assessment-engineering-crosswalk.mixed-grade9.v2.patch.json
engine/validate_assessment_engineering_crosswalk.py
tests/test_mathematics_engineering_gates.py
tests/test_engineering_registry_composition.py
tests/test_assessment_engineering_crosswalk.py
```

The architectural invariant is:

> **Mathematical technical authority is explicit, typed, falsifiable and digest-bound. Blueprint consumes exact Engineering identities and current custody; it never invents a missing gate by semantic resemblance.**
