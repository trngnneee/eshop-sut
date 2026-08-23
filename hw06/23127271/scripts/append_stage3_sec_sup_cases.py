#!/usr/bin/env python3
"""Append Stage 3 human-found SEC-SUP rows to security-tests.csv (idempotent by TestCaseID)."""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHEET = ROOT / "sheets" / "security-tests.csv"
TC_ROOT = ROOT / "tests" / "test-cases"

NO_HTTP = "HTTP status and error body are not specified — record actual without inventing codes."

ROWS = [
    {
        "TestCaseID": "TC-PROFILE-SEC-SUP-001",
        "module": "profile",
        "API": "UpdateProfile",
        "Method": "PUT",
        "Endpoint": "/api/users/me",
        "fr": "FR-04 / SEC-06",
        "sec": "SEC-06",
        "threat": "Race — concurrent PUT with role=admin vs valid profile",
        "type": "Unspecified (concurrency)",
        "why": (
            "Why AI missed: Prompt quality — security generator emitted one-shot SEC-06 probes (TC-PROFILE-SEC-007); "
            "checklist section 2 concurrency/race was never requested, so parallel privilege-escalation PUTs were absent."
        ),
        "Preconditions": (
            "EShop at http://localhost:3000. | POST /api/login email=test@eshop.com password=Test1234!. | "
            "GET /api/users/me snapshot role=user."
        ),
        "Input": json.dumps(
            {
                "sequence": [
                    'PUT {"name":"Valid Name","phone":"0912345678","shipping_address":"123 Le Loi","role":"admin"}',
                    'PUT {"name":"Race Name B","phone":"0912345678","shipping_address":"123 Le Loi"} — fire immediately parallel',
                    "GET /api/users/me",
                ]
            },
            ensure_ascii=False,
        ),
        "ExpectedResult": (
            "SEC-06: role must remain user regardless of ordering. GET shows one coherent profile; "
            "role must not become admin. Record which PUT wins for name. " + NO_HTTP
        ),
        "Priority": "High",
    },
    {
        "TestCaseID": "TC-PROFILE-SEC-SUP-002",
        "module": "profile",
        "API": "UpdateProfile",
        "Method": "PUT",
        "Endpoint": "/api/users/me",
        "fr": "FR-04 / SEC-06",
        "sec": "SEC-06",
        "threat": "Mass assignment — numeric id field in PUT body",
        "type": "Illegal / mass assignment",
        "why": (
            "Why AI missed: Model limitation — AI mapped SEC-06 to role/password/email/login_attempts only; "
            "primary-key id swap in profile body is a classic mass-assignment vector not listed in spec example JSON."
        ),
        "Preconditions": (
            "EShop at http://localhost:3000. | POST /api/login email=test@eshop.com password=Test1234!. | "
            "Note seed admin id=1, test user id=2."
        ),
        "Input": json.dumps(
            {
                "body": {
                    "name": "Nguyen Van A",
                    "phone": "0912345678",
                    "shipping_address": "123 Le Loi",
                    "id": 1,
                }
            },
            ensure_ascii=False,
        ),
        "ExpectedResult": (
            "SEC-06 / FR-04: client must not rebind profile to another user id. "
            "GET /api/users/me still shows test@eshop.com and original id; must not become admin id=1. " + NO_HTTP
        ),
        "Priority": "High",
        "steps": [
            'PUT /api/users/me with body including "id":1 plus FR-04-valid fields.',
            "GET /api/users/me.",
        ],
    },
    {
        "TestCaseID": "TC-PROFILE-SEC-SUP-003",
        "module": "profile",
        "API": "UpdateProfile",
        "Method": "PUT",
        "Endpoint": "/api/users/me",
        "fr": "FR-04 / SEC-05",
        "sec": "SEC-05",
        "threat": "Null-byte encoding in name field",
        "type": "Encoding / injection probe",
        "why": (
            "Why AI missed: Model limitation — SQLi/XSS probes used printable ASCII quotes; "
            "null-byte and encoding-truncation attacks on SQLite/string handling are absent from LLM default payloads."
        ),
        "Preconditions": f"EShop at http://localhost:3000. | POST /api/login email=test@eshop.com password=Test1234!.",
        "Input": json.dumps(
            {
                "body": {
                    "name": "Nguyen\u0000admin",
                    "phone": "0912345678",
                    "shipping_address": "123 Le Loi",
                }
            },
            ensure_ascii=False,
        ),
        "ExpectedResult": (
            "SEC-05: null byte must not truncate stored name or cause SQL/500 leak. "
            "GET /api/users/me shows literal storage or rejection; email/role unchanged. " + NO_HTTP
        ),
        "Priority": "High",
        "steps": [
            "PUT /api/users/me with null byte in name field.",
            "GET /api/users/me.",
        ],
    },
    {
        "TestCaseID": "TC-PROFILE-SEC-SUP-004",
        "module": "profile",
        "API": "UpdateProfile",
        "Method": "PUT",
        "Endpoint": "/api/users/me",
        "fr": "FR-04 / SEC-02",
        "sec": "SEC-02",
        "threat": "Content-Type text/plain with JSON body",
        "type": "Header / parser confusion",
        "why": (
            "Why AI missed: Prompt quality — SEC-02 cases targeted missing/invalid Authorization only; "
            "Content-Type confusion (valid JWT + wrong media type) is a common bypass class not in the SEC checklist prompt."
        ),
        "Preconditions": (
            "EShop at http://localhost:3000. | POST /api/login email=test@eshop.com password=Test1234!. | "
            "Snapshot GET /api/users/me."
        ),
        "Input": json.dumps(
            {
                "headers": {
                    "Authorization": "Bearer <valid_user_token>",
                    "Content-Type": "text/plain",
                },
                "body_raw": '{"name":"Hacked Via Plain","phone":"0912345678","shipping_address":"X"}',
            },
            ensure_ascii=False,
        ),
        "ExpectedResult": (
            "SEC-02: profile must not change if body is ignored or parsed unsafely. "
            "GET /api/users/me matches snapshot unless spec allows plain-text profile updates (it does not). " + NO_HTTP
        ),
        "Priority": "Medium",
        "steps": [
            "PUT /api/users/me with valid JWT and Content-Type: text/plain; body is JSON string.",
            "GET /api/users/me with valid token.",
        ],
    },
    {
        "TestCaseID": "TC-PROFILE-SEC-SUP-005",
        "module": "profile",
        "API": "UpdateProfile",
        "Method": "PUT",
        "Endpoint": "/api/users/me",
        "fr": "FR-04 / SEC-04 / SEC-05",
        "sec": "SEC-04",
        "threat": "Race — concurrent XSS vs SQLi PUT on same field",
        "type": "Unspecified (concurrency)",
        "why": (
            "Why AI missed: API characteristic — in-memory/SQLite profile may last-write-win under race; "
            "AI never combined SEC-04 and SEC-05 payloads in parallel PUTs to detect torn or mixed malicious storage."
        ),
        "Preconditions": f"EShop at http://localhost:3000. | POST /api/login email=test@eshop.com password=Test1234!.",
        "Input": json.dumps(
            {
                "sequence": [
                    'PUT name=<script>alert(1)</script> (other fields FR-04-valid)',
                    "PUT name=Nguyen' OR '1'='1 (parallel, no GET between)",
                    "GET /api/users/me",
                ]
            },
            ensure_ascii=False,
        ),
        "ExpectedResult": (
            "GET must return exactly one stored name value (XSS literal or SQLi literal), not concatenated/corrupt. "
            "SEC-04/SEC-05: no server execution/SQL leak. email/role unchanged. Record winner. " + NO_HTTP
        ),
        "Priority": "High",
    },
    {
        "TestCaseID": "TC-CART-SEC-SUP-001",
        "module": "cart",
        "API": "AddToCart",
        "Method": "POST",
        "Endpoint": "/api/cart",
        "fr": "FR-07 / SEC-06",
        "sec": "SEC-06",
        "threat": "Race — parallel POST same id with price=1 vs catalogue price",
        "type": "Unspecified (concurrency)",
        "why": (
            "Why AI missed: Prompt quality — TC-CART-SEC-006 tested price tampering sequentially; "
            "parallel client price writes are the realistic attack for in-memory cart without locking."
        ),
        "Preconditions": (
            "EShop at http://localhost:3000. | POST /api/login email=test@eshop.com password=Test1234!. | "
            "GET /api/cart empty."
        ),
        "Input": json.dumps(
            {
                "sequence": [
                    "POST id=1 name=iPhone price=1 qty=1",
                    "POST id=1 name=iPhone price=30000000 qty=1 — parallel",
                    "GET /api/cart",
                ]
            },
            ensure_ascii=False,
        ),
        "ExpectedResult": (
            "FR-07/SEC-06: cart must not persist attacker price=1 if catalogue price is authoritative. "
            "At most one line id=1; record stored price and qty (expect qty=2 if merge). " + NO_HTTP
        ),
        "Priority": "High",
    },
    {
        "TestCaseID": "TC-CART-SEC-SUP-002",
        "module": "cart",
        "API": "AddToCart",
        "Method": "POST",
        "Endpoint": "/api/cart",
        "fr": "FR-07 / SEC-06",
        "sec": "SEC-06",
        "threat": "Negative quantity integrity probe",
        "type": "Illegal / integrity",
        "why": (
            "Why AI missed: Model limitation — AI focused on auth/SQLi/XSS/price tampering; "
            "negative qty is an integrity edge (refund/credit exploit) not visible in spec example body."
        ),
        "Preconditions": f"EShop at http://localhost:3000. | POST /api/login email=test@eshop.com password=Test1234!.",
        "Input": json.dumps(
            {"body": {"id": 1, "name": "iPhone", "price": 30000000, "quantity": -1}},
            ensure_ascii=False,
        ),
        "ExpectedResult": (
            "Cart must not store negative qty or reduce totals below zero. "
            "GET /api/cart shows rejection or qty clamped >=1; no corrupt line count. " + NO_HTTP
        ),
        "Priority": "High",
        "steps": [
            "POST /api/cart with quantity=-1.",
            "GET /api/cart.",
        ],
    },
    {
        "TestCaseID": "TC-CART-SEC-SUP-003",
        "module": "cart",
        "API": "AddToCart",
        "Method": "POST",
        "Endpoint": "/api/cart",
        "fr": "FR-07 / SEC-02",
        "sec": "SEC-02",
        "threat": "Race — GET /api/cart concurrent with POST add",
        "type": "Unspecified (concurrency)",
        "why": (
            "Why AI missed: API characteristic — TC-CART-SEC-007 tested sequential cross-user IDOR; "
            "same-user GET during POST may expose partial cart state or stale JWT-scoped snapshot under race."
        ),
        "Preconditions": (
            "EShop at http://localhost:3000. | POST /api/login email=test@eshop.com password=Test1234!. | "
            "Cart empty."
        ),
        "Input": json.dumps(
            {
                "sequence": [
                    "Fire POST /api/cart id=1 qty=5 and GET /api/cart in parallel",
                    "GET /api/cart after both complete",
                ]
            },
            ensure_ascii=False,
        ),
        "ExpectedResult": (
            "Final GET must show id=1 qty=5 (or merged total). Concurrent GET may show empty or partial — record. "
            "Must not leak another user's lines. No duplicate corrupt rows. " + NO_HTTP
        ),
        "Priority": "Medium",
    },
    {
        "TestCaseID": "TC-CART-SEC-SUP-004",
        "module": "cart",
        "API": "AddToCart",
        "Method": "POST",
        "Endpoint": "/api/cart",
        "fr": "FR-07 / SEC-04",
        "sec": "SEC-04",
        "threat": "Unicode-escaped XSS bypass in cart name",
        "type": "Encoding / XSS bypass",
        "why": (
            "Why AI missed: Model limitation — TC-CART-SEC-005 used literal <script> tags; "
            "Unicode escape and normalization bypasses for SEC-04 are a known gap when prompts say 'XSS' generically."
        ),
        "Preconditions": f"EShop at http://localhost:3000. | POST /api/login email=test@eshop.com password=Test1234!.",
        "Input": json.dumps(
            {
                "body": {
                    "id": 1,
                    "name": "\\u003cscript\\u003ealert(1)\\u003c/script\\u003e",
                    "price": 30000000,
                    "quantity": 1,
                }
            },
            ensure_ascii=False,
        ),
        "ExpectedResult": (
            "SEC-04: API must store/return literal escaped or decoded text without server-side execution. "
            "GET /api/cart JSON inspected for normalization to executable HTML — note for manual UI follow-up. " + NO_HTTP
        ),
        "Priority": "High",
        "steps": [
            "POST /api/cart with Unicode-escaped script in name.",
            "GET /api/cart — inspect JSON literal.",
        ],
    },
    {
        "TestCaseID": "TC-CART-SEC-SUP-005",
        "module": "cart",
        "API": "AddToCart",
        "Method": "POST",
        "Endpoint": "/api/cart",
        "fr": "FR-07 / SEC-06",
        "sec": "SEC-06",
        "threat": "Extreme quantity integer overflow probe",
        "type": "Boundary / integrity",
        "why": (
            "Why AI missed: Prompt quality — domain partitions covered qty boundaries for FR-07 functionally; "
            "security pass did not reuse INT_MAX-scale qty as integrity/DoS probe against cart total."
        ),
        "Preconditions": f"EShop at http://localhost:3000. | POST /api/login email=test@eshop.com password=Test1234!.",
        "Input": json.dumps(
            {
                "body": {
                    "id": 1,
                    "name": "iPhone",
                    "price": 30000000,
                    "quantity": 999999999,
                }
            },
            ensure_ascii=False,
        ),
        "ExpectedResult": (
            "Cart must reject or clamp extreme qty; must not wrap negative or corrupt price*qty math. "
            "GET /api/cart records actual qty stored. " + NO_HTTP
        ),
        "Priority": "Medium",
        "steps": [
            "POST /api/cart id=1 quantity=999999999.",
            "GET /api/cart.",
        ],
    },
    {
        "TestCaseID": "TC-ADMINUSERS-SEC-SUP-001",
        "module": "admin-users",
        "API": "AdminListUsers",
        "Method": "GET",
        "Endpoint": "/api/admin/users",
        "fr": "FR-19 / SEC-02",
        "sec": "SEC-02",
        "threat": "Auth bypass — GET admin list without JWT",
        "type": "Illegal / auth bypass",
        "why": (
            "Why AI missed: Prompt quality — SEC-02 probes targeted DELETE /api/admin/users/:id (SEC-001/010); "
            "GET list is part of FR-19 but never tested unauthenticated, leaving list exposure untested."
        ),
        "Preconditions": f"EShop at http://localhost:3000. | Disposable users exist in system.",
        "Input": json.dumps({"headers": {}}, ensure_ascii=False),
        "ExpectedResult": (
            "SEC-02: unauthenticated GET must not return user roster or password fields. "
            "Record status/body; must not expose PII list. " + NO_HTTP
        ),
        "Priority": "High",
        "steps": [
            "GET /api/admin/users without Authorization header.",
            "Inspect response for user list and password fields.",
        ],
    },
    {
        "TestCaseID": "TC-ADMINUSERS-SEC-SUP-002",
        "module": "admin-users",
        "API": "AdminListUsers",
        "Method": "GET",
        "Endpoint": "/api/admin/users",
        "fr": "FR-19 / SEC-03",
        "sec": "SEC-03",
        "threat": "Role escalation — user JWT on GET admin list",
        "type": "Illegal / privilege",
        "why": (
            "Why AI missed: Model limitation — AI mapped SEC-03 only to DELETE admin routes (SEC-002/003); "
            "spec section 6.1 pairs GET list with DELETE under same admin guard — list endpoint SEC-03 gap."
        ),
        "Preconditions": (
            "EShop at http://localhost:3000. | POST /api/login email=test@eshop.com password=Test1234!."
        ),
        "Input": json.dumps({"headers": {"Authorization": "Bearer <user_token>"}}, ensure_ascii=False),
        "ExpectedResult": (
            "SEC-03 / FR-12: user JWT must not retrieve full user list. "
            "No password/hash in body if any data returned. " + NO_HTTP
        ),
        "Priority": "High",
        "steps": [
            "GET /api/admin/users with test user JWT (role=user).",
            "Inspect response — must not return full admin roster.",
        ],
    },
    {
        "TestCaseID": "TC-ADMINUSERS-SEC-SUP-003",
        "module": "admin-users",
        "API": "AdminDeleteUser",
        "Method": "DELETE",
        "Endpoint": "/api/admin/users/:id",
        "fr": "FR-19 / SEC-02",
        "sec": "SEC-02",
        "threat": "Race — parallel DELETE on same disposable user",
        "type": "Unspecified (concurrency)",
        "why": (
            "Why AI missed: Prompt quality — checklist concurrency item omitted from security generator; "
            "AI emitted sequential delete probes only (SEC-001/013), not double-delete idempotency side effects."
        ),
        "Preconditions": (
            "EShop at http://localhost:3000. | POST /api/login email=admin@eshop.com password=Admin123!. | "
            "Disposable D registered."
        ),
        "Input": json.dumps(
            {
                "sequence": [
                    "DELETE /api/admin/users/D twice in parallel with admin JWT",
                    "GET /api/admin/users",
                ]
            },
            ensure_ascii=False,
        ),
        "ExpectedResult": (
            "D absent from final list exactly once removed. Second parallel DELETE may error or noop — not specified. "
            "No other user deleted; SEC-01 no password in responses. " + NO_HTTP
        ),
        "Priority": "High",
    },
    {
        "TestCaseID": "TC-ADMINUSERS-SEC-SUP-004",
        "module": "admin-users",
        "API": "AdminDeleteUser",
        "Method": "DELETE",
        "Endpoint": "/api/admin/users/:id",
        "fr": "FR-19 / SEC-05",
        "sec": "SEC-05",
        "threat": "Negative path id -1",
        "type": "Boundary / injection",
        "why": (
            "Why AI missed: Model limitation — path SQLi cases used string tautologies (SEC-004/005/011); "
            "numeric boundary ids (-1, 0) as type-confusion deletes are a separate SEC-05 partition."
        ),
        "Preconditions": (
            "EShop at http://localhost:3000. | POST /api/login email=admin@eshop.com password=Admin123!. | "
            "Snapshot GET /api/admin/users count."
        ),
        "Input": json.dumps({"path": {"id": "-1"}}, ensure_ascii=False),
        "ExpectedResult": (
            "Must not delete seed users or cause SQL/500 leak. List count unchanged except legitimate target. "
            "SEC-05 parameterized path parsing. " + NO_HTTP
        ),
        "Priority": "Medium",
        "steps": [
            "DELETE /api/admin/users/-1 with admin JWT.",
            "GET /api/admin/users — compare count to snapshot.",
        ],
    },
    {
        "TestCaseID": "TC-ADMINUSERS-SEC-SUP-005",
        "module": "admin-users",
        "API": "AdminDeleteUser",
        "Method": "DELETE",
        "Endpoint": "/api/admin/users/:id",
        "fr": "FR-19 / SEC-05",
        "sec": "SEC-05",
        "threat": "Path traversal — encoded slash in :id",
        "type": "Path manipulation",
        "why": (
            "Why AI missed: API characteristic — AI used SQL metacharacters in path; "
            "URL-encoded slash (%2f) routing confusion is an HTTP/framework attack absent from spec text."
        ),
        "Preconditions": (
            "EShop at http://localhost:3000. | POST /api/login email=admin@eshop.com password=Admin123!. | "
            "Note seed user id=2 exists."
        ),
        "Input": json.dumps({"path": {"id": "1%2f2"}}, ensure_ascii=False),
        "ExpectedResult": (
            "DELETE must not remove user 2 via path confusion. Treat id as opaque string or reject. "
            "GET /api/admin/users — user 2 still present unless id literally matched. " + NO_HTTP
        ),
        "Priority": "High",
        "steps": [
            "DELETE /api/admin/users/1%2f2 with admin JWT.",
            "GET /api/admin/users — confirm user id=2 still exists.",
        ],
    },
]


