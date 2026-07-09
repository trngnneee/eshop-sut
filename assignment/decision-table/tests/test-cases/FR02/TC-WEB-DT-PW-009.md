# TC-WEB-DT-PW-009: Đúng mật khẩu sau 1 lần sai — reset attempts về 0

## Requirement ID
FR02

## Module / Test Type / Technique
Web / Functional / Decision Table + Pairwise

## Source Design
- Decision Rule ID(s): R003
- Pairwise Case ID: PW009

## Preconditions
- Server đang chạy tại `http://localhost:3000`
- Tài khoản `test@eshop.com` tồn tại
- DB: `login_attempts = 1`, `locked_until = NULL`

## Test Data
| Field | Value | Class |
|---|---|---|
| email | `test@eshop.com` | Valid |
| password | `Test1234!` | Valid — đúng mật khẩu |
| DB login_attempts before | 1 | Boundary — 1 lần sai trước |

## Test Steps
1. Thiết lập DB: `UPDATE users SET login_attempts = 1, locked_until = NULL WHERE email = 'test@eshop.com'`
2. Gửi `POST /api/login` với body `{ "email": "test@eshop.com", "password": "Test1234!" }`
3. Kiểm tra HTTP status code
4. Kiểm tra DB: `login_attempts` phải được reset về 0

## Expected Result
- HTTP status: `200`
- Body: `{ "message": "Login successful", "token": "<jwt>", ... }`
- DB: `login_attempts = 0`, `locked_until = NULL` (đã reset)

## Status / Related Bugs
**Pass** / None
