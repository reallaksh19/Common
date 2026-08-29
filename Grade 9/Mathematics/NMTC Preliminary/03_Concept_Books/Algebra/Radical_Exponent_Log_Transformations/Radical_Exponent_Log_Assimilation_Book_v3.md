# Radicals, Exponents & Logarithmic Transformations — Assimilation Book v3
## Grade IX/X competitive-foundation learning book

### Who this book is for

You probably already know some exponent laws, can simplify familiar surds, and remember that logarithms are related to exponents. The difficulty begins when the surface changes:

- three radicals look unrelated but share one basis;
- an ugly surd is actually a perfect square in disguise;
- an exponential equation should be normalized rather than logged;
- a legal transformation is not reversible;
- a symmetric target can be found without solving the hidden variable;
- logarithms disappear, but their domain restrictions must remain.

This book repairs those connections.

The learning loop is

\[
\text{RECONNECT}\to\text{DISCOVER}\to\text{MAKE SENSE}\to\text{TRY}\to\text{DIAGNOSE}\to\text{FADE}\to\text{ADOPT}\to\text{TRANSFER}.
\]

The mathematical loop is simpler:

\[
\boxed{\text{SEE}\to\text{REPRESENT}\to\text{SOLVE SMALLER ALGEBRA}\to\text{CHECK}}.
\]

A transformation is not complete until you can answer two questions:

1. Did I preserve the exact solution set, or did I only generate candidates?
2. Which domain, sign, non-zero, or range condition must survive?

---

# 0. RECONNECT DIAGNOSTIC — attempt before any help

Do these without notes. Do not look for hints yet.

1. Simplify \(\sqrt{72}\).
2. Simplify \(\sqrt{(x-4)^2}\) for real \(x\).
3. Evaluate \(16^{-3/4}\).
4. Solve \(8^x=4^{x+1}\).
5. Is squaring both sides of a real equation always reversible? Give one sentence.
6. Why can dividing \((x-2)(x+3)=0\) by \(x-2\) lose a solution?
7. If \(u+u^{-1}=4\), find \(u^2+u^{-2}\).
8. Rewrite \(\log_3 81=4\) in exponent form.
9. State the real domain of \(\log_2(x-5)\).
10. Is \(\log(a+b)=\log a+\log b\) a logarithm law?
11. If \(v=\sqrt{\log_2 x}\), what restriction belongs beside \(v\)?
12. For \(9^x-5\cdot6^x+4\cdot4^x=0\), what repeated object or ratio would you try before solving?

Do not score yourself yet. The diagnostic key is in the separate teacher/diagnostic key. Its purpose is to identify the missing bridge, not to label the learner.

---

# 1. DISCOVER — one object, several languages

The expressions

\[
\sqrt 8,\qquad 8^{1/2},\qquad \log_2 8=3\iff 2^3=8
\]

belong to one network, not three disconnected chapters.

A difficult expression is often a simple object written in an inconvenient representation. Before calculating, ask:

- What repeats?
- Can several terms be rewritten in one common basis?
- Is there a hidden square, cube, or reciprocal symmetry?
- Is the transformation one-to-one on the domain I am using?
- What conditions must I carry beside the algebra?

## Contrast: same surface family, different first move

Compare:

\[
\sqrt{18}+\sqrt 8
\]

with

\[
\sqrt{21-8\sqrt5}.
\]

Both contain radicals. The first wants a **common radical basis**. The second wants a **hidden-square reconstruction**. A chapter label cannot make this decision for you; the structure must.

---

# 2. RADICALS — basis, hidden powers, and principal roots

## 2.1 Reconnect: extracting perfect powers

For positive numerical radicands,

\[
\sqrt{18}=\sqrt{9\cdot2}=3\sqrt2,
\]

so

\[
\sqrt{18}+\sqrt8-\sqrt2
=3\sqrt2+2\sqrt2-\sqrt2
=4\sqrt2.
\]

### Realization

The visible radicands were \(18,8,2\), but the expression had only one independent radical building block: \(\sqrt2\).

**First question:** can I expose a common irreducible radical basis before combining terms?

## 2.2 Why radicals do not distribute over addition

