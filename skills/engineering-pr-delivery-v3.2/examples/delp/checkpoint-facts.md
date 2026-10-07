TASK_EVIDENCE — CHECKPOINT

U01 and U02 are implemented and verified on the current head. Negative knowledge: the cached fixture path
is not used by the replay lane. Next: build the replay lane (U03).

```yaml
CHECKPOINT_FACTS_V1:
  responsibility: {issue: Common#592, id: P3-I-R2}
  material: {pr: Common#593, candidate_sha: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa}
  units:
    - id: U01
      state: COMPLETE
      result: VERIFIED
      evidence_refs: [Common#592#issuecomment-101]
    - id: U02
      state: COMPLETE
      result: VERIFIED
      evidence_refs: [Common#592#issuecomment-101, Common#593#check-run-77]
  activity: ACTIVE
  next: {unit: U03, action: build the replay lane}
  blocker: NONE
  owner_action: NONE
```
