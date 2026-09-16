# V2.5 CI evidence correction

## Purpose

This note corrects the validation interpretation used before the WP-02 completion gate.

The workflow previously contained one discovery command:

```text
python -m unittest discover -s skills/engineering-pr-delivery-v2.5/tests -p 'test*.py' -v
```

Python unittest discovery did not recurse into `tests/stress/` because that directory was not imported as a package by this invocation. The workflow compiled the stress modules, but the stress tests themselves were not executed by that command.

Therefore, historical statements describing runs such as **35088847648** and **35091290911** as executing the complete unit + synthetic stress suite were too strong. Those runs remain valid evidence for checkout/setup/compile and the root unit-discovery surface, but they are **not** evidence that every file under `tests/stress/` executed.

## Correction

The workflow now runs two explicit test steps:

```text
python -m unittest discover -s skills/engineering-pr-delivery-v2.5/tests -p 'test*.py' -v
python -m unittest discover -s skills/engineering-pr-delivery-v2.5/tests/stress -p 'test*.py' -v
```

The first corrected full-suite run exposed stale readiness fixtures and three evidence-mutation tests whose Python fixture objects aliased predecessor and successor evidence before serialization. Those fixtures were corrected rather than weakening the validators.

## First corrected whole-suite evidence

Exact branch head:

```text
33ef1ab6c1d723c8de763b28146e25319738167e
```

Workflow run:

```text
35095076892
```

Result:

```text
checkout                         PASS
Python setup                     PASS
validator dependency             PASS
compile V2.5 Python              PASS
root unit tests                  PASS
synthetic stress tests           PASS
```

The synthetic stress step executes the dedicated `tests/stress/` suite, including the WP-02 zero-context takeover/candidate-write-readiness regressions.

## Evidence rule going forward

A claim that the **complete V2.5 unit + synthetic stress suite passed** requires evidence that both explicit workflow test steps completed successfully on the claimed exact head.

Historical checkpoint artifacts are not rewritten to erase prior evidence. This correction is additive and authoritative for interpreting those historical workflow claims.
