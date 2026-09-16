# STEM Subject Adapter Interface Candidate

> **Status: DESIGN / NON-NORMATIVE**
>
> This document describes the Stage-C4 subject-adapter interface candidate. It does not create subject authority, change Mathematics runtime behavior, authorize Chemistry runtime behavior, or permit production consumers to read `design/` as authority.

## 1. C4 purpose

C4 extracts a cross-subject interface from current Mathematics behavior so the future generic STEM kernel can ask subject-neutral questions without absorbing Mathematics-specific truth.

The extraction rule is:

```text
CURRENT MATHEMATICS BEHAVIOR
    ↓ repository-derived classification only
SUBJECT-NEUTRAL OPERATION
    ↓ exact reference back to current Mathematics components
DESIGN ADAPTER PROJECTION
```

It is deliberately **not**:

```text
new generic interface
    ↓
replace Mathematics authority
```

or:

```text
Chemistry design vocabulary
    ↓
Chemistry runtime authority
```

## 2. Authority boundary

The candidate is locked to:

```text
authority = NONE
semantic_change = NONE
runtime_migration_authorized = false
production_consumers_allowed = false
```

Mathematics technical truth remains owned by current Mathematics Engineering and governed domain data. Existing validators, compilers, registries and release gates remain unchanged.

The adapter candidate may classify how current behavior could satisfy a future interface. It may not make that interface executable.

## 3. Generic-kernel boundary

The proposed generic kernel owns cross-subject mechanics such as identity, scope membership, provenance, maturity, exact-reference custody, non-authoritative discovery, research promotion, learner calibration, learning-purpose control, prerequisite/transition composition, assessment custody, TTU lifecycle, publication lifecycle, versioning/invalidation and risk reporting.

It must not encode algebra, geometry, chemical identity, stoichiometry, reaction mechanisms, laboratory safety or any other subject truth.

The central prohibition is:

```text
if subject == MATHEMATICS and topic == ...
if subject == CHEMISTRY and topic == ...
```

Subject differences belong in governed adapter data and subject validators, not topic branches in the generic kernel.

## 4. Candidate interface operations

C4 defines eight core operations plus one conditional subject capability:

| Operation | Requirement | Meaning |
|---|---|---|
| `DISCOVER_CANDIDATES` | CORE | find candidates only; no authorization |
| `RESOLVE_EXACT_IDENTITY` | CORE | resolve explicit exact identity against current subject authority |
| `VALIDATE_SUBJECT_AUTHORITY` | CORE | apply subject-owned structural/maturity validation |
| `COMPUTE_PREREQUISITE_CLOSURE` | CORE | derive closure only from governed exact relations |
| `RETURN_CANONICAL_OBJECTS` | CORE | project canonical objects from already-authorized state |
| `VALIDATE_TRANSFORMATION` | CORE | validate transformations through subject rules rather than plausibility |
| `VALIDATE_REPRESENTATION` | CORE | validate meaning/bindings/forbidden implications of a representation |
| `VALIDATE_VERIFICATION_RULE` | CORE | validate subject verification methods from governed objects |
| `VALIDATE_SUBJECT_SAFETY` | CONDITIONAL | require explicit subject safety authority where the subject exposes safety-governed actions |

The interface operation names are subject-neutral. The Mathematics projection and future Chemistry adapter remain separate.

## 5. Mathematics behavior projection

The C4 Mathematics projection is a **reference-only mapping** over the existing C1 architecture catalog. It does not wrap, replace or intercept the runtime.

Current mappings are:

| Generic operation | Current Mathematics component |
|---|---|
| `DISCOVER_CANDIDATES` | `MATH-ARCH-ENGINEERING-DISCOVERY` |
| `RESOLVE_EXACT_IDENTITY` | `MATH-ARCH-ENGINEERING-WORKBENCH` |
| `VALIDATE_SUBJECT_AUTHORITY` | `MATH-ARCH-ENGINEERING-VALIDATION` |
| `COMPUTE_PREREQUISITE_CLOSURE` | `MATH-ARCH-ENGINEERING-WORKBENCH` |
| `RETURN_CANONICAL_OBJECTS` | `MATH-ARCH-DOMAIN-PROJECTION` |
| `VALIDATE_TRANSFORMATION` | `MATH-ARCH-ENGINEERING-VALIDATION` |
| `VALIDATE_REPRESENTATION` | `MATH-ARCH-DOMAIN-PROJECTION` |
| `VALIDATE_VERIFICATION_RULE` | `MATH-ARCH-DOMAIN-PROJECTION` |

