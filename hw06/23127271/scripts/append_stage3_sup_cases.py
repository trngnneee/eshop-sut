#!/usr/bin/env python3
"""Append Stage 3 human-found SUP domain-partition rows to domain-partitions.csv."""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHEET = ROOT / "sheets" / "domain-partitions.csv"

ROWS = [
    {
        "TestCaseID": "TC-PROFILE-SUP-001",
        "API": "UpdateProfile",
        "Method": "PUT",
        "Endpoint": "/api/users/me",
        "Category": "DomainPartition",
        "Preconditions": "EShop backend running. Logged in as test@eshop.com. Snapshot GET /api/users/me.",
        "Input": json.dumps(
            {
                "headers": {"Authorization": "Bearer <access_token>", "Content-Type": "application/json"},
                "body": {"phone": "0987654321"},
            },
            ensure_ascii=False,
        ),
        "ExpectedResult": (
            "If phone is applied, GET shows phone=0987654321 (FR-04-valid). email/role unchanged. "
            "Omitted name/address semantics not specified — record whether snapshot fields stay or change. "
            "Do not reject solely because body is not the three-field example."
        ),
        "Priority": "High",
        "Source": "Human",
        "AuditStatus": "N/A",
        "AuditReasoning": (
            "Why AI missed: Prompt quality — API example triple treated as only valid shape; "
            "omit-name was negative-only; no positive phone-only after Stage 2."
        ),
        "Notes": (
            "Sub-domains: P-PHONE-01, P-NAME-05, P-ADDR-04 | Type=Valid/Unspecified | "
            "File=tests/test-cases/profile/TC-PROFILE-SUP-001.md"
        ),
    },
    {
        "TestCaseID": "TC-PROFILE-SUP-002",
        "API": "UpdateProfile",
        "Method": "PUT",
        "Endpoint": "/api/users/me",
        "Category": "DomainPartition",
        "Preconditions": "Logged in as test@eshop.com. Snapshot phone.",
        "Input": json.dumps(
            {
                "headers": {"Authorization": "Bearer <access_token>", "Content-Type": "application/json"},
                "body": {
                    "name": "Nguyen Van A",
                    "shipping_address": "123 Le Loi, Q1, TP.HCM",
                    "phone": "０９１２３４５６７８",
                },
            },
            ensure_ascii=False,
        ),
        "ExpectedResult": (
            "Fullwidth digits (U+FF10…) are not the documented ASCII 0–9 form. "
            "GET must not persist this string as phone. Normalisation not specified — record only."
        ),
        "Priority": "Medium",
        "Source": "Human",
        "AuditStatus": "N/A",
        "AuditReasoning": (
            "Why AI missed: Model limitation — phone partitions were ASCII-only; "
            "Unicode digit scripts not split from chữ số."
        ),
        "Notes": "Sub-domains: P-PHONE-H01 | Type=Invalid | File=tests/test-cases/profile/TC-PROFILE-SUP-002.md",
    },
    {
        "TestCaseID": "TC-PROFILE-SUP-003",
        "API": "UpdateProfile",
        "Method": "PUT",
        "Endpoint": "/api/users/me",
        "Category": "DomainPartition",
        "Preconditions": "Logged in as test@eshop.com. Snapshot GET /api/users/me.",
        "Input": json.dumps(
            {
                "headers": {"Authorization": "Bearer <access_token>", "Content-Type": "application/json"},
                "body": '{"name":"Nguyen Van A","shipping_address":"123 Le Loi, Q1, TP.HCM","phone":"0912345678","phone":"1912345678"}',
            },
            ensure_ascii=False,
        ),
        "ExpectedResult": (
            "Duplicate JSON keys not specified. Stored phone, if any, must be FR-04-valid — "
            "GET must not show 1912345678. email/role unchanged."
        ),
        "Priority": "Medium",
        "Source": "Human",
        "AuditStatus": "N/A",
        "AuditReasoning": (
            "Why AI missed: API characteristic (JSON parser) + model limitation — "
            "LLMs emit unique keys; duplicate-key wins not in spec."
        ),
        "Notes": "Sub-domains: P-BODY-H01 | Type=Invalid/Unspecified | File=tests/test-cases/profile/TC-PROFILE-SUP-003.md",
    },
    {
        "TestCaseID": "TC-CART-SUP-001",
        "API": "AddToCart",
        "Method": "POST",
        "Endpoint": "/api/cart",
        "Category": "DomainPartition",
        "Preconditions": "Logged in. Cart has id=1 qty=1. GET confirms one line.",
        "Input": json.dumps(
            {
                "headers": {"Authorization": "Bearer <access_token>", "Content-Type": "application/json"},
                "body": {
                    "id": 1,
                    "name": "Completely Different Label",
                    "price": 30000000,
                    "quantity": 1,
                },
            },
            ensure_ascii=False,
        ),
        "ExpectedResult": (
            "FR-07 same-product merge does not define identity key (id vs name). "
            "Record: one line qty=2 if id-keyed, or two lines if name-keyed. Fail only on crash or lost qty."
        ),
        "Priority": "High",
        "Source": "Human",
        "AuditStatus": "N/A",
        "AuditReasoning": (
            "Why AI missed: API characteristic — cùng một sản phẩm undefined; "
            "mismatch tested alone, merge only with identical bodies."
        ),
        "Notes": (
            "Sub-domains: C-STATE-02, C-NAME-04, C-ID-01 | Type=Unspecified | "
            "File=tests/test-cases/cart/TC-CART-SUP-001.md"
        ),
    },
    {
        "TestCaseID": "TC-CART-SUP-002",
        "API": "AddToCart",
        "Method": "POST",
        "Endpoint": "/api/cart",
        "Category": "DomainPartition",
        "Preconditions": "Logged in. Cart has id=1 qty=2.",
        "Input": json.dumps(
            {
                "headers": {"Authorization": "Bearer <access_token>", "Content-Type": "application/json"},
                "body": {"id": 1, "name": "iPhone 15 Pro Max", "price": 30000000, "quantity": 3},
            },
            ensure_ascii=False,
        ),
        "ExpectedResult": "FR-07: one line id=1 with quantity 5 (2+3). No second row.",
        "Priority": "High",
        "Source": "Human",
        "AuditStatus": "N/A",
        "AuditReasoning": (
            "Why AI missed: Prompt quality / 1×1 — merge covered only 1+1 (TC-CART-006); "
            "unequal operands not a separate domain."
        ),
        "Notes": (
            "Sub-domains: C-STATE-02, C-QTY-02, C-QTY-03 | Type=Valid | "
            "File=tests/test-cases/cart/TC-CART-SUP-002.md"
        ),
    },
    {
        "TestCaseID": "TC-ADMINUSERS-SUP-001",
        "API": "AdminDeleteUser",
        "Method": "DELETE",
        "Endpoint": "/api/admin/users/:id",
        "Category": "DomainPartition",
        "Preconditions": "Admin JWT. Disposable user registered. enc = percent-encoded decimal id.",
        "Input": json.dumps(
            {"headers": {"Authorization": "Bearer <admin_token>"}, "path": {"id": "<percent_encoded_id>"}},
            ensure_ascii=False,
        ),
        "ExpectedResult": (
            "Percent-encoded path id not specified. If decoded to disposable id (not self), FR-19 allows delete. "
            "If not decoded, record status; no other user deleted."
        ),
        "Priority": "Medium",
        "Source": "Human",
        "AuditStatus": "N/A",
        "AuditReasoning": (
            "Why AI missed: Model limitation — path ids were decimal literals only; "
            "URI percent-encoding not in api_specification.md."
        ),
        "Notes": (
            "Sub-domains: A-ID-01, A-REL-01 | Type=Valid/Unspecified | "
            "File=tests/test-cases/admin-users/TC-ADMINUSERS-SUP-001.md"
        ),
    },
    {
        "TestCaseID": "TC-PROFILE-SUP-004",
        "API": "UpdateProfile",
        "Method": "PUT",
        "Endpoint": "/api/users/me",
        "Category": "DomainPartition",
        "Preconditions": "Logged in as test@eshop.com. Snapshot GET /api/users/me.",
        "Input": json.dumps(
            {"headers": {"Authorization": "Bearer <access_token>", "Content-Type": "application/json"},
             "body": {"name": "Updated Name Only"}},
            ensure_ascii=False,
        ),
        "ExpectedResult": (
            "If name applied, GET shows Updated Name Only. email/role unchanged. "
            "Omitted phone/address not specified — record snapshot vs cleared."
        ),
        "Priority": "High",
        "Source": "Human",
        "AuditStatus": "N/A",
        "AuditReasoning": (
            "Why AI missed: Prompt quality — only phone-only partial (SUP-001) added; "
            "name-only positive partial never split out."
        ),
        "Notes": "Sub-domains: P-NAME-01, P-PHONE-07, P-ADDR-04 | File=tests/test-cases/profile/TC-PROFILE-SUP-004.md",
    },
    {
        "TestCaseID": "TC-PROFILE-SUP-005",
        "API": "UpdateProfile",
        "Method": "PUT",
        "Endpoint": "/api/users/me",
        "Category": "DomainPartition",
        "Preconditions": "Logged in as test@eshop.com. Snapshot GET /api/users/me.",
        "Input": json.dumps(
            {"headers": {"Authorization": "Bearer <access_token>", "Content-Type": "application/json"},
             "body": {"name": "Nguyen Van B", "phone": "0909090909"}},
            ensure_ascii=False,
        ),
        "ExpectedResult": (
            "Two-field subset: name + FR-04-valid phone may update; shipping_address behaviour unspecified. "
            "email/role unchanged."
        ),
        "Priority": "High",
        "Source": "Human",
        "AuditStatus": "N/A",
        "AuditReasoning": (
            "Why AI missed: Prompt quality — valid 2-of-3 field combinations not enumerated after full on-point."
        ),
        "Notes": "Sub-domains: P-NAME-01, P-PHONE-01, P-ADDR-04 | File=tests/test-cases/profile/TC-PROFILE-SUP-005.md",
    },
    {
        "TestCaseID": "TC-CART-SUP-003",
        "API": "AddToCart",
        "Method": "POST",
        "Endpoint": "/api/cart",
        "Category": "DomainPartition",
        "Preconditions": "Cart has id=1 qty=1 price=30000000.",
        "Input": json.dumps(
            {"headers": {"Authorization": "Bearer <access_token>", "Content-Type": "application/json"},
             "body": {"id": 1, "name": "iPhone 15 Pro Max", "price": 1, "quantity": 1}},
            ensure_ascii=False,
        ),
        "ExpectedResult": (
            "FR-07 merge: one line for id=1 if id-keyed. Stored price after merge not specified. "
            "Fail if second line for id=1."
        ),
        "Priority": "High",
        "Source": "Human",
        "AuditStatus": "N/A",
        "AuditReasoning": (
            "Why AI missed: API characteristic — merge + price mismatch never combined; "
            "price tested only standalone."
        ),
        "Notes": "Sub-domains: C-STATE-02, C-PRICE-07 | File=tests/test-cases/cart/TC-CART-SUP-003.md",
    },
    {
        "TestCaseID": "TC-CART-SUP-004",
        "API": "AddToCart",
        "Method": "POST",
        "Endpoint": "/api/cart",
        "Category": "DomainPartition",
        "Preconditions": "Logged in. Prefer empty cart. Seed product id=1.",
        "Input": json.dumps(
            {"headers": {"Authorization": "Bearer <access_token>", "Content-Type": "application/json"},
             "body": {"id": 1, "quantity": 1}},
            ensure_ascii=False,
        ),
        "ExpectedResult": (
            "Minimal body id+quantity only. name/price not required per spec — record line shape; "
            "do not expect reject solely for omission."
        ),
        "Priority": "Medium",
        "Source": "Human",
        "AuditStatus": "N/A",
        "AuditReasoning": (
            "Why AI missed: Prompt quality — cart example treated as atomic; no positive minimal-body after Stage 2."
        ),
        "Notes": "Sub-domains: C-ID-01, C-QTY-01, C-NAME-03, C-PRICE-04 | File=tests/test-cases/cart/TC-CART-SUP-004.md",
    },
    {
        "TestCaseID": "TC-CART-SUP-005",
        "API": "AddToCart",
        "Method": "POST",
        "Endpoint": "/api/cart",
        "Category": "DomainPartition",
        "Preconditions": "Cart has id=1 qty=1 and id=2 qty=1.",
        "Input": json.dumps(
            {"headers": {"Authorization": "Bearer <access_token>", "Content-Type": "application/json"},
             "body": {"id": 1, "name": "iPhone 15 Pro Max", "price": 30000000, "quantity": 2}},
            ensure_ascii=False,
        ),
        "ExpectedResult": "FR-07: two lines remain; id=1 qty=3 (1+2); id=2 qty=1 unchanged.",
        "Priority": "High",
        "Source": "Human",
        "AuditStatus": "N/A",
        "AuditReasoning": (
            "Why AI missed: Prompt quality — merge never tested when cart already had another product line."
        ),
        "Notes": "Sub-domains: C-STATE-02, C-STATE-03 | File=tests/test-cases/cart/TC-CART-SUP-005.md",
    },
    {
        "TestCaseID": "TC-ADMINUSERS-SUP-002",
        "API": "AdminDeleteUser",
        "Method": "DELETE",
        "Endpoint": "/api/admin/users/:id",
        "Category": "DomainPartition",
        "Preconditions": "Admin JWT. Disposable user registered.",
        "Input": json.dumps(
            {"headers": {"Authorization": "Bearer <admin_token>"}, "path": {"id": "<disposable_user_id>/"}},
            ensure_ascii=False,
        ),
        "ExpectedResult": (
            "Trailing slash not specified. Record routing outcome; if delete succeeds, target is disposable user only."
        ),
        "Priority": "Medium",
        "Source": "Human",
        "AuditStatus": "N/A",
        "AuditReasoning": (
            "Why AI missed: Model limitation — URI trailing-slash normalisation not in spec text."
        ),
        "Notes": "Sub-domains: A-ID-01 | File=tests/test-cases/admin-users/TC-ADMINUSERS-SUP-002.md",
    },
    {
        "TestCaseID": "TC-ADMINUSERS-SUP-003",
        "API": "AdminDeleteUser",
        "Method": "DELETE",
        "Endpoint": "/api/admin/users/:id",
        "Category": "DomainPartition",
        "Preconditions": "Fresh seed DB. Admin JWT. Target id=2 (test@eshop.com), not admin id=1.",
        "Input": json.dumps(
            {"headers": {"Authorization": "Bearer <admin_token>"}, "path": {"id": 2}},
            ensure_ascii=False,
        ),
        "ExpectedResult": (
            "FR-19: delete other user allowed. id=2 gone; admin id=1 remains. No password in list responses."
        ),
        "Priority": "High",
        "Source": "Human",
        "AuditStatus": "N/A",
        "AuditReasoning": (
            "Why AI missed: Prompt quality — happy path always used register disposable user, not seed id=2."
        ),
        "Notes": "Sub-domains: A-ID-01, A-REL-01 | File=tests/test-cases/admin-users/TC-ADMINUSERS-SUP-003.md",
    },
    {
        "TestCaseID": "TC-ADMINUSERS-SUP-004",
        "API": "AdminDeleteUser",
        "Method": "DELETE",
        "Endpoint": "/api/admin/users/:id",
        "Category": "DomainPartition",
        "Preconditions": "Admin JWT. Snapshot GET /api/admin/users.",
        "Input": json.dumps(
            {"headers": {"Authorization": "Bearer <admin_token>"}, "path": {"id": "12abc"}},
            ensure_ascii=False,
        ),
        "ExpectedResult": (
            "Mixed alphanumeric path not specified. No unintended user deleted; admin still exists."
        ),
        "Priority": "Medium",
        "Source": "Human",
        "AuditStatus": "N/A",
        "AuditReasoning": (
            "Why AI missed: Model limitation — collapsed into pure letters vs floats; no 12abc class."
        ),
        "Notes": "Sub-domains: A-ID-06 | File=tests/test-cases/admin-users/TC-ADMINUSERS-SUP-004.md",
    },
    {
        "TestCaseID": "TC-ADMINUSERS-SUP-005",
        "API": "AdminDeleteUser",
        "Method": "DELETE",
        "Endpoint": "/api/admin/users/:id",
        "Category": "DomainPartition",
        "Preconditions": "Admin JWT. Disposable user id=12 (example). Path uses double percent-encoding.",
        "Input": json.dumps(
            {"headers": {"Authorization": "Bearer <admin_token>"}, "path": {"id": "%2531%2532"}},
            ensure_ascii=False,
        ),
        "ExpectedResult": (
            "Double-encoding decode depth not specified. Record outcome; FR-19: admin must not delete self."
        ),
        "Priority": "Medium",
        "Source": "Human",
        "AuditStatus": "N/A",
        "AuditReasoning": (
            "Why AI missed: API/HTTP characteristic — encoding layers beyond single percent-encoding (SUP-001)."
        ),
        "Notes": "Sub-domains: A-ID-01 | File=tests/test-cases/admin-users/TC-ADMINUSERS-SUP-005.md",
    },
]


def main() -> None:
    with SHEET.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames or [])
        existing = list(reader)

    ids = {r["TestCaseID"] for r in existing}
    to_add = [r for r in ROWS if r["TestCaseID"] not in ids]
    if not to_add:
        print("All SUP rows already present")
        return

    for r in to_add:
        for k in fieldnames:
            r.setdefault(k, "")

    with SHEET.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(existing + to_add)

    print(f"Appended {len(to_add)} rows to {SHEET} (total {len(existing) + len(to_add)})")


if __name__ == "__main__":
    main()
