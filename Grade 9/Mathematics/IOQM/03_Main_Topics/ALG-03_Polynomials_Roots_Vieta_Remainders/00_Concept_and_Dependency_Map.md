# IOQM Grade 9 - ALG-03 Polynomials, Roots, Vieta & Remainders

Status: `WAVE0_MAP_FROZEN`

## Governing principle

> **THE REQUESTED INFORMATION CHOOSES THE REPRESENTATION.**

## Learner entry model

Assume the learner can expand/factor routine quadratics and solve familiar equations. ALG-01 is a stable prerequisite interface: target-led representation, symmetric reconstruction from already-given data, relation rewriting, and equivalence checks are retrieved rather than rederived.

## Dependency map

```text
F0 polynomial algebra
      |
      +--> frozen ALG-01 interface
      |      target -> representation -> conditions -> check
      |
      v
polynomial representations
  |       |        |         |
coeff   factors   roots    relation/remainder
  |       |        |         |
  |       +--> factor theorem
  |       +--> Vieta derived from factor expansion
  |       +--> transformed-root polynomials
  |
  +--> discriminant/root behavior
  +--> remainder theorem / polynomial reduction
  +--> common-root elimination
```

ALG-02 owns optimization/equality/attainment. A quadratic minimum-value question routes there; a root-count/real-root question routes here.

## Representation router

1. Need individual roots? -> solve/factor if cheapest.
2. Need a symmetric root expression? -> use Vieta invariants first.
3. Need number/type of real roots? -> discriminant/root geometry.
4. Need polynomial whose roots are shifted/scaled? -> transform the **input** carefully.
5. Need remainder/value modulo a relation? -> reduce powers, do not expand high powers.
6. Need common roots? -> eliminate by subtracting/combining equations to lower degree.

## Mandatory decision boundaries

- solve roots vs use symmetric invariants;
- discriminant/root-count vs vertex/minimum-value;
- transformed roots vs shifted polynomial input;
- calculate a high power vs reduce modulo a polynomial relation;
- factor theorem vs merely spotting a numerical value;
- common-root elimination vs solving two polynomials independently.

## Canonical ownership

ALG-03 owns:
- root/factor correspondence;
- Vieta derived from factor expansion;
- discriminant and root behavior;
- transformed roots;
- remainder/factor theorem;
- polynomial reduction/modular remainder language;
- common-root elimination.

## Exit belief

> **I decide whether the target wants coefficients, factors, roots, symmetric invariants, a remainder class, or a feasibility statement before I calculate.**
