# Chemistry Redox source hardening v1

This layer repairs source-scope overclaim in the original `CHEM-REDOX-OXIDATION` engineering gate without silently broadening Grade 9/10 learner scope.

## Finding

The v1 gate cited only **NCERT Class X Science Chapter 1 §1.2.5** while simultaneously claiming authority for oxidation-number rules, electron-transfer definitions, agent assignment and an acidic permanganate half-reaction. That is too broad for the cited source.

## Effective source split

| Tier | Authority | Authorized technical use |
|---|---|---|
| `FOUNDATION_G10` | NCERT Class X Science Ch. 1 §1.2.5 | oxidation/reduction foundation and textbook reaction examples such as `CuO + H2 -> Cu + H2O` |
| `FORMAL_G11` | NCERT Chemistry XI syllabus Unit VIII | electron transfer, oxidation number and formal redox identification/balancing |
| `EXTENDED_G11` | NCERT XI formal redox + exemplar practice | ionic half-reaction balancing such as permanganate systems when explicitly in scope |

The official NCERT Chemistry XI-XII syllabus states that Unit VIII covers oxidation and reduction, redox reactions, oxidation number, and balancing redox reactions in terms of electron loss/gain and oxidation-number change. Class XI Exemplar independently carries a dedicated Unit 8 `REDOX REACTIONS` problem set.

## Downstream rule

A technical gate can span Grade 9-11 engineering knowledge while a learner product remains grade-bounded. Therefore:

- Grade 9/10 products may consume only `FOUNDATION_G10` unless an owner scope explicitly authorizes formal enrichment.
- `FORMAL_G11` assets require the Class XI source layer.
- `EXTENDED_G11` assets are held from Grade 9/10 products by default.
- the internal ID `CON-CHEM-OIL-RIG` is legacy metadata only; learner surfaces must use direct chemistry language, not the mnemonic or the phrase `agent inversion`.

## Fail-closed checks

`validate_chemistry_gate_source_audit.py` rejects:

- missing Class XI formal authority,
- oxidation-number/agent claims routed as Grade 10 foundation,
- incomplete concept/equation source coverage,
- unresolved source-layer references,
- permanganate half-reaction leakage into Grade 10,
- learner-facing mnemonic leakage,
- or failure to acknowledge/repair the original provenance overclaim.

This audit changes source authority and grade-scope custody only. It does not establish learner mastery, Core purpose, question legality, or publication readiness.
