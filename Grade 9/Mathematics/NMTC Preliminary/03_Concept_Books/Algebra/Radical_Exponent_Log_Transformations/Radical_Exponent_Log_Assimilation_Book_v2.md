# Radicals, Exponents & Logarithmic Transformations — Assimilation Book v2

`ISSUE_AUTHORITY: #45`

`WAVE: 2 — INTEGRATED_ASSIMILATION_BOOK`

`STATUS: INTERNAL_ASSIMILATION_COMPLETE`

Target learner: Grade IX/X student with partial prior knowledge. You probably remember some exponent laws, routine surd simplification and basic logarithm rules. The missing skill is usually not another formula. It is deciding **what representation makes the mathematics smaller**, whether that change is reversible, and which conditions must survive it.

This book is the teaching layer. The First-Step Reference is deliberately **not** included here; it belongs to Wave 3 after assimilation.

---

# 0. The operating idea

A difficult-looking expression may be a small algebraic object written in an inconvenient language.

Use this loop:

```text
RECONNECT
   -> DISCOVER the useful representation
   -> MAKE SENSE of why it works
   -> TRY before hints
   -> DIAGNOSE the actual gap
   -> FADE H3 -> H2 -> H1 -> H0
   -> ADOPT the first move
   -> TRANSFER without chapter labels
```

And during every transformation ask:

```text
Did I make an equivalent statement?       <=>
Or did I only generate candidates?         =>
What domain / sign / non-zero condition must survive?
```

The central habit is:

> **Transform before calculating, but audit the transformation.**

---

# 1. RECONNECT — what do you already own?

Attempt these without notes. Do not treat this as a score. Each miss identifies a bridge to repair.

1. Simplify `sqrt(72)`.
2. Evaluate `16^(-3/4)`.
3. Simplify `sqrt((x-4)^2)` for real `x`.
4. Solve `4^x=8`.
5. Rewrite `log_3 81=4` in exponential form.
6. State the real domain of `log_2(x-5)`.
7. If `t+1/t=4`, find `t^2+1/t^2`.
8. Is squaring both sides of a real equation always reversible?
9. Is `log(a+b)=log a+log b` a logarithm law?
10. If `u=sqrt(log_2 x)`, what restriction must be written beside `u`?

## Reconnect check

1. `6sqrt(2)`.
2. `1/8`.
3. `|x-4|`.
4. `x=3/2`.
5. `3^4=81`.
6. `x>5`.
7. `14`.
8. No. Squaring is not one-to-one on the reals.
9. No.
10. `u>=0` (and the original log requires `x>0`).

## Diagnose, do not label yourself

- misses 1–3 -> radical representation / principal-root bridge;
- misses 2 or 4 -> exponent meaning / base-normalization bridge;
- misses 5, 6 or 9 -> logarithm-as-exponent / domain bridge;
- miss 7 -> reciprocal-invariant recognition bridge;
- misses 8 or 10 -> reversibility / condition-ledger bridge.

---

# 2. DISCOVER — one object can speak several languages

Consider these three statements:

```text
sqrt(8) = 2sqrt(2)
8^(1/2) = 2sqrt(2)
log_2 8 = 3  <=>  2^3 = 8
```

They are not three unrelated chapters. They are examples of **representation switching**.

A strong solver asks:

1. What object repeats?
2. Can different-looking terms be put into one common language?
3. Is there a hidden square, cube, reciprocal pair or repeated power?
4. Does the transformation preserve the exact solution set?
5. What conditions must be carried forward?

This is the bridge that joins the whole unit.

---

# 3. Radical language — make the basis visible

## 3.1 SEE

Simplify:

`sqrt(18)+sqrt(8)-sqrt(2)`.

Before calculating term by term, rewrite every radical using the same irreducible building block:

`sqrt(18)=3sqrt(2)` and `sqrt(8)=2sqrt(2)`.

So the expression becomes:

`3sqrt(2)+2sqrt(2)-sqrt(2)=4sqrt(2)`.

## 3.2 REALIZE

The visible radicands were 18, 8 and 2, but the structural basis was only `sqrt(2)`.

