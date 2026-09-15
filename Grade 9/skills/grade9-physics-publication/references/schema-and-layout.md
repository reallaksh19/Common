# Schema and layout contract

The executable Pydantic classes in `scripts/validate_v2.py` are authoritative. Export the matching JSON Schema with `python scripts/validate_v2.py --schema`. The renderer validates before drawing; unknown fields fail.

## Objects

| Object | Required meaning |
|---|---|
| Model | Version, product, band, syllabus scope, placement evidence, status, frozen question count, concepts, sources |
| Product identity | Stable model ID, pair ID, role and reciprocal companion model ID for the Core Study Guide / ExamSIDE Solution Book pair |
| Lesson | ID, title, situation, FINAL figure, caption, ordered heading/body/equation blocks, takeaway, concept/source IDs, optional practice IDs |
| Figure | ID, supported kind, final status, exact numerical/relational data |
| Question | ID, visible label, full prompt, primary/secondary concepts, source status, figure or deliberate workspace, task badge, H1–H3, recap, why/method/answer/keep, repair target |
| Difficulty badge | Normalized D1–D5 band, deterministic learner label (`D1 Easy`, `D2 Medium`, `D3 Hard`, `D4/D5 Challenge`), evidence basis and untouched source code when source-mapped |
| Guided solution | Linked guided-lesson ID, step-by-step feedback and a completed depiction |
| Handout | Self-contained visual recap of both subtopics with symbol meanings and conditions |

The canonical per-topic production contract is exactly two models/files: `study_guide` with role `CORE_STUDY_GUIDE`, and `transfer_book` with role `EXAMSIDE_SOLUTION_BOOK`. Both carry reciprocal `product_identity` values. Validate them together with `python scripts/validate_v2.py --pair <core.json> <examside.json>`; this checks pair identity, topic/project scope, canonical concept authority and concept segregation. Legacy `core` and `question_bank` remain bounded pilot profiles and cannot claim canonical pair completion.

The Core Study Guide renders Appendix A Core practice, Appendix B optional hints/full solutions, and Appendix C printable handout, in that order. The ExamSIDE Solution Book renders external attempts with visible concept/task/difficulty labels, concept-hidden mixed transfer, optional hints, post-marking diagnosis and Appendix A full solutions. Its external corpus and source fidelity still require the ExamSIDE ledger/reconciliation gates.

Question source status is ORIGINAL, SOURCE_VERIFIED or ADAPTED. The last two require a verified citation with a short title, exact HTTPS URL and locator; ADAPTED also requires an adaptation note. The renderer prints a source link on the question and solution. Real ExamSIDE records must additionally close the separate frozen source ledger. Do not relabel the original pilot to pretend it verifies a corpus. The supplied handout is a bounded two-topic profile, not an arbitrary whole-textbook schema.

## Exact figures

- Number line: range, ticks, ordered positions, leg labels and optional displacement arrow. Validate positions and leg count.
- v–t graph: axis ranges/units, ticks, contiguous `[t₁,v₁,t₂,v₂]` segments and optional area shading. Preserve zero and all values; do not expose answers in assessment figures.
- Tiles: positive row/column count, cell meaning and time-column grouping.
- Comparison: two complete labelled depictions.
- Blank workspace: deliberately withheld student construction; never use it as the first required concept depiction.

Data drives vector geometry. Independently recompute route lengths and signed areas, splitting crossing segments for distance. Check graph data against numeric-check data and the actual prompt. Machine equality is not a semantic reading of the question.

For future figure types extend schema, renderer, bounds checks and tests together. Unsupported diagrams must fail rather than silently become placeholders.

## Placeholders

Keep production-only placeholder records separately with ID, concept, purpose, semantic axes/objects/labels/data, required dimensions, evidence and owner. Mark PLACEHOLDER or REVIEW_REQUIRED. They are invalid learner-renderer input. The final concept depiction must be FINAL and semantically reviewed. An intentionally absent assessment drawing is a different state and must be justified by the task.

## Page grammar

Use A4 landscape for this profile, 40 pt side margins, 12 pt instructional body, 11.5 pt solutions/hints, at least 10.5 pt figure labels, 9.5 pt footer and 17 pt equations. Reflow or repaginate; do not shrink to fit.

Concept pages pair a large functional depiction with a nearby explanation and a single takeaway. Alter this geometry for other relationships when needed. Guided pages visibly withhold a step. Practice pages offer work space before optional help. Hint pages stack H1/H2/H3. Solutions put recap before reasoning and reproduce necessary figures. The Appendix C handout is printable alone.

Reserve → measure/wrap → draw → advance. Each component owns its rectangle. Text exceeding its budget raises an error. Inspect shapes and labels too; successful text wrapping does not establish diagram bounds.

## Links, sources and badges

Use stable IDs for question→hint, question→solution, reverse links and Core lesson repair links. Generate printable page references from the actual pagination plan, then compare that plan with produced destinations. A standalone external question bank needs a valid companion-Core citation or reproduced concept help.

Keep hashes, pipeline terminology and audit statuses in the review report. Learner source citations can be useful, but never invent exam/year/session or claim source completeness. Identify original questions on the question-bank entry surface. Use task badges, not unearned mastery/approval badges.

Audit model validation, numeric cases, actual PDF links, appendix order, layout regions, font floors, render evidence and final hashes. Keep teacher review separate from machine checks.
