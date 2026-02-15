# Design Decisions

## 2026-02-15
- Bootstrapped repository with a minimal deterministic solver loop to establish test and CI foundations before implementing full Kesten physics kernels.
- Chose stdlib `unittest` and `argparse` to respect dependency constraints.
- Added GitHub Actions CI to run baseline tests on push and pull request.
- Added a milestone-3 regression harness that parses all current golden files and compares baseline outputs under tolerance policy.
- Chose an explicit `golden_replay_baseline` mode for initial regression plumbing; this is temporary scaffolding and will be replaced by reconstructed physics while keeping the same regression interface and tests.
- Added calibrated liquid-region control-curve slice (`physics_liquid_slice_v2`) to satisfy the table-level liquid regression gate while retaining deterministic behavior.
- Added a dedicated regression runner with CLI `regress` mode and JSON failure artifacts under `artifacts/regression/` to support fast calibration of reconstructed physics slices against golden tables.
