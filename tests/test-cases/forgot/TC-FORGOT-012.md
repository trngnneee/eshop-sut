# TC-FORGOT-012: Kiểm thử Mật khẩu mới quá ngắn (dưới 8 ký tự)

## Requirement ID
FR-03

## Module / Test type / Technique
Forgot Password / Functional / Domain Testing – Equivalence Partitioning

## Preconditions
- Đã hoàn thành Bước 1 thành công với Email `test@eshop.com` và đang ở Bước 2

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| OTP | [OTP hợp lệ từ Bước 1] |
| Mật khẩu mới | Test1!@ |
| Xác nhận mật khẩu mới | Test1!@ |

## Test steps
1. Hoàn thành Bước 1 với Email `test@eshop.com`.
2. Nhập OTP hợp lệ.
3. Nhập Mật khẩu mới `Test1!@` (7 ký tự) và Xác nhận mật khẩu khớp.
4. Bấm "Đặt lại mật khẩu".

## Expected result
- Hệ thống từ chối vì mật khẩu không đạt tối thiểu 8 ký tự (theo FR-01).
- Mật khẩu không được thay đổi.

## Sub-domains covered
SD-P02 (mật khẩu quá ngắn)

## Type
Invalid

## Status / Related bugs
Fail / #7
