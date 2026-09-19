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

If the user asks for **multiple lots**, preserve the number of lots and the requested analysis level of each lot exactly.

Do not replace a user-requested tab/surface review with a related issue, decision, roadmap, or repository review merely because that artifact appears important.

Each lot gets its own preflight and its own three prompts.

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

For ISSUE_TASK, Prompt 1 must preserve the issue's **PROBLEM KERNEL**: the smallest set of stable facts without which it would no longer be the same issue.

That kernel may include named domain entities, a source/method boundary, the affected user/job, the particular authority or applicability tension, and the lifecycle stage if those facts define the issue.

It must not include the issue's current proposed options, implementation recipe, present evidence interpretation, current work breakdown, or chosen artifact form merely because those appear in the issue body.

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
EMP.1 / WRC 537 tab
practising pressure-equipment engineer
real vessel / attachment geometry and loads
need a defensible local-stress assessment
must understand applicability and refusal
must distinguish numerical evidence from engineering authority

Not blind-pass anchors:
today's gamma=5 implementation limit
current hidden disclosures
current radii dead end
specific issue numbers
current CI outage
```

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
- current benchmark numbers unless the number itself defines the problem;
- current proposed implementation;
- current PR/branch sequence;
- current bug inventory;
- current acceptance checklist;
- present evidence conclusions that Prompt 2 is supposed to verify.

### Example — issue-level engineering decision

Too generic:

```text
How should a responsible organisation decide whether to extend a standard beyond its tabulated range?
```

Still contaminated:

```text
Should we choose Option 1, Option 2 or Option 3 given CAUx agreement and the current conservatism study?
```

Correct corridor:

```text
PROBLEM KERNEL:
- EMP.1 is a WRC 537 local-attachment assessment capability.
- The professionally usable route is tied to a tabulated gamma condition.
- Real vessel geometries commonly require non-tabulated gamma values.
- WRC 537 does not itself provide the missing non-tabulated-gamma rule.
- Extending professional-use authority therefore requires an explicit engineering basis;
  numerical plausibility alone cannot silently create source/method authority.
```

This is specific enough to identify the issue, but it does not reveal today's option list,
benchmark conclusion, chosen interpolation coordinate, sample statistics, or recommendation.

Complete:

```text
TARGET ANCHORS:
<stable, level-specific facts that make this unmistakably THIS target without leaking today's answer>

PROBLEM KERNEL:
<for ISSUE_TASK: 3–7 minimal identity-bearing facts that must survive blindness;
for other levels: optional if useful>

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

BLIND REFERENCE — THE ONLY SIDE ALLOWED TO SHAPE PROMPT 1
TARGET ANCHORS:
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

COMPLEX Q1–Q5 COVERAGE:
PASS — <one short reason, or N/A when COMPLEX MODE = OFF>

SPECIFICITY-FLOOR GATE:
PASS — <one short reason>

SAME-ISSUE IDENTITY GATE:
PASS — <one short reason>

ANSWER-RECONSTRUCTION GATE:
PASS — <one short reason>

LOT/LEVEL BOUNDARY GATE:
PASS — <one short reason>

PROMPT-3 FREEDOM GATE:
PASS — <one short reason>
```

Do not draft Prompt 1 until these fields and gates are resolved.

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

# HARD GATE 0.9 — ANSWER-RECONSTRUCTION GATE

For ISSUE_TASK, ask the opposite question:

> **From Prompt 1 alone, could a domain-aware person reconstruct today's proposed answer, option set, current evidence conclusion, implementation recipe, or backlog sequence?**

If yes, Prompt 1 is contaminated.

Examples of leakage:

```text
Option 1 / Option 2 / Option 3
LINEAR_GAMMA vs LOG_GAMMA
current CAUx percentage
current n=57 study
current exact PR order
current matrix/rung names
current proposed file/schema changes
```

Prompt 1 should expose the **question worth answering**, not the repository's current answer to it.

---

# HARD GATE 0.95 — ISSUE GOLDILOCKS CORRIDOR

An issue-level Prompt 1 passes only if **both** are true:

```text
RECOGNISABLE:
The underlying issue is identifiable from its problem kernel.

