# Implementation Specification

## Purpose
Define scope and acceptance criteria for milestones 3 and 4 (Python solver creation and verification).

## Scope boundaries
- This spec governs solver and verification code work.
- Source-document conversion rules remain in `docs/conversion/spec.md`.

## Milestone 3: Minimal, testable 1D solver
### Goal
Produce a deterministic 1D solver path that reproduces Kesten reference behavior within project tolerances.

### Required outputs
- Core solver module(s) under `src/`
- Thin CLI entry points under `app/` (if needed)
- Unit tests and regression tests under `tests/`
- Example runner under `examples/`

### Acceptance criteria
- Tests pass via `python -m unittest discover -s tests -v`.
- Numerical comparisons use policy in `docs/verification/tolerances.md`.
- At least one regression check compares solver output to each in-scope reference table.
- Deterministic behavior confirmed across repeated local runs.

## Milestone 4: Minimal, testable 2D solver
### Goal
Extend milestone-3 approach to a minimal 2D solver with preserved modularity and deterministic verification.

### Required outputs
- 2D solver path in `src/` with clear boundaries from 1D code.
- Regression tests against 2D-relevant reference outputs.
- Example script demonstrating a reproducible 2D run.

### Acceptance criteria
- All milestone-3 gates continue to pass.
- 2D tests pass and verify against reference behavior within tolerance.
- No architectural boundary violations against `ARCHITECTURE.md`.

## Implementation process
1. Define smallest vertical slice.
2. Add tests first or in lockstep with code.
3. Implement deterministic numerical path.
4. Compare to reference outputs and log differences.
5. Record key decisions in `docs/design/decisions.md`.

## Out of scope
- Performance optimization beyond correctness and readability.
- New dependencies beyond stdlib, NumPy, and Matplotlib.
