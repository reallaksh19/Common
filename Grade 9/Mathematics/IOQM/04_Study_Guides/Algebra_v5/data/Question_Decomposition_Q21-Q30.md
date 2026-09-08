# Algebra v5 - Question decomposition Q21-Q30

Exact stems remain frozen in Appendix A. These are analysis records, not replacement transcriptions.

## Q21 / ALG-A-21
- Topic/subtopic: Algebra / AP, GP, HP and mixed progression structure
- Concepts: primary `C10`; secondary ALG-GP-01, convergence
- Recognition cue: The squared-term series is another GP with first term a^2 and ratio r^2.
- Representation/compression: Parameterize AP/GP structure with the minimum variables; use convergence and divisibility before enumeration; HP is reciprocal-AP.
- FIRST MOVE: Write a/(1-r)=2005 and a^2/(1-r^2)=20050.
- Execution route: Divide the two GP-sum equations and factor 1-r^2=(1-r)(1+r); solve with |r|<1.
- Legality/domain/reversibility/admissibility: Infinite GP requires |r|<1.
- Prerequisites: AP formulas, GP formulas, convergence, integrality
- Likely misconception: Ignoring convergence or solving for more parameters than needed.
- Competing method: A tempting but usually inferior route is: ignoring convergence or solving for more parameters than needed.
- Concrete variant: Change the sum of an infinite GP and the sum of the squared-term GP; divide the two equations using 1-r^2=(1-r)(1+r) and enforce |r|<1.
- Transfer: before `MEDIUM`; v5 `Closed by the primary concept journey, a concrete first move, legality/check guidance, and Appendix A progressive hints.`
- Visual: `OPTIONAL` - GP relation table
- Source: `RECONSTRUCTED` / `RECONSTRUCTED_FROM_SCAN` / badge `REC`
- Difficulty vector: {'conceptual': 5, 'recognition': 6, 'reasoning_steps': 5, 'algebra': 5, 'hidden_structure': 5, 'constraints_cases': 6, 'calculation_burden': 4, 'trap_density': 6}; badge `D3 STRATEGIC`
- Priority/mastery/support: `MUST` / `UNKNOWN_DIAGNOSTIC_SKIPPED_BY_LEARNER` / `PASS_STATIC_CONTENT`
- Hints: Notice = The squared-term series is another GP with first term a^2 and ratio r^2.; Recall = Recall ALG-GP-01 · Coupled Geometric Series: compare a/(1-r) and a^2/(1-r^2), using 1-r^2=(1- r)(1+r).; Start = none

## Q22 / ALG-A-22
- Topic/subtopic: Algebra / AP, GP, HP and mixed progression structure
- Concepts: primary `C10`; secondary ALG-AP-01, sum of odd numbers
- Recognition cue: The total increase is the sum of the first n odd numbers.
- Representation/compression: Parameterize AP/GP structure with the minimum variables; use convergence and divisibility before enumeration; HP is reciprocal-AP.
- FIRST MOVE: Write 836-715 as the sum of the first n odd numbers, hence n^2.
- Execution route: Use the odd-number sum n^2 to find n, then use AP symmetry around the middle term and the known average.
- Legality/domain/reversibility/admissibility: n is a positive integer; AP parity/middle-term reasoning must match the number of terms.
- Prerequisites: AP formulas, GP formulas, convergence, integrality
- Likely misconception: Trying to find the first term and common difference instead of using AP symmetry.
- Competing method: A tempting but usually inferior route is: trying to find the first term and common difference instead of using ap symmetry.
- Concrete variant: Change the original AP total and the added odd-number increments; recover n from the square increment and use the middle-term/average structure instead of solving for a and d.
- Transfer: before `LOW`; v5 `Closed by the primary concept journey, a concrete first move, legality/check guidance, and Appendix A progressive hints.`
- Visual: `NONE`
- Source: `RECONSTRUCTED` / `RECONSTRUCTED_FROM_SCAN` / badge `REC`
- Difficulty vector: {'conceptual': 3, 'recognition': 4, 'reasoning_steps': 3, 'algebra': 3, 'hidden_structure': 3, 'constraints_cases': 3, 'calculation_burden': 3, 'trap_density': 3}; badge `D2 ROUTINE`
- Priority/mastery/support: `SHOULD` / `UNKNOWN_DIAGNOSTIC_SKIPPED_BY_LEARNER` / `PASS_STATIC_CONTENT`
- Hints: Notice = The total increase is the sum of the first n odd numbers.; Recall = Recall ALG-AP-01 · Odd-Increment Count: 1+3+...+(2n-1)=n^2, which reveals how many AP terms there are.; Start = none

