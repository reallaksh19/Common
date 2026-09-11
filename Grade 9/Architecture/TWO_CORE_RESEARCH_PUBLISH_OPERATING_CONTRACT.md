# Two-Core Research → Publish Operating Contract

**Status:** Adopted for architecture design; implementation pending  
**Unified architecture:** [`UNIFIED_TWO_CORE_ARCHITECTURE.md`](UNIFIED_TWO_CORE_ARCHITECTURE.md)  
**Core (1):** [`CORE1_RESEARCH_CONCEPT_NOTE.md`](CORE1_RESEARCH_CONCEPT_NOTE.md)  
**Core (2):** [Draft PR #161](https://github.com/reallaksh19/Common/pull/161)

This is the concise operating contract. Where older concept drafts differ, the Unified Architecture + Core (1) note + aligned PR #161 interface take precedence.

---

## 1. Operating invariant

> **Research once per evidence version → reuse many → publish many → refresh when evidence/authority changes.**

Default flow:

```text
PROMPT / SOURCES
      ↓
INTAKE PARSE
      ↓
REPOSITORY DISCOVERY
      ↓
CONDITIONAL EXAM / WEB RESEARCH
      ↓
PROPOSE / CONFIRM TOPIC + SUBTOPIC MAP
      ↓
ASK / CONFIRM Bxx + PURPOSE
      ↓
FREEZE PROJECT SCOPE GRAPH
      ↓
CORE (1) RESEARCH
      ↓
RESEARCH BUNDLE + MANIFEST
      ↓
                 LearnerProfile + PublicationTarget
                              ↓
CORE (2) PUBLISH — PR #161
      ↓
STUDY GUIDE / OPTIONAL TRANSFER BOOK
```

---

## 2. Core boundary

> **Core (1) owns project scope, source/evidence verification, research claims, semantic representation requirements and exam-demand interpretation. Core (2) owns learner adaptation, rendering, scaffolding, composition and publication QA.**

Global concept identity belongs to the shared canonical registry, not to a project Core (1).

---

## 3. Intake and Bxx

Ask only for missing information:

```text
grade
subject
topic / subtopics
Bxx by subtopic
purpose
exam/stage/cycle when applicable
user-supplied sources
```

`Bxx` is estimated prior working knowledge. Store it in a separate `LearnerProfile` with provenance/confidence.

```yaml
baseline:
  PHY-NLM-FBD:
    band: B30
    basis: USER_DECLARED
    confidence: MEDIUM
```

Bxx may inform Core (1) research priority, but it does **not** enter Research Bundle identity/hash.

---

## 4. Competitive vs generic routing

### Competitive

```text
repo discovery
→ resolve exam identity/cycle
→ inspect fresh verified samples/PYQs
→ research missing demand evidence
→ reverse engineer mechanisms/question families
→ propose subtopics
→ confirm Bxx/purpose
→ freeze ScopeGraph
→ Core (1)
```

### Generic/routine

```text
repo discovery
→ propose/confirm subtopics
→ confirm Bxx + purpose
→ use supplied/curriculum authority
→ research missing/stale evidence only
→ freeze ScopeGraph
→ Core (1)
```

A mock must be driven by an evidence-grounded exam blueprint, not generic difficulty.

---

## 5. Canonical registry vs ScopeGraph

Core (1) references canonical concepts through `ScopeGraph`.

If research discovers a new/changed concept:

```text
RESEARCH_CANDIDATE
→ SUBJECT AUTHORITY REVIEW
→ CANONICAL REGISTRY VERSION
```

Core (1) must not silently mutate the shared ontology.

---

## 6. Repository-first and web research

Before network research Core (1) checks:

```text
prior Research Bundles
canonical concepts
source snapshots/ledgers
question content/occurrences/families
exam profiles/cycles
representation definitions
misconceptions
audits/review records
```

Only missing/stale evidence is searched.

> **Search → verify → fingerprint → deduplicate → map → store → reuse.**

Core (2) does not normally browse for mathematical/scientific content.

---

## 7. Core (1) outputs

Mandatory:

```text
<Topic>_Research_Bundle.json
<Topic>_Research_Bundle_Manifest.json
<Topic>_Research_Core.md
<Topic>_Research_Core.pdf
<Topic>_Source_Ledger.json
```

Competitive/external-question additions:

```text
<Topic>_Exam_Demand_Profile.json
<Topic>_Question_Evidence_Ledger.json
```

`Research_Bundle.json` is the canonical semantic machine hand-off. MD/PDF are derived human review surfaces. The manifest binds hashes/version/change class.

---

## 8. Versioning and hashing

Do not hash the bundle into itself.

`Research_Bundle_Manifest.json` stores:

```text
bundle_id
version
change_class
artifact hashes
semantic_digest
package_digest
```

Allowed primary change classes:

```text
EDITORIAL
EVIDENCE
SEMANTIC
SCOPE
EXAM_DEMAND
ASSET
```

Core (2) uses the class for selective revalidation/rebuild; unknown impact fails closed.

---

## 9. Core (1) human-view zero drift

Required generation/reconciliation direction:

```text
ResearchBundle
→ Research Core view model
→ Markdown + PDF
```

Required material coverage:

```text
BUNDLE_TO_MD_MATERIAL_COVERAGE = 100%
BUNDLE_TO_PDF_MATERIAL_COVERAGE = 100%
UNMAPPED_MD_MATERIAL_CLAIMS = 0
UNMAPPED_PDF_MATERIAL_CLAIMS = 0
```

---

## 10. External-question closure

`Question_Evidence_Ledger.json` freezes the result of the canonical corpus-coverage service.

Each candidate occurrence must have:

```text
REQUIRED | DEFER | EXCLUDE | REVIEW | DUPLICATE
primary owner
source/transcription/answer states
QuestionContent / QuestionFamily links
publication target
reason/duplicate link where applicable
```

`REVIEW` blocks closeout. Subject-specific auditors extend the generic denominator mechanics; they do not redefine them.

---

## 11. Source rights/use

Source records must distinguish evidence availability from reproduction rights using structured status such as:

```text
REPRODUCTION_ALLOWED
REFERENCE_ONLY
USER_SUPPLIED_LIMITED
DISCOVERY_ONLY
UNKNOWN_REVIEW_REQUIRED
```

This applies especially to mirrors, indexes, ExamSIDE/Scribd-style discovery and third-party archives.

---

## 12. Core (2) canonical input

Core (2) receives:

```text
ResearchBundle
+ ResearchBundleManifest
+ LearnerProfile
+ PublicationTarget
+ PublicationProfile
```

If the target asks for exam demand not supported by Core (1), Core (2) returns `CORE1_RESEARCH_GAP`.

---

## 13. Core (2) output contract

Aligned shared Study Guide base:

```text
MAIN LEARNING SECTION

Appendix A — Core Practice
Appendix B — Core Solutions
Appendix C — Printable Handout
```

`first_step_reference` is a module inside Appendix C when required by subject/purpose; it is not the Appendix identity itself.

Hints remain support mechanics:

```text
H0 independent
H1 recognition/notice
H2 structure/model
H3 first executable step
```

Competitive/external work may additionally produce a Transfer Book.

---

## 14. Shared Representation Layer

Use the cross-subject name **Shared Representation Layer**, not “Scientific Representation Core”.

Core (1) specifies semantic obligations. The shared layer provides typed representation/rendering capabilities for Math, Physics and Chemistry. Core (2) selects, places and audits them.

Unsupported required representation semantics fail closed.

---

## 15. Material traceability

Traceability applies to semantic/material objects, not connective prose.

Material classes include:

```text
MATERIAL_CLAIM
MATERIAL_CONDITION
MATERIAL_EXAMPLE
MATERIAL_REPRESENTATION
MATERIAL_QUESTION
MATERIAL_SOLUTION_METHOD
MATERIAL_EXAM_FACT
```

Every material Core (2) object must resolve to Core (1) IDs and source/question evidence where applicable.

---

## 16. Gap protocol

Core (2) must not silently repair missing research.

```yaml
status: CORE1_RESEARCH_GAP
research_bundle_id: ...
gap_type: SOURCE | CONCEPT | REPRESENTATION | EQUATION | QUESTION_FAMILY | EXAM_DEMAND | ASSET
object_id: ...
blocking: true
reason: ...
```

Core (1) resolves, versions, remanifests and re-hands off.

---

## 17. Original-question claims

Default authored mock/practice status should be:

```text
ORIGINAL_EXAM_ALIGNED
ORIGINAL_EDITORIAL_PROFILED
```

Use a “calibrated” claim only when a calibration basis is explicitly recorded:

```text
SOURCE_MAPPING
EXPERT_REVIEW
EMPIRICAL
```

---

## 18. Cold-start acceptance

A clean Core (2) agent must be able to publish using only the released Core (1) package plus LearnerProfile/PublicationTarget and canonical schemas/skills.

Required:

```text
CORE1_COLD_START_SUFFICIENT = PASS
PUBLISH_AGENT_NO_HIDDEN_CONTEXT = PASS
PUBLISH_AGENT_UNDECLARED_WEB_SEARCHES = 0
MATERIAL_TRACEABILITY_COVERAGE = 100%
BLOCKING_UNRESOLVED_ITEMS = 0
```

---

## 19. Central contract

> **Shared canonical knowledge is governed once. Core (1) freezes a project ScopeGraph and evidence package for one evidence version. Learner Bxx is downstream state, not Research Bundle truth. Core (2) combines the Research Bundle with LearnerProfile and PublicationTarget, and no agent may silently create a second ontology, corpus or research authority.**