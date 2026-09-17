# MathBlueprint Design Workspace

> **Status: DESIGN / NON-NORMATIVE**
>
> Nothing under this directory is runtime authority, subject authority, publication authority, learner-release authority or a production schema unless an explicit governed migration moves it into the relevant contract/policy location and adds executable validation.

## Purpose

This directory holds architecture proposals, review evidence and migration receipts intentionally separated from current executable Mathematics V2 authority.

Current production authority remains in the governed schemas, policies, validators, registries and normative documents outside `design/`.

The design workspace exists so future architecture can be reviewed, falsified and reconciled with independent audits before it becomes executable.

## Current design documents

### C0 — executable-first audit

- `MATHEMATICS_ARCHITECTURE_DOCUMENTATION_DRIFT_AUDIT.md`
- `mathematics-architecture-documentation-drift-audit.json`
- `mathematics-architecture-documentation-drift-audit.schema.json`

### C1 — Architecture Catalog candidate

- `MATHEMATICS_ARCHITECTURE_CATALOG_CANDIDATE.md`
- `mathematics-architecture-catalog.candidate.json`
- `mathematics-architecture-catalog.candidate.schema.json`

### C2 — normative-root consolidation evidence

- `MATHEMATICS_NORMATIVE_ROOT_CONSOLIDATION.md`
- `mathematics-normative-root-consolidation.json`
- `mathematics-normative-root-consolidation.schema.json`

### C3 — generated architecture references

- `generate_mathematics_architecture_references.py`
- `mathematics-architecture-generated-references.schema.json`
- `mathematics-generated-references.receipt.json`
- `mathematics-generated-references.receipt.schema.json`
- `generated/mathematics-architecture-reference-index.generated.json`
- `generated/MATHEMATICS_ARCHITECTURE_REFERENCES.generated.md`

### C4 — subject-adapter interface extraction

- `SUBJECT_ADAPTER_INTERFACE_CANDIDATE.md`
- `stem-subject-adapter-interface.candidate.json`
- `stem-subject-adapter-interface.candidate.schema.json`
- `validate_subject_adapter_interface_candidate.py`
- `mathematics-subject-adapter-equivalence.receipt.json`
- `mathematics-subject-adapter-equivalence.receipt.schema.json`

### C5 — SIL contracts + PR #395 selective integration

- `C5_PR395_SIL_INTEGRATION.md` — integration rationale, ownership boundary, promotion rules and next-stage condition.
- `pr395-sil-integration.candidate.json` — immutable PR #395 candidate-surface pins; whole-branch merge explicitly unauthorized.
- `c5-sil-contract-catalog.candidate.json` — five-contract C5 catalog and authority invariants.
- `stem-subtopic-intelligence-pack.candidate.schema.json` — reference-only compiled context pack candidate.
- `stem-learning-transition.candidate.schema.json` — typed learning transitions separating subject-owned dependency from pedagogy-owned sequencing/repair.
- `stem-source-selection-profile.candidate.schema.json` — source role/suitability metadata without authority promotion.
- `stem-library-gap.candidate.schema.json` — typed unresolved-state routing; missing truth becomes a gap rather than generated prose.
- `stem-library-coverage-report.candidate.schema.json` — derived coverage only; no technical/publication authority.
- `validate_c5_sil_contracts.py` — fail-closed C5 contract/custody validator.
- `test_c5_sil_contracts.py` — mutation falsifiers for authority, PR #395 custody and predecessor-gate boundaries.
- `mathematics-c5-sil-contracts.receipt.json` — C5 completion receipt advancing only to the C6 Mathematics pilot.

### Long-range design inputs

- `STEM_CORE_SPEC_CONSOLIDATION_ROADMAP.md`
- `SUBTOPIC_INTELLIGENCE_LIBRARY_ROADMAP.md`
- `SUBTOPIC_INTELLIGENCE_LIBRARY_SCHEMA_FAMILY_DRAFT.md`
- `SIL_COMPILATION_AND_CUSTODY_MODEL.md`

## Mandatory boundary

