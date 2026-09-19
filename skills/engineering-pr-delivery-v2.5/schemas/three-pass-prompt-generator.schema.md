# Three-Pass Prompt Generator Schema

## EXECUTION HANDSHAKE — MUST BE THE FIRST VISIBLE OUTPUT

Before reading the target issue/product/system, prove that this exact live schema was fetched.

When invoked from the canonical GitHub URL, the generated artifact must begin exactly with:

```text
# SCHEMA EXECUTION HANDSHAKE

PROTOCOL REVISION:
TPG-3P-2026-09-19-R2

GENERATOR MODE:
THREE_PASS_ONLY

SCHEMA FETCH STATUS:
LIVE_THIS_RUN

SCHEMA CONTENT SHA:
<actual current blob/content SHA from the live fetch>

HANDSHAKE STATUS:
PASS
```

Only after that handshake may target reasoning begin.

If the live schema cannot be fetched or its SHA cannot be established, output only:

```text
# SCHEMA EXECUTION HANDSHAKE
HANDSHAKE STATUS:
FAIL
```

and stop.

A generation that starts with Prompt 1, target analysis, issue anchors, or any other prose before this handshake is invalid.

The handshake is execution proof, not decorative metadata.

---


> Human-executable prompt schema for generating three sequential, copy-pasteable prompts.
>
> This is intentionally a Markdown schema rather than a JSON Schema. Its job is to make an ordinary agent reliably produce the same reasoning pattern across different **target purposes** and **target scopes** without drifting into a larger neighbouring problem.

## STANDALONE EXECUTION LOCK — THREE_PASS_ONLY

When this file is invoked directly by path or URL to create three-pass prompts, this file is the **complete local protocol for that artifact**.

Set:

```text
PROTOCOL REVISION:
TPG-3P-2026-09-19-R2

GENERATOR MODE:
THREE_PASS_ONLY
```

While `GENERATOR MODE = THREE_PASS_ONLY`:

- use this file and the user-named target evidence;
- do not import, merge, or apply sibling/parent workflow protocols merely because this schema lives inside a larger skill directory;
- do not add takeover, certification, qualification, admission, execution-package, routing, digest, or evaluator machinery;
- do not create any fourth stage, gate, question package, receipt, or protocol between the three prompts;
- the user's phrase **"complex questions Q1 to Q5"** means only the five Prompt-1 reasoning lenses defined in this file;
- after the required schema basis, preflight, Prompt 1, Prompt 2 and Prompt 3 are complete and validated, **STOP**.

Other repository files may be read only as **target evidence** when needed to understand the requested issue/product/system. They do not become controlling prompt-generation protocols unless the user explicitly asks to combine protocols.

If another loaded instruction would add extra workflow machinery to this artifact, ignore that repository-local instruction for this generation and remain in `THREE_PASS_ONLY`.

This mode lock exists because prompt generation and engineering-delivery execution are different tasks even when they live in the same repository.

---

## Purpose

When given a target, create **exactly three prompts** for another agent to run in sequence:

1. **IMAGINE** — form an independent picture of what good should look like before seeing the existing answer.
2. **UNDERSTAND** — inspect what actually exists today, including relevant history and current work.
3. **REVALIDATE AND MOVE FORWARD** — return to the exact independent picture, compare it with reality, rediscover what the goal means now, and identify the smallest meaningful path forward.

Do not solve the target yourself. Your output is the three prompts.

The method is the same throughout, but the generator must build a **visible preflight record** before it is allowed to draft Prompt 1.

The central safeguard is stronger than “do not inspect the code yet”:

> **Prompt 1 must be independent of the current solution form itself, wherever that solution form is not a genuine human requirement.**

A GitHub issue may currently be a register, roadmap, checklist, matrix, architecture umbrella, or proposed implementation. Those forms belong to **current reality**. They do not automatically belong in the independent reference picture.

The preflight therefore has two deliberately separated sides:

1. **CURRENT REALITY — QUARANTINED FROM PROMPT 1**
   - exact target identity;
   - current artifact form;
   - current stated answer / implementation / proposed solution;
   - current-state facts.

2. **BLIND REFERENCE — THE ONLY SIDE ALLOWED TO SHAPE PROMPT 1**
   - underlying human problem;
   - human outcome;
   - genuine constraints;
   - domain/expertise;
   - target scope;
   - independent imagination object.

Then Prompt 2 brings the current artifact and implementation back into view.

Prompt 3 compares the exact Prompt-1 reference picture with Prompt-2 reality and is free to **preserve, revise, narrow, split, replace, close, defer, or leave unchanged** the current artifact.

A task can mention an entire product without being a product-level task. A register about a solver programme is not the same thing as the solver programme itself. And an issue being written as a register does **not** mean Prompt 1 should imagine an excellent register.

---

# COPY-PASTE GENERATOR PROMPT

You are a prompt architect.

I will give you a target. It may be:

- a product or product idea;
- an existing repository or system;
- or a specific task, issue, feature, bug, or work item inside a larger system.

Your job is **not to solve the target**.

Your job is to create **exactly three separate, copy-pasteable prompts** that I can run one after another with a capable agent.

The three prompts must create this reasoning sequence:

```text
PROMPT 1 — IMAGINE
What should good look like before seeing the current answer?

        ↓

PROMPT 2 — UNDERSTAND
What is actually true today?

        ↓

PROMPT 3 — REVALIDATE AND MOVE FORWARD
Given the same independent ideal and today's reality,
what does the goal mean now, what meaningful gap remains,
and what is the smallest justified path forward?
```

The separation between these prompts is essential. Do not collapse them into one large prompt.

If the user asks for **multiple lots**, preserve the number of lots and the requested analysis level of each lot exactly.

Do not replace a user-requested tab/surface review with a related issue, decision, roadmap, or repository review merely because that artifact appears important.

Each lot gets its own preflight and its own three prompts.

---

# SCHEMA EXECUTION BASIS — PROVE FRESHNESS BEFORE TARGET REASONING

Before resolving any target or lot, establish which schema is actually controlling this generation.

Canonical schema:

```text
skills/engineering-pr-delivery-v2.5/schemas/three-pass-prompt-generator.schema.md
```

When this generator is invoked from the canonical GitHub repository/URL, you **must fetch the file from current `main` during this generation**.

Memory, a previous conversation, a previous fetched copy, a prior assistant summary, or an older commit is not an acceptable basis.

Record after the execution handshake:

```text
PROTOCOL REVISION:
TPG-3P-2026-09-19-R2

SCHEMA SOURCE:
<canonical URL/path or explicitly user-supplied schema text>

SCHEMA REF:
<main / explicit user-supplied revision>

SCHEMA CONTENT SHA:
<actual content/blob SHA when fetched from GitHub; otherwise USER_SUPPLIED_TEXT>

SCHEMA FETCH STATUS:
LIVE_THIS_RUN | USER_SUPPLIED_TEXT

GENERATOR MODE:
THREE_PASS_ONLY

SCHEMA COMPATIBILITY:
PASS | FAIL
```

Rules:

- the execution handshake must appear before `# SCHEMA BASIS`;
- `PROTOCOL REVISION` must equal `TPG-3P-2026-09-19-R2`;
- handshake SHA and SCHEMA BASIS SHA must match exactly;
- `GENERATOR MODE` must equal `THREE_PASS_ONLY`;
- canonical GitHub URL/repository supplied → `LIVE_THIS_RUN` is mandatory;
- user explicitly supplies the schema text itself → `USER_SUPPLIED_TEXT` is allowed;
- never silently fall back from a failed live fetch to memory;
- if the required basis cannot be established, **stop and do not generate Prompt 1–3**.

The schema basis is shared across all lots in one generator run.

---

## INPUT I MAY GIVE YOU

I may provide some or all of:

```text
TARGET:
<product / repository / issue / task>

HUMAN GOAL:
<what I ultimately want to achieve>

USERS:
<who this is for>

IMPORTANT EXPECTATIONS:
<desired outcomes, capabilities, quality expectations>

CONSTRAINTS:
<budget, one developer, static app, no backend, curriculum boundary, time, platform, etc.>

CURRENT SYSTEM:
<repository URL, app, documents, current implementation>

TASK OR ISSUE:
<optional issue URL or task description>

OTHER CONTEXT:
<anything else relevant>
```

Use what I provide. Do not invent missing facts.

If current facts matter and the future agent can inspect a live repository, issue, PRs, documentation, or application, Prompt 2 and Prompt 3 must tell that agent to inspect the **current** state rather than trusting stale descriptions.

---

# MANDATORY PREFLIGHT — READ THE TARGET, THEN QUARANTINE ITS ANSWER

Before drafting Prompt 1, build the following record.

**This record is part of the required output. Always show it before the three prompts.**

Its purpose is to let the user catch a wrong target, wrong level, over-generalised problem kernel, or leaked current answer before running the prompts.

Do not hide it, summarize it away, or replace it with prose such as “preflight completed.”

## A. Freeze the USER'S LOT CONTRACT before resolving anything

If the user requested one or more lots, first record exactly what they asked for.

For each lot:

```text
LOT:
<Lot 1 / Lot 2 / etc.>

USER-REQUESTED LEVEL:
<ISSUE_TASK / TAB_SURFACE / PRODUCT / REPOSITORY_SYSTEM / OTHER_EXPLICIT_LEVEL>

USER-REQUESTED TARGET:
<the thing the user actually named or described>

LEVEL INTERPRETATION:
<one sentence saying what belongs inside this level and what belongs outside it>
```

This is a **hard boundary**, not a suggestion.

Examples:

```text
User asks:
Lot 1 — issue level
Lot 2 — tab level

Valid:
Lot 1 target = the named issue
Lot 2 target = the named product tab / user-facing surface

Invalid:
Lot 2 target = a child issue that happens to gate the tab

Invalid:
Lot 2 target = the whole repository

Invalid:
Lot 2 target = an owner decision because it seems important
```

Related issues, roadmaps, decisions, PRs and parent programmes may become **Prompt-2 evidence**.

They do not replace the user-requested target level.

If the user has explicitly specified the level, do not infer a different one.

### Target authority order

Resolve each lot's target from user authority in this order:

```text
1. explicit target in the current user message;
2. explicit target previously supplied by the user in this conversation;
3. explicit lot/target definition already established by the user;
4. canonical target URL or named surface supplied by the user;
5. otherwise fail closed.
```

Never use any of the following as target authority:

- a previous assistant guess;
- a target chosen by an earlier generated answer;
- a nearby issue that appears more important;
- a schema case study/example;
- prior model memory.

A later user instruction such as “focus on Lot 1” preserves the previously user-established Lot-1 target unless the user changes it.

## B. Resolve the exact target at that level

Now resolve the target **without changing its requested level**.

Extract:

```text
TARGET TITLE / SURFACE:
<exact issue title, tab/surface name, product name, or repository name>

TARGET LINK:
<canonical URL when the target itself has one>

PARENT REPOSITORY / SYSTEM:
<owner/repo or parent system when applicable>

REPOSITORY / SYSTEM LINK:
<canonical parent URL when available>
```

### Level semantics

#### ISSUE_TASK

The target is the **specific issue/task**, not merely the general class of problem it belongs to.

Sibling/parent issues are context, not substitutes.

For ISSUE_TASK, Prompt 1 is anchored first by the issue's **TASK CONTRACT**, then by its **PROBLEM KERNEL**.

