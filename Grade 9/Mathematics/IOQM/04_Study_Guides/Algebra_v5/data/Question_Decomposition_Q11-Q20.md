# Algebra v5 - Question decomposition Q11-Q20

Exact stems remain frozen in Appendix A. These are analysis records, not replacement transcriptions.

## Q11 / ALG-A-11
- Topic/subtopic: Algebra / Quadratic root classification and repeated-root geometry
- Concepts: primary `C06`; secondary ALG-QUAD-02, ALG-POLY-04
- Recognition cue: A cubic with exactly two distinct real roots must have a repeated root.
- Representation/compression: Translate root-language to discriminant or repeated-root equations, then use geometry/global shape when degree >2.
- FIRST MOVE: Let r be the repeated root and write f(r)=0=f'(r).
- Execution route: Solve f(r)=f'(r)=0 for the repeated root and parameter; exclude the triple-root case.
- Legality/domain/reversibility/admissibility: c real; exactly two distinct roots means repeated but not triple.
- Prerequisites: quadratic discriminant, factorization, graph meaning of roots
- Likely misconception: Using a cubic discriminant formula without understanding multiplicity.
- Competing method: A tempting but usually inferior route is: using a cubic discriminant formula without understanding multiplicity.
- Concrete variant: Use a different one-parameter cubic required to have exactly two distinct real roots; impose f(r)=f'(r)=0 and separately rule out a triple root.
- Transfer: before `HIGH`; v5 `Closed by the primary concept journey, a concrete first move, legality/check guidance, and Appendix A progressive hints.`
- Visual: `OPTIONAL` - tangent/double-root sketch
- Source: `RECONSTRUCTED` / `RECONSTRUCTED_FROM_SCAN` / badge `REC`
- Difficulty vector: {'conceptual': 7, 'recognition': 7, 'reasoning_steps': 8, 'algebra': 8, 'hidden_structure': 8, 'constraints_cases': 7, 'calculation_burden': 6, 'trap_density': 7}; badge `D4 ADVANCED`
- Priority/mastery/support: `MUST` / `UNKNOWN_DIAGNOSTIC_SKIPPED_BY_LEARNER` / `PASS_STATIC_CONTENT`
- Hints: Notice = A cubic with exactly two distinct real roots must have a repeated root.; Recall = Recall ALG-POLY-04 · Repeated-Root Test: a repeated root r satisfies f(r)=0 and f’(r)=0.; Start = none

## Q12 / ALG-A-12
- Topic/subtopic: Algebra / Three-variable symmetry and cyclic method selection
- Concepts: primary `C05`; secondary ALG-SYM3-01, reciprocal sum
- Recognition cue: Rewrite the condition with s=x+y+z, q=xy+yz+zx, r=xyz; the reciprocal target is q/r.
- Representation/compression: Choose among s,q,r; a common value k; p=xyz; or cyclic orientation before algebra.
- FIRST MOVE: Set s=x+y+z, q=xy+yz+zx, r=xyz.
- Execution route: Rewrite the cubic identity in s,q,r to get sq=3r, then compute the reciprocal target q/r or sq/r as required.
- Legality/domain/reversibility/admissibility: x,y,z nonzero complex numbers, so r=xyz!=0.
- Prerequisites: symmetric sums, factorization, rational algebra
- Likely misconception: Expanding all products instead of using s,q,r.
- Competing method: A tempting but usually inferior route is: expanding all products instead of using s,q,r.
- Concrete variant: Change the symmetric cubic identity but keep a reciprocal target; compress with s,q,r and decide which Newton/Vieta identity recovers the target without finding individual variables.
- Transfer: before `MEDIUM`; v5 `Closed by the primary concept journey, a concrete first move, legality/check guidance, and Appendix A progressive hints.`
- Visual: `NONE`
- Source: `RECONSTRUCTED` / `RECONSTRUCTED_FROM_SCAN` / badge `REC`
- Difficulty vector: {'conceptual': 5, 'recognition': 7, 'reasoning_steps': 5, 'algebra': 6, 'hidden_structure': 7, 'constraints_cases': 5, 'calculation_burden': 4, 'trap_density': 5}; badge `D3 STRATEGIC`
- Priority/mastery/support: `MUST` / `UNKNOWN_DIAGNOSTIC_SKIPPED_BY_LEARNER` / `PASS_STATIC_CONTENT`
- Hints: Notice = Rewrite the condition with s=x+y+z, q=xy+yz+zx, r=xyz; the reciprocal target is q/r.; Recall = none; Start = none

