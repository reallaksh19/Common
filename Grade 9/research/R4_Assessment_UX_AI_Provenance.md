# Deep Research R4 — Assessment, Publication UX, Accessibility, AI Correctness, Provenance, and Copyright

## Purpose

Research the Grade 9 system’s **assessment contract, publication design, accessibility, AI-content validation, provenance, auditability, and copyright-safe authoring rules**.

This is professional methodology research **for a Grade 9 learning system**. The researcher is an expert multidisciplinary team. **Do not convert this task into a Grade 9 student project, school assignment, teacher-supervised capstone, marking rubric, or classroom activity.**

Do not implement repository changes. Produce evidence and design proposals for later synthesis in R5.

---

# 1. Frozen repository baseline

Evaluate:

`https://github.com/reallaksh19/Common`

at commit:

`cadf66e32dfef5e04c7213d9d1fe45750ee8c08f`

Inspect at minimum:

- `Grade9schema.md`
- `Grade 9/roadmap.md`
- `Grade 9/SKILLSET.md`
- `Grade 9/shared/grade9-workflow.md`
- `Grade 9/shared/grade9-master.schema.json`
- `Grade 9/skills/grade9-source-grounding/`
- `Grade 9/skills/grade9-question-bank/`
- `Grade 9/skills/grade9-learning-enrichment/`
- `Grade 9/skills/grade9-textbook-publisher/`
- subject adapters where subject examples are relevant.

Current practices to evaluate include:

- source-status and provenance classes;
- source-grounded versus original-calibrated content;
- practice/question-bank use without pretending psychometric calibration;
- canonical master JSON as authority;
- linked textbook/question-bank/integrated PDF architecture;
- internal PDF navigation;
- page vocabulary such as Mission / Spot the Pattern / Toolbox / First Move / Common Trap / Try Now / Level Up / Exit Ticket / Work Zone;
- purposeful-whitespace policy;
- rough 70–85% meaningful page-occupancy heuristic;
- page rendering and link QA;
- AI-assisted authoring with independent checking.

Treat current numeric or visual heuristics as hypotheses unless evidence supports them.

---

# 2. Central research question

> What standards and evidence should govern the Grade 9 system when it moves from learning content to practice, diagnosis, assessment, print/digital publication, and AI-assisted generation—so that score interpretations remain valid, pages remain usable and accessible, and every released item remains correct, traceable, auditable, and copyright-conscious?

The output must be sufficiently explicit for R5 to derive Methodology v2 rules, schema migrations, skill changes, validators, and pilot requirements.

---

# 3. Evidence requirements

Prioritize:

1. authoritative testing/measurement standards;
2. peer-reviewed assessment and psychometric research;
3. authoritative accessibility standards and research;
4. multimedia-learning, cognitive-load, instructional-design, typography/readability and digital-reading research;
5. authoritative AI-in-education guidance and empirical research on model failure modes;
6. copyright offices, legislation/guidance, licensing authorities, and publisher policies where relevant;
7. official exam/curriculum sources for secure-versus-released item practices.

For each important claim distinguish:

- `EMPIRICAL_EVIDENCE`
- `PROFESSIONAL_STANDARD`
- `LEGAL_OR_POLICY_GUIDANCE`
- `EXPERT_SYNTHESIS`
- `ENGINEERING_INFERENCE`

Use durable citations with DOI, journal/publisher URL, government/professional body URL, or official legal/policy URL. Session citation handles alone are insufficient.

Where law is jurisdiction-dependent, say so explicitly. Do not convert one jurisdiction’s rules into universal legal advice.

---

# 4. Research stream R4-A — Practice, diagnostic, and assessment purposes

Research the distinction among:

- learning/practice items;
- formative checks;
- diagnostic probes;
- mastery checks;
- classroom/summative assessments;
- competition/foundation extension;
- research/pilot items.

Investigate how intended use affects:

- item construction;
- feedback availability;
- hints/solutions;
- exposure/reuse;
- blueprint requirements;
- score interpretation;
- item security;
- validity evidence.

### Required R4-A output

Propose an explicit item-purpose model, for example:

```text
LEARN
PRACTICE
DIAGNOSTIC
RETRIEVAL
TRANSFER
CHALLENGE
ASSESSMENT
PILOT
```

