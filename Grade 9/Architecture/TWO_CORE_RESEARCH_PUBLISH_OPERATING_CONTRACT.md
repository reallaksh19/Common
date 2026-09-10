# Two-Core Research → Publish Operating Contract

**Status:** Adopted for architecture design; implementation pending  
**Unified architecture:** [`UNIFIED_TWO_CORE_ARCHITECTURE.md`](UNIFIED_TWO_CORE_ARCHITECTURE.md)  
**Core (1):** [`CORE1_RESEARCH_CONCEPT_NOTE.md`](CORE1_RESEARCH_CONCEPT_NOTE.md)  
**Core (2):** [Draft PR #161](https://github.com/reallaksh19/Common/pull/161)

This document is the concise operating contract. Where an older draft differs, the Unified Architecture + Core (1) note + PR #161 Core (2) contract take precedence.

---

## 1. Default workflow

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
ASK / CONFIRM Bxx MATRIX + PURPOSE
      ↓
FREEZE RESEARCH BRIEF
      ↓
CORE (1) RESEARCH
      ↓
VERSIONED RESEARCH BUNDLE
      ↓
CORE (2) PUBLISH — PR #161
      ↓
LEARNER STUDY GUIDE / OPTIONAL TRANSFER BOOK
```

The default is two cores unless the user explicitly asks for `research-only` or `publish-from-existing-research`.

---

## 2. Core boundary

> **Core (1) owns truth, scope, source evidence, concept structure and exam-demand interpretation. Core (2) owns learner adaptation, representations, scaffolding, composition, rendering and publication QA.**

Core (2) must be runnable by a clean agent from the completed Core (1) package plus the publication request. No chat history or hidden researcher state is permitted.

---

## 3. Intake contract

Ask only for missing information:

```text
grade
subject
topic / subtopics
Bxx baseline by subtopic
purpose
exam / stage / cycle when applicable
user-supplied sources
```

### Bxx

`Bxx` is estimated prior working knowledge for a subtopic.

```text
B30 ≈ substantial rebuilding needed
B50 ≈ partial working knowledge
B80 ≈ strong working knowledge; more compression/transfer
```

It is not a task-difficulty or ability score. Preserve the basis (`USER_DECLARED`, `DIAGNOSTIC_DERIVED`, `TEACHER_DECLARED`, `EVIDENCE_ESTIMATED`).

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
→ confirm Bxx
→ Core (1)
```

### Generic/routine

```text
repo discovery
→ propose/confirm subtopics
→ confirm Bxx + purpose
→ use supplied/curriculum authority
→ research missing evidence only
→ Core (1)
```

A mock requires an evidence-grounded exam blueprint; “make hard questions” is not an exam model.

---

## 5. Repository-first and web-research rule

Before network research, Core (1) checks:

```text
existing Research Bundles
concept IDs/maps
source snapshots/ledgers
question content/occurrences
question families
exam profiles/cycles
representations
misconceptions
audits/review records
```

Only missing/stale evidence is searched.

> **Search → verify → fingerprint → deduplicate → map → store → reuse.**

Core (2) does not normally browse for scientific/mathematical content.

---

## 6. Core (1) outputs

Canonical names aligned to PR #161:

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

`Research_Bundle.json` is the machine hand-off.

Core (1) contains canonical claims, concepts, prerequisites, misconceptions, semantic representation requirements, equations/reactions, expert reasoning, stable research IDs, sources/assets, exam-demand evidence and explicit unresolved items.

---

## 7. Versioned hand-off

Core (2) records:

```text
research_bundle_id
research_bundle_version
research_bundle_sha256
```

A new Research Bundle version makes dependent publications stale until revalidated.

Core (2) must not silently patch research gaps. It returns:

```text
CORE1_RESEARCH_GAP
```

with a structured object containing `gap_type`, `object_id`, `reason` and `blocking`.

---

## 8. Core (2) output contract

Aligned to PR #161, the default Study Guide is:

```text
MAIN LEARNING SECTION

Appendix A — Core Practice
Appendix B — Core Solutions
Appendix C — First-Step Reference / Printable Handout
```

This replaces earlier wording that treated Appendix B primarily as “Hints”. Hints remain optional support mechanics; Appendix B's canonical purpose is complete Core Solutions.

When external/competitive practice is in scope, Core (2) may also produce a separate Transfer Book containing attempt-first H0/H1-H3 support, source/exam/difficulty/transfer metadata, primary/support concept ownership, mixed-transfer behavior and complete solutions.

---

## 9. Research → Publish traceability

Every Core (2) material object must be traceable:

```text
SOURCE / QUESTION OCCURRENCE
      ↓
CORE (1) RESEARCH CLAIM / CONCEPT / REPRESENTATION
      ↓
CORE (2) SECTION / FIGURE / QUESTION / SOLUTION
```

Core (2) may show light research anchors to students while retaining full machine linkage in publication metadata.

---

## 10. Representation responsibility

Core (1) specifies **semantic representation requirements**:

```text
what must be shown
scientific/mathematical relationships
required labels
conditions/meaning
approved assets/source crops
supporting research claims
```

Core (2), per PR #161, owns the shared Scientific Representation Core and rendering routes:

```text
structured generated vector
approved SVG/vector asset
source crop / fidelity-controlled image
```

Core (2) may choose geometry; it may not invent missing semantics.

---

## 11. Shared question/source data

Maintain separate identities:

```text
QuestionContent
QuestionOccurrence
QuestionFamily
QuestionAdaptation
```

Maintain source snapshots separately from project Research Bundles.

Projects reference shared objects instead of copying canonical data. One Research Bundle can therefore support multiple Bxx/purpose publications without repeating source research.

---

## 12. Cold-start acceptance

### Core (1)

A clean Core (2) agent must be able to identify exact scope, baseline, purpose, verified claims, required representations, exam demand, question evidence and unresolved items without the original chat.

### Core (2)

A clean Publisher receives only the frozen Research package, explicit publication request and canonical schemas/skills. It performs no undeclared research.

Required cross-core counters include:

```text
CORE1_COLD_START_SUFFICIENT = PASS
CORE2_UNDECLARED_RESEARCH_REQUIRED = 0
PUBLISH_TO_RESEARCH_LINK_COVERAGE = 100%
UNSUPPORTED_PUBLISH_CLAIMS = 0
HANDOFF_HASH_MATCH = 1
BLOCKING_RESEARCH_GAPS = 0
```

---

## 13. Examples

### Grade 9 Physics — Laws of Motion — competitive

Core (1) resolves exam identity, studies verified sample demand, freezes concepts/FBD semantics/misconceptions/question families and produces the Research Bundle. Core (2) expands B30 FBD sections, compresses B80 Newton-law recap, publishes Appendix A/B/C and an optional exam-aligned Transfer Book.

### Grade 10 Chemistry — Redox — routine study

Core (1) reuses existing Redox authority/source data, confirms subtopics/Bxx/purpose, researches only gaps, and freezes canonical macro/particle/symbolic/redox claims. Core (2) performs the Bxx-sensitive learner transformation and publishes Appendix A/B/C. No competitive crawl is required unless requested.

---

## 14. Central invariant

> **Research once; publish many. Core (1) is the only project research/evidence authority. Core (2), as specified by PR #161, is the learner/publication authority. A change in learner baseline or purpose normally rebuilds Core (2); a change in scope, scientific/mathematical truth, source evidence or exam-demand authority versions Core (1) and invalidates dependent publications until revalidated.**
