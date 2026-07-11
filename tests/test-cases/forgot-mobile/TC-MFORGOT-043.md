# TC-MFORGOT-043: Cả hai trường mật khẩu cùng ở biên tối đa (50 ký tự) — Cross-boundary

## Requirement ID
FR-22

## Module / Test type / Technique
Forgot Password (Mobile) / Functional / BVA – Cross-boundary

## Boundary under test
Mật khẩu mới + Xác nhận mật khẩu đồng thời tại max (50 ký tự)

## Preconditions
- Đã hoàn thành Bước 1 thành công với Email `test@eshop.com` và đang ở Bước 2

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| OTP | [OTP hợp lệ từ Bước 1] |
| Mật khẩu mới | Aa1!xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx |
| Xác nhận mật khẩu mới | Aa1!xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx |

## Test steps
> **Lưu ý:** Theo FR-22, Bước 2 phải có trường Xác nhận mật khẩu mới (nếu có trên UI).
1. Hoàn thành Bước 1 với Email `test@eshop.com`.
2. Nhập OTP hợp lệ.
3. Nhập cả Mật khẩu mới và Xác nhận mật khẩu đều có độ dài 50 ký tự và khớp nhau.
4. Bấm "Đặt lại mật khẩu".

## Expected result
- Hệ thống chấp nhận cả hai trường ở biên tối đa và đặt lại mật khẩu thành công.

## Valid / Invalid
Valid

## Status / Related bugs
Fail / #7