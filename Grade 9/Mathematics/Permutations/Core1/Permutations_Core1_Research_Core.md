# Permutations - Core (1) Research - Research Core

- Research bundle: `RB-MATH-PERMUTATIONS-CORE1-2026`
- Evidence version: `1.0.0`
- Status: `READY_FOR_PUBLISH`
- Grade: 11
- Subject: MATHEMATICS

## Scope

Canonical registry releases:

- `REG-MATH-PERM-TAXONOMY` @ `ec4e35b51a7c1c9a6740cebc75700c02e11e306b`

Included canonical nodes:

- `PERM-ST01`
- `PERM-ST02`
- `PERM-ST03`
- `PERM-ST04`
- `PERM-ST05`
- `PERM-ST06`
- `PERM-ST07`
- `PERM-ST08`
- `PERM-ST09`
- `PERM-ST10`
- `PERM-ST11`
- `PERM-ST12`

## Verified research claims

### R-MATH-PERM-001

A permutation count is valid only after one outcome is defined and the counting procedure is checked to count every valid outcome exactly once.

- Type: `METHOD`
- Verification: `VERIFIED`
- Concepts: `PERM-ST01`, `PERM-ST02`, `PERM-ST03`, `PERM-ST04`, `PERM-ST05`, `PERM-ST06`, `PERM-ST07`, `PERM-ST08`, `PERM-ST09`, `PERM-ST10`, `PERM-ST11`, `PERM-ST12`
- Sources: `SRC-REPO-COMB-CONCEPT-MAP-V2`, `SRC-REPO-MATH-CORPUS-AUDITOR`

### R-MATH-PERM-002

For sequential ordered choices, multiply the number of legal choices at each stage; when r distinct positions are filled from n distinct objects without repetition, this compresses to nPr = n!/(n-r)!.

- Type: `METHOD`
- Verification: `VERIFIED`
- Concepts: `PERM-ST01`
- Sources: `SRC-REPO-COMB-CONCEPT-MAP-V2`, `SRC-REPO-MATH-CORPUS-AUDITOR`
- Conditions: Order or role must distinguish outcomes.; No repetition in the nPr compression.

### R-MATH-PERM-003

For a multiset of n objects with repeated multiplicities m1,m2,..., distinct linear arrangements are n! divided by m1!m2!... because swapping identical copies does not create a new outcome.

- Type: `METHOD`
- Verification: `VERIFIED`
- Concepts: `PERM-ST02`
- Sources: `SRC-REPO-COMB-CONCEPT-MAP-V2`, `SRC-REPO-MATH-CORPUS-AUDITOR`
- Conditions: Repeated copies are indistinguishable for outcome identity.

### R-MATH-PERM-004

Positional restrictions should be applied to the restricted positions or value classes before using an unrestricted permutation count; otherwise the base sample space is wrong.

- Type: `METHOD`
- Verification: `VERIFIED`
- Concepts: `PERM-ST03`
- Sources: `SRC-REPO-COMB-CONCEPT-MAP-V2`, `SRC-REPO-MATH-CORPUS-AUDITOR`

### R-MATH-PERM-005

When specified objects must stay together, a block representation preserves the external order of the block and the internal order within it; both levels must be counted exactly once.

- Type: `METHOD`
- Verification: `VERIFIED`
- Concepts: `PERM-ST04`
- Sources: `SRC-REPO-COMB-CONCEPT-MAP-V2`, `SRC-REPO-MATH-CORPUS-AUDITOR`

### R-MATH-PERM-006

For a condition such as not all specified objects together, total minus the all-together complement is valid when the total universe and the forbidden event are defined on the same outcome space.

- Type: `METHOD`
- Verification: `VERIFIED`
- Concepts: `PERM-ST05`
- Sources: `SRC-REPO-COMB-CONCEPT-MAP-V2`, `SRC-REPO-MATH-CORPUS-AUDITOR`
- Conditions: The complement event must be exact, not a stronger or weaker restriction.

### R-MATH-PERM-007

