# TC-WEB-DT-PW-002: Đăng nhập thành công với tài khoản Admin hợp lệ

## Requirement ID
FR02

## Module / Test Type / Technique
Web / Functional / Decision Table + Pairwise

## Source Design
- Decision Rule ID(s): R002
- Pairwise Case ID: PW002

## Preconditions
- Server đang chạy tại `http://localhost:3000`
- Tài khoản `admin@eshop.com` / `Admin123!` tồn tại, role=admin
- `login_attempts = 0`, `locked_until = NULL`

## Test Data
| Field | Value | Class |
|---|---|---|
| email | `admin@eshop.com` | Valid |
| password | `Admin123!` | Valid — đúng mật khẩu |

## Test Steps
1. Gửi `POST /api/login` với body `{ "email": "admin@eshop.com", "password": "Admin123!" }`
2. Kiểm tra HTTP status code
3. Kiểm tra body response có `token` và `user.role = "admin"`
4. Kiểm tra DB: `login_attempts = 0`, `locked_until = NULL`

## Expected Result
- HTTP status: `200`
- Body: `{ "message": "Login successful", "token": "<jwt>", "user": { "role": "admin", ... } }`
- DB: `login_attempts = 0`, `locked_until = NULL`

## Status / Related Bugs
**Pass** / None
