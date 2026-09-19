# Three-Pass Prompt Generator Schema

> Human-executable prompt schema for generating three sequential, copy-pasteable prompts.
>
> This is intentionally a Markdown schema rather than a JSON Schema. Its job is to make an ordinary agent reliably produce the same reasoning pattern across different **target purposes** and **target scopes** without drifting into a larger neighbouring problem.

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

Its purpose is to let the user catch a wrong interpretation before running the prompts.

Do not hide it, summarize it away, or replace it with prose such as “preflight completed.”

## A. Resolve the exact target

If the user provides a URL to an issue, PR, repository, document, plan, register, or other live artifact, **open that exact target first**.

Extract:

```text
TARGET TITLE:
<exact title or stable name>

TARGET LINK:
<canonical URL when available>

PARENT REPOSITORY / SYSTEM:
<owner/repo or parent system when applicable>

REPOSITORY / SYSTEM LINK:
<canonical parent URL when available>
```

Do not infer the target from its repository name or nearby work.

If the target cannot be inspected and its meaning is not otherwise supplied clearly, fail closed rather than inventing it.

## B. Freeze the request mode and target scope

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

Choose one target scope:

```text
PRODUCT
REPOSITORY_SYSTEM
TASK_ARTIFACT
```

These describe the assignment and its width. They do **not** decide what Prompt 1 imagines.

## C. Snapshot CURRENT REALITY — then quarantine it

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
```

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

## D. Recover the BLIND REFERENCE

Now mentally remove the current issue text, artifact form, implementation, roadmap, checklist, and proposed solution.

Ask:

> **If the current target artifact had never been created, what human problem would still exist?**

Complete:

```text
UNDERLYING HUMAN PROBLEM:
<the problem that survives even if today's issue/artifact/implementation disappears>

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

Better:

```text
UNDERLYING HUMAN PROBLEM:
after substantial work has happened, determine what genuinely remains,
what requires judgement rather than more implementation,
what can proceed independently, what has become historical,
and whether the remaining path is still worth pursuing

IMAGINATION OBJECT:
excellent judgement about what genuinely remains in an evolved engineering programme
```

Prompt 2 may later discover that a live register is a useful solution.

Prompt 1 must not assume that conclusion.

## E. Freeze Prompt 2's REALITY OBJECT

Complete:

```text
REALITY OBJECT:
"Prompt 2 must establish what is actually true today about ______."
```

This may explicitly include the current target artifact, repository, issue history, implementation, PRs, tests, examples, and in-flight work.

## F. Freeze Prompt 3's COMPARISON QUESTION — not its artifact form

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

## G. Visible PREFLIGHT RECORD

The visible record must contain:

```text
TARGET TITLE:
TARGET LINK:
PARENT REPOSITORY / SYSTEM:
REPOSITORY / SYSTEM LINK:

REQUEST MODE:
TARGET SCOPE:

CURRENT REALITY — QUARANTINED FROM PROMPT 1
CURRENT ARTIFACT FORM:
CURRENT STATED ANSWER / IMPLEMENTATION:
CURRENT-STATE FACTS:

BLIND REFERENCE — THE ONLY SIDE ALLOWED TO SHAPE PROMPT 1
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

PROMPT-3 FREEDOM GATE:
PASS — <one short reason>
```

Do not draft Prompt 1 until these fields and gates are resolved.

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
- For an issue currently expressed as a “register,” “matrix,” or “roadmap,” that artifact form usually should **not** survive unless the user explicitly requires that form.

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

If B, remove it unless you can independently justify it as a genuine constraint.

Hiding the issue number while paraphrasing its current state is **not** blindness.

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

If Prompt 3 mandates a better version of today's artifact before comparison is complete, fail.

Examples of failure:

```text
"Produce the reconciled register"
when an earlier section asks whether the register is still the right instrument.

"Complete the matrix"
when the comparison may show the matrix is no longer the right remaining work.

"Update the roadmap"
when the roadmap may have become historical.
```

