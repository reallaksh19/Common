# MathBlueprint Design Workspace

> **Status: DESIGN / NON-NORMATIVE**
>
> Nothing under this directory is runtime authority, subject authority, publication authority, learner-release authority or a production schema unless an explicit governed migration moves it into the relevant contract/policy location and adds executable validation.

## Purpose

This directory holds architecture proposals, architecture-review evidence, generated reference views and migration receipts intentionally separated from current executable Mathematics V2 authority.

Current production authority remains in governed schemas, policies, validators, registries and normative documents outside `design/`.

## Stage index

### C0 — executable-first architecture/documentation audit

- `MATHEMATICS_ARCHITECTURE_DOCUMENTATION_DRIFT_AUDIT.md`
- `mathematics-architecture-documentation-drift-audit.json`
- `mathematics-architecture-documentation-drift-audit.schema.json`

C0 independently derived current executable architecture before comparing documentation. Findings C0-F001 through C0-F006 were documentation drift; C0-F007 remains `CURRENT + DOCUMENTED ONLY`.

### C1 — Architecture Catalog candidate

- `MATHEMATICS_ARCHITECTURE_CATALOG_CANDIDATE.md`
- `mathematics-architecture-catalog.candidate.json`
- `mathematics-architecture-catalog.candidate.schema.json`

C1 is a non-authoritative repository classification/index, not evidence merely because it agrees with C0.

### C2 — normative-root consolidation evidence

- `MATHEMATICS_NORMATIVE_ROOT_CONSOLIDATION.md`
- `mathematics-normative-root-consolidation.json`
- `mathematics-normative-root-consolidation.schema.json`

C2 reconciled the normative root to C0 without changing executable semantics and preserved F007 as documented-only.

### C3 — generated architecture references

- `generate_mathematics_architecture_references.py`
- `mathematics-architecture-generated-references.schema.json`
- `mathematics-generated-references.receipt.json`
- `mathematics-generated-references.receipt.schema.json`
- `generated/mathematics-architecture-reference-index.generated.json`
- `generated/MATHEMATICS_ARCHITECTURE_REFERENCES.generated.md`

C3 deterministically projects catalog-declared references. The generated view is non-authoritative and publication authorization is not implied.

### C4 — subject-adapter interface extraction

- `SUBJECT_ADAPTER_INTERFACE_CANDIDATE.md`
- `stem-subject-adapter-interface.candidate.json`
- `stem-subject-adapter-interface.candidate.schema.json`
- `validate_subject_adapter_interface_candidate.py`
- `mathematics-subject-adapter-equivalence.receipt.json`
- `mathematics-subject-adapter-equivalence.receipt.schema.json`

C4 binds eight subject-neutral operations to already-current Mathematics evidence, verifies the current 13-type Mathematics canonical object vocabulary, retains Chemistry only as an unbound design stress target, and makes no runtime migration.

### C5 — Subtopic Intelligence Library contracts + PR #395 integration

Single family root:

- `stem-subtopic-intelligence-contract-family.candidate.json`
- `stem-subtopic-intelligence-contract-family.candidate.schema.json`

Field-level subcontracts:

- `stem-subtopic-intelligence-pack.candidate.schema.json`
- `stem-learning-transition.candidate.schema.json`
- `stem-source-selection-profile.candidate.schema.json`
- `stem-library-gap.candidate.schema.json`
- `stem-library-coverage-report.candidate.schema.json`

Validation/evidence:

- `C5_PR395_SIL_INTEGRATION.md`
- `validate_c5_sil_contracts.py`
- `test_c5_sil_contracts.py`
- `mathematics-c5-sil-contracts.receipt.json`

The C5 family is the single design root; the five field schemas are subordinate contracts, not a competing ontology.

PR #395 is integrated at exact head `242878b04787905087060318c14b89b14238f195` as `DIGEST_PINNED_CANDIDATE_SOURCE_ONLY`. The family pins four source artifacts: the 15-packet SIL corpus, its structural validator, the nano-level research input and the SIL catalog generator. Direct normative import and direct runtime import are both false.

At C5 audit time PR #395 and the C4 branch were diverged from merge-base `d86e7b764edbb8f72d5358c93ee57fb4ebd6cad8` (`21` commits ahead, `9` behind). C5 therefore does not merge #395 wholesale.

The normalization rule is fail-closed:

```text
PR395 candidate content
    ↓
EXACT governed identity / current authority revalidation
    ↓
reference-only SIL composition
```

If the exact authority does not exist:

```text
EMIT_GAP_AND_BLOCK_DEPENDENT_CLAIM
```

Never:

```text
well-formed packet / source suitability / discovery rank / coverage PASS
    → subject authority
```

The C5 dependency boundary is explicit:

```text
LOGICAL_DEPENDENCY                 → SUBJECT_ENGINEERING; SIL may not define
ASSESSMENT_CAPABILITY_DEPENDENCY   → ASSESSMENT; SIL may not define
INSTRUCTIONAL_SEQUENCE             → LEARNING_STRUCTURE; SIL may define
REPRESENTATION_BRIDGE              → LEARNING_STRUCTURE; SIL may define
REPAIR_SEQUENCE                    → LEARNING_STRUCTURE; SIL may define
```

The compiled pack remains a composition view:

```text
view_class = COMPILED_SUBTOPIC_INTELLIGENCE_CONTEXT
authority = COMPOSITION_OF_BOUND_GOVERNED_REFERENCES
technical_authorization = NOT_GRANTED_BY_PACK
publication_authorization = NOT_IMPLIED
learner_mastery_claim = NOT_IMPLIED
```

C5 preserves C0-F007 unchanged and makes no production/runtime migration.

### Long-range design inputs

- `STEM_CORE_SPEC_CONSOLIDATION_ROADMAP.md`
- `SUBTOPIC_INTELLIGENCE_LIBRARY_ROADMAP.md`
- `SUBTOPIC_INTELLIGENCE_LIBRARY_SCHEMA_FAMILY_DRAFT.md`
- `SIL_COMPILATION_AND_CUSTODY_MODEL.md`

## Mandatory boundary

```text
DESIGN / AUDIT EVIDENCE
    ↓ review / owner decision when required
APPROVED ARCHITECTURE CHANGE
    ↓
GOVERNED SCHEMA / POLICY / VALIDATOR / DATA
    ↓
PRODUCTION RUNTIME
```

Forbidden:

```text
production runtime → directly reads design/* as authority
```

Also forbidden:

```text
design or audit prose → silently overrides an existing schema, policy, validator or registry
```

A design idea becomes executable only through an explicit migration identifying the new/changed governed contract, ownership domain, validator/compiler, fail-closed tests, compatibility effect, release-class effect and any required owner decision.

## Current design gate

C5 advances only to:

```text
C6_MATHEMATICS_SIL_PILOT_READY
```

C6 should normalize one high-stress Mathematics vertical—preferably Theory of Equations—against exact current Engineering/Canonical Domain authority, route every unresolved claim to a typed gap, and compile a deterministic reference-only pack.

C6 does **not** authorize mass SIL population, subject-adapter runtime migration, Chemistry production authority or publication.

If a design/audit/generated reference disagrees with current executable authority, current executable authority remains in force until an explicit governed migration resolves the conflict.
