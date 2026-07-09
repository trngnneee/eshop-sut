# TC-WEB-DT-PW-017: Đúng mật khẩu sau hết khóa — attempts ≥2 trước đó (User)

## Requirement ID
FR02

## Module / Test Type / Technique
Web / Functional / Decision Table + Pairwise

## Source Design
- Decision Rule ID(s): R017
- Pairwise Case ID: PW017

## Preconditions
- Server đang chạy tại `http://localhost:3000`
- Tài khoản `test@eshop.com` tồn tại
- DB: `login_attempts = 5`, `locked_until = <đã hết hạn>`

## Test Data
| Field | Value | Class |
|---|---|---|
| email | `test@eshop.com` | Valid |
| password | `Test1234!` | Valid — đúng mật khẩu |
| DB login_attempts | 5 | Edge |
| DB locked_until | Quá khứ (hết hạn) | Boundary — expired lock |

## Test Steps
1. Thiết lập DB: `UPDATE users SET login_attempts = 5, locked_until = datetime('now', '-1 minute') WHERE email = 'test@eshop.com'`
2. Gửi `POST /api/login` với body `{ "email": "test@eshop.com", "password": "Test1234!" }`
3. Kiểm tra HTTP status code
4. Kiểm tra DB: `login_attempts` và `locked_until` sau login thành công

## Expected Result
- HTTP status: `200`
- Body: `{ "message": "Login successful", "token": "<jwt>", ... }`
- DB: `login_attempts = 0`, `locked_until = NULL` (reset hoàn toàn)

## Status / Related Bugs
**Pass** / None
