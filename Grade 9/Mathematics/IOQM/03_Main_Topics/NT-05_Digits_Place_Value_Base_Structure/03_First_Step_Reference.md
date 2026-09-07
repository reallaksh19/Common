# First-Step Reference - Digits, Place Value & Base Structure

| Visible clue | First question | First useful line |
|---|---|---|
| `abc...` digit notation | what are place weights? | expand as powers of 10 |
| divisible by 9 | what is 10 mod9? | collapse to digit sum |
| divisible by 11 | what is 10 mod11? | alternating signed sum |
| block appended | how many digits in new block? | `10^k x+y` |
| `n+1` and digit sum | how many trailing 9s? | `s(n+1)=s(n)+1-9t` |
| squarefree digit product | which prime exponent would repeat? | factor allowed digits conceptually |
| base-b numeral | what are powers of b? | `sum d_i b^i` |
| count admissible strings | has arithmetic restriction been derived? | freeze restriction, then count |

## Close contrasts
- Digit sum vs digit product: additive place-value collapse versus multiplicative prime compatibility.
- Place-value reduction vs generic modular cycle: derive the decimal structure first; retrieve modular legality only as needed.
- Concatenation vs permutation: joining blocks changes numerical value by a power of the base.
- Carry reasoning vs brute force: trailing maximal digits determine the entire digit-sum jump.
- Arithmetic restriction vs string counting: different canonical jobs.
