# Core (2) Publisher — v1 Frozen Upstream Interface

**Status:** JOINT V1 CONTRACT FREEZE — Core (2) implementation pending  
**Normative schema source:** PR #160 `Grade 9/Architecture/contracts/v1/`  
**Core (2) architecture:** `CORE2_PUBLISHER_CONCEPT_NOTE.md`  
**Validated upstream by:** `validate_contracts.py` + `validate_handoff.py` in PR #160

This file records the frozen Core (1) → Core (2) interface. The main Core (2) concept note has been normalized to this interface; this document is no longer an override for stale terminology.

---

## 1. Canonical Core (2) input

```text
ResearchBundle + ResearchBundleManifest
+ referenced Source / ExamDemand / QuestionEvidence artifacts
+ approved assets when applicable
+ LearnerProfile
+ PublicationTarget
```

Equivalent formulation:

```text
CORE2 = ResearchPackage × LearnerProfile × PublicationTarget
```

Learner Bxx is not part of ResearchBundle identity.

---

## 2. Frozen package binding

Core (1) release contains, as applicable:

```text
<Topic>_Research_Bundle.json
<Topic>_Research_Bundle_Manifest.json
<Topic>_Research_Core.md
<Topic>_Research_Core.pdf
<Topic>_Source_Ledger.json
<Topic>_Exam_Demand_Profile.json
<Topic>_Question_Evidence_Ledger.json
approved assets
```

`ResearchBundleManifest` carries:

```text
research_bundle_id
evidence_version
change_class
semantic_digest
package_digest
artifact hashes
material-view reconciliation
```

The frozen `PublicationTarget` field is:

```text
research_package_digest
```

and it MUST equal:

```text
ResearchBundleManifest.package_digest
```

The manifest does not self-hash.

---

## 3. LearnerProfile and PublicationTarget

`LearnerProfile` owns per-subtopic baseline:

```text
value 0–100
basis
confidence
evidence refs when applicable
```

`PublicationTarget` owns:

```text
ResearchBundle ID
ResearchPackage digest
LearnerProfile ID
purpose
exam/curriculum target when applicable
requested Study Guide / Transfer Book
publication profile
```

Changing Bxx or ordinary publication purpose normally rebuilds Core (2) only.

---

## 4. Scope and canonical knowledge boundary

Core (2) consumes `ScopeGraph` and stable canonical IDs.

It does not promote project research candidates. Promotion remains upstream:

```text
RESEARCH_CANDIDATE
→ SUBJECT_AUTHORITY_REVIEW
→ CANONICAL_PROMOTION_APPROVED
```

---

## 5. Change-class handling

Core (2) recognizes:

```text
EDITORIAL
EVIDENCE
SEMANTIC
SCOPE
EXAM_DEMAND
ASSET
```

Default behavior:

```text
EDITORIAL    → metadata/view revalidation
EVIDENCE     → provenance/traceability revalidation
ASSET        → affected representation rerender/revalidation
SEMANTIC     → rebuild affected learner objects
SCOPE        → scope reconciliation; broad/full rebuild by default
EXAM_DEMAND  → rebuild/revalidate competitive products
```

If impact cannot be localized safely, fail closed.

---

## 6. Appendix semantics

Frozen shared Study Guide semantics:

```text
Appendix A — Core Practice
Appendix B — Core Solutions
Appendix C — Printable Handout
```

`first_step_reference` is a module/profile inside Appendix C.

---

## 7. Shared Representation Layer

The cross-subject rendering subsystem is named:

> **Shared Representation Layer**

Core (1) `RepresentationRequirement` owns semantic obligations:

```text
what must be shown
relationships
required labels
conditions
approved assets
research refs
```

Core (2) owns:

```text
renderer selection
geometry
layout
asset placement
legibility
grayscale behavior
render QA
```

An upstream representation type does not imply renderer support. Unsupported required representations fail closed.

---

## 8. Material traceability

100% research linkage applies to:

```text
MATERIAL_CLAIM
MATERIAL_CONDITION
MATERIAL_EXAMPLE
MATERIAL_REPRESENTATION
MATERIAL_QUESTION
MATERIAL_SOLUTION_METHOD
MATERIAL_EXAM_FACT
```

