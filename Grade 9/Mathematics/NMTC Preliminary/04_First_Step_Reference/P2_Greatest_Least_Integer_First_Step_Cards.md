# P2 Greatest / Least Integer Functions — First-Step Cards

Use these before calculating.

| Code | Trigger | First move | Trap |
|---|---|---|---|
| `FL` | `floor(f(x))=m` | write `m<=f(x)<m+1` | losing the open right endpoint |
| `CE` | `ceil(f(x))=m` | write `m-1<f(x)<=m` | copying floor endpoints |
| `NEG` | negative input | locate between consecutive integers | truncating toward zero |
| `FR` | fractional part `{x}` | write `x=floor(x)+{x}` with `0<={x}<1` | treating it as signed decimal digits |
| `RF` | ceiling/floor reflection | use `ceil(x)=-floor(-x)` | sign loss |
| `SH` | integer shift | pull integer outside floor/ceiling | using rule for noninteger shifts |
| `FI` | floor inequality | convert by integer threshold | replacing strict endpoint incorrectly |
| `CI` | ceiling inequality | convert by integer threshold | replacing strict endpoint incorrectly |
| `NX` | expression contains both `x` and `floor(x)` | set `n=floor(x)`, enforce `n<=x<n+1` | solve algebra but forget interval consistency |
| `NE` | nested floor/ceiling | collapse outer operator if inner value is integer | simplifying noninteger inner forms illegally |
| `SUM` | floor of sum / sum of floors | set `x=a+r`, `y=b+s` | assuming additivity |
| `CNT` | count integers in real interval | first=`ceil(left)`, last=`floor(right)` | mishandling open integer endpoints |
| `SQ` | `floor(sqrt(...))` | translate to consecutive-square interval | squaring without nonnegative domain |
| `QC` | claimed PYQ/frequency | check whether floor is primary mechanism or only final bridge | inflating sparse evidence |

## Four mandatory contrasts

### 1. Floor vs truncation

`floor(-2.4)=-3`, not `-2`.

### 2. Floor vs ceiling equation

`floor(y)=m`: `m<=y<m+1`.

`ceil(y)=m`: `m-1<y<=m`.

### 3. Primary vs incidental mechanism

A problem ending with `floor(answer)` is not automatically a floor-function problem.

### 4. Solve vs verify

After setting `n=floor(x)`, every algebraic candidate must satisfy its own defining interval.
