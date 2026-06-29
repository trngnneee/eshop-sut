# TC-FORGOT-SUP-004: OTP không thể tái sử dụng sau reset thành công

## Requirement ID
FR-03

## Module / Test type / Technique
Forgot Password / Functional / Domain Testing – Supplementary

## Preconditions
- Đã reset mật khẩu thành công một lần với OTP `X`

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| OTP (lần 2) | X (cùng mã đã dùng) |

## Test steps
1. Hoàn tất reset mật khẩu thành công với OTP `X`.
2. Gọi lại `POST /api/reset-password` với cùng email, OTP `X`, và mật khẩu mới khác.

## Expected result
- Lần 2 bị từ chối (OTP đã vô hiệu / token cleared).

## Sub-domains covered
GAP-05 — OTP one-time use

## Type
Invalid

## Status / Related bugs
Not Run / None
