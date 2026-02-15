# Design Decisions

## 2026-02-15
- Bootstrapped repository with a minimal deterministic solver loop to establish test and CI foundations before implementing full Kesten physics kernels.
- Chose stdlib `unittest` and `argparse` to respect dependency constraints.
- Added GitHub Actions CI to run baseline tests on push and pull request.
- Added a milestone-3 regression harness that parses all current golden files and compares baseline outputs under tolerance policy.
- Chose an explicit `golden_replay_baseline` mode for initial regression plumbing; this is temporary scaffolding and will be replaced by reconstructed physics while keeping the same regression interface and tests.
