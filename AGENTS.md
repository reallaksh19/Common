# Universal Engineering Agent Policy

This file applies to **all contributors and agents** working in this repository: ChatGPT, Codex, Claude, Cursor, Copilot, Gemini, local agents, scripts acting as agents, and humans.

The repository—not a chat session—is the durable source of engineering-work state.

## Canonical delivery protocol

For new engineering work, active relay work, takeover, abrupt-agent recovery, multi-agent coordination, AUTO MODE, and owner-governed roadmap handling, the canonical reusable delivery protocol is:

- `skills/engineering-pr-delivery-v2/SKILL.md`
- `skills/engineering-pr-delivery-v2/references/`
- `skills/engineering-pr-delivery-v2/scripts/`
- canonical chain-local current state: `agents/chains/<CHAIN_ID>/ACTIVE.md`
- canonical immutable endpoints: `agents/chains/<CHAIN_ID>/endpoints/<ENDPOINT_ID>.md`
- owner roadmap architecture: `skills/engineering-pr-delivery-v2/references/owner-roadmaps.md`

Recommended repository roadmap routing is:

```text
docs/roadmaps/ROADMAP_REGISTRY.md
docs/roadmaps/Overallroadmap_<domain>.md
```

Existing owner-roadmap paths such as `docs/OWNER_ROADMAP.md` remain valid when explicitly registered or bound.

`agents/agentchain.md` is retained as derived/legacy navigation and historical compatibility. It is not the authoritative mutable pointer for new canonical chains and does not need to change at every endpoint.

The previous protocol under `skills/engineering-pr-delivery/**` is **LEGACY / ROLLBACK-ONLY**. Do not start new workreport-centric chains under v1 unless explicitly directed.

Repository-local rules may be stricter. Explicit current owner instructions override generic workflow defaults, but no agent may silently weaken source authority, engineering evidence, validation integrity, takeover qualification, roadmap authority, concurrency/custody controls, code-quality requirements, or anti-gaming controls.

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

## 2. Chain-local repository traffic control

For each new chain use:

```text
agents/chains/<CHAIN_ID>/ACTIVE.md
agents/chains/<CHAIN_ID>/endpoints/<ENDPOINT_ID>.md
```

`ACTIVE.md` is the single mutable current-state/custody record for that chain. Other chains do not edit it.

For new material coding chains/legs use `CHAIN_STATE_VERSION: 2` with at least:

```text
CHAIN_STATE_VERSION
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
ROADMAPS
ROADMAP_REVIEW_STATUS
```

Every immutable endpoint records the same `CUSTODY_EPOCH`, `ROADMAPS`, and `ROADMAP_REVIEW_STATUS`. The first endpoint uses epoch `1`; each accepted direct successor increments by exactly one.

Advance `ACTIVE.md` only against the exact repository blob/version that was read. If the write conflicts or the observed epoch changed:

```text
STALE_WRITE
→ TAKEOVER_AUTHORITY = READ_ONLY
→ re-ground
→ reconcile same-chain custody
```

Do not force a stale pointer.

Repository-wide traffic is discovered by scanning `agents/chains/*/ACTIVE.md`. Shared dashboards are derived state only.

Historical `agents/agentchain.md`, `agents/agentchain/<CHAIN_ID>/**`, and chain-local version-1 artifacts remain readable history. Do not mass-rewrite them.

## 3. Mandatory owner-roadmap gate before coding

Before the first material coding action of every new chain or material leg:

1. read this `AGENTS.md`;
2. read `docs/roadmaps/ROADMAP_REGISTRY.md` when present;
3. identify every roadmap applicable to the issue, authority domain, expected changed paths, benchmark/oracle domain, and dependencies;
4. read the full applicable roadmap(s);
5. re-ground roadmap **observed status** claims against live repository/source/test/PR evidence when they affect the planned change;
6. record exact roadmap path + current Git blob SHA in `ACTIVE.md` and the active endpoint;
7. classify alignment:

```text
ALIGNED
ROADMAP_STATUS_STALE_BUT_SCOPE_ALIGNED
OWNER_DECISION_REQUIRED
NO_APPLICABLE_ROADMAP
```

8. do not start material coding if the planned implementation contradicts owner intent or requires an unapproved roadmap change.

Binding format:

```text
ROADMAPS: docs/roadmaps/Overallroadmap_wrc.md@<40-hex-git-blob-sha>
ROADMAP_REVIEW_STATUS: COMPLETE
```

Multiple roadmaps are separated by semicolons.

If no roadmap applies:

```text
ROADMAPS: NONE — <explicit discovery reason>
ROADMAP_REVIEW_STATUS: NOT_APPLICABLE
```

A changed roadmap blob invalidates the old binding. Re-read and re-bind before further material coding.

### Owner intent versus observed status

Keep these distinct:

```text
OWNER INTENT
  strategic architecture, sequencing, required benchmarks, scope,
  exclusions, authority direction, acceptance/release gates

OBSERVED STATUS
  current implementation/phase/benchmark state, which may become stale
```

Owner intent remains authoritative until the Owner changes it. Observed status must be verified before use.

When observed status is stale, do not silently edit the roadmap. Continue only within already-authorized owner intent and live repository truth, and create a `STATUS_REFRESH` proposal when the strategic document should be refreshed.

### Roadmap write authority

Owner roadmaps are `OWNER_CONTROLLED`.

Agents may think, analyze, challenge, and propose changes, including:

- major concept/architecture changes;
- additions or scope reductions;
- benchmark additions/replacements;
- phase reordering;
- authority-boundary changes;
- dependency changes;
- status refreshes;
- deprecation/migration proposals.

Agents may **not** mutate an owner roadmap merely because a proposal is good, AUTO MODE is active, a coding PR is merge-authorized, or the agent owns the implementation chain.

Roadmap mutation requires explicit Owner authorization for that roadmap/change boundary.

Agent proposals live at:

```text
agents/chains/<CHAIN_ID>/roadmap-proposals/<PROPOSAL_ID>.md
```

They remain advisory:

```text
PROPOSAL_STATUS: PROPOSED
ROADMAP_WRITE_AUTHORITY: NONE
```

After an explicit Owner decision, preserve a decision receipt at:

```text
agents/chains/<CHAIN_ID>/roadmap-decisions/<DECISION_ID>.md
```

Do not infer roadmap approval from silence, merge approval, permission to proceed, issue assignment, AUTO MODE, or a prior roadmap authorization.

Roadmap mutation should normally be its own leg/PR. Combining roadmap mutation with production implementation requires explicit Owner authorization for the combined scope.

## 4. Mandatory endpoint content

Every non-terminal version-2 endpoint must contain:

- mission and current state;
- completed/current/remaining work;
- one executable exact next action;
- known/proven and not-proven state;
- explicit `NOT_RUN` / `NOT_APPLICABLE` classifications;
- current hypothesis and falsifier;
- protected invariants;
- `Do not redo` and `Do not change` boundaries;
- expected next-leg files/domains;
- `Owner roadmaps` section;
- Inputs;
- Benchmarks;
- Common/governing documents;
- Authoritative sources;
- Production paths;
- Validation/test paths;
- changed-this-leg summary;
- validation summary and open risks;
- code-quality review when production code changes;
- exactly five next-agent qualification questions.

The `Owner roadmaps` section must record:

- roadmap ID/path and exact blob basis;
- applicable owner intent;
- roadmap status claims independently re-grounded for this leg;
- stale status discovered, if any;
- alignment classification;
- proposal/owner-decision references, if any.

If a required inventory is genuinely empty, record `NONE — <reason>` rather than silently omitting it.

## 5. Endpoint triggers

Create a durable endpoint at meaningful transitions, especially:

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
- after applicable roadmap change/re-binding;
- after an Owner roadmap decision changes the next safe leg;
- when ready for the next engineering leg;
- when the chain is objectively complete.

