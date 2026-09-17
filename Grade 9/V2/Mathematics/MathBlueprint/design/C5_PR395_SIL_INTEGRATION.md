# C5 — Subtopic Intelligence Library contracts + PR #395 integration

> **Status: DESIGN / NON-NORMATIVE / NO RUNTIME MIGRATION**
>
> This stage integrates the useful SIL work from PR #395 without importing its branch wholesale or allowing its Markdown corpus to become mathematical authority.

## 1. Why selective integration is required

At the integration point, PR #395 and the canonical PR #351 branch are diverged from merge-base `d86e7b764edbb8f72d5358c93ee57fb4ebd6cad8`:

```text
PR #395 head: 242878b04787905087060318c14b89b14238f195
PR #351 C4:   41d6040565408fe0ee5844090da19947358b31d9
relationship: DIVERGED
#395 ahead:   21 commits
#395 behind:   9 commits
```

A whole-branch merge would mix pre-C4 architectural assumptions with the C4 authority boundary. C5 therefore uses immutable candidate pins and explicit normalization instead.

## 2. What is accepted from PR #395

C5 recognizes four candidate surfaces at the exact pinned PR #395 head:

- `SUBTOPIC_INTELLIGENCE_INTAKE_SPECIFICATION.md` → **candidate subtopic corpus**.
- `validate_subtopic_intelligence_library.py` → **structural validator reference**.
- `references/NANO_LEVEL_SUBTOPIC_INTELLIGENCE_RESEARCH.md` → **candidate research corpus**.
- `tools/sil_explorer/generate_sil_catalog.py` → **observability tooling candidate**.

These are useful inputs. None is subject authority.

## 3. Critical incompatibility resolved by C5

The PR #395 SIL validator demonstrates that packets have structural content by counting items such as preconditions, atoms, misconception contrasts, TTUs and problem families. That is useful as an authoring-completeness signal, but it does not prove that embedded formulas, invariants, prerequisite claims, scope mappings or problem-family identities already resolve to current governed Engineering/Domain authority.

C5 therefore replaces the authority interpretation with:

```text
PR395 candidate prose / research / tooling
        ↓
C5 candidate classification
        ↓
EXACT existing governed identity resolution
        ↓
reference-only SIL composition
        ↓
explicit gap when exact authority is absent
```

Never:

```text
well-formed packet
        ↓
mathematical authority
```

## 4. C5 contract family

C5 introduces five design-only schema candidates:

1. `stem-subtopic-intelligence-pack.candidate.schema.json`
2. `stem-learning-transition.candidate.schema.json`
3. `stem-source-selection-profile.candidate.schema.json`
4. `stem-library-gap.candidate.schema.json`
5. `stem-library-coverage-report.candidate.schema.json`

The pack is a compiled context view. It contains exact references and dependency custody, not copied mathematical payloads.

## 5. Ownership boundary

```text
Mathematical truth / logical prerequisite
    → Subject Engineering / Canonical Domain

Assessment capability requirement / problem-family identity
    → Assessment / canonical domain authority

Instructional sequence / repair sequence / representation-use choice
    → governed learning structure / pedagogy

Source suitability rationale
    → source-selection profile

Missing required information
    → first-class gap routed to owning authority

Coverage state
    → derived report only
```

An `INSTRUCTIONAL_SEQUENCE` cannot satisfy a `LOGICAL_DEPENDENCY_REFERENCE`. Source suitability cannot satisfy subject authority. Coverage PASS cannot imply technical or publication authorization.

## 6. Pack authority locks

Every candidate pack is schema-locked to semantics equivalent to:

```text
status = DESIGN_CANDIDATE
authority = NONE
view_class = COMPILED_SUBTOPIC_INTELLIGENCE_CONTEXT
technical_authorization = NOT_GRANTED_BY_PACK
publication_authorization = NOT_IMPLIED
learner_mastery_claim = NOT_IMPLIED
```

Learner percentage remains run/LAU state and is not embedded as canonical subtopic truth.

## 7. PR #395 content promotion rules

PR #395 material can be reused only by class:

```text
candidate mathematical claim
    → exact current subject/domain ref OR MISSING_SUBJECT_TRUTH gap

candidate logical prerequisite
    → exact subject dependency ref OR MISSING_LOGICAL_PREREQUISITE gap

candidate teaching sequence / repair
    → governed learning-transition proposal

candidate research claim
    → existing claim-level research promotion workflow

candidate exam/scope mapping
    → exact scope authority OR MISSING_SCOPE_AUTHORITY gap

candidate explorer/tooling
    → derived view over normalized contracts only
```

## 8. Fail-closed validation

`validate_c5_sil_contracts.py` checks:

- C4 exact predecessor status and custody.
- C0-F007 remains `CURRENT + DOCUMENTED ONLY`.
- all five C5 contracts are design-only and digest-pinned.
- pack schema does not admit inline equation/formula/statement/solution payload fields.
- transition schema distinguishes subject-owned logical dependency from pedagogy-owned sequencing.
- source profiles cannot grant technical authority.
- coverage cannot grant technical/publication authority.
- PR #395 remains candidate-only and whole-branch merge is forbidden.
- current Mathematics canonical object vocabulary remains the 13 types exposed by the existing domain schema.

`test_c5_sil_contracts.py` mutation-falsifies these boundaries.

## 9. What C5 does not do

C5 does **not**:

- merge PR #395 wholesale;
- promote its 15 packets into Engineering authority;
- replace current Mathematics schemas or validators;
- alter Blueprint runtime;
- change learner calibration behavior;
- resolve C0-F007;
- authorize publication;
- establish a Chemistry runtime.

## 10. Next stage

C5 advances only to:

```text
C6_MATHEMATICS_SIL_PILOT_READY
```

C6 should normalize one high-stress Mathematics vertical (Theory of Equations is the preferred pilot) by resolving PR #395 candidate material against exact current Engineering/Domain authority, routing every unresolved claim to a typed gap, and compiling a deterministic reference-only pack. No mass library population should precede that pilot.
