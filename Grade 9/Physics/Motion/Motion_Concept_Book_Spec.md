# Motion Concept Book Specification

## 1. Mission

Create a Grade 9 / competitive-foundation Physics concept book for Motion in a Straight Line that is grounded to the supplied 68-question source bank and explicitly solves the learner problem:

> I can continue once I see the first step, but I often do not know what the equation means or why it applies.

The Concept Book must teach *why the relationships work*. Equation selection is handled by the linked First-Step Reference Book.

## 2. Core pedagogy

The mandatory learning sequence is:

`SEE THE EQUATION -> REALIZE -> UNDERSTAND`

Use `CONNECT` only for traceability/navigation.

### SEE

Show the physical relationship through a chalkboard-friendly representation before or together with the symbolic form:

- number line;
- path/arrow;
- time boxes;
- velocity table;
- graph;
- rectangle/triangle area;
- dropped/thrown chalk thought experiment;
- two-body diagram;
- before/after comparison.

### REALIZE

Require the learner to verbalize the relationship and explain every term physically.

### UNDERSTAND

As applicable require:

- derivation or reconstruction;
- assumptions/model validity;
- coordinate/sign convention;
- units/dimensions;
- limiting/special cases;
- graph equivalence;
- proportional/scaling reasoning;
- misconception contrast;
- prediction before calculation;
- transfer to a source-style unfamiliar problem.

## 3. Target depth

Explanations may be simple; reasoning must not stop at elementary intuition.

The finished book must include Grade 9-level reasoning such as:

- signed displacement and velocity;
- algebraic rearrangement and elimination;
- derivation of kinematic equations;
- interval versus cumulative motion;
- quadratic dependence and first differences;
- stopping-distance `u^2` scaling;
- square-root fall-time scaling;
- vertical-motion sign convention;
- same-height symmetry;
- relative-motion cancellation of common acceleration;
- words <-> graphs <-> equations translation;
- slope and area interpretation;
- physical possibility of time graphs.

## 4. Source coverage authority

The book must cover all source concepts represented by:

- Q1-Q5 — Distance and Displacement
- Q6-Q10 — Speed and Velocity
- Q11-Q34 — Acceleration and Equations of Motion
- Q35-Q62 — Motion Under Gravity
- Q63-Q68 — Graphs

See `Motion_Source_Coverage_Map.md` for the Q1-Q68 mapping.

## 5. Concept architecture

### CB0 — The Language of Motion

Enabling concepts added for understanding:

- reference point;
- one-dimensional coordinate axis;
- initial/final position;
- positive direction;
- signed quantities;
- SI units;
- motion timelines;
- how to read a word problem without calculating.

These are enabling concepts, not claimed as standalone topics directly present in the source.

### CB1 — Position, Distance and Displacement

Cover:

- path length versus change in position;
- `Delta x = x_f - x_i`;
- sign as direction;
- closed-path motion;
- distance >= magnitude of displacement;
- polygon and circular-path examples.

Source: Q1-Q5.

### CB2 — Speed, Velocity and Average Motion

Cover:

- speed as path rate;
- velocity as displacement rate;
- average speed versus average velocity;
- equal-time average;
- equal-distance average;
- why arithmetic mean can fail;
- cyclic forward/backward motion.

Source: Q6-Q10.

Mandatory contrast: Q8-type equal-time versus Q9-type equal-distance average.

### CB3 — What Acceleration Really Means

Cover:

- acceleration as rate of velocity change;
- `a = (v-u)/t`;
- speeding up versus slowing down;
- negative acceleration versus negative velocity;
- velocity change caused by direction change;
- constant acceleration as a modelling assumption.

Source emphasis: Q11-Q14, Q28-Q31.

### CB4 — Velocity Under Constant Acceleration

Core relation:

`v = u + at`

SEE:

velocity table / equal velocity increments each second.

REALIZE:

final velocity = starting velocity + accumulated velocity change.

UNDERSTAND:

- derive from acceleration definition;
- units;
- `a=0` limiting case;
- straight-line `v-t` graph;
- stopping-time applications;
- sign convention.

### CB5 — Displacement Under Constant Acceleration

Core relations:

`s = ut + 1/2 at^2`

`s = ((u+v)/2)t`

Teach from `v-t` area and average velocity.

Mandatory explanations:

- why `ut` is present;
- why acceleration creates an extra term;
- why `1/2` appears;
- why `t^2` appears;
- why units reduce to displacement;
- `a=0` gives `s=ut`.

Source emphasis: Q13, Q16-Q17, Q20, Q23-Q27, Q32-Q34.

### CB6 — Motion Without Time

Core relation:

`v^2 = u^2 + 2as`

Teach by eliminating time from earlier relations.

Mandatory explanations:

- time is absent because it was algebraically eliminated;
- squared velocities arise from `(v+u)(v-u)`;
- direct velocity-displacement connection;
- stopping-distance scaling;
- vertical maximum-height use.

Source emphasis: Q15, Q18, Q21, Q25 and later gravity applications.

### CB7 — Special Patterns Hidden in the Equations

Cover:

- `starts from rest -> u=0`;
- `comes to rest -> v=0`;
- stopping distance `s_stop proportional to u^2`;
- interval motion;
- nth-second derivation from `S(n)-S(n-1)`;
- `1:3:5:7:...` successive distances from rest;
- equal-distance constant-resistance problems and equal changes in `v^2`.

Source emphasis: Q13, Q15-Q18, Q20-Q21, Q27, Q32, Q34, Q59.

### CB8 — Delayed Start and Multi-stage Motion

Cover:

- common timeline;
- delayed release/start;
- multiple stages;
- stopping each body separately before comparing separation;
- interpreting "4 s before" or similar temporal language.

