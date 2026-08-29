# Radicals, Exponents & Logarithmic Transformations — Assimilation Concept Map v2

`ISSUE_AUTHORITY: #45`

`WAVE: 0 — GROUNDING_AND_CONCEPT_MAP`

`STATUS: DRAFT_CONCEPT_MAP`

This map is the mandatory pre-prose authority for the Issue #45 assimilation rebuild. It is written for a Grade IX/X learner who remembers roughly half of the topic but does not yet choose representations, preserve domains, or distinguish reversible from non-reversible transformations reliably.

The map is not the student teaching book. It defines what the teaching book must repair.

---

# 1. Governing architecture

## 1.1 Central mathematical belief

> A radical, exponent or logarithm is often not the problem itself. It is a representation of a smaller algebraic structure.

The learner must acquire this operating loop:

```text
VISIBLE FORM
   |
   v
WHAT CAN BE REWRITTEN WITHOUT CHANGING THE MATHEMATICS?
   |
   +--> common radical basis
   +--> hidden square/cube or conjugate structure
   +--> common exponential base / repeated power
   +--> reciprocal invariant
   +--> logarithm <-> exponent
   +--> logarithmic relation -> algebraic relation
   |
   v
DID THE TRANSFORMATION PRESERVE THE EXACT SOLUTION SET?
   |
   +--> YES: equivalence step ( <=> )
   |
   +--> NO / CONDITIONALLY: implication step ( => )
            keep domain/sign/zero restrictions
            generate candidates only
            verify in the original problem
   |
   v
SOLVE THE SMALLER ALGEBRA
   |
   v
RESTORE DOMAIN / SIGN / SOURCE CONDITIONS
   |
   v
CHECK -> TRANSFER
```

## 1.2 Cognitive contract

```text
SEE
  -> REALIZE the hidden representation or invariant
  -> UNDERSTAND why the rewrite is valid and under what conditions
  -> ADOPT the first move independently
```

Operationally:

```text
RECONNECT -> DISCOVER -> MAKE SENSE -> TRY -> DIAGNOSE -> FADE -> ADOPT -> TRANSFER
```

Performance target:

```text
RECOGNIZE -> FIRST MOVE -> SOLVE EFFICIENTLY -> CHECK -> TRANSFER
```

---

# 2. Learner-state map

## 2.1 PRIOR_KNOWLEDGE — likely already present

`PK-01` Simplify routine square roots by extracting a perfect square.

`PK-02` Recall common exponent laws for positive integer exponents.

`PK-03` Solve simple same-base equations such as `2^x=8`.

`PK-04` Recognize `log_b x=y` as related to exponentiation, at least procedurally.

`PK-05` Use basic algebraic identities such as `(a+b)^2`, `(a-b)^2`, and difference of squares.

`PK-06` Solve linear and quadratic equations after a substitution has already been supplied.

`PK-07` Perform routine rationalization when explicitly instructed.

`PK-08` Check a numerical candidate by substitution when prompted.

## 2.2 LIKELY_HALF_KNOWLEDGE — remembered but unstable

`HK-01` Knows `a^(m/n)` notation but does not consistently connect it to nth roots and domain restrictions.

`HK-02` Knows `a^-n=1/a^n` but may treat the negative sign as belonging to the base or numerator incorrectly.

`HK-03` Simplifies individual radicals but does not first search for a common radical basis across an expression.

`HK-04` Recognizes conjugates after they are pointed out, but does not run square/cube expansions backwards to expose them.

`HK-05` Recalls `sqrt(x^2)` as “x” or “±x” instead of the principal-root result `|x|`.

`HK-06` Knows squaring can create an extraneous root, but cannot explain the loss of reversibility.

`HK-07` Cancels/divides by an expression containing the variable without asking whether it can be zero.

`HK-08` Uses logarithm laws as a formula list and may invent a sum law by analogy.

`HK-09` Knows logs and exponents are inverse operations, but does not use the inverse relation as a representation switch.

`HK-10` Uses `t=log_b x` mechanically even when the repeated object is `sqrt(log_b x)` or another larger structure.

`HK-11` Solves for a hidden variable such as `x` even when only `x+1/x` or a symmetric power expression is needed.

`HK-12` Can manipulate a transformed equation but may forget restrictions inherited from the original radical/logarithmic form.

## 2.3 MISSING_BRIDGES — the actual repair targets

`B-01 REPRESENTATION_CHOICE` — ask “what equivalent language makes the structure smaller?” before calculating.

`B-02 COMMON_BASIS` — different-looking radicals or powers can be the same building block in disguise.

`B-03 REVERSE_IDENTITY_RECOGNITION` — expansions can be read backwards to reconstruct hidden squares/cubes and conjugate pairs.

`B-04 PRINCIPAL_ROOT_MODEL` — the radical symbol denotes a single non-negative root; solving `u^2=a` is a different task.

`B-05 INVERSE_AND_RECIPROCAL_MODEL` — negative exponents and reciprocal variables are structural inverses, not sign decorations.

`B-06 EQUIVALENCE_VS_IMPLICATION` — not every legal forward algebraic operation is reversible on the whole domain.

`B-07 DOMAIN_LEDGER` — conditions are mathematical information that must survive every rewrite.

