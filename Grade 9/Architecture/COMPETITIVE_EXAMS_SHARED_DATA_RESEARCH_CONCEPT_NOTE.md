# Competitive Exams, Shared Data and Web-Research Architecture

**Concept note for review**  
**Scope:** Grades 9–11 learning platform, with initial emphasis on Mathematics, Physics and Chemistry  
**Status:** DRAFT / FOR REVIEW  
**Date:** 2026-09-10

> **Normative architecture note:** This document supplies the shared-data/exam/web-research layer. The current two-core ownership model is defined by [`UNIFIED_TWO_CORE_ARCHITECTURE.md`](UNIFIED_TWO_CORE_ARCHITECTURE.md), [`CORE1_RESEARCH_CONCEPT_NOTE.md`](CORE1_RESEARCH_CONCEPT_NOTE.md), and Core (2) draft PR #161. Where older wording here conflicts, those documents take precedence.

---

## 1. Core model

The shared platform model is:

> **Canonical knowledge × Exam demand × Student state**

with a strict storage/ownership split:

```text
SHARED CANONICAL REGISTRY
concepts · methods · representations · misconceptions
questions · sources · exam identities · curricula
            │
            ├───────────────┐
            │               │
            ▼               ▼
     PROJECT SCOPE      LEARNER STATE
      / evidence            Bxx
            │               │
            ▼               │
      CORE (1) RESEARCH     │
            │               │
      Research Bundle       │
            │               │
            └───────┬───────┘
                    ▼
              CORE (2) PUBLISH
```

Learner Bxx is not stored in the canonical Research Bundle. It is a downstream `LearnerProfile` input.

---

## 2. Exam identity and versioning

Never use ambiguous display names as canonical IDs.

Examples:

```text
HBCSE_IOQM
HBCSE_RMO
HBCSE_INMO
INTERNATIONAL_IMO
SOF_IMO_L1
SOF_IMO_L2
SOF_NSO_L1_2025_26
SOF_ISO_L1_2026_27
```

Separate persistent exam family from yearly cycle:

```yaml
exam_family_id: SOF_SCIENCE_OLYMPIAD
aliases:
  - name: SOF_NSO
    valid_until: 2025-26
  - name: SOF_ISO
    valid_from: 2026-27
```

Cycle-specific data is versioned and freshness-gated.

---

## 3. Knowledge is stored once

Do not create separate knowledge bases for school, IOQM, SOF IMO, RMO, Physics olympiad/foundation, Chemistry olympiad/foundation, etc.

Use one canonical knowledge graph:

```text
DOMAIN
  ↓
CONCEPT
  ↓
MICRO-CONCEPT
  ↓
METHOD / STRATEGY
  ↓
QUESTION FAMILY
  ↓
QUESTION CONTENT
  ↓
EXAM OCCURRENCE
```

Parallel links include prerequisites, representations, misconceptions, model/law, experimental skills and proof/response contracts.

Cross-grade depth is represented through profiles rather than duplicate concepts.

---

## 4. ExamDemand as overlay

Competitive exams map onto canonical knowledge through `ExamDemand` records.

Example:

```yaml
exam_demand_id: HBCSE-RMO-NUMBER-THEORY-D4
exam_id: HBCSE_RMO
concept_ids:
  - MATH-NT-CONGRUENCE
  - MATH-NT-DIOPHANTINE
required_capabilities:
  recognition: 4
  model_selection: 4
  synthesis: 4
  proof_construction: 5
  proof_completeness: 5
response_format:
  type: WRITTEN_PROOF
question_families:
  - NT-DIOPH-LINEAR
  - NT-CONG-CRT
```

Different exam stages may require different response contracts over the same mathematics.

---

## 5. Curriculum profiles are overlays too

Curriculum/year maps canonical concepts into statuses such as:

```text
INCLUDED
EXCLUDED_THIS_CYCLE
PRACTICAL_ONLY
FORMATIVE
SUMMATIVE
OPTIONAL_ENRICHMENT
```

Curriculum profiles do not redefine canonical concept identity.

---

## 6. Shared question identity

Separate:

```text
QuestionContent      intellectual question
QuestionOccurrence   where/when it appeared
QuestionFamily       underlying recognition/method family
QuestionAdaptation   derived learner-facing version
```

The same question may have multiple source occurrences without duplicating the intellectual content object.

Adaptations preserve lineage and never masquerade as source occurrences.

---

## 7. External-question denominator

The shared corpus-coverage authority freezes the candidate denominator. Project Core (1) records the result in `Question_Evidence_Ledger.json`.

Each candidate row carries:

```text
REQUIRED | DEFER | EXCLUDE | REVIEW | DUPLICATE
primary owner
source/transcription/answer state
QuestionContent / QuestionFamily links
publication target
reason or duplicate link
```

`REVIEW` blocks closeout. Subject-specific auditors extend the generic contract rather than replacing it.

---

## 8. Source and research persistence

Shared source records contain:

```text
provider
URL/repo path
retrieved_at
content hash
authority level
verification state
rights/use state
```

Rights/use is structured, for example:

```text
REPRODUCTION_ALLOWED
REFERENCE_ONLY
USER_SUPPLIED_LIMITED
DISCOVERY_ONLY
UNKNOWN_REVIEW_REQUIRED
```

