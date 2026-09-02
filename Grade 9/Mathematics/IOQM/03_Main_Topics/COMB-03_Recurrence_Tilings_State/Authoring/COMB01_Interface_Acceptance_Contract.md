# COMB-03 <- COMB-01 Interface Acceptance Contract

Status: `ACCEPTED_CURRENT_CORPUS`
Consumer: `IOQM-G9-COMB-03`
Provider: `IOQM-G9-COMB-01`
Provider artifact: `Grade 9/Mathematics/IOQM/03_Main_Topics/COMB-01_Basic_Counting_Restrictions_Inclusion_Exclusion/Authoring/COMB01_Stable_Counting_Model_Interface_v1.md`
Provider blob at acceptance: `c4d80bfeed3bca5d2b9cc3bd02b1a92fa7b66152`
Accepted against production base: `47af427f65a3370676931f885df09494524b9424`

This is a consumer-side evidence record. COMB-03 retrieves the provider semantics below; it does not recreate COMB-01 teaching.

## C01-1 through C01-10 evidence table

| ID | Exact provider section | Required semantic contract | Concrete COMB-03 consumption point | Result | Adaptation |
|---|---|---|---|---|---|
| C01-1 | `Minimum provider payload / C01-1 — Counted-object definition` | define one valid object/outcome and identity before counting | every state definition; tilings count canonical partial configurations, not construction-history labels | PASS | extend object identity to **state identity**: histories merge only when remembered data gives identical future legality |
| C01-2 | `C01-2 — Addition principle semantics` | add only disjoint case counts | first/last transition recurrence terms | PASS | recurrence branches are added only after a disjointness proof |
| C01-3 | `C01-3 — Multiplication principle semantics` | stage counts are conditional on earlier choices | weighted/multi-choice transitions inside one recurrence branch | PASS | transition weight is attached only after prior state fixes the choices available at that stage |
| C01-4 | `C01-4 — Exhaustiveness discipline` | every valid object enters at least one case; disjoint + exhaustive means exactly one | branch-validation question for every recurrence derivation | PASS | exact consumer check retained verbatim: `Does every valid object enter exactly one branch?` |
| C01-5 | `C01-5 — Ordered vs unordered decision` | swapping roles changes the object iff order is structural | state identity, path vs state counting, Q21 partition representation | PASS | identity decision remains provider retrieval; COMB-03 only checks whether its state representation preserves that identity |
| C01-6 | `C01-6 — Direct vs complement decision` | use universe-complement when negation is simpler under same object definition | router decision: recurrence vs direct/complement representation | PASS | no complement lesson; one decision cue only |
| C01-7 | `C01-7 — Restriction vocabulary` | distinguish allowed/forbidden choice; local/global restrictions; state memory | previous-tile flag, boundary occupancy, carry, residual resource coordinates | PASS | `state memory / remembered condition` is the exact bridge into minimal-sufficient-state design |
| C01-8 | `C01-8 — Inclusion-exclusion boundary` | overlapping cases cannot be naively added; redesign or route to counting owner | recurrence branch overlap diagnosis | PASS | fail closed: no recurrence is written until branches are disjoint; generic IE routes back to COMB-01 |
| C01-9 | `C01-9 — Repeated-object distinction` | indistinguishability is determined by whether swapping copies changes the counted object | tiling/resource representations with identical pieces | PASS | no repeated-object formula derivation; only identity retrieval when defining the state/object |
| C01-10 | `C01-10 — Digit-string counting boundary` | COMB-01 counts admissible strings once arithmetic rule is known; NT digit owner derives arithmetic rule | carry-state representations such as Q26 | PASS | COMB-03 owns state/carry transition once the arithmetic constraint is supplied; it does not derive decimal/divisibility doctrine |

Result: `C01_ACCEPTANCE = PASS_10_OF_10`.

## T1 through T6 executed compatibility tests

| Test | Concrete COMB-03 evidence | Result |
|---|---|---|
| T1 — retrieval, not reteaching | planned prose uses a one-line retrieval such as “these first-step cases are disjoint, so add their counts”; no addition/multiplication chapter appears in the blueprint | PASS |
| T2 — exact-one-branch | every recurrence derivation must answer the provider question `Does every valid object enter exactly one branch?`; the tiling branch router and QA gate use this exact test | PASS |
| T3 — ordered/unordered stability | Q21/partition and path/state representations retain C01-5 identity semantics; COMB-03 does not introduce `nPr`/`nCr` as the deciding rule | PASS |
| T4 — overlap fail-closed | `CASES_OVERLAP` is a blocking recurrence defect; the repair is redesign into disjoint states or route generic IE to COMB-01, never local IE teaching | PASS |
| T5 — restriction handoff | State Representation Atlas explicitly tests previous tile type, carry, boundary occupancy, residual resource and other memory coordinates by searching for equal-state histories with different futures | PASS |
| T6 — boundary ownership | generic permutation/combination, complement/IE, repeated-object formula derivation remain COMB-01; arithmetic digit properties remain NT digit owner; COMB-03 owns only state design and transition decomposition | PASS |

Result: `COMB01_COMPATIBILITY = PASS_6_OF_6`.

## Consumer retrieval map now in force

| COMB-03 move | Exact provider retrieval | COMB-03-owned addition |
|---|---|---|
| define counted state | C01-1 + C01-7 | minimal sufficient state and sufficiency falsifier |
| split by first/last move | C01-2 + C01-4 | map branches bijectively to smaller states and derive recurrence |
| count transition stages | C01-3 | state-specific transition weights |
| avoid double count | C01-5 + C01-8 + C01-9 | validate state/branch identity |
| choose direct/complement/recursive route | C01-6 | decide whether recurrence is structurally useful |
| carry/string representation | C01-7 + C01-10 | local carry/state transition after arithmetic constraint is supplied |

## Acceptance decision

All ten payload requirements and all six compatibility tests pass against the current frozen provider artifact.

`COMB01_PROVIDER_ACCEPTED_FOR_COMB03 = PASS`

This removes the COMB-01 dependency blocker. Wave-0 promotion still additionally requires the ALG-04 boundary check and current-corpus overlap revalidation recorded in the companion checklist/ledger.