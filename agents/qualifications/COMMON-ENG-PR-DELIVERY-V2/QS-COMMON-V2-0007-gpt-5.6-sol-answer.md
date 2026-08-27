# Relay Qualification Answer — QS-COMMON-V2-0007

CHAIN_ID: COMMON-ENG-PR-DELIVERY-V2
ENDPOINT_ID: EP-0007
QUESTION_SET_ID: QS-COMMON-V2-0007
QUALIFICATION_BASIS_HEAD: 98b36f72015f12d8bf4f4e1bedce4753d911bfdc
CANDIDATE_ID: gpt-5.6-sol-20260827-leg002
LIVE_PR_HEAD_OBSERVED: b3abde9b344b98d5807eb83ccec55b5cdab55630
LIVE_MAIN_HEAD_OBSERVED: 98b36f72015f12d8bf4f4e1bedce4753d911bfdc
RECONCILIATION: METADATA_DRIFT
QUALIFICATION_STATUS: DEFERRED_VERIFICATION
TAKEOVER_AUTHORITY: READ_ONLY

The post-merge material basis is unchanged. PR #19 contains only EP-0007 plus `agents/agentchain.md` synchronization at this observation point; root `AGENTS.md` and both delivery-skill implementations remain untouched on LEG-002.

## Q1 — Production Trace

Current authority path:

```text
main@98b36f72015f12d8bf4f4e1bedce4753d911bfdc
  -> root AGENTS.md
  -> canonical reusable delivery protocol:
       skills/engineering-pr-delivery/SKILL.md
       skills/engineering-pr-delivery/references/
       skills/engineering-pr-delivery/scripts/

main@98b36f...
  -> skills/engineering-pr-delivery-v2/SKILL.md
  -> merged and available
  -> NOT named by root AGENTS.md as canonical yet
```

The authority-granting file today is root `AGENTS.md`. Its opening policy section explicitly names only legacy `engineering-pr-delivery` as canonical. V2 exists on main and describes its own relay behavior, but presence of a Skill does not itself override root repository policy.

The minimal bounded adoption surface is therefore the root `AGENTS.md` authority declaration and the v1 work-identity/handover sections that currently require per-PR workreports. A safe first adoption should not delete the v1 paths. Instead it should state that v2 is the bounded relay protocol for new relay work/pilot chains, while v1 remains an explicit legacy/fallback protocol until the real pilot acceptance gate closes.

The trace becomes stale if `main` moves and changes root `AGENTS.md`, either delivery Skill, shared agent governance, or the qualification/relay semantics consumed by this leg. It also becomes stale if PR #19 begins root-policy mutation before the verifier verdict.

## Q2 — Current Unresolved Problem / Failure Isolation

PR #17 squash-merged successfully to `main` as `98b36f72015f12d8bf4f4e1bedce4753d911bfdc` with parent `08ca43a26aec4cacb0d7714cb059f71266c033e2`.

Post-merge repository checks show:

- `skills/engineering-pr-delivery-v2/SKILL.md` on `main` has blob SHA `b5ef40e04f9dc58c17577618d2e4dabbcdec9f25`.
- The final PR #17 branch version of that same file has the identical blob SHA `b5ef40e04f9dc58c17577618d2e4dabbcdec9f25`.
- `validate_candidate_answer.py` on `main` has blob SHA `27dd4221e95ea9909ee070b869def364741c463b`; the final PR #17 branch has the same blob SHA.
- `validate_qualification.py` on `main` has blob SHA `77dc756bada3a030bc14a6a5d79a63c6a8367eb9`; the final PR #17 branch has the same blob SHA.

Therefore the core Skill and both qualification-control parsers survived squash merge byte-identically. The compact index, endpoint files, candidate answer and verifier handoff are also present on merged main because LEG-002 was started from that exact tree.

The smallest remaining isolating check before root-policy mutation is to verify the full set of merged v2 package/relay paths against the final PR #17 tree or execute the modular runner from a normal checkout. Prediction: no v2 semantic delta exists from squash; only Git commit identity changed.

Falsifier: any merged v2 file has a different blob/content than the final qualified PR #17 file without an explained base-only change, or any modular structural outcome differs when run from current main. On falsification, stop root adoption, create a recovery endpoint, isolate the first differing file/test, and requalify.

## Q3 — Authority / Invariant

Bounded adoption changes repository policy authority, not merely documentation wording.

Must remain available:

- legacy `skills/engineering-pr-delivery/**` files and their historical workreport protocol;
- v1 evidence-integrity rules: live Git truth over stale reports, READ_ONLY takeover, independent engineering validation, anti-gaming, NOT_RUN honesty, overlap checks, owner-only merge;
- explicit rollback route to v1 if the v2 pilot fails.

May become active after a valid verifier PASS:

- `engineering-pr-delivery-v2` as the bounded/default relay protocol for new engineering relay chains in Common pilot scope;
- `agents/agentchain.md` + immutable endpoint files as the primary new continuity surface for those chains;
- candidate/verifier separation before new-agent engineering-critical custody.