The multiplication rule comes from multiplication:

\[
\sqrt{9\cdot5}=\sqrt9\sqrt5=3\sqrt5.
\]

There is no corresponding addition law. A single counterexample is enough:

\[
\sqrt{9+16}=5\neq7=\sqrt9+\sqrt{16}.
\]

The misconception is an operation-structure error: a multiplicative property has been extended to addition.

## 2.3 Hidden surds: run the square identity backwards

Expand

\[
(4-\sqrt5)^2=16+5-8\sqrt5=21-8\sqrt5.
\]

Now reverse the direction. Because \(4-\sqrt5>0\),

\[
\sqrt{21-8\sqrt5}=4-\sqrt5.
\]

The recognition mechanism comes directly from

\[
(\sqrt m-\sqrt n)^2=m+n-2\sqrt{mn}.
\]

So for a radicand \(A-B\sqrt d\), test whether you can choose \(m,n>0\) such that

\[
m+n=A,\qquad 2\sqrt{mn}=B\sqrt d.
\]

Do not trust a pattern match until you square the proposed reconstruction.

## 2.4 Principal root: why \(\sqrt{x^2}=|x|\)

The symbol \(\sqrt A\) means the **non-negative** square root of \(A\). Therefore

\[
\sqrt{x^2}=|x|.
\]

For example,

\[
\sqrt{(-3)^2}=3,
\]

not \(-3\).

This is different from solving

\[
u^2=x^2,
\]

where both signs are possible:

\[
u=\pm x.
\]

### Decision boundary

- radical notation \(\sqrt{x^2}\): one non-negative value;
- equation \(u^2=x^2\): potentially two values.

## 2.5 Rationalization is a tactic, not a ritual

For example,

\[
\frac1{\sqrt5+\sqrt2}
=\frac{\sqrt5-\sqrt2}{3}.
\]

This is useful when the denominator is the obstruction. But rationalizing every surd expression by reflex can destroy a simpler symmetry or common-basis structure. Ask what the target wants before choosing the representation.

## TRY A — no hints on this page

A1. Simplify \(\dfrac{\sqrt{98}-\sqrt8}{\sqrt2}\).

A2. Simplify \(\sqrt{13-4\sqrt{10}}\).

A3. Simplify \(\sqrt{(3x+1)^2}\) and state when it equals \(3x+1\).

A4. Simplify

\[
\frac1{\sqrt7+\sqrt2}+\frac1{\sqrt7-\sqrt2}.
\]

A5. Simplify \(\sqrt[3]{16}+\sqrt[3]{54}-\sqrt[3]{2}\).

If blocked, record the item code and use the Hint Bank only after making a genuine first attempt.

---

# 3. EXPONENTS — meaning before manipulation

## 3.1 Rebuild the product law

\[
2^3\cdot2^4
\]

means three factors of 2 followed by four more factors of 2. Hence there are seven factors:

\[
2^3\cdot2^4=2^7.
\]

This explains why exponents add under multiplication of the same base. It does **not** justify

\[
2^3+2^4=2^7.
\]

## 3.2 Negative exponent means reciprocal

For \(a\neq0\),

\[
a^n a^{-n}=a^0=1,
\]

so

\[
a^{-n}=\frac1{a^n}.
\]

A negative exponent does not make the value negative.

Contrast:

\[
2^{-3}=\frac18,
\qquad
(-2)^3=-8.
\]

## 3.3 Fractional exponent is radical language

For suitable real inputs,

\[
a^{1/n}=\sqrt[n]{a},
\qquad
 a^{m/n}=\left(\sqrt[n]{a}\right)^m.
\]

This is a representation switch, not a separate formula family.

## 3.4 Normalize related bases before taking logarithms

Solve

\[
8^x=4^{x+1}.
\]

Rewrite both sides in base 2:

\[
2^{3x}=2^{2x+2}.
\]

Because \(2^t\) is one-to-one,

\[
3x=2x+2,
\]

so \(x=2\).

Taking logarithms would be legal but inferior here. The common base already exposes the algebra.

## 3.5 Repeated exponential object

Consider

