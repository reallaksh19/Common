# Mathematics Two-Core Specialization

**Companion concept note for PR #160 review**  
**Applies to:** the shared Two-Core Research → Publish operating contract  
**Scope:** Mathematics across Grades 9–11, school/foundation/Olympiad-style use cases  
**Status:** DRAFT / FOR REVIEW  
**Date:** 2026-09-10

---

## 1. Why Mathematics needs an explicit specialization

The shared two-core architecture already separates Research Core from Publish Core. Mathematics should adopt the same boundary, but with a stronger distinction between **mathematical authority** and **learner-assimilation execution**.

The current Grade 9 Mathematics family still couples these concerns:

- `grade9-math` contains subject reasoning, concept mapping, difficulty analysis and a default roughly-50%-known learner model, plus substantial concept-book pedagogy;
- `grade9-math-assimilation` then operationalizes the same partial-knowledge model from source grounding through concept map, assimilation sequence, first-step reference, transfer/mastery and publication-oriented outputs.

The two-core design should remove that coupling without discarding the strong existing pedagogy.

> **Core 1 answers: What mathematics should be taught, what structure makes it true/useful, and what evidence supports that scope?**
>
> **Core 2 answers: How should this learner be taught that mathematics for this purpose and target exam?**

Core 2 must not silently research or redefine Mathematics when a valid Core 1 exists.

---

## 2. Target Mathematics workflow

```text
USER REQUEST
    │
    ▼
MATH INTAKE / ORCHESTRATOR
    │
    ├─ repository search first
    ├─ identify topic/subtopics
    ├─ identify purpose
    ├─ identify learner baseline by subtopic
    ├─ identify target exam/response contract when applicable
    └─ identify supplied sources / external corpus
    │
    ▼
CORE 1 — MATH RESEARCH CORE
    │
    ├─ source custody
    ├─ repo/web research
    ├─ exam reverse engineering
    ├─ concept architecture
    ├─ mathematical verification
    ├─ question-family analysis
    └─ learner-neutral canonical manuscript
    │
    ├── 01_Research_Core.md
    ├── 01_Research_Core.pdf
    ├── 01_Research_Core.manifest.json
    └── 01_Research_Ledger.json
            │
            │ frozen machine handoff
            ▼
CORE 2 — MATH PUBLISH CORE
    │
    ├─ consumes Core 1 as authority
    ├─ applies Bxx by subtopic
    ├─ applies purpose/exam profile
    ├─ chooses scaffolding and fading
    ├─ creates learner sequence
    ├─ creates Appendix A/B/C
    └─ links every published object to Core 1 IDs
    │
    ├── 02_Publish_Core.md
    ├── 02_Publish_Core.pdf
    └── 02_Publish_Core.manifest.json
```

The architectural invariant is:

> **Research once; publish many. Mathematical truth/evidence is frozen once; Bxx/purpose/exam adaptation is a reproducible downstream projection.**

---

## 3. Intake: remove the implicit B50 assumption

The current Mathematics authority uses a roughly 50%-known learner as its default model for difficult concepts. Under the two-core architecture, that should no longer be the default authoring assumption.

The orchestrator should ask only for missing inputs and should prefer a **subtopic baseline matrix**.

Example:

```text
Grade 9 Mathematics — Polynomials

Subtopic                         Baseline
algebraic identities             B85
factorisation                    B70
factor theorem                   B55
remainder theorem                B30
transformed-polynomial problems  B15

Purpose: COMPETITIVE_PREPARATION
Target: IOQM / Olympiad foundation
```

`Bxx` means estimated usable prior ownership of that subtopic. It is not intelligence, exam difficulty or a permanent student label.

If the user declines calibration, a fallback baseline may be used, but it must be recorded explicitly:

```yaml
baseline:
  value: 50
  basis: FALLBACK_USER_DECLINED_CALIBRATION
  confidence: LOW
```

Do not silently treat all Mathematics requests as B50.

---

## 4. Competitive and generic intake should not have identical ordering

### 4.1 Competitive Mathematics

For a request such as:

> Prepare combinatorics for IOQM.

Use:

```text
repo search
→ resolve exam/cycle/profile
→ inspect representative verified sample/PYQ evidence
→ reverse engineer mechanisms and hidden prerequisites
→ propose subtopic architecture
→ ask user for Bxx by proposed subtopic
→ freeze Research Brief
→ Core 1
→ Core 2
```

