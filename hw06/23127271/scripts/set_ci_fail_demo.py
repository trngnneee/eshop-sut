#!/usr/bin/env python3
"""Set ciFailDemo collection variable for CI pass/fail homework demo."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COLLECTION = ROOT / "postman" / "eshop-hw06.postman_collection.json"


def main() -> None:
    if len(sys.argv) != 2 or sys.argv[1] not in ("true", "false"):
        sys.exit("Usage: python set_ci_fail_demo.py true|false")
    value = sys.argv[1]
    data = json.loads(COLLECTION.read_text(encoding="utf-8"))
    found = False
    for v in data.get("variable", []):
        if v.get("key") == "ciFailDemo":
            v["value"] = value
            found = True
            break
    if not found:
        data.setdefault("variable", []).append({"key": "ciFailDemo", "value": value})
    COLLECTION.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Set ciFailDemo={value} in {COLLECTION}")


if __name__ == "__main__":
    main()