\[
9^x-10\cdot3^x+9=0.
\]

The repeated object is \(3^x\). Set

\[
t=3^x,\qquad t>0.
\]

Then

\[
t^2-10t+9=0.
\]

The condition \(t>0\) is part of the substitution. A negative polynomial root would not map back to a real exponential value for a positive base.

## 3.6 Two-base homogeneous equations: divide to expose a ratio

For

\[
9^x-5\cdot6^x+4\cdot4^x=0,
\]

divide by \(4^x>0\):

\[
\left(\frac32\right)^{2x}
-5\left(\frac32\right)^x+4=0.
\]

Now set

\[
t=\left(\frac32\right)^x>0.
\]

Again the surface was exponential, but the hidden object was a quadratic in one positive variable.

## TRY B — no hints on this page

B1. Evaluate \(27^{-2/3}\).

B2. Solve \(16^x=8^{x+1}\).

B3. Solve \(9^x-10\cdot3^x+9=0\).

B4. Solve \(9^x-5\cdot6^x+4\cdot4^x=0\).

B5. Evaluate \(32^{3/5}\,8^{-2/3}\).

---

# 4. REVERSIBILITY — equivalent equation or candidate equation?

This is the logical spine of the unit.

## 4.1 Two arrows, two claims

\[
A\iff B
\]

means the two statements have the same truth conditions on the stated domain.

\[
A\Rightarrow B
\]

means every solution of \(A\) satisfies \(B\), but \(B\) may contain extra candidates.

Example:

\[
x=2\Rightarrow x^2=4,
\]

but the reverse is false because \(x=-2\) also satisfies \(x^2=4\).

## 4.2 Why squaring loses information

Squaring is not one-to-one on the reals:

\[
2^2=(-2)^2.
\]

Cubing is one-to-one:

\[
a^3=b^3\iff a=b\quad\text{for real }a,b.
\]

So the operation itself determines whether information can be lost.

## 4.3 When squaring becomes reversible

Solve

\[
\sqrt{x+1}=x-1.
\]

The right side must be non-negative, so \(x\ge1\). On that restricted domain both sides are non-negative. Therefore

\[
\sqrt{x+1}=x-1
\iff
x+1=(x-1)^2,\qquad x\ge1.
\]

The algebra produces candidates, but the carried condition immediately filters them.

### Condition ledger

Before a risky transformation, write what is known:

- radical arguments \(\ge0\);
- principal-root side \(\ge0\);
- log arguments \(>0\);
- substituted exponential variable \(>0\);
- square-root substitution \(\ge0\);
- divisor \(\neq0\) or a separate zero case.

## 4.4 Division by a variable expression

From

\[
(x-2)(x+3)=0,
\]

dividing by \(x-2\) assumes \(x-2\neq0\) and therefore deletes the case \(x=2\).

The zero-product rule is the safe representation:

\[
x-2=0\quad\text{or}\quad x+3=0.
\]

## TRY C — no hints on this page

C1. Solve \(\sqrt{x+1}=x-1\).

C2. Solve \(\sqrt{2x+3}=3\sqrt{x-1}\), and justify whether squaring is reversible on your domain.

C3. Solve \((x-2)(x+3)=0\) without dividing by either factor.

C4. Classify each step as \(\iff\) or only \(\Rightarrow\):

- \(x=2\) to \(x^2=4\);
- \(a=b\) to \(a^3=b^3\) over the reals;
- valid \(\log_2 x=3\) to \(x=8\).

C5. Solve \(\sqrt{x+4}=2\sqrt{x-5}\).

---

# 5. RECIPROCAL INVARIANTS — preserve symmetry

## 5.1 The symmetry test

If the data contains \(x\) and \(1/x\), ask:

> If I replace \(x\) by \(1/x\), does the target stay the same?

If yes, solving explicitly for \(x\) may be unnecessary.

Suppose

\[
x+\frac1x=5.
\]

Then

\[
\left(x+\frac1x\right)^2
=x^2+2+\frac1{x^2},
\]

so

\[
x^2+\frac1{x^2}=23.
\]

No quadratic formula was needed.

## 5.2 Derive the recurrence

