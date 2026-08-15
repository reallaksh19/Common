# Grade 9 Physics Concept Book Protocol

## Purpose

Use this protocol when a Physics reference/concept book must teach *why the physics works*, not merely list definitions and formulas.

The required cognitive sequence is:

`SEE THE EQUATION -> REALIZE -> UNDERSTAND -> CONNECT`

`CONNECT` is the traceability and navigation layer. The learning objective itself remains SEE -> REALIZE -> UNDERSTAND.

## 1. Definitions of the three stages

### SEE THE EQUATION

The learner encounters the mathematical relationship inside something observable or drawable:

- a chalkboard sketch;
- a motion timeline;
- a number pattern;
- a graph;
- an area model;
- a physical demonstration;
- a thought experiment;
- a before/after comparison;
- two-body or multi-stage diagrams.

The equation may appear at this stage, but it must not appear as an unexplained formula to memorize.

### REALIZE

The learner can explain what every term means physically and can say the relationship in ordinary language.

Example:

`v = u + at`

means:

`final velocity = initial velocity + velocity accumulated because acceleration acts for time t`.

A successful REALIZE stage should produce an "of course" response: the symbolic relation now matches the physical story.

### UNDERSTAND

The learner can justify or reconstruct the relationship and knows its limits. As applicable, include:

- derivation;
- assumptions;
- model-validity conditions;
- coordinate/frame/sign convention;
- dimensional check;
- limiting/special cases;
- graph interpretation;
- proportional/scaling consequences;
- contrast with a plausible wrong idea;
- prediction before calculation;
- reconstruction if the formula is forgotten;
- transfer to a differently worded source question.

### CONNECT

Connect the concept to:

- original/source question IDs;
- prerequisite concept IDs;
- first-step/problem-recognition material;
- question-bank items;
- challenge/JEE items where applicable.

CONNECT must not replace explanation with links.

## 2. Chalkboard choreography

Prefer this board sequence for each major idea:

1. **SEE** — show a physical situation, pattern, graph, table, or sketch.
2. **NOTICE** — ask what changes and what stays constant.
3. **SAY** — express the relationship in words.
4. **BUILD** — construct the mathematics incrementally.
5. **COMPRESS** — arrive at the compact equation.
6. **CHECK** — units, sign, special case, graph, or limiting behavior.
7. **PREDICT** — change one variable and predict the effect before calculation.
8. **RECONSTRUCT** — rebuild the relation from the physical picture or earlier law.
9. **CONNECT** — identify which source problems the idea unlocks.

Do not front-load formal derivations before the physical relationship is visible.

## 3. Equation Passport

Every major equation must have a complete passport.

Record:

- `equation_id`
- equation/relation;
- physical system;
- **SEE** representation;
- plain-language meaning;
- meaning of every symbol;
- origin of every term/factor;
- derivation/reconstruction route;
- assumptions and validity;
- units/dimensions;
- graph equivalent where relevant;
- limiting/special cases;
- proportional/scaling consequences;
- common misconception;
- prediction question;
- reconstruction question;
- source question IDs;
- linked first-step/question-bank items.

## 4. Grade 9 depth gate

Conceptual simplicity is desirable; intellectual shallowness is not.

A Grade 9 concept lesson must, where the concept permits, move beyond an elementary story into at least several of the following:

- symbolic derivation;
- algebraic elimination;
- model/assumption selection;
- signed quantities and coordinate choice;
- proportional and inverse-proportional reasoning;
- quadratic or square-root scaling;
- graph/equation/word translation;
- interval versus cumulative quantity;
- multi-stage or two-body reasoning;
- dimensional reasoning;
- limiting-case reasoning;
- reconstruction from first principles;
- transfer to a non-identical problem.

Do not mistake a child-friendly explanation for a Grade 5 learning target. The explanation should be accessible; the reasoning target must remain Grade 9 / competitive-foundation where the source demands it.

## 5. SEE -> REALIZE -> UNDERSTAND acceptance tests

### SEE test

Can the learner point to the physical meaning of the equation in the drawing, graph, pattern, or experiment?

### REALIZE test

Can the learner explain the relation without symbols?

Can the learner explain why each term has the sign, power, coefficient, or operation that it does?

### UNDERSTAND test

Can the learner:

1. reconstruct or justify the relationship if the formula is hidden;
2. state when the model is valid;
3. predict how the result changes when one variable changes;
4. detect at least one physically impossible or dimensionally inconsistent alternative;
5. recognize the same concept in a differently worded source question?

If not, the lesson is incomplete.

## 6. Mandatory SRU authoring gates

### SRU-01 — No Naked Equation

No important equation may first appear as an isolated formula box.

### SRU-02 — Every Symbol Speaks

Symbols require physical meanings, not merely dictionary labels.

### SRU-03 — Every Term Has an Origin

Explain each additive term, factor, exponent, and sign.

### SRU-04 — Explain Unusual Mathematics

Explicitly explain features such as `1/2`, `t^2`, `v^2`, negative signs, square roots, and nth-interval differences.

### SRU-05 — Verbalize Before Calculating

The student should state the physical meaning before substitution.

### SRU-06 — Prediction Required

At least one prediction question is required per major concept.

### SRU-07 — Misconception Confrontation

Use a real misconception, not generic "be careful" advice.

### SRU-08 — Reconstruction Test

A concept is not complete unless the learner can rebuild the relation from an earlier principle, graph, pattern, or physical picture.

### SRU-09 — Source Traceability

Every source question must map to one or more concept sections.

### SRU-10 — Do Not Silently Repair Source Defects

Missing assumptions, ambiguous stems, poor notation, or ordering defects must be recorded as source-QA issues.

### SRU-11 — Symbolic Depth

At least one symbolic reasoning or derivation step is required for major quantitative relations.

### SRU-12 — Assumptions / Validity

State the model conditions: e.g. constant acceleration, negligible air resistance, chosen reference frame.

### SRU-13 — Representation Translation

Require translation among at least two of words, diagram, graph, table, and equation; use three where practical.

### SRU-14 — Scaling Reasoning

When an equation contains powers or inverse dependence, make the scaling consequence explicit.

### SRU-15 — Transfer

End major concepts with a source-style or unfamiliar-context transfer prompt that cannot be answered by copying the worked example.

## 7. Contrast teaching

Use paired examples deliberately.

Examples:

- equal times versus equal distances in average speed;
- stopping time versus stopping distance;
- total distance in 5 s versus distance during the 5th second;
- same speed versus same velocity;
- `v = 0` versus `a = 0`;
- dropped from rest versus released from a moving carrier;
- valid but inefficient equation versus most direct equation.

Contrast is preferred when two similar-looking problems require different modelling choices.

## 8. Source-grounding workflow

Before authoring:

1. enumerate every source question/item;
2. assign stable concept IDs;
3. identify the explicit concept and hidden recognition step;
4. identify the governing relation or qualitative law;
5. record source ambiguities/defects;
6. create a Source -> Concept coverage matrix;
7. confirm 100% source coverage before PDF production.

For each concept, keep bidirectional traceability:

`source question -> concept section`

and

`concept section -> source questions`.

## 9. Relationship to other Grade 9 products

### Concept Book

`SEE -> REALIZE -> UNDERSTAND`

Answers: **Why does this work?**

### First-Step Reference Book

`SEE THE STORY -> WRITE WHAT IS KNOWN -> CHOOSE`

Answers: **How do I start?**

### Question Bank

`RECOGNIZE -> SOLVE -> CHECK -> TRANSFER`

Answers: **Can I do it independently?**

These are linked products, not interchangeable layouts.

## 10. Physics publication handoff

When producing PDF/print output:

- preserve board/diagram/equation sequencing;
- do not compress SEE, REALIZE and UNDERSTAND into one dense formula page;
- use a math-capable font stack with complete Unicode glyph coverage;
- embed fonts where licensing permits;
- check superscripts, subscripts, arrows, Greek letters, minus signs, multiplication symbols, radicals, and equation alignment;
- reject missing-glyph boxes or fallback-font mismatches;
- keep equations readable at normal A4 print size;
- avoid excessive whitespace that breaks the chalkboard narrative;
- use diagrams for reasoning, not decorative imagery;
- retain concept IDs and source IDs in authoring metadata.

## 11. Definition of done

A concept lesson is complete only when the learner can:

1. **recognize** the physical situation behind the equation;
2. **explain** every term in ordinary language;
3. **justify/reconstruct** the relation;
4. **state assumptions** and sign conventions;
5. **predict** scaling or directional consequences;
6. **translate** among representations;
7. **reject** a common wrong model;
8. **transfer** the idea to a source-style unfamiliar question.
