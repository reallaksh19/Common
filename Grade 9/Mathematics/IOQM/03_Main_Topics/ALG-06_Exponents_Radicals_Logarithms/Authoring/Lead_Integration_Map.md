# ALG-06 Topic-Lead Integration Map

Status: `INTERFACES_COMPLETE_READY_FOR_INTEGRATED_PROSE`

## Learner promise
By the end of the topic, the learner should not ask “which radical trick do I remember?” but instead run:

`DOMAIN -> NORMALIZE -> CHOOSE REPRESENTATION -> RECORD EQUIVALENCE/IMPLICATION -> SOLVE -> CHECK ORIGINAL`.

## Integrated order
1. **Reconnect: exponents as representation** — normalize powers, common bases, negative/rational exponents only with valid domains.
2. **Principal roots are signed objects** — `sqrt(u)>=0`; `sqrt(x^2)=|x|`; radicand restrictions before algebra.
3. **Radical simplification and conjugates** — use factoring/rationalization only when it exposes structure.
4. **Nested radicals** — name the inner radical, exploit sign/irrationality/integer structure, do not square blindly.
5. **Reversibility doctrine** — distinguish `⇔` from `⇒`; squaring generates candidates unless sign conditions make it reversible.
6. **Logarithms as exponents** — define domain first, convert to exponent relations, use reciprocal-log identities only under valid bases.
7. **Integer/domain filters** — terminal filters after algebraic structure, not a separate number-theory chapter.
8. **Mixed route selection and transfer** — common-base vs log, conjugate vs square, simple radical vs nested radical.

## Teach once globally
- principal-root convention;
- domain inventory before any radical/log move;
- `⇔` versus `⇒` notation and candidate validation;
- target-led representation choice inherited from ALG-01.

## Retrieve, do not reteach
From ALG-01: factor/expand strategically, substitution for repeated structure, identity vs solution relation, implication/equivalence awareness, original-condition checking.

## Mandatory contrast placements
- common base vs logarithm: immediately after exponent normalization;
- `sqrt(x^2)=|x|` vs `sqrt(x^2)=x`: first radical lesson;
- rationalize vs square: radical simplification lab;
- simple difference of radicals vs nested radical: before Q28;
- reversible square vs candidate-generating square: before first mixed radical equation;
- log equation vs exponent relation: first log lesson.

## Historical anchor placement
### IOQM-2023-Q02 = 54
Use after logarithm-as-exponent conversion. First line: `t=log_a b`, then `log_b a=1/t`; domain makes `t>0`. The quadratic gives `t=2,3`, hence `b=a^2` or `a^3` and 43+11=54 ordered pairs.

### IOQM-2025-Q28 = 91
Use as the late mixed anchor. Exact controlled stem is the nested radical `sqrt(x-sqrt(x+a))=sqrt(a)-y`; stale simple-radical metadata is prohibited. The teaching objective is not the final triangular-number parameter alone but the full chain: domain -> prove `y=0` -> reversible square -> set `t=x-a` -> `a=t(t-1)/2` -> largest nonsquare under 100 is 91.

## Recognition Lab targets
- choose common base vs log;
- detect principal-root sign requirement;
- classify a square as reversible or one-way;
- choose conjugation vs substitution vs squaring;
- spot nested radical structure;
- identify integer/domain filter as final rather than first move.

## First-Line Lab targets
Minimum first lines only:
- `u>=0` for `sqrt(u)`;
- `sqrt(x^2)=|x|`;
- common-base normalization line;
- conjugate multiplier;
- `t=sqrt(inner)` for nested radicals;
- sign condition before squaring;
- `t=log_a b` with base/domain declaration.

## F0 -> F4 ladder
- F0: direct domain and exponent normalization.
- F1: single radical simplification/conjugate with explicit conditions.
- F2: radical equations where squaring is reversible after a sign check.
- F3: nested radicals and log/exponent conversion with reduced prompting.
- F4: mixed changed-surface items requiring route selection and original-condition validation.

## H0 mastery design
First mastery attempt must be unlabelled/unhinted. Include at least:
- one exponent-normalization item;
- one principal-root/domain trap;
- one conjugate item;
- one nested-radical item;
- one implication-vs-equivalence item;
- one log-as-exponent item;
- one mixed integer/domain filter.

## Teacher diagnostic codes
- `DOMAIN_NOT_DECLARED`
- `PRINCIPAL_ROOT_SIGN_LOST`
- `SQUARING_STATUS_UNTRACKED`
- `EXTRANEOUS_NOT_CHECKED`
- `REPRESENTATION_TOO_EXPENSIVE`
- `LOG_DOMAIN_INVALID`
- `NESTED_RADICAL_FLATTENED`

## Source and publication gates
Historical mathematics: 2/2 PASS. Exact Q28 correction overlay consumed and independent proof recorded. Figure dependency: none for the two anchors. Before ready-for-review: authored-item keys, frozen metadata, integrated prose, practice/mastery, teacher key, canonical student/teacher PDFs, hash/blob/page count and page-by-page visual QA must pass. Classroom timing/retention/psychometrics remain `NOT_RUN`.
