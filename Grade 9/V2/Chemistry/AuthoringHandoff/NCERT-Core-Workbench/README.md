# Chemistry NCERT Core Workbench — Agent Handoff

This folder is a **working handoff**, not a mature release. It packages the artifacts created while stress-testing and extending Chemistry PR #322 so another agent can continue from the current state instead of rebuilding the authoring approach from scratch.

The branch for this handoff is intentionally stacked on `v2-chemistry-upgrade-real-rendering` (PR #322). That keeps the work close to the exact-product/representation changes it depends on and avoids mixing this experimental authoring work into `main` before #322 is resolved.

## What is here

Four topics have complete Core (1) / Core (2) working artifacts:

| Topic | Core (1) | Core (2) | Retained NCERT question instances | Immediate answer checks | Full worked solutions |
|---|---|---|---:|---:|---:|
| Some Basic Concepts of Chemistry | `final/some-basic-concepts/core1.*` | `final/some-basic-concepts/core2.*` | 68 | 68 | 68 |
| Behaviour of Gases | `final/behaviour-of-gases/core1.*` | `final/behaviour-of-gases/core2.*` | 27 | 27 | 27 |
| Chemical Bonding | `final/chemical-bonding/core1.*` | `final/chemical-bonding/core2.*` | 38 | 38 | 38 |
| Redox Reactions | `final/redox-reactions/core1.*` | `final/redox-reactions/core2.*` | 11 | 11 | 11 |

For each topic the folder contains:

- `core1.html` — editable source for the Study Guide.
- `core2.html` — editable source for the Question Helper / Transfer Book.
- `coverage-ledger.csv` — retained NCERT question inventory and topic mapping.
- generated PDF names/hashes are recorded in `BINARY_ARTIFACTS.md`; PDFs can be regenerated from the committed HTML with `tools/rebuild_pdf.py`.

The HTML files are the most useful starting point for an agent because they preserve layout, helper language, diagrams, equation styling and source links in editable form.

## Start here — do not start from a blank page

When authoring the next topic:

1. Read **this README** and `WORKFLOW.md`.
2. Pick the completed topic whose reasoning pattern is closest to the new one.
3. Copy its `core1.html`, `core2.html`, and `coverage-ledger.csv` as working templates.
4. Replace the source denominator first. **Do not author pages until the denominator is frozen.**
5. Derive question families / learner capabilities from the retained source items.
6. Assign a visual obligation to each family before writing prose.
7. Build Core (1), then Core (2), then run the checks in `tools/validate_handoff.py`.
8. Render HTML to PDF with `tools/rebuild_pdf.py` and inspect the rendered pages, not only the HTML.

## Source corpus used in this workbench

The stress test used only the NCERT Class IX exemplar links supplied by the task plus the two sample papers. The most relevant source URLs are preserved in the HTML and coverage ledgers.

Primary PDFs used repeatedly:

- Unit 1 — Matter in Our Surroundings: `https://ncert.nic.in/pdf/publication/exemplarproblem/classIX/science/ieep101.pdf`
- Unit 2 — Is Matter Around Us Pure: `https://ncert.nic.in/pdf/publication/exemplarproblem/classIX/science/ieep102.pdf`
- Unit 3 — Atoms & Molecules: `https://ncert.nic.in/pdf/publication/exemplarproblem/classIX/science/ieep103.pdf`
- Unit 4 — Structure of the Atom: `https://ncert.nic.in/pdf/publication/exemplarproblem/classIX/science/ieep104.pdf`
- Sample Question Paper I: `https://ncert.nic.in/pdf/publication/exemplarproblem/classIX/science/ieep116.pdf`
- Sample Question Paper II: `https://ncert.nic.in/pdf/publication/exemplarproblem/classIX/science/ieep117.pdf`

Do not silently import higher-grade or external chemistry merely because it is normally associated with the chapter title. Source-derived coverage and external enrichment must remain distinguishable.

## Core (1) contract used in these artifacts

Core (1) is the **teaching product**. It should not be a summary sheet. A mature-enough working page normally includes some combination of:

- an ordinary-language explanation;
- a **diagrammatic representation**, not just prose;
- a worked example with visible equations / steps;
- an actionable helper / first move;
- a misconception repair or “Watch for this” contrast;
- guided, faded and independent practice where the topic supports it;
- competitive / transfer reasoning where source-authorized;
- a check or answer path for every practice question.

Core (1) should also retain the PR #322 topology: Main Teaching + Core Practice + Core Solutions + Printable Handout. The exact internal layout can evolve, but those roles should not disappear silently.

### Technical depth rule

“Competitive” does **not** mean importing unsupported syllabus content. It means extracting more reasoning from the same authorized material: proportional shortcuts, dimensional reasoning, comparison methods, decision trees, sanity checks, exception handling and transfer between representations.

## Core (2) contract used in these artifacts

Every retained question is treated as a self-study object. The preferred page sequence is:

1. **Try the question**
2. **See the idea** — question-specific diagram / representation
3. **Write this first** — the first useful mark on paper
4. **First nudge**
5. **Set it up on paper** — equation, table, classification frame, ledger, etc.
6. **Watch for this** — likely error / misconception
7. **Before you answer** — a verification check
8. **Answer check** — immediate final answer / marking points, visually separated so the learner can cover it
9. **Full worked solution later** — Appendix A or equivalent

The helper must sound like a teacher helping the learner **do the next step**, not like a software workflow. Prefer “Write the ion charges, make total charge zero, then simplify the ratio” over “Apply the ionic-formula method.”

## Non-negotiable self-study invariant

> **NO QUESTION WITHOUT A CHECKABLE ANSWER PATH.**

For closed / objectively checkable items:

`retained_questions == immediate_answer_checks == full_worked_solutions`

For genuinely open-ended items, replace the ordinary answer with an explicit `EXPECTED_RESPONSE_RUBRIC`; do not leave the learner with no way to check the attempt.

The immediate answer is intentionally shorter than the full solution:

- MCQ → correct option + compact result;
- numerical → final value + unit;
- classification → expected classes / members;
- short answer → essential marking points;
- diagram / graph → expected labels / features.

## Visual-obligation rule

A book can contain many diagrams globally and still fail locally. The stronger rule used after the first iterations is:

> **Every question family / major concept gets a declared visual reasoning aid when a visual would reduce cognitive load.**

Examples used in these files include:

- matter classification tree / sorting buckets;
- unit-conversion ladder / dimensional cancellation;
- formula anatomy: coefficient vs subscript vs charge;
- ion-charge balance model;
- electron-shell / valency representation;
- mass ↔ moles ↔ particles bridge;
- particle/entity count model;
- concentration part/whole model;
- reaction / stoichiometry route;
- oxidation-number lane / before-after tracking;
- redox vs non-redox contrast.

A visual is not accepted merely because it occupies space. It should help the learner know what to **write, count, compare, cancel, label or track next**.

## Typography / layout targets

PR #322's 8 pt minimum is an engineering floor, not a learner target. These artifacts evolved toward approximately:

- body instructional text: 10–11 pt or larger;
- question stems: 12–14 pt where space permits;
- primary equations: 12 pt+;
- diagram labels / annotations: normally 9 pt+;
- adequate white space for working;
- no overlapping diagram shapes;
- no essential meaning encoded by color alone.

Always inspect the **rendered PDF at actual output size**. HTML validity does not prove page usability.

## Relationship to PR #322

PR #322 is strong in publication engineering, notation safety, vector primitive realization, custody, exact-artifact freezing and learner-surface guards. This handoff captures the additional authoring rules that were discovered by applying it to new NCERT topics.

Important distinction:

- PR #322 says which exact products / quality states / representation machinery exist.
- This workbench documents how an agent should turn a fresh source corpus into learner-usable Core (1) and Core (2) artifacts without repeatedly rediscovering source closure, diagram selection, helper wording and answer-check requirements.

The workbench does **not** claim that pending human gates in #322 are passed.

## Current known limitations

1. These HTML artifacts are working authoring sources, not yet integrated as first-class outputs of the C-F / C-G / C-H registries.
2. Source ingestion was manually audited during the stress test; there is not yet a generic parser that freezes the denominator automatically from arbitrary PDFs.
3. Some representation families needed here are not yet first-class PR #322 primitive kinds (for example classification trees, unit ladders, mole bridges and some quantitative setup frames).
4. The artifacts preserve direct official NCERT hyperlinks for traceability; production source-display policy may need further alignment with repository contracts.
5. Human subject, pedagogy, assessment and visual-usability review remains required before any mature-release claim.
6. Historical iterations are retained under `history/` so future agents can see how the design evolved, but **the `final/` artifacts are the preferred starting point**.

## Repository layout in this handoff

```text
NCERT-Core-Workbench/
├── README.md
├── WORKFLOW.md
├── BINARY_ARTIFACTS.md
├── requirements.txt
├── final/
│   ├── some-basic-concepts/
│   ├── behaviour-of-gases/
│   ├── chemical-bonding/
│   └── redox-reactions/
├── history/
│   └── ... editable HTML iterations ...
└── tools/
    ├── rebuild_pdf.py
    └── validate_handoff.py
```

## Minimum acceptance checklist for a new topic

Before calling a topic complete, an agent should be able to answer **yes** to all of these:

- [ ] Did I scan all supplied source PDFs, not only filenames that looked relevant?
- [ ] Is the retained denominator fixed and recorded in a ledger?
- [ ] Does every retained question have exactly one canonical primary placement?
- [ ] Is every source-derived concept / skill given a teaching home in Core (1)?
- [ ] Does each major concept / question family have the correct visual reasoning aid where useful?
- [ ] Do helpers tell the learner what to write / draw / count / compare next?
- [ ] Does every Core (1) practice item have a quick answer and a worked solution or rubric?
- [ ] Does every Core (2) retained item have an immediate answer check and a full worked solution or rubric?
- [ ] Are equations, units, subscripts, superscripts and charges rendered unambiguously?
- [ ] Are fonts large enough at actual PDF size?
- [ ] Are diagrams unclipped, non-overlapping and semantically correct?
- [ ] Did I visually inspect representative pages from every page family after PDF rendering?
- [ ] Did I keep excluded / cross-chapter items explicit rather than silently dropping them?
- [ ] Did I avoid claiming human-reviewed maturity?

If any answer is “no”, the topic is not ready to be used as the next agent's baseline.
