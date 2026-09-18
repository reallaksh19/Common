# Primary Mathematics V2 — Human Review Rubric

## Purpose

Machine validation proves consistency and custody. It does not prove that a Grade 4–5 learner can actually learn from the material.

This rubric is applied to the **exact rendered candidate** after machine acceptance. Reviews must be bound to artifact digests and may not be synthesized from test fixtures.

## Required review dimensions

### H1 — Subject correctness

Reviewer asks:

- Are mathematical statements, examples and solutions correct?
- Do visual representations preserve the intended mathematical relationships?
- Are units, scales, remainder interpretations and equivalence claims correct?
- Do worked algorithms preserve place value?
- Are source-derived questions/diagrams represented faithfully where required?

Release-blocking examples:

- visually plausible but mathematically false fraction partition;
- missing internal quotient zero;
- bar chart scale inconsistent with data;
- unit conversion silently omitted;
- written algorithm numerically correct but place-value explanation false.

### H2 — Pedagogical design

Reviewer asks:

- Does the explanation move from meaningful representation toward abstraction rather than beginning with rules?
- Does each major visual do instructional work rather than decorate the page?
- Are representation changes purposeful and connected?
- Is scaffolding faded rather than permanently attached?
- Is a supported attempt followed by a genuinely fresh independent attempt?
- Are misconceptions treated as bounded hypotheses rather than learner labels?

### H3 — Assessment and practice design

Reviewer asks:

- Do practice batches test more than repeated number substitution?
- Does `CHOOSE` actually discriminate structures/operations?
- Does transfer vary context, representation or unknown position deliberately?
- Do solutions remain distinct from hints?
- Are unsupported independent items available for evidence?
- Are answer forms correct for remainder/context questions?

### H4 — Visual usability

Reviewer inspects rendered pages at normal A4 print/read size.

Blocking concerns include:

- text or diagrams too small for the intended child;
- visual crowding / excessive panels;
- diagrams whose labels collide or cannot be traced;
- colour carrying meaning that disappears in grayscale;
- insufficient response/work space;
- decorative art competing with mathematical structure;
- multi-step algorithms presented mainly as prose;
- source or notebook work too small to inspect.

### H5 — Child usability

Reviewer applies the cold-start child-facing question:

> Could a typical learner in the target Grade 4–5 range understand what to look at, what to do, and where to work without an adult reading paragraphs aloud repeatedly?

Check:

- one dominant cognitive job per page/spread;
- short, functional child language;
- visible learner action;
- enough whitespace;
- obvious route from model to example to attempt;
- adult diagnostic terminology excluded from student pages.

### H6 — Mature design quality

This gate is comparative and holistic. It may run only after H1–H5 pass.

Reviewer asks:

- Does the product feel intentionally designed rather than mechanically assembled?
- Are typography, spacing, component language and visual conventions coherent across topics?
- Do multiplication, division, fractions, measurement and geometry feel like one product system without becoming visually monotonous?
- Does the product preserve Primary simplicity while retaining mathematical depth?

## Review state

Each dimension uses:

```text
NOT_RUN
PASS
FAIL
BLOCKED
```

A machine/AI pre-review may record findings but cannot assign a human `PASS`.

## Exact-artifact binding

Every real review receipt must bind:

```text
candidate_id
core1_sha256
core2_sha256
review_dimension
reviewer / review authority
review_date
state
findings
```

If either PDF changes, the previous visual/pedagogical review no longer certifies the new bytes.

## Recommended representative pages

Human reviewers should not inspect only the cover and first lesson. At minimum inspect pages containing:

- place-value/regrouping;
- multiplication area → algorithm bridge;
- division sharing/grouping;
- internal quotient zero;
- remainder-context interpretation;
- fraction equivalence;
- decimal representation;
- measurement/unit chain;
- perimeter/area distinction;
- geometry/angle visual;
- chart/data visual;
- notebook/source-work replay;
- Core2 H1/H2/H3 sequence and fresh retry;
- Appendix C quick-reference page.

## Prohibited shortcut

`CI_GREEN == MATURE_PRIMARY_PRODUCT` is always false.