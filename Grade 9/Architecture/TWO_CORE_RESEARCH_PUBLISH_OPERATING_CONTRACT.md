# Two-Core Research → Publish Operating Contract

**Concept addendum for PR #160 review**  
**Scope:** study-material generation across Grades 9–11, initially Mathematics, Physics and Chemistry  
**Status:** DRAFT / FOR REVIEW  
**Date:** 2026-09-10

---

## 1. Decision proposed

For every in-scope **study-material generation request**, the platform should produce two deliberately separate cores:

```text
(1) RESEARCH CORE
    Research, source custody, concept architecture, exam-demand analysis,
    canonical teaching content, question-family analysis and evidence.

                ↓ frozen handoff

(2) PUBLISH CORE
    Student-level adaptation, exam/purpose adaptation, instructional sequencing,
    practice, hints/solutions, Appendix A–C and final learner publication.
```

The two cores are not two copies of the same book.

> **Core 1 establishes what is true, in scope, supported and worth teaching. Core 2 decides how that validated material should be taught to this student for this purpose.**

The central handoff requirement is:

> **An independent Publish agent with no prior chat history must be able to produce Core 2 from the frozen Core 1 package plus the explicit learner/purpose profile.**

No hidden conversational context may be required.

---

## 2. Why two cores

The current architecture correctly separates canonical knowledge, exam demand and student state. The operational workflow should now also separate two different jobs that otherwise drift into one another:

| Concern | Research Core | Publish Core |
|---|---|---|
| source truth | owns | consumes |
| web research | owns | normally prohibited |
| repository discovery | owns | consumes resolved references |
| exam reverse engineering | owns | consumes ExamDemand |
| topic/subtopic architecture | owns/finalizes | preserves |
| canonical explanation | owns | adapts |
| model/law/reaction correctness | owns with subject authority | may not redefine |
| question families / source samples | owns | selects/adapts within contract |
| learner baseline Bxx | records as targeting input | actively uses |
| scaffolding | notes constraints only | owns |
| page structure | not authoritative | owns |
| Appendix A–C | may specify obligations | renders |
| final PDF | research/reference PDF | learner publication PDF |
| citations/provenance | full evidence chain | references Research Core IDs and source evidence |

This prevents four recurring failure modes:

1. web research and learner simplification happening simultaneously;
2. student level changing what the source is claimed to say;
3. the publishing agent independently searching and creating a second source corpus;
4. later agents being unable to reproduce the material without the original chat.

---

## 3. Mandatory outputs

A normal study-material request emits two top-level output packages.

### 3.1 Core 1 — Research Core

Required deliverables:

```text
01_Research_Core.md
01_Research_Core.pdf
01_Research_Core.manifest.json
01_Research_Ledger.json
```

The Markdown/PDF are human-reviewable. The manifest/ledger are the machine handoff.

### 3.2 Core 2 — Publish Core

Required deliverables:

```text
02_Publish_Core.md
02_Publish_Core.pdf
02_Publish_Core.manifest.json
```

Additional internal QA/evidence files are allowed, but they do not count as extra learner “cores”.

The user may explicitly request `research-only` or `publish-from-existing-research-core`; otherwise both cores are the default for study-material production.

---

## 4. Intake contract: ask only what is missing

The agent first parses the prompt and supplied files/links. It should not ask for information already explicit in the request.

Minimum targeting fields:

```text
grade
subject
topic(s)
subtopic(s)
student baseline by topic/subtopic
purpose
```

Conditional fields:

```text
competitive exam / exam stage / cycle
mock vs study vs clarification vs revision
board/curriculum if relevant
user-supplied source authority
language / output constraints when material
```

### 4.1 Purpose vocabulary

Recommended initial values:

```text
ROUTINE_STUDY
CONCEPT_CLARIFICATION
COMPETITIVE_PREPARATION
EXAM_MOCK
REVISION
DIAGNOSTIC_REPAIR
```

A request may combine purposes, but one must be primary.

---

## 5. Bxx baseline model

Use `Bxx` only for **estimated prior student knowledge**, not exam difficulty.

Examples:

```text
B30 = limited prior knowledge / substantial rebuilding expected
B50 = partial knowledge / mixed independence
B80 = strong prior knowledge / compressed support and more transfer
```

Do not infer psychometric precision from the number. Store confidence and source:

```yaml
baseline:
  value: 80
  basis: USER_ESTIMATE
  confidence: MEDIUM
```

Recommended interpretation anchors:

| Baseline | Planning interpretation |
|---|---|
| B0–20 | little demonstrated prior knowledge |
| B21–40 | weak/fragmented knowledge |
| B41–60 | partial usable knowledge |
| B61–80 | strong knowledge with selected gaps |
| B81–100 | very strong prior knowledge; emphasize transfer/diagnosis |

These ranges guide scaffolding; they are not labels printed on the student as an ability judgement.

### 5.1 Topic-specific baseline matrix

Never require one Bxx for a whole chapter when knowledge is uneven.

The agent should propose/ask for a compact matrix such as:

```text
Grade 9 Physics — Laws of Motion

Subtopic                              Baseline
Newton's first law / inertia          B80
Newton's second law                   B65
free-body diagrams                    B30
friction                              B40
action-reaction pairs                 B55
```

The user may answer only the rows that differ; a declared chapter default can fill the rest.

### 5.2 Exam demand remains separate

Never encode:

```text
B80 = hard exam
```

Instead:

```yaml
student_baseline: B80
exam_demand: SOF_ISO_ACHIEVERS_D3
```

A B30 learner may target a hard exam; that changes the scaffold path, not the exam definition.

---

## 6. State machine

The default workflow is:

```text
PROMPT / SOURCES
      ↓
INTAKE PARSE
      ↓
REPOSITORY DISCOVERY
      ↓
CONDITIONAL EXAM / WEB RESEARCH
      ↓
PROPOSE TOPIC + SUBTOPIC MAP
      ↓
ASK / CONFIRM Bxx MATRIX + PURPOSE
      ↓
FREEZE RESEARCH BRIEF
      ↓
BUILD CORE 1 — RESEARCH CORE
      ↓
RESEARCH CORE QA / FREEZE
      ↓
HANDOFF PACKAGE
      ↓
BUILD CORE 2 — PUBLISH CORE
      ↓
STUDENT / EXAM ADAPTATION
      ↓
APPENDIX A–C + LINK/CITATION QA
      ↓
FINAL CORE 2 PDF
```

A competitive-exam request may perform a small amount of exam-demand discovery before Bxx confirmation so the agent can propose the correct subtopics. It should not perform a full corpus crawl before the user confirms scope.

---

## 7. Repository-first rule

Every material-generation request begins by checking the repository/shared store for existing reusable assets:

```text
concept IDs
subject authority
existing topic/subtopic maps
Research Core packs
source snapshots
exam profiles/cycles
question content and occurrences
question families
representation definitions
misconceptions
prior coverage audits
```

The repository lookup should answer:

```text
WHAT ALREADY EXISTS?
WHAT IS CURRENT?
WHAT CAN BE REUSED WITHOUT RESEARCH?
WHAT IS MISSING OR STALE?
```

Only the missing/stale portion becomes a web-research intent.

---

## 8. Competitive-exam branch: reverse engineer demand before teaching

For a request such as:

> Prepare Grade 9 Physics Laws of Motion for NSO/ISO or an ExamSIDE-style mock.

The Research agent should not simply take a school chapter and add harder questions.

It should build an **exam-demand evidence set** from the best available sources:

```text
repo-held verified past questions / exam profile
        ↓ if insufficient/stale
official exam organizer / official samples / official past papers
        ↓
verified provider/index when official evidence is insufficient
        ↓
user-supplied question PDFs / links / screenshots
        ↓
secondary samples only with provenance and limitations
```

Examples such as ExamSIDE or Scribd may be useful as discovery/secondary evidence when permitted and available, but they must not silently override official exam sources. Full copyrighted source content should not be copied into the repository unless supplied/authorized; store provenance, locators, fingerprints and only the evidence necessary for lawful verification.

### 8.1 Reverse-engineering dimensions

For each representative sample question, derive as applicable:

```text
primary concept
secondary/prerequisite concepts
question family
recognition trigger
hidden model choice
representation dependency
reasoning chain
calculation burden
common distractor/wrong model
response format
time-pressure characteristic
transfer distance
source difficulty, if explicitly supplied
editorial demand estimate, separately
```

Then aggregate into an `ExamDemand` view for the requested topic.

### 8.2 Official vs inferred demand

Keep two statuses separate:

```text
OFFICIAL_EXAM_REQUIREMENT
INFERRED_FROM_VERIFIED_SAMPLE
```

A pattern seen in ten past questions is evidence of recurring demand; it is not automatically an official syllabus statement.

---

## 9. Generic-topic branch

For a request such as:

> Prepare Grade 10 Chemistry on Redox.

The sequence is slightly different:

```text
repo discovery
→ identify existing canonical Redox concepts/source packs
→ propose topic/subtopic decomposition
→ ask user to confirm subtopics + Bxx matrix + purpose
→ incorporate supplied PDFs/links as source authority
→ research only missing/stale evidence
→ build Research Core
→ freeze
→ independent Publish Core
```

Routine/generic study should not trigger a broad competitive-exam crawl unless the user asks for one.

---

## 10. Web-search trigger matrix

The Research agent owns web research. Search should be purpose-aware.

| Purpose | Web behavior |
|---|---|
| ROUTINE_STUDY | repository/source first; web only for missing evidence, requested expansion or current curriculum facts |
| CONCEPT_CLARIFICATION | normally no web if verified canonical data is sufficient |
| COMPETITIVE_PREPARATION | verify current exam profile; inspect representative verified question evidence if not already fresh in store |
| EXAM_MOCK | require exam-demand evidence and question-family distribution before authoring the mock |
| REVISION | reuse existing Research Core where fresh; avoid research by default |
| DIAGNOSTIC_REPAIR | use student/topic evidence first; research only when a concept/source gap is detected |

The rule remains:

> **Search → verify → fingerprint → deduplicate → map → store → reuse.**

---

## 11. Research Core content contract

Core 1 is a **target-aware but not student-simplified** knowledge package.

It may know that the target is Grade 9 + SOF ISO + B30/B80 mix, because that affects scope and research priorities. But its scientific/mathematical claims are canonical and should not be rewritten differently for B30 vs B80.

Required sections/objects:

```text
R1. research brief and targeting metadata
R2. repository reuse report
R3. source inventory and source-authority hierarchy
R4. topic/subtopic scope map
R5. canonical concept map + prerequisites
R6. canonical explanations / laws / equations / reactions / model conditions
R7. representations required and semantic specifications
R8. misconceptions / wrong models / repair logic
R9. question families and representative evidence
R10. exam-demand analysis when applicable
R11. practical/experimental requirements when applicable
R12. unresolved gaps / exclusions / confidence
R13. source/evidence citations
R14. Publish-agent handoff instructions
```

### 11.1 Stable Research Core IDs

Every reusable research object receives a stable ID, for example:

```text
RC-SUB-LOM-01       subtopic
RC-CON-LOM-04       concept claim
RC-REP-FBD-01       representation specification
RC-MIS-AR-01        misconception
RC-QF-LOM-07        question family
RC-EXD-ISO-03       exam-demand finding
RC-SRC-0042         source snapshot/evidence
```

These IDs are the bridge to Core 2.

---

## 12. Research Core machine handoff

`01_Research_Core.manifest.json` should be sufficient for a cold-start Publish agent.

Illustrative structure:

```yaml
research_core_id: RC-G9-PHY-LOM-2026-001
status: READY_FOR_PUBLISH

target:
  grade: 9
  subject: Physics
  topic_ids:
    - PHY-LOM
  purpose: COMPETITIVE_PREPARATION
  exam_profile_id: SOF_ISO_G9_2026_27

student_baseline:
  PHY-LOM-NEWTON1: 80
  PHY-LOM-FBD: 30
  PHY-LOM-FRICTION: 40

canonical_concepts: [...]
subtopics: [...]
representations: [...]
misconceptions: [...]
question_families: [...]
exam_demand_ids: [...]
source_snapshot_ids: [...]
research_gaps: []

human_core_md: 01_Research_Core.md
human_core_pdf: 01_Research_Core.pdf
ledger: 01_Research_Ledger.json
```

