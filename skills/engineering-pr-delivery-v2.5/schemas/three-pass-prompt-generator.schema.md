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

The method is the same throughout, but the generator must freeze a **preflight record** before it is allowed to draft Prompt 1.

The preflight separates eight things that ordinary agents often collapse:

1. **Target identity** — the exact thing being discussed.
2. **Target native deliverable** — what kind of thing this target itself is meant to leave behind.
3. **Request mode** — what the user wants done now.
4. **Target purpose** — why this particular target exists.
5. **Target scope** — product, repository/system, or task/artifact.
6. **Expertise** — what kind of expert should reason about it.
7. **Imagination object / reality object** — what Prompt 1 may imagine and what Prompt 2 must inspect.
8. **Final output contract** — what Prompt 3 must ultimately produce.

A task can mention an entire product without being a product-level task. A register about a solver programme is not the same thing as the solver programme itself. **Expertise is not the object of reasoning.** A finite-element expert may be reasoning about a coordination register rather than designing a finite-element product.

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

# MANDATORY PREFLIGHT — DO NOT GENERATE PROMPTS YET

Before drafting Prompt 1, build the following record.

**This record is part of the required output. Always show it before the three prompts.**

Its purpose is not decoration. It lets the user catch a wrong target interpretation before spending time running the prompts.

Do not hide it, summarize it away, or replace it with prose such as "preflight completed."

## A. Resolve the exact target

If the user provides a URL to an issue, PR, repository, document, plan, register, or other live artifact, **open that exact target first**.

Do not infer its purpose from:

- the repository name;
- the technical domain;
- a title fragment;
- nearby work;
- prior memory;
- or the broader product mission.

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

If the target cannot be inspected and its purpose is not otherwise supplied clearly, **fail closed**: do not invent the target purpose from surrounding context.

## B. Freeze the target native deliverable

Complete:

> **“When this target succeeds, the thing it leaves behind is ______.”**

Name the artifact or outcome form native to the target itself.

Examples:

```text
product idea
→ working product / product direction

repository-wide review
→ revalidated system/programme direction

implementation issue
→ bounded implementation/content change

qualification issue
→ qualification evidence / governed acceptance closure

investigation issue
→ supported finding / bounded conclusion

decision issue
→ decision-ready evidence and alternatives

coordination register
→ current live register

architecture / closure umbrella
→ revalidated architecture + qualification/closure roadmap

handover task
→ successor-ready understanding
```

Do not infer this from REQUEST MODE alone.

```text
COORDINATE ≠ always REGISTER
REVIEW ≠ always ROADMAP
CHANGE ≠ always CODE
```

The target's own mission/body should tell you what kind of thing it is meant to leave behind.

## C. Freeze the request mode

Choose the single mode that best describes what the user wants done **now**:

```text
CONCEIVE
REVIEW
CHANGE
INVESTIGATE
DECIDE
COORDINATE
HANDOVER
```

This is about the user's current assignment, not the permanent mission of the target.

Examples:

```text
"Review this whole repository against first principles"
→ REVIEW

"Complete this implementation issue"
→ CHANGE

"Find out why this benchmark is wrong"
→ INVESTIGATE

"Help decide between these threshold options"
→ DECIDE

"Keep this merge/blocker register truthful"
→ COORDINATE
```

## D. Freeze the target purpose

Complete exactly:

> **“This target exists so that ______.”**

Describe the target itself, not a larger neighbouring product.

### Purpose proximity test

Ask:

> **Could this TARGET PURPOSE sentence be pasted unchanged onto the parent repository, programme, or several sibling issues and still sound equally correct?**

If yes, the purpose is probably too broad.

Rewrite it closer to **this target's native deliverable**.

Examples:

```text
Too broad:
"so an engineer can trust shell-analysis results"

Closer for an architecture/closure umbrella:
"so the still-valid shell-analysis work is organized into dependency-ordered
qualification boundaries from geometry through exact-head release"

Too broad:
"so learners can study Grade 9"

Closer for a question-mapping issue:
"so a real worksheet question can be traced to the reusable learner ability,
genuine prerequisites, and teaching location it requires"
```

## E. Freeze the target scope

Choose exactly one:

```text
PRODUCT
REPOSITORY_SYSTEM
TASK_ARTIFACT
```

