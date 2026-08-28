# 2018 Bhaskara Preliminary — Mathematical Qualification v1

## Authority boundary

Primary ingestion source remains the Cheenta reproduction. Mathematical paths below were independently derived for this project. A second reproduction carrying the AMTI paper/solution text (`Junior`, Scribd; mirrored at PDFCoffee) was used only as independent-match evidence, not silently promoted to an official AMTI-hosted source.

Important recovery: the second reproduction explicitly marks **Q03, Q05 and Q07 as Bonus**. This explains the defective option sets in the Cheenta transcription. They remain valuable mathematical evidence, but `scoring_disposition=BONUS` and they must not be counted as scored-item difficulty/frequency without that qualifier.

Profile columns are local Preliminary engineering screens, not psychometric calibration:

`C/R/F/S/A/H/K/B/T/P = conceptual / recognition / first-move / reasoning-steps / algebra / hidden-structure / constraints-cases / calculation-burden / trap-density / time-pressure` on 0–10.

## Qualified question ledger

| ID | Derived answer | Best first move | Minimum expert path | Solution/source disposition | Profile; speed |
|---|---|---|---|---|---|
| Q01 | `sqrt(3)` (B) | Rewrite every radical over `sqrt(2), sqrt(3)` | denominator -> `sqrt(3)+sqrt(2)`; numerator -> `sqrt(3)(sqrt(3)+sqrt(2))` | `INDEPENDENT_MATCH`; scored | `3/4/3/2/3/3/1/3/3/3`; DIRECT |
| Q02 | `60` (C) | Let train length be `L`; equate speeds | `L/4=(L+75)/9`; solve `5L=300` | `INDEPENDENT_MATCH`; scored | `2/2/2/2/2/2/1/2/2/2`; DIRECT |
| Q03 | no canonical option answer as written | Test candidate factor by polynomial division/substitution | none of the four listed linear factors divides the reproduced polynomial identically | `RESOLVED_BONUS`; bonus; source expression still not canonical for teaching | not scored-profiled |
| Q04 | `3` (C) | Translate proportion directly | `(17-x)/(31-x)=(25-x)/(47-x)` -> `x=3` | `INDEPENDENT_MATCH`; scored | `3/3/3/2/3/2/1/2/3/2`; DIRECT |
| Q05 | `x=3`; absent from choices | Test the small integer exponent suggested by scale | `5*27+3*125=510` | `RESOLVED_BONUS`; bonus; option set intentionally non-scoring in recovered copy | `3/3/3/2/3/2/1/2/5/3`; DIRECT |
| Q06 | `1` (A) | Convert the given relation to `x^2+x+1=0` | reduce target modulo `x^2+x+1`; equivalently target=`(x^2+x+1)(11x-3)+1` | `INDEPENDENT_MATCH`; scored | `4/5/4/3/4/5/2/2/4/4`; FAST_IF_RECOGNIZED |
| Q07 | parameter values `4,-20`; requested sum `-16` | Repeated root -> discriminant zero | `(m+8)^2-144=0`; solve | `RESOLVED_BONUS`; bonus; listed scored options do not contain `-16` | `3/3/3/2/3/2/2/2/5/3`; DIRECT |
| Q08 | `24` (D) | Count factors of 5 in `100!` | `floor(100/5)+floor(100/25)=20+4` | `INDEPENDENT_MATCH`; scored | `3/3/3/2/2/3/2/2/2/3`; DIRECT |
| Q09 | `44%` (D) | Similar-length scale `1.2` -> area scale square | `1.2^2=1.44` | `INDEPENDENT_MATCH`; scored | `2/2/2/2/2/2/1/2/2/2`; DIRECT |
| Q10 | `4` pairs (D) | Use coprimality to force `a|15`, `b|4` | enumerate divisor candidates under gcd=1; valid `(1,2),(3,2),(5,2),(15,2)` | `HAND_DERIVED`; scored | `6/7/6/5/5/7/6/4/6/6`; MULTISTEP |
| Q11 | `52` (A) | Bound the square between `8000` and `9000`; use last digit 9 | only `93^2=8649`; `a=6,b=4`; `a^2+b^2=52` | `HAND_DERIVED`; scored | `4/5/4/3/3/5/3/3/4/4`; FAST_IF_RECOGNIZED |
| Q12 | `16` (B) | Apply Engel/Cauchy or AM-GM to the reciprocal constraint | `(1+3)^2 <= (a+b)(1/a+9/b)=a+b`; equality at `a=4,b=12` | `HAND_DERIVED`; scored | `5/6/5/3/4/6/3/2/5/5`; FAST_IF_RECOGNIZED |
| Q13 | `-1` (C) | Complete squares / solve stationary linear system | `2a+b=1`, `a+2b=2` -> `(0,1)`; evaluate `-1` | `INDEPENDENT_MATCH`; scored | `5/4/4/4/5/4/2/3/4/4`; MULTISTEP |
| Q14 | `130 deg` (D) | Recall/derive incenter relation | `angle BIC=90+A/2=130` | `INDEPENDENT_MATCH`; scored | `3/4/3/2/2/4/1/1/3/3`; FAST_IF_RECOGNIZED |
| Q15 | `15 deg` (A) | Use square/rhombus equal lengths and the recovered construction | recovered solution reduces to a triangle with sine relation giving `15 deg` | `INDEPENDENT_MATCH`; scored; `IMAGE_REQUIRED_FOR_STUDENT_ANCHOR` | `5/6/5/5/3/6/2/4/5/5`; MULTISTEP |
| Q16 | `1` | Introduce the auxiliary point implied by `45 deg`; seek congruent triangles | recovered solution obtains `BE=GD`, `GF=EF`, hence `BE+DF=EF` | `INDEPENDENT_MATCH`; scored | `6/7/7/5/5/7/2/3/6/6`; MULTISTEP |
| Q17 | `20` | Average of five consecutive integers is the middle integer | numbers `8,9,10,11,12`; second+fourth=`20` | `INDEPENDENT_MATCH`; scored | `1/1/1/1/1/1/1/1/1/1`; DIRECT |
| Q18 | `4` | Difference of squares | `(k-n)(k+n)=96`; retain same-parity positive factor pairs | `INDEPENDENT_MATCH`; scored | `4/5/4/4/3/5/5/3/4/4`; MULTISTEP |
| Q19 | `-6` | Rewrite radicand as `3-8/(n+1)` | require perfect-square integer; only `n=3,-9`; sum `-6` | `INDEPENDENT_MATCH`; scored | `6/7/6/5/5/7/7/4/6/6`; CASE_HEAVY |
| Q20 | `11` | Use `b=a+3` immediately | `(a+7)/b=a/b+1` -> `b=7,a=4` | `INDEPENDENT_MATCH`; scored | `3/3/3/3/3/3/2/2/3/3`; DIRECT |
| Q21 | `5` | Set `t=cuberoot(2)` and use `(t+1/t)^3` | `x^3-3x=t^3+t^-3=5/2`; double | `HAND_DERIVED`; scored | `5/6/5/3/4/6/2/2/4/4`; FAST_IF_RECOGNIZED |
| Q22 | `155/2` (`77.5 deg`) | Use polygon interior-angle sum | heptagon sum `900`; known five sum `745`; `2x=155` | `HAND_DERIVED`; scored | `2/2/2/2/2/2/1/2/2/2`; DIRECT |
| Q23 | `2` | Cancel altitude through difference of Pythagorean identities | `AB^2-AC^2=BD^2-DC^2`; set `DC=t`, `BD=5t` | `HAND_DERIVED`; scored | `4/5/4/3/3/5/2/2/4/4`; FAST_IF_RECOGNIZED |
| Q24 | `8 cm^2` | Convert each inscribing relation into diameter/space diagonal | outer cube side `2` -> sphere diameter `2` -> inner cube side `2/sqrt(3)` -> area `8` | `HAND_DERIVED`; scored | `5/5/5/4/3/5/3/3/4/5`; MULTISTEP |
| Q25 | `4` | Square the interval, then count multiples of 7 | `225<n<256`; `231,238,245,252` | `HAND_DERIVED`; scored | `2/2/2/2/2/2/2/2/2/2`; DIRECT |
| Q26 | `20` | Name the two radicals and cross-multiply before squaring | ratio gives `sqrt(x+5)=(5/2)sqrt(x-16)`; solve and domain-check | `HAND_DERIVED`; scored | `4/4/4/4/5/4/3/3/4/4`; MULTISTEP |
| Q27 | `1` | Equate total work | `Mm=(M+N)(m-n)` -> `M/N=m/n-1` | `HAND_DERIVED`; scored | `4/5/4/3/4/5/2/2/4/4`; FAST_IF_RECOGNIZED |
| Q28 | `78` | Write number as `10a+b` | `a+b=15`; reversal increase 9 -> `b-a=1`; solve | `HAND_DERIVED`; scored | `2/2/2/3/2/2/2/2/2/2`; DIRECT |
| Q29 | `7` | Reduce to last-digit cycle of 7 | period 4; `173 mod 4=1` | `HAND_DERIVED`; scored | `2/3/2/2/1/3/1/1/2/2`; FAST_IF_RECOGNIZED |
| Q30 | `1:2` | Normalize with total `S=a+b+c` | first ratio -> `S=4a`; second -> `c=5S/12=5a/3`; obtain `b=4a/3` and target `1/2` | `HAND_DERIVED`; scored | `4/5/4/4/5/5/2/3/4/4`; MULTISTEP |

## Qualification counts

- visible question slots: 30
- mathematically hand-derived to a determinate result: 29
- unresolved mathematical expression: Q03 only
- recovered `BONUS` disposition: Q03, Q05, Q07
- image-dependent for clean student reproduction: Q15
- scored questions with a usable mathematical path in this file: 27

## Curriculum evidence promoted from 2018

Strong first-move families supported by solution-qualified scored items include:

1. **transform/reduce before calculating** — Q01, Q06, Q21;
2. **divisibility/modular structure** — Q08, Q10, Q18, Q19, Q25, Q29;
3. **short metric geometry identities** — Q14, Q16, Q23, Q24;
4. **constraint optimization** — Q12, Q13;
5. **model translation from words to equations** — Q02, Q04, Q20, Q27, Q28, Q30.

Do not count the three bonus items as ordinary scored frequency evidence.