These labels are illustrative. Recommend the final set and define each operationally.

For each purpose specify:

- whether hints are allowed;
- whether immediate feedback is allowed;
- whether concept labels may be visible;
- whether items may be reused;
- what score interpretations are legitimate;
- what validation level is required.

---

# 5. Research stream R4-B — Validity, reliability, and psychometric boundaries

Research:

- validity and validation;
- reliability/precision;
- fairness;
- item difficulty and discrimination;
- distractor functioning;
- local dependence;
- test blueprints;
- content representativeness;
- standard setting;
- score interpretation;
- Classical Test Theory;
- Rasch/IRT;
- small-sample limitations;
- test security/exposure.

### Required R4-B output

Clearly separate what the system can claim:

### Before learner-response data

Possible examples:

- expert cognitive-demand estimate;
- curriculum/content alignment;
- solution correctness;
- blueprint coverage;
- item-writing QA;
- source/provenance status.

### After sufficient learner-response data

Possible examples:

- observed proportion correct;
- item-total relations/discrimination;
- distractor behavior;
- reliability estimates;
- empirical difficulty;
- model-based item parameters only when assumptions/sample are defensible.

Do not claim that all of the latter are automatically appropriate.

Propose explicit metadata that prevents expert pre-calibration from being mislabeled as psychometric calibration.

---

# 6. Research stream R4-C — Assessment blueprinting and item lifecycle

Research what a defensible small educational assessment should record.

Consider:

- learning objectives/concepts;
- content coverage;
- cognitive/representation demand;
- item purpose;
- response format;
- approximate time;
- accessibility/accommodation concerns;
- scoring scheme;
- answer/solution verification;
- item status/version;
- exposure history;
- pilot statistics where available.

### Required R4-C output

Propose:

- minimum assessment blueprint schema;
- release gates;
- item revision statuses;
- retirement criteria;
- versioning policy;
- secure/released/public item distinctions.

---

# 7. Research stream R4-D — Publication and page design

Research evidence on educational-page design for approximately secondary/Grade 9 learners, including:

- multimedia-learning principles;
- coherence;
- signaling;
- segmenting;
- spatial contiguity;
- temporal contiguity where relevant digitally;
- split attention;
- redundancy;
- diagram labeling;
- worked-example layout;
- typography;
- line length;
- spacing/whitespace;
- visual hierarchy;
- color use;
- decorative imagery;
- print versus screen reading;
- navigation;
- cross-references;
- annotation/work space;
- cognitive load from page design.

Critically distinguish rigorous multimedia-learning evidence from broad popular claims such as simplistic “dual coding” advice.

### Required R4-D output

Provide page-design principles grouped as:

- evidence-supported;
- standards/accessibility-driven;
- reasonable design convention;
- project hypothesis requiring pilot.

Evaluate the current recurring page vocabulary:

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

Do not ask whether the labels are attractive. Ask what instructional functions should exist, whether the labels communicate those functions, and whether every page needs every function.

---

# 8. Research stream R4-E — Purposeful whitespace and page-density heuristic

Critically evaluate the current rough target of `70–85% meaningful page occupancy`.

Research whether meaningful learning-page quality can be reduced to an occupancy percentage and what better proxies exist.

Consider:

- text density;
- line spacing;
- working area;
- visual grouping;
- signaling;
- chunking;
- diagram space;
- learner annotation;
- print trim/margins;
- screen viewport;
- accessibility/readability.

### Required R4-E output

Classify the occupancy rule as:

- evidence-supported;
- useful project heuristic;
- misleading metric;
- pilot-only.

If it should be replaced, propose a page QA rubric that can distinguish intentional work space from accidental emptiness and overcrowding.

---

# 9. Research stream R4-F — Print, linked PDF, and digital differences

Research what should differ among:

- print textbook;
- print question bank;
- linked PDF;
- screen-first document;
- future digital adaptive tutor.

Consider:

- navigation;
- solution reveal;
- hint access;
- learner state;
- repeated exposure;
- accessibility;
- search/bookmarks;
- annotations;
- responsive versus fixed layout;
- hyperlink dependence.

### Required R4-F output

Define publication profiles:

```text
PRINT_STATIC
LINKED_PDF
SCREEN_DOCUMENT
DIGITAL_STATEFUL
```

