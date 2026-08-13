# Deep Research Prompt — Grade 9 Evidence-Based Learning System

Copy the prompt below into a Deep Research session. Return the complete research report with citations and source links intact so it can be used to revise the Grade 9 skill family and roadmap directly.

---

## PROMPT START

# DEEP RESEARCH TASK

## Evidence-Based Grade 9 Learning Architecture, Question-Bank Calibration, Diagnostic Pedagogy, and Textbook/Assessment Production System

### ROLE

Act as a multidisciplinary research team combining expertise in:

- learning science and cognitive psychology;
- educational psychology;
- mathematics education;
- physics education research;
- chemistry education research;
- assessment design and psychometrics;
- item writing and question-bank engineering;
- curriculum/learning-progression design;
- educational measurement;
- textbook and instructional-material design;
- human-computer interaction for educational products;
- AI-assisted educational-content generation, validation, provenance, and safety.

Approach this as an independent research and design review. Do not simply endorse the existing methodology. Identify what is well supported, weakly supported, oversimplified, missing, or potentially harmful to learning/assessment validity.

---

# 1. PROJECT CONTEXT

I am developing a reusable Grade 9 learning-production system stored in:

`https://github.com/reallaksh19/Common`

Primary files/folders to inspect:

- `Grade9schema.md`
- `Grade 9/roadmap.md`
- `Grade 9/SKILLSET.md`
- `Grade 9/shared/grade9-workflow.md`
- `Grade 9/shared/grade9-master.schema.json`
- `Grade 9/skills/grade9/`
- `Grade 9/skills/grade9-source-grounding/`
- `Grade 9/skills/grade9-concept-architect/`
- `Grade 9/skills/grade9-question-bank/`
- `Grade 9/skills/grade9-learning-enrichment/`
- `Grade 9/skills/grade9-textbook-publisher/`
- `Grade 9/skills/grade9-math/`
- `Grade 9/skills/grade9-physics/`
- `Grade 9/skills/grade9-chemistry/`

The existing production pattern is broadly:

```text
Source material
  -> source fidelity / QC / provenance
  -> subject-specific reasoning fingerprint
  -> stable concept architecture
  -> difficulty-calibrated Core N question bank
  -> next-level challenge bank
  -> helpers / progressive hints / misconceptions / diagnostics
  -> mixed mastery / transfer
  -> canonical master data
  -> linked textbook / question bank / integrated PDF
  -> content + link + visual QA
```

A prior Sequence & Series implementation established a linked pattern:

```text
Concept
  <-> uploaded/source anchor
  <-> same-level calibrated practice
  <-> next-level challenge
  <-> helper / hints
  <-> misconception diagnosis
  <-> answers / solutions
  <-> mixed-test diagnosis
```

Current heuristics include, among others:

- difficulty is treated as a multidimensional cognitive profile rather than only Easy/Medium/Hard;
- a Mathematics same-level candidate is provisionally screened around anchor score ±0.4;
- a next-level question is provisionally targeted around +0.8 to +1.3 above the anchor;
- difficulty should increase through synthesis/recognition rather than calculation clutter;
- Core 30 is a default only when the user does not specify another number;
- when 20 usable anchors and Core 30 are requested, a common pattern is 20 anchors + 10 calibrated originals;
- progressive hints may use increasing reveal levels;
- mixed practice hides concept labels to test independent method recognition;
- textbook pages aim to avoid both excessive whitespace and overcrowding;
- canonical structured master data is authoritative; PDF is a publication product.

Treat all of these as hypotheses to evaluate, not established facts.

---

# 2. CENTRAL RESEARCH QUESTION

Research and answer:

> What evidence-based methodology should govern a reusable Grade 9 system that converts source material into concept architecture, difficulty-controlled questions, diagnostics, hints, mastery practice, next-level challenges, and textbook/question-bank publications while preserving correctness, source provenance, learner appropriateness, assessment validity, and transfer of learning?

The desired outcome is not a literature review only. I need a **directly implementable methodology** that can revise the repository's schemas, skills, algorithms, validators, and publishing rules.

---

# 3. SOURCE QUALITY REQUIREMENTS

