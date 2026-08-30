# NT-01 — First-Step Reference

Use after the Assimilation Book.

## Recognition atlas

| Visible clue | First thought |
|---|---|
| “greatest integer dividing all...” | gcd |
| “same remainder” | subtract numbers; divisor divides differences |
| “least positive integer divisible by...” | lcm |
| “first time together / synchronize” | lcm |
| very large gcd pair | Euclidean algorithm |
| gcd and lcm both given | `gcd*lcm = product` |
| common divisor of several linear combinations | take differences / integer linear combinations |

## Quick router

```text
Need a DIVISOR?
  -> common divisor / same remainder -> gcd / differences

Need a MULTIPLE?
  -> least simultaneous multiple -> lcm

Need to SHRINK numbers without changing gcd?
  -> Euclidean algorithm

Need to reconstruct from gcd+lcm?
  -> normalize and use product relation
```

## First-step cards

### Same remainder
Write the numbers as `dq+r`; subtract immediately.

### Euclid
Replace `(a,b)` by `(b, a mod b)`.

### LCM construction
Translate every condition to “this number is a multiple of ...”.

### gcd/lcm pair
Write `a=gu, b=gv`, `gcd(u,v)=1`.

## Contrast strip

- same remainder -> **difference/gcd**, not lcm;
- least simultaneous multiple -> **lcm**, not gcd;
- divisor count / prime exponents -> **NT-03**, not NT-01;
- residue cycles -> **NT-02**, retrieve this topic only for divisibility meaning.

## 30-second self-check

Before calculating, can you answer:
1. am I looking for a divisor or a multiple?
2. can subtraction reduce the problem?
3. is Euclid cheaper than factoring?
4. does gcd*lcm give an invariant?
