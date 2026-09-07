---
main_topic_id: IOQM-G9-NT-05
microstream_id: W1-D
microstream_title: Carrying
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-NT-05
prerequisite_interfaces: [NT02, COMB01]
source_cutoff: 2026-09-02
---
# Carrying - Research Interface
## A. Scope boundary
Owns arithmetic effects of decimal carries on digit sums, especially successor changes. Does not own generic finite-state recurrence or modular-cycle theory.
## B. Learner-state model
Learner can add 1 but tends to recompute examples. Target is recognition that only the number of trailing 9s controls the digit-sum jump.
## C. Derivation / invariant
If `n` has exactly `t` trailing 9s, adding 1 replaces those `t` nines by zeros and raises the preceding digit by 1, so `s(n+1)=s(n)+1-9t`.
## D. Representations
- column addition picture: explains the carry chain;
- trailing-9 count `t`: compresses the state;
- digit-sum difference equation: reconstructs `t` from observed sums.
## E. Decision boundaries
1. no trailing 9 vs one or more: increase by 1 versus a drop;
2. local carry chain vs generic modular residue: use the exact local structure when successor is involved;
3. digit sum change vs numerical difference: the number rises by 1 while digit sum can fall greatly.
## F. Misconceptions
- digit sum always rises after +1; falsifier `19->20`; repair count trailing 9s.
- each carry subtracts 10 from digit sum; falsifier one 9 becomes 0 while preceding digit gains 1; repair net `-9` per trailing 9 plus initial `+1`.
- infer carry length from final zeros alone without stated exactness; repair track the pre-increment trailing 9s.
## G. First-move cues
“n and n+1”, “digit sum changes after adding 1”, terminal 9-pattern -> set `t` equal to number of trailing 9s.
## H. H3->H0 fading
H3 marks changed digits; H2 supplies `t`; H1 asks which digits change; H0 asks for an inverse carry-length reconstruction.
## I. Source anchors
Primary anchor `IOQM-2024-Q08=49`; independent route uses the carry identity plus divisibility restrictions to identify the least admissible number.
## J. Source-independent traces
Practice P06-P08,P19 and mastery M02,M07,M11 independently recomputed.
## K. Contrast candidates
carry invariant vs brute force; digit sum vs number value; successor carry vs generic power cycle.
## L. Transfer candidates
adding powers of 10, base-b carry chains, reconstructing suffix length from digit-sum jump.
## M. Mastery candidates
forward change, inverse `t`, base-b analogue, WHY-NOT “always +1”.
## N. Dependencies
REQUIRES decimal place value and school addition. No COMB-03 recurrence teaching.
## O. Integration notes
Position after concatenation so place-value changes are already familiar; keep `t` notation local and concrete.
## P. QA state
DERIVATION PASS; DECISION_BOUNDARIES >=3 PASS; FALSIFIERS PASS; SOURCE VERIFIED; DEPENDENCY CONFLICTS NONE.
