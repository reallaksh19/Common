---
name: grade9-concept-architect
description: Build stable Grade 9 concept IDs, prerequisite graphs, source-anchor mappings, practice/challenge links, mastery paths, and bidirectional textbook-to-question-bank navigation. Use when converting notes or questions into a concept map or canonical learning graph for Mathematics, Physics, or Chemistry.
---

# Grade 9 Concept Architect

Every concept uses a stable ID independent of page numbers.

```text
Concept
  <-> source anchor
  <-> same-level practice
  <-> next-level challenge
  <-> helper / hints
  <-> misconception diagnostic
  <-> answer / solution
  <-> mixed-test diagnosis
```

A question may map to multiple concepts, but every scored question must have exactly one `primary_concept_id`.

Workflow: consume grounded source records; cluster by reasoning mechanism; assign `<CHAPTER>-Cnn`; identify meaningful prerequisites; separate foundations from synthesis; map anchors; add validated practice/challenges; add misconception/mastery/review paths; export to master data.

Prefer reasoning-action titles such as `Recurrence -> Constant First Difference` or `Velocity-Time Graph Area`; avoid labels like `Hard Questions`.

Do not pass downstream until anchors are mapped, IDs are unique, prerequisite cycles are resolved or justified, every scored question has one primary concept, and challenge mappings preserve lineage.
