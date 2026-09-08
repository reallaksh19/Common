# Student-First Question-Bank Layout

Use this reference whenever a source-grounded educational PDF is primarily a long question bank, transfer-practice book, exam-practice book, worksheet collection, or question-plus-solution publication.

The governing learner rule is:

> **The student should experience one bounded study set at a time, not the total page count of the book.**

A technically compact publication can still feel overwhelming if every question consumes a page, global pagination dominates the interface, hints are visually exposed before the learner attempts the problem, or solutions appear without enough question context.

## 1. Chunk the book into bounded study sets

Do not present a long question bank as one continuous stack of hundreds of pages.

Prefer:

- 6-10 questions per study set when question difficulty is mixed;
- fewer questions for graph-heavy or D4/multi-step sets;
- a visible `SET n / N` identity;
- set-level progress rather than constant emphasis on total book pages;
- a short set title such as `Average speed & velocity` or `Graphs & representation`;
- question-page counters such as `Set 2 - question page 1 of 3` rather than psychologically heavy global page counts.

The learner should be able to answer: **What do I need to finish now?** without scanning the whole book.

## 2. Let question complexity determine page density

Do not force every question into the same geometry.

Recommended defaults:

- `D1`: compact; usually 2 per page and sometimes 3 when wording is short and no figure is required;
- `D2`: usually 2 per page;
- `D3`: 1-2 per page depending on representation and work-space need;
- `D4`, graph-heavy, diagram-heavy, or long algebraic questions: full page or generous half-spread.

Working space counts as meaningful occupancy. Empty lower halves caused only by a rigid one-question-per-page template do not.

## 3. Student eye-path: question -> work -> optional hints

For practice pages, the visual order is mandatory unless the source pedagogy explicitly requires something else:

```text
QUESTION
-> WORK HERE / representation area
-> visual stop line
-> H1 NOTICE
-> H2 MODEL
-> H3 START
-> optional link to method check
```

Never place H1-H3 beside the question in a way that the student reads them accidentally before attempting.

Use a clear stop label such as:

`STOP - look below only if stuck. Read one hint at a time.`

The hint block belongs **below the work area**.

## 4. H1-H3 must become progressively more concrete

Do not make all three hints generic restatements.

### H1 - NOTICE

Identify the decisive observation or data interpretation. It may contain numbers already present in the question when that helps the learner notice what matters.

Examples:

- `The two legs are both 4 km, so their times are 4/3 h and 4/5 h.`
- `The second half uses equal times at 9 m/s and 15 m/s.`
- `During the one-second interval, Delta v = 50 m/s, so a = 50 m/s^2.`

H1 should not normally reveal the final answer.

### H2 - MODEL

Translate the observation into the model, intermediate quantities, or equations. Numerical intermediate values are allowed and often useful.

Examples:

- `Total time = 4/3 + 4/5 = 32/15 h; total distance = 8 km.`
- `T = V(1/alpha + 1/beta), so V = alpha beta T/(alpha + beta).`

### H3 - START

Give the exact calculation, equation, substitution, or first executable line from which the student can finish.

Examples:

- `Average speed = 8 / (32/15). Now simplify.`
- `S = 1/2 VT = alpha beta T^2/[2(alpha + beta)].`

H3 may be close to the solution because the learner has deliberately requested the strongest hint. It should still avoid unnecessary explanatory text once the starting line is clear.

## 5. Hint layout must tolerate mathematical detail

Because H1-H3 may contain fractions, symbols, and numerical intermediate steps:

- use stacked full-width hint rows by default;
- avoid narrow three-column hint layouts;
- reserve the hint region before placing work-space lines;
- use dynamic height based on wrapped text;
- never allow hint labels, equations, or body copy to collide;
- treat any overlap, clipping, or text spill as a release-blocking defect.

A visually elegant hint block that cannot safely hold real mathematical content is the wrong component.

## 6. Solutions must repeat enough of the question to orient the learner

Avoid an isolated heading such as `METHOD CHECK - SET 1` followed by solutions that require the learner to remember which problem they refer to.

Use a question-aware structure:

```text
CHECK YOUR METHOD - SET n

EX-... / Qn
QUESTION RECAP
<short but unambiguous question wording>

METHOD
<source-grounded worked route>

ANSWER
<final answer>

<- Return to question
```

The question recap may be shortened only when it remains unambiguous and does not alter data, conditions, or mathematical meaning.

## 7. Keep answers out of the main question card

If the source page currently exposes a worked route or final result while simultaneously instructing the learner to reveal hints progressively, recompose the publication so that:

- question data remain on the question page;
- H1-H3 remain optional and progressively stronger;
- full worked method/final answer moves to the solution section or answer layer;
- question -> solution and solution -> question links remain stable.

This is a presentation reconstruction, not deletion: the source solution remains present in the publication model.

## 8. Navigation should reduce perceived workload

Prefer learner-facing navigation such as:

- `Today: Set 3 / 8`;
- `4 questions - about 20-30 minutes` when duration is genuinely supportable;
- set progress bars;
- concept/subtopic labels;
- `After attempting: check method ->`.

Avoid making `127 pages`, `61 solutions`, or similar totals the dominant first impression. These may exist in metadata/audit pages but should not define the learner experience.

## 9. Compact does not mean cramped

Do not reduce font size or work space merely to minimize page count.

A compact student-first publication should gain efficiency through:

- grouping short questions;
- variable-height components;
- multi-solution pages;
- removal of repeated decorative dead space;
- set-based navigation;
- moving full solutions away from question pages.

It should not gain efficiency through 7 pt body text, tight leading, clipped equations, or insufficient work space.

## 10. Required student-first QA

In addition to the normal zero-loss and render QA, inspect every practice-page template for:

```text
question visible before hints = true
work area precedes hint block = true
H1/H2/H3 order = correct
hint progression becomes more concrete = true
numeric/math detail wraps without collision = true
question text overlaps = 0
hint text overlaps = 0
solution cards include question recap = true
solution-to-question return links resolve = true
question-to-solution links resolve = true
```

For long books, inspect representative short, medium, long, graph-heavy, and equation-heavy questions at normal reading size before scaling the template.

## 11. Anti-patterns to reject

- one question per page regardless of difficulty;
- three narrow hint columns containing equations;
- hints above or beside the work area where they are read accidentally;
- H1, H2, and H3 that all say essentially the same thing;
- hiding all numerical detail from hints even when an intermediate calculation is exactly what the learner needs;
- putting the final answer in H1;
- a solution page that says only `METHOD CHECK` without repeating the problem context;
- compressing a long question bank by shrinking typography rather than improving composition;
- large global page-count emphasis that makes the learner feel they must confront the whole book at once.

## 12. Prototype acceptance gate for question banks

Before full reconstruction, the approved prototype should include at least:

1. one compact D1/D2 two-question page;
2. one D3 question with meaningful work space;
3. one D4/graph-heavy full-page question;
4. stacked H1-H3 containing real numerical/mathematical detail;
5. one solution page containing question recaps, methods, answers, and return links;
6. a set-progress/navigation page or header;
7. rendered proof that no text overlaps or clips.

Once the user approves this pattern, scale the system while preserving source obligations and running the normal anti-drift and render-first audits.