The first move is therefore not “apply a radical formula.” It is:

> **extract perfect powers until the independent radical basis is visible.**

This same idea works with cube roots and nth roots.

## 3.3 MAKE SENSE

For positive numerical examples,

`sqrt(18)=sqrt(9*2)=3sqrt(2)`.

For variables, sign matters. The full real statement is:

`sqrt(m^2)=|m|`,

not automatically `m`.

That absolute value is not decoration. The radical symbol denotes the **non-negative principal square root**.

### Contrast pair A — product versus sum

A valid product split under suitable real conditions:

`sqrt(9*5)=sqrt(9)sqrt(5)=3sqrt(5)`.

But:

`sqrt(9+16)=5`, while `sqrt(9)+sqrt(16)=7`.

So there is no general rule `sqrt(a+b)=sqrt(a)+sqrt(b)`.

### Why the false rule feels plausible

Students often overextend a true multiplicative property into an additive one. The repair is not “remember the exception”; it is to track the operation structure.

## 3.4 TRY — H0 first

Without a hint, simplify:

`(sqrt(98)-sqrt(8))/sqrt(2)`.

Write only the first useful line before finishing.

### Rescue ladder — reveal only if needed

- `H1 RECOGNITION`: all three radicals contain the same residual radical.
- `H2 STRUCTURE`: reduce each term to a multiple of `sqrt(2)`.
- `H3 EXECUTION`: `sqrt(98)=7sqrt(2)` and `sqrt(8)=2sqrt(2)`.

**Check:** result `5`.

## 3.5 Source mechanism custody

Clean historical mechanisms supporting common-basis work include `NMTC-BH-P-2018-Q01`, `NMTC-BH-P-2023-Q26` and `NMTC-BH-P-2025-Q03`. They ground the mechanism; their full third-party statements are not reproduced here.

---

# 4. Hidden surds — run an identity backwards

## 4.1 SEE

Expand:

`(4-sqrt(5))^2=16+5-8sqrt(5)=21-8sqrt(5)`.

Now reverse the direction:

`sqrt(21-8sqrt(5))` is not inviting you to approximate. It is inviting you to **recognize a hidden square**.

Since `4-sqrt(5)>0`,

`sqrt(21-8sqrt(5))=4-sqrt(5)`.

## 4.2 REALIZE

When you see `A±Bsqrt(d)`, especially inside a square root or fractional power, test whether it was engineered from a binomial square.

For

`A±Bsqrt(d)=(sqrt(m)±sqrt(n))^2`,

you want:

`m+n=A`,

`2sqrt(mn)=Bsqrt(d)`.

The point is not to memorize those two lines. They come directly from expanding the square.

## 4.3 Decision boundary — common basis or hidden square?

Compare:

- `sqrt(18)+sqrt(8)` -> common radical basis;
- `sqrt(21-8sqrt(5))` -> reverse-square reconstruction.

Both contain radicals, but the structural cue is different.

## 4.4 Rationalize only when it helps

Rationalization is legal and useful in many denominators, but it is not a compulsory ceremony.

For example:

`1/(sqrt(5)+sqrt(2)) = (sqrt(5)-sqrt(2))/3`.

But if a whole expression is already symmetric in a number and its reciprocal, rationalizing each piece separately may hide the invariant. Ask what structure the target wants before choosing the tool.

## 4.5 TRY — H0 first

Simplify:

`sqrt(13-4sqrt(10))`.

- `H1`: test a difference of two square roots.
- `H2`: seek `m+n=13` and `mn=40`.
- `H3`: use `m=8`, `n=5` and check which difference is positive.

**Check:** `2sqrt(2)-sqrt(5)`.

## 4.6 Principal-root boundary

`sqrt((3x+1)^2)=|3x+1|`.

It equals `3x+1` only when `x>=-1/3`.

This is different from solving

`u^2=(3x+1)^2`,

where `u=±(3x+1)`.

### Source mechanism custody

Clean mechanisms: `NMTC-BH-P-2023-Q21`, `NMTC-BH-P-2024-Q26`, `NMTC-BH-P-2025-Q04`. `NMTC-BH-P-2023-Q04` remains source-sensitive bridge evidence only.