## Q23 / ALG-A-23
- Topic/subtopic: Algebra / AP, GP, HP and mixed progression structure
- Concepts: primary `C10`; secondary ALG-GP-01, distinct-branch logic
- Recognition cue: For a GP with sum 1, the second term can be written directly from its ratio.
- Representation/compression: Parameterize AP/GP structure with the minimum variables; use convergence and divisibility before enumeration; HP is reciprocal-AP.
- FIRST MOVE: Let the two GP ratios be r and s; equate their common second term r(1-r)=s(1-s).
- Execution route: From equal second terms get either r=s or r+s=1; discard the identical branch, use the third-term information, then enforce convergence.
- Legality/domain/reversibility/admissibility: Both |r|<1 and |s|<1; the two GPs are distinct, so reject r=s.
- Prerequisites: AP formulas, GP formulas, convergence, integrality
- Likely misconception: Keeping the r=s branch even though the GPs are distinct.
- Competing method: A tempting but usually inferior route is: keeping the r=s branch even though the gps are distinct.
- Concrete variant: Use two distinct convergent GPs with equal total and equal second term, but specify a different later term; retain the r+s relation and reject the identical/nonconvergent branches.
- Transfer: before `HIGH`; v5 `Closed by the primary concept journey, a concrete first move, legality/check guidance, and Appendix A progressive hints.`
- Visual: `NONE`
- Source: `RECONSTRUCTED` / `RECONSTRUCTED_FROM_SCAN` / badge `REC`
- Difficulty vector: {'conceptual': 7, 'recognition': 8, 'reasoning_steps': 7, 'algebra': 7, 'hidden_structure': 7, 'constraints_cases': 8, 'calculation_burden': 6, 'trap_density': 8}; badge `D4 ADVANCED`
- Priority/mastery/support: `SHOULD` / `UNKNOWN_DIAGNOSTIC_SKIPPED_BY_LEARNER` / `PASS_STATIC_CONTENT`
- Hints: Notice = For a GP with sum 1, the second term can be written directly from its ratio.; Recall = Recall ALG-GP-01 · Twin GP Ratios: a sum-1 GP with ratio r starts (1-r), r(1-r), r^2(1-r), ... .; Start = Let the two ratios be r,s. Equal second terms give r(1-r)=s(1-s); use distinctness before using the given third term.

## Q24 / ALG-A-24
- Topic/subtopic: Algebra / Finite differences and recurrence structure
- Concepts: primary `C11`; secondary ALG-REC-02, periodicity
- Recognition cue: Compare the recurrence with the same recurrence one index earlier; alternating signs suggest a short shift identity.
- Representation/compression: Look for degree via differences or a shift/period identity before computing many terms.
- FIRST MOVE: Write the recurrence at n and n-1 and substitute one into the other.
- Execution route: Algebraically derive x_n=-x_{n-5}, hence period 10, and reduce the huge indices before evaluating.
- Legality/domain/reversibility/admissibility: Derived shift identity applies only where both recurrence instances are valid; respect starting index.
- Prerequisites: sequence algebra, finite differences, induction
- Likely misconception: Guessing a period from numerical terms without proving the shift identity.
- Competing method: A tempting but usually inferior route is: guessing a period from numerical terms without proving the shift identity.
- Concrete variant: Change the initial values of the same alternating-sign fourth-order recurrence and ask for another combination of huge indices; first prove the short shift/period identity symbolically.
- Transfer: before `HIGH`; v5 `Closed by the primary concept journey, a concrete first move, legality/check guidance, and Appendix A progressive hints.`
- Visual: `REQUIRED` - recurrence shift/period cycle
- Source: `RECONSTRUCTED` / `RECONSTRUCTED_FROM_SCAN` / badge `REC`
- Difficulty vector: {'conceptual': 7, 'recognition': 9, 'reasoning_steps': 9, 'algebra': 7, 'hidden_structure': 9, 'constraints_cases': 7, 'calculation_burden': 6, 'trap_density': 7}; badge `D4 ADVANCED`
- Priority/mastery/support: `MUST` / `UNKNOWN_DIAGNOSTIC_SKIPPED_BY_LEARNER` / `PASS_STATIC_CONTENT`
- Hints: Notice = Compare the recurrence with the same recurrence one index earlier; alternating signs suggest a short shift identity.; Recall = none; Start = none

