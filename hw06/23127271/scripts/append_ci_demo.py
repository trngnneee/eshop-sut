#!/usr/bin/env python3
"""Append CI — HW06 pipeline demo folder + ciFailDemo collection variable."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COLLECTION = ROOT / "postman" / "eshop-hw06.postman_collection.json"
FOLDER_NAME = "CI — HW06 pipeline demo"
STUDENT_ID = "23127271"

CI_FOLDER = {
    "name": FOLDER_NAME,
    "description": (
        "GitHub Actions CI demo folder (2 requests).\n"
        f"Student: {STUDENT_ID}\n"
        "Collection variable ciFailDemo:\n"
        "  false / empty → all assertions pass (Run A)\n"
        "  true → exactly 1 failure on 'Fail demo — intentional' (Run B homework demo)\n"
        "Revert ciFailDemo after screenshot — homework fail demo only."
    ),
    "item": [
        {
            "name": "Pass — login 200",
            "event": [
                {
                    "listen": "test",
                    "script": {
                        "type": "text/javascript",
                        "exec": [
                            "pm.test('login 200', function () {",
                            "    pm.response.to.have.status(200);",
                            "});",
                            "const body = pm.response.json();",
                            "pm.expect(body).to.have.property('token');",
                            "console.log('[CI-PASS] login status=', pm.response.code);",
                        ],
                    },
                }
            ],
            "request": {
                "method": "POST",
                "header": [
                    {"key": "Content-Type", "value": "application/json", "type": "text"},
                    {"key": "Accept", "value": "application/json", "type": "text"},
                ],
                "body": {
                    "mode": "raw",
                    "raw": '{\n  "email": "test@eshop.com",\n  "password": "Test1234!"\n}',
                    "options": {"raw": {"language": "json"}},
                },
                "url": "{{baseUrl}}/api/login",
            },
        },
        {
            "name": "Fail demo — intentional",
            "event": [
                {
                    "listen": "test",
                    "script": {
                        "type": "text/javascript",
                        "exec": [
                            "// Revert ciFailDemo after screenshot — homework fail demo only",
                            "const failDemo = pm.collectionVariables.get('ciFailDemo');",
                            "if (failDemo === 'true') {",
                            "    pm.test('INTENTIONAL CI FAIL DEMO', function () {",
                            "        pm.response.to.have.status(404);",
                            "    });",
                            "} else {",
                            "    pm.test('login 200', function () {",
                            "        pm.response.to.have.status(200);",
                            "    });",
                            "}",
                            "console.log('[CI-DEMO] ciFailDemo=', failDemo, 'status=', pm.response.code);",
                        ],
                    },
                }
            ],
            "request": {
                "method": "POST",
                "header": [
                    {"key": "Content-Type", "value": "application/json", "type": "text"},
                    {"key": "Accept", "value": "application/json", "type": "text"},
                ],
                "body": {
                    "mode": "raw",
                    "raw": '{\n  "email": "test@eshop.com",\n  "password": "Test1234!"\n}',
                    "options": {"raw": {"language": "json"}},
                },
                "url": "{{baseUrl}}/api/login",
                "description": (
                    "Same login as Setup. When ciFailDemo=true, asserts 404 to produce "
                    "exactly one Newman failure for homework pipeline screenshot."
                ),
            },
        },
    ],
}


def main() -> None:
    collection_path = Path(sys.argv[1]) if len(sys.argv) > 1 else COLLECTION
    data = json.loads(collection_path.read_text(encoding="utf-8"))

    variables = data.get("variable", [])
    if not any(v.get("key") == "ciFailDemo" for v in variables):
        variables.append({"key": "ciFailDemo", "value": "false"})
    else:
        for v in variables:
            if v.get("key") == "ciFailDemo" and len(sys.argv) <= 2:
                pass  # preserve existing value on normal run
    data["variable"] = variables

    items = data.get("item", [])
    items = [it for it in items if it.get("name") != FOLDER_NAME]
    items.append(CI_FOLDER)
    data["item"] = items

    desc = data["info"].get("description", "")
    note = f'\nCI: folder "{FOLDER_NAME}" for GitHub Actions (ciFailDemo variable).'
    if note.strip() not in desc:
        data["info"]["description"] = desc.rstrip() + note

    collection_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tc_count = sum(
        1
        for fr in items
        if fr.get("name", "").startswith("FR-")
        for cat in fr.get("item", [])
        for tc in cat.get("item", [])
    )
    ci_fail = next((v["value"] for v in variables if v.get("key") == "ciFailDemo"), "?")
    print(f"Updated {collection_path}")
    print(f"  Folder: {FOLDER_NAME} (2 requests)")
    print(f"  ciFailDemo = {ci_fail!r}")
    print(f"  TC folders untouched: {tc_count}")


if __name__ == "__main__":
    main()