Do not create endpoints for trivial commentary-only edits.

## 6. Exactly five next-agent questions

Every non-terminal endpoint must contain exactly:

```text
Q1 Production Trace
Q2 Current Unresolved Problem / Failure Isolation
Q3 Authority / Invariant
Q4 Independent Validation
Q5 Next Contribution / Minimal Patch
```

Questions test the **next unresolved engineering work**. They are invalid if generic or answerable without opening the current repository/PR/evidence.

Where roadmap intent materially governs the next leg, qualification must test the candidate's ability to reconcile the proposed contribution with the roadmap basis rather than merely recite the roadmap.

## 7. Incoming takeover begins READ_ONLY

For engineering-critical takeover:

```text
TAKEOVER_AUTHORITY = READ_ONLY
```

The incoming candidate must independently:

1. locate `agents/chains/<CHAIN_ID>/ACTIVE.md` and its referenced endpoint;
2. read and verify every bound roadmap blob;
3. read endpoint-listed inputs, benchmarks, Common/governing docs, authoritative sources, production paths, and validation paths;
4. re-ground live main/PR/head/diff/reviews/checks;
5. reconcile live repository state, roadmap state, custody epoch, and endpoint state;
6. inspect material commits plus orphan/divergent endpoints after the active endpoint;
7. answer Q1–Q5;
8. obtain a separate verifier verdict;
9. acquire engineering-critical write authority only after a valid verdict.

For a legacy-format chain, use its existing locator until deliberate migration. The outgoing agent is never required.

## 8. Qualification separation and freshness

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

Fabricated repository evidence, stale roadmap basis, unsafe engineering claims, validation gaming, or incorrect authority assumptions may fail qualification regardless of numeric score.

Every question set binds to `QUALIFICATION_BASIS_HEAD`, `QUESTION_SET_ID`, and `QUESTION_SET_STATUS`.

Material changes to production, tests, benchmarks, oracles, engineering inputs, source authority, methodology, publication authority, or applicable owner roadmap intent can make prior qualification stale.

## 9. Crash recovery

Recover from the chain's `ACTIVE.md`, referenced immutable endpoint, bound roadmaps, and live repository state.

If commits exist after the latest endpoint, classify them:

```text
RECOVERABLE
PARTIAL_UNKNOWN
CONTAMINATED
UNTRUSTED
```

Never represent abrupt loss as graceful handoff.

If an endpoint was written but `ACTIVE.md` did not advance, treat it as an orphan durable endpoint requiring reconciliation.

If another agent advanced the chain first, stale blob/epoch fails closed. Do not force-write over accepted custody.

If a bound roadmap changed, old roadmap basis is stale; re-read before material coding.

## 10. Multi-agent coordination

Different independent chains use different relay files. WRC, LAFEA, and LoadCalc should not conflict merely because they share a repository.

Before mutation/new leg compare active chains for:

- exact-file/path overlap;
- authority-domain overlap;
- benchmark/oracle overlap;
- controlled-input overlap;
- release/publication overlap;
- roadmap-mutation overlap;
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

Multiple chains may safely **read** the same roadmap. An authorized mutation of a roadmap shared by active chains is coordination-sensitive because it invalidates their pinned roadmap basis. Do not rewrite other chains' state on their behalf; they must re-read/re-bind before their next material coding action.

Same-chain concurrency remains one `ACTIVE.md`, one lineage, and one custody-epoch sequence. Divergent direct successors require explicit reconciliation.

## 11. Engineering validation integrity

Separate software regression evidence from independent engineering verification.

Every material validation should record:

```text
STATUS      = PASS | FAIL | NOT_RUN | NOT_APPLICABLE
OBSERVATION = execution | source inspection | artifact inspection | inference
ORACLE      = implementation-coupled | independent reproduction |
              analytical | authoritative reference | cross-solver | experimental
```

