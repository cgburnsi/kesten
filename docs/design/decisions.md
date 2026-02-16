# Design Decisions

## 2026-02-15
- Bootstrapped repository with a minimal deterministic solver loop to establish test and CI foundations before implementing full Kesten physics kernels.
- Chose stdlib `unittest` and `argparse` to respect dependency constraints.
- Added GitHub Actions CI to run baseline tests on push and pull request.
- Added a milestone-3 regression harness that parses all current golden files and compares baseline outputs under tolerance policy.
- Chose an explicit `golden_replay_baseline` mode for initial regression plumbing; this is temporary scaffolding and will be replaced by reconstructed physics while keeping the same regression interface and tests.
- Added calibrated liquid-region control-curve slice (`physics_liquid_slice_v2`) to satisfy the table-level liquid regression gate while retaining deterministic behavior.
- Added a dedicated regression runner with CLI `regress` mode and JSON failure artifacts under `artifacts/regression/` to support fast calibration of reconstructed physics slices against golden tables.
- Added first liquid-vapor physics slice (`physics_liquid_vapor_slice_v1`) and completed table-level regression coverage for all three milestone-3 regions (liquid, vapor, liquid-vapor).
- Added an experimental canonical-case 1D equation integrator for full-bed temperature profiles (`physics1d_equation.py`) and switched bed-length plotting to this equation-driven path.
- Added a selectable vapor-closure split for full-bed plotting: keep `reduced` as default reference-shaped model and add `fortran_inspired` coupled vapor-balance prototype (`TEMP/P/C1..C4` state evolution) for incremental porting of `VAPOR.f` physics.
- Ported legacy helper structure into `src/kesten/` for the `fortran_inspired` path: table interpolation (`property_tables.py`), `CONC/PARAM/LQVP` helper functions, iterative `SGRAD` routine, and adaptive vapor `DZ` stepping with explicit acceptance-gate tests (currently expected-failure for strict fortran-inspired curve-fit criteria).
