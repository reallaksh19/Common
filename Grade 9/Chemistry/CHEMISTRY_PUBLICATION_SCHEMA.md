# Grade 9 Chemistry Publication/Review Schema

This is the **subject-wide publication contract for Grade 9 Chemistry**. A chapter such as Redox is an instance of the schema, not the schema itself.

## Design goals

A Chemistry publication package must let a cold-start reviewer or agent answer, from repository state alone:

1. What supplied source is authoritative?
2. Which source obligations were extracted, where exactly did they come from, and where are they taught?
3. What external question corpus was frozen, how was every candidate classified, and where is every eligible question published?
4. What exact learner artifact bytes are under review, and can they be reconstructed deterministically?
5. Do PDF links, page bounds, typography, chemistry notation, answer-separation rules, and render evidence pass?
6. Which claims are technical PASSes versus independent pedagogy/classroom claims still PENDING?

## Package layers

```text
SOURCE AUTHORITY
  -> source-obligation ledger with page/region locators
  -> canonical learner units/concepts
  -> optional external-corpus ledger
  -> exact reviewed learner artifacts
  -> render/link/notation audit
  -> package validator
  -> draft PR review
```

## Required instance files

Every chapter/package instance has one `Chemistry_Publication_Package.json` that points to:

- a source-obligation ledger;
- an external-corpus ledger when external questions are in scope;
- one or more exact reviewed learner artifacts;
- deterministic artifact reconstruction information when binaries are stored as chunks or generated;
- text snapshots for in-PR inspection;
- link expectations where links are part of the product;
- render/chemistry QA evidence;
- review documentation.

## Source obligation contract

Each obligation has:

- stable `obligation_id`;
- exact `source_page`;
- human-meaningful `source_locator` or region;
- concise evidence summary;
- canonical primary learner unit;
- status.

A file hash alone is not enough: it proves source identity, not extraction fidelity.

## External corpus contract

Every frozen candidate is a record. Summary counters are **derived views** and must be recomputed by the validator.

Every eligible candidate requires:

- stable hash-based `candidate_id`;
- immutable provider/index/snapshot identity;
- direct source URL or exact source locator;
- full verified stem and options where applicable;
- answer used in publication;
- scope status/reason;
- exactly one primary learner unit;
- primary concept ID;
- transfer-book ID + question ID + page;
- difficulty + required hint depth;
- Appendix/full-solution status;
- source-link status;
- placement status.

Partial-scope candidates preserve the external dependency and source transcript but are not silently converted into in-scope PYQs.

## Reviewed artifact custody

Preferred order:

1. commit the PDF directly;
2. otherwise commit exact PDF bytes through deterministic text-safe chunks plus a manifest;
3. otherwise commit a deterministic canonical content model + renderer.

A fingerprint without recoverable bytes or a reproducible renderer is not sufficient for a formal technical PASS. A remote review mirror may improve draft reviewability but does not replace repository custody.

Each learner artifact also carries a plain-text review snapshot tied to the PDF hash so reviewers can search learner text, questions, hints and solutions in the PR diff.

## Chemistry publication QA

The validator must fail closed on:

- missing/reconstruction-failed learner artifacts;
- hash/page-count mismatch;
- out-of-page text geometry;
- configured minimum-font violation;
- wrong/missing external URI or invalid internal destination;
- failed chemistry notation probes;
- forbidden ASCII chemistry notation when the package disallows it;
- answer leakage onto configured attempt/question pages;
- source/corpus ledger inconsistency;
- missing placement/support fields for eligible external questions.

The package can separately record `agent_visual_review` and `independent_human_review`. Technical automation must not be presented as classroom validation.

## Exit codes

- `0`: package technical PASS.
- `1`: validation failure (schema/content/QA mismatch).
- `2`: blocking state such as missing reviewed artifact bytes or required manual gate.

There is no exit-code-0 blocked state.

## Chapter-agnostic rule

Redox-specific fields belong only in the Redox instance data. The schema/validator/skill must work for Atomic Structure, Periodicity, Chemical Reactions, Acids/Bases, Separation, or any other Grade 9 Chemistry package without code changes to concept names or fixed candidate counts.
