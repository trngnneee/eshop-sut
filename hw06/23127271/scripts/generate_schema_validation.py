#!/usr/bin/env python3
"""Generate Stage-1 schema-validation test artifacts for FR-04 / FR-07 / FR-19."""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TC_ROOT = ROOT / "tests" / "test-cases"
SHEET = ROOT / "sheets" / "schema-validation.csv"
REPORT = ROOT / "docs" / "schema-validation-report.md"

BASE = "http://localhost:3000"
USER_LOGIN = "POST /api/login email=test@eshop.com password=Test1234!"
ADMIN_LOGIN = "POST /api/login email=admin@eshop.com password=Admin123!"

NO_HTTP = "HTTP status is not specified in api_specification.md — record actual without inventing codes."
CT_JSON = "Response Content-Type header includes application/json (or charset=utf-8 JSON body)."
VALID_BODY = (
    '{"name":"Nguyen Van A","shipping_address":"123 Le Loi, Q1, TP.HCM","phone":"0912345678"}'
)
CART_BODY = '{"id":1,"name":"San pham A","price":100000,"quantity":2}'


def case(**kw):
    return kw


def md_body(c: dict) -> str:
    steps = c.get("steps") or []
    steps_md = "\n".join(f"{i}. {s}" for i, s in enumerate(steps, 1))
    pre_block = "\n".join(f"- {p.strip()}" for p in c["preconditions"].split("|"))
    schema = c.get("schema_check", "")
    return f"""# {c['id']}: {c['title']}

## Requirement ID
{c['fr']}

## Module / Test type / Technique
{c['module']} / Schema validation / Response & request shape

## Schema aspect
{c['aspect']}

## Preconditions
{pre_block}

## Test data
| (see steps) | |

## Test steps
{steps_md}

## Expected result
{c['expected']}

## Schema contract reference
{schema}

## Type
Schema validation

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
        "Category": "SchemaValidation",
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
        "Notes": f"Aspect={c['aspect']} | File=tests/test-cases/{c['module']}/{c['id']}.md",
    }


PROFILE = [
    case(
        id="TC-PROFILE-SCH-001", module="profile", api="GetProfile", method="GET", endpoint="/api/users/me",
        fr="FR-04", aspect="GET response root type", title="GET /api/users/me returns JSON object",
        preconditions=f"EShop at {BASE}. | {USER_LOGIN}.",
        steps=["GET /api/users/me with valid JWT.", "Parse body as JSON; assert root is object (not array/null)."],
        expected=f"Body is a JSON object. {CT_JSON} {NO_HTTP}",
        schema_check="api_spec section 2.1 documents GET profile; root envelope type not explicit — object inferred from single-user resource.",
    ),
    case(
        id="TC-PROFILE-SCH-002", module="profile", api="GetProfile", method="GET", endpoint="/api/users/me",
        fr="FR-04", aspect="Field name type", title="Profile name field is string",
        preconditions=f"EShop at {BASE}. | {USER_LOGIN}.",
        steps=["GET /api/users/me.", "Assert typeof name === 'string' when present."],
        expected="name is present and typeof string (FR-04 profile field). Record if absent — not explicitly listed on GET in api_spec.",
        schema_check="api_spec PUT example includes name string; FR-04 lists name as updatable profile field.",
    ),
    case(
        id="TC-PROFILE-SCH-003", module="profile", api="GetProfile", method="GET", endpoint="/api/users/me",
        fr="FR-04", aspect="Field phone type", title="Profile phone field is string",
        preconditions=f"EShop at {BASE}. | {USER_LOGIN}.",
        steps=["GET /api/users/me.", "Assert typeof phone === 'string' when present."],
        expected="phone is present and typeof string. FR-04 phone format rule applies to value, not JSON type.",
        schema_check="api_spec PUT example phone:'0912345678' (string).",
    ),
    case(
        id="TC-PROFILE-SCH-004", module="profile", api="GetProfile", method="GET", endpoint="/api/users/me",
        fr="FR-04", aspect="Field shipping_address type", title="shipping_address field is string",
        preconditions=f"EShop at {BASE}. | {USER_LOGIN}.",
        steps=["GET /api/users/me.", "Assert typeof shipping_address === 'string' when present."],
        expected="shipping_address is present and typeof string.",
        schema_check="api_spec PUT example shipping_address string.",
    ),
    case(
        id="TC-PROFILE-SCH-005", module="profile", api="GetProfile", method="GET", endpoint="/api/users/me",
        fr="FR-04", aspect="Field email type", title="email field present as string",
        preconditions=f"EShop at {BASE}. | {USER_LOGIN}. | email=test@eshop.com.",
        steps=["GET /api/users/me.", "Assert email key exists and typeof string."],
        expected="email is string equal to test@eshop.com (FR-04: email immutable).",
        schema_check="FR-04: email must not change — implies email exposed on profile read.",
    ),
    case(
        id="TC-PROFILE-SCH-006", module="profile", api="GetProfile", method="GET", endpoint="/api/users/me",
        fr="FR-04", aspect="Field role type", title="role field is string",
        preconditions=f"EShop at {BASE}. | {USER_LOGIN}.",
        steps=["GET /api/users/me.", "Assert typeof role === 'string'."],
        expected="role is string with value user (FR-04 / SEC-06 immutability context).",
        schema_check="FR-04 forbids client role change — role must be readable.",
    ),
    case(
        id="TC-PROFILE-SCH-007", module="profile", api="GetProfile", method="GET", endpoint="/api/users/me",
        fr="FR-04 / SEC-01", aspect="Forbidden field password", title="GET profile must not expose password",
        preconditions=f"EShop at {BASE}. | {USER_LOGIN}.",
        steps=["GET /api/users/me.", "Assert no password or password_hash key in JSON object."],
        expected="Response object must not contain password or password_hash (SEC-01). Other fields may exist — record keys.",
        schema_check="SEC-01 README; api_spec does not document password on profile GET.",
    ),
    case(
        id="TC-PROFILE-SCH-008", module="profile", api="UpdateProfile", method="PUT", endpoint="/api/users/me",
        fr="FR-04", aspect="PUT request body schema", title="PUT accepts documented three-field JSON body",
        preconditions=f"EShop at {BASE}. | {USER_LOGIN}.",
        steps=[f"PUT /api/users/me body {VALID_BODY}.", "GET /api/users/me — verify name/phone/shipping_address strings updated."],
        expected="PUT succeeds per spec example shape (three string fields). GET reflects submitted string values. "
        f"{NO_HTTP}",
        schema_check="api_spec section 2.2 PUT body JSON example.",
        body={"name": "Nguyen Van A", "shipping_address": "123 Le Loi, Q1, TP.HCM", "phone": "0912345678"},
    ),
    case(
        id="TC-PROFILE-SCH-009", module="profile", api="UpdateProfile", method="PUT", endpoint="/api/users/me",
        fr="FR-04", aspect="PUT success response envelope", title="PUT success response is JSON object",
        preconditions=f"EShop at {BASE}. | {USER_LOGIN}.",
        steps=["PUT /api/users/me with valid documented body.", "Inspect response body JSON type and top-level keys."],
        expected=f"Response body is JSON object (not array/HTML). Field names/types not documented in api_spec — record actual. {NO_HTTP}",
        schema_check="Gap: api_spec section 2.2 does not document PUT success response envelope.",
        body={"name": "Schema Test Name", "shipping_address": "1 Schema St", "phone": "0912345678"},
    ),
    case(
        id="TC-PROFILE-SCH-010", module="profile", api="GetProfile", method="GET", endpoint="/api/users/me",
        fr="FR-04", aspect="Content-Type header", title="GET profile Content-Type is JSON",
        preconditions=f"EShop at {BASE}. | {USER_LOGIN}.",
        steps=["GET /api/users/me.", "Inspect Content-Type response header."],
        expected=CT_JSON,
        schema_check="Checklist section 4: Content-Type correctness.",
    ),
    case(
        id="TC-PROFILE-SCH-011", module="profile", api="UpdateProfile", method="PUT", endpoint="/api/users/me",
        fr="FR-04", aspect="Request field type coercion", title="phone sent as JSON number — observe type handling",
        preconditions=f"EShop at {BASE}. | {USER_LOGIN}.",
        steps=['PUT body {"name":"Nguyen Van A","shipping_address":"Addr","phone":912345678} (phone number not string).', "GET /api/users/me — record typeof phone."],
        expected="Spec example types phone as string. Record whether server coerces number to string, rejects, or stores number. "
        f"{NO_HTTP}",
        schema_check="api_spec example uses string phone; numeric type is schema deviation probe.",
        body={"name": "Nguyen Van A", "shipping_address": "Addr", "phone": 912345678},
    ),
    case(
        id="TC-PROFILE-SCH-012", module="profile", api="UpdateProfile", method="PUT", endpoint="/api/users/me",
        fr="FR-04", aspect="Empty PUT body", title="PUT with empty JSON object — observe response schema",
        preconditions=f"EShop at {BASE}. | {USER_LOGIN}. | Snapshot GET profile.",
        steps=["PUT /api/users/me with body {}.", "Inspect response JSON; GET profile."],
        expected="Response is JSON (object or documented error shape). Partial update semantics not specified — record GET field values. "
        f"{NO_HTTP}",
        schema_check="Required fields on PUT not stated in api_spec — observe-only.",
        body={},
    ),
    case(
        id="TC-PROFILE-SCH-013", module="profile", api="GetProfile", method="GET", endpoint="/api/users/me",
        fr="FR-04", aspect="Numeric id field", title="id field type if present on GET profile",
        preconditions=f"EShop at {BASE}. | {USER_LOGIN}.",
        steps=["GET /api/users/me.", "If id key exists, assert typeof id === 'number' (integer)."],
        expected="If id is returned, it must be JSON number (not string). If absent, record — not documented in api_spec GET.",
        schema_check="Login/register responses reference numeric id; profile GET schema silent.",
    ),
    case(
        id="TC-PROFILE-SCH-014", module="profile", api="GetProfile", method="GET", endpoint="/api/users/me",
        fr="FR-04 / SEC-02", aspect="Unauthenticated error body", title="GET without JWT — error body is JSON not HTML",
        preconditions=f"EShop at {BASE}.",
        steps=["GET /api/users/me without Authorization.", "Inspect body is parseable JSON or empty; must not be HTML stack trace page."],
        expected=f"Body must not be HTML error page with stack trace. If JSON error object, record keys (spec does not define auth error schema). {NO_HTTP}",
        schema_check="SEC-02 requires auth; error envelope undefined in api_spec.",
    ),
]

CART = [
    case(
        id="TC-CART-SCH-001", module="cart", api="GetCart", method="GET", endpoint="/api/cart",
        fr="FR-07", aspect="GET response root type", title="GET /api/cart returns JSON array",
        preconditions=f"EShop at {BASE}. | {USER_LOGIN}.",
        steps=["GET /api/cart.", "Assert Array.isArray(body) === true."],
        expected="Root body is JSON array (cart lines list). " + CT_JSON,
        schema_check="api_spec section 4.1 cart list — implied collection.",
    ),
    case(
        id="TC-CART-SCH-002", module="cart", api="GetCart", method="GET", endpoint="/api/cart",
        fr="FR-07", aspect="Empty cart shape", title="Empty cart is empty array []",
        preconditions=f"EShop at {BASE}. | {USER_LOGIN}. | Cart cleared or fresh user.",
        steps=["GET /api/cart on empty cart."],
        expected="Body equals JSON empty array [] (length 0), not null or {}.",
        schema_check="FR-07 empty-cart UI implies no lines — array envelope.",
    ),
    case(
        id="TC-CART-SCH-003", module="cart", api="AddToCart", method="POST", endpoint="/api/cart",
        fr="FR-07", aspect="Line item id type", title="Cart line id is number",
        preconditions=f"EShop at {BASE}. | {USER_LOGIN}. | One item in cart.",
        steps=["POST one item per api_spec example.", "GET /api/cart — first element typeof id === 'number'."],
        expected="Each line has id as JSON number per POST example (id:1).",
        schema_check="api_spec section 4.2 POST body id numeric.",
        body={"id": 1, "name": "San pham A", "price": 100000, "quantity": 2},
    ),
    case(
        id="TC-CART-SCH-004", module="cart", api="AddToCart", method="POST", endpoint="/api/cart",
        fr="FR-07", aspect="Line item name type", title="Cart line name is string",
        preconditions=f"EShop at {BASE}. | {USER_LOGIN}. | Item in cart.",
        steps=["GET /api/cart.", "Assert each line.name typeof string."],
        expected="name is string on every cart line object.",
        schema_check="api_spec POST example name string.",
    ),
    case(
        id="TC-CART-SCH-005", module="cart", api="AddToCart", method="POST", endpoint="/api/cart",
        fr="FR-07", aspect="Line item price type", title="Cart line price is number",
        preconditions=f"EShop at {BASE}. | {USER_LOGIN}. | Item in cart.",
        steps=["GET /api/cart.", "Assert each line.price typeof number."],
        expected="price is JSON number on each line (not string).",
        schema_check="api_spec POST example price:100000 number.",
    ),
    case(
        id="TC-CART-SCH-006", module="cart", api="AddToCart", method="POST", endpoint="/api/cart",
        fr="FR-07", aspect="Line item quantity type", title="Cart line quantity is number",
        preconditions=f"EShop at {BASE}. | {USER_LOGIN}. | Item in cart.",
        steps=["GET /api/cart.", "Assert each line.quantity typeof number."],
        expected="quantity is JSON number on each line.",
        schema_check="api_spec POST example quantity:2 number.",
    ),
    case(
        id="TC-CART-SCH-007", module="cart", api="AddToCart", method="POST", endpoint="/api/cart",
        fr="FR-07", aspect="POST success response envelope", title="POST /api/cart success response is JSON object",
        preconditions=f"EShop at {BASE}. | {USER_LOGIN}.",
        steps=["POST /api/cart with documented body.", "Inspect response JSON root type and keys."],
        expected=f"Response body is JSON object. Top-level fields not documented in api_spec — record names/types. {NO_HTTP}",
        schema_check="Gap: api_spec 4.2 documents request only, not POST success response.",
        body={"id": 1, "name": "San pham A", "price": 100000, "quantity": 1},
    ),
    case(
        id="TC-CART-SCH-008", module="cart", api="AddToCart", method="POST", endpoint="/api/cart",
        fr="FR-07", aspect="POST request four-field schema", title="POST body matches example four-field schema",
        preconditions=f"EShop at {BASE}. | {USER_LOGIN}.",
        steps=[f"POST body {CART_BODY}.", "GET /api/cart — line contains id,name,price,quantity keys."],
        expected="Stored line object includes all four keys from api_spec example with matching JSON types.",
        schema_check="api_spec section 4.2 POST JSON example.",
        body={"id": 1, "name": "San pham A", "price": 100000, "quantity": 2},
    ),
    case(
        id="TC-CART-SCH-009", module="cart", api="AddToCart", method="POST", endpoint="/api/cart",
        fr="FR-07", aspect="Array length after merge", title="Two POST same id — array length and qty schema",
        preconditions=f"EShop at {BASE}. | {USER_LOGIN}. | Empty cart.",
        steps=["POST id=1 qty=1 twice (merge).", "GET /api/cart — array length 1; quantity number >=2."],
        expected="Array has one object element; quantity is number reflecting merge (FR-07). id still number.",
        schema_check="FR-07 merge rule + line object shape from POST example.",
        input=json.dumps({"sequence": ["POST qty=1", "POST qty=1", "GET /api/cart"]}, ensure_ascii=False),
    ),
    case(
        id="TC-CART-SCH-010", module="cart", api="AddToCart", method="POST", endpoint="/api/cart",
        fr="FR-07", aspect="Request price string type", title="price sent as string — observe stored type",
        preconditions=f"EShop at {BASE}. | {USER_LOGIN}.",
        steps=['POST {"id":1,"name":"A","price":"100000","quantity":1}.', "GET /api/cart — record typeof price."],
        expected="Spec types price as number. Record coercion to number vs string storage. " + NO_HTTP,
        schema_check="Type deviation probe on documented price field.",
        body={"id": 1, "name": "A", "price": "100000", "quantity": 1},
    ),
    case(
        id="TC-CART-SCH-011", module="cart", api="GetCart", method="GET", endpoint="/api/cart",
        fr="FR-07", aspect="Content-Type header", title="GET cart Content-Type is JSON",
        preconditions=f"EShop at {BASE}. | {USER_LOGIN}.",
        steps=["GET /api/cart.", "Inspect Content-Type header."],
        expected=CT_JSON,
        schema_check="Checklist section 4 Content-Type.",
    ),
    case(
        id="TC-CART-SCH-012", module="cart", api="AddToCart", method="POST", endpoint="/api/cart",
        fr="FR-07", aspect="Malformed request root", title="POST body JSON array instead of object",
        preconditions=f"EShop at {BASE}. | {USER_LOGIN}.",
        steps=["POST /api/cart with raw body `[{\"id\":1}]` Content-Type application/json.", "Inspect response body type."],
        expected=f"Server rejects or ignores malformed root; response JSON or parse error — record shape. Cart unchanged on GET. {NO_HTTP}",
        schema_check="Request must be object per example; array root is schema violation.",
        input=json.dumps({"body_raw": '[{"id":1}]', "headers": {"Content-Type": "application/json"}}, ensure_ascii=False),
    ),
    case(
        id="TC-CART-SCH-013", module="cart", api="AddToCart", method="POST", endpoint="/api/cart",
        fr="FR-07", aspect="quantity string type", title="quantity sent as string — observe stored type",
        preconditions=f"EShop at {BASE}. | {USER_LOGIN}.",
        steps=['POST {"id":1,"name":"A","price":100000,"quantity":"2"}.', "GET — record typeof quantity."],
        expected="Spec types quantity as number. Record coercion behaviour. " + NO_HTTP,
        schema_check="Type deviation on documented quantity field.",
        body={"id": 1, "name": "A", "price": 100000, "quantity": "2"},
    ),
    case(
        id="TC-CART-SCH-014", module="cart", api="GetCart", method="GET", endpoint="/api/cart",
        fr="FR-07 / SEC-02", aspect="Unauthenticated error body", title="GET cart without JWT — response body shape",
        preconditions=f"EShop at {BASE}.",
        steps=["GET /api/cart without Authorization.", "Record whether body is JSON object/array vs HTML."],
        expected=f"Must not return cart array without auth. Error body schema not specified — record parseable JSON keys if any. {NO_HTTP}",
        schema_check="SEC-02 + api_spec section 4 auth note.",
    ),
]

ADMIN = [
    case(
        id="TC-ADMINUSERS-SCH-001", module="admin-users", api="AdminListUsers", method="GET", endpoint="/api/admin/users",
        fr="FR-19", aspect="GET list root type", title="GET /api/admin/users returns JSON array",
        preconditions=f"EShop at {BASE}. | {ADMIN_LOGIN}.",
        steps=["GET /api/admin/users.", "Assert Array.isArray(body)."],
        expected="Root is JSON array of users. " + CT_JSON,
        schema_check="api_spec section 6.1 user list.",
    ),
    case(
        id="TC-ADMINUSERS-SCH-002", module="admin-users", api="AdminListUsers", method="GET", endpoint="/api/admin/users",
        fr="FR-19", aspect="List element type", title="Each list element is JSON object",
        preconditions=f"EShop at {BASE}. | {ADMIN_LOGIN}.",
        steps=["GET /api/admin/users.", "For each element assert typeof object and not array."],
        expected="Every array element is plain JSON object (user record).",
        schema_check="List of user objects implied by FR-19 admin user management.",
    ),
    case(
        id="TC-ADMINUSERS-SCH-003", module="admin-users", api="AdminListUsers", method="GET", endpoint="/api/admin/users",
        fr="FR-19", aspect="Field id type", title="User list item id is number",
        preconditions=f"EShop at {BASE}. | {ADMIN_LOGIN}.",
        steps=["GET /api/admin/users.", "Pick first user — typeof id === 'number'."],
        expected="id is JSON number on list items.",
        schema_check="Register response documents numeric id; list items expected consistent.",
    ),
    case(
        id="TC-ADMINUSERS-SCH-004", module="admin-users", api="AdminListUsers", method="GET", endpoint="/api/admin/users",
        fr="FR-19", aspect="Field name type", title="User list item name is string",
        preconditions=f"EShop at {BASE}. | {ADMIN_LOGIN}.",
        steps=["GET /api/admin/users.", "Assert each user.name typeof string when present."],
        expected="name is string on each user object.",
        schema_check="User entity name from register example.",
    ),
    case(
        id="TC-ADMINUSERS-SCH-005", module="admin-users", api="AdminListUsers", method="GET", endpoint="/api/admin/users",
        fr="FR-19", aspect="Field email type", title="User list item email is string",
        preconditions=f"EShop at {BASE}. | {ADMIN_LOGIN}.",
        steps=["GET /api/admin/users.", "Assert each user.email typeof string."],
        expected="email is string on each user object.",
        schema_check="Login/register email string; admin list exposes users.",
    ),
    case(
        id="TC-ADMINUSERS-SCH-006", module="admin-users", api="AdminListUsers", method="GET", endpoint="/api/admin/users",
        fr="FR-19", aspect="Field role type", title="User list item role is string",
        preconditions=f"EShop at {BASE}. | {ADMIN_LOGIN}.",
        steps=["GET /api/admin/users.", "Assert each user.role typeof string in {user,admin}."],
        expected="role is string (user or admin per FR-12).",
        schema_check="FR-12 role=admin for admin APIs implies role field on user records.",
    ),
    case(
        id="TC-ADMINUSERS-SCH-007", module="admin-users", api="AdminListUsers", method="GET", endpoint="/api/admin/users",
        fr="FR-19 / SEC-01", aspect="Forbidden password field", title="List items must not contain password",
        preconditions=f"EShop at {BASE}. | {ADMIN_LOGIN}.",
        steps=["GET /api/admin/users.", "For each object assert password key absent."],
        expected="No password key on any list element (FR-19 / SEC-01).",
        schema_check="FR-19: list must not expose password.",
    ),
    case(
        id="TC-ADMINUSERS-SCH-008", module="admin-users", api="AdminListUsers", method="GET", endpoint="/api/admin/users",
        fr="FR-19 / SEC-01", aspect="Forbidden password_hash field", title="List items must not contain password_hash",
        preconditions=f"EShop at {BASE}. | {ADMIN_LOGIN}.",
        steps=["GET /api/admin/users.", "Assert password_hash absent on all elements."],
        expected="No password_hash key on any list element.",
        schema_check="SEC-01 no plaintext — hash also must not leak in API list.",
    ),
    case(
        id="TC-ADMINUSERS-SCH-009", module="admin-users", api="AdminDeleteUser", method="DELETE", endpoint="/api/admin/users/:id",
        fr="FR-19", aspect="DELETE success response type", title="DELETE success body is JSON object",
        preconditions=f"EShop at {BASE}. | {ADMIN_LOGIN}. | Register disposable D.",
        steps=["DELETE /api/admin/users/D.", "Parse response as JSON object."],
        expected=f"Response body is JSON object (not HTML/array). Field schema not in api_spec — record keys/types. {NO_HTTP}",
        schema_check="Gap: api_spec 6.1 DELETE response undocumented.",
        input=json.dumps({"path": {"id": "<D>"}}, ensure_ascii=False),
    ),
    case(
        id="TC-ADMINUSERS-SCH-010", module="admin-users", api="AdminDeleteUser", method="DELETE", endpoint="/api/admin/users/:id",
        fr="FR-19", aspect="DELETE message field", title="DELETE response message field type if present",
        preconditions=f"EShop at {BASE}. | {ADMIN_LOGIN}. | Disposable D.",
        steps=["DELETE D.", "If message key exists, assert typeof message === 'string'."],
        expected="If response includes message, it is string. If absent, record — not required by written spec.",
        schema_check="Observe-only; compare with register success {message,id} pattern.",
        input=json.dumps({"path": {"id": "<D>"}}, ensure_ascii=False),
    ),
    case(
        id="TC-ADMINUSERS-SCH-011", module="admin-users", api="AdminListUsers", method="GET", endpoint="/api/admin/users",
        fr="FR-19", aspect="Non-empty list schema", title="Seed users appear as valid objects in list",
        preconditions=f"EShop at {BASE}. | {ADMIN_LOGIN}.",
        steps=["GET /api/admin/users.", "Find email admin@eshop.com and test@eshop.com entries — schema check each."],
        expected="List length >= 2. Seed users are objects with string email and string role.",
        schema_check="SUT seed data; validates list schema on real records.",
    ),
    case(
        id="TC-ADMINUSERS-SCH-012", module="admin-users", api="AdminListUsers", method="GET", endpoint="/api/admin/users",
        fr="FR-19", aspect="Content-Type header", title="GET admin users Content-Type is JSON",
        preconditions=f"EShop at {BASE}. | {ADMIN_LOGIN}.",
        steps=["GET /api/admin/users.", "Inspect Content-Type."],
        expected=CT_JSON,
        schema_check="Checklist section 4.",
    ),
    case(
        id="TC-ADMINUSERS-SCH-013", module="admin-users", api="AdminListUsers", method="GET", endpoint="/api/admin/users",
        fr="FR-19 / FR-12", aspect="User JWT error body", title="GET list as user — error response JSON shape",
        preconditions=f"EShop at {BASE}. | {USER_LOGIN}.",
        steps=["GET /api/admin/users with user JWT.", "Record response body JSON type and keys."],
        expected=f"Must not return full admin user array. Error envelope not specified — record JSON vs HTML. {NO_HTTP}",
        schema_check="FR-12 admin-only API; error schema gap in api_spec.",
    ),
    case(
        id="TC-ADMINUSERS-SCH-014", module="admin-users", api="AdminDeleteUser", method="DELETE", endpoint="/api/admin/users/:id",
        fr="FR-19", aspect="List schema after delete", title="After DELETE, list remains array of valid user objects",
        preconditions=f"EShop at {BASE}. | {ADMIN_LOGIN}. | Register D.",
        steps=["DELETE D.", "GET /api/admin/users.", "Assert array; no element with id===D; remaining elements pass object schema."],
        expected="GET still JSON array. Deleted id absent. Remaining items retain id(number), email(string), role(string).",
        schema_check="DELETE effect on list collection schema.",
        input=json.dumps({"sequence": ["DELETE D", "GET /api/admin/users"]}, ensure_ascii=False),
    ),
]

ALL = PROFILE + CART + ADMIN


def build_report() -> str:
    aspect_map: dict[str, list[str]] = {}
    for c in ALL:
        aspect_map.setdefault(c["aspect"].split()[0], []).append(c["id"])

    lines = [
        "# Schema Validation Report — FR-04, FR-07, FR-19",
        "",
        f"**Student:** 23127271 · **SUT:** EShop (`{BASE}`)  ",
        "**Category:** Stage 1 — Schema validation (API testing skill checklist section 4)  ",
        "**Sources:** `Repo/eshop-sut/api_specification.md`, `README.md` (FR-04/07/19, SEC-01)",
        "",
        "---",
        "",
        "## Schema contract sources",
        "",
        "| Source | What it defines for schema tests |",
        "|--------|----------------------------------|",
        "| api_spec §2.2 | PUT `/api/users/me` request: name, shipping_address, phone (strings) |",
        "| api_spec §4.2 | POST `/api/cart` request: id, name, price, quantity (number/string types per example) |",
        "| api_spec §4.1 / §6.1 | GET cart array; GET admin users list (shapes partially implied) |",
        "| FR-04 README | Profile fields; email/role readable and immutable |",
        "| FR-19 README | Admin user list without password |",
        "| SEC-01 | password/password_hash must not appear in responses |",
        "",
        "**Documented gaps (observe-only oracles):** PUT profile success body, POST cart success body, DELETE user success body, and auth error envelopes are **not** defined in api_spec — TCs record actual JSON types/keys without inventing required status codes.",
        "",
        "## In-scope endpoints",
        "",
        "| FR | Endpoints | Schema focus |",
        "|----|-----------|--------------|",
        "| FR-04 | `GET/PUT /api/users/me` | Profile object fields/types; PUT request body; forbidden password |",
        "| FR-07 | `GET/POST /api/cart` | Array of line objects; four-field line schema; Content-Type |",
        "| FR-19 | `GET/DELETE /api/admin/users` | User list array schema; no password fields; DELETE response observe |",
        "",
        "---",
        "",
        "## FR-04 — `GET/PUT /api/users/me`",
        "",
        f"**Count:** {len(PROFILE)} cases",
        "",
        "| TC ID | Aspect | Title |",
        "|-------|--------|-------|",
    ]
    for c in PROFILE:
        lines.append(f"| {c['id']} | {c['aspect']} | {c['title']} |")

    lines += ["", "---", "", "## FR-07 — `GET/POST /api/cart`", "", f"**Count:** {len(CART)} cases", "", "| TC ID | Aspect | Title |", "|-------|--------|-------|"]
    for c in CART:
        lines.append(f"| {c['id']} | {c['aspect']} | {c['title']} |")

    lines += ["", "---", "", "## FR-19 — `GET/DELETE /api/admin/users`", "", f"**Count:** {len(ADMIN)} cases", "", "| TC ID | Aspect | Title |", "|-------|--------|-------|"]
    for c in ADMIN:
        lines.append(f"| {c['id']} | {c['aspect']} | {c['title']} |")

    total = len(ALL)
    lines += [
        "",
        "---",
        "",
        "## Combined Stage-1 counts (domain + state + security + schema)",
        "",
        f"- FR-04: 40 + 12 + 14 + 5 + {len(PROFILE)} = **{40 + 12 + 14 + 5 + len(PROFILE)}**",
        f"- FR-07: 39 + 15 + 11 + 5 + {len(CART)} = **{39 + 15 + 11 + 5 + len(CART)}**",
        f"- FR-19: 20 + 15 + 12 + 5 + {len(ADMIN)} = **{20 + 15 + 12 + 5 + len(ADMIN)}**",
        "",
        "## Artifacts",
        "",
        "| Artifact | Path |",
        "|----------|------|",
        "| This report | `docs/schema-validation-report.md` |",
        "| Per-TC files | `tests/test-cases/{{profile,cart,admin-users}}/TC-*-SCH-*.md` |",
        "| Sheet | `sheets/schema-validation.csv` |",
        "| Generator | `scripts/generate_schema_validation.py` |",
        "",
        f"**Total schema cases:** {total} AI-generated.",
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
    print(f"Wrote {len(ALL)} schema validation cases")
    print(f"  PROFILE: {len(PROFILE)}")
    print(f"  CART: {len(CART)}")
    print(f"  ADMINUSERS: {len(ADMIN)}")
    print(f"Sheet: {SHEET}")
    print(f"Report: {REPORT}")


if __name__ == "__main__":
    main()
