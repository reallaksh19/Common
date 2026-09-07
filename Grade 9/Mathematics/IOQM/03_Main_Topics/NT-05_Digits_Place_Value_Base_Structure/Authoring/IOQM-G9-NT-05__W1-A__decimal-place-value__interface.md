---
main_topic_id: IOQM-G9-NT-05
microstream_id: W1-A
microstream_title: Decimal Place Value
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-NT-05
prerequisite_interfaces: [NT02, COMB01]
source_cutoff: 2026-09-02
---
# Decimal Place Value - Research Interface
## A. Scope boundary
Owns numeral-to-polynomial translation in powers of 10 and leading-digit conditions. Does not own generic congruence theory or counting strings.
## B. Learner-state model
Learner reads decimal numerals fluently but may treat digit patterns visually instead of algebraically; bridge is representation choice before arithmetic.
## C. Derivation / invariant
`d_k...d_0 = sum d_i 10^i`; every later digit restriction begins from this equality.
## D. Representations
- expanded place-value polynomial -> exact arithmetic structure;
- block form -> preserve repeated/concatenated structure;
- residue of the expanded value -> only after the place-value equation exists.
## E. Decision boundaries
1. digit pattern vs integer value: expand first;
2. whole-digit expansion vs block representation: preserve blocks when repeated/concatenated;
3. arithmetic restriction vs counting: stop once admissible digits are characterized.
## F. Misconceptions
- reading `abc` as `a*b*c`; falsifier: `123 != 1*2*3`; repair: weights 100,10,1.
- allowing leading zero in a k-digit numeral; falsifier: representation has fewer digits; repair: leading digit nonzero.
- applying a divisibility slogan before representing the numeral; repair: derive from place value.
## G. First-move cues
Named digits -> write the power-of-10 expansion. Repeated blocks -> keep the block as one variable when cheaper.
## H. H3->H0 fading
H3 supplies weights; H2 names place value; H1 asks “what integer is this string?”; H0 changed-surface numeral with no method label.
## I. Source anchors
Primary bridge to `IOQM-2025-Q12`; exact source/key custody in Source Coverage Map and source-audit stream.
## J. Source-independent traces
Practice/mastery place-value identities independently evaluated; teacher answers and metadata reconciled.
## K. Contrast candidates
visual digit pattern vs algebraic numeral; full expansion vs block form; decimal representation vs base-b representation.
## L. Transfer candidates
palindromes, repeated blocks, divisibility derivations, unknown-base equations.
## M. Mastery candidates
unlabelled numeral translation, repeated block, leading-zero trap, choose block vs digit expansion.
## N. Dependencies
REQUIRES school place value. APPLIES NT02 only after translation. HANDOFF to COMB01 only after restriction derived.
## O. Integration notes
Teach as the first representation layer; reuse its vocabulary throughout all later streams.
## P. QA state
DERIVATION PASS; DECISION_BOUNDARIES >=3 PASS; MISCONCEPTION_FALSIFIERS PASS; SOURCE CUSTODY PASS; DEPENDENCY INVERSION NONE.
