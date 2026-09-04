---
name: ioqm-grade9-study-guide-builder
description: Build or revise a Grade 9 competitive-exam study guide from repository material plus user-supplied questions/notes, with configurable learner knowledge, portable domain profiles, difficulty badges, challenge ladders, flexible T1-to-Tx readiness checks, source/citation badges, self-sufficiency audits, decision-first quick reference, and traceable visual/PDF QA.
---

# IOQM Grade 9 Study Guide Builder

## Purpose

Use this skill when the goal is not merely to collect solved questions, but to produce a **teacher-style study guide** that lets a Grade 9 learner with partial prior knowledge recognize and execute the methods needed for a supplied problem set.

This skill is deliberately different from a main-topic production package. It may synthesize several existing main topics into one revision/study guide, but it must preserve canonical topic ownership and must not silently create a new official syllabus.

The orchestration rules should remain portable enough that future domain profiles can specialize the same builder for Mathematics, Physics, or Chemistry without importing Mathematics-only method language into those domains.

## Mandatory v2 references

Before authoring or revising a production study guide, read:

`Grade 9/skills/ioqm-grade9-study-guide-builder/references/question-driven-self-sufficient-study-guide-skill-v2.md`

That reference is the detailed production contract for question-to-method matrices, stable skill IDs, orphan-method repair, progressive local hints, Visual Bridges, self-sufficiency gates, optional short-horizon navigation, and inspected PDF delivery.

Also read:

`Grade 9/skills/ioqm-grade9-study-guide-builder/references/difficulty-badges-portability-and-challenge-ladders-addendum.md`

That addendum defines the portable difficulty contract, learner-facing `D1-D5` question badges, topic/concept difficulty bands, compact citation/source badges, separation of authored difficulty from learner mastery/priority/empirical difficulty, and Challenge Ladders that train progression without duplicating Appendix B.

When the user provides learner-specific topic/subtopic/skill knowledge, or when short-horizon readiness routing is requested, also read:

`Grade 9/skills/ioqm-grade9-study-guide-builder/references/learner-knowledge-profile-and-readiness-addendum.md`

That addendum defines optional learner-knowledge input, specificity precedence, personalization without pruning the durable core, and flexible `T1 ... Tx` Quick Check selection. It overrides older fixed prior-knowledge percentages and fixed Quick Check counts for those fields only.

If **any** question, chapter, Worked Bridge, Appendix A/B item, Appendix C method family, Challenge Ladder, badge/icon system, or Navigator element has a visual requirement other than `VISUAL_NONE`, also read and apply:

`Grade 9/skills/ioqm-grade9-study-guide-builder/references/question-driven-self-sufficient-study-guide-skill-v2-visual-production-addendum.md`

The visual addendum is mandatory when triggered. A required visual is a teaching obligation, not optional polish.

When a domain profile exists, read it after the generalized contracts. A domain profile specializes the generalized rules; it does not weaken them. Learner-profile/readiness overrides may then specialize only learner knowledge and Quick Check selection.

Current profile example:

`Grade 9/skills/ioqm-grade9-study-guide-builder/references/algebra-question-driven-profile-v2.md`

## Portable module architecture

Think of the reusable system as one orchestrator plus domain-neutral contracts and domain profiles:

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

Keep orchestration generic. Put domain reasoning, representations, legality checks, and concrete difficulty anchors in domain profiles.

## Core student standard

If no learner-specific knowledge is supplied, assume the learner knows roughly 30–50% of the school-level background:

- familiar formulas may be remembered;
- routine exercises may be solvable;
- method recognition is inconsistent;
- nearby methods are confused;
- advanced Olympiad moves cannot be assumed.

If the user provides topic/subtopic/skill-wise knowledge, **do not flatten it into one global percentage**. Use the most specific relevant information for routing. Accept categorical, approximate-percentage, or natural-language input. Treat stated percentages as planning estimates unless they come from measured evidence.

Examples:

```text
Quadratics = strong
Polynomials / Vieta = strong
Polynomials / repeated roots = weak
Recurrences = 20%
ALG-EQ-04 = unknown
```

