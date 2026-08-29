# Radicals, Exponents & Logarithmic Transformations — Assimilation Concept Map v3

## Learner assumption

The learner already owns fragments: routine surd simplification, exponent laws, simple same-base equations, and basic logarithm notation. The teaching target is not formula accumulation. It is **representation choice + reversibility + condition custody**.

## One integrated master map

```mermaid
flowchart LR
    A[VISIBLE FORM\nradical / exponent / log / reciprocal] --> B{What structure repeats?}

    B --> R1[COMMON RADICAL BASIS\nextract perfect powers]
    B --> R2[HIDDEN POWER\nreverse square/cube identity]
    B --> E1[COMMON EXPONENTIAL BASE\nnormalize related bases]
    B --> E2[REPEATED POWER / RATIO\nt=a^x>0]
    B --> I1[RECIPROCAL SYMMETRY\nS_n=x^n+x^-n]
    B --> L1[LOG <-> EXPONENT\ndefinition + domain]
    B --> L2[REPEATED LOG OBJECT\nt=log_b x or u=sqrt(log_b x)]
    B --> L3[LOG RELATION -> ALGEBRA\nkeep original domain]

    R1 --> C[SMALLER ALGEBRA]
    R2 --> C
    E1 --> C
    E2 --> C
    I1 --> C
    L1 --> C
    L2 --> C
    L3 --> C

    C --> D{Was the transformation reversible\non the current domain?}
    D -->|YES| EQ[EQUIVALENCE  <=>]
    D -->|NO / CONDITIONAL| IM[CANDIDATES  =>]

    EQ --> K[CHECK CONDITION LEDGER]
    IM --> K

    K --> K1[principal-root sign]
    K --> K2[radical domain]
    K --> K3[log argument > 0\nbase valid]
    K --> K4[t>0 / u>=0]
    K --> K5[zero-divisor case]

    K --> F[ORIGINAL SOLUTION / EXACT VALUE]
    F --> T[TRANSFER: recognize same mechanism\nunder a new surface]

    Q[SOURCE / KEY CONFLICT] --> Q1[recompute independently]
    Q1 --> Q2[preserve printed source]
    Q1 --> Q3[preserve derived mathematics]
    Q1 --> Q4[preserve key disposition]
```

## Missing bridges the book must repair

1. **Representation choice** — ask what equivalent language makes the object smaller before calculating.
2. **Common basis** — several radicals or powers may be the same generator in disguise.
3. **Reverse identity recognition** — read expansions backwards to expose hidden squares/cubes.
4. **Principal-root model** — \(\sqrt{u^2}=|u|\); radical notation is not a built-in \(\pm\).
5. **Exponent meaning** — negative means reciprocal; fractional powers connect to roots.
6. **Equivalence vs implication** — legal forward algebra is not automatically reversible.
7. **Condition ledger** — domain/sign/non-zero/range information survives every rewrite.
8. **Repeated-object substitution** — choose the whole repeating object, not mechanically the innermost one.
9. **Invariant over explicit solving** — symmetric reciprocal targets often do not need the hidden variable.
10. **Logarithm as exponent language** — derive laws and inverses from exponent structure.
11. **Exact structure before decimals** — preserve common-base/inverse structure until simplification is complete.
12. **Source integrity** — a key never overrides valid mathematics.

## Core invariants

- **Perfect-power core:** separate a perfect power from a residual radical basis.
- **Hidden binomial power:** \(A\pm B\sqrt d\) may be a square/cube encoding.
- **Principal-root nonnegativity:** \(\sqrt{u^2}=|u|\).
- **Positive exponential variable:** if \(t=a^x\) with valid positive base, then \(t>0\).
- **Reciprocal recurrence:** \(S_0=2\), \(S_1=x+x^{-1}\), \(S_n=S_1S_{n-1}-S_{n-2}\).
- **Log/exponent inverse:** \(\log_b y=z\iff b^z=y\) for \(b>0,b\neq1,y>0\).
- **Log-domain persistence:** disappearing notation does not erase original restrictions.
- **Source-custody invariant:** clean/sensitive/conflict dispositions do not change because an item is pedagogically useful.

## Decision boundaries / near-miss pairs