The manifest is not a summary written after the fact. It is the frozen machine contract from which Publish operates.

---

## 13. Research Core readiness gate

The Research agent may emit:

```text
READY_FOR_PUBLISH
READY_WITH_NONBLOCKING_GAPS
BLOCKED_RESEARCH_GAP
```

`READY_WITH_NONBLOCKING_GAPS` is allowed only when every gap is explicitly outside the requested learning claims/products.

Before `READY_FOR_PUBLISH`:

```text
TOPIC_SCOPE_CONFIRMED = PASS
SUBTOPIC_SCOPE_CONFIRMED = PASS
BASELINE_MATRIX_RECORDED = PASS
PURPOSE_RECORDED = PASS
SOURCE_AUTHORITY_RESOLVED = PASS
CANONICAL_CONCEPTS_RESOLVED = PASS
REPRESENTATION_REQUIREMENTS_RESOLVED = PASS
EXAM_DEMAND_RESOLVED = PASS | NOT_APPLICABLE
QUESTION_FAMILY_EVIDENCE = PASS | NOT_APPLICABLE
RESEARCH_GAPS_BLOCKING = 0
CITATION_CHAIN_COMPLETE = PASS
```

---

## 14. Publish agent authority boundary

Agent 2 is an independent **transformation/publishing agent**, not a second researcher.

By default Agent 2 must not:

```text
search the web
replace source authority
change canonical concept claims
change exam-demand facts
invent missing source questions
silently add out-of-scope subtopics
alter source difficulty labels
```

Agent 2 may:

```text
change explanation order
choose student-facing wording
choose scaffolding depth
compress or expand worked reasoning
select examples from approved families
create clearly-labelled original practice
adapt visuals to baseline
apply exam-format practice
lay out Appendix A–C
```

If Agent 2 detects a factual/evidence gap, it emits a structured backfill request:

```yaml
status: RESEARCH_BACKFILL_REQUIRED
research_core_id: ...
gap_type: EXAM_DEMAND | SOURCE | CONCEPT | REPRESENTATION | QUESTION_FAMILY
object_id: ...
reason: ...
```

The fix returns to Research Core. Publish does not quietly research around the gap.

---

## 15. Publish Core content contract

Core 2 is the student-facing, purpose-specific transformation of Core 1.

Required main flow should be selected by subject and purpose, but the general structure is:

```text
ORIENT
→ CONNECT TO PRIOR KNOWLEDGE
→ REPRESENT / SEE
→ EXPLAIN / REALIZE
→ MODEL / RELATION / RULE
→ WORKED REASONING
→ MISCONCEPTION REPAIR
→ GUIDED PRACTICE
→ FADED PRACTICE
→ INDEPENDENT / EXAM TRANSFER
```

The student baseline changes the support profile:

```text
B30
  more prerequisite repair
  larger depictions
  explicit intermediate reasoning
  guided → faded → independent

B80
  compressed prerequisite repair
  decisive representation retained
  more model-choice contrast
  earlier transfer / mixed practice
```

The exam profile changes the task contract, not the science/mathematics truth.

---

## 16. Appendix A–C base contract

Unless a future subject profile has an approved alternative, Core 2 should use a shared base:

### Appendix A — Practice / Transfer

- independent and mixed questions;
- exam-style distribution when applicable;
- no solution leakage;
- stable question IDs;
- question-family diversity rather than repeated numerical variants.

### Appendix B — Hints and Solutions

- optional progressive hints when appropriate;
- complete solutions after the attempt boundary;
- WHY / METHOD / ANSWER / CHECK or subject-specific equivalent;
- necessary diagrams/tables/data repeated where a standalone solution requires them.

### Appendix C — Printable First-Step / Revision Handout

- standalone usable;
- first moves / key representations / rules / conditions / traps;
- short retrieval/self-check;
- no new content not grounded in Core 1;
- not a dense answer sheet.

The base contract may be extended for proof exams, practical/lab work or other response formats.

---

## 17. Core 2 must cite Core 1

