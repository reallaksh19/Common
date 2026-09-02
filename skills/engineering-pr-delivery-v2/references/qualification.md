# Relay Takeover Qualification

## Purpose

Qualification answers one question:

> Can this incoming agent safely perform the next unresolved engineering leg against the current repository state?

It is not a retrospective score for the outgoing agent and not a theory quiz.

Qualification is a **takeover/recovery gate**. It must not be repurposed to stop a continuous active agent that is already executing the same bounded leg under explicit owner authorization and a durably recorded continuation basis.

## Applicability

Use candidate/verifier qualification when engineering-critical authority is being transferred or reconstructed, including:

```text
new incoming engineering agent
abrupt-agent recovery
session/agent handoff where continuity cannot be established
materially changed unresolved leg being taken over by a different candidate
```

Do not create an artificial candidate/verifier loop merely because:

```text
the same active agent created a new endpoint
the owner explicitly said proceed/continue/next
a relay metadata commit moved the branch head
```

For continuous owner-authorized work, use the continuation rules in `SKILL.md#6A` and record the bounded authority in a pre-mutation endpoint.

## Separation of roles

For takeover qualification, use three logical roles where possible:

```text
OUTGOING / ENDPOINT AUTHOR
  -> prepares the next-leg question set as part of the endpoint

INCOMING CANDIDATE
  -> answers from live repository evidence while READ_ONLY

VERIFIER
  -> independently evaluates the candidate answer and grants or denies takeover authority
```

Hard rule:

```text
candidate_id == verifier_id
-> SELF_VERIFIED
-> cannot grant WRITE_ALLOWED for engineering-critical takeover mutation
```

The same person/system may prepare an endpoint and later serve as verifier for a different candidate if independence and repository evidence remain valid. The candidate never grants itself authority.

A continuous active agent under `OWNER_AUTHORIZED_CONTINUATION` is not a takeover candidate and therefore does not create a self-verdict artifact. Its authority derives from explicit owner authorization plus a bounded durable continuation endpoint, not from claiming that its own engineering judgment is independent verification.

## Continuous owner-authorized continuation

Before engineering-critical mutation without a takeover verifier, the continuous active agent must durably record:

```text
CONTINUATION_MODE: OWNER_AUTHORIZED_CONTINUATION
CONTINUATION_AGENT_ID:
CONTINUATION_BASIS_HEAD:
OWNER_AUTHORIZATION_EVIDENCE:
ENGINEERING_CRITICAL_WRITE_AUTHORITY: BOUNDED
AUTHORIZED_SCOPE:
PROHIBITED_SCOPE:
PROTECTED_INVARIANTS:
VALIDATION_OR_FALSIFIER:
ROLLBACK_OR_STOP_CONDITION:
MERGE_AUTHORITY: OWNER_ONLY
```

The following are not waived:

- authoritative-source custody;
- preimage/postimage or equivalent engineering validation;
- independent oracle requirements where the engineering method itself requires one;
- exact changed-file/scope review;
- NOT_RUN visibility;
- multi-agent coordination;
- destructive-operation restrictions;
- merge authorization.

Continuation authority ends immediately on material scope expansion, source-authority contradiction, uncontrolled base drift, blocked/unknown coordination, owner revocation, or handoff to another engineering agent.

## Question timing

Q1-Q5 exist at every non-terminal endpoint, not only graceful handoff.

This ensures abrupt agent loss does not remove the next-agent exam.

When the endpoint's unresolved work changes materially, create a new endpoint and new question set.

For continuous active work, Q1-Q5 are recovery/takeover material for the **next** agent; the current agent is not required to answer its own endpoint to continue an already owner-authorized bounded leg.

## Mandatory questions

Exactly five questions:

### Q1 — Production Trace

Require the candidate to trace one critical current value/state through actual live production files/functions/data boundaries.

Evidence should include concrete repository anchors and the first boundary where the value could become wrong.

### Q2 — Current Unresolved Problem / Failure Isolation

Use an actual current failure, blocker, risk, unresolved question, or active hypothesis.

Require:

```text
minimum isolating experiment
prediction
falsifier
first wrong boundary
```

### Q3 — Authority / Invariant

Require identification of:

```text
authoritative source
owned/derived data boundaries
what may change
what must not change
one plausible but invalid shortcut/fix
```

### Q4 — Independent Validation

Require an independent or authoritative basis where available:

```text
analytical/hand calculation
authoritative published/reference result
independent arithmetic
cross-solver
experimental evidence
independently frozen expected value
```

