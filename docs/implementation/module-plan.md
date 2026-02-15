# Module Plan

## Purpose
Plan module boundaries for milestones 3 and 4 before implementation expands.

## Proposed module layout
- `src/kesten/core/` shared data structures and utilities
- `src/kesten/solver1d/` 1D solver path
- `src/kesten/solver2d/` 2D solver path
- `src/kesten/verification/` comparison helpers against golden data

## Ownership and boundaries
- `core` must not depend on solver-specific modules.
- `solver2d` may reuse `core` but should avoid tight coupling to `solver1d` internals.
- verification helpers should not implement solver logic.

## Planned rollout
1. Establish minimal 1D state and stepping interfaces.
2. Add 1D regression harness and baseline cases.
3. Introduce 2D state/layout with minimal shared abstractions.
4. Add 2D regression harness.

## Open decisions
- TODO: confirm final package names for 1D and 2D solvers.
- TODO: decide whether to expose solver APIs in `src/kesten/__init__.py`.
