# Mathematics V2 canonical reasoning authority

**Tracking:** #197  
**Stage:** MATH-V2-01  
**Lineage:** fresh from `main`; old PRs are migration sources only.

This package freezes learner-independent Mathematics reasoning semantics used by later V2 layers.

```text
Mathematical object / representation
→ structure
→ legal operation or theorem
→ transformation
→ invariant / equivalence preservation
→ conditions / domain
→ verification
```

It owns canonical capability definitions, error signatures, diagnostic probes, and problem-family reasoning checkpoints.

It does **not** own learner diagnosis, Study Synthesis treatment, teaching choreography, publication layout, longitudinal scheduling, or benchmark validation.

## Central falsifier

```text
correct modelling + invalid downstream algebra != modelling failure
```

Synthetic acceptance cases prove that word/equation modelling, system setup, and geometric modelling remain distinct from equality preservation, expression identity, binomial expansion, ordered-pair semantics, and verification.

## Verification boundary

`MATH-SOLUTION-VERIFICATION` defines how a mathematical result can be checked: substitution, equivalence, domain/constraint checking, or alternate representation. Whether a learner spontaneously initiates a check is learner evidence and is not encoded here.

## Cross-subject family tags

A capability may carry a descriptive reasoning-family tag such as `INVARIANT_TRACKING`. The tag is canonical taxonomy only; it is not a learner trait, diagnosis, or mastery state.

## Benchmark firewall

Historical learner products and benchmark/reference PRs are not producer inputs. The generated canonical package requires `benchmark_inputs = []`.
