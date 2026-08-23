#!/usr/bin/env python3
"""Append Stage 3 human-found SCH-SUP rows to schema-validation.csv (idempotent by TestCaseID)."""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHEET = ROOT / "sheets" / "schema-validation.csv"
TC_ROOT = ROOT / "tests" / "test-cases"

NO_HTTP = "HTTP status is not specified in api_specification.md — record actual without inventing codes."

ROWS = [
    {
        "TestCaseID": "TC-PROFILE-SCH-SUP-001",
        "module": "profile",
        "API": "GetProfile",
        "Method": "GET",
        "Endpoint": "/api/users/me",
        "fr": "FR-04",
        "aspect": "Undocumented DB columns on GET",
        "title": "GET profile exposes login_attempts / locked_until schema",
        "why": (
            "Why AI missed: Model limitation — AI checked documented FR-04 fields only; "
            "SUT uses SELECT * and may return lockout columns not listed in api_spec GET schema."
        ),
        "Preconditions": "EShop at http://localhost:3000. | POST /api/login email=test@eshop.com password=Test1234!.",
        "Input": json.dumps({"headers": {}}, ensure_ascii=False),
        "ExpectedResult": (
            "Record all top-level keys on GET /api/users/me. login_attempts (number) and locked_until "
            "(null or string) may appear — not in api_spec profile schema. FR-04 does not require them; "
            f"flag as schema over-exposure if present. {NO_HTTP}"
        ),
        "Priority": "Medium",
        "steps": ["GET /api/users/me.", "Inventory every key; note login_attempts and locked_until types if present."],
    },
    {
        "TestCaseID": "TC-PROFILE-SCH-SUP-002",
        "module": "profile",
        "API": "UpdateProfile",
        "Method": "PUT",
        "Endpoint": "/api/users/me",
        "fr": "FR-04",
        "aspect": "Nested request envelope",
        "title": "PUT with nested profile object — wrong request schema",
        "why": (
            "Why AI missed: Prompt quality — schema generator used flat objects matching api_spec example; "
            "nested envelope {profile:{...}} is a common client mistake never probed."
        ),
        "Preconditions": "EShop at http://localhost:3000. | POST /api/login email=test@eshop.com password=Test1234!. | Snapshot GET.",
        "Input": json.dumps(
            {"body": {"profile": {"name": "Nested Name", "phone": "0912345678", "shipping_address": "Addr"}}},
            ensure_ascii=False,
        ),
        "ExpectedResult": (
            "api_spec shows flat body keys. Server must reject or ignore nested envelope; "
            f"GET profile must not change to Nested Name unless flat parsing occurs. {NO_HTTP}"
        ),
        "Priority": "High",
        "steps": ["PUT nested body.", "GET /api/users/me — compare to snapshot."],
    },
    {
        "TestCaseID": "TC-PROFILE-SCH-SUP-003",
        "module": "profile",
        "API": "GetProfile",
        "Method": "GET",
        "Endpoint": "/api/users/me",
        "fr": "FR-04 / SEC-01",
        "aspect": "Full column dump vs minimum schema",
        "title": "Schema inventory — no password column on GET user object",
        "why": (
            "Why AI missed: API characteristic — SELECT * returns full row; AI SCH-007 checked password key "
            "but not whether other sensitive columns (e.g. password hash variants) appear under alternate names."
        ),
        "Preconditions": "EShop at http://localhost:3000. | POST /api/login email=test@eshop.com password=Test1234!.",
        "Input": json.dumps({"headers": {}}, ensure_ascii=False),
        "ExpectedResult": (
            "List all keys. Must not include password, password_hash, or hash. "
            "Document any unexpected sensitive-looking keys for SEC-01 follow-up."
        ),
        "Priority": "High",
        "steps": ["GET /api/users/me.", "Assert forbidden secret keys absent; log full key list."],
    },
    {
        "TestCaseID": "TC-PROFILE-SCH-SUP-004",
        "module": "profile",
        "API": "UpdateProfile",
        "Method": "PUT",
        "Endpoint": "/api/users/me",
        "fr": "FR-04",
        "aspect": "Array root request body",
        "title": "PUT body JSON array instead of object",
        "why": (
            "Why AI missed: Model limitation — SCH generator tested empty object and type coercion; "
            "array-root malformed JSON is a distinct parser/schema failure mode."
        ),
        "Preconditions": "EShop at http://localhost:3000. | POST /api/login email=test@eshop.com password=Test1234!.",
        "Input": json.dumps(
            {"body_raw": '[{"name":"Hack"}]', "headers": {"Content-Type": "application/json"}},
            ensure_ascii=False,
        ),
        "ExpectedResult": (
            f"Profile must not update from array body. Response JSON or parse error — record shape. {NO_HTTP}"
        ),
        "Priority": "Medium",
        "steps": ["PUT with raw JSON array body.", "GET profile unchanged or record actual."],
    },
    {
        "TestCaseID": "TC-PROFILE-SCH-SUP-005",
        "module": "profile",
        "API": "UpdateProfile",
        "Method": "PUT",
        "Endpoint": "/api/users/me",
        "fr": "FR-04",
        "aspect": "Charset Content-Type variant",
        "title": "PUT with Content-Type application/json; charset=utf-8",
        "why": (
            "Why AI missed: Prompt quality — SCH-010 checked response Content-Type on GET only; "
            "request charset variant on PUT not tested (RFC 7231 interoperability)."
        ),
        "Preconditions": "EShop at http://localhost:3000. | POST /api/login email=test@eshop.com password=Test1234!.",
        "Input": json.dumps(
            {
                "headers": {"Content-Type": "application/json; charset=utf-8"},
                "body": {"name": "Charset Name", "phone": "0912345678", "shipping_address": "Addr"},
            },
            ensure_ascii=False,
        ),
        "ExpectedResult": (
            "Valid UTF-8 JSON body should parse; GET name becomes Charset Name if update applies. "
            f"Record if charset suffix breaks parser. {NO_HTTP}"
        ),
        "Priority": "Low",
        "steps": ["PUT with charset Content-Type and valid body.", "GET /api/users/me."],
    },
    {
        "TestCaseID": "TC-CART-SCH-SUP-001",
        "module": "cart",
        "API": "AddToCart",
        "Method": "POST",
        "Endpoint": "/api/cart",
        "fr": "FR-07",
        "aspect": "Minimal partial POST body",
        "title": "POST {id, quantity} only — partial line schema",
        "why": (
            "Why AI missed: Prompt quality — domain SUP-004 added minimal body functionally; "
            "schema pass required all four example fields and never tested stored line shape after partial POST."
        ),
        "Preconditions": "EShop at http://localhost:3000. | POST /api/login email=test@eshop.com password=Test1234!.",
        "Input": json.dumps({"body": {"id": 1, "quantity": 1}}, ensure_ascii=False),
        "ExpectedResult": (
            "GET /api/cart line may lack name/price keys — record which keys exist and types. "
            "Spec example shows four fields; partial storage is schema deviation. " + NO_HTTP
        ),
        "Priority": "High",
        "steps": ["POST {id:1, quantity:1}.", "GET /api/cart — schema-check first line keys."],
    },
    {
        "TestCaseID": "TC-CART-SCH-SUP-002",
        "module": "cart",
        "API": "AddToCart",
        "Method": "POST",
        "Endpoint": "/api/cart",
        "fr": "FR-07",
        "aspect": "Extra client keys persisted",
        "title": "POST line with extra user_id key — stored schema pollution",
        "why": (
            "Why AI missed: API characteristic — SUT pushes req.body verbatim; "
            "AI schema cases asserted four canonical keys but not extra properties persistence."
        ),
        "Preconditions": "EShop at http://localhost:3000. | POST /api/login email=test@eshop.com password=Test1234!.",
        "Input": json.dumps(
            {"body": {"id": 1, "name": "Phone", "price": 100000, "quantity": 1, "user_id": 999, "role": "admin"}},
            ensure_ascii=False,
        ),
        "ExpectedResult": (
            "Record whether GET line includes user_id/role keys (additionalProperties). "
            "Canonical four fields should still have correct types if present."
        ),
        "Priority": "High",
        "steps": ["POST with extra keys.", "GET /api/cart — inspect line object keys."],
    },
    {
        "TestCaseID": "TC-CART-SCH-SUP-003",
        "module": "cart",
        "API": "GetCart",
        "Method": "GET",
        "Endpoint": "/api/cart",
        "fr": "FR-07",
        "aspect": "Homogeneous line schema",
        "title": "Multi-line cart — each element same key set",
        "why": (
            "Why AI missed: Model limitation — AI validated types per line in isolation (SCH-004..006); "
            "heterogeneous keys across lines after different POST shapes not compared."
        ),
        "Preconditions": (
            "EShop at http://localhost:3000. | POST /api/login email=test@eshop.com password=Test1234!. | "
            "POST full line id=1; POST minimal {id:2, quantity:1}."
        ),
        "Input": json.dumps({"sequence": ["POST full line", "POST minimal id=2", "GET /api/cart"]}, ensure_ascii=False),
        "ExpectedResult": (
            "Array length 2 (or 1 if merge on id — record). Compare key sets of line[0] vs line[1]; "
            "document schema inconsistency if one line lacks name/price."
        ),
        "Priority": "Medium",
        "steps": ["POST two different body shapes.", "GET — diff keys per array element."],
    },
    {
        "TestCaseID": "TC-CART-SCH-SUP-004",
        "module": "cart",
        "API": "AddToCart",
        "Method": "POST",
        "Endpoint": "/api/cart",
        "fr": "FR-07",
        "aspect": "Null field values",
        "title": "POST with name:null — nullable string schema",
        "why": (
            "Why AI missed: Prompt quality — schema tests used valid strings; null literal for optional-looking "
            "name field (not stated required in spec) never tested."
        ),
        "Preconditions": "EShop at http://localhost:3000. | POST /api/login email=test@eshop.com password=Test1234!.",
        "Input": json.dumps(
            {"body": {"id": 1, "name": None, "price": 100000, "quantity": 1}},
            ensure_ascii=False,
        ),
        "ExpectedResult": (
            "Record whether GET stores null, omits name, or rejects. typeof name on GET if present. " + NO_HTTP
        ),
        "Priority": "Medium",
        "steps": ["POST with name:null.", "GET /api/cart."],
    },
    {
        "TestCaseID": "TC-CART-SCH-SUP-005",
        "module": "cart",
        "API": "AddToCart",
        "Method": "POST",
        "Endpoint": "/api/cart",
        "fr": "FR-07",
        "aspect": "Duplicate JSON keys in POST",
        "title": "Duplicate quantity keys — last-wins schema parse",
        "why": (
            "Why AI missed: Model limitation — domain SUP-003 covered duplicate keys for profile phone; "
            "cart POST duplicate quantity not mirrored in schema category."
        ),
        "Preconditions": "EShop at http://localhost:3000. | POST /api/login email=test@eshop.com password=Test1234!.",
        "Input": json.dumps(
            {"body_raw": '{"id":1,"name":"Dup","price":100000,"quantity":1,"quantity":5}'},
            ensure_ascii=False,
        ),
        "ExpectedResult": (
            "GET line quantity reflects parser last-wins (5) or first-wins (1) — record. id/name/price types unchanged."
        ),
        "Priority": "Medium",
        "steps": ["POST raw JSON with duplicate quantity key.", "GET /api/cart."],
    },
    {
        "TestCaseID": "TC-ADMINUSERS-SCH-SUP-001",
        "module": "admin-users",
        "API": "AdminListUsers",
        "Method": "GET",
        "Endpoint": "/api/admin/users",
        "fr": "FR-19",
        "aspect": "Undocumented list columns",
        "title": "Admin list exposes shipping_address / login_attempts",
        "why": (
            "Why AI missed: API characteristic — SUT SELECT lists extra columns; "
            "AI FR-19 schema assumed id/name/email/role only."
        ),
        "Preconditions": "EShop at http://localhost:3000. | POST /api/login email=admin@eshop.com password=Admin123!.",
        "Input": json.dumps({"headers": {}}, ensure_ascii=False),
        "ExpectedResult": (
            "Record presence/types of shipping_address, login_attempts, locked_until on list items. "
            "FR-19 documents list without password — extra PII columns are schema finding."
        ),
        "Priority": "Medium",
        "steps": ["GET /api/admin/users.", "Inventory keys on first user object."],
    },
    {
        "TestCaseID": "TC-ADMINUSERS-SCH-SUP-002",
        "module": "admin-users",
        "API": "AdminListUsers",
        "Method": "GET",
        "Endpoint": "/api/admin/users",
        "fr": "FR-19",
        "aspect": "Homogeneous list element schema",
        "title": "All list users share identical key set",
        "why": (
            "Why AI missed: Prompt quality — SCH-002 checked each element is object; "
            "key-set equality across seed admin vs test user rows not asserted."
        ),
        "Preconditions": "EShop at http://localhost:3000. | POST /api/login email=admin@eshop.com password=Admin123!.",
        "Input": json.dumps({"headers": {}}, ensure_ascii=False),
        "ExpectedResult": (
            "Every user object in array has the same keys (order may differ). "
            "Report any row missing email or role compared to others."
        ),
        "Priority": "High",
        "steps": ["GET list.", "Compare Object.keys() for admin@eshop.com vs test@eshop.com entries."],
    },
    {
        "TestCaseID": "TC-ADMINUSERS-SCH-SUP-003",
        "module": "admin-users",
        "API": "AdminDeleteUser",
        "Method": "DELETE",
        "Endpoint": "/api/admin/users/:id",
        "fr": "FR-19",
        "aspect": "DELETE non-numeric path schema",
        "title": "DELETE path id=abc — error JSON shape",
        "why": (
            "Why AI missed: Model limitation — schema DELETE cases assumed valid numeric delete; "
            "malformed path error envelope type (object vs string vs HTML) not catalogued."
        ),
        "Preconditions": "EShop at http://localhost:3000. | POST /api/login email=admin@eshop.com password=Admin123!.",
        "Input": json.dumps({"path": {"id": "abc"}}, ensure_ascii=False),
        "ExpectedResult": (
            f"Response body type is JSON object or parseable JSON — not HTML. Record keys if object. {NO_HTTP}"
        ),
        "Priority": "Medium",
        "steps": ["DELETE /api/admin/users/abc.", "Record response Content-Type and JSON root type."],
    },
    {
        "TestCaseID": "TC-ADMINUSERS-SCH-SUP-004",
        "module": "admin-users",
        "API": "AdminListUsers",
        "Method": "GET",
        "Endpoint": "/api/admin/users",
        "fr": "FR-19 / SEC-01",
        "aspect": "Empty string email edge",
        "title": "Registered user with normal schema after disposable add",
        "why": (
            "Why AI missed: Prompt quality — SCH-011 checked seed users exist; "
            "schema validation immediately after register+list (new row shape) not isolated."
        ),
        "Preconditions": (
            "EShop at http://localhost:3000. | Admin JWT. | Register user schema-test@example.com."
        ),
        "Input": json.dumps({"sequence": ["GET list", "find new user by email"]}, ensure_ascii=False),
        "ExpectedResult": (
            "New list entry is object with number id, string name, string email, string role. "
            "No password fields."
        ),
        "Priority": "High",
        "steps": ["Register disposable user.", "GET /api/admin/users.", "Schema-check new row only."],
    },
    {
        "TestCaseID": "TC-ADMINUSERS-SCH-SUP-005",
        "module": "admin-users",
        "API": "AdminDeleteUser",
        "Method": "DELETE",
        "Endpoint": "/api/admin/users/:id",
        "fr": "FR-19",
        "aspect": "DELETE response must not echo full user row",
        "title": "DELETE success body minimal schema — no full user object leak",
        "why": (
            "Why AI missed: API characteristic — SCH-009/010 checked JSON object and message string; "
            "did not forbid echoing deleted user record with PII in DELETE body."
        ),
        "Preconditions": "EShop at http://localhost:3000. | Admin JWT. | Register disposable D.",
        "Input": json.dumps({"path": {"id": "<D>"}}, ensure_ascii=False),
        "ExpectedResult": (
            "DELETE response must not contain full user object with email/password. "
            "If only {message:string} — pass. Record actual keys. SEC-01 applies."
        ),
        "Priority": "High",
        "steps": ["DELETE disposable D.", "Inspect response keys — no email/password echo of deleted user."],
    },
]


