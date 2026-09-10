# Core (2) Publisher — v1 Contract Alignment Addendum

**Status:** JOINT V1 CONTRACT FREEZE — implementation pending  
**Normative schema source:** PR #160 `Grade 9/Architecture/contracts/v1/`  
**Applies to:** `CORE2_PUBLISHER_CONCEPT_NOTE.md`  
**Validated by:** `validate_contracts.py` + `validate_handoff.py` in PR #160  

Where the earlier Core (2) concept note conflicts with this addendum, this addendum controls for the v1 hand-off.

## 1. Core (2) canonical input

Core (2) receives the frozen research package plus two downstream targeting inputs:

```text
ResearchBundle + ResearchBundleManifest
LearnerProfile
PublicationTarget
```

Learner Bxx is **not** part of ResearchBundle identity.

Core (2) therefore implements:

```text
CORE2 = ResearchPackage × LearnerProfile × PublicationTarget
```

Changing Bxx or publication purpose normally rebuilds Core (2) only. Changing truth, scope, evidence or supported exam demand versions Core (1).

## 2. Frozen upstream package

Core (1) release contains:

```text
<Topic>_Research_Bundle.json
<Topic>_Research_Bundle_Manifest.json
<Topic>_Research_Core.md
<Topic>_Research_Core.pdf
<Topic>_Source_Ledger.json
<Topic>_Exam_Demand_Profile.json          # when applicable
<Topic>_Question_Evidence_Ledger.json     # when applicable
approved assets                           # when applicable
```

`ResearchBundle` does not hash itself. `ResearchBundleManifest` binds the released artifacts and contains:

```text
research_bundle_id
evidence_version
change_class
semantic_digest
package_digest
artifact hashes
material-view reconciliation
```

Core (2) validates the manifest/package binding before publication.

## 3. PublicationTarget package binding

The frozen v1 field is:

```text
research_package_digest
```

It MUST equal:

```text
ResearchBundleManifest.package_digest
```

Do not use the earlier `research_bundle_manifest_digest` wording. The manifest intentionally does not self-hash; the publication target binds to the released research package digest instead.

## 4. Change-class aware invalidation

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

If impact cannot be safely localized, fail closed and require broader revalidation.

## 5. Scope and canonical-registry boundary

Core (2) consumes project scope from `ScopeGraph` and stable canonical IDs. It must not promote project research candidates into global canonical knowledge.

Promotion remains outside Core (2):

```text
RESEARCH_CANDIDATE
→ SUBJECT_AUTHORITY_REVIEW
→ CANONICAL_PROMOTION
```

## 6. LearnerProfile

Bxx belongs to `LearnerProfile`, with per-subtopic:

```text
value 0–100
basis
confidence
evidence refs when applicable
```

Core (2) applies Bxx to scaffolding, exposition density, prerequisite repair, worked-example depth and transfer timing. It must not reinterpret Bxx as exam difficulty, intelligence or psychometric mastery.

## 7. PublicationTarget

`PublicationTarget` binds:

```text
ResearchBundle ID
ResearchPackage digest
LearnerProfile ID
purpose
exam/curriculum target when applicable
requested Study Guide / Transfer Book
publication profile
```

A competitive publication request is valid only when the requested exam demand is supported by the ResearchBundle/ExamDemand evidence. Otherwise return `CORE1_RESEARCH_GAP`.

The v1 schema also requires at least one learner product and requires an exam profile for competitive/foundation/mock purposes.

## 8. Appendix semantics

Freeze the shared Study Guide semantics as:

```text
Appendix A — Core Practice
Appendix B — Core Solutions
Appendix C — Printable Handout
```

`first_step_reference` is a module/profile inside Appendix C, not the identity of Appendix C itself.

Subject profiles may require different handout modules, for example:

```text
Mathematics: first moves / invariants / decision router
Physics: first moves / models / diagram cues / equation conditions
Chemistry: process cues / representation links / conditions / common traps
```

## 9. Shared Representation Layer

Rename the cross-subject rendering subsystem from **Scientific Representation Core** to **Shared Representation Layer**.

Core (1) owns `RepresentationRequirement` semantics:

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

The layer must support Mathematics as well as Physics/Chemistry, including proof/construction/graph/case structures where implemented.

## 10. Material traceability

100% research linkage applies to material semantic objects:

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

Core (2)'s release gate measures material-object traceability, not sentence-level citation density.

## 11. External-question closure

Core (2) consumes the frozen `QuestionEvidenceLedger`; it does not re-own corpus denominator mechanics.

Per-row dispositions are:

```text
REQUIRED | DEFER | EXCLUDE | REVIEW | DUPLICATE
```

Core (2) may publish only rows authorized for its publication target. `REVIEW` remains blocking. Source/transcription/answer state and one primary owner remain upstream evidence obligations.

The executable v1 hand-off validator also checks that the candidate denominator equals the frozen row count and that an optional ledger summary reconciles to row dispositions.

## 12. Original-question provenance

Replace unconditional `ORIGINAL_CALIBRATED` terminology with:

```text
ORIGINAL_EXAM_ALIGNED
ORIGINAL_EDITORIAL_PROFILED
```

unless an explicit calibration basis is present:

```text
SOURCE_MAPPING
EXPERT_REVIEW
EMPIRICAL
```

Core (2) may display difficulty/editorial labels only with provenance preserved.

## 13. Rights/use enforcement

Source evidence validity does not imply reproduction permission.

Core (2) consumes structured rights states:

```text
REPRODUCTION_ALLOWED
REFERENCE_ONLY
USER_SUPPLIED_LIMITED
DISCOVERY_ONLY
UNKNOWN_REVIEW_REQUIRED
```

The publisher must refuse learner-facing reproduction when the relevant source/asset rights state does not permit it. It may still use permitted factual/structural evidence according to the recorded rights contract.

## 14. Core (1) gap protocol

Core (2) continues to return:

```text
CORE1_RESEARCH_GAP
```

using the frozen `core1-research-gap.schema.json` contract when required evidence/semantics/rights are missing.

Core (2) must not silently browse, invent or locally patch material truth.

## 15. Cold-start acceptance

A clean Core (2) agent receives only:

```text
ResearchBundle
ResearchBundleManifest
Source/ExamDemand/QuestionEvidence artifacts referenced by the manifest
approved assets
LearnerProfile
PublicationTarget
canonical schemas/skills
```

and no prior chat/researcher state.

Required v1 hand-off outcomes:

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

## 16. Joint freeze evidence

The v1 schema family in PR #160 has been executed in GitHub Actions against Python 3.11 / `jsonschema` Draft 2020-12 validation.

The joint contract run passed:

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

This is a contract/interface PASS only. It does not establish pedagogy quality, source truth, classroom effectiveness, renderer coverage or psychometric calibration.

## 17. Cross-PR freeze rule

PR #161 must not fork its implementation schema independently of PR #160's v1 contract directory. Breaking interface changes require joint review and a new contract version directory (`v2/`) unless the user explicitly reopens the pre-implementation v1 freeze.
