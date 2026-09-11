# Difficulty Badges, Portability, and Challenge Ladders Addendum

## Role

This addendum makes the study-guide builder more portable across competitive-exam domains and adds a robust learner-facing difficulty system.

Use it with:

- `../SKILL.md`;
- `question-driven-self-sufficient-study-guide-skill-v2.md`;
- `learner-knowledge-profile-and-readiness-addendum.md` when learner-specific knowledge exists;
- the applicable domain profile;
- the visual-production addendum when badge/icon rendering or other visuals are generated in the final document.

It introduces four linked ideas:

1. a **domain-neutral modular architecture** so the builder can later support Physics and Chemistry without inheriting Mathematics-only assumptions;
2. a **difficulty calibration contract** for questions, concepts, subtopics, and topics;
3. learner-facing **difficulty badges/stamps** and compact **citation/source badges**;
4. **Challenge Ladders** that reuse existing questions/Worked Bridges by increasing difficulty instead of creating another redundant mixed problem appendix.

This addendum is a production-calibration system. Unless real learner-response data exist, its difficulty labels are authored estimates, not psychometric measurements.

---

## 1. Portable builder architecture

Treat the reusable study-guide system as:

```text
STUDY-GUIDE ORCHESTRATOR
|
|-- source / corpus custody
|-- learner knowledge profile
|-- difficulty calibration + badges
|-- question -> concept -> method map
|-- concept dependency / progression map
|-- challenge-ladder generator
|-- short-horizon readiness/router
|-- practice + assessment design
|-- visual-production contract
|-- document / PDF QA
|
`-- domain profiles
    |-- mathematics
    |   |-- algebra
    |   |-- geometry
    |   |-- number theory
    |   `-- combinatorics
    |-- physics
    `-- chemistry
```

The orchestrator owns cross-domain production mechanics.

Domain profiles own domain-specific representations, legality checks, terminology, worked-example patterns, and difficulty anchors.

Examples:

- Mathematics may define Vieta, cyclicity, invariants, valuation, proof structure, etc.
- Physics may define system choice, free-body diagrams, sign conventions, modelling assumptions, dimensional checks, graph interpretation, conservation laws, experimental reasoning, etc.
- Chemistry may define equation balancing, stoichiometric representation, limiting reagent logic, periodic trends, equilibrium reasoning, molecular structure, reaction constraints, unit/mole conversions, etc.

Do **not** force Mathematics-specific method vocabulary into Physics/Chemistry merely because the same orchestrator is used.

---

## 2. Four quantities that must remain separate

Never collapse these into one label:

```text
DIFFICULTY != PRIORITY
DIFFICULTY != LEARNER_MASTERY
DIFFICULTY != FREQUENCY
DIFFICULTY != EMPIRICAL_ITEM_DIFFICULTY
```

### Authored difficulty

A curriculum/author estimate of the cognitive and execution demand for a suitably prepared learner.

### Learner-relative risk

How risky the item is for this learner given their topic/subtopic/skill knowledge profile.

### Educational priority

How valuable the skill/item is for the declared syllabus, transfer, dependency graph, and short-horizon route.

### Empirical item difficulty

Observed difficulty inferred from real learner-response data.

Do not call authored labels `empirical`, `calibrated`, `percentile`, or `psychometric` unless appropriate response data and a real calibration method exist.

---

## 3. Question difficulty dimensions

Before assigning a question badge, rate the item internally on these portable dimensions.

| Code | Dimension | Core question |
|---|---|---|
| `K` | Knowledge depth | How much prerequisite knowledge is required? |
| `R` | Recognition | How hidden is the relevant method/principle? |
| `M` | Representation / modelling | Must the learner change representation, choose a model, or construct a useful state/diagram? |
| `E` | Execution | How long or technically demanding is the correct route after the opening is found? |
| `I` | Integration | How many distinct concepts/principles must interact? |
| `B` | Branching / constraints | Are there cases, domains, legality checks, exceptional conditions, or competing branches? |
| `T` | Transfer novelty | How far is the surface from the examples on which the method was taught? |

Use a small internal ordinal scale such as `0-3` for each dimension.

Example internal record:

```text
QDIFF_PROFILE
K=2
R=3
M=3
E=2
I=2
B=1
T=3