Recommend what each profile may and may not claim or support.

---

# 10. Research stream R4-G — Accessibility

Research current authoritative accessibility requirements and good practice relevant to educational documents and digital learning content.

Address:

- semantic structure;
- reading order;
- contrast;
- font scaling/readability;
- color dependence;
- alt text / diagram descriptions;
- table structure;
- keyboard navigation where interactive;
- links and labels;
- mathematical notation accessibility;
- PDF accessibility limitations;
- print accessibility considerations;
- cognitive/readability considerations without overclaiming disability-specific efficacy.

### Required R4-G output

Provide an accessibility checklist separated into:

- mandatory/standards-driven;
- strongly recommended;
- context-dependent.

Identify which checks can be automated.

---

# 11. Research stream R4-H — AI-generated educational content correctness

Research current evidence and documented failure modes of generative AI in educational-content authoring, especially:

- mathematical errors;
- scientific misconceptions;
- inconsistent solutions;
- invented citations;
- ambiguous questions;
- unsatisfiable or multi-answer items;
- accidental scope drift;
- hidden assumptions;
- unreliable difficulty judgments;
- style imitation / near-copy risk;
- benchmark memorization or contamination concerns.

### Required R4-H output

Propose an independent verification policy for AI-authored or AI-modified content.

At minimum distinguish:

- transcription/extraction;
- paraphrase;
- authored item;
- answer generation;
- solution generation;
- difficulty estimate;
- misconception diagnosis;
- source attribution.

Define which outputs require:

- deterministic verification;
- second independent solution;
- source cross-check;
- expert subject review;
- pilot data.

---

# 12. Research stream R4-I — Error severity and release gates

Propose a severity taxonomy for educational-content defects, such as:

- cosmetic/editorial;
- pedagogical weakness;
- ambiguity;
- wrong answer;
- invalid solution;
- source/provenance defect;
- curriculum-scope defect;
- assessment-validity defect;
- safety/legal/accessibility issue where applicable.

### Required R4-I output

Define release-blocking versus non-blocking defect classes and the evidence required to close them.

---

# 13. Research stream R4-J — Provenance and auditability

Research best practice for traceability in educational content pipelines.

The system currently distinguishes source-derived and original-calibrated content. Determine what a robust provenance record should include.

Consider:

- source ID;
- exact source location/page/item;
- source authority;
- copyright/license status;
- transcription status;
- transformation history;
- AI involvement;
- verification events;
- answer/solution reviewers;
- version history;
- derived-from relationships;
- URLs/DOIs;
- repository commit;
- release state.

### Required R4-J output

Propose a machine-oriented provenance/audit schema concept for R5.

Define minimum provenance required before release.

---

# 14. Research stream R4-K — Copyright-safe question-bank construction

Research copyright/licensing considerations relevant to:

- user-supplied material;
- official released exam items;
- secure exam items;
- textbook/commercial-bank questions;
- paraphrase;
- structural inspiration;
- generated analogues;
- near copying;
- source citation versus permission;
- public-domain/open-license material.

Do not provide jurisdiction-specific legal conclusions as universal rules.

### Required R4-K output

Provide a cautious source-use policy with categories such as:

- reproduce permitted/authorized;
- cite and link only;
- paraphrase metadata only;
- use for calibration but author a genuinely new item;
- do not ingest/reproduce;
- legal review required.

Identify what metadata is needed to support later jurisdiction-specific policy.

---

# 15. Research stream R4-L — Source authority and external verification

Research a source hierarchy suitable for educational content verification.

Consider:

- user-supplied primary source;
- official curriculum/exam source;
- government/academic source;
- peer-reviewed source;
- professional standard;
- recognized educational repository;
- commercial educational content;
- general web source.

### Required R4-L output

Define how **authority**, **relevance**, **recency**, and **source fidelity** interact.

Do not assume one hierarchy fits every task: an official exam paper may be authoritative for wording/provenance, while peer-reviewed research may be authoritative for pedagogy.

---

# 16. Worked analyses required

Provide at least:

1. one practice item versus assessment-item comparison;
2. one example showing why expert difficulty is not psychometric difficulty;
3. one current Grade 9 page archetype audit;
4. one print-versus-linked-PDF redesign comparison;
5. one AI-authored question QA walk-through;
6. one provenance record for a source item and one for an original calibrated item;
7. one copyright-safe transformation example and one near-copy failure example.

Use traceable sources and clearly label original examples.

---

# 17. Current-rule audit required from R4

Audit at minimum:

- current source-status taxonomy;
- current provenance taxonomy;
- `USER_UPLOADED_ANCHOR`, `OFFICIAL_PYQ`, `SECONDARY_VERIFIED_PYQ`, `PUBLISHED_REFERENCE`, `ORIGINAL_CALIBRATED`, `RECONSTRUCTED_FROM_SCAN`;
- current source fidelity policy;
- current assessment/practice distinction, or lack thereof;
- current canonical master JSON authority;
- current PDF internal-link QA;
- current page vocabulary/archetypes;
- 70–85% occupancy heuristic;
- purposeful-whitespace rule;
- publication render inspection;
- AI answer/solution verification policy;
- copyright-safe transformation guidance;
- durable source citation/audit requirements.

Use verdicts:

- `KEEP`
- `KEEP WITH CLARIFICATION`
- `MODIFY`
- `REPLACE`
- `REMOVE`
- `REQUIRES PILOT DATA`

---

# 18. Required output format

Return exactly these sections:

## R4.1 Executive findings

Maximum 15 findings.

## R4.2 Evidence matrix

| Evidence ID | Domain | Claim / Design Question | Finding | Evidence Type | Grade A-D | Durable Sources | Boundary Conditions | Grade 9 Implication |
|---|---|---|---|---|---|---|---|---|

## R4.3 Item-purpose and assessment contract

## R4.4 Psychometric inference boundaries

Explicitly state what can and cannot be claimed before learner-response data.

## R4.5 Assessment blueprint and item-lifecycle model

## R4.6 Publication/page-design principles

Classify each recommendation by evidence/standard/design status.

## R4.7 Purposeful-whitespace/page-QA model

## R4.8 Print / linked PDF / screen / digital-stateful profiles

## R4.9 Accessibility checklist

## R4.10 AI correctness and verification policy

## R4.11 Error severity and release gates

## R4.12 Provenance/audit model

## R4.13 Copyright/source-use policy

## R4.14 Source-authority model

## R4.15 Worked analyses

## R4.16 Current-rule verdict matrix

| Current Rule | Verdict | Evidence IDs | Replacement/Clarification | Confidence | Pilot Needed? |
|---|---|---|---|---|---|

## R4.17 Candidate schema implications for R5

Proposal records only; do not edit schemas.

## R4.18 Candidate skill implications for R5

Identify likely deltas for:

- `grade9-source-grounding`;
- `grade9-question-bank`;
- `grade9-learning-enrichment`;
- `grade9-textbook-publisher`;
- router/shared workflow where appropriate.

## R4.19 Candidate validator implications for R5

Separate deterministic, heuristic and expert-review gates.

## R4.20 Open questions and pilots

## R4.21 Durable bibliography/source ledger

---

# 19. Important constraints

- Do not implement repository changes.
- Do not turn this into a student project.
- Do not claim psychometric properties without suitable learner-response evidence.
- Do not treat educational purpose as an automatic copyright exemption.
- Do not generalize one jurisdiction’s copyright law globally.
- Do not treat accessibility as optional visual polish.
- Do not recommend decorative design merely because it appears child-friendly.
- Do not turn page occupancy into a universal learning-science law without evidence.
- Do not trust AI-generated citations, answers, or difficulty judgments without verification.
- Keep official/source wording, paraphrase, and original generation distinguishable.
- Preserve uncertainty and boundary conditions.

---

# 20. Final handoff block

End with:

# R4 HANDOFF TO METHODOLOGY-v2 SYNTHESIS

Include:

1. top 10 R4 decisions;
2. assessment claims safe before learner data;
3. claims requiring learner data;
4. publication rules supported strongly enough for immediate adoption;
5. page/UX hypotheses requiring pilot testing;
6. provenance fields R5 should consider mandatory;
7. AI verification gates R5 should consider mandatory;
8. copyright/source-use rules suitable for global baseline versus jurisdiction adapter;
9. validator candidates;
10. current rules most likely to change;
11. unresolved questions R5 must preserve.