Define

\[
S_n=x^n+x^{-n}.
\]

Then \(S_0=2\) and \(S_1=x+x^{-1}\). Multiply:

\[
S_1S_{n-1}
=(x+x^{-1})(x^{n-1}+x^{-(n-1)}).
\]

The outer terms give \(S_n\), while the two middle terms give \(S_{n-2}\). Hence

\[
\boxed{S_n=S_1S_{n-1}-S_{n-2}}.
\]

The recurrence is not a detached formula; it is a consequence of multiplication and symmetry.

## 5.3 Decision boundary: symmetric data cannot determine every asymmetric target

If

\[
x+\frac1x=4,
\]

then

\[
\left(x-\frac1x\right)^2=16-4=12.
\]

Therefore

\[
x-\frac1x=\pm2\sqrt3.
\]

The original symmetric information does not choose the sign.

## TRY D — no hints on this page

D1. If \(x+x^{-1}=5\), find \(x^3+x^{-3}\).

D2. If \(x+x^{-1}=4\), find \(x^5+x^{-5}\).

D3. If \(x+x^{-1}=4\), determine all possible values of \(x^2-x^{-2}\).

D4. If \(x+x^{-1}=3\), find \(x^6+x^{-6}\) without solving for \(x\).

---

# 6. LOGARITHMS — exponent language reversed

## 6.1 Definition first

The statements

\[
5^3=125
\]

and

\[
\log_5 125=3
\]

say the same thing. In general,

\[
\boxed{\log_b y=z\iff b^z=y},
\]

with

\[
b>0,\qquad b\neq1,\qquad y>0.
\]

The domain restrictions come from the exponential function itself: a positive real base never produces zero or a negative output.

## 6.2 Derive the product law

Let

\[
M=b^p,\qquad N=b^q,
\]

with \(M,N>0\). Then

\[
MN=b^{p+q}.
\]

Translate back into logarithm language:

\[
\log_b(MN)=p+q=\log_bM+\log_bN.
\]

The quotient and power laws arise from exponent subtraction and multiplication in the same way.

### Why there is no log-sum law

There is no exponent law saying that adding two outputs corresponds to adding exponents. Therefore no general identity

\[
\log(a+b)=\log a+\log b
\]

exists.

A quick falsifier in base 10 is

\[
\log(1+9)=1,
\]

while

\[
\log1+\log9=\log9\neq1.
\]

## 6.3 Exact inverse before decimal approximation

Evaluate

\[
25^{\log_5 3}.
\]

Since \(25=5^2\),

\[
25^{\log_5 3}
=5^{2\log_5 3}
=(5^{\log_5 3})^2
=3^2=9.
\]

The structure disappears if you approximate the logarithm too early.

## 6.4 Choose the whole repeated object

For

\[
(\log_2x)^2-5\log_2x+6=0,
\]

set

\[
t=\log_2x.
\]

But for

\[
\log_2x-5\sqrt{\log_2x}+4=0,
\]

the repeated object is better represented by

\[
u=\sqrt{\log_2x},\qquad u\ge0.
\]

Then \(\log_2x=u^2\), and the equation becomes ordinary quadratic algebra in \(u\).

The range \(u\ge0\) is not optional.

## TRY E — no hints on this page

E1. Evaluate \(25^{\log_5 3}\) exactly.

E2. Solve \((\log_2x)^2-5\log_2x+6=0\).

E3. Solve \(\log_2x-5\sqrt{\log_2x}+4=0\).

E4. Give a numerical counterexample to \(\log(a+b)=\log a+\log b\).

E5. Evaluate \(27^{\log_3 2}\) exactly.

E6. Positive \(x,y\) satisfy \(\log_4x=\log_2y\) and \(x-y=6\). Find \(x+y\).

---

# 7. LOG-TO-ALGEBRA — remove the logs, not their domain

## 7.1 Equal valid logs are injective information

For a valid base \(b>0\), \(b\neq1\), the logarithm is one-to-one on positive arguments. Thus, if both sides exist,

\[
\log_b A=\log_b B\iff A=B.
\]

The phrase **if both sides exist** is part of the statement.

