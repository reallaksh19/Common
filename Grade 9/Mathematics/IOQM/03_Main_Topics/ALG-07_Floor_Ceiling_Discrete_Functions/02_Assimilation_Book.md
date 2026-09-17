# Floor, Ceiling & Discrete Functions - Assimilation Book

For a Grade-9 learner who may have seen the symbols but does not yet reliably control intervals, endpoints or negative inputs.

## 1. RECONNECT - what the symbol is trying to say

You may remember that `floor(3.7)=3`. That is not a rule about deleting decimals. The real definition is:

`floor(x)=n  <=>  n<=x<n+1`, for an integer `n`.

Likewise,

`ceil(x)=n  <=>  n-1<x<=n`.

The two symbols encode **half-open intervals**.

Try before reading further:

- What is `floor(-2.3)`?
- What is `ceil(-2.3)`?
- Solve `floor(x)=4` without writing `x=4`.

## 2. DISCOVER - the staircase interval

If `floor(x)=4`, then every real number from 4 up to, but not including, 5 works:

`x in [4,5)`.

If `ceil(x)=4`, then

`x in (3,4]`.

The endpoint direction is the first major decision boundary:

- floor: include the lower integer, exclude the next;
- ceiling: exclude the previous integer, include the upper integer.

## 3. MAKE SENSE - negative inputs expose truncation errors

`-3 < -2.3 < -2`.

The greatest integer not exceeding `-2.3` is `-3`, so

`floor(-2.3)=-3`.

Truncating toward zero would give `-2`, which is wrong for floor.

For ceiling, the least integer at least `-2.3` is `-2`:

`ceil(-2.3)=-2`.

So the safest habit is not "drop decimals". It is "locate the number between consecutive integers".

## 4. Integer shifts and reflection

For every integer `k`,

`floor(x+k)=floor(x)+k`,

`ceil(x+k)=ceil(x)+k`.

Also,

`ceil(x)=-floor(-x)`.

These are representation shortcuts, not new casework.

## 5. Fractional part

Define

`{x}=x-floor(x)`.

Then always

`0<={x}<1`.

For positive decimals this resembles the digits after the point. For negative numbers it does not:

`{-2.3}=-2.3-(-3)=0.7`.

That is why "fractional part" is structural, not typographical.

## 6. Floor equations are interval equations

Example:

`floor((2x+1)/3)=4`.

Do not write `(2x+1)/3=4`.

Translate first:

`4 <= (2x+1)/3 < 5`.

Then solve:

`11/2 <= x < 7`.

One discrete value has encoded a whole real interval.

For ceiling,

`ceil((3x-1)/2)=5`

means

`4 < (3x-1)/2 <= 5`,

so

`3 < x <= 11/3`.

## 7. Real interval first, integer filter second

Suppose `n` is required to be an integer and

`floor((n+1)/3)=2`.

First solve over the reals:

`2 <= (n+1)/3 < 3`,

hence

`5 <= n < 8`.

Now use the integer filter:

`n in {5,6,7}`.

Do not mix the two stages mentally. First decode the real interval; then intersect it with the required discrete domain.

## 8. Counting integers in a real interval

If you need integers `m` with

`a <= m < b`,

the first candidate is `ceil(a)` and the last is `ceil(b)-1`. The count is

`ceil(b)-ceil(a)`

when the interval is nonempty.

For a closed interval `[a,b]`, the count is

`floor(b)-ceil(a)+1`

when nonempty.

## 9. TRY - attempt before help

### Track A - floor equation

Solve `floor((x-1)/2)=3`.

Attempt first.

- **Full support:** write `3 <= (x-1)/2 < 4`, then solve both sides.
- **Structural prompt:** replace the floor equation by its half-open interval.
- **Recognition prompt:** which endpoint is strict for floor?
- **Independent target:** solve `floor((3x+2)/5)=-1` independently.

### Track B - ceiling equation

Solve `ceil((x+2)/3)=2`.

Attempt first.

- **Full support:** write `1 < (x+2)/3 <= 2`.
- **Structural prompt:** ceiling uses a left-open, right-closed interval.
- **Recognition prompt:** decode before doing algebra.
- **Independent target:** solve `ceil((2x-5)/4)=-2` independently.

### Track C - integer filtering

Find all integers `n` with `floor((n-2)/4)=3`.

Attempt first.

- **Full support:** `3 <= (n-2)/4 < 4`, then keep only integers.
- **Structural prompt:** solve a real interval, then intersect with `Z`.
- **Recognition prompt:** do not count before the interval is correct.
- **Independent target:** find the number of integers `n` satisfying `ceil(n/5)=3`.

## 10. DIAGNOSE - common wrong starts

### Wrong start 1: floor means truncation

Works accidentally for some positive numbers; fails immediately for negative inputs.

### Wrong start 2: `floor(f(x))=k` means `f(x)=k`

False. The correct statement is `k<=f(x)<k+1`.

### Wrong start 3: forgetting the strict endpoint

Changing `[k,k+1)` into `[k,k+1]` can create a false extra solution.

### Wrong start 4: filtering integers too early

First solve the real interval. Then apply the integer condition.

### Wrong start 5: importing general inequality machinery

Most floor problems are not optimization problems. The first move is usually interval translation, not an inequality theorem.

## 11. ADOPT - seven mental rules

1. `floor(x)=n <=> n<=x<n+1`.
2. `ceil(x)=n <=> n-1<x<=n`.
3. Negative input: never trust truncation intuition.
4. Integer shifts pass through floor/ceiling.
5. `ceil(x)=-floor(-x)`.
6. `{x}=x-floor(x)` lies in `[0,1)`.
7. Decode interval first; integer-filter second.

## 12. Validated IOQM anchors

- `IOQM-2024-Q21`: two floor intervals intersect digit structure; answer 91.
- `IOQM-2024-Q26`: set `n=floor(x)`, use `x in [n,n+1)`, and test feasibility; floor values 16 and 17 sum to 33.

Use the validated paper for exact historical wording.

## 13. TRANSFER

The same mechanism appears when:

- a counting problem asks how many integer labels lie inside a real interval;
- a number-theory condition narrows an integer into a one-unit floor interval;
- a combinatorics state is selected by `floor(t/T)`;
- a negative parameter makes truncation and floor diverge.

The surface changes. The first question stays:

> "What half-open interval does this discrete value encode?"
