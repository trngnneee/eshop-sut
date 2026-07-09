# TC-WEB-DT-PW-016: Sai mật khẩu nhiều lần liên tiếp — tăng attempts và khóa (attempts ≥2)

## Requirement ID
FR02

## Module / Test Type / Technique
Web / Functional / Decision Table + Pairwise

## Source Design
- Decision Rule ID(s): R023
- Pairwise Case ID: PW016

## Preconditions
- Server đang chạy tại `http://localhost:3000`
- Tài khoản `test@eshop.com` tồn tại
- DB: `login_attempts = 4`, `locked_until = NULL` (giả lập bằng DB manipulation)

## Test Data
| Field | Value | Class |
|---|---|---|
| email | `test@eshop.com` | Valid |
| password | `WrongPass!` | Invalid |
| DB login_attempts before | 4 | Edge — nhiều lần sai |

## Test Steps
1. Thiết lập DB: `UPDATE users SET login_attempts = 4, locked_until = NULL WHERE email = 'test@eshop.com'`
2. Gửi `POST /api/login` với body `{ "email": "test@eshop.com", "password": "WrongPass!" }`
3. Kiểm tra HTTP status
4. Kiểm tra DB: `login_attempts` sau request

## Expected Result
- HTTP status: `401`
- DB: `login_attempts = 5` (hoặc 6 với bug), `locked_until` đã set (vì >= 3)

## Status / Related Bugs
**Fail(Bug)** / BUG-FR02-001
