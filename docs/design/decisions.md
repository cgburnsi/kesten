# Design Decisions

## 2026-02-15
- Bootstrapped repository with a minimal deterministic solver loop to establish test and CI foundations before implementing full Kesten physics kernels.
- Chose stdlib `unittest` and `argparse` to respect dependency constraints.
- Added GitHub Actions CI to run baseline tests on push and pull request.