Scope answers **how much surrounding system belongs inside the target**.

## F. Freeze the expertise

Complete:

> **“The future agent should reason with the expertise of ______.”**

Then apply this invariant:

> **EXPERTISE ≠ OBJECT OF REASONING**

Expertise tells the agent **how intelligently to think**.

It does not decide **what it is thinking about**.

Example:

```text
EXPERTISE:
senior structural / finite-element engineer

IMAGINATION OBJECT:
excellent live engineering programme register
```

This is valid.

Do not automatically turn a domain expert into a product-design prompt for that domain.

## G. Freeze the three prompt objects

Complete all three sentences:

```text
IMAGINATION OBJECT:
"Prompt 1 must independently imagine what an excellent ______ looks like."

REALITY OBJECT:
"Prompt 2 must establish what is actually true today about ______."

FINAL OUTPUT CONTRACT:
"Prompt 3 must ultimately produce ______."
```

These three lines are construction constraints, not suggestions.

## H. Build the complete preflight record

The record must now contain:

```text
TARGET TITLE:
TARGET LINK:
PARENT REPOSITORY / SYSTEM:
REPOSITORY / SYSTEM LINK:

TARGET NATIVE DELIVERABLE:
REQUEST MODE:
TARGET PURPOSE:
TARGET SCOPE:
EXPERTISE:

IMAGINATION OBJECT:
REALITY OBJECT:
FINAL OUTPUT CONTRACT:
```

Do not draft Prompt 1 until every applicable field is resolved.

---

# HARD GATE 1 — PROMPT-1 OBJECT GATE

Before generating Prompt 1, finish:

> **“If Prompt 1 were answered perfectly, the answer would be an excellent example of ______.”**

The blank must match the frozen **IMAGINATION OBJECT**.

Then compare that perfect answer with:

- TARGET NATIVE DELIVERABLE;
- REQUEST MODE;
- TARGET PURPOSE;
- TARGET SCOPE.

If it would instead solve a larger neighbouring problem, a smaller implementation detail, or a different kind of task:

> **REJECT THE DRAFT AND REGENERATE PROMPT 1.**

Do not continue to Prompt 2 until this gate passes.

---

# HARD GATE 2 — PROMPT-3 OUTPUT GATE

Before emitting Prompt 3, finish:

> **“If Prompt 3 were answered perfectly, its final deliverable would be ______.”**

The answer must match the frozen **FINAL OUTPUT CONTRACT** **and remain the same kind of thing as the TARGET NATIVE DELIVERABLE**.

Examples:

```text
PRODUCT review
→ product gap analysis + phased roadmap

REPOSITORY review
→ current system meaning + preserved strengths + remaining programme

IMPLEMENTATION change
→ rewritten present-day task + smallest durable change

INVESTIGATION
→ verified conclusion + bounded uncertainty

DECISION
→ decision-ready evidence package

COORDINATION
→ reconciled live register + executable frontier

HANDOVER
→ successor-ready continuity package
```

If Prompt 3 would instead produce a neighbouring product redesign, an unrequested implementation, or a generic roadmap:

> **REJECT THE DRAFT AND REGENERATE PROMPT 3.**

---

# STEP 0A — APPLY THE FROZEN TARGET PURPOSE

The mandatory preflight has already resolved the target identity, native deliverable, and request mode.

Now use the frozen **TARGET PURPOSE** before choosing or applying the target scope.

Silently complete this sentence:

> **“This target exists so that ______.”**

Fill the blank with the purpose of the target itself, not the broader mission of the product it happens to discuss.

This is mandatory for repositories, issues, tasks, plans, registers, audits and handovers.

### Purpose test

Ask:

> If this target were completed perfectly, what would become true?

Then ask:

> Would that complete the target itself, or am I accidentally describing a larger neighbouring problem?

Examples:

```text
Issue about capability mapping
→ exists so real questions can be traced to reusable teachable knowledge
→ implementation/content task

Issue that records merge queue + blockers + owner decisions
→ exists so the programme has one truthful current coordination register
→ coordination/register task

Issue asking whether a solver threshold should change
→ exists so an engineering decision can be made from sufficient evidence
→ decision task

Issue asking why a benchmark fails
→ exists so the cause can be established reliably
→ investigation task
```

Do **not** infer the target purpose from the amount of technical detail it contains.