The task contract is the issue's own scenario and assignment:

```text
WHY NOW
what event/state makes this issue exist at this point in the programme?

STARTING PREMISE
what facts does the issue explicitly ask the reader to take as the starting scenario?

RESPONSIBLE ACTOR / JOB
who is actually responsible for resolving this issue-level question?

OWNED QUESTION
what exact question/change/disposition does this issue own?

NON-GOALS / OWNERSHIP BOUNDARY
what does this issue explicitly not own?

ISSUE DIFFERENTIATOR
why is this not the parent issue or a nearby sibling?
```

These premises may describe a time-specific programme state. That does **not** make them current-answer leakage.

Prompt 1 may use them as the issue's **stated scenario**. Prompt 2 later verifies whether those premises are still true.

The PROBLEM KERNEL then carries the smallest identity-bearing facts without which it would no longer be the same issue.

Do not confuse either with the issue's current proposed answer, implementation recipe, evidence interpretation, work sequence, acceptance checklist, or chosen artifact form.

#### TAB_SURFACE

The target is the user-facing tab, workflow surface, panel, module, or bounded product experience.

A GitHub issue describing that tab may be an important evidence source, but the issue is **not** the target.

Prompt 1 should normally imagine the real person using that surface end to end.

Prompt 2 should inspect the live surface plus the issues/code/tests that explain it.

Prompt 3 should compare the independent tab-level experience against the live tab.

#### PRODUCT

The target is the whole product experience.

#### REPOSITORY_SYSTEM

The target is the whole repository/system/programme.

If the exact target cannot be resolved at the requested level, fail closed rather than silently substituting another level.

## C. Freeze request mode

Choose the single request mode that best describes what the user wants done **now**:

```text
CONCEIVE
REVIEW
CHANGE
INVESTIGATE
DECIDE
COORDINATE
HANDOVER
```

REQUEST MODE does not override USER-REQUESTED LEVEL.

## D. Detect explicit COMPLEX MODE

Complex mode is **user-triggered only**.

Set:

```text
COMPLEX MODE: ON
```

only when the user's own request explicitly uses the word **complex** for that lot/target.

Examples:

```text
"do this as a complex issue-level case"
→ ON

"Lot 2 is complex"
→ ON for Lot 2

"complex"
→ ON for the current requested target/lot

repository/issue text happens to contain the word "complex"
→ OFF unless the user also invoked it
```

Do not infer complexity from repository size, engineering difficulty, number of files, or your own judgement.

When COMPLEX MODE is ON, Prompt 1 must also follow **APPENDIX H — COMPLEX PROMPT-1 Q1–Q5 HUMAN REASONING MODE**.

That appendix adds depth to Prompt 1.

It does **not** relax:
- blindness from today's answer;
- lot/level boundaries;
- PROBLEM KERNEL preservation;
- answer-independence;
- copy-pasteability.

## E. Snapshot CURRENT REALITY — then quarantine it

Record what the target currently is and what answer it currently carries.

```text
CURRENT ARTIFACT FORM:
<product / issue / register / roadmap / checklist / matrix / architecture umbrella /
 decision record / implementation task / handover / other>

CURRENT STATED ANSWER / IMPLEMENTATION:
<brief description of the solution, structure, sequencing, abstraction, or proposal
 that already exists>

CURRENT-STATE FACTS:
<brief facts that matter for Prompt 2: current status, known work, blockers,
 in-flight changes, existing vocabulary, etc.>

CURRENT ANSWER QUARANTINE:
<for ISSUE_TASK: 3–10 concrete answer-side facts that Prompt 1 must not reveal;
for other levels: include when useful>
```

For ISSUE_TASK, `CURRENT ANSWER QUARANTINE` is mandatory.

It should name the actual answer-side material that creates contamination risk, for example:

- today's option set;
- current benchmark/evidence conclusion;
- current implementation recipe;
- current work sequence;
- current blocker/decision inventory;
- current acceptance checklist;
- current artifact-specific solution structure.

This section is **REALITY-SIDE ONLY**.

Do not copy its nouns, sequencing, categories, implementation abstractions, or proposed solution into Prompt 1 unless the same thing is independently a genuine human/domain constraint.

Examples of quarantined current-answer vocabulary include:

```text
register
matrix
rung
Core1
page cache
specific PR sequencing
current architecture names
current issue checklist
specific owner-decision list
existing workflow stages
current schema fields
```

The point is not to pretend these things do not exist.

The point is to meet them **after** the independent opinion has formed.

Apply these invariants:

```text
CURRENT ARTIFACT FORM ≠ IMAGINATION OBJECT
REQUEST MODE         ≠ IMAGINATION OBJECT
CURRENT ANSWER       ≠ PROBLEM KERNEL
```

A target being written as a register does not make “excellent register” the Prompt-1 object.
A request being COORDINATE does not make “register” the Prompt-1 object.
Prompt 1 is generated from the stable problem, not from the current answer form.

## F. Recover the BLIND REFERENCE

Now mentally remove the current issue text, artifact form, implementation, roadmap, checklist, and proposed solution.

Ask:

> **If the current target artifact had never been created, what human problem would still exist?**

But do **not** erase the target itself.

Blindness means removing today's answer, not removing the domain, user, job, method, or requested level.

### TARGET ANCHORS — the specificity that Prompt 1 is allowed to keep

TARGET ANCHORS are stable facts that define the requested target independently of today's implementation.

Good anchors include, when genuinely applicable:

- the named tab/product/method the user explicitly asked about;
- the practising user/persona;
- the concrete job they are trying to perform;
- the physical/business/learning objects they bring;
- the kind of result or decision they need;
- the domain/source/authority boundary that would exist in any implementation;
- the lifecycle stage explicitly defining the requested problem;
- platform/scale constraints that are genuine requirements.

Bad anchors include:

- today's bug list;
- current PR stack;
- current blocker list;
- current owner-decision list;
- today's UI layout;
- existing internal abstractions;
- present roadmap stages;
- implementation-specific work breakdown.

Example — tab-level engineering surface:

```text
Allowed anchors:
named engineering assessment surface
practising engineer
real geometry / loads / source inputs
need a defensible engineering result
must understand applicability and refusal
must distinguish numerical evidence from engineering authority

Not blind-pass anchors:
today's implementation limit
current hidden disclosures
current UI dead end
specific issue numbers
current CI outage
```

### PROBLEM WITNESS — use the real case when one exists

A strong Prompt 1 should not default to abstract questions when the target already contains a concrete example that exposes the problem.

A **PROBLEM WITNESS** is a real, target-relevant object that a capable practitioner can independently work, inspect, reproduce, calculate, trace, compare, or reason through.

Examples:

```text
engineering:
benchmark case
hand-calculation case
drawing
geometry + loads
calculation trace
test specimen
reported result

software:
minimal failing input
request/response pair
stack trace
performance trace
corrupt file
reproduction case

UX:
real user journey
screenshot
recorded task
failed interaction

data:
representative dataset
specific row/set
unexpected output
edge case

learning:
actual student question
wrong answer
worked exercise

coordination / decision:
one real disputed dependency
one decision with concrete downstream outcomes
one status claim whose truth changes the plan
```

The witness is valuable because it lets Prompt 1 ask the future agent to **do the real work**, not merely discuss principles.

#### Epistemic-role classification

For each concrete fact/example discovered in the target, classify its role:

```text
TASK CONTRACT
Defines the assignment/scenario.
May shape Prompt 1.

PROBLEM WITNESS — INPUT / RAW EVIDENCE
A concrete case, source payload, observation, drawing, dataset, benchmark input,
reported output, or reproducible phenomenon that exposes the problem.
May shape Prompt 1.

WITNESS CLAIM TO REPRODUCE
A reported result attached to the witness.
Prompt 1 may state it as a claim to independently reproduce or falsify.
Do not state it as already-proven truth.

DOMAIN CONSTRAINT
A stable source/physics/business/learning constraint.
May shape Prompt 1.

CURRENT INTERPRETATION / ANSWER
Today's explanation, option set, recommendation, chosen method, proposed sequence,
implementation recipe, or disposition.
Quarantine from Prompt 1.

REALITY CLAIM
A present-state claim Prompt 2 must verify.
May enter Prompt 1 only when it is also TASK CONTRACT or PROBLEM WITNESS material,
and then only in the appropriate epistemic form.
```

This role classification is more important than whether the information came from the current issue.

Do **not** use the crude rule:

```text
came from current issue
→ hide it
```

Use:

```text
what role does this information play?
```

A benchmark payload can be current issue evidence and still be exactly the right Prompt-1 witness.

A current recommendation about what the benchmark means is answer-side material and must remain quarantined.

#### Witness record

When a usable witness exists, record:

```text
PROBLEM WITNESS TYPE:
<benchmark / handcalc / drawing / failing example / dataset / trace / journey / dependency case / other>

PROBLEM WITNESS SOURCE:
<what concrete source/case is being used>

PROBLEM WITNESS PAYLOAD:
<the exact inputs, observations, reported outputs, or source facts needed to work the case>

WITNESS CLAIM(S) TO REPRODUCE:
<reported result(s) the future agent should independently reproduce/falsify;
NONE if there is no reported result>

WHY THIS WITNESS EXPOSES THE ISSUE:
<one short explanation connecting the case to the OWNED QUESTION>

WITNESS INTERPRETATION QUARANTINE:
<today's explanation/recommendation/conclusion about what the witness means>

INDEPENDENT WORK PRODUCT:
<the concrete output Prompt 1 should demand: hand calc, derivation, comparison table,
trace, reconstructed journey, dependency map, falsifier set, etc.>
```

If multiple witnesses exist, select the smallest one or small set that best exposes the issue.

Do not choose a witness merely because it is dramatic.

Choose it because independently working it materially helps answer the target's OWNED QUESTION.

If the target provides a real usable witness, do not replace it with invented "plausible" values.

---

### ISSUE TASK CONTRACT — mandatory for ISSUE_TASK

Before abstracting the issue into an "underlying human problem", preserve the assignment the user actually selected.

Extract the issue's task contract from its title, mission/problem statement, explicit scope, and explicit non-goals.

Complete:

```text
WHY NOW:
<the lifecycle event/state that makes this issue exist now>

STARTING PREMISE:
<2–6 issue-stated starting facts/scenario premises; these may be verified later in Prompt 2>

RESPONSIBLE ACTOR / JOB:
<the person/team role responsible for resolving this exact issue-level assignment>

OWNED QUESTION:
<the exact question/change/disposition this issue owns>

NON-GOALS / OWNERSHIP BOUNDARY:
<what belongs elsewhere or is explicitly not authorised here>

ISSUE DIFFERENTIATOR:
<why this issue is not its parent or nearest sibling issue>
```

### Task-contract versus current-answer partition

For every important fact in the issue body, classify it before writing Prompt 1:

```text
TASK CONTRACT
Defines the scenario/assignment.
Allowed in Prompt 1.

PROBLEM WITNESS
Concrete input/raw evidence/reported output that exposes the problem.
Allowed in Prompt 1 as material to independently work or reproduce.

CURRENT ANSWER
The issue's current proposed resolution, ordering, option set, implementation,
disposition, or conclusion.
Quarantine from Prompt 1.

REALITY CLAIM
A claimed current status/evidence statement that Prompt 2 must verify.
Do not present it as verified truth in Prompt 1 unless it is also a task-contract
premise. If it is a witness claim, present it as something to reproduce/falsify,
not as an accepted conclusion.
```

