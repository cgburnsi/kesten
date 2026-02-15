"""CLI wrapper for the minimal steady-state solver."""

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from kesten import SolverConfig, run_solver


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run minimal Kesten steady-state solver loop.")
    parser.add_argument("--initial", type=float, default=0.0, help="Initial state value")
    parser.add_argument("--target", type=float, default=1.0, help="Target steady-state value")
    parser.add_argument("--max-iterations", type=int, default=100, help="Maximum solver iterations")
    parser.add_argument("--tolerance", type=float, default=1e-8, help="Convergence tolerance")
    parser.add_argument("--relaxation", type=float, default=0.5, help="Relaxation factor in (0,1]")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = SolverConfig(
        max_iterations=args.max_iterations,
        tolerance=args.tolerance,
        relaxation=args.relaxation,
    )
    result = run_solver(initial_value=args.initial, target_value=args.target, config=config)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
