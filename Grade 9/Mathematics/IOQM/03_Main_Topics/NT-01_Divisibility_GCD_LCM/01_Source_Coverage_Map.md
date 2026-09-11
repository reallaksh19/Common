# NT-01 - Source Coverage Map

Status: `SOURCE_GROUNDED__ANCHORS_INDEPENDENTLY_RECOMPUTED`

## Authority

The historical anchors below use the HBCSE official IOQM 2025 Set M1 question paper and the final official answer key. Stable IDs are inherited from the 90-question corpus. This topic does not infer any official Grade-9 syllabus or topic weightage from the two anchors.

| ID | Year/Q | Paper/key status | Official answer | NT-01 role | Independent audit |
|---|---:|---|---:|---|---|
| `IOQM-2025-Q02` | 2025 Q2 | HBCSE official paper; `FINAL_OFFICIAL` key | 17 | direct divisibility counting bridge | PASS |
| `IOQM-2025-Q27` | 2025 Q27 | HBCSE official paper; `FINAL_OFFICIAL` key | 40 | lcm equation, gcd normalization, integer triples | PASS |

Official paper: `https://olympiads.hbcse.tifr.res.in/wp-content/uploads/2025/10/en.M1.pdf`

Final key: `https://olympiads.hbcse.tifr.res.in/wp-content/uploads/2025/10/final-key-7th-September.pdf`

## Independent mathematical audit - IOQM-2025-Q02

The official stem asks for positive integers `n <= 100` divisible by 3 but not by 2.

- multiples of 3: `floor(100/3)=33`;
- those also divisible by 2 are multiples of 6: `floor(100/6)=16`;
- required count: `33-16=17`.

Independent result: `17`, agreeing with the final key.

## Independent mathematical audit - IOQM-2025-Q27

For the official relation, write

`x = gcd(a,c)`, `y = gcd(b,c)`.

Using `lcm(a,c)=ac/x` and `lcm(b,c)=bc/y`, cancellation of `c` gives

`27(a/x + b/y) = 26(a+b)`.

Thus

`a(27/x-26) + b(27/y-26)=0`.

For a positive gcd value, `27/t-26` is positive only at `t=1`; for every integer `t>=2` it is negative. Therefore exactly one of `x,y` equals 1. Suppose `x=1` and `y>1`. Then

`a = b(26y-27)/y`.

Since `y|b`, let `b=yt`. Then `a=(26y-27)t`. The bound `a<=50` forces `y=2`; coprimality with `c` then forces `t=1`, so `(a,b)=(25,2)`. Now `c=2s<=50` and `gcd(25,c)=1`, so `s` may be any integer from 1 to 25 except multiples of 5: 20 choices. The symmetric case `(a,b)=(2,25)` gives another 20.

Independent result: `40`, agreeing with the final key.

## Source custody rules

- Exact historical wording and figures remain controlled by the official paper.
- Student material may cite the stable ID and mechanism without pretending author-created variants are PYQs.
- Author-created items use `AUTHOR_CREATED_FOUNDATION`, `AUTHOR_CREATED_RECOGNITION`, `AUTHOR_CREATED_TRANSFER` or `AUTHOR_CREATED_MASTERY` in metadata.
- The two anchors are primary recurrence owners only once each; bridge use elsewhere does not inflate counts.

## Ownership note

`IOQM-2025-Q27` is cross-tagged with integer-structure reasoning, but the frozen primary owner remains NT-01 because the decisive reduction is through lcm/gcd normalization. No ownership change is proposed.
