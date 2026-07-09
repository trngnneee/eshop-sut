# TC-WEB-DT-PW-006: Admin bị khóa — đúng mật khẩu vẫn bị từ chối

## Requirement ID
FR02

## Module / Test Type / Technique
Web / Functional / Decision Table + Pairwise

## Source Design
- Decision Rule ID(s): R010
- Pairwise Case ID: PW006

## Preconditions
- Server đang chạy tại `http://localhost:3000`
- Tài khoản `admin@eshop.com` tồn tại, mật khẩu đúng là `Admin123!`
- DB: `locked_until = <thời điểm trong tương lai>`, tài khoản đang bị khóa

## Test Data
| Field | Value | Class |
|---|---|---|
| email | `admin@eshop.com` | Valid |
| password | `Admin123!` | Valid — đúng mật khẩu |
| DB locked_until | NOW + 120 giây | Security — admin locked |

## Test Steps
1. Thiết lập DB: `UPDATE users SET login_attempts = 3, locked_until = datetime('now', '+2 minutes') WHERE email = 'admin@eshop.com'`
2. Gửi `POST /api/login` với body `{ "email": "admin@eshop.com", "password": "Admin123!" }`
3. Kiểm tra HTTP status code
4. Kiểm tra message trong response body

## Expected Result
- HTTP status: `403`
- Body: `{ "error": "Tài khoản đã bị khóa. Vui lòng thử lại sau." }`
- DB: không thay đổi

## Status / Related Bugs
**Pass** / None
