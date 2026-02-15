"""Core package for Kesten 1968 model implementations."""

from .bed_temperature import load_reference_bed_temperature_curve, run_full_bed_temperature_model
from .golden_data import load_region_rows
from .liquid_physics import LiquidPhysicsConfig, run_liquid_region_physics
from .liquid_vapor_physics import LiquidVaporPhysicsConfig, run_liquid_vapor_region_physics
from .physics1d_equation import CanonicalCaseConstants, EquationModelConfig, run_canonical_case_equation_profile
from .regression import REGION_TOLERANCES, ToleranceSpec, compare_rows
from .regression_runner import REGION_FIELDS, run_region_regression
from .solver import SolverConfig, run_region_baseline, run_region_physics, run_solver
from .vapor_physics import VaporPhysicsConfig, run_vapor_region_physics

__all__ = [
    "CanonicalCaseConstants",
    "EquationModelConfig",
    "REGION_TOLERANCES",
    "REGION_FIELDS",
    "LiquidPhysicsConfig",
    "LiquidVaporPhysicsConfig",
    "SolverConfig",
    "ToleranceSpec",
    "compare_rows",
    "load_reference_bed_temperature_curve",
    "load_region_rows",
    "run_region_baseline",
    "run_canonical_case_equation_profile",
    "run_full_bed_temperature_model",
    "run_liquid_region_physics",
    "run_liquid_vapor_region_physics",
    "run_region_physics",
    "run_region_regression",
    "run_solver",
    "VaporPhysicsConfig",
    "run_vapor_region_physics",
]
