import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from kesten import run_region_physics


class TestLiquidPhysics(unittest.TestCase):
    def test_liquid_physics_returns_expected_shape(self) -> None:
        rows = run_region_physics("liquid")["rows"]

        self.assertEqual(len(rows), 24)
        for key in ("Z", "TEMP", "H", "DHDZ"):
            self.assertIn(key, rows[0])
            self.assertIn(key, rows[-1])

    def test_liquid_physics_monotonic_profile(self) -> None:
        rows = run_region_physics("liquid")["rows"]

        z_values = [row["Z"] for row in rows]
        t_values = [row["TEMP"] for row in rows]
        h_values = [row["H"] for row in rows]
        dhdz_values = [row["DHDZ"] for row in rows]

        self.assertTrue(all(b >= a for a, b in zip(z_values, z_values[1:])))
        self.assertTrue(all(b > a for a, b in zip(t_values, t_values[1:])))
        self.assertTrue(all(b > a for a, b in zip(h_values, h_values[1:])))
        self.assertTrue(all(b > a for a, b in zip(dhdz_values, dhdz_values[1:])))

    def test_liquid_physics_is_deterministic(self) -> None:
        first = run_region_physics("liquid")
        second = run_region_physics("liquid")
        self.assertEqual(first, second)

    def test_unimplemented_region_raises(self) -> None:
        with self.assertRaises(NotImplementedError):
            run_region_physics("vapor")


if __name__ == "__main__":
    unittest.main()
