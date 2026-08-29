# Quadratics - Transformed Roots, Integer Roots & Structural Reduction
## First-Step Reference - compression layer

> Use this only **after** the Assimilation Module. It compresses understanding; it does not replace the derivations and decision-boundary teaching.

Reference loop:

`SEE -> REALIZE -> WRITE -> CHOOSE -> CHECK`

---

# 1. Recognition atlas

| SEE this clue | REALIZE | WRITE first |
|---|---|---|
| new roots are \(\alpha+h,eta+h\) | root values are transformed | \(S'=S+2h,\;P'=P+hS+h^2\) |
| new roots are \(1/\alpha,1/eta\) | reciprocal transform | check \(P\ne0\), then \(S'=S/P,\;P'=1/P\) |
| new roots are \(\alpha^2,eta^2\) | square the root pair structurally | \(S'=S^2-2P,\;P'=P^2\) |
| equation is \(f(x+h)=0\) | input is shifted, not the roots directly | if \(f(r)=0\), write \(x+h=r\) |
| roots are positive real | sign + reality information | reality condition, then \(S>0,\;P>0\) |
| roots are positive integers | continuous + discrete restrictions | Vieta, then positive factor pairs/parity/divisibility |
| fixed positive product and smallest sum | equality boundary | \(S\ge2\sqrt P\) |
| \(x^2=px+q\) and target has large power | low-degree rewrite controls high degree | \(x^n=px^{n-1}+qx^{n-2}\) |
| \(u+u^{-1}=k\), target has reciprocal powers | reciprocal recurrence | \(A_n=u^n+u^{-n}\), then \(A_n=kA_{n-1}-A_{n-2}\) |
| derivation disagrees with supplied key | source integrity case | recompute -> preserve print -> classify conflict |

---

# 2. Phrase decoder

### “Form a quadratic whose roots are transformed...”

Do **not** solve the original quadratic by default.

1. get \(S,P\);
2. transform to \(S',P'\);
3. write

\[
y^2-S'y+P'=0.
\]

### “Solve \(f(x+h)=0\)”

Do not confuse this with roots \(\alpha+h,eta+h\).

If \(r\) is an original root,

\[
x+h=r\quad\Rightarrow\quad x=r-h.
\]

### “Positive roots”

Ask first: are the roots real?

For two real roots:

\[
P>0\Rightarrow\text{same sign},
\]

and \(S>0\) selects both positive.

### “Positive integer roots”

Add discrete filters:

- factor pairs;
- parity;
- divisibility;
- finite case checking.

### “High power of a root satisfying a quadratic relation”

Write the reduction rule before any root formula.

---

# 3. Decision tree

```text
What does the target ask for?
|
+-- a new equation from changed roots?
|      |
|      +-- roots explicitly changed -> transform S,P
|      |
|      +-- function input changed -> translate x+h=r first
|
+-- roots have adjectives?
|      |
|      +-- real/positive -> reality + signs
|      |
|      +-- integer -> add factor/parity/divisibility structure
|
+-- a large power under a quadratic relation?
|      |
|      +-- yes -> rewrite/recur before solving
|
+-- individual root/larger root requested?
       |
       +-- explicit solving may be justified
```

---

# 4. First-Step cards

## Card A - Shifted roots

Given \(S=\alpha+\beta,\;P=\alpha\beta\), roots become \(\alpha+h,eta+h\):

\[
S'=S+2h,
\]

\[
P'=P+hS+h^2.
\]

**Check:** did you change the roots themselves, or the function input?

## Card B - Reciprocal roots

First:

\[
P\ne0.
\]

Then:

\[
S'=\frac SP,\qquad P'=\frac1P.
\]

**Check:** reciprocal of a zero root is undefined.

## Card C - Squared roots

\[
S'=S^2-2P,\qquad P'=P^2.
\]

**Check:** do not confuse \(\alpha^2+eta^2\) with \(S^2\).

## Card D - Positive roots

For real roots:

\[
P>0\quad\text{and}\quad S>0.
\]

**Check:** \(P>0\) alone means same sign, not necessarily positive.

## Card E - Positive integer roots

Start with \(S,P\), then inspect:

1. positive factor pairs of \(P\);
2. required sum \(S\);
3. parity;
4. divisibility;
5. equality boundary if relevant.

## Card F - Equality collapse

For positive roots:

\[
S\ge2\sqrt P.
\]

Equality iff roots are equal.

## Card G - Rewrite high powers

If

\[
x^2=px+q,
\]

then

\[
x^n=px^{n-1}+qx^{n-2}.
\]

Reduce until only \(Ax+B\) remains, or identify a cycle.

## Card H - Reciprocal recurrence

If \(u+u^{-1}=k\), define \(A_n=u^n+u^{-n}\):

\[
A_0=2,\qquad A_1=k,
\]

\[
A_n=kA_{n-1}-A_{n-2}.
\]

---

# 5. Six decision-boundary contrasts

| Similar surface | Boundary question |
|---|---|
| roots \(\alpha+2,eta+2\) vs \(f(x+2)=0\) | are root values changing, or the input? |
| positive real vs positive integer roots | is sign information enough, or is discreteness added? |
| find a root vs simplify \(x^{20}\) | does the target need individual roots? |
| clean source vs conflicting key | does derivation agree with the source disposition? |
| form reciprocal-root equation vs find reciprocal sum | do you need both transformed invariants or only one? |
| equality boundary vs ordinary integer pair search | can equality collapse the cases first? |

---

# 6. Trap checklist

Before finalizing an answer, ask:

- Did I solve the original roots unnecessarily?
- For \(f(x+h)=0\), did I move the roots in the correct direction?
- Did I check \(P\ne0\) before reciprocals?
- Did I mistake \(P>0\) for “both roots positive”?
- Did I use integer factor/parity/divisibility restrictions when integrality was stated?
- Did I test an equality boundary before enumeration?
- Did I write the quadratic relation as a rewrite rule before high-power work?
- Did I apply a root relation only to the specified value satisfying it, rather than as a universal identity?
- If a source/key conflict appeared, did I preserve it instead of repairing it silently?

---

# 7. Recognition-only self-test

Write only the first move. Stop after one line.

1. Roots of a known quadratic become \(\alpha-4,eta-4\).
2. Solve \(f(x-4)=0\) from known roots of \(f\).
3. A monic quadratic has positive integer roots and product \(36\).
4. A quadratic has two positive real roots and a parameter in its middle coefficient.
5. A root satisfies \(z^2=-z-1\); target is \(z^{202}\).
6. \(w+w^{-1}=5\); target is \(w^7+w^{-7}\).
7. New roots are reciprocal to the old roots and the original constant term is \(0\).
8. A supplied answer key conflicts with a derivation from the printed statement.

If you cannot write the first line without a formula hunt, return to the corresponding MAKE SENSE section of the Assimilation Module.

---

# 8. Source-to-first-step map

| Qualified ID | Evidence role | Mechanism to remember |
|---|---|---|
| `NMTC-BH-P-2024-Q22` | `CLEAN_SCORED_ANCHOR` | shift input first, then use root structure |
| `NMTC-BH-P-2024-Q17` | `CLEAN_SCORED_ANCHOR` | positive-root/equality collapse |
| `NMTC-BH-P-2023-Q13` | `BRIDGE_EVIDENCE` | integer/discriminant admissible cases |
| `NMTC-BH-P-2018-Q06` | `CLEAN_SCORED_ANCHOR` | quadratic relation -> reduce powers |
| `NMTC-BH-P-2023-Q03` | `CLEAN_SCORED_ANCHOR` | reciprocal/low-degree power reduction |
| `NMTC-BH-P-2024-Q01` | `CLEAN_SCORED_ANCHOR` | recurrence/cycle from a quadratic relation |
| `NMTC-BH-P-2025-Q20` | `SOURCE_CONFLICT_EVIDENCE` | recompute and preserve conflict; never canonicalize silently |

---

# 9. Five-second internal script

> **Changed roots?** Transform \(S,P\).
>
> **Changed input?** Translate the variable.
>
> **Positive?** Reality + signs.
>
> **Integer?** Add discrete arithmetic.
>
> **High powers?** Rewrite/recur.
>
> **Conflicting source?** Recompute, preserve, classify.
