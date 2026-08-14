# Deep Research R1 — Cognitive Difficulty and Question Engineering

## Purpose

Research and design a defensible **pre-empirical difficulty-calibration and question-engineering methodology** for the Grade 9 learning system.

This is professional research **for Grade 9 learners**. The researcher is an expert multidisciplinary team. **Do not convert this into a Grade 9 student project, school assignment, marking rubric, or classroom research capstone.**

Do not implement repository changes. Produce research evidence and an implementation-ready design proposal for later synthesis in R5.

---

# 1. Frozen repository baseline

Evaluate the repository at this exact commit:

`cadf66e32dfef5e04c7213d9d1fe45750ee8c08f`

Repository:

`https://github.com/reallaksh19/Common`

Inspect at minimum:

- `Grade9schema.md`
- `Grade 9/roadmap.md`
- `Grade 9/SKILLSET.md`
- `Grade 9/shared/grade9-workflow.md`
- `Grade 9/shared/grade9-master.schema.json`
- `Grade 9/skills/grade9-question-bank/`
- `Grade 9/skills/grade9-math/`
- `Grade 9/skills/grade9-physics/`
- `Grade 9/skills/grade9-chemistry/`

Also inspect any current Sequence & Series reference material in the repository if useful for concrete item comparisons.

Current rules are hypotheses to test, not facts. In particular evaluate:

- multidimensional difficulty profiles;
- the Mathematics scalar composite currently used as a screening aid;
- same-level screen around `anchor ±0.4`;
- challenge target around `anchor +0.8 to +1.3`;
- `NEAR_TWIN`, `STRUCTURAL_ANALOGUE`, `CONCEPT_REINFORCEMENT`, `ADVANCED_TRANSFER`;
- Core-N allocation, including the 20-anchor + 10-original pattern when Core 30 is requested;
- the principle that harder questions should increase synthesis/recognition rather than merely calculation burden.

---

# 2. Central research question

> How should the Grade 9 system estimate and compare cognitive demand **before learner-response data exist**, generate same-level and harder questions that preserve deep structure without superficial duplication, and express uncertainty honestly until empirical calibration becomes possible?

The final output must be usable by R5 to design Methodology v2.

---

# 3. Evidence requirements

Prioritize:

1. peer-reviewed systematic reviews and meta-analyses;
2. primary research on problem solving, transfer, cognitive demand, item generation, item-writing and assessment;
3. authoritative psychometric and educational-testing standards;
4. mathematics/science education research;
5. official released-item frameworks and item specifications where they illuminate item demand;
6. research on generative or automatic item generation only where methodologically relevant.

Do not rely on commercial tutoring blogs or SEO summaries for major conclusions.

For every major claim distinguish:

- `EMPIRICAL_EVIDENCE`
- `PROFESSIONAL_STANDARD`
- `EXPERT_SYNTHESIS`
- `ENGINEERING_INFERENCE`

Use durable citations. For each important source provide, where available:

- authors/organization;
- year;
- title;
- journal/publisher/standard body;
- DOI;
- stable official URL.

ChatGPT citation handles alone are not sufficient repository provenance.

---

# 4. Research stream R1-A — What creates item difficulty?

Investigate which factors can reasonably be judged by experts before field data exist, including:

- conceptual demand;
- prerequisite load;
- hidden-structure recognition;
- model/method selection;
- number and dependency of meaningful reasoning steps;
- working-memory burden;
- representational translation;
- abstraction;
- symbolic/algebraic manipulation;
- numerical/calculation burden;
- constraints and case analysis;
- novelty;
- near versus far transfer;
- linguistic/reading demand;
- diagram/graph interpretation;
- distractor plausibility;
- answer-format effects;
- time pressure.

Separate **construct-relevant cognitive demand** from incidental difficulty caused by wording, arithmetic clutter, notation, poor diagrams, or ambiguity.

Compare and clearly distinguish:

- expert-rated cognitive demand;
- Bloom/revised Bloom;
- Webb DOK;
- SOLO;
- other subject-specific cognitive-demand frameworks;
- Classical Test Theory item difficulty;
- Rasch/IRT item parameters.

Do not treat these as interchangeable.

### Required R1-A output

Propose:

1. a generic pre-empirical difficulty representation;
2. which dimensions should be subject-specific rather than generic;
3. whether dimensions should be ordinal, interval-like, categorical, or mixed;
4. whether fixed weights are defensible;
5. how uncertainty/confidence should be stored;
6. what claims must be deferred until learner data exist.

