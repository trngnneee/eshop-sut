# TC-WEB-DT-PW-012: Đăng nhập thành công sau khi hết thời gian khóa (User)

## Requirement ID
FR02

## Module / Test Type / Technique
Web / Functional / Decision Table + Pairwise

## Source Design
- Decision Rule ID(s): R015
- Pairwise Case ID: PW012

## Preconditions
- Server đang chạy tại `http://localhost:3000`
- Tài khoản `test@eshop.com` tồn tại
- DB: `login_attempts = 3`, `locked_until = <thời điểm đã qua>` (đã hết hạn khóa)

## Test Data
| Field | Value | Class |
|---|---|---|
| email | `test@eshop.com` | Valid |
| password | `Test1234!` | Valid — đúng mật khẩu |
| DB locked_until | Quá khứ (e.g., datetime('now', '-1 minute')) | Boundary — hết hạn khóa |

## Test Steps
1. Thiết lập DB: `UPDATE users SET login_attempts = 3, locked_until = datetime('now', '-1 minute') WHERE email = 'test@eshop.com'`
2. Chờ đến sau thời điểm `locked_until` (nếu cần)
3. Gửi `POST /api/login` với body `{ "email": "test@eshop.com", "password": "Test1234!" }`
4. Kiểm tra HTTP status code
5. Kiểm tra DB sau đăng nhập thành công

## Expected Result
- HTTP status: `200`
- Body: `{ "message": "Login successful", "token": "<jwt>", ... }`
- DB: `login_attempts = 0`, `locked_until = NULL` (reset sau khi đăng nhập thành công)

## Status / Related Bugs
**Pass** / None
