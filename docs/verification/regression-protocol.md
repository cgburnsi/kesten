# Regression Protocol

## Purpose
Standardize how regression comparisons are run and how failures are handled.

## Run protocol
1. Execute deterministic solver run for target case.
2. Compare against golden values using `docs/verification/tolerances.md`.
3. Emit per-value pass/fail records and summary pass percentage.
4. Store failure details sufficient for reproduction.

Current CLI path:
- `python app/run_solver.py --mode regress --region liquid --source baseline`
- `python app/run_solver.py --mode regress --region liquid --source physics`
- `python app/run_solver.py --mode regress --region vapor --source baseline`
- `python app/run_solver.py --mode regress --region vapor --source physics`

## Failure logging requirements
- Test/case identifier
- Golden file and row/column index
- Reference value
- Model value
- Absolute error
- Relative error
- Applied tolerances
- Artifact path (when failures are written)

Current artifact convention:
- `artifacts/regression/<region>_<source>_failures.json`

## Decision policy for failures
- If failures are due to code changes: treat as regression until explained and approved.
- If failures suggest tolerance mismatch: propose adjustment with evidence and update `docs/design/decisions.md` only after approval.
- If failures suggest source ambiguity: document in conversion notes and open a verification action item.

## Repeatability check
- Run each regression case at least twice in the same environment when introducing a new solver path.
- Results must be stable within tolerance.
