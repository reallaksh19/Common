# ALG-06 Independent Mathematics and Source Audit

Status: `HISTORICAL_ANCHORS_INDEPENDENTLY_CLOSED`

This audit uses the exact controlled historical stem for `IOQM-2025-Q28` from the official paper/correction overlay and the exact source statement for `IOQM-2023-Q02`. Official answers are used only as a final check after an independent derivation.

## IOQM-2025-Q28

Controlled stem:

> Assume `a` is a positive integer which is not a perfect square. Let `x,y` be non-negative integers such that
> `√(x - √(x+a)) = √a - y`.
> Find the largest possible `a<100`.

### Domain first

The left side is a principal square root, so it is non-negative. Therefore

`√a - y >= 0`.

Because `a` is not a perfect square and `y` is an integer, equality cannot occur; hence `y < √a`.

### Prove `y=0`

Both sides are non-negative, so squaring is reversible:

`x - √(x+a) = a + y^2 - 2y√a`.

Rearrange:

`√(x+a) - 2y√a = x-a-y^2`.

The right side is an integer. Let

`k = x-a-y^2`.

Then

`√(x+a) = k + 2y√a`.

Suppose `y>0`. Squaring gives

`x+a = k^2 + 4y^2 a + 4ky√a`.

The left side is an integer. Since `a` is nonsquare, `√a` is irrational. Thus the irrational term can vanish only if `k=0`.

So `√(x+a)=2y√a`, and therefore

`x+a = 4y^2 a`,

hence `x=a(4y^2-1)`.

But `k=0` also means

`x-a-y^2=0`.

Substitution yields

`a(4y^2-2)=y^2`,

so

`a = y^2/(4y^2-2) < 1`

for every integer `y>=1`, impossible because `a` is a positive integer.

Therefore

`y=0`.

### Reduce to a triangular-number form

The equation becomes

`√(x - √(x+a)) = √a`.

Again both sides are non-negative, so squaring is reversible:

`x - √(x+a)=a`.

Thus

`√(x+a)=x-a`.

The right side is an integer and non-negative. Set

`t=x-a`.

Then `t` is a non-negative integer and

`t^2=x+a=(a+t)+a=2a+t`.

Hence

`2a=t^2-t=t(t-1)`,

so

`a=t(t-1)/2`.

For `a<100`, `t=14` gives

`a=14*13/2=91`,

while `t=15` gives `105>100`. Also `91` is not a perfect square.

Therefore the largest admissible value is

`91`.

Independent result: `91` — matches verification authority.

### Reversibility record

| move | condition | status |
|---|---|---|
| original equation -> first square | both sides non-negative from principal-root domain and `√a-y>=0` | `⇔` |
| irrationality argument | `a` nonsquare and `y>0` | exact contradiction route |
| `y=0` equation -> second square | both sides non-negative | `⇔` |
| `√(x+a)=x-a` -> `t` substitution | equality itself proves `x-a>=0` | `⇔` |

No extraneous candidate survives because no implication-only squaring was used without its sign condition.

---

## IOQM-2023-Q02

Controlled stem:

Find the number of ordered pairs `(a,b)` of natural numbers with `2<=a,b<=2023` satisfying

`log_a(b) + 6 log_b(a) = 5`.

### Domain

Since `a,b>=2`, both logarithms are defined with positive bases different from `1`, and both are positive.

Set

`t = log_a(b)`.

Then

`log_b(a)=1/t`.

So

`t + 6/t = 5`.

Multiplying by positive `t` gives the equivalent quadratic

`t^2-5t+6=0`,

hence

`t=2` or `t=3`.

### Case 1: `t=2`

`b=a^2`.

The bound `b<=2023` gives `a<=44` because `44^2=1936` and `45^2=2025`.

Thus

`a=2,3,...,44`,

which gives `43` ordered pairs.

### Case 2: `t=3`

`b=a^3`.

The bound `b<=2023` gives `a<=12` because `12^3=1728` and `13^3=2197`.

Thus

`a=2,3,...,12`,

which gives `11` ordered pairs.

Total:

`43+11=54`.

Independent result: `54` — matches verification authority.

### Reversibility record

- `log_b(a)=1/log_a(b)` is valid because both bases are positive and not `1`, and `a,b>1` makes `t>0`.
- multiplying by `t` is reversible because `t>0`.
- each root `t=2,3` is converted back to an exact exponent relation and counted under the original integer bounds.

---

## Audit disposition

- exact Q28 nested-radical correction consumed: PASS;
- Q28 domain/sign discipline: PASS;
- Q28 independent answer `91`: PASS;
- Q02 logarithm-domain discipline: PASS;
- Q02 independent answer `54`: PASS;
- official/verification-ledger answer agreement: 2/2 PASS;
- historical figure dependency: none for these two source statements;
- classroom readability/timing: `NOT_RUN`.

Next authoring gate: build the seven microstream A-P interfaces, with principal-root/domain/reversibility doctrine treated as a cross-cutting invariant rather than a late warning.
