# Test Matrix

## Purpose
Track required tests by milestone, region, and scope.

## Matrix
| Milestone | Component | Test Type | Reference Data | Status | Notes |
|---|---|---|---|---|---|
| 3 | solver1d convergence loop | unit | n/a | planned | |
| 3 | solver1d liquid region | regression | `docs/verification/liquid_region_kesten_output.txt` | planned | |
| 3 | solver1d vapor region | regression | `docs/verification/Vapor Region Correct Output.txt` | planned | |
| 3 | solver1d liquid-vapor region | regression | `docs/verification/LV_region_Kesten_Output.txt` | planned | |
| 4 | solver2d stepping | unit | n/a | planned | |
| 4 | solver2d reference case(s) | regression | TODO | planned | |

## Determinism checks
- Repeat key regression cases to ensure stable outputs.
- Record any platform-sensitive behavior and tolerance rationale.

## CI expectations
- Unit tests required on every push/PR.
- Regression suite required on every push/PR once milestone-3 harness is active.
