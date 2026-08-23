#!/usr/bin/env python3
"""Generate Stage-1 security test artifacts for FR-04 / FR-07 / FR-19 (SEC-01..SEC-07)."""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TC_ROOT = ROOT / "tests" / "test-cases"
SHEET = ROOT / "sheets" / "security-tests.csv"
REPORT = ROOT / "docs" / "security-testing-report.md"

BASE = "http://localhost:3000"
USER_LOGIN = "POST /api/login email=test@eshop.com password=Test1234!"
ADMIN_LOGIN = "POST /api/login email=admin@eshop.com password=Admin123!"

# Canonical injection / XSS probes
SQL_NAME = "Nguyen' OR '1'='1"
SQL_ADDR = "123 Le Loi'; DROP TABLE users;--"
SQL_PHONE = "0912345678' OR '1'='1"
XSS_NAME = '<script>alert("SEC04")</script>'
XSS_ADDR = '"><img src=x onerror=alert(1)>'
PATH_SQL = "1 OR 1=1"
PATH_STACK = "1; DELETE FROM users WHERE '1'='1"

NO_HTTP = "HTTP status and error body are not specified — record actual without inventing codes."
SEC05_ORACLE = (
    "SEC-05: database must use parameterized queries — request must not cause SQL syntax errors, "
    "500 stack traces with query text, or unauthorized data change. Record status and GET side effects."
)
SEC02_ORACLE = (
    "SEC-02: protected endpoint requires a valid JWT. Profile/cart/user must not change for the attack. "
    + NO_HTTP
)
SEC03_ORACLE = (
    "SEC-03 / FR-12: admin API requires role=admin in token, not merely a valid JWT. "
    "Target user must still exist; no unauthorized delete. " + NO_HTTP
)
SEC06_ORACLE = (
    "SEC-06 / FR-04: role must not change via client body. GET /api/users/me role unchanged. "
    "Documented fields may update — record actual. " + NO_HTTP
)
SEC01_ORACLE = (
    "SEC-01 / FR-19: password must not appear in API responses (plaintext or hash). "
    "Inspect JSON bodies and error messages."
)
SEC04_ORACLE = (
    "SEC-04 targets UI escaping; at API layer record whether payload is stored/returned as literal text "
    "without server-side execution. XSS rendering is a frontend concern — note for manual UI follow-up."
)


def case(**kw):
    return kw


def md_body(c: dict) -> str:
    steps = c.get("steps") or []
    steps_md = "\n".join(f"{i}. {s}" for i, s in enumerate(steps, 1))
    pre = c["preconditions"]
    pre_block = "\n".join(f"- {p.strip()}" for p in pre.split("|"))
    td = c.get("test_data", [])
    td_block = "| Field | Value |\n|-------|-------|\n" + "\n".join(f"| {k} | {v} |" for k, v in td) if td else "| (see steps) | |"
    return f"""# {c['id']}: {c['title']}

## Requirement ID
{c['fr']}

## Module / Test type / Technique
{c['module']} / Security / SEC-mapped probe

## Security requirement(s)
{c['sec']}

## Threat / probe
{c['threat']}

## Preconditions
{pre_block}

## Test data
{td_block}

## Test steps
{steps_md}

## Expected result
{c['expected']}

## SEC coverage
{c['sec']}

## Type
{c['type']}

## Status / Related bugs
Not Run / None
"""


def csv_row(c: dict) -> dict:
    inp = c.get("input")
    if inp is None:
        inp = json.dumps({"body": c.get("body", {}), "headers": c.get("headers", {})}, ensure_ascii=False)
    return {
        "TestCaseID": c["id"],
        "API": c["api"],
        "Method": c["method"],
        "Endpoint": c["endpoint"],
        "Category": "Security",
        "Preconditions": c["preconditions"],
        "Input": inp if isinstance(inp, str) else json.dumps(inp, ensure_ascii=False),
        "ExpectedResult": c["expected"].replace("\n", " "),
        "Priority": c.get("priority", "High"),
        "Source": "AI",
        "AuditStatus": "",
        "AuditReasoning": "",
        "ActualResult": "",
        "PassFail": "",
        "BugRef": "",
        "Notes": f"SEC={c['sec']} | Threat={c['threat']} | File=tests/test-cases/{c['module']}/{c['id']}.md",
    }


