# Verification Tolerances

## Purpose
Define tolerance policy for comparing reconstructed outputs with Kesten 1968 reference values.

## Comparison rule
For each value, pass when:

`abs(err) <= max(abs_tol, rel_tol * max(1.0, abs(reference)))`

Where:
- `err = model_value - reference_value`
- `abs_tol` is absolute tolerance
- `rel_tol` is relative tolerance

## Baseline tolerances
- Liquid region: `abs_tol=1e-6`, `rel_tol=5e-4`
- Vapor region: `abs_tol=1e-6`, `rel_tol=1e-3`
- Liquid-vapor region: `abs_tol=1e-6`, `rel_tol=2e-3`

## Table-level acceptance
- At least 95% of values must pass per reference table.
- Failing rows must be logged with index, reference value, model value, and absolute/relative error.

## Tightening policy
After stable baseline parity is reached:
1. Reduce relative tolerances by 2x for a milestone.
2. Keep changes only if tests remain stable across repeated runs and environments.
3. Record tolerance changes in `docs/design/decisions.md`.