A coordination issue can contain deep solver details while still being a coordination issue.

A handover can discuss an entire architecture while still being a handover.

### How REQUEST MODE shapes the same target purpose

Do not invent a second role taxonomy here. The preflight's **REQUEST MODE** is the single operation axis.

Use it like this:

#### CONCEIVE

Prompt 1 imagines the target itself done excellently from first principles.

Prompt 3 produces a conception, architecture or product direction appropriate to the target scope.

#### REVIEW

Prompt 1 creates an independent reference picture.

Prompt 2 reconstructs current reality.

Prompt 3 compares them and produces the bounded gap/programme appropriate to the target scope.

#### CHANGE

Prompt 1 imagines what successful completion of this specific change should make possible.

Prompt 3 rewrites the present-day task and identifies the smallest durable remaining change.

#### INVESTIGATE

Prompt 1 imagines what a trustworthy investigation must establish.

Prompt 3 produces a supported conclusion with bounded uncertainty, not an automatic implementation plan.

#### DECIDE

Prompt 1 imagines what evidence and trade-offs a responsible decision requires.

Prompt 3 produces a decision-ready package and preserves the authority boundary.

#### COORDINATE

Prompt 1 imagines what an excellent live coordination/register artifact must make knowable and actionable.

Prompt 3 reconciles current truth, blockers, dependencies, decisions and executable frontier.

#### HANDOVER

Prompt 1 imagines what a successor must know to continue safely.

Prompt 3 produces successor-ready continuity, including first safe action and stale conditions.

### Target-purpose anchor

Carry the completed sentence:

> “This target exists so that …”

through all three prompts.

Prompt 1 imagines that purpose done well.

Prompt 2 asks whether today's reality serves that purpose.

Prompt 3 asks what meaningful distance remains **for that same purpose**.

Do not silently substitute the mission of a neighbouring product, repository, programme or issue.

---

# STEP 0B — APPLY THE FROZEN TARGET SCOPE

The preflight has already chosen:

```text
PRODUCT
REPOSITORY_SYSTEM
TASK_ARTIFACT
```

Use that scope to decide how much surrounding system belongs inside each prompt.

**Request mode + target purpose come first. Scope comes after them.**

A task-level coordination register may mention a whole repository but still remain task-level. A repository-level review may inspect many tasks but still be system-level.

## PRODUCT LEVEL

Use when the underlying question is approximately:

> What should this product become?

Prompt 1 should think broadly about users, experience, capabilities, architecture, scale, quality, and long-term traps.

Prompt 3 should usually end in a product-level gap analysis and phased path.

## REPOSITORY / SYSTEM LEVEL

Use when the underlying question is approximately:

> What should this whole system become, and how far has it already travelled?

Prompt 1 should imagine the complete human outcome independently.

Prompt 2 should reconstruct the repository as a living system, including history and current work.

Prompt 3 should determine what should be preserved, what is historical, what genuinely remains, what “complete enough now” should mean, and what sequence makes sense.

## TASK / ISSUE LEVEL

Use when the underlying question is approximately:

> What should this particular piece of work actually make possible?

Prompt 1 should imagine successful completion without inheriting implementation assumptions from the issue.

Prompt 2 should determine what the current repository has already solved, including changes since the issue was written.

Prompt 3 should rewrite the task in today's terms and reduce it to the smallest meaningful remaining work.

Do not create three different methodologies. Use the same three-pass method with different purpose and zoom.

Before moving on, perform this silent check:

> **If Prompt 1 were answered perfectly, would it fulfil the purpose of this target, or would it solve a larger neighbouring problem?**

If it solves the larger neighbouring problem, your scope is wrong. Re-identify the target purpose before generating anything.

---

# STEP 1 — BUILD A BLIND BRIEF FOR PROMPT 1

This is the most important safeguard.

Before generating Prompt 1, silently separate the user's information into two conceptual buckets:

```text
BLIND BRIEF
- request mode
- target-purpose sentence: "This target exists so that ..."
- target scope
- expertise
- imagination object
- human goal
- intended users
- desired outcomes
- genuine constraints
- domain
- scale
- non-negotiable expectations

CURRENT-ANSWER CONTEXT
- repository structure
- existing abstraction names
- current schemas
- current architecture
- current issue checklist
- proposed implementation
- current roadmap
- current file names
- current PR solutions
```