---

# 5. Exponents — meaning before law

## 5.1 RECONNECT

`2^3*2^4` means three factors of 2 multiplied by four more factors of 2. There are seven factors in total, so:

`2^3*2^4=2^7`.

That is why multiplication of like bases adds exponents.

It does **not** imply:

`2^3+2^4=2^7`.

Indeed, `8+16=24`, not 128.

## 5.2 Negative exponent means reciprocal

For non-zero `a`,

`a^n*a^(-n)=a^0=1`.

So:

`a^(-n)=1/a^n`.

A negative exponent does not mean a negative value.

Example:

`27^(-2/3)=1/(27^(2/3))=1/9`.

### Contrast pair B — negative exponent versus negative base

`2^(-3)=1/8`,

while

`(-2)^3=-8`.

The first changes multiplication into a reciprocal. The second changes the sign of the base.

## 5.3 Fractional exponent is radical language

For suitable real inputs,

`a^(1/n)` is an nth root representation, and `a^(m/n)` links repeated powers with nth roots.

This is why radical and exponent work belong in the same transformation network.

---

# 6. Exponential equations — normalize before taking logs

## 6.1 SEE

Solve:

`8^x=4^(x+1)`.

Rewrite both sides in base 2:

`2^(3x)=2^(2x+2)`.

Since `2^u` is one-to-one on the reals,

`3x=2x+2`, so `x=2`.

No logarithm was needed.

## 6.2 REALIZE

The question was not “which exponential formula?” It was “can the bases speak a common language?”

### Contrast pair C — normalization versus unnecessary logs

For `8^x=4^(x+1)`, taking logarithms works, but common-base normalization is shorter and preserves the exact structure.

When bases are not related cleanly, logarithms may become useful later. Method choice depends on structure, not chapter label.

## 6.3 Repeated power substitution

Solve:

`9^x-10*3^x+9=0`.

The repeated object is `3^x`. Let:

`t=3^x`, with the essential condition `t>0`.

Then:

`t^2-10t+9=0`,

so `t=1` or `9`.

Thus:

`x=0` or `2`.

The positivity note matters in harder problems because a transformed polynomial can have negative roots that cannot equal `a^x` for positive base `a`.

## 6.4 Two bases — use a ratio variable

Consider:

`9^x-5*6^x+4*4^x=0`.

Divide by `4^x>0`:

`(3/2)^(2x)-5(3/2)^x+4=0`.

Let `t=(3/2)^x>0`:

`t^2-5t+4=0`.

So `t=1` or `4`, giving:

`x=0` or `x=log_(3/2)4`.

## 6.5 TRY — H0 first

Solve:

`16^x=8^(x+1)`.

- `H1`: related bases.
- `H2`: rewrite both in base 2.
- `H3`: `2^(4x)=2^(3x+3)`.

**Check:** `x=3`.

### Source mechanism custody

Clean mechanisms: `NMTC-BH-P-2023-Q07`, `NMTC-BH-P-2024-Q04`, `NMTC-BH-P-2024-Q09`. `NMTC-BH-P-2023-Q20` remains source-sensitive bridge evidence only.

---

# 7. CHECKPOINT — equivalent equation or candidate equation?

This is the unit's most important logical bridge.

## 7.1 What `<=>` means

`A <=> B` means each statement implies the other on the stated domain. The solution set is preserved exactly.

Example:

For `x>0`,

`log_2 x=3 <=> x=8`.

The exponential/logarithmic conversion is reversible on the valid domain.

## 7.2 What `=>` means

`A => B` means every solution of A satisfies B, but B may contain extra candidates.

Example:

`x=2 => x^2=4`.

But `x^2=4` also has `x=-2`. Squaring lost sign information.

## 7.3 Squaring versus cubing

Squaring is not one-to-one over the reals:

`2^2=(-2)^2`.

Cubing is one-to-one over the reals:

if `a^3=b^3`, then `a=b`.

So cubing a real equality is reversible; squaring generally is not unless sign conditions make it so.

### Contrast pair D — same-looking transform, different reversibility

