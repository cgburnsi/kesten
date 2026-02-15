"""Minimal deterministic liquid-region physics slice."""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, log
from typing import Dict, List


@dataclass(frozen=True)
class LiquidPhysicsConfig:
    """Configuration for the milestone-3 liquid-region reconstruction slice."""

    points: int = 24
    h_start: float = 0.0
    h_end: float = 212.628
    t_feed: float = 530.0
    t_end: float = 820.0
    dhdz_start: float = 37754.1
    dhdz_end: float = 38332300.0


def _linspace(start: float, stop: float, points: int) -> List[float]:
    if points < 2:
        raise ValueError("points must be >= 2")
    step = (stop - start) / (points - 1)
    return [start + i * step for i in range(points)]


def run_liquid_region_physics(config: LiquidPhysicsConfig | None = None) -> List[Dict[str, float]]:
    """Generate liquid-region rows from a compact deterministic model.

    Model assumptions for this initial milestone-3 slice:
    - Enthalpy increases uniformly over the liquid-region span.
    - Temperature is linear in enthalpy.
    - DHDZ follows an exponential trend with enthalpy anchored at region endpoints.
    - Axial distance is integrated as dz = dH / DHDZ using trapezoidal averaging.
    """

    cfg = config or LiquidPhysicsConfig()
    h_values = _linspace(cfg.h_start, cfg.h_end, cfg.points)

    temp_slope = (cfg.t_end - cfg.t_feed) / (cfg.h_end - cfg.h_start)
    log_dhdz_slope = (log(cfg.dhdz_end) - log(cfg.dhdz_start)) / (cfg.h_end - cfg.h_start)

    rows: List[Dict[str, float]] = []
    z = 0.0
    previous_h = None
    previous_dhdz = None

    for h in h_values:
        temp = cfg.t_feed + temp_slope * (h - cfg.h_start)
        dhdz = exp(log(cfg.dhdz_start) + log_dhdz_slope * (h - cfg.h_start))

        if previous_h is not None and previous_dhdz is not None:
            dh = h - previous_h
            z += dh / max(1e-12, 0.5 * (dhdz + previous_dhdz))

        rows.append(
            {
                "Z": z,
                "TEMP": temp,
                "H": h,
                "DHDZ": dhdz,
            }
        )

        previous_h = h
        previous_dhdz = dhdz

    return rows
