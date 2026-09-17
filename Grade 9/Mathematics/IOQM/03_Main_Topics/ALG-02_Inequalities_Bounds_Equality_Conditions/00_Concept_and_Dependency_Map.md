# IOQM Grade 9 - ALG-02 Inequalities, Bounds & Equality Conditions

Status: `WAVE0_MAP_FROZEN`

## Learner entry model

Assume the learner knows order on real numbers, routine algebra, squares are nonnegative, and perhaps remembers AM-GM as a formula. The unstable bridge is deciding whether a bound is in the correct direction, whether equality is feasible, and whether the optimizing value belongs to the requested domain.

## Central learner belief

> **A bound is NOT automatically the requested extremum.**

A minimum/maximum claim requires the correct direction, equality analysis, and attainment in the actual domain.

## Knowledge dependency map

```text
F0 order + algebra + squares >= 0
          |
          +--> ALG-01 frozen interface
          |      target -> representation -> conditions -> check
          |
          v
REQUEST + DOMAIN
      |
      +--> boundedness / direction
      +--> representation choice
      +--> AM-GM / square completion / justified Cauchy-Engel
      +--> equality conditions
      +--> attainment in requested domain
      +--> discrete filter if integers/rationals are required
      |
      +--> optimization conclusion
```

ALG-03 discriminant/root-count machinery is not a prerequisite for canonical ALG-02 teaching. Where a problem is fundamentally about quadratic root existence, route to ALG-03 rather than rebuilding discriminant doctrine here.

## Canonical method-selection router

```text
REQUEST
  -> DOMAIN
  -> BOUNDED?
  -> DIRECTION
  -> REPRESENTATION
  -> BOUND
  -> EQUALITY
  -> ATTAINMENT
  -> DISCRETE FILTER
  -> CHECK
```

## Decision boundaries

- lower bound vs minimum: a lower bound may never be attained;
- upper bound vs maximum: an upper bound may be a strict supremum;
- real optimum vs integer optimum: the real equality point may be inadmissible;
- inequality proof vs optimization: proving `f(x)>=L` is not enough until equality/attainment are checked;
- inequality method vs discriminant feasibility: choose according to the requested information, not because both can produce an inequality;
- AM-GM vs square completion: use the representation naturally matched to positive product structure or quadratic structure.

## Transfer map

- same expression, changed domain -> equality may stop being attainable;
- same bound, changed request -> lower bound may answer minimum, infimum, or neither;
- algebraic product/sum -> AM-GM representation;
- quadratic expression -> completed-square representation;
- reciprocal sum under fixed sum -> Engel/Cauchy representation;
- continuous optimum -> integer candidate filter.

## Canonical ownership

ALG-02 owns boundedness, inequality direction, AM-GM, justified Cauchy/Engel use, completing-square optimization, equality conditions, attainment, and discrete filtering after a continuous bound.

ALG-01 is retrieved for target-led transformation and equivalence. ALG-03 owns Vieta/discriminant/root behavior. Do not duplicate those derivations here.

## Exit belief

> **I do not call a number the minimum or maximum until I know why it is a bound, when equality can occur, and whether that equality case is allowed.**
