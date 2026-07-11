# TC-MFORGOT-SUP-007: Mật khẩu với ký tự đặc biệt ngoài whitelist FR-01

## Requirement ID
FR-22 (FR-01)

## Module / Test type / Technique
Forgot Password (Mobile) / Functional / Domain Testing – Supplementary

## Preconditions
- Mobile App (React Native + Expo) đang chạy và kết nối Backend API tại IP LAN máy chủ
- Đang ở Bước 2 với OTP hợp lệ

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| OTP | [OTP hợp lệ] |
| Mật khẩu mới | Test1234+ |

## Test steps
1. Hoàn thành Bước 1 với `test@eshop.com`.
2. Nhập OTP hợp lệ và mật khẩu `Test1234+` (ký tự `+` **không** thuộc `@$!%*?&`).
3. Bấm "Đặt lại mật khẩu".

## Expected result
- Theo FR-01: hệ thống **từ chối** vì ký tự đặc biệt không thuộc tập cho phép.
- Client Mobile không được chấp nhận chỉ vì regex `[^A-Za-z\\d]` rộng hơn đặc tả.

## Sub-domains covered
GAP-08 — FR-01 special-char whitelist

## Type
Invalid

## Status / Related bugs
Fail / #7