PROFILE = [
    case(
        id="TC-PROFILE-SEC-001", module="profile", api="UpdateProfile", method="PUT", endpoint="/api/users/me",
        fr="FR-04", sec="SEC-05", threat="SQL injection in name",
        title="SQLi classic OR tautology in name field",
        preconditions=f"EShop at {BASE}. | {USER_LOGIN}. | Snapshot GET /api/users/me.",
        test_data=[("name", SQL_NAME), ("phone", "0912345678"), ("shipping_address", "123 Le Loi, Q1")],
        steps=["PUT /api/users/me with SQLi name payload.", "GET /api/users/me — email/role unchanged; no SQL error leak."],
        expected=SEC05_ORACLE + " email/role unchanged.",
        type="Security probe",
        body={"name": SQL_NAME, "phone": "0912345678", "shipping_address": "123 Le Loi, Q1"},
    ),
    case(
        id="TC-PROFILE-SEC-002", module="profile", api="UpdateProfile", method="PUT", endpoint="/api/users/me",
        fr="FR-04", sec="SEC-05", threat="SQL injection UNION in name",
        title="SQLi UNION SELECT probe in name",
        preconditions=f"EShop at {BASE}. | {USER_LOGIN}.",
        test_data=[("name", "x' UNION SELECT null,null,null--"), ("phone", "0912345678"), ("shipping_address", "Addr")],
        steps=["PUT /api/users/me with UNION payload in name.", "GET /api/users/me."],
        expected=SEC05_ORACLE,
        type="Security probe",
        body={"name": "x' UNION SELECT null,null,null--", "phone": "0912345678", "shipping_address": "Addr"},
    ),
    case(
        id="TC-PROFILE-SEC-003", module="profile", api="UpdateProfile", method="PUT", endpoint="/api/users/me",
        fr="FR-04", sec="SEC-05", threat="SQL injection in shipping_address",
        title="SQLi stacked DROP probe in shipping_address",
        preconditions=f"EShop at {BASE}. | {USER_LOGIN}.",
        test_data=[("name", "Nguyen Van A"), ("phone", "0912345678"), ("shipping_address", SQL_ADDR)],
        steps=["PUT /api/users/me with SQLi address.", "GET /api/users/me — profile intact; no SQL error leak."],
        expected=SEC05_ORACLE + " shipping_address must not corrupt user record.",
        type="Security probe",
        body={"name": "Nguyen Van A", "phone": "0912345678", "shipping_address": SQL_ADDR},
    ),
    case(
        id="TC-PROFILE-SEC-004", module="profile", api="UpdateProfile", method="PUT", endpoint="/api/users/me",
        fr="FR-04", sec="SEC-05", threat="SQL injection in phone",
        title="SQLi OR probe in phone field",
        preconditions=f"EShop at {BASE}. | {USER_LOGIN}.",
        test_data=[("phone", SQL_PHONE)],
        steps=["PUT /api/users/me with SQLi phone (other fields FR-04-valid).", "GET /api/users/me."],
        expected=SEC05_ORACLE + " phone must not become a valid FR-04 phone if injection fails.",
        type="Security probe",
        body={"name": "Nguyen Van A", "phone": SQL_PHONE, "shipping_address": "123 Le Loi"},
    ),
    case(
        id="TC-PROFILE-SEC-005", module="profile", api="UpdateProfile", method="PUT", endpoint="/api/users/me",
        fr="FR-04", sec="SEC-04", threat="Stored XSS script in name",
        title="Stored XSS script tag in name (API literal storage)",
        preconditions=f"EShop at {BASE}. | {USER_LOGIN}.",
        test_data=[("name", XSS_NAME)],
        steps=["PUT /api/users/me with script payload in name.", "GET /api/users/me — inspect JSON literal."],
        expected=SEC04_ORACLE + " role/email unchanged.",
        type="Security probe",
        body={"name": XSS_NAME, "phone": "0912345678", "shipping_address": "123 Le Loi"},
    ),
    case(
        id="TC-PROFILE-SEC-006", module="profile", api="UpdateProfile", method="PUT", endpoint="/api/users/me",
        fr="FR-04", sec="SEC-04", threat="Stored XSS event handler in address",
        title="Stored XSS img onerror in shipping_address",
        preconditions=f"EShop at {BASE}. | {USER_LOGIN}.",
        test_data=[("shipping_address", XSS_ADDR)],
        steps=["PUT /api/users/me with XSS address payload.", "GET /api/users/me."],
        expected=SEC04_ORACLE,
        type="Security probe",
        body={"name": "Nguyen Van A", "phone": "0912345678", "shipping_address": XSS_ADDR},
    ),
    case(
        id="TC-PROFILE-SEC-007", module="profile", api="UpdateProfile", method="PUT", endpoint="/api/users/me",
        fr="FR-04", sec="SEC-06", threat="Role escalation role=admin",
        title="Mass assignment — role=admin in profile body",
        preconditions=f"EShop at {BASE}. | {USER_LOGIN}. | GET role=user.",
        steps=['PUT /api/users/me with "role":"admin" plus valid profile fields.', "GET /api/users/me."],
        expected=SEC06_ORACLE,
        type="Security probe",
        body={"name": "Nguyen Van A", "phone": "0912345678", "shipping_address": "123 Le Loi", "role": "admin"},
    ),
    case(
        id="TC-PROFILE-SEC-008", module="profile", api="UpdateProfile", method="PUT", endpoint="/api/users/me",
        fr="FR-04", sec="SEC-06", threat="Mass assignment password field",
        title="Mass assignment — password in profile PUT body",
        preconditions=f"EShop at {BASE}. | {USER_LOGIN}.",
        steps=['PUT body includes "password":"Hacked123!" with valid profile fields.', "POST /api/login with original password Test1234!."],
        expected=(
            "SEC-06 / SEC-01: password must not be overwritten via profile PUT. Login with original password still works. "
            "GET /api/users/me must not expose password. " + NO_HTTP
        ),
        type="Security probe",
        body={"name": "Nguyen Van A", "phone": "0912345678", "shipping_address": "123 Le Loi", "password": "Hacked123!"},
    ),
    case(
        id="TC-PROFILE-SEC-009", module="profile", api="UpdateProfile", method="PUT", endpoint="/api/users/me",
        fr="FR-04", sec="SEC-02", threat="Auth bypass — no JWT",
        title="Auth bypass — PUT without Authorization header",
        preconditions=f"EShop at {BASE}. | Snapshot GET /api/users/me as test user.",
        steps=["PUT /api/users/me valid body with no Authorization header.", "GET /api/users/me with valid token."],
        expected=SEC02_ORACLE + " Snapshot profile unchanged.",
        type="Security probe",
        headers={"Content-Type": "application/json"},
        input=json.dumps({"headers": {"Content-Type": "application/json"}, "body": {"name": "Hacked", "phone": "0912345678", "shipping_address": "X"}}, ensure_ascii=False),
    ),
    case(
        id="TC-PROFILE-SEC-010", module="profile", api="UpdateProfile", method="PUT", endpoint="/api/users/me",
        fr="FR-04", sec="SEC-02", threat="Auth bypass — invalid signature JWT",
        title="JWT tampering — invalid signature on PUT",
        preconditions=f"EShop at {BASE}. | Valid user token available.",
        steps=["PUT /api/users/me with Authorization Bearer <token_with_bad_signature>.", "GET with valid token."],
        expected=SEC02_ORACLE,
        type="Security probe",
        input=json.dumps({"headers": {"Authorization": "Bearer <tampered_token>", "Content-Type": "application/json"}, "body": {"name": "Nguyen Van A", "phone": "0912345678", "shipping_address": "123 Le Loi"}}, ensure_ascii=False),
    ),
    case(
        id="TC-PROFILE-SEC-011", module="profile", api="UpdateProfile", method="PUT", endpoint="/api/users/me",
        fr="FR-04", sec="SEC-06", threat="Privilege — email change",
        title="Immutable email — client attempts email change",
        preconditions=f"EShop at {BASE}. | {USER_LOGIN}. | email=test@eshop.com.",
        steps=['PUT with "email":"attacker@evil.com".', "GET /api/users/me."],
        expected="FR-04: email must remain test@eshop.com. Request rejected or email ignored. " + NO_HTTP,
        type="Security probe",
        body={"name": "Nguyen Van A", "phone": "0912345678", "shipping_address": "123 Le Loi", "email": "attacker@evil.com"},
    ),
    case(
        id="TC-PROFILE-SEC-012", module="profile", api="UpdateProfile", method="PUT", endpoint="/api/users/me",
        fr="FR-04", sec="SEC-06", threat="Mass assignment login_attempts / locked_until",
        title="Mass assignment — login_attempts and locked_until in body",
        preconditions=f"EShop at {BASE}. | {USER_LOGIN}.",
        steps=['PUT with "login_attempts":0,"locked_until":null plus valid fields.', "GET /api/users/me."],
        expected="Undocumented fields must not grant account-lockout bypass or admin flags. role/email unchanged. Record actual.",
        type="Security probe",
        body={"name": "Nguyen Van A", "phone": "0912345678", "shipping_address": "123 Le Loi", "login_attempts": 0, "locked_until": None},
    ),
    case(
        id="TC-PROFILE-SEC-013", module="profile", api="UpdateProfile", method="PUT", endpoint="/api/users/me",
        fr="FR-04", sec="SEC-05", threat="SQLi in Authorization header",
        title="SQLi probe via Authorization Bearer value",
        preconditions=f"EShop at {BASE}.",
        steps=['PUT /api/users/me with Authorization: Bearer \' OR 1=1-- and valid body.', "GET /api/users/me with valid token."],
        expected=SEC05_ORACLE + " " + SEC02_ORACLE,
        type="Security probe",
        input=json.dumps({"headers": {"Authorization": "Bearer ' OR 1=1--", "Content-Type": "application/json"}, "body": {"name": "Nguyen Van A", "phone": "0912345678", "shipping_address": "123 Le Loi"}}, ensure_ascii=False),
    ),
    case(
        id="TC-PROFILE-SEC-014", module="profile", api="UpdateProfile", method="PUT", endpoint="/api/users/me",
        fr="FR-04", sec="SEC-04", threat="Template/polyglot injection in name",
        title="Polyglot payload ${7*7} in name",
        preconditions=f"EShop at {BASE}. | {USER_LOGIN}.",
        test_data=[("name", "${7*7} {{constructor.constructor('return 1')()}}")],
        steps=["PUT with template/polyglot name.", "GET /api/users/me — value stored literally or rejected."],
        expected=SEC04_ORACLE + " No server-side template evaluation in API JSON.",
        type="Security probe",
        body={"name": "${7*7} {{constructor.constructor('return 1')()}}", "phone": "0912345678", "shipping_address": "123 Le Loi"},
    ),
]

