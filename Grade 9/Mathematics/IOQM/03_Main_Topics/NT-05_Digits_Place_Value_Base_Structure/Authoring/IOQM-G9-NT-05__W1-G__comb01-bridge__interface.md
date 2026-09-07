---
main_topic_id: IOQM-G9-NT-05
microstream_id: W1-G
microstream_title: Counting Handoff
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-NT-05
prerequisite_interfaces: [NT02, COMB01]
source_cutoff: 2026-09-02
---
# Counting Handoff - Research Interface
## A. Scope boundary
Owns the boundary statement: NT-05 derives arithmetic admissibility; COMB-01 counts admissible strings once the restriction is frozen. Does not derive generic permutations/combinations or inclusion-exclusion.
## B. Learner-state model
Learner may continue doing number theory after the arithmetic condition is complete, or may count before deriving it. Target is a clean two-stage handoff.
## C. Derivation / invariant
A counting universe is meaningful only after the arithmetic predicate defining admissibility is explicit. NT-05 outputs that predicate; COMB-01 C01-10 owns enumeration of the resulting digit strings.
## D. Representations
- arithmetic predicate on digits;
- admissible-set description;
- counting object definition supplied by COMB-01 after handoff.
## E. Decision boundaries
1. derive restriction vs count strings: stop NT work once the predicate is complete;
2. number of values vs number of representations: COMB-01 defines object identity;
3. local digit restrictions vs global arithmetic condition: communicate all constraints before counting.
## F. Misconceptions
- count first and test divisibility later; falsifier overcounts forbidden strings; repair derive arithmetic predicate first.
- NT-05 teaches combinations to finish; falsifier duplicates COMB-01 canon; repair retrieve C01-1..C01-10.
- hand off only a vague phrase like “valid digits”; falsifier counter cannot define objects; repair state exact digit equations/inequalities and leading-zero rule.
## G. First-move cues
“how many digit strings/numbers” after arithmetic structure appears -> first finish and freeze the arithmetic restriction, then invoke counting.
## H. H3->H0 fading
H3 identifies the handoff point; H2 asks whether the predicate is complete; H1 asks “what remains: arithmetic or counting?”; H0 mixed problem requiring autonomous boundary choice.
## I. Source anchors
`IOQM-2025-Q12` illustrates arithmetic restriction/optimization; no historical anchor is used to reteach COMB-01 counting doctrine.
## J. Source-independent traces
Practice P24 and mastery M16 explicitly test the ownership boundary; teacher responses are verbal and checked for semantic correctness.
## K. Contrast candidates
arithmetic structure vs string counting; admissibility predicate vs counted object; modular test vs combinatorial enumeration.
## L. Transfer candidates
multiples with repeated digits, digit-sum constraints, forbidden-digit strings after number-theory filtering.
## M. Mastery candidates
identify handoff, state exact predicate, WHY-NOT early counting, choose correct owner.
## N. Dependencies
CONSUMES COMB-01 stable interface blob `c4d80bfeed3bca5d2b9cc3bd02b1a92fa7b66152`; specifically C01-1,C01-4,C01-10. No counting canon authored here.
## O. Integration notes
Use a visible sentence in the learner book: derive the arithmetic restriction here; count only afterward if asked.
## P. QA state
COMB-01 BOUNDARY PASS; DUPLICATION NONE; >=3 DECISION BOUNDARIES PASS; HANDOFF CUES VERIFIED.
