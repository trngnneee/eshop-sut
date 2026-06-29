# TC-FORGOT-009: Kiểm thử OTP sai giá trị (đúng định dạng 6 chữ số)

## Requirement ID
FR-03

## Module / Test type / Technique
Forgot Password / Functional / Domain Testing – Equivalence Partitioning

## Preconditions
- Đã hoàn thành Bước 1 thành công với Email `test@eshop.com` và đang ở Bước 2
- OTP thực tế hiển thị trên màn hình khác với giá trị thử nghiệm

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| OTP | 000000 |
| Mật khẩu mới | NewPass1! |
| Xác nhận mật khẩu mới | NewPass1! |

## Test steps
1. Hoàn thành Bước 1 với Email `test@eshop.com` và ghi nhận OTP hiển thị.
2. Nhập OTP `000000` (khác OTP thực tế).
3. Nhập Mật khẩu mới và Xác nhận mật khẩu hợp lệ `NewPass1!`.
4. Bấm "Đặt lại mật khẩu".

## Expected result
- Hệ thống từ chối vì OTP không đúng.
- Hiển thị thông báo lỗi OTP không hợp lệ; mật khẩu không được thay đổi.

## Sub-domains covered
SD-O05 (OTP đúng định dạng nhưng sai giá trị)

## Type
Invalid

## Status / Related bugs
Fail / #7