It does not require artificial claim IDs for:

```text
PEDAGOGICAL_CONNECTIVE
PRESENTATION_ONLY
```

Core (2) measures material-object traceability, not sentence-level citation density.

---

## 9. Core (2) publisher readiness gate

The upstream hand-off validator establishes contract closure. Core (2) adds a publication-readiness gate.

Before learner-content planning:

```text
RESEARCH_BUNDLE_STATUS = READY_FOR_PUBLISH
BLOCKING_UNRESOLVED_ITEMS = 0
MATERIAL_RESEARCH_CLAIMS_VERIFIED = PASS
RESEARCH_PACKAGE_DIGEST_BINDING = PASS
LEARNER_TARGET_BINDING = PASS
```

For v1, a material Research Claim must be `VERIFIED` before Core (2) can publish it as settled learner content.

This rule is intentionally publisher-side: a schema-valid or research-in-progress bundle is not automatically publishable.

---

## 10. External-question closure

Core (2) consumes the frozen `QuestionEvidenceLedger`; it does not re-own corpus-denominator mechanics.

Dispositions:

```text
REQUIRED | DEFER | EXCLUDE | REVIEW | DUPLICATE
```

`REVIEW` remains blocking. Core (2) publishes only records authorized for its target and preserves source/transcription/answer/primary-owner state.

---

## 11. Original-question provenance

Default original-question states are:

```text
ORIGINAL_EXAM_ALIGNED
ORIGINAL_EDITORIAL_PROFILED
```

A stronger calibration claim requires an explicit basis such as:

```text
SOURCE_MAPPING
EXPERT_REVIEW
EMPIRICAL
```

---

## 12. Rights/use enforcement

Core (2) consumes:

```text
REPRODUCTION_ALLOWED
REFERENCE_ONLY
USER_SUPPLIED_LIMITED
DISCOVERY_ONLY
UNKNOWN_REVIEW_REQUIRED
```

Source validity does not imply reproduction permission. Learner-facing reproduction must comply with the recorded rights contract.

---

## 13. Gap protocol

Missing material truth, representation semantics, exam evidence, asset evidence or rights returns:

```text
CORE1_RESEARCH_GAP
```

using PR #160's frozen `core1-research-gap.schema.json`.

Core (2) does not silently browse, invent or locally patch material truth.

---

## 14. Cold-start acceptance

A clean Publisher receives only the frozen research package, `LearnerProfile`, `PublicationTarget` and canonical schemas/skills.

Required hand-off outcomes include:

```text
HANDOFF_SCHEMA_VALID = PASS
RESEARCH_PACKAGE_DIGEST_BINDING = PASS
BUNDLE_MANIFEST_BINDING = PASS
LEARNER_TARGET_BINDING = PASS
MATERIAL_VIEW_RECONCILIATION = PASS
RESEARCH_REFERENCE_CLOSURE = PASS
QUESTION_DENOMINATOR_CLOSURE = PASS | NOT_APPLICABLE
COMPETITIVE_EXAM_DEMAND_BINDING = PASS | NOT_APPLICABLE
BLOCKING_RESEARCH_GAPS = 0
UNDECLARED_CORE2_RESEARCH = 0
```

Core (2) then applies its additional publisher readiness gate from §9.

---

## 15. Joint freeze evidence

PR #160's v1 schema family has been executed in GitHub Actions using Python 3.11 and JSON Schema Draft 2020-12 validation.

Recorded joint run:

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

GitHub Actions run: `34447311075`.

This establishes interface/contract closure only. It does not establish pedagogy quality, source truth, renderer breadth, classroom effectiveness or psychometric calibration.

---

## 16. Upstream freeze vs downstream implementation

The frozen PR #160 objects are **upstream hand-off contracts**.

Core (2) should next define its own downstream objects:

```text
PublicationPlan
StudyGuidePublicationModel
TransferBookPublicationModel
RepresentationInstance
Badge
PublicationAudit
PublicationManifest
```

These may evolve inside Core (2) without altering PR #160 v1, provided the frozen input contract is preserved.

Breaking changes to the Core (1) → Core (2) interface require joint review and a new `v2/` contract unless the user explicitly reopens v1.