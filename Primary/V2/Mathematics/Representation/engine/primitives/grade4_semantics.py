"""Compatibility import for migrated Grade-4 semantic primitives.

Canonical ownership is `Grade 4/V2/Mathematics/Representation/...`.
New Grade-4 code should import through `Grade4.V2...`; this shim exists only for
historical Primary import paths during migration issue #340.
"""
from Grade4.V2.Mathematics.Representation.engine.primitives.grade4_semantics import (  # noqa: F401
    Grade4SemanticPrimitives,
)

__all__ = ["Grade4SemanticPrimitives"]