AUTHORED_DIFFICULTY = D4
DIFFICULTY_CONFIDENCE = MEDIUM
```

The profile explains **why** the question is difficult.

Do not expose the seven-number profile to a Grade 9 learner by default.

---

## 4. Five difficulty levels

Use five human-readable authored levels.

| Badge | Name | Anchor |
|---|---|---|
| `D1` | **DIRECT** | Recall or one familiar operation; method/representation is obvious. |
| `D2` | **ROUTINE** | Familiar method with short multi-step execution. |
| `D3` | **STRATEGIC** | Method must be selected; small representation change or concept combination is needed. |
| `D4` | **ADVANCED** | Non-obvious opening, substantial integration/branching, or meaningful transfer. |
| `D5` | **CHALLENGE** | Deep synthesis, unusual representation/model, proof/insight, or very high transfer distance. |

These labels are domain-neutral; each domain profile should provide concrete anchor examples.

A badge must reflect the **whole task**, not merely the hardest-looking formula in the statement.

---

## 5. Learner-facing question difficulty badge

Every learner-facing question in the core practice, Appendix A, Appendix B, Challenge Ladders, or mock/test material should carry a small difficulty stamp unless the user explicitly requests a clean exam facsimile.

Preferred display:

```text
[D3 STRATEGIC]
```

or, in a designed PDF, a small rounded badge in the question header:

```text
D3
STRATEGIC
```

### Placement

- top-right of the question card/header when possible;
- never inside the mathematical statement;
- visually secondary to the question number/title;
- consistent size and position throughout the book.

### Badge design

- use a compact vector/text pill or stamp;
- do not rely on color alone; print `D1`-`D5` explicitly;
- keep text readable in grayscale and at final PDF size;
- no decorative star ratings such as `***` because they are ambiguous;
- avoid red=`bad`/green=`good` emotional coding; difficulty is not performance judgment;
- a monochrome or restrained five-step tint system is acceptable if the code/name remains printed.

### Clean exam exception

For an exam-simulation page where difficulty metadata would influence strategy unnaturally, hide badges during the attempt and show them only in the answer/review section.

---

## 6. Topic difficulty badge

A topic is rarely one fixed difficulty.

Do **not** stamp a broad topic simply `D4` when its questions range from basic to Olympiad-level.

Use a difficulty band.

Preferred learner-facing topic badge:

```text
[D2 -> D5]
```

Meaning:

- accessible/core entry questions begin around D2;
- the topic can extend to D5 challenge work.

Internal topic record may be richer:

```text
TOPIC_DIFFICULTY
ENTRY = D2
CORE = D3
CEILING = D5
SPREAD = WIDE
```

A chapter heading can therefore show:

```text
POLYNOMIALS                          [D2 -> D5]
```

This is more honest than pretending the entire chapter has one difficulty.

---

## 7. Subtopic and concept difficulty badges

For a narrow subtopic or stable concept, distinguish learning/direct use from hidden transfer when that difference matters.

Internal form:

```text
CONCEPT_DIFFICULTY
LEARN = D2
DIRECT_APPLY = D2
HIDDEN_TRANSFER = D4
```

Example:

```text
Vieta
learn D2 | direct D2 | hidden transfer D4
```

The default learner-facing badge should remain compact.

Preferred options:

```text
[D2 core | D4 transfer]
```

or, where space is tight:

```text
[D2 -> D4]
```

Do not print three technical difficulty dimensions beside every concept unless a teacher/reviewer edition requests them.

---

## 8. Difficulty badge assignment procedure

For every question:

1. identify required stable concepts/skills;
2. rate `K,R,M,E,I,B,T` internally;
3. assign a proposed `D1-D5` level from the anchored definitions;
4. compare with nearby questions in the same concept family;
5. verify that a D-level increase corresponds to a real increase in cognitive/transfer demand, not merely larger numbers or longer arithmetic;
6. record confidence: `HIGH`, `MEDIUM`, or `LOW`;
7. allow domain-profile overrides where the generic anchor is misleading.

Recommended matrix fields:

- `authored_difficulty`;
- `difficulty_profile_KRMEIBT`;
- `difficulty_confidence`;
- `learner_relative_risk` if a learner profile exists;
- `priority` as a separate field;
- `difficulty_badge_rendered = YES/NO`.

---

## 9. Difficulty must not be computed by a fake precise formula

Do not publish a formula such as:

```text
Difficulty = 2.73K + ...
```

unless it is genuinely calibrated and validated.

The seven dimensions are an **authoring rubric**.

Use anchored judgment and cross-question consistency.

If the author is uncertain between two levels, record `LOW` confidence and prefer the lower learner-facing badge until reviewed, unless under-labelling would create a safety/expectation problem in another domain.

---

## 10. Learner-relative risk

When a learner knowledge profile exists, do not rewrite the authored difficulty badge to match that learner.

Example:

```text
QUESTION = D4 ADVANCED

