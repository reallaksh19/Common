# Golden example — Original Intent source

```text
ISSUE_ROLE: ORIGINAL_INTENT
PARENT_WORK_ITEM: github:owner/repo#210
AUTHORITY: HISTORICAL_OWNER_SOURCE
NO_EP: true
RELAY_PROTOCOL: V3.1_ONLY
```

## Original Owner instruction — VERBATIM

```text
<<<
Make the current readiness flow reconstructible for a fresh agent. Preserve the original programme intent, do not treat old status prose as current truth, and keep existing producer work reusable.
>>>
```

## Capture metadata

```text
Captured at: 2026-09-28T10:00:00Z
Source conversation/ref: owner-chat/current
Parent work item: github:owner/repo#210
Observed repository/main: 0123456789012345678901234567890123456789
Original-intent digest: sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
```

## Owner-supplied inputs

- programme issue #210;
- current producer PRs;
- one screenshot showing stale status.

## Owner ideas / hypotheses

- the status view may be reconstructing the wrong responsibility.

## Expected outputs explicitly requested

- a durable current-state view for a fresh agent;
- no new permission gate.

## Explicit constraints / preserve

- existing producer material remains valid;
- current Roadmap / EP / Local Agent / RLL semantics remain authoritative in their own domains.

## Derived intent index — NON-AUTHORITATIVE

```text
UNDERLYING HUMAN PROBLEM
A successor cannot reliably distinguish original intent from stale coordination prose.

REQUESTED OUTCOME
Preserve intent and make current reconstruction explicit.

INPUTS
Programme issue, provider PRs, screenshot.

IDEAS / HYPOTHESES
Status reconstruction may be responsibility-stale.

EXPECTED OUTPUTS
Reconstructible current state without a new gate.

OPEN AMBIGUITIES
Exact projection surface remains an engineering decision.
```

This source issue gets no EP, implementation plan, Local Agent execution or RLL state.
