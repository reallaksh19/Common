# NT-02 - Source Coverage Map

Status: `SOURCE_GROUNDED__3_ANCHORS_INDEPENDENTLY_RECOMPUTED`

| ID | Key | Mechanism | Independent result |
|---|---:|---|---:|
| `IOQM-2024-Q03` | 25 | last two digits / powers mod 100 | 25 |
| `IOQM-2024-Q23` | 31 | distinct fourth-power residues / collision test | 31 |
| `IOQM-2025-Q20` | 42 | global period of `n^n mod 7` | 42 |

All three are clean historical anchors in the corpus verification authority. Exact printed wording remains controlled by the official paper.

## Q03 independent audit

`5^2=25 (mod 100)`. If `5^k=25 (mod 100)` for `k>=2`, multiplying by 5 gives `5^(k+1)=125=25 (mod 100)`. Hence the last two digits of `5^2024` are **25**.

## Q23 independent audit

The verified source asks for the first modulus under which `1^4,2^4,...,14^4` have distinct residues. For modulus below 14, pigeonhole already prevents 14 distinct classes. For each modulus 14 through 30 an explicit collision exists; e.g. modulo 14, `6^4=8^4`; modulo 17, `1^4=4^4`; modulo 29, `2^4=5^4`. Modulo 31 the residues are

`1,16,19,8,5,25,14,4,20,18,9,28,10,7`,

all distinct. Therefore the first modulus is **31**.

## Q20 independent audit

Let `f(n)` be the residue of `n^n` modulo 7. A universal period T must preserve the zero positions, so `7|T`. For numbers coprime to 7, once the base residue is preserved, we also need `a^T=1 (mod 7)` for every nonzero residue `a`. Residue 3 has order 6 modulo 7, so `6|T`. Thus `42|T`. Conversely adding 42 preserves both base modulo 7 and exponent modulo 6, so T=42 works. Minimum period: **42**.

## Source-custody note

The plain-text classifier field for Q23 can visually flatten superscripts; the verified mathematical statement and official paper are authority for exact-stem use. This is not treated as a historical source conflict.