Prompt 3 may require a **decision and reasoning**, but must not pre-decide the survival of the current solution form.

---

# STEP 1 — BUILD PROMPT 1 ONLY FROM THE BLIND REFERENCE

This is the most important construction rule.

Allowed inputs to Prompt 1:

```text
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

Prompt 1 must explicitly tell the future agent not to inspect the current repository/issue/implementation.

# PROMPT 1 — IMAGINE

Generate a self-contained first-principles prompt from the **BLIND REFERENCE only**.

It should begin from:

- the underlying human problem;
- the intended human outcome;
- genuine constraints;
- relevant domain realities;
- the required expertise.

It should explicitly tell the future agent **not to inspect the current repository, issue, roadmap, implementation, or current artifact yet**.

Use human language and mental simulation.

Good forms include:

> Imagine the person actually facing this situation.

> Walk through what they need to understand before acting.

> What should become possible?

> What would make the result trustworthy?

> What would look like progress but actually be a trap?

> What should remain true even if today's implementation were rewritten from scratch?

Do not reveal the current solution form merely because you know it.

Do not tell the future agent there is a register, matrix, roadmap, particular architecture, specific sequencing, or named abstraction unless that is independently part of the human requirement.

### Prompt 1 must create a fixed reference picture

At the end require something equivalent to:

> **“If this were handled really well, this is what would become possible…”**

Then ask for the principles underneath that picture.

That answer becomes the fixed reference point for Prompt 3.

### Product-level note

At product level, the product category itself can be part of the human goal. Prompt 1 may therefore imagine the desired product experience broadly.

What remains forbidden is leaking the **current product implementation**.

### Repository/system-level note

Imagine the desired human/system outcome independent of today's repository architecture, roadmap, phase names and implementation vocabulary.

### Task/issue-level note

Imagine what successful handling of the underlying problem would make possible.

Do **not** assume the current issue's proposed artifact or work breakdown is the correct instrument.

Run the ARTIFACT-ERASURE, CURRENT-VOCABULARY and PROMPT-1 OBJECT gates before accepting Prompt 1.

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

## D. Does the current artifact still deserve to exist in its present form?

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

Do not assume “COORDINATE” means “produce a better register.”

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

The generator output has **four visible sections**:

1. one **PREFLIGHT RECORD**;
2. exactly three **copy-pasteable prompt blocks**.

The preflight is metadata, **not a fourth prompt**.

Output this structure and nothing else:

```markdown
## PREFLIGHT RECORD

```text
TARGET TITLE:
TARGET LINK:
PARENT REPOSITORY / SYSTEM:
REPOSITORY / SYSTEM LINK:

REQUEST MODE:
TARGET SCOPE:

CURRENT REALITY — QUARANTINED FROM PROMPT 1
CURRENT ARTIFACT FORM:
CURRENT STATED ANSWER / IMPLEMENTATION:
CURRENT-STATE FACTS:

BLIND REFERENCE — THE ONLY SIDE ALLOWED TO SHAPE PROMPT 1
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
```

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

Keep it blind. Use the human purpose, genuine constraints, domain, and imagination object.

Do not include a live issue/repository link when following it would expose the current answer.

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

The visible preflight plus the three prompt fences are the complete deliverable.

---

# SILENT QUALITY CHECKS BEFORE OUTPUT

Do not show these checks outside the visible gate results in the PREFLIGHT RECORD.

### Visible-preflight check

Is the complete PREFLIGHT RECORD visible?

If it is hidden or replaced by “preflight completed,” fail.

### Copy-pasteability check

Are Prompt 1, Prompt 2 and Prompt 3 each isolated in one clean outer text fence and directly pasteable without editing?

If there is commentary mixed into a prompt, known placeholders, nested fences, or notes after Prompt 3, fail.

### Reality-quarantine check

Are CURRENT ARTIFACT FORM, CURRENT STATED ANSWER / IMPLEMENTATION, and CURRENT-STATE FACTS absent from Prompt 1 unless independently justified as genuine constraints?

