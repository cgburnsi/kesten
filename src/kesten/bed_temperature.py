"""Full-bed temperature profile helpers for visualization and early calibration."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List

from .physics1d_equation import EquationModelConfig, run_canonical_case_equation_profile


def run_full_bed_temperature_model(vapor_model: str = "reduced") -> List[Dict[str, float]]:
    """Generate a continuous full-bed temperature profile from equation integration."""

    rows = run_canonical_case_equation_profile(config=EquationModelConfig(vapor_model=vapor_model))
    return [{"Z": row["Z"], "TEMP": row["TEMP"]} for row in rows]


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
