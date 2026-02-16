# Fortran Vapor Port Blockers

## Current status
- `fortran_inspired` vapor mode now includes:
  - table-driven interpolation port (`UNBAR`-style)
  - helper routine ports for `CONC`, `PARAM`, and `LQVP`
  - iterative `SGRAD`-style gradient solve
  - adaptive vapor-step logic
- It is **not** yet a faithful Kesten 1968 vapor-region reproduction.

## Remaining blockers
- The strict `fortran_inspired` acceptance gate (peak location/shape/end-state) still fails.
- Current port relies on an early Python translation as source, not authoritative original `UNBAR.f`/`TABLES.f`.
- Additional `VAPOR.f` controls (step-size branch logic and coupled terms) are still simplified.

## Why this blocks true-physics parity
- `VAPOR.f`, `PARAM.f`, `SGRAD.f`, and `CONC.f` are highly coupled and sensitive to table values + stepping logic.
- Even with current ports, small deviations in iterative/step-control behavior produce large curve-shape drift.

## Next steps
1. Tighten full `VAPOR.f` branch/step-control parity (`KFLAG/JFLAG` flow and interval subdivision behavior).
2. Replace remaining closure constants with direct mapped terms from the legacy equations.
3. Iterate against strict fortran-inspired acceptance gate until it passes, then consider switching defaults.
