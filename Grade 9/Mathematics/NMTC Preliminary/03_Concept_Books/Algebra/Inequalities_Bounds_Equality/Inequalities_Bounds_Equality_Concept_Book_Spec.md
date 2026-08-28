# Inequalities, Bounds & Equality Conditions — Concept Book Spec

## 1. Cognitive contract

Every major concept follows:

`SEE -> REALIZE -> UNDERSTAND -> ADOPT`

Every Preliminary performance task follows:

`RECOGNIZE -> BOUND? -> DOMAIN? -> FIRST MOVE -> EQUALITY CONDITION -> VERIFY -> TRANSFER`

The package must never teach an inequality formula without also teaching:

- what assumptions make it legal;
- what quantity it bounds;
- whether the bound is upper or lower;
- when equality occurs;
- whether the requested extremum actually exists.

## 2. Mastery target

The learner must be able to:

- detect bounded vs unbounded objectives;
- construct an escaping family to disprove a maximum/minimum;
- derive two-variable AM-GM from a square;
- extend AM-GM to simple multi-variable equal-product/sum cases;
- use equality conditions as information, not decoration;
- recognize reciprocal structure suitable for Cauchy/Engel;
- derive a lower bound by completing a square;
- translate root existence into a discriminant inequality;
- solve absolute-value inequalities as distance statements;
- solve simple rational inequalities with sign charts/critical points;
- intersect intervals and count integer/natural solutions;
- separate a true mathematical bound from a supplied source/key claim.

## 3. Chapter architecture

### Unit 0 — Before optimizing, ask whether an optimum exists

SEE: `a b=1`, target `a+b` or `a^2+b^2`.

REALIZE: a minimum may exist while no maximum exists.

UNDERSTAND: use `a=t`, `b=1/t` and test `t->infinity`.

ADOPT: student must decide `MIN / MAX / BOTH / NEITHER` before applying a named inequality.

Required anchor: `NMTC-BH-P-2023-Q17`.

### Unit 1 — Non-negativity is the root of elementary inequalities

Start from:

`(a-b)^2 >= 0`.

Derive:

`a^2+b^2 >= 2ab`.

For positive `a,b` derive:

`(a+b)/2 >= sqrt(ab)`.

Do not present AM-GM as a memorized formula first.

### Unit 2 — Equality conditions carry mathematical information

From `(sqrt(a)-sqrt(b))^2>=0`, equality iff `a=b`.

Teach the distinction:

- inequality gives the bound;
- equality condition tells whether/where the bound is attained.

PYQ connection: 2024 Q17.

### Unit 3 — Fixed sum vs fixed product

Teach:

- fixed positive sum -> product maximized at equality;
- fixed positive product -> sum minimized at equality;
- these statements do **not** automatically give the opposite extremum.

Required contrast:

`ab=1`: `a+b` has minimum 2 but no maximum.

### Unit 4 — Weighted/product bounds without black-box memorization

Use simple normalization and repeated AM-GM where Grade IX/X appropriate.

Avoid advanced named inequality machinery unless the derivation is visible.

High-ceiling items may use weighted forms only after the simple equality logic is secure.

### Unit 5 — Reciprocal constraints and Engel/Cauchy form

Derive from Cauchy in an accessible form:

`(x1^2/a1)+...+(xn^2/an) >= (x1+...+xn)^2/(a1+...+an)` for positive denominators.

For 2018-style reciprocal constraints, show how a target sum pairs naturally with reciprocal coefficients.

Required anchor: 2018 Q12.

### Unit 6 — Completing squares to manufacture bounds

Teach:

`x^2-6x+11=(x-3)^2+2 >= 2`.

Then two-variable examples:

`x^2+y^2+2x-4y+7=(x+1)^2+(y-2)^2+2`.

Required anchors: 2018 Q13, 2025 Q16.

### Unit 7 — Zero sum of non-negative terms

If real quantities satisfy:

`A^2+B^2=0`,

then `A=0` and `B=0`.

This is an equality-collapse tool, not merely an inequality fact.

Required anchor: 2025 Q16.

### Unit 8 — Discriminant as feasibility and bound

