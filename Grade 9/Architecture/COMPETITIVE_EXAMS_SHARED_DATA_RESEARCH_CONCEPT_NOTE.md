# Competitive Exams, Shared Data and Web-Research Architecture

**Concept note for review**  
**Scope:** Grades 9–11 learning platform, with initial emphasis on Mathematics, Physics and Chemistry  
**Status:** DRAFT / FOR REVIEW  
**Date:** 2026-09-10

> **Operational addendum:** The default study-material workflow proposed in this concept now uses two separate outputs: **(1) Research Core** and **(2) Publish Core**. The detailed handoff, Bxx intake, repository-first research, competitive-exam reverse engineering, Appendix A–C publication contract, and independent-agent replay requirements are defined in [`TWO_CORE_RESEARCH_PUBLISH_OPERATING_CONTRACT.md`](TWO_CORE_RESEARCH_PUBLISH_OPERATING_CONTRACT.md). This addendum is intended to refine—not replace—the canonical-knowledge / exam-demand / student-state architecture below.

---

## 1. Purpose

The Grade 9 repository is evolving from a collection of subject/publication skills into a reusable learning-production platform. The next architectural problem is broader than one chapter or one subject:

1. support different competitive examinations without duplicating the same knowledge;
2. support different student levels without creating separate copies of concepts/questions;
3. share source, concept, method, representation and question data across school and competitive products;
4. let an agent research current exam information and missing source evidence on the web;
5. store verified research so the same material is not repeatedly searched, copied and reclassified;
6. preserve exact provenance, versioning and exam-year history;
7. prevent exam-specific workflows from becoming parallel subject authorities.

This note proposes a common architecture based on:

> **Canonical knowledge × Exam demand × Student state**

The proposal is intentionally conceptual. It does **not** change existing skills or migrate data in this draft.

---

## 2. Design evidence and current exam examples

This architecture must support materially different exam contracts.

### 2.1 HBCSE mathematical Olympiad pathway

The official HBCSE mathematical Olympiad information for the 2025–26 cycle describes a staged pathway beginning with IOQM and continuing through RMO and INMO. RMO 2025 had six questions in three hours and required detailed proofs; INMO 2026 had six questions in 4.5 hours and also required detailed proofs. The official HBCSE pages and brochures are the appropriate authority for cycle-specific rules.

Official source:

- https://olympiads.hbcse.tifr.res.in/mathematical-olympiad-2025-2026/
- https://olympiads.hbcse.tifr.res.in/information-brochures/

Architectural implication: the same mathematical concept may be assessed under different **response contracts**. An IOQM-oriented task may prioritize rapid recognition/model selection, while RMO/INMO demand proof construction, logical completeness and written argument. These must be separate demand dimensions, not one generic `difficulty` label.

### 2.2 SOF International Mathematics Olympiad

SOF IMO is a different competition and must never share an ambiguous canonical identifier with the International Mathematical Olympiad. For Class 9, SOF currently publishes a one-hour, 50-question Level 1 structure with sections for reasoning, mathematical reasoning, everyday mathematics and an Achievers section. SOF also states that Level 1 questions use 60% current-class and 40% previous-class syllabus, while Level 2 uses current-class syllabus.

Official source:

- https://sofworld.org/imo/class-9/imo-syllabus/imo-syllabus-class-9

Architectural implication: use qualified IDs such as `SOF_IMO_L1`, not `IMO`.

### 2.3 SOF NSO → ISO naming transition

SOF announced that the National Science Olympiad (NSO) was renamed the International Science Olympiad (ISO) from the 2026–27 session.

Official sources:

- https://sofworld.org/iso
- https://sofworld.org/download/file/fid/73919

Architectural implication: historical records must retain the name valid for the occurrence year. Do not rewrite old `SOF_NSO` occurrences as `SOF_ISO`; instead connect both names to one exam family with date-bounded aliases.

### 2.4 Domain-completeness implication