`B-08 REPEATED_OBJECT_SUBSTITUTION` — choose the whole object that repeats, not automatically the innermost expression.

`B-09 INVARIANT_OVER_EXPLICIT_SOLVING` — symmetric/reciprocal targets can often be reduced without finding the underlying variable.

`B-10 LOG_AS_EXPONENT_LANGUAGE` — logs should be converted to and from exponent form as needed, not treated as a separate rule universe.

`B-11 EXACT_STRUCTURE_BEFORE_DECIMALS` — preserve exact inverse/common-base structure before approximation.

`B-12 SOURCE_INTEGRITY` — a supplied key never overrides valid mathematics; conflicted historical evidence stays conflicted.

---

# 3. Core invariants and structures

`I-01 EQUIVALENT_REPRESENTATION`  
The numerical/algebraic object is unchanged when rewritten correctly, even if its surface notation changes.

`I-02 PERFECT_POWER_CORE`  
A radical expression simplifies when a perfect power is separated from a residual common radical basis.

`I-03 HIDDEN_BINOMIAL_POWER`  
Expressions of the form `A ± B sqrt(d)` may be deliberately encoded binomial squares/cubes.

`I-04 PRINCIPAL_ROOT_NONNEGATIVITY`  
For real `u`, `sqrt(u^2)=|u|`.

`I-05 EXPONENT_BASE_NORMALIZATION`  
Related bases can often be rewritten as powers of a common base or common ratio.

`I-06 POSITIVE_EXPONENTIAL_VARIABLE`  
For valid real base `a>0`, `a!=1`, a substitution `t=a^x` carries `t>0`.

`I-07 RECIPROCAL_SYMMETRY`  
If `x!=0`, the pair `x` and `1/x` is often better represented through `S_n=x^n+x^-n` than through explicit solution of `x`.

`I-08 TRANSFORMATION_REVERSIBILITY`  
An invertible transformation on the relevant domain preserves the solution set; a non-invertible transformation may only preserve one direction.

`I-09 LOG_EXP_INVERSE`  
For `b>0`, `b!=1`, `x>0`: `log_b x=y <=> b^y=x`.

`I-10 LOG_DOMAIN_PERSISTENCE`  
Every logarithmic argument must remain positive and every base valid, even after logs disappear from the transformed algebra.

`I-11 REPEATED_OBJECT_COMPRESSION`  
A complicated equation often becomes low-degree algebra when its repeated structural object is named once.

`I-12 SOURCE_CUSTODY`  
Historical source disposition is invariant under teaching reuse: clean stays clean, sensitive stays sensitive, conflict stays conflict.

---

# 4. Representation network

```text
RADICAL FORM
   <-----------------------> FRACTIONAL-EXPONENT FORM
   |                                  |
   | extract perfect powers            | normalize powers
   v                                  v
COMMON RADICAL BASIS              COMMON EXPONENTIAL BASE
   |                                  |
   | reverse identity                  | repeated power / ratio
   v                                  v
HIDDEN SQUARE/CUBE                LOW-DEGREE ALGEBRA IN t
   |                                  |
   +--------------+-------------------+
                  |
                  v
             DOMAIN / SIGN CHECK
                  |
                  v
            ORIGINAL VARIABLE
```

```text
EXPONENTIAL STATEMENT
      <==================>
LOGARITHMIC STATEMENT
      |
      | choose repeated log object
      v
LOW-DEGREE ALGEBRA IN t OR u
      |
      | map back with base/argument restrictions
      v
ORIGINAL POSITIVE VARIABLE
```

```text
x and 1/x
   |
   v
S1 = x + 1/x
   |
   +--> S2 = S1^2 - 2
   +--> S3 = S1*S2 - S1
   +--> Sn = S1*S(n-1) - S(n-2)

Do not solve x unless the target actually requires x.
```

```text
ORIGINAL EQUATION
   |
   +-- invertible step on valid domain --> EQUIVALENT EQUATION  (<=>)
   |
   +-- non-invertible / zero-sensitive step --> CANDIDATE EQUATION  (=>)
                                                  |
                                                  v
                                            VERIFY / FILTER
```

---

# 5. Stream W1-A — Common radical basis & surd structure

## PRIOR_KNOWLEDGE

- extract obvious perfect squares/cubes;
- basic conjugate identity;
- routine rationalization.

## LIKELY_HALF_KNOWLEDGE

- simplifies terms one by one but does not search for a shared radical generator;
- rationalizes automatically even when factoring or reconstruction is shorter;
- sees `A+B sqrt(d)` as something to expand numerically rather than reverse-engineer.

## MISSING_BRIDGES

`A-B1` Radical expressions have a basis: reduce each term to the same irreducible radical building block before combining.

`A-B2` Use `A ± B sqrt(d)` as a recognition cue for a hidden square/cube.

`A-B3` The radical symbol is the principal root; sign information must be recovered from the outer context.

`A-B4` Rationalization is a tactical representation change, not a compulsory finishing ritual.

## INVARIANTS / STRUCTURES

- extraction of perfect nth powers;
- common irreducible radical basis;
- conjugate product and reverse binomial identities;
- principal-root nonnegativity.