Never weaken a tolerance merely because a test fails, replace independent expected values with production output, change implementation and oracle together and call it independent, delete difficult benchmarks, hard-code fixture answers into production, silence fail-closed behavior, represent source inspection as runtime proof, or represent `NOT_RUN` as `PASS`.

A roadmap may require a benchmark program; it is not itself an independent engineering oracle.

## 12. Code quality and anti-gaming

For production coding, default review thresholds are:

```text
new production module     normally <= 300 physical lines
function / method          normally <= 40 logical lines
```

These are review triggers, not blind failures. Do not game them with arbitrary split files or meaningless wrappers.

Module boundaries follow responsibility, state ownership, test seams, and engineering authority. New abstractions require real production consumers; new unused production modules are `0` by default; hidden globals/implicit singleton engineering authority are prohibited.

Source authority, applicability, numerical mechanics, independent oracle, publication/release authority, and presentation must remain separable.

Canonical validators must reject, at minimum:

- self-verification/self-scoring authority injection;
- duplicate critical control fields;
- stale chain-local pointers/epochs;
- same-chain divergent successors without reconciliation;
- missing endpoint/source/benchmark inventories;
- stale/missing roadmap bindings for version-2 chains;
- missing `Owner roadmaps` evidence section;
- PASS below qualification threshold;
- meaningless automatic-failure overrides.

A syntactically valid artifact is not substantive proof. Verifiers must independently open repository anchors.

## 13. PR, roadmap-write, and merge discipline

- One coherent assignment per PR unless the Owner explicitly changes scope.
- Keep implementation changes surgical and reviewable.
- Explain every changed file before closure.
- Do not silently broaden scope.
- Do not modify workflows unless explicitly authorized.
- Keep the chain recoverable while waiting for review/merge.
- PR merge does not imply chain completion.
- **Never merge without explicit Owner authorization.**
- **Never mutate an owner roadmap without explicit roadmap-write authorization.**

Merge authority and roadmap-write authority are separate permissions.

## 14. AUTO MODE

`AUTO MODE` grants autonomous phase progression within the approved mission. It does not waive qualification, source authority, roadmap review/write controls, validation integrity, chain-custody controls, code-quality gates, destructive-operation controls, or merge authority.

AUTO MODE may create roadmap proposals. It may not apply them to an owner roadmap without explicit authorization.

While no hard stop exists:

1. re-check live repository and active-chain overlap;
2. read exact chain `ACTIVE.md` version and custody epoch;
3. verify current roadmap binding(s);
4. select the next bounded action within owner intent;
5. implement one coherent unit;
6. validate accurately;
7. create the next immutable endpoint;
8. compare-and-swap `ACTIVE.md` to the next epoch;
9. continue automatically.

Hard stops include roadmap conflict/required unapproved roadmap mutation, stale roadmap binding, material scope expansion, unresolved authority change, stale/failed qualification, stale custody write, unresolved active-chain collision, validation gaming pressure, destructive/security operations needing authorization, or merge without merge authority.

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

Do not automatically edit roadmap status on chain completion. Propose a `STATUS_REFRESH` when strategically useful.

## 16. Legacy policy

`skills/engineering-pr-delivery/**` remains preserved for audit/history, rollback, repositories not yet migrated, and explicit compatibility work.

Legacy v2 shared-index artifacts and chain-local version-1 artifacts remain readable evidence. Existing chains may finish/migrate deliberately. New material coding legs should use/migrate to version 2 for roadmap binding.

Historical workreports/status/claims are not deleted merely because newer policy is canonical.

## 17. Executable controls

Canonical chain-local store:

```text
python skills/engineering-pr-delivery-v2/scripts/validate_chain_store.py .
python skills/engineering-pr-delivery-v2/scripts/validate_roadmap_bindings.py .
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

`Common` is the cross-repository governance and controlled-reference repository. Changes to reusable Skills, methodology, controlled evidence, roadmaps, or cross-repo policy can affect many downstream repositories and therefore require explicit provenance, narrow scope, durable compatibility reasoning, and rollback traceability.
