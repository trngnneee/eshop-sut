#!/usr/bin/env python3
"""Reproduce HW06 bugs, save PNG evidence, and file GitHub Issues."""
from __future__ import annotations

import json
import subprocess
import textwrap
import time
from pathlib import Path

import requests
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence" / "bugs"
REPO_ROOT = ROOT.parents[1]
REPO = "trngnneee/eshop-sut"
BRANCH = "HW6-Tram"
BASE = "http://localhost:3000"
STUDENT = "23127271"
LABELS = "bug,API-testing"

BUGS = [
    {
        "id": "BUG-001",
        "title": "[HW06][23127271][BUG-001] Non-admin user can list all users via GET /api/admin/users",
        "severity": "Critical",
        "tc": "TC-ADMINUSERS-SEC-SUP-002",
        "found_by": "Human (Stage 3)",
    },
    {
        "id": "BUG-002",
        "title": "[HW06][23127271][BUG-002] Non-admin user receives HTTP 200 on DELETE /api/admin/users/:id",
        "severity": "Critical",
        "tc": "TC-ADMINUSERS-SEC-002",
        "found_by": "AI (Stage 1)",
    },
    {
        "id": "BUG-003",
        "title": "[HW06][23127271][BUG-003] User can escalate to admin via PUT /api/users/me (role mass assignment)",
        "severity": "Critical",
        "tc": "TC-PROFILE-SEC-007",
        "found_by": "AI (Stage 1)",
    },
    {
        "id": "BUG-004",
        "title": "[HW06][23127271][BUG-004] GET /api/users/me exposes password field (SEC-01)",
        "severity": "Critical",
        "tc": "TC-PROFILE-SCH-SUP-003",
        "found_by": "Human (Stage 3)",
    },
    {
        "id": "BUG-006",
        "title": "[HW06][23127271][BUG-006] Profile PUT with Content-Type text/plain returns HTTP 500",
        "severity": "Medium",
        "tc": "TC-PROFILE-SEC-SUP-004",
        "found_by": "Human (Stage 3)",
    },
    {
        "id": "BUG-007",
        "title": "[HW06][23127271][BUG-007] POST /api/cart accepts negative quantity",
        "severity": "Medium",
        "tc": "TC-CART-SEC-SUP-002",
        "found_by": "Human (Stage 3)",
    },
    {
        "id": "BUG-008",
        "title": "[HW06][23127271][BUG-008] GET /api/admin/users exposes undocumented DB columns",
        "severity": "Medium",
        "tc": "TC-ADMINUSERS-SCH-SUP-001",
        "found_by": "Human (Stage 3)",
    },
    {
        "id": "BUG-005",
        "title": "[HW06][23127271][BUG-005] Admin can delete own account (FR-19 self-delete not enforced)",
        "severity": "High",
        "tc": "TC-ADMINUSERS-SEC-003",
        "found_by": "AI (Stage 1)",
    },
]


def hdrs(token: str | None = None, content_type: str | None = "application/json") -> dict:
    h = {"X-Student-Id": STUDENT, "Accept": "application/json"}
    if token:
        h["Authorization"] = f"Bearer {token}"
    if content_type:
        h["Content-Type"] = content_type
    return h


def login(email: str, password: str) -> str:
    r = requests.post(
        f"{BASE}/api/login",
        json={"email": email, "password": password},
        headers=hdrs(content_type="application/json"),
        timeout=15,
    )
    r.raise_for_status()
    return r.json()["token"]


def register_disposable() -> int:
    ts = int(time.time())
    email = f"bugdisp{ts}@example.com"
    r = requests.post(
        f"{BASE}/api/register",
        json={"name": "Disp User", "email": email, "password": "Test1234!"},
        headers=hdrs(),
        timeout=15,
    )
    r.raise_for_status()
    return r.json()["id"]


def redact(obj: object) -> object:
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            if k.lower() in {"password", "password_hash"}:
                out[k] = "<REDACTED>"
            else:
                out[k] = redact(v)
        return out
    if isinstance(obj, list):
        return [redact(x) for x in obj]
    return obj


def format_block(title: str, method: str, url: str, status: int, body: object) -> str:
    body_txt = json.dumps(body, ensure_ascii=False, indent=2) if body is not None else "(empty)"
    return (
        f"{title}\n"
        f"Student: {STUDENT} | SUT: {BASE}\n"
        f"\n{method} {url}\n"
        f"HTTP {status}\n"
        f"\nResponse (sensitive fields redacted in screenshot):\n"
        f"{body_txt}\n"
    )


def save_screenshot(bug_id: str, text: str) -> Path:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    png = EVIDENCE / f"{bug_id}.png"
    json_path = EVIDENCE / f"{bug_id}.json"
    json_path.write_text(text, encoding="utf-8")

    font = ImageFont.load_default()
    lines: list[str] = []
    for para in text.splitlines():
        if not para.strip():
            lines.append("")
            continue
        lines.extend(textwrap.wrap(para, width=110) or [""])

    line_h = 14
    pad = 16
    w = 920
    h = pad * 2 + line_h * max(len(lines), 1)
    img = Image.new("RGB", (w, h), color=(248, 248, 252))
    draw = ImageDraw.Draw(img)
    y = pad
    for line in lines:
        draw.text((pad, y), line, fill=(20, 20, 20), font=font)
        y += line_h
    img.save(png)
    return png


def reproduce(bug_id: str) -> str:
    if bug_id == "BUG-001":
        tok = login("test@eshop.com", "Test1234!")
        r = requests.get(f"{BASE}/api/admin/users", headers=hdrs(tok), timeout=15)
        body = r.json() if r.text else None
        return format_block(bug_id, "GET", "/api/admin/users", r.status_code, redact(body))

    if bug_id == "BUG-002":
        tok = login("test@eshop.com", "Test1234!")
        uid = register_disposable()
        r = requests.delete(f"{BASE}/api/admin/users/{uid}", headers=hdrs(tok), timeout=15)
        body = r.json() if r.text else None
        return format_block(bug_id, "DELETE", f"/api/admin/users/{uid}", r.status_code, body)

    if bug_id == "BUG-003":
        tok = login("test@eshop.com", "Test1234!")
        requests.put(
            f"{BASE}/api/users/me",
            json={
                "name": "Nguyen Van A",
                "phone": "0912345678",
                "shipping_address": "123 Le Loi",
                "role": "admin",
            },
            headers=hdrs(tok),
            timeout=15,
        )
        r = requests.get(f"{BASE}/api/users/me", headers=hdrs(tok), timeout=15)
        body = r.json() if r.text else None
        return format_block(bug_id, "GET", "/api/users/me (after PUT role=admin)", r.status_code, redact(body))

    if bug_id == "BUG-004":
        tok = login("test@eshop.com", "Test1234!")
        r = requests.get(f"{BASE}/api/users/me", headers=hdrs(tok), timeout=15)
        body = r.json() if r.text else None
        keys = list(body.keys()) if isinstance(body, dict) else []
        note = f"Keys returned: {keys}\n"
        return note + format_block(bug_id, "GET", "/api/users/me", r.status_code, redact(body))

    if bug_id == "BUG-005":
        tok = login("admin@eshop.com", "Admin123!")
        me = requests.get(f"{BASE}/api/users/me", headers=hdrs(tok), timeout=15).json()
        aid = me.get("id", 1)
        r = requests.delete(f"{BASE}/api/admin/users/{aid}", headers=hdrs(tok), timeout=15)
        body = r.json() if r.text else None
        return format_block(bug_id, "DELETE", f"/api/admin/users/{aid} (admin self)", r.status_code, body)

    if bug_id == "BUG-006":
        tok = login("test@eshop.com", "Test1234!")
        r = requests.put(
            f"{BASE}/api/users/me",
            data='{"name":"Plain Text","phone":"0912345678","shipping_address":"X"}',
            headers=hdrs(tok, content_type="text/plain"),
            timeout=15,
        )
        body = r.text[:800] if r.text else None
        return format_block(bug_id, "PUT", "/api/users/me (Content-Type: text/plain)", r.status_code, body)

    if bug_id == "BUG-007":
        tok = login("test@eshop.com", "Test1234!")
        r = requests.post(
            f"{BASE}/api/cart",
            json={"id": 1, "name": "iPhone", "price": 30000000, "quantity": -1},
            headers=hdrs(tok),
            timeout=15,
        )
        post_body = r.json() if r.text else None
        cart = requests.get(f"{BASE}/api/cart", headers=hdrs(tok), timeout=15).json()
        return format_block(
            bug_id,
            "POST+GET",
            "/api/cart (quantity=-1) then GET /api/cart",
            r.status_code,
            {"post_response": post_body, "cart_after": cart},
        )

    if bug_id == "BUG-008":
        tok = login("admin@eshop.com", "Admin123!")
        r = requests.get(f"{BASE}/api/admin/users", headers=hdrs(tok), timeout=15)
        body = r.json() if r.text else None
        if isinstance(body, list) and body:
            keys = list(body[0].keys())
            note = f"First list item keys: {keys}\n"
        else:
            note = ""
        return note + format_block(bug_id, "GET", "/api/admin/users", r.status_code, redact(body))

    raise ValueError(bug_id)


def issue_body(meta: dict, md_path: Path, image_name: str) -> str:
    md = md_path.read_text(encoding="utf-8")
    img_url = f"https://github.com/{REPO}/raw/{BRANCH}/hw06/23127271/evidence/bugs/{image_name}"
    md_name = md_path.name
    return (
        f"**HW06 API Testing — Student {STUDENT}**\n\n"
        f"- **Severity:** {meta['severity']}\n"
        f"- **Found via:** `{meta['tc']}` ({meta['found_by']})\n"
        f"- **Local report:** `hw06/23127271/bugs/{md_name}`\n\n"
        f"## Screenshot evidence\n\n"
        f"![{meta['id']} evidence]({img_url})\n\n"
        f"---\n\n"
        f"{md}"
    )


def push_evidence() -> None:
    subprocess.run(
        ["git", "add", "hw06/23127271/evidence/bugs"],
        cwd=REPO_ROOT,
        check=True,
    )
    status = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    if not status.stdout.strip():
        print("  evidence already committed")
        return
    subprocess.run(
        [
            "git",
            "commit",
            "-m",
            "HW06: add bug reproduction screenshot evidence for GitHub Issues.",
        ],
        cwd=REPO_ROOT,
        check=True,
    )
    subprocess.run(
        ["git", "push", f"https://github.com/{REPO}.git", BRANCH],
        cwd=REPO_ROOT,
        check=True,
    )


def create_issue(meta: dict, body_file: Path) -> str:
    for labels in (LABELS, "bug"):
        result = subprocess.run(
            [
                "gh",
                "issue",
                "create",
                "--repo",
                REPO,
                "--title",
                meta["title"],
                "--label",
                labels,
                "--body-file",
                str(body_file),
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        if result.returncode == 0:
            return result.stdout.strip()
        if "not found" not in (result.stderr or "").lower():
            print(result.stderr)
            break
    result = subprocess.run(
        [
            "gh",
            "issue",
            "create",
            "--repo",
            REPO,
            "--title",
            meta["title"],
            "--body-file",
            str(body_file),
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if result.returncode != 0:
        print(result.stderr)
        raise SystemExit(f"gh issue create failed for {meta['id']}")
    return result.stdout.strip()


def main() -> None:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    issue_urls: dict[str, str] = {}
    body_files: list[tuple[dict, Path]] = []

    for meta in BUGS:
        bug_id = meta["id"]
        print(f"Reproducing {bug_id}...")
        text = reproduce(bug_id)
        png = save_screenshot(bug_id, text)
        print(f"  evidence: {png}")
        body_file = EVIDENCE / f"{bug_id}-issue-body.md"
        body_files.append((meta, body_file))

    print("Pushing screenshot evidence to GitHub...")
    push_evidence()

    for meta, body_file in body_files:
        bug_id = meta["id"]
        md_path = next(ROOT.glob(f"bugs/{bug_id}-*.md"))
        body_file.write_text(issue_body(meta, md_path, f"{bug_id}.png"), encoding="utf-8")
        url = create_issue(meta, body_file)
        issue_urls[bug_id] = url
        print(f"  {bug_id}: {url}")

    out = ROOT / "docs" / "github-issues.md"
    lines = ["# GitHub Issues — HW06 bugs\n", f"Repo: https://github.com/{REPO}/issues\n"]
    for meta in BUGS:
        bid = meta["id"]
        lines.append(f"- **{bid}** — {issue_urls[bid]}")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
