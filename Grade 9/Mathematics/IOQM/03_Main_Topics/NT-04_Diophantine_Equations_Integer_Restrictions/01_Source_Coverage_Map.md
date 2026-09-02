# NT-04 - Source Coverage Map

Status: `WAVE0_ARCHITECTURE_FROZEN`
Main topic: `IOQM-G9-NT-04`

All promoted answers below were independently reconstructed from the validated paper statement and
checked against the repository answer-verification ledger.

| Stable ID | Authority / key status | Answer | Decisive mechanism | Independent trace |
|---|---|---:|---|---|
| `IOQM-2025-Q03` | HBCSE official / final official | 18 | discrete factor-pair optimization | Integer side pairs for area 20 are `(1,20),(2,10),(4,5)`; perimeters are 42,24,18. |
| `IOQM-2025-Q11` | HBCSE official / **final key corrected** | 26 | exact rational gap | `|a/b-3/4|=|4a-3b|/(4b)`. Minimum nonzero determinant is 1. The best admissible denominator is 15 with `4a-45=-1`, giving `a/b=11/15`, distance `1/60`, so `a+b=26`. |
| `IOQM-2024-Q13` | HBCSE official / official key | 19 | factorisation to divisor cases | From `(a-b)(c-1)=66-c`, `a-b=65/(c-1)-1`, hence `c-1|65`. The only feasible positive case with `a+b+c=32` and `a>c` is `(a,b,c)=(19,7,6)`. |
| `IOQM-2023-Q03` | HBCSE-linked MTAI / embedded key | 23 | determinant-gap reconstruction | Let `p=37alpha-16beta>0`, `q=7beta-16alpha>0`. Then `beta=(16p+37q)/3`. Integrality gives `p+q` divisible by 3; minimum positive sum is 3. `(p,q)=(2,1)` yields `(alpha,beta)=(10,23)`, and the alternative `(1,2)` gives beta 30. |
| `IOQM-2023-Q04` | HBCSE-linked MTAI / embedded key; metadata overlay active | 07 | divisibility after exact source correction | Exact paper has `x^4=(x-1)(y^3-23)-1`. Thus `x^4+1=(x-1)(y^3-23)` and reducing mod `x-1` gives `x-1|2`. `x=2` gives no integer y; `x=3` gives `y=4`; maximum `x+y=7`. |
| `IOQM-2023-Q11` | HBCSE-linked MTAI / embedded key | 14 | discriminant-square -> difference of squares | Treat as quadratic in n: discriminant `k^2=16m^2-231`, so `(4m-k)(4m+k)=231`. Positive factor pairs give integer solutions `(m,n)=(29,15),(10,-4),(5,-1),(4,0)` with `|m-n|=14,14,6,4`; maximum 14. |
| `IOQM-2023-Q29` | HBCSE-linked MTAI / embedded key | 95 | multiplicative-partition uniqueness | Remove all 1s. Every representation corresponds to an unordered nontrivial multiplicative partition of n; ones are then forced in number `n-sum(factors)`. 99,98,96 have multiple partitions, 97 has none, while `95=5*19` has exactly one. |

## Source-integrity notes

- `IOQM-2025-Q11`: the final official key corrected the provisional answer from 61 to 26.
  Only the final official value 26 is promoted.
- `IOQM-2023-Q04`: the historical paper is clean. The first-pass repository classifier flattened
  the exponent and displayed `x/4`; the active correction overlay restores the exact paper relation `x^4`.
  This is a metadata correction, not a source conflict.
- Historical IDs and source/key authority are inherited from the frozen corpus ledger.
- Learner-facing material may discuss mechanisms and concise paraphrases; it does not reproduce
  full historical papers.
- No recurrence count from these anchors is promoted as official topic weightage.

## Mechanism coverage

| Mechanism | Anchors |
|---|---|
| discrete factor pairs / integer optimization | 2025-Q03 |
| rational approximation / determinant gaps | 2025-Q11, 2023-Q03 |
| factorisation to finite divisor cases | 2024-Q13, 2023-Q04 |
| quadratic/perfect-square filter | 2023-Q11 |
| sum/product reconstruction / multiplicative partitions | 2023-Q29 |

All seven anchors agree with the independent verification ledger after applying the explicit source
custody notes above.
