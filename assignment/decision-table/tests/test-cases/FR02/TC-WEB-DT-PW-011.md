# TC-WEB-DT-PW-011: Admin sai mật khẩu lần đầu — chưa bị khóa

## Requirement ID
FR02

## Module / Test Type / Technique
Web / Functional / Decision Table + Pairwise

## Source Design
- Decision Rule ID(s): R020
- Pairwise Case ID: PW011

## Preconditions
- Server đang chạy tại `http://localhost:3000`
- Tài khoản `admin@eshop.com` tồn tại, role=admin
- DB: `login_attempts = 0`, `locked_until = NULL`

## Test Data
| Field | Value | Class |
|---|---|---|
| email | `admin@eshop.com` | Valid |
| password | `badpassword` | Invalid |
| DB login_attempts before | 0 | Boundary |

## Test Steps
1. Đảm bảo DB: `UPDATE users SET login_attempts = 0, locked_until = NULL WHERE email = 'admin@eshop.com'`
2. Gửi `POST /api/login` với body `{ "email": "admin@eshop.com", "password": "badpassword" }`
3. Kiểm tra HTTP status code
4. Kiểm tra DB sau request

## Expected Result (theo spec đúng)
- HTTP status: `401`
- Body: `{ "error": "Invalid email or password" }`
- DB: `login_attempts = 1`, `locked_until = NULL`

## Actual Behavior (với bug +2)
- DB: `login_attempts = 2`, `locked_until = NULL` ← **BUG counter**

## Status / Related Bugs
**Fail(Bug)** / BUG-FR02-001