## Q13 / ALG-A-13
- Topic/subtopic: Algebra / Sum-product compression in two variables
- Concepts: primary `C04`; secondary ALG-SYM2-03, power sums
- Recognition cue: The factors a-1 and b-1 are reciprocal.
- Representation/compression: Compress a symmetric pair to s=x+y and p=xy; rebuild targets from s,p.
- FIRST MOVE: Observe (a-1)(b-1)=1.
- Execution route: From (a-1)(b-1)=1 derive ab=a+b, recover a+b from the given square sum, then use symmetric power identities.
- Legality/domain/reversibility/admissibility: x,y positive, so a,b>1; reciprocal transformations are legal.
- Prerequisites: identities, quadratic Vieta, factorization
- Likely misconception: Solving x/y explicitly instead of using reciprocal factors.
- Competing method: A tempting but usually inferior route is: solving x/y explicitly instead of using reciprocal factors.
- Concrete variant: Let a=1+t and b=1+1/t with t>0, give a different symmetric power such as a^2+b^2, and ask for a higher power sum using ab=a+b.
- Transfer: before `MEDIUM`; v5 `Closed by the primary concept journey, a concrete first move, legality/check guidance, and Appendix A progressive hints.`
- Visual: `NONE`
- Source: `RECONSTRUCTED` / `RECONSTRUCTED_FROM_SCAN` / badge `REC`
- Difficulty vector: {'conceptual': 5, 'recognition': 7, 'reasoning_steps': 5, 'algebra': 6, 'hidden_structure': 7, 'constraints_cases': 5, 'calculation_burden': 4, 'trap_density': 5}; badge `D3 STRATEGIC`
- Priority/mastery/support: `MUST` / `UNKNOWN_DIAGNOSTIC_SKIPPED_BY_LEARNER` / `PASS_STATIC_CONTENT`
- Hints: Notice = The factors a-1 and b-1 are reciprocal.; Recall = Recall ALG-SYM2-03 · Reciprocal-Ratio Identity: (a-1)(b-1)=1 converts the problem to a relation between a+b and ab.; Start = none

## Q14 / ALG-A-14
- Topic/subtopic: Algebra / Three-variable symmetry and cyclic method selection
- Concepts: primary `C05`; secondary ALG-SYM3-02, real-root structure
- Recognition cue: The symmetric reciprocal condition is much stronger than the huge exponent suggests.
- Representation/compression: Choose among s,q,r; a common value k; p=xyz; or cyclic orientation before algebra.
- FIRST MOVE: Set s=m+n+p, q=mn+np+pm, r=mnp, then translate the reciprocal condition.
- Execution route: Turn the reciprocal condition into sq=r; factor the root cubic and use reality to force an opposite pair, so huge odd powers cancel.
- Legality/domain/reversibility/admissibility: m,n,p nonzero real; use real-root consequences only after preserving nonzero conditions.
- Prerequisites: symmetric sums, factorization, rational algebra
- Likely misconception: Trying to manipulate 2023rd powers directly.
- Competing method: A tempting but usually inferior route is: trying to manipulate 2023rd powers directly.
- Concrete variant: Replace 2023 by any large odd exponent; once the symmetric reciprocal condition forces an opposite pair, explain why every odd-power target cancels in the same way.
- Transfer: before `HIGH`; v5 `Closed by the primary concept journey, a concrete first move, legality/check guidance, and Appendix A progressive hints.`
- Visual: `NONE`
- Source: `RECONSTRUCTED` / `RECONSTRUCTED_FROM_SCAN` / badge `REC`
- Difficulty vector: {'conceptual': 7, 'recognition': 9, 'reasoning_steps': 7, 'algebra': 8, 'hidden_structure': 9, 'constraints_cases': 7, 'calculation_burden': 6, 'trap_density': 7}; badge `D4 ADVANCED`
- Priority/mastery/support: `SHOULD` / `UNKNOWN_DIAGNOSTIC_SKIPPED_BY_LEARNER` / `PASS_STATIC_CONTENT`
- Hints: Notice = The symmetric reciprocal condition is much stronger than the huge exponent suggests.; Recall = Recall ALG-SYM3-02 · Opposite-Pair Factorization: express the condition with s,q,r and factor the cubic having m,n,p as roots.; Start = From (m+n+p)(1/m+1/n+1/p)=1 obtain sq=r; factor t^3-st^2+qt-r and look for an opposite pair of real roots.