NOT PRE-SOLVED:
The current answer/options/evidence interpretation cannot be reconstructed.
```

Think of the allowed information band as:

```text
too generic
    ↓
[ problem kernel + domain truth + human outcome ]
    ↑
too contaminated
```

The generator's job is to stay inside that band.

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

Likewise, replacing proper nouns with generic nouns is not enough:

```text
WRC 537        → "a published standard"
gamma          → "a parameter"
CAUx           → "third-party software"
EMP.1          → "a software implementation"
```

If the narrative structure and current evidence story are preserved, the answer has merely been **laundered into generic language**.

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
USER-REQUESTED LEVEL
TARGET TITLE / SURFACE when it is itself part of the requested human problem
TARGET ANCHORS
PROBLEM KERNEL
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

### Blind does not mean generic

Prompt 1 should be concrete enough that the user can immediately tell whether it is:

- issue-level;
- tab/surface-level;
- product-level;
- or repository/system-level.

For TAB_SURFACE, normally walk a real user through the surface from arrival/input to result/refusal/review.

For ISSUE_TASK, stay on the specific underlying issue problem and its lifecycle stage; do not drift to the whole tab.

Use TARGET ANCHORS aggressively enough to make the scenario vivid, while keeping current-answer facts quarantined.

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

Issue-level Prompt 1 should be **closer to the issue than to the parent programme**, while still preceding today's answer.

Construct it in this order:

```text
1. Name the real domain/person affected.
2. State the PROBLEM KERNEL concretely.
3. Put that person into a realistic situation where the issue matters.
4. Ask first-principles questions that could lead to multiple legitimate answers.
5. Ask what evidence/principles would justify action.
6. End with the independent reference picture.
```

Do not begin by asking for the current artifact:

```text
bad:  "Imagine an excellent decision package."
bad:  "Imagine an excellent register."
bad:  "Imagine an excellent matrix."
```

Instead ask about the actual unresolved problem:

```text
better:
"EMP.1 uses WRC 537 for local-attachment assessment. Its professionally usable
method basis is tied to tabulated gamma conditions, while real vessel geometry
often lies between those conditions and the source itself does not provide the
missing rule. Before looking at how this repository has tried to resolve that,
what would have to be true before an engineering organisation could responsibly
let the product serve those non-tabulated cases?"
```

That is issue-specific without revealing today's options or evidence conclusion.

Do **not** assume the current issue's proposed artifact or work breakdown is the correct instrument.

Run the SAME-ISSUE IDENTITY, ANSWER-RECONSTRUCTION, ARTIFACT-ERASURE,
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

For **each requested lot**, the generator output has four visible sections:

1. one **PREFLIGHT RECORD**;
2. exactly three **copy-pasteable prompt blocks**.

The preflight is metadata, **not a fourth prompt**.

If the user requested two lots, output two lot sections. Do not merge them and do not invent a different second target.

Output this structure and nothing else:

````markdown
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

CURRENT REALITY — QUARANTINED FROM PROMPT 1
CURRENT ARTIFACT FORM:
CURRENT STATED ANSWER / IMPLEMENTATION:
CURRENT-STATE FACTS:

BLIND REFERENCE — THE ONLY SIDE ALLOWED TO SHAPE PROMPT 1
TARGET ANCHORS:
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

SPECIFICITY-FLOOR GATE:
PASS — <one short reason>

SAME-ISSUE IDENTITY GATE:
PASS — <one short reason, or N/A outside ISSUE_TASK>

ANSWER-RECONSTRUCTION GATE:
PASS — <one short reason, or N/A outside ISSUE_TASK>

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

Keep it blind to today's answer. Use TARGET ANCHORS, PROBLEM KERNEL where applicable, human outcome, genuine constraints, domain, and imagination object.

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

### Lot-count / level-fidelity check

Does the output contain exactly the number of lots the user requested?

Does each lot preserve the requested level exactly?

If a tab-level lot became an issue-level lot, fail.

### Specificity-floor check

Is Prompt 1 recognisably about this exact requested target and level?

Could it be pasted unchanged into many unrelated projects?

If yes, fail as too generic.

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

### Same-issue identity check

For ISSUE_TASK, after removing the title/number, is the particular issue still distinguishable from sibling issues?

If not, restore the PROBLEM KERNEL.

### Answer-reconstruction check

For ISSUE_TASK, can Prompt 1 reveal today's option set, evidence conclusion, implementation recipe or sequence?

If yes, remove those answer-side facts.

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
TARGET TITLE:
Static browser-based PDF editor

TARGET LINK:
not supplied

PARENT REPOSITORY / SYSTEM:
not supplied

REPOSITORY / SYSTEM LINK:
not supplied

REQUEST MODE:
REVIEW


CURRENT REALITY — QUARANTINED FROM PROMPT 1

CURRENT ARTIFACT FORM:
existing browser PDF editor/product implementation

CURRENT STATED ANSWER / IMPLEMENTATION:
not supplied in the blind brief; inspect the real application/repository only in Prompt 2

CURRENT-STATE FACTS:
an existing implementation is being reviewed, but its architecture and abstractions
must not shape Prompt 1

BLIND REFERENCE — THE ONLY SIDE ALLOWED TO SHAPE PROMPT 1

UNDERLYING HUMAN PROBLEM:
Users need to seriously edit, inspect and save real PDFs in a browser-oriented environment
without having to operate backend infrastructure.

HUMAN OUTCOME:
A personal or professional user can open a real PDF, understand it, modify it confidently,
work with large documents, save it and reopen it without the tool becoming fragile or misleading.

GENUINE CONSTRAINTS:
primarily client-side/static; phone and desktop; one developer with AI assistance;
real PDF semantics and large-document behaviour matter

EXPERTISE:
PDF/browser architecture and document-editing product expertise

IMAGINATION OBJECT:
an excellent static/browser PDF editing experience and the principles needed to sustain it

PROMPT 2

REALITY OBJECT:
the current PDF application's real user journeys, architecture, performance, persistence,
supported operations, tests and in-flight work

PROMPT 3

COMPARISON QUESTION:
what meaningful distance remains between the independent PDF-editor picture and today's
application, and what is the smallest sensible phased path from here?

HANDOVER DESTINATION:
the next agent should understand the intended user experience, what reality taught us,
the real remaining gaps, what should not be built, and what evidence should change direction

ARTIFACT-ERASURE GATE:
PASS — the Prompt-1 picture survives removal of the current implementation

CURRENT-VOCABULARY GATE:
PASS — no current library, cache, schema or architecture name is required

PROMPT-1 OBJECT GATE:
PASS — the answer independently defines the PDF experience being sought

PROMPT-3 FREEDOM GATE:
PASS — current architecture may be preserved, changed, simplified or replaced
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

## Frozen preflight

```text
TARGET TITLE:
Grade9V3 repository

