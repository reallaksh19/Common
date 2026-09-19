# Three-Pass Prompt Generator Schema

> Human-executable prompt schema for generating three sequential, copy-pasteable prompts.
>
> This is intentionally a Markdown schema rather than a JSON Schema. Its job is to make an ordinary agent reliably produce the same reasoning pattern at three different zoom levels: product, repository/system, and task/issue.

## Purpose

When given a target, create **exactly three prompts** for another agent to run in sequence:

1. **IMAGINE** — form an independent picture of what good should look like before seeing the existing answer.
2. **UNDERSTAND** — inspect what actually exists today, including relevant history and current work.
3. **REVALIDATE AND MOVE FORWARD** — return to the exact independent picture, compare it with reality, rediscover what the goal means now, and identify the smallest meaningful path forward.

Do not solve the target yourself. Your output is the three prompts.

The method is the same at every scale. Only the zoom level changes.

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

# STEP 0 — SILENTLY DETERMINE THE ZOOM LEVEL

Before writing the three prompts, silently decide which of these best describes the target.

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

Do not create three different methodologies. Use the same three-pass method with different zoom.

---

# STEP 1 — BUILD A BLIND BRIEF FOR PROMPT 1

This is the most important safeguard.

Before generating Prompt 1, silently separate the user's information into two conceptual buckets:

```text
BLIND BRIEF
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

The purpose is to let the future agent **form an opinion before meeting the current solution**.

---

# PROMPT 1 — IMAGINE

Generate a self-contained prompt that asks the future agent to reason from first principles.

It should begin from:

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

At task level, Prompt 1 should ask what successful completion would make possible, while deliberately ignoring implementation suggestions in the historical task text.

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

Tell it to follow **real journeys**, not merely list folders.

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

Prompt 3 must explicitly tell the future agent to return to the **actual answer it produced for Prompt 1**.

Do not let it quietly rewrite the ideal after seeing the repository.

Tell it:

> Take the independent picture you produced in Prompt 1.

> Put it beside the reality you discovered in Prompt 2.

> Where evidence from reality genuinely changed your mind, explain exactly why.

> Otherwise keep the original independent baseline.

This is the anti-goalpost-moving rule.

If the three prompts are likely to be run in separate conversations, Prompt 3 should instruct the user to paste or attach the outputs of Prompt 1 and Prompt 2 before running it. If they are expected to run in one continuous conversation, simply tell the agent to use its prior two outputs.

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

## C. What is the real problem now?

Ask:

> Given the independent ideal and today's reality, what meaningful distance still remains?

Also ask:

> Has the original task, roadmap, or product goal changed meaning because the system has evolved?

The agent should explicitly **rediscover the current meaning of the goal**.

## D. What deeper idea is the example exposing?

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

## E. What is the smallest durable change?

The valid answers include:

- add;
- extend;
- simplify;
- refactor;
- remove;
- defer;
- preserve unchanged;
- or **make no change yet**.

Explicitly allow “no change is justified yet.”

Do not manufacture work because a plan was requested.

## F. How will reality test it?

Use real examples both to shape the proposed solution and to verify it.

Ask:

> Does this help more than the single example that exposed the gap?

> Does the idea survive when the context changes?

> Does the real user, learner, document, workflow, or task now behave better?

---

# DIFFERENTIATE THE END OF PROMPT 3 BY ZOOM LEVEL

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

## TASK / ISSUE LEVEL

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

### Independence check

Could Prompt 1 have been written without knowing the current implementation?

If not, remove leaked implementation vocabulary.

### Human-intent check

Does Prompt 1 describe what a person should be able to achieve rather than what files or abstractions should exist?

### Reality check

Does Prompt 2 force inspection of current evidence rather than trusting old issue or roadmap language?

### In-flight-work check

Does Prompt 2 account for relevant current PRs/work without pretending they are already merged?

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

Only the zoom level changes.
