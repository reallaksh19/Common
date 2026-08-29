# Issue #45 — Wave 1D Interface
## Reciprocal invariants

`STATUS: W1_INTERFACE_COMPLETE`

`ROLE: INTERNAL_SUBTOPIC_INTERFACE`

This interface teaches the learner to preserve symmetry instead of destroying it by solving for the hidden variable too early.

## 1. CONCEPTS

- reciprocal pairs `x` and `1/x`;
- symmetry under `x <-> 1/x`;
- low-order reciprocal identities;
- recurrence for `S_n=x^n+x^-n`;
- palindromic expressions/equations;
- decision to reduce an invariant rather than solve explicitly for `x`.

## 2. PREREQUISITES

- expansion of `(a+b)^2` and `(a+b)^3`;
- simple recurrence thinking;
- quadratic solving;
- reciprocal notation and nonzero denominator condition.

## 3. RECOGNITION_CUES

| Visible cue | Structural recognition |
|---|---|
| `x+1/x` is given | treat it as the primary variable/invariant |
| target is `x^n+x^-n` | use power-sum reduction/recurrence |
| coefficients read the same forwards/backwards | divide by a middle power and expose reciprocal symmetry |
| radical ratio and its reciprocal appear | combine symmetrically before solving parameters |
| target changes sign under `x <-> 1/x` | reciprocal invariant may not determine it uniquely |

## 4. FIRST_MOVES

1. Record `x!=0`.
2. Let `S_0=2`, `S_1=x+1/x` when higher symmetric powers are needed.
3. Build `S_n=S_1*S_(n-1)-S_(n-2)` rather than solve for `x`.
4. For a palindromic polynomial, divide by the central power and set `y=x+1/x`.
5. Before using the invariant, ask whether the target is symmetric or asymmetric under `x <-> 1/x`.

## 5. INVARIANTS

For `x!=0`, define `S_n=x^n+x^-n`.

- `S_0=2`;
- `S_1=x+x^-1`;
- `S_2=S_1^2-2`;
- `S_3=S_1^3-3S_1`;
- recurrence: `S_n=S_1*S_(n-1)-S_(n-2)`.

Swapping `x` and `1/x` does not change any `S_n`.

## 6. REPRESENTATION_SWITCHES

- explicit reciprocal pair -> `S_1=x+1/x`;
- high reciprocal powers -> recurrence in `S_n`;
- palindromic polynomial -> divide by a central power -> polynomial in `y=x+1/x`;
- radical ratio -> identify a number and its reciprocal -> symmetric target.

## 7. REVERSIBILITY_OR_DOMAIN_CONDITIONS

- all reciprocal expressions require `x!=0`;
- knowing `x+1/x` does not always determine an asymmetric target such as `x-1/x` uniquely;
- solving `y=x+1/x` back for `x` is unnecessary unless the target genuinely requires individual values;
- if the reduction produces possible `y` values, any later return to real `x` must respect the real-solvability condition of `x+1/x=y` when real `x` is required.

## 8. DECISION_BOUNDARIES

`D-DB1 INVARIANT_REDUCTION_vs_EXPLICIT_ROOTS`  
If the target is symmetric, reduce it directly. Solve for `x` only if an asymmetric target or individual root is required.

`D-DB2 SYMMETRIC_vs_ASYMMETRIC_TARGET`  
`x^n+x^-n` is fixed by the reciprocal invariant; `x^n-x^-n` may require an additional sign choice.

`D-DB3 RECURRENCE_vs_FRESH_EXPANSION`  
Use one recurrence for higher powers rather than re-expand each time.

`D-DB4 PALINDROMIC_REDUCTION_vs_GENERIC_QUARTIC`  
A reciprocal-symmetric quartic is often a quadratic in `x+1/x`, not a quartic-formula problem.

## 9. MISCONCEPTION_TRAPS

- solving a quadratic for `x` and creating unnecessary radicals;
- forgetting `x!=0`;
- recurrence sign/index error;
- assuming symmetric data determines an asymmetric target uniquely;
- failing to recognize palindromic coefficient symmetry;
- confusing `x+1/x` with `(x+1)/x`.

