# V3 lease admission and V2.5 compatibility

V3-5 replaces normal future receipt proliferation with one native lease admission object while preserving V2.5 evidence as historical evidence.

## Native admission

`lease_admission.py` builds a schema-valid native `LEASE-*` from the current V3 STATE/EP.

Methods:
- `DETERMINISTIC` — repository-grounded admission when EP policy does not require qualification;
- `QUALIFIED` — embeds qset, independent evaluator identity, PASS result and durable qualification evidence inside the lease;
- `OWNER_OVERRIDE` — represents direct bounded Owner execution authority as Owner authority, not fake discovery/qualification.

Example:

```bash
python skills/engineering-pr-delivery-v3.1/scripts/lease_admission.py . \
  --lease-id LEASE-001 \
  --executor-id agent-A \
  --method DETERMINISTIC
```

For qualified work:

```bash
python skills/engineering-pr-delivery-v3.1/scripts/lease_admission.py . \
  --lease-id LEASE-002 \
  --executor-id agent-B \
  --method QUALIFIED \
  --qualification qualification.yaml
```

The admission builder does **not** persist or activate the lease. V3-6 transactional commands own atomic LEASE + STATE mutation. This avoids introducing a half-transaction before the transactional layer exists.

An ACTIVE lease already owned by a different executor prevents a new lease from being admitted for that route until release/transfer.


## Custody liveness and abandoned-agent recovery

New native leases are epoch-fenced and default to a 300-second inactivity recovery horizon.

Normal governed activity by the current lease executor refreshes liveness in the same transaction; Relay does not require a background heartbeat daemon. When the command has a material basis, the lease also records digests of the current sensitive and dependency worktrees. These are abandonment/liveness evidence only, not accepted material authority.

Timeout-based recovery therefore requires both:

1. the persisted inactivity horizon has elapsed; and
2. the current sensitive/dependency worktree still matches the predecessor's last recorded activity basis.

If worktree material changed after the last activity record, timeout-only takeover is refused. An exact provider/session termination observation bound to the predecessor lease, executor and custody epoch may instead establish immediate abandonment evidence.

Recovery still advances the custody epoch and invalidates predecessor custody. Programme reconciliation remains a separate prerequisite before a provider-backed EP can be continued.

Legacy native leases without complete liveness fields remain readable and are not partially upgraded by unrelated commands.

## EP admission policy

An EP may declare:

```yaml
admission_policy:
  qualification: REQUIRED
  question_policy: Q1_Q5
```

If qualification is required, deterministic admission is rejected. A qualified evaluator cannot be the execution candidate.

## Owner override

OWNER_OVERRIDE requires a direct-utterance digest, session timestamp and bounded branch. Its generated lease authority excludes MERGE and RELEASE and carries EP write scope plus explicit prohibitions.

## V2.5 compatibility

`v25_lease_view.py` reads the current V2.5 takeover admission and its DISC / optional QUAL / TC evidence. Its CLI first executes the existing V2.5 takeover validator.

Its output is explicitly:

```yaml
authority: DERIVED_COMPATIBILITY_VIEW
native_lease: false
may_authorize_v3_actions: false
```

The view can inform migration and handover. It cannot directly authorize V3 material actions and it does not write synthetic V3 events.

This preserves the rule:

> V2.5 history remains inspectable; migration must not rewrite historical evidence into fictitious V3-native events.
