# Project AGENTS.md overlay template

Repository-root `AGENTS.md` is a **project overlay only**. Reusable engineering-delivery mechanics live in Common.

Use a compact form like:

```text
# <Repository> project agent overlay

COMMON_POLICY_SOURCE:
reallaksh19/Common/skills/engineering-pr-delivery-v2/

COMMON_POLICY_REFERENCE:
reallaksh19/Common/skills/engineering-pr-delivery-v2/references/repository-agent-policy.md

COMMON_PROTOCOL_MINIMUM_BASIS: <40-hex Common commit containing required protocol floor>
LOCAL_POLICY_SCOPE: PROJECT_ONLY
LEGACY_RELAY_WRITES: FORBIDDEN

## Project identity / criticality
<repo-specific domain and criticality>

## Project roadmaps / governing inputs
<repo-specific roadmap registry, owner roadmaps, master inputs>

## Project authoritative sources
<standards, controlled PDFs, datasets, source custodians>

## Protected project domains
<solver formulation, engineering methods, release/publication boundaries, etc.>

## Project validation / benchmark entrypoints
<repo-specific commands and benchmark/oracle locations>

## Project-specific AUTO hard stops
<only domain-specific stop conditions not already defined in Common>

## Project-specific merge/release restrictions
<only stricter local rules, if any>
```

Do not copy into the overlay:

- canonical chain paths;
- chain-state schema;
- crash-recovery sequence;
- qualification sequencing/scoring;
- Q1–Q5 schema;
- generic AUTO semantics;
- generic merge discipline;
- generic validation-integrity rules.

Those are read from the live Common protocol for every material leg.
