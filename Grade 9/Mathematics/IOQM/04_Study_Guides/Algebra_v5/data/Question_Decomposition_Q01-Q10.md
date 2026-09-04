# Algebra v5 - Question decomposition Q01-Q10

Exact stems remain frozen in Appendix A. These are analysis records, not replacement transcriptions.

## Q1 / ALG-A-01
- Topic/subtopic: Algebra / Sum-product compression in two variables
- Concepts: primary `C04`; secondary ALG-FAC-01, ALG-POLY-03
- Recognition cue: The conditions contain both x+y and xy after one factorization.
- Representation/compression: Compress a symmetric pair to s=x+y and p=xy; rebuild targets from s,p.
- FIRST MOVE: Let s=x+y and p=xy.
- Execution route: Factor x^2y+xy^2=xy(x+y), solve the two equations in s,p, then rebuild x^2+y^2=s^2-2p.
- Legality/domain/reversibility/admissibility: x,y positive integers; retain only branches admitting such x,y.
- Prerequisites: identities, quadratic Vieta, factorization
- Likely misconception: Solving for x,y individually before compressing.
- Competing method: A tempting but usually inferior route is: solving for x,y individually before compressing.
- Concrete variant: Keep the same two symmetric conditions but ask for x^3+y^3; after finding s=x+y and p=xy, rebuild the new target from s,p.
- Transfer: before `MEDIUM`; v5 `Closed by the primary concept journey, a concrete first move, legality/check guidance, and Appendix A progressive hints.`
- Visual: `OPTIONAL` - sum-product compression map
- Source: `RECONSTRUCTED` / `RECONSTRUCTED_FROM_SCAN` / badge `REC`
- Difficulty vector: {'conceptual': 5, 'recognition': 7, 'reasoning_steps': 5, 'algebra': 6, 'hidden_structure': 7, 'constraints_cases': 5, 'calculation_burden': 4, 'trap_density': 5}; badge `D3 STRATEGIC`
- Priority/mastery/support: `MUST` / `UNKNOWN_DIAGNOSTIC_SKIPPED_BY_LEARNER` / `PASS_STATIC_CONTENT`
- Hints: Notice = The conditions contain both x+y and xy after one factorization.; Recall = Recall ALG-SYM2-01 · Sum-Product Trick: use s=x+y and p=xy instead of solving x,y first.; Start = none

## Q2 / ALG-A-02
- Topic/subtopic: Algebra / Three-variable symmetry and cyclic method selection
- Concepts: primary `C05`; secondary ALG-CYC-02, ALG-EQ-02
- Recognition cue: The three cyclic expressions become much simpler when multiplied under xyz=1.
- Representation/compression: Choose among s,q,r; a common value k; p=xyz; or cyclic orientation before algebra.
- FIRST MOVE: Let t=z+1/y and multiply the three displayed cyclic sums.
- Execution route: Use xyz=1 to collapse the product of the three cyclic sums to an equation in the requested t.
- Legality/domain/reversibility/admissibility: x,y,z positive, hence all reciprocal expressions are defined.
- Prerequisites: symmetric sums, factorization, rational algebra
- Likely misconception: Trying to solve x,y,z separately instead of exploiting xyz=1.
- Competing method: A tempting but usually inferior route is: trying to solve x,y,z separately instead of exploiting xyz=1.
- Concrete variant: Keep xyz=1 but change the two given cyclic reciprocal sums; ask for the third cyclic sum and test whether multiplying the cycle still closes in one variable.
- Transfer: before `MEDIUM`; v5 `Closed by the primary concept journey, a concrete first move, legality/check guidance, and Appendix A progressive hints.`
- Visual: `OPTIONAL` - cyclic method selector
- Source: `RECONSTRUCTED` / `RECONSTRUCTED_FROM_SCAN` / badge `REC`
- Difficulty vector: {'conceptual': 5, 'recognition': 7, 'reasoning_steps': 6, 'algebra': 5, 'hidden_structure': 7, 'constraints_cases': 5, 'calculation_burden': 4, 'trap_density': 5}; badge `D3 STRATEGIC`
- Priority/mastery/support: `MUST` / `UNKNOWN_DIAGNOSTIC_SKIPPED_BY_LEARNER` / `PASS_STATIC_CONTENT`
- Hints: Notice = The three cyclic expressions become much simpler when multiplied under xyz=1.; Recall = Recall ALG-CYC-02 · Cyclic Product Collapse: reciprocal products can collapse using xyz=1.; Start = Name the requested quantity t=z+1/y, then multiply the three cyclic sums before solving any variable.

