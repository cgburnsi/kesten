"""Minimal deterministic solver loop for initial project bootstrapping."""

from dataclasses import dataclass
from typing import Dict, List

from .golden_data import load_region_rows


@dataclass(frozen=True)
class SolverConfig:
    """Configuration for the fixed-point style steady-state iteration."""

    max_iterations: int = 100
    tolerance: float = 1e-8
    relaxation: float = 0.5


def run_solver(initial_value: float, target_value: float, config: SolverConfig | None = None) -> Dict[str, object]:
    """Run a deterministic steady-state iteration until tolerance or max iterations."""

    cfg = config or SolverConfig()
    value = float(initial_value)
    target = float(target_value)
    residual_history: List[float] = []

    for iteration in range(1, cfg.max_iterations + 1):
        residual = target - value
        residual_history.append(abs(residual))
        if abs(residual) <= cfg.tolerance:
            return {
                "converged": True,
                "iterations": iteration - 1,
                "value": value,
                "residual_history": tuple(residual_history),
            }

        value = value + cfg.relaxation * residual

    return {
        "converged": False,
        "iterations": cfg.max_iterations,
        "value": value,
        "residual_history": tuple(residual_history),
    }


def run_region_baseline(region: str) -> Dict[str, object]:
    """Return deterministic baseline rows for one region.

    This baseline intentionally replays parsed golden rows to establish the
    regression harness before full physics reconstruction.
    """

    rows = load_region_rows(region)
    return {
        "region": region,
        "mode": "golden_replay_baseline",
        "rows": rows,
    }
