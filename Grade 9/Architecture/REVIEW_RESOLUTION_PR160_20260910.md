# PR #160 Architecture Review Resolution — 2026-09-10

**Review incorporated:** Math/Core (1) architecture review at head `6e39d5b`  
**Status:** accepted into concept architecture; implementation remains pending

---

## Resolution summary

The review supports the two-core direction and identifies ownership/identity issues that must be resolved before schema implementation. The architecture has been revised accordingly.

| Review issue | Resolution |
|---|---|
| Bxx/student baseline inside Research Bundle | **ACCEPTED.** Bxx moves to separate `LearnerProfile`; Core (1) may see it only as a research-priority hint. It does not affect Research Bundle identity/hash. |
| Project research vs global canonical ontology | **ACCEPTED.** Add project `ScopeGraph`; Core (1) references canonical IDs and uses `RESEARCH_CANDIDATE → SUBJECT REVIEW → CANONICAL PROMOTION` for ontology changes. |
| Self-referential bundle hash | **ACCEPTED.** Add external `Research_Bundle_Manifest.json` with canonical semantic digest, package digest and per-artifact hashes. |
| MD/PDF as parallel authorities | **ACCEPTED.** Research Core MD/PDF become derived/reconciled views of the semantic bundle with 100% material-coverage gates. |
| Appendix C slash ambiguity | **ACCEPTED.** Freeze `Appendix C — Printable Handout`; `first_step_reference` becomes a profile/module inside the handout. |
| “Scientific Representation Core” naming | **ACCEPTED.** Rename cross-subject subsystem to `Shared Representation Layer`. |
| “Research once” too absolute | **ACCEPTED.** Use `research once per evidence version → reuse many → refresh on stale/changed authority`. |
| External-question denominator closure | **ACCEPTED.** `QuestionEvidenceLedger` freezes canonical corpus-auditor output with `REQUIRED | DEFER | EXCLUDE | REVIEW | DUPLICATE`, one primary owner and source/transcription/answer states. |
| `ORIGINAL_CALIBRATED` overclaim | **ACCEPTED.** Default to `ORIGINAL_EXAM_ALIGNED` / `ORIGINAL_EDITORIAL_PROFILED`; stronger calibration requires explicit basis/evidence. |
| Literal sentence-level traceability | **ACCEPTED.** Add material traceability classes; 100% applies to claims, conditions, examples, representations, questions, solution methods and exam facts, not connective prose/layout. |
| Change impact/invalidation | **ACCEPTED.** Add `change_class`: `EDITORIAL`, `EVIDENCE`, `SEMANTIC`, `SCOPE`, `EXAM_DEMAND`, `ASSET`. |
| Rights/use status | **ACCEPTED.** Replace free-text-only use notes with structured rights statuses and allowed/prohibited uses. |

---

## Revised canonical flow

```text
SHARED CANONICAL REGISTRY
        ↓
PROJECT SCOPE GRAPH
        ↓
CORE (1) RESEARCH
        ↓
Research_Bundle.json
Research_Bundle_Manifest.json
        ↓
        ├────────────── LearnerProfile (Bxx)
        └────────────── PublicationTarget
                         ↓
                  CORE (2) PUBLISH
                         ↓
                  LEARNER PRODUCTS
```

`ResearchBundle` is reusable learner-neutrally. `LearnerProfile` is downstream state.

---

## Core (1) release package after review

```text
<Topic>_Research_Bundle.json
<Topic>_Research_Bundle_Manifest.json
<Topic>_Research_Core.md
<Topic>_Research_Core.pdf
<Topic>_Source_Ledger.json
<Topic>_Exam_Demand_Profile.json          # when applicable
<Topic>_Question_Evidence_Ledger.json     # when applicable
```

The manifest binds bundle identity/version/change class and released artifact hashes.

---

## Required alignment with PR #161

Before Core (2) implementation freeze, PR #161 should align its interface to these accepted decisions:

```text
ResearchBundle excludes learner Bxx
Core (2) receives LearnerProfile separately
Appendix C = Printable Handout
first_step_reference = handout module/profile
Scientific Representation Core → Shared Representation Layer
material traceability classes
bundle manifest/digest/change_class awareness
```

PR #161 remains the downstream Publisher architecture; these are interface refinements, not a change to its primary ownership.

---

## Implementation gate

Do not start large skill/schema migration until the following architecture contracts are frozen together:

```text
CanonicalRegistry references
ScopeGraph
LearnerProfile
PublicationTarget
ResearchBundle
ResearchBundleManifest
ResearchClaim
SourceLedger + rights/use
ExamDemandProfile
QuestionEvidenceLedger
RepresentationRequirement
Core1ResearchGap
TraceabilityClass
ChangeClass
```

The decisive acceptance test remains a cold-start Core (2) agent publishing from the released Core (1) package plus learner/publication inputs with no prior chat or hidden research state.