## 7.2 Related bases can hide a power relation

If positive \(x,y\) satisfy

\[
\log_4x=\log_2y,
\]

then

\[
\frac12\log_2x=\log_2y,
\]

so

\[
\log_2x=\log_2(y^2),
\]

and therefore

\[
x=y^2.
\]

The logarithmic relation has become ordinary algebra.

## 7.3 Domain survives after the logarithms disappear

Solve

\[
\log_2(x-3)=2\log_2(x-5).
\]

Before using any law,

\[
x>5.
\]

Then

\[
\log_2(x-3)=\log_2((x-5)^2),
\]

so on the valid domain

\[
x-3=(x-5)^2.
\]

The transformed polynomial may produce values outside \(x>5\). Those are algebraic candidates, not original solutions.

## TRY F — no hints on this page

F1. Solve \(\log_2(x-3)=2\log_2(x-5)\).

F2. Solve \(\log_3(x-1)=2\log_3(x-4)\).

F3. Solve \(\log_2(x-1)=\log_2(7-x)\).

F4. Positive \(x,y\) satisfy \(\log_9x=\log_3y\) and \(x-y=20\). Find \(x+y\).

---

# 8. DIAGNOSE — find the first broken bridge

For each student solution below, do **not** simply write the final answer. Identify the first invalid or inferior line, name the missing idea, and repair it.

## Dg1 — operation structure

A student writes

\[
\sqrt{4+9}=\sqrt4+\sqrt9.
\]

Is the step valid? What property has been overextended?

## Dg2 — principal root

A student writes

\[
\sqrt{(x-2)^2}=x-2
\]

for all real \(x\). Find the first missing condition.

## Dg3 — exponent meaning

A student writes

\[
a^{-2}=-a^2.
\]

Repair the meaning before doing any further algebra.

## Dg4 — legal but inferior method

A student begins \(8^x=4^{x+1}\) by taking logarithms. Is the move invalid or merely inefficient? Give the shorter structural move.

## Dg5 — squaring without sign information

A student squares \(\sqrt{x+1}=x-1\) immediately and later accepts every polynomial root. Identify the missing ledger entry.

## Dg6 — zero-sensitive division

A student divides \((x-2)(x+3)=0\) by \(x-2\). Which case disappears?

## Dg7 — solving too much

Given \(x+x^{-1}=5\), a student solves explicitly for \(x\) before finding \(x^3+x^{-3}\). Why is this a poor representation choice?

## Dg8 — domain persistence

A transformed logarithmic equation gives two polynomial roots. One makes an original logarithm argument zero. What must happen to it?

## Dg9 — source integrity

A printed historical key conflicts with independently verified mathematics. What must remain separate in the record?

---

# 9. FADE — support disappears, not merely the label

Every item is attempted at H0 first. The hints are physically separated in the **Hint Bank** after this section. Across each track, the maximum available rescue decreases from H3 to H0.

## Track R — radicals

R1 [max H3] Simplify \(\sqrt{50}+\sqrt8\).

R2 [max H2] Simplify \(\sqrt{21-8\sqrt5}\).

R3 [max H1] Simplify \(\sqrt{(2x-5)^2}\) and state when it equals \(2x-5\).

R4 [H0 only] Simplify \(\sqrt[3]{54}-\sqrt[3]{16}\).

## Track X — exponents

X1 [max H3] Solve \(8^x=4^{x+1}\).

X2 [max H2] Solve \(4^x-10\cdot2^x+16=0\).

X3 [max H1] Solve \(25^x-5\cdot10^x+4\cdot4^x=0\).

X4 [H0 only] Evaluate \(81^{3/4}/\sqrt[3]{27}\).

## Track C — reversibility

C-F1 [max H3] Solve \(\sqrt{x+4}=x-2\).

C-F2 [max H2] Solve \((x-1)(x+4)=0\) without unsafe division.

C-F3 [max H1] Classify \(x=3\to x^2=9\) and \(a=b\leftrightarrow a^3=b^3\) over the reals.

C-F4 [H0 only] Solve \(\sqrt{3x+4}=x\) over the reals.

## Track L — logarithms

