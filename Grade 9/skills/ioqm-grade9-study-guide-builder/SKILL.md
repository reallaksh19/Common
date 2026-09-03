---
name: ioqm-grade9-study-guide-builder
description: Build or revise a Grade 9 IOQM study guide from existing repository material plus user-supplied questions/notes, with a 50%-prior-knowledge self-sufficiency audit, benchmark comparison, clean question appendices, quick-reference handout, source/citation ledger, and domain-specific authoring prompts.
---

# IOQM Grade 9 Study Guide Builder

## Purpose

Use this skill when the goal is not merely to collect solved questions, but to produce a **teacher-style study guide** that lets a Grade 9 learner with partial prior knowledge recognize and execute the methods needed for a supplied problem set.

This skill is deliberately different from a main-topic production package. It may synthesize several existing main topics into one revision/study guide, but it must preserve canonical topic ownership and must not silently create a new official syllabus.

## Core student standard

Assume the learner knows roughly 50% of the school-level background:

- familiar formulas may be remembered;
- routine exercises may be solvable;
- method recognition is inconsistent;
- nearby methods are confused;
- advanced Olympiad moves cannot be assumed.

The guide must therefore teach **enough to start and execute**, not merely name methods.

## Source roles

Classify every input before authoring.

### Authority source

Official/validated contest papers, frozen repository source maps, correction overlays, stable interfaces.

Use these for exact historical claims, answer custody and official-source statements.

### Comparison/practice source

User notes, coaching handouts, videos, DPP compilations, preparation routines, external question lists.

Use these to discover methods, teaching cues and practice coverage. Do not upgrade them to official authority.

### Internal quality benchmark

For Grade 9 mathematics, inspect:

`Grade 9/Mathematics/benchmarks/Quadratics_Assimilation_v2/README.md`

Use it as a quality comparator for:

- explanation completeness;
- missing-link repair;
- method contrast;
- attempt before answers;
- independence in starting unfamiliar problems;
- source/citation discipline.

Do not copy its wording, layout or exercises.

## Required pre-authoring audit

Before writing the guide, create a question inventory.

For every supplied question record:

- stable local question number;
- mathematical surface;
- primary method;
- secondary prerequisite;
- first useful line;
- difficulty of recognition;
- whether the current guide explicitly teaches the method;
- whether the current guide gives enough execution detail.

### Orphan-method test

A method is **orphaned** if a student must already know a trick that the guide only names.

Examples:

- “use derangements” without defining/counting derangements;
- “use Burnside” without a small-symmetry path or Burnside explanation;
- “degree 2 means cycles” without the labeled cycle-count formula;
- “use generating functions” without explaining coefficient extraction;
- “alternate inequalities” without showing how to count a small alternating pattern.

No supplied question may retain an orphan method.

## 50%-knowledge self-sufficiency gate

A question passes only if the guide contains all of the following:

1. **Prerequisite refresh** — the minimum background is stated or recalled.
2. **Recognition cue** — what in the wording/structure should trigger the method.
3. **First useful step** — an executable first mathematical line.
4. **Execution bridge** — enough explanation to finish the method without an unnamed trick.
5. **Legality/common-error check** — the nearby wrong move is identified.
6. **Practice isolation** — the question itself does not leak the method or answer unless the user asks for hints.

Record:

`STATIC_CONTENT_SELF_SUFFICIENCY = PASS_n_OF_n`

only when every supplied question passes.

This is not classroom evidence. Keep actual learner success, timing, retention and psychometrics unclaimed unless observed.

## Subtopic grouping rule

Do not group by the source document's lot/order unless that order is pedagogically strong.

Group by dependency:

1. fundamentals;
2. direct applications;
3. restricted/conditional variants;
4. representation changes;
5. advanced structures.

For combinatorics, a strong default progression is:

- counting foundations;
- selections and logical restrictions;
- distributions/multisets;
- linear arrangements;
- relative order/rank;
- circular symmetry;
- graphs/matchings/colorings;
- recurrence/state;
- number-theoretic counting;
- pigeonhole/extremal;
- invariants/games.

For other domains, derive a comparable dependency order from the repository topic map.

## Learner-facing style

Write like a strong teacher, not like an internal production system.

Prefer:

- “What should I notice?”
- “Why this works”
- “Try this first”
- “Common mistake”
- “When this method is not appropriate”
- short worked examples

Avoid learner-facing internal terms such as:

- wave;
- microstream;
- H0/H1/H2/H3;
- transfer gate;
- control plane;
- interface owner.

Internal QA documents may use technical production terminology when necessary.

## Worked-example rule

For every non-routine method needed by the supplied questions, include at least one **non-identical worked example**.

The example should reveal the mechanism without becoming a disguised copy of the appendix question.

## Appendix contract

### Appendix A — supplied questions

If the user asks for questions-only:

- reproduce every supplied question;
- remove solutions, tips, source commentary and module-position notes from the appendix;
- preserve all mathematical conditions needed to solve the question;
- place the answer key only after the final question.

Maintain source/provenance in a separate citation ledger.

### Appendix B — audit mock

Create a fresh mixed mock set when requested.

Rules:

- label author-created items as author-created;
- model method balance on verified historical repository patterns;
- do not claim an official Grade-9-only IOQM paper exists;
- include methods underrepresented by the supplied attachment but present in the canonical curriculum;
- answers only after the final mock question;
- independently recompute every answer.

## Quick-reference handout

Create a 1–2 page memory sheet when the subject benefits from formulas, legality checks or recognition cues.

The handout should contain only material worth recalling quickly:

- core formulas;
- compact method triggers;
- common legality conditions;
- high-value small constants/values;
- final pre-submit checklist.

Do not put full worked solutions in the handout.

## Citation and provenance rule

Provide citations wherever useful, but do not contaminate a questions-only appendix.

Preferred locations:

- source/citation ledger;
- chapter endnotes;
- teacher/reviewer manifest;
- stable historical ID references.

For a comparison source, preserve its uncertainty. Never turn “identified practice problem” into “confirmed official lecture question.”

## Independent cross-check

Before finalizing:

1. every supplied question appears exactly once in Appendix A;
2. no inline answers appear before the Appendix A answer key;
3. every Appendix A question maps to a taught method;
4. every non-routine method has an execution bridge;
5. Appendix B answer count matches question count;
6. every Appendix B answer is independently recomputed;
7. broader canonical curriculum gaps exposed by the source set are repaired or explicitly listed;
8. citations/source roles are recorded;
9. quick-reference content matches the main guide;
10. no unsupported classroom-effectiveness claim is made.

## Required output set

A practical study-guide package should contain:

```text
README.md
<Subject>_Study_Guide_vN.md
Quick_Reference_1or2pp.md
Appendix_A_<supplied-question-set>.md
Appendix_B_<mixed-mock>.md
Self_Sufficiency_Audit.md
Sources_and_Citations.md
```

For reusable agent operation also create or maintain:

```text
Grade 9/skills/ioqm-grade9-study-guide-builder/SKILL.md
Grade 9/skills/ioqm-grade9-study-guide-builder/references/domain-prompt-examples.md
Grade 9/skills/ioqm-grade9-study-guide-builder/references/self-sufficiency-audit-template.md
```

## Completion language

Use:

`STATIC_CONTENT_SELF_SUFFICIENCY = PASS`

only for document-level coverage.

Keep these separate unless measured:

- classroom readability/timing;
- learner solve rate;
- retention;
- psychometric calibration;
- qualification/pass-mark prediction.

## Final rule

A guide is not self-sufficient because it lists every formula.

It is self-sufficient only when a half-prepared student can move from **problem wording → recognized structure → first useful step → executable method** without needing an unnamed trick that exists only in the teacher's head.
