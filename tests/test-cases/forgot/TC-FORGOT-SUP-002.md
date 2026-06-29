# TC-FORGOT-SUP-002: Backend từ chối mật khẩu yếu khi reset

## Requirement ID
FR-03 (FR-01 password rules)

## Module / Test type / Technique
Forgot Password / Functional / Domain Testing – Supplementary

## Preconditions
- Đã lấy OTP hợp lệ cho `test@eshop.com` qua API

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| newPassword | weakpass |

## Test steps
1. Gọi `POST /api/reset-password` với email, OTP hợp lệ và `newPassword: "weakpass"`.
2. Quan sát HTTP status và body.

## Expected result
- API trả lỗi 4xx và **không** cập nhật mật khẩu (theo quy tắc FR-01).

## Sub-domains covered
GAP-03 — server-side password validation

## Type
Invalid

## Status / Related bugs
Not Run / #10