The durable guide should still remain self-sufficient for a partial-knowledge learner unless the user explicitly requests a personally pruned edition. Personalization changes the Navigator route, Quick Check selection, practice priority, challenge-ladder starting rung, and starting support level; it does not silently delete core teaching.

The guide must therefore teach **enough to recognize, start, execute, and check**, not merely name methods.

The learner path is:

**problem wording → recognized structure → legal method choice → first useful line → execution → checking.**

## Source roles

Classify every input before authoring.

### Authority source

Official/validated contest papers, frozen repository source maps, correction overlays, stable interfaces.

Use these for exact historical claims, answer custody and official-source statements.

### Comparison/practice source

User notes, coaching handouts, videos, DPP compilations, preparation routines, external question lists.

Use these to discover methods, teaching cues and practice coverage. Do not upgrade them to official authority.

### Internal quality benchmark

For Grade 9 mathematics, inspect:

`Grade 9/Mathematics/benchmarks/Quadratics_Assimilation_v2/README.md`

Use it as a quality comparator for:

- explanation completeness;
- missing-link repair;
- method contrast;
- attempt before answers;
- independence in starting unfamiliar problems;
- source/citation discipline;
- visual pedagogy;
- cover/index usability;
- final PDF quality.

Do not copy its wording, layout, exercises, typography, or diagrams.

## Required pre-authoring audit

Before writing the guide, create a question inventory / question-to-method matrix.

For every supplied question record at minimum:

- stable local question number;
- mathematical surface;
- primary method;
- secondary prerequisite;
- recognition cue;
- first useful line;
- enough execution detail to finish;
- likely half-knowledge misconception;
- legality/reversibility/admissibility checks where relevant;
- whether the current guide explicitly teaches the method;
- whether the current guide gives enough execution detail;
- planned teaching location;
- initial hint depth where hints are allowed;
- visual requirement;
- authored difficulty `D1-D5`;
- internal difficulty profile `K/R/M/E/I/B/T` and confidence;
- learner-relative risk when a learner profile exists;
- educational priority as a **separate** field;
- source/provenance ledger reference and source-status class.

Do not use one vague `difficulty` column without the anchored difficulty contract.

Keep these separate:

```text
DIFFICULTY != PRIORITY
DIFFICULTY != LEARNER_MASTERY
DIFFICULTY != FREQUENCY
DIFFICULTY != EMPIRICAL_ITEM_DIFFICULTY
```

When learner-specific input exists, also maintain enough internal mapping to know which topic/subtopic/skill is `UNKNOWN`, `NONE`, `WEAK`, `PARTIAL`, `STRONG`, or `SECURE`, and what evidence/source produced that state.

### Visual requirement fields

When a visual may matter, do not use only a loose note such as “diagram useful.” Apply the visual addendum and record:

- `visual_level = NONE / OPTIONAL / REQUIRED / SOURCE_REQUIRED`;
- visual teaching job;
- stable visual asset ID;
- visual form;
- what the learner should notice;
- placement layer(s);
- leakage risk;
- visual status.

A `REQUIRED` or `SOURCE_REQUIRED` visual must be traceable through:

**question/skill → visual obligation → asset → placement → rendered page → QA pass.**

### Orphan-method test

A method is **orphaned** if a student must already know a trick that the guide only names.

Examples:

- “use derangements” without defining/counting derangements;
- “use Burnside” without a small-symmetry path or Burnside explanation;
- “degree 2 means cycles” without the labeled cycle-count formula;
- “use generating functions” without explaining coefficient extraction;
- “alternate inequalities” without showing how to count a small alternating pattern.

No supplied question may retain an orphan method.

## Static self-sufficiency gate

A question passes only if the guide contains all required support:

1. **Prerequisite refresh** — the minimum background is stated or recalled.
2. **Recognition cue** — what in the wording/structure should trigger the method.
3. **First useful step** — an executable first mathematical line, construction, or representation.
4. **Execution bridge** — enough explanation to finish the method without an unnamed trick.
5. **Legality/common-error check** — the nearby wrong move is identified where relevant.
6. **Practice isolation** — the question itself does not leak the method or answer beyond the requested support level.
7. **Required visual support** — if `visual_level` is `REQUIRED` or `SOURCE_REQUIRED`, the visual must exist, be correctly placed, and pass final-size rendered QA.
8. **Difficulty metadata** — the authored `D1-D5` level is assigned consistently and is not confused with priority or learner mastery.
9. **Provenance metadata** — source status and ledger mapping are preserved even if only a mini source badge is shown to the learner.

Record:

`STATIC_CONTENT_SELF_SUFFICIENCY = PASS_n_OF_n`

only when every supplied question passes.

This gate evaluates the durable document, not the learner's stated percentage. A personalized route may skip secure topics in short-horizon mode without weakening the underlying core.

This is not classroom evidence. Keep actual learner success, timing, retention and psychometrics unclaimed unless observed.

## Subtopic grouping rule

Do not group by the source document's lot/order unless that order is pedagogically strong.

Group by dependency:

1. fundamentals;
2. direct applications;
3. restricted/conditional variants;
4. representation changes;
5. advanced structures;
6. mixed method selection.

For combinatorics, a strong default progression is:

- counting foundations;
- selections and logical restrictions;
- distributions/multisets;
- linear arrangements;
- relative order/rank;
- circular symmetry;
- graphs/matchings/colorings;
- recurrence/state;
- number-theoretic counting;
- pigeonhole/extremal;
- invariants/games.

For other domains, derive a comparable dependency order from the repository topic map and the domain profile.

## Learner-facing difficulty and source badges

Difficulty should be visible as a compact badge, not buried in reviewer metadata.

Question example:

```text
Q17                         [D4 ADVANCED] [SRC 7]
```

Topic example:

```text
POLYNOMIALS                         [D2 -> D5]
```

Narrow concept example:

```text
Repeated roots                      [D2 core | D4 transfer]
```

Rules:

- every ordinary learner-facing practice question receives a `D1-D5` badge unless a clean exam simulation/facsimile intentionally hides it;
- broad topics use a range/band rather than one misleading difficulty value;
- narrow concepts may show core-to-transfer range;
- the difficulty badge is a small pill/stamp in the header and is never part of the mathematical statement;
- do not rely on color alone; always print the D-code;
- do not use star ratings;
- a source badge such as `[SRC 12]` may point to the source/provenance ledger instead of printing a long citation beside the problem;
- in a digital PDF, source badges should hyperlink to the ledger when practical;
- use a vector icon or text fallback, never an emoji-only icon dependency;
- keep badge density low: question ID + difficulty + source is normally enough.

The source badge is a shortcut to provenance, not a substitute for the full ledger.

## Learner-facing style

Write like a strong teacher, not like an internal production system.

Prefer:

- “What should I notice?”
- “Why this works”
- “Try this first”
- “Common mistake”
- “When this method is not appropriate”
- “Check”
- short worked examples

For progressive hints, learner-facing labels may be:

- **Notice**;
- **Recall**;
- **Start**.

Internal QA may call these H1/H2/H3, but do not make opaque `H1/H2/H3` codes the main learner-facing language.

Avoid learner-facing internal terms such as:

- wave;
- microstream;
- RMSEC;
- transfer gate;
- control plane;
- interface owner;
- raw priority equations;
- psychometric-sounding readiness percentages unless actually measured.

Internal QA documents may use technical production terminology when necessary.

## Worked-example rule

For every non-routine method needed by the supplied questions, include at least one **non-identical worked example**.

The example should reveal the mechanism without becoming a disguised copy of the appendix question.

If the representation itself is the hidden method, the worked example must include the corresponding required visual at the point where the representation is introduced.

## Visual pedagogy rule

Figures are teaching tools, not decoration.

Use visuals when they materially reduce cognitive load or expose a structure that prose hides: graphs, constructions, blocks/gaps, state diagrams, number lines, exponent grids, symmetry/orbit models, case-overlap schematics, tables, or other exact mathematical representations.