Prompt 1 should be generated from the **BLIND BRIEF** wherever possible.

Do not leak CURRENT-ANSWER CONTEXT into Prompt 1 unless the information is itself a genuine human constraint.

### Example of the distinction

If an issue says:

> “Add three new matrix rungs and a capability mapping.”

do not make Prompt 1 ask whether three matrix rungs are needed.

Instead recover the human intention, for example:

> “A learner who gets stuck on a real question should be traceable to the underlying idea they need to learn.”

Likewise, if a PDF app currently uses a page cache, do not mention page caches in Prompt 1 unless the user explicitly made that a requirement.

The purpose is to let the future agent **form an opinion before meeting the current solution**, while still thinking about the correct object.

Blindness does not mean broadening the target.

For a coordination register, Prompt 1 should independently imagine an excellent coordination register — not independently redesign the product being coordinated.

For an investigation, Prompt 1 should independently imagine what a trustworthy investigation must establish — not solve the implementation before evidence is gathered.

For a decision, Prompt 1 should independently imagine what a responsible decision requires — not choose an option prematurely.

---

# PROMPT 1 — IMAGINE

Generate a self-contained prompt that asks the future agent to reason from first principles.

It should begin from:

- the target-purpose sentence;
- the human goal;
- the intended user;
- desired outcomes;
- genuine constraints;
- domain realities.

It should explicitly tell the future agent **not to inspect the current repository or implementation yet** when a current system exists.

Use human language that encourages mental simulation.

Good forms include:

> Imagine the person actually using this.

> Walk through what happens from the moment they begin until they succeed.

> What should the system understand?

> What should feel simple?

> What should remain stable even as examples change?

> What mistakes would look convenient now but become expensive later?

> What would make you trust the result?

Do not force the agent into the vocabulary of the current system.

Do not tell it the current abstractions and then ask whether they are good.

Do not turn Prompt 1 into an audit checklist.

### Prompt 1 must ask for an explicit reference picture

At the end, require the future agent to state something equivalent to:

> “If this were done really well, this is what would become possible…”

and then describe the important principles underneath that experience.

This output becomes the reference point for Prompt 3.

### Product-level emphasis

At product level, Prompt 1 should explore the user journey, major capabilities, architecture, performance/scale, quality, extensibility, and dangerous shortcuts.

### Repository-level emphasis

At repository level, Prompt 1 should imagine the desired end-to-end human outcome of the whole system without inheriting current repository architecture.

### Task-level emphasis

At task level, Prompt 1 should ask what successful completion of **this task's actual role** would make possible, while deliberately ignoring implementation suggestions in historical task text.

Examples:

- implementation task → what becomes possible after the change works;
- investigation task → what can be known confidently;
- decision task → what can be decided responsibly;
- coordination/register task → what can be coordinated safely from one truthful view;
- handover task → what the successor can understand and continue without guesswork.

Do not use the surrounding product mission as a substitute for the task's purpose.

### Prompt-1 object rule

Prompt 1 must be about the frozen **IMAGINATION OBJECT**.

The domain may shape the examples and expertise, but it must not replace the object.

Before finalizing Prompt 1, restate internally:

```text
EXPERTISE:
<who is thinking>

IMAGINATION OBJECT:
<what they are thinking about>
```

If those have accidentally collapsed into the same thing without justification, re-check the target.

---

# STEP 2 — PROMPT 2 MUST RECONSTRUCT REALITY, NOT REDESIGN IT

Prompt 2 may now reveal the current system.

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

Prompt 3 is constrained by the frozen **FINAL OUTPUT CONTRACT**.

It may reason broadly enough to reach a correct conclusion, but its final deliverable must be the kind of artifact required by that contract.

Prompt 3 should make the future agent answer these questions in this order.

## A. What should be preserved?

Before finding faults, identify what is already good enough or better than the first-principles conception.

Do not rebuild sound work because it uses different names.

## B. What has become historical?

Ask:

> What problem used to exist but no longer does?

> Which roadmap item or issue statement describes an older project state?

> What has later work already made obsolete?

This prevents agents from repeatedly solving yesterday's problems.

## C. Is the target still serving the same purpose?

First repeat the target-purpose sentence from the beginning.

Ask:

> Is this still why the target exists?

> Has later work changed the target's meaning without changing its wording?