A science olympiad can require a broader science domain than Physics + Chemistry alone. The exam registry must therefore declare all required domains and must return `PARTIAL_COVERAGE` when an installed subject authority does not cover one of them. The platform must never infer complete-exam readiness merely because two subject packs are strong.

---

## 3. Core principle: knowledge exists once

The system should not create separate knowledge bases for:

- school Grade 9 Mathematics;
- IOQM Grade 9 preparation;
- SOF IMO Grade 9 preparation;
- RMO preparation;
- INMO preparation;
- Physics school exams;
- Physics Olympiad/foundation practice;
- Chemistry school exams;
- Chemistry science olympiads.

Instead:

```text
                         CANONICAL KNOWLEDGE
                   concepts / methods / representations
                     prerequisites / misconceptions
                               │
                ┌──────────────┴──────────────┐
                │                             │
           EXAM DEMAND                  STUDENT STATE
         what is required?             what is known?
         how is it tested?             what is weak?
         response format?              what transfers?
         current cycle?                what support?
                │                             │
                └──────────────┬──────────────┘
                               ▼
                        LEARNING TARGET
                               │
                teaching / practice / test / review
                               │
                               ▼
                        ATTEMPT EVIDENCE
                               │
                               ▼
                       UPDATED STUDENT STATE
```

A concept is canonical. Exams, curricula and students are overlays.

---

## 4. Do not use one field called “level”

At least these dimensions must remain independent:

| Dimension | Example |
|---|---|
| school grade | Grade 9 |
| curriculum depth | introductory / intermediate / senior-secondary |
| exam family | HBCSE mathematical Olympiad |
| exam stage | IOQM / RMO / INMO |
| problem demand | recognition / representation / synthesis / proof |
| student mastery | unseen / partial / independent / robust-transfer |
| support state | H0 / H1 / H2 / H3 |
| response contract | integer / MCQ / numerical / proof / experiment |

Example:

```yaml
grade: 9
exam_id: HBCSE_IOQM
concept_id: MATH-NT-CONGRUENCE
student_mastery: PARTIAL
problem_demand_profile: IOQM_NT_D3
support_state: H2
```

This is meaningful. `level: hard` is not.

---

## 5. Canonical identity model

### 5.1 Exam identity

Use stable, qualified IDs:

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

Display names are aliases, never identity keys.

### 5.2 Exam families and cycles

Separate persistent family from yearly occurrence:

```yaml
exam_family_id: SOF_SCIENCE_OLYMPIAD
aliases:
  - name: SOF_NSO
    valid_until: 2025-26
  - name: SOF_ISO
    valid_from: 2026-27
```

Cycle data contains mutable/current facts:

```yaml
exam_cycle_id: SOF_ISO_2026_27
exam_family_id: SOF_SCIENCE_OLYMPIAD
academic_year: 2026-27
registration_window: ...
exam_dates: ...
pattern_version: ...
syllabus_version: ...
source_snapshot_ids: [...]
```

Past cycles become immutable after verification.

---

## 6. Canonical knowledge graph

The reusable knowledge graph should not be organized primarily by textbook chapter. It should contain stable scientific/mathematical concepts and their relationships.

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

Parallel links:

```text
PREREQUISITE
REPRESENTATION
MISCONCEPTION
MODEL / LAW
EXPERIMENTAL SKILL
```

### 6.1 Cross-grade depth

The same concept may have different required depths by grade/exam.

Example:

```text
NEWTON_SECOND_LAW
  Grade 9:
    qualitative force-acceleration relation
    F = ma
    simple free-body reasoning

  Grade 11:
    vector treatment
    constraints
    friction
    connected bodies
    circular-motion applications
```

Do not duplicate `NEWTON_SECOND_LAW` as disconnected Grade 9 and Grade 11 concepts. Add depth profiles.

---

## 7. ExamDemand: the core competitive-exam overlay

Each exam/stage maps onto the canonical graph through `ExamDemand` records.

Illustrative structure:

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

The same concept can have different demand profiles:

```text
CONGRUENCES
   ├── school Grade 9 enrichment
   ├── IOQM recognition/model selection
   ├── RMO proof construction
   └── INMO high-synthesis proof
```

---

## 8. Competitive-exam progression changes the response contract

Qualifying for a later stage must not simply increase numerical difficulty.

Example:

```text
IOQM
recognize → select model → compute/derive answer → verify efficiently

                 ↓ stage transition

RMO / INMO
recognize → construct argument → choose lemmas → justify cases
→ write proof → close logical gaps
```

The learner product, feedback rubric and mastery model must therefore be stage-aware.

For proof exams, assessment objects need fields such as:

```text
claim_identified
lemma_selection
logical_dependency
case_completeness
counterexample_control
proof_closure
notation_precision
```

For objective exams, fields may emphasize:

```text
recognition_latency
method_selection
calculation_efficiency
option_elimination
error_type
```

---

## 9. Curriculum profiles are overlays too

Curriculum/year should not be the canonical concept authority.

```yaml
curriculum_profile_id: CBSE-2026-27-G11-PHYSICS
board: CBSE
academic_year: 2026-27
grade: 11
subject: Physics
```

It maps canonical concepts into:

```text
INCLUDED
EXCLUDED_THIS_CYCLE
PRACTICAL_ONLY
FORMATIVE
SUMMATIVE
OPTIONAL_ENRICHMENT
```

This allows the same knowledge graph to serve CBSE, ICSE, state boards, foundation programs and competitive exams without rewriting concepts.

---

## 10. Shared data: separate content identity from source occurrence

This is essential for deduplication.

### 10.1 QuestionContent

The mathematical/scientific question as an intellectual object:

```yaml
question_content_id: QC-8F12...
stem_normalized_fingerprint: ...
primary_concept_id: ...
secondary_concept_ids: [...]
question_family_ids: [...]
method_family_ids: [...]
representation_dependencies: [...]
```

### 10.2 QuestionOccurrence

One appearance of that content in a source/exam:

```yaml
occurrence_id: QO-HBCSE-IOQM-2025-Q14
question_content_id: QC-8F12...
exam_cycle_id: HBCSE_IOQM_2025
question_number: 14
source_document_id: SRC-HBCSE-IOQM-2025
source_locator: ...
```

The same question mirrored by another website becomes another occurrence linked to the same content object.

This prevents multiple copies of the same intellectual question while preserving provenance.

---

## 11. Adaptation lineage

Never overwrite a source question when creating a scaffolded or simplified version.

```text
SOURCE QUESTION QC-001
   │
   ├── ADAPTATION A
   │     added H1/H2/H3 support
   │
   ├── ADAPTATION B
   │     changed numerical values
   │
   └── ORIGINAL VARIANT C
         same method family, new context
```

Suggested metadata:

```yaml
derived_from: QC-001
derivation_type: SCAFFOLDED_ADAPTATION
changes:
  - ADDED_HINTS
  - CHANGED_VALUES
source_claim: ADAPTED
```

Original source text remains immutable.

---

## 12. QuestionFamily: avoid false mastery from repeated variants

Competitive-exam preparation needs a level above individual questions.

Example:

```yaml
family_id: NT-PIGEON-RESIDUE-01
concept_ids:
  - MATH-COMB-PIGEONHOLE
  - MATH-NT-RESIDUES
recognition_signature:
  - more objects than residue classes
common_wrong_models:
  - brute-force all cases
  - confuse equality with congruence
first_move:
  - identify the finite residue classes
```

A student who solves six variants of one family has not demonstrated six independent areas of mastery.

Mastery should therefore be estimated across:

```text
concept diversity
method diversity
question-family diversity
representation diversity
transfer distance
support depth
```

---

## 13. Student state is a private overlay

Shared knowledge is global. Student evidence is private.

```text
SHARED KNOWLEDGE
      │
      ├── Student A mastery overlay
      ├── Student B mastery overlay
      └── Student C mastery overlay
```

Do not store student attempts/mastery in the public skills repository.

