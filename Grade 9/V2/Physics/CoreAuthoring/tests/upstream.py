#!/usr/bin/env python3
"""Shared in-process P-A .. P-F upstream driver for the P-G .. P-L phases.

This exists so every later phase proves itself against the *real* merged
assessment chain (P-A intake fixtures -> P-B review -> P-C scope authority ->
P-D problem semantics -> P-E learner evidence -> P-F study scope/model) rather
than against a hand-written stub of its own input.
"""
import copy, importlib.util, json, sys
from pathlib import Path

PHYS = Path(__file__).resolve().parents[2]
A = PHYS / "AssessmentIntake"
B = PHYS / "AssessmentReview"
S = PHYS / "AssessmentScope"
CAN = PHYS / "Canonical"
PD = PHYS / "ProblemSemantics"
PE = PHYS / "LearnerEvidence"
PF = PHYS / "StudySynthesis"


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def _module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


_semantics_mod = None
_evidence_mod = None
_study_mods = None


def _load_engines():
    global _semantics_mod, _evidence_mod, _study_mods
    if _semantics_mod is None:
        _semantics_mod = _module("phy_pd", PD / "engine" / "build_physics_problem_semantics.py")
    if _evidence_mod is None:
        _evidence_mod = _module("phy_pe", PE / "engine" / "infer_physics_learner_evidence.py")
    if _study_mods is None:
        if str(PF / "engine") not in sys.path:
            sys.path.insert(0, str(PF / "engine"))
        import study_scope  # noqa: E402
        import study_treatment_core  # noqa: E402
        _study_mods = (study_scope, study_treatment_core)
    return _semantics_mod, _evidence_mod, _study_mods


def build_problem_semantics():
    pd, _, _ = _load_engines()
    return pd.build_package(
        load(A / "fixtures" / "motion-question-set.fixture.json"),
        load(A / "fixtures" / "motion-topic-scope.fixture.json"),
        load(B / "registry" / "physics-item-validity-registry.json"),
        load(B / "policies" / "diagnostic-use-policy.json"),
        load(CAN / "registry" / "capabilities.json"),
        load(S / "authority" / "physics-assessment-scope-authority.json"),
        load(S / "registry" / "motion-question-scope-bindings.json"),
        load(PD / "registry" / "physics-reasoning-role-registry.json"),
        load(PD / "registry" / "physics-problem-family-registry.json"),
        load(PD / "registry" / "physics-verification-route-registry.json"),
        load(PD / "registry" / "motion-item-semantics.json"),
        load(PD / "registry" / "guide-demand-badge-policy.json"),
    )


def build_snapshot(semantics, attempts=False):
    _, pe, _ = _load_engines()
    kwargs = {}
    if attempts:
        kwargs["attempts"] = load(A / "fixtures" / "motion-attempt-set.fixture.json")
        kwargs["ledger"] = load(PE / "fixtures" / "physics-learner-evidence-ledger.fixture.json")
    return pe.build_snapshot(
        copy.deepcopy(semantics),
        load(A / "fixtures" / "motion-question-set.fixture.json"),
        load(PE / "registry" / "physics-observation-code-registry.json"),
        load(PE / "registry" / "physics-diagnostic-policy.json"),
        **kwargs,
    )


def build_upstream(attempts=False, semantics=None):
    """Return (study_scope, study_model) from the real P-A..P-F chain."""
    _, _, (study_scope_mod, study_treatment) = _load_engines()
    semantics = semantics or build_problem_semantics()
    snapshot = build_snapshot(semantics, attempts=attempts)
    scope = study_scope_mod.derive_study_scope(
        load(S / "registry" / "motion-question-scope-bindings.json"),
        load(S / "authority" / "physics-assessment-scope-authority.json"),
        copy.deepcopy(semantics),
    )
    model = study_treatment.build_model(
        copy.deepcopy(scope),
        copy.deepcopy(snapshot),
        load(PF / "policies" / "physics-treatment-policy.json"),
    )
    return scope, model


def core1_plan(attempts=False, plan_id=None):
    """Return (study_scope, study_model, core1_plan) with P-G applied."""
    sys.path.insert(0, str(PHYS / "CoreAuthoring" / "engine"))
    from build_physics_core1 import build_plan, load_pck_registry  # noqa: E402

    ca = PHYS / "CoreAuthoring"
    scope, model = build_upstream(attempts=attempts)
    plan = build_plan(
        copy.deepcopy(model),
        copy.deepcopy(scope),
        load_pck_registry(),
        load(ca / "registry" / "physics-instructional-authoring-profile.json"),
        load(ca / "registry" / "physics-core1-scope-completeness-policy.json"),
        load(ca / "registry" / "physics-problem-authoring-profile.json"),
        plan_id,
    )
    return scope, model, plan


def question_set():
    return load(A / "fixtures" / "motion-question-set.fixture.json")


def representation_bundle(core1, model, bundle_id=None):
    """Return the P-H representation bundle for a P-G plan."""
    sys.path.insert(0, str(PHYS / "Representation" / "engine"))
    from build_physics_representations import build_bundle  # noqa: E402

    rep = PHYS / "Representation"
    kwargs = {"bundle_id": bundle_id} if bundle_id else {}
    return build_bundle(
        copy.deepcopy(core1), copy.deepcopy(model), question_set(),
        load(rep / "registry" / "physics-teaching-primitive-registry.json"),
        load(rep / "registry" / "physics-page-intent-profile.json"),
        load(rep / "registry" / "physics-figure-render-contract.json"),
        **kwargs,
    )


def core2_plan(core1, model, scope, plan_id=None):
    """Return the P-I Core2 transfer plan for a P-G plan."""
    sys.path.insert(0, str(PHYS / "Core2Transfer" / "engine"))
    from build_physics_core2_transfer import build_plan as build_core2  # noqa: E402

    t = PHYS / "Core2Transfer"
    kwargs = {"plan_id": plan_id} if plan_id else {}
    return build_core2(
        load(t / "fixtures" / "physics-external-transfer-source.fixture.json"),
        load(t / "registry" / "physics-external-corpus-classification.json"),
        copy.deepcopy(core1), copy.deepcopy(model), copy.deepcopy(scope),
        load(t / "registry" / "physics-core2-authoring-profile.json"),
        load(t / "registry" / "physics-transfer-badge-policy.json"),
        load(t / "registry" / "physics-concept-segregation.json"),
        **kwargs,
    )
