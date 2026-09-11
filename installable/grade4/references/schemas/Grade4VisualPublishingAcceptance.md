# Grade 4 Visual Publishing Acceptance Contract

**Status:** Mandatory publishing acceptance profile for child-facing Grade 4 products

A technically correct PDF can still fail as a Grade 4 learning product. This contract prevents outputs that read like research papers, teacher notes, or dense adult reference material when the intended reader is a 9–10 year old child.

## VISUAL_FIRST student default

Unless the source explicitly requires a text-heavy format, Grade 4 study guides and revision products should default to `VISUAL_FIRST`.

A concept/worked-example page should normally contain:

- one dominant learning idea;
- at least one meaningful instructional visual/model/organizer when one exists;
- short child-facing text chunks;
- clear hierarchy and generous whitespace;
- one visible learner action: notice, point, match, draw, choose, complete, explain, solve, or check;
- readable type/diagrams at normal A4 print size;
- adequate response space.

Fail student pages that are dominated by long prose, research-style explanation, teacher terminology, diagnostic codes, dense bullets without models, tiny diagrams, or several consecutive explanation-only pages.

## Student / adult separation

Prefer separate products:

```text
STUDENT PRODUCT
  concept visuals
  worked examples
  short cues
  practice
  reasoning / transfer
  self-check

TEACHER / PARENT PRODUCT
  what to watch for
  possible error patterns
  diagnostic probes
  H1-H3 quick hints
  repair suggestion
  independent retry
  support-fading / stop rule
```

## H1-H3 quick-hint profile

For Teacher / Parent keys:

```text
H1 NOTICE
  Point to the important feature without supplying the method.

H2 REMEMBER
  Trigger a relevant fact, rule, relationship, place-value idea, or unit fact.

H3 REPRESENT
  Change/externalize representation: groups, bar model, place-value chart,
  number line, unit chain, multiples strip, organizer, etc.
```

Use progressively:

```text
H1 -> if insufficient H2 -> if insufficient H3 -> NEW INDEPENDENT RETRY
```

If H1 works, stop. If H3 works, fade the representation on the next retry where appropriate.

Hints restart thinking; they do not reveal the answer progressively.

## Visual diagnostic-card pattern

```text
WHAT YOU MAY SEE
      ↓
VISUAL EXAMPLE / STRUCTURE
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

## Grade 4 Math visual models

Use, as appropriate:

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

Worked procedures should be visually staged rather than explained mainly through prose.

## Division regression target

Student guide should visually cover relevant items from:

```text
sharing vs grouping
fact family / multiplication connection
estimation and multiples strip
long-division routine
2-digit divisors
zero in quotient
word-problem structure
units / dozen / rate chain
remainder meaning
practice
error detective
reasoning / challenge
```

Teacher / Parent key should include visual H1-H3 sequences for high-value patterns such as:

```text
wrong operation choice
missing zero in quotient
unit/dozen conversion chain
2-digit divisor / multiples support
remainder interpretation
```

Each repair sequence ends with a fresh independent retry and stop/fade rule.

## Grade 4 English visual structure

Visual-first does not replace reading. Use organizers to expose language/evidence, such as story sequence, character-evidence map, main-idea/detail map, compare/contrast map, grammar pattern strip, sentence model, word-family map, writing planner, or text-evidence highlighting.

## Page-image QA

Render every PDF page to an image and inspect as a child-facing spread. Ask:

- Is there enough visual structure?
- Are diagrams readable?
- Is text chunked?
- Is the page inviting rather than dense?
- Is the learner asked to do something?
- Are adult diagnostics hidden from student pages?
- Would an average Grade 4 learner understand how to use the page without repeatedly asking an adult what the page means?

If the last answer is NO, the product is not finished.

## Additional quality gates

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

Student guide release is blocked by failure of P-QG13, P-QG14, P-QG16, P-QG17, or P-QG20. Teacher/Parent hint-key release is blocked by failure of P-QG18 or P-QG19.
