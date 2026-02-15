import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from kesten.bed_temperature import load_reference_bed_temperature_curve, run_full_bed_temperature_model


class TestBedTemperatureModel(unittest.TestCase):
    def test_full_bed_model_is_monotonic_in_z(self) -> None:
        rows = run_full_bed_temperature_model()
        z_values = [row["Z"] for row in rows]
        self.assertTrue(all(b > a for a, b in zip(z_values, z_values[1:])))

    def test_full_bed_model_has_single_peak_shape(self) -> None:
        rows = run_full_bed_temperature_model()
        temps = [row["TEMP"] for row in rows]
        peak_index = max(range(len(temps)), key=temps.__getitem__)

        self.assertTrue(all(b >= a for a, b in zip(temps[:peak_index], temps[1:peak_index + 1])))
        self.assertTrue(all(b <= a for a, b in zip(temps[peak_index:], temps[peak_index + 1:])))

    def test_reference_curve_loader_reads_points(self) -> None:
        rows = load_reference_bed_temperature_curve("docs/verification/general_curve_data.csv")
        self.assertGreater(len(rows), 0)
        self.assertIn("Z", rows[0])
        self.assertIn("TEMP", rows[0])


if __name__ == "__main__":
    unittest.main()