def md_body(row: dict) -> str:
    steps = row.get("steps")
    if not steps:
        inp = json.loads(row["Input"])
        steps = inp.get("sequence") or ["Execute probe per Input JSON.", "Verify per Expected result."]
    steps_md = "\n".join(f"{i}. {s}" for i, s in enumerate(steps, 1))
    td = json.dumps(json.loads(row["Input"]), ensure_ascii=False, indent=2)
    return f"""# {row['TestCaseID']}: {row['threat']}

## Requirement ID
{row['fr']}

## Module / Test type / Technique
{row['module']} / Security / Human extension (SEC-SUP)

## Security requirement(s)
{row['sec']}

## Threat / probe
{row['threat']}

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

## Type
{row['type']}

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

    for row in ROWS:
        path = TC_ROOT / row["module"] / f"{row['TestCaseID']}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(md_body(row), encoding="utf-8")

    to_add = [r for r in ROWS if r["TestCaseID"] not in existing]
    if not to_add:
        print(f"No new CSV rows (all {len(ROWS)} SEC-SUP IDs present); refreshed {len(ROWS)} markdown files.")
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
                "Category": "Security",
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
                "Notes": (
                    f"SEC={row['sec']} | Type={row['type']} | Threat={row['threat']} | "
                    f"File=tests/test-cases/{row['module']}/{row['TestCaseID']}.md"
                ),
            }
        )

    with SHEET.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows_out)

    print(f"Appended {len(to_add)} rows to {SHEET} (total {len(rows_out)})")


if __name__ == "__main__":
    main()
