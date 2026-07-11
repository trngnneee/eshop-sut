# TC-MFORGOT-SUP-003: Backend từ chối mật khẩu yếu khi reset (Mobile flow)

## Requirement ID
FR-22 (FR-01 password rules)

## Module / Test type / Technique
Forgot Password (Mobile) / Functional / Domain Testing – Supplementary

## Preconditions
- Đã lấy OTP hợp lệ cho `test@eshop.com` qua API (dùng chung backend với Mobile)

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| newPassword | weakpass |

## Test steps
1. Gọi `POST /api/reset-password` với email, OTP hợp lệ và `newPassword: "weakpass"`.
2. Quan sát HTTP status và body.
3. (Tùy chọn) Lặp qua Mobile Bước 2 với cùng OTP và mật khẩu yếu.

## Expected result
- API trả lỗi 4xx và **không** cập nhật mật khẩu (theo FR-01).
- Mobile không cho hoàn tất reset với mật khẩu yếu.

## Sub-domains covered
GAP-04 — server-side password validation

## Type
Invalid

## Status / Related bugs
Fail / #10