- square both sides: usually candidate-generating;
- cube both sides over the reals: reversible.

## 7.4 Isolate before you square

Solve:

`sqrt(x+1)=x-1`.

Before squaring, the right side must be non-negative, so `x>=1`.

On this restricted domain both sides are non-negative, so the squaring step is reversible:

`sqrt(x+1)=x-1 <=> x+1=(x-1)^2`, with `x>=1`.

The algebra gives candidates `x=0,3`; the carried domain leaves `x=3`.

The original check confirms it.

## 7.5 Multiplying or dividing by something that may be zero

From:

`(x-2)(x+3)=0`,

if you divide by `x-2`, you lose the valid solution `x=2`.

The safe first move is to split the zero-product cases:

`x-2=0` or `x+3=0`.

### Contrast pair E — constant versus variable factor

Dividing by a known non-zero constant preserves equivalence.

Dividing by `g(x)` requires a separate `g(x)=0` case unless non-zero status is already established.

## 7.6 Arrow lab — TRY before reading the check

Classify each transformation as `<=>` or only `=>` under the conditions shown.

1. `x=2` to `x^2=4`.
2. `x>0, log_2 x=3` to `x=8`.
3. `a=b` to `a^3=b^3` for real `a,b`.
4. `x-1=0` to `x(x-1)=0`.
5. `x>=1, sqrt(x+1)=x-1` to `x+1=(x-1)^2`.

**Check:** `=>, <=>, <=>, =>, <=>`.

---

# 8. Reciprocal invariants — do not solve what the target does not ask for

## 8.1 SEE

Suppose:

`x+1/x=5`, with `x!=0`.

If the target is `x^3+1/x^3`, solving the quadratic for `x` creates unnecessary radicals.

Instead:

`(x+1/x)^2=x^2+2+1/x^2`,

so:

`x^2+1/x^2=25-2=23`.

Then:

`x^3+1/x^3=(x+1/x)(x^2+1/x^2)-(x+1/x)`

`=5*23-5=110`.

## 8.2 MAKE SENSE — recurrence

Let:

`S_n=x^n+x^(-n)`.

Then:

`S_0=2`, `S_1=x+1/x`.

Multiplying `S_(n-1)` by `S_1` creates `S_n` plus the two middle terms that form `S_(n-2)`. Therefore:

`S_n=S_1*S_(n-1)-S_(n-2)`.

This is a rewriting machine, not a new formula to memorize blindly.

## 8.3 TRY — H0 first

If `x+1/x=4`, find `x^4+1/x^4`.

- `H1`: build symmetric power sums, not `x`.
- `H2`: first find `S_2` and `S_3`.
- `H3`: `S_2=4^2-2=14`, `S_3=4*14-4=52`.

**Check:** `S_4=4*52-14=194`.

## 8.4 Decision boundary — symmetric versus asymmetric target

If `x+1/x=4`, can you determine `x-1/x` uniquely?

Square it:

`(x-1/x)^2=(x+1/x)^2-4=12`.

So:

`x-1/x=±2sqrt(3)`.

The symmetric information does **not** choose the sign. This is the boundary:

- symmetric target -> invariant may determine it uniquely;
- asymmetric target -> additional branch/sign information may be required.

### Source mechanism custody

Clean mechanisms: `NMTC-BH-P-2018-Q21` and `NMTC-BH-P-2025-Q09`.

---

# 9. Logarithms — exponent language reversed

## 9.1 SEE

`5^3=125`.

Ask: to what power must 5 be raised to get 125?

The answer is 3, so:

`log_5 125=3`.

These are the same mathematical statement:

`log_b x=y <=> b^y=x`,

provided:

`b>0`, `b!=1`, `x>0`.

## 9.2 Why the domain is structural

For a valid positive base, `b^y` is always positive. Therefore a real logarithm cannot have zero or a negative argument.

The domain is not an end-of-solution checklist. It is part of the meaning of the notation.

## 9.3 Derive the product law instead of memorizing it

Let:

`M=b^p`, `N=b^q`, with positive `M,N`.

Then:

`MN=b^(p+q)`.