required skills:
Vieta = STRONG
Repeated roots = WEAK
Integer filter = PARTIAL
```

Keep the question badge:

```text
[D4 ADVANCED]
```

Then route personally:

```text
PERSONAL_RISK
repeated roots = HIGH
integer filter = MEDIUM
Vieta = LOW
```

The same D4 question can therefore be easy for one prepared learner and risky for another without corrupting the authored difficulty label.

---

## 11. Difficulty badges in the three-day Navigator

Difficulty badges may support the route but must not replace knowledge/priority logic.

Bad default:

> “Do all D5 questions first because they are hardest.”

Correct logic:

- secure high-value D4 skill -> quick retest;
- weak high-value D2 prerequisite -> DO FIRST;
- weak niche D5 skill -> often ONLY IF TIME;
- D3/D4 transfer questions -> use after prerequisite repair.

Therefore:

```text
PERSONAL_ROUTE = learner deficit + educational priority + prerequisite order
```

Difficulty is supporting metadata, not the routing algorithm.

---

## 12. Citation / source mini-badges

Long source notes beside every student question create clutter. Use a compact mini-badge when provenance is useful at point of use.

Preferred learner-facing forms:

```text
[SRC 12]
```

or a designed mini-badge with a small vector book/link icon plus the source-ledger number:

```text
book-icon 12
```

### Badge meaning

The badge points to the source/provenance ledger; it is **not** itself the complete citation.

Example question header:

```text
Q18                                  [D4 ADVANCED]   [SRC 12]
```

### Digital PDF behavior

Where the PDF pipeline supports internal hyperlinks:

- clicking/tapping the source badge should jump to the source-ledger entry;
- the ledger entry may contain the full citation/link/source-status note;
- use a backlink only if it does not clutter the ledger.

### Static/print behavior

The numeric/text code must remain understandable without color or hyperlink.

### Glyph fallback

Do not depend on an emoji icon.

Preferred rendering order:

1. vector-drawn book/link/source icon;
2. supported embedded glyph;
3. text pill `SRC 12`.

Broken/missing icon glyphs are a QA failure.

---

## 13. Source badge taxonomy

Keep the student-facing badge simple, but preserve source status internally.

Suggested internal source-status values:

- `OFFICIAL_VERIFIED`;
- `REPOSITORY_VERIFIED`;
- `IDENTIFIED_EXTERNAL`;
- `AUTHOR_CREATED`;
- `RECONSTRUCTED`;
- `UNRESOLVED`.

Optional compact learner badges where distinction matters:

```text
[SRC 12]     external/identified source entry
[AC]         author-created
[UNV]        unresolved/reconstructed item when the uncertainty itself matters
```

Do not overload ordinary questions with multiple provenance pills.

When uncertainty affects mathematical/source custody, the ledger remains authoritative.

---

## 14. Badge density rule

A question header should normally contain at most:

- question ID;
- one difficulty badge;
- one source/citation badge if useful;
- optional priority badge only in a dedicated study-route edition.

Avoid badge soup.

Bad:

```text
Q17 [D4] [MUST] [H3] [SRC7] [ALG-INEQ-02] [RED]
```

Better student-facing:

```text
Q17                         [D4 ADVANCED] [SRC 7]
```

Stable skill IDs, hint depth, priority, learner status, and internal diagnostics remain in quieter secondary locations or reviewer metadata.

---

## 15. Difficulty badge QA

Before final PDF acceptance require:

```text
QUESTION_DIFFICULTY_ASSIGNED = PASS_n_OF_n
QUESTION_DIFFICULTY_BADGES_RENDERED = PASS_n_OF_n
TOPIC_DIFFICULTY_BANDS_PRESENT = PASS_n_OF_n
DIFFICULTY_PRIORITY_CONFLATION = 0
DIFFICULTY_MASTERY_CONFLATION = 0
UNSUPPORTED_EMPIRICAL_DIFFICULTY_CLAIMS = 0
BADGE_TEXT_LEGIBLE_AT_FINAL_SIZE = PASS
BADGE_COLOR_ONLY_ENCODING = 0
```

If citation badges are used:

```text
SOURCE_BADGE_TO_LEDGER_LINK = PASS_n_OF_n
SOURCE_BADGE_BROKEN_GLYPHS = 0
SOURCE_BADGE_CUSTODY_MISMATCH = 0
```

---

## 16. Appendix B versus Challenge Ladders

Do **not** create another large hard/mixed appendix that duplicates Appendix B.

Keep the roles distinct.

### Appendix B = mixed transfer / audit

Purpose:

- topic/method labels hidden;
- broad independent transfer;
- exam-like selection pressure;
- answers only after the set;
- lighter or no scaffolding.

### Challenge Ladders = progression routing

Purpose:

- concept-specific progression;
- questions deliberately ordered by difficulty;
- mostly reuse existing Worked Bridges, Appendix A, Appendix B, and verified practice;
- add a new problem only when a required difficulty rung is missing;
- answer the question: **“What should I try next for this concept?”**

Therefore:

```text
APPENDIX_B = TEST_TRANSFER
CHALLENGE_LADDER = TRAIN_PROGRESSION
```

A Challenge Ladder may be an appendix, a route table, or integrated into Contents/Study Route. It does not need to be called Appendix D.

---

## 17. Challenge Ladder structure

For each high-value concept, aim for a sequence such as:

```text
D1/D2 ENTRY
-> D2 CORE
-> D3 STRATEGIC
-> D4 TRANSFER
-> D5 CHALLENGE (only if educationally useful)
```

Example:

```text
REPEATED ROOTS