## REPRESENTATIONS

- `sqrt(km^2) <-> |m|sqrt(k)` in full real-variable form;
- `nthroot(a^m) <-> a^(m/n)` only under appropriate real-domain interpretation;
- `A±B sqrt(d) <-> (sqrt(m)±sqrt(n))^2` when the match exists;
- conjugate pair `u+v`, `u-v`.

## FIRST_MOVE_CUES

- many radicals share the same non-perfect residue -> rewrite to a common basis;
- nested radical or `A±B sqrt(d)` -> test whether it is a square before doing anything else;
- fractional power of a surd pair -> reconstruct the inside first;
- denominator containing a conjugate -> ask whether rationalization exposes a simpler invariant; do not rationalize automatically.

## DECISION_BOUNDARIES

`A-DB1` `sqrt(ab)` under valid real conditions vs false `sqrt(a+b)=sqrt(a)+sqrt(b)`.

`A-DB2` simplify-to-common-basis vs reconstruct-hidden-square.

`A-DB3` rationalize vs factor/common-basis first.

`A-DB4` `sqrt(x^2)=|x|` vs solutions of `u^2=x^2`, which are `u=±x`.

`A-DB5` even root vs odd root: real principal even roots are non-negative; real odd roots preserve sign.

## MISCONCEPTION_TRAPS

- distributing a radical over addition/subtraction;
- forgetting absolute value in `sqrt(x^2)`;
- treating the radical symbol as “±”; 
- expanding a high power before reconstructing a hidden square/cube;
- rationalizing by reflex when it increases complexity.

## TRANSFER_ENDPOINTS

- mixed nth-root expression whose common basis is not stated;
- conjugate/fractional-power expression where reconstruction eliminates a large expansion;
- variable radical requiring a principal-root sign case;
- item where rationalization is valid but inferior to symmetry/factoring.

## SOURCE_CUSTODY

Clean scored mechanism anchors:

- `NMTC-BH-P-2018-Q01` — common square-root basis;
- `NMTC-BH-P-2023-Q21` — nested-radical reconstruction;
- `NMTC-BH-P-2023-Q26` — common cube-root basis;
- `NMTC-BH-P-2024-Q26` — structured radical normalization;
- `NMTC-BH-P-2025-Q03` — common nth-root factor;
- `NMTC-BH-P-2025-Q04` — conjugate surd square/cube.

Source-sensitive bridge only:

- `NMTC-BH-P-2023-Q04` — cube-root identity mechanism; notation/options remain sensitive.

Author-created foundation required:

- principal-root meaning;
- rationalization method-choice contrasts;
- legal/illegal radical distribution;
- variable-domain examples.

---

# 6. Stream W1-B — Exponent normalization

## PRIOR_KNOWLEDGE

- positive integer exponent laws;
- simple negative/fractional exponent notation;
- solve `a^x=a^k` for a familiar valid base.

## LIKELY_HALF_KNOWLEDGE

- exponent laws are memorized as symbolic templates but not tied to multiplication/reciprocal structure;
- negative exponents are confused with negative numbers;
- related bases such as 4, 8 and 2 are treated separately;
- logs are introduced prematurely when common-base normalization would solve the problem more cheaply.

## MISSING_BRIDGES

`B-B1` Every exponent law must preserve base grouping and operation structure.

`B-B2` Negative exponent means multiplicative inverse: `a^-n=1/a^n`, not a negative value.

`B-B3` Fractional exponent links powers and radicals; it is a representation bridge.

`B-B4` Repeated exponential objects can be named as one positive algebraic variable.

## INVARIANTS / STRUCTURES

- same-base exponent addition/subtraction;
- power-of-a-power multiplication;
- reciprocal meaning of negative exponents;
- common-base or common-ratio normalization;
- positivity of `a^x` for `a>0`.

## REPRESENTATIONS

- `8^x <-> 2^(3x)`;
- `a^-x <-> 1/a^x`;
- `a^(m/n) <-> nthroot(a^m)` under valid interpretation;
- homogeneous expressions in `2^x,3^x` -> ratio variable such as `(2/3)^x`;
- repeated `a^x` -> `t` with `t>0`.

## FIRST_MOVE_CUES

- bases are powers of the same number -> normalize bases before considering logs;
- `a^(2x),a^x,1` pattern -> set `t=a^x`;
- homogeneous two-base powers -> divide by one power and set a ratio variable;
- negative/fractional exponents -> rewrite explicitly as reciprocal/radical if sign meaning is unstable.

## DECISION_BOUNDARIES

`B-DB1` same-base normalization vs logarithms.

`B-DB2` negative exponent vs negative base: `a^-n` is not `(-a)^n`.

`B-DB3` `(-a)^n` vs `-a^n`.

`B-DB4` valid product law `a^m a^n=a^(m+n)` vs false addition law `a^m+a^n=a^(m+n)`.

`B-DB5` repeated power substitution vs solving the exponent immediately.

## MISCONCEPTION_TRAPS

- roaming reciprocal/negative-sign errors;
- treating exponentiation as linear distribution over addition;
- cancelling exponents across an addition;
- ignoring `t>0` after `t=a^x`;
- using logarithms on an equation already reducible by common-base structure.