For no-two-together restrictions, arrange the anchor objects first and count legal gaps for the restricted objects; the number and capacity of gaps are part of the model.

- Type: `METHOD`
- Verification: `VERIFIED`
- Concepts: `PERM-ST06`
- Sources: `SRC-REPO-COMB-CONCEPT-MAP-V2`, `SRC-REPO-MATH-CORPUS-AUDITOR`

### R-MATH-PERM-008

Number-formation problems are positional permutation problems in which leading zero, controlling terminal digits, prefix/range conditions, repetition, and divisibility restrictions alter the legal slot choices before counting.

- Type: `METHOD`
- Verification: `VERIFIED`
- Concepts: `PERM-ST07`
- Sources: `SRC-REPO-COMB-CONCEPT-MAP-V2`, `SRC-REPO-MATH-CORPUS-AUDITOR`
- Conditions: Leading zero is not a legal first digit in an ordinary multi-digit integer.

### R-MATH-PERM-009

Lexicographic rank is obtained by counting complete admissible prefix buckets before the target prefix; with repeated symbols, each bucket uses multiset counts rather than ordinary factorial counts.

- Type: `METHOD`
- Verification: `VERIFIED`
- Concepts: `PERM-ST08`
- Sources: `SRC-REPO-COMB-CONCEPT-MAP-V2`, `SRC-REPO-MATH-CORPUS-AUDITOR`

### R-MATH-PERM-010

For n distinct objects arranged around a circle when rotations are equivalent and reflections remain distinct, fixing one anchor removes rotational overcount and gives (n-1)! arrangements.

- Type: `CANONICAL_FACT`
- Verification: `VERIFIED`
- Concepts: `PERM-ST09`
- Sources: `SRC-REPO-COMB-CONCEPT-MAP-V2`, `SRC-REPO-MATH-CORPUS-AUDITOR`
- Conditions: Rotations are considered identical.; Reflections are not identified unless the problem explicitly says so.

### R-MATH-PERM-011

A derangement is a permutation with no fixed point; forbidden-position counting requires inclusion-exclusion or an equivalent derangement recurrence rather than an unrestricted factorial count.

- Type: `METHOD`
- Verification: `VERIFIED`
- Concepts: `PERM-ST10`
- Sources: `SRC-REPO-COMB-CONCEPT-MAP-V2`, `SRC-REPO-MATH-CORPUS-AUDITOR`

### R-MATH-PERM-012

Forbidden-string problems should be modeled by bad events for the forbidden patterns; inclusion-exclusion must account for intersections when forbidden patterns can coexist or overlap.

- Type: `METHOD`
- Verification: `VERIFIED`
- Concepts: `PERM-ST11`
- Sources: `SRC-REPO-COMB-CONCEPT-MAP-V2`, `SRC-REPO-MATH-CORPUS-AUDITOR`

### R-MATH-PERM-013

Hybrid permutation problems should expose each distinct decision stage - such as choose, assign, then arrange - and verify that no stage re-counts symmetry already handled by another stage.

- Type: `METHOD`
- Verification: `VERIFIED`
- Concepts: `PERM-ST12`
- Sources: `SRC-REPO-COMB-CONCEPT-MAP-V2`, `SRC-REPO-MATH-CORPUS-AUDITOR`

### R-MATH-PERM-014

Across permutation families, the primary mathematical engine should be assigned by the decision that carries the solution rather than by surface nouns such as digits, books, students, letters, or functions.

- Type: `EDITORIAL_ANALYSIS`
- Verification: `VERIFIED`
- Concepts: `PERM-ST01`, `PERM-ST02`, `PERM-ST03`, `PERM-ST04`, `PERM-ST05`, `PERM-ST06`, `PERM-ST07`, `PERM-ST08`, `PERM-ST09`, `PERM-ST10`, `PERM-ST11`, `PERM-ST12`
- Sources: `SRC-REPO-MATH-CORPUS-AUDITOR`

## Representation requirements

### RREP-PERM-SLOTS-001