### Artifact-erasure check

If today's issue/artifact/implementation disappeared, would Prompt 1 still make essentially the same sense?

If not, fail.

### Current-vocabulary check

Did any important Prompt-1 noun or scenario detail come from today's target rather than the blind human problem?

If yes, remove it unless independently justified.

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

# APPENDIX A — CASE STUDY: PRODUCT LEVEL

## Input example

```text
TARGET:
A static, browser-based PDF editor.

HUMAN GOAL:
A strong PDF editor usable by an individual without operating a backend service.

USERS:
Personal and professional users on phone and desktop.

IMPORTANT EXPECTATIONS:
Page insertion/deletion/reordering, headers/footers, rotation, text overlay,
large-PDF handling, annotations/comments, non-flattened saving, OCR,
inline text editing where practical, APIs for integration.

CONSTRAINTS:
Mostly client-side/static architecture.
Built and maintained by one developer with AI-agent help.
```

## Frozen preflight

```text
TARGET NATIVE DELIVERABLE:
working browser PDF product / product direction

REQUEST MODE:
TARGET TITLE:
Static browser-based PDF editor
TARGET LINK:
not supplied
PARENT REPOSITORY / SYSTEM:
not supplied
REPOSITORY / SYSTEM LINK:
not supplied


REVIEW

TARGET PURPOSE:
This product exists so that users can seriously edit, inspect and save real PDFs
in a browser-oriented environment without depending on backend infrastructure.

TARGET SCOPE:
PRODUCT

EXPERTISE:
PDF/browser architecture and document-editing product expertise

IMAGINATION OBJECT:
an excellent static/browser PDF editor experience and architecture

REALITY OBJECT:
the current PDF application's real architecture, editing journeys, performance,
persistence, supported operations and in-flight work

FINAL OUTPUT CONTRACT:
a product-level gap analysis and phased roadmap from current reality
toward the independent reference picture
```

**Gate expectation:** a perfect Prompt-1 answer describes the PDF product itself. PASS.

## What a good generated Prompt 1 should feel like

It should **not** say:

> “Evaluate whether PDF.js plus pdf-lib plus an IndexedDB page cache is the right architecture.”

That already contains an answer.

It should say something closer to:

> Imagine a professional-quality PDF editor that must work primarily in the browser without depending on a backend. Think from first principles about what a user should be able to do, how editing should feel on phone and desktop, how a 1,000-page document should behave, what must survive save/reopen, what operations are fundamentally easy or difficult in PDF, and what architectural mistakes would trap a one-developer project later. Do not inspect the existing app yet. End by describing what would become possible if this product were done really well.

## What a good generated Prompt 2 should feel like

It should now introduce the repository/application and ask the agent to follow real journeys such as:

```text
open large PDF
→ navigate
→ edit
→ reorder
→ annotate
→ save
→ reopen
```

It should inspect current code, dependencies, rendering, document mutation, persistence, mobile/desktop UI, tests, issues and active PRs.

It should explain what the app has actually become without redesigning it yet.

## What a good generated Prompt 3 should feel like

It should explicitly return to the original first-principles PDF picture and ask:

> Which parts of the existing app already satisfy it?

> Which historical limitations are already gone?

> Which real user journeys still break?

> Is a visible symptom such as slow scrolling actually a rendering/lifecycle problem underneath?

> What is the smallest durable change?

Then it should produce a product-level phased path and explicitly say what should **not** be built yet.

---

# APPENDIX B — CASE STUDY: REPOSITORY / SYSTEM LEVEL

## Input example

```text
TARGET:
https://github.com/reallaksh19/Grade9V3

HUMAN GOAL:
A serious self-study learning system for Grade-9 learners, eventually spanning Physics,
Mathematics and Chemistry, maintained by one developer with agent help.

USERS:
Learners studying independently from real curriculum material, worksheets and questions.

CONSTRAINTS:
The system must scale without creating a special architecture for every subject or topic.
Machine checks must not be mistaken for proof that material actually teaches.
```

