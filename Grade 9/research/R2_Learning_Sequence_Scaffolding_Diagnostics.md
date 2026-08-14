# Deep Research R2 — Learning Sequence, Scaffolding, Diagnostics, Retrieval, and Mastery

## Purpose

Research and design the **learning-enrichment and practice-sequencing methodology** for the Grade 9 system.

This is professional methodology research **for Grade 9 learners**. The researcher is an expert multidisciplinary team. **Do not convert this task into a Grade 9 student project, school assignment, marking rubric, lesson-plan exercise, or teacher-supervision schedule.**

Do not implement repository changes. Produce evidence and explicit design proposals for later synthesis in R5.

---

# 1. Frozen repository baseline

Evaluate:

`https://github.com/reallaksh19/Common`

at commit:

`cadf66e32dfef5e04c7213d9d1fe45750ee8c08f`

Inspect at minimum:

- `Grade9schema.md`
- `Grade 9/roadmap.md`
- `Grade 9/shared/grade9-workflow.md`
- `Grade 9/shared/grade9-master.schema.json`
- `Grade 9/skills/grade9-learning-enrichment/`
- `Grade 9/skills/grade9-concept-architect/`
- `Grade 9/skills/grade9-question-bank/`
- `Grade 9/skills/grade9-textbook-publisher/`
- subject adapters where subject-specific examples are required.

Current patterns to evaluate include:

- concept-first learning;
- `What should I notice?` / recognition prompts;
- helper versus progressive hints;
- five-level hint patterns such as direction → concept → connection → setup → near-solution;
- fixed reveal percentages such as 10/25/45/70/90 where present;
- worked solutions and transfer questions;
- misconception → error signature → diagnostic probe → repair → retry → transfer;
- concept-visible practice followed by mixed mastery with concept labels hidden;
- mastery judgments based on correctness, hint usage, retries, transfer, and later retention where available.

Treat all current rules as hypotheses to evaluate.

---

# 2. Central research question

> What evidence-based sequence of examples, guided practice, hints, diagnostics, retrieval, spacing, interleaving, retries, and transfer should a reusable Grade 9 learning system use so that support improves learning without creating dependency, answer leakage, or false claims of mastery?

The output must be sufficiently explicit for R5 to derive Methodology v2 rules, schema changes, skill changes, and pilot tests.

---

# 3. Evidence requirements

Prioritize:

1. meta-analyses and systematic reviews on worked examples, retrieval, spacing, interleaving, feedback and scaffolding;
2. primary cognitive and educational research on example-problem sequencing, fading, self-explanation, productive struggle and feedback timing;
3. mathematics/science education research on misconceptions and diagnostic teaching;
4. authoritative practice guides and professional research syntheses;
5. relevant intelligent-tutoring / hint-system research, with caution about context and learner population.

For each important claim distinguish:

- `EMPIRICAL_EVIDENCE`
- `PROFESSIONAL_GUIDANCE`
- `EXPERT_SYNTHESIS`
- `ENGINEERING_INFERENCE`

Use durable citations: DOI, journal/publisher URL, government/professional organization URL, or other stable source. Do not rely only on session citation handles.

---

# 4. Research stream R2-A — Worked examples and example-to-problem sequencing

Research:

- worked-example effect;
- example-problem pairs;
- completion problems;
- faded worked examples;
- self-explanation prompts;
- expertise-reversal effect;
- novice versus more knowledgeable learners;
- blocked examples versus varied examples;
- when to expose solution steps;
- when to require generation before seeing a worked solution;
- example comparison / contrasting cases where relevant.

### Required R2-A output

Propose a practical sequence for different learner states, for example:

```text
NOVICE
worked example
-> completion problem
-> guided problem
-> independent same-level problem
-> mixed retrieval

DEVELOPING
brief reminder/example
-> independent problem
-> targeted hint only if needed
-> transfer

CONFIDENT
independent mixed problem
-> delayed retrieval
-> challenge/transfer
```

Do not accept this example blindly. Replace it with the evidence-supported version.

Specify:

- when a worked example is preferred;
- when it should be faded;
- when a full solution should be hidden;
- whether example/problem interleaving is recommended;
- what information a learner-state model would need.

---

# 5. Research stream R2-B — Helper versus hint

Define the distinction between:

- recognition prompt;
- helper;
- hint;
- partial setup;
- worked step;
- full solution.

Research how much assistance should be provided and when.

Critically evaluate the current idea that a helper should point attention without exposing the setup, while progressive hints reveal increasingly more of the path.

### Required R2-B output

Provide:

1. operational definitions;
2. allowed content in each assistance type;
3. reveal boundaries;
4. learner-state-dependent rules;
5. when to skip early hints;
6. when a worked example is better than many hints;
7. when assistance should trigger a prerequisite repair instead of another hint.

