---
main_topic_id: IOQM-G9-NT-04
microstream_id: W3-B
microstream_title: GCD, parity and divisibility filters
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-NT-04
prerequisite_interfaces: [NT01_Stable_Prerequisite_Interface, NT03_Stable_Divisor_PerfectPower_Interface_v1]
source_cutoff: 2026-09-02
---

# GCD, parity and divisibility filters - Research Interface

## A. Scope boundary
Included: using parity, gcd and divisibility as filters after a structural relation has been found; whole-branch elimination and coprimality consequences. Excluded: full Euclidean/gcd teaching (NT-01), prime-factorisation doctrine (NT-03), and modular-cycle doctrine (NT-02).

## B. Learner-state model
`PRIOR_KNOWLEDGE:` even/odd arithmetic, gcd, divisibility.

`LIKELY_HALF_KNOWLEDGE:` learner checks parity late instead of using it to cut cases early.

`MISSING_BRIDGES:` derive a divisibility consequence before enumerating; normalize gcd information; separate a necessary filter from a complete solution.

`OWNERSHIP_TARGET:` use cheap integer filters early enough to shrink a proved candidate set.

## C. Mathematical invariant / governing structure
**Invariant:** `CHEAP NECESSARY CONDITIONS FIRST`: parity, gcd and divisibility can delete entire branches before expensive reconstruction.

If an equation implies `d | N`, every solution must use `d` from the divisor set of `N`. If `gcd(u,v)=1` and `uv=N`, NT-03's block rule may force prime-power blocks wholly to one side. Parity is often a factor-pair condition: if a sum is odd the terms have opposite parity; squares are 0 or 1 mod 4. These are necessary conditions; survivors still return to the original equation.

## D. Representation inventory
| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| `d | N` | finite divisor filter | list relevant divisors | `d!=0` where needed | scan d values |
| `gcd(u,v)=1, uv=N` | whole prime-power allocation | retrieve NT-03 block rule | exact gcd condition | split a prime power |
| parity of sum/product | branch elimination | label parity before cases | integer variables | perform full algebra first |
| linear combination | gcd divisor | take gcd into a combination | divisibility direction | assume converse |

## E. Decision boundaries
| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| parity statement | eliminate branches | enumerate all branches | Does parity decide before values? | enumeration feels concrete |
| gcd plus product | whole blocks | arbitrary factor split | Is gcd exactly 1? | all factor pairs look allowed |
| `d|N` | necessary candidate set | conclude solution | Are other original constraints left? | divisibility feels decisive |
| congruence-like parity | simple parity | full modular arithmetic | Is modulus 2/4 enough? | NT-02 is more powerful than needed |

## F. Misconception / diagnosis catalogue
`NT04-FIL-01`
- WRONG_MOVE: do all factor pairs then test parity.
- WHY_TEMPTING: factor enumeration is already finite.
- MISSING_LINK_CLASS: DISCRETE_FILTER.
- REPAIR_INVARIANT: apply the cheapest necessary filter first.
- FALSIFIER_OR_CONTRAST: parity can halve or annihilate branches immediately.

`NT04-FIL-02`
- WRONG_MOVE: from `d|N`, declare every divisor a solution.
- WHY_TEMPTING: transformed condition is simple.
- MISSING_LINK_CLASS: DOMAIN_CONDITION.
- REPAIR_INVARIANT: divisor relation generates candidates only.
- FALSIFIER_OR_CONTRAST: order/positivity can reject most divisors.

`NT04-FIL-03`
- WRONG_MOVE: split a prime power between coprime factors.
- WHY_TEMPTING: exponent splitting is valid without gcd=1.
- MISSING_LINK_CLASS: PREREQUISITE.
- REPAIR_INVARIANT: retrieve NT-03 whole-block rule.
- FALSIFIER_OR_CONTRAST: `2^3` cannot contribute a factor 2 to both coprime sides.

## G. First-move cues
- "gcd=1 and product fixed" -> allocate whole prime-power blocks.
- "sum odd/even" -> write parity of each factor before values.
- "integer quotient" -> write the corresponding divisibility statement.
- "square" -> retrieve an allowed parity/residue signature only if it kills branches cheaply.

## H. H3 -> H0 fading plan
- **H3:** factor pairs of 72 under gcd=1; allocate blocks explicitly.
- **H2:** product fixed plus sum odd; identify parity before listing.
- **H1:** an integer quotient appears; ask for the divisor relation only.
- **H0:** changed-surface reconstruction where gcd and a bound jointly leave one factor pair.

## I. Validated IOQM source anchors
Supportive roles in `IOQM-2024-Q13`, `IOQM-2023-Q04`, and `IOQM-2023-Q11`; stable answers are 19, 07, and 14 respectively.

## J. Source-independent mathematical trace
- 2024-Q13 uses `c-1|65` to make c finite.
- 2023-Q04 uses `x-1|2` after applying the exact-source `x^4` correction.
- 2023-Q11 uses sign/parity of factor pairs of 231 to reconstruct integer roots.
No new historical answer is introduced by this stream.

## K. Contrast-pair candidates
1. necessary divisibility vs sufficient solution;
2. parity first vs parity after enumeration;
3. gcd=1 product allocation vs unrestricted factor pair;
4. modulus 2/4 filter vs unnecessary modular machinery;
5. prime-factor retrieval vs re-teaching NT-03.

## L. Transfer candidates
- **T2:** consecutive integers with product divisible by a fixed prime power.
- **T2:** signed factor pairs filtered by parity.
- **T3:** integer geometry where parity rejects a metric candidate.
- **T4:** gcd filter followed by discriminant-square reconstruction.

## M. Candidate mastery items
- Recognition: mark which conditions are cheapest filters.
- First-line: reduce `(x^4+1)/(x-1)` integrality to `x-1|2`.
- Full solve: coprime positive integers `uv=360`, minimize `u+v`.
- WHY-NOT: explain why `gcd(u,v)=1` does not mean both are prime.
- Verification: identify divisor candidates that fail an original inequality.

## N. Dependency declarations
`REQUIRES:` NT-01 gcd/divisibility; NT-03 prime-block rule.

`BRIDGE_REQUIRES:` factor-pair generator from W3-A.

`APPLIES:` parity and gcd without owning their basic theory.

`EXPORTS:` cheap-filter ordering and candidate-vs-solution discipline.

## O. Lead integration notes
Use this immediately after factor-pair generation. It must not become a chapter of divisibility rules. The integrated book should repeatedly ask "what is the cheapest necessary filter?" and compress borrowed arithmetic facts to one-line retrieval cues.

## P. Independent QA status
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: NONE
