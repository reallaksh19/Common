# Radicals, Exponents & Logs — First-Step Reference v3
## Use only after the Assimilation Book

This is a compression layer, not a teaching chapter.

Use the five-second routine:

\[
\boxed{\text{SEE}\to\text{NAME THE STRUCTURE}\to\text{WRITE THE FIRST LINE}\to\text{CARRY THE CONDITION}\to\text{CHECK}}
\]

---

# 1. Quick decision tree

## Radicals

**Several radicals share a residue?**  
Extract perfect powers and rewrite to a common radical basis.

**One radicand looks like \(A\pm B\sqrt d\)?**  
Test a hidden binomial square/cube before expanding or approximating.

**You see \(\sqrt{g(x)^2}\)?**  
Write \(|g(x)|\) first. Remove the absolute value only after a sign argument.

## Exponents

**Negative/fractional exponent?**  
Stabilize the meaning: reciprocal / radical language first.

**Related bases?**  
Normalize bases before taking logarithms.

**Repeated \(a^x\) pattern?**  
Set \(t=a^x\) and write \(t>0\).

**Homogeneous powers of two bases?**  
Divide by a known positive power and use a ratio variable.

## Risky transformations

**About to square?**  
Write domain and side-sign information first. Use \(\Rightarrow\) unless the restricted domain makes squaring reversible.

**About to divide by \(g(x)\)?**  
Check or split the case \(g(x)=0\) first.

## Reciprocal structure

**Target is symmetric in \(x\) and \(1/x\)?**  
Use \(S_n=x^n+x^{-n}\); do not solve for \(x\) unless the target needs individual branch information.

**Target changes under \(x\leftrightarrow1/x\)?**  
The symmetric invariant may not determine it uniquely.

## Logarithms

**Meaning/law uncertain?**  
Return to

\[
\log_b y=z\iff b^z=y,
\qquad b>0,\ b\neq1,\ y>0.
\]

**Repeated \(\log_bx\)?**  
Set \(t=\log_bx\).

**Repeated \(\sqrt{\log_bx}\)?**  
Set \(u=\sqrt{\log_bx}\), \(u\ge0\).

**Equal logs / related bases?**  
Write the original domain, then convert to common-base or algebraic form.

**Exponent and log share a base?**  
Expose the exact inverse before using decimals.

---

# 2. Nine first-step cards

## Card A — Common radical basis

**Clue:** several radicals reduce to the same irreducible residue.  
**Write:** extract perfect powers.  
**Reject:** \(\sqrt{a+b}=\sqrt a+\sqrt b\).

## Card B — Hidden power / principal root

**Clue:** \(A\pm B\sqrt d\), nested radical, or \(\sqrt{g(x)^2}\).  
**Write:** reverse a square/cube identity; for a squared expression write an absolute value.  
**Check:** square the reconstruction and verify the principal sign.

## Card C — Exponent meaning

**Clue:** negative or fractional exponent.  
**Write:**

\[
a^{-n}=\frac1{a^n}\quad(a\neq0),
\]

and translate fractional powers to radicals when that makes the structure clearer.

## Card D — Normalize / substitute / ratio

**Clue:** related exponential bases or repeated powers.  
**Write:** common base first; otherwise set \(t=a^x>0\) or divide by a positive power and set a ratio variable.  
**Reject:** logarithms by reflex.

## Card E — Reversibility / zero case

**Clue:** squaring, taking roots, multiplying/dividing by a variable expression.  
**Write:** domain/sign/non-zero ledger first.  
**Question:** is this step \(\iff\) or only \(\Rightarrow\)?

## Card F — Reciprocal invariant

**Clue:** \(x^n+x^{-n}\), symmetry under \(x\leftrightarrow1/x\).  
**Write:**

\[
S_0=2,\qquad S_1=x+x^{-1},\qquad
S_n=S_1S_{n-1}-S_{n-2}.
\]

**Reject:** solving for \(x\) when the target is symmetric.

## Card G — Log definition / domain

**Clue:** log law or meaning is uncertain.  
**Write:** exponent form and the base/argument restrictions.  
**Reject:** a fabricated sum law.

## Card H — Repeated log object