D1  identify what “repeated” means
D2  discriminant=0 in a quadratic
D3  use f(r)=f'(r)=0
D4  repeated root + global root-count condition
D5  repeated root hidden inside composition/parameter constraints
```

Each rung should point to an existing item where possible:

```text
Repeated Roots                         [D1 -> D5]
D2  Worked Bridge ALG-Axx
D3  Appendix A Qxx
D4  Appendix B Bxx
D5  Optional challenge Cxx
```

Do not create five near-identical new questions solely to fill a table.

---

## 18. Challenge Ladder personalization

Combine authored difficulty with learner knowledge.

Example:

```text
CONCEPT = repeated roots
learner state = PARTIAL
```

Suggested route:

- skip D1 if secure prerequisite evidence exists;
- begin at D2/D3;
- if successful independently, move one rung up;
- if stuck on recognition, use Notice/Recall and one rung down or a Worked Bridge;
- after success, test a non-identical higher rung later rather than immediate identical repetition.

Student-facing language can be:

```text
START HERE -> NEXT -> STRETCH
```

while D1-D5 badges remain visible on the linked questions.

---

## 19. Topic/concept difficulty map

For reviewer/authoring QA, create a table such as:

| Topic | Concept | Entry | Core | Transfer | Ceiling | Current question coverage |
|---|---|---:|---:|---:|---:|---|
| Polynomials | Vieta | D1 | D2 | D4 | D5 | A-Q.. / B-Q.. |
| Polynomials | Repeated roots | D2 | D3 | D4 | D5 | Bridge / A-Q.. / B-Q.. |
| Sequences | AP | D1 | D2 | D3 | D4 | ... |

This is a progression map, not a claim that every topic must reach D5.

Some concepts naturally top out at D3/D4 for the declared syllabus.

---

## 20. Domain-specific difficulty anchors

The D1-D5 names stay portable, but every domain profile should define examples.

### Mathematics anchor pattern

- `D1`: direct identity/formula or obvious substitution;
- `D2`: familiar method with short execution;
- `D3`: hidden method choice / representation shift;
- `D4`: multiple mechanisms, non-obvious transformation, proof/branching;
- `D5`: deep Olympiad synthesis/high transfer.

### Physics anchor pattern

A future Physics profile may use:

- `D1`: direct law substitution with explicit system;
- `D2`: multi-step calculation with standard diagram/model;
- `D3`: choose system/principle and construct representation;
- `D4`: combine principles, model assumptions, constraints, graphs, or frames;
- `D5`: novel modelling/synthesis with non-obvious invariants/approximations or proof-like reasoning.

### Chemistry anchor pattern

A future Chemistry profile may use:

- `D1`: direct definition/equation/standard conversion;
- `D2`: routine stoichiometric/reaction application;
- `D3`: select representation, combine two ideas, or infer hidden species/constraint;
- `D4`: multi-concept equilibrium/stoichiometry/structure reasoning;
- `D5`: unfamiliar synthesis with subtle competing constraints or proof-like justification.

These are seed anchors only. A real Physics/Chemistry domain profile should refine them using its syllabus and problem corpus.

---

## 21. Difficulty calibration audit

Before finalizing a domain edition, inspect:

1. Are D1-D5 anchors internally consistent?
2. Does increasing difficulty reflect recognition/representation/integration demand rather than bigger arithmetic?
3. Are nearby questions in the same concept ordered sensibly?
4. Are D5 labels rare enough to retain meaning?
5. Are foundational high-priority D1/D2 skills visibly important even though they are not hard?
6. Are broad topics shown as ranges rather than misleading single levels?
7. Are learner-specific weaknesses stored separately from authored difficulty?
8. Are exam-simulation pages free from pre-attempt metadata if the badge would alter authentic strategy?

Recommended gates:

```text
DIFFICULTY_SCHEMA = D1_TO_D5_ANCHORED
QUESTION_DIFFICULTY_COVERAGE = PASS_n_OF_n
TOPIC_DIFFICULTY_RANGE_COVERAGE = PASS_n_OF_n
CONCEPT_DIFFICULTY_PROGRESSION = PASS_n_OF_n
CHALLENGE_LADDER_ORPHANS = 0
APPENDIX_B_CHALLENGE_LADDER_ROLE_COLLISION = 0
```

---

## 22. Badge rendering and PDF QA

Difficulty and citation badges are small but learner-facing; treat them as real production elements.

During PDF QA:

- inspect badge legibility at final reading size;
- ensure the badge never collides with long question titles or figures;
- verify grayscale readability;
- verify all internal source-badge hyperlinks if generated;
- ensure repeated badges align consistently across pages;
- ensure topic-band badges do not look like question-level point scores;
- inspect at least one dense page with question ID + difficulty + source badge + local hint/figure to confirm metadata does not overwhelm the mathematics.

If a badge is unreadable at 200-dpi rendered final size, it fails.

---

## 23. Final principles

For difficulty:

> **Difficulty should be visible, simple, and honest: a badge for the learner, a richer profile for the author.**

For citations:

> **Provenance should be one tap/lookup away, not a paragraph beside every problem.**

For progression:

> **Appendix B tests transfer; Challenge Ladders tell the learner what difficulty rung to attempt next.**

For portability:

> **Keep the orchestration generic; put domain reasoning inside domain profiles.**
