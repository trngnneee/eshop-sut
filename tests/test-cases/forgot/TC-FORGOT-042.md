# TC-FORGOT-042: Cả hai trường mật khẩu cùng ở biên tối thiểu (8 ký tự) — Cross-boundary

## Requirement ID
FR-03

## Module / Test type / Technique
Forgot Password / Functional / BVA – Cross-boundary

## Boundary under test
Mật khẩu mới + Xác nhận mật khẩu đồng thời tại min (8 ký tự)

## Preconditions
- Đã hoàn thành Bước 1 thành công với Email `test@eshop.com` và đang ở Bước 2

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| OTP | [OTP hợp lệ từ Bước 1] |
| Mật khẩu mới | Abc@1234 |
| Xác nhận mật khẩu mới | Abc@1234 |

## Test steps
1. Hoàn thành Bước 1 với Email `test@eshop.com`.
2. Nhập OTP hợp lệ.
3. Nhập cả Mật khẩu mới và Xác nhận mật khẩu đều `Abc@1234` (8 ký tự).
4. Bấm "Đặt lại mật khẩu".

## Expected result
- Hệ thống chấp nhận cả hai trường ở biên tối thiểu và đặt lại mật khẩu thành công.

## Valid / Invalid
Valid

## Status / Related bugs
Fail / #7
