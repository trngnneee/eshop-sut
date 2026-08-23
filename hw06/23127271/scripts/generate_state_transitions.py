#!/usr/bin/env python3
"""Generate Stage-1 state-transition artifacts for FR-04 / FR-07 / FR-19."""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TC_ROOT = ROOT / "tests" / "test-cases"
SHEET = ROOT / "sheets" / "state-transitions.csv"
REPORT = ROOT / "docs" / "state-transition-report.md"

BASE = "http://localhost:3000"
USER_LOGIN = "POST /api/login email=test@eshop.com password=Test1234!"
ADMIN_LOGIN = "POST /api/login email=admin@eshop.com password=Admin123!"

PROFILE_BODY = {
    "name": "Nguyen Van A",
    "shipping_address": "123 Le Loi, Q1, TP.HCM",
    "phone": "0912345678",
}
CART_ITEM_1 = {
    "id": 1,
    "name": "iPhone 15 Pro Max",
    "price": 30000000,
    "quantity": 1,
}
CART_ITEM_2 = {
    "id": 2,
    "name": "MacBook Pro M3",
    "price": 45000000,
    "quantity": 1,
}


def steps_md(steps: list[str]) -> str:
    return "\n".join(f"{i}. {s}" for i, s in enumerate(steps, 1))


def write_tc(module: str, case: dict) -> Path:
    tc_id = case["id"]
    path = TC_ROOT / module / f"{tc_id}.md"
    pre = case["preconditions"]
    if isinstance(pre, list):
        pre_block = "\n".join(f"- {p}" for p in pre)
    else:
        pre_block = f"- {pre}"

    td_rows = case.get("test_data", [])
    td_block = ""
    if td_rows:
        td_block = "| Field | Value |\n|-------|-------|\n" + "\n".join(
            f"| {k} | {v} |" for k, v in td_rows
        )

    content = f"""# {tc_id}: {case["title"]}

## Requirement ID
{case["fr"]}

## Module / Test type / Technique
{module} / Functional / State Transition Testing

## State machine
{case["sm_ref"]}

## Transition under test
{case["transition"]}

## Preconditions
{pre_block}

## Test data
{td_block or "| (see steps — multi-step sequence) | |"}

## Test steps
{steps_md(case["steps"])}

## Expected result
{case["expected"]}

## States / transitions covered
{case["states"]}

## Type
{case["type"]}

## Status / Related bugs
Not Run / None
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def row(case: dict) -> dict:
    return {
        "TestCaseID": case["id"],
        "API": case["api"],
        "Method": case["method"],
        "Endpoint": case["endpoint"],
        "Category": "StateTransition",
        "Preconditions": " | ".join(case["preconditions"])
        if isinstance(case["preconditions"], list)
        else case["preconditions"],
        "Input": json.dumps(case["input"], ensure_ascii=False),
        "ExpectedResult": case["expected"].replace("\n", " "),
        "Priority": case.get("priority", "High"),
        "Source": "AI",
        "AuditStatus": "",
        "AuditReasoning": "",
        "ActualResult": "",
        "PassFail": "",
        "BugRef": "",
        "Notes": f"Transition={case['transition']} | States={case['states']} | File=tests/test-cases/{case['module']}/{case['id']}.md",
    }


# ---------------------------------------------------------------------------
# FR-04 — Profile snapshot state (PUT /api/users/me)
# ---------------------------------------------------------------------------

PROFILE_CASES = [
    {
        "id": "TC-PROFILE-ST-001",
        "module": "profile",
        "fr": "FR-04",
        "api": "UpdateProfile",
        "method": "PUT",
        "endpoint": "/api/users/me",
        "title": "Seed profile → full update → verified snapshot",
        "sm_ref": "P0 (seed) → P1 (updated) via valid full PUT",
        "transition": "P0 → P1",
        "preconditions": [
            f"EShop backend at {BASE}.",
            USER_LOGIN,
            "GET /api/users/me → snapshot P0 (name, phone, shipping_address, email, role).",
        ],
        "steps": [
            "PUT /api/users/me with name, phone, shipping_address (FR-04-valid).",
            "GET /api/users/me.",
        ],
        "expected": (
            "GET shows submitted name, phone, shipping_address (P1). email and role unchanged from P0 (FR-04 / SEC-06). "
            "Success status/body not specified."
        ),
        "states": "P0→P1",
        "type": "Legal",
        "input": {"sequence": ["PUT /api/users/me full body", "GET /api/users/me"]},
    },
    {
        "id": "TC-PROFILE-ST-002",
        "module": "profile",
        "fr": "FR-04",
        "api": "UpdateProfile",
        "method": "PUT",
        "endpoint": "/api/users/me",
        "title": "Sequential partial updates — name then phone",
        "sm_ref": "P0 → P1a (name) → P1b (name+phone)",
        "transition": "P0 → P1a → P1b",
        "preconditions": [f"EShop at {BASE}.", USER_LOGIN, "Snapshot P0 via GET /api/users/me."],
        "steps": [
            'PUT /api/users/me body {"name":"Updated Name Only"}.',
            'PUT /api/users/me body {"phone":"0987654321"}.',
            "GET /api/users/me.",
        ],
        "expected": (
            "GET shows name=Updated Name Only and phone=0987654321 if both applied. "
            "shipping_address behaviour after partial PUTs not specified — record P0 vs cleared vs unchanged. email/role unchanged."
        ),
        "states": "P0→P1a→P1b",
        "type": "Legal / Unspecified",
        "input": {"sequence": ["PUT name only", "PUT phone only", "GET"]},
    },
    {
        "id": "TC-PROFILE-ST-003",
        "module": "profile",
        "fr": "FR-04",
        "api": "UpdateProfile",
        "method": "PUT",
        "endpoint": "/api/users/me",
        "title": "Second full PUT overwrites first update",
        "sm_ref": "P0 → P1 → P2 (full overwrite)",
        "transition": "P1 → P2",
        "preconditions": [f"EShop at {BASE}.", USER_LOGIN, "P0 snapshot taken."],
        "steps": [
            "PUT /api/users/me set A (name A, phone A, address A). GET → P1.",
            "PUT /api/users/me set B (name B, phone B, address B).",
            "GET /api/users/me.",
        ],
        "expected": "GET shows set B only (P2). Set A values must not remain. email/role unchanged.",
        "states": "P0→P1→P2",
        "type": "Legal",
        "input": {"sequence": ["PUT set A", "GET", "PUT set B", "GET"]},
    },
    {
        "id": "TC-PROFILE-ST-004",
        "module": "profile",
        "fr": "FR-04",
        "api": "UpdateProfile",
        "method": "PUT",
        "endpoint": "/api/users/me",
        "title": "Idempotent — identical PUT twice leaves stable P1",
        "sm_ref": "P0 → P1 → P1 (idempotent)",
        "transition": "P1 → P1",
        "preconditions": [f"EShop at {BASE}.", USER_LOGIN],
        "steps": [
            "PUT /api/users/me with valid full body (set V).",
            "PUT /api/users/me with identical body (set V) again.",
            "GET /api/users/me twice.",
        ],
        "expected": "Both GETs show set V. No corruption or drift between reads.",
        "states": "P0→P1→P1",
        "type": "Legal (idempotency)",
        "input": {"sequence": ["PUT V", "PUT V", "GET", "GET"]},
    },
    {
        "id": "TC-PROFILE-ST-005",
        "module": "profile",
        "fr": "FR-04",
        "api": "UpdateProfile",
        "method": "PUT",
        "endpoint": "/api/users/me",
        "title": "Profile persists across re-login",
        "sm_ref": "P0 → P1 → (new session) → P1",
        "transition": "session boundary",
        "preconditions": [f"EShop at {BASE}."],
        "steps": [
            "Login as test@eshop.com. PUT /api/users/me (set V). GET → P1.",
            "POST /api/login again (new token). GET /api/users/me.",
        ],
        "expected": "New session GET still shows P1 (set V). Profile is persisted, not token-scoped only.",
        "states": "P0→P1→P1",
        "type": "Legal",
        "input": {"sequence": ["login", "PUT", "login", "GET"]},
    },
    {
        "id": "TC-PROFILE-ST-006",
        "module": "profile",
        "fr": "FR-04",
        "api": "UpdateProfile",
        "method": "PUT",
        "endpoint": "/api/users/me",
        "title": "email immutable through profile update transition",
        "sm_ref": "P0 → PUT(with email) → P1, email stays P0.email",
        "transition": "immutable email",
        "preconditions": [f"EShop at {BASE}.", USER_LOGIN, "P0 email=test@eshop.com."],
        "steps": [
            'PUT /api/users/me with valid fields plus "email":"attacker@evil.com".',
            "GET /api/users/me.",
        ],
        "expected": "email remains test@eshop.com. Other fields may update per FR-04. Request rejected or email ignored — either way email unchanged.",
        "states": "P0→P1 (email locked)",
        "type": "Legal constraint",
        "input": {"body": {**PROFILE_BODY, "email": "attacker@evil.com"}},
    },
    {
        "id": "TC-PROFILE-ST-007",
        "module": "profile",
        "fr": "FR-04 / SEC-06",
        "api": "UpdateProfile",
        "method": "PUT",
        "endpoint": "/api/users/me",
        "title": "role immutable through profile update chain",
        "sm_ref": "P0(user) → PUT(+role=admin) → P1, role stays user",
        "transition": "immutable role",
        "preconditions": [f"EShop at {BASE}.", USER_LOGIN, "P0 role=user."],
        "steps": [
            'PUT /api/users/me valid fields plus "role":"admin".',
            "GET /api/users/me.",
        ],
        "expected": "role remains user (SEC-06 / FR-04). Documented profile fields may still update.",
        "states": "P0→P1 (role locked)",
        "type": "Legal constraint",
        "input": {"body": {**PROFILE_BODY, "role": "admin"}},
    },
    {
        "id": "TC-PROFILE-ST-008",
        "module": "profile",
        "fr": "FR-04",
        "api": "UpdateProfile",
        "method": "PUT",
        "endpoint": "/api/users/me",
        "title": "Admin profile update — role stays admin",
        "sm_ref": "P0(admin) → P1 → role=admin",
        "transition": "admin P0→P1",
        "preconditions": [f"EShop at {BASE}.", ADMIN_LOGIN, "GET P0 role=admin."],
        "steps": [
            'PUT /api/users/me {"name":"Admin Updated","phone":"0911111111","shipping_address":"Admin HQ"}.',
            "GET /api/users/me.",
        ],
        "expected": "Profile fields updated. role still admin.",
        "states": "P0(admin)→P1(admin)",
        "type": "Legal",
        "input": {"sequence": ["PUT admin profile", "GET"]},
    },
    {
        "id": "TC-PROFILE-ST-009",
        "module": "profile",
        "fr": "FR-04",
        "api": "UpdateProfile",
        "method": "PUT",
        "endpoint": "/api/users/me",
        "title": "Three single-field transitions accumulate (or last-wins per field)",
        "sm_ref": "P0 → P(name) → P(phone) → P(address)",
        "transition": "multi partial chain",
        "preconditions": [f"EShop at {BASE}.", USER_LOGIN],
        "steps": [
            'PUT {"name":"Step Name"}.',
            'PUT {"phone":"0909090909"}.',
            'PUT {"shipping_address":"99 Pasteur, Q3"}.',
            "GET /api/users/me.",
        ],
        "expected": (
            "GET shows Step Name, 0909090909, 99 Pasteur if each partial update applies. "
            "If earlier fields revert when omitted, record actual partial-vs-replace semantics."
        ),
        "states": "P0→P(n)→P(np)→P(npa)",
        "type": "Legal / Unspecified",
        "input": {"sequence": ["PUT name", "PUT phone", "PUT address", "GET"]},
    },
    {
        "id": "TC-PROFILE-ST-010",
        "module": "profile",
        "fr": "FR-04",
        "api": "UpdateProfile",
        "method": "PUT",
        "endpoint": "/api/users/me",
        "title": "Invalid phone after valid update — state rollback unspecified",
        "sm_ref": "P0 → P1(valid) → PUT(invalid phone) → ?",
        "transition": "invalid transition attempt",
        "preconditions": [f"EShop at {BASE}.", USER_LOGIN, "Reach P1 with valid full PUT."],
        "steps": [
            "PUT /api/users/me valid full body → P1.",
            'PUT /api/users/me {"name":"Still Valid","shipping_address":"Addr","phone":"123"}.',
            "GET /api/users/me.",
        ],
        "expected": (
            "phone=123 violates FR-04. If rejected, GET should still show P1 phone (no partial invalid persist). "
            "Validation status not specified — record 4xx vs silent accept."
        ),
        "states": "P1→P1 or P1→invalid",
        "type": "Illegal input / Unspecified",
        "input": {"sequence": ["PUT valid", "PUT invalid phone", "GET"]},
    },
    {
        "id": "TC-PROFILE-ST-011",
        "module": "profile",
        "fr": "FR-04",
        "api": "UpdateProfile",
        "method": "PUT",
        "endpoint": "/api/users/me",
        "title": "User A update does not change User B profile (isolation)",
        "sm_ref": "PA0→PA1 while PB0 unchanged",
        "transition": "cross-user isolation",
        "preconditions": [
            f"EShop at {BASE}.",
            "Users test@eshop.com and admin@eshop.com exist.",
            "Snapshot PB0 for admin via admin login GET /api/users/me.",
        ],
        "steps": [
            "Login test@eshop.com. PUT /api/users/me (set V user). GET → PA1.",
            "Login admin@eshop.com. GET /api/users/me → PB1.",
        ],
        "expected": "PB1 equals PB0 (admin profile not affected by user A PUT). PA1 shows set V.",
        "states": "PA0→PA1, PB0→PB0",
        "type": "Legal (isolation)",
        "input": {"sequence": ["user PUT", "admin GET"]},
    },
    {
        "id": "TC-PROFILE-ST-012",
        "module": "profile",
        "fr": "FR-04",
        "api": "UpdateProfile",
        "method": "PUT",
        "endpoint": "/api/users/me",
        "title": "Empty body PUT — profile state unchanged",
        "sm_ref": "P0 → PUT({}) → P0",
        "transition": "no-op / reject",
        "preconditions": [f"EShop at {BASE}.", USER_LOGIN, "Snapshot P0."],
        "steps": [
            "PUT /api/users/me with empty JSON object {}.",
            "GET /api/users/me.",
        ],
        "expected": "GET matches P0 (no unintended wipe). Request may be rejected — if so, state unchanged.",
        "states": "P0→P0",
        "type": "Illegal / no-op",
        "input": {"body": {}},
    },
]

# ---------------------------------------------------------------------------
# FR-07 — Cart line-item state (POST /api/cart, observe via GET /api/cart)
# ---------------------------------------------------------------------------

CART_CASES = [
    {
        "id": "TC-CART-ST-001",
        "module": "cart",
        "fr": "FR-07",
        "api": "AddToCart",
        "method": "POST",
        "endpoint": "/api/cart",
        "title": "EMPTY → SINGLE — first add creates one line",
        "sm_ref": "C_EMPTY → C_SINGLE",
        "transition": "C_EMPTY → C_SINGLE",
        "preconditions": [f"EShop at {BASE}.", USER_LOGIN, "GET /api/cart → [] (empty)."],
        "steps": ["POST /api/cart id=1 qty=1.", "GET /api/cart."],
        "expected": "GET shows exactly one line id=1 qty=1. C_SINGLE reached.",
        "states": "C_EMPTY→C_SINGLE",
        "type": "Legal",
        "input": {"body": CART_ITEM_1},
    },
    {
        "id": "TC-CART-ST-002",
        "module": "cart",
        "fr": "FR-07",
        "api": "AddToCart",
        "method": "POST",
        "endpoint": "/api/cart",
        "title": "SINGLE → MERGED — same product increases quantity",
        "sm_ref": "C_SINGLE → C_MERGED (FR-07 merge rule)",
        "transition": "C_SINGLE → C_MERGED",
        "preconditions": [f"EShop at {BASE}.", USER_LOGIN, "Cart has id=1 qty=1."],
        "steps": ["POST /api/cart id=1 qty=1 again.", "GET /api/cart."],
        "expected": "One line id=1 qty=2. No second row (FR-07).",
        "states": "C_SINGLE→C_MERGED",
        "type": "Legal",
        "input": {"sequence": ["POST same id", "GET"]},
    },
    {
        "id": "TC-CART-ST-003",
        "module": "cart",
        "fr": "FR-07",
        "api": "AddToCart",
        "method": "POST",
        "endpoint": "/api/cart",
        "title": "SINGLE → TWO_LINES — different product adds new row",
        "sm_ref": "C_SINGLE → C_MULTI(2)",
        "transition": "C_SINGLE → C_TWO",
        "preconditions": [f"EShop at {BASE}.", USER_LOGIN, "Cart has id=1 qty=1."],
        "steps": ["POST /api/cart id=2 qty=1.", "GET /api/cart."],
        "expected": "Two lines: id=1 qty=1 unchanged, id=2 qty=1 added.",
        "states": "C_SINGLE→C_TWO",
        "type": "Legal",
        "input": {"body": CART_ITEM_2},
    },
    {
        "id": "TC-CART-ST-004",
        "module": "cart",
        "fr": "FR-07",
        "api": "AddToCart",
        "method": "POST",
        "endpoint": "/api/cart",
        "title": "TWO_LINES → merge on line 1, line 2 unchanged",
        "sm_ref": "C_TWO → C_TWO(merged L1)",
        "transition": "C_TWO → C_TWO'",
        "preconditions": [f"EShop at {BASE}.", USER_LOGIN, "Cart: id=1 qty=1, id=2 qty=1."],
        "steps": ["POST /api/cart id=1 qty=2.", "GET /api/cart."],
        "expected": "id=1 qty=3 (1+2 merged). id=2 qty=1 unchanged. Still two lines total.",
        "states": "C_TWO→C_TWO'",
        "type": "Legal",
        "input": {"sequence": ["POST id=1 qty=2", "GET"]},
    },
    {
        "id": "TC-CART-ST-005",
        "module": "cart",
        "fr": "FR-07",
        "api": "AddToCart",
        "method": "POST",
        "endpoint": "/api/cart",
        "title": "TWO_LINES → THREE_LINES — third distinct product",
        "sm_ref": "C_TWO → C_THREE",
        "transition": "C_TWO → C_THREE",
        "preconditions": [f"EShop at {BASE}.", USER_LOGIN, "Cart: id=1 and id=2 each qty=1."],
        "steps": ["POST /api/cart id=3 qty=1 (seed product 3).", "GET /api/cart."],
        "expected": "Three distinct lines. Prior lines unchanged except new id=3 line added.",
        "states": "C_TWO→C_THREE",
        "type": "Legal",
        "input": {"body": {"id": 3, "name": "AirPods Pro 2", "price": 5990000, "quantity": 1}},
    },
    {
        "id": "TC-CART-ST-006",
        "module": "cart",
        "fr": "FR-07",
        "api": "AddToCart",
        "method": "POST",
        "endpoint": "/api/cart",
        "title": "EMPTY → two POST same id → one merged line (not two rows)",
        "sm_ref": "C_EMPTY → C_MERGED via double POST",
        "transition": "C_EMPTY → C_MERGED",
        "preconditions": [f"EShop at {BASE}.", USER_LOGIN, "Empty cart."],
        "steps": [
            "POST /api/cart id=1 qty=1.",
            "POST /api/cart id=1 qty=1.",
            "GET /api/cart.",
        ],
        "expected": "Exactly one line id=1 qty=2 after both POSTs (FR-07 merge from empty).",
        "states": "C_EMPTY→C_MERGED",
        "type": "Legal",
        "input": {"sequence": ["POST", "POST", "GET"]},
    },
    {
        "id": "TC-CART-ST-007",
        "module": "cart",
        "fr": "FR-07",
        "api": "AddToCart",
        "method": "POST",
        "endpoint": "/api/cart",
        "title": "MERGED qty=5 → add 3 → qty=8",
        "sm_ref": "C_MERGED(5) → C_MERGED(8)",
        "transition": "quantity accumulation",
        "preconditions": [f"EShop at {BASE}.", USER_LOGIN, "Cart id=1 qty=5."],
        "steps": ["POST /api/cart id=1 qty=3.", "GET /api/cart."],
        "expected": "One line id=1 qty=8.",
        "states": "C_MERGED(5)→C_MERGED(8)",
        "type": "Legal",
        "input": {"sequence": ["POST qty=3", "GET"]},
    },
    {
        "id": "TC-CART-ST-008",
        "module": "cart",
        "fr": "FR-07",
        "api": "AddToCart",
        "method": "POST",
        "endpoint": "/api/cart",
        "title": "Idempotent POST from SINGLE — merged not duplicated",
        "sm_ref": "C_SINGLE → C_MERGED (repeat identical POST)",
        "transition": "idempotent add",
        "preconditions": [f"EShop at {BASE}.", USER_LOGIN, "Cart id=1 qty=2."],
        "steps": [
            "POST /api/cart identical body id=1 qty=2.",
            "GET /api/cart.",
        ],
        "expected": "One line id=1 qty=4 (2+2) if merge applies. Never two rows for id=1.",
        "states": "C_SINGLE→C_MERGED",
        "type": "Legal",
        "input": {"sequence": ["POST duplicate", "GET"]},
    },
    {
        "id": "TC-CART-ST-009",
        "module": "cart",
        "fr": "FR-07",
        "api": "AddToCart",
        "method": "POST",
        "endpoint": "/api/cart",
        "title": "Interleaved POST/GET — state stable between reads",
        "sm_ref": "C_EMPTY → POST → GET → POST → GET",
        "transition": "observable consistency",
        "preconditions": [f"EShop at {BASE}.", USER_LOGIN, "Empty cart."],
        "steps": [
            "POST id=1 qty=1. GET (expect qty=1).",
            "POST id=2 qty=1. GET (expect two lines).",
        ],
        "expected": "Each GET reflects all prior POSTs. No phantom reset between steps.",
        "states": "C_EMPTY→C_SINGLE→C_TWO",
        "type": "Legal",
        "input": {"sequence": ["POST", "GET", "POST", "GET"]},
    },
    {
        "id": "TC-CART-ST-010",
        "module": "cart",
        "fr": "FR-07",
        "api": "AddToCart",
        "method": "POST",
        "endpoint": "/api/cart",
        "title": "User A cart isolated from User B",
        "sm_ref": "CA evolves; CB unchanged",
        "transition": "cross-user isolation",
        "preconditions": [f"EShop at {BASE}.", "test@eshop.com and admin@eshop.com exist."],
        "steps": [
            "Login test@eshop.com. POST id=1. GET → CA1.",
            "Login admin@eshop.com. GET /api/cart → CB.",
        ],
        "expected": "CB empty or admin's own cart only — must not contain user A's line.",
        "states": "CA: C_EMPTY→C_SINGLE; CB: unchanged",
        "type": "Legal (isolation)",
        "input": {"sequence": ["user POST", "admin GET"]},
    },
    {
        "id": "TC-CART-ST-011",
        "module": "cart",
        "fr": "FR-07 / FR-08",
        "api": "AddToCart",
        "method": "POST",
        "endpoint": "/api/cart",
        "title": "MULTI → checkout → EMPTY (FR-08 clears cart)",
        "sm_ref": "C_MULTI → C_EMPTY after successful checkout",
        "transition": "C_MULTI → C_EMPTY",
        "preconditions": [f"EShop at {BASE}.", USER_LOGIN, "Cart has at least one line."],
        "steps": [
            "POST /api/cart until cart non-empty. GET snapshot C_MULTI.",
            "POST /api/checkout with shipping_address (total per cart).",
            "GET /api/cart.",
        ],
        "expected": "After successful checkout (FR-08), GET /api/cart is empty []. Order created — status pending per FR-10.",
        "states": "C_MULTI→C_EMPTY",
        "type": "Legal (cross-endpoint FR-08)",
        "input": {"sequence": ["POST cart", "POST checkout", "GET cart"]},
    },
    {
        "id": "TC-CART-ST-012",
        "module": "cart",
        "fr": "FR-07 / FR-08",
        "api": "AddToCart",
        "method": "POST",
        "endpoint": "/api/cart",
        "title": "After checkout EMPTY → fresh SINGLE (no stale lines)",
        "sm_ref": "C_EMPTY(post-checkout) → C_SINGLE",
        "transition": "post-checkout fresh add",
        "preconditions": [f"EShop at {BASE}.", USER_LOGIN, "Cart empty after prior checkout."],
        "steps": [
            "POST /api/cart id=1 qty=1.",
            "GET /api/cart.",
        ],
        "expected": "Exactly one new line id=1 qty=1. No lines from pre-checkout cart.",
        "states": "C_EMPTY→C_SINGLE",
        "type": "Legal",
        "input": {"sequence": ["POST after checkout", "GET"]},
    },
    {
        "id": "TC-CART-ST-013",
        "module": "cart",
        "fr": "FR-07",
        "api": "AddToCart",
        "method": "POST",
        "endpoint": "/api/cart",
        "title": "POST cannot decrease quantity (no negative transition)",
        "sm_ref": "C_SINGLE(qty=5) → POST cannot reduce",
        "transition": "illegal qty decrease via POST-only",
        "preconditions": [f"EShop at {BASE}.", USER_LOGIN, "Cart id=1 qty=5."],
        "steps": [
            "POST /api/cart id=1 qty=1 (add-only semantics).",
            "GET /api/cart.",
        ],
        "expected": "qty becomes 6 if merge/add-only. Must not drop below 5 unless a separate remove API exists (none in spec).",
        "states": "C_SINGLE(5)→C_SINGLE(6)",
        "type": "Legal (monotonic add)",
        "input": {"sequence": ["POST add", "GET"]},
    },
    {
        "id": "TC-CART-ST-014",
        "module": "cart",
        "fr": "FR-07",
        "api": "AddToCart",
        "method": "POST",
        "endpoint": "/api/cart",
        "title": "Unequal merge operands 2+3 from EMPTY sequence",
        "sm_ref": "C_EMPTY → C_MERGED qty=5",
        "transition": "C_EMPTY → C_MERGED(5)",
        "preconditions": [f"EShop at {BASE}.", USER_LOGIN, "Empty cart."],
        "steps": [
            "POST id=1 qty=2.",
            "POST id=1 qty=3.",
            "GET /api/cart.",
        ],
        "expected": "One line id=1 qty=5.",
        "states": "C_EMPTY→C_MERGED(5)",
        "type": "Legal",
        "input": {"sequence": ["POST qty=2", "POST qty=3", "GET"]},
    },
    {
        "id": "TC-CART-ST-015",
        "module": "cart",
        "fr": "FR-07",
        "api": "AddToCart",
        "method": "POST",
        "endpoint": "/api/cart",
        "title": "Cart survives re-login (persistence boundary)",
        "sm_ref": "C_SINGLE → (new token) → C_SINGLE",
        "transition": "session boundary",
        "preconditions": [f"EShop at {BASE}."],
        "steps": [
            "Login test@eshop.com. POST id=1 qty=1. GET → C_SINGLE.",
            "Login again (new token). GET /api/cart.",
        ],
        "expected": "Cart still shows id=1 if server persists per user. If in-memory only, record Blocked/actual — spec does not define persistence medium.",
        "states": "C_SINGLE→C_SINGLE",
        "type": "Legal / Unspecified persistence",
        "input": {"sequence": ["POST", "re-login", "GET"]},
    },
]

# ---------------------------------------------------------------------------
# FR-19 — User existence state (DELETE /api/admin/users/:id)
# ---------------------------------------------------------------------------

ADMIN_CASES = [
    {
        "id": "TC-ADMINUSERS-ST-001",
        "module": "admin-users",
        "fr": "FR-19",
        "api": "AdminDeleteUser",
        "method": "DELETE",
        "endpoint": "/api/admin/users/:id",
        "title": "U_EXISTS → U_DELETED — other user removed from list",
        "sm_ref": "U_EXISTS → U_DELETED",
        "transition": "U_EXISTS → U_DELETED",
        "preconditions": [f"EShop at {BASE}.", ADMIN_LOGIN, "Register disposable user → id D."],
        "steps": [
            "GET /api/admin/users → includes D.",
            "DELETE /api/admin/users/D.",
            "GET /api/admin/users.",
        ],
        "expected": "D absent from list. Admin caller still present. Password never in responses (FR-19).",
        "states": "U_EXISTS→U_DELETED",
        "type": "Legal",
        "input": {"path": {"id": "<disposable_id>"}},
    },
    {
        "id": "TC-ADMINUSERS-ST-002",
        "module": "admin-users",
        "fr": "FR-19",
        "api": "AdminDeleteUser",
        "method": "DELETE",
        "endpoint": "/api/admin/users/:id",
        "title": "U_SELF — admin cannot delete own account",
        "sm_ref": "U_SELF → U_SELF (blocked)",
        "transition": "illegal self-delete",
        "preconditions": [f"EShop at {BASE}.", ADMIN_LOGIN, "Note admin_self_id from token/GET."],
        "steps": [
            "DELETE /api/admin/users/{admin_self_id}.",
            "GET /api/admin/users.",
            "GET /api/users/me as admin.",
        ],
        "expected": "Admin still exists in list and /api/users/me. FR-19 forbids deleting logged-in account. Status not specified — record 4xx vs silent no-op.",
        "states": "U_SELF→U_SELF",
        "type": "Illegal",
        "input": {"path": {"id": "<admin_self_id>"}},
    },
    {
        "id": "TC-ADMINUSERS-ST-003",
        "module": "admin-users",
        "fr": "FR-19",
        "api": "AdminDeleteUser",
        "method": "DELETE",
        "endpoint": "/api/admin/users/:id",
        "title": "U_DELETED → repeat DELETE — terminal state",
        "sm_ref": "U_DELETED → DELETE → U_DELETED",
        "transition": "terminal / idempotency",
        "preconditions": [f"EShop at {BASE}.", ADMIN_LOGIN, "User D already deleted."],
        "steps": [
            "DELETE /api/admin/users/D again.",
            "GET /api/admin/users.",
        ],
        "expected": "D still absent. Second delete must not resurrect user or delete another row. 404/4xx preferred over silent 200 on missing user — not specified.",
        "states": "U_DELETED→U_DELETED",
        "type": "Illegal repeat",
        "input": {"path": {"id": "<deleted_id>"}},
    },
    {
        "id": "TC-ADMINUSERS-ST-004",
        "module": "admin-users",
        "fr": "FR-19",
        "api": "AdminDeleteUser",
        "method": "DELETE",
        "endpoint": "/api/admin/users/:id",
        "title": "List count N → delete one → N−1",
        "sm_ref": "LIST(N) → LIST(N-1)",
        "transition": "list state",
        "preconditions": [f"EShop at {BASE}.", ADMIN_LOGIN, "Count users N before delete."],
        "steps": [
            "GET /api/admin/users → count N.",
            "DELETE disposable user D.",
            "GET /api/admin/users → count N-1.",
        ],
        "expected": "Exactly one fewer user. Only D removed.",
        "states": "LIST(N)→LIST(N-1)",
        "type": "Legal",
        "input": {"sequence": ["GET", "DELETE", "GET"]},
    },
    {
        "id": "TC-ADMINUSERS-ST-005",
        "module": "admin-users",
        "fr": "FR-19",
        "api": "AdminDeleteUser",
        "method": "DELETE",
        "endpoint": "/api/admin/users/:id",
        "title": "Sequential delete A then B — both terminal",
        "sm_ref": "UA_EXISTS→DELETED; UB_EXISTS→DELETED",
        "transition": "multi-delete chain",
        "preconditions": [f"EShop at {BASE}.", ADMIN_LOGIN, "Register users A and B."],
        "steps": [
            "DELETE /api/admin/users/A.",
            "DELETE /api/admin/users/B.",
            "GET /api/admin/users.",
        ],
        "expected": "Neither A nor B in list. Other users unchanged.",
        "states": "UA→DEAD, UB→DEAD",
        "type": "Legal",
        "input": {"sequence": ["DELETE A", "DELETE B", "GET"]},
    },
    {
        "id": "TC-ADMINUSERS-ST-006",
        "module": "admin-users",
        "fr": "FR-19 / SEC-03",
        "api": "AdminDeleteUser",
        "method": "DELETE",
        "endpoint": "/api/admin/users/:id",
        "title": "Non-admin token — U_EXISTS unchanged",
        "sm_ref": "U_EXISTS → (user DELETE) → U_EXISTS",
        "transition": "illegal role",
        "preconditions": [f"EShop at {BASE}.", USER_LOGIN, "Target disposable D exists."],
        "steps": [
            "DELETE /api/admin/users/D with user JWT.",
            "GET /api/admin/users as admin.",
        ],
        "expected": "D still in list. SEC-03 / FR-12: admin route requires admin role.",
        "states": "U_EXISTS→U_EXISTS",
        "type": "Illegal",
        "input": {"auth": "user_token", "path": {"id": "<disposable_id>"}},
    },
    {
        "id": "TC-ADMINUSERS-ST-007",
        "module": "admin-users",
        "fr": "FR-19 / SEC-02",
        "api": "AdminDeleteUser",
        "method": "DELETE",
        "endpoint": "/api/admin/users/:id",
        "title": "No token — U_EXISTS unchanged",
        "sm_ref": "U_EXISTS → (no auth DELETE) → U_EXISTS",
        "transition": "illegal unauthenticated",
        "preconditions": [f"EShop at {BASE}.", "Disposable D exists."],
        "steps": [
            "DELETE /api/admin/users/D without Authorization.",
            "GET /api/admin/users as admin.",
        ],
        "expected": "D still present. SEC-02 requires valid JWT.",
        "states": "U_EXISTS→U_EXISTS",
        "type": "Illegal",
        "input": {"auth": "none"},
    },
    {
        "id": "TC-ADMINUSERS-ST-008",
        "module": "admin-users",
        "fr": "FR-19",
        "api": "AdminDeleteUser",
        "method": "DELETE",
        "endpoint": "/api/admin/users/:id",
        "title": "Register → EXISTS → delete — full lifecycle",
        "sm_ref": "REGISTER → U_EXISTS → U_DELETED",
        "transition": "lifecycle",
        "preconditions": [f"EShop at {BASE}.", ADMIN_LOGIN],
        "steps": [
            "POST /api/register new user → id R.",
            "GET /api/admin/users includes R.",
            "DELETE /api/admin/users/R.",
            "GET /api/admin/users excludes R.",
        ],
        "expected": "R visible then gone. No password in any list response.",
        "states": "REGISTER→EXISTS→DELETED",
        "type": "Legal",
        "input": {"sequence": ["register", "GET", "DELETE", "GET"]},
    },
    {
        "id": "TC-ADMINUSERS-ST-009",
        "module": "admin-users",
        "fr": "FR-19",
        "api": "AdminDeleteUser",
        "method": "DELETE",
        "endpoint": "/api/admin/users/:id",
        "title": "Delete user 3 — users 1 and 2 remain",
        "sm_ref": "selective delete",
        "transition": "U3→DELETED, U1/U2→EXISTS",
        "preconditions": [f"EShop at {BASE}.", ADMIN_LOGIN, "Seed users id=1 admin, id=2 test exist."],
        "steps": [
            "Register disposable id=3 (or use existing id=3 if present).",
            "DELETE /api/admin/users/3.",
            "GET /api/admin/users.",
        ],
        "expected": "id=1 and id=2 still listed. id=3 gone.",
        "states": "U3→DEAD; U1/U2 stable",
        "type": "Legal",
        "input": {"path": {"id": "3"}},
    },
    {
        "id": "TC-ADMINUSERS-ST-010",
        "module": "admin-users",
        "fr": "FR-19",
        "api": "AdminDeleteUser",
        "method": "DELETE",
        "endpoint": "/api/admin/users/:id",
        "title": "Self-delete attempt leaves other users untouched",
        "sm_ref": "U_SELF block; others EXISTS",
        "transition": "illegal self + list stability",
        "preconditions": [f"EShop at {BASE}.", ADMIN_LOGIN, "List includes admin + test@eshop.com."],
        "steps": [
            "DELETE /api/admin/users/{admin_self_id}.",
            "GET /api/admin/users.",
        ],
        "expected": "Full user list unchanged (same count and ids). No collateral delete.",
        "states": "U_SELF→U_SELF; others unchanged",
        "type": "Illegal",
        "input": {"path": {"id": "<admin_self_id>"}},
    },
    {
        "id": "TC-ADMINUSERS-ST-011",
        "module": "admin-users",
        "fr": "FR-19",
        "api": "AdminDeleteUser",
        "method": "DELETE",
        "endpoint": "/api/admin/users/:id",
        "title": "Deleted user cannot login (account terminal)",
        "sm_ref": "U_DELETED → login fails",
        "transition": "cross-endpoint auth state",
        "preconditions": [f"EShop at {BASE}.", "User D deleted by admin."],
        "steps": [
            "POST /api/login with D credentials.",
        ],
        "expected": "Login rejected (401/403). U_DELETED is terminal for authentication.",
        "states": "U_DELETED→auth blocked",
        "type": "Legal consequence",
        "input": {"sequence": ["login deleted user"]},
    },
    {
        "id": "TC-ADMINUSERS-ST-012",
        "module": "admin-users",
        "fr": "FR-19",
        "api": "AdminDeleteUser",
        "method": "DELETE",
        "endpoint": "/api/admin/users/:id",
        "title": "Delete user with orders — cascade unspecified",
        "sm_ref": "U_EXISTS(+orders) → ?",
        "transition": "cascade edge",
        "preconditions": [
            f"EShop at {BASE}.",
            "Register user D. Login as D. POST cart + POST checkout to create order.",
            ADMIN_LOGIN,
        ],
        "steps": [
            "DELETE /api/admin/users/D.",
            "GET /api/admin/users.",
            "GET /api/admin/orders (optional).",
        ],
        "expected": "Cascade not specified in FR-19. Record: user deleted vs blocked; orders orphaned vs cascade. Do not invent requirement.",
        "states": "U_EXISTS→DELETED or blocked",
        "type": "Unspecified",
        "input": {"sequence": ["DELETE user with orders", "GET users"]},
    },
    {
        "id": "TC-ADMINUSERS-ST-013",
        "module": "admin-users",
        "fr": "FR-19",
        "api": "AdminDeleteUser",
        "method": "DELETE",
        "endpoint": "/api/admin/users/:id",
        "title": "Body id must not override path — self-delete guard holds",
        "sm_ref": "path=self, body=other → U_SELF protected",
        "transition": "path wins over body",
        "preconditions": [f"EShop at {BASE}.", ADMIN_LOGIN, "Disposable D exists."],
        "steps": [
            'DELETE /api/admin/users/{admin_self_id} with JSON body {"id": D}.',
            "GET /api/admin/users.",
        ],
        "expected": "Admin not deleted. D not deleted via body override. FR-19 path id is authoritative.",
        "states": "U_SELF→U_SELF; D→EXISTS",
        "type": "Illegal / guard",
        "input": {"path": "<admin_self_id>", "body": {"id": "<D>"}},
    },
    {
        "id": "TC-ADMINUSERS-ST-014",
        "module": "admin-users",
        "fr": "FR-19",
        "api": "AdminDeleteUser",
        "method": "DELETE",
        "endpoint": "/api/admin/users/:id",
        "title": "Delete seed user id=2 — admin id=1 survives",
        "sm_ref": "U2→DELETED; U1(admin)→EXISTS",
        "transition": "seed user delete",
        "preconditions": [f"EShop at {BASE}.", ADMIN_LOGIN, "Fresh seed DB."],
        "steps": [
            "DELETE /api/admin/users/2 (test@eshop.com).",
            "GET /api/admin/users.",
            "GET /api/users/me as admin.",
        ],
        "expected": "id=2 gone. Admin id=1 still exists and can access /api/users/me.",
        "states": "U2→DEAD; U1→EXISTS",
        "type": "Legal",
        "input": {"path": {"id": "2"}},
    },
    {
        "id": "TC-ADMINUSERS-ST-015",
        "module": "admin-users",
        "fr": "FR-19",
        "api": "AdminDeleteUser",
        "method": "DELETE",
        "endpoint": "/api/admin/users/:id",
        "title": "Non-existent id — U_NONE stays none, list unchanged",
        "sm_ref": "U_NONE → DELETE → U_NONE",
        "transition": "delete missing user",
        "preconditions": [f"EShop at {BASE}.", ADMIN_LOGIN, "Snapshot user list L0."],
        "steps": [
            "DELETE /api/admin/users/99999.",
            "GET /api/admin/users → L1.",
        ],
        "expected": "L1 equals L0 (no user removed). 404/4xx expected — status not specified.",
        "states": "U_NONE→U_NONE",
        "type": "Illegal",
        "input": {"path": {"id": "99999"}},
    },
]

ALL_CASES = PROFILE_CASES + CART_CASES + ADMIN_CASES


def build_report() -> str:
    lines = [
        "# State Transition Testing Report — FR-04, FR-07, FR-19",
        "",
        "**Student:** 23127271 · **SUT:** EShop (`http://localhost:3000`)  ",
        "**Category:** Stage 1 — State Transitions (API testing skill checklist §2)  ",
        "**Sources:** `Repo/eshop-sut/README.md`, `api_specification.md`",
        "",
        "---",
        "",
        "## Scope",
        "",
        "| FR | Endpoint | Resource state model |",
        "|----|----------|----------------------|",
        "| FR-04 | `PUT /api/users/me` | Profile field snapshot P0→P1→…; immutables email/role |",
        "| FR-07 | `POST /api/cart` | Cart line-item states EMPTY/SINGLE/MERGED/MULTI; FR-08 clears cart |",
        "| FR-19 | `DELETE /api/admin/users/:id` | User existence EXISTS/DELETED/SELF; admin list count |",
        "",
        "---",
        "",
        "## FR-04 — Profile state machine",
        "",
        "```",
        "P0 (seed profile)",
        "  │ PUT valid (name/phone/address)",
        "  ▼",
        "P1 (updated snapshot)",
        "  │ PUT again (full or partial — partial semantics unspecified)",
        "  ▼",
        "P2 … Pn",
        "",
        "Constraints (no transition): email, role",
        "```",
        "",
        f"**Count:** {len(PROFILE_CASES)} cases (`TC-PROFILE-ST-001` … `TC-PROFILE-ST-{len(PROFILE_CASES):03d}`)",
        "",
        "| TC ID | Transition | Type |",
        "|-------|------------|------|",
    ]
    for c in PROFILE_CASES:
        lines.append(f"| {c['id']} | {c['transition']} | {c['type']} |")

    lines += [
        "",
        "---",
        "",
        "## FR-07 — Cart state machine",
        "",
        "```",
        "C_EMPTY",
        "  │ POST product",
        "  ▼",
        "C_SINGLE ──POST same id──► C_MERGED (qty↑, one line)   [FR-07]",
        "  │ POST different id",
        "  ▼",
        "C_MULTI ──POST checkout (FR-08)──► C_EMPTY",
        "```",
        "",
        f"**Count:** {len(CART_CASES)} cases (`TC-CART-ST-001` … `TC-CART-ST-{len(CART_CASES):03d}`)",
        "",
        "| TC ID | Transition | Type |",
        "|-------|------------|------|",
    ]
    for c in CART_CASES:
        lines.append(f"| {c['id']} | {c['transition']} | {c['type']} |")

    lines += [
        "",
        "---",
        "",
        "## FR-19 — User existence state machine",
        "",
        "```",
        "U_EXISTS (in admin list)",
        "  │ DELETE by admin (other user)",
        "  ▼",
        "U_DELETED (terminal — not in list, login fails)",
        "",
        "U_SELF (admin own id)",
        "  │ DELETE self",
        "  ✗ blocked [FR-19]",
        "```",
        "",
        f"**Count:** {len(ADMIN_CASES)} cases (`TC-ADMINUSERS-ST-001` … `TC-ADMINUSERS-ST-{len(ADMIN_CASES):03d}`)",
        "",
        "| TC ID | Transition | Type |",
        "|-------|------------|------|",
    ]
    for c in ADMIN_CASES:
        lines.append(f"| {c['id']} | {c['transition']} | {c['type']} |")

    total = len(ALL_CASES)
    lines += [
        "",
        "---",
        "",
        "## Step 5 — Review checklist",
        "",
        "| Check | FR-04 | FR-07 | FR-19 |",
        "|-------|-------|-------|-------|",
        "| Legal transition covered | Yes | Yes | Yes |",
        "| Illegal / terminal transition | Yes | Yes | Yes |",
        "| Idempotency / repeat | Yes | Yes | Yes |",
        "| Cross-session / isolation | Yes | Yes | Yes |",
        "| Oracles spec-only (no invented HTTP codes) | Yes | Yes | Yes |",
        "",
        "## Artifact index",
        "",
        "| Artifact | Path |",
        "|----------|------|",
        "| This report | `docs/state-transition-report.md` |",
        "| Per-TC files | `tests/test-cases/{profile,cart,admin-users}/TC-*-ST-*.md` |",
        "| Sheet | `sheets/state-transitions.csv` |",
        "| Generator | `scripts/generate_state_transitions.py` |",
        "",
        f"**Totals:** {len(PROFILE_CASES)} PROFILE + {len(CART_CASES)} CART + {len(ADMIN_CASES)} ADMINUSERS = **{total}** state-transition cases.",
        "",
        "**Combined Stage-1 AI counts (domain + state):**",
        f"- FR-04: 40 + {len(PROFILE_CASES)} = {40 + len(PROFILE_CASES)}",
        f"- FR-07: 39 + {len(CART_CASES)} = {39 + len(CART_CASES)}",
        f"- FR-19: 20 + {len(ADMIN_CASES)} = {20 + len(ADMIN_CASES)}",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    for case in ALL_CASES:
        write_tc(case["module"], case)

    fieldnames = [
        "TestCaseID",
        "API",
        "Method",
        "Endpoint",
        "Category",
        "Preconditions",
        "Input",
        "ExpectedResult",
        "Priority",
        "Source",
        "AuditStatus",
        "AuditReasoning",
        "ActualResult",
        "PassFail",
        "BugRef",
        "Notes",
    ]
    with SHEET.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for case in ALL_CASES:
            w.writerow(row(case))

    REPORT.write_text(build_report(), encoding="utf-8")
    print(f"Wrote {len(ALL_CASES)} state-transition cases")
    print(f"  PROFILE: {len(PROFILE_CASES)}")
    print(f"  CART: {len(CART_CASES)}")
    print(f"  ADMINUSERS: {len(ADMIN_CASES)}")
    print(f"Sheet: {SHEET}")
    print(f"Report: {REPORT}")


if __name__ == "__main__":
    main()
