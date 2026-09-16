# Mathematics V2 — C2 Normative-Root Consolidation

> **Status: DESIGN EVIDENCE / NON-NORMATIVE**
>
> This file records the C2 migration result. It does not create runtime, subject, publication or learner-release authority. The normative changes are the explicit edits to `CANONICAL_ARCHITECTURE.md` and `DUAL_TRACK_PRODUCT_MODEL.md`; executable authority remains in the governed schemas, policies, validators, compilers and release gates.

## Result

Stage C2 reconciles the normative architecture documents against the executable-first C0 audit without changing runtime semantics.

The consolidation resolves the documentation drift recorded by C0-F001 through C0-F006 and deliberately preserves C0-F007 as a visible implementation gap.

```text
C0-F001 Engineering authority omitted from root      -> documentation reconciled
C0-F002 EASY research rule stale                     -> documentation reconciled
C0-F003 publication topology stale                   -> documentation reconciled
C0-F004 discovery boundary omitted                   -> documentation reconciled
C0-F005 claim-level research promotion omitted       -> documentation reconciled
C0-F006 derived Engineering visibility omitted       -> documentation reconciled
C0-F007 EASY research compiler materialization gap   -> PRESERVED, not upgraded
```

## Canonical authority result

The consolidated root now expresses the durable authority order as:

```text
non-authoritative discovery
        ↓ explicit exact-ID selection
Engineering technical authority
        ↓ current validation + depth + prerequisite closure + custody
Canonical Domain admission
        ↓
Core0 / Core1 / Core2
        ↓
Canonical Domain Registry
        ↓
CDAU → SDU / LAU → TTU
        ↓
Core1A / Core1B / Core2A / Core2B
        ↓
product release gate
        ↓
derived Engineering visibility
NON-AUTHORITATIVE; publication_authorization = NOT_IMPLIED
        ↓
semantic learner publication bundle
        ↓
bundle-only deterministic rendering
```

Core1 remains semantic reconstruction authority and Core2 remains assessment/source-question authority only inside already-authorized mathematical scope. Topic-specific mathematical truth remains upstream in governed Engineering data.

## F007 remains open at runtime

Current policy and generation-spec validation permit fully bound optional EASY pedagogy research. The canonical SDU/LAU compiler still materializes research bindings only for non-EASY rows.

Therefore C2 records:

```text
OPTIONAL EASY RESEARCH POLICY / VALIDATION      = CURRENT + EXECUTABLE
OPTIONAL EASY RESEARCH AUTO-MATERIALIZATION
THROUGH CANONICAL SDU/LAU COMPILER              = CURRENT + DOCUMENTED ONLY
```

C2 does not modify `engine/compile_sdu_lau_generation_spec.py`. A later governed compiler migration must add its own falsifier before this status may become `CURRENT + EXECUTABLE`.

## Semantic-change boundary

C2 is a documentation consolidation only:

```text
authority = NONE
semantic_change = NONE
runtime semantics changed = false
owner-decision blockers = 0
```

The machine-readable receipt is `design/mathematics-normative-root-consolidation.json`, validated against `design/mathematics-normative-root-consolidation.schema.json`.

## Next stage

C2 unblocks **Stage C3 — generated references**. C3 should generate architecture/schema/policy/validator/test reference tables from machine-readable metadata without turning generated views into authority.
