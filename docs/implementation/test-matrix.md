# Test Matrix

## Purpose
Track required tests by milestone, region, and scope.

## Matrix
| Milestone | Component | Test Type | Reference Data | Status | Notes |
|---|---|---|---|---|---|
| 3 | solver1d convergence loop | unit | n/a | implemented | Covered by `tests/test_solver.py`. |
| 3 | solver1d liquid region | regression | `docs/verification/liquid_region_kesten_output.txt` | implemented | Tolerance-gate comparison is wired for both baseline and physics sources; current physics slice fails gate and emits diagnostics for iteration. |
| 3 | solver1d vapor region | regression | `docs/verification/Vapor Region Correct Output.txt` | implemented | Baseline harness compares deterministic golden-replay output against vapor reference fields. |
| 3 | solver1d liquid-vapor region | regression | `docs/verification/LV_region_Kesten_Output.txt` | implemented | Baseline harness compares deterministic golden-replay output against liquid-vapor reference fields. |
| 4 | solver2d stepping | unit | n/a | planned | |
| 4 | solver2d reference case(s) | regression | TODO | planned | |

## Determinism checks
- Repeat key regression cases to ensure stable outputs.
- Record any platform-sensitive behavior and tolerance rationale.

## CI expectations
- Unit tests required on every push/PR.
- Regression suite required on every push/PR once milestone-3 harness is active.
