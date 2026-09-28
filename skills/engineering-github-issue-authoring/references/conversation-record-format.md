# Responsibility-scoped conversation record

Use this format only for a substantive conversation that changes how a zero-context successor should understand the bounded engineering responsibility.

Do **not** create a global catch-all conversation ledger. Store primary-agent records on the owned implementation issue. Store Local Agent/helper conversation and return evidence on the existing governed offload/provider sub-issue. Keep RLL operational state in the existing RLL surfaces.

```text
CONVERSATION_RECORD — CX-<issue>-<serial>

AGENT_ROLE
PRIMARY_AGENT | COORDINATOR | SUCCESSOR | LOCAL_AGENT

AUTHORITY_CLASS
OWNER_AUTHORITY | OWNER_CONTEXT | NON_AUTHORITATIVE_REASONING | MATERIAL_EVIDENCE

SEMANTIC_TAGS
INTENT | INPUT | IDEA | EXPECTED_OUTPUT | QUESTION | RCA |
PROPOSAL | APPROVAL | REJECTION | AMENDMENT | RECONCILIATION | EVIDENCE

OWNER MESSAGE — VERBATIM
<<<
<relevant Owner turn, or NONE>
>>>

AGENT RESPONSE
<<<
<substantive reasoning/response, or durable summary when exact text cannot be persisted safely>
>>>

DERIVED CONSEQUENCE — NON-AUTHORITATIVE
<what this record changes for reconstruction>

AFFECTS
TASK-* | AC-* | PLAN | ROADMAP | OFFLOAD-* | RLL | NONE
```

## Persist when

A successor could make a different engineering decision because of the exchange, for example:
- new Owner input/source/example;
- Owner approval/rejection/amendment;
- RCA conclusion;
- architecture proposal with downstream consequence;
- corrected engineering assumption;
- important falsifier;
- takeover/handover interpretation;
- accepted/rejected Improvement Proposal.

## Do not persist as semantic conversation

- file reads;
- command logs;
- test retries;
- timer wakes;
- RLL lease renewals;
- routine progress chatter;
- acknowledgements with no decision consequence.

Short Owner messages such as `approve IP-01`, `merge`, or `do not implement IP-02` are semantic and should be retained with the relevant authority class.

## Existing topology

### Primary engineering agent

Post the record on the owned EP/implementation issue.

### Local Agent

Reuse the existing governed provider return sub-issue referenced by EP `offloads[]` / `OFFLOAD-*` and the generated `LOCAL-<EP>-<head>` request. The helper issue contains bounded request, helper conversation, returned evidence and unresolved/negative knowledge.

### RLL

Do not duplicate transport chatter. Keep:
- `RLL_EXECUTION_V1`;
- singular mutable `RLL_WORKER_STATE_V1`;
- authorized `RELAY_DIRECTIVE_V1`;
- `rll-*` labels.

Transport state is not engineering acceptance evidence.