Prioritize high-quality and preferably primary/authoritative sources.

Use, where relevant:

1. peer-reviewed meta-analyses and systematic reviews;
2. major learning-science/cognitive-psychology reviews;
3. primary educational research papers;
4. authoritative assessment/psychometric standards and organizations;
5. recognized curriculum/education research institutions;
6. mathematics/physics/chemistry education research journals;
7. major textbook/instructional-design research;
8. official examination and curriculum sources for concrete item examples;
9. authoritative AI/education research for AI-assisted content-generation risks and validation.

Do not base major conclusions primarily on SEO education blogs, commercial tutoring marketing pages, or unsourced teaching advice.

For contested areas, present competing findings and boundary conditions rather than forcing consensus.

Distinguish:

- evidence from controlled/empirical studies;
- expert consensus or standards;
- plausible design inference;
- project-specific engineering recommendation.

---

# 4. RESEARCH STREAM A — COGNITIVE DIFFICULTY AND ITEM CALIBRATION

Investigate how question difficulty should be represented and calibrated for Grade 9 learning and advanced/competitive-foundation problems.

Address:

### A1. What creates cognitive difficulty?

Investigate factors such as:

- conceptual demand;
- recognition of hidden structure;
- number/depth of reasoning steps;
- working-memory load;
- representational translation;
- abstraction;
- algebra/calculation burden;
- constraint/case reasoning;
- transfer distance;
- novelty;
- linguistic complexity;
- diagram interpretation;
- prerequisite load;
- distractor plausibility;
- time pressure.

Determine which dimensions are useful for **expert pre-calibration** before learner data exists.

### A2. Compare taxonomies/frameworks

Critically compare the usefulness and limitations of:

- Bloom / revised Bloom;
- SOLO taxonomy;
- Webb's Depth of Knowledge;
- cognitive complexity frameworks used in assessment;
- item difficulty in Classical Test Theory;
- Rasch/IRT item difficulty;
- knowledge-component / skill models;
- any relevant mathematics/science-specific cognitive-demand frameworks.

Do not assume these frameworks measure the same thing.

### A3. Anchor-based difficulty matching

Research how to decide whether a newly authored problem is genuinely equivalent in cognitive demand to an anchor problem.

Evaluate the current idea of:

```text
same-level = close multidimensional profile
challenge = same conceptual lineage + additional synthesis
```

Propose a defensible algorithm/rubric.

### A4. Evaluate numeric thresholds

Evaluate whether fixed rules such as:

- anchor ±0.4 for same-level;
- anchor +0.8 to +1.3 for challenge;

have any scientific basis or should be treated only as local engineering heuristics.

Recommend a replacement if appropriate.

### REQUIRED OUTPUT FOR STREAM A

Provide:

1. recommended difficulty dimensions by subject;
2. weighting guidance, if weights are defensible;
3. a practical anchor-to-candidate comparison rubric;
4. rejection criteria;
5. uncertainty/confidence fields;
6. future empirical calibration method using learner data;
7. example comparisons using at least one Mathematics, one Physics, and one Chemistry item.

---

# 5. RESEARCH STREAM B — QUESTION GENERATION AND ITEM QUALITY

Research how to build reliable same-level and next-level questions without creating superficial numerical variants.

Investigate:

- isomorphic problems;
- structural analogues;
- near versus far transfer;
- surface-feature changes;
- schema-based problem generation;
- template-based versus generative item construction;
- distractor design;
- misconception-based distractors;
- multiple-choice versus constructed response;
- answer-format effects;
- item-writing guidelines;
- item bias/fairness;
- ambiguity detection;
- duplicate/near-duplicate detection;
- adversarial review of generated questions;
- solution uniqueness;
- parameter selection to avoid accidental degeneracy;
- ensuring authored questions remain inside intended curriculum scope.

Evaluate the current relationship classes:

```text
NEAR_TWIN
STRUCTURAL_ANALOGUE
CONCEPT_REINFORCEMENT
ADVANCED_TRANSFER
```

Recommend improved names/classes if needed.

Determine how many same-level variants per concept are pedagogically useful before diminishing returns or overfitting to a pattern occur.

