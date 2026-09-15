# External question record and anti-drift contract

## Extraction record

Capture `id`, `source_document`, `source_sha256`, `source_page`, exact `source_url`, `source_locator`, `raw_stem`, `values_units`, all `options`, `figure_locator`, `figure_semantics`, `raw_answer`, exam/year/session verification state, `primary_concept`, prerequisite concepts, `difficulty_source`, adaptation status and `target_ids`. For externally sourced records, the document hash is a lowercase 64-character SHA-256 and the page is one-based. These raw fields are immutable source facts; adaptations belong in the publication question and are described by `adaptation_note`.

Keep these axes independent:

- `state`: corpus workflow state (`ORIGINAL` or `SOURCE_RECONCILED`);
- `source_status`: publication treatment (`ORIGINAL`, `SOURCE_VERIFIED` or `ADAPTED`);
- `provenance_class`: source authority, using the shared master-schema vocabulary;
- `transcription_status`: transcription fidelity, null for original authoring;
- `difficulty_source`: `AUTHOR_HEURISTIC`, `SOURCE_ANALYSIS`, `EXPERT_CALIBRATED` or `EMPIRICAL`.

No axis may be inferred from another. In particular, `SOURCE_VERIFIED` does not determine provenance, and a provenance class does not prove transcription fidelity.

Classify dependencies NONE, GRAPH, DIAGRAM, TABLE, TIMELINE, NUMBER_LINE, OPTION_FIGURES, STATEMENT_SET or MIXED. Preserve axes, origins, negative regions, scales, units, arrows and all option semantics. A solution saying “Option D” without D's meaning is incomplete. If options are missing, flag the source; transparently adapt only with authorised scope, never invent them.

## Worked example of hint separation

Original demonstration problem: velocity is +4 m/s from 0–2 s and −2 m/s from 2–5 s. Find displacement and distance.

- H1: Notice the duration of each horizontal segment.
- H2: Divide the graph into two rectangles on opposite sides of zero.
- H3: Start the first signed area with (+4) × (2 − 0).

Keep the full values +2 m displacement and 14 m distance in the final solution. The method explains that the second width is 5 − 2 = 3 s, giving changes +8 m and −6 m, then distinguishes signed sum from total path. Show the graph again in the solution. Do not combine all three hints into a paragraph that includes the answer.

## Corpus ledger

Use `expected_ids` fixed before layout, `scope`, `source_snapshot`, `records` and `claim`. For each record store every extraction field above, the five independent state axes, `dependency`, `question_representation`, `solution_representation`, `hints` with h1/h2/h3, `solution` with why/method/answer/keep, `links_closed`, and `editorial_issue`.

For a real source-complete claim, expected and recorded IDs must match exactly; every state must be SOURCE_RECONCILED; metadata must be verified; URLs present; dependencies closed; hints distinct; solution components present; links closed; no editorial issue. This machine check validates records, not the truth of a verification checkbox. Manually compare records to source pages and published PDF.

For an original layout demonstration use `claim=PILOT_ORIGINAL`, `state=ORIGINAL`, `source_status=ORIGINAL`, `provenance_class=ORIGINAL_CALIBRATED`, null `transcription_status`, and `difficulty_source=AUTHOR_HEURISTIC`. Keep external document hash/page null and source URL empty. Do not set exam verification true. A pilot may demonstrate the workflow without claiming any official or platform attribution.

## Review loop

For each bounded set: compare source wording and figure → extracted record → question page → optional hints → standalone solution. Check copy/paste mismatches, missing conditions, answer leakage and formula-only methods. Recompute independently before accepting the source answer; record suspected source defects instead of silently repairing them. Inspect graph-heavy and longest-hint pages at full size. Freeze the final ledger/model/PDF hashes only after repairs. Run `reconcile.py <ledger.json> <published_model.json> <artifact.audit.json>` for the final artifact so the audit's model hash proves which exact model was rendered; omission of the audit is allowed only for pre-render model checks.
