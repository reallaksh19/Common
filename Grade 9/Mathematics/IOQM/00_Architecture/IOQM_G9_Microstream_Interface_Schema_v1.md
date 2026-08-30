# IOQM Grade 9 — Microstream Interface Schema v1

Status: `MANDATORY_INTERNAL_INTERFACE`

Purpose: allow parallel agents to reduce work without fragmenting the student book.

A Wave-1 microstream must return a structured interface to the main-topic lead. It must **not** claim ownership of the final student chapter.

## 1. File naming

`<MAIN_TOPIC_ID>__W1-<LETTER>__<short-name>__interface.md`

Example:

`IOQM-G9-NT-02__W1-C__power-cycles__interface.md`

## 2. Required header

```yaml
main_topic_id: IOQM-G9-...
microstream_id: W1-X
microstream_title: ...
owner_role: RESEARCH_INTERFACE_ONLY
status: DRAFT|READY_FOR_LEAD|BLOCKED
canonical_teaching_owner: IOQM-G9-...
prerequisite_interfaces: []
source_cutoff: YYYY-MM-DD
```

## 3. Mandatory interface fields

### A. Scope boundary

State:

- included mechanisms;
- explicitly excluded neighbouring mechanisms;
- where canonical teaching ownership lies for overlaps.

### B. Learner-state model

```text
PRIOR_KNOWLEDGE:
LIKELY_HALF_KNOWLEDGE:
MISSING_BRIDGES:
OWNERSHIP_TARGET:
```

### C. Mathematical invariant / governing structure

One concise statement of the core mathematical idea.

Then provide derivation/proof or reconstruction sufficient for the lead to verify it.

### D. Representation inventory

For every useful representation:

| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|

### E. Decision boundaries

At least 3 for a small microstream; more where necessary.

| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|

### F. Misconception/diagnosis catalogue

For each misconception:

```text
ERROR_CODE:
WRONG_MOVE:
WHY_TEMPTING:
MISSING_LINK_CLASS:
REPAIR_INVARIANT:
FALSIFIER_OR_CONTRAST:
```

Missing-link classes:

- `PREREQUISITE`
- `RECOGNITION`
- `REPRESENTATION`
- `INVARIANT`
- `DOMAIN_CONDITION`
- `DISCRETE_FILTER`
- `EXECUTION`
- `SOURCE_INTEGRITY`

### G. First-move cues

For each visible clue, state only the minimum first mathematical object the learner should eventually write automatically.

Do not provide a whole worked solution where one line suffices.

### H. H3 -> H0 fading plan

Provide at least one fading track:

- H3 — execution relation;
- H2 — structure/representation cue;
- H1 — recognition clue;
- H0 — changed-surface independent item.

Candidate items must be independently checked.

### I. Validated IOQM source anchors

For each relevant historical question:

| Stable ID | Year/Q | Source status | Primary/bridge role | Mechanism | Figure? | Key status |
|---|---|---|---|---|---|---|

No source ID may be guessed.

### J. Source-independent mathematical trace

For every historical anchor promoted beyond mere mention, provide:

- independent solution outline;
- key numerical checkpoints;
- domain/parity/sign/degeneracy checks;
- whether official key agrees;
- unresolved source issue if any.

### K. Contrast-pair candidates

Provide at least 5 strong candidates for the main-topic lead, including at least one cross-microstream boundary if known.

### L. Transfer candidates

Provide T2–T4 candidate transfers:

- representation change;
- context change;
- discrete/continuous change;
- cross-domain bridge.

Label author-created items distinctly.

### M. Candidate mastery items

Provide, as appropriate:

- recognition-only;
- first-line-only;
- full solve;
- WHY-NOT;
- verification/source-integrity.

These are candidates. The lead decides which survive integration.

### N. Dependency declarations

List:

- concepts this stream `REQUIRES`;
- concepts it `BRIDGE_REQUIRES`;
- concepts it only `APPLIES`;
- concepts downstream streams may assume from this interface.

### O. Lead integration notes

Explicitly state:

- what should be taught once globally;
- what can be compressed into retrieval later;
- what overlaps another stream;
- what should **not** appear in student prose;
- where the stream should likely appear in dependency order.

### P. Independent QA status

```text
DERIVATIONS_CHECKED: PASS/PARTIAL/NOT_RUN
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS/PARTIAL/NOT_RUN
SOURCE_IDS_VERIFIED: PASS/PARTIAL/NOT_RUN
DEPENDENCY_CONFLICTS: NONE/list
OPEN_ISSUES: ...
```

## 4. Forbidden microstream outputs

A research agent must not:

- create its own final student PDF as the canonical topic artifact;
- declare the main topic publication-ready;
- introduce a new canonical notation without lead approval;
- repeat full teaching of an overlap concept owned elsewhere;
- infer official weightage from recurrence;
- silently repair a source question/key;
- create child GitHub issues unless the main-topic issue explicitly requires them.

## 5. Lead consumption contract

The lead may:

- discard interface content;
- merge multiple interfaces;
- change order;
- rewrite all prose;
- reduce duplicated examples;
- move a prerequisite earlier;
- create new bridges/contrasts;
- reject candidate items after audit.

The interface is evidence, not a frozen chapter.

## 6. Interface completion gate

`READY_FOR_LEAD` requires:

- scope boundary complete;
- learner-state model complete;
- derivation/invariant complete;
- decision boundaries complete;
- misconception catalogue complete;
- first-move cues complete;
- fading plan complete;
- source anchors verified;
- promoted answers independently checked;
- dependency declarations complete;
- no unresolved error affecting integration.

A lead must not treat a partially filled interface as authoritative merely because an agent says the stream is done.