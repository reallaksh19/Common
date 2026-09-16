# MathBlueprint Design Workspace

> **Status: DESIGN / NON-NORMATIVE**
>
> Nothing under this directory is runtime authority, subject authority, publication authority, learner-release authority or a production schema unless an explicit owner-approved migration moves it into the relevant governed contract/policy location and adds executable validation.

## Purpose

This directory holds architecture proposals and architecture-review evidence that are intentionally separated from current executable Mathematics V2 authority.

Current production authority remains in the existing governed schemas, policies, validators, registries and normative documents outside `design/`.

The design workspace exists so future architecture can be reviewed, falsified and reconciled with independent audits before it becomes executable.

## Current design documents

- `STEM_CORE_SPEC_CONSOLIDATION_ROADMAP.md` — proposed consolidation sequence, Architecture Catalog direction, cross-subject adapter boundary, provenance model, risks and migration path.
- `MATHEMATICS_ARCHITECTURE_DOCUMENTATION_DRIFT_AUDIT.md` — Stage-C0 executable-first architecture/documentation drift audit; methodologically independent of the C1 catalog and explicitly non-normative.
- `mathematics-architecture-documentation-drift-audit.json` — machine-readable C0 findings, current-doctrine evidence, C1 post-hoc comparison and C2 documentation-remediation gate.
- `mathematics-architecture-documentation-drift-audit.schema.json` — design-only schema that makes C0 findings falsifiable without promoting the audit into runtime authority.
- `MATHEMATICS_ARCHITECTURE_CATALOG_CANDIDATE.md` — Stage-C1 repository-inventory boundary for the machine-readable architecture catalog candidate; explicitly non-authoritative.
- `mathematics-architecture-catalog.candidate.json` — repository-derived, machine-readable candidate classification of major Mathematics V2 architecture responsibilities; `authority = NONE` and `semantic_change = NONE`.
- `mathematics-architecture-catalog.candidate.schema.json` — design-only schema that keeps the candidate catalog internally falsifiable without promoting it into production authority.
- `MATHEMATICS_NORMATIVE_ROOT_CONSOLIDATION.md` — Stage-C2 migration evidence describing how the normative root and dual-track subordinate specification were reconciled to C0 without runtime semantic change.
- `mathematics-normative-root-consolidation.json` — machine-readable C2 finding dispositions; records C0-F007 as preserved `CURRENT + DOCUMENTED ONLY` and marks C3 generated references ready.
- `mathematics-normative-root-consolidation.schema.json` — design-only schema that prevents the C2 receipt from claiming authority or silently upgrading F007.
- `generate_mathematics_architecture_references.py` — Stage-C3 design-only generator that projects catalog-declared architecture/schema/policy/validator/test references without changing catalog semantics.
- `mathematics-architecture-generated-references.schema.json` — design-only schema for the generated reference manifest; locks authority to `NONE` and publication authorization to `NOT_IMPLIED`.
- `mathematics-generated-references.receipt.json` — machine-readable C3 completion receipt; preserves C0-F007 as documented-only and advances only to the C4 design gate.
- `mathematics-generated-references.receipt.schema.json` — design-only receipt schema that prevents C3 from claiming runtime/publication authority.
- `generated/mathematics-architecture-reference-index.generated.json` — machine-readable C3 architecture/reference projection generated from the frozen C1 catalog.
- `generated/MATHEMATICS_ARCHITECTURE_REFERENCES.generated.md` — generated human reference view containing architecture, schema, policy, validator and catalog-declared test tables.
- `SUBJECT_ADAPTER_INTERFACE_CANDIDATE.md` — Stage-C4 explanation of the subject-neutral interface, current Mathematics reference projection, Chemistry stress target, limitations and promotion rule.
- `stem-subject-adapter-interface.candidate.json` — machine-readable C4 interface candidate with eight core operations, one conditional safety operation, current Mathematics component bindings and an unbound Chemistry stress profile.
- `stem-subject-adapter-interface.candidate.schema.json` — design-only schema that prevents the C4 candidate from claiming authority, runtime migration or Chemistry production bindings.
- `validate_subject_adapter_interface_candidate.py` — design-only C4 equivalence validator; checks C3 custody, C1 component/evidence ownership, exact current Mathematics object vocabulary, subject-neutral operations and Chemistry non-authority.
- `mathematics-subject-adapter-equivalence.receipt.json` — machine-readable C4 receipt; records `PASS_DESIGN_PROJECTION_ONLY`, no Mathematics runtime change/validation weakening and no Chemistry runtime binding.
- `mathematics-subject-adapter-equivalence.receipt.schema.json` — design-only schema locking the C4 receipt to non-authoritative, semantic-noop extraction.
- `SUBTOPIC_INTELLIGENCE_LIBRARY_ROADMAP.md` — proposed ontology and delivery roadmap for the Subtopic Intelligence Library.
- `SUBTOPIC_INTELLIGENCE_LIBRARY_SCHEMA_FAMILY_DRAFT.md` — field-level draft of the proposed SIL schema family and fail-closed invariants.
- `SIL_COMPILATION_AND_CUSTODY_MODEL.md` — proposed deterministic compilation/custody model for reusable subtopic context and run-specific agent context.

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

Generated C3 reference views and the C4 subject-adapter candidate are subject to the same boundary. Reporting that a current Mathematics component has an executable authority effect does not transfer that effect to the design view or adapter candidate.

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

## Relationship between C0, C1, C2, C3 and C4

The five stages have deliberately different evidence roles:

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
```

The C0 audit compares the C1 catalog only **after** deriving the executable model. The C1 catalog therefore remains an index/candidate and never becomes evidence merely by agreeing with C0.

C2 resolved the documentation drift identified by C0-F001 through C0-F006. C0-F007 remains intentionally open as `CURRENT + DOCUMENTED ONLY`: optional EASY research is current policy and accepted by the generation-spec validator, but the canonical SDU/LAU compiler does not yet auto-materialize those bindings.

C3 does not modify that status. Its committed reference view projects **17 architecture components, 24 schema refs, 11 policy refs, 10 validator refs and 2 catalog-declared test refs**. Those counts describe the C1 catalog projection, not the total number of tests or executable files in Mathematics V2.

C4 also preserves C0-F007 unchanged. The C4 Mathematics projection binds **8 core subject-adapter operations** to existing C1 component/evidence identities and verifies **13 canonical Mathematics object types** against the current domain-registry schema. `VALIDATE_SUBJECT_SAFETY` remains conditional and unbound in Mathematics; Chemistry remains `DESIGN_STRESS_TARGET_ONLY` with no production registry or validator reference.

The current design-workspace migration gate is now `C5_SUBTOPIC_INTELLIGENCE_LIBRARY_CONTRACTS_READY`. That status authorizes only SIL contract work; it does not authorize a subject-adapter runtime migration.

If a design/audit/generated reference disagrees with current executable authority, the current executable authority remains in force until an explicit governed migration resolves the documentation or contract conflict.