L1 [max H3] Solve \((\log_2x)^2-3\log_2x+2=0\).

L2 [max H2] Solve \(\log_2x-5\sqrt{\log_2x}+4=0\).

L3 [max H1] Positive \(x,y\) satisfy \(\log_9x=\log_3y\) and \(x-y=20\). Find \(x+y\).

L4 [H0 only] Solve \(\log_2(x-3)=2\log_2(x-5)\).

---

# 10. HINT BANK — open only after a real attempt

The purpose of a hint is to restart reasoning, not to replace it.

## TRY A

A1 H1: expose one common radical basis. H2: both numerator radicals reduce to multiples of \(\sqrt2\). H3: \(\sqrt{98}=7\sqrt2\), \(\sqrt8=2\sqrt2\).

A2 H1: test a hidden difference of square roots. H2: seek \(m+n=13\), \(mn=40\). H3: use \(m=8,n=5\) and check the principal sign.

A3 H1: principal square root. H2: write an absolute value before removing it.

A4 H1: use conjugates. H2: simplify each denominator to the same rational number before adding.

A5 H1: extract perfect cubes. H2: reduce every term to a multiple of \(\sqrt[3]2\).

## TRY B

B1 H1: negative exponent means reciprocal. H2: evaluate the cube root before squaring.

B2 H1: related bases. H2: use base 2.

B3 H1: one repeated exponential object. H2: set \(t=3^x>0\).

B4 H1: two-base homogeneous pattern. H2: divide by \(4^x>0\).

B5 H1: rewrite both factors in base 2.

## TRY C

C1 H1: the right side must be non-negative. H2: restrict first, then square.

C2 H1: both square-root sides are non-negative on the original domain. H2: write the common domain before squaring.

C3 H1: zero-product rule.

C4 H1: ask whether the operation is one-to-one on the stated domain.

C5 H1: write the original radical domain first. H2: both sides are non-negative there.

## TRY D

D1 H1: define \(S_n=x^n+x^{-n}\). H2: build \(S_2\) before \(S_3\).

D2 H1: recurrence. H2: compute successively from \(S_0=2,S_1=4\).

D3 H1: the target is asymmetric. H2: factor it as \((x-x^{-1})(x+x^{-1})\).

D4 H1: recurrence from \(S_0=2,S_1=3\).

## TRY E/F

E1 H1: rewrite 25 as a power of 5.

E2 H1: set \(t=\log_2x\).

E3 H1: name the outer repeated object. H2: set \(u=\sqrt{\log_2x}\ge0\).

E4 H1: test small positive numbers in base 10.

E5 H1: rewrite 27 as \(3^3\).

E6 H1: convert \(\log_4x\) to base 2.

F1/F2 H1: write the log domain before combining logs. H2: use the power law and then injectivity.

F3 H1: first require \(x-1>0\) and \(7-x>0\).

F4 H1: rewrite \(\log_9x\) in base 3.

## Fading-track rescue

R1 H3: \(\sqrt{50}=5\sqrt2\), \(\sqrt8=2\sqrt2\).

R2 H2: test a hidden binomial square.

R3 H1: principal root.

X1 H3: \(2^{3x}=2^{2x+2}\).

X2 H2: set \(t=2^x>0\).

X3 H1: divide by a positive base-power to create a ratio variable.

C-F1 H3: write \(x\ge2\), then \(x+4=(x-2)^2\).

C-F2 H2: split the zero-product cases.

C-F3 H1: one-to-one transformation test.

L1 H3: set \(t=\log_2x\), then solve \(t^2-3t+2=0\).

L2 H2: set \(u=\sqrt{\log_2x}\ge0\).

L3 H1: convert the base-9 logarithm to base 3.

---

# 11. ADOPT — mixed and unlabelled

For each item, write four things before looking at any key:

1. the visible clue;
2. the first useful move;
3. the exact solution or conclusion;
4. one tempting alternative and why you rejected it.

M1. Simplify \((\sqrt{72}-\sqrt8)/\sqrt2\).

M2. Simplify \(\sqrt{17-4\sqrt{15}}\).

M3. Evaluate \(64^{-2/3}\).

