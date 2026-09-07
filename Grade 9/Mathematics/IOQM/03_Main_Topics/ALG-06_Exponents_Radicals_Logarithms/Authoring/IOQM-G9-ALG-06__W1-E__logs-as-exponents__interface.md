---
main_topic_id: IOQM-G9-ALG-06
microstream_id: W1-E
microstream_title: Logarithms as exponents
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-ALG-06
prerequisite_interfaces:
  - ALG01_Stable_Prerequisite_Interface_v1.md
source_cutoff: 2026-09-03
---
# W1-E — Logarithms as Exponents

## A. Scope boundary
Included: `log_b a=x ⇔ b^x=a`, base/argument domain, reciprocal logs, product/power laws only as consequences of exponent meaning, and choosing common-base algebra before logs. Excluded: calculus, change-of-base numerics, graph theory of logarithmic functions, and broad transcendental equation solving.

## B. Learner-state model
```text
PRIOR_KNOWLEDGE: may have seen log notation or exponent rules.
LIKELY_HALF_KNOWLEDGE: memorizes log laws without knowing domain or exponent meaning.
MISSING_BRIDGES: log is an exponent; base and argument conditions; reciprocal relation; common-base route is often cheaper.
OWNERSHIP_TARGET: DOMAIN -> READ AS EXPONENT -> NORMALIZE/RECIPROCAL -> ALGEBRA -> INTEGER FILTER.
```

## C. Mathematical invariant / governing structure
For `b>0`, `b!=1`, `a>0`, `log_b a=x` means exactly `b^x=a`. Therefore, when `a,b>0` and neither is `1`, `log_a b * log_b a=1`. The standard log laws are exponent laws transported through this definition.

## D. Representation inventory
| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| exponent statement | concrete meaning | rewrite `log_b a=x` as `b^x=a` | valid base/argument | manipulate symbols first |
| reciprocal pair | one variable `t` | set `t=log_a b` | `a,b>0`, `a,b!=1` | treat logs as independent |
| common exact base | linear exponent relation | avoid logs | exact base exists | use change-of-base decimals |
| integer power relation | count admissible pairs | convert `t=k` to `b=a^k` | integer bounds | count real solutions |

## E. Decision boundaries
| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| `8^x=4^y` | common base | logs | exact base available? | logs are associated with exponents |
| `log_a b` and `log_b a` | reciprocal substitution | two variables | are bases/arguments mutually swapped? | notation looks different |
| `log_b(X)=c` | exponent conversion | log-law expansion | is one log isolated? | memorized laws |
| integer `a,b` after `t=2` | power counting | continuous analysis | does `b=a^2` close the problem? | exponent variable feels abstract |

## F. Misconception/diagnosis catalogue
```text
ERROR_CODE: ALG06-LOG-01
WRONG_MOVE: use a logarithm with nonpositive argument or base 1.
WHY_TEMPTING: domain is treated as afterthought.
MISSING_LINK_CLASS: DOMAIN_CONDITION
REPAIR_INVARIANT: before any log step record base>0, base!=1, argument>0.
FALSIFIER_OR_CONTRAST: log_1(5) is not defined.

ERROR_CODE: ALG06-LOG-02
WRONG_MOVE: log(a+b)=log a+log b.
WHY_TEMPTING: product law is overextended to addition.
MISSING_LINK_CLASS: INVARIANT
REPAIR_INVARIANT: log laws come from multiplication of powers, not addition.
FALSIFIER_OR_CONTRAST: base 10 with a=b=1.
```

## G. First-move cues
- reciprocal log pair -> `t=log_a b`, then `log_b a=1/t`.
- isolated logarithm -> convert to exponent form.
- exact power bases -> route back to W1-A instead of adding logs.
- integer bounds after exponent relation -> hand off to W1-F discrete count.

## H. H3 -> H0 fading plan
- H3: convert supplied logs to exponent statements.
- H2: cue “one log variable; use reciprocity.”
- H1: show only swapped-base log pair.
- H0: integer-bounded log equation where learner discovers the reciprocal substitution and counts power pairs.

## I. Validated IOQM source anchors
| Stable ID | Year/Q | Source status | Primary/bridge role | Mechanism | Figure? | Key status |
|---|---|---|---|---|---|---|
| IOQM-2023-Q02 | 2023/Q02 | CLEAN_VALIDATED | primary | reciprocal logarithms + integer power counting | no | HBCSE-linked embedded key; independently verified 54 |

## J. Source-independent mathematical trace
For `2<=a,b<=2023`, set `t=log_a b>0`. Then `log_b a=1/t`, so `t+6/t=5 ⇔ t^2-5t+6=0`, giving `t=2,3`. For `b=a^2`, `a=2..44`: 43 pairs. For `b=a^3`, `a=2..12`: 11 pairs. Total 54; official/verification answer agrees.

## K. Contrast-pair candidates
1. log as exponent vs memorized symbol laws;
2. common base vs logarithm;
3. reciprocal logs vs independent variables;
4. legal product law vs illegal sum law;
5. real exponent solution vs integer pair count;
6. cross-stream: log-domain restrictions vs radical-domain restrictions.

## L. Transfer candidates
- T2: `log_x 16=4` -> exponent equation plus base domain.
- T2: swapped logs with coefficients changed.
- T3: exponent result followed by divisor/integer bounds.
- T4: geometric growth ratio represented as a log, then returned to exact powers.

## M. Candidate mastery items
- recognition: choose common base or log for four equations.
- first-line: state full domain for `log_(x-1)(x+3)`.
- full solve: reciprocal-log equation with integer bounds.
- WHY-NOT: diagnose `log(a+b)` expansion.
- verification: check whether a proposed base satisfies `b>0,b!=1`.

## N. Dependency declarations
`REQUIRES`: W1-A exponent normalization; ALG-01 equivalence discipline.  
`BRIDGE_REQUIRES`: W1-D domain/reversibility ledger.  
`APPLIES`: integer filters in W1-F.  
Downstream may assume log notation is read through exponent meaning and domain is recorded before use.

## O. Lead integration notes
Keep the learner chapter narrow: logs are a representation, not a formula list. Introduce only after common-base exponent work, so learners can consciously decide when a log is unnecessary. Q02 is the canonical source anchor.

## P. Independent QA status
```text
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: none affecting integration
```