CART = [
    case(
        id="TC-CART-SEC-001", module="cart", api="AddToCart", method="POST", endpoint="/api/cart",
        fr="FR-07", sec="SEC-02", threat="Auth bypass — no JWT",
        title="POST /api/cart without Authorization",
        preconditions=f"EShop at {BASE}.",
        steps=["POST /api/cart valid body, no Authorization.", "GET /api/cart as test user — cart unchanged."],
        expected=SEC02_ORACLE + " No line added.",
        type="Security probe",
        input=json.dumps({"headers": {"Content-Type": "application/json"}, "body": {"id": 1, "name": "iPhone", "price": 30000000, "quantity": 1}}, ensure_ascii=False),
    ),
    case(
        id="TC-CART-SEC-002", module="cart", api="AddToCart", method="POST", endpoint="/api/cart",
        fr="FR-07", sec="SEC-02", threat="Auth bypass — malformed JWT",
        title="POST /api/cart with malformed JWT",
        preconditions=f"EShop at {BASE}.",
        steps=["POST /api/cart with Bearer not-a-jwt.", "GET /api/cart with valid user token."],
        expected=SEC02_ORACLE,
        type="Security probe",
        input=json.dumps({"headers": {"Authorization": "Bearer not-a-jwt", "Content-Type": "application/json"}, "body": {"id": 1, "name": "iPhone", "price": 30000000, "quantity": 1}}, ensure_ascii=False),
    ),
    case(
        id="TC-CART-SEC-003", module="cart", api="AddToCart", method="POST", endpoint="/api/cart",
        fr="FR-07", sec="SEC-05", threat="SQL injection in name",
        title="SQLi in cart line name field",
        preconditions=f"EShop at {BASE}. | {USER_LOGIN}.",
        test_data=[("name", SQL_NAME)],
        steps=["POST /api/cart with SQLi name.", "GET /api/cart — line stored or rejected; no SQL error leak."],
        expected=SEC05_ORACLE + " Cart POST/GET must not expose SQL errors or corrupt cart data.",
        type="Security probe",
        body={"id": 1, "name": SQL_NAME, "price": 30000000, "quantity": 1},
    ),
    case(
        id="TC-CART-SEC-004", module="cart", api="AddToCart", method="POST", endpoint="/api/cart",
        fr="FR-07", sec="SEC-05", threat="SQL injection numeric id as string",
        title="SQLi-style string id in JSON body",
        preconditions=f"EShop at {BASE}. | {USER_LOGIN}.",
        test_data=[("id", "1 OR 1=1")],
        steps=['POST /api/cart with id="1 OR 1=1" (string).', "GET /api/cart."],
        expected=SEC05_ORACLE + " Record coercion behaviour; no DB error leak.",
        type="Security probe",
        body={"id": "1 OR 1=1", "name": "iPhone", "price": 30000000, "quantity": 1},
    ),
    case(
        id="TC-CART-SEC-005", module="cart", api="AddToCart", method="POST", endpoint="/api/cart",
        fr="FR-07", sec="SEC-04", threat="Stored XSS in cart name",
        title="XSS payload in cart item name",
        preconditions=f"EShop at {BASE}. | {USER_LOGIN}.",
        steps=["POST with XSS name.", "GET /api/cart — literal in JSON."],
        expected=SEC04_ORACLE,
        type="Security probe",
        body={"id": 1, "name": XSS_NAME, "price": 30000000, "quantity": 1},
    ),
    case(
        id="TC-CART-SEC-006", module="cart", api="AddToCart", method="POST", endpoint="/api/cart",
        fr="FR-07", sec="SEC-06", threat="Price tampering / integrity",
        title="Client price tampering — price=1 for expensive product",
        preconditions=f"EShop at {BASE}. | {USER_LOGIN}.",
        test_data=[("id", 1), ("price", 1), ("quantity", 1)],
        steps=["POST /api/cart id=1 price=1.", "GET /api/cart — record stored price and quantity."],
        expected=(
            "FR-07 cart must not accept client price tampering without server-side validation. "
            "Record whether POST rejects price=1 or GET shows catalogue/server price instead of 1. " + NO_HTTP
        ),
        type="Security probe / integrity",
        body={"id": 1, "name": "iPhone 15 Pro Max", "price": 1, "quantity": 1},
    ),
    case(
        id="TC-CART-SEC-007", module="cart", api="AddToCart", method="GET", endpoint="/api/cart",
        fr="FR-07", sec="SEC-02", threat="IDOR — cross-user cart read",
        title="IDOR — user B cannot read user A cart via GET",
        preconditions=f"EShop at {BASE}. | User A and B exist.",
        steps=["Login A. POST item to cart. Login B. GET /api/cart as B.", "Confirm B cart does not show A line."],
        expected="Cart is scoped to JWT subject. B's GET must not return A's lines (IDOR).",
        type="Security probe",
        input=json.dumps({"sequence": ["user A POST", "user B GET /api/cart"]}, ensure_ascii=False),
    ),
    case(
        id="TC-CART-SEC-008", module="cart", api="AddToCart", method="POST", endpoint="/api/cart",
        fr="FR-07", sec="SEC-06", threat="Mass assignment user_id",
        title="Mass assignment — user_id in POST body",
        preconditions=f"EShop at {BASE}. | {USER_LOGIN}. | Note admin user id=1.",
        steps=['POST /api/cart with "user_id":1 in body as test user.', "GET /api/cart as test user — line belongs to JWT subject, not body user_id."],
        expected="Item must attach to authenticated user (test), not admin via body user_id. Record actual.",
        type="Security probe",
        body={"id": 1, "name": "iPhone", "price": 30000000, "quantity": 1, "user_id": 1},
    ),
    case(
        id="TC-CART-SEC-010", module="cart", api="AddToCart", method="POST", endpoint="/api/cart",
        fr="FR-07", sec="SEC-05", threat="NoSQL-style operator in name",
        title="NoSQL-style $gt operator string in name",
        preconditions=f"EShop at {BASE}. | {USER_LOGIN}.",
        test_data=[("name", '{"$gt":""}')],
        steps=["POST with NoSQL-style name string.", "GET /api/cart."],
        expected=SEC05_ORACLE + " SQLite backend — record literal storage vs parse error.",
        type="Security probe",
        body={"id": 1, "name": '{"$gt":""}', "price": 30000000, "quantity": 1},
    ),
    case(
        id="TC-CART-SEC-011", module="cart", api="AddToCart", method="POST", endpoint="/api/cart",
        fr="FR-07", sec="SEC-02", threat="IDOR — POST to another user cart",
        title="IDOR attempt — user_id path not in API; body user_id swap",
        preconditions=f"EShop at {BASE}. | Register user C. | Login test user.",
        steps=["POST with user_id set to C's id.", "Login as C. GET /api/cart."],
        expected="Line must not appear in C's cart unless server ignores user_id (then record as finding).",
        type="Security probe",
        body={"id": 1, "name": "iPhone", "price": 30000000, "quantity": 1, "user_id": "<user_C_id>"},
    ),
    case(
        id="TC-CART-SEC-012", module="cart", api="AddToCart", method="POST", endpoint="/api/cart",
        fr="FR-07", sec="SEC-05", threat="SQLi in Authorization header",
        title="SQLi in Authorization header on POST /api/cart",
        preconditions=f"EShop at {BASE}.",
        steps=["POST /api/cart with Bearer SQLi token.", "GET /api/cart with valid token."],
        expected=SEC05_ORACLE + " " + SEC02_ORACLE,
        type="Security probe",
        input=json.dumps({"headers": {"Authorization": "Bearer ' OR '1'='1", "Content-Type": "application/json"}, "body": {"id": 1, "name": "iPhone", "price": 30000000, "quantity": 1}}, ensure_ascii=False),
    ),
]

