# TC-WEB-DT-PW-001: Đăng nhập thành công với tài khoản User hợp lệ

## Requirement ID
FR02

## Module / Test Type / Technique
Web / Functional / Decision Table + Pairwise

## Source Design
- Decision Rule ID(s): R001
- Pairwise Case ID: PW001

## Preconditions
- Server đang chạy tại `http://localhost:3000`
- Tài khoản `test@eshop.com` / `Test1234!` tồn tại, role=user
- `login_attempts = 0`, `locked_until = NULL`

## Test Data
| Field | Value | Class |
|---|---|---|
| email | `test@eshop.com` | Valid |
| password | `Test1234!` | Valid — đúng mật khẩu |

## Test Steps
1. Gửi `POST /api/login` với body `{ "email": "test@eshop.com", "password": "Test1234!" }`
2. Kiểm tra HTTP status code
3. Kiểm tra body response có chứa `token` và `user`
4. Kiểm tra DB: `login_attempts = 0`, `locked_until = NULL` cho user này

## Expected Result
- HTTP status: `200`
- Body: `{ "message": "Login successful", "token": "<jwt>", "user": { "role": "user", ... } }`
- DB: `login_attempts = 0`, `locked_until = NULL`

## Status / Related Bugs
**Pass** / None
