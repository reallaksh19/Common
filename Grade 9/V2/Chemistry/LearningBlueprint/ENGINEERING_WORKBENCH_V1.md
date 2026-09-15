# Chemistry Engineering Workbench v1

## Purpose

The Workbench operationalizes the Chemistry Technical Engineering Gate Registry from PR #377 without granting it pedagogical, source-legal, learner-state, or publication authority.

Canonical engineering data remains:

`policies/chemistry-technical-engineering-gates.v1.json`

The hardened production wrapper is:

`engine/validate_chemistry_engineering_gates_v2.py`

## Lifecycle

```text
ENGINEERING REQUEST
        ↓
TOPIC / SUBTOPIC / BUCKET MANIFEST
        ↓
PR377 CHEMISTRY GATE REGISTRY
        ↓
HARDENED PRODUCTION VALIDATION
        ↓
RECURSIVE CHEM-* PREREQUISITE CLOSURE
        ↓
EXTERNAL-PREREQUISITE RESOLUTION
        ↓
RESEARCH DOSSIER + CLAIM LEDGER, when depth = RESEARCH
        ↓
ENGINEERING CLOSURE RECEIPT
        ↓
ENGINEERING PASSPORT
        ↓
ENGINEERING-READY CDAU BOUNDARY
        ↓
CDAU → SDU / LAU → Concept / Problem TTU → v7 PAL
```

Readiness is derived. Requests and manifests may not contain an `engineering_ready` field.

## Layer boundary

Engineering owns technical prerequisite closure only. It does not establish source legality, Core purpose, learner mastery, learner support fit, TTU pedagogy, or publication approval.

Chemistry differs deliberately from the Physics Workbench: Chemistry v6 currently routes Canonical Domain Registry → CDAU → SDU/LAU, so v1 gates the CDAU entry rather than inventing a parallel CCU authority.

## Request and manifest

The request records topic/scope, engineering depth (`FOUNDATION | STANDARD | RESEARCH`) and intended downstream consumers. `RESEARCH` is an engineering evidence mode, not a learner difficulty badge.

The manifest declares direct Chemistry gates only. Internal `CHEM-*` prerequisites are derived recursively. Non-Chemistry prerequisites are reported separately and must be explicitly resolved by authority or auditable owner scope; they are never silently ignored.

Source state remains independent:

`INDEPENDENT_OF_TECHNICAL_GATE | SOURCE_HELD | SOURCE_READY`

## Hardened registry validation

`validate_chemistry_engineering_gates_v2.py` first invokes the exact #377 production validator, then additionally enforces:

- exact registry identity and `maturity = ENGINEERING`;
- no empirical/psychometric maturity claim;
- gate and difficulty maturity remain engineering-only;
- declared canonical concept IDs equal the actual technical-core IDs;
- READY gates have non-empty concepts, representations, reasoning, misconceptions, verifications, problem families, and falsification cases;
- READY gates cannot carry a false release-checklist field.

The release checklist is corroborative metadata, not sufficient proof by itself.

## Closure compiler

`compile_chemistry_engineering_closure.py` validates request/manifest contracts and the current registry, derives recursive Chemistry prerequisites, detects cycles, resolves external prerequisites, requires research artifacts in RESEARCH mode, emits registry/closure SHA-256 digests, and derives `READY | BLOCKED`.

## Passport

The passport is a human-visible projection of the closure receipt. It revalidates receipt semantics and reports internal gate state, external dependency state, independent source state, CDAU technical authorization, and next action.

## CDAU boundary

`validate_cdau_engineering_ready.py` recompiles the current closure from the current registry. It requires `scope_kind = SUBTOPIC`, exact manifest `scope_ref == CDAU.subtopic_id`, and explicit CDAU downstream authorization. Only then is the existing CDAU schema validation invoked.

A stale/manual READY claim therefore cannot authorize CDAU.

## Redox vertical slice

The v1 golden request declares only:

`CHEM-REDOX-OXIDATION`

The compiler must derive the internal Chemistry prerequisite closure from the registry and separately expose `MATH-BASIC-ARITHMETIC` as an external prerequisite. The golden resolves that external dependency explicitly as an owner-confirmed Grade-9 entry-scope prerequisite; this is visible in the receipt and is not disguised as source evidence.

The manifest binds `scope_ref = REDOX-SPECIES-STATE-AGENT`, matching the existing v6 Redox CDAU fixture.

## Falsification requirements

The production tests prove at minimum: exact Redox closure derivation; CDAU authorization only through current READY closure; unknown/missing/non-ready gates block; cycles fail; unresolved external prerequisites block; RESEARCH without dossier/claim ledger blocks; manual readiness fields are schema-rejected; passport rejects contradictory receipts; scope mismatch blocks CDAU; and empirical maturity overclaim is rejected.