TARGET LINK:
https://github.com/reallaksh19/Grade9V3

PARENT REPOSITORY / SYSTEM:
reallaksh19/Grade9V3

REPOSITORY / SYSTEM LINK:
https://github.com/reallaksh19/Grade9V3

REQUEST MODE:
REVIEW


CURRENT REALITY — QUARANTINED FROM PROMPT 1

CURRENT ARTIFACT FORM:
existing self-study repository/system

CURRENT STATED ANSWER / IMPLEMENTATION:
the repository already has its own products, routing, schemas, matrices, gates,
subject boundaries and programme history; all of that belongs to Prompt 2

CURRENT-STATE FACTS:
the current system is a living implementation with recent work and subject-specific progress

BLIND REFERENCE — THE ONLY SIDE ALLOWED TO SHAPE PROMPT 1

UNDERLYING HUMAN PROBLEM:
A Grade-9 learner studying mostly alone needs to understand new ideas, practise them,
recover from misunderstanding or missing prerequisites, and eventually handle unfamiliar work.

HUMAN OUTCOME:
The learner can move from first exposure to independent application with useful diagnosis
and repair when they get stuck.

GENUINE CONSTRAINTS:
multiple subjects; one developer with agents; maintainability across topics matters;
machine checks are not proof that material actually teaches

EXPERTISE:
learning-system, curriculum and educational-product architecture expertise

