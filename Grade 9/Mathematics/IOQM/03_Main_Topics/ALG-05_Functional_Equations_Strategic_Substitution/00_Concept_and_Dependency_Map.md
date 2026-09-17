# Functional Equations — Strategic Substitution

Status: `WAVE0_ARCHITECTURE_FROZEN`

Accepted prerequisite:
- `Grade 9/Mathematics/IOQM/03_Main_Topics/ALG-01_Identities_Transformations/Authoring/ALG01_Stable_Prerequisite_Interface_v1.md`
- provider blob: `fc685ff0a2e9bd67fbd6a920e730b7fff633404b`
- production base at freeze: `bc4a26aa17d9117f8e8ef57459a3414fcec7a156`

ALG-05 retrieves target-led substitution and equivalence discipline. It does not reteach general algebraic transformation.

## Governing learner model

A functional equation is not solved by trying random numbers. The useful input is chosen because it does one of four things:

`COLLAPSE -> PAIR -> ELIMINATE -> PROVE`

- **collapse** a product/sum/shift to a known argument such as 0 or 1;
- **pair** an input with its symmetric partner such as `c-x`;
- **eliminate** an unwanted companion value by adding/subtracting equations;
- **prove** the inferred rule on the whole stated domain.

## Scope boundary

ALG-05 owns:
- special inputs 0, 1 and equation-created constants;
- symmetric/involutive partner substitutions;
- combining two functional equations to eliminate companion values;
- integer-domain propagation when the equation itself links integer inputs;
- concrete injectivity/surjectivity arguments only when they unlock a solution;
- proof of a candidate formula by substitution into the original equation.

ALG-05 does not own:
- general algebraic equivalence doctrine (retrieve ALG-01);
- abstract function-space theory;
- continuity, monotonicity, differentiability, topology, or advanced Cauchy theory;
- generic sequence recurrence methods (ALG-04);
- polynomial/Vieta doctrine (ALG-03).

## Knowledge dependency map

```text
Grade-9 algebra + proof language
        |
        +--> ALG-01 stable interface
                retrieve substitution choice
                retrieve equivalence vs implication
                retrieve candidate checking
        |
        +--> ALG-05
                legal input set
                -> strategic special value
                -> partner equation if present
                -> eliminate companion values
                -> derive rule / requested value
                -> prove on stated domain
```

## Method-selection map

| Visible clue | Structural question | First move | Nearby wrong route |
|---|---|---|---|
| `mn+1`, `xy+1`, product inside argument | Can one variable make the argument 0 or 1? | try an allowed zero/one input | random substitutions |
| `f(c-x)` beside `f(x)` | Does `x -> c-x` return to x? | write the equation again at `c-x` | guess a formula |
| two companion function values | Can two equations eliminate one? | add/subtract or solve a 2x2 system | compute sample values one by one |
| domain is integers | Can a legal unit step propagate all integers? | derive base value and step relation | assume a real-domain theorem |
| same function value appears from two inputs | Would equality force the inputs equal? | compare the two equations | declare injective without proof |
| target asks whether every real is hit | Can an arbitrary target be constructed? | solve for an input producing target | declare surjective from a graph-like intuition |
| several small values fit a pattern | Has the rule been proved for every allowed input? | substitute candidate into original equation | extrapolate from a table |

## Mandatory contrasts

1. **Arbitrary vs strategic substitution** — an input is good because it simplifies the structure, not because it is small.
2. **Functional equation vs recurrence** — a functional equation constrains one function at related inputs; a recurrence generates indexed sequence terms. An integer-domain substitution can produce a recurrence-like step, but the ownership and proof start from the functional equation.
3. **Guessing vs proving** — finite values suggest; the original equation certifies.

## Transfer map

```text
product argument -> zero input -> explicit integer formula
reflection `c-x` -> paired equations -> elimination
integer sum rule -> unit-step propagation -> all integers
nested `x+f(y)` -> compare equal function values -> injectivity
same nested rule -> construct arbitrary output -> surjectivity
sample-value pattern -> candidate -> original-equation verification
```

## Domain discipline

Every substitution must stay inside the stated input domain. In this topic:
- for real-domain equations, affine partners such as `c-x` remain real;
- for integer-domain equations, substitutions such as `m=0`, `n=1`, `n=-1` are legal only because those are integers;
- division by an expression requires a nonzero check before cancellation;
- injectivity/surjectivity are never assumed merely because a formula looks simple.

## Historical anchors

- `IOQM-2025-Q14 = 12`: integer domain; asymmetric `m=0` and `n=0` collapse the equation to `f(k)=k+1`, then the cumulative target gives 12.
- `IOQM-2024-Q16 = 08`: real domain; `x` and `3-x` form a two-equation involution pair, yielding a direct formula and difference 8.

Both anchors are `PASS`, independently verified, and `CLEAN` in the frozen answer-verification authority. No metadata-correction overlay event applies to either.

`WAVE0_ARCHITECTURE_FROZEN`