Taking the exponent description back into log notation gives:

`log_b(MN)=p+q=log_b M+log_b N`.

The quotient and power laws follow from exponent subtraction and multiplication in the same way.

### Contrast pair F — product versus sum

The product law exists because multiplying like bases adds exponents.

There is no analogous exponent law behind `M+N`. Hence no general rule:

`log(M+N)=log M+log N`.

A numerical falsifier in base 10:

`log(1+9)=1`, but `log 1+log 9=log 9`, not 1.

## 9.4 Exact inverse before decimals

Evaluate:

`25^(log_5 3)`.

Rewrite `25=5^2`:

`25^(log_5 3)=5^(2log_5 3)=(5^(log_5 3))^2=3^2=9`.

No approximation was needed.

### Source mechanism custody

`NMTC-BH-P-2024-Q28` is a clean exact log-exponent mechanism anchor. The basic definition and law derivations are `AUTHOR_CREATED_FOUNDATION` because historical items usually assume them.

---

# 10. Choose the whole repeated logarithmic object

## 10.1 Direct repeated log

Solve:

`(log_2 x)^2-5log_2 x+6=0`.

Let:

`t=log_2 x`.

Then:

`t^2-5t+6=0`, so `t=2,3`.

Map back:

`x=4,8`.

The original logarithm already imposes `x>0`, and both values satisfy it.

## 10.2 The outer repeated object is sometimes better

Now solve:

`log_2 x-5sqrt(log_2 x)+4=0`.

If you choose `t=log_2 x`, you still carry `sqrt(t)`.

Instead choose:

`u=sqrt(log_2 x)`, with `u>=0`.

Then:

`log_2 x=u^2`, and the equation becomes:

`u^2-5u+4=0`.

So `u=1,4`.

Therefore:

`log_2 x=1,16`,

and:

`x=2,65536`.

### Contrast pair G — inner object versus repeated object

- repeated `(log_b x)` -> `t=log_b x`;
- repeated `sqrt(log_b x)` -> naming the square-rooted log itself often gives smaller algebra.

Carry the range of the substitution: `u>=0`.

## 10.3 TRY — H0 first

Solve:

`log_3 x-4sqrt(log_3 x)+3=0`.

- `H1`: what entire object repeats?
- `H2`: set `u=sqrt(log_3 x)>=0`.
- `H3`: solve `u^2-4u+3=0`.

**Check:** `x=3` or `19683`.

Clean mechanism anchors include `NMTC-BH-P-2024-Q12` and `NMTC-BH-P-2025-Q12`.

---

# 11. Log-to-algebra conversion — remove the logs but keep their domain

## 11.1 SEE

Suppose positive `x,y` satisfy:

`log_4 x=log_2 y`.

Since:

`log_4 x=(1/2)log_2 x`,

we have:

`(1/2)log_2 x=log_2 y`.

Thus:

`log_2 x=log_2(y^2)`.

With positive arguments and a valid base:

`x=y^2`.

The logarithmic relation has become ordinary algebra.

## 11.2 Add a second relation

If also:

`x-y=6`,

then:

`y^2-y=6`,

so:

`(y-3)(y+2)=0`.

The algebra offers `y=3,-2`, but the original logarithm requires `y>0`. Therefore:

`y=3`, `x=9`, and `x+y=12`.

The negative branch is not “almost right.” It never belonged to the original log domain.

## 11.3 Domain filtering after logs disappear

Solve:

`log_2(x-3)=2log_2(x-5)`.

Original domain:

`x>5`.

Use the power law:

`log_2(x-3)=log_2((x-5)^2)`.

On the valid domain, injectivity gives:

`x-3=(x-5)^2`.

So:

`x^2-11x+28=0`,

with algebraic roots `4,7`.

The original domain rejects 4. Thus:

`x=7`.

### Contrast pair H — algebraic root versus original solution

Once logarithms disappear, their domain does **not** disappear. Carry it beside the transformed algebra.

Clean mechanism anchor: `NMTC-BH-P-2025-Q27`.

---

# 12. DIAGNOSE — Error Laboratory

Do not merely correct each line. Identify the missing bridge.

