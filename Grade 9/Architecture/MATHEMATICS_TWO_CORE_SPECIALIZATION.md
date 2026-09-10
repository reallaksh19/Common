# Mathematics Two-Core Specialization

**Status:** Adopted for architecture design; implementation pending  
**Unified architecture:** [`UNIFIED_TWO_CORE_ARCHITECTURE.md`](UNIFIED_TWO_CORE_ARCHITECTURE.md)  
**Core (1):** [`CORE1_RESEARCH_CONCEPT_NOTE.md`](CORE1_RESEARCH_CONCEPT_NOTE.md)  
**Core (2):** [Draft PR #161](https://github.com/reallaksh19/Common/pull/161)

Mathematics uses the same two-core boundary as Physics and Chemistry, with a stricter distinction between **mathematical authority** and **learner-assimilation execution**.

> **Core (1) answers: What mathematics is true, in scope, structurally important and supported by evidence?**  
> **Core (2) answers: How should this learner be taught that mathematics for this purpose/exam?**

---

## 1. Target workflow

```text
USER REQUEST
    ↓
MATH INTAKE / ROUTER
    ├─ repo search first
    ├─ topic/subtopics
    ├─ purpose/exam
    ├─ Bxx by subtopic
    └─ supplied sources/corpus
    ↓
CORE (1) — MATH RESEARCH
    ├─ source custody
    ├─ mathematical verification
    ├─ concept architecture
    ├─ invariants / bridges / decision boundaries
    ├─ question-family analysis
    └─ competitive-exam reverse engineering when applicable
    ↓
VERSIONED RESEARCH BUNDLE
    ↓
CORE (2) — MATH PUBLISH (PR #161)
    ├─ Bxx adaptation
    ├─ purpose/exam adaptation
    ├─ assimilation / fading
    ├─ Appendix A/B/C
    └─ learner publication + QA
```

> **Research once; publish many.**

---

## 2. Remove implicit B50 as the normal default

The current Math authority's roughly-50%-known learner assumption should not remain the default control surface.

Prefer a subtopic matrix:

```text
Polynomials
algebraic identities             B85
factorisation                    B70
factor theorem                   B55
remainder theorem                B30
transformed-polynomial problems  B15
```

`Bxx` is estimated prior working knowledge, not intelligence, task difficulty or permanent mastery.

If the user declines calibration, any fallback must be explicit:

```yaml
baseline:
  band: B50
  basis: FALLBACK_USER_DECLINED_CALIBRATION
  confidence: LOW
```

Core (1) records Bxx but does not simplify mathematical truth. Core (2) uses it to determine scaffolding and depth.

---

## 3. Competitive vs generic intake

### Competitive Mathematics

```text
repo search
→ resolve exam/cycle/profile
→ inspect verified samples/PYQs
→ reverse engineer mechanisms + hidden prerequisites
→ propose subtopics
→ ask/confirm Bxx
→ freeze Core (1)
```

Do not ask the learner to define an IOQM/RMO topic map before the system understands the exam demand.

### Generic Mathematics

```text
repo search
→ propose/confirm topic/subtopics
→ ask/confirm Bxx + purpose
→ research only missing evidence
→ freeze Core (1)
```

Routine study does not trigger broad Olympiad research by default.

---

## 4. Core (1) Mathematics responsibilities

Core (1) owns:

```text
scope
source/corpus custody
canonical concepts
prerequisites and missing bridges
invariants / hidden structure
mathematical claims and derivations
conditions and edge cases
representations
expert noticing / first moves
decision boundaries / competing methods
misconceptions
question families
exam-demand interpretation
verification status and evidence
```

A major concept should support:

```text
PRIOR
→ BRIDGE
→ INVARIANT
→ REPRESENTATION
→ DERIVATION / RECONSTRUCTION
→ DECISION BOUNDARY
→ WRONG MODEL
→ EXPERT FIRST MOVE
→ EDGE CASES
→ TRANSFER
```

This is the mathematical source-of-truth layer.

---

## 5. Core (1) canonical outputs

Use the shared names aligned to PR #161:

```text
<Topic>_Research_Core.md
<Topic>_Research_Core.pdf
<Topic>_Research_Bundle.json
<Topic>_Source_Ledger.json
```

Competitive/external work also uses:

```text
<Topic>_Exam_Demand_Profile.json
<Topic>_Question_Evidence_Ledger.json
```

Math-specific verification may be a referenced bundle object/file such as:

```text
Math_Verification.json
```

but `Research_Bundle.json` remains the canonical machine hand-off.

---

## 6. Mathematics Research Bundle extension

Illustrative extension:

```yaml
research_bundle_id: RC-G9-MATH-POLY-001
research_bundle_version: 1.0

project:
  grade: 9
  subject: MATHEMATICS
  topic: Polynomials

baseline_profile:
  factor_theorem: B55
  remainder_theorem: B30

concepts:
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

research_claims:
  - claim_id: R-MATH-POLY-017
    concept_id: MATH-POLY-C03
    statement: ...
    derivation: ...
    conditions: [...]
    edge_cases: [...]
    verification_status: VERIFIED
    source_refs: [...]

worked_reasoning:
  - example_id: MEX-009
    concept_id: MATH-POLY-C03
    expert_noticing: ...
    minimum_solution_path: [...]

question_family_ids: [...]
exam_demand_profile: ...
unresolved_items: []
```

The Markdown/PDF is a learner-neutral human view of the same verified package.

---

## 7. Learner-neutral Math Research Core PDF

The Research Core PDF should not be labelled B30/B80.

For each concept:

```text
WHY THIS CONCEPT EXISTS
→ PREREQUISITES
→ INTUITIVE ENTRY
→ INVARIANT / HIDDEN STRUCTURE
→ REPRESENTATIONS
→ DERIVATION / RECONSTRUCTION
→ DECISION BOUNDARY
→ COMMON WRONG MODEL
→ EXPERT FIRST MOVE
→ EDGE / SPECIAL CASES
→ TRANSFER ENDPOINTS
→ SOURCE / EVIDENCE
```

That allows the same verified mathematics to support several downstream learner publications.

---

## 8. Competitive reverse engineering belongs in Core (1)

For IOQM/RMO/Olympiad-style work, Core (1) extracts the actual mathematical engine rather than simply tagging school questions as “hard”.

For each representative item record, as applicable:

```text
surface form
primary mechanism
hidden prerequisites
recognition trigger
representation/proof dependency
expert noticing
nearest tempting wrong method
response-format demand
transfer family
time/efficiency demand where evidenced
```

Core (2) consumes these objects; it does not independently browse to rediscover them.

---

## 9. Core (2) Mathematics adaptation

Core (2), under PR #161, applies learner/purpose transformation.

Useful Math choreography retained from the existing assimilation work:

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

Macro ownership sequence:

```text
SEE → REALIZE → UNDERSTAND → ADOPT
```

Math hint semantics:

```text
H0 INDEPENDENT
H1 RECOGNITION
H2 STRUCTURE / REPRESENTATION
H3 FIRST EXECUTABLE STEP
```

Support must fade. H3 is not permanent teaching furniture.

---

## 10. Bxx Math publishing profile

### B81–B100

Compressed reconnect; decision boundaries; competing methods; early transfer; H0 early; proof/efficiency critique when relevant.

### B61–B80

One complete reconstruction; representation switching; limited guided support; misconception contrast; H2 → H1 → H0.

### B41–B60

Explicit missing bridge; multiple representations; complete worked model; guided first move; H3/H2 → H1 → H0.

### B21–B40

Prerequisite rebuilding; concrete-before-symbolic entry; explicit bridge node; worked model; guided completion; H3 → H2 → H1 → H0.

### B0–B20

Near-first-exposure treatment; prerequisite mini-lessons; meaning before notation; narrow cognitive load; frequent retrieval; gradual independence.

These are different learner transformations of one mathematical truth.

---

## 11. Purpose is independent of Bxx

For the same B40 learner:

```text
ROUTINE_STUDY
  continuity + standard applications + retrieval

CONCEPT_CLARIFICATION
  missing bridge + contrast + diagnosis + reconstruction

COMPETITIVE_PREPARATION
  recognition + hidden structure + method selection + mixed transfer

MOCK_EXAM_PREPARATION
  exam-faithful response contract + timed distribution + post-attempt diagnosis
```

So:

```text
RESEARCH BUNDLE × Bxx × PURPOSE × EXAM DEMAND
                         ↓
                    PUBLISH CORE
```

---

## 12. Appendix A/B/C aligned to PR #161

The shared Study Guide contract is:

### Appendix A — Core Practice

Include routine application, recognition, representation change, compare/contrast, error diagnosis, reconstruction/proof where relevant, disguised transfer and exam-format items when applicable. No answer leakage.

### Appendix B — Core Solutions

This is the canonical meaning of Appendix B.

Solutions should include, where applicable:

```text
QUESTION RECAP
WHY THIS METHOD FITS
REPRESENTATION / FIRST MOVE
METHOD
ANSWER / CHECK
EDGE-CONDITION / COUNTEREXAMPLE CHECK
CONCEPT TO KEEP
RESEARCH LINK
```

Hints may support attempts but do not redefine Appendix B as a “Hints appendix”.

### Appendix C — First-Step Reference / Printable Handout

Concept map, trigger structures, invariants, formulas/theorems with conditions, decision router, first moves, common traps and short self-check. It is not an answer sheet.

---

## 13. Math traceability

Every published object retains Research Bundle lineage:

```yaml
publish_object_id: PUB-POLY-C03
research_refs:
  - R-MATH-POLY-017
  - R-MATH-POLY-021
concept_refs:
  - MATH-POLY-C03
question_family_refs:
  - QF-POLY-FACTOR-02
```

Reviewer chain:

```text
Published explanation/question
→ Research Claim / concept / question family
→ SourceSnapshot / QuestionOccurrence
```

---

## 14. Gap protocol aligned to PR #161

If Core (2) finds missing mathematics, return:

```yaml
status: CORE1_RESEARCH_GAP
research_bundle_id: ...
gap_type: CONCEPT | CLAIM | CONDITION | EDGE_CASE | REPRESENTATION | EXAM_DEMAND | QUESTION_FAMILY
object_id: ...
blocking: true
reason: ...
```

Core (1) resolves the gap, increments the Research Bundle version and re-hands off.

Core (2) may not patch missing mathematics locally.

---

## 15. Mathematics release gates

### Core (1)

```text
REPO_DISCOVERY_RECORDED = PASS
SCOPE_FROZEN = PASS
BASELINE_PROFILE_RECORDED = PASS
SOURCE_CUSTODY = PASS
CONCEPT_MAP_COMPLETE = PASS
PREREQUISITES_AND_BRIDGES_COMPLETE = PASS
MATHEMATICAL_CLAIMS_VERIFIED = PASS
CONDITIONS_AND_EDGE_CASES_VERIFIED = PASS
REPRESENTATIONS_RESOLVED = PASS
DECISION_BOUNDARIES_RESOLVED = PASS
EXAM_REVERSE_ENGINEERING = PASS | NOT_APPLICABLE
QUESTION_FAMILY_EVIDENCE = PASS | NOT_APPLICABLE
BLOCKING_UNRESOLVED_ITEMS = 0
RESEARCH_BUNDLE_SCHEMA_VALID = PASS
RESEARCH_BUNDLE_HASHED = PASS
```

### Core (2), in addition to PR #161 gates

```text
PUBLISH_TO_RESEARCH_LINK_COVERAGE = 100%
BASELINE_PROFILE_APPLIED_TO_EVERY_SUBTOPIC = PASS
UNSUPPORTED_NEW_MATHEMATICAL_CLAIMS = 0
APPENDIX_A_CORE_PRACTICE = PASS
APPENDIX_B_CORE_SOLUTIONS = PASS
APPENDIX_C_FIRST_STEP_REFERENCE = PASS
ATTEMPT_BEFORE_HINT = PASS
HINT_FADING = PASS
MATHEMATICAL_ANSWERS_INDEPENDENTLY_VERIFIED = PASS
RESEARCH_TO_PUBLISH_RECONCILIATION = PASS
```

---

## 16. Existing Math skill implications

Long-term ownership:

```text
grade9-math
  = Mathematics subject authority
    correctness / invariants / representations / misconceptions /
    solution-path semantics / decision boundaries

CORE (1) Math Research
  = project research workflow

shared corpus authority + Math profile
  = source/question accounting

CORE (2) Math Publish — PR #161 profile
  = learner assimilation / fading / publication
```

`grade9-math-assimilation` contains valuable choreography but should not remain a second end-to-end mathematical authority after migration. Its reusable pedagogy should move/delegate into the downstream Math Publish profile.

Do not delete or rename existing skill IDs until compatibility migration is separately approved.

---

## 17. Cold-start test

A clean Core (2) Math agent receives only:

```text
Research_Core.md
Research_Core.pdf
Research_Bundle.json
Source_Ledger.json
Exam_Demand_Profile.json when applicable
Question_Evidence_Ledger.json when applicable
publication request
canonical schemas/skills
```

and no prior chat/browser state.

Required:

```text
MATH_RESEARCH_CORE_REUSABLE = PASS
PUBLISH_AGENT_NO_HIDDEN_CONTEXT = PASS
PUBLISH_AGENT_UNDECLARED_WEB_SEARCHES = 0
PUBLISH_TO_RESEARCH_LINK_COVERAGE = 100%
UNSUPPORTED_NEW_MATH_CLAIMS = 0
HANDOFF_HASH_MATCH = 1
```

---

## 18. Reuse example

```text
Quadratics Research Bundle
    ├─ B30 routine-study Publish Core
    ├─ B80 routine-study Publish Core
    ├─ B50 school-exam Publish Core
    ├─ B70 Olympiad-foundation Publish Core
    └─ B40 concept-repair Publish Core
```

The source custody, derivations, conditions, concept graph, misconceptions and question-family evidence are not re-researched for each learner profile.

---

## 19. Central Mathematics invariant

> **Mathematics is researched and verified once in Core (1). Learner baseline, purpose and exam demand determine how that mathematics is taught in Core (2), not what the mathematics is. A Publisher may transform a frozen Research Bundle but may not silently become a second Mathematics researcher.**
