# Deep Research R5 — Grade 9 Methodology v2 Synthesis and Implementation Plan

## Purpose

Synthesize the completed R1–R4 research into a coherent, evidence-traceable **Grade 9 Methodology v2 plan**.

This is a professional research-and-engineering synthesis **for a Grade 9 learning system**. It is **not** a Grade 9 student project, school assignment, marking rubric, or lesson-planning exercise.

**Do not implement anything.** Do not edit repository files, skills, schemas, scripts, or PDFs. The purpose is to produce the plan that will be reviewed before implementation authorization.

---

# 1. Frozen repository baseline

Use this exact baseline:

Repository:

`https://github.com/reallaksh19/Common`

Commit:

`cadf66e32dfef5e04c7213d9d1fe45750ee8c08f`

Inspect at minimum:

- `Grade9schema.md`
- `Grade 9/roadmap.md`
- `Grade 9/SKILLSET.md`
- `Grade 9/shared/grade9-workflow.md`
- `Grade 9/shared/grade9-master.schema.json`
- all folders under `Grade 9/skills/`
- current Grade 9 validation scripts;
- Sequence & Series reference implementation/material where useful for regression planning.

Do not silently substitute current `main` for the frozen baseline.

---

# 2. Required research inputs

R5 must consume the **complete outputs** of:

1. R1 — Cognitive Difficulty and Question Engineering;
2. R2 — Learning Sequence, Scaffolding, Diagnostics, Retrieval, and Mastery;
3. R3 — Subject-Specific Pedagogy for Mathematics, Physics, and Chemistry;
4. R4 — Assessment, Publication UX, Accessibility, AI Correctness, Provenance, and Copyright.

The user may provide these reports as files, repository paths, or pasted content.

Before synthesis, create an input-completeness table:

| Research Package | Present? | Evidence Matrix Present? | Durable Bibliography Present? | Handoff Present? | Major Gaps |
|---|---|---|---|---|---|

If a required report is materially incomplete, **do not invent its findings**. Continue only where synthesis is defensible and clearly mark blocked decisions.

---

# 3. Research behavior in R5

R5 is primarily a synthesis task, not another broad literature review.

You may perform targeted external verification only when:

- two R1–R4 reports conflict;
- a critical claim lacks a durable source;
- a current standard has clearly changed;
- a high-impact decision would otherwise rest on an unresolved factual gap.

When you perform targeted verification, mark it as `R5_TARGETED_VERIFICATION` and add durable citations.

Do not use new searches to overwrite well-supported R1–R4 findings merely because an alternative opinion is easy to find.

---

# 4. Central synthesis question

> Given the frozen Grade 9 repository baseline and the evidence from R1–R4, what should Methodology v2 be, which current rules should change, which should remain, which require pilot data, and what exact schema/skill/validator/pilot plan should be approved before implementation?

The synthesis must preserve uncertainty. The goal is not to force every question into a rule.

---

# 5. Build a unified evidence ledger

Normalize R1–R4 evidence into one ledger.

Each record should have at minimum:

```yaml
evidence_id: G9-EVID-###
domain: DIFFICULTY|ITEM_GENERATION|SCAFFOLDING|DIAGNOSTICS|RETRIEVAL|MATH|PHYSICS|CHEMISTRY|ASSESSMENT|UX|ACCESSIBILITY|AI|PROVENANCE|COPYRIGHT
claim: "..."
finding: "..."
evidence_type: EMPIRICAL_EVIDENCE|PROFESSIONAL_STANDARD|LEGAL_OR_POLICY_GUIDANCE|EXPERT_SYNTHESIS|ENGINEERING_INFERENCE
evidence_grade: A|B|C|D
sources:
  - source_id: "..."
    doi: "..."
    url: "..."
boundary_conditions: []
conflicts_with: []
implications: []
```

Do not duplicate the same claim merely because multiple research packages discussed it. Merge supporting evidence and preserve conflicts.