## Frozen preflight

```text
TARGET NATIVE DELIVERABLE:
revalidated Grade-9 system/programme direction

REQUEST MODE:
TARGET TITLE:
Grade9V3 repository
TARGET LINK:
https://github.com/reallaksh19/Grade9V3
PARENT REPOSITORY / SYSTEM:
reallaksh19/Grade9V3
REPOSITORY / SYSTEM LINK:
https://github.com/reallaksh19/Grade9V3


REVIEW

TARGET PURPOSE:
This system exists so that learners can study independently, understand ideas,
practise, recover from misunderstandings, repair prerequisites and transfer learning.

TARGET SCOPE:
REPOSITORY_SYSTEM

EXPERTISE:
learning-system, curriculum and educational-product architecture expertise

IMAGINATION OBJECT:
an excellent Grade-9 self-study system and learner journey

REALITY OBJECT:
what Grade9V3 actually provides today across teaching, practice, routing,
feedback, subjects, evidence and current work

FINAL OUTPUT CONTRACT:
a present-day definition of what Grade 9 should mean, what is already solved,
what genuinely remains, and an ordered programme for closing that distance
```

**Gate expectation:** a perfect Prompt-1 answer describes the learner/system outcome without inheriting Grade9V3 vocabulary. PASS.

## What a good generated Prompt 1 should feel like

It should **not** mention matrices, Core1/Core2, gates, current routing enums, or the existing repository structure.

Instead it should ask:

> Imagine a Grade-9 learner studying mostly alone. They meet a new topic, think they partly understand it, attempt real questions, get stuck for different reasons, sometimes need an earlier prerequisite, and eventually need to solve unfamiliar problems independently. What should an excellent self-study system do from beginning to end? How should teaching, practice, diagnosis, repair, transfer, subject boundaries, learner evidence and maintainability work for one developer using agents? Do not inspect Grade9V3 yet.

The answer becomes the independent reference picture.

## What a good generated Prompt 2 should feel like

It should now inspect the live repository and discover:

- what the six products actually do;
- how subject-neutral and subject-specific concerns are separated;
- what Grade 9 currently means;
- what Physics, Mathematics and Chemistry genuinely contain;
- how routing and learner feedback actually behave;
- what has been proven by tests versus real questions versus real learners;
- what recent PRs have already changed;
- what active issues still represent current reality.

It should follow learner journeys rather than merely summarize directories.

## What a good generated Prompt 3 should feel like

It should return to the exact learner experience imagined in Prompt 1 and ask:

> What should survive?

> What architecture or roadmap concern used to matter but no longer does?

> What really prevents Grade 9 from feeling complete today?

> Is the missing thing architecture, content, routing, academic review, learner evidence, or something else?

> What should “complete enough for Grade 9” mean now?

It should then produce a phased repo-level path based on learner value and real dependency, not on old phase labels alone.

---

# APPENDIX C — CASE STUDY: TASK / ISSUE LEVEL

## Input example

```text
TARGET:
https://github.com/reallaksh19/Grade9V3/issues/19

HUMAN GOAL:
Make real Physics/Mathematics worksheet questions traceable to the reusable ideas a learner
must know, their genuine prerequisites, and where those ideas are taught.

CURRENT SYSTEM:
https://github.com/reallaksh19/Grade9V3
```

## Frozen preflight

```text
TARGET NATIVE DELIVERABLE:
bounded worksheet-to-learning content/mapping change

REQUEST MODE:
TARGET TITLE:
Complete Physics/Math matrices and capability mappings for worksheet-driven study routing
TARGET LINK:
https://github.com/reallaksh19/Grade9V3/issues/19
PARENT REPOSITORY / SYSTEM:
reallaksh19/Grade9V3
REPOSITORY / SYSTEM LINK:
https://github.com/reallaksh19/Grade9V3


CHANGE

TARGET PURPOSE:
This issue exists so that a real worksheet question can be connected to the reusable
learner ability it requires, the genuine earlier knowledge it depends on,
and where that knowledge is taught.

TARGET SCOPE:
TASK_ARTIFACT

EXPERTISE:
learning-system and curriculum-mapping expertise

IMAGINATION OBJECT:
an excellent worksheet-question-to-learning mapping outcome

REALITY OBJECT:
what Issue #19, the current repository, later PRs and real-question evidence
have already accomplished

FINAL OUTPUT CONTRACT:
a rewritten present-day Issue #19 containing only the meaningful remaining work
and its smallest durable solution
```

