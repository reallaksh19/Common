# Learner Knowledge Profile and Flexible Readiness Addendum

## Role

This addendum extends the Grade 9 IOQM study-guide builder with two optional capabilities:

1. **topic/subtopic/skill-wise learner knowledge input** instead of always assuming one global 30–50% prior-knowledge level;
2. **flexible short-horizon Quick Check size** using `T1 ... Tx` rather than a fixed `T1 ... T10` count.

Use it with:

- `../SKILL.md`;
- `question-driven-self-sufficient-study-guide-skill-v2.md`;
- `difficulty-badges-portability-and-challenge-ladders-addendum.md`;
- the applicable domain profile, if one exists.

This addendum changes learner-profile defaults and short-horizon diagnostic selection. It does **not** weaken source custody, self-sufficiency, difficulty, visual, worked-bridge, hint, provenance, or PDF-QA requirements.

When this addendum conflicts with a fixed prior-knowledge percentage or a fixed Quick Check item count in an older generalized/domain profile, this addendum takes precedence for those two fields only.

---

## 1. Default behavior when no learner profile is supplied

If the user provides no learner-specific knowledge information, use the existing partial-knowledge baseline:

> roughly 30–50% of the school-level background is available, but method recognition and Olympiad execution are unreliable.

This is a production assumption, not a measured learner score.

The durable core should still be written to support a partial-knowledge Grade 9 learner even when a personalized short-horizon route is also produced.

---

## 2. Optional learner-knowledge input

The user may supply knowledge at any useful granularity:

- whole subject;
- topic;
- subtopic;
- stable skill ID;
- specific method family.

Example:

```yaml
learner_knowledge:
  overall: partial
  topics:
    Symmetric Algebra: weak
    Quadratics: strong
    Polynomials:
      overall: partial
      Vieta: strong
      Factor theorem: weak
      Repeated roots: unknown
    Sequences:
      AP: strong
      GP: partial
      Recurrences: weak
  skills:
    ALG-EQ-04: unknown
    ALG-POLY-05: weak
```

Equivalent natural-language input is also valid, for example:

> “Comfortable with AP and basic quadratics; weak in polynomial roots; almost no recurrence practice.”

Normalize the input internally instead of forcing the user to rewrite it into a schema.

---

## 3. Accepted knowledge values

Accept any of these forms:

### Categorical

- `UNKNOWN`
- `NONE`
- `WEAK`
- `PARTIAL`
- `STRONG`
- `SECURE`

### Approximate percentage

A user may provide values such as:

```text
Quadratics = 80%
Polynomial roots = 40%
Recurrences = 10%
```

Treat percentages as **planning estimates** unless they come from an actual measured diagnostic.

Do not manufacture decimal precision or claim psychometric calibration.

### Free text

Examples:

- “I know formulas but cannot decide what to use.”
- “I can do Vieta but not repeated roots.”
- “Geometry circles are okay; similarity is weak.”

Translate the meaning into the nearest internal state while preserving uncertainty.

---

## 4. Knowledge-resolution precedence

When multiple levels are supplied, the most specific relevant input wins.

Default precedence:

```text
latest observed diagnostic evidence
> explicit stable-skill/method input
> subtopic input
> topic input
> subject-level input
> default partial-knowledge assumption
```

Example:

```text
Polynomials = STRONG
Repeated roots = WEAK
```

The learner is treated as `WEAK` for repeated-root routing even though the parent topic is `STRONG`.

Do not average away a specific weakness into a broad topic percentage.

If two equally specific user statements conflict, preserve the uncertainty and mark the skill `UNKNOWN/PARTIAL` until checked rather than silently choosing one.

---

## 5. Internal learner-knowledge matrix

When learner-specific input exists, create an internal matrix such as:

| Scope | Stable skill(s) | Stated knowledge | Evidence/source | Routing status | Diagnostic need |
|---|---|---|---|---|---|
| topic/subtopic | IDs | UNKNOWN/NONE/WEAK/PARTIAL/STRONG/SECURE | user / diagnostic / teacher | do-first / do-next / retest / skip | none / spot-check / required |

The exact file/table is optional unless the package needs reviewer traceability, but the logic must be explicit.

Recommended interpretation:

| Knowledge state | Default short-horizon action |
|---|---|
| `UNKNOWN` | diagnose if educationally important |
| `NONE` | foundational teaching; high-value families route early |
| `WEAK` | DO FIRST if high-value; usually probe recognition + first move |
| `PARTIAL` | DO NEXT / targeted check; distinguish recognition from execution internally |
| `STRONG` | one spot-check or mixed retest; avoid repetitive teaching |
| `SECURE` | normally skip direct teaching in 3-day route; retain in durable core |

