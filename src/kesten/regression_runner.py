"""High-level regression execution and artifact emission."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict

from .golden_data import REGION_TO_FILE, load_region_rows
from .regression import REGION_TOLERANCES, compare_rows
from .solver import run_region_baseline, run_region_physics


REGION_FIELDS = {
    "liquid": ("Z", "TEMP", "H", "DHDZ"),
    "vapor": ("Z", "TEMP", "P", "H", "C1", "C2", "C3", "C4"),
    "liquid_vapor": ("Z", "TEMP", "H", "WFV"),
}


def _select_model_rows(region: str, source: str) -> tuple[list[dict[str, float]], str]:
    if source == "baseline":
        result = run_region_baseline(region)
        return result["rows"], result["mode"]

    if source == "physics":
        result = run_region_physics(region)
        return result["rows"], result["mode"]

    raise ValueError(f"Unsupported source '{source}'")


def run_region_regression(
    region: str,
    source: str,
    write_artifact: bool = True,
    artifact_dir: str | Path | None = None,
) -> Dict[str, object]:
    """Execute one region regression and optionally write failure artifacts."""

    normalized_region = region.strip().lower()
    if normalized_region not in REGION_FIELDS:
        raise ValueError(f"Unsupported region '{region}'")

    reference_rows = load_region_rows(normalized_region)
    model_rows, model_mode = _select_model_rows(normalized_region, source)

    result = compare_rows(
        reference_rows=reference_rows,
        model_rows=model_rows,
        fields=REGION_FIELDS[normalized_region],
        spec=REGION_TOLERANCES[normalized_region],
    )

    output: Dict[str, object] = {
        "test_case": f"{normalized_region}_{source}",
        "region": normalized_region,
        "source": source,
        "model_mode": model_mode,
        "golden_file": REGION_TO_FILE[normalized_region],
        "row_count": len(reference_rows),
        **result,
    }

    if write_artifact and result["failures"]:
        root = Path(artifact_dir) if artifact_dir is not None else Path("artifacts") / "regression"
        root.mkdir(parents=True, exist_ok=True)
        artifact_path = root / f"{normalized_region}_{source}_failures.json"
        artifact_path.write_text(json.dumps(output, indent=2), encoding="utf-8")
        output["artifact_path"] = str(artifact_path)

    return output