- Type: `ORDERED_SLOTS`
- Concepts: `PERM-ST01`, `PERM-ST03`, `PERM-ST07`
- Research refs: `R-MATH-PERM-002`, `R-MATH-PERM-004`, `R-MATH-PERM-008`
- Required labels: slot role, legal choices
- Semantic requirements: `{"mark_illegal_leading_zero_when_relevant": true, "show_choice_pool_change": true, "show_slot_roles": true}`

### RREP-PERM-MULTISET-001

- Type: `MULTISET_INVENTORY`
- Concepts: `PERM-ST02`, `PERM-ST08`
- Research refs: `R-MATH-PERM-003`, `R-MATH-PERM-009`
- Required labels: multiplicity, distinct arrangements
- Semantic requirements: `{"show_identical_swap_equivalence": true, "show_symbol_multiplicities": true}`

### RREP-PERM-BLOCK-001

- Type: `BLOCK_MODEL`
- Concepts: `PERM-ST04`, `PERM-ST05`
- Research refs: `R-MATH-PERM-005`, `R-MATH-PERM-006`
- Required labels: block, internal order
- Semantic requirements: `{"preserve_same_outcome_universe_for_complement": true, "separate_external_block_order_from_internal_order": true}`

### RREP-PERM-GAPS-001

- Type: `GAP_MODEL`
- Concepts: `PERM-ST06`, `PERM-ST09`
- Research refs: `R-MATH-PERM-007`, `R-MATH-PERM-010`
- Required labels: anchors, gaps
- Semantic requirements: `{"distinguish_linear_and_circular_gap_count": true, "show_anchor_objects": true, "show_legal_gaps": true}`

### RREP-PERM-PREFIX-001

- Type: `PREFIX_BUCKETS`
- Concepts: `PERM-ST08`
- Research refs: `R-MATH-PERM-009`
- Required labels: prefix, bucket size
- Semantic requirements: `{"show_complete_buckets_before_target": true, "show_prefix_decision": true}`

### RREP-PERM-CIRCLE-001

- Type: `CIRCULAR_ANCHOR`
- Concepts: `PERM-ST09`
- Research refs: `R-MATH-PERM-010`
- Required labels: anchor, rotation equivalence
- Semantic requirements: `{"show_fixed_anchor": true, "state_reflection_policy": true, "state_rotation_equivalence": true}`

### RREP-PERM-FORBIDDEN-001

- Type: `FORBIDDEN_POSITION_EVENT_GRID`
- Concepts: `PERM-ST10`, `PERM-ST11`
- Research refs: `R-MATH-PERM-011`, `R-MATH-PERM-012`
- Required labels: bad event, intersection
- Semantic requirements: `{"distinguish_fixed_position_from_forbidden_substring": true, "show_bad_events": true, "show_intersections_when_present": true}`

### RREP-PERM-HYBRID-001

- Type: `STAGE_DECISION_TABLE`
- Concepts: `PERM-ST12`
- Research refs: `R-MATH-PERM-013`
- Required labels: stage, decision, overcount check
- Semantic requirements: `{"include_overcount_check": true, "separate_choose_assign_arrange_stages": true}`

## Equations / reactions / formal objects

### ID-PERM-NPR-001

- Kind: `IDENTITY`
- Semantic expression: `nPr = n!/(n-r)!`
- Research refs: `R-MATH-PERM-002`

### ID-PERM-MULTISET-001

- Kind: `IDENTITY`
- Semantic expression: `distinct arrangements = n!/(m1! m2! ... mk!)`
- Research refs: `R-MATH-PERM-003`

### ID-PERM-CIRCLE-001

- Kind: `IDENTITY`
- Semantic expression: `circular arrangements of n distinct objects = (n-1)!`
- Research refs: `R-MATH-PERM-010`

### ID-PERM-DERANGE-001

- Kind: `IDENTITY`
- Semantic expression: `!n = (n-1)(!(n-1)+!(n-2))`
- Research refs: `R-MATH-PERM-011`

### ID-PERM-IE-001

