# Algebra v5 — Visual obligation register

Required/optional visuals were decided during analysis, not added decoratively after layout. Each was rendered in the final student PDF and inspected at final reading size.

| ID | Level | Visual | Teaching job | Must not imply/show | Final-size QA |
|---|---|---|---|---|---|
| VIS-01 | REQUIRED | Concept graph | Show prerequisite links and teaching order independent from question order. | Do not use question-order as the organizing spine. | RENDERED_QA_PASS |
| VIS-02 | REQUIRED | Sum-product compression map | Show raw symmetric variables -> s,p -> rebuilt targets. | Do not imply x,y must be solved. | RENDERED_QA_PASS |
| VIS-03 | REQUIRED | Three-variable method selector | Distinguish symmetric, cyclic, and repeated-product opening signatures. | Do not collapse cyclic and symmetric into one label. | RENDERED_QA_PASS |
| VIS-04 | REQUIRED | Quadratic/discriminant root geometry | Show crossing/tangency/no-crossing and repeated-root meaning. | Do not treat Delta=0 as no real roots. | RENDERED_QA_PASS |
| VIS-05 | REQUIRED | Polynomial preimage map | Show roots of P becoming output targets for Q in P(Q(x)). | Do not draw composition as direct root substitution. | RENDERED_QA_PASS |
| VIS-06 | REQUIRED | Symmetric-pole number line | Show paired poles around midpoint and excluded values. | Do not hide domain exclusions. | RENDERED_QA_PASS |
| VIS-07 | REQUIRED | Ordered-mass bound diagram | Show positive/negative mass budgets and forced tail counts. | Do not imply the bound alone proves equality. | RENDERED_QA_PASS |
| VIS-08 | REQUIRED | Finite-difference and recurrence flow | Show quadratic second differences and a proved shift/period cycle. | Do not infer period from a few numerical terms. | RENDERED_QA_PASS |
| VIS-09 | REQUIRED | Multiplicity-aware Vieta diagram | Show repeated root copies and same-root vs distinct-root pair contributions. | Do not count only distinct roots. | RENDERED_QA_PASS |
| VIS-10 | REQUIRED | Smoothing/boundary diagram | Show fixed-sum x+y and range of xy, with coefficient sign deciding boundary/equality. | Do not force x=y in minimization when boundary is optimal. | RENDERED_QA_PASS |
| VIS-11 | OPTIONAL | AP/GP overlap parameterization | Show a-d,a,a+d,T and the GP overlap relation. | Do not introduce four unrelated variables. | RENDERED_QA_PASS |

## QA rule

`RENDERED_QA_PASS` means the visual was inspected in the 200 dpi full-page render, labels were readable, and the mathematical relation was not obscured. The ordered-mass diagram was explicitly corrected after a final-size overlap was found during QA and then re-rendered.
