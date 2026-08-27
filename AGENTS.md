# Universal Engineering Agent Policy

This file applies to **all contributors and agents** working in this repository: ChatGPT, Codex, Claude, Cursor, Copilot, Gemini, local agents, scripts acting as agents, and humans.

The repository—not a chat session—is the durable source of engineering-work state.

## Canonical delivery protocol

For new engineering work, active relay work, takeover, abrupt-agent recovery, multi-agent coordination, and AUTO MODE, the canonical reusable delivery protocol is:

- `skills/engineering-pr-delivery-v2/SKILL.md`
- `skills/engineering-pr-delivery-v2/references/`
- `skills/engineering-pr-delivery-v2/scripts/`
- repo-wide relay index: `agents/agentchain.md`

The previous protocol remains available under:

- `skills/engineering-pr-delivery/**`

but is now **LEGACY / ROLLBACK-ONLY**. Do not start new workreport-centric chains under v1 unless an explicit owner instruction requires rollback or a repository has not yet adopted v2.

Repository-local rules may be stricter. Explicit current owner instructions override generic workflow defaults, but no agent may silently weaken source authority, engineering evidence, validation integrity, takeover qualification, or anti-gaming controls.

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

A PR is a delivery container; it is not the durable engineering-work identity.

## 2. Repository traffic control

Use:

```text
agents/agentchain.md
```

as the repo-wide traffic/index log.

Use immutable detailed endpoints at:

```text
agents/agentchain/<CHAIN_ID>/<ENDPOINT_ID>.md
```

`agents/agentchain.md` contains:

1. `ACTIVE CHAINS` — mutable current traffic state;
2. `ENDPOINT LOG` — append-only compact history.

Detailed endpoint files are created once and must not be rewritten merely to clean history. Correct prior state by appending a later endpoint with explicit reconciliation/supersession provenance.

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

1. read `agents/agentchain.md` and the latest endpoint;
2. read the endpoint-listed inputs, benchmarks, Common/governing docs, authoritative sources, production paths, and validation paths;
3. re-ground live main/PR/head/diff/reviews/checks;
4. reconcile live state with the endpoint;
5. inspect material commits after the endpoint;
6. answer Q1–Q5;
7. obtain a separate verifier verdict;
8. acquire engineering-critical write authority only after a valid verdict.

The outgoing agent is never required.

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

Metadata-only index synchronization does not by itself change the material basis.

## 9. Crash recovery

If an agent disappears, recover from the latest durable repository state.

If commits exist after the latest endpoint, inspect and classify them:

```text
RECOVERABLE
PARTIAL_UNKNOWN
CONTAMINATED
UNTRUSTED
```

Then create a recovery endpoint. Never represent abrupt loss as a graceful handoff.

If a detailed endpoint was written but the index update did not occur before the crash, treat it as an **orphan durable endpoint** requiring reconciliation; do not silently delete it or ignore it.

## 10. Multi-agent coordination

Before mutation and before each new leg, compare active chains for:

- exact-file overlap;
- path-prefix overlap;
- authority-domain overlap;
- benchmark/oracle overlap;
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

## 12. Anti-gaming / fail-closed qualification

The canonical validators must reject, at minimum:

- candidate self-verification;
- candidate self-scoring/WRITE_ALLOWED claims;
- duplicate critical control fields;
- duplicate verdict/scores intended to exploit first/last-match parsing;
- stale active-index pointers;
- cross-chain/skipped predecessor lineage;
- missing endpoint files;
- orphan endpoint files without reconciliation;
- active historical-blob locators;
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

The exact owner keyword `AUTO MODE` grants autonomous phase progression within the approved mission. It does not waive qualification, source authority, validation integrity, destructive-operation controls, or merge authority.

While no hard stop exists:

1. re-check live repository and active-chain overlap;
2. select the next bounded action;
3. preserve hypothesis, prediction, invariants, and expected files;
4. implement one coherent unit;
5. validate accurately;
6. create/refresh the endpoint and Q1–Q5;
7. continue automatically.

Hard stops include material scope expansion, unresolved authority change, stale/failed qualification, unresolved active-chain collision, validation gaming pressure, destructive/security operations needing new authorization, or merge without owner merge authority.

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

Remove completed chains from `ACTIVE CHAINS` but retain their endpoint-log history.

## 16. Legacy v1 policy

`skills/engineering-pr-delivery/**` remains preserved for:

- audit/history;
- rollback if v2 proves defective;
- repositories not yet migrated;
- explicit owner-directed compatibility work.

Legacy artifacts such as `PR<NUMBER>_workreport.md`, status/claim registries, and embedded Appendix A remain readable evidence but are **not mandatory for new v2 chains** unless repository-local policy explicitly requires them.

Do not delete historical workreports merely because v2 is canonical.

## 17. Executable controls

Use the v2 scripts under:

```text
skills/engineering-pr-delivery-v2/scripts/
```

including the agentchain, candidate-answer, qualification, composite relay, transition/freshness/source/overlap controls, and self-tests.

Structural validation does not replace engineering judgment or independent technical verification.

## 18. Repository role

`Common` is the cross-repository governance and controlled-reference repository. Changes to reusable Skills, methodology, controlled evidence, or cross-repo policy can affect many downstream repositories and therefore require explicit provenance, narrow scope, durable compatibility reasoning, and rollback traceability.