## Error 1

Student writes:

`sqrt(4+9)=sqrt(4)+sqrt(9)`.

**Diagnosis:** operation-structure gap.

**Repair:** product behavior does not extend to addition.

## Error 2

Student writes:

`sqrt((x-2)^2)=x-2` for every real `x`.

**Diagnosis:** principal-root sign gap.

**Repair:** `sqrt((x-2)^2)=|x-2|`; remove the absolute value only with a sign condition.

## Error 3

Student writes:

`a^(-2)=-a^2`.

**Diagnosis:** reciprocal/inverse gap.

**Repair:** `a^(-2)=1/a^2` for `a!=0`.

## Error 4

Student takes logarithms immediately in `8^x=4^(x+1)`.

**Diagnosis:** representation-choice gap.

**Repair:** logs are legal but inferior here; normalize to base 2 first.

## Error 5

Student squares `sqrt(x+1)=x-1` before noticing that the right side must be non-negative.

**Diagnosis:** condition-ledger/reversibility gap.

**Repair:** write domain/sign first; then decide whether squaring is equivalent on that restricted domain.

## Error 6

Student divides `(x-2)(x+3)=0` by `x-2`.

**Diagnosis:** zero-case gap.

**Repair:** split the zero-product cases; dividing by a factor that can vanish can lose a solution.

## Error 7

Student solves explicitly for `x` when `x+1/x=5` and only `x^3+1/x^3` is requested.

**Diagnosis:** invariant-recognition gap.

**Repair:** preserve symmetry and generate the target from `S_1`.

## Error 8

Student writes `log(a+b)=log a+log b`.

**Diagnosis:** false analogy / log-meaning gap.

**Repair:** rebuild the true product law from exponent multiplication and use a counterexample for sums.

## Error 9

Student solves a transformed log equation and accepts a value making an original argument non-positive.

**Diagnosis:** domain-persistence gap.

**Repair:** original logarithmic domain remains authoritative after transformation.

## Error 10

Student defines `u=sqrt(log_b x)` but later accepts `u=-3`.

**Diagnosis:** substitution-range gap.

**Repair:** write `u>=0` at the definition.

## Error 11 — source integrity

A historical key conflicts with independently verified mathematics.

**Diagnosis:** source-custody issue, not necessarily learner algebra.

**Repair:** keep three records separate:

1. printed source;
2. independent derivation;
3. key/scoring disposition.

Do not silently edit the problem to force agreement.

`NMTC-BH-P-2025-Q18` remains source-conflict evidence for this purpose only.

---

# 13. FADE — support must genuinely disappear

Every item below begins with an H0 attempt. If rescue is needed, reveal only the minimum level. Across each row, maximum available support fades from H3 to H0.

## 13.1 Radical / surd fading

### R-F1 — max H3

Simplify `sqrt(50)+sqrt(8)`.

If needed: `H3` gives `sqrt(50)=5sqrt(2)`, `sqrt(8)=2sqrt(2)`.

**Check:** `7sqrt(2)`.

### R-F2 — max H2

Simplify `sqrt(21-8sqrt(5))`.

If needed: `H2` says “test a hidden binomial square.”

**Check:** `4-sqrt(5)`.

### R-F3 — max H1

Simplify `sqrt((2x-5)^2)` and state when it equals `2x-5`.

If needed: `H1` says “principal root.”

**Check:** `|2x-5|`; equals `2x-5` iff `x>=5/2`.

### R-F4 — H0 only

Simplify exactly:

`1/(sqrt(7)+sqrt(2)) + 1/(sqrt(7)-sqrt(2))`.

**Check:** `2sqrt(7)/5`.

## 13.2 Exponent fading

### E-F1 — max H3

Solve `8^x=4^(x+1)`.

**Check:** `x=2`.

### E-F2 — max H2

Solve `9^x-10*3^x+9=0`.

**Check:** `x=0,2`.

### E-F3 — max H1

Solve `9^x-5*6^x+4*4^x=0`.

**Check:** `x=0` or `log_(3/2)4`.

### E-F4 — H0 only

Evaluate `32^(3/5)*8^(-2/3)`.

