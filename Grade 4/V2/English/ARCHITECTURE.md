# Grade 4 English V2 Architecture

## Ownership

`Grade 4/V2/English/**` is the canonical Grade-4 English product namespace for source-to-publication authoring.

`Primary/**` remains reusable Primary/Common authority for Teacher Runtime semantics, diagnostic reasoning, source-boundary status values, and visual-first publishing principles. English V2 consumes those meanings; it does not redefine them in Publication.

## Product layers

```text
SourceAuthority
  -> CoreSkills
  -> LearningDesign
  -> Representation
  -> Publication
  -> Benchmarks / Acceptance
```

## Core invariant

Every learner-facing rule, classification, hint, worked example, response frame, misconception repair, rubric criterion, source-boundary statement, and fresh retry must be justified by a typed semantic or pedagogical object upstream of layout.

Layout may position or style validated English learning content. It may not invent pedagogy.

## Three evidence planes

### 1. Source evidence
What the supplied worksheet, textbook, teacher note, or question paper actually says.

### 2. Learner evidence
What the child selected, wrote, said, underlined, ordered, omitted, or revised, with response mode and support provenance.

### 3. Enrichment evidence
Research or broader language guidance used to explain or extend the source. Enrichment may not silently overwrite the assessment source model.

These planes must remain distinguishable in every handoff.

## English-specific invariants

1. Source taxonomies are authoritative for source-bound assessment answers. If a word does not fit cleanly, use `SOURCE_MODEL_BOUNDARY`, `AMBIGUOUS`, or `TEACHER_JUDGMENT`; do not invent a category.
2. Interpretive responses are evidence structures, not exact-string truth. Typical structures include `ANSWER + TEXT_CLUE + CONNECTION`, `CHOICE + JUSTIFICATION`, and rubric criteria for extended writing.
3. Oral and written response modes remain observable evidence and are not collapsed.
4. Conceptual support is separate from access support such as simpler wording, read-aloud, or oral response.
5. H1/H2/H3 support must fade to a fresh H0 independent retry.
6. Repeated same-route failure requires a materially different representation or diagnostic contrast, not another paraphrase of the same explanation.
