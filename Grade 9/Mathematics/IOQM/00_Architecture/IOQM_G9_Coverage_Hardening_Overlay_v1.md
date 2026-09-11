# IOQM Grade 9 — Coverage Hardening Overlay v1

Status: `V1_MANDATORY_CROSS_TOPIC_OVERLAY`
Issues: `#132`, `#134`

This overlay hardens the frozen 22-topic production architecture against external preparation/checklist comparisons while keeping official-paper/corpus verification as the authority for historical claims.

It does **not** create a 23rd main topic, change domain ownership, or claim official IOQM topic weightage. The user-provided `IOQM grade 9.docx` is treated only as comparison material: it may reveal a useful teaching emphasis, but it does not override the verified corpus or canonical ownership.

## H1 — Euclid’s Lemma

Canonical teaching owner: `IOQM-G9-NT-01`.

Learner statement:

> If `p` is prime and `p | ab`, then `p | a` or `p | b`.

Required teaching behavior:
- check that the divisor is prime before invoking the lemma;
- connect the statement to gcd/Bézout-style divisibility structure rather than presenting it as an isolated slogan;
- contrast it with the false composite analogue (for example `6 | 2*3` but `6` divides neither factor);
- export the result downstream so NT-03 may retrieve it in prime-factor/FTA arguments without reteaching it.

NT-03 remains the owner of prime factorisation, valuations, divisor counts and perfect-power structure.

## H2 — Bounded Euler bridge

Canonical teaching owner: `IOQM-G9-NT-02`.

Learner statement:

> If `gcd(a,n)=1`, then `a^phi(n) ≡ 1 (mod n)`, where `phi(n)` is the number of integers in `1,...,n` that are coprime to `n`.

Grade-9 boundary:
- define `phi(n)` only as much as needed to apply the theorem;
- require an explicit coprimality check before use;
- prefer a short visible residue cycle/order argument when it is cheaper;
- do not expand this into a full totient-function chapter.

### Prime-modulus companion

Fermat’s little theorem may be taught as a **curriculum-design companion/corollary**, not as a claim extracted from the external preparation checklist:

> If `p` is prime and `p ∤ a`, then `a^(p-1) ≡ 1 (mod p)`.

The learner must still check `p ∤ a` / `gcd(a,p)=1` before invoking it.

## H3 — Proof Strategy Toolkit

All main-topic authoring consumes:

`00_Architecture/IOQM_G9_Proof_Strategy_Toolkit_v1.md`

Topics retrieve the relevant proof modes rather than duplicating a generic proof chapter. The toolkit is cross-topic infrastructure, not a new main topic.

Minimum reusable modes:
- direct implication;
- equivalence vs implication discipline;
- contradiction;
- contrapositive where cheaper;
- legal counterexample;
- finite exhaustive cases with completeness proof;
- extremal choice;
- invariant / monovariant;
- construction vs obstruction;
- equality-condition closure.

## H4 — Absolute-value inequality bridge

Canonical teaching owner: `IOQM-G9-ALG-02`.

Required learner capabilities:
- interpret `|x-a|` as distance from `a`;
- translate `|u|<d`, `|u|<=d`, `|u|>d`, `|u|>=d` into the correct interval/union form with the sign condition `d>=0` handled explicitly;
- for nested forms such as `||x|-k|<d`, remove the **outer** absolute value first, then solve the resulting condition on `|x|`;
- count integer solutions only after the real solution set is correct;
- distinguish interval solving from optimization: do not import AM-GM/Cauchy merely because an inequality symbol is visible.

ALG-07 may retrieve the resulting real intervals when floor/ceiling or integer-counting structure becomes primary, but canonical absolute-value inequality teaching remains ALG-02.

## H5 — Bézout / extended-Euclid bridge

Canonical teaching owner: `IOQM-G9-NT-01`; downstream reconstruction owner: `IOQM-G9-NT-04`.

Learner statement:

> For integers `a,b`, there exist integers `x,y` with `ax+by=gcd(a,b)`.

Grade-9 use boundary:
- teach the identity as the constructive end-state of the Euclidean algorithm, not as an isolated theorem name;
- derive the solvability criterion `ax+by=c` has integer solutions iff `gcd(a,b)|c`;
- for closest-rational/determinant-style problems, use small values of `|qb-pa|` only after denominator/integrality constraints are stated;
- NT-04 retrieves this solvability/linear-combination bridge and owns the full Diophantine reconstruction, parameterization and finite filtering.

## H6 — Consecutive-sum / odd-divisor transfer

Structural owner: `IOQM-G9-NT-03`; reconstruction/application owner: `IOQM-G9-NT-04`.

For a sum of `r>=2` consecutive positive integers beginning at `a>=1`,

`n = r(2a+r-1)/2`, hence `2n = r(2a+r-1)`.

Required transfer:
- recognize that the two factors on the right have opposite parity;
- derive that a positive integer is representable as a sum of at least two consecutive positive integers **iff it is not a power of 2** (equivalently, iff it has an odd divisor greater than 1);
- NT-03 owns the odd-divisor/power-of-two structural characterization;
- NT-04 owns reconstruction of `r,a`, positivity checks, bounds and any finite admissible-case analysis.

This is a cross-topic transfer module, not a new number-theory topic.

## Production acceptance

A future or revised topic package should not claim this overlay is satisfied merely because a theorem/method name appears in metadata/control prose. Where H1/H2/H4/H5/H6 are owned, the learner layer must include:
- meaning/hypotheses;
- one proof or derivational explanation at Grade-9 depth where appropriate;
- decision boundary for when to use it;
- at least one diagnostic contrast;
- synchronized teacher diagnostics;
- recertified rendered artifacts if a previously certified learner source changes.

## Evidence truth

This overlay records curriculum coverage, not classroom effectiveness. Classroom timing/readability, longitudinal retention, psychometric calibration, qualification/pass-mark calibration and publication approval remain `NOT_RUN` unless separately evidenced.