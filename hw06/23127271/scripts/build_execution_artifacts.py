#!/usr/bin/env python3
"""Stage 4 — merge test-case sheets, Excel workbook, and Postman collection."""
from __future__ import annotations

import csv
import json
import re
import subprocess
import sys
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHEETS = ROOT / "sheets"
POSTMAN_DIR = ROOT / "postman"
DOCS = ROOT / "docs"
SKILL_SCRIPT = (
    Path(__file__).resolve().parents[4]
    / ".cursor"
    / "skills"
    / "api-testing"
    / "scripts"
    / "build_test_case_sheet.py"
)

STUDENT_ID = "23127271"
BASE_URL = "http://localhost:3000"

SHEET_FILES = [
    ("domain-partitions.csv", "DomainPartition"),
    ("state-transitions.csv", "StateTransition"),
    ("security-tests.csv", "Security"),
    ("schema-validation.csv", "SchemaValidation"),
]

MODULE_ORDER = {
    "UpdateProfile": ("FR-04", "Profile"),
    "GetProfile": ("FR-04", "Profile"),
    "AddToCart": ("FR-07", "Cart"),
    "GetCart": ("FR-07", "Cart"),
    "Checkout": ("FR-07", "Cart"),
    "AdminListUsers": ("FR-19", "Admin Users"),
    "AdminDeleteUser": ("FR-19", "Admin Users"),
}

CATEGORY_ORDER = ["DomainPartition", "StateTransition", "Security", "SchemaValidation"]

DEFAULT_PROFILE_BODY = {
    "name": "Nguyen Van A",
    "phone": "0912345678",
    "shipping_address": "123 Le Loi, Q1, TP.HCM",
}
DEFAULT_CART_BODY = {
    "id": 1,
    "name": "iPhone",
    "price": 30000000,
    "quantity": 1,
}

TOKEN_LITERALS = {
    "<access_token>": "{{userToken}}",
    "<user_token>": "{{userToken}}",
    "<valid_user_token>": "{{userToken}}",
    "<admin_token>": "{{adminToken}}",
    "<token>": "{{userToken}}",
    "Bearer <access_token>": "Bearer {{userToken}}",
    "Bearer <user_token>": "Bearer {{userToken}}",
    "Bearer <valid_user_token>": "Bearer {{userToken}}",
    "Bearer <admin_token>": "Bearer {{adminToken}}",
    "Bearer <token>": "Bearer {{userToken}}",
}

PATH_LITERALS = {
    "<disposable_user_id>": "{{disposableUserId}}",
    "<user_self_id>": "{{userSelfId}}",
    "<admin_self_id>": "{{adminSelfId}}",
    "<other_existing_id>": "2",
    "D": "{{disposableUserId}}",
}


def load_rows() -> list[dict]:
    rows: list[dict] = []
    for filename, sheet_tag in SHEET_FILES:
        path = SHEETS / filename
        with path.open(encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                row = dict(row)
                row["SheetSource"] = sheet_tag
                rows.append(row)
    rows.sort(key=lambda r: (r.get("API", ""), CATEGORY_ORDER.index(r.get("Category", "")), r.get("TestCaseID", "")))
    return rows


def write_combined_csv(rows: list[dict]) -> Path:
    out = SHEETS / "all-test-cases.csv"
    fieldnames = list(rows[0].keys()) if rows else []
    if "SheetSource" not in fieldnames:
        fieldnames.append("SheetSource")
    with out.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    return out


def build_excel(csv_path: Path) -> Path:
    xlsx = SHEETS / "all-test-cases.xlsx"
    cmd = [sys.executable, str(SKILL_SCRIPT), str(csv_path), str(xlsx)]
    subprocess.run(cmd, check=True)
    return xlsx


def parse_input(raw: str) -> dict:
    if not raw or not raw.strip():
        return {}
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {}


def substitute_token(value: str) -> str:
    if value in TOKEN_LITERALS:
        return TOKEN_LITERALS[value]
    for old, new in TOKEN_LITERALS.items():
        value = value.replace(old, new)
    return value


def substitute_path(value: str) -> str:
    if value in PATH_LITERALS:
        return PATH_LITERALS[value]
    for old, new in PATH_LITERALS.items():
        value = value.replace(old, new)
    return value


def infer_auth(preconditions: str) -> str | None:
    p = (preconditions or "").lower()
    if any(x in p for x in ("no jwt", "without jwt", "unauthenticated", "headers: {}", "no active session")):
        if "admin jwt" not in p and "login as admin" not in p:
            return None
    if "admin@eshop.com" in p or "admin jwt" in p or "login as admin" in p or "seed admin" in p:
        return "Bearer {{adminToken}}"
    if "login" in p or "jwt" in p or "bearer" in p or "test@eshop.com" in p:
        return "Bearer {{userToken}}"
    return None


def build_url(endpoint: str, path_params: dict | str | None = None, query: dict | None = None) -> str:
    ep = endpoint
    if isinstance(path_params, str):
        val = substitute_path(path_params)
        if ":id" in ep:
            ep = ep.replace(":id", val)
        else:
            ep = ep.rstrip("/") + "/" + val.lstrip("/")
    elif path_params:
        for key, val in path_params.items():
            val = substitute_path(str(val))
            ep = ep.replace(f":{key}", val)
    url = "{{baseUrl}}" + ep
    if query:
        parts = []
        for k, v in query.items():
            parts.append(f"{k}={substitute_path(str(v))}")
        url += "?" + "&".join(parts)
    return url


def default_body(api: str, method: str) -> dict | None:
    if api in ("UpdateProfile", "GetProfile") and method == "PUT":
        return dict(DEFAULT_PROFILE_BODY)
    if api in ("AddToCart", "GetCart") and method == "POST":
        return dict(DEFAULT_CART_BODY)
    return None


def headers_from_input(inp: dict, preconditions: str) -> list[dict]:
    headers: list[dict] = []
    raw = inp.get("headers") or {}
    for key, val in raw.items():
        headers.append({"key": key, "value": substitute_token(str(val)), "type": "text"})
    auth = infer_auth(preconditions)
    has_auth = any(h["key"].lower() == "authorization" for h in headers)
    if auth and not has_auth:
        headers.append({"key": "Authorization", "value": auth, "type": "text"})
    has_ct = any(h["key"].lower() == "content-type" for h in headers)
    method_hint = inp.get("_method", "GET")
    if method_hint in ("POST", "PUT", "PATCH") and not has_ct and "body_raw" not in inp:
        headers.append({"key": "Content-Type", "value": "application/json", "type": "text"})
    headers.append({"key": "Accept", "value": "application/json", "type": "text"})
    return headers


def body_mode(inp: dict, row: dict) -> tuple[str | None, dict | str | None]:
    if "body_raw" in inp:
        return "raw", inp["body_raw"]
    if "body" in inp:
        return "json", inp["body"]
    default = default_body(row.get("API", ""), row.get("Method", ""))
    if default:
        return "json", default
    return None, None


def make_request(name: str, method: str, url: str, headers: list[dict], body_kind: str | None, body) -> dict:
    req: dict = {
        "name": name,
        "request": {
            "method": method,
            "header": headers,
            "url": url,
        },
    }
    if body_kind == "raw" and body is not None:
        req["request"]["body"] = {"mode": "raw", "raw": str(body)}
    elif body_kind == "json" and body is not None:
        req["request"]["body"] = {
            "mode": "raw",
            "raw": json.dumps(body, ensure_ascii=False, indent=2),
            "options": {"raw": {"language": "json"}},
        }
    return req


def test_script(tc_id: str, expected: str, step: str = "primary") -> list[dict]:
    esc = expected.replace("\\", "\\\\").replace("`", "\\`").replace("\n", " ")
    return [
        {
            "listen": "test",
            "script": {
                "type": "text/javascript",
                "exec": [
                    f"const tcId = '{tc_id}';",
                    f"const step = '{step}';",
                    f"const expected = `{esc}`;",
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
                    "console.log(`[${tcId}] ${step} status=`, pm.response.code);",
                    "console.log(`[${tcId}] expected oracle:`, expected);",
                    "pm.collectionVariables.set('lastTcId', tcId);",
                    "pm.collectionVariables.set('lastStatus', String(pm.response.code));",
                ],
            },
        }
    ]


def sequence_requests(row: dict, inp: dict) -> list[dict]:
    seq = inp.get("sequence") or []
    reqs: list[dict] = []
    method = row.get("Method", "GET")
    endpoint = row.get("Endpoint", "/")
    pre = row.get("Preconditions", "")
    tc_id = row["TestCaseID"]

    if not seq:
        return reqs

    for idx, step in enumerate(seq, start=1):
        step_l = step.lower()
        if "login" in step_l and "put" not in step_l and "get" not in step_l:
            continue
        if step_l.startswith("get ") or step_l == "get":
            m = "GET"
            ep = endpoint
            m_ep = re.search(r"(GET\s+)(/api/\S+)", step, re.I)
            if m_ep:
                ep = m_ep.group(2)
            url = build_url(ep)
            headers = headers_from_input({"_method": "GET"}, pre)
            req = make_request(f"{idx} — GET {ep}", m, url, headers, None, None)
            req["event"] = test_script(tc_id, row.get("ExpectedResult", ""), f"step-{idx}")
            reqs.append(req)
            continue
        if "put" in step_l:
            m = "PUT"
            ep = "/api/users/me" if "users/me" in step_l else endpoint
            url = build_url(ep)
            headers = headers_from_input({"_method": "PUT"}, pre)
            kind, body = body_mode(inp, row)
            req = make_request(f"{idx} — PUT {ep}", m, url, headers, kind, body)
            req["event"] = test_script(tc_id, row.get("ExpectedResult", ""), f"step-{idx}")
            reqs.append(req)
            continue
        if "post" in step_l and "/api/cart" in step_l:
            m = "POST"
            ep = "/api/cart"
            url = build_url(ep)
            headers = headers_from_input({"_method": "POST"}, pre)
            kind, body = body_mode(inp, row)
            req = make_request(f"{idx} — POST {ep}", m, url, headers, kind, body)
            req["event"] = test_script(tc_id, row.get("ExpectedResult", ""), f"step-{idx}")
            reqs.append(req)
            continue
        if "delete" in step_l:
            m = "DELETE"
            ep = endpoint
            m_ep = re.search(r"(DELETE\s+)(/api/\S+)", step, re.I)
            if m_ep:
                ep = m_ep.group(2).replace("D", "{{disposableUserId}}")
            path = inp.get("path") or {"id": "{{disposableUserId}}"}
            url = build_url(ep, path)
            headers = headers_from_input({**inp, "_method": "DELETE"}, pre)
            kind, body = body_mode(inp, row)
            req = make_request(f"{idx} — DELETE", m, url, headers, kind, body)
            req["event"] = test_script(tc_id, row.get("ExpectedResult", ""), f"step-{idx}")
            reqs.append(req)
            continue
        if "parallel" in step_l or "concurrent" in step_l or "fire" in step_l:
            url = build_url(endpoint, inp.get("path"))
            headers = headers_from_input({**inp, "_method": method}, pre)
            kind, body = body_mode(inp, row)
            req = make_request(
                f"{idx} — {method} (manual parallel — see description)",
                method,
                url,
                headers,
                kind,
                body,
            )
            req["request"]["description"] = (
                "This step is a concurrency probe. Run manually in parallel with the paired step, "
                f"or use Postman Collection Runner with multiple workers.\n\nOriginal step: {step}"
            )
            req["event"] = test_script(tc_id, row.get("ExpectedResult", ""), f"step-{idx}")
            reqs.append(req)
            continue

    if not reqs:
        url = build_url(endpoint, inp.get("path"), inp.get("query"))
        headers = headers_from_input({**inp, "_method": method}, pre)
        kind, body = body_mode(inp, row)
        req = make_request(f"1 — {method} {endpoint}", method, url, headers, kind, body)
        req["event"] = test_script(tc_id, row.get("ExpectedResult", ""), "primary")
        reqs.append(req)
    return reqs


def primary_requests(row: dict, inp: dict) -> list[dict]:
    if inp.get("sequence"):
        return sequence_requests(row, inp)
    tc_id = row["TestCaseID"]
    method = row.get("Method", "GET")
    endpoint = row.get("Endpoint", "/")
    pre = row.get("Preconditions", "")
    url = build_url(endpoint, inp.get("path"), inp.get("query"))
    headers = headers_from_input({**inp, "_method": method}, pre)
    kind, body = body_mode(inp, row)
    req = make_request(f"1 — {method} {endpoint}", method, url, headers, kind, body)
    req["event"] = test_script(tc_id, row.get("ExpectedResult", ""), "primary")
    reqs = [req]

    exp = (row.get("ExpectedResult") or "").lower()
    ep = endpoint.lower()
    if method != "GET" and "get /api/users/me" in exp and "/users/me" not in ep:
        url2 = build_url("/api/users/me")
        headers2 = headers_from_input({"_method": "GET"}, pre)
        v = make_request("2 — GET /api/users/me (verify)", "GET", url2, headers2, None, None)
        v["event"] = test_script(tc_id, row.get("ExpectedResult", ""), "verify-profile")
        reqs.append(v)
    if "get /api/cart" in exp and ep != "/api/cart":
        url2 = build_url("/api/cart")
        headers2 = headers_from_input({"_method": "GET"}, pre)
        v = make_request("2 — GET /api/cart (verify)", "GET", url2, headers2, None, None)
        v["event"] = test_script(tc_id, row.get("ExpectedResult", ""), "verify-cart")
        reqs.append(v)
    if "get /api/admin/users" in exp and ep != "/api/admin/users":
        url2 = build_url("/api/admin/users")
        headers2 = headers_from_input({"_method": "GET"}, "admin JWT")
        v = make_request("2 — GET /api/admin/users (verify)", "GET", url2, headers2, None, None)
        v["event"] = test_script(tc_id, row.get("ExpectedResult", ""), "verify-admin-list")
        reqs.append(v)
    return reqs


def tc_folder(row: dict) -> dict:
    inp = parse_input(row.get("Input", ""))
    tc_id = row["TestCaseID"]
    title = tc_id
    notes = row.get("Notes", "")
    m = re.search(r"File=tests/test-cases/[^/]+/([^.]+)\.md", notes)
    desc_parts = [
        f"**Test case:** {tc_id}",
        f"**Category:** {row.get('Category')} | **Source:** {row.get('Source')} | **Audit:** {row.get('AuditStatus') or 'N/A'}",
        f"**Priority:** {row.get('Priority')}",
        "",
        "**Preconditions:**",
        row.get("Preconditions", ""),
        "",
        "**Expected result (oracle):**",
        row.get("ExpectedResult", ""),
        "",
        "**Audit reasoning:**",
        row.get("AuditReasoning", "") or "(none)",
    ]
    item = {
        "name": title,
        "description": "\n".join(desc_parts),
        "item": primary_requests(row, inp),
    }
    return item


def setup_folder() -> dict:
    login_user_test = [
        "pm.test('Login user — 200', function () { pm.response.to.have.status(200); });",
        "const body = pm.response.json();",
        "pm.expect(body).to.have.property('token');",
        "pm.collectionVariables.set('userToken', body.token);",
        "if (body.user && body.user.id) { pm.collectionVariables.set('userSelfId', String(body.user.id)); }",
    ]
    login_admin_test = [
        "pm.test('Login admin — 200', function () { pm.response.to.have.status(200); });",
        "const body = pm.response.json();",
        "pm.expect(body).to.have.property('token');",
        "pm.collectionVariables.set('adminToken', body.token);",
        "if (body.user && body.user.id) { pm.collectionVariables.set('adminSelfId', String(body.user.id)); }",
    ]
    register_test = [
        "pm.test('Register disposable — 200', function () { pm.response.to.have.status(200); });",
        "const body = pm.response.json();",
        "pm.expect(body).to.have.property('id');",
        "pm.collectionVariables.set('disposableUserId', String(body.id));",
        "pm.collectionVariables.set('disposableUserEmail', pm.variables.replaceIn('del.{{$timestamp}}@example.com'));",
    ]
    capture_user_id = [
        "pm.test('Capture userSelfId', function () { pm.response.to.have.status(200); });",
        "const body = pm.response.json();",
        "if (body.id) pm.collectionVariables.set('userSelfId', String(body.id));",
    ]
    capture_admin_id = [
        "pm.test('Capture adminSelfId', function () { pm.response.to.have.status(200); });",
        "const body = pm.response.json();",
        "if (body.id) pm.collectionVariables.set('adminSelfId', String(body.id));",
    ]

    def login_req(name: str, email: str, password: str, tests: list[str]) -> dict:
        return {
            "name": name,
            "event": [{"listen": "test", "script": {"type": "text/javascript", "exec": tests}}],
            "request": {
                "method": "POST",
                "header": [
                    {"key": "Content-Type", "value": "application/json"},
                    {"key": "Accept", "value": "application/json"},
                ],
                "body": {
                    "mode": "raw",
                    "raw": json.dumps({"email": email, "password": password}, indent=2),
                    "options": {"raw": {"language": "json"}},
                },
                "url": "{{baseUrl}}/api/login",
            },
        }

    return {
        "name": "00 — Setup (run first)",
        "description": "Seed tokens and disposable user ids used by FR-04/07/19 tests.",
        "item": [
            login_req("Login — test user (test@eshop.com)", "test@eshop.com", "Test1234!", login_user_test),
            login_req("Login — admin (admin@eshop.com)", "admin@eshop.com", "Admin123!", login_admin_test),
            {
                "name": "GET /api/users/me — capture userSelfId",
                "event": [{"listen": "test", "script": {"type": "text/javascript", "exec": capture_user_id}}],
                "request": {
                    "method": "GET",
                    "header": [
                        {"key": "Authorization", "value": "Bearer {{userToken}}"},
                        {"key": "Accept", "value": "application/json"},
                    ],
                    "url": "{{baseUrl}}/api/users/me",
                },
            },
            {
                "name": "GET /api/users/me — capture adminSelfId",
                "event": [{"listen": "test", "script": {"type": "text/javascript", "exec": capture_admin_id}}],
                "request": {
                    "method": "GET",
                    "header": [
                        {"key": "Authorization", "value": "Bearer {{adminToken}}"},
                        {"key": "Accept", "value": "application/json"},
                    ],
                    "url": "{{baseUrl}}/api/users/me",
                },
            },
            {
                "name": "Register disposable user",
                "event": [{"listen": "test", "script": {"type": "text/javascript", "exec": register_test}}],
                "request": {
                    "method": "POST",
                    "header": [
                        {"key": "Content-Type", "value": "application/json"},
                        {"key": "Accept", "value": "application/json"},
                    ],
                    "body": {
                        "mode": "raw",
                        "raw": json.dumps(
                            {
                                "name": "Disposable User",
                                "email": "del.{{$timestamp}}@example.com",
                                "password": "Password123!",
                            },
                            indent=2,
                        ),
                        "options": {"raw": {"language": "json"}},
                    },
                    "url": "{{baseUrl}}/api/register",
                },
            },
        ],
    }


def build_postman(rows: list[dict]) -> dict:
    tree: dict[str, dict[str, list[dict]]] = {}
    for row in rows:
        api = row.get("API", "Other")
        fr, module = MODULE_ORDER.get(api, ("Other", api))
        cat = row.get("Category", "Other")
        tree.setdefault(fr, {}).setdefault(cat, []).append(tc_folder(row))

    fr_items = []
    for fr in sorted(tree.keys(), key=lambda x: (x == "Other", x)):
        cat_items = []
        cats = tree[fr]
        for cat in CATEGORY_ORDER:
            if cat not in cats:
                continue
            tcs = sorted(cats[cat], key=lambda x: x["name"])
            cat_items.append({"name": cat, "item": tcs})
        for cat, tcs in sorted(cats.items()):
            if cat in CATEGORY_ORDER:
                continue
            cat_items.append({"name": cat, "item": sorted(tcs, key=lambda x: x["name"])})
        module_name = next((MODULE_ORDER[a][1] for a in MODULE_ORDER if MODULE_ORDER[a][0] == fr), fr)
        fr_items.append({"name": f"{fr} — {module_name}", "item": cat_items})

    return {
        "info": {
            "_postman_id": str(uuid.uuid4()),
            "name": f"HW06 EShop API Tests — {STUDENT_ID}",
            "description": (
                "Combined execution collection for FR-04 / FR-07 / FR-19.\n"
                f"Student ID: {STUDENT_ID}\n"
                "Run Setup folder first, then category folders.\n"
                "Newman: newman run postman/eshop-hw06.postman_collection.json "
                "-e postman/eshop-hw06.postman_environment.json "
                "--folder \"00 — Setup (run first)\""
            ),
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
        },
        "event": [
            {
                "listen": "prerequest",
                "script": {
                    "type": "text/javascript",
                    "exec": [
                        "const studentId = pm.collectionVariables.get('studentId') || pm.environment.get('studentId');",
                        "if (!studentId) { console.warn('studentId not set — set collection or environment variable.'); }",
                        "pm.request.headers.upsert({ key: 'X-Student-Id', value: studentId || '' });",
                    ],
                },
            }
        ],
        "variable": [
            {"key": "baseUrl", "value": BASE_URL},
            {"key": "studentId", "value": STUDENT_ID},
            {"key": "userToken", "value": ""},
            {"key": "adminToken", "value": ""},
            {"key": "userSelfId", "value": "2"},
            {"key": "adminSelfId", "value": "1"},
            {"key": "disposableUserId", "value": ""},
            {"key": "lastTcId", "value": ""},
            {"key": "lastStatus", "value": ""},
        ],
        "item": [setup_folder(), *fr_items],
    }


def write_environment() -> Path:
    POSTMAN_DIR.mkdir(parents=True, exist_ok=True)
    env = {
        "id": str(uuid.uuid4()),
        "name": "eshop-hw06-local",
        "values": [
            {"key": "baseUrl", "value": BASE_URL, "type": "default", "enabled": True},
            {"key": "studentId", "value": STUDENT_ID, "type": "default", "enabled": True},
            {"key": "userToken", "value": "", "type": "secret", "enabled": True},
            {"key": "adminToken", "value": "", "type": "secret", "enabled": True},
            {"key": "disposableUserId", "value": "", "type": "default", "enabled": True},
            {"key": "userSelfId", "value": "2", "type": "default", "enabled": True},
            {"key": "adminSelfId", "value": "1", "type": "default", "enabled": True},
        ],
        "_postman_variable_scope": "environment",
        "_postman_exported_at": "2026-08-23T17:00:00.000Z",
        "_postman_exported_using": "build_execution_artifacts.py",
    }
    path = POSTMAN_DIR / "eshop-hw06.postman_environment.json"
    path.write_text(json.dumps(env, indent=2), encoding="utf-8")
    return path


def write_execution_doc(rows: list[dict], csv_path: Path, xlsx_path: Path, coll_path: Path, env_path: Path) -> None:
    by_cat = {}
    for r in rows:
        by_cat[r["Category"]] = by_cat.get(r["Category"], 0) + 1
    doc = f"""# Stage 4 — Execution artifacts

**Student:** {STUDENT_ID} · **SUT:** EShop `{BASE_URL}` · **APIs:** FR-04, FR-07, FR-19

## Deliverables

| Artifact | Path | Count |
|----------|------|------:|
| Combined CSV | `{csv_path.relative_to(ROOT).as_posix()}` | {len(rows)} |
| Excel workbook | `{xlsx_path.relative_to(ROOT).as_posix()}` | {len(rows)} (+ Summary tab) |
| Postman collection | `{coll_path.relative_to(ROOT).as_posix()}` | {len(rows)} TC folders + Setup |
| Postman environment | `{env_path.relative_to(ROOT).as_posix()}` | local vars |

### Combined totals by category

| Category | Cases |
|----------|------:|
"""
    for cat in CATEGORY_ORDER:
        if cat in by_cat:
            doc += f"| {cat} | {by_cat[cat]} |\n"
    doc += f"| **Total** | **{len(rows)}** |\n"

    doc += """
## Postman features used

- **Collection variables** — `baseUrl`, `studentId`, `userToken`, `adminToken`, `userSelfId`, `adminSelfId`, `disposableUserId`
- **Environment file** — local overrides for base URL and tokens
- **Collection pre-request script** — injects `X-Student-Id` on every request
- **Setup folder** — login user/admin, capture ids, register disposable user
- **Nested folders** — FR → category → test case → step requests
- **Test scripts** — observe-only oracles (status recorded, no invented HTTP codes)
- **Dynamic variables** — `{{$timestamp}}` for unique register emails

## How to run

### Postman GUI
1. Import `postman/eshop-hw06.postman_collection.json` and `postman/eshop-hw06.postman_environment.json`
2. Select environment **eshop-hw06-local**
3. Run folder **00 — Setup (run first)**
4. Run FR/category folders or individual TC folders

### Newman (Stage 5)
```bash
# Setup only
newman run postman/eshop-hw06.postman_collection.json -e postman/eshop-hw06.postman_environment.json --folder "00 — Setup (run first)"

# Full collection (long — 280 cases; SUT must be running)
newman run postman/eshop-hw06.postman_collection.json -e postman/eshop-hw06.postman_environment.json -r cli,htmlextra --reporter-htmlextra-export reports/newman-report.html
```

**Note:** Concurrency / parallel probes are marked in request descriptions — run those manually or with multiple Newman workers. Observe-only oracles require human pass/fail against ExpectedResult in the Excel sheet.
"""
    (DOCS / "execution-artifacts.md").write_text(doc, encoding="utf-8")


def main() -> None:
    rows = load_rows()
    csv_path = write_combined_csv(rows)
    xlsx_path = build_excel(csv_path)
    POSTMAN_DIR.mkdir(parents=True, exist_ok=True)
    coll = build_postman(rows)
    coll_path = POSTMAN_DIR / "eshop-hw06.postman_collection.json"
    coll_path.write_text(json.dumps(coll, indent=2, ensure_ascii=False), encoding="utf-8")
    env_path = write_environment()
    write_execution_doc(rows, csv_path, xlsx_path, coll_path, env_path)

    req_count = sum(
        len(tc["item"]) for fr in coll["item"][1:] for cat in fr["item"] for tc in cat["item"]
    )
    print(f"Combined CSV: {csv_path} ({len(rows)} rows)")
    print(f"Excel: {xlsx_path}")
    print(f"Postman: {coll_path} ({len(rows)} TC folders, ~{req_count} requests)")
    print(f"Environment: {env_path}")
    print(f"Doc: {DOCS / 'execution-artifacts.md'}")


if __name__ == "__main__":
    main()
