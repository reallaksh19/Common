# Common repository project agent overlay

COMMON_POLICY_SOURCE:
`skills/engineering-pr-delivery-v3.2/`

COMMON_POLICY_REFERENCE:
`skills/engineering-pr-delivery-v3.2/SKILL.md`

COMMON_PROTOCOL_MINIMUM_BASIS: `149770a21ca073df49717a96e2106c967adddc2d`
LOCAL_POLICY_SCOPE: PROJECT_ONLY
LEGACY_RELAY_WRITES: FORBIDDEN

Common's Owner-selected engineering policy source is `skills/engineering-pr-delivery-v3.2/`. Its `SKILL.md` is normative for the v3.2 continuity/recovery slice; inherited compatibility material remains subject to that document's precedence rules. Do not duplicate reusable policy here. This overlay does not change downstream repositories' protocol selectors or rewrite historical evidence.

## Project identity / criticality

`reallaksh19/Common` is the shared repository for reusable skills, templates, governance references, and cross-project educational/engineering assets.

Changes to shared engineering-delivery protocol paths, including `skills/engineering-pr-delivery-v2/**`, `skills/engineering-pr-delivery-v3.1/**` and `skills/engineering-pr-delivery-v3.2/**`, are `GOVERNANCE_CRITICAL` because they can change delivery behavior across downstream engineering repositories.

Other project folders may carry their own local instructions and artifacts; do not infer engineering-delivery authority over unrelated content merely because it lives in Common.

## Project governing inputs

For work governed by the selected Common policy source, the governing inputs are:

- `skills/engineering-pr-delivery-v3.2/SKILL.md`
- `skills/engineering-pr-delivery-v3.2/operating-model/**`
- `skills/engineering-pr-delivery-v3.2/schemas/**`
- `skills/engineering-pr-delivery-v3.2/scripts/**`
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

For changes to `engineering-pr-delivery-v3.2`, use applicable focused validators and the candidate continuity/replay regressions:

```bash
python -m unittest discover -s skills/engineering-pr-delivery-v3.2/tests -p 'test_continuity_v32*.py' -v
python -m unittest discover -s skills/engineering-pr-delivery-v3.2/tests -p 'test_replay_cases_v32.py' -v
```

When validating a repository with native Relay authority objects, use `python skills/engineering-pr-delivery-v3.2/scripts/validate_foundation.py .` as applicable. Validate changes to other skills with their own focused checks. Existing hosted checks remain path-scoped; a terminal NOT_APPLICABLE result is not candidate acceptance evidence.

Do not promote unavailable execution to PASS.

## Project-specific AUTO hard stops

Stop AUTO progression when a proposed Common change would silently break downstream compatibility, rewrite historical relay evidence, weaken owner/source/oracle authority, or require guessing another project's engineering intent.

## Project-specific release / merge restriction

Changes to the shared engineering delivery protocol require an explicit PR and remain Owner-controlled for merge unless the Owner explicitly grants otherwise.