| Boundary | First surface | Near-miss |
|---|---|---|
| common basis vs hidden power | \(\sqrt{18}+\sqrt8\) | \(\sqrt{21-8\sqrt5}\) |
| principal root vs square equation | \(\sqrt{x^2}=|x|\) | \(u^2=x^2\Rightarrow u=\pm x\) |
| exponent meaning vs sign | \(2^{-3}=1/8\) | \((-2)^3=-8\) |
| normalize vs logarithm | related bases | unrelated bases may need logs |
| repeated power vs ratio variable | \(a^{2x},a^x\) | homogeneous two-base powers |
| reversible vs candidate-generating | cubing over reals | squaring over reals |
| safe division vs zero loss | known non-zero constant | variable factor \(g(x)\) |
| invariant vs explicit root | symmetric target | asymmetric target |
| log product law vs false sum law | \(\log(MN)\) | \(\log(M+N)\) |
| inner vs whole repeated object | \(\log_bx\) repeats | \(\sqrt{\log_bx}\) repeats |
| algebraic candidate vs original solution | transformed polynomial root | original log/radical domain may reject it |
| learner error vs source conflict | invalid student step | printed key/source disagreement |

## First-move atlas

| Visible clue | First move to test |
|---|---|
| several radicals share residue | extract perfect powers; common basis |
| \(A\pm B\sqrt d\) / nested surd | reverse square/cube identity |
| \(\sqrt{g(x)^2}\) | absolute value / sign check |
| negative/fractional exponent | reciprocal/radical meaning |
| related exponential bases | normalize bases |
| \(a^{2x},a^x,1\) | \(t=a^x>0\) |
| homogeneous two-base powers | divide by positive power; ratio variable |
| even-root equation | original domain/sign, then transform |
| temptation to divide by \(g(x)\) | preserve \(g(x)=0\) case |
| \(x^n+x^{-n}\) | reciprocal invariant/recurrence |
| log law uncertain | convert to exponent meaning |
| repeated \(\log_bx\) | \(t=\log_bx\) |
| repeated \(\sqrt{\log_bx}\) | \(u=\sqrt{\log_bx}\ge0\) |
| equal logs / related bases | domain first, then algebraic relation |
| matching log/exponent base | expose exact inverse |
| source/key contradiction | independent recomputation + source disposition |

## Transfer endpoints

The learner should be able to handle without chapter labels:

- a conjugate pair of hidden surds whose simplification requires reconstructing both radicals;
- a two-base exponential equation solved through a ratio variable;
- a radical/absolute-value equation where squaring becomes reversible only after domain analysis;
- a reciprocal-power problem starting from an asymmetric-looking invariant;
- an exponential version of a reciprocal invariant such as \(a^x+a^{-x}\);
- a logarithmic relation that becomes a polynomial relation between positive variables;
- a log equation where a square creates an absolute-value relation;
- a source-conflicted item where mathematical validity and provenance must be audited separately.

## Source custody

**Clean scored anchors (mechanism grounding only):**

`NMTC-BH-P-2018-Q01`, `NMTC-BH-P-2018-Q21`, `NMTC-BH-P-2018-Q26`, `NMTC-BH-P-2023-Q07`, `NMTC-BH-P-2023-Q21`, `NMTC-BH-P-2023-Q26`, `NMTC-BH-P-2024-Q04`, `NMTC-BH-P-2024-Q09`, `NMTC-BH-P-2024-Q12`, `NMTC-BH-P-2024-Q26`, `NMTC-BH-P-2024-Q28`, `NMTC-BH-P-2025-Q03`, `NMTC-BH-P-2025-Q04`, `NMTC-BH-P-2025-Q09`, `NMTC-BH-P-2025-Q12`, `NMTC-BH-P-2025-Q27`.

**Source-sensitive bridge only:** `NMTC-BH-P-2023-Q04`, `NMTC-BH-P-2023-Q20`.

**Source-conflict/QC only:** `NMTC-BH-P-2025-Q18`.

**Bonus evidence:** none identified; none inferred.

## End-state learner belief

> Radicals, exponents and logarithms are not separate bags of formulas. They are representations. I choose the representation that makes the target smallest, and I do not accept a transformation until I know what information it preserves.