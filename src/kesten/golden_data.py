"""Load and normalize legacy Kesten golden output files."""

from __future__ import annotations

from pathlib import Path
import re
from typing import Dict, List


PROJECT_ROOT = Path(__file__).resolve().parents[2]
VERIFICATION_DIR = PROJECT_ROOT / "docs" / "verification"

REGION_TO_FILE = {
    "liquid": "liquid_region_kesten_output.txt",
    "vapor": "Vapor Region Correct Output.txt",
    "liquid_vapor": "LV_region_Kesten_Output.txt",
}


def _normalize_number_token(token: str) -> str:
    text = token.strip().replace("\t", "")

    # Legacy FORTRAN-like exponent format, e.g. ".530000+03" or ".251216-03".
    if re.match(r"^[+-]?\d*\.\d+[+-]\d{2}$", text):
        return f"{text[:-3]}E{text[-3:]}"

    # OCR artifact seen in vapor data (e.g. ".2966e7-01"): keep trailing signed exponent.
    if re.match(r"^[+-]?\d*\.\d+[eE]\d+[+-]\d+$", text):
        return re.sub(r"([eE])\d+([+-]\d+)$", r"\1\2", text)

    return text


def _parse_float(token: str) -> float:
    return float(_normalize_number_token(token))


def _load_liquid_rows(path: Path) -> List[Dict[str, float]]:
    rows: List[Dict[str, float]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        raw = line.strip()
        if not raw:
            continue
        if raw.upper().startswith("Z"):
            continue

        parts = raw.split()
        if len(parts) != 4:
            continue

        rows.append(
            {
                "Z": _parse_float(parts[0]),
                "TEMP": _parse_float(parts[1]),
                "H": _parse_float(parts[2]),
                "DHDZ": _parse_float(parts[3]),
            }
        )
    return rows


def _load_tagged_rows(path: Path) -> List[Dict[str, float]]:
    rows: List[Dict[str, float]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        raw = line.strip()
        if not raw:
            continue

        row: Dict[str, float] = {}
        for item in raw.split(","):
            match = re.match(r"^\s*([A-Za-z0-9]+)\s*:\s*([^\s\[,]+)", item)
            if not match:
                continue
            key = match.group(1).upper()
            value = match.group(2)
            row[key] = _parse_float(value)

        if row:
            rows.append(row)
    return rows


def load_region_rows(region: str, path: str | Path | None = None) -> List[Dict[str, float]]:
    """Load parsed golden rows for one region.

    Supported regions: liquid, vapor, liquid_vapor
    """

    normalized_region = region.strip().lower()
    if normalized_region not in REGION_TO_FILE:
        raise ValueError(f"Unsupported region '{region}'")

    target = Path(path) if path is not None else VERIFICATION_DIR / REGION_TO_FILE[normalized_region]

    if normalized_region == "liquid":
        return _load_liquid_rows(target)

    return _load_tagged_rows(target)
