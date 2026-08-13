# Grade 9 Learning System Roadmap

**Status:** Active roadmap  
**Scope:** Reusable Grade 9 learning-production system for Mathematics, Physics, and Chemistry  
**Repository root:** `Grade 9/`  
**Primary references:** `Grade9schema.md`, `Grade 9/SKILLSET.md`, `Grade 9/shared/grade9-workflow.md`

---

## 1. Vision

Build a reusable, evidence-grounded Grade 9 learning system that can turn uploaded notes, textbook pages, worksheets, past papers, or curated sources into a coherent learning product:

```text
Source material
  -> source fidelity / QC / provenance
  -> concept architecture
  -> difficulty-calibrated question bank
  -> helpers / hints / misconceptions / diagnostics
  -> mixed mastery / transfer / next-level challenge
  -> canonical master data
  -> student textbook / question bank / integrated edition
  -> publication QA / learning QA / evidence loop
```

The target is not merely to generate worksheets or PDFs. The target is a **linked learning system** in which every concept, question, hint, misconception, challenge, and assessment has a stable identity and a reason for being present.

---

## 2. Current baseline

The current Grade 9 skill family already provides:

- a Grade 9 router/orchestrator;
- source-grounding and QC rules;
- stable concept IDs and prerequisite mapping;
- user-controlled Core N question banks;
- same-level difficulty calibration against uploaded anchors;
- next-level challenge banks;
- progressive hints, misconceptions, diagnostics, and transfer questions;
- Mathematics, Physics, and Chemistry subject adapters;
- linked textbook/question-bank publication rules;
- canonical master-data authority;
- deterministic bank/link validators;
- render/link/publication QA requirements.

The current workflow is strong operationally, but several policies are still based on expert heuristics rather than a sufficiently broad research base. The next stage is to convert those heuristics into **evidence-backed, testable methodology**.

---

## 3. Research-first principle

Before materially expanding the system, conduct a focused deep-research program on:

1. learning science and instructional sequencing;
2. cognitive difficulty and question calibration;
3. item-generation and item-quality methodology;
4. misconceptions, diagnostics, and feedback;
5. retrieval practice, interleaving, spacing, and mixed mastery;
6. worked examples, fading, hints, and scaffolding;
7. concept graphs, prerequisites, mastery models, and adaptive practice;
8. subject-specific pedagogy for Mathematics, Physics, and Chemistry;
9. textbook/page design for adolescent learners;
10. assessment validity, reliability, and psychometrics;
11. source provenance, copyright-safe reuse, and authored variants;
12. AI-assisted educational-content QA and hallucination control.

The research output should directly support changes to the current Grade 9 schemas and skills. See `DeepResearchPrompt.md`.

---

## 4. Target architecture

### 4.1 Canonical learning graph

Every reusable chapter should converge on:

```text
CONCEPT
  <-> source anchor
  <-> prerequisite concepts
  <-> same-level practice
  <-> next-level challenge
  <-> helper / progressive hints
  <-> misconception / error signature
  <-> worked solution / solution paths
  <-> transfer question
  <-> mixed-test diagnosis
  <-> mastery evidence
```

Stable IDs are authoritative. PDF page numbers are render outputs only.

### 4.2 Canonical master data

The canonical master should eventually contain:

- project metadata;
- source/provenance records;
- concept graph;
- learning objectives;
- anchor questions;
- calibrated core questions;
- challenge questions;
- difficulty vectors;
- solution paths;
- helper/hint ladders;
- misconception/error-signature library;
- mixed tests;
- mastery criteria;
- publication mappings;
- QA results;
- empirical learner-performance data when available.

### 4.3 Separation of concerns

```text
grade9-source-grounding
    owns source fidelity, QC, provenance

grade9-[subject]
    owns discipline-specific reasoning and difficulty dimensions

grade9-concept-architect
    owns concept IDs, prerequisites, dependency graph

grade9-question-bank
    owns calibrated item construction and mixed assessment

grade9-learning-enrichment
    owns scaffolding, diagnostics, misconceptions, transfer

grade9-textbook-publisher
    owns rendering, navigation, visual hierarchy, publication QA
```

No specialist should silently override another specialist's authority.

---

## 5. Research tracks

### RT-01 — Difficulty calibration and cognitive equivalence

