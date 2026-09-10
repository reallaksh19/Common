# Unified Two-Core Learning Architecture

**Architecture decision:** ADOPTED FOR DESIGN  
**Implementation status:** DRAFT / NOT YET MIGRATED  
**Scope:** Grades 9–11 Mathematics, Physics and Chemistry initially; extensible to additional subjects/exams  
**Core (1):** [`CORE1_RESEARCH_CONCEPT_NOTE.md`](CORE1_RESEARCH_CONCEPT_NOTE.md)  
**Core (2):** [Draft PR #161 — Core (2) Publisher](https://github.com/reallaksh19/Common/pull/161)

---

## 1. Unified decision

The production model is now:

> **Research once → Publish many.**

Every substantial study-material request is resolved through two independent cores:

```text
USER PROMPT / SUPPLIED SOURCES
            │
            ▼
      INTAKE / ROUTER
            │
            ├── grade / subject
            ├── topic / subtopics
            ├── Bxx baseline by subtopic
            └── purpose / exam target
            │
            ▼
     REPOSITORY-FIRST DISCOVERY
            │
            ▼
       CORE (1) RESEARCH
 truth · scope · source custody · concepts
 representations · verification · exam demand
            │
            ▼
   VERSIONED RESEARCH BUNDLE
            │
            ▼
       CORE (2) PUBLISH
  learner adaptation · representation rendering
  scaffolding · practice · appendices · publication QA
            │
            ▼
       LEARNER PRODUCTS
```

The two cores are different products and different authority boundaries. They are not two versions of one book.

---

## 2. Governing responsibilities

| Concern | Core (1) Research | Core (2) Publisher — PR #161 |
|---|---|---|
| repository discovery | owns | consumes result |
| web research | owns | prohibited by default |
| source custody / provenance | owns | references |
| topic/subtopic scope | owns/finalizes | preserves |
| canonical concepts/prerequisites | owns | adapts presentation |
| mathematical/scientific correctness | owns with subject authority | may not redefine |
| exam reverse engineering | owns | consumes ExamDemand |
| question evidence/families | owns | selects/adapts within contract |
| Bxx baseline | records targeting input | actively applies |
| learner sequencing | constraints only | owns |
| scientific figure semantics | specifies required meaning | renders/places |
| badges | provides underlying source/demand values | owns visual publication semantics |
| Appendix A/B/C | provides source/content obligations | owns learner implementation |
| PDF composition | reference Core PDF only | owns learner PDFs |
| publication/render QA | research artifact integrity | owns learner artifact QA |

The authority boundary is:

> **Core (1) owns truth, scope, evidence and assessment-demand interpretation. Core (2) owns learner adaptation, scientific representation rendering, scaffolding, composition and publication QA.**

---

## 3. Shared platform model

The two-core workflow sits on top of the shared-data architecture:

```text
                     SHARED CANONICAL DATA
          concepts · methods · representations · misconceptions
      QuestionContent · QuestionOccurrence · QuestionFamily · sources
          curriculum profiles · exam families/cycles/demands
                              │
                ┌─────────────┴─────────────┐
                │                           │
         PROJECT SCOPE                 STUDENT STATE
       topic / purpose / exam          Bxx / evidence
                │                           │
                └─────────────┬─────────────┘
                              ▼
                       CORE (1) RESEARCH
                              │
                     frozen Research Bundle
                              │
                              ▼
                       CORE (2) PUBLISH
                              │
                   learner/purpose projection
```

Shared knowledge is stored once. Project Research Bundles reference/select it. Publish Cores transform it for a learner/purpose.

Therefore:

```text
SHARED KNOWLEDGE → many Research Bundles
ONE Research Bundle → many Publish Cores
```

---

## 4. Intake and Bxx

The router asks only for unresolved information.

Minimum targeting fields:

```text
grade
subject
topic / subtopics
Bxx baseline by subtopic
purpose
```

Conditional fields:

```text
exam family / stage / cycle
board / curriculum
mock vs study vs clarification vs revision
user-supplied PDFs / links / papers
```

`Bxx` means estimated **prior working knowledge for that subtopic**.

It does not mean:

```text
exam difficulty
student intelligence
global mastery
question difficulty
transfer distance
```

Example:

```text
Newton's laws             B80
free-body diagrams        B30
friction                  B40
action-reaction pairs     B55
```

Core (1) records this. Core (2) turns it into different instructional depth.

---

## 5. Competitive and generic intake differ

### Competitive request

For competitive work, the system may need limited demand discovery before the user can sensibly confirm the subtopic map:

```text
repo discovery
→ resolve exam identity/cycle
→ inspect existing verified sample/PYQ evidence
→ research only missing demand evidence
→ reverse engineer mechanisms/question families
→ propose subtopics
→ ask/confirm Bxx
→ freeze Core (1) brief
```

This prevents a school chapter list from being made merely “harder”.

### Generic/routine request

```text
repo discovery
→ propose/confirm topic/subtopics
→ ask/confirm Bxx + purpose
→ use supplied source/curriculum authority
→ research only missing/stale evidence
→ freeze Core (1) brief
```

Routine study does not trigger broad competitive crawling by default.

---

## 6. Core (1) canonical outputs

The adopted Core (1) contract is defined in [`CORE1_RESEARCH_CONCEPT_NOTE.md`](CORE1_RESEARCH_CONCEPT_NOTE.md).

Mandatory outputs:

```text
<Topic>_Research_Core.md
<Topic>_Research_Core.pdf
<Topic>_Research_Bundle.json
<Topic>_Source_Ledger.json
```

Competitive/external-question additions:

```text
<Topic>_Exam_Demand_Profile.json
<Topic>_Question_Evidence_Ledger.json
```

The **Research Bundle** is the canonical machine hand-off.

The Markdown/PDF is the human research/reference core, not a B30/B80 learner book.

---

## 7. Core (2) canonical requirements from PR #161

The downstream publisher is intentionally aligned to [PR #161](https://github.com/reallaksh19/Common/pull/161).

Core (2) expects a completed, versioned Research Bundle and records:

```text
research_bundle_id
research_bundle_version
research_bundle_sha256
```

Core (2) input combines:

```text
Research Bundle
+ learner baseline profile
+ purpose / exam target
+ requested products
+ publication profile
```

If complete, Core (2) proceeds without re-asking the user.

Core (2) performs:

```text
HAND-OFF VALIDATE
→ LEARNER PROFILE
→ PURPOSE PROFILE
→ CONTENT DEPTH PLAN
→ REPRESENTATION PLAN
→ LEARNING SEQUENCE
→ PUBLICATION MODEL
→ REPRESENTATIVE PROTOTYPE
→ PROTOTYPE QA
→ FULL BUILD
→ CONTENT/REPRESENTATION QA
→ QUESTION-LEVEL CLOSURE
→ PACKAGE CERTIFICATION
```

Core (2) normally does **no scientific/mathematical web research**.

---

## 8. Gap and invalidation protocol

Use one canonical fail-back status, aligned with PR #161:

```text
CORE1_RESEARCH_GAP
```

Structured form:

```yaml
status: CORE1_RESEARCH_GAP
research_bundle_id: ...
gap_type: SOURCE | CONCEPT | REPRESENTATION | EQUATION | QUESTION_FAMILY | EXAM_DEMAND | ASSET
object_id: ...
blocking: true
reason: ...
```

Core (1) resolves the gap and publishes a new Research Bundle version.

Any Core (2) artifact built from the previous version becomes stale until revalidated.

```text
Research Bundle 1.3
   ↓
Publish Core A
Publish Core B

Core 1 changes → Research Bundle 1.4
   ↓
A + B = STALE_PENDING_REVALIDATION
```

This makes the hand-off a build dependency, not a loose citation.

---

## 9. Core (2) learner outputs

PR #161 defines the shared Study Guide base as:

```text
MAIN LEARNING SECTION

Appendix A — Core Practice
Appendix B — Core Solutions
Appendix C — First-Step Reference / Printable Handout
```

This is the adopted cross-subject base contract.

For competitive/external-question work, Core (2) may also create a separate Transfer Book with:

```text
attempt-first H0
optional H1 NOTICE
H2 MODEL / STRUCTURE
H3 START
primary/support concept ownership
source / exam metadata
separate difficulty and transfer metadata
mixed-transfer concept hiding
complete solutions
Core (1) traceability
```

Important alignment change: Appendix B is **Core Solutions**. Hints may support Appendix A or the Transfer Book but should not redefine Appendix B's canonical meaning.

---

## 10. Research-to-publication citation chain

Every material learner object must remain traceable:

```text
SOURCE / QUESTION OCCURRENCE
      ↓
CORE (1) RESEARCH CLAIM / CONCEPT / REPRESENTATION
      ↓
CORE (2) SECTION / FIGURE / QUESTION / SOLUTION
```

Example:

```text
PC-SEC-04
  derived_from → R-PHY-NLM-014
  supported_by → SRC-NCERT-...

PC-Q-A7
  derived_from → RC-QF-NLM-07
  evidence → QuestionOccurrence QO-...
```

Student pages may use unobtrusive research anchors. Machine manifests retain full linkage.

---

## 11. Scientific Representation boundary

PR #161 correctly places a shared **Scientific Representation Core** in the publication layer.

Core (1) defines semantic obligations:

```text
what must be shown
which scientific objects/relationships matter
required labels
conditions/meaning
approved assets/source crops
research claims supporting the representation
```

Core (2) renders them through reusable routes:

```text
structured generated vector
approved SVG/vector asset
source crop / fidelity-controlled image
```

Core (2) may choose geometry/layout but may not invent missing scientific semantics.

A required unsupported representation is fail-closed, not replaced by decorative approximation.

---

## 12. Shared-data and web-research rules

Before network research, Core (1) queries existing data using:

```text
source URL/provider
source hash
exam family + cycle
concept IDs
question fingerprint
question family
research intent
freshness window
prior Research Bundle
```

Results:

```text
REUSE_VERIFIED_FRESH
REUSE_WITH_REVALIDATION
SEARCH_MISSING
SOURCE_UNRESOLVED
```

Every accepted web result is verified, fingerprinted, deduplicated and stored for reuse.

Question entities remain separated:

```text
QuestionContent
QuestionOccurrence
QuestionFamily
QuestionAdaptation
```

This prevents one past-paper problem from being stored separately for every mirror and prevents repeated variants from falsely inflating mastery/coverage.

---

## 13. Subject specialization

The cores are workflows, not subject authorities.

### Mathematics

Core (1): invariant, bridge, proof/derivation, decision boundary, first move, competing method, edge cases, question-family mechanism.  
Core (2): Bxx-sensitive assimilation, `RECONNECT → DISCOVER → MAKE SENSE → TRY → DIAGNOSE → FADE → ADOPT → TRANSFER`, proof/exam adaptation.

See [`MATHEMATICS_TWO_CORE_SPECIALIZATION.md`](MATHEMATICS_TWO_CORE_SPECIALIZATION.md).

### Physics

Core (1): system, frame, model law, assumptions, units, vector/sign semantics, representation meaning, validation.  
Core (2): diagrams/graphs/equations, scaffolding, practice, mixed transfer, layout/render QA.

### Chemistry

Core (1): macro/particle/symbolic meaning, species, conservation, reaction/process conditions, evidence and exceptions.  
Core (2): particle/symbolic diagrams, chemical typesetting, learner sequencing, Appendix A/B/C and optional transfer product.

Subject-specific pedagogy extends the common Core (2) contract but does not redefine the two-core boundary.

---

## 14. Existing architecture / skills relationship

The future logical model is:

```text
ROUTER
  │
  ├── shared data / exam / curriculum lookup
  │
  ▼
CORE (1) RESEARCH WORKFLOW
  ├── source grounding
  ├── subject authority
  ├── concept architecture
  ├── corpus/exam analysis
  └── research freeze
  │
  ▼
CORE (2) PUBLISH WORKFLOW — PR #161
  ├── learner/purpose adaptation
  ├── learning enrichment
  ├── question selection/adaptation
  ├── scientific representation
  ├── publication
  └── completeness/render QA
```

Existing skills should initially remain stable. Migration should assign their useful contracts to Core (1), Core (2), subject authority, service or audit roles rather than deleting them abruptly.

In particular:

```text
grade9-math                 remains Math authority
grade9-math-assimilation    candidate downstream Publish workflow/profile
Physics/Chemistry builders  candidate subject-specific Core (2) profiles/workflows
publication skills           renderer/reconstruction dependencies, not research authority
corpus auditors              shared research/assurance services
```

---

## 15. Unified project directory concept

Conceptual project structure:

```text
<Project>/
  00_intake/
    Project_Manifest.json
    Baseline_Profile.json

  01_research_core/
    <Topic>_Research_Core.md
    <Topic>_Research_Core.pdf
    <Topic>_Research_Bundle.json
    <Topic>_Source_Ledger.json
    <Topic>_Exam_Demand_Profile.json          # when applicable
    <Topic>_Question_Evidence_Ledger.json     # when applicable

  02_publish_core/
    Publication_Request.json
    Study_Guide.publication.json
    <Topic>_<Profile>_Study_Guide.pdf
    Transfer_Book.publication.json            # when applicable
    <Topic>_<Profile>_Transfer_Book.pdf        # when applicable

  03_review/
    Research_to_Publish_Reconciliation.json
    Publication_Audit.json
    Review_Record.md
```

The exact filesystem is implementation-detail pending approval; the artifact boundaries are architectural.

---

## 16. Acceptance tests

### Core (1)

```text
REPO_DISCOVERY_RECORDED = PASS
SOURCE_LEDGER_RECONCILED = PASS
CANONICAL_CONCEPTS_RESOLVED = PASS
RESEARCH_CLAIMS_VERIFIED = PASS
REPRESENTATION_REQUIREMENTS_RESOLVED = PASS
EXAM_DEMAND_RESOLVED = PASS | NOT_APPLICABLE
QUESTION_EVIDENCE_RECONCILED = PASS | NOT_APPLICABLE
BLOCKING_UNRESOLVED_ITEMS = 0
RESEARCH_BUNDLE_SCHEMA_VALID = PASS
RESEARCH_BUNDLE_HASHED = PASS
CORE1_COLD_START_SUFFICIENT = PASS
```

### Core (2), aligned with PR #161

```text
HANDOFF_HASH_MATCH = 1
BLOCKING_RESEARCH_GAPS = 0
RESEARCH_REFS_RESOLVED = 1
REQUIRED_REPRESENTATIONS_PRESENT = 1
REQUIRED_REPRESENTATIONS_LEGIBLE = 1
QUESTION_DENOMINATOR_RECONCILED = 1
SOLUTION_DENOMINATOR_RECONCILED = 1
HINT_PROGRESSION_FAILURES = 0
METHOD_ASSIMILATION_FAILURES = 0
BADGE_MAPPING_FAILURES = 0
BROKEN_INTERNAL_LINKS = 0
BROKEN_SOURCE_LINKS = 0
MATH_SCIENCE_TYPOGRAPHY_FAILURES = 0
TEXT_OVERLAP_OR_CLIPPING = 0
FIGURE_BOUNDS_FAILURES = 0
ANSWER_LEAKAGE_FAILURES = 0
GRAYSCALE_INFORMATION_LOSS = 0
```

Independent subject review, pedagogy review, classroom effectiveness and psychometric calibration remain separate states.

---

## 17. Adoption and implementation sequence

Architecture direction is adopted; implementation remains phased.

```text
Phase 1
shared hand-off schemas + enums

Phase 2
Core (1) repo discovery / source cache / Research Bundle implementation

Phase 3
Core (2) shared publisher objects from PR #161

Phase 4
Scientific Representation Core fixtures

Phase 5
cold-start Core (1) → Core (2) replay

Phase 6
Physics Laws of Motion + Chemistry Redox falsifiers

Phase 7
Math/IOQM/proof and broader representation stress tests
```

Do not migrate all stable skill IDs before the two-core hand-off and replay are proven.

---

## 18. Final invariant

> **Canonical knowledge and evidence are researched once. Core (1) freezes a project-specific, versioned Research Bundle. Core (2), as specified by PR #161, transforms that bundle for a particular learner and purpose. A learner/publication change normally rebuilds Core (2); a truth/scope/evidence/exam-demand change versions Core (1) and invalidates dependent publications until revalidated.**