### REQUIRED OUTPUT FOR STREAM B

Provide:

- item-generation taxonomy;
- item-authoring workflow;
- minimum transformation requirements;
- item QA checklist;
- near-duplicate rejection procedure;
- concept-leakage controls;
- recommended Core N allocation algorithm when N is limited;
- worked examples of strong versus weak variants.

---

# 6. RESEARCH STREAM C — CONCEPT ARCHITECTURE AND LEARNING PROGRESSIONS

Research how the system should define and connect concepts.

Investigate:

- prerequisite graphs;
- learning progressions;
- knowledge-space theory;
- knowledge components/skills;
- threshold concepts if relevant;
- misconception dependencies;
- spiral curricula;
- prerequisite remediation;
- concept granularity;
- when one question should map to multiple concepts;
- how to designate primary versus secondary concepts;
- how concept maps differ across Mathematics, Physics, and Chemistry.

Evaluate the existing use of stable IDs such as:

```text
<CHAPTER>-C01
Q01
C21
H01
M01
T01
```

### REQUIRED OUTPUT FOR STREAM C

Provide:

- recommended concept-node schema;
- prerequisite edge types;
- mastery prerequisite rules;
- concept granularity guidance;
- many-to-many question mapping guidance;
- concept coverage metrics;
- remediation-routing logic.

---

# 7. RESEARCH STREAM D — HINTS, SCAFFOLDING, WORKED EXAMPLES, AND PRODUCTIVE STRUGGLE

Research evidence for:

- worked-example effect;
- example-problem pairs;
- completion problems;
- fading scaffolds;
- expertise-reversal effect;
- self-explanation;
- metacognitive prompts;
- progressive hints;
- feedback timing;
- productive struggle;
- when struggle becomes unproductive;
- solution visibility;
- hint penalties/mastery interpretation if relevant.

Critically evaluate a five-level progressive-hint model such as:

```text
H1 direction
H2 concept
H3 connection/representation
H4 setup
H5 near-solution
```

Determine whether fixed percentage reveal scores such as 10/25/45/70/90 have any defensible basis.

### REQUIRED OUTPUT FOR STREAM D

Provide:

- recommended helper-versus-hint definition;
- recommended number/type of hint stages;
- fading policy;
- learner-state-dependent hint policy;
- worked-example placement policy;
- solution-reveal policy;
- rules preventing hints from leaking too much;
- examples for Math, Physics, and Chemistry.

---

# 8. RESEARCH STREAM E — MISCONCEPTIONS, ERROR SIGNATURES, AND DIAGNOSTICS

Research how to identify and remediate misconceptions rather than giving generic corrections.

Investigate:

- misconception models in mathematics education;
- naive conceptions in physics education;
- alternative conceptions in chemistry education;
- error analysis;
- diagnostic assessment;
- misconception-based distractors;
- feedback specificity;
- confidence judgments;
- repair examples;
- immediate retry versus delayed retry;
- transfer checks.

Evaluate a diagnostic structure such as:

```text
wrong model
 -> observable error signature
 -> diagnostic probe
 -> repair explanation / micro-example
 -> retry
 -> transfer check
```

### REQUIRED OUTPUT FOR STREAM E

Provide:

- misconception object schema;
- error-signature schema;
- diagnostic confidence policy;
- repair workflow;
- rules for distinguishing misconception from slip/calculation error;
- subject-specific examples.

---

# 9. RESEARCH STREAM F — RETRIEVAL PRACTICE, SPACING, INTERLEAVING, AND MIXED MASTERY

Research:

- testing effect/retrieval practice;
- spacing effect;
- interleaving;
- blocked versus mixed practice;
- desirable difficulties;
- cumulative review;
- delayed testing;
- transfer testing;
- overlearning;
- how much concept labeling helps learning versus leaks strategy.

Evaluate the current model:

```text
learn by concept
 -> practice with concept visible
 -> mixed mastery with concept hidden
 -> diagnosis back to concept
```

### REQUIRED OUTPUT FOR STREAM F

Provide:

- recommended practice sequence;
- spacing/review schedule principles;
- mixed-test construction rules;
- ratio of blocked to interleaved practice if evidence supports one;
- delayed-retest rules;
- mastery-retention criteria;
- recommendations for printed textbooks versus digital tutors.

---

# 10. RESEARCH STREAM G — ASSESSMENT VALIDITY AND PSYCHOMETRICS

The system may be used for practice and assessment. These must not be conflated.

Research:

- validity;
- reliability;
- item discrimination;
- difficulty statistics;
- distractor functioning;
- classical test theory;
- Rasch/IRT;
- local dependence;
- test blueprinting;
- standard setting;
- score interpretation;
- small-sample limitations;
- formative versus summative assessment.

### REQUIRED OUTPUT FOR STREAM G

Provide:

- metadata needed to distinguish `PRACTICE`, `DIAGNOSTIC`, and `ASSESSMENT` items;
- minimum test blueprint requirements;
- what can/cannot be inferred without empirical learner data;
- future learner-performance schema;
- item revision/retirement policy;
- warnings against false psychometric precision.

---

# 11. RESEARCH STREAM H — MATHEMATICS-SPECIFIC PEDAGOGY

Research Grade 9 / secondary mathematics learning with emphasis on:

- structural recognition;
- algebraic reasoning;
- representation flexibility;
- problem solving;
- proof and justification;
- worked examples;
- procedural fluency versus conceptual understanding;
- non-routine/HOTS problems;
- transfer;
- common misconceptions;
- contest/competitive-foundation extension without premature syllabus drift.

### REQUIRED OUTPUT

Propose a Mathematics difficulty vector and question fingerprint schema suitable for the Grade 9 system, with examples.

---

# 12. RESEARCH STREAM I — PHYSICS-SPECIFIC PEDAGOGY

Research physics education with emphasis on:

- physical-system definition;
- model selection;
- assumptions;
- frame/reference choice;
- vectors and spatial reasoning;
- free-body/other diagrams;
- verbal <-> diagram <-> graph <-> equation translation;
- proportional reasoning;
- units and dimensions;
- limiting cases and sanity checks;
- experimentation and data interpretation;
- common naive physical models/misconceptions.

Evaluate whether a physics question should explicitly store fields such as:

```text
system
frame_of_reference
assumptions
knowns
unknowns
governing_model
representations
validation_checks
```

### REQUIRED OUTPUT

Propose a Physics difficulty vector, question fingerprint, solution contract, and misconception taxonomy suitable for the Grade 9 system.

---

# 13. RESEARCH STREAM J — CHEMISTRY-SPECIFIC PEDAGOGY

Research chemistry education with emphasis on:

- Johnstone-style macroscopic/particulate/symbolic representations and modern critiques/extensions;
- substance identity;
- particle models;
- conservation;
- symbolic equations;
- evidence -> claim -> reasoning;
- practical-method selection;
- model limitations;
- common alternative conceptions;
- quantitative reasoning at Grade 9 level.

Evaluate the proposed core relationship:

```text
MACROSCOPIC <-> PARTICULATE <-> SYMBOLIC
```

### REQUIRED OUTPUT

Propose a Chemistry difficulty vector, question fingerprint, solution contract, experimental-reasoning schema, and misconception taxonomy suitable for the Grade 9 system.

---

# 14. RESEARCH STREAM K — TEXTBOOK / QUESTION-BANK DESIGN AND LEARNER UX

Research evidence-based textbook and educational-page design for approximately Grade 9 learners.

Investigate:

- multimedia learning principles;
- signaling;
- coherence;
- segmenting;
- spatial contiguity;
- split attention;
- redundancy;
- dual coding (carefully distinguish the popular claim from evidence-based multimedia principles);
- typography;
- line length;
- whitespace;
- visual hierarchy;
- diagram labeling;
- decorative graphics;
- worked-example page design;
- print versus screen reading;
- adolescent readability;
- navigation and cross-references;
- accessibility.

Evaluate the current design preference:

```text
Mission
Spot the Pattern
Toolbox
First Move
Common Trap
Try Now
Level Up
Exit Ticket
Work Zone
```

and the rough page-occupancy heuristic of 70-85% meaningful content.

