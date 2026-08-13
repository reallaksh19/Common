---
name: grade9-concept-architect
description: Build stable Grade 9 concept IDs, prerequisite graphs, anchor mappings, mastery paths, and bidirectional textbook-to-question-bank links. Use when turning notes or anchor questions into a concept map, when linking practice/challenge questions to lessons, or when creating canonical master data for Mathematics, Physics, or Chemistry.
---

# Grade 9 Concept Architect

Turn source material into a stable learning graph before page layout.

## Core model

Every concept must have a stable ID independent of PDF page numbers.

```json
{
  "concept_id": "SEQ-C01",
  "title": "GP Roots and Vieta",
  "primary_anchor_ids": ["Q01"],
  "prerequisites": [],
  "same_level_question_ids": ["C21"],
  "challenge_question_ids": ["H01"],
  "misconception_ids": [],
  "mastery_path": []
}
```

## Required graph

```text
Concept
  <-> source anchor
  <-> same-level practice
  <-> next-level challenge
  <-> helper/hints
  <-> misconception diagnostic
  <-> answer/solution
  <-> mixed-test diagnosis
```

A question may map to several concepts, but every scored question must have exactly one `primary_concept_id` for navigation and analytics.

## Workflow

1. Read source-grounding records.
2. Cluster anchors by actual reasoning mechanism, not just chapter heading.
3. Assign stable concept IDs using a chapter prefix plus `Cnn`.
4. Identify prerequisite relationships.
5. Separate foundation concepts from synthesis concepts.
6. Map each anchor to its concept.
7. Map same-level practice and challenges after question-bank validation.
8. Generate mastery/review paths.
9. Export the graph into the canonical master data.

## Concept-title rule

Prefer titles that describe the reasoning move:

- `Recurrence -> Constant First Difference`
- `Macroscopic -> Particle -> Symbolic Translation`
- `Velocity-Time Graph Area`

Avoid vague labels such as `Hard AP Questions` or `Chapter 4 Practice`.

## Prerequisite rule

A prerequisite must help explain why a learner is stuck. Do not create decorative dependency edges.

## Publishing rule

Page numbers are render outputs. Do not store page numbers as the authoritative concept linkage. Publishers may derive page destinations from stable IDs.

## Completion gate

Do not pass the concept graph downstream until:

- every usable source anchor is mapped;
- no duplicate concept IDs exist;
- prerequisite cycles are resolved or explicitly justified;
- every scored question has one primary concept;
- challenge mappings preserve conceptual lineage.