Illustrative student record:

```yaml
student_id: ...
grade: 9

targets:
  - exam_id: HBCSE_IOQM
    target_cycle: 2027

mastery:
  MATH-NT-DIVISIBILITY:
    recognition: 0.90
    execution: 0.82
    transfer: 0.54

  MATH-GEO-CYCLIC:
    recognition: 0.40
    execution: 0.20
    transfer: 0.05

behaviour:
  hint_dependency: MODERATE
  proof_completeness: WEAK
```

Marks are evidence, not the student model itself.

---

## 14. Recommended data stores

Do not place all operational data in GitHub JSON files.

| Store | Canonical responsibility |
|---|---|
| Git repository | schemas, skills, taxonomies, exam/curriculum profile definitions, versioned policy |
| relational database | concepts, edges, methods, questions, occurrences, source metadata, exam demands, student attempts/mastery |
| object/blob store | PDFs, scans, figures, source snapshots, rendered publications |
| search/vector index | retrieval acceleration and similarity discovery only |

The vector index must never become source authority.

A PostgreSQL/Supabase implementation is sufficient for the relational layer initially.

---

## 15. Core shared entities

Suggested logical entities:

```text
Concept
ConceptEdge
Representation
Method
Misconception
QuestionFamily
QuestionContent
QuestionOccurrence
QuestionAdaptation
SourceDocument
SourceSnapshot

CurriculumProfile
ExamFamily
ExamCycle
ExamStage
ExamDemand

StudentProfile
StudentMastery
StudentAttempt

WebSource
ResearchRun
ResearchResult
ResearchDecision
```

Relationships are mostly many-to-many and should use stable IDs rather than rendered page numbers.

---

## 16. Web research should be a controlled subsystem

The agent should not search the web every time a user mentions an exam.

Decision flow:

```text
USER REQUEST
      ↓
CHECK VERIFIED INTERNAL DATA
      ↓
Is required data present and fresh?
      │
  ┌───┴─────┐
 YES        NO
  │          │
  │       WEB RESEARCH
  │          ↓
  │     SOURCE VERIFY
  │          ↓
  │    DEDUP / INGEST
  │          ↓
  └───────── REUSE
```

### 16.1 Search triggers

Search only when one or more are true:

1. exam/cycle information is missing;
2. stored syllabus/pattern/eligibility is stale for the requested cycle;
3. user explicitly requests latest/current information;
4. a required source question remains unresolved;
5. the frozen corpus has a documented evidence gap;
6. the organizer/exam naming or pattern may have changed;
7. the user requests an external resource not present in the verified store.

Otherwise reuse verified internal data.

---

## 17. Research intent should be explicit before search

Do not issue broad queries such as `IOQM questions` without a structured need.

```yaml
research_intent:
  exam_id: HBCSE_IOQM
  cycle: 2026-27
  student_grade: 9
  need: PRACTICE_CORPUS
  concepts:
    - MATH-GEO-CYCLIC
    - MATH-GEO-ANGLE_CHASE
  problem_demand:
    min: D2
    max: D4
  provenance_required:
    - OFFICIAL
  existing_question_ids:
    - ...
```

The search planner then looks specifically for missing evidence rather than re-downloading the entire exam ecosystem.

---

## 18. Source authority hierarchy

For exam facts and source-grounded questions, use a deterministic source hierarchy:

```text
1. official exam organizer
2. official syllabus / brochure / archive
3. official past paper / official solution
4. government / board source
5. verified publisher or authorized provider
6. reputable secondary explanation
7. community discussion
```

A community post may inform learner sentiment or common mistakes. It must not establish current exam eligibility, dates, syllabus or official marking rules when an official source is available.

---

## 19. Research ledger: search once, verify, store, reuse

Every accepted web research run should leave durable evidence.

