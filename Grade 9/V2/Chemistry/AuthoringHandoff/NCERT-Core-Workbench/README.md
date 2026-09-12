# Chemistry NCERT Core Workbench — Agent Handoff

This directory is a **working authoring handoff**, not a mature-release claim. It captures the reusable files and operating rules discovered while stress-testing Chemistry PR #322 against fresh NCERT source material so a later agent can continue from the current state instead of restarting the design process.

This branch is intentionally **stacked on `v2-chemistry-upgrade-real-rendering` (PR #322)**. Open/review this PR against that branch, not against `main`, so the diff contains only the handoff work.

## 0. Fast start for a new agent

From `Grade 9/V2/Chemistry/AuthoringHandoff/NCERT-Core-Workbench/`:

```bash
python tools/restore_source_bundle.py --output restored-workspace
python tools/validate_handoff.py restored-workspace/final
```

Then pick the nearest completed topic under `restored-workspace/final/` and use its HTML + coverage ledger as the starting pattern.

Do **not** begin by designing pages. The first job is to freeze the source/question denominator for the new topic.

## 1. What is preserved here

Four topic builds are included as editable source-of-truth artifacts:

| Topic | Core (1) | Core (2) | Retained source-question instances | Immediate answer checks | Full worked solutions |
|---|---|---|---:|---:|---:|
| Some Basic Concepts of Chemistry | `core1.html` | `core2.html` | 68 | 68 | 68 |
| Behaviour of Gases | `core1.html` | `core2.html` | 27 | 27 | 27 |
| Chemical Bonding | `core1.html` | `core2.html` | 38 | 38 | 38 |
| Redox Reactions | `core1.html` | `core2.html` | 11 | 11 | 11 |

For each topic the restored tree contains:

- `core1.html` — editable Core Study Guide source;
- `core2.html` — editable ExamSIDE / Question Helper source;
- `coverage-ledger.csv` — retained source-question inventory and mapping.

The final editable sources are stored losslessly as a chunked base64 `tar.gz` archive under:

```text
bundles/final-sources/
```

`tools/restore_source_bundle.py` reconstructs them and verifies both byte size and SHA-256 before extraction.

Generated PDF filenames, byte sizes and SHA-256 values from the working session are recorded in `BINARY_ARTIFACTS.md`. The PDFs are reproducible from the HTML and therefore are not duplicated as opaque binaries in this handoff PR. Session-only screenshots/contact sheets are also omitted because they are QA evidence, not authoring inputs.

## 2. What PR #322 gives you — and what this workbench adds

PR #322 is strong in exact-product/publication engineering: product topology, chemistry notation safety, vector primitive realization, learner-surface guards, placement custody, frozen candidates and engineering falsifiers.

This workbench adds the **cold-start authoring discipline** that a novice agent needs when given a new chapter + a set of source PDFs:

1. source denominator closure;
2. topic relevance / exclusion decisions;
3. question-family and learner-capability derivation;
4. visual-obligation assignment;
5. Core (1) depth expectations;
6. teacher-helper microcopy rules for Core (2);
7. immediate answer-check requirements;
8. rendering/legibility targets;
9. final coverage invariants.

Do not treat this handoff as evidence that PR #322's pending human gates have passed. Subject correctness, pedagogy, assessment, visual usability and mature-design review still require their authorized review path.

## 3. Source corpus used during the stress test

The workbench was created from the supplied NCERT Class IX exemplar PDFs and sample papers. Primary links used repeatedly:

- Unit 1 — Matter in Our Surroundings: `https://ncert.nic.in/pdf/publication/exemplarproblem/classIX/science/ieep101.pdf`
- Unit 2 — Is Matter Around Us Pure: `https://ncert.nic.in/pdf/publication/exemplarproblem/classIX/science/ieep102.pdf`
- Unit 3 — Atoms & Molecules: `https://ncert.nic.in/pdf/publication/exemplarproblem/classIX/science/ieep103.pdf`
- Unit 4 — Structure of the Atom: `https://ncert.nic.in/pdf/publication/exemplarproblem/classIX/science/ieep104.pdf`
- Sample Question Paper I: `https://ncert.nic.in/pdf/publication/exemplarproblem/classIX/science/ieep116.pdf`
- Sample Question Paper II: `https://ncert.nic.in/pdf/publication/exemplarproblem/classIX/science/ieep117.pdf`

A chapter title is **not permission to import arbitrary textbook knowledge**. Keep source-derived obligations, justified enrichment and exclusions distinguishable.

## 4. Required authoring sequence

Use this order. Skipping steps is how the first stress-test attempts became thin or incomplete.

### Step A — scan the complete supplied corpus

Do not select PDFs only from filenames. Inspect every supplied source that could plausibly contain an in-scope question, including sample papers.

For every discovered question instance record:

- source PDF / unit;
- source question number;
- question focus;
- `IN_SCOPE` / `OUT_OF_SCOPE`;
- canonical topic/subtopic;
- exclusion reason if not retained;
- primary placement identity.

### Step B — freeze the denominator

Before writing Core (1) or Core (2), state explicit counts:

```text
TOTAL_SCANNED
RETAINED_IN_TOPIC
EXCLUDED_WITH_REASON
PRIMARY_PLACEMENTS
MISSING
DUPLICATE_PRIMARY
```

A topic is not coverage-complete unless:

```text
RETAINED_IN_TOPIC == PRIMARY_PLACEMENTS
MISSING == 0
DUPLICATE_PRIMARY == 0
```

Multi-skill questions may support several teaching concepts, but each source-question instance gets **one canonical primary placement** for counting purposes.

### Step C — derive capabilities from questions

Do not force questions into the capability taxonomy merely because a nearby label exists. Derive what the learner actually has to do.

Examples discovered during this work:

- classify matter by composition;
- convert units by dimensional reasoning;
- distinguish coefficient / subscript / charge;
- construct ionic formulae by charge neutrality;
- calculate formula mass and composition;
- move mass ↔ moles ↔ particles;
- count ions / atoms per entity;
- calculate concentration using the correct denominator;
- follow stoichiometric mole-ratio routes;
- assign oxidation number and track redox change.

### Step D — assign visual obligations before prose

A book can contain many diagrams and still fail locally. Decide the representation family at the question/concept-family level first.

Useful visual families from the completed topics include:

- matter classification tree / three-bucket sort;
- particle model;
- dimensional-analysis ladder;
- formula-anatomy strip;
- ionic charge-balance builder;
- electron-shell / valence representation;
- mass–mole–particle bridge;
- formula-unit → ion-count model;
- concentration part/whole frame;
- stoichiometry route;
- atom-conservation ledger;
- oxidation-number lane / before-after tracking;
- redox vs non-redox contrast.

A visual is useful only if it helps the learner know what to **write, draw, count, cancel, compare, label or track next**.

### Step E — build Core (1)

Core (1) is the teaching product, not a summary sheet. Preserve the PR #322 topology:

- Main Teaching;
- Appendix A — Core Practice;
- Appendix B — Core Solutions;
- Appendix C — Printable Handout.

For a full-learning concept, aim for the following where applicable:

- ordinary-language explanation;
- diagrammatic representation;
- rule/model/condition;
- why/reconstruction reasoning;
- worked example with visible equations/steps;
- misconception repair;
- guided attempt;
- faded attempt;
- independent attempt;
- verification / sense check;
- transfer or competitive reasoning derived from the authorized material.

“Competitive depth” means extracting stronger reasoning from the same scope — proportional shortcuts, comparison strategies, dimensional reasoning, sanity checks, decision trees, exceptions and transfer — not importing unsupported higher-grade syllabus content.

### Step F — build Core (2)

Every retained source question is a self-study object. The preferred learner sequence is:

1. **Try the question**
2. **See the idea** — question-specific diagram / representation
3. **Write this first**
4. **First nudge**
5. **Set it up on paper**
6. **Watch for this**
7. **Before you answer**
8. **Answer check**
9. **Full worked solution later**

The helper must tell the learner what to do next on paper. Avoid software-like statements such as “Apply the mole method.” Prefer:

> Write `n = m/M`. Substitute the sample mass and molar mass with units. Cancel `g`; the remaining unit should be `mol`.

## 5. Non-negotiable answer invariant

> **NO QUESTION WITHOUT A CHECKABLE ANSWER PATH.**

For closed/objectively checkable items:

```text
retained_questions == immediate_answer_checks == full_worked_solutions
```

For genuinely open-ended prompts, provide an explicit expected-response rubric instead of pretending there is a single answer.

Immediate checks are intentionally compact:

- MCQ → option + result;
- numerical → final value + unit;
- classification → expected classes/members;
- short answer → essential marking points;
- graph/diagram → required labels/features.

The full solution remains separate and shows reasoning/equations/units.

## 6. Teacher-helper language contract

A hint is weak if it only names a method. A useful hint produces an observable learner action.

Bad:

> Use formula writing rules.

Better:

> Write `Ca²⁺` and `PO₄³⁻`. The LCM of 2 and 3 is 6. How many calcium ions give +6? How many phosphate ions give −6? Put those counts into the formula and simplify if possible.

Bad:

> Use the definition to classify the substances.

Better:

> First split the entries into mixtures and pure substances. For each pure substance ask: one kind of atom only, or different elements chemically combined in a fixed ratio?

## 7. Typography and page-geometry targets

PR #322's 8 pt floor is an engineering minimum, not the preferred learner size. Use approximately:

- instructional body: **10–11 pt+**;
- question stem: **12–14 pt** where practical;
- primary equations: **12 pt+**;
- diagram labels: normally **9 pt+**;
- enough working space for the expected calculation/reasoning;
- no overlapping shapes;
- no clipped text;
- no essential meaning encoded only by color.

Inspect rendered PDF pages at actual output size. HTML/CSS validity is not a visual-usability test.

## 8. Validation before calling a topic complete

Run:

```bash
python tools/validate_handoff.py restored-workspace/final
```

Then render both HTML products and inspect representative pages from **every page family**, not just the cover.

Minimum acceptance checklist:

- [ ] all supplied PDFs were considered;
- [ ] retained denominator is fixed in a ledger;
- [ ] excluded items have explicit reasons;
- [ ] every retained question has exactly one primary placement;
- [ ] every source-derived skill/concept has a Core (1) teaching home;
- [ ] visually obligated concepts/questions have the right representation;
- [ ] helpers tell the learner the next useful paper action;
- [ ] all Core (1) practice has an answer path;
- [ ] all Core (2) retained questions have immediate answer checks;
- [ ] all Core (2) retained questions have full worked solutions/rubrics;
- [ ] chemical notation is unambiguous;
- [ ] units are shown through calculations;
- [ ] text is legible at actual output size;
- [ ] diagrams are unclipped and non-overlapping;
- [ ] source links / identifiers do not leak internal authoring tokens;
- [ ] no human-reviewed maturity is claimed without the required review.

## 9. Choosing a template

Use the completed topic with the closest reasoning structure:

- **Some Basic Concepts** — best reference for mixed quantitative + classification + formula/mole workflows and large source denominators.
- **Behaviour of Gases** — best reference for particle models, qualitative causal reasoning, phase/temperature graphs and state-change questions.
- **Chemical Bonding** — best reference for notation, electron/valency visuals, ions and formula construction.
- **Redox Reactions** — best reference for before/after tracking, oxidation-number reasoning and redox/non-redox contrasts.

Copy structure, **not answers or chemistry entities**. New chapter content must remain grounded in its own source set.

## 10. Files in this PR

```text
NCERT-Core-Workbench/
├── README.md
├── WORKFLOW.md
├── BINARY_ARTIFACTS.md
├── requirements.txt
├── bundles/
│   └── final-sources/
│       └── final-sources.tar.gz.b64.part000 ... part007
└── tools/
    ├── restore_source_bundle.py
    ├── rebuild_pdf.py
    └── validate_handoff.py
```

After restoration:

```text
restored-workspace/
└── final/
    ├── some-basic-concepts/
    │   ├── core1.html
    │   ├── core2.html
    │   └── coverage-ledger.csv
    ├── behaviour-of-gases/
    │   └── ...
    ├── chemical-bonding/
    │   └── ...
    └── redox-reactions/
        └── ...
```

The editable final source bundle is the intended handoff baseline. `BINARY_ARTIFACTS.md` records the rendered-session provenance; regenerate PDFs from the committed sources before making further edits or review claims.
