---
main_topic_id: IOQM-G9-ALG-07
microstream_id: W1-A
microstream_title: Definition and order structure
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-ALG-07
prerequisite_interfaces: []
source_cutoff: 2026-08-31
---

## A. Scope boundary
Included: floor/ceiling definitions as order statements and half-open intervals. Excluded: general inequality optimization (ALG-02), counting applications (W1-F), source custody (W1-G).

## B. Learner-state model
PRIOR_KNOWLEDGE: ordering real numbers; consecutive integers.
LIKELY_HALF_KNOWLEDGE: remembers examples such as floor(3.7)=3.
MISSING_BRIDGES: definition as an interval encoder.
OWNERSHIP_TARGET: automatic translation between a discrete value and its half-open interval.

## C. Mathematical invariant / governing structure
`floor(x)=n <=> n<=x<n+1` and `ceil(x)=n <=> n-1<x<=n` for integer n. These follow directly from greatest-integer-not-exceeding and least-integer-not-below definitions.

## D. Representation inventory
| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| floor equation | left-closed/right-open interval | write `n<=x<n+1` | n integer | replace by ordinary equality |
| ceiling equation | left-open/right-closed interval | write `n-1<x<=n` | n integer | reverse strict endpoint |
| number line | endpoint inclusion | mark brackets first | ordered endpoints | decimal deletion |

## E. Decision boundaries
| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| floor vs ordinary equality | interval | single value | does the symbol collapse a unit interval? | familiar algebra reflex |
| floor vs ceiling | lower anchor | upper anchor | is the integer below or above x? | symmetric notation |
| included vs excluded endpoint | closed | open | which defining inequality is strict? | endpoint neglect |

## F. Misconception/diagnosis catalogue
ERROR_CODE: ALG07-A-01
WRONG_MOVE: `floor(f(x))=n` becomes `f(x)=n`.
WHY_TEMPTING: equation-solving habit.
MISSING_LINK_CLASS: REPRESENTATION
REPAIR_INVARIANT: decode to a half-open interval first.
FALSIFIER_OR_CONTRAST: `floor(4.8)=4` although `4.8!=4`.

## G. First-move cues
Visible integer output from floor: write `n<=...<n+1`. Visible integer output from ceiling: write `n-1<...<=n`.

## H. H3 -> H0 fading plan
H3: supply the full double inequality. H2: cue “half-open interval.” H1: cue the strict endpoint only. H0: changed-surface floor/ceiling equation with no hint.

## I. Validated IOQM source anchors
| Stable ID | Year/Q | Source status | Primary/bridge role | Mechanism | Figure? | Key status |
|---|---|---|---|---|---|---|
| IOQM-2024-Q21 | 2024 Q21 | HBCSE_OFFICIAL | primary | invert floor constraints | no | verified |
| IOQM-2024-Q26 | 2024 Q26 | HBCSE_OFFICIAL | primary | set n=floor(x), enforce interval feasibility | no | verified |

## J. Source-independent mathematical trace
Q21 and Q26 are independently recomputed in `01_Source_Coverage_Map.md`; results 91 and 33 agree with the official key. No unresolved domain or source issue applies to this stream.

## K. Contrast-pair candidates
floor vs equality; floor vs ceiling; included vs excluded endpoint; integer output vs real input interval; positive example vs negative example.

## L. Transfer candidates
T2 symbol-to-number-line; T2 interval-to-symbol; T3 integer timestamp interpretation; T3 shifted input; T4 use as final discrete filter in NT/COMB.

## M. Candidate mastery items
Recognition: identify the correct half-open interval. First-line: translate a floor equation only. Full solve: linear floor equation. WHY-NOT: explain why ordinary equality loses solutions. Verification: test both endpoints.

## N. Dependency declarations
REQUIRES: order on reals. BRIDGE_REQUIRES: elementary linear inequality manipulation. APPLIES: half-open interval notation. Downstream may assume exact floor/ceiling interval definitions.

## O. Lead integration notes
Teach definitions once globally, then retrieve. Keep microstream/control labels out of student prose. Place before negative-input, transformation, equation and counting streams.

## P. Independent QA status
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: none affecting integration
