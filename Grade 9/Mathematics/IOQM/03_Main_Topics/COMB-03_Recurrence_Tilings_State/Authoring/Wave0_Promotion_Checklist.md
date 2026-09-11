# COMB-03 Wave-0 Promotion Checklist

Status: `WAVE0_ARCHITECTURE_FROZEN`

Accepted against production base `47af427f65a3370676931f885df09494524b9424`.

## A. Dependency gates

- [x] COMB-01 stable provider located: `.../COMB-01_Basic_Counting_Restrictions_Inclusion_Exclusion/Authoring/COMB01_Stable_Counting_Model_Interface_v1.md` (`c4d80bfeed3bca5d2b9cc3bd02b1a92fa7b66152`).
- [x] C01-1 through C01-10 executed individually in `COMB01_Interface_Acceptance_Contract.md`: PASS 10/10.
- [x] T1 through T6 executed with concrete consumer evidence: PASS 6/6.
- [x] COMB-01 retrieval is limited to object identity, counting semantics, exact-one-branch, restriction vocabulary and owner boundaries; no generic counting reteach remains planned.
- [x] ALG-04 stable provider located: `.../ALG-04_Sequences_Recurrences/Authoring/ALG04_Recurrence_Interface_v1.md` (`12891c65de0e1c26b6fef6623d54246a3d9dfd56`).
- [x] ALG-04 retrieval limited to indexed notation, initialization, explicit-v-recursive distinction and algebraic verification after structural derivation.
- [x] COMB-03 retains proof responsibility for counted state, base-state meaning, disjoint/exhaustive transition decomposition and recurrence derivation.
- [x] AP/GP, telescoping, generic sequence algebra and supplied-recurrence doctrine are not recreated.

## B. Compatibility / ownership tests

- [x] Retrieval-only counting test: PASS.
- [x] Every planned recurrence uses the exact-one-branch test: PASS.
- [x] Ordered/unordered identity remains COMB-01 retrieval: PASS.
- [x] Overlapping branches fail closed; generic IE routes to COMB-01: PASS.
- [x] State memory retains every restriction that changes future legal moves: PASS via State Representation Atlas sufficiency falsifier.
- [x] Generic IE, repeated-object formula, digit arithmetic and P&C ownership do not drift into COMB-03: PASS.
- [x] Deterministic state evolution remains distinct from COMB-04 adversarial games: PASS.
- [x] NT-05 arithmetic digit/property derivation remains outside COMB-03; carry/state transitions may consume a supplied constraint: PASS.

## C. Mathematical/source gates

- [x] Five primary anchors mapped and source-controlled.
- [x] Authority answers independently checked: `80, 10, 59, 15, 19`.
- [x] Frozen verification ledger join PASS for all five.
- [x] Metadata correction overlay not applicable to all five.
- [x] Deterministic-state vs adversarial-game boundary explicit.
- [x] Algebraic recurrence vs counting recurrence boundary explicit.
- [x] Forward vs reverse search contrast explicit.
- [x] Direct enumeration vs recursive decomposition contrast explicit.
- [x] One-state vs hidden-memory state sufficiency contrast explicit.
- [x] Recurrence vs better representation contrast explicit.

## D. Frozen teaching spine

1. **RECONNECT** — retrieve only recurrence notation/initialization and counting identity/disjointness vocabulary.
2. **DISCOVER** — same-size histories can have different futures; state must remember exactly what matters.
3. **MAKE SENSE** — define state, partition by first/last transition, prove exactly-once coverage, map to smaller states.
4. **TRY** — state meaning, base states, branches, recurrence, small-case verification.
5. **DIAGNOSE** — overlapping/omitted branches, too-small/too-large state, wrong base states, path-vs-state identity, game confusion.
6. **FADE** — support decreases across separate practice items; first mastery attempt is unlabelled/unhinted.
7. **ADOPT** — choose direct count, one-state recurrence, finite-memory recurrence, forward search, reverse search or no recurrence.
8. **TRANSFER** — tilings, strings, paths, deterministic machines, residual partitions and carry states.

## E. Frozen router

`OBJECT / TARGET`
`-> DEFINE MINIMAL SUFFICIENT STATE`
`-> PARTITION BY FIRST/LAST TRANSITION`
`-> DOES EVERY VALID OBJECT ENTER EXACTLY ONE BRANCH?`
`-> MAP BRANCHES TO SMALLER STATE(S)`
`-> GIVE BASE-STATE MEANING + INITIAL VALUES`
`-> VERIFY SMALL CASES`
`-> CHOOSE FORWARD / REVERSE / RECURRENCE / BETTER REPRESENTATION`
`-> COMPUTE`

First irreversible learner habit: **state before recurrence**.

## F. Required integrated contrasts

- supplied algebraic recurrence vs derived counting recurrence;
- direct enumeration vs recursive decomposition;
- deterministic state vs adversarial game;
- forward vs reverse-state search;
- one-state vs finite-memory/multi-state recurrence;
- recurrence vs better non-recursive representation;
- overlapping vs disjoint/exhaustive branches;
- ordered path/history vs state identity;
- carry-state transition vs digit-arithmetic derivation.

## G. Promotion decision

All provider acceptance, compatibility, source/math and overlap gates required by Agent D are PASS.

`WAVE0_ARCHITECTURE_FROZEN`

Next allowed operation: author one integrated learner package on the existing PR #95. No merge/readiness transition is authorized. Human evidence gates remain `NOT_RUN`.