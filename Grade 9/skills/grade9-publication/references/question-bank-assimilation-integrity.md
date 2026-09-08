# Question-Bank Assimilation and Dependency Integrity

Use this reference for any long practice book, transfer book, worksheet collection, PYQ book, or question-plus-solution publication reconstructed from a source PDF.

The governing rule is:

> **A student must be able to understand, attempt, and check every question from the published artifact without reconstructing missing context from the source.**

Source preservation is necessary but not sufficient. A publication fails if it technically contains the question and answer yet removes the graph, options, table, notation, reasoning, or context required for learning.

## 1. Per-question contract

Create one record for every published question before layout. Minimum fields:

```text
question_id
source_page
set_id
question_family
question_recap_complete
representation_dependency
representation_source_status
representation_present_student
representation_present_solution
answer_choice_status
h1_status
h2_status
h3_status
method_has_why
method_has_executable_route
method_distinct_from_answer
answer_present
concept_to_keep_present
math_typography_ok
question_to_solution_link_ok
solution_to_question_link_ok
source_link_ok
status
```

Do not scale layout until this record exists for every question.

Allowed `representation_dependency` values:

```text
NONE
GRAPH
DIAGRAM
TABLE
TIMELINE
NUMBER_LINE
OPTION_FIGURES
STATEMENT_SET
MIXED
```

Allowed `representation_source_status` values:

```text
PRESENT_SOURCE
INTENTIONALLY_ABSENT
SOURCE_CORRUPT
SOURCE_INCOMPLETE
RECONSTRUCT_APPROVED
REVIEW_REQUIRED
```

Allowed `answer_choice_status` values:

```text
NOT_APPLICABLE
VISIBLE_SOURCE
VISIBLE_PUBLISHED
TRANSPARENTLY_ADAPTED
RECONSTRUCT_APPROVED
REVIEW_REQUIRED
```

Any `REVIEW_REQUIRED` blocks release.

## 2. Representation-dependency closure

If the question says or implies any of the following, treat the representation as core content:

- `from the graph`;
- `as shown in the figure`;
- `using the table`;
- `choose the corresponding curve`;
- `which of the following diagrams`;
- `statement I / statement II` when the statements are not in the prose recap;
- geometry or apparatus whose dimensions/labels carry data.

A question with a representation dependency must satisfy:

```text
representation_present_student = true
```

If the solution/method section is designed to be usable independently, it must also satisfy:

```text
representation_present_solution = true
```

A text recap such as `Find distance from a v-t graph` is not self-contained if the graph is absent.

### Crop fidelity

When preserving a source figure by cropping/rendering:

- include every axis, scale, label, arrow, legend, shaded region, option label, dimension, and datum used by the reasoning;
- exclude unrelated question text, hints, solution text, or neighboring cards where practical;
- do not crop away zero lines, axis origins, negative regions, option letters, units, or endpoint values;
- inspect the crop at normal student size, not only at high zoom;
- if the crop is too small to read, redraw semantically or allocate more space.

A crop that is technically present but pedagogically unreadable counts as missing.

## 3. Answer-choice integrity

Never ask the learner to select an invisible option.

For MCQ, graph-choice, matching, statement-set, or curve-choice items, one of these must be true:

1. all source-supported choices are visible in the student artifact;
2. the task is transparently adapted into a standalone `calculate`, `describe`, `sketch`, or `state the criterion` task using only source-supported semantics;
3. the missing choices are reconstructed from approved source evidence and audited.

Never invent options from general knowledge.

If the method book says `Option D`, the semantic meaning must also be present unless the choices are visible there:

```text
Option D — straight a-x line with positive slope and negative intercept.
```

Reject orphan answers such as:

```text
D
Graph 3
A, B and D only
(B), (C), (E)
```

when the referenced choices are not visible.

## 4. Solution assimilation contract

A solution section is not an answer key with extra words. It must teach the reusable concept.

Default structure:

```text
QUESTION RECAP
<enough wording to identify the task without changing data>

QUESTION FIGURE / OPTIONS / TABLE
<when representation-dependent>

WHY THIS WORKS
<physical, mathematical, chemical, or conceptual reason for the model>

METHOD
<question-specific executable route with intermediate reasoning>

ANSWER / CHECK
<final answer, units, sign, option meaning, or criterion>

CONCEPT TO KEEP
<one transferable idea for the next problem>
```

