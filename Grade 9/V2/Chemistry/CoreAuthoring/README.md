# Chemistry V2 — C-G Promoted PCK and Core1 Authoring

C-G implements issue #269. It converts a C-F `LearnerStudyModel` into a treatment-relative Core1 semantic study plan using producer-legal **pilot** Chemistry PCK, new problem-family instances and mandatory Appendices A/B/C.

## Authority boundary

```text
C-F LearnerStudyModel decides treatment
+ C-D problem-family / reasoning authority
+ promoted-pilot Chemistry PCK supplies teaching affordances
+ C-G authoring profiles constrain authored instances
→ Core1 semantic study plan
```

PCK does **not** choose learner treatment and does not redefine canonical Chemistry. The PCK registry is promoted only for the C-G architecture pilot. Its records explicitly state that subject-expert and pedagogy-expert release authority are **NOT_GRANTED** and final-product release remains blocked. Raw mature-reference wording or page structure is not a producer input.

## Cross-topic PCK pilot

The registry includes the required families for representation translation, formula/charge anatomy, notation discrimination, conservation, rule/exception handling, observation→claim reasoning, process classification, species roles/spectators, structure/site reasoning, practical method/property links, chemical verification, causal misconception contrast and first-move support.

Redox-only assets (oxidation-state lanes, SELF/OTHER agent logic and split/converge topology) are explicitly topic-scoped and are not selected by a non-Redox StudyModel.

## Treatment-relative Core1

`ACTIVE_STUDY`, `REPAIR_BEFORE` and `REPAIR_IN_UNIT` receive the full semantic teaching path:

```text
familiar/macro anchor
→ representation
→ ordinary-language explanation
→ rule/model/condition
→ reconstruction
→ worked reasoning
→ concept helper
→ causal misconception repair + retry
→ guided
→ faded
→ independent
→ chemical verification
→ transfer bridge
```

`READY_VERIFY_ONLY` remains concise: activation, independent check and chemical verification. `PROBE_FIRST` remains a probe and does not silently become reteaching.

## New Core1 problems, not transfer leakage

Worked examples and Appendix A items are `NEW_AUTHORED_CORE1` problem instances bound to an upstream Chemistry problem family. They contain no external-candidate reference. Original external transfer/PYQ items remain reserved for Core2.

## Mandatory appendices

Every generated Core1 plan contains:

```text
Appendix A — Core Practice
Appendix B — Core Solutions
Appendix C — Printable Handout
```

Appendix A distributes guided/faded/independent practice according to treatment. Appendix B is one-to-one complete and includes reasoning plus an independent chemical verification route. Appendix C is answer-free, scope-bounded and carries grayscale/no-colour/notation-safe/standalone print constraints.

## Non-claims

C-G authors semantic instructional material and authoring plans; it does not claim renderer quality, exact page composition, authorized expert review, learning effectiveness, Core2 hint quality or publication readiness.