## Q3 / ALG-A-03
- Topic/subtopic: Algebra / Exponent substitutions, radicals and algebraic irrational bases
- Concepts: primary `C12`; secondary ALG-POLY-03, ALG-EXP-01
- Recognition cue: Every exponent is built from the same multiple of 111x.
- Representation/compression: Replace common exponential blocks by a positive variable; compare irrational basis components exactly rather than numerically.
- FIRST MOVE: Set u=2^(111x)>0.
- Execution route: Convert to a cubic in u, apply Vieta to the positive u-roots, then translate the root product into the sum of x-roots.
- Legality/domain/reversibility/admissibility: u=2^(111x)>0; only positive u-roots correspond to real x.
- Prerequisites: index laws, Vieta, linear independence over Q
- Likely misconception: Taking logarithms term-by-term before converting to a polynomial.
- Competing method: A tempting but usually inferior route is: taking logarithms term-by-term before converting to a polynomial.
- Concrete variant: Replace base 2 by another positive base B≠1 and keep all exponents as multiples of one linear form in x; ask for the sum of real x-roots after the polynomial substitution.
- Transfer: before `HIGH`; v5 `Closed by the primary concept journey, a concrete first move, legality/check guidance, and Appendix A progressive hints.`
- Visual: `NONE`
- Source: `RECONSTRUCTED` / `RECONSTRUCTED_FROM_SCAN` / badge `REC`
- Difficulty vector: {'conceptual': 7, 'recognition': 9, 'reasoning_steps': 7, 'algebra': 8, 'hidden_structure': 7, 'constraints_cases': 7, 'calculation_burden': 6, 'trap_density': 7}; badge `D4 ADVANCED`
- Priority/mastery/support: `MUST` / `UNKNOWN_DIAGNOSTIC_SKIPPED_BY_LEARNER` / `PASS_STATIC_CONTENT`
- Hints: Notice = Every exponent is built from the same multiple of 111x.; Recall = Recall ALG-EXP-01 · Common Exponent Substitution: turn the exponential equation into a polynomial in one positive variable.; Start = Set u=2^(111x)>0. Use Vieta on the cubic in u, then translate the product of u-roots back to the sum of the x-roots.

## Q4 / ALG-A-04
- Topic/subtopic: Algebra / Linear totals, averages and consecutive-block translation
- Concepts: primary `C03`; secondary ALG-LIN-01
- Recognition cue: Every average statement changes both the total and the number of terms.
- Representation/compression: Replace raw lists by count, total, extremes and consecutive-block sums.
- FIRST MOVE: Let n be the original size, T the total, L the least value, and M the greatest value.
- Execution route: Translate each average statement to a total/count equation in n,T,L,M and solve the linear system.
- Legality/domain/reversibility/admissibility: Finite positive-integer set; all counts after removals must be positive integers.
- Prerequisites: mean = total/count, linear elimination, arithmetic series
- Likely misconception: Manipulating averages without tracking totals and counts.
- Competing method: A tempting but usually inferior route is: manipulating averages without tracking totals and counts.
- Concrete variant: Change which extreme values are removed and the resulting averages; require the original set size, forcing total/count bookkeeping rather than ad hoc averaging.
- Transfer: before `LOW`; v5 `Closed by the primary concept journey, a concrete first move, legality/check guidance, and Appendix A progressive hints.`
- Visual: `NONE`
- Source: `RECONSTRUCTED` / `RECONSTRUCTED_FROM_SCAN` / badge `REC`
- Difficulty vector: {'conceptual': 3, 'recognition': 4, 'reasoning_steps': 4, 'algebra': 3, 'hidden_structure': 3, 'constraints_cases': 3, 'calculation_burden': 2, 'trap_density': 3}; badge `D2 ROUTINE`
- Priority/mastery/support: `SHOULD` / `UNKNOWN_DIAGNOSTIC_SKIPPED_BY_LEARNER` / `PASS_STATIC_CONTENT`
- Hints: Notice = Every average statement changes both the total and the number of terms.; Recall = Recall ALG-LIN-03 · Changing-Average Ledger: introduce original count n, total T, least L, greatest M.; Start = none

## Q5 / ALG-A-05
- Topic/subtopic: Algebra / AP, GP, HP and mixed progression structure
- Concepts: primary `C10`; secondary ALG-AP-01, polygon angle sum
- Recognition cue: The 18 angles are an integer arithmetic progression with a fixed polygon total.
- Representation/compression: Parameterize AP/GP structure with the minimum variables; use convergence and divisibility before enumeration; HP is reciprocal-AP.
- FIRST MOVE: Write the angles as a,a+d,...,a+17d and use their total 2880 degrees.
- Execution route: Use AP average 160 together with integrality, positivity of d, and convexity (<180 degrees) to restrict d and recover the first angle.
- Legality/domain/reversibility/admissibility: d is a positive integer and every interior angle is <180 degrees.
- Prerequisites: AP formulas, GP formulas, convergence, integrality
- Likely misconception: Using the AP sum but forgetting integrality or convexity.
- Competing method: A tempting but usually inferior route is: using the ap sum but forgetting integrality or convexity.
- Concrete variant: Use a convex n-gon whose integer angles form an increasing AP; change n and ask for the common difference, preserving angle-sum, integrality, and convexity filters.
- Transfer: before `MEDIUM`; v5 `Closed by the primary concept journey, a concrete first move, legality/check guidance, and Appendix A progressive hints.`
- Visual: `NONE`
- Source: `RECONSTRUCTED` / `RECONSTRUCTED_FROM_SCAN` / badge `REC`
- Difficulty vector: {'conceptual': 5, 'recognition': 6, 'reasoning_steps': 5, 'algebra': 5, 'hidden_structure': 5, 'constraints_cases': 5, 'calculation_burden': 5, 'trap_density': 5}; badge `D3 STRATEGIC`
- Priority/mastery/support: `MUST` / `UNKNOWN_DIAGNOSTIC_SKIPPED_BY_LEARNER` / `PASS_STATIC_CONTENT`
- Hints: Notice = The 18 angles are an integer arithmetic progression with a fixed polygon total.; Recall = Recall ALG-AP-01 · Integer AP Constraints: write a,a+d,...,a+17d, then combine the angle sum with integrality and convexity.; Start = none

## Q6 / ALG-A-06
- Topic/subtopic: Algebra / Identities and manufactured factorisation
- Concepts: primary `C01`; secondary ALG-ID-01, integer factor pairs
- Recognition cue: The equation is one constant away from a product in x^2 and y^2.
- Representation/compression: Manufacture a factorization whose factors expose divisibility, sign or squares.
- FIRST MOVE: Add/subtract the constant needed to form (3x^2+1)(y^2-10).
- Execution route: Factor to (3x^2+1)(y^2-10)=507 and enumerate divisor-compatible square values.
- Legality/domain/reversibility/admissibility: x,y integers; divisor factors and square conditions must both hold.
- Prerequisites: basic expansion, difference of squares, integer factor pairs
- Likely misconception: Expanding instead of manufacturing a divisor product.
- Competing method: A tempting but usually inferior route is: expanding instead of manufacturing a divisor product.
- Concrete variant: Alter the constant so the equation is one adjustment away from (Ax^2+B)(y^2-C)=N; the task is still to manufacture the product before enumerating factor pairs.
- Transfer: before `MEDIUM`; v5 `Closed by the primary concept journey, a concrete first move, legality/check guidance, and Appendix A progressive hints.`
- Visual: `NONE`
- Source: `RECONSTRUCTED` / `RECONSTRUCTED_FROM_SCAN` / badge `REC`
- Difficulty vector: {'conceptual': 5, 'recognition': 6, 'reasoning_steps': 5, 'algebra': 5, 'hidden_structure': 7, 'constraints_cases': 5, 'calculation_burden': 4, 'trap_density': 5}; badge `D3 STRATEGIC`
- Priority/mastery/support: `MUST` / `UNKNOWN_DIAGNOSTIC_SKIPPED_BY_LEARNER` / `PASS_STATIC_CONTENT`
- Hints: Notice = The equation is one constant away from a product in x^2 and y^2.; Recall = Recall ALG-FAC-01 · Manufactured Factorization: try to create (3x^2+1)(y^2-c)=N.; Start = none