## Q15 / ALG-A-15
- Topic/subtopic: Algebra / Polynomial difference, Vieta, root sums and preimage thinking
- Concepts: primary `C07`; secondary ALG-POLY-01, integer-root cases
- Recognition cue: The equation p(m)=p(2) automatically has the factor m-2.
- Representation/compression: Use P(x)-P(a), Vieta/root sums, P'/P, multiplicity counting, or quadratic preimage pairing according to the output/root surface.
- FIRST MOVE: Factor p(m)-p(2)=(m-2)q(m).
- Execution route: After factoring out m-2, classify the monic integer quadratic q(m) so there is exactly one allowed integer m!=2; count coefficient cases.
- Legality/domain/reversibility/admissibility: Coefficient bounds, integer coefficients, uniqueness, and m!=2 must all be enforced.
- Prerequisites: factor theorem, Vieta, quadratic axis symmetry, root multiplicity
- Likely misconception: Treating the residual quadratic's roots as arbitrary reals instead of integer-root cases.
- Competing method: A tempting but usually inferior route is: treating the residual quadratic's roots as arbitrary reals instead of integer-root cases.
- Concrete variant: Replace P(m)=P(2) by P(m)=P(k) for a fixed integer k and change the coefficient box; factor P(m)-P(k) first, then redo the integer-root case split.
- Transfer: before `HIGH`; v5 `Closed by the primary concept journey, a concrete first move, legality/check guidance, and Appendix A progressive hints.`
- Visual: `NONE`
- Source: `RECONSTRUCTED` / `RECONSTRUCTED_FROM_SCAN` / badge `REC`
- Difficulty vector: {'conceptual': 7, 'recognition': 7, 'reasoning_steps': 8, 'algebra': 8, 'hidden_structure': 8, 'constraints_cases': 7, 'calculation_burden': 6, 'trap_density': 7}; badge `D4 ADVANCED`
- Priority/mastery/support: `MUST` / `UNKNOWN_DIAGNOSTIC_SKIPPED_BY_LEARNER` / `PASS_STATIC_CONTENT`
- Hints: Notice = The equation p(m)=p(2) automatically has the factor m-2.; Recall = Recall ALG-POLY-01 · Polynomial Difference Factor: factor p(m)-p(2) before counting integer solutions.; Start = Write p(m)-p(2)=(m-2)Q(m), where Q is a monic integer quadratic; classify how Q can have exactly one allowed integer root.

## Q16 / ALG-A-16
- Topic/subtopic: Algebra / Three-variable symmetry and cyclic method selection
- Concepts: primary `C05`; secondary ALG-CYC-02, real branch comparison
- Recognition cue: The same xyz appears in all three cubic equations.
- Representation/compression: Choose among s,q,r; a common value k; p=xyz; or cyclic orientation before algebra.
- FIRST MOVE: Let p=xyz.
- Execution route: Write x^3=p+2, y^3=p+6, z^3=p+20, multiply to get one equation in p, and compare real p branches.
- Legality/domain/reversibility/admissibility: Real solutions; compare every real p branch that yields real cube roots.
- Prerequisites: symmetric sums, factorization, rational algebra
- Likely misconception: Solving three nonlinear variables directly.
- Competing method: A tempting but usually inferior route is: solving three nonlinear variables directly.
- Concrete variant: Change the constants in x^3-xyz=A, y^3-xyz=B, z^3-xyz=C; again set p=xyz, multiply the three equations, and compare real p-branches before evaluating the target.
- Transfer: before `HIGH`; v5 `Closed by the primary concept journey, a concrete first move, legality/check guidance, and Appendix A progressive hints.`
- Visual: `NONE`
- Source: `RECONSTRUCTED` / `RECONSTRUCTED_FROM_SCAN` / badge `REC`
- Difficulty vector: {'conceptual': 7, 'recognition': 9, 'reasoning_steps': 8, 'algebra': 7, 'hidden_structure': 9, 'constraints_cases': 7, 'calculation_burden': 6, 'trap_density': 7}; badge `D4 ADVANCED`
- Priority/mastery/support: `MUST` / `UNKNOWN_DIAGNOSTIC_SKIPPED_BY_LEARNER` / `PASS_STATIC_CONTENT`
- Hints: Notice = The same xyz appears in all three cubic equations.; Recall = Recall ALG-CYC-02 · Common Product p=xyz: set p=xyz, rewrite x^3,y^3,z^3, then multiply the three equations.; Start = none