---

# 5. Research stream R1-B — Anchor-to-candidate cognitive equivalence

Research how a newly authored item should be compared with a source anchor.

The system must distinguish:

- same concept but easier cueing;
- same concept but greater computation;
- same solution engine with changed surface context;
- same structural schema with changed representation;
- additional prerequisite or inference;
- genuine transfer;
- accidental difficulty due to language or ambiguity.

Evaluate whether a scalar distance threshold is useful at all.

### Required R1-B output

Design an explicit comparison protocol containing at minimum:

- concept/mechanism match;
- expert solution-path comparison;
- recognition/method-selection comparison;
- representation comparison;
- prerequisite comparison;
- reasoning dependency comparison;
- constraint/case comparison;
- calculation burden comparison;
- language/diagram demand comparison;
- transfer-distance comparison;
- uncertainty/confidence.

Define outcomes such as:

- `EQUIVALENT_FOR_PRACTICE`
- `EQUIVALENT_WITH_CAVEAT`
- `EASIER_REINFORCEMENT`
- `HARDER_SAME_LINEAGE`
- `TRANSFER_EXTENSION`
- `REJECT_DIFFERENT_CONSTRUCT`
- `REJECT_AMBIGUOUS_OR_DEFECTIVE`

You may recommend different names, but the operational distinctions must be clear.

Test the current `±0.4` same-level rule. State whether it should be kept, demoted to a local heuristic, replaced, or piloted.

---

# 6. Research stream R1-C — Challenge construction

Research what makes a legitimate next-level item.

Evaluate increases in difficulty through:

- reduced cueing;
- hidden representation;
- one additional inference;
- interacting constraints;
- changed representation;
- less direct target;
- cross-concept synthesis;
- farther transfer.

Distinguish these from artificial difficulty through long arithmetic, ugly coefficients, obscure wording, or unnecessary expansion.

Test the current `+0.8 to +1.3` challenge heuristic.

### Required R1-C output

Provide a challenge-construction rubric with:

- lineage requirements;
- acceptable difficulty transformations;
- rejection rules;
- transfer-distance labels;
- uncertainty fields;
- examples of strong and weak challenge transformations.

---

# 7. Research stream R1-D — Question-generation taxonomy

Research isomorphic items, structural analogues, schema-based generation, near/far transfer, template-based item generation and controlled generative authoring.

Critically review the current relationship classes:

```text
NEAR_TWIN
STRUCTURAL_ANALOGUE
CONCEPT_REINFORCEMENT
ADVANCED_TRANSFER
```

Determine whether they should be retained, renamed, subdivided, or replaced.

A useful taxonomy must describe **what changed in the problem representation or reasoning**, not merely how visually similar the questions appear.

### Required R1-D output

For every recommended class provide:

- definition;
- allowed transformations;
- prohibited transformations;
- intended learning purpose;
- expected transfer distance;
- example;
- common failure mode.

---

# 8. Research stream R1-E — Item authoring and QA

Research item-writing quality for constructed-response and multiple-choice items, including:

- unambiguous stems;
- solution uniqueness;
- parameter selection;
- accidental degeneracy;
- unintended shortcuts;
- answer-format effects;
- misconception-based distractors;
- distractor plausibility;
- curriculum/scope drift;
- bias/fairness concerns;
- excessive language demand;
- diagram dependence;
- adversarial review;
- independent answer verification.

### Required R1-E output

Produce an item QA gate sequence such as:

```text
construct intent
-> scope/prerequisite check
-> structural transformation check
-> solve independently
-> ambiguity/degeneracy check
-> difficulty comparison
-> duplicate check
-> provenance check
-> release decision
```

Define which gates can later be deterministic and which require expert judgment.

---

# 9. Research stream R1-F — Near-duplicate and overfitting control

Research how repeated practice can become superficial pattern matching.

Investigate:

- lexical similarity;
- mathematical structural similarity;
- semantic similarity;
- solution-path similarity;
- representation reuse;
- numeric-only variation;
- repeated cueing;
- overexposure to one problem template.

### Required R1-F output

Propose a duplicate/near-duplicate policy with at least three layers:

1. surface similarity;
2. structural/solution similarity;
3. pedagogical redundancy.

Do not pretend an embedding threshold alone can establish pedagogical distinctness.

---

# 10. Research stream R1-G — Core-N allocation

