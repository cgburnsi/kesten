# kesten

A small, deterministic Python library for reproducing the steady-state numerical models described in A.S. Kesten (1968).

## Current milestone
- Minimal, testable solver loop
- Baseline regression-friendly test pipeline

## Repository layout
- `src/` core library code
- `app/` command-line entry points
- `tests/` unittest test suite
- `examples/` minimal runnable examples
- `docs/` design and verification notes
- `tools/` helper scripts

## Local setup
```sh
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install numpy matplotlib
```

## Run tests
```sh
python -m unittest discover -s tests -v
```

## Run example
```sh
python examples/ex01_minimal_solver.py
```

## Notes
- Dependencies are intentionally restricted to Python stdlib + NumPy + Matplotlib.
- Keep architectural decisions in `docs/design/decisions.md`.
- Keep verification gates and acceptance criteria in `docs/verification/plan.md`.
