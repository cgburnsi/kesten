import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from kesten.bed_temperature import load_reference_bed_temperature_curve, run_full_bed_temperature_model


def _interp_ref(reference_rows, z_value: float) -> float:
    ref_z = [row["Z"] for row in reference_rows]
    ref_t = [row["TEMP"] for row in reference_rows]
    if z_value <= ref_z[0]:
        return ref_t[0]
    if z_value >= ref_z[-1]:
        return ref_t[-1]
    upper = 1
    while ref_z[upper] < z_value:
        upper += 1
    lower = upper - 1
    span = ref_z[upper] - ref_z[lower]
    frac = 0.0 if span <= 1.0e-12 else (z_value - ref_z[lower]) / span
    return ref_t[lower] + frac * (ref_t[upper] - ref_t[lower])


def _metrics(vapor_model: str) -> tuple[float, float, float, float]:
    rows = run_full_bed_temperature_model(vapor_model=vapor_model)
    reference = load_reference_bed_temperature_curve("docs/verification/general_curve_data.csv")
    sampled = rows[:: max(1, len(rows) // 30)]
    mse = 0.0
    for row in sampled:
        delta = row["TEMP"] - _interp_ref(reference, row["Z"])
        mse += delta * delta
    rmse = (mse / max(len(sampled), 1)) ** 0.5

    temperatures = [row["TEMP"] for row in rows]
    z_values = [row["Z"] for row in rows]
    peak_temp = max(temperatures)
    peak_z = z_values[temperatures.index(peak_temp)]
    end_temp = temperatures[-1]
    return rmse, peak_temp, peak_z, end_temp


class TestFortranInspiredAcceptance(unittest.TestCase):
    def test_reduced_model_reference_gate(self) -> None:
        rmse, peak_temp, peak_z, end_temp = _metrics("reduced")
        self.assertLess(rmse, 150.0)
        self.assertLess(abs(peak_temp - 2054.2897), 120.0)
        self.assertLess(abs(peak_z - 0.011785), 0.008)
        self.assertLess(abs(end_temp - 1815.6890), 80.0)

    @unittest.expectedFailure
    def test_fortran_inspired_reference_gate(self) -> None:
        rmse, peak_temp, peak_z, end_temp = _metrics("fortran_inspired")
        self.assertLess(rmse, 220.0)
        self.assertLess(abs(peak_temp - 2054.2897), 180.0)
        self.assertLess(abs(peak_z - 0.011785), 0.010)
        self.assertLess(abs(end_temp - 1815.6890), 120.0)


if __name__ == "__main__":
    unittest.main()