## Q7 / ALG-A-07
- Topic/subtopic: Algebra / Quadratic root classification and repeated-root geometry
- Concepts: primary `C06`; secondary ALG-QUAD-01, integer bounds
- Recognition cue: “Not two distinct real roots” means a non-positive discriminant, and there are two quadratics.
- Representation/compression: Translate root-language to discriminant or repeated-root equations, then use geometry/global shape when degree >2.
- FIRST MOVE: Write b^2<=4c and c^2<=4b.
- Execution route: Combine the two discriminant inequalities to obtain a small finite bound on positive integers b,c, then enumerate.
- Legality/domain/reversibility/admissibility: b,c positive integers; Delta=0 is allowed because the condition excludes only two distinct real roots.
- Prerequisites: quadratic discriminant, factorization, graph meaning of roots
- Likely misconception: Using Delta<0 instead of Delta<=0 and losing double-root cases.
- Competing method: A tempting but usually inferior route is: using delta<0 instead of delta<=0 and losing double-root cases.
- Concrete variant: Replace the two parameterized quadratics by another reciprocal pair and require each to have at most one real root; the opening remains two discriminant inequalities with boundary equality allowed.
- Transfer: before `MEDIUM`; v5 `Closed by the primary concept journey, a concrete first move, legality/check guidance, and Appendix A progressive hints.`
- Visual: `REQUIRED` - root-classification geometry
- Source: `RECONSTRUCTED` / `RECONSTRUCTED_FROM_SCAN` / badge `REC`
- Difficulty vector: {'conceptual': 5, 'recognition': 6, 'reasoning_steps': 5, 'algebra': 5, 'hidden_structure': 5, 'constraints_cases': 6, 'calculation_burden': 4, 'trap_density': 6}; badge `D3 STRATEGIC`
- Priority/mastery/support: `MUST` / `UNKNOWN_DIAGNOSTIC_SKIPPED_BY_LEARNER` / `PASS_STATIC_CONTENT`
- Hints: Notice = “Not two distinct real roots” means a non-positive discriminant, and there are two quadratics.; Recall = Recall ALG-QUAD-03 · Two Discriminant Bounds: write both discriminant inequalities before doing any integer casework.; Start = none

## Q8 / ALG-A-08
- Topic/subtopic: Algebra / Sum-product compression in two variables
- Concepts: primary `C04`; secondary ALG-SYM2-04, ALG-QUAD-01
- Recognition cue: Use s=x+y and p=xy, but remember the target is |x-y|, not (x-y)^2.
- Representation/compression: Compress a symmetric pair to s=x+y and p=xy; rebuild targets from s,p.
- FIRST MOVE: Let s=x+y and p=xy.
- Execution route: Use the shifted product and square-sum to obtain possible s,p branches; compute (x-y)^2=s^2-4p on every branch, then take |x-y|.
- Legality/domain/reversibility/admissibility: x,y real; check every s,p branch and return |x-y|, not its square.
- Prerequisites: identities, quadratic Vieta, factorization
- Likely misconception: Maximizing (x-y)^2 but reporting that square as |x-y|.
- Competing method: A tempting but usually inferior route is: maximizing (x-y)^2 but reporting that square as |x-y|.
- Concrete variant: Replace (x-2)(y-2) by (x-a)(y-a) and change the fixed value of x^2+y^2; maximize |x-y| by comparing all admissible s,p branches.
- Transfer: before `MEDIUM`; v5 `Closed by the primary concept journey, a concrete first move, legality/check guidance, and Appendix A progressive hints.`
- Visual: `OPTIONAL` - branch comparison table
- Source: `RECONSTRUCTED` / `RECONSTRUCTED_FROM_SCAN` / badge `REC`; QC: Worksheet key printed 2197 for a target |x-y|; verified answer for the stated target is sqrt(2197).
- Difficulty vector: {'conceptual': 5, 'recognition': 7, 'reasoning_steps': 5, 'algebra': 6, 'hidden_structure': 7, 'constraints_cases': 5, 'calculation_burden': 4, 'trap_density': 5}; badge `D3 STRATEGIC`
- Priority/mastery/support: `MUST` / `UNKNOWN_DIAGNOSTIC_SKIPPED_BY_LEARNER` / `PASS_STATIC_CONTENT`
- Hints: Notice = Use s=x+y and p=xy, but remember the target is |x-y|, not (x-y)^2.; Recall = none; Start = none