M4. Solve \(32^x=8^{x+1}\).

M5. Solve \(16^x-10\cdot4^x+9=0\).

M6. If \(t+t^{-1}=5\), find \(t^4+t^{-4}\).

M7. Solve \(\sqrt{x+5}=x-1\).

M8. Solve \((\log_3x)^2-4\log_3x+3=0\).

M9. Solve \(\log_2x-3\sqrt{\log_2x}+2=0\).

M10. Positive \(x,y\) satisfy \(\log_4x=\log_2y\) and \(x-y=2\). Find \(x+y\).

M11. Evaluate \(16^{\log_2 3}\) exactly.

M12. A printed key accepts a value that makes an original logarithm argument non-positive. State the correct mathematical and source-custody action.

---

# 12. TRANSFER — new surface, same underlying structure

These problems deliberately combine or disguise mechanisms. Do not treat them as number swaps.

T1. Simplify

\[
\sqrt{2+\sqrt3}+\sqrt{2-\sqrt3}.
\]

T2. Simplify

\[
\sqrt{5+2\sqrt6}-\sqrt{5-2\sqrt6}.
\]

T3. Solve

\[
49^x-8\cdot21^x+7\cdot9^x=0.
\]

T4. If

\[
x-\frac1x=3,
\]

find \(x^4+x^{-4}\) without solving for \(x\).

T5. If \(a>0\), \(a\neq1\), and

\[
a^x+a^{-x}=3,
\]

find \(a^{3x}+a^{-3x}\).

T6. Solve over the reals

\[
\sqrt{x+10}=|x-2|.
\]

Explain why squaring is reversible after the original domain is written.

T7. Solve

\[
\frac{(x-1)(x+2)}{x-1}=3.
\]

Do not forget the original domain.

T8. Positive \(x,y\) satisfy

\[
\log_8x=\log_2y,
\qquad x-y=6.
\]

Find \(x+y\).

T9. Evaluate \(81^{\log_3 2}\) exactly.

T10. Solve

\[
\log_2(x+1)=\log_4((x-1)^2).
\]

Keep every original domain restriction and handle the absolute-value structure created by the square.

T11. Solve

\[
\log_5x+2\sqrt{\log_5x}-3=0.
\]

T12. A source prints a real cube-root equation, but a provisional key treats repeated transformed roots as if squaring had occurred. Explain the two independent checks needed before accepting or rejecting the key.

---

# 13. ADOPTION CHECK — can you explain your method?

For each major mechanism, you should be able to answer:

1. What did I notice?
2. Why does the first move work?
3. Which condition must survive?
4. Which similar-looking problem would require a different move?
5. Can I write the first two useful lines without a hint?
6. Can I solve a disguised version?

A correct answer reached by an automatic or inappropriate method is not full adoption. The goal is reliable representation choice.

---

# 14. Source note

Historical NMTC IDs are used only to ground mechanisms; full third-party problem statements are not reproduced here.

Clean scored mechanism anchors retained for this topic include:

`NMTC-BH-P-2018-Q01`, `NMTC-BH-P-2018-Q21`, `NMTC-BH-P-2018-Q26`, `NMTC-BH-P-2023-Q07`, `NMTC-BH-P-2023-Q21`, `NMTC-BH-P-2023-Q26`, `NMTC-BH-P-2024-Q04`, `NMTC-BH-P-2024-Q09`, `NMTC-BH-P-2024-Q12`, `NMTC-BH-P-2024-Q26`, `NMTC-BH-P-2024-Q28`, `NMTC-BH-P-2025-Q03`, `NMTC-BH-P-2025-Q04`, `NMTC-BH-P-2025-Q09`, `NMTC-BH-P-2025-Q12`, `NMTC-BH-P-2025-Q27`.

`NMTC-BH-P-2023-Q04` and `NMTC-BH-P-2023-Q20` remain source-sensitive bridge evidence only. `NMTC-BH-P-2025-Q18` remains source-conflict/QC evidence only. No topic-specific bonus recurrence is inferred.

All unlabelled practice, fading, ADOPT, and TRANSFER prompts in this v3 book are author-created.