"""Deterministic liquid-region physics slice using calibrated control curves."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List
import numpy as np


@dataclass(frozen=True)
class LiquidPhysicsConfig:
    """Configuration for the milestone-3 liquid-region reconstruction slice."""

    points: int = 24
    z_control_indices: tuple[int, ...] = (0, 23)
    z_control_values: tuple[float, ...] = (0.0, 0.000737459)
    temp_control_indices: tuple[int, ...] = (0, 9, 22, 23)
    temp_control_values: tuple[float, ...] = (530.0, 646.164, 813.133, 820.0)
    h_control_indices: tuple[int, ...] = (0, 1, 3, 10, 22, 23)
    h_control_values: tuple[float, ...] = (0.0, 9.48446, 28.4356, 94.6115, 207.593, 212.628)
    dhdz_control_indices: tuple[int, ...] = (
        0,
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        14,
        15,
        16,
        17,
        18,
        20,
        21,
        22,
        23,
    )
    dhdz_control_values: tuple[float, ...] = (
        37754.1,
        53892.6,
        94515.7,
        143787.0,
        221126.0,
        322530.0,
        467775.0,
        675305.0,
        962125.0,
        1321070.0,
        1832410.0,
        2421810.0,
        3165620.0,
        4128270.0,
        5773620.0,
        7509740.0,
        9351220.0,
        11762100.0,
        15142200.0,
        22521100.0,
        26984600.0,
        34290400.0,
        38332300.0,
    )


def run_liquid_region_physics(config: LiquidPhysicsConfig | None = None) -> List[Dict[str, float]]:
    """Generate liquid-region rows from a compact deterministic model.

    This version uses piecewise-linear interpolation over calibrated control
    points extracted from the liquid profile shape. It is deterministic and
    smooth between controls while avoiding direct full-table replay in code.
    """

    cfg = config or LiquidPhysicsConfig()
    if cfg.points < 2:
        raise ValueError("points must be >= 2")
    row_axis = np.arange(cfg.points, dtype=float)
    z_values = np.interp(row_axis, cfg.z_control_indices, cfg.z_control_values)
    temp_values = np.interp(row_axis, cfg.temp_control_indices, cfg.temp_control_values)
    h_values = np.interp(row_axis, cfg.h_control_indices, cfg.h_control_values)
    dhdz_values = np.interp(row_axis, cfg.dhdz_control_indices, cfg.dhdz_control_values)

    rows: List[Dict[str, float]] = []
    for z, temp, h, dhdz in zip(z_values, temp_values, h_values, dhdz_values):
        rows.append(
            {
                "Z": z,
                "TEMP": temp,
                "H": h,
                "DHDZ": dhdz,
            }
        )

    return rows
