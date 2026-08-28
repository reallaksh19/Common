# Universal Engineering Agent Policy

This file applies to **all contributors and agents** working in this repository: ChatGPT, Codex, Claude, Cursor, Copilot, Gemini, local agents, scripts acting as agents, and humans.

The repository—not a chat session—is the durable source of engineering-work state.

## Canonical delivery protocol

For new engineering work, active relay work, takeover, abrupt-agent recovery, multi-agent coordination, and AUTO MODE, the canonical reusable delivery protocol is:

- `skills/engineering-pr-delivery-v2/SKILL.md`
- `skills/engineering-pr-delivery-v2/references/`
- `skills/engineering-pr-delivery-v2/scripts/`
- canonical chain-local current state: `agents/chains/<CHAIN_ID>/ACTIVE.md`
- canonical immutable endpoints: `agents/chains/<CHAIN_ID>/endpoints/<ENDPOINT_ID>.md`

`agents/agentchain.md` is retained as derived/legacy navigation and historical compatibility. It is not the authoritative mutable pointer for new canonical chains and does not need to change at every endpoint.

The previous protocol remains available under:

- `skills/engineering-pr-delivery/**`

but is now **LEGACY / ROLLBACK-ONLY**. Do not start new workreport-centric chains under v1 unless an explicit owner instruction requires rollback or a repository has not yet adopted v2.

Repository-local rules may be stricter. Explicit current owner instructions override generic workflow defaults, but no agent may silently weaken source authority, engineering evidence, validation integrity, takeover qualification, concurrency/custody controls, code-quality requirements, or anti-gaming controls.

## 1. Core relay invariant

Assume the active agent may disappear after any meaningful action.

A competent next agent must be able to recover the mission from repository + PR artifacts without chat history and without the outgoing agent.

The canonical durable identity is:

```text
REPOSITORY
  -> CHAIN_ID
  -> LEG_ID
  -> ENDPOINT_ID
  -> PR / branch / commits
```

The durable endpoint key is `(CHAIN_ID, ENDPOINT_ID)`. Endpoint IDs are chain-local, so `EP-0001` may validly exist in WRC, LAFEA, LoadCalc, and other chains simultaneously.

A PR is a delivery container; it is not the durable engineering-work identity.

## 2. Repository traffic control

For each new chain use:

```text
agents/chains/<CHAIN_ID>/ACTIVE.md
agents/chains/<CHAIN_ID>/endpoints/<ENDPOINT_ID>.md
```

`ACTIVE.md` is the single mutable current-state/custody record for that chain. Other chains do not edit it.

Required current-state fields include:

```text
CHAIN_ID
MISSION
ACTIVE_ENDPOINT
ACTIVE_ENDPOINT_FILE
PR
BRANCH
HEAD
STATE
AUTHORITY_DOMAIN
ACTIVE_CUSTODIAN
CUSTODY_EPOCH
COORDINATION_STATE
DEPENDENCIES
```

Every immutable endpoint records the same `CUSTODY_EPOCH`. The first endpoint uses `1`; each accepted direct successor increments by exactly one.

Advance `ACTIVE.md` only against the exact repository blob/version that was read. If the write conflicts or the observed epoch changed:

```text
STALE_WRITE
→ TAKEOVER_AUTHORITY = READ_ONLY
→ re-ground
→ reconcile same-chain custody
```

Do not force a stale pointer.

Repository-wide current traffic is discovered by scanning `agents/chains/*/ACTIVE.md`. A shared dashboard may be rendered for convenience but is derived state, not write authority.

Historical `agents/agentchain.md` and `agents/agentchain/<CHAIN_ID>/**` artifacts remain valid legacy/recovery evidence and must not be mass-rewritten.

## 3. Mandatory endpoint content

Every non-terminal durable endpoint must contain:

- mission and current state;
- completed/current/remaining work;
- one executable `EXACT_NEXT_ACTION`;
- known/proven state;
- not-proven state;
- explicit `NOT_RUN` / `NOT_APPLICABLE` classifications;
- current hypothesis and falsifier;
- protected invariants;
- `DO NOT REDO` and `DO NOT CHANGE` boundaries;
- expected next-leg files/domains;
- changed-this-leg summary;
- validation summary and open risks;
- code-quality gate result and justified exceptions when production code changes;
- exactly five next-agent qualification questions;
- exact source/input custody described below.

### Required source/input custody at every endpoint

Always list:

```text
INPUTS
BENCHMARKS
COMMON / GOVERNING DOCUMENTS
AUTHORITATIVE SOURCES
PRODUCTION PATHS
VALIDATION / TEST PATHS
```

Where practical pin repository/path/commit/blob/hash and the relevant standard/source locator. If a category is genuinely empty, record `NONE — <reason>` rather than silently omitting it.

## 4. Endpoint triggers

Create a new durable endpoint at meaningful transitions, especially:

- before first engineering-critical mutation;
- after a coherent implementation unit;
- after a material hypothesis change;
- after significant validation PASS/FAIL;
- when a blocker changes;
- before/after PR transition;
- before intentional stop;
- before merge request;
- during recovery after agent loss;
- during same-chain custody reconciliation;
- when ready for the next engineering leg;
- when the chain is objectively complete.

Do not create endpoints for trivial commentary-only edits.

## 5. Exactly five next-agent questions

Every non-terminal endpoint must contain exactly:

```text
Q1 Production Trace
Q2 Current Unresolved Problem / Failure Isolation
Q3 Authority / Invariant
Q4 Independent Validation
Q5 Next Contribution / Minimal Patch
```

Questions test the **next unresolved engineering work**. They are invalid if they are generic textbook prompts or can be answered correctly without opening the current repository/PR/evidence.

Prefer tasks requiring the candidate to trace, reproduce, calculate, isolate, predict, falsify, compare, prove, reconcile, or define an exact patch boundary.

## 6. Incoming takeover begins READ_ONLY

For engineering-critical takeover:

```text
TAKEOVER_AUTHORITY = READ_ONLY
```

The incoming candidate must independently:

1. locate `agents/chains/<CHAIN_ID>/ACTIVE.md` and its referenced endpoint;
2. read the endpoint-listed inputs, benchmarks, Common/governing docs, authoritative sources, production paths, and validation paths;
3. re-ground live main/PR/head/diff/reviews/checks;
4. reconcile live state, active custody epoch, and endpoint state;
5. inspect material commits plus orphan/divergent endpoint files after the active endpoint;
6. answer Q1–Q5;
7. obtain a separate verifier verdict;
8. acquire engineering-critical write authority only after a valid verdict.

For a legacy-format chain that has not migrated, use its existing `agents/agentchain.md` locator. The outgoing agent is never required.

## 7. Qualification separation and threshold

Candidate-answer and verifier-verdict artifacts are separate:

```text
agents/qualifications/<CHAIN_ID>/<QUESTION_SET_ID>-<candidate>-answer.md
agents/qualifications/<CHAIN_ID>/<QUESTION_SET_ID>-<candidate>-verdict.md
```

Rules:

```text
candidate != verifier
candidate cannot self-award WRITE_ALLOWED
verdict basis == question material basis
total >= 92/100
minimum each >= 17/20
```

Question-set IDs should be visibly chain-namespaced.

Fabricated repository evidence, unsafe engineering claims, validation gaming, incorrect authority assumptions, or other substantive automatic-failure reasons may fail qualification regardless of numeric score.

An owner may authorize scope/merge/product direction but such authorization must not be rewritten as fabricated independent technical verification.

## 8. Qualification freshness

Every current question set binds to:

```text
QUALIFICATION_BASIS_HEAD
QUESTION_SET_ID
QUESTION_SET_STATUS
```

Material changes to production, tests, benchmarks, oracles, engineering inputs, source authority, behavior-changing configuration, methodology, or publication authority make the prior qualification stale.

Relay metadata-only state synchronization does not by itself change the material basis.

## 9. Crash recovery

If an agent disappears, recover from the chain's `ACTIVE.md`, its referenced immutable endpoint, and live repository state.

If commits exist after the latest endpoint, inspect and classify them:

```text
RECOVERABLE
PARTIAL_UNKNOWN
CONTAMINATED
UNTRUSTED
```

Then create a recovery endpoint. Never represent abrupt loss as a graceful handoff.

If a detailed endpoint was written but `ACTIVE.md` did not advance before the crash, treat it as an **orphan durable endpoint** requiring reconciliation.

If another agent advanced the same chain first, the stale blob/epoch must fail closed. Do not force-write over the accepted chain state.

## 10. Multi-agent coordination

Different independent chains use different relay files. WRC, LAFEA, and LoadCalc should not conflict merely because they are in the same repository.

Before mutation and before each new leg, compare active chains for:

- exact-file overlap;
- path-prefix overlap;
- authority-domain overlap;
- benchmark/oracle overlap;
- controlled-input overlap;
- release/publication overlap;
- dependency/stacking;
- base/main drift.

Classify:

```text
SAFE
COORDINATION_REQUIRED
BLOCKED_BY_ACTIVE_CHAIN
UNKNOWN
```

No exact-file overlap does not prove semantic independence.

Same-chain concurrency is different: there is one `ACTIVE.md`, one accepted lineage, and one custody-epoch sequence. Divergent direct successors must be reconciled before either becomes authoritative.

## 11. Engineering validation integrity

Separate software regression evidence from independent engineering verification.

Every material validation should record:

```text
STATUS      = PASS | FAIL | NOT_RUN | NOT_APPLICABLE
OBSERVATION = execution | source inspection | artifact inspection | inference
ORACLE      = implementation-coupled | independent reproduction |
              analytical | authoritative reference | cross-solver | experimental
```

