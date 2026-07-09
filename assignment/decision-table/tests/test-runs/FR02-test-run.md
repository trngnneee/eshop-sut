# Test Run: FR02 — Đăng nhập & Khóa tài khoản

**Ngày chạy**: 2026-06-29 16:14  
**Tester**: AI Automated (fr02-test-runner.js)  
**Build / Commit**: local  
**Base URL**: `http://localhost:3000`  
**Environment**: Node.js v24.10.0 / SQLite / Windows

---

| Test Case ID | Module | Tester | Date | Result | Related Bug | Note / Evidence |
|---|---|---|---|---|---|---|
| TC-WEB-DT-PW-001 | Web / API | AI Runner | 2026-06-29 | **Pass** | None | Happy path user — 200 + JWT |
| TC-WEB-DT-PW-002 | Web / API | AI Runner | 2026-06-29 | **Pass** | None | Happy path admin — 200 + role=admin |
| TC-WEB-DT-PW-003 | Web / API | AI Runner | 2026-06-29 | **Fail(Bug)** | BUG-FR02-001 | attempts=3 (actual) vs 2 (spec); locked_until SET tại lần sai thứ 2 |
| TC-WEB-DT-PW-004 | Web / API | AI Runner | 2026-06-29 | **Fail(Bug)** | BUG-FR02-001 | Admin: attempts=3, locked_until SET tại lần sai thứ 2 |
| TC-WEB-DT-PW-005 | Web / API | AI Runner | 2026-06-29 | **Pass** | None | Locked + đúng password → 403 đúng |
| TC-WEB-DT-PW-006 | Web / API | AI Runner | 2026-06-29 | **Pass** | None | Admin locked + đúng password → 403 |
| TC-WEB-DT-PW-007 | Web / API | AI Runner | 2026-06-29 | **Pass** | None | Lock check priority: locked+sai password → 403 (không phải 401) |
| TC-WEB-DT-PW-008 | Web / API | AI Runner | 2026-06-29 | **Pass** | None | Email không tồn tại → 401 "Invalid email or password" |
| TC-WEB-DT-PW-009 | Web / API | AI Runner | 2026-06-29 | **Pass** | None | Đúng password sau 1 sai → reset attempts=0 |
| TC-WEB-DT-PW-010 | Web / API | AI Runner | 2026-06-29 | **Fail(Bug)** | BUG-FR02-001 | Sai lần 1: attempts=2 (actual) vs 1 (spec) — +2 bug |
| TC-WEB-DT-PW-011 | Web / API | AI Runner | 2026-06-29 | **Fail(Bug)** | BUG-FR02-001 | Admin sai lần 1: attempts=2 vs 1 |
| TC-WEB-DT-PW-012 | Web / API | AI Runner | 2026-06-29 | **Pass** | None | Login thành công sau hết khóa → reset attempts=0, locked_until=NULL |
| TC-WEB-DT-PW-013 | Web / API | AI Runner | 2026-06-29 | **Fail(Bug)** | BUG-FR02-001 | Sai sau hết khóa: attempts=5 (actual) vs 4 (spec) |
| TC-WEB-DT-PW-014 | Web / API | AI Runner | 2026-06-29 | **Pass** | None | Admin login sau hết khóa → 200, reset |
| TC-WEB-DT-PW-015 | Web / API | AI Runner | 2026-06-29 | **Pass** | None | Locked + many attempts: đúng/sai đều 403, attempts không tăng |
| TC-WEB-DT-PW-016 | Web / API | AI Runner | 2026-06-29 | **Fail(Bug)** | BUG-FR02-001 | Sai nhiều lần: attempts=6 (actual) vs 5 (spec) |
| TC-WEB-DT-PW-017 | Web / API | AI Runner | 2026-06-29 | **Pass** | None | Đúng password sau hết khóa (attempts=5) → 200, reset hoàn toàn |
| TC-WEB-DT-PW-018 | Web / API | AI Runner | 2026-06-29 | **Pass** | None | Admin locked + sai password → 403, attempts không tăng |

---

**Allowed Results**: `Pass` | `Fail` | `Fail(Bug)` | `Blocked` | `Not Run`

---

## Summary

| Metric | Value |
|---|---|
| Total Test Cases | 18 |
| **Pass** | **12** |
| **Fail (unrelated to known bug)** | **0** |
| **Fail (Bug known — BUG-FR02-001)** | **6** |
| Blocked | 0 |
| Not Run | 0 |
| Pass Rate (excl. known bugs) | **100%** |
| Pass Rate (incl. known bugs) | **66.7%** |

---

## Bug Confirmed by Execution

**BUG-FR02-001** — `login_attempts += 2` (server.js line 54):

| Scenario | Expected (spec) | Actual (code) |
|---|---|---|
| Sai lần 1 (attempts bắt đầu = 0) | attempts = 1 | attempts = 2 |
| Sai lần 2 (attempts bắt đầu = 1) | attempts = 2, NOT locked | attempts = 3, **LOCKED** |
| Tài khoản bị khóa lần sai thứ | **3** | **2** |