This prevents asking the learner to enumerate an exam-specific topic map before the system understands the actual assessment demand.

### 4.2 Generic Mathematics

For a request such as:

> Teach me quadratic equations.

Use:

```text
repo search
→ propose/confirm topic and subtopics
→ ask Bxx by subtopic
→ ask purpose
→ research only missing evidence
→ Core 1
→ Core 2
```

Do not trigger broad Olympiad/PYQ research for routine study unless requested.

---

## 5. Core 1 — Mathematics Research Core

Core 1 is the Mathematics source-of-truth package for the project. It ends before learner-level rewriting.

### 5.1 Repository-first discovery

Always inspect:

```text
existing Math authority
existing concept registry
source/corpus ledgers
prior Research Core packs
benchmarks
question families
exam profiles
existing publications
open/unresolved audits
```

If a valid Research Core already covers the requested mathematical scope and exam evidence is fresh, reuse it. Extend only missing scope or version it when the authority/exam target changes.

### 5.2 Research mode by purpose

`ROUTINE_STUDY`

- syllabus/textbook authority;
- repo concept architecture;
- supplied sources;
- reputable mathematical references only where needed;
- goal: complete conceptual progression.

`CONCEPT_CLARIFICATION`

Research narrowly around:

```text
prerequisite
→ missing bridge
→ invariant
→ representation
→ nearest competing method
→ misconception
→ transfer boundary
```

`COMPETITIVE_PREPARATION`

Reverse engineer the exam before publication:

```text
target exam
→ verified sample/PYQ evidence
→ question fingerprints
→ recurring mathematical mechanisms
→ hidden prerequisites
→ expected response compression/proof depth
→ traps and transfer demands
→ concept architecture
```

Do not begin from a school chapter list and merely make the questions harder.

`EXAM_MOCK`

The corpus/demand profile is a major authority:

```text
frozen evidence set
→ question engines/families
→ concept ownership
→ response format
→ difficulty/demand evidence
→ representation/proof dependencies
→ timing characteristics
→ mock blueprint
```

Use the canonical corpus-coverage machinery rather than creating a Mathematics-only competing denominator engine.

---

## 6. Mathematics-specific Research Package objects

The generic Research Core manifest should be extended for Mathematics with explicit mathematical structure.

Illustrative logical model:

```yaml
research_core_id: RC-G9-MATH-POLY-001
subject: MATHEMATICS
status: READY_FOR_PUBLISH

target:
  grade: 9
  purpose: COMPETITIVE_PREPARATION
  exam_profile_id: HBCSE_IOQM_CURRENT

scope:
  topic_ids: [MATH-POLY]
  subtopic_ids:
    - MATH-POLY-IDENTITY
    - MATH-POLY-FACTOR
    - MATH-POLY-REMAINDER

baseline_map:
  MATH-POLY-IDENTITY: 85
  MATH-POLY-FACTOR: 55
  MATH-POLY-REMAINDER: 30

concept_registry:
  - concept_id: MATH-POLY-C03
    prerequisite_ids: [...]
    bridge_ids: [...]
    invariant: ...
    visible_clues: [...]
    first_moves: [...]
    decision_boundaries: [...]
    representation_ids: [...]
    misconception_ids: [...]
    transfer_endpoint_ids: [...]

mathematical_claims:
  - claim_id: MCL-017
    concept_id: MATH-POLY-C03
    statement: ...
    derivation: ...
    conditions: [...]
    edge_cases: [...]
    verification_status: VERIFIED
    source_refs: [...]

examples:
  - example_id: MEX-009
    concept_id: MATH-POLY-C03
    purpose: NEUTRAL_EXEMPLAR
    prompt: ...
    solution_path: [...]
    expert_noticing: ...
    representation_ids: [...]

question_family_ids: [...]
exam_demand_ids: [...]
source_snapshot_ids: [...]
research_gaps: []
```

The `.md` and `.pdf` are human views of this frozen package, not independent authorities.

---

## 7. Core 1 Mathematics PDF should be learner-neutral

The Research Core PDF should not be labelled B30/B80. It should be mathematically complete and pedagogically intelligent without choosing one learner's scaffold depth.

For each major concept use a structure such as:

```text
WHY THIS CONCEPT EXISTS
↓
PREREQUISITES
↓
CONCRETE / INTUITIVE ENTRY
↓
INVARIANT / HIDDEN STRUCTURE
↓
MULTIPLE REPRESENTATIONS
↓
DERIVATION / RECONSTRUCTION
↓
DECISION BOUNDARY
↓
COMMON WRONG MODEL
↓
EXPERT FIRST MOVE
↓
EDGE / SPECIAL CASES
↓
TRANSFER ENDPOINTS
↓
SOURCE / EVIDENCE
```

This is the canonical mathematical manuscript that permits many different learner publications later.

---

## 8. Competitive-exam reverse engineering belongs only in Core 1

For example, a coordinate-geometry question may have a surface appearance such as coordinates + an integer condition, while the actual mechanism is:

```text
distance constraint
+ parity / divisibility
+ integer lattice interpretation
```

Core 1 should store:

```text
surface form
actual mathematical engine
hidden prerequisites
expert noticing
nearest wrong approach
response-format demand
transfer family
```

Core 2 consumes those objects. It must not independently browse/search merely to rediscover why the exam tests that structure.

---

## 9. Core 2 — Mathematics Publish Core

Core 2 transforms a valid Research Core for one learner/purpose profile.

Required inputs:

```text
01_Research_Core.md / PDF
01_Research_Core.manifest.json
01_Research_Ledger.json
Bxx matrix
purpose
exam/profile when applicable
publication preferences
```

No original Core 1 chat session is required.

---

## 10. Mathematics Bxx adaptation profile

The generic Bxx model should have a Mathematics-specific execution profile.

### B81–B100

- compressed reconnect;
- minimal derivation where already owned;
- decision boundaries and competing methods;
- harder disguised transfer;
- early H0;
- proof/efficiency critique where the exam requires it.

### B61–B80

- reconnect diagnostic;
- one complete conceptual reconstruction;
- representation switching;
- limited guided support;
- misconception contrast;
- fade H2 → H1 → H0.

### B41–B60

- reconnect + explicit missing bridge;
- multiple representations;
- one complete worked model;
- guided first move;
- decision-boundary contrast;
- fade H3/H2 → H1 → H0.

### B21–B40

- prerequisite reconstruction;
- concrete examples before symbols;
- explicit bridge node;
- representation choice made visible;
- worked model + guided completion;
- H3 → H2 → H1 → H0.

### B0–B20

- near-first-exposure treatment;
- prerequisite mini-lessons;
- meaning before notation;
- narrow cognitive load;
- repeated retrieval;
- gradual independence.

These are publishing transformations, not different versions of mathematical truth.

---

## 11. Purpose and baseline are independent axes

A B40 learner may need very different publications depending on purpose.

`ROUTINE_STUDY`

- conceptual continuity;
- standard applications;
- retrieval;
- moderate transfer.

`CONCEPT_CLARIFICATION`

- missing bridge first;
- contrast pairs;
- wrong-model diagnosis;
- reconstruction;
- first-move ownership.

`COMPETITIVE_PREPARATION`

- recognition speed;
- hidden structure;
- method selection;
- alternate solution routes;
- traps;
- efficient first move;
- mixed transfer.

`EXAM_MOCK`

- exam-faithful response format;
- concept-hidden attempts;
- question-family/demand distribution;
- timed structure;
- post-attempt diagnosis;
- source/occurrence traceability where external evidence is used.

Therefore:

```text
RESEARCH CORE × Bxx × PURPOSE × EXAM DEMAND
                     ↓
               PUBLISH CORE
```

---

## 12. Mathematics Publish sequence

The existing assimilation choreography remains valuable, but its execution belongs in Core 2:

```text
RECONNECT
→ DISCOVER
→ MAKE SENSE
→ TRY
→ DIAGNOSE
→ FADE
→ ADOPT
→ TRANSFER
```

Use the macro ownership sequence where useful:

```text
SEE → REALIZE → UNDERSTAND → ADOPT
```

`CONNECT` remains source/navigation traceability, not an additional cognitive stage.

### Hint semantics

```text
H0 INDEPENDENT
H1 RECOGNITION
H2 STRUCTURE / REPRESENTATION
H3 FIRST EXECUTABLE STEP
```

Support must fade; permanent H3 scaffolding is a Publish failure.

---

## 13. Appendix A–C for Mathematics