This distinction is critical.

A fact can be both a **task-contract premise** and a **reality claim**.

Example:

```text
"The P0 fix set has landed and changed the landscape."
```

For a post-P0 reconciliation issue, that may be essential to the task contract.

Prompt 1 may therefore say:

> You are responsible for the programme at the point where the P0 fix round is treated as complete and the earlier sequence is no longer trusted.

Prompt 2 must still verify whether that premise is actually true today.

Do not solve specificity by deleting the premise.

Do not solve blindness by importing the issue's proposed answer.

---

### PROBLEM KERNEL — mandatory for ISSUE_TASK

For issue/task-level work, TARGET ANCHORS alone are not enough.

Extract the **minimum identity-bearing facts that make this issue this issue**.

Complete:

> **“If I remove any one of these facts, I may be talking about a different sibling issue.”**

A good PROBLEM KERNEL usually contains 3–7 facts.

Possible kernel facts:

- the exact named method/product/domain entity central to the issue;
- the exact kind of user/job affected;
- the particular source/authority/applicability boundary at stake;
- the specific input/output or lifecycle tension;
- the stage of the programme if the issue only exists because earlier work already happened;
- the safety/trust invariant that makes this issue materially different from nearby work.

The kernel is **not** a disguised issue summary.

Do not include:

- current option lists;
- current recommendation;
- current benchmark **interpretations/recommendations**;
- benchmark numbers may appear when they are part of a selected PROBLEM WITNESS,
  but reported results must be framed as claims to reproduce/falsify rather than accepted conclusions;
- current proposed implementation;
- current PR/branch sequence;
- current bug inventory;
- current acceptance checklist;
- present evidence conclusions that Prompt 2 is supposed to verify.

### Example — issue-level engineering decision

Too generic:

```text
How should a responsible organisation decide whether to extend a governed method beyond its directly supported range?
```

Still contaminated:

```text
Should we choose among today's proposed options because the current benchmark looks favourable?
```

Correct corridor:

```text
PROBLEM KERNEL:
- a named professional method governs a real engineering job;
- the directly supported domain does not cover an important real case;
- the governing source does not supply the missing extension rule;
- professional-use authority therefore needs an explicit engineering basis;
- numerical plausibility or external agreement cannot silently create source/method authority.
```

This is specific enough to identify the issue class without revealing today's option list,
benchmark interpretation, implementation choice, sample statistics, or recommendation.

For ISSUE_TASK, construct Prompt 1 mechanically from:

```text
ISSUE TASK CONTRACT
+ PROBLEM KERNEL
+ TARGET ANCHORS
+ PROBLEM WITNESS when available
+ HUMAN OUTCOME
+ GENUINE CONSTRAINTS
- CURRENT ANSWER QUARANTINE
- WITNESS INTERPRETATION QUARANTINE
```

Do not solve contamination by anonymising the quarantined facts.
Remove them.

Complete:

```text
TARGET ANCHORS:
<stable, level-specific facts that make this unmistakably THIS target without leaking today's answer>

PROBLEM WITNESS:
PROBLEM WITNESS TYPE:
PROBLEM WITNESS SOURCE:
PROBLEM WITNESS PAYLOAD:
WITNESS CLAIM(S) TO REPRODUCE:
WHY THIS WITNESS EXPOSES THE ISSUE:
WITNESS INTERPRETATION QUARANTINE:
INDEPENDENT WORK PRODUCT:

ISSUE TASK CONTRACT:
WHY NOW:
STARTING PREMISE:
RESPONSIBLE ACTOR / JOB:
OWNED QUESTION:
NON-GOALS / OWNERSHIP BOUNDARY:
ISSUE DIFFERENTIATOR:

PROBLEM KERNEL:
<for ISSUE_TASK: 3–7 minimal identity-bearing facts that must survive blindness;
for other levels: optional if useful>

UNDERLYING HUMAN PROBLEM:
<for ISSUE_TASK: a plain-language restatement of the OWNED QUESTION that must not broaden
beyond the ISSUE TASK CONTRACT; for other levels: the problem that survives today's implementation>

HUMAN OUTCOME:
<what should become possible for the person/team when that problem is handled well>

GENUINE CONSTRAINTS:
<facts that remain true regardless of today's implementation>

EXPERTISE:
<what kind of expert should reason about the problem>

IMAGINATION OBJECT:
"Prompt 1 must independently imagine ______."
```

The IMAGINATION OBJECT should describe the **situation/outcome/problem-solving capability**, not today's artifact form, unless that artifact form is itself explicitly required by the human goal.

### Example — issue currently written as a register

Bad:

```text
UNDERLYING HUMAN PROBLEM:
keep an excellent register

IMAGINATION OBJECT:
an excellent live register
```

Better only when no stronger concrete witness exists:

```text
UNDERLYING HUMAN PROBLEM:
after substantial work has happened, determine what genuinely remains,
what requires judgement rather than more implementation,
what can proceed independently, what has become historical,
and whether the remaining path is still worth pursuing
```

Stronger when the issue contains a real discriminating case:

```text
PROBLEM WITNESS:
a concrete benchmark / calculation / dependency case that exposes why one unresolved
question changes the value or ordering of the remaining work

INDEPENDENT WORK PRODUCT:
work that case transparently, identify the actual technical/authority boundary,
then use what was learned to reason about which downstream work is rational
```

Do not prefer abstract programme judgement over a concrete witness that can make the underlying issue understandable.

Prompt 2 may later discover that a live register is a useful solution.

Prompt 1 must not assume that conclusion.

## G. Freeze Prompt 2's REALITY OBJECT

Complete:

```text
REALITY OBJECT:
"Prompt 2 must establish what is actually true today about ______."
```

This may explicitly include the current target artifact, repository, issue history, implementation, PRs, tests, examples, and in-flight work.

## H. Freeze Prompt 3's COMPARISON QUESTION — not its artifact form

Complete:

```text
COMPARISON QUESTION:
"After putting the exact Prompt-1 picture beside Prompt-2 reality,
Prompt 3 must determine ______."

HANDOVER DESTINATION:
"The next agent must understand ______."
```

Do **not** pre-commit Prompt 3 to producing “a better register,” “a revised matrix,” “an updated roadmap,” or any other improved version of the current artifact.

Prompt 3 must remain free to conclude that the current artifact should be:

- preserved;
- updated;
- narrowed;
- split;
- replaced;
- closed;
- moved back to owning issues;
- deferred;
- or left unchanged.

The response form should emerge **after comparison**, not be decided before it.

## I. Visible PREFLIGHT RECORD

The visible record must contain:

```text
LOT:
USER-REQUESTED LEVEL:
USER-REQUESTED TARGET:
LEVEL INTERPRETATION:

TARGET TITLE / SURFACE:
TARGET LINK:
PARENT REPOSITORY / SYSTEM:
REPOSITORY / SYSTEM LINK:

REQUEST MODE:
COMPLEX MODE: ON | OFF

CURRENT REALITY — QUARANTINED FROM PROMPT 1
CURRENT ARTIFACT FORM:
CURRENT STATED ANSWER / IMPLEMENTATION:
CURRENT-STATE FACTS:
CURRENT ANSWER QUARANTINE:

BLIND REFERENCE — THE ONLY SIDE ALLOWED TO SHAPE PROMPT 1
TARGET ANCHORS:

PROBLEM WITNESS
PROBLEM WITNESS TYPE:
PROBLEM WITNESS SOURCE:
PROBLEM WITNESS PAYLOAD:
WITNESS CLAIM(S) TO REPRODUCE:
WHY THIS WITNESS EXPOSES THE ISSUE:
WITNESS INTERPRETATION QUARANTINE:
INDEPENDENT WORK PRODUCT:

ISSUE TASK CONTRACT
WHY NOW:
STARTING PREMISE:
RESPONSIBLE ACTOR / JOB:
OWNED QUESTION:
NON-GOALS / OWNERSHIP BOUNDARY:
ISSUE DIFFERENTIATOR:

PROBLEM KERNEL:
UNDERLYING HUMAN PROBLEM:
HUMAN OUTCOME:
GENUINE CONSTRAINTS:
EXPERTISE:
IMAGINATION OBJECT:

PROMPT 2
REALITY OBJECT:

PROMPT 3
COMPARISON QUESTION:
HANDOVER DESTINATION:

ARTIFACT-ERASURE GATE:
PASS — <one short reason>

CURRENT-VOCABULARY GATE:
PASS — <one short reason>

PROMPT-1 OBJECT GATE:
PASS — <one short reason>

HUMAN-IMMERSION GATE:
PASS — <one short reason>

COMPLEX Q1–Q5 COVERAGE:
PASS — <one short reason, or N/A when COMPLEX MODE = OFF>

MODE-ISOLATION GATE:
PASS — Q1–Q5 stay inside Prompt 1; no extra protocol/gate/stage is added

SPECIFICITY-FLOOR GATE:
PASS — <one short reason>

TASK-CONTRACT FIDELITY GATE:
PASS — <one short reason, or N/A outside ISSUE_TASK>

NEIGHBOUR-SEPARATION GATE:
PASS — <one short reason, or N/A outside ISSUE_TASK>

PROBLEM-WITNESS SELECTION GATE:
PASS — <one short reason, or N/A outside ISSUE_TASK>

WITNESS-INDEPENDENCE GATE:
PASS — <one short reason, or N/A outside ISSUE_TASK>

KERNEL-COVERAGE GATE:
PASS — <one short reason, or N/A outside ISSUE_TASK>

SAME-ISSUE IDENTITY GATE:
PASS — <one short reason, or N/A outside ISSUE_TASK>

ANSWER-EXCLUSION GATE:
PASS — <one short reason, or N/A outside ISSUE_TASK>

LOT/LEVEL BOUNDARY GATE:
PASS — <one short reason>

PROMPT-3 FREEDOM GATE:
PASS — <one short reason>
```

Do not draft Prompt 1 until these fields and gates are resolved.

---

# HARD GATE -2 — SCHEMA FRESHNESS GATE

Before any target reasoning, verify the SCHEMA EXECUTION BASIS.

If the canonical repository/URL is the source:

```text
SCHEMA FETCH STATUS must equal LIVE_THIS_RUN
SCHEMA CONTENT SHA must be populated from that fetch
SCHEMA COMPATIBILITY must equal PASS
```

If this cannot be proven, stop.

Do not generate prompts from remembered schema rules.

---

# HARD GATE -1 — LEGACY-SIGNATURE REJECTION GATE

Before emitting the final artifact, reject any output that:

- makes the current artifact form the Prompt-1 imagination object merely because it exists today;
- narrates repository-blindness or three-pass mechanics inside Prompt 1;
- inserts an extra certification/admission/question stage between the three prompts;
- exposes internal machine/taxonomy fields as visible Q1–Q5 language;
- predetermines in Prompt 3 that the current artifact must survive.

The executable validator owns the exact legacy signature list. Do not reproduce those signatures inside this schema.

---

# HARD GATE 0 — LOT / LEVEL BOUNDARY GATE

Before writing any prompt, compare the resolved target with the user's lot contract.

Ask:

> **Am I still analysing the exact level the user asked for?**

If the user asked for TAB_SURFACE and the target is now a GitHub issue, decision, roadmap, or repository, fail.

