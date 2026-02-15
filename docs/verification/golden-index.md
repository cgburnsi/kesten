# Golden Data Index

## Purpose
Catalog reference outputs used for solver verification.

## Golden datasets
| File | Region/Model | Units | Source provenance | Planned tests | Notes |
|---|---|---|---|---|---|
| `docs/verification/liquid_region_kesten_output.txt` | liquid | `Z [ft]`, `TEMP [degR]`, `H [BTU/lb]`, `DHDZ` | Kesten 1968 report | `tests/test_regression_baseline.py::test_liquid_region_baseline_meets_threshold` | Parsed with legacy FORTRAN-like exponent normalization. |
| `docs/verification/Vapor Region Correct Output.txt` | vapor | `Z [ft]`, `TEMP [degR]`, `P`, `H [BTU/lb]`, `C1..C4` | Kesten 1968 report | `tests/test_regression_baseline.py::test_vapor_region_baseline_meets_threshold` | Single-line baseline sample in current golden file. |
| `docs/verification/LV_region_Kesten_Output.txt` | liquid-vapor | `Z [ft]`, `TEMP [degR]`, `H [BTU/lb]`, `WFV` | Kesten 1968 report | `tests/test_regression_baseline.py::test_liquid_vapor_region_baseline_meets_threshold` | Parsed as tagged key/value lines. |

## Data handling rules
- Never edit raw golden files in-place.
- If normalization/preprocessing is needed, write derived files under a clearly named path and document transform logic.
- Tests must declare which golden file(s) they consume.
