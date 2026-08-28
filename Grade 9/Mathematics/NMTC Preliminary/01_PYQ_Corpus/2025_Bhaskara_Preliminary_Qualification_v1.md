# 2025 Bhaskara Preliminary — Mathematical Qualification v1

## Source authority

Question source used for qualification:

- reproduced 2025–2026 Bhaskara Screening paper carrying the Association of Mathematics Teachers of India heading and 30-question paper structure;
- Cheenta searchable reproduction for question-level text/figure locators.

Answer authority:

- **The Association of Mathematics Teachers of India — `NMTC-2025-Answer Key (Provisional)`**, one-page official provisional key covering Primary/Sub-junior/Junior/Inter.

The key is authoritative evidence of AMTI's **provisional** intended answers, not a license to overwrite a mathematically inconsistent printed stem. Where stem mathematics and provisional key conflict, both are preserved and the question is blocked from clean canonical use.

The reproduced paper profile states a two-hour test (`10 am–12 noon`), `+1` for a correct response and `-1/2` for an incorrect response. Treat this as the 2025 paper profile, not a timeless format claim.

## Qualification ledger

| ID | Derived / provisional-key answer | Best first move | Minimum expert path | Qualification disposition |
|---|---|---|---|---|
| Q01 | `9940` (B) | Subtract the common remainder, then use LCM | `lcm(16,24,36)=144`; largest `144k+4<10000` is `9940` | scored; derived matches provisional key |
| Q02 | key C (`p+q=157`) | Use the supplied rectangle/shaded-region geometry before coordinates | decompose the shaded area using the given `20×10` rectangle and `AP=8`; reduce the rational area | scored; `FIGURE_REQUIRED_FOR_STUDENT_ANCHOR`; provisional key available |
| Q03 | `115` (A) | Factor the common seventh-root term | `(12+x)^(8/7)/(12x)=(64/3)x^(1/7)` -> `12+x=128x` -> `x=12/127`; `b-a=115` | scored; clean transform-first anchor |
| Q04 | `828` (D) | Recognize `52±6√43=(√43±3)^2` | convert the `3/2` powers to cubes and use `(u+v)^3-(u-v)^3` | scored; clean surd-identity anchor |
| Q05 | `44°` (C) | Mark the three supplied angles on the exact figure before chasing | short angle-chain solution depends on the supplied construction | scored; `FIGURE_REQUIRED_FOR_STUDENT_ANCHOR` |
| Q06 | `13` (C) | Convert `R:r=5:2` into a side relation for a right triangle | with hypotenuse `b=2R` and `r=(a+c-b)/2`, normalize `b=5`; obtain legs `3,4`; half-angle cotangents are `3,2` | scored; clean geometry/algebra anchor |
| Q07 | `15/2` (A) | Substitute the second absolute-value equation into the first | `|y-5|=|x-1|`; hence `2|x-1|=1`; points have `x=1/2,3/2`, common `y=11/2` | scored; clean absolute-locus anchor |
| Q08 | printed stem gives `40/3` days for half the work; provisional key D=`26 2/3` | Add pairwise rates, then divide by 2 to get all-three rate | pair rates sum `3/40=2(R+A+P)` so all-three rate `3/80`; half-work time `40/3`; whole-work time `80/3=26 2/3` | **SOURCE/KEY CONFLICT**: provisional key answers whole-house time while printed stem asks 50%; not a canonical anchor |
| Q09 | `2` (B) | Compute `x+1/x` instead of solving for `a,b` | with `U=√(a+3b),V=√(a-3b)`, `(x²+1)/x=x+1/x=2a/(3b)` | scored; clean symmetric-radical anchor |
| Q10 | `4` (D) | Remove the absolute value by converting to a distance inequality | `2/|x-13|>8/9` -> `0<|x-13|<9/4`; integers `11,12,14,15` | scored; clean inequality/count anchor |
| Q11 | `80°` (B) | Use exact two-circle/tangent figure; mark radii to tangency points first | tangent/radius and circle angle relations produce the short target-angle chain | scored; `FIGURE_REQUIRED_FOR_STUDENT_ANCHOR` |
| Q12 | `8` (D) | Set `t=√(log_2 x)` | `log_2(8x)=3+t²`; equation -> `t²-3t+2=0`; `x=2,16`; ratio `8` | scored; clean logarithmic-substitution anchor |
| Q13 | `5` (B) | Square the residue directly | `n≡4 (mod 11)` -> `n²≡16≡5` | scored; direct modular anchor |
| Q14 | `87` (D) | Encode each two-digit number by its digits immediately | first number `12a`, digit sum `3a`: `36a²=144` -> `24`; second `21b`, sum `3b`: `63b²=567` -> `63`; total `87` | scored; place-value equation anchor |
| Q15 | `143°` (D) | Preserve the supplied collinearity/bisector figure and write pentagon angle sum | translate the linked angle differences/equalities, then use the two bisectors to obtain the angle at `R` | scored; `FIGURE_REQUIRED_FOR_STUDENT_ANCHOR` |
| Q16 | `0` | Complete the square before touching the huge powers | `b=c+8`; `bc+a²+16=(c+4)²+a²=0`; realness forces `a=0,b=4,c=-4`; odd powers cancel | scored; strong `REAL_CONSTRAINT_SUM_SQUARE_COLLAPSE` anchor |
| Q17 | `-1/2025` | Compose the Möbius map algebraically before substituting numbers | for `k=2025`, `f(f(x))=k²x/((k+1)x+1)`; setting equal `k²` gives `kx+1=0` | scored; derived result matches the fractionally formatted provisional key |
| Q18 | printed real equation has distinct root set `{2}`; provisional key reports `4` | Cube once; real cube is bijective | `16-x³=(4-x)^3` -> `12(x-2)^2=0`; distinct solution `x=2`; algebraic multiplicity-two sum would be `4` | **CONVENTION/KEY CONFLICT**: “sum of all roots” normally uses distinct equation solutions; key appears to count multiplicity created after cubing; block canonical use |
| Q19 | provisional key `67.5°` | Use the exact touching-quadrants figure; locate radii and midpoint before angle chase | geometry depends on the supplied diagram | scored; `FIGURE_REQUIRED_FOR_STUDENT_ANCHOR` |
| Q20 | printed `+(6-k)` gives `k=12`; provisional key gives `0` | Use Vieta: three positive integer roots with sum 6 and pair-sum 11 must be `1,2,3` | their product is `6`, so printed constant `6-k=-6` -> `k=12`; **if** constant were `k-6`, key `0` follows | **SIGN SOURCE/KEY CONFLICT**; likely `6-k` vs `k-6` defect; do not silently repair |
| Q21 | `10` | Use digit-sum divisibility by 9 | count `(a,b)` with `a+b+5≡0 mod9`, remembering digit `b=0` or `9` can share residue 0 | scored; clean counting/divisibility anchor |
| Q22 | `2024` | Center the consecutive bases around `2024` | `(m+1)^3-(m-1)^3=6m²+2`; hence `(a²-2)/6=2024²` | scored; clean difference-of-cubes anchor |
| Q23 | `25` | Use the complement percentage | fully correct `=100-12-32=56%`; `0.56N=14` | scored; direct percentage anchor |
| Q24 | `4051` | Determine signs first; only then remove absolute values | both cubic expressions are positive at `a=2025`; subtract them directly to get `2a+1=4051` | scored; sign-before-expansion anchor |
| Q25 | `20` | Use the exact hoop/rectangle secant construction | metric relation from `AB=18`, `BC=32` and the circle's highest point gives radius 20 | scored; `FIGURE_REQUIRED_FOR_STUDENT_ANCHOR` |
| Q26 | `3` | Put `t=2n-1` | `n²-n-1=(t²-5)/4`; expression becomes `(t²-5)^2/t`; integrality iff positive odd `t|25`; `t=1,5,25` | scored; elegant divisibility substitution anchor |
| Q27 | `1` | Convert the log equation to `x=y²` | `log_4x=log_2y` -> `x=y²`; then `y^4=8+2y²`; positivity/log domain leaves `(x,y)=(4,2)` | scored; clean log-system anchor |
| Q28 | `6` | Use the exact tangent/parallel figure; seek similarity/tangent-length equalities | supplied geometry with `PQ=6,QR=18` determines `SB=6` | scored; `FIGURE_REQUIRED_FOR_STUDENT_ANCHOR` |
| Q29 | final reduced weight `8 kg`; mass lost `12 kg` | Track invariant dry mass, not water mass | dry mass `=2%·20=0.4 kg`; when dry mass is 5%, final weight `=8 kg` | scored; provisional key `8`; wording “reduced weight” should be taught as final reduced weight, with 12 kg separately identified as reduction |
| Q30 | printed stem has non-key values; provisional key `31` corresponds to “fourth exceeds **second** by 24” | Let second/third/fourth terms be `x,y,z` and use `y²=xz` | printed `z-y=24`, `x+y=6` leads irrational alternatives, not 31; changing only to `z-x=24` gives `x=1,y=5,z=25`, sum `31` | **SOURCE/KEY CONFLICT**; likely “second” vs “third” defect; block canonical use |

## 2025 qualification status

- question slots: **30/30**
- official answer evidence: complete **AMTI provisional** Junior key
- clean mathematical/source conflicts requiring canonical block: **Q08, Q18, Q20, Q30**
- figure-gated exact student anchors: **Q02, Q05, Q11, Q15, Q19, Q25, Q28**
- wording nuance requiring explicit teaching note: Q29 (`final reduced weight=8`, `amount reduced=12`)
- all other non-image questions have a compact independently derived first move/path matching the provisional key

## Curriculum findings promoted from 2025

1. **Transformation remains the dominant algebra behavior**: common-root factorization (Q03), surd-square recognition (Q04), transformed log variable (Q12), square-collapse realness (Q16), Möbius composition (Q17), centered cubes (Q22), and odd/even sign handling (Q24).
2. **Elementary number theory is highly first-move sensitive**: LCM/remainder (Q01), direct modular square (Q13), digit divisibility (Q21), and the substitution `t=2n-1` (Q26).
3. **Preliminary geometry remains recognition-heavy and figure-custody sensitive**: seven questions require exact supplied diagrams for a defensible student-facing anchor.
4. **Source QC is not clerical**: Q08/Q18/Q20/Q30 show that even an official provisional answer key can disagree with reproduced stems or with standard equation-root convention. The curriculum must preserve both source evidence and independent mathematics.
5. **Sequence & Series evidence is present but Q30 is not clean**: it may inform source-QC/contrast teaching, but cannot be used as a canonical scored GP anchor until the original wording/key conflict is resolved.