---

# 6. Build a current-rule registry

Identify every important current methodology rule in the baseline repository and assign a stable audit ID.

Suggested families:

```text
G9-SRC-###   source fidelity / QC
G9-PROV-###  provenance
G9-SCOPE-### curriculum / learner scope
G9-CON-###   concepts / prerequisites
G9-DIFF-###  cognitive demand
G9-QB-###    question bank / variants / Core-N
G9-HINT-###  helper / hints / worked examples
G9-DIAG-###  misconceptions / diagnostics
G9-RET-###   retrieval / spacing / mixed mastery
G9-MAST-###  mastery / transfer
G9-ASMT-###  assessment / psychometrics
G9-MATH-###  Mathematics adapter
G9-PHYS-###  Physics adapter
G9-CHEM-###  Chemistry adapter
G9-PUB-###   publication / PDF / UX
G9-A11Y-###  accessibility
G9-AI-###    AI correctness / verification
G9-QA-###    validators / release gates
```

At minimum include all rules explicitly evaluated by R1–R4.

---

# 7. Audit every current rule

For each rule use exactly one verdict:

- `KEEP`
- `KEEP WITH CLARIFICATION`
- `MODIFY`
- `REPLACE`
- `REMOVE`
- `REQUIRES PILOT DATA`

Produce:

| Rule ID | Current Rule | Verdict | Evidence IDs | Proposed v2 Rule | Confidence | Migration Impact | Pilot Required? |
|---|---|---|---|---|---|---|---|

High-impact rules requiring explicit review include at minimum:

- source status taxonomy;
- provenance taxonomy;
- stable concept IDs;
- primary/secondary concept mapping;
- concept/prerequisite graph;
- current difficulty dimensions;
- scalar difficulty weighting;
- `±0.4` same-level heuristic;
- `+0.8 to +1.3` challenge heuristic;
- current question relationship classes;
- Core-N allocation;
- 20-anchor + 10-original pattern;
- helper definition;
- fixed five-level hints;
- fixed reveal percentages;
- worked-example placement;
- misconception/error-signature structure;
- retry/transfer flow;
- concept-visible practice;
- hidden-label mixed mastery;
- mastery interpretation;
- practice/diagnostic/assessment distinction;
- Mathematics adapter;
- Physics adapter;
- Chemistry adapter;
- canonical master JSON authority;
- page vocabulary/archetypes;
- 70–85% occupancy heuristic;
- purposeful whitespace;
- internal PDF links;
- render/preflight QA;
- AI verification;
- source/copyright handling;
- accessibility rules.

---

# 8. Design Methodology v2 before designing schema v2

Do not begin with JSON fields.

First define the end-to-end methodological workflow in prose and diagrams.

A candidate shape may resemble:

```text
SOURCE
 -> source claim extraction
 -> fidelity / QC / provenance
 -> curriculum + learner scope
 -> learning objectives
 -> concept / knowledge-component graph
 -> anchor-item analysis
 -> subject-specific cognitive profile + uncertainty
 -> candidate item generation
 -> structural / scope / solution / ambiguity / duplicate QA
 -> learning sequence
      -> worked example / guided practice as appropriate
      -> independent practice
      -> diagnosis / prerequisite repair
      -> retrieval / spacing / interleaving
      -> transfer / challenge
 -> learner evidence when available
 -> mastery / remediation decision
 -> publication or digital delivery
 -> empirical calibration loop
```

This is illustrative. Replace it where R1–R4 evidence supports a better architecture.

For every stage specify:

- purpose;
- inputs;
- outputs;
- owner skill;
- deterministic checks;
- expert-review checks;
- data required;
- evidence IDs;
- failure states.

---

# 9. Define architecture boundaries

Methodology v2 must preserve clear ownership among skills.

Review and propose final ownership for:

- router/orchestrator;
- source grounding;
- concept architecture;
- question-bank engineering;
- learning enrichment;
- textbook/publication;
- Mathematics adapter;
- Physics adapter;
- Chemistry adapter;
- future assessment/calibration services if needed.

