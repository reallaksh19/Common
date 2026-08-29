# Quadratics — Transformed Roots, Integer Roots & Structural Reduction
## Subtopic Assimilation Concept Map — Issue #39

**Target learner:** Grade IX/X / NMTC Preliminary learner who can solve ordinary quadratics but only partly sees how root transformations, sign/integrality restrictions, and a quadratic relation can replace explicit root solving.

**Authoring rule:** this map is the pre-prose authority for Issue #39. The student module, practice, First-Step Reference, answer key and QA must trace back to these nodes.

---

# 1. Central belief

> A quadratic does more than give two roots. It stores root invariants, sign/discrete constraints, and a low-degree rewriting rule. Before solving roots, ask what information the target actually needs.

Three strands connect through one decision habit:

```text
KNOWN QUADRATIC / ROOT RELATION
        |
        +--> ROOT INVARIANTS S,P
        |       |
        |       +--> TRANSFORM ROOTS
        |       |       shift / reciprocal / square
        |       |       |
        |       |       +--> new sum + new product
        |       |               |
        |       |               +--> new quadratic
        |       |
        |       +--> ROOT RESTRICTIONS
        |               real / sign / positive / integer
        |               |
        |               +--> inequalities + factor pairs
        |               +--> parity / divisibility
        |               +--> equality collapse
        |
        +--> QUADRATIC RELATION AS REWRITING RULE
                x^2 = px + q
                |
                +--> reduce every higher power
                +--> recurrence / cycle
                +--> reciprocal-power recurrence

FIRST DECISION AT EVERY BRANCH:
"Do I need the individual roots at all?"
```

---

# 2. Node map required by the assimilation skill

## A. PRIOR_KNOWLEDGE

The learner probably already knows some of:

- factorization and the zero-product rule;
- quadratic formula for explicit roots;
- Vieta in the form `S = alpha + beta`, `P = alpha beta`;
- a monic quadratic with roots `u,v` can be written from their sum and product;
- basic integer factor pairs;
- simple AM-GM for positive numbers;
- substitution into an equation.

## B. LIKELY_HALF_KNOWLEDGE

Typical partial understanding:

- can find `alpha,beta` and then transform them, but does not see that transformed `S',P'` are enough;
- hears “positive roots” and checks only `P>0`;
- hears “integer roots” but treats it like a continuous real-root condition;
- sees a high power and reaches for the quadratic formula instead of reducing powers;
- confuses “roots become `alpha+h,beta+h`” with “the equation contains `f(x+h)`”;
- treats a supplied source key as more authoritative than the printed mathematics when they conflict.

## C. MISSING_BRIDGE

1. **Transformation bridge:** root transformations can be performed on the invariants rather than on individual roots.
2. **Restriction bridge:** adjectives such as real, positive and integer add distinct mathematical constraints; they are not interchangeable.
3. **Reduction bridge:** a relation true for a root can be used as a replacement rule for every higher power of that root.
4. **Source-integrity bridge:** a source conflict must be classified, not silently repaired.

## D. INVARIANT_OR_STRUCTURE

### D1 — Transformed-root invariants

For original roots `alpha,beta`, write

`S = alpha + beta`, `P = alpha beta`.

Then derive the transformed sum/product before forming any new equation.

- Shifted roots `alpha+h, beta+h`:
  - `S' = S + 2h`
  - `P' = P + hS + h^2`
- Reciprocal roots `1/alpha,1/beta` (requires `P != 0`):
  - `S' = S/P`
  - `P' = 1/P`
- Squared roots `alpha^2,beta^2`:
  - `S' = S^2 - 2P`
  - `P' = P^2`

Once `S',P'` are known, the monic transformed quadratic is

`y^2 - S'y + P' = 0`.

### D2 — Positive-real structure

For **real** roots `alpha,beta`:

- `P>0` means same sign;
- `S>0` then selects both positive;
- `S<0` selects both negative.

Therefore, for two real roots, positivity requires the reality condition plus `S>0` and `P>0`.

### D3 — Positive-integer structure

