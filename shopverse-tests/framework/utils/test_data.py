from pathlib import Path
import json
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
TESTDATA_ROOT = ROOT / "testdata"

def load_test_data(name: str) -> Any:
    """
    Load test data from a JSON file under testdata/ directory by logical name (without .json).
    """
    file_path = TESTDATA_ROOT / f"{name}.json"
    with file_path.open(encoding="utf-8") as f:
        return json.load(f)
