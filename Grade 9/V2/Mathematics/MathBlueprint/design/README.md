# MathBlueprint Design Workspace

> **Status: DESIGN / NON-NORMATIVE**
>
> Nothing under this directory is runtime authority, subject authority, publication authority, learner-release authority or a production schema unless an explicit owner-approved migration moves it into the relevant governed contract/policy location and adds executable validation.

## Purpose

This directory holds architecture proposals and architecture-review evidence that are intentionally separated from current executable Mathematics V2 authority.

Current production authority remains in the existing governed schemas, policies, validators, registries and normative documents outside `design/`.

The design workspace exists so future architecture can be reviewed, falsified and reconciled with independent audits before it becomes executable.

## Current design documents

- `STEM_CORE_SPEC_CONSOLIDATION_ROADMAP.md` — proposed consolidation of the future Core Specification, Architecture Catalog, cross-subject adapter boundary, provenance model, risks and migration path.
- `MATHEMATICS_ARCHITECTURE_DOCUMENTATION_DRIFT_AUDIT.md` — Stage-C0 executable-first architecture/documentation drift audit; methodologically independent of the C1 catalog and explicitly non-normative.
- `mathematics-architecture-documentation-drift-audit.json` — machine-readable C0 findings, current-doctrine evidence, C1 post-hoc comparison and C2 documentation-remediation gate.
- `mathematics-architecture-documentation-drift-audit.schema.json` — design-only schema that makes C0 findings falsifiable without promoting the audit into runtime authority.
- `MATHEMATICS_ARCHITECTURE_CATALOG_CANDIDATE.md` — Stage-C1 repository-inventory boundary for the machine-readable architecture catalog candidate; explicitly non-authoritative.
- `mathematics-architecture-catalog.candidate.json` — repository-derived, machine-readable candidate classification of major Mathematics V2 architecture responsibilities; `authority = NONE` and `semantic_change = NONE`.
- `mathematics-architecture-catalog.candidate.schema.json` — design-only schema that keeps the candidate catalog internally falsifiable without promoting it into production authority.
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

Moving prose from this folder into production code without those controls is an architectural regression.

## Relationship between C0 and C1

C0 and C1 have deliberately different evidence roles:

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
```

The C0 audit compares the C1 catalog only **after** deriving the executable model. The C1 catalog therefore remains an index/candidate and never becomes evidence merely by agreeing with C0.

The current C0 result is `READY_WITH_DOCUMENTATION_REMEDIATIONS` for Stage C2, with zero owner-decision blockers. That statement is a design-workspace migration gate only; it does not itself rewrite any current normative document.

If a design/audit document disagrees with current executable authority, the current executable authority remains in force until an explicit governed migration resolves the documentation or contract conflict.