Integrality changes the search from continuous to discrete.

Useful restrictions:

- integer roots must satisfy the Vieta sum/product exactly;
- for a monic quadratic with integer constant `P`, candidate integer roots come from signed factor pairs of `P`;
- positivity keeps only positive factor pairs;
- parity of the sum/product can eliminate pairs quickly;
- divisibility information can eliminate pairs before full enumeration.

### D4 — Equality collapse

For positive roots,

`alpha + beta >= 2 sqrt(alpha beta)`.

Equality holds only when `alpha = beta`.

So if the given sum/product hits the equality boundary, the root pair collapses to one value without trial-and-error.

### D5 — Quadratic relation as rewriting machine

If a root `x` satisfies

`x^2 = px + q`,

then for `n >= 2`, multiplying by `x^(n-2)` gives

`x^n = p x^(n-1) + q x^(n-2)`.

Every high power can therefore be reduced to degree at most 1 in `x`.

For special relations, this recurrence may become a short cycle.

For reciprocal structure, if `u + 1/u = k` and `u != 0`, then with

`A_n = u^n + u^(-n)`,

`A_n = k A_(n-1) - A_(n-2)`.

This is a structural reduction route; explicit roots of the underlying quadratic are usually unnecessary.

## E. REPRESENTATIONS

```text
COEFFICIENT FORM
ax^2+bx+c=0
   |
   +--> Vieta S,P
   |       |
   |       +--> transformed S',P'
   |       +--> sign / integer constraints
   |
   +--> FACTOR-PAIR VIEW
   |       integer roots / parity / divisibility
   |
   +--> RELATION VIEW
           x^2=px+q
           |
           +--> linear remainder form Ax+B
           +--> recurrence / cycle
```

The key representation switch is from **individual roots** to **information about the pair** or to **a rewrite rule**.

---

# 3. Decision boundaries — mandatory close contrasts

## DB1 — Transformed roots vs shifted function input

**Surface A:** “The new roots are `alpha+3` and `beta+3`.”

- Correct first move: transform `S,P`.

**Surface B:** “The equation is `f(x+3)=0`.”

- Correct first move: relate `x+3` to a root of `f`; if `r` is a root of `f`, then `x=r-3`.

**Tempting wrong model:** apply the same `+3` root shift in both cases.

**Repair statement:** transforming the *root values* and shifting the *input variable* are inverse-looking but different operations.

## DB2 — Positive real roots vs positive integer roots

**Surface A:** two roots are positive real numbers.

- First move: ensure reality, then use `S>0`, `P>0`.

**Surface B:** two roots are positive integers.

- First move: use `S,P`, then enumerate/trim positive factor pairs and discrete restrictions.

**Tempting wrong model:** stop after sign conditions.

**Repair statement:** positivity is a sign condition; integrality is a discreteness condition.

## DB3 — Solve the quadratic vs reduce powers first

**Surface A:** find the larger root of a quadratic.

- Individual roots may be necessary.

**Surface B:** a root satisfies `x^2=px+q`; simplify `x^20`.

- First move: write the reduction rule/recurrence.

**Tempting wrong model:** quadratic present -> quadratic formula.

**Repair statement:** solve only when the target needs individual root values; otherwise exploit the relation directly.

## DB4 — Valid source mathematics vs source/key conflict

**Surface A:** derivation and source key agree.

- Use the item according to its qualified evidence role.

**Surface B:** printed mathematics and supplied/provisional key disagree.

- Recompute from the printed mathematics; record the disagreement; classify `SOURCE_CONFLICT_EVIDENCE`.

**Tempting wrong model:** silently flip a sign so the key works.

**Repair statement:** source custody is part of mathematical correctness.

## DB5 — Reciprocal roots vs reciprocal sum

**Surface A:** form the quadratic whose roots are `1/alpha,1/beta`.

- Need both transformed sum and product.

**Surface B:** find only `1/alpha + 1/beta`.

- Need only `S/P`; do not build an entire new quadratic.

**Repair statement:** compute only the information the target requests.

