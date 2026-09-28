# Issue Authoring Profiles

Use these profiles to choose the amount of durable engineering structure an issue needs. They are **authoring heuristics, not qualification/admission gates**. A missing optional section must never become production permission logic.

## FOCUSED

Use for one small bounded responsibility such as:
- one concrete falsifier;
- one stale expectation correction;
- one source-derived oracle update;
- focused guardrail debt;
- one narrow integration defect.

Expected durable content:
- outcome / why now;
- owned responsibility and boundary;
- canonical input/source truth;
- preserve/invariants;
- falsifier;
- acceptance criteria;
- implementation-plan surface;
- expected handoff;
- parent/EP/consumer refs where applicable.

Do not inflate a focused issue into a programme specification.

## DETAILED

Use for a substantial single engineering responsibility where a zero-context successor must understand source authority, current production path, acceptance, validation, protected domains and handoff without replaying chat history.

Expected durable content:
- mission;
- creation-time ground truth;
- Original Intent ref when direct Owner source exists;
- Owner task/expected-output ledger;
- Roadmap/authority refs;
- INPUT-* source inventory;
- current production/repository path;
- AC-* acceptance denominator;
- implementation direction without replacing the agent-authored plan;
- BM-* benchmark/oracle programme where applicable;
- VAL-* validation expectations;
- protected domains and falsifiers;
- dependencies/consumers;
- explicit exclusions;
- Definition of Done;
- reconstruction topology covering EP / Local Agent / RLL / Handover where present.

## PROGRAMME

Use when one Owner outcome spans multiple responsibilities/agents/PRs, shared source truth, producer-consumer edges or integration/exit work.

Expected durable content:
- everything materially relevant from DETAILED;
- stable TASK-* Owner requirements;
- RM-* roadmap bindings;
- versioned INPUT/BM/VAL/RM common sets;
- workstream/ownership registry;
- producer/consumer contracts;
- dependency contracts expressed as required production outputs;
- EXIT-* programme denominator;
- [Original Intent] source issue;
- [Relay Handover] operational ledger;
- explicit EP / Local Agent / RLL reconstruction refs.

## Selection rule

Choose the smallest profile that still lets a new engineer answer:

1. What did the Owner actually ask for?
2. What does the live system do now?
3. What exactly does this responsibility own?
4. What source/input is authoritative?
5. What result proves success?
6. What must remain unchanged?
7. What would falsify the current diagnosis?
8. Who consumes the output?
9. What active work can overlap/conflict?
10. Where are Original Intent, EP, Local Agent, RLL and Handover records when they exist?

If an answer cannot be established, write `UNRESOLVED`, `UNKNOWN`, `NOT_YET_GROUNDED`, or `OWNER_DECISION_REQUIRED`. Do not block issue creation merely because uncertainty exists.