Identify cross-skill contracts and explicitly prevent silent overrides.

If a new specialist skill is justified, propose it but do not create it.

---

# 10. Difficulty and item-generation model v2

Synthesize R1 and R3 into one coherent model.

Provide:

- shared generic dimensions, if any;
- Mathematics dimensions;
- Physics dimensions;
- Chemistry dimensions;
- rating types/scales;
- uncertainty/confidence;
- anchor-to-candidate comparison method;
- same-level acceptance method;
- challenge method;
- transfer-distance representation;
- incidental-difficulty controls;
- question relationship taxonomy;
- candidate rejection rules;
- duplicate/near-duplicate policy;
- Core-N allocation policy;
- boundary between expert pre-calibration and empirical calibration.

If scalar scores remain, state exactly what they may and may not be used for.

---

# 11. Learning-enrichment model v2

Synthesize R2 and R3.

Provide explicit policy for:

- recognition prompts;
- helper;
- worked examples;
- completion/faded examples;
- hints;
- bottom-out hints;
- solution reveal;
- productive struggle/intervention;
- misconception evidence;
- error signatures;
- diagnostic probes;
- repair;
- retry;
- transfer checks;
- feedback;
- retrieval;
- spacing;
- interleaving;
- mixed mastery;
- mastery evidence.

Separate recommendations for:

- print/static;
- linked PDF;
- digital stateful systems.

---

# 12. Subject methodology v2

For Mathematics, Physics, and Chemistry provide final proposed contracts for:

- difficulty representation;
- question fingerprint;
- concept/prerequisite specifics;
- solution contract;
- misconception taxonomy;
- subject-specific QA;
- curriculum-adapter needs;
- competitive-foundation extension policy.

Explicitly show which fields belong to the shared base model and which belong only to subject extensions.

---

# 13. Assessment and empirical-calibration model v2

Synthesize R4 with R1/R2.

Define:

- item purposes;
- practice/diagnostic/assessment separation;
- blueprint requirements;
- pre-empirical metadata;
- learner event schema conceptually;
- observed item statistics;
- conditions for CTT/Rasch/IRT use;
- item revision/retirement;
- score interpretation cautions;
- security/exposure considerations.

Create an explicit table:

| Claim / Metric | Allowed Before Learner Data? | Allowed After Learner Data? | Minimum Conditions | Notes |
|---|---|---|---|---|

---

# 14. Publication and accessibility model v2

Define page/product archetypes for:

- student textbook;
- question bank;
- challenge appendix;
- teacher edition;
- integrated linked PDF;
- screen-first document;
- future digital tutor.

For each define:

- pedagogical purpose;
- required blocks;
- optional blocks;
- solution/hint visibility;
- navigation;
- workspace;
- diagrams;
- accessibility;
- print/screen differences;
- QA.

Resolve the status of the 70–85% occupancy rule explicitly.

Separate:

- evidence-based requirements;
- accessibility/standards requirements;
- design conventions;
- pilot-only hypotheses.

---

# 15. AI, provenance, correctness, and source-use model v2

Define:

- content provenance classes;
- source authority context;
- transformation history;
- AI involvement metadata;
- verification events;
- error severity;
- release-blocking defects;
- independent answer/solution verification;
- source citation requirements;
- durable source ledger;
- copyright/source-use baseline;
- jurisdiction-dependent policy hooks;
- version/audit history.

Make clear which fields are mandatory for all released items.

---

# 16. Master schema migration plan

Only after Methodology v2 is complete, derive the data model changes.

Do **not** edit the existing schema.

Provide explicit migration proposals:

```yaml
change_id: G9-SCHEMA-###
path: "..."
operation: ADD|MODIFY|DEPRECATE|REMOVE|MOVE
current_definition: "..."
proposed_definition: "..."
required: true|false
evidence_ids: []
rationale: "..."
backward_compatibility: "..."
migration_strategy: "..."
pilot_required: true|false
```