Determine which parts have research support and which are only design heuristics.

### REQUIRED OUTPUT FOR STREAM K

Provide:

- recommended page archetypes;
- typography/layout guidance;
- purposeful-whitespace guidance;
- diagram-use rules;
- print versus digital differences;
- student textbook versus question-bank differences;
- accessibility checklist;
- recommendations for linked integrated PDFs.

---

# 15. RESEARCH STREAM L — AI CONTENT GENERATION, CORRECTNESS, PROVENANCE, AND COPYRIGHT

Research current evidence and best practices for using generative AI to author educational content.

Investigate:

- hallucination/error rates and failure modes;
- answer verification;
- mathematical/scientific consistency checking;
- source-grounded generation;
- provenance;
- citation integrity;
- synthetic question disclosure;
- copyright-safe transformation;
- benchmark contamination / memorized item risks;
- near-copy detection;
- human-in-the-loop review;
- auditability and versioning.

### REQUIRED OUTPUT

Provide:

- source-authority hierarchy;
- content provenance schema improvements;
- independent verification policy;
- severity classes for errors;
- human-review gates;
- AI-authored item disclosure recommendation;
- copyright/provenance cautions relevant to building question banks from web sources.

---

# 16. CRITICAL REVIEW OF THE CURRENT REPOSITORY

After completing the literature/evidence review, inspect the current Grade 9 repository methodology and produce a **gap analysis**.

For every major current rule, classify it as:

```text
KEEP
KEEP WITH CLARIFICATION
MODIFY
REPLACE
REMOVE
REQUIRES PILOT DATA
```

At minimum review:

- source status taxonomy;
- provenance taxonomy;
- stable concept IDs;
- primary/secondary concept mapping;
- difficulty vectors;
- ±0.4 same-level heuristic;
- +0.8 to +1.3 challenge heuristic;
- Core N policy;
- 20 anchors + 10 calibrated originals pattern;
- NEAR_TWIN / STRUCTURAL_ANALOGUE / CONCEPT_REINFORCEMENT / ADVANCED_TRANSFER;
- progressive hints;
- misconception/error-signature structure;
- mixed mastery;
- linked Concept <-> Practice <-> Challenge architecture;
- canonical master JSON;
- 70-85% page occupancy heuristic;
- publication QA;
- current Mathematics, Physics, and Chemistry adapters.

---

# 17. REQUIRED RESEARCH OUTPUT FORMAT

Return the report in the following structure so it can be consumed directly by a coding/design agent.

## 17.1 Executive findings

Maximum ~2 pages equivalent.

State:

- 10-20 most important findings;
- what the current architecture gets right;
- the highest-risk weaknesses;
- top recommendations.

## 17.2 Evidence matrix

Provide a table with columns:

| ID | Claim / Design Question | Finding | Evidence Strength | Key Sources | Boundary Conditions | Implication for Grade 9 System |
|---|---|---|---|---|---|---|

Use evidence grades:

- `A` strong;
- `B` good;
- `C` promising;
- `D` design hypothesis.

## 17.3 Current-rule review matrix

| Current Rule | Verdict | Evidence | Recommended Replacement/Clarification | Priority |
|---|---|---|---|---|

## 17.4 Recommended methodology v2

Give a complete replacement workflow from source ingestion through publication and empirical calibration.

## 17.5 Revised difficulty model

Provide:

- generic dimensions;
- Math dimensions;
- Physics dimensions;
- Chemistry dimensions;
- scoring method;
- confidence method;
- same-level acceptance method;
- challenge method;
- empirical calibration extension.

## 17.6 Revised question-generation model

Provide exact item relationships/classes, generation workflow, candidate rejection rules, and QA gates.

## 17.7 Revised learning-enrichment model

Provide exact policy for:

- helper;
- hints;
- worked examples;
- misconception diagnostics;
- retries;
- transfer;
- mixed mastery;
- spacing/review.

## 17.8 Subject schemas

Provide separate machine-oriented schema recommendations for Math, Physics, Chemistry.

## 17.9 Publication system

Provide page archetypes and design rules for:

- student textbook;
- question bank;
- challenge appendix;
- teacher edition;
- integrated digital/linked PDF.

## 17.10 Schema change proposals

Give explicit additions/removals/changes for the current master schema.

Use a format such as:

```yaml
change_id: G9-SCHEMA-001
path: concepts[].learning_objectives
operation: ADD
required: true
rationale: "..."
evidence_grade: A
```

## 17.11 Skill-by-skill change plan

For each current skill:

```text
grade9
grade9-source-grounding
grade9-concept-architect
grade9-question-bank
grade9-learning-enrichment
grade9-textbook-publisher
grade9-math
grade9-physics
grade9-chemistry
```

provide:

- KEEP;
- ADD;
- MODIFY;
- REMOVE;
- new validation scripts needed.

Prefer explicit proposed wording/rules where practical.

## 17.12 Deterministic validation roadmap

Identify which checks can be automated, such as:

- schema validation;
- ID uniqueness;
- concept mapping;
- question counts;
- difficulty delta;
- solution completeness;
- numeric verification;
- duplicate detection;
- provenance completeness;
- hint leakage indicators;
- mixed-test balance;
- internal PDF link integrity;
- page-density flags.

Separate deterministic checks from checks that necessarily require expert/LLM judgment.

## 17.13 Pilot and experiment plan

Design a practical validation program using at least:

- one Grade 9 Mathematics chapter;
- one Physics chapter;
- one Chemistry chapter.

Specify:

- hypotheses;
- baseline versus revised approach;
- sample metrics;
- learner evidence to collect;
- minimum useful sample-size caveats;
- qualitative feedback;
- acceptance criteria.

## 17.14 Prioritized implementation backlog

Categorize into:

```text
P0 research-critical / correctness
P1 methodology/schema
P2 validators/tooling
P3 publishing/UX
P4 empirical/adaptive system
```

For each recommendation include:

- effort: S/M/L/XL;
- impact: Low/Medium/High/Critical;
- dependencies;
- evidence grade.

## 17.15 Open research questions

Explicitly list questions for which the literature does not justify a confident rule.

Do not hide uncertainty.

## 17.16 Source bibliography

Provide complete citations and usable source links.

Prioritize DOI, publisher, journal, university, government, professional standard, or official exam/curriculum links.

---

# 18. DIRECT IMPLEMENTATION HANDOFF

The final section must be titled:

# IMPLEMENTATION HANDOFF FOR GRADE 9 SKILL FAMILY

It must contain:

1. **Top 25 changes to implement**, ordered;
2. **Exact files likely affected** in `Grade 9/`;
3. **Proposed new files**;
4. **Master-schema migration list**;
5. **Skill instruction changes**;
6. **Validator/script additions**;
7. **Research findings that should NOT yet be implemented** because evidence is insufficient;
8. **Pilot experiments required before adoption**;
9. **Definition of Done for Methodology v2**.

This handoff should be sufficiently explicit that another agent can implement the recommendations without rereading the full report.

---

# 19. IMPORTANT CONSTRAINTS

- Do not optimize only for examination scores; consider conceptual understanding, retention, and transfer.
- Do not assume more scaffolding is always better.
- Do not assume more difficult-looking algebra means greater cognitive demand.
- Do not assume Bloom/DOK/SOLO scores can substitute directly for psychometric item difficulty.
- Do not present IRT/Rasch-derived claims unless learner-response data exists.
- Do not recommend decorative textbook features merely because they look child-friendly.
- Do not copy large copyrighted question sets.
- Clearly separate sourced exam items, paraphrased examples, and newly authored items.
- Preserve Grade 9 appropriateness while allowing explicitly tagged competitive-foundation/next-level extension.
- Prefer robust principles with documented boundary conditions over rigid universal numeric thresholds.
- Where evidence is weak, recommend a pilot rather than inventing precision.

---

# 20. FINAL STANDARD

The research succeeds only if it tells us not just **what good education research says**, but exactly:

> **What should change in the current Grade 9 schemas, skills, question-generation methods, difficulty calibration, diagnostic logic, and textbook/question-bank publication pipeline—and why?**

## PROMPT END
