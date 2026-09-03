# IOQM Grade 9 — Coverage Hardening Overlay v1

Status: `V1_MANDATORY_CROSS_TOPIC_OVERLAY`
Issue: `#132`

This overlay hardens the frozen 22-topic production architecture against an external preparation checklist that explicitly names **Euclid’s Lemma**, **Euler’s Theorem (basic)** and **Basic Proofs / Proof strategies**.

It does **not** create a 23rd main topic, change domain ownership, or claim official IOQM topic weightage.

## H1 — Euclid’s Lemma

Canonical teaching owner: `IOQM-G9-NT-01`.

Learner statement:

> If `p` is prime and `p | ab`, then `p | a` or `p | b`.

Required teaching behavior:
- check that the divisor is prime before invoking the lemma;
- connect the statement to gcd/Bezout-style divisibility structure rather than presenting it as an isolated slogan;
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

## Production acceptance

A future or revised topic package should not claim this overlay is satisfied merely because a theorem name appears in metadata/control prose. Where H1/H2 are owned, the learner layer must include:
- meaning/hypotheses;
- one proof or derivational explanation at Grade-9 depth where appropriate;
- decision boundary for when to use it;
- at least one diagnostic contrast;
- synchronized teacher diagnostics;
- recertified rendered artifacts if a previously certified learner source changes.

## Evidence truth

This overlay records curriculum coverage, not classroom effectiveness. Classroom timing/readability, longitudinal retention, psychometric calibration, qualification/pass-mark calibration and publication approval remain `NOT_RUN` unless separately evidenced.