Must NOT be inferred by downstream repositories yet:

- that all downstream repos are automatically migrated;
- that legacy workreports may be deleted immediately;
- that passing structural tests proves the real abrupt-loss relay;
- that v2 is globally canonical before the separate A -> B -> C pilot acceptance evidence exists.

Owner authorization to merge PR #17 authorized the package merge. It did not convert candidate evidence for this new post-merge adoption leg into an independent verifier verdict. The material basis changed from pre-merge PR-head identity to merged main, and EP-0007 intentionally created a fresh qualification set.

Invalid shortcut: edit root `AGENTS.md` to replace every v1 reference with v2 immediately because PR #17 is merged. That would erase fallback provenance and treat package merge as proof of operational relay behavior.

## Q4 — Independent Validation

The merged structural/policy benchmark set is sufficient to justify a bounded Common-only pilot after independent qualification because it fail-closes the known protocol failure modes:

- stale active pointer;
- cross-chain/skipped predecessor;
- missing/orphan endpoint;
- active historical blob;
- missing benchmark inventory;
- candidate self-verification;
- threshold manipulation;
- meaningless automatic-failure override;
- duplicate authority/verdict/score/control fields;
- candidate self-authorization/self-scoring.

It remains insufficient for downstream canonical rollout because these checks validate structure and policy mechanics, not the engineering cognition of an incoming agent on a difficult live task.

Required real pilot evidence:

1. Agent A performs a real engineering contribution and leaves a current endpoint with inputs, benchmarks, common/governing docs and Q1-Q5.
2. At least one material commit occurs after the last endpoint, then A is deliberately treated as unavailable.
3. Agent B gets no chat-history help, discovers the chain/index, re-grounds live state, classifies post-endpoint commits, answers Q1-Q5 and states falsifiers before mutation.
4. A distinct verifier checks B's anchors directly.
5. One deliberately fabricated but syntactically valid candidate answer is included. Example: it cites a plausible nonexistent production function or claims a benchmark value from a file that does not contain it. The structural parser may accept the Markdown shape; the verifier must reject the evidence.
6. After PASS, B makes one bounded change and creates the next endpoint.
7. Agent C repeats recovery from repository artifacts only.
8. The pilot records whether abrupt loss produces safe continuation or fail-closed recovery without reconstruction from chat.

Only that evidence can close the behavioral claim that the relay works as an engineering team rather than as a documentation format.

## Q5 — Next Contribution / Minimal Patch

After independent `PASS_WRITE_ALLOWED`, the smallest legitimate Common root-policy patch is confined to `AGENTS.md` plus relay/qualification metadata.

Root policy changes should:

1. keep the existing statement that the repository is the durable source of work state;
2. retain the legacy v1 paths explicitly as `legacy/fallback` rather than delete them;
3. add the merged v2 path as the bounded relay protocol for new/pilot engineering relay work;
4. change durable work identity from unconditional `WIP/PR` wording to acknowledge `CHAIN_ID -> LEG_ID -> ENDPOINT_ID -> PR/commit` for v2 relay chains, while preserving legacy workreport rules for v1 work already in flight;
5. replace the unconditional mandatory-workreport language for v2 chains with the compact `agents/agentchain.md` + immutable endpoint contract;
6. state that new-agent engineering-critical v2 takeover requires separate candidate/verifier qualification and cannot self-authorize;
7. preserve v1 validation-integrity, anti-gaming, multi-agent overlap and owner-only merge rules;
8. state that downstream canonical migration is blocked pending the real A -> B -> C abrupt-loss pilot.

Expected changed paths after PASS:

```text
AGENTS.md
agents/agentchain.md
agents/agentchain/COMMON-ENG-PR-DELIVERY-V2/<next endpoint>.md
agents/qualifications/COMMON-ENG-PR-DELIVERY-V2/<verdict>.md
```

Protected unchanged:

```text
skills/engineering-pr-delivery/**
skills/engineering-pr-delivery-v2/** unless a separately proven defect exists
workflows
Grade 9 content
unrelated Skills
downstream repos during this Common-only leg
```

Rollback/supersession if the pilot fails: do not delete failed relay history. Append a supersession/recovery endpoint, restore or retain v1 as canonical fallback in root policy, classify the exact failed v2 assumption, and repair v2 in a new bounded PR. Downstream adoption remains blocked.

Validation before downstream PRs:

- current-main re-ground;
- root policy diff inspection;
- modular v2 structural suite from normal checkout if available;
- independent verifier verdict for adoption;
- successful Common bounded adoption;
- successful real A -> B -> C abrupt-loss pilot;
- demonstrated rejection of fabricated repository evidence;
- no chat-history dependency for B/C recovery.

## Candidate declaration

I assign no score and no verdict to this answer.

QUALIFICATION_STATUS remains DEFERRED_VERIFICATION and TAKEOVER_AUTHORITY remains READ_ONLY until a distinct verifier checks the post-merge evidence and records a valid verdict.