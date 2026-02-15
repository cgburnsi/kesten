import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from kesten import SolverConfig, run_solver


class TestSolver(unittest.TestCase):
    def test_solver_converges_to_target(self) -> None:
        config = SolverConfig(max_iterations=200, tolerance=1e-10, relaxation=0.5)
        result = run_solver(initial_value=0.0, target_value=1.0, config=config)

        self.assertTrue(result["converged"])
        self.assertLessEqual(abs(1.0 - result["value"]), config.tolerance)
        self.assertGreater(result["iterations"], 0)

    def test_solver_hits_max_iterations_when_not_converged(self) -> None:
        config = SolverConfig(max_iterations=2, tolerance=1e-12, relaxation=0.01)
        result = run_solver(initial_value=0.0, target_value=1.0, config=config)

        self.assertFalse(result["converged"])
        self.assertEqual(result["iterations"], config.max_iterations)


if __name__ == "__main__":
    unittest.main()
