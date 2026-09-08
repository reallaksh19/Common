# Student Page QA for Grade 9 Publication

Use this checklist on every student-facing batch after source mapping and before release. These checks are additive to source-fidelity and link audits.

For long question banks, also read `question-bank-assimilation-integrity.md` and `student-first-question-bank-layout.md`.

## Artifact separation

Student materials and publisher/audit materials are different products.

- Student Core PDF: teaching, representations, equations, worked/guided practice, independent transfer, purposeful work space.
- Self-Check PDF: retrieval/self-check statements and revision prompts.
- Audit PDF / manifest: source mapping, provenance, QA counters, editorial exceptions, source-focus data, reconstruction notes.

Fail if the Student Core PDF contains process language such as `source mapping`, `audit`, `publication`, `reconstruction`, `moved to another PDF`, `QA`, `provenance`, or internal production status.

## Scaffold fidelity

Support must visibly fade by learning stage.

- Concept / worked / full-support guided: show the operative relation and the physical representation.
- Faded guided: keep recognition cues or partial variable/relation scaffolds, but remove some completed steps.
- Independent transfer: do not provide the formula or answer path when the source intentionally withholds it; provide a task-shaped neutral workspace only.

Fail if all three stages look equally scaffolded or equally blank.

## AD-13 MODEL VISIBILITY

On every quantitative worked or full-support guided page, the operative relation must be visible on that page, or on an intentional facing spread that is simultaneously visible in the target medium.

Fail if prose or hint text describes the formula but the equation itself is absent.

## AD-14 STUDENT-AUDIENCE PURITY

The Student Core PDF must contain zero publisher-process language. Move provenance, source focus, mapping, QA and reconstruction commentary to the Audit PDF.

## AD-15 TASK-SPECIFIC WORKSPACE

Work zones must match the actual cognitive task. Prefer prompts such as `mark start and finish`, `separate distance and displacement`, `fill the two numerators`, `draw velocity arrows`, or `inspect the final partial cycle` over generic `facts / reasoning / answer` boxes.

A neutral visual seed is allowed when it reduces drawing friction without giving away an intentionally withheld answer.

## AD-16 ZERO TEXT COLLISION

Run `scripts/check_text_overlaps.py` on every final PDF. Material cross-line text overlaps must be zero before release.

This does not replace visual inspection. False positives may be reviewed, but a known real overlap blocks release.

## AD-17 COMPONENT BOUNDS CONTRACT

Every reusable layout component must have a declared width and height. The component must render all labels, notes, arrows, equations and captions inside that rectangle unless overflow is explicitly part of its API.

Use the layout rule:

`reserve -> draw -> advance`

Do not place a fixed-height diagram and then continue text at a guessed y-coordinate.

## AD-18 COMPONENT CONTENT BUDGET

Before drawing a bounded component, calculate whether its text/equations fit its allocated width and height.

- wrap text before rendering;
- fit mathematical display size to the available width;
- reserve vertical lines before placing subsequent content;
- if content does not fit, enlarge the component, reduce noncritical decoration, or repaginate;
- never truncate a core equation or sentence to make it fit.

Fail if a sentence/equation is clipped, silently cut, continues under another component, or ends with an incomplete expression such as `use 2v1...`.

## AD-19 FORMULA LINE COMPLETENESS

Every displayed formula and every calculation step must be semantically complete and readable as a whole expression.

Fail if:

- the right-hand side is clipped;
- a numerator/denominator is visually separated from its fraction;
- a subscript/superscript collides with adjacent text;
- a formula wraps into prose in a way that changes interpretation;
- the equation is smaller than secondary helper prose on a full-support page.

For long equations, move them to their own display line instead of squeezing them into a narrow card.

## AD-20 NORMAL-VIEW READABILITY

Inspect renders at normal student viewing size, including a phone-width or fit-page view where applicable.

Pass only if:

- the main question and operative equation can be identified in a few seconds;
- body text does not require zoom for ordinary reading;
- diagrams remain legible and labels do not merge;
- large blank areas are purposeful work space rather than accidental layout voids;
- page furniture does not dominate the physics/mathematics.

## AD-21 ANSWER-CHOICE INTEGRITY

A student must never be asked to select an option that is not visible or otherwise recoverable in the student artifact.

For any multiple-choice, graph-choice, statement-set, matching, or `choose the correct curve` item, one of these must be true:

- all source-supported answer choices/graphs/statements are reproduced faithfully on the question page; or
- the student-facing task is transparently adapted into a standalone `sketch`, `describe`, `calculate`, or `state the criterion` task because the audited source does not preserve the choices, and the audit records that presentation adaptation; or
- the missing choices are reconstructed from approved source evidence and marked `RECONSTRUCT` with a semantic figure/choice audit.

The method/answer section must never stop at an orphan label such as `Option D`, `Graph 3`, or `(B), (C), (E)` when the choices are not visible there. It must include the semantic answer as well, for example:

`Option D - a straight a-x line with positive slope and negative intercept.`

Fail if:

- the question says `choose A-D` but A-D are not visible;
- the answer says only an option letter/number whose meaning the learner cannot see;
- the option label is clipped or truncated;
- a reconstructed option set is invented without source evidence;
- the publication silently converts an option-selection task without recording the adaptation.

## AD-22 TRUE MATH / SCIENCE TYPOGRAPHY

Student-facing mathematical notation must be typeset as mathematics rather than leaking source-authoring syntax.

Fail if student pages visibly contain source-style tokens such as:

- `x_f`, `v_i`, `a_avg`, `s_(n+2)`;
- `v1`, `v2`, `t1`, `t2` when those digits are mathematical indices;
- `sqrt(...)` instead of a radical;
- unintentional caret notation such as `t^2` when a true superscript is expected;
- `m/s2` when `m/s²` is intended;
- baseline ionic charges, chemical subscripts, or scientific exponents that should be raised/lowered;
- ambiguous unit notation caused by missing superscripts.

The raw/source token remains preserved in the audit model; only the student rendering is normalized typographically. Do not guess index versus exponent semantics from the token alone; resolve it from the source relation.

Run `scripts/check_math_typography.py` as a deterministic baseline, then visually inspect equations because a text scan cannot verify glyph placement.

## AD-23 REPRESENTATION-DEPENDENCY CLOSURE

If a question depends on a graph, diagram, table, timeline, number line, option figure, apparatus, geometry, or statement set, that representation is core content.

Pass only when:

```text
representation required by source = identified
representation present on student question = true
representation legible at normal view = true
critical labels/data preserved = true
```

If the solution/method section is intended to be standalone, also require:

```text
representation present in solution recap = true
```

Fail if the recap says `from the graph` while the graph is absent.

For source crops, include all axes/scales/labels/data used by the reasoning and exclude unrelated solution/hint text where practical. A tiny or over-cropped figure counts as missing.

## AD-24 SOLUTION SELF-CONTAINMENT

A learner opening a standalone solution must be able to identify the problem without returning to the source PDF.

Use this default structure for question banks:

```text
QUESTION RECAP
QUESTION FIGURE / OPTIONS / TABLE when required
WHY THIS WORKS
METHOD
ANSWER / CHECK
CONCEPT TO KEEP
RETURN TO QUESTION
```

The recap may be shortened only if target, data, units, conditions, sign/frame information and representation dependency remain unambiguous.

Fail if the solution depends on context not visible in the solution artifact.

## AD-25 METHOD ASSIMILATION: METHOD MUST NOT EQUAL ANSWER

The solution must teach a reusable reasoning move, not merely restate the result.

Fail if:

- `METHOD` is identical or near-identical to `ANSWER`;
- `METHOD` is only a memorized formula with no reason it applies;
- the decisive model/representation step is absent;
- the method skips directly to substitution/result;
- generic boilerplate is copied across questions whose reasoning differs;
- a method cannot be understood without a missing graph/table/options.

For a quantitative or model-based problem, require as applicable:

```text
WHY THIS WORKS = physical/mathematical/chemical reason
METHOD = question-specific executable route
ANSWER / CHECK = explicit result with units/sign/semantic option meaning
CONCEPT TO KEEP = transferable principle
```

Short conceptual questions may use concise versions, but `METHOD` and `ANSWER` must remain pedagogically distinct.

## AD-26 H1-H3 PROGRESSIVE REVEAL

For question-bank practice pages the default eye path is:

```text
QUESTION
-> WORK HERE
-> STOP / optional hint boundary
-> H1 NOTICE
-> H2 MODEL
-> H3 START
```

H1-H3 must become progressively more concrete. Numerical intermediate detail is allowed when it is the useful next step.

Fail if:

- hints are above/beside the work zone and read accidentally;
- H1 reveals the final answer;
- H1-H3 repeat essentially the same sentence;
- H3 is still generic rather than executable;
- hint equations collide or clip.

## AD-27 QUESTION-LEVEL CERTIFICATION

For a question bank, page-level or PDF-level completeness is not enough. Every question must close individually.

Required per-question state:

```text
source question mapped = true
question attemptable = true
representation dependency closed = true
answer-choice dependency closed = true
hints progressive = true
solution self-contained = true
method distinct from answer = true
method teaches transferable reasoning = true
answer explicit = true
math/science typography ok = true
question->solution link ok = true
solution->question link ok = true
render readable = true
```

Any failed question blocks the batch.

## AD-28 COPY-PASTE / TEMPLATE DRIFT

Repeated visual structure is allowed; repeated reasoning that does not fit the question is not.

Inspect each batch for:

- identical `WHY THIS WORKS` text across different concept families;
- identical `METHOD` text where numbers/conditions/representations differ materially;
- stray production tokens such as `SUBTOPIC`, placeholder text, truncated labels, or inherited answer fragments;
- figures copied to questions that do not semantically match them;
- a solution answer pulled from a neighboring question.

If found, stop generation and re-audit the affected batch from the source pages.

## Required pre-release sequence

1. freeze the question/source denominator;
2. classify representation and answer-choice dependencies for every question;
3. render every page;
4. run text-overlap preflight;
5. run math-typography preflight;
6. run bounds/content-budget checks for reusable components;
7. inspect all pages in a contact sheet for rhythm and density;
8. inspect every quantitative page at 100% for complete formulas;
9. inspect every guided/independent page for scaffold fidelity;
10. verify every choice-based question against AD-21;
11. verify every representation-dependent question against AD-23;
12. verify every standalone solution against AD-24 and AD-25;
13. verify H1-H3 progression against AD-26;
14. verify every question reaches AD-27 closed state;
15. inspect batch for AD-28 copy-paste/template drift;
16. verify Student Core, Self-Check and Audit separation;
17. repair, re-render and repeat until all blocking counters are zero.

Any failed checkpoint blocks the batch until repaired and re-rendered.