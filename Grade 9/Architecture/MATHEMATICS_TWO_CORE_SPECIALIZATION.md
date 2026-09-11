# Mathematics Two-Core Specialization

**Applies to:** the Unified Two-Core Architecture  
**Scope:** Mathematics across Grades 9–11, school/foundation/Olympiad-style use cases  
**Status:** DRAFT / FOR REVIEW  
**Date:** 2026-09-10

---

## 1. Mathematics specialization decision

Mathematics uses the same two-core boundary as Physics and Chemistry, with one important ownership rule:

> **Mathematical truth, invariants, conditions, proofs/derivations, decision boundaries and question mechanisms belong upstream. Learner assimilation, hint fading and publication belong downstream.**

Long-term model:

```text
grade9-math / Math subject authority
        ↓
shared canonical Math registry
        ↓
project ScopeGraph
        ↓
CORE (1) — Math Research
        ↓
Research Bundle + Manifest
        ↓
                     LearnerProfile + PublicationTarget
                                ↓
CORE (2) — Math Publish profile over PR #161
        ↓
learner Study Guide / optional Transfer Book
```

---

## 2. Remove implicit B50 from mathematical authority

The current Math family contains a roughly-50%-known default for difficult concepts. Under this architecture that is no longer a canonical subject assumption.

The router should ask for Bxx by subtopic when learner targeting is required:

```text
Grade 9 Mathematics — Polynomials

algebraic identities             B85
factorisation                    B70
factor theorem                   B55
remainder theorem                B30
transformed-polynomial problems  B15
```

Store these values in `LearnerProfile`, not `Research_Bundle.json`.

If a user declines calibration, use an explicit low-confidence fallback:

```yaml
baseline:
  value: 50
  basis: FALLBACK_USER_DECLINED_CALIBRATION
  confidence: LOW
```

Bxx does not change the mathematical truth or Research Bundle identity.

---

## 3. Competitive and generic intake differ

### Competitive Mathematics

```text
repo search
→ resolve exam/cycle/response contract
→ inspect verified sample/PYQ evidence
→ reverse engineer mechanisms and hidden prerequisites
→ propose ScopeGraph/subtopics
→ ask final Bxx by subtopic
→ Core (1)
→ Core (2)
```

This is appropriate for IOQM/RMO/INMO/Olympiad-foundation style work because the exam may test mechanisms not obvious from the school chapter list.

### Generic Mathematics

```text
repo search
→ propose/confirm topic/subtopics
→ ask Bxx + purpose
→ research missing/stale evidence only
→ Core (1)
→ Core (2)
```

Routine study should not trigger broad Olympiad/PYQ research by default.

---

## 4. Core (1) Mathematics responsibilities

Math Core (1) owns project verification of:

```text
canonical concept references
prerequisite and bridge graph
invariants / hidden structures
derivations / proofs where required
conditions / domains / edge cases
representations
expert noticing / first moves
nearest competing method
misconceptions
transfer endpoints
question families
exam-demand interpretation
source/question evidence
```

Core (1) references the shared canonical Math registry through a project `ScopeGraph`; it does not silently mutate the ontology.

New/changed mathematical concepts follow:

```text
RESEARCH_CANDIDATE
→ MATH SUBJECT REVIEW
→ CANONICAL PROMOTION
→ new registry version
```

---

## 5. Mathematics Research Bundle objects

Illustrative semantic objects:

```yaml
concept_ref:
  concept_id: MATH-POLY-C03

project_extension:
  prerequisite_ids: [...]
  bridge_ids: [...]
  invariant: ...
  visible_clues: [...]
  first_moves: [...]
  decision_boundaries: [...]
  representation_ids: [...]
  misconception_ids: [...]
  transfer_endpoint_ids: [...]

mathematical_claim:
  claim_id: MCL-017
  concept_id: MATH-POLY-C03
  statement: ...
  derivation: ...
  conditions: [...]
  edge_cases: [...]
  verification_status: VERIFIED
  source_refs: [...]

example:
  example_id: MEX-009
  concept_id: MATH-POLY-C03
  purpose: NEUTRAL_EXEMPLAR
  solution_path: [...]
  expert_noticing: ...
  representation_ids: [...]
```

Learner Bxx is deliberately absent from the semantic bundle.

---

## 6. Mathematics Research Core MD/PDF

The Research Core human view should remain learner-neutral and be derived/reconciled from the semantic bundle.

