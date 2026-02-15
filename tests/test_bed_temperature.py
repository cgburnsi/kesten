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

    def test_full_bed_model_tracks_reference_shape_with_loose_tolerance(self) -> None:
        model_rows = run_full_bed_temperature_model()
        ref_rows = load_reference_bed_temperature_curve("docs/verification/general_curve_data.csv")
        self.assertGreater(len(model_rows), 0)
        self.assertGreater(len(ref_rows), 1)

        ref_z = [row["Z"] for row in ref_rows]
        ref_t = [row["TEMP"] for row in ref_rows]

        def interp_ref(z_value: float) -> float:
            if z_value <= ref_z[0]:
                return ref_t[0]
            if z_value >= ref_z[-1]:
                return ref_t[-1]
            upper = 1
            while ref_z[upper] < z_value:
                upper += 1
            lower = upper - 1
            span = ref_z[upper] - ref_z[lower]
            frac = 0.0 if span <= 1e-12 else (z_value - ref_z[lower]) / span
            return ref_t[lower] + frac * (ref_t[upper] - ref_t[lower])

        sampled = model_rows[::20]
        mse = 0.0
        for row in sampled:
            delta = row["TEMP"] - interp_ref(row["Z"])
            mse += delta * delta
        rmse = (mse / max(len(sampled), 1)) ** 0.5

        model_t = [row["TEMP"] for row in model_rows]
        model_z = [row["Z"] for row in model_rows]
        ref_peak_temp = max(ref_t)
        model_peak_temp = max(model_t)
        model_peak_z = model_z[model_t.index(model_peak_temp)]
        ref_peak_z = ref_z[ref_t.index(ref_peak_temp)]

        self.assertLess(rmse, 150.0)
        self.assertLess(abs(model_peak_temp - ref_peak_temp), 120.0)
        self.assertLess(abs(model_peak_z - ref_peak_z), 0.008)
        self.assertLess(abs(model_t[-1] - ref_t[-1]), 80.0)


if __name__ == "__main__":
    unittest.main()