## TRANSFER_ENDPOINTS

- mixed bases reducible to prime-base powers;
- ratio-normalization problem with no obvious single base;
- quadratic/cubic algebra in `a^x` with positivity filtering;
- fractional/negative exponent expression disguised as a radical simplification.

## SOURCE_CUSTODY

Clean scored mechanism anchors:

- `NMTC-BH-P-2023-Q07` — exponential ratio normalization;
- `NMTC-BH-P-2024-Q04` — same-base normalization;
- `NMTC-BH-P-2024-Q09` — exponential-to-algebra substitution.

Source-sensitive bridge only:

- `NMTC-BH-P-2023-Q20` — exponent/radical system linearization; notation remains delicate.

Author-created foundation required:

- negative exponent meaning;
- fractional exponent meaning;
- false-distribution contrasts;
- positivity filtering after exponential substitution.

---

# 7. Stream W1-C — Reversible vs non-reversible transformations

## PRIOR_KNOWLEDGE

- “do the same thing to both sides”;
- square an equation to remove a square root;
- substitute candidates back when told.

## LIKELY_HALF_KNOWLEDGE

- views all same-operation steps as equivalent;
- knows the word “extraneous” but not the logical mechanism;
- divides by a variable expression as if it were a non-zero constant;
- forgets to distinguish domain validity from algebraic candidacy.

## MISSING_BRIDGES

`C-B1` Separate `equivalent equation` from `candidate equation`.

`C-B2` An invertible function on the relevant domain gives a reversible step.

`C-B3` Squaring is many-to-one on the reals: `a=b => a^2=b^2`, but the converse need not hold.

`C-B4` Cubing is one-to-one on the reals and is reversible there.

`C-B5` Multiplying by a variable expression can add candidates where that multiplier is zero; dividing by it can lose valid zero-case solutions.

`C-B6` Domain restrictions must be written before the risky transformation, not reconstructed from memory at the end.

## INVARIANTS / STRUCTURES

- solution-set preservation under reversible transformations;
- implication-only candidate generation under non-injective transforms;
- zero-case preservation;
- original-domain authority.

## REPRESENTATIONS

Use transformation arrows deliberately:

- `<=>` only when both directions are justified on the stated domain;
- `=>` when the step preserves every original solution but may create candidates.

Maintain a side ledger:

```text
DOMAIN / NON-ZERO CONDITIONS
D0: ...
D1: ...
CANDIDATES: ...
VALID AFTER ORIGINAL CHECK: ...
```

## FIRST_MOVE_CUES

- square root equation -> write radicand and side-sign restrictions before squaring;
- planned squaring -> mark the step `=>` unless equivalence conditions are explicitly secured;
- division by `g(x)` -> ask `g(x)=0?` before dividing;
- multiplication by `g(x)` -> recognize that zero values can make the transformed equality lose information;
- odd-root/cube transform over reals -> exploit reversibility.

## DECISION_BOUNDARIES

`C-DB1` squaring vs cubing.

`C-DB2` multiply/divide by non-zero constant vs expression that may vanish.

`C-DB3` algebraic candidate vs valid original solution.

`C-DB4` taking the principal square root vs solving a squared equation.

`C-DB5` isolate first then square vs square a complicated radical equation immediately.

## MISCONCEPTION_TRAPS

- `same operation on both sides` treated as automatic equivalence;
- failure to check original equation after even-power transformation;
- dividing by a zero-capable factor and losing a solution;
- accepting transformed polynomial multiplicity as the count of distinct original solutions;
- forgetting side-sign conditions such as a principal radical equaling a negative expression.

## TRANSFER_ENDPOINTS

- radical equation with one extraneous candidate;
- equation where division by a factor would lose the zero case;
- compare two nearly identical transformations, one reversible and one implication-only;
- source-integrity case where transformed multiplicity disagrees with the printed/key interpretation.

## SOURCE_CUSTODY

Clean scored mechanism anchor:

- `NMTC-BH-P-2018-Q26` — radical-ratio equation; isolate/cross-multiply/square/check.

Source-conflict evidence only:

- `NMTC-BH-P-2025-Q18` — printed real cube-root equation versus provisional-key multiplicity convention. Do not repair or normalize it into a clean exercise.

Author-created foundation required:

- explicit `<=>` versus `=>` contrasts;
- multiply/divide-by-zero-capable-expression examples;
- isolate-before-square method-choice pairs.

---

# 8. Stream W1-D — Reciprocal invariants

## PRIOR_KNOWLEDGE

- expand `(a+b)^2` and `(a+b)^3`;
- solve simple quadratics;
- reciprocal notation.

## LIKELY_HALF_KNOWLEDGE

- can derive `x^2+1/x^2` after seeing the trick;
- tends to solve the quadratic for `x` first;
- does not see higher-power recurrence as the same invariant repeated.

## MISSING_BRIDGES

`D-B1` Symmetric reciprocal targets belong to an invariant variable, not usually to explicit roots.

`D-B2` Higher powers can be generated recursively from `S1=x+1/x`.

`D-B3` The reciprocal structure requires `x!=0`; this is part of the domain ledger.

## INVARIANTS / STRUCTURES

