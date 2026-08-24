#!/usr/bin/env python3
"""Append folder 99 — Data-driven Runner (CSV) without modifying existing TC folders."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COLLECTION = ROOT / "postman" / "eshop-hw06.postman_collection.json"
FOLDER_NAME = "99 — Data-driven Runner (CSV)"
STUDENT_ID = "23127271"

DATA_DRIVEN_FOLDER = {
    "name": FOLDER_NAME,
    "description": (
        "FR-04 phone partition probe via Postman Collection Runner / Newman data file.\n"
        f"Student: {STUDENT_ID}\n"
        "Data: postman/runner-data-profile-phone.csv (5 iterations)\n"
        "Columns: tc_id, test_phone, test_name, test_shipping_address, partition_note\n"
        "Observe-only — record status and GET /api/users/me phone after run; no invented HTTP codes."
    ),
    "item": [
        {
            "name": "1 — Login test user (per iteration)",
            "event": [
                {
                    "listen": "test",
                    "script": {
                        "type": "text/javascript",
                        "exec": [
                            "const tcId = pm.iterationData.get('tc_id') || 'DD-PHONE-UNK';",
                            "pm.test(`[${tcId}] login — response received`, function () {",
                            "    pm.expect(pm.response.code).to.be.within(100, 599);",
                            "});",
                            "if (pm.response.code === 200) {",
                            "    const body = pm.response.json();",
                            "    if (body.token) pm.collectionVariables.set('userToken', body.token);",
                            "}",
                            "console.log(`[${tcId}] login status=`, pm.response.code);",
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
            "name": "2 — PUT /api/users/me ({{test_phone}})",
            "event": [
                {
                    "listen": "prerequest",
                    "script": {
                        "type": "text/javascript",
                        "exec": [
                            "const tcId = pm.iterationData.get('tc_id') || 'DD-PHONE-UNK';",
                            "const phone = pm.iterationData.get('test_phone') || '';",
                            "const name = pm.iterationData.get('test_name') || 'Nguyen Van A';",
                            "const addr = pm.iterationData.get('test_shipping_address') || '123 Le Loi';",
                            "pm.variables.set('test_phone', phone);",
                            "pm.variables.set('test_name', name);",
                            "pm.variables.set('test_shipping_address', addr);",
                            "console.log(`[${tcId}] iteration phone=`, phone);",
                        ],
                    },
                },
                {
                    "listen": "test",
                    "script": {
                        "type": "text/javascript",
                        "exec": [
                            "const tcId = pm.iterationData.get('tc_id') || 'DD-PHONE-UNK';",
                            "const phone = pm.iterationData.get('test_phone') || '';",
                            "const note = pm.iterationData.get('partition_note') || '';",
                            "const step = 'data-driven-put';",
                            "",
                            "pm.test(`[${tcId}] ${step} — response received`, function () {",
                            "    pm.expect(pm.response.code).to.be.within(100, 599);",
                            "});",
                            "",
                            "pm.test(`[${tcId}] ${step} — JSON or empty body`, function () {",
                            "    const ct = pm.response.headers.get('Content-Type') || '';",
                            "    if (pm.response.text() && ct.includes('json')) {",
                            "        pm.response.to.be.json;",
                            "    }",
                            "});",
                            "",
                            "pm.test(`[${tcId}] ${step} — response time < 10s`, function () {",
                            "    pm.expect(pm.response.responseTime).to.be.below(10000);",
                            "});",
                            "",
                            "console.log(`[${tcId}] ${step} phone=${phone} status=`, pm.response.code);",
                            "console.log(`[${tcId}] partition:`, note);",
                            "console.log(`[${tcId}] oracle: record GET /api/users/me phone — FR-04 valid = 10-11 digits starting with 0`);",
                            "pm.collectionVariables.set('lastTcId', tcId);",
                            "pm.collectionVariables.set('lastStatus', String(pm.response.code));",
                        ],
                    },
                },
            ],
            "request": {
                "method": "PUT",
                "header": [
                    {"key": "Authorization", "value": "Bearer {{userToken}}", "type": "text"},
                    {"key": "Content-Type", "value": "application/json", "type": "text"},
                    {"key": "Accept", "value": "application/json", "type": "text"},
                ],
                "body": {
                    "mode": "raw",
                    "raw": (
                        "{\n"
                        '  "name": "{{test_name}}",\n'
                        '  "phone": "{{test_phone}}",\n'
                        '  "shipping_address": "{{test_shipping_address}}"\n'
                        "}"
                    ),
                    "options": {"raw": {"language": "json"}},
                },
                "url": "{{baseUrl}}/api/users/me",
                "description": (
                    "Data-driven PUT from CSV iteration. "
                    "Attach postman/runner-data-profile-phone.csv in Collection Runner."
                ),
            },
        },
    ],
}


def main() -> None:
    data = json.loads(COLLECTION.read_text(encoding="utf-8"))
    items = data.get("item", [])
    items = [it for it in items if it.get("name") != FOLDER_NAME]
    items.append(DATA_DRIVEN_FOLDER)
    data["item"] = items

    desc = data["info"].get("description", "")
    extra = (
        f"\nData-driven: folder \"{FOLDER_NAME}\" + "
        "postman/runner-data-profile-phone.csv (5 phone partitions)."
    )
    if extra.strip() not in desc:
        data["info"]["description"] = desc.rstrip() + extra

    COLLECTION.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tc_count = sum(
        1
        for fr in items
        if fr.get("name", "").startswith("FR-")
        for cat in fr.get("item", [])
        for tc in cat.get("item", [])
    )
    print(f"Updated {COLLECTION}")
    print(f"  Folder: {FOLDER_NAME} (2 requests × 5 CSV rows)")
    print(f"  Existing TC folders untouched: {tc_count}")


if __name__ == "__main__":
    main()
