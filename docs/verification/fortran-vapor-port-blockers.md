# Fortran Vapor Port Blockers

## Current status
- `fortran_inspired` vapor mode ports part of the `VAPOR.f` balance structure.
- It is **not** yet a faithful Kesten 1968 vapor-region reproduction.

## Missing source artifacts
- `docs/fortran/UNBAR.f` is effectively empty in this repo.
- `docs/fortran/TABLES.f` is effectively empty in this repo.
- These are required for original property interpolation and table values:
  - `TBLVP`, `TBLH4`, `TBLH3`
  - `SHTBL1..SHTBL4`
  - `DHVST`, `DHLVST`, `VPTBL`
  - viscosity/auxiliary tables referenced by `UNBAR`

## Why this blocks true-physics parity
- `VAPOR.f`, `PARAM.f`, `SGRAD.f`, and `CONC.f` rely on table-driven property lookups.
- Without those tables and the original interpolation routine, vapor rates and energy terms cannot be reconstructed exactly.

## Immediate next step once files are available
1. Port `UNBAR` interpolation behavior verbatim.
2. Port block-data tables into Python arrays.
3. Replace provisional vapor property closures with table lookups.
4. Re-run vapor/bed-shape verification against Kesten outputs.
