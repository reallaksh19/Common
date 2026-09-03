---
main_topic_id: IOQM-G9-NT-05
microstream_id: W1-C
microstream_title: Concatenation
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-NT-05
prerequisite_interfaces: [NT02, COMB01]
source_cutoff: 2026-09-02
---
# Concatenation - Research Interface
## A. Scope boundary
Owns conversion of appended/repeated decimal blocks into `10^k x+y` and factored repeat forms. Generic congruence laws remain NT-02; counting resulting strings remains COMB-01.
## B. Learner-state model
Learner can visually join blocks but may not encode block length algebraically. Target state: shift the left block by the exact power of 10 before any divisibility work.
## C. Derivation / invariant
Appending a `k`-digit block `y` to integer block `x` gives `N=10^k x+y`. Repeating a two-digit block gives `101x`; repeating a three-digit block twice gives `1001x`.
## D. Representations
- digit-by-digit expansion: useful only when individual digits matter;
- block form `10^k x+y`: exposes concatenation directly;
- factored repeated-block form: exposes fixed divisors such as 101 and 1001.
## E. Decision boundaries
1. appended block vs arithmetic sum: use a base shift, not `x+y`;
2. digit expansion vs block form: preserve blocks when the divisor mentions whole blocks;
3. arithmetic divisibility vs string counting: derive the divisibility condition before any count.
## F. Misconceptions
- `37` followed by `42` as `37+42`; falsifier: written numeral is 3742; repair multiply 37 by 100.
- use wrong shift for leading-zero-capable block; falsifier: block width is part of representation; repair fix `k` from stated width.
- expand every digit and hide a repeated-block factor; falsifier: `123123=1001*123`; repair retain block variable.
## G. First-move cues
“followed by”, “concatenate”, “repeat the block” -> identify block width and write `10^k x+y`.
## H. H3->H0 fading
H3 supplies the shift; H2 asks for block width; H1 asks for the first algebraic line; H0 gives a novel repeated-block divisibility problem without a label.
## I. Source anchors
Primary anchor `IOQM-2024-Q18=13`: represent the printed four-digit value as `100p+q=99p+(p+q)` before applying gcd/divisibility restrictions.
## J. Source-independent traces
Practice P04,P05,P17,P18 and mastery M03,M09,M12 were independently evaluated and reconciled with the teacher key.
## K. Contrast candidates
concatenation vs addition; block form vs digit expansion; repeated block vs digit permutation.
## L. Transfer candidates
repeated blocks in other bases; divisibility of `xx`; concatenation under a divisor involving both blocks.
## M. Mastery candidates
unknown block width, repeated three times, modulo a block-sum divisor, WHY-NOT wrong power of 10.
## N. Dependencies
REQUIRES decimal place value. APPLIES NT-02 legality after representation. HANDOFF to COMB-01 only if counting is requested.
## O. Integration notes
Teach after divisibility tests; reuse block notation later without reteaching place value.
## P. QA state
DERIVATION PASS; DECISION_BOUNDARIES >=3 PASS; MISCONCEPTION FALSIFIERS PASS; SOURCE ANCHOR VERIFIED; DEPENDENCY INVERSION NONE.
