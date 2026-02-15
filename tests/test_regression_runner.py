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

    def test_liquid_physics_writes_failure_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            result = run_region_regression("liquid", "physics", write_artifact=True, artifact_dir=tmpdir)

            self.assertFalse(result["meets_threshold"])
            self.assertGreater(len(result["failures"]), 0)
            self.assertIn("artifact_path", result)

            artifact = Path(result["artifact_path"])
            self.assertTrue(artifact.exists())

            payload = json.loads(artifact.read_text(encoding="utf-8"))
            self.assertEqual(payload["region"], "liquid")
            self.assertEqual(payload["source"], "physics")
            self.assertGreater(len(payload["failures"]), 0)


if __name__ == "__main__":
    unittest.main()
