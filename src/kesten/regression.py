"""Deterministic regression comparison helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List


@dataclass(frozen=True)
class ToleranceSpec:
    abs_tol: float
    rel_tol: float
    min_pass_fraction: float = 0.95


REGION_TOLERANCES = {
    "liquid": ToleranceSpec(abs_tol=1e-6, rel_tol=5e-4),
    "vapor": ToleranceSpec(abs_tol=1e-6, rel_tol=1e-3),
    "liquid_vapor": ToleranceSpec(abs_tol=1e-6, rel_tol=2e-3),
}


def _is_value_within_tolerance(reference: float, model: float, spec: ToleranceSpec) -> tuple[bool, float, float]:
    abs_error = abs(model - reference)
    rel_error = abs_error / max(1.0, abs(reference))
    allowed_error = max(spec.abs_tol, spec.rel_tol * max(1.0, abs(reference)))
    return abs_error <= allowed_error, abs_error, rel_error


def compare_rows(
    reference_rows: List[Dict[str, float]],
    model_rows: List[Dict[str, float]],
    fields: Iterable[str],
    spec: ToleranceSpec,
) -> Dict[str, object]:
    """Compare model rows against reference rows for selected fields."""

    if len(reference_rows) != len(model_rows):
        raise ValueError("Row-count mismatch between reference and model")

    failures = []
    total = 0
    passed = 0

    for row_index, (reference_row, model_row) in enumerate(zip(reference_rows, model_rows)):
        for field in fields:
            total += 1
            reference_value = reference_row[field]
            model_value = model_row[field]

            ok, abs_error, rel_error = _is_value_within_tolerance(reference_value, model_value, spec)
            if ok:
                passed += 1
                continue

            failures.append(
                {
                    "row": row_index,
                    "field": field,
                    "reference": reference_value,
                    "model": model_value,
                    "abs_error": abs_error,
                    "rel_error": rel_error,
                    "abs_tol": spec.abs_tol,
                    "rel_tol": spec.rel_tol,
                }
            )

    pass_fraction = 1.0 if total == 0 else passed / total
    return {
        "total": total,
        "passed": passed,
        "pass_fraction": pass_fraction,
        "minimum_required": spec.min_pass_fraction,
        "meets_threshold": pass_fraction >= spec.min_pass_fraction,
        "failures": failures,
    }
