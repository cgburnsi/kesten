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
from kesten.bed_temperature import load_reference_bed_temperature_curve, run_full_bed_temperature_model

CALIBRATED_WARNING = (
    "EXPERIMENTAL EQUATION MODEL: current 'physics' outputs use equation-based vapor closures "
    "for full-bed temperature with simplifying assumptions and are not yet fully validated."
)
FORTRAN_INSPIRED_WARNING = (
    "FORTRAN-INSPIRED VAPOR MODE: structural equations and table lookups are partially ported "
    "from legacy sources, but this path is still experimental and not yet a validated "
    "reproduction of the 1968 vapor-region physics."
)


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
    parser.add_argument(
        "--plot-compare",
        action="store_true",
        help="When plotting baseline/physics, overlay the opposite source for comparison",
    )
    parser.add_argument(
        "--plot-temp-bed",
        action="store_true",
        help="Plot temperature vs catalyst bed length (Z) across liquid, liquid-vapor, and vapor regions",
    )
    parser.add_argument(
        "--temp-curve-source",
        choices=("model", "reference", "both"),
        default="both",
        help="Source for --plot-temp-bed: model points, reference CSV, or both",
    )
    parser.add_argument(
        "--temp-curve-file",
        type=str,
        default=str(Path("docs") / "verification" / "general_curve_data.csv"),
        help="Reference CSV path for --plot-temp-bed when using reference or both",
    )
    parser.add_argument(
        "--temp-bed-vapor-model",
        choices=("reduced", "fortran_inspired"),
        default="reduced",
        help="Vapor closure for --plot-temp-bed model source",
    )
    return parser.parse_args()


