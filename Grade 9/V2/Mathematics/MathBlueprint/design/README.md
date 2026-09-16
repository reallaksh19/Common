# MathBlueprint Design Workspace

> **Status: DESIGN / NON-NORMATIVE**
>
> Nothing under this directory is runtime authority, subject authority, publication authority, learner-release authority or a production schema unless an explicit owner-approved migration moves it into the relevant governed contract/policy location and adds executable validation.

## Purpose

This directory holds architecture proposals that are intentionally separated from current executable Mathematics V2 authority.

Current production authority remains in the existing governed schemas, policies, validators, registries and normative documents outside `design/`.

The design workspace exists so future architecture can be reviewed, falsified and reconciled with independent audits before it becomes executable.

## Current design documents

- `STEM_CORE_SPEC_CONSOLIDATION_ROADMAP.md` — proposed consolidation of the future Core Specification, Architecture Catalog, cross-subject adapter boundary, provenance model, risks and migration path.
- `MATHEMATICS_ARCHITECTURE_CATALOG_CANDIDATE.md` — Stage-C1 repository-inventory boundary for the machine-readable architecture catalog candidate; explicitly blocks normative Core-Spec consolidation pending the independent audit.
- `mathematics-architecture-catalog.candidate.json` — repository-derived, machine-readable candidate classification of major Mathematics V2 architecture responsibilities; `authority = NONE` and `semantic_change = NONE`.
- `mathematics-architecture-catalog.candidate.schema.json` — design-only schema that keeps the candidate catalog internally falsifiable without promoting it into production authority.
- `SUBTOPIC_INTELLIGENCE_LIBRARY_ROADMAP.md` — proposed ontology and delivery roadmap for the Subtopic Intelligence Library.
- `SUBTOPIC_INTELLIGENCE_LIBRARY_SCHEMA_FAMILY_DRAFT.md` — field-level draft of the proposed SIL schema family and fail-closed invariants.
- `SIL_COMPILATION_AND_CUSTODY_MODEL.md` — proposed deterministic compilation/custody model for reusable subtopic context and run-specific agent context.

## Mandatory boundary

The intended flow is:

```text
DESIGN
    ↓ review / audit / owner decision
APPROVED ARCHITECTURE CHANGE
    ↓
GOVERNED SCHEMA / POLICY / VALIDATOR / DATA
    ↓
PRODUCTION RUNTIME
```

Forbidden:

```text
production runtime
    → directly reads design/*.md as authority
```

Also forbidden:

```text
design prose
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

## Relationship to the Phase-1 audit

The independent Architecture / Documentation Drift Audit and Architecture Explorer should treat this directory as `ROADMAP / DESIGN`, never as evidence of current production behavior.

If a design document disagrees with current executable authority, the current executable authority remains in force until an explicit migration resolves the conflict.