Never:

- weaken a tolerance merely because a test fails;
- replace an independent expected value with production output;
- change implementation and oracle together and call it independent verification;
- delete/skip a difficult benchmark to obtain green status;
- hard-code fixture answers into production;
- silence a fail-closed condition to make a test pass;
- represent source inspection as runtime proof;
- represent `NOT_RUN` as `PASS`.

## 12. Code quality and anti-gaming

For production coding, default review thresholds are:

```text
new production module     normally <= 300 physical lines
function / method          normally <= 40 logical lines
```

These are review triggers, not blind hard failures. Do not game metrics with arbitrary `part1`/`part2` files or meaningless wrappers.

Module boundaries follow responsibility, state ownership, test seams, and engineering authority. New abstractions require real production consumers; new unused production modules are `0` by default; hidden globals/implicit singleton engineering authority are prohibited.

Source authority, applicability, numerical mechanics, independent oracle, publication/release authority, and presentation must remain separable.

Canonical validators must reject, at minimum:

- candidate self-verification;
- candidate self-scoring/WRITE_ALLOWED claims;
- duplicate critical control fields;
- duplicate verdict/scores intended to exploit parsing;
- stale chain-local active pointers/epochs;
- same-chain divergent successors without reconciliation;
- cross-chain predecessor lineage;
- missing endpoint files;
- orphan endpoint lineages without reconciliation;
- missing required source/benchmark inventories;
- PASS below threshold;
- meaningless automatic-failure overrides.

A syntactically valid Markdown artifact is not substantive proof. Verifiers must independently open repository anchors; fabricated paths/functions/SHAs are automatic failure.

## 13. PR and merge discipline

- One coherent assignment per PR unless the owner explicitly changes scope.
- Keep implementation changes surgical and reviewable.
- Explain every changed file before closure.
- Do not silently broaden scope.
- Do not modify workflows unless explicitly authorized.
- Keep the chain recoverable while waiting for review/merge.
- PR merge does not imply chain completion.
- **Never merge without explicit owner authorization.**

## 14. AUTO MODE

The exact owner keyword `AUTO MODE` grants autonomous phase progression within the approved mission. It does not waive qualification, source authority, validation integrity, chain-custody controls, code-quality gates, destructive-operation controls, or merge authority.

While no hard stop exists:

1. re-check live repository and active-chain overlap;
2. read exact chain `ACTIVE.md` version and custody epoch;
3. select the next bounded action;
4. preserve hypothesis, prediction, invariants, and expected files;
5. implement one coherent unit;
6. validate accurately;
7. create the next immutable endpoint;
8. compare-and-swap that chain's `ACTIVE.md` to the next epoch;
9. continue automatically.

Hard stops include material scope expansion, unresolved authority change, stale/failed qualification, stale custody write, unresolved active-chain collision, validation gaming pressure, destructive/security operations needing new authorization, or merge without owner merge authority.

## 15. Completion semantics

Distinguish:

```text
AGENT_LEG_COMPLETE
PR_COMPLETE
CHAIN_COMPLETE
```

A terminal endpoint uses:

```text
STATE: COMPLETE
NEXT_AGENT_QUALIFICATION: NOT_REQUIRED
QUESTION_SET_STATUS: NOT_REQUIRED
COMPLETION_BASIS:
```

Advance that chain's `ACTIVE.md` to the terminal endpoint/epoch. Derived dashboards omit terminal chains; immutable endpoint history remains.

## 16. Legacy v1 and shared-index policy

`skills/engineering-pr-delivery/**` remains preserved for audit/history, rollback, repositories not yet migrated, and explicit compatibility work.

Legacy v2 shared-index artifacts such as `agents/agentchain.md` and `agents/agentchain/<CHAIN_ID>/**` also remain readable historical/recovery evidence. Do not mass-rewrite immutable history.

Existing legacy-format chains may finish in place or migrate deliberately at a new endpoint. New chains should use `agents/chains/**`.

## 17. Executable controls

Canonical chain-local store:

```text
python skills/engineering-pr-delivery-v2/scripts/validate_chain_store.py .
python skills/engineering-pr-delivery-v2/scripts/detect_chain_overlap.py .
python skills/engineering-pr-delivery-v2/scripts/render_agentchain_dashboard.py .
python skills/engineering-pr-delivery-v2/scripts/check_relay.py . [<answer.md> <verdict.md>]
```

Legacy shared-index format remains supported by:

```text
python skills/engineering-pr-delivery-v2/scripts/validate_agentchain.py agents/agentchain.md
```

Structural validation does not replace engineering judgment or independent technical verification.

## 18. Repository role

`Common` is the cross-repository governance and controlled-reference repository. Changes to reusable Skills, methodology, controlled evidence, or cross-repo policy can affect many downstream repositories and therefore require explicit provenance, narrow scope, durable compatibility reasoning, and rollback traceability.
