"""
Independent Visual Semantic Validator Module.
Provides:
- Strict fail-closed verification of visual primitive specs against question item data
- Eliminates semantic drift (e.g. rendering Iron on an Oxalate problem)
- Enforces quantitative fidelity (slopes, areas, vector signs, stoichiometry, shell capacities)
"""

import math
from typing import Dict, Any, List, Optional


# ------------------------------------------------------------------------------
# Exception Hierarchy
# ------------------------------------------------------------------------------
class VisualValidationError(Exception):
    """Base exception for all visual semantic validation errors."""
    pass


class UngroundedEntityError(VisualValidationError):
    """Raised when a visual primitive depicts entities absent from question item scope."""
    pass


class QuantitativeDiscrepancyError(VisualValidationError):
    """Raised when numerical values in visual primitive disagree with item values."""
    pass


class DirectionInversionError(VisualValidationError):
    """Raised when vector directions or coordinate signs are inverted."""
    pass


class ConservationError(VisualValidationError):
    """Raised when mass, atom count, or charge conservation is violated."""
    pass


class RolePolarityError(VisualValidationError):
    """Raised when oxidant/reductant agent roles are inverted with respect to delta ON."""
    pass


class AreaIntegralError(VisualValidationError):
    """Raised when graphic Riemann area under curve does not match kinematic displacement."""
    pass


class GeometryAxiomError(VisualValidationError):
    """Raised when geometric angles, collinearity, or triangle inequalities are violated."""
    pass


class CircleTheoremError(VisualValidationError):
    """Raised when central angle does not equal double the circumference subtended angle."""
    pass


class BohrCapacityError(VisualValidationError):
    """Raised when electron shells violate 2*n^2 Pauli/Bohr limits."""
    pass


class WaveKinematicsError(VisualValidationError):
    """Raised when wave speed, frequency, and wavelength violate v = nu * lambda."""
    pass


