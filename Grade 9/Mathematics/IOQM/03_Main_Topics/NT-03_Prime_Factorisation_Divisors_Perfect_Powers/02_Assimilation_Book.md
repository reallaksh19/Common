# Prime Factorisation, Divisors & Perfect Powers
## Integrated Assimilation Book

> **Prime factorisation is a coordinate system for integers. Translate the condition into
> exponent conditions before you count or search.**

## 1. Reconnect: factors are easier in prime coordinates

You already know that `72=8*9=2^3*3^2`. The important upgrade is not the factorisation
itself; it is what the exponents remember.

For a positive integer
`n=p1^a1 p2^a2 ... pr^ar`,
every positive divisor has the form
`d=p1^b1 ... pr^br`
with `0<=bi<=ai`.

This one statement turns a divisor problem into a finite choice problem.

### Fundamental Theorem of Arithmetic

Every positive integer greater than 1 has a prime factorisation, unique apart from the order
of the primes. That uniqueness is why exponent arguments are legitimate: two positive
integers are equal exactly when the exponent of every prime agrees.

## 2. Divisibility becomes componentwise comparison

If
`A=2^5*3^2*7` and `B=2^8*3^2*5*7^4`,
then `A|B`: each exponent required by `A` fits inside the corresponding exponent of `B`.
The extra factor 5 in `B` is harmless.

General rule:

`A|B` iff `v_p(A)<=v_p(B)` for every prime `p`.

The symbol `v_p(N)` means the exponent of `p` in the prime factorisation of `N`.

## 3. Count divisors without listing them

For `n=p1^a1...pr^ar`, each divisor independently chooses exponent `0,1,...,ai`.
Therefore

`tau(n)=(a1+1)(a2+1)...(ar+1)`.

Example: `360=2^3*3^2*5`, so `tau(360)=4*3*2=24`.

### Square divisors

A square divisor must use even exponents. The number of square divisors is

`(floor(a1/2)+1)...(floor(ar/2)+1)`.

### Why divisor parity detects squares

Divisors usually pair as `d` and `n/d`. Exactly one divisor can be unpaired: `sqrt(n)`.
Thus `tau(n)` is odd exactly when `n` is a perfect square.

This is a structural test; enumeration is the wrong route.

## 4. Perfect powers are exponent divisibility

`n` is a square iff every prime exponent is even.

`n` is a cube iff every prime exponent is divisible by 3.

More generally, `n` is a perfect `k`-th power iff every prime exponent is divisible by `k`.

Hence, if `n=2^18*3^12*5^6`, the largest `k>1` for which `n` is a perfect `k`-th power is

`gcd(18,12,6)=6`.

### Minimal multiplier or divisor

To make `756=2^2*3^3*7` a square, fix only the odd exponents:
multiply by `3*7=21`.

To turn a number into a cube, raise each exponent to the next multiple of 3.

## 5. Squarefree structure

A positive integer is squarefree when no prime square divides it. In prime coordinates,
every exponent is 0 or 1.

This is nearly the opposite of a square:

- square: every exponent is even;
- squarefree: every exponent is at most 1.

If a squarefree number has `r` distinct prime factors, it has exactly `2^r` divisors,
because each prime is either included or not included.

## 6. Valuations: focus on one prime at a time

For products, valuations add:

`v_p(AB)=v_p(A)+v_p(B)`.

For factorials, Legendre's formula gives

`v_p(n!)=floor(n/p)+floor(n/p^2)+floor(n/p^3)+...`.

Example:

`v_2(25!)=12+6+3+1=22`.

This is much cheaper than calculating `25!`.

### A key decision boundary

If the question asks whether a candidate divides `n!`, compare each required prime
exponent with the corresponding valuation of `n!`.

If it asks only for a gcd or lcm of two ordinary integers, the earlier gcd/lcm machinery
may be cheaper than full prime factorisation.

## 7. Factor pairs and coprimality

When `xy=N`, the exponent vector of `N` is split between `x` and `y`.

If no gcd condition is present, each prime exponent may be divided between the two factors
in many ways.

If `gcd(x,y)=1`, the rule becomes much sharper: for every prime power `p^a||N`, the
whole block `p^a` must go to exactly one of `x,y`. Splitting the exponent would put `p`
in both factors.

So if `N` has `r` distinct prime factors, the number of ordered coprime factor pairs
`(x,y)` with `xy=N` is `2^r`.

## 8. Extremal reconstruction from a divisor count

Suppose `tau(n)=12`. Factor 12 as exponent-choice products:

- `12` -> exponent pattern `11`;
- `6*2` -> pattern `5,1`;
- `4*3` -> pattern `3,2`;
- `3*2*2` -> pattern `2,1,1`.

To make `n` as small as possible, put larger exponents on smaller primes. Candidates are

`2^11`, `2^5*3`, `2^3*3^2`, `2^2*3*5`.

The minimum is `60`.

This is the governing extremal principle:

> For a fixed multiset of positive exponents, assign them in non-increasing order to
> primes in increasing order.

## 9. Historical decision models

### Two perfect squares separated by 13
A fixed difference between squares suggests difference-of-squares factorisation before
any age enumeration. The factor pair of 13 fixes the ages immediately.

### Smallest integer not dividing a factorial
The surface says "smallest integer", but the hidden test is prime-exponent capacity in
the factorial. This is valuation structure, not a long divisibility table.

### Distinct-square average
Averages first determine how many squares and their total. Then the extremal question
becomes "how much total must be reserved for the smaller distinct squares?"

### Divisors of `n^2` below `n`
Divisor pairing around `sqrt(n^2)=n` halves the divisor set before any detailed
classification.

### Cumulative divisor parity
Replace every `d(i)` by one bit: odd for squares, even otherwise. The enormous-looking
sum becomes a count of square indices.

## 10. Diagnose the common failures

- **Factor-list reflex:** listing divisors when exponent choices count them immediately.
- **Prime-set confusion:** forgetting multiplicity; `2^5` and `2` have the same prime set
  but very different divisor structure.
- **Square/squarefree reversal:** "even exponents" and "exponents at most one" are not
  interchangeable.
- **Perfect-power guesswork:** checking numerical roots instead of taking gcd of exponents.
- **Factorial expansion:** calculating a factorial instead of a valuation.
- **Coprime-pair splitting error:** splitting a prime power between both factors despite
  `gcd(x,y)=1`.
- **Extremal exponent order error:** assigning the largest exponent to a larger prime.

## 11. Fade toward independence

### Full support
Find the number of positive divisors of `2^4*3^2*5`.
Write one factor for each independent exponent choice.

### Reduced support
What is the least multiplier that makes `2^5*3^2*7^3` a square?

### Light support
A number has exactly 18 positive divisors. What exponent patterns are possible?

### Independent
Find the smallest positive integer with exactly 45 positive divisors.

Do not search integer-by-integer. Decide what the divisor-count factorisations force.

## 12. Adopt the router

When an integer-structure problem appears, ask:

1. Can I write or infer its prime exponent vector?
2. Is the target about divisibility, a divisor count, a perfect power, squarefreeness,
   a valuation, or a factor pair?
3. What condition does that target impose on each exponent?
4. Are exponent choices independent, complementary, or forced into whole blocks?
5. If minimizing, have I assigned the largest exponents to the smallest primes?
6. Have I checked all prime exponents and all boundary cases?
