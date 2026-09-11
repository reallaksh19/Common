# NT-03 - Source Coverage Map

All answers below were independently reconstructed from the validated paper statement and
checked against the repository answer-verification ledger.

| Stable ID | Authority / key | Answer | Mechanism | Independent trace |
|---|---|---:|---|---|
| `IOQM-2025-Q06` | HBCSE official / final official | 15 | difference of squares; next perfect cube | If 2025 age is `u^2` and 2012 age is `v^2`, then `(u-v)(u+v)=13`, so `(u,v)=(7,6)`. Age is 49; next cube is 64, hence 15 years. |
| `IOQM-2024-Q01` | HBCSE official / official key | 11 | valuations in `9!` | Every positive integer `1,...,10` divides `9!`; prime 11 does not. |
| `IOQM-2024-Q25` | HBCSE official / official key | 22 | extremal distinct squares | If `|M|=k`, `85k-92=84(k-1)` gives `k=8`; seven distinct squares sum to 588. `24^2` and `23^2` leave too little for six distinct positive squares; `22^2` works with `1,4,9,16,25,49`. |
| `IOQM-2024-Q28` | HBCSE official / official key | 20 | squarefree factor testing | For `A_n=(n^8+3n^4-4)/2`, direct prime-factor verification gives `A_20` squarefree; each `n=21,...,29` has a squared prime factor. |
| `IOQM-2024-Q29` | HBCSE official / official key | 28 | divisor symmetry around `n` | `n=2^19*3^12`; `tau(n^2)=39*25=975`. Hence 487 divisors of `n^2` are below `n`. Of these, 259 are divisors of `n`; `M=228`, last two digits 28. |
| `IOQM-2023-Q01` | HBCSE-linked MTAI / embedded key | 22 | count squares in a moving interval | `M_n=floor(sqrt(4n+1000))-floor(sqrt(4n))`; on `1<=n<=1000`, max is 29 and min is 7. |
| `IOQM-2023-Q09` | HBCSE-linked MTAI / embedded key | 17 | squarefree prime structure | `ab` prime forces one of `a,b` to be 1. Case `a=1` gives 14 ordered distinct-prime pairs `pq<=30`; case `b=1` forces product 30 with three distinct primes, giving 3 more. |
| `IOQM-2023-Q30` | HBCSE-linked MTAI / embedded key | 18 | divisor parity | `d(i)` is odd exactly for squares, so cumulative parity is `floor(sqrt n) mod 2`. Odd square-root blocks up to 2023 contain 990 integers; digit sum is 18. |

## Source-integrity notes

- No anchor here uses a corrected question statement.
- Historical IDs and paper/key authority are inherited from the frozen corpus ledger.
- The source papers are used as evidence; learner-facing text does not reproduce full historical wording.