```yaml
research_run_id: RR-2026-09-10-0042
intent:
  exam_id: HBCSE_IOQM
  cycle: 2026-27
  need: EXAM_PATTERN

queries:
  - ...

results:
  - source_url: ...
    authority: OFFICIAL
    retrieved_at: ...
    content_sha256: ...
    accepted: true
    extracted_entity_ids:
      - EXAM-PATTERN-IOQM-2026

  - source_url: ...
    authority: SECONDARY
    accepted: false
    rejection_reason: OFFICIAL_SOURCE_AVAILABLE
```

The next agent first checks this ledger and freshness policy before searching again.

---

## 20. Freshness policy

Different data ages differently.

| Data type | Freshness / immutability rule |
|---|---|
| canonical concept | persistent, versioned only when conceptual model changes |
| prerequisite graph | persistent/versioned |
| verified past exam occurrence | immutable after source verification |
| source PDF hash | immutable |
| exam eligibility | refresh each cycle |
| exam dates | refresh each cycle and near registration/exam windows |
| exam name/branding | refresh each cycle |
| syllabus | refresh annually/cycle-wise |
| pattern/marking | refresh annually/cycle-wise |
| registration window | short freshness |
| community recommendations | short freshness |
| student mastery | updated after attempts/evidence |

Research should be triggered by expiry policy, not by habit.

---

## 21. Deduplication model

Deduplicate at several layers.

### Exact source duplicate

```text
SHA-256
```

### Normalized textual duplicate

```text
normalized stem/options/answer fingerprint
```

### Question-content duplicate

```text
stem + options + answer + representation fingerprint
```

### Semantic near-duplicate

```text
concept IDs + method family + question family + representation + semantic similarity
```

Semantic near-duplicates should be flagged as `POSSIBLE_VARIANT`, not automatically merged. Two Olympiad problems may look similar but differ in the decisive idea.

---

## 22. Competitive learning planner

The planner computes:

```text
EXAM DEMAND
   MINUS
DEMONSTRATED STUDENT CAPABILITY
   =
LEARNING DEFICIT
```

Then orders the deficit by prerequisites and transfer requirements.

Example student:

```text
Grade 9
Target: IOQM
16 weeks
Strong algebra
Weak geometry
Can solve after seeing the first step
```

Planner response should be based on:

```text
missing prerequisites
→ concept repair
→ first-step recognition
→ method families
→ question-family diversity
→ independent mixed sets
→ exam-format simulation
```

It must not simply serve random exam questions.

---

## 23. Product routing by exam and student state

The same canonical concept can generate different products.

```text
PARTIAL MASTERY + H2 DEPENDENCY
→ concept explanation
→ first-step reference
→ guided/faded practice

ROBUST SCHOOL MASTERY + IOQM TARGET
→ recognition drills
→ method-choice contrasts
→ timed integer-answer mixed sets

IOQM QUALIFIED + RMO TARGET
→ proof construction
→ lemma selection
→ case completeness
→ written proof critique
```

Exam profile controls the task contract; student state controls the scaffolding.

---

## 24. Representation registry must be shared

Competitive exams frequently change difficulty through representation rather than concept.

Create a shared representation registry rather than hard-coding representation semantics inside every exam workflow.

Examples:

```yaml
PHYSICS_FREE_BODY:
  subject: Physics
  semantic_checks:
    - body_declared
    - force_source_declared
    - direction_valid

PHYSICS_RAY_DIAGRAM:
  subject: Physics
  semantic_checks:
    - optical_axis
    - focal_points
    - ray_rules

CHEM_LEWIS_STRUCTURE:
  subject: Chemistry
  semantic_checks:
    - valence_electrons
    - formal_charge
    - octet_exception_handling

MATH_PROOF_DEPENDENCY_GRAPH:
  subject: Mathematics
  semantic_checks:
    - assumptions_explicit
    - implication_direction
    - case_closure
```

Exam-specific difficulty then references representation demand rather than creating a new renderer per exam.

---

## 25. Subject coverage must be explicit

An exam profile declares all required domains:

```yaml
exam_id: SOF_ISO_L1
required_domains:
  - logical_reasoning
  - physics
  - chemistry
  - biology
  - environmental_science
```

