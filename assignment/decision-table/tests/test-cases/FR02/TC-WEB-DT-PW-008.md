# TC-WEB-DT-PW-008: Đăng nhập với email không tồn tại

## Requirement ID
FR02

## Module / Test Type / Technique
Web / Functional / Decision Table + Pairwise

## Source Design
- Decision Rule ID(s): R037
- Pairwise Case ID: PW008

## Preconditions
- Server đang chạy tại `http://localhost:3000`
- Email `nonexistent@test.com` không có trong DB

## Test Data
| Field | Value | Class |
|---|---|---|
| email | `nonexistent@test.com` | Invalid — email không tồn tại |
| password | `AnyPassword123!` | Bất kỳ |

## Test Steps
1. Gửi `POST /api/login` với body `{ "email": "nonexistent@test.com", "password": "AnyPassword123!" }`
2. Kiểm tra HTTP status code
3. Kiểm tra message trong response body — phải KHÔNG tiết lộ "email không tồn tại"

## Expected Result
- HTTP status: `401`
- Body: `{ "error": "Invalid email or password" }` (không phải "Email not found" — tránh user enumeration)
- DB: Không có gì thay đổi

## Status / Related Bugs
**Pass** / None