Use the shared publication base.

### Appendix A — Practice / Transfer

Include a deliberate mix of:

- routine application;
- recognition;
- representation change;
- compare/contrast;
- error diagnosis;
- reconstruction/proof where relevant;
- disguised transfer;
- exam-format items when applicable.

No answer leakage on attempt surfaces.

### Appendix B — Hints and Solutions

For each relevant item:

```text
H0 independent attempt
H1 recognition clue
H2 structure / representation
H3 first executable line
full conceptual solution
check / edge-condition verification
transferable takeaway
```

The full solution must be independently verified, not merely copied from the drafted answer.

### Appendix C — First-Step / Revision Handout

Include:

- concept map;
- visible trigger phrases/structures;
- invariants;
- formulas/theorems with conditions;
- decision router;
- visual/structural memory anchors;
- common traps;
- first moves;
- short self-check.

It is a compression product, not the teaching product and not an answer sheet.

---

## 14. Core 2 → Core 1 traceability for Mathematics

Every published concept block, worked example and practice object should retain structured lineage.

Example:

```yaml
publish_object_id: PUB-POLY-C03

derived_from:
  research_concepts:
    - MATH-POLY-C03
  research_claims:
    - MCL-017
    - MCL-021
  research_examples:
    - MEX-009
  question_families:
    - QF-POLY-FACTOR-02
```

Reviewer chain:

```text
Published explanation/question
→ Research concept / claim / example / question family
→ SourceSnapshot / QuestionOccurrence
```

The learner PDF may render only unobtrusive research anchors; the manifest retains the full chain.

---

## 15. Research-backfill rule is mandatory

If Core 2 discovers missing Mathematics, it must not patch locally.

Return:

```yaml
status: RESEARCH_BACKFILL_REQUIRED
research_core_id: ...
gap_type: CONCEPT | CLAIM | CONDITION | EDGE_CASE | REPRESENTATION | EXAM_DEMAND | QUESTION_FAMILY
object_id: ...
reason: ...
```

Core 1 is revised and re-frozen. Core 2 then resumes from the new Research Core version.

This is the decisive anti-drift rule.

---

## 16. Suggested Mathematics project structure

```text
Mathematics/
  <project>/
    00_intake/
      Request.json
      Baseline_Map.json

    01_research_core/
      01_Research_Core.md
      01_Research_Core.pdf
      01_Research_Core.manifest.json
      01_Research_Ledger.json
      Concept_Registry.json
      Math_Verification.json
      External_Corpus.json               # when applicable
      Corpus_Classification.json         # when applicable

    02_publish_core/
      Publication_Request.json
      Publication_Model.json
      02_Publish_Core.md
      02_Publish_Core.pdf
      02_Publish_Core.manifest.json
      Publication_Audit.json

    03_review/
      Research_to_Publish_Reconciliation.json
      Render_Audit.json
      Review_Record.md
```

External-question ownership belongs in Research Core because it is evidence/scope, not presentation.

---

## 17. Mathematics-specific gates

### Core 1 cannot be `READY_FOR_PUBLISH` unless

```text
REPO_DISCOVERY_RECORDED = PASS
SCOPE_FROZEN = PASS
BASELINE_MATRIX_RECORDED = PASS
PURPOSE_RECORDED = PASS
SOURCE_CUSTODY = PASS
CONCEPT_MAP_COMPLETE = PASS
PREREQUISITES_AND_BRIDGES_COMPLETE = PASS
MATHEMATICAL_CLAIMS_VERIFIED = PASS
CONDITIONS_AND_EDGE_CASES_VERIFIED = PASS
REPRESENTATIONS_RESOLVED = PASS
DECISION_BOUNDARIES_RESOLVED = PASS
EXAM_REVERSE_ENGINEERING = PASS | NOT_APPLICABLE
QUESTION_FAMILY_EVIDENCE = PASS | NOT_APPLICABLE
RESEARCH_MD_PDF_MATCH_MANIFEST = PASS
BLOCKING_RESEARCH_GAPS = 0
```

### Core 2 cannot pass unless

