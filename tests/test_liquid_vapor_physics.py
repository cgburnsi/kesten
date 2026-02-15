import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from kesten import run_region_physics


class TestLiquidVaporPhysics(unittest.TestCase):
    def test_liquid_vapor_physics_returns_expected_shape(self) -> None:
        rows = run_region_physics("liquid_vapor")["rows"]

        self.assertEqual(len(rows), 11)
        for key in ("Z", "TEMP", "H", "WFV"):
            self.assertIn(key, rows[0])

    def test_liquid_vapor_physics_is_deterministic(self) -> None:
        first = run_region_physics("liquid_vapor")
        second = run_region_physics("liquid_vapor")
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