If the user asked for ISSUE_TASK and the target has broadened to the whole tab/product/repository, fail.

Do not “improve” the user's decomposition by substituting a supposedly more important target.

---

# HARD GATE 0.5 — SPECIFICITY-FLOOR GATE

Prompt 1 must be independent, but it must not become generic consultancy prose.

Ask all of these:

> **Could this Prompt 1 be pasted unchanged into ten unrelated projects in the same industry?**

> **Could a competent general manager answer most of it without knowing this target domain?**

> **Would the user recognise the exact requested level and job-to-be-done from Prompt 1 even though today's implementation is hidden?**

If the first two are yes, or the third is no, Prompt 1 is too generic.

A good Prompt 1 normally contains:

- a concrete person;
- a concrete job or decision;
- a concrete real-world scenario;
- target-specific domain objects/inputs/results;
- genuine target constraints;
- target-specific failure/trust questions.

It should be **specific to the target, independent of today's answer**.

For ISSUE_TASK, genericness is not cured by adding more abstract questions. It is cured by restoring the PROBLEM KERNEL.

---

# HARD GATE 0.75 — SAME-ISSUE IDENTITY GATE

For ISSUE_TASK only, remove the issue number/title from Prompt 1 and ask:

> **Could a domain-aware person familiar with the programme distinguish this issue from its sibling issues?**

They do not need to guess the exact GitHub number.

But they should be able to say what *particular unresolved problem* this prompt is about.

If Prompt 1 collapses to something like:

- “how should engineering decisions be made?”;
- “how should a register work?”;
- “how should qualification be governed?”;
- “how should a learner system map knowledge?”;

without the identity-bearing tension of the issue, fail.

The fix is **not** to restore today's solution.

The fix is to restore the PROBLEM KERNEL.

---

# HARD GATE 0.8 — TASK-CONTRACT FIDELITY GATE

For ISSUE_TASK, inspect every field of the ISSUE TASK CONTRACT.

Ask:

> **Is Prompt 1 materially situated in this exact assignment, or has it abstracted upward into a generic class of work?**

Prompt 1 must preserve:

- WHY NOW;
- the load-bearing STARTING PREMISE;
- RESPONSIBLE ACTOR / JOB;
- OWNED QUESTION;
- relevant NON-GOALS / OWNERSHIP BOUNDARY.

If these disappear, fail.

Do not replace them with generic words such as "complex programme", "responsible owner", or "remaining work" when the issue gives a more specific assignment.

---

# HARD GATE 0.82 — NEIGHBOUR-SEPARATION GATE

For ISSUE_TASK, compare Prompt 1 with the parent and nearest sibling issues.

Ask:

> **Could this Prompt 1 be used unchanged for the parent issue or a nearby sibling?**

If yes, it is too broad.

Use ISSUE DIFFERENTIATOR to restore the exact edge.

For example, an issue-level prompt must remain distinguishable from its parent audit, a sibling authority decision, and downstream release-execution work.

---

# HARD GATE 0.83 — PROBLEM-WITNESS SELECTION GATE

For ISSUE_TASK, ask:

> **Does the target contain a concrete benchmark, case, trace, example, dataset, drawing, observed output, user journey, dependency case, or other witness that materially exposes the owned question?**

If yes:

- select it explicitly;
- retain enough real payload to let the future agent work it;
- do not replace real values with invented plausible values;
- require a concrete INDEPENDENT WORK PRODUCT from it.

If a strong witness exists and Prompt 1 ignores it in favour of abstract consultancy questions, fail.

If no usable witness exists, record:

```text
PROBLEM WITNESS TYPE: NONE
```

and proceed from the task contract/kernel.

---

# HARD GATE 0.84 — WITNESS-INDEPENDENCE GATE

If Prompt 1 uses a witness, separate:

```text
raw/input/source facts
reported outputs to reproduce
today's interpretation/recommendation
```

Prompt 1 may provide the first two.

The second must be framed as:

> reproduce, verify, explain, or falsify this reported result

—not:

> accept this result and reason from its conclusion.

The third remains quarantined.

Fail if the witness merely launders today's recommendation into Prompt 1.

---

# HARD GATE 0.85 — KERNEL-COVERAGE GATE

For ISSUE_TASK, inspect every PROBLEM KERNEL fact.

Ask:

> **Is this fact materially present in Prompt 1, either explicitly or naturally in the scenario?**

Every load-bearing kernel fact must survive.

If any kernel fact disappears, Prompt 1 is drifting toward generic class-level advice.

Do not repair missing identity by adding today's answer.
Restore only the missing kernel fact.

---

# HARD GATE 0.9 — ANSWER-EXCLUSION GATE

For ISSUE_TASK, inspect every CURRENT ANSWER QUARANTINE item.

Ask:

> **Can a reader learn or reconstruct this quarantined fact from Prompt 1?**

If yes, Prompt 1 is contaminated.

Examples of quarantined leakage:

```text
today's option set
today's chosen numerical rule
current benchmark percentage
current study/sample conclusion
current exact PR order
current blocker/decision inventory
current matrix/rung names
current proposed file/schema changes
```

Prompt 1 should expose the **question worth answering**, not today's repository answer.

Do not merely replace leaked proper nouns with generic nouns.
Remove the answer-side fact.

---

# HARD GATE 0.95 — ISSUE GOLDILOCKS CORRIDOR

An issue-level Prompt 1 passes only if **both** are true:

```text
KERNEL-COMPLETE:
The load-bearing PROBLEM KERNEL survives.

RECOGNISABLE:
The underlying issue is identifiable from that kernel.

ANSWER-EXCLUDED:
CURRENT ANSWER QUARANTINE does not leak.

NOT PRE-SOLVED:
The current answer/options/evidence interpretation cannot be reconstructed.
```

Think of the allowed information band as:

```text
too generic
    ↓
[ task contract + problem kernel + concrete witness + domain truth + human outcome ]
    ↑
too contaminated
```

The generator's job is to stay inside that band.

---

# HARD GATE 0.965 — HUMAN-Q-LABEL GATE

When COMPLEX MODE is ON and visible Q1–Q5 headings are used, inspect each heading and the text immediately beneath it.

Fail if the visible surface contains internal taxonomy labels or protocol metadata.

Examples that fail:

```text
Q1 — PRODUCTION_PATH
Q2 — ENGINEERING_PROBLEM
Q3 — BOUNDARIES_INVARIANTS
Q4 — VERIFICATION
Q5 — FIRST_SAFE_SLICE

required_output_keys:
reconstruction_mode:
payload.source:
evidence_required:
oracle_refs:
step_refs:
```

Passing labels must be short, natural, target-specific practitioner language.

Examples:

```text
Q1 — Work out what is happening in this real case
Q2 — Do the calculation or reconstruction yourself
Q3 — Change the case and see what breaks
Q4 — Check your result against the independent comparator
Q5 — Given what you learned, what is worth doing next?
```

If the user did not ask to see Q1–Q5 labels, prefer natural prose and do not show labels at all.

---

# HARD GATE 0.97 — HUMAN-IMMERSION GATE

Read Prompt 1 as though you were the future agent receiving it with no knowledge of this schema.

Fail if Prompt 1 contains process/meta language about:

- pass sequencing;
- later comparison mechanics;
- repository or issue-access restrictions;
- schema/preflight/gate/quarantine terminology;
- preserving an answer for a future stage.

Also fail if the opening spends more time explaining how to think than describing the person, job, domain situation, real object/case, and stakes.

A passing Prompt 1 should begin inside the human/domain problem, not outside it.

The blindness mechanism must be invisible to the future agent.

---

# HARD GATE 1 — ARTIFACT-ERASURE GATE

Imagine that the current issue, register, roadmap, matrix, architecture, checklist, implementation and proposed solution never existed.

Keep only:

- the human problem;
- desired outcome;
- genuine constraints;
- domain;
- scale.

Ask:

> **Would Prompt 1 still make essentially the same sense?**

If no, Prompt 1 has inherited the current answer.

Reject it and rewrite.

Important nuance:

- For a product target, the product category may itself be part of the human request. “Browser PDF editor” can survive erasure of the **current implementation**.
- For ISSUE_TASK, erase the **artifact form and current answer**, but preserve the ISSUE TASK CONTRACT. Imagine the Markdown issue/register disappeared while the assignment it represents remained.
- For an issue currently expressed as a “register,” “matrix,” or “roadmap,” that artifact form usually should **not** survive unless the task contract explicitly requires that form.

---

# HARD GATE 2 — CURRENT-VOCABULARY LEAKAGE GATE

Scan Prompt 1 noun-by-noun and fact-by-fact.

For every important term, ask:

```text
Did this come from:

A. the blind human problem / genuine domain constraint

or

B. the current target / repository / issue / implementation / proposed solution?
```

If B, remove it unless it is explicitly classified as either:

- ISSUE TASK CONTRACT / PROBLEM KERNEL material for ISSUE_TASK; or
- a genuine independent domain/human constraint.

For issue-level work, deleting all target-derived facts is a failure: it erases the assignment itself.

Hiding the issue number while paraphrasing its current state is **not** blindness.

Likewise, replacing target-specific proper nouns with generic nouns is not enough.

If the narrative structure and current evidence story are preserved while only names are anonymised, the answer has merely been **laundered into generic language**.

For ISSUE_TASK, preserve the PROBLEM KERNEL directly and remove the current answer instead of anonymising both.

A Prompt 1 that says:

```text
recently landed work
in-flight work
infrastructure blockers
owner-reserved decisions
one living register
stale written plans
```

because those facts came from today's issue is contaminated even if no repository name appears.

---

# HARD GATE 3 — PROMPT-1 OBJECT GATE

Finish:

> **“If Prompt 1 were answered perfectly, the answer would give us an independent picture of ______.”**

The blank must match the frozen IMAGINATION OBJECT and help solve the UNDERLYING HUMAN PROBLEM.

If it instead describes:

- a larger neighbouring product;
- a current artifact form;
- a specific implementation proposal;
- or a smaller symptom;

reject Prompt 1.

---

# HARD GATE 4 — PROMPT-3 FREEDOM GATE

Read Prompt 3 before output.

Ask:

> **Can the agent still conclude, based on evidence, that today's artifact should be preserved, changed, narrowed, split, replaced, closed, deferred, moved elsewhere, or left alone?**

Fail if Prompt 3 mandates a better version of today's artifact before comparison is complete.

Prompt 3 may require a decision and reasoning, but must not pre-decide the survival of the current solution form.

---

# STEP 1 — BUILD PROMPT 1 ONLY FROM THE BLIND REFERENCE

This is the most important construction rule.

Allowed inputs to Prompt 1:

```text
USER-REQUESTED LEVEL
TARGET TITLE / SURFACE when it is itself part of the requested human problem
TARGET ANCHORS
ISSUE TASK CONTRACT for ISSUE_TASK
PROBLEM KERNEL
PROBLEM WITNESS for ISSUE_TASK when one exists
INDEPENDENT WORK PRODUCT for ISSUE_TASK when a witness is selected
UNDERLYING HUMAN PROBLEM
HUMAN OUTCOME
GENUINE CONSTRAINTS
EXPERTISE
IMAGINATION OBJECT
domain facts that are genuinely independent of the current implementation
```

Forbidden inputs to Prompt 1 unless independently justified as genuine constraints:

```text
CURRENT ARTIFACT FORM
CURRENT STATED ANSWER / IMPLEMENTATION
CURRENT-STATE FACTS
CURRENT ANSWER QUARANTINE
repository structure
existing abstraction names
current schemas
current architecture
issue checklist
current roadmap
file names
PR numbers
present blockers
current decision list
current solution vocabulary
```

The purpose is to let the future agent **have an opinion before meeting today's answer**.

For task/issue targets, recover the human intention underneath the work item.

Examples:

```text
"Add three matrix rungs and capability mappings"
→ not "imagine an excellent matrix"
→ imagine how a learner stuck on a real question should be connected
   to reusable knowledge, prerequisites and teaching

"Maintain this open-items register"
→ not "imagine an excellent register"
→ imagine how a competent successor should determine what genuinely remains,
   what is decision versus executable work, and what should happen next

"Fix 900-page scrolling"
→ not "imagine a 900-page mode"
→ imagine what working with a very large document should feel like and
   what must remain responsive
```

The generator itself enforces blindness by controlling what information is allowed into Prompt 1.

**Do not make Prompt 1 talk about that enforcement.**

# PROMPT 1 — IMAGINE

Generate a self-contained first-principles prompt from the **BLIND REFERENCE only**.

It should begin from the strongest available concrete footing:

- for ISSUE_TASK with a usable PROBLEM WITNESS: the real case/object and the practitioner who must work it;
- otherwise: the underlying human problem;
- the intended human outcome;
- genuine constraints;
- relevant domain realities;
- the required expertise.

When a witness exists, prefer verbs such as:

```text
calculate
derive
reconstruct
trace
compare
reproduce
falsify
explain
work the case
```

over:

```text
consider
discuss
imagine principles
think about
```

Prompt 1 should make the future agent **do the substantive work** that reveals the issue.

Prompt 1 must **not mention** repositories, issue trackers, later passes, blind/reference mechanics, schema rules, or instructions about what the agent is forbidden to inspect.

Those are generator-side controls, not part of the human prompt.

Use human language and mental simulation.

### Blind does not mean generic

Prompt 1 should be concrete enough that the user can immediately tell whether it is:

- issue-level;
- tab/surface-level;
- product-level;
- or repository/system-level.

For TAB_SURFACE, normally walk a real user through the surface from arrival/input to result/refusal/review.

For ISSUE_TASK, stay on the specific underlying issue problem and its lifecycle stage; do not drift to the whole tab.

Use TARGET ANCHORS aggressively enough to make the scenario vivid, while keeping current-answer facts quarantined.

### Human-immersion rule

Prompt 1 should feel as though a strong practitioner has been dropped directly into the real situation.

Prefer this shape:

```text
who is the person?
→ what are they trying to accomplish?
→ what real thing is in front of them?
→ what makes this case difficult or consequential?
→ what would they need to understand, calculate, decide, trust, notice, or prove?
→ what would good handling make possible?
```

The reader should forget that a three-pass method exists.

Do not narrate:

- pass sequencing;
- future comparison mechanics;
- repository/issue-access restrictions;
- schema/preflight/gate terminology;
- instructions about preserving an answer for a later stage.

Do not begin with procedural advice about how to think.

Cause first-principles reasoning through the real situation, concrete object and questions.

### Prompt 1 must end in a human picture of success

At the end, ask naturally for something equivalent to:

> **“If this were handled really well, what would become possible for the person doing the work?”**

Then ask what would make that outcome trustworthy, durable, or worth defending.

Do not mention that the answer will become a reference for another pass. The generator retains that relationship internally.

### Complex-mode addition

If COMPLEX MODE is ON, Prompt 1 must naturally cover all five Q1–Q5 reasoning lenses from Appendix H.

Do **not** write robotic headings such as:

```text
Q1:
Q2:
Q3:
Q4:
Q5:
```

unless the user explicitly asks to see those labels.

Instead weave the five lenses into the human scenario so they feel like the natural questions a strong practitioner would ask.

### Product-level note

At product level, the product category itself can be part of the human goal. Prompt 1 may therefore imagine the desired product experience broadly.

What remains forbidden is leaking the **current product implementation**.

### Repository/system-level note

Imagine the desired human/system outcome independent of today's repository architecture, roadmap, phase names and implementation vocabulary.

### Tab/surface-level note

Imagine the real user using that named surface end to end.

Prompt 1 should normally cover:

```text
real starting situation
→ inputs / choices
→ interpretation / calculation / transformation
→ result or refusal
→ understanding of applicability
→ review / evidence / next action
```

Use the tab's genuine domain purpose and user job.

Do not leak today's UI arrangement, bug list, implementation limits or current backlog.

### Task/issue-level note

Issue-level Prompt 1 should be **closer to the issue than to the parent programme**.

Do not start by abstracting upward to a generic human problem.

Start with the ISSUE TASK CONTRACT.

Construct Prompt 1 in this order:

```text
1. Put the RESPONSIBLE ACTOR into the exact WHY-NOW situation.
2. State the STARTING PREMISE as a scenario, not as verified reality.
3. Make the OWNED QUESTION unmistakable.
4. State the NON-GOALS / OWNERSHIP BOUNDARY where it matters.
5. Carry the PROBLEM KERNEL concretely.
6. If a PROBLEM WITNESS exists, give the future agent the real case/payload and require
   the INDEPENDENT WORK PRODUCT before asking for broader judgement.
7. Make reported witness outputs claims to reproduce/falsify, not accepted conclusions.
8. Ask first-principles questions that emerge from what the witness teaches.
9. Return explicitly to the OWNED QUESTION.
10. End with the human/domain outcome.
```

The actor is the person responsible for **this issue's outcome**.

Do not automatically substitute the product end-user.

For a coordination/closure issue, the right actor may be the engineering owner or successor deciding what truly remains.

For a user-facing defect issue, the end-user may be appropriate.

Do not begin by asking for the current artifact:

```text
bad:  "Imagine an excellent decision package."
bad:  "Imagine an excellent register."
bad:  "Imagine an excellent matrix."
```

Instead ask about the actual unresolved problem:

```text
better:
"You are responsible for a professional engineering capability whose governing method
directly supports some cases but not the real case now in front of you. The source does
not provide the missing extension rule. Work the case far enough to show exactly where
the governed method ends, what additional assumption would be needed to continue, and
what evidence would be required before an organisation could responsibly rely on that extension."
```

That is issue-specific in structure without revealing today's options or evidence conclusion.

Do **not** assume the current issue's proposed artifact or work breakdown is the correct instrument.

Run the TASK-CONTRACT FIDELITY, NEIGHBOUR-SEPARATION,
PROBLEM-WITNESS SELECTION, WITNESS-INDEPENDENCE, KERNEL-COVERAGE,
SAME-ISSUE IDENTITY, ANSWER-EXCLUSION, ARTIFACT-ERASURE,
CURRENT-VOCABULARY and PROMPT-1 OBJECT gates before accepting Prompt 1.

---

# STEP 2 — PROMPT 2 MUST RECONSTRUCT REALITY, NOT REDESIGN IT

Prompt 2 now deliberately brings back everything quarantined from Prompt 1: the exact target artifact, its current answer, implementation vocabulary, history, repository, tests, PRs and live state.

Its subject is the frozen **REALITY OBJECT**.

Tell the future agent to inspect the live implementation and understand the reality relevant to that object before proposing changes. Do not automatically broaden Prompt 2 into a full repository audit if the target only needs a bounded register, decision, investigation, or implementation reality.

Depending on the target, inspect relevant:

- repository code and data;
- README and architecture documents;
- tests;
- issue history;
- PR history;
- current open PRs;
- recent merged work;
- current roadmap;
- real examples, real failures, real questions, real documents, or real usage evidence.

Tell it not to rely only on documentation or issue prose when actual code or data can answer the question.

Tell it to follow **real journeys appropriate to the target's purpose**, not merely list folders.

Examples:

```text
user intent
→ action
→ system decisions
→ result
```

```text
real question/problem
→ interpretation
→ underlying need
→ route through the system
→ outcome
```

```text
open document
→ load
→ interact
→ modify
→ save
```

For coordination/register work, Prompt 2 should trace claims such as:

```text
register statement
→ live issue / PR / branch / test / workflow / decision
→ still true, stale, superseded, blocked, or unresolved
```

For decision work, trace:

```text
decision to be made
→ alternatives
→ evidence
→ uncertainty
→ consequence of each choice
→ authority boundary
```

For investigation work, trace:

```text
claim or symptom
→ evidence source
→ reproduction
→ competing explanations
→ conclusion and remaining uncertainty
```

For handover work, trace:

```text
what successor is told
→ source of truth
→ current validity
→ first safe action
→ stale condition
```

Prompt 2 should encourage the agent to discover:

- what is already genuinely strong;
- what is incomplete;
- what exists only in documentation;
- what is intentionally absent;
- what has become obsolete;
- what has been superseded;
- what real examples have exposed;
- what current work is already trying to solve.

### Present baseline and near-future baseline

When relevant PRs or in-flight work exist, Prompt 2 must distinguish:

```text
CURRENT BASELINE
what is actually true now

NEAR-FUTURE BASELINE
what would be true if the clearly relevant current work lands
```

This prevents the future agent from proposing work another agent is already completing.

Do not let Prompt 2 become the redesign step.

Its closing job is to explain, in plain language:

> “This is what the system has actually become.”

---

# STEP 3 — PROMPT 3 MUST REUSE THE EXACT PASS-1 IDEAL

Prompt 3 must also be **self-identifying**.

At its top, include the concrete target references again:

```text
TARGET:
<issue/task/product/repository name>

TARGET LINK:
<canonical issue/task/PR/document URL when available>

REPOSITORY / SYSTEM:
<repository or parent system name when applicable>

REPOSITORY LINK:
<repository URL when available>
```

Do not assume the agent running Prompt 3 still has access to the original user message.

If the target is an issue inside a repository, Prompt 3 should normally contain **both**:

- the issue URL;
- the repository URL.

If the target is the repository itself, one repository URL is enough.

If the target has no URL, use the clearest stable identifier available.



Prompt 3 must explicitly tell the future agent to return to the **actual answer it produced for Prompt 1**.

Do not let it quietly rewrite the ideal after seeing the repository.

Tell it:

> Take the independent picture you produced in Prompt 1.

> Put it beside the reality you discovered in Prompt 2.

> Where evidence from reality genuinely changed your mind, explain exactly why.

> Otherwise keep the original independent baseline.

This is the anti-goalpost-moving rule.

If the three prompts are likely to be run in separate conversations, Prompt 3 should instruct the user to paste or attach the outputs of Prompt 1 and Prompt 2 before running it. If they are expected to run in one continuous conversation, simply tell the agent to use its prior two outputs.

The Prompt-1 and Prompt-2 outputs are supporting context; they do **not** replace the target identity and links.

---

# PROMPT 3 — REVALIDATE AND MOVE FORWARD

Prompt 3 must return to the **actual Prompt-1 answer** and place it beside Prompt-2 reality.

It is constrained by the frozen **COMPARISON QUESTION**, not by a preselected artifact form.

Tell the future agent explicitly:

> Take the independent picture you produced before meeting the current answer.

> Put it beside what you discovered about reality.

> Where evidence genuinely changed your mind, say exactly why.

> Otherwise keep the independent baseline.

> Do not assume the current issue, register, matrix, roadmap, architecture, checklist or task breakdown deserves to survive merely because it already exists.

