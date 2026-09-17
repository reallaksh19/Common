# C5 — SIL field contracts and PR #395 integration hardening

> **Status: DESIGN / NON-NORMATIVE / NO RUNTIME MIGRATION**
>
> This note supplements the existing `stem-subtopic-intelligence-contract-family.candidate.json`. That file is the single C5 family root. The work here adds field-level contracts, deterministic validation, mutation falsifiers, custody and a completion receipt; it does not create a second SIL ontology.

## 1. Integration basis

The C5 family already records the exact PR #395 integration state:

```text
PR #395 head: 242878b04787905087060318c14b89b14238f195
C4 branch head used by the audit: 41d6040565408fe0ee5844090da19947358b31d9
merge base: d86e7b764edbb8f72d5358c93ee57fb4ebd6cad8
relationship at audit: DIVERGED_21_AHEAD_9_BEHIND
import mode: DIGEST_PINNED_CANDIDATE_SOURCE_ONLY
```

The current C5 root pins four #395 artifacts: the SIL packet corpus, its structural validator, the nano-level research reference, and the SIL catalog generator. Their direct runtime and direct normative import are both forbidden.

## 2. Why the PR #395 SIL cannot be promoted as written

PR #395 contains substantial useful academic content, but its SIL validator proves structural presence by counting preconditions, atoms, misconception contrasts, TTUs and problem families. That is an authoring-completeness signal. It is not proof that embedded equations, invariants, logical prerequisites, scope claims or problem-family identities already resolve to current governed Engineering/Canonical Domain authority.

C5 therefore interprets #395 as:

```text
candidate corpus / research / tooling
        ↓
exact-ID normalization
        ↓
current authority revalidation
        ↓
reference-only SIL composition
        ↓
explicit typed gap when exact authority is absent
```

Never:

```text
well-formed packet → mathematical authority
```

## 3. Single C5 contract family

The existing family root defines five contract objects:

```text
STEM-SIL-SUBTOPIC-PACK
STEM-SIL-LEARNING-TRANSITION
STEM-SIL-SOURCE-SELECTION-PROFILE
STEM-SIL-LIBRARY-GAP
STEM-SIL-COVERAGE-REPORT
```

This hardening stage adds one field-level JSON Schema candidate for each object. They are subordinate to the family root; conflicting definitions are rejected by validation.

## 4. Pack model

The pack is a compiled context view, not a subject registry:

```text
view_class = COMPILED_SUBTOPIC_INTELLIGENCE_CONTEXT
authority = COMPOSITION_OF_BOUND_GOVERNED_REFERENCES
technical_authorization = NOT_GRANTED_BY_PACK
publication_authorization = NOT_IMPLIED
learner_mastery_claim = NOT_IMPLIED
```

Its exact-reference envelope requires:

```text
ref
ref_type
subject_id
registry_ref
registry_version_or_digest
```

The pack schema intentionally has no field for inline equation expressions, mathematical statements, derivation steps, canonical solutions or problem prompts. Subject truth is referenced, never re-authored inside the pack.

## 5. Dependency ownership

The family and field contracts distinguish five dependency classes:

```text
LOGICAL_DEPENDENCY
    owner = SUBJECT_ENGINEERING
    SIL may define = false

ASSESSMENT_CAPABILITY_DEPENDENCY
    owner = ASSESSMENT
    SIL may define = false

INSTRUCTIONAL_SEQUENCE
    owner = LEARNING_STRUCTURE
    SIL may define = true

REPRESENTATION_BRIDGE
    owner = LEARNING_STRUCTURE
    SIL may define = true

REPAIR_SEQUENCE
    owner = LEARNING_STRUCTURE
    SIL may define = true
```

An instructional preference cannot become proof of mathematical necessity. A learning-transition record may explain a bridge, but logical dependency remains exact subject authority.

## 6. Source selection, gaps and coverage

Source-selection profiles may state role, suitability, rationale, limitations, rejection conditions, capture/version and reuse state. They cannot grant technical authority.

A missing required fact becomes a first-class gap. Examples include:

```text
MISSING_SUBJECT_TRUTH
MISSING_LOGICAL_PREREQUISITE
MISSING_INSTRUCTIONAL_BRIDGE
MISSING_ASSESSMENT_EVIDENCE
MISSING_SCOPE_AUTHORITY
MISSING_PEDAGOGY_EVIDENCE
```

The gap routes to the owning authority. It is never auto-closed with plausible prose.

Coverage is derived only:

```text
authority = DERIVED_LIBRARY_COVERAGE
technical_authorization = NOT_IMPLIED
publication_authorization = NOT_IMPLIED
```

## 7. PR #395 layer normalization

The existing family root maps the four #395 packet layers as follows:

```text
Layer 1 mathematical core
    → EXACT_SUBJECT_REFERENCE_OR_GAP

Layer 2 cognitive transformations
    → EXACT_DOMAIN_REFERENCE + GOVERNED_LEARNING_TRANSITION_OR_GAP

Layer 3 reconstructable TTU
    → NON_AUTHORITATIVE_TTU_CANDIDATE_INPUT_ONLY

Layer 4 problem families
    → EXACT_PROBLEM_FAMILY_OR_ASSESSMENT_REFERENCE_OR_GAP
```

Automatic authority promotion is false for every layer.

## 8. Deterministic validator

`validate_c5_sil_contracts.py` verifies:

- the existing C5 family validates against its schema;
- C4 is the exact legal predecessor and remains non-authoritative;
- the current 13-type Mathematics domain vocabulary matches the family projection exactly;
- all five contract objects remain non-authorizing and non-inline;
- dependency ownership cannot be reassigned to SIL;
- exact references fail closed to `EMIT_GAP_AND_BLOCK_DEPENDENT_CLAIM`;
- the four PR #395 source artifact blob pins remain exact;
- no #395 layer can auto-promote authority;
- each field-level schema remains valid and aligned to family locks;
- the pack cannot acquire inline subject-truth fields;
- source selection and coverage cannot grant authority;
- C0-F007 remains `CURRENT + DOCUMENTED ONLY`;
- receipt custody is exact when the receipt is present.

`test_c5_sil_contracts.py` mutation-falsifies these boundaries.

## 9. What C5 does not do

C5 does not merge PR #395 wholesale, promote its 15 packets into Engineering, change the current Mathematics runtime, alter learner calibration, resolve F007, authorize publication, or establish Chemistry production authority.

It also does not mass-populate SIL. The purpose of C5 is to make the contract boundary strong enough that population can happen without an agent silently inventing architecture or subject truth.

## 10. Next stage

C5 advances only to:

```text
C6_MATHEMATICS_SIL_PILOT_READY
```

C6 should normalize one high-stress Mathematics vertical—preferably Theory of Equations—against exact current Engineering/Canonical Domain authority, route every unresolved claim to a typed gap, and compile a deterministic reference-only pack. Mass population should wait until that pilot survives reproducibility and non-algebra stress tests.
