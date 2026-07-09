# TC-WEB-DT-PW-004: Admin sai mật khẩu lần 2 gây khóa tài khoản (BUG)

## Requirement ID
FR02

## Module / Test Type / Technique
Web / Functional / Decision Table + Pairwise

## Source Design
- Decision Rule ID(s): R022
- Pairwise Case ID: PW004

## Preconditions
- Server đang chạy tại `http://localhost:3000`
- Tài khoản `admin@eshop.com` tồn tại, role=admin
- DB: `login_attempts = 1`, `locked_until = NULL`

## Test Data
| Field | Value | Class |
|---|---|---|
| email | `admin@eshop.com` | Valid |
| password | `wrongpassword` | Invalid |
| DB login_attempts before | 1 | Boundary |

## Test Steps
1. Thiết lập DB: `UPDATE users SET login_attempts = 1, locked_until = NULL WHERE email = 'admin@eshop.com'`
2. Gửi `POST /api/login` với body `{ "email": "admin@eshop.com", "password": "wrongpassword" }`
3. Kiểm tra HTTP status code
4. Kiểm tra DB: `locked_until` sau request

## Expected Result (theo spec)
- HTTP status: `401`
- DB: `login_attempts = 2`, `locked_until = NULL` (chưa đủ 3 lần)

## Actual Behavior (với bug)
- HTTP status: `401`
- DB: `login_attempts = 3`, `locked_until = <NOW + 180s>` ← **BUG**

## Status / Related Bugs
**Fail(Bug)** / BUG-FR02-001
