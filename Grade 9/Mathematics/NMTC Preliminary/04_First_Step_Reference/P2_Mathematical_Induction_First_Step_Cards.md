# P2 Mathematical Induction — First-Step Cards

Use before full proof writing.

## Card 1 — State P(n)
Trigger: “prove for all integers n...”

First move: write the exact proposition and domain.

## Card 2 — Find the true start
Trigger: statement says `n>=n0`.

First move: base case is `P(n0)`, not automatically `P(1)`.

## Card 3 — Sum identity
Trigger: target is a finite sum through n.

First move: write `S_{k+1}=S_k + new term`.

## Card 4 — Product identity
Trigger: target is a finite product through n.

First move: write `A_{k+1}=A_k * new factor`.

## Card 5 — Divisibility by fixed m
Trigger: `m | F(n)`.

First move: rewrite `F(k+1)` as `coefficient*F(k) + obvious multiple of m` when possible.

## Card 6 — Power divisibility
Trigger: `a^n-b^n` or `a^n-c`.

First move: factor/rewrite the next power so the induction-hypothesis block appears.

## Card 7 — Inequality
Trigger: `F(n)>=G(n)`.

First move: use IH, then explicitly identify the extra comparison needed to reach `G(k+1)`.

## Card 8 — Later threshold
Trigger: inequality becomes true only for large n.

First move: test the claimed threshold and make the induction step valid from that threshold onward.

## Card 9 — Recurrence verification
Trigger: recurrence + proposed closed form.

First move: substitute the IH expression into the recurrence for `a_{k+1}`.

## Card 10 — Two previous terms
Trigger: next case depends on `k` and `k-1`.

First move: plan two base cases or strong induction.

## Card 11 — Step size 2
Trigger: proof naturally gives `P(k)->P(k+2)`.

First move: establish enough bases to cover both parity chains.

## Card 12 — Broken proof
Trigger: supplied “induction proof.”

First move: audit in order: proposition -> base -> hypothesis -> bridge -> domain -> conclusion.

## Card 13 — Direct proof cheaper
Trigger: expression visibly factors or has a one-line congruence argument.

First move: compare direct proof cost before committing to induction.

## Card 14 — Source/QC
Trigger: exercise is presented as “NMTC induction PYQ” without source ID.

First move: demand provenance. Current package is syllabus-first and must not invent historical attribution.

---

# Recognition codes

- `PN` proposition/domain
- `BC` base case
- `SA` sum-add-term
- `PF` product-factor
- `DV` divisibility rewrite
- `IQ` inequality bridge
- `RC` recurrence substitution
- `SI` strong/multiple-case induction
- `BR` broken proof repair
- `DP` direct proof preferred
- `QC` provenance/source check