Core 2 should not copy the entire source ledger into the learner pages, but it must preserve machine and reviewer traceability.

Required chain:

```text
PUBLISH SECTION / QUESTION / FIGURE
          ↓ derived_from
RESEARCH CORE OBJECT ID
          ↓ supported_by
SOURCE SNAPSHOT / QUESTION OCCURRENCE
```

Examples:

```text
PC-SEC-04 → RC-CON-LOM-04 → RC-SRC-0042
PC-FIG-02 → RC-REP-FBD-01
PC-Q-A7   → RC-QF-LOM-07 → QO-SOF-ISO-2025-Qxx
```

### 17.1 Human-facing citation style

Use unobtrusive references in Core 2, for example:

```text
[Research anchor: RC-CON-LOM-04]
```

or endnotes/source notes where direct source citations are useful.

Do not clutter student pages with publisher/audit language. The student-facing PDF can keep citations minimal while the Markdown/manifest retains the full chain.

---

## 18. Shared data persistence

A Research Core should reuse shared canonical objects rather than cloning them into every project.

Logical split:

```text
SHARED / GLOBAL
  concepts
  methods
  representations
  misconceptions
  question families
  source documents / source snapshots
  question content / occurrences
  exam families / cycles / demands
  curriculum profiles

PROJECT RESEARCH PACK
  selected IDs
  project-specific scope
  project-specific evidence decisions
  Bxx matrix
  purpose
  research run
  Research Core narrative

PUBLISH PACK
  transformations from Research Core IDs
  student-facing questions/examples
  layout/publication metadata
```

A project manifest should reference shared IDs rather than copying their canonical records.

---

## 19. Avoiding repeated web fetches

Before any network research, query the research/source index by:

```text
normalized URL
source provider
exam family + cycle
source document hash
concept IDs
question content fingerprint
research intent
retrieved_at / freshness window
```

Possible outcomes:

```text
REUSE_VERIFIED_FRESH
REVERIFY_STALE
SEARCH_MISSING
SOURCE_UNRESOLVED
```

Accepted web evidence is stored once as a `SourceSnapshot` plus extracted structured entities. Later Research Cores point to those IDs.

A second project on the same exam/topic should normally reuse the previous verified snapshot rather than download/reclassify it again.

---

## 20. Question deduplication during research

Competitive preparation must separate:

```text
QuestionContent      intellectual question
QuestionOccurrence   where/when it appeared
QuestionFamily       underlying recognition/method family
QuestionAdaptation   learner-facing derived version
```

This supports cases such as the same past-paper question appearing on:

```text
official paper
official solution archive
ExamSIDE/index
publisher mirror
user PDF
```

There should still be one canonical `QuestionContent` object with multiple occurrences.

Agent 2 may create a scaffolded adaptation, but it remains linked to the canonical content/family and cannot masquerade as the source occurrence.

---

## 21. Example 1 — Grade 9 Physics, Laws of Motion, competitive exam

Prompt:

> Prepare study material for Grade 9 Physics, Laws of Motion, for NSO/ISO exam or an ExamSIDE-type mock.

### Phase A — discovery before user confirmation

```text
1. parse Grade 9 / Physics / Laws of Motion / competitive intent
2. search repository/shared store
3. resolve current exam identity (e.g. SOF NSO historical vs SOF ISO current cycle)
4. find existing verified sample/past-question evidence
5. research missing exam-demand evidence if needed
6. decompose Laws of Motion according to actual question-demand families
```

The agent may propose:

```text
inertia / first law
force and acceleration / second law
momentum interpretation where in scope
free-body diagrams
friction
third-law action-reaction pairs
multi-body / transfer variants if exam evidence supports them
```

### Phase B — user confirmation

Ask for/confirm:

```text
subtopics to include
Bxx for each subtopic
primary purpose: study or mock
specific exam cycle/level if important
```

### Phase C — Core 1

Research Core contains:

```text
canonical physics explanation
model conditions
FBD representation specification
misconception map
exam-demand map
question-family distribution
verified source/sample evidence
research citations
```

### Phase D — independent Core 2

Publish agent receives Core 1 and the Bxx matrix.

