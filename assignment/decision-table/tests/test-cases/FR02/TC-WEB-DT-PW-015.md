# TC-WEB-DT-PW-015: Tài khoản khóa nhiều lần sai — đúng/sai password đều bị từ chối (attempts ≥2)

## Requirement ID
FR02

## Module / Test Type / Technique
Web / Functional / Decision Table + Pairwise

## Source Design
- Decision Rule ID(s): R011, R029
- Pairwise Case ID: PW015

## Preconditions
- Server đang chạy tại `http://localhost:3000`
- Tài khoản `test@eshop.com` đang bị khóa
- DB: `login_attempts = 5` (≥2), `locked_until = <trong tương lai>`

## Test Data
| Field | Value | Class |
|---|---|---|
| email | `test@eshop.com` | Valid |
| password | `Test1234!` (đúng) HOẶC `WrongPass!` (sai) | Valid/Invalid |
| DB login_attempts | 5 | Boundary — nhiều lần sai |
| DB locked_until | NOW + 120s | Security |

## Test Steps
1. Thiết lập DB: `UPDATE users SET login_attempts = 5, locked_until = datetime('now', '+2 minutes') WHERE email = 'test@eshop.com'`
2. **Test với đúng password**: Gửi `POST /api/login` với `password = "Test1234!"`
3. Kiểm tra response
4. **Test với sai password**: Gửi `POST /api/login` với `password = "WrongPass!"`
5. Kiểm tra response

## Expected Result
**Cả hai sub-test:**
- HTTP status: `403`
- Body: `{ "error": "Tài khoản đã bị khóa. Vui lòng thử lại sau." }`
- DB: `login_attempts` KHÔNG thay đổi (lock check trước password check)

## Status / Related Bugs
**Pass** / None
