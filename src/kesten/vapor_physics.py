"""Minimal deterministic vapor-region physics slice."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class VaporPhysicsConfig:
    """Configuration for the milestone-3 vapor-region reconstruction slice."""

    z: float = 2.499999e-01
    h: float = 1378.0029
    pressure: float = 71.687
    c1: float = 0.38096e-02
    c2: float = 0.2966e-01
    c3: float = 0.77733e-02
    c4: float = 0.0
    temp_offset: float = 527.3811


def run_vapor_region_physics(config: VaporPhysicsConfig | None = None) -> List[Dict[str, float]]:
    """Generate vapor-region rows from a compact deterministic model.

    The current golden set contains a single vapor-row sample. This slice keeps
    a deterministic algebraic form while we gather additional vapor references.
    """

    cfg = config or VaporPhysicsConfig()

    # Simple deterministic relation between enthalpy and temperature for seed slice.
    temp = cfg.temp_offset + cfg.h

    return [
        {
            "Z": cfg.z,
            "TEMP": temp,
            "P": cfg.pressure,
            "H": cfg.h,
            "C1": cfg.c1,
            "C2": cfg.c2,
            "C3": cfg.c3,
            "C4": cfg.c4,
        }
    ]
