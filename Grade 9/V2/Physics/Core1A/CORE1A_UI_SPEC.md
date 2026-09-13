# Core (1A) learner UI specification

This specification is normative for the learner surface produced by Core (1A). It exists to prevent a visual from replacing the teaching, to make low-readiness learning explicit, and to connect each Subtopic Bucket Assimilation (SBA) unit to the exact Core (2) transfer families it prepares.

## 1. First publication surface: SBA bucket map

Every chapter sequence starts by publishing the SBA bucket table with these columns:

`SBA index | Subtopic bucket | Origin | Core (1A) teaching home | Core (2) primary questions | State`

The table is not decorative. It tells the learner/teacher what each bucket owns and gives later agents a stable semantic map independent of page numbers.

## 2. Teaching is primary; illustration is support

For a low-readiness learner, a concept is incomplete if it only has prose, only has a formula, or only has a diagram.

Use this macro-sequence when applicable:

`FOUNDATION / PRETRAINING → STORY / PHENOMENON → PLAIN LANGUAGE → STAGED PICTURE → WHAT CHANGED PHYSICALLY? → PICTURE-TO-MATHS → MODEL/VALIDITY → MISCONCEPTION → WATCH ONE → COMPLETE ONE → PROBLEM-FAMILY ROUTINE → INDEPENDENT PRACTICE → HINTS → READINESS → CORE (2) TRANSFER`

A hard concept means **more pictures and fewer inferential jumps**, not smaller text or denser pages.

## 3. Difficulty and learner readiness are separate

Difficulty describes the concept. Readiness describes the learner.

| Badge | Meaning | 20% learner expectation |
| --- | --- | --- |
| `D1 FOUNDATION` | direct/essential idea | rebuild basics, one or more explanatory visuals, direct retrieval |
| `D2 THINK CAREFULLY` | representation/equation connection | prerequisite bridge, staged visual, misconception contrast, worked + guided practice |
| `D3 CHALLENGE` | inverse/event/multi-representation reasoning | full foundation path, several visual stages, explicit model conditions, worked + completion + independent practice |
| `D4 STRETCH` | advanced/extension bridge | full prerequisite rebuild, explicit derivation and transfer framing when Core (2) requires it |

Badges are support contracts, not decoration.

## 4. Staged illustration contract

Illustrations are first-class instructional objects.

- keep a stable coordinate frame unless a frame change is itself the idea;
- use one conceptual change per stage;
- place labels next to the represented object;
- keep words and graphics spatially adjacent;
- show sign/direction changes visually when they matter;
- for D2/D3, use staged representations rather than one static diagram when the concept changes through time or across cases;
- unresolved label collision or panel overflow is a build failure;
- the completed figure is treated as one bounded layout object.

Each difficult figure should answer: **What should the learner notice before the equation appears?**

## 5. Problem-family assimilation layer

Core (1A) must not end with a flat list of Core (2) question numbers when several questions share distinct attack patterns.

Cluster questions into problem families. Each family uses the same learner grammar:

`LOOK FOR → STEP 1 → STEP 2 → STEP 3 → ... → WATCH/COMPLETE analogue → INDEPENDENT PRACTICE → OPTIONAL H1/H2/H3 → READY TO MOVE ON? → exact Core (2) questions`

The numbered method should tell the learner what to do when they recognise that family. The earlier conceptual pages explain why the method works.

Question-load scaling:

- 1–2 primary questions: one or more routines as needed;
- 3–5: split by recognition signal / first move;
- 6–9: expanded transfer section, normally at least three families;
- 10+: explicit family map first, normally at least five families, with proportionately more transfer elaboration.

Do not compress a very-high-load bucket into one generic end page.

## 6. Independent practice is mandatory

Guided practice is not the same as independent practice.

For every released problem family, provide a fresh analogous problem where the learner attempts first.

Preferred static-PDF sequence:

`INDEPENDENT PRACTICE → blank working space → turn page / uncover next section only if help is needed → H1 → H2 → H3 → answer check`

Do not expose all three hints before the learner has a chance to attempt the problem when the design claims progressive support.

## 7. Hint ladder contract

Core (2) uses protected hints:

- `H1` — key physics;
- `H2` — representation/model;
- `H3` — first mathematical move.

Core (1A) must pre-teach every reveal before transfer. Core (1A) independent-practice hints may mirror this progression, but they are still teaching support.

A topic-level link is not sufficient. Every H1/H2/H3 must trace to an earlier learning atom and to an example/check.

## 8. Readiness gate is mandatory

Every released problem family ends with `READY TO MOVE ON?` covering four abilities:

1. **RECOGNISE** — identify the family from the wording/signals;
2. **REPRESENT** — draw/write the correct model without help;
3. **FIRST MOVE** — choose the first useful equation/condition without H2/H3;
4. **FINISH** — solve and physically check a fresh analogous problem.

Recommended release rule: 4/4 without H2/H3. Otherwise point the learner back to the exact learning atom or routine.

## 9. Core (2) transfer and release control

Use exact `Qxx` identifiers from Revised Core (2) v2.

A primary question may be owned by one SBA but held until another prerequisite bucket is complete. This must be explicit in the build manifest.

Examples:

- SBA-03 owns Q43 conceptually but holds release until SBA-04 teaches the apex event.
- SBA-04 owns Q14/Q27 but holds release until SBA-05 supplies the same-height relation needed to finish them.

Never imply that a held question is ready merely because its primary bucket has been taught.

## 10. Misconception box contract

For D2/D3 learners, prefer a conceptual-change sequence instead of a one-line correction:

`WHAT SOME STUDENTS THINK → LOOK AT THE EVIDENCE / PICTURE → WHAT MUST BE TRUE? → REBUILD THE IDEA`

Use `Easy mistake to make` as the learner-facing label when space is limited.

## 11. Typography and layout

- A4, stable margins;
- textbook body target around 10.5–11 pt, hard floor defined by publication policy;
- diagram labels readable without zooming;
- heading/badge areas may not collide;
- use real Greek symbols, subscripts, superscripts, fractions and radicals;
- no learner-facing raw strings such as `sqrt(...)`, `theta`, `v_A/B`, or `u^2`;
- major diagrams require captions and label-safe space;
- avoid one-card-per-page rhythm when explanation + figure + equation form one learning unit;
- do not squeeze a high-load transfer section to preserve an arbitrary page count.

## 12. Visual audit

Automated checks are necessary but not sufficient. Render every release candidate to page images and visually inspect it.

Reject:

- clipping, overlap or broken glyphs;
- unresolved diagram-label collision;
- raw math notation;
- blank pages or accidental large voids;
- D2/D3 pages with equations but no explanatory representation;
- independent-practice pages that reveal the full method before the attempt;
- missing readiness gates;
- flat Core (2) lists where problem-family routines are required;
- question release that ignores prerequisite buckets;
- topic leakage beyond authorised source/Core (1) scope.

## 13. Gold-standard process references

Use these as process references, not fixed page-count templates:

- `M2D-SBA-03`: low question load; one main transfer routine; independent practice + separate hints + readiness.
- `M2D-SBA-04`: high load; several velocity-event routines; explicit cross-bucket hold/release.
- `M2D-SBA-05`: very-high load; publication map first, family map, expanded transfer section and multiple readiness gates.

The exact execution order is defined in `AGENT_RUNBOOK.md`; machine state is defined in `registry/physics-core1a-motion-in-a-plane-build-state-v1.json` and per-bucket build manifests.

## 14. Compatibility aliases for existing policy/tests

The publication-policy registry still contains legacy machine labels such as `D3 CHALLENGING` and the older gateway phrase `CHECK → APPLY → CORE (2) TRANSFER`. Treat these as compatibility aliases, not as a reason to simplify the newer SBA flow.

The current learner-facing flow is richer: independent attempt, optional hints, readiness, then transfer. When a learner is stuck, the backward link must still point to the **exact repair target**: the named Core (1A) learning atom or transfer routine that addresses the missing idea.