## Q9 / ALG-A-09
- Topic/subtopic: Algebra / Sum-product compression in two variables
- Concepts: primary `C04`; secondary ALG-SYM2-04, complex admissibility
- Recognition cue: The conditions and target are symmetric in a,b, and complex values are allowed.
- Representation/compression: Compress a symmetric pair to s=x+y and p=xy; rebuild targets from s,p.
- FIRST MOVE: Let s=a+b and p=ab; keep complex branches.
- Execution route: Solve for symmetric data s,p, express the target in s,p, and sum over all complex-admissible branches without imposing real discriminant conditions.
- Legality/domain/reversibility/admissibility: Complex values are explicitly allowed; do not impose real-root discriminant restrictions.
- Prerequisites: identities, quadratic Vieta, factorization
- Likely misconception: Assuming complex variables must form real-root pairs.
- Competing method: A tempting but usually inferior route is: assuming complex variables must form real-root pairs.
- Concrete variant: Keep the equations symmetric in complex a,b but change the requested symmetric power sum; retain nonreal branches and aggregate all admissible target values.
- Transfer: before `HIGH`; v5 `Closed by the primary concept journey, a concrete first move, legality/check guidance, and Appendix A progressive hints.`
- Visual: `NONE`
- Source: `RECONSTRUCTED` / `RECONSTRUCTED_FROM_SCAN` / badge `REC`
- Difficulty vector: {'conceptual': 7, 'recognition': 7, 'reasoning_steps': 7, 'algebra': 7, 'hidden_structure': 7, 'constraints_cases': 7, 'calculation_burden': 6, 'trap_density': 10}; badge `D4 ADVANCED`
- Priority/mastery/support: `SHOULD` / `UNKNOWN_DIAGNOSTIC_SKIPPED_BY_LEARNER` / `PASS_STATIC_CONTENT`
- Hints: Notice = The conditions and target are symmetric in a,b, and complex values are allowed.; Recall = Recall ALG-CPLX-03 · Keep Complex Branches: compute through s=a+b,p=ab and do not reject a branch merely for a negative real discriminant.; Start = none

## Q10 / ALG-A-10
- Topic/subtopic: Algebra / Three-variable symmetry and cyclic method selection
- Concepts: primary `C05`; secondary ALG-EQ-02, ALG-CYC-01
- Recognition cue: Several expressions are equal; naming the common value should reduce the system.
- Representation/compression: Choose among s,q,r; a common value k; p=xyz; or cyclic orientation before algebra.
- FIRST MOVE: Let the common value be k.
- Execution route: Multiply the equalities by the variables that clear reciprocal terms, derive relations in k and abc, then recover a+b+c.
- Legality/domain/reversibility/admissibility: a,b,c and a+b+c are nonzero wherever they appear in denominators.
- Prerequisites: symmetric sums, factorization, rational algebra
- Likely misconception: Using pairwise subtraction only and missing the common-value compression.
- Competing method: A tempting but usually inferior route is: using pairwise subtraction only and missing the common-value compression.
- Concrete variant: Change the constants in the equal cyclic rational expressions; name the common value first and test whether multiplication/summation still reduces the system before pairwise elimination.
- Transfer: before `HIGH`; v5 `Closed by the primary concept journey, a concrete first move, legality/check guidance, and Appendix A progressive hints.`
- Visual: `NONE`
- Source: `RECONSTRUCTED` / `RECONSTRUCTED_FROM_SCAN` / badge `REC`
- Difficulty vector: {'conceptual': 7, 'recognition': 9, 'reasoning_steps': 8, 'algebra': 7, 'hidden_structure': 9, 'constraints_cases': 7, 'calculation_burden': 6, 'trap_density': 7}; badge `D4 ADVANCED`
- Priority/mastery/support: `MUST` / `UNKNOWN_DIAGNOSTIC_SKIPPED_BY_LEARNER` / `PASS_STATIC_CONTENT`
- Hints: Notice = Several expressions are equal; naming the common value should reduce the system.; Recall = Recall ALG-CYC-01 · Common-Value Method: multiply each equality by the variable that clears its reciprocal term.; Start = Let the common value be k. Multiply the three equalities by a,b,c respectively, then add/multiply the resulting simple relations.