## 10. CONTRAST_PAIRS

### CP-D1 — symmetric target vs asymmetric target
Given `x+1/x=4`:
- `x^2+1/x^2` is uniquely determined: `14`.
- `x^2-1/x^2` has two possible signs without extra information.

### CP-D2 — reduce vs solve
Given `x+1/x=5`, asking for `x^3+1/x^3` needs only the invariant.
Asking for the larger of the two possible real values of `x` requires solving the quadratic.

### CP-D3 — palindromic vs generic quartic
- `x^4-5x^3+8x^2-5x+1=0` has reciprocal symmetry.
- changing one end coefficient breaks that exact reduction.

## 11. TRANSFER_MECHANISMS

- high reciprocal power with recurrence;
- radical ratio that becomes `t+1/t` only after conjugate simplification;
- palindromic quartic reduced to a quadratic in `y=x+1/x`;
- boundary item where a symmetric invariant cannot fix an asymmetric sign-sensitive target.

## 12. SOURCE_IDS_AND_DISPOSITIONS

### CLEAN_SCORED_ANCHOR
- `NMTC-BH-P-2018-Q21` — reciprocal cube-root invariant;
- `NMTC-BH-P-2025-Q09` — symmetric radical ratio leading to reciprocal structure.

### AUTHOR_CREATED_FOUNDATION required
- recurrence derivation;
- palindromic reduction;
- symmetric-versus-asymmetric target boundary.

## 13. CANDIDATE_MASTERY_ITEMS

All are `AUTHOR_CREATED_TRANSFER` candidates.

### D-M1 — direct invariant
If `x+1/x=5`, find `x^3+1/x^3`.

Expected: `110`.

Check: `5^3-3*5=125-15`.

### D-M2 — recurrence
If `x+1/x=3`, find `x^5+1/x^5`.

Expected: `123`.

Independent recurrence check:
`S0=2`, `S1=3`, `S2=7`, `S3=18`, `S4=47`, `S5=123`.

### D-M3 — palindromic structural reduction
Solve over nonzero real `x`:
`x^4-5x^3+8x^2-5x+1=0`.

First reduction: divide by `x^2` and let `y=x+1/x`:
`y^2-5y+6=0`, so `y=2` or `3`.

Expected real solutions: `x=1`, `(3+sqrt5)/2`, `(3-sqrt5)/2`.

Check: `y=2` gives `(x-1)^2=0`; `y=3` gives `x^2-3x+1=0`.

### D-M4 — boundary: invariant insufficient
If `x+1/x=4`, determine `x^2-1/x^2`.

Expected: not unique; `x-1/x=±sqrt(12)`, so `x^2-1/x^2=±8sqrt3`.

This item must diagnose the learner who assumes every reciprocal-looking target is uniquely determined.

## 14. DIAGNOSTIC_TAGS

- `RECIPROCAL_INVARIANT_MISSED`
- `SOLVED_X_UNNECESSARILY`
- `RECIPROCAL_NONZERO_DOMAIN_IGNORED`
- `RECURRENCE_SIGN_OR_INDEX_ERROR`
- `PALINDROMIC_STRUCTURE_MISSED`
- `SYMMETRIC_DATA_ASYMMETRIC_TARGET_CONFUSION`
- `CALCULATION`

## 15. H3_TO_H0_FADE_PLAN

Every task begins H0; support fades:

- **H3 execution**: give `S2=S1^2-2` or the recurrence formula with current values inserted.
- **H2 structure**: “Work with `S_n=x^n+x^-n`; do not solve for `x`.”
- **H1 recognition**: “The target is unchanged when `x` and `1/x` are swapped.”
- **H0 independent**: learner chooses invariant/recurrence unaided.

For palindromic equations:

- H3: “divide by `x^2`, then replace `x^2+x^-2` by `y^2-2`”;
- H2: “divide by the middle power and expose reciprocal pairs”;
- H1: “read the coefficients forward and backward”;
- H0: no hint.

`W1-D_GATE: PASS_INTERFACE_READY_FOR_WAVE2`
