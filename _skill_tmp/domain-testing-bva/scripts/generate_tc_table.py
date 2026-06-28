#!/usr/bin/env python3
"""
generate_tc_table.py
--------------------
Scaffolds Domain Testing and BVA test case Markdown tables from a JSON
variable definition file.

Usage:
    python generate_tc_table.py variables.json FR01

Input JSON format (variables.json):
[
  {
    "id": 1,
    "name": "email",
    "type": "string",
    "required": true,
    "constraints": {
      "max_length": 254,
      "format": "RFC 5322"
    },
    "classes": [
      {"id": "EC-01", "desc": "Typical valid email", "type": "valid",   "value": "alice@example.com"},
      {"id": "EC-02", "desc": "Missing @ symbol",    "type": "invalid", "value": "aliceexample.com"},
      {"id": "EC-03", "desc": "Empty",               "type": "invalid", "value": ""}
    ],
    "boundaries": [
      {"name": "length", "min": 6, "max": 254, "unit": "char",
       "on_low": "a@b.co", "off_low": "a@b.c", "in_val": "alice@example.com",
       "on_high": "<254-char email>", "off_high": "<255-char email>",
       "out_low": "", "out_high": "<300-char email>"}
    ]
  }
]
"""

import json
import sys
from pathlib import Path


def generate_dt_table(variables: list, fr_id: str) -> str:
    lines = [f"# Domain Testing Test Cases — {fr_id}\n"]
    lines.append("| TC ID | Description | Preconditions | Input Data | Expected Result | Actual Result | Status |")
    lines.append("|-------|-------------|---------------|------------|-----------------|---------------|--------|")

    seq = 1
    for var in variables:
        for cls in var.get("classes", []):
            tc_id = f"TC-{fr_id}-DT-{seq:03d}"
            expected = "Account created / feature succeeds" if cls["type"] == "valid" \
                else f"Error: rejected ({cls['desc']})"
            value_display = repr(cls["value"]) if cls["value"] == "" else cls["value"]
            lines.append(
                f"| {tc_id} | {cls['desc']} | — | {var['name']}={value_display} | {expected} | | Not Executed |"
            )
            seq += 1

    return "\n".join(lines) + "\n"


def generate_bva_table(variables: list, fr_id: str) -> str:
    lines = [f"# BVA Test Cases — {fr_id}\n"]

    seq = 1
    for var in variables:
        for boundary in var.get("boundaries", []):
            lines.append(f"\n## Variable: `{var['name']}` — {boundary['name']} boundary\n")
            lines.append("| TC ID | BVA Point | Value | Expected Result | Actual Result | Status |")
            lines.append("|-------|-----------|-------|-----------------|---------------|--------|")

            points = [
                ("ON (lower)",  boundary.get("on_low"),   "Accepted"),
                ("OFF (lower)", boundary.get("off_low"),  "Rejected"),
                ("IN",          boundary.get("in_val"),   "Accepted"),
                ("ON (upper)",  boundary.get("on_high"),  "Accepted"),
                ("OFF (upper)", boundary.get("off_high"), "Rejected"),
                ("OUT (low)",   boundary.get("out_low"),  "Rejected"),
                ("OUT (high)",  boundary.get("out_high"), "Rejected"),
            ]

            for point_name, value, expected in points:
                if value is None:
                    continue
                tc_id = f"TC-{fr_id}-BVA-{seq:03d}"
                val_display = repr(value) if value == "" else value
                lines.append(f"| {tc_id} | {point_name} | {val_display} | {expected} | | Not Executed |")
                seq += 1

    return "\n".join(lines) + "\n"


def main():
    if len(sys.argv) < 3:
        print("Usage: python generate_tc_table.py <variables.json> <FR_ID>")
        print("Example: python generate_tc_table.py variables.json FR01")
        sys.exit(1)

    json_path = Path(sys.argv[1])
    fr_id = sys.argv[2].upper()

    if not json_path.exists():
        print(f"Error: {json_path} not found.")
        sys.exit(1)

    with open(json_path, "r", encoding="utf-8") as f:
        variables = json.load(f)

    dt_output = Path(f"test-cases-DT-{fr_id}.md")
    bva_output = Path(f"test-cases-BVA-{fr_id}.md")

    dt_output.write_text(generate_dt_table(variables, fr_id), encoding="utf-8")
    bva_output.write_text(generate_bva_table(variables, fr_id), encoding="utf-8")

    print(f"✅ Generated: {dt_output}")
    print(f"✅ Generated: {bva_output}")
    print("\nNext steps:")
    print("  1. Review the tables and fill in 'Preconditions' column")
    print("  2. Adjust 'Expected Result' based on actual SUT spec")
    print("  3. Execute tests and fill 'Actual Result' + 'Status'")


if __name__ == "__main__":
    main()