Source emphasis: Q19, Q22, Q25, Q33.

### CB9 — Gravity Is Acceleration

Core idea:

The kinematic framework is unchanged; use `a = +/- g` according to the chosen positive direction.

Cover:

- free fall from rest;
- `v=gt` and `s=1/2 gt^2` as special cases;
- height from time;
- interval/last-distance problems;
- mass independence within the idealized school model;
- `t proportional to sqrt(h)`.

Source: Q35, Q40-Q44, Q53, Q56, Q59-Q60.

### CB10 — Vertical Projection

Cover:

- upward-positive sign convention;
- gravity remains downward throughout;
- highest point: `v=0` but `a=-g`;
- time to top;
- `H = u^2/(2g)`;
- total flight time when launch/landing levels coincide;
- same-height symmetry;
- Earth/Moon scaling;
- `H proportional to u^2`;
- height-fraction/speed-fraction reasoning;
- bridge/tower problems with signed displacement.

Source: Q36-Q38, Q45-Q50, Q54-Q58, Q61.

### CB11 — Two Bodies, Release and Relative Motion

Cover:

- separate variable sets for each body;
- common gravitational acceleration;
- relative acceleration cancellation when both bodies share `g`;
- released body inherits the carrier's instantaneous ground velocity;
- upward/downward launch comparisons from the same height.

Source: Q39, Q41, Q46-Q47, Q51-Q54, Q62.

### CB12 — Motion as a Graph

Cover:

- slope of `x-t` = velocity;
- slope of `v-t` = acceleration;
- signed area under `v-t` = displacement;
- constant acceleration -> linear `v-t`;
- constant acceleration -> quadratic `x-t`;
- velocity-displacement relation;
- graph single-valuedness/physical possibility;
- words <-> graph <-> equation translation.

Source: Q63-Q68.

## 6. Standard concept spread

Every major concept should use a repeatable board sequence.

### BOARD 1 — SEE

Physical situation/pattern/graph.

### BOARD 2 — REALIZE

Highlight the physical meaning of every term and state the equation in words.

### BOARD 3 — UNDERSTAND: BUILD

Derive or reconstruct.

### BOARD 4 — UNDERSTAND: CHECK

Use units, sign, limiting case, graph, model validity, or physical magnitude.

### BOARD 5 — WRONG IDEA

Confront one real misconception.

### BOARD 6 — PREDICT

Require a qualitative/scaling prediction before arithmetic.

### BOARD 7 — RECONSTRUCT / TRANSFER

Hide the formula or change the surface context.

### BOARD 8 — CONNECT

Map to source question IDs and companion products.

## 7. Required equation passports

At minimum create complete passports for:

1. `Delta x = x_f - x_i`
2. `average speed = total distance / total time`
3. `average velocity = displacement / time`
4. `a = (v-u)/t`
5. `v = u + at`
6. `s = ut + 1/2 at^2`
7. `s = ((u+v)/2)t`
8. `v^2 = u^2 + 2as`
9. `s_n = S(n)-S(n-1)` and the nth-second shortcut after derivation
10. gravity specializations with `a=+/-g`
11. `H = u^2/(2g)`
12. same-level total flight time `T=2u/g`
13. `slope(x-t)=v`
14. `slope(v-t)=a`
15. `area(v-t)=displacement`

## 8. First-step linkage

The Concept Book must not become a formula-selection manual, but each CONNECT box should link to the First-Step Book.

The First-Step method is:

`SEE THE STORY -> WRITE -> CHOOSE`

where WRITE captures knowns, hidden facts, sign convention, and target.

## 9. Question-bank linkage

Question Bank method:

`RECOGNIZE -> SOLVE -> CHECK -> TRANSFER`

Mixed mastery must progressively remove topic headings so the learner must classify the motion structure independently.

## 10. JEE/competitive-foundation appendix policy

If a future appendix uses real JEE previous-year questions:

- verify exam identity and year/session from an authoritative or traceable archive;
- do not invent year/shift metadata;
- link each item back to Concept Book section IDs;
- provide graduated reasoning hints rather than revealing the equation immediately;
- keep answers/solutions at the back if that is the requested publication style;
- separate source wording from any adapted/paraphrased publication wording.

## 11. Source QA flags

Preserve these until independently reverified:

- **Q29** — expected solution appears to require constant/uniform acceleration, not clearly visible in the stem.
- **Q49** — Earth/Moon gravity ratio is needed for a self-contained numerical/comparative answer.
- **Q52** — scan visibility obscures part of the stem; exact reproduction requires verification.
- **Q65** — curve naming depends on axis assignment; teach the invariant relation first.
- Printed page order around Q41-Q68 is not reliable; use question number.

## 12. Typography / PDF requirements

Because mathematical glyph failures were observed in an earlier draft, final PDF production must:

- use a math-capable font stack;
- verify superscripts/subscripts;
- verify Greek symbols such as Delta where used;
- verify arrows, radicals, multiplication signs, minus signs, and inequality signs;
- embed fonts where permitted;
- prevent clipping at equation baselines and page edges;
- keep body text and equations consistent in weight/scale;
- visually inspect representative pages after rendering;
- reject missing-glyph squares/tofu or fallback-font mismatches.

## 13. Definition of done

The Motion Concept Book is complete only when:

1. all Q1-Q68 have valid concept destinations;
2. all major equations have complete passports;
3. every major lesson passes SRU-01 to SRU-15;
4. the learner can recognize, verbalize, reconstruct, predict, and transfer;
5. source ambiguities remain explicitly recorded;
6. typography/rendering QA passes;
7. companion First-Step and Question Bank links are defined.