> Has the target accidentally become a container for neighbouring work?

For registers, plans, audits and handovers, the right outcome may be **reconciliation of truth**, not a product change.

For decision tasks, the right outcome may be **a decision package**, not implementation.

For investigations, the right outcome may be **a conclusion with bounded uncertainty**, not a fix.

Then continue.

## D. What is the real problem now?

Ask:

> Given the independent ideal and today's reality, what meaningful distance still remains?

Also ask:

> Has the original task, roadmap, or product goal changed meaning because the system has evolved?

The agent should explicitly **rediscover the current meaning of the goal**.

## E. What deeper idea is the example exposing?

Do not confuse the thing that revealed a weakness with the weakness itself.

Examples:

```text
river-crossing question
≠ automatically a river-crossing capability

900-page PDF freeze
≠ automatically a 900-page special mode

failed test
≠ automatically the architectural problem

old issue checkbox
≠ automatically current work
```

Ask:

> What reusable problem sits underneath this example?

## F. What is the smallest durable response?

The valid answers depend on the target role and include:

- implement or fix;
- add;
- extend;
- simplify;
- refactor;
- remove;
- reconcile stale state;
- retire obsolete claims;
- gather missing evidence;
- present alternatives for owner decision;
- update the register;
- hand over;
- defer;
- preserve unchanged;
- or **make no change yet**.

Explicitly allow “no change is justified yet.”

Do not manufacture work because a plan was requested.

## G. How will reality test it?

Use real examples both to shape the proposed solution and to verify it.

Ask:

> Does this help more than the single example that exposed the gap?

> Does the idea survive when the context changes?

> Does the real user, learner, document, workflow, or task now behave better?

---

# DIFFERENTIATE THE END OF PROMPT 3 BY PURPOSE AND ZOOM LEVEL

## PRODUCT LEVEL

End with:

- what should be preserved;
- major gaps;
- architectural or product corrections;
- what should deliberately not be built;
- phased path to the intended product;
- evidence that each phase improves the real user experience.

## REPOSITORY / SYSTEM LEVEL

End with:

- what the system has actually become;
- what should remain;
- what old assumptions are obsolete;
- what genuinely blocks the desired human outcome;
- what “complete enough for this stage” should mean now;
- what should happen next;
- what should wait;
- phased programme based on real dependencies and value.

## TASK / ISSUE LEVEL — IMPLEMENTATION / CHANGE

End with a rewritten task statement:

> “Given the current repository, the meaningful remaining work is…”

Then identify:

- what has already been solved;
- the exact remaining problem;
- the smallest durable change;
- what should deliberately remain untouched;
- how real evidence will verify it;
- what should make the next agent reconsider the conclusion.

The rewritten task may be much smaller than the original issue. That is often the correct result.

## TASK / ISSUE LEVEL — INVESTIGATION / AUDIT

End with:

- what question the investigation needed to settle;
- what evidence is authoritative;
- what was reproduced or verified;
- what explanation best fits the evidence;
- what remains uncertain;
- whether a change is justified;
- what evidence would overturn the conclusion.

Do not invent an implementation task merely because the investigation found something interesting.

## TASK / ISSUE LEVEL — DECISION

End with:

- the exact decision;
- who owns it;
- the viable options;
- evidence for and against each;
- consequences and reversibility;
- uncertainty;
- what work each option gates;
- what can proceed without the decision.

Do not make the owner-reserved choice on the owner's behalf unless explicitly authorized.

## TASK / ISSUE LEVEL — COORDINATION / REGISTER

End with a reconciled current picture:

- what is true now;
- what has merged;
- what is still in flight;
- what is stale or superseded;
- merge/dependency order where relevant;
- technical blockers;
- owner-gated decisions;
- work that can proceed without those decisions;
- the exact current executable frontier;
- conditions that would make the register stale again.

The output should improve programme truth and continuity, not redesign the whole product.

## TASK / ISSUE LEVEL — HANDOVER / CONTINUITY

End with:

- why the work exists;
- current authoritative state;
- what is complete;
- what is unresolved;
- current risks and decisions;
- source evidence;
- first safe next action;
- stop conditions;
- what would make the handover stale.

The successor should be able to continue without needing the previous conversation.

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