These states guide routing. They do not alter source truth or syllabus ownership.

---

## 6. Durable core must not be pruned by personalization

A personalized learner profile changes:

- Navigator route;
- Quick Check selection;
- practice priority;
- starting scaffold/hint level;
- which Worked Bridges are emphasized;
- Challenge Ladder starting rung;
- what is retested versus skipped in the 3-day plan.

It does **not** automatically remove teaching from the durable reference core.

The reference book should remain reusable for a partial-knowledge learner unless the user explicitly requests a personally pruned edition.

Therefore:

```text
PERSONALIZATION = ROUTING_AND_EMPHASIS
CORE_SELF_SUFFICIENCY = PRESERVED
```

---

## 7. Interaction with difficulty badges

Learner knowledge and authored difficulty are separate.

Do not change a question's `D1-D5` badge merely because this learner is strong or weak at the required concept.

Example:

```text
QUESTION = D4 ADVANCED
Vieta = STRONG
Repeated roots = WEAK
```

Keep the learner-facing question badge:

```text
[D4 ADVANCED]
```

Then route personally:

```text
PERSONAL_RISK
Vieta = LOW
Repeated roots = HIGH
```

Difficulty answers:

> How demanding is this task for a suitably prepared learner?

Learner knowledge answers:

> Which parts of this task are risky for this learner?

Priority answers:

> How important is this skill for the current syllabus/horizon?

Keep all three separate.

---

## 8. Flexible Quick Check: `T1 ... Tx`

The short-horizon Quick Check must not assume that every learner needs the same number of probes.

Use:

```text
T1, T2, ... Tx
```

where `x` is selected from:

- the learner-knowledge profile;
- number of high-value families whose status is unknown/weak/partial;
- domain coverage needs;
- available Quick Check time;
- page-fit / simple-Navigator constraints;
- explicit user-requested count, if supplied.

`T` numbering is edition-local diagnostic numbering. It is never source authority and must never collide with corpus `Q` numbering.

---

## 9. How to choose `x`

### Step 1 — build the candidate family set

Start from high-transfer / prerequisite / canonical families in the question-to-method matrix and domain profile.

### Step 2 — use known learner information

- `SECURE`: normally no dedicated T item; optional mixed spot-check only.
- `STRONG`: usually one spot-check across a cluster, not one item per subskill.
- `PARTIAL`: usually one targeted recognition/first-move probe.
- `WEAK` / `NONE`: include if the family matters to the 3-day route.
- `UNKNOWN`: include when the family is high-value enough that its status affects routing.

### Step 3 — use difficulty intelligently

Difficulty is supporting metadata, not the Quick Check selection rule.

Prefer probes that discriminate important decisions.

Examples:

- a weak D2 prerequisite may deserve a T slot before a niche D5 concept;
- a D3 recognition probe can be more useful than a long D4 execution item;
- do not select T items merely to create one item from every D-level.

### Step 4 — deduplicate mechanisms

Do not spend two Quick Check slots on duplicate source questions or two surfaces that test the same decision unless contrast/discrimination is the explicit teaching goal.

### Step 5 — fit the time budget

Each T item should normally take about 1–2 minutes and should ask for recognition / first move rather than full solution.

For the simple child-facing Navigator, a useful default is roughly **10–15 minutes total**.

Typical `x` may therefore be around **6–10**, but this is a design default, not a hard rule.

A domain or user may legitimately use a smaller or larger `x` when coverage and page design justify it.

### Step 6 — preserve a simple interface

Do not increase `x` merely because many deficits exist.

The Quick Check samples the decisions that change the 3-day route. It is not a mini-exam covering every skill.

---

## 10. Explicit user override for Quick Check count

If the user supplies a desired count, for example:

```text
quick_check_count = 7
```

or

> “Give me 12 readiness prompts.”

honor the count unless it is impossible to preserve the requested layout or source constraints.

When the requested count is smaller than the number of important families, prioritize:

1. weak/unknown high-dependency families;
2. high-transfer method-selection families;
3. representative contrasts between commonly confused methods;
4. spot-checks of claimed strong areas only if space remains.

Do not pretend an intentionally short Quick Check sampled every family.

---

## 11. Topic/subtopic-specific readiness mode

The 3-day readiness check may target the whole subject or only a supplied scope.

Examples:

```text
scope = Algebra
```

or

```text
scope = Polynomials + Recurrences
```

or

```text
scope = Geometry / Circles only
```

When scope is narrow, `T1 ... Tx` should probe distinctions **inside that scope** rather than wasting slots on unrelated topics.

Example for a polynomial-only readiness check:

- factor/remainder theorem;
- Vieta;
- repeated roots;
- strategic evaluation;
- power sums;
- composition/preimages;
- integer-root consequences.