## Q17 / ALG-A-17
- Topic/subtopic: Algebra / Inequalities, smoothing and ordered-mass bounds
- Concepts: primary `C09`; secondary ALG-INEQ-04, equality construction
- Recognition cue: Zero sum plus total absolute value fixes the positive and negative mass separately.
- Representation/compression: Freeze one variable or one mass budget, reduce to a one-variable/boundary problem, and prove equality is attainable.
- FIRST MOVE: Use zero sum and L1 norm 1 to write positive mass = negative mass = 1/2.
- Execution route: Use ordering to force many tail terms above/below selected order statistics, derive the sharp bound from the fixed positive/negative mass, and construct equality.
- Legality/domain/reversibility/admissibility: Ordered 100-tuple; equality/attainability must be constructed, not only bounded.
- Prerequisites: AM-GM, fixed-sum product bounds, boundary checking
- Likely misconception: Producing an upper bound without constructing equality.
- Competing method: A tempting but usually inferior route is: producing an upper bound without constructing equality.
- Concrete variant: Use an ordered n-tuple with zero sum and fixed L1 norm, but ask for a different order-statistic gap; convert the norm into positive/negative mass budgets and prove attainability.
- Transfer: before `HIGH`; v5 `Closed by the primary concept journey, a concrete first move, legality/check guidance, and Appendix A progressive hints.`
- Visual: `REQUIRED` - ordered positive/negative mass bar
- Source: `RECONSTRUCTED` / `RECONSTRUCTED_FROM_SCAN` / badge `REC`
- Difficulty vector: {'conceptual': 10, 'recognition': 9, 'reasoning_steps': 10, 'algebra': 9, 'hidden_structure': 9, 'constraints_cases': 10, 'calculation_burden': 8, 'trap_density': 10}; badge `D5 CHALLENGE`
- Priority/mastery/support: `SHOULD` / `UNKNOWN_DIAGNOSTIC_SKIPPED_BY_LEARNER` / `PASS_STATIC_CONTENT`
- Hints: Notice = Zero sum plus total absolute value fixes the positive and negative mass separately.; Recall = Recall ALG-INEQ-04 · Order-Statistic Mass Bound: count how many entries are forced above x_76 and below x_16, then prove equality is attainable.; Start = none

## Q18 / ALG-A-18
- Topic/subtopic: Algebra / Three-variable symmetry and cyclic method selection
- Concepts: primary `C05`; secondary ALG-SYM3-01, shifted products
- Recognition cue: Use s,q,r; the shifted product and cubic power sum determine q and r without solving a,b,c.
- Representation/compression: Choose among s,q,r; a common value k; p=xyz; or cyclic orientation before algebra.
- FIRST MOVE: Set s=6, q=ab+bc+ca, r=abc.
- Execution route: Use x^3+y^3+z^3=s^3-3sq+3r and the shifted product expansion to solve q,r, then evaluate q/r.
- Legality/domain/reversibility/admissibility: Target reciprocal sum requires abc!=0; confirm from the derived branch.
- Prerequisites: symmetric sums, factorization, rational algebra
- Likely misconception: Solving the individual roots rather than symmetric sums.
- Competing method: A tempting but usually inferior route is: solving the individual roots rather than symmetric sums.
- Concrete variant: Keep s=a+b+c fixed but change the given cubic power sum and shifted product (a+t)(b+t)(c+t); recover q,r and then a reciprocal symmetric target.
- Transfer: before `MEDIUM`; v5 `Closed by the primary concept journey, a concrete first move, legality/check guidance, and Appendix A progressive hints.`
- Visual: `NONE`
- Source: `RECONSTRUCTED` / `RECONSTRUCTED_FROM_SCAN` / badge `REC`
- Difficulty vector: {'conceptual': 5, 'recognition': 7, 'reasoning_steps': 5, 'algebra': 6, 'hidden_structure': 7, 'constraints_cases': 5, 'calculation_burden': 4, 'trap_density': 5}; badge `D3 STRATEGIC`
- Priority/mastery/support: `MUST` / `UNKNOWN_DIAGNOSTIC_SKIPPED_BY_LEARNER` / `PASS_STATIC_CONTENT`
- Hints: Notice = Use s,q,r; the shifted product and cubic power sum determine q and r without solving a,b,c.; Recall = none; Start = none

