# Original Intent source issue template

Use when a new engineering/programme issue originates from direct Owner instruction and preserving the raw source materially improves later reconstruction.

This issue is **historical context source**, not an engineering responsibility.

```text
ISSUE_ROLE: ORIGINAL_INTENT
PARENT_WORK_ITEM: github:<owner>/<repo>#<parent>
AUTHORITY: HISTORICAL_OWNER_SOURCE
NO_EP: true
```

## Original Owner instruction — VERBATIM

Copy the Owner's relevant original instruction exactly as received.

```text
<<<
<verbatim Owner message>
>>>
```

Do not "clean up" spelling, grammar, terminology or sequencing inside the verbatim block.

### Sensitive-data exception

Do not copy:
- passwords;
- access tokens;
- private keys;
- credentials;
- sensitive personal data not needed for engineering reconstruction.

Use:

```text
[REDACTED_SENSITIVE — retained only in original source conversation]
```

when necessary.

## Capture metadata

```text
Captured at:
Source conversation/ref:
Parent work item:
Observed repository/main:
Original-intent digest:
```

## Owner-supplied inputs

Record direct inputs without promoting them to a stronger authority class than the Owner supplied:

- links;
- files;
- screenshots/images;
- examples;
- datasets;
- reference issues;
- external sources.

## Owner ideas / hypotheses

Preserve ideas as ideas when they were not explicit requirements.

## Expected outputs explicitly requested

List only outputs actually requested by the Owner.

## Explicit constraints / preserve

Record direct constraints and things the Owner explicitly said should not change.

## Derived intent index — NON-AUTHORITATIVE

This section exists only to make reconstruction fast.

```text
UNDERLYING HUMAN PROBLEM
...

REQUESTED OUTCOME
...

INPUTS
...

IDEAS / HYPOTHESES
...

EXPECTED OUTPUTS
...

OPEN AMBIGUITIES
...
```

If this derived index conflicts with the verbatim source, the verbatim source wins as historical evidence.

## Later amendments

Do **not** rewrite this issue body to make historical intent look current.

Later Owner decisions/amendments belong on the governing programme/implementation issue using existing Owner-amendment/Roadmap semantics.

## EP / Local Agent / RLL rule

- `ORIGINAL_INTENT` gets **no EP**.
- It gets no implementation plan.
- It gets no RLL execution envelope.
- Local Agent/RLL execution history stays with the governed engineering responsibility.
