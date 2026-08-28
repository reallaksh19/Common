# Greatest / Least Integer Functions — Concept Book Specification v1

## Cognitive contract

`SEE -> REALIZE -> UNDERSTAND -> ADOPT`

Performance contract:

`SYMBOL -> INTERVAL -> ENDPOINTS -> CASE/DOMAIN -> SOLVE -> VERIFY`

The learner should finish the unit believing:

> A floor or ceiling symbol is usually an interval statement in disguise.

---

# Unit architecture

## Unit 0 — prerequisite diagnostic

Check:

- inequalities on the number line;
- open/closed interval notation;
- integer vs real distinction;
- negative-number ordering;
- linear/quadratic inequality solving;
- basic counting of integers in an interval.

## Unit 1 — definitions from order

Teach:

`floor(x)=greatest integer <=x`

`ceil(x)=least integer >=x`.

Contrast `floor(-2.3)=-3` with truncation toward zero `-2`.

## Unit 2 — the two master equivalences

For integer `m`:

`floor(x)=m <=> m<=x<m+1`

`ceil(x)=m <=> m-1<x<=m`.

These are the main solving tools.

## Unit 3 — graph and boundary grammar

Build the step graph from intervals, not by memorized drawing.

Train endpoint discipline:

- floor: closed left, open right;
- ceiling: open left, closed right.

Check every integer boundary explicitly.

## Unit 4 — integer shifts and reflection

Derive for integer `n`:

`floor(x+n)=floor(x)+n`

`ceil(x+n)=ceil(x)+n`.

Derive:

`ceil(x)=-floor(-x)`.

Then derive:

`floor(x)+floor(-x)=0` if `x` is integer, otherwise `-1`.

## Unit 5 — fractional part

Define:

`{x}=x-floor(x)` with `0<={x}<1`.

Negative-number example:

`{-1.3}=0.7`.

Teach decomposition:

`x=floor(x)+{x}`.

Use `x=n+r`, `n` integer and `0<=r<1`, as a universal case engine.

## Unit 6 — equations

Main route:

1. set the floor/ceiling output to an integer;
2. translate to an interval;
3. solve the inner inequality;
4. intersect with domain;
5. check endpoints.

Examples:

`floor(2x+1)=5 -> 2<=x<5/2`.

`ceil(3x-2)=4 -> 5/3<x<=2`.

## Unit 7 — inequalities

For integer `m`, derive:

- `floor(y)>=m <=> y>=m`;
- `floor(y)<=m <=> y<m+1`;
- `ceil(y)<=m <=> y<=m`;
- `ceil(y)>=m <=> y>m-1`.

Do not replace strict endpoints by intuition.

## Unit 8 — equations involving x and floor(x)

Set:

`n=floor(x)`, so `n<=x<n+1`.

Then solve algebraically and require the result to lie in its defining interval.

This is the preferred route for expressions such as:

`x+floor(x)=7/2`

or

`floor(x)+floor(2x)=k`.

## Unit 9 — nested forms and idempotence

Since `floor(x)` and `ceil(x)` are integers:

`floor(floor(x))=floor(x)`

`ceil(floor(x))=floor(x)`

`ceil(ceil(x))=ceil(x)`

`floor(ceil(x))=ceil(x)`.

Contrast these with nontrivial forms such as `floor(2floor(x/2))`.

## Unit 10 — sum/product structure

Derive:

`floor(x)+floor(y) <= floor(x+y) <= floor(x)+floor(y)+1`.

Using fractional parts, decide exactly when the extra `1` appears.

Reject false identities such as:

`floor(x+y)=floor(x)+floor(y)` always.

## Unit 11 — counting integers with floor/ceiling

For real `a<=b`, number of integers in `[a,b]` is

`max(0, floor(b)-ceil(a)+1)`.

Derive variants for open/half-open intervals by endpoint adjustment rather than memorizing four formulas.

## Unit 12 — Preliminary transfer bridges

Use floor/ceiling to connect with:

- divisibility and quotient/remainder;
- number of complete groups / minimum containers;
- square-root intervals;
- sequence indexing;
- counting lattice/integer solutions;
- final-value flooring after another primary mechanism.

`NMTC-BH-P-2024-Q27` belongs here only as bridge evidence.

## Unit 13 — error-check laboratory

Mandatory contrasts:

1. floor vs truncation for negative numbers;
2. floor vs ceiling endpoints;
3. identity vs case-dependent statement;
4. direct interval translation vs graph guessing;
5. floor as primary mechanism vs incidental final operation;
6. source evidence vs author-created syllabus practice.

---

# Mastery standard

Ready for mixed Preliminary use only when the learner can:

1. classify at least 9/10 floor/ceiling interval forms correctly;
2. solve at least 8/10 boundary-sensitive equations/inequalities;
3. handle negative examples without truncation errors;
4. derive reflection and fractional-part identities;
5. solve one mixed integer-counting problem;
6. reject at least 4/5 plausible false floor identities;
7. preserve provenance when no clean PYQ family exists.
