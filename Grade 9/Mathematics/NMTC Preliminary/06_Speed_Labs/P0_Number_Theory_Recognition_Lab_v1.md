# P0 Number Theory — Recognition Lab v1

Do **not solve**. Name the first move only. Internal target: 20 items in 6 minutes after learning; not an official NMTC timing claim.

Codes:

`MC` modular cycle; `LM` subtract remainder + LCM; `GD` pairwise differences + GCD; `CR` congruence reconstruction; `PV` place value; `D9` digit sum mod9; `D11` alternating sum / mod11; `IV` integer-valued divisor reduction; `DS` difference of squares; `CP` coprime perfect-power; `PR` prefix residues; `OR` multiplicative order; `AT` attainable-total congruence; `QC` source integrity.

1. Last digit of `9^2027`.
2. `N` leaves remainder 5 on division by 8,12,18.
3. Greatest divisor leaving the same remainder on 91,143,195.
4. `N≡2 mod5`, `N≡4 mod7`.
5. Two-digit number and its reversal.
6. Count `a,b` so `a4b` is divisible by 9.
7. Test divisibility of a five-digit number by 11.
8. `(n+11)/(n+3)` is an integer.
9. `k^2-n^2=120`.
10. `gcd(a,b)=1`, `ab` is a square.
11. Count consecutive blocks whose sum is divisible by 5.
12. Prime `p` divides `2^10+1`; filter possible `p`.
13. Can a score be made from 4-point and 7-point events?
14. Searchable PYQ statement has corrupted exponent notation.
15. Find `5^123 mod13`.
16. One number leaves remainder 2 under 9 and 15.
17. A divisor leaves equal remainders on 100,136,190.
18. Three-digit number with digit sum relation.
19. `ABCABC` appears in a divisibility question.
20. `(2n+9)/(n+2)` must be integer.

## Key

1 MC; 2 LM; 3 GD; 4 CR; 5 PV; 6 D9; 7 D11; 8 IV; 9 DS; 10 CP; 11 PR; 12 OR; 13 AT; 14 QC; 15 MC; 16 LM; 17 GD; 18 PV; 19 PV/D11-style structural factorization; 20 IV.

## Diagnostic

- confuse 2/3 or 16/17 -> `LCM_GCD_REMAINDER_CONFUSION`;
- miss 11/12 -> high-ceiling bridge not adopted;
- solve digit questions without PV -> representation weakness;
- choose ordinary trial for IV -> divisor-reduction weakness.