## Q25 / ALG-A-25
- Topic/subtopic: Algebra / Three-variable symmetry and cyclic method selection
- Concepts: primary `C05`; secondary ALG-CYC-03, complementary fractions
- Recognition cue: The target numerators complement the denominators a+b,b+c,c+a.
- Representation/compression: Choose among s,q,r; a common value k; p=xyz; or cyclic orientation before algebra.
- FIRST MOVE: Let s=a+b+c and let T be the target cyclic sum.
- Execution route: Compute sT termwise, introduce the complementary cyclic sum U with T+U=3, and use the two given sums to solve for s and T.
- Legality/domain/reversibility/admissibility: All denominators a+b,b+c,c+a are nonzero.
- Prerequisites: symmetric sums, factorization, rational algebra
- Likely misconception: Clearing all denominators at once and destroying the cyclic complement structure.
- Competing method: A tempting but usually inferior route is: clearing all denominators at once and destroying the cyclic complement structure.
- Concrete variant: Alter the two supplied cyclic fraction sums while keeping complementary numerators over a+b,b+c,c+a; introduce T and its complement U before any global denominator clearing.
- Transfer: before `HIGH`; v5 `Closed by the primary concept journey, a concrete first move, legality/check guidance, and Appendix A progressive hints.`
- Visual: `NONE`
- Source: `RECONSTRUCTED` / `RECONSTRUCTED_FROM_SCAN` / badge `REC`
- Difficulty vector: {'conceptual': 7, 'recognition': 9, 'reasoning_steps': 8, 'algebra': 7, 'hidden_structure': 9, 'constraints_cases': 7, 'calculation_burden': 6, 'trap_density': 7}; badge `D4 ADVANCED`
- Priority/mastery/support: `SHOULD` / `UNKNOWN_DIAGNOSTIC_SKIPPED_BY_LEARNER` / `PASS_STATIC_CONTENT`
- Hints: Notice = The target numerators complement the denominators a+b,b+c,c+a.; Recall = Recall ALG-CYC-03 · Multiply by the Total Sum: let s=a+b+c and multiply the target term-by-term by s; also use the complementary cyclic sum.; Start = none

## Q26 / ALG-A-26
- Topic/subtopic: Algebra / Polynomial difference, Vieta, root sums and preimage thinking
- Concepts: primary `C07`; secondary ALG-ROOTSUM-02, Newton sums
- Recognition cue: Only the constant term changes when the right side 1/3 is moved into the cubic.
- Representation/compression: Use P(x)-P(a), Vieta/root sums, P'/P, multiplicity counting, or quadratic preimage pairing according to the output/root surface.
- FIRST MOVE: Compare the elementary symmetric sums before and after the constant-term perturbation.
- Execution route: Keep the first two elementary symmetric sums unchanged, update the product by the constant perturbation, and translate to the cubic power sum.
- Legality/domain/reversibility/admissibility: Use the stated three distinct real roots; coefficient perturbation changes only the constant term as specified.
- Prerequisites: factor theorem, Vieta, quadratic axis symmetry, root multiplicity
- Likely misconception: Trying to solve shifted cube roots numerically.
- Competing method: A tempting but usually inferior route is: trying to solve shifted cube roots numerically.
- Concrete variant: Perturb only the constant term of another monic cubic and ask how a low power sum of the roots changes; compare elementary symmetric sums before applying Newton identities.
- Transfer: before `HIGH`; v5 `Closed by the primary concept journey, a concrete first move, legality/check guidance, and Appendix A progressive hints.`
- Visual: `NONE`
- Source: `RECONSTRUCTED` / `RECONSTRUCTED_FROM_SCAN` / badge `REC`
- Difficulty vector: {'conceptual': 7, 'recognition': 7, 'reasoning_steps': 9, 'algebra': 8, 'hidden_structure': 9, 'constraints_cases': 7, 'calculation_burden': 6, 'trap_density': 7}; badge `D4 ADVANCED`
- Priority/mastery/support: `SHOULD` / `UNKNOWN_DIAGNOSTIC_SKIPPED_BY_LEARNER` / `PASS_STATIC_CONTENT`
- Hints: Notice = Only the constant term changes when the right side 1/3 is moved into the cubic.; Recall = Recall ALG-ROOTSUM-02 · Changed Constant Term: the first two elementary symmetric sums stay fixed; only the root product changes.; Start = Compare the original roots cubert(13),cubert(53),cubert(103) with the new roots r,s,t via Vieta, then use the cubic power-sum identity.