**Check:** `2`.

## 13.3 Reversibility fading

### C-F1 — max H3

Solve `sqrt(x+4)=x-2`.

**Check:** `x=5`.

### C-F2 — max H2

Solve `(x-1)(x+4)=0` without dividing by either factor.

**Check:** `x=1,-4`.

### C-F3 — max H1

Classify: `x=3 -> x^2=9`; `a=b <=> a^3=b^3` over the reals.

**Check:** first is only `=>`; second is `<=>`.

### C-F4 — H0 only

Solve `sqrt(2x+3)=3sqrt(x-1)` and justify the transformation.

**Check:** domain `x>=1`; squaring is equivalent there; `x=12/7`.

## 13.4 Logarithm fading

### L-F1 — max H3

Solve `(log_2 x)^2-3log_2 x+2=0`.

**Check:** `x=2,4`.

### L-F2 — max H2

Solve `log_2 x-5sqrt(log_2 x)+4=0`.

**Check:** `x=2,65536`.

### L-F3 — max H1

Positive `x,y` satisfy `log_9 x=log_3 y` and `x-y=20`. Find `x+y`.

**Check:** `30`.

### L-F4 — H0 only

Solve `log_2(x-3)=2log_2(x-5)`.

**Check:** `x=7`.

---

# 14. ADOPT — mixed, unlabelled, first move before solution

Do not write a chapter name. For each item, write the first useful mathematical line or decision before finishing.

1. Simplify `(sqrt(72)-sqrt(8))/sqrt(2)`.
2. Simplify `sqrt(21-8sqrt(5))`.
3. Evaluate `27^(-2/3)`.
4. Solve `16^x=8^(x+1)`.
5. Solve `9^x-10*3^x+9=0`.
6. If `t+1/t=4`, find `t^4+1/t^4`.
7. Solve `sqrt(x+4)=x-2` over the reals.
8. Solve `(log_2 x)^2-5log_2 x+6=0`.
9. Solve `log_3 x-4sqrt(log_3 x)+3=0`.
10. Positive `x,y` satisfy `log_9 x=log_3 y` and `x-y=20`. Find `x+y`.
11. Evaluate exactly `25^(log_5 2)`.
12. Solve `(x-1)(x+4)=0` without using a division that can lose a case.
13. Solve `log_2(x-3)=2log_2(x-5)`.
14. A printed historical key accepts a transformed candidate that violates the original domain. State the correct source-QC action.

## ADOPT self-check

1. `4`.
2. `4-sqrt(5)`.
3. `1/9`.
4. `x=3`.
5. `x=0,2`.
6. `194`.
7. `x=5`.
8. `x=4,8`.
9. `x=3,19683`.
10. `30`.
11. `4`.
12. `x=1,-4`.
13. `x=7`.
14. Recompute from the printed mathematics, preserve the original domain, record the disagreement and classify the source/key conflict; do not silently repair the source.

A correct final answer with the wrong first move is not full adoption. The target is independent method selection.

---

# 15. TRANSFER — change the surface, preserve the structure

These are not merely number swaps.

## T1 — radical/exponent bridge

Evaluate exactly:

`(81)^(3/4) / cuberoot(27)`.

**Check:** `9`.

Mechanism: translate two surface forms into powers before calculating.

## T2 — hidden structure versus routine rationalization

Simplify `sqrt(28-12sqrt(5))`.

**Check:** `3-sqrt(5)` because `(3-sqrt(5))^2=14-6sqrt(5)` is **not** the radicand; therefore this tempting reconstruction is wrong. Recompute instead: seek `m+n=28`, `2sqrt(mn)=12sqrt(5)`, so `mn=180`; `m,n=18,10`; answer `sqrt(18)-sqrt(10)=3sqrt(2)-sqrt(10)`.

This item is deliberately a near-miss: it tests whether you verify a proposed reconstruction rather than pattern-match carelessly.

## T3 — exponent ratio disguise

Solve:

`25^x-5*10^x+4*4^x=0`.

Divide by `4^x>0` and set `t=(5/2)^x`:

`t^2-5t+4=0`.

