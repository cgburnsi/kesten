from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from kesten import REGION_TOLERANCES, compare_rows, load_region_rows, run_region_baseline


REGION_FIELDS = {
    "liquid": ("Z", "TEMP", "H", "DHDZ"),
    "vapor": ("Z", "TEMP", "P", "H", "C1", "C2", "C3", "C4"),
    "liquid_vapor": ("Z", "TEMP", "H", "WFV"),
}


if __name__ == "__main__":
    for region, fields in REGION_FIELDS.items():
        reference = load_region_rows(region)
        model = run_region_baseline(region)["rows"]
        result = compare_rows(reference, model, fields, REGION_TOLERANCES[region])
        print(region, result["passed"], "/", result["total"], "pass_fraction=", f"{result['pass_fraction']:.3f}")
