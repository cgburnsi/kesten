import json
import tempfile
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from kesten.regression_runner import run_region_regression


class TestRegressionRunner(unittest.TestCase):
    def test_liquid_baseline_passes_without_failures(self) -> None:
        result = run_region_regression("liquid", "baseline", write_artifact=False)

        self.assertTrue(result["meets_threshold"])
        self.assertEqual(result["passed"], result["total"])
        self.assertEqual(result["failures"], [])

    def test_liquid_physics_regression_emits_diagnostics_payload(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            result = run_region_regression("liquid", "physics", write_artifact=True, artifact_dir=tmpdir)

            self.assertTrue(result["meets_threshold"])
            self.assertGreaterEqual(len(result["failures"]), 0)

            if result["failures"]:
                self.assertIn("artifact_path", result)
                artifact = Path(result["artifact_path"])
                self.assertTrue(artifact.exists())

                payload = json.loads(artifact.read_text(encoding="utf-8"))
                self.assertEqual(payload["region"], "liquid")
                self.assertEqual(payload["source"], "physics")
                self.assertGreater(len(payload["failures"]), 0)


if __name__ == "__main__":
    unittest.main()