---

# 6. Research stream R2-C — Progressive hints and hint leakage

Research:

- progressive hint systems;
- bottom-out hints;
- hint abuse / gaming where relevant;
- feedback specificity;
- metacognitive prompts;
- motivational costs and benefits;
- expertise effects;
- delayed versus immediate assistance.

Critically evaluate:

```text
H1 direction
H2 concept
H3 connection/representation
H4 setup
H5 near-solution
```

and fixed percentage reveal scores such as:

```text
10 / 25 / 45 / 70 / 90
```

### Required R2-C output

Recommend:

- fixed or variable number of hint stages;
- stage types;
- whether numeric reveal percentages should be removed, retained only as internal labels, or empirically calibrated;
- hint leakage rubric;
- rules for bottom-out hints;
- whether hint use should affect mastery interpretation;
- what can be automated versus judged by experts.

---

# 7. Research stream R2-D — Productive struggle and intervention timing

Research what evidence supports allowing struggle before assistance and where this becomes counterproductive.

Investigate:

- productive failure;
- desirable difficulty;
- cognitive overload;
- prerequisite absence;
- frustration and disengagement;
- when prior generation attempts aid later instruction;
- interaction with learner expertise.

### Required R2-D output

Provide a decision framework such as:

```text
incorrect attempt
-> classify likely cause
   -> missing prerequisite
   -> wrong model / misconception
   -> strategy-selection failure
   -> execution slip
   -> insufficient persistence / incomplete attempt
-> choose intervention
```

Do not impose universal time-to-hint thresholds unless evidence supports them.

---

# 8. Research stream R2-E — Misconceptions, slips, and error signatures

Research subject-learning literature on misconceptions and diagnostic assessment.

The system needs to distinguish at least:

- persistent wrong conceptual model;
- overgeneralized rule;
- representation error;
- procedural error;
- arithmetic/calculation slip;
- reading/interpretation error;
- incomplete prerequisite;
- random/low-confidence guess where detectable.

Evaluate the current structure:

```text
wrong model
-> observable error signature
-> diagnostic probe
-> repair explanation / micro-example
-> retry
-> transfer check
```

### Required R2-E output

Propose:

- misconception object schema conceptually;
- error-signature fields;
- diagnostic confidence levels;
- evidence required before labeling a misconception;
- rules preventing one wrong answer from being overdiagnosed;
- diagnostic probe principles;
- repair workflow;
- retry and transfer criteria.

Include Math, Physics, and Chemistry examples, but leave detailed subject taxonomies to R3.

---

# 9. Research stream R2-F — Feedback design

Research:

- correctness-only feedback;
- knowledge-of-correct-response feedback;
- explanatory feedback;
- elaborated feedback;
- immediate versus delayed feedback;
- feedback after constructed response versus MCQ;
- feedback that addresses misconception versus procedure;
- confidence judgments.

### Required R2-F output

Define feedback modes for:

- learning/practice;
- diagnosis;
- mixed retrieval;
- transfer/challenge;
- formal assessment.

Specify what should and should not be shown immediately in each mode.

---

# 10. Research stream R2-G — Retrieval practice and delayed review

Research:

- testing effect / retrieval practice;
- retrieval success versus retrieval difficulty;
- corrective feedback after retrieval;
- repeated retrieval;
- delayed retesting;
- cumulative review;
- transfer retrieval.

### Required R2-G output

Propose principles for:

- first retrieval after learning;
- repeated retrieval;
- delayed review;
- failure handling;
- concept mixing;
- retention evidence.

Avoid inventing fixed day schedules unless literature supports context-appropriate ranges. If exact timing depends on curriculum cadence, provide principles and parameterized windows rather than universal dates.

---

# 11. Research stream R2-H — Spacing and interleaving

Research:

- spacing effect;
- expanding versus fixed intervals where relevant;
- blocked versus interleaved practice;
- category discrimination;
- contextual interference;
- learner expertise;
- task similarity;
- when interleaving helps method selection versus when it overwhelms novices.

Evaluate the existing sequence:

```text
learn by concept
-> practice with concept visible
-> mixed mastery with concept hidden
-> diagnosis back to concept
```

### Required R2-H output

Recommend:

- when concept labels should be visible;
- when they should be hidden;
- how quickly mixed practice should begin;
- how mixed sets should be constructed;
- whether blocked-to-interleaved progression is supported;
- how to avoid mixing items that introduce new prerequisites accidentally;
- print versus digital differences.

If no universal blocked/interleaved ratio is defensible, explicitly say so.

---

# 12. Research stream R2-I — Mastery, retention, and transfer

Research what evidence can support a practical learning-system definition of mastery.

Distinguish:

- immediate correctness;
- independent correctness;
- correctness after hints;
- repeated correctness;
- delayed retention;
- near transfer;
- far transfer;
- challenge performance.

