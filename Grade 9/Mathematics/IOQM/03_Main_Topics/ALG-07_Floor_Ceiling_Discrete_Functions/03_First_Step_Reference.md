# ALG-07 - First-Step Reference

Use after the Assimilation Book.

## Recognition atlas

| Visible clue | First thought |
|---|---|
| `floor(f(x))=n` | `n<=f(x)<n+1` |
| `ceil(f(x))=n` | `n-1<f(x)<=n` |
| negative decimal inside floor | locate between consecutive integers; do not truncate |
| integer shift `x+k` | pull integer `k` outside floor/ceiling |
| fractional part | `x-floor(x)` |
| real interval + integer target | solve real interval, then intersect with `Z` |
| count integers in `[a,b)` | first `ceil(a)`, last `ceil(b)-1` |
| `floor(x)=ceil(x)` | test whether x must be an integer |

## Quick router

```text
FLOOR or CEILING VALUE GIVEN?
  -> write the correct half-open interval

NEGATIVE INPUT?
  -> use order, not truncation

INTEGER SHIFT?
  -> use translation identity

REAL INTERVAL FOUND?
  -> if target is integer, filter only now

COUNTING INTEGERS?
  -> identify first/last admissible integer and check endpoints
```

## First-step cards

### Floor equation
`floor(A)=n` -> `n<=A<n+1`.

### Ceiling equation
`ceil(A)=n` -> `n-1<A<=n`.

### Negative input
Find the consecutive integers surrounding the input.

### Fractional part
Write `{x}=x-floor(x)` before looking at decimal digits.

### Integer filter
Solve the real interval, then intersect with `Z`.

## Contrast strip

- floor vs truncation: negative inputs expose the difference;
- floor vs ceiling: opposite half-open endpoint convention;
- floor equation vs ordinary equation: interval vs single equality;
- real interval vs integer solutions: continuum vs discrete filter;
- included vs excluded endpoint: brackets are mathematical data, not typography.

## 30-second self-check

Before calculating, ask:

1. What integer is the floor/ceiling claiming?
2. Which half-open interval corresponds to it?
3. Which endpoint is strict?
4. Is the final variable real or integer?
5. Can a shift/reflection identity shorten the work?