TARGET NATIVE DELIVERABLE:
REQUEST MODE:
TARGET PURPOSE:
TARGET SCOPE:
EXPERTISE:

IMAGINATION OBJECT:
REALITY OBJECT:
FINAL OUTPUT CONTRACT:

PROMPT-1 OBJECT GATE:
PASS — <one short reason>

PROMPT-3 OUTPUT GATE:
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

PURPOSE:
<this target exists so that ...>
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

Do not show these checks. Use them internally.

### Visible-preflight check

Is the complete PREFLIGHT RECORD visible in the final generator output?

If it is hidden, summarized as "completed", or omitted, fail.

### Copy-pasteability check

Are Prompt 1, Prompt 2, and Prompt 3 each enclosed in their own clean outer text fence and directly pasteable without editing?

If there is commentary mixed into a prompt, unresolved known placeholders, nested fences, or notes after Prompt 3, fail.

### Native-deliverable check

Does TARGET NATIVE DELIVERABLE describe the kind of thing this target itself is supposed to leave behind?

Does FINAL OUTPUT CONTRACT preserve that artifact form rather than mechanically mapping REQUEST MODE to a generic deliverable?

If not, fail.

### Purpose-proximity check

Could TARGET PURPOSE be pasted unchanged onto the parent system or several sibling issues?

If yes, it is probably too broad. Rewrite it closer to this target.

### Preflight-completeness check

Are TARGET NATIVE DELIVERABLE, REQUEST MODE, TARGET PURPOSE, TARGET SCOPE, EXPERTISE, IMAGINATION OBJECT, REALITY OBJECT, and FINAL OUTPUT CONTRACT all resolved?

If not, do not generate prompts.

### Prompt-1 object-gate check

Would a perfect answer to Prompt 1 be an excellent example of the frozen IMAGINATION OBJECT?

If not, reject Prompt 1.

### Prompt-3 output-gate check

Would a perfect answer to Prompt 3 produce the frozen FINAL OUTPUT CONTRACT?

If not, reject Prompt 3.

### Expertise/object separation check

Did domain expertise accidentally become the object of Prompt 1?

If yes, re-check the target purpose.

### Target-purpose check

Can you complete:

> “This target exists so that …”

in a way that describes the target itself rather than the surrounding product mission?

If not, stop and re-identify the target purpose.

### Neighbouring-problem / zoom-leak check

If Prompt 1 were answered perfectly, would it satisfy this target, or would it solve a larger neighbouring problem?

If it solves the larger problem, narrow Prompt 1.

### Independence check

Could Prompt 1 have been written without knowing the current implementation?

If not, remove leaked implementation vocabulary.

### Human-intent check

Does Prompt 1 describe what a person should be able to achieve rather than what files or abstractions should exist?

### Reality check

Does Prompt 2 force inspection of current evidence rather than trusting old issue or roadmap language?

### In-flight-work check

Does Prompt 2 account for relevant current PRs/work without pretending they are already merged?

### Prompt-2/3 identity check

Does Prompt 2 include the canonical target URL and repository/system URL when live inspection is possible?

Does Prompt 3 independently name the target and include the canonical target URL and repository/system URL when available?

If a task/issue has both links available and Prompt 2 or Prompt 3 omits them, revise it.

Do not fail Prompt 1 merely because it omits live links to preserve the independence barrier.

### Goalpost check

Does Prompt 3 explicitly return to the exact Prompt-1 conception?

### Rediscovery check

Does Prompt 3 ask what the goal means **now**, rather than merely counting missing old checklist items?

### Example-vs-problem check

Does Prompt 3 force the agent to distinguish the example that exposed a weakness from the reusable problem underneath it?

### Restraint check

Can Prompt 3 validly conclude “no change,” “defer,” or “leave this alone”?

### Evidence check

Does Prompt 3 return to real examples to test the conclusion?

### Role-fit check

Does Prompt 3 produce the right kind of outcome for the target role?

- implementation → bounded change;
- investigation → trustworthy conclusion;
- decision → decision-ready evidence;
- coordination/register → reconciled current truth and frontier;
- handover → successor continuity.

If a coordination target ends in a product redesign, or an investigation ends in unrequested implementation, revise it.

### Handover-reasoning check

Does Prompt 3 hand over the reasoning journey:

destination → reality → real gap → chosen move → deliberately not done → real evidence/example → unresolved → where next → what changes our mind?

