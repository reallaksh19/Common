# Two-Core Contract Schema Freeze v1

**Status:** JOINT V1 CONTRACT FROZEN — implementation pending  
**Schema family:** `Grade 9/Architecture/contracts/v1/`  
**Applies to:** Core (1) Research in PR #160 and Core (2) Publisher in PR #161  
**JSON Schema dialect:** Draft 2020-12  
**Freeze evidence:** GitHub Actions run `34447311075`

## Freeze objective

This directory converts the reviewed architecture into a small, versioned machine interface before any broad skill migration or renderer rewrite.

The frozen boundary is:

```text
Shared Canonical Registry
        ↓
Project ScopeGraph
        ↓
Core (1) Research
        ↓
ResearchBundle + ResearchBundleManifest
        ↓
LearnerProfile + PublicationTarget
        ↓
Core (2) Publisher
```

The central rule is:

> **Research once per evidence version; reuse many; publish many.**

Learner Bxx is not part of `ResearchBundle` identity. A learner/publication change therefore does not require a new ResearchBundle. A truth, scope, evidence or supported exam-demand change does.

## Frozen v1 contracts

| Contract | Owner | Purpose |
|---|---|---|
| `common.schema.json` | shared | IDs, digests and frozen enums |
| `project-manifest.schema.json` | intake/router | project routing and Core state |
| `scope-graph.schema.json` | Core (1) | project selection of canonical concepts plus research candidates |
| `learner-profile.schema.json` | intake/student state | Bxx by subtopic, basis and confidence |
| `publication-target.schema.json` | intake/Core (2) | learner/purpose/products requested from one frozen research package |
| `research-claim.schema.json` | Core (1) | verified material claims with source lineage |
| `representation-requirement.schema.json` | Core (1) | semantic figure/representation obligations; no geometry ownership |
| `source-ledger.schema.json` | Core (1)/source authority | provenance, verification and structured rights/use state |
| `exam-demand-profile.schema.json` | Core (1) | versioned competitive-exam demand derived from evidence |
| `question-evidence-ledger.schema.json` | corpus authority/Core (1) | frozen external-question denominator and per-row disposition |
| `research-bundle.schema.json` | Core (1) | canonical machine hand-off; excludes learner Bxx |
| `research-bundle-manifest.schema.json` | Core (1) release | external artifact hashes, semantic/package digests and change class |
| `core1-research-gap.schema.json` | Core (2) → Core (1) | fail-back for missing research/evidence |

## Executable gates

The v1 contract family is checked by:

```text
validate_contracts.py
validate_handoff.py
```

`validate_contracts.py` checks Draft 2020-12 schema validity, example fixtures and frozen architecture invariants.

`validate_handoff.py` checks cross-object closure that JSON Schema alone cannot prove, including:

```text
ResearchBundle ↔ ResearchBundleManifest identity/version binding
PublicationTarget ↔ ResearchPackage digest binding
PublicationTarget ↔ LearnerProfile binding
ResearchClaim ↔ SourceLedger closure
Representation/equation/worked-reasoning ↔ ResearchClaim closure
ResearchBundle source/exam/question artifact refs ↔ manifest artifact binding
Research Core MD/PDF material-view reconciliation
QuestionEvidence candidate denominator and REVIEW closure
competitive PublicationTarget ↔ ExamDemand support
```

## Joint CI evidence

GitHub Actions run `34447311075` completed successfully with:

```text
CONTRACT_SCHEMA_FREEZE_V1 = PASS (13 schemas)
BXX_OUTSIDE_RESEARCH_BUNDLE = PASS
MANIFEST_NO_SELF_HASH = PASS
CHANGE_CLASS_ENUM = PASS
RIGHTS_USE_ENUM = PASS
QUESTION_DISPOSITION_ENUM = PASS
CORE1_CORE2_HANDOFF_V1 = PASS
BUNDLE_MANIFEST_BINDING = PASS
LEARNER_TARGET_BINDING = PASS
MATERIAL_VIEW_RECONCILIATION = PASS
RESEARCH_REFERENCE_CLOSURE = PASS
QUESTION_DENOMINATOR_CLOSURE = PASS
COMPETITIVE_EXAM_DEMAND_BINDING = PASS
```

This is a contract/interface PASS. It does **not** establish source truth, learner pedagogy, renderer breadth, classroom effectiveness or psychometric calibration.

## Normative identity and hashing rules

`ResearchBundle` MUST NOT contain its own hash.

Canonical JSON serialization for semantic hashing is **RFC 8785 JSON Canonicalization Scheme (JCS)**. The `semantic_digest` in `ResearchBundleManifest` is SHA-256 over the canonicalized `ResearchBundle` bytes.

The `package_digest` is SHA-256 over the canonicalized ordered list of release artifact tuples:

```text
(role, path, sha256)
```

sorted lexicographically by `role`, then `path`. The manifest itself is not included in that list, avoiding self-reference.

The manifest separately binds each released artifact including Research Core Markdown/PDF, Source Ledger, ExamDemand/QuestionEvidence when applicable, and approved assets.

`PublicationTarget` binds Core (2) to the released package through:

```text
research_package_digest
```

which MUST equal:

```text
ResearchBundleManifest.package_digest
```

Do not introduce a manifest self-hash or restore the superseded `research_bundle_manifest_digest` wording.

## Canonical knowledge vs project scope

A project does not own the global ontology. `ScopeGraph` references canonical registry IDs and registry versions. New or changed concepts remain `RESEARCH_CANDIDATE` until:

```text
RESEARCH_CANDIDATE
→ SUBJECT_AUTHORITY_REVIEW
→ CANONICAL_PROMOTION
→ new canonical registry version
```

A ResearchBundle may reference a candidate only while explicitly marked as non-canonical/project-local.

## Bxx and learner privacy

`LearnerProfile` owns Bxx. `ResearchBundle` does not.

Core (1) may receive Bxx as an intake/research-priority hint, but the ResearchBundle schema does not contain a baseline field and its semantic digest cannot change merely because Bxx changes.

Shared/public research storage must not contain personally identifying learner state. LearnerProfile has an explicit privacy classification.

## Core (1) review surfaces

`Research_Core.md` and `Research_Core.pdf` are derived review surfaces, not parallel authorities. They must be generated from or reconciled against the ResearchBundle semantic model.

Release gates enforce:

```text
BUNDLE_TO_MD_MATERIAL_COVERAGE = 100%
BUNDLE_TO_PDF_MATERIAL_COVERAGE = 100%
UNMAPPED_MD_MATERIAL_CLAIMS = 0
UNMAPPED_PDF_MATERIAL_CLAIMS = 0
```

Material traceability applies to claims, conditions, worked examples, representations, questions, solution methods and exam facts. Connective/layout prose does not require artificial research claim IDs.

## Appendix and representation alignment with Core (2)

The cross-subject publication invariant is:

```text
Appendix A — Core Practice
Appendix B — Core Solutions
Appendix C — Printable Handout
```

`first_step_reference` is a handout module/profile, not the Appendix C identity.

The cross-subject rendering subsystem is named **Shared Representation Layer**. Core (1) emits `RepresentationRequirement`; Core (2) selects a compliant renderer/asset route and owns geometry, placement and render QA.

## Change classes and invalidation

Frozen v1 `change_class` values are:

```text
EDITORIAL
EVIDENCE
SEMANTIC
SCOPE
EXAM_DEMAND
ASSET
```

Expected downstream effect:

| Change class | Default Core (2) action |
|---|---|
| EDITORIAL | metadata/view revalidation; semantic rebuild normally unnecessary |
| EVIDENCE | provenance/traceability revalidation |
| ASSET | affected representation rerender/revalidation |
| SEMANTIC | rebuild affected learner objects |
| SCOPE | scope reconciliation; usually broad/full rebuild |
| EXAM_DEMAND | rebuild/revalidate competitive products; routine products may remain valid if unaffected |

Core (2) remains fail-closed when impact cannot be determined.

## External-question closure

The canonical corpus-coverage authority freezes the candidate denominator. `QuestionEvidenceLedger` records that result; it is not a second denominator engine.

Every candidate row receives exactly one disposition:

```text
REQUIRED | DEFER | EXCLUDE | REVIEW | DUPLICATE
```

`REVIEW` blocks closeout. `DUPLICATE` requires a canonical duplicate link. `EXCLUDE` and `DEFER` require a reason. Every non-duplicate row has one primary owner.

The executable hand-off validator additionally requires `candidate_denominator == len(rows)` and reconciles the optional summary to row dispositions.

## Source rights/use

Discovery/evidence validity is separate from reproduction permission. Frozen rights states are:

```text
REPRODUCTION_ALLOWED
REFERENCE_ONLY
USER_SUPPLIED_LIMITED
DISCOVERY_ONLY
UNKNOWN_REVIEW_REQUIRED
```

A mirror, index or secondary repository may be useful for discovery while remaining unusable for reproduced learner content.

## Original-question provenance

Do not use `ORIGINAL_CALIBRATED` without an explicit calibration basis. Preferred authored-item provenance is:

```text
ORIGINAL_EXAM_ALIGNED
ORIGINAL_EDITORIAL_PROFILED
```

Calibration, if claimed, must record one of:

```text
SOURCE_MAPPING
EXPERT_REVIEW
EMPIRICAL
```

## Freeze discipline

The v1 hand-off is now jointly frozen across PR #160 and PR #161.

Until a new contract version is approved:

- do not migrate stable skill IDs broadly before cold-start replay;
- do not make topic-specific schemas the new platform authority;
- do not put learner Bxx back into ResearchBundle;
- do not add hidden Core (2) web research paths;
- do not fork external-corpus denominator semantics;
- do not rename or repurpose frozen fields/enums in place.

A breaking interface change requires a new contract version directory (`v2/`) unless the user explicitly reopens the pre-implementation v1 freeze.

## Next implementation gate

Proceed in this order:

```text
1. Core (1) package generation
2. Core (2) hand-off validation
3. cold-start Laws of Motion replay
4. cold-start Redox replay
5. only then broad skill/router migration
```
