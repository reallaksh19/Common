# Topic packet and extension transaction

Exploration does not require a frozen production packet: use the [research policy](../Blueprint/V3B-Research-and-Minimum-Criteria.md). Relevant findings become a source-linked candidate/delta before promotion; only adopted dependency changes invalidate accepted evidence.

Mandatory portable payload and current-state detail: [V3B agent execution and relay](../Blueprint/V3B-Agent-Execution.md). Source summaries and answer-only packets cannot substitute for the required source/model/content dependency closure.

Every packet envelope has schema_version, packet_id, packet_type, topic_id, bucket_ids (1–3), producer_instance, producer_role, created_at, predecessor_packet_ids, exact source/gate/baseline/policy revisions, artifact manifest, review evidence, unresolved issues and next action. Digests are computed by the execution host from bytes; author-supplied hashes alone are not trust evidence.

## Packet types

| Packet | Intellectual payload | Consumer / acceptance |
|---|---|---|
| TopicRequest | Grade/exam scope, products, depth, source availability, owner purpose, knowledge/waiver if applicable | Scope planner; missing data visible |
| SourceInventory | Original objects and locations, extraction uncertainty, independent completeness comparison | Gate designer and source reviewer |
| GateProposal | Concepts, conditions, relation anatomy, representations, reasoning transitions, misconceptions, checks | Independent Physics reviewer |
| GateBaseline | Expected obligations, source basis, version and approval provenance | Structural validator; lesson author cannot edit it |
| TopicBinding | Exact selected gates, computed dependencies, bundle assignment, depth profile | Governor and work-order builder |
| StudyPlan | Intrinsic badge, fragile checkpoints, research contribution and A/B division | Core1A/1B authors |
| PracticePlan | Owner purpose, calibration basis, legal questions, support and demand dimensions | Core2A/2B authors |
| Realization | Actual explanation/equation/visual/question/answer objects and coverage | Content and source reviewers |
| ExtensionRequest | Parent versions, added/changed gates, research scope, required new evidence | Impact analysis and successor baseline |
| ChangeReceipt | Transitive affected gates/products, retained versions and stale receipts | Governor; rejects stale returns |
| ReleaseReport | All independent readiness columns and unresolved gates | Owner board; no automatic human approval |

## Minimal omission-resistant binding

A realization points both ways:
source or gate obligation → assigned Core treatment → exact content object → published location;
question → original identity/source → prompt → hints → answer/rubric → verification → prerequisite teaching.

An equation binding carries meaning, symbol definitions, conditions, frame/sign conventions where applicable, derivation obligations and checks. A representation binding carries labelled elements and the terms/steps they support. IDs without these semantic contents are insufficient for handoff.

## Reuse decisions

PROFILE_REUSE: same specialist role and instructions can be reused.
INSTANCE_REUSE: permitted for uninterrupted author continuation within unchanged scope; independent validation uses another instance.
ARTIFACT_REUSE: exact approved artifact can be reused only with compatible sources, assumptions, obligations, mode and relevant learner controls.
TOPIC_EXTENSION: new dependency closure and version; reuse unaffected artifacts and regenerate affected ones.
RESEARCH_EXTENSION: new depth/scope profile; no automatic expansion of exam scope or inherited claim of expert qualification.

The Governor records these decisions. The generating agent does not assign itself independent reviewer status.

## Crash and stale-worker recovery

Before accepting output, compare packet predecessors and gate/baseline versions with current custody. Same accepted bytes are idempotent; conflicting duplicate or stale worker output is rejected. Preserve rejected content as evidence but never replace accepted state with it.

A changed shared prerequisite invalidates all downstream consumers transitively. A newly added independent bucket does not force unrelated pages to regenerate. Removed required gates or missing closure block the extension.

Portable recovery requires original sources, actual assets, exact policy code, all accepted/rejected packets and review records; a manifest pointing to inaccessible files is not a complete handoff. This package defines that host obligation but does not claim to implement filesystem portability or model isolation.


