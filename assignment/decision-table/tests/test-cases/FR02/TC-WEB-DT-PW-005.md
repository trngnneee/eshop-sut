# TC-WEB-DT-PW-005: Tài khoản bị khóa — đúng mật khẩu vẫn bị từ chối (User)

## Requirement ID
FR02

## Module / Test Type / Technique
Web / Functional / Decision Table + Pairwise

## Source Design
- Decision Rule ID(s): R009
- Pairwise Case ID: PW005

## Preconditions
- Server đang chạy tại `http://localhost:3000`
- Tài khoản `test@eshop.com` tồn tại, mật khẩu đúng là `Test1234!`
- DB: `login_attempts = 3`, `locked_until = <thời điểm trong tương lai>` (tài khoản đang bị khóa)

## Test Data
| Field | Value | Class |
|---|---|---|
| email | `test@eshop.com` | Valid |
| password | `Test1234!` | Valid — đúng mật khẩu |
| DB locked_until | NOW + 120 giây (còn 2 phút khóa) | Security — locked account |

## Test Steps
1. Thiết lập DB: `UPDATE users SET login_attempts = 3, locked_until = datetime('now', '+2 minutes') WHERE email = 'test@eshop.com'`
2. Gửi `POST /api/login` với body `{ "email": "test@eshop.com", "password": "Test1234!" }`
3. Kiểm tra HTTP status code
4. Kiểm tra message trong response body

## Expected Result
- HTTP status: `403`
- Body: `{ "error": "Tài khoản đã bị khóa. Vui lòng thử lại sau." }`
- DB: `locked_until` không thay đổi, `login_attempts` không thay đổi

## Status / Related Bugs
**Pass** / None