When visuals are triggered:

1. create a Visual Obligation Register before final layout;
2. write an asset brief for every required visual;
3. prefer deterministic/vector/programmatic construction when exact mathematical relationships matter;
4. do not use generative illustration as authority for exact geometry, graph topology, coordinate intersections, mathematical labels/equations, or source-required contest figures;
5. place the first useful visual where the representation is first taught, not only in a later gallery;
6. use quieter variants in Appendix A when they help recognition without leaking the solution;
7. preserve transfer integrity in Appendix B — method-revealing visuals normally belong after the attempt unless the problem itself requires the figure;
8. use retrieval micro-models in Appendix C for high-value visually driven method families;
9. do not show method-revealing routers before an unaided short-horizon diagnostic;
10. render and inspect every required visual and badge/icon system at final size.

A decorative image never satisfies a required visual obligation.

## Appendix contract

### Appendix A — supplied questions

If the user explicitly asks for **strict questions-only**, that instruction overrides the default local-hint presentation:

- reproduce every supplied question;
- remove solutions, tips, source commentary, local hints, and module-position notes from the appendix;
- preserve all mathematical conditions and source-required figures needed to solve the question;
- place the answer key only after the final question.

Otherwise, for the partial-knowledge learner profile, use the detailed v2 contract's adaptive local hint model where appropriate:

- **Notice** — recognition clue;
- **Recall** — readable prior skill + stable ID;
- **Start** — first executable move without solution leakage.

Required local visuals may sit with the question/Notice strip when they reduce recognition load, but must not reveal more than the assigned support depth.

Maintain source/provenance in a separate citation ledger; use a compact source badge on a question when useful.

### Appendix B — audit / mixed transfer

Create a fresh mixed mock set when requested or required by the domain profile.

Rules:

- label author-created items clearly;
- model method balance on verified historical repository patterns;
- do not claim an official Grade-9-only IOQM paper exists;
- include methods underrepresented by the supplied attachment but present in the canonical curriculum;
- hide topic labels where transfer is being tested;
- answers only after the final mock question;
- independently recompute every answer;
- include a problem-essential figure with the problem when necessary;
- keep method-revealing rescue visuals out of the pre-attempt page unless explicitly requested.

Appendix B is the **mixed independent transfer/audit set**. Do not create another large “hard mixed problem appendix” with the same job.

### Appendix C — decision-first quick reference

Create a compact decision-first memory helper, usually 1–3 pages depending on the domain.

Start with:

**What do I see? → What should I draw/write first? → What must I check?**

Then include only material worth recalling quickly:

- compact method triggers;
- core formulas after method choice;
- common legality/equality conditions;
- high-value transforms;
- final pre-submit checklist;
- stable IDs in secondary type where useful.

If the domain contains high-value visually driven method families, Appendix C must include small retrieval micro-models where they beat another sentence: gaps, blocks, circle identity, graph, state arrows, residue cycle, exponent grid, root/tangency sketch, similarity/cyclicity configuration, etc.

Do not put full worked solutions in the handout.

### Challenge Ladders — progression, not another problem bank

Challenge Ladders answer:

> **What should I try next for this concept?**

They are concept-specific progression maps and should mostly reuse existing Worked Bridges, Appendix A questions, Appendix B questions, and verified practice.

Typical progression:

```text
D1/D2 ENTRY -> D2 CORE -> D3 STRATEGIC -> D4 TRANSFER -> optional D5 CHALLENGE
```

Add a new problem only when an educationally important difficulty rung is missing.

Keep roles distinct:

```text
APPENDIX_B = TEST_TRANSFER
CHALLENGE_LADDER = TRAIN_PROGRESSION
```

A Challenge Ladder may be an appendix, a route table, or part of Contents/Study Route. It does not need to be called Appendix D.

When learner knowledge exists, start the learner at the lowest rung that is still informative rather than forcing every learner through D1.

## Optional short-horizon Navigator

When the learner has only a few days, apply the detailed v2 Navigator rules, the difficulty addendum, and the learner-profile/readiness addendum when applicable.