If only Physics and Chemistry are present:

```text
EXAM_COVERAGE = PARTIAL
MISSING_DOMAINS = BIOLOGY, LOGICAL_REASONING, ...
```

The platform must never infer complete-exam readiness from partial subject support.

---

## 26. Proposed repository organization

Keep skills and runtime data separate.

```text
Grade 9/
│
├── shared/
│   ├── ontology/
│   │   ├── concepts/
│   │   ├── methods/
│   │   ├── representations/
│   │   ├── misconceptions/
│   │   └── question-families/
│   │
│   ├── curricula/
│   │   ├── cbse/
│   │   └── ...
│   │
│   ├── exams/
│   │   ├── exam-registry.yaml
│   │   ├── hbcse/
│   │   ├── sof/
│   │   └── international/
│   │
│   ├── schemas/
│   └── vocabularies/
│
├── skills/
│   └── reusable behavior contracts
│
└── Architecture/
    └── concept notes / ADRs
```

Operational student/source/question data should live in a database/object store rather than the public repository.

---

## 27. Interaction with the Grade 9 skill architecture

The recommended ownership boundaries are:

```text
SUBJECT AUTHORITY
  Math / Physics / Chemistry
       │
       ├── owns subject correctness
       │
EXAM PROFILE
       ├── owns current exam demand/format overlays
       │
STUDENT MODEL
       ├── owns private mastery/attempt state
       │
QUESTION / ENRICHMENT SERVICES
       ├── create/adapt learning objects
       │
CORPUS / SOURCE AUDIT
       ├── proves source and external-question accounting
       │
PUBLICATION
       └── renders validated products
```

An exam workflow must not redefine Mathematics/Physics/Chemistry truth.

A subject skill must not hard-code current exam dates/patterns.

A publication skill must not become student-memory authority.

---

## 28. Generic corpus authority should remain subject-agnostic

Long-term architecture should be:

```text
GRADE9 CORPUS COVERAGE AUTHORITY
          │
     ┌────┼────┐
     ▼    ▼    ▼
   Math Physics Chemistry
   profile profile profile
```

Subject profiles may add representation, notation or solution checks but should not copy the denominator/ownership/reconciliation engine.

This is especially important once IOQM, SOF IMO, SOF ISO and other external corpora coexist.

---

## 29. Shared topic-product pair

Physics and Chemistry are already converging toward a common learner product pattern. Before further expansion, define a subject-neutral base contract such as:

```text
CORE_LEARNING_PRODUCT
+
TRANSFER_PRACTICE_PRODUCT
```

Then extend it:

```text
Physics:
  graphs / vectors / model validity

Chemistry:
  macro-particle-symbolic / notation / conservation

Mathematics:
  proof / construction / invariants / counterexamples
```

The shared base should own identity, reciprocal linkage, topic scope, concept authority and common attempt/hint/solution semantics.

---

## 30. Agent research workflow

Proposed agent sequence:

```text
USER
 │
 ▼
REQUEST INTERPRETER
 │
 ├── grade?
 ├── subject?
 ├── exam family/stage?
 ├── target cycle/date?
 ├── student state?
 └── requested product?
 │
 ▼
EXAM REGISTRY
 │
 ▼
CURRICULUM + CANONICAL CONCEPT GRAPH
 │
 ▼
STUDENT STATE
 │
 ▼
GAP ANALYSER
 │
 ├── internal verified data sufficient/fresh? ─────┐
 │                                                 │
 └── missing/stale → RESEARCH AGENT                │
                      │                            │
                      ▼                            │
                SOURCE VERIFIER                    │
                      │                            │
                DEDUP / INGEST                     │
                      └────────────────────────────┘
                              │
                              ▼
                       LEARNING PLANNER
                              │
                    ┌─────────┼─────────┐
                    ▼         ▼         ▼
                  TEACH     PRACTICE    TEST
                    │         │         │
                    └─────────┼─────────┘
                              ▼
                       ATTEMPT EVIDENCE
                              │
                              ▼
                     STUDENT STATE UPDATE
```