def md_body(row: dict) -> str:
    td = json.dumps(json.loads(row["Input"]), ensure_ascii=False, indent=2)
    steps_md = "\n".join(f"{i}. {s}" for i, s in enumerate(row["steps"], 1))
    return f"""# {row['TestCaseID']}: {row['title']}

## Requirement ID
{row['fr']}

## Module / Test type / Technique
{row['module']} / Schema validation / Human extension (SCH-SUP)

## Schema aspect
{row['aspect']}

## Preconditions
{chr(10).join('- ' + p.strip() for p in row['Preconditions'].split('|'))}

## Test data
```json
{td}
```

## Test steps
{steps_md}

## Expected result
{row['ExpectedResult']}

## Why the AI missed this
{row['why'].replace('Why AI missed: ', '')}

## Status / Related bugs
Not Run / None
"""


def main() -> None:
    existing: set[str] = set()
    if SHEET.exists():
        with SHEET.open(encoding="utf-8", newline="") as f:
            existing = {r["TestCaseID"] for r in csv.DictReader(f)}

    to_add = [r for r in ROWS if r["TestCaseID"] not in existing]
    for row in ROWS:
        path = TC_ROOT / row["module"] / f"{row['TestCaseID']}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(md_body(row), encoding="utf-8")

    if not to_add:
        print(f"No new CSV rows; refreshed {len(ROWS)} SCH-SUP markdown files.")
        return

    fieldnames = [
        "TestCaseID", "API", "Method", "Endpoint", "Category", "Preconditions", "Input",
        "ExpectedResult", "Priority", "Source", "AuditStatus", "AuditReasoning",
        "ActualResult", "PassFail", "BugRef", "Notes",
    ]
    rows_out: list[dict] = []
    if SHEET.exists():
        with SHEET.open(encoding="utf-8", newline="") as f:
            rows_out = list(csv.DictReader(f))

    for row in to_add:
        rows_out.append(
            {
                "TestCaseID": row["TestCaseID"],
                "API": row["API"],
                "Method": row["Method"],
                "Endpoint": row["Endpoint"],
                "Category": "SchemaValidation",
                "Preconditions": row["Preconditions"],
                "Input": row["Input"],
                "ExpectedResult": row["ExpectedResult"],
                "Priority": row["Priority"],
                "Source": "Human",
                "AuditStatus": "N/A",
                "AuditReasoning": row["why"],
                "ActualResult": "",
                "PassFail": "",
                "BugRef": "",
                "Notes": f"Aspect={row['aspect']} | File=tests/test-cases/{row['module']}/{row['TestCaseID']}.md",
            }
        )

    with SHEET.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows_out)

    print(f"Appended {len(to_add)} rows (total {len(rows_out)})")


if __name__ == "__main__":
    main()