## DB6 — Equality boundary vs ordinary factor-pair search

**Surface A:** positive roots have `S^2 = 4P`.

- Equality collapse forces equal roots.

**Surface B:** positive integer roots have ordinary `S,P` away from equality.

- Use factor pairs/discrete search.

**Repair statement:** test a structural equality/boundary before enumerating cases.

---

# 4. MISCONCEPTION_TRAPS

| Trap | Why it attracts a partly prepared learner | Smallest repair |
|---|---|---|
| Solve original roots before every transformation | quadratic formula feels universal | ask whether `S',P'` can be found directly |
| Shifted-input sign error | `f(x+h)` looks like roots move by `+h` | if `f(r)=0`, solve `x+h=r` |
| `P>0` means positive roots | learner remembers product sign only | `P>0` = same sign; use `S` to choose which sign |
| Positive = positive integer | both sound like “restricted roots” | integer adds factor-pair/parity/divisibility constraints |
| Enumerate before checking equality | factor-pair habit is familiar | test AM-GM/discriminant/equality boundary first |
| High power -> solve roots | equation is seen only as a solving task | rewrite `x^2` immediately and reduce |
| Treat relation as identity for every number | algebraic relation is overgeneralized | state: the rewrite is valid for the specified root/value satisfying the relation |
| Trust key over mathematics | answer key feels authoritative | recompute, then label source conflict without repair |

---

# 5. FIRST_MOVE_CUES

| Visible clue | First move that should become automatic |
|---|---|
| roots become `alpha+h,beta+h` | write `S'` and `P'` |
| roots become reciprocals | check `P != 0`, then write `S'=S/P`, `P'=1/P` |
| roots become squares | write `S'=S^2-2P`, `P'=P^2` |
| `f(x+h)=0` | set `x+h=r` where `r` is an original root / substitute a shifted variable |
| “positive real roots” | reality + `S>0` + `P>0` |
| “positive integer roots” | Vieta + positive factor pairs + parity/divisibility |
| equality/boundary language with positive roots | test AM-GM equality before casework |
| `x^2=px+q` with high powers | write the rewrite rule / recurrence before calculation |
| `u+1/u=k` with reciprocal powers | define `A_n=u^n+u^-n` or square/cube structurally |
| printed source result conflicts with derivation | stop, recompute, classify source status |

---

# 6. H3 -> H0 fading plan

Each strand must move from execution support to independence **after an initial attempt**.

## Strand A — transformed roots

- `H3`: first transformed sum/product relation supplied.
- `H2`: cue “work with new sum and product, not individual roots.”
- `H1`: cue only “do you need the roots themselves?”
- `H0`: no method cue; mixed transformed/input-shift surface.

## Strand B — positive/integer roots

- `H3`: list the first admissible factor-pair equation.
- `H2`: cue “separate sign/reality from integrality.”
- `H1`: cue only “which adjective adds a discrete restriction?”
- `H0`: unlabelled feasibility/parameter problem.

## Strand C — structural reduction

- `H3`: provide the first rewrite `x^2 -> px+q` inside the target.
- `H2`: cue “keep degree at most 1.”
- `H1`: cue only “is solving the root actually necessary?”
- `H0`: disguised recurrence/cycle problem.

---

# 7. TRANSFER_ENDPOINTS

A learner owns the unit when they can handle all of the following without topic labels:

1. form a quadratic for shifted roots of an awkward original quadratic without solving it;
2. combine a function-input shift with a later Vieta target and get the shift direction correct;
3. form reciprocal-root and squared-root equations while checking zero/domain conditions;
4. decide whether sign conditions alone suffice or integer factor-pair structure is required;
5. use parity/divisibility to reject impossible positive-integer root data quickly;
6. spot an AM-GM equality collapse before factor enumeration;
7. reduce a high power to `Ax+B` using a quadratic recurrence;
8. detect a short power cycle from a special quadratic relation;
9. use a reciprocal-power recurrence without solving the underlying quadratic;
10. identify a source/key conflict and preserve the printed mathematics without repair.

---

