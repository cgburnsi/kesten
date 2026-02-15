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
- Future tasks add file-based regression tests using `docs/verification/*_output.txt` reference data.
