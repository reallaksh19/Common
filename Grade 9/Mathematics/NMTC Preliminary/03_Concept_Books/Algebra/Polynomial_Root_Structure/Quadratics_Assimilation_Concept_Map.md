# Quadratics — Assimilation Concept Map

## Learner assumption

Target a student who can probably factor some quadratics, remembers the quadratic formula/discriminant vaguely, and has heard of Vieta, but does not reliably know **which representation or method to choose** when the question surface changes.

The book must repair connections, not restart from zero.

## Master map

```text
BASIC EQUATION VIEW
ax^2 + bx + c = 0
    |
    +--> FACTOR VIEW ------------------------------+
    |       | roots / zero product                 |
    |       | integer factor pairs                 |
    |       v                                      |
    |   INDIVIDUAL ROOTS                           |
    |                                              |
    +--> GRAPH / VERTEX VIEW ------------------+   |
    |       | intersections / tangency          |   |
    |       | minimum/maximum                  |   |
    |       v                                  |   |
    |   DISCRIMINANT <---- nature of roots     |   |
    |       |                                  |   |
    |       +--> D>0 two real                  |   |
    |       +--> D=0 repeated/tangent          |   |
    |       +--> D<0 no real                   |   |
    |                                          |   |
    +--> COEFFICIENT <-> ROOT INVARIANTS ------+---+
    |       S = alpha + beta = -b/a
    |       P = alpha beta = c/a
    |       |
    |       +--> symmetric expressions
    |       +--> reciprocal roots
    |       +--> shifted/squared roots
    |       +--> parameter restrictions
    |       +--> positive/integer root constraints
    |
    +--> QUADRATIC RELATION AS REWRITING RULE
            x^2 = px + q
            |
            +--> reduce x^3, x^4, ...
            +--> recurrence / cycle
            +--> transform before calculate
```

## Prior-knowledge nodes

A partly prepared student is likely to know some of:

- a quadratic has degree 2;
- factorization such as `x^2-5x+6=(x-2)(x-3)`;
- zero-product rule;
- quadratic formula;
- discriminant symbol `b^2-4ac`;
- sum/product of roots as a memorized rule;
- completing square in routine textbook examples.

Do not spend long sections restating these. Use them to reconnect and expose missing links.

## Missing bridge nodes

These are the key teaching targets.

### B1 — The requested quantity chooses the method

Same equation, different target -> different representation.

- “find the roots” -> factor/formula may be appropriate;
- “find alpha^2+beta^2” -> Vieta/invariants;
- “exactly one real root” -> discriminant;
- “minimum value” -> vertex/completing square;
- “x^20 under a quadratic relation” -> reduction, not solving roots.

### B2 — Discriminant is geometric/root-count information

`D` is not just a formula part. It classifies how the parabola meets the x-axis.

### B3 — Vieta stores relational information

Coefficients may answer a root-expression question without finding either root.

### B4 — A quadratic equation can be a rewriting machine

From `x^2=px+q`, every higher power can be reduced. The equation is not merely something to solve.

### B5 — Root restrictions are extra mathematical information

“real,” “positive,” “integer,” “equal,” and “distinct” are not adjectives; each creates equations/inequalities/case restrictions.

## Core invariant nodes

1. **Factor/zero invariant**
   `P(r)=0 <=> (x-r)` is a factor.

2. **Discriminant invariant**
   `D=b^2-4ac` controls the number/nature of real roots.

3. **Vieta invariants**
   `S=alpha+beta=-b/a`, `P=alpha beta=c/a`.

4. **Symmetric-expression reduction**
   Rewrite targets in `S` and `P` before solving roots.

5. **Quadratic reduction invariant**
   Modulo a quadratic relation, high powers collapse to degree at most 1.

6. **Transformation invariant**
   Shifted/reciprocal/squared roots can often be handled by transforming `S` and `P` rather than individual roots.

## Representation map

```text
STANDARD FORM ax^2+bx+c
   |-- coefficient comparison --> Vieta / discriminant / parameters
   |
   |-- factorization --> roots / integer structure / sign
   |
   |-- complete square --> vertex / minimum / maximum / graph
   |
   |-- graph --> intercept count / tangency / sign regions
   |
   |-- relation x^2=px+q --> power reduction / recurrence
```

A major teaching goal is to make representation switching deliberate.

## Decision boundaries / contrast pairs

### C1 — Find roots vs find a symmetric expression

Same quadratic:

- larger root -> individual-root method;
- `alpha^2+beta^2` -> Vieta.

**Repair rule:** ask whether the target changes when alpha and beta are swapped. If not, test `S,P` first.

### C2 — Equal roots vs minimum value

- “equal roots” -> `D=0`;
- “minimum value” -> complete square / vertex.

**Repair rule:** root-count language points to discriminant; value-of-expression language points to the graph/vertex representation.

