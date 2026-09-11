# Functional Equations — Source Coverage and PYQ Map

Status: `SOURCE_GROUNDED_2_PRIMARY_ANCHORS__PASS`

| Stable ID | Year/Q | Verified answer | Source/key status | Mechanism | First move |
|---|---|---:|---|---|---|
| `IOQM-2025-Q14` | 2025 Q14 | `12` | HBCSE official / final official key | integer functional equation; strategic special inputs | set `m=0` and `n=0` before doing any recursion |
| `IOQM-2024-Q16` | 2024 Q16 | `08` | HBCSE official / official HBCSE key | reflection/involution pair; linear elimination | write the equation at `x` and `3-x` |

## Source custody

2025 paper:
`https://olympiads.hbcse.tifr.res.in/wp-content/uploads/2025/10/en.M1.pdf`

2025 final key:
`https://olympiads.hbcse.tifr.res.in/wp-content/uploads/2025/10/final-key-7th-September.pdf`

2024 paper:
`https://olympiads.hbcse.tifr.res.in/wp-content/uploads/2025/04/ioqm-2024-english.pdf`

2024 key:
`https://olympiads.hbcse.tifr.res.in/wp-content/uploads/2025/04/ioqm2024-answerkey.pdf`

Historical wording remains source-controlled. This topic uses stable IDs, verified answers and mechanism fingerprints; it does not silently alter a paper stem.

## Independent anchor reconstruction

### IOQM-2025-Q14

The domain is the integers and `f(0)=1`.

From the equation, set `m=0`. The left side becomes `f(1)` and the right side collapses to 2, so `f(1)=2`.

Now set `n=0`. The same left side is `f(1)`, while the right side is `f(m)-m+1`. Hence
`2=f(m)-m+1`, so `f(m)=m+1` for every integer `m`.

Therefore
`f(1)+...+f(N)=2+3+...+(N+1)=N(N+3)/2`.

For `N=12` the sum is 90; for `N=13` it is 104. The largest valid `N` is `12`.

### IOQM-2024-Q16

For every real `x`,
`4f(3-x)+3f(x)=x^2`.

Replace `x` by `3-x`. Since `3-(3-x)=x`,
`4f(x)+3f(3-x)=(3-x)^2`.

With `a=f(x)` and `b=f(3-x)`, solve
`3a+4b=x^2`,
`4a+3b=(3-x)^2`.

Elimination gives
`7f(x)=x^2-24x+36`.

Thus
`f(27)-f(25)=[117-61]/7=8`.

The requested nearest integer is `08`.

## Coverage conclusion

The two anchors deliberately cover different strategic moves:
- a special input that collapses a many-variable expression;
- an involutive partner input that creates a solvable equation pair.

The learner package expands these into integer propagation, equation combination, justified injectivity/surjectivity, and proof-vs-guessing transfers without introducing abstract higher-level function theory.