## Q27 / ALG-A-27
- Topic/subtopic: Algebra / Three-variable symmetry and cyclic method selection
- Concepts: primary `C05`; secondary ALG-CYC-04, Vandermonde factorization
- Recognition cue: Expanding the squared-difference expression produces the reverse cyclic sum.
- Representation/compression: Choose among s,q,r; a common value k; p=xyz; or cyclic orientation before algebra.
- FIRST MOVE: Expand the squared-difference condition to recover the reverse cyclic sum.
- Execution route: Subtract the two cyclic orientations and factor the difference by the Vandermonde product; conclude two variables coincide, then include all ordered permutations.
- Legality/domain/reversibility/admissibility: Ordered triples: after solving equality patterns include all admissible permutations.
- Prerequisites: symmetric sums, factorization, rational algebra
- Likely misconception: Assuming one equality pattern and forgetting ordered permutations.
- Competing method: A tempting but usually inferior route is: assuming one equality pattern and forgetting ordered permutations.
- Concrete variant: Change the numerical cyclic sums while keeping both orientations present; subtract the two orientations, factor the Vandermonde term, and enumerate all ordered permutations forced by repeated variables.
- Transfer: before `HIGH`; v5 `Closed by the primary concept journey, a concrete first move, legality/check guidance, and Appendix A progressive hints.`
- Visual: `NONE`
- Source: `RECONSTRUCTED` / `RECONSTRUCTED_FROM_SCAN` / badge `REC`; QC: Ordered-triple answer key must include all six permutations, not only two representatives.
- Difficulty vector: {'conceptual': 7, 'recognition': 9, 'reasoning_steps': 8, 'algebra': 7, 'hidden_structure': 9, 'constraints_cases': 7, 'calculation_burden': 6, 'trap_density': 7}; badge `D4 ADVANCED`
- Priority/mastery/support: `SHOULD` / `UNKNOWN_DIAGNOSTIC_SKIPPED_BY_LEARNER` / `PASS_STATIC_CONTENT`
- Hints: Notice = Expanding the squared-difference expression produces the reverse cyclic sum.; Recall = Recall ALG-CYC-04 · Cyclic Orientation Factor: subtract x^2y+y^2z+z^2x and xy^2+yz^2+zx^2 to expose a Vandermonde factor.; Start = Expand the third condition, recover the reverse cyclic sum, then factor the difference as a multiple of (x-y)(y-z)(z-x).

## Q28 / ALG-A-28
- Topic/subtopic: Algebra / Symmetric poles and midpoint shifts
- Concepts: primary `C08`; secondary ALG-EQ-04, ALG-EQ-02
- Recognition cue: The pole locations 3,5,17,19 are symmetric around 11.
- Representation/compression: Center symmetric poles with t=x-c; pair reciprocals; if even in t, use u=t^2.
- FIRST MOVE: Rewrite k/(x-k)+1=x/(x-k), then set t=x-11.
- Execution route: Pair reciprocal terms after t=x-11, reduce to an equation in u=t^2, restore t and x branches, exclude poles, and compare the requested extremal branch.
- Legality/domain/reversibility/admissibility: Exclude x=3,5,17,19 and any divided-away branch; if u=t^2 then u>=0.
- Prerequisites: rational equations, domain exclusions, even substitution u=t^2
- Likely misconception: Cross-multiplying immediately into a high-degree polynomial.
- Competing method: A tempting but usually inferior route is: cross-multiplying immediately into a high-degree polynomial.
- Concrete variant: Place four poles at c±a and c±b and build a rational equation from them; shift t=x-c, pair reciprocals into functions of t^2, and preserve excluded poles.
- Transfer: before `HIGH`; v5 `Closed by the primary concept journey, a concrete first move, legality/check guidance, and Appendix A progressive hints.`
- Visual: `REQUIRED` - symmetric-pole number line
- Source: `RECONSTRUCTED` / `RECONSTRUCTED_FROM_SCAN` / badge `REC`
- Difficulty vector: {'conceptual': 7, 'recognition': 7, 'reasoning_steps': 7, 'algebra': 7, 'hidden_structure': 7, 'constraints_cases': 9, 'calculation_burden': 6, 'trap_density': 9}; badge `D4 ADVANCED`
- Priority/mastery/support: `MUST` / `UNKNOWN_DIAGNOSTIC_SKIPPED_BY_LEARNER` / `PASS_STATIC_CONTENT`
- Hints: Notice = The pole locations 3,5,17,19 are symmetric around 11.; Recall = Recall ALG-EQ-04 · Symmetric Poles: shift to the midpoint and pair reciprocals at ±a.; Start = Rewrite k/(x-k)+1=x/(x-k), then set t=x-11. Handle t=0 before dividing and reduce the remaining equation to u=t^2.