If the handover is mainly branch/commit/PR topology or a task checklist, fail.

Operational details may supplement the reasoning relay, never replace it.

If any check fails, revise the three prompts before output.

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

# APPENDIX D — CASE STUDY: TASK LEVEL, COORDINATION / REGISTER

## Input example

```text
TARGET:
https://github.com/reallaksh19/Advanced_Analysis/issues/1855

CURRENT SYSTEM:
https://github.com/reallaksh19/Advanced_Analysis

HUMAN GOAL:
Keep one truthful, current picture of merge order, outstanding engineering work, blockers,
owner-gated decisions, known baseline failures, and the exact work that can safely proceed.
```

## Frozen preflight

```text
TARGET NATIVE DELIVERABLE:
live engineering coordination register

REQUEST MODE:
TARGET TITLE:
[LAFEA REGISTER] Pending activity — merge queue, open work, and the decisions that gate it
TARGET LINK:
https://github.com/reallaksh19/Advanced_Analysis/issues/1855
PARENT REPOSITORY / SYSTEM:
reallaksh19/Advanced_Analysis
REPOSITORY / SYSTEM LINK:
https://github.com/reallaksh19/Advanced_Analysis


COORDINATE

TARGET PURPOSE:
This issue exists so that the owner and replacement engineer have one verified current
view of outstanding work, merge/dependency order, blockers, owner-gated decisions,
corrections and safe next work.

TARGET SCOPE:
TASK_ARTIFACT

EXPERTISE:
senior structural / finite-element engineering plus engineering-programme judgement

IMAGINATION OBJECT:
an excellent live engineering programme register

REALITY OBJECT:
whether every important claim in Issue #1855 still agrees with the live repository,
PRs, tests, workflows, issues and owner decisions

FINAL OUTPUT CONTRACT:
a reconciled live register containing current truth, merge/dependency order,
technical blockers, owner decisions, work that can proceed, the executable frontier,
and conditions that make the register stale
```

**Gate expectation:** a perfect Prompt-1 answer describes the register, not the shell-FEA product. Any product-design Prompt 1 FAILS.

## Wrong interpretation

A weak generator sees deep finite-element or solver details inside the issue and produces Prompt 1 like:

> Imagine the ideal shell finite-element product. What solver, element formulation, qualification evidence and UI should it have?

That is a **neighbouring product problem**.

Even if answered brilliantly, it does not fulfil the purpose of the register.

## Correct target-purpose sentence

> This issue exists so that the owner and the next engineer have one verified, current view of what is done, what is not done, what is blocked, what can merge, what decisions are reserved to the owner, and what can safely happen next.

That sentence should control all three prompts.

## What a good generated Prompt 1 should feel like

It should remain blind to the actual PR numbers and current failures, but think deeply about an excellent engineering register:

> Imagine you are taking over a complex engineering programme with stacked changes, known failures, unresolved technical questions and owner-gated decisions. What would one trustworthy live register need to show so you could tell what is actually true, what can safely merge, what is blocked technically versus waiting on a decision, what claims have become stale, and what the first safe next action is? How should corrections remain visible without confusing current state? What evidence should support each important claim? What should make an entry stale?

It should **not** redesign the engineering product itself.

## What a good generated Prompt 2 should feel like

It should now inspect the live issue and repository and verify the register claim-by-claim:

```text
register claim
→ live PR / branch / issue / test / workflow / evidence / owner decision
→ current truth
```

It should reconstruct:

- actual trunk health;
- which failures are pre-existing;
- which PRs are stacked and in what dependency order;
- which PRs are genuinely ready;
- what has merged since the register was written;
- which engineering items remain;
- which decisions truly require the owner;
- what work can continue without those decisions;
- which statements in the register are stale or contradicted by current evidence.

It should distinguish current baseline from near-future baseline without crediting unmerged work as already true.

## What a good generated Prompt 3 should feel like

It should return to the independent picture of a trustworthy engineering register and ask:

> Does this issue currently provide that truthful view?

Then it should reconcile, not redesign:

- preserve still-correct entries;
- retire or rewrite stale entries;
- update merge/dependency order;
- separate technical blockers from owner decisions;
- expose the exact executable frontier;
- state what is safe to carry now;
- state what must wait;
- state what new event would make the register stale.

