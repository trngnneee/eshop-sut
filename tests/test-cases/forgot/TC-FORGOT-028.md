# TC-FORGOT-028: Kiểm thử OTP với độ dài biên đúng 6 chữ số (on-point)

## Requirement ID
FR-03

## Module / Test type / Technique
Forgot Password / Functional / Boundary Value Analysis

## Boundary under test
OTP at min/max — value: [OTP 6 chữ số hợp lệ từ Bước 1]

## Preconditions
- Đã hoàn thành Bước 1 thành công với Email `test@eshop.com` và đang ở Bước 2

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| OTP | [OTP 6 chữ số hiển thị trên màn hình] |
| Mật khẩu mới | NewPass1! |
| Xác nhận mật khẩu mới | NewPass1! |

## Test steps
1. Hoàn thành Bước 1 với Email `test@eshop.com` và ghi nhận OTP 6 chữ số.
2. Nhập OTP vừa nhận.
3. Nhập Mật khẩu mới và Xác nhận mật khẩu hợp lệ `NewPass1!`.
4. Bấm "Đặt lại mật khẩu".

## Expected result
- Hệ thống chấp nhận OTP đúng 6 chữ số và đặt lại mật khẩu thành công.

## Valid / Invalid
Valid

## Status / Related bugs
Not Run / None
