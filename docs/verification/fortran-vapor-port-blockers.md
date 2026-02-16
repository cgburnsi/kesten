# Fortran Vapor Port Blockers

## Session handoff (2026-02-16)
- Working branch at pause: `feat/full-physics-fortran-port`
- Last pushed commit: `a849388`
- Local uncommitted work exists in: `src/kesten/physics1d_equation.py`
- Goal at pause: make `fortran_inspired` a true computed vapor-physics port (no synthetic curve shaping).

## Current status
- `fortran_inspired` vapor mode includes:
  - table-driven interpolation path (`unbar` + property tables)
  - helper routine ports for `CONC`, `PARAM`, and `LQVP`
  - iterative `SGRAD`-style routine (`sgrad_full_port`)
  - vapor-region coupled balances with adaptive `dz`
- Recent translation fixes added in local (not pushed) work:
  - added Fortran-style compressibility-coupling path (`DRDZR`/`T5`) into `DCi/DZ`
  - removed non-Fortran heat-loss term from vapor `dT/dz`
  - corrected `DWi/DZ` terms to use `Wi` in the feed-correction term
- It is still **not** a faithful Kesten 1968 vapor-region reproduction.

## Repro commands
1. `python -m unittest discover -s tests -v`
2. `python app/run_solver.py --mode physics --plot-temp-bed --temp-bed-vapor-model reduced --temp-curve-source both --temp-curve-file docs/verification/general_curve_data.csv --plot-output artifacts/plots/temp_vs_bed_reduced.png`
3. `python app/run_solver.py --mode physics --plot-temp-bed --temp-bed-vapor-model fortran_inspired --temp-curve-source both --temp-curve-file docs/verification/general_curve_data.csv --plot-output artifacts/plots/temp_vs_bed_fortran_inspired.png`

## Observed model-vs-reference summary at pause
- Reference curve source: `docs/verification/general_curve_data.csv`
- `reduced` mode:
  - RMSE ~= 274.7
  - peak ~= 2017 degR at `z ~= 0.0073`
  - end temp ~= 1843 degR
- `fortran_inspired` mode:
  - RMSE ~= 268.7
  - peak hits current cap (`2150 degR`) at `z ~= 0.0221`
  - end temp ~= 2025 degR
- Reference:
  - peak ~= 2054 degR at `z ~= 0.0118`
  - end temp ~= 1815.7 degR

## Remaining blockers
- Strict `fortran_inspired` acceptance gate (peak location/shape/end-state) still fails.
- `VAPOR.f` branch-control parity is incomplete:
  - `KFLAG/JFLAG/KOUNT/N` flow
  - `REDIVD`-style interval subdivision
  - slope-turn/first-peak branch behavior
- Legacy data is sparse for vapor-path checkpoints (current golden has one vapor row), so step-by-step parity is hard to confirm.

## Why this still blocks parity
- `VAPOR.f`, `PARAM.f`, `SGRAD.f`, and table lookups are tightly coupled.
- Small differences in step control and derivative coupling move the peak location and cooling tail significantly.
- Current output still relies on guardrails (`fortran_max_temp`, source caps) to stay numerically stable.

## Restart plan (recommended order)
1. Implement line-by-line `VAPOR.f` control flow in Python (`KFLAG/JFLAG/KOUNT/N`, step subdivision, slope-turn logic).
2. Add a vapor debug trace writer per axial step (`z,temp,p,h,c1..c4,t2,t3,t4,dhdz,dtdz,dpdz,dz`) under `artifacts/diagnostics/`.
3. Add verification fixture(s) with intermediate vapor checkpoints so parity is tested on more than one endpoint.
4. Remove or loosen guardrail clamps only after step-trace parity is acceptable.
5. Re-run acceptance and document the final verified tolerance in `docs/verification/tolerances.md`.
