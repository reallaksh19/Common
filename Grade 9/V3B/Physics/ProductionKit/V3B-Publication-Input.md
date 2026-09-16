# V3B Physics publication input and commands

Run from any working directory, with Python 3.11 or newer. The host uses the standard library and the existing Physics evaluator; no network/model call occurs during publication. Read [the runtime map](V3B-Runtime-Map.md) for scope and limits.

```bash
python 'Grade 9/V3B/Physics/ProductionKit/run.py' publish \
  --plan /path/to/plan.json \
  --baseline /path/to/baseline.json \
  --source-root /path/to/frozen-sources \
  --out /path/to/new-publication

python 'Grade 9/V3B/Physics/ProductionKit/run.py' verify-publication \
  --publication /path/to/new-publication \
  --expected-basis ACCEPTED_BASIS_DIGEST
```

The successful publish response returns the exact basis digest. Keep it in the accepted work packet. A new output directory is required. Errors produce structured BLOCKED output and exit code 2; a partially constructed directory is never promoted as the finished publication. The temporary build is cleaned up on handled failures. A process crash may leave a temporary directory; it is not an accepted publication.

## Separate inputs

| Input | Contents |
|---|---|
| Baseline | `schema_version: 1.0.0`, topic/baseline IDs, selected A/B Cores, source-file IDs/relative paths/SHA-256 digests, buckets with intrinsic badges and prerequisite edges, obligations with required source atoms/Cores/object kinds, required source questions per Core |
| Frozen source JSON | ID, truthful ORIGINAL/ADAPTED/AUTHOR_CREATED classification, citation, atoms with original locators and values/units; complete supported question fields and optional scientific evaluator bindings |
| Authored plan | `schema_version: 1.0.0`, subject Physics, topic/title, exact baseline digest, practice control if applicable, products with units and typed content blocks |

IDs for atoms and content blocks are globally unique within the packet. Each unit binds an existing bucket. Each content block binds source atoms and obligations from that bucket. Every required atom must reach a declared object in each required selected Core. Every required object kind must be realized. This is structural evidence only: independent review must verify that the actual explanation teaches the obligation.

Each source question preserves `id`, `original_number`, `stem`, and optional string lists `subparts`, `options`, `conditions`. Those values must match the authored question exactly. Original numbering remains visible. Additional original-question fields are rejected until supported; this deliberately prevents silent loss of original figures or metadata. A generated question needs an author-created source record, not a fabricated official citation.

Supported scalar verification is declared on the frozen source question:

```json
{
  "verification": {
    "validator_id": "SPEED_FROM_COMPONENTS",
    "bindings": {"vx": "VELOCITY_X_ATOM", "vy": "VELOCITY_Y_ATOM"}
  }
}
```

The referenced atoms carry numerical values and units. Constant-acceleration families also require their model and axis convention in this source verification record. The authored answer supplies the candidate `numeric: {value, unit}`; the evaluator's expected result is not copied from that candidate. Absent or unsupported evaluators permit a visibly marked review draft with oracle NONE. Only the transcription is checked; learner-ready scientific acceptance remains pending. Existing supported evaluators still reject wrong results.

## Content blocks

Every block has `id`, `kind`, `source_atom_ids` and `obligation_ids`.

| Kind | Additional fields |
|---|---|
| TEXT | Nonempty `text` |
| EQUATION | `mathml`, either matching a frozen EQUATION atom or accompanied by a source-linked `transformation` record; `meaning`, nonempty `symbols` and `conditions` lists. Restricted native MathML tags; no scripts or arbitrary markup |
| QUESTION | Source ID/question ID, exact original fields, `family`, `learner_action`, `exposure_role`, optional hints/guidance, complete answer summary/steps/check and all subpart answers; optional numeric candidate whose verification status is explicit |
| FIGURE | `scene`; optional `placement: ANSWER` plus a question ID in the same unit, so a model drawing can remain after the attempt |

Vector scenes specify kind VECTOR, x/y atom IDs, unit, symbol, frame, x/y labels and caption. They render at equal coordinate scales with a bold vector symbol and an arrow from the origin. Zero vectors have a point instead of an invented direction. Canvas size follows the geometry within readable limits.

Graph scenes specify kind GRAPH, ordered pairs of atom IDs, x/y units, frame, labels and caption. The x domain must strictly increase. The default vertical axis includes zero; an optional source-bound `y_min_atom` chooses a different minimum and is explicitly labelled. A range that clips supplied points is rejected. Piecewise straight segments are the only graph interpolation supported in this version; do not use them to imply a curved model.

Only 2A/2B require `practice_control`. Use KNOWLEDGE with percentage, scope, evidence reference, date, calibration policy and support plan; OWNER_WAIVER with authorization reference, purpose and support plan; or DESIGN_PREVIEW with purpose when no personalization is claimed. The publisher cannot authenticate a waiver or measure learning. Purpose is STARTER, PRACTICE, REVISION or COMPETITION. Study-only requests do not consult this control.

## Files returned

Open `OWNER_BOARD.html` first. The folder contains one HTML document per selected Core, SVG figures, `evidence.json`, a file-digest `manifest.json`, exact input/source copies and a runtime/policy snapshot. Answers and hint ladders appear in a separate section; hints can be revealed individually in HTML. There is no learner-release command.

The snapshot supports relocation and regeneration with:

```bash
python runtime/Physics/ProductionKit/run.py publish \
  --plan inputs/plan.json --baseline inputs/baseline.json \
  --source-root inputs/sources --out /path/to/another-new-publication
```

This demonstrates deterministic command recovery, not a newly qualified agent. Full agent packets still require accepted/rejected authoring history, reviewed model rationale and current work-item custody from the governing packet contract.

## Reproducible engineering fixture

`tests/publication_fixture.py` builds a small author-created fixture with four A/B products, velocity and force vectors, a constant-acceleration answer and a temperature graph. It is an integration specimen, not a complete Grade 9 chapter or academic-quality acceptance. The committed proof archive includes its exact inputs and generated artifacts.

```bash
python -m unittest discover \
  -s 'Grade 9/V3B/Physics/ProductionKit/tests' \
  -p 'test_publication_host.py' -v
```

## Research-friendly adaptations

A changed equation form uses `transformation: {source_atom_id, reason, steps}`. The referenced original must be an assigned EQUATION atom; meaning, symbols and conditions remain required on the equation block. The original is retained. The transformed form and its reasoning are rendered with an explicit pending-review notice. This records a candidate derivation; it does not prove semantic equivalence or accept an author-supplied APPROVED label.

Hints may be omitted, empty, short or extended according to the task. Optional `guidance` is a nonempty list when supplied. Complete answer summary/steps/check and required subpart answers still apply. A full explanation may itself provide the appropriate help; academic review assesses sufficiency. Frozen Core2 ladders are not changed by this A/B publication rule.

`numeric_answers_compared` counts supported-oracle comparisons only. `unverified_numeric_transcriptions_checked` counts draft candidates checked only against their authored representation. `scientific_reviews_pending` counts recorded equation/numeric adaptations; it does not count every remaining academic obligation. Scientific notices remain visible in print CSS.

The earlier V3B-Publication-Proof.zip is a historical packet with its original runtime. Current behaviour is exercised by both test_publication_host.py and test_research_flexibility.py; run discovery with `-p 'test_*.py'`. See the research policy for exploratory work that precedes this structured publication command.