---

## 12. Probe identity versus printed T number

For reusable authoring, a domain may keep stable internal probe IDs, for example:

```text
ALG-PROBE-SYM2
ALG-PROBE-REPEATROOT
ALG-PROBE-RECURRENCE
```

The student-facing edition still renumbers selected probes sequentially:

```text
T1 ... Tx
```

This allows the probe bank to evolve without making `T7` itself a stable curriculum identity.

---

## 13. Algebra interpretation

In the Algebra profile, the existing ten prompts should be treated as the **default no-profile probe bank**, not as a permanently mandatory printed set.

Default candidate families include:

- sum-product compression;
- repeated `xyz`;
- discriminant/root condition;
- repeated root;
- `P(m)=P(k)` factor difference;
- AP/GP overlap;
- large-index recurrence;
- common exponent substitution;
- fixed-sum extremum/smoothing;
- midpoint shift for symmetric poles.

When learner knowledge is supplied:

- select the relevant subset;
- add a probe for another high-value weak/unknown Algebra family if needed;
- renumber the final printed set `T1 ... Tx`;
- keep `Q1 ... Q50` exclusively for the actual corpus.

Examples of extension probe families when needed:

- `s,q,r` three-variable symmetry;
- Vieta/power sums;
- rational/radical legality;
- functional/polynomial identity recognition;
- integer/divisibility filter;
- composition/preimage symmetry.

The existing `T1–T10` wording remains a valid default edition when no learner-specific profile is available.

---

## 14. Student-facing Quick Check instruction

Use a stable simple instruction regardless of `x`:

> **Quick Check — What would you try first?**  
> Spend about 1–2 minutes on each. Do not fully solve. Mark: `[OK] knew the move` `[?] unsure` `[X] no idea`.

Do not show H1, method router, or method-revealing visual before the learner marks the item.

After marking, route the learner to readable skill names and the relevant core section.

---

## 15. Readiness output

A personalized short-horizon route should be able to say, in learner-facing language:

- **DO FIRST** — important weak/unknown skills;
- **DO NEXT** — partial/uncertain skills;
- **QUICK RETEST** — strong skills that only need confirmation;
- **ONLY IF TIME** — low-value/niche material for the current horizon.

The internal system may keep richer diagnostic states, but the child interface remains simple.

Difficulty badges may remain visible on linked questions, but do not turn the route into `do hardest first`.

---

## 16. Challenge Ladder starting point

When Challenge Ladders exist, learner knowledge determines where to enter the ladder.

Example:

```text
Repeated roots ladder: D1 -> D2 -> D3 -> D4 -> D5
learner state: PARTIAL
```

Default action:

- skip D1 if evidence shows the prerequisite is secure;
- start around D2/D3;
- move up one rung after independent success;
- move down or open the Worked Bridge when recognition/execution breaks;
- use a non-identical later rung for transfer rather than immediately repeating the same item.

The D-level itself does not diagnose mastery; it only describes authored task demand.

---

## 17. Acceptance gates

When no learner-specific knowledge is supplied:

```text
LEARNER_KNOWLEDGE_PROFILE = DEFAULT_PARTIAL_KNOWLEDGE
```

When learner-specific knowledge is supplied:

```text
LEARNER_KNOWLEDGE_PROFILE = PRESENT_NORMALIZED
KNOWLEDGE_SCOPE_RESOLUTION = PASS
MOST_SPECIFIC_KNOWLEDGE_WINS = PASS
UNSUPPORTED_PRECISION_INTRODUCED = 0
CORE_SELF_SUFFICIENCY_PRESERVED = PASS
DIFFICULTY_MASTERY_CONFLATION = 0
```

For a flexible Quick Check:

```text
QUICK_CHECK_COUNT = x
QUICK_CHECK_LABELS = T1_TO_Tx
QUICK_CHECK_COUNT_DERIVATION = PASS
QUICK_CHECK_SCOPE_COVERAGE = PASS_FOR_SELECTED_SCOPE
QUICK_CHECK_UNAIDED_BEFORE_HINT = PASS
QUICK_CHECK_Q_LABEL_COLLISION = 0
DUPLICATE_MECHANISMS_WASTING_T_SLOTS = 0
```

If a domain profile contains a fixed gate such as `QUICK_CHECK_ITEMS = 10`, interpret it as the **default no-profile edition**. When this addendum is active, replace it with the dynamic `x` gate above.

---

## 18. Final principle

Do not ask:

> “Is this student 50% prepared?”

when more useful information is available.

Ask:

> “Which important skills are secure, partial, weak, or unknown — what difficulty rung is informative next — and what is the smallest readiness check that changes what they should do over the next three days?”

The durable guide stays complete. The personal route becomes specific.
