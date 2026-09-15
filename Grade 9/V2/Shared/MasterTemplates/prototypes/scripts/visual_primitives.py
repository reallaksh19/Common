"""
Compatibility forwarder for legacy imports.
Directs all callers to the decoupled Grade 9 MasterTemplates primitives package.
"""

from pathlib import Path
import sys

PRIMITIVES_DIR = Path(__file__).resolve().parent.parent.parent
if str(PRIMITIVES_DIR) not in sys.path:
    sys.path.insert(0, str(PRIMITIVES_DIR))

from primitives import (
    FONT_NAME,
    FONT_BOLD,
    FONT_OBLIQUE,
    Palette,
    draw_card_box,
    draw_pill_badge,
    draw_arrow,
    CartesianPlotter2D,
    KinematicGraphRenderer,
    StatisticalPlotter,
    ThermalCurvePlotter,
    PlaneGeometryRenderer,
    Vector1DDiagram,
    FreeBodyDiagramRenderer,
    WaveformRenderer,
    BohrAtomRenderer,
    ParticleLatticeDiagram,
    OxidationLaneDiagram,
    CombinatorialSlotDiagram,
    FormulaAnatomyEngine,
    ValencyCrissCrossEngine,
    ChemicalReactionEngine,
    GeometryProofBlock,
    MathEquationBlock,
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

# Legacy alias functions
def draw_number_line_1d(c, x, y, w, h, title="1D REFERENCE FRAME & DISPLACEMENT STRIP"):
    return Vector1DDiagram.draw(c, x, y, w, h, title=title)

def draw_vt_graph(c, x, y, w, h, title="VELOCITY-TIME (v-t) GRAPH & INTEGRAL AREA", u=0.0, v=20.0, t_accel=5.0):
    return KinematicGraphRenderer.draw_vt_graph(c, x, y, w, h, title=title, u=u, v=v, t_accel=t_accel)

def draw_particle_model(c, x, y, w, h, title="PARTICULATE DALTON REACTION MODEL"):
    return ParticleLatticeDiagram.draw_reaction_chamber(c, x, y, w, h, title=title)

def draw_formula_anatomy(c, x, y, w, h, title="CHEMICAL FORMULA ANATOMY"):
    return FormulaAnatomyEngine.draw_formula_anatomy(c, x, y, w, h, title=title)

def draw_oxidation_state_lane(c, x, y, w, h, title="OXIDATION STATE LANE & ROLE ATTACHMENT",
                             reactant_label="Fe^2+ (aq)", reactant_on="+2",
                             product_label="Fe^3+ (aq)", product_on="+3",
                             delta_text="Delta ON = +1 (Oxidation)",
                             electron_text="Loss of 1e- --> Fe^2+ is REDUCING AGENT"):
    return OxidationLaneDiagram.draw_lane(c, x, y, w, h, reactant_label, reactant_on, product_label, product_on, delta_text, electron_text, title=title)

def draw_coordinate_grid_2d(c, x, y, w, h, title="2D CARTESIAN PLANE & SLOPE TRIANGLE"):
    return CartesianPlotter2D.draw_slope_bridge(c, x, y, w, h, title=title)

def draw_combinatorial_slots(c, x, y, w, h, title="COMBINATORIAL SLOT MODEL"):
    return CombinatorialSlotDiagram.draw_slots(c, x, y, w, h, title=title)
