#!/usr/bin/env python3
"""Compatibility adapter for the pre-P-F synthetic StudySynthesis consumer path.

P-F owns the authoritative LearnerStudyScope/LearnerStudyModel.  LearningDesign
and Publication still exercise the older synthetic proof pipeline; keep that
pipeline isolated behind the legacy schema until those consumers migrate.
"""
from legacy_synthesize_physics_study_model import *  # noqa: F401,F403
import legacy_synthesize_physics_study_model as _legacy

_original_validate = _legacy.validate

def _compat_validate(value, schema_name):
    if schema_name == "physics-learner-study-model.schema.json":
        schema_name = "physics-legacy-learner-study-model.schema.json"
    return _original_validate(value, schema_name)

_legacy.validate = _compat_validate
synthesize = _legacy.synthesize
load = _legacy.load
main = _legacy.main

if __name__ == "__main__":
    main()
