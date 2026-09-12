"""
Primitives Package for Grade 9 Pedagogical Visuals.
Exposes modular engines:
- graphs: CartesianPlotter2D, KinematicGraphRenderer, StatisticalPlotter, ThermalCurvePlotter
- diagrams: PlaneGeometryRenderer, Vector1DDiagram, FreeBodyDiagramRenderer, WaveformRenderer, BohrAtomRenderer, ParticleLatticeDiagram, OxidationLaneDiagram, CombinatorialSlotDiagram
- equations: FormulaAnatomyEngine, ValencyCrissCrossEngine, ChemicalReactionEngine, GeometryProofBlock, MathEquationBlock
- validator: VisualSemanticValidator, typed exceptions
- base: Palette, FONT_NAME, FONT_BOLD, draw_card_box, draw_pill_badge, draw_arrow
"""

from .base import (
    FONT_NAME,
    FONT_BOLD,
    FONT_OBLIQUE,
    Palette,
    draw_card_box,
    draw_pill_badge,
    draw_arrow
)

from .graphs import (
    CartesianPlotter2D,
    KinematicGraphRenderer,
    StatisticalPlotter,
    ThermalCurvePlotter
)

from .diagrams import (
    PlaneGeometryRenderer,
    Vector1DDiagram,
    FreeBodyDiagramRenderer,
    WaveformRenderer,
    BohrAtomRenderer,
    ParticleLatticeDiagram,
    OxidationLaneDiagram,
    CombinatorialSlotDiagram
)

from .equations import (
    FormulaAnatomyEngine,
    ValencyCrissCrossEngine,
    ChemicalReactionEngine,
    GeometryProofBlock,
    MathEquationBlock
)

from .validator import (
    VisualSemanticValidator,
    VisualValidationError,
    UngroundedEntityError,
    QuantitativeDiscrepancyError,
    DirectionInversionError,
    ConservationError,
    RolePolarityError,
    AreaIntegralError,
    GeometryAxiomError,
    CircleTheoremError,
    BohrCapacityError,
    WaveKinematicsError
)

__all__ = [
    "FONT_NAME",
    "FONT_BOLD",
    "FONT_OBLIQUE",
    "Palette",
    "draw_card_box",
    "draw_pill_badge",
    "draw_arrow",
    "CartesianPlotter2D",
    "KinematicGraphRenderer",
    "StatisticalPlotter",
    "ThermalCurvePlotter",
    "PlaneGeometryRenderer",
    "Vector1DDiagram",
    "FreeBodyDiagramRenderer",
    "WaveformRenderer",
    "BohrAtomRenderer",
    "ParticleLatticeDiagram",
    "OxidationLaneDiagram",
    "CombinatorialSlotDiagram",
    "FormulaAnatomyEngine",
    "ValencyCrissCrossEngine",
    "ChemicalReactionEngine",
    "GeometryProofBlock",
    "MathEquationBlock",
    "VisualSemanticValidator",
    "VisualValidationError",
    "UngroundedEntityError",
    "QuantitativeDiscrepancyError",
    "DirectionInversionError",
    "ConservationError",
    "RolePolarityError",
    "AreaIntegralError",
    "GeometryAxiomError",
    "CircleTheoremError",
    "BohrCapacityError",
    "WaveKinematicsError"
]
