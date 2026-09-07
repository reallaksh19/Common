---
main_topic_id: IOQM-G9-NT-05
microstream_id: W1-B
microstream_title: Divisibility by 9 and 11
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-NT-05
prerequisite_interfaces: [NT02, COMB01]
source_cutoff: 2026-09-02
---
# Divisibility by 9 and 11 - Research Interface
## A. Scope boundary
Owns derivation of decimal digit tests from place value. Generic modular laws/cycles remain NT-02 retrieval-only.
## B. Learner-state model
Learner may remember tests without knowing why signs/order work; target is reconstructability from powers of 10.
## C. Derivation / invariant
Modulo 9, `10^i` leaves 1, so numeral and digit sum agree. Modulo 11, `10` leaves -1, so signs alternate.
## D. Representations
expanded numeral; digit-sum form; alternating-sum form.
## E. Decision boundaries
1. mod 9 -> ordinary digit sum, not alternating;
2. mod 11 -> alternating sum, not ordinary sum;
3. place-value test vs generic power cycle -> use local power-of-10 collapse, retrieve cycle machinery only if truly needed.
## F. Misconceptions
- using digit sum for 11; falsifier: 121 has sum 4 but is divisible by 11; repair alternating signs.
- forgetting sign orientation matters only up to overall sign; repair verify divisibility of zero residue.
- treating memorized test as unexplained magic; repair derive from `10 ≡ 1` or `-1`.
## G. First-move cues
“divisible by 9/11” + digit string -> expand powers of 10 mentally and collapse.
## H. H3->H0 fading
H3 shows residues of powers; H2 names sum/alternating sum; H1 asks which collapse applies; H0 mixed 9/11 numeral with no label.
## I. Source anchors
Supports `IOQM-2025-Q12`; other anchors use adjacent place-value/carry/product mechanisms.
## J. Source-independent traces
All authored remainders and divisibility answers independently recomputed.
## K. Contrast candidates
9 vs 11; digit sum vs digit product; place-value reduction vs generic modular cycle.
## L. Transfer candidates
palindromes, repeated digits, simultaneous divisibility, base-dependent analogues.
## M. Mastery candidates
derive both restrictions for one numeral; WHY-NOT wrong test; simultaneous 9-and-11 filter.
## N. Dependencies
REQUIRES decimal place value; APPLIES frozen NT02 congruence legality without reteaching it.
## O. Integration notes
Teach immediately after place value so tests are consequences, not isolated mnemonics.
## P. QA state
DERIVATION PASS; >=3 DECISION BOUNDARIES PASS; MISCONCEPTION FALSIFIERS PASS; SOURCE CHECK PASS; DEPENDENCY INVERSION NONE.
