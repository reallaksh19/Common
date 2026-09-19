# Three-Pass Prompt Generator Schema

> Human-executable prompt schema for generating three sequential, copy-pasteable prompts.
>
> This is intentionally a Markdown schema rather than a JSON Schema. Its job is to make an ordinary agent reliably produce the same reasoning pattern across different **target purposes** and **zoom levels** without drifting into a larger neighbouring problem.

## Purpose

When given a target, create **exactly three prompts** for another agent to run in sequence:

1. **IMAGINE** — form an independent picture of what good should look like before seeing the existing answer.
2. **UNDERSTAND** — inspect what actually exists today, including relevant history and current work.
3. **REVALIDATE AND MOVE FORWARD** — return to the exact independent picture, compare it with reality, rediscover what the goal means now, and identify the smallest meaningful path forward.

Do not solve the target yourself. Your output is the three prompts.

The method is the same throughout, but two things must be identified correctly before generating prompts:

1. **Target purpose** — why this target exists at all.
2. **Zoom level** — how much of the surrounding system the target is responsible for.

A task can mention an entire product without being a product-level task. A register about a solver programme is not the same thing as the solver programme itself.

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

# STEP 0A — FIRST IDENTIFY WHY THE TARGET EXISTS

Do this **before** choosing the zoom level.

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

### Common target roles

Choose the dominant role. More than one may apply, but one should control Prompt 1.

#### IMPLEMENTATION / CHANGE

The target exists to make, fix, add, remove or alter something.

Prompt 1 should imagine what successful completion of **that change** makes possible.

#### INVESTIGATION / AUDIT

The target exists to establish what is true, why something happened, or whether a claim holds.

Prompt 1 should imagine what a trustworthy investigation would let a human know or decide.

#### DECISION / OWNER-GATED CHOICE

The target exists to support a bounded choice that someone with authority must make.

Prompt 1 should imagine what evidence, alternatives, consequences and uncertainty a responsible decision-maker would need.

Do not turn the decision task into implementing one option before the decision exists.

#### COORDINATION / REGISTER / PROGRAMME CONTROL

The target exists to keep current truth about multiple pieces of work: status, dependencies, merge order, blockers, decisions, stale claims and executable next work.

Prompt 1 should imagine what an excellent live register would let an owner or replacement engineer understand and do safely.

Do **not** broaden Prompt 1 into redesigning the product whose work is being coordinated.

#### HANDOVER / CONTINUITY

The target exists so another person or agent can continue correctly without reconstructing the programme from scratch.

Prompt 1 should imagine what the successor must understand, what evidence they must trust, what uncertainty must remain visible, and what the first safe action should be.

#### PRODUCT / SYSTEM CONCEPTION

The target genuinely exists to define or rethink the product/system itself.

Only here should Prompt 1 directly ask what the overall product or system should become.

### Target-purpose anchor

Carry the completed sentence:

> “This target exists so that …”

through all three prompts.

Prompt 1 imagines that purpose done well.

Prompt 2 asks whether today's reality serves that purpose.

Prompt 3 asks what meaningful distance remains **for that same purpose**.

Do not silently substitute the mission of a neighbouring product, repository, programme or issue.

---

# STEP 0B — SILENTLY DETERMINE THE ZOOM LEVEL

After identifying the target's purpose, silently decide which zoom level best describes how much of the surrounding system the target is responsible for.

**Purpose comes first. Zoom comes second.**

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
- target-purpose sentence: "This target exists so that ..."
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

---

# STEP 2 — PROMPT 2 MUST RECONSTRUCT REALITY, NOT REDESIGN IT

Prompt 2 may now reveal the current system.

Tell the future agent to inspect the live implementation and understand it on its own terms before proposing changes.

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

# HANDOVER REQUIREMENT

Prompt 3 must end with a handover section.

The next agent should learn:

- what we were trying to achieve;
- what was already good;
- what reality taught us;
- why the chosen work matters;
- what was deliberately left alone;
- what real evidence supported the decision;
- what remains unresolved;
- what should make the next agent change course.

Use this principle:

> Do not merely hand over what you changed.

> Hand over what you understood.

---

# STRICT OUTPUT CONTRACT FOR THE GENERATOR

Before answering me, silently check your work against the quality checks below.

Then output **exactly three major copy-pasteable blocks** and no analysis of the target.

Use these headings exactly:

```text
# PROMPT 1 — IMAGINE

# PROMPT 2 — UNDERSTAND

# PROMPT 3 — REVALIDATE AND MOVE FORWARD
```

Each block must:

- stand on its own;
- clearly identify the target;
- include the canonical target link when one exists;
- include the repository/system link when the target is a task, issue, PR, audit, register, or handover inside a repository;
- be ready to paste directly into another agent;
- contain enough context for its own purpose;
- preserve the independence barrier;
- use human language;
- be adapted to the selected zoom level.

Do not add a fourth prompt.

Do not solve the target.

Do not output your private classification work.

Do not add a roadmap outside Prompt 3.

Do not add explanatory prose before or after the three blocks.

---

# SILENT QUALITY CHECKS BEFORE OUTPUT

Do not show these checks. Use them internally.

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

### Prompt-3 identity check

Does Prompt 3 independently name the target and include the canonical target URL and repository/system URL when available?

If a task/issue prompt lacks either link even though both were supplied, revise it.

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

### Handover check

Will a replacement agent understand the reasoning, not only the files changed?

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
A GitHub issue whose purpose is to be the single register of pending work for a complex engineering programme.

HUMAN GOAL:
Keep one truthful, current picture of merge order, outstanding engineering work, blockers,
owner-gated decisions, known baseline failures, and the exact work that can safely proceed.

CURRENT SYSTEM:
A live engineering repository with stacked PRs, red baseline checks, several programme phases,
and decisions reserved to the owner.
```

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

This is the canonical example of why **target purpose must be identified before zoom level**.


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

The **target purpose** determines what kind of problem the prompts are solving.

The **zoom level** determines how much surrounding system belongs inside that problem.