```text
PUBLISH_TO_RESEARCH_LINK_COVERAGE = 100%
BASELINE_PROFILE_APPLIED_TO_EVERY_SUBTOPIC = PASS
PURPOSE_PROFILE_APPLIED = PASS
EXAM_PROFILE_APPLIED = PASS | NOT_APPLICABLE
UNSUPPORTED_NEW_MATHEMATICAL_CLAIMS = 0
APPENDIX_A = PASS
APPENDIX_B = PASS
APPENDIX_C = PASS
ATTEMPT_BEFORE_HINT = PASS
HINT_FADING = PASS
MATHEMATICAL_ANSWERS_INDEPENDENTLY_VERIFIED = PASS
RESEARCH_TO_PUBLISH_RECONCILIATION = PASS
RENDER_QA = PASS
```

---

## 18. Implication for the existing Math skill family

Long-term ownership should become:

```text
grade9-math
    = Mathematics subject reasoning authority
      invariants / correctness / solution-path semantics /
      representations / misconceptions / decision boundaries

        │
        ├───────────────┐
        ▼               ▼
MATH RESEARCH CORE      canonical corpus/coverage authority
workflow                + Math-specific extension/profile
        │
        ▼
MATH RESEARCH PACKAGE
        │
        ▼
MATH PUBLISH CORE
workflow
        │
        ▼
learner publication + QA
```

The current `grade9-math-assimilation` contains valuable pedagogy, but under this architecture it should not remain a second independent end-to-end authority. Its reusable teaching choreography should be migrated/delegated into the Mathematics Publish Core profile.

Likewise, low-level rendering/schema/audit code should remain a dependency of Publish Core rather than becoming the user-facing knowledge/research authority.

Do **not** change or delete current skill IDs until migration/compatibility is separately approved.

---

## 19. Cold-start Mathematics acceptance test

### Research agent

Given only:

```text
user request
repo
supplied files/links
web access when policy permits
```

can it produce a complete, verified, reusable Mathematics Research Core?

### Publish agent

Given only:

```text
01_Research_Core.md
01_Research_Core.manifest.json
01_Research_Ledger.json
explicit Bxx matrix
purpose/exam profile
canonical schemas/skills
```

and no original chat/browser state, can it produce the learner publication with complete traceability?

Required:

```text
MATH_RESEARCH_CORE_REUSABLE = PASS
PUBLISH_AGENT_NO_HIDDEN_CONTEXT = PASS
PUBLISH_AGENT_UNDECLARED_WEB_SEARCHES = 0
PUBLISH_TO_RESEARCH_LINK_COVERAGE = 100%
UNSUPPORTED_NEW_MATH_CLAIMS = 0
```

---

## 20. Reuse example

One canonical Research Core for Quadratics should support multiple Publish Cores:

```text
Quadratics Research Core
    ├─ B30 routine-study publication
    ├─ B80 routine-study publication
    ├─ B50 school-exam publication
    ├─ B70 Olympiad-foundation publication
    └─ B40 concept-repair publication
```

The source custody, concept registry, derivations, conditions, misconceptions and question-family evidence are not re-researched for each learner profile.

---

## 21. Approval decisions requested

| ID | Decision | Recommendation |
|---|---|---|
| M1 | Adopt Mathematics Research Core + Publish Core as the Math specialization of the shared two-core model | APPROVE |
| M2 | Remove implicit B50 as the normal default; require subtopic Bxx or an explicit fallback record | APPROVE |
| M3 | Keep Core 1 learner-neutral even when Bxx is known | APPROVE |
| M4 | Put mathematical verification, invariants, bridges, decision boundaries and exam reverse engineering in Core 1 | APPROVE |
| M5 | Put partial-knowledge assimilation choreography, hint fading and learner sequencing in Core 2 | APPROVE |
| M6 | Require independent mathematical answer verification before Core 2 PASS | APPROVE |
| M7 | Make competitive Mathematics discover/reverse-engineer exam demand before asking final Bxx subtopic mapping | APPROVE |
| M8 | Require ResearchBackfillRequest rather than local Publish patches for missing Mathematics | APPROVE |
| M9 | Reuse the shared corpus authority rather than create a second Math-only denominator engine | APPROVE |
| M10 | Preserve existing skill IDs until a separate compatibility/migration change is approved | APPROVE |

---

## 22. Central Mathematics invariant

> **Mathematics is researched and verified once. Learner level, purpose and exam demand determine how that Mathematics is taught, not what the Mathematics is. A Publish agent may transform a frozen Research Core, but may not silently become a second Mathematics researcher.**
