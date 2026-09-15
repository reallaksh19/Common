# Source-fidelity checks — EXECUTED

`qa/check_source_fidelity.py` compared each immutable Core2 source block against independently parsed `source-corpus.md` bytes after isolating the Q01–Q12 question blocks. Result: **PASS**.

- Q01–Q12 exact source text: **12/12**.
- Required attribution on each source question: **12/12**.
- H1/H2/H3 outside immutable source block: **12/12**.
- Complete answer anchor: **12/12**.
- Q02 recorded-position table is inside its immutable source block and matched exactly.
- Q12 source text remained exactly “A moves at 5 m/s and B moves at 3 m/s. Find the velocity of A relative to B.” Its answer reports **underdetermination**, identifies missing direction information and gives explicitly conditional examples; no unique invented answer is supplied.

`qa/reconcile_inventory.py` independently reconciled corpus headings, single-/multi-part structure, Q02 table rows, conventions, source hash and frozen atom-kind denominators. Result: **PASS**, **159 atoms**. This is not a manifest validating itself: it reparses the original corpus text and compares the extracted structure to the inventory.

**Held item:** `SRC-Q12-QC01` remains `SOURCE_DEFECT_UNDERDETERMINED`. This hold concerns source quality, not answer closure. It blocks any claim that the frozen corpus is fully well-posed.
