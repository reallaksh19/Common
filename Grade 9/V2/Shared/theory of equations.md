# Theory of Equations

**9) Find an eqn whose roots are $0, 1, \frac{-3}{2}, \frac{5}{2}$**

**Ans:**
$$ (x - \alpha)(x - \beta)(x - \gamma)(x - \delta) = 0 $$
$$ (x - 0)(x - 1)\left(x - \left(\frac{-3}{2}\right)\right)\left(x - \left(\frac{5}{2}\right)\right) = 0 $$
$$ (x^2 - x)\left(x^2 - \frac{5}{2}x + \frac{3}{2}x - \frac{15}{4}\right) = 0 $$
$$ x^4 - \frac{5}{2}x^3 + \frac{3}{2}x^3 - \frac{15}{4}x^2 - x^3 + \frac{5}{2}x^2 - \frac{3}{2}x^2 + \frac{15}{4}x = 0 $$
Multiply by 4.
$$ 4x^4 - 8x^3 - 11x^2 + 15x = 0 $$

---

**10) $1, 1, \alpha$ are roots of $x^3 - 6x^2 + 9x - 4 = 0$. Find $\alpha$.**

**Ans:**
$$ x^3 - 6x^2 + 9x - 4 = 0 \implies ax^3 + bx^2 + cx + d = 0 $$
$$ S_1 = \frac{-b}{a} = \frac{-(-6)}{1} = 6 = 1 + 1 + \alpha $$
$$ 2 + \alpha = 6 $$
$$ \alpha = 4 $$

(or)
$$ S_3 = \frac{-d}{a} = \frac{-(-4)}{1} = 4 $$
$$ \alpha \times 1 \times 1 = 4 $$
$$ \alpha = 4 $$

---

**11) $1, -2, 3$ are roots of $x^3 - 2x^2 + ax + 6 = 0$. Find $a$.**

**Ans:**
$$ x^3 - 2x^2 + ax + 6 = 0 $$
$$ ax^3 + bx^2 + cx + d = 0 $$
$$ (x - 1)(x - (-2))(x - 3) = 0 $$
$$ (x - 1)(x + 2)(x - 3) = 0 $$
$$ (x^2 + 2x - x - 2)(x - 3) = 0 $$
$$ x^3 - 3x^2 + 2x^2 - 6x - x^2 + 3x - 2x + 6 = 0 $$
$$ x^3 - 2x^2 - 5x + 6 = 0 $$
$$ \therefore a = -5 $$

---

**12) Product of the roots of $4x^3 + 16x^2 - 9x - a = 0$ [is 9]. Find $a$.**

*(Note: The value 9 for the product is implied from the solution)*

**Ans:**
$$ \text{Product} = \alpha\beta\gamma = \frac{-d}{a} $$
$$ 4x^3 + 16x^2 - 9x - a = 0 $$
$$ -\frac{(-a)}{4} = \frac{a}{4} $$
$$ \frac{a}{4} = 9 \quad (\text{Product}) $$
$$ a = 4(9) $$
$$ a = 36 $$

---

**13) If $\alpha, \beta, \gamma$ are roots of $x^3 - 2x^2 - 5x + 6 = 0$. Find $\alpha$ & $\beta$ if $\alpha + \beta = 1$.**

**Ans:**
$$ x^3 - 2x^2 - 5x + 6 = 0 $$
$$ S_1 = \frac{-b}{a} \implies \alpha + \beta + \gamma = 2 $$
$$ S_3 = \frac{-d}{a} \implies \alpha\beta\gamma = -6 \quad \dots (2) $$
Given:
$$ \alpha + \beta = 1 \quad \dots (1) $$
From $S_1$, since $\alpha + \beta = 1$, then $\gamma = 1$.
$$ \alpha = 1 - \beta $$
Substitute into (2):
$$ (1 - \beta)(\beta)(1) = -6 $$
$$ \beta - \beta^2 = -6 $$
$$ \beta^2 - \beta - 6 = 0 $$
$$ \beta^2 - 3\beta + 2\beta - 6 = 0 $$
$$ \beta(\beta - 3) + 2(\beta - 3) = 0 $$
$$ (\beta - 3)(\beta + 2) = 0 $$

$$ \beta = 3 \quad | \quad \beta = -2 $$
$$ \downarrow \quad | \quad \downarrow $$
$$ \alpha = -2 \quad | \quad \alpha = 3 $$