IMAGINATION OBJECT:
an excellent Grade-9 self-study learner journey and system

PROMPT 2

REALITY OBJECT:
what Grade9V3 actually provides today across teaching, practice, routing, feedback,
subjects, evidence, repository architecture and current work

PROMPT 3

COMPARISON QUESTION:
what should Grade 9 mean now, what is already solved, what genuinely remains,
and what programme makes sense from today's reality?

HANDOVER DESTINATION:
the next agent should understand the learner destination, what the repository has become,
the real remaining distance, deliberate boundaries and evidence needed to change direction

ARTIFACT-ERASURE GATE:
PASS — Prompt 1 still works if all current Core/matrix/gate architecture disappears

CURRENT-VOCABULARY GATE:
PASS — current Grade9V3 vocabulary is withheld from Prompt 1

PROMPT-1 OBJECT GATE:
PASS — the answer defines the learner/system outcome independently

PROMPT-3 FREEDOM GATE:
PASS — current architecture and programme priorities may be preserved or changed
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

## Frozen preflight

```text
LOT:
single lot

USER-REQUESTED LEVEL:
ISSUE_TASK

USER-REQUESTED TARGET:
Grade9V3 Issue #19

LEVEL INTERPRETATION:
stay on the question-to-learning mapping problem owned by this issue;
do not broaden to overall Grade9V3

TARGET TITLE / SURFACE:
Complete Physics/Math matrices and capability mappings for worksheet-driven study routing

TARGET LINK:
https://github.com/reallaksh19/Grade9V3/issues/19

PARENT REPOSITORY / SYSTEM:
reallaksh19/Grade9V3

REPOSITORY / SYSTEM LINK:
https://github.com/reallaksh19/Grade9V3

REQUEST MODE:
CHANGE

CURRENT REALITY — QUARANTINED FROM PROMPT 1

CURRENT ARTIFACT FORM:
GitHub implementation/content-mapping issue

CURRENT STATED ANSWER / IMPLEMENTATION:
the issue is expressed through matrices, capabilities, prerequisite closure,
rungs/microtopics and a historical implementation checklist

CURRENT-STATE FACTS:
later repository work may already have satisfied or changed parts of the issue

BLIND REFERENCE — THE ONLY SIDE ALLOWED TO SHAPE PROMPT 1

TARGET ANCHORS:
real Physics/Mathematics worksheet questions;
self-study learner who gets stuck;
reusable learner ability;
genuine prerequisite;
where the idea is taught

PROBLEM KERNEL:
- a real worksheet question should resolve to the reusable learner action it requires;
- supporting ideas must be distinguished from genuine prerequisites;
- the learner must be able to reach where the needed idea is taught or repaired;
- the mapping must generalise across questions rather than create one concept per surface context.

UNDERLYING HUMAN PROBLEM:
when a learner is stuck on a real worksheet question, the system needs to identify
what reusable ability is actually missing, what earlier understanding is genuinely required,
and where that understanding can be learned

HUMAN OUTCOME:
real questions reliably lead a learner to the right reusable knowledge and prerequisite repair

GENUINE CONSTRAINTS:
the mapping must remain reusable across future questions;
prerequisites must be genuine;
surface context must not become a capability by itself

EXPERTISE:
learning-system and curriculum-mapping expertise

IMAGINATION OBJECT:
an excellent question → reusable learning need → prerequisite → teaching outcome

PROMPT 2

REALITY OBJECT:
what Issue #19, the current repository, later PRs and real-question evidence
have already accomplished

PROMPT 3

COMPARISON QUESTION:
given today's repository, what meaningful work under Issue #19 genuinely remains,
if any, and what is the smallest durable response?

HANDOVER DESTINATION:
the next agent should understand the learner problem, what is already solved,
the real remaining gap, the reusable idea exposed by real questions,
and what evidence would justify changing course

LOT/LEVEL BOUNDARY GATE:
PASS — the target remains Issue #19, not overall Grade9V3

SPECIFICITY-FLOOR GATE:
PASS — the prompt is specifically about worksheet-question-to-learning mapping

SAME-ISSUE IDENTITY GATE:
PASS — a Grade9V3-aware reader can distinguish this from sibling content/routing issues

ANSWER-RECONSTRUCTION GATE:
PASS — matrices, rungs, schema fields and current implementation recipe are withheld

ARTIFACT-ERASURE GATE:
PASS — Prompt 1 still works if matrices, rungs and the issue checklist disappear

CURRENT-VOCABULARY GATE:
PASS — current implementation vocabulary is quarantined

PROMPT-1 OBJECT GATE:
PASS — the answer independently defines the question-to-learning outcome

PROMPT-3 FREEDOM GATE:
PASS — Issue #19 may shrink, close, defer, change form or require bounded implementation
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

# APPENDIX F — MULTI-LOT REGRESSION: ISSUE LEVEL VS TAB LEVEL

This case exists because a generator previously received:

```text
Lot 1 — issue level
Lot 2 — tab level
```

and incorrectly produced:

```text
Lot 1 — Issue #1854
Lot 2 — Issue #1834
```

That is a schema failure.

## Lot 1 — ISSUE_TASK

Requested target:

```text
Issue #1854
Open-items register after the P0 product fixes
```

This issue is unusually easy to over-generalise because its present form is a register.

The blind pass must preserve its **post-P0 closure problem**, not the register form.

A compliant kernel is closer to:

```text
PROBLEM KERNEL:
- The target is the EMP.1 / WRC 537 professional product programme.
- A substantive P0 product-fix round has just changed what is true.
- The question is what genuinely remains before further bounded professional-release work is worthwhile.
- Some remaining matters may be executable engineering; others may require accountable disposition rather than implementation.
- Earlier sequencing may have become historical because the product changed.
```

A strong Prompt 1 could begin:

> EMP.1/WRC has just come through a substantial round of product fixes. Before anyone spends another engineering week, imagine you are responsible for deciding what genuinely remains between the product as it now stands and a worthwhile bounded professional release. What must you establish about remaining engineering work, unresolved authority/judgement, obsolete plans, independent work, and stop/defer conditions before continuing?

That is recognisably #1854's underlying problem.

It does **not** reveal today's gamma item, CI outage, UI residue, hash issue, current sequence, or acceptance list.

The following is too generic and should fail:

> How should a responsible owner determine what remains in a complex engineering programme?

The following is contaminated and should also fail:

> Given the gamma decision, CI outage, U-16 residue and resultHash issue, what order should the remaining work take?

## Lot 2 — TAB_SURFACE

Requested target:

```text
EMP.1 / WRC 537 user-facing tab
inside reallaksh19/Advanced_Analysis
```

Do **not** substitute Issue #1834, #1830, #1775 or any other issue as the target.

Those are Prompt-2 evidence.

A strong Prompt 1 should be recognisably about the actual engineering tab:

> Imagine a practising pressure-equipment engineer opening a browser tool because they need a defensible WRC 537 local-stress assessment for a real vessel/attachment problem. They have geometry, thicknesses, material information and loads, but they did not write the software and should not need to know its internal architecture. Walk through what this one tab should let them understand, enter, check, calculate, refuse, review and retain before they would put the result into an engineering assessment.

Then explore target-specific questions such as:

- what geometry/load/source information the engineer must understand and what the tool can derive;
- how the method's applicability should be made obvious before and during the run;
- how load transfer, local-stress results and governing locations should be explained;
- what the engineer sees when the method cannot honestly answer;
- how numerical comparison evidence differs from source/method authority;
- what makes a result current, reviewable and defensible;
- what the tab should retain/export so another engineer can reconstruct the assessment;
- what should be simple versus deliberately explicit in safety-relevant work.

Notice the distinction:

```text
SPECIFIC:
WRC 537
pressure-equipment engineer
real vessel / attachment geometry
loads
local stresses
applicability
result / refusal
review evidence

