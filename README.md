# kesten

A small, deterministic Python library for reproducing the steady-state numerical models described in A.S. Kesten (1968).

## Current milestone
- Milestone 1: quick, readable conversion of the original document and Fortran source
- Milestone 2: production-grade faithful conversion of the original document and Fortran source
- Milestone 3+: solver reconstruction and verification against Kesten reference outputs

## Current phase workflow
- Conversion rules: `docs/conversion/spec.md`
- Conversion progress log: `docs/conversion/worklog.md`
- Conversion QA checklist: `docs/conversion/qa_checklist.md`
- Verification tolerances: `docs/verification/tolerances.md`
- Decision history: `docs/design/decisions.md`

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
