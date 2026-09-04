# Benchmark Assimilation Lab — Triangle Feasibility and Metric Relations

Use this after the Assimilation Book and before the H0 mastery test. The aim is to test whether you can **classify the object and select a legal metric route before calculating**.

Learning loop:

`RECONNECT -> DIAGNOSE -> ADOPT -> TRANSFER`

## A. RECONNECT — no notes

Write only the first useful relation unless a short explanation is requested.

1. Two sides are `p,q`; what strict interval must a third side `d` satisfy?
2. What must be identified before using the acute/right/obtuse square test?
3. What fact turns a cevian into a median?
4. What fact turns a cevian into an angle bisector?
5. When is Apollonius cheaper than Stewart?
6. What must be written before substituting into Stewart?
7. What direct metric relation should be tested when an altitude meets the hypotenuse of a right triangle?
8. What variables are natural when exradii are given?
9. In an integer-geometry problem, what comes before enumeration/factor filtering?
10. When should GEO-03 be retrieved rather than reteaching a theorem here?

Diagnostic interpretation:

- misses 1 -> feasibility/degeneracy control is weak;
- misses 2 -> largest-side classification is weak;
- misses 3-4 -> special-cevian classification is weak;
- misses 5-6 -> theorem-selection hierarchy is weak;
- misses 7 -> right-triangle metric retrieval is weak;
- misses 8 -> radius/complement bridge is weak;
- misses 9 -> continuous-to-discrete sequencing is weak;
- misses 10 -> prerequisite boundary control is weak.

## B. Error laboratory

For each proposed solution, identify the first invalid or inefficient move and repair it.

### Error 1 — positive lengths imply triangle
Claim: “All three lengths are positive, so the triangle exists.”

Repair target: strict triangle inequality.

### Error 2 — wrong side in the square test
Claim: “To decide acute/right/obtuse, compare any one side squared with the sum of the other two squares.”

Repair target: sort and use the largest side.

### Error 3 — median from appearance
Claim: “`AD` looks symmetric, so `BD=DC`.”

Repair target: midpoint must be stated or proved.

### Error 4 — angle bisector means midpoint
Claim: “`AD` bisects `angle A`, so `BD=DC`.”

Repair target: use `BD/DC=AB/AC`; midpoint occurs only under extra symmetry.

### Error 5 — Stewart reflex
Claim: “There is a cevian, therefore Stewart is the correct first theorem.”

Repair target: classify median/angle-bisector/right-triangle/GEO-03 routes before the general fallback.

### Error 6 — integer search first
Claim: “The answer is an integer, so list candidate integers and test them.”

Repair target: derive the continuous geometric constraint first.

### Error 7 — source semantics flattened
Claim: “When choosing three values from a set, I will assume they are distinct unless the diagram suggests otherwise.”

Repair target: obey the exact selection language; repetition/distinctness changes the extremal triple.

### Error 8 — verified answer means verified figure
Claim: “The historical numerical answer is independently verified, so any equivalent redraw of the geometry is safe to publish.”

Repair target: exact source-page/figure custody is a separate publication gate.

## C. ADOPT — first two useful lines

Do not solve fully.

1. A triangle has sides `14,19,x`.
2. A triangle has side lengths `10,11,15` and its type is requested.
3. `M` is midpoint of `BC`; all three side lengths are known and `AM` is requested.
4. `AD` bisects `angle A`; `AB,AC,BC` are known and the split of `BC` is requested.
5. `D` divides `BC` in ratio `2:3`; no special-cevian property is stated and `AD` is requested.
6. A right-triangle altitude divides the hypotenuse into `p,q`.
7. Three exradii are known.
8. A proposed quadrilateral diagonal must work for two side-pairs.
9. An integer side length is required after a metric equation is derived.
10. Parallel lines create similar triangles and the target is a ratio.

## D. TRANSFER — changed surface

1. A quadrilateral diagonal problem becomes an intersection of two triangle-feasibility intervals. Explain the invariant.
2. An algebraic equation determines candidate side ratios. Explain why geometry still has veto power after the algebra is solved.
3. A problem says every allowed triple must be acute. Explain how source selection semantics determine the extremal triple.
4. A ratio-marked cevian lies in a right triangle. Explain how to decide between direct Pythagoras/right-triangle metric and Stewart.
5. Exradius data is replaced by semiperimeter-complement data. Explain why the same reconstruction machinery still works.
6. A synthetic configuration is placed on coordinate axes. Explain what geometric classification must survive the representation change.
7. A learner recognizes similarity in a triangle metric problem. Explain when the GEO-03 route should replace a new metric theorem.
8. A historical item has a verified answer but its exact printed figure is not yet in custody. Explain what may and may not enter learner material.

## E. Six-question assimilation test

Choose one prompt from Section D and answer all six questions before completing a solution.

1. **What did you notice?** State the structural classification.
2. **Why is it legal?** Name the stated/proved fact that earns it.
3. **What is the cheapest first relation?** Write it.
4. **What tempting route are you rejecting?** Explain why.
5. **What discrete/source condition must be preserved?** State it explicitly.
6. **Can you disguise the surface and keep the invariant?** Write a changed-surface version and outline the route.

## Readiness rule

You are not ready merely because you can quote triangle formulas. You are ready when you can reject an impossible triangle immediately, identify the largest side before classification, refuse to infer special-cevian properties from appearance, use special/right-triangle/GEO-03 routes before Stewart when cheaper, delay integer filtering until the real geometry is closed, and preserve exact source selection semantics under transfer.