Group changes into:

- shared/base schema;
- source/provenance;
- concepts;
- questions;
- difficulty;
- hints/enrichment;
- diagnostics;
- learner evidence/mastery;
- assessment;
- publication;
- QA;
- Mathematics extension;
- Physics extension;
- Chemistry extension.

Identify schema changes that should **not** be made yet.

---

# 17. Skill-by-skill migration plan

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

- current responsibility;
- v2 responsibility;
- `KEEP` instructions;
- `ADD` instructions;
- `MODIFY` instructions;
- `REMOVE/DEPRECATE` instructions;
- new references needed;
- scripts/validators needed;
- cross-skill contracts;
- migration risk.

Where practical, provide proposed wording snippets, but do not edit files.

---

# 18. Deterministic and judgment-based validation roadmap

Create three categories:

## Deterministic

Examples may include:

- schema validity;
- required fields;
- ID uniqueness;
- referential integrity;
- question counts;
- provenance completeness;
- answer presence;
- numeric/algebra checks where computable;
- test blueprint counts;
- PDF destination/link integrity;
- accessibility metadata presence.

## Heuristic / algorithmic

Examples may include:

- lexical similarity;
- structural duplicate flags;
- hint leakage indicators;
- difficulty-profile distance;
- page-density/overflow flags;
- concept coverage balance.

## Expert judgment

Examples may include:

- cognitive equivalence;
- conceptual correctness of explanations;
- misconception validity;
- fairness/construct relevance;
- pedagogical quality;
- diagram adequacy;
- challenge lineage.

For each proposed validator provide:

```yaml
validator_id: G9-VAL-###
name: "..."
type: DETERMINISTIC|HEURISTIC|EXPERT_GATE
inputs: []
outputs: []
release_blocking: true|false
false_positive_risk: LOW|MEDIUM|HIGH
evidence_ids: []
```

---

# 19. Pilot program before broad implementation

Design a pilot comparing baseline methodology with proposed v2.

Use at minimum:

### Mathematics

- Sequence & Series as a regression/reference chapter;
- one geometry chapter such as Triangles.

### Physics

- Motion or another representation-rich Grade 9 chapter.

### Chemistry

- Matter/Particle Model or another representation-rich Grade 9 chapter.

For each pilot define:

- current baseline method;
- proposed v2 method;
- hypotheses;
- artifacts to build;
- expert-review metrics;
- content-quality metrics;
- question-equivalence metrics;
- hint/diagnostic metrics;
- UX/accessibility metrics;
- learner metrics if data become available;
- data/privacy requirements;
- acceptance/rejection criteria;
- minimum sample-size caveats.

Do not invent statistically meaningful sample sizes without justification.

---

# 20. Backward compatibility and migration strategy

The current system already produces usable Grade 9 artifacts. Methodology v2 must not destroy reproducibility casually.

Plan:

- baseline tagging/versioning;
- v1 master-data compatibility;
- deprecation periods;
- migration scripts/converters if required;
- regression fixtures;
- Sequence & Series comparison build;
- dual-run v1/v2 pilot where useful;
- rollback strategy.

Classify each proposed change as:

- backward-compatible;
- migratable;
- breaking;
- pilot-only.

---

# 21. Prioritized backlog

Use:

```text
P0 correctness / research integrity
P1 methodology / schema
P2 skills / validators / tooling
P3 publication / UX / accessibility
P4 empirical / adaptive learner system
```

For each item include:

- backlog ID;
- description;
- evidence IDs;
- priority;
- effort S/M/L/XL;
- impact Low/Medium/High/Critical;
- dependencies;
- affected files;
- pilot required?;
- implementation risk.

Do not prioritize visual polish ahead of correctness, provenance, construct validity, or methodology integrity.

---

# 22. Decisions that must remain unimplemented

