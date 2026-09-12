"""Optional learner-facing production refinements for a copied source set.

Keep this file boring unless visual QA finds an upstream representation-selection
problem.  Fix the LearningDesign/representation selection here; do not add
question-specific pedagogy to the PDF composer.
"""
from __future__ import annotations

import copy
from typing import Any, Dict

from .build_fixture import build_primary_input as _build_base_primary_input


def build_primary_input() -> Dict[str, Any]:
    primary_input = copy.deepcopy(_build_base_primary_input())

    # Example pattern only:
    #
    # q = next(row for row in primary_input["question_set"]["questions"] if row["question_ref"] == "Q1")
    # evidence = q["evidence"]
    # evidence["representation_requirements"].append({...validated representation...})
    # evidence["learning_support_blueprint"]["primary"] = {
    #     "representation_ref": "REP-Q1-REFINED",
    #     "fidelity": "SCHEMATIC",
    #     "fade_mode": "FULL",
    # }
    #
    # Use this only when the refined representation is semantically justified by
    # the source/teaching concept.  Never expose the target answer simply to make
    # the visual look complete.

    return primary_input
