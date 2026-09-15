---
name: grade9-learning-enrichment
description: Enrich validated Grade 9 questions and concepts with student-facing recognition prompts, helpers, progressive hints, misconceptions, error signatures, diagnostics, solution strategies, worked solutions, transfer questions, takeaways, and mastery evidence. Use after concept/question validation when the user wants textbook pedagogy, hints, misconceptions, tutoring support, or diagnostic learning material.
---

# Grade 9 Learning Enrichment

Transform validated questions into teachable learning objects without reducing the intended difficulty prematurely.

## Canonical learning sequence

```text
Question
  -> Concepts / prerequisites
  -> What should I notice?
  -> Helper
  -> Progressive hints
  -> Solution strategy
  -> Worked solution
  -> Misconception clinic
  -> Diagnostic / repair
  -> Transfer question
  -> Takeaway
```

## Recognition layer

`What should I notice?` identifies salient structure without solving the problem. It should train problem recognition.

## Helper rule

A helper answers: `What should I think about first?`

Prefer helper types such as:

- observation;
- representation;
- connection;
- model selection;
- evidence interpretation;
- validation.

Do not give away the setup in the helper.

## Progressive hint ladder

Default to 4-5 levels when appropriate:

- H1 ~10% reveal: direction only.
- H2 ~25%: relevant concept/model.
- H3 ~45%: representation/connection.
- H4 ~70%: equation or setup.
- H5 ~90%: final push, not the finished answer.

Challenge sections may use fewer initial hints.

## Misconception object

Misconceptions must describe a specific wrong mental model, not generic warnings.

```json
{
  "id": "M-001",
  "wrong_model": "...",
  "observable_error": "...",
  "diagnostic_question": "...",
  "repair_explanation": "...",
  "micro_example": "...",
  "transfer_check": "..."
}
```

## Error diagnosis

Use the causal sequence:

`wrong response -> likely misconception -> diagnostic probe -> targeted repair -> retry/transfer`

Do not infer a misconception solely from one arithmetic slip when several explanations are plausible.

## Solutions

Separate:

- `strategy` — the route before details;
- `worked_solution` — complete reasoning;
- `alternative_methods` — only when genuinely useful;
- `validation_check` — sanity/dimensional/logical check appropriate to the subject.

## Mastery evidence

Hint use can reduce strength of mastery evidence. A learner solving without hints or after H1 demonstrates stronger independent recognition than one requiring H4/H5.

Keep this as analytics metadata; do not shame the learner for using hints.

## Partial-knowledge learner mode

Some learners already know roughly half of a concept: formulas or definitions may be remembered, but connections, decision boundaries, first moves and transfer are unstable. For this learner:

- do not reteach from zero unless a diagnostic shows a genuine prerequisite gap;
- use a diagnostic to choose which bridge to teach, never as a pass/fail label;
- distinguish, for a wrong response: missing prerequisite, remembered-but-hollow formula, correct concept with a weak representation choice, recognition failure, and execution/calculation failure. These need different repairs, not the same reteach.

## First-Step Reference (companion product)

A First-Step Reference is a compression/revision product, built only after concept teaching is complete — it is not the teaching product and must not substitute for it. Keep it a distinct, named companion to the Concept Book/Study Guide and the Question Bank in each subject's own product architecture, rather than folding its role into either.

It should contain, as applicable to the subject:

- a recognition atlas: what should the learner notice first?
- a phrase/structure decoder: what wording maps to which concept/model?
- a decision router: given the recognition, which method/relation applies?
- first-step cards: the first executable line for each recognized pattern, not the full worked solution;
- contrast pairs: near-miss situations that require a different first step;
- a recognition-only drill: practice noticing and choosing, not solving to the end;
- a concise source-to-first-step map when a source corpus is in scope.

## Six-question assimilation test

For a concept a learner is expected to have fully assimilated, all six should be answerable without hints:

1. What did you notice?
2. Why does the method work?
3. What clue would make you think of it?
4. What similar-looking situation needs a different method?
5. Can you write the first useful line without help?
6. Can you solve a disguised (non-identical transfer) version?

Use this as a generic mastery/diagnostic template across subjects. A subject skill may extend it with subject-specific probes but should not replace its structure with a parallel one.
