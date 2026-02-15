# AGENTS.md — How to work in this repo (Python)

This file is a **map + operating rules** for agents working on this codebase.
It is not the full design spec. When in doubt, follow the docs listed below.

## Project intent 
Build a small, correct, legible, modular, Python library that implements the steady-state numerical models described in A.S. Kesten's 1968 paper.
- The first milestone is a minimal, testable solver loop and an automated test pipeline that catches regressions.

## Source of truth (read these first)
- README.md — how to install/run and what the repo is for
- ARCHITECTURE.md — module boundaries and data ownership rules
- docs/verification/plan.md — verification strategy + acceptance gates
- docs/design/decisions.md — decision log (add entries when changing direction)

If any of these files are missing, create them as small stubs rather than
inventing undocumented architecture.

## Definition of Done (for any change)
A change is “done” only if:
1. It runs without errors for the intended use case.
2. Tests pass (unit + any applicable regression tests).
3. New behavior has tests (or an explicit note why it cannot).
4. Docs are updated when behavior/CLI/file formats change.
5. The change is deterministic (within stated tolerances).
6. No unrelated refactors are mixed in.
7. Dependency rules (below) are respected.
8. Results match the values provided in the Kesten report from 1968.

## Work style rules
### Keep changes small and reviewable
- Prefer multiple small PRs over one large PR.
- Each PR should have a clear goal and short summary.

### Be deterministic
- Avoid nondeterminism. If randomness is required, seed it and document why.
- Numerical outputs should be stable across machines within tolerances.
- If results differ by CPU/BLAS/platform, encode tolerance-based checks.

### Respect module boundaries
- No “god modules.” Keep files focused.
- Avoid circular imports.
- Modules should follow the code layout in the Kesten paper.
- Keep data ownership clear: who constructs, mutates, and consumes arrays.

### Avoid premature complexity
- No GPU/MPI/multiprocessing until verification harness is solid.
- Prefer simple numerics and clean interfaces over cleverness.

## Dependencies (hard rule)
This project must run with only:
- Python standard library
- NumPy
- Matplotlib

No other packages may be added (runtime or development). This includes (but is
not limited to): scipy, numba, pandas, sympy, meshio, shapely, pyvista, tqdm,
rich, click/typer, pydantic, pytest, ruff, black, etc.

### Dependency gate (must follow)
If any task appears to require a new dependency:
1. **Stop immediately.**
2. Write a short note (issue/PR comment/docs snippet) that includes:
   - What feature is blocked
   - Why stdlib + NumPy + Matplotlib are insufficient
   - Two alternative approaches that keep the dependency set unchanged
   - If still justified: the proposed dependency, its scope, and why it’s worth it
3. Do **not** add the dependency or refactor towards it until explicit approval.

### Guidance under this constraint
- Use `argparse` for CLI (stdlib), not click/typer.
- Use stdlib `unittest` for tests (no pytest).
- Use stdlib `json`, `csv`, `pathlib`, `logging` for I/O and instrumentation.
- Keep plotting in `examples/` or `tools/` when possible (avoid importing
  matplotlib in the core solver path unless necessary).

## Repo conventions (expected layout)
(If the repo differs, update this section.)

- src/                       core library code
- app/                       command line entry points (thin wrappers)
- tests/                     unittest tests
- examples/                  runnable examples (kept small)
- docs/                      design + verification notes
- tools/                     helper scripts (goldens/plots/etc.)

## Setup (local)
From the repo root:

```sh
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install numpy matplotlib
```

