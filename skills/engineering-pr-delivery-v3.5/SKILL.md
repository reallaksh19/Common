# Engineering Relay V3.5 — embedded Coder continuity/recovery for Local PR Delivery v1.1

## Status and lineage

V3.5 is an additive protocol line for **nested Coder engineering execution** under `Local_PR_Deliverty_v1.1`.

It was forked without modifying V3.2 from the exact Common basis:

```text
SOURCE_COMMIT: a29e67ae8beabaeca8a794343e72c01e37d067af
SOURCE_V3_2_TREE: 88ac97432a811f9a6b8d00bbe45cbec891e70d6a
SOURCE_PATH: skills/engineering-pr-delivery-v3.2
```

`skills/engineering-pr-delivery-v3.2/**` is frozen by #492/#494 and is not a V3.5 implementation surface.

The copied V3.2-named files under this V3.5 directory are retained only as compatibility/replay baseline. They do **not** select the active V3.5 state machine. Active V3.5 behavior is defined by this file plus the explicitly V3.5-named schema/script/tests.

## Nesting invariant

Local v1.1 owns the production responsibility and role lifecycle:

```text
LOCAL RESPONSIBILITY
PRD-017
  |
  `-- CODER stage
        |
        `-- V3.5 nested engineering execution
            ENG-PRD-017-CODER
```

V3.5 owns only continuity/recovery/provenance for the nested Coder engineering execution.

V3.5 MUST NOT own or infer Local:

- Reviewer or Coordinator/Super Reviewer transitions;
- writer-slot/start permission;
- Local stage timer accounting or watchdog truth;
- merge authority;
- acceptance-policy adoption;
- risk-relaxation authority;
- Local responsibility completion.

A V3.5 `TASK_RESULT` may complete `ENG-PRD-017-CODER`; it can never by itself complete `PRD-017`.

## Canonical nested identity

For Local responsibility `PRD-017`, the default nested engineering identity is:

```text
ENG-PRD-017-CODER
```

The active binding records both identities:

```yaml
local_responsibility_task_id: PRD-017
engineering_responsibility: ENG-PRD-017-CODER
role: CODER
result_scope: CODER_ENGINEERING_EXECUTION
local_responsibility_complete: false
```

Identity is explicit and durable. Do not derive Local completion from V3.5 state names such as `COMPLETE`.

## Exact protocol provenance

A native V3.5 nested execution records exact immutable refs for both governing layers:

```text
LOCAL_PROTOCOL_REF: owner/repo@<40-sha>:skills/Local_PR_Deliverty_v1.1
V3_5_PROTOCOL_REF: owner/repo@<40-sha>:skills/engineering-pr-delivery-v3.5
```

It also records the Local acceptance epoch/profile references supplied by the Local control plane. Those references are observed/bound context only; V3.5 cannot adopt or mutate them.

## Recorder-first continuity semantics

V3.5 retains the useful V3.2 continuity/recovery invariants for the nested engineering execution:

- material truth comes from Git/PR/tests/runtime/artifacts;
- durable task publications explain successor-safe engineering truth;
- material and semantic/evidence frontiers remain separate;
- passive frontier lag is not an engineering permission gate;
- replacement executors do not create a new nested responsibility;
- recovery evidence is required before the next material change after detected interruption/recovery;
- progress is denominator-based, never activity-count based;
- provider/reporting failure reduces observability, not engineering agency.

The publication family remains:

```text
IMPLEMENTATION_PLAN
PLAN_UPDATE
TASK_EVIDENCE
TASK_RESULT
```

## Embedded Coder contract

The machine-readable active contract is:

- `schemas/embedded-coder-context-v35.schema.yaml`
- `scripts/embedded_coder_v35.py`
- `tests/test_embedded_coder_v35.py`

The contract validates:

1. exact Local and V3.5 protocol refs/digests;
2. `PRD-*` Local identity and namespaced `ENG-PRD-*-CODER` engineering identity;
3. role fixed to `CODER`;
4. acceptance epoch/profile binding as read-only Local context;
5. explicit denial of Local transition/timer/merge/policy/risk authority;
6. Coder-scoped result semantics;
7. `local_responsibility_complete: false` for every V3.5 result.

## Completion semantics

V3.5 uses:

```text
RESULT_SCOPE = CODER_ENGINEERING_EXECUTION
ENGINEERING_RESPONSIBILITY_COMPLETE = true | false
LOCAL_RESPONSIBILITY_COMPLETE = false
```

Even when engineering responsibility is complete:

```text
ENG-PRD-017-CODER COMPLETE
```

Local remains responsible for:

```text
Coder END
→ Reviewer
→ Coordinator/Super Reviewer
→ delivery / merge lifecycle
→ Local responsibility completion
```

## Version drift

V3.5 never silently falls back to V3.1/V3.2 as active authority merely because copied files, CI names, migration fixtures, generated state, or historical references contain those versions.

Historical/compatibility reads are allowed only when explicitly classified as such.

If a later Relay version appears, the current nested execution remains pinned until the Local/Owner control plane authorizes migration.

## CI

Dedicated V3.5 hosted validation is `.github/workflows/engineering-pr-delivery-v3.5.yml`.

It validates the V3.5 active contract and verifies that the frozen `skills/engineering-pr-delivery-v3.2/**` tree is not modified by #494 work.
