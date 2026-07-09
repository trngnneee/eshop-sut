# TC-WEB-DT-PW-018: Admin bị khóa — sai mật khẩu → từ chối 403

## Requirement ID
FR02

## Module / Test Type / Technique
Web / Functional / Decision Table + Pairwise

## Source Design
- Decision Rule ID(s): R028
- Pairwise Case ID: PW018

## Preconditions
- Server đang chạy tại `http://localhost:3000`
- Tài khoản `admin@eshop.com` đang bị khóa
- DB: `login_attempts = 3`, `locked_until = <trong tương lai>`

## Test Data
| Field | Value | Class |
|---|---|---|
| email | `admin@eshop.com` | Valid |
| password | `wrongpassword` | Invalid |
| DB locked_until | NOW + 120s | Security — admin locked |

## Test Steps
1. Thiết lập DB: `UPDATE users SET login_attempts = 3, locked_until = datetime('now', '+2 minutes') WHERE email = 'admin@eshop.com'`
2. Gửi `POST /api/login` với body `{ "email": "admin@eshop.com", "password": "wrongpassword" }`
3. Kiểm tra HTTP status code — phải là 403 (không phải 401)

## Expected Result
- HTTP status: `403`
- Body: `{ "error": "Tài khoản đã bị khóa. Vui lòng thử lại sau." }`
- DB: `login_attempts` KHÔNG tăng (lock check trước password check)

## Status / Related Bugs
**Pass** / None