For `x!=0`, let `S_n=x^n+x^-n`.

Then:

- `S_0=2`;
- `S_1=x+1/x`;
- `S_n=S_1 S_(n-1)-S_(n-2)`.

The pair `{x,1/x}` is unchanged by swapping the two members.

## REPRESENTATIONS

- direct reciprocal pair;
- symmetric power sums;
- low-order identity;
- recurrence.

## FIRST_MOVE_CUES

- target contains equal positive/negative powers -> define `S_n` or start from `x+1/x`;
- coefficients are symmetric under `x <-> 1/x` -> divide by a middle power and expose reciprocal symmetry;
- only symmetric target is requested -> do not solve for `x`.

## DECISION_BOUNDARIES

`D-DB1` invariant reduction vs explicit quadratic solving.

`D-DB2` symmetric reciprocal target vs asymmetric target that really needs `x`.

`D-DB3` recurrence vs repeated fresh expansion.

## MISCONCEPTION_TRAPS

- solving for `x` and introducing unnecessary radicals;
- forgetting `x!=0`;
- sign error in the recurrence;
- treating `x+1/x` as if it were `(x+1)/x`.

## TRANSFER_ENDPOINTS

- high-power reciprocal sum with no explicit `x` required;
- palindromic expression reduced by division and reciprocal substitution;
- radical ratio that becomes `t+1/t` only after a representation switch.

## SOURCE_CUSTODY

Clean scored mechanism anchors:

- `NMTC-BH-P-2018-Q21` — reciprocal cube-root invariant;
- `NMTC-BH-P-2025-Q09` — symmetric radical ratio leading to reciprocal structure.

---

# 9. Stream W1-E — Logarithms as exponents

## PRIOR_KNOWLEDGE

- basic notation such as `log_2 8=3`;
- product/quotient/power log laws may be memorized;
- simple change-of-form tasks.

## LIKELY_HALF_KNOWLEDGE

- treats log laws as unrelated formulas;
- forgets base/argument restrictions;
- may attempt `log(a+b)=log a+log b` by analogy;
- knows inverse notation but does not use it to simplify exact exponent/log expressions.

## MISSING_BRIDGES

`E-B1` A logarithm is the exponent required to produce a positive number from a valid base.

`E-B2` Product/quotient/power laws are consequences of exponent laws.

`E-B3` Inverse cancellation is exact only when base/domain conditions are valid.

`E-B4` Change of base is a representation tool, not a compulsory formula.

## INVARIANTS / STRUCTURES

For `b>0`, `b!=1`, `x>0`:

`log_b x=y <=> b^y=x`.

Consequences:

- multiplication of positive arguments corresponds to addition of exponents;
- quotient corresponds to subtraction;
- valid powers correspond to scalar multiplication of the log value;
- `b^(log_b x)=x`.

## REPRESENTATIONS

- exponential statement;
- logarithmic statement;
- common-base log representation;
- exact inverse pair.

## FIRST_MOVE_CUES

- asked to interpret a log -> rewrite as an exponent statement;
- a log law is uncertain -> derive from exponent form rather than guess;
- exponent and log share a base -> test inverse cancellation before computing decimals;
- different log bases encode a simple relation -> move to a common base only if it shortens the algebra.

## DECISION_BOUNDARIES

`E-DB1` product/quotient/power log laws vs nonexistent sum/difference laws.

`E-DB2` exact inverse simplification vs decimal approximation.

`E-DB3` common-base exponent route vs taking logarithms unnecessarily.

`E-DB4` valid logarithm vs invalid base/argument.

## MISCONCEPTION_TRAPS

- `log(a+b)` splitting;
- ignoring argument positivity;
- allowing base 1 or non-positive real base in ordinary real logarithm work;
- using calculator approximations before structural cancellation;
- treating `log_b x` as multiplication of symbols rather than an exponent quantity.

## TRANSFER_ENDPOINTS

- rebuild each log law from exponent laws without a formula sheet;
- exact mixed log/exponent simplification;
- choose between common-base exponent solving and logarithmic transformation;
- domain-invalid near-miss with identical surface algebra.

## SOURCE_CUSTODY

Clean scored mechanism bridge/anchors:

- `NMTC-BH-P-2024-Q28` — exact log-exponent simplification;
- `NMTC-BH-P-2024-Q12` and `NMTC-BH-P-2025-Q12` — log quantities used as transformed algebra variables;
- `NMTC-BH-P-2025-Q27` — log-to-algebra system conversion.

Author-created foundation is mandatory for log definition/laws because PYQs mostly assume them.

---

# 10. Stream W1-F — Log-to-algebra conversion & source/domain QC

## PRIOR_KNOWLEDGE

- solve a quadratic after substitution is supplied;
- basic log laws;
- check a final numerical answer if prompted.

## LIKELY_HALF_KNOWLEDGE

- mechanically sets `t=log_b x` even when a larger object repeats;
- drops `t>=0` after a square-root substitution;
- forgets positivity once the logs have been converted away;
- treats a key as an authority over recomputed mathematics.

## MISSING_BRIDGES

`F-B1` Choose the entire repeated object as the algebraic variable.

`F-B2` Every substitution carries a range/domain into the transformed algebra.

`F-B3` Logarithmic equalities can encode simple power relations; solve the smaller algebra, then restore positivity.

`F-B4` Source/key disagreement is a separate QC state, not a license to edit the mathematics.

## INVARIANTS / STRUCTURES

- repeated-object substitution;
- injectivity of valid logs/exponentials;
- argument/base domain persistence;
- map-back filtering;
- source custody.

## REPRESENTATIONS

- `t=log_b x`;
- `u=sqrt(log_b x)` with `u>=0`;
- common-base log equality -> algebraic power relation;
- transformed algebra + domain ledger;
- source record: printed form / derived mathematics / key disposition.

## FIRST_MOVE_CUES

- one log object repeats polynomially -> set that object to `t`;
- `sqrt(log_b x)` repeats -> set the square-rooted log itself to `u`;
- same valid log base on both sides -> use injectivity after checking positive arguments;
- different related bases -> express in a common base or exponent language;
- key disagrees with verified mathematics -> stop and classify source evidence; do not edit the problem silently.

## DECISION_BOUNDARIES

`F-DB1` `t=log_b x` vs `u=sqrt(log_b x)`.

`F-DB2` transformed algebraic root vs domain-valid original root.

`F-DB3` equality of valid same-base logs vs manipulation with an invalid argument.

`F-DB4` source conflict vs learner calculation error.

`F-DB5` change of base because it reduces structure vs change of base by reflex.

## MISCONCEPTION_TRAPS

- substitution without range restriction;
- forgetting to map all branches back to positive `x`;
- using a log equality to equate arguments before validating the log expressions;
- accepting a root that makes a log argument zero/negative;
- rewriting a conflicted source to force a provisional key.

## TRANSFER_ENDPOINTS

- repeated-log expression with two plausible substitutions but only one efficient choice;
- log system that becomes a low-degree algebraic system;
- domain-invalid algebraic candidate;
- source/key conflict requiring a disposition statement rather than a repaired exercise.

## SOURCE_CUSTODY

Clean scored anchors:

- `NMTC-BH-P-2024-Q12` — logarithmic variable substitution;
- `NMTC-BH-P-2024-Q28` — exact log-exponent simplification;
- `NMTC-BH-P-2025-Q12` — `sqrt(log)` substitution;
- `NMTC-BH-P-2025-Q27` — log-system algebraic conversion.

Source-sensitive bridge:

- `NMTC-BH-P-2023-Q20` — useful exponent/radical linearization, but exact notation is delicate.

Source-conflict QC exemplar:

- `NMTC-BH-P-2025-Q18` — retained only to teach source/convention integrity, not as a clean log exercise.

---

# 11. Cross-stream bridge graph

```text
COMMON BASIS / PERFECT POWER
        |
        +-------------------------+
        |                         |
        v                         v
RADICAL <-> FRACTIONAL EXPONENT   EXPONENT BASE NORMALIZATION
        |                         |
        |                         v
        |                  REPEATED-POWER VARIABLE
        |                         |
        +------------+------------+
                     |
                     v
             SMALLER ALGEBRA
                     |
          +----------+----------+
          |                     |
          v                     v
REVERSIBILITY CHECK      RECIPROCAL INVARIANT
          |                     |
          +----------+----------+
                     |
                     v
             DOMAIN / ZERO LEDGER
                     |
                     v
LOG <-> EXPONENT INVERSE LANGUAGE
                     |
                     v
        REPEATED LOG OBJECT / LOG TO ALGEBRA
                     |
                     v
             RESTORE DOMAIN
                     |
                     v
           SOURCE / ANSWER QC
```

The cross-stream teaching sequence must therefore avoid treating the six streams as sealed chapters. The same bridges recur:

1. choose a representation;
2. name an invariant/repeated object;
3. reduce to small algebra;
4. label transformation reversibility;
5. preserve domain/range conditions;
6. map back and check.

---

# 12. Mandatory decision-boundary matrix

| ID | Looks similar | Correct boundary to learn |
|---|---|---|
| `DB-01` | `sqrt(ab)` and `sqrt(a+b)` | product splitting can be valid under real-domain conditions; sum splitting is generally false |
| `DB-02` | `sqrt(x^2)` and solving `u^2=x^2` | principal root gives `|x|`; an equation in `u` may have two signs |
| `DB-03` | common radicals and hidden `A±B sqrt(d)` | first asks for basis reduction; second may demand reverse square/cube reconstruction |
| `DB-04` | rationalization and common-basis simplification | rationalize only if it exposes structure or removes a useful denominator obstacle |
| `DB-05` | `a^-n` and `(-a)^n` | negative exponent means reciprocal; negative base is a grouping/sign issue |
| `DB-06` | `a^m a^n` and `a^m+a^n` | exponent addition law belongs to multiplication, not addition |
| `DB-07` | related exponential bases and arbitrary bases | common-base normalization can avoid logs when bases are structurally related |
| `DB-08` | squaring and cubing an equation | squaring is not injective on reals; cubing is injective on reals |
| `DB-09` | multiply/divide by constant and by `g(x)` | variable factor requires a zero-case check |
| `DB-10` | explicit solve for `x` and reciprocal symmetric target | if target is invariant under `x <-> 1/x`, reduce the invariant first |
| `DB-11` | `t=log_b x` and `u=sqrt(log_b x)` | choose the whole repeated object and carry its range |
| `DB-12` | `log(MN)` and `log(M+N)` | product law is inherited from exponent addition; no corresponding sum law |
| `DB-13` | exact inverse pair and decimal evaluation | preserve exact `b^(log_b x)` structure before approximating |
| `DB-14` | transformed algebraic root and original solution | transformed roots are candidates until original domain/equivalence is checked |
| `DB-15` | wrong learner result and source conflict | recompute first; if mathematics is sound and source/key conflicts, preserve the conflict rather than “fix” it |

---

# 13. Misconception -> diagnostic -> repair map

| Misconception code | Observable wrong move | Likely gap | Smallest repair contrast |
|---|---|---|---|
| `M-RAD-DISTRIBUTE` | `sqrt(a+b)=sqrt(a)+sqrt(b)` | operation-structure | compare product and sum using one numerical counterexample |
| `M-PRINCIPAL-SIGN` | `sqrt(x^2)=x` or `±x` | principal-root concept | compare `x=5` and `x=-5`; then separate radical notation from equation solving |
| `M-NEGEXP-SIGN` | `a^-2=-a^2` or sign drifts | reciprocal/inverse | rewrite negative exponent as an explicit reciprocal before simplifying |
| `M-EXP-ADD` | `a^m+a^n=a^(m+n)` | operation-structure | contrast multiplication of same bases with addition |
| `M-BASE-BLIND` | takes logs immediately | representation choice | pair with a same-base equivalent solvable without logs |
| `M-SQUARE-EQUIV` | accepts all squared-equation roots | reversibility | compare `x=2` with squared equation `x^2=4` |
| `M-DIVIDE-ZERO` | divides by `x-a` and loses `x=a` | zero-case/domain | solve once by factoring, once by division, compare solution sets |
| `M-RECIP-OVERSOLVE` | solves for `x` when `x+1/x` is enough | invariant recognition | ask only for `x^2+x^-2` from known `x+x^-1` |
| `M-LOG-SUM` | splits `log(a+b)` | false analogy | compare exponent-derived product law with a numerical sum counterexample |
| `M-LOG-DOMAIN` | accepts non-positive argument | condition/domain | transformed algebra root versus original log expression |
| `M-SUB-RANGE` | accepts negative `u` for `u=sqrt(log_b x)` | substitution range | write `u>=0` beside definition before solving |
| `M-DECIMAL-EARLY` | approximates exact log/exponent pair | representation | exact inverse cancellation versus calculator route |
| `M-SOURCE-FORCE` | changes sign/interpretation to match key | source integrity | separate printed source, derivation and key as three records |

---

# 14. First-move atlas to be automatized later

| Visible cue | First move to train |
|---|---|
| several square/cube/nth roots with related radicands | extract perfect powers and build a common radical basis |
| `A±B sqrt(d)` or nested radical | test a reverse square/cube identity before expansion |
| `sqrt(g(x)^2)` | write `|g(x)|` unless a known sign removes the absolute value |
| related exponential bases | rewrite to one base before using logarithms |
| `a^(2x), a^x, 1` pattern | set `t=a^x`, record `t>0` |
| homogeneous powers of two bases | divide by one power and set a ratio variable |
| square-root equation | write domain/side-sign restrictions, isolate, then square if needed |
| planned division by `g(x)` | split/check `g(x)=0` before dividing |
| symmetric `x^n+x^-n` | use reciprocal invariant/recurrence; do not solve `x` first |
| log notation uncertain | convert to exponent form |
| repeated `log_b x` | set `t=log_b x` and preserve `x>0` |
| repeated `sqrt(log_b x)` | set the whole object `u=sqrt(log_b x)`, record `u>=0` |
| equal logs with related bases | common-base/exponent conversion after domain check |
| exponent and log share a base | test exact inverse cancellation |
| source/key disagreement | recompute independently, then classify source disposition |

---

# 15. Transfer endpoint map

Wave 2/4 must eventually prove all of these without chapter labels.

`T-01` Radical basis recognition with nth roots and fractional exponents mixed in one expression.

`T-02` Hidden surd square/cube where rationalization is possible but structurally inferior.

`T-03` Principal-root sign problem embedded inside an equation rather than asked directly.

`T-04` Exponential equation that looks like it needs logs but collapses by base normalization.

`T-05` Exponential equation with no single obvious base but a ratio variable gives low-degree algebra.

`T-06` Radical equation where a non-reversible step creates an extraneous candidate.

`T-07` Equation where dividing by a variable factor would lose a valid zero case.

`T-08` Reciprocal high-power target solvable by recurrence without finding the hidden variable.

`T-09` Log problem requiring reconstruction from exponent meaning rather than a memorized law.

`T-10` Repeated-log problem where the efficient substitution is the outer repeated object.

`T-11` Log system that becomes a power/algebra relation, with one algebraic branch rejected by domain.

`T-12` Exact log/exponent expression where decimal work is deliberately a trap.

`T-13` Mixed item where the learner must state whether each transformation arrow is `<=>` or `=>`.

`T-14` Source-integrity item requiring the learner to preserve a conflict rather than force a key.

---

# 16. Source-custody overlay

## CLEAN_SCORED_ANCHOR

- `NMTC-BH-P-2018-Q01`
- `NMTC-BH-P-2018-Q21`
- `NMTC-BH-P-2018-Q26`
- `NMTC-BH-P-2023-Q07`
- `NMTC-BH-P-2023-Q21`
- `NMTC-BH-P-2023-Q26`
- `NMTC-BH-P-2024-Q04`
- `NMTC-BH-P-2024-Q09`
- `NMTC-BH-P-2024-Q12`
- `NMTC-BH-P-2024-Q26`
- `NMTC-BH-P-2024-Q28`
- `NMTC-BH-P-2025-Q03`
- `NMTC-BH-P-2025-Q04`
- `NMTC-BH-P-2025-Q09`
- `NMTC-BH-P-2025-Q12`
- `NMTC-BH-P-2025-Q27`

## SOURCE_SENSITIVE_EVIDENCE

- `NMTC-BH-P-2023-Q04` — useful cube-root identity mechanism; notation/options inconsistent in secondary evidence.
- `NMTC-BH-P-2023-Q20` — useful exponent/radical linearization; exact notation delicate.

These may inform bridges but must not be promoted as clean canonical anchors.

## SOURCE_CONFLICT_EVIDENCE

- `NMTC-BH-P-2025-Q18` — printed real cube-root equation and provisional-key root/multiplicity convention conflict. Preserve exactly as conflict evidence.

## BONUS_EVIDENCE

- None identified for the core Radical / Exponent / Log mechanism set in the current topic Source Coverage Map.
- Do not create or infer a bonus recurrence signal.

## AUTHOR_CREATED_FOUNDATION required by coverage gaps

- negative and fractional exponent meaning;
- principal square-root meaning and `sqrt(a^2)=|a|`;
- rationalization only when structurally useful;
- valid/invalid exponent-distribution contrasts;
- `<=>` versus `=>` transformation logic;
- division/multiplication by an expression that may vanish;
- log definition and base/argument domains;
- derivation of log product/quotient/power laws;
- exponential/log injectivity and inverse cancellation;
- explicit extraneous-candidate checking.

## AUTHOR_CREATED_TRANSFER

Required later for disguised mixed mastery. Author-created items must carry no fake NMTC year/question attribution.

---

# 17. Wave-1 interface contract derived from this map

Every W1-A ... W1-F stream must return a compact interface with exactly these fields before integration:

1. `CONCEPTS`
2. `PREREQUISITES`
3. `RECOGNITION_CUES`
4. `FIRST_MOVES`
5. `INVARIANTS`
6. `REPRESENTATION_SWITCHES`
7. `REVERSIBILITY_OR_DOMAIN_CONDITIONS`
8. `DECISION_BOUNDARIES`
9. `MISCONCEPTION_TRAPS`
10. `CONTRAST_PAIRS`
11. `TRANSFER_MECHANISMS`
12. `SOURCE_IDS_AND_DISPOSITIONS`
13. `CANDIDATE_MASTERY_ITEMS`
14. `DIAGNOSTIC_TAGS`
15. `H3_TO_H0_FADE_PLAN`

No stream is integration-ready if it contains formulas and exercises but lacks method-choice boundaries or condition/domain custody.

---

# 18. Wave-0 completion checks encoded in the map

| Requirement | Map location | Status |
|---|---|---|
| prior knowledge | Sections 2, 5–10 | PASS |
| likely half-knowledge | Sections 2, 5–10 | PASS |
| missing bridges | Sections 2, 5–10 | PASS |
| invariants/structures | Sections 3, 5–10 | PASS |
| representations | Sections 4, 5–10 | PASS |
| decision boundaries | Sections 5–12 | PASS |
| misconception traps | Sections 5–13 | PASS |
| first-move cues | Sections 5–10, 14 | PASS |
| transfer endpoints | Sections 5–10, 15 | PASS |
| source custody | Sections 5–10, 16 | PASS |
| clean/sensitive/conflict separation | Section 16 | PASS |
| bonus evidence isolated | Section 16 — none identified | PASS |
| author-created foundation gaps explicit | Section 16 | PASS |
| reversibility/domain as cross-stream bridge | Sections 1, 7, 11–14 | PASS |
| concept map before new teaching prose | this file is the first Issue #45 Wave-0 authoring artifact | PASS |

---

# 19. Successor execution state

Wave 1 has now implemented the Section 17 contract in six independent interface files under `Wave1_Interfaces/`.

Current status:

- W1-A through W1-F interfaces: PASS;
- 15/15 interface fields: PASS across 6/6;
- candidate mastery design pool: 28;
- independent candidate mathematics recheck: 28/28 PASS;
- source custody unchanged: 16 clean, 2 source-sensitive, 1 conflict, no topic-specific bonus evidence identified;
- First-Step remains intentionally untouched as a rebuild product until after Wave 2 teaching;
- next allowed state: `WAVE2_INTEGRATED_ASSIMILATION_BOOK`.

See `Wave1_Interfaces/Wave1_Integration_Readiness_Matrix.md` for the detailed audit.
