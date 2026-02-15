# Golden Data Index

## Purpose
Catalog reference outputs used for solver verification.

## Golden datasets
| File | Region/Model | Units | Source provenance | Planned tests | Notes |
|---|---|---|---|---|---|
| `docs/verification/liquid_region_kesten_output.txt` | liquid | TODO | Kesten 1968 report | TODO | |
| `docs/verification/Vapor Region Correct Output.txt` | vapor | TODO | Kesten 1968 report | TODO | |
| `docs/verification/LV_region_Kesten_Output.txt` | liquid-vapor | TODO | Kesten 1968 report | TODO | |

## Data handling rules
- Never edit raw golden files in-place.
- If normalization/preprocessing is needed, write derived files under a clearly named path and document transform logic.
- Tests must declare which golden file(s) they consume.
