# Core (1A) source completeness contract

Core (1A) may simplify language and improve teaching, but it must not silently drop source scope. Every source-visible item must be inventoried before publication and mapped to a learner-facing home.

## Why this exists

A polished textbook can still be incomplete. The publication build therefore uses a **Source Coverage Ledger** in addition to the Core (2) challenge-link map.

```text
SOURCE PDF
   ↓
SOURCE INVENTORY
   ├── heading / subtopic
   ├── concept / definition
   ├── equation / relation
   ├── derivation
   ├── worked illustration
   ├── figure / graph
   ├── formula-sheet item
   └── practice item
   ↓
CORE (1A) LEARNER HOME
   ↓
CORE (2) PRACTICE LINKS
```

No learner PDF is source-complete merely because its chapter headings look similar.

## Stable source item IDs

Every inventory row has a stable ID and one source locator. Example:

```json
{
  "source_item_id": "M2D-EQ-3.1.3-TIME-FLIGHT",
  "kind": "EQUATION",
  "source_locator": "§3.1.3",
  "learner_name": "Time of flight for same-height landing",
  "canonical_expression": "T = 2u sin(theta) / g",
  "valid_when": "ideal projectile; launch and landing at same height",
  "core1a_home": "2.4",
  "coverage_mode": "TEACH_AND_USE",
  "status": "PLANNED"
}
```

## Coverage modes

- `TEACH_AND_USE` — concept/equation must be explicitly explained and then used.
- `TEACH_VISUALLY` — source concept must have a visual explanation, not only prose.
- `WORKED_EXAMPLE` — source illustration/problem must have a worked learner treatment or an explicitly declared equivalent preserving the same reasoning demand.
- `REFERENCE` — formula-sheet item is retained as a reference after it has a teaching home.
- `STRETCH` — source-visible advanced material is kept as a visibly optional stretch topic.
- `SOURCE_LIMITATION` — the supplied source is clipped, missing, contradictory, or otherwise insufficient; do not invent missing content.

`SOURCE_LIMITATION` is the only allowed unmapped teaching state, and it must include a reason.

## Equation completeness

Every source equation gets an individual ledger row. Equations may not be covered only by appearing in an appendix. Each equation row must name:

1. the learner-facing concept that explains it;
2. the physical state/event that makes it valid;
3. where the equation is first derived or motivated;
4. at least one learner use (worked example, guided example, or Core (2) challenge);
5. any validity restriction.

For example, same-height projectile shortcuts must explicitly carry the equal-height condition. General component equations remain available for different launch/landing heights.

## Concept completeness

A source concept is not considered covered merely because its formula appears. A `CONCEPT` row requires:

- child-friendly explanation;
- physics word/definition where needed;
- at least one suitable representation;
- common confusion where the source or Core (2) shows one;
- question linkage when Core (2) tests the idea.

## Visual completeness

Source geometry, graphs, frame changes, vector relationships, or direction-dependent ideas require an illustration spec. A source figure may be redrawn, but the reasoning payload must be preserved.

The audit rejects difficult concepts marked D2/D3 when the learner home contains equations but no explanatory stages.

## Worked illustration completeness

Source illustrations are inventoried individually. An illustration may be replaced by a cleaner equivalent only if the following are preserved:

- problem family;
- decisive physical state/event;
- representation demand;
- governing relation;
- conclusion being taught.

Otherwise the source illustration remains a distinct learner item.

## Practice completeness

The source practice bank is inventoried separately from the teaching book. Core (2) owns challenge execution, but Core (1A) must prove that every challenge-relevant concept has a teaching home.

The Core (1A) → Core (2) map is therefore checked in both directions:

- every Core (2) challenge has at least one Core (1A) concept home;
- every assessed Core (1A) concept points to relevant Core (2) challenges;
- the concept names and equations used in Core (2) must exist in the source-coverage ledger or be explicitly classified as a source-visible extension.

## Build gates

Publication fails if any of these are true:

- a source subtopic has no Core (1A) home;
- a source equation has no equation row;
- an equation row lacks a validity condition when one is needed;
- an equation is present only in the formula sheet and nowhere taught;
- a source illustration is neither mapped nor explicitly classified;
- a D2/D3 visual concept has no staged illustration plan;
- Core (2) tests an idea with no teaching home;
- a learner page uses an equation that is absent from the source inventory and is not explicitly marked as an extension;
- the source has a visible limitation and the build silently fills the gap.

## Learner-facing language

The coverage machinery is internal. Learners see friendly navigation only:

- `Where you will use this`
- `Try Core (2)`
- `Need a quick refresher?`
- `Go back to this idea`
- `Easy mistake to make`
- `Does the answer make sense?`

They do not see implementation terms such as ledger, custody, repair, falsifier, or source-grounding.
