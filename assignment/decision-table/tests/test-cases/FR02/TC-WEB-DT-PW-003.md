# TC-WEB-DT-PW-003: Sai mật khẩu lần 2 gây khóa tài khoản (BUG — should be lần 3)

## Requirement ID
FR02

## Module / Test Type / Technique
Web / Functional / Decision Table + Pairwise

## Source Design
- Decision Rule ID(s): R021
- Pairwise Case ID: PW003

## Preconditions
- Server đang chạy tại `http://localhost:3000`
- Tài khoản `test@eshop.com` tồn tại
- DB: `login_attempts = 1` (đã sai 1 lần trước đó — nhưng với bug +2, attempt counter thực tế là 2 sau lần đầu tiên)
- `locked_until = NULL`

> **Ghi chú Bug**: Do `login_attempts += 2` (dòng 54, server.js), sau lần sai đầu tiên attempts=2. Lần sai tiếp theo: 2+2=4 ≥ 3 → locked. Theo spec đúng, phải sai 3 lần mới khóa.

## Test Data
| Field | Value | Class |
|---|---|---|
| email | `test@eshop.com` | Valid |
| password | `WrongPass!` | Invalid — sai mật khẩu |
| DB login_attempts before | 1 | Boundary — ngưỡng khóa |

## Test Steps
1. Thiết lập DB: `UPDATE users SET login_attempts = 1, locked_until = NULL WHERE email = 'test@eshop.com'`
2. Gửi `POST /api/login` với body `{ "email": "test@eshop.com", "password": "WrongPass!" }`
3. Kiểm tra HTTP status code
4. Kiểm tra DB: `login_attempts` và `locked_until` sau request

## Expected Result (theo spec — PASS nếu hệ thống đúng)
- HTTP status: `401` (sai lần 2, theo spec chưa đủ ngưỡng 3 lần → chưa khóa)
- DB: `login_attempts = 2`, `locked_until = NULL`

## Actual Behavior (với bug hiện tại — FAIL)
- HTTP status: `401`
- DB: `login_attempts = 3`, `locked_until = <NOW + 180s>` ← **BUG: bị khóa sớm hơn 1 lần**

## Status / Related Bugs
**Fail(Bug)** / BUG-FR02-001
