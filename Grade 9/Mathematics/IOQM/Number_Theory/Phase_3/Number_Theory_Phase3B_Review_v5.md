# Number Theory v5 - Phase 3B Full Student-Book Scale-Up

**Status:** `PHASE3B_FULL_STUDENT_BOOK_DRAFT_COMPLETE`

## Purpose

Scale the accepted Phase 3A information-design grammar across the complete student-facing Number Theory book before running the integrated PR140 gates.

The mathematical stems of Appendix A (90) and Appendix B (20) remain frozen under the corpus-custody rule.

## Student book now included

1. **4-page 3-Day Simple Navigator**
   - Quick Check on first useful moves;
   - weak-topic -> stable-skill routing;
   - H1/H2/H3 fading-help protocol.
2. **Full dependency-ordered reference core**
   - 36 stable Number Theory skills;
   - repeated semantic page grammar: remember -> missing IOQM link -> mechanism -> worked bridge -> first line -> contrast -> legality.
3. **Expanded Advanced Worked Bridges**
   - increased from 16 to **30**;
   - new bridges close specific difficult-transfer gaps in the 90-row matrix rather than adding generic enrichment.
4. **Student support map**
   - all NT-Q001--NT-Q090 mapped to stable skill/bridge review locations;
   - deliberately names the review location, not the trick.
5. **Appendix A**
   - all **90 frozen questions**;
   - compact difficulty + broad-family badges;
   - adaptive H1/H2/H3 hints;
   - structural figures where they reduce cognitive load;
   - answer key after NT-Q090.
6. **Appendix B**
   - all **20 reliable-source challenge questions**;
   - PYQ + difficulty + family badges;
   - adaptive hints;
   - answer key after B20.
7. **Appendix C**
   - exactly **2 pages**;
   - formulas, theorem hypotheses, first-line router and final legality checklist.

## Advanced-bridge expansion

Phase 2 contained NT-A01--NT-A16. Phase 3B adds NT-A17--NT-A30 for gaps that were still too question-specific for a half-prepared learner:

- maximal prime powers controlling an LCM interval;
- divisor-count congruence for kth powers;
- least exponent for a prescribed terminal block;
- factorial quotient integrality via a known multinomial integer;
- nested digit sums by backward minimisation;
- nearby floor functions as divisor-boundary jumps;
- double-factorial denominators by 2-adic valuation;
- square roots modulo powers of 10;
- coefficient domination for the same digit string in two bases;
- prime triples under a cubic quotient;
- sum=product uniqueness when 1s are allowed;
- distinct fourth powers modulo a prime;
- the period of n^n modulo a prime;
- fixed-hypotenuse primitive Pythagorean triples.

`ADVANCED_BRIDGES_PHASE3B = 30`

## Information-design changes from Phase 2

Phase 2 was the engineering backbone. Phase 3B is the student product.

The book now uses:

- semantic colour panels instead of undifferentiated prose;
- equations in open whitespace;
- explicit worked bridges;
- quiet support cross-references;
- question cards with the problem visually dominant;
- small badges rather than method-revealing labels;
- fading hints immediately under the question;
- mathematical diagrams only where a representation is genuinely easier to see than remember.

## Appendix design boundary

The Appendix B **method-coverage table is not placed in the student section**. It belongs in the Reviewer / Build Dossier required in the final PDF. This keeps the student challenge bank visually comparable to the supplied Algebra benchmark while still preserving the method-coverage evidence for Phase 4.

## PDF production check

- PDF: `Number_Theory_Phase3B_Student_Book_v5.pdf`
- Page count: **90 A4 pages**
- Openable: PASS
- Encrypted: no
- Fonts embedded: PASS
- PDF outline present: 51 items
- Phase 3B PDF SHA-256: `93e0eb483da389f73053b27993eb2328a4ecff1235b91f690bc266dbbc8a4f82`

### Render verification

The document was rendered at 200 dpi across the phase build. Representative pages were visually inspected across:

- Navigator;
- early/middle/late reference core;
- Advanced Bridges;
- early/middle/late Appendix A;
- Appendix B;
- Appendix C.

The final Appendix C and answer-key tail were re-rendered after layout corrections.

Observed Phase 3B state:

- no observed clipping in inspected pages;
- no black squares or missing glyphs in inspected pages;
- no off-page tables in inspected pages;
- Appendix C corrected from a one-page overpacked draft to a true two-page helper;
- Appendix B method-coverage table moved out of the student book after its reviewer-style density was visually identified as a mismatch.

**Evidence boundary:** this is not the final Phase 5 page-by-page visual QA. Full 200-dpi inspection of every final delivered page remains mandatory after the Phase 4 content gates and reviewer dossier are integrated.

## Known Phase 4 obligations

Phase 3B does **not** claim final PR140 PASS.

Phase 4 must still:

1. re-run the 90/90 Appendix A question-to-method and orphan-method gates against this integrated student book;
2. audit all 90 H1/H2/H3 strips for leakage, retrieval quality, math typography and stable-ID validity;
3. re-run the 90/90 visual-pedagogy audit against the actual rendered figures;
4. verify Appendix A custody 90/90;
5. reverify Appendix B source custody, method coverage, hints and answers 20/20;
6. build the Reviewer / Build Dossier inside the final PDF;
7. only then declare `STATIC_CONTENT_SELF_SUFFICIENCY = PASS_90_OF_90` if every row passes.

## Phase 4 next

**Integrated PR140 audit and reviewer dossier.**

No new question corpus is required. The next phase audits the complete student book that now exists, repairs any failed rows, and creates the reviewer evidence pages that the user requested to be inside the final PDF.
