"""
Unit tests for modular visual primitives rendering functions.
Verifies ReportLab canvas integration, coordinate transformations, and data models.
"""

import sys
import unittest
from pathlib import Path
from reportlab.pdfgen import canvas

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from primitives.graphs import CartesianPlotter2D, KinematicGraphRenderer, StatisticalPlotter, ThermalCurvePlotter
from primitives.diagrams import (
    PlaneGeometryRenderer, Vector1DDiagram, FreeBodyDiagramRenderer,
    WaveformRenderer, BohrAtomRenderer, ParticleLatticeDiagram,
    OxidationLaneDiagram, CombinatorialSlotDiagram
)
from primitives.equations import (
    FormulaAnatomyEngine, ValencyCrissCrossEngine,
    ChemicalReactionEngine, GeometryProofBlock, MathEquationBlock
)


class TestVisualPrimitives(unittest.TestCase):
    """Verifies that all primitives render cleanly on a headless canvas without throwing errors."""

    def setUp(self):
        # Headless mock/discard canvas
        self.scratch_pdf = Path(__file__).resolve().parent / "test_scratch.pdf"
        self.c = canvas.Canvas(str(self.scratch_pdf), pagesize=(600, 800))

    def tearDown(self):
        if self.scratch_pdf.exists():
            try:
                self.scratch_pdf.unlink()
            except Exception:
                pass

    def test_cartesian_plotter_coordinate_scaling(self):
        plotter = CartesianPlotter2D(self.c, 50, 50, 200, 200, x_domain=(0, 10), y_domain=(0, 20))
        cx, cy = plotter.to_canvas(5, 10)
        # Midpoint of plot area
        expected_cx = plotter.plot_x + plotter.plot_w * 0.5
        expected_cy = plotter.plot_y + plotter.plot_h * 0.5
        self.assertAlmostEqual(cx, expected_cx, places=2)
        self.assertAlmostEqual(cy, expected_cy, places=2)

    def test_render_all_primitives_headless(self):
        """Exercises every primitive to ensure zero syntax or ReportLab API errors."""
        c = self.c
        
        # Graphs
        plotter = CartesianPlotter2D(c, 50, 600, 200, 150)
        plotter.draw_axes()
        plotter.plot_point(2, 3, "P(2,3)")
        plotter.plot_slope_triangle(1, 1, 4, 5)
        
        KinematicGraphRenderer.draw_vt_graph(c, 50, 420, 240, 150, u=5.0, v=25.0, t_accel=4.0)
        StatisticalPlotter.draw_histogram(c, 310, 420, 240, 150, [(0, 10, 5), (10, 20, 12), (20, 30, 8)])
        ThermalCurvePlotter.draw_heating_curve(c, 50, 240, 240, 150)
        
        # Diagrams
        PlaneGeometryRenderer.draw_parallel_transversal(c, 310, 240, 240, 150)
        PlaneGeometryRenderer.draw_triangle_with_altitude(c, 50, 60, 240, 150)
        PlaneGeometryRenderer.draw_circle_subtended_angles(c, 310, 60, 240, 150)
        
        c.showPage()
        
        Vector1DDiagram.draw(c, 50, 600, 240, 120)
        FreeBodyDiagramRenderer.draw_fbd(c, 310, 600, 240, 120)
        WaveformRenderer.draw_transverse_wave(c, 50, 440, 240, 120)
        BohrAtomRenderer.draw_bohr_atom(c, 310, 440, 240, 120)
        ParticleLatticeDiagram.draw_reaction_chamber(c, 50, 280, 240, 120)
        OxidationLaneDiagram.draw_lane(c, 310, 280, 240, 120,
                                      reactant_label="C2O4^2-", reactant_on="+3",
                                      product_label="2 CO2", product_on="+4",
                                      delta_text="Delta ON = +1 (Oxidation)",
                                      electron_text="Reducing Agent")
        CombinatorialSlotDiagram.draw_slots(c, 50, 120, 240, 120)
        
        # Equations
        FormulaAnatomyEngine.draw_formula_anatomy(c, 310, 120, 240, 120)
        
        c.showPage()
        
        ValencyCrissCrossEngine.draw_criss_cross(c, 50, 600, 240, 120)
        ChemicalReactionEngine.draw_reaction(c, 310, 600, 240, 120)
        GeometryProofBlock.draw_proof(c, 50, 400, 500, 160, [("In Triangle ABC and PQR, AB = PQ", "Given"), ("Angle B = Angle Q", "Given")])
        MathEquationBlock.draw_algebra_block(c, 50, 200, 500, 160, ["2x + 4 = 12", "2x = 8", "x = 4"], invariant_text="LHS = 2(4) + 4 = 12 = RHS")
        
        c.save()
        self.assertTrue(self.scratch_pdf.exists())


if __name__ == "__main__":
    unittest.main()
