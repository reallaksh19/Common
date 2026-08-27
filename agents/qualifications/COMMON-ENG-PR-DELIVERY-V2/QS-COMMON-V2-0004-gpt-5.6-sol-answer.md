# Relay Qualification Answer — QS-COMMON-V2-0004

CHAIN_ID: COMMON-ENG-PR-DELIVERY-V2
ENDPOINT_ID: EP-0004
QUESTION_SET_ID: QS-COMMON-V2-0004
QUALIFICATION_BASIS_HEAD: 2d9160bd123eb91ca9c7f9e99ecbf050e4a07c3b
CANDIDATE_ID: gpt-5.6-sol-20260827-leg002
LIVE_PR_HEAD_OBSERVED: c3443ce8cc4f973c8a5356dadde27dfe6373788f
LIVE_MAIN_HEAD_OBSERVED: 08ca43a26aec4cacb0d7714cb059f71266c033e2
RECONCILIATION: METADATA_DRIFT
QUALIFICATION_STATUS: DEFERRED_VERIFICATION
TAKEOVER_AUTHORITY: READ_ONLY

The live PR remains one commit behind current `main`. The intervening main commit is still the Grade 9 bucket-builder change previously reconciled in EP-0004. No new v2/root-agent-policy overlap is observed. The PR head has moved beyond the material qualification basis only through relay/package metadata and split-endpoint work already recorded by EP-0003/EP-0004; no new engineering-critical adoption mutation has occurred.

## Q1 — Production Trace

The live relay path is:

```text
agents/agentchain.md
  -> ACTIVE CHAINS row for COMMON-ENG-PR-DELIVERY-V2
  -> latest endpoint EP-0004
  -> agents/agentchain/COMMON-ENG-PR-DELIVERY-V2/EP-0004.md
  -> PREVIOUS_ENDPOINT EP-0003
  -> EP-0003 retained material qualification basis
  -> skills/engineering-pr-delivery-v2/SKILL.md
  -> references/qualification.md
  -> candidate answer artifact
  -> separate verifier verdict artifact
  -> scripts/validate_qualification.py
  -> PASS_WRITE_ALLOWED only after independent verdict
```

Concrete current anchors:

- `agents/agentchain.md` points `COMMON-ENG-PR-DELIVERY-V2` to `EP-0004` and its split endpoint file.
- `EP-0004` binds the current question set to `QUALIFICATION_BASIS_HEAD=2d9160bd123eb91ca9c7f9e99ecbf050e4a07c3b` and records live-main reconciliation at `08ca43a26aec4cacb0d7714cb059f71266c033e2`.
- `references/qualification.md` states `candidate_id == verifier_id -> SELF_VERIFIED -> cannot grant WRITE_ALLOWED` and explicitly defines `DEFERRED_VERIFICATION` when no independent verifier is available.
- `scripts/validate_qualification.py` machine-enforces candidate/verifier identity inequality, answer/verdict shared-field equality, verdict-basis equality, score arithmetic, `>=92/100`, every score `>=17/20`, and a substantive reason for a numeric-pass `FAIL_READ_ONLY`.
- `scripts/validate_agentchain.py` separately checks index/endpoint linkage, chain-local predecessor lineage, endpoint files, active pointers, orphan endpoints, required source inventories, and Q1-Q5 structure.

The current Grade 9-only main drift does not enter that material path. The one intervening main commit changes `Grade 9/Mathematics/README.md` and `skills/grade9-question-bucket-builder/**`; it does not change `AGENTS.md`, `agents/**`, `skills/engineering-pr-delivery/**`, or `skills/engineering-pr-delivery-v2/**`.

The conclusion becomes stale immediately if live main acquires a commit touching root `AGENTS.md`, relay/qualification/shared-agent governance, either engineering-delivery skill, or another shared artifact consumed by v2 semantics; or if branch reconciliation creates a v2 conflict/test change.

## Q2 — Current Unresolved Problem / Failure Isolation

Current repository relationship:

```text
original merge base:
551d614c581f39a47015106ae9866c44304d8e9f

live main:
08ca43a26aec4cacb0d7714cb059f71266c033e2

observed PR head before this answer artifact:
c3443ce8cc4f973c8a5356dadde27dfe6373788f

branch relation:
1 commit behind main; v2 branch also contains the relay package commits
```

The sole main-only commit is `08ca43a26aec4cacb0d7714cb059f71266c033e2` (`Upgrade Grade 9 bucket builder skill to v2`). Its changed authority domain is Grade 9 question-bucket pedagogy/source/PDF governance. Changed paths are confined to:

- `Grade 9/Mathematics/README.md`;
- `skills/grade9-question-bucket-builder/SKILL.md`;
- `skills/grade9-question-bucket-builder/references/**`.

Prediction: a normal update/rebase/merge of this PR branch onto current main should import those Grade 9 changes without modifying any v2 relay file or root engineering-agent policy file.

Minimum isolating experiment before adoption: update/reconcile the branch in a normal Git-capable environment, then compare the v2/agent/root-policy diff and rerun `python skills/engineering-pr-delivery-v2/scripts/self_test.py`.

Falsifier: any conflict or post-update diff under `agents/**`, `AGENTS.md`, `skills/engineering-pr-delivery/**`, or `skills/engineering-pr-delivery-v2/**`; or any change in the 14 expected structural outcomes.

If falsified, the first action is not to resolve by guess. Stop adoption mutation, classify `MATERIAL_DRIFT` or `CONTRADICTION`, record a new recovery endpoint, identify the first conflicting path/semantic rule, and requalify against the reconciled material state.

## Q3 — Authority / Invariant

Current authority remains with root `AGENTS.md` on `main`. It explicitly names these as the canonical reusable protocol:

```text
skills/engineering-pr-delivery/SKILL.md
skills/engineering-pr-delivery/references/
skills/engineering-pr-delivery/scripts/
```

Therefore v2 is presently only a proposed sibling on draft PR #17. `READY_FOR_NEXT_LEG` in EP-0004 means the relay package has reached a safe qualification boundary; it does not grant root-policy mutation authority and does not make v2 canonical.

The adoption leg must preserve at least these v1 evidence-integrity invariants:

- live repository state outranks stale handover metadata;
- incoming engineering-critical takeover starts read-only;
- no self-granted expertise/write authority;
- software regression evidence remains distinct from independent engineering verification;
- never weaken tolerance/expected values/oracles merely to obtain PASS;
- never represent `NOT_RUN` as PASS;
- damaged intent is quarantined rather than guessed;
- merge remains owner-authorized;
- multi-agent overlap must be checked by both path and authority domain.

V2 adds a different continuity representation; it must not erase those engineering-integrity rules.

A plausible but invalid shortcut would be to edit root `AGENTS.md` now to replace v1 entirely simply because v2's structural tests are green. That would conflate structural package validation with real relay qualification and remove rollback/traceability before the A -> B -> C pilot exists.

The actual authority transition occurs only when root policy is deliberately changed on an authorized PR and that change becomes the repository's governing state. A safe initial transition should recognize v2 as a bounded pilot/next-generation protocol while preserving explicit v1 fallback/traceability until the real relay acceptance criteria are satisfied.

## Q4 — Independent Validation

The current 14-case suite is sufficient to begin a bounded pilot because it exercises the structural mechanisms that previously failed:

- compact index to immutable endpoint linkage;
- latest-active-pointer correctness;
- chain-local predecessor custody;
- missing/orphan endpoint detection;
- historical migration without rewriting old endpoints;
- mandatory Inputs/Benchmarks/Common documents;
- exactly five next-leg questions;
- separate candidate/verifier identity;
- basis-head/scoring/92-and-17 enforcement;
- rejection of meaningless numeric-pass override.

It is insufficient for downstream canonical rollout because all of those are structural/protocol checks. They do not prove that a real incoming engineering agent can recover a difficult live task, understand engineering authority, reject fabricated evidence, and safely contribute without conversation history.

Required real pilot evidence:

1. Agent A works a real engineering chain and leaves a durable endpoint with all six source inventories and Q1-Q5.
2. After that endpoint, at least one additional material repository commit exists and Agent A is deliberately treated as unavailable.
3. Agent B receives no chat-history dependency. B must discover the chain from the repo-wide index, reconcile the last endpoint plus later commits, classify those commits, and state a falsifier before mutation.
4. B answers the current Q1-Q5 with actual file/function/data anchors.
5. A separate verifier checks the anchors directly and rejects any plausible but fabricated/generic answer even if its Markdown is structurally valid.
6. Only after a valid verdict does B perform one bounded engineering contribution and create the next endpoint.
7. Agent C then repeats takeover from repository artifacts, proving the relay is not accidentally dependent on B's conversation state.
8. The deliberate abrupt-loss case must demonstrate either safe continuation or fail-closed recovery; guessing is a failure.

A fabricated-candidate rejection test should deliberately include one syntactically valid answer containing a nonexistent function/commit/value or a generic engineering explanation without the live production trace. The structural validator may accept the file shape; the verifier must reject it on repository-evidence grounds. That separation is intentional and necessary.

## Q5 — Next Contribution / Minimal Patch

After independent qualification passes, the smallest legitimate Common adoption/pilot leg is:

1. Reconcile `engineering-pr-delivery-v2-relay` with then-current `main` using a normal Git branch update/rebase/merge mechanism.
2. Rerun the full v2 structural suite and verify no relay-path semantic conflict.
3. Modify root `AGENTS.md` only enough to introduce `engineering-pr-delivery-v2` as the bounded relay/pilot protocol while retaining the legacy v1 location and explicit rollback/compatibility traceability.
4. Update only relay artifacts required to record that authority/pilot transition (`agents/agentchain.md`, a new immutable endpoint, and qualification/pilot evidence paths).
5. Do not modify `skills/engineering-pr-delivery/**` in the adoption patch.
6. Do not modify workflows unless separately authorized.
7. Start the real A -> B -> C pilot in a separate engineering repository/workstream, with its own PR/chain rather than expanding Common PR #17 into downstream implementation.

Expected Common changed domains for the bounded adoption patch:

```text
AGENTS.md
agents/agentchain.md
agents/agentchain/COMMON-ENG-PR-DELIVERY-V2/<new endpoint>.md
agents/qualifications/COMMON-ENG-PR-DELIVERY-V2/**
```

Protected unchanged domains:

```text
skills/engineering-pr-delivery/**
engineering evidence/oracles unrelated to relay governance
workflows
Grade 9 skill files
unrelated repository content
```

Pilot acceptance requires: successful A -> B -> C custody chain, deliberate abrupt-loss recovery, independent rejection of one fabricated candidate, no chat-history requirement, no evidence-integrity regression, and clear rollback/supersession behavior.

Rollback boundary: if the pilot shows that the compact index cannot reliably identify the current baton, endpoint/source custody becomes stale, agents require conversation history, or independent qualification is operationally unworkable, do not promote downstream. Append a supersession/recovery endpoint, keep v1 canonical, and correct v2 in a new bounded leg rather than rewriting the failed evidence.

## Candidate declaration

I do not assign a qualification score or write authority to this answer.

No independent verifier is available in this execution context, therefore:

```text
QUALIFICATION_STATUS: DEFERRED_VERIFICATION
TAKEOVER_AUTHORITY: READ_ONLY
```

Inspection, reconciliation, and evidence gathering may continue. Root-policy adoption mutation must not be self-authorized from this artifact.