**Goal:** Replace ad-hoc hard/easy judgments with a defensible, practical calibration method.

Research:

- cognitive complexity versus calculation burden;
- Bloom, revised Bloom, SOLO, Webb DOK, and related taxonomies;
- expert solution-path depth;
- representational translation demand;
- hidden-structure / recognition demand;
- constraint/case reasoning;
- psychometric difficulty versus expert-rated difficulty;
- IRT/Rasch principles relevant to future empirical calibration;
- methods for comparing generated items to anchor items.

Deliverables:

- subject-specific difficulty vectors;
- anchor-candidate acceptance rules;
- challenge-level rules;
- calibration rubric with examples;
- uncertainty/confidence policy;
- empirical-calibration extension plan.

### RT-02 — Question-generation methodology

**Goal:** Generate fewer, better questions with controlled variation.

Research:

- isomorphic versus structurally analogous problems;
- surface-feature variation versus deep-structure transfer;
- distractor construction;
- answer-format effects;
- adversarial item QA;
- near-duplicate detection;
- concept leakage in grouped practice;
- transfer-item design;
- item templates versus generative construction.

Deliverables:

- item-generation taxonomy;
- minimum transformation requirements for authored variants;
- duplicate/similarity rejection rules;
- item-writing QA checklist;
- balanced Core N allocation policy.

### RT-03 — Learning sequence and concept architecture

**Goal:** Improve how concepts and prerequisites are ordered and linked.

Research:

- prerequisite graphs;
- knowledge-space / learning-progression models;
- worked-example sequencing;
- concrete-to-abstract and representation sequencing;
- prerequisite remediation;
- mastery prerequisites versus useful background;
- spiral review.

Deliverables:

- concept-node schema;
- prerequisite edge types;
- concept coverage metrics;
- remediation routing rules;
- concept-to-question allocation rules.

### RT-04 — Scaffolding, hints, and worked examples

**Goal:** Make help useful without leaking the solution too early.

Research:

- worked-example effect;
- expertise-reversal effect;
- completion problems;
- fading scaffolds;
- self-explanation prompts;
- progressive hints;
- metacognitive prompts;
- productive struggle and when to intervene.

Deliverables:

- hint ladder policy;
- helper-versus-hint distinction;
- reveal-level rubric;
- solution presentation policy;
- scaffold fading rules by mastery state.

### RT-05 — Misconceptions and diagnostic feedback

**Goal:** Turn wrong answers into causal diagnostic signals.

Research:

- misconception libraries;
- error classifications;
- diagnostic questions;
- feedback timing;
- explanatory versus corrective feedback;
- confidence-based diagnosis;
- misconception repair and retry design.

Deliverables:

- misconception object schema;
- error-signature schema;
- diagnostic decision tree;
- repair micro-example format;
- retry/transfer criteria.

### RT-06 — Retrieval, spacing, interleaving, and mixed mastery

**Goal:** Improve long-term retention and independent method selection.

Research:

- retrieval practice;
- spacing;
- interleaving;
- blocking versus mixing;
- desirable difficulties;
- cumulative review;
- test-enhanced learning;
- delayed transfer.

Deliverables:

- mixed-test construction policy;
- revisit cadence recommendations;
- chapter review schedule;
- mastery retest policy;
- concept-label hiding policy.

### RT-07 — Assessment quality and psychometrics

**Goal:** Make banks usable for trustworthy assessment, not only practice.

Research:

- validity and reliability;
- item discrimination;
- distractor analysis;
- classical test theory;
- Rasch/IRT basics;
- standard setting;
- score interpretation;
- small-sample constraints in classroom/home use.

Deliverables:

- assessment-mode metadata;
- minimum QA for scored tests;
- future learner-data schema;
- item-retirement/revision policy;
- score-reporting cautions.

### RT-08 — Mathematics pedagogy

Focus on:

- structural recognition;
- multiple representations;
- algebraic/symbolic fluency;
- proof/reasoning progression;
- non-routine problem solving;
- contest-style transfer without syllabus drift;
- common Grade 9 misconceptions.

Output should refine `grade9-math` and the generic question-bank calibration model.

### RT-09 — Physics pedagogy

Focus on:

- system/model selection;
- assumptions;
- diagrams and free-body diagrams;
- verbal/graphical/mathematical translation;
- units and dimensions;
- proportional reasoning;
- physical plausibility and limiting cases;
- experimental/data reasoning;
- common naive physical models.

