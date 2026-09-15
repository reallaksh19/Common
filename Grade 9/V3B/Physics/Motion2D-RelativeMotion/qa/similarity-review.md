# Cross-Core reuse / similarity review — EXECUTED SELF_REVIEW

The executable method is published in `qa/run_similarity.py`; raw result is `qa/similarity-results.json`.

Tokenizer and boundaries: Unicode NFKC → lowercase → `[a-z0-9]+` words → word 5-shingles. Blocks are blank-line prose paragraphs plus adjacent two-block windows. Registered frozen Core2 source blocks, canonical equation/definition metadata, headings/anchors/diagram tags, engineering question-record/attribution/intrinsic-scope metadata and blocks shorter than eight words are excluded from **prose duplication statistics** but remain subject to their own fidelity checks.

For shingle sets S,T, Jaccard is `|S∩T|/|S∪T|` and containment is `|S∩T|/min(|S|,|T|)`. Empty sets are not comparable. Routing intervals are exactly `[0.65,0.80)` candidate, `[0.80,0.90)` review, `[0.90,1]` high-priority; containment `>=0.80` is reviewed for blocks of at least 50 words.

Actual final run: **0 lexical threshold-routed pairs; 0 short/exact prose duplicates.** This low count is **not** treated as proof of differentiation.

Structural review was run separately for the four declared Core2A→Core2B anchor revisits: `2A-Q02→2B-Q02`, `2A-Q06→2B-Q06`, `2A-Q08→2B-Q10`, `2A-Q12→2B-Q12`. Each changes target and learner action (reconstruction, invariant inference, error diagnosis or plan discrimination). All four remain `ALLOWED_REVISIT_NOT_INDEPENDENT_TRANSFER` and do **not** count among Core2B's eight fresh transfer tasks.

No embedding model ran. No semantic/embedding score is reported; no uncalibrated semantic threshold is claimed.