def _plot_region_rows(
    rows: List[Dict[str, float]],
    region: str,
    mode: str,
    output_path: str = "",
    compare_rows: List[Dict[str, float]] | None = None,
    compare_label: str = "",
) -> None:
    import matplotlib.pyplot as plt
    import numpy as np

    if not rows:
        return

    x_values = [row.get("Z", float(i)) for i, row in enumerate(rows)]
    x_label = "Z" if "Z" in rows[0] else "Row Index"
    y_fields = [field for field in rows[0].keys() if field != "Z"]
    compare_enabled = bool(compare_rows) and len(compare_rows or []) == len(rows)

    if len(rows) == 1:
        field_positions = np.arange(len(y_fields))
        primary_values = np.array([rows[0][field] for field in y_fields], dtype=float)

        if compare_enabled:
            fig, axes = plt.subplots(2, 1, figsize=(10, 8))
            compare_values = np.array([compare_rows[0][field] for field in y_fields], dtype=float)
            width = 0.38
            axes[0].bar(field_positions - width / 2, primary_values, width=width, label=mode)
            axes[0].bar(field_positions + width / 2, compare_values, width=width, label=compare_label)
            axes[0].set_yscale("symlog", linthresh=1e-6)
            axes[0].legend()
            axes[0].grid(True, axis="y", alpha=0.3)
            axes[0].set_title(f"Kesten {region} single-point value comparison (experimental)")

            pct_diff = np.zeros_like(primary_values)
            for i, (value, ref) in enumerate(zip(primary_values, compare_values)):
                if abs(ref) <= 1e-12:
                    pct_diff[i] = 0.0 if abs(value) <= 1e-12 else np.nan
                else:
                    pct_diff[i] = 100.0 * (value - ref) / ref

            axes[1].bar(field_positions, pct_diff)
            axes[1].axhline(0.0, color="black", linewidth=1.0)
            axes[1].set_ylabel("% diff vs compare")
            axes[1].grid(True, axis="y", alpha=0.3)
            axes[1].set_title("Relative difference by field")
            axes[-1].set_xticks(field_positions)
            axes[-1].set_xticklabels(y_fields, rotation=20, ha="right")
            fig.tight_layout()
        else:
            fig, axis = plt.subplots(1, 1, figsize=(10, 4))
            axis.bar(field_positions, primary_values)
            axis.set_yscale("symlog", linthresh=1e-6)
            axis.set_title(f"Kesten {region} single-point field values ({mode}, experimental)")
            axis.grid(True, axis="y", alpha=0.3)
            axis.set_xticks(field_positions)
            axis.set_xticklabels(y_fields, rotation=20, ha="right")
            fig.tight_layout()

        if output_path:
            path = Path(output_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            fig.savefig(path, dpi=150)
            print(f"Saved plot: {path}")
            plt.close(fig)
            return

        plt.show()
        return

    fig, axes = plt.subplots(len(y_fields), 1, figsize=(8, max(3, 2.6 * len(y_fields))), sharex=True)
    if hasattr(axes, "plot"):
        axes = [axes]
    else:
        axes = list(axes)

    for axis, field in zip(axes, y_fields):
        axis.plot(x_values, [row[field] for row in rows], marker="o", linewidth=1.5)
        if compare_enabled:
            axis.plot(
                x_values,
                [row[field] for row in compare_rows],
                linestyle="--",
                linewidth=1.2,
                alpha=0.8,
                label=compare_label,
            )
            axis.legend(loc="best")
        axis.set_ylabel(field)
        axis.grid(True, alpha=0.3)

    axes[-1].set_xlabel(x_label)
    fig.suptitle(f"Kesten {region} {mode} profile (experimental reduced equation model)")
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


def _collect_bed_temperature_points(source: str, vapor_model: str = "reduced") -> List[Dict[str, float]]:
    if source == "physics":
        return run_full_bed_temperature_model(vapor_model=vapor_model)

    region_order = ("liquid", "liquid_vapor", "vapor")
    points: List[Dict[str, float]] = []

    for region in region_order:
        if source == "physics":
            result = run_region_physics(region)
        else:
            result = run_region_baseline(region)

        for row in result["rows"]:
            if "Z" not in row or "TEMP" not in row:
                continue
            points.append(
                {
                    "Z": float(row["Z"]),
                    "TEMP": float(row["TEMP"]),
                    "region": region,
                }
            )

    points.sort(key=lambda item: item["Z"])
    return points


def _plot_temperature_vs_bed(
    points: List[Dict[str, float]],
    mode_label: str,
    curve_source: str,
    output_path: str = "",
    compare_points: List[Dict[str, float]] | None = None,
    compare_label: str = "",
    reference_points: List[Dict[str, float]] | None = None,
    model_label: str = "reduced",
) -> None:
    import matplotlib.pyplot as plt

    if not points and not reference_points:
        return

    fig, axis = plt.subplots(1, 1, figsize=(9, 4.5))
    model_plotted = False
    reference_plotted = False

    if curve_source in ("model", "both") and points:
        x_values = [p["Z"] for p in points]
        y_values = [p["TEMP"] for p in points]
        axis.plot(x_values, y_values, marker="o", linewidth=1.8, label=mode_label)
        model_plotted = True

    if curve_source in ("reference", "both") and reference_points:
        axis.plot(
            [p["Z"] for p in reference_points],
            [p["TEMP"] for p in reference_points],
            linewidth=2.0,
            linestyle="-",
            label="reference_curve",
        )
        reference_plotted = True

    if compare_points:
        axis.plot(
            [p["Z"] for p in compare_points],
            [p["TEMP"] for p in compare_points],
            linestyle="--",
            linewidth=1.5,
            alpha=0.9,
            label=compare_label,
        )
        axis.legend(loc="best")

    if model_plotted or reference_plotted or compare_points:
        axis.legend(loc="best")
    axis.set_xlabel("Catalyst bed length Z [ft]")
    axis.set_ylabel("Temperature [degR]")
    axis.set_title(f"Temperature vs catalyst bed length ({model_label} equation model, experimental)")
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
    reference_curve_points = load_reference_bed_temperature_curve(args.temp_curve_file)
    if args.mode == "baseline":
        baseline_result = run_region_baseline(args.region)
        baseline_result["row_count"] = len(baseline_result["rows"])
        print(json.dumps(baseline_result, indent=2))
        if args.plot_temp_bed:
            if args.temp_bed_vapor_model == "fortran_inspired":
                print(FORTRAN_INSPIRED_WARNING)
            compare_points = None
            compare_label = ""
            if args.plot_compare:
                compare_points = _collect_bed_temperature_points("physics", vapor_model=args.temp_bed_vapor_model)
                compare_label = "physics"
            _plot_temperature_vs_bed(
                points=_collect_bed_temperature_points("baseline", vapor_model=args.temp_bed_vapor_model),
                mode_label="baseline",
                curve_source=args.temp_curve_source,
                output_path=args.plot_output,
                compare_points=compare_points,
                compare_label=compare_label,
                reference_points=reference_curve_points,
                model_label=args.temp_bed_vapor_model,
            )
            return
        if args.plot or args.plot_output:
            compare_rows = None
            compare_label = ""
            if args.plot_compare:
                compare_rows = run_region_physics(args.region)["rows"]
                compare_label = "physics"
            _plot_region_rows(
                rows=baseline_result["rows"],
                region=args.region,
                mode="baseline",
                output_path=args.plot_output,
                compare_rows=compare_rows,
                compare_label=compare_label,
            )
        return
    if args.mode == "physics":
        physics_result = run_region_physics(args.region)
        physics_result["row_count"] = len(physics_result["rows"])
        physics_result["warning"] = CALIBRATED_WARNING
        print(json.dumps(physics_result, indent=2))
        print(CALIBRATED_WARNING)
        if args.plot_temp_bed:
            if args.temp_bed_vapor_model == "fortran_inspired":
                print(FORTRAN_INSPIRED_WARNING)
            compare_points = None
            compare_label = ""
            if args.plot_compare:
                compare_points = _collect_bed_temperature_points("baseline")
                compare_label = "baseline"
            _plot_temperature_vs_bed(
                points=_collect_bed_temperature_points("physics", vapor_model=args.temp_bed_vapor_model),
                mode_label="physics",
                curve_source=args.temp_curve_source,
                output_path=args.plot_output,
                compare_points=compare_points,
                compare_label=compare_label,
                reference_points=reference_curve_points,
                model_label=args.temp_bed_vapor_model,
            )
            return
        if args.plot or args.plot_output:
            compare_rows = None
            compare_label = ""
            if args.plot_compare:
                compare_rows = run_region_baseline(args.region)["rows"]
                compare_label = "baseline"
            _plot_region_rows(
                rows=physics_result["rows"],
                region=args.region,
                mode="physics",
                output_path=args.plot_output,
                compare_rows=compare_rows,
                compare_label=compare_label,
            )
        return
    if args.mode == "regress":
        regression_result = run_region_regression(
            region=args.region,
            source=args.source,
            write_artifact=True,
            artifact_dir=args.artifact_dir,
        )
        if args.source == "physics":
            regression_result["warning"] = CALIBRATED_WARNING
        print(json.dumps(regression_result, indent=2))
        if args.source == "physics":
            print(CALIBRATED_WARNING)
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
