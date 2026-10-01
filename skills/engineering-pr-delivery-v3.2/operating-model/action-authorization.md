# V3.1 action diagnostics — recorder-first

Engineering Relay V3.1 is a **recording and reconstruction system**, not an execution gatekeeper.

The compatibility CLI remains:

```bash
python skills/engineering-pr-delivery-v3.1/scripts/relay_can.py MATERIAL_WRITE <repo-root> --path path/to/file --base-ref origin/main
python skills/engineering-pr-delivery-v3.1/scripts/relay_can.py CHECKPOINT <repo-root> --base-ref origin/main
python skills/engineering-pr-delivery-v3.1/scripts/relay_can.py HANDOVER <repo-root>
python skills/engineering-pr-delivery-v3.1/scripts/relay_can.py MERGE <repo-root>
```

## Semantics

For every recognized action, `relay_can.py` returns `allowed: true`.

The existing fields remain useful:

- `basis` records the facts inspected;
- `blocking_controls` is a legacy field name and now lists controls that would previously have blocked the action;
- `reason_codes` records advisory conditions such as stale custody, drift, missing checkpoint, protected scope, or missing Owner delivery authority.

These are **diagnostics only**. They do not authorize or deny engineering work.

Examples:

```text
DRIFT_RELEVANT                 -> advisory
STALE_CUSTODY_EPOCH            -> advisory
CONTROL_BLOCKS_ACTION          -> advisory
CHECKPOINT_NOT_ACCEPTED        -> advisory
OWNER_DELIVERY_AUTHORITY_REQUIRED -> advisory
```

## What may still fail

Recorder-first does not mean corrupt-the-ledger-first. A write may still fail when the recorder cannot safely persist the record itself, for example:

- malformed YAML or schema-invalid object supplied to a concrete transaction;
- duplicate immutable IDs;
- unsafe/path-traversal identifiers;
- impossible file write;
- append-only event corruption;
- an interrupted atomic transaction that cannot be committed.

Those are storage/integrity failures, not programme or engineering-policy gates.

## Custody, scope, drift and controls

Custody epochs, leases, scope declarations, material drift and controls remain valuable provenance.

They answer questions such as:

- who was recorded as current;
- what scope was intended;
- whether base material moved;
- what risks or unresolved controls existed;
- what a successor should inspect.

They no longer stop MATERIAL_WRITE, TEST, CHECKPOINT, HANDOVER, delivery or closure.

## Delivery

Relay records delivery and Owner-authority observations. It does not decide whether GitHub or another provider will accept an external action. Provider permissions and explicit human decisions remain outside the recorder.
