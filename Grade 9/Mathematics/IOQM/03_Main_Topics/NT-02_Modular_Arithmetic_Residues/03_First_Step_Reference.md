# NT-02 - First-Step Reference

## Recognition atlas

| Clue | First move |
|---|---|
| same remainder / congruent | write modulus divides the difference |
| huge power modulo m | reduce base; list a short power cycle |
| last digit | work mod 10 |
| last two digits | work mod 100 |
| common factor on both sides | test gcd(factor,m)=1 before cancelling |
| `ax congruent b` | look for inverse of a, if it exists |
| two congruences | parametrize/list one class and test the other |
| distinct residues | convert collision to divisibility of a difference |
| `n^n`-style periodicity | track both base residue and exponent residue |

## Router

`MODULUS -> REDUCE -> LEGAL? -> CYCLE/COMBINE -> CHECK`

## Contrast strip

- equality vs congruence: exact value vs residue class;
- divisibility vs congruence: one expression vs comparison by difference;
- brute powers vs cycle: expansion vs finite state;
- legal vs illegal cancellation: inverse exists vs not;
- mod 10 vs mod 100: target decides modulus;
- compatible vs incompatible simultaneous congruences.

## Quick legality checks

Safe: add, subtract, multiply, raise congruent quantities to positive integer powers.

Conditional: cancel/divide only through an inverse; check gcd with the modulus first.
