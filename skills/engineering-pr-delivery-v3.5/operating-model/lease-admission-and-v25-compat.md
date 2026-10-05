# V3.1 lease recording and historical compatibility

A V3.1 lease records the **current actor pointer and provenance**. It is not an exclusive lock.

## Admission

`lease_admission.py` creates a schema-valid lease record.

Methods remain as descriptive metadata:

- `DETERMINISTIC`
- `QUALIFIED`
- `OWNER_OVERRIDE`

Qualification policy is recorded but does not prevent a deterministic executor from being recorded. A previous ACTIVE lease does not prevent a new executor from being recorded.

## Takeover and recovery

A successor does not need to prove abandonment before taking over the recorder.

When a different executor activates a new lease:

- a fresh handover, when available, is recorded as HANDOFF;
- otherwise the transition is recorded as RECOVERY;
- the predecessor lease is invalidated/released as transition history;
- the custody epoch advances for provenance.

The following are diagnostics only:

- lease age;
- inactivity horizon;
- terminal-session evidence;
- changed sensitive/dependency material;
- stale or omitted expected custody epoch;
- programme-frontier assessment.

In particular, `UNACCEPTED_MATERIAL_ACTIVITY_PRESENT` is recorded as recovery context and **never blocks takeover**.

## Liveness

Renewal timestamps and material activity digests remain useful for reconstruction. They are not permission tokens.

## Owner override

OWNER_OVERRIDE remains a descriptive admission form. It does not imply merge/release permission, but Relay itself does not use that absence as an execution blocker.

## Historical protocol material

Older protocol state may remain readable for reconstruction. V3.1 recorder-first does not use older protocol generations as fallback execution authority.