### C3 — Positive roots vs positive integer roots

- positive real roots -> sign + discriminant constraints;
- positive integer roots -> additionally factor-pair/divisibility structure.

### C4 — Solve relation vs reduce powers

- target is root itself -> solve may be justified;
- target contains large powers -> first test reduction.

### C5 — Shifted roots vs shifted function input

- roots become `alpha+h, beta+h` -> transform `S,P`;
- equation involves `f(x+h)` -> variable substitution/shift the input carefully.

## Misconception nodes

### M1 — “Quadratic present -> quadratic formula”
Why attractive: the student remembers one universal-looking procedure.

Repair: identify the requested information first; solving roots may create information the problem never asked for.

### M2 — Vieta sign error
Why attractive: memorized formulas detach from factor expansion.

Repair: rebuild from `a(x-alpha)(x-beta)`.

### M3 — `D=0` memorized without meaning
Repair: connect repeated root <-> one x-intercept <-> tangency.

### M4 — Positive roots inferred from positive product alone
Repair: product gives same sign; sum decides whether both are positive or both negative, subject to reality.

### M5 — Equation treated as identity
A relation true for roots is not automatically true for every x.

### M6 — Source/key conflict forced into agreement
Repair: derive from the printed mathematics, then mark `SOURCE_CONFLICT` if the key disagrees.

## First-move atlas

| Visible clue | First move to test |
|---|---|
| factorable small integer coefficients | factor view |
| exactly one / repeated real root | set `D=0` |
| two distinct real roots | require `D>0` |
| no real roots | require `D<0` |
| `alpha^2+beta^2`, reciprocals, ratios | rewrite in `S,P` |
| roots shifted/squared/reciprocal | transform `S,P` |
| positive/integer roots | Vieta + sign/factor-pair constraints |
| large power under quadratic relation | reduce powers |
| minimum/maximum value | complete square / vertex |
| common root of two equations | eliminate at the shared root |
| printed result contradicts derivation | source-integrity check |

## Hint-fading examples

### Example: symmetric root expression

`H0` Solve independently.

`H1` Does the target change if alpha and beta are swapped?

`H2` Write `S=alpha+beta`, `P=alpha beta`.

`H3` Use `alpha^2+beta^2=S^2-2P`.

### Example: repeated root parameter

`H0` Attempt independently.

`H1` What does “repeated root” say about the graph/root count?

`H2` Use the discriminant condition.

`H3` Set `b^2-4ac=0` and solve the parameter equation.

## Assimilation path by module

### Module A — Representation choice
`known factorization -> same quadratic in standard/factor/graph/root form -> target chooses view -> mixed first-move drill`

### Module B — Discriminant
`known formula fragment -> root-count/tangency meaning -> parameter conditions -> contrast with vertex problems -> disguised transfer`

### Module C — Vieta
`known roots of easy factorable quadratic -> notice sum/product in coefficients -> derive -> symmetric targets -> contrast with individual-root questions -> transfer`

### Module D — Transformations and restrictions
`known S,P -> transform roots -> positivity/integrality adds constraints -> parameter feasibility -> source-QC cases`

### Module E — Power reduction
`known equation manipulation -> use quadratic as rewriting rule -> recurrence/cycle -> high-power problems -> contrast with explicit root solving`

## Transfer endpoints

The student should eventually handle, without chapter labels:

- an ugly quadratic with a simple symmetric root target;
- a parameter chosen for repeated roots;
- a shifted-root equation;
- a positive-integer-root feasibility problem;
- a high-power expression controlled by a quadratic relation;
- a mixed problem where completing square is better than discriminant;
- a source-conflicted item where mathematical consistency must be checked.

## Source grounding

Clean/qualified mechanism anchors currently include:

- `NMTC-BH-P-2018-Q06` — quadratic relation / power reduction;
- `NMTC-BH-P-2023-Q03` — low-degree relation / reciprocal-power structure;
- `NMTC-BH-P-2024-Q01` — `x^2=1-x` reduction/recurrence;
- `NMTC-BH-P-2024-Q14` — transformed-root Vieta;
- `NMTC-BH-P-2024-Q17` — positive roots / equality collapse;
- `NMTC-BH-P-2024-Q22` — shifted input/root structure.

Additional evidence:

- `NMTC-BH-P-2018-Q07` — bonus evidence for repeated-root discriminant;
- `NMTC-BH-P-2023-Q13` — bridge for discriminant/integer cases;
- `NMTC-BH-P-2025-Q20` — `SOURCE_CONFLICT` only, not canonical practice.

Do not reproduce full third-party statements in ordinary chapter text. Use IDs and mechanism descriptions, with original author-created teaching/practice problems.

## End-state student belief

> A quadratic is not one formula. It is a mathematical object with several views. I choose the view that makes the requested information smallest.
