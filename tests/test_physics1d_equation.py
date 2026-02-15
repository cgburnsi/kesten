import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from kesten.physics1d_equation import EquationModelConfig, run_canonical_case_equation_profile


class TestPhysics1DEquation(unittest.TestCase):
    def test_profile_spans_bed(self) -> None:
        rows = run_canonical_case_equation_profile()
        self.assertGreater(len(rows), 50)
        self.assertAlmostEqual(rows[0]["Z"], 0.0, places=9)
        self.assertAlmostEqual(rows[-1]["Z"], 0.25, places=6)

    def test_profile_has_phase_progression(self) -> None:
        rows = run_canonical_case_equation_profile()
        regions = {row["region"] for row in rows}
        self.assertIn("liquid", regions)
        self.assertIn("liquid_vapor", regions)
        self.assertIn("vapor", regions)

    def test_profile_temperature_peak_and_decline(self) -> None:
        rows = run_canonical_case_equation_profile()
        temps = [row["TEMP"] for row in rows]
        peak = max(range(len(temps)), key=lambda i: temps[i])
        self.assertTrue(all(b >= a for a, b in zip(temps[:peak], temps[1:peak + 1])))
        self.assertTrue(all(b <= a for a, b in zip(temps[peak:], temps[peak + 1:])))

    def test_fortran_inspired_vapor_model_is_stable_and_deterministic(self) -> None:
        config = EquationModelConfig(vapor_model="fortran_inspired")
        first = run_canonical_case_equation_profile(config=config)
        second = run_canonical_case_equation_profile(config=config)

        self.assertEqual(first, second)
        self.assertGreater(len(first), 50)
        z_values = [row["Z"] for row in first]
        temp_values = [row["TEMP"] for row in first]

        self.assertTrue(all(b > a for a, b in zip(z_values, z_values[1:])))
        self.assertTrue(all(value > 0.0 for value in temp_values))
        self.assertAlmostEqual(first[-1]["Z"], 0.25, places=6)


if __name__ == "__main__":
    unittest.main()
