# kesten

A small, deterministic Python library for reproducing the steady-state numerical models described in A.S. Kesten (1968).

## Current milestone
- Milestone 1: quick, readable conversion of the original document and Fortran source
- Milestone 2: production-grade faithful conversion of the original document and Fortran source
- Milestone 3: completed baseline 1D reconstruction and regression gates
- Milestone 4+: 2D solver reconstruction and verification against Kesten reference outputs

## Current phase workflow
- Conversion rules: `docs/conversion/spec.md`
- Conversion style guide: `docs/conversion/style-guide.md`
- Conversion source mapping: `docs/conversion/source-map.md`
- Conversion acceptance criteria: `docs/conversion/acceptance.md`
- Conversion progress log: `docs/conversion/worklog.md`
- Conversion QA checklist: `docs/conversion/qa_checklist.md`
- Implementation rules (milestones 3-4): `docs/implementation/spec.md`
- Implementation module plan: `docs/implementation/module-plan.md`
- Implementation test matrix: `docs/implementation/test-matrix.md`
- Verification tolerances: `docs/verification/tolerances.md`
- Verification golden index: `docs/verification/golden-index.md`
- Verification regression protocol: `docs/verification/regression-protocol.md`
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

## Run baseline regression example
```sh
python examples/ex02_baseline_regression.py
```

## Run liquid physics slice
```sh
python app/run_solver.py --mode physics --region liquid
python app/run_solver.py --mode physics --region vapor
python app/run_solver.py --mode physics --region liquid_vapor
```

## Plot outputs
```sh
# Interactive plot window
python app/run_solver.py --mode physics --region liquid --plot

# Save PNG
python app/run_solver.py --mode physics --region liquid --plot-output artifacts/plots/liquid_physics.png
python app/run_solver.py --mode iterate --initial 0 --target 1 --max-iterations 50 --plot-output artifacts/plots/iterate_residual.png
```

## Run regression gate
```sh
python app/run_solver.py --mode regress --region liquid --source baseline
python app/run_solver.py --mode regress --region liquid --source physics
python app/run_solver.py --mode regress --region vapor --source physics
python app/run_solver.py --mode regress --region liquid_vapor --source physics
```

## Build LaTeX PDF
```sh
tools/build_pdf.sh
```
- Build details and options: `docs/latex/BUILD.md`

## Notes
- Dependencies are intentionally restricted to Python stdlib + NumPy + Matplotlib.
- Keep architectural decisions in `docs/design/decisions.md`.
- Keep verification gates and acceptance criteria in `docs/verification/plan.md`.
