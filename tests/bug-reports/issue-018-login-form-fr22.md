# Bug Report #18 — Ready for GitHub Issue

**Title:** [BUG][Login] Login form violates FR-22 Form Requirements

**Found by Test Case:** TC-GUI-001-Login, TC-GUI-003, TC-GUI-006  
**Requirement:** FR-22  
**Severity / Priority:** Major / P2  
**Environment:** Windows 11 · Chromium (Playwright) · `http://localhost:5173`  
**Reported by:** QA / Playwright automation (`npm run test:gui`)  
**Date:** 2026-06-29

**Classification:** Type: UI/UX | Severity: Major | Priority: P2

## Description

Trang `/login` không tuân **FR-22: Form Requirements**:

| FR-22 rule | Expected | Actual (`Login.jsx`) |
| :--- | :--- | :--- |
| Trường bắt buộc có `*` | Nhãn Email / Mật khẩu có `*` | Không có `*` trên form |
| Email `type="email"` | `input[type="email"]` | `type="text"`, label "Username" (line 28–34) |
| Mật khẩu `type="password"` | `input[type="password"]` | `type="text"` (line 39–40) |

Tiêu đề form hiển thị **Đăng Ký** thay vì Đăng nhập (line 24) — lỗi nhãn giao diện liên quan form.

## Steps to Reproduce

1. Mở `http://localhost:5173/login`.
2. Inspect các trường Email/Username và Mật khẩu.
3. Chạy `npm run test:gui` — các test TC-GUI-001-Login, TC-GUI-003, TC-GUI-006 fail.

## Expected Result

- Trường bắt buộc có ký hiệu `*` (FR-22).
- Email dùng `type="email"`.
- Mật khẩu dùng `type="password"` (không hiển thị rõ).

## Actual Result

- `body` không chứa `*` trên form đăng nhập.
- `input[type="email"]` count = **0**; `input[type="password"]` count = **0**.
- Playwright TC-GUI-003 / TC-GUI-006: assertion fail trên `/login`.

## Evidence

- `frontend-web/src/pages/Login.jsx` lines 24, 26–45
- `tests/e2e/gui-requirements.spec.js` — TC-GUI-001-Login, TC-GUI-003, TC-GUI-006
- `test-results/gui-requirements-FR-22-*/error-context.md`

## Suggested Labels

`type: bug`, `module: login`, `severity: major`, `priority: P2`, `status: new`, `found-by: test-case`, `requirement: FR-22`
