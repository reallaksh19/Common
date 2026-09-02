# Modular Arithmetic, Residues & Power Cycles - First-Step Reference

## Recognition atlas

| Clue | First move |
|---|---|
| same remainder / congruent | write modulus divides the difference |
| huge power modulo m | reduce base; list a short power cycle |
| last digit | work mod 10 |
| last two digits | work mod 100 |
| modular equation with a coefficient | test whether the coefficient is invertible |
| two congruences | parametrize one class, then test the other |
| shared-factor moduli | check compatibility modulo their gcd first |

## Legal-operation checklist

From `a congruent b (mod m)` you may safely add, subtract, multiply and take positive integer powers. Division or cancellation needs an invertible factor.

Before cancelling `c` from `ac congruent bc (mod m)`, check `gcd(c,m)=1`.

## Power-cycle checklist

1. Choose the modulus from the target.
2. Reduce the base.
3. List powers only until the residue state repeats.
4. Reduce the exponent by the justified cycle length.
5. Handle zero/non-invertible residue cases separately when needed.

## Simultaneous-congruence checklist

1. Check compatibility if moduli share factors.
2. Write one congruence as a parametrized class.
3. Substitute into the other congruence.
4. State the combined repeating class and its period.

## WHY-NOT reminders

- Congruence is not ordinary equality.
- A common factor does not always cancel.
- A large exponent is not a signal to expand.
- The target determines the modulus; do not default to mod 10.
