---
main_topic_id: IOQM-G9-ALG-06
microstream_id: W1-A
microstream_title: Exponent normalization and common bases
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-ALG-06
prerequisite_interfaces:
  - ALG01_Stable_Prerequisite_Interface_v1.md
source_cutoff: 2026-09-03
---
# W1-A — Exponent Normalization and Common Bases

## A. Scope boundary
Included: integer/rational exponent laws on admissible positive bases, rewriting to a common base, extracting exponent equations, and deciding when a logarithm is unnecessary. Excluded: logarithm-domain canon (W1-E), radical principal-value doctrine (W1-B/W1-D), and polynomial factorisation teaching owned by ALG-01/03.

## B. Learner-state model
```text
PRIOR_KNOWLEDGE: routine laws such as a^m a^n=a^(m+n).
LIKELY_HALF_KNOWLEDGE: manipulates exponents but changes bases inconsistently or ignores zero/negative-base conditions.
MISSING_BRIDGES: normalize before expanding; identify a common positive base; distinguish equality of powers from equality of exponents.
OWNERSHIP_TARGET: TARGET -> COMMON STRUCTURE -> DOMAIN -> EXPONENT RELATION -> CHECK.
```

## C. Mathematical invariant / governing structure
For a fixed base `b>0`, `b!=1`, the map `x -> b^x` is one-to-one. Therefore `b^u=b^v ⇔ u=v`. Rewriting is valid only when both sides are represented by the same admissible base and the rewrite preserves the original domain.

Proof reconstruction: if `b>1`, powers increase strictly; if `0<b<1`, they decrease strictly. Thus equal powers have equal exponents. Integer-base IOQM items usually exploit exact factorisation such as `8=2^3`, `27=3^3`, not logarithms.

## D. Representation inventory
| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| prime-power base | exponent linearity | factor bases | positive bases | take logs immediately |
| reciprocal base | sign of exponent | write `1/b=b^-1` | `b!=0` | invert one side only |
| rational exponent | root/exponent link | state positivity/domain | real-valued interpretation | cancel denominators blindly |
| logarithmic fallback | exponent as unknown | use only if no common exact base | log domain valid | introduce decimals |

## E. Decision boundaries
| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| powers of 4 and 8 | common base 2 | logarithm | can every base be rewritten exactly? | logs feel universal |
| `a^x=a^y` | compare exponents | divide powers | is `a>0,a!=1` known? | exponent cancellation is memorized |
| negative base integer exponents | parity/case route | real logarithm | are exponents guaranteed integers? | notation looks identical |
| sum of powers | factor first | compare exponents | is equality termwise? | equal-base rule is overgeneralized |

## F. Misconception/diagnosis catalogue
```text
ERROR_CODE: ALG06-EXP-01
WRONG_MOVE: from 2^x+2^y=2^z conclude x+y=z.
WHY_TEMPTING: multiplication exponent law is misapplied to addition.
MISSING_LINK_CLASS: INVARIANT
REPAIR_INVARIANT: factor a common power; exponent laws act on products/quotients.
FALSIFIER_OR_CONTRAST: 2+2=4 but 1+1!=2 as an exponent law.

ERROR_CODE: ALG06-EXP-02
WRONG_MOVE: compare exponents with base 1 or an inadmissible real base.
WHY_TEMPTING: the equal-base rule is remembered without conditions.
MISSING_LINK_CLASS: DOMAIN_CONDITION
REPAIR_INVARIANT: write `base>0, base!=1` before using injectivity.
FALSIFIER_OR_CONTRAST: 1^3=1^9.
```

## G. First-move cues
- bases `4,8,32` -> write all as powers of `2`.
- reciprocal powers -> move sign into the exponent before solving.
- sum/difference of same-base powers -> factor the smallest power first.
- no exact common base -> only then consider W1-E logarithm conversion.

## H. H3 -> H0 fading plan
- H3: “Rewrite `8^(x-1)` as `2^(3x-3)`.”
- H2: “Put both sides on one base.”
- H1: only display mixed exact powers such as `4^x` and `8^(x-1)`.
- H0: changed-surface equation mixing a reciprocal power and a product; learner chooses common-base normalization independently.

## I. Validated IOQM source anchors
No historical anchor is promoted solely by this stream. `IOQM-2023-Q02` uses exponent relations after logarithm conversion and is owned jointly by W1-E/W1-G.

## J. Source-independent mathematical trace
No numerical historical answer promoted here. The common-base rules above were independently reconstructed from monotonicity/injectivity and algebraic exponent laws.

## K. Contrast-pair candidates
1. common base vs logarithm;
2. product of powers vs sum of powers;
3. positive fixed base vs base `1`;
4. integer exponent on negative base vs real exponent;
5. exact symbolic normalization vs decimal approximation;
6. cross-stream: exponent normalization vs radical rationalisation.

## L. Transfer candidates
- T2 representation: `9^x=27^(x-1)` -> base 3.
- T2 context: growth-rate statement -> exact power equation.
- T3 discrete: integer exponent plus divisibility condition.
- T4 cross-domain: geometric scale factors expressed as powers.

## M. Candidate mastery items
- recognition: choose the cheapest route for `16^x=8^(x+2)`.
- first-line: write the first normalized line for `1/27^x=3^(2-x)`.
- full solve: mixed exact powers with one factored sum.
- WHY-NOT: explain why `2^x+2^x=2^(2x)` is false.
- verification: identify the missing base condition in a proposed proof.

## N. Dependency declarations
`REQUIRES`: ALG-01 equivalence and factor/transform habits.  
`BRIDGE_REQUIRES`: elementary integer factorisation.  
`APPLIES`: monotonicity/injectivity of positive exponential functions.  
Downstream may assume learners normalize exact powers before reaching for logs.

## O. Lead integration notes
Teach the route rule once near the topic opening. Compress routine exponent laws into retrieval; do not make a school-style formula chapter. Keep negative-base real-exponent edge cases teacher-side unless an item needs them. Place before radicals and logs.

## P. Independent QA status
```text
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: NOT_RUN
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: none affecting integration
```
