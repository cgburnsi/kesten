"""Core package for Kesten 1968 model implementations."""

from .golden_data import load_region_rows
from .regression import REGION_TOLERANCES, ToleranceSpec, compare_rows
from .solver import SolverConfig, run_region_baseline, run_solver

__all__ = [
    "REGION_TOLERANCES",
    "SolverConfig",
    "ToleranceSpec",
    "compare_rows",
    "load_region_rows",
    "run_region_baseline",
    "run_solver",
]
