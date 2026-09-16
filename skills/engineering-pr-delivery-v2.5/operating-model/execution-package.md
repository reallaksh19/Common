# Execution package (EP)

An EP is a forward-looking executable contract derived from exactly one roadmap frontier work package.

WP-01 upgrades the kernel from structural/key-presence validation to **semantic sufficiency**. `validate_ep_self_contained.py` still enforces core identity/baton/context invariants; `validate_ep_semantics.py` now enforces the detailed forward contract used by zero-context successors. Serial aggregate conformance runs both. Approved parallel plans run the same semantic validator against every lane EP.

## One work package per EP

```text
one executable frontier WP -> one EP
```

Defining several future work packages does not make them one EP. Under serial execution, only the current frontier WP receives material execution authority. Parallel execution still uses one EP per approved lane work package.

## Semantic sufficiency

An executable EP must contain enough durable engineering information that a zero-context candidate can discover the repository, understand the current slice, identify current authoritative/editable inputs, resolve current required benchmarks/oracles, execute bounded implementation steps, verify acceptance, report exact results, and prepare the successor without prior chat.

The semantic validator requires:

- observable outcome plus a non-placeholder context capsule;
- executable `DSTEP-*` repository-discovery instructions;
- typed slice-specific inputs;
- typed benchmarks/oracles when present;
- allowed-write, allowed-read, protected, prohibited and Owner-reserved scope;
- structured anti-drift restrictions and invalidation rules;
- executable implementation steps with exact mappings to inputs, acceptance and tests;
- weighted acceptance and classified validation;
- source-bound report reconciliation payloads rather than headings alone;
- exact durable successor outputs.

## Slice-specific inputs

Each input records stable identity, description, authority, durable source, type/units, editability, applicability, resolution, consumers, validation and stale conditions. A `READY`/`OWNER_EDITABLE_READY` input must embed a value or define a resolution mechanism.

Applicability:

```text
CURRENT_STEP_REQUIRED
CURRENT_EP_REQUIRED
FUTURE_STEP
INFORMATIONAL
```

Resolution:

```text
READY
OWNER_EDITABLE_READY
DEFERRED_NOT_CURRENTLY_REQUIRED
MISSING_BLOCKING
INVALID
STALE
```

An executable EP cannot carry a current-required input in `MISSING_BLOCKING`, `INVALID`, `STALE`, or `DEFERRED_NOT_CURRENTLY_REQUIRED` state. Future/informational inputs remain visible without falsely blocking the current authorized slice.

## Benchmarks / oracles

Each declared benchmark/oracle records:

```text
id / name / purpose
source
oracle_class
payload
expected result
tolerance
independence rationale
applicability / resolution
AC/TEST mappings
stale conditions
```

Oracle classes currently include analytical, reference-data, independent-implementation, frozen-golden, external-standard, manual-reconstruction and observational evidence. Empty benchmark lists are permitted when the current slice does not require an independent benchmark; any benchmark that is declared must be semantically complete.

## Discovery

Discovery is executable, not narrative. A forward instruction uses a `DSTEP-*` ID and carries:

```text
action
target / targets
question
expected outputs
receipt-required flag
failure/reconciliation behavior
```

The future candidate evidence object remains distinct:

```text
DSTEP-* = forward discovery instruction in the EP
DISC-*  = backward Discovery Receipt produced by the incoming candidate
```

Legacy `DISC-*` discovery-step IDs are rejected by semantic validation. The `DISC-*` receipt itself is WP-02 work.

## Scope and authority

The semantic scope is split into:

```text
allowed        material write domains
allowed_reads  explicit read dependencies
protected      invariants/domains that must remain unchanged
prohibited     work this EP may not perform
owner_reserved changes requiring explicit Owner authority
```

Every declared domain carries a reason. An executable EP must have a non-empty allowed-write domain. Acceptance that requires prohibited or Owner-reserved work invalidates the forward contract rather than silently expanding it.

## Anti-drift

`anti_drift.do_not` and `anti_drift.stale_if` are structured records. They carry stable IDs, explicit restrictions/conditions, reasons/rationale, and an effect (`STALE | STOP | OWNER_REVIEW | RECONCILE`). Empty/vague string-only anti-drift is not sufficient for an executable EP.

## Implementation steps

Every implementation step names:

```text
id
objective
targets
reads
writes
input IDs
acceptance IDs
test IDs
expected state
stop conditions
```

Input/acceptance/test references are cross-checked against the EP. A vague step such as “implement required changes” does not pass semantic validation.

## Exact report contract

Required report headings remain stable for human continuity, but headings are no longer enough. `report_contract.payloads[]` binds each mandatory section to source objects and required reconciliation fields. `validate_report_contract.py` independently enforces those payloads, while `validate_ep_semantics.py` treats them as part of overall baton sufficiency.

Generated reports remain projections. They do not override roadmap, EP, checkpoint, progress, issue, quality or future certification authority.

## Successor contract

`successor_relay.required_outputs` must durably require at least:

```text
checkpoint
next_frontier
successor_ep_or_terminal_disposition
```

The canonical template also carries progress and issue-projection reconciliation outputs. This turns successor preparation from an informal duty list into an explicit return contract.

## Repository profile and protocol basis

WP-01 also closes two discovery preconditions around the EP:

- `REPO_PROFILE.yaml` is now a required aggregate-conformance object with dedicated procedural validation;
- `REPO_STATE.relay_protocol.version/basis_ref` is now mandatory, and placeholder/unbound protocol refs fail repo-state validation.

This makes repository discovery depend on admitted repository metadata and a pinned V2.5 protocol basis instead of bootstrap convention alone.

## Failure rule

The EP fails semantic sufficiency if a new candidate needs hidden chat context to resolve a material instruction, authority source, current input, benchmark/oracle, scope boundary, implementation step, required test, acceptance criterion, report obligation, successor duty or staleness condition.

WP-01 does **not** claim candidate takeover certification. A semantically complete baton is necessary but not sufficient for `TAKEOVER_CERTIFIED`; DISC/QUAL/TC admission remains WP-02/WP-03 work.
