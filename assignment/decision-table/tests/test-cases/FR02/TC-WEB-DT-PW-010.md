# TC-WEB-DT-PW-010: Sai mật khẩu lần đầu — chưa bị khóa (User)

## Requirement ID
FR02

## Module / Test Type / Technique
Web / Functional / Decision Table + Pairwise

## Source Design
- Decision Rule ID(s): R019
- Pairwise Case ID: PW010

## Preconditions
- Server đang chạy tại `http://localhost:3000`
- Tài khoản `test@eshop.com` tồn tại
- DB: `login_attempts = 0`, `locked_until = NULL` (tài khoản sạch)

## Test Data
| Field | Value | Class |
|---|---|---|
| email | `test@eshop.com` | Valid |
| password | `WrongPass!` | Invalid — sai mật khẩu |
| DB login_attempts before | 0 | Boundary — lần sai đầu tiên |

## Test Steps
1. Đảm bảo DB: `UPDATE users SET login_attempts = 0, locked_until = NULL WHERE email = 'test@eshop.com'`
2. Gửi `POST /api/login` với body `{ "email": "test@eshop.com", "password": "WrongPass!" }`
3. Kiểm tra HTTP status code
4. Kiểm tra DB: `login_attempts` và `locked_until` sau request

## Expected Result (theo spec đúng)
- HTTP status: `401`
- Body: `{ "error": "Invalid email or password" }`
- DB: `login_attempts = 1`, `locked_until = NULL`

## Actual Behavior (với bug +2)
- DB: `login_attempts = 2` ← **BUG: counter tăng gấp đôi**
- `locked_until = NULL` (vẫn chưa bị khóa — 2 < 3)

## Status / Related Bugs
**Fail(Bug)** / BUG-FR02-001
