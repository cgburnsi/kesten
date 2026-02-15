"""CLI wrapper for the minimal steady-state solver."""

import argparse
import json
from pathlib import Path
import sys
from typing import Dict, List

ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from kesten import SolverConfig, run_region_baseline, run_region_physics, run_region_regression, run_solver


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run minimal Kesten steady-state solver loop.")
    parser.add_argument(
        "--mode",
        choices=("iterate", "baseline", "physics", "regress"),
        default="iterate",
        help="iterate: fixed-point loop, baseline: replay golden dataset, physics: reconstructed region slice, regress: compare model source to golden data",
    )
    parser.add_argument(
        "--region",
        choices=("liquid", "vapor", "liquid_vapor"),
        default="liquid",
        help="Region key used by baseline/physics/regress modes",
    )
    parser.add_argument(
        "--source",
        choices=("baseline", "physics"),
        default="baseline",
        help="Model source for --mode regress",
    )
    parser.add_argument(
        "--artifact-dir",
        type=str,
        default=str(Path("artifacts") / "regression"),
        help="Output directory for regression failure artifacts",
    )
    parser.add_argument("--initial", type=float, default=0.0, help="Initial state value")
    parser.add_argument("--target", type=float, default=1.0, help="Target steady-state value")
    parser.add_argument("--max-iterations", type=int, default=100, help="Maximum solver iterations")
    parser.add_argument("--tolerance", type=float, default=1e-8, help="Convergence tolerance")
    parser.add_argument("--relaxation", type=float, default=0.5, help="Relaxation factor in (0,1]")
    parser.add_argument(
        "--plot",
        action="store_true",
        help="Show a plot for baseline/physics/iterate outputs",
    )
    parser.add_argument(
        "--plot-output",
        type=str,
        default="",
        help="Optional PNG path to save plots (e.g., artifacts/plots/liquid_physics.png)",
    )
    return parser.parse_args()


def _plot_region_rows(rows: List[Dict[str, float]], region: str, mode: str, output_path: str = "") -> None:
    import matplotlib.pyplot as plt

    if not rows:
        return

    x_values = [row.get("Z", float(i)) for i, row in enumerate(rows)]
    x_label = "Z" if "Z" in rows[0] else "Row Index"
    y_fields = [field for field in rows[0].keys() if field != "Z"]

    fig, axes = plt.subplots(len(y_fields), 1, figsize=(8, max(3, 2.6 * len(y_fields))), sharex=True)
    if hasattr(axes, "plot"):
        axes = [axes]
    else:
        axes = list(axes)

    for axis, field in zip(axes, y_fields):
        axis.plot(x_values, [row[field] for row in rows], marker="o", linewidth=1.5)
        axis.set_ylabel(field)
        axis.grid(True, alpha=0.3)

    axes[-1].set_xlabel(x_label)
    fig.suptitle(f"Kesten {region} {mode} profile")
    fig.tight_layout()

    if output_path:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(path, dpi=150)
        print(f"Saved plot: {path}")
        plt.close(fig)
        return

    plt.show()


def _plot_iterate_result(result: Dict[str, object], output_path: str = "") -> None:
    import matplotlib.pyplot as plt

    residual_history = result.get("residual_history", ())
    if not residual_history:
        return

    iterations = list(range(1, len(residual_history) + 1))
    fig, axis = plt.subplots(1, 1, figsize=(8, 4))
    axis.plot(iterations, residual_history, marker="o", linewidth=1.5)
    axis.set_xlabel("Iteration")
    axis.set_ylabel("Absolute Residual")
    axis.set_title("Fixed-point convergence history")
    axis.grid(True, alpha=0.3)
    fig.tight_layout()

    if output_path:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(path, dpi=150)
        print(f"Saved plot: {path}")
        plt.close(fig)
        return

    plt.show()


def main() -> None:
    args = parse_args()
    if args.mode == "baseline":
        baseline_result = run_region_baseline(args.region)
        baseline_result["row_count"] = len(baseline_result["rows"])
        print(json.dumps(baseline_result, indent=2))
        if args.plot or args.plot_output:
            _plot_region_rows(
                rows=baseline_result["rows"],
                region=args.region,
                mode="baseline",
                output_path=args.plot_output,
            )
        return
    if args.mode == "physics":
        physics_result = run_region_physics(args.region)
        physics_result["row_count"] = len(physics_result["rows"])
        print(json.dumps(physics_result, indent=2))
        if args.plot or args.plot_output:
            _plot_region_rows(
                rows=physics_result["rows"],
                region=args.region,
                mode="physics",
                output_path=args.plot_output,
            )
        return
    if args.mode == "regress":
        regression_result = run_region_regression(
            region=args.region,
            source=args.source,
            write_artifact=True,
            artifact_dir=args.artifact_dir,
        )
        print(json.dumps(regression_result, indent=2))
        return

    config = SolverConfig(
        max_iterations=args.max_iterations,
        tolerance=args.tolerance,
        relaxation=args.relaxation,
    )
    result = run_solver(initial_value=args.initial, target_value=args.target, config=config)
    print(json.dumps(result, indent=2))
    if args.plot or args.plot_output:
        _plot_iterate_result(result=result, output_path=args.plot_output)


if __name__ == "__main__":
    main()
