"""Compatibility dispatcher for migrated Grade-4 Mathematics V2.

Canonical Grade-4 dispatch ownership moved to:
`Grade 4/V2/Mathematics/Representation/engine/primitives/dispatcher.py`.

Reusable primitive implementations remain available under Primary/Common, but the
old Primary dispatcher must not form a second Grade-4 semantic authority.
"""
from Grade4.V2.Mathematics.Representation.engine.primitives.dispatcher import (  # noqa: F401
    UnsupportedPrimaryPrimitive,
    render_primitive,
)

__all__ = ["UnsupportedPrimaryPrimitive", "render_primitive"]
