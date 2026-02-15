import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from kesten import REGION_FIELDS, REGION_TOLERANCES, compare_rows, load_region_rows, run_region_baseline


class TestGoldenParsers(unittest.TestCase):
    def test_all_regions_load_non_empty(self) -> None:
        for region in ("liquid", "vapor", "liquid_vapor"):
            rows = load_region_rows(region)
            self.assertGreater(len(rows), 0, msg=f"Expected rows for region={region}")
            for field in REGION_FIELDS[region]:
                self.assertIn(field, rows[0], msg=f"Missing field={field} for region={region}")


class TestBaselineRegression(unittest.TestCase):
    def test_liquid_region_baseline_meets_threshold(self) -> None:
        self._assert_region_passes("liquid")

    def test_vapor_region_baseline_meets_threshold(self) -> None:
        self._assert_region_passes("vapor")

    def test_liquid_vapor_region_baseline_meets_threshold(self) -> None:
        self._assert_region_passes("liquid_vapor")

    def test_baseline_is_deterministic(self) -> None:
        first = run_region_baseline("liquid")
        second = run_region_baseline("liquid")
        self.assertEqual(first, second)

    def _assert_region_passes(self, region: str) -> None:
        reference_rows = load_region_rows(region)
        model_rows = run_region_baseline(region)["rows"]

        result = compare_rows(
            reference_rows=reference_rows,
            model_rows=model_rows,
            fields=REGION_FIELDS[region],
            spec=REGION_TOLERANCES[region],
        )

        self.assertTrue(result["meets_threshold"], msg=f"Region {region} failed threshold with {result}")
        self.assertEqual(result["total"], result["passed"])


if __name__ == "__main__":
    unittest.main()