Output should refine `grade9-physics` difficulty and solution contracts.

### RT-10 — Chemistry pedagogy

Focus on:

- macroscopic <-> particulate <-> symbolic translation;
- substance identity;
- conservation reasoning;
- evidence/claim/reasoning;
- practical-method selection;
- chemical equations and representation;
- model limitations;
- common Grade 9 misconceptions.

Output should refine `grade9-chemistry` and its question taxonomy.

### RT-11 — Textbook and question-bank UX

**Goal:** Create print/digital pages that are inviting, dense enough, and pedagogically functional.

Research:

- adolescent textbook readability;
- typography and line length;
- visual hierarchy;
- purposeful whitespace;
- worked-example layouts;
- dual coding / diagrams;
- signaling and coherence principles;
- split attention;
- cognitive load from decorative visuals;
- print versus screen differences;
- navigation and cross-linking.

Deliverables:

- page archetypes;
- density/occupancy guidance;
- typography rules;
- callout/icon rules;
- diagram decision rules;
- integrated-edition navigation specification.

### RT-12 — AI quality, provenance, and governance

Research:

- educational hallucination risks;
- independent answer verification;
- source-grounded generation;
- provenance granularity;
- copyright-safe transformation;
- AI-generated question disclosure;
- versioning and auditability;
- human-review thresholds.

Deliverables:

- provenance contract revision;
- verification severity levels;
- release gates;
- audit log format;
- source-authority hierarchy.

---

## 6. Product roadmap

### Phase 0 — Baseline freeze

**Objective:** Preserve the current proven system before research-driven changes.

Tasks:

- tag current skill family baseline;
- freeze `grade9-master.schema.json` v1;
- record current default difficulty rules;
- preserve Sequence & Series as reference implementation;
- define regression fixtures.

Exit criteria:

- current skills can reproduce an equivalent linked textbook/question-bank build;
- deterministic validators pass.

### Phase 1 — Deep research and evidence matrix

**Objective:** Build the evidence base.

Tasks:

- run `DeepResearchPrompt.md`;
- collect primary/authoritative sources;
- create claim-evidence matrix;
- separate strong evidence, expert consensus, promising practice, and open questions;
- identify contradictions between current heuristics and evidence.

Exit criteria:

- every proposed methodological change has evidence, rationale, and confidence level;
- unsupported recommendations are explicitly marked as hypotheses.

### Phase 2 — Methodology v2

**Objective:** Convert research into implementable contracts.

Tasks:

- revise difficulty model;
- revise concept/prerequisite schema;
- formalize item-generation taxonomy;
- formalize hint/scaffold policy;
- formalize misconception/diagnostic schema;
- define mixed-practice scheduling;
- define assessment versus practice modes.

Exit criteria:

- proposed schema changes have migration notes;
- subject adapters have explicit deltas.

### Phase 3 — Deterministic QA expansion

Add validators for:

- schema conformance;
- ID/link integrity;
- question-count policy;
- difficulty delta;
- duplicate/similarity flags;
- provenance completeness;
- solution/answer completeness;
- mixed-test coverage;
- concept coverage;
- publication link integrity.

Where feasible, add numeric solution checks for generated mathematics/physics/chemistry items.

### Phase 4 — Pilot chapters

Run controlled pilots on at least:

- Mathematics: one algebra/number chapter and one geometry chapter;
- Physics: Motion or Force;
- Chemistry: Matter or Atomic Structure.

For each pilot compare:

- old versus new difficulty calibration;
- question quality;
- hint quality;
- misconception usefulness;
- page usability;
- learner performance where available.

### Phase 5 — Empirical learner loop

When learner data becomes available, capture:

- answer correctness;
- time to answer;
- hint level used;
- confidence;
- misconception diagnosis;
- retry success;
- delayed retention;
- transfer success.

Use this to calibrate the expert difficulty model rather than replacing it blindly.

### Phase 6 — Adaptive Grade 9 learning engine

Longer-term target:

```text
Learner attempt
  -> evidence update
  -> concept mastery estimate
  -> misconception hypothesis
  -> choose next action
       - retry
       - helper
       - worked example
       - prerequisite repair
       - same-level practice
       - interleaved review
       - challenge
  -> reassess
```

