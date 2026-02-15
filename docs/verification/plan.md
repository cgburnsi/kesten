# Verification Plan

## Objective
Verify that the implemented numerical loop is deterministic, stable, and aligned with the Kesten 1968 reference behavior for each modeled region.

## Gates
1. Unit tests pass for solver convergence and non-convergence behavior.
2. Regression checks against Kesten reference outputs are added region-by-region.
3. Any tolerance-based checks document rationale and accepted numeric bounds.
4. CI runs tests on every push and pull request.

## Initial scope
- Baseline deterministic solver loop checks (`tests/test_solver.py`).
- File-based regression harness checks for liquid, vapor, and liquid-vapor reference outputs (`tests/test_regression_baseline.py`).
- Reconstructed liquid-region physics slice is available behind CLI `--mode physics --region liquid` and covered by `tests/test_liquid_physics.py`.
- Reconstructed vapor-region physics slice is available behind CLI `--mode physics --region vapor` and covered by `tests/test_vapor_physics.py`.
- Next stage calibrates the reconstructed liquid physics slice until it meets the liquid tolerance gate.