---

## 31. Search/ingest invariant

Lock this as an architecture rule:

> **Search → verify → fingerprint → deduplicate → map → store → reuse.**

Never:

```text
search → answer → forget → search again
```

Every accepted web source should be reusable by another agent without relying on prior chat history.

---

## 32. Privacy boundary

Student state is sensitive operational data and must be separated from public curriculum/source assets.

Minimum requirements:

- private student identifiers;
- no public Git commits containing student attempt history;
- least-privilege access;
- separate shared-content and student-state tables;
- explicit retention policy;
- aggregate analytics should avoid exposing individual students;
- research/source records must never contain student-specific prompts unless needed and authorized.

This concept note does not define a full privacy/security implementation; that requires a separate design review.

---

## 33. Failure modes the architecture must prevent

1. `IMO` ambiguity mixes SOF IMO with International IMO.
2. current-year exam rules overwrite historical occurrences.
3. one source question is stored independently 5–10 times from mirrors.
4. an adapted question loses its source lineage.
5. a student receives repeated variants of one question family and is marked mastered.
6. a subject skill embeds stale exam dates/syllabi.
7. the web agent searches the same official page on every request.
8. secondary websites override an available official source.
9. semantic near-duplicates are automatically merged even when the decisive method differs.
10. vector search results become treated as canonical truth.
11. student mastery is committed into the public repository.
12. a two-subject implementation claims full science-olympiad coverage.
13. RMO/INMO preparation is treated as merely “harder IOQM”.
14. exam difficulty and learner support level are conflated.
15. publication page numbers become canonical concept/question identity.

---

## 34. Minimum viable implementation

### Phase 1 — shared IDs and registries

- define `exam-registry.yaml`;
- define `curriculum-profile` schema;
- define canonical exam/cycle/stage IDs;
- define `ExamDemand` schema;
- define freshness policy vocabulary;
- define source-authority vocabulary;
- define `QuestionContent` vs `QuestionOccurrence`.

No student personalization is required in this phase.

### Phase 2 — shared question/source store

- relational tables for sources, snapshots, question content, occurrences and lineage;
- exact and normalized dedup;
- source/research ledger;
- corpus ingestion from one official exam family;
- source-to-question-to-concept reconciliation.

### Phase 3 — student state

- mastery dimensions;
- attempt evidence;
- support/hint dependency;
- question-family diversity;
- planner query: `exam demand − demonstrated mastery`.

### Phase 4 — controlled web research

- research-intent object;
- freshness checks;
- official-source routing;
- accepted/rejected result records;
- dedup before ingestion;
- research cache reuse.

### Phase 5 — cross-exam planner

Pilot at least:

- HBCSE IOQM;
- HBCSE RMO;
- SOF IMO Level 1;
- SOF science olympiad current-cycle profile;
- school curriculum profile.

The pilot should prove that one concept/question/source graph can serve multiple exam products without duplication.

---

## 35. Recommended falsifier pilots

Do not scale by adding many exams immediately. Use deliberately different contracts.

| Pilot | What it falsifies/tests |
|---|---|
| IOQM | objective/integer-answer mathematical selection and speed |
| RMO | proof construction and written reasoning |
| SOF IMO Level 1 | class-specific objective + reasoning + previous-class overlap |
| SOF science olympiad | multi-domain science dependency and yearly naming/pattern versioning |
| Grade 9 school curriculum | curriculum overlay without competitive-exam assumptions |

Success means one shared knowledge layer survives all five without exam-specific duplication.

---

## 36. Success criteria

The architecture is ready for broader implementation when all of the following can be demonstrated:

```text
ONE_CANONICAL_CONCEPT_PER_IDEA = PASS
EXAM_IDS_UNAMBIGUOUS = PASS
HISTORICAL_EXAM_NAMES_PRESERVED = PASS
QUESTION_CONTENT_DEDUP = PASS
SOURCE_OCCURRENCES_PRESERVED = PASS
ADAPTATION_LINEAGE = PASS
QUESTION_FAMILY_DIVERSITY_TRACKED = PASS
EXAM_DEMAND_SEPARATE_FROM_STUDENT_SUPPORT = PASS
STUDENT_STATE_PRIVATE = PASS
WEB_RESEARCH_FRESHNESS_GATED = PASS
OFFICIAL_SOURCE_PRIORITY = PASS
RESEARCH_RESULTS_REUSABLE = PASS
NO_REPEATED_UNNECESSARY_SEARCH = PASS
PARTIAL_DOMAIN_COVERAGE_REPORTED_HONESTLY = PASS
COLD_START_AGENT_CAN_REUSE_DATA = PASS
```

A cold-start agent should be able to answer:

1. What exam/cycle/stage is being targeted?
2. Which official source establishes the current pattern/syllabus?
3. Which canonical concepts are demanded?
4. Which demand dimensions apply?
5. Which of those capabilities has the student demonstrated?
6. Which verified questions already exist in the shared store?
7. Which question families are underrepresented?
8. Is web research necessary, and why?
9. If research is performed, what new verified entity was stored?
10. Can another agent reuse the result without searching again?

---

## 37. Explicit non-goals for this draft

This concept note does not yet propose:

- a final database vendor/schema migration;
- a complete privacy/security threat model;
- scraping arbitrary websites at scale;
- automatic ingestion of copyrighted question banks without source/licensing review;
- psychometric claims about student ability;
- automatic semantic dedup without human-review escape paths;
- a new skill for every competitive examination;
- a replacement for existing subject authorities;
- a claim that current Physics/Chemistry coverage alone constitutes complete science-olympiad preparation.

---

## 38. Approval decisions requested

| ID | Decision | Recommendation |
|---|---|---|
| A1 | Adopt `Canonical knowledge × Exam demand × Student state` as the core model | APPROVE |
| A2 | Use stable qualified exam IDs and versioned exam cycles | APPROVE |
| A3 | Separate `QuestionContent` from `QuestionOccurrence` | APPROVE |
| A4 | Add `QuestionFamily` above individual questions | APPROVE |
| A5 | Store adaptations through explicit lineage instead of copying source questions | APPROVE |
| A6 | Treat curriculum and exam requirements as overlays, not concept authorities | APPROVE |
| A7 | Keep student state private and outside the public skills repository | APPROVE |
| A8 | Introduce a controlled web-research subsystem with freshness gates | APPROVE |
| A9 | Persist accepted/rejected research evidence in a reusable research ledger | APPROVE |
| A10 | Use official-source-first authority hierarchy | APPROVE |
| A11 | Keep vector/search indexes non-canonical | APPROVE |
| A12 | Build shared representation and product-pair base contracts before adding many exam-specific workflows | APPROVE |
| A13 | Pilot IOQM + RMO + SOF IMO + SOF science olympiad + school profile before broader expansion | APPROVE |
| A14 | Adopt the separate Research Core → Publish Core operating contract in the linked addendum | APPROVE |

---

## 39. Recommended approval statement

> Approved in principle to develop a shared Grades 9–11 learning architecture in which canonical concepts, methods, representations, questions and sources are stored once; curricula and competitive examinations are versioned demand overlays; student mastery is a private evidence overlay; and web research is invoked only for missing/stale evidence, with verified findings fingerprinted, deduplicated, stored and reused. Study-material generation should use the linked two-core operating contract so source/research truth is frozen independently before learner adaptation and publication. Implementation should begin with shared IDs/schemas and a deliberately diverse exam pilot before any large-scale migration or new exam-specific skill proliferation.

---

## 40. Central invariant

> **Knowledge is stored once. Sources are stored once. Question content is stored once. Exams, curricula and students are overlays expressed through stable links. Web research fills missing or stale evidence; it must not create an unmanaged second knowledge base. Research Core freezes that evidence; Publish Core adapts it for the learner without redefining it.**