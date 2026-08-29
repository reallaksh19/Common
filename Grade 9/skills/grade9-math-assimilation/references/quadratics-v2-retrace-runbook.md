# Quadratics v2 Retrace Runbook

## Purpose

This file records the exact production sequence used to create the Quadratics v2 benchmark so another agent can reproduce the method without access to the original conversation.

The objective is not to recreate the same sentences or visual design. Reproduce the **reasoning process, pedagogy, evidence discipline, QA, and artifact set**.

---

# 1. Starting point

The earlier Quadratics output existed as five short student PDFs:

1. Foundations and Representations
2. Discriminant and Repeated Roots
3. Vieta and Root Invariants
4. Transformed and Integer Roots
5. NMTC Preliminary Mastery

The mathematics was generally strong, but the teaching architecture was too close to a sequence of well-formatted notes. The student model was changed to:

> learner has roughly 50% prior knowledge and needs missing connections repaired.

The benchmark question became:

> Can a partly prepared student reconstruct the idea, recognize when it applies, write the first move, reject a near-miss method, and transfer it without help?

---

# 2. Benchmark comparison that triggered redesign

A separate Sequence & Series First-Step Reference was inspected for useful pedagogy features:

- recognition atlas;
- phrase decoder;
- decision tree;
- First-Step cards;
- contrast pairs;
- staged hints;
- recognition-only laboratory;
- transfer problems;
- stronger mathematical typography.

The conclusion was **not** to copy that book. The useful insight was to separate two products:

1. an **Assimilation Book** that repairs understanding;
2. a **First-Step Reference** that compresses already-understood structure for revision.

Core design decision:

`CONCEPT ASSIMILATION -> RECOGNITION -> EXECUTION -> TRANSFER`

not

`RECOGNITION -> FORMULA -> PRACTICE`.

---

# 3. Derive the learner loop

The existing Grade 9 Mathematics macro contract remained:

`SEE -> REALIZE -> UNDERSTAND -> ADOPT`

A new operational loop was added for the partial learner:

`RECONNECT -> DISCOVER -> MAKE SENSE -> TRY -> DIAGNOSE -> FADE -> ADOPT -> TRANSFER`

Reason for each stage:

- `RECONNECT`: activate what the learner already owns;
- `DISCOVER`: reveal the new relation/structure through a concrete case;
- `MAKE SENSE`: derive/explain why it works;
- `TRY`: force an attempt before full scaffolding;
- `DIAGNOSE`: explain the likely wrong move and the missing bridge;
- `FADE`: remove support systematically;
- `ADOPT`: require independent recognition/first move;
- `TRANSFER`: change the surface while preserving the invariant.

---

# 4. Build the generic partial-knowledge concept map

Before rewriting Quadratics, create the generic authority:

`Grade 9/skills/grade9-math/references/partial-knowledge-assimilation-concept-map.md`

Mandatory nodes:

- PRIOR_KNOWLEDGE
- LIKELY_HALF_KNOWLEDGE
- MISSING_BRIDGE
- INVARIANT_OR_STRUCTURE
- REPRESENTATIONS
- DECISION_BOUNDARIES
- MISCONCEPTION_TRAPS
- FIRST_MOVE_CUES
- TRANSFER_ENDPOINTS
- SOURCE_CUSTODY

This prevents prose-first authoring.

---

# 5. Update Grade 9 Mathematics skill/protocol

Update:

- `Grade 9/skills/grade9-math/SKILL.md`
- `Grade 9/skills/grade9-math/references/concept-book-see-realize-understand-adopt.md`

Add:

- partial-knowledge learner model;
- concept-map-before-prose requirement;
- H3/H2/H1/H0 hint model;
- attempt-before-hint;
- explicit diagnostic repair;
- First-Step Reference as compression after understanding;
- six-question assimilation test;
- new gates `MSRU-16` through `MSRU-22`.

The six-question test is:

1. What did you notice?
2. Why does the method work?
3. What clue would make you think of it?
4. What similar-looking situation requires a different method?
5. Can you write the first two useful lines without help?
6. Can you solve a disguised version?

---

# 6. Re-ground Quadratics source authority

Read before authoring:

- `Grade 9/Mathematics/NMTC Preliminary/03_Concept_Books/Algebra/Polynomial_Root_Structure/Polynomial_Root_Structure_Source_Coverage_Map.md`
- `Grade 9/Mathematics/NMTC Preliminary/00_Authority/`
- existing Polynomial/Root concept spec/student draft;
- existing first-step/practice/mastery/QA assets where relevant.

Preserve evidence roles:

- clean scored anchors;
- bonus evidence;
- bridge evidence;
- source conflicts;
- author-created foundation/transfer.

Important retained conflict:

`NMTC-BH-P-2025-Q20` must remain source-conflict evidence; never repair the sign/key silently.

---

# 7. Build the Quadratics-specific concept map

Create:

`Quadratics_Assimilation_Concept_Map.md`

Map these main bridges:

- standard form <-> factor/root form <-> graph/vertex view;
- discriminant <-> root count <-> tangency/intersection;
- coefficients <-> Vieta root invariants;
- root invariants <-> symmetric targets;
- transformed roots <-> transformed sum/product;
- positive/integer restrictions <-> discrete factor/inequality structure;
- quadratic relation <-> rewriting rule/power reduction;
- requested quantity <-> representation choice.

