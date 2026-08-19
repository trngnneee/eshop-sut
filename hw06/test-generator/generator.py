#!/usr/bin/env python3
"""Small, deterministic endpoint-to-test-case generator used by HW06."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def generate(spec: dict) -> tuple[list[dict], dict]:
    prefix = spec.get("id_prefix", "TC-API")
    cases = []
    counter = 1
    for parameter in spec.get("parameters", []):
        name = parameter["name"]
        values = parameter.get("examples", ["valid", None, "boundary"])
        for value in values:
            cases.append({"id": f"{prefix}-{counter:03d}", "group": "Partition", "technique": "EP/BVA", "title": f"{name} partition: {value}", "precondition": "seed state", "data": {name: value}, "expected": parameter.get("expected", "controlled response"), "requirement": parameter.get("requirement", "—"), "source": "generated"})
            counter += 1
    for state in spec.get("states", []):
        cases.append({"id": f"{prefix}-{counter:03d}", "group": "State", "technique": "transition", "title": state["title"], "precondition": state.get("from", "state setup"), "data": state.get("data", {}), "expected": state.get("expected", "state-specific response"), "requirement": state.get("requirement", "—"), "source": "generated"})
        counter += 1
    for security in spec.get("security", []):
        cases.append({"id": f"{prefix}-{counter:03d}", "group": "Security", "technique": security.get("technique", "negative"), "title": security["title"], "precondition": security.get("precondition", "controlled auth state"), "data": security.get("data", {}), "expected": security.get("expected", "reject safely"), "requirement": security.get("requirement", "SEC"), "source": "generated"})
        counter += 1
    for field in spec.get("response_schema", []):
        cases.append({"id": f"{prefix}-{counter:03d}", "group": "Schema", "technique": "schema", "title": f"response field {field['name']}", "precondition": "valid request", "data": {}, "expected": field.get("expected", f"{field['name']} has type {field.get('type', 'contract') }"), "requirement": field.get("requirement", "schema"), "source": "generated"})
        counter += 1
    return cases, {"count": len(cases), "duplicate_ids": len(cases) - len({case["id"] for case in cases}), "missing_expected": [case["id"] for case in cases if not case["expected"]]}


def render(cases: list[dict], audit: dict, out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    fields = ["id", "group", "technique", "title", "precondition", "data", "expected", "requirement", "source"]
    lines = [f"# Generated test cases — {len(cases)}", "", f"> Audit hook: `{audit}`", "", "| " + " | ".join(fields) + " |", "| " + " | ".join(":---" for _ in fields) + " |"]
    for case in cases:
        lines.append("| " + " | ".join(str(case[field]).replace("|", "\\|") for field in fields) + " |")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")

    collection = {"info": {"name": "Generated API skeleton", "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"}, "item": [{"name": case["id"] + " - " + case["title"], "request": {"method": "POST", "url": "{{base_url}}"}} for case in cases]}
    out.with_suffix(".postman.json").write_text(json.dumps(collection, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("endpoint", type=Path)
    parser.add_argument("--out", type=Path, default=Path("generated-test-cases.md"))
    args = parser.parse_args()
    cases, audit = generate(json.loads(args.endpoint.read_text(encoding="utf-8")))
    render(cases, audit, args.out)
    print(json.dumps({"cases": len(cases), "audit": audit}, ensure_ascii=False))


if __name__ == "__main__":
    main()
