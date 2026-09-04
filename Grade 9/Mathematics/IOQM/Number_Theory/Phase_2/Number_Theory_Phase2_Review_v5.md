# Number Theory v5 - Phase 2 Teaching / Visual / Orphan Review

**Phase:** 2 of 5  
**Status:** `COMPLETE_FOR_PHASE2`

## What Phase 2 changed

- Rebuilt the teaching layer around **36 stable Number Theory skills**.
- Preserved **16 Advanced Worked Bridges**, but expanded each to the full PR140 bridge contract.
- Split broad 'factorisation' into power, SFFT/fixed-product and polynomial/consecutive-factor engines.
- Split exact carries from ordinary digit-sum congruence.
- Split overlapping windows from affine recurrences.
- Split number-theory counting into fixed-multiplicity counting, residue/pigeonhole obstruction, square-gap extremal reasoning and shared-prime graph modelling.
- Added an explicit mixed method-selection lab.
- Audited every Appendix A question for a complete recognition -> first line -> execution -> legality support route.
- Audited every Appendix A question for whether a structural visual helps or merely adds clutter.

## Phase 2 gate result

| Check | Result |
|---|---:|
| Stable skills taught | 36/36 |
| Advanced bridges rebuilt | 16/16 |
| Appendix A orphan-method routes | 90/90 PASS |
| Missing stable support IDs | 0 |
| Question visual decisions | 90/90 |
| Questions marked VISUAL_HELPFUL | 18 |
| Questions marked TEXT_DOMINANT | 72 |
| Teaching-layer structural visuals specified | 16/16 |
| Final hint audit | NOT RUN - Phase 3 |
| Final self-sufficiency audit | NOT RUN - Phase 4 |
| Final PDF | BLOCKED until Phase 4 |

## Dependency order

1. Integer structure before tricks
2. GCD -> Bézout -> congruence legality -> inverses -> CRT
3. Huge powers legally
4. Prime exponents inside factorials and perfect powers
5. Integer equations: manufacture structure and filter
6. Digits and bases are equations
7. Floors, recurrences, windows and arithmetic-combinatorial bridges
8. Mixed method-selection lab
9. Advanced Worked Bridges

## Orphan-method result

At the **teaching architecture level**, every one of the 90 Appendix A questions now has:

- an explicit recognition cue in the matrix;
- an explicit first useful line;
- an executable method description;
- a legality/boundary check;
- one or more stable skill/bridge IDs that exist in the rebuilt teaching layer.

Therefore:

`ORPHAN_METHODS_PHASE2 = 0`

This is not the final PR140 self-sufficiency gate. Phase 3 must still manually
audit the local H1/H2/H3 presentation, and Phase 4 must re-run all gates against
the integrated book.

## Visual-pedagogy result

A figure is required only where it reveals representation or structure that
would otherwise live in working memory. Decorative number imagery is rejected.

Question-level decisions:

- `VISUAL_HELPFUL`: 18
- `TEXT_DOMINANT`: 72

The final Appendix figures will be created/reused in Phase 3 and checked at
final PDF size in Phase 5.

## New teaching distinctions that matter for a 50%-prepared learner

### Factorisation is no longer one skill

- `NT-FACT-POW-01`: exponent parity / difference and sum of powers
- `NT-FACT-SFFT-01`: manufactured fixed-product forms
- `NT-FACT-POLY-01`: polynomial -> consecutive/near-consecutive factors
- `NT-FACT-01`: method-selection umbrella only

### Digit sum is no longer asked to do the work of carries

- `NT-DIGSUM-01`: congruence and bounded digit-sum structure
- `NT-CARRY-01`: exact $-9$ per carry accounting

### Sequence structure is split by first move

- `NT-REC-01`: reduce an affine recurrence modulo the target
- `NT-WINDOW-01`: subtract adjacent overlapping windows

### 'Counting' is no longer a catch-all

- `NT-COUNT-01`: fixed multiplicity / direct constrained choices
- `NT-PIGEON-01`: small-prime residue obstruction
- `NT-SQUAREGAP-01`: moving square interval extremum
- `NT-PRIMEGRAPH-01`: shared-prime graph model

## Files produced in Phase 2

1. `Number_Theory_Teaching_Architecture_v5.md`
2. `Number_Theory_Advanced_Worked_Bridges_v5.md`
3. `Number_Theory_Orphan_Method_Audit_v5.csv`
4. `Number_Theory_Visual_Pedagogy_Manifest_v5.csv`
5. `Number_Theory_Teaching_Visual_Manifest_v5.csv`

## Next phase

**Phase 3 - Appendix A/B repackaging.**

The frozen stems will be reused. Phase 3 adds non-spoiling badges, manually
rewrites every H1/H2/H3 strip, creates the approved structural figures, and
re-verifies all 20 Appendix B answers/method coverage.
