# TC-WEB-DT-PW-007: Tài khoản bị khóa — sai mật khẩu vẫn trả 403 (lock check priority)

## Requirement ID
FR02

## Module / Test Type / Technique
Web / Functional / Decision Table + Pairwise

## Source Design
- Decision Rule ID(s): R027
- Pairwise Case ID: PW007

## Preconditions
- Server đang chạy tại `http://localhost:3000`
- Tài khoản `test@eshop.com` đang bị khóa (`locked_until` trong tương lai)
- `login_attempts = 3`

## Test Data
| Field | Value | Class |
|---|---|---|
| email | `test@eshop.com` | Valid |
| password | `WrongPass!` | Invalid |
| DB locked_until | NOW + 120 giây | Security — locked state |

## Test Steps
1. Thiết lập DB: `UPDATE users SET login_attempts = 3, locked_until = datetime('now', '+2 minutes') WHERE email = 'test@eshop.com'`
2. Gửi `POST /api/login` với body `{ "email": "test@eshop.com", "password": "WrongPass!" }`
3. Kiểm tra HTTP status code: phải là 403 (không phải 401)
4. Kiểm tra server không tăng `login_attempts` trong khi đang khóa

## Expected Result
- HTTP status: `403` (lock check có priority trước password check)
- Body: `{ "error": "Tài khoản đã bị khóa. Vui lòng thử lại sau." }`
- DB: `login_attempts` KHÔNG tăng thêm

## Status / Related Bugs
**Pass** / None