The student-facing interface should remain simple:

- Quick Check uses `T1`, `T2`, ... `Tx` rather than colliding with corpus `Q1`, `Q2`, ...;
- `x` is derived from the learner profile, high-value unknown/weak/partial families, time budget, page fit, and any explicit user count;
- if no learner profile is supplied, use the domain's default Quick Check bank/count;
- score recognition before exposing method cues or visual routers;
- use readable `DO FIRST / DO NEXT / QUICK RETEST / ONLY IF TIME` routing;
- use plain-language `Notice / Recall / Start` repair;
- keep internal diagnostic codes and priority equations out of the child-facing pages;
- do not waste T-slots repeatedly testing explicitly secure families unless a mixed spot-check is useful;
- use difficulty badges as supporting metadata only; never route by “hardest first”;
- no major new core skill on Day 3;
- protect normal sleep rather than prescribing late-night new theory.

The governing architecture remains:

**Navigator = where to go. Core = how to do it.**

## Citation and provenance rule

Provide citations wherever useful, but do not contaminate a strict questions-only appendix with long source prose.

Preferred full-provenance locations:

- source/citation ledger;
- chapter endnotes;
- teacher/reviewer manifest;
- stable historical ID references.

At point of use, a compact source mini-badge such as `[SRC 12]` may link/jump to the ledger entry. For author-created items use a compact `AC` marker only when the distinction matters to the learner; otherwise preserve author-created status in the ledger.

For a comparison source, preserve its uncertainty. Never turn “identified practice problem” into “confirmed official lecture question.”

## Independent cross-check

Before finalizing:

1. every supplied question appears exactly once in Appendix A;
2. no inline answers appear before the Appendix A answer key;
3. every Appendix A question maps to a taught method;
4. every non-routine method has an execution bridge;
5. every `REQUIRED`/`SOURCE_REQUIRED` visual has an asset, placement, and rendered QA pass;
6. no decorative figure is counted as pedagogical visual coverage;
7. Appendix B answer count matches question count;
8. every Appendix B answer is independently recomputed;
9. broader canonical curriculum gaps exposed by the source set are repaired or explicitly listed;
10. citations/source roles are recorded and every rendered source badge resolves to the correct ledger entry;
11. quick-reference content matches the main guide and carries micro-models for visually driven core families where appropriate;
12. no unsupported classroom-effectiveness claim is made;
13. when learner knowledge is supplied, the most specific topic/subtopic/skill evidence controls routing without pruning the durable core;
14. when a short-horizon Quick Check is used, its `T1 ... Tx` count and family coverage are justified by the selected scope/profile rather than copied blindly from a default edition;
15. every ordinary learner-facing practice question has an authored `D1-D5` difficulty badge unless a clean exam simulation intentionally hides it;
16. broad topics use difficulty ranges/bands rather than misleading single-number labels;
17. authored difficulty is not confused with priority, learner mastery, frequency, or empirical item difficulty;
18. Challenge Ladders do not duplicate Appendix B as another mixed hard set.

## Difficulty and badge gates

Recommended gates:

```text
QUESTION_DIFFICULTY_ASSIGNED = PASS_n_OF_n
QUESTION_DIFFICULTY_BADGES_RENDERED = PASS_n_OF_n
TOPIC_DIFFICULTY_BANDS_PRESENT = PASS_n_OF_n
CONCEPT_DIFFICULTY_PROGRESSION = PASS_n_OF_n
DIFFICULTY_PRIORITY_CONFLATION = 0
DIFFICULTY_MASTERY_CONFLATION = 0
UNSUPPORTED_EMPIRICAL_DIFFICULTY_CLAIMS = 0
APPENDIX_B_CHALLENGE_LADDER_ROLE_COLLISION = 0
BADGE_TEXT_LEGIBLE_AT_FINAL_SIZE = PASS
BADGE_COLOR_ONLY_ENCODING = 0
```

When source badges are used:

```text
SOURCE_BADGE_TO_LEDGER_LINK = PASS_n_OF_n
SOURCE_BADGE_BROKEN_GLYPHS = 0
SOURCE_BADGE_CUSTODY_MISMATCH = 0
```