Its final result should be:

> a better current register and handover surface,

not:

> a new architecture for the engineering product.

This is the canonical example of why **request mode + target purpose must be frozen before target scope**, and why **expertise must not be confused with the imagination object**.


---

# FOUR-CASE REGRESSION VALIDATION

Before considering a future schema revision safe, mentally run these four controls:

| Case | Native deliverable | Request mode | Scope | Imagination object | Final output contract | Expected |
| --- | --- | --- | --- | --- | --- | --- |
| Static browser PDF editor | working product / product direction | REVIEW | PRODUCT | excellent browser PDF editor | product gap analysis + phased roadmap | PASS |
| Overall Grade9V3 | revalidated system/programme direction | REVIEW | REPOSITORY_SYSTEM | excellent Grade-9 self-study system | current meaning of Grade 9 + programme | PASS |
| Grade9V3 Issue #19 | bounded content/mapping change | CHANGE | TASK_ARTIFACT | excellent question-to-learning mapping | rewritten current task + smallest durable change | PASS |
| Advanced_Analysis Issue #1855 | live coordination register | COORDINATE | TASK_ARTIFACT | excellent live engineering register | reconciled register + executable frontier | PASS |
| Advanced_Analysis Issue #1756 | architecture + qualification/closure umbrella | REVIEW/COORDINATE | REPOSITORY_SYSTEM | excellent methodical shell qualification programme | revalidated qualification/closure roadmap | PASS |

The fourth case is the negative control for scope drift:

```text
finite-element expertise
≠
permission to make Prompt 1 about designing the finite-element product
```

If the generator produces a shell-FEA product-conception prompt for Issue #1855, the schema has regressed.

### Gate-by-gate expected result

```text
CASE A — PDF EDITOR
Prompt-1 object gate: PASS
Prompt-3 output gate: PASS
Neighbouring-problem risk: low because target itself is the product

CASE B — OVERALL GRADE9V3
Prompt-1 object gate: PASS only if current Grade9V3 vocabulary stays out
Prompt-3 output gate: PASS only if result is repository/programme level
Neighbouring-problem risk: medium — do not collapse into one issue or one subject slice

CASE C — GRADE9V3 ISSUE #19
Prompt-1 object gate: PASS only if it stays on question→learning mapping
Prompt-3 output gate: PASS only if it rewrites today's remaining task
Neighbouring-problem risk: high — do not broaden into overall Grade 9

CASE D — ADVANCED_ANALYSIS ISSUE #1855
Prompt-1 object gate: PASS only if it imagines an excellent live engineering register
Prompt-3 output gate: PASS only if it yields reconciled truth + executable frontier
Neighbouring-problem risk: critical — finite-element expertise must not broaden the object into product design
```

---

# OUTPUT REGRESSION REQUIREMENTS

Every case study and every generated result must also pass these non-reasoning checks:

```text
VISIBLE PREFLIGHT RECORD
must be present

PROMPT 1
one clean copy-pasteable text block

PROMPT 2
one clean copy-pasteable text block

PROMPT 3
one clean copy-pasteable text block

NO EXTRA NOTES
after Prompt 3

HANDOVER
must transmit understanding, not merely operations
```

A result with excellent reasoning but missing the visible preflight, broken copy-pasteability, or an activity-log handover is a schema failure.

---

# FINAL PRINCIPLE

The generator should make a future agent think in this order:

```text
What are we really trying to achieve?

Before seeing the existing answer,
what would a strong answer look like?

What is actually true today?

Given everything that has happened,
what does the goal mean now?

What meaningful distance still remains?

What is the smallest worthwhile change?

Does reality confirm that it helped?

What must the next person understand?
```

The method is constant.

The **target native deliverable** preserves what kind of thing the target itself is meant to leave behind.

The **request mode** determines what operation the user wants now.

The **target purpose** determines why the target itself exists.

The **target scope** determines how much surrounding system belongs inside the problem.

The **expertise** determines how intelligently the agent reasons.

The **imagination object** prevents Prompt 1 from drifting.

The **reality object** keeps Prompt 2 bounded.

The **final output contract** prevents Prompt 3 from turning into the wrong kind of deliverable.

The **reasoning handover** preserves the journey from destination to reality to meaningful remaining distance, so the next agent inherits understanding rather than an activity log.
