# Recognition and First-Line Lab

For each item, write only the **best first move** or choose the best option. Do not complete a long solution unless needed to justify the choice.

## Recognition

1. For integers, an equation contains `f(mn+1)`. Which is the strongest first test?
   A. `m=7`  B. `m=0`  C. `m=n`  D. large positive m

2. For all real `x`, an equation contains `f(8-x)` and `f(x)`. What structure matters?
   A. periodicity  B. the partner map returns to x after two uses  C. divisibility  D. ordering

3. You know values at `x` and `5-x` occur in one equation. What should you manufacture?
   A. a graph  B. the equation at `5-x`  C. ten sample values  D. a sequence table

4. A relation is stated only for integers. Which substitution needs no extra justification?
   A. `x=1/2`  B. `x=sqrt(2)`  C. `x=-1`  D. `x=pi`

5. Five computed values fit `f(n)=n+1`. What is still missing?
   A. arithmetic  B. proof for every allowed input  C. another table  D. a graph

6. A problem asks whether equal outputs always force equal inputs. Which start is legitimate?
   A. assume the function is increasing  B. assume `f(a)=f(b)` and try to force `a=b`  C. draw a sketch  D. test three values

7. A problem asks whether every real number occurs as an output. Which start is legitimate?
   A. pick arbitrary target `t` and construct an input  B. test positive outputs  C. assume continuity  D. assume equal outputs force equal inputs

8. Which object is a recurrence rather than a functional equation?
   A. `f(x+y)=f(x)+f(y)`  B. `a_(n+1)=2a_n+1`  C. `f(3-x)+f(x)=7`  D. `f(xf(y))=x+y`

## First lines

9. For real `x`, `3f(4-x)+2f(x)=x+7`. Write the partner equation.

10. For integers `m,n`, `f(m+n)=f(m)+n` and `f(0)=5`. Write the substitution that determines `f(n)` immediately.

11. For integers, `f(m+n)=f(m)+f(n)+mn`. Write the substitution that reveals `f(0)`.

12. Suppose `f(x+f(y))=f(x)+y` for all reals and you want to prove that equal function values force equal inputs. Write the assumption involving two inputs.

13. For all reals, `f(x)+f(2-x)=10` and `f(2-x)-f(x)=2-2x`. Write the equation-combination move.

14. A proposed formula is `f(x)=x^2+1` for `f(x+y)=f(x)+f(y)+2xy-1`. Write the verification line to check.

15. For integers, a derived rule is `f(n+1)=f(n)+2n+1` and `f(0)=0`. State one thing you must still do before claiming the original two-variable functional equation is solved.

16. The equation contains `f(1-xy)` on an integer domain. Name two legal structural substitutions worth testing first.