## Hard visual gate

If any required visual remains only `PLANNED`, missing, broken, misplaced, unreadable at final size, mathematically incorrect, or too solution-revealing:

`PDF_GENERATION_ALLOWED = FALSE`

for a first final build, or:

`STATUS = VISUAL_REBUILD_REQUIRED`

for a rendered draft.

Use contact sheets for whole-book scanning, but inspect every critical required visual on its actual rendered page at final reading size.

Recommended visual gates when triggered:

```text
VISUAL_OBLIGATION_REGISTER = COMPLETE
VISUAL_OBLIGATIONS = PASS_n_OF_n
VISUAL_REQUIRED_ASSETS = PASS_n_OF_n
VISUAL_PLACEMENT = PASS_n_OF_n
CRITICAL_VISUAL_FINAL_SIZE_QA = PASS_n_OF_n
SOURCE_REQUIRED_FIGURE_CUSTODY = PASS_n_OF_n
ANSWER_FREE_VISUAL_LEAKAGE = 0
BROKEN_OR_MISSING_FIGURES = 0
VISUAL_ASSET_ORPHANS = 0
DECORATIVE_FIGURES_COUNTED_AS_COVERAGE = 0
```

## Required output set

A practical study-guide package should contain:

```text
README.md
<Subject>_Study_Guide_vN.md
Quick_Reference_or_Appendix_C.md
Appendix_A_<supplied-question-set>.md
Appendix_B_<mixed-transfer-set>.md
Challenge_Ladders.md or integrated challenge-ladder route table
Difficulty_Map.md or equivalent difficulty fields in the question matrix
Self_Sufficiency_Audit.md
Sources_and_Citations.md
QA.md
```

When meaningful visual obligations exist, also create:

```text
Visual_Obligation_Register.md or .csv
Visual_Manifest.md or .csv
Visual_Pedagogy_Audit.md
visuals/
```

For reusable agent operation create or maintain:

```text
Grade 9/skills/ioqm-grade9-study-guide-builder/SKILL.md
Grade 9/skills/ioqm-grade9-study-guide-builder/references/question-driven-self-sufficient-study-guide-skill-v2.md
Grade 9/skills/ioqm-grade9-study-guide-builder/references/learner-knowledge-profile-and-readiness-addendum.md
Grade 9/skills/ioqm-grade9-study-guide-builder/references/difficulty-badges-portability-and-challenge-ladders-addendum.md
Grade 9/skills/ioqm-grade9-study-guide-builder/references/question-driven-self-sufficient-study-guide-skill-v2-visual-production-addendum.md
Grade 9/skills/ioqm-grade9-study-guide-builder/references/domain-prompt-examples.md
Grade 9/skills/ioqm-grade9-study-guide-builder/references/self-sufficiency-audit-template.md
```

Read any available domain profile as part of the reusable authoring context.

## Completion language

Use:

`STATIC_CONTENT_SELF_SUFFICIENCY = PASS`

only for document-level coverage.

When visual obligations exist, do not call the final PDF visually complete until the visual addendum gates pass.

Keep these separate unless measured:

- classroom readability/timing;
- learner solve rate;
- retention;
- recognition accuracy;
- hint dependency;
- transfer success;
- psychometric calibration;
- qualification/pass-mark prediction.

## Final rule

A guide is not self-sufficient because it lists every formula, contains many pages, or looks professional.

It is self-sufficient only when the target learner can move from:

**problem wording → recognized structure → legal first step → executable method → correct check**

without needing an unnamed trick that exists only in the teacher's head.

If learner-specific knowledge is unavailable, use the partial-knowledge baseline. If it is available, personalize the route rather than pretending one global “50%” describes every topic.

Difficulty should be simple and visible to the learner but richer internally; provenance should be one badge/tap away rather than a paragraph beside every problem; Challenge Ladders should train progression without duplicating Appendix B.

When a representation is part of the method, the learner must also be able to **see the representation at the point of need**.