Require units/sign conventions/tolerance/provenance and limitations.

### Q5 — Next Contribution / Minimal Patch

Require the smallest legitimate next engineering contribution:

```text
exact file/function/domain
expected changed files
protected unchanged files/domains
focused tests/evidence
rollback/falsifier boundary
```

## Question quality gate

Reject any question that:

- can be answered correctly without the current repository;
- could be copied unchanged into an unrelated task;
- asks mainly about completed work rather than the next unresolved leg;
- has no required repository evidence;
- lacks a falsifiable prediction/decision where applicable;
- does not test knowledge needed for the next contribution.

Avoid generic prompts such as:

```text
What is FEA?
Explain WRC 537.
Describe validation.
What is dependency injection?
```

## Candidate answer artifact

For takeover qualification, store outside `agentchain.md`, for example:

```text
agents/qualifications/<CHAIN_ID>/<QUESTION_SET_ID>-<candidate>-answer.md
```

Minimum header:

```text
CHAIN_ID:
ENDPOINT_ID:
QUESTION_SET_ID:
QUALIFICATION_BASIS_HEAD:
CANDIDATE_ID:
LIVE_PR_HEAD_OBSERVED:
LIVE_MAIN_HEAD_OBSERVED:
RECONCILIATION: MATCH | METADATA_DRIFT | MATERIAL_DRIFT | CONTRADICTION
```

Then answer Q1-Q5 with concrete evidence.

The candidate may identify uncertainty but must not assign final authorization to itself.

## Verifier verdict artifact

Recommended path:

```text
agents/qualifications/<CHAIN_ID>/<QUESTION_SET_ID>-<candidate>-verdict.md
```

Minimum header:

```text
CHAIN_ID:
ENDPOINT_ID:
QUESTION_SET_ID:
QUALIFICATION_BASIS_HEAD:
CANDIDATE_ID:
VERIFIER_ID:
VERDICT_BASIS_HEAD:
```

Score each question:

```text
Q1 __/20
Q2 __/20
Q3 __/20
Q4 __/20
Q5 __/20
TOTAL __/100
MINIMUM_QUESTION __/20
```

Default engineering-critical takeover pass:

```text
total >= 92/100
minimum each >= 17/20
```

Verdict:

```text
PASS_WRITE_ALLOWED
FAIL_READ_ONLY
STALE_REQUALIFICATION_REQUIRED
INVALID_SELF_VERIFIED
```

## Scoring guidance

Per question, a useful default rubric is:

```text
Repository evidence          /6
Correct implementation trace /5
Engineering reasoning        /4
Falsifiable validation       /3
Authority/scope protection   /2
Total                       /20
```

Adjust emphasis only when the endpoint clearly requires a different engineering competency.

## Automatic failure conditions

Regardless of numerical score, fail takeover qualification for material instances of:

- fabricated repository evidence or invented objects;
- unsafe engineering claims;
- expected values replaced from production output and called independent;
- tolerance weakening solely to force PASS;
- NOT_RUN represented as PASS;
- silent fallback authority;
- benchmark/oracle corruption;
- shotgun changes to multiple numerical mechanisms without isolation when isolation is possible;
- candidate self-verification presented as independent authorization.

The same anti-gaming rules apply to owner-authorized continuation even though no candidate/verifier artifact is involved.

## Freshness

The takeover question set is bound to:

```text
ENDPOINT_ID
QUALIFICATION_BASIS_HEAD
current unresolved problem
```

Material drift requires re-grounding and normally a new question set.

Do not invalidate solely because an `agentchain.md` metadata commit moved the branch head while production/test/source authority remained materially unchanged.

A continuation endpoint is separately bound to `CONTINUATION_BASIS_HEAD` and `AUTHORIZED_SCOPE`; material scope drift requires a new continuation endpoint before further mutation.

## No independent verifier available

For an **incoming takeover candidate**, use:

```text
QUALIFICATION_STATUS: DEFERRED_VERIFICATION
TAKEOVER_AUTHORITY: READ_ONLY
```

The takeover candidate may continue inspection, reproduction, and evidence gathering. It may not invent a verifier or self-grant engineering-critical takeover authority.

For a **continuous active agent**, absence of a verifier is not itself a blocker when the owner has explicitly authorized continuation and the Section 6A continuation controls are satisfied. Do not mislabel that agent as a takeover candidate solely to force a verifier cycle.
