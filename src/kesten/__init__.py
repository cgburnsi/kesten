"""Core package for Kesten 1968 model implementations."""

from .golden_data import load_region_rows
from .liquid_physics import LiquidPhysicsConfig, run_liquid_region_physics
from .regression import REGION_TOLERANCES, ToleranceSpec, compare_rows
from .regression_runner import REGION_FIELDS, run_region_regression
from .solver import SolverConfig, run_region_baseline, run_region_physics, run_solver

__all__ = [
    "REGION_TOLERANCES",
    "REGION_FIELDS",
    "LiquidPhysicsConfig",
    "SolverConfig",
    "ToleranceSpec",
    "compare_rows",
    "load_region_rows",
    "run_region_baseline",
    "run_liquid_region_physics",
    "run_region_physics",
    "run_region_regression",
    "run_solver",
]