**Gate expectation:** a perfect Prompt-1 answer explains question → reusable ability → prerequisite → teaching location, not the whole Grade-9 system. PASS.

## What a good generated Prompt 1 should feel like

It should **not** begin with the issue's proposed files, historical donor PRs, matrix schema, or implementation checklist.

It should ask something closer to:

> Imagine a learner is stuck on a real worksheet question. What should a good self-study system be able to understand about that question? How should it identify the reusable learner action underneath the surface context, distinguish supporting ideas from true prerequisites, find where the idea is taught, and remain reusable across future worksheets? Do not inspect the repository or the issue implementation history yet.

## What a good generated Prompt 2 should feel like

It should now read the live issue, comments, current repository, related PRs and present subject content.

It should ask:

> Which parts of the original problem are already solved?

> What changed after the issue was written?

> Which current or recent PRs alter the near-future baseline?

> What real questions have exposed gaps?

> Which apparent gaps are deliberate boundaries?

It must not assume the original checklist is today's work.

## What a good generated Prompt 3 should feel like

It should return to the exact learner-centered conception from Prompt 1 and rewrite the task:

> “Given the current repository, the meaningful remaining work under this issue is…”

It should distinguish the exposing example from the reusable problem underneath it.

For example:

```text
river-crossing question
→ may expose reusable vector composition/component reasoning
→ should not automatically create a river-specific capability
```

It should identify what is already solved, what should remain untouched, the smallest durable remaining change, how at least two real questions will test it, and what the next agent needs to understand.

The final task may be much smaller than the historical issue. That is a successful outcome, not a failure.


---

# APPENDIX D — CASE STUDY: TASK LEVEL, COORDINATION TARGET

## Input example

```text
TARGET:
https://github.com/reallaksh19/Advanced_Analysis/issues/1855

CURRENT SYSTEM:
https://github.com/reallaksh19/Advanced_Analysis
```

## Current reality to quarantine

The live issue happens to be a **register** containing merge order, open work, blockers, decisions and corrections.

That fact belongs to Prompt 2.

It must not automatically define Prompt 1.

## Correct blind recovery

```text
UNDERLYING HUMAN PROBLEM:
A successor entering a complex engineering programme needs to determine what genuinely
remains, what is already solved or historical, what is executable work versus a decision,
what depends on what, and what can safely happen next without blindly continuing an old plan.

HUMAN OUTCOME:
The owner and next engineer can make the correct next move from a truthful understanding
of the programme rather than from inherited status prose.

IMAGINATION OBJECT:
excellent judgement about what genuinely remains and can safely happen next
in an evolved engineering programme
```

Notice what is intentionally absent:

```text
register
specific PR stack
specific red gates
specific owner decisions
current merge order
current corrections
```

Those are Prompt-2 discoveries.

## What a good Prompt 1 should feel like

Something closer to:

> Imagine taking over a long-running engineering programme after substantial work has already happened. Before spending another week, how would you determine what genuinely remains, what has become historical, what requires a human decision rather than more engineering, what can proceed independently, and whether some planned work should no longer be pursued? What evidence would you need to trust that picture, and what mistakes cause teams to keep solving yesterday's problems?

It should **not** say:

> Imagine an excellent live register.

That would inherit today's solution form.

## What Prompt 2 should do

Now reveal Issue #1855 and the repository.

Inspect the register claim-by-claim, reconstruct current and near-future baseline, verify dependencies, blockers, decisions, current work and stale statements.

