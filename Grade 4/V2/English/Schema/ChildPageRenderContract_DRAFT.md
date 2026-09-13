# Grade 4 English - Child Page Render Contract (DRAFT)

**Status:** DRAFT - English child-facing specialization of `Grade4PublishingSchema.md` and `Grade4VisualPublishingAcceptance.md`  
**Scope:** learner-facing Grade 4 English pages  
**Purpose:** turn child-friendly layout from an editorial preference into a testable page-plan contract.

---

## 1. Parent contracts

This contract does not replace the shared publishing system.

It inherits:

- structured content before layout;
- A4 output profiles and shared typography minimums;
- explicit writing-space allocation;
- reusable page components;
- student/adult edition separation;
- PDF -> page-image -> visual-QA release flow.

Where this draft is more specific, it constrains Grade 4 English child pages only.

---

## 2. Allowed learner page roles

A golden child-facing lesson should compose from these roles:

```text
NOTICE
UNDERSTAND
WATCH_ONE
TRY_ONE
BOUNDARY
FRESH_RETRY
TRANSFER
REVIEW
```

Every page declares exactly one `dominant_move`:

```text
NOTICE
EXPLAIN
MODEL
CLASSIFY
ORDER
REPAIR
APPLY
REVIEW
```

A page may contain supporting elements, but they must serve that one move.

---

## 3. Measurable child-load defaults

Unless a reviewed exception is recorded, a student page must satisfy:

```yaml
child_load:
  max_new_rules: 1
  max_explanation_chunks: 3
  max_instruction_words: 18
  max_dense_rule_blocks: 1
  require_learner_action: true
  require_instructional_visual_on_teaching_pages: true
  min_body_pt: 10.5
  min_question_pt: 11
```

These are page-plan gates, not a substitute for visual inspection.

A `REVIEW` page may contain several short retrieval prompts because the dominant move remains retrieval/review.

---

## 4. Learner action contract

Every page must include one observable child action near the teaching it checks.

Allowed action families include:

```text
NOTICE
POINT
CIRCLE
UNDERLINE
MATCH
CLASSIFY
ORDER
COMPLETE
CHOOSE
EXPLAIN
WRITE
CHECK
CREATE
```

For actions that require handwriting, the page plan must declare response space explicitly. Do not infer space from prompt length.

---

## 5. English visual-model requirement

Teaching pages use a recurring instructional visual rather than decorative art.

For the adjective golden lesson, the persistent models are:

```text
NOUN PHRASE BUILDER
ADJECTIVE FAMILY CARDS
ADJECTIVE ORDER TRAIN
BOUNDARY STAR
```

The same category names and order must remain visually stable across pages.

---

## 6. Boundary-star rendering rule

A source-boundary adjective is rendered with a star marker, never as a new category box.

Child meaning:

```text
STAR = still a describing word; our book does not give it a box.
```

Internal labels such as `SOURCE_MODEL_BOUNDARY`, provenance enums, validation codes, or authority names must not render on `CHILD_SURFACE`.

A boundary page must visually separate:

1. the book boxes that are known;
2. the starred extra describing word;
3. the completed phrase;
4. the child action.

The starred word may be placed in the completed phrase only when the underlying content record carries non-unresolved phrase-placement authority.

---

## 7. Page anatomy

A normal student page should use this hierarchy:

```text
PAGE ROLE / SHORT TITLE
LEARNING GOAL OR CUE
INSTRUCTIONAL VISUAL
ONE SHORT EXPLANATION OR MODEL
CHILD ACTION
RESPONSE SPACE / SELF-CHECK
```

Avoid:

- adult notes above the child task;
- repeated rule paragraphs;
- more than one competing visual organizer;
- shrinking type to save a page;
- answer-key explanations on the student surface.

---

## 8. Golden adjective lesson acceptance

The golden render must demonstrate all of the following:

```text
[ ] one dominant move per page
[ ] nine-position school model is frozen for the lesson fixture
[ ] category cards recur consistently
[ ] order train uses the same category sequence
[ ] at least one worked boundary case uses the star treatment
[ ] boundary word does not create a new box
[ ] guided practice follows a model
[ ] fresh retry changes lexical surface
[ ] review includes delayed-retrieval instruction
[ ] child surface contains no internal schema labels
[ ] response space is visible where handwriting is requested
[ ] page images are visually inspected after PDF render
```

The fixture may retain `OWNER_CONFIRMED_PENDING_PRIMARY_SOURCE` internally while primary-workbook verification is outstanding. That status must not appear on child pages.

---

## 9. Release blockers

Fail child-page QA when any of these occurs:

```text
MULTIPLE_DOMINANT_MOVES
TOO_MANY_NEW_RULES
INSTRUCTION_TOO_LONG
TOO_MANY_EXPLANATION_CHUNKS
MISSING_LEARNER_ACTION
MISSING_INSTRUCTIONAL_VISUAL
MISSING_RESPONSE_SPACE
INTERNAL_LABEL_LEAKED_TO_CHILD_SURFACE
BOUNDARY_RENDERED_AS_CATEGORY
BOUNDARY_PLACEMENT_UNRESOLVED
TEXT_BELOW_SHARED_MINIMUM
PAGE_IMAGE_NOT_VISUALLY_REVIEWED
```

These diagnostics are internal only.

---

## 10. Adoption rule

This draft can be used for golden renders and supervised learner trials immediately.

It remains non-canonical until:

1. the primary adjective workbook taxonomy/order is verified;
2. the golden PDF passes page-image review;
3. a supervised Grade 4 learner can follow the page routine without adult translation;
4. selected clauses are migrated deliberately into the canonical Grade 4 English and publishing contracts.