NOT CURRENT-ANSWER LEAKAGE:
gamma=5 current implementation
specific current UI defects
current issue sequence
current CI outage
specific current PRs
```

This is the required standard:

> **Blind to today's answer. Richly specific to today's requested target.**

---

# APPENDIX G — ISSUE-LEVEL SPECIFICITY CONTROL: #1834

This case protects against **laundered generalisation**.

A weak generator reads Issue #1834, strips its proper nouns, and produces:

> A published standard has discrete tabulated values. Real equipment lies between them.
> How should a responsible decision package be built?

That is not genuinely blind.

It is the current issue narrative rewritten generically.

It also loses the issue's identity.

## Correct PROBLEM KERNEL

```text
- EMP.1 is a WRC 537 local-attachment assessment capability for pressure-equipment work.
- Professional-use applicability is tied to tabulated gamma conditions.
- Real vessel geometry commonly requires non-tabulated gamma values.
- WRC 537 does not itself supply the missing non-tabulated-gamma rule.
- The unresolved engineering problem is what basis, if any, could justify serving such cases
  without pretending that numerical plausibility creates WRC source/method authority.
```

## What Prompt 1 may know

It may know those kernel facts.

They are the problem.

It may also use stable domain distinctions such as:

```text
source/method fidelity
numerical validity
conservatism
independent qualification
organisation-owned policy
professional-use authority
fail-closed refusal
```

## What Prompt 1 must not know

```text
current Option 1 / 2 / 3
LINEAR_GAMMA
LOG_GAMMA
current sample size/statistics
current CAUx agreement percentage
current repository recommendation
current downstream issue sequence
```

## Strong Prompt-1 direction

> EMP.1 is intended to support WRC 537 local-attachment assessment for real pressure-equipment work. The professional-use basis is tied to tabulated gamma conditions, but real vessel geometry commonly falls between those conditions and the source itself does not provide the missing rule. Before looking at how the current repository has approached that gap, reason from engineering first principles: what would have to be true before an organisation could responsibly let the product serve non-tabulated-gamma cases? What separate claims would need support—numerical behaviour, conservatism, source fidelity, independent qualification, organisation-owned policy and professional-use authority? When is refusal the correct answer? What evidence would change your position?

This passes because a programme-aware engineer can identify the issue, but cannot infer today's chosen options or evidence conclusion.

---

# APPENDIX H — COMPLEX PROMPT-1 Q1–Q5 HUMAN REASONING MODE

Use this appendix **only when COMPLEX MODE = ON** because the user explicitly used the word **complex** for that target/lot.

The source idea comes from the engineering-pr-delivery-v2.5 qualification model:

```text
Q1 actual production path, state owner, authority source, downstream consumer
Q2 engineering reconstruction; quantitative work carries concrete payload values
Q3 explicit mutation + protected invariant + exact falsifier
Q4 independent verification using incoming benchmark/oracle evidence
Q5 exact first bounded change + predicted before/after verification
```

In a qualification QSET those are repository-grounded takeover questions.

In **Prompt 1**, however, the current repository/answer is still hidden.

Therefore preserve the reasoning intent, but translate it into a first-principles human conversation.

## Governing rule

> **Complex mode makes Prompt 1 deeper, not more mechanical.**

Do not paste QSET vocabulary into Prompt 1.

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

> Walk me through the real journey from the thing the person starts with to the thing they finally rely on. Where does each important fact or decision come from? What should be authoritative at each hand-off? Who or what depends on it next?

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

> Take one representative real case that genuinely belongs to this problem. Work it through from beginning to end. If this is quantitative, use concrete plausible values and show the intermediate reasoning. What result or conclusion should we expect, and where are the points most likely to be misunderstood?

For non-quantitative targets, reconstruct the logic or decision journey rather than inventing numbers.

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

> Suppose you did not trust the main mechanism at all. How would you check the important conclusion independently? Is there a hand calculation, second source, benchmark, physical argument, second representation, real example, or other route that does not merely repeat the same assumptions?

Where meaningful, ask what level of agreement would count and why.

Independence matters more than having many checks.

## Q5 — Human first bounded proof: what is the smallest real slice worth trying first?

Canonical intent:

```text
first safe bounded change
predicted before
predicted after
verification
```

Prompt 1 must not turn this into a patch plan for today's repository.

Translate it into a **first proof slice**:

> If you could test only one small, bounded slice of this idea before committing to the larger direction, what would you choose? What would you expect to see before and after? What evidence would convince you it worked, and what result would make you stop rather than expand?

This gives Prompt 3 a disciplined seed later without contaminating Prompt 1 with current implementation assumptions.

## Human weaving requirement

Do not produce five disconnected exam questions.

The preferred shape is a natural progression:

```text
Start with the person's real journey.
→ work one concrete case through
→ disturb one important assumption/input
→ check the conclusion independently
→ identify the smallest bounded proof worth trying
```

Prompt 1 may use paragraphs, a journey, or conversational questions.

The labels Q1–Q5 are for the generator's internal coverage check, not normally for the future agent.

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
- a realistic person/journey;
- genuine constraints.

Complex mode should make the prompt **more concrete and diagnostic**, not longer for its own sake.

## Example — complex issue-level engineering decision

Weak:

> Trace the process. Reconstruct the problem. State the invariant. Validate independently. Pick a first slice.

Still too mechanical.

Better:

> Start with the practising engineer who needs to use this method on the kind of real case that creates the issue. Walk the reasoning from their physical inputs through method applicability to the professional conclusion they need to rely on: where should authority come from, and who relies on that conclusion next?
>
> Then take one representative case and work the engineering logic through concretely. Show what the method would need to establish, what remains an assumption, and what a defensible expected result would look like.
>
> Now perturb one important condition. What should change? What must remain protected? What observation would prove that the whole reasoning model is wrong rather than merely inconvenient?
>
> Check the central conclusion by a genuinely independent route rather than by another expression of the same assumption.
>
> Finally, if you were allowed to test only one bounded proof before committing to a larger programme, what would you test first, what would you predict beforehand, and what result would make you stop?

That is Q1–Q5 in human form.

---

# NINE-CASE REGRESSION VALIDATION

Before considering a future schema revision safe, mentally run these controls:

| Case | Prompt-1 independent object | Main contamination risk | Prompt-3 freedom requirement |
| --- | --- | --- | --- |
| Static browser PDF editor | excellent browser PDF experience/product | current implementation architecture | may preserve/change architecture |
| Overall Grade9V3 | excellent Grade-9 self-study learner journey/system | Core/matrix/gate vocabulary | may redefine programme priorities |
| Grade9V3 Issue #19 | excellent question → reusable learning need → prerequisite → teaching outcome | matrix/rung/current checklist | may shrink/close/rewrite task |
| Advanced_Analysis Issue #1855 | excellent judgement about what genuinely remains and can safely happen next | “register” and current queue/details | may preserve/reconcile/replace/close register |
| Advanced_Analysis Issue #1854 | excellent post-change judgement about the true remaining path | sanitized restatement of issue as blind context | may preserve/reconcile/replace/close register |
| Advanced_Analysis Issue #1756 | excellent methodical qualification of shell capability from foundations through release | current architecture/child-roadmap form | may preserve/rewrite/split/retire roadmap |
| EMP.1/WRC tab-level lot | practising engineer's end-to-end WRC 537 tab experience | related issue substitution + generic Prompt 1 | may redefine tab UX/workflow while preserving method authority |
| Advanced_Analysis Issue #1834 | responsible basis for non-tabulated-gamma professional use | generic standards-governance prose or leaked current options/evidence | may yield decision/evidence need without inheriting current option set |
| Explicit complex-mode target | same target plus human Q1–Q5 depth | mechanical Q labels or generic five-question checklist | Prompt 1 covers path → reconstruction → stress test → independent check → bounded proof |

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

But independence is not vagueness.

> **Prompt 1 must be blind to today's answer while remaining richly specific to the user-requested target, level, domain and job-to-be-done.**

The user's lot boundaries are authoritative. A tab-level request stays tab-level; a related issue becomes evidence, not a substitute target.

For issue-level work, preserve the **PROBLEM KERNEL**:

> **Erase today's answer, not the facts that make it the same issue.**

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

> **Prompt 1 must reason through Q1–Q5 in human form: journey, concrete reconstruction, invariant/falsifier, independent check, and first bounded proof.**

Complexity must deepen specificity and falsifiability; it must never become generic ceremony.

Prompt 2 brings reality back.

Prompt 3 decides what deserves to survive.

The handover preserves the reasoning journey so the next agent inherits understanding, not merely activity.
