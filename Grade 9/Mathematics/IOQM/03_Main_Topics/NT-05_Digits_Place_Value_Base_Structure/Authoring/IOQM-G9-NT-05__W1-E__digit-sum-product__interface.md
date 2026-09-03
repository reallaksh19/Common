---
main_topic_id: IOQM-G9-NT-05
microstream_id: W1-E
microstream_title: Digit Sum and Product
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-NT-05
prerequisite_interfaces: [NT02, COMB01]
source_cutoff: 2026-09-02
---
# Digit Sum and Product - Research Interface
## A. Scope boundary
Owns arithmetic restrictions arising from digit sums and products. Squarefree prime-exponent facts may be retrieved from NT-03; generic prime-factorisation doctrine is not retaught.
## B. Learner-state model
Learner may mix additive and multiplicative digit data. Target is immediate classification: sum questions use additive/place-value structure; product questions use prime compatibility.
## C. Derivation / invariant
Digit sum is additive across positions and controls residue mod 9. A nonzero squarefree digit product has every prime exponent at most 1 across all non-one digits; digit 1 may repeat freely.
## D. Representations
- digit-sum expression: additive restriction;
- prime-support/exponent view of each digit: multiplicative restriction;
- compatibility list of allowed simultaneous non-one digits.
## E. Decision boundaries
1. sum vs product: additive residue/carry versus prime exponents;
2. squarefree product vs squarefree individual digits: compatibility must hold across all digits, not separately;
3. arithmetic restriction vs maximizing/counting strings: first classify digits, then optimize/count using the relevant owner.
## F. Misconceptions
- digits 2 and 6 are individually squarefree so may coexist; falsifier product has `2^2`; repair combine prime exponents globally.
- digit 4 allowed because it is one digit; falsifier `4=2^2`; repair test the digit’s own factorization.
- ones are useless in a length maximum; falsifier multiplying by 1 preserves product; repair separate neutral digits from prime-consuming digits.
## G. First-move cues
“digit sum” -> additive expression/carry; “digit product squarefree” -> list prime factors used by non-one digits.
## H. H3->H0 fading
H3 supplies digit factorizations; H2 asks which prime repeats; H1 asks sum-or-product structure; H0 gives a length/compatibility problem without labels.
## I. Source anchors
`IOQM-2023-Q19=92` primary: squarefree product limits prime usage; product 210 plus 88 ones achieves the optimum. `IOQM-2025-Q12=33` also uses digit restrictions and optimization.
## J. Source-independent traces
Practice P09,P10,P20,P21 and mastery M06,M15 independently checked.
## K. Contrast candidates
digit sum vs digit product; individually squarefree digits vs globally squarefree product; arithmetic classification vs combinatorial counting.
## L. Transfer candidates
cube-free products, fixed digit-product support, maximizing length with neutral digits.
## M. Mastery candidates
compatibility decision, forbidden digit, maximum repeated non-one digit, WHY-NOT pairwise oversight.
## N. Dependencies
RETRIEVES NT-03 squarefree/exponent facts only. APPLIES decimal digit structure. HANDOFF counting to COMB-01.
## O. Integration notes
Explicitly contrast with divisibility-by-9 so “digit sum” language does not trigger product reasoning and vice versa.
## P. QA state
DERIVATIONS PASS; NT-03 BOUNDARY PASS; >=3 DECISION BOUNDARIES PASS; SOURCE VERIFIED; AUTHORED ANSWERS CHECKED.