The intended flow is:

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
production runtime
    → directly reads design/* as authority
```

Also forbidden:

```text
design or audit prose
    → silently overrides an existing schema, policy, validator or registry
```

Generated C3 reference views, the C4 subject-adapter candidate, and all C5 SIL contracts/integration manifests are subject to the same boundary. Reporting or composing an executable authority does not transfer that authority to a design view.

## Promotion rule

A design idea becomes executable only through an explicit migration that identifies:

```text
new or changed governed contract;
ownership / authority domain;
validator or compiler;
fail-closed tests;
migration / compatibility effect;
release-class effect;
owner decision when authority semantics change.
```

Moving prose or design data from this folder into production code without those controls is an architectural regression.

## Relationship between C0–C5

The six stages have deliberately different evidence roles:

```text
C0
schemas / policies / validators / compilers / release path
→ independently derive current executable architecture
→ compare normative documentation
→ classify drift

C1
repository inventory
→ classify architecture responsibilities
→ no semantic change

C2
consume C0 findings
→ reconcile normative root/subordinate documentation
→ preserve executable behavior
→ keep documented-only runtime gaps explicit

C3
consume the unchanged C1 catalog after the C2 gate
→ deterministically generate architecture/schema/policy/validator/test references
→ bind the view to exact catalog/schema/C2/generator Git blobs
→ remain derived and non-authoritative

C4
consume the completed C3 design gate + current C1 component inventory
→ define subject-neutral adapter operations
→ map Mathematics operations only to already-current component/evidence identities
→ verify Mathematics object vocabulary against the current Canonical Domain Registry schema
→ retain Chemistry as an unbound design stress target
→ make no runtime migration and weaken no Mathematics validation

C5
consume the completed C4 gate + current SIL design work
→ classify PR #395 SIL/research/tooling as immutable candidate inputs
→ reject whole-branch architectural import because #395 and #351 diverged
→ define reference-only pack / transition / source / gap / coverage contracts
→ preserve exact subject authority outside SIL
→ route missing authority to typed gaps
→ add deterministic contract/custody falsifiers
→ make no runtime migration
```

The C0 audit compares the C1 catalog only **after** deriving the executable model. The C1 catalog therefore remains an index/candidate and never becomes evidence merely by agreeing with C0.

C2 resolved documentation drift C0-F001 through C0-F006. C0-F007 remains intentionally open as `CURRENT + DOCUMENTED ONLY`: optional EASY research is current policy and accepted by generation-spec validation, but the canonical SDU/LAU compiler does not yet auto-materialize those bindings.

C3 does not modify that status. Its committed reference view projects **17 architecture components, 24 schema refs, 11 policy refs, 10 validator refs and 2 catalog-declared test refs**. Those counts describe the C1 catalog projection, not the total number of tests or executable files in Mathematics V2.

C4 preserves C0-F007 unchanged. Its Mathematics projection binds **8 core subject-adapter operations** to existing C1 component/evidence identities and verifies **13 canonical Mathematics object types** against the current domain-registry schema. `VALIDATE_SUBJECT_SAFETY` remains conditional and unbound in Mathematics; Chemistry remains `DESIGN_STRESS_TARGET_ONLY` with no production registry or validator reference.

C5 also preserves C0-F007 unchanged. PR #395 is integrated only through exact candidate pins at head `242878b04787905087060318c14b89b14238f195`. At review time #395 is 21 commits ahead and 9 behind the C4 branch from merge-base `d86e7b764edbb8f72d5358c93ee57fb4ebd6cad8`; a whole-branch merge is therefore explicitly not part of C5. Its SIL prose, nano-level research and structural validator remain candidate inputs until exact governed identities or claim-level research promotion exist.

The current design-workspace migration gate is now:

```text
C6_MATHEMATICS_SIL_PILOT_READY
```

C6 should normalize one high-stress Mathematics vertical against exact current Engineering/Domain authority and compile a deterministic reference-only pack. It does not authorize mass SIL population, subject-adapter runtime migration, Chemistry production authority or publication.

If a design/audit/generated reference disagrees with current executable authority, current executable authority remains in force until an explicit governed migration resolves the conflict.