The system may have many anchor concepts but a limited bank size.

Research how additional authored practice should be allocated when N is constrained.

Consider:

- source coverage;
- prerequisite centrality;
- misconception risk;
- recognition demand;
- transfer importance;
- concept difficulty uncertainty;
- breadth versus depth;
- diminishing returns from repeated same-schema variants.

Critically evaluate mechanical equal allocation and the existing pattern of allocating extras to concepts with greater practice need.

### Required R1-G output

Provide a practical Core-N allocation policy or scoring rubric. If no research supports a universal formula, provide a transparent decision procedure rather than invented precision.

---

# 11. Worked examples required

Use at least:

- two Mathematics anchor/candidate comparisons;
- one Physics comparison;
- one Chemistry comparison.

At least one example must demonstrate why two items with similar apparent difficulty are **not** cognitively equivalent.

At least one must demonstrate a strong same-level transformation.

At least one must demonstrate a legitimate next-level challenge.

Use released/official or fully traceable examples where possible. Do not copy large copyrighted sets.

---

# 12. Current-rule audit required from R1

Audit only the rules within R1 scope using:

- `KEEP`
- `KEEP WITH CLARIFICATION`
- `MODIFY`
- `REPLACE`
- `REMOVE`
- `REQUIRES PILOT DATA`

At minimum review:

- multidimensional difficulty;
- current generic Mathematics difficulty vector;
- scalar composite weighting;
- `±0.4` same-level screen;
- `+0.8 to +1.3` challenge target;
- current four relationship classes;
- Core-N allocation;
- 20-anchor + 10-original default pattern;
- synthesis-over-arithmetic challenge principle;
- current difficulty checker logic.

---

# 13. Required output format

Return exactly these sections:

## R1.1 Executive findings

10–15 findings maximum.

## R1.2 Evidence matrix

| Evidence ID | Claim / Design Question | Finding | Evidence Type | Grade A-D | Durable Sources | Boundary Conditions | Grade 9 Implication |
|---|---|---|---|---|---|---|---|

## R1.3 Definitions and construct boundaries

Define expert cognitive demand, empirical item difficulty, transfer distance, structural equivalence and incidental difficulty.

## R1.4 Recommended pre-empirical difficulty model

Generic model plus notes on subject specialization.

## R1.5 Anchor-to-candidate comparison protocol

Provide a field-level rubric that can later become schema/skill rules.

## R1.6 Same-level acceptance policy

Include rejection and uncertainty rules.

## R1.7 Challenge-construction policy

## R1.8 Question relationship taxonomy v2

## R1.9 Item-authoring and QA workflow

## R1.10 Duplicate/near-duplicate policy

## R1.11 Core-N allocation policy

## R1.12 Worked examples

## R1.13 Current-rule verdict matrix

| Current Rule | Verdict | Evidence IDs | Replacement/Clarification | Confidence | Pilot Needed? |
|---|---|---|---|---|---|

## R1.14 Candidate schema implications for R5

Do not edit schemas. List proposed fields only, e.g.:

```yaml
proposal_id: R1-SCHEMA-001
path: questions[].difficulty_estimate
operation: ADD_OR_REPLACE
rationale: "..."
evidence_ids: []
confidence: HIGH|MEDIUM|LOW
pilot_required: true|false
```

## R1.15 Candidate validator implications for R5

Separate:

- deterministic checks;
- probabilistic/heuristic checks;
- expert-review gates.

## R1.16 Open questions and required pilots

## R1.17 Durable bibliography/source ledger

No session-only citations.

---

# 14. Important constraints

- Do not implement code or modify repository files.
- Do not turn this into a student project.
- Do not claim psychometric calibration without learner-response data.
- Do not invent precise thresholds because they are convenient.
- Do not equate algebra length or arithmetic burden with cognitive demand.
- Do not assume Bloom/DOK/SOLO are item-difficulty scales.
- Do not recommend many variants simply because generation is cheap.
- Do not copy copyrighted question banks at scale.
- Preserve uncertainty explicitly.

---

# 15. Final handoff block

End with:

# R1 HANDOFF TO METHODOLOGY-v2 SYNTHESIS

Include:

1. top 10 R1 decisions;
2. current rules most likely to change;
3. proposed replacement rules;
4. fields R5 should consider for the master schema;
5. validator candidates;
6. recommendations safe to adopt from evidence alone;
7. recommendations requiring pilot data;
8. unresolved questions R5 must preserve.
