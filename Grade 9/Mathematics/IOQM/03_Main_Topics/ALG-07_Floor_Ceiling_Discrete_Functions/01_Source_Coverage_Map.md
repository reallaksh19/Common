# ALG-07 - Source Coverage Map

Status: `SOURCE_GROUNDED__ANCHORS_INDEPENDENTLY_RECOMPUTED`

## Validated anchors

| ID | Year/Q | Source/key status | Official answer | Primary mechanism | Fresh independent audit |
|---|---:|---|---:|---|---|
| `IOQM-2024-Q21` | 2024 Q21 | HBCSE official paper / official HBCSE key | 91 | invert two floor constraints, then intersect digit structure | PASS |
| `IOQM-2024-Q26` | 2024 Q26 | HBCSE official paper / official HBCSE key | 33 | set `n=floor(x)`, use `x in [n,n+1)`, test interval feasibility | PASS |

Official paper: `https://olympiads.hbcse.tifr.res.in/wp-content/uploads/2025/04/ioqm-2024-english.pdf`

Official key: `https://olympiads.hbcse.tifr.res.in/wp-content/uploads/2025/04/ioqm2024-answerkey.pdf`

The consolidated verification ledger records both anchors as independently verified `PASS`, with clean source/metadata status.

## Independent audit - IOQM-2024-Q21

The source states that `floor(n/9)` is a three-digit repeated-digit number and `floor((n-172)/4)` is a four-digit permutation of the digits `2,0,2,4`.

Write

`floor(n/9)=111d`, where `d` is one of `1,...,9`.

Then

`111d <= n/9 < 111d+1`,

so, because `n` is an integer,

`999d <= n <= 999d+8`.

The second floor value must be one of the valid four-digit permutations. Since the first condition gives `n<=8999`, the second floor is at most `2206`, so only `2024, 2042, 2204` need inspection.

- value `2024` gives `8268<=n<=8271`;
- value `2042` gives `8340<=n<=8343`;
- value `2204` gives `8988<=n<=8991`.

Only the last interval intersects a repeated-digit interval, namely the `d=9` interval `8991<=n<=8999`, at the unique integer

`n=8991`.

Therefore the requested remainder modulo 100 is `91`.

Independent result: **91**, matching the official key.

## Independent audit - IOQM-2024-Q26

Let `n=floor(x)`. The equation is

`16+15x+15x^2=n^3`, with `x in [n,n+1)`.

The left side is positive, so `n>=1`. On `[n,n+1)` it is increasing. Hence a solution with floor value `n` exists exactly when

`15n^2+15n+16 <= n^3 < 15(n+1)^2+15(n+1)+16`.

The first inequality becomes

`(n-16)(n^2+n+1)>=0`,

so `n>=16`.

For `n=16`, equality occurs at `x=16`, so 16 is admissible. For `n=17`, the right endpoint test still passes, so one solution occurs in `[17,18)`. For `n=18`,

`18^3 > 15(19)^2+15(19)+16`,

and the gap thereafter increases, so no `n>=18` is possible.

Thus the only floor values are `16` and `17`, and their sum is

`16+17=33`.

Independent result: **33**, matching the official key.

## Source custody rules

- Historical wording remains controlled by the official paper.
- Author-created items receive no historical IOQM ID.
- Bridge use in NT/COMB does not inflate primary recurrence counts.
- No official Grade-9-only syllabus or official topic-weightage claim is inferred from these two anchors.