Central student belief:

> The requested information chooses the representation.

---

# 8. Author the Assimilation Book

Create:

`Quadratics_Assimilation_Book_v2.md`

The benchmark source used these sections:

0. Reconnect diagnostic
1. One quadratic, several useful views
2. Discriminant as root geometry
3. Vieta as relational information
4. Transformed roots
5. Positive/integer roots
6. Quadratic relation as a rewriting machine
7. Vertex/completing-square view
8. Parameter translation
9. Error laboratory
10. Faded practice ladder
11. Mixed ADOPT laboratory
12. Six-question mastery check

Required repeated teaching devices:

- RECONNECT examples;
- contrast pairs;
- first-move-only attempts;
- explicit wrong-move diagnosis;
- H3->H0 fading;
- source mechanism notes without full third-party reproduction.

---

# 9. Author the First-Step Reference

Create:

`Quadratics_First_Step_Reference_v2.md`

Only after the Assimilation Book structure is stable.

Required components:

- recognition atlas;
- phrase/structure decoder;
- quick decision tree;
- First-Step cards;
- contrast pairs;
- recognition-only lab;
- quick source-to-first-step map;
- concise checks/traps.

Do not repeat full concept derivations here.

---

# 10. Generate the student PDFs

Canonical benchmark files:

- `Quadratics_Concept_Map_v2.pdf`
- `Quadratics_Assimilation_Book_v2.pdf`
- `Quadratics_First_Step_Reference_v2.pdf`
- `Quadratics_Complete_Learning_Pack_v2.pdf`

Canonical reading order in the complete pack:

`Concept Map -> Assimilation Book -> First-Step Reference`

Use real mathematical typesetting rather than raw `sqrt(...)`, ASCII alpha/beta, or unformatted powers where the production renderer supports proper notation.

---

# 11. Render and inspect every page

Use the PDF workflow:

1. render all pages to images;
2. inspect page-by-page/contact sheets;
3. check clipping/overlap;
4. check equations and glyphs;
5. check tables/callout breaks;
6. check learner flow and fading;
7. run PDF preflight;
8. record page count and hash.

The benchmark render review produced:

- Assimilation Book: 9 A4 pages;
- First-Step Reference: 4 A4 pages;
- Concept Map: 1 A4 page;
- combined learning pack: 14 A4 pages.

---

# 12. Perform an independent math audit

Do not trust the authored answer section because it was written by the same authoring pass.

Recompute selected/all answers separately.

A real defect caught in this phase:

For roots of

`2x^2 + x - 4 = 0`,

`S=-1/2`, `P=-2`, hence

`(alpha-beta)^2 = S^2 - 4P = 1/4 + 8 = 33/4`.

An earlier source answer had `17/4`. The benchmark PDF already used the correct `33/4`; the repository source was then corrected.

Rule:

> Correct stale source output before promotion. Do not leave a known wrong answer in student-facing source with an audit footnote.

---

# 13. Record QA honestly

Create/update QA snapshot.

Static gates may PASS:

- concept map;
- pedagogy architecture;
- mathematical audit;
- typesetting/render;
- source custody;
- PDF preflight.

Do not convert unavailable evidence into PASS:

- classroom timing/readability: `NOT_RUN`;
- longitudinal student mastery evidence: `NOT_RUN`;
- publication approval: `NOT_READY` until separately authorized/calibrated.

---

# 14. Create reusable issue program

Split the original five deliverables into independently executable issues:

- #36 Foundations / representations
- #37 Discriminant / repeated roots
- #38 Vieta / root invariants
- #39 Transformed & integer roots / structural reduction
- #40 Mixed mastery / transfer

Use #41 as coordination only.

Each issue contains:

- exact objective;
- required input links;
- scope;
- pedagogy;
- deliverables;
- acceptance criteria;
- copy-ready agent prompt.

---

# 15. Benchmark use policy

The benchmark is used to answer:

- Is the concept map as complete?
- Is the missing bridge explicit?
- Are contrast pairs meaningful?
- Does support genuinely fade?
- Can the student recognize without labels?
- Is transfer non-identical?
- Is source custody at least as strong?
- Is the PDF at least as readable/clean?

The benchmark must **not** be used to copy:

- sentences;
- exercise wording;
- exact page layout;
- colors/cards;
- typography choices;
- visual composition.

A successor should preserve the method and improve the content.

---

# 16. Minimum completion checklist for another agent

Before declaring a child issue internally complete, verify:

- [ ] all required inputs were read;
- [ ] concept map created first;
- [ ] target 50%-prepared learner explicitly modeled;
- [ ] RECONNECT diagnostic present;
- [ ] invariant/structure derived, not formula-dumped;
- [ ] at least two meaningful contrast pairs;
- [ ] attempt-before-hint present;
- [ ] H3->H0 fading present;
- [ ] First-Step Reference is separate/compressed;
- [ ] recognition and first-line work present;
- [ ] non-identical transfer present;
- [ ] source roles preserved;
- [ ] all answers independently rechecked;
- [ ] PDF rendered and visually inspected;
- [ ] QA records PASS/PARTIAL/NOT_RUN honestly;
- [ ] benchmark comparison completed without copying.
