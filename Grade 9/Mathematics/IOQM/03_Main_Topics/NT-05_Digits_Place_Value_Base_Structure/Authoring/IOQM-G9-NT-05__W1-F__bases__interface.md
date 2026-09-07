---
main_topic_id: IOQM-G9-NT-05
microstream_id: W1-F
microstream_title: Base Representation
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-NT-05
prerequisite_interfaces: [NT02, COMB01]
source_cutoff: 2026-09-02
---
# Base Representation - Research Interface
## A. Scope boundary
Owns positional representation in an arbitrary integer base, digit-range conditions, unknown-base equations, and elementary carries. Generic modular cycles remain NT-02.
## B. Learner-state model
Learner may read a base-b numeral as decimal text. Target is automatic evaluation as a polynomial in the base with digit constraints.
## C. Derivation / invariant
`d_k...d_0` in base `b` equals `sum d_i b^i`, with `0<=d_i<b` and leading digit nonzero. Carries occur when a digit reaches `b`.
## D. Representations
- positional polynomial in `b`;
- repeated-block base-b form;
- carry normalization where coefficients are reduced into `[0,b-1]`.
## E. Decision boundaries
1. subscripted numeral vs decimal numeral: the weights are powers of the stated base;
2. evaluate known base vs solve unknown base: in the latter, form an integer equation plus `b>max digit`;
3. raw coefficient sum vs valid numeral: coefficients >=b require carrying.
## F. Misconceptions
- `352_7=352`; falsifier direct expansion gives 184; repair use `3*7^2+5*7+2`.
- accept base smaller than a displayed digit; falsifier digit not in range; repair impose `b>max digit`.
- write `777_8+1=778_8`; falsifier digit 8 is illegal; repair carry to `1000_8`.
## G. First-move cues
subscript/base language -> write power-of-base expansion; unknown base -> add digit-range inequalities before solving.
## H. H3->H0 fading
H3 labels powers; H2 supplies expansion skeleton; H1 asks what each position weighs; H0 unknown-base/carry problem.
## I. Source anchors
No historical anchor is promoted solely as a base-notation item; this stream is source-independent support for transfer from decimal place value.
## J. Source-independent traces
Practice P11-P13,P22 and mastery M04,M10,M14 independently evaluated.
## K. Contrast candidates
decimal vs base-b reading; known base vs unknown base; coefficient arithmetic vs valid carried numeral.
## L. Transfer candidates
unknown-base palindromes, divisibility rules in other bases, repeated blocks, carry chains.
## M. Mastery candidates
value conversion, reverse conversion, base equation, carry normalization.
## N. Dependencies
REQUIRES positional place value. MAY RETRIEVE NT-02 only for modular applications after expansion.
## O. Integration notes
Teach as a transfer of the decimal model, not as a separate chapter of notation rules.
## P. QA state
DERIVATION PASS; DIGIT-RANGE CONDITIONS CHECKED; >=3 DECISION BOUNDARIES PASS; SOURCE-INDEPENDENT ITEMS VERIFIED.