Recommended concept view:

```text
WHY THIS CONCEPT EXISTS
↓
PREREQUISITES / BRIDGES
↓
INTUITIVE ENTRY
↓
INVARIANT / HIDDEN STRUCTURE
↓
REPRESENTATIONS
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
EVIDENCE
```

Required zero-drift checks:

```text
BUNDLE_TO_MD_MATERIAL_COVERAGE = 100%
BUNDLE_TO_PDF_MATERIAL_COVERAGE = 100%
```

---

## 7. Competitive-exam reverse engineering belongs in Core (1)

For each representative problem store, as applicable:

```text
surface form
actual mathematical engine
hidden prerequisites
recognition trigger
representation choice
expert noticing
nearest tempting wrong method
minimum legitimate solution path
response-format demand
proof/completeness demand
transfer family
```

For proof-oriented exams, include explicit proof-demand dimensions such as logical dependency, case completeness, lemma choice, notation precision and proof closure.

Core (2) consumes these findings; it does not browse again to rediscover them.

---

## 8. External-question denominator

Math Core (1) must use the canonical corpus-coverage service and Math-specific extension/profile, rather than create a second denominator engine.

`Question_Evidence_Ledger.json` records the frozen result with:

```text
REQUIRED | DEFER | EXCLUDE | REVIEW | DUPLICATE
primary concept owner
source/transcription/answer state
QuestionContent + QuestionOccurrence + QuestionFamily
publication target
reason/duplicate link
```

`REVIEW` blocks closeout.

---

## 9. Core (2) Mathematics responsibilities

Math Publish owns learner transformation:

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

The existing assimilation choreography remains valuable, but it belongs in the downstream Math Publish profile rather than the subject authority.

Hint semantics:

```text
H0 INDEPENDENT
H1 RECOGNITION
H2 STRUCTURE / REPRESENTATION
H3 FIRST EXECUTABLE STEP
```

Support must fade.

---

## 10. Bxx execution profile

### B81–B100

Compressed reconnect, decision boundaries, competing methods, early H0, harder transfer, proof/efficiency critique where relevant.

### B61–B80

One complete conceptual reconstruction, representation switching, limited guided support, misconception contrast, fade to H0.

### B41–B60

Explicit missing bridge, multiple representations, worked model, guided first move, decision-boundary contrast.

### B21–B40

Prerequisite reconstruction, concrete examples before symbols, explicit bridge, worked + guided completion, full hint fading.

### B0–B20

Near-first exposure, prerequisite mini-lessons, meaning before notation, narrow cognitive load, repeated retrieval, gradual independence.

These are publication transformations, not different mathematics.

---

## 11. Purpose × Bxx

Purpose and learner baseline remain independent:

```text
ResearchBundle × LearnerProfile × PublicationTarget
                      ↓
               Math Publish Core
```

Examples:

`ROUTINE_STUDY` emphasizes conceptual continuity and retrieval.

`CONCEPT_CLARIFICATION` emphasizes missing bridges, contrast pairs, wrong-model diagnosis and reconstruction.

`COMPETITIVE_PREPARATION` emphasizes recognition speed, hidden structure, method selection, alternate routes, traps and mixed transfer.

`EXAM_MOCK` follows a frozen exam-demand blueprint and keeps concept identity hidden where the target exam does.

---

## 12. Appendix contract for Mathematics

Use the shared base:

```text
Appendix A — Core Practice
Appendix B — Core Solutions
Appendix C — Printable Handout
```

### Appendix A

Independent/faded practice covering routine application, recognition, representation change, compare/contrast, error diagnosis, reconstruction/proof and disguised transfer.

### Appendix B

Complete solutions. Hints may be available separately or adjacent to attempt paths, but Appendix B's invariant role is solutions.

Suggested solution structure:

```text
QUESTION RECAP
REQUIRED REPRESENTATION
WHY / KEY IDEA
METHOD
ANSWER / CHECK
CONDITION / EDGE CASE
CONCEPT TO KEEP
RESEARCH LINK
```

### Appendix C

One printable/revision handout. For Mathematics, `first_step_reference` is normally a required internal module alongside:

```text
concept map
visible triggers
invariants/theorems with conditions
decision router
common traps
first moves
short self-check
```

---

## 13. Shared Representation Layer for Mathematics

Mathematics must use the same Shared Representation Layer as Physics/Chemistry.

Required Math families may include:

```text
number line
coordinate/function graph
geometric construction
proof/dependency graph
algebra transformation chain
case tree
combinatorial structure/table
sequence/pattern table
trusted source crop/vector asset
```

Core (1) specifies semantic obligations; Core (2) renders/composes them.

---

## 14. Material traceability

100% traceability applies to material mathematical objects:

```text
claims/theorems/conditions
worked examples
representations
questions
solution methods
exam-demand facts
```

It does not require research IDs for connective prose.

Example:

```yaml
publish_object_id: PUB-POLY-C03
traceability_class: MATERIAL_CLAIM
derived_from:
  research_claims:
    - MCL-017
  concepts:
    - MATH-POLY-C03
```

---

## 15. Research-gap rule

If Math Publish discovers missing mathematics:

```yaml
status: CORE1_RESEARCH_GAP
gap_type: CONCEPT | CLAIM | CONDITION | EDGE_CASE | REPRESENTATION | EXAM_DEMAND | QUESTION_FAMILY
object_id: ...
reason: ...
```

Core (1) resolves and versions the bundle. Core (2) must not patch locally.

---

## 16. Original-question and difficulty claims

Do not call an authored item `ORIGINAL_CALIBRATED` unless calibration basis is explicit.

Prefer:

```text
ORIGINAL_EXAM_ALIGNED
ORIGINAL_EDITORIAL_PROFILED
```

If calibration is claimed:

```yaml
calibration:
  basis: SOURCE_MAPPING | EXPERT_REVIEW | EMPIRICAL
  evidence_refs: [...]
```

Difficulty labels likewise carry basis/provenance.

---

## 17. Math-specific gates

### Core (1)

```text
SCOPE_GRAPH_FROZEN = PASS
CANONICAL_REFERENCES_RESOLVED = PASS
UNAPPROVED_CANONICAL_MUTATIONS = 0
SOURCE_CUSTODY = PASS
MATHEMATICAL_CLAIMS_VERIFIED = PASS
PREREQUISITES_AND_BRIDGES_COMPLETE = PASS
CONDITIONS_AND_EDGE_CASES_VERIFIED = PASS
REPRESENTATIONS_RESOLVED = PASS
DECISION_BOUNDARIES_RESOLVED = PASS
EXAM_REVERSE_ENGINEERING = PASS | NOT_APPLICABLE
QUESTION_EVIDENCE_RECONCILED = PASS | NOT_APPLICABLE
BUNDLE_TO_MD_MATERIAL_COVERAGE = 100%
BUNDLE_TO_PDF_MATERIAL_COVERAGE = 100%
BLOCKING_RESEARCH_GAPS = 0
```

### Core (2)

```text
MATERIAL_TRACEABILITY_COVERAGE = 100%
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
RENDER_QA = PASS
```

---

## 18. Existing Math skill implication

Long-term ownership:

```text
grade9-math
  = Math subject authority

Core (1) Math Research workflow
  = project evidence/scope/verification

canonical corpus authority + Math profile
  = question denominator/coverage

Core (2) Math Publish profile
  = assimilation/scaffolding/publication
```

`grade9-math-assimilation` contains valuable downstream pedagogy, but should eventually delegate/migrate that choreography into Math Publish rather than remain a second end-to-end authority.

Do not delete/rename current stable skill IDs until compatibility migration is separately approved.

---

## 19. Cold-start acceptance

Research agent starts from request/repository/sources and produces a verified Research Bundle package.

Publish agent receives only:

```text
Research_Bundle.json
Research_Bundle_Manifest.json
Research_Core.md / PDF
Research ledgers/assets
LearnerProfile
PublicationTarget
canonical schemas/skills
```

No prior chat/browser state.

Required:

```text
MATH_RESEARCH_CORE_REUSABLE = PASS
PUBLISH_AGENT_NO_HIDDEN_CONTEXT = PASS
PUBLISH_AGENT_UNDECLARED_WEB_SEARCHES = 0
MATERIAL_TRACEABILITY_COVERAGE = 100%
UNSUPPORTED_NEW_MATH_CLAIMS = 0
```

---

## 20. Central Mathematics invariant

> **Mathematics is researched and verified once per evidence version. The project Research Bundle references governed canonical mathematics and contains no learner Bxx. Learner baseline, purpose and exam target determine the downstream Math publication, while missing mathematics returns to Core (1) instead of being silently invented by the Publisher.**