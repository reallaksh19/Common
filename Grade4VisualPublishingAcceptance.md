# Grade 4 Visual Publishing Acceptance Contract

**Status:** Mandatory publishing acceptance profile for child-facing Grade 4 products  
**Applies to:** Mathematics and English student PDFs, workbooks, revision booklets, teacher/parent keys, and diagnostic companions  
**Parent schema:** `Grade4PublishingSchema.md`

---

## 1. Purpose

A technically correct PDF can still fail as a Grade 4 learning product.

This contract prevents outputs that read like research papers, teacher notes, or dense adult reference material when the intended reader is a 9–10 year old child.

The publishing target is:

```text
CORRECT CONTENT
    +
CHILD-APPROPRIATE VISUAL EXPERIENCE
    +
OBSERVABLE CHILD ACTION
    +
SEPARATE ADULT DIAGNOSTIC SUPPORT
```

A student product is not release-ready merely because the mathematics/English content is correct and the PDF has no layout errors.

---

## 2. Student-facing default: VISUAL_FIRST

Unless the source explicitly requires a text-heavy format, a Grade 4 student study guide or revision booklet must default to `VISUAL_FIRST`.

A `VISUAL_FIRST` page should normally contain:

- one dominant learning idea;
- at least one instructional visual, diagram, model, worked layout, organizer, or meaningful visual structure on concept/worked-example pages;
- short child-facing text chunks rather than long paragraphs;
- clear visual hierarchy and generous whitespace;
- one visible learner action such as notice, classify, complete, draw, choose, explain, or solve;
- large enough type and diagrams for normal A4 print reading;
- response space proportional to the expected work.

Visuals must carry instructional meaning. Decorative imagery may support engagement but cannot replace the instructional model.

### Fail examples

A student-facing page fails if it is dominated by:

- multiple long prose paragraphs;
- teacher terminology or research-style explanation;
- dense bullet lists with no model/example;
- diagnostic codes, architecture language, or adult metadata;
- tiny diagrams used only to decorate large text blocks;
- more explanation than learner action across several consecutive pages.

---

## 3. Child-language contract

Student-facing explanation should answer concrete questions such as:

```text
What is happening?
What should I notice?
What can I do next?
How can I check?
```

Prefer functional cues over adult abstractions.

Examples:

```text
"Large tells how big something is."
```

instead of:

```text
"Large is classified under the semantic adjective category of size."
```

And:

```text
"If 12 does not fit into the 6, write 0 in that quotient place."
```

instead of a paragraph about procedural place-value failure.

---

## 4. Student / adult edition separation

Do not combine a child study guide and a full diagnostic manual into one undifferentiated product.

Preferred split:

```text
STUDENT PRODUCT
  concept visuals
  worked examples
  short cues
  practice
  reasoning
  self-check

TEACHER / PARENT PRODUCT
  what to watch for
  likely error patterns
  diagnostic probes
  H1–H3 hint ladder
  repair suggestions
  independent retry
  support-fading / stop rule
```

A combined document is allowed only when edition boundaries are visually explicit and student pages do not expose adult diagnostic language.

---

## 5. H1–H3 quick-hint publishing profile

The canonical Grade 4 Math hint ladder may continue beyond H3 internally, but a quick Teacher / Parent Diagnostic Key should default to this visual projection:

```text
H1 NOTICE
  Point the child to the important feature without supplying the method.

H2 REMEMBER
  Trigger a fact, rule, relationship, place-value idea, or unit fact the child already knows.

H3 REPRESENT
  Change the representation: draw groups, use a bar model, place-value chart, number line, unit chain, multiples strip, or other relevant model.
```

### Hint rule

```text
START H1
  ↓ if insufficient
H2
  ↓ if insufficient
H3
  ↓
NEW INDEPENDENT RETRY
```

If H1 works, stop. Do not automatically show H2/H3.

If H3 works, remove or reduce the representation on the next independent retry where appropriate.

Hints are for restarting thinking, not for progressively revealing the answer.

---

## 6. Visual Teacher / Parent diagnostic card pattern

For each high-value misconception/error pattern, prefer one visual card/page containing:

```text
WHAT YOU MAY SEE
      ↓
VISUAL STRUCTURE / EXAMPLE
      ↓
H1 NOTICE
      ↓
H2 REMEMBER
      ↓
H3 REPRESENT
      ↓
INDEPENDENT RETRY
      ↓
STOP / FADE RULE
```

Teacher diagnosis must remain bounded language such as `possible pattern`, `likely mechanism`, or `probe next`; do not turn one response into a durable learner label.

---

## 7. Grade 4 Math visual expectations

On concept pages, prefer representations appropriate to the learning object, including:

```text
COUNTERS
EQUAL_GROUPS
ARRAY
BAR_MODEL
NUMBER_LINE
PLACE_VALUE_MODEL
FACT_FAMILY
MULTIPLES_STRIP
WRITTEN_ALGORITHM
UNIT_CHAIN
REMAINDER_CONTEXT_MODEL
ERROR_COMPARISON
```

Worked procedures should be visually staged. Do not explain multi-step arithmetic mainly through prose.

### Division-specific examples

A good Division product should visually support, where relevant:

- equal sharing vs equal grouping;
- multiplication–division fact families;
- estimation before exact division;
- multiples strips for 2-digit divisors;
- long-division place-value alignment;
- zero in the quotient;
- quantity/unit chains such as dozen → items → money;
- remainder interpretation in context;
- mistake-detective comparison.

---

## 8. Grade 4 English visual expectations

Visual-first does not mean replacing reading with pictures.

Use visual structure to reduce unnecessary load and expose language patterns, for example:

```text
story sequence
character-evidence map
main-idea/detail organizer
compare/contrast map
grammar pattern strip
sentence parts / editing marks
word-family / morphology map
writing planner
text-evidence highlighting
```

Literature pages must preserve the text as primary evidence. Visual organizers support interpretation; they do not replace the passage.

---

## 9. Page-density acceptance

There is no universal fixed visual percentage, but student pages must pass an editorial test:

> At a glance, does this look like material designed for a Grade 4 child to learn from, or like adult notes placed into a PDF?

Default checks for student concept/worked-example pages:

- no single prose block should dominate most of the page;
- prefer several short chunks to one long explanation;
- avoid consecutive text-only concept pages when a meaningful representation is available;
- maintain visible whitespace between learning chunks;
- use callouts sparingly and consistently;
- do not shrink text/diagrams simply to fit more content;
- split the learning experience across pages when needed.

If the only way to fit the page is to reduce child readability, revise the page plan instead.

---

## 10. Required learner action

A study guide should not become a sequence of explanations.

Across concept instruction, regularly include an observable child action:

```text
NOTICE
POINT
CIRCLE
MATCH
COMPLETE
DRAW
CHOOSE
EXPLAIN
SOLVE
CHECK
CREATE
```

A worked example may be followed by a tiny `Try it` rather than another paragraph.

---

## 11. Golden regression: Grade 4 Division

The following output shape is a publishing regression target because it exercises common Primary failures.

### Student guide

Must include visually distinct treatment of:

```text
1. sharing vs grouping
2. fact family / multiplication connection
3. estimation and multiples strip
4. long-division routine
5. 2-digit divisors
6. zero in the quotient
7. word-problem structure
8. units / dozen / rate chain
9. remainder meaning
10. practice
11. error detective
12. reasoning / challenge
```

The student guide must not contain full diagnostic codes or teacher analysis.

### Teacher / Parent key

Must visually include H1–H3 for at least these patterns:

```text
wrong operation choice
missing zero in quotient
unit/dozen conversion chain
2-digit divisor / multiples support
remainder interpretation
```

Each should end with an independent retry and a stop/fade rule.

---

## 12. Visual QA procedure

For every final Grade 4 PDF:

```text
RENDER PDF
  ↓
RENDER EVERY PAGE TO IMAGE
  ↓
INSPECT AS A CHILD-FACING SPREAD
  ↓
ASK:
  Is there enough visual structure?
  Are diagrams readable?
  Is text chunked?
  Is the page inviting rather than dense?
  Is the learner asked to do something?
  Are adult diagnostics hidden from student pages?
  ↓
FIX PAGE PLAN / COMPONENTS
  ↓
RE-RENDER
```

Do not approve from source code or text extraction alone.

---

## 13. Additional publishing quality gates

The following gates extend `Grade4PublishingSchema.md`:

```text
P-QG13 CHILD_FACING_VISUAL_FIRST
P-QG14 CHILD_LANGUAGE_AND_DENSITY_PASS
P-QG15 STUDENT_ADULT_EDITION_SEPARATION
P-QG16 INSTRUCTIONAL_VISUAL_COVERAGE
P-QG17 LEARNER_ACTION_DENSITY
P-QG18 HINT_LADDER_RENDER_VALID
P-QG19 INDEPENDENT_RETRY_VISIBLE
P-QG20 PAGE_IMAGE_CHILD_USABILITY_PASS
```

For a student-facing Grade 4 study guide, failure of `P-QG13`, `P-QG14`, `P-QG16`, `P-QG17`, or `P-QG20` blocks release.

For a Teacher / Parent diagnostic key that exposes hints, failure of `P-QG18` or `P-QG19` blocks release.

---

## 14. Cold-start agent acceptance checklist

Before delivering a Grade 4 PDF, the producing agent must be able to answer YES to all applicable questions:

```text
[ ] Is the intended reader explicit: child, teacher/parent, workbook user, or assessor?
[ ] Does the child edition look visually designed for a 9–10 year old?
[ ] Is each major new concept shown with a meaningful model/visual when one exists?
[ ] Is prose chunked and child-facing rather than research-style?
[ ] Are adult diagnostics separated from student content?
[ ] Does the product contain observable learner actions, not only explanations?
[ ] If a Teacher/Parent key uses hints, are H1 NOTICE, H2 REMEMBER, H3 REPRESENT shown progressively?
[ ] Does each repair sequence include a fresh independent retry?
[ ] Are page images inspected, not just the PDF text/source?
[ ] Would an average child be able to use the page without repeatedly asking an adult what the page means?
```

If the last answer is NO, the product is not finished.
