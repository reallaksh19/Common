# Prime Factorisation, Divisors & Perfect Powers
## First-Step Reference

### One-line router

`FACTOR / INFER EXPONENTS -> TRANSLATE TARGET -> COUNT OR RECONSTRUCT -> CHECK`

| Visible clue | First mathematical line |
|---|---|
| "number of divisors" | write `n=prod p_i^{a_i}` and `tau(n)=prod(a_i+1)` |
| "perfect square" | require every `a_i` even |
| "perfect cube" | require every `a_i` divisible by 3 |
| "greatest perfect-power exponent" | compute `gcd(a_1,...,a_r)` |
| "squarefree" | require every exponent `0` or `1` |
| "divides n!" | compare `v_p(candidate)` with `v_p(n!)` |
| "factor pairs" | pair complementary exponent choices |
| `xy=N`, `gcd(x,y)=1` | assign each complete prime-power block to one side |
| `tau(n)` odd | test whether `n` is a square |
| "smallest n with tau(n)=K" | factor `K` into `(a_i+1)` patterns |
| "divisors of n^2 below n" | pair divisors around `n` first |

## Close contrasts

- gcd/lcm target -> retrieve gcd/lcm structure; multiplicity target -> exponent vector.
- square -> all exponents even; squarefree -> all exponents at most 1.
- count divisors -> independent exponent choices; count factor pairs -> complementary choices.
- candidate divides factorial -> valuation; last digits of factorial -> modular machinery elsewhere.
- minimize number with fixed `tau` -> exponent pattern + ordered primes; merely compute `tau` -> no minimization.

## Checks

1. Did every prime appearing in the number appear in the vector?
2. Did you accidentally use a square criterion for a cube or vice versa?
3. For `gcd(x,y)=1`, did any prime enter both factors?
4. For an extremal construction, did a larger exponent land on a larger prime?
5. For historical source work, did you use the validated statement and key status?