## Q19 / ALG-A-19
- Topic/subtopic: Algebra / AP, GP, HP and mixed progression structure
- Concepts: primary `C10`; secondary ALG-AP-01, difference of squares
- Recognition cue: Three consecutive AP terms are easiest as u-d,u,u+d before squaring.
- Representation/compression: Parameterize AP/GP structure with the minimum variables; use convergence and divisibility before enumeration; HP is reciprocal-AP.
- FIRST MOVE: Write 36+k=(u-d)^2, 300+k=u^2, 596+k=(u+d)^2.
- Execution route: Subtract adjacent square equations to obtain equations in ud and d^2; recover k without choosing square-root signs early.
- Legality/domain/reversibility/admissibility: k integer; squared AP terms allow signed underlying AP values, so do not choose square-root signs early.
- Prerequisites: AP formulas, GP formulas, convergence, integrality
- Likely misconception: Taking square roots too early and introducing sign branches.
- Competing method: A tempting but usually inferior route is: taking square roots too early and introducing sign branches.
- Concrete variant: Replace the three base numbers while requiring that adding k makes them squares of three consecutive AP terms; subtract adjacent square equations before taking any square roots.
- Transfer: before `MEDIUM`; v5 `Closed by the primary concept journey, a concrete first move, legality/check guidance, and Appendix A progressive hints.`
- Visual: `OPTIONAL` - AP-square alignment
- Source: `RECONSTRUCTED` / `RECONSTRUCTED_FROM_SCAN` / badge `REC`
- Difficulty vector: {'conceptual': 5, 'recognition': 6, 'reasoning_steps': 5, 'algebra': 5, 'hidden_structure': 5, 'constraints_cases': 5, 'calculation_burden': 5, 'trap_density': 5}; badge `D3 STRATEGIC`
- Priority/mastery/support: `SHOULD` / `UNKNOWN_DIAGNOSTIC_SKIPPED_BY_LEARNER` / `PASS_STATIC_CONTENT`
- Hints: Notice = Three consecutive AP terms are easiest as u-d,u,u+d before squaring.; Recall = Recall ALG-AP-01 · Centered AP Parameterization: subtract adjacent square equations to isolate d^2 and ud.; Start = none

## Q20 / ALG-A-20
- Topic/subtopic: Algebra / Finite differences and recurrence structure
- Concepts: primary `C11`; secondary ALG-REC-01, quadratic sequences
- Recognition cue: A product of corresponding AP terms is quadratic in the index, so its second finite difference is constant.
- Representation/compression: Look for degree via differences or a shift/period identity before computing many terms.
- FIRST MOVE: Recognize the product sequence as quadratic in n and write a second-difference table.
- Execution route: Because each AP term is linear in n, the product is quadratic; use constant second differences to continue the sequence.
- Legality/domain/reversibility/admissibility: No reconstruction of the two APs is required; second-difference conclusion depends only on linear-in-n factors.
- Prerequisites: sequence algebra, finite differences, induction
- Likely misconception: Assuming first differences, rather than second differences, are constant.
- Competing method: A tempting but usually inferior route is: assuming first differences, rather than second differences, are constant.
- Concrete variant: Give four early terms of a sequence known to be the product of corresponding terms of two APs and ask for a later term; use constant second differences rather than reconstructing both APs.
- Transfer: before `LOW`; v5 `Closed by the primary concept journey, a concrete first move, legality/check guidance, and Appendix A progressive hints.`
- Visual: `REQUIRED` - finite-difference table
- Source: `RECONSTRUCTED` / `RECONSTRUCTED_FROM_SCAN` / badge `REC`
- Difficulty vector: {'conceptual': 3, 'recognition': 5, 'reasoning_steps': 5, 'algebra': 3, 'hidden_structure': 5, 'constraints_cases': 3, 'calculation_burden': 3, 'trap_density': 3}; badge `D2 ROUTINE`
- Priority/mastery/support: `MUST` / `UNKNOWN_DIAGNOSTIC_SKIPPED_BY_LEARNER` / `PASS_STATIC_CONTENT`
- Hints: Notice = A product of corresponding AP terms is quadratic in the index, so its second finite difference is constant.; Recall = none; Start = none
