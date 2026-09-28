# PR naming and provider lifecycle discipline

Advisory reconstruction quality only. These conventions are not merge/admission gates.

## PR title

Recommended:

```text
[#<owned-issue>][<KIND>] <bounded outcome>
```

Controlled KIND vocabulary:

```text
Impl
Fix
Infra
Evidence
Migration
Refactor
Docs
```

Examples:

```text
[#477][Impl] Preserve Owner intent and execution continuity
[#334][Infra] Add thin RLL/Codex local adapter
[#332][Evidence] Certify NLM metadata exact head
```

Do not encode lifecycle in title. Avoid `WIP`, `DONE`, `FINAL`, `READY`, `PASS`, `v2`, `new`, `fix again`.

GitHub Draft/Open/Merged/Closed owns lifecycle.

If a repository has an established branch/title convention, preserve it rather than forcing a rename. V3.1 uses naming to improve reconstruction, never as engineering permission.

## Branch

Recommended when no stronger repository convention exists:

```text
issue-<issue>/<short-outcome>
```

## PR identity header

Every implementation PR should make delivery identity easy to read:

```text
OWNED ISSUE: #<issue>
EP: <EP | NONE>
PLAN: <issuecomment/ref | NONE>
AGENT STATUS: <issuecomment/ref | NONE>
RELATIONSHIP: PRIMARY | STACK_PARENT | STACK_CHILD | RELATED
BASE: main@<sha>
HEAD: <sha>
```

The relationship vocabulary is the existing `delivery_stack[]` vocabulary.

## Provider lifecycle

Keep these separate:

```text
engineering responsibility complete
!= GitHub issue already closed
!= PR merged
!= programme complete
```

### Complete responsibility

```text
exact validation
→ TASK_RESULT / ACHIEVED
→ AGENT_STATUS_V1 status COMPLETE
→ Further task NONE within this responsibility
→ Task Snapshot / Handover refresh
→ provider issue may close when appropriate
```

### Superseded responsibility

If a genuinely different successor issue replaces the responsibility:

- publish `TASK_RESULT` with PARTIAL / SUPERSEDED disposition;
- identify successor issue;
- preserve material and negative knowledge;
- final AGENT_STATUS_V1 is `SUPERSEDED` with no further task here;
- close provider issue normally as not-planned when appropriate.

If the responsibility is unchanged but approach changes, use `PLAN_UPDATE`, same issue, same EP.

### Duplicate

Use GitHub duplicate semantics rather than SUPERSEDED when the issue is truly a duplicate.

### Superseded PR

Close with a durable note:

```text
SUPERSEDED BY #<new PR>

Owned issue: #...
Last exact head: ...
Reason: ...
Preserved material: ...
Consumer consequence: ...
```

Branch deletion is a separate provider operation and must not erase semantic handoff.
