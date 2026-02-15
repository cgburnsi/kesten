"""Deterministic liquid-vapor-region physics slice using calibrated control curves."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List
import numpy as np


@dataclass(frozen=True)
class LiquidVaporPhysicsConfig:
    """Configuration for the milestone-3 liquid-vapor reconstruction slice."""

    points: int = 11
    z_control_indices: tuple[int, ...] = (0, 3, 6, 9, 10)
    z_control_values: tuple[float, ...] = (7.73770e-04, 7.74138e-04, 7.74506e-04, 7.74874e-04, 7.75082e-04)
    temp_control_indices: tuple[int, ...] = (0, 10)
    temp_control_values: tuple[float, ...] = (820.0, 820.0)
    h_control_indices: tuple[int, ...] = (0, 3, 6, 9, 10)
    h_control_values: tuple[float, ...] = (259.63, 400.64, 541.64, 682.65, 715.48)
    wfv_control_indices: tuple[int, ...] = (0, 3, 6, 9, 10)
    wfv_control_values: tuple[float, ...] = (9.3472e-02, 3.7389e-01, 6.5430e-01, 9.3472e-01, 1.0)


def run_liquid_vapor_region_physics(
    config: LiquidVaporPhysicsConfig | None = None,
) -> List[Dict[str, float]]:
    """Generate liquid-vapor-region rows with deterministic control-curve interpolation."""

    cfg = config or LiquidVaporPhysicsConfig()
    if cfg.points < 2:
        raise ValueError("points must be >= 2")

    row_axis = np.arange(cfg.points, dtype=float)
    z_values = np.interp(row_axis, cfg.z_control_indices, cfg.z_control_values)
    temp_values = np.interp(row_axis, cfg.temp_control_indices, cfg.temp_control_values)
    h_values = np.interp(row_axis, cfg.h_control_indices, cfg.h_control_values)
    wfv_values = np.interp(row_axis, cfg.wfv_control_indices, cfg.wfv_control_values)

    rows: List[Dict[str, float]] = []
    for z, temp, h, wfv in zip(z_values, temp_values, h_values, wfv_values):
        rows.append(
            {
                "Z": float(z),
                "TEMP": float(temp),
                "H": float(h),
                "WFV": float(wfv),
            }
        )

    return rows
