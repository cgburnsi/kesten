from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from kesten import SolverConfig, run_solver


if __name__ == "__main__":
    config = SolverConfig(max_iterations=50, tolerance=1e-8, relaxation=0.5)
    result = run_solver(initial_value=0.0, target_value=1.0, config=config)
    print(result)
