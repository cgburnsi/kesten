"""Full-bed temperature profile helpers for visualization and early calibration."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

import numpy as np


@dataclass(frozen=True)
class BedTemperatureModelConfig:
    """Control points for the calibrated full-bed temperature curve."""

    points: int = 300
    z_controls: tuple[float, ...] = (
        0.00016354069742728224,
        0.0012100240410729375,
        0.0034511810354192216,
        0.008187366864883496,
        0.011784967008468941,
        0.023802551471039764,
        0.06948885561658978,
        0.16249569008270331,
        0.2490116710198801,
    )
    temp_controls: tuple[float, ...] = (
        502.4516935022986,
        697.6525120323448,
        1498.03745259091,
        2001.1691683866975,
        2054.289725629484,
        2002.1388997784823,
        1947.867948857223,
        1860.5761828066188,
        1815.6890435998328,
    )


def run_full_bed_temperature_model(
    config: BedTemperatureModelConfig | None = None,
) -> List[Dict[str, float]]:
    """Generate a continuous full-bed temperature profile.

    This is a calibrated shape model used for visualization while 2D and richer
    1D physics reconstruction are in progress.
    """

    cfg = config or BedTemperatureModelConfig()
    if cfg.points < 2:
        raise ValueError("points must be >= 2")

    z_controls = np.asarray(cfg.z_controls, dtype=float)
    t_controls = np.asarray(cfg.temp_controls, dtype=float)

    z_axis = np.linspace(float(z_controls.min()), float(z_controls.max()), cfg.points)
    t_axis = np.interp(z_axis, z_controls, t_controls)

    return [{"Z": float(z), "TEMP": float(t)} for z, t in zip(z_axis, t_axis)]


def load_reference_bed_temperature_curve(path: str | Path) -> List[Dict[str, float]]:
    """Load reference bed-temperature points from a CSV with two numeric columns."""

    curve_path = Path(path)
    if not curve_path.exists():
        return []

    rows: List[Dict[str, float]] = []
    for line in curve_path.read_text(encoding="utf-8").splitlines():
        text = line.strip()
        if not text:
            continue
        parts = [item.strip() for item in text.split(",")]
        if len(parts) < 2:
            continue
        try:
            z_value = float(parts[0])
            temp_value = float(parts[1])
        except ValueError:
            continue
        rows.append({"Z": z_value, "TEMP": temp_value})

    rows.sort(key=lambda item: item["Z"])
    return rows