## Q29 / ALG-A-29
- Topic/subtopic: Algebra / Polynomial difference, Vieta, root sums and preimage thinking
- Concepts: primary `C07`; secondary ALG-ROOTSUM-03, source audit
- Recognition cue: Source wording is unresolved. If you explore the literal statement, reduce the denominators with Vieta and use P’/P; do not force the printed key.
- Representation/compression: Use P(x)-P(a), Vieta/root sums, P'/P, multiplicity counting, or quadratic preimage pairing according to the output/root surface.
- FIRST MOVE: Reduce each denominator with Vieta, then prepare to use P'/P; keep the source caveat visible.
- Execution route: For the literal recovered wording, simplify each root-dependent denominator with Vieta, use partial fractions and P'/P, and report the source conflict rather than repairing it.
- Legality/domain/reversibility/admissibility: SOURCE_UNRESOLVED wording; do not silently alter the expression or force the printed key.
- Prerequisites: factor theorem, Vieta, quadratic axis symmetry, root multiplicity
- Likely misconception: Forcing the worksheet key to fit by silently editing the source.
- Competing method: A tempting but usually inferior route is: forcing the worksheet key to fit by silently editing the source.
- Concrete variant: Use a source-verified polynomial and ask for a sum of reciprocal linear functions of its roots; reduce the expression to Σ1/(u-r_i) and evaluate with P'(u)/P(u), with no key-repair ambiguity.
- Transfer: before `SOURCE`; v5 `Closed by the primary concept journey, a concrete first move, legality/check guidance, and Appendix A progressive hints.`
- Visual: `NONE`
- Source: `SOURCE_UNRESOLVED` / `RECONSTRUCTED_FROM_SCAN` / badge `SRC?`; QC: Literal recovered wording gives -19/40 while worksheet key reports 1/8; wording remains unresolved.
- Difficulty vector: {'conceptual': 9, 'recognition': 9, 'reasoning_steps': 10, 'algebra': 10, 'hidden_structure': 10, 'constraints_cases': 9, 'calculation_burden': 8, 'trap_density': 10}; badge `D5 CHALLENGE`
- Priority/mastery/support: `IF TIME` / `UNKNOWN_DIAGNOSTIC_SKIPPED_BY_LEARNER` / `PASS_STATIC_CONTENT`
- Hints: Notice = Source wording is unresolved. If you explore the literal statement, reduce the denominators with Vieta and use P’/P; do not force the printed key.; Recall = none; Start = none

## Q30 / ALG-A-30
- Topic/subtopic: Algebra / Integer and discrete filters
- Concepts: primary `C14`; secondary ALG-INT-02, sum-square identity
- Recognition cue: The ordering a<b<c suggests positive gaps rather than three independent integers.
- Representation/compression: Replace ordered integers by gaps or roots, then use divisibility/bounds/inclusion-exclusion to make the search finite.
- FIRST MOVE: Use the gap identity for a<b<c, then set p=b-a and q=c-b.
- Execution route: Convert the known sum/sum-of-squares to p^2+pq+q^2=112 for positive gaps p,q, then use integrality of a to filter possibilities.
- Legality/domain/reversibility/admissibility: p,q are positive integers because a<b<c; recovered a must be integral.
- Prerequisites: integer gaps, divisibility, Vieta, stars-and-bars with caps
- Likely misconception: Brute-forcing all triples instead of using gap variables.
- Competing method: A tempting but usually inferior route is: brute-forcing all triples instead of using gap variables.
- Concrete variant: Change the fixed sum and sum of squares of three ordered integers; introduce positive gaps p=b-a, q=c-b and use the gap quadratic form before checking integrality.
- Transfer: before `HIGH`; v5 `Closed by the primary concept journey, a concrete first move, legality/check guidance, and Appendix A progressive hints.`
- Visual: `NONE`
- Source: `RECONSTRUCTED` / `RECONSTRUCTED_FROM_SCAN` / badge `REC`
- Difficulty vector: {'conceptual': 7, 'recognition': 7, 'reasoning_steps': 8, 'algebra': 7, 'hidden_structure': 7, 'constraints_cases': 9, 'calculation_burden': 6, 'trap_density': 7}; badge `D4 ADVANCED`
- Priority/mastery/support: `SHOULD` / `UNKNOWN_DIAGNOSTIC_SKIPPED_BY_LEARNER` / `PASS_STATIC_CONTENT`
- Hints: Notice = The ordering a<b<c suggests positive gaps rather than three independent integers.; Recall = Recall ALG-INT-02 · Gap Variables: set p=b-a and q=c-b, then use the sum/sum-of-squares invariant.; Start = none
