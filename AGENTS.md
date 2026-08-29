# Common repository project agent overlay

COMMON_POLICY_SOURCE:
`skills/engineering-pr-delivery-v2/`

COMMON_POLICY_REFERENCE:
`skills/engineering-pr-delivery-v2/references/repository-agent-policy.md`

COMMON_PROTOCOL_MINIMUM_BASIS: `36068fde5b860ca1870311b166d28077b4c0bcf8`
LOCAL_POLICY_SCOPE: PROJECT_ONLY
LEGACY_RELAY_WRITES: FORBIDDEN

All reusable engineering-delivery, relay, qualification, crash-recovery, AUTO, validation-integrity, roadmap, and merge semantics live under `skills/engineering-pr-delivery-v2/`. Do not duplicate those rules here.

## Project identity / criticality

`reallaksh19/Common` is the shared repository for reusable skills, templates, governance references, and cross-project educational/engineering assets.

Changes under `skills/engineering-pr-delivery-v2/**` are `GOVERNANCE_CRITICAL` because they can change delivery behavior across downstream engineering repositories.

Other project folders may carry their own local instructions and artifacts; do not infer engineering-delivery authority over unrelated content merely because it lives in Common.

## Project governing inputs

For engineering-pr-delivery-v2 work, the governing implementation is:

- `skills/engineering-pr-delivery-v2/SKILL.md`
- `skills/engineering-pr-delivery-v2/references/**`
- `skills/engineering-pr-delivery-v2/scripts/**`
- the applicable Common chain under `agents/chains/**`

Owner-roadmap policy is defined inside the skill. Project/domain roadmaps outside this skill remain separately owner-controlled.

## Protected project domains

Do not silently weaken:

- downstream source/benchmark/oracle authority;
- qualification-first takeover;
- owner roadmap authority;
- validation truth / `NOT_RUN` integrity;
- canonical chain/custody controls;
- anti-gaming rules;
- Owner-controlled merge authority.

A governance change does not itself create engineering authority in a downstream product repository.

## Project validation entrypoints

For changes to `engineering-pr-delivery-v2`, use the applicable focused validators and, when a full checkout is available:

```bash
python skills/engineering-pr-delivery-v2/scripts/check_relay.py .
python skills/engineering-pr-delivery-v2/scripts/self_test.py
```

Do not promote unavailable execution to PASS.

## Project-specific AUTO hard stops

Stop AUTO progression when a proposed Common change would silently break downstream compatibility, rewrite historical relay evidence, weaken owner/source/oracle authority, or require guessing another project's engineering intent.

## Project-specific release / merge restriction

Changes to the shared engineering delivery protocol require an explicit PR and remain Owner-controlled for merge unless the Owner explicitly grants otherwise.
