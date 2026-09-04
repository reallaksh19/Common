# IOQM Grade 9 — ALG-01 Identities, Transformations & Equation Structure

Status: `WAVE0_ARCHITECTURE_FROZEN`

## Learner entry model

Assume the learner can expand, factor and solve routine equations, but often manipulates algebra without asking **which representation makes the requested target easiest**.

## Governing idea

> Algebraic manipulation is not a sequence of legal moves chosen at random. Choose a transformation because it exposes an invariant, lowers degree, isolates the target, or makes a constraint visible.

## Knowledge dependency map

```text
G9 expansion/factorisation/linear equations
        |
        v
identity vs equation-on-solutions
        |
        +--> factor <-> expand as representation choice
        +--> substitution / renaming repeated structure
        +--> symmetric recombination
        +--> equivalence and reversibility
        +--> hidden low-degree relation / reduction
        |
        +--> stable ALG-01 interface
               +--> ALG-02 inequalities
               +--> ALG-03 polynomials/Vieta
               +--> ALG-05 functional equations
               +--> ALG-06 radicals/logs
               +--> NT-04 Diophantine algebra
```

## Method-selection router

1. **Expression contains a repeated block?** Name it.
2. **Target resembles a factor?** Factor before expanding.
3. **Target resembles a sum/product identity?** Rewrite toward the target.
4. **Equation gives a relation such as `x^2 = ax+b`?** Reduce higher powers using the relation instead of solving for `x` first.
5. **You square, multiply by a variable, or clear denominators?** Check reversibility/domain.
6. **Target is symmetric in two quantities?** Recombine with sum/product identities; detailed Vieta ownership belongs to ALG-03.

## Canonical ownership

ALG-01 owns:
- strategic factor/expand choice;
- substitution for repeated structure;
- identity-driven target reconstruction;
- equivalence vs one-way implication;
- hidden low-degree relation as rewriting rule.

ALG-03 owns Vieta, discriminant and polynomial reduction as canonical topics. ALG-06 owns principal-root and logarithm domain doctrine.

## Transfer map

```text
repeated block -> substitution
              -> lower-degree equation
              -> sequence recurrence compression
              -> functional-equation substitution

relation true on solutions -> rewriting rule
                           -> power reduction
                           -> polynomial remainder methods
```

## Mandatory contrasts

- expand vs factor;
- solve the variable vs compute only the requested expression;
- identity true for all inputs vs equation true only for solutions;
- reversible transformation vs implication that may add solutions.

## Exit belief

> “Before manipulating, I ask what form the target wants.”