Prompt 3 should reason in this order.

## A. Return to the exact Prompt-1 picture

What did we believe good handling of the underlying human problem looked like **before** seeing today's answer?

Do not rewrite that picture to resemble the repository.

## B. What should be preserved?

Identify what reality already does well.

Preserve sound mechanisms, evidence and decisions even if they use different vocabulary.

## C. What has become historical?

Ask:

> What problem used to exist but no longer does?

> Which issue text, roadmap item, status statement or assumption describes an earlier project state?

> What has later work already made obsolete?

## D. First determine today's remaining problem; then decide the artifact's disposition

Do not start by assuming the artifact needs reconciliation.

First ask:

> **Given the independent Prompt-1 picture and verified reality, what is the actual remaining problem today?**

Only after stating that problem independently, ask:

> **Does the current artifact still deserve to exist in its present form as the instrument for that problem?**

This is mandatory for issues, registers, matrices, roadmaps, checklists, architecture umbrellas, handovers and plans.

Ask:

> Is today's artifact actually the right instrument for the underlying human problem now?

Possible conclusions include:

```text
yes — preserve it
yes — but narrow/update it
split it
replace it
move remaining work back to owning issues
close it because its job is done
defer it
leave it unchanged
```

Do not prejudge the answer.

## E. What is the real problem now?

Given the independent picture and verified reality:

> What meaningful distance genuinely remains today?

Rewrite the problem in today's language.

For task/issue work, prefer:

> **“Given the current repository, the meaningful remaining work is…”**

when implementation work genuinely remains.

If the correct result is instead “decision needed,” “close this artifact,” “no change,” or “collect evidence first,” say that instead.

## F. What deeper idea is the example exposing?

Do not confuse the thing that exposed a weakness with the reusable problem underneath it.

Examples:

```text
river-crossing question
≠ automatically a river capability

900-page PDF freeze
≠ automatically a 900-page mode

one stale register entry
≠ automatically a need for a better register

failed test
≠ automatically an architecture problem
```

## G. What is the smallest justified response?

Valid responses include:

- add;
- fix;
- extend;
- simplify;
- refactor;
- remove;
- reconcile;
- gather evidence;
- present a decision;
- narrow or split the current artifact;
- close it;
- move work elsewhere;
- defer;
- preserve unchanged;
- or make no change yet.

Do not manufacture work because a plan was requested.

## H. How will reality test the conclusion?

Return to real examples, journeys, questions, models, failures, benchmarks or observations.

Ask:

> Does the conclusion survive beyond the example that exposed the issue?

> What evidence would show that the chosen response helped?

> What evidence would prove the conclusion wrong?

---

# HOW PROMPT 3 SHOULD END BY REQUEST MODE

These are **decision duties**, not mandatory artifact forms.

## CONCEIVE

Determine what should be built or become possible from first principles.

## REVIEW

Determine:

- what should be preserved;
- what has become historical;
- the meaningful remaining distance;
- what “complete enough now” should mean;
- the smallest sensible phased path;
- what should deliberately wait or never be built.

## CHANGE

Determine whether meaningful implementation/change work still remains.

If yes, rewrite the task in today's terms and identify the smallest durable change.

If no, say whether the issue should close, defer, become a decision, or move elsewhere.

## INVESTIGATE

Produce the best-supported conclusion, uncertainty and evidence that would overturn it.

Do not automatically convert a finding into implementation work.

## DECIDE

State the exact decision, viable options, evidence, consequences, reversibility, uncertainty, authority boundary and what each option gates.

Do not make an owner-reserved choice unless authorized.

## COORDINATE

Determine the truthful current state, real dependencies, decisions versus executable work, and the safe frontier.

Then decide whether the current coordination artifact should be preserved, reconciled, narrowed, split, replaced or closed.

Do not assume “COORDINATE” means force a better version of the current artifact.

## HANDOVER

Transmit enough understanding that a successor can continue with correct judgement.

The handover must preserve reasoning, not merely operational state.

Run the PROMPT-3 FREEDOM GATE before accepting Prompt 3.

---

# RESTRAINT IS A FIRST-CLASS REQUIREMENT

All three generated prompts should encourage restraint.

The future agent should repeatedly ask:

> What are we tempted to build that we should not build?

> Is this genuinely required by the human outcome?

> Are we filling an honest gap merely because empty space looks uncomfortable?

> Are we creating a special case when a reusable idea already exists?

> Are we mistaking more architecture for more progress?

> Are we mistaking passing tests for proof that the human outcome works?

> Are we carrying an old plan forward only because nobody explicitly retired it?

A mature result may conclude:

> Leave this alone.

> Wait for real evidence.

> This is already good enough for this stage.

> The architecture is sufficient; author content instead.

> The content is sufficient; test with real people instead.

---

# HUMAN-LANGUAGE RULE

Write the generated prompts so that they engage judgment and imagination.

Prefer:

> Imagine the learner.

> Imagine the person opening the document.

> Imagine the developer returning six months later.

> Follow what really happens.

> Ask what the person is trying to accomplish.

> Ask what has already been learned by the project.

> Find the reusable idea underneath the example.

Avoid turning the prompts into machine-level jargon.

Do not overuse terms such as:

- execution graph;
- reconciliation engine;
- ontology completion;
- state machine;
- delta processor;
- classification pipeline.

Technical language is fine where the domain genuinely requires it, but the reasoning prompts themselves should remain human-readable.

---

# HANDOVER REQUIREMENT — HAND OVER THE REASONING, NOT THE ACTIVITY LOG

Prompt 3 must end with a **reasoning handover**.

The original purpose of this method is continuity of judgement. The next agent should be able to understand **why this is the right next move**, not merely recover file names, commits, branches, or a task list.

Use this shape, adapted naturally to the target:

```text
DESTINATION
What were we ultimately trying to make possible?
Use the human/reference picture, not the implementation vocabulary.

REALITY
What did we learn the current system/task actually is today?
What surprised us or changed the meaning of the original plan?

REAL GAP
After comparing destination and reality, what meaningful distance genuinely remains?
State the gap in today's language.

CHOSEN MOVE
What is the smallest worthwhile response now, and why this rather than something larger?

DELIBERATELY NOT DONE
What tempting work are we intentionally leaving alone, and why?
Include work already solved, unsupported by evidence, outside authority, or unnecessary.

REAL EVIDENCE / EXAMPLE
What concrete example, user journey, question, model, failure, benchmark, or observation
most strongly supports the conclusion?

UNRESOLVED
What remains uncertain, owner-gated, evidence-limited, or intentionally deferred?

WHERE THE NEXT AGENT SHOULD START
What should the next agent look at first, and what understanding should they carry with them?

WHAT SHOULD CHANGE OUR MIND
What future evidence or discovery would justify taking a different direction?
```

For repositories and engineering tasks, operational details such as branch, commit, PR topology, or exact next command may be added **after** this reasoning relay when genuinely useful.

They must not replace it.

The governing principle is:

> **Do not hand over what you did. Hand over what you understood.**

A good handover should let a fresh agent reconstruct the journey:

```text
destination
→ current reality
→ meaningful remaining distance
→ smallest justified move
→ evidence
→ uncertainty
→ next judgement
```

This is the same reasoning continuity used by the successful product-level and task-level applications of the method.

---

# STRICT OUTPUT CONTRACT FOR THE GENERATOR

The complete generator output begins with the mandatory **SCHEMA EXECUTION HANDSHAKE**, followed by one shared **SCHEMA BASIS** section.

Then, for **each requested lot**, output four visible sections:

1. one **PREFLIGHT RECORD**;
2. exactly three **copy-pasteable prompt blocks**.

The preflight is metadata, **not a fourth prompt**.

If the user requested two lots, output two lot sections. Do not merge them and do not invent a different second target.

Output this structure and nothing else:

````markdown
# SCHEMA EXECUTION HANDSHAKE

```text
PROTOCOL REVISION:
TPG-3P-2026-09-19-R2

GENERATOR MODE:
THREE_PASS_ONLY

SCHEMA FETCH STATUS:
LIVE_THIS_RUN

SCHEMA CONTENT SHA:
<actual live fetched SHA>

HANDSHAKE STATUS:
PASS
```

# SCHEMA BASIS

```text
PROTOCOL REVISION:
TPG-3P-2026-09-19-R2

GENERATOR MODE:
THREE_PASS_ONLY

SCHEMA SOURCE:
SCHEMA REF:
SCHEMA CONTENT SHA:
SCHEMA FETCH STATUS:
SCHEMA COMPATIBILITY:
LEGACY-SIGNATURE GATE:
PASS — no retired active construction signature appears in this deliverable
```

# LOT <n> — <USER-REQUESTED LEVEL>: <TARGET>

## PREFLIGHT RECORD

```text
LOT:
USER-REQUESTED LEVEL:
USER-REQUESTED TARGET:
LEVEL INTERPRETATION:

TARGET TITLE / SURFACE:
TARGET LINK:
PARENT REPOSITORY / SYSTEM:
REPOSITORY / SYSTEM LINK:

REQUEST MODE:
COMPLEX MODE: ON | OFF

CURRENT REALITY — QUARANTINED FROM PROMPT 1
CURRENT ARTIFACT FORM:
CURRENT STATED ANSWER / IMPLEMENTATION:
CURRENT-STATE FACTS:
CURRENT ANSWER QUARANTINE:

BLIND REFERENCE — THE ONLY SIDE ALLOWED TO SHAPE PROMPT 1
TARGET ANCHORS:

PROBLEM WITNESS
PROBLEM WITNESS TYPE:
PROBLEM WITNESS SOURCE:
PROBLEM WITNESS PAYLOAD:
WITNESS CLAIM(S) TO REPRODUCE:
WHY THIS WITNESS EXPOSES THE ISSUE:
WITNESS INTERPRETATION QUARANTINE:
INDEPENDENT WORK PRODUCT:

ISSUE TASK CONTRACT
WHY NOW:
STARTING PREMISE:
RESPONSIBLE ACTOR / JOB:
OWNED QUESTION:
NON-GOALS / OWNERSHIP BOUNDARY:
ISSUE DIFFERENTIATOR:

PROBLEM KERNEL:
UNDERLYING HUMAN PROBLEM:
HUMAN OUTCOME:
GENUINE CONSTRAINTS:
EXPERTISE:
IMAGINATION OBJECT:

PROMPT 2
REALITY OBJECT:

PROMPT 3
COMPARISON QUESTION:
HANDOVER DESTINATION:

LOT/LEVEL BOUNDARY GATE:
PASS — <one short reason>

COMPLEX Q1–Q5 COVERAGE:
PASS — <one short reason, or N/A when COMPLEX MODE = OFF>

MODE-ISOLATION GATE:
PASS — Q1–Q5 stay inside Prompt 1; no extra protocol/gate/stage is added

SPECIFICITY-FLOOR GATE:
PASS — <one short reason>

TASK-CONTRACT FIDELITY GATE:
PASS — <one short reason, or N/A outside ISSUE_TASK>

NEIGHBOUR-SEPARATION GATE:
PASS — <one short reason, or N/A outside ISSUE_TASK>

PROBLEM-WITNESS SELECTION GATE:
PASS — <one short reason, or N/A outside ISSUE_TASK>

WITNESS-INDEPENDENCE GATE:
PASS — <one short reason, or N/A outside ISSUE_TASK>

KERNEL-COVERAGE GATE:
PASS — <one short reason, or N/A outside ISSUE_TASK>

SAME-ISSUE IDENTITY GATE:
PASS — <one short reason, or N/A outside ISSUE_TASK>

ANSWER-EXCLUSION GATE:
PASS — <one short reason, or N/A outside ISSUE_TASK>

ARTIFACT-ERASURE GATE:
PASS — <one short reason>

CURRENT-VOCABULARY GATE:
PASS — <one short reason>

PROMPT-1 OBJECT GATE:
PASS — <one short reason>

HUMAN-Q-LABEL GATE:
PASS — <one short reason, or N/A when Q1–Q5 labels are not visible>

HUMAN-IMMERSION GATE:
PASS — <one short reason>

PROMPT-3 FREEDOM GATE:
PASS — <one short reason>
```