- Kind: `IDENTITY`
- Semantic expression: `|A union B| = |A| + |B| - |A intersection B|`
- Research refs: `R-MATH-PERM-012`

## Worked reasoning records

### WR-PERM-OUTCOME-001

- Concepts: `PERM-ST01`, `PERM-ST02`, `PERM-ST12`
- Research refs: `R-MATH-PERM-001`, `R-MATH-PERM-002`, `R-MATH-PERM-003`, `R-MATH-PERM-013`
- Summary: Define one outcome, decide whether order/roles distinguish it, decide repetition/identity, expose sequential stages, count, then run omission/overcount checks.

### WR-PERM-RESTRICT-001

- Concepts: `PERM-ST03`, `PERM-ST07`
- Research refs: `R-MATH-PERM-004`, `R-MATH-PERM-008`
- Summary: Identify the controlling position or value restriction first, reserve or branch on it, then count the remaining slots under the reduced legal choice pool.

### WR-PERM-ADJACENCY-001

- Concepts: `PERM-ST04`, `PERM-ST05`, `PERM-ST06`
- Research refs: `R-MATH-PERM-005`, `R-MATH-PERM-006`, `R-MATH-PERM-007`
- Summary: Translate together to a block, not-all-together to a complement over the same universe, and no-two-together to an anchor-plus-gap capacity model.

### WR-PERM-RANK-001

- Concepts: `PERM-ST08`
- Research refs: `R-MATH-PERM-009`
- Summary: At each position, count all admissible smaller next symbols and the complete suffix arrangements they permit; then continue with the target prefix.

### WR-PERM-SYMMETRY-001

- Concepts: `PERM-ST09`
- Research refs: `R-MATH-PERM-010`
- Summary: State the equivalence relation first. If only rotations are identical, fix one anchor and linearly arrange the remaining objects; do not divide by reflection unless specified.

### WR-PERM-FORBIDDEN-001

- Concepts: `PERM-ST10`, `PERM-ST11`
- Research refs: `R-MATH-PERM-011`, `R-MATH-PERM-012`
- Summary: Define one bad event per forbidden fixed position or pattern, compute intersections, and use inclusion-exclusion or a validated derangement recurrence.

## Source ledger

### SRC-REPO-COMB-CONCEPT-MAP-V2

- Provider: Common repository
- Locator: Grade 9/Mathematics/NMTC Preliminary/03_Concept_Books/Combinatorics/Counting_Permutations_Pigeonhole_IE/Combinatorics_Assimilation_Concept_Map_v2.md
- Authority: `VERIFIED_SECONDARY`
- Verification: `VERIFIED`
- Rights/use: `REPRODUCTION_ALLOWED`

### SRC-REPO-COMB-ASSIMILATION-V2

- Provider: Common repository
- Locator: Grade 9/Mathematics/NMTC Preliminary/03_Concept_Books/Combinatorics/Counting_Permutations_Pigeonhole_IE/Combinatorics_Assimilation_Book_v2.md
- Authority: `VERIFIED_SECONDARY`
- Verification: `VERIFIED`
- Rights/use: `REPRODUCTION_ALLOWED`

### SRC-REPO-MATH-CORPUS-AUDITOR

- Provider: Common repository
- Locator: Grade 9/skills/grade9-math-corpus-coverage-auditor/SKILL.md
- Authority: `VERIFIED_SECONDARY`
- Verification: `VERIFIED`
- Rights/use: `REPRODUCTION_ALLOWED`

### SRC-EXAMSIDE-JEE-PC

- Provider: ExamSIDE
- Locator: https://questions.examside.com/past-years/jee/jee-main/mathematics/permutations-and-combinations
- Authority: `VERIFIED_SECONDARY`
- Verification: `PARTIAL`
- Rights/use: `REFERENCE_ONLY`

## Unresolved items

None.

## Handoff statement

This Research Core is a derived human review view of the machine ResearchBundle. Learner Bxx and publication-purpose adaptation are downstream Core (2) inputs and are not part of this research package.