Do not equate one correct answer with mastery.

### Required R2-I output

Propose a mastery-evidence model that may include evidence states such as:

```text
NOT_YET_EVIDENCED
GUIDED_SUCCESS
INDEPENDENT_SUCCESS
REPEATED_SUCCESS
DELAYED_RETENTION
TRANSFER_EVIDENCE
```

These names are illustrative, not mandatory.

Specify:

- what evidence each state requires;
- how hint usage affects interpretation;
- how misconceptions affect mastery;
- when a concept should be revisited;
- what cannot be inferred without longitudinal learner data.

---

# 13. Research stream R2-J — Printed textbook versus digital tutor

The current Grade 9 system publishes PDFs but may later support adaptive digital learning.

Research which learning-sequence features can be expressed in print and which require interaction/state.

### Required R2-J output

Separate recommendations into:

- `PRINT_STATIC`
- `LINKED_PDF`
- `DIGITAL_STATEFUL`

For example, a printed book can sequence examples and mixed sets, but cannot truly adapt hint order to learner state without learner choice.

Identify where publication design must avoid pretending to be adaptive.

---

# 14. Worked examples required

Provide at least:

- one Mathematics worked-example/fading sequence;
- one Physics diagnostic misconception sequence;
- one Chemistry representation/misconception repair sequence;
- one mixed-practice construction example;
- one example showing why too much help can reduce diagnostic value or independent retrieval.

Use traceable sources for claims. Authored examples may be original but must be labeled as such.

---

# 15. Current-rule audit required from R2

Audit at minimum:

- `What should I notice?` recognition layer;
- helper definition;
- fixed five-level hints;
- fixed hint reveal percentages;
- solution-reveal placement;
- worked-example placement;
- misconception/error-signature structure;
- immediate retry;
- delayed transfer check;
- concept-visible practice;
- hidden-label mixed mastery;
- use of hint consumption as mastery evidence;
- current transfer-question policy.

Use verdicts:

- `KEEP`
- `KEEP WITH CLARIFICATION`
- `MODIFY`
- `REPLACE`
- `REMOVE`
- `REQUIRES PILOT DATA`

---

# 16. Required output format

Return exactly these sections:

## R2.1 Executive findings

10–15 findings maximum.

## R2.2 Evidence matrix

| Evidence ID | Claim / Design Question | Finding | Evidence Type | Grade A-D | Durable Sources | Boundary Conditions | Grade 9 Implication |
|---|---|---|---|---|---|---|---|

## R2.3 Learning-sequence model

Provide the recommended learner journey from initial instruction to delayed transfer.

## R2.4 Worked-example and fading policy

## R2.5 Helper/hint/solution taxonomy

## R2.6 Hint policy and leakage rubric

## R2.7 Productive-struggle/intervention decision framework

## R2.8 Misconception and diagnostic model

## R2.9 Feedback policy

## R2.10 Retrieval/spacing/interleaving policy

## R2.11 Mastery-evidence model

## R2.12 Print vs linked-PDF vs digital-stateful contract

## R2.13 Worked examples

## R2.14 Current-rule verdict matrix

| Current Rule | Verdict | Evidence IDs | Replacement/Clarification | Confidence | Pilot Needed? |
|---|---|---|---|---|---|

## R2.15 Candidate schema implications for R5

Use proposal records only; do not edit schemas.

## R2.16 Candidate skill implications for R5

Identify likely changes to:

- `grade9-learning-enrichment`;
- `grade9-question-bank`;
- `grade9-concept-architect`;
- `grade9-textbook-publisher`;
- subject adapters where relevant.

## R2.17 Candidate validator implications for R5

Separate deterministic, heuristic, and expert-review checks.

## R2.18 Open questions and pilots

## R2.19 Durable bibliography/source ledger

---

# 17. Important constraints

- Do not implement code or modify repository files.
- Do not turn this into a student project.
- Do not assume more scaffolding is always better.
- Do not assign a misconception from one wrong answer without evidence.
- Do not define mastery as immediate correctness alone.
- Do not invent universal spacing schedules or hint counts when evidence is context-dependent.
- Preserve distinctions among learning, diagnosis, retrieval, transfer, and assessment.
- Preserve uncertainty and boundary conditions.

---

# 18. Final handoff block

End with:

# R2 HANDOFF TO METHODOLOGY-v2 SYNTHESIS

Include:

1. top 10 R2 decisions;
2. current rules most likely to change;
3. evidence-supported replacement rules;
4. proposed learner-state/mastery fields for R5 consideration;
5. diagnostic fields for R5 consideration;
6. validator candidates;
7. print-only versus digital-only recommendations;
8. recommendations safe to adopt from evidence alone;
9. recommendations requiring pilots;
10. unresolved questions R5 must preserve.