For a real quadratic in one variable depending on a parameter, root existence requires:

`D>=0`.

Repeated root:

`D=0`.

Use this to bound parameters or integer possibilities.

Supporting anchor: 2023 Q13.

### Unit 9 — Absolute value is distance

Teach:

`|x-a|<r <=> a-r < x < a+r`.

`|x-a|>r <=> x<a-r or x>a+r`.

Then rational/reciprocal absolute forms with denominator exclusions.

Required anchor: 2025 Q10.

### Unit 10 — Rational inequalities and sign charts

Workflow:

1. move to one side;
2. factor numerator/denominator;
3. list critical points;
4. exclude denominator zeros;
5. test interval signs;
6. apply strict/non-strict endpoint rules.

### Unit 11 — Integer solution counting

Only after the real interval/set is correct:

`REAL SOLUTION SET -> DOMAIN FILTER -> INTEGER/NATURAL FILTER -> COUNT/SUM`.

Supporting anchor: 2023 Q28.

### Unit 12 — Direct bounds and hybrid structure

Examples:

- `|sin x|<=1`, `|cos x|<=1`;
- squares non-negative;
- triangle/geometric feasibility bounds when directly supplied.

Required anchor: 2024 Q30.

### Unit 13 — Source-integrity contrast

Give a deliberately inconsistent key/stem pair involving a claimed maximum or equality value.

Student must:

1. solve printed mathematics;
2. identify conflict;
3. label `SOURCE_CONFLICT`;
4. not modify the problem to fit the key.

### Unit 14 — ADOPT lab

Unlabelled problems mixing:

- boundedness falsifier;
- AM-GM equality;
- Cauchy/reciprocal;
- completion of squares;
- discriminant feasibility;
- absolute/rational intervals;
- integer counts.

Student must write the first move before solving.

## 4. Mandatory contrasts

1. `minimum exists` vs `maximum exists`.
2. AM-GM lower bound vs wrongly claimed upper bound.
3. equality possible vs equality impossible under domain restrictions.
4. `|x-a|<r` vs `|x-a|>r`.
5. numerator zero included vs denominator zero excluded.
6. real interval vs integer solution set.
7. discriminant `>=0` vs `=0`.
8. completing square vs differentiating/calculus (calculus not needed).

## 5. First-move vocabulary

- `BD` — boundedness test
- `AM` — AM-GM/equality
- `CY` — Cauchy/Engel reciprocal
- `CS` — complete square
- `ZZ` — sum-of-squares zero collapse
- `DR` — discriminant feasibility
- `AV` — absolute-value distance
- `RI` — rational inequality sign chart
- `IC` — integer count after interval
- `DB` — direct standard bound
- `QC` — source/consistency check

## 6. Misconception map

- `AMGM_USED_BEFORE_BOUNDEDNESS`
- `MIN_REPORTED_AS_MAX`
- `EQUALITY_CONDITION_OMITTED`
- `EQUALITY_CONDITION_INFEASIBLE`
- `CAUCHY_DENOMINATOR_SIGN_IGNORED`
- `COMPLETING_SQUARE_SIGN_ERROR`
- `DISCRIMINANT_WRONG_DIRECTION`
- `ABSOLUTE_VALUE_INTERVAL_REVERSED`
- `DENOMINATOR_ZERO_INCLUDED`
- `STRICT_ENDPOINT_INCLUDED`
- `INTEGER_FILTER_APPLIED_TOO_EARLY`
- `SOURCE_CONFLICT_NOT_FLAGGED`

## 7. PYQ grounding policy

Use stable IDs and mathematical summaries rather than copying full paper text.

Clean anchors drive teaching. Bonus/starred/source-conflicted items may appear only as explicitly labeled evidence/contrast.

## 8. Publication acceptance

The package is not complete until it has:

- Concept Book student draft;
- source coverage map;
- First-Step cards;
- F0–F4→PYQ→XF ladder;
- >=18 reviewed transfer items;
- 20-item recognition lab;
- 12-item first-line lab;
- 12-question unlabelled mastery test;
- difficulty vectors;
- gate-by-gate QA;
- second math/editorial pass.