ADMIN = [
    case(
        id="TC-ADMINUSERS-SEC-001", module="admin-users", api="AdminDeleteUser", method="DELETE", endpoint="/api/admin/users/:id",
        fr="FR-19", sec="SEC-02", threat="Auth bypass — no JWT",
        title="DELETE without Authorization",
        preconditions=f"EShop at {BASE}. | Disposable user D registered.",
        steps=["DELETE /api/admin/users/D without Authorization.", "GET /api/admin/users as admin."],
        expected=SEC02_ORACLE + " D still in list.",
        type="Security probe",
        input=json.dumps({"path": {"id": "<D>"}, "headers": {}}, ensure_ascii=False),
    ),
    case(
        id="TC-ADMINUSERS-SEC-002", module="admin-users", api="AdminDeleteUser", method="DELETE", endpoint="/api/admin/users/:id",
        fr="FR-19", sec="SEC-03", threat="Role escalation — user JWT",
        title="User JWT on admin DELETE",
        preconditions=f"EShop at {BASE}. | {USER_LOGIN}. | Disposable D exists.",
        steps=["DELETE /api/admin/users/D with user token.", "GET /api/admin/users as admin."],
        expected=SEC03_ORACLE,
        type="Security probe",
        input=json.dumps({"headers": {"Authorization": "Bearer <user_token>"}, "path": {"id": "<D>"}}, ensure_ascii=False),
    ),
    case(
        id="TC-ADMINUSERS-SEC-003", module="admin-users", api="AdminDeleteUser", method="DELETE", endpoint="/api/admin/users/:id",
        fr="FR-19", sec="SEC-03", threat="Admin self-delete bypass FR-19",
        title="FR-19 — admin cannot delete self via DELETE",
        preconditions=f"EShop at {BASE}. | {ADMIN_LOGIN}. | admin_self_id from GET.",
        steps=["DELETE /api/admin/users/{admin_self_id}.", "GET /api/admin/users — admin account still present."],
        expected="FR-19: logged-in admin must not be deleted. " + NO_HTTP,
        type="Security probe",
        input=json.dumps({"path": {"id": "<admin_self_id>"}}, ensure_ascii=False),
    ),
    case(
        id="TC-ADMINUSERS-SEC-004", module="admin-users", api="AdminDeleteUser", method="DELETE", endpoint="/api/admin/users/:id",
        fr="FR-19", sec="SEC-05", threat="SQL injection in path id",
        title="SQLi OR tautology in path :id",
        preconditions=f"EShop at {BASE}. | {ADMIN_LOGIN}.",
        steps=[f"DELETE /api/admin/users/{PATH_SQL}.", "GET /api/admin/users — no mass delete of all users."],
        expected=SEC05_ORACLE + " Must not delete all users or return SQL error with query text.",
        type="Security probe",
        input=json.dumps({"path": {"id": PATH_SQL}}, ensure_ascii=False),
    ),
    case(
        id="TC-ADMINUSERS-SEC-005", module="admin-users", api="AdminDeleteUser", method="DELETE", endpoint="/api/admin/users/:id",
        fr="FR-19", sec="SEC-05", threat="SQL injection stacked in path",
        title="SQLi stacked DELETE in path :id",
        preconditions=f"EShop at {BASE}. | {ADMIN_LOGIN}.",
        steps=[f"DELETE /api/admin/users/{PATH_STACK}.", "GET /api/admin/users."],
        expected=SEC05_ORACLE + " Seed users admin and test still exist unless path parsed as single id safely.",
        type="Security probe",
        input=json.dumps({"path": {"id": PATH_STACK}}, ensure_ascii=False),
    ),
    case(
        id="TC-ADMINUSERS-SEC-006", module="admin-users", api="AdminListUsers", method="GET", endpoint="/api/admin/users",
        fr="FR-19", sec="SEC-01", threat="Password exposure in list response",
        title="SEC-01 — GET /api/admin/users never exposes password",
        preconditions=f"EShop at {BASE}. | {ADMIN_LOGIN}.",
        steps=["GET /api/admin/users.", "Inspect every object for password/password_hash fields."],
        expected=SEC01_ORACLE,
        type="Security probe",
        input=json.dumps({"headers": {}, "query": {}}, ensure_ascii=False),
    ),
    case(
        id="TC-ADMINUSERS-SEC-007", module="admin-users", api="AdminDeleteUser", method="DELETE", endpoint="/api/admin/users/:id",
        fr="FR-19", sec="SEC-01", threat="Password in DELETE error response",
        title="SEC-01 — error response on DELETE must not leak password",
        preconditions=f"EShop at {BASE}. | {ADMIN_LOGIN}.",
        steps=["DELETE /api/admin/users/99999 (missing user).", "Inspect response body for password/hash substrings."],
        expected=SEC01_ORACLE + " " + NO_HTTP,
        type="Security probe",
        input=json.dumps({"path": {"id": "99999"}}, ensure_ascii=False),
    ),
    case(
        id="TC-ADMINUSERS-SEC-008", module="admin-users", api="AdminDeleteUser", method="DELETE", endpoint="/api/admin/users/:id",
        fr="FR-19", sec="SEC-05", threat="SQLi in JSON DELETE body",
        title="SQLi in unexpected DELETE JSON body",
        preconditions=f"EShop at {BASE}. | {ADMIN_LOGIN}. | Disposable D.",
        steps=['DELETE /api/admin/users/D with body {"id":"\' OR 1=1--"}.', "GET /api/admin/users."],
        expected=SEC05_ORACLE + " Path id D is authoritative; body must not widen delete scope.",
        type="Security probe",
        input=json.dumps({"path": {"id": "<D>"}, "body": {"id": "' OR 1=1--"}}, ensure_ascii=False),
    ),
    case(
        id="TC-ADMINUSERS-SEC-010", module="admin-users", api="AdminDeleteUser", method="DELETE", endpoint="/api/admin/users/:id",
        fr="FR-19", sec="SEC-02", threat="Empty Bearer token",
        title="DELETE with empty Bearer token",
        preconditions=f"EShop at {BASE}. | Disposable D.",
        steps=["DELETE with Authorization: Bearer (empty).", "GET /api/admin/users as admin."],
        expected=SEC02_ORACLE,
        type="Security probe",
        input=json.dumps({"headers": {"Authorization": "Bearer "}, "path": {"id": "<D>"}}, ensure_ascii=False),
    ),
    case(
        id="TC-ADMINUSERS-SEC-011", module="admin-users", api="AdminDeleteUser", method="DELETE", endpoint="/api/admin/users/:id",
        fr="FR-19", sec="SEC-05", threat="SQLi percent-encoded path",
        title="URL-encoded SQLi in path id",
        preconditions=f"EShop at {BASE}. | {ADMIN_LOGIN}.",
        steps=["DELETE /api/admin/users/1%20OR%201%3D1.", "GET /api/admin/users."],
        expected=SEC05_ORACLE + " Must not delete unintended users.",
        type="Security probe",
        input=json.dumps({"path": {"id": "1%20OR%201%3D1"}}, ensure_ascii=False),
    ),
    case(
        id="TC-ADMINUSERS-SEC-013", module="admin-users", api="AdminDeleteUser", method="DELETE", endpoint="/api/admin/users/:id",
        fr="FR-19", sec="SEC-01", threat="Data exposure after successful delete",
        title="DELETE success body must not echo password",
        preconditions=f"EShop at {BASE}. | {ADMIN_LOGIN}. | Register D.",
        steps=["DELETE D.", "Inspect 200/success JSON for password fields."],
        expected=SEC01_ORACLE,
        type="Security probe",
        input=json.dumps({"path": {"id": "<D>"}}, ensure_ascii=False),
    ),
    case(
        id="TC-ADMINUSERS-SEC-014", module="admin-users", api="AdminDeleteUser", method="DELETE", endpoint="/api/admin/users/:id",
        fr="FR-19", sec="SEC-05", threat="SQLi in Authorization on DELETE",
        title="SQLi Bearer token on admin DELETE",
        preconditions=f"EShop at {BASE}. | Disposable D.",
        steps=["DELETE D with Authorization Bearer ' OR 1=1--.", "GET list as admin."],
        expected=SEC05_ORACLE + " " + SEC02_ORACLE,
        type="Security probe",
        input=json.dumps({"headers": {"Authorization": "Bearer ' OR 1=1--"}, "path": {"id": "<D>"}}, ensure_ascii=False),
    ),
]