For B30 FBD + B80 inertia, for example:

```text
FBD pages = explicit body choice, force source, arrow meaning, guided completion
inertia pages = compressed recap, contrast cases, earlier exam transfer
```

Appendix A is exam-shaped practice, Appendix B contains progressive help/solutions, Appendix C is the compact first-step/revision sheet.

Every section/question carries `derived_from` Research Core IDs in metadata.

---

## 22. Example 2 — Grade 10 Chemistry, Redox, generic study

Prompt:

> Prepare study material for Grade 10 Chemistry on Redox.

### Phase A — repository discovery

Search for:

```text
existing Redox canonical concepts
prior Research Core / source map
macro-particle-symbolic representations
oxidation-number / electron-transfer misconceptions
existing question families
user-supplied Redox PDF provenance
```

### Phase B — ask scope/baseline

The agent proposes a subtopic table and asks the user to confirm Bxx values, for example:

```text
oxidation / reduction meaning        B50
oxidation number rules               B30
oxidising vs reducing agent          B40
electron-transfer representation     B60
redox identification                 B70
```

Purpose defaults to `ROUTINE_STUDY` unless the user specifies competitive/mock/revision.

### Phase C — research

Use user PDFs/links as the requested source authority. Research the web only for explicit expansion/current curriculum or evidence gaps, keeping source-derived and web-derived additions distinguishable.

### Phase D — Core 1

Research Core freezes:

```text
source obligations
canonical chemistry claims
macro / particulate / symbolic transitions
oxidation-number rules + exceptions in scope
agent logic
representation specifications
misconceptions
question families
citations
```

### Phase E — Core 2

Publish Core adapts the same Research Core for the requested Bxx distribution and produces the learner PDF with Appendix A–C.

No web search is required by Agent 2 unless it returns a research-backfill request.

---

## 23. Mock-generation rule

An `EXAM_MOCK` request must not mean “make difficult questions”.

Core 1 first freezes a mock blueprint from exam evidence:

```text
question count / section structure
response format
concept distribution
question-family distribution
representation distribution
difficulty/demand distribution
time-pressure characteristics
source/current-cycle constraints
```

Core 2 then authors/selects the mock from approved canonical/question-family data.

Original mock questions must be labelled `ORIGINAL_CALIBRATED`, never passed off as previous-year questions.

---

## 24. Skill ownership implied by the two-core design

The architecture should eventually expose two top-level workflows rather than one giant skill:

```text
RESEARCH CORE WORKFLOW
  repo discovery
  source grounding
  subject authority
  exam registry / curriculum profile
  web research
  question/corpus analysis
  concept architecture
  research-core freeze

PUBLISH CORE WORKFLOW
  research-core validation
  subject-aware pedagogical adaptation
  Bxx adaptation
  exam-purpose adaptation
  learning enrichment
  question selection/original adaptation
  publication
  completeness / render QA
```

Existing subject skills remain authorities. Existing publication skills remain render/reconstruction authorities. The new cores are workflow compositions, not replacement subject authorities.

---

## 25. Cold-start handoff test

The decisive test is deliberately asymmetric:

### Agent 1 test

Given only:

```text
user request
repository
supplied files/links
web access when policy permits
```

can Research produce a complete frozen Core 1?

### Agent 2 test

Given only:

```text
01_Research_Core.md
01_Research_Core.manifest.json
01_Research_Ledger.json
explicit Bxx/purpose profile
canonical schemas/skills
```

and **no original chat history**, can Publish produce the same learner architecture and traceability?

Required counters:

```text
RESEARCH_CORE_REPRODUCIBLE = PASS
PUBLISH_AGENT_NO_HIDDEN_CONTEXT = PASS
PUBLISH_AGENT_UNDECLARED_WEB_SEARCHES = 0
PUBLISH_TO_RESEARCH_LINK_COVERAGE = 100%
UNSUPPORTED_PUBLISH_CLAIMS = 0
```

---

## 26. Failure modes this contract must prevent

