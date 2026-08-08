# TC-LOCK-BVA-006: Kiểm tra đăng nhập đúng thời điểm khóa vừa hết hạn

## Requirement ID
FR-02

## Module / Test type / Technique
Lockout / Boundary Value Analysis (BVA)

## Preconditions
- Tài khoản đang bị khóa.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email | test@eshop.com |
| Mật khẩu đúng | ValidPassword1! |

## Test steps
1. Gửi yêu cầu login đúng chính xác vào mili-giây mà thời gian khóa kết thúc (so khớp trường thời gian khóa).

## Expected result
- Hệ thống xử lý an toàn, cho phép đăng nhập thành công, reset trạng thái khóa về mặc định.

## Status / Related bugs
Not Run / None