A source may be valid discovery/evidence without permission for reproduction.

---

## 9. Controlled web research

The agent searches only when:

```text
required evidence is missing
stored evidence is stale
exam/curriculum cycle may have changed
source/question provenance is unresolved
user explicitly asks for current/external information
```

Source hierarchy:

```text
1 official organizer/board
2 official syllabus/brochure/archive
3 official paper/solution
4 user-supplied source
5 verified/authorized provider
6 reputable secondary source
7 discovery/community source
```

Invariant:

> **Search → verify → fingerprint → deduplicate → map → store → reuse.**

And operationally:

> **Research once per evidence version → reuse many → refresh on stale or changed authority.**

---

## 10. Research run ledger

Every research run should record:

```yaml
research_run_id: RR-...
intent:
  exam_id: ...
  cycle: ...
  topic_ids: [...]
queries: [...]
results:
  - source_id: ...
    accepted: true
    authority: OFFICIAL
    extracted_entity_ids: [...]
  - source_id: ...
    accepted: false
    rejection_reason: OFFICIAL_SOURCE_AVAILABLE
```

Later agents reuse accepted entities/snapshots instead of searching again.

---

## 11. Freshness policy

Different data has different refresh requirements:

```text
canonical theorem/concept        persistent/versioned
past exam question              immutable after verification
source snapshot/hash            immutable
exam eligibility/date/pattern   cycle-fresh
syllabus                         cycle/annual refresh
community recommendation        short freshness
student mastery/Bxx              operational/private state
```

Freshness prevents cached exam evidence from becoming unintended permanent truth.

---

## 12. Student state privacy boundary

Student data remains separate from shared curriculum/research assets.

Shared/global:

```text
concepts
questions
sources
exam profiles
question families
representations
```

Private learner overlay:

```text
Bxx / mastery estimates
attempt history
hint dependency
time budget
target exam/date
```

LearnerProfile must not be committed into shared/public canonical research data unless explicitly anonymized/authorized.

---

## 13. Deduplication layers

Use multiple levels:

```text
exact source/file hash
normalized text fingerprint
question-content fingerprint
semantic near-duplicate candidate
```

Semantic similarity flags `POSSIBLE_VARIANT`; it does not auto-merge mathematically distinct problems.

---

## 14. Original question provenance

Do not call original authored questions `CALIBRATED` without a stated basis.

Prefer:

```text
ORIGINAL_EXAM_ALIGNED
ORIGINAL_EDITORIAL_PROFILED
```

Calibration, when claimed, is separate evidence:

```yaml
calibration:
  basis: SOURCE_MAPPING | EXPERT_REVIEW | EMPIRICAL
  evidence_refs: [...]
```

---

## 15. Project research package vs shared canonical data

A project Research Bundle references shared canonical IDs and freezes project-specific evidence/scope. It must not clone or silently redefine the global ontology.

If project research discovers a new concept/relationship:

```text
RESEARCH_CANDIDATE
→ SUBJECT AUTHORITY REVIEW
→ CANONICAL PROMOTION
→ new registry version
```

---

## 16. Core (1) / Core (2) integration

Core (1) owns:

```text
ScopeGraph
source/evidence verification
research claims
semantic representation requirements
exam-demand profile
question evidence closure
```

Core (2) receives:

```text
ResearchBundle
ResearchBundleManifest
LearnerProfile
PublicationTarget
PublicationProfile
```

Core (2) must return `CORE1_RESEARCH_GAP` instead of silently browsing to fill missing mathematical/scientific content.

---

## 17. Shared Representation Layer

Use the cross-subject term **Shared Representation Layer**.

It supports Math, Physics and Chemistry representation types while leaving semantics in Core (1) and rendering/composition in Core (2).

---

## 18. Success criteria

```text
ONE_CANONICAL_CONCEPT_PER_IDEA = PASS
PROJECT_SCOPE_DOES_NOT_MUTATE_CANONICAL_REGISTRY = PASS
QUESTION_CONTENT_DEDUP = PASS
SOURCE_OCCURRENCES_PRESERVED = PASS
ADAPTATION_LINEAGE = PASS
QUESTION_FAMILY_DIVERSITY_TRACKED = PASS
EXAM_DEMAND_SEPARATE_FROM_LEARNER_BASELINE = PASS
LEARNER_PROFILE_OUTSIDE_RESEARCH_BUNDLE = PASS
STUDENT_STATE_PRIVATE = PASS
WEB_RESEARCH_FRESHNESS_GATED = PASS
OFFICIAL_SOURCE_PRIORITY = PASS
SOURCE_RIGHTS_STATUS_RESOLVED = PASS
RESEARCH_RESULTS_REUSABLE = PASS
NO_REPEATED_UNNECESSARY_SEARCH = PASS
COLD_START_AGENT_CAN_REUSE_DATA = PASS
```

---

## 19. Central invariant

> **Knowledge is governed once. Source/question evidence is stored once with provenance and rights/use status. Core (1) freezes a version-scoped project evidence package; learner state remains separate. Exams, curricula and students are overlays expressed through stable links. Web research fills missing or stale evidence and is then stored for reuse rather than becoming an unmanaged second knowledge base.**