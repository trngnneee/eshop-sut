# TC-WEB-DT-PW-013: Sai mật khẩu sau hết hạn khóa → bị khóa lại (User)

## Requirement ID
FR02

## Module / Test Type / Technique
Web / Functional / Decision Table + Pairwise

## Source Design
- Decision Rule ID(s): R033
- Pairwise Case ID: PW013

## Preconditions
- Server đang chạy tại `http://localhost:3000`
- Tài khoản `test@eshop.com` tồn tại
- DB: `login_attempts = 3`, `locked_until = <đã hết hạn>`

## Test Data
| Field | Value | Class |
|---|---|---|
| email | `test@eshop.com` | Valid |
| password | `WrongPass!` | Invalid |
| DB locked_until | Quá khứ (đã hết hạn khóa) | Boundary — expired lock |

## Test Steps
1. Thiết lập DB: `UPDATE users SET login_attempts = 3, locked_until = datetime('now', '-1 minute') WHERE email = 'test@eshop.com'`
2. Gửi `POST /api/login` với body `{ "email": "test@eshop.com", "password": "WrongPass!" }`
3. Kiểm tra HTTP status code
4. Kiểm tra DB: `locked_until` có bị set lại không

## Expected Result (theo spec đúng)
- HTTP status: `401`
- DB: `login_attempts = 4` (tăng +1 theo spec), `locked_until = NOW + 180s` (vì vẫn >= 3)

## Actual Behavior (với bug +2)
- DB: `login_attempts = 5` (3+2), `locked_until = NOW + 180s` ← **BUG counter**

## Status / Related Bugs
**Fail(Bug)** / BUG-FR02-001