**Clue:** the same log structure appears more than once.  
**Write:** name the whole repeated object.  
**Carry:** \(x>0\) and any substitution range such as \(u\ge0\).

## Card I — Log to algebra / exact inverse

**Clue:** equal logs, related log bases, or \(b^{\log_b y}\)-type structure.  
**Write:** original domain first, then convert exactly.  
**Check:** algebraic candidates must still satisfy the original log domain.

---

# 3. Decision-boundary contrasts

| Looks similar | First problem | Near-miss requiring another move |
|---|---|---|
| radicals | \(\sqrt{18}+\sqrt8\): common basis | \(\sqrt{21-8\sqrt5}\): hidden square |
| square notation | \(\sqrt{x^2}=|x|\) | \(u^2=x^2\Rightarrow u=\pm x\) |
| exponents | related bases: normalize | unrelated bases: logs may be useful |
| transformation | cube both real sides: reversible | square both sides: usually candidate-generating |
| division | divide by known non-zero constant | divide by \(g(x)\): preserve \(g(x)=0\) case |
| reciprocal target | symmetric: invariant | asymmetric: branch/sign information may be missing |
| log substitution | repeated \(\log_bx\): \(t=\log_bx\) | repeated \(\sqrt{\log_bx}\): \(u=\sqrt{\log_bx}\) |
| log equation | algebraic candidate | original solution must satisfy every old domain restriction |

---

# 4. Arrow and condition guide

| Transformation | Default status | Condition to remember |
|---|---|---|
| add/subtract same defined expression | \(\iff\) | original domain still applies |
| multiply/divide by known non-zero constant | \(\iff\) | constant must be non-zero |
| divide by \(g(x)\) | conditional | split/prove \(g(x)\neq0\) |
| square both sides | usually \(\Rightarrow\) | becomes \(\iff\) when both sides are known non-negative on the carried domain |
| cube both sides over reals | \(\iff\) | real setting |
| \(\log_b y=z\leftrightarrow b^z=y\) | \(\iff\) | \(b>0,b\neq1,y>0\) |
| equal same-base valid logs \(\to\) equal arguments | \(\iff\) | both arguments positive |
| \(t=a^x\) | representation change | \(t>0\) for \(a>0,a\neq1\) |
| \(u=\sqrt{\log_bx}\) | representation change | \(u\ge0\) plus original log domain |

---

# 5. Recognition-only drill — do not solve

Write only the first move in words.

1. \(\sqrt{50}+\sqrt8-\sqrt2\).
2. \(\sqrt{17-4\sqrt{15}}\).
3. \(\sqrt{(2x-7)^2}\).
4. \(81^{-3/4}\).
5. \(32^x=8^{x+1}\).
6. \(4^x-7\cdot2^x+12=0\).
7. \(9^x-7\cdot6^x+10\cdot4^x=0\).
8. \(\sqrt{x+5}=x-1\).
9. A solution divides \((x-3)(x+2)=0\) by \(x-3\).
10. If \(u+u^{-1}=5\), target \(u^6+u^{-6}\).
11. \(\log_2x-5\sqrt{\log_2x}+4=0\).
12. A transformed log candidate makes an original argument zero.

### Recognition key

1. common radical basis;
2. hidden square;
3. principal root / absolute value;
4. exponent meaning: reciprocal + fractional power;
5. normalize related bases;
6. repeated positive exponential variable;
7. divide by positive power, then ratio variable;
8. domain/sign before squaring;
9. preserve the zero case before division;
10. reciprocal invariant / recurrence;
11. substitute the whole repeated square-root-log object and carry \(u\ge0\);
12. reject by original domain; if the source/key accepts it, record a source conflict rather than repairing the mathematics.

---

# 6. Thirty-second final check

Before accepting an answer, ask:

1. Did I choose the smallest useful representation?
2. Did I solve more of the hidden variable than the target required?
3. Was every risky step reversible on my current domain?
4. Did I keep \(t>0\), \(u\ge0\), log arguments \(>0\), principal-root signs, and zero cases?
5. Did I verify a hidden-square reconstruction instead of trusting its appearance?
6. Did I simplify exact log/exponent structure before approximating?
7. If source and mathematics disagree, did I preserve the disagreement rather than force the key?

If these decisions are stable without chapter labels, the topic is becoming operational rather than memorized.