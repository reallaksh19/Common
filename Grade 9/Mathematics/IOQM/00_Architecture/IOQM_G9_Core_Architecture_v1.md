# IOQM Grade 9 — Core Architecture v1

Status: `ARCHITECTURE_V1_DRAFT`

## 1. Architectural objective

Create a source-grounded IOQM preparation system for a Grade IX learner who may already know roughly half of the school mathematics behind a topic but does not yet reliably:

- connect representations;
- recognize the hidden mechanism;
- choose between near-neighbour methods;
- write the first useful line;
- preserve domain/condition constraints;
- transfer the invariant to an unfamiliar surface.

The system must support self-learning, self-evaluation, self-testing and transfer.

## 2. What this architecture explicitly rejects

Do not build the curriculum as:

`SUBTOPIC AGENT A WRITES BOOK A + SUBTOPIC AGENT B WRITES BOOK B + ... -> CONCATENATE`

That model creates local quality but weak global assimilation.

The accepted model is:

`MAIN-TOPIC LEAD -> FROZEN MAPS -> PARALLEL RESEARCH INTERFACES -> ONE LEAD INTEGRATION -> ONE STUDENT BOOK -> ONE FIRST-STEP LAYER -> ONE MASTERY LAYER -> INDEPENDENT QA`

Parallelism is used for evidence production, not fragmented student authorship.

## 3. Four architecture levels

### Level A — Program

`IOQM-G9`

Owns:

- competition-source scope;
- domain taxonomy;
- common learner model;
- stable provenance vocabulary;
- global question IDs;
- common PDF/export rules;
- cross-domain mixed assessment.

### Level B — Domain

- `NT` — Number Theory
- `ALG` — Algebra
- `GEO` — Geometry
- `COMB` — Combinatorics

A domain is an organizational container, not necessarily one student book.

### Level C — Main Topic

A main topic is the **unit of issue ownership, PR ownership, pedagogical integration and student publication**.

One main topic may contain several microconcepts that can be researched in parallel.

Required stable form:

`IOQM-G9-<DOMAIN>-<NN>`

Example:

`IOQM-G9-NT-02 — Modular Arithmetic & Cycles`

### Level D — Microstream

A microstream is internal working decomposition.

Examples inside Modular Arithmetic:

- congruence meaning;
- legal modular operations;
- power cycles;
- last digits;
- simultaneous congruences;
- cancellation/inverse traps.

A microstream produces an **interface**, not a standalone finished student book.

## 4. Single pedagogical owner rule

For every main topic, assign one lead with authority to:

- reorder microstream material;
- delete duplicated explanations;
- merge overlapping concepts;
- decide canonical terminology;
- move prerequisites earlier;
- rewrite transitions;
- select one governing invariant/router;
- reject locally good material that harms the global learning sequence;
- create the final student-facing prose.

This authority is mandatory. The lead is not merely an editor who concatenates stable outputs.

## 5. Three mandatory maps before prose

Every main topic must freeze three different maps before integrated prose is written.

### 5.1 Knowledge Dependency Map

Question answered:

> What must the learner understand before what?

Each node records:

- prerequisite;
- partial prior knowledge likely;
- missing bridge;
- new ownership target;
- dependency direction.

No downstream section may require a concept that is taught later.

### 5.2 Method Selection Map

Question answered:

> Once several methods are known, how does the learner choose the cheapest valid one?

Each boundary records:

- similar visible surface;
- Decision A;
- Decision B;
- discriminating question;
- invalid/oversized reflex;
- first useful line.

### 5.3 Transfer Map

Question answered:

> Where does the same invariant reappear under a changed surface?

Transfer edges must distinguish:

- representation change;
- context change;
- domain change;
- discrete/continuous change;
- cross-domain bridge;
- genuine new constraint.

Changing only numbers is not transfer.

## 6. Main-topic governing invariant

Every main topic must be compressible to one learner-owned rule or router.

Examples of acceptable form:

- Quadratics: `REQUESTED INFORMATION -> REPRESENTATION -> FIRST MOVE`
- Inequalities: `REQUEST -> DOMAIN -> BOUNDED? -> DIRECTION -> REPRESENTATION -> EQUALITY -> ATTAINMENT`
- Modular arithmetic: `TARGET MODULUS -> REDUCE STATE -> PRESERVE LEGAL OPERATIONS -> CYCLE/STRUCTURE -> CHECK`

A topic with many methods but no shared governing model fails architecture review.

## 7. Partial-knowledge assimilation contract

Every main topic follows:

`RECONNECT -> DISCOVER -> MAKE SENSE -> TRY -> DIAGNOSE -> FADE -> ADOPT -> TRANSFER`

### RECONNECT

Retrieve what the learner already owns; do not restart from definitions unless diagnostics show a prerequisite gap.

### DISCOVER

Expose the missing connection using one concrete case, pattern or contrast.

### MAKE SENSE

Derive/reconstruct the invariant, condition, representation or theorem mechanism.

### TRY

Require first-move attempt before full help.

### DIAGNOSE

Explain the tempting wrong move and classify the missing bridge.

### FADE

Use `H3 -> H2 -> H1 -> H0` support reduction.

### ADOPT

Require recognition without chapter labels and first-line independence.

### TRANSFER

Change the surface while preserving the mathematical invariant.

## 8. Main-topic execution waves

### Wave 0 — Grounding and freeze

Lead must establish:

- exact main-topic boundary;
- official-syllabus relationship;
- Grade-9 prerequisite adaptation;
- relevant validated PYQ set;
- source statuses;
- Knowledge Dependency Map;
- Method Selection Map;
- Transfer Map;
- overlap ownership matrix;
- governing invariant/router.

Gate: `WAVE0_ARCHITECTURE_FROZEN`

No integrated student prose before this gate.

### Wave 1 — Parallel microstream research

Parallel agents may produce:

- derivations/proofs;
- prerequisite notes;
- misconception catalogues;
- method boundaries;
- worked mathematical traces;
- PYQ tagging;
- source-integrity notes;
- candidate contrast pairs;
- candidate recognition items;
- candidate transfer items;
- independent answer verification.

Required output is the Microstream Interface Schema.

Gate: `WAVE1_INTERFACES_COMPLETE`

### Wave 2 — Lead integration

Only the pedagogical lead writes the integrated student teaching layer.

Required behavior:

- follow dependency order, not agent order;
- teach each concept canonically once;
- later appearances retrieve/apply, not reteach;
- merge shared bridges;
- insert cross-microstream contrast pairs;
- preserve one terminology set;
- use one continuous learner voice.

Deliverable:

`<MainTopic>_Assimilation_Book_v1.md`

Gate: `WAVE2_INTEGRATED_ASSIMILATION_PASS`

### Wave 3 — First-Step compression

Created only after Wave 2.

Contains:

- recognition atlas;
- phrase/structure decoder;
- decision tree/router;
- first-step cards;
- contrast strip;
- common traps/checks;
- recognition-only lab;
- source-to-mechanism map.

Gate: `WAVE3_FIRST_STEP_PASS`

### Wave 4 — Mastery and transfer

Create an H0 student paper with no method labels.

Required layers:

1. `NOTICE` — visible clue -> structure;
2. `FIRST LINE` — one useful mathematical line only;
3. `FULL SOLVE` — mixed unlabelled problems;
4. `SAME SURFACE / DIFFERENT DECISION` — close contrasts;
5. `TRANSFER` — changed-surface problems;
6. `WHY NOT / VERIFICATION` — reject invalid nearby reasoning.

Gate: `WAVE4_H0_MASTERY_PASS`

### Wave 5 — Independent audit

A fresh reviewer must independently verify:

- all promoted numerical answers;
- proof/derivation validity;
- endpoints, sign, parity, divisibility, domain and degeneracy cases;
- source IDs and source-status claims;
- no dependency inversion;
- no duplicated full teaching;
- no student-visible workflow/control-plane leakage.

Gate: `WAVE5_INDEPENDENT_QA_PASS`

### Wave 6 — Production/render

One render authority produces all final PDFs for the main topic.

Required:

- consistent math typography;
- one title/header/footer system;
- one box/callout grammar;
- student/teacher separation;
- page-by-page visual inspection;
- structural PDF preflight;
- page counts and SHA-256 hashes recorded.

Gate: `WAVE6_STATIC_RENDER_QA_PASS`

Human classroom timing/readability and longitudinal transfer remain `NOT_RUN` until actually observed.

## 9. Overlap ownership matrix

Before Wave 1, every concept that can appear in multiple main topics must receive one of:

- `CANONICAL_TEACHING_OWNER`
- `PREREQUISITE_RETRIEVAL_ONLY`
- `APPLICATION_ONLY`
- `CROSS_DOMAIN_BRIDGE`

Examples:

- Vieta may be canonically taught in `ALG-03`; geometry may apply it but should not rebuild it from scratch.
- AM-GM may be canonically taught in `ALG-02`; Number Theory may use equality/factor constraints as application.
- modular arithmetic may be canonically taught in `NT-02`; combinatorial state problems may use residues as a bridge.

No concept may have two independent canonical teaching owners without an explicit architecture exception.

## 10. Grade-9 adaptation levels

Every prerequisite/concept is tagged:

### `G9_CORE`

Reasonable Class 8–9 mathematical knowledge.

### `IOQM_BRIDGE`

A new Olympiad mechanism that can be taught directly to the Grade-9 learner.

### `JUST_IN_TIME_ADVANCED_LANGUAGE`

A small higher-class notation/concept needed for the mechanism; teach only the required portion.

### `DEFERRED`

Not needed for the current Grade-9 IOQM path.

The architecture must not force the learner to complete all higher-class school mathematics before IOQM preparation.

## 11. Student artifact contract

A final main-topic student pack should read as one book, not as production history.

The student export must remove:

- `Issue #...`;
- `PR #...`;
- `Wave 0/1/2...` labels;
- agent/interface names;
- QA state labels;
- internal evidence codes unless the code itself is pedagogically useful;
- authoring-only provenance detail beyond concise source notes.

Teacher/authoring artifacts retain full control-plane information.

## 12. Main-topic completion definition

A topic is internally complete only if the learner can answer, for each major mechanism:

1. What did I notice?
2. Why does the method work?
3. What clue should trigger it?
4. What similar-looking situation needs a different start?
5. Can I write the first two useful lines without help?
6. Can I solve a changed-surface version?

Static completion state:

`BENCHMARK_READY_NOT_CLASSROOM_CALIBRATED`

Do not promote classroom timing, retention or psychometric claims without evidence.

## 13. Program-level capstone

Only after main-topic packages are stable should the program create:

- domain-mixed recognition tests;
- cross-domain first-line tests;
- full IOQM-style mixed papers;
- source-grounded PYQ retrieval sets;
- remediation routing based on mechanism/error tags.

The capstone must consume topic interfaces and metadata. It must not become the place where missing main-topic integration is repaired.