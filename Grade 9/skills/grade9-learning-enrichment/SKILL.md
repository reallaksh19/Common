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
