---
name: grade9-physics-examside
description: Build source-grounded Grade 9–11 Physics ExamSIDE/PYQ transfer question banks with complete question representations, verified exam metadata, staged H1/H2/H3 hints, conceptual solutions, Core links and frozen-corpus audits. Use when a Physics question-bank skill or external-exam assimilation workflow is requested.
---

# Physics ExamSIDE transfer practice

Build a question bank, not a second concept textbook. Use Physics teaching authority for modelling and `grade9-physics-publication` for rendering/audience rules. Keep it linked to the Core book; it does not replace Core Appendix A or Appendix B.

Read [question-contract.md](references/question-contract.md) before extracting or authoring. Read [source-ledger.example.json](references/source-ledger.example.json) for the ledger shape. Run `scripts/check_ledger.py` before declaring source completeness.

## Freeze the external corpus

1. Read the provided PDF/pages and every available diagram, option, table and source link. Save the immutable source and a hash. Define the selected chapter/subtopics, exams/date range and exact expected source IDs before layout.
2. Use exact URLs and verified exam/year/session metadata. “Looks like JEE” is not provenance. Do not fabricate or infer a missing question from its answer or a coverage map alone.
3. Keep raw source stem/options/figure locator/answer separate from adaptations and original support. Record every editorial change. Source ambiguity or corruption becomes REVIEW_REQUIRED.
4. Map each eligible question to one primary Physics concept and optional prerequisites. Record recognition/model choice separately from algebraic demand.
5. Do not shrink the expected question set because an item is awkward. Partition items with explicit reasons; a selected pilot must not claim the whole chapter or full ExamSIDE corpus.

## Teach through optional help

Preserve this learner order:

`question → representation/work space → stop boundary → optional H1/H2/H3 → complete solution at end`

- H1 Notice: point to the decisive clue without giving the answer.
- H2 Model: select or construct the physical representation; distinguish competing models.
- H3 Start: give the first executable relation or calculation, leaving the learner work to do.

Keep the three hints distinct and spatially separated from the first attempt. Separate hint pages are acceptable for print when page references and return links are provided. Full solutions follow all questions/hints at the end.

## Solution and linkage contract

Every solution contains a sufficient question recap, all necessary graph/table/option data, WHY the model applies, an executable METHOD, explicit ANSWER/CHECK, a CONCEPT TO KEEP and a return link. For B30, depict the completed model in the repair; for B80/B90, keep the decisive depiction even when arithmetic is compressed.

Link question↔solution, question↔hints and solution→Core concept. In a standalone PDF reproduce minimal concept help or provide a working companion-Core link plus printable title/section/page. Do not ship a dangling cross-file link. A generic “see concept book” is inadequate.

Use source-supported difficulty or clearly labelled editorial task-demand badges. Keep exam badges separate from learning-demand badges. Never display an exam badge for an original item.

## Executable demonstration

The sibling publication skill contains `examples/motion_question_bank_v2.json`, an **original-question** demonstration of the optional-hint layout. Render it with that skill's renderer. It proves that the question/hint/solution layout executes; it does not prove assimilation of a real ExamSIDE corpus. Its solutions reproduce minimal concept help because the demonstration is standalone.

For real external records, close the ledger here and populate the publication model's SOURCE_VERIFIED or ADAPTED question status plus `source_citation` (title, exact URL, locator, verification and adaptation note where applicable). The renderer prints question/solution source links and its audit checks the exact PDF URI annotations. Missing or unverified citations fail validation. Verification still requires inspecting the source; a checkbox is not evidence by itself.

## Audit before approval

Close every individual question: source mapped, attemptable, dependency visible, options complete, progressive optional hints, complete conceptual method, explicit answer, correct typography, resolved links and readable render. Aggregate counts do not substitute for this check.

Separate `PILOT_ORIGINAL`, `SOURCE_REVIEW_REQUIRED`, `SOURCE_RECONCILED`, `FOR_USER_REVIEW` and user approval. Reconcile frozen IDs with observed and published IDs; any unexplained loss blocks source-complete status. State unresolved sourcing honestly. Render every page and repair all labels/collisions before presenting for approval.
