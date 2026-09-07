# Grade 9 Skill Family

This folder contains the reusable Grade 9 learning-production skill family derived from the repository's `Grade9schema.md` and the proven linked textbook/question-bank workflow.

## Skills

| Skill | Purpose |
|---|---|
| `grade9` | Router/orchestrator |
| `grade9-source-grounding` | Source extraction, QC, provenance, verification |
| `grade9-concept-architect` | Stable concept IDs, prerequisites, learning graph, links |
| `grade9-question-bank` | Core N, same-level calibration, Level-Up challenges, mixed tests |
| `grade9-learning-enrichment` | Helpers, hints, misconceptions, diagnostics, transfer |
| `grade9-subtopic-completeness-auditor` | Whole-subtopic audit: source, instructional grammar, familiar/real-life bridges, helpers, misconceptions, practice, chemistry typography and layout |
| `grade9-transfer-coverage-auditor` | Subtopic-wise external/PYQ accounting; missing/duplicate placement; concept, hint, solution and source-link coverage |
| `grade9-redox-subtopic-book-builder` | Source-grounded Redox Study Guide + ExamSIDE transfer-book builder with approved textbook rhythm, Redox-specific helpers/misconceptions, chemistry typography, H1-H3 support, Appendix A, transfer audit and render-first QA |
| `grade9-textbook-publisher` | Kid-friendly linked textbook/question-bank PDF production and QA |
| `grade9-math` | Mathematics reasoning/difficulty profile plus SEE -> REALIZE -> UNDERSTAND -> ADOPT concept-book mode |
| `grade9-physics` | Physics model/representation/validation profile plus SEE -> REALIZE -> UNDERSTAND concept-book mode |
| `grade9-chemistry` | Chemistry macro-particle-symbolic/evidence profile |

## Shared contracts

- `shared/grade9-workflow.md` — operational cross-skill workflow.
- `shared/grade9-master.schema.json` — canonical reusable master-data schema.
- Repository root `Grade9schema.md` — fuller human specification and implementation history.
- `skills/grade9-math/references/concept-book-see-realize-understand-adopt.md` — reusable Mathematics Concept Book protocol.
- `skills/grade9-physics/references/concept-book-see-realize-understand.md` — reusable Physics Concept Book protocol.

## Redox subtopic-book mode

For the source-grounded Redox project, invoke `$grade9-redox-subtopic-book-builder` one subtopic at a time. It requires:

- a source-obligation ledger before drafting;
- the approved instructional grammar: orient/context -> explain -> visual/symbolic meaning -> key rule -> worked reasoning -> helper -> misconception repair -> guided/faded/independent practice -> transfer;
- Redox-specific reasoning patterns such as oxidation-number lanes, SELF vs OTHER for agents, the redox fingerprint, and split/converge topology;
- chemistry-safe subscripts/superscripts and `e⁻` notation;
- a frozen canonical ExamSIDE required set with exactly one primary subtopic per eligible question;
- difficulty-based H1-H3 support, Appendix A solutions, source links and bidirectional transfer coverage;
- render-first QA with repair/re-render before publication.

Run it together with `$grade9-subtopic-completeness-auditor` and `$grade9-transfer-coverage-auditor`.

## Subtopic completeness audit mode

Run `$grade9-subtopic-completeness-auditor` after a Study Guide / transfer-book draft exists and before publication.

The auditor requires the subtopic to prove:

- every assigned source obligation is taught;
- concept meaning appears before a procedure where the concept is new;
- at least one familiar/real-life bridge is used when safe, or `NOT_APPLICABLE` is recorded;
- reusable concept helpers exist for recognition-heavy concepts;
- high-risk misconceptions have explicit repair objects and retry checks;
- worked, guided, faded and independent practice are present as appropriate;
- chemistry formulas, subscripts, superscripts and ionic charges render correctly;
- titles/subtitles do not collide or clip;
- rendered pages read as coherent learning spreads rather than disconnected card dashboards;
- transfer coverage passes whenever an external corpus is part of the brief.

## Transfer coverage audit mode

When an external question corpus (for example ExamSIDE or another PYQ index) is part of the brief, run `$grade9-transfer-coverage-auditor` before declaring a subtopic complete.

The auditor requires:

- one scope status for every corpus item;
- exactly one primary subtopic for every eligible item;
- all required questions placed in the correct transfer book or explicitly deferred to a named future subtopic during incremental builds;
- stable concept links;
- difficulty-appropriate H1-H3 support;
- Appendix A solution coverage;
- original source-link validation;
- zero missing/duplicate primary placements and zero scope leaks at final acceptance.

## Mathematics Concept Book mode

For a Mathematics concept/reference book use:

`SEE -> REALIZE -> UNDERSTAND -> ADOPT`

- SEE the pattern/representation;
- REALIZE the invariant/hidden structure;
- UNDERSTAND by deriving/reconstructing and explaining the form;
- ADOPT by recognizing, choosing, transferring and rebuilding independently.

`CONNECT` remains the source-traceability/navigation layer.

The first worked Mathematics chapter exemplar is under:

- `Mathematics/Sequence and Series/`
- `skills/grade9-math/references/sequence-series-concept-book-example.md`

## Physics Concept Book mode

For a Physics concept/reference book use:

`SEE THE EQUATION -> REALIZE -> UNDERSTAND`

and retain `CONNECT` as the source-traceability/navigation layer.

The first worked Physics chapter exemplar is under:

- `Physics/Motion/`
- `skills/grade9-physics/references/motion-concept-book-example.md`

## Deterministic checks

- `skills/grade9-question-bank/scripts/difficulty_check.py`
- `skills/grade9-question-bank/scripts/validate_bank.py`
- `skills/grade9-textbook-publisher/scripts/check_master_links.py`

## Recommended invocation

Start with `$grade9` for multi-stage work. Invoke a specialist directly for narrow tasks, for example:

```text
Use $grade9-question-bank to build 30 same-level questions from these anchors.
Use $grade9-redox-subtopic-book-builder to build the next Redox subtopic with Study Guide + ExamSIDE transfer audit.
Use $grade9-subtopic-completeness-auditor to audit a drafted subtopic before publication.
Use $grade9-transfer-coverage-auditor to prove every eligible PYQ is covered against exactly one subtopic.
Use $grade9-math in Concept Book mode using SEE -> REALIZE -> UNDERSTAND -> ADOPT.
Use $grade9-physics in Concept Book mode using SEE -> REALIZE -> UNDERSTAND.
Use $grade9-textbook-publisher to publish this validated master JSON.
```

Each skill follows the Agent Skills folder structure with required `SKILL.md` and recommended `agents/openai.yaml` metadata.

## Schema status

This concept-book expansion does **not** migrate or redesign the Grade 9 master schema. It is a subject-specific authoring/pedagogy layer within the existing workflow.