# 8. SOURCE_CUSTODY

| Mechanism | Qualified ID | Role in this unit | Allowed use |
|---|---|---|---|
| shifted function/root structure | `NMTC-BH-P-2024-Q22` | `CLEAN_SCORED_ANCHOR` | ground the distinction “shift input first, then use root structure”; do not reproduce full source wording |
| positive roots / equality collapse | `NMTC-BH-P-2024-Q17` | `CLEAN_SCORED_ANCHOR` | ground positivity + equality mechanism |
| integer/discriminant case restriction | `NMTC-BH-P-2023-Q13` | `BRIDGE_EVIDENCE` | support admissible integer-case reasoning; do not inflate to exact recurrence |
| positive-integer cubic source conflict | `NMTC-BH-P-2025-Q20` | `SOURCE_CONFLICT_EVIDENCE` | source-QC only; printed sign/key conflict must remain unrepaired |
| quadratic relation / power reduction | `NMTC-BH-P-2018-Q06` | `CLEAN_SCORED_ANCHOR` | ground reduction-before-solving |
| reciprocal / low-degree high-power reduction | `NMTC-BH-P-2023-Q03` | `CLEAN_SCORED_ANCHOR` | ground reciprocal-power structural reduction |
| recurrence from `x^2=1-x` style relation | `NMTC-BH-P-2024-Q01` | `CLEAN_SCORED_ANCHOR` | ground recurrence/cycle recognition |

**Source-integrity rule:** historical IDs ground mechanisms. Student practice is author-created unless exact source reproduction is separately authorized. `NMTC-BH-P-2025-Q20` must never appear as a clean canonical PYQ.

---

# 9. Performance interface for downstream mixed mastery (#40)

## Concepts taught

- transformed-root sum/product;
- function-input shift vs root-value transformation;
- positive-real vs positive-integer root constraints;
- factor-pair/parity/divisibility filters;
- AM-GM equality collapse;
- quadratic relation as rewrite rule;
- recurrence/cycle/reciprocal-power reduction;
- source-conflict discrimination.

## Prerequisites assumed

- basic quadratic solving;
- Vieta `S,P` from the preceding root-invariants unit;
- simple factor pairs;
- elementary inequalities/AM-GM;
- algebraic substitution.

## Recognition cues

- “new roots are ...”;
- `f(x+h)`;
- positive/integer adjectives;
- high powers under a degree-2 relation;
- reciprocal powers;
- source/key disagreement.

## First-move rules

1. transformed roots -> write transformed `S',P'`;
2. shifted input -> solve the input relation `x+h=r` / substitute variable;
3. positive real -> reality + sign invariants;
4. positive integer -> discrete factor/parity/divisibility search;
5. high powers -> write reduction rule/recurrence;
6. source conflict -> recompute, do not repair.

## Decision boundaries to mix in #40

- root transform vs input shift;
- positive real vs positive integer;
- equality collapse vs factor enumeration;
- solve roots vs reduce powers;
- clean source vs conflict evidence.

## Misconception tags

- `TRANSFORM_SOLVED_ROOTS_UNNECESSARILY`
- `SHIFT_DIRECTION_ERROR`
- `POSITIVE_PRODUCT_ONLY`
- `INTEGRALITY_IGNORED`
- `EQUALITY_BOUNDARY_MISSED`
- `SOLVED_WHEN_REDUCTION_WAS_ENOUGH`
- `RELATION_TREATED_AS_IDENTITY`
- `SOURCE_CONFLICT_NOT_FLAGGED`

## Transfer mechanisms suitable for mixed mastery

- compound shift + reciprocal transform;
- parameter feasibility with positive integer roots;
- parity-based impossibility;
- short-cycle high-power target;
- reciprocal-power recurrence;
- source-QC decision item.

---

# 10. End-state adoption statement

> When I see transformed roots, I transform the root information first. When roots are restricted, I translate each adjective into a mathematical constraint. When a quadratic relation controls a high power, I reduce before solving. When a source and its key disagree, I preserve the mathematics and record the conflict.