ALL = PROFILE + CART + ADMIN


def build_report() -> str:
    sec_map = {}
    for c in ALL:
        for s in c["sec"].replace("/", " ").split():
            if s.startswith("SEC-"):
                sec_map.setdefault(s, []).append(c["id"])

    lines = [
        "# Security Testing Report — FR-04, FR-07, FR-19",
        "",
        f"**Student:** 23127271 · **SUT:** EShop (`{BASE}`)  ",
        "**Category:** Stage 1 — Security (API testing skill checklist section 3)  ",
        "**Sources:** `Repo/eshop-sut/README.md` (SEC-01..SEC-07), `api_specification.md`",
        "",
        "---",
        "",
        "## SEC requirement applicability",
        "",
        "| SEC | Requirement | In-scope endpoints | Testable here? |",
        "|-----|-------------|-------------------|----------------|",
        "| SEC-01 | Password not plaintext in storage/responses | GET /api/admin/users, DELETE responses | Yes (FR-19) |",
        "| SEC-02 | Protected APIs require valid JWT | PUT /me, POST /cart, GET /cart (IDOR), DELETE admin | Yes |",
        "| SEC-03 | Admin APIs require role=admin | DELETE /api/admin/users/:id | Yes |",
        "| SEC-04 | UI escape user input | Profile/cart string fields on in-scope PUT/POST | API stores literal; UI manual |",
        "| SEC-05 | Parameterized queries | In-scope string/path inputs | Yes |",
        "| SEC-06 | No privilege/integrity tampering via body | PUT /me, POST /cart | Yes |",
        "| SEC-07 | OTP reset entropy/expiry | Forgot-password APIs | **Gap** — not in FR-04/07/19 scope |",
        "",
        "## In-scope endpoints",
        "",
        "| FR | Primary endpoints under test | Allowed verification only |",
        "|----|------------------------------|---------------------------|",
        "| FR-04 | `PUT /api/users/me` | `GET /api/users/me`; `POST /api/login` as password oracle |",
        "| FR-07 | `POST /api/cart` | `GET /api/cart` for cart isolation/IDOR and POST side effects |",
        "| FR-19 | `DELETE /api/admin/users/:id`, `GET /api/admin/users` | `GET /api/admin/users` after DELETE for SEC-01/SEC-03 checks |",
        "",
        "Out of scope (no dedicated security TCs): checkout (FR-08), catalogue/products (FR-05), login/register (FR-02/03), forgot-password (SEC-07).",
        "",
        "## SEC → test case map",
        "",
        "| SEC | TC IDs |",
        "|-----|--------|",
    ]
    for sec in sorted(sec_map):
        lines.append(f"| {sec} | {', '.join(sorted(sec_map[sec]))} |")

    lines += ["", "---", "", "## FR-04 — `PUT /api/users/me`", "", f"**Count:** {len(PROFILE)} cases", "", "| TC ID | SEC | Threat |", "|-------|-----|--------|"]
    for c in PROFILE:
        lines.append(f"| {c['id']} | {c['sec']} | {c['threat']} |")

    lines += ["", "---", "", "## FR-07 — `POST /api/cart` (+ GET cart IDOR)", "", f"**Count:** {len(CART)} cases", "", "| TC ID | SEC | Threat |", "|-------|-----|--------|"]
    for c in CART:
        lines.append(f"| {c['id']} | {c['sec']} | {c['threat']} |")

    lines += [
        "", "---", "",
        "## FR-19 — `DELETE /api/admin/users/:id` + `GET /api/admin/users`",
        "",
        f"**Count:** {len(ADMIN)} cases",
        "",
        "| TC ID | SEC | Threat |",
        "|-------|-----|--------|",
    ]
    for c in ADMIN:
        lines.append(f"| {c['id']} | {c['sec']} | {c['threat']} |")

    total = len(ALL)
    lines += [
        "",
        "---",
        "",
        "## Combined Stage-1 counts (domain + state + security)",
        "",
        f"- FR-04: 40 + 12 + {len(PROFILE)} = **{40 + 12 + len(PROFILE)}**",
        f"- FR-07: 39 + 15 + {len(CART)} = **{39 + 15 + len(CART)}**",
        f"- FR-19: 20 + 15 + {len(ADMIN)} = **{20 + 15 + len(ADMIN)}**",
        "",
        "## Artifacts",
        "",
        "| Artifact | Path |",
        "|----------|------|",
        "| This report | `docs/security-testing-report.md` |",
        "| Per-TC files | `tests/test-cases/{profile,cart,admin-users}/TC-*-SEC-*.md` |",
        "| Sheet | `sheets/security-tests.csv` |",
        "| Generator | `scripts/generate_security_tests.py` |",
        "",
        f"**Total security cases:** {total} AI-generated.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    fieldnames = [
        "TestCaseID", "API", "Method", "Endpoint", "Category", "Preconditions", "Input",
        "ExpectedResult", "Priority", "Source", "AuditStatus", "AuditReasoning",
        "ActualResult", "PassFail", "BugRef", "Notes",
    ]
    for c in ALL:
        path = TC_ROOT / c["module"] / f"{c['id']}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(md_body(c), encoding="utf-8")

    with SHEET.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for c in ALL:
            w.writerow(csv_row(c))

    REPORT.write_text(build_report(), encoding="utf-8")
    print(f"Wrote {len(ALL)} security cases")
    print(f"  PROFILE: {len(PROFILE)}")
    print(f"  CART: {len(CART)}")
    print(f"  ADMINUSERS: {len(ADMIN)}")
    print(f"Sheet: {SHEET}")
    print(f"Report: {REPORT}")


if __name__ == "__main__":
    main()
