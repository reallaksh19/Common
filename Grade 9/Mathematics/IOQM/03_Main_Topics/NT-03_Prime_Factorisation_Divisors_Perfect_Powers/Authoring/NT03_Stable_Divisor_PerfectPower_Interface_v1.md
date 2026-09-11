# NT-03 Stable Divisor / Perfect-Power Interface v1

Status: `FROZEN_FOR_DOWNSTREAM_CONSUMPTION_CONTENT_PATCH_RENDER_PENDING`
Main topic: `IOQM-G9-NT-03`
Canonical owner: `IOQM-G9-NT-03`

## Exported model
`INTEGER -> PRIME EXPONENT VECTOR / DIVISOR STRUCTURE -> RESTRICTION -> FINITE CASES -> CHECK`

## Downstream may assume
1. unique prime factorisation;
2. `A|B` iff `v_p(A)<=v_p(B)` for every prime;
3. `tau(prod p_i^a_i)=prod(a_i+1)`;
4. square iff all exponents are even;
5. cube iff all exponents are divisible by 3;
6. perfect `k`-th power iff all exponents are divisible by `k`;
7. greatest perfect-power exponent is `gcd(a_i)`;
8. squarefree iff every exponent is 0 or 1;
9. `tau(n)` is odd iff `n` is a square;
10. `v_p(AB)=v_p(A)+v_p(B)` and factorial valuations use Legendre's sum;
11. if `xy=N` and `gcd(x,y)=1`, each full prime-power block belongs wholly to one factor;
12. for a fixed exponent pattern, the smallest integer assigns larger exponents to smaller primes;
13. a positive integer is a sum of at least two consecutive positive integers iff it has an odd divisor greater than `1`, equivalently iff it is **not** a power of `2`.

## Consecutive-sum export boundary

For

`n=a+(a+1)+...+(a+r-1)`, `a>=1`, `r>=2`,

NT-03 exports the structural factorization

`2n=r(2a+r-1)`

and the odd-divisor / power-of-two existence criterion. NT-03 does **not** own enumeration of all `(a,r)` pairs.

## NT-04 consumption contract

NT-04 may retrieve these facts while teaching integer factorisation into cases, parity/gcd/bound filters, finite-case completeness and integer reconstruction. For consecutive sums it owns:
- choosing the correct complementary factor pair of `2n`;
- recovering `a` and `r`;
- positivity and `r>=2` checks;
- counting/all-representation questions;
- any extra bounds or admissibility filters.

It must not become a second divisor-count/perfect-power chapter.

## Non-exports
Generic gcd/lcm and Bézout/extended Euclid (NT-01), congruence/cycles (NT-02), general Diophantine reconstruction (NT-04), polynomial/discriminant canon (ALG-03).

## Verification
Historical anchors 8/8 independently reconstructed; author-created numerical items independently checked; consecutive-sum existence criterion independently derived; dependency inversion NONE; downstream content status `READY_FOR_RETRIEVAL`; previous render certification invalidated by learner-source change; current render recertification `PENDING`; classroom/retention/psychometrics `NOT_RUN`.
