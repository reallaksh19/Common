# Grade 9 Chemistry Publication/Review Schema

This is the **subject-wide publication contract for Grade 9 Chemistry**. A topic or chapter such as Redox is an instance of the schema, not the schema itself.

## Non-negotiable learner deliverable contract

Every Chemistry **topic** that is taken up must produce exactly **two learner-facing PDF files**:

1. **Core Study Guide** — the teaching product, including Appendix A, Appendix B and Appendix C.
2. **ExamSIDE Solution & Transfer Book** — the external-question practice/solution product with progressive hints, transfer/badge metadata, concept segregation labels and complete solutions.

Do not create a third learner-facing handout PDF. The handout is mandatory **Appendix C inside the Core Study Guide**. Chapter-level master compilations may be generated later, but they do not replace the two required per-topic files.

### Core Study Guide required structure

The Core Study Guide contains the connected teaching narrative first, then three mandatory appendices:

- **Appendix A — Core Practice.** Independent/faded topic practice tied to stable concept IDs. It must include sufficient mixed and transfer-ready questions to verify the topic, without leaking the Appendix B solutions.
- **Appendix B — Core Solutions.** Complete reasoning solutions for every Appendix A question, with chemistry representation, units/charge/conservation checks where relevant, and explicit misconception repair when the question targets a known trap.
- **Appendix C — Printable Handout.** A detachable/printable revision handout for the topic. It must be usable without reading the main book at that moment and should compress the topic into the minimum useful learner reference: concept map/first moves, key rules and exceptions, required diagrams or symbolic patterns, common traps, and a short self-check. It must not become a dense answer sheet or introduce new chemistry.

Appendix C is **blocking**: a Core Study Guide without the handout is incomplete.

### ExamSIDE Solution & Transfer Book required structure

Each placed external question must remain attempt-first and carry structured support. At minimum each question record/render must expose:

- canonical question ID and provider/source/date or shift badge;
- original source link/locator;
- `primary_concept_id` and a visible **concept segregation label** identifying the primary concept separately from prerequisite/secondary concepts;
- difficulty badge;
- transfer badge (for example direct, representation-shift, multi-concept, far-transfer or cumulative, as configured by the topic); 
- scope/placement badge when needed for auditability;
- independent-attempt state (`H0`) before hints;
- progressive H1/H2/H3 support according to difficulty;
- question-specific concept helper and misconception watch when relevant;
- cross-link back to the Core Study Guide concept;
- complete conceptual solution in the same ExamSIDE PDF;
- Appendix/solution placement status and source-link status in the external-corpus ledger.

Hints must reveal progressively and must not collapse into the full solution. The ExamSIDE file is a practice-and-solution product, not a second copy of the Study Guide.

## Design goals

A Chemistry publication package must let a cold-start reviewer or agent answer, from repository state alone:

1. What supplied source is authoritative?
2. Which source obligations were extracted, where exactly did they come from, and where are they taught?
3. For every topic, are the two required learner files present and does the Core contain Appendix A, Appendix B and Appendix C?
4. What external question corpus was frozen, how was every candidate classified, and where is every eligible question published?
5. What exact learner artifact bytes are under review, and can they be reconstructed deterministically?
6. Do PDF links, page bounds, typography, chemistry notation, answer-separation rules, appendix boundaries and render evidence pass?
7. Which claims are technical PASSes versus independent pedagogy/classroom claims still PENDING?

## Package layers

```text
SOURCE AUTHORITY
  -> source-obligation ledger with page/region locators
  -> canonical learner units/concepts
  -> TOPIC DELIVERY CONTRACT
       -> Core Study Guide
          -> Appendix A Core Practice
          -> Appendix B Core Solutions
          -> Appendix C Printable Handout
       -> ExamSIDE Solution & Transfer Book
  -> optional external-corpus ledger
  -> exact reviewed learner artifacts
  -> render/link/notation/appendix audit
  -> package validator
  -> draft PR review
```

## Required instance files

Every chapter/package instance has one `Chemistry_Publication_Package.json` that points to:

- a source-obligation ledger;
- one or more topic-delivery records conforming to `schema/chemistry-topic-delivery.schema.json`;
- an external-corpus ledger when external questions are in scope;
- the exact reviewed learner artifacts;
- deterministic artifact reconstruction information when binaries are stored as chunks or generated;
- text snapshots for in-PR inspection;
- link expectations where links are part of the product;
- render/chemistry/appendix QA evidence;
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
- primary concept ID and concept-segregation label;
- transfer-book ID + question ID + page;
- difficulty badge + required hint depth;
- transfer badge;
- full-solution status;
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

- missing one of the two required topic PDFs;
- missing Appendix A, Appendix B or Appendix C in the Core Study Guide;
- Appendix C not being recognisable as the printable handout;
- missing ExamSIDE concept-segregation label, badges, hint support or complete solution for a required question;
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

Redox-specific fields belong only in the Redox instance data. The two-file topic contract, Appendix A/B/C contract, ExamSIDE support metadata and validator rules must work for Atomic Structure, Periodicity, Chemical Reactions, Acids/Bases, Separation, or any other Grade 9 Chemistry package without code changes to concept names or fixed candidate counts.