Not every conceptual question needs long prose, but the method must remain pedagogically distinct from the answer.

### Method-distinctness gate

Fail when any of these is true:

- `METHOD` is identical or near-identical to `ANSWER`;
- `METHOD` merely states a memorized formula with no reason it applies;
- `METHOD` skips the decisive modeling step;
- `METHOD` gives only the final substitution/result;
- a generic method is copied across questions whose decisive reasoning differs;
- the explanation depends on a missing graph/table/options.

For example, reject:

```text
METHOD
Equal distances -> 2v1v2/(v1+v2)

ANSWER
2v1v2/(v1+v2)
```

Prefer:

```text
WHY THIS WORKS
Average speed is total distance / total time. Equal-distance legs generally take unequal times, so the arithmetic mean of speeds is not valid.

METHOD
Let each leg be x. Total distance = 2x and total time = x/v1 + x/v2. Therefore
v_avg = 2x / (x/v1 + x/v2) = 2v1v2/(v1+v2).

ANSWER / CHECK
v_avg = 2v1v2/(v1+v2).

CONCEPT TO KEEP
Equal-distance average speed is time-weighted; for two legs it has the harmonic-mean form.
```

The learner should finish the solution knowing **why** the relation applies, not only what formula to copy.

## 5. Question recap integrity

A solution recap may be shorter than the source question only when all of these remain explicit:

- target quantity;
- numerical data;
- units;
- conditions/constraints;
- direction/sign/frame information;
- referenced representation;
- choice semantics when needed.

Do not shorten away the very condition that makes the method valid.

## 6. Progressive H1-H3 integrity

Hints must be below the work area and become progressively more concrete.

```text
H1 NOTICE  -> decisive clue/data interpretation
H2 MODEL   -> representation/model/intermediate quantities
H3 START   -> first executable calculation/equation/substitution
```

Numerical detail is allowed when it is the useful next step.

Fail if:

- H1 gives the final answer;
- H1-H3 repeat essentially the same sentence;
- H3 is still generic and not executable;
- hints sit beside/above the question and are read accidentally;
- equations overflow because the component was designed only for short prose.

## 7. True math/science typography

Student-facing notation must be publication notation, not source-authoring syntax.

Examples:

```text
v1 -> v₁
v2 -> v₂
t2 -> t² only when exponent semantics are intended
t_2 -> t₂
s_(n+2) -> sₙ₊₂ or properly typeset equivalent
sqrt(t1 t2) -> √(t₁t₂)
m/s2 -> m/s²
```

The semantic source form stays in the audit model. The learner sees correctly typeset notation.

Do not guess subscript versus exponent semantics from typography alone; determine it from the source relation.

## 8. Per-batch drift gate

After every 5-10 questions or one complete set, run this exact review:

```text
QUESTION COUNT frozen = published count
REPRESENTATION DEPENDENCIES unresolved = 0
INVISIBLE CHOICES = 0
QUESTION RECAP failures = 0
HINT PROGRESSION failures = 0
METHOD≈ANSWER failures = 0
METHOD missing WHY / model reason = 0
METHOD missing executable route = 0
ANSWER missing semantic meaning = 0
MATH TYPOGRAPHY failures = 0
QUESTION->SOLUTION broken links = 0
SOLUTION->QUESTION broken links = 0
TEXT OVERLAPS = 0
```

Any non-zero count stops the batch. Repair before generating more pages.

## 9. Representation-first audit order

For each question, inspect in this order:

```text
1 source question wording
2 source figure/options/table
3 source hint route
4 source solution/answer
5 published student question
6 published hints
7 published standalone solution
```

This order prevents a common drift pattern: extracting the prose and answer first, then forgetting that the source graph/options were part of the actual problem.

## 10. Final acceptance

A question-bank publication is not ready until every question is individually closed:

```text
question source obligation = mapped
question representation dependency = closed
question is attemptable = yes
hints are optional/progressive = yes
solution is self-contained = yes
method teaches transferable reasoning = yes
answer is explicit = yes
notation is correct = yes
links resolve = yes
render is readable = yes
```

The unit of certification is the **question**, not merely the page or PDF.