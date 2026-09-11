"""
Falsifier and Regression Test Suite for VisualSemanticValidator.
Verifies all 10 fail-closed gates with both negative (defect caught) and positive (valid pass) cases.
"""

import sys
import unittest
from pathlib import Path

# Add MasterTemplates root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from primitives.validator import (
    VisualSemanticValidator,
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


class TestVisualSemanticValidator(unittest.TestCase):
    """Falsifier suite verifying that all semantic, numerical, and topological mismatches are rejected."""

    # --------------------------------------------------------------------------
    # GATE 01: Entity Closure & Grounding (Permanent fix for Iron on Oxalate defect)
    # --------------------------------------------------------------------------
    def test_gate01_rejects_ungrounded_entity_iron_on_oxalate(self):
        """Item declares Oxalate/Carbon redox, visual tries to render Iron -> REJECTED."""
        item_data = {
            "item_id": "CHEM_G09_CORE2_001",
            "chemical_entities": ["C2O4^2-", "CO2", "MnO4^-", "Mn^2+"],
            "oxidation_numbers": {"reactant": 3.0, "product": 4.0}
        }
        # Faulty visual spec trying to render Iron
        mismatched_visual = {
            "reactant_species": "Fe^2+ (aq)",
            "reactant_on": "+2",
            "product_species": "Fe^3+ (aq)",
            "product_on": "+3",
            "assigned_role": "REDUCING_AGENT"
        }
        with self.assertRaises(UngroundedEntityError) as ctx:
            VisualSemanticValidator.validate("OXIDATION_LANE", item_data, mismatched_visual)
        self.assertIn("Fe^2+", str(ctx.exception))
        self.assertIn("ungrounded entities", str(ctx.exception).lower())

    def test_gate01_accepts_grounded_oxalate_visual(self):
        """Item declares Oxalate/Carbon redox, visual renders Oxalate/CO2 -> ACCEPTED."""
        item_data = {
            "item_id": "CHEM_G09_CORE2_001",
            "chemical_entities": ["C2O4^2-", "CO2", "MnO4^-", "Mn^2+"],
            "oxidation_numbers": {"reactant": 3.0, "product": 4.0}
        }
        valid_visual = {
            "reactant_species": "C2O4^2- (aq)",
            "reactant_on": "+3",
            "product_species": "CO2 (g)",
            "product_on": "+4",
            "assigned_role": "REDUCING_AGENT"
        }
        self.assertTrue(VisualSemanticValidator.validate("OXIDATION_LANE", item_data, valid_visual))

    # --------------------------------------------------------------------------
    # GATE 02: Quantitative Congruence
    # --------------------------------------------------------------------------
    def test_gate02_rejects_mismatched_kinematic_velocity(self):
        """Item has v=20 m/s, visual specifies v=25 m/s -> REJECTED."""
        item_data = {"u": 0.0, "v": 20.0, "t_accel": 5.0}
        mismatched_visual = {"u": 0.0, "v": 25.0, "t_accel": 5.0}
        with self.assertRaises(QuantitativeDiscrepancyError) as ctx:
            VisualSemanticValidator.validate("KINEMATIC_GRAPH", item_data, mismatched_visual)
        self.assertIn("disagrees with item parameter", str(ctx.exception))

    # --------------------------------------------------------------------------
    # GATE 03: Directional & Vector Congruence
    # --------------------------------------------------------------------------
    def test_gate03_rejects_inverted_direction(self):
        """Leg label says East (+x) but vector has negative displacement -> REJECTED."""
        item_data = {}
        faulty_visual = {
            "legs": [{"start": 5, "end": 2, "label": "Leg 1: East (+5 m)"}]
        }
        with self.assertRaises(DirectionInversionError):
            VisualSemanticValidator.validate("VECTOR_1D", item_data, faulty_visual)

    # --------------------------------------------------------------------------
    # GATE 04: Mass & Stoichiometric Conservation
    # --------------------------------------------------------------------------
    def test_gate04_rejects_unbalanced_particulate_atoms(self):
        """Reactants have 4 H, Products have 2 H -> REJECTED."""
        item_data = {}
        unbalanced_visual = {
            "reactants": {"H": 4, "O": 2},
            "products": {"H": 2, "O": 1} # Missing 1 H2O!
        }
        with self.assertRaises(ConservationError) as ctx:
            VisualSemanticValidator.validate("PARTICULATE_MODEL", item_data, unbalanced_visual)
        self.assertIn("is not conserved", str(ctx.exception))

    # --------------------------------------------------------------------------
    # GATE 05: Redox Agent Polarity Integrity
    # --------------------------------------------------------------------------
    def test_gate05_rejects_inverted_redox_role(self):
        """Delta ON = +1 (Oxidation) but labeled OXIDISING_AGENT -> REJECTED."""
        item_data = {}
        inverted_visual = {
            "reactant_species": "C2O4^2-",
            "reactant_on": "+3",
            "product_species": "CO2",
            "product_on": "+4",
            "assigned_role": "OXIDISING_AGENT" # Inversion!
        }
        with self.assertRaises(RolePolarityError) as ctx:
            VisualSemanticValidator.validate("OXIDATION_LANE", item_data, inverted_visual)
        self.assertIn("REDUCING AGENT", str(ctx.exception))

    # --------------------------------------------------------------------------
    # GATE 06: Calculus & Area Integration
    # --------------------------------------------------------------------------
    def test_gate06_rejects_area_integral_mismatch(self):
        """Area under v-t does not match declared item displacement -> REJECTED."""
        # u=0, v=20, t=5 -> Area = 0.5 * 20 * 5 = 50 m. Item says displacement = 70 m.
        item_data = {"u": 0.0, "v": 20.0, "t_accel": 5.0, "displacement": 70.0}
        visual_spec = {"u": 0.0, "v": 20.0, "t_accel": 5.0}
        with self.assertRaises(AreaIntegralError) as ctx:
            VisualSemanticValidator.validate("KINEMATIC_GRAPH", item_data, visual_spec)
        self.assertIn("does not match declared item displacement", str(ctx.exception))

    # --------------------------------------------------------------------------
    # GATE 07: Euclidean Geometry Consistency
    # --------------------------------------------------------------------------
    def test_gate07_rejects_triangle_angle_sum_violation(self):
        """Triangle angles sum to 190 deg -> REJECTED."""
        visual_spec = {"triangle_angles": [60.0, 70.0, 60.0]} # sum = 190
        with self.assertRaises(GeometryAxiomError):
            VisualSemanticValidator.validate("TRIANGLE_GEOMETRY", {}, visual_spec)

    # --------------------------------------------------------------------------
    # GATE 08: Circle Subtended Angle Theorem
    # --------------------------------------------------------------------------
    def test_gate08_rejects_circle_subtended_angle_violation(self):
        """Circumference angle = 35 deg, but central angle = 60 deg (should be 70 deg) -> REJECTED."""
        visual_spec = {"theta_circumference": 35.0, "central_angle": 60.0}
        with self.assertRaises(CircleTheoremError):
            VisualSemanticValidator.validate("CIRCLE_THEOREM", {}, visual_spec)

    # --------------------------------------------------------------------------
    # GATE 09: Bohr Shell Capacity Limit (2n^2)
    # --------------------------------------------------------------------------
    def test_gate09_rejects_bohr_shell_overflow(self):
        """K shell (n=1) has 4 electrons (max 2 allowed) -> REJECTED."""
        visual_spec = {
            "protons": 11,
            "shells": [4, 6, 1] # K shell overflow!
        }
        with self.assertRaises(BohrCapacityError) as ctx:
            VisualSemanticValidator.validate("BOHR_ATOM", {}, visual_spec)
        self.assertIn("exceeding maximum theoretical capacity of 2", str(ctx.exception))

    # --------------------------------------------------------------------------
    # GATE 10: Wave Kinematic Equation (v = nu * lambda)
    # --------------------------------------------------------------------------
    def test_gate10_rejects_wave_speed_inconsistency(self):
        """nu=100 Hz, lambda=2 m -> v must be 200 m/s. Spec says v=300 -> REJECTED."""
        visual_spec = {"v": 300.0, "nu": 100.0, "wavelength": 2.0}
        with self.assertRaises(WaveKinematicsError):
            VisualSemanticValidator.validate("WAVE_KINEMATICS", {}, visual_spec)

    def test_gate10_accepts_valid_wave_speed(self):
        visual_spec = {"v": 200.0, "nu": 100.0, "wavelength": 2.0}
        self.assertTrue(VisualSemanticValidator.validate("WAVE_KINEMATICS", {}, visual_spec))


if __name__ == "__main__":
    unittest.main()