Prompt 2 may conclude that the register is excellent, weak, stale, redundant, or no longer the right coordination surface.

## What Prompt 3 should do

Return to the independent picture of sound engineering judgement.

Then ask:

> Given today's reality, does #1855 remain the right instrument?

The result may be:

- preserve it unchanged;
- reconcile it;
- narrow it;
- split it;
- close it and return work to owning issues;
- replace it with another coordination surface;
- or defer action.

It must not be forced to “produce a better register.”

This case is the canonical test for **artifact-form contamination**.

---

# APPENDIX E — NEGATIVE CONTROL: ISSUE #1854

Issue #1854 exposed the strongest failure mode.

Its generated Prompt 1 was told, in supposedly blind form, that there was:

- recently landed work;
- in-flight work;
- infrastructure blockers;
- owner-reserved decisions;
- pre-existing failures;
- stale written plans;
- and one living register.

Those details were a sanitized restatement of the current issue.

The Prompt 1 then explicitly said:

> “The register is the thing you are imagining.”

That fails this schema.

A compliant preflight for #1854 would instead recover:

```text
UNDERLYING HUMAN PROBLEM:
After a major round of product fixes, determine what genuinely remains,
what is decision rather than implementation, what can proceed now,
what has become historical, and whether the remaining release path is worth pursuing.

IMAGINATION OBJECT:
excellent post-change engineering judgement about the true remaining path
```

The current register, gamma decision, CI failure, UI residue, hash issue and sequencing belong to Prompt 2.

Prompt 3 must be free to decide whether the register should survive at all.

If a future schema revision again generates “imagine an excellent register” for #1854, the schema has regressed.

---

# FIVE-CASE REGRESSION VALIDATION

Before considering a future schema revision safe, mentally run these controls:

| Case | Prompt-1 independent object | Main contamination risk | Prompt-3 freedom requirement |
| --- | --- | --- | --- |
| Static browser PDF editor | excellent browser PDF experience/product | current implementation architecture | may preserve/change architecture |
| Overall Grade9V3 | excellent Grade-9 self-study learner journey/system | Core/matrix/gate vocabulary | may redefine programme priorities |
| Grade9V3 Issue #19 | excellent question → reusable learning need → prerequisite → teaching outcome | matrix/rung/current checklist | may shrink/close/rewrite task |
| Advanced_Analysis Issue #1855 | excellent judgement about what genuinely remains and can safely happen next | “register” and current queue/details | may preserve/reconcile/replace/close register |
| Advanced_Analysis Issue #1854 | excellent post-change judgement about the true remaining path | sanitized restatement of issue as blind context | may preserve/reconcile/replace/close register |
| Advanced_Analysis Issue #1756 | excellent methodical qualification of shell capability from foundations through release | current architecture/child-roadmap form | may preserve/rewrite/split/retire roadmap |

### Critical negative control

The following must fail:

```text
TARGET CURRENTLY IS A REGISTER
→ therefore Prompt 1 imagines an excellent register
```

The correct logic is:

```text
read current register
→ recover problem behind it
→ quarantine register form
→ Prompt 1 imagines handling of underlying problem
→ Prompt 2 discovers the register
→ Prompt 3 decides whether register deserves to survive
```

### Output regression requirements

Every generated result must contain:

```text
VISIBLE PREFLIGHT RECORD

PROMPT 1
one clean copy-pasteable text block

PROMPT 2
one clean copy-pasteable text block

PROMPT 3
one clean copy-pasteable text block

NO EXTRA NOTES
after Prompt 3

HANDOVER
reasoning continuity, not merely operations
```

A result with sophisticated reasoning but contaminated Prompt 1, hidden preflight, broken copy-pasteability, predetermined artifact survival, or activity-log handover is a schema failure.

---

# FINAL PRINCIPLE

The generator should make a future agent think in this order:

```text
Read the target carefully.

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

Prompt 2 brings reality back.

Prompt 3 decides what deserves to survive.

The handover preserves the reasoning journey so the next agent inherits understanding, not merely activity.