**Check:** `x=0` or `x=log_(5/2)4`.

## T4 — symmetric information, asymmetric target

If `x+1/x=6`, determine all possible values of `x-1/x`.

**Check:** `±4sqrt(2)`.

The invariant does not select the sign.

## T5 — exact inverse under a disguised base

Evaluate:

`27^(log_3 2)`.

**Check:** `8`.

## T6 — domain survives algebra

Solve:

`log_3(x-1)=2log_3(x-4)`.

Domain `x>4`; algebra gives `x-1=(x-4)^2`, hence `x^2-9x+17=0`.

**Check:** `x=(9+sqrt(13))/2` only, because `(9-sqrt(13))/2<4` and violates the original domain.

---

# 16. Method-choice summary — say it in your own words

A concept is not assimilated until you can answer all six questions for each major mechanism:

1. What did I notice?
2. Why does the method work?
3. What clue should trigger it?
4. What similar-looking situation needs another method?
5. Can I write the first two useful lines without help?
6. Can I solve a disguised version?

Useful internal rules to adopt:

- **Several radicals:** reduce to a common basis before combining.
- **Engineered surd:** test reverse square/cube structure before expansion.
- **Principal square root:** think non-negative value, hence absolute value when a square hides a sign.
- **Related exponential bases:** normalize before taking logs.
- **Repeated power:** name it once and record its positivity.
- **Risky transformation:** label `<=>` or `=>` and carry domain/non-zero conditions.
- **Reciprocal symmetric target:** reduce the invariant before solving the hidden variable.
- **Logarithm:** translate to exponent language when meaning or laws are uncertain.
- **Repeated log structure:** substitute the whole repeated object and carry its range.
- **Logs converted to algebra:** keep the original log domain beside the algebra.
- **Exact log/exponent pair:** simplify structurally before decimals.
- **Source disagreement:** mathematics and provenance are audited separately; never force the key.

---

# 17. Source-custody map for this teaching layer

## Clean scored mechanism anchors

`NMTC-BH-P-2018-Q01`, `NMTC-BH-P-2018-Q21`, `NMTC-BH-P-2018-Q26`, `NMTC-BH-P-2023-Q07`, `NMTC-BH-P-2023-Q21`, `NMTC-BH-P-2023-Q26`, `NMTC-BH-P-2024-Q04`, `NMTC-BH-P-2024-Q09`, `NMTC-BH-P-2024-Q12`, `NMTC-BH-P-2024-Q26`, `NMTC-BH-P-2024-Q28`, `NMTC-BH-P-2025-Q03`, `NMTC-BH-P-2025-Q04`, `NMTC-BH-P-2025-Q09`, `NMTC-BH-P-2025-Q12`, `NMTC-BH-P-2025-Q27`.

These ground mechanisms only; full third-party statements are not reproduced.

## Source-sensitive bridge evidence

- `NMTC-BH-P-2023-Q04` — cube-root identity mechanism; notation/options remain sensitive.
- `NMTC-BH-P-2023-Q20` — exponent/radical linearization; exact notation remains delicate.

They do not become clean anchors by reuse.

## Source-conflict evidence

- `NMTC-BH-P-2025-Q18` — printed real equation versus provisional-key root/multiplicity convention conflict. It remains a source-QC case, not a canonical exercise.

## Bonus evidence

No topic-specific `BONUS_EVIDENCE` is identified in the current source coverage map. None is inferred.

## Author-created material

All diagnostic, fading, ADOPT and TRANSFER prompts in this v2 book that are not stable historical IDs are `AUTHOR_CREATED_FOUNDATION` or `AUTHOR_CREATED_TRANSFER`. They carry no fake NMTC year/question attribution.

---

# 18. What comes next

This teaching layer is complete enough for Wave 3 compression, but it is not the final publication package.

Next:

1. build the **First-Step Reference** only now, after teaching;
2. build the larger unlabelled Wave-4 mastery/transfer layer;
3. independently audit all final answers and domains;
4. render PDFs and inspect every page in Wave 5.

`NEXT_ALLOWED_STATE: WAVE3_FIRST_STEP_REFERENCE`
