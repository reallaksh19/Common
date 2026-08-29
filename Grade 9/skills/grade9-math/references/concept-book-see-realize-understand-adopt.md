# Grade 9 Mathematics Concept Book Protocol

## Purpose

Use this protocol when a Mathematics concept/reference book must teach *how to see and own the structure*, not merely list definitions and formulas.

Required macro cognitive sequence:

`SEE -> REALIZE -> UNDERSTAND -> ADOPT`

`CONNECT` is source traceability/navigation, not a fifth cognitive stage.

For difficult concepts, assume the learner may already have partial knowledge. Read `partial-knowledge-assimilation-concept-map.md` before authoring.

Operational teaching loop for a roughly 50%-prepared student:

`RECONNECT -> DISCOVER -> MAKE SENSE -> TRY -> DIAGNOSE -> FADE -> ADOPT -> TRANSFER`

This loop sits *inside* the four-stage macro sequence; it does not replace it.

## Mandatory concept map before prose

Before writing the chapter, map:

- prior-knowledge nodes;
- missing bridge nodes;
- core invariants;
- representation nodes;
- decision boundaries;
- misconception nodes;
- first-move nodes;
- transfer nodes;
- source-custody nodes where relevant.

Every major concept must contain a valid path:

`PRIOR -> BRIDGE -> INVARIANT -> FIRST MOVE -> TRANSFER`

and a competing-method path:

`VISIBLE CLUE -> TEMPTING WRONG MODEL -> CONTRAST -> CORRECT DECISION`.

## SEE / RECONNECT / DISCOVER

The learner first encounters a visible mathematical object and retrieves something already familiar:

- number pattern;
- table;
- finite difference or ratio marks;
- diagram or construction;
- worked fragment;
- graph;
- repeated operation;
- contrasting pair;
- expansion before compression;
- a basic case the learner can already solve.

Do not introduce an important formula as an unexplained starting point.

For partial-knowledge learners, do not spend pages reteaching what a quick diagnostic shows they already own. Use familiar material to expose the missing connection.

## REALIZE

The learner identifies what remains structurally unchanged or what transformation makes the problem simpler.

Typical invariants/structures include:

- constant difference;
- constant ratio;
- recurrence;
- symmetry;
- accumulation;
- reciprocal structure;
- cancellation;
- parity / odd-even split;
- factorization;
- common subexpression;
- equal spacing or equal scaling;
- coefficient/root relationships;
- boundary/equality conditions.

The learner should be able to state the hidden structure in ordinary language before calculation.

## UNDERSTAND / MAKE SENSE

The learner can rebuild the mathematics and explain why the compact result has its form. As applicable include:

- derivation or reconstruction;
- origin of every factor, exponent and sign;
- relation among equivalent representations;
- boundary/special cases;
- condition checks;
- dimensional or unit checks where mathematics is applied;
- proportional/scaling consequences;
- contrast with a plausible wrong method;
- explanation of why a transformation preserves the problem;
- reverse reconstruction if the formula is forgotten.

A worked example is not enough. Include commentary on what an experienced solver noticed *before* calculation.

## TRY -> DIAGNOSE

After the relationship is made sensible, require an attempt before giving the method.

Prefer prompts such as:

- “write only the first useful line”;
- “which representation would you choose?”;
- “what clue matters?”;
- “which of these two methods would you reject, and why?”

Diagnose the failure as one of:

- recognition gap;
- representation gap;
- conceptual/reconstruction gap;
- first-move gap;
- algebra/calculation gap;
- condition/domain gap;
- transfer gap.

Do not respond to every error with more worked examples. Repair the actual gap.

## FADE

Hints must decrease as ownership increases.

- `H0 INDEPENDENT` — no hint.
- `H1 RECOGNITION` — point to the visible clue/question type.
- `H2 STRUCTURE` — name the invariant or representation to build.
- `H3 EXECUTION` — give the first algebraic relation only.

On repeated practice remove H3, then H2, then H1.

A student who still requires H2/H3 has not reached ADOPT.

## ADOPT

The learner can use the idea independently when the surface form changes.

Each major concept should include several of:

1. **RECOGNIZE** — identify the structure in a disguised example.
2. **FIRST MOVE** — write only the first useful mathematical line.
3. **WHY NOT?** — reject a tempting but structurally wrong method.
4. **TRANSFER** — solve a non-identical problem using the same structure.
5. **REBUILD** — reconstruct the result without looking at the formula.
6. **CONTRAST** — distinguish a near-neighbour that needs another method.

Adoption is achieved when the learner can choose the structure without being told the chapter label.

## Six-question assimilation test

For every major concept ask:

1. What did you notice?
2. Why does the method work?
3. What clue would make you think of it?
4. What similar-looking situation would require a different method?
5. Can you write the first two useful lines without help?
6. Can you solve a disguised version?

Do not label the concept mastered when only the worked-example procedure is repeatable.

## Mathematical lenses

For a chapter, choose a small set of recurring lenses rather than organize only by formula names. For Sequence & Series use:

- `POSITION` — what lives at term `n`?
- `CHANGE` — what repeats additively?
- `RATIO` — what repeats multiplicatively?
- `ACCUMULATION` — what happens when terms are added?
- `TRANSFORM` — can the appearance be changed into an easier structure?
- `REVERSE` — can one term be recovered from cumulative information?

Other chapters must define their own lenses while preserving the cognitive and assimilation contracts.

## Chalkboard choreography

For each major idea prefer:

1. retrieve one familiar case;
2. show 2-4 concrete/contrasting cases;
3. mark what changes and what stays unchanged;
4. name the invariant/structure;
5. build the symbolic relation incrementally;
6. compress to the standard form;
7. switch to another representation;
8. contrast with a near-miss example;
9. ask for the first move on a disguised problem;
10. diagnose the response;
11. provide only the minimum hint level needed;
12. fade the hint on the next item;
13. require reconstruction or transfer;
14. connect to source question IDs.

## Contrast teaching

Use close contrasts because Mathematics difficulty often comes from choosing the right structure.

For Sequence & Series, examples include:

- sequence vs series;
- `a_n` vs `S_n`;
- AP vs GP;
- AP vs HP after reciprocation;
- finite vs infinite GP;
- direct sum vs nested sum;
- routine power sum vs telescoping transformation;
- same numbers with different conditions.

For other topics define equally specific competing-method contrasts. A contrast must teach the *decision boundary*, not just list a wrong answer.

## Summation teaching contract

Teach sigma notation as compressed repeated addition, not as a new formula family.

Required order:

`long addition -> counter/index -> start/stop -> expand -> compress -> split -> standard sums -> hidden transformations`

For example, establish

`1 + 2 + 3 + 4 + 5`

before

`sum_{k=1}^5 k`.

Then establish linearity by expanding real terms before using

`sum(2k^2 + 3k + 1) = 2 sum k^2 + 3 sum k + sum 1`.

## Product architecture

### Assimilation Book

This is the primary teaching layer for difficult concepts.

Use:

`RECONNECT -> DISCOVER -> MAKE SENSE -> TRY -> DIAGNOSE -> FADE -> ADOPT -> TRANSFER`

It should repair the learner's mental model, not merely deliver notes.

### First-Step Reference

This is a compression/revision layer after understanding.

Use:

`SEE -> REALIZE -> WRITE -> CHOOSE -> CHECK`

Include recognition atlas, phrase/structure decoder, decision tree, first-step cards, traps, recognition-only drills, and source-to-mechanism map.

**The First-Step Reference must not be the sole teaching layer for a difficult concept.**

### Mixed assessment

Use unlabelled mixed problems to prove independent method selection. Do not reveal chapter/method tags on the student paper.

## Mandatory MSRU gates

- **MSRU-01 No Naked Formula** — no major formula appears first in isolation.
- **MSRU-02 See Before Name** — show the mathematical behavior before naming the family where practical.
- **MSRU-03 Invariant Explicit** — state what is structurally unchanged.
- **MSRU-04 Explain Form** — explain factors, exponents, signs and index shifts such as `n-1`.
- **MSRU-05 Representation Translation** — move among at least two representations; three where practical.
- **MSRU-06 Contrast Pair** — include a close non-example or competing structure.
- **MSRU-07 First Move** — learner must choose a first line without full solution scaffolding.
- **MSRU-08 Reconstruction** — learner can rebuild the relation.
- **MSRU-09 Transfer** — finish with a non-identical problem.
- **MSRU-10 Source Traceability** — source questions map to concept sections.
- **MSRU-11 No Silent Repair** — preserve source defects/ambiguities explicitly.
- **MSRU-12 Grade 9 Depth** — accessible explanation must still include symbolic and structural reasoning.
- **MSRU-13 Summation Is Addition** — sigma notation must be grounded in ordinary addition first.
- **MSRU-14 Transform Before Calculate** — when a hard surface hides a simple structure, teach the transformation rather than brute force.
- **MSRU-15 Adopt Mastery** — concept is not complete until independent recognition/transfer is demonstrated.
- **MSRU-16 Partial-Knowledge Reconnect** — begin from what a partly prepared learner already owns; do not default to blank-slate exposition.
- **MSRU-17 Missing-Link Explicit** — identify the bridge that converts remembered fragments into a coherent model.
- **MSRU-18 Attempt Before Hint** — require H0 attempt before H1-H3 support.
- **MSRU-19 Diagnostic Repair** — classify the learner's failure mode and repair that gap rather than adding generic repetition.
- **MSRU-20 Hint Fading** — assistance must reduce across adjacent practice.
- **MSRU-21 Six-Question Assimilation** — mastery must cover notice, why, clue, contrast, first lines, and disguise.
- **MSRU-22 Reference Is Compression** — a First-Step Reference compresses assimilated understanding; it does not replace the Assimilation Book.

## Publication handoff

Preserve the macro stages visually, but design the page flow around the partial-knowledge learner. `ADOPT` must be a real learning zone, not a decorative practice box. Use stable concept/source IDs and retain full provenance in authoring metadata.
