# Software design blueprint

Use for architecture, domain-boundary or non-trivial behavioral change.

Procedure: state changed capability; trace current production path; identify state ownership and authority; prefer cohesion and narrow coupling; avoid a second source-of-truth; make failure semantics explicit; preserve test seams/rollback; record deliberate non-solves; verify design against EP acceptance rather than aesthetic preference.

A design smell is a quality finding unless it violates acceptance, safety or an explicit invariant.