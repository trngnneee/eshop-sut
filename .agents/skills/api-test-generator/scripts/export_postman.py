#!/usr/bin/env python3
"""
export_postman.py — test_cases.json -> Postman v2.1 collection.json

Builds a Postman collection with:
  - a collection-level pre-request script injecting X-Student-Id on every
    request (per the assignment's anti-cheat requirement)
  - {{baseUrl}} and {{studentId}} collection variables
  - one folder per stage, one request per test case
  - a basic test script per request asserting the expected status code and
    (when provided) that body_contains keys exist with the right JS typeof

Usage:
    python3 export_postman.py test_cases.json --out collection.json \
        --base-url "{{baseUrl}}" --student-id-header "{{studentId}}" \
        --collection-name "EShop API Test Suite"
"""
import argparse
import json
import uuid


def build_test_script(expected):
    lines = []
    status = expected.get("status")
    if status is not None:
        lines.append(f"pm.test('Status code is {status}', function () {{")
        lines.append(f"    pm.response.to.have.status({status});")
        lines.append("});")

    body_contains = expected.get("body_contains") or {}
    if body_contains:
        lines.append("pm.test('Response schema shape', function () {")
        lines.append("    const body = pm.response.json();")
        for key, jstype in body_contains.items():
            if jstype == "array":
                lines.append(f"    pm.expect(Array.isArray(body['{key}'])).to.be.true;")
            else:
                lines.append(f"    pm.expect(typeof body['{key}']).to.eql('{jstype}');")
        lines.append("});")

    return lines


def build_request_item(tc):
    req = tc.get("request", {})
    method = req.get("method", "GET").upper()
    path = req.get("path", "/")
    headers = [{"key": k, "value": str(v)} for k, v in (req.get("headers") or {}).items()]
    query = req.get("query") or {}
    body = req.get("body")

    url_query = [{"key": k, "value": str(v)} for k, v in query.items()]

    item = {
        "name": f"{tc.get('id', '')} - {tc.get('title', '')}".strip(" -"),
        "request": {
            "method": method,
            "header": headers,
            "url": {
                "raw": "{{baseUrl}}" + path + (("?" + "&".join(f"{q['key']}={q['value']}" for q in url_query)) if url_query else ""),
                "host": ["{{baseUrl}}"],
                "path": [p for p in path.strip("/").split("/") if p],
                "query": url_query,
            },
            "description": (
                f"Stage: {tc.get('stage')}\n"
                f"Category: {tc.get('category')}\n"
                f"FR ref: {tc.get('fr_ref')}  SEC ref: {tc.get('sec_ref')}\n"
                f"Preconditions: {tc.get('preconditions')}"
            ),
        },
        "response": [],
    }
    if body is not None:
        item["request"]["body"] = {
            "mode": "raw",
            "raw": json.dumps(body, indent=2, ensure_ascii=False),
            "options": {"raw": {"language": "json"}},
        }

    test_lines = build_test_script(tc.get("expected") or {})
    if test_lines:
        item["event"] = [
            {
                "listen": "test",
                "script": {"type": "text/javascript", "exec": test_lines},
            }
        ]
    return item


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("test_cases_json")
    ap.add_argument("--out", default="collection.json")
    ap.add_argument("--base-url", default="{{baseUrl}}")
    ap.add_argument("--student-id-header", default="{{studentId}}")
    ap.add_argument("--collection-name", default="API Test Suite")
    args = ap.parse_args()

    with open(args.test_cases_json, "r", encoding="utf-8") as f:
        cases = json.load(f)

    folders = {}
    for tc in cases:
        stage = tc.get("stage", "uncategorized")
        folders.setdefault(stage, []).append(build_request_item(tc))

    collection = {
        "info": {
            "_postman_id": str(uuid.uuid4()),
            "name": args.collection_name,
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
        },
        "event": [
            {
                "listen": "prerequest",
                "script": {
                    "type": "text/javascript",
                    "exec": [
                        "// Anti-cheat requirement: attach X-Student-Id to every request",
                        f"pm.request.headers.add({{ key: 'X-Student-Id', value: '{args.student_id_header}' }});",
                        "console.log('X-Student-Id header set to', pm.variables.get('studentId'));",
                    ],
                },
            }
        ],
        "variable": [
            {"key": "baseUrl", "value": args.base_url if args.base_url != "{{baseUrl}}" else "http://localhost:3000"},
            {"key": "studentId", "value": "REPLACE_WITH_STUDENT_ID"},
        ],
        "item": [
            {"name": stage, "item": items} for stage, items in folders.items()
        ],
    }

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(collection, f, indent=2, ensure_ascii=False)

    total = sum(len(v) for v in folders.values())
    print(f"Wrote {args.out} ({total} requests across {len(folders)} folders)")
    print("Remember to set the 'studentId' collection/environment variable before running with Newman.")


if __name__ == "__main__":
    main()