---

**14) $\alpha, \beta, \gamma$ are roots of $x^3 - 2x^2 + 3x - 4 = 0$. Find $\sum \alpha^2 \beta^2$.**

**Ans:**
$$ \sum \alpha^2 \beta^2 = \alpha^2 \beta^2 + \beta^2 \gamma^2 + \gamma^2 \alpha^2 $$
$$ = (\alpha\beta + \beta\gamma + \gamma\alpha)^2 - 2\alpha\beta\gamma(\alpha + \beta + \gamma) $$
$$ = \left(\frac{c}{a}\right)^2 - 2\left(\frac{-d}{a}\right)\left(\frac{-b}{a}\right) $$
$$ = (-3)^2 - 2(4)(2) $$
$$ = 9 - 16 $$
$$ \sum \alpha^2 \beta^2 = -7 $$

---

## Newton's sum of relations of an equation:

*   **If $x^3 + a_1 x^2 + a_2 x + a_3 = 0 \rightarrow$ Cubic equation**
    $\alpha, \beta, \gamma$ are the roots.
    Then, $S_k = \alpha^k + \beta^k + \gamma^k$

    **Formula:** $S_n + a_1 S_{n-1} + a_2 S_{n-2} + \dots + n \cdot a_n = 0$
    for $n \le 3$ (for $3^{\text{rd}}$ degree equation)

*   **If $x^4 + a_1 x^3 + a_2 x^2 + a_3 x + a_4 = 0 \rightarrow$ Biquadratic**
    $\alpha, \beta, \gamma, \delta$ are the roots.
    Then, $S_k = \alpha^k + \beta^k + \gamma^k + \delta^k$

    **Formula:** $S_n + a_1 S_{n-1} + a_2 S_{n-2} + a_3 S_{n-3} + a_4 S_{n-4} = 0$
    for $n \ge 4$ (for $4^{\text{th}}$ degree equation)

---

**1) Find the sum of $5^{\text{th}}$ power of the roots of the equation $x^4 - 7x^2 + 4x - 3 = 0$**

**Ans:**
$$ x^4 + a_1 x^3 + a_2 x^2 + a_3 x + a_4 = 0 $$
$$ a_1 = 0 $$
$$ a_2 = -7 $$
$$ a_3 = 4 $$
$$ a_4 = -3 $$

$$ S_n + a_1 S_{n-1} + a_2 S_{n-2} + a_3 S_{n-3} + a_4 S_{n-4} = 0 $$

**for $n = 1$:**
$$ S_1 + 1 \cdot a_1 = 0 $$
$$ S_1 + 1(0) = 0 $$
$$ S_1 = 0 \implies \alpha + \beta + \gamma + \delta = 0 $$

**for $n = 2$:**
$$ S_2 + a_1 S_1 + 2 \cdot a_2 = 0 $$
$$ S_2 + 0(0) + 2(-7) = 0 $$
$$ S_2 = 14 \implies \alpha^2 + \beta^2 + \gamma^2 + \delta^2 = 14 $$

**for $n = 3$:**
$$ S_3 + a_1 S_2 + a_2 S_1 + 3 \cdot a_3 = 0 $$
$$ S_3 + 0(14) + (-7)(0) + 3(4) = 0 $$
$$ S_3 = -12 \implies \alpha^3 + \beta^3 + \gamma^3 + \delta^3 = -12 $$

**for $n = 4$:**
$$ S_4 + a_1 S_3 + a_2 S_2 + a_3 S_1 + 4(a_4) = 0 $$
$$ S_4 + 0 + (-7)(14) + 4(0) + 4(-3) = 0 $$
$$ S_4 - 98 - 12 = 0 $$
$$ S_4 = 110 \implies \alpha^4 + \beta^4 + \gamma^4 + \delta^4 = 110 $$

**for $n = 5$:**
$$ S_5 + a_1 S_4 + a_2 S_3 + a_3 S_2 + a_4 S_1 = 0 $$
$$ S_5 + 0(110) + (-7)(-12) + 4(14) + (-3)(0) = 0 $$
$$ S_5 + 84 + 56 - 0 = 0 $$
$$ S_5 + 140 = 0 $$
$$ S_5 = -140 \implies \alpha^5 + \beta^5 + \gamma^5 + \delta^5 = -140 $$