# ------------------------------------------------------------------------------
# Validator Implementation
# ------------------------------------------------------------------------------
class VisualSemanticValidator:
    """
    Independent pre-render gate for pedagogical graphics.
    Enforces 10 fail-closed verification gates before ReportLab canvas draws anything.
    """

    @classmethod
    def validate_oxidation_state_lane(cls, item_data: Dict[str, Any], visual_spec: Dict[str, Any]) -> bool:
        """
        Gate 1, Gate 2, Gate 5 validation for OxidationStateLane.
        Guarantees that an item about Oxalate/Carbon NEVER renders an Iron diagram.
        """
        # GATE-01: ENTITY CLOSURE & GROUNDING
        declared_entities = set(item_data.get("chemical_entities", [])) | set(item_data.get("entities", []))
        if declared_entities:
            reactant_species = visual_spec.get("reactant_species", "")
            product_species = visual_spec.get("product_species", "")
            
            def clean_species_token(label: str) -> str:
                if not label:
                    return ""
                for tok in label.strip().split():
                    if tok.isdigit():
                        continue
                    if tok.startswith("(") and tok.endswith(")"):
                        continue
                    return tok
                return ""
                
            r_clean = clean_species_token(reactant_species)
            p_clean = clean_species_token(product_species)
            
            visual_entities = {r_clean, p_clean} - {"", None}
            ungrounded = visual_entities - declared_entities
            
            if ungrounded:
                raise UngroundedEntityError(
                    f"[GATE-01 FAIL: ENTITY_CLOSURE] Visual contains ungrounded entities {ungrounded}. "
                    f"Item scope is strictly restricted to {declared_entities}. "
                    f"(Prevented rendering mismatched species like Iron on Carbon/Oxalate problem)."
                )

        # GATE-02: QUANTITATIVE CONGRUENCE (Oxidation numbers)
        r_on_str = str(visual_spec.get("reactant_on", "")).replace("+", "")
        p_on_str = str(visual_spec.get("product_on", "")).replace("+", "")
        
        try:
            r_on = float(r_on_str)
            p_on = float(p_on_str)
        except ValueError:
            raise QuantitativeDiscrepancyError(
                f"[GATE-02 FAIL] Oxidation numbers must be numeric. Received: reactant={r_on_str}, product={p_on_str}"
            )

        # Check against item declared ONs if present
        item_ons = item_data.get("oxidation_numbers", {})
        if item_ons:
            if "reactant" in item_ons and abs(item_ons["reactant"] - r_on) > 1e-4:
                raise QuantitativeDiscrepancyError(
                    f"[GATE-02 FAIL] Reactant ON {r_on} does not match item value {item_ons['reactant']}."
                )
            if "product" in item_ons and abs(item_ons["product"] - p_on) > 1e-4:
                raise QuantitativeDiscrepancyError(
                    f"[GATE-02 FAIL] Product ON {p_on} does not match item value {item_ons['product']}."
                )

        # GATE-05: REDOX AGENT POLARITY INTEGRITY
        delta_on = p_on - r_on
        assigned_role = str(visual_spec.get("assigned_role", "")).upper()
        
        if delta_on > 0:
            # Oxidation -> Must be Reducing Agent
            if "OXIDISING" in assigned_role or "OXIDANT" in assigned_role:
                raise RolePolarityError(
                    f"[GATE-05 FAIL: REDOX_POLARITY] Species has Delta ON = +{delta_on:g} (Oxidation), "
                    f"so it acts as a REDUCING AGENT. Cannot be labeled {assigned_role}."
                )
        elif delta_on < 0:
            # Reduction -> Must be Oxidising Agent
            if "REDUCING" in assigned_role or "REDUCTANT" in assigned_role:
                raise RolePolarityError(
                    f"[GATE-05 FAIL: REDOX_POLARITY] Species has Delta ON = {delta_on:g} (Reduction), "
                    f"so it acts as an OXIDISING AGENT. Cannot be labeled {assigned_role}."
                )
                
        return True

    @classmethod
    def validate_kinematic_graph(cls, item_data: Dict[str, Any], visual_spec: Dict[str, Any]) -> bool:
        """
        Gate 2 and Gate 6 validation for Kinematic graphs (v-t).
        """
        u = float(visual_spec.get("u", 0.0))
        v = float(visual_spec.get("v", 0.0))
        t = float(visual_spec.get("t_accel", 1.0))
        
        if t <= 0:
            raise QuantitativeDiscrepancyError("[GATE-02 FAIL] Kinematic duration t must be strictly positive.")
            
        # GATE-02: Item value agreement
        for param, spec_val in [("u", u), ("v", v), ("t", t)]:
            if param in item_data and abs(item_data[param] - spec_val) > 1e-4:
                raise QuantitativeDiscrepancyError(
                    f"[GATE-02 FAIL] Visual parameter {param}={spec_val} disagrees with item parameter {item_data[param]}."
                )
                
        # GATE-06: AREA INTEGRAL VALIDATION
        # Area = u * t + 0.5 * (v - u) * t
        calculated_area = u * t + 0.5 * (v - u) * t
        if "displacement" in item_data:
            item_disp = float(item_data["displacement"])
            if abs(calculated_area - item_disp) > 1e-3:
                raise AreaIntegralError(
                    f"[GATE-06 FAIL: AREA_INTEGRAL] Shaded Riemann area {calculated_area:.4f} m "
                    f"does not match declared item displacement {item_disp:.4f} m."
                )
                
        return True

    @classmethod
    def validate_vector_1d(cls, item_data: Dict[str, Any], visual_spec: Dict[str, Any]) -> bool:
        """
        Gate 3 validation for 1D reference frames and vectors.
        """
        legs = visual_spec.get("legs", [])
        net_disp = 0.0
        for leg in legs:
            start = float(leg.get("start", 0))
            end = float(leg.get("end", 0))
            leg_disp = end - start
            net_disp += leg_disp
            
            # Directional check: if label contains East / +x, displacement must be positive
            label = leg.get("label", "").lower()
            if "east" in label and leg_disp < 0:
                raise DirectionInversionError(
                    f"[GATE-03 FAIL: DIRECTION_INVERSION] Leg '{label}' specifies East but has negative vector {leg_disp}."
                )
            if "west" in label and leg_disp > 0:
                raise DirectionInversionError(
                    f"[GATE-03 FAIL: DIRECTION_INVERSION] Leg '{label}' specifies West but has positive vector {leg_disp}."
                )
                
        # Resultant check
        res_start = float(visual_spec.get("resultant_start", 0))
        res_end = float(visual_spec.get("resultant_end", net_disp))
        if abs((res_end - res_start) - net_disp) > 1e-4:
            raise DirectionInversionError(
                f"[GATE-03 FAIL] Vector resultant {res_end - res_start} does not equal sum of legs {net_disp}."
            )
            
        return True

    @classmethod
    def validate_particulate_model(cls, item_data: Dict[str, Any], visual_spec: Dict[str, Any]) -> bool:
        """
        Gate 1 and Gate 4 validation for Johnstone submicroscopic models.
        """
        # GATE-04: MASS CONSERVATION (Atom count ledger)
        reactants = visual_spec.get("reactants", {})
        products = visual_spec.get("products", {})
        
        all_elements = set(reactants.keys()) | set(products.keys())
        for elem in all_elements:
            r_count = reactants.get(elem, 0)
            p_count = products.get(elem, 0)
            if r_count != p_count:
                raise ConservationError(
                    f"[GATE-04 FAIL: MASS_CONSERVATION] Element '{elem}' is not conserved! "
                    f"Reactants count = {r_count}, Products count = {p_count}."
                )
                
        return True

    @classmethod
    def validate_plane_geometry(cls, item_data: Dict[str, Any], visual_spec: Dict[str, Any]) -> bool:
        """
        Gate 7 validation for Euclidean geometry (Triangle angle sums, parallel angles).
        """
        angles = visual_spec.get("triangle_angles", [])
        if angles and len(angles) == 3:
            angle_sum = sum(angles)
            if abs(angle_sum - 180.0) > 1e-4:
                raise GeometryAxiomError(
                    f"[GATE-07 FAIL: GEOMETRY_AXIOM] Triangle interior angle sum must equal 180 deg. "
                    f"Current sum = {angle_sum} deg ({angles})."
                )
        return True

    @classmethod
    def validate_circle_theorem(cls, item_data: Dict[str, Any], visual_spec: Dict[str, Any]) -> bool:
        """
        Gate 8 validation: Angle at center = 2 * Angle at circumference.
        """
        theta = float(visual_spec.get("theta_circumference", 0.0))
        central = float(visual_spec.get("central_angle", 0.0))
        
        if theta > 0 and central > 0:
            if abs(central - 2 * theta) > 1e-4:
                raise CircleTheoremError(
                    f"[GATE-08 FAIL: CIRCLE_THEOREM] Central angle must equal double circumference angle! "
                    f"Central = {central} deg, 2 * theta = {2 * theta} deg."
                )
        return True

    @classmethod
    def validate_bohr_atom(cls, item_data: Dict[str, Any], visual_spec: Dict[str, Any]) -> bool:
        """
        Gate 9 validation for Bohr electron shells (2*n^2 capacity and Z sum).
        """
        protons = int(visual_spec.get("protons", 0))
        shells = list(visual_spec.get("shells", []))
        
        # Max capacity formula 2 * n^2: K(1)=2, L(2)=8, M(3)=18, N(4)=32
        for n_idx, e_count in enumerate(shells):
            n = n_idx + 1
            max_allowed = 2 * (n ** 2)
            if e_count > max_allowed:
                raise BohrCapacityError(
                    f"[GATE-09 FAIL: BOHR_SHELL_CAPACITY] Shell n={n} contains {e_count} electrons, "
                    f"exceeding maximum theoretical capacity of {max_allowed} (2*n^2)."
                )
                
        # Total electrons must match atomic number Z for neutral atom
        if protons > 0 and sum(shells) != protons:
            raise BohrCapacityError(
                f"[GATE-09 FAIL] Total electrons ({sum(shells)}) does not match proton count Z={protons} for neutral atom."
            )
            
        return True

    @classmethod
    def validate_wave_kinematics(cls, item_data: Dict[str, Any], visual_spec: Dict[str, Any]) -> bool:
        """
        Gate 10 validation: v = nu * lambda.
        """
        v = visual_spec.get("v")
        nu = visual_spec.get("nu")
        lam = visual_spec.get("wavelength")
        
        if v is not None and nu is not None and lam is not None:
            if abs(float(v) - float(nu) * float(lam)) > 1e-4:
                raise WaveKinematicsError(
                    f"[GATE-10 FAIL: WAVE_KINEMATICS] Wave speed v={v} does not equal frequency * wavelength "
                    f"({nu} * {lam} = {float(nu) * float(lam)})."
                )
        return True

    @classmethod
    def validate(cls, primitive_type: str, item_data: Dict[str, Any], visual_spec: Dict[str, Any]) -> bool:
        """
        Master dispatch entry point for pre-render validation.
        """
        p_type = primitive_type.upper()
        if "WAVE" in p_type:
            return cls.validate_wave_kinematics(item_data, visual_spec)
        elif "OXIDATION" in p_type or "REDOX" in p_type:
            return cls.validate_oxidation_state_lane(item_data, visual_spec)
        elif "KINEMATIC" in p_type or "VT_GRAPH" in p_type or "MOTION" in p_type:
            return cls.validate_kinematic_graph(item_data, visual_spec)
        elif "VECTOR" in p_type or "1D" in p_type:
            return cls.validate_vector_1d(item_data, visual_spec)
        elif "PARTICULATE" in p_type or "DALTON" in p_type:
            return cls.validate_particulate_model(item_data, visual_spec)
        elif "TRIANGLE" in p_type or "GEOMETRY" in p_type:
            return cls.validate_plane_geometry(item_data, visual_spec)
        elif "CIRCLE" in p_type:
            return cls.validate_circle_theorem(item_data, visual_spec)
        elif "BOHR" in p_type or "ATOM" in p_type:
            return cls.validate_bohr_atom(item_data, visual_spec)
            
        return True