## PROMPT 1 — IMAGINE

```text
<complete Prompt 1 text only>
```

## PROMPT 2 — UNDERSTAND

```text
<complete Prompt 2 text only>
```

## PROMPT 3 — REVALIDATE AND MOVE FORWARD

```text
<complete Prompt 3 text only>
```
````

### Copy-pasteability rules

Each of the three prompt fences must be directly pasteable into another agent **without editing**.

Therefore:

- no commentary before or after a prompt inside its fence;
- no phrases such as "here is Prompt 1";
- no analysis notes mixed into the prompt;
- no "two notes on how I applied the schema" after the prompts;
- no nested fenced code blocks inside a prompt fence;
- if a prompt needs a diagram, table, template, or mini-structure, express it as plain indented text inside the outer fence;
- no placeholders that the user must manually replace when the information is already known;
- Prompt 2 and Prompt 3 must contain the actual target/repository links when available;
- Prompt 3 must contain the actual identity capsule, not instructions saying to add one later.

### Pass-specific identity rule

**Prompt 1 — IMAGINE**

Use TARGET ANCHORS, PROBLEM KERNEL where applicable, human outcome, genuine constraints, domain, and imagination object.

Do not include live current-system links or current-answer material.

Do not explain this omission inside Prompt 1. The prompt should read as a complete human/domain scenario, not as a methodology instruction.

**Prompt 2 — UNDERSTAND**

Include the exact target and repository/system links when available.

**Prompt 3 — REVALIDATE AND MOVE FORWARD**

Include this identity capsule with real resolved values:

```text
TARGET:
<exact title/name>

TARGET LINK:
<canonical target URL>

REPOSITORY / SYSTEM:
<parent repository/system>

REPOSITORY LINK:
<canonical repository/system URL>

UNDERLYING HUMAN PROBLEM:
<the blind problem Prompt 1 was built from>
```

Omit only fields that genuinely do not exist.

### No extra output

Do not add:

- a fourth prompt;
- explanatory prose before the preflight;
- commentary between prompt blocks;
- implementation notes after Prompt 3;
- a second summary of how you applied the schema.

The shared SCHEMA BASIS plus each lot's visible preflight and three prompt fences are the complete deliverable.

After Prompt 3, STOP. Do not append any admission/qualification/certification block, evaluator request, fourth stage, or extra question package.

---

# SILENT QUALITY CHECKS BEFORE OUTPUT

Do not show these checks outside the visible gate results in the PREFLIGHT RECORD.

### Lot-count / level-fidelity check

Does the output contain exactly the number of lots the user requested?

Does each lot preserve the requested level exactly?

If a tab-level lot became an issue-level lot, fail.

### Specificity-floor check

Is Prompt 1 recognisably about this exact requested target and level?

Could it be pasted unchanged into many unrelated projects?

If yes, fail as too generic.

### Schema-freshness check

When canonical GitHub is the schema source, is `SCHEMA FETCH STATUS = LIVE_THIS_RUN` with a real current content SHA?

If not, fail before evaluating prompts.

### Legacy-signature check

Does the generated deliverable contain any retired active field/instruction listed by the LEGACY-SIGNATURE REJECTION GATE?

If yes, fail and regenerate from current schema.

### Visible-preflight check

Is the complete PREFLIGHT RECORD visible?

If it is hidden or replaced by “preflight completed,” fail.

### Copy-pasteability check

Are Prompt 1, Prompt 2 and Prompt 3 each isolated in one clean outer text fence and directly pasteable without editing?

If there is commentary mixed into a prompt, known placeholders, nested fences, or notes after Prompt 3, fail.

### Complex-mode Q1–Q5 check

If COMPLEX MODE is ON, does Prompt 1 cover all five human reasoning lenses from Appendix H?

Specifically:
- path/ownership/consumer;
- concrete reconstruction;
- change/invariant/falsifier;
- independent check;
- first bounded proof slice.

If any lens is missing, fail.

Do not accept five generic bullet questions. They must be expressed in the language of this target and its PROBLEM KERNEL.

### Human-immersion check

Does Prompt 1 begin inside the person's real situation and stay there?

Fail if it mentions later passes, fixed references, repositories to avoid inspecting, schema mechanics, gates, quarantine, or being "held to" a future comparison.

The method must be invisible in Prompt 1.

### Problem-witness check

For ISSUE_TASK, did the target contain a real benchmark/example/trace/dataset/drawing/journey/dependency case that materially exposes the issue?

If yes, does Prompt 1 actually use it and demand a concrete independent work product?

If not, fail as abstract.

### Witness-independence check

Are reported witness outputs framed as claims to reproduce/falsify rather than truths to inherit?

Is today's interpretation/recommendation still quarantined?

If not, fail as contaminated.

### Task-contract fidelity check

For ISSUE_TASK, does Prompt 1 preserve the issue's WHY NOW, starting premise, responsible actor/job, owned question, and relevant ownership boundary?

If not, fail as over-generalised.

### Neighbour-separation check

Could Prompt 1 serve the parent or nearest sibling issue unchanged?

If yes, fail.

### Human Q-label check

If Q1–Q5 labels are visible, do they sound like natural, target-specific questions/tasks a practitioner would actually ask?

Reject taxonomy labels and protocol metadata.

### Mode-isolation check

When COMPLEX MODE is ON, are Q1–Q5 expressed only as Prompt-1 reasoning lenses?

Reject any extra question package, routing metadata, certification/qualification block, evaluator requirement, or admission stage inserted between the three prompts.

### Same-issue identity check

For ISSUE_TASK, after removing the title/number, is the particular issue still distinguishable from sibling issues?

If not, restore the PROBLEM KERNEL.

### Kernel-coverage check

For ISSUE_TASK, does every load-bearing PROBLEM KERNEL fact materially survive into Prompt 1?

If not, the prompt is too generic.

### Answer-exclusion check

For ISSUE_TASK, does any CURRENT ANSWER QUARANTINE fact leak into Prompt 1 directly or through generic paraphrase?

If yes, remove it.

### Goldilocks-corridor check

Is the issue-level Prompt 1 simultaneously:

- recognisable as this issue; and
- not pre-solved by today's issue text?

Both must pass.

### Reality-quarantine check

Are CURRENT ARTIFACT FORM, CURRENT STATED ANSWER / IMPLEMENTATION, and CURRENT-STATE FACTS absent from Prompt 1 unless independently justified as genuine constraints?

### Artifact-erasure check

If today's issue/artifact/implementation disappeared, would Prompt 1 still make essentially the same sense?

If not, fail.

### Current-vocabulary check

Did any important Prompt-1 noun or scenario detail come from today's target rather than the blind human problem?

If yes, remove it unless independently justified.

### Laundered-generalisation check

Did the generator merely replace issue-specific proper nouns with generic nouns while preserving today's issue narrative?

If yes, fail.

The correction is:
- restore the stable PROBLEM KERNEL;
- remove today's options/evidence interpretation/implementation answer.

### Human-problem check

Does UNDERLYING HUMAN PROBLEM describe what would still need solving if the current artifact had never existed?

### Prompt-1 object check

Would a perfect answer to Prompt 1 create the independent reference picture needed for that underlying problem?

### Reality check

Does Prompt 2 force inspection of live evidence rather than trusting issue prose or old plans?

### In-flight-work check

Does Prompt 2 distinguish current baseline from relevant near-future work without pretending open work is merged?

### Prompt-2/3 identity check

When links exist, does Prompt 2 contain the exact target and repository/system links?

Does Prompt 3 independently identify the exact target and repository/system?

Prompt 1 may omit live links to protect blindness.

### Goalpost check

Does Prompt 3 explicitly return to the exact Prompt-1 answer?

### Artifact-survival freedom check

Can Prompt 3 legitimately preserve, update, narrow, split, replace, close, defer, move elsewhere or leave unchanged today's artifact?

If it mandates an improved version of the artifact before comparison, fail.

### Rediscovery check

Does Prompt 3 ask what the goal/problem means **now**, rather than merely count old checklist items?

### Example-vs-problem check

Does Prompt 3 distinguish the exposing example from the reusable problem underneath it?

### Restraint check

Can Prompt 3 conclude no change, close, defer, collect evidence first, or leave this alone?

### Evidence check

Does Prompt 3 return to real examples/evidence to test the conclusion?

### Handover-reasoning check

Does Prompt 3 hand over:

```text
destination
→ reality
→ real gap
→ chosen move
→ deliberately not done
→ real evidence/example
→ unresolved
→ where next
→ what changes our mind
```

If handover is mainly branch/commit/PR topology or a task checklist, fail.

Operational details may supplement the reasoning relay, never replace it.

If any check fails, revise before output.

---

# COMPLEX MODE — Q1–Q5 HUMAN REASONING


Use this appendix **only when COMPLEX MODE = ON** because the user explicitly used the word **complex** for that target/lot.

Complex mode is defined **entirely inside this schema**.

The five reasoning lenses are:

```text
Q1 — trace the real path from inputs/evidence to the result or decision that matters,
     including where authority comes from and who relies on it.

Q2 — independently reconstruct one concrete real case; for quantitative work,
     use the real payload when available and show intermediate reasoning.

Q3 — change one load-bearing input/assumption; state what should change,
     what must remain invariant, and what observation would falsify the model.

Q4 — verify the important conclusion by a genuinely independent route;
     reproduce reported comparisons rather than inheriting them.

Q5 — return to the issue's owned question and identify the smallest
     no-regret or uncertainty-reducing next move.
```

These are **Prompt-1 reasoning lenses only**.

They do not create another workflow stage, question package, admission step, evaluator requirement, or protocol outside Prompt 1.

In **Prompt 1**, preserve the reasoning intent but translate it into a first-principles human conversation.

The future agent should not be told about the hidden/current-system distinction; that separation is enforced by the generator.

## Governing rule

> **Complex mode makes Prompt 1 deeper, not more mechanical.**

Do not paste external workflow/certification vocabulary into Prompt 1.

Do not ask the future agent to inspect current files, functions, current state owners, current benchmarks, or current implementation steps.

Instead ask the human equivalents below using the target's own domain language and PROBLEM KERNEL.

## Q1 — Human path: how does truth travel?

Canonical intent:

```text
production path
state owner
authority source
downstream consumer
```

Human Prompt-1 form:

> Start with the selected PROBLEM WITNESS when one exists. Trace the real path from its physical/business/learning inputs to the result or decision that matters. Where does each important quantity, fact or authority come from? What is source-defined, what is derived, what is assumed, and who relies on the result next?

Adapt this to the target.

Examples:

```text
engineering tab:
drawing + geometry + loads
→ interpretation
→ governed calculation
→ result
→ engineering review

learning issue:
real question
→ learner action required
→ prerequisite
→ teaching location
→ learner retry
```

The point is to expose the natural chain of custody/meaning without knowing today's architecture.

## Q2 — Human reconstruction: can we work one real case through?

Canonical intent:

```text
engineering reconstruction
concrete payload values when quantitative
intermediate result
expected result
```

Human Prompt-1 form:

> Work the selected real witness through from beginning to end. If it is quantitative, use the actual retained payload when available and show intermediate reasoning. If a reported output exists, reproduce or falsify it independently. Identify exactly where source-defined reasoning ends and any extra assumption begins.

If no real witness exists, then choose one representative case and use plausible values.

For non-quantitative targets, reconstruct the actual example/dependency/journey rather than inventing a generic scenario.

This question prevents complex Prompt 1 from becoming abstract consultancy prose.

## Q3 — Human stress test: what changes, what must not, and what would prove us wrong?

Canonical intent:

```text
explicit mutation
protected invariant
exact falsifier
```

Human Prompt-1 form:

> Now change one important thing. What should legitimately change because of it? What must remain true no matter what? What observation would make you stop and say, "our understanding is wrong"?

When a witness exists, mutate one of its load-bearing inputs, assumptions, authority conditions, or dependencies.

Use a change that belongs to the PROBLEM KERNEL, not today's bug list.

Examples:

```text
change a load
change geometry
change a prerequisite
change a document size
change an authority assumption
change the order of one dependency
```

The answer should reveal the deep invariant and a real falsifier.

## Q4 — Human independent check: how would we know without trusting ourselves?

Canonical intent:

```text
independent verification
benchmark/oracle
predicted result
tolerance/exactness
```

Human Prompt-1 form:

> Check the witness by a genuinely independent route. If the witness itself is an external benchmark, first build your own transparent calculation/derivation and only then compare against the benchmark. Recalculate any reported agreement yourself. Explain what the comparison supports and, separately, what it cannot establish.

Possible independent routes include a hand calculation, second source, benchmark, physical argument, second representation, real example, or separately derived dependency analysis.

Where meaningful, ask what level of agreement would count and why.

Independence matters more than having many checks.

## Q5 — Human discriminating next step: what is the smallest no-regret or uncertainty-reducing move?

Canonical intent:

```text
first safe bounded change
predicted before
predicted after
verification
```

Prompt 1 must not turn this into a patch plan for today's repository.

Translate it according to the issue type.

For implementation/technical-proof issues, it may be a **first bounded proof**.

For decision, coordination, sequencing, or closure issues, it may instead be the **smallest no-regret action or discriminating evidence step**:

> Given what the independent witness taught you, what is the smallest next move that either reduces uncertainty about the OWNED QUESTION or produces value under all plausible dispositions? What would you predict before doing it? What result would make you proceed, wait, narrow, move work elsewhere, or stop?

Valid Q5 conclusions include:

```text
another calculation
a deliberately discriminating benchmark
collect one missing piece of evidence
prepare an owner decision
do work useful under either outcome
wait
defer
no further technical work yet
```

Do not manufacture implementation merely because Q5 asks for a next step.

## ISSUE_TASK anchoring for complex Q1–Q5

For ISSUE_TASK, every Q1–Q5 lens must answer the **OWNED QUESTION**.

Do not let complex mode broaden the prompt into the product, parent programme, or end-user journey unless the issue itself owns that level.

In particular:

- Q1 traces the truth/authority path through the selected witness and ties it to this issue's decision.
- Q2 independently reconstructs the witness using its real payload when available.
- Q3 mutates a witness input/assumption or task-contract premise and protects the issue's invariant.
- Q4 independently checks the witness/report and separates evidence from authority/conclusion.
- Q5 returns to the OWNED QUESTION and chooses the smallest no-regret or uncertainty-reducing move.

For a coordination/decision issue with a technical witness, do **not** force Q2 to be a generic programme case.
Work the technical witness first if understanding it is what makes the coordination/decision question intelligible.

Each lens must materially connect back to the ISSUE TASK CONTRACT.

## Human weaving requirement

Do not produce five disconnected exam questions.

The preferred shape is a natural progression:

```text
Start with the concrete problem witness.
→ trace how the real inputs become a result/decision
→ independently work/reconstruct the witness
→ disturb one important input/assumption
→ check the reported result/conclusion independently
→ return to the issue's OWNED QUESTION
→ identify the smallest no-regret or uncertainty-reducing move
```

Prompt 1 may use paragraphs, a journey, or conversational questions.

The labels Q1–Q5 are for the generator's internal coverage check, not normally for the future agent.

## Human-visible Q1–Q5 labels

The internal Q1–Q5 semantics are **coverage categories**, not surface language.

If the user explicitly asks to see `Q1` through `Q5`, keep the numbers but translate every visible heading into a short, natural, target-specific question or task.

Use this test:

> **Would an experienced practitioner actually say this heading to another practitioner across a desk?**

If no, rewrite it.

For example, for a quantitative engineering benchmark issue:

```text
Good:
Q1 — From these real inputs, where does the governing method take you?
Q2 — Can you reproduce the reported result yourself?
Q3 — What changes when the case moves outside the directly supported condition?
Q4 — Why does the independent comparison agree, and what does that actually prove?
Q5 — Given what you learned, what is actually worth doing next?

Bad:
Q1 — PRODUCTION_PATH
Q2 — ENGINEERING_PROBLEM
Q3 — BOUNDARIES_INVARIANTS
Q4 — VERIFICATION
Q5 — FIRST_SAFE_SLICE
```

Also reject machine/protocol metadata inside Prompt 1 such as:

```text
anchors:
evidence_required:
required_output_keys:
reconstruction_mode:
payload.source:
payload.values:
oracle_refs:
independence_requirement:
step_refs:
mutation.protected_invariant:
mutation.falsifier:
```

Those concepts may guide the generator internally.

They must be rewritten into ordinary practitioner language in the generated prompt.

The future agent should encounter a **real question**, not a schema field.

---

## Relationship to the three-pass method

Complex Q1–Q5 mode affects **Prompt 1 only**.

```text
PROMPT 1
independent human Q1–Q5 reasoning picture

PROMPT 2
live repository/system reality

PROMPT 3
exact Prompt-1 picture + Prompt-2 reality
→ rediscover the present problem and smallest justified response
```

Do not repeat Q1–Q5 mechanically in Prompts 2 or 3 unless the target itself genuinely benefits from those questions.

## Complex-mode anti-generic test

A complex Prompt 1 fails if the five questions could be copied unchanged to an unrelated project.

Each lens must use:
- the correct user-requested level;
- TARGET ANCHORS;
- PROBLEM KERNEL where applicable;
- concrete domain objects;
- the selected PROBLEM WITNESS when one exists;
- a concrete INDEPENDENT WORK PRODUCT;
- a realistic person/journey;
- genuine constraints.

Complex mode should make the prompt **more concrete and diagnostic**, not longer for its own sake.

## Example — complex issue-level engineering decision with a benchmark witness

Weak:

> Trace the process. Reconstruct the problem. State the invariant. Validate independently. Pick a first slice.

Still too mechanical.

Also weak:

> How should a responsible organisation decide whether to continue a release programme?

Too abstract when the issue already contains a real engineering case.

Better:

> Start with the retained real-vessel benchmark case that creates the tension. Reconstruct its physical geometry, loads, nondimensional parameters and governing-source path. Work the calculation transparently as far as the source permits. If the source does not specify a required non-tabulated step, stop and identify the exact missing rule before exploring any extra assumption.
>
> Then independently reproduce the reported external-software comparison. Recalculate the differences and governing location yourself. Explain separately what close numerical agreement supports and what it cannot establish about source/method authority.
>
> Perturb the case across meaningful input/authority conditions. Identify the invariant and a real falsifier.
>
> Finally return to the issue-level decision: given what this concrete case taught you, which downstream work is no-regret, which is conditional on an owner disposition, what evidence would most reduce uncertainty, and when is doing nothing yet the correct next move?

That is Q1–Q5 in human form because the concrete witness drives the reasoning rather than decorating it.

---

# REGRESSION OWNERSHIP

Historical target-specific regressions, stale-output examples and exact forbidden signatures belong in executable tests and validators, not in this production schema.

The production schema must remain target-neutral so it cannot supply stale answer-side context for the very target it is asked to generate.

---

# FINAL PRINCIPLE

The generator should make a future agent think in this order:

```text
Prove the current schema basis first.

Read the user-authoritative target carefully.

What answer/form does the target currently carry?
Quarantine that.

If today's artifact and implementation had never existed,
what human problem would still remain?

Before seeing today's answer,
what would strong handling of that problem look like?

What is actually true today?

Put the independent picture beside reality.

Does today's artifact deserve to survive in its current form?

What meaningful distance genuinely remains?

What is the smallest justified response?

What real evidence confirms or challenges that conclusion?

What understanding must the next person inherit?
```

The method is constant:

> **Read the target to discover the problem behind it. Then mentally throw away the target's current answer for Prompt 1.**

Prompt 1 is independent not only of the code, but—where possible—of the current solution form itself.

But independence is not vagueness.

> **Prompt 1 must be blind to today's answer while remaining richly specific to the user-requested target, level, domain and job-to-be-done.**

The user's lot boundaries are authoritative. A tab-level request stays tab-level; a related issue becomes evidence, not a substitute target.

For issue-level work, preserve the **ISSUE TASK CONTRACT**, then its **PROBLEM KERNEL**, and—when one exists—the **PROBLEM WITNESS** that makes the issue concrete. Explicitly quarantine the current answer and the current interpretation of that witness:

> **Erase today's answer, not the facts that make it the same issue.**

Construction rule:

```text
Prompt 1 =
ISSUE TASK CONTRACT
+ PROBLEM KERNEL
+ TARGET ANCHORS
+ PROBLEM WITNESS when available
+ HUMAN OUTCOME
+ GENUINE CONSTRAINTS
- CURRENT ANSWER QUARANTINE
- WITNESS INTERPRETATION QUARANTINE
```

The issue-level blind pass must live inside the Goldilocks corridor:

```text
recognisable as this issue
but
not reconstructable as today's answer
```

That means two independent axes must both be correct:

```text
IDENTITY PRESERVATION
keep the facts that make it this issue

ANSWER INDEPENDENCE
remove the facts that tell you how today's repository has chosen to answer it
```

Do not trade one for the other.

When the user explicitly says **complex**, add one more requirement:

> **Prompt 1 must reason through Q1–Q5 in human form: trace the real witness/path, independently reconstruct it, stress/falsify it, verify it independently, then return to the issue's owned question and choose the smallest no-regret or uncertainty-reducing move.**

Complexity must deepen specificity and falsifiability; it must never become generic ceremony.

Internal Q1–Q5 taxonomy must also disappear at the surface:

> **If Q1–Q5 are shown, their labels must sound like real questions/tasks from the target domain, not names of reasoning categories.**

Prompt 1 must also be **method-invisible**:

> **The future agent should experience a real person, real job, real objects, real stakes and real questions — not instructions about the three-pass method.**

Blindness is enforced by the generator, not narrated to the agent.

Prompt 2 brings reality back.

Prompt 3 decides what deserves to survive.

The handover preserves the reasoning journey so the next agent inherits understanding, not merely activity.
