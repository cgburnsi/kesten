import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from kesten.regression_runner import run_region_regression


class TestLiquidVaporPhysicsRegression(unittest.TestCase):
    def test_liquid_vapor_physics_meets_threshold(self) -> None:
        result = run_region_regression("liquid_vapor", "physics", write_artifact=False)

        self.assertTrue(result["meets_threshold"], msg=str(result))


if __name__ == "__main__":
    unittest.main()