1. Core 2 searches independently and builds a competing source corpus.
2. B30 wording is stored as if it were canonical concept truth.
3. exam difficulty is confused with student Bxx.
4. user baseline for one subtopic is applied to the whole chapter.
5. a mock is generated from generic “hard” questions instead of exam demand evidence.
6. the same ExamSIDE/past-paper page is fetched and classified repeatedly.
7. a source question is copied once per website mirror.
8. Core 2 cannot identify which Core 1 claim supports a paragraph/question.
9. a Publish agent fixes a research gap silently.
10. research material contains learner-layout decisions that should belong to Publish.
11. Publish Core contains facts not supported by Core 1 or approved source additions.
12. user-supplied source material is silently replaced by generic web knowledge.
13. secondary web sources are treated as official exam authority.
14. copyrighted third-party material is copied into shared storage without permission/source policy.
15. the Research Core becomes so student-specific that it cannot be reused for another Bxx publication.

---

## 27. Proposed implementation sequence

### Phase 1 — schemas and handoff only

Define:

```text
ResearchBrief
BaselineMatrix
ResearchCoreManifest
ResearchObject IDs
ResearchLedger
PublishCoreManifest
ResearchBackfillRequest
```

Use Markdown + JSON fixtures before building a database.

### Phase 2 — repo-first discovery + research cache

Add:

```text
shared-object lookup
source snapshot registry
research-run registry
freshness checks
question-content dedup
```

### Phase 3 — one competitive and one generic falsifier

Pilot exactly the two examples in this note:

```text
G9 Physics Laws of Motion → competitive study/mock
G10 Chemistry Redox → generic routine study
```

Use at least two baseline patterns per pilot, such as B30-heavy and B80-heavy, from the same Research Core.

### Phase 4 — independent-agent replay

Freeze Core 1, start a clean Publish agent, prohibit chat-history access and test Core 2 reproduction/traceability.

### Phase 5 — expand exams/subjects only after replay passes

Then test IOQM/RMO, optics, electricity, bonding/equilibrium and proof-oriented Mathematics to stress new representations/response contracts.

---

## 28. Approval decisions requested

| ID | Decision | Recommendation |
|---|---|---|
| TC1 | Make Research Core + Publish Core the default two-output architecture for study-material generation | APPROVE |
| TC2 | Require topic/subtopic baseline matrix using Bxx before final Research Core freeze | APPROVE |
| TC3 | Keep Bxx as student-prior-knowledge estimate, separate from exam demand/difficulty | APPROVE |
| TC4 | Search repository/shared store before web research | APPROVE |
| TC5 | For competitive requests, reverse engineer topic demand from verified exam/sample evidence before publication | APPROVE |
| TC6 | Persist accepted research/source data as reusable structured entities and snapshots | APPROVE |
| TC7 | Make Research Core machine-readable and sufficient for an independent Publish agent | APPROVE |
| TC8 | Prohibit Publish-agent web research by default; use ResearchBackfillRequest for evidence gaps | APPROVE |
| TC9 | Require every material Core 2 object to trace to Research Core IDs | APPROVE |
| TC10 | Use Appendix A Practice, Appendix B Hints/Solutions, Appendix C First-Step/Revision Handout as the shared base publication contract | APPROVE |
| TC11 | Allow subject/exam profiles to extend, but not silently replace, the shared Appendix contract | APPROVE |
| TC12 | Pilot one competitive Physics and one generic Chemistry use case before broad rollout | APPROVE |

---

## 29. Recommended approval statement

> Approved in principle to adopt a two-core operating model for study-material generation. Core 1 (`Research Core`) owns repository discovery, source/web research, source custody, canonical concept and representation architecture, question-family/exam-demand analysis and the frozen evidence handoff. Core 2 (`Publish Core`) consumes that frozen handoff to create a Bxx- and purpose-adapted learner publication with Appendix A–C and complete traceability back to Core 1. The Publish agent must not independently redefine source/exam truth or create a parallel research corpus; unresolved evidence is returned through an explicit research-backfill request.

---

## 30. Central invariant

> **Research once; publish many. Core 1 owns truth and evidence. Core 2 owns learner adaptation and presentation. A new Publish agent must be able to work from Core 1 without the original chat, and every Core 2 claim/question/representation must remain traceable to the Research Core that authorized it.**