Create a dedicated list of recommendations that must **not** be implemented yet because:

- evidence is weak;
- R1–R4 conflict;
- learner data are required;
- curriculum scope is unresolved;
- legal jurisdiction matters;
- pilot evidence is required;
- implementation would create excessive migration risk.

For each state the evidence needed to unlock it.

---

# 23. Definition of Done for Methodology v2 planning

Define planning completion separately from implementation completion.

At minimum, planning is complete only when:

- R1–R4 inputs are accounted for;
- evidence ledger is normalized;
- current-rule registry is complete;
- every major current rule has a verdict;
- Methodology v2 workflow is explicit;
- subject contracts are explicit;
- assessment boundaries are explicit;
- publication/accessibility contract is explicit;
- AI/provenance contract is explicit;
- schema migration proposals are complete;
- skill migration proposals are complete;
- validator roadmap is complete;
- pilot plan is complete;
- backward compatibility is addressed;
- unresolved questions remain visible;
- no code or repository methodology files have been changed.

---

# 24. Required output format

Return exactly these sections:

## R5.1 Executive decision summary

Maximum 2 pages equivalent.

## R5.2 Research-input completeness and conflict report

## R5.3 Unified evidence ledger

## R5.4 Current-rule registry

## R5.5 Current-rule verdict matrix

## R5.6 Methodology v2 end-to-end workflow

## R5.7 Architecture and skill ownership model

## R5.8 Difficulty and question-engineering model v2

## R5.9 Learning-enrichment/diagnostic/mastery model v2

## R5.10 Mathematics methodology v2

## R5.11 Physics methodology v2

## R5.12 Chemistry methodology v2

## R5.13 Assessment and empirical-calibration model v2

## R5.14 Publication/accessibility model v2

## R5.15 AI/provenance/source-use model v2

## R5.16 Master-schema migration proposals

## R5.17 Skill-by-skill migration plan

## R5.18 Validator roadmap

## R5.19 Pilot program

## R5.20 Backward-compatibility and migration strategy

## R5.21 Prioritized backlog

## R5.22 Do-not-implement-yet register

## R5.23 Open research questions

## R5.24 Definition of Done for Methodology v2 planning

## R5.25 Durable bibliography/source ledger

---

# 25. Mandatory implementation handoff

End with exactly this heading:

# IMPLEMENTATION HANDOFF FOR GRADE 9 METHODOLOGY v2 — PLAN ONLY

Include:

1. top 25 proposed changes, ordered;
2. exact current files likely affected;
3. proposed new files;
4. schema migration list;
5. skill instruction changes;
6. validator/script additions;
7. migration/backward-compatibility actions;
8. findings safe to implement after approval;
9. findings requiring pilot data;
10. findings requiring learner data;
11. findings requiring curriculum-specific decisions;
12. findings requiring legal/jurisdiction review;
13. pilot experiments required;
14. proposed implementation phases;
15. explicit statement: **NO IMPLEMENTATION HAS BEEN PERFORMED**.

---

# 26. Important constraints

- Do not implement or edit repository methodology files.
- Do not turn this into a student project.
- Do not suppress conflicts among R1–R4.
- Do not convert low-confidence evidence into hard rules.
- Do not claim psychometric properties without appropriate data.
- Do not force Math, Physics, and Chemistry into one identical cognitive model.
- Do not design schema fields before defining the methodology they serve.
- Do not replace useful legacy heuristics without a migration/pilot plan when evidence is incomplete.
- Do not treat page aesthetics as more important than learning function or accessibility.
- Do not make global copyright/legal claims from one jurisdiction.
- Preserve durable provenance for every high-impact recommendation.

---

# 27. Final success standard

R5 succeeds only if an implementation agent can later answer, without rereading all research papers:

> What exactly should change in the Grade 9 methodology, why should it change, which evidence supports the change, what remains uncertain, which files will be affected, how will compatibility be preserved, what must be piloted, and what must not yet be implemented?