Each binding is valid only when its component identity exists in the current C1 catalog and every evidence path used by the binding is already declared by the referenced component.

The Mathematics object vocabulary is not copied by hand as a new authority. C4 verifies that the projection equals the current `assetType` enum in `contracts/math-canonical-domain-registry.schema.json` exactly:

```text
CONCEPT
MODEL
EQUATION
DERIVATION
CAPABILITY
LEARNING_ATOM
REPRESENTATION
MISCONCEPTION
PROBLEM_FAMILY
SOURCE_QUESTION
CANONICAL_SOLUTION
EXAMPLE
VERIFICATION_RULE
```

Any future change to that canonical vocabulary stales the C4 equivalence receipt until C4 is deliberately reviewed and regenerated.

## 6. Chemistry stress target

Chemistry exists in C4 only to falsify a Mathematics-shaped generic interface.

C4 records candidate Chemistry object categories such as chemical entities, species, macroscopic observations, particle models, symbolic representations, reactions, reaction conditions, stoichiometric relations, mechanisms, thermodynamic/kinetic relations, nomenclature, experimental observations, measurement/uncertainty and hazard/safety constraints.

Those categories are **design vocabulary only**. C4 sets:

```text
chemistry.authority = NONE
chemistry.runtime_binding_present = false
chemistry.production_registry_ref = null
chemistry.production_validator_ref = null
```

A later Chemistry pilot must establish its own governed technical authority, schemas, validators, provenance and release behavior. C4 cannot infer or pre-authorize those from Mathematics.

The Chemistry profile explicitly reserves subject-specific controls for:

```text
macro ↔ particle ↔ symbolic coordination
chemical identity and nomenclature
measurement / unit / uncertainty
reaction-condition custody
laboratory safety authority
```

This is why `VALIDATE_SUBJECT_SAFETY` is conditional rather than a Mathematics operation.

## 7. Equivalence proof in C4

`validate_subject_adapter_interface_candidate.py` performs design-only equivalence checks. It proves only that:

1. C3 completed and opened the C4 design gate;
2. the candidate and receipt remain non-authoritative;
3. generic operation declarations contain no Mathematics/Chemistry/topic dispatch;
4. every CORE operation has exactly one Mathematics reference binding;
5. conditional subject-safety validation is not silently bound into Mathematics;
6. every Mathematics component reference resolves in the C1 catalog;
7. every Mathematics evidence path is already declared by the referenced C1 component and exists in the current tree;
8. the Mathematics canonical object vocabulary exactly matches the current Canonical Domain Registry schema;
9. Chemistry has no runtime/registry/validator authority in C4;
10. C0-F007 remains `CURRENT + DOCUMENTED ONLY`.

The resulting receipt status is:

```text
C4_SUBJECT_ADAPTER_INTERFACE_EXTRACTED
PASS_DESIGN_PROJECTION_ONLY
```

That is not runtime equivalence. No production code calls the adapter candidate.

## 8. What C4 does not prove

C4 does not prove that a future generic adapter implementation is behaviorally identical to current Mathematics runtime. That requires a later executable migration with side-by-side outputs and fail-closed parity tests.

C4 also does not prove that the Chemistry object model is complete, pedagogically sufficient or safe. It only ensures the generic interface has room for subject-specific structures and safety authority without adding subject branches to Blueprint.

Known residual risks include:

- an operation that appears generic may later hide Mathematics-specific assumptions;
- a future adapter implementation could weaken error handling even if the design mapping is correct;
- canonical object types alone do not capture all subject semantics;
- Chemistry may require additional operation classes discovered only in the bounded C8 pilot;
- subject-specific safety cannot be reduced to a generic boolean or plausibility check;
- C0-F007 remains unresolved at runtime and is unrelated to C4 extraction.

## 9. Promotion rule

C4 authorizes only the next design stage:

```text
C5_SUBTOPIC_INTELLIGENCE_LIBRARY_CONTRACTS_READY
```

Any executable subject-adapter migration must separately identify:

```text
governed production contract;
subject-owned validator;
exact authority source;
old-vs-new parity corpus;
negative/falsification cases;
stale-state behavior;
release impact;
rollback/deprecation path;
owner approval when authority semantics change.
```

Until that happens, current Mathematics execution remains the reference behavior and production code must not consume this design workspace.
