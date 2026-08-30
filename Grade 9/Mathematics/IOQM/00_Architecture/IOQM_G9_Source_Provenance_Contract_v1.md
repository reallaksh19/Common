# IOQM Grade 9 — Source & Provenance Contract v1

Status: `SOURCE_BASELINE_V1`

## 1. Source hierarchy

### S0 — Current official competition authority

Use for eligibility, current exam pattern, current competition scope and official notices.

Primary entry points:

- IOQM/MTA(I): `https://ioqm.mtai.org.in/`
- HBCSE Mathematical Olympiad stages: `https://olympiads.hbcse.tifr.res.in/about-olympiads/stages/mathematical-olympiad/`
- HBCSE Mathematical Olympiad brochure 2025–26: `https://olympiads.hbcse.tifr.res.in/wp-content/uploads/2025/09/Brochure-Maths-Olympiad-2025-26.pdf`

Important curriculum statement:

This repository adapts IOQM for a Grade IX learner. It must not call the resulting taxonomy an official separate “Grade 9 IOQM syllabus.”

### S1 — Official/validated question papers and answer keys

Canonical HBCSE past-paper index:

`https://olympiads.hbcse.tifr.res.in/how-to-prepare/past-papers/`

Frozen initial corpus:

#### IOQM 2025 — September 7, 2025

Question paper:

`https://olympiads.hbcse.tifr.res.in/wp-content/uploads/2025/10/en.M1.pdf`

Final answer key:

`https://olympiads.hbcse.tifr.res.in/wp-content/uploads/2025/10/final-key-7th-September.pdf`

Key status: `FINAL_OFFICIAL`

Paper evidence from the official paper: 30 questions, 3 hours, 100 marks; Q1–Q10 carry 2 marks, Q11–Q20 carry 3 marks, Q21–Q30 carry 5 marks; integer answers 00–99; no negative marking.

#### IOQM 2024

Question paper:

`https://olympiads.hbcse.tifr.res.in/wp-content/uploads/2025/04/ioqm-2024-english.pdf`

Answer key:

`https://olympiads.hbcse.tifr.res.in/wp-content/uploads/2025/04/ioqm2024-answerkey.pdf`

Key status: `OFFICIAL_HBCSE_KEY`

#### IOQM 2023

Question paper + answer key:

`https://www.mtai.org.in/wp-content/uploads/2023/09/IOQM_Sep_2023_Question-paper-with-answer-key.pdf`

HBCSE links this paper from its official past-paper page.

Key status: `HBCSE_LINKED_MTAI_EMBEDDED_KEY`

## 2. Stable historical question ID

Every historical item uses:

`IOQM-YYYY-QNN`

Examples:

- `IOQM-2025-Q24`
- `IOQM-2024-Q17`
- `IOQM-2023-Q29`

Do not create alternate IDs based on internal topic number, page or agent.

## 3. Required question-level metadata

Every historical question record must include:

```yaml
item_id: IOQM-YYYY-QNN
source_year: YYYY
source_question_number: NN
source_paper_url: ...
source_key_url: ...
source_authority: ...
key_status: ...
question_mark_value: 2|3|5|UNKNOWN
primary_domain: NT|ALG|GEO|COMB
main_topic_id: IOQM-G9-...
secondary_domains: []
mechanisms: []
visible_clues: []
hidden_invariant: ...
first_move: ...
prerequisites: []
decision_boundaries: []
figure_required: true|false
source_integrity_status: ...
student_use_disposition: ...
teacher_use_disposition: ...
```

## 4. Source-integrity statuses

Use at least:

- `CLEAN_OFFICIAL`
- `CLEAN_VALIDATED`
- `TYPOGRAPHIC_AMBIGUITY`
- `KEY_CORRECTED`
- `KEY_STATUS_UNRESOLVED`
- `SOURCE_CONFLICT`
- `FIGURE_DEPENDENT`
- `PARTIAL_TRANSCRIPTION`
- `BLOCKED`

Do not silently convert a source defect into a clean exercise.

## 5. Key custody rule

Always distinguish:

- paper as printed;
- provisional key, if any;
- final/official key;
- independent mathematical verification.

If a final official key supersedes a provisional key, record both roles rather than rewriting history.

## 6. Historical wording and student use

The repository may use historical questions for:

- exact source-ledger custody;
- teacher analysis;
- mechanism classification;
- source-to-concept mapping;
- authorized student PYQ practice where the project explicitly permits it.

For newly authored teaching material:

- do not pretend author-created items are historical PYQs;
- do not invent year/question attribution;
- preserve source links and IDs when a historical mechanism is cited;
- keep author-created foundation/transfer items distinctly labelled in metadata.

Recommended author-created provenance:

- `AUTHOR_CREATED_FOUNDATION`
- `AUTHOR_CREATED_RECOGNITION`
- `AUTHOR_CREATED_TRANSFER`
- `AUTHOR_CREATED_MASTERY`

## 7. Primary vs secondary mechanism

A question may involve multiple domains, but recurrence/practice analysis must avoid double inflation.

Each historical question has exactly one `primary_domain` and one `main_topic_id` for primary counting, plus optional secondary/bridge tags.

If a future analysis needs genuinely multi-primary classification, define that denominator explicitly rather than silently double-counting.

## 8. Recurrence policy

Three-paper recurrence is an operational training signal only.

Forbidden wording:

- “official IOQM weightage” unless an official source says so;
- “this chapter carries X%” from three historical papers;
- dropping official-syllabus mechanisms solely because they did not appear in the seed corpus.

Allowed wording:

- “appeared in X of the validated 2023–2025 primary classifications”;
- “high recurrence in the current three-paper training corpus”;
- “syllabus-supported but low/absent in the current seed corpus.”

## 9. Question-paper verification gate

Before a paper enters the normalized corpus:

1. confirm the whole paper is available;
2. confirm year/date identity;
3. confirm question numbering/total count;
4. confirm answer-key authority/status;
5. check whether alternate sets differ by order or content;
6. record figure pages/requirements;
7. record any known corrections;
8. independently recompute promoted answers before using them as teaching authority.

## 10. Initial corpus state

```text
IOQM_2023 = VALIDATED_BASELINE
IOQM_2024 = VALIDATED_BASELINE
IOQM_2025_SEP07 = VALIDATED_BASELINE_FINAL_KEY
CORPUS_QUESTION_COUNT = 90
QUESTION_LEVEL_TAGGING = REQUIRED_BEFORE_TAXONOMY_FREEZE
```

The source baseline is ready for architecture use. Full 90-question mechanism tagging remains a separate corpus-build task and must precede any quantitative recurrence freeze.