# TC-WEB-DT-PW-014: Admin đăng nhập thành công sau hết hạn khóa

## Requirement ID
FR02

## Module / Test Type / Technique
Web / Functional / Decision Table + Pairwise

## Source Design
- Decision Rule ID(s): R016
- Pairwise Case ID: PW014

## Preconditions
- Server đang chạy tại `http://localhost:3000`
- Tài khoản `admin@eshop.com` tồn tại, role=admin
- DB: `login_attempts = 3`, `locked_until = <đã hết hạn>`

## Test Data
| Field | Value | Class |
|---|---|---|
| email | `admin@eshop.com` | Valid |
| password | `Admin123!` | Valid — đúng mật khẩu |
| DB locked_until | Quá khứ | Boundary — expired lock |

## Test Steps
1. Thiết lập DB: `UPDATE users SET login_attempts = 3, locked_until = datetime('now', '-1 minute') WHERE email = 'admin@eshop.com'`
2. Gửi `POST /api/login` với body `{ "email": "admin@eshop.com", "password": "Admin123!" }`
3. Kiểm tra HTTP status code
4. Kiểm tra body có `role = "admin"`
5. Kiểm tra DB: `login_attempts = 0`, `locked_until = NULL`

## Expected Result
- HTTP status: `200`
- Body: `{ "message": "Login successful", "token": "<jwt>", "user": { "role": "admin", ... } }`
- DB: `login_attempts = 0`, `locked_until = NULL`

## Status / Related Bugs
**Pass** / None