The existing PDF/textbook system remains a publication surface over the same master data.

---

## 7. Priority implementation backlog

### P0 — Research blockers

- Deep research on difficulty calibration.
- Deep research on scaffolding/hint design.
- Deep research on question-generation quality.
- Deep research on subject-specific misconception frameworks.
- Deep research on mixed practice and mastery scheduling.

### P1 — Schema and methodology

- Add explicit learning objectives to concept nodes.
- Add prerequisite edge types (`REQUIRED`, `SUPPORTING`, `REMEDIAL`).
- Add item purpose (`LEARN`, `PRACTICE`, `DIAGNOSTIC`, `ASSESS`, `TRANSFER`, `CHALLENGE`).
- Add cognitive-demand evidence fields.
- Add difficulty confidence/uncertainty.
- Add misconception diagnostic confidence.
- Add representation-demand metadata.
- Add assessment validity metadata.

### P2 — Validators

- Duplicate / near-duplicate checker.
- Core-bank coverage checker.
- challenge lineage checker.
- hint leakage checker rubric.
- source/provenance completeness checker.
- mixed-test exposure checker.

### P3 — Publishing

- define reusable page archetypes;
- improve concept-map visualization;
- improve practice-path navigation;
- add print-friendly and screen-friendly profiles;
- add teacher edition and diagnostic summary;
- add accessibility checks.

### P4 — Empirical optimization

- learner event schema;
- mastery estimation;
- item statistics;
- spaced review scheduler;
- adaptive recommendation engine.

---

## 8. Evidence grading policy

Research recommendations should be classified as:

- **A — Strong evidence:** replicated empirical evidence, meta-analysis, authoritative synthesis, or widely accepted psychometric standard.
- **B — Good evidence:** multiple credible studies or strong domain consensus, but some boundary conditions remain.
- **C — Promising:** plausible and supported by limited evidence or adjacent evidence.
- **D — Design hypothesis:** useful engineering/pedagogical proposal requiring pilot validation.

Every roadmap change should record an evidence grade.

---

## 9. Roadmap decision record template

For every major methodology change:

```yaml
decision_id: G9-DEC-###
title: "..."
current_rule: "..."
proposed_rule: "..."
evidence_grade: A|B|C|D
source_refs: []
rationale: "..."
subject_scope: [math, physics, chemistry]
schema_impact: []
skill_files_affected: []
validation_required: []
migration_notes: "..."
status: proposed|pilot|accepted|rejected
```

---

## 10. Success metrics

### Content quality

- zero unresolved correctness defects in released scored questions;
- 100% provenance coverage;
- 100% scored-question concept mapping;
- independently verified answer/solution paths for release items;
- low near-duplicate rate among calibrated originals.

### Difficulty quality

- same-level questions preserve anchor cognitive profile;
- challenge questions increase synthesis rather than arithmetic clutter;
- expert ratings show acceptable agreement;
- empirical difficulty converges with predicted bands as learner data grows.

### Learning quality

- fewer hints needed over repeated practice;
- improved delayed-retention performance;
- improved transfer to mixed/unlabeled problems;
- misconception-specific remediation improves retry success.

### Publication quality

- no broken internal links;
- no accidental high-whitespace or overcrowded pages;
- render/preflight QA passes;
- student can move from concept -> practice -> help -> challenge -> concept without ambiguity.

---

## 11. Immediate next action

1. Run the deep-research brief in `Grade 9/DeepResearchPrompt.md`.
2. Return the complete research output, preferably with source links/citations intact.
3. Convert findings into a `research-evidence-matrix.md` and explicit change proposals.
4. Review changes against the current Sequence & Series reference implementation.
5. Revise the skill family and master schema only after the evidence review.

---

## 12. Definition of roadmap maturity

The Grade 9 framework is considered mature when:

- core methodology is evidence-backed rather than heuristic-only;
- subject-specific cognitive models are calibrated and documented;
- generated question quality is deterministic enough to audit;
- misconception/diagnostic pathways are reusable across chapters;
- mixed practice and challenge progression have clear rationale;
- textbook and question-bank layouts are validated for learning use, not only aesthetics;
- empirical learner evidence can feed back into difficulty/mastery models;
- the same Grade 9 master data can drive PDF, digital tutor, assessment, and future app